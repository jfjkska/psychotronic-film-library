# How to post a review

You never touch code. One file per film, and the site rebuilds itself in about a minute.

## 1. Add the poster (optional)

Put a JPEG in `assets/img/posters/`. Name it something simple, all lowercase, dashes
for spaces: `emanuelle-e-francoise.jpg`. Around 900 pixels wide is plenty.

On GitHub: open the folder, **Add file → Upload files**, drag it in, **Commit changes**.

## 2. Write the review

Copy `_template/review-template.md` into `_posts/` and name it with today's date
followed by the film title:

```
_posts/2026-09-18-emanuelle-e-francoise.md
```

On GitHub: open `_posts/`, **Add file → Create new file**, type the name, paste the
template in, fill it out, **Commit changes**.

The block between the two `---` lines is the film's credits. Fill in what you know and
delete any line you don't want. The review goes underneath, as plain paragraphs.

Genres are free text. Whatever you type becomes a filter button on the front page and
a section on The Shelf, so spell them the same way each time (`giallo`, not `Giallo`
one week and `gialli` the next).

Rating is 0 to 5. It shows as eyes. 0 hides it, for when you can't decide.

## Trailer and score

Find the video on YouTube and copy the id from its address: in
`https://www.youtube.com/watch?v=dQw4w9WgXcQ` the id is `dQw4w9WgXcQ`. Put it on the
`trailer:` line. Score tracks go under `tracks:`, one `title` and `youtube` pair each.
Delete the lines you don't use. The page shows a thumbnail with a play button, and the
video only loads from YouTube when a reader presses it.

## Version seen

A `version:` line for the cut or copy you watched: "88 Films Blu-ray, uncut", "a worn
ex-rental VHS", "the BBFC-cut TV print". Shows in the credits block.

## Stills, links and share cards

These arrive by themselves within a minute or two of posting: four stills under the
review, IMDb and Letterboxd links in the credits, and a share card so the link looks
right when pasted into WhatsApp or X. Nothing to do.

## Where to watch

Under `watch:` list the disc label or streaming home, one `label` per line with an
optional `url`. It shows in the credits block. Delete the lines if you don't know.

## The front-page "In the pile" strip

Open `_config.yml` and edit the lines under `next_up:`. One film per line, in quotes.
Delete them all to hide the strip.

## 3. Wait a minute

GitHub rebuilds the site on every commit. If the page doesn't change, hard-refresh
(Ctrl+Shift+R). If it still doesn't, check the **Actions** tab on the repo for a red
cross and read the error, which is nearly always a missing quote mark in the credits.

## Fixing a review

Open the file in `_posts/`, click the pencil, edit, commit. Same for deleting: the
bin icon on the file page.
