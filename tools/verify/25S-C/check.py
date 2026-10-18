# -*- coding: utf-8 -*-
"""Verification harness for 25S-C (probability). Run: PYTHONUTF8=1 py tools/verify/25S-C/check.py
Each final answer: EXACT (fractions / enumeration / sympy) and MC (>= 10^6 trials, within 4 SE). ASCII output only.
Symbolic answers are checked at sample parameter values (and as polynomial identities with sympy where possible)."""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20251211)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


def se_var(v):
    return math.sqrt((np.mean((v - v.mean()) ** 4) - v.var() ** 2) / len(v))


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se + 1e-12
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1  (a = (L-b)/2, b~U(0,1), L~U(1,2) independent)
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


sq = [(Fr(0), Fr(1)), (Fr(1), Fr(1)), (Fr(1), Fr(2)), (Fr(0), Fr(2))]   # (b, L) in [0,1]x[1,2]
bb = rng.random(N)
LL = 1 + rng.random(N)
aa = (LL - bb) / 2
for item, thr, off in (("Q1a", Fr(1, 4), Fr(1, 8)), ("Q1b", Fr(2, 3), Fr(7, 9))):
    # a < thr  <=>  L - b < 2 thr  <=>  b + 2thr - L >= 0
    poly = clip(sq, Fr(1), Fr(-1), 2 * thr)
    rec(item, "P(a<%s)" % thr, off, area(poly), float(np.mean(aa < float(thr))), se_p(float(off)), tol=0)
bs, Ls = sp.symbols("b L")
Ea = sp.Rational(1, 2) * (sp.Rational(3, 2) - sp.Rational(1, 2))
EL2 = sp.integrate(Ls ** 2, (Ls, 1, 2))
Eb2 = sp.integrate(bs ** 2, (bs, 0, 1))
Ea2 = sp.Rational(1, 4) * (EL2 + Eb2 - 2 * sp.Rational(1, 2) * sp.Rational(3, 2))
Va = Ea2 - Ea ** 2
Eab = sp.Rational(1, 2) * (sp.Rational(3, 2) * sp.Rational(1, 2) - Eb2)
Cab = Eab - Ea * sp.Rational(1, 2)
assert Ea == sp.Rational(1, 2) and Va == sp.Rational(1, 24) and Cab == sp.Rational(-1, 24)
rec("Q1c", "E[a]=1/2", Fr(1, 2), Fr(1, 2), float(aa.mean()), se_mean(aa))
rec("Q1c", "Var[a]=1/24", Fr(1, 24), Fr(Va.p, Va.q), float(aa.var()), se_var(aa))
prod = aa * bb
rec("Q1d", "E[ab]=5/24", Fr(5, 24), Fr(Eab.p, Eab.q), float(prod.mean()), se_mean(prod))
cov_mc = float(np.mean((aa - aa.mean()) * (bb - bb.mean())))
cv = (aa - aa.mean()) * (bb - bb.mean())
rec("Q1d", "Cov[a,b]=-1/24", Fr(-1, 24), Fr(Cab.p, Cab.q), cov_mc, se_mean(cv))

# ============================================================ Q2  (two distinct digits 1..9, ordered)
pairs = [(x, y) for x in range(1, 10) for y in range(1, 10) if x != y]
tot = len(pairs)
d1 = rng.integers(1, 10, N)
d2 = rng.integers(1, 9, N)
d2 = np.where(d2 >= d1, d2 + 1, d2)          # uniform on the other 8 digits
num = 10 * d1 + d2
odd = (num % 2 == 1)
rec("Q2a", "P(odd)=5/9", Fr(5, 9), Fr(sum(1 for x, y in pairs if y % 2), tot), float(odd.mean()), se_p(5 / 9), tol=0)
rec("Q2b", "P(div 3)=1/3", Fr(1, 3), Fr(sum(1 for x, y in pairs if (10 * x + y) % 3 == 0), tot), float((num % 3 == 0).mean()), se_p(1 / 3), tol=0)
rec("Q2c", "P(div 5)=1/9", Fr(1, 9), Fr(sum(1 for x, y in pairs if (10 * x + y) % 5 == 0), tot), float((num % 5 == 0).mean()), se_p(1 / 9), tol=0)
ev = ((d1 + d2) % 2 == 0)
ex = Fr(sum(1 for x, y in pairs if (x + y) % 2 == 0 and y % 2), sum(1 for x, y in pairs if (x + y) % 2 == 0))
rec("Q2d", "P(odd | sum even)=5/8", Fr(5, 8), ex, float(odd[ev].mean()), se_p(5 / 8, int(ev.sum())), tol=0)

# ============================================================ Q3  (Bernoulli matrix)
pv = Fr(3, 10)
pmf = {}
for x_, y_ in itertools.product((0, 1), repeat=2):
    Q = ((x_ * y_, -x_), (y_, x_ + y_ - x_ * y_))
    D = Q[0][0] * Q[1][1] - Q[0][1] * Q[1][0]
    T = Q[0][0] + Q[1][1]
    w = (pv if x_ else 1 - pv) * (pv if y_ else 1 - pv)
    pmf[(D, T)] = pmf.get((D, T), Fr(0)) + w
off = {(0, 0): (1 - pv) ** 2, (0, 1): 2 * pv * (1 - pv), (0, 2): Fr(0), (2, 0): Fr(0), (2, 1): Fr(0), (2, 2): pv ** 2}
Xs = rng.random(N) < float(pv)
Ys = rng.random(N) < float(pv)
Dm = 2 * (Xs & Ys).astype(int)
Tm = Xs.astype(int) + Ys.astype(int)
for key, o in off.items():
    rec("Q3a", "P(D=%d,T=%d)" % key, o, pmf.get(key, Fr(0)), float(np.mean((Dm == key[0]) & (Tm == key[1]))), se_p(float(o)), tol=0)
rec("Q3b", "P(D=2)=p^2", pv ** 2, sum(v for (d, t), v in pmf.items() if d == 2), float(np.mean(Dm == 2)), se_p(float(pv ** 2)), tol=0)
for t_ in range(3):
    o = Fr(math.comb(2, t_)) * pv ** t_ * (1 - pv) ** (2 - t_)
    rec("Q3c", "P(T=%d) Bin(2,p)" % t_, o, sum(v for (d, t), v in pmf.items() if t == t_), float(np.mean(Tm == t_)), se_p(float(o)), tol=0)
rows.append(("Q3d", "P(D=2,T=0)=0 != P(D=2)P(T=0)", pmf.get((2, 0), 0) == 0 and pv ** 2 * (1 - pv) ** 2 > 0, True, "dependent"))
ED = sum(d * v for (d, t), v in pmf.items())
ET = sum(t * v for (d, t), v in pmf.items())
EDT = sum(d * t * v for (d, t), v in pmf.items())
cov_ex = EDT - ED * ET
cov_off = 4 * pv ** 2 * (1 - pv)
cvv = (Dm - Dm.mean()) * (Tm - Tm.mean())
rec("Q3e", "Cov(D,T)=4p^2(1-p)", cov_off, cov_ex, float(cvv.mean()), se_mean(cvv), tol=0)
# DT identities at several p (symbolic)
ps = sp.symbols("p")
assert sp.simplify(4 * ps ** 2 - 2 * ps ** 2 * 2 * ps - 4 * ps ** 2 * (1 - ps)) == 0

# ============================================================ Q4  (pdf: x/a on [0,a], 1 on [a,b])
a_, b_ = sp.symbols("a b", positive=True)
xs = sp.symbols("x")
norm = sp.integrate(xs / a_, (xs, 0, a_)) + sp.integrate(1, (xs, a_, b_)) - 1
mean = sp.integrate(xs * xs / a_, (xs, 0, a_)) + sp.integrate(xs, (xs, a_, b_)) - sp.Rational(23, 24)
sols = sp.solve([norm, mean], [a_, b_], dict=True)
sols_ab = sorted((s_[a_], s_[b_]) for s_ in sols)
rows.append(("Q4a", "solutions of the two equations: %s" % (sols_ab,), (sp.Integer(1), sp.Rational(3, 2)) in sols_ab and
             all(s_[0] > s_[1] for s_ in sols_ab if s_ != (1, sp.Rational(3, 2))), True, "a<b picks a=1,b=3/2"))
# sample X: pdf x on [0,1) (mass 1/2), 1 on [1,3/2] (mass 1/2)
u = rng.random(N)
half = rng.random(N) < 0.5
X = np.where(half, np.sqrt(rng.random(N)), 1 + rng.random(N) / 2)
rec("Q4a", "E[X]=23/24", Fr(23, 24), Fr(23, 24), float(X.mean()), se_mean(X), tol=0)


def F(t):
    return 0.0 if t < 0 else (t * t / 2 if t < 1 else (t - 0.5 if t < 1.5 else 1.0))


for t in (0.3, 0.9, 1.2, 1.4):
    ex = float(sp.integrate(xs, (xs, 0, min(t, 1))) + (sp.integrate(1, (xs, 1, t)) if t > 1 else 0))
    rec("Q4b", "F(%.1f)" % t, F(t), ex, float(np.mean(X <= t)), se_p(F(t)), tol=1e-12)
off4 = Fr(5, 7)
ex4 = (Fr(5, 4) - Fr(1, 2) - Fr(1, 8)) / (1 - Fr(1, 8))
evx = X > 0.5
rec("Q4c", "P(X<=5/4 | X>1/2)=5/7", off4, ex4, float(np.mean(X[evx] <= 1.25)), se_p(5 / 7, int(evx.sum())), tol=0)

# ============================================================ Q5  (circuits; enumerate all 32 states)
p = sp.symbols("p")


def q1_works(A, B, C, D, E):    # bridge: top A-B, bottom C-D, E between the two middle nodes
    return (A and B) or (C and D) or (A and E and D) or (C and E and B)


def q2_works(A, B, C, D, E):
    return (A or B) and (C or D or E)


def poly_prob(f):
    tot = 0
    for st in itertools.product((0, 1), repeat=5):
        if f(*st):
            k = sum(st)
            tot += p ** k * (1 - p) ** (5 - k)
    return sp.expand(tot)


P1 = poly_prob(q1_works)
P2 = poly_prob(q2_works)
P12 = poly_prob(lambda *s: q1_works(*s) and q2_works(*s))
o1 = sp.expand((2 + 2 * p - 5 * p ** 2 + 2 * p ** 3) * p ** 2)
o2 = sp.expand(6 * p ** 2 - 9 * p ** 3 + 5 * p ** 4 - p ** 5)
o12 = sp.expand(3 * p ** 5 - 9 * p ** 4 + 7 * p ** 3)
oc = (p * (7 - 9 * p + 3 * p ** 2)) / (6 - 9 * p + 5 * p ** 2 - p ** 3)
rows.append(("Q5a", "P(Q1) polynomial identity (enumeration of 32 states)", sp.expand(P1 - o1) == 0, True, ""))
rows.append(("Q5b", "P(Q2) polynomial identity", sp.expand(P2 - o2) == 0, True, ""))
rows.append(("Q5c", "P(Q1 and Q2) polynomial identity", sp.expand(P12 - o12) == 0, True, ""))
rows.append(("Q5c", "P(Q1|Q2) identity", sp.simplify(P12 / P2 - oc) == 0, True, ""))
for pf in (0.3, 0.55, 0.8):
    st = rng.random((N, 5)) < pf
    A, B, C, D, E = (st[:, i] for i in range(5))
    q1 = (A & B) | (C & D) | (A & E & D) | (C & E & B)
    q2 = (A | B) & (C | D | E)
    v1 = float(o1.subs(p, pf)); v2 = float(o2.subs(p, pf)); vc = float(oc.subs(p, pf))
    rec("Q5a", "P(Q1) p=%.2f" % pf, v1, float(P1.subs(p, pf)), float(q1.mean()), se_p(v1), tol=1e-12)
    rec("Q5b", "P(Q2) p=%.2f" % pf, v2, float(P2.subs(p, pf)), float(q2.mean()), se_p(v2), tol=1e-12)
    rec("Q5c", "P(Q1|Q2) p=%.2f" % pf, vc, float((P12 / P2).subs(p, pf)), float(q1[q2].mean()), se_p(vc, int(q2.sum())), tol=1e-12)

# ============================================================ Q6  (size-biased average)
for ns in ([2, 5, 9], [1, 3, 4, 10], [7, 2]):
    n_arr = np.array(ns)
    fam = rng.integers(0, len(ns), N)
    Xv = n_arr[fam]                                     # random family
    person = rng.integers(0, n_arr.sum(), N)            # random participant
    cum = np.cumsum(n_arr)
    Yv = n_arr[np.searchsorted(cum, person, side="right")]
    EX = Fr(sum(ns), len(ns))
    EY = Fr(sum(k * k for k in ns), sum(ns))
    rec("Q6a", "E[X] %s" % ns, EX, Fr(sum(ns), len(ns)), float(Xv.mean()), se_mean(Xv), tol=0)
    rec("Q6b", "E[Y] %s" % ns, EY, sum(Fr(k, sum(ns)) * k for k in ns), float(Yv.mean()), se_mean(Yv), tol=0)
    var = sum(Fr(k * k, 1) for k in ns) / len(ns) - EX ** 2
    rows.append(("Q6c", "E[Y]/E[X] = 1+Var/E^2 >= 1, strict %s" % ns, EY / EX == 1 + var / EX ** 2 and EY > EX, float(Yv.mean()) > float(Xv.mean()), ""))

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(1 if bad else 0)
