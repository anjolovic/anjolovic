# Production Plan — "What If You Fell Off a Cruise Ship?" (5-minute cut)

Status: **prepared, not generated.** No credits were spent. This folder holds everything
needed to start the run later.

## Locked brief

| Parameter | Value |
|---|---|
| Length | 5:00 = 30 blocks × 10 s |
| Aspect / resolution | 16:9, 1080p |
| Video model | Seedance 2.0, standard mode (1080p requires `mode: std`) |
| Look | cinematic, realistic (not cartoon) |
| Narrator | Arthur — `voice_id 30fc8796-ceb6-4a66-b3a7-4a145ef7f346`, `voice_type preset`, engine `text2speech_v2` / `elevenlabs` |
| Captions | off (matches the reference channel) |
| Music bed | instrumental, 300 s, ducked under narration |
| Script | `script_manifest.json` (30 blocks, 20–23 words each, numbers as words, one line per block) |

## Cost sheet (credits, measured with cost preflight on 2026-09-06)

| Item | Unit cost | Qty for 5 min | Subtotal |
|---|---|---|---|
| Seedance 2.0, 1080p std, 10 s clip | 90 | 30 | 2,700 |
| Seedance 2.0, 1080p std, 15 s clip | 135 | (20) | (2,700) |
| Seedance 2.0, 720p fast, 10 s clip | 35 | 30 | 1,050 |
| Seedance 2.5, 1080p, 10 s / 30 s clip | 90 / 270 | 30 / 10 | 2,700 |
| Reference still (character, location, prop), 1k | 1.5 | ~20 | 30 |
| Narration take, per block | 0.6 | 30 + retries | ~25 |
| Music bed, 300 s | 18.75 | 1 | 19 |
| **Total, 1080p as specified** | | | **~2,800 + ~10% retry margin ≈ 3,100** |

Balance at time of prep: 1,272. Shortfall for the specified cut: ~1,800–2,000 credits.

Cheaper paths priced: 2 min at 1080p (~1,160 total) or 5 min at 720p fast (~1,130 total),
both leaving almost no retry margin.

## Pipeline (when funded)

1. **Reference stills.** One photoreal passenger reference (full body, plain backdrop, adult,
   striped holiday shirt), 11 location plates (see `locations` in the manifest), 4 props
   (lifebuoy ring, thermometer, binoculars, whistle), a crew member, a shark. Every clip
   references location → characters → props so identity and palette hold across 30 clips.
2. **Clips.** 30 Seedance 2.0 requests, `duration 10`, `resolution 1080p`, `mode std`,
   `aspect_ratio 16:9`, image references attached, prompt = five hard-cut ~2 s shots per
   block from `blocks[].shots`, rewritten in live-action language (real camera moves,
   natural light, diegetic sound only, no on-screen text, nobody speaks on camera).
   Submit in batches of 12, wait each batch to terminal, retry only failed indices.
3. **Narration.** One take per block with Arthur, prompt format
   `[measured documentary narrator, dry British warmth, starts speaking immediately] [00:00-00:09] {line}`.
   Gate every take at 7.8–9.5 s of detected speech, no internal pause ≥ 0.8 s, under
   2.9 words/s. Fix misses by rewriting words, never by time-stretching.
4. **Assembly.** Each voice line centered in its 10 s block, clips concatenated to exactly
   300 s, diegetic clip audio ~18 dB under voice, music bed ducked by the voice, loudness
   normalized to −16 LUFS. Output one `final.mp4`.
5. **Thumbnail.** Realistic 16:9 cover: figure mid-fall beside a white hull, one line of
   text, `COULD YOU SURVIVE?`.

## Script notes

The 30 lines follow the reference channel's beat sheet: cold open under eight words,
promise, escalation, mini-cliffs at blocks 9 and 20 (mid-roll positions), the turn at
block 29 (railings are over a meter tall by law; people climb them), payoff at block 30
echoing the hook. The through-line is the orange lifebuoy ring: on the rail, thrown, reached,
held up as a beacon, back on its bracket.

Verify before recording (see `../brightside-video-script.md` Part 4): overboard counts and
survival rate, deck height, stopping distance, Williamson-turn timing, overboard-sensor
adoption, swim-vs-float heat loss, water-temperature survival windows.
