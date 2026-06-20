#!/usr/bin/env python3
"""Läser Staticman YAML-filer från _data/gastbok/ och genererar JSON för gästbokssidan."""
import yaml, json, sys
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "_data" / "gastbok"
OUT_FILE = Path(__file__).resolve().parent.parent / "quartz" / "static" / "gastbok-entries.json"

entries = []
if DATA_DIR.is_dir():
    for yf in sorted(DATA_DIR.glob("*.yml"), reverse=True):
        try:
            data = yaml.safe_load(yf.read_text())
            name = data.get("name", "Anonym")
            message = data.get("message", "")
            url = data.get("url", "")
            date_str = data.get("date", "")
            try:
                ts = datetime.fromisoformat(date_str)
                date_str = ts.strftime("%-d %B %Y")
            except ValueError:
                pass
            entries.append({
                "name": str(name),
                "message": str(message),
                "url": str(url),
                "date": str(date_str),
            })
        except Exception as e:
            print(f"  [gastbok] Hoppar över {yf.name}: {e}", file=sys.stderr)

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2))
print(f"  [gastbok] {len(entries)} inlägg → {OUT_FILE}")
