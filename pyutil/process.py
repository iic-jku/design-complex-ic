"""Drawing helpers for the CMOS process-flow cross-section figures.

The drawn geometry shows an NMOS (in the p-well) and a PMOS (in the n-well)
on a p-type substrate, each with its well tap on the outside — the p-well tap
left of the NMOS, the n-well tap right of the PMOS — evolving through the
front-end and back-end processing steps.

Copyright (C) 2017-2026 Harald Pretl and co-authors (harald.pretl@jku.at)
Licensed under the Apache License, Version 2.0.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

C = {
    'sub': '#f5e9d0',     # p-substrate
    'pwell': '#f5c98a',   # p-well
    'nwell': '#aacdea',   # n-well
    'ox': '#c7dff2',      # SiO2 (STI fill, gate oxide, ILD is lighter)
    'poly': '#3e9c5c',    # poly-silicon
    'nplus': '#4a7fb5',   # n+ implant
    'pplus': '#d1862c',   # p+ implant
    'resist': '#dd82b4',  # photo resist
    'mask': '#8ab6d6',    # hard mask (SiO2)
    'metal': '#8f8f8f',   # metal (Al)
    'sil': '#8e44ad',     # silicide (TiSi2)
    'ild': '#ebebeb',     # inter-layer dielectric
    'nit': '#c9c9a3',     # spacer nitride
}

SURF = 4.0
XMAX = 15.6
WELL_X = 7.8                # p-well / n-well boundary

# Isolation, from the left edge: wafer edge, p-well tap from NMOS, NMOS from
# PMOS (the well boundary), PMOS from n-well tap, wafer edge.
STI_X = [(0.0, 0.6), (1.8, 2.6), (7.1, 8.5), (13.0, 13.8), (15.0, 15.6)]
STI_D = 0.8   # trench depth
FOX_H = 0.3   # field oxide grown above the silicon surface

# NMOS geometry, with the p-well tap on its left
PTAP = (0.8, 1.6)           # p+ tap contacting the p-well
NG = (4.35, 5.25)           # gate
NSD = [(3.0, 4.25), (5.35, 6.6)]
# PMOS geometry, with the n-well tap on its right
PG = (10.35, 11.25)
PSD = [(9.0, 10.25), (11.35, 12.6)]
NTAP = (14.0, 14.8)         # n+ tap contacting the n-well

SD_D = 0.5       # junction depth
SPACER_W = 0.28  # spacer footprint on the silicon surface
SIL_T = 0.18     # silicide thickness

# Implant masks open over the transistor and the tap that share an implant:
# phosphorus dopes the NMOS source/drain and the n-well tap, boron the PMOS
# source/drain and the p-well tap. Boundaries lie on isolation.
NPLUS_OPEN = [(2.2, WELL_X), (13.4, XMAX)]
PPLUS_OPEN = [(0.0, 2.2), (WELL_X, 13.4)]


def setup(ax, title=None, ymax=7.2):
    ax.set_xlim(-0.2, XMAX + 0.2)
    ax.set_ylim(-0.3, ymax)
    ax.set_aspect('equal')
    ax.axis('off')
    if title is not None:
        ax.set_title(title, fontsize=9, loc='left')


def _top_profile(x0, x1, ytop, notches, depth):
    """Trace the top edge from x0 to x1, dipping `depth` into every notch
    that falls inside the span, so the body outline follows the trenches."""
    pts = []
    x = x0
    for a, b in sorted(notches):
        a, b = max(a, x0), min(b, x1)
        if b <= a:
            continue
        if a > x:
            pts += [(x, ytop), (a, ytop)]
        pts += [(a, ytop - depth), (b, ytop - depth)]
        x = b
    if x < x1:
        pts += [(x, ytop), (x1, ytop)]
    return pts


def _complement(spans, x0=0.0, x1=XMAX):
    """The parts of [x0, x1] that `spans` do not cover."""
    out, x = [], x0
    for a, b in sorted(spans):
        a, b = max(a, x0), min(b, x1)
        if b <= a:
            continue
        if a > x:
            out.append((x, a))
        x = max(x, b)
    if x < x1:
        out.append((x, x1))
    return out


def _layer(ax, profile, h, color, lw=0.4, zorder=None):
    """A layer of thickness h deposited conformally on a surface profile."""
    top = [(x, y + h) for x, y in reversed(profile)]
    ax.add_patch(Polygon(profile + top, closed=True, fc=C[color], ec='k',
                         lw=lw, zorder=zorder))


def _body(ax, x0, x1, ybot, color, trenches, lw):
    """One silicon region as a single closed polygon, trenches cut in."""
    top = _top_profile(x0, x1, SURF, trenches, STI_D)
    ax.add_patch(Polygon([(x0, ybot)] + top + [(x1, ybot)], closed=True,
                         fc=C[color], ec='k', lw=lw))


def wafer(ax, pwell=False, nwell=False, label=True, trenches=None):
    """Substrate and (optionally) the wells. `trenches` is a list of (x0, x1)
    spans that are etched STI_D deep into the silicon."""
    t = trenches or []
    _body(ax, 0, XMAX, 0, 'sub', t, 0.8)
    if label:
        ax.text(XMAX / 2, 0.4, 'p-substrate', ha='center', fontsize=8)
    if pwell:
        _body(ax, 0, WELL_X, 2.2, 'pwell', t, 0.5)
        ax.text(WELL_X / 2, 2.5, 'p-well', ha='center', fontsize=8)
    if nwell:
        _body(ax, WELL_X, XMAX, 2.2, 'nwell', t, 0.5)
        ax.text((WELL_X + XMAX) / 2, 2.5, 'n-well', ha='center', fontsize=8)


def sti(ax, trenches=None, fox=0.0):
    """Fill the etched trenches with oxide. The trench walls are already part
    of the silicon outline, so only the top surface adds a new edge. `fox`
    leaves a field oxide of that height standing on top of the isolation,
    drawn as one shape with the trench fill below it."""
    for x0, x1 in (trenches or STI_X):
        ax.add_patch(Rectangle((x0, SURF - STI_D), x1 - x0, STI_D + fox,
                               fc=C['ox'], ec='k', lw=0.6))


def field_oxide(ax, h=FOX_H, trenches=None):
    """The field oxide as grown, blanketing the whole wafer and merged with
    the oxide already filling the trenches underneath."""
    bot = _top_profile(0, XMAX, SURF, trenches or STI_X, STI_D)
    ax.add_patch(Polygon(bot + [(XMAX, SURF + h), (0, SURF + h)], closed=True,
                         fc=C['ox'], ec='k', lw=0.6))


def hard_mask(ax, openings=None, y=SURF, h=0.25, color='mask'):
    """Cover the wafer surface with a masking layer, leaving openings
    (list of (x0, x1)) uncovered."""
    openings = sorted(openings or [])
    x = 0.0
    for x0, x1 in openings + [(XMAX, XMAX)]:
        if x0 > x:
            ax.add_patch(Rectangle((x, y), x0 - x, h, fc=C[color],
                                   ec='k', lw=0.5))
        x = x1


def resist(ax, openings=None, y=None, h=0.45):
    if y is None:
        y = SURF + 0.25
    hard_mask(ax, openings=openings, y=y, h=h, color='resist')


def implant_arrows(ax, y0=6.6, y1=5.6, n=12, label=None):
    for i in range(n):
        x = (i + 0.5) * XMAX / n
        ax.annotate('', xy=(x, y1), xytext=(x, y0),
                    arrowprops=dict(arrowstyle='->', lw=0.8))
    if label:
        ax.text(XMAX / 2, y0 + 0.25, label, ha='center', fontsize=9)


def gate_stack(ax, oxide_everywhere=False, poly_everywhere=False,
               patterned=True, fox=0.0):
    """Gate oxide and polysilicon. With a field oxide of height `fox` present,
    the gate oxide grows only on the exposed active areas and the deposited
    poly follows the topography instead of lying flat."""
    t_ox = 0.1
    if oxide_everywhere:
        spans = _complement(STI_X) if fox else [(0, XMAX)]
        for x0, x1 in spans:
            ax.add_patch(Rectangle((x0, SURF), x1 - x0, t_ox, fc=C['ox'],
                                   ec='k', lw=0.4))
    if poly_everywhere:
        # without a field oxide the gate oxide covers everything and the
        # poly lies flat; with one, it steps up over the isolation
        prof = _top_profile(0, XMAX, SURF + t_ox, STI_X,
                            t_ox - fox if fox else 0.0)
        _layer(ax, prof, 0.35, 'poly')
    if patterned:
        for g in (NG, PG):
            ax.add_patch(Rectangle((g[0], SURF), g[1] - g[0], 0.12,
                                   fc=C['ox'], ec='k', lw=0.4, zorder=3))
            ax.add_patch(Rectangle((g[0], SURF + 0.12), g[1] - g[0], 0.5,
                                   fc=C['poly'], ec='k', lw=0.4, zorder=3))


def _implant(ax, spans, color, label):
    for x0, x1 in spans:
        ax.add_patch(Rectangle((x0, SURF - SD_D), x1 - x0, SD_D,
                               fc=C[color], ec='k', lw=0.5))
        # centred in the part of the implant the silicide does not cover
        ax.text((x0 + x1) / 2, SURF - (SD_D + SIL_T) / 2, label,
                ha='center', va='center', fontsize=7, color='white')


def implants(ax, ntype=True, ptype=True):
    """Source/drain implants. Each also forms a well tap: the n+ implant
    contacts the n-well, the p+ implant the p-well."""
    if ntype:
        _implant(ax, NSD + [NTAP], 'nplus', '$n^+$')
    if ptype:
        _implant(ax, PSD + [PTAP], 'pplus', '$p^+$')


def spacers(ax):
    for g in (NG, PG):
        for side, sgn in ((g[0], -1), (g[1], 1)):
            tri = [(side, SURF), (side + sgn * SPACER_W, SURF),
                   (side, SURF + 0.6)]
            ax.add_patch(Polygon(tri, closed=True, fc=C['nit'],
                                 ec='k', lw=0.4, zorder=3))


def _spacer_feet():
    """The strips of silicon surface the spacers cover at the gate edges."""
    feet = []
    for g in (NG, PG):
        feet += [(g[0] - SPACER_W, g[0]), (g[1], g[1] + SPACER_W)]
    return feet


def silicide(ax):
    """Silicide on every exposed silicon surface. The spacers mask the strip
    of source/drain beside each gate — that is what they are there for: it
    keeps the silicide off the junction edge and stops it shorting the gate
    to the source/drain."""
    t = SIL_T
    feet = _spacer_feet()
    for span in NSD + PSD + [PTAP, NTAP]:
        for x0, x1 in _complement(feet, *span):
            ax.add_patch(Rectangle((x0, SURF - t), x1 - x0, t, fc=C['sil'],
                                   ec='none', zorder=4))
    for g in (NG, PG):
        ax.add_patch(Rectangle((g[0], SURF + 0.62 - t), g[1] - g[0], t,
                               fc=C['sil'], ec='none', zorder=4))


# one contact per source/drain and per well tap
CONTACTS = [sum(s) / 2 for s in [PTAP] + NSD + PSD + [NTAP]]
M1 = [(c - 0.5, c + 0.5) for c in CONTACTS]
VIA12 = [sum(NSD[0]) / 2, sum(PSD[0]) / 2]

# back-end stack, all heights measured from the wafer surface
PLUG_W = 0.24               # contact and via width
ILD_H = 1.1                 # dielectric up to the underside of metal-1
M1_Y, M1_H = ILD_H, 0.35    # metal-1
VIA_H = 0.7                 # via-12
M2_Y = M1_Y + M1_H + VIA_H  # dielectric up to the underside of metal-2
M2_H = 0.35


def dielectric(ax, top=ILD_H, fox=FOX_H):
    """The dielectric stack, from the wafer topography up to `top` above the
    surface. It is deposited in several steps — ILD, then IMD between and
    over metal-1 — but is one material, so it is drawn as a single body with
    no seam between the levels. The underside follows the field oxide; the
    top is flat, as left by CMP."""
    bot = _top_profile(0, XMAX, SURF, STI_X, -fox)
    ax.add_patch(Polygon(bot + [(XMAX, SURF + top), (0, SURF + top)],
                         closed=True, fc=C['ild'], ec='k', lw=0.5, zorder=2))


def _plug_line(x0, x1, y, h, plugs, y_plug):
    """A metal line from x0 to x1 at height y, merged with the plugs that
    drop out of it down to y_plug, so the two show no seam where they meet."""
    pts = [(x0, y)]
    for c in sorted(plugs):
        pts += [(c - PLUG_W / 2, y), (c - PLUG_W / 2, y_plug),
                (c + PLUG_W / 2, y_plug), (c + PLUG_W / 2, y)]
    return pts + [(x1, y), (x1, y + h), (x0, y + h)]


def _metal(ax, pts):
    ax.add_patch(Polygon(pts, closed=True, fc=C['metal'], ec='k', lw=0.5,
                         zorder=5))


def contacts(ax, h=ILD_H):
    """The contact plugs on their own, before metal-1 is deposited."""
    for x in CONTACTS:
        ax.add_patch(Rectangle((x - PLUG_W / 2, SURF), PLUG_W, h,
                               fc=C['metal'], ec='k', lw=0.4, zorder=5))


def metal1(ax):
    """Metal-1, drawn as one shape with the contact plugs beneath it."""
    for (x0, x1), c in zip(M1, CONTACTS):
        _metal(ax, _plug_line(x0, x1, SURF + M1_Y, M1_H, [c], SURF))


def via_metal2(ax):
    """Metal-2, drawn as one shape with the via-12 beneath it."""
    for c in VIA12:
        _metal(ax, _plug_line(c - 1.0, c + 1.0, SURF + M2_Y, M2_H, [c],
                              SURF + M1_Y + M1_H))
