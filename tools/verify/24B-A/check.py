# -*- coding: utf-8 -*-
"""Verification harness for 24B-A (probability). Run: PYTHONUTF8=1 py tools/verify/24B-A/check.py

Every final answer gets two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy).
  MC    : Monte Carlo (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Official keys are never changed here. Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20240716)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1 (L = 1; the ratios are scale free)
X = rng.random(N); Y = rng.random(N); Z = np.minimum(X, Y)
x, y = sp.symbols("x y", positive=True)
rec("Q1a", "P(X<1/3)", Fr(1, 3), Fr(1, 3), float(np.mean(X < 1 / 3)), se_p(1 / 3))
rec("Q1b", "P(Y>1/4)", Fr(3, 4), 1 - Fr(1, 4), float(np.mean(Y > 0.25)), se_p(.75))
# area x+y<=4/3 in the unit square: integral of min(1, 4/3-x) over x in (1/3,1) plus 1/3 (x<1/3 -> all y)
ex = sp.Rational(1, 3) + sp.integrate(sp.Rational(4, 3) - x, (x, sp.Rational(1, 3), 1))
rec("Q1c", "P(X+Y<=4/3)", Fr(7, 9), Fr(int(ex.p), int(ex.q)), float(np.mean(X + Y <= 4 / 3)), se_p(7 / 9))
# P(min<1/3) = 1 - (2/3)^2 and by the two-region area sum
ex = 2 * (sp.Rational(1, 3) - sp.Rational(1, 2) * sp.Rational(1, 9))
rec("Q1d", "P(Z<1/3)", Fr(5, 9), Fr(int(ex.p), int(ex.q)), float(np.mean(Z < 1 / 3)), se_p(5 / 9))
rows.append(("Q1d", "P(Z<1/3) = 1-(2/3)^2", 1 - Fr(4, 9) == Fr(5, 9), True, "complement"))
sel = X > 0.25
cond = float(np.mean((Z < .5) & sel) / np.mean(sel))
nsel = int(sel.sum())
rec("Q1e", "P(Z<1/2 | X>1/4)", Fr(2, 3), (Fr(3, 4) - Fr(1, 4)) / Fr(3, 4), cond, math.sqrt((2 / 3) * (1 / 3) / nsel))

# ============================================================ Q2
digits = range(10)
for pos, off in ((1, Fr(1, 10)), (2, Fr(1, 10)), (3, Fr(1, 10)), (10, Fr(1, 10))):
    prod = Fr(1)
    k = 10
    for _ in range(pos - 1):
        prod *= Fr(k - 1, k); k -= 1
    prod *= Fr(1, k)
    perms = 0; tot = 0
    if pos <= 3:
        for s in itertools.permutations(digits, pos):
            tot += 1; perms += (s[-1] == 3)
        ex = Fr(perms, tot)
    else:
        ex = Fr(math.factorial(9), math.factorial(10))   # permutations with 3 last / all permutations
    M = np.argsort(rng.random((N, 10), dtype=np.float32), axis=1)
    mc = float(np.mean(M[:, pos - 1] == 3))
    rec("Q2%s" % "abcd"[(1, 2, 3, 10).index(pos)], "P(digit %d == 3) chain=%s" % (pos, prod), off, ex, mc, se_p(.1))
    rows.append(("Q2%s" % "abcd"[(1, 2, 3, 10).index(pos)], "chain product == 1/10", prod == Fr(1, 10), True, ""))

# ============================================================ Q3
for p in (Fr(3, 10), Fr(7, 10)):
    pf = float(p)
    Xs = rng.random(N) < pf; Ys = rng.random(N) < pf
    Xi = Xs.astype(int); Yi = Ys.astype(int)
    # build the matrix directly and take determinant/trace (no use of the X^2=X simplification)
    Dm = Xi * (Xi - Yi) - (-(Xi ** 2)) * (Yi ** 2); Tm = Xi + (Xi - Yi)
    joint = {}
    for a in (0, 1):
        for b in (0, 1):
            d = a * (a - b) + a * a * b * b; t = a + (a - b)
            w = (p if a else 1 - p) * (p if b else 1 - p)
            joint[(d, t)] = joint.get((d, t), Fr(0)) + w
    off = {(0, -1): p * (1 - p), (0, 0): (1 - p) ** 2, (1, 1): p ** 2, (1, 2): p * (1 - p)}
    for k, v in off.items():
        rec("Q3a", "P(D=%d,T=%d) p=%s" % (k[0], k[1], p), v, joint.get(k, 0), float(np.mean((Dm == k[0]) & (Tm == k[1]))), se_p(float(v)))
    rows.append(("Q3a", "zero cells (0,1),(0,2),(1,-1),(1,0) p=%s" % p,
                 all(joint.get(k, 0) == 0 for k in ((0, 1), (0, 2), (1, -1), (1, 0))), True, ""))
    ED = sum(d * v for (d, t), v in joint.items()); ET = sum(t * v for (d, t), v in joint.items())
    VD = sum(d * d * v for (d, t), v in joint.items()) - ED ** 2; VT = sum(t * t * v for (d, t), v in joint.items()) - ET ** 2
    cov = sum(d * t * v for (d, t), v in joint.items()) - ED * ET
    rec("Q3b", "E[D] p=%s" % p, p, ED, float(Dm.mean()), float(Dm.std() / math.sqrt(N)))
    rec("Q3b", "Var[D] p=%s" % p, p * (1 - p), VD, float(Dm.var()), 4e-3 * 0 + float(Dm.var() * math.sqrt(2 / N)) * 2)
    rec("Q3c", "E[T] p=%s" % p, p, ET, float(Tm.mean()), float(Tm.std() / math.sqrt(N)))
    rec("Q3c", "Var[T] p=%s" % p, 5 * p * (1 - p), VT, float(Tm.var()), float(Tm.var() * math.sqrt(2 / N)) * 2)
    sd = float(np.std((Dm - Dm.mean()) * (Tm - Tm.mean())) / math.sqrt(N))
    rec("Q3d", "Cov[D,T] p=%s" % p, 2 * p * (1 - p), cov, float(np.cov(Dm, Tm)[0, 1]), sd)
    rows.append(("Q3e", "dependent: P(D=0,T=1)=0 != P(D=0)P(T=1) p=%s" % p,
                 joint.get((0, 1), 0) == 0 and (1 - p) * p ** 2 > 0, True, ""))
    rows.append(("Q3f", "Cov != 0 p=%s" % p, cov != 0, True, ""))

# ============================================================ Q4
z, a_, b_ = sp.symbols("z a b", positive=True)
area = sp.integrate(-z / a_, (z, -a_, 0)) * -1 * -1  # placeholder replaced below
f_V = sp.Abs(z) / a_
tot = sp.integrate(z / a_, (z, 0, a_)) * 2 + (b_ - a_)
sol = sp.solve([sp.Eq(tot, 1), sp.Eq(sp.integrate(z * 1, (z, a_, b_)), sp.Rational(3, 8))], [a_, b_], dict=True)
sol = [s for s in sol if s[a_] > 0 and s[b_] > s[a_]]
rows.append(("Q4a", "sympy solve gives a=1/2, b=1", len(sol) == 1 and sol[0][a_] == sp.Rational(1, 2) and sol[0][b_] == 1, True, str(sol)))
# sampler from the pdf: V part has mass 1/4 (symmetric), flat part mass 1/2 on (1/2,1)? mass: V = a = 1/2, flat = 1/2
u = rng.random(N)
V = u < 0.5
mag = np.sqrt(rng.random(N)) * 0.5          # |z| density 4|z| on (0,1/2) -> inverse cdf sqrt(u)/2
Zs = np.where(V, np.where(rng.random(N) < .5, -mag, mag), 0.5 + 0.5 * rng.random(N))


def F_off(t):
    return 0 if t < -.5 else (.25 - t * t if t < 0 else (.25 + t * t if t < .5 else (t if t < 1 else 1)))


tt = sp.symbols("t", real=True)
for t in (-.4, -.1, .2, .4, .75, 1.2):
    if t < 0:
        ex = float(sp.integrate(-2 * z, (z, -sp.Rational(1, 2), 0)) * 0 + sp.integrate(sp.Abs(z) * 2 * 0 + (-2) * z, (z, -sp.Rational(1, 2), sp.nsimplify(t))))
    elif t < .5:
        ex = 0.25 + float(sp.integrate(2 * z, (z, 0, sp.nsimplify(t))))
    elif t < 1:
        ex = 0.5 + (t - .5)
    else:
        ex = 1.0
    rec("Q4b", "F_Z(%.2f)" % t, F_off(t), ex, float(np.mean(Zs <= t)), se_p(float(F_off(t))), tol=1e-9)
rec("Q4a", "E[Z]=3/8 (MC)", Fr(3, 8), Fr(3, 8), float(Zs.mean()), float(Zs.std() / math.sqrt(N)))
sel = np.abs(Zs) < .5
cc = float(np.mean((Zs > .25) & sel) / np.mean(sel))
rec("Q4c", "P(Z>1/4 | |Z|<1/2)", Fr(3, 8), (Fr(1, 2) - Fr(5, 16)) / Fr(1, 2), cc, math.sqrt(.375 * .625 / int(sel.sum())))

# ============================================================ Q5 (sample family sizes, distinct)
for sizes in ((1, 2, 5, 9), (2, 3, 4), (1, 4, 6, 7, 10)):
    n = np.array(sizes); Nn = len(n); tot = n.sum()
    EX = Fr(int(tot), Nn); EY = Fr(int((n ** 2).sum()), int(tot))
    fam = rng.integers(0, Nn, N)
    Xm = n[fam]
    person = rng.integers(0, tot, N)
    owner = np.repeat(np.arange(Nn), n)[person]
    Ym = n[owner]
    rec("Q5a", "E[X] sizes=%s" % (sizes,), EX, sum(Fr(int(s), Nn) for s in sizes), float(Xm.mean()), float(Xm.std() / math.sqrt(N)))
    rec("Q5b", "E[Y] sizes=%s" % (sizes,), EY, sum(Fr(int(s), int(tot)) * int(s) for s in sizes), float(Ym.mean()), float(Ym.std() / math.sqrt(N)))
    rows.append(("Q5c", "E[Y]>E[X] (strict for distinct sizes) sizes=%s" % (sizes,), EY > EX, float(Ym.mean()) > float(Xm.mean()), "E[Y]/E[X]=%s" % (EY / EX)))

# ============================================================ Q6
def works(s, p, q):
    A, B, C, D, E = s
    return D and ((A and B) or C), D and ((E and B) or A)


for p, q in ((Fr(1, 2), Fr(1, 3)), (Fr(7, 10), Fr(9, 10)), (Fr(3, 10), Fr(4, 5))):
    P1 = P12 = P2 = Fr(0)
    for s in itertools.product((0, 1), repeat=5):
        w = Fr(1)
        for i, v in enumerate(s):
            pr = q if i == 4 else p
            w *= pr if v else 1 - pr
        w1, w2 = works(s, p, q)
        P1 += w * bool(w1); P2 += w * bool(w2); P12 += w * bool(w1 and w2)
    off1 = p ** 2 * (1 + p - p ** 2)
    off12 = p ** 3 * (1 + (1 - p) * (1 + q))
    off3 = p * (1 + (1 - p) * (1 + q)) / (1 + (1 - p) * p)
    pf, qf = float(p), float(q)
    S = rng.random((N, 5)) < np.array([pf, pf, pf, pf, qf])
    A, B, C, D, E = S.T
    q1 = D & ((A & B) | C); q2 = D & ((E & B) | A)
    rec("Q6a", "P(Q1) p=%s" % p, off1, P1, float(q1.mean()), se_p(float(off1)))
    rec("Q6b", "P(Q1 and Q2) p=%s q=%s" % (p, q), off12, P12, float((q1 & q2).mean()), se_p(float(off12)))
    rec("Q6c", "P(Q2|Q1) p=%s q=%s" % (p, q), off3, P12 / P1, float((q1 & q2).sum() / q1.sum()), math.sqrt(float(off3) * (1 - float(off3)) / int(q1.sum())))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if not bad else 1)
