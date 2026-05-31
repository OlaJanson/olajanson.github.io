#!/usr/bin/env python3
"""
Auto-translate Swedish markdown to English using Gemini API.
Always overwrites existing .en.md.
"""
import sys, os, re
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"

def get_known_slugs():
    """Return set of Swedish slugs that have content files."""
    slugs = set()
    for f in CONTENT_DIR.glob("*.md"):
        if not f.name.endswith(".en.md"):
            slugs.add(f.stem)
    return slugs

def fix_wikilinks(text, known_slugs):
    """
    Fix wiki-links in translated text:
    - [[slug]] → [[slug.en]] if slug exists as a page
    - [[slug|display]] → [[slug.en|display]] if slug exists
    - Leave image links and external URLs as-is
    """
    def replace_link(m):
        inner = m.group(1)
        if "|" in inner:
            target, display = inner.split("|", 1)
        else:
            target, display = inner, None

        # Skip images, external URLs, and already-en links
        if any(target.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
            return m.group(0)
        if target.startswith("http"):
            return m.group(0)
        if target.endswith(".en"):
            return m.group(0)

        # If target is a known slug, add .en
        if target in known_slugs:
            new_target = target + ".en"
            if display:
                return f"[[{new_target}|{display}]]"
            return f"[[{new_target}]]"

        return m.group(0)

    return re.sub(r"\[\[([^\]]+)\]\]", replace_link, text)

def translate_with_gemini(text, src_path):
    import urllib.request, json
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        env_file = Path.home() / "whatsapp-bot/.env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    if not api_key:
        print(f"  No GEMINI_API_KEY — skipping translation for {src_path}", file=sys.stderr)
        return None

    prompt = f"""Translate this Swedish markdown file to English.

RULES — follow exactly:
1. Translate all natural language text (body text, titles, descriptions).
2. Keep ALL frontmatter fields. Only translate the value of the "title" field.
3. Keep ALL wiki-links exactly as written: [[target]] or [[target|display]].
   - Do NOT translate the target (the part before |).
   - You MAY translate the display text (the part after |).
   - Example: [[jag|I am]] → [[jag|I am]]  (keep "jag", translate "I am" if needed)
4. Keep ALL markdown formatting, HTML tags, code blocks, and image references exactly as-is.
5. Do NOT wrap output in markdown code fences.

{text}"""

    body = json.dumps({
        "model": "gemini-2.5-flash",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 8192
    }).encode()
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]

def main():
    if len(sys.argv) < 2:
        print("Usage: translate.py <file.md>", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1])
    en_path = src.parent / (src.stem + ".en.md")

    print(f"  Translating {src.name} → {en_path.name}...")
    try:
        translated = translate_with_gemini(src.read_text(), src)
        if translated:
            # Strip markdown code fences that Gemini sometimes adds anyway
            translated = translated.strip()
            if translated.startswith("```"):
                lines = translated.splitlines()
                translated = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

            # Fix wiki-links: add .en suffix to known internal slugs
            known_slugs = get_known_slugs()
            translated = fix_wikilinks(translated, known_slugs)

            en_path.write_text(translated)
            print(f"  ✓ {en_path.name} created")
        else:
            en_path.write_text(src.read_text())
            print(f"  ✓ {en_path.name} copied (no translation — add GEMINI_API_KEY)")
    except Exception as e:
        print(f"  Translation error: {e} — copying original", file=sys.stderr)
        en_path.write_text(src.read_text())

if __name__ == "__main__":
    main()
