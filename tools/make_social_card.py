#!/usr/bin/env python3
"""Draw the 1200x630 site-wide share card (assets/img/social-card-wide.jpg)
from the 1200x400 banner card, for pages that are not reviews. Large-card
previews (X, Facebook, WhatsApp, Bluesky) expect roughly 1.91:1; the 3:1
original gets cropped or shown small. Run again only if the artwork changes."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PLUM, INK, MAGENTA, CREAM, YELLOW, BLACK = "#2a0b2e", "#12060f", "#ff2d9b", "#f4e6c3", "#f4e04d", "#070206"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "tools", "fonts")

im = Image.new("RGB", (W, H), PLUM)
d = ImageDraw.Draw(im)
for y in range(H):  # plum to ink, as on the site background
    t = y / H
    a, b = (0x2a, 0x0b, 0x2e), (0x12, 0x06, 0x0f)
    d.line([(0, y), (W, y)], fill=tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)))
for y in range(0, H, 26):  # halftone dots
    for x in range(0, W, 26):
        d.ellipse([x + 12, y + 12, x + 14, y + 14], fill=(110, 30, 90))

art = Image.open(os.path.join(ROOT, "assets/img/social-card.jpg")).convert("RGB")
aw = 1104
art = art.resize((aw, round(aw * art.height / art.width)), Image.LANCZOS)
x0, y0 = (W - aw) // 2, 58
d.rectangle([x0 - 10 + 10, y0 - 10 + 10, x0 + aw + 10 + 10, y0 + art.height + 10 + 10], fill=MAGENTA)
d.rectangle([x0 - 10, y0 - 10, x0 + aw + 10, y0 + art.height + 10], fill=CREAM, outline=BLACK, width=3)
im.paste(art, (x0, y0))

tag = "Obscure exploitation, giallo, eurosleaze and cult horror".upper()
f = ImageFont.truetype(os.path.join(F, "Anton.ttf"), 38)
tw = d.textlength(tag, font=f)
ty = y0 + art.height + 34
d.text(((W - tw) / 2 + 3, ty + 3), tag, font=f, fill=BLACK)
d.text(((W - tw) / 2, ty), tag, font=f, fill=YELLOW)
site = "psychotronicfilmlibrary.com"
g = ImageFont.truetype(os.path.join(F, "SpecialElite.ttf"), 28)
sw = d.textlength(site, font=g)
d.text(((W - sw) / 2, ty + 58), site, font=g, fill=CREAM)

im.save(os.path.join(ROOT, "assets/img/social-card-wide.jpg"), quality=86, optimize=True, progressive=True)
print("wrote assets/img/social-card-wide.jpg")
