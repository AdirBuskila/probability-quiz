# -*- coding: utf-8 -*-
"""Circuit widgets for the circ videos (C01..C09): an SVG circuit drawn from the same tree the checker uses
(tools/verify/needhelp/circ/circuits_lib.py), with per-unit overlays that the timeline fades in and out, plus the
exact-probability helpers every script asserts with.

Tree (circuits_lib): ("C", "A") a unit, ("S", [kids]) series, ("P", [kids]) parallel,
("BR", (tl, tr, bl, br, mid)) the five-unit bridge (top-left, top-right, bottom-left, bottom-right, middle).
A series/parallel node may carry a name as a third item, ("P", [kids], "bc"): it gets a dashed block frame.

Ids (all hidden at start):
  {pfx}-u-<X>     the unit itself (VISIBLE at start; hide it to replace the unit by a wire or to cut it)
  {pfx}-ok-<X>    green ring: the unit works          {pfx}-x-<X>   red ring + cross: the unit failed
  {pfx}-w-<X>     a bright wire in place of the unit  {pfx}-cut-<X> a dashed ghost: the unit is cut out
  {pfx}-p-<X>     the probability label under the unit (visible when probs are given and hide_probs is False)
  {pfx}-blk-<n>   dashed frame around the named block {pfx}-bt-<n>  its tag (text from tags={n: "..."})
  {pfx}-on        the whole circuit lit (works)       {pfx}-off     the whole circuit dimmed (fails)

Exact checks: sprob(event, weights) enumerates every 0/1 state of the units with sympy weights, so a symbolic answer
is the full truth table summed; fprob is the same with Fractions (circuits_lib.prob).
"""
import itertools
import pathlib
import sys
from xml.sax.saxutils import escape

import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools" / "verify" / "needhelp" / "circ"))
import circuits_lib as cl  # noqa: E402

S, Pa, C, BR, fprob = cl.S, cl.P, cl.C, cl.BR, cl.prob


def strip(t):
    """drop block names: the checker's tree"""
    if t[0] in ("S", "P"):
        return (t[0], [strip(ch) for ch in t[1]])
    return (t[0], t[1])


def works(tree, st):
    return cl.works(strip(tree), st)
p, q = sp.symbols("p q", positive=True)

R = 32          # unit radius
GAP = 44        # wire between series items
VG = 26         # gap between parallel branches
RAIL = 40       # horizontal stub from a rail to a branch
LEAD = 56       # in/out leads
PL = 34         # room under a unit for its probability label
BW, BH = 400, 300   # bridge core


# ---------------------------------------------------------------- exact probability
def sprob(event, weights, given=None):
    """weights: {unit: sympy prob of working} (independent units) or a callable state -> weight (dependent units,
    then pass ids=... via weights.ids). Returns the simplified exact P(event | given)."""
    if callable(weights):
        ids, wf = weights.ids, weights
    else:
        ids = sorted(weights)
        wf = lambda st: sp.Mul(*[(weights[i] if st[i] else 1 - weights[i]) for i in ids])
    num = den = sp.Integer(0)
    for bits in itertools.product((False, True), repeat=len(ids)):
        st = dict(zip(ids, bits))
        w = wf(st)
        if given is None or given(st):
            den += w
            if event(st):
                num += w
    return sp.factor(sp.simplify(num / den))


def N(node, name):
    """name a series/parallel block: it gets a dashed frame {pfx}-blk-<name> and an optional tag"""
    return (node[0], node[1], name)


def same(ids, val=p):
    return {i: val for i in ids}


def eq(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


# ---------------------------------------------------------------- drawing
def _node(t):
    k, v = t[0], t[1]
    name = t[2] if len(t) > 2 else None
    return k, v, name


class Circ:
    def __init__(self, pfx, tree, probs=None, tags=None, hide_probs=False, scale=1.0, lead=True):
        self.pfx, self.tree, self.probs, self.tags = pfx, tree, dict(probs or {}), dict(tags or {})
        self.hide_probs, self.scale, self.lead = hide_probs, scale, lead
        self.pos, self.dirs, self.units, self.frames = {}, {}, [], []

    # layout: returns (w, h, cy, draw(x, y) -> [svg])
    def _lay(self, t):
        k, v, name = _node(t)
        lab = PL if self.probs else 0
        if k == "C":
            def draw(x, y, v=v):
                cx, cy = x + R, y + R
                self.pos[v] = (cx, cy)
                self.dirs[v] = ((cx - R, cy), (cx + R, cy))
                self.units.append(v)
                return []
            return 2 * R, 2 * R + lab, R, draw
        if k == "BR":
            a, b, c, d, e = v

            def draw(x, y):
                L, T, U, Rt = (x, y + BH / 2), (x + BW / 2, y), (x + BW / 2, y + BH), (x + BW, y + BH / 2)
                out = [f'<line x1="{L[0]}" y1="{L[1]}" x2="{T[0]}" y2="{T[1]}"/>',
                       f'<line x1="{T[0]}" y1="{T[1]}" x2="{Rt[0]}" y2="{Rt[1]}"/>',
                       f'<line x1="{L[0]}" y1="{L[1]}" x2="{U[0]}" y2="{U[1]}"/>',
                       f'<line x1="{U[0]}" y1="{U[1]}" x2="{Rt[0]}" y2="{Rt[1]}"/>']
                for i, (P1, P2) in zip((a, b, c, d), ((L, T), (T, Rt), (L, U), (U, Rt))):
                    self.pos[i] = ((P1[0] + P2[0]) / 2, (P1[1] + P2[1]) / 2)
                    self.dirs[i] = (P1, P2)
                    self.units.append(i)
                self.pos[e] = ((T[0] + U[0]) / 2, (T[1] + U[1]) / 2)
                self.dirs[e] = (T, U)
                self.units.append(e)
                for P0 in (L, T, U, Rt):
                    out.append(f'<circle cx="{P0[0]}" cy="{P0[1]}" r="6" class="circ-dot"/>')
                return out
            return BW, BH + (lab if self.probs else 0), BH / 2, draw
        subs = [self._lay(ch) for ch in v]
        if k == "S":
            top = max(s[2] for s in subs)
            bot = max(s[1] - s[2] for s in subs)
            w = sum(s[0] for s in subs) + GAP * (len(subs) - 1)

            def draw(x, y):
                out, cx = [], x
                for i, (sw, sh, scy, sd) in enumerate(subs):
                    out += sd(cx, y + top - scy)
                    if i < len(subs) - 1:
                        out.append(f'<line x1="{cx + sw}" y1="{y + top}" x2="{cx + sw + GAP}" y2="{y + top}"/>')
                    cx += sw + GAP
                if name:
                    self.frames.append((name, x, y, w, top + bot))
                return out
            return w, top + bot, top, draw
        # parallel
        mw = max(s[0] for s in subs)
        w = mw + 2 * RAIL
        h = sum(s[1] for s in subs) + VG * (len(subs) - 1)
        ys, y0 = [], 0
        for s in subs:
            ys.append(y0)
            y0 += s[1] + VG
        wy = [ys[i] + subs[i][2] for i in range(len(subs))]
        cy = (wy[0] + wy[-1]) / 2

        def draw(x, y):
            out = [f'<line x1="{x}" y1="{y + wy[0]}" x2="{x}" y2="{y + wy[-1]}"/>',
                   f'<line x1="{x + w}" y1="{y + wy[0]}" x2="{x + w}" y2="{y + wy[-1]}"/>']
            for i, (sw, sh, scy, sd) in enumerate(subs):
                bx = x + RAIL + (mw - sw) / 2
                out.append(f'<line x1="{x}" y1="{y + wy[i]}" x2="{bx}" y2="{y + wy[i]}"/>')
                out.append(f'<line x1="{bx + sw}" y1="{y + wy[i]}" x2="{x + w}" y2="{y + wy[i]}"/>')
                out += sd(bx, y + ys[i])
            if name:
                self.frames.append((name, x, y, w, h))
            return out
        return w, h, cy, draw

    def svg(self):
        self.pos, self.dirs, self.units, self.frames = {}, {}, [], []
        w, h, cy, draw = self._lay(self.tree)
        pad, top = 26, 70           # room for block tags above
        lead = LEAD if self.lead else 0
        W, H = w + 2 * lead + 2 * pad, h + top + pad
        x0, y0 = pad + lead, top
        wires = draw(x0, y0)
        pf = self.pfx
        o = [f'<svg class="circ-svg" id="{pf}" viewBox="0 0 {W:.0f} {H:.0f}" width="{W * self.scale:.0f}" '
             f'height="{H * self.scale:.0f}" direction="ltr">']
        if self.lead:
            o.append(f'<g class="circ-wire"><line x1="{pad}" y1="{y0 + cy}" x2="{x0}" y2="{y0 + cy}"/>'
                     f'<line x1="{x0 + w}" y1="{y0 + cy}" x2="{x0 + w + lead}" y2="{y0 + cy}"/></g>'
                     f'<circle cx="{pad}" cy="{y0 + cy}" r="7" class="circ-term"/>'
                     f'<circle cx="{x0 + w + lead}" cy="{y0 + cy}" r="7" class="circ-term"/>')
        o.append(f'<g class="circ-wire">{"".join(wires)}</g>')
        o.append(f'<rect id="{pf}-on" class="circ-on h" x="{x0 - 14}" y="{y0 - 14}" width="{w + 28}" height="{h + 28}" rx="22"/>')
        for name, fx, fy, fw, fh in self.frames:
            o.append(f'<rect id="{pf}-blk-{name}" class="circ-blk h" x="{fx - 12}" y="{fy - 12}" width="{fw + 24}" '
                     f'height="{fh + 24}" rx="16"/>')
            if name in self.tags:
                tag = self.tags[name]
                text, where = (tag, "top") if isinstance(tag, str) else tag
                tx, anc = {"top": (fx + fw / 2, "middle"), "topright": (fx + fw + 4, "end"),
                           "topleft": (fx - 4, "start")}[where]
                o.append(f'<text id="{pf}-bt-{name}" class="circ-bt h" x="{tx}" y="{fy - 22}" '
                         f'style="text-anchor:{anc}">{escape(text)}</text>')
        for u in self.units:
            cx, cy_ = self.pos[u]
            (ax, ay), (bx, by) = self.dirs[u]
            if self.tree[0] == "BR" and u == self.tree[1][4]:   # the bridge's middle unit owns its wire
                wire = f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" class="circ-own"/>'
            else:
                wire = ""
            plab = ""
            if self.probs and u in self.probs:
                lx, ly = (ax, ay - 16) if wire else (cx, cy_ + R + 30)     # the bridge's middle: above its top node
                cls = "circ-pl h" if self.hide_probs else "circ-pl"
                plab = f'<text id="{pf}-p-{u}" class="{cls}" x="{lx}" y="{ly}">{escape(str(self.probs[u]))}</text>'
            o.append(f'<g id="{pf}-u-{u}">{wire}<circle cx="{cx}" cy="{cy_}" r="{R}" class="circ-unit"/>'
                     f'<text x="{cx}" y="{cy_ + 11}" class="circ-ul">{escape(u)}</text></g>{plab}')
            o.append(f'<line id="{pf}-w-{u}" class="circ-short h" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}"/>')
            o.append(f'<g id="{pf}-cut-{u}" class="h"><line class="circ-ghost" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}"/>'
                     f'<circle cx="{cx}" cy="{cy_}" r="{R}" class="circ-ghostu"/></g>')
            o.append(f'<circle id="{pf}-ok-{u}" class="circ-ok h" cx="{cx}" cy="{cy_}" r="{R + 7}"/>')
            d = R * 0.55
            o.append(f'<g id="{pf}-x-{u}" class="h"><circle class="circ-bad" cx="{cx}" cy="{cy_}" r="{R + 7}"/>'
                     f'<path class="circ-cross" d="M{cx - d},{cy_ - d} L{cx + d},{cy_ + d} M{cx + d},{cy_ - d} L{cx - d},{cy_ + d}"/></g>')
        o.append(f'<rect id="{pf}-off" class="circ-off h" x="{x0 - 14}" y="{y0 - 14}" width="{w + 28}" height="{h + 28}" rx="22"/>')
        o.append("</svg>")
        return "".join(o)


def states(pfx, st):
    """show() ids for a 0/1 state dict: ok rings for working units, crosses for failed ones"""
    return [f"{pfx}-{'ok' if v else 'x'}-{u}" for u, v in st.items()]


def clear(pfx, units):
    return [f"{pfx}-{k}-{u}" for u in units for k in ("ok", "x")]


def table(pfx, head, rows, cls=""):
    """a small LTR table; row i has id {pfx}-r-<i> (hidden), cells may hold $TeX$"""
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join(f'<tr id="{pfx}-r-{i}" class="h">' + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                 for i, r in enumerate(rows))
    return f'<table class="circ-tab {cls}" id="{pfx}" dir="ltr"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
