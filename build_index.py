#!/usr/bin/env python3
"""Bygg startsidan: injicera brödtext (intro) och dynamiska kort från index.md + contentIndex.json.

Specialregel för startsidan: publicering får BARA uppdatera brödtexten.
Rubrik (hero-title) och bild (hero ::before) bor hårdkodade i index2.html och rörs aldrig.
Endast innehållet i <div class="intro-text">…</div> ersätts med intro-stycket ur index.md
(allt mellan ev. bild-embed och första ##-rubriken).

Korten genereras dynamiskt från Quartz contentIndex.json:
- De 4 vanligaste taggarna → kategorier med 2 artiklar vardera
- En "Senaste" kategori med de 2 senast modifierade artiklarna

Körs i deploy.yml efter `npx quartz build`. Skriver public/index.html (+ .en).
"""
import json
import os
import re
import sys
from pathlib import Path
from collections import Counter

# (markdown-källa, html-mall, utdata)  — html-mallen kopieras + intro injiceras
PAGES = [
    ("content/index.md",    "content/index2.html",   "public/index.html"),
    ("content/index.en.md", "content/index.en.html", "public/index.en.html"),
]
# index2.html sparas också rått (används av /index2)
EXTRA_COPIES = [("content/index2.html", "public/index2.html")]

# Taggar att ignorera (interna/strukturella)
IGNORE_TAGS = {"meta", "garden", "index"}
# Engelska suffix att filtrera bort i den svenska vyn
EN_SUFFIX = ".en"
# Prefix för Obsidian-taggar att strippa
TAG_PREFIX = "#"


def load_content_index(repo_root: str) -> dict:
    """Ladda Quartz contentIndex.json."""
    ci_path = os.path.join(repo_root, "public", "static", "contentIndex.json")
    if not os.path.exists(ci_path):
        print("  ⚠ contentIndex.json saknas — kör npx quartz build först", file=sys.stderr)
        return {}
    with open(ci_path, encoding="utf-8") as f:
        return json.load(f)


def is_swedish(slug: str) -> bool:
    return not slug.endswith(EN_SUFFIX)


def strip_tag(tag: str) -> str:
    return tag.lstrip(TAG_PREFIX).strip().lower()


def analyze_tags(content_index: dict) -> list[tuple[str, list[dict]]]:
    """Räkna taggar, hitta topp 4, returnera (kategori, [artiklar])."""
    tag_articles: dict[str, list[dict]] = {}
    for slug, entry in content_index.items():
        if not is_swedish(slug):
            continue
        if slug in ("index", "gästbok", "gastbok"):
            continue
        tags = [strip_tag(t) for t in entry.get("tags", [])]
        display_tags = [t for t in tags if t not in IGNORE_TAGS]
        if not display_tags:
            display_tags = ["övrigt"]
        for tag in display_tags:
            tag_articles.setdefault(tag, []).append({
                "slug": slug,
                "title": entry.get("title", slug),
                "tags": entry.get("tags", []),
                "content": entry.get("content", ""),
            })

    # Topp 4 taggar efter antal artiklar
    tag_counts = Counter({t: len(v) for t, v in tag_articles.items()})
    top4 = [t for t, _ in tag_counts.most_common(4)]

    result = []
    for tag in top4:
        articles = tag_articles.get(tag, [])
        # Ta max 2, prioritera de med rikast content som proxy för "bäst"
        articles.sort(key=lambda a: len(a.get("content", "")), reverse=True)
        result.append((tag, articles[:2]))

    return result


def get_latest_articles(content_index: dict, repo_root: str) -> list[dict]:
    """Hitta de 2 senast modifierade .md-filerna (svenska, ej index/gästbok)."""
    content_dir = os.path.join(repo_root, "content")
    candidates = []
    for slug, entry in content_index.items():
        if not is_swedish(slug):
            continue
        if slug in ("index", "gästbok", "gastbok"):
            continue
        fp = entry.get("filePath", "")
        md_path = os.path.join(content_dir, fp)
        mtime = os.path.getmtime(md_path) if os.path.exists(md_path) else 0
        candidates.append({
            **entry,
            "mtime": mtime,
        })
    candidates.sort(key=lambda a: a["mtime"], reverse=True)
    return candidates[:2]


def extract_intro(md_text: str) -> str:
    """Returnera intro-markdown: rader efter frontmatter + ev. ![[bild]],
    fram till första ##-rubriken."""
    md = re.sub(r"^---\n.*?\n---\n", "", md_text, count=1, flags=re.DOTALL)
    lines = md.splitlines()
    intro = []
    for line in lines:
        if line.lstrip().startswith("## "):
            break
        if re.match(r"\s*!\[\[?.*", line):  # hoppa över bild-embeds — bilden är låst i heron
            continue
        intro.append(line)
    return "\n".join(intro).strip()


def md_to_html(md: str) -> str:
    """Minimal markdown → HTML för intro-stycket (stycken, wiki-/md-länkar, fet/kursiv)."""
    paras = re.split(r"\n\s*\n", md.strip())
    out = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        p = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]",
                   lambda m: f'<a href="{m.group(1).strip()}">{m.group(2).strip()}</a>', p)
        p = re.sub(r"\[\[([^\]]+)\]\]",
                   lambda m: f'<a href="{m.group(1).strip()}">{m.group(1).strip()}</a>', p)
        p = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', p)
        p = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", p)
        p = re.sub(r"[ \t]*\n[ \t]*", "<br>\n", p)
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


def _extract_snippet(content: str, max_chars: int = 160) -> str:
    """Första meningsfulla meningen som kort beskrivning."""
    # Ta första stycket, rensa bort markdown-syntax
    first_para = content.split("\n\n")[0] if content else ""
    # Ta bort wikilinks [[]], markdown-länkar, bilder
    clean = re.sub(r"\[\[([^\]|]+)\|?[^\]]*\]\]", r"\1", first_para)
    clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
    clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean)
    clean = re.sub(r"[#*_>`]", "", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    if len(clean) > max_chars:
        clean = clean[:max_chars].rsplit(" ", 1)[0] + "…"
    return clean


def category_label(tag: str) -> str:
    """Översätt tag till läsbar kategorirubrik."""
    translations = {
        "storytelling": "Storytelling",
        "enshitification": "Enshitifiering",
        "enshittification": "Enshitifiering",
        "ai": "AI",
        "premiss": "Premisser",
        "process": "Process",
        "designprocess": "Designprocess",
        "game-design": "Speldesign",
        "ttrpg": "Rollspel",
        "comedian": "Humor",
        "likeablepersons": "Personer jag gillar",
        "iterativedesign": "Iterativ design",
        "digital-trädgård": "Digital trädgård",
        "övrigt": "Övrigt",
    }
    return translations.get(tag, tag.replace("-", " ").title())


def generate_cards_html(categories: list[tuple[str, list[dict]]], latest: list[dict]) -> str:
    """Generera HTML för alla kortsektioner."""
    html_parts = []

    for tag, articles in categories:
        label = category_label(tag)
        html_parts.append(f'        <section class="category-section">')
        html_parts.append(f'            <h2 class="category-title">{label}</h2>')
        html_parts.append(f'            <div class="cards-grid">')
        for a in articles:
            snippet = _extract_snippet(a.get("content", ""))
            html_parts.append(f'                <a class="card" href="./{a["slug"]}">')
            html_parts.append(f'                    <span class="card-icon">▸</span>')
            html_parts.append(f'                    <div>')
            html_parts.append(f'                        <div class="card-title">{a["title"]}</div>')
            html_parts.append(f'                        <div class="card-sub">{snippet}</div>')
            html_parts.append(f'                    </div>')
            html_parts.append(f'                </a>')
        html_parts.append(f'            </div>')
        html_parts.append(f'        </section>')

    # Senaste
    if latest:
        html_parts.append(f'        <section class="category-section">')
        html_parts.append(f'            <h2 class="category-title">Senaste</h2>')
        html_parts.append(f'            <div class="cards-grid">')
        for a in latest:
            snippet = _extract_snippet(a.get("content", ""))
            html_parts.append(f'                <a class="card" href="./{a["slug"]}">')
            html_parts.append(f'                    <span class="card-icon">▸</span>')
            html_parts.append(f'                    <div>')
            html_parts.append(f'                        <div class="card-title">{a["title"]}</div>')
            html_parts.append(f'                        <div class="card-sub">{snippet}</div>')
            html_parts.append(f'                    </div>')
            html_parts.append(f'                </a>')
        html_parts.append(f'            </div>')
        html_parts.append(f'        </section>')

    return "\n".join(html_parts)


def inject_intro(html: str, intro_html: str) -> str:
    """Ersätt innehållet i <div class="intro-text">…</div> (innehåller bara <p>)."""
    pattern = re.compile(r'(<div class="intro-text">)(.*?)(</div>)', re.DOTALL)
    if not pattern.search(html):
        print("  ⚠ hittade ingen .intro-text — lämnar mallen orörd", file=sys.stderr)
        return html
    return pattern.sub(lambda m: m.group(1) + "\n" + intro_html + "\n" + m.group(3), html, count=1)


def inject_cards(html: str, cards_html: str) -> str:
    """Ersätt <!-- CARD-SECTION --> med den genererade korthandeln."""
    marker = "<!-- CARD-SECTION -->"
    if marker not in html:
        print("  ⚠ hittade ingen CARD-SECTION-marker — lämnar mallen orörd", file=sys.stderr)
        return html
    return html.replace(marker, "\n" + cards_html + "\n", 1)


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    content_index = load_content_index(repo_root)

    categories = []
    latest = []
    if content_index:
        categories = analyze_tags(content_index)
        latest = get_latest_articles(content_index, repo_root)
        print(f"  [dynamiska kort] {len(categories)} kategorier, {sum(len(a) for _, a in categories)} kort, {len(latest)} senaste")

    for md_path, tmpl_path, out_path in PAGES:
        if not (os.path.exists(md_path) and os.path.exists(tmpl_path)):
            print(f"  • hoppar över {out_path} (saknar {md_path} eller {tmpl_path})")
            continue
        with open(md_path, encoding="utf-8") as f:
            intro_html = md_to_html(extract_intro(f.read()))
        with open(tmpl_path, encoding="utf-8") as f:
            html = inject_intro(f.read(), intro_html)
        html = inject_cards(html, generate_cards_html(categories, latest))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ {out_path}  ({intro_html.count('<p>')} stycke(n) brödtext från {md_path})")
    for src, dst in EXTRA_COPIES:
        if os.path.exists(src):
            with open(src, encoding="utf-8") as f:
                data = inject_cards(f.read(), generate_cards_html(categories, latest))
            with open(dst, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"  ✓ {dst} (rå kopia)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
