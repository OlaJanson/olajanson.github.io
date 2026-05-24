#!/usr/bin/env python3
"""Auto-translate Swedish Quartz content to English using Gemini."""

import os
import re
import sys
import json
import subprocess
import urllib.request

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

LANG_EN_MARKER = 'class="lang-en"'


def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end]
    body = content[end + 4:].lstrip("\n")
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"')
    return fm, body


def is_published(fm):
    val = fm.get("publish", "false")
    return str(val).lower() in ("true", "\"true\"", "'true'")


def translate(text):
    prompt = (
        "Translate the following Swedish markdown text to English. "
        "Preserve all markdown formatting, HTML tags, links, and code blocks exactly. "
        "Only translate the natural language text. "
        "Return only the translated markdown, no explanation.\n\n"
        f"{text}"
    )
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }).encode()
    req = urllib.request.Request(
        GEMINI_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["candidates"][0]["content"]["parts"][0]["text"]


def process_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()

    if LANG_EN_MARKER in raw:
        print(f"  skip (already translated): {filepath}")
        return False

    fm, body = parse_frontmatter(raw)

    if not is_published(fm):
        print(f"  skip (not published): {filepath}")
        return False

    print(f"  translating: {filepath}")
    english = translate(body)

    end = raw.find("\n---", 3)
    fm_block = raw[:end + 4]

    new_body = (
        '<div class="lang-sv">\n\n'
        + body.rstrip("\n")
        + '\n\n</div>\n\n'
        + '<div class="lang-en">\n\n'
        + english.rstrip("\n")
        + '\n\n</div>\n'
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fm_block + "\n" + new_body)

    return True


def get_changed_md_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True, text=True
    )
    return [
        f for f in result.stdout.strip().splitlines()
        if f.startswith("content/") and f.endswith(".md")
    ]


if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else get_changed_md_files()
    changed = [f for f in files if os.path.exists(f) and process_file(f)]

    if changed:
        print(f"\nTranslated {len(changed)} file(s): {changed}")
    else:
        print("No files needed translation.")
