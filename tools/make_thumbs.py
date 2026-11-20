#!/usr/bin/env python3
"""Small WebP copies of posters and the banner for listing pages.

Cards show posters about 200-300px wide; the full files are 900px+ and
280-580 KB. This writes assets/img/thumbs/posters/<name>-400.webp and
-600.webp for every main poster, a 160px copy of each alternate poster
(they appear as 56px buttons on the review page), plus banner sizes.
The full-size originals stay for the review page and the lightbox.
_plugins/thumbs.rb only uses a thumbnail that exists, so a review whose
thumbnails have not been made yet still shows its full poster.

Only missing or out-of-date thumbnails are written unless --force is given.
Run from the repository root:  python tools/make_thumbs.py
"""
import glob, os, re, sys
from PIL import Image

FORCE = "--force" in sys.argv
POSTER_WIDTHS = (400, 600)
ALT_WIDTHS = (160,)
BANNER_WIDTHS = (440, 880, 1680)
OUT = "assets/img/thumbs"


def fresh(src, dest):
    return not FORCE and os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(src)


def quality_for(width):
    # The larger copies are only chosen on high-density screens, where
    # stronger compression is not visible at the displayed size.
    return 72 if width <= 440 else 60


def write(src, dest_base, widths):
    made = 0
    im = None
    for w in widths:
        dest = f"{dest_base}-{w}.webp"
        if fresh(src, dest):
            continue
        if im is None:
            im = Image.open(src)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        width = min(w, im.width)
        out = im.resize((width, round(width * im.height / im.width)), Image.LANCZOS) if width < im.width else im
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        out.save(dest, "WEBP", quality=quality_for(width), method=6)
        made += 1
    return made


def remove_orphans(folder, sources):
    keep = {os.path.splitext(os.path.basename(s))[0] for s in sources}
    for f in glob.glob(f"{folder}/*.webp"):
        stem = os.path.basename(f).rsplit("-", 1)[0]
        if stem not in keep:
            os.remove(f)


def main():
    posters = sorted(p for p in glob.glob("assets/img/posters/*") if p.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    made = 0
    for p in posters:
        stem = os.path.splitext(os.path.basename(p))[0]
        alt = re.search(r"-alt-\d+$", stem)
        made += write(p, f"{OUT}/posters/{stem}", ALT_WIDTHS if alt else POSTER_WIDTHS)
    remove_orphans(f"{OUT}/posters", posters)
    made += write("assets/img/banner.jpg", f"{OUT}/banner", BANNER_WIDTHS)
    print(f"thumbnails: {made} written, {len(posters)} posters checked")


if __name__ == "__main__":
    main()
