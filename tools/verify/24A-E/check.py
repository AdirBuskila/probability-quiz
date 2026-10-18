# -*- coding: utf-8 -*-
"""Verification harness for 24A-E (probability, reserve-duty moed 9.5.2024). Run: PYTHONUTF8=1 py tools/verify/24A-E/check.py
Every final answer: EXACT (fractions / enumeration / sympy / quadrature) AND Monte Carlo (>=10^6 trials, 4 SE).
Symbolic answers are checked at sample parameter values. Q3 bonus (cov[D,T]) has no key and is held, not checked.
Output is ASCII only."""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20240509)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ---------------- Q1: grasshopper
XL = rng.random(N); XR = 2 * rng.random(N)
rec("Q1a", "P(XL=XR)=0", 0, 0, float((XL == XR).mean()), 1e-6)
ex_b = integrate.quad(lambda x: 2 - x, 0, 1)[0] / 2
rec("Q1b", "P(XR>XL)", Fr(3, 4), ex_b, float((XR > XL).mean()), se_p(0.75), tol=1e-9)
ex_c = integrate.quad(lambda x: x, 0, 1)[0] / 2
rec("Q1c", "P(XR<XL)", Fr(1, 4), ex_c, float((XR < XL).mean()), se_p(0.25), tol=1e-9)
ex_d = integrate.quad(lambda x: 1 / 3, 0, 1)[0] / 2
rec("Q1d", "P(0<XR-XL<1/3)", Fr(1, 6), ex_d, float(((XR - XL > 0) & (XR - XL < 1 / 3)).mean()), se_p(1 / 6), tol=1e-9)

# ---------------- Q2: quadratic y^2+2*X1*y+X2=0 with fair dice
pairs = list(itertools.product(range(1, 7), repeat=2))
R = rng.integers(1, 7, (N, 2)); x1, x2 = R[:, 0], R[:, 1]
disc = x1 * x1 - x2


def is_sq(v):
    return v >= 0 and int(math.isqrt(v)) ** 2 == v


A = [t for t in pairs if t[0] ** 2 < t[1]]
B = [t for t in pairs if is_sq(t[0] ** 2 - t[1])]
rec("Q2a", "P(complex roots)", Fr(7, 36), Fr(len(A), 36), float((disc < 0).mean()), se_p(7 / 36))
sqv = np.isin(disc, [0, 1, 4, 9, 16, 25])
rec("Q2b", "P(integer roots)", Fr(1, 9), Fr(len(B), 36), float((sqv & (disc >= 0)).mean()), se_p(1 / 9))
rows.append(("Q2b", "B = {11,23,24,35}", sorted(10 * a + b for a, b in B) == [11, 23, 24, 35], True, ""))
real = disc >= 0
rec("Q2c", "P(integer | real)", Fr(4, 29), Fr(len([t for t in B if t not in A]), 36 - len(A)), float((sqv & real).sum() / real.sum()), math.sqrt(0.12 / real.sum()))
m = x1 == 3
rec("Q2d", "P(integer | X1=3)", Fr(1, 6), Fr(len([t for t in B if t[0] == 3]), 6), float(sqv[m].mean()), math.sqrt(0.14 / m.sum()))
rows.append(("Q2d", "roots at (3,5) are -1,-5", sorted(sp.solve(sp.Symbol("y") ** 2 + 6 * sp.Symbol("y") + 5, sp.Symbol("y"))) == [-5, -1], True, ""))

# ---------------- Q3: sums of Bernoulli-built variables
for n, p in ((3, Fr(3, 10)), (5, Fr(1, 2)), (4, Fr(4, 5))):
    X = rng.random((N, n)) < float(p); Y = rng.random((N, n)) < float(p)
    Dj = (X & Y); Tj = X.astype(int) + Y
    # per-matrix determinant/trace check by sympy at all 4 states
    for x_, y_ in itertools.product((0, 1), repeat=2):
        Mx = sp.Matrix([[0, -x_], [y_, x_ + y_]])
        assert int(Mx.det()) == x_ * y_ and int(Mx.trace()) == x_ + y_
    rec("Q3a", "P(D1=1)=p^2 n=%d p=%s" % (n, p), p ** 2, p ** 2, float(Dj[:, 0].mean()), se_p(float(p ** 2)))
    for t, v in ((0, (1 - p) ** 2), (1, 2 * p * (1 - p)), (2, p ** 2)):
        rec("Q3b", "T1~Bin(2,p) P=%d" % t, v, v, float((Tj[:, 0] == t).mean()), se_p(float(v)))
    D = Dj.sum(1); T = Tj.sum(1)
    for k in range(0, n + 1):
        off = math.comb(n, k) * p ** (2 * k) * (1 - p ** 2) ** (n - k)
        rec("Q3c", "D~Bin(n,p^2) P(D=%d) n=%d p=%s" % (k, n, p), off, off, float((D == k).mean()), se_p(float(off)))
    for k in range(0, 2 * n + 1):
        off = math.comb(2 * n, k) * p ** k * (1 - p) ** (2 * n - k)
        rec("Q3d", "T~Bin(2n,p) P(T=%d) n=%d p=%s" % (k, n, p), off, off, float((T == k).mean()), se_p(float(off)))
    # exact convolution of the n per-matrix pmfs equals the binomial formulas
    pmfD = {0: 1 - p ** 2, 1: p ** 2}
    conv = {0: Fr(1)}
    for _ in range(n):
        nxt = {}
        for a, va in conv.items():
            for b, vb in pmfD.items():
                nxt[a + b] = nxt.get(a + b, Fr(0)) + va * vb
        conv = nxt
    rows.append(("Q3c", "convolution == Bin(n,p^2) n=%d" % n, all(conv[k] == math.comb(n, k) * p ** (2 * k) * (1 - p ** 2) ** (n - k) for k in conv), True, ""))

# ---------------- Q4: parabola pdf
a_, b_ = sp.symbols("a b", positive=True)
x = sp.symbols("x", real=True)
area = sp.integrate(a_ * (b_ ** 2 - x ** 2), (x, -b_, b_))
var = sp.integrate(x ** 2 * a_ * (b_ ** 2 - x ** 2), (x, -b_, b_))
sol = sp.solve([area - 1, var - sp.Rational(3, 15)], [a_, b_], dict=True)
rows.append(("Q4b", "sympy: a=3/4, b=1", sol == [{a_: sp.Rational(3, 4), b_: 1}], True, str(sol)))
rows.append(("Q4a", "E[X]=0 (odd integrand)", sp.integrate(x * sp.Rational(3, 4) * (1 - x ** 2), (x, -1, 1)) == 0, True, ""))
# rejection sampling from f(x) = 3/4 (1-x^2) on [-1,1]
cand = rng.uniform(-1, 1, 3 * N)
acc = cand[rng.random(3 * N) < (1 - cand ** 2)][:N]
assert len(acc) == N
rec("Q4a", "E[X]", 0, 0, float(acc.mean()), float(acc.std() / math.sqrt(N)))
rec("Q4b", "Var[X]=3/15", Fr(3, 15), float(sp.integrate(x ** 2 * sp.Rational(3, 4) * (1 - x ** 2), (x, -1, 1))), float(acc.var()),
    math.sqrt((np.mean((acc - acc.mean()) ** 4) - acc.var() ** 2) / N), tol=1e-12)
Ft = lambda t: 0.25 * (2 + 3 * t - t ** 3)
for t in (-0.8, 0.0, 0.5, 0.9):
    ex = integrate.quad(lambda u: 0.75 * (1 - u * u), -1, t)[0]
    rec("Q4c", "F(%.1f)" % t, Ft(t), ex, float((acc <= t).mean()), se_p(Ft(t)), tol=1e-9)
rec("Q4d", "P(X>3/4 | |X|<1)", Fr(11, 256), (1 - Ft(0.75)) / (Ft(1) - Ft(-1)), float((acc > 0.75).mean()), se_p(11 / 256), tol=1e-12)

# ---------------- Q5: Poisson thinning
for lam, p in ((6.0, 0.3), (3.5, 0.6), (10.0, 0.15)):
    Y = rng.poisson(lam, N)
    Xw = rng.binomial(Y, p)
    mu = lam * p
    for k in (0, 1, 3, 6):
        off = math.exp(-mu) * mu ** k / math.factorial(k)
        ex = sum(math.comb(j, k) * p ** k * (1 - p) ** (j - k) * math.exp(-lam) * lam ** j / float(math.factorial(j)) for j in range(k, 120))
        rec("Q5a", "P(X=%d) lam=%s p=%s" % (k, lam, p), off, ex, float((Xw == k).mean()), se_p(off), tol=1e-9)
    rows.append(("Q5b", "normalisation sum=1", abs(sum(math.exp(-mu) * mu ** k / float(math.factorial(k)) for k in range(0, 120)) - 1) < 1e-12, True, ""))
    rec("Q5c", "E[X]=p*lam", mu, sum(k * math.exp(-mu) * mu ** k / float(math.factorial(k)) for k in range(120)), float(Xw.mean()), float(Xw.std() / math.sqrt(N)), tol=1e-9)
    rec("Q5c", "Var[X]=p*lam", mu, sum(k * k * math.exp(-mu) * mu ** k / float(math.factorial(k)) for k in range(120)) - mu ** 2, float(Xw.var()),
        math.sqrt((np.mean((Xw - Xw.mean()) ** 4) - Xw.var() ** 2) / N), tol=1e-9)
    n0 = int(round(mu))
    mk = Xw == n0
    for Nn in (n0, n0 + 2, n0 + 5):
        off = (lam * (1 - p)) ** (Nn - n0) / math.factorial(Nn - n0) * math.exp(-lam * (1 - p))
        ex = (math.comb(Nn, n0) * p ** n0 * (1 - p) ** (Nn - n0) * math.exp(-lam) * lam ** Nn / float(math.factorial(Nn))) / \
             (math.exp(-mu) * mu ** n0 / math.factorial(n0))
        rec("Q5d", "P(Y=%d | X=%d) lam=%s p=%s" % (Nn, n0, lam, p), off, ex, float((Y[mk] == Nn).mean()), math.sqrt(max(off * (1 - off), 1e-12) / mk.sum()), tol=1e-9)


# ---------------- Q6: circuits
def Q1f(A, B, C, D):
    return D and ((A and B) or C)


def Q2f(A, B, C, D):
    return D and ((C and B) or A)


def pexact(f, p):
    t = Fr(0)
    for s in itertools.product((0, 1), repeat=4):
        if f(*s):
            t += math.prod(p if v else 1 - p for v in s)
    return t


for p in (Fr(1, 2), Fr(3, 10), Fr(4, 5)):
    S = rng.random((N, 4)) < float(p)
    A, B, C, D = (S[:, i] for i in range(4))
    m1 = D & ((A & B) | C); m2 = D & ((C & B) | A)
    o1 = p ** 2 * (1 + p - p ** 2)
    ou = p ** 2 * (2 - p)
    oi = p ** 3 * (3 - 2 * p)
    rec("Q6a", "P(Q1) p=%s" % p, o1, pexact(Q1f, p), float(m1.mean()), se_p(float(o1)))
    rec("Q6b", "P(Q1 or Q2) p=%s" % p, ou, pexact(lambda *s: Q1f(*s) or Q2f(*s), p), float((m1 | m2).mean()), se_p(float(ou)))
    ex_i = pexact(lambda *s: Q1f(*s) and Q2f(*s), p)
    rec("Q6c", "P(Q1^Q2) p=%s" % p, oi, ex_i, float((m1 & m2).mean()), se_p(float(oi)))
    off = p * (3 - 2 * p) / (1 + p - p ** 2)
    rec("Q6c", "P(Q2|Q1) p=%s" % p, off, ex_i / pexact(Q1f, p), float((m1 & m2).sum() / m1.sum()), math.sqrt(0.25 / m1.sum()))
    allw = A & B & C & D
    offd = p / (3 - 2 * p)
    rec("Q6d", "P(ABCD | Q1^Q2) p=%s" % p, offd, p ** 4 / ex_i, float(allw[m1 & m2].mean()), math.sqrt(0.25 / (m1 & m2).sum()))

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print("\nTOTAL %d checks, %d failing" % (len(rows), len(bad)))
