"""Drawing helpers for layout (mask top-view) figures.

Layer names and drawing conventions follow the generic layer definition
used in the course text (RX, PC, NW, BP, OP, CA, M1, V1, M2).

Copyright (C) 2017-2026 Harald Pretl and co-authors (harald.pretl@jku.at)
Licensed under the Apache License, Version 2.0.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Patch

LAYERS = {
    'NW': dict(fc='#dce9f5', ec='#7a9cbf', lw=1.0, ls='--', alpha=1.0, z=1),
    'BP': dict(fc='none', ec='#d1862c', lw=1.2, hatch='///', alpha=1.0, z=2),
    'RX': dict(fc='#9fd6a1', ec='#2e7d32', lw=1.0, alpha=1.0, z=3),
    'OP': dict(fc='none', ec='#aaaaaa', lw=0.8, hatch='\\\\', alpha=1.0, z=4,
               hlw=0.5),
    'PC': dict(fc='#e57373', ec='#b71c1c', lw=1.0, alpha=0.9, z=5),
    'CA': dict(fc='#222222', ec='k', lw=0.5, alpha=1.0, z=7),
    'M1': dict(fc='#64a0e8', ec='#1a5cb0', lw=1.0, alpha=0.55, z=6),
    'V1': dict(fc='#eeeeee', ec='k', lw=0.8, alpha=1.0, z=8),
    'M2': dict(fc='#b39ddb', ec='#5e35b1', lw=1.0, alpha=0.55, z=7),
}


def _draw(ax, layer, make):
    s = LAYERS[layer]
    kw = dict(fc=s['fc'], ec=s['ec'], lw=s['lw'], alpha=s['alpha'],
              zorder=s['z'])
    if 'ls' in s:
        kw['ls'] = s['ls']
    if 'hatch' in s:
        kw['hatch'] = s['hatch']
    p = make(kw)
    if 'hlw' in s:
        p.set_hatch_linewidth(s['hlw'])
    ax.add_patch(p)


def rect(ax, layer, x, y, w, h):
    _draw(ax, layer, lambda kw: Rectangle((x, y), w, h, **kw))


def poly(ax, layer, points):
    """Draw one merged polygon on *layer*.

    Use this instead of several overlapping rects wherever the shapes belong
    to the same net on the same layer: a single polygon has no internal
    edges and therefore reads as the one piece of metal that it is.
    """
    _draw(ax, layer, lambda kw: Polygon(points, closed=True, **kw))


def contacts(ax, x0, y0, nx, ny, pitch=0.6, size=0.32, layer='CA'):
    for i in range(nx):
        for j in range(ny):
            rect(ax, layer, x0 + i * pitch, y0 + j * pitch, size, size)


def legend(ax, layers, loc='upper right', ncol=1):
    handles = []
    for name in layers:
        s = LAYERS[name]
        h = Patch(fc=s['fc'] if s['fc'] != 'none' else 'white',
                  ec=s['ec'], lw=s['lw'],
                  hatch=s.get('hatch'), alpha=s['alpha'], label=name)
        if 'hlw' in s:
            h.set_hatch_linewidth(s['hlw'])
        handles.append(h)
    ax.legend(handles=handles, loc=loc, fontsize=8, ncol=ncol,
              framealpha=0.95)


def align_legend_tops(fig, ref_ax, *axes):
    """Shift the legends of *axes* down so their top edge matches ref_ax's.

    Legends placed with a 'lower ...' location share a common bottom edge, so
    a legend with more entries sticks out further up. This lines up the top
    edges instead, which reads better across subplots.
    """
    fig.canvas.draw()
    ref_top = ref_ax.get_legend().get_window_extent().y1
    for ax in axes:
        leg = ax.get_legend()
        dy = (ref_top - leg.get_window_extent().y1) / ax.get_window_extent().height
        leg.set_bbox_to_anchor((0, dy, 1, 1), transform=ax.transAxes)


def finish(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
