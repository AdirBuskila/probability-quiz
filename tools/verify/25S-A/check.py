# -*- coding: utf-8 -*-
"""Verification harness for 25S-A (probability). Run: PYTHONUTF8=1 py tools/verify/25S-A/check.py
Each final answer: EXACT (fractions / enumeration / sympy) and MC (>= 10^6 trials, within 4 SE). ASCII output only.
Symbolic answers are checked at sample parameter values (and as polynomial identities with sympy where possible).
Q3 part e (bonus) has no official key: the solver value is only printed, never compared."""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20251020)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se + 1e-12
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


def clip(poly, a, b, c):  # keep a*x+b*y+c >= 0
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * p[0] + b * p[1] + c, a * q[0] + b * q[1] + c
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


# ============================================================ Q1  (X1~U(0,1), X2~U(0,2))
rect = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(1), Fr(2)), (Fr(0), Fr(2))]   # (x1, x2)
X1 = rng.random(N)
X2 = 2 * rng.random(N)
tri_a = clip(rect, Fr(1), Fr(-1), Fr(0))               # x1 > x2
rec("Q1a", "P(X1>X2)=1/4", Fr(1, 4), area(tri_a) / 2, float((X1 > X2).mean()), se_p(0.25), tol=0)
pb = Fr(1, 2) + Fr(1, 4) - Fr(1, 2) * Fr(1, 4)
rec("Q1b", "P(X1<1/2 or X2<1/2)=5/8", Fr(5, 8), pb, float(((X1 < 0.5) | (X2 < 0.5)).mean()), se_p(0.625), tol=0)
# exact for b by area complement: 1 - P(X1>=1/2)P(X2>=1/2)
rows.append(("Q1b", "complement check 1-(1/2)(3/4)=5/8", Fr(5, 8) == 1 - Fr(1, 2) * Fr(3, 4), True, ""))
tri_c = clip(rect, Fr(-1), Fr(-1), Fr(1))              # x1 + x2 <= 1
rec("Q1c", "P(X1+X2<=1)=1/4", Fr(1, 4), area(tri_c) / 2, float((X1 + X2 <= 1).mean()), se_p(0.25), tol=0)
big = clip(rect, Fr(1), Fr(1), Fr(-2))                 # x1 + x2 >= 2
both = clip(big, Fr(1), Fr(0), Fr(-1, 2))              # x1 >= 1/2
ev = (X1 + X2) > 2
rec("Q1d", "P(X1>1/2 | X1+X2>2)=3/4", Fr(3, 4), area(both) / area(big), float((X1[ev] > 0.5).mean()), se_p(0.75, int(ev.sum())), tol=0)

# ============================================================ Q2  (P(A\B)=p, P(A&B)=q, P(A|B)=s)
p, q, s = Fr(1, 5), Fr(3, 20), Fr(1, 2)             # P(B)=q/s=3/10, P(A)=7/20
PB = q / s
pmf = {(1, 1): q, (1, 0): p, (0, 1): PB - q}
pmf[(0, 0)] = 1 - sum(pmf.values())
assert all(v >= 0 for v in pmf.values())
u = rng.random(N)
cum = np.cumsum([float(pmf[k]) for k in ((1, 1), (1, 0), (0, 1), (0, 0))])
idx = np.searchsorted(cum, u)
A = (idx == 0) | (idx == 1)
B = (idx == 0) | (idx == 2)
ex_PA = sum(v for (a, b), v in pmf.items() if a)
ex_PB = sum(v for (a, b), v in pmf.items() if b)
ex_AgNB = pmf[(1, 0)] / (pmf[(1, 0)] + pmf[(0, 0)])
ex_nAgB = pmf[(0, 1)] / (pmf[(0, 1)] + pmf[(1, 1)])
ex_nAgNB = pmf[(0, 0)] / (pmf[(1, 0)] + pmf[(0, 0)])
rec("Q2a", "P(A)=p+q", p + q, ex_PA, float(A.mean()), se_p(float(p + q)), tol=0)
rec("Q2b", "P(B)=q/s", PB, ex_PB, float(B.mean()), se_p(float(PB)), tol=0)
off = p * s / (s - q)
rec("Q2c", "P(A|~B)=ps/(s-q)", off, ex_AgNB, float(A[~B].mean()), se_p(float(off), int((~B).sum())), tol=0)
rec("Q2d", "P(~A|B)=1-s", 1 - s, ex_nAgB, float((~A)[B].mean()), se_p(float(1 - s), int(B.sum())), tol=0)
off = 1 - p * s / (s - q)
rec("Q2e", "P(~A|~B)=1-ps/(s-q)", off, ex_nAgNB, float((~A)[~B].mean()), se_p(float(off), int((~B).sum())), tol=0)
rows.append(("Q2f", "P(B)=q/s<=1 forces q<=s (s<q impossible)", all(not (q_ / s_ <= 1) for q_, s_ in ((Fr(1, 2), Fr(1, 4)),)), True, ""))
# independence iff s = p+q: construct independent pair and compare
pa, pb2 = Fr(2, 5), Fr(1, 3)
pq = pa * pb2
rows.append(("Q2g", "independent case: s=P(A|B)=P(A)=p+q", pa == (pa - pq) + pq and pa == pq / pb2, True, ""))

# ============================================================ Q3  (urn, no replacement)
for Nn, D, nn in ((8, 3, 4), (9, 5, 6), (7, 2, 3), (10, 7, 8)):
    ex_n = Fr(sum(1 for perm in itertools.permutations(range(Nn), nn) if perm[-1] < D), math.perm(Nn, nn))
    draws = np.argsort(rng.random((1_000_000, Nn), dtype=np.float32), axis=1)[:, :nn]
    red = draws < D
    rec("Q3d", "N=%d D=%d n=%d P(R_n)=D/N" % (Nn, D, nn), Fr(D, Nn), ex_n, float(red[:, nn - 1].mean()), se_p(D / Nn, 1_000_000), tol=0)
    if nn >= 3:
        rec("Q3c", "N=%d D=%d P(R_3)=D/N" % (Nn, D), Fr(D, Nn), Fr(sum(1 for perm in itertools.permutations(range(Nn), 3) if perm[2] < D), math.perm(Nn, 3)),
            float(red[:, 2].mean()), se_p(D / Nn, 1_000_000), tol=0)
    rec("Q3b", "N=%d D=%d P(R_2)=D/N" % (Nn, D), Fr(D, Nn), Fr(sum(1 for perm in itertools.permutations(range(Nn), 2) if perm[1] < D), math.perm(Nn, 2)),
        float(red[:, 1].mean()), se_p(D / Nn, 1_000_000), tol=0)
    rec("Q3a", "N=%d D=%d P(R_1)=D/N" % (Nn, D), Fr(D, Nn), Fr(D, Nn), float(red[:, 0].mean()), se_p(D / Nn, 1_000_000), tol=0)
    # bonus (no official key): informational solver value D(D-1)/(N(N-1))
    solver = Fr(D * (D - 1), Nn * (Nn - 1))
    mcb = float((red[:, nn - 1] & red[:, nn - 2]).mean())
    print("INFO Q3e (held, no key) N=%d D=%d n=%d: solver D(D-1)/(N(N-1))=%.6f mc=%.6f" % (Nn, D, nn, float(solver), mcb))

# ============================================================ Q4
a, b, c = sp.symbols("a b c", positive=True)
x = sp.symbols("x")
eq1 = sp.integrate(c * x / (2 * a), (x, 0, a)) - sp.Rational(1, 2)
eq2 = sp.integrate(c, (x, a, b)) - sp.Rational(1, 2)
eq3 = sp.integrate(x * c * x / (2 * a), (x, 0, a)) + sp.integrate(x * c, (x, a, b)) - sp.Rational(43, 48)
sol = sp.solve([eq1, eq2, eq3], [a, b, c], dict=True)
rows.append(("Q4a", "sympy solution a,b,c = %s" % (sol,), sol == [{a: 1, b: sp.Rational(5, 4), c: 2}], True, ""))
half = rng.random(N) < 0.5
Xs = np.where(half, np.sqrt(rng.random(N)), 1 + rng.random(N) / 4)           # pdf x on [0,1), 2 on [1,5/4]
rec("Q4a", "E[X]=43/48", Fr(43, 48), Fr(43, 48), float(Xs.mean()), se_mean(Xs), tol=0)


def F(t):
    return 0.0 if t < 0 else (t * t / 2 if t < 1 else (0.5 + 2 * (t - 1) if t < 1.25 else 1.0))


for t in (0.4, 0.9, 1.1, 1.2):
    ex = float((sp.integrate(x, (x, 0, min(t, 1))) + (sp.integrate(2, (x, 1, t)) if t > 1 else 0)))
    rec("Q4b", "F(%.1f)" % t, F(t), ex, float((Xs <= t).mean()), se_p(F(t)), tol=1e-12)
rec("Q4c", "P(X>1)=1/2", 0.5, 1 - F(1), float((Xs > 1).mean()), se_p(0.5), tol=0)

# ============================================================ Q5  (ring of roads; enumerate 16 states)
pp = sp.symbols("p")


def qe(A, B, C, D):
    return A or (B and C and D)


def qs(A, B, C, D):
    return B or (A and C and D)


def poly_prob(f):
    tot = 0
    for st in itertools.product((0, 1), repeat=4):
        if f(*st):
            k = sum(st)
            tot += pp ** k * (1 - pp) ** (4 - k)
    return sp.expand(tot)


P1 = poly_prob(qe)
P2 = poly_prob(lambda *s_: qe(*s_) and qs(*s_))
P3 = poly_prob(lambda *s_: qe(*s_) and not qs(*s_))
Pall = pp ** 4
rows.append(("Q5a", "P1 = p+p^3-p^4", sp.expand(P1 - (pp + pp ** 3 - pp ** 4)) == 0, True, ""))
rows.append(("Q5b", "P2 = p^2(1+2p-2p^2)", sp.expand(P2 - pp ** 2 * (1 + 2 * pp - 2 * pp ** 2)) == 0, True, ""))
rows.append(("Q5c", "P3 = p-p^2-p^3+p^4", sp.expand(P3 - (pp - pp ** 2 - pp ** 3 + pp ** 4)) == 0, True, ""))
rows.append(("Q5d", "P4 = p^2/(1+2p-2p^2)", sp.simplify(Pall / P2 - pp ** 2 / (1 + 2 * pp - 2 * pp ** 2)) == 0, True, ""))
for pf in (0.3, 0.6, 0.85):
    st = rng.random((N, 4)) < pf
    A_, B_, C_, D_ = (st[:, i] for i in range(4))
    qe_ = A_ | (B_ & C_ & D_)
    qs_ = B_ | (A_ & C_ & D_)
    g = qe_ & qs_
    v1 = pf + pf ** 3 - pf ** 4
    v2 = pf ** 2 * (1 + 2 * pf - 2 * pf ** 2)
    v3 = pf - pf ** 2 - pf ** 3 + pf ** 4
    v4 = pf ** 2 / (1 + 2 * pf - 2 * pf ** 2)
    rec("Q5a", "P1 p=%.2f" % pf, v1, float(P1.subs(pp, pf)), float(qe_.mean()), se_p(v1), tol=1e-12)
    rec("Q5b", "P2 p=%.2f" % pf, v2, float(P2.subs(pp, pf)), float(g.mean()), se_p(v2), tol=1e-12)
    rec("Q5c", "P3 p=%.2f" % pf, v3, float(P3.subs(pp, pf)), float((qe_ & ~qs_).mean()), se_p(v3), tol=1e-12)
    rec("Q5d", "P4 p=%.2f" % pf, v4, float((Pall / P2).subs(pp, pf)), float((A_ & B_ & C_ & D_)[g].mean()), se_p(v4, int(g.sum())), tol=1e-12)

# ============================================================ Q6  (lattice paths)
for m, n in ((4, 3), (5, 2), (3, 3)):
    for pf in (0.3, 0.7):
        # exact: P(reach corner)=C(n+m,m)p^m(1-p)^n via binomial pmf
        off = math.comb(n + m, m) * pf ** m * (1 - pf) ** n
        steps = rng.random((N, n + m)) < pf              # True = right
        nright = steps.sum(axis=1)
        rec("Q6b", "m=%d n=%d p=%.1f" % (m, n, pf), off, off, float((nright == m).mean()), se_p(off), tol=0)
        reach = nright == m
        for (X, Y) in ((1, 1), (2, 1), (m - 1, n - 1)):
            if not (0 <= X <= m and 0 <= Y <= n):
                continue
            offc = Fr(math.comb(X + Y, X) * math.comb(m + n - X - Y, m - X), math.comb(n + m, m))
            # exact by enumerating all paths with m rights: fraction passing through (X,Y)
            cnt = tot = 0
            for rights in itertools.combinations(range(n + m), m):
                tot += 1
                rs = set(rights)
                x_ = y_ = 0
                hit = (X == 0 and Y == 0)
                for t in range(n + m):
                    if t in rs:
                        x_ += 1
                    else:
                        y_ += 1
                    if x_ == X and y_ == Y:
                        hit = True
                cnt += hit
            cs = np.cumsum(steps, axis=1)
            ts = np.arange(1, n + m + 1)
            passes = ((cs == X) & ((ts - cs) == Y)).any(axis=1)
            nr = int(reach.sum())
            rec("Q6c", "m=%d n=%d p=%.1f point (%d,%d)" % (m, n, pf, X, Y), offc, Fr(cnt, tot), float(passes[reach].mean()),
                se_p(float(offc), nr), tol=0)

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(1 if bad else 0)
