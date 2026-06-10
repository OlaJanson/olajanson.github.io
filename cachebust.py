#!/usr/bin/env python3
"""Cache-busting: lägg innehålls-hash på index.css-referenser i all HTML.

GitHub Pages serverar index.css med cache-control: max-age=600 utan hash, så i
10 min efter en deploy visar webbläsaren GAMMAL cachad CSS vid navigering (man
måste refresha). Genom att referera index.css?v=<hash> får varje deploy med
ändrad CSS en unik URL → webbläsaren hämtar alltid den nya automatiskt.

Körs i deploy.yml efter `npx quartz build` + `build_index.py`.
"""
import hashlib
import glob
import os
import re
import sys

CSS = "public/index.css"


def main() -> int:
    if not os.path.exists(CSS):
        print(f"  ⚠ {CSS} saknas — hoppar cache-busting", file=sys.stderr)
        return 0
    h = hashlib.md5(open(CSS, "rb").read()).hexdigest()[:8]
    n = 0
    for html in glob.glob("public/**/*.html", recursive=True):
        with open(html, encoding="utf-8") as f:
            t = f.read()
        # ersätt index.css ev. med befintlig ?v=… → ny hash
        new = re.sub(r"(index\.css)(\?v=[a-f0-9]+)?", rf"\1?v={h}", t)
        if new != t:
            with open(html, "w", encoding="utf-8") as f:
                f.write(new)
            n += 1
    print(f"  ✓ cache-bust: index.css?v={h} i {n} HTML-filer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
