# Spec for practice exams (מבחנים לדוגמא) — block-1 final exam

Course: "כימיה כללית ואנאורגנית" (Tel-Hai, biotechnology year 1). Block-1 final exam covers lectures 1–11:
- L1 matter, atom, EM radiation, black-body & atomic emission spectra, Planck quanta
- L2 photoelectric effect, Bohr model (energy levels, transitions, H-like ions), photons, de Broglie
- L3 orbitals, quantum numbers, Aufbau / Pauli / Hund, electron configurations (incl. exceptions Cr, Cu)
- L4 periodic table, periodic trends (radius, ionization energy, electron affinity, EN), isoelectronic series
- L5 bond energetics, ionic/covalent, EN & ΔEN, Lewis structures
- L6 formal charge, octet exceptions, bond enthalpy & ΔH estimate, resonance
- L7 VSEPR shapes, EN & dipole moment
- L8 dipole moment / % ionic character, hybridization sp³/sp²/sp, σ and π bonds
- L9 intermolecular forces (London, dipole–dipole, H-bonds), boiling points
- L10 isotopes, average atomic mass, mole, molar mass, mass %, empirical/molecular formula
- L11 balancing, stoichiometric ratios, limiting reagent, yield, combustion analysis, molarity
Sources: `sources/Lecture1..11.pdf`, `sources/Tutorial*.pdf`, the official sample exam `sources/PracticeExam.pdf`
(read it first: it defines the **format and level**). Read PDFs visually with the Read tool (`pages` ≤ 20).
Course conventions for bonds/stoich: see `SPEC.md`. Use the lecturer's constants/notation (check the slides for
h, c, Bohr energy constant 2.18×10⁻¹⁸ J or R, etc.).

## Format (exactly like the sample exam)
- Questions 1–12: multiple choice with **5 options** (א–ה), one correct. Level: like the sample — mostly
  apply/compare/calculate, few pure recall. Distractors are real mistakes (wrong sign, forgot Z², wrong
  direction of transition, counted lone pairs as bonds, forgot to balance …).
- Questions 13–15: open questions with 2–3 sub-parts (א, ב, ג): one Lewis/resonance/structure question, one
  quantum/Bohr/photon calculation, one stoichiometry (balance + limiting reagent + mass) — vary the mix
  between exams but keep the balance of topics similar to the sample.
- Topic balance per exam (≈): 4–5 questions on L1–4, 6–7 on L5–9, 3–4 on L10–11. Different molecules,
  numbers and contexts than the sample exam, the tutorials and the other mock exams.

## Output: one UTF-8 JSON file per exam
```json
{
  "id": "mock1",
  "title": "מבחן לדוגמא 1",
  "constants": ["h = 6.626×10⁻³⁴ J·s", "c = 3.00×10⁸ m/s", "…"],
  "mc": [
    {
      "n": 1,
      "topic": "נוסחה אמפירית",
      "lecture": 10,
      "q": "question text",
      "table": [["קשר", "אנרגיית קשר (kJ/mol)"], ["N–N", "163"]],
      "o": ["א text", "ב text", "ג text", "ד text", "ה text"],
      "a": 2,
      "sol": "full reasoned solution: the idea, the calculation step by step (\n between lines)",
      "why_not": ["why א is wrong", "why ב is wrong", "", "why ד is wrong", "why ה is wrong"]
    }
  ],
  "open": [
    {
      "n": 13,
      "topic": "רזוננס ומטען פורמלי",
      "lecture": 6,
      "q": "stem",
      "parts": [
        {"q": "א. …", "sol": "full worked answer", "svg": "<svg …>…</svg>"}
      ]
    }
  ]
}
```
- `table` optional (first row = header). `svg` optional per part — use it for Lewis structures / resonance /
  energy-level diagrams in solutions (viewBox, `text` elements, classes `ln bx fi b sm ac tr` as in
  `docs/guide.html`; Hebrew text needs `direction="rtl"`; set font sizes with inline `style`). `why_not` has an
  empty string at the index of the correct answer.
- Everything else is **plain text** (no HTML/Markdown/LaTeX), Unicode formulas (H₂O, Fe₂O₃, 10⁻¹⁹, Δ, λ, ν),
  "\n" for line breaks. Bidi: in Hebrew sentences avoid "Latin:number", don't start/end a sentence with a bare
  formula, keep each calculation as one compact chunk on its own line (`E = hc/λ = … = 7.95×10⁻¹⁹ J`).
- `sol` = the "reasoned answer sheet": explain the principle in 1–2 sentences, then the calculation, then the
  final answer. For open parts, write the full answer a student would be expected to write in the exam,
  plus a short "נקודות שבודקים" / common-mistake line when useful.
- **Check every calculation with Python (run it)** and make sure exactly one option is correct and the
  distractors are numerically distinct.
- Validate: `python tools/validate_exam.py <file>`.

## Final reply
File path(s), topic per question, and anything in the sources that looked wrong or ambiguous.
