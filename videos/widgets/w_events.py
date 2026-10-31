# -*- coding: utf-8 -*-
"""Event-algebra widgets for the הסתברות videos of course `events` (E01..E10), plus the exact checks the scripts
assert with. Every CSS class is prefixed ev- so other courses are untouched.

Exact math: finite probability spaces with Fraction weights. The dice / urn spaces come from the course checker
(tools/verify/needhelp/events/check.py: dice(), urn()), so a video counts on the very space the app's checker uses.
  Space(outcomes)                [(dict, Fraction)], must sum to 1;  Space.dice(n)  Space.urn(...)  Space.uniform(items)
    .P(pred, given=None)         exact (Fraction), pred/given are callables on the outcome dict
    .both(pred, given=None)      exact, and a Monte Carlo cross-check within 5 standard errors (asserted)
  ft(x) "3/10" (SVG text)   tx(x) "\\frac{3}{10}" (TeX)   dec(x) "0.35"

Stage widgets (SVG has no TeX; labels are plain text):
  Venn(pfx, ...)       two events in Ω. Regions: "a" = A only, "ab" = A∩B, "b" = B only, "o" = outside both.
      .fill(name, regions, cls)  -> layer id {pfx}-{name} (hidden)
      .text(name, region|(x,y), lines, cls) -> text id {pfx}-{name} (hidden unless shown=True)
  DiceGrid(pfx, values) the 36 outcomes of two dice, die 1 = rows, die 2 = columns.
      .layer(name, pred, cls)    -> {pfx}-{name}: every cell (i, j) with pred(i, j), as one hidden layer
  Tree(pfx, spec)      probability tree, root on the left. spec = [(key, label, prob, children)], prob a Fraction,
                       or (sympy value, text) for a symbolic branch; the branches of every node must sum to 1.
      ids: {pfx}-b-{path} a branch (edge + prob + node label; hidden when hidden=True),
           {pfx}-hl-{path} the edge highlighted, {pfx}-p-{path} the product at a leaf (always hidden at start)
      .path_hl(path) the highlight ids along a path;  .leaf_prob(path) exact product along the path
  Urn(pfx, items)      balls in a jar: items = [(label, cls)], cls "r" (red) / "k" (black) / "t" (teal) / "g" (gray).
      ids: {pfx}-k{i} ball, {pfx}-x{i} "removed" overlay, {pfx}-h{i} highlight ring (both hidden)
  cells_table(pfx, vals, shown)  2x2 table of A/Ā × B/B̄ with margins. keys: ab an nb nn (cells: A∩B, A∩B̄, Ā∩B, Ā∩B̄), mA mnA mB mnB tot (margins).
      ids: {pfx}-<key> value (hidden unless in shown), {pfx}-h-<key> highlight
"""
import html as _html
import math
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

from events.check import dice as _dice, urn as _urn       # the course checker (SIM_PATHS)

_rng = np.random.default_rng(20261031)


def esc(s):
    return _html.escape(str(s), quote=True)


def ft(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def tx(x):
    x = Fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = "-" if x < 0 else ""
    return f"{s}\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def dec(x, nd=4):
    x = Fr(x)
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    assert Fr(s) == x, f"{x} is not exactly {s}"
    return s


# ---------------------------------------------------------------- exact spaces
class Space:
    def __init__(self, outcomes):
        self.out = [(o, Fr(w)) for o, w in outcomes if Fr(w) != 0]
        assert sum(w for _, w in self.out) == 1, "outcome probabilities do not sum to 1"

    @classmethod
    def dice(cls, n):
        return cls(_dice(n))

    @classmethod
    def urn(cls, **kw):
        return cls(_urn(**kw))

    @classmethod
    def uniform(cls, items):
        items = list(items)
        return cls([(o, Fr(1, len(items))) for o in items])

    def P(self, pred, given=None):
        den = sum((w for o, w in self.out if given is None or given(o)), Fr(0))
        num = sum((w for o, w in self.out if (given is None or given(o)) and pred(o)), Fr(0))
        assert den > 0, "conditioning on an empty event"
        return num / den

    def count(self, pred):
        return sum(1 for o, _ in self.out if pred(o))

    def both(self, pred, given=None, n=400_000):
        ex = self.P(pred, given)
        w = np.array([float(x) for _, x in self.out])
        idx = _rng.choice(len(self.out), size=n, p=w / w.sum())
        e = np.array([bool(pred(o)) for o, _ in self.out])[idx]
        g = np.array([True if given is None else bool(given(o)) for o, _ in self.out])[idx]
        k = int(g.sum())
        assert k >= 1000, "too few Monte Carlo trials meet the condition"
        est = float((e & g).sum()) / k
        se = math.sqrt(max(est * (1 - est), 1e-12) / k)
        assert abs(est - float(ex)) <= 5 * se + 1e-9, f"Monte Carlo {est:.5f} vs exact {float(ex):.5f}"
        return ex


# ---------------------------------------------------------------- Venn diagram of two events
class Venn:
    def __init__(self, pfx, w=700, h=440, names=("A", "B"), omega="Ω", r=None, gap=0.58):
        self.pfx, self.w, self.h, self.names, self.omega = pfx, w, h, names, omega
        self.r = r or round(h * 0.37)
        self.cy = h / 2 + 14
        self.ca = w / 2 - gap * self.r
        self.cb = w / 2 + gap * self.r
        self.layers, self.texts = [], []
        r = self.r
        self.at = {"a": (self.ca - 0.5 * r, self.cy), "ab": (w / 2, self.cy), "b": (self.cb + 0.5 * r, self.cy),
                   "o": (64, h - 34)}

    def _shape(self, region, cls):
        p, r, cy = self.pfx, self.r, self.cy
        A = f'cx="{self.ca:.1f}" cy="{cy:.1f}" r="{r}"'
        B = f'cx="{self.cb:.1f}" cy="{cy:.1f}" r="{r}"'
        if region == "ab":
            return f'<circle {B} class="ev-r {cls}" clip-path="url(#{p}-cpA)"/>'
        if region == "a":
            return f'<circle {A} class="ev-r {cls}" mask="url(#{p}-mnB)"/>'
        if region == "b":
            return f'<circle {B} class="ev-r {cls}" mask="url(#{p}-mnA)"/>'
        if region == "o":
            return f'<rect x="8" y="8" width="{self.w - 16}" height="{self.h - 16}" rx="18" class="ev-r {cls}" mask="url(#{p}-mnAB)"/>'
        raise ValueError(region)

    def fill(self, name, regions, cls="ev"):
        self.layers.append((name, "".join(self._shape(g, cls) for g in regions)))
        return f"{self.pfx}-{name}"

    def text(self, name, where, lines, cls="", shown=False, size=None):
        x, y = self.at[where] if isinstance(where, str) else where
        lines = [lines] if isinstance(lines, str) else list(lines)
        lh = (size or 32) * 1.15
        y0 = y - (len(lines) - 1) * lh / 2 + 10
        st = f' style="font-size:{size}px"' if size else ""
        ts = "".join(f'<tspan x="{x:.1f}" y="{y0 + k * lh:.1f}">{esc(t.replace(" ", chr(0x2002)))}</tspan>'
                     for k, t in enumerate(lines))
        self.texts.append(f'<text id="{self.pfx}-{name}" class="ev-vt {cls}{"" if shown else " h"}"{st}>{ts}</text>')
        return f"{self.pfx}-{name}"

    def svg(self):
        p, w, h, r, cy = self.pfx, self.w, self.h, self.r, self.cy
        A = f'cx="{self.ca:.1f}" cy="{cy:.1f}" r="{r}"'
        B = f'cx="{self.cb:.1f}" cy="{cy:.1f}" r="{r}"'
        defs = (f'<defs><clipPath id="{p}-cpA"><circle {A}/></clipPath>'
                f'<mask id="{p}-mnA"><rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/><circle {A} fill="#000"/></mask>'
                f'<mask id="{p}-mnB"><rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/><circle {B} fill="#000"/></mask>'
                f'<mask id="{p}-mnAB"><rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/><circle {A} fill="#000"/>'
                f'<circle {B} fill="#000"/></mask></defs>')
        layers = "".join(f'<g id="{p}-{n}" class="h">{body}</g>' for n, body in self.layers)
        frame = (f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="18" class="ev-om"/>'
                 f'<circle {A} class="ev-c"/><circle {B} class="ev-c"/>'
                 f'<text x="34" y="52" class="ev-nm om">{esc(self.omega)}</text>'
                 f'<text x="{self.ca - 0.78 * r:.1f}" y="{cy - 0.80 * r:.1f}" class="ev-nm">{esc(self.names[0])}</text>'
                 f'<text x="{self.cb + 0.78 * r:.1f}" y="{cy - 0.80 * r:.1f}" class="ev-nm">{esc(self.names[1])}</text>')
        return (f'<svg class="ev-svg" id="{p}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">'
                f'{defs}{layers}{frame}{"".join(self.texts)}</svg>')


# ---------------------------------------------------------------- two dice: the 6 x 6 grid
class DiceGrid:
    def __init__(self, pfx, values=None, cell=64, rows="קובייה ראשונה", cols="קובייה שנייה"):
        self.pfx, self.values, self.cell, self.rows, self.cols = pfx, values, cell, rows, cols
        self.layers = []
        self.x0, self.y0 = 92, 82

    def cells(self, pred):
        return [(i, j) for i in range(1, 7) for j in range(1, 7) if pred(i, j)]

    def layer(self, name, pred, cls="ev"):
        c, x0, y0 = self.cell, self.x0, self.y0
        body = "".join(f'<rect x="{x0 + (j - 1) * c + 3}" y="{y0 + (i - 1) * c + 3}" width="{c - 6}" height="{c - 6}" '
                       f'rx="9" class="ev-cell {cls}"/>' for i, j in self.cells(pred))
        self.layers.append((name, body))
        return f"{self.pfx}-{name}"

    def svg(self):
        c, x0, y0, p = self.cell, self.x0, self.y0, self.pfx
        w, h = x0 + 6 * c + 10, y0 + 6 * c + 10
        o = [f'<svg class="ev-svg" id="{p}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">']
        for i in range(1, 7):
            for j in range(1, 7):
                o.append(f'<rect x="{x0 + (j - 1) * c + 2}" y="{y0 + (i - 1) * c + 2}" width="{c - 4}" height="{c - 4}" '
                         f'rx="10" class="ev-bg"/>')
        o += [f'<g id="{p}-{n}" class="h">{b}</g>' for n, b in self.layers]
        for k in range(1, 7):
            o.append(f'<text x="{x0 + (k - 0.5) * c:.1f}" y="{y0 - 14}" class="ev-gh">{k}</text>')
            o.append(f'<text x="{x0 - 22}" y="{y0 + (k - 0.5) * c + 10:.1f}" class="ev-gh">{k}</text>')
        o.append(f'<text x="{x0 + 3 * c}" y="{y0 - 50}" class="ev-gt">{esc(self.cols)}</text>')
        o.append(f'<text x="{x0 - 64}" y="{y0 + 3 * c}" class="ev-gt" transform="rotate(-90 {x0 - 64} {y0 + 3 * c})">'
                 f'{esc(self.rows)}</text>')
        if self.values:
            for i in range(1, 7):
                for j in range(1, 7):
                    o.append(f'<text x="{x0 + (j - 0.5) * c:.1f}" y="{y0 + (i - 0.5) * c + 10:.1f}" class="ev-gv">'
                             f'{esc(self.values(i, j))}</text>')
        o.append("</svg>")
        return "".join(o)


# ---------------------------------------------------------------- probability tree
class Tree:
    """spec: [(key, label, prob, children)], children in the same shape ([] for a leaf). Root on the left."""

    def __init__(self, pfx, spec, w=760, h=560, hidden=True, leaf_gap=None, prod_text=None, xs=None):
        self.pfx, self.spec, self.w, self.h, self.hidden = pfx, spec, w, h, hidden
        self.prod_text = prod_text or {}
        self._check(spec)
        self.leaves = []
        self._collect(spec, "")
        depth = max(len(pth) for pth in self.leaves)
        self.xs = xs or ([30] + [round(w * (0.34 + 0.36 * k)) for k in range(depth)] if depth == 2
                         else [30, round(w * 0.42)])
        n = len(self.leaves)
        gap = leaf_gap or (h - 40) / n
        self.ly = {pth: 20 + gap * (k + 0.5) for k, pth in enumerate(self.leaves)}

    @staticmethod
    def _val(pr):
        return pr[0] if isinstance(pr, tuple) else pr

    @staticmethod
    def _txt(pr):
        return pr[1] if isinstance(pr, tuple) else ft(pr)

    def _check(self, spec):
        tot = sum(sp.sympify(self._val(pr)) for _, _, pr, _ in spec)
        assert sp.simplify(tot - 1) == 0, "branches of a node must sum to 1"
        for _, _, _, ch in spec:
            if ch:
                self._check(ch)

    def _collect(self, spec, path):
        for key, _, _, ch in spec:
            if ch:
                self._collect(ch, path + key)
            else:
                self.leaves.append(path + key)

    def _y(self, path, spec=None):
        if path in self.ly:
            return self.ly[path]
        kids = [pth for pth in self.leaves if pth.startswith(path)]
        return sum(self.ly[k] for k in kids) / len(kids) if path else sum(self.ly.values()) / len(self.ly)

    def _node(self, path):
        spec, node = self.spec, None
        for ch in path:
            node = next(t for t in spec if t[0] == ch)
            spec = node[3]
        return node

    def leaf_prob(self, path):
        pr = sp.Integer(1)
        for k in range(1, len(path) + 1):
            pr *= sp.sympify(self._val(self._node(path[:k])[2]))
        pr = sp.simplify(pr)
        return Fr(int(pr.p), int(pr.q)) if pr.is_Rational else pr

    def path_hl(self, path):
        return [f"{self.pfx}-hl-{path[:k]}" for k in range(1, len(path) + 1)]

    def svg(self):
        p = self.pfx
        base, hl, nodes, prods = [], [], [], []

        def walk(spec, path, depth):
            x1, y1 = self.xs[depth], self._y(path)
            for key, label, pr, ch in spec:
                pth = path + key
                x2, y2 = self.xs[depth + 1], self._y(pth)
                sx = x1 + 14
                ex = x2 - 16
                mx, my = (sx + ex) / 2, (y1 + y2) / 2
                ang = math.atan2(y2 - y1, ex - sx)
                if y2 > y1 + 1:                         # a branch going down: its label below the line
                    tx_, ty_ = mx - 26 * math.sin(ang), my + 26 * math.cos(ang) + 22
                else:                                   # going up or level: above the line
                    tx_, ty_ = mx + 26 * math.sin(ang), my - 26 * math.cos(ang) + 4
                if ch:                                  # inner node: label above (or below) the node, a dot on it
                    ly = y2 - 22 if y2 <= y1 else y2 + 42
                    lab = (f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="7" class="ev-root"/>'
                           f'<text x="{x2:.1f}" y="{ly:.1f}" class="ev-nl mid">{esc(label)}</text>')
                else:
                    lab = f'<text x="{x2 + 4:.1f}" y="{y2 + 11:.1f}" class="ev-nl">{esc(label)}</text>'
                g = (f'<g id="{p}-b-{pth}"{" class=\"h\"" if self.hidden else ""}>'
                     f'<line x1="{sx:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{y2:.1f}" class="ev-edge"/>'
                     f'<text x="{tx_:.1f}" y="{ty_:.1f}" class="ev-pr">{esc(self._txt(pr))}</text>{lab}</g>')
                base.append(g)
                hl.append(f'<line id="{p}-hl-{pth}" x1="{sx:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{y2:.1f}" class="ev-edge-hi h"/>')
                if ch:
                    walk(ch, pth, depth + 1)
                else:
                    lp = self.leaf_prob(pth)
                    t = self.prod_text.get(pth, f"= {ft(lp)}" if isinstance(lp, Fr) else "")
                    px = x2 + 30 + 17 * len(label)
                    prods.append(f'<text id="{p}-p-{pth}" x="{px:.1f}" y="{y2 + 11:.1f}" class="ev-lp h">{esc(t)}</text>')

        walk(self.spec, "", 0)
        root = f'<circle cx="{self.xs[0]}" cy="{self._y(""):.1f}" r="9" class="ev-root"/>'
        return (f'<svg class="ev-svg" id="{p}" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'direction="ltr">{"".join(hl)}{"".join(base)}{root}{"".join(prods)}</svg>')


# ---------------------------------------------------------------- urn of balls
class Urn:
    def __init__(self, pfx, items, per_row=5, d=78):
        self.pfx, self.items, self.per_row, self.d = pfx, list(items), per_row, d

    def svg(self):
        p, d, n, k = self.pfx, self.d, len(self.items), self.per_row
        rows = math.ceil(n / k)
        w = k * d + 60
        h = rows * d + 70
        o = [f'<svg class="ev-svg" id="{p}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">',
             f'<path d="M14,22 L14,{h - 30} Q14,{h - 8} 40,{h - 8} L{w - 40},{h - 8} Q{w - 14},{h - 8} {w - 14},{h - 30} '
             f'L{w - 14},22" class="ev-jar"/>']
        for i, (label, cls) in enumerate(self.items):
            r_, c_ = divmod(i, k)
            cx = 30 + d / 2 + c_ * d
            cy = 40 + d / 2 + r_ * d
            rr = d / 2 - 6
            o.append(f'<g id="{p}-k{i}"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" class="ev-ball {cls}"/>'
                     f'<text x="{cx:.1f}" y="{cy + 11:.1f}" class="ev-bl">{esc(label)}</text></g>'
                     f'<circle id="{p}-h{i}" cx="{cx:.1f}" cy="{cy:.1f}" r="{rr + 5:.1f}" class="ev-ring h"/>'
                     f'<g id="{p}-x{i}" class="h"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr + 2:.1f}" class="ev-gone"/>'
                     f'<line x1="{cx - rr * .7:.1f}" y1="{cy - rr * .7:.1f}" x2="{cx + rr * .7:.1f}" y2="{cy + rr * .7:.1f}" class="ev-xl"/>'
                     f'<line x1="{cx - rr * .7:.1f}" y1="{cy + rr * .7:.1f}" x2="{cx + rr * .7:.1f}" y2="{cy - rr * .7:.1f}" class="ev-xl"/></g>')
        o.append("</svg>")
        return "".join(o)


# ---------------------------------------------------------------- the four cells of two events
def cells_table(pfx, vals, shown=(), a="A", b="B"):
    """vals: {key: TeX} for keys ab an nb nn mA mnA mB mnB tot. Rows A / Ā, columns B / B̄, margins on the far side."""
    def cell(k, tag="td", extra=""):
        v = vals.get(k, "")
        hide = "" if k in shown else " h"
        return (f'<{tag} class="{extra}"><i id="{pfx}-h-{k}" class="ev-hl h"></i>'
                f'<span id="{pfx}-{k}" class="ev-tv{hide}">{"$" + v + "$" if v else ""}</span></{tag}>')
    na, nb = f"\\overline{{{a}}}", f"\\overline{{{b}}}"
    return (f'<table class="ev-tab" id="{pfx}"><thead><tr><th></th><th>${b}$</th><th>${nb}$</th>'
            f'<th class="ev-mc">סה״כ</th></tr></thead><tbody>'
            f'<tr><th class="ev-rh">${a}$</th>{cell("ab")}{cell("an")}{cell("mA", extra="ev-mc ev-m")}</tr>'
            f'<tr><th class="ev-rh">${na}$</th>{cell("nb")}{cell("nn")}{cell("mnA", extra="ev-mc ev-m")}</tr>'
            f'<tr><th class="ev-rh ev-mr">סה״כ</th>{cell("mB", extra="ev-mr ev-m")}{cell("mnB", extra="ev-mr ev-m")}'
            f'{cell("tot", extra="ev-mr ev-mc ev-m")}</tr></tbody></table>')
