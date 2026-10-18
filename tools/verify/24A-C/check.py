# -*- coding: utf-8 -*-
"""Verification harness for 24A-C (probability). Run: PYTHONUTF8=1 py tools/verify/24A-C/check.py
Every final answer: EXACT (fractions / enumeration / sympy / quadrature) AND Monte Carlo (>=10^6 trials, 4 SE).
Symbolic answers are checked at sample parameter values. Output is ASCII only."""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20240527)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ---------------- Q1: area method, conditional on the big triangle
X = rng.random(N); Y = rng.random(N)
inT = Y <= 1 - X
nT = int(inT.sum())
rec("Q1a", "P(O in triangle)", Fr(1, 2), Fr(1, 2), float(inT.mean()), se_p(0.5))
S1, S2 = X / 2, Y / 2
S3 = 0.5 - S1 - S2


def cond(ev):
    return float((ev & inT).sum() / nT), math.sqrt(0.25 / nT)


def quad_area(f):
    return integrate.quad(f, 0, 1, points=[1 / 3, 2 / 3, 0.5], limit=200)[0]


ex_b = quad_area(lambda x: (1 - x) if x < 2 / 3 else 0) / 0.5
ex_c = quad_area(lambda x: max(0.0, (1 - x) - max(0.0, 2 / 3 - x))) / 0.5
ex_d = quad_area(lambda x: max(0.0, min(1 - x, 1 - 2 * x))) / 0.5
for item, off, ex, ev in (("Q1b", Fr(8, 9), ex_b, S1 < 1 / 3), ("Q1c", Fr(5, 9), ex_c, S1 + S2 > 1 / 3),
                          ("Q1d", Fr(1, 2), ex_d, S3 > S1)):
    m, se = cond(ev)
    rec(item, "conditional area", off, ex, m, se, tol=1e-9)

# ---------------- Q2: unbalanced die
q = Fr(1, 9)
pm = {1: q, 3: q, 5: q, 2: 2 * q, 4: 2 * q, 6: 2 * q}
rows.append(("Q2a", "3q+6q=1 -> q=1/9", sum(pm.values()) == 1, True, ""))
faces = np.array(list(pm.keys())); pr = np.array([float(pm[f]) for f in faces])


def roll(shape):
    return rng.choice(faces, size=shape, p=pr)


def pe(n, ev):
    return sum(math.prod(pm[f] for f in s) for s in itertools.product(pm, repeat=n) if ev(s))


R2 = roll((N, 2)); R3 = roll((N, 3))
rec("Q2b", "P(sum2=5)", Fr(8, 81), pe(2, lambda s: sum(s) == 5), float((R2.sum(1) == 5).mean()), se_p(8 / 81))
rec("Q2c", "P(sum3=5)", Fr(5, 243), pe(3, lambda s: sum(s) == 5), float((R3.sum(1) == 5).mean()), se_p(5 / 243))
c = (R3[:, 0] + R3[:, 1] == 2)
rec("Q2d", "P(sum3=5 | s2=2)", Fr(1, 9), pe(3, lambda s: sum(s) == 5 and s[0] + s[1] == 2) / pe(3, lambda s: s[0] + s[1] == 2),
    float(((R3.sum(1) == 5) & c).sum() / c.sum()), math.sqrt(0.1 / c.sum()))
d = R3[:, 0] < R3[:, 1]
rec("Q2e", "P(sum3=5 | first<second)", Fr(5, 297),
    pe(3, lambda s: sum(s) == 5 and s[0] < s[1]) / pe(3, lambda s: s[0] < s[1]),
    float(((R3.sum(1) == 5) & d).sum() / d.sum()), math.sqrt(0.02 / d.sum()))
rows.append(("Q2e", "P(D)=33q^2 and P(B^D)=5q^3",
             pe(3, lambda s: s[0] < s[1]) == 33 * q ** 2 and pe(3, lambda s: sum(s) == 5 and s[0] < s[1]) == 5 * q ** 3, True, ""))

# ---------------- Q3: Bernoulli matrix
for p, qq in ((Fr(3, 10), Fr(1, 2)), (Fr(2, 5), Fr(7, 10)), (Fr(1, 4), Fr(1, 3))):
    joint = {}
    for x_, y_ in itertools.product((0, 1), repeat=2):
        M = sp.Matrix([[-1, -x_ ** 2], [y_ ** 2, x_ + y_]])
        key = (int(M.det()), int(M.trace()))
        joint[key] = joint.get(key, Fr(0)) + (p if x_ else 1 - p) * (qq if y_ else 1 - qq)
    off = {(-1, 0): p + qq - 2 * p * qq, (-1, 1): p * qq, (0, -1): (1 - p) * (1 - qq),
           (-1, -1): Fr(0), (0, 0): Fr(0), (0, 1): Fr(0)}
    Xs = rng.random(N) < float(p); Ys = rng.random(N) < float(qq)
    Dm = (Xs * Ys).astype(int) - Xs - Ys; Tm = Xs.astype(int) + Ys - 1
    for k, v in off.items():
        rec("Q3a", "p(D=%d,T=%d) p=%s q=%s" % (k + (p, qq)), v, joint.get(k, Fr(0)),
            float(((Dm == k[0]) & (Tm == k[1])).mean()), max(se_p(float(v)), 1e-9))
    ED = sum(k[0] * v for k, v in joint.items()); ET = sum(k[1] * v for k, v in joint.items())
    VD = sum(k[0] ** 2 * v for k, v in joint.items()) - ED ** 2
    VT = sum(k[1] ** 2 * v for k, v in joint.items()) - ET ** 2
    cov = sum(k[0] * k[1] * v for k, v in joint.items()) - ED * ET
    rec("Q3b", "E[D] p=%s q=%s" % (p, qq), p * qq - p - qq, ED, float(Dm.mean()), float(Dm.std() / math.sqrt(N)))
    rec("Q3b", "Var[D]", p + qq - p * qq - (p + qq - p * qq) ** 2, VD, float(Dm.var()),
        math.sqrt((np.mean((Dm - Dm.mean()) ** 4) - Dm.var() ** 2) / N))
    rec("Q3c", "E[T]", p + qq - 1, ET, float(Tm.mean()), float(Tm.std() / math.sqrt(N)))
    rec("Q3c", "Var[T]", p * (1 - p) + qq * (1 - qq), VT, float(Tm.var()),
        math.sqrt((np.mean((Tm - Tm.mean()) ** 4) - Tm.var() ** 2) / N))
    off_cov = -p * qq - (p * qq - p - qq) * (p + qq - 1)
    mc_cov = float(np.mean(Dm * Tm) - Dm.mean() * Tm.mean())
    rec("Q3d", "Cov[D,T]", off_cov, cov, mc_cov, 4.0 / math.sqrt(N) * 0.5)
    rows.append(("Q3d", "Cov == -(p+q)(1-p)(1-q)", off_cov == -(p + qq) * (1 - p) * (1 - qq), True, ""))
    rows.append(("Q3e", "dependent: P(D=0,T=0)=0 != P(D=0)P(T=0)",
                 joint.get((0, 0), Fr(0)) == 0 and (1 - p) * (1 - qq) * (p + qq - 2 * p * qq) > 0, True, ""))
    rows.append(("Q3f", "correlated: cov != 0", cov != 0, True, ""))

# ---------------- Q4: pdf
a_, b_ = sp.symbols("a b", positive=True)
sols = sp.solve([b_ - a_ / 2 - 1, b_ ** 2 / 2 - a_ ** 2 / 6 - sp.Rational(23, 24)], [a_, b_], dict=True)
good = [s for s in sols if s[a_] < s[b_]]
rows.append(("Q4a", "sympy: a=1,b=3/2 unique with a<b",
             len(good) == 1 and good[0][a_] == 1 and good[0][b_] == sp.Rational(3, 2), True, str(sols)))


def Fx(t):
    return 0 if t < 0 else (t * t / 2 if t < 1 else (t - 0.5 if t < 1.5 else 1))


u = rng.random(N)
Xs = np.where(u < 0.5, np.sqrt(2 * u), u + 0.5)       # inverse CDF
rec("Q4a", "E[X]", Fr(23, 24), integrate.quad(lambda x: x * x, 0, 1)[0] + integrate.quad(lambda x: x, 1, 1.5)[0],
    float(Xs.mean()), float(Xs.std() / math.sqrt(N)), tol=1e-9)
for t in (0.4, 1.0, 1.3):
    ex = integrate.quad(lambda x: x if x < 1 else 1, 0, t, points=[1])[0]
    rec("Q4b", "F(%.1f)" % t, Fx(t), ex, float((Xs <= t).mean()), se_p(Fx(t)), tol=1e-9)
m = Xs > 0.5
rec("Q4c", "P(X<=5/4 | X>1/2)", Fr(5, 7), (Fx(1.25) - Fx(0.5)) / (1 - Fx(0.5)), float((Xs[m] <= 1.25).mean()),
    math.sqrt(0.2 / m.sum()), tol=1e-12)


# ---------------- Q5: ball counts
def q5_check(Nn, Dd, p):
    Q_ = Dd / Nn
    Y = rng.geometric(p, N)
    Z = rng.binomial(Y, Q_)
    off0 = p * (1 - Q_) / (p * (1 - Q_) + Q_)
    ex0 = sum(p * (1 - p) ** (j - 1) * (1 - Q_) ** j for j in range(1, 3000))
    rec("Q5b", "P(Z=0) N=%d D=%d p=%s" % (Nn, Dd, p), off0, ex0, float((Z == 0).mean()), se_p(off0), tol=1e-9)
    for k in (1, 2, 4):
        off = p / (1 - p) / (p * (1 - Q_) + Q_) * (Q_ * (1 - p) / (p * (1 - Q_) + Q_)) ** k
        ex = sum(math.comb(j, k) * Q_ ** k * (1 - Q_) ** (j - k) * p * (1 - p) ** (j - 1) for j in range(k, 3000))
        rec("Q5c", "P(Z=%d) N=%d D=%d p=%s" % (k, Nn, Dd, p), off, ex, float((Z == k).mean()), se_p(off), tol=1e-9)
    tot = off0 + sum(p / (1 - p) / (p * (1 - Q_) + Q_) * (Q_ * (1 - p) / (p * (1 - Q_) + Q_)) ** k for k in range(1, 4000))
    rows.append(("Q5c", "sum_k P(Z=k)=1", abs(tot - 1) < 1e-9, True, ""))


for args in ((10, 4, 0.3), (8, 6, 0.5), (20, 3, 0.7)):
    q5_check(*args)
for n_, Nn, Dd in ((6, 10, 4), (12, 7, 3)):
    sim = np.zeros(N, dtype=int)
    for _ in range(n_):                       # n draws with replacement from a collection with D red of N
        sim += (rng.integers(0, Nn, N) < Dd)
    for k in (0, 2, n_ // 2):
        off = math.comb(n_, k) * (Dd / Nn) ** k * (1 - Dd / Nn) ** (n_ - k)
        rec("Q5a", "X~Bin(n,D/N) P(X=%d) n=%d" % (k, n_), off, off, float((sim == k).mean()), se_p(off))


# ---------------- Q6: circuits (bridge: paths AB, CD, AED, CEB)
def Q1f(A, B, C, D, E):
    return (A and B) or (C and D) or (A and E and D) or (C and E and B)


def Q2f(A, B, C, D, E):
    return (A or B) and (C or D or E)


def pexact(f, p):
    t = Fr(0)
    for s in itertools.product((0, 1), repeat=5):
        if f(*s):
            t += math.prod(p if v else 1 - p for v in s)
    return t


for p in (Fr(1, 2), Fr(3, 10), Fr(4, 5)):
    S = rng.random((N, 5)) < float(p)
    A, B, C, D, E = (S[:, i] for i in range(5))
    m1 = (A & B) | (C & D) | (A & E & D) | (C & E & B)
    m2 = (A | B) & (C | D | E)
    o1 = (2 + 2 * p - 5 * p ** 2 + 2 * p ** 3) * p ** 2
    o2 = 6 * p ** 2 - 9 * p ** 3 + 5 * p ** 4 - p ** 5
    o12 = 3 * p ** 5 - 9 * p ** 4 + 7 * p ** 3
    rec("Q6a", "P(Q1) p=%s" % p, o1, pexact(Q1f, p), float(m1.mean()), se_p(float(o1)))
    rec("Q6b", "P(Q2) p=%s" % p, o2, pexact(Q2f, p), float(m2.mean()), se_p(float(o2)))
    ex12 = pexact(lambda *s: Q1f(*s) and Q2f(*s), p)
    rec("Q6c", "P(Q1^Q2) p=%s" % p, o12, ex12, float((m1 & m2).mean()), se_p(float(o12)))
    off = p * (7 - 9 * p + 3 * p ** 2) / (6 - 9 * p + 5 * p ** 2 - p ** 3)
    rec("Q6c", "P(Q1|Q2) p=%s" % p, off, ex12 / pexact(Q2f, p), float((m1 & m2).sum() / m2.sum()),
        math.sqrt(0.25 / m2.sum()))

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print("\nTOTAL %d checks, %d failing" % (len(rows), len(bad)))
