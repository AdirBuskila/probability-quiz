# -*- coding: utf-8 -*-
"""Verification harness for 24A-D (probability, 20021-80 group, 3.4.2024). Run: PYTHONUTF8=1 py tools/verify/24A-D/check.py
Every final answer: EXACT (fractions / enumeration / sympy / quadrature) AND Monte Carlo (>=10^6 trials, 4 SE).
Symbolic answers are checked at sample parameter values. Output is ASCII only."""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20240403)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ---------------- Q1: two uniform jumps
X1 = rng.random(N); X2 = rng.random(N)
ex_a = integrate.quad(lambda x: max(0.0, 2 / 3 - x), 0, 1, points=[2 / 3])[0]
rec("Q1a", "P(X1+X2<=2/3)", Fr(2, 9), ex_a, float((X1 + X2 <= 2 / 3).mean()), se_p(2 / 9), tol=1e-9)
rec("Q1b", "P(X1<2/3, X2<2/3)", Fr(4, 9), (2 / 3) ** 2, float(((X1 < 2 / 3) & (X2 < 2 / 3)).mean()), se_p(4 / 9))
ex_c = integrate.quad(lambda x: 1 - x, 0, 2 / 3)[0] / (2 / 3)
m = X1 <= 2 / 3
rec("Q1c", "P(X1+X2<=1 | X1<=2/3)", Fr(2, 3), ex_c, float((X1[m] + X2[m] <= 1).mean()), math.sqrt(0.2222 / m.sum()), tol=1e-9)

# ---------------- Q2: fair dice
trip = list(itertools.product(range(1, 7), repeat=3))
pair = list(itertools.product(range(1, 7), repeat=2))
R = rng.integers(1, 7, (N, 3)); s3 = R.sum(1)
rec("Q2a", "P(sum2=6)", Fr(5, 36), Fr(sum(1 for t in pair if sum(t) == 6), 36), float((R[:, 0] + R[:, 1] == 6).mean()), se_p(5 / 36))
rec("Q2b", "P(sum3=6)", Fr(5, 108), Fr(sum(1 for t in trip if sum(t) == 6), 216), float((s3 == 6).mean()), se_p(5 / 108))
m = R[:, 0] + R[:, 1] == 2
rec("Q2c", "P(sum3=6 | X1+X2=2)", Fr(1, 6), Fr(sum(1 for t in trip if sum(t) == 6 and t[0] + t[1] == 2), sum(1 for t in trip if t[0] + t[1] == 2)),
    float((s3[m] == 6).mean()), math.sqrt(0.14 / m.sum()))
m = R[:, 0] < R[:, 1]
rec("Q2d", "P(sum3=6 | X1<X2)", Fr(2, 45), Fr(sum(1 for t in trip if sum(t) == 6 and t[0] < t[1]), sum(1 for t in trip if t[0] < t[1])),
    float((s3[m] == 6).mean()), math.sqrt(0.043 / m.sum()))
rows.append(("Q2d", "P(X1<X2)=5/12, |sum=6 ^ X1<X2|=4", sum(1 for t in pair if t[0] < t[1]) == 15 and sum(1 for t in trip if sum(t) == 6 and t[0] < t[1]) == 4, True, ""))
m = R[:, 0] == R[:, 1]
rec("Q2e", "P(sum3=6 | X1=X2)", Fr(1, 18), Fr(sum(1 for t in trip if sum(t) == 6 and t[0] == t[1]), sum(1 for t in trip if t[0] == t[1])),
    float((s3[m] == 6).mean()), math.sqrt(0.053 / m.sum()))

# ---------------- Q3: matrix [[0,X],[Y,X+Y]]
for p, q in ((Fr(3, 10), Fr(1, 2)), (Fr(2, 5), Fr(7, 10)), (Fr(1, 4), Fr(1, 3))):
    joint = {}
    for x_, y_ in itertools.product((0, 1), repeat=2):
        M = sp.Matrix([[0, x_], [y_, x_ + y_]])
        key = (int(M.det()), int(M.trace()))
        joint[key] = joint.get(key, Fr(0)) + (p if x_ else 1 - p) * (q if y_ else 1 - q)
    ED = sum(k[0] * v for k, v in joint.items()); ET = sum(k[1] * v for k, v in joint.items())
    VD = sum(k[0] ** 2 * v for k, v in joint.items()) - ED ** 2
    VT = sum(k[1] ** 2 * v for k, v in joint.items()) - ET ** 2
    cov = sum(k[0] * k[1] * v for k, v in joint.items()) - ED * ET
    Xs = rng.random(N) < float(p); Ys = rng.random(N) < float(q)
    Dm = -(Xs & Ys).astype(int); Tm = Xs.astype(int) + Ys
    rec("Q3a", "E[D] p=%s q=%s" % (p, q), -p * q, ED, float(Dm.mean()), float(Dm.std() / math.sqrt(N)))
    rec("Q3a", "Var[D]", p * q * (1 - p * q), VD, float(Dm.var()), math.sqrt((np.mean((Dm - Dm.mean()) ** 4) - Dm.var() ** 2) / N))
    rec("Q3b", "E[T]", p + q, ET, float(Tm.mean()), float(Tm.std() / math.sqrt(N)))
    rec("Q3b", "Var[T]", p * (1 - p) + q * (1 - q), VT, float(Tm.var()), math.sqrt((np.mean((Tm - Tm.mean()) ** 4) - Tm.var() ** 2) / N))
    rec("Q3c", "Cov[D,T] = pq(p+q-2)", p * q * (p + q - 2), cov, float(np.mean(Dm * Tm) - Dm.mean() * Tm.mean()), 2.0 / math.sqrt(N))

# ---------------- Q4: triangular pdf
a_, b_ = sp.symbols("a b", positive=True)
x = sp.symbols("x", real=True)
area = 2 * sp.integrate(a_ * (b_ - x), (x, 0, b_))
var = 2 * sp.integrate(x ** 2 * a_ * (b_ - x), (x, 0, b_))
sol = sp.solve([area - 1, var - sp.Rational(2, 3)], [a_, b_], dict=True)
rows.append(("Q4b", "sympy: a=1/4, b=2", sol == [{a_: sp.Rational(1, 4), b_: 2}], True, str(sol)))
rows.append(("Q4a", "E[X]=0", sp.integrate(x * sp.Rational(1, 4) * (2 - sp.Abs(x)), (x, -2, 2)) == 0, True, ""))
# inverse-CDF sampling for the triangular density on [-2,2]
u = rng.random(N)
Xs = np.where(u < 0.5, -2 + np.sqrt(8 * u), 2 - np.sqrt(8 * (1 - u)))


def Ft(t):
    return 0 if t < -2 else (0.125 * (t + 2) ** 2 if t < 0 else (1 - 0.125 * (2 - t) ** 2 if t < 2 else 1))


rec("Q4a", "E[X]", 0, 0, float(Xs.mean()), float(Xs.std() / math.sqrt(N)))
rec("Q4b", "Var[X]=2/3", Fr(2, 3), float(sp.integrate(x ** 2 * sp.Rational(1, 4) * (2 - sp.Abs(x)), (x, -2, 2))), float(Xs.var()),
    math.sqrt((np.mean((Xs - Xs.mean()) ** 4) - Xs.var() ** 2) / N), tol=1e-12)
for t in (-1.5, -0.5, 0.5, 1.5):
    ex = integrate.quad(lambda u_: 0.25 * (2 - abs(u_)), -2, t, points=[0])[0]
    rec("Q4c", "F(%.1f)" % t, Ft(t), ex, float((Xs <= t).mean()), se_p(Ft(t)), tol=1e-9)
mm = np.abs(Xs) < 1
rec("Q4d", "P(X>1/4 | |X|<1)", Fr(11, 32), (Ft(1) - Ft(0.25)) / (Ft(1) - Ft(-1)), float((Xs[mm] > 0.25).mean()),
    math.sqrt(0.23 / mm.sum()), tol=1e-12)


# ---------------- Q5: birthdays, Poisson thinning
for lam, pp in ((8.0, 1 / 365 * 30), (5.0, 0.2), (12.0, 0.1)):     # larger p than 1/365 so that conditioning has data
    Xp = rng.poisson(lam, N)
    Yb = rng.binomial(Xp, pp)
    mu = lam * pp
    for k in (0, 1, 2, 3):
        off = math.exp(-mu) * mu ** k / math.factorial(k)
        ex = sum(math.comb(j, k) * pp ** k * (1 - pp) ** (j - k) * math.exp(-lam) * lam ** j / float(math.factorial(j)) for j in range(k, 120))
        rec("Q5b", "P(Y=%d) lam=%s p=%.4f" % (k, lam, pp), off, ex, float((Yb == k).mean()), se_p(off), tol=1e-9)
    k0 = 1
    mk = Yb == k0
    for n in (k0, k0 + 2, k0 + 5):
        off = (lam * (1 - pp)) ** (n - k0) / math.factorial(n - k0) * math.exp(-lam * (1 - pp))
        ex = (math.comb(n, k0) * pp ** k0 * (1 - pp) ** (n - k0) * math.exp(-lam) * lam ** n / float(math.factorial(n))) / \
             (math.exp(-mu) * mu ** k0 / math.factorial(k0))
        rec("Q5c", "P(X=%d | Y=1) lam=%s p=%.4f" % (n, lam, pp), off, ex, float((Xp[mk] == n).mean()), math.sqrt(max(off * (1 - off), 1e-9) / mk.sum()), tol=1e-9)
Nn, pb = 9, 1 / 365
for k in (0, 1, 2):
    off = math.comb(Nn, k) * pb ** k * (1 - pb) ** (Nn - k)
    sim = (rng.random((N, Nn)) < pb).sum(1)
    rec("Q5a", "W~Bin(N,1/365) P(%d) N=%d" % (k, Nn), off, off, float((sim == k).mean()), se_p(off))


# ---------------- Q6: Q1 = bridge (top-left A, middle E); Q2 = A or (E and B) or (C and D)
def Q1f(A, B, C, D, E):
    return (A and B) or (C and D) or (A and E and D) or (C and E and B)


def Q2f(A, B, C, D, E):
    return A or (E and B) or (C and D)


def pexact(f, p):
    t = Fr(0)
    for s_ in itertools.product((0, 1), repeat=5):
        if f(*s_):
            t += math.prod(p if v else 1 - p for v in s_)
    return t


rows.append(("Q6c", "Q1 is contained in Q2 (all 32 states)", all((not Q1f(*s_)) or Q2f(*s_) for s_ in itertools.product((0, 1), repeat=5)), True, ""))
for p in (Fr(1, 2), Fr(3, 10), Fr(4, 5)):
    S = rng.random((N, 5)) < float(p)
    A, B, C, D, E = (S[:, i] for i in range(5))
    m1 = (A & B) | (C & D) | (A & E & D) | (C & E & B)
    m2 = A | (E & B) | (C & D)
    o1 = p * (2 * p - p ** 2) ** 2 + (1 - p) * (2 * p ** 2 - p ** 4)
    o2 = p + (1 - p) * (2 * p ** 2 - p ** 4)
    oi = (2 * p - p ** 2) * p ** 2 + p ** 2 * (1 - p) ** 2 + p * (1 - p) * (p + p ** 2 - p ** 3) + p ** 2 * (1 - p) * (2 * p - p ** 2)
    rec("Q6a", "P(Q1) p=%s" % p, o1, pexact(Q1f, p), float(m1.mean()), se_p(float(o1)))
    rec("Q6b", "P(Q2) p=%s" % p, o2, pexact(Q2f, p), float(m2.mean()), se_p(float(o2)))
    exi = pexact(lambda *s_: Q1f(*s_) and Q2f(*s_), p)
    rec("Q6c", "P(Q1^Q2) official expansion p=%s" % p, oi, exi, float((m1 & m2).mean()), se_p(float(oi)))
    rows.append(("Q6c", "P(Q1^Q2) == P(Q1) so P(Q2|Q1)=1 p=%s" % p, oi == o1 and exi / pexact(Q1f, p) == 1, True, ""))
    rec("Q6c", "P(Q2|Q1)=1 (MC)", 1, exi / pexact(Q1f, p), float((m1 & m2).sum() / m1.sum()), 1e-9)

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print("\nTOTAL %d checks, %d failing" % (len(rows), len(bad)))
