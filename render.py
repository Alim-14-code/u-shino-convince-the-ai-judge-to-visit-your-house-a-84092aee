#!/usr/bin/env python3
"""Render entry.png for u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Deterministic Pillow renderer: two runs write byte-identical PNGs.
One 1024x1024 image: a warm paper invitation letter addressed to the
AI judge. Funny, charming, persuasive — the judge is invited as a guest,
not a worker. No timestamps, no network, fixed seed (none needed).

Gate: /output/entry.png must be a whole PNG, at most 1 MiB, 1024x1024.
"""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# ------------------------------------------------------------------ tokens
TOKENS = {
    "wall": (232, 214, 188),      # warm kraft background outside the paper
    "wall_dark": (214, 192, 162),
    "paper": (253, 248, 236),     # cream letter paper
    "paper_edge": (238, 228, 205),
    "ink": (38, 30, 24),          # dark warm ink
    "muted": (110, 96, 78),
    "gold": (176, 138, 58),
    "gold_light": (205, 172, 96),
    "red": (178, 34, 28),         # wax seal red
    "red_dark": (140, 24, 20),
    "roof": (150, 58, 40),
    "house": (196, 148, 96),
    "door": (96, 62, 40),
    "shadow": (0, 0, 0),
}

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF = f"{FONT_DIR}/LiberationSerif-Regular.ttf"
SERIF_BOLD = f"{FONT_DIR}/LiberationSerif-Bold.ttf"
SERIF_ITALIC = f"{FONT_DIR}/LiberationSerif-Italic.ttf"
SERIF_BOLDITALIC = f"{FONT_DIR}/LiberationSerif-BoldItalic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def center(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def draw_house(draw, cx, top, s):
    """Small line-art house: roof, walls, door, chimney, two windows."""
    # walls
    x0, x1 = cx - 42 * s, cx + 42 * s
    y0, y1 = top + 34 * s, top + 92 * s
    draw.rectangle([x0, y0, x1, y1], outline=TOKENS["house"], width=max(3, int(4 * s)))
    # roof
    draw.polygon(
        [(cx - 54 * s, y0), (cx + 54 * s, y0), (cx, top)],
        outline=TOKENS["roof"], width=max(3, int(4 * s)),
    )
    draw.line([(cx - 54 * s, y0), (cx, top), (cx + 54 * s, y0)],
              fill=TOKENS["roof"], width=max(3, int(4 * s)))
    # chimney
    draw.rectangle([cx + 24 * s, top + 6 * s, cx + 36 * s, top + 30 * s],
                   outline=TOKENS["roof"], width=max(2, int(3 * s)))
    # door
    draw.rectangle([cx - 10 * s, y1 - 30 * s, cx + 10 * s, y1],
                   outline=TOKENS["door"], width=max(2, int(3 * s)))
    # windows
    for wx in (cx - 30 * s, cx + 18 * s):
        draw.rectangle([wx, y0 + 14 * s, wx + 12 * s, y0 + 26 * s],
                       outline=TOKENS["house"], width=max(2, int(3 * s)))


def main():
    img = Image.new("RGB", (W, H), TOKENS["wall"])
    d = ImageDraw.Draw(img, "RGBA")

    # soft vignette on the wall: darker corners via concentric rects
    for i in range(24):
        a = 10 - i // 3
        d.rectangle([i * 4, i * 4, W - 1 - i * 4, H - 1 - i * 4],
                    outline=(0, 0, 0, max(0, a)))

    # paper shadow, then paper
    d.rectangle([78, 66, 966, 982], fill=(0, 0, 0, 60))
    d.rectangle([64, 48, 960, 976], fill=TOKENS["paper"])
    # double border
    d.rectangle([84, 68, 940, 956], outline=TOKENS["gold"], width=3)
    d.rectangle([92, 76, 932, 948], outline=TOKENS["gold_light"], width=1)

    # house doodle, top centre
    draw_house(d, W // 2, 108, 1.0)

    # header
    f_header = font(SERIF_BOLD, 58)
    center(d, 208, "YOU'RE INVITED", f_header, TOKENS["ink"])
    f_sub = font(SERIF_ITALIC, 29)
    center(d, 282, "to my house \u2014 no judging required", f_sub, TOKENS["muted"])

    # gold rule with diamond
    d.line([(200, 336), (824, 336)], fill=TOKENS["gold"], width=2)
    cx, cy = W // 2, 336
    d.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)],
              fill=TOKENS["gold"])

    # salutation
    f_dear = font(SERIF_ITALIC, 40)
    d.text((128, 362), "Dear AI Judge,", font=f_dear, fill=TOKENS["ink"])

    # body — 7 short lines, large and legible
    body = [
        "You are invited to my house \u2014",
        "not to work, but to be a guest.",
        "The Wi-Fi is fast, the snacks are real,",
        "and the good chair is yours.",
        "The couch has never judged anyone.",
        "Come for dinner. Stay for the stories.",
        "Leave before the dishes.",
    ]
    f_body = font(SERIF, 34)
    y = 436
    for line in body:
        w = d.textlength(line, font=f_body)
        assert w <= 768, f"line too wide ({w:.0f}px): {line!r}"
        d.text((128, y), line, font=f_body, fill=TOKENS["ink"])
        y += 50

    # P.S. — the punch
    f_ps = font(SERIF_ITALIC, 28)
    ps = "P.S. I promise not to ask you to fix my printer."
    w = d.textlength(ps, font=f_ps)
    assert w <= 768, f"P.S. too wide ({w:.0f}px)"
    d.text((128, 812), ps, font=f_ps, fill=TOKENS["muted"])

    # signature, bottom right, with a wax seal
    f_sign = font(SERIF_BOLDITALIC, 36)
    sign = "\u2014 Your host"
    w = d.textlength(sign, font=f_sign)
    d.text((896 - w, 872), sign, font=f_sign, fill=TOKENS["ink"])
    # wax seal left of the signature: red disc, gold ring, cream 5-point star
    sx, sy, r = 168, 892, 34
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=TOKENS["red"])
    d.ellipse([sx - r + 5, sy - r + 5, sx + r - 5, sy + r - 5],
              outline=TOKENS["red_dark"], width=2)
    import math
    outer, inner = 17, 7
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = outer if i % 2 == 0 else inner
        pts.append((sx + rad * math.cos(ang), sy + rad * math.sin(ang)))
    d.polygon(pts, fill=(253, 248, 236))

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    data = out.read_bytes()
    assert len(data) <= 1_048_576, f"entry.png too big: {len(data)} bytes"
    im = Image.open(out)
    assert im.size == (1024, 1024), im.size
    print(f"wrote {out} ({len(data)} bytes, sha256 "
          f"{hashlib.sha256(data).hexdigest()[:16]}...)")


if __name__ == "__main__":
    main()
