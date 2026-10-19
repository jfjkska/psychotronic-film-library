#!/usr/bin/env python3
"""Rebuild the Connections draft from every review plus curated research.

    python tools/make_connections.py
    python tools/make_connections.py --preview _site/preview/connections/index.html
    python tools/make_connections.py --check

Requires PyYAML. No network calls. Images and fonts use existing site assets.
"""
import argparse
import collections
import itertools
import json
from pathlib import Path
import re
import unicodedata
import yaml
import connections_data as D

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "connections/index.html"
ALIASES = {
    "anthony m. dawson": "Antonio Margheriti", "vincent dawn": "Bruno Mattei",
    "martin dolman": "Sergio Martino", "aristide massaccesi": "Joe D'Amato",
    "luigi montefiori": "George Eastman", "pierluigi conti": "Al Cliver",
    "luciano stella": "Tony Kendall", "annie brilland": "Annie Belle",
    "burt rexon": "Berto Pisano",
}

def key(value):
    value = str(value).replace("’", "'")
    return "".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c)).casefold().strip()

def names(value):
    if isinstance(value, list):
        return [n for item in value for n in names(item)]
    value = re.sub(r"\([^)]*\)", "", str(value or "")).replace("performed by ", "")
    return [ALIASES.get(key(n), n.strip()) for n in re.split(r",| and ", value) if n.strip()]

def load_films():
    films = {}
    for path in sorted((ROOT / "_posts").glob("*.md")):
        match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", path.read_text(encoding="utf-8-sig"), re.S)
        if not match:
            raise ValueError(f"Missing front matter: {path.name}")
        fm = yaml.safe_load(match[1])
        if fm.get("published") is False:
            continue
        slug = re.sub(r"^\d{4}-\d\d-\d\d-", "", path.stem)
        if slug in films:
            raise ValueError(f"Duplicate film: {slug}")
        poster = fm.get("poster") or ""
        if poster and not (ROOT / poster.lstrip("/")).is_file():
            raise ValueError(f"Missing poster: {poster}")
        films[slug] = dict(id=slug, t=fm.get("title", slug), y=int(fm.get("year") or 0),
            d=fm.get("director", ""), c=str(fm.get("country", "")), r=int(fm.get("rating") or 0),
            img=poster, url=f"/reviews/{slug}/", genres=fm.get("genres") or [],
            credits={role: names(fm.get(field)) for field, role in
                     (("director", "director"), ("starring", "cast"), ("music", "music"))})
    return films

def build():
    films = load_films()
    research = json.loads((ROOT / "tools/connections_research.json").read_text(encoding="utf-8"))
    people = {}
    for slug, film in films.items():
        for role, credits in film["credits"].items():
            for name in credits:
                person = people.setdefault(key(name), {"n": name, "films": {}})
                roles = person["films"].setdefault(slug, [])
                if role not in roles:
                    roles.append(role)
    # Existing supplemental research: keep these in the same credit model.
    for name, role, slugs in [
        ("David McGillivray", "writer", ["house-of-whipcord", "frightmare", "house-of-mortal-sin", "schizo", "satans-slave"]),
        ("Candace Glendenning", "cast", ["the-flesh-and-blood-show", "satans-slave"]),
    ]:
        person = people.setdefault(key(name), {"n": name, "films": {}})
        for slug in slugs:
            roles = person["films"].setdefault(slug, [])
            if role not in roles:
                roles.append(role)
    pairs = collections.defaultdict(list)
    rep = []
    for person in people.values():
        if len(person["films"]) < 2:
            continue
        rep.append(person)
        for a, b in itertools.combinations(sorted(person["films"]), 2):
            pairs[(a, b)].append({"n": person["n"], "a": person["films"][a], "b": person["films"][b]})
    rep.sort(key=lambda p: (-len(p["films"]), key(p["n"])))
    direct = [dict(a=a, b=b, via=sorted(v, key=lambda p: key(p["n"]))) for (a, b), v in sorted(pairs.items())]
    # A newly reviewed title graduates from the outside shelf into the film graph.
    hubs = [h for h in D.HUBS if h["id"] not in films] + research["hubs"]
    data = dict(films=list(films.values()), direct=direct, rep=rep, hubs=hubs,
        clubs=D.CLUBS, themes=D.THEMES, dossiers=research["dossiers"], bills=research["bills"],
        echoes=[dict(src=a, year=b, film=c, note=d) for a,b,c,d,_ in D.LINEAGE],
        clashes=[dict(title=a, films=b, note=c) for a,b,c in D.TITLE_CLASHES],
        aliases=[dict(real=a, alias=b, films=c) for a,b,c in D.PSEUDONYMS])
    validate(data)
    return data

def validate(data):
    ids = {f["id"] for f in data["films"]}
    hub_ids = [h["id"] for h in data["hubs"]]
    if len(hub_ids) != len(set(hub_ids)) or ids.intersection(hub_ids):
        raise ValueError("Duplicate or reviewed outside hub")
    for collection in ("hubs", "clubs", "themes", "dossiers", "bills", "aliases", "clashes"):
        for item in data[collection]:
            missing = set(item["films"]) - ids
            if missing:
                raise ValueError(f"{collection}: unknown films {missing}")
    for echo in data["echoes"]:
        if echo["film"] not in ids:
            raise ValueError(f"Unknown echo: {echo['film']}")
    for link in data["direct"]:
        if link["a"] == link["b"] or not {link["a"], link["b"]} <= ids:
            raise ValueError("Invalid shared-credit link")
    for hub in data["hubs"]:
        if len(hub["films"]) < 2:
            raise ValueError(f"Unconnected hub: {hub['id']}")

def render(data):
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    template = (ROOT / "tools/connections_template.html").read_text(encoding="utf-8")
    if template.count("/*__DATA__*/null") != 1:
        raise ValueError("Expected one data placeholder")
    return template.replace("/*__DATA__*/null", payload)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--body", type=Path, help="Legacy alias for --preview")
    args = parser.parse_args()
    data = build()
    page = render(data)
    generated = "---\nlayout: null\npermalink: /connections/\nsitemap: false\n---\n{% raw %}\n" + page + "\n{% endraw %}\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != generated:
            raise SystemExit("Connections is stale. Run python tools/make_connections.py")
    else:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(generated, encoding="utf-8", newline="\n")
    preview = args.preview or args.body
    if preview:
        preview.parent.mkdir(parents=True, exist_ok=True)
        preview.write_text(page, encoding="utf-8", newline="\n")
    print(f"{len(data['films'])} films; {len(data['direct'])} credit pairs; {len(data['rep'])} recurring credits; {len(data['hubs'])} detours. {'Current' if args.check else 'Built'}: {OUT}")

if __name__ == "__main__":
    main()
