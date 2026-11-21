// Check rendered output, including duplicate metadata and visible-rating parity.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require(path.resolve(process.argv[3] || '_site/tooling/js/node_modules/jsdom'));
const build = path.resolve(process.argv[2] || '_site');
const reviews = fs.readdirSync(path.join(build, 'reviews'), { withFileTypes: true }).filter(d => d.isDirectory());
assert(reviews.length > 0, 'No review pages found');
for (const entry of reviews) {
  const document = new JSDOM(fs.readFileSync(path.join(build, 'reviews', entry.name, 'index.html'), 'utf8')).window.document;
  const one = selector => {
    const matches = document.querySelectorAll(selector);
    assert.equal(matches.length, 1, `${entry.name}: expected one ${selector}`);
    return matches[0];
  };
  const name = one('h1').textContent.trim();
  const year = document.querySelector('.strap-year')?.textContent.trim();
  const title = `${name}${year ? ` (${year})` : ''} review`;
  assert.equal(one('title').textContent, `${title} | Psychotronic Film Library`);
  const description = one('meta[name="description"]').content;
  assert(description.length > 0 && description.length <= 180, `${entry.name}: description length`);
  const canonical = one('link[rel="canonical"]').href;
  assert.equal(new URL(canonical).pathname, `/reviews/${entry.name}/`);
  assert.equal(one('meta[property="og:title"]').content, title);
  assert.equal(one('meta[property="og:description"]').content, description);
  assert.equal(one('meta[property="og:url"]').content, canonical);
  assert.equal(one('meta[name="twitter:title"]').content, title);
  assert.equal(one('meta[name="twitter:description"]').content, description);
  assert.equal(one('meta[name="twitter:card"]').content, 'summary_large_image');
  assert.match(one('meta[property="og:image"]').content, /^https:\/\//);
  const records = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => JSON.parse(s.textContent));
  assert.equal(records.length, 2, `${entry.name}: expected Review and BreadcrumbList JSON-LD`);
  const schema = records.find(r => r['@type'] === 'Review');
  const crumbs = records.find(r => r['@type'] === 'BreadcrumbList');
  assert(schema && crumbs, `${entry.name}: Review and BreadcrumbList present`);
  assert.deepEqual(crumbs.itemListElement.map(i => i.position), [1, 2, 3]);
  assert.equal(crumbs.itemListElement[2].item, canonical);
  assert.equal(crumbs.itemListElement[2].name, name);
  assert.match(schema.publisher.logo.url, /^https:\/\/.+\.png$/);
  const credit = label => {
    const dt = [...document.querySelectorAll('.credits dt')].find(d => d.textContent.trim() === label);
    return dt ? dt.nextElementSibling.textContent.trim() : null;
  };
  const list = text => text.split(/\s*,\s*/).map(s => s.replace(/^performed by /, '').trim()).filter(Boolean);
  const movie = schema.itemReviewed;
  const starring = credit('Starring');
  if (starring) assert.deepEqual(movie.actor.map(a => a.name), list(starring), `${entry.name}: actors match credits`);
  else assert.equal(movie.actor, undefined);
  const music = credit('Music');
  if (music) assert.deepEqual(movie.musicBy.map(a => a.name), list(music), `${entry.name}: music matches credits`);
  else assert.equal(movie.musicBy, undefined);
  const runtime = credit('Runtime');
  if (runtime && /^\d+ min$/.test(runtime)) assert.equal(movie.duration, `PT${parseInt(runtime, 10)}M`, `${entry.name}: duration`);
  else assert.equal(movie.duration, undefined);
  const country = [...document.querySelectorAll('.strap')].map(s => s.textContent)[0];
  if (movie.countryOfOrigin) {
    assert(movie.countryOfOrigin.length > 0 && movie.countryOfOrigin.every(c => c['@type'] === 'Country' && c.name && country.includes(c.name)), `${entry.name}: countries`);
  }
  assert.equal(schema['@type'], 'Review');
  assert.equal(schema.url, canonical);
  assert.equal(schema.description, description);
  assert.equal(schema.itemReviewed['@type'], 'Movie');
  assert.equal(schema.itemReviewed.name, name);
  if (year) assert.equal(schema.itemReviewed.dateCreated, year);
  assert.match(schema.itemReviewed.image, /^https:\/\//);
  assert.equal(schema.author['@type'], 'Person');
  assert(schema.author.name.length > 0);
  assert.equal(schema.publisher.name, 'Psychotronic Film Library');
  assert(Number.isFinite(Date.parse(schema.datePublished)), `${entry.name}: publication date`);
  const visibleRating = document.querySelector('.credits .eyes');
  if (visibleRating) {
    assert.equal(schema.reviewRating.ratingValue, Number(visibleRating.getAttribute('aria-label').split(' ')[0]));
    assert.equal(schema.reviewRating.bestRating, 5);
    assert.equal(schema.reviewRating.worstRating, 1);
  } else {
    assert.equal(schema.reviewRating, undefined, `${entry.name}: hidden rating must not be marked up`);
  }
  assert.equal(document.querySelectorAll('[itemtype="https://schema.org/Review"]').length, 0, 'No incomplete duplicate Review microdata');
}
console.log(`PASS: SEO metadata, film identity, JSON-LD and visible rating parity for ${reviews.length} reviews.`);
