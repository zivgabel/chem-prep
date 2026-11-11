# Spec for writing explanation-guide chapters (guide.html)

Audience: first-year biotechnology students (Tel-Hai, course "כימיה כללית ואנאורגנית"), Hebrew speakers, some
starting from zero. Goal: the block-1 final exam (lectures 1–11). The students explicitly asked for **visual
explanations, not only text**: diagrams, step-by-step illustrations, and **every important formula in its own
big formula card** (see below), never buried inside a sentence.

Look at `docs/guide.html` first — it is the style reference. Good examples to imitate:
- Chapter 0 (`id="i1"`…`id="i12"`): SVG figures, tables, callouts.
- Section `id="s3"`: figure + **formula card** (`class="fcard"`) + worked examples (`class="ex"`).
- Section `id="b4"`, `id="b6"`: worked examples with `ol.steps`.

## Output
An HTML **fragment** (no `<html>/<head>/<body>`) that will be pasted into `guide.html` as a new part:
```html
<div class="part-head" data-part="PART"> … </div>   <!-- copy the structure of an existing part-head -->
<div data-part="PART" id="PART"><div class="col">     <!-- copy the wrapper structure of an existing part -->
<section class="topic" id="x1"> <h3><span class="n">1</span>title</h3> … </section>
…
<section class="topic" id="xsol"> tutorial solutions in <details class="sol"> … </section>
<div class="recap"> bottom-line list </div>
<div class="cta"><a href="practice.html#PART">…</a></div>
</div></div>
```
Copy the exact wrapper / part-head / toc markup from the bonds part (`id="bonds"`) and adapt it.
Section ids: use the prefix you are given (e.g. `q1`, `q2`, … for quantum).

## Building blocks (CSS already exists — use only these)
- `<p>`, `<ul>`, `<ol>`, `<b>`, `<mark>`, `<sub>`, `<sup>`; tables: `<div class="tbl"><table>…</table></div>`
  (cells that are pure formula/number: `<td class="f">`).
- Callouts: `<div class="callout must"><span class="tag">חובה לזכור</span>…</div>`, also `trap` (מלכודת),
  `tip` (טיפ), `note` (הערה על המקור).
- Worked example: `<div class="ex"><header>title <small>הרצאה 2 שקף 7</small></header><div class="body">…</div></div>`,
  steps with `<ol class="steps"><li><div>…</div></li></ol>`.
- Reaction / single-line equation: `<div class="eq">…</div>` (LTR, centered).
- **Formula card** (use for EVERY formula a student must know):
```html
<div class="fcard"><span class="fname">אנרגיה של פוטון</span>
<div class="fx">E = h · ν = <span class="frac"><span>h · c</span><span>λ</span></span></div>
<dl class="fvars">
  <div><dt>E</dt><dd>אנרגיית הפוטון <span class="u">(J)</span></dd></div>
  <div><dt>h</dt><dd>קבוע פלנק, 6.626×10⁻³⁴ <span class="u">(J·s)</span></dd></div>
  …
</dl>
<p class="fnote">optional one-line note (when to use / common trap)</p>
</div>
```
  Inside `.fx`: `<span class="frac"><span>num</span><span>den</span></span>` for fractions, `<span class="sep"></span>`
  between several related formulas, `<span class="hl">…</span>` to highlight a term. Cards enlarge on click.
- Figures: `<figure><svg viewBox="0 0 W H" role="img" aria-label="…">…</svg><figcaption>…</figcaption></figure>`.
  SVG CSS classes available: `fs fa ft bx bx-ac ln ln-d ln-ac fi` (shapes), text classes `b sm ac tr`.
  Look at existing SVGs for usage. Rules learned the hard way:
  - The SVG is LTR. For **Hebrew** `<text>` add `direction="rtl"` and use `text-anchor="start"` to anchor at the
    right edge (x = right edge), or `middle`. Latin/math text needs no direction attribute.
  - Page CSS sets `svg text{font-size:15px}`, so set other sizes with **inline style** `style="font-size:22px"`,
    not the `font-size` attribute.
  - Use the CSS classes (they switch for dark mode); never hard-code colors.
  - Make figures genuinely explanatory (energy-level ladders, spectra, orbital boxes, trends arrows on a
    periodic-table sketch, 3D-ish shape sketches …), not decoration. Typical width 600–720.
- Every section must cite its source in small print where relevant: `<p class="src">הרצאה 2 שקפים 5–7</p>`.

## Hebrew + formulas (bidi) — very important, the page is RTL
- Wrap any inline formula/calculation inside a Hebrew sentence in `<span class="f">…</span>`
  (e.g. `<span class="f">E = hν</span>`). Pure-formula lines go in `.eq` or `.fcard`.
- Never write "Latin letter + colon + number" (`n: 2`) inside Hebrew; never start or end a Hebrew sentence
  with a bare formula; put numbers+units together inside a `.f` span (`<span class="f">250 nm</span>`).
- After you finish, the integrator runs `tools/isolate_ltr.py` which auto-wraps leftovers, but do it right
  yourself.

## Content rules
- Follow the **lecture slides** (read the PDFs in `sources/` visually with the Read tool, `pages` ≤ 20 per call;
  `sources/text_dump.txt` has some extracted text but Hebrew may be reversed). Use the lecturer's notation,
  constants and numbers. When the slides are thin, fill in with standard first-year general chemistry
  (OpenStax Chemistry 2e level) consistent with the slides, and say so in a `note` callout if it matters.
- Explain for understanding: start from the idea/intuition, then the formula card, then a worked example, then
  the typical traps. Prefer diagrams and tables over paragraphs. Short sentences.
- Include worked solutions to the matching tutorial sheet(s) in a final `…sol` section, one
  `<details class="sol"><summary>תרגול N – …</summary><div class="body">…</div></details>` per sheet.
  Check every calculation with Python (run it). Report anything in the sources that looks wrong — don't
  silently fix it.
- No names of students anywhere.

## Check-yourself questions
Also write `checks/<part>.json`: a JSON array of `{"sec": "<section id>", "q": "…", "a": "…"}`, 1–3 per
section (2 typical), open questions with a short answer first then why (use "\n" between lines; calc steps each
on its own line). Plain text with Unicode (no HTML). Same bidi rules (no "Latin:number", no sentence starting or
ending with a formula). Different numbers/examples than the section's worked examples.
