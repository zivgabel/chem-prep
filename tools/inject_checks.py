# -*- coding: utf-8 -*-
"""Insert "check yourself" boxes (checks/*.json) at the end of each guide section. Re-runnable."""
import io, json, glob, html, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from isolate_ltr import fix_text, HEB
ROOT = os.path.dirname(HERE)
GUIDE = os.path.join(ROOT, "docs", "guide.html")

def para(t):
    t = html.escape(t.replace("‎", "").strip(), quote=False)
    if not re.search(f"[{HEB}]", t):           # pure formula/number line -> isolate whole thing
        return f'<span class="li">{t}</span>'
    return fix_text(t)

def block(sec, items):
    out = [f'<!-- CHECK:{sec} -->', '<div class="check"><span class="tag">בדקו את עצמכן</span>']
    for i, it in enumerate(items, 1):
        a = "".join(f"<p>{para(l)}</p>" for l in it["a"].split("\n") if l.strip())
        out.append(f'<div class="cq"><p class="q"><span class="qn">{i}</span><span class="qt">{para(it["q"])}</span></p>'
                   f'<details class="reveal"><summary>הצגת התשובה</summary><div class="a">{a}</div></details></div>')
    out.append('</div>\n<!-- /CHECK -->\n')
    return "\n".join(out)

by_sec = {}
for f in sorted(glob.glob(os.path.join(ROOT, "checks", "*.json"))):
    for it in json.load(io.open(f, encoding="utf-8")):
        assert set(it) == {"sec", "q", "a"} and all(it.values()), it
        by_sec.setdefault(it["sec"], []).append(it)

s = io.open(GUIDE, encoding="utf-8").read()
s = re.sub(r"<!-- CHECK:\w+ -->.*?<!-- /CHECK -->\n", "", s, flags=re.S)   # remove old boxes
n = 0
for sec, items in by_sec.items():
    m = re.search(rf'<section class="topic" id="{sec}">', s)
    assert m, sec
    end = s.index("</section>", m.end())
    s = s[:end] + block(sec, items) + s[end:]
    n += len(items)
io.open(GUIDE, "w", encoding="utf-8", newline="\n").write(s)
print(f"{n} questions in {len(by_sec)} sections")
