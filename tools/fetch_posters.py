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
    if not re.search(r"^stills:", fm, re.M):
        try:
            bds = (api(f"/movie/{movie['id']}/images").get("backdrops") or [])
            bds.sort(key=lambda b: (b.get("vote_count", 0), b.get("vote_average", 0)), reverse=True)
            paths = []
            os.makedirs("assets/img/stills", exist_ok=True)
            for i, b in enumerate(bds[:4]):
                im = Image.open(io.BytesIO(get(IMG + b["file_path"]))).convert("RGB")
                w = min(1280, im.width)
                im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
                out = f"assets/img/stills/{slug}-{i+1}.jpg"
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
    need_extras = not field(fm, "imdb") or not re.search(r"^stills:", fm, re.M)
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
        if skip_poster:
            print(f"skip  {slug}: poster already {width}px wide"); continue
        text = open(path, encoding="utf-8").read(); fm, end = front_matter(text)
        fp = pinned or best_poster(movie["id"])
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
        if not poster:
            fm2 = fm + f"\nposter: /{dest}"
            text = "---\n" + fm2 + "\n---\n" + text[end:]
            open(path, "w", encoding="utf-8").write(text)
        elif poster.lstrip("/") != dest:
            text = text.replace(poster, "/" + dest, 1)
            open(path, "w", encoding="utf-8").write(text)
        print(f"fetch {slug}: {movie.get('title')} ({movie.get('release_date','')[:4]}) -> {w}px wide")
        changed.append(slug)
    except Exception as e:
        print(f"error {slug}: {e}")

print(f"\n{len(changed)} poster(s) updated: {', '.join(changed) or 'none'}")
