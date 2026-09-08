# Publishing Then What? from the repo

Standard-library Python against the YouTube Data API v3. No SDK, no service account,
nothing that needs installing beyond Pillow (already used by the brand build).

## One-time, on your machine

1. In Google Cloud the OAuth client of type **Desktop app** exists (name "ThenWhat"). Download its
   JSON. The API key is not used by anything here; delete or restrict it.
2. Google Auth Platform → Audience: set the publishing status to **In production**. In Testing
   mode a refresh token dies after seven days.
3. Run the authorisation, signed in as the Brand Account, picking **Then What?** on the account picker:

   ```
   python3 channel/publish/auth.py ~/Downloads/client_secret_349793113569-*.json
   ```

   It writes `~/.config/thenwhat/youtube-token.json` (mode 0600), confirms which channel it
   authorised, and names the three values to copy.
4. Add those three as **secret environment variables** on the Claude Code environment
   (Settings → Environments → the environment → Environment variables):
   `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`. Never paste them into chat.
5. Network policy on the same environment: allow `d2ol7oe51mr4n9.cloudfront.net` (the finished
   videos and thumbnails). Google's API hosts are already reachable.

## Then, from anywhere with the variables set

```
python3 channel/publish/publish.py setup --dry-run     # see the calls
python3 channel/publish/publish.py setup               # playlists, banner, description, keywords, watermark, sections
python3 channel/publish/publish.py upload cruise       # video, thumbnail A + badge, captions, playlists, comment
python3 channel/publish/publish.py upload all
python3 channel/publish/publish.py status
```

`state.json` records the playlist and video ids created, so re-running is idempotent: an episode
already in `state.json` gets its metadata refreshed, not re-uploaded. Commit `state.json`.

`episodes.json` is generated; edit the upload packages, then `python3 channel/publish/build_episodes.py`.
`channel.json` holds the channel-level copy. Set `country` there, and `trailer_video_id` once the
trailer exists, then re-run `setup`.

## What stays manual in Studio

The Data API has no endpoint for: the profile picture (a Brand Account setting), playlist cover
images, end screens, cards, pinning a comment (the text is posted; click pin), community posts,
Test & compare thumbnails, and the altered-content disclosure beyond the `containsSyntheticMedia`
flag the upload sets. Videos uploaded through a Cloud project that has not passed Google's
API compliance audit are held **private**; flip each to public or scheduled in Studio, or request
the audit under YouTube API Services in the Cloud console.

## Quota

Default quota is 10,000 units per day. A video upload costs 1,600; the whole `setup` plus three
uploads fits inside one day with room to spare.
