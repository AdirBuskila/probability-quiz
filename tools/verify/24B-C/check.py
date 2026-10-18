# -*- coding: utf-8 -*-
"""Verification harness for 24B-C (probability). Run: PYTHONUTF8=1 py tools/verify/24B-C/check.py

Every final answer gets two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy).
  MC    : Monte Carlo (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Official keys are never changed. Q6a (expanded form) and Q6b (final answer) disagree with the exact value and are HELD.
Q3 bonus has no official solution: cov[D,T] = 2 n p^2 (1-p) is computed here only (not shipped).
Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20240915)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok, "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1 (L = 1), Z = max(X, Y) as printed
X = rng.random(N); Y = rng.random(N); Z = np.maximum(X, Y)
x, y = sp.symbols("x y", positive=True)
rec("Q1a", "P(X<1/5)", Fr(1, 5), Fr(1, 5), float(np.mean(X < .2)), se_p(.2))
rec("Q1b", "P(Y>1/3)", Fr(2, 3), 1 - Fr(1, 3), float(np.mean(Y > 1 / 3)), se_p(2 / 3))
ex = 1 - sp.Rational(1, 2) * sp.Rational(1, 4)
rec("Q1c", "P(X+Y<=3/2)", Fr(7, 8), Fr(int(ex.p), int(ex.q)), float(np.mean(X + Y <= 1.5)), se_p(7 / 8))
ex = 2 * (sp.Rational(1, 2) * sp.Rational(1, 9))
rec("Q1d", "P(max<1/3)", Fr(1, 9), Fr(int(ex.p), int(ex.q)), float(np.mean(Z < 1 / 3)), se_p(1 / 9))
rows.append(("Q1d", "P(max<1/3) = (1/3)^2", Fr(1, 3) ** 2 == Fr(1, 9), True, "product of cdfs"))
sel = X > .25
ex = sp.Rational(1, 4) * sp.Rational(1, 2) / sp.Rational(3, 4)
rec("Q1e", "P(max<1/2 | X>1/4)", Fr(1, 6), Fr(int(ex.p), int(ex.q)),
    float(np.mean((Z < .5) & sel) / np.mean(sel)), math.sqrt((1 / 6) * (5 / 6) / int(sel.sum())))
# note: with MIN instead of MAX (the printed word "shorter") the values would be 5/9 and 2/3, as in 24B-A
print("Q1 note: printed word 'shorter' contradicts Z=max(X,Y); key matches max (min would give 5/9 and 2/3).")

# ============================================================ Q2 (digits 0..9)
dig = list(range(10))
div3 = lambda d: d % 3 == 0
rec("Q2a", "P(div by 3)", Fr(2, 5), Fr(sum(div3(d) for d in dig), 10), float(np.mean(div3(rng.integers(0, 10, N)))) if False else float(np.mean(rng.integers(0, 10, N) % 3 == 0)), se_p(.4))
pairs = list(itertools.permutations(dig, 2))
rec("Q2b", "P(2nd div by 3)", Fr(2, 5), Fr(sum(div3(b) for a, b in pairs), len(pairs)),
    float(np.mean(np.argsort(rng.random((N, 10), dtype=np.float32), axis=1)[:, 1] % 3 == 0)), se_p(.4))
A1 = [(a, b) for a, b in pairs if div3(a)]
ex = Fr(sum(b % 2 == 0 for a, b in A1), len(A1))
M = np.argsort(rng.random((N, 10), dtype=np.float32), axis=1)
s1 = (M[:, 0] % 3 == 0)
rec("Q2c", "P(2nd even | 1st div by 3)", Fr(1, 2), ex, float(np.mean(M[s1, 1] % 2 == 0)), math.sqrt(.25 / int(s1.sum())))
rows.append(("Q2c", "|A1 n B2| = 18 of 90", sum(1 for a, b in pairs if div3(a) and b % 2 == 0) == 18, True, ""))
trip = list(itertools.permutations(dig, 3))
rec("Q2d", "P(3rd div by 3)", Fr(2, 5), Fr(sum(div3(c) for a, b, c in trip), len(trip)), float(np.mean(M[:, 2] % 3 == 0)), se_p(.4))

# ============================================================ Q3
for p in (Fr(3, 10), Fr(1, 2)):
    pf = float(p)
    for n in (1, 4):
        Xj = rng.random((N, n)) < pf; Yj = rng.random((N, n)) < pf
        Xi = Xj.astype(int); Yi = Yj.astype(int)
        # build each matrix, take its determinant and trace directly
        Dj = 0 * (Xi + Yi) - (-Xi) * Yi
        Tj = 0 + (Xi + Yi)
        D = Dj.sum(axis=1); T = Tj.sum(axis=1)
        for k in range(n + 1):
            off = math.comb(n, k) * (p ** 2) ** k * (1 - p ** 2) ** (n - k)
            ex = Fr(0)
            for bits in itertools.product((0, 1), repeat=2 * n):
                w = Fr(1); d = 0
                for j in range(n):
                    a, b = bits[2 * j], bits[2 * j + 1]
                    w *= (p if a else 1 - p) * (p if b else 1 - p); d += a * b
                if d == k:
                    ex += w
            rec("Q3a/c", "P(D=%d) n=%d p=%s" % (k, n, p), off, ex, float(np.mean(D == k)), se_p(float(off)))
        for t in range(2 * n + 1):
            off = math.comb(2 * n, t) * p ** t * (1 - p) ** (2 * n - t)
            ex = Fr(0)
            for bits in itertools.product((0, 1), repeat=2 * n):
                if sum(bits) == t:
                    ex += p ** t * (1 - p) ** (2 * n - t)
            rec("Q3b/d", "P(T=%d) n=%d p=%s" % (t, n, p), off, ex, float(np.mean(T == t)), se_p(float(off)))
        # bonus (not shipped): cov[D,T] = 2 n p^2 (1-p)
        cov_formula = 2 * n * p ** 2 * (1 - p)
        sd = float(np.std((D - D.mean()) * (T - T.mean())) / math.sqrt(N))
        rec("Q3bonus", "cov[D,T] n=%d p=%s (not shipped)" % (n, p), cov_formula, cov_formula, float(np.cov(D, T)[0, 1]), sd)
        rows.append(("Q3a", "D_1,T_1 pmf: D~Ber(p^2), T~Bin(2,p) n=%d" % n, True, True, ""))

# ============================================================ Q4
z = sp.symbols("z", real=True)
a_, b_ = sp.symbols("a b", positive=True)
area = 2 * a_ * sp.Rational(2, 5) + (b_ - a_) * sp.Rational(2, 5) / 2
fz_tail = sp.Rational(2, 5) * (b_ - z) / (b_ - a_)
Ez = sp.integrate(z * fz_tail, (z, a_, b_))
sols = sp.solve([sp.Eq(area, 1), sp.Eq(Ez, sp.Rational(4, 15))], [a_, b_], dict=True)
valid = [s for s in sols if s[a_] > 0 and s[b_] > s[a_]]
rows.append(("Q4a", "sympy: candidates=%s valid=%s" % (sols, valid),
             len(valid) == 1 and valid[0][a_] == 1 and valid[0][b_] == 2, True, "a=21/4 gives b=-43/4 < 0, excluded by the positivity of b"))
# sampler: rectangle mass 4/5 on (-1,1), triangle mass 1/5 on (1,2) with density (2/5)(2-z)
u = rng.random(N)
rect = u < 0.8
w = 1 - np.sqrt(1 - rng.random(N))             # density 2(1-w)... on (0,1) -> z = 2 - ... use cdf: 1-(1-s)^2
Zs = np.where(rect, -1 + 2 * rng.random(N), 2 - (1 - w) * 0 - np.sqrt(rng.random(N)))
# triangle part: density proportional to (2-z) on (1,2): z = 2 - sqrt(U)


def F_off(t):
    return 0.0 if t < -1 else (0.4 * (t + 1) if t < 1 else (1 - (2 - t) ** 2 / 5 if t < 2 else 1.0))


for t in (-.5, .3, .9, 1.2, 1.8, 2.5):
    tt = sp.nsimplify(t)
    ex = float((sp.integrate(sp.Rational(2, 5), (z, -1, min(tt, 1))) if tt > -1 else 0) +
               (sp.integrate(sp.Rational(2, 5) * (2 - z), (z, 1, min(tt, 2))) if tt > 1 else 0))
    rec("Q4b", "F_Z(%.2f)" % t, F_off(t), ex, float(np.mean(Zs <= t)), se_p(F_off(t)), tol=1e-9)
rec("Q4a", "E[Z]=4/15 (MC)", Fr(4, 15), Fr(4, 15), float(Zs.mean()), float(Zs.std() / math.sqrt(N)))
sel = np.abs(Zs) < 1.5
cc = float(np.mean((Zs > .5) & sel) / np.mean(sel))
rec("Q4c", "P(Z>1/2 | |Z|<3/2)", Fr(7, 19), (Fr(19, 20) - Fr(3, 5)) / Fr(19, 20), cc, math.sqrt(7 / 19 * 12 / 19 / int(sel.sum())))

# ============================================================ Q5 (as in 24B-A Q5)
for sizes in ((1, 2, 5, 9), (2, 3, 4), (1, 4, 6, 7, 10)):
    n = np.array(sizes); Nn = len(n); tot = n.sum()
    EX = Fr(int(tot), Nn); EY = Fr(int((n ** 2).sum()), int(tot))
    Xm = n[rng.integers(0, Nn, N)]
    Ym = n[np.repeat(np.arange(Nn), n)[rng.integers(0, tot, N)]]
    rec("Q5a", "E[X] sizes=%s" % (sizes,), EX, sum(Fr(int(s), Nn) for s in sizes), float(Xm.mean()), float(Xm.std() / math.sqrt(N)))
    rec("Q5b", "E[Y] sizes=%s" % (sizes,), EY, sum(Fr(int(s), int(tot)) * int(s) for s in sizes), float(Ym.mean()), float(Ym.std() / math.sqrt(N)))
    rows.append(("Q5c", "B>=A (strict for distinct sizes) sizes=%s" % (sizes,), EY >= EX, float(Ym.mean()) > float(Xm.mean()), "B/A=%s" % (EY / EX)))

# ============================================================ Q6 (Wheatstone bridge)
def works(s):
    A, B, C, D, E = s
    return bool(((A or B) and (C or D)) if E else ((A and C) or (B and D)))


hold_report = []
for p in (Fr(1, 2), Fr(7, 10), Fr(3, 10)):
    PQ = PA = Fr(0); one_fail_ok = True
    for s in itertools.product((0, 1), repeat=5):
        w = Fr(1)
        for v in s:
            w *= p if v else 1 - p
        if works(s):
            PQ += w
            if s[0]:
                PA += w
    PQA = PA / p
    ofirst = p * (2 * p - p ** 2) ** 2 + (1 - p) * (2 * p ** 2 - p ** 4)
    oexp = p ** 2 * (2 + p - 5 * p ** 2 + 2 * p ** 3)
    oPQA = p + 2 * p ** 2 - 4 * p ** 3 + p ** 4
    oPQA_formula = p + p * (2 * p - p ** 2) - p ** 2 * (2 * p - p ** 2)
    ob = (1 + 2 * p - 4 * p ** 2 + p ** 3) / (2 + p - 5 * p ** 2 + 2 * p ** 3)
    S = rng.random((N, 5)) < float(p)
    Aa, Bb, Cc, Dd, Ee = S.T
    mq = np.where(Ee, (Aa | Bb) & (Cc | Dd), (Aa & Cc) | (Bb & Dd))
    mc_PQ = float(mq.mean()); mc_b = float((mq & Aa).sum() / mq.sum())
    rec("Q6a", "first line p(2p-p^2)^2+(1-p)(2p^2-p^4), p=%s" % p, ofirst, PQ, mc_PQ, se_p(float(PQ)))
    rec("Q6b", "formula P(Q|A)=p+p(2p-p^2)-p^2(2p-p^2), p=%s" % p, oPQA_formula, PQA, float((mq & Aa).sum() / Aa.sum()), math.sqrt(float(PQA) * (1 - float(PQA)) / int(Aa.sum())))
    hold_report.append(("Q6a expanded", p, oexp == PQ, abs(mc_PQ - float(oexp)) <= 4 * se_p(float(PQ)), float(oexp), float(PQ)))
    hold_report.append(("Q6b P(Q|A) printed", p, oPQA == PQA, True, float(oPQA), float(PQA)))
    hold_report.append(("Q6b final", p, ob == PA / PQ, abs(mc_b - float(ob)) <= 4 * math.sqrt(float(PA / PQ) * (1 - float(PA / PQ)) / int(mq.sum())), float(ob), float(PA / PQ)))
    # Q6c: exactly one unit fails -> circuit works with probability 1
    allok = all(works(s) for s in itertools.product((0, 1), repeat=5) if sum(s) == 4)
    rows.append(("Q6c", "every single-failure state works p=%s" % p, allok, True, ""))
# correct expansions, for the ASK_ADIR entry (sympy)
pp = sp.symbols("p")
true_PQ = sp.expand(pp * (2 * pp - pp ** 2) ** 2 + (1 - pp) * (2 * pp ** 2 - pp ** 4))
true_PQA = sp.expand(pp + pp * (2 * pp - pp ** 2) - pp ** 2 * (2 * pp - pp ** 2))
true_b = sp.simplify(pp * true_PQA / true_PQ)

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-7s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("Q6 HOLD report (official printed forms vs exact):")
for what, p, ex_ok, mc_ok, off, true in hold_report:
    print("  %-20s p=%-5s exact=%s mc=%s official=%.6f true=%.6f" % (what, p, "match" if ex_ok else "MISMATCH", "match" if mc_ok else "MISMATCH", off, true))
print("  correct P(Q)   = %s" % true_PQ)
print("  correct P(Q|A) = %s" % true_PQA)
print("  correct P(A|Q) = %s" % true_b)
exp_hold = (not any(h[2] for h in hold_report if h[0] in ("Q6a expanded", "Q6b P(Q|A) printed", "Q6b final"))
            and sp.expand(true_PQ - pp ** 2 * (2 + 2 * pp - 5 * pp ** 2 + 2 * pp ** 3)) == 0
            and sp.expand(true_PQA - (pp + 2 * pp ** 2 - 3 * pp ** 3 + pp ** 4)) == 0)
print("  => Q6a and Q6b held (printed expansions wrong); first-line formulas verified. expected=%s" % exp_hold)
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if (not bad and exp_hold) else 1)
