# Then What — Channel Brand Record

Status: **name locked 2026-09-07.** Handle not yet claimed (see §2). No channel art generated yet.

This is the single source of truth for how the channel is named, sounds, looks, and packages
its videos. Every script, thumbnail, and upload package inherits from here. When something
changes, change it here first.

---

## 1. Name and positioning

| Field | Value |
|---|---|
| Channel name | **Then What** |
| Wordmark | `THEN WHAT?` |
| Positioning line | You're in the scenario. We tell you, minute by minute, what happens next and what to do about it. |
| One-line About | Something goes wrong. Then what? Cinematic, second-person explainers on what actually happens next: survival, science, your body, space, and the mysteries nobody has quite solved. |
| Audience | 18–44, global English-speaking, watches on phone with sound on, arrives from Browse and Suggested, not Search |
| Category | Education |
| Reference channel | Bright Side (structure only; see `../brightside-video-script.md` Part 1). Not the tone. |

**Why the name.** Every video is a premise followed by the viewer's own question. It works
for every pillar without a genre word: *You Fell Off a Cruise Ship. Then What?* /
*The Moon Vanishes. Then What?* / *You Stop Sleeping for a Week. Then What?* /
*The Titanic Sinks. Then What Really Happened?* Two syllables, sounds like a person, and is
not a science-brand cliché. Names rejected for boxing the channel into survival: Minute One,
Rule One, Close Call, Worst Case. Names rejected for collisions: Split Second, Brink,
Fair Warning, Hindsight, Still Floating.

## 2. Handle

Bare `@thenwhat` is taken. YouTube handles allow letters, numbers, periods, underscores and
hyphens, so the fallbacks use punctuation, never a trailing number (a `00` suffix reads as
a spam account). Claim in this order, first one that is free wins:

1. `@then.what`
2. `@then_what`
3. `@thenwhat.tv`
4. `@thenwhatshow`
5. `@then-what`

Display name in the channel settings: **Then What?** with the question mark, matching the
wordmark. The handle carries no punctuation beyond the separator.

Record the claimed handle here once done: `@________` (claimed ____-__-__).

Also claim the matching name on TikTok and Instagram the same day, even if unused; Shorts
cuts will be cross-posted later.

## 3. Voice

- **Second person, present tense.** The viewer is the protagonist within one sentence. Never "a person," always "you."
- **Dry warmth, not goofy.** Narrator is Arthur (preset voice, id `30fc8796-ceb6-4a66-b3a7-4a145ef7f346`, ElevenLabs engine), read as a measured documentary narrator with dry British warmth. One wry line per act, never a pun-per-minute.
- **Numbers become objects.** Forty meters is a thirteen-story building. Twenty knots is ten meters every second. Every abstract figure gets a physical anchor.
- **Short sentences. One clause. Then another.** Grade-6 reading level. Jargon gets a plain-English gloss in the same breath.
- **Sourced or softened.** Every statistic has a line in the episode fact-check table or it is rounded to a shape ("a couple dozen a year"). The reference channel's reputation for invented numbers is the thing we do not copy.
- **Kid-safe by construction.** Danger is real, never graphic. No gore, no profanity. Keeps the channel globally monetizable.

## 4. Fixed lines

Say these identically in every episode. They become the brand within twenty uploads.

| Slot | Line |
|---|---|
| Promise (end of cold open) | "By the end of this video, you'll know exactly what happens, and exactly what to do." |
| Mini-cliff 1 | "But that's not the worst part." |
| Mini-cliff 2 | "And this is where most people get it wrong." |
| Recap lead-in | "Let's run it back." |
| Bonus lead-in | "Oh, and one more thing, since you stayed to the end." |
| **Sign-off** | **"That's what. See you in the next one."** |

The sign-off answers the channel name. It follows the next-video pointer, so the last words
the viewer hears are the brand.

Exception: the delivered 2:00 cut of episode 1 was rendered before the name was chosen and
ends on "one mistake" with no spoken sign-off. It carries the line in the pinned comment
only. The 5:00 cut and every episode after it speak the line.

## 5. Title grammar

Primary pattern, used on at least two of every three uploads:

```
[Premise, second person, past or present tense]. Then What?
```

Examples: *You Fell Off a Cruise Ship. Then What?* · *Your Elevator Cable Snaps. Then What?* ·
*The Moon Vanishes. Then What?*

Rules:

- 6–10 words, under 65 characters so it never truncates on mobile.
- Strongest word first. Never start with "The" if it can be avoided.
- No numbers over 20 in list-style titles.
- The pattern is a default, not a cage. Keep one or two "What If…" or "Why…" titles in every
  batch for the title test, and let the data pick.

## 6. Thumbnail and wordmark

Consistent with thumbnails A/B/C in `../production/YOUTUBE-PACKAGE.md`.

- **Look:** photoreal, cinematic, one oversized subject, one moment of tension. Not cartoon.
- **Colours:** at most three. Base palette from thumbnail A: white hull, cobalt water, yellow text with black stroke.
- **Text:** 2–4 words max, heavy geometric sans (Bebas Neue / Anton weight), black stroke. Bottom-left by default, never over the subject's face.
- **Wordmark:** `THEN WHAT?` in the same face. The question mark is set in the accent colour (yellow on dark, cobalt on light) and is the standalone mark at avatar size. Watermark appears at bottom-right of the video, never in the thumbnail.
- **Accent devices:** one red arrow or circle, only when it points at the thing the title is about.
- **Test:** upload one thumbnail, enable Test & compare with two alternates, retire the losers after the test window.

## 7. Channel art (not yet generated)

When commissioned:

- **Avatar:** the yellow `?` mark on cobalt, 800×800, readable at 36 px.
- **Banner:** 2560×1440, safe area 1546×423 centred. Left: wordmark. Right: one photoreal still from the latest episode. Nothing else.
- **Shorts wordmark:** 9:16 safe, top-centre, same mark.

Generate with Higgsfield `generate_image` in the palette above. A few credits; do not spend without a go-ahead.

## 8. Channel settings (copy-ready)

**Description (About):**

```
Something goes wrong. Then what?

Cinematic, second-person explainers on what actually happens next: what your body does in the first sixty seconds, why the ship can't just stop, what the search teams are doing while you float. Survival, science, your body, space, and the mysteries nobody has quite solved.

Every number is sourced or rounded. Danger is real, never graphic. Footage is AI-generated to illustrate the scenario; no real incident is depicted.

New episodes weekly. That's what.
```

**Channel keywords:**

```
then what, what if, what happens if, survival, how to survive, science explained, your body, space, mysteries, minute by minute
```

**Defaults for every upload** (mirrors `../production/YOUTUBE-PACKAGE.md` §10):

- Altered or synthetic content: **yes** (realistic AI-generated people).
- Audience: not made for kids. Age restriction: no.
- Category: Education. Language: English.
- Comments: on, hold potentially inappropriate for review.
- License: Standard YouTube.
- Description footer, always present: general-information disclaimer, sources list, AI-footage disclosure, three hashtags.

## 9. Playlist architecture

One playlist per pillar so the channel reads as broad from the first week, even while most
uploads are survival what-ifs.

| Playlist | Pillar | Title grammar |
|---|---|---|
| What If | Hypotheticals | *[Impossible premise]. Then What?* |
| Survival | What to do if | *You [get into trouble]. Then What?* |
| Mysteries | History and unexplained | *[Event]. Then What Really Happened?* |
| Your Body | Body and psychology | *You [stop/start doing X]. Then What?* |
| Space | Space and science scale | *[Cosmic premise]. Then What?* |
| Tests | Riddles and challenges | *Only 1 in [N] Get This. Then What?* |

Every upload goes into exactly one pillar playlist. Cards point within the pillar; end screens
point across pillars.

## 10. Episode backlog

Retitled from `../brightside-video-script.md` Part 6, plus one seed per non-survival pillar
to prove the name stretches.

| # | Title | Pillar | Status |
|---|---|---|---|
| 1 | You Fell Off a Cruise Ship. Then What? | Survival | 2:00 cut delivered; 5:00 cut prepared |
| 2 | You're Locked in a Walk-In Freezer. Then What? | Survival | 2:00 cut delivered (`production/freezer/`) |
| 3 | Your Elevator Cable Snaps. Then What? | Survival | 2:00 cut delivered (`production/elevator/`) |
| 4 | The Dive Boat Left Without You. Then What? | Survival | hook written |
| 5 | The Volcano Erupts While You're on It. Then What? | Survival | hook written |
| 6 | You're Lost in a Cave With One Flashlight. Then What? | Survival | hook written |
| 7 | The Pilot Passes Out at 35,000 Feet. Then What? | Survival | long-form script written (`production/pilot/SCRIPT.md`); promised in the episode 1 outro |
| 8 | You Stop Sleeping for a Week. Then What? | Your Body | seed |
| 9 | The Moon Vanishes Tonight. Then What? | Space | seed |
| 10 | The Titanic Sinks. Then What Really Happened? | Mysteries | seed; fact-check heavy |
| 11 | Only 1 in 10 Escape This Room. Then What? | Tests | seed |

Episode 7 ships next as a long-form episode: it is already promised in the episode 1 outro and end screen.

## 11. Launch order

1. Claim the handle (§2) and set the About, keywords, and defaults (§8).
2. Create the six playlists (§9), empty is fine.
3. Upload episode 1 with the package in `../production/YOUTUBE-PACKAGE.md`, into the Survival playlist.
4. Schedule the two Shorts cuts one and two days later.
5. Commission channel art (§7) once the first thumbnail test has a winner, so the banner still matches.
