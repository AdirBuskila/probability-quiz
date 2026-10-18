# -*- coding: utf-8 -*-
"""Verification of the guided steps of 24B-B (probability). Run: PYTHONUTF8=1 py tools/verify/24B-B/steps_check.py

Reads tools/raw/24B-B.json (written by tools/gen/gen_24B-B.py) and re-derives every NUMERIC step independently:
  EXACT : fractions / itertools enumeration / sympy, compared with the stored answer (within its tol, and 5e-5 of exact);
  MC    : Monte Carlo (>= 10^6 trials) within 4 standard errors of the exact value, where a kind applies.
Every CHOICE step is either evaluated numerically (opts: the correct option must equal the exact value and every
distractor must differ) or ARGUED, in which case the claims its explanation makes are asserted explicitly (claim rows).
At the end every step of the raw file must have been covered, otherwise this script fails. Exits 1 on any failure.
ASCII output.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

CODE = "24B-B"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20240806)
rows = []
fails = 0
covered = set()


def rec(tag, ok, info):
    global fails
    rows.append((tag, ok, info))
    if not ok:
        fails += 1


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-12) / n)


def num(qid, idx, exact, mc=None, se=None):
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "numeric", (qid, idx, s["type"])
    covered.add((qid, idx))
    ex = float(exact)
    ok_ex = abs(s["answer"] - ex) <= max(5e-5, abs(ex) * 2e-6) and abs(s["answer"] - ex) <= s["tol"] + 1e-12
    ok_mc = True
    info = "answer=%s exact=%.8g" % (s["answer"], ex)
    if mc is not None:
        ok_mc = abs(mc - ex) <= 4 * (se if se is not None else se_p(ex))
        info += " mc=%.6g" % mc
    rec("%s step%d numeric" % (qid, idx), ok_ex and ok_mc, info)


def opts(qid, idx, vals, target):
    """choice step whose options are numbers: vals[i] is the numeric value of option i."""
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "choice" and len(vals) == len(s["options"]), (qid, idx)
    covered.add((qid, idx))
    ci = "abcdefgh".index(s["correctId"])
    good = abs(vals[ci] - target) <= 1e-9 * max(1, abs(target))
    bad = [i for i, v in enumerate(vals) if i != ci and abs(v - target) <= 1e-4 * max(1, abs(target))]
    rec("%s step%d choice-values" % (qid, idx), good and not bad, "values=%s target=%.6g" % (["%.5g" % v for v in vals], target))


def argued(qid, idx):
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "choice", (qid, idx)
    covered.add((qid, idx))
    rec("%s step%d choice-argued" % (qid, idx), True, "reasoning choice; claims asserted separately")


def claim(tag, ok, info=""):
    rec(tag, bool(ok), info)


def finish():
    total = 0
    for q in RAW["questions"]:
        k = "Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))
        for i, s in enumerate(q.get("steps", [])):
            total += 1
            if (k, i) not in covered:
                rec("%s step%d COVERAGE" % (k, i), False, "step not covered by any check")
    for tag, ok, info in rows:
        print("%s %-28s %s" % ("ok  " if ok else "FAIL", tag, info))
    print("steps in raw: %d; steps covered: %d; check rows: %d; failures: %d" % (total, len(covered), len(rows), fails))
    sys.exit(1 if fails else 0)

# ============================================================ Q1 (L = 1): X1~U(0,1), X2~U(0,2)
X1 = rng.random(N); X2 = 2 * rng.random(N)
x, y = sp.symbols("x y")
OM = sp.integrate(1, (x, 0, 1), (y, 0, 2))
for q in ("Q1a", "Q1b", "Q1c"):
    num(q, 0, OM)
m = X1 < .2
num("Q1a", 1, sp.integrate(1, (x, 0, sp.Rational(1, 5)), (y, 0, 2)), 2 * float(m.mean()), 2 * se_p(.2))
num("Q1a", 2, sp.Rational(1, 5), float(m.mean()), se_p(.2))
m = X1 + X2 <= 1
num("Q1b", 1, sp.integrate(sp.Min(2, 1 - x), (x, 0, 1)), 2 * float(m.mean()), 2 * se_p(.25))
num("Q1b", 2, 2 - sp.integrate(sp.Min(2, 1 - x), (x, 0, 1)), 2 * float((~m).mean()), 2 * se_p(.75))
num("Q1b", 3, (2 - sp.Rational(1, 2)) / 2, float((~m).mean()), se_p(.75))
m = X2 < X1
num("Q1c", 1, sp.integrate(x, (x, 0, 1)), 2 * float(m.mean()), 2 * se_p(.25))
num("Q1c", 2, sp.integrate(x, (x, 0, 1)) / 2, float(m.mean()), se_p(.25))
pm = Fr(3, 10)
head = rng.random(N) < .3
Y = np.where(head, X1, X2)
p1 = Fr(1); p2 = Fr(1, 2)
vals = [float(pm * p1 + (1 - pm) * p2), float((p1 + p2) / 2), float(p1 * p2)]
opts("Q1d", 0, vals, 0.65)
num("Q1d", 1, 1, float(np.mean(X1 < 1)), 1e-9)
num("Q1d", 2, sp.Rational(1, 2), float(np.mean(X2 < 1)), se_p(.5))
num("Q1d", 3, pm * p1 + (1 - pm) * p2, float(np.mean(Y < 1)), se_p(.65))
num("Q1e", 0, sp.integrate(1, (x, sp.Rational(1, 2), 1)), float(np.mean((X1 > .5) & (X1 < 1.5))), se_p(.5))
num("Q1e", 1, sp.integrate(sp.Rational(1, 2), (x, sp.Rational(1, 2), sp.Rational(3, 2))), float(np.mean((X2 > .5) & (X2 < 1.5))), se_p(.5))
num("Q1e", 2, pm * sp.Rational(1, 2) + (1 - pm) * sp.Rational(1, 2), float(np.mean((Y > .5) & (Y < 1.5))), se_p(.5))

# ============================================================ Q2 (urn D=3 red, 7 black, without replacement)
NB, DR = 10, 3
M = np.argsort(rng.random((N, NB), dtype=np.float32), axis=1)     # row = a random permutation of the balls
RD = M < DR                                                        # ball id < 3 is red
perm = lambda k: list(itertools.permutations(range(NB), k))
P2, P3 = perm(2), perm(3)
red = lambda b: b < DR
pr = lambda f, S: Fr(sum(1 for s in S if f(s)), len(S))
num("Q2a", 1, pr(lambda s: red(s[0]), perm(1)), float(RD[:, 0].mean()))
argued("Q2a", 0)
claim("Q2a claims", pr(lambda s: red(s[0]), perm(1)) == Fr(3, 10), "one draw: |A|/|Omega| = 3/10 (a single trial has no 'first success' wait)")
num("Q2b", 1, pr(lambda s: red(s[0]), P2), float(RD[:, 0].mean()))
c1 = [s for s in P2 if red(s[0])]; c2 = [s for s in P2 if not red(s[0])]
num("Q2b", 2, pr(lambda s: red(s[1]), c1), float(RD[RD[:, 0]][:, 1].mean()), se_p(2 / 9, int(RD[:, 0].sum())))
num("Q2b", 3, pr(lambda s: red(s[1]), c2), float(RD[~RD[:, 0]][:, 1].mean()), se_p(1 / 3, int((~RD[:, 0]).sum())))
num("Q2b", 4, pr(lambda s: red(s[1]), P2), float(RD[:, 1].mean()))
argued("Q2b", 0)
both_red = pr(lambda s: red(s[0]) and red(s[1]), P2)
claim("Q2b claims", Fr(3, 10) ** 2 == Fr(9, 100) != Fr(3, 10) and both_red == Fr(1, 15) and Fr(2, 9) != Fr(3, 10),
      "(D/N)^2=0.09 is neither P(R2)=0.3 nor P(both red)=1/15 here; assuming R1 gives 2/9, not 0.3")
num("Q2c", 1, pr(lambda s: red(s[0]) and red(s[1]) and red(s[2]), P3), float((RD[:, 0] & RD[:, 1] & RD[:, 2]).mean()))
num("Q2c", 2, pr(lambda s: not red(s[0]) and not red(s[1]) and red(s[2]), P3), float((~RD[:, 0] & ~RD[:, 1] & RD[:, 2]).mean()))
num("Q2c", 3, pr(lambda s: red(s[2]), P3), float(RD[:, 2].mean()))
argued("Q2c", 0)
claim("Q2c claims", Fr(3, 10) ** 3 == Fr(27, 1000) != Fr(3, 10) and pr(lambda s: red(s[0]) and red(s[1]) and red(s[2]), P3) == Fr(1, 120) != Fr(3, 10),
      "(D/N)^3=0.027 and P(R1R2R3)=1/120 both differ from P(R3)=0.3")
num("Q2d", 1, pr(lambda s: red(s[1]), P2), float(RD[:, 1].mean()))
num("Q2d", 2, pr(lambda s: red(s[1]) and red(s[2]), P3), float((RD[:, 1] & RD[:, 2]).mean()))
cond = pr(lambda s: red(s[2]), [s for s in P3 if red(s[1])])
num("Q2d", 3, cond, float(RD[RD[:, 1]][:, 2].mean()), se_p(2 / 9, int(RD[:, 1].sum())))
argued("Q2d", 0)
claim("Q2d claims", cond == Fr(2, 9) and cond != Fr(3, 10) and cond != Fr(1, 8), "P(R3|R2)=2/9; independence gives 0.3, two-reds assumption gives 1/8")

# ============================================================ Q3 (ordered pairs of distinct digits 1..9)
pairs = [(a, b) for a in range(1, 10) for b in range(1, 10) if a != b]
G = np.argsort(rng.random((N, 9), dtype=np.float32), axis=1)[:, :2] + 1
tens, units = G[:, 0], G[:, 1]
num2 = lambda a, b: 10 * a + b
claim("Q3a claims", len(pairs) == 72 and 81 != 72 and 36 != 72 and num2(1, 2) != num2(2, 1), "|Omega|=72 ordered distinct pairs; 12 != 21 so unordered (36) is wrong; repeats excluded (81)")
argued("Q3a", 0)
ev = [pr_ for pr_ in pairs if num2(*pr_) % 2 == 0]
num("Q3a", 1, len(ev))
num("Q3a", 2, Fr(len(ev), 72), float(((10 * tens + units) % 2 == 0).mean()))
argued("Q3b", 0)
claim("Q3b claims", all((num2(a, b) % 3 == 0) == ((a + b) % 3 == 0) for a, b in pairs)
      and any((num2(a, b) % 3 == 0) != (b % 3 == 0) for a, b in pairs) and any((num2(a, b) % 3 == 0) != (a % 3 == 0) for a, b in pairs),
      "digit-sum rule is exact; units-digit and tens-digit rules are not")
d3 = [pr_ for pr_ in pairs if num2(*pr_) % 3 == 0]
num("Q3b", 1, len(d3))
num("Q3b", 2, Fr(len(d3), 72), float(((10 * tens + units) % 3 == 0).mean()))
argued("Q3c", 0)
claim("Q3c claims", all((num2(a, b) % 5 == 0) == (b == 5) for a, b in pairs) and any((num2(a, b) % 5 == 0) != (a == 5) for a, b in pairs)
      and any((num2(a, b) % 5 == 0) != ((a + b) % 5 == 0) for a, b in pairs), "units digit 5 is exactly the rule; tens=5 and digit-sum rules fail")
d5 = [pr_ for pr_ in pairs if num2(*pr_) % 5 == 0]
num("Q3c", 1, len(d5))
num("Q3c", 2, Fr(len(d5), 72), float((units == 5).mean()))
odd = [pr_ for pr_ in pairs if (pr_[0] + pr_[1]) % 2 == 1]
oe = [pr_ for pr_ in odd if num2(*pr_) % 2 == 0]
mo = (tens + units) % 2 == 1
num("Q3d", 0, len(odd))
num("Q3d", 1, Fr(len(odd), 72), float(mo.mean()))
num("Q3d", 2, Fr(len(oe), 72), float((mo & (units % 2 == 0)).mean()))
num("Q3d", 3, Fr(len(oe), len(odd)), float((units % 2 == 0)[mo].mean()), se_p(.5, int(mo.sum())))

# ============================================================ Q4 (pdf with a=1/3, b=1)
a_, b_ = sp.symbols("a b", positive=True)
z = sp.Symbol("z")
pieces = [(-a_, 0, 1 + z / a_), (0, a_, 1 - z / a_), (a_, b_, 1)]
norm = sum(sp.integrate(f, (z, lo, hi)) for lo, hi, f in pieces)
mean = sum(sp.integrate(z * f, (z, lo, hi)) for lo, hi, f in pieces)
bsol = sp.solve(sp.Eq(norm, 1), b_)
num("Q4a", 0, bsol[0])
argued("Q4a", 1)
tri_mean = sp.integrate(z * (1 + z / a_), (z, -a_, 0)) + sp.integrate(z * (1 - z / a_), (z, 0, a_))
claim("Q4a claims", sp.simplify(tri_mean) == 0 and sp.simplify(mean.subs(b_, 1) - (1 - a_ ** 2) / 2) == 0 and a_ / 2 != 0,
      "triangle part contributes 0; E[Z]=(1-a^2)/2 once b=1")
asol = sp.solve(sp.Eq((1 - a_ ** 2) / 2, sp.Rational(4, 9)), a_)
num("Q4a", 2, asol[0])
# sample Z: left triangle (prob 1/6), right triangle (1/6), rectangle on (1/3,1) (2/3)
u = rng.random(N); Zs = np.empty(N)
k1 = u < 1 / 6; k2 = (u >= 1 / 6) & (u < 1 / 3); k3 = u >= 1 / 3
Zs[k1] = (np.sqrt(rng.random(k1.sum())) - 1) / 3
Zs[k2] = (1 - np.sqrt(rng.random(k2.sum()))) / 3
Zs[k3] = 1 / 3 + 2 / 3 * rng.random(k3.sum())
rec("Q4a MC mean", abs(Zs.mean() - 4 / 9) <= 4 * Zs.std() / math.sqrt(N), "mc E[Z]=%.5f vs 4/9" % Zs.mean())


R = sp.Rational
pc = [(-R(1, 3), 0, 1 + 3 * z), (0, R(1, 3), 1 - 3 * z), (R(1, 3), 1, sp.Integer(1))]
def Fm(t):
    t = R(t)
    return sum(sp.integrate(f, (z, lo, min(t, hi))) for lo, hi, f in pc if lo < t)
num("Q4b", 0, Fm(sp.Integer(0)), float(np.mean(Zs <= 0)))
num("Q4b", 1, Fm(sp.Rational(1, 6)), float(np.mean(Zs <= 1 / 6)))
num("Q4b", 2, Fm(sp.Rational(1, 2)), float(np.mean(Zs <= .5)))
sel = np.abs(Zs) < .75
num("Q4c", 0, Fm(sp.Rational(3, 4)) - Fm(-sp.Rational(3, 4)), float(sel.mean()))
num("Q4c", 1, Fm(sp.Rational(1, 4)), float(np.mean(Zs <= .25)))
num("Q4c", 2, Fm(sp.Rational(3, 4)) - Fm(sp.Rational(1, 4)), float(np.mean((Zs > .25) & (Zs < .75))))
num("Q4c", 3, (Fm(sp.Rational(3, 4)) - Fm(sp.Rational(1, 4))) / (Fm(sp.Rational(3, 4)) - Fm(-sp.Rational(3, 4))), float((Zs > .25)[sel].mean()), se_p(41 / 72, int(sel.sum())))

# ============================================================ Q5 (N=5 students, p=0.6, Q=1/365)
NS, pp, Qb = 5, Fr(3, 5), Fr(1, 365)
joint = {}
for att in itertools.product((0, 1), repeat=NS):
    for bd in itertools.product((0, 1), repeat=NS):
        w = Fr(1)
        for a_i, b_i in zip(att, bd):
            w *= (pp if a_i else 1 - pp) * (Qb if b_i else 1 - Qb)
        key = (sum(att), sum(a_i * b_i for a_i, b_i in zip(att, bd)))
        joint[key] = joint.get(key, 0) + w
PX = lambda n: sum(w for (xx, yy), w in joint.items() if xx == n)
PY = lambda k: sum(w for (xx, yy), w in joint.items() if yy == k)
Ua = rng.random((N, NS)) < .6; Ub = rng.random((N, NS)) < 1 / 365
Xs = Ua.sum(1); Ys = (Ua & Ub).sum(1)
argued("Q5a", 0)
claim("Q5a claims", max(xx for xx, _ in joint) == NS and sum(PX(n) for n in range(NS + 1)) == 1, "X is bounded by N and has N+1 values (not geometric / Poisson)")
num("Q5a", 1, PX(3), float((Xs == 3).mean()))
argued("Q5b", 0)
from math import comb
binom_pm = lambda n, pr_, k: comb(n, k) * pr_ ** k * (1 - pr_) ** (n - k)
claim("Q5b claims", all(PY(k) == binom_pm(NS, pp * Qb, k) for k in range(NS + 1)) and PY(NS) != binom_pm(NS, Qb, NS)
      and pp + Qb < 1 and PY(1) != binom_pm(NS, pp + Qb, 1), "enumerated pmf of Y = Bin(5, pQ) exactly; Bin(5,Q) and Bin(5,p+Q) differ")
num("Q5b", 1, pp * Qb, float((Ua & Ub).mean()), se_p(float(pp * Qb)) / math.sqrt(NS))
num("Q5b", 2, PY(0), float((Ys == 0).mean()))
num("Q5b", 3, PY(1), float((Ys == 1).mean()))
pjoint = joint[(2, 1)]
bayes = pjoint / PY(1)
opts("Q5c", 0, [float(bayes), float(joint[(2, 1)] / PX(2)), float(PX(2))], float(bayes))
num("Q5c", 1, PY(1), float((Ys == 1).mean()))
num("Q5c", 2, pjoint, float(((Xs == 2) & (Ys == 1)).mean()))
sel = Ys == 1
num("Q5c", 3, bayes, float((Xs == 2)[sel].mean()), se_p(float(bayes), int(sel.sum())))
pt = (1 - pp) / (1 - pp * Qb)
rec("Q5c closed form", bayes == comb(4, 3) * pt ** 3 * (1 - pt), "P(X=2|Y=1) = C(N-k,N-n) pt^(N-n) (1-pt)^(n-k)")

# ============================================================ Q6 (bridge Q1, series-of-parallels Q2; p=0.6)
def q1w(s):
    A, B, C, D, E = s
    return bool((A and B) or (C and D) or (E and ((A and D) or (C and B))))


def q2w(s):
    A, B, C, D, E = s
    return bool((A or B) and (C or D or E))


p6 = Fr(3, 5)
def prob(f, g=lambda s: True):
    tot = Fr(0)
    for s in itertools.product((0, 1), repeat=5):
        if f(s) and g(s):
            tot += math.prod(p6 if v else 1 - p6 for v in s)
    return tot


U = rng.random((N, 5)) < .6
A_, B_, C_, D_, E_ = (U[:, i] for i in range(5))
m1 = (A_ & B_) | (C_ & D_) | (E_ & ((A_ & D_) | (C_ & B_)))
m2 = (A_ | B_) & (C_ | D_ | E_)
P1, P2_, P12 = prob(q1w), prob(q2w), prob(lambda s: q1w(s) and q2w(s))
argued("Q6a", 0)
claim("Q6a claims", prob(lambda s: (s[0] and s[1]) or (s[2] and s[3])) == Fr(5904, 10000) != P1 and p6 ** 5 == Fr(7776, 100000) != P1,
      "ignoring E gives 0.5904, all-in-series 0.07776; both differ from 0.65952")
num("Q6a", 1, prob(q1w, lambda s: s[4]) / p6, float(m1[E_].mean()), se_p(.7056, int(E_.sum())))
num("Q6a", 2, prob(q1w, lambda s: not s[4]) / (1 - p6), float(m1[~E_].mean()), se_p(.5904, int((~E_).sum())))
num("Q6a", 3, P1, float(m1.mean()))
argued("Q6b", 0)
claim("Q6b claims", Fr(1) - (1 - p6) ** 5 == Fr(98976, 100000) != P2_ and p6 ** 5 != P2_, "all-parallel 0.98976 and all-series 0.07776 differ from 0.78624")
num("Q6b", 1, 1 - (1 - p6) ** 2, float((A_ | B_).mean()))
num("Q6b", 2, 1 - (1 - p6) ** 3, float((C_ | D_ | E_).mean()))
num("Q6b", 3, P2_, float(m2.mean()))
argued("Q6c", 0)
claim("Q6c claims", P1 * P2_ != P12 and P1 + P2_ > 1, "P(Q1)P(Q2)=%s != P(Q1^Q2)=%s; the sum exceeds 1" % (float(P1 * P2_), float(P12)))
num("Q6c", 1, P2_, float(m2.mean()))
num("Q6c", 2, P12, float((m1 & m2).mean()))
num("Q6c", 3, P12 / P2_, float(m1[m2].mean()), se_p(float(P12 / P2_), int(m2.sum())))
rec("Q6 closed forms", P1 == p6 ** 2 * (2 + 2 * p6 - 5 * p6 ** 2 + 2 * p6 ** 3) and P2_ == 6 * p6 ** 2 - 9 * p6 ** 3 + 5 * p6 ** 4 - p6 ** 5
    and P12 == 3 * p6 ** 5 - 9 * p6 ** 4 + 7 * p6 ** 3, "shipped closed forms = enumeration at p=0.6")

finish()
