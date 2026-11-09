# כימיה – הכנה לבחנים

חומר מוסבר ושאלות תרגול לקורס "כימיה כללית ואנאורגנית" (ביוטכנולוגיה, שנה א').

- `docs/` – האתר (GitHub Pages): `index.html`, `guide.html`, `practice.html`, `questions.json`
- `questions/*.json` – מאגרי השאלות; `python build.py` בונה את `docs/questions.json`
- `validate.py` – בדיקת מבנה המאגר; `SPEC.md` – הנחיות לכתיבת שאלות
- `checks/*.json` – שאלות "בדקו את עצמכן" בסוף כל פרק בחומר המוסבר (sec/q/a); `python tools/inject_checks.py` מכניס אותן ל-`guide.html`
- `tools/isolate_ltr.py` – עוטף נוסחאות, יונים ומספרים עם יחידות בתוך טקסט עברי כדי שיוצגו בסדר הנכון (אחרי כל עריכה של `guide.html`: `python tools/isolate_ltr.py docs/guide.html`)
