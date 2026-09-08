#!/usr/bin/env python3
"""Publish the Then What? channel from the repo.

    python3 channel/publish/publish.py setup            # branding, watermark, playlists, sections
    python3 channel/publish/publish.py upload cruise    # one episode (or: all)
    python3 channel/publish/publish.py status           # what the channel currently holds
    add --dry-run to any command to print the calls without making them

Credentials: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN in the environment
(or YT_TOKEN_FILE). Copy comes from channel.json and episodes.json next to this
file; regenerate episodes.json with build_episodes.py after editing a package.

Things the Data API does not expose and that stay manual in Studio: profile
picture, playlist cover images, end screens, cards, pinning a comment, community
posts, Test & compare thumbnails, and flipping API-uploaded videos to public
until the Cloud project passes Google's compliance audit.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yt import YouTube, download  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BRAND = ROOT / "channel" / "brand" / "out"
CHANNEL = json.loads((HERE / "channel.json").read_text())
EPISODES = json.loads((HERE / "episodes.json").read_text())
STATE = HERE / "state.json"          # ids we created, so re-runs are idempotent
CACHE = Path(tempfile.gettempdir()) / "thenwhat-media"


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {"playlists": {}, "videos": {}}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=2) + "\n")


# ---------------------------------------------------------------- setup
def ensure_playlists(yt, state):
    existing = {p["snippet"]["title"]: p["id"] for p in yt.get_all("playlists", {"part": "snippet", "mine": "true"})} if not yt.dry_run else {}
    for pl in CHANNEL["playlists"]:
        if pl["title"] in existing:
            state["playlists"][pl["title"]] = existing[pl["title"]]
            print(f"  playlist exists: {pl['title']}")
            continue
        r = yt.call("POST", "playlists", {"part": "snippet,status"}, {
            "snippet": {"title": pl["title"], "description": pl["description"], "defaultLanguage": "en"},
            "status": {"privacyStatus": "public"},
        })
        state["playlists"][pl["title"]] = r["id"]
        print(f"  playlist created: {pl['title']} ({r['id']})")
    save_state(state)


def set_branding(yt):
    ch = yt.call("GET", "channels", {"part": "brandingSettings", "mine": "true"})
    item = ch["items"][0] if not yt.dry_run else {"id": CHANNEL["channel_id"], "brandingSettings": {}}
    bs = item.get("brandingSettings", {})
    bs.setdefault("channel", {}).update({
        "description": CHANNEL["description"],
        "keywords": CHANNEL["keywords"],
        "defaultLanguage": "en",
        "country": CHANNEL.get("country") or bs.get("channel", {}).get("country"),
    })
    if CHANNEL.get("trailer_video_id"):
        bs["channel"]["unsubscribedTrailer"] = CHANNEL["trailer_video_id"]
    # banner: upload, then reference the returned URL in brandingSettings.image
    b = yt.simple_upload("channelBanners/insert", {}, BRAND / "banner-2560x1440.png", "image/png")
    if b.get("url"):
        bs["image"] = {"bannerExternalUrl": b["url"]}
    yt.call("PUT", "channels", {"part": "brandingSettings"}, {"id": item["id"], "brandingSettings": bs})
    print("  branding set: description, keywords, language, country, banner" + (", trailer" if CHANNEL.get("trailer_video_id") else ""))


def set_watermark(yt):
    meta = {"timing": {"type": "offsetFromStart", "offsetMs": 0}, "position": {"type": "corner", "cornerPosition": "bottomRight"}}
    yt.multipart_upload("watermarks/set", {"channelId": CHANNEL["channel_id"]}, meta, BRAND / "watermark-150.png", "image/png")
    print("  watermark set: entire video, bottom-right")


def set_sections(yt, state):
    if not yt.dry_run:
        for s in yt.get_all("channelSections", {"part": "id", "mine": "true"}):
            yt.call("DELETE", "channelSections", {"id": s["id"]})
    for i, sec in enumerate(CHANNEL["sections"]):
        body = {"snippet": {"type": sec["type"], "position": i}}
        if sec["type"] == "singlePlaylist":
            pid = state["playlists"].get(sec["playlist"])
            if not pid:
                print(f"  skip section {sec['playlist']}: playlist not created yet")
                continue
            body["contentDetails"] = {"playlists": [pid]}
        yt.call("POST", "channelSections", {"part": "snippet,contentDetails"}, body)
        print(f"  section {i}: {sec['type']} {sec.get('playlist', '')}")


def setup(yt):
    state = load_state()
    print("Playlists"); ensure_playlists(yt, state)
    print("Branding"); set_branding(yt)
    print("Watermark"); set_watermark(yt)
    print("Sections"); set_sections(yt, state)


# ---------------------------------------------------------------- upload
def composite_thumbnail(src_jpg, dest_png):
    from PIL import Image
    base = Image.open(src_jpg).convert("RGBA").resize((1280, 720))
    badge = Image.open(BRAND / "thumbnail-badge-1280x720.png").convert("RGBA")
    Image.alpha_composite(base, badge).convert("RGB").save(dest_png, "JPEG", quality=92)
    return dest_png


def upload_episode(yt, key):
    ep = EPISODES[key]
    state = load_state()
    if key in state["videos"]:
        print(f"{key}: already uploaded as {state['videos'][key]}; skipping video, refreshing metadata only")
        vid = state["videos"][key]
    else:
        CACHE.mkdir(parents=True, exist_ok=True)
        video = download(ep["video_url"], CACHE / f"{key}.mp4") if not yt.dry_run else CACHE / f"{key}.mp4"
        meta = {
            "snippet": {
                "title": ep["title"], "description": ep["description"], "tags": ep["tags"],
                "categoryId": ep["category_id"], "defaultLanguage": ep["language"], "defaultAudioLanguage": ep["language"],
            },
            "status": {
                "privacyStatus": ep["privacy"], "selfDeclaredMadeForKids": ep["made_for_kids"],
                "containsSyntheticMedia": ep["synthetic_media"], "license": "youtube", "embeddable": True,
            },
        }
        r = yt.resumable_video_upload(meta, video)
        vid = r["id"]
        state["videos"][key] = vid
        save_state(state)
        print(f"{key}: uploaded as {vid} (private)")

    # thumbnail A with the badge composited on
    if not yt.dry_run:
        src = download(ep["thumbnail_url"], CACHE / f"{key}-thumb.jpg")
        thumb = composite_thumbnail(src, CACHE / f"{key}-thumb-badged.jpg")
    else:
        thumb = CACHE / f"{key}-thumb-badged.jpg"
    yt.simple_upload("thumbnails/set", {"videoId": vid}, thumb, "image/jpeg")
    print("  thumbnail set (A + badge)")

    # captions
    yt.multipart_upload("captions", {"part": "snippet"},
                        {"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}},
                        ROOT / ep["captions"], "application/octet-stream")
    print("  captions uploaded")

    # playlists
    for title in ep["playlists"]:
        pid = state["playlists"].get(title)
        if not pid:
            print(f"  playlist {title} missing; run setup first")
            continue
        yt.call("POST", "playlistItems", {"part": "snippet"}, {
            "snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        print(f"  added to {title}")

    # the pinned-comment text, posted as the channel (pin it in Studio)
    if ep.get("pinned_comment"):
        yt.call("POST", "commentThreads", {"part": "snippet"}, {"snippet": {
            "videoId": vid, "topLevelComment": {"snippet": {"textOriginal": ep["pinned_comment"]}}}})
        print("  comment posted (pin it in Studio)")


def status(yt):
    ch = yt.call("GET", "channels", {"part": "snippet,statistics,brandingSettings", "mine": "true"})["items"][0]
    print(ch["snippet"]["title"], ch["id"], ch["statistics"])
    for v in yt.get_all("search", {"part": "snippet", "forMine": "true", "type": "video"}):
        print(" ", v["id"]["videoId"], v["snippet"]["title"])
    for p in yt.get_all("playlists", {"part": "snippet,contentDetails", "mine": "true"}):
        print("  playlist", p["snippet"]["title"], p["contentDetails"]["itemCount"])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit(__doc__)
    yt = YouTube(dry_run=dry)
    cmd = args[0]
    if cmd == "setup":
        setup(yt)
    elif cmd == "upload":
        keys = list(EPISODES) if args[1:] == ["all"] else args[1:]
        for k in keys:
            upload_episode(yt, k)
    elif cmd == "status":
        status(yt)
    else:
        sys.exit(__doc__)
