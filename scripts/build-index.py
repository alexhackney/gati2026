#!/usr/bin/env python3
"""Regenerate public/index.html by listing every class folder in public/.

A class folder is any directory in public/ containing an index.html.
Its title is taken from the <title> tag of that index.html.
Run from anywhere:  python3 scripts/build-index.py
"""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "public"
SKIP = {"assets"}


def title_of(page: Path, fallback: str) -> str:
    m = re.search(r"<title>(.*?)</title>", page.read_text(errors="ignore"), re.I | re.S)
    return html.unescape(m.group(1).strip()) if m and m.group(1).strip() else fallback


def grade_of(folder: Path):
    """Grade from <class>/meta.json ({"grade": 3}); None if absent."""
    try:
        return int(json.loads((folder / "meta.json").read_text())["grade"])
    except Exception:
        return None


classes = []
for d in sorted(ROOT.iterdir()):
    if d.is_dir() and not d.name.startswith((".", "_")) and d.name not in SKIP and (d / "index.html").exists():
        classes.append((d.name, title_of(d / "index.html", d.name.replace("-", " ").title()), grade_of(d)))

# lowest grade first, classes without a grade last, then alphabetical by title
classes.sort(key=lambda c: (c[2] is None, c[2] or 0, c[1].lower()))

cards = "\n".join(
    f'      <a class="card" style="--i:{i}" href="{html.escape(n)}/">'
    f'<span class="num">{i + 1:02d}.</span>'
    + (f'<span class="grade">Grade {g}</span>' if g else '')
    + f'<strong>{html.escape(t)}</strong>'
    f'<code>/{html.escape(n)}/</code>'
    f'<span class="go">open &rarr;</span></a>'
    for i, (n, t, g) in enumerate(classes)
) or '      <p class="empty">// no classes yet</p>'

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Great American Teach-In 2026 | Pinellas Academy of Math and Science</title>
  <meta name="description" content="Websites and games built live with classrooms at Pinellas Academy of Math and Science for the Great American Teach-In 2026.">
  <script src="https://cdn.usefathom.com/script.js" data-site="OMTQDNRH" defer></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0a0a0f; --card: #12121a; --line: #1a1a25;
      --text: #e5e7eb; --muted: #9ca3af;
      --blue: #3b82f6; --purple: #8b5cf6; --red: #ef4444;
      --grad: linear-gradient(90deg, var(--blue), var(--purple), var(--red));
      --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin: 0; background: var(--bg); color: var(--text);
           font-family: Inter, system-ui, sans-serif; min-height: 100vh; }
    #rain { position: fixed; inset: 0; width: 100%; height: 100%; z-index: 0;
            pointer-events: none; opacity: .5; }
    /* soft vignette keeps text readable over the rain */
    body::before { content: ""; position: fixed; inset: 0; z-index: 1; pointer-events: none;
      background: radial-gradient(ellipse at 50% 35%, rgba(10,10,15,.15) 0%, rgba(10,10,15,.85) 75%); }
    nav, header, main, footer { position: relative; z-index: 2; }
    nav { position: sticky; top: 0; z-index: 3; display: flex; justify-content: space-between;
          align-items: center; padding: .9rem 1.5rem; background: rgba(10,10,15,.7);
          backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
          border-bottom: 1px solid var(--line); }
    .logo { font-family: var(--mono); font-weight: 500; }
    .logo b { background: var(--grad); -webkit-background-clip: text; background-clip: text; color: transparent; }
    .logo i { color: var(--muted); font-style: normal; }
    nav a.link { color: var(--muted); text-decoration: none; font-size: .9rem; margin-left: 1.2rem; }
    nav a.link:hover { color: var(--text); }
    header { text-align: center; padding: 6rem 1.5rem 3rem; max-width: 900px; margin: 0 auto; }
    .tag { font-family: var(--mono); color: var(--blue); font-size: .95rem; letter-spacing: .05em; }
    .school { margin-top: 1.1rem; font-size: clamp(1.1rem, 3.5vw, 1.6rem); font-weight: 600; letter-spacing: .02em; }
    h1 { font-size: clamp(2.4rem, 8vw, 4.6rem); line-height: 1.05; font-weight: 800; margin: .8rem 0 1rem; letter-spacing: -.02em; }
    h1 span { background: var(--grad); -webkit-background-clip: text; background-clip: text; color: transparent; }
    .sub { color: var(--muted); font-size: 1.15rem; max-width: 560px; margin: 0 auto; line-height: 1.6; }
    .stats { display: flex; justify-content: center; gap: 3rem; margin-top: 2.5rem; font-family: var(--mono); }
    .stats div strong { display: block; font-size: 2rem; color: var(--text); }
    .stats div span { color: var(--muted); font-size: .8rem; }
    .section-title { max-width: 1000px; margin: 1rem auto 0; padding: 0 1.5rem;
                     font-family: var(--mono); color: var(--muted); font-size: .9rem; }
    .section-title b { color: var(--purple); font-weight: 500; }
    main { max-width: 1000px; margin: 0 auto; padding: 1.2rem 1.5rem 5rem; display: grid; gap: 1.1rem;
           grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }
    .card { position: relative; display: flex; flex-direction: column; gap: .45rem; padding: 1.4rem;
            background: rgba(18,18,26,.82); border: 1px solid var(--line); border-radius: 14px;
            text-decoration: none; color: inherit; backdrop-filter: blur(4px);
            transition: transform .15s, border-color .15s, box-shadow .15s;
            opacity: 0; animation: rise .5s ease forwards; animation-delay: calc(var(--i) * 70ms); }
    .card:hover { transform: translateY(-4px); border-color: var(--purple);
                  box-shadow: 0 8px 30px rgba(139,92,246,.25); }
    .card .num { font-family: var(--mono); color: var(--blue); font-size: .85rem; }
    .card .grade { position: absolute; top: 1.2rem; right: 1.2rem; font-family: var(--mono); font-size: .75rem;
                   padding: .2rem .6rem; border-radius: 999px; color: var(--text);
                   background: linear-gradient(90deg, rgba(59,130,246,.25), rgba(139,92,246,.25));
                   border: 1px solid rgba(139,92,246,.5); }
    .card strong { font-size: 1.25rem; font-weight: 600; }
    .card code { font-family: var(--mono); color: var(--muted); font-size: .8rem; }
    .card .go { margin-top: .6rem; font-family: var(--mono); font-size: .85rem; color: var(--purple); }
    .empty { grid-column: 1 / -1; text-align: center; font-family: var(--mono); color: var(--muted); }
    footer { text-align: center; padding: 2rem 1rem 3rem; color: var(--muted); font-family: var(--mono); font-size: .8rem; line-height: 1.8; }
    footer .thanks { color: var(--text); font-size: .95rem; margin: 0 0 .6rem; }
    footer a { color: var(--purple); text-decoration: none; border-bottom: 1px solid rgba(139,92,246,.5); }
    footer a:hover { color: var(--text); }
    @keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
    @media (prefers-reduced-motion: reduce) { .card { animation: none; opacity: 1; } }
    @media (max-width: 560px) { .stats { gap: 1.5rem; } header { padding-top: 4rem; } }
  </style>
</head>
<body>
  <canvas id="rain" aria-hidden="true"></canvas>

  <nav>
    <div class="logo"><b>GATI</b> <i>//</i> 2026</div>
    <div><a class="link" href="#classes">Classes</a></div>
  </nav>

  <header>
    <div class="tag">&lt; Great American Teach-In /&gt;</div>
    <div class="school">Pinellas Academy of Math and Science</div>
    <h1>Built live in the <span>classroom</span></h1>
    <p class="sub">Websites and games made together with students, one idea shouted from the back row at a time.</p>
    <div class="stats">
      <div><strong>__COUNT__</strong><span>classes</span></div>
      <div><strong>100%</strong><span>kid ideas</span></div>
      <div><strong>0</strong><span>bugs (probably)</span></div>
    </div>
  </header>

  <div class="section-title" id="classes"><b>01.</b> Our Classes</div>
  <main>
__CARDS__
  </main>

  <footer>
    <p class="thanks">Thank you for having me! &mdash; Alex</p>
    <div>See the code we built today: <a href="https://github.com/alexhackney/gati2026">github.com/alexhackney/gati2026</a></div>
    <div>&copy; 2026 // Pinellas Academy of Math and Science // built with kids &amp; code</div>
  </footer>

  <script>
  (function () {
    var c = document.getElementById('rain'), ctx = c.getContext('2d');
    var chars = '01<>/{}=+アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワ'.split('');
    var size = 16, drops = [], last = 0;
    var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function resize() {
      c.width = innerWidth; c.height = innerHeight;
      var cols = Math.ceil(c.width / size);
      while (drops.length < cols) drops.push(Math.random() * -50);
      drops.length = cols;
      ctx.fillStyle = '#0a0a0f'; ctx.fillRect(0, 0, c.width, c.height);
    }
    function frame(t) {
      if (t - last > 55) {            // ~18fps: calm, cheap on the projector laptop
        last = t;
        ctx.fillStyle = 'rgba(10,10,15,0.09)';
        ctx.fillRect(0, 0, c.width, c.height);
        ctx.font = size + 'px "JetBrains Mono", monospace';
        for (var i = 0; i < drops.length; i++) {
          var ch = chars[Math.floor(Math.random() * chars.length)], x = i * size, y = drops[i] * size;
          ctx.fillStyle = Math.random() > .93 ? '#ef4444' : (i % 2 ? '#3b82f6' : '#8b5cf6');
          ctx.fillText(ch, x, y);
          if (y > c.height && Math.random() > .975) drops[i] = 0;
          drops[i]++;
        }
      }
      if (!still) requestAnimationFrame(frame);
    }
    addEventListener('resize', resize);
    resize();
    if (still) { for (var k = 0; k < 60; k++) frame(k * 100); } else { requestAnimationFrame(frame); }
  })();
  </script>
</body>
</html>
"""

(ROOT / "index.html").write_text(
    TEMPLATE.replace("__CARDS__", cards).replace("__COUNT__", str(len(classes)))
)
print(f"index.html built with {len(classes)} class(es)")
