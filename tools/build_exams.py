# -*- coding: utf-8 -*-
"""Render exams/*.json into docs/exam-<id>.html pages + docs/exams.html index (see EXAM_SPEC.md)."""
import glob, html, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from isolate_ltr import fix_text, HEB
ROOT = os.path.dirname(HERE)
EXDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "exams")
DOCS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "docs")
LET = "אבגדה"
ORDER = ["sample", "mock1", "mock2", "mock3", "mock4", "mock5"]

def para(t):
    t = html.escape(t.replace("‎", "").strip(), quote=False)
    if not re.search(f"[{HEB}]", t):
        return f'<span class="li">{t}</span>'
    return fix_text(t)

def paras(t, cls=""):
    c = f' class="{cls}"' if cls else ""
    return "".join(f"<p{c}>{para(l)}</p>" for l in t.split("\n") if l.strip())

def cell(c):
    if re.search(f"[{HEB}]", c): return f"<td>{para(c)}</td>"
    return f'<td class="f">{html.escape(c)}</td>'

def table(rows):
    if not rows: return ""
    h = "".join(f"<th>{para(c)}</th>" for c in rows[0])
    b = "".join("<tr>" + "".join(cell(c) for c in r) + "</tr>" for r in rows[1:])
    return f'<div class="tbl xt"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

def svg(s):
    return f'<figure class="xfig">{s}</figure>' if s else ""

NAV = '''<nav class="topbar" aria-label="ניווט"><div class="in">
  <b>כימיה · מבחן מסכם</b>
  <a class="pill go" href="exams.html">כל המבחנים</a>
  <a class="pill" href="guide.html">חומר מוסבר</a>
  <a class="pill" href="formulas.html">דף נוסחאות</a>
  <a class="pill" href="practice.html">תרגול לפי נושא</a>
  <a class="pill" href="index.html">דף הבית</a>
  <button class="pill btn" id="themeBtn" type="button">מצב תצוגה</button>
</div></nav>'''

HEAD = '''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;500;600;700;800&family=Frank+Ruhl+Libre:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="exam.css">
<script data-goatcounter="https://zivgabel.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</head>
<body data-part="exam">
'''

def render(d):
    eid = d["id"]
    out = [HEAD.format(title=html.escape(d["title"]) + " – כימיה", desc="מבחן לדוגמא עם פתרונות מנומקים – כימיה כללית ואנאורגנית"), NAV]
    nmc, nop = len(d["mc"]), len(d["open"])
    out.append(f'''<header class="hero xhero">
  <div class="kicker">כימיה כללית ואנאורגנית · מבחן סיום בלוק 1 · שיעורים 1–11</div>
  <h1>{html.escape(d["title"])}</h1>
  <p class="lede">{nmc} שאלות אמריקאיות (תשובה אחת נכונה) ו-{nop} שאלות פתוחות. פותרים כמו במבחן: מסמנים תשובה בכל שאלה אמריקאית, את הפתוחות כותבים על דף, ובסוף לוחצים <b>"סיום ובדיקה"</b>. ליד כל שאלה יש גם פתרון מנומק שאפשר לפתוח.</p>
  <div class="xbar">
    <button class="xbtn" type="button" data-act="print-exam">🖨 הדפסת המבחן</button>
    <button class="xbtn" type="button" data-act="print-key">🖨 הדפסת דף התשובות המנומק</button>
    <button class="xbtn ghost" type="button" data-act="reset">התחלה מחדש</button>
  </div>
</header>
<main class="xwrap" data-exam="{eid}">''')
    if d.get("constants"):
        out.append('<div class="xconst"><span class="tag">נתונים וקבועים</span><ul>' +
                   "".join(f"<li>{para(c)}</li>" for c in d["constants"]) + "</ul></div>")
    out.append('<h2 class="xsec">חלק א – שאלות אמריקאיות</h2>')
    for q in d["mc"]:
        opts = "".join(
            f'<li><button type="button" class="xo" data-i="{i}"><span class="L">{LET[i]}</span><span class="t">{para(o)}</span></button></li>'
            for i, o in enumerate(q["o"]))
        why = "".join(
            f'<li><b>{LET[i]}.</b> {para(w)}</li>' for i, w in enumerate(q.get("why_not", [])) if i != q["a"] and w)
        lec = f' · הרצאה {q["lecture"]}' if q.get("lecture") else ""
        out.append(f'''<article class="xq" id="q{q["n"]}" data-a="{q["a"]}">
<h3><span class="xn">{q["n"]}</span><small>{html.escape(q.get("topic",""))}{lec}</small></h3>
{paras(q["q"], "xstem")}{table(q.get("table"))}{svg(q.get("svg",""))}
<ol class="xopts">{opts}</ol>
<details class="xsol"><summary>פתרון מנומק</summary><div class="xbody">
<p class="xans">התשובה הנכונה: <b>{LET[q["a"]]}</b></p>
{paras(q["sol"])}{svg(q.get("sol_svg",""))}
{('<div class="xwhy"><b>למה לא האחרות:</b><ul>' + why + '</ul></div>') if why else ''}
</div></details>
</article>''')
    out.append('<h2 class="xsec">חלק ב – שאלות פתוחות</h2>')
    for q in d["open"]:
        lec = f' · הרצאה {q["lecture"]}' if q.get("lecture") else ""
        parts = "".join(f'''<div class="xpart">{paras(p["q"], "xpq")}
<details class="xsol"><summary>פתרון</summary><div class="xbody">{paras(p["sol"])}{svg(p.get("svg",""))}</div></details></div>'''
                        for p in q["parts"])
        out.append(f'''<article class="xq open" id="q{q["n"]}">
<h3><span class="xn">{q["n"]}</span><small>{html.escape(q.get("topic",""))}{lec}</small></h3>
{paras(q["q"], "xstem")}{table(q.get("table"))}{svg(q.get("svg",""))}
{parts}
</article>''')
    out.append(f'''<div class="xdone">
  <button class="xbtn big" type="button" data-act="check">סיום ובדיקה</button>
  <div class="xscore" aria-live="polite"></div>
</div>
</main>
<footer>מבחן תרגול שנכתב לפי המבחן לדוגמא של הקורס. הפתרונות נבדקו, אבל אם משהו נראה לא נכון – כדאי לבדוק מול המצגות.</footer>
<script src="site.js"></script>
<script src="exam.js"></script>
</body>
</html>''')
    return "\n".join(out)

exams = []
for f in glob.glob(os.path.join(EXDIR, "*.json")):
    d = json.load(io.open(f, encoding="utf-8"))
    exams.append(d)
exams.sort(key=lambda d: ORDER.index(d["id"]) if d["id"] in ORDER else 99)
for d in exams:
    io.open(os.path.join(DOCS, f'exam-{d["id"]}.html'), "w", encoding="utf-8", newline="\n").write(render(d))

cards = []
for d in exams:
    topics = sorted({q.get("topic", "") for q in d["mc"] + d["open"]} - {""})
    kind = "המבחן לדוגמא של הקורס, עם פתרון מלא" if d["id"] == "sample" else "מבחן תרגול באותו מבנה ובאותה רמה"
    cards.append(f'''<a class="day xcard" href="exam-{d["id"]}.html" data-exam="{d["id"]}">
  <div class="d">{kind}</div><h2>{html.escape(d["title"])}</h2>
  <p>{len(d["mc"])} אמריקאיות · {len(d["open"])} פתוחות · פתרונות מנומקים</p>
  <p class="xtopics">{" · ".join(html.escape(t) for t in topics)}</p>
  <p class="xlast"></p></a>''')
idx = HEAD.format(title="מבחנים לדוגמא – כימיה", desc="מבחנים לדוגמא למבחן הסיום של בלוק 1, עם דפי תשובות מנומקים") + NAV + f'''
<header class="hero xhero">
  <div class="kicker">כימיה כללית ואנאורגנית · מבחן סיום בלוק 1 · שיעורים 1–11</div>
  <h1>מבחנים לדוגמא</h1>
  <p class="lede">כל מבחן בנוי כמו המבחן לדוגמא של הקורס: 12 שאלות אמריקאיות עם 5 תשובות ו-3 שאלות פתוחות עם סעיפים. לכל שאלה יש פתרון מנומק, ולכל תשובה שגויה – הסבר למה היא לא נכונה. מומלץ להתחיל מהמבחן של הקורס, ואחר כך לעבור למבחני התרגול.</p>
</header>
<main class="xwrap"><div class="days xcards">
{"".join(cards)}
</div>
<div class="callout tip"><span class="tag">איך להתאמן</span><ul>
<li>פותרים בתנאי מבחן: עם שעון, בלי לפתוח פתרונות באמצע.</li>
<li>אחרי "סיום ובדיקה" – קוראים את הפתרון המנומק גם בשאלות שצדקתן בהן; לפעמים צודקים מהסיבה הלא נכונה.</li>
<li>כל טעות → חוזרים לפרק המתאים <a href="guide.html">בחומר המוסבר</a> ואז לתרגול לפי נושא.</li>
</ul></div>
</main>
<footer>נבנה מתוך המצגות, התרגולים והמבחן לדוגמא של הקורס.</footer>
<script src="site.js"></script>
<script>
document.querySelectorAll(".xcard").forEach(c=>{{try{{const r=JSON.parse(localStorage.getItem("chem_exam_"+c.dataset.exam)||"null");
 if(r&&r.score!=null) c.querySelector(".xlast").textContent="ניסיון אחרון: "+r.score+" מתוך "+r.total+" באמריקאיות";}}catch(e){{}}}});
</script>
</body>
</html>'''
io.open(os.path.join(DOCS, "exams.html"), "w", encoding="utf-8", newline="\n").write(idx)
print(len(exams), "exams:", ", ".join(d["id"] for d in exams))
