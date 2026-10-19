# Connections draft

The page remains unlinked and marked noindex. Local edits do not publish it.

## Rebuild after adding a review

Install PyYAML in your Python environment, then run:

```sh
python tools/make_connections.py
python tools/make_connections.py --check
node tools/test_connections.cjs
```

The generator reads all published review front matter. It refreshes the counts,
shared-credit graph and career lines. Commit the generated
`connections/index.html` alongside its sources when publication is requested.

For a local preview, use `--preview PATH` to write plain HTML without Jekyll
front matter. Serve it at `/connections/` with the repository's `/assets/`
available. For example, the existing local preview server can serve:

```sh
python tools/make_connections.py --preview _site/preview/connections/index.html
```

## Source ownership

- `tools/connections_template.html`: semantic page structure.
- `assets/css/connections.css`: responsive visual design.
- `assets/js/connections.js`: interaction and rendering.
- `assets/js/connections-core.js`: pure graph operations.
- `tools/make_connections.py`: review parsing, explicit name aliases, validation.
- `tools/connections_research.json`: new sourced outside links, research cards and
  editorial double bills.
- `tools/connections_data.py`: earlier outside shelf, clubs, comparison notes
  and aliases. Earlier unsourced entries are labelled Library research notes.

Add a source URL and precise per-film explanation for new outside connections.
Outside titles are separate graph nodes; a title now reviewed in the library
is removed from that outside shelf automatically. It must get its film-to-film
connections from the review credits or explicit supplemental research.
Keep a band and its members distinct, and keep all roles for a person.
Do not turn shared themes, family relationships or speculative influence into
shared-credit edges. Release years and incomplete credit lists follow the reviews.

For DOM integration checks, pass an installed jsdom path to `node tools/test_connections_ui.cjs PATH_TO_JSDOM`. The existing local tooling has it at `_site/tooling/js/node_modules/jsdom`.

## October 2026 refresh

86 reviews, 107 shared-credit pairs, 48 recurring credits, 33 outside detours.
Four newly sourced detours: THX 1138, Joe Kidd, Black Christmas and Escape from
New York. Eight research cards and eight editorial double bills. New
methodologies include exhibition context, reused footage, intended audience,
known aliases, role-filtered neighbourhoods and deterministic shortest routes.

The page loads local fonts and existing poster images. No graph CDN or
third-party JavaScript is needed. Review pages and the public header are
unchanged. Older research is retained as notes; it has not all been independently
re-sourced during this refresh.
