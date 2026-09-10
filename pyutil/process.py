"""Drawing helpers for the CMOS process-flow cross-section figures.

The drawn geometry shows an NMOS (left, in the p-well) and a PMOS (right,
in the n-well) on a p-type substrate, evolving through the front-end and
back-end processing steps.

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
    'resist': '#9a7bd4',  # photo resist
    'mask': '#8ab6d6',    # hard mask (SiO2)
    'metal': '#8f8f8f',   # metal (Al)
    'sil': '#3a3a3a',     # silicide
    'ild': '#ebebeb',     # inter-layer dielectric
    'nit': '#c9c9a3',     # spacer nitride
}

SURF = 4.0
XMAX = 12.0

STI_X = [(0.0, 0.8), (5.3, 6.7), (11.2, 12.0)]
STI_D = 0.8   # trench depth

# NMOS geometry
NG = (2.55, 3.45)           # gate
NSD = [(1.2, 2.45), (3.55, 4.8)]
# PMOS geometry
PG = (8.55, 9.45)
PSD = [(7.2, 8.45), (9.55, 10.8)]

SD_D = 0.5    # junction depth


def setup(ax, title=None, ymax=7.2):
    ax.set_xlim(-0.2, XMAX + 0.2)
    ax.set_ylim(-0.3, ymax)
    ax.set_aspect('equal')
    ax.axis('off')
    if title is not None:
        ax.set_title(title, fontsize=9, loc='left')


def wafer(ax, pwell=False, nwell=False, label=True):
    ax.add_patch(Rectangle((0, 0), XMAX, SURF, fc=C['sub'], ec='k', lw=0.8))
    if label:
        ax.text(XMAX / 2, 0.4, 'p-substrate', ha='center', fontsize=8)
    if pwell:
        ax.add_patch(Rectangle((0, 2.2), 6, SURF - 2.2, fc=C['pwell'],
                               ec='k', lw=0.5))
        ax.text(2.0, 2.5, 'p-well', ha='center', fontsize=8)
    if nwell:
        ax.add_patch(Rectangle((6, 2.2), 6, SURF - 2.2, fc=C['nwell'],
                               ec='k', lw=0.5))
        ax.text(10.0, 2.5, 'n-well', ha='center', fontsize=8)


def sti(ax, etched=True, filled=True):
    for x0, x1 in STI_X:
        if filled:
            ax.add_patch(Rectangle((x0, SURF - STI_D), x1 - x0, STI_D,
                                   fc=C['ox'], ec='k', lw=0.6))
        elif etched:
            ax.add_patch(Rectangle((x0, SURF - STI_D), x1 - x0, STI_D,
                                   fc='white', ec='k', lw=0.6))


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
               patterned=True):
    if oxide_everywhere:
        ax.add_patch(Rectangle((0, SURF), XMAX, 0.1, fc=C['ox'],
                               ec='k', lw=0.4))
    if poly_everywhere:
        ax.add_patch(Rectangle((0, SURF + 0.1), XMAX, 0.35, fc=C['poly'],
                               ec='k', lw=0.4))
    if patterned:
        for g in (NG, PG):
            ax.add_patch(Rectangle((g[0], SURF), g[1] - g[0], 0.12,
                                   fc=C['ox'], ec='k', lw=0.4, zorder=3))
            ax.add_patch(Rectangle((g[0], SURF + 0.12), g[1] - g[0], 0.5,
                                   fc=C['poly'], ec='k', lw=0.4, zorder=3))


def implants(ax, ntype=True, ptype=True):
    if ntype:
        for x0, x1 in NSD:
            ax.add_patch(Rectangle((x0, SURF - SD_D), x1 - x0, SD_D,
                                   fc=C['nplus'], ec='k', lw=0.5))
            ax.text((x0 + x1) / 2, SURF - 0.27, '$n^+$', ha='center',
                    va='center', fontsize=7, color='white')
    if ptype:
        for x0, x1 in PSD:
            ax.add_patch(Rectangle((x0, SURF - SD_D), x1 - x0, SD_D,
                                   fc=C['pplus'], ec='k', lw=0.5))
            ax.text((x0 + x1) / 2, SURF - 0.27, '$p^+$', ha='center',
                    va='center', fontsize=7, color='white')


def spacers(ax):
    for g in (NG, PG):
        for side, sgn in ((g[0], -1), (g[1], 1)):
            tri = [(side, SURF), (side + sgn * 0.28, SURF),
                   (side, SURF + 0.6)]
            ax.add_patch(Polygon(tri, closed=True, fc=C['nit'],
                                 ec='k', lw=0.4, zorder=3))


def silicide(ax):
    t = 0.09
    for (x0, x1) in NSD + PSD:
        ax.add_patch(Rectangle((x0, SURF - t), x1 - x0, t, fc=C['sil'],
                               ec='none', zorder=4))
    for g in (NG, PG):
        ax.add_patch(Rectangle((g[0], SURF + 0.62 - t), g[1] - g[0], t,
                               fc=C['sil'], ec='none', zorder=4))


CONTACTS = [2.0, 4.0, 8.0, 10.0]   # x-centers of S/D contacts


def ild(ax, h=1.1):
    ax.add_patch(Rectangle((0, SURF), XMAX, h, fc=C['ild'], ec='k',
                           lw=0.5, zorder=2, alpha=0.8))


def contacts(ax, h=1.1):
    for x in CONTACTS:
        ax.add_patch(Rectangle((x - 0.12, SURF), 0.24, h, fc=C['metal'],
                               ec='k', lw=0.4, zorder=5))


M1 = [(1.5, 2.5), (3.5, 4.5), (7.5, 8.5), (9.5, 10.5)]


def metal1(ax, y=None, h=0.35):
    if y is None:
        y = SURF + 1.1
    for x0, x1 in M1:
        ax.add_patch(Rectangle((x0, y), x1 - x0, h, fc=C['metal'],
                               ec='k', lw=0.5, zorder=5))


def imd_via_metal2(ax):
    y0 = SURF + 1.45
    ax.add_patch(Rectangle((0, y0), XMAX, 0.7, fc=C['ild'], ec='k',
                           lw=0.5, zorder=2, alpha=0.8))
    for x in (2.0, 10.0):
        ax.add_patch(Rectangle((x - 0.12, y0), 0.24, 0.7, fc=C['metal'],
                               ec='k', lw=0.4, zorder=5))
    ax.add_patch(Rectangle((1.3, y0 + 0.7), 2.0, 0.35, fc=C['metal'],
                           ec='k', lw=0.5, zorder=5))
    ax.add_patch(Rectangle((8.7, y0 + 0.7), 2.0, 0.35, fc=C['metal'],
                           ec='k', lw=0.5, zorder=5))
