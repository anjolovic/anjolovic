# Handoff: the Then What? YouTube channel

Written 2026-09-08 for the agent taking over. The new agent runs **on the owner's Mac with
access to local files**, which simplifies the credential and media steps; see §9. Everything
below is in this repository unless it says otherwise. Read this file first, then
`CHANNEL-BRAND.md`, then `CHANNEL-SETUP.md` and `ENGAGEMENT-KIT.md`.

Part A is the full history of the project, in order, with the reasoning behind each decision.
Part B is the current state: files, media, identity, publishing, and what remains.

---

# Part A. History, from the idea to now

## A1. The idea and the Bright Side evaluation

The owner's starting point: make YouTube videos with Higgsfield (AI video, images, and voice)
in the style of **Bright Side**, the faceless explainer channel. The first session produced
`brightside-video-script.md`, which has two halves: a teardown of the channel, and a full
script for a first episode in its style.

**What the teardown found** (Part 1 of that file, worth reading in full):

- Bright Side is a volume play by TheSoul Publishing: ~44.7M subscribers, ~11.5B views, writers
  draft, a professional narrator reads, editors assemble stock footage and 2D graphics. Flagship
  videos sit in the 8–15 minute band for mid-roll ads.
- Every video belongs to one of **seven scenario families**: What-If hypotheticals, Survival /
  "what to do if", Riddles and tests, Mysteries and history, Space and science explainers, Body
  and psychology, Life hacks. Each has its own title grammar and retention mechanic. The biggest
  hits combine two, typically What-If plus Survival, which is the DNA of their most-viewed video
  (*13 Tips on How to Survive Wild Animal Attacks*).
- **Hook anatomy**: no intro card, the narrator starts before the thumb leaves the screen. Six
  openers (second-person cold open, the impossible number, the ticking clock, the everyday twist,
  the authority gap, the reversal), each ending in an explicit promise line.
- **The reusable beat sheet**: hook 0:00, setup, Act 1 (the first 60 seconds of the scenario),
  mini-cliff at ~3:15, Act 2 (the first hour), mini-cliff at ~6:20, Act 3 (the long game),
  recap at 9:00, bonus fact at 10:00, outro. Rules: a new fact or image every 20–40 seconds,
  mini-cliffs at ad positions, escalation not lists, recap before outro, bonus after recap.
- **Voice**: second person, present tense; warm goofy uncle; every number translated into a
  physical object; grade-6 sentences; rhetorical questions as connective tissue; kid-safe.
- **Visual grammar**: stock clips cut every 3–6 s, 2D overlays for diagrams, bold text pops
  with SFX, recurring graphics (timeline bar, countdown clock, tick/cross stamps).
- **Packaging**: one oversized subject, saturated colours, 2–4 words in heavy sans with a
  stroke, a red arrow; titles of 6–10 words starting with the strongest word.
- **What to copy and what to skip**: copy the structure (cold open, promise, escalation, fact
  cadence, cliffs, number-to-object, recap + bonus, text pops). Skip invented statistics and
  "scientists say" without a source. Bright Side's growth predates YouTube's current scrutiny of
  low-quality educational content; a new channel gets punished for what they got away with.

That last point shaped everything after: the channel keeps Bright Side's skeleton and rejects its
tone and its looseness with facts.

## A2. Episode 1: the cruise-ship script and the first produced cut

The first script: *What If You Fell Off a Cruise Ship in the Middle of the Ocean?* (10:30,
~1,750 VO words at ~160 wpm, What-If × Survival). It follows the beat sheet exactly, with the
lifebuoy ring as a through-line object, a temperature fork (Caribbean vs Alaska) as the
personalisation beat, the shark question answered late on purpose, a five-line recap ("Float.
Don't swim."), a bonus fact (a ship rescuing someone from a different ship), and a 15-row
fact-check table with sources (CLIA overboard data, the RNLI Float to Live campaign, the 1-10-1
rule, the Williamson turn, the Cruise Vessel Security and Safety Act). Five follow-up hooks were
written in the same family: walk-in freezer, elevator cable, dive boat, volcano, cave.

Production then happened in `production/`. A **30-block, 5:00 manifest** was prepared
(`script_manifest.json`, `build_manifest.py`, `PRODUCTION-PLAN.md`): 30 blocks × 10 s, each with
a 20–23 word VO line, five hard-cut shots, a location, and the through-line state; Seedance 2.0
at 1080p standard mode priced at ~3,100 credits, which exceeded the balance at the time
(1,272). The cheaper path was taken: a **2:00 cut** (`DELIVERY-2MIN.md`), 12 Seedance clips at
1080p, cinematic live-action realism rather than cartoon, one recurring passenger and one
officer built from eleven photoreal reference plates, narrated by **Arthur** (Higgsfield preset
voice, ElevenLabs engine) prompted as a "measured documentary narrator, dry British warmth",
music bed ducked under voice, loudness normalised to −16 LUFS, no captions burned in. Measured
spend: ~1,125 credits. Known quality notes: Seedance under-delivered the five hard cuts per
clip; two blocks carry loud diegetic audio. Three thumbnails were cut, an upload package written
(`YOUTUBE-PACKAGE.md`: title, description with chapters, tags, cards, end screen, pinned
comment, community post, Shorts cuts, upload settings), and a timed SRT produced.

A separate session later produced **freezer** and **elevator** 2:00 cuts in the same format
(`production/freezer/`, `production/elevator/`), and an `ASSET-MANIFEST.json` listing every
generated asset URL with a `pull_assets.sh` downloader.

## A3. Naming the channel

The owner asked for several names: marketable, short, memorable, with broad appeal beyond
survival. A naming brief was set (1–2 words, works as a title grammar on every episode,
second-person tension, reads well in Arthur's voice as a sign-off, survives all seven pillars)
and a collision check was run by web search, since youtube.com is blocked from the cloud
environment.

Shortlist, ranked: **Then What** (clear), **Odds Are** (clear, stats-led), **Minute One** (urgent
but survival-only), **In Which** (dry British chapter grammar, weak cold-traffic CTR), **Rule
One** (unverified). Dropped for collisions or genre-boxing: Close Call (BBC series), Worst Case
(several channels plus the book franchise), Split Second (two in-genre properties), Brink
(Science Channel), Fair Warning (bands), Hindsight (geopolitics channel), Still Floating, Slim
Chance, Thin Ice.

**Decision: Then What.** Every episode is a premise followed by the viewer's own question, and
the grammar carries every pillar without a genre word: *You Fell Off a Cruise Ship. Then What?*
/ *The Moon Vanishes. Then What?* / *The Titanic Sinks. Then What Really Happened?* The sign-off
answers the name: **"That's what. See you in the next one."** The display name carries the
question mark: **Then What?**

The handle: `@thenwhat` was taken, and YouTube only offered numbered suffixes, which read as spam.
Punctuated fallbacks (`@then.what`, `@then_what`, `@thenwhat.tv`) were tried; the owner landed on
**`@thenwhattvshow`** and created the channel on 2026-09-07 as a Brand Account managed by their
dovecore.com Google account. All of this is recorded in `CHANNEL-BRAND.md` §2.

`CHANNEL-BRAND.md` was written as the single source of truth (PR #1): positioning, voice rules,
fixed lines, title grammar, thumbnail rules, About copy, six pillar playlists, an eleven-episode
backlog retitled in the channel grammar, launch order.

## A4. Episode 2: the pilot script

Episode 1's outro promised "what happens when a pilot passes out at thirty-five thousand feet",
so that became the next long-form script (PR #2): `production/pilot/SCRIPT.md`, *The Pilot
Passes Out at 35,000 Feet. Then What?*, 10:30, 1,832 VO words after trimming. Spine: cold open
from seat 14C and the flight attendant's fast walk; Act 1 is the first officer's incapacitation
drill ("I have control", seat back, harness, mask, cabin call) and the two-person rule at the
cockpit door; mini-cliff into the version pilots fear, both pilots via the air, with Helios 522
as the one named accident, time of useful consciousness 15–30 s at cruise, mask-first, the
emergency descent to 10,000 ft, and the redundancy rules (two pilots, different meals, two on
the flight deck after Germanwings 2015); Act 3 answers "could you land it" honestly: on an
airliner almost certainly not, then the May 2022 Florida Cessna landing where a passenger with
no experience was talked down, with the lesson "don't fly it, talk"; five-line recap; bonus:
the Garmin Autoland King Air that landed itself. 21-row fact-check table with sources. Packaging,
retention notes, five follow-up hooks, production sheet. The cockpit door is the through-line
object.

## A5. The identity: three directions, one chosen

The owner asked for a creative asset suite explored from several angles with outside-the-box
imagination. Three read-only design agents ran in parallel, each with one angle:

- **A. The Drop ("the mark as object")**: a machined question mark whose oversized dot has
  fallen through the baseline; "That's what." is the sound of it landing. Bone `#F5F1E8` mark
  with a Signal `#FFC300` dot on Deep `#0E1A24`. Flat typographic banner, no photo. Badge
  top-left on thumbnails. Ident: the dot falls and lands on the word "what". Per pillar only the
  fall changes (What If falls upward and never lands; Survival lands hard with one bounce;
  Mysteries has the dot already there; Your Body pulses at 60 bpm; Space falls slowly in
  silence; Tests hovers a second). Risk: bare `?` prior art; the dropped dot could read as broken.
- **B. Hard Cut ("the cut between")**: typographic only, THEN [cut] WHAT, a yellow vertical bar
  beside a paper `?` on `#0C0E10`; a black bottom plate on thumbnails with a slot; ident of two
  black frames of silence between two shots. Risk: black avatar reads as "not loaded"; motion-
  native on a channel with no intro.
- **C. Figure 1 ("the safety card")**: the channel as the safety card nobody prints; the `?`'s
  dot is a standing pictogram figure, the "you"; amber avatar, bone card banner folded once,
  six pillar pictograms, a bone corner-cut badge. Risk: council-leaflet drift, parody, and an
  "aviation channel" read after episode 2.

All three independently concluded: the wordmark must not use the thumbnail face (Archivo 700
instead of Anton); the avatar must not be yellow on cobalt (cobalt buzzes against YouTube's
red); the wordmark never goes on a thumbnail. **The owner chose A, The Drop.** C's pictograms
are noted as a reserve for playlist covers.

The suite was then built in code (PR #3): `channel/brand/build.py` draws the mark as SVG (120-unit
box, 15-unit stroke, bowl centred (60,40) r 22.5 from 9 o'clock clockwise 240°, dead-centre
stem to y 82, dot r 10.5 at (60,101)), sets type in real Archivo through headless Chromium, and
renders every YouTube size; headless Chromium enforces a minimum window so small assets render
large and crop with Pillow. The banner's lockup was verified inside the phone-safe strip by
overlay. An in-situ preview page shows the avatar at 98/48/32/24 px, the desktop and phone
banner crops, the watermark over a freezer-white frame, a feed row with the badge, playlist
covers, the end screen, and the Shorts stamp:
https://claude.ai/code/artifact/6755f346-dfdf-40f1-b061-a9712bbfef90. No Higgsfield credits
were spent on art.

## A6. Studio copy and the engagement system

`CHANNEL-SETUP.md` fills every Studio field in Studio's order: banner and picture files, name,
handle, a 657-character description (first line carries it: "Something goes wrong. Then what?"),
links led by the confirm-subscribe URL, contact slot (owner wants a dedicated address, not
personal), Home tab layout with trailer and featured video, a 50-second trailer script cut from
the three existing videos, channel keywords, advanced settings, phone verification for
intermediate features, upload defaults, six playlists with descriptions and covers, watermark,
community defaults, and a launch checklist in order.

`ENGAGEMENT-KIT.md` fixes three CTA lines in three slots with the reasoning: a one-sentence
subscribe ask right after the first payoff (~1:15), a comment question at the beat where the
scenario maps onto the viewer's own life, and a like-and-share line that names the person to
send it to. Plus templates for the description (subscribe link, chapters, recap, question, next
episode, disclaimer, sources, AI disclosure, hashtags), pinned comment, cards, end screen, a
weekly off-video cadence (community post, two Shorts, poll, reply pass), and what to measure.
The three delivered packages were retrofitted (subscribe link, comment question, named next
episode) and both long-form scripts got the three lines at their slots.

## A7. Publishing on the owner's behalf

The owner asked what access would let the agent upload everything. Answer: a YouTube Data API
OAuth credential for the Brand Account. The owner created a Google Cloud project with the API
enabled, a Desktop OAuth client named "ThenWhat" (id begins `349793113569-`), downloaded its
JSON to `~/Downloads`, and also an API key (unused; advised to delete since a prefix appeared in
a screenshot). `channel/publish/` (PR #4, open) is a standard-library tool: `auth.py` (loopback
OAuth, token file, channel confirmation), `yt.py` (refresh, JSON calls, media and resumable
uploads), `publish.py setup | upload | status` with `--dry-run`, `build_episodes.py` generating
`episodes.json` from the packages and manifest, `channel.json`, README. Dry-run tested end to
end. A bug where dry runs persisted placeholder ids was fixed.

---

# Part B. Current state

## B1. Facts

| Fact | Value |
|---|---|
| Channel | **Then What?** · `@thenwhattvshow` · `UC3on7iZXg0n1oRYBvk7wpOA` · Brand Account |
| Live state | Created; default teal "T" avatar; nothing uploaded; no art; About empty |
| Owner | Alex, GitHub `anjolovic`, solo founder; wants direct, opinionated, actionable collaboration |
| Repo | `anjolovic/anjolovic`; default branch `claude/brightside-video-script-8yno3u`; working branch `claude/hinksfield-youtube-channel-names-1ynas0` |
| PRs | #1 name + brand record (merged) · #2 pilot script (merged) · #3 identity + setup + engagement (merged) · #4 publishing tool (merged) · **#5 this handoff (open)** |

## B2. File map

```
brightside-video-script.md          Bright Side teardown + episode 1 long-form script + fact-check table
channel/CHANNEL-BRAND.md            brand record (single source of truth)
channel/CHANNEL-SETUP.md            every Studio field, copy-ready; trailer script; launch checklist
channel/ENGAGEMENT-KIT.md           CTA lines and slots; description/pinned/cards/end-screen templates; cadence
channel/HANDOFF.md                  this file
channel/brand/                      build.py, out/*.png (15 upload-ready files), fonts/, mark*.svg, tokens.json, README.md, preview.py
channel/publish/                    auth.py, yt.py, publish.py, build_episodes.py, channel.json, episodes.json, README.md
production/ASSET-MANIFEST.json      every generated asset URL per episode; production/pull_assets.sh downloads all
production/{YOUTUBE-PACKAGE.md,captions.srt,two-minute-narration.json}   cruise 2:00 package
production/freezer/, production/elevator/                                 same three files each
production/pilot/SCRIPT.md          episode 2 long-form script (not produced)
production/{PRODUCTION-PLAN.md,script_manifest.json,build_manifest.py,DELIVERY-2MIN.md}   cruise pipeline and delivery notes
```

## B3. Episodes

| Episode | Channel-grammar title | State |
|---|---|---|
| Cruise ship | You Fell Off a Cruise Ship. Then What? | 2:00 cut delivered; 10:30 script; 5:00 manifest prepared, never run |
| Walk-in freezer | You're Locked in a Walk-In Freezer. Then What? | 2:00 cut delivered |
| Elevator | Your Elevator Cable Snaps. Then What? | 2:00 cut delivered |
| Pilot | The Pilot Passes Out at 35,000 Feet. Then What? | Long-form script written |
| Backlog | dive boat, volcano, cave, sleep, moon, Titanic, escape room | Titles in `CHANNEL-BRAND.md` §10 |

The upload packages still carry the "What If…" primaries with the channel-grammar title as the
test alternate; the owner has not decided which to upload with.

## B4. Media

All generated media is on Higgsfield's CDN, listed in `production/ASSET-MANIFEST.json` (stills,
12 clips, 12 narration takes, music, final MP4, three thumbnails per episode). Finals:

- cruise: `https://d2ol7oe51mr4n9.cloudfront.net/user_3HIlJupKcTkYDUHP2WsYg8p9vv2/2f7f8b60-7e86-4c58-aebf-280943f2cb19.mp4`
- elevator: `https://d2ol7oe51mr4n9.cloudfront.net/user_3HIlJupKcTkYDUHP2WsYg8p9vv2/a2156adc-85e4-4f48-8b05-74120e3c2739.mp4`
- freezer: `https://d2ol7oe51mr4n9.cloudfront.net/user_3HIlJupKcTkYDUHP2WsYg8p9vv2/561f247f-1182-4de8-a558-fc1ce939323f.mp4`

From the owner's Mac these download directly (`bash production/pull_assets.sh` from the repo
root). From the cloud environment they were blocked by the egress proxy.

Higgsfield settings: video `seedance_2_0`, mode `std`, 1080p, 10 s, 16:9; stills `seedream_v5_pro`
1k; narrator **Arthur**, preset voice id `30fc8796-ceb6-4a66-b3a7-4a145ef7f346`, ElevenLabs
engine, prompt style "measured documentary narrator, dry British warmth". Account: Ultra plan,
**484 credits** at last check. A 2:00 cut ≈ 1,125 credits; a 5:00 cut ≈ 3,100. **Never spend
credits without the owner's explicit go-ahead.**

## B5. Identity rules that must not drift

The Drop. Deep `#0E1A24` ground, Bone `#F5F1E8` ink, Signal `#FFC300` for the dot only, Fog
`#7C8894` secondary. Archivo 700 wordmark, Archivo 500 support; thumbnails keep Anton/Bebas
yellow with black stroke. The wordmark never appears on a thumbnail; the badge (mark, Bone,
top-left, 11% height, 32 px inset) does. Watermark and badge are single-colour Bone. Do not
pre-round the avatar. Regenerate with `python3 channel/brand/build.py`.

## B6. Fixed lines

Promise: "By the end of this video, you'll know exactly what happens, and exactly what to do." ·
Mini-cliff 1: "But that's not the worst part." · Mini-cliff 2: "And this is where most people
get it wrong." · Recap: "Let's run it back." · Bonus: "Oh, and one more thing, since you stayed
to the end." · Subscribe (~1:15): "If you're new here, subscribe. This is what we do: what
happens next, minute by minute." · Comment: "Tell me in the comments: [the episode's one
question]." · Like/share (outro): "If you learned something today, hit like and send this to
[the person who needs it]." · **Sign-off: "That's what. See you in the next one."** · Title
grammar: `[Premise, second person]. Then What?`

## B7. Publishing: what to do next, for a local agent

Because you run on the owner's Mac:

1. Confirm the OAuth consent screen is **In production** (Google Auth Platform → Audience); in
   Testing mode the refresh token expires after 7 days.
2. Run `python3 channel/publish/auth.py ~/Downloads/client_secret_349793113569-*.json`. The
   owner must pick **Then What?** on the account picker. It writes
   `~/.config/thenwhat/youtube-token.json` (0600) and confirms the channel id.
3. Export `YT_TOKEN_FILE=~/.config/thenwhat/youtube-token.json` (or the three `YT_*` variables).
   Keep the JSON and the token file out of the repo and out of any chat.
4. `python3 channel/publish/publish.py setup --dry-run`, then without `--dry-run`: playlists,
   banner, description, keywords, watermark, sections.
5. `python3 channel/publish/publish.py upload all`: each video lands **private** with metadata,
   badged thumbnail A, captions, playlists, and the comment text. Commit the resulting
   `channel/publish/state.json`.
6. Tell the owner to do the Studio-only items: profile picture (`channel/brand/out/avatar-800.png`),
   playlist cover images, pin each comment, end screens and cards, community posts, and flip each
   video to public or scheduled. API uploads from an unaudited Cloud project stay private until
   Google's compliance audit; the owner can request it under YouTube API Services.
7. Delete or restrict the unused API key in Google Cloud.

Also pending: `channel/publish/channel.json` has `country` null and `trailer_video_id` null;
TikTok and Instagram `thenwhattvshow` not yet claimed; contact email slot in `CHANNEL-SETUP.md`.

## B8. Process conventions used so far

Work on the working branch; restart it from the default head after each merge; open PRs as
drafts against the default branch; one commit per logical change; plan before each phase and
confirm direction choices with the owner; ask before anything that spends credits or is hard to
reverse; verify every statistic against the fact-check tables before recording. PRs #1–#4 are
merged; #5 (this file) is open for the owner to merge.
