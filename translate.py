#!/usr/bin/env python3
"""Translate Swedish .md articles to English using mistral-nemo (Janus) via Ollama.

Usage:
  python translate.py                        # translate all missing .en.md in content/
  python translate.py content/article.md    # translate specific file
"""

import sys
import json
import re
import urllib.request
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral-nemo"

# Mirror .en.md files here for editing in Obsidian (set to None to disable)
OBSIDIAN_MIRROR = Path.home() / "Dokument/Vaul II/5. Utveckla/digital-garden/publicerat"

PROMPT = """Translate the following Swedish markdown article to natural, fluent English.

Rules:
- Preserve ALL markdown formatting exactly (**, *, #, >, -, [ ], etc.)
- Preserve ALL wiki-links exactly as-is: [[link|text]] — keep brackets and pipe
- Preserve ALL URLs unchanged
- For YAML frontmatter: only translate the title value; keep all keys and other values unchanged
- Keep the author's personal, conversational voice and tone
- Output ONLY the translated text — no explanations, no preamble, nothing else

Article:
---
{text}"""


def translate(text: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": PROMPT.format(text=text),
        "stream": False,
        "options": {"temperature": 0.3},
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read())["response"].strip()


def add_en_to_wikilinks(text: str) -> str:
    """Add .en to wikilink targets so they point to English pages."""
    def replace(m):
        target = m.group(1).strip()
        display = m.group(2)
        if target.endswith(".en") or "://" in target:
            return m.group(0)
        new_target = f"{target}.en"
        return f"[[{new_target}|{display.strip()}]]" if display else f"[[{new_target}]]"

    return re.sub(r"\[\[([^\]|#]+)(?:\|([^\]]*))?\]\]", replace, text)


def translate_file(src: Path) -> Path:
    en_path = src.parent / f"{src.stem}.en.md"
    print(f"  {src.name} → {en_path.name} ...", end=" ", flush=True)
    content = src.read_text(encoding="utf-8")
    translated = translate(content)
    translated = add_en_to_wikilinks(translated)
    en_path.write_text(translated, encoding="utf-8")
    if OBSIDIAN_MIRROR and OBSIDIAN_MIRROR.exists():
        (OBSIDIAN_MIRROR / en_path.name).write_text(translated, encoding="utf-8")
    print("✓")
    return en_path


def find_untranslated(content_dir: Path) -> list:
    sv_files = [f for f in content_dir.glob("*.md") if not f.stem.endswith(".en")]
    return [f for f in sv_files if not (content_dir / f"{f.stem}.en.md").exists()]


if __name__ == "__main__":
    content_dir = Path(__file__).parent / "content"

    if len(sys.argv) > 1:
        files = [Path(a) for a in sys.argv[1:]]
    else:
        files = find_untranslated(content_dir)

    if not files:
        print("All articles already have English versions.")
        sys.exit(0)

    print(f"Translating {len(files)} file(s) with Janus (mistral-nemo)...")
    for f in files:
        translate_file(f)
    print("Done.")
