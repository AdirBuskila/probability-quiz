# -*- coding: utf-8 -*-
"""Step checks for 25S-C (probability). Run: PYTHONUTF8=1 py tools/verify/25S-C/steps_check.py
Re-derives every guided-step value stored in tools/raw/25S-C.json: exactly (fractions / enumeration / sympy) and,
where a simulation applies, by Monte Carlo (>= 10^6 trials, within 4 SE). ASCII output only.
(The final-answer checks of the sitting itself are in check.py.)"""
import itertools
import math
import pathlib
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from steps_lib import Chk

c = Chk("25S-C")
N = 2_000_000
rng = np.random.default_rng(20251211)


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


# ============================================================ Q1  b ~ U(0,1), L ~ U(1,2), a = (L-b)/2
b = rng.random(N)
L = 1 + rng.random(N)
a = (L - b) / 2
p_quarter = float(np.mean(a < 0.25))
c.vals("Q1a", 0, {"a": float(np.mean(L < b + 0.5)), "b": float(np.mean(L < b + 2)), "c": float(np.mean(L > b + 0.5)),
                  "d": float(np.mean(L < 2 * b + 0.5))}, p_quarter, tol=3e-3)
c.correct("Q1a", 0, "a")
c.num("Q1a", 1, 1, what="|Omega|")
c.num("Q1a", 2, sp.solve(sp.Eq(1, sp.Symbol("b") + sp.Rational(1, 2)), sp.Symbol("b"))[0], what="b where L=b+1/2 meets L=1")
c.num("Q1a", 3, Fr(1, 2) * Fr(1, 2) * Fr(1, 2), mc=(p_quarter, se_p(0.125)), what="P(a<1/4)")
p_23 = float(np.mean(a < 2 / 3))
c.vals("Q1b", 0, {"a": float(np.mean(L < b + 4 / 3)), "b": float(np.mean(L < b + 2 / 3)), "c": float(np.mean(L > b + 4 / 3)),
                  "d": float(np.mean(L < 4 * b / 3 + 1))}, p_23, tol=3e-3)
c.correct("Q1b", 0, "a")
c.num("Q1b", 1, 1, what="|Omega|")
c.num("Q1b", 2, Fr(1, 2) * Fr(2, 3) ** 2, mc=(float(np.mean(L > b + 4 / 3)), se_p(2 / 9)), what="excluded triangle")
c.num("Q1b", 3, 1 - Fr(2, 9), mc=(p_23, se_p(7 / 9)), what="P(a<2/3)")
dep = 1 + b                                              # L = 1 + b: uniform on (1,2) but dependent on b
c.vals("Q1c", 0, {"a": float(np.mean(L * b)), "b": float(np.mean(dep * b)), "c": 0.75 + 1.0}, 0.75, tol=3e-3)
c.correct("Q1c", 0, "a")
c.num("Q1c", 1, Fr(1, 2), mc=(float(a.mean()), se_mean(a)), what="E[a]")
c.num("Q1c", 2, Fr(7, 24), mc=(float((a ** 2).mean()), se_mean(a ** 2)), what="E[a^2]")
c.num("Q1c", 3, Fr(1, 24), mc=(float(a.var()), math.sqrt((np.mean((a - a.mean()) ** 4) - a.var() ** 2) / N)), what="Var[a]")
c.num("Q1d", 0, Fr(5, 24), mc=(float((a * b).mean()), se_mean(a * b)), what="E[ab]")
cv = (a - a.mean()) * (b - b.mean())
c.num("Q1d", 1, Fr(-1, 24), mc=(float(cv.mean()), se_mean(cv)), what="Cov[a,b]")
c.fact("Q1d", 2, "corr(a,b) = -0.7071 (correlated)", abs(np.corrcoef(a, b)[0, 1] + 1 / math.sqrt(2)) < 0.002)

# ============================================================ Q2  two distinct digits, ordered
pairs = [(x, y) for x in range(1, 10) for y in range(1, 10) if x != y]
tot = len(pairs)
frac = lambda f: Fr(sum(1 for x, y in pairs if f(x, y)), tot)
dis = lambda rule, truth: sum(1 for x, y in pairs if bool(rule(x, y)) != bool(truth(x, y)))
c.vals("Q2a", 0, {"a": tot, "b": 81, "c": 36}, 72)
c.correct("Q2a", 0, "a")
c.num("Q2a", 1, tot, what="|Omega|")
c.num("Q2a", 2, sum(1 for x, y in pairs if y % 2), what="odd numbers")
d1 = rng.integers(1, 10, N)
d2 = rng.integers(1, 9, N)
d2 = np.where(d2 >= d1, d2 + 1, d2)
c.num("Q2a", 3, frac(lambda x, y: y % 2 == 1), mc=(float(np.mean(d2 % 2 == 1)), se_p(5 / 9)), what="P(odd)")
div3 = lambda x, y: (10 * x + y) % 3 == 0
c.vals("Q2b", 0, {"a": dis(lambda x, y: (x + y) % 3 == 0, div3), "b": dis(lambda x, y: y % 3 == 0, div3), "c": dis(lambda x, y: x % 3 == 0, div3)}, 0)
c.correct("Q2b", 0, "a")
c.num("Q2b", 1, sum(1 for x, y in pairs if x % 3 == 0 and y % 3 == 0), what="both remainder 0")
c.num("Q2b", 2, sum(1 for x, y in pairs if {x % 3, y % 3} == {1, 2}), what="remainders 1 and 2")
c.num("Q2b", 3, frac(lambda x, y: div3(x, y)), mc=(float(np.mean((10 * d1 + d2) % 3 == 0)), se_p(1 / 3)), what="P(div by 3)")
div5 = lambda x, y: (10 * x + y) % 5 == 0
c.vals("Q2c", 0, {"a": dis(lambda x, y: y == 5, div5), "b": dis(lambda x, y: x == 5 or y == 5, div5), "c": dis(lambda x, y: (x + y) % 5 == 0, div5)}, 0)
c.correct("Q2c", 0, "a")
c.num("Q2c", 1, sum(1 for x, y in pairs if y == 5), what="units digit 5")
c.num("Q2c", 2, frac(div5), mc=(float(np.mean((10 * d1 + d2) % 5 == 0)), se_p(1 / 9)), what="P(div by 5)")
even = lambda x, y: (x + y) % 2 == 0
c.vals("Q2d", 0, {"a": dis(lambda x, y: x % 2 == y % 2, even), "b": dis(lambda x, y: x % 2 == 1 and y % 2 == 1, even), "c": dis(lambda x, y: x % 2 == 0, even)}, 0)
c.correct("Q2d", 0, "a")
ev_ = (d1 + d2) % 2 == 0
c.num("Q2d", 1, frac(even), mc=(float(ev_.mean()), se_p(4 / 9)), what="P(sum even)")
c.num("Q2d", 2, frac(lambda x, y: even(x, y) and y % 2 == 1), mc=(float(np.mean(ev_ & (d2 % 2 == 1))), se_p(5 / 18)), what="P(odd and sum even)")
c.num("Q2d", 3, frac(lambda x, y: even(x, y) and y % 2 == 1) / frac(even), mc=(float((d2 % 2 == 1)[ev_].mean()), se_p(5 / 8, int(ev_.sum()))), what="P(odd|sum even)")

# ============================================================ Q3  Bernoulli matrix, p = 0.3
pv = Fr(3, 10)


def matrix(x, y):
    return np.array([[x * y, -x], [y, x + y - x * y]], dtype=float)


def DT(x, y):
    m = matrix(x, y)
    return round(float(np.linalg.det(m))), int(round(float(np.trace(m))))


pmf = {}
for x, y in itertools.product((0, 1), repeat=2):
    w = (pv if x else 1 - pv) * (pv if y else 1 - pv)
    pmf[DT(x, y)] = pmf.get(DT(x, y), Fr(0)) + w
Xb = rng.random(N) < 0.3
Yb = rng.random(N) < 0.3
Dm = 2 * (Xb & Yb).astype(int)
Tm = Xb.astype(int) + Yb.astype(int)
c.fact("Q3a", 0, "4 outcomes of (X,Y); X^2=X so D = 2XY = det of the printed matrix and T = X + Y",
       all(DT(x, y) == (2 * x * y, x + y) for x, y in itertools.product((0, 1), repeat=2)))
c.num("Q3a", 1, DT(1, 1)[0], what="det at (1,1)")
c.num("Q3a", 2, DT(1, 0)[1], what="trace at (1,0)")
c.num("Q3a", 3, pmf[(0, 1)], mc=(float(np.mean((Dm == 0) & (Tm == 1))), se_p(0.42)), what="P(D=0,T=1)")
pD1 = sum(v for (d, t), v in pmf.items() if d == 1)
c.vals("Q3b", 0, {"a": pD1, "b": Fr(21, 50), "c": Fr(3, 10)}, pD1)
c.correct("Q3b", 0, "a")
c.num("Q3b", 1, sum(v for (d, t), v in pmf.items() if d == 2), mc=(float(np.mean(Dm == 2)), se_p(0.09)), what="P(D=2)")
c.num("Q3b", 2, sum(v for (d, t), v in pmf.items() if d == 0), mc=(float(np.mean(Dm == 0)), se_p(0.91)), what="P(D=0)")
pT1 = sum(v for (d, t), v in pmf.items() if t == 1)
c.vals("Q3c", 0, {"a": pT1, "b": Fr(3, 10), "c": 0.6 * math.exp(-0.6)}, pT1)
c.correct("Q3c", 0, "a")
c.num("Q3c", 1, pT1, mc=(float(np.mean(Tm == 1)), se_p(0.42)), what="P(T=1)")
c.num("Q3c", 2, sum(v for (d, t), v in pmf.items() if t == 2), mc=(float(np.mean(Tm == 2)), se_p(0.09)), what="P(T=2)")
c.num("Q3d", 0, pmf.get((2, 0), 0), mc=(float(np.mean((Dm == 2) & (Tm == 0))), 1e-9), what="P(D=2,T=0)")
PD2 = sum(v for (d, t), v in pmf.items() if d == 2)
PT0 = sum(v for (d, t), v in pmf.items() if t == 0)
c.num("Q3d", 1, PD2 * PT0, mc=(float(np.mean(Dm == 2) * np.mean(Tm == 0)), 4e-4), what="product of marginals")
c.fact("Q3d", 2, "joint 0 differs from product 0.0441: dependent", pmf.get((2, 0), 0) != PD2 * PT0)
ED = sum(d * v for (d, t), v in pmf.items())
ET = sum(t * v for (d, t), v in pmf.items())
EDT = sum(d * t * v for (d, t), v in pmf.items())
cvv = (Dm - Dm.mean()) * (Tm - Tm.mean())
c.num("Q3e", 0, EDT, mc=(float((Dm * Tm).mean()), se_mean((Dm * Tm).astype(float))), what="E[DT]")
c.num("Q3e", 1, ED * ET, what="E[D]E[T]")
c.num("Q3e", 2, EDT - ED * ET, mc=(float(cvv.mean()), se_mean(cvv)), what="Cov")
c.fact("Q3e", 3, "Cov = 0.252 != 0: correlated", EDT - ED * ET != 0)

# ============================================================ Q4  pdf: x/a on [0,a), 1 on [a,b]
aa, bb = sp.symbols("a b", positive=True)
x = sp.symbols("x")
norm = sp.integrate(x / aa, (x, 0, aa)) + sp.integrate(1, (x, aa, bb)) - 1
mean = sp.integrate(x * x / aa, (x, 0, aa)) + sp.integrate(x, (x, aa, bb)) - sp.Rational(23, 24)
sols = sp.solve([norm, mean], [aa, bb], dict=True)
sol_ab = sorted((s_[aa], s_[bb]) for s_ in sols)
assert sol_ab == [(1, sp.Rational(3, 2)), (11, sp.Rational(13, 2))]
c.num("Q4a", 0, sp.solve(sp.Eq(bb - sp.Rational(1, 2), 1), bb)[0], what="b from normalization, a=1")
c.num("Q4a", 1, sp.integrate(x * x, (x, 0, 1)) + sp.integrate(x, (x, 1, sp.Rational(3, 2))), what="E[X]")


def violations(av, bv):
    av, bv = sp.nsimplify(av), sp.nsimplify(bv)
    n_ = 0
    n_ += 0 if av / 2 + (bv - av) == 1 else 1
    n_ += 0 if bv ** 2 / 2 - av ** 2 / 6 == sp.Rational(23, 24) else 1
    n_ += 0 if av < bv else 1
    return n_


c.vals("Q4a", 2, {"a": violations(1, sp.Rational(3, 2)), "b": violations(11, sp.Rational(13, 2)), "c": violations(2, sp.Rational(5, 2))}, 0)
c.correct("Q4a", 2, "a")
# sample X: x on [0,1) (mass 1/2), 1 on [1,3/2] (mass 1/2)
half = rng.random(N) < 0.5
X = np.where(half, np.sqrt(rng.random(N)), 1 + rng.random(N) / 2)
assert abs(X.mean() - 23 / 24) < 4 * se_mean(X)


def Fpdf(t):
    return float(sp.integrate(x, (x, 0, min(t, 1))) + (sp.integrate(1, (x, 1, t)) if t > 1 else 0))


c.num("Q4b", 0, Fpdf(1), mc=(float(np.mean(X <= 1)), se_p(0.5)), what="F(1)")
c.formula("Q4b", 1, lambda t: Fpdf(t),
          {"a": lambda t: t - 0.5, "b": lambda t: t * t / 2, "c": lambda t: t - 1, "d": lambda t: t * t / 2 + 0.5},
          [{"t": 1.2}, {"t": 1.4}])
c.correct("Q4b", 1, "a")
c.num("Q4b", 2, Fpdf(1.25), mc=(float(np.mean(X <= 1.25)), se_p(0.75)), what="F(5/4)")
ev = X > 0.5
c.num("Q4c", 0, 1 - Fpdf(0.5), mc=(float(ev.mean()), se_p(7 / 8)), what="P(X>1/2)")
c.num("Q4c", 1, Fpdf(1.25) - Fpdf(0.5), mc=(float(np.mean((X > 0.5) & (X <= 1.25))), se_p(5 / 8)), what="P(1/2<X<=5/4)")
c.num("Q4c", 2, (Fpdf(1.25) - Fpdf(0.5)) / (1 - Fpdf(0.5)), mc=(float(np.mean(X[ev] <= 1.25)), se_p(5 / 7, int(ev.sum()))), what="conditional")

# ============================================================ Q5  circuits at p = 0.6 (path sets from the caption)
BRIDGE_PATHS = [("A", "B"), ("C", "D"), ("A", "E", "D"), ("C", "E", "B")]
Q2_PATHS = [(u, v) for u in "AB" for v in "CDE"]


def works(paths, st):
    return any(all(st[k] for k in path) for path in paths)


def prob(pp, f, given=None):
    num_, den_ = 0.0, 0.0
    for bits in itertools.product((0, 1), repeat=5):
        st = dict(zip("ABCDE", bits))
        w = 1.0
        for bit in bits:
            w *= pp if bit else 1 - pp
        if given is None or given(st):
            den_ += w
            if f(st):
                num_ += w
    return num_ / den_


pp = 0.6
q1 = lambda st: works(BRIDGE_PATHS, st)
q2 = lambda st: works(Q2_PATHS, st)
P1, P2 = prob(pp, q1), prob(pp, q2)
P12 = prob(pp, lambda st: q1(st) and q2(st))
st = rng.random((N, 5)) < pp
A_, B_, C_, D_, E_ = (st[:, i] for i in range(5))
q1m = (A_ & B_) | (C_ & D_) | (A_ & E_ & D_) | (C_ & E_ & B_)
q2m = (A_ | B_) & (C_ | D_ | E_)
binom_ge3 = sum(math.comb(5, k) * pp ** k * (1 - pp) ** (5 - k) for k in range(3, 6))
c.vals("Q5a", 0, {"a": P1, "b": 2 * pp ** 2 - pp ** 4, "c": binom_ge3}, float(q1m.mean()), tol=3e-3)
c.correct("Q5a", 0, "a")
c.num("Q5a", 1, prob(pp, q1, given=lambda s: s["E"]), mc=(float(q1m[E_].mean()), se_p(0.7056, int(E_.sum()))), what="P(Q1 | E works)")
c.num("Q5a", 2, prob(pp, q1, given=lambda s: not s["E"]), mc=(float(q1m[~E_].mean()), se_p(0.5904, int((~E_).sum()))), what="P(Q1 | E fails)")
c.num("Q5a", 3, P1, mc=(float(q1m.mean()), se_p(P1)), what="P(Q1)")
alt_b = prob(pp, lambda s: (s["A"] and s["B"]) or (s["C"] and s["D"] and s["E"]))
alt_c = prob(pp, lambda s: (s["A"] or s["B"]) and s["C"] and (s["D"] or s["E"]))
c.vals("Q5b", 0, {"a": prob(pp, lambda s: (s["A"] or s["B"]) and (s["C"] or s["D"] or s["E"])), "b": alt_b, "c": alt_c}, P2)
c.correct("Q5b", 0, "a")
c.num("Q5b", 1, prob(pp, lambda s: s["A"] or s["B"]), mc=(float((A_ | B_).mean()), se_p(0.84)), what="P(A or B)")
c.num("Q5b", 2, prob(pp, lambda s: s["C"] or s["D"] or s["E"]), mc=(float((C_ | D_ | E_).mean()), se_p(0.936)), what="P(C or D or E)")
c.num("Q5b", 3, P2, mc=(float(q2m.mean()), se_p(P2)), what="P(Q2)")
c.num("Q5c", 0, P2, what="conditioning event")
c.fact("Q5c", 1, "P(Q1 | A,B work) = 1", prob(pp, q1, given=lambda s: s["A"] and s["B"]) == 1.0)
c.num("Q5c", 2, P12, mc=(float((q1m & q2m).mean()), se_p(P12)), what="P(Q1 and Q2)")
c.num("Q5c", 3, P12 / P2, mc=(float(q1m[q2m].mean()), se_p(P12 / P2, int(q2m.sum()))), what="P(Q1|Q2)")

# ============================================================ Q6  families of sizes 2, 5, 9
sizes = np.array([2, 5, 9])
fam = rng.integers(0, 3, N)
Xv = sizes[fam]
person = rng.integers(0, sizes.sum(), N)
Yv = sizes[np.searchsorted(np.cumsum(sizes), person, side="right")]
c.vals("Q6a", 0, {"a": Fr(16, 3), "b": Fr(110, 16), "c": 2}, float(Xv.mean()), tol=3e-3)
c.correct("Q6a", 0, "a")
c.num("Q6a", 1, sizes.sum(), what="sum of sizes")
c.num("Q6a", 2, Fr(int(sizes.sum()), 3), mc=(float(Xv.mean()), se_mean(Xv.astype(float))), what="E[X]")
c.vals("Q6b", 0, {"a": Fr(9, 16), "b": Fr(1, 3), "c": 3}, float(np.mean(Yv == 9)), tol=3e-3)
c.correct("Q6b", 0, "a")
c.num("Q6b", 1, Fr(9, 16), mc=(float(np.mean(Yv == 9)), se_p(9 / 16)), what="P(Y=9)")
c.num("Q6b", 2, Fr(110, 16), mc=(float(Yv.mean()), se_mean(Yv.astype(float))), what="E[Y]")
EX, EY = Fr(16, 3), Fr(110, 16)
VX = Fr(int((sizes ** 2).sum()), 3) - EX ** 2
c.num("Q6c", 0, VX / EX ** 2, mc=(float(Xv.var() / Xv.mean() ** 2), 0.002), what="Var[X]/E[X]^2")
c.num("Q6c", 1, EY / EX, mc=(float(Yv.mean() / Xv.mean()), 0.003), what="E[Y]/E[X]")
c.fact("Q6c", 2, "E[Y]/E[X] = 1 + Var[X]/E[X]^2 > 1 when the sizes differ",
       EY / EX == 1 + VX / EX ** 2 and EY > EX and float(Yv.mean()) > float(Xv.mean()))

c.finish()
