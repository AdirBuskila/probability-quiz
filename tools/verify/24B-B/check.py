# -*- coding: utf-8 -*-
"""Verification harness for 24B-B (probability). Run: PYTHONUTF8=1 py tools/verify/24B-B/check.py

Every final answer gets two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy).
  MC    : Monte Carlo (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Official keys are never changed. Q3d disagrees with the exact value (official 5/9, exact 1/2) and is HELD.
Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20240806)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1 (L = 1)
X1 = rng.random(N); X2 = 2 * rng.random(N)
x, y = sp.symbols("x y", positive=True)
rec("Q1a", "P(X1<1/5)", Fr(1, 5), Fr(1, 5), float(np.mean(X1 < .2)), se_p(.2))
ex = sp.integrate(sp.Integer(2) - sp.Max(0, 1 - x) * 0 - sp.Min(2, sp.Max(0, 1 - x)), (x, 0, 1)) / 2
ex = sp.integrate(2 - (1 - x), (x, 0, 1)) / 2     # y>1-x within y in (0,2)
rec("Q1b", "P(X1+X2>1)", Fr(3, 4), Fr(int(ex.p), int(ex.q)), float(np.mean(X1 + X2 > 1)), se_p(.75))
ex = sp.integrate(x, (x, 0, 1)) / 2             # y<x
rec("Q1c", "P(X1>X2)", Fr(1, 4), Fr(int(ex.p), int(ex.q)), float(np.mean(X1 > X2)), se_p(.25))
for p in (Fr(3, 10), Fr(4, 5)):
    head = rng.random(N) < float(p)
    Y = np.where(head, X1, X2)
    off = (1 + p) / 2
    ex = p * 1 + (1 - p) * Fr(1, 2)
    rec("Q1d", "P(Y<L) p=%s" % p, off, ex, float(np.mean(Y < 1)), se_p(float(off)))
    off = Fr(1, 2)
    ex = p * Fr(1, 2) + (1 - p) * Fr(1, 2)
    rec("Q1e", "P(1/2<Y<3/2) p=%s" % p, off, ex, float(np.mean((Y > .5) & (Y < 1.5))), se_p(.5))

# ============================================================ Q2 (urn)
for (Nn, D) in ((10, 4), (7, 3), (12, 5)):
    balls = [1] * D + [0] * (Nn - D)
    perms = list(itertools.permutations(range(Nn), 3))
    r = lambda i: balls[i]
    tot = len(perms)
    a = Fr(sum(r(s[0]) for s in perms), tot)
    b = Fr(sum(r(s[1]) for s in perms), tot)
    c = Fr(sum(r(s[2]) for s in perms), tot)
    n2 = sum(r(s[1]) for s in perms)
    d = Fr(sum(r(s[1]) * r(s[2]) for s in perms), n2)
    M = np.argsort(rng.random((N, Nn), dtype=np.float32), axis=1)[:, :3]
    R = (M < D)
    rec("Q2a", "N=%d D=%d" % (Nn, D), Fr(D, Nn), a, float(R[:, 0].mean()), se_p(D / Nn))
    rec("Q2b", "N=%d D=%d" % (Nn, D), Fr(D, Nn), b, float(R[:, 1].mean()), se_p(D / Nn))
    rec("Q2c", "N=%d D=%d" % (Nn, D), Fr(D, Nn), c, float(R[:, 2].mean()), se_p(D / Nn))
    n2m = int(R[:, 1].sum())
    rec("Q2d", "N=%d D=%d" % (Nn, D), Fr(D - 1, Nn - 1), d, float((R[:, 1] & R[:, 2]).sum() / n2m),
        math.sqrt((D - 1) / (Nn - 1) * (1 - (D - 1) / (Nn - 1)) / n2m))

# ============================================================ Q3 (two distinct digits 1..9, XY = 10X+Y)
pairs = [(a, b) for a in range(1, 10) for b in range(1, 10) if a != b]
num = [10 * a + b for a, b in pairs]
tot = len(pairs)
G = rng.integers(1, 10, (N, 2))
while True:
    bad = G[:, 0] == G[:, 1]
    if not bad.any():
        break
    G[bad, 1] = rng.integers(1, 10, int(bad.sum()))
Num = 10 * G[:, 0] + G[:, 1]
rec("Q3a", "P(even)", Fr(4, 9), Fr(sum(n % 2 == 0 for n in num), tot), float(np.mean(Num % 2 == 0)), se_p(4 / 9))
rec("Q3b", "P(div by 3)", Fr(1, 3), Fr(sum(n % 3 == 0 for n in num), tot), float(np.mean(Num % 3 == 0)), se_p(1 / 3))
rec("Q3c", "P(div by 5)", Fr(1, 9), Fr(sum(n % 5 == 0 for n in num), tot), float(np.mean(Num % 5 == 0)), se_p(1 / 9))
oddsum = [(a, b) for a, b in pairs if (a + b) % 2 == 1]
ex3d = Fr(sum(b % 2 == 0 for a, b in oddsum), len(oddsum))
Sodd = (G.sum(axis=1) % 2 == 1)
mc3d = float(np.mean(Num[Sodd] % 2 == 0)); nS = int(Sodd.sum())
off3d = Fr(5, 9)
d_ex = (off3d == ex3d)
d_mc = abs(mc3d - float(off3d)) <= 4 * math.sqrt(.25 / nS)
print("Q3d: odd-sum pairs=%d, with even number=%d, exact=%s official=%s mc=%.6f" % (
    len(oddsum), sum(b % 2 == 0 for a, b in oddsum), ex3d, off3d, mc3d))

# ============================================================ Q4
z = sp.symbols("z", real=True)
a_, b_ = sp.symbols("a b", positive=True)
tot_area = a_ + (b_ - a_)
sol = sp.solve([sp.Eq(tot_area, 1), sp.Eq(sp.integrate(z, (z, a_, b_)), sp.Rational(4, 9))], [a_, b_], dict=True)
rows.append(("Q4a", "sympy solve gives a=1/3, b=1", len(sol) == 1 and sol[0][a_] == sp.Rational(1, 3) and sol[0][b_] == 1, True, str(sol)))
# sampler: triangle mass 1/3 (density 1-3|z| on |z|<1/3), flat mass 2/3 on (1/3,1)
u = rng.random(N)
tri = u < 1 / 3
# |z| ~ density 6(1-3s) on (0,1/3): cdf 6s-9s^2 -> s = (1 - sqrt(1-w))/3
s = (1 - np.sqrt(1 - rng.random(N))) / 3
Zs = np.where(tri, np.where(rng.random(N) < .5, -s, s), 1 / 3 + (2 / 3) * rng.random(N))


def F_off(t):
    if t < -1 / 3: return 0.0
    if t < 0: return (1 + 3 * t) ** 2 / 6
    if t < 1 / 3: return 1 / 3 - (1 - 3 * t) ** 2 / 6
    return t if t < 1 else 1.0


def F_exact(t):
    t = sp.nsimplify(t)
    fz = lambda zz: 1 - 3 * abs(zz) if abs(zz) < sp.Rational(1, 3) else 0
    tot = 0
    if t > -sp.Rational(1, 3):
        tot += sp.integrate(3 * z + 1, (z, -sp.Rational(1, 3), min(t, 0)))
    if t > 0:
        tot += sp.integrate(1 - 3 * z, (z, 0, min(t, sp.Rational(1, 3))))
    if t > sp.Rational(1, 3):
        tot += sp.integrate(sp.Integer(1), (z, sp.Rational(1, 3), min(t, 1)))
    return float(tot)


for t in (-.2, -.05, .1, .3, .6, 1.5):
    rec("Q4b", "F_Z(%.2f)" % t, F_off(t), F_exact(t), float(np.mean(Zs <= t)), se_p(F_off(t)), tol=1e-9)
rec("Q4a", "E[Z]=4/9 (MC)", Fr(4, 9), Fr(4, 9), float(Zs.mean()), float(Zs.std() / math.sqrt(N)))
sel = np.abs(Zs) < .75
cc = float(np.mean((Zs > .25) & sel) / np.mean(sel))
exc = Fr(41, 72)
rec("Q4c", "P(Z>1/4 | |Z|<3/4)", Fr(41, 72), (Fr(3, 4) - Fr(31, 96)) / Fr(3, 4), cc, math.sqrt(41 / 72 * 31 / 72 / int(sel.sum())))

# ============================================================ Q5
Qb = Fr(1, 365)
for (Nn, p) in ((6, Fr(3, 5)), (8, Fr(1, 4))):
    # exact joint over (X=j, Y=k)
    joint = {}
    for j in range(Nn + 1):
        pj = math.comb(Nn, j) * p ** j * (1 - p) ** (Nn - j)
        for k in range(j + 1):
            joint[(j, k)] = pj * math.comb(j, k) * Qb ** k * (1 - Qb) ** (j - k)
    # MC with a large birthday probability to get statistical power (formula is symbolic in Q)
for (Nn, p, Q) in ((6, Fr(3, 5), Fr(1, 5)), (8, Fr(1, 4), Fr(1, 3)), (5, Fr(7, 10), Fr(1, 365))):
    joint = {}
    for j in range(Nn + 1):
        pj = math.comb(Nn, j) * p ** j * (1 - p) ** (Nn - j)
        for k in range(j + 1):
            joint[(j, k)] = pj * math.comb(j, k) * Q ** k * (1 - Q) ** (j - k)
    Xs = rng.binomial(Nn, float(p), N)
    Ys = rng.binomial(Xs, float(Q))
    for k in range(Nn + 1):
        off = math.comb(Nn, k) * (p * Q) ** k * (1 - p * Q) ** (Nn - k)
        ex = sum(v for (j, kk), v in joint.items() if kk == k)
        rec("Q5b", "P(Y=%d) N=%d p=%s Q=%s" % (k, Nn, p, Q), off, ex, float(np.mean(Ys == k)), se_p(float(off)))
    rows.append(("Q5a", "X~Bin(N,p) pmf sums to 1 N=%d" % Nn, sum(math.comb(Nn, k) * p ** k * (1 - p) ** (Nn - k) for k in range(Nn + 1)) == 1, True, ""))
    pt = (1 - p) / (1 - p * Q)
    for k in range(0, Nn + 1):
        pk = sum(v for (j, kk), v in joint.items() if kk == k)
        if pk == 0 or float(pk) < 1e-3:
            continue
        nk = int(np.sum(Ys == k))
        for n in range(k, Nn + 1):
            off = math.comb(Nn - k, Nn - n) * pt ** (Nn - n) * (1 - pt) ** (n - k)
            ex = joint[(n, k)] / pk
            mc = float(np.sum((Xs == n) & (Ys == k)) / nk)
            rec("Q5c", "P(X=%d|Y=%d) N=%d p=%s Q=%s" % (n, k, Nn, p, Q), off, ex, mc,
                math.sqrt(max(float(off) * (1 - float(off)), 1e-12) / nk), tol=1e-12)

# ============================================================ Q6
def q1w(s):
    A, B, C, D, E = s
    return bool((A and B) or (C and D) or (E and ((A and D) or (C and B))))


def q2w(s):
    A, B, C, D, E = s
    return bool((A or B) and (C or D or E))


for p in (Fr(1, 2), Fr(7, 10), Fr(3, 10)):
    P1 = P2 = P12 = Fr(0)
    for s in itertools.product((0, 1), repeat=5):
        w = Fr(1)
        for v in s:
            w *= p if v else 1 - p
        P1 += w * q1w(s); P2 += w * q2w(s); P12 += w * (q1w(s) and q2w(s))
    off1 = p ** 2 * (2 + 2 * p - 5 * p ** 2 + 2 * p ** 3)
    off2 = 6 * p ** 2 - 9 * p ** 3 + 5 * p ** 4 - p ** 5
    off12 = 3 * p ** 5 - 9 * p ** 4 + 7 * p ** 3
    off3 = p * (7 - 9 * p + 3 * p ** 2) / (6 - 9 * p + 5 * p ** 2 - p ** 3)
    S = rng.random((N, 5)) < float(p)
    A, B, C, D, E = S.T
    m1 = (A & B) | (C & D) | (E & ((A & D) | (C & B)))
    m2 = (A | B) & (C | D | E)
    rec("Q6a", "P(Q1) p=%s" % p, off1, P1, float(m1.mean()), se_p(float(off1)))
    rec("Q6b", "P(Q2) p=%s" % p, off2, P2, float(m2.mean()), se_p(float(off2)))
    rows.append(("Q6c", "P(Q1 and Q2) = 3p^5-9p^4+7p^3 p=%s" % p, off12 == P12, abs(float((m1 & m2).mean()) - float(off12)) <= 4 * se_p(float(off12)), ""))
    rec("Q6c", "P(Q1|Q2) p=%s" % p, off3, P12 / P2, float((m1 & m2).sum() / m2.sum()), math.sqrt(float(off3) * (1 - float(off3)) / int(m2.sum())))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("Q3d HOLD: official 5/9 vs exact %s: exact-match=%s mc-match=%s (expected: both False)" % (ex3d, d_ex, d_mc))
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if (not bad and not d_ex and not d_mc and ex3d == Fr(1, 2)) else 1)
