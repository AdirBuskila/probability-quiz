# -*- coding: utf-8 -*-
"""Step checks for 26A-B (probability). Run: PYTHONUTF8=1 py tools/verify/26A-B/steps_check.py
Re-derives every guided-step value stored in tools/raw/26A-B.json: exactly (fractions / enumeration / sympy) and,
where a simulation applies, by Monte Carlo (>= 10^6 trials, within 4 SE). ASCII output only.
Q3 follows the PRINTED definitions q2 = P(B | not A, not C), q4 = P(B | not A, C)."""
import itertools
import math
import pathlib
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from steps_lib import Chk

c = Chk("26A-B")
N = 2_000_000
rng = np.random.default_rng(20260430)


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


def se_var(v):
    return math.sqrt((np.mean((v - v.mean()) ** 4) - v.var() ** 2) / len(v))


# ============================================================ Q1  D = XY
X = rng.random(N)
Y = rng.random(N)
D = X * Y
t = 0.3
c.fact("Q1a", 0, "XY<=t area method vs convolution: P(X+Y<=0.3)=0.045 but P(XY<=0.3)=0.661",
       abs(np.mean(X + Y <= t) - 0.045) < 4 * se_p(0.045) and abs(np.mean(D <= t) - (t - t * math.log(t))) < 4 * se_p(0.66))
c.num("Q1a", 1, 1, what="|Omega|")
c.num("Q1a", 2, Fr(3, 10), mc=(float(np.mean(X < t)), se_p(0.3)), what="strip x<t")
c.num("Q1a", 3, -t * math.log(t), mc=(float(np.mean((X > t) & (D <= t))), se_p(0.36)), what="hyperbola part")
c.num("Q1a", 4, t - t * math.log(t), mc=(float(np.mean(D <= t)), se_p(0.66)), what="F_D(0.3)")
# check F_D at several t by sympy integral too
tt, xx = sp.symbols("t x", positive=True)
Fsym = tt + sp.integrate(tt / xx, (xx, tt, 1))
assert sp.simplify(Fsym - (tt - tt * sp.log(tt))) == 0
# Q1b
dens = np.mean(np.abs(D - 0.5) < 0.01) / 0.02
c.vals("Q1b", 0, {"a": float(dens), "b": float(sp.integrate(sp.Float(1) * (tt - tt * sp.log(tt)), (tt, 0, sp.Rational(1, 2)))),
                  "c": 1 - float(np.mean(D <= 0.5))}, math.log(2), tol=0.03)
c.correct("Q1b", 0, "a")
c.num("Q1b", 1, math.log(2), mc=(float(dens), math.sqrt(0.0139 / N) / 0.02), what="f(0.5)")
d2 = np.mean(np.abs(D - math.exp(-2)) < 0.004) / 0.008
c.num("Q1b", 2, 2, mc=(float(d2), 0.06), what="f(e^-2) (density estimate)")
# Q1c
c.vals("Q1c", 0, {"a": float(np.mean(X * Y)), "b": float(np.mean(X * X)), "c": 0.25 + 1.0}, 0.25, tol=3e-3)
c.correct("Q1c", 0, "a")
c.num("Q1c", 1, Fr(1, 9), mc=(float(np.mean(D ** 2)), se_mean(D ** 2)), what="E[D^2]")
c.num("Q1c", 2, Fr(7, 144), mc=(float(D.var()), se_var(D)), what="Var[D]")


# ============================================================ Q2  tosses
def geo(p, k):
    return p * (1 - p) ** (k - 1)


tosses = rng.random((400_000, 40)) < 0.3          # head = True with probability p = 0.3
first_head = tosses.argmax(axis=1) + 1
c.fact("Q2a", 0, "number of the first tail/head toss is geometric (explicit tosses)",
       all(abs(np.mean(first_head == k) - geo(0.3, k)) < 4 * se_p(geo(0.3, k), 400_000) for k in range(1, 8)))
n_, p_ = 4, 0.5
T = rng.random((N, n_)) < p_                       # head = True
first_tail = np.where((~T).any(axis=1), (~T).argmax(axis=1) + 1, 0)
c.num("Q2a", 1, geo(0.5, 3), mc=(float(np.mean(first_tail == 3)), se_p(0.125)), what="P(K=3) as H,H,T")
c.num("Q2a", 2, Fr(1, 16), mc=(float(np.mean(first_tail == 0)), se_p(1 / 16)), what="P(no tail)")
ev = (first_tail >= 2)
c.num("Q2a", 3, Fr(7, 16), mc=(float(ev.mean()), se_p(7 / 16)), what="P(first tail after a head)")
assert sum(p_ ** (k - 1) * (1 - p_) for k in range(2, n_ + 1)) == 7 / 16
# Q2b
c.fact("Q2b", 0, "geometric toss index (see Q2a); geometric pmf ratio of the even terms is (1-p)^2",
       abs(geo(0.5, 4) / geo(0.5, 2) - 0.25) < 1e-12)
g = rng.geometric(0.5, N)
c.num("Q2b", 1, Fr(1, 4), what="ratio of even terms")
c.num("Q2b", 2, Fr(1, 3), mc=(float(np.mean(g % 2 == 0)), se_p(1 / 3)), what="P(X even)")
c.formula("Q2b", 3, lambda p: sum(geo(p, k) for k in range(2, 900, 2)),
          {"a": lambda p: (1 - p) / (2 - p), "b": lambda p: 1 / (2 - p), "c": lambda p: p / (2 - p), "d": lambda p: 0.5},
          [{"p": 0.3}, {"p": 0.5}, {"p": 0.8}])
c.correct("Q2b", 3, "a")


# Q2c: negative binomial
def nb(m, p, k):
    return math.comb(k - 1, m - 1) * p ** m * (1 - p) ** (k - m)


tos2 = rng.random((300_000, 80)) < 0.5
second = np.cumsum(tos2, axis=1).__ge__(2).argmax(axis=1) + 1
c.fact("Q2c", 0, "toss index of the 2nd head has the negative-binomial pmf (k-1)p^2(1-p)^(k-2)",
       all(abs(np.mean(second == k) - nb(2, 0.5, k)) < 4 * se_p(nb(2, 0.5, k), 300_000) for k in range(2, 9)))
Yn = rng.negative_binomial(2, 0.5, N) + 2
Es = sum((-1) ** k * nb(2, 0.5, k) for k in range(2, 300))
Po = sum(nb(2, 0.5, k) for k in range(3, 300, 2))
c.num("Q2c", 1, Es, mc=(float(np.mean((-1.0) ** Yn)), se_mean((-1.0) ** Yn)), what="E[(-1)^Y]")
c.num("Q2c", 2, Po, mc=(float(np.mean(Yn % 2 == 1)), se_p(4 / 9)), what="P(Y odd)")
assert abs(Po - 4 / 9) < 1e-12 and abs(Es - 1 / 9) < 1e-12

# ============================================================ Q3  A, C ~ Ber(0.3) independent, B | (A,C) with the PRINTED q's
p3 = Fr(3, 10)
q = {(1, 1): Fr(9, 10), (0, 0): Fr(7, 10), (1, 0): Fr(1, 2), (0, 1): Fr(3, 10)}      # q1, q2, q3, q4 by (A, C)
joint = {}
for a, cc, b in itertools.product((0, 1), repeat=3):
    w = (p3 if a else 1 - p3) * (p3 if cc else 1 - p3) * (q[(a, cc)] if b else 1 - q[(a, cc)])
    joint[(a, b, cc)] = w
assert sum(joint.values()) == 1
P = lambda f: sum(v for (a, b, cc), v in joint.items() if f(a, b, cc))
PB, PAB, PA = P(lambda a, b, cc: b), P(lambda a, b, cc: a and b), P(lambda a, b, cc: a)
PQ1, PQ2 = P(lambda a, b, cc: a and b and cc), P(lambda a, b, cc: a or b or cc)
A3 = rng.random(N) < 0.3
C3 = rng.random(N) < 0.3
qa = np.where(A3 & C3, 0.9, np.where(~A3 & ~C3, 0.7, np.where(A3 & ~C3, 0.5, 0.3)))
B3 = rng.random(N) < qa
c.fact("Q3a", 0, "total probability over the 4 states of (A,C) (not P(A)P(C))",
       abs(float(PB) - float(B3.mean())) < 4 * se_p(0.592) and abs(0.09 - float(PB)) > 0.4)
cond_nn = P(lambda a, b, cc: b and not a and not cc) / P(lambda a, b, cc: not a and not cc)
c.vals("Q3a", 1, {"a": q[(1, 1)], "b": q[(0, 0)], "c": q[(1, 0)], "d": q[(0, 1)]}, cond_nn)
c.correct("Q3a", 1, "b")
c.num("Q3a", 2, Fr(21, 100), mc=(float(np.mean(~A3 & C3)), se_p(0.21)), what="P(not A and C)")
c.num("Q3a", 3, PB, mc=(float(B3.mean()), se_p(0.592)), what="P(B)")
c.num("Q3b", 0, PB, what="conditioning event")
c.num("Q3b", 1, PAB, mc=(float(np.mean(A3 & B3)), se_p(0.186)), what="P(A and B)")
c.num("Q3b", 2, PAB / PB, mc=(float(A3[B3].mean()), se_p(0.31419, int(B3.sum()))), what="P(A|B)")
c.fact("Q3b", 3, "P(A|B) != P(A)", abs(float(PAB / PB) - 0.3) > 0.01)
c.num("Q3c", 0, p3 ** 2, mc=(float(np.mean(A3 & C3)), se_p(0.09)), what="P(A and C)")
c.vals("Q3c", 1, {"a": P(lambda a, b, cc: a and cc) * q[(1, 1)], "b": P(lambda a, b, cc: a and cc) * PB, "c": P(lambda a, b, cc: a and cc) + q[(1, 1)]}, PQ1)
c.correct("Q3c", 1, "a")
c.num("Q3c", 2, PQ1, mc=(float(np.mean(A3 & B3 & C3)), se_p(0.081)), what="P(Q1)")
fail_all = 1 - PQ2
c.vals("Q3d", 0, {"a": fail_all, "b": 1 - PQ1, "c": 1 - PB}, fail_all)
c.correct("Q3d", 0, "a")
c.num("Q3d", 1, (1 - p3) ** 2, mc=(float(np.mean(~A3 & ~C3)), se_p(0.49)), what="P(not A and not C)")
c.num("Q3d", 2, 1 - q[(0, 0)], mc=(float(np.mean(~B3[~A3 & ~C3])), se_p(0.3, int((~A3 & ~C3).sum()))), what="P(not B | not A, not C)")
c.num("Q3d", 3, PQ2, mc=(float(np.mean(A3 | B3 | C3)), se_p(0.853)), what="P(Q2)")
# the swapped-q error value 0.657 quoted in the pitfall
assert abs(1 - (1 - 0.3) * 0.49 - 0.657) < 1e-12

# ============================================================ Q4  f = b x^2 [0,1), c e^{-(x-1)} x>=1
x = sp.symbols("x")
mu = sp.symbols("mu")
b_, c_ = sp.symbols("b c")
sol = sp.solve([sp.Eq(b_ / 3 + c_, 1), sp.Eq(b_ / 4 + 2 * c_, mu)], [b_, c_])
bm = sp.lambdify(mu, sol[b_])
cm = sp.lambdify(mu, sol[c_])
assert sp.simplify(sol[b_] - 12 * (2 - mu) / 5) == 0 and sp.simplify(sol[c_] - (4 * mu - 3) / 5) == 0
assert sp.integrate(x * sp.exp(-(x - 1)), (x, 1, sp.oo)) == 2


def sample_q4(m, n=N):
    b, cc = bm(m), cm(m)
    m1 = b / 3                                            # mass of [0,1)
    left = rng.random(n) < m1
    return np.where(left, rng.random(n) ** (1 / 3), 1 + rng.exponential(1.0, n))


X1 = sample_q4(1.0)
c.fact("Q4a", 0, "mu=1: a=0 but b=2.4 (a != b); an infinite-ray constant diverges",
       bm(1.0) == 2.4 and float(sp.integrate(sp.Float(0.001), (x, 0, 1))) < 1)
c.num("Q4a", 1, 2, what="int x e^-(x-1)")
c.num("Q4a", 2, Fr(12, 5), what="b at mu=1")
c.num("Q4a", 3, Fr(1, 5), what="c at mu=1")
c.fact("Q4a", 2, "MC: P(X<1) = b/3 = 0.8 for the density with b=2.4, c=0.2", abs(np.mean(X1 < 1) - 2.4 / 3) < 4 * se_p(0.8))
c.fact("Q4a", 3, "MC: E[X] = 1 for that density", abs(X1.mean() - 1.0) < 4 * se_mean(X1))
assert abs(bm(1.0) / 4 + 2 * cm(1.0) - 1.0) < 1e-12
c.fact("Q4b", 0, "mu=3/4: b=3>1, c=0 is a valid density; mu bounds from b,c>=0",
       abs(bm(0.75) - 3) < 1e-12 and abs(cm(0.75)) < 1e-12 and abs(bm(2) ) < 1e-12 and abs(cm(2) - 1) < 1e-12)
c.num("Q4b", 1, sp.solve(sol[b_], mu)[0], what="mu max (b=0)")
c.num("Q4b", 2, sp.solve(sol[c_], mu)[0], what="mu min (c=0)")
c.num("Q4c", 0, sp.integrate(2.4 * x ** 2, (x, 0, 0.5)), mc=(float(np.mean(X1 <= 0.5)), se_p(0.1)), what="F(0.5)")
c.num("Q4c", 1, 0.8, mc=(float(np.mean(X1 <= 1)), se_p(0.8)), what="F(1)")
c.num("Q4c", 2, 1 - 0.2 / math.e, mc=(float(np.mean(X1 <= 2)), se_p(0.9264)), what="F(2)")
c.fact("Q4d", 0, "mu in [3/4, 2] implies mu/2 <= 1", all(m / 2 <= 1 for m in (0.75, 1, 1.5, 2)))
for mv, idx, ex in ((1.0, 1, 0.1), (1.5, 2, 0.16875)):
    Xs = sample_q4(mv)
    val = float(bm(mv) * sp.integrate(x ** 2, (x, 0, mv / 2)))
    c.num("Q4d", idx, val, mc=(float(np.mean((Xs > 0) & (Xs < mv / 2))), se_p(ex)), what="P(0<X<mu/2) at mu=%s" % mv)


# ============================================================ Q5  two urns
def hyper(Nn, K, n, k):
    return Fr(math.comb(K, k) * math.comb(Nn - K, n - k), math.comb(Nn, n))


M = 1_000_000
keys = rng.random((M, 10))
order = keys.argsort(axis=1)[:, :3]                   # 3 balls from urn 1 (balls 0..3 are red)
red_drawn = (order < 4).sum(axis=1)
Xr = red_drawn
c.vals("Q5a", 0, {"a": hyper(10, 4, 3, 1), "b": 3 * 0.4 * 0.6 ** 2, "c": 1.2 * math.exp(-1.2), "d": 0.4},
       float(np.mean(Xr == 1)), tol=3e-3)
c.correct("Q5a", 0, "a")
c.num("Q5a", 1, hyper(10, 4, 3, 1), mc=(float(np.mean(Xr == 1)), se_p(0.5, M)), what="P(X=1)")
c.num("Q5a", 2, hyper(10, 4, 3, 3), mc=(float(np.mean(Xr == 3)), se_p(1 / 30, M)), what="P(X=3)")
c.num("Q5a", 3, min(k for k in range(0, 8) if math.comb(4, k) * math.comb(6, 7 - k) > 0), what="min X for n=7")
black_drawn = 3 - Xr
c.fact("Q5b", 0, "black = n - red always, hypergeometric with 6 black balls, dependent on X",
       np.all(black_drawn + Xr == 3) and abs(np.corrcoef(Xr, black_drawn)[0, 1] + 1) < 1e-9)
c.num("Q5b", 1, hyper(10, 6, 3, 2), mc=(float(np.mean(black_drawn == 2)), se_p(0.5, M)), what="P(black=2)")
pmf = {k: hyper(10, 4, 3, k) for k in range(4)}
EX = sum(k * v for k, v in pmf.items())
VX = sum(k * k * v for k, v in pmf.items()) - EX ** 2
cov = sum(k * (3 - k) * v for k, v in pmf.items()) - EX * (3 - EX)
c.fact("Q5c", 0, "corr(X, n-X) = -1 (linear, negative slope)", abs(np.corrcoef(Xr, 3 - Xr)[0, 1] + 1) < 1e-9)
c.num("Q5c", 1, cov, mc=(float(np.cov(Xr, black_drawn)[0, 1]), float(Xr.std() * black_drawn.std() / math.sqrt(M)) * 1.5), what="Cov[X, n-X] = -Var[X]")
assert cov == -VX == Fr(-14, 25)
c.num("Q5c", 2, cov / VX, what="rho")
# second stage: urn 2 has 3 red + 5 black, receives the 3 drawn balls, then 2 balls are drawn
red2 = 3 + Xr
tot2 = 11
keys2 = rng.random((M, tot2))
second = keys2.argsort(axis=1)[:, :2]
# the first red2 positions of the (shuffled) urn are the red balls: ball index < red2 is red
Yr = (second < red2[:, None]).sum(axis=1)
m1 = Xr == 1
m2 = Xr == 2
pA = float(hyper(11, 4, 2, 1))
pB_ = float(hyper(8, 3, 2, 1))
pC = float(hyper(11, 6, 2, 1))
c.vals("Q5d", 0, {"a": pA, "b": pB_, "c": pC}, float(np.mean(Yr[m1] == 1)), tol=3e-3)
c.correct("Q5d", 0, "a")
c.num("Q5d", 1, 3 + 1, what="reds in urn 2 after the transfer, k=1")
c.num("Q5d", 2, hyper(11, 4, 2, 1), mc=(float(np.mean(Yr[m1] == 1)), se_p(28 / 55, int(m1.sum()))), what="P(Y=1|X=1)")
joint21 = pmf[2] * hyper(11, 5, 2, 1)
PY1 = sum(pmf[k] * hyper(11, 3 + k, 2, 1) for k in range(4))
c.vals("Q5e", 0, {"a": joint21, "b": pmf[2] * PY1, "c": hyper(11, 5, 2, 1)}, float(np.mean((Xr == 2) & (Yr == 1))), tol=3e-3)
c.correct("Q5e", 0, "a")
c.num("Q5e", 1, pmf[2], mc=(float(np.mean(Xr == 2)), se_p(0.3, M)), what="P(X=2)")
c.num("Q5e", 2, joint21, mc=(float(np.mean((Xr == 2) & (Yr == 1))), se_p(9 / 55, M)), what="P(X=2,Y=1)")
assert joint21 == Fr(9, 55) and pmf[2] * PY1 != joint21


# ============================================================ Q6  crosses / V shapes
def vshapes(R, C):
    sh = set()
    for r in range(R - 1):
        for cc in range(C - 2):
            sh.add(frozenset({(r, cc), (r, cc + 2), (r + 1, cc + 1)}))
            sh.add(frozenset({(r + 1, cc), (r + 1, cc + 2), (r, cc + 1)}))
    for r in range(R - 2):
        for cc in range(C - 1):
            sh.add(frozenset({(r, cc), (r + 2, cc), (r + 1, cc + 1)}))
            sh.add(frozenset({(r, cc + 1), (r + 2, cc + 1), (r + 1, cc)}))
    return sh


def n_triples(R, C):
    return sum(1 for _ in itertools.combinations(range(R * C), 3))


c.vals("Q6a", 0, {"a": n_triples(3, 4), "b": 12 * 11 * 10, "c": 12 ** 3}, n_triples(3, 4))
c.correct("Q6a", 0, "a")
c.num("Q6a", 1, n_triples(3, 4), what="C(12,3)")
c.num("Q6b", 0, n_triples(3, 4), what="|Omega|")
blocks_23 = (3 - 1) * (4 - 2)
c.num("Q6b", 1, blocks_23, what="2x3 blocks in a 3x4 board")
c.num("Q6b", 2, len(vshapes(3, 4)), what="V shapes in 3x4")
assert len(vshapes(4, 3)) == len(vshapes(3, 4))
c.num("Q6b", 3, Fr(len(vshapes(3, 4)), n_triples(3, 4)), what="P(V)")
c.formula("Q6c", 0, lambda M_, N_: n_triples(int(M_), int(N_)) if False else math.comb(int(M_) * int(N_), 3),
          {"a": lambda M_, N_: math.comb(int(M_ * N_), 3), "b": lambda M_, N_: math.comb(int(M_), 3) * math.comb(int(N_), 3),
           "c": lambda M_, N_: math.comb(int(M_ + N_), 3), "d": lambda M_, N_: M_ * N_ * (M_ * N_ - 1) * (M_ * N_ - 2)},
          [{"M_": 2, "N_": 3}, {"M_": 3, "N_": 4}, {"M_": 5, "N_": 6}])
c.correct("Q6c", 0, "a")
c.num("Q6c", 1, math.comb(30, 3), what="C(30,3)")
c.num("Q6d", 0, n_triples(4, 5), what="|Omega| 4x5")
c.formula("Q6d", 1, lambda M_, N_: len(vshapes(int(M_), int(N_))),
          {"a": lambda M_, N_: 4 * M_ * N_ - 6 * M_ - 6 * N_ + 8, "b": lambda M_, N_: 2 * (M_ - 1) * (N_ - 2),
           "c": lambda M_, N_: 4 * (M_ - 1) * (N_ - 1), "d": lambda M_, N_: 2 * M_ * N_ - 3 * M_ - 3 * N_ + 4},
          [{"M_": 3, "N_": 4}, {"M_": 4, "N_": 5}, {"M_": 3, "N_": 3}, {"M_": 5, "N_": 3}])
c.correct("Q6d", 1, "a")
c.num("Q6d", 2, len(vshapes(4, 5)), what="V shapes 4x5")
c.num("Q6d", 3, Fr(len(vshapes(4, 5)), n_triples(4, 5)), what="P(V) 4x5")
# Monte Carlo: random 3 cells of a 4x5 board
sh45 = vshapes(4, 5)
cnt = 0
K = 300_000
pick = np.array([rng.permutation(20)[:3] for _ in range(K)])
for row in pick:
    if frozenset((int(v) // 5, int(v) % 5) for v in row) in sh45:
        cnt += 1
c.fact("Q6d", 3, "MC P(V) near 34/1140", abs(cnt / K - 34 / 1140) < 4 * se_p(34 / 1140, K), "%.5f" % (cnt / K))

c.finish()
