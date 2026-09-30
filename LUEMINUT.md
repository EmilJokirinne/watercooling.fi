# watercooling.fi – julkaisuohje

Kaikki tiedostot ovat juuressa (litteä rakenne). Lataa ne sellaisenaan palvelimen juurihakemistoon.

- Sivut: index, vesijaahdytys, aio, custom-loop, komponentit, hinnat, tuotemerkit, oppaat, ukk + artikkelipohja `oppaat-vesijaahdytys-aloittelijalle.html`, tietosuoja, evasteet, yhteystiedot, 404.
- Siistit URL:t (/aio, /oppaat/<artikkeli>): Apachessa `.htaccess`, Netlify/Cloudflare Pagesissa `_redirects` (nämä palvelut tarjoilevat /aio → aio.html automaattisesti).
- Linkit ja resurssit ovat juuripolkuja (/style.css), joten esikatsele paikallisella palvelimella, ei tiedostoa suoraan avaamalla.
- Hintalaskurin hintahaarukat: `main.js` → PRICES.
- `build.py` generoi kaikki HTML-sivut yhteisistä komponenteista (Header, Footer, FAQ, kortit…). Muokkaa sisältöä siellä ja aja `python3 build.py` (vaihda OUT-polku).
- Uusi opas: kopioi `build_article()`, lisää GUIDES-listaan `True` ja sitemap.xml:ään.
- Täytä ennen julkaisua: tietosuoja- ja yhteystietosivun [hakasulkeissa olevat] kohdat.
- Affiliate: ei linkkejä. "Katso tuotteet →" / "Hinta alkaen" -painikkeet lisätään vasta kun konfiguraatio on olemassa.
