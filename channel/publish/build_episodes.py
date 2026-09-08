#!/usr/bin/env python3
"""Generate channel/publish/episodes.json from the upload packages and the
asset manifest, so publish.py never carries copy that lives elsewhere.

Sources per episode:
  title, description, tags, pinned comment  <- production/**/YOUTUBE-PACKAGE.md
  final video URL, thumbnail A URL           <- production/ASSET-MANIFEST.json
  captions                                    <- production/**/captions.srt
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROD = ROOT / "production"
MANIFEST = json.loads((PROD / "ASSET-MANIFEST.json").read_text())

EPISODES = {
    # key: (package path, captions path, playlists, next-episode key)
    "cruise": (PROD / "YOUTUBE-PACKAGE.md", PROD / "captions.srt", ["Survival", "What If"], "elevator"),
    "elevator": (PROD / "elevator" / "YOUTUBE-PACKAGE.md", PROD / "elevator" / "captions.srt", ["Survival", "What If"], "freezer"),
    "freezer": (PROD / "freezer" / "YOUTUBE-PACKAGE.md", PROD / "freezer" / "captions.srt", ["Survival", "What If"], None),
}


def fenced_after(text, heading):
    """First fenced block after a '## N. Heading' line."""
    m = re.search(r"^## \d+\. " + re.escape(heading) + r".*?\n```\n(.*?)\n```", text, re.S | re.M)
    if not m:
        raise SystemExit(f"no fenced block after '{heading}'")
    return m.group(1).strip()


def title_of(text):
    # 'Primary: **Title**' (freezer, elevator) or 'Primary (62 characters):' + blockquote (cruise)
    m = re.search(r"^Primary:\s*\*\*(.+?)\*\*", text, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^Primary.*?\n\n> (.+)$", text, re.M)
    if not m:
        raise SystemExit("no primary title found")
    return m.group(1).strip()


def pinned_of(text):
    m = re.search(r"^## \d+\. Pinned comment\s*\n+```\n(.*?)\n```", text, re.S | re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^- Pinned comment: \"(.+?)\"\s*$", text, re.M)
    return m.group(1) if m else ""


out = {}
for key, (pkg, srt, playlists, nxt) in EPISODES.items():
    text = pkg.read_text()
    ep = MANIFEST["episodes"][key]
    thumb_a = next(t for t in ep["thumbnails"] if t["kind"].startswith("A_"))
    out[key] = {
        "title": title_of(text),
        "description": fenced_after(text, "Description"),
        "tags": [t.strip() for t in fenced_after(text, "Tags").split(",") if t.strip()],
        "pinned_comment": pinned_of(text),
        "video_url": ep["final"]["url"],
        "thumbnail_url": thumb_a["url"],
        "captions": str(srt.relative_to(ROOT)),
        "playlists": playlists,
        "next": nxt,
        "category_id": "27",           # Education
        "language": "en",
        "made_for_kids": False,
        "synthetic_media": True,
        "privacy": "private",          # flip to public/scheduled in Studio (API-project audit)
    }

dest = Path(__file__).with_name("episodes.json")
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
for k, v in out.items():
    print(f"{k:9} {v['title']!r:70} tags={len(v['tags'])} desc={len(v['description'])} chars")
print("wrote", dest.relative_to(ROOT))
