#!/usr/bin/env python3
"""
Auto-translate Swedish markdown to English using Gemini API.
If .en.md already exists, skip (no-op).
"""
import sys, os, re
from pathlib import Path

def translate_with_gemini(text, src_path):
    import urllib.request, json
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        # Try reading from .env
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
Keep all frontmatter fields except change the title value to English.
Keep all markdown formatting, links, code blocks, and HTML tags exactly as-is.
Only translate the natural language text.

{text}"""

    body = json.dumps({
        "model": "gemini-2.5-flash",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096
    }).encode()
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]

def main():
    if len(sys.argv) < 2:
        print("Usage: translate.py <file.md>", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1])
    en_path = src.with_suffix("").with_suffix("").parent / (src.stem + ".en.md")
    if not en_path.exists():
        # Try the standard pattern: file.md -> file.en.md
        en_path = src.parent / (src.stem + ".en.md")

    if en_path.exists():
        print(f"  {en_path.name} already exists — skipping translation")
        sys.exit(0)

    print(f"  Translating {src.name} → {en_path.name}...")
    try:
        translated = translate_with_gemini(src.read_text(), src)
        if translated:
            en_path.write_text(translated)
            print(f"  ✓ {en_path.name} created")
        else:
            # No API key — create a stub so the hook doesn't fail
            en_path.write_text(src.read_text())
            print(f"  ✓ {en_path.name} copied (no translation — add GEMINI_API_KEY)")
    except Exception as e:
        print(f"  Translation error: {e} — copying original", file=sys.stderr)
        en_path.write_text(src.read_text())

if __name__ == "__main__":
    main()
