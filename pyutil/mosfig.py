"""Drawing helpers for the NMOS operation cross-section figures.

Copyright (C) 2017-2026 Harald Pretl and co-authors (harald.pretl@jku.at)
Licensed under the Apache License, Version 2.0.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

COL = {
    'sub': '#f5e9d0',      # p-doped silicon
    'nplus': '#aacdea',    # n+ diffusion
    'ox': '#c7dff2',       # gate oxide
    'poly': '#c46262',     # poly gate
    'metal': '#a0a0a0',    # contact metal
    'depl': '#fdf6e5',     # depletion region
    'inv': '#5588bb',      # inversion layer
}

# geometry (all in arbitrary units)
SURF = 3.0        # silicon surface
XL, XR = 0.0, 11.0
S_X = (1.0, 4.25)   # source n+ region
D_X = (6.75, 10.0)  # drain n+ region
G_X = (4.0, 7.0)    # gate stack


def _nplus(ax, x0, x1, label=True):
    ax.add_patch(Rectangle((x0, SURF - 1.0), x1 - x0, 1.0,
                           fc=COL['nplus'], ec='k', lw=0.8))
    if label:
        ax.text((x0 + x1) / 2, SURF - 0.5, r'$n^+$', ha='center',
                va='center', fontsize=9)


def _depletion(ax, under_gate=0.0, drain_extra=0.0):
    """Draw dashed depletion-region boundary around S/D junctions and,
    optionally, under the gate (depth given by under_gate). The drain-side
    depletion width can be increased by drain_extra."""
    m = 0.35  # margin around junctions
    # source-side boundary
    xs0, xs1 = S_X[0] - m, S_X[1] + (m if under_gate == 0 else 0)
    xd0, xd1 = D_X[0] - (m if under_gate == 0 else 0), D_X[1] + m + drain_extra
    ys = SURF - 1.0 - m
    yd = SURF - 1.0 - m - drain_extra
    if under_gate > 0:
        # one contiguous dashed outline from source around gate to drain
        yg = SURF - 0.35 - under_gate
        xx = [xs0, xs0, S_X[1], S_X[1] + 0.2]
        yy = [SURF, ys, ys, yg]
        xx += [D_X[0] - 0.2, D_X[0], xd1, xd1]
        yy += [yg, yd, yd, SURF]
        ax.plot(xx, yy, 'k--', lw=1.0)
    else:
        ax.plot([xs0, xs0, xs1, xs1], [SURF, ys, ys, SURF], 'k--', lw=1.0)
        ax.plot([xd0, xd0, xd1, xd1], [SURF, yd, yd, SURF], 'k--', lw=1.0)


def _inversion(ax, taper=0.0, pinchoff=False):
    """Draw the inversion layer under the gate. taper reduces the thickness
    towards the drain; pinchoff ends the layer before the drain."""
    t0 = 0.25  # thickness at source side
    x0, x1 = S_X[1], D_X[0]
    if pinchoff:
        x1 = x1 - 0.5
        t1 = 0.0
    else:
        t1 = t0 * (1.0 - taper)
    poly = [(x0, SURF), (x1, SURF), (x1, SURF - t1), (x0, SURF - t0)]
    ax.add_patch(Polygon(poly, closed=True, fc=COL['inv'], ec='none'))
    n = 4 if not pinchoff else 3
    for i in range(n):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        ax.text(x, SURF - 0.12, '$-$', ha='center', va='center',
                fontsize=8, color='white')


def _gate_charge(ax, n=5):
    for i in range(n):
        x = G_X[0] + (i + 0.5) * (G_X[1] - G_X[0]) / n
        ax.text(x, SURF + 0.7, '$+$', ha='center', va='center', fontsize=8)


def _acceptor_ions(ax, xs, y=SURF - 0.55):
    for x in xs:
        ax.text(x, y, '$-$', ha='center', va='center', fontsize=8)
        ax.add_patch(Circle((x, y), 0.17, fc='none', ec='k', lw=0.7))


def _holes(ax):
    for x in range(1, 11):
        ax.text(x, 1.0, '$+$', ha='center', va='center', fontsize=8)


def draw_nmos(ax, state, vg_label, vd_label):
    """Draw an NMOS cross section in a given operating state.

    state is one of 'flatband', 'zero', 'depletion', 'inversion',
    'triode', 'saturation'.
    """
    # substrate
    ax.add_patch(Rectangle((XL, 0), XR - XL, SURF, fc=COL['sub'],
                           ec='k', lw=0.8))
    ax.text(XR / 2, 0.35, 'p-doped Si', ha='center', fontsize=9)
    _holes(ax)

    # source/drain diffusions
    _nplus(ax, *S_X)
    _nplus(ax, *D_X)

    # gate stack
    ax.add_patch(Rectangle((G_X[0], SURF), G_X[1] - G_X[0], 0.5,
                           fc=COL['ox'], ec='k', lw=0.8))
    ax.text((G_X[0] + G_X[1]) / 2, SURF + 0.25, 'oxide', ha='center',
            va='center', fontsize=8)
    ax.add_patch(Rectangle((G_X[0], SURF + 0.5), G_X[1] - G_X[0], 0.4,
                           fc=COL['poly'], ec='k', lw=0.8))

    # contacts
    ax.add_patch(Rectangle((1.4, SURF), 2.0, 0.35, fc=COL['metal'],
                           ec='k', lw=0.8))
    ax.add_patch(Rectangle((7.6, SURF), 2.0, 0.35, fc=COL['metal'],
                           ec='k', lw=0.8))

    # terminal wires and labels
    ax.plot([2.4, 1.0], [SURF + 0.35, 5.0], 'k-', lw=1.0)
    ax.plot([8.6, 10.0], [SURF + 0.35, 5.0], 'k-', lw=1.0)
    ax.plot([5.5, 5.5], [SURF + 0.9, 5.0], 'k-', lw=1.0)
    ax.text(1.0, 5.15, 'Source $V_\\mathrm{S} = 0\\,$V', ha='center',
            fontsize=9)
    ax.text(10.0, 5.15, 'Drain ' + vd_label, ha='center', fontsize=9)
    ax.text(5.5, 5.15, 'Gate ' + vg_label, ha='center', fontsize=9)

    # state-dependent features
    if state == 'flatband':
        _depletion(ax)
        ax.text(5.0, SURF - 0.5, '$+$', ha='center', va='center', fontsize=8)
        ax.text(6.0, SURF - 0.5, '$+$', ha='center', va='center', fontsize=8)
    elif state == 'zero':
        _depletion(ax, under_gate=0.3)
        _acceptor_ions(ax, [5.0, 6.0], y=SURF - 0.2)
        ax.text(5.0, SURF - 0.8, '$+$', ha='center', va='center', fontsize=8)
        ax.text(6.0, SURF - 0.8, '$+$', ha='center', va='center', fontsize=8)
        _gate_charge(ax, 2)
    elif state == 'depletion':
        _depletion(ax, under_gate=0.8)
        _acceptor_ions(ax, [4.8, 5.5, 6.2], y=SURF - 0.4)
        _gate_charge(ax, 3)
    elif state == 'inversion':
        _depletion(ax, under_gate=1.3)
        _inversion(ax)
        _acceptor_ions(ax, [5.0, 6.0], y=SURF - 0.7)
        _gate_charge(ax)
    elif state == 'triode':
        _depletion(ax, under_gate=1.3, drain_extra=0.25)
        _inversion(ax, taper=0.5)
        _acceptor_ions(ax, [5.0, 6.0], y=SURF - 0.7)
        _gate_charge(ax)
    elif state == 'saturation':
        _depletion(ax, under_gate=1.3, drain_extra=0.5)
        _inversion(ax, pinchoff=True)
        _acceptor_ions(ax, [5.0, 6.0], y=SURF - 0.7)
        _gate_charge(ax)

    ax.set_xlim(-1.2, 12.2)
    ax.set_ylim(-0.3, 5.6)
    ax.set_aspect('equal')
    ax.axis('off')
