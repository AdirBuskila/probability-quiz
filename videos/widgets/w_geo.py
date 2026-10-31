# -*- coding: utf-8 -*-
"""Geometric-probability widgets for the geo videos (area method): a coordinate plane with the sample-space
rectangle, event regions, lines, curves and labelled points, plus a function plot (CDF / density) and the checks
that tie every drawn region to its probability.

Everything is SVG computed here in Python. SVG never contains TeX (labels are plain text: "1/3", "π/2"), so a
drawing is exactly the region that the script verified, nothing more.

Ids (all hidden at start unless shown=True):
  {pfx}-<name>   any layer created by Plane.poly / region / slab / line / curve / pt / text

Verification helpers (used by every script):
  clip(halfplanes, box)  exact polygon (Fractions) of a box cut by half-planes a*x + b*y < c  -> vertices
  area(poly)             exact shoelace area (Fractions when the vertices are Fractions)
  mc(pred, xr, yr, exact, given=None)   Monte Carlo of P(pred | given) on the uniform box, asserted within 5 SE
  grid(pred, xr, yr, given=None)        midpoint-grid estimate (deterministic), asserted within tol by the caller
"""
from fractions import Fraction as Fr
import math
import numpy as np

_rng = np.random.default_rng(20261031)


# ---------------------------------------------------------------- exact geometry
def clip(halfplanes, xr, yr):
    """the box xr x yr cut by half-planes (a, b, c, op) meaning a*x + b*y op c, op in '<', '>'.
    Sutherland-Hodgman with Fractions: exact vertices (counter-clockwise from the lower-left corner)."""
    x0, x1 = map(Fr, xr)
    y0, y1 = map(Fr, yr)
    poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for a, b, c, op in halfplanes:
        a, b, c = Fr(a), Fr(b), Fr(c)
        s = 1 if op in ("<", "<=") else -1
        inside = lambda p: s * (a * p[0] + b * p[1] - c) <= 0
        out = []
        for i in range(len(poly)):
            P, Q = poly[i], poly[(i + 1) % len(poly)]
            ip, iq = inside(P), inside(Q)
            if ip:
                out.append(P)
            if ip != iq:
                fp, fq = a * P[0] + b * P[1] - c, a * Q[0] + b * Q[1] - c
                t = fp / (fp - fq)
                out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
        poly = []
        for p in out:                                  # drop repeated vertices
            if not poly or poly[-1] != p:
                poly.append(p)
        if len(poly) > 1 and poly[0] == poly[-1]:
            poly.pop()
        if len(poly) < 3:
            return []
    return poly


def area(poly):
    """shoelace area (exact for Fraction vertices)"""
    n = len(poly)
    if n < 3:
        return Fr(0)
    s = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    return abs(s) / 2


# ---------------------------------------------------------------- numeric checks
def mc(pred, xr, yr, exact, given=None, n=2_000_000):
    """Monte Carlo of P(pred) (or P(pred | given)) for a point uniform on the box; asserts |est - exact| < 5 SE"""
    x = _rng.uniform(float(xr[0]), float(xr[1]), n)
    y = _rng.uniform(float(yr[0]), float(yr[1]), n)
    ev = pred(x, y)
    if given is not None:
        g = given(x, y)
        m = int(g.sum())
        est = float((ev & g).sum()) / m
    else:
        m = n
        est = float(ev.mean())
    p = float(exact)
    se = math.sqrt(max(p * (1 - p), 1e-12) / m)
    assert abs(est - p) < 5 * se + 1e-9, (est, p, se)
    return est


def grid(pred, xr, yr, given=None, n=1600):
    """deterministic midpoint-grid estimate of P(pred) (or P(pred | given))"""
    xs = float(xr[0]) + (np.arange(n) + 0.5) * (float(xr[1]) - float(xr[0])) / n
    ys = float(yr[0]) + (np.arange(n) + 0.5) * (float(yr[1]) - float(yr[0])) / n
    X, Y = np.meshgrid(xs, ys)
    ev = pred(X, Y)
    if given is not None:
        g = given(X, Y)
        return float((ev & g).sum()) / float(g.sum())
    return float(ev.mean())


# ---------------------------------------------------------------- drawing
def _f(v):
    return f"{float(v):.1f}"


class Plane:
    """a coordinate plane for the box xr x yr (or a plot area). Equal scales unless w and h are both given.
    xticks / yticks: [(value, label)]; labels are plain text. xlab / ylab: axis names (plain text, may use ₁ ₂)."""

    def __init__(self, pfx, xr, yr, maxw=470, maxh=470, w=None, h=None, xlab="X", ylab="Y", xticks=(), yticks=(),
                 frame=True, view=None, fs=26):
        self.pfx, self.xr, self.yr = pfx, tuple(map(float, xr)), tuple(map(float, yr))
        self.view = view or (self.xr, self.yr)            # the drawn window (a plot may extend past the box)
        (vx0, vx1), (vy0, vy1) = self.view
        if w and h:
            self.kx, self.ky = w / (vx1 - vx0), h / (vy1 - vy0)
        else:
            k = min(maxw / (vx1 - vx0), maxh / (vy1 - vy0))
            self.kx = self.ky = k
        self.ml, self.mt, self.mr, self.mb = 78, 62, 78, 50
        self.W = self.ml + self.kx * (vx1 - vx0) + self.mr
        self.H = self.mt + self.ky * (vy1 - vy0) + self.mb
        self.xlab, self.ylab, self.xticks, self.yticks, self.frame, self.fs = xlab, ylab, xticks, yticks, frame, fs
        self.layers = []
        self.defs = (f'<pattern id="{pfx}-hatch" width="14" height="14" patternUnits="userSpaceOnUse" '
                     f'patternTransform="rotate(45)"><rect width="14" height="14" fill="rgba(56,189,248,.10)"/>'
                     f'<line x1="0" y1="0" x2="0" y2="14" stroke="#38bdf8" stroke-width="5"/></pattern>')

    def X(self, x):
        return self.ml + self.kx * (float(x) - self.view[0][0])

    def Y(self, y):
        return self.mt + self.ky * (self.view[1][1] - float(y))

    def _cls(self, cls, shown):
        return cls + ("" if shown else " h")

    def _d(self, pts, close=True):
        d = "M" + " L".join(f"{_f(self.X(x))},{_f(self.Y(y))}" for x, y in pts)
        return d + (" Z" if close else "")

    # -- layers
    def poly(self, name, pts, cls="ev", shown=False):
        """a filled polygon. cls: ev (event, teal), given (condition, hatched blue), comp (complement, red),
        both (intersection, strong teal), om (the whole sample space, highlighted)"""
        fill = f' fill="url(#{self.pfx}-hatch)"' if cls == "given" else ""
        self.layers.append(f'<path id="{self.pfx}-{name}" class="geo-r {self._cls(cls, shown)}" d="{self._d(pts)}"{fill}/>')
        return pts

    def region(self, name, halfplanes, cls="ev", shown=False):
        """the box cut by half-planes; returns the exact polygon (its area: area(poly))"""
        pts = clip(halfplanes, self.xr, self.yr)
        assert pts, f"{name}: empty region"
        self.poly(name, pts, cls, shown)
        return pts

    def slab(self, name, lo, hi, xa, xb, cls="ev", shown=False, breaks=(), n=240):
        """{(x, y): xa < x < xb, lo(x) < y < hi(x)} clipped to the box (lo/hi may leave it); returns its numeric area"""
        y0, y1 = self.yr
        xs = sorted(set(np.linspace(float(xa), float(xb), n).tolist()) | {float(b) for b in breaks if xa <= b <= xb})
        top = [(x, min(max(hi(x), y0), y1)) for x in xs]
        bot = [(x, min(max(lo(x), y0), y1)) for x in xs]
        top = [(x, max(t, b)) for (x, t), (_, b) in zip(top, bot)]
        pts = top + bot[::-1]
        self.poly(name, pts, cls, shown)
        return float(area([(Fr(x), Fr(y)) for x, y in pts]))

    def line(self, name, a, b, c, cls="ln", shown=False, label=None, at=None, dx=10, dy=-12, anchor="start"):
        """the line a*x + b*y = c inside the box, optional plain-text label near the point at=(x, y)"""
        (x0, x1), (y0, y1) = self.xr, self.yr
        pts = []
        if b != 0:
            for x in (x0, x1):
                y = (c - a * x) / b
                if y0 - 1e-12 <= y <= y1 + 1e-12:
                    pts.append((x, y))
        if a != 0:
            for y in (y0, y1):
                x = (c - b * y) / a
                if x0 - 1e-12 <= x <= x1 + 1e-12:
                    pts.append((x, y))
        uniq = []
        for p in pts:
            if all(abs(p[0] - q[0]) > 1e-9 or abs(p[1] - q[1]) > 1e-9 for q in uniq):
                uniq.append(p)
        assert len(uniq) >= 2, f"{name}: line misses the box"
        p, q = uniq[0], uniq[1]
        lab = ""
        if label:
            lx, ly = at if at else ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
            lab = (f'<text class="geo-lt" x="{_f(self.X(lx) + dx)}" y="{_f(self.Y(ly) + dy)}" '
                   f'text-anchor="{anchor}">{label}</text>')
        self.layers.append(f'<g id="{self.pfx}-{name}" class="{self._cls(cls, shown)}">'
                           f'<path class="geo-line" d="{self._d([p, q], False)}"/>{lab}</g>')

    def seg(self, name, p, q, cls="ln", shown=False, dash=False):
        """a straight segment between two points (inside the window)"""
        self.layers.append(f'<path id="{self.pfx}-{name}" class="geo-line{" geo-dash" if dash else ""} '
                           f'{self._cls(cls, shown)}" d="{self._d([p, q], False)}"/>')

    def curve(self, name, f, xa, xb, cls="ln", shown=False, n=300, label=None, at=None, dx=10, dy=-12,
              anchor="start", clip_box=True):
        """the graph y = f(x) for xa..xb, cut where it leaves the window"""
        (vx0, vx1), (vy0, vy1) = self.view if not clip_box else (self.view[0], self.yr)
        runs, cur = [], []
        for x in np.linspace(float(xa), float(xb), n):
            y = f(x)
            if vy0 - 1e-9 <= y <= vy1 + 1e-9:
                cur.append((x, y))
            elif cur:
                runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        d = " ".join(self._d(r, False) for r in runs if len(r) > 1)
        lab = ""
        if label:
            lx, ly = at
            lab = (f'<text class="geo-lt" x="{_f(self.X(lx) + dx)}" y="{_f(self.Y(ly) + dy)}" '
                   f'text-anchor="{anchor}">{label}</text>')
        self.layers.append(f'<g id="{self.pfx}-{name}" class="{self._cls(cls, shown)}"><path class="geo-line" d="{d}"/>'
                           f'{lab}</g>')

    def pt(self, name, x, y, label="", shown=False, dx=12, dy=-12, anchor="start"):
        """a dot with a plain-text label"""
        self.layers.append(f'<g id="{self.pfx}-{name}" class="{self._cls("", shown)}">'
                           f'<circle class="geo-dot" cx="{_f(self.X(x))}" cy="{_f(self.Y(y))}" r="8"/>'
                           f'<text class="geo-pt" x="{_f(self.X(x) + dx)}" y="{_f(self.Y(y) + dy)}" '
                           f'text-anchor="{anchor}">{label}</text></g>')

    def text(self, name, x, y, label, shown=False, cls="geo-tag", anchor="middle"):
        """a plain-text label centred at (x, y) (math coordinates)"""
        self.layers.append(f'<text id="{self.pfx}-{name}" class="{cls}{"" if shown else " h"}" x="{_f(self.X(x))}" '
                           f'y="{_f(self.Y(y) + 10)}" text-anchor="{anchor}">{label}</text>')

    # -- the picture
    def svg(self):
        (x0, x1), (y0, y1) = self.xr, self.yr
        (vx0, vx1), (vy0, vy1) = self.view
        ax = []
        X0, Y0 = self.X(vx0), self.Y(vy0)
        ax.append(f'<path class="geo-axis" d="M{_f(X0)},{_f(Y0)} L{_f(self.X(vx1) + 26)},{_f(Y0)}"/>')
        ax.append(f'<path class="geo-axis" d="M{_f(X0)},{_f(Y0)} L{_f(X0)},{_f(self.Y(vy1) - 22)}"/>')
        ax.append(f'<text class="geo-ax" x="{_f(self.X(vx1) + 34)}" y="{_f(Y0 + 11)}" text-anchor="start">{self.xlab}</text>')
        ax.append(f'<text class="geo-ax" x="{_f(X0)}" y="{_f(self.Y(vy1) - 30)}" text-anchor="middle">{self.ylab}</text>')
        for v, lab in self.xticks:
            X = self.X(v)
            ax.append(f'<path class="geo-tick" d="M{_f(X)},{_f(Y0)} L{_f(X)},{_f(Y0 + 9)}"/>'
                      f'<text class="geo-tk" x="{_f(X)}" y="{_f(Y0 + 38)}" text-anchor="middle">{lab}</text>')
        for v, lab in self.yticks:
            Y = self.Y(v)
            ax.append(f'<path class="geo-tick" d="M{_f(X0 - 9)},{_f(Y)} L{_f(X0)},{_f(Y)}"/>'
                      f'<text class="geo-tk" x="{_f(X0 - 14)}" y="{_f(Y + 9)}" text-anchor="end">{lab}</text>')
        box = ""
        if self.frame:
            box = (f'<rect class="geo-box" x="{_f(self.X(x0))}" y="{_f(self.Y(y1))}" width="{_f(self.X(x1) - self.X(x0))}" '
                   f'height="{_f(self.Y(y0) - self.Y(y1))}"/>')
        edge = ""
        if self.frame:
            edge = (f'<rect class="geo-edge" x="{_f(self.X(x0))}" y="{_f(self.Y(y1))}" '
                    f'width="{_f(self.X(x1) - self.X(x0))}" height="{_f(self.Y(y0) - self.Y(y1))}"/>')
        return (f'<svg class="geo-svg" id="{self.pfx}" width="{_f(self.W)}" height="{_f(self.H)}" '
                f'viewBox="0 0 {_f(self.W)} {_f(self.H)}" direction="ltr"><defs>{self.defs}</defs>{box}'
                + "".join(l for l in self.layers if 'class="geo-r ' in l) + edge
                + "".join(l for l in self.layers if 'class="geo-r ' not in l) + "".join(ax) + "</svg>")


def bar(pfx, parts, width=560, label=""):
    """a probability bar: parts = [(name, fraction, cls, text)] stacked left to right over [0, 1]; ids {pfx}-<name>"""
    segs, x = [], 0.0
    for name, p, cls, text in parts:
        w = float(p) * width
        segs.append(f'<div id="{pfx}-{name}" class="geo-seg {cls} h" style="left:{x:.1f}px;width:{w:.1f}px">'
                    f'<span>{text}</span></div>')
        x += w
    return (f'<div class="geo-bar" id="{pfx}" style="width:{width}px" dir="ltr">{"".join(segs)}'
            f'<b class="geo-b0">0</b><b class="geo-b1">1</b></div>')
