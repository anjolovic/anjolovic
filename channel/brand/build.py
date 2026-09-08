#!/usr/bin/env python3
"""Then What? brand asset builder ("The Drop").

Renders every PNG YouTube needs from one SVG mark and two font files, using
headless Chromium so type is set in real Archivo. Run from anywhere:

    python3 channel/brand/build.py            # build everything into channel/brand/out/
    python3 channel/brand/build.py avatar     # build one asset by name

Requires: Chromium at $CHROMIUM (default /opt/pw-browsers/chromium) and
channel/brand/fonts/Archivo-{500,700}.woff2.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
FONTS = HERE / "fonts"
CHROMIUM = os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium")

# ---------------------------------------------------------------- tokens
TOKENS = {
    "name": "Then What?",
    "direction": "The Drop",
    "colors": {
        "deep": "#0E1A24",    # ground
        "bone": "#F5F1E8",    # ink
        "signal": "#FFC300",  # the dot, and nothing else
        "fog": "#7C8894",     # straplines, rules, secondary
    },
    "type": {
        "wordmark": {"family": "Archivo", "weight": 700, "case": "upper", "tracking_em": 0.045},
        "support": {"family": "Archivo", "weight": 500, "case": "upper", "tracking_em": 0.14},
        "thumbnail_title": {"family": "Anton or Bebas Neue", "note": "thumbnails only, never the wordmark"},
    },
    "mark": {
        "viewBox": "0 0 120 120",
        "stroke": 15,
        "bowl_center": [60, 40],
        "bowl_centerline_radius": 22.5,
        "stem_x": 60,
        "stem_foot_y": 82,
        "dot_center": [60, 101],
        "dot_radius": 10.5,
        "ink_box": [30, 10, 90, 111.5],
        "cap_height_units": 72,
        "dot_drop_below_baseline": "0.26 x cap height (centre), 0.41 x cap height (bottom)",
    },
    "sizes": {
        "avatar": [800, 800],
        "watermark": [150, 150],
        "banner": [2560, 1440],
        "banner_min": [2048, 1152],
        "banner_safe_2560": [1546, 423],
        "banner_safe_2048": [1235, 338],
        "thumbnail": [1280, 720],
        "end_screen": [1920, 1080],
        "shorts": [1080, 1920],
    },
    "rules": [
        "The wordmark never appears on a thumbnail.",
        "The dot is the only element that is ever Signal yellow.",
        "Watermark and thumbnail badge are single-colour Bone.",
        "Clear space around the mark: one stroke width; two on the banner.",
        "Minimum wordmark width 180 px; below that use the mark alone.",
    ],
}
C = TOKENS["colors"]

# ---------------------------------------------------------------- the mark
# Centreline geometry on a 120 x 120 box. Bowl: circle centre (60,40), r 22.5,
# from 9 o'clock (37.5,40) clockwise over the top to (71.25,59.5), a 240° sweep.
# Shoulder: cubic into a dead-centre vertical stem, x = 60, foot at y = 82.
# Dot: centre (60,101), r 10.5 = 1.4 x stroke, gap to foot 8.5 = 0.57 x stroke.
MARK_PATH = "M37.5 40 A22.5 22.5 0 1 1 71.25 59.5 C66.05 62.5 60 65 60 70 L60 82"


def mark_svg(ink=C["bone"], dot=C["signal"], size=None, extra_attr=""):
    """The mark as an inline SVG. Bowl and stem are one stroked path with
    flat (butt) terminals; the dot is a separate filled circle."""
    dim = f'width="{size}" height="{size}"' if size else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" {dim} {extra_attr}>'
        f'<path d="{MARK_PATH}" fill="none" stroke="{ink}" stroke-width="15" '
        f'stroke-linecap="butt" stroke-linejoin="round"/>'
        f'<circle cx="60" cy="101" r="10.5" fill="{dot}"/>'
        f"</svg>"
    )


def mark_glyph_svg(ink, dot, cap_px):
    """The mark sized so that bowl top to stem foot equals cap_px (the cap
    height of adjacent type). Returns (svg, total_height_px, width_px,
    ascent_px) for baseline alignment: ascent is the bowl-top-to-baseline
    distance in px, which equals cap_px."""
    unit = cap_px / 72.0  # 72 units = bowl top (10) to stem foot (82)
    total_h = 101.5 * unit  # 10 -> 111.5
    w = 60 * unit           # 30 -> 90
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="30 10 60 101.5" '
        f'width="{w:.2f}" height="{total_h:.2f}" style="display:block">'
        f'<path d="{MARK_PATH}" fill="none" stroke="{ink}" stroke-width="15" '
        f'stroke-linecap="butt" stroke-linejoin="round"/>'
        f'<circle cx="60" cy="101" r="10.5" fill="{dot}"/>'
        f"</svg>"
    )
    return svg, total_h, w


# ---------------------------------------------------------------- html shell
def font_face():
    return f"""
@font-face {{ font-family:'Archivo'; font-weight:700; src:url('file://{FONTS}/Archivo-700.woff2') format('woff2'); }}
@font-face {{ font-family:'Archivo'; font-weight:500; src:url('file://{FONTS}/Archivo-500.woff2') format('woff2'); }}
"""


# Archivo 700 cap height, measured against the em box in Chromium: 0.716 em.
CAP_RATIO = 0.716


def wordmark_html(cap_px, ink=C["bone"], dot=C["signal"], tracking_em=0.045, gap_ratio=0.28):
    """'THEN WHAT' in Archivo 700 followed by the mark as the question mark,
    bowl top on the cap line, stem foot on the baseline, dot hanging below."""
    font_px = cap_px / CAP_RATIO
    svg, total_h, w = mark_glyph_svg(ink, dot, cap_px)
    # Flex row aligned on the baseline: type gets its natural line box; the
    # mark is placed with its top at (line_top + ascent - cap).
    return f"""
<div class="wm" style="display:inline-flex;align-items:flex-start;font-family:Archivo;font-weight:700;
     font-size:{font_px:.2f}px;line-height:1;letter-spacing:{tracking_em}em;color:{ink};white-space:nowrap">
  <span style="display:block;line-height:1;padding-top:{font_px*(1-CAP_RATIO)*0.5:.2f}px">THEN&nbsp;WHAT</span>
  <span style="display:block;margin-left:{cap_px*gap_ratio:.2f}px;padding-top:{font_px*(1-CAP_RATIO)*0.5:.2f}px">{svg}</span>
</div>"""


def page(body, w, h, bg, extra_css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_face()}
html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:{bg};}}
*{{box-sizing:border-box;}}
.abs{{position:absolute;}}
{extra_css}
</style></head><body>{body}</body></html>"""


def render(name, html, w, h, transparent=False, crop=None, trim_pad=None, bg_rgb=None):
    """Screenshot html at w x h. Headless Chromium enforces a minimum window
    size, so small assets are rendered on a large canvas and then cropped:
    crop=(left, top, right, bottom) cuts a fixed box; trim_pad=N autocrops to
    the content bounding box plus N px (alpha for transparent pages, colour
    difference from bg_rgb otherwise)."""
    OUT.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=str(OUT)) as f:
        f.write(html)
        src = f.name
    dst = OUT / f"{name}.png"
    args = [
        CHROMIUM, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", f"--window-size={w},{h}",
        "--allow-file-access-from-files", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=2000",
        f"--screenshot={dst}", f"file://{src}",
    ]
    if transparent:
        args.insert(1, "--default-background-color=00000000")
    subprocess.run(args, check=True, capture_output=True)
    os.unlink(src)
    if crop or trim_pad is not None:
        from PIL import Image, ImageChops
        im = Image.open(dst)
        if crop:
            im = im.crop(crop)
        if trim_pad is not None:
            if transparent:
                bbox = im.split()[-1].getbbox()
            else:
                base = Image.new(im.mode, im.size, bg_rgb)
                bbox = ImageChops.difference(im.convert("RGB"), base.convert("RGB")).getbbox()
            if bbox:
                l, t, r, b = bbox
                im = im.crop((max(0, l - trim_pad), max(0, t - trim_pad), min(im.width, r + trim_pad), min(im.height, b + trim_pad)))
        im.save(dst)
    return dst


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- assets
def build_avatar():
    # Mark at 58% of canvas height, ink-weight centred: nudge up 20 px.
    h = 464
    unit = h / 101.5
    w = 60 * unit
    # mark_svg with extra viewBox: rebuild directly
    body = (f'<div class="abs" style="left:{(800-w)/2:.1f}px;top:{(800-h)/2-20:.1f}px">'
            f'{mark_glyph_svg(C["bone"], C["signal"], h*72/101.5)[0]}</div>')
    return render("avatar-800", page(body, 800, 800, C["deep"]), 800, 800)


def build_watermark():
    # Single colour Bone, 118 px tall, soft Deep shadow, transparent ground.
    h = 118
    svg, total_h, w = mark_glyph_svg(C["bone"], C["bone"], h * 72 / 101.5)
    cx, cy = 400, 400
    body = (f'<div class="abs" style="left:{cx-w/2:.1f}px;top:{cy-h/2:.1f}px;'
            f'filter:drop-shadow(0 0 4px rgba(14,26,36,.55))">{svg}</div>')
    return render("watermark-150", page(body, 800, 800, "transparent"), 800, 800,
                  transparent=True, crop=(cx - 75, cy - 75, cx + 75, cy + 75))


def build_banner(W, H, name):
    """Flat typographic banner. Everything that must survive the phone crop
    sits inside the centred safe strip (1546x423 at 2560, 1235x338 at 2048).
    Metrics: within .wm the cap line sits at 0.142 em below the block top,
    the baseline at 0.142 em + cap, the dot bottom at 0.142 em + 1.41 cap."""
    s = W / 2048.0
    safe_w, safe_h = 1235 * s, 338 * s
    sx, sy = (W - safe_w) / 2, (H - safe_h) / 2
    cap = 103 * s                      # lockup ~1290 px wide at 2560, ~128 px air each side
    font_px = cap / CAP_RATIO
    lead = 0.142 * font_px
    strap_px = 30 * s
    strap_gap = 44 * s
    block_h = lead + 1.41 * cap + strap_gap + strap_px
    top = sy + (safe_h - block_h) / 2
    baseline_y = top + lead + cap
    strap_top = top + lead + 1.41 * cap + strap_gap
    # ghost mark, outside the safe strip on the right, texture only
    ghost_h = 1400 * s
    ghost_svg, gh, gw = mark_glyph_svg(C["bone"], C["bone"], ghost_h * 72 / 101.5)
    ghost_left = sx + safe_w + 60 * s
    body = f"""
<div class="abs" style="left:{ghost_left:.1f}px;top:{(H-gh)/2:.1f}px;opacity:.05">{ghost_svg}</div>
<div class="abs" style="left:0;top:{baseline_y:.1f}px;width:{W}px;height:{max(2, round(3*s))}px;background:{C['bone']};opacity:.14"></div>
<div class="abs" style="left:0;top:{top:.1f}px;width:{W}px;display:flex;justify-content:center">
  <div style="position:relative">
    {wordmark_html(cap)}
    <div style="position:absolute;left:0;top:{strap_top-top:.1f}px;font-family:Archivo;font-weight:500;font-size:{strap_px:.1f}px;line-height:1;
         letter-spacing:.14em;color:{C['fog']};white-space:nowrap">SOMETHING GOES WRONG.</div>
  </div>
</div>"""
    css = ".wm span{vertical-align:top}"
    return render(name, page(body, W, H, C["deep"], css), W, H)


def build_thumbnail_badge():
    # Mark, Bone, 11% of 720 = 79 px tall, inset 32 px top-left, transparent.
    h = 79
    svg, th, w = mark_glyph_svg(C["bone"], C["bone"], h * 72 / 101.5)
    body = f'<div class="abs" style="left:32px;top:32px;filter:drop-shadow(0 0 4px rgba(14,26,36,.55))">{svg}</div>'
    return render("thumbnail-badge-1280x720", page(body, 1280, 720, "transparent"), 1280, 720, transparent=True)


PILLARS = [
    ("whatif", "WHAT IF"), ("survival", "SURVIVAL"), ("mysteries", "MYSTERIES"),
    ("body", "YOUR BODY"), ("space", "SPACE"), ("tests", "TESTS"),
]


def build_playlist_covers():
    outs = []
    for key, word in PILLARS:
        h = 360
        svg, th, w = mark_glyph_svg(C["bone"], C["signal"], h * 72 / 101.5)
        body = f"""
<div class="abs" style="left:0;top:0;width:1280px;height:720px;display:flex;align-items:center;justify-content:center;gap:72px">
  <div style="margin-top:-24px">{svg}</div>
  <div style="font-family:Archivo;font-weight:500;font-size:64px;letter-spacing:.14em;color:{C['fog']};line-height:1">{word}</div>
</div>"""
        outs.append(render(f"playlist-{key}-1280x720", page(body, 1280, 720, C["deep"]), 1280, 720))
    return outs


def build_end_screen():
    # Ground plate for the final 20 s. Elements are placed in Studio:
    # video element left, subscribe right, playlist below. Keep the lower
    # two-thirds clear; sign-off top-centre.
    cap = 84
    body = f"""
<div class="abs" style="left:0;top:96px;width:1920px;text-align:center">
  <div style="display:inline-block">{wordmark_html(cap)}</div>
  <div style="margin-top:40px;font-family:Archivo;font-weight:500;font-size:34px;letter-spacing:.14em;color:{C['fog']}">THAT'S WHAT. SEE YOU IN THE NEXT ONE.</div>
</div>
<div class="abs" style="left:0;top:{96+cap+40+34+60}px;width:1920px;height:2px;background:{C['bone']};opacity:.10"></div>"""
    return render("end-screen-1920x1080", page(body, 1920, 1080, C["deep"], ".wm span{vertical-align:top}"), 1920, 1080)


def build_shorts_stamp():
    # Stacked lockup, top-centre, above the 9:16 UI gutter, transparent.
    cap = 86
    font_px = cap / CAP_RATIO
    svg, mh, mw = mark_glyph_svg(C["bone"], C["signal"], cap * 2 * 72 / 72)  # mark spans both lines
    body = f"""
<div class="abs" style="left:0;top:150px;width:1080px;text-align:center;filter:drop-shadow(0 0 6px rgba(14,26,36,.6))">
  <div style="display:inline-flex;align-items:flex-start;gap:{cap*0.35:.0f}px;font-family:Archivo;font-weight:700;font-size:{font_px:.1f}px;line-height:{cap*1.16/font_px*1.0:.3f};letter-spacing:.045em;color:{C['bone']};text-align:left">
    <div><div>THEN</div><div>WHAT</div></div>
    <div style="padding-top:{font_px*(1-CAP_RATIO)*0.5:.1f}px">{mark_glyph_svg(C['bone'], C['signal'], cap + cap*1.16)[0]}</div>
  </div>
</div>"""
    return render("shorts-stamp-1080x1920", page(body, 1080, 1920, "transparent"), 1080, 1920, transparent=True)


def build_wordmark_pngs():
    cap = 200
    body = f'<div class="abs" style="left:40px;top:60px">{wordmark_html(cap)}</div>'
    W, H = 3200, 700
    a = render("wordmark-horizontal-deep", page(body, W, H, C["deep"], ".wm span{vertical-align:top}"), W, H,
               trim_pad=60, bg_rgb=hex_rgb(C["deep"]))
    body2 = f'<div class="abs" style="left:40px;top:60px">{wordmark_html(cap, ink=C["deep"], dot=C["signal"])}</div>'
    b = render("wordmark-horizontal-bone", page(body2, W, H, C["bone"], ".wm span{vertical-align:top}"), W, H,
               trim_pad=60, bg_rgb=hex_rgb(C["bone"]))
    return [a, b]


def write_sources():
    (HERE / "mark.svg").write_text(mark_svg() + "\n")
    (HERE / "mark-mono.svg").write_text(mark_svg(ink=C["bone"], dot=C["bone"]) + "\n")
    (HERE / "mark-on-bone.svg").write_text(mark_svg(ink=C["deep"], dot=C["signal"]) + "\n")
    (HERE / "tokens.json").write_text(json.dumps(TOKENS, indent=2) + "\n")


BUILDERS = {
    "avatar": build_avatar,
    "watermark": build_watermark,
    "banner": lambda: [build_banner(2560, 1440, "banner-2560x1440"), build_banner(2048, 1152, "banner-2048x1152")],
    "badge": build_thumbnail_badge,
    "playlists": build_playlist_covers,
    "endscreen": build_end_screen,
    "shorts": build_shorts_stamp,
    "wordmark": build_wordmark_pngs,
}

if __name__ == "__main__":
    write_sources()
    names = sys.argv[1:] or list(BUILDERS)
    for n in names:
        out = BUILDERS[n]()
        for p in (out if isinstance(out, list) else [out]):
            print(p.relative_to(HERE.parent.parent))
