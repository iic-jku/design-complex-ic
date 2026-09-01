# Design of Complex Integrated Circuits

**(c) 2017-2026 Harald Pretl, Institute for Integrated Circuits and Quantum Computing (IICQC), Johannes Kepler University, Linz (JKU)**

This is the material for a graduate-level course on the design of complex integrated circuits, held at JKU under course number 336.048 ("VL Entwurf komplexer integrierter Schaltungen").

The manuscript is written in [Quarto](https://quarto.org). All figures are generated from Python code (`matplotlib`, `schemdraw`) embedded in the Quarto sources, so the complete document can be built from source without any binary image assets.

## Building

```sh
pip install -r requirements.txt
quarto render
```

The rendered website is placed in `_site`.

## License

All course material is shared under the Apache-2.0 license (see `LICENSE`).

We happily accept pull requests to fix typos or add content!
