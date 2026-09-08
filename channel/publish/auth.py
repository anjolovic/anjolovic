#!/usr/bin/env python3
"""One-time YouTube authorisation for the Then What? channel. Run this on YOUR
machine, not in the cloud environment. Standard library only.

    python3 channel/publish/auth.py ~/Downloads/client_secret_*.json

It opens a browser. Sign in and, on the account picker, choose the channel
"Then What?" (the Brand Account), not your personal account. It then writes

    ~/.config/thenwhat/youtube-token.json   (mode 0600)

and prints the three values to add to the Claude Code environment as secret
variables: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN. Never paste them
into a chat. The refresh token does not expire while the client is in use;
if Google's consent screen is left in "Testing" mode it expires after 7 days,
so set the app's publishing status to "In production" in Google Auth Platform.
"""
import http.server
import json
import os
import secrets
import stat
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN = "https://oauth2.googleapis.com/token"
OUT = Path.home() / ".config" / "thenwhat" / "youtube-token.json"


def main(client_json):
    data = json.loads(Path(client_json).read_text())
    c = data.get("installed") or data.get("web") or data
    client_id, client_secret = c["client_id"], c["client_secret"]

    state = secrets.token_urlsafe(16)
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            ok = q.get("state", [""])[0] == state and "code" in q
            result["code"] = q.get("code", [None])[0] if ok else None
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(("<h2>Then What? authorised. You can close this tab.</h2>" if ok
                              else "<h2>Authorisation failed. Check the terminal.</h2>").encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    port = srv.server_address[1]
    redirect = f"http://127.0.0.1:{port}/"
    threading.Thread(target=srv.handle_request, daemon=True).start()

    url = AUTH + "?" + urllib.parse.urlencode({
        "client_id": client_id, "redirect_uri": redirect, "response_type": "code",
        "scope": " ".join(SCOPES), "access_type": "offline", "prompt": "consent",
        "include_granted_scopes": "true", "state": state,
    })
    print("Opening browser. Pick the 'Then What?' channel on the account picker.\n")
    if not webbrowser.open(url):
        print("Open this URL manually:\n" + url)
    while "code" not in result:
        threading.Event().wait(0.2)
    if not result["code"]:
        sys.exit("No authorisation code received.")

    body = urllib.parse.urlencode({
        "code": result["code"], "client_id": client_id, "client_secret": client_secret,
        "redirect_uri": redirect, "grant_type": "authorization_code",
    }).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN, data=body)) as r:
        tok = json.load(r)
    if "refresh_token" not in tok:
        sys.exit("Google returned no refresh token. Revoke the app at myaccount.google.com/permissions and run again.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "client_id": client_id, "client_secret": client_secret,
        "refresh_token": tok["refresh_token"], "scopes": SCOPES,
    }, indent=2))
    os.chmod(OUT, stat.S_IRUSR | stat.S_IWUSR)

    # Confirm which channel the token belongs to.
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        headers={"Authorization": "Bearer " + tok["access_token"]})
    with urllib.request.urlopen(req) as r:
        ch = json.load(r)["items"][0]
    print(f"Authorised as: {ch['snippet']['title']}  ({ch['id']})")
    if ch["id"] != "UC3on7iZXg0n1oRYBvk7wpOA":
        print("WARNING: that is not the Then What? channel. Run again and pick the Brand Account.")
    print(f"\nToken written to {OUT}\n")
    print("Add these three as SECRET environment variables on the Claude Code environment")
    print("(Settings -> Environments -> your environment -> Environment variables):")
    print("  YT_CLIENT_ID      = client_id from the file")
    print("  YT_CLIENT_SECRET  = client_secret from the file")
    print("  YT_REFRESH_TOKEN  = refresh_token from the file")
    print("Do not paste the values into chat.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
