# -*- coding: utf-8 -*-
"""Wrap non-Hebrew math/symbol runs inside Hebrew text nodes with <span class="li"> (LTR isolate)."""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
HEB = r"\u0590-\u05FF"
OP = re.compile(r"(=|→|×|÷|\+|−|≈|≤|≥|/|&lt;|&gt;|≠)")
SKIP = re.compile(r"(<head.*?</head>|<svg.*?</svg>|<script.*?</script>|<style.*?</style>|<span class=\"li\">.*?</span>)", re.S)
count = 0
def trim(run):
    lead = trail = ""
    while run and run[0] in " ,.·–-:;":
        lead += run[0]; run = run[1:]
    while run and run[-1] in " ,.·–-:":
        trail = run[-1] + trail; run = run[:-1]
    # unbalanced parens at the edges stay outside
    while run.startswith("(") and run.count("(") > run.count(")"):
        lead += "("; run = run[1:]
    while run.endswith(")") and run.count(")") > run.count("("):
        trail = ")" + trail; run = run[:-1]
    return lead, run, trail
def fix_text(t):
    global count
    if not re.search(f"[{HEB}]", t): return t
    out = []
    for part in re.split(f"([^{HEB}\n]+)", t):
        if part and not re.search(f"[{HEB}]", part) and OP.search(part) and re.search(r"[0-9A-Za-zΔΣσπμ]", part):
            lead, core, trail = trim(part)
            if core and OP.search(core) and re.search(r"[0-9A-Za-zΔΣσπμ]", core) and re.match(r"[0-9A-Za-zΔΣσπμ(\[&]", core) and re.search(r"[0-9A-Za-zΔΣσπμ⁰-⁹₀-₉⁺⁻)\]%;]$", core) and not core.startswith("&"):
                out.append(lead + '<span class="li">' + core + '</span>' + trail); count += 1; continue
        out.append(part)
    return "".join(out)
def fix_html(chunk):
    # operate on text between tags; keep inline tags (sub/sup/b) inside a run by merging first
    return re.sub(r">([^<]+)<", lambda m: ">" + fix_text(m.group(1)) + "<", chunk)
pieces = SKIP.split(s)
res = [x if SKIP.fullmatch(x or "") else fix_html(x) for x in pieces]
io.open(p, "w", encoding="utf-8", newline="\n").write("".join(res))
print("wrapped", count)
