#!/usr/bin/env python3
"""Generate the in-situ identity preview page (channel/brand/out/preview.html).
Embeds the built PNGs as data URIs so the page needs no external images."""
import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def uri(name):
    return "data:image/png;base64," + base64.b64encode((OUT / name).read_bytes()).decode()


A = {k: uri(v) for k, v in {
    "avatar": "avatar-800.png", "banner": "banner-2560x1440.png", "wm": "watermark-150.png",
    "badge": "thumbnail-badge-1280x720.png", "end": "end-screen-1920x1080.png",
    "wordmark": "wordmark-horizontal-deep.png", "wordmark_bone": "wordmark-horizontal-bone.png",
    "shorts": "shorts-stamp-1080x1920.png",
    "p_whatif": "playlist-whatif-1280x720.png", "p_survival": "playlist-survival-1280x720.png",
    "p_mysteries": "playlist-mysteries-1280x720.png", "p_body": "playlist-body-1280x720.png",
    "p_space": "playlist-space-1280x720.png", "p_tests": "playlist-tests-1280x720.png",
}.items()}

MARK = (HERE / "mark.svg").read_text().strip()

# Stand-in frames for the three delivered thumbnails (the hosted JPEGs are not
# reachable from this environment). Same titles, same yellow-stroke treatment.
THUMBS = [
    ("COULD YOU SURVIVE?", "linear-gradient(160deg,#dfe7ee 0%,#8fb3c9 28%,#1f4fd1 60%,#0b1d3a 100%)", "You Fell Off a Cruise Ship. Then What?", "2:00"),
    ("LOCKED IN AT -18°C", "linear-gradient(200deg,#f4f7f9 0%,#b9c7d1 40%,#5c6f7d 75%,#1c2730 100%)", "You're Locked in a Walk-In Freezer. Then What?", "2:00"),
    ("DON'T JUMP", "linear-gradient(180deg,#2a2f36 0%,#5a5f66 45%,#15181c 100%)", "Your Elevator Cable Snaps. Then What?", "2:00"),
]

OTHERS = [  # stand-in neighbour avatars for the rails
    ("#e53935", "K"), ("#3949ab", "V"), ("#00897b", "M"), ("#8e24aa", "N"), ("#f4511e", "S"),
]


def thumb(title, grad, w, badge=True, dur=True):
    h = round(w * 9 / 16)
    fs = round(w * 0.072)
    return f'''<div class="thumb" style="width:{w}px;height:{h}px;background:{grad}">
  {f'<img class="badge" src="{A["badge"]}" alt="">' if badge else ''}
  <span class="ttl" style="font-size:{fs}px">{title}</span>
  {f'<span class="dur">2:00</span>' if dur else ''}
</div>'''


def rail(size, dark):
    cells = "".join(
        f'<div class="av" style="width:{size}px;height:{size}px;background:{c}"><span style="font-size:{round(size*0.42)}px">{l}</span></div>'
        for c, l in OTHERS[:3]
    ) + f'<img class="av" style="width:{size}px;height:{size}px" src="{A["avatar"]}" alt="Then What? avatar">' + "".join(
        f'<div class="av" style="width:{size}px;height:{size}px;background:{c}"><span style="font-size:{round(size*0.42)}px">{l}</span></div>'
        for c, l in OTHERS[3:]
    )
    return f'<div class="rail {"yt-dark" if dark else "yt-light"}">{cells}</div>'


html = f'''<title>Then What? Identity</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&family=Anton&family=Roboto:wght@400;500&display=swap">
<style>
:root{{
  --ground:#F5F1E8; --ink:#0E1A24; --signal:#FFC300; --fog:#7C8894;
  --line:rgba(14,26,36,.14); --panel:#ECE7DC; --note:#4E5A64;
  --yt-l-bg:#FFFFFF; --yt-l-ink:#0F0F0F; --yt-l-sub:#606060; --yt-l-chip:#F2F2F2;
  --yt-d-bg:#0F0F0F; --yt-d-ink:#F1F1F1; --yt-d-sub:#AAAAAA; --yt-d-chip:#272727;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{
  --ground:#0E1A24; --ink:#F5F1E8; --line:rgba(245,241,232,.14); --panel:#152431; --note:#A9B3BB; }} }}
:root[data-theme="dark"]{{ --ground:#0E1A24; --ink:#F5F1E8; --line:rgba(245,241,232,.14); --panel:#152431; --note:#A9B3BB; }}

html{{color-scheme:light dark}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:Archivo,"Helvetica Neue",Arial,sans-serif;font-size:15px;line-height:1.5}}
main{{max-width:1120px;margin:0 auto;padding:40px 24px 96px}}
h1,h2{{text-wrap:balance;margin:0}}
h1{{font-weight:700;font-size:clamp(28px,4vw,40px);letter-spacing:-.01em;line-height:1.05}}
h2{{font-weight:700;font-size:20px;letter-spacing:.01em}}
.eyebrow{{font-weight:500;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--fog)}}
p{{max-width:62ch;margin:0}}
.note{{color:var(--note);font-size:14px;max-width:68ch}}
header{{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:end;padding-bottom:24px;border-bottom:1px solid var(--line)}}
header .lock{{display:flex;flex-direction:column;gap:14px}}
.chips{{display:flex;gap:8px}}
.chip{{display:flex;flex-direction:column;gap:4px;font-size:11px;letter-spacing:.06em;color:var(--fog);font-variant-numeric:tabular-nums}}
.chip i{{display:block;width:56px;height:36px;border:1px solid var(--line)}}
section{{padding:40px 0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:220px 1fr;gap:28px;align-items:start}}
section .side{{display:flex;flex-direction:column;gap:10px;position:sticky;top:16px}}
.stage{{overflow-x:auto;display:flex;flex-direction:column;gap:20px}}
.stage>*{{flex:none}}

/* YouTube surfaces */
.yt{{font-family:Roboto,Arial,sans-serif;border:1px solid var(--line);overflow:hidden}}
.yt-light{{background:var(--yt-l-bg);color:var(--yt-l-ink)}}
.yt-dark{{background:var(--yt-d-bg);color:var(--yt-d-ink)}}
.yt .sub{{color:var(--yt-l-sub)}} .yt-dark .sub{{color:var(--yt-d-sub)}}
.desk{{width:1000px}}
.desk .banner{{display:block;width:100%;aspect-ratio:2560/423;object-fit:cover;object-position:center}}
.chead{{display:flex;gap:24px;padding:16px 24px 20px;align-items:center}}
.chead img{{width:160px;height:160px;border-radius:50%}}
.chead .nm{{font-size:36px;font-weight:700;line-height:1.1}}
.chead .meta{{font-size:14px;margin-top:6px}}
.btn{{display:inline-block;margin-top:12px;padding:0 16px;height:36px;line-height:36px;border-radius:18px;font-size:14px;font-weight:500;background:#0F0F0F;color:#fff}}
.yt-dark .btn{{background:#F1F1F1;color:#0F0F0F}}
.phone{{width:390px;border-radius:28px;border:1px solid var(--line);overflow:hidden}}
.phone .banner{{display:block;width:100%;aspect-ratio:1546/423;object-fit:cover;object-position:center}}
.phone .chead{{padding:14px 16px 18px;gap:14px}}
.phone .chead img{{width:72px;height:72px}}
.phone .chead .nm{{font-size:22px}}
.rail{{display:flex;gap:18px;padding:14px 18px;align-items:center;font-family:Roboto,Arial,sans-serif}}
.av{{border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:500;flex:none}}
.rail.yt-light,.rail.yt-dark{{border:1px solid var(--line)}}
.comment{{display:flex;gap:12px;padding:14px 18px;font-family:Roboto,Arial,sans-serif;font-size:13px;width:520px;border:1px solid var(--line)}}
.comment .body{{display:flex;flex-direction:column;gap:2px}}
.comment .who{{font-weight:500;font-size:12px}}
.comment .reply{{display:flex;gap:10px;margin-top:8px;margin-left:0}}
.player{{width:720px;aspect-ratio:16/9;position:relative;overflow:hidden;background:linear-gradient(200deg,#f4f7f9 0%,#b9c7d1 40%,#5c6f7d 75%,#1c2730 100%)}}
.player .wm{{position:absolute;right:14px;bottom:48px;width:44px;height:44px}}
.player .bar{{position:absolute;left:0;right:0;bottom:0;height:40px;background:linear-gradient(transparent,rgba(0,0,0,.55))}}
.player .prog{{position:absolute;left:0;bottom:0;height:3px;width:38%;background:#FF0000}}
.player .prog2{{position:absolute;left:0;bottom:0;height:3px;width:100%;background:rgba(255,255,255,.3)}}
.feed{{display:grid;grid-template-columns:repeat(3,272px);gap:16px;padding:16px;font-family:Roboto,Arial,sans-serif}}
.feed .item{{display:flex;flex-direction:column;gap:10px}}
.feed .row{{display:flex;gap:10px;align-items:flex-start}}
.feed .row img{{width:36px;height:36px;border-radius:50%;flex:none}}
.feed .t{{font-size:14px;font-weight:500;line-height:1.3}}
.feed .m{{font-size:12px;margin-top:2px}}
.thumb{{position:relative;border-radius:12px;overflow:hidden;font-family:Anton,Impact,sans-serif}}
.thumb .badge{{position:absolute;inset:0;width:100%;height:100%}}
.thumb .ttl{{position:absolute;left:4.5%;bottom:5%;color:#FFD100;-webkit-text-stroke:.05em #000;paint-order:stroke fill;letter-spacing:.01em;line-height:1}}
.thumb .dur{{position:absolute;right:6px;bottom:6px;background:rgba(0,0,0,.8);color:#fff;font:500 11px/1 Roboto,Arial,sans-serif;padding:3px 4px;border-radius:4px}}
.plist{{display:grid;grid-template-columns:repeat(6,150px);gap:12px;padding:16px;font-family:Roboto,Arial,sans-serif;font-size:12px}}
.plist img{{width:150px;border-radius:8px;display:block}}
.plist .n{{margin-top:6px;font-weight:500}}
.endwrap{{position:relative;width:720px}}
.endwrap img{{display:block;width:100%}}
.zone{{position:absolute;border:1.5px dashed rgba(245,241,232,.55);color:#F5F1E8;font:500 11px/1 Archivo,sans-serif;letter-spacing:.1em;display:flex;align-items:center;justify-content:center;text-transform:uppercase}}
.rules{{display:grid;grid-template-columns:1fr 1fr;gap:12px 28px;list-style:none;padding:0;margin:0;font-size:14px;max-width:none}}
.rules li{{padding-left:18px;position:relative}}
.rules li::before{{content:"";position:absolute;left:0;top:.62em;width:8px;height:8px;border-radius:50%;background:var(--signal)}}
.marks{{display:flex;gap:28px;align-items:flex-end}}
.marks figure{{margin:0;display:flex;flex-direction:column;gap:8px;align-items:center;font-size:11px;color:var(--fog);font-variant-numeric:tabular-nums}}
.marks .box{{background:#0E1A24;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.shorts{{width:270px;aspect-ratio:9/16;position:relative;overflow:hidden;border-radius:16px;background:linear-gradient(160deg,#dfe7ee 0%,#8fb3c9 28%,#1f4fd1 60%,#0b1d3a 100%)}}
.shorts img{{position:absolute;inset:0;width:100%;height:100%}}
@media (max-width:760px){{section{{grid-template-columns:1fr}} section .side{{position:static}} header{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:no-preference){{a:focus-visible{{outline:2px solid var(--signal)}}}}
</style>

<main>
<header>
  <div class="lock">
    <span class="eyebrow">Channel identity · The Drop · @thenwhattvshow</span>
    <img src="{A["wordmark"]}" alt="THEN WHAT? wordmark" style="width:min(560px,100%);display:block">
    <p class="note">A machined question mark whose oversized dot has fallen through the baseline. Every letter sits on the line; the dot drops below it. The dot is the only thing that is ever yellow.</p>
  </div>
  <div class="chips">
    <div class="chip"><i style="background:#0E1A24"></i>Deep #0E1A24</div>
    <div class="chip"><i style="background:#F5F1E8"></i>Bone #F5F1E8</div>
    <div class="chip"><i style="background:#FFC300"></i>Signal #FFC300</div>
    <div class="chip"><i style="background:#7C8894"></i>Fog #7C8894</div>
  </div>
</header>

<section>
  <div class="side"><span class="eyebrow">Channel page, desktop</span><h2>Banner and avatar as YouTube crops them</h2><p class="note">Desktop shows the full banner width in a 6:1 band. The ghost mark on the right only appears here and on TV.</p></div>
  <div class="stage">
    <div class="yt yt-light desk">
      <img class="banner" src="{A["banner"]}" alt="Banner, desktop crop">
      <div class="chead"><img src="{A["avatar"]}" alt=""><div><div class="nm">Then What?</div><div class="meta sub">@thenwhattvshow · 3 videos</div><div class="meta sub">Something goes wrong. Then what? <b>...more</b></div><span class="btn">Subscribe</span></div></div>
    </div>
  </div>
</section>

<section>
  <div class="side"><span class="eyebrow">Channel page, phone</span><h2>Only the safe strip survives</h2><p class="note">Phones crop the banner to the centred 1546×423 strip. The whole lockup and strapline sit inside it, so nothing is lost.</p></div>
  <div class="stage">
    <div class="yt yt-dark phone">
      <img class="banner" src="{A["banner"]}" alt="Banner, phone crop">
      <div class="chead"><img src="{A["avatar"]}" alt=""><div><div class="nm">Then What?</div><div class="meta sub">@thenwhattvshow · 3 videos</div></div></div>
    </div>
  </div>
</section>

<section>
  <div class="side"><span class="eyebrow">Small sizes</span><h2>The mark at 98, 48 and 24 px</h2><p class="note">The subscriptions rail renders avatars at 48 px; comment replies at 24 px. At 24 px the mark becomes a ring with a bite and a separate dot, which is still a question mark.</p></div>
  <div class="stage">
    <div class="marks">
      <figure><div class="box" style="width:98px;height:98px"><img src="{A["avatar"]}" style="width:98px;height:98px;border-radius:50%" alt=""></div><figcaption>98 px · channel list</figcaption></figure>
      <figure><div class="box" style="width:48px;height:48px"><img src="{A["avatar"]}" style="width:48px;height:48px;border-radius:50%" alt=""></div><figcaption>48 px · rail</figcaption></figure>
      <figure><div class="box" style="width:32px;height:32px"><img src="{A["avatar"]}" style="width:32px;height:32px;border-radius:50%" alt=""></div><figcaption>32 px</figcaption></figure>
      <figure><div class="box" style="width:24px;height:24px"><img src="{A["avatar"]}" style="width:24px;height:24px;border-radius:50%" alt=""></div><figcaption>24 px · reply</figcaption></figure>
    </div>
    {rail(48, False)}
    {rail(48, True)}
    <div class="comment yt yt-light">
      <img src="{A["avatar"]}" style="width:40px;height:40px;border-radius:50%" alt="">
      <div class="body"><span class="who">@thenwhattvshow <span class="sub" style="font-weight:400">· 1 day ago</span></span>
        <span>The whole video in five lines: feet first · breathe for sixty seconds · get to the ring · knees to chest · one arm up. Which cruise are you on next?</span>
        <div class="reply"><img src="{A["avatar"]}" style="width:24px;height:24px;border-radius:50%" alt=""><span class="sub">Replying as Then What? at 24 px</span></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="side"><span class="eyebrow">Player</span><h2>Watermark over the brightest footage</h2><p class="note">Single-colour Bone with a soft Deep shadow, bottom-right, over a freezer-white frame. Yellow would vanish here and fight the burned-in text.</p></div>
  <div class="stage">
    <div class="player"><img class="wm" src="{A["wm"]}" alt="Watermark"><div class="bar"></div><div class="prog2"></div><div class="prog"></div></div>
  </div>
</section>

<section>
  <div class="side"><span class="eyebrow">Browse feed</span><h2>Thumbnails carry the badge, not the wordmark</h2><p class="note">Stand-in frames for the three delivered thumbnails, same titles and yellow-stroke treatment. The mark sits top-left at 11% height, sharing the 32 px left edge with the title. Duration pill stays clear bottom-right.</p></div>
  <div class="stage">
    <div class="yt yt-light feed">
      {"".join(f'<div class="item">{thumb(t, g, 272)}<div class="row"><img src="{A["avatar"]}" alt=""><div><div class="t">{name}</div><div class="m sub">Then What? · 12K views · 2 days ago</div></div></div></div>' for t, g, name, d in THUMBS)}
    </div>
  </div>
</section>

<section>
  <div class="side"><span class="eyebrow">Playlists</span><h2>Six pillars, one mark</h2><p class="note">Punctuation carries no genre. The pillar word sits in Fog beside the same mark; nothing else changes.</p></div>
  <div class="stage">
    <div class="yt yt-dark plist">
      {"".join(f'<div><img src="{A["p_"+k]}" alt=""><div class="n">{n}</div><div class="sub">Playlist</div></div>' for k, n in [("whatif","What If"),("survival","Survival"),("mysteries","Mysteries"),("body","Your Body"),("space","Space"),("tests","Tests")])}
    </div>
  </div>
</section>

<section>
  <div class="side"><span class="eyebrow">End screen</span><h2>The last twenty seconds</h2><p class="note">Ground plate with the sign-off. Elements are added in Studio: next episode left, subscribe right, playlist below. The dot lands on the word "what".</p></div>
  <div class="stage">
    <div class="endwrap"><img src="{A["end"]}" alt="End screen plate">
      <div class="zone" style="left:6%;top:42%;width:40%;aspect-ratio:16/9">Next episode</div>
      <div class="zone" style="left:56%;top:46%;width:14%;aspect-ratio:1;border-radius:50%">Subscribe</div>
      <div class="zone" style="left:6%;top:82%;width:40%;height:10%">Survival playlist</div>
    </div>
  </div>
</section>

<section>
  <div class="side"><span class="eyebrow">Shorts</span><h2>Stacked lockup, top-centre</h2><p class="note">The one place the wordmark sits over footage: above the 9:16 UI gutter, with the mark spanning both lines.</p></div>
  <div class="stage"><div class="shorts"><img src="{A["shorts"]}" alt="Shorts stamp"></div></div>
</section>

<section style="border-bottom:0">
  <div class="side"><span class="eyebrow">Rules</span><h2>What never changes</h2></div>
  <ul class="rules">
    <li>The wordmark never appears on a thumbnail.</li>
    <li>The dot is the only element that is ever Signal yellow.</li>
    <li>Watermark and badge are single-colour Bone.</li>
    <li>Do not pre-round the avatar; YouTube applies the circle.</li>
    <li>Below 180 px wide, use the mark alone.</li>
    <li>No rounded caps, no gradients, no glow. Flat cuts, one shadow at most.</li>
  </ul>
</section>
</main>
'''
(OUT / "preview.html").write_text(html)
print(OUT / "preview.html", len(html) // 1024, "KB")
