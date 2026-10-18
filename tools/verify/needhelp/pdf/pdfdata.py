# -*- coding: utf-8 -*-
"""Shared data for the guided course `pdf` ("continuous random variable: density, CDF, parameters").

ONE source for check.py (exact sympy + Monte Carlo) and figs.py (the matplotlib figures), so a figure can never
disagree with the key. A pdf is a list of pieces (lo, hi, expr) in the symbol x; lo/hi may be +-oo; outside the
pieces the density is 0.  Output is ASCII only.
"""
import sympy as sp

x, t = sp.symbols("x t", real=True)
R = sp.Rational
oo = sp.oo

PDFS = {
    # L1 lesson figure / drill: f = 2x on [0,1]
    "tri": [(0, 1, 2 * x)],
    # L1 drill: f = 3x^2 on [0,1]
    "cubic": [(0, 1, 3 * x**2)],
    # master pdf of levels 5-7: rises as x on [0,1], then flat 1/2 on [1,2]
    "P1": [(0, 1, x), (1, 2, R(1, 2))],
    # second pdf of levels 5-6: 2/3 on [0,1], 1/3 on [1,2]
    "P2": [(0, 1, R(2, 3)), (1, 2, R(1, 3))],
    # F(t)=t^3 on [0,1]  =>  f = 3x^2   (level 5, f = F')
    # symmetric tent on [-1,1] (level 7)
    "S": [(-1, 0, 1 + x), (0, 1, 1 - x)],
    # level 8 figure A: trapezoid, rises 0 -> c on [0,1], flat c on [1,3]; area 5c/2 = 1  => c = 2/5
    "trap": [(0, 1, R(2, 5) * x), (1, 3, R(2, 5))],
    # level 8 figure B: tent with apex (1, 2/3) on [0,3]; area 3h/2 = 1 => h = 2/3
    "tent": [(0, 1, R(2, 3) * x), (1, 3, R(1, 3) * (3 - x))],
    # level 2 / 3 solved densities (so the sim buttons show the pdf WITH the solved constant)
    "L2a": [(0, 2, x / 2)],
    "L2b": [(0, 3, x**2 / 9)],
    "L2c": [(-1, 1, R(3, 4) * (1 - x**2))],
    "L3a": [(0, 1, R(1, 3)), (1, 2, R(2, 3))],
    "L3b": [(0, 1, R(2, 3) * x), (1, 2, R(2, 3))],
    "L4a": [(0, 1, R(1, 3)), (1, 2, R(2, 3))],  # E = 7/6  (a=1/3, b=2/3)
    "L4b": [(0, 1, R(4, 5) * x), (1, 2, R(3, 5))],  # E = 7/6  (a=4/5, b=3/5)
}


def piece_mass(p):
    lo, hi, e = p
    return sp.integrate(e, (x, lo, hi))


def total(pdf):
    return sp.simplify(sum(piece_mass(p) for p in pdf))


def mean(pdf):
    return sp.simplify(sum(sp.integrate(x * e, (x, lo, hi)) for lo, hi, e in pdf))


def cdf_at(pdf, tt):
    """F(tt) exactly."""
    tot = 0
    for lo, hi, e in pdf:
        if tt <= lo:
            continue
        up = hi if tt >= hi else tt
        tot += sp.integrate(e, (x, lo, up))
    return sp.nsimplify(sp.simplify(tot))


def cdf_piece(pdf, k):
    """F(t) on the k-th piece as an expression in t (accumulate: F(lo_k) + int_lo^t)."""
    lo, hi, e = pdf[k]
    base = cdf_at(pdf, lo) if lo != -oo else 0
    return sp.simplify(base + sp.integrate(e.subs(x, sp.Symbol("u")), (sp.Symbol("u"), lo, t)))


def fnum(pdf):
    """numeric density"""
    import numpy as np
    fs = [(lo, hi, sp.lambdify(x, e, "numpy")) for lo, hi, e in pdf]

    def f(xs):
        xs = np.asarray(xs, dtype=float)
        out = np.zeros_like(xs)
        for lo, hi, fn in fs:
            m = (xs >= float(lo)) & (xs < float(hi)) if hi != oo else (xs >= float(lo))
            if lo == -oo:
                m = xs < float(hi)
            out[m] = fn(xs[m]) * np.ones(int(m.sum()))
        return out
    return f
