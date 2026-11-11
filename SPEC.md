# Chemistry quiz-prep question bank — spec for question writers

Audience: first-year biotechnology students (Tel-Hai, course "כימיה כללית ואנאורגנית").
Two big quizzes this week:
- **Tuesday — chemical bonds (קשרים כימיים)** → `quiz: "bonds"`
- **Wednesday — stoichiometry (סטויכיומטריה)** → `quiz: "stoich"`

Language: **Hebrew**, the way the course writes it (terms like ΔEN, VSEPR, sp², mol, g/mol stay in Latin script).
Write chemical formulas with Unicode sub/superscripts: H₂O, CO₂, NO₂⁻, NH₄⁺, SO₃²⁻, sp³, 6.022×10²³.
Plain text only — no HTML, no Markdown, no LaTeX.

## Sources (all in `sources/`)
- Lectures as PDF (one slide per page): `Lecture5.pdf` (bond energetics, ionic/covalent, EN, Lewis),
  `Lecture6.pdf` (formal charge, octet exceptions, bond enthalpy, resonance),
  `Lecture10.pdf` (isotopes, amu, Avogadro, mole, molar mass, empirical/molecular formula, mass %),
  `Lecture11.pdf` (empirical/molecular formula, balancing, stoichiometric ratios, limiting reagent,
  combustion analysis, solutions & molarity). `Lecture4.pdf` = periodic trends (background only).
- Tutorials (question sheets, no answers except where shown): `Tutorial5.pdf` … `Tutorial11.pdf`.
  Tutorial 7–9 cover VSEPR/dipole/% ionic character, hybridization & σ/π, intermolecular forces —
  the lecture slides for those topics (lectures 7–9) are NOT available, so for those topics you may use
  standard first-year general-chemistry knowledge (consistent with the tutorial wording), and set
  `"source": {"file": "TutorialN", "page": p}` pointing to the tutorial that practises that topic.
- `sources/text_dump.txt` has extracted text, but Hebrew may be reversed and equations are missing.
  **Read the PDFs visually with the Read tool (`pages` param, ≤20 pages per call)** to see figures,
  equations and tables.

## Course-specific facts you must respect
- ΔEN thresholds used in this course (Lecture5 p.13): < 0.4 mostly (non-polar) covalent; 0.4–1.7 polar
  covalent; > 1.7 mostly ionic. ΔEN = 0 → pure covalent. Use the Pauling values on Lecture5 p.11–12
  (H 2.1, C 2.5, N 3.0, O 3.5, F 4.0, Cl 3.0, Br 2.8, I 2.5, S 2.5, P 2.1, Na 0.9, Li 1.0, K 0.8, Mg 1.2,
  Ca 1.0, Al 1.5, Si 1.8, B 2.0, Be 1.5 …). When a question needs EN values, give them in the stem.
- Formal charge FC = valence e⁻ − non-bonding e⁻ − ½·bonding e⁻ (Lecture6 p.3).
- ΔH_rxn ≈ Σ BE(reactants) − Σ BE(products) (Lecture6 p.13). Bond-energy table on Lecture6 p.12
  (H–H 436, C–H 414, O–H 464, O=O 498, C=O 736 (in CO₂ the course table footnotes it; use 799 only if you
  state it), C–C 347, C=C 611, C≡C 837, N≡N 946, H–Cl 431, Cl–Cl 243, H–F 565, F–F 159, C–O 360, C–Cl 339,
  N–H 389, H–N 389 …). Give needed bond energies in the stem.
- Atomic masses the course uses: H 1.008 (or 1), C 12.01 (or 12), O 16.00, N 14.01, Na 22.99, Cl 35.45,
  Al 26.98, S 32.07, P 30.97, Ca 40.08, Mg 24.31, Cu 63.55, Fe 55.85. State the masses you use in the stem
  for calculation questions (e.g. "(H=1, C=12, O=16)").
- N_A = 6.022×10²³. 1 amu = 1/12 of a ¹²C atom = 1.66×10⁻²⁴ g.
- Limiting reagent method (Lecture11 p.19–21): moles ÷ coefficient, smallest value = limiting.
- Molarity M = n(solute) / V(solution, L) — volume of the **solution**, not the solvent.

## Question quality
- Multiple choice, exactly 4 options, exactly one correct answer.
- Distractors must be the mistakes a real student makes: forgot to balance, used the coefficient
  wrong, divided instead of multiplied, forgot ×2 for H in H₂O, used solvent volume, counted lone pairs as
  bonds, mixed up VSEPR electron geometry vs molecular shape, etc. Never absurd.
- **Every calculation must be checked with Python** (run it) before you write the answer; round
  sensibly and make the distractors numerically distinct (not within rounding of the right answer).
- Mix: ~30% easy (definition/recall), ~45% medium (apply one idea / one-step calc), ~25% hard
  (multi-step calc, compare structures, choose best Lewis structure, combustion analysis…).
- Many questions should mirror the tutorial question styles (that is what the quiz will look like),
  but with **different numbers/molecules** — don't copy a tutorial question verbatim.
- Cover every topic in your list evenly. No near-duplicates.
- Avoid "all/none of the above". Negative stems ("איזה מהבאים אינו…") max 1 in 8, with the word
  **לא/אינו** clearly in the stem.
- Don't reveal the answer in the stem; options of similar length and form.
- `explanation`: 1–4 sentences in Hebrew: why the answer is right, show the short calculation for calc
  questions, and name the typical mistake behind the most tempting distractor.

## Output format
One UTF-8 JSON array file at the path you're given. Each item:
```json
{
  "id": "<prefix>-001",
  "quiz": "bonds" | "stoich",
  "topic": "<Hebrew topic, from your topic list exactly>",
  "source": { "file": "Lecture6", "page": 12 },
  "difficulty": "easy" | "medium" | "hard",
  "question": "…",
  "options": ["…","…","…","…"],
  "answer": 0,
  "explanation": "…"
}
```
`answer` is 0-based; options get shuffled later, so don't worry about position balance.
Validate: `python "validate.py" <your file>` and fix every error.

## Final reply
Short: file path, total count, count per topic, anything in the sources that looked wrong or
contradictory (don't silently fix — report it).
