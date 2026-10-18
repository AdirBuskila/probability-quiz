# -*- coding: utf-8 -*-
"""Verification harness for 24S-A (probability). Run: PYTHONUTF8=1 py tools/verify/24S-A/check.py

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
rng = np.random.default_rng(20241014)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1
X = rng.random(N); Y = rng.random(N)
L1 = np.sqrt(X ** 2 + Y ** 2)
ex = integrate.quad(lambda x: math.sqrt(max(0.0, 1 - x * x)), 0, 1)[0]
rec("Q1b", "P(L<1) = pi/4", math.pi / 4, ex, float(np.mean(L1 < 1)), se_p(math.pi / 4), tol=1e-9)
ex = integrate.quad(lambda x: math.sqrt(max(0.0, 1 - x * x)) - math.sqrt(max(0.0, 0.25 - x * x)), 0, 1)[0]
rec("Q1b", "P(1/2<L<1) = 3pi/16", 3 * math.pi / 16, ex, float(np.mean((L1 > .5) & (L1 < 1))), se_p(3 * math.pi / 16), tol=1e-9)
L2 = np.sqrt(1 + (X - Y) ** 2)
ex = integrate.dblquad(lambda y, x: 1.0 if abs(x - y) < 1 / 3 else 0.0, 0, 1, 0, 1, epsabs=1e-4)[0]
rec("Q1c", "P(L<sqrt(10)/3) = 5/9", Fr(5, 9), Fr(1) - 2 * Fr(1, 2) * Fr(2, 3) ** 2, float(np.mean(L2 < math.sqrt(10) / 3)), se_p(5 / 9))
rows.append(("Q1c", "quadrature of |x-y|<1/3 ~ 5/9", abs(ex - 5 / 9) < 3e-3, True, "quad=%.5f" % ex))

# ============================================================ Q2
# a: P(partial sums ever hit 5): exact recursion h(s) = 1/6 sum h(s+d), h(5)=1, h(s>5)=0
from functools import lru_cache


@lru_cache(None)
def hit(s):
    if s == 5: return Fr(1)
    if s > 5: return Fr(0)
    return sum(hit(s + d) for d in range(1, 7)) / 6


rolls = rng.integers(1, 7, (N, 5))
cs = np.cumsum(rolls, axis=1)
mc_a = float(np.mean((cs == 5).any(axis=1)))
rec("Q2a", "P(ever sum 5) = 7^4/6^5", Fr(7 ** 4, 6 ** 5), hit(0), mc_a, se_p(7 ** 4 / 6 ** 5))
two = list(itertools.product(range(1, 7), repeat=2)); three = list(itertools.product(range(1, 7), repeat=3))
rec("Q2b", "P(sum of 2 = 5)", Fr(1, 9), Fr(sum(a + b == 5 for a, b in two), 36), float(np.mean(cs[:, 1] == 5)), se_p(1 / 9))
rec("Q2c", "P(sum of 3 = 5)", Fr(1, 36), Fr(sum(sum(t) == 5 for t in three), 216), float(np.mean(cs[:, 2] == 5)), se_p(1 / 36))
D = [t for t in three if t[0] + t[1] == 3]
ex = Fr(sum(sum(t) == 5 for t in D), len(D))
selD = cs[:, 1] == 3
rec("Q2d", "P(sum3=5 | first two sum 3)", Fr(1, 6), ex, float(np.mean(cs[selD, 2] == 5)), math.sqrt(1 / 6 * 5 / 6 / int(selD.sum())))

# ============================================================ Q3
for p in (Fr(3, 10), Fr(1, 2), Fr(4, 5)):
    pf = float(p)
    T = rng.random((N, 3)) < pf
    Xs = T[:, 0].astype(int) + T[:, 1]; Ys = T[:, 1].astype(int) + T[:, 2]
    joint = {}
    for bits in itertools.product((0, 1), repeat=3):
        w = Fr(1)
        for b in bits:
            w *= p if b else 1 - p
        k = (bits[0] + bits[1], bits[1] + bits[2])
        joint[k] = joint.get(k, Fr(0)) + w
    off = {(0, 0): (1 - p) ** 3, (0, 1): p * (1 - p) ** 2, (0, 2): Fr(0), (1, 0): p * (1 - p) ** 2, (1, 1): p * (1 - p),
           (1, 2): p ** 2 * (1 - p), (2, 0): Fr(0), (2, 1): p ** 2 * (1 - p), (2, 2): p ** 3}
    for k, v in off.items():
        rec("Q3a", "P_XY%s p=%s" % (k, p), v, joint.get(k, 0), float(np.mean((Xs == k[0]) & (Ys == k[1]))), se_p(float(v)))
    rows.append(("Q3a", "joint sums to 1 p=%s" % p, sum(off.values()) == 1, True, ""))
    for x in range(3):
        offm = math.comb(2, x) * p ** x * (1 - p) ** (2 - x)
        exm = sum(v for (a, b), v in joint.items() if a == x); eym = sum(v for (a, b), v in joint.items() if b == x)
        rec("Q3b", "P_X(%d) p=%s" % (x, p), offm, exm, float(np.mean(Xs == x)), se_p(float(offm)))
        rec("Q3b", "P_Y(%d) p=%s" % (x, p), offm, eym, float(np.mean(Ys == x)), se_p(float(offm)))
    EX = sum(a * v for (a, b), v in joint.items()); VX = sum(a * a * v for (a, b), v in joint.items()) - EX ** 2
    rec("Q3c", "E[X] p=%s" % p, 2 * p, EX, float(Xs.mean()), float(Xs.std() / math.sqrt(N)))
    rec("Q3c", "Var[X] p=%s" % p, 2 * p * (1 - p), VX, float(Xs.var()), float(Xs.var() * math.sqrt(2 / N)) * 2)
    rows.append(("Q3d", "dependent: P(2,0)=0 != P_X(2)P_Y(0)>0 p=%s" % p, joint.get((2, 0), 0) == 0 and p ** 2 * (1 - p) ** 2 > 0, True, ""))

# ============================================================ Q4
x = sp.symbols("x", real=True)
a_, b_ = sp.symbols("a b", positive=True)
sol = sp.solve([sp.Eq(a_ + sp.integrate(b_ * sp.exp(-x), (x, 0, sp.oo)), 1),
                sp.Eq(sp.integrate(a_ * x, (x, -1, 0)) + sp.integrate(b_ * x * sp.exp(-x), (x, 0, sp.oo)), 0)], [a_, b_], dict=True)
rows.append(("Q4a", "sympy: a=2/3, b=1/3", len(sol) == 1 and sol[0][a_] == sp.Rational(2, 3) and sol[0][b_] == sp.Rational(1, 3), True, str(sol)))
u = rng.random(N)
Xs4 = np.where(u < 2 / 3, -1 + rng.random(N), rng.exponential(1.0, N))


def F_off(t):
    return 0.0 if t < -1 else (2 / 3 * (t + 1) if t < 0 else 1 - math.exp(-t) / 3)


for t in (-.7, -.2, 0.0, .5, 1.0, 3.0):
    tt = sp.nsimplify(t)
    ex = float((sp.integrate(sp.Rational(2, 3), (x, -1, min(tt, 0))) if tt > -1 else 0) + (sp.integrate(sp.Rational(1, 3) * sp.exp(-x), (x, 0, tt)) if tt > 0 else 0))
    rec("Q4b", "F_X(%.1f)" % t, F_off(t), ex, float(np.mean(Xs4 <= t)), se_p(F_off(t)), tol=1e-9)
rec("Q4a", "E[X]=0 (MC)", 0, 0, float(Xs4.mean()), float(Xs4.std() / math.sqrt(N)))
sel = Xs4 < 1
off = (2 * math.e - 1) / (3 * math.e - 1)
cc = float(np.mean((Xs4 > -.5) & sel) / np.mean(sel))
ex = float(((sp.integrate(sp.Rational(2, 3), (x, -sp.Rational(1, 2), 0)) + sp.integrate(sp.Rational(1, 3) * sp.exp(-x), (x, 0, 1))) /
            (sp.integrate(sp.Rational(2, 3), (x, -1, 0)) + sp.integrate(sp.Rational(1, 3) * sp.exp(-x), (x, 0, 1)))).evalf(30))
rec("Q4c", "P(X>-1/2 | X<1) = (2e-1)/(3e-1)", off, ex, cc, math.sqrt(off * (1 - off) / int(sel.sum())), tol=1e-12)

# ============================================================ Q5
for (Nn, p, Q) in ((6, Fr(3, 5), Fr(1, 5)), (8, Fr(1, 4), Fr(1, 3)), (5, Fr(7, 10), Fr(1, 365))):
    joint = {}
    for j in range(Nn + 1):
        pj = math.comb(Nn, j) * p ** j * (1 - p) ** (Nn - j)
        for k in range(j + 1):
            joint[(j, k)] = pj * math.comb(j, k) * Q ** k * (1 - Q) ** (j - k)
    Xs = rng.binomial(Nn, float(p), N); Ys = rng.binomial(Xs, float(Q))
    # also the alternative solution: per-student Bernoulli product
    arrive = rng.random((N, Nn)) < float(p); born = rng.random((N, Nn)) < float(Q)
    Yalt = (arrive & born).sum(axis=1)
    for k in range(Nn + 1):
        off = math.comb(Nn, k) * (p * Q) ** k * (1 - p * Q) ** (Nn - k)
        ex = sum(v for (j, kk), v in joint.items() if kk == k)
        rec("Q5b", "P(Y=%d) N=%d p=%s Q=%s" % (k, Nn, p, Q), off, ex, float(np.mean(Ys == k)), se_p(float(off)))
        rec("Q5b", "alt solution P(Y=%d) N=%d" % (k, Nn), off, ex, float(np.mean(Yalt == k)), se_p(float(off)))
    rows.append(("Q5a", "X~Bin(N,p) sums to 1 N=%d" % Nn, sum(math.comb(Nn, k) * p ** k * (1 - p) ** (Nn - k) for k in range(Nn + 1)) == 1, True, ""))
    pt = (1 - p) / (1 - p * Q)
    for k in range(0, Nn + 1):
        pk = sum(v for (j, kk), v in joint.items() if kk == k)
        if float(pk) < 1e-3:
            continue
        nk = int(np.sum(Ys == k))
        for n in range(k, Nn + 1):
            off = math.comb(Nn - k, Nn - n) * pt ** (Nn - n) * (1 - pt) ** (n - k)
            ex = joint[(n, k)] / pk
            rec("Q5c", "P(X=%d|Y=%d) N=%d p=%s Q=%s" % (n, k, Nn, p, Q), off, ex, float(np.sum((Xs == n) & (Ys == k)) / nk),
                math.sqrt(max(float(off) * (1 - float(off)), 1e-12) / nk))

# ============================================================ Q6 (graph: l,r,t,c; A l-t, C t-r, B t-c, D l-c, E c-r, F l-r)
edges = {"A": ("l", "t"), "C": ("t", "r"), "B": ("t", "c"), "D": ("l", "c"), "E": ("c", "r"), "F": ("l", "r")}
names = "ABCDEF"


def conn(state):
    par = {v: v for v in "ltrc"}

    def find(v):
        while par[v] != v:
            v = par[v]
        return v
    for nme, up in zip(names, state):
        if up:
            a, b = edges[nme]; par[find(a)] = find(b)
    return find("l") == find("r")


for p in (Fr(1, 2), Fr(7, 10), Fr(3, 10)):
    PQ = PBbarQ = PAll = Fr(0); PQ_B = PQ_nB = Fr(0)
    for s in itertools.product((0, 1), repeat=6):
        w = Fr(1)
        for v in s:
            w *= p if v else 1 - p
        if conn(s):
            PQ += w
            if not s[1]: PBbarQ += w
            if all(s): PAll += w
    PQgB = sum(math.prod([p if v else 1 - p for v in s]) for s in itertools.product((0, 1), repeat=6) if s[1] and conn(s)) / p
    PQgnB = sum(math.prod([p if v else 1 - p for v in s]) for s in itertools.product((0, 1), repeat=6) if (not s[1]) and conn(s)) / (1 - p)
    offQ = p * (1 + 2 * p - 7 * p ** 3 + 7 * p ** 4 - 2 * p ** 5)
    offQgB = p + 4 * p ** 2 - 8 * p ** 3 + 5 * p ** 4 - p ** 5
    offQgnB = p + 2 * p ** 2 - 2 * p ** 3 - p ** 4 + p ** 5
    offb = (1 + p - 4 * p ** 2 + p ** 3 + 2 * p ** 4 - p ** 5) / (1 + 2 * p - 7 * p ** 3 + 7 * p ** 4 - 2 * p ** 5)
    offd = p ** 5 / (1 + 2 * p - 7 * p ** 3 + 7 * p ** 4 - 2 * p ** 5)
    S = rng.random((N, 6)) < float(p)
    Aa, Bb, Cc, Dd, Ee, Ff = S.T
    mq = (Ff | (np.where(Bb, (Aa | Dd) & (Cc | Ee), (Aa & Cc) | (Dd & Ee))))
    # independent check of the structure: connectivity via union-find on a subset sample
    sub = S[:20000]
    mq_sub = np.array([conn(tuple(int(v) for v in r)) for r in sub])
    rows.append(("Q6a", "vectorised structure == union-find on 20000 samples p=%s" % p, bool((mq_sub == mq[:20000]).all()), True, ""))
    rec("Q6a", "P(Q) p=%s" % p, offQ, PQ, float(mq.mean()), se_p(float(offQ)))
    rec("Q6a", "P(Q|B) p=%s" % p, offQgB, PQgB, float(mq[Bb].mean()), se_p(float(offQgB), int(Bb.sum())))
    rec("Q6a", "P(Q|not B) p=%s" % p, offQgnB, PQgnB, float(mq[~Bb].mean()), se_p(float(offQgnB), int((~Bb).sum())))
    rec("Q6b", "P(not B|Q) p=%s" % p, offb, PBbarQ / PQ, float((mq & ~Bb).sum() / mq.sum()), math.sqrt(float(offb) * (1 - float(offb)) / int(mq.sum())))
    rows.append(("Q6c", "every single-failure state works p=%s" % p, all(conn(s) for s in itertools.product((0, 1), repeat=6) if sum(s) == 5), True, ""))
    rec("Q6d", "P(all work|Q) p=%s" % p, offd, PAll / PQ, float((mq & S.all(axis=1)).sum() / mq.sum()), math.sqrt(float(offd) * (1 - float(offd)) / int(mq.sum())))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if not bad else 1)
