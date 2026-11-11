# -*- coding: utf-8 -*-
"""Validate a question-bank JSON file. Usage: python validate.py file.json"""
import json, sys, io, re, os
sys.stdout.reconfigure(encoding="utf-8")
SRC = {f[:-4] for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources")) if f.endswith(".pdf")}
SRC |= {"general"}
errs = []
data = json.load(io.open(sys.argv[1], encoding="utf-8"))
if not isinstance(data, list): sys.exit("top level must be a JSON array")
ids = set(); stems = set()
for i, q in enumerate(data):
    where = q.get("id", f"#{i}")
    for k in ["id","quiz","topic","source","difficulty","question","options","answer","explanation"]:
        if k not in q: errs.append(f"{where}: missing {k}")
    if errs and errs[-1].startswith(where): continue
    if q["id"] in ids: errs.append(f"{where}: duplicate id")
    ids.add(q["id"])
    if q["quiz"] not in ("bonds","stoich","atom","periodic"): errs.append(f"{where}: quiz must be bonds|stoich|atom|periodic")
    if q["difficulty"] not in ("easy","medium","hard"): errs.append(f"{where}: bad difficulty")
    s = q["source"]
    if not isinstance(s, dict) or s.get("file") not in SRC: errs.append(f"{where}: source.file must be one of {sorted(SRC)}")
    if s.get("file") != "general" and not isinstance(s.get("page"), int): errs.append(f"{where}: source.page must be int")
    o = q["options"]
    if not (isinstance(o, list) and len(o) == 4 and all(isinstance(x,str) and x.strip() for x in o)): errs.append(f"{where}: need 4 non-empty options")
    elif len(set(x.strip() for x in o)) != 4: errs.append(f"{where}: duplicate options")
    if not (isinstance(q["answer"], int) and 0 <= q["answer"] <= 3): errs.append(f"{where}: answer must be 0-3")
    if len(q["question"].strip()) < 10: errs.append(f"{where}: question too short")
    if len(q["explanation"].strip()) < 15: errs.append(f"{where}: explanation too short")
    st = re.sub(r"\s+"," ",q["question"].strip())
    if st in stems: errs.append(f"{where}: duplicate stem")
    stems.add(st)
    if re.search(r"<[a-z/]", q["question"]+"".join(o)+q["explanation"]): errs.append(f"{where}: no HTML allowed")
print(f"{len(data)} questions checked")
if errs:
    print("\n".join(errs)); sys.exit(1)
from collections import Counter
print("topics:", dict(Counter(q["topic"] for q in data)))
print("difficulty:", dict(Counter(q["difficulty"] for q in data)))
print("OK")
