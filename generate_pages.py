#!/usr/bin/env python3
"""Genererar custom HTML-sidor från markdown-filer med premiss.html som mall."""
import re, os

CONTENT_DIR = "content"

PAGES = {
    "anthony": {
        "title": "Jag gillar verkligen Anthony Jesilnek",
        "tags": ["#comedian", "#likeablepersons"],
        "image": "/anthony.jpg",
        "image_alt": "Anthony Jesilnek",
        "body": """<p>I den nu påhittade serien personer jag gillar så inleder jag med sagda komiker. Men vem är Anthony Jeselinik kanske du säger? Han är en komiker som kanske mest är känd för sina stundtals mörka skämt. Och innan du viftar bort det så vill jag bara säga att det är inte är därför jag gillar honom. Jo, men visst, han är kul. Men här är en liten lista varför jag respekterar honom:</p>
<ul>
<li>Hans tiktok feed upptas av hans bokcirkel som man kan gå med i om man skickar ett mail till honom. Man läser en bok i månaden.</li>
<li>Trots sina bryska skämt så har han flera gånger tagit ställning emot komiker som ägnar sig åt "bullying" — framför allt på högerkanten.</li>
<li>Han framstår som en oerhört ärlig person.</li>
</ul>
<p>Jag kan ha fel. Allt kanske bara är fejk. Men så känns det för mig.</p>""",
        "backlinks": [("/", "En mytoman i en lögndetektorfabriken")],
    },
    "avatar": {
        "title": "Character arcs of Avatar",
        "tags": ["#storytelling", "#characterarc", "#avatarthelastaibender"],
        "image": "/unclehiro-and-zuko.png",
        "image_alt": "Uncle Iroh och Zuko",
        "body": """<h5>Villkorslös kärlek</h5>
<p>Jag sitter med min 10 åring och gör vår lördags binge förmiddagar av Avatar the last airbender. Eller vi har kommit så lång som slutet på säsongsfinalen av anda säsongen av legend of Korra.</p>
<p>Avatar the last airbender, den animerade serien från Nickelodeon, är i mina ögon 10/10. Jag kan inte komma på ett enda avsnitt som fick mig att slumra till och tappa fokus. Det gäller även mina barn, samtliga fyra barn skulle jag nog säga, trots att de tittade på serien i sin helhet vid helt olika tillfällen. Om du är förälder med barn som börjar närma sig tioårsåldern så är detta en perfekt introduktion till next level story telling.</p>
<p>Legend of Korra var inte lika imponerande till en början. Lite för mycket silly, lite för mycket soap opera romance. Hantverket var mästerligt men kanske en lite för stor överdos av spektakulära krafter. Men halvvägs in i säsong två reste den sig till en grad att jag allvarligt funderade på att stanna inne och kolla resten hela dagen.</p>
<p>Om jag skulle plocka upp en sak som båda the last airbender och legend of Korra gör ofantligt bra så är det character development. Karaktärer som vi vanligtvis skulle beskriva som arketyper för det goda eller onda tillåts tas längs med lååånga arcs för att till slut hamna på en plats där du i hemlighet alltid önskat att de var.</p>
<p>I the last airbender är prins Zuko det absolut starkaste exemplet, men i legend of Korra skulle jag säga att det är Tenzin. Kanske är det för att han precis som jag är far till många barn. Jag blev verkligen berörd av bördan av ansvar som den siste av sin sort och bördan av föräldraskap.</p>
<p>Jag säger som Eska: <em>"You will always hold a special place in the organ that pumps my blood."</em></p>
<img src="/eska.png" alt="Eska — Legend of Korra">""",
        "backlinks": [("/premiss", "Vikten av att ha en enastående premiss"), ("/", "En mytoman i en lögndetektorfabriken")],
    },
    "businesschmodels": {
        "title": "Business model enshitification",
        "tags": ["#businessmodels", "#enshitification"],
        "image": "/mandrake.png",
        "image_alt": "Mandrake",
        "body": """<h5>Business models, busines schmodels sa Mandrake och gjorde en magisk gest.</h5>
<blockquote><p>"En affärsmodell eller företagsmodell är en teoretisk beskrivning av hur ett företag, eller en affärsverksamhet, är tänkt att fungera."</p></blockquote>
<p>Det ovanstående är näppeligen något anmärkningsvärt. Klart alla företag skall ha rätten att bestämma hur de tjänar sina pengar. Denna lilla rant handlar istället om frustrationen av att känna sig lurad av en affärsmodell. Förmodligen för att den aldrig presenterades som just en affärsmodell utan som det enda självklara sättet att göra något.</p>
<p>Exempel ett av dessa modeller är chattbotten som vi chattar med i ett dialogfönster. Att låta modeller skriva rakt in i de dokument du vill ändra är självklart oerhört mycket mer logiskt och effektivt. Men varför har denna feature tagit så lång tid? Självklart för att det är viktigt att vi fortsätter att betala för tjänsten som innehåller chatfönstret och en sammanhållen upplevelse på ai-leverantörens sajt.</p>
<p>Så kallat minne är en annan feature som är en del av dold affärsmodell. Det vi kallar minne hos en chat gpt simulerar ett mänskligt beteende i syfte att få oss att känna varmare känslor för tjänsten. Det är manipulativt varumärkesmagi. Faktum är att varenda gång du skickar ett chattmeddelande så talar du med en språkmodell med fullkomligt blankt minne.</p>
<p>Det sista exemplet är de sociala mediernas olika strategier för att lyckas slå igenom. Du skall posta x antal gånger per dygn, du skall posta vid vissa tider, du skall vara lättsmält och förutsägbar. Det är inte för att vi användare skall få en bättre upplevelse — det är en del av en smart affärsmodell som genererar innehåll åt plattformen.</p>
<p>I sammanfattning: Affärsmodeller bör vara transparenta. Om de döljs under lager av manipulativ användardesign och paketeras som något du måste anpassa dig till, finns det överhängande risk att du blivit lurad.</p>""",
        "backlinks": [("/varfor-digital-garden", "Varför digital garden?"), ("/", "En mytoman i en lögndetektorfabriken")],
    },
    "gastbok": {
        "title": "Gästbok",
        "tags": ["#meta"],
        "image": None,
        "image_alt": None,
        "body": """<p>Lämna ett spår. Skriv vad du vill — vad du tänkte på, vad du hittade här, eller bara hej.</p>
<p>Inläggen lagras som <a href="https://github.com/OlaJanson/olajanson.github.io/issues">GitHub Issues</a> och visas direkt nedan. Du behöver ett GitHub-konto för att skriva.</p>
<hr style="border-color:#2a2a2a; margin: 32px 0;">
<script src="https://utteranc.es/client.js"
        repo="OlaJanson/olajanson.github.io"
        issue-term="pathname"
        label="gästbok"
        theme="dark-blue"
        crossorigin="anonymous"
        async>
</script>
<hr style="border-color:#2a2a2a; margin: 32px 0;">
<p><em>Föredrar du att skriva utan konto? Mejla <a href="mailto:ola.janson@gmail.com">ola.janson@gmail.com</a>.</em></p>""",
        "backlinks": [("/", "En mytoman i en lögndetektorfabriken")],
    },
    "jag": {
        "title": "Fragment",
        "tags": ["#meta", "#cv"],
        "image": "/arme-dith-trans.png",
        "image_alt": "Arme-dith",
        "body": """<p>Jag är en schweizisk armékniv, brukar jag säga.</p>
<p>Eller det kanske inte är en perfekt beskrivning av vad jag är? Hos en schweizisk armékniv är mångfalden dess främsta unika egenskap. Det enskilda verktyget är inte så imponerande men att klämma in alla i en och samma röda enhet är unikt. Och det är nog där jag känner att liknelsen haltar. Jag minns som barn hur irriterad jag var över hur detta röda multiverktyg inte gick att använda i mina träkojor — hur den lilla sågen var värdelös på att kapa grenar.</p>
<p>Nej, jag tror snarare att jag kanske skall beskriva mig som en verktygslåda. Men vad innehåller verktygslådan?</p>
<p>Pedagogik skulle jag vilja hävda är ett väl använt verktyg. Jag har jobbat från och till som lärare, främst inom yrkeshögskola men också på universitet och grundskola. Jag arbetar efter bästa förmåga med formativ bedömning. Just nu uteslutande i online-kurser.</p>
<p>Designprocess och kreativa processer är något jag också spenderat många yrkesår med. Senast som creative director på SKF. Men dessförinnan som affärsutvecklare på HiQ.</p>
<p>Speldesign. Jag har designat spel — digitala, brädspel och rollspel. Just nu blir det mest rollspel. Jag har konstant ett spelprojekt igång men blir sällan klar.</p>""",
        "backlinks": [("/varfor-digital-garden", "Varför digital garden?"), ("/", "En mytoman i en lögndetektorfabriken")],
    },
    "treehouse": {
        "title": "Varför finns det så ont om bilder av kojor byggda av barn?",
        "tags": ["#enshitification", "#designprocess", "#algorithm"],
        "image": "/treehouse.png",
        "image_alt": "Koja byggd av vuxna",
        "body": """<p>Vad har dessa kojor gemensamt?</p>
<p>Ingen av dem är byggda av barn.</p>
<img src="/treehouse-1.png" alt="Kojor sökta på 'treehouse made by kids'">
<p>Men låt oss ändra sökningen till "treehouse made by kids". Yeah right. Inte ens exemplaret tredje från vänster har den vuxne lyckats hålla sina kontrollerande fingrar i styr. Alldeles för rakt och tillrättalagt.</p>
<p>Men detta handlar inte om att vuxna inte låter barn göra kojor — utan varför det är så otroligt svårt att hitta bilder på det. Jag minns att jag gjorde en sökning för kanske tio år sedan och att det då fanns fler bilder av barns kojor.</p>
<p>Betänk att jag sitter framför min dator och killgissar. Jag skulle som många andra +50 vita män kunna arbeta upp lite tangentbordsvrede och skylla på telefoner, spel, film eller annan skit. Och visst har det säkert att göra med att barn i mindre utsträckning idag rör sig i skog och mark. Springer i containrar bara för att hitta plankor att bygga livsfarliga träskapelser i träkronor — dom där som är fullkomligt livsfarliga men så laddade med barns förväntan och skaparglädje.</p>
<img src="/treehouse-bethany.jpg" alt="Treehouse by Bethany Weeks">
<p>Men jag väljer att tänka att det är en del av enshitification — hur sökningarna av bilder blivit mer strömlinjeformade. Hur algoritmer trycker fram bild efter bild med konformt snömos. Jag väljer att rikta min gubbvrede åt det hållet för jag kan inte leva med tanken på att barn inte längre bygger livsfarliga kojor i träd.</p>""",
        "backlinks": [("/", "En mytoman i en lögndetektorfabriken")],
    },
    "varfor-digital-garden": {
        "title": "Varför digital garden?",
        "tags": ["#digitalgararden", "#webb"],
        "image": None,
        "image_alt": None,
        "body": """<p>Jag delade ut en läxa i en av kurserna jag just nu håller. Den heter konstnärligt förverkligande i digitala miljöer. Mina studenter fick i uppgift att hitta digitala förebilder — men inte fokusera på innehållet, utan på <em>hur</em> de gör det.</p>
<p>En student vars intresse primärt var inom skrivande delade en sida och sa: "Maggie Appeltons, vars konst/intressen jag inte är särskilt intresserad av, men själva hemsidan är ungefärligt med det jag vill få fram." Jag insåg med ens att detta var något utöver det vanliga. Hennes sida var det där någon satt sig ner och funderat på "hur vill jag ha det?" — struntat i mallar, och bara kört. Byggt utifrån sina egna behov.</p>
<p>Och det fick mig att inse: hur jävla mycket vi sitter fast i andras <a href="/businesschmodels">affärsmodeller</a>. Vi sitter fast för att de har övertygat oss om att det här är det enda sättet att göra det.</p>
<p>Jag läste vidare på Maggies sida. Jag läste hennes artikel om digital gardens. Jag blev nästan förbannad men mest på mig själv — hur fan har jag missat det här? Why was I not invited to this party?</p>
<p>Det satte fingret på exakt det som jag har känt saknas i webbsammanhang. Sociala medier handlar om att sälja sitt innehåll till någon annan och vara helt i händerna på någon annans affärsmodell. Där du har noll kontroll om du inte är otroligt följsam och hela tiden försöker hacka koden för att go viral.</p>
<p>Råd nummer ett om du ska starta en kanal på något socialt media är alltid att hitta ett koncept. Prata bara om en sak. Och <a href="/jag">jag</a> är bred och vill prata om allt. Med min ADHD-hjärna hänger allting ihop. Det är en del i samma moln av koncept som alltid har med varandra att göra.</p>
<p>Slutsatsen i korthet — digital gardering är som gjort för mig. Sedan vet jag inte om det bara blir ytterligare en gravplats på internet. Det får tiden utvisa.</p>""",
        "backlinks": [("/", "En mytoman i en lögndetektorfabriken")],
    },
}

TEMPLATE = '''<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Ola Janson</title>
    <link href="/index.css" rel="stylesheet" type="text/css">
    <script src="/prescript.js" type="application/javascript" data-persist="true"></script>
    <script type="application/javascript" data-persist="true">const fetchData = fetch("/static/contentIndex.json").then(data => data.json())</script>
    <style>
        @font-face {{
            font-family: 'Magic Romance';
            src: url('/fonts/magic-romance.ttf') format('truetype');
        }}
        @font-face {{
            font-family: 'Fraunces';
            src: url('/fonts/fraunces.ttf') format('truetype');
        }}
        @font-face {{
            font-family: 'SKF Sans';
            src: url('/fonts/skfsans.otf') format('opentype');
        }}

        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        html {{
            overflow-x: clip !important;
            overflow-y: auto !important;
        }}
        body {{
            overflow: visible !important;
            background-color: #14120e !important;
            background-image: repeating-linear-gradient(
                0deg, transparent, transparent 3px,
                rgba(0,0,0,0.08) 3px, rgba(0,0,0,0.08) 4px
            ) !important;
            color: #EAE6DA !important;
            font-family: 'Fraunces', Georgia, serif !important;
            max-width: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        .grid-row {{
            display: grid;
            grid-template-columns: 280px minmax(0, 720px) 280px;
            gap: 0 48px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .title-band {{
            width: 100%;
            padding-top: 80px;
            padding-bottom: 0;
        }}
        .title-band .col-left  {{ grid-column: 1; }}
        .title-band .col-main  {{ grid-column: 2; }}
        .title-band .col-right {{ grid-column: 3; }}
        .page-title {{
            font-family: 'Magic Romance', serif !important;
            font-size: clamp(2.8rem, 6vw + 1rem, 6rem) !important;
            font-weight: 400 !important;
            color: #F2D024 !important;
            line-height: 0.9 !important;
            margin-bottom: 0;
            letter-spacing: -0.01em;
        }}

        .topbar {{
            width: 100%;
            background: #181c1e;
            border-bottom: 1px solid #2a2a2a;
            position: sticky;
            top: 0;
            z-index: 100;
            margin-top: 0;
        }}
        .topbar-inner {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: flex-end;
            padding: 10px 0;
        }}
        .topbar-controls {{
            width: 280px;
            padding-right: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .search-button {{
            display: flex;
            align-items: center;
            gap: 5px;
            background: #0e0e0e;
            border: 1px solid #2a2a2a;
            border-radius: 16px;
            color: #888;
            padding: 4px 12px;
            font-family: 'SKF Sans', sans-serif;
            font-size: 12px;
            cursor: pointer;
        }}
        .search-button svg {{ width: 12px; height: 12px; stroke: #888; fill: none; }}
        .darkmode-btn {{
            background: none; border: none; cursor: pointer;
            padding: 3px; display: flex; align-items: center;
            margin-left: auto;
        }}
        .darkmode-btn svg {{ width: 18px; height: 18px; fill: #888; }}
        .nightIcon {{ display: none; }}
        [saved-theme="dark"] .dayIcon  {{ display: none; }}
        [saved-theme="dark"] .nightIcon{{ display: block; }}
        .language-toggle {{
            background: none; border: none; cursor: pointer;
            color: #888; font-family: 'SKF Sans', sans-serif;
            font-size: 12px; padding: 3px 6px; white-space: nowrap;
        }}
        .lang-separator {{ margin: 0 1px; opacity: 0.3; }}
        .lang-sv, .lang-en {{ opacity: 0.4; }}
        .lang-sv.active, .lang-en.active {{ opacity: 1; color: #EAE6DA; }}

        .page-layout {{
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 280px minmax(0, 720px) 280px;
            grid-template-areas: "left main right";
            gap: 0 48px;
            padding-top: 32px;
            align-items: start;
        }}
        .sidebar-left  {{ grid-area: left;  padding-left: 24px; }}
        .main-col      {{ grid-area: main;  padding-bottom: 100px; }}
        .sidebar-right {{ grid-area: right; padding-right: 24px; position: sticky; top: 56px; }}

        .book-cover-mobile {{
            display: none;
            width: 140px;
            border-radius: 4px;
            opacity: 0.9;
            margin-bottom: 32px;
        }}
        .book-cover {{
            width: 100%;
            max-width: 200px;
            border-radius: 4px;
            opacity: 0.9;
            display: block;
            margin-left: auto;
            margin-top: 96px;
        }}

        .title-divider {{
            border: none;
            border-top: 1px solid #2a2a2a;
            margin-bottom: 16px;
        }}
        .properties {{
            display: flex;
            align-items: baseline;
            gap: 10px;
            margin-bottom: 48px;
        }}
        .prop-icon {{ color: #555; font-size: 13px; flex-shrink: 0; }}
        .prop-label {{
            font-family: 'Fraunces', serif;
            font-style: italic;
            font-size: 16px; color: #EAE6DA;
            flex-shrink: 0;
        }}
        .tags {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .tag {{
            font-family: 'SKF Sans', sans-serif;
            font-size: 14px; color: #9E9A91; text-decoration: none;
            letter-spacing: 0.03em;
        }}
        .tag:hover {{ color: #F2D024; }}

        .article-body {{ font-size: 20px; line-height: 2.0; color: #EAE6DA; }}
        .article-body p {{ margin-bottom: 32px; }}
        .article-body p:last-child {{ margin-bottom: 0; }}
        .article-body ul, .article-body ol {{ margin-bottom: 32px; padding-left: 1.5em; }}
        .article-body li {{ margin-bottom: 8px; }}
        .article-body h5 {{
            font-family: 'Fraunces', serif;
            font-style: italic;
            font-size: 18px; color: #EAE6DA;
            margin-bottom: 16px; margin-top: 40px;
        }}
        .article-body blockquote {{
            border-left: 3px solid #2a2a2a;
            padding-left: 20px;
            margin-bottom: 32px;
            color: #9E9A91;
            font-style: italic;
        }}
        .article-body a {{ color: #EAE6DA; text-decoration: underline; text-underline-offset: 3px; }}
        .article-body a:hover {{ color: #F2D024; }}
        .article-body strong {{ color: #ffffff; }}
        .article-body hr {{ border-color: #2a2a2a; margin: 32px 0; }}
        .article-body img {{
            max-width: 100%;
            border-radius: 6px;
            display: block;
            margin: 40px 0;
            opacity: 0.92;
        }}
        .article-body figure {{
            margin: 40px 0;
        }}
        .article-body figcaption {{
            font-family: 'SKF Sans', sans-serif;
            font-size: 13px;
            color: #9E9A91;
            margin-top: 8px;
            font-style: italic;
        }}

        .backlinks {{ margin-bottom: 32px; }}
        .backlinks h3 {{
            font-family: 'SKF Sans', sans-serif;
            font-size: 10px; color: #666;
            text-transform: uppercase; letter-spacing: 0.1em;
            margin-bottom: 10px;
        }}
        .backlinks ul {{ list-style: none; }}
        .backlinks ul li {{ margin-bottom: 6px; }}
        .backlinks ul li a {{
            font-family: 'Fraunces', serif;
            font-size: 14px; color: #9E9A91;
            text-decoration: underline; text-underline-offset: 3px;
        }}
        .backlinks ul li a:hover {{ color: #F2D024; }}

        .graph {{ all: unset; display: block; }}
        .graph h3 {{
            font-family: 'SKF Sans', sans-serif;
            font-size: 10px; color: #666;
            text-transform: uppercase; letter-spacing: 0.1em;
            margin-bottom: 8px;
        }}
        .graph-outer {{
            width: 100%; height: 200px;
            border: 1px solid #222; border-radius: 6px;
            background: #181c1e; overflow: hidden; position: relative;
        }}
        .graph-container {{ width: 100%; height: 100%; }}
        .global-graph-icon {{
            position: absolute; bottom: 8px; right: 8px;
            background: none; border: none; cursor: pointer;
            color: #555; padding: 4px;
        }}
        .global-graph-icon svg {{ width: 14px; height: 14px; }}
        .global-graph-outer {{ display: none; }}

        .search-container {{ display: none; }}
        .search-container.active {{ display: block; }}

        @media (max-width: 900px) {{
            .grid-row {{ grid-template-columns: 1fr; }}
            .title-band .col-left,
            .title-band .col-right {{ display: none; }}
            .title-band .col-main {{ padding: 0 16px; }}
            .page-title {{ font-size: clamp(2.2rem, 8vw, 3.5rem) !important; }}
            .topbar-controls {{ width: auto; }}
            .page-layout {{
                grid-template-columns: 1fr;
                grid-template-areas: "main" "right";
            }}
            .sidebar-left {{ display: none; }}
            .book-cover-mobile {{ display: block; }}
            .sidebar-right {{ position: static; padding: 0 16px 40px; }}
            .sidebar-right .graph {{ display: none; }}
            .main-col {{ padding: 0 16px 48px; }}
        }}
        @media (max-width: 480px) {{
            .page-title {{ font-size: 40px !important; }}
            .article-body {{ font-size: 18px; }}
        }}
    </style>
</head>
<body>

<div class="title-band">
    <div class="grid-row">
        <div class="col-left"></div>
        <div class="col-main">
            <h1 class="page-title">{title}</h1>
        </div>
        <div class="col-right"></div>
    </div>
</div>

<div class="topbar">
    <div class="topbar-inner">
        <div class="topbar-controls">
            <div class="search">
                <button class="search-button" aria-label="Search" aria-expanded="false">
                    <svg role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 19.9 19.7"><title>Search</title><g class="search-path" fill="none"><path stroke-linecap="square" d="M18.5 18.3l-5.4-5.4"></path><circle cx="8" cy="8" r="7"></circle></g></svg>
                    Sök
                </button>
                <div class="search-container">
                    <div class="search-space">
                        <input autocomplete="off" class="search-bar" name="search" type="text" aria-label="Sök efter något..." placeholder="Sök efter något..."/>
                        <div class="search-layout" data-preview="true" data-field-priority="[&quot;title&quot;,&quot;content&quot;,&quot;tags&quot;]"></div>
                    </div>
                </div>
            </div>
            <button class="darkmode-btn" style="margin-left:auto;">
                <svg xmlns="http://www.w3.org/2000/svg" class="dayIcon" viewBox="0 0 35 35"><path d="M6,17.5C6,16.672,5.328,16,4.5,16h-3C0.672,16,0,16.672,0,17.5S0.672,19,1.5,19h3C5.328,19,6,18.328,6,17.5z M7.5,26c-0.414,0-0.789,0.168-1.061,0.439l-2,2C4.168,28.711,4,29.086,4,29.5C4,30.328,4.671,31,5.5,31c0.414,0,0.789-0.168,1.06-0.44l2-2C8.832,28.289,9,27.914,9,27.5C9,26.672,8.329,26,7.5,26z M17.5,6C18.329,6,19,5.328,19,4.5v-3C19,0.672,18.329,0,17.5,0S16,0.672,16,1.5v3C16,5.328,16.671,6,17.5,6z M27.5,9c0.414,0,0.789-0.168,1.06-0.439l2-2C30.832,6.289,31,5.914,31,5.5C31,4.672,30.329,4,29.5,4c-0.414,0-0.789,0.168-1.061,0.44l-2,2C26.168,6.711,26,7.086,26,7.5C26,8.328,26.671,9,27.5,9z M6.439,8.561C6.711,8.832,7.086,9,7.5,9C8.328,9,9,8.328,9,7.5c0-0.414-0.168-0.789-0.439-1.061l-2-2C6.289,4.168,5.914,4,5.5,4C4.672,4,4,4.672,4,5.5c0,0.414,0.168,0.789,0.439,1.06L6.439,8.561z M33.5,16h-3c-0.828,0-1.5,0.672-1.5,1.5s0.672,1.5,1.5,1.5h3c0.828,0,1.5-0.672,1.5-1.5S34.328,16,33.5,16z M28.561,26.439C28.289,26.168,27.914,26,27.5,26c-0.828,0-1.5,0.672-1.5,1.5c0,0.414,0.168,0.789,0.439,1.06l2,2C28.711,30.832,29.086,31,29.5,31c0.828,0,1.5-0.672,1.5-1.5c0-0.414-0.168-0.789-0.439-1.061L28.561,26.439z M17.5,29c-0.829,0-1.5,0.672-1.5,1.5v3c0,0.828,0.671,1.5,1.5,1.5s1.5-0.672,1.5-1.5v-3C19,29.672,18.329,29,17.5,29z M17.5,7C11.71,7,7,11.71,7,17.5S11.71,28,17.5,28S28,23.29,28,17.5S23.29,7,17.5,7z M17.5,25c-4.136,0-7.5-3.364-7.5-7.5c0-4.136,3.364-7.5,7.5-7.5c4.136,0,7.5,3.364,7.5,7.5C25,21.636,21.636,25,17.5,25z"/></svg>
                <svg xmlns="http://www.w3.org/2000/svg" class="nightIcon" viewBox="0 0 100 100"><path d="M96.76,66.458c-0.853-0.852-2.15-1.064-3.23-0.534c-6.063,2.991-12.858,4.571-19.655,4.571C62.022,70.495,50.88,65.88,42.5,57.5C29.043,44.043,25.658,23.536,34.076,6.47c0.532-1.08,0.318-2.379-0.534-3.23c-0.851-0.852-2.15-1.064-3.23-0.534c-4.918,2.427-9.375,5.619-13.246,9.491c-9.447,9.447-14.65,22.008-14.65,35.369c0,13.36,5.203,25.921,14.65,35.368s22.008,14.65,35.368,14.65c13.361,0,25.921-5.203,35.369-14.65c3.872-3.871,7.064-8.328,9.491-13.246C97.826,68.608,97.611,67.309,96.76,66.458z"/></svg>
            </button>
            <button class="language-toggle" id="lang-btn" aria-label="Växla språk" data-slug="{slug}">
                <span class="lang-sv" id="lang-sv">SV</span><span class="lang-separator">/</span><span class="lang-en" id="lang-en">EN</span>
            </button>
        </div>
    </div>
</div>

<div class="page-layout">

    <aside class="sidebar-left">
        {sidebar_left}
    </aside>

    <main class="main-col">
        {mobile_image}
        <hr class="title-divider">
        <div class="properties">
            <span class="prop-icon">◈</span>
            <span class="prop-label">Properties</span>
            <div class="tags">
                {tags_html}
            </div>
        </div>
        <article class="article-body">
            {body}
        </article>
    </main>

    <aside class="sidebar-right">
        <div class="backlinks">
            <h3>Backlinks</h3>
            <ul>
                {backlinks_html}
            </ul>
        </div>
        <div class="graph">
            <h3>Grafvy</h3>
            <div class="graph-outer">
                <div class="graph-container" data-cfg="{{&quot;drag&quot;:true,&quot;zoom&quot;:true,&quot;depth&quot;:3,&quot;scale&quot;:1.1,&quot;repelForce&quot;:0.5,&quot;centerForce&quot;:0.3,&quot;linkDistance&quot;:30,&quot;fontSize&quot;:0.6,&quot;opacityScale&quot;:1,&quot;showTags&quot;:false,&quot;removeTags&quot;:[],&quot;focusOnHover&quot;:false,&quot;enableRadial&quot;:false}}"></div>
                <button class="global-graph-icon" aria-label="Global Graph">
                    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 55 55" fill="currentColor"><path d="M49,0c-3.309,0-6,2.691-6,6c0,1.035,0.263,2.009,0.726,2.86l-9.829,9.829C32.542,17.634,30.846,17,29,17s-3.542,0.634-4.898,1.688l-7.669-7.669C16.785,10.424,17,9.74,17,9c0-2.206-1.794-4-4-4S9,6.794,9,9s1.794,4,4,4c0.74,0,1.424-0.215,2.019-0.567l7.669,7.669C21.634,21.458,21,23.154,21,25s0.634,3.542,1.688,4.897L10.024,42.562C8.958,41.595,7.549,41,6,41c-3.309,0-6,2.691-6,6s2.691,6,6,6s6-2.691,6-6c0-1.035-0.263-2.009-0.726-2.86l12.829-12.829c1.106,0.86,2.44,1.436,3.898,1.619v10.16c-2.833,0.478-5,2.942-5,5.91c0,3.309,2.691,6,6,6s6-2.691,6-6c0-2.967-2.167-5.431-5-5.91v-10.16c1.458-0.183,2.792-0.759,3.898-1.619l7.669,7.669C41.215,39.576,41,40.26,41,41c0,2.206,1.794,4,4,4s4-1.794,4-4s-1.794-4-4-4c-0.74,0-1.424,0.215-2.019,0.567l-7.669-7.669C36.366,28.542,37,26.846,37,25s-0.634-3.542-1.688-4.897l9.665-9.665C46.042,11.405,47.451,12,49,12c3.309,0,6-2.691,6-6S52.309,0,49,0z"/></svg>
                </button>
            </div>
            <div class="global-graph-outer">
                <div class="global-graph-container" data-cfg="{{&quot;drag&quot;:true,&quot;zoom&quot;:true,&quot;depth&quot;:-1,&quot;scale&quot;:0.9,&quot;repelForce&quot;:0.5,&quot;centerForce&quot;:0.2,&quot;linkDistance&quot;:30,&quot;fontSize&quot;:0.6,&quot;opacityScale&quot;:1,&quot;showTags&quot;:false,&quot;removeTags&quot;:[],&quot;focusOnHover&quot;:true,&quot;enableRadial&quot;:true}}"></div>
            </div>
        </div>
    </aside>

</div>

<script src="/postscript.js" type="module" data-persist="true"></script>
<script>
(function() {{
    var slug = document.getElementById('lang-btn').dataset.slug;
    var path = window.location.pathname.replace(/\/$/, '');
    var isEn = path.endsWith('.en');
    var svEl = document.getElementById('lang-sv');
    var enEl = document.getElementById('lang-en');
    if (isEn) {{
        enEl.classList.add('active'); svEl.classList.remove('active');
    }} else {{
        svEl.classList.add('active'); enEl.classList.remove('active');
    }}
    document.getElementById('lang-btn').addEventListener('click', function() {{
        if (isEn) {{
            window.location.href = '/' + slug;
        }} else {{
            window.location.href = '/' + slug + '.en';
        }}
    }});
}})();
</script>
</body>
</html>'''


def make_tags_html(tags):
    def tag_url(t):
        # strip leading # and lowercase for Quartz tag URL
        return "/tags/" + t.lstrip("#").lower()
    return "\n                ".join(f'<a class="tag" href="{tag_url(t)}">{t}</a>' for t in tags)

def make_backlinks_html(backlinks):
    return "\n                ".join(f'<li><a href="{href}">{label}</a></li>' for href, label in backlinks)

def make_sidebar_left(image, alt):
    if not image:
        return ""
    return f'<img class="book-cover" src="{image}" alt="{alt}">'

def make_mobile_image(image, alt):
    if not image:
        return ""
    return f'<img class="book-cover-mobile" src="{image}" alt="{alt}">'


for slug, page in PAGES.items():
    html = TEMPLATE.format(
        title=page["title"],
        slug=slug,
        tags_html=make_tags_html(page["tags"]),
        body=page["body"],
        backlinks_html=make_backlinks_html(page["backlinks"]),
        sidebar_left=make_sidebar_left(page.get("image"), page.get("image_alt", "")),
        mobile_image=make_mobile_image(page.get("image"), page.get("image_alt", "")),
    )
    out_path = os.path.join(CONTENT_DIR, f"{slug}.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"✓ {out_path}")

print("Klart!")

# ─── ENGELSKA SIDOR ───────────────────────────────────────────────────────────

EN_PAGES = {
    "anthony": {
        "title": "I really like Anthony Jeselnik",
        "tags": ["#comedian", "#likeablepersons"],
        "image": "/anthony.jpg",
        "image_alt": "Anthony Jeselnik",
        "body": """<p>In the now made-up series of people I like, I'm starting with the aforementioned comedian. But who is Anthony Jeselnik, you might ask? He is a comedian perhaps best known for his at times dark jokes. And before you dismiss that, I just want to say that's not why I like him. Yes, but he is funny, of course. But here's a small list of why I respect him:</p>
<ul>
<li>His TikTok feed is taken up by his book club, which you can join if you send him an email. You read one book a month.</li>
<li>Despite his abrupt jokes, he has several times taken a stand against comedians who engage in "bullying", especially on the right wing.</li>
<li>He comes across as an incredibly honest person.</li>
</ul>
<p>I could be wrong. It might all just be fake. But that's how it feels to me.</p>""",
        "backlinks": [("/", "A mythomaniac in a lie detector factory")],
    },
    "avatar": {
        "title": "Character arcs of Avatar",
        "tags": ["#storytelling", "#characterarc", "#avatarthelastaibender"],
        "image": "/unclehiro-and-zuko.png",
        "image_alt": "Uncle Iroh and Zuko",
        "body": """<h5>Unconditional love</h5>
<p>I'm sitting with my 10-year-old, doing our Saturday binge mornings of Avatar the Last Airbender. Or rather, we've gotten as far as the end of the season finale of the second season of Legend of Korra.</p>
<p>Avatar the Last Airbender, the animated series from Nickelodeon, is in my eyes a 10/10. I can't think of a single episode that made me doze off and lose focus. This also applies to my children, all four of them I would say, even though they watched the series in its entirety at completely different times. If you are a parent with children approaching their ten-year-old age, this is a perfect introduction to next-level storytelling.</p>
<p>Legend of Korra was not as impressive at first. A little too silly, a little too much soap opera romance. The craftsmanship was masterful, but perhaps a slightly too great overdose of spectacular powers. But halfway through season two, it rose to such a degree that I'm now seriously considering staying inside and watching the rest.</p>
<p>If I were to pick one thing that both The Last Airbender and Legend of Korra do immensely well, it's character development. Characters we would typically describe as archetypes for good or evil are allowed to be taken along loooong arcs to finally end up in a place where you secretly always wished they were. In The Last Airbender, Prince Zuko is the absolute strongest example, but in Legend of Korra, I would say it's Tenzin. Perhaps it's because, just like me, he is a father to many children. But I was truly moved by the burden of responsibility as the last of his kind and the burden of parenthood.</p>
<p>I say like Eska: <em>"You will always hold a special place in the organ that pumps my blood."</em></p>
<img src="/eska.png" alt="Eska — Legend of Korra">""",
        "backlinks": [("/premiss.en", "The importance of having an outstanding premise"), ("/", "A mythomaniac in a lie detector factory")],
    },
    "businesschmodels": {
        "title": "Business model enshitification",
        "tags": ["#businessmodels", "#enshitification"],
        "image": "/mandrake.png",
        "image_alt": "Mandrake",
        "body": """<h5>Business models, business schmodels said Mandrake and made a magical gesture.</h5>
<blockquote><p>"A business model or company model is a theoretical description of how a company, or a business activity, is intended to function."</p></blockquote>
<p>The above is hardly anything remarkable. Of course, all companies should have the right to decide how they earn their money. This little rant is instead about the frustration of feeling deceived by a business model. Probably because it was never presented as just a business model but as the only obvious way to do something.</p>
<p>One example of these models is the chatbot, which we chat with in a dialogue window. Letting models write directly into the documents you want to edit is, of course, immensely more logical and efficient. But why has this feature taken so long? Of course, because it's important that we continue to pay for the service that includes the chat window and a cohesive experience on the AI provider's site.</p>
<p>So-called memory is another feature that is part of a hidden business model. What we call memory in a chat GPT simulates human behavior to make us feel warmer towards the service. It's manipulative brand magic. In fact, every time you send a chat message, you are talking to a language model with a completely blank memory.</p>
<p>The last example is the various strategies of social media to succeed in breaking through. You should post x number of times per day, post at certain times, be easily digestible and predictable. It's not for users to get a better experience — it's part of a smart business model that generates content for the platform.</p>
<p>In summary: Business models should be transparent. If they are hidden under layers of manipulative user design and packaged as something you must adapt to, there is a high risk that you have been deceived.</p>""",
        "backlinks": [("/varfor-digital-garden.en", "Why digital garden?"), ("/", "A mythomaniac in a lie detector factory")],
    },
    "gastbok": {
        "title": "Guestbook",
        "tags": ["#meta"],
        "image": None,
        "image_alt": None,
        "body": """<p>Leave a trace. Write what you want — what you were thinking about, what you found here, or just hello.</p>
<p>The posts are stored as <a href="https://github.com/OlaJanson/olajanson.github.io/issues">GitHub Issues</a> and displayed directly below. You need a GitHub account to write.</p>
<hr style="border-color:#2a2a2a; margin: 32px 0;">
<script src="https://utteranc.es/client.js"
        repo="OlaJanson/olajanson.github.io"
        issue-term="pathname"
        label="gästbok"
        theme="dark-blue"
        crossorigin="anonymous"
        async>
</script>
<hr style="border-color:#2a2a2a; margin: 32px 0;">
<p><em>Prefer to write without an account? Email <a href="mailto:ola.janson@gmail.com">ola.janson@gmail.com</a>.</em></p>""",
        "backlinks": [("/", "A mythomaniac in a lie detector factory")],
    },
    "jag": {
        "title": "Fragment",
        "tags": ["#meta", "#cv"],
        "image": "/arme-dith-trans.png",
        "image_alt": "Arme-dith",
        "body": """<p>I am a Swiss army knife, I usually say.</p>
<p>Or perhaps it's not a perfect description of what I am? With a Swiss army knife, its primary unique characteristic is its versatility. The individual tool isn't that impressive, but fitting them all into one single red unit is unique. And that's probably where I feel the analogy falls short. I remember as a child how annoyed I was that this red multi-tool couldn't be used in my treehouses — how the small saw was useless for cutting branches.</p>
<p>No, I rather think I should describe myself as a toolbox. But what does the toolbox contain?</p>
<p>Pedagogy, I would argue, is a well-used tool. I have worked on and off as a teacher, mainly in vocational colleges but also at universities and primary schools. I work to the best of my ability with formative assessment. Currently exclusively in online courses.</p>
<p>Design process and creative processes are something I have also spent many professional years with. Most recently as creative director at SKF. But before that, as a business developer at HiQ.</p>
<p>Game design. I have designed games — digital, board games, and role-playing games. Right now, it's mostly role-playing games. I constantly have a game project going but rarely finish it.</p>""",
        "backlinks": [("/varfor-digital-garden.en", "Why digital garden?"), ("/", "A mythomaniac in a lie detector factory")],
    },
    "treehouse": {
        "title": "Why are there so few pictures of treehouses built by children?",
        "tags": ["#enshitification", "#designprocess", "#algorithm"],
        "image": "/treehouse.png",
        "image_alt": "Treehouse built by adults",
        "body": """<p>What do these treehouses have in common?</p>
<p>None of them are built by children.</p>
<img src="/treehouse-1.png" alt="Treehouses searched for 'treehouse made by kids'">
<p>But let's change the search to "treehouse made by kids". Yeah right. Not even the example third from the left has the adult managed to keep their controlling fingers in check. Far too straight and tidy.</p>
<p>But this isn't about adults not letting children build treehouses — but why it's so incredibly difficult to find pictures of it. I remember doing a search maybe ten years ago and there were more pictures of children's treehouses then.</p>
<p>Consider that I'm sitting in front of my computer speculating wildly. Like many other +50 white men, I could work up some keyboard rage and blame adjacent modern phenomena. And sure, it probably has to do with children moving less in forests and fields today.</p>
<img src="/treehouse-bethany.jpg" alt="Treehouse by Bethany Weeks">
<p>But I choose to think that it's part of enshitification — how image searches have become more streamlined. How algorithms push forward picture after picture with conformist mush. I choose to direct my old man rage in that direction because I can't live with the thought that children no longer build deadly treehouses.</p>""",
        "backlinks": [("/", "A mythomaniac in a lie detector factory")],
    },
    "varfor-digital-garden": {
        "title": "Why digital garden?",
        "tags": ["#digitalgararden", "#webb"],
        "image": None,
        "image_alt": None,
        "body": """<p>I gave an assignment in one of the courses I'm currently teaching. It's called artistic realization in digital environments. My students were tasked with finding digital role models — but not focusing on the content, but on <em>how</em> they do it.</p>
<p>A student whose primary interest was in writing shared a page and said: "Maggie Appleton's, whose art/interests I'm not particularly interested in, but the website itself is roughly what I want to achieve." I immediately realized this was something out of the ordinary. Her site was where someone had sat down and thought, "how do I want it?" — disregarded templates, and just went for it. Built based on their own needs.</p>
<p>And that made me realize: how damn much we are stuck in other people's <a href="/businesschmodels.en">business models</a>. We are stuck because they have convinced us that this is the only way to do it.</p>
<p>I read on Maggie's page. I read her article on <a href="https://maggieappleton.com/garden-history">digital gardens</a>. I almost got angry, but mostly at myself — how the hell did I miss this? Why was I not invited to this party?</p>
<p>It precisely put its finger on what I've felt is missing in web contexts. Social media is about selling your content to someone else and being entirely in the hands of someone else's business model. Where you have zero control unless you are incredibly compliant and constantly trying to hack the code to go viral.</p>
<p>The advice if you're going to start a channel on any social media is always to find a concept. Only talk about one thing. And <a href="/jag.en">I</a> am broad and want to talk about everything. With my ADHD brain, everything is connected. It's part of the same cloud of concepts that always relate to each other.</p>
<p>In short — digital gardening is made for me. Then I don't know if it will just become another graveyard on the internet. Time will tell.</p>""",
        "backlinks": [("/", "A mythomaniac in a lie detector factory")],
    },
}

for slug, page in EN_PAGES.items():
    html = TEMPLATE.format(
        title=page["title"],
        slug=slug,
        tags_html=make_tags_html(page["tags"]),
        body=page["body"],
        backlinks_html=make_backlinks_html(page["backlinks"]),
        sidebar_left=make_sidebar_left(page.get("image"), page.get("image_alt", "")),
        mobile_image=make_mobile_image(page.get("image"), page.get("image_alt", "")),
    )
    out_path = os.path.join(CONTENT_DIR, f"{slug}.en.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"✓ {out_path}")

print("Engelska sidor klara!")
