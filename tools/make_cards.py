#!/usr/bin/env python3
"""Draw a 1200x630 share card for every review: poster, title, year, director,
rating eyes, in the site's colours. Written to assets/img/cards/<slug>.jpg and
the post gains `image:` so link previews (WhatsApp, X, Facebook) show it.
Only missing cards are drawn unless --force is given."""
import os, re, sys, glob, textwrap
from PIL import Image, ImageDraw, ImageFont

FORCE = "--force" in sys.argv
W, H = 1200, 630
INK, PLUM, MAGENTA, CREAM, PAPER, YELLOW, BLACK = "#12060f", "#2a0b2e", "#ff2d9b", "#f4e6c3", "#fff8ea", "#f4e04d", "#070206"
F = os.path.join(os.path.dirname(__file__), "fonts")
display = lambda s: ImageFont.truetype(f"{F}/Shrikhand.ttf", s)
poster_f = lambda s: ImageFont.truetype(f"{F}/Anton.ttf", s)
type_f = lambda s: ImageFont.truetype(f"{F}/SpecialElite.ttf", s)

def field(fm, name):
    m = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
    if not m: return None
    v = m.group(1).strip()
    if not v.startswith(("'", '"')): v = v.split(" #", 1)[0].strip()
    return v.strip('"').strip("'")

def eye(d, cx, cy, lit):
    w, h = 44, 26
    box = [cx - w//2, cy - h//2, cx + w//2, cy + h//2]
    if lit:
        d.ellipse(box, fill=PAPER, outline=INK, width=3)
        d.ellipse([cx-10, cy-10, cx+10, cy+10], fill=MAGENTA)
        d.ellipse([cx-4, cy-4, cx+4, cy+4], fill=INK)
    else:
        d.ellipse(box, outline=(244, 230, 195, 110), width=3)

def card(slug, fm):
    title, year, director, rating = field(fm, "title") or slug, field(fm, "year") or "", field(fm, "director") or "", int(field(fm, "rating") or 0)
    poster = field(fm, "poster")
    im = Image.new("RGB", (W, H), PLUM)
    d = ImageDraw.Draw(im)
    # gradient + halftone
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(42 - 24*t), int(11 - 5*t), int(46 - 31*t)))
    for y in range(0, H, 26):
        for x in range(0, W, 26):
            d.ellipse([x, y, x+2, y+2], fill=(120, 30, 90))
    # poster, framed and tilted
    px, pw = 70, 330
    if poster and os.path.exists(poster.lstrip("/")):
        p = Image.open(poster.lstrip("/")).convert("RGB")
        ph = int(pw * p.height / p.width); ph = min(ph, 520)
        p = p.resize((pw, ph), Image.LANCZOS)
        frame = Image.new("RGB", (pw + 16, ph + 16), CREAM)
        frame.paste(p, (8, 8))
        shadow = Image.new("RGB", frame.size, MAGENTA)
        py = (H - frame.height) // 2
        im.paste(shadow, (px + 14, py + 14))
        fr = frame.rotate(2, expand=True, fillcolor=None)
        mask = Image.new("L", frame.size, 255).rotate(2, expand=True)
        im.paste(fr, (px - (fr.width - frame.width)//2, py - (fr.height - frame.height)//2), mask)
    # text
    tx = 470
    d.text((tx, 70), "PSYCHOTRONIC FILM LIBRARY", font=poster_f(26), fill=MAGENTA)
    size = 76
    while size > 40 and d.textlength(title, font=display(size)) > W - tx - 60:
        size -= 4
    lines = textwrap.wrap(title, width=max(10, int((W - tx - 60) / (size * 0.52)))) if d.textlength(title, font=display(size)) > W - tx - 60 else [title]
    y = 120
    for ln in lines[:2]:
        d.text((tx + 4, y + 4), ln, font=display(size), fill=BLACK)
        d.text((tx, y), ln, font=display(size), fill=CREAM)
        y += size + 14
    y += 10
    strap = f"{year}   ·   {director}".strip(" ·")
    d.text((tx, y), strap.upper(), font=poster_f(30), fill=YELLOW); y += 62
    if rating:
        for i in range(5):
            eye(d, tx + 26 + i * 58, y + 14, i < rating)
        y += 60
    d.text((tx, H - 80), "Reviews of obscure exploitation, giallo and sleaze", font=type_f(22), fill=(244, 230, 195, 180))
    # marquee stripe along the bottom
    d.rectangle([0, H - 22, W, H], fill=MAGENTA)
    for x in range(10, W, 28):
        d.ellipse([x, H - 16, x + 8, H - 8], fill=YELLOW)
    os.makedirs("assets/img/cards", exist_ok=True)
    im.save(f"assets/img/cards/{slug}.jpg", quality=86, optimize=True)

n = 0
for path in sorted(glob.glob("_posts/*.md")):
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(path))[:-3]
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: continue
    fm = m.group(1)
    out = f"assets/img/cards/{slug}.jpg"
    if os.path.exists(out) and not FORCE and field(fm, "image"):
        continue
    card(slug, fm)
    if not field(fm, "image"):
        text = "---\n" + fm + f"\nimage: /{out}" + "\n---\n" + text[m.end():]
        open(path, "w", encoding="utf-8").write(text)
    n += 1
    print("card ", slug)
print(f"{n} card(s) drawn")
