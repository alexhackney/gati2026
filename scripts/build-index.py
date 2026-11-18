#!/usr/bin/env python3
"""Regenerate the root index.html by listing every class folder.

A class folder is any top-level directory containing an index.html.
Its title is taken from the <title> tag of that index.html.
Run from anywhere:  python3 scripts/build-index.py
"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"scripts", "assets"}


def title_of(page: Path, fallback: str) -> str:
    m = re.search(r"<title>(.*?)</title>", page.read_text(errors="ignore"), re.I | re.S)
    return html.unescape(m.group(1).strip()) if m and m.group(1).strip() else fallback


classes = []
for d in sorted(ROOT.iterdir()):
    if d.is_dir() and not d.name.startswith((".", "_")) and d.name not in SKIP and (d / "index.html").exists():
        classes.append((d.name, title_of(d / "index.html", d.name.replace("-", " ").title())))

cards = "\n".join(
    f'      <a class="card" href="{html.escape(n)}/"><strong>{html.escape(t)}</strong><span>/{html.escape(n)}/</span></a>'
    for n, t in classes
) or "      <p>No classes yet.</p>"

(ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Great American Teach-In 2026</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 0; background: #f4f7ff; color: #1b2340; }}
    header {{ padding: 3rem 1rem 1.5rem; text-align: center; }}
    h1 {{ margin: 0 0 .5rem; font-size: clamp(1.8rem, 5vw, 3rem); }}
    main {{ max-width: 900px; margin: 0 auto; padding: 1rem; display: grid; gap: 1rem;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }}
    .card {{ display: flex; flex-direction: column; gap: .3rem; padding: 1.2rem; background: #fff;
             border-radius: 14px; text-decoration: none; color: inherit;
             box-shadow: 0 2px 8px rgba(0,0,0,.08); transition: transform .1s; }}
    .card:hover {{ transform: translateY(-3px); }}
    .card span {{ color: #6b7391; font-size: .85rem; }}
  </style>
</head>
<body>
  <header><h1>Great American Teach-In 2026</h1><p>Websites and games made with our classes.</p></header>
  <main>
{cards}
  </main>
</body>
</html>
""")
print(f"index.html built with {len(classes)} class(es)")
