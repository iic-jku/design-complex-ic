# Design of Complex Integrated Circuits

[![Quarto Publish](https://github.com/iic-jku/design-complex-ic/actions/workflows/quarto-publish.yml/badge.svg?branch=main)](https://github.com/iic-jku/design-complex-ic/actions/workflows/quarto-publish.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-online-brightgreen)](https://iic-jku.github.io/design-complex-ic/dcic.html)

**(c) 2017-2026 Harald Pretl, Institute for Integrated Circuits and Quantum Computing (IICQC), Johannes Kepler University, Linz (JKU)**

This is the material for a graduate-level course on the design of complex integrated circuits, held at JKU under course number 336.048 ("VL Entwurf komplexer integrierter Schaltungen").

The manuscript is written in [Quarto](https://quarto.org). All figures are generated from Python code (`matplotlib`, `schemdraw`) embedded in the Quarto sources, so the complete document can be built from source without any binary image assets.

## Lecture Slides

One reveal.js deck per chapter is generated from the lecture notes (`slides/<topic>.qmd`, listed on `slides/index.qmd`; tooling in `slides/_tools/`). Figures, display equations, callouts, lists and tables go on slides; prose becomes speaker notes (press `S`). Figure, equation, table and section numbers match the notes.

After adding, removing or renaming a chapter, or adding/removing labels (`#fig-`, `#eq-`, `#tbl-`, `#nte-`, `#sec-`), regenerate and check:

```bash
python3 slides/_tools/gen_decks.py
python3 -m unittest slides/_tools/test_gen_decks.py
```

Optional markup in the chapter files to improve slides (ignored by the HTML and PDF notes):

- `::: {.content-visible when-format="revealjs"}` — slide-only content (e.g. key bullet points); a leading `###` heading becomes the slide title; without a heading, it fills a section slide that would otherwise be empty.
- `::: {.content-hidden when-format="revealjs"}` — keep content in the notes only.
- `{.no-slide}` on a div (callout, figure cell) or in an equation label (`{#eq-foo .no-slide}`) — skip it on slides.

The render log lists `SLIDES: crowded slide …` warnings for slides that are good candidates for slide-only bullets.

## Building

```sh
pip install -r requirements.txt
quarto render
```

The rendered website is placed in `_site`.

## License

All course material is shared under the Apache-2.0 license (see `LICENSE`).

We happily accept pull requests to fix typos or add content!
