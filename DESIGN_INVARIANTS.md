# Design-invarianter — olajanson.se

Detta är **referensen** för designverifiering. Efter varje UI-ändring: screenshota
(Playwright headless) + kör /vision (läs HELA spec:en) + DOM-geometri-probe, och
checka varje rad nedan som ✅/❌ med uppmätt värde. "Koden ligger rätt" är inte bevis.

## Färgsystem (mörkt, gäller BÅDA temana — aldrig pre-Magic-Romance pappers-tema)
- [ ] Bakgrund `#14120e` (mörk varm)
- [ ] Brödtext `#EAE6DA` (creme)
- [ ] Guld accent `#F2D024` (rubriker, hover)
- [ ] Dämpad text `#9E9A91`
- [ ] Kantlinjer `#2a2a2a`

## Typografi
- [ ] Rubriker/hero: **Magic Romance**
- [ ] Brödtext: **Fraunces**
- [ ] Sidebar-labels, properties, backlinks, grafrubrik, breadcrumb, topbar-kontroller: **SKF Sans**

## Startsida (index)
- [ ] Magic Romance-hero: full-bleed `factotal.jpeg`, guld skuggtitel
- [ ] Brödtext (intro) kommer från `index.md` (via build_index.py) — rubrik/bild/kort LÅSTA i index2.html
- [ ] **Sticky topbar** finns (search + darkmode + språk)

## Undersidor (artiklar, Quartz-renderade)
- [ ] **Sticky topbar finns** (`position: sticky`, `top:0`) — INTE bara CSS, elementet måste renderas
- [ ] Search + darkmode + språkväljare ligger i **topbaren** — INTE i höger sidofält under grafvyn
- [ ] Höger sidofält innehåller ENDAST grafvy + backlinks
- [ ] H1 i Magic Romance, guld `#F2D024`, med text-shadow
- [ ] Breadcrumb (om kvar): **SKF Sans**, i sticky-topbaren, **vänsterkant alignad med mittenkolumnens vänsterkant**
- [ ] Properties / backlinks-länkar / grafrubrik i SKF Sans

## Verifieringsmetod (obligatorisk)
1. **Skärmdump + DOM-probe** via standardverktyget (1990px, Playwright headless — aldrig zen-browser-MCP):
   ```bash
   python3 ~/.claude/tools/shot.py https://olajanson.se/<sida> --probe -o /tmp/out.png
   python3 ~/.claude/tools/shot.py https://olajanson.se/<sida> --full -o /tmp/full.png
   ```
   `--probe` ger `position/top/left/WxH/font` för topbar, search, darkmode, breadcrumb, h1, kolumner — strukturen som bild→text missar.
2. `python3 ~/.claude/tools/vision_check.py /tmp/full.png` — läs LAYOUT + KOMPONENTER + TYPOGRAFI + FÄRGSYSTEM, inte bara en sektion.
3. PASS/FAIL per rad ovan med UPPMÄTT värde. Ingen "klart" om någon rad är ❌.
