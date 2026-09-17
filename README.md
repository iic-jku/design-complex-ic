# Design of Complex Integrated Circuits

[![Quarto Publish](https://github.com/iic-jku/design-complex-ic/actions/workflows/quarto-publish.yml/badge.svg?branch=main)](https://github.com/iic-jku/design-complex-ic/actions/workflows/quarto-publish.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-online-brightgreen)](https://iic-jku.github.io/design-complex-ic/dcic.html)

**(c) 2017-2026 Harald Pretl, Institute for Integrated Circuits and Quantum Computing (IICQC), Johannes Kepler University, Linz (JKU)**

This is the material for a graduate-level course on the design of complex integrated circuits, held at JKU under course number 336.048 ("VL Entwurf komplexer integrierter Schaltungen").

The manuscript is written in [Quarto](https://quarto.org). All figures are generated from Python code (`matplotlib`, `schemdraw`) embedded in the Quarto sources, so the complete document can be built from source without any binary image assets.

## Lecture Slides

One reveal.js deck per chapter (and appendix) is generated from the lecture notes (`slides/<topic>.qmd`, listed on `slides/index.qmd`). Figures, display equations, callouts, lists and tables go on slides; prose becomes speaker notes (press `S`). Figure, equation, table, callout and section numbers match the notes.

The slide tooling in `slides/_tools/` is shared by all lectures ([AICD](https://github.com/iic-jku/analog-circuit-design), [RFIC](https://github.com/iic-jku/radio-frequency-integrated-circuits), [DCIC](https://github.com/iic-jku/design-complex-ic)) and is kept identical; lecture-specific settings (book file, name, chapters without a deck) live in `slides/_course.json`. When improving the tooling, copy `slides/_tools/` (without `numbers.json`) to the other lectures; [hpretl-lectures](https://github.com/iic-jku/hpretl-lectures) checks that the copies match.

After adding, removing or renaming a chapter, or adding/removing labels (`#fig-`, `#eq-`, `#tbl-`, `#nte-`, `#imp-`, `#sec-`), regenerate and check:

```bash
python3 slides/_tools/gen_decks.py
python3 -m unittest discover -s slides/_tools
```

Optional markup in the chapter files to improve slides (ignored by the HTML and PDF notes):

- `::: {.content-visible when-format="revealjs"}` — slide-only content (e.g. key bullet points); a leading `###` heading becomes the slide title and the preceding prose its speaker notes; without a heading, it fills a section slide that would otherwise be empty.
- `::: {.content-hidden when-format="revealjs"}` — keep content in the notes only; on slides its text becomes speaker notes (also inside callouts). Pair it with a slide-only block to condense long lists or callouts.
- `{.no-slide}` on a div (callout, figure cell), a figure (`![](x.png){#fig-foo .no-slide}`) or in an equation label (`{#eq-foo .no-slide}`) — skip it on slides.

"Solution: …" callouts are revealed step by step. Use project-absolute paths (`/content/...`) for `{{< include >}}` and `{{< embed >}}`, as they are resolved before the slide filter can adjust paths for `slides/`.

Long lists, callouts, paragraphs and tables continue on further slides (at most 80 words per slide; tables at most 12 rows or 120 words); prose sentences around a display equation go to the speaker notes. The render log lists `SLIDES: crowded slide …` warnings for slides that are still too full (e.g. a single very long sentence); these are good candidates for slide-only bullets.

## Building

```sh
pip install -r requirements.txt
quarto render
```

The rendered website is placed in `_site`.

## License

All course material is shared under the Apache-2.0 license (see `LICENSE`).

We happily accept pull requests to fix typos or add content!
