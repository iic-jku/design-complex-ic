"""Drawing helpers for layout (mask top-view) figures.

Layer names and drawing conventions follow the generic layer definition
used in the course text (RX, PC, NW, BP, OP, CA, M1, V1, M2).

Copyright (C) 2017-2026 Harald Pretl and co-authors (harald.pretl@jku.at)
Licensed under the Apache License, Version 2.0.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

LAYERS = {
    'NW': dict(fc='#dce9f5', ec='#7a9cbf', lw=1.0, ls='--', alpha=1.0, z=1),
    'BP': dict(fc='none', ec='#d1862c', lw=1.2, hatch='///', alpha=1.0, z=2),
    'RX': dict(fc='#9fd6a1', ec='#2e7d32', lw=1.0, alpha=1.0, z=3),
    'OP': dict(fc='none', ec='#888888', lw=1.0, hatch='\\\\\\', alpha=1.0, z=4),
    'PC': dict(fc='#e57373', ec='#b71c1c', lw=1.0, alpha=0.9, z=5),
    'CA': dict(fc='#222222', ec='k', lw=0.5, alpha=1.0, z=7),
    'M1': dict(fc='#64a0e8', ec='#1a5cb0', lw=1.0, alpha=0.55, z=6),
    'V1': dict(fc='#eeeeee', ec='k', lw=0.8, alpha=1.0, z=8),
    'M2': dict(fc='#b39ddb', ec='#5e35b1', lw=1.0, alpha=0.55, z=7),
}


def rect(ax, layer, x, y, w, h):
    s = LAYERS[layer]
    kw = dict(fc=s['fc'], ec=s['ec'], lw=s['lw'], alpha=s['alpha'],
              zorder=s['z'])
    if 'ls' in s:
        kw['ls'] = s['ls']
    if 'hatch' in s:
        kw['hatch'] = s['hatch']
    ax.add_patch(Rectangle((x, y), w, h, **kw))


def contacts(ax, x0, y0, nx, ny, pitch=0.6, size=0.32, layer='CA'):
    for i in range(nx):
        for j in range(ny):
            rect(ax, layer, x0 + i * pitch, y0 + j * pitch, size, size)


def legend(ax, layers, loc='upper right', ncol=1):
    handles = []
    for name in layers:
        s = LAYERS[name]
        handles.append(Patch(fc=s['fc'] if s['fc'] != 'none' else 'white',
                             ec=s['ec'], lw=s['lw'],
                             hatch=s.get('hatch'), alpha=s['alpha'],
                             label=name))
    ax.legend(handles=handles, loc=loc, fontsize=8, ncol=ncol,
              framealpha=0.95)


def finish(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
