// Search, filter and sort the library. The full shelf remains readable without JS.
(function () {
  var finder = document.querySelector('[data-finder]');
  if (!finder) return;
  var input = finder.querySelector('[data-finder-input]');
  var chips = Array.prototype.slice.call(finder.querySelectorAll('[data-genre]'));
  var rack = document.querySelector('[data-rack]');
  var cards = Array.prototype.slice.call(rack.querySelectorAll('.card'));
  var empty = document.querySelector('[data-empty]');
  var decade = finder.querySelector('[data-decade]');
  var country = finder.querySelector('[data-country]');
  var rating = finder.querySelector('[data-rating]');
  var sort = finder.querySelector('[data-sort]');
  var count = document.querySelector('[data-result-count]');
  var reset = document.querySelector('[data-reset-finder]');
  var row = finder.querySelector('[data-genre-row]');
  var more = finder.querySelector('[data-more-genres]');
  var genre = '';

  function norm(s) {
    return (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function countries(s) { return (s || '').split(/\s*[,/;]\s*/).filter(Boolean); }
  var records = cards.map(function (card, index) {
    var data = card.dataset;
    return {
      card: card, index: index, title: data.title || '', year: Number(data.year) || 0,
      date: Number(data.date) || 0, rating: Number(data.rating) || 0,
      countries: countries(data.country), genres: (data.genres || '').split('|'),
      hay: norm([data.title, data.aka, data.cast, data.director, data.year, data.country, data.genres].join(' '))
    };
  });
  function addOptions(select, values, label) {
    values.forEach(function (value) {
      var option = document.createElement('option');
      option.value = value; option.textContent = label ? label(value) : value;
      select.appendChild(option);
    });
  }
  var decades = [];
  var nations = [];
  records.forEach(function (r) {
    var d = String(Math.floor(r.year / 10) * 10);
    if (r.year && decades.indexOf(d) === -1) decades.push(d);
    r.countries.forEach(function (c) { if (nations.indexOf(c) === -1) nations.push(c); });
  });
  addOptions(decade, decades.sort(), function (d) { return d + 's'; });
  addOptions(country, nations.sort(function (a, b) { return a.localeCompare(b); }));
  finder.querySelector('[data-finder-controls]').hidden = false;
  document.querySelector('[data-finder-summary]').hidden = false;

  function apply(updateURL) {
    var words = norm(input.value).split(' ').filter(Boolean);
    var shown = 0;
    records.forEach(function (r) {
      var ok = (!genre || r.genres.indexOf(genre) !== -1) &&
        words.every(function (word) { return r.hay.indexOf(word) !== -1; }) &&
        (!decade.value || Math.floor(r.year / 10) * 10 === Number(decade.value)) &&
        (!country.value || r.countries.indexOf(country.value) !== -1) &&
        (!rating.value || r.rating >= Number(rating.value));
      r.card.hidden = !ok;
      if (ok) shown++;
    });
    var ordered = records.slice().sort(function (a, b) {
      var result = 0;
      if (sort.value === 'title') result = a.title.localeCompare(b.title, 'en', { sensitivity: 'base' });
      else if (sort.value === 'rating') result = b.rating - a.rating;
      else if (sort.value === 'year-asc') result = (a.year || Infinity) - (b.year || Infinity);
      else if (sort.value === 'year-desc') result = b.year - a.year;
      else result = b.date - a.date;
      return result || a.index - b.index;
    });
    var fragment = document.createDocumentFragment();
    ordered.forEach(function (r) { fragment.appendChild(r.card); });
    rack.appendChild(fragment);
    chips.forEach(function (chip) {
      var on = chip.getAttribute('data-genre') === genre;
      chip.classList.toggle('is-on', on);
      chip.setAttribute('aria-pressed', String(on));
      if (on && chip.classList.contains('chip-more')) {
        row.classList.add('is-open');
        if (more) more.setAttribute('aria-expanded', 'true');
      }
    });
    if (empty) empty.hidden = shown !== 0;
    count.textContent = shown + ' of ' + cards.length + ' films';
    reset.hidden = !(input.value || genre || decade.value || country.value || rating.value || sort.value !== 'newest');
    if (updateURL) {
      var url = new URL(location.href);
      var values = { q: input.value.trim(), genre: genre, decade: decade.value, country: country.value, rating: rating.value, sort: sort.value === 'newest' ? '' : sort.value };
      Object.keys(values).forEach(function (key) {
        if (values[key]) url.searchParams.set(key, values[key]); else url.searchParams.delete(key);
      });
      history.replaceState(null, '', url.pathname + url.search + url.hash);
    }
  }
  function restore() {
    var params = new URLSearchParams(location.search);
    input.value = params.get('q') || '';
    genre = params.get('genre') || '';
    if (!chips.some(function (c) { return c.getAttribute('data-genre') === genre; })) genre = '';
    [decade, country, rating, sort].forEach(function (select) {
      var value = params.get(select.name) || (select === sort ? 'newest' : '');
      select.value = value;
      if (select.selectedIndex < 0) select.selectedIndex = 0;
    });
    apply(false);
  }
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      genre = chip.getAttribute('data-genre');
      apply(true);
    });
  });
  if (more && row) more.addEventListener('click', function () { row.classList.add('is-open'); more.setAttribute('aria-expanded', 'true'); });
  input.addEventListener('input', function () { apply(true); });
  [decade, country, rating, sort].forEach(function (select) { select.addEventListener('change', function () { apply(true); }); });
  reset.addEventListener('click', function () {
    finder.reset(); genre = ''; apply(true); input.focus();
  });
  finder.addEventListener('submit', function (e) { e.preventDefault(); });
  window.addEventListener('popstate', restore);
  restore();
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
    var enlarge = document.querySelector('[data-poster-enlarge]');
    if (enlarge) enlarge.href = frame.src;
    Array.prototype.forEach.call(row.querySelectorAll('.alt'), function (b) { b.classList.toggle('is-on', b === btn); });
  });
})();

// Posters and stills: native modal dialog, keyboard navigation and touch swipes.
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (!links.length) return;
  var dialog = document.createElement('dialog');
  if (typeof dialog.showModal !== 'function') return;
  dialog.className = 'lightbox';
  dialog.setAttribute('aria-label', 'Image viewer');
  dialog.innerHTML = '<div class="lightbox-panel">' +
    '<button type="button" class="lightbox-close" aria-label="Close image viewer">Close ×</button>' +
    '<button type="button" class="lightbox-prev" aria-label="Previous image">‹</button>' +
    '<img class="lightbox-image" alt="">' +
    '<button type="button" class="lightbox-next" aria-label="Next image">›</button>' +
    '<div class="lightbox-caption"><p aria-live="polite" aria-atomic="true"></p><a target="_blank" rel="noopener">Open full image</a></div></div>';
  document.body.appendChild(dialog);
  var image = dialog.querySelector('img');
  var caption = dialog.querySelector('p');
  var original = dialog.querySelector('a');
  var previous = dialog.querySelector('.lightbox-prev');
  var next = dialog.querySelector('.lightbox-next');
  var close = dialog.querySelector('.lightbox-close');
  var items = [], index = 0, opener, touch;
  var title = document.querySelector('.review-head h1').textContent;
  function show(position) {
    index = (position + items.length) % items.length;
    image.alt = items[index].alt;
    image.src = items[index].src;
    original.href = items[index].src;
    caption.textContent = items[index].alt + ' · ' + (index + 1) + ' of ' + items.length;
    previous.hidden = next.hidden = items.length < 2;
  }
  links.forEach(function (link) {
    link.addEventListener('click', function (event) {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); opener = link;
      if (link.dataset.lightbox === 'posters') {
        var variants = Array.prototype.slice.call(document.querySelectorAll('[data-poster-alts] [data-src]'));
        items = variants.length ? variants.map(function (b, i) { return { src: b.dataset.src, alt: title + ' — poster ' + (i + 1) }; }) : [{ src: link.getAttribute('href'), alt: title + ' — poster' }];
      } else {
        items = links.filter(function (l) { return l.dataset.lightbox === 'stills'; }).map(function (l) { return { src: l.getAttribute('href'), alt: l.querySelector('img').alt }; });
      }
      var current = items.findIndex(function (item) { return new URL(item.src, location.href).href === link.href; });
      show(current < 0 ? 0 : current);
      dialog.showModal();
      document.documentElement.classList.add('lightbox-open');
      close.focus();
    });
  });
  close.addEventListener('click', function () { dialog.close(); });
  previous.addEventListener('click', function () { show(index - 1); });
  next.addEventListener('click', function () { show(index + 1); });
  dialog.addEventListener('click', function (event) { if (event.target === dialog || event.target.classList.contains('lightbox-panel')) dialog.close(); });
  dialog.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(index - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(index + 1); }
  });
  dialog.addEventListener('close', function () {
    document.documentElement.classList.remove('lightbox-open');
    image.removeAttribute('src');
    if (opener) opener.focus();
  });
  image.addEventListener('error', function () { caption.textContent = 'This image could not be loaded. Try opening the full image.'; });
  image.addEventListener('touchstart', function (event) {
    touch = event.touches.length === 1 ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  image.addEventListener('touchend', function (event) {
    if (!touch || !event.changedTouches.length) return;
    var dx = event.changedTouches[0].clientX - touch.x;
    var dy = event.changedTouches[0].clientY - touch.y;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.5) show(index + (dx < 0 ? 1 : -1));
    touch = null;
  }, { passive: true });
})();
