#!/usr/bin/env python3
"""
Auto-translate changed Swedish .md files to English.
Called by GitHub Actions on push to v5 branch.
Always overwrites existing .en.md so updates stay in sync.
"""

import os
import sys
import json
import subprocess
import urllib.request


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key={key}"
)


def gemini(text, key):
    url = GEMINI_URL.format(key=key)
    payload = json.dumps({
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"temperature": 0.2},
    }).encode()
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def parse_frontmatter(content):
    if not content.startswith("---"):
        return "", content
    end = content.find("\n---", 3)
    if end == -1:
        return "", content
    fm_raw = content[:end + 4]
    body = content[end + 4:].lstrip("\n")
    return fm_raw, body


def is_published(fm_raw):
    in_publish = False
    for line in fm_raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("publish:"):
            val = stripped[8:].strip().strip("\"'")
            if val.lower() == "true":
                return True
            in_publish = True
            continue
        if in_publish:
            if stripped.startswith("-"):
                val = stripped[1:].strip().strip("\"'")
                if val.lower() == "true":
                    return True
            elif stripped and not stripped.startswith(" "):
                in_publish = False
    return False


def get_title(fm_raw):
    for line in fm_raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("title:"):
            return stripped[6:].strip().strip("\"'")
    return ""


def build_en_frontmatter(fm_raw, en_title):
    lines = []
    for line in fm_raw.splitlines():
        if line.strip().startswith("title:"):
            lines.append(f"title: {en_title}")
        else:
            lines.append(line)
    return "\n".join(lines)


def translate_file(filepath, key):
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()

    fm_raw, body = parse_frontmatter(raw)

    if not is_published(fm_raw):
        print(f"  skip (not published): {filepath}")
        return None

    print(f"  translating: {filepath} ...", flush=True)

    sv_title = get_title(fm_raw)
    if sv_title:
        en_title = gemini(
            "Translate this Swedish title to English. "
            "Return only the translated title, nothing else.\n\n" + sv_title,
            key,
        )
    else:
        en_title = ""

    en_body = gemini(
        "Translate the following Swedish markdown text to natural, fluent English. "
        "Preserve markdown formatting, external links, and code blocks exactly. "
        "For wiki-links [[target|alias]]: keep the target (before the | ) UNCHANGED, "
        "but translate the visible alias (after the | ) to English. "
        "For [[target]] without an alias, leave it unchanged. "
        "Example: [[varfor-digital-garden|digital trädgård]] -> [[varfor-digital-garden|digital garden]]; "
        "[[jag|Jag]] -> [[jag|I]]. "
        "Only translate natural language text. Return only the translated markdown, no explanation.\n\n" + body,
        key,
    )

    en_fm = build_en_frontmatter(fm_raw, en_title)
    en_path = filepath.replace(".md", ".en.md")

    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_fm + "\n" + en_body + "\n")

    print(f"  done -> {en_path}")
    return en_path


def _git_mtime(path):
    """Senaste commit-tidsstämpel (epoch) för en fil; 0 om okänd. Kräver git-historik
    (fetch-depth: 0) — disk-mtime är opålitlig efter en fräsch checkout."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", path],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return int(out) if out else 0
    except (subprocess.CalledProcessError, ValueError):
        return 0


def changed_sv_files():
    """TILLSTÅNDSBASERAD detektion: returnera varje svensk .md vars engelska
    motsvarighet SAKNAS eller är ÄLDRE (stale). Robust mot commit-/push-struktur
    och självläkande — fångar UPPDATERINGAR som gamla diff-baserade (`HEAD~1 HEAD`)
    detektionen tappade vid batchade/multi-commit-pushar. (is_published filtrerar
    bort opublicerade i translate_file.)"""
    stale = []
    for root, _, fnames in os.walk("content"):
        for fname in fnames:
            if not fname.endswith(".md") or fname.endswith(".en.md"):
                continue
            md = os.path.join(root, fname)
            en = md[:-3] + ".en.md"
            if not os.path.exists(en) or _git_mtime(md) > _git_mtime(en):
                stale.append(md)
    return stale


def main():
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        print("ERROR: GEMINI_API_KEY saknas")
        sys.exit(1)

    files = sys.argv[1:] if len(sys.argv) > 1 else changed_sv_files()

    if not files:
        print("Inga svenska .md-filer ändrade.")
        return

    print(f"Processar {len(files)} fil(er)...\n")
    generated = [f for f in files if os.path.exists(f) and translate_file(f, key)]

    print(f"\n{'=' * 40}")
    if generated:
        print(f"Genererat/uppdaterat {len(generated)} .en.md-fil(er):")
        for f in generated:
            print(f"  ✓ {f.replace('.md', '.en.md')}")
    else:
        print("Inget att översätta.")


if __name__ == "__main__":
    main()
