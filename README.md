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

## Turning on the newsletter (Buttondown, free to 100 subscribers)

1. Sign up at https://buttondown.com and pick a username.
2. Put it in `buttondown_username` in `_config.yml`. Commit.
3. A sign-up box appears above the footer on every page. New subscribers land in
   Buttondown; write and send from there.

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
