#!/usr/bin/env python3
"""Fetch the best poster for every review from The Movie Database.

Runs in GitHub Actions (see .github/workflows/posters.yml). For each file in
_posts/, it looks the film up by title and year, downloads the highest-voted
English-language poster (falling back to any language), resizes it to 900px
wide, and writes it to assets/img/posters/<slug>.jpg. A post's poster is only
replaced when the existing file is narrower than MIN_WIDTH, or missing, or the
script is run with --force. The post's `poster:` line is added if absent.

Needs TMDB_API_KEY in the environment (a free v3 key from
https://www.themoviedb.org/settings/api).
"""
import io, os, re, sys, json, glob, urllib.parse, urllib.request
from PIL import Image

API = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p/original"
KEY = os.environ.get("TMDB_API_KEY", "").strip()
MIN_WIDTH = 700
FORCE = "--force" in sys.argv
CANDIDATES = "--candidates" in sys.argv
RESTILLS = "--restills" in sys.argv   # rebuild the stills strip even if a post has one
ONLY = [a for a in sys.argv[1:] if not a.startswith("--")]

if not KEY:
    sys.exit("TMDB_API_KEY is not set")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "psychotronic-film-library/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def api(path, **params):
    params["api_key"] = KEY
    return json.loads(get(f"{API}{path}?{urllib.parse.urlencode(params)}"))

def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), m.end()) if m else (None, 0)

def field(fm, name):
    m = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
    if not m: return None
    v = m.group(1).strip()
    if not v.startswith(("'", '"')):
        v = v.split(" #", 1)[0].strip()   # drop an inline YAML comment
    return v.strip('"').strip("'")

def best_poster(movie_id):
    imgs = api(f"/movie/{movie_id}/images", include_image_language="en,null")
    posters = imgs.get("posters") or []
    if not posters:
        posters = api(f"/movie/{movie_id}/images").get("posters") or []
    if not posters: return None
    en = [p for p in posters if p.get("iso_639_1") == "en"]
    pool = en or posters
    pool.sort(key=lambda p: (p.get("vote_count", 0), p.get("vote_average", 0), p.get("width", 0)), reverse=True)
    return pool[0]["file_path"]

def candidate_sheet(slug, movie):
    """Write _poster_candidates/<slug>.jpg: the top posters, numbered, plus a
    .txt listing each number's TMDB path. Pin one with `tmdb_poster:` in the post."""
    from PIL import ImageDraw
    imgs = api(f"/movie/{movie['id']}/images")
    posters = imgs.get("posters") or []
    posters.sort(key=lambda p: (p.get("vote_count", 0), p.get("vote_average", 0)), reverse=True)
    posters = posters[:16]
    if not posters:
        print(f"none  {slug}: TMDB has no posters"); return
    W, H, cols = 230, 345, 4
    rows = (len(posters) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W, rows * (H + 22)), "black")
    d = ImageDraw.Draw(sheet)
    lines = []
    for i, p in enumerate(posters):
        try:
            im = Image.open(io.BytesIO(get(f"https://image.tmdb.org/t/p/w342{p['file_path']}"))).convert("RGB")
        except Exception as e:
            print(f"  candidate {i+1}: {e}"); continue
        im.thumbnail((W, H))
        x, y = (i % cols) * W, (i // cols) * (H + 22)
        sheet.paste(im, (x + (W - im.width) // 2, y))
        d.rectangle([x, y + H, x + W, y + H + 22], fill="black")
        d.text((x + 6, y + H + 5), f"{i+1}  {p.get('iso_639_1') or '--'}  {p.get('width')}x{p.get('height')}", fill="white")
        lines.append(f"{i+1}\t{p['file_path']}\t{p.get('iso_639_1') or '--'}\t{p.get('width')}x{p.get('height')}\tvotes={p.get('vote_count',0)}")
    os.makedirs("_poster_candidates", exist_ok=True)
    sheet.save(f"_poster_candidates/{slug}.jpg", quality=80)
    open(f"_poster_candidates/{slug}.txt", "w").write("\n".join(lines) + "\n")
    print(f"sheet {slug}: {len(lines)} candidates written to _poster_candidates/{slug}.jpg")

def _gray_rows(im, w=96):
    g = im.convert("L"); h = max(1, round(w * g.height / g.width)); g = g.resize((w, h), Image.LANCZOS)
    return [list(g.crop((0, y, w, y + 1)).tobytes()) for y in range(h)]

def _corr(A, B, dx, dy):
    import math
    ha, wa = len(A), len(A[0]); hb, wb = len(B), len(B[0])
    xs = range(max(0, dx), min(wa, wb + dx)); ys = range(max(0, dy), min(ha, hb + dy))
    if len(xs) < wa * 0.5 or len(ys) < ha * 0.5: return 0.0
    a = [A[y][x] for y in ys for x in xs]; b = [B[y - dy][x - dx] for y in ys for x in xs]
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    den = math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b)) or 1.0
    return num / den

def looks_same(im1, im2, threshold=0.6):
    """True when im2 is the same picture as im1 at another crop or scale:
    slide a downscaled im2 over im1 and take the best normalized correlation."""
    A = _gray_rows(im1)
    for sc in (0.85, 1.0, 1.18):
        B = _gray_rows(im2, w=round(96 * sc))
        for dx in range(-30, 31, 6):
            for dy in range(-20, 21, 5):
                if _corr(A, B, dx, dy) > threshold: return True
    return False

def tmdb_image(file_path, size="w342"):
    return Image.open(io.BytesIO(get(f"https://image.tmdb.org/t/p/{size}{file_path}"))).convert("RGB")

def all_posters(movie_id):
    imgs = api(f"/movie/{movie_id}/images")
    posters = imgs.get("posters") or []
    posters.sort(key=lambda p: (p.get("vote_count", 0), p.get("vote_average", 0), p.get("width", 0)), reverse=True)
    return posters

def match_supplied(current_path, posters, current_width):
    """Find the same design as the supplied poster among TMDB's, at a higher
    resolution. Returns the TMDB file_path or None."""
    try: cur = Image.open(current_path).convert("RGB")
    except Exception: return None
    for p in posters[:24]:
        if p.get("width", 0) <= current_width: continue
        try: cand = tmdb_image(p["file_path"])
        except Exception: continue
        if looks_same(cur, cand, threshold=0.7):
            return p["file_path"]
    return None

def variants(slug, movie, path, main_img, posters):
    """Up to five other distinct posters, saved beside the main one; the post
    gains a posters: list."""
    chosen, imgs = [], [main_img] if main_img is not None else []
    for old in glob.glob(f"assets/img/posters/{slug}-alt-*.jpg"): os.remove(old)
    for p in posters:
        if len(chosen) == 5: break
        if p.get("width", 0) < 500: continue
        try: thumb = tmdb_image(p["file_path"])
        except Exception: continue
        if any(looks_same(prev, thumb, threshold=0.6) for prev in imgs): continue
        try: full = tmdb_image(p["file_path"], "original")
        except Exception: continue
        w = min(700, full.width); full = full.resize((w, round(w * full.height / full.width)), Image.LANCZOS)
        out = f"assets/img/posters/{slug}-alt-{len(chosen)+1}.jpg"
        full.save(out, quality=82, optimize=True, progressive=True)
        chosen.append("/" + out); imgs.append(thumb)
    text = open(path, encoding="utf-8").read(); fm, _ = front_matter(text)
    if chosen:
        text, fm = set_field(text, fm, "posters", "[" + ", ".join(chosen) + "]")
    elif re.search(r"^posters:", fm, re.M):
        text = re.sub(r"^posters:.*\n", "", text, count=1, flags=re.M)
    open(path, "w", encoding="utf-8").write(text)
    print(f"alts  {slug}: {len(chosen)}")
    return bool(chosen)

def set_field(text, fm, name, value):
    """Add or replace a front-matter line; returns (new text, new fm)."""
    if re.search(rf"^{name}:", fm, re.M):
        fm2 = re.sub(rf"^{name}:.*$", f"{name}: {value}", fm, count=1, flags=re.M)
    else:
        fm2 = fm + f"\n{name}: {value}"
    return "---\n" + fm2 + "\n---\n" + text.split("\n---\n", 1)[1], fm2

def extras(slug, movie, path):
    """Stills (up to 4 TMDB backdrops) and the IMDb id, added to the post."""
    text = open(path, encoding="utf-8").read()
    fm, _ = front_matter(text)
    changed_here = False
    if not field(fm, "imdb"):
        try:
            det = api(f"/movie/{movie['id']}")
            if det.get("imdb_id"):
                text, fm = set_field(text, fm, "imdb", det["imdb_id"]); changed_here = True
        except Exception as e:
            print(f"  imdb {slug}: {e}")
    if RESTILLS or not re.search(r"^stills:", fm, re.M):
        try:
            bds = (api(f"/movie/{movie['id']}/images").get("backdrops") or [])
            bds.sort(key=lambda b: (b.get("vote_count", 0), b.get("vote_average", 0)), reverse=True)
            paths, seen = [], []
            os.makedirs("assets/img/stills", exist_ok=True)
            for old in glob.glob(f"assets/img/stills/{slug}-*.jpg"): os.remove(old)
            for b in bds[:10]:
                if len(paths) == 4: break
                im = Image.open(io.BytesIO(get(IMG + b["file_path"]))).convert("RGB")
                # skip the same picture at another crop or scale
                if any(looks_same(prev, im) for prev in seen): continue
                seen.append(im)
                w = min(1280, im.width)
                im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
                out = f"assets/img/stills/{slug}-{len(paths)+1}.jpg"
                im.save(out, quality=82, optimize=True, progressive=True)
                paths.append("/" + out)
            if paths:
                text, fm = set_field(text, fm, "stills", "[" + ", ".join(paths) + "]"); changed_here = True
                print(f"stills {slug}: {len(paths)}")
        except Exception as e:
            print(f"  stills {slug}: {e}")
    if changed_here:
        open(path, "w", encoding="utf-8").write(text)
    return changed_here

changed = []
for path in sorted(glob.glob("_posts/*.md")):
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(path))[:-3]
    if ONLY and slug not in ONLY: continue
    text = open(path, encoding="utf-8").read()
    fm, end = front_matter(text)
    if fm is None: continue
    title, year = field(fm, "title"), field(fm, "year")
    poster = field(fm, "poster")
    dest = f"assets/img/posters/{slug}.jpg"
    current = poster.lstrip("/") if poster else dest
    width = 0
    if os.path.exists(current):
        try: width = Image.open(current).size[0]
        except Exception: width = 0
    # A square or landscape image is a stand-in (album cover, quad), not a poster.
    ratio = 1.0
    if width:
        try: w0, h0 = Image.open(current).size; ratio = w0 / h0
        except Exception: ratio = 1.0
    pinned = field(fm, "tmdb_poster")
    need_extras = RESTILLS or not field(fm, "imdb") or not re.search(r"^stills:", fm, re.M) or not re.search(r"^posters:", fm, re.M) or not pinned
    if width >= MIN_WIDTH and ratio < 0.8 and not FORCE and not pinned and not CANDIDATES and not need_extras:
        print(f"skip  {slug}: already {width}px wide"); continue
    skip_poster = width >= MIN_WIDTH and ratio < 0.8 and not FORCE and not pinned

    try:
        tmdb_id = field(fm, "tmdb")
        if tmdb_id:
            movie = api(f"/movie/{tmdb_id}")
        else:
            res = api("/search/movie", query=title, year=year or "")
            hits = res.get("results") or []
            if not hits and year:
                hits = (api("/search/movie", query=title).get("results") or [])
            if not hits:
                print(f"none  {slug}: no TMDB match for {title!r} {year}. Add a `tmdb:` id to the post."); continue
            movie = hits[0]
        if CANDIDATES:
            candidate_sheet(slug, movie); continue
        if extras(slug, movie, path): changed.append(slug + " (extras)")
        posters_all = all_posters(movie["id"])
        text = open(path, encoding="utf-8").read(); fm, end = front_matter(text)
        # A supplied poster (no pin): look for the same design in higher resolution.
        fp = pinned
        if not fp and width and ratio < 0.8:
            hit = match_supplied(current, posters_all, width)
            if hit:
                fp = hit; skip_poster = False
                print(f"match {slug}: TMDB has the supplied design at higher resolution")
        if skip_poster and not fp:
            print(f"skip  {slug}: poster already {width}px wide")
            main_img = Image.open(current).convert("RGB") if os.path.exists(current) else None
            if RESTILLS or not re.search(r"^posters:", fm, re.M):
                if variants(slug, movie, path, main_img, posters_all): changed.append(slug + " (variants)")
            continue
        fp = fp or best_poster(movie["id"])
        if not fp:
            print(f"none  {slug}: TMDB has no poster for {movie.get('title')}"); continue
        raw = get(IMG + fp)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width <= width and ratio < 0.8 and not FORCE and not pinned:
            print(f"skip  {slug}: TMDB poster ({im.width}px) is no wider than current ({width}px)"); continue
        w = min(900, im.width)
        im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im.save(dest, quality=84, optimize=True, progressive=True)
        text = open(path, encoding="utf-8").read(); fm, end = front_matter(text)
        if not poster:
            text, fm = set_field(text, fm, "poster", "/" + dest)
        elif poster.lstrip("/") != dest:
            text = text.replace(poster, "/" + dest, 1); fm, _ = front_matter(text)
        # Pin what was fetched so later runs are stable and know it came from TMDB.
        text, fm = set_field(text, fm, "tmdb_poster", fp)
        open(path, "w", encoding="utf-8").write(text)
        print(f"fetch {slug}: {movie.get('title')} ({movie.get('release_date','')[:4]}) -> {w}px wide")
        changed.append(slug)
        if variants(slug, movie, path, im, posters_all): changed.append(slug + " (variants)")
    except Exception as e:
        print(f"error {slug}: {e}")

print(f"\n{len(changed)} poster(s) updated: {', '.join(changed) or 'none'}")
