# -*- coding: utf-8 -*-
"""Watercooling.fi – staattisen sivuston generaattori.
Yhteiset komponentit (Header, Footer, Hero, kortit, FAQ ...) ovat funktioita,
joilla kaikki sivut rakennetaan. Aja: python3 build.py  -> tiedostot /tmp/wc/
"""
import json, html, os

OUT = "/tmp/wc"
SITE = "https://watercooling.fi"
UPDATED = "30.9.2026"
UPDATED_ISO = "2026-09-30"
e = html.escape

NAV = [
    ("/", "Etusivu", "index"),
    ("/vesijaahdytys", "Vesijäähdytys", "vesijaahdytys"),
    ("/aio", "AiO", "aio"),
    ("/custom-loop", "Custom Loop", "custom-loop"),
    ("/komponentit", "Komponentit", "komponentit"),
    ("/hinnat", "Hinnat", "hinnat"),
    ("/tuotemerkit", "Tuotemerkit", "tuotemerkit"),
    ("/oppaat", "Oppaat", "oppaat"),
    ("/ukk", "UKK", "ukk"),
]

CUR = ' aria-current="page"'
PRICE_NOTE = "Hintatiedot ovat suuntaa-antavia ja voivat muuttua jälleenmyyjien, tarjousten ja saatavuuden mukaan."

# ---------------------------------------------------------------- ikonit
ICONS = {
 "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>',
 "warn": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01"/></svg>',
 "cpu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/></svg>',
 "gpu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="2" y="6" width="20" height="11" rx="2"/><circle cx="9" cy="11.5" r="3"/><circle cx="16.5" cy="11.5" r="2"/><path d="M5 17v3M9 17v2"/></svg>',
 "rad": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="2" y="7" width="20" height="10" rx="2"/><path d="M6 7v10M10 7v10M14 7v10M18 7v10"/></svg>',
 "pump": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 8a4 4 0 0 1 4 4M12 16a4 4 0 0 1-4-4"/><circle cx="12" cy="12" r="1.5"/></svg>',
 "res": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="7" y="2.5" width="10" height="19" rx="3"/><path d="M7 11c2 1 4-1 6 0s3 0 4-.5"/></svg>',
 "fan": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="4"/><circle cx="12" cy="12" r="1.6"/><path d="M12 10.4c0-3 1-5 3.5-5M13.6 12c3 0 5 1 5 3.5M12 13.6c0 3-1 5-3.5 5M10.4 12c-3 0-5-1-5-3.5"/></svg>',
 "tube": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 20c0-8 4-8 8-8s8 0 8-8"/><path d="M7 20c0-6 3-5.5 5-5.5s8-.5 8-6.5" opacity=".5"/></svg>',
 "fit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M8 3h8v4H8zM7 7h10v4H7zM9 11h6v10H9z"/></svg>',
 "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.5s6.5 7 6.5 11.5a6.5 6.5 0 0 1-13 0C5.5 9.5 12 2.5 12 2.5z"/></svg>',
 "loop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 2l3 3-3 3"/><path d="M4 11V9a4 4 0 0 1 4-4h12"/><path d="M7 22l-3-3 3-3"/><path d="M20 13v2a4 4 0 0 1-4 4H4"/></svg>',
 "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/></svg>',
 "temp": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M14 14.8V4a2 2 0 0 0-4 0v10.8a4 4 0 1 0 4 0z"/></svg>',
 "sound": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>',
 "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5v14z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/></svg>',
 "euro": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M18 6.5A7 7 0 1 0 18 17.5"/><path d="M4 10h10M4 14h10"/></svg>',
 "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.3"/></svg>',
 "help": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7M12 17h.01"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
}

LOGO = '''<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22c7e8"/><stop offset="1" stop-color="#3b82f6"/></linearGradient></defs><rect x="1" y="1" width="38" height="38" rx="11" fill="#0f141b" stroke="rgba(148,178,210,.25)"/><path d="M20 8s8 8.6 8 14.2A8 8 0 0 1 12 22.2C12 16.6 20 8 20 8z" fill="url(#lg)"/><path d="M16.5 23.5a3.6 3.6 0 0 0 3.5 3.3" stroke="#e8f9ff" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".8"/></svg>'''

# ---------------------------------------------------------------- komponentit
def header(active):
    items = "".join(
        f'<li><a href="{href}"{CUR if key == active else ""}>{label}</a></li>'
        for href, label, key in NAV)
    return f'''<a class="skip" href="#sisalto">Siirry sisältöön</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="/" aria-label="Watercooling.fi – etusivu">{LOGO}<span class="logo-text"><span class="logo-name">WATERCOOLING.FI</span><span class="logo-tag">Suomalainen vesijäähdytyksen tietopankki</span></span></a>
    <nav id="main-nav" class="main-nav" aria-label="Päävalikko">
      <ul>{items}</ul>
      <a class="btn btn-primary nav-cta" href="/hinnat#laskuri">Aloita vesijäähdytyksen suunnittelu →</a>
    </nav>
    <a class="btn btn-primary btn-sm header-cta" href="/hinnat#laskuri">Aloita suunnittelu →</a>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Avaa valikko">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
  </div>
</header>'''

def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l, k in NAV[1:])
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/">{LOGO}<span class="logo-text"><span class="logo-name">WATERCOOLING.FI</span></span></a>
        <p class="muted mt-2">Suomalainen vesijäähdytyksen tietopankki.</p>
        <p class="small muted">Riippumaton tietosivusto – ei verkkokauppa. {PRICE_NOTE}</p>
      </div>
      <nav aria-label="Sivuston osiot"><h2>Sisältö</h2><ul>{links}</ul></nav>
      <nav aria-label="Tietoa sivustosta"><h2>Sivusto</h2><ul>
        <li><a href="/tietosuoja">Tietosuojakäytäntö</a></li>
        <li><a href="/evasteet">Evästekäytäntö</a></li>
        <li><a href="/yhteystiedot">Yhteystiedot</a></li>
      </ul></nav>
    </div>
    <div class="footer-bottom"><span>© 2026 Watercooling.fi</span><span>Sisältö päivitetty {UPDATED}</span></div>
  </div>
</footer>'''

def breadcrumbs(trail):
    """trail: [(nimi, polku), ...] – viimeinen on nykyinen sivu."""
    lis = []
    for i, (name, path) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append(f'<li aria-current="page">{name}</li>')
        else:
            lis.append(f'<li><a href="{path}">{name}</a></li>')
    return f'<nav class="breadcrumbs" aria-label="Murupolku"><ol>{"".join(lis)}</ol></nav>'

def breadcrumb_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (p if p != "/" else "/")}
        for i, (n, p) in enumerate(trail)]}

def infobox(text, kind="info"):
    cls = "infobox infobox--warn" if kind == "warn" else "infobox"
    return f'<div class="{cls}" role="note">{ICONS["warn" if kind=="warn" else "info"]}<div><p>{text}</p></div></div>'

def faq_block(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in items) + '</div>'

def faq_schema(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

def cta(title="Suunnittele oma vesijäähdytyksesi",
        text="Laske suuntaa-antava budjetti AiO- tai custom loop -kokoonpanolle ja tutustu komponentteihin ennen ostopäätöstä.",
        primary=("Avaa hintalaskuri", "/hinnat#laskuri"), secondary=("Lue aloittelijan opas", "/oppaat/vesijaahdytys-aloittelijalle")):
    return f'''<section class="section"><div class="container"><div class="cta-band reveal">
  <h2>{title}</h2><p>{text}</p>
  <div class="btn-row"><a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a><a class="btn btn-ghost" href="{secondary[1]}">{secondary[0]}</a></div>
</div></div></section>'''

def page(slug, title, desc, body, active, schema_extra=None, og_type="website", path=None):
    path = path if path is not None else ("/" if slug == "index" else "/" + slug)
    canonical = SITE + path
    graph = [
        {"@type": "Organization", "@id": SITE + "/#org", "name": "Watercooling.fi", "url": SITE + "/",
         "logo": SITE + "/favicon.svg"},
        {"@type": "WebSite", "@id": SITE + "/#website", "name": "Watercooling.fi", "url": SITE + "/",
         "inLanguage": "fi-FI", "publisher": {"@id": SITE + "/#org"},
         "description": "Suomalainen vesijäähdytyksen tietopankki"},
    ]
    if schema_extra:
        graph += schema_extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    doc = f'''<!doctype html>
<html lang="fi" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#06080b">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fi_FI">
<meta property="og:site_name" content="Watercooling.fi">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{header(active)}
<main id="sisalto">
{body}
</main>
{footer()}
<script src="/main.js" defer></script>
</body>
</html>
'''
    # kaikki tiedostot juureen (litteä rakenne); alihakemistopolut muunnetaan tiedostonimiksi
    fname = ("index" if slug == "index" else slug.replace("/", "-")) + ".html"
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)

def page_hero(trail, eyebrow, h1, lead, extra=""):
    return f'''<section class="page-hero"><div class="container">
  {breadcrumbs(trail)}
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>{extra}
  <p class="updated">Päivitetty {UPDATED}</p>
</div></section>'''

def section(inner, alt=False, id_=None, narrow=False):
    idattr = f' id="{id_}"' if id_ else ""
    return f'<section class="section{" section--alt" if alt else ""}"{idattr}><div class="container{" narrow" if narrow else ""}">{inner}</div></section>'

def head(eyebrow, h2, lead="", h2id=None):
    hid = f' id="{h2id}"' if h2id else ""
    lp = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="section-head reveal"><span class="eyebrow">{eyebrow}</span><h2{hid}>{h2}</h2>{lp}</div>'

# ---------------------------------------------------------------- data
BASICS = [
 ("cpu", "CPU-vesijäähdytys", "Prosessorin päälle asennettava vesiblokki siirtää lämmön nesteeseen. Yleisin tapa aloittaa vesijäähdytys – usein valmiilla AiO-jäähdyttimellä."),
 ("gpu", "GPU-vesijäähdytys", "Näytönohjaimen alkuperäinen jäähdytin korvataan vesiblokilla. Tyypillisesti osa custom loopia ja selvästi vaativampi projekti."),
 ("box", "AiO", "All-in-One eli valmiiksi koottu ja suljettu järjestelmä: pumppu, blokki, letkut ja radiatori samassa paketissa."),
 ("loop", "Custom loop", "Avoin vesijäähdytys, joka kootaan erillisistä osista. Voi jäähdyttää sekä prosessorin että näytönohjaimen."),
 ("pump", "Pumppu", "Kierrättää nestettä järjestelmässä. AiO:ssa pumppu on yleensä vesiblokin yhteydessä."),
 ("cpu", "Vesiblokki", "Metallinen, yleensä kuparipohjainen kappale, joka on suorassa kosketuksessa komponenttiin ja johtaa lämmön nesteeseen."),
 ("rad", "Radiatori / jäähdytin", "Ohuista lamelleista koostuva lämmönvaihdin, josta tuulettimet puhaltavat lämmön pois ilmaan."),
 ("tube", "Letkut", "Kuljettavat nestettä osien välillä. Custom loopissa valitaan joustavan letkun ja kovaputken välillä."),
 ("fit", "Liittimet", "Kiinnittävät letkut komponentteihin. Yleisin kierrestandardi on G1/4\"."),
 ("drop", "Jäähdytysneste", "Tislattuun veteen perustuva neste, johon on lisätty korroosion- ja kasvustonestoaineita."),
]

COMPONENTS = [
 ("cpu", "CPU-vesiblokki", "Siirtää prosessorin lämmön nesteeseen.", "Ilman blokkia lämpö ei siirry prosessorilta kiertoon.", "Socket-tuki (esim. AM5, LGA1700, LGA1851), kiinnityssarja ja virtausrajoitus.", "50–150 €"),
 ("gpu", "GPU-vesiblokki", "Korvaa näytönohjaimen tehdasjäähdyttimen ja jäähdyttää grafiikkapiiriä, muisteja ja virransyöttöä.", "Tarvitaan, jos näytönohjain halutaan mukaan looppiin.", "Blokki on tehty tietylle piirilevylle – yhteensopivuus on tarkistettava mallikohtaisesti.", "100–250+ €"),
 ("rad", "Radiatori", "Luovuttaa nesteen lämmön ilmaan tuulettimien avulla.", "Radiatori on järjestelmän varsinainen lämmönpoistaja.", "Koko (120–480 mm), paksuus, lamellitiheys ja kotelon tuki.", "50–150 €"),
 ("pump", "Pumppu", "Pitää nesteen kierrossa tasaisella virtauksella.", "Ilman virtausta lämpö jää blokkiin ja lämpötilat nousevat nopeasti.", "Pumppumalli (esim. D5 tai DDC), melutaso, ohjaus PWM:llä.", "70–150 €"),
 ("res", "Säiliö", "Varastoi nestettä, helpottaa täyttöä ja ilmanpoistoa.", "Tekee loopin täytöstä ja huollosta selvästi helpompaa.", "Usein yhdistetty pumppuun; tarkista kiinnitystapa ja koko.", "40–120 €"),
 ("fan", "Tuulettimet", "Puhaltavat ilmaa radiatorin läpi.", "Radiatori ilman ilmavirtaa jäähdyttää hyvin heikosti.", "Staattinen paine, melutaso ja PWM-ohjaus; koko 120 tai 140 mm.", "30–150 €"),
 ("tube", "Letkut", "Kuljettavat nestettä komponenttien välillä.", "Muodostavat loopin reitin.", "Joustava letku on helpompi; kovaputki vaatii taivutusta ja tarkkuutta.", "10–40 €"),
 ("fit", "Liittimet", "Kiinnittävät letkut blokkeihin, radiatoreihin ja säiliöön.", "Tiiviit liitokset ovat vuodottoman loopin perusta.", "Letkun sisä- ja ulkohalkaisijan on vastattava liitintä.", "30–150+ €"),
 ("drop", "Jäähdytysneste", "Siirtää lämpöä ja suojaa järjestelmää korroosiolta.", "Pelkkä hanavesi voi aiheuttaa kasvustoa ja korroosiota.", "Valmisneste tai tislattu vesi + lisäaineet; vältä metallien sekoittamista.", "10–30 €"),
]

RADS = [
 ("120 mm", 1, "Pienet kotelot ja kevyet kuormat. Pinta-ala on rajallinen, joten tuulettimet joutuvat usein pyörimään nopeammin."),
 ("240 mm", 2, "Yleinen valinta keskitason prosessoreille. Mahtuu useimpiin koteloihin."),
 ("280 mm", 2, "Kaksi 140 mm:n tuuletinta – enemmän pinta-alaa kuin 240 mm:ssä, usein hiljaisemmin kierroksin."),
 ("360 mm", 3, "Suosittu tehokkaiden prosessorien kanssa. Vaatii kotelolta pidemmän kiinnityspaikan."),
 ("420 mm", 3, "Kolme 140 mm:n tuuletinta ja paljon pinta-alaa. Kotelotuki on selvästi harvinaisempi."),
]

BRANDS = [
 ("Arctic", "AR", "Tunnettu erityisesti Liquid Freezer -sarjan AiO-jäähdyttimistä.", ["AiO"]),
 ("Corsair", "CO", "Laaja valikoima AiO-jäähdyttimiä sekä custom loop -komponentteja.", ["AiO", "Custom loop"]),
 ("NZXT", "NZ", "Tunnettu Kraken-sarjan AiO-jäähdyttimistä.", ["AiO"]),
 ("ASUS / ROG", "AS", "AiO-vesijäähdyttimiä erityisesti ROG- ja Prime-tuoteperheissä.", ["AiO"]),
 ("Cooler Master", "CM", "AiO-jäähdyttimiä ja muita PC-jäähdytysratkaisuja.", ["AiO"]),
 ("be quiet!", "BQ", "Valmistaja, joka painottaa tuotteissaan hiljaista jäähdytystä. Valikoimassa myös AiO-jäähdyttimiä.", ["AiO"]),
 ("Alphacool", "AC", "Laaja custom-vesijäähdytysvalikoima: radiatorit, CPU- ja GPU-blokit, pumput, säiliöt ja liittimet. Myös AiO-malleja.", ["Custom loop", "AiO"]),
 ("EKWB", "EK", "Tunnettu custom loop -vesijäähdytyskomponenteista.", ["Custom loop"]),
 ("Thermaltake", "TT", "Sekä AiO- että custom loop -ratkaisuja.", ["AiO", "Custom loop"]),
 ("Lian Li", "LL", "Koteloita, tuulettimia ja AiO-ratkaisuja.", ["AiO"]),
 ("MSI", "MS", "AiO-vesijäähdyttimiä muiden PC-komponenttien ohella.", ["AiO"]),
 ("Fractal Design", "FD", "Koteloita sekä AiO-vesijäähdytysratkaisuja.", ["AiO"]),
 ("Gigabyte / AORUS", "GA", "AiO-vesijäähdytysratkaisuja AORUS- ja Gigabyte-tuotemerkeillä.", ["AiO"]),
 ("Phanteks", "PH", "Koteloita, custom cooling -komponentteja ja PC-jäähdytystä.", ["Custom loop"]),
 ("Noctua", "NO", "Tunnettu ensisijaisesti ilmajäähdytyksestä. Seuraamme valmistajan mahdollisia vesijäähdytysmarkkinoille tulevia tuotteita ja päivitämme tiedot, kun ne ovat saatavilla.", ["Ilmajäähdytys"]),
]

GUIDES = [
 ("vesijaahdytys-aloittelijalle", "Vesijäähdytys aloittelijalle", "Perusteet selkokielellä: miten vesijäähdytys toimii ja kumpi sopii sinulle, AiO vai custom loop.", "Perusteet", True),
 ("aio-vai-ilmajaahdytys", "AiO vai ilmajäähdytys?", "Milloin tornijäähdytin riittää ja milloin AiO tuo todellista hyötyä.", "Vertailu", False),
 ("240-vs-280-vs-360", "240 mm vs 280 mm vs 360 mm", "Radiatorikoot vertailussa: pinta-ala, melu ja kotelotuki.", "Radiatorit", False),
 ("custom-loop-aloittelijalle", "Custom loop aloittelijalle", "Mitä ensimmäiseen avoimeen looppiin tarvitaan ja mihin kannattaa varautua.", "Custom loop", False),
 ("custom-loop-hinta", "Kuinka paljon custom loop maksaa?", "Suuntaa-antavat budjetit perus-, keski- ja premium-tason looppeihin.", "Hinnat", False),
 ("nain-valitset-aio", "Näin valitset AiO-vesijäähdytyksen", "Koko, pumppu, tuulettimet, takuu ja socket-tuki – tarkistuslista ostajalle.", "AiO", False),
 ("kotelon-radiatorituki", "Näin tarkistat kotelon radiatorituen", "Mittaa oikein: pituus, paksuus, tuulettimet ja emolevyn komponentit.", "Yhteensopivuus", False),
 ("cpu-vesijaahdytys", "CPU-vesijäähdytys", "TDP, kulutus ja socketit (AM5, LGA1700, LGA1851) prosessorin vesijäähdytyksessä.", "CPU", False),
 ("gpu-vesijaahdytys", "GPU-vesijäähdytys", "Full-cover-blokit, VRAM, VRM ja hotspot – näytönohjaimen vesijäähdytys käytännössä.", "GPU", False),
 ("onko-vesijaahdytys-turvallinen", "Onko vesijäähdytys turvallinen?", "Vuotoriski, vuototesti ja huolto – realistinen katsaus riskeihin.", "Turvallisuus", False),
 ("vesijaahdytys-sahkonkulutus", "Kuinka paljon vesijäähdytys kuluttaa sähköä?", "Pumppujen ja tuulettimien kulutus suhteessa koko tietokoneeseen.", "Sähkö", False),
 ("yleisimmat-virheet", "Vesijäähdytyksen yleisimmät virheet", "Suojakalvot, väärä virtaussuunta, ilmakuplat ja muut tyypilliset sudenkuopat.", "Vinkit", False),
]

FAQ = [
 ("Mitä vesijäähdytys tarkoittaa?", "Vesijäähdytyksessä komponentin, kuten prosessorin tai näytönohjaimen, lämpö siirretään nesteeseen vesiblokin kautta. Pumppu kierrättää nesteen radiatoriin, josta tuulettimet puhaltavat lämmön ilmaan."),
 ("Onko vesijäähdytys parempi kuin ilmajäähdytys?", "Ei automaattisesti. Hyvä ilmajäähdytin riittää monelle prosessorille ja on yksinkertainen sekä pitkäikäinen. Vesijäähdytyksestä on yleensä eniten hyötyä, kun lämpökuorma on suuri, kotelossa halutaan tilaa prosessorin ympärille tai kun halutaan jäähdyttää myös näytönohjain. Lopputulos riippuu aina kokoonpanosta."),
 ("Mikä on AiO?", "AiO eli All-in-One on valmiiksi koottu ja suljettu vesijäähdytin. Paketissa on pumppu, CPU-vesiblokki, letkut, radiatori ja neste. Se asennetaan suunnilleen yhtä helposti kuin ilmajäähdytin, eikä sitä tarvitse täyttää."),
 ("Mitä custom loop tarkoittaa?", "Custom loop eli avoin vesijäähdytys rakennetaan erillisistä osista: vesiblokeista, pumpusta, säiliöstä, radiatoreista, letkuista ja liittimistä. Se on muokattava ja voi jäähdyttää sekä CPU:n että GPU:n, mutta vaatii suunnittelua ja huoltoa."),
 ("Paljonko vesijäähdytys maksaa?", "AiO-vesijäähdytin maksaa suuntaa-antavasti noin 50–300 € koosta ja varustelusta riippuen. Custom loop maksaa tyypillisesti useita satoja euroja, CPU+GPU-loop helposti 500 € tai enemmän. Katso tarkemmat hintahaarukat <a href=\"/hinnat\">hintasivulta</a>."),
 ("Tarvitsenko vesijäähdytyksen pelitietokoneeseen?", "Et välttämättä. Moni pelikone toimii hyvin laadukkaalla ilmajäähdyttimellä. Vesijäähdytystä kannattaa harkita erityisesti tehokkaan, paljon virtaa kuluttavan prosessorin kanssa tai jos arvostat tiettyä ulkonäköä tai kotelon tilankäyttöä."),
 ("Onko vesijäähdytys turvallista?", "Oikein asennettuna vesijäähdytys on yleisesti turvallinen. AiO on tehtaalla suljettu ja testattu. Custom loopissa riskit liittyvät lähinnä asennusvirheisiin, joten vuototesti ennen käynnistystä on välttämätön."),
 ("Voiko vesijäähdytys vuotaa?", "Voi, vaikka se on harvinaista. Custom loopissa vuotoriski on suurempi, koska liitoksia on enemmän ja ne tehdään itse. Tee aina vuototesti, tarkista liittimet ja seuraa järjestelmää erityisesti ensimmäisten päivien aikana."),
 ("Kuinka kauan AiO kestää?", "Käyttöikä riippuu tuotteesta, pumpusta ja käyttöolosuhteista. Monet valmistajat antavat AiO:lle useamman vuoden takuun, mikä antaa suuntaa odotettavasta käyttöiästä. Nesteen hidas haihtuminen ja pumpun kuluminen rajoittavat lopulta ikää."),
 ("Tarvitseeko AiO huoltaa?", "Juuri ei. Riittää, että radiatorin lamellit ja tuulettimet puhdistetaan pölystä säännöllisesti ja pumpun ääniä sekä lämpötiloja seurataan. AiO:ta ei tavallisesti avata eikä täytetä."),
 ("Mikä on hyvä radiatori?", "Hyvä radiatori on sellainen, joka mahtuu koteloon ja vastaa lämpökuormaa. Pinta-ala, paksuus, lamellitiheys ja tuulettimet vaikuttavat yhdessä. Tiheälamellinen radiatori tarvitsee staattiselta paineeltaan hyviä tuulettimia."),
 ("Onko 240 mm vai 360 mm parempi?", "360 mm:n radiatorissa on enemmän pinta-alaa, joten se voi poistaa enemmän lämpöä tai tehdä saman työn hiljaisemmin. Se ei kuitenkaan ole aina parempi valinta: kotelotuki, ilmanvaihto, tuulettimet ja prosessorin kulutus ratkaisevat. Kevyellä kuormalla ero voi jäädä pieneksi."),
 ("Voiko GPU:n jäähdyttää vedellä?", "Voi. Yleisin tapa on vaihtaa näytönohjaimeen full-cover-vesiblokki ja liittää se custom looppiin. Markkinoilla on myös tehtaalla vesijäähdytettyjä näytönohjaimia. GPU-vesijäähdytys on kuitenkin selvästi vaativampi projekti kuin CPU:n AiO."),
 ("Voiko CPU:n ja GPU:n jäähdyttää samalla loopilla?", "Voi, ja se on custom loopin tyypillisin käyttötarkoitus. Tällöin radiatoripinta-alaa kannattaa mitoittaa molempien komponenttien yhteenlasketun lämpökuorman mukaan."),
 ("Mitä custom loop maksaa?", "Pelkän prosessorin custom loop maksaa suuntaa-antavasti noin 250–600 €, ja CPU+GPU-loop tyypillisesti noin 400–1 000 € tai enemmän. Hinta riippuu radiatoreista, liittimien määrästä ja siitä, käytetäänkö kovaputkea."),
 ("Onko vesijäähdytys hiljainen?", "Ei automaattisesti. Melu syntyy pumpusta, tuulettimista, ilmavirrasta ja joskus resonanssista. Suurempi radiatoripinta-ala voi mahdollistaa tuulettimien pienemmät kierrokset, mutta lopputulos riippuu koko järjestelmästä ja säädöistä."),
 ("Mitä pumppu tekee?", "Pumppu kierrättää jäähdytysnestettä vesiblokeista radiatoreihin ja takaisin. Ilman virtausta lämpö ei siirry pois komponenteilta. Pumpun nopeutta voi usein säätää PWM-ohjauksella."),
 ("Mitä jäähdytysnestettä pitäisi käyttää?", "Custom loopissa käytetään yleensä vesijäähdytykseen tarkoitettua valmisnestettä tai tislattua vettä korroosion- ja kasvustonestoaineiden kanssa. Hanavettä ei suositella. AiO:ssa neste on valmiina, eikä sitä vaihdeta."),
 ("Miten tarkistan kotelon yhteensopivuuden?", "Katso kotelon valmistajan teknisistä tiedoista tuetut radiatorikoot ja -paikat (esim. katto, etu, sivu) sekä suurin sallittu paksuus. Huomioi myös emolevyn jäähdytysrivat, RAM-kammat ja tuulettimien paksuus."),
 ("Kannattaako aloittelijan rakentaa custom loop?", "Se on mahdollista, jos suunnittelee huolella ja varaa aikaa. Moni aloittaa AiO:lla ja siirtyy custom looppiin myöhemmin. Jos rakennat ensimmäisen loopin, aloita joustavilla letkuilla, lue asennusohjeet ja tee perusteellinen vuototesti."),
]

# ---------------------------------------------------------------- hero-kuva (inline SVG)
HERO_SVG = '''<svg viewBox="0 0 560 520" role="img" aria-labelledby="hero-t hero-d">
<title id="hero-t">Havainnekuva vesijäähdytetystä tietokoneesta</title>
<desc id="hero-d">Tietokoneen kotelo, jossa katossa 360 mm radiatori tuulettimineen, prosessorin vesiblokki, näytönohjaimen vesiblokki, pumppu ja säiliö sekä niitä yhdistävät letkut.</desc>
<defs>
 <linearGradient id="hg-case" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141b24"/><stop offset="1" stop-color="#0a0e13"/></linearGradient>
 <linearGradient id="hg-cool" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22c7e8"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
 <linearGradient id="hg-glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="rgba(255,255,255,.07)"/><stop offset=".5" stop-color="rgba(255,255,255,0)"/></linearGradient>
 <radialGradient id="hg-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="rgba(34,199,232,.35)"/><stop offset="1" stop-color="rgba(34,199,232,0)"/></radialGradient>
 <linearGradient id="hg-res" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(34,199,232,.15)"/><stop offset=".35" stop-color="rgba(34,199,232,.55)"/><stop offset="1" stop-color="rgba(59,130,246,.7)"/></linearGradient>
</defs>
<!-- kotelo -->
<rect x="40" y="20" width="480" height="480" rx="26" fill="url(#hg-case)" stroke="rgba(148,178,210,.22)" stroke-width="2"/>
<rect x="58" y="38" width="444" height="444" rx="16" fill="#080b0f" stroke="rgba(148,178,210,.1)"/>
<!-- radiatori + tuulettimet katossa -->
<rect x="92" y="54" width="380" height="64" rx="8" fill="#10161e" stroke="rgba(148,178,210,.22)"/>
<g stroke="rgba(148,178,210,.1)">''' + "".join(f'<line x1="{100+i*8}" y1="60" x2="{100+i*8}" y2="112"/>' for i in range(46)) + '''</g>
''' + "".join(f'''<g transform="translate({152+i*122} 86)"><circle r="27" fill="#0b1016" stroke="rgba(34,199,232,.45)" stroke-width="1.5"/><g class="fan-spin"><path d="M0-4C3-14 11-18 17-12 12-6 5-3 0-4ZM4 0C14 3 18 11 12 17 6 12 3 5 4 0ZM0 4C-3 14-11 18-17 12-12 6-5 3 0 4ZM-4 0C-14-3-18-11-12-17-6-12-3-5-4 0Z" fill="rgba(34,199,232,.35)"/></g><circle r="5" fill="#141b24" stroke="rgba(34,199,232,.6)"/></g>''' for i in range(3)) + '''
<!-- emolevy -->
<rect x="100" y="150" width="250" height="300" rx="10" fill="#0d1218" stroke="rgba(148,178,210,.14)"/>
<g fill="rgba(148,178,210,.12)"><rect x="275" y="176" width="8" height="90" rx="2"/><rect x="290" y="176" width="8" height="90" rx="2"/><rect x="305" y="176" width="8" height="90" rx="2"/><rect x="320" y="176" width="8" height="90" rx="2"/></g>
<!-- CPU-blokki -->
<circle cx="195" cy="222" r="70" fill="url(#hg-glow)"/>
<rect x="155" y="182" width="80" height="80" rx="14" fill="#141b24" stroke="rgba(148,178,210,.3)" stroke-width="1.5"/>
<rect x="170" y="197" width="50" height="50" rx="25" fill="none" stroke="url(#hg-cool)" stroke-width="3"/>
<circle cx="195" cy="222" r="10" fill="rgba(34,199,232,.35)"/>
<!-- GPU + blokki -->
<rect x="112" y="320" width="300" height="62" rx="10" fill="#131a23" stroke="rgba(148,178,210,.28)" stroke-width="1.5"/>
<rect x="128" y="332" width="200" height="38" rx="8" fill="#0b1016" stroke="rgba(34,199,232,.35)"/>
<path d="M142 351h170" stroke="url(#hg-cool)" stroke-width="3" stroke-linecap="round" opacity=".8"/>
<text x="364" y="345" fill="rgba(148,178,210,.55)" font-family="Inter,Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="2">GPU</text>
<!-- pumppu/säiliö -->
<rect x="410" y="170" width="54" height="170" rx="16" fill="#0b1016" stroke="rgba(148,178,210,.3)" stroke-width="1.5"/>
<rect x="416" y="210" width="42" height="124" rx="12" fill="url(#hg-res)"/>
<rect x="410" y="170" width="54" height="170" rx="16" fill="url(#hg-glass)"/>
<rect x="404" y="344" width="66" height="40" rx="10" fill="#141b24" stroke="rgba(148,178,210,.3)" stroke-width="1.5"/>
<circle cx="437" cy="364" r="11" fill="none" stroke="url(#hg-cool)" stroke-width="2.5"/>
<!-- letkut -->
<g fill="none" stroke-linecap="round" stroke-linejoin="round">
 <path id="t1" d="M437 170 V140 Q437 128 425 128 H440 Q452 128 452 118" stroke="rgba(34,199,232,.25)" stroke-width="10"/>
 <path d="M210 182 V145 Q210 130 225 130 H440 Q455 130 455 118" stroke="rgba(34,199,232,.22)" stroke-width="10"/>
 <path d="M180 182 V150 Q180 120 110 120 V118" stroke="rgba(34,199,232,.22)" stroke-width="10"/>
 <path d="M404 364 H380 Q360 364 360 351 H328" stroke="rgba(34,199,232,.22)" stroke-width="10"/>
 <path d="M128 351 Q100 351 100 310 V280 Q100 262 140 262 H160" stroke="rgba(34,199,232,.22)" stroke-width="10"/>
 <path d="M210 182 V145 Q210 130 225 130 H440 Q455 130 455 118" stroke="url(#hg-cool)" stroke-width="3" class="flow"/>
 <path d="M180 182 V150 Q180 120 110 120 V118" stroke="url(#hg-cool)" stroke-width="3" class="flow"/>
 <path d="M404 364 H380 Q360 364 360 351 H328" stroke="url(#hg-cool)" stroke-width="3" class="flow"/>
 <path d="M128 351 Q100 351 100 310 V280 Q100 262 140 262 H160" stroke="url(#hg-cool)" stroke-width="3" class="flow"/>
</g>
<!-- tunnisteet -->
<g font-family="Inter,Arial,sans-serif" font-size="11" font-weight="600" fill="#9aa8b8">
 <text x="92" y="142">RADIATORI 360 MM</text>
 <text x="248" y="276">CPU-VESIBLOKKI</text>
 <text x="400" y="404">PUMPPU / SÄILIÖ</text>
 <text x="112" y="404">GPU-VESIBLOKKI</text>
</g>
<rect x="58" y="38" width="444" height="444" rx="16" fill="url(#hg-glass)"/>
</svg>'''

# ---------------------------------------------------------------- osiot
def basics_section():
    cards = "".join(f'<div class="card reveal"><div class="card-icon">{ICONS[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in BASICS)
    return section(
        head("Perusteet", "Mikä on vesijäähdytys?",
             "Vesijäähdytyksessä tietokoneen komponenttien tuottama lämpö siirretään nesteen avulla jäähdyttimeen, jossa lämpö poistetaan ilman avulla. Järjestelmä koostuu tyypillisesti vesiblokista, pumpusta, jäähdyttimestä, tuulettimista ja nesteestä.")
        + '<div class="grid grid-4">' + cards[:0] + "".join(
            f'<div class="card reveal"><div class="card-icon">{ICONS[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in BASICS[:4]) + '</div>'
        + '<div class="grid grid-3 mt-2">' + "".join(
            f'<div class="card reveal"><div class="card-icon">{ICONS[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in BASICS[4:]) + '</div>'
        + '<p class="mt-2"><a class="btn btn-ghost" href="/vesijaahdytys">Lue lisää vesijäähdytyksestä →</a></p>',
        id_="mika")

def versus_section(alt=True):
    aio = '''<div class="card reveal"><span class="versus-badge">All-in-One</span><h3>AiO-vesijäähdytys</h3>
<p class="muted">AiO on valmiiksi koottu ja suljettu järjestelmä. Pumppu, CPU-vesiblokki, letkut, jäähdytin, tuulettimet ja neste tulevat samassa paketissa – asennus muistuttaa ilmajäähdyttimen asentamista.</p>
<div class="chips"><span class="tag">Pumppu</span><span class="tag">CPU-vesiblokki</span><span class="tag">Letkut</span><span class="tag">Jäähdytin</span><span class="tag">Tuulettimet</span><span class="tag">Neste</span></div>
<div class="split"><div><h4>Hyödyt</h4><ul class="pros"><li>Helppo asentaa</li><li>Vähän huoltoa</li><li>Hyvä jäähdytysteho</li><li>Siisti ulkonäkö</li><li>Sopii aloittelijalle</li></ul></div>
<div><h4>Haitat</h4><ul class="cons"><li>Yleensä CPU-painotteinen</li><li>Rajalliset muokkausmahdollisuudet</li><li>Käyttöikä riippuu tuotteesta</li><li>Pumppu voi rikkoutua</li></ul></div></div>
<p class="price-chip mt-2">Tyypillisesti noin 50–300 € <small>suuntaa-antava</small></p>
<p class="mt-2"><a href="/aio">Kaikki AiO:sta →</a></p></div>'''
    cl = '''<div class="card reveal"><span class="versus-badge">Avoin vesijäähdytys</span><h3>Custom loop</h3>
<p class="muted">Custom loop rakennetaan erillisistä komponenteista. Jokainen osa valitaan itse, ja samaan kiertoon voidaan liittää sekä prosessori että näytönohjain.</p>
<div class="chips"><span class="tag">CPU-blokki</span><span class="tag">GPU-blokki</span><span class="tag">Pumppu</span><span class="tag">Säiliö</span><span class="tag">Radiatori</span><span class="tag">Letkut</span><span class="tag">Liittimet</span><span class="tag">Neste</span></div>
<div class="split"><div><h4>Hyödyt</h4><ul class="pros"><li>Erittäin tehokas</li><li>CPU ja GPU samalla loopilla</li><li>Ulkonäköä voi muokata</li><li>Suuri määrä komponenttivaihtoehtoja</li></ul></div>
<div><h4>Haitat</h4><ul class="cons"><li>Kallis</li><li>Vaikeampi rakentaa</li><li>Vaatii enemmän suunnittelua</li><li>Huoltoa tarvitaan</li><li>Vuotoriski on olemassa</li></ul></div></div>
<p class="price-chip mt-2">Tyypillisesti noin 250–1 000+ € <small>suuntaa-antava</small></p>
<p class="mt-2"><a href="/custom-loop">Kaikki custom loopista →</a></p></div>'''
    return section(head("Vertailu", "AiO vs custom loop", "Kaksi hyvin erilaista tapaa vesijäähdyttää tietokone. Kumpikaan ei ole kaikille oikea valinta – ratkaisevaa on käyttötarkoitus, budjetti ja se, kuinka paljon haluat rakentaa itse.")
                   + f'<div class="versus">{aio}{cl}</div>', alt=alt, id_="vertailu")

def price_tables():
    aio_rows = [("Edullinen 120/240 mm", "noin 50–90 €"), ("Keskitaso 240/280 mm", "noin 80–130 €"), ("Tehokas 360 mm", "noin 100–170 €"), ("Premium AiO", "noin 150–300+ €")]
    cl_rows = [("CPU-vesiblokki", "50–150 €"), ("GPU-vesiblokki", "100–250+ €"), ("Pumppu", "70–150 €"), ("Säiliö", "40–120 €"), ("Jäähdytin", "50–150 €"), ("Tuulettimet", "30–150 €"), ("Letkut", "10–40 €"), ("Liittimet", "30–150+ €"), ("Jäähdytysneste", "10–30 €")]
    t1 = '<div class="table-wrap reveal"><table><caption>AiO-vesijäähdytys</caption><thead><tr><th scope="col">Luokka</th><th scope="col" class="num">Tyypillinen hinta</th></tr></thead><tbody>' + "".join(f'<tr><td>{a}</td><td class="num">{b}</td></tr>' for a, b in aio_rows) + '</tbody></table></div>'
    t2 = '<div class="table-wrap reveal"><table><caption>Custom loop</caption><thead><tr><th scope="col">Komponentti</th><th scope="col" class="num">Tyypillinen hintaluokka</th></tr></thead><tbody>' + "".join(f'<tr><td>{a}</td><td class="num">{b}</td></tr>' for a, b in cl_rows) + '</tbody></table></div>'
    return f'<div class="grid grid-2">{t1}{t2}</div>' + infobox("<strong>Hinnat ovat suuntaa-antavia ja vaihtelevat valmistajan, koon, mallin ja jälleenmyyjän mukaan.</strong> " + PRICE_NOTE + " Hinnat eivät ole reaaliaikaisia.")

def prices_section(alt=False):
    return section(head("Hinnat", "Mitä vesijäähdytys maksaa?", "Alla tyypilliset hintaluokat Suomessa. Ne auttavat hahmottamaan budjettia – eivät lupaa tiettyä hintaa tietylle tuotteelle.") + price_tables(), alt=alt, id_="hinnat")

def calculator(id_="laskuri", alt=True):
    aio_opts = "".join(
        f'<label class="opt"><input type="radio" name="aio-size" data-set="aio" data-key="{s}"{" checked" if s=="360" else ""}><span class="opt-body"><span class="opt-name">{s} mm</span><span class="opt-price"></span></span><span class="check"></span></label>'
        for s in ["120", "240", "280", "360", "420"])
    cl_items = [("cpu", "CPU-vesiblokki", True), ("gpu", "GPU-vesiblokki", False), ("pumpres", "Pumppu/säiliö", True), ("rad360", "Radiatori 360 mm", True), ("rad420", "Radiatori 420 mm", False), ("fans", "Tuulettimet", True), ("tubes", "Letkut", True), ("fittings", "Liittimet", True), ("coolant", "Neste", True)]
    cl_opts = "".join(
        f'<label class="opt"><input type="checkbox" data-set="custom" data-key="{k}"{" checked" if c else ""}><span class="opt-body"><span class="opt-name">{n}</span><span class="opt-price"></span></span><span class="check"></span></label>'
        for k, n, c in cl_items)
    inner = head("Hintalaskuri", "Paljonko oma vesijäähdytys maksaisi?", "Valitse jäähdytystapa ja osat. Laskuri näyttää suuntaa-antavan budjettihaarukan tyypillisten hintaluokkien perusteella.", h2id="laskuri-otsikko") + f'''
<div class="calc" data-calc>
  <div class="calc-panel reveal">
    <div class="seg" role="group" aria-label="Jäähdytystapa">
      <button type="button" data-mode="aio" aria-pressed="true">AiO</button>
      <button type="button" data-mode="custom" aria-pressed="false">Custom loop</button>
    </div>
    <div data-panel="aio"><fieldset class="fieldset"><legend>Radiatorin koko</legend><div class="opt-grid">{aio_opts}</div></fieldset></div>
    <div data-panel="custom" hidden><fieldset class="fieldset"><legend>Valitse loopin osat</legend><div class="opt-grid">{cl_opts}</div></fieldset>
      <p class="small muted">Vinkki: CPU+GPU-loopissa kaksi radiatoria (esim. 360 mm + 420 mm) on tavallinen ratkaisu.</p></div>
  </div>
  <aside class="calc-result reveal" aria-live="polite" aria-labelledby="laskuri-otsikko">
    <div class="label">Arvioitu kokonaisbudjetti</div>
    <div class="calc-total" data-total>– €</div>
    <div class="calc-mid" data-mid></div>
    <ul class="calc-lines" data-lines></ul>
    <p class="small muted" style="margin:0"><strong style="color:var(--text)">Kyseessä on arvio.</strong> Todellinen hinta riippuu valmistajasta, mallista, jälleenmyyjästä ja tarjouksista. Asennustarvikkeet, lämpötahna ja mahdolliset lisäosat eivät sisälly laskelmaan.</p>
  </aside>
</div>'''
    return section(inner, alt=alt, id_=id_)

def components_section(alt=False, full=False):
    cards = []
    for ic, name, what, why, note, price in COMPONENTS:
        if full:
            body = f'<ul class="def-list"><li><b>Mitä se tekee</b>{what}</li><li><b>Miksi sitä tarvitaan</b>{why}</li><li><b>Huomioi</b>{note}</li></ul><p class="price-chip">{price} <small>tyypillinen hintaluokka</small></p>'
        else:
            body = f'<p class="muted">{what}</p><p class="price-chip">{price} <small>tyypillisesti</small></p>'
        cards.append(f'<article class="card reveal"><div class="card-icon">{ICONS[ic]}</div><h3>{name}</h3>{body}</article>')
    more = "" if full else '<p class="mt-2"><a class="btn btn-ghost" href="/komponentit">Tutustu komponentteihin tarkemmin →</a></p>'
    return section(head("Komponentit", "Vesijäähdytyksen komponentit", "Jokaisella osalla on oma tehtävänsä. Kun tiedät mitä kukin osa tekee, on helpompi mitoittaa järjestelmä ja välttää yhteensopivuusongelmat.")
                   + '<div class="grid grid-3">' + "".join(cards) + '</div>' + more, alt=alt, id_="komponentit")

def rad_section(alt=True, more=True):
    cards = "".join(
        f'<div class="rad reveal"><div class="rad-bar{" big" if s in ("280 mm","420 mm") else ""}">{"<i></i>"*n}</div><b>{s}</b><p>{d}</p></div>'
        for s, n, d in RADS)
    link = '<p class="mt-2"><a class="btn btn-ghost" href="/komponentit#radiatorit">Lue radiatoriopas →</a></p>' if more else ""
    return section(head("Radiatorit", "Suositut radiatorikoot", "Suurempi radiatori tarjoaa yleensä enemmän pinta-alaa lämmön poistamiseen. Todellinen suorituskyky riippuu kuitenkin myös tuulettimista, radiatorin paksuudesta, kotelon ilmanvaihdosta ja lämpökuormasta.")
                   + f'<div class="rad-grid">{cards}</div>' + infobox("Isompi ei ole automaattisesti parempi: 360 mm:n radiatori ahtaassa kotelossa huonolla ilmanvaihdolla voi toimia heikommin kuin hyvin sijoitettu 280 mm:n malli.") + link,
                   alt=alt, id_="radiatorit")

def brands_grid(limit=None, full=False):
    items = BRANDS[:limit] if limit else BRANDS
    out = []
    for n, mono, d, tags in items:
        t = "".join(f'<span class="tag{" tag-muted" if tg=="Ilmajäähdytys" else ""}">{tg}</span>' for tg in tags)
        extra = '<p class="small muted mt-2" style="margin-bottom:0">Tuotteet ja hinnat lisätään myöhemmin.</p>' if full else ""
        out.append(f'<article class="card reveal"><div class="brand-head"><span class="brand-mono" aria-hidden="true">{mono}</span><h3>{n}</h3></div><p class="muted">{d}</p><div>{t}</div>{extra}</article>')
    return '<div class="grid grid-3">' + "".join(out) + '</div>'

def brands_section(alt=False):
    return section(head("Valmistajat", "Vesijäähdytyksen valmistajat", "Esittelemme valmistajat neutraalisti. Emme nimeä mitään merkkiä automaattisesti parhaaksi – sopiva valinta riippuu tarpeesta, kotelosta ja budjetista.")
                   + brands_grid(limit=9) + '<p class="mt-2"><a class="btn btn-ghost" href="/tuotemerkit">Kaikki valmistajat →</a></p>', alt=alt, id_="valmistajat")

def guide_cards(items):
    out = []
    for slug, title, desc, cat, ready in items:
        if ready:
            out.append(f'<article class="card article-card reveal"><span class="tag">{cat}</span><h3><a href="/oppaat/{slug}">{title}</a></h3><p class="muted">{desc}</p><p class="meta">Päivitetty {UPDATED} · Lue opas →</p><a class="card-link" href="/oppaat/{slug}" aria-hidden="true" tabindex="-1"></a></article>')
        else:
            out.append(f'<article class="card article-card soon reveal"><span class="tag tag-muted">{cat}</span><h3>{title}</h3><p class="muted">{desc}</p><p class="meta">Tulossa pian</p></article>')
    return '<div class="grid grid-3">' + "".join(out) + '</div>'

def beginner_section(alt=True):
    steps = [
        ("Selvitä lämpökuorma", "Mitä jäähdytät? Pelkkä prosessori vai myös näytönohjain? Prosessorin kulutus kertoo, kuinka paljon jäähdytystä tarvitaan."),
        ("Valitse AiO tai custom loop", "Useimmille AiO on helpoin tapa aloittaa. Custom loop on projekti niille, jotka haluavat jäähdyttää myös GPU:n tai rakentaa itse."),
        ("Tarkista yhteensopivuus", "Varmista prosessorin socket-tuki ja kotelon radiatorituki: koko, paikka ja paksuus."),
        ("Asenna ja seuraa lämpötiloja", "Asenna huolella, kytke pumppu oikeaan liitäntään ja seuraa lämpötiloja kuormituksessa ensimmäisten päivien ajan."),
    ]
    lis = "".join(f'<li class="reveal"><h3>{a}</h3><p>{b}</p></li>' for a, b in steps)
    return section(head("Aloittelijalle", "Aloittelijan opas vesijäähdytykseen", "Neljä askelta, joilla pääset alkuun ilman turhia virheitä.")
                   + f'<ol class="steps two-col">{lis}</ol>'
                   + '<div class="btn-row mt-2"><a class="btn btn-primary" href="/oppaat/vesijaahdytys-aloittelijalle">Lue koko aloittelijan opas →</a><a class="btn btn-ghost" href="/aio#asennus">AiO-asennusopas</a></div>',
                   alt=alt, id_="aloittelijalle")

def proscons_section(alt=False):
    return section(head("Hyödyt ja haitat", "Kannattaako vesijäähdytys?", "Vesijäähdytys ei ole ilmajäähdytystä automaattisesti parempi. Punnitse hyötyjä ja haittoja oman kokoonpanosi kannalta.")
                   + '''<div class="grid grid-2">
<div class="card reveal"><h3>Hyödyt</h3><ul class="pros"><li>Tehokas lämmönhallinta</li><li>Mahdollisesti pienempi melutaso</li><li>Hyvä suorituskyky suurella lämpökuormalla</li><li>Premium-ulkonäkö ja tilaa prosessorin ympärillä</li><li>Custom loop mahdollistaa CPU:n ja GPU:n jäähdytyksen</li></ul></div>
<div class="card reveal"><h3>Haitat</h3><ul class="cons"><li>Korkeampi hinta</li><li>Monimutkaisempi asennus</li><li>Pumppuun liittyvä vikaantumisriski</li><li>AiO:n rajallinen käyttöikä</li><li>Custom loop vaatii huoltoa</li><li>Vuotoriski custom loopissa</li></ul></div>
</div>''', alt=alt, id_="hyodyt")

def temps_block():
    temps = [
        ("Idle", "Kevyt käyttö", "Selaimen ja työpöydän käytössä lämpötilat ovat tyypillisesti lähellä huoneenlämpöä + joitakin kymmeniä asteita. Lukemat vaihtelevat prosessorin virransäästöominaisuuksien mukaan."),
        ("Pelikuorma", "Gaming", "Pelatessa näytönohjain on yleensä lämpimin komponentti. Prosessorin lämpötila riippuu pelistä ja siitä, kuinka paljon se kuormittaa CPU:ta."),
        ("Raskas kuorma", "Heavy load", "Renderöinti ja stressitestit nostavat kulutuksen maksimiin. Nykyprosessorit voivat tietoisesti ajaa lähellä lämpörajaansa ja säätää kellotaajuuksiaan."),
        ("CPU-lämpötila", "Prosessori", "Turvallinen raja riippuu mallista – tarkista valmistajan ilmoittama suurin sallittu lämpötila (esim. Tjmax). Lämpötila heilahtelee nopeasti kuorman mukaan."),
        ("GPU-lämpötila", "Näytönohjain", "Seuraa sekä ydinlämpöä että hotspot-lukemaa. Vesiblokilla ero voi pienentyä, mutta raja-arvot ovat mallikohtaisia."),
        ("Nesteen lämpötila", "Coolant", "Kertoo, kuinka hyvin radiatorit poistavat lämpöä. Tyypillisesti seurataan eroa huoneenlämpöön (delta T) – pienempi ero tarkoittaa enemmän jäähdytysvaraa."),
    ]
    return '<div class="grid grid-3">' + "".join(
        f'<article class="card temp reveal"><div class="card-icon">{ICONS["temp"]}</div><span class="tag tag-muted">{b}</span><h3>{a}</h3><div class="temp-bar" aria-hidden="true"></div><p class="muted">{c}</p></article>'
        for a, b, c in temps) + '</div>' + infobox("Yhtä universaalia “turvallista lämpötilaa” ei ole. Turvalliset lämpötilat riippuvat komponentista, kuormasta, jännitteestä, ympäristön lämpötilasta ja kokoonpanosta. Tarkista aina oman prosessorisi ja näytönohjaimesi valmistajan tiedot.", "warn")

def noise_block():
    src = [("pump", "Pumppu", "Pumpun hurina tai surina, erityisesti täysillä kierroksilla tai jos kierrossa on ilmaa."),
           ("fan", "Tuulettimet", "Yleensä suurin melun lähde. Kierrosnopeus ja tuulettimen laatu ratkaisevat."),
           ("rad", "Ilman virtaus", "Tiheä radiatori ja rajoittava kotelon etupaneeli lisäävät ilmavirran ääntä."),
           ("sound", "Resonanssi", "Värinä voi siirtyä pumpusta tai tuulettimista koteloon. Kumityynyt ja oikea kiinnitys auttavat.")]
    return '<div class="grid grid-4">' + "".join(f'<div class="card reveal"><div class="card-icon">{ICONS[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in src) + '</div>' + infobox("Suurempi radiatori voi mahdollistaa tuulettimien ajamisen pienemmillä kierroksilla, mutta lopputulos riippuu koko järjestelmästä: tuulettimista, pumpusta, kotelosta ja käyttäjän säätämistä tuuletinkäyristä.")

# ================================================================== SIVUT
def build_index():
    hero = f'''<section class="hero"><div class="container hero-grid">
  <div>
    <span class="eyebrow">Suomalainen vesijäähdytyksen tietopankki</span>
    <h1>Vesijäähdytys tietokoneeseen – <span class="grad">kaikki mitä sinun tarvitsee tietää</span></h1>
    <p class="lead">Vesijäähdytys pitää tehokkaan tietokoneen viileänä ja voi mahdollistaa hiljaisemman sekä tehokkaamman kokoonpanon. Watercooling.fi auttaa sinua ymmärtämään, miten AiO- ja custom loop -vesijäähdytys toimivat, mitä ne maksavat ja mitä tarvitset oman järjestelmäsi rakentamiseen.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/vesijaahdytys">Tutustu vesijäähdytykseen</a><a class="btn btn-ghost" href="#hinnat">Katso hinnat</a></div>
    <div class="hero-stats"><div class="stat"><b>AiO</b><span>valmis ja suljettu</span></div><div class="stat"><b>Custom</b><span>avoin loop</span></div><div class="stat"><b>9</b><span>komponenttia selitettynä</span></div></div>
  </div>
  <div class="hero-visual">{HERO_SVG}</div>
</div></section>'''
    body = (hero + basics_section() + versus_section() + prices_section() + calculator()
            + components_section() + rad_section() + brands_section() + beginner_section()
            + proscons_section()
            + section(head("UKK", "Usein kysyttyä vesijäähdytyksestä") + faq_block(FAQ[:8]) + '<p class="mt-2"><a class="btn btn-ghost" href="/ukk">Kaikki kysymykset →</a></p>', alt=True, id_="ukk", narrow=True)
            + cta())
    page("index", "Vesijäähdytys tietokoneeseen – Oppaat, hinnat ja valmistajat | Watercooling.fi",
         "Watercooling.fi on suomalainen vesijäähdytyksen tietopankki. Tutustu AiO- ja custom loop -vesijäähdytykseen, komponentteihin, hintoihin, valmistajiin ja asennusoppaisiin.",
         body, "index", [faq_schema(FAQ[:8])])

def build_vesijaahdytys():
    trail = [("Etusivu", "/"), ("Vesijäähdytys", "/vesijaahdytys")]
    cpu = '''<div class="two-col-md"><div class="reveal">
<h3>Milloin AiO kannattaa?</h3><p class="muted">AiO on järkevä valinta, kun prosessori kuluttaa kuormassa paljon tehoa, kotelossa ei ole tilaa isolle tornijäähdyttimelle tai kun haluat siistin ilmeen ja vapaata tilaa muistien ympärille.</p>
<h3>Milloin ilmajäähdytin riittää?</h3><p class="muted">Keskitason ja monille tehokkaillekin prosessoreille laadukas ilmajäähdytin riittää hyvin. Se on yksinkertainen, edullinen ja siinä ei ole pumppua, joka voisi vikaantua. Vesijäähdytys ei ole aina parempi.</p>
<h3>Mitä TDP tarkoittaa?</h3><p class="muted">TDP (Thermal Design Power) kuvaa valmistajan määrittelemää lämpötehoa, jolle jäähdytys mitoitetaan. Todellinen kulutus voi kuormassa ylittää TDP-arvon selvästi, koska prosessorit tehostavat kellotaajuuksiaan, kun virta- ja lämpövara sallii.</p>
<h3>Miksi kulutus ratkaisee?</h3><p class="muted">Käytännössä lähes kaikki prosessorin käyttämä sähköteho muuttuu lämmöksi. Mitä enemmän wattia prosessori kuluttaa, sitä enemmän lämpöä jäähdytyksen on siirrettävä pois.</p>
</div><div class="reveal">
<h3>Socket-yhteensopivuus</h3><p class="muted">Vesiblokki kiinnitetään emolevyyn socketkohtaisella kiinnityssarjalla. Tarkista aina, että jäähdyttimen mukana tulee oikea kiinnike – tai että sen voi tilata valmistajalta.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Socket</th><th scope="col">Alusta</th><th scope="col">Huomioitavaa</th></tr></thead><tbody>
<tr><td><b>AM5</b></td><td>AMD Ryzen 7000 ja uudemmat</td><td>Käyttää emolevyn vakiotakalevyä; monet AM4-kiinnikkeet sopivat, tarkista valmistajalta.</td></tr>
<tr><td><b>LGA1700</b></td><td>Intel Core 12.–14. sukupolvi</td><td>Vaatii LGA1700-yhteensopivan kiinnityssarjan.</td></tr>
<tr><td><b>LGA1851</b></td><td>Intel Core Ultra 200S</td><td>Kiinnitysreiät yleensä samat kuin LGA1700:ssa; varmista valmistajan tuki.</td></tr>
</tbody></table></div></div></div>'''
    gpu_terms = [("GPU-vesiblokki", "Näytönohjaimen tehdasjäähdyttimen tilalle asennettava blokki, joka jäähdyttää grafiikkapiiriä nesteellä."),
                 ("Full-cover-blokki", "Peittää koko piirilevyn ja jäähdyttää grafiikkapiirin lisäksi muistit ja virransyötön. Suunniteltu tietylle piirilevymallille."),
                 ("VRAM", "Näytönohjaimen muistipiirit. Ne lämpenevät kuormassa ja tarvitsevat kontaktin blokkiin lämpötyynyjen avulla."),
                 ("VRM", "Näytönohjaimen virransyöttö, joka lämpenee erityisesti tehokkailla korteilla ja on siksi jäähdytettävä."),
                 ("GPU:n lämpötila", "Grafiikkapiirin keskimääräinen ydinlämpötila, jonka useimmat ohjelmat näyttävät oletuksena."),
                 ("Hotspot", "Piirin kuumimman kohdan lukema. Suuri ero ydinlämpöön voi viitata esimerkiksi huonoon kontaktiin tai epätasaiseen tahnaan."),
                 ("Backplate", "Kortin takapuolen levy, joka jäykistää piirilevyä ja voi osaltaan johtaa lämpöä pois muisteista ja virransyötöstä.")]
    gpu = '<div class="grid grid-3">' + "".join(f'<div class="card reveal"><h3>{a}</h3><p class="muted">{b}</p></div>' for a, b in gpu_terms) + '</div>' + infobox("Näytönohjaimen vesijäähdytys custom loopilla on huomattavasti monimutkaisempi projekti kuin tavallinen CPU:n AiO. Kortti puretaan, blokki asennetaan lämpötyynyjen kanssa ja kortti liitetään looppiin. Purkaminen voi vaikuttaa takuuseen – tarkista valmistajan ehdot.", "warn")
    body = (page_hero(trail, "Perusteet", "Vesijäähdytys – näin se toimii", "Mitä vesijäähdytys on, mistä osista se koostuu ja milloin siitä on oikeasti hyötyä. Selitämme perusteet aloittelijalle ymmärrettävästi – ilman myyntipuheita.")
            + basics_section().replace('<p class="mt-2"><a class="btn btn-ghost" href="/vesijaahdytys">Lue lisää vesijäähdytyksestä →</a></p>', "")
            + section(head("Prosessori", "CPU-vesijäähdytys", "Prosessorin vesijäähdytys on yleisin tapa aloittaa – useimmiten AiO:lla.") + cpu, alt=True, id_="cpu")
            + section(head("Näytönohjain", "GPU-vesijäähdytys", "Näytönohjain on pelikoneen suurin lämmönlähde. Sen vesijäähdyttäminen onnistuu, mutta vaatii osaamista.") + gpu, id_="gpu")
            + section(head("Lämpötilat", "Vesijäähdytyksen lämpötilat", "Mitä lukemia kannattaa seurata ja miten niitä tulkitaan.") + temps_block(), alt=True, id_="lampotilat")
            + section(head("Melu", "Onko vesijäähdytys hiljainen?", "Vesijäähdytys ei automaattisesti tarkoita hiljaisuutta. Melu voi syntyä useasta lähteestä.") + noise_block(), id_="melu")
            + versus_section(alt=True) + proscons_section() + cta())
    page("vesijaahdytys", "Vesijäähdytys – näin tietokoneen vesijäähdytys toimii | Watercooling.fi",
         "Mitä vesijäähdytys on ja miten se toimii? CPU- ja GPU-vesijäähdytys, lämpötilat, melu sekä hyödyt ja haitat selitettynä selkeästi suomeksi.",
         body, "vesijaahdytys", [breadcrumb_schema(trail)])

def build_aio():
    trail = [("Etusivu", "/"), ("AiO", "/aio")]
    steps = [("Tarkista CPU-socket", "Varmista, että AiO:n mukana tulee kiinnityssarja prosessorisi socketille (esim. AM5, LGA1700 tai LGA1851)."),
             ("Tarkista kotelon radiatorituki", "Selvitä, mihin kohtaan (katto, etu, sivu) radiatori mahtuu, ja huomioi radiatorin ja tuulettimien yhteispaksuus."),
             ("Asenna backplate", "Asenna emolevyn taakse tarvittava takalevy tai käytä emolevyn omaa takalevyä ohjeen mukaan. AM5-alustalla käytetään yleensä vakiotakalevyä."),
             ("Asenna CPU block", "Poista suojakalvo blokin pohjasta. Levitä tarvittaessa lämpötahna ja kiristä ruuvit ristiin tasaisesti."),
             ("Asenna radiatori", "Kiinnitä radiatori koteloon. Sijoita pumppu mieluiten radiatorin yläreunaa alemmas, jotta ilma ei kerry pumppuun."),
             ("Asenna tuulettimet", "Päätä puhallussuunta (sisään tai ulos) ja huomioi kotelon ilmavirtaus kokonaisuutena."),
             ("Kytke pumppu", "Kytke pumppu emolevyn pumpulle tarkoitettuun liitäntään (usein AIO_PUMP tai PUMP_FAN) tai valmistajan ohjeen mukaan."),
             ("Kytke tuulettimet", "Kytke tuulettimet CPU_FAN-liitäntään tai tuuletinjakajaan ja säädä käyrä myöhemmin BIOSissa tai ohjelmistossa."),
             ("Kytke mahdollinen RGB", "Tarkista, onko liitäntä 5 V ARGB (3-pin) vai 12 V RGB (4-pin). Väärä liitäntä voi vahingoittaa valoja."),
             ("Käynnistä ja tarkista lämpötilat", "Tarkista BIOSista, että pumppu pyörii. Seuraa lämpötiloja kevyessä käytössä ja kuormassa.")]
    lis = "".join(f'<li class="reveal"><h3>{a}</h3><p>{b}</p></li>' for a, b in steps)
    choose = [("rad", "Radiatorin koko", "Valitse koko kotelon tuen ja prosessorin kulutuksen mukaan. 240–360 mm on yleisin haarukka."),
              ("pump", "Pumppu", "Pumpun ääni ja nopeudensäätö vaikuttavat melutasoon. Lue arvosteluista pumpun käyttäytymisestä."),
              ("fan", "Tuulettimet", "Hyvä staattinen paine ja säädettävyys ovat tärkeämpiä kuin maksimikierrokset."),
              ("shield", "Takuu", "Takuun pituus kertoo valmistajan luottamuksesta ja antaa suuntaa käyttöiästä."),
              ("cpu", "Socket-tuki", "Tarkista, että kiinnike sopii nykyiselle – ja mieluiten myös seuraavalle – alustallesi."),
              ("tube", "Letkun pituus", "Etupaneeliin asennettaessa letkujen täytyy riittää pumpulta radiatoriin.")]
    choose_html = '<div class="grid grid-3">' + "".join(f'<div class="card reveal"><div class="card-icon">{ICONS[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in choose) + '</div>'
    faq = [FAQ[2], FAQ[8], FAQ[9], FAQ[11]]
    body = (page_hero(trail, "All-in-One", "AiO-vesijäähdytys", "AiO on valmiiksi koottu ja suljettu vesijäähdytin. Se on helpoin tapa ottaa vesijäähdytys käyttöön – tässä kaikki mitä tarvitset valintaan ja asennukseen.")
            + section(head("Valinta", "Mitä AiO:ssa kannattaa katsoa?", "AiO:t eroavat toisistaan erityisesti radiatorin koon, pumpun, tuulettimien ja ohjelmistojen osalta.") + choose_html, id_="valinta")
            + rad_section(alt=True, more=False)
            + section(head("Asennusopas", "Näin asennat AiO-vesijäähdytyksen", "Aloittelijalle sopiva vaiheittainen ohje. Noudata aina myös valmistajan omaa asennusohjetta.") + f'<ol class="steps two-col">{lis}</ol>' + infobox("Muista poistaa suojakalvo vesiblokin pohjasta ennen asennusta. Se on yksi yleisimmistä – ja helpoimmin vältettävistä – virheistä."), id_="asennus")
            + section(head("Hinnat", "AiO:n hintaluokat") + price_tables(), alt=True)
            + section(head("UKK", "Kysymyksiä AiO:sta") + faq_block(faq), narrow=True)
            + cta())
    page("aio", "AiO-vesijäähdytys – valinta, koot ja asennusopas | Watercooling.fi",
         "AiO-vesijäähdytys selitettynä: mitä valita, mikä radiatorikoko (240 mm, 280 mm, 360 mm) sopii ja miten AiO asennetaan vaihe vaiheelta.",
         body, "aio", [breadcrumb_schema(trail), faq_schema(faq)])

def build_custom_loop():
    trail = [("Etusivu", "/"), ("Custom Loop", "/custom-loop")]
    steps = [("Suunnittele loop", "Päätä mitä jäähdytät (CPU, GPU vai molemmat), budjetti ja tyyli: joustava letku vai kovaputki."),
             ("Tarkista kotelon yhteensopivuus", "Selvitä radiatoripaikat, paksuusrajat sekä pumppu-säiliöyhdistelmän kiinnitysvaihtoehdot."),
             ("Valitse radiatori", "Mitoita radiatoripinta-ala lämpökuorman mukaan. CPU+GPU-loopissa käytetään usein kahta radiatoria."),
             ("Valitse CPU/GPU-blokit", "Tarkista CPU-blokin socket-tuki ja GPU-blokin yhteensopivuus juuri sinun näytönohjaimesi piirilevyn kanssa."),
             ("Valitse pumppu ja säiliö", "Pumppu-säiliöyhdistelmä helpottaa asennusta. Sijoita säiliö niin, että pumppu saa nesteen painovoimaisesti."),
             ("Valitse letkut ja liittimet", "Varmista, että letkun sisä- ja ulkohalkaisija vastaavat liittimiä. Varaa muutama ylimääräinen liitin."),
             ("Suunnittele loopin reitti", "Järjestyksellä ei ole suurta merkitystä lämpötiloihin, kunhan säiliö on ennen pumppua. Suosi selkeitä ja lyhyitä reittejä."),
             ("Asenna komponentit", "Asenna blokit, radiatorit ja pumppu. Kiristä liittimet käsin – älä käytä työkaluja ylikiristykseen."),
             ("Täytä järjestelmä", "Täytä säiliön kautta ja käytä pumppua lyhyissä jaksoissa. Älä anna pumpun käydä kuivana."),
             ("Tee vuototesti", "Aja pumppua erillisellä virtalähteen hyppylangalla tai testerillä vähintään useita tunteja ilman, että muut komponentit saavat virtaa. Tarkista liitokset paperilla."),
             ("Käynnistä järjestelmä", "Kun loop on tiivis ja ilmat poistettu, kytke virrat koko koneeseen ja tarkista pumpun sekä tuulettimien toiminta."),
             ("Seuraa lämpötiloja", "Seuraa CPU-, GPU- ja nesteen lämpötiloja. Ilmaa poistuu vielä ensimmäisten päivien aikana – täydennä nestettä tarvittaessa.")]
    lis = "".join(f'<li class="reveal"><h3>{a}</h3><p>{b}</p></li>' for a, b in steps)
    maint = '''<div class="grid grid-3">
<div class="card reveal"><div class="card-icon">'''+ICONS["drop"]+'''</div><h3>Nesteen vaihto</h3><p class="muted">Valmistajat suosittelevat nesteen vaihtoa tyypillisesti noin 6–24 kuukauden välein nesteestä riippuen. Värilliset ja läpikuultamattomat nesteet vaativat useammin huoltoa.</p></div>
<div class="card reveal"><div class="card-icon">'''+ICONS["rad"]+'''</div><h3>Pölyn puhdistus</h3><p class="muted">Radiatorien lamellit keräävät pölyä. Puhdista ne säännöllisesti paineilmalla tai pehmeällä harjalla.</p></div>
<div class="card reveal"><div class="card-icon">'''+ICONS["shield"]+'''</div><h3>Tarkastukset</h3><p class="muted">Tarkista nesteen määrä, väri ja liitokset silloin tällöin. Sameus tai kasvusto kertoo, että loop kaipaa puhdistusta.</p></div>
</div>'''
    faq = [FAQ[3], FAQ[13], FAQ[14], FAQ[17], FAQ[19]]
    body = (page_hero(trail, "Avoin vesijäähdytys", "Custom loop – avoin vesijäähdytys", "Custom loop kootaan erillisistä osista ja voi jäähdyttää sekä prosessorin että näytönohjaimen. Tämä opas käy läpi suunnittelun, osat ja rakentamisen vaihe vaiheelta.")
            + section(infobox("<strong>Custom loop vaatii huolellista asennusta. Älä käynnistä tietokonetta ennen kuin olet varmistanut, että järjestelmä on tiivis.</strong>", "warn"), narrow=True)
            + section(head("Opas", "Custom loop vaihe vaiheelta", "12 vaihetta ensimmäisestä suunnitelmasta valmiiseen, tiiviiseen looppiin.") + f'<ol class="steps two-col">{lis}</ol>', id_="opas")
            + components_section(alt=True)
            + section(head("Huolto", "Custom loopin huolto", "Avoin vesijäähdytys vaatii säännöllistä, mutta ei raskasta huoltoa.") + maint, id_="huolto")
            + calculator(id_="laskuri", alt=True)
            + section(head("UKK", "Kysymyksiä custom loopista") + faq_block(faq), narrow=True)
            + cta())
    page("custom-loop", "Custom loop – avoin vesijäähdytys vaihe vaiheelta | Watercooling.fi",
         "Custom loop -opas: suunnittelu, kotelon yhteensopivuus, radiatorit, blokit, pumppu, täyttö ja vuototesti. Suuntaa-antavat hinnat ja huolto-ohjeet.",
         body, "custom-loop", [breadcrumb_schema(trail), faq_schema(faq)])

def build_komponentit():
    trail = [("Etusivu", "/"), ("Komponentit", "/komponentit")]
    rad_guide = '''<div class="two-col-md mt-3"><div class="prose reveal">
<h3>Mikä radiatori kannattaa valita?</h3>
<p>Suurempi radiatori tarjoaa yleensä enemmän pinta-alaa lämmön poistamiseen. Todellinen suorituskyky riippuu kuitenkin myös tuulettimista, radiatorin paksuudesta, kotelon ilmanvaihdosta ja lämpökuormasta.</p>
<h3>Paksuus ja lamellitiheys</h3>
<p>Paksumpi radiatori (esim. 45–60 mm) sisältää enemmän pinta-alaa samalla leveydellä, mutta vie tilaa ja voi osua emolevyn komponentteihin. Tiheä lamellitus toimii parhaiten nopeampien, staattiselta paineeltaan hyvien tuulettimien kanssa, kun taas harvempi lamellitus sopii hiljaisiin kokoonpanoihin.</p>
<h3>Sijoitus kotelossa</h3>
<p>Etu-, katto- ja sivupaikoilla on kaikilla puolensa. Etuasennuksessa radiatori saa viileää ulkoilmaa, mutta lämmin ilma kulkee koteloon. Kattoasennus puhaltaa lämmön ulos, mutta käyttää kotelon sisällä jo lämmennyttä ilmaa.</p>
</div><div class="reveal"><div class="table-wrap"><table><thead><tr><th scope="col">Koko</th><th scope="col">Tuulettimet</th><th scope="col">Tyypillinen käyttö</th></tr></thead><tbody>
<tr><td><b>120 mm</b></td><td>1 × 120</td><td>Pienet kotelot, kevyt kuorma</td></tr>
<tr><td><b>240 mm</b></td><td>2 × 120</td><td>Keskitason prosessorit</td></tr>
<tr><td><b>280 mm</b></td><td>2 × 140</td><td>Tehokkaammat prosessorit, hiljaisuus</td></tr>
<tr><td><b>360 mm</b></td><td>3 × 120</td><td>Tehokkaat prosessorit, CPU+GPU-loop</td></tr>
<tr><td><b>420 mm</b></td><td>3 × 140</td><td>Suuri lämpökuorma, isot kotelot</td></tr>
</tbody></table></div></div></div>'''
    body = (page_hero(trail, "Komponentit", "Vesijäähdytyksen komponentit", "Yhdeksän osaa, joista vesijäähdytys rakentuu. Kerromme mitä kukin tekee, miksi sitä tarvitaan, mitä kannattaa huomioida ja mitä se tyypillisesti maksaa.")
            + components_section(full=True).replace('<div class="section-head reveal"><span class="eyebrow">Komponentit</span><h2>Vesijäähdytyksen komponentit</h2>', '<div class="section-head reveal"><span class="eyebrow">Osat</span><h2>Komponentit yksitellen</h2>')
            + section(infobox(PRICE_NOTE), narrow=True)
            + rad_section(alt=True, more=False).replace('</div></section>', rad_guide + '</div></section>', 1)
            + section(head("Yhteensopivuus", "Yhteensopivuuden tarkistuslista") + '''<ul class="list-check reveal">
<li>CPU-blokin kiinnike sopii prosessorisi socketiin (AM5, LGA1700, LGA1851 …).</li>
<li>GPU-blokki on tehty juuri sinun näytönohjaimesi piirilevylle (referenssi vai valmistajan oma malli).</li>
<li>Kotelo tukee valitsemaasi radiatorikokoa ja -paksuutta halutussa paikassa.</li>
<li>Letkujen ja liittimien halkaisijat vastaavat toisiaan (esim. 10/13 mm, 10/16 mm tai 16 mm kovaputki).</li>
<li>Kierteet ovat yhteensopivia – vesijäähdytyksessä vakiona G1/4".</li>
<li>Loopissa ei sekoiteta alumiinia ja kuparia korroosion välttämiseksi.</li>
<li>Pumpulle ja tuulettimille on riittävästi liitäntöjä emolevyllä tai ohjaimessa.</li>
</ul>''', id_="yhteensopivuus", narrow=True)
            + cta())
    page("komponentit", "Vesijäähdytyksen komponentit – vesiblokki, radiatori, pumppu | Watercooling.fi",
         "Vesijäähdytyksen komponentit selitettynä: CPU- ja GPU-vesiblokki, radiatori, pumppu, säiliö, tuulettimet, letkut, liittimet ja jäähdytysneste hintaluokkineen.",
         body, "komponentit", [breadcrumb_schema(trail)])

def build_hinnat():
    trail = [("Etusivu", "/"), ("Hinnat", "/hinnat")]
    budgets = [("AiO – perustaso", "noin 50–110 €", "120–240 mm AiO keskitason prosessorille."),
               ("AiO – tehokas", "noin 100–220 €", "360–420 mm AiO suuremmalle lämpökuormalle."),
               ("Custom loop – CPU", "noin 250–600 €", "Blokki, pumppu/säiliö, yksi radiatori, letkut, liittimet ja neste."),
               ("Custom loop – CPU + GPU", "noin 400–1 000+ €", "Kaksi blokkia, yleensä kaksi radiatoria ja enemmän liittimiä.")]
    cards = '<div class="grid grid-4">' + "".join(f'<article class="card reveal"><div class="card-icon">{ICONS["euro"]}</div><h3>{a}</h3><p class="calc-total" style="font-size:1.5rem">{b}</p><p class="muted">{c}</p></article>' for a, b, c in budgets) + '</div>'
    faq = [FAQ[4], FAQ[14]]
    body = (page_hero(trail, "Hinnat", "Vesijäähdytyksen hinta", "Mitä vesijäähdytys maksaa Suomessa? Kokosimme tyypilliset hintaluokat AiO:lle ja custom loopin komponenteille sekä hintalaskurin oman budjetin arviointiin.")
            + section(head("Budjetit", "Tyypilliset kokonaisbudjetit", "Suuntaa-antavat haarukat eri kokoonpanoille.") + cards + infobox(PRICE_NOTE), id_="budjetit")
            + section(head("Hintaluokat", "Mitä vesijäähdytys maksaa?", "Tyypilliset hintaluokat komponenteittain.") + price_tables(), alt=True, id_="hinnat")
            + calculator(alt=False)
            + section(head("Tulossa", "Tuotekohtaiset hinnat", "Myöhemmin sivustolle voidaan lisätä tuotekohtaisia hintatietoja suomalaisilta jälleenmyyjiltä. Hinnat näytetään silloin aina päivämäärän ja lähteen kanssa.") + infobox("Emme esitä hintoja reaaliaikaisina. Kaikki tämän sivun luvut ovat suuntaa-antavia hintaluokkia."), alt=True, narrow=True)
            + section(faq_block(faq), narrow=True)
            + cta())
    page("hinnat", "Vesijäähdytys hinta – AiO ja custom loop hinnat | Watercooling.fi",
         "Paljonko vesijäähdytys maksaa? Suuntaa-antavat hintaluokat AiO-jäähdyttimille ja custom loopin komponenteille sekä hintalaskuri oman budjetin arvioimiseen.",
         body, "hinnat", [breadcrumb_schema(trail), faq_schema(faq)])

def build_tuotemerkit():
    trail = [("Etusivu", "/"), ("Tuotemerkit", "/tuotemerkit")]
    body = (page_hero(trail, "Valmistajat", "Vesijäähdytyksen valmistajat", "Esittelemme vesijäähdytystuotteita valmistavat merkit neutraalisti. Emme järjestä valmistajia paremmuusjärjestykseen – sopiva merkki riippuu tarpeesta, kotelosta ja budjetista.")
            + section(brands_grid(full=True) + infobox("Valmistajien tuotevalikoimat muuttuvat. Tarkista ajantasaiset mallit ja socket-tuki aina valmistajan omilta sivuilta."), id_="valmistajat")
            + cta("Mikä jäähdytin sopii sinulle?", "Ennen merkin valintaa kannattaa päättää jäähdytystapa ja koko. Aloita vertailusta tai laske budjetti.", ("AiO vs custom loop", "/#vertailu"), ("Avaa hintalaskuri", "/hinnat#laskuri")))
    items = {"@type": "ItemList", "name": "Vesijäähdytyksen valmistajat", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Brand", "name": b[0]}} for i, b in enumerate(BRANDS)]}
    page("tuotemerkit", "Vesijäähdytyksen valmistajat – Arctic, Corsair, NZXT, EKWB … | Watercooling.fi",
         "Vesijäähdytyksen valmistajat esiteltynä neutraalisti: Arctic, Corsair, NZXT, ASUS ROG, Cooler Master, be quiet!, Alphacool, EKWB, Thermaltake ja muut.",
         body, "tuotemerkit", [breadcrumb_schema(trail), items])

def build_oppaat():
    trail = [("Etusivu", "/"), ("Oppaat", "/oppaat")]
    body = (page_hero(trail, "Oppaat", "Vesijäähdytyksen oppaat", "Käytännönläheisiä oppaita aloittelijoille ja kokeneemmille rakentajille. Uusia artikkeleita julkaistaan jatkuvasti.")
            + section(guide_cards(GUIDES), id_="artikkelit")
            + cta())
    page("oppaat", "Vesijäähdytyksen oppaat – AiO, custom loop ja asennus | Watercooling.fi",
         "Vesijäähdytyksen oppaat suomeksi: vesijäähdytys aloittelijalle, AiO vai ilmajäähdytys, radiatorikoot, custom loop ja yleisimmät virheet.",
         body, "oppaat", [breadcrumb_schema(trail)])

def build_ukk():
    trail = [("Etusivu", "/"), ("UKK", "/ukk")]
    body = (page_hero(trail, "UKK", "Usein kysytyt kysymykset vesijäähdytyksestä", "Vastaukset yleisimpiin vesijäähdytystä koskeviin kysymyksiin – hinnoista ja turvallisuudesta radiatorikokoihin ja huoltoon.")
            + section(faq_block(FAQ), narrow=True, id_="kysymykset")
            + cta("Etkö löytänyt vastausta?", "Lue aloittelijan opas tai tutustu komponentteihin tarkemmin.", ("Aloittelijan opas", "/oppaat/vesijaahdytys-aloittelijalle"), ("Komponentit", "/komponentit")))
    page("ukk", "UKK – usein kysyttyä vesijäähdytyksestä | Watercooling.fi",
         "Vastaukset yleisimpiin kysymyksiin vesijäähdytyksestä: onko se parempi kuin ilmajäähdytys, voiko se vuotaa, kuinka kauan AiO kestää ja mitä custom loop maksaa.",
         body, "ukk", [breadcrumb_schema(trail), faq_schema(FAQ)])

def build_article():
    """Artikkelipohja (ArticleCard -> artikkelisivu). Kopioi tämä uusille oppaille."""
    slug = "vesijaahdytys-aloittelijalle"
    title = "Vesijäähdytys aloittelijalle"
    trail = [("Etusivu", "/"), ("Oppaat", "/oppaat"), (title, f"/oppaat/{slug}")]
    toc = [("toimintaperiaate", "Miten vesijäähdytys toimii?"), ("aio-vai-custom", "AiO vai custom loop?"), ("tarvitsetko", "Tarvitsetko vesijäähdytyksen?"), ("hinta", "Mitä aloittaminen maksaa?"), ("virheet", "Aloittelijan yleisimmät virheet"), ("ukk", "Usein kysyttyä")]
    faq = [FAQ[1], FAQ[6], FAQ[19]]
    prose = f'''<h2 id="toimintaperiaate">Miten vesijäähdytys toimii?</h2>
<p>Vesijäähdytyksessä lämpö kulkee kolmen vaiheen kautta. Ensin <b>vesiblokki</b> johtaa lämmön prosessorista tai näytönohjaimesta nesteeseen. Sitten <b>pumppu</b> kierrättää lämmenneen nesteen <b>radiatoriin</b>. Lopuksi tuulettimet puhaltavat ilmaa radiatorin lamellien läpi, ja lämpö siirtyy ilmaan.</p>
<p>Neste siis ei itsessään "jäähdytä" mitään – se toimii tehokkaana kuljettimena, joka siirtää lämmön paikkaan, josta sen voi poistaa suurelta pinta-alalta.</p>
{infobox("Vesi johtaa lämpöä huomattavasti paremmin kuin ilma, ja sillä on suuri lämpökapasiteetti. Siksi nestekierto voi tasoittaa lyhyitä lämpöpiikkejä.")}
<h3>Järjestelmän osat lyhyesti</h3>
<ul><li><b>Vesiblokki</b> – kosketuksessa komponenttiin</li><li><b>Pumppu</b> – pitää nesteen liikkeessä</li><li><b>Radiatori ja tuulettimet</b> – poistavat lämmön</li><li><b>Letkut ja liittimet</b> – yhdistävät osat</li><li><b>Jäähdytysneste</b> – kuljettaa lämmön</li></ul>
<h2 id="aio-vai-custom">AiO vai custom loop?</h2>
<p>Aloittelijalle AiO on lähes aina helpoin tapa kokeilla vesijäähdytystä. Se on tehtaalla koottu, täytetty ja suljettu, joten sinun tarvitsee vain kiinnittää blokki prosessoriin ja radiatori koteloon.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Ominaisuus</th><th scope="col">AiO</th><th scope="col">Custom loop</th></tr></thead><tbody>
<tr><td>Asennus</td><td>Helppo</td><td>Vaativa</td></tr>
<tr><td>Huolto</td><td>Vähäinen</td><td>Säännöllinen</td></tr>
<tr><td>Jäähdytettävät osat</td><td>Yleensä CPU</td><td>CPU ja GPU</td></tr>
<tr><td>Muokattavuus</td><td>Rajallinen</td><td>Laaja</td></tr>
<tr><td>Hinta (suuntaa-antava)</td><td>noin 50–300 €</td><td>noin 250–1 000+ €</td></tr>
</tbody></table></div>
<h2 id="tarvitsetko">Tarvitsetko vesijäähdytyksen?</h2>
<p>Et välttämättä. Moni tietokone toimii erinomaisesti hyvällä ilmajäähdyttimellä. Vesijäähdytystä kannattaa harkita, jos</p>
<ul><li>prosessorisi kuluttaa kuormassa paljon tehoa</li><li>kotelossa ei ole tilaa korkealle tornijäähdyttimelle</li><li>haluat jäähdyttää myös näytönohjaimen nesteellä</li><li>arvostat tiettyä ulkonäköä</li></ul>
<p>Lopputulos riippuu aina kokoonpanosta: kotelosta, tuulettimista ja komponenttien kulutuksesta.</p>
<h2 id="hinta">Mitä aloittaminen maksaa?</h2>
<p>Keskitason 240 mm:n AiO maksaa suuntaa-antavasti noin 55–110 € ja tehokkaampi 360 mm:n malli noin 100–170 €. Custom loopin kokonaishinta alkaa tyypillisesti muutamasta sadasta eurosta.</p>
{infobox(PRICE_NOTE)}
<p><a href="/hinnat#laskuri">Laske oma budjettisi hintalaskurilla →</a></p>
<h2 id="virheet">Aloittelijan yleisimmät virheet</h2>
<ol><li><b>Suojakalvo jää blokin pohjaan.</b> Tarkista aina ennen asennusta.</li><li><b>Pumppu kytketään väärään liitäntään</b> tai sen nopeus rajoitetaan liian matalaksi.</li><li><b>Radiatori ei mahdu koteloon</b>, koska tuulettimien paksuus unohtui.</li><li><b>Pumppu on järjestelmän korkeimmassa kohdassa</b>, jolloin ilma kertyy pumppuun ja aiheuttaa ääntä.</li><li><b>Custom loop käynnistetään ilman vuototestiä.</b></li></ol>
{infobox("Custom loop vaatii huolellista asennusta. Älä käynnistä tietokonetta ennen kuin olet varmistanut, että järjestelmä on tiivis.", "warn")}
<h2 id="ukk">Usein kysyttyä</h2>
{faq_block(faq)}'''
    body = f'''<section class="page-hero"><div class="container">{breadcrumbs(trail)}<span class="eyebrow">Perusteet</span><h1>{title}</h1>
<p class="lead">Mitä vesijäähdytys on, miten se toimii ja kumpi sopii sinulle paremmin: valmis AiO vai itse rakennettu custom loop? Tämä opas käy perusteet läpi selkeästi.</p>
<p class="updated">Päivitetty <time datetime="{UPDATED_ISO}">{UPDATED}</time> · Lukuaika noin 6 min</p></div></section>
<div class="container"><div class="article-layout">
<nav class="toc" aria-label="Sisällysluettelo"><h2>Sisällys</h2><ol>{"".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in toc)}</ol></nav>
<article class="prose">{prose}</article>
</div></div>''' + cta()
    art = {"@type": "Article", "headline": title, "description": "Vesijäähdytyksen perusteet aloittelijalle: toimintaperiaate, AiO vs custom loop, hinnat ja yleisimmät virheet.",
           "inLanguage": "fi-FI", "datePublished": UPDATED_ISO, "dateModified": UPDATED_ISO,
           "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"},
           "mainEntityOfPage": f"{SITE}/oppaat/{slug}", "image": SITE + "/og-image.png"}
    page(f"oppaat/{slug}", f"{title} – perusteet selkokielellä | Watercooling.fi",
         "Vesijäähdytys aloittelijalle: miten vesijäähdytys toimii, AiO vai custom loop, mitä aloittaminen maksaa ja mitkä ovat yleisimmät virheet.",
         body, "oppaat", [breadcrumb_schema(trail), art, faq_schema(faq)], og_type="article", path=f"/oppaat/{slug}")

def build_simple(slug, title, h1, lead, html_body, desc):
    trail = [("Etusivu", "/"), (h1, "/" + slug)]
    body = page_hero(trail, "Watercooling.fi", h1, lead) + section(f'<div class="prose">{html_body}</div>', narrow=True)
    page(slug, title, desc, body, None, [breadcrumb_schema(trail)])

def build_legal():
    build_simple("tietosuoja", "Tietosuojakäytäntö | Watercooling.fi", "Tietosuojakäytäntö",
        "Miten Watercooling.fi käsittelee kävijöiden tietoja.",
        '''<p><em>Pohja – täydennä ylläpitäjän tiedot ennen julkaisua.</em></p>
<h2>Rekisterinpitäjä</h2><p>[Ylläpitäjän nimi / yritys, Y-tunnus, osoite, sähköposti]</p>
<h2>Mitä tietoja käsittelemme</h2><p>Sivusto ei vaadi rekisteröitymistä. Palvelin voi tallentaa teknisiä lokitietoja (esim. IP-osoite, selain, aikaleima) tietoturvan ja toiminnan varmistamiseksi. Jos sivustolle lisätään analytiikka tai kumppanilinkit, niiden käsittelemät tiedot kuvataan tässä.</p>
<h2>Käsittelyn peruste</h2><p>Oikeutettu etu palvelun ylläpitämiseksi sekä suostumus analytiikka- ja markkinointievästeiden osalta.</p>
<h2>Säilytysaika</h2><p>Lokitiedot säilytetään vain niin kauan kuin se on tarpeen.</p>
<h2>Oikeutesi</h2><p>Sinulla on oikeus saada pääsy tietoihisi, pyytää niiden oikaisua tai poistamista sekä tehdä valitus tietosuojavaltuutetulle.</p>''',
        "Watercooling.fi:n tietosuojakäytäntö.")
    build_simple("evasteet", "Evästekäytäntö | Watercooling.fi", "Evästekäytäntö",
        "Mitä evästeitä sivustolla käytetään.",
        '''<p><em>Pohja – päivitä, kun analytiikka tai kumppanilinkit otetaan käyttöön.</em></p>
<h2>Välttämättömät evästeet</h2><p>Sivusto ei tällä hetkellä aseta omia evästeitä. Fontit ladataan Google Fonts -palvelusta.</p>
<h2>Analytiikka ja kumppanilinkit</h2><p>Jos sivustolle lisätään analytiikka tai affiliate-linkkejä, niihin liittyvät evästeet otetaan käyttöön vain suostumuksellasi.</p>
<h2>Evästeiden hallinta</h2><p>Voit poistaa ja estää evästeet selaimesi asetuksista.</p>''',
        "Watercooling.fi:n evästekäytäntö.")
    build_simple("yhteystiedot", "Yhteystiedot | Watercooling.fi", "Yhteystiedot",
        "Palaute, korjausehdotukset ja yhteistyötiedustelut.",
        '''<p>Watercooling.fi on riippumaton suomalainen tietosivusto. Otamme mielellämme vastaan palautetta ja korjausehdotuksia sisältöön.</p>
<h2>Sähköposti</h2><p>[toimitus@watercooling.fi]</p>
<h2>Yhteistyö</h2><p>Valmistajat ja jälleenmyyjät: pidämme sisällön neutraalina. Mahdolliset kaupalliset yhteistyöt ja kumppanilinkit merkitään sivustolla selkeästi.</p>''',
        "Ota yhteyttä Watercooling.fi:hin.")
    # 404
    body = section('<div class="center"><span class="eyebrow">404</span><h1>Sivua ei löytynyt</h1><p class="lead" style="margin:0 auto 1.5em">Etsimääsi sivua ei ole olemassa tai se on siirretty.</p><div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/">Etusivulle</a><a class="btn btn-ghost" href="/oppaat">Oppaat</a></div></div>')
    page("404", "Sivua ei löytynyt | Watercooling.fi", "Sivua ei löytynyt.", body, None)
    # 404-sivua ei indeksoida
    p = os.path.join(OUT, "404.html")
    s = open(p, encoding="utf-8").read().replace('content="index, follow, max-image-preview:large"', 'content="noindex"')
    open(p, "w", encoding="utf-8").write(s)

def build_meta():
    urls = ["/", "/vesijaahdytys", "/aio", "/custom-loop", "/komponentit", "/hinnat", "/tuotemerkit", "/oppaat", "/ukk",
            "/oppaat/vesijaahdytys-aloittelijalle", "/tietosuoja", "/evasteet", "/yhteystiedot"]
    pr = {"/": "1.0"}
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED_ISO}</lastmod><priority>{pr.get(u, "0.5" if u in ("/tietosuoja","/evasteet","/yhteystiedot") else "0.8")}</priority></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(LOGO.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ''))
    # Apache: siistit URL:t litteälle rakenteelle (/aio -> aio.html, /oppaat/x -> oppaat-x.html)
    open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8").write(r'''# Watercooling.fi – siistit URL-osoitteet litteälle tiedostorakenteelle
Options -MultiViews
RewriteEngine On
DirectoryIndex index.html
ErrorDocument 404 /404.html

# Pakota https ja ilman www-etuliitettä
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\. [NC]
RewriteRule ^ https://watercooling.fi%{REQUEST_URI} [L,R=301]

# /index.html ja /sivu.html -> siisti osoite
RewriteCond %{THE_REQUEST} \s/+index\.html[\s?] [NC]
RewriteRule ^ / [R=301,L]
RewriteCond %{THE_REQUEST} \s/+([a-z0-9-]+)\.html[\s?] [NC]
RewriteRule ^ /%1 [R=301,L]

# /oppaat/artikkeli -> oppaat-artikkeli.html
RewriteCond %{DOCUMENT_ROOT}/oppaat-$1.html -f
RewriteRule ^oppaat/([a-z0-9-]+)/?$ oppaat-$1.html [L]

# /sivu -> sivu.html
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^([a-z0-9-]+)/?$ $1.html [L]

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml text/plain
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/svg+xml "access plus 1 month"
  ExpiresByType image/png "access plus 1 month"
  ExpiresByType text/html "access plus 0 seconds"
</IfModule>
''')
    # Netlify / Cloudflare Pages
    open(os.path.join(OUT, "_redirects"), "w", encoding="utf-8").write("/oppaat/:slug  /oppaat-:slug.html  200\n")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_index(); build_vesijaahdytys(); build_aio(); build_custom_loop(); build_komponentit()
    build_hinnat(); build_tuotemerkit(); build_oppaat(); build_ukk(); build_article(); build_legal(); build_meta()
    print("OK", sorted(os.listdir(OUT)))
