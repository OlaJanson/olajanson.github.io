#!/usr/bin/env python3
"""Bygg startsidan: injicera brödtexten (intro) från index.md in i index2.html.

Specialregel för startsidan: publicering får BARA uppdatera brödtexten.
Rubrik (hero-title), bild (hero ::before) och korten (category-section) bor
hårdkodade i index2.html och rörs aldrig. Endast innehållet i
<div class="intro-text">…</div> ersätts med intro-stycket ur index.md
(allt mellan ev. bild-embed och första ##-rubriken).

Körs i deploy.yml efter `npx quartz build`. Skriver public/index.html (+ .en).
"""
import os
import re
import sys

# (markdown-källa, html-mall, utdata)  — html-mallen kopieras + intro injiceras
PAGES = [
    ("content/index.md",    "content/index2.html",   "public/index.html"),
    ("content/index.en.md", "content/index.en.html", "public/index.en.html"),
]
# index2.html sparas också rått (används av /index2)
EXTRA_COPIES = [("content/index2.html", "public/index2.html")]


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
        p = re.sub(r"\s*\n\s*", " ", p)  # mjuka radbrytningar → mellanslag (som Quartz)
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


def inject_intro(html: str, intro_html: str) -> str:
    """Ersätt innehållet i <div class="intro-text">…</div> (innehåller bara <p>)."""
    pattern = re.compile(r'(<div class="intro-text">)(.*?)(</div>)', re.DOTALL)
    if not pattern.search(html):
        print("  ⚠ hittade ingen .intro-text — lämnar mallen orörd", file=sys.stderr)
        return html
    return pattern.sub(lambda m: m.group(1) + "\n" + intro_html + "\n" + m.group(3), html, count=1)


def main() -> int:
    for md_path, tmpl_path, out_path in PAGES:
        if not (os.path.exists(md_path) and os.path.exists(tmpl_path)):
            print(f"  • hoppar över {out_path} (saknar {md_path} eller {tmpl_path})")
            continue
        with open(md_path, encoding="utf-8") as f:
            intro_html = md_to_html(extract_intro(f.read()))
        with open(tmpl_path, encoding="utf-8") as f:
            html = inject_intro(f.read(), intro_html)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ {out_path}  ({intro_html.count('<p>')} stycke(n) brödtext från {md_path})")
    for src, dst in EXTRA_COPIES:
        if os.path.exists(src):
            with open(src, encoding="utf-8") as f:
                data = f.read()
            with open(dst, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"  ✓ {dst} (rå kopia)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
