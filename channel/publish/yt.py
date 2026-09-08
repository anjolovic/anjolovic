"""Minimal YouTube Data API v3 client, standard library only.

Credentials come from the environment (YT_CLIENT_ID, YT_CLIENT_SECRET,
YT_REFRESH_TOKEN) or from YT_TOKEN_FILE (the file auth.py writes).
"""
import json
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
TOKEN_URL = "https://oauth2.googleapis.com/token"


class ApiError(RuntimeError):
    pass


class YouTube:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self._access = None
        self._exp = 0
        f = os.environ.get("YT_TOKEN_FILE")
        if f and Path(f).exists():
            d = json.loads(Path(f).read_text())
            self.client_id, self.client_secret, self.refresh = d["client_id"], d["client_secret"], d["refresh_token"]
        else:
            self.client_id = os.environ.get("YT_CLIENT_ID")
            self.client_secret = os.environ.get("YT_CLIENT_SECRET")
            self.refresh = os.environ.get("YT_REFRESH_TOKEN")
        if not dry_run and not all([self.client_id, self.client_secret, self.refresh]):
            raise ApiError("Missing YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN (or YT_TOKEN_FILE).")

    # ---------------------------------------------------------------- auth
    def token(self):
        if self._access and time.time() < self._exp - 60:
            return self._access
        body = urllib.parse.urlencode({
            "client_id": self.client_id, "client_secret": self.client_secret,
            "refresh_token": self.refresh, "grant_type": "refresh_token",
        }).encode()
        with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body)) as r:
            d = json.load(r)
        self._access, self._exp = d["access_token"], time.time() + d.get("expires_in", 3600)
        return self._access

    # ---------------------------------------------------------------- core
    def _req(self, method, url, params=None, body=None, headers=None, raw=None):
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
        h = {"Authorization": "Bearer " + self.token()}
        h.update(headers or {})
        data = None
        if body is not None:
            data = json.dumps(body).encode()
            h["Content-Type"] = "application/json; charset=UTF-8"
        if raw is not None:
            data = raw
        req = urllib.request.Request(url, data=data, method=method, headers=h)
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req) as r:
                    txt = r.read()
                    return json.loads(txt) if txt else {}, r.headers
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")
                if e.code in (500, 502, 503, 504) and attempt < 4:
                    time.sleep(2 ** attempt)
                    continue
                raise ApiError(f"{method} {url} -> {e.code}: {msg[:800]}")
        raise ApiError("unreachable")

    def call(self, method, resource, params=None, body=None):
        if self.dry_run:
            print(f"  [dry-run] {method} {resource} {json.dumps(params or {})} {json.dumps(body or {})[:300]}")
            return {"id": "dry-run-id"}
        out, _ = self._req(method, f"{API}/{resource}", params, body)
        return out

    def get_all(self, resource, params):
        items, tok = [], None
        while True:
            p = dict(params, maxResults=50)
            if tok:
                p["pageToken"] = tok
            d = self.call("GET", resource, p)
            items += d.get("items", [])
            tok = d.get("nextPageToken")
            if not tok:
                return items

    # ---------------------------------------------------------------- media
    def simple_upload(self, resource, params, path, content_type=None):
        """Single-request media upload (thumbnails, captions, banners, watermarks)."""
        if self.dry_run:
            print(f"  [dry-run] UPLOAD {resource} {json.dumps(params)} <- {path}")
            return {"id": "dry-run-id"}
        ct = content_type or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        p = dict(params, uploadType="media")
        out, _ = self._req("POST", f"{UPLOAD}/{resource}", p, headers={"Content-Type": ct},
                           raw=Path(path).read_bytes())
        return out

    def multipart_upload(self, resource, params, meta, path, content_type):
        """Metadata + media in one request (captions.insert needs this)."""
        if self.dry_run:
            print(f"  [dry-run] MULTIPART {resource} {json.dumps(params)} {json.dumps(meta)[:200]} <- {path}")
            return {"id": "dry-run-id"}
        boundary = "thenwhat" + str(int(time.time()))
        parts = (
            f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
            f"--{boundary}\r\nContent-Type: {content_type}\r\n\r\n"
        ).encode() + Path(path).read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        p = dict(params, uploadType="multipart")
        out, _ = self._req("POST", f"{UPLOAD}/{resource}", p,
                           headers={"Content-Type": f"multipart/related; boundary={boundary}"}, raw=parts)
        return out

    def resumable_video_upload(self, meta, path, chunk=8 * 1024 * 1024, progress=print):
        """videos.insert with a resumable session, 8 MB chunks, retry on 5xx/308."""
        if self.dry_run:
            print(f"  [dry-run] RESUMABLE videos.insert {json.dumps(meta)[:300]} <- {path}")
            return {"id": "dry-run-video-id"}
        path = Path(path)
        size = path.stat().st_size
        params = {"uploadType": "resumable", "part": "snippet,status"}
        _, hdr = self._req("POST", f"{UPLOAD}/videos", params, body=meta, headers={
            "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
        session = hdr["Location"]
        sent = 0
        with path.open("rb") as f:
            while sent < size:
                f.seek(sent)
                blob = f.read(chunk)
                end = sent + len(blob) - 1
                req = urllib.request.Request(session, data=blob, method="PUT", headers={
                    "Authorization": "Bearer " + self.token(),
                    "Content-Type": "video/mp4",
                    "Content-Range": f"bytes {sent}-{end}/{size}",
                })
                try:
                    with urllib.request.urlopen(req) as r:
                        return json.loads(r.read())  # 200/201: complete
                except urllib.error.HTTPError as e:
                    if e.code == 308:
                        rng = e.headers.get("Range")
                        sent = int(rng.split("-")[1]) + 1 if rng else end + 1
                        progress(f"  uploaded {sent/size:5.1%}")
                        continue
                    if e.code in (500, 502, 503, 504):
                        time.sleep(3)
                        # ask the server where we are
                        q = urllib.request.Request(session, data=b"", method="PUT", headers={
                            "Authorization": "Bearer " + self.token(), "Content-Range": f"bytes */{size}"})
                        try:
                            urllib.request.urlopen(q)
                        except urllib.error.HTTPError as e2:
                            if e2.code == 308:
                                rng = e2.headers.get("Range")
                                sent = int(rng.split("-")[1]) + 1 if rng else 0
                                continue
                        raise ApiError(f"upload failed: {e.code}")
                    raise ApiError(f"upload failed: {e.code} {e.read().decode(errors='replace')[:500]}")
        raise ApiError("upload ended without a completion response")


def download(url, dest, progress=print):
    """Stream a URL to disk. Skips if the file already exists with size > 0."""
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "thenwhat-publish/1.0"})
    with urllib.request.urlopen(req) as r, tmp.open("wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        got = 0
        while True:
            b = r.read(1024 * 1024)
            if not b:
                break
            f.write(b)
            got += len(b)
            if total:
                progress(f"  downloading {got/total:5.1%}")
    tmp.rename(dest)
    return dest
