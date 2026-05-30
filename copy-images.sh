#!/bin/bash
# Kopiera bilder refererade med ![[...]] i en artikel till content/
# Användning: ./copy-images.sh content/artikel.md
VAULT_ATTACHED="/home/ola/Dokument/Vaul II/6. Verktyg/Attached"
CONTENT_DIR="$(dirname "$0")/content"
ARTICLE="$1"

if [ -z "$ARTICLE" ]; then
  echo "Användning: $0 content/artikel.md"
  exit 1
fi

FOUND=0
grep -oP '(?<=\[\[)[^\]|]+\.(png|jpg|jpeg|gif|webp|svg)' "$ARTICLE" | while read img; do
  src="$VAULT_ATTACHED/$img"
  dst="$CONTENT_DIR/$img"
  if [ -f "$src" ] && [ ! -f "$dst" ]; then
    cp "$src" "$dst"
    echo "  ✓ kopierade: $img"
    FOUND=1
  elif [ -f "$dst" ]; then
    echo "  · redan finns: $img"
  else
    echo "  ✗ hittades inte: $img"
  fi
done
