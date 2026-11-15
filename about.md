---
layout: page
title: About the library
permalink: /about/
description: >-
  Psychotronic Film Library is Darren Evanson's collection of reviews of
  obscure exploitation, giallo, eurosleaze, horror and cult films, each rated
  out of five eyes.
---
{%- assign films = site.posts -%}
{%- assign years = films | map: "year" | compact | sort -%}
{%- assign lib = site.data.library_pages -%}

**Psychotronic Film Library** is a collection of film reviews by Darren Evanson:
{{ films | size }} reviews so far, of films made between {{ years | first }} and {{ years | last }}.

{% comment %}
  ── AUTHOR GAP: about Darren ─────────────────────────────────────────────
  Two or three sentences in your own words: who you are, how you got into
  these films, what you look for in them. Nothing here has been written
  for you on purpose. Some of your reviews already mention late-night TV
  in the early 1980s, worn VHS tapes and second features at the local
  Ritz, if any of that belongs here. Delete this comment when done.
  ─────────────────────────────────────────────────────────────────────────
{% endcomment %}

## What's on the shelf

Horror, exploitation, giallo, eurosleaze, European cult cinema and British sex
comedies: the obscure, strange and psychotronic corners of cinema.
Most of the films come from {% if lib.country.Italy %}[Italy]({{ lib.country.Italy | relative_url }}){% else %}Italy{% endif %},
{% if lib.country.UK %}[the UK]({{ lib.country.UK | relative_url }}){% else %}the UK{% endif %} and
{% if lib.country.USA %}[the USA]({{ lib.country.USA | relative_url }}){% else %}the USA{% endif %}, with plenty
from Spain, France and West Germany.
{% if lib.decade.size > 0 %}Browse them by decade ({% assign decades = lib.decade | sort %}{% for d in decades %}<a href="{{ d[1] | relative_url }}">{{ d[0] }}</a>{% unless forloop.last %}, {% endunless %}{% endfor %}), by [director]({{ '/directors/' | relative_url }}), or on the [Browse]({{ '/shelf/' | relative_url }}) page.{% endif %}

Each review comes with the film's credits, where it can be watched in the UK
(the disc or streaming service, and a UK availability guide), the trailer and
picks from the score where they can be found, and a gallery of alternative
posters and stills.

## How the rating works

Every review is rated out of five eyes:
{% include rating.html rating=4 %} is four out of five. A short verdict
stamped on the poster sums the film up in a few words. A film can be left
unrated, in which case no eyes are shown.

{% comment %}
  ── AUTHOR GAP: what the eyes mean ──────────────────────────────────────
  Optional. One line per score, in your words, e.g. what separates three
  eyes from four. The site doesn't define the levels anywhere yet, so
  nothing has been made up. Delete this comment when done.
  ─────────────────────────────────────────────────────────────────────────
{% endcomment %}

{%- assign five = films | where: "rating", 5 | size -%}
{%- assign four = films | where: "rating", 4 | size -%}
{%- assign three = films | where: "rating", 3 | size -%}
{%- assign two = films | where: "rating", 2 | size -%}
{%- assign one = films | where: "rating", 1 | size %}

So far: {{ five }} with five eyes, {{ four }} with four, {{ three }} with three,
{{ two }} with two and {{ one }} with one. The four- and five-eye films are
collected in [Darren’s picks]({{ '/top-shelf/' | relative_url }}).

## Who runs it

Library Director: Darren Evanson

Library Manager: Phil Fisher

## Posters, stills and corrections

Posters and stills belong to their studios and distributors and are shown here for
review and comment. If you own one and would rather it was not here, [get in touch]({{ '/contact/' | relative_url }})
and it will come down. The same goes for corrections, a better poster scan or a
film that deserves a review.

Many posters and stills are found through [The Movie Database (TMDB)](https://www.themoviedb.org/).
This site uses the TMDB API but is not endorsed or certified by TMDB.

## Following new reviews

Get new reviews by [email]({{ '/updates/' | relative_url }}) or subscribe to the
[RSS feed]({{ '/feed.xml' | relative_url }}).
