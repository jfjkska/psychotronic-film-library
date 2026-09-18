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
    if width >= MIN_WIDTH and not FORCE:
        print(f"skip  {slug}: already {width}px wide"); continue

    try:
        res = api("/search/movie", query=title, year=year or "")
        hits = res.get("results") or []
        if not hits and year:
            hits = (api("/search/movie", query=title).get("results") or [])
        if not hits:
            print(f"none  {slug}: no TMDB match for {title!r} {year}"); continue
        movie = hits[0]
        fp = best_poster(movie["id"])
        if not fp:
            print(f"none  {slug}: TMDB has no poster for {movie.get('title')}"); continue
        raw = get(IMG + fp)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width <= width and not FORCE:
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
        print(f"fetch {slug}: {movie.get('title')} ({movie.get('release_date','')[:4]}) -> {w}px from {im.width}px")
        changed.append(slug)
    except Exception as e:
        print(f"error {slug}: {e}")

print(f"\n{len(changed)} poster(s) updated: {', '.join(changed) or 'none'}")
