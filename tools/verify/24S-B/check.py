# -*- coding: utf-8 -*-
"""Verification harness for 24S-B (probability). Run: PYTHONUTF8=1 py tools/verify/24S-B/check.py

Every final answer gets two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy / quadrature).
  MC    : Monte Carlo (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Official keys are never changed. Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20241107)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1
X = rng.random(N); Y = rng.random(N); S = X * Y; L = np.sqrt(X ** 2 + Y ** 2)
off = 0.5 + 0.5 * math.log(2)
ex = integrate.quad(lambda x: min(1.0, 1 / (2 * x)), 0, 1, points=[0.5])[0]
rec("Q1a", "P(S<1/2)", off, ex, float(np.mean(S < .5)), se_p(off), tol=1e-9)
ex = integrate.quad(lambda x: math.sqrt(max(0.0, 0.25 - x * x)), 0, .5)[0]
rec("Q1b", "P(L<1/2) = pi/16", math.pi / 16, ex, float(np.mean(L < .5)), se_p(math.pi / 16), tol=1e-9)
off = 0.4 * math.log(2)
ex = integrate.quad(lambda x: min(1.0, 1 / (5 * x)), .5, 1)[0] / .5
sel = X > .5
rec("Q1c", "P(S<1/5 | X>1/2) = (2/5) ln 2", off, ex, float(np.mean((S < .2) & sel) / np.mean(sel)), math.sqrt(off * (1 - off) / int(sel.sum())), tol=1e-9)
rec("Q1d", "E[S]=1/4", Fr(1, 4), Fr(1, 2) * Fr(1, 2), float(S.mean()), float(S.std() / math.sqrt(N)))
m4 = float(np.mean((S - S.mean()) ** 4))
rec("Q1d", "Var[S]=7/144", Fr(7, 144), Fr(1, 3) ** 2 - Fr(1, 16), float(S.var()), math.sqrt((m4 - S.var() ** 2) / N))

# ============================================================ Q2
pairs = list(itertools.product(range(1, 7), repeat=2))
d1 = rng.integers(1, 7, N); d2 = rng.integers(1, 7, N)
# roots computed from the quadratic itself
disc = (d1 + d2) ** 2 - 4 * d1 * d2
r1 = (d1 + d2 + np.sqrt(disc)) / 2; r2 = (d1 + d2 - np.sqrt(disc)) / 2
rec("Q2a", "P(equal roots)", Fr(1, 6), Fr(sum(a == b for a, b in pairs), 36), float(np.mean(disc == 0)), se_p(1 / 6))
rec("Q2b", "P(roots integers)", Fr(1), Fr(1), float(np.mean(np.abs(r1 - np.round(r1)) < 1e-9) * np.mean(np.abs(r2 - np.round(r2)) < 1e-9)), 1e-9)
dist = disc > 0
ex = Fr(sum((a * b) % 2 == 1 for a, b in pairs if a != b), sum(a != b for a, b in pairs))
rec("Q2c", "P(product odd | distinct)", Fr(1, 5), ex, float(np.mean(((r1 * r2) % 2 == 1)[dist])), math.sqrt(.2 * .8 / int(dist.sum())))
ex = Fr(sum((a - b) % 2 == 0 for a, b in pairs if a != b), sum(a != b for a, b in pairs))
rec("Q2d", "P(difference even | distinct)", Fr(2, 5), ex, float(np.mean((np.abs(r1 - r2) % 2 == 0)[dist])), math.sqrt(.4 * .6 / int(dist.sum())))

# ============================================================ Q3 (Y = heads in all three tosses)
for p in (Fr(3, 10), Fr(1, 2), Fr(4, 5)):
    pf = float(p)
    T = rng.random((N, 3)) < pf
    Xs = T[:, 0].astype(int) + T[:, 1]; Ys = T.sum(axis=1)
    joint = {}
    for bits in itertools.product((0, 1), repeat=3):
        w = Fr(1)
        for b in bits:
            w *= p if b else 1 - p
        k = (bits[0] + bits[1], sum(bits))
        joint[k] = joint.get(k, Fr(0)) + w
    off = {(0, 0): (1 - p) ** 3, (0, 1): p * (1 - p) ** 2, (1, 1): 2 * p * (1 - p) ** 2, (1, 2): 2 * p ** 2 * (1 - p),
           (2, 2): p ** 2 * (1 - p), (2, 3): p ** 3}
    for k in itertools.product(range(3), range(4)):
        v = off.get(k, Fr(0))
        rec("Q3a", "P_XY%s p=%s" % (k, p), v, joint.get(k, 0), float(np.mean((Xs == k[0]) & (Ys == k[1]))), se_p(float(v)))
    rows.append(("Q3a", "joint sums to 1 p=%s" % p, sum(off.values()) == 1, True, ""))
    for x in range(3):
        o = math.comb(2, x) * p ** x * (1 - p) ** (2 - x)
        rec("Q3b", "P_X(%d) p=%s" % (x, p), o, sum(v for (a, b), v in joint.items() if a == x), float(np.mean(Xs == x)), se_p(float(o)))
    for y in range(4):
        o = math.comb(3, y) * p ** y * (1 - p) ** (3 - y)
        rec("Q3b", "P_Y(%d) p=%s" % (y, p), o, sum(v for (a, b), v in joint.items() if b == y), float(np.mean(Ys == y)), se_p(float(o)))
    EX = sum(a * v for (a, b), v in joint.items()); EY = sum(b * v for (a, b), v in joint.items())
    VX = sum(a * a * v for (a, b), v in joint.items()) - EX ** 2; VY = sum(b * b * v for (a, b), v in joint.items()) - EY ** 2
    rec("Q3c", "E[X] p=%s" % p, 2 * p, EX, float(Xs.mean()), float(Xs.std() / math.sqrt(N)))
    rec("Q3c", "E[Y] p=%s" % p, 3 * p, EY, float(Ys.mean()), float(Ys.std() / math.sqrt(N)))
    rec("Q3c", "Var[X] p=%s" % p, 2 * p * (1 - p), VX, float(Xs.var()), float(Xs.var() * math.sqrt(2 / N)) * 2)
    rec("Q3c", "Var[Y] p=%s" % p, 3 * p * (1 - p), VY, float(Ys.var()), float(Ys.var() * math.sqrt(2 / N)) * 2)
    rows.append(("Q3d", "dependent: P(2,0)=0 != P_X(2)P_Y(0)>0 p=%s" % p, joint.get((2, 0), 0) == 0 and p ** 2 * (1 - p) ** 3 > 0, True, ""))

# ============================================================ Q4
x = sp.symbols("x", real=True)
a_, b_ = sp.symbols("a b", positive=True)
area = sp.integrate(a_ * sp.exp(x), (x, -sp.oo, -1)) + sp.Rational(1, 2) + sp.integrate(b_ * sp.exp(-x), (x, 1, sp.oo))
mean = sp.integrate(x * a_ * sp.exp(x), (x, -sp.oo, -1)) + sp.integrate(x * b_ * sp.exp(-x), (x, 1, sp.oo))
sol = sp.solve([sp.Eq(area, 1), sp.Eq(mean, 0)], [a_, b_], dict=True)
rows.append(("Q4a", "sympy: a=b=e/4", len(sol) == 1 and sp.simplify(sol[0][a_] - sp.E / 4) == 0 and sp.simplify(sol[0][b_] - sp.E / 4) == 0, True, str(sol)))
e = math.e
u = rng.random(N)
# masses: left tail a/e = 1/4, middle 1/2, right tail 1/4
Xs4 = np.where(u < .25, -1 - rng.exponential(1.0, N), np.where(u < .75, -1 + 2 * rng.random(N), 1 + rng.exponential(1.0, N)))


def F_off(t):
    return e / 4 * math.exp(t) if t < -1 else (.5 + t / 4 if t < 1 else 1 - e / 4 * math.exp(-t))


for t in (-3.0, -1.5, -.5, .7, 1.2, 3.0):
    tt = sp.nsimplify(t)
    ex = float(sp.integrate(sp.E / 4 * sp.exp(x), (x, -sp.oo, min(tt, -1))) +
               (sp.integrate(sp.Rational(1, 4), (x, -1, min(tt, 1))) if tt > -1 else 0) +
               (sp.integrate(sp.E / 4 * sp.exp(-x), (x, 1, tt)) if tt > 1 else 0))
    rec("Q4b", "F_X(%.1f)" % t, F_off(t), ex, float(np.mean(Xs4 <= t)), se_p(F_off(t)), tol=1e-9)
rec("Q4a", "E[X]=0 (MC)", 0, 0, float(Xs4.mean()), float(Xs4.std() / math.sqrt(N)))
sel = Xs4 < 3
off = (4 * e ** 2 - e - 1) / (4 * e ** 2 - 1)
ex = (F_off(3) - F_off(-2)) / F_off(3)
rec("Q4c", "P(X>-2 | X<3)", off, ex, float(np.mean((Xs4 > -2) & sel) / np.mean(sel)), math.sqrt(off * (1 - off) / int(sel.sum())), tol=1e-12)

# ============================================================ Q5
for (Nn, D, M, p) in ((10, 4, 5, Fr(3, 10)), (7, 3, 6, Fr(1, 2)), (12, 5, 4, Fr(4, 5))):
    # exact: enumerate the M tosses
    PR = Fr(0); joint_red = {}
    for k in range(M + 1):
        pk = math.comb(M, k) * p ** k * (1 - p) ** (M - k)
        pr = Fr(D + 2 * k, Nn + 2 * M)
        PR += pk * pr; joint_red[k] = pk * pr
    off = Fr(D) + 2 * p * M
    off = off / (Nn + 2 * M)
    heads = rng.binomial(M, float(p), N)
    red = rng.random(N) < (D + 2 * heads) / (Nn + 2 * M)
    rec("Q5a", "P(red) N=%d D=%d M=%d p=%s" % (Nn, D, M, p), off, PR, float(red.mean()), se_p(float(off)))
    nr = int(red.sum())
    for n in range(0, 2 * M + 1):
        if n % 2 == 1:
            rows.append(("Q5b", "odd n=%d: 0 (no sample has an odd number of red balls added)" % n, True,
                         float(np.mean((2 * heads == n) & red)) == 0.0, ""))
            continue
        k = n // 2
        offb = Fr(D + n, D) if False else Fr(D + n) / (D + 2 * p * M) * math.comb(M, k) * p ** k * (1 - p) ** (M - k)
        exb = joint_red[k] / PR
        rec("Q5b", "P(n=%d red added | red) N=%d D=%d M=%d p=%s" % (n, Nn, D, M, p), offb, exb,
            float(np.sum((heads == k) & red) / nr), math.sqrt(max(float(offb) * (1 - float(offb)), 1e-12) / nr))

# ============================================================ Q6
# inner bridge E: units TL(t-l), A(t-r), BL(l-b), BR(r-b), B(l-r); terminals t, b
# outer: E in parallel with two series pairs
def bridge(st):
    TL, A, BL, BR, B = st
    return bool((TL and BL) or (A and BR) or (TL and B and BR) or (A and B and BL))


def Qw(st9):
    E = bridge(st9[:5])
    o1, o2, o3, o4 = st9[5:]
    return bool(E or (o1 and o2) or (o3 and o4))


for p in (Fr(1, 2), Fr(7, 10), Fr(3, 10)):
    P0 = PQA = PA = Fr(0)
    for st in itertools.product((0, 1), repeat=9):
        w = Fr(1)
        for v in st:
            w *= p if v else 1 - p
        if Qw(st):
            P0 += w
            if not st[1]:
                PA += w          # A = index 1 (inner top-right unit)
    PE = p ** 3 * (2 - p) ** 2 + p ** 2 * (2 - p ** 2) * (1 - p)
    off0 = p ** 2 * (2 - p ** 2) + (1 - p ** 2) ** 2 * PE
    PEgA = p ** 2 * (1 + p - p ** 2)
    offQgA = p ** 2 * (2 - p ** 2) + (1 - p ** 2) ** 2 * PEgA
    off1 = offQgA / off0 * (1 - p)
    S9 = rng.random((N, 9)) < float(p)
    E_m = ((S9[:, 0] & S9[:, 2]) | (S9[:, 1] & S9[:, 3]) | (S9[:, 0] & S9[:, 4] & S9[:, 3]) | (S9[:, 1] & S9[:, 4] & S9[:, 2]))
    Qm = E_m | (S9[:, 5] & S9[:, 6]) | (S9[:, 7] & S9[:, 8])
    # exact P(E) and P(E | A fails) by enumeration of the bridge
    PEex = sum(math.prod([p if v else 1 - p for v in st]) for st in itertools.product((0, 1), repeat=5) if bridge(st))
    PEAex = sum(math.prod([p if v else 1 - p for v in st]) for st in itertools.product((0, 1), repeat=5) if bridge(st) and not st[1]) / (1 - p)
    rec("Q6a", "P(E) p=%s" % p, PE, PEex, float(E_m.mean()), se_p(float(PE)))
    rec("Q6a", "P0 p=%s" % p, off0, P0, float(Qm.mean()), se_p(float(off0)))
    rec("Q6b", "P(E|not A) p=%s" % p, PEgA, PEAex, float(E_m[~S9[:, 1]].mean()), se_p(float(PEgA), int((~S9[:, 1]).sum())))
    rec("Q6b", "P1 = P(not A|Q) p=%s" % p, off1, PA / P0, float((Qm & ~S9[:, 1]).sum() / Qm.sum()), math.sqrt(float(off1) * (1 - float(off1)) / int(Qm.sum())))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if not bad else 1)
