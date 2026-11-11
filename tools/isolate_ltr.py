# -*- coding: utf-8 -*-
"""Wrap non-Hebrew math/symbol runs inside Hebrew text nodes with <span class="li"> (LTR isolate)."""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HEB = r"\u0590-\u05FF"
OP = re.compile(r"(=|→|×|÷|\+|−|≈|≤|≥|/|&lt;|&gt;|≠)")
SKIP = re.compile(r"(<head.*?</head>|<svg.*?</svg>|<script.*?</script>|<style.*?</style>|<span class=\"li\">.*?</span>|<(td|span|div|p)\b[^>]*class=\"(?:[^\"]* )?(?:f|ltr|eq)(?: [^\"]*)?\"[^>]*>.*?</\2>)", re.S)
# small LTR tokens that break in RTL even without an operator: ions (Na⁺, SO₄²⁻, 2e⁻), δ+/δ−, signed numbers (−183 kJ)
TOKEN = re.compile(r"(?:\[(?:He|Ne|Ar|Kr|Xe|Rn)\](?: ?[1-7][spdf][⁰-⁹¹²³]+)+|(?<![0-9A-Za-z])(?:[1-7][spdf][⁰-⁹¹²³]+){2,})|(?<![\w⁰-⁹¹²³₀-₉=≡–])(?:(?:[0-9]+|[⁰-⁹¹²³]+)?[A-Za-z\[][A-Za-z0-9₀-₉⁰-⁹¹²³()\[\]]*[⁺⁻](?![A-Za-z0-9₀-₉⁰-⁹¹²³])"
                   r"|δ[+−⁺⁻]"
                   r"|(?<![0-9A-Za-z.,])[−+]?[0-9]+(?:[.,][0-9]+)? ?°C?(?![A-Za-z])"
                   r"|(?<![0-9A-Za-z.,])[0-9]+(?:[.,][0-9]+)?[–-][0-9]+(?:[.,][0-9]+)?(?![0-9A-Za-z])"
                   r"|(?<![0-9A-Za-z.,×⁰-⁹¹²³])[0-9]+(?:[.,][0-9]+)*(?:×10[⁰-⁹¹²³⁻]+)? (?:kJ/mol|kJ|g/mol|mol/L|mol|amu|kg|mg|mL|mm|g|L|D|M|Å|pm|nm|cm|m|K|°C)(?![A-Za-z0-9/])"
                   r"|(?<![0-9A-Za-z)\]] )(?<![0-9A-Za-z])[−+][0-9]+(?:[.,][0-9]+)*(?: ?(?:kJ/mol|kJ|g/mol|mol|amu|g|D|M|Å|pm|nm))?(?![\w]))")
def tok(t):
    global count
    def w(m):
        global count; count += 1; return '<span class="li">' + m.group(0) + '</span>'
    return TOKEN.sub(w, t)
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
    if not re.search(f"[{HEB}]", t): return tok(t)
    out = []
    for part in re.split(f"([^{HEB}\n]+)", t):
        if part and not re.search(f"[{HEB}]", part) and OP.search(part) and re.search(r"[0-9A-Za-zΔΣσπμ]", part):
            lead, core, trail = trim(part)
            if core and OP.search(core) and re.search(r"[0-9A-Za-zΔΣσπμ]", core) and re.match(r"[0-9A-Za-zΔΣσπμ(\[&]", core) and re.search(r"[0-9A-Za-zΔΣσπμÅ⁰-⁹¹²³₀-₉⁺⁻)\]%;]$", core) and not core.startswith("&"):
                out.append(lead + '<span class="li">' + core + '</span>' + trail); count += 1; continue
        out.append(part if re.search(f"[{HEB}]", part) else tok(part))
    return "".join(out)
def fix_html(chunk):
    # operate on text between tags; keep inline tags (sub/sup/b) inside a run by merging first
    return "".join(x if x.startswith("<") else fix_text(x) for x in re.split(r"(<[^>]*>)", chunk))
if __name__ == "__main__":
    p = sys.argv[1]
    s = io.open(p, encoding="utf-8").read()
    res, pos = [], 0
    for m in SKIP.finditer(s):
        res += [fix_html(s[pos:m.start()]), m.group(0)]; pos = m.end()
    res.append(fix_html(s[pos:]))
    io.open(p, "w", encoding="utf-8", newline="\n").write("".join(res))
    print("wrapped", count)
