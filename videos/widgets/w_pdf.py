# -*- coding: utf-8 -*-
"""Density / CDF widgets for the הסתברות videos of course `pdf` (F01..F09), plus the exact checks the scripts assert
with. Every class is prefixed pd- so other courses are untouched.

Exact math (sympy) and numeric cross-checks (mpmath.quad):
  Pdf(pieces)            pieces = [(lo, hi, expr in x)], lo/hi may be +-oo; 0 outside the pieces
    .total()  .mean()  .moment(k)    exact integrals (sympy), each also integrated numerically and compared
    .F(v)                            F(v) exactly (piece by piece)
    .Fpiece(k)                       F(t) on piece k as an expression in t: F(lo_k) + int_lo^t f
    .prob(a, b)                      P(a < X < b) exactly
    .nonneg(n)                       f >= 0 on a grid of every piece (numeric, endpoints included)
    .fnum(v)                         float density (for drawing)
  nint(expr, lo, hi)     numeric integral (mpmath), for the cross-checks
  close(a, b)            exact value a vs float b

Stage widgets (HTML / SVG; SVG never contains TeX, labels are plain unicode text):
  Plot(pfx, xr, yr, ...)    axes with independent x / y scales, ticks given as (value, text). Methods (hidden by default):
     area(id, f, a, b)          the region under y = f(x), a <= x <= b (a probability)
     curve(id, f, a, b)         the graph y = f(x) on [a, b]   (clip=ymax cuts an unbounded density at the top)
     seg(id, pts)               a polyline in data coordinates
     vline(id, x, y0, y1)       a dashed vertical guide
     hline(id, y, x0, x1)       a dashed horizontal guide
     dot(id, x, y, text)        a point with an optional label (open=True: a hollow dot)
     label(id, x, y, text)      a text label (unicode, no TeX)
     svg()
  eqs(pfx, lines)          a column of display formulas revealed one by one: ids {pfx}-0, {pfx}-1, …
  chip(id, html, kind)     a result pill (ok / bad / warn)
  stem(qid, html)          the exam question in the panel (bank id chip + statement)
  raster_crop(id, src, size, w, keep)  an original exam figure, scaled to width w, showing only the left `keep` of it
"""
import html as _html
import math

import mpmath as mp
import sympy as sp

x, t = sp.symbols("x t", real=True)
R = sp.Rational
oo = sp.oo


# ---------------------------------------------------------------- exact + numeric checks
def nint(expr, lo, hi, var=x):
    f = sp.lambdify(var, expr, "mpmath")
    a = -mp.inf if lo == -oo else mp.mpf(float(lo))
    b = mp.inf if hi == oo else mp.mpf(float(hi))
    return float(mp.quad(f, [a, b]))


def close(exact, num, tol=1e-7):
    return abs(float(exact) - float(num)) < tol


class Pdf:
    def __init__(self, pieces):
        self.pieces = [(sp.sympify(lo), sp.sympify(hi), sp.sympify(e)) for lo, hi, e in pieces]

    def _int(self, g):
        """exact sum of int g(x) f(x) over the pieces, checked against mpmath"""
        tot = 0
        for lo, hi, e in self.pieces:
            v = sp.simplify(sp.integrate(g * e, (x, lo, hi)))
            assert v.is_finite, (g, e, lo, hi, v)
            assert close(v, nint(g * e, lo, hi)), (g, e, lo, hi, v)
            tot += v
        return sp.nsimplify(sp.simplify(tot))

    def total(self):
        return self._int(sp.Integer(1))

    def mean(self):
        return self._int(x)

    def moment(self, k):
        return self._int(x ** k)

    def F(self, v):
        v = sp.sympify(v)
        tot, num = 0, 0.0
        for lo, hi, e in self.pieces:
            if v <= lo:
                continue
            up = hi if v >= hi else v
            tot += sp.integrate(e, (x, lo, up))
            num += nint(e, lo, up)
        tot = sp.simplify(tot)
        assert close(tot, num), (v, tot, num)
        return tot

    def Fpiece(self, k):
        lo, hi, e = self.pieces[k]
        u = sp.Symbol("u", real=True)
        base = self.F(lo) if lo != -oo else 0
        return sp.simplify(base + sp.integrate(e.subs(x, u), (u, lo, t)))

    def prob(self, a, b):
        return sp.simplify(self.F(b) - self.F(a))

    def nonneg(self, n=400):
        for lo, hi, e in self.pieces:
            a = float(lo) if lo != -oo else float(hi) - 30
            b = float(hi) if hi != oo else float(lo) + 30
            f = sp.lambdify(x, e, "math")
            for i in range(n + 1):
                xv = a + (b - a) * i / n
                if (lo == 0 and xv == 0) and not sp.limit(e, x, 0, "+").is_finite:
                    continue
                try:
                    if f(xv) < -1e-12:
                        return False
                except (ValueError, ZeroDivisionError):
                    continue
        return True

    def fnum(self, v):
        for lo, hi, e in self.pieces:
            if (lo == -oo or v >= float(lo)) and (hi == oo or v < float(hi)):
                return float(e.subs(x, v))
        return 0.0


# ---------------------------------------------------------------- the plot
def esc(s):
    return _html.escape(s, quote=True)


def _f(v):
    return f"{v:.1f}"


class Plot:
    def __init__(self, pfx, xr, yr, w=820, h=460, xticks=(), yticks=(), xname="x", yname="f(x)", pad=(56, 60, 56, 54)):
        (self.x0, self.x1), (self.y0, self.y1) = xr, yr
        self.pfx, self.w, self.h = pfx, w, h
        self.pl, self.pr, self.pt, self.pb = pad
        self.kx = (w - self.pl - self.pr) / (self.x1 - self.x0)
        self.ky = (h - self.pt - self.pb) / (self.y1 - self.y0)
        self.xticks, self.yticks, self.xname, self.yname = list(xticks), list(yticks), xname, yname
        self.layers = {"fill": [], "guide": [], "curve": [], "dot": [], "label": []}

    def X(self, v):
        return self.pl + (v - self.x0) * self.kx

    def Y(self, v):
        return self.pt + (self.y1 - v) * self.ky

    def _d(self, pts, close=False):
        s = "M" + " L".join(f"{_f(self.X(a))},{_f(self.Y(b))}" for a, b in pts)
        return s + (" Z" if close else "")

    @staticmethod
    def _h(hidden):
        return " h" if hidden else ""

    def _sample(self, f, a, b, n, clip=None):
        pts = []
        for i in range(n + 1):
            v = a + (b - a) * i / n
            try:
                y = f(v)
            except (ValueError, ZeroDivisionError):
                y = clip if clip is not None else 0
            if clip is not None:
                y = min(y, clip)
            pts.append((v, y))
        return pts

    def area(self, id_, f, a, b, kind="a", hidden=True, n=160, clip=None):
        pts = [(a, 0)] + self._sample(f, a, b, n, clip) + [(b, 0)]
        self.layers["fill"].append(f'<path id="{id_}" class="pd-fill k-{kind}{self._h(hidden)}" d="{self._d(pts, True)}"/>')
        return id_

    def curve(self, id_, f, a, b, kind="a", hidden=True, n=200, clip=None, dash=False):
        return self.seg(id_, self._sample(f, a, b, n, clip), kind=kind, hidden=hidden, dash=dash)

    def seg(self, id_, pts, kind="a", hidden=True, dash=False):
        cls = f"pd-cv k-{kind}" + (" dash" if dash else "") + self._h(hidden)
        self.layers["curve"].append(f'<path id="{id_}" class="{cls}" d="{self._d(pts)}"/>')
        return id_

    def vline(self, id_, xv, y0, y1, hidden=True):
        self.layers["guide"].append(f'<line id="{id_}" class="pd-guide{self._h(hidden)}" x1="{_f(self.X(xv))}" '
                                    f'x2="{_f(self.X(xv))}" y1="{_f(self.Y(y0))}" y2="{_f(self.Y(y1))}"/>')
        return id_

    def hline(self, id_, yv, x0, x1, hidden=True):
        self.layers["guide"].append(f'<line id="{id_}" class="pd-guide{self._h(hidden)}" y1="{_f(self.Y(yv))}" '
                                    f'y2="{_f(self.Y(yv))}" x1="{_f(self.X(x0))}" x2="{_f(self.X(x1))}"/>')
        return id_

    def dot(self, id_, xv, yv, text=None, dx=14, dy=-16, anchor="start", hidden=True, kind="ink", open=False):
        px, py = self.X(xv), self.Y(yv)
        tx = (f'<text class="pd-pt" x="{_f(px + dx)}" y="{_f(py + dy)}" text-anchor="{anchor}">{esc(text)}</text>'
              if text else "")
        cls = f"pd-dot k-{kind}" + (" open" if open else "")
        self.layers["dot"].append(f'<g id="{id_}" class="{self._h(hidden).strip()}">'
                                  f'<circle class="{cls}" cx="{_f(px)}" cy="{_f(py)}" r="9"/>{tx}</g>')
        return id_

    def label(self, id_, xv, yv, text, kind="ink", anchor="middle", hidden=True, size=None):
        stl = f' style="font-size:{size}px"' if size else ""
        self.layers["label"].append(f'<text id="{id_}" class="pd-lb k-{kind}{self._h(hidden)}" x="{_f(self.X(xv))}" '
                                    f'y="{_f(self.Y(yv))}" text-anchor="{anchor}"{stl}>{esc(text)}</text>')
        return id_

    def _axes(self):
        o = []
        ay = min(max(0, self.y0), self.y1)
        ax = min(max(0, self.x0), self.x1)
        for v, _ in self.yticks:
            o.append(f'<line class="pd-grid" y1="{_f(self.Y(v))}" y2="{_f(self.Y(v))}" x1="{_f(self.X(self.x0))}" '
                     f'x2="{_f(self.X(self.x1))}"/>')
        m = f"{self.pfx}-ah"
        o.append(f'<defs><marker id="{m}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" '
                 f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#9aa0cf"/></marker></defs>')
        o.append(f'<line class="pd-ax" x1="{_f(self.X(self.x0) - 8)}" x2="{_f(self.X(self.x1) + 22)}" y1="{_f(self.Y(ay))}" '
                 f'y2="{_f(self.Y(ay))}" marker-end="url(#{m})"/>')
        o.append(f'<line class="pd-ax" y1="{_f(self.Y(self.y0) + 6)}" y2="{_f(self.Y(self.y1) - 22)}" x1="{_f(self.X(ax))}" '
                 f'x2="{_f(self.X(ax))}" marker-end="url(#{m})"/>')
        o.append(f'<text class="pd-an" x="{_f(self.X(self.x1) + 30)}" y="{_f(self.Y(ay) + 9)}">{esc(self.xname)}</text>')
        o.append(f'<text class="pd-an" x="{_f(self.X(ax) + 14)}" y="{_f(self.Y(self.y1) - 26)}" text-anchor="start">'
                 f'{esc(self.yname)}</text>')
        for v, s in self.xticks:
            o.append(f'<line class="pd-tk" x1="{_f(self.X(v))}" x2="{_f(self.X(v))}" y1="{_f(self.Y(ay) - 6)}" '
                     f'y2="{_f(self.Y(ay) + 6)}"/><text class="pd-tl" x="{_f(self.X(v))}" y="{_f(self.Y(ay) + 34)}" '
                     f'text-anchor="middle">{esc(s)}</text>')
        for v, s in self.yticks:
            o.append(f'<line class="pd-tk" y1="{_f(self.Y(v))}" y2="{_f(self.Y(v))}" x1="{_f(self.X(ax) - 6)}" '
                     f'x2="{_f(self.X(ax) + 6)}"/><text class="pd-tl" x="{_f(self.X(self.x0) - 12)}" '
                     f'y="{_f(self.Y(v) + 9)}" text-anchor="end">{esc(s)}</text>')
        return o

    def svg(self):
        body = self._axes()
        for k in ("fill", "guide", "curve", "dot", "label"):
            body += self.layers[k]
        return (f'<svg class="pd-plot" id="{self.pfx}" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" direction="ltr">{"".join(body)}</svg>')


# ---------------------------------------------------------------- HTML helpers
def eqs(pfx, lines, size=40, gap=14, shown=0):
    rows = "".join(f'<div id="{pfx}-{i}" class="pd-eq{"" if i < shown else " h"}">{s}</div>' for i, s in enumerate(lines))
    return f'<div class="pd-eqs" style="font-size:{size}px;gap:{gap}px">{rows}</div>'


def chip(id_, html_, kind="ok", hidden=True):
    return f'<div id="{id_}" class="pd-chip {kind}{" h" if hidden else ""}">{html_}</div>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{qid}</span>{html_}</div>'


def raster_crop(id_, src, size, w, keep=1.0):
    """an original exam figure at width w (of the full image), clipped to the left `keep` fraction (drops stray text
    that the PDF crop left at the right edge). Never redrawn, never edited."""
    sw, sh = size
    h = round(sh * w / sw)
    return (f'<div class="pd-raster" id="{id_}" style="width:{round(w * keep)}px;height:{h}px">'
            f'<img src="{esc(src)}" width="{w}" height="{h}"></div>')


def fx(s):
    r"""Chrome sets KaTeX's \ln t as 'lnt': put a thin space after \ln / \log before a letter or digit"""
    import re
    return re.sub(r"\\(ln|log)\s+(?=[A-Za-z0-9])", r"\\\1\\, ", s)


def fix_scenes(scenes):
    """apply fx() to every stage, panel and subtitle; returns the scenes"""
    for S in scenes:
        S.stage, S.panel = fx(S.stage), fx(S.panel)
        for p in S.phrases:
            p.sub = fx(p.sub)
    return scenes
