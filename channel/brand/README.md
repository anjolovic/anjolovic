# Then What? brand assets ("The Drop")

One mark, two colours, one rule: the dot is the only thing that is ever yellow.

The mark is a machined question mark whose oversized dot has fallen through the
baseline. In the wordmark every letter sits on the line and the dot drops below
it. "That's what." is the sound of it landing.

## Rebuild

```
python3 channel/brand/build.py            # everything into channel/brand/out/
python3 channel/brand/build.py banner     # one asset: avatar, watermark, banner, badge,
                                          # playlists, endscreen, shorts, wordmark
```

Needs Chromium (`$CHROMIUM`, default `/opt/pw-browsers/chromium`), Pillow, and the two
Archivo font files in `fonts/` (OFL, from Google Fonts). Type is set live in Archivo, so
never edit the PNGs by hand; change `build.py` and rebuild.

## Files and where they go

| File | Size | Where in YouTube Studio |
|---|---|---|
| `out/avatar-800.png` | 800×800 | Customization → Profile → Picture |
| `out/banner-2560x1440.png` | 2560×1440 | Customization → Profile → Banner image (use this one; `banner-2048x1152.png` is the minimum-size fallback) |
| `out/watermark-150.png` | 150×150 transparent | Settings → Channel → Branding → Video watermark, display "Entire video" |
| `out/thumbnail-badge-1280x720.png` | 1280×720 transparent | Composite over every thumbnail as the top layer. Mark top-left, 79 px tall, 32 px inset |
| `out/playlist-*-1280x720.png` | 1280×720 | Playlist thumbnails for What If, Survival, Mysteries, Your Body, Space, Tests |
| `out/end-screen-1920x1080.png` | 1920×1080 | Ground plate for the final 20 s of every episode; add video, subscribe and playlist elements in Studio |
| `out/shorts-stamp-1080x1920.png` | 1080×1920 transparent | Top layer on every Shorts cut |
| `out/wordmark-horizontal-*.png` | trimmed | Press, community posts, social headers |
| `mark.svg`, `mark-mono.svg`, `mark-on-bone.svg` | vector | Anything else |
| `tokens.json` | | Palette, type, geometry, rules |

## Palette

| Role | Hex | Use |
|---|---|---|
| Deep | `#0E1A24` | Ground: avatar, banner, end screen, diagram stage |
| Bone | `#F5F1E8` | Ink: bowl and stem, all wordmark type, watermark, badge |
| Signal | `#FFC300` | The dot. Nothing else. Same family as the thumbnail title yellow |
| Fog | `#7C8894` | Straplines, rules, playlist words, secondary UI |

## Type

Wordmark: Archivo 700, all caps, tracking +45/1000, the `?` is always the mark, never
typed. Support: Archivo 500, all caps, tracking +140/1000. Thumbnail titles stay in
Anton or Bebas Neue with the black stroke; that voice is for thumbnails only.

## Rules

1. The wordmark never appears on a thumbnail. The badge does, top-left, single colour.
2. The watermark and badge are Bone only. Yellow vanishes over bright footage and
   collides with burned-in yellow text.
3. Do not pre-round the avatar. YouTube applies the circle.
4. Clear space around the mark is one stroke width; two on the banner.
5. Below 180 px of width use the mark alone, never a shrunken wordmark.
6. No rounded caps, no gradients, no glow. Flat cuts and one shadow at most.

## Ident (3 s, end screen only)

The bowl and stem are already there. The dot falls in from above, lands 0.26 cap
heights below the baseline with one dull impact (a hardback dropped flat on a desk),
recoils two frames, then turns from Bone to Signal over six frames. Hold. Hard cut to
black. On the end screen, the landing syncs to the word "what" in "That's what."
Episodes have no intro card; Shorts run the full three seconds at the head.

Per pillar the fall changes, nothing else: What If falls upward and never lands;
Survival lands hard with one bounce (default); Mysteries has the dot already there
and the bowl draws down to it; Your Body pulses twice at about 60 bpm; Space falls at
four times the duration in silence; Tests hovers one second, then lands.

## The found mark

Once per episode, in the footage, the mark exists physically for about one second:
frost wiped off a freezer door in the shape of the bowl with the release knob as the
dot; a lifebuoy line coiled on deck with the ring below it; a cockpit door's cable
curl above the lock light. Never labelled, never pointed at. Regular viewers find it.
