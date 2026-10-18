# -*- coding: utf-8 -*-
"""Step checks for 25S-B (probability). Run: PYTHONUTF8=1 py tools/verify/25S-B/steps_check.py
Re-derives every guided-step value stored in tools/raw/25S-B.json: exactly (fractions / enumeration / sympy) and,
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

c = Chk("25S-B")
N = 2_000_000
rng = np.random.default_rng(20251110)


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


# ============================================================ Q1  (alpha1, alpha2) uniform on (0, pi)^2  (scaled to the unit square)
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


UNIT = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(1), Fr(1)), (Fr(0), Fr(1))]


def region(*cons):
    p = UNIT
    for a, b, k in cons:
        p = clip(p, Fr(a), Fr(b), Fr(k))
    return area(p) if len(p) >= 3 else Fr(0)


half = Fr(1, 2)
A_CON = [(-2, 1, 0)]                                   # u2 > 2 u1
STRIP = [(-1, 1, half), (1, -1, half)]                 # |u1 - u2| < 1/2
u1 = rng.random(N)
u2 = rng.random(N)
evA = u2 > 2 * u1
evS = np.abs(u1 - u2) < 0.5
aA, aS, aAS = region(*A_CON), region(*STRIP), region(*A_CON, *STRIP)
assert (aA, aS, aAS) == (Fr(1, 4), Fr(3, 4), Fr(1, 8))
c.fact("Q1a", 0, "area method: P(alpha2>2 alpha1) = 1/4 by MC", abs(evA.mean() - 0.25) < 4 * se_p(0.25))
c.num("Q1a", 1, math.pi ** 2, what="|Omega| = pi^2")
c.num("Q1a", 2, math.pi ** 2 / 4, mc=(float(evA.mean()) * math.pi ** 2, math.pi ** 2 * se_p(0.25)), what="triangle area")
c.num("Q1a", 3, aA, mc=(float(evA.mean()), se_p(0.25)), what="P")
c.vals("Q1b", 0, {"a": float(aS), "b": float(region((-1, 1, half))), "c": float(1 - aS)}, aS)
c.correct("Q1b", 0, "a")
c.num("Q1b", 1, math.pi ** 2, what="|Omega|")
c.num("Q1b", 2, math.pi ** 2 / 8, mc=(float(np.mean(u2 - u1 > 0.5)) * math.pi ** 2, math.pi ** 2 * se_p(0.125)), what="one corner triangle")
c.num("Q1b", 3, aS, mc=(float(evS.mean()), se_p(0.75)), what="P(acute)")
c.num("Q1c", 0, math.pi ** 2, what="|Omega|")
c.num("Q1c", 1, aA, mc=(float(evA.mean()), se_p(0.25)), what="conditioning event")
c.num("Q1c", 2, aAS, mc=(float(np.mean(evA & evS)), se_p(0.125)), what="intersection")
c.num("Q1c", 3, aAS / aA, mc=(float(evS[evA].mean()), se_p(0.5, int(evA.sum()))), what="conditional")

# ============================================================ Q2  numbers 1..2N+1
nums = list(range(1, 10))                            # N = 4
c.fact("Q2a", 0, "uniform single pick: P(even) = 4/9 by MC", abs(np.mean(rng.integers(1, 10, N) % 2 == 0) - 4 / 9) < 4 * se_p(4 / 9))
c.num("Q2a", 1, len(nums), what="|Omega| N=4")
c.num("Q2a", 2, sum(1 for v in nums if v % 2 == 0), what="evens N=4")
c.formula("Q2a", 3, lambda N_: sum(1 for v in range(1, 2 * int(N_) + 2) if v % 2 == 0) / (2 * N_ + 1),
          {"a": lambda N_: N_ / (2 * N_ + 1), "b": lambda N_: N_ / (2 * N_), "c": lambda N_: (N_ + 1) / (2 * N_ + 1), "d": lambda N_: 0.5},
          [{"N_": 2}, {"N_": 4}, {"N_": 7}])
c.correct("Q2a", 3, "a")
pairs = [(x, y) for x in nums for y in nums if x != y]
tot = len(pairs)
P_ = lambda f: Fr(sum(1 for pr in pairs if f(*pr)), tot)
PD1 = P_(lambda x, y: x % 2 == 0)
PD1D2 = P_(lambda x, y: x % 2 == 0 and y % 2 == 0)
PC = P_(lambda x, y: (x + y) % 2 == 0)
PCD1 = P_(lambda x, y: (x + y) % 2 == 0 and x % 2 == 0)
a_ = rng.integers(1, 10, N)
b_ = rng.integers(1, 9, N)
b_ = np.where(b_ >= a_, b_ + 1, b_)                  # second number uniform on the other 8
Cm = (a_ + b_) % 2 == 0
D1m = a_ % 2 == 0
c.vals("Q2b", 0, {"a": PD1 * Fr(3, 8), "b": PD1 ** 2, "c": 2 * PD1}, PD1D2)
c.correct("Q2b", 0, "a")
c.num("Q2b", 1, PD1D2 / PD1, what="P(D2|D1)")
c.num("Q2b", 2, P_(lambda x, y: x % 2 == 1 and y % 2 == 1), mc=(float(np.mean((a_ % 2 == 1) & (b_ % 2 == 1))), se_p(5 / 18)), what="both odd")
c.num("Q2b", 3, PC, mc=(float(Cm.mean()), se_p(4 / 9)), what="P(sum even)")
c.num("Q2c", 0, PD1, mc=(float(D1m.mean()), se_p(4 / 9)), what="P(D1)")
c.vals("Q2c", 1, {"a": PD1D2, "b": PD1 ** 2, "c": PC}, PCD1)
c.correct("Q2c", 1, "a")
c.num("Q2c", 2, PCD1 / PD1, mc=(float(Cm[D1m].mean()), se_p(3 / 8, int(D1m.sum()))), what="P(C|D1)")

# ============================================================ Q3  Poisson thinning, lambda=2, p=0.3
Xp = rng.poisson(2.0, N)
Yp = rng.binomial(Xp, 0.3)
pois = lambda lam, k: math.exp(-lam) * lam ** k / math.factorial(k)
c.fact("Q3a", 0, "P(Y=5)>0 (unbounded support); Y is a count", pois(0.6, 5) > 0 and Yp.min() >= 0 and Yp.max() > 5)
c.num("Q3a", 1, 0, mc=(float(Yp.min()), 0.5), what="min Y")
mcY1 = float(np.mean(Yp == 1))
c.vals("Q3b", 0, {"a": pois(0.6, 1), "b": pois(2.0, 1), "c": pois(1.4, 1), "d": 2 * 0.3 * 0.7}, mcY1, tol=3e-3)
c.correct("Q3b", 0, "a")
c.num("Q3b", 1, 0.6, mc=(float(Yp.mean()), se_mean(Yp.astype(float))), what="E[Y]")
c.num("Q3b", 2, math.exp(-0.6), mc=(float(np.mean(Yp == 0)), se_p(math.exp(-0.6))), what="P(Y=0)")
c.num("Q3b", 3, pois(0.6, 1), mc=(mcY1, se_p(pois(0.6, 1))), what="P(Y=1)")
Y5 = rng.binomial(5, 0.3, N)
binom = lambda n, k, p: math.comb(n, k) * p ** k * (1 - p) ** (n - k)
c.vals("Q3c", 0, {"a": binom(5, 2, 0.3), "b": pois(1.5, 2), "c": binom(5, 2, 0.7)}, float(np.mean(Y5 == 2)), tol=3e-3)
c.correct("Q3c", 0, "a")
c.num("Q3c", 1, binom(5, 2, 0.3), mc=(float(np.mean(Y5 == 2)), se_p(0.3087)), what="P(Y=2|X=5)")
m1 = Yp == 1
num_mc = float(np.mean((Yp == 1) & (Xp == 3)))
c.num("Q3d", 0, pois(0.6, 1), mc=(mcY1, se_p(pois(0.6, 1))), what="P(Y=1)")
c.num("Q3d", 1, binom(3, 1, 0.3) * pois(2.0, 3), mc=(num_mc, se_p(0.0796)), what="numerator")
cond_mc = float(np.mean(Xp[m1] == 3))
c.num("Q3d", 2, pois(1.4, 2), mc=(cond_mc, se_p(0.2417, int(m1.sum()))), what="P(X=3|Y=1)")
c.vals("Q3d", 3, {"a": pois(1.4, 2), "b": pois(2.0, 2), "c": binom(3, 2, 0.7)}, cond_mc, tol=3e-3)
c.correct("Q3d", 3, "a")

# ============================================================ Q4  f = a + c x on (0,1]  (b = 0)
mu, a, cc, x = sp.symbols("mu a c x")
sol = sp.solve([sp.Eq(a + cc / 2, 1), sp.Eq(a / 2 + cc / 3, mu)], [a, cc])
assert sp.simplify(sol[a] - (4 - 6 * mu)) == 0 and sp.simplify(sol[cc] - (12 * mu - 6)) == 0
eps = sp.symbols("eps", positive=True)
c.fact("Q4a", 0, "int x^(-3/2) diverges at 0, while int x^(-1/2) = 2 is finite (unbounded densities are allowed)",
       sp.limit(sp.integrate(x ** sp.Rational(-3, 2), (x, eps, 1)), eps, 0) == sp.oo and sp.integrate(x ** sp.Rational(-1, 2), (x, 0, 1)) == 2)
c.num("Q4a", 1, sp.solve(sp.Eq(sp.Rational(1, 2) + cc / 2, 1), cc)[0], what="c at a=1/2")
c.num("Q4a", 2, sp.solve(sp.Eq(a + (2 - 2 * a), 0), a)[0], what="a max (f(1)=0)")


def sample_lin(av, cv, n=N):
    # density av + cv*x on (0,1): F(t) = av t + cv t^2 / 2
    u = rng.random(n)
    if abs(cv) < 1e-12:
        return u / av
    return (-av + np.sqrt(av * av + 2 * cv * u)) / cv


a4, c4 = float(sol[a].subs(mu, 0.4)), float(sol[cc].subs(mu, 0.4))
X4 = sample_lin(a4, c4)
c.fact("Q4b", 0, "c = 2-2a comes from normalization; f(1) = 0.4 != 0 at mu = 0.4",
       abs(c4 - (2 - 2 * a4)) < 1e-12 and abs(a4 + c4 - 0.4) < 1e-12 and abs(X4.mean() - 0.4) < 4 * se_mean(X4))
c.num("Q4b", 1, a4, mc=None, what="a at mu=0.4")
c.num("Q4b", 2, c4, what="c at mu=0.4")
c.fact("Q4b", 1, "MC: E[X]=0.4 and P(X<=1/2)=0.65 for (a,c)=(1.6,-1.2)", abs(np.mean(X4 <= 0.5) - 0.65) < 4 * se_p(0.65))
c.num("Q4c", 0, float(sol[a].subs(mu, 0)), what="a at mu=0")
c.num("Q4c", 1, float((sol[a] + sol[cc]).subs(mu, 0)), what="f(1) at mu=0")
c.fact("Q4c", 2, "any density on (0,1] has E[X]>0 and f(1)<0 at mu=0", float(sol[a].subs(mu, 0)) > 2 and float(sol[cc].subs(mu, 0)) < 0)
a_lo = sp.solve(sp.Eq(sol[a], 0), mu)[0]
a_hi = sp.solve(sp.Eq(sol[a], 2), mu)[0]
c.num("Q4d", 0, a_lo, what="mu at a=0")
c.num("Q4d", 1, a_hi, what="mu at a=2")
c.fact("Q4d", 2, "a = 4-6 mu is decreasing in mu, so mu is largest at the smallest a", float(sp.diff(sol[a], mu)) < 0 and a_lo > a_hi)
c.num("Q4e", 0, float(sp.integrate(sol[a].subs(mu, 0.4) + sol[cc].subs(mu, 0.4) * x, (x, 0, sp.Rational(1, 2)))), mc=(float(np.mean(X4 <= 0.5)), se_p(0.65)), what="P(X<=1/2) mu=0.4")
a3 = float(sol[a].subs(mu, sp.Rational(1, 3)))
c3 = float(sol[cc].subs(mu, sp.Rational(1, 3)))
Xe = 1 - np.sqrt(rng.random(N))                      # density 2-2x
assert abs(a3 - 2) < 1e-12 and abs(c3 + 2) < 1e-12
c.num("Q4e", 1, float(sp.integrate(2 - 2 * x, (x, 0, sp.Rational(1, 2)))), mc=(float(np.mean(Xe <= 0.5)), se_p(0.75)), what="P(X<=1/2) mu=1/3")

# ============================================================ Q5  circuits (described in words in the caption)
def paths_work(paths, st):
    return any(all(st[k] for k in path) for path in paths)


Q1P = [("D", "C"), ("D", "A", "B")]                  # D in series with ((A then B) in parallel with C)
Q2P = [("B", "D"), ("B", "A", "C")]                  # B in series with (D parallel to (A then C))


def prob(pp, f, given=None):
    num_, den_ = 0.0, 0.0
    for bits in itertools.product((0, 1), repeat=4):
        st = dict(zip("ABCD", bits))
        w = 1.0
        for b in bits:
            w *= pp if b else 1 - pp
        if given is None or given(st):
            den_ += w
            if f(st):
                num_ += w
    return num_ / den_


q1 = lambda st: paths_work(Q1P, st)
q2 = lambda st: paths_work(Q2P, st)
both = lambda st: q1(st) and q2(st)
c.vals("Q5a", 0, {"a": prob(0.5, q1),
                  "b": prob(0.5, lambda s: s["D"] and (s["A"] or s["B"]) and s["C"]),
                  "c": prob(0.5, lambda s: (s["D"] and s["A"] and s["B"]) or s["C"])}, prob(0.5, q1))
c.correct("Q5a", 0, "a")
c.num("Q5a", 1, prob(0.5, lambda s: (s["A"] and s["B"]) or s["C"]), what="P((A and B) or C) at p=.5")
c.num("Q5a", 2, prob(0.5, q1), what="P(Q1) at p=.5")
c.fact("Q5b", 0, "P(G | B fails) = 0 (Q2 is in series with B)", prob(0.4, both, given=lambda s: not s["B"]) == 0)
c.num("Q5b", 1, prob(0.4, both, given=lambda s: s["A"] and s["B"]), what="P(G|A,B) p=.4")
c.num("Q5b", 2, prob(0.4, both, given=lambda s: (not s["A"]) and s["B"]), what="P(G|not A,B) p=.4")
c.num("Q5b", 3, prob(0.4, both), what="P(G) p=.4")
c.num("Q5c", 0, prob(0.4, both), what="conditioning event")
c.fact("Q5c", 1, "all four units working implies both circuits work", prob(0.4, both, given=lambda s: all(s.values())) == 1.0)
c.num("Q5c", 2, 0.4 ** 4, what="p^4")
c.num("Q5c", 3, prob(0.4, lambda s: all(s.values()), given=both), what="P(all|G)")
# Monte Carlo for Q5 at p = 0.4 and 0.5
for pv, items in ((0.4, ("b", "c")), (0.5, ("a",))):
    st = rng.random((N, 4)) < pv
    A_, B_, C_, D_ = (st[:, i] for i in range(4))
    q1m = D_ & ((A_ & B_) | C_)
    q2m = B_ & (D_ | (A_ & C_))
    gm = q1m & q2m
    if pv == 0.4:
        c.fact("Q5b", 3, "MC P(G)=0.1024 and P(G|A,B)=0.4, P(G|not A,B)=0.16",
               abs(gm.mean() - 0.1024) < 4 * se_p(0.1024) and abs(gm[A_ & B_].mean() - 0.4) < 4 * se_p(0.4, int((A_ & B_).sum()))
               and abs(gm[~A_ & B_].mean() - 0.16) < 4 * se_p(0.16, int((~A_ & B_).sum())))
        c.fact("Q5c", 3, "MC P(all | G) = 0.25", abs((A_ & B_ & C_ & D_)[gm].mean() - 0.25) < 4 * se_p(0.25, int(gm.sum())))
    else:
        c.fact("Q5a", 2, "MC P(Q1) at p=0.5 = 0.3125", abs(q1m.mean() - 0.3125) < 4 * se_p(0.3125))

# ============================================================ Q6  two dice, N = 6
d1 = rng.integers(1, 7, N)
d2 = rng.integers(1, 7, N)
mn, mx = np.minimum(d1, d2), np.maximum(d1, d2)
ordered = [(i, j) for i in range(1, 7) for j in range(1, 7)]
Pm = lambda f: Fr(sum(1 for i, j in ordered if f(min(i, j), max(i, j))), 36)
p_2_5 = Pm(lambda k, l: k == 2 and l == 5)
c.vals("Q6a", 0, {"a": p_2_5, "b": Fr(1, math.comb(6, 2)), "c": Pm(lambda k, l: k == 2) * Pm(lambda k, l: l == 5)}, p_2_5)
c.correct("Q6a", 0, "a")
c.num("Q6a", 1, p_2_5, mc=(float(np.mean((mn == 2) & (mx == 5))), se_p(1 / 18)), what="P(min=2,max=5)")
c.num("Q6a", 2, Pm(lambda k, l: k == 3 and l == 3), mc=(float(np.mean((mn == 3) & (mx == 3))), se_p(1 / 36)), what="P(min=max=3)")
c.num("Q6a", 3, sum(1 for k in range(1, 7) for l in range(1, 7) if k < l), what="pairs k<l")
c.vals("Q6b", 0, {"a": Pm(lambda k, l: k == 2), "b": Fr(1, 6), "c": Pm(lambda k, l: k == 2) + Fr(2, 36)}, Pm(lambda k, l: k == 2))
c.correct("Q6b", 0, "a")
c.num("Q6b", 1, Pm(lambda k, l: k == 2), mc=(float(np.mean(mn == 2)), se_p(0.25)), what="P(min=2)")
c.num("Q6b", 2, Pm(lambda k, l: k == 1), mc=(float(np.mean(mn == 1)), se_p(11 / 36)), what="P(min=1)")
c.num("Q6c", 0, Pm(lambda k, l: l == 4), mc=(float(np.mean(mx == 4)), se_p(7 / 36)), what="P(max=4)")
c.vals("Q6c", 1, {"a": Pm(lambda k, l: k == 3), "b": Pm(lambda k, l: k == 4), "c": 1 - Pm(lambda k, l: k == 4)}, Pm(lambda k, l: l == 4))
c.correct("Q6c", 1, "a")
c.num("Q6c", 2, Pm(lambda k, l: l == 6), mc=(float(np.mean(mx == 6)), se_p(11 / 36)), what="P(max=6)")
c.num("Q6d", 0, Pm(lambda k, l: k == 2 and l == 1), mc=(float(np.mean((mn == 2) & (mx == 1))), 1e-9), what="P(min=2,max=1)")
c.num("Q6d", 1, Pm(lambda k, l: k == 2) * Pm(lambda k, l: l == 1), what="product of marginals")
c.fact("Q6d", 2, "joint 0 != product 1/144 > 0, so dependent", Pm(lambda k, l: k == 2 and l == 1) == 0 and Pm(lambda k, l: k == 2) * Pm(lambda k, l: l == 1) > 0)

c.finish()
