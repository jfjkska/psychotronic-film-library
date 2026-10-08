#!/usr/bin/env python3
"""Build the connections report: every link between the films in the library.

Shared credits (director, starring, music) come straight from the reviews' front
matter. The deep cuts (films outside the library that tie two reviews together,
clubs, themes, cash-ins) live in tools/connections_data.py; add to them there.

    python3 tools/make_connections.py              # writes connections/index.html
    python3 tools/make_connections.py --body PATH  # also writes the page without
                                                   # its <html>/<head> wrapper

Needs PyYAML and Pillow. Poster thumbnails are embedded, so the page stands alone.
"""
import base64, collections, glob, io, itertools, json, os, re, sys
import yaml
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import connections_data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "connections", "index.html")
SITE = "https://psychotronicfilmlibrary.com"
TEMPLATE = os.path.join(os.path.dirname(__file__), "connections_template.html")


def names(s):
    s = re.sub(r"\(.*?\)", "", str(s or "")).replace("performed by ", "")
    return [x.strip() for x in re.split(r",| and ", s) if x.strip()]


def thumb(path):
    p = os.path.join(ROOT, (path or "").lstrip("/"))
    if not path or not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGB")
    w, h = im.size
    side = min(w, h)
    top = int((h - side) * 0.18)  # faces and titles sit high on a poster
    im = im.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side)).resize((96, 96), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=70, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def load_films():
    films = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "_posts", "*.md"))):
        fm = yaml.safe_load(open(f, encoding="utf-8").read().split("---")[1])
        slug = re.sub(r"^\d{4}-\d\d-\d\d-", "", os.path.basename(f)[:-3])
        films[slug] = {
            "id": slug,
            "t": fm.get("title", slug),
            "y": int(fm.get("year") or 0),
            "d": re.sub(r"\s*\(as .*?\)", "", fm.get("director", "")),
            "c": str(fm.get("country", "")),
            "r": int(fm.get("rating") or 0),
            "img": thumb(fm.get("poster")),
            "url": SITE + "/reviews/" + slug + "/",
            "_credits": {k: names(fm.get(k)) for k in ("director", "starring", "music")},
        }
    return films


def build():
    films = load_films()
    role = {"director": "directed", "starring": "acted", "music": "scored"}
    people = collections.defaultdict(dict)  # name -> {slug: role}
    for s, f in films.items():
        for k, ns in f.pop("_credits").items():
            for n in ns:
                people[n][s] = role[k]

    # Direct film-to-film links, one per pair, listing everyone they share.
    pair = collections.defaultdict(list)
    for n, fs in people.items():
        for a, b in itertools.combinations(sorted(fs), 2):
            pair[(a, b)].append(n)
    for a, b, via in D.DIRECT:
        pair[tuple(sorted((a, b)))].append(via)
    direct = [{"a": a, "b": b, "via": v} for (a, b), v in sorted(pair.items())]

    # Repertory: everyone credited on 2+ films, plus the uncredited writer.
    rep = [{"n": n, "films": fs} for n, fs in people.items() if len(fs) > 1]
    rep.append({"n": "David McGillivray", "films": {s: "wrote" for s in
                ("house-of-whipcord", "frightmare", "house-of-mortal-sin", "schizo", "satans-slave")}})
    rep.append({"n": "Candace Glendenning", "films": {"the-flesh-and-blood-show": "acted", "satans-slave": "acted"}})
    rep.sort(key=lambda p: (-len(p["films"]), min(films[s]["y"] for s in p["films"])))

    for group in (D.HUBS, D.CLUBS, D.THEMES):
        for h in group:
            missing = [s for s in h["films"] if s not in films]
            if missing:
                sys.exit(f"{h['id']}: no review for {missing}")

    return {
        "films": list(films.values()),
        "direct": direct,
        "hubs": D.HUBS, "clubs": D.CLUBS, "themes": D.THEMES,
        "rep": rep,
        "lineage": [dict(zip(("src", "sy", "film", "note", "dir"), l)) for l in D.LINEAGE],
        "clashes": [dict(zip(("title", "films", "note"), c)) for c in D.TITLE_CLASHES],
        "aliases": [dict(zip(("real", "as", "films"), p)) for p in D.PSEUDONYMS],
    }


def main():
    data = build()
    body = open(TEMPLATE, encoding="utf-8").read().replace(
        "/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    if "--body" in sys.argv:
        with open(sys.argv[sys.argv.index("--body") + 1], "w", encoding="utf-8") as fh:
            fh.write(body)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("---\nlayout: null\npermalink: /connections/\nsitemap: false\n---\n"
                 '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                 '<meta name="robots" content="noindex">\n</head>\n<body>\n'
                 "{% raw %}\n" + body + "\n{% endraw %}\n</body>\n</html>\n")
    print(f"{len(data['films'])} films, {len(data['direct'])} shared-credit links, "
          f"{len(data['hubs'])} outside films -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
