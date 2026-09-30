/* Watercooling.fi – kevyt yhteinen skripti (ei riippuvuuksia) */
(function () {
  document.documentElement.classList.remove('no-js');

  /* ---------- Mobiilivalikko ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Sulje valikko' : 'Avaa valikko');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ---------- Hienovarainen esiin tulo ---------- */
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && els.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Hintalaskuri (PriceCalculator) ----------
     Hintahaarukat ovat suuntaa-antavia arvioita, eivät reaaliaikaisia hintoja.
     Muokkaa arvoja tästä yhdestä paikasta. */
  var PRICES = {
    aio: {
      '120': { name: 'AiO 120 mm', min: 45, max: 80 },
      '240': { name: 'AiO 240 mm', min: 55, max: 110 },
      '280': { name: 'AiO 280 mm', min: 80, max: 130 },
      '360': { name: 'AiO 360 mm', min: 100, max: 170 },
      '420': { name: 'AiO 420 mm', min: 120, max: 220 }
    },
    custom: {
      cpu: { name: 'CPU-vesiblokki', min: 50, max: 150 },
      gpu: { name: 'GPU-vesiblokki', min: 100, max: 250 },
      pumpres: { name: 'Pumppu/säiliö', min: 90, max: 250 },
      rad360: { name: 'Radiatori 360 mm', min: 50, max: 150 },
      rad420: { name: 'Radiatori 420 mm', min: 60, max: 170 },
      fans: { name: 'Tuulettimet', min: 30, max: 150 },
      tubes: { name: 'Letkut', min: 10, max: 40 },
      fittings: { name: 'Liittimet', min: 30, max: 150 },
      coolant: { name: 'Jäähdytysneste', min: 10, max: 30 }
    }
  };

  var calc = document.querySelector('[data-calc]');
  if (!calc) return;

  var fmt = function (n) { return n.toLocaleString('fi-FI') + ' €'; };
  var modeBtns = calc.querySelectorAll('[data-mode]');
  var panels = calc.querySelectorAll('[data-panel]');
  var totalEl = calc.querySelector('[data-total]');
  var midEl = calc.querySelector('[data-mid]');
  var linesEl = calc.querySelector('[data-lines]');
  var mode = 'aio';

  // Hintahaarukat näkyviin valintoihin
  calc.querySelectorAll('[data-key]').forEach(function (inp) {
    var set = PRICES[inp.getAttribute('data-set')];
    var item = set && set[inp.getAttribute('data-key')];
    var out = inp.closest('.opt') && inp.closest('.opt').querySelector('.opt-price');
    if (item && out) out.textContent = item.min + '–' + item.max + ' €';
  });

  function update() {
    var min = 0, max = 0, rows = [];
    var panel = calc.querySelector('[data-panel="' + mode + '"]');
    panel.querySelectorAll('input:checked').forEach(function (inp) {
      var item = PRICES[inp.getAttribute('data-set')][inp.getAttribute('data-key')];
      if (!item) return;
      min += item.min; max += item.max;
      rows.push('<li><span>' + item.name + '</span><span>' + item.min + '–' + item.max + ' €</span></li>');
    });
    if (rows.length === 0) {
      totalEl.textContent = '– €';
      midEl.textContent = 'Valitse vähintään yksi osa.';
      linesEl.innerHTML = '';
      return;
    }
    totalEl.textContent = fmt(min) + ' – ' + fmt(max);
    midEl.textContent = 'Keskiarvio noin ' + fmt(Math.round((min + max) / 2 / 5) * 5);
    linesEl.innerHTML = rows.join('');
  }

  modeBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.getAttribute('data-mode');
      modeBtns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      panels.forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== mode; });
      update();
    });
  });
  calc.addEventListener('change', update);
  update();
})();
