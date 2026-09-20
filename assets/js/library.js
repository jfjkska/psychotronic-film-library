// Front-page finder: type to search, click a genre to filter. Nothing is
// required to read the site; without JavaScript every card simply shows.
(function () {
  var finder = document.querySelector('[data-finder]');
  if (!finder) return;
  var input = finder.querySelector('[data-finder-input]');
  var chips = Array.prototype.slice.call(finder.querySelectorAll('[data-genre]'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-rack] .card'));
  var empty = document.querySelector('[data-empty]');
  var genre = '';

  function norm(s) { return (s || '').toLowerCase().trim(); }

  function apply() {
    var q = norm(input.value);
    var shown = 0;
    cards.forEach(function (card) {
      var genres = (card.getAttribute('data-genres') || '').split('|');
      var hay = [card.getAttribute('data-title'), card.getAttribute('data-year'), card.getAttribute('data-director'), genres.join(' ')].join(' ');
      var ok = (!genre || genres.indexOf(genre) !== -1) && (!q || hay.indexOf(q) !== -1);
      card.hidden = !ok;
      if (ok) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      genre = norm(chip.getAttribute('data-genre'));
      chips.forEach(function (c) { c.classList.toggle('is-on', c === chip); });
      apply();
    });
  });
  var more = finder.querySelector('[data-more-genres]');
  var row = finder.querySelector('[data-genre-row]');
  if (more && row) more.addEventListener('click', function () { row.classList.add('is-open'); more.setAttribute('aria-expanded', 'true'); });
  input.addEventListener('input', apply);
  finder.addEventListener('submit', function (e) { e.preventDefault(); });
})();

// Screening room: swap the thumbnail for a YouTube embed only when pressed.
(function () {
  var players = document.querySelectorAll('[data-player]');
  Array.prototype.forEach.call(players, function (box) {
    var btn = box.querySelector('.player-face');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var id = box.getAttribute('data-player');
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
      f.title = btn.getAttribute('aria-label') || 'Video';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.setAttribute('allowfullscreen', '');
      f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
      box.replaceChild(f, btn);
    });
  });
})();

// Roll the dice: open a review at random. Falls back to the shelf without JS.
(function () {
  var dice = document.querySelector('[data-dice]');
  var reel = document.querySelector('[data-reel]');
  if (!dice || !reel) return;
  var urls;
  try { urls = JSON.parse(reel.textContent); } catch (e) { return; }
  if (!urls || !urls.length) return;
  dice.addEventListener('click', function (e) {
    e.preventDefault();
    var here = location.pathname.replace(/\/$/, '');
    var pool = urls.filter(function (u) { return u.replace(/\/$/, '') !== here; });
    var pick = (pool.length ? pool : urls)[Math.floor(Math.random() * (pool.length ? pool : urls).length)];
    location.href = pick;
  });
})();

// Other posters: tap a thumbnail to swap it into the frame.
(function () {
  var row = document.querySelector('[data-poster-alts]');
  var frame = document.querySelector('.poster-frame img');
  if (!row || !frame) return;
  row.addEventListener('click', function (e) {
    var btn = e.target.closest('.alt');
    if (!btn) return;
    frame.src = btn.getAttribute('data-src');
    Array.prototype.forEach.call(row.querySelectorAll('.alt'), function (b) { b.classList.toggle('is-on', b === btn); });
  });
})();
