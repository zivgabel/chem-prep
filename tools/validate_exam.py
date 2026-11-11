# -*- coding: utf-8 -*-
"""Validate a practice-exam JSON file (see EXAM_SPEC.md)."""
import io, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
errs = []
def err(m): errs.append(m)
p = sys.argv[1]
d = json.load(io.open(p, encoding="utf-8"))
for k in ("id", "title", "mc", "open"):
    if k not in d: err(f"missing top-level '{k}'")
HTMLISH = re.compile(r"<(?!svg|/svg)[a-zA-Z/][^>]*>")
def plain(where, t):
    if not isinstance(t, str) or not t.strip(): err(f"{where}: empty or not a string"); return
    if HTMLISH.search(t): err(f"{where}: looks like HTML")
    for line in t.split("\n"):
        m = re.search(r"(?<![A-Za-z])[A-Za-z]{1,3} ?:[ ]?[0-9]", line)
        if m and re.search("[֐-׿]", line):
            err(f"{where}: 'Latin:number' pattern (bidi) -> {m.group(0)!r}")
mc = d.get("mc", [])
if len(mc) != 12: err(f"expected 12 multiple-choice questions, got {len(mc)}")
for i, q in enumerate(mc, 1):
    w = f"mc[{i}]"
    if q.get("n") != i: err(f"{w}: n should be {i}")
    for k in ("topic", "q", "sol"): plain(f"{w}.{k}", q.get(k))
    o = q.get("o", [])
    if len(o) != 5: err(f"{w}: needs 5 options")
    for j, x in enumerate(o): plain(f"{w}.o[{j}]", x)
    if len(set(o)) != len(o): err(f"{w}: duplicate options")
    if not isinstance(q.get("a"), int) or not 0 <= q["a"] <= 4: err(f"{w}: a must be 0..4")
    wn = q.get("why_not", [])
    if len(wn) != 5: err(f"{w}: why_not needs 5 entries")
    else:
        for j, x in enumerate(wn):
            if j == q.get("a") and x: err(f"{w}: why_not[{j}] should be empty (correct answer)")
            if j != q.get("a"): plain(f"{w}.why_not[{j}]", x)
    if "table" in q and not (isinstance(q["table"], list) and all(isinstance(r, list) for r in q["table"])):
        err(f"{w}: table must be list of rows")
op = d.get("open", [])
if len(op) != 3: err(f"expected 3 open questions, got {len(op)}")
for i, q in enumerate(op, 13):
    w = f"open[{i}]"
    if q.get("n") != i: err(f"{w}: n should be {i}")
    for k in ("topic", "q"): plain(f"{w}.{k}", q.get(k))
    ps = q.get("parts", [])
    if not 2 <= len(ps) <= 4: err(f"{w}: needs 2-4 parts")
    for j, pt in enumerate(ps):
        plain(f"{w}.parts[{j}].q", pt.get("q")); plain(f"{w}.parts[{j}].sol", pt.get("sol"))
        if "svg" in pt and not pt["svg"].lstrip().startswith("<svg"): err(f"{w}.parts[{j}].svg must start with <svg")
print(f"{p}: {len(mc)} MC, {len(op)} open")
if errs:
    print("\n".join("ERROR " + e for e in errs)); sys.exit(1)
print("OK")
