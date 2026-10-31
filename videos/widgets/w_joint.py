# -*- coding: utf-8 -*-
"""Joint-distribution widgets for the הסתברות videos of course `joint` (J01..J09), plus the exact checks the scripts
assert with. Every class is prefixed jt- so other courses are untouched.

Exact math (sympy, exact rationals and polynomials in p, q):
  Space(outcomes)               a finite experiment: [(prob, {name: value})], probabilities must sum to 1
    Space.product({n: [(v, pr)]})  independent components;   Space.uniform([dict, ...])
    .P(pred)  .E(f)  .joint(fx, fy) -> Joint   (cells grouped: outcomes with the same (x, y) are added)
  Joint(cells)                  {(x, y): prob}; asserts the normalization
    J(x, y)  .PX(x)  .PY(y)  .E(g)  .EX .EY .EXY .VX .VY .cov .rho  .cond_x(y)  .cond_y(x)  .Ecx(y)
    .independent()  .witness()  (first cell with P_XY != P_X P_Y)
  mc(gen, checks, n)            Monte Carlo cross-check of a generative simulation (numpy), each mean within 5 SE
  eq(a, b)                      exact equality after simplify

Stage widgets (HTML; math is $TeX$ rendered by the engine):
  table(pfx, J, cells, ...)     the joint table, x = rows, y = columns, optional margins. Ids (i, j = positions):
       {pfx}-v-i-j cell value   {pfx}-h-i-j teal highlight   {pfx}-w-i-j amber highlight
       {pfx}-mx-i / {pfx}-my-j marginal values, {pfx}-mxh / {pfx}-myh their headers, {pfx}-tot the corner total
  ids(pfx, kind, cells)         helper: ids of several cells, e.g. ids("t", "h", [(0, 1), (1, 1)])
  cards(pfx, items)             one card per outcome (lines of TeX); {pfx}-o-k card, {pfx}-oh-k highlight,
                                {pfx}-l-k-r line r of card k (lines from `reveal` on start hidden)
  eqs(pfx, lines)  chip(id, html, kind)  stem(qid, html)  box(id, html)
"""
import html as _html
import itertools

import numpy as np
import sympy as sp

R = sp.Rational
p, q = sp.symbols("p q", positive=True)


# ---------------------------------------------------------------- exact
def simp(e):
    e = sp.simplify(sp.sympify(e))
    return sp.factor(e) if e.free_symbols else sp.nsimplify(e)


def eq(a, b):
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


class Space:
    def __init__(self, outcomes):
        self.out = [(sp.sympify(w), o) for w, o in outcomes if sp.sympify(w) != 0]
        assert eq(sum(w for w, _ in self.out), 1), "probabilities of the outcomes do not sum to 1"

    @classmethod
    def product(cls, specs):
        names = list(specs)
        outs = []
        for combo in itertools.product(*(specs[n] for n in names)):
            w, o = sp.Integer(1), {}
            for n, (v, pr) in zip(names, combo):
                w *= sp.sympify(pr)
                o[n] = v
            outs.append((w, o))
        return cls(outs)

    @classmethod
    def uniform(cls, items):
        return cls([(R(1, len(items)), o) for o in items])

    def P(self, pred):
        return simp(sum((w for w, o in self.out if pred(o)), sp.Integer(0)))

    def E(self, f):
        return simp(sum((w * f(o) for w, o in self.out), sp.Integer(0)))

    def joint(self, fx, fy):
        cells = {}
        for w, o in self.out:
            k = (fx(o), fy(o))
            cells[k] = cells.get(k, 0) + w
        return Joint(cells)


class Joint:
    def __init__(self, cells, xs=None, ys=None):
        self.c = {k: simp(v) for k, v in cells.items()}
        self.xs = list(xs) if xs is not None else sorted({k[0] for k in cells})
        self.ys = list(ys) if ys is not None else sorted({k[1] for k in cells})
        assert eq(self.total(), 1), f"joint table sums to {self.total()}"

    def __call__(self, x, y):
        return self.c.get((x, y), sp.Integer(0))

    def total(self):
        return simp(sum(self.c.values()))

    def PX(self, x):
        return simp(sum(self(x, y) for y in self.ys))

    def PY(self, y):
        return simp(sum(self(x, y) for x in self.xs))

    def E(self, g):
        return simp(sum(g(x, y) * self(x, y) for x in self.xs for y in self.ys))

    @property
    def EX(self):
        return self.E(lambda x, y: x)

    @property
    def EY(self):
        return self.E(lambda x, y: y)

    @property
    def EXY(self):
        return self.E(lambda x, y: x * y)

    @property
    def VX(self):
        return simp(self.E(lambda x, y: x * x) - self.EX ** 2)

    @property
    def VY(self):
        return simp(self.E(lambda x, y: y * y) - self.EY ** 2)

    @property
    def cov(self):
        return simp(self.EXY - self.EX * self.EY)

    @property
    def rho(self):
        return sp.simplify(self.cov / sp.sqrt(self.VX * self.VY))

    def cond_x(self, y):
        return {x: simp(self(x, y) / self.PY(y)) for x in self.xs}

    def cond_y(self, x):
        return {y: simp(self(x, y) / self.PX(x)) for y in self.ys}

    def Ecx(self, y):
        return simp(sum(x * v for x, v in self.cond_x(y).items()))

    def witness(self):
        for x in self.xs:
            for y in self.ys:
                if not eq(self(x, y), self.PX(x) * self.PY(y)):
                    return (x, y)
        return None

    def independent(self):
        return self.witness() is None

    def subs(self, d):
        return Joint({k: v.subs(d) for k, v in self.c.items()}, self.xs, self.ys)


def mc(gen, checks, n=400_000, seed=7):
    """gen(rng, n) -> {name: numpy array}; checks: [(label, f(d) -> array, exact)]: mean of f within 5 SE of exact"""
    rng = np.random.default_rng(seed)
    d = gen(rng, n)
    for label, f, exact in checks:
        v = np.asarray(f(d), dtype=float)
        m, se = v.mean(), v.std() / np.sqrt(n)
        assert abs(m - float(exact)) <= 5 * se + 1e-9, (label, m, float(exact), se)
    return True


# ---------------------------------------------------------------- formatting
def frac(v):
    """an exact rational -> TeX (0, 1, \\frac{a}{b}, -\\frac{a}{b})"""
    v = sp.nsimplify(v)
    assert v.is_Rational, v
    if v.q == 1:
        return str(v.p)
    s = "-" if v < 0 else ""
    return f"{s}\\frac{{{abs(v.p)}}}{{{v.q}}}"


def dec(v, nd=3, fixed=False):
    """an exact rational with a terminating decimal -> '0.15' (asserts it terminates within nd digits);
    fixed=True keeps nd digits (0.30)"""
    v = sp.nsimplify(v)
    s = f"{float(v):.{nd}f}"
    if not fixed:
        s = s.rstrip("0").rstrip(".")
    assert sp.nsimplify(s) == v, (v, s)
    return s if s not in ("-0",) else "0"


# ---------------------------------------------------------------- widgets
def esc(s):
    return _html.escape(s, quote=True)


def _cell_tex(cells, x, y, v):
    if cells == "frac":
        return frac(v)
    if cells == "dec":
        return dec(v)
    t, e = cells[(x, y)]
    assert eq(e, v), f"cell ({x},{y}): shown {e}, table has {v}"
    return t


def table(pfx, J, cells="frac", xname="x", yname="y", mx=None, my=None, tot=False, shown=False, size=34,
          xlab=None, ylab=None, mxh="P_X(x)", myh="P_Y(y)", pad="10px 22px", mshown=False):
    """cells: 'frac' | 'dec' | {(x, y): (tex, expr)} (expr is asserted equal to the table's cell).
    mx / my: 'frac' | 'dec' | {x: (tex, expr)} the marginals (asserted), or None for no margin column / row."""
    xlab = xlab or {x: str(x) for x in J.xs}
    ylab = ylab or {y: str(y) for y in J.ys}
    hid = "" if shown else " h"
    mh = "" if mshown else " h"

    def mtex(m, key, v):
        if m in ("frac", "dec"):
            return frac(v) if m == "frac" else dec(v)
        t, e = m[key]
        assert eq(e, v), f"marginal {key}: shown {e}, table has {v}"
        return t

    head = f'<th class="jt-corner">${xname}\\backslash {yname}$</th>' + "".join(
        f'<th>${ylab[y]}$</th>' for y in J.ys)
    if mx is not None:
        head += f'<th class="jt-mc"><span id="{pfx}-mxh" class="jt-m{hid}">${mxh}$</span></th>'
    rows = []
    for i, x in enumerate(J.xs):
        tds = []
        for j, y in enumerate(J.ys):
            v = J(x, y)
            z = " jt-z" if v == 0 else ""
            tds.append(f'<td class="jt-c{z}"><i id="{pfx}-h-{i}-{j}" class="jt-hl h"></i>'
                       f'<i id="{pfx}-w-{i}-{j}" class="jt-hl k-w h"></i>'
                       f'<span id="{pfx}-v-{i}-{j}" class="jt-v{hid}">${_cell_tex(cells, x, y, v)}$</span></td>')
        if mx is not None:
            tds.append(f'<td class="jt-mc"><i id="{pfx}-hm-{i}" class="jt-hl k-w h"></i>'
                       f'<span id="{pfx}-mx-{i}" class="jt-m{mh}">${mtex(mx, x, J.PX(x))}$</span></td>')
        rows.append(f'<tr><th class="jt-rh">${xlab[x]}$</th>{"".join(tds)}</tr>')
    if my is not None:
        tds = "".join(f'<td class="jt-mr"><i id="{pfx}-hn-{j}" class="jt-hl k-w h"></i>'
                      f'<span id="{pfx}-my-{j}" class="jt-m{mh}">${mtex(my, y, J.PY(y))}$</span></td>'
                      for j, y in enumerate(J.ys))
        corner = (f'<td class="jt-mr jt-mc"><span id="{pfx}-tot" class="jt-m{mh}">$1$</span></td>'
                  if (mx is not None and tot) else ('<td class="jt-mr jt-mc"></td>' if mx is not None else ""))
        rows.append(f'<tr><th class="jt-rh jt-mr"><span id="{pfx}-myh" class="jt-m{hid}">${myh}$</span></th>'
                    f'{tds}{corner}</tr>')
    return (f'<table class="jt-tab" id="{pfx}" dir="ltr" style="font-size:{size}px;--jt-pad:{pad}">'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>')


def ids(pfx, kind, cells):
    return [f"{pfx}-{kind}-{i}-{j}" for i, j in cells]


def all_cells(J):
    return [(i, j) for i in range(len(J.xs)) for j in range(len(J.ys))]


def pos(J, x, y):
    return (J.xs.index(x), J.ys.index(y))


def cards(pfx, items, size=28, reveal=1, shown=False, minw=0, maxw=1040):
    """items: [[tex line, ...], ...] one card per outcome. Line 0 (the outcome) is always drawn with the card;
    lines r >= reveal start hidden ({pfx}-l-k-r). Cards start hidden unless shown."""
    out = []
    for k, lines in enumerate(items):
        ls = "".join(f'<div id="{pfx}-l-{k}-{r}" class="jt-cl{" h" if r >= reveal else ""}">{t}</div>'
                     for r, t in enumerate(lines))
        mw = f";min-width:{minw}px" if minw else ""
        out.append(f'<div id="{pfx}-o-{k}" class="jt-card{"" if shown else " h"}" style="font-size:{size}px{mw}">'
                   f'<i id="{pfx}-oh-{k}" class="jt-hl h"></i><i id="{pfx}-ow-{k}" class="jt-hl k-w h"></i>{ls}</div>')
    return f'<div class="jt-cards" id="{pfx}" style="max-width:{maxw}px">{"".join(out)}</div>'


def eqs(pfx, lines, size=36, gap=10, shown=0):
    rows = "".join(f'<div id="{pfx}-{i}" class="jt-eq{"" if i < shown else " h"}">{s}</div>' for i, s in enumerate(lines))
    return f'<div class="jt-eqs" style="font-size:{size}px;gap:{gap}px">{rows}</div>'


def chip(id_, html_, kind="ok", hidden=True):
    return f'<div id="{id_}" class="jt-chip {kind}{" h" if hidden else ""}">{html_}</div>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


def box(id_, html_, size=32, hidden=True):
    return f'<div id="{id_}" class="jt-box{" h" if hidden else ""}" style="font-size:{size}px">{html_}</div>'
