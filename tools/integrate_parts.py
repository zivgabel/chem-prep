# -*- coding: utf-8 -*-
"""Insert parts/atom.html + parts/periodic.html into guide.html (between intro and bonds), replace b8–b11 with
parts/bonds_update.html, swap tutorial 7–9 solutions if parts/bonds_bsol_t7_9.html exists, refresh header/nav.
Idempotent: parts are wrapped in <!-- PART:x --> … <!-- /PART:x --> markers."""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "docs", "guide.html")
s = io.open(G, encoding="utf-8").read()

def block(s, start, tag):
    depth = 0
    for m in re.finditer(rf"<{tag}\b|</{tag}>", s[start:]):
        depth += 1 if m.group(0) != f"</{tag}>" else -1
        if depth == 0:
            return start, start + m.end()
    raise ValueError("unbalanced " + tag)

def rd(name):
    p = os.path.join(ROOT, "parts", name)
    return io.open(p, encoding="utf-8").read().strip() if os.path.exists(p) else None

# 1) new parts before the bonds part
anchor = "<!-- ============================ PART A: BONDS"
for pid, title in (("atom", "ATOM"), ("periodic", "PERIODIC")):
    frag = rd(pid + ".html")
    if not frag: print("skip", pid); continue
    wrapped = f"<!-- PART:{pid} -->\n<!-- ============================ PART: {title} ============================ -->\n{frag}\n<!-- /PART:{pid} -->\n\n"
    if f"<!-- PART:{pid} -->" in s:
        s = re.sub(rf"<!-- PART:{pid} -->.*?<!-- /PART:{pid} -->\n\n", lambda m: wrapped, s, flags=re.S)
    else:
        i = s.index(anchor); s = s[:i] + wrapped + s[i:]
    print("part", pid, "ok")

# 2) replace b8..b11 (+ any b12.. previously inserted) with the update
upd = rd("bonds_update.html")
if upd:
    ids = re.findall(r'<section class="topic" id="(b\d+)">', upd)
    old = [i for i in re.findall(r'<section class="topic" id="(b\d+)">', s) if int(i[1:]) >= 8]
    first = s.index(f'<section class="topic" id="{old[0]}">')
    last_start = s.index(f'<section class="topic" id="{old[-1]}">')
    _, last_end = block(s, last_start, "section")
    # keep CHECK blocks out (they are re-injected by inject_checks.py)
    s = s[:first] + upd + s[last_end:]
    print("bonds sections replaced:", old, "->", ids)

# 3) tutorial 7–9 solutions
t79 = rd("bonds_bsol_t7_9.html")
if t79:
    news = [s2 for s2 in re.findall(r"<details class=\"sol\">.*?</details>", t79, re.S)]
    bsol_start = s.index('<section class="topic" id="bsol">')
    bs, be = block(s, bsol_start, "section")
    sec = s[bs:be]
    for nd in news:
        n = re.search(r"תרגול\s*(\d+)", nd).group(1)
        m = re.search(rf'<details class="sol"><summary>[^<]*תרגול\s*{n}\b.*?</details>', sec, re.S)
        if m: sec = sec[:m.start()] + nd + sec[m.end():]; print("bsol tutorial", n, "replaced")
        else: print("bsol tutorial", n, "NOT FOUND")
    s = s[:bs] + sec + s[be:]

io.open(G, "w", encoding="utf-8", newline="\n").write(s)
print("sections:", len(re.findall(r'<section class="topic"', s)))
