#!/usr/bin/env python3
"""Inject the Fathom Analytics tag into every class page in public/.

Idempotent: pages that already contain it are left alone.
Run by ~/gati/publish.sh on every deploy (the local ~/gati/sites copies stay tag-free).
"""
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
TAG = '<script src="https://cdn.usefathom.com/script.js" data-site="OMTQDNRH" defer></script>'

n = 0
for page in sorted(PUBLIC.glob("*/index.html")):
    if page.parent.name.startswith("_"):
        continue
    text = page.read_text()
    if "cdn.usefathom.com" in text:
        continue
    new, hits = re.subn(r"</head>", "  " + TAG + "\n</head>", text, count=1, flags=re.I)
    if hits:
        page.write_text(new)
        n += 1
print(f"analytics added to {n} page(s)")
