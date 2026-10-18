// Integration checks against a Jekyll build. Pass the build folder and jsdom module path.
// Example: node tools/test_library.cjs _site/preview _site/tooling/js/node_modules/jsdom
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require(path.resolve(process.argv[3] || '_site/tooling/js/node_modules/jsdom'));
const build = path.resolve(process.argv[2] || '_site');
const script = fs.readFileSync(path.join(build, 'assets/js/library.js'), 'utf8');
function page(file, query = '') {
  const dom = new JSDOM(fs.readFileSync(path.join(build, file), 'utf8'), {
    url: 'https://psychotronicfilmlibrary.com/' + query, runScripts: 'outside-only', pretendToBeVisual: true
  });
  // jsdom does not implement native dialog methods. Browser tests cover the native modal.
  dom.window.HTMLDialogElement.prototype.showModal = function () { this.open = true; };
  dom.window.HTMLDialogElement.prototype.close = function () { this.open = false; this.dispatchEvent(new dom.window.Event('close')); };
  dom.window.eval(script);
  return dom;
}
function change(dom, selector, value, event = 'change') {
  const element = dom.window.document.querySelector(selector);
  element.value = value;
  element.dispatchEvent(new dom.window.Event(event, { bubbles: true }));
}
function visible(dom) { return [...dom.window.document.querySelectorAll('[data-rack] .card')].filter(c => !c.hidden); }
function titles(dom) { return visible(dom).map(c => c.dataset.title); }
function reset(dom) { dom.window.document.querySelector('[data-reset-finder]').click(); }

const home = page('index.html');
const total = visible(home).length;
assert(total >= 83);
change(home, '[data-genre-select]', 'giallo');
assert(visible(home).length > 0 && visible(home).every(c => c.dataset.genres.split('|').includes('giallo')), 'Genre dropdown filters reviews');
assert.equal(new URLSearchParams(home.window.location.search).get('genre'), 'giallo');
reset(home);
assert.equal(home.window.document.querySelector('[data-genre-select]').value, '');
const genreLink = page('index.html', '?genre=british+horror');
assert.equal(genreLink.window.document.querySelector('[data-genre-select]').value, 'british horror');
assert(visible(genreLink).length > 0 && visible(genreLink).every(c => c.dataset.genres.split('|').includes('british horror')), 'Genre links restore the dropdown and results');
genreLink.window.close();
change(home, '[data-finder-input]', 'Blood Camp Thatcher', 'input');
assert.deepEqual(titles(home), ['Turkey Shoot'], 'Alternative title search');
reset(home);
change(home, '[data-finder-input]', 'Dennis Hopper', 'input');
assert(titles(home).includes('Queen of Blood'), 'Cast search');
change(home, '[data-finder-input]', 'Queen of Blood', 'input');
change(home, '[data-decade]', '1960');
change(home, '[data-country]', 'USA');
change(home, '[data-rating]', '3');
assert.deepEqual(titles(home), ['Queen of Blood'], 'Combined filters');
change(home, '[data-decade]', '1970');
assert.equal(visible(home).length, 0);
assert.equal(home.window.document.querySelector('[data-empty]').hidden, false);
reset(home);
assert.equal(visible(home).length, total);
assert.equal(home.window.location.search, '');
assert.equal(home.window.document.activeElement.id, 'finder-q');
const coproduction = visible(home).find(c => c.dataset.country.includes('/'));
change(home, '[data-country]', coproduction.dataset.country.split('/')[1].trim());
assert(visible(home).includes(coproduction), 'Co-production can be found through either country');
reset(home);
change(home, '[data-rating]', '5');
assert(visible(home).length > 0 && visible(home).every(c => Number(c.dataset.rating) === 5));
reset(home);
change(home, '[data-sort]', 'year-asc');
assert(visible(home).every((c, i, all) => !i || Number(all[i - 1].dataset.year) <= Number(c.dataset.year)));
change(home, '[data-sort]', 'rating');
assert(visible(home).every((c, i, all) => !i || Number(all[i - 1].dataset.rating) >= Number(c.dataset.rating)));
const restored = page('index.html', '?q=Blood+Camp+Thatcher&country=Australia');
assert.deepEqual(titles(restored), ['Turkey Shoot'], 'Shared search URL restores state');
const invalid = page('index.html', '?country=Nowhere&sort=invalid&genre=unknown');
assert.equal(visible(invalid).length, total, 'Unknown filters fall back safely');

const review = page('reviews/queen-of-blood/index.html');
const doc = review.window.document;
const poster = doc.querySelector('[data-poster-enlarge]');
doc.querySelectorAll('[data-poster-alts] button')[1].click();
assert.equal(poster.href, doc.querySelector('.poster-frame img').src);
poster.click();
const dialog = doc.querySelector('dialog');
assert.equal(dialog.open, true);
assert(doc.querySelector('.lightbox-caption').textContent.includes('2 of 2'));
doc.querySelector('.lightbox-next').click();
assert(doc.querySelector('.lightbox-caption').textContent.includes('1 of 2'), 'Poster navigation wraps');
doc.querySelector('.lightbox-close').click();
assert.equal(dialog.open, false);
assert.equal(doc.activeElement, poster, 'Focus returns to the opener');
doc.querySelectorAll('[data-lightbox="stills"]')[2].click();
assert(doc.querySelector('.lightbox-caption').textContent.includes('3 of 4'));
dialog.dispatchEvent(new review.window.KeyboardEvent('keydown', { key: 'ArrowLeft', bubbles: true }));
assert(doc.querySelector('.lightbox-caption').textContent.includes('2 of 4'));
const img = doc.querySelector('.lightbox-image');
function touchEvent(type, x, y) {
  const event = new review.window.Event(type);
  Object.defineProperty(event, type === 'touchstart' ? 'touches' : 'changedTouches', { value: [{ clientX: x, clientY: y }] });
  img.dispatchEvent(event);
}
touchEvent('touchstart', 200, 100); touchEvent('touchend', 80, 105);
assert(doc.querySelector('.lightbox-caption').textContent.includes('3 of 4'), 'Horizontal swipe advances');
touchEvent('touchstart', 200, 100); touchEvent('touchend', 195, 220);
assert(doc.querySelector('.lightbox-caption').textContent.includes('3 of 4'), 'Vertical gestures do not change image');
doc.querySelector('.lightbox-close').click();
assert(!doc.documentElement.classList.contains('lightbox-open'));
const connections = [...doc.querySelectorAll('.related .card')];
assert(connections.length > 0 && connections.length <= 4);
assert(connections.every(c => c.querySelector('.card-reason') && !c.querySelector('a').href.endsWith('/queen-of-blood/')));
assert(doc.querySelector('.watch a[href="https://www.justwatch.com/uk/movie/queen-of-blood-1966"]'));
const apaches = page('reviews/apaches/index.html');
assert(apaches.window.document.querySelector('.related a[href="/reviews/the-finishing-line/"]'), 'Public information films connect');
assert(apaches.window.document.querySelector('.watch a[href*="replay.bfi.org.uk"]'));
const updates = page('updates/index.html');
assert(updates.window.document.querySelector('a[href="/feed.xml"]'));
console.log(`PASS: ${total} reviews; search, combined filters, co-productions, sorts, shared URLs, gallery navigation, swipes, focus, recommendations and viewing links.`);
[home, restored, invalid, review, apaches, updates].forEach(dom => dom.window.close());
