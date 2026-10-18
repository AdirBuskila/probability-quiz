# -*- coding: utf-8 -*-
"""Verification harness for 24A-B (probability). Run: PYTHONUTF8=1 py tools/verify/24A-B/check.py
Every final answer: EXACT (fractions / enumeration / sympy / quadrature) AND Monte Carlo (>=10^6 trials, 4 SE).
Symbolic answers are checked at sample parameter values. Output is ASCII only."""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20240417)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ---------------- Q1: unit square, S1=x/2, S2=y/2, S3=(1-x)/2
X = rng.random(N); Y = rng.random(N)
S1, S2, S3 = X / 2, Y / 2, (1 - X) / 2
ex1 = lambda f: integrate.dblquad(lambda y, x: f(x, y), 0, 1, 0, 1, epsabs=1e-7)[0]
areas = {
    "Q1a": (Fr(1, 4), 0.25, S1 < 1 / 8),
    "Q1b": (Fr(7, 8), 1 - 0.5 * 0.25, S1 + S2 < 3 / 4),
    "Q1c": (Fr(1, 2), 0.5, S1 < S2),
    "Q1d": (Fr(1, 4), integrate.quad(lambda x: max(0.0, min(x, 1 - x) * 0 + max(0.0, (1 - x) - x)) if x < 0.5 else 0.0, 0, 1, points=[0.5])[0], (S1 < S2) & (S2 < S3)),
}
for item, (off, ex, ev) in areas.items():
    rec(item, "area", off, ex, float(ev.mean()), se_p(float(off)), tol=1e-9)

# ---------------- Q2: fair dice
pairs = list(itertools.product(range(1, 7), repeat=2))
d = lambda ev: Fr(sum(1 for s in pairs if ev(s)), 36)
R = rng.integers(1, 7, (N, 2))
s = R.sum(1); pr = R[:, 0] * R[:, 1]
rec("Q2a", "P(sum=5)", Fr(1, 9), d(lambda t: sum(t) == 5), float((s == 5).mean()), se_p(1 / 9))
m = s == 5
rec("Q2b", "P(first>3 | sum=5)", Fr(1, 4), Fr(sum(1 for t in pairs if sum(t) == 5 and t[0] > 3), sum(1 for t in pairs if sum(t) == 5)),
    float((R[m, 0] > 3).mean()), math.sqrt(0.1875 / m.sum()))
rec("Q2c", "P(prod<=18)", Fr(7, 9), d(lambda t: t[0] * t[1] <= 18), float((pr <= 18).mean()), se_p(7 / 9))
m = pr <= 18
cnt = sum(1 for t in pairs if t[0] * t[1] <= 18)
rec("Q2d", "P(both odd | prod<=18)", Fr(2, 7), Fr(sum(1 for t in pairs if t[0] * t[1] <= 18 and t[0] % 2 and t[1] % 2), cnt),
    float(((R[m, 0] % 2 == 1) & (R[m, 1] % 2 == 1)).mean()), math.sqrt(0.2 / m.sum()))
rows.append(("Q2", "|C|=28, |C^D|=8, |B|=18", cnt == 28 and sum(1 for t in pairs if t[0] > 3) == 18, True, ""))

# ---------------- Q3: Bernoulli matrix
for p in (Fr(3, 10), Fr(1, 2), Fr(4, 5)):
    joint = {}
    for x_, y_ in itertools.product((0, 1), repeat=2):
        M = sp.Matrix([[x_ * y_, -x_], [y_, x_ + y_ - x_ * y_]])
        key = (int(M.det()), int(M.trace()))
        joint[key] = joint.get(key, Fr(0)) + (p if x_ else 1 - p) * (p if y_ else 1 - p)
    off = {(0, 0): (1 - p) ** 2, (0, 1): 2 * p * (1 - p), (2, 2): p ** 2, (0, 2): Fr(0), (2, 0): Fr(0), (2, 1): Fr(0)}
    Xs = rng.random(N) < float(p); Ys = rng.random(N) < float(p)
    Dm = 2 * (Xs & Ys).astype(int); Tm = Xs.astype(int) + Ys
    for k, v in off.items():
        rec("Q3a", "p(D=%d,T=%d) p=%s" % (k + (p,)), v, joint.get(k, Fr(0)), float(((Dm == k[0]) & (Tm == k[1])).mean()), max(se_p(float(v)), 1e-9))
    rec("Q3b", "P(D=2)=p^2 p=%s" % p, p ** 2, sum(v for k, v in joint.items() if k[0] == 2), float((Dm == 2).mean()), se_p(float(p ** 2)))
    for t, v in ((0, (1 - p) ** 2), (1, 2 * p * (1 - p)), (2, p ** 2)):
        rec("Q3c", "T~Bin(2,p) P(T=%d) p=%s" % (t, p), v, sum(w for k, w in joint.items() if k[1] == t), float((Tm == t).mean()), se_p(float(v)))
    ED = sum(k[0] * v for k, v in joint.items()); ET = sum(k[1] * v for k, v in joint.items())
    cov = sum(k[0] * k[1] * v for k, v in joint.items()) - ED * ET
    rows.append(("Q3e", "E[D]=2p^2, E[T]=2p, E[DT]=4p^2", ED == 2 * p ** 2 and ET == 2 * p and sum(k[0] * k[1] * v for k, v in joint.items()) == 4 * p ** 2, True, ""))
    mc_cov = float(np.mean(Dm * Tm) - Dm.mean() * Tm.mean())
    rec("Q3e", "Cov = 4p^2(1-p) p=%s" % p, 4 * p ** 2 * (1 - p), cov, mc_cov, 2.0 / math.sqrt(N))
    rows.append(("Q3d", "dependent: p(2,0)=0 != p_D(2)p_T(0)", joint.get((2, 0), Fr(0)) == 0 and p ** 2 * (1 - p) ** 2 > 0, True, ""))

# ---------------- Q4
a_, b_, c_ = sp.symbols("a b c", positive=True)
sols = sp.solve([a_ * c_ - 2 * (b_ - a_), a_ * c_ + (b_ - a_) - 1, c_ * a_ ** 2 / 2 + (b_ ** 2 - a_ ** 2) / 2 - sp.Rational(5, 9)], [a_, b_, c_], dict=True)
good = [t for t in sols if t[a_] < t[b_]]
rows.append(("Q4a", "sympy: a=3/4,b=13/12,c=8/9", len(good) == 1 and good[0][a_] == sp.Rational(3, 4) and good[0][b_] == sp.Rational(13, 12) and good[0][c_] == sp.Rational(8, 9), True, str(sols)))
a, b, c = 0.75, 13 / 12, 8 / 9


def Fx(t):
    return 0 if t < 0 else (c * t if t < a else (c * a + t - a if t < b else 1))


u = rng.random(N)
Xs = np.where(u < 2 / 3, u / c, u + a - c * a)        # inverse CDF
rec("Q4a", "E[X]", Fr(5, 9), integrate.quad(lambda x: x * c, 0, a)[0] + integrate.quad(lambda x: x, a, b)[0], float(Xs.mean()), float(Xs.std() / math.sqrt(N)), tol=1e-9)
rows.append(("Q4a", "P(0<=X<=a)=2P(a<=X<=b)", abs(c * a - 2 * (b - a)) < 1e-12, True, ""))
rec("Q4a", "MC P(X<=a)=2/3", Fr(2, 3), Fr(2, 3), float((Xs <= a).mean()), se_p(2 / 3))
for t in (0.3, 0.9, 1.05):
    ex = integrate.quad(lambda x: c if x < a else 1, 0, t, points=[a])[0]
    off = (8 / 9 * t) if t < 0.75 else t - 1 / 12
    rec("Q4b", "F(%.2f)" % t, off, ex, float((Xs <= t).mean()), se_p(off), tol=1e-9)
rec("Q4c", "P(X<=5/9)", Fr(40, 81), Fx(5 / 9), float((Xs <= 5 / 9).mean()), se_p(40 / 81), tol=1e-12)


# ---------------- Q5: identical to 24A-C Q5
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
    for _ in range(n_):
        sim += (rng.integers(0, Nn, N) < Dd)
    for k in (0, 2, n_ // 2):
        off = math.comb(n_, k) * (Dd / Nn) ** k * (1 - Dd / Nn) ** (n_ - k)
        rec("Q5a", "X~Bin(n,D/N) P(X=%d) n=%d" % (k, n_), off, off, float((sim == k).mean()), se_p(off))


# ---------------- Q6: Q1 bridge, Q2 = (A|B)&(C|D)
def Q1f(A, B, C, D, E):
    return (A and B) or (C and D) or (A and E and D) or (C and E and B)


def Q2f(A, B, C, D, E):
    return (A or B) and (C or D)


def pexact(f, p):
    t = Fr(0)
    for s_ in itertools.product((0, 1), repeat=5):
        if f(*s_):
            t += math.prod(p if v else 1 - p for v in s_)
    return t


for p in (Fr(1, 2), Fr(3, 10), Fr(4, 5)):
    S = rng.random((N, 5)) < float(p)
    A, B, C, D, E = (S[:, i] for i in range(5))
    m1 = (A & B) | (C & D) | (A & E & D) | (C & E & B)
    m2 = (A | B) & (C | D)
    o1 = (2 + 2 * p - 5 * p ** 2 + 2 * p ** 3) * p ** 2
    o2 = (2 * p - p ** 2) ** 2
    o12 = p ** 3 * (6 - 7 * p + 2 * p ** 2)
    rec("Q6a", "P(Q1) p=%s" % p, o1, pexact(Q1f, p), float(m1.mean()), se_p(float(o1)))
    rec("Q6b", "P(Q2) p=%s" % p, o2, pexact(Q2f, p), float(m2.mean()), se_p(float(o2)))
    ex12 = pexact(lambda *s_: Q1f(*s_) and Q2f(*s_), p)
    rec("Q6c", "P(Q1^Q2) p=%s" % p, o12, ex12, float((m1 & m2).mean()), se_p(float(o12)))
    rows.append(("Q6c", "alt: p^2(2p-p^2)(3-2p) == p^3(6-7p+2p^2)", p ** 2 * (2 * p - p ** 2) * (3 - 2 * p) == o12, True, ""))
    off = p * (3 - 2 * p) / (2 - p)
    rec("Q6c", "P(Q1|Q2) p=%s" % p, off, ex12 / pexact(Q2f, p), float((m1 & m2).sum() / m2.sum()), math.sqrt(0.25 / m2.sum()))

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print("\nTOTAL %d checks, %d failing" % (len(rows), len(bad)))
