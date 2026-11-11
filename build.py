# -*- coding: utf-8 -*-
"""Merge questions/*.json into site/questions.json (options shuffled deterministically)."""
import json, glob, io, os, random, hashlib, sys, html, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from isolate_ltr import fix_text, HEB
def h(t):
    """escape + wrap LTR math runs so they render correctly inside the RTL page (practice.html inserts as HTML)"""
    t = html.escape(t.replace("‎", "").strip(), quote=False)
    return f'<span class="li">{t}</span>' if not re.search(f"[{HEB}]", t) else fix_text(t)
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
out, seen = [], set()
for path in sorted(glob.glob(os.path.join(HERE, "questions", "*.json"))):
    for q in json.load(io.open(path, encoding="utf-8")):
        assert q["id"] not in seen, q["id"]; seen.add(q["id"])
        opts = list(enumerate(q["options"]))
        random.Random(int(hashlib.md5(q["id"].encode()).hexdigest(), 16)).shuffle(opts)
        out.append({"id": q["id"], "c": q["quiz"], "t": q["topic"], "d": q["difficulty"],
                    "f": q["source"]["file"], "p": q["source"].get("page", 0),
                    "q": h(q["question"]), "o": [h(o[1]) for o in opts],
                    "a": [i for i, o in enumerate(opts) if o[0] == q["answer"]][0], "e": h(q["explanation"])})
json.dump(out, io.open(os.path.join(HERE, "docs", "questions.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
pos = [0]*4
for q in out: pos[q["a"]] += 1
print(len(out), "questions; answer positions", pos)
