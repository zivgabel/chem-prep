# -*- coding: utf-8 -*-
"""Collect every formula card (.fcard) from docs/guide.html into docs/formulas.html, grouped by part."""
import html, io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = io.open(os.path.join(ROOT, "docs", "guide.html"), encoding="utf-8").read()

def block(s, start, tag="div"):
    """Return the balanced <tag …>…</tag> starting at index start."""
    depth, i = 0, start
    pat = re.compile(rf"<{tag}\b|</{tag}>")
    for m in pat.finditer(s, start):
        depth += 1 if m.group(0) != f"</{tag}>" else -1
        if depth == 0:
            return s[start:m.end()]
    raise ValueError("unbalanced")

parts = []   # (part id, part title, [(sec id, sec title, [cards])])
for pm in re.finditer(r'<div data-part="(\w+)" id="\w+">', G):
    pid = pm.group(1)
    body = block(G, pm.start())
    t = re.search(r'<div class="part-head">.*?<h2>(.*?)</h2>', body, re.S)
    title = re.sub(r"<[^>]+>", "", t.group(1)) if t else pid
    secs = []
    for sm in re.finditer(r'<section class="topic" id="(\w+)">', body):
        sec = block(body, sm.start(), "section")
        h = re.search(r"<h3>(.*?)</h3>", sec, re.S)
        stitle = re.sub(r'<span class="n">(.*?)</span>', r"\1 · ", h.group(1)) if h else ""
        cards = [block(sec, cm.start()) for cm in re.finditer(r'<div class="fcard"', sec)]
        if cards:
            secs.append((sm.group(1), stitle, cards))
    if secs:
        parts.append((pid, title, secs))

n = sum(len(c) for _, _, ss in parts for _, _, c in ss)
toc = "".join(f'<a class="pill" href="#f-{pid}" data-part="{pid}" style="border-color:var(--accent);color:var(--accent)">{html.escape(t)}</a>' for pid, t, _ in parts)
out = [f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>דף נוסחאות – כימיה</title>
<meta name="description" content="כל הנוסחאות של הקורס במקום אחד, בתיבות ברורות עם הסבר לכל סימן">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;500;600;700;800&family=Frank+Ruhl+Libre:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="site.css">
<style>
.fwrap{{max-width:var(--wide);margin:0 auto;padding:0 16px 40px}}
.fgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,28rem),1fr));gap:0 18px}}
.fpart{{margin-top:2rem;padding-top:.6rem;border-top:3px solid var(--accent)}}
.fpart>h2{{font-family:var(--serif);margin:.2em 0 .4em}}
.fsec{{font-size:.85rem;font-weight:800;color:var(--accent);margin:0 0 -.9rem;text-decoration:none;display:block}}
.ftoc{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}
@media print{{.topbar,.ftoc,footer{{display:none}} body{{background:#fff}} .fsec{{margin-bottom:-.6rem}}}}
</style>
<script data-goatcounter="https://zivgabel.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</head>
<body>
<nav class="topbar" aria-label="ניווט"><div class="in">
  <b>כימיה · דף נוסחאות</b>
  <a class="pill go" href="guide.html">חומר מוסבר</a>
  <a class="pill" href="exams.html">מבחנים לדוגמא</a>
  <a class="pill" href="practice.html">תרגול לפי נושא</a>
  <a class="pill" href="index.html">דף הבית</a>
  <button class="pill btn" id="themeBtn" type="button">מצב תצוגה</button>
</div></nav>
<header class="hero">
  <div class="kicker">כימיה כללית ואנאורגנית · בלוק 1</div>
  <h1>דף נוסחאות</h1>
  <p class="lede">כל {n} הנוסחאות מהחומר המוסבר, מסודרות לפי פרקים. לוחצים על תיבה כדי להגדיל אותה, ועל שם הסעיף כדי לחזור להסבר המלא. אפשר גם להדפיס את הדף.</p>
  <div class="ftoc">{toc}</div>
</header>
<main class="fwrap">''']
for pid, title, secs in parts:
    out.append(f'<section class="fpart" id="f-{pid}" data-part="{pid}"><h2>{html.escape(title)}</h2><div class="fgrid">')
    for sid, stitle, cards in secs:
        for c in cards:
            out.append(f'<div><a class="fsec" href="guide.html#{sid}">{stitle} ←</a>{c}</div>')
    out.append("</div></section>")
out.append('''</main>
<footer>הנוסחאות נאספות אוטומטית מתוך החומר המוסבר.</footer>
<script src="site.js"></script>
</body>
</html>''')
io.open(os.path.join(ROOT, "docs", "formulas.html"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(n, "formula cards in", len(parts), "parts")
