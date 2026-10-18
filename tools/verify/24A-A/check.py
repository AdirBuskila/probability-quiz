# -*- coding: utf-8 -*-
"""Verification harness for 24A-A (probability). Run: PYTHONUTF8=1 py tools/verify/24A-A/check.py
Every final answer: EXACT (fractions / enumeration / sympy / quadrature) AND Monte Carlo (>=10^6 trials, 4 SE).
Symbolic answers are checked at sample parameter values. The two bonus parts (Q2 d, Q3 d) have no key and ship as solved:
P_N = (1/N)(1+1/N)^(N-1) and E[X1 | X=n] = n N1/(N1+N2), both checked exactly and by MC.
Output is ASCII only."""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20240325)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ---------------- Q1: rectangle X~U(0,1), Y~U(0,2)
X = rng.random(N); Y = 2 * rng.random(N)
S = X * Y; L = 2 * (X + Y)
o_a = 0.5 * (1 + math.log(2))
ex_a = integrate.quad(lambda x: min(2.0, 1 / x), 0, 1, points=[0.5], limit=200)[0] / 2
rec("Q1a", "P(S<1)", o_a, ex_a, float((S < 1).mean()), se_p(o_a), tol=1e-9)
ex_b = integrate.quad(lambda x: max(0.0, 1 - x), 0, 1)[0] / 2
rec("Q1b", "P(L<2)", Fr(1, 4), ex_b, float((L < 2).mean()), se_p(0.25), tol=1e-9)
o_c = 1 / 3 + 2 / 3 * math.log(2)
ex_c = integrate.quad(lambda x: max(0.0, min(2.0, 1 / x) - max(0.0, 1 - x)), 0, 1, points=[0.5], limit=200)[0] / 2 / 0.75
m = L > 2
rec("Q1c", "P(S<1 | L>2)", o_c, ex_c, float((S[m] < 1).mean()), math.sqrt(0.16 / m.sum()), tol=1e-9)
x_, y_ = sp.symbols("x y", positive=True)
ES = sp.integrate(sp.integrate(x_ * y_ / 2, (y_, 0, 2)), (x_, 0, 1))
ES2 = sp.integrate(sp.integrate(x_ ** 2 * y_ ** 2 / 2, (y_, 0, 2)), (x_, 0, 1))
rec("Q1d", "E[S]", Fr(1, 2), float(ES), float(S.mean()), float(S.std() / math.sqrt(N)), tol=1e-12)
rec("Q1d", "Var[S]=7/36", Fr(7, 36), float(ES2 - ES ** 2), float(S.var()), math.sqrt((np.mean((S - S.mean()) ** 4) - S.var() ** 2) / N), tol=1e-12)
EL = sp.integrate(sp.integrate(2 * (x_ + y_) / 2, (y_, 0, 2)), (x_, 0, 1))
EL2 = sp.integrate(sp.integrate((2 * (x_ + y_)) ** 2 / 2, (y_, 0, 2)), (x_, 0, 1))
rec("Q1e", "E[L]", 3, float(EL), float(L.mean()), float(L.std() / math.sqrt(N)), tol=1e-12)
rec("Q1e", "Var[L]=5/3", Fr(5, 3), float(EL2 - EL ** 2), float(L.var()), math.sqrt((np.mean((L - L.mean()) ** 4) - L.var() ** 2) / N), tol=1e-12)


# ---------------- Q2: probability the running sum ever equals n (fair n-sided die)
def p_hit(n, faces):
    f = [Fr(0)] * (n + 1); f[0] = Fr(1)
    for s in range(1, n + 1):
        f[s] = sum(f[s - k] for k in range(1, faces + 1) if s - k >= 0) / faces
    return f[n]


def mc_hit(n, trials):
    pos = np.zeros(trials, dtype=np.int64); hit = np.zeros(trials, dtype=bool)
    live = np.ones(trials, dtype=bool)
    while live.any():
        idx = np.nonzero(live)[0]
        pos[idx] += rng.integers(1, n + 1, len(idx))
        hit[idx[pos[idx] == n]] = True
        live[idx[pos[idx] >= n]] = False
    return float(hit.mean())


for n, item in ((3, "Q2a"), (4, "Q2b"), (5, "Q2c")):
    p = Fr(1, n)
    off = p * (1 + p) ** (n - 1)
    rec(item, "P_%d = p(1+p)^%d" % (n, n - 1), off, p_hit(n, n), mc_hit(n, N), se_p(float(off)))
rows.append(("Q2d", "P_N = (1/N)(1+1/N)^(N-1) exact for N=2..12 (shipped bonus answer)",
             all(p_hit(n, n) == Fr(1, n) * (1 + Fr(1, n)) ** (n - 1) for n in range(2, 13)), True, ""))
for n in (6, 10):
    off = Fr(1, n) * (1 + Fr(1, n)) ** (n - 1)
    rec("Q2d", "P_%d = (1/N)(1+1/N)^(N-1) (shipped)" % n, off, p_hit(n, n), mc_hit(n, N), se_p(float(off)))
rows.append(("Q2", "compositions count C(n-1,k-1) used in the official lists (n=3,4,5)",
             all(sum(1 for c in itertools.product(range(1, n + 1), repeat=k) if sum(c) == n) == math.comb(n - 1, k - 1)
                 for n in (3, 4, 5) for k in range(1, n + 1)), True, ""))

# ---------------- Q3: binomial strings
for N1, N2, p in ((7, 9, 0.35), (4, 6, 0.5), (10, 5, 0.8)):
    X1 = rng.binomial(N1, p, N); X2 = rng.binomial(N2, p, N); Xs = X1 + X2
    for k in (0, N1 // 2, N1):
        off = math.comb(N1, k) * p ** k * (1 - p) ** (N1 - k)
        rec("Q3a", "X1~Bin P(%d) N1=%d" % (k, N1), off, off, float((X1 == k).mean()), se_p(off))
    for j in (1, (N1 + N2) // 2, N1 + N2):
        off = math.comb(N1 + N2, j) * p ** j * (1 - p) ** (N1 + N2 - j)
        ex = sum(math.comb(N1, a) * math.comb(N2, j - a) * p ** j * (1 - p) ** (N1 + N2 - j) for a in range(0, N1 + 1) if 0 <= j - a <= N2)
        rec("Q3b", "X~Bin(N1+N2,p) P(%d)" % j, off, ex, float((Xs == j).mean()), se_p(off), tol=1e-12)
    n_ = (N1 + N2) // 2
    mm = Xs == n_
    for k in range(max(0, n_ - N2), min(N1, n_) + 1):
        off = math.comb(N1, k) * math.comb(N2, n_ - k) / math.comb(N1 + N2, n_)
        ex = (math.comb(N1, k) * p ** k * (1 - p) ** (N1 - k) * math.comb(N2, n_ - k) * p ** (n_ - k) * (1 - p) ** (N2 - n_ + k)) / \
             (math.comb(N1 + N2, n_) * p ** n_ * (1 - p) ** (N1 + N2 - n_))
        rec("Q3c", "P(X1=%d | X=%d) N1=%d N2=%d" % (k, n_, N1, N2), off, ex, float((X1[mm] == k).mean()),
            math.sqrt(max(off * (1 - off), 1e-9) / mm.sum()), tol=1e-12)
    # Q3d (bonus, solved): E[X1 | X=n] = n N1/(N1+N2); exact from the joint binomial pmf, MC on the X=n slice
    for n_d in (n_ - 2, n_, n_ + 2):
        ship = Fr(n_d * N1, N1 + N2)
        pp = Fr(p).limit_denominator(100)
        w = [Fr(math.comb(N1, k)) * pp ** k * (1 - pp) ** (N1 - k) * math.comb(N2, n_d - k) * pp ** (n_d - k) * (1 - pp) ** (N2 - n_d + k)
             for k in range(0, N1 + 1) if 0 <= n_d - k <= N2]
        ks = [k for k in range(0, N1 + 1) if 0 <= n_d - k <= N2]
        ex = sum(k * wk for k, wk in zip(ks, w)) / sum(w)
        md = Xs == n_d
        sl = X1[md]
        rec("Q3d", "E[X1 | X=%d] = nN1/(N1+N2) N1=%d N2=%d p=%s (shipped)" % (n_d, N1, N2, p), ship, ex, float(sl.mean()),
            float(sl.std() / math.sqrt(md.sum())), tol=1e-12)

# ---------------- Q4
a_, b_, c_ = sp.symbols("a b c", positive=True)
sols = sp.solve([a_ * c_ / 2 + c_ * (b_ - a_) - 1, a_ * c_ / 2 - c_ * (b_ - a_), c_ * b_ ** 2 / 2 - c_ * a_ ** 2 / 6 - sp.Rational(23, 24)],
                [a_, b_, c_], dict=True)
rows.append(("Q4a", "sympy: a=1,b=3/2,c=1", sols == [{a_: 1, b_: sp.Rational(3, 2), c_: 1}], True, str(sols)))
u = rng.random(N)
Xs = np.where(u < 0.5, np.sqrt(2 * u), u + 0.5)


def Fx(t):
    return 0 if t < 0 else (t * t / 2 if t < 1 else (t - 0.5 if t < 1.5 else 1))


rec("Q4a", "E[X]=23/24", Fr(23, 24), integrate.quad(lambda x: x * x, 0, 1)[0] + integrate.quad(lambda x: x, 1, 1.5)[0], float(Xs.mean()),
    float(Xs.std() / math.sqrt(N)), tol=1e-9)
rec("Q4a", "P(0<=X<=a)=P(a<=X<=b)", Fr(1, 2), Fr(1, 2), float((Xs <= 1).mean()), se_p(0.5))
for t in (0.4, 1.0, 1.3):
    ex = integrate.quad(lambda x: x if x < 1 else 1, 0, t, points=[1])[0]
    rec("Q4b", "F(%.1f)" % t, Fx(t), ex, float((Xs <= t).mean()), se_p(Fx(t)), tol=1e-9)
o4c = 1 - 0.5 * (23 / 24) ** 2
rec("Q4c", "P(X>E[X])", o4c, 1 - Fx(23 / 24), float((Xs > 23 / 24).mean()), se_p(o4c), tol=1e-12)

# ---------------- Q5: students, birthdays
Nn, p, Q = 8, 0.6, 0.2        # Q=1/365 is too small to condition on; the formulas are identical in Q
came = rng.random((N, Nn)) < p
born = rng.random((N, Nn)) < Q
Xc = came.sum(1); Yc = (came & born).sum(1)
for j in (0, 3, 8):
    off = math.comb(Nn, j) * p ** j * (1 - p) ** (Nn - j)
    rec("Q5a", "X~Bin(N,p) P(%d)" % j, off, off, float((Xc == j).mean()), se_p(off))
for k in (0, 1, 2, 4):
    off = math.comb(Nn, k) * (p * Q) ** k * (1 - p * Q) ** (Nn - k)
    ex = sum(math.comb(j, k) * Q ** k * (1 - Q) ** (j - k) * math.comb(Nn, j) * p ** j * (1 - p) ** (Nn - j) for j in range(k, Nn + 1))
    rec("Q5b", "Y~Bin(N,pQ) P(%d)" % k, off, ex, float((Yc == k).mean()), se_p(off), tol=1e-12)
pt = (1 - p) / (1 - p * Q)
for k in (1, 2):
    mk = Yc == k
    for n in range(k, Nn + 1):
        off = math.comb(Nn - k, Nn - n) * pt ** (Nn - n) * (1 - pt) ** (n - k)
        ex = (math.comb(n, k) * Q ** k * (1 - Q) ** (n - k) * math.comb(Nn, n) * p ** n * (1 - p) ** (Nn - n)) / \
             (math.comb(Nn, k) * (p * Q) ** k * (1 - p * Q) ** (Nn - k))
        rec("Q5c", "P(X=%d | Y=%d)" % (n, k), off, ex, float((Xc[mk] == n).mean()), math.sqrt(max(off * (1 - off), 1e-9) / mk.sum()), tol=1e-12)


# ---------------- Q6: bridge circuits; Q1 middle=E, Q2 middle=A (top-left=A in Q1, E in Q2)
def bridge(tl, tr, bl, br, mid):
    return (tl and tr) or (bl and br) or (tl and mid and br) or (bl and mid and tr)


def Q1f(A, B, C, D, E):
    return bridge(A, B, C, D, E)


def Q2f(A, B, C, D, E):
    return bridge(E, B, C, D, A)


def pexact(f, p):
    t = Fr(0)
    for s in itertools.product((0, 1), repeat=5):
        if f(*s):
            t += math.prod(p if v else 1 - p for v in s)
    return t


for p in (Fr(1, 2), Fr(3, 10), Fr(4, 5)):
    Sm = rng.random((N, 5)) < float(p)
    A, B, C, D, E = (Sm[:, i] for i in range(5))
    m1 = (A & B) | (C & D) | (A & E & D) | (C & E & B)
    m2 = (E & B) | (C & D) | (E & A & D) | (C & A & B)
    o1 = p ** 2 * (2 + 2 * p - 5 * p ** 2 + 2 * p ** 3)
    oi = p ** 2 * (1 + 4 * p - 6 * p ** 2 + 2 * p ** 3)
    ou = p ** 2 * (3 - 4 * p ** 2 + 2 * p ** 3)
    rec("Q6a", "P(Q1) p=%s" % p, o1, pexact(Q1f, p), float(m1.mean()), se_p(float(o1)))
    rec("Q6a", "P(Q2)=P(Q1) p=%s" % p, o1, pexact(Q2f, p), float(m2.mean()), se_p(float(o1)))
    exi = pexact(lambda *s: Q1f(*s) and Q2f(*s), p)
    rec("Q6b", "P(Q1^Q2) p=%s" % p, oi, exi, float((m1 & m2).mean()), se_p(float(oi)))
    off = (1 + 4 * p - 6 * p ** 2 + 2 * p ** 3) / (2 + 2 * p - 5 * p ** 2 + 2 * p ** 3)
    rec("Q6b", "P(Q2|Q1) p=%s" % p, off, exi / pexact(Q1f, p), float((m1 & m2).sum() / m1.sum()), math.sqrt(0.25 / m1.sum()))
    alt = p * (2 * p - p ** 2) ** 2 + (1 - p) * p ** 2 * (1 + p - p ** 2)
    rows.append(("Q6b", "alternative solution == main p=%s" % p, alt == oi, True, ""))
    rec("Q6c", "P(Q1 or Q2) p=%s" % p, ou, pexact(lambda *s: Q1f(*s) or Q2f(*s), p), float((m1 | m2).mean()), se_p(float(ou)))

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print("\nTOTAL %d checks, %d failing" % (len(rows), len(bad)))
raise SystemExit(1 if bad else 0)
