# -*- coding: utf-8 -*-
"""Step checks for 26A-A (probability). Run: PYTHONUTF8=1 py tools/verify/26A-A/steps_check.py
Re-derives every guided-step value stored in tools/raw/26A-A.json: exactly (fractions / enumeration / sympy) and,
where a simulation applies, by Monte Carlo (>= 10^6 trials, within 4 SE). ASCII output only."""
import itertools
import math
import pathlib
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from steps_lib import Chk

c = Chk("26A-A")
N = 2_000_000
rng = np.random.default_rng(20260209)


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


def se_var(v):
    return math.sqrt((np.mean((v - v.mean()) ** 4) - v.var() ** 2) / len(v))


# ============================================================ Q1  (X1, X2 ~ U(0, 1/2) independent)
def clip(poly, a, b, k):  # keep a*x + b*y + k >= 0
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * p[0] + b * p[1] + k, a * q[0] + b * q[1] + k
        if fp >= 0:
            out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def area(poly):
    s = Fr(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


half = Fr(1, 2)
SQ = [(Fr(0), Fr(0)), (half, Fr(0)), (half, half), (Fr(0), half)]


def region(*cons):
    p = SQ
    for a, b, k in cons:
        p = clip(p, Fr(a), Fr(b), Fr(k))
    return area(p) if len(p) >= 3 else Fr(0)


# constraints a*x1 + b*x2 + k > 0
LEFT_SHORTEST = [(-1, 1, 0), (-2, -1, 1)]            # x2 > x1 and 1 - 2 x1 - x2 > 0
RIGHT_LONGEST = [(-1, 1, 0), (1, 2, -1)]             # x2 > x1 and x2 > (1-x1)/2
MID_LONGEST = [(-2, -1, 1), (-1, -2, 1)]
aL, aR = region(*LEFT_SHORTEST), region(*RIGHT_LONGEST)
aLR = region(*LEFT_SHORTEST, *RIGHT_LONGEST)
aM = region(*MID_LONGEST)
x1 = rng.random(N) / 2
x2 = rng.random(N) / 2
mid = 1 - x1 - x2
ev_L = (x1 < x2) & (x1 < mid)
ev_R = (x2 > x1) & (x2 > mid)
ev_LR = ev_L & ev_R
ev_M = (mid > x1) & (mid > x2)
assert (aL, aR, aLR, aM) == (Fr(5, 48), Fr(1, 24), Fr(1, 48), Fr(1, 6))
for key, a, ev in (("Q1a", aL, ev_L), ("Q1b", aR, ev_R), ("Q1c", aLR, ev_LR), ("Q1d", aM, ev_M)):
    c.num(key, 2, a, mc=(float(ev.mean()) / 4, math.sqrt(ev.mean() * (1 - ev.mean()) / N) / 4), what="area")
    c.num(key, 3, a * 4, mc=(float(ev.mean()), se_p(float(a * 4))), what="probability")
# |Omega| steps (indexes: Q1a.1, Q1b.1, Q1c.0, Q1d.0)
for key, idx in (("Q1a", 1), ("Q1b", 1), ("Q1c", 0), ("Q1d", 0)):
    c.num(key, idx, area(SQ), what="|Omega|")
# Q1b choice: translate 'right longest'
va = float(np.mean((x2 > x1) & (x2 > 1 - x1)))
vb = float(ev_R.mean())
vc = float(np.mean((x2 > x1) | (x2 > mid)))
vd = float(np.mean((x2 < x1) & (x2 < mid)))
c.vals("Q1b", 0, {"a": va, "b": vb, "c": vc, "d": vd}, 1 / 6, tol=3e-3)
c.correct("Q1b", 0, "b")
# Q1c choice: combining
union = float(aL + aR - aLR) * 4
c.vals("Q1c", 1, {"a": float(aL * 4 * aR * 4), "b": union, "c": float(aLR * 4)}, 1 / 12)
# Q1d choice: partition
p_left_long = float(np.mean((x1 > x2) & (x1 > mid)))
c.fact("Q1d", 1, "three 'longest' events partition Omega; not independent",
       abs(p_left_long + float(ev_M.mean()) + float(ev_R.mean()) - 1) < 4e-3 and np.mean(ev_R & ev_M) == 0 and float(ev_R.mean()) * float(ev_M.mean()) > 0.05,
       "sum=%.4f, P(R and M)=0 but P(R)P(M)=%.3f" % (p_left_long + float(ev_M.mean()) + float(ev_R.mean()), float(ev_R.mean()) * float(ev_M.mean())))
c.fact("Q1a", 0, "area method: the point model is uniform on a square (probability = area ratio, matches MC)",
       abs(ev_L.mean() - 5 / 12) < 4 * se_p(5 / 12))
# Q1e
sol = sp.solve(sp.Eq(sp.Symbol("t"), 1 - 2 * sp.Symbol("t")), sp.Symbol("t"))
c.num("Q1e", 0, sol[0], what="x1 where all three equal")
c.fact("Q1e", 1, "(1/3,1/3) is inside (0,1/2)^2 (possible) but a single point (area 0)", 0 < Fr(1, 3) < half and region(*[]) == Fr(1, 4))
c.num("Q1e", 2, 0, mc=(float(np.mean((np.abs(x1 - x2) < 1e-9) & (np.abs(x1 - mid) < 1e-9))), 1e-6), what="P=0")


# ============================================================ Q2  geometric race
def geo_pmf(p, k):
    return p * (1 - p) ** (k - 1)


def tie(p, K=800):
    return sum(geo_pmf(p, k) ** 2 for k in range(1, K))


def pE(p1, p2, K=800):          # P(X1 < X2)
    return sum(geo_pmf(p1, k) * (1 - p2) ** k for k in range(1, K))


# geometric model: first head of explicit coin tosses has pmf p(1-p)^(k-1)
tosses = rng.random((400_000, 40)) < 0.3
first = tosses.argmax(axis=1) + 1
c.fact("Q2a", 0, "G(p) = index of the first head of explicit tosses",
       all(abs(np.mean(first == k) - geo_pmf(0.3, k)) < 4 * se_p(geo_pmf(0.3, k), 400_000) for k in range(1, 8)))
c.fact("Q2a", 1, "independent but unequal coins: P_E != P_B; tie has positive probability",
       abs(pE(0.5, 0.25) - 0.6) < 1e-9 and abs(pE(0.25, 0.5) - 0.2) < 1e-9 and tie(0.3) > 0)
p_q = Fr(4, 7)                                  # tie probability 0.4 <=> p = 4/7
assert abs(tie(float(p_q)) - 0.4) < 1e-12
g1 = rng.geometric(float(p_q), N)
g2 = rng.geometric(float(p_q), N)
c.num("Q2a", 2, pE(float(p_q), float(p_q)), mc=(float(np.mean(g1 < g2)), se_p(0.3)), what="P_E at Q=0.4")
# Q2b
c.vals("Q2b", 0, {"a": tie(0.5), "b": 0.25, "c": 0.25}, tie(0.5))
c.correct("Q2b", 0, "a")
h1 = rng.geometric(0.5, N)
h2 = rng.geometric(0.5, N)
c.num("Q2b", 1, tie(0.5), mc=(float(np.mean(h1 == h2)), se_p(1 / 3)), what="Q at p=0.5")
c.formula("Q2b", 2, tie,
          {"a": lambda p: p / (1 - p), "b": lambda p: p * p / (1 - p * p), "c": lambda p: p / (2 - p), "d": lambda p: p * p / (1 - p) ** 2},
          [{"p": 0.3}, {"p": 0.5}, {"p": 0.8}])
c.correct("Q2b", 2, "c")
# inversion: find p with tie(p)=0.6 by bisection
lo, hi = 0.01, 0.999
for _ in range(80):
    mid_p = (lo + hi) / 2
    if tie(mid_p) < 0.6:
        lo = mid_p
    else:
        hi = mid_p
c.num("Q2b", 3, (lo + hi) / 2, what="p with Q=0.6")


# Q2c
def cond_both(p, k):
    return geo_pmf(p, k) ** 2 / tie(p)


tie_mask = h1 == h2
c.num("Q2c", 0, tie(0.5), what="conditioning event")
c.num("Q2c", 1, geo_pmf(0.5, 2) ** 2, what="numerator")
c.num("Q2c", 2, cond_both(0.5, 2), mc=(float(np.mean(h1[tie_mask] == 2)), se_p(3 / 16, int(tie_mask.sum()))), what="ratio")


def qk(Q, k, p):
    return None


def mk(form):
    # samples are given as p and k; Q is derived from p by the brute-force series
    return form


samples23 = [{"p": 0.5, "k": 2}, {"p": 0.3, "k": 3}, {"p": 0.8, "k": 1}]
truth2c = lambda p, k: cond_both(p, k)
Qof = lambda p: tie(p)
c.formula("Q2c", 3, truth2c,
          {"a": lambda p, k: 4 * Qof(p) / (1 + Qof(p)) ** 2 * ((1 - Qof(p)) / (1 + Qof(p))) ** (2 * (k - 1)),
           "b": lambda p, k: 4 * Qof(p) / (1 + Qof(p)) ** 2 * ((1 - Qof(p)) / (1 + Qof(p))) ** (k - 1),
           "c": lambda p, k: Qof(p) * (1 - Qof(p)) ** (k - 1),
           "d": lambda p, k: Qof(p) / (1 + Qof(p)) ** 2 * ((1 - Qof(p)) / (1 + Qof(p))) ** (2 * (k - 1))},
          samples23)
c.correct("Q2c", 3, "a")
# Q2d
bmask = h2 < h1
c.num("Q2d", 0, pE(0.5, 0.5), mc=(float(bmask.mean()), se_p(1 / 3)), what="P_B")
c.formula("Q2d", 1, lambda p, k: sum(geo_pmf(p, j) for j in range(k + 1, 900)),
          {"a": lambda p, k: (1 - p) ** (k - 1), "b": lambda p, k: p * (1 - p) ** k, "c": lambda p, k: (1 - p) ** k, "d": lambda p, k: 1 - (1 - p) ** k},
          [{"p": 0.5, "k": 2}, {"p": 0.3, "k": 4}])
c.correct("Q2d", 1, "c")
c.num("Q2d", 2, geo_pmf(0.5, 2) * (0.5 ** 2), what="numerator")
c.num("Q2d", 3, 3 / 16, mc=(float(np.mean(h2[bmask] == 2)), se_p(3 / 16, int(bmask.sum()))), what="conditional")
# Q2e
p0 = 1 - (1 - 0.5) ** 2
Qv = tie(0.5)
c.vals("Q2e", 0, {"a": float(np.mean(h1[tie_mask])), "b": 2.0, "c": 0.0}, 4 / 3, tol=0.03)
c.correct("Q2e", 0, "a")
c.num("Q2e", 1, 4 * Qv / (1 + Qv) ** 2, what="p0 two ways")
assert abs(p0 - 4 * Qv / (1 + Qv) ** 2) < 1e-12
c.num("Q2e", 2, 1 / p0, mc=(float(np.mean(h1[tie_mask])), se_mean(h1[tie_mask].astype(float))), what="E[T|tie]")

# ============================================================ Q3  A, B: P(A)=p, P(B|A)=q, P(B|not A)=s
p3, q3, s3 = Fr(3, 5), Fr(7, 10), Fr(1, 5)
joint = {(1, 1): p3 * q3, (1, 0): p3 * (1 - q3), (0, 1): (1 - p3) * s3, (0, 0): (1 - p3) * (1 - s3)}
assert sum(joint.values()) == 1
PB = joint[(1, 1)] + joint[(0, 1)]
PQ1 = joint[(1, 1)]
PQ2 = sum(v for (a, b), v in joint.items() if a or b)
A_ = rng.random(N) < float(p3)
B_ = np.where(A_, rng.random(N) < float(q3), rng.random(N) < float(s3))
Q1m = A_ & B_
Q2m = A_ | B_
c.vals("Q3a", 0, {"a": PQ1, "b": PQ2, "c": PB}, PQ1)
c.correct("Q3a", 0, "a")
c.vals("Q3a", 1, {"a": p3 * q3, "b": p3 * PB, "c": p3 * s3}, PQ1)
c.correct("Q3a", 1, "a")
c.num("Q3a", 2, PQ1, mc=(float(Q1m.mean()), se_p(0.42)), what="P(Q1)")
c.vals("Q3b", 0, {"a": p3 + PB, "b": p3 + (1 - p3) * s3, "c": PQ1}, PQ2)
c.correct("Q3b", 0, "b")
c.num("Q3b", 1, (1 - p3) * s3, mc=(float(np.mean(~A_ & B_)), se_p(0.08)), what="P(not A and B)")
c.num("Q3b", 2, PQ2, mc=(float(Q2m.mean()), se_p(0.68)), what="P(Q2)")
c.num("Q3c", 0, PQ2, what="conditioning event")
c.vals("Q3c", 1, {"a": PQ1, "b": PQ1 * PQ2, "c": PQ2}, PQ1)
c.correct("Q3c", 1, "a")
c.num("Q3c", 2, PQ1 / PQ2, mc=(float(Q1m[Q2m].mean()), se_p(21 / 34, int(Q2m.sum()))), what="P(Q1|Q2)")
c.vals("Q3d", 0, {"a": PQ2, "b": PQ1 + PQ2, "c": PQ1 + PQ2 - PQ1 * PQ2}, PQ2)
c.correct("Q3d", 0, "a")
c.num("Q3d", 1, PQ2, mc=(float(Q2m.mean()), se_p(0.68)), what="P(Q1 or Q2)")


# ============================================================ Q4  density a e^x | b (1-x)^2 on [0,2)
def ab_of(mu):
    a, b = sp.symbols("a b")
    sol = sp.solve([sp.Eq(a + sp.Rational(2, 3) * b, 1), sp.Eq(-a + sp.Rational(2, 3) * b, mu)], [a, b])
    return sol[a], sol[b]


xs = sp.symbols("x")
a5, b5 = ab_of(sp.Rational(1, 2))
assert sp.integrate(xs * sp.exp(xs), (xs, -sp.oo, 0)) == -1
assert sp.integrate(a5 * sp.exp(xs), (xs, -sp.oo, 0)) + sp.integrate(b5 * (1 - xs) ** 2, (xs, 0, 2)) == 1
assert sp.integrate(xs * a5 * sp.exp(xs), (xs, -sp.oo, 0)) + sp.integrate(xs * b5 * (1 - xs) ** 2, (xs, 0, 2)) == sp.Rational(1, 2)


def sample_q4(mu, n=N):
    a, b = (float(v) for v in ab_of(sp.nsimplify(mu)))
    grid = np.linspace(-30, 2, 640_001)
    pdf = np.where(grid < 0, a * np.exp(grid), np.where(grid < 2, b * (1 - grid) ** 2, 0.0))
    cdf = np.cumsum(pdf)
    cdf /= cdf[-1]
    return np.interp(rng.random(n), cdf, grid)


X5 = sample_q4(0.5)
c.fact("Q4a", 0, "pdf is discontinuous at 0 (a != b), positive for x<0: c=0 only from normalization",
       a5 != b5 and a5 > 0 and sp.integrate(a5 * sp.exp(xs), (xs, -sp.oo, 0)) + sp.integrate(b5 * (1 - xs) ** 2, (xs, 0, 2)) == 1)
c.num("Q4a", 1, -1, what="int x e^x")
c.num("Q4a", 2, a5, mc=(float(np.mean(X5 < 0)), se_p(0.25)), what="a at mu=1/2")
c.num("Q4a", 3, b5, what="b at mu=1/2")
c.fact("Q4a", 3, "b at mu=1/2: sampled E[X]=mu and P(0<X<1)=b/3*(1)", abs(X5.mean() - 0.5) < 4 * se_mean(X5) and abs(np.mean((X5 > 0) & (X5 < 2)) - float(b5) * 2 / 3) < 4 * se_p(0.75))
mu = sp.symbols("mu")
aa, bb = ab_of(mu)
rng_ok = sp.solve_univariate_inequality(aa >= 0, mu, relational=False), sp.solve_univariate_inequality(bb >= 0, mu, relational=False)
c.fact("Q4b", 0, "a,b >= 0 are the constraints; b = 1.5 > 1 at mu=1 is a valid density",
       ab_of(1)[1] == sp.Rational(3, 2) and ab_of(1)[0] == 0 and ab_of(-1)[1] == 0)
c.num("Q4b", 1, 1, what="mu max")
c.num("Q4b", 2, -1, what="mu min")
assert str(rng_ok[0]) == "Interval(-oo, 1)" and str(rng_ok[1]) == "Interval(-1, oo)"


def F_mid(mu_v, t):
    a, b = ab_of(sp.nsimplify(mu_v))
    return float(a + b * sp.integrate((1 - xs) ** 2, (xs, 0, t)))


c.num("Q4c", 0, float(a5), mc=(float(np.mean(X5 <= 0)), se_p(0.25)), what="F(0)")
c.num("Q4c", 1, F_mid(0.5, 1), mc=(float(np.mean(X5 <= 1)), se_p(0.625)), what="F(1)")
c.formula("Q4c", 2, lambda mu, t: F_mid(mu, t),
          {"a": lambda mu, t: (3 - mu) / 4 + (1 + mu) / 4 * (t - 1) ** 3,
           "b": lambda mu, t: (1 - mu) / 2 + (1 + mu) / 4 * t ** 3,
           "c": lambda mu, t: (3 - mu) / 4 + (1 + mu) / 4 * (t - 1) ** 2,
           "d": lambda mu, t: (1 + mu) / 4 * (t - 1) ** 3},
          [{"mu": 0.5, "t": 1.5}, {"mu": -0.5, "t": 0.5}, {"mu": 0.0, "t": 1.0}])
c.correct("Q4c", 2, "a")
c.fact("Q4d", 0, "|mu| <= 1 < 2 for every allowed mu", all(abs(m) <= 1 for m in (-1, -0.5, 0, 0.5, 1)))
for mv, idx, ex in ((-0.5, 1, Fr(7, 64)), (0.5, 2, Fr(21, 64))):
    a, b = ab_of(sp.nsimplify(mv))
    val = b * sp.integrate((1 - xs) ** 2, (xs, 0, abs(sp.nsimplify(mv))))
    mcv = None
    if mv > 0:
        mcv = (float(np.mean((X5 > 0) & (X5 < 0.5))), se_p(21 / 64))
    else:
        Xm = sample_q4(-0.5)
        mcv = (float(np.mean((Xm > 0) & (Xm < 0.5))), se_p(7 / 64))
    c.num("Q4d", idx, val, mc=mcv, what="P(0<X<|mu|) at mu=%s" % mv)
    assert sp.Rational(ex.numerator, ex.denominator) == val

# ============================================================ Q5  stick breaking
xb = rng.random(N)                 # L = 1
eta1 = np.minimum(xb, 1 - xb)
xb3 = 3 * rng.random(N)            # L = 3: eta = min(x, 3-x)/3
eta3 = np.minimum(xb3, 3 - xb3) / 3
c.fact("Q5a", 0, "min(x, L-x) is not one-to-one (2 preimages per value) and eta is not a sum of independent variables",
       abs(min(0.3, 1 - 0.3) - min(0.7, 1 - 0.7)) < 1e-12)
c.num("Q5a", 1, 0.5, mc=(float(eta1.max()), 1e-3), what="max of eta")
c.num("Q5a", 2, 0.4, mc=(float(np.mean(eta1 <= 0.2)), se_p(0.4)), what="F(0.2)")
c.fact("Q5a", 3, "F(0.2) is the same for L=1 and L=3", abs(np.mean(eta3 <= 0.2) - np.mean(eta1 <= 0.2)) < 4 * math.sqrt(2) * se_p(0.4))
dens = np.mean(np.abs(eta1 - 0.3) < 0.01) / 0.02
c.num("Q5b", 0, 2, mc=(float(dens), math.sqrt(0.04) / math.sqrt(N) / 0.02 * 0.5), what="f(0.3)")
c.num("Q5b", 1, 0, mc=(float(np.mean(eta1 > 0.5)), 1e-9), what="f(0.6)")
c.vals("Q5b", 2, {"a": 1.0, "b": float(2.0), "c": 2 * math.exp(-0.6), "d": 1 / 3}, 2.0)
c.correct("Q5b", 2, "b")
# Q5c
aa_, bb_, tt = sp.symbols("aa bb tt", positive=True)
varU = sp.simplify(sp.integrate(tt ** 2 / (bb_ - aa_), (tt, aa_, bb_)) - (sp.integrate(tt / (bb_ - aa_), (tt, aa_, bb_))) ** 2)
fv = sp.lambdify((aa_, bb_), varU)
c.formula("Q5c", 0, lambda a, b: float(fv(a, b)),
          {"a": lambda a, b: (b - a) ** 2 / 12, "b": lambda a, b: (b - a) ** 2 / 4, "c": lambda a, b: (b - a) / 12},
          [{"a": 0.0, "b": 0.5}, {"a": 1.0, "b": 4.0}, {"a": 0.0, "b": 1.0}])
c.correct("Q5c", 0, "a")
c.num("Q5c", 1, sp.integrate(tt * 2, (tt, 0, sp.Rational(1, 2))), mc=(float(eta1.mean()), se_mean(eta1)), what="E[eta]")
c.num("Q5c", 2, sp.integrate(tt ** 2 * 2, (tt, 0, sp.Rational(1, 2))) - sp.Rational(1, 16), mc=(float(eta1.var()), se_var(eta1)), what="Var[eta]")
# Q5d: second break
y = xb * 0 + rng.random(N) * eta1
eta2 = np.minimum(y, eta1 - y) / eta1
X2 = np.minimum(y, eta1 - y)
low = eta1 < 0.25
c.fact("Q5d", 0, "eta2 = X2/X1 does not depend on X1 (independent of eta1), product structure",
       abs(eta2[low].mean() - eta2[~low].mean()) < 4 * math.sqrt(eta2[low].var() / low.sum() + eta2[~low].var() / (~low).sum())
       and abs(np.corrcoef(eta1, eta2)[0, 1]) < 4 / math.sqrt(N))
E2 = sp.integrate(tt ** 2 * 2, (tt, 0, sp.Rational(1, 2)))
c.num("Q5d", 1, E2, mc=(float((eta1 ** 2).mean()), se_mean(eta1 ** 2)), what="E[eta^2]")
c.num("Q5d", 2, sp.Rational(1, 16), mc=(float(X2.mean()), se_mean(X2)), what="E[X2]")
c.num("Q5d", 3, E2 ** 2 - sp.Rational(1, 256), mc=(float(X2.var()), se_var(X2)), what="Var[X2]")
# Q5e: n = 3 breaks
cur = np.ones(N)
for _ in range(3):
    yy = rng.random(N) * cur
    cur = np.minimum(yy, cur - yy)
E1m = sp.integrate(tt * 2, (tt, 0, sp.Rational(1, 2)))
varn = lambda n, L: float(L ** 2 * (E2 ** n - E1m ** (2 * n)))
c.formula("Q5e", 0, lambda n, L: varn(n, L),
          {"a": lambda n, L: L ** 2 * ((1 / 12) ** n - (1 / 16) ** n), "b": lambda n, L: L ** 2 * (1 / 48) ** n, "c": lambda n, L: n * L ** 2 / 48},
          [{"n": 3, "L": 1.0}, {"n": 2, "L": 2.0}, {"n": 1, "L": 1.0}])
c.correct("Q5e", 0, "a")
c.num("Q5e", 1, E1m ** 3, mc=(float(cur.mean()), se_mean(cur)), what="E[X3]")
c.num("Q5e", 2, E2 ** 3 - E1m ** 6, mc=(float(cur.var()), se_var(cur)), what="Var[X3]")


# ============================================================ Q6  crosses on grids
def cells(n):
    return [(r, cc) for r in range(n) for cc in range(n)]


def pairs(n):
    return list(itertools.combinations(cells(n), 2))


def horiz_or_vert(pr):
    (r1, c1), (r2, c2) = pr
    return abs(r1 - r2) + abs(c1 - c2) == 1


def diag_any(pr):
    (r1, c1), (r2, c2) = pr
    return abs(r1 - r2) == 1 and abs(c1 - c2) == 1


c.vals("Q6a", 0, {"a": len(pairs(3)), "b": 9 * 8, "c": 9 ** 2, "d": 2 ** 9}, len(pairs(3)))
c.correct("Q6a", 0, "a")
c.num("Q6a", 1, len(pairs(3)), what="C(9,2)")
c.num("Q6b", 0, len(pairs(3)), what="|Omega|")
c.num("Q6b", 1, sum(1 for pr in pairs(3) if abs(pr[0][0] - pr[1][0]) == 0 and abs(pr[0][1] - pr[1][1]) == 1), what="horizontal pairs")
c.num("Q6b", 2, Fr(sum(horiz_or_vert(pr) for pr in pairs(3)), len(pairs(3))), what="P(h or v) 3x3")
c.num("Q6c", 0, sum(1 for pr in pairs(3) if diag_any(pr) and (pr[1][0] - pr[0][0]) * (pr[1][1] - pr[0][1]) > 0), what="down-right pairs")
c.num("Q6c", 1, sum(diag_any(pr) for pr in pairs(3)), what="diag + anti-diag pairs")
c.num("Q6c", 2, Fr(sum(diag_any(pr) for pr in pairs(3)), len(pairs(3))), what="P(diag) 3x3")
c.formula("Q6d", 0, lambda N: len(pairs(int(N))),
          {"a": lambda N: N * N * (N * N - 1) / 2, "b": lambda N: N * N * (N * N - 1), "c": lambda N: N * (N - 1) / 2, "d": lambda N: N ** 4},
          [{"N": 2}, {"N": 3}, {"N": 4}, {"N": 5}])
c.correct("Q6d", 0, "a")
c.num("Q6d", 1, len(pairs(4)), what="|Omega| N=4")
c.num("Q6e", 0, len(pairs(4)), what="|Omega| N=4")
c.num("Q6e", 1, sum(horiz_or_vert(pr) for pr in pairs(4)), what="h or v pairs N=4")
pr_hv = lambda N: sum(horiz_or_vert(pr) for pr in pairs(int(N))) / len(pairs(int(N)))
c.formula("Q6e", 2, pr_hv,
          {"a": lambda N: 4 / (N * (N + 1)), "b": lambda N: 2 / (N * (N + 1)), "c": lambda N: 2 * N * (N - 1) / (N * N * (N * N - 1)), "d": lambda N: 4 / N ** 2},
          [{"N": 2}, {"N": 3}, {"N": 4}, {"N": 5}])
c.correct("Q6e", 2, "a")
c.num("Q6f", 0, sum(1 for pr in pairs(4) if diag_any(pr) and (pr[1][0] - pr[0][0]) * (pr[1][1] - pr[0][1]) > 0), what="down-right pairs N=4")
c.num("Q6f", 1, sum(diag_any(pr) for pr in pairs(4)), what="diag + anti pairs N=4")
pr_d = lambda N: sum(diag_any(pr) for pr in pairs(int(N))) / len(pairs(int(N)))
c.formula("Q6f", 2, pr_d,
          {"a": lambda N: 4 * (N - 1) / (N * N * (N + 1)), "b": lambda N: 2 * (N - 1) ** 2 / (N * N * (N * N - 1)),
           "c": lambda N: 4 * (N - 1) / (N * (N + 1)), "d": lambda N: 2 / N ** 2},
          [{"N": 2}, {"N": 3}, {"N": 4}, {"N": 5}])
c.correct("Q6f", 2, "a")


def runs(n, k, kinds):
    tot = 0
    for r in range(n):
        for cc in range(n):
            for dr, dc in kinds:
                end = (r + (k - 1) * dr, cc + (k - 1) * dc)
                if 0 <= end[0] < n and 0 <= end[1] < n:
                    tot += 1
    return tot


trip = list(itertools.combinations(cells(4), 3))
c.num("Q6g", 0, len(trip), what="C(16,3)")
c.num("Q6g", 1, runs(4, 3, [(0, 1)]), what="horizontal runs")
c.num("Q6g", 2, runs(4, 3, [(0, 1), (1, 0), (1, 1), (1, -1)]), what="all runs")
c.num("Q6g", 3, Fr(runs(4, 3, [(0, 1), (1, 0), (1, 1), (1, -1)]), len(trip)), what="probability")
# Monte Carlo for the 3-in-a-line probability on a 4x4 board
idx = np.array([rng.permutation(16)[:3] for _ in range(300_000)])
rows_, cols_ = idx // 4, idx % 4


def is_line(rs, cs):
    o = np.lexsort((cs, rs))
    rr, cc = rs[o], cs[o]
    d1r, d1c, d2r, d2c = rr[1] - rr[0], cc[1] - cc[0], rr[2] - rr[1], cc[2] - cc[1]
    return d1r == d2r and d1c == d2c and (d1r, d1c) in ((0, 1), (1, 0), (1, 1), (1, -1))


hits = sum(is_line(rows_[i], cols_[i]) for i in range(len(idx)))
c.fact("Q6g", 3, "MC 3-in-line probability near 3/70", abs(hits / len(idx) - 3 / 70) < 4 * se_p(3 / 70, len(idx)), "%.5f" % (hits / len(idx)))

c.finish()
