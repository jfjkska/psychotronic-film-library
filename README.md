# Psychotronic Film Library

A Jekyll blog of exploitation, giallo and eurosleaze film reviews, built to run on
GitHub Pages for free with no build tooling on your side.

- Posting a review: see [HOW-TO-POST.md](HOW-TO-POST.md).
- Design: a psychedelic grindhouse look cut from the banner in `assets/img/banner.jpg`.
  All colour and type lives in `assets/css/library.css`.

## Hosting on GitHub Pages (free)

1. Create a repository on GitHub, e.g. `psychotronic-film-library`, and push these files
   to its `main` branch (they must sit at the repo root, not in a subfolder).
2. In the repo go to **Settings → Pages**. Under *Build and deployment* pick
   **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
3. About a minute later the site is at `https://<username>.github.io/psychotronic-film-library/`.

`_config.yml` has `baseurl: "/psychotronic-film-library"` to match that address. If the
repo is named differently, change `baseurl` to `/<repo-name>`.

## Posters fetched automatically (TMDB, free)

`.github/workflows/posters.yml` looks every review up on The Movie Database and
downloads the best poster whenever the one in the repo is small or missing. It
runs when a review is added and can be run by hand from the **Actions** tab
(with a "force" option to replace everything).

One-time setup: make a free account at https://www.themoviedb.org, then under
**Settings → API** request a key (choose "Developer", fill the form with the site's
name and address). Copy the **API Key (v3 auth)** and add it on this repo under
**Settings → Secrets and variables → Actions → New repository secret**, named
`TMDB_API_KEY`. Then run the workflow once from the Actions tab.

If it picks the wrong poster (a modern Blu-ray cover, say), run the workflow with
**candidates** ticked and the review's slug in **only**. It commits a numbered sheet
to `_poster_candidates/<slug>.jpg` with the TMDB paths in the `.txt` beside it. Put
the chosen path on a `tmdb_poster:` line in the review and run the fetch again.

For archive films with no reliable TMDB entry, add `fetch_posters: false` to
the review's front matter. This skips automatic poster, gallery and credit
lookups for that review, preserving its supplied assets; share cards still run.

## Wiring the contact form (2 minutes, free)

GitHub Pages can't process a form on its own, so the form posts to Formspree.

1. Sign up at https://formspree.io with the address that should receive messages.
2. Click **New form**, name it, and copy the endpoint it gives you
   (it looks like `https://formspree.io/f/abcdwxyz`).
3. In `_config.yml` replace `YOUR_FORM_ID` in `contact_form_endpoint` with that. Commit.

The free plan takes 50 messages a month, which is plenty. The form has a hidden
spam-trap field that Formspree honours.

## Turning on comments (giscus, free)

Comments live in GitHub Discussions on this repo, so nothing else to host.

1. On the repo: **Settings → General → Features**, tick **Discussions**.
2. Install the giscus app on the repo: https://github.com/apps/giscus
3. Go to https://giscus.app, enter the repo, choose the Discussion category
   (make one called "Reviews" first, type Announcements), mapping **pathname**.
4. It shows a snippet with `data-repo`, `data-repo-id`, `data-category` and
   `data-category-id`. Copy those four values into the `giscus:` block in `_config.yml`.
   Commit. The comments box appears at the foot of every review, in the site's colours.

## Following new reviews

Readers can subscribe by email on `/updates/` or beneath any review. The form
posts directly to follow.it, which delivers new reviews from the site's RSS feed
and handles confirmation and unsubscribe. Its endpoint and public subscription
link are set in `_config.yml` as `followit_form_action` and `followit_url`.
No subscriber addresses are stored in this repository.

Readers can also follow `https://psychotronicfilmlibrary.com/feed.xml` in an RSS
reader without an email signup; `/updates/` retains the feed link.

## Review search metadata

Review pages automatically use `Film Title (year) review | Psychotronic Film
Library` as their browser/search title. The visible film title and URL stay the
same. A short `description:` can override the excerpt for search and sharing;
otherwise the excerpt is used, with HTML removed and a 180-character limit.

`_includes/review-seo.html` supplies canonical URLs, social cards and one complete
Review JSON-LD record identifying the Movie, author, publication date and visible
1–5 eye rating. A rating of 0 means unrated and is omitted from structured data.
Only set `last_modified_at:` when a review is actually updated. Structured data
does not guarantee a particular search appearance.

## Visitor analytics

Cloudflare Web Analytics works with GitHub Pages without moving hosting or DNS.
In the Cloudflare dashboard, add `psychotronicfilmlibrary.com` under Web Analytics
and copy the public `token` value from the installation snippet into
`cloudflare_web_analytics_token` in `_config.yml`. Do not paste an account API key.
Use manual snippet installation rather than also enabling automatic injection.

The beacon loads only in production builds with a non-empty token. Local
development stays untracked. After publishing, visit a review and confirm that
the dashboard receives its page view. Counts start when tracking is activated;
blocked scripts and visitors without JavaScript will not be counted.

## Checking browsing and gallery changes

Build the site with Jekyll, then run `node tools/test_library.cjs <build-folder> <jsdom-module-path>`.
Run `node tools/test_review_seo.cjs <build-folder> <jsdom-module-path>` to check
review metadata, JSON-LD and parity between visible and structured ratings.
This exercises search by alternative title/cast, combined filters, country
co-productions, sorting, shared search URLs, gallery navigation, focus restoration,
swipes, recommendations and viewing links. Also check desktop and mobile in a
browser, including Escape and the native modal focus behaviour.

The `Check site` workflow builds with the production Jekyll version and runs these
interaction checks on feature branches and pull requests, without publishing.

## Adding your own domain later

1. Buy the domain, then in **Settings → Pages → Custom domain** enter it and save.
   GitHub creates a `CNAME` file in the repo.
2. At the registrar add the DNS records GitHub shows you (four `A` records for the apex
   plus a `CNAME` for `www`).
3. In `_config.yml` set `url: "https://yourdomain.com"` and `baseurl: ""`. Commit.
4. Tick **Enforce HTTPS** once the certificate appears.

## Previewing on your own machine (optional)

Needs Ruby. Then:

```
bundle install
bundle exec jekyll serve
```

and open http://localhost:4000/psychotronic-film-library/.
