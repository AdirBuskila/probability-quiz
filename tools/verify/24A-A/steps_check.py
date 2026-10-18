# -*- coding: utf-8 -*-
"""Verification of the guided steps of 24A-A (probability). Run: PYTHONUTF8=1 py tools/verify/24A-A/steps_check.py

Reads tools/raw/24A-A.json (written by tools/gen/gen_24A-A.py) and re-derives every NUMERIC step independently:
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

CODE = "24A-A"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20240325)
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

R = sp.Rational
# ============================================================ Q1: rectangle sides X~U(0,1), Y~U(0,2)
X = rng.random(N); Y = 2 * rng.random(N)
x, y = sp.symbols("x y", positive=True)
OMG = sp.integrate(1, (x, 0, 1), (y, 0, 2))
for q in ("Q1a", "Q1b", "Q1c"):
    num(q, 0, OMG)
S_ = X * Y; L_ = 2 * (X + Y)
area_a = sp.integrate(sp.Min(2, 1 / x), (x, 0, 1))
num("Q1a", 1, sp.solve(sp.Eq(1 / x, 2), x)[0])
num("Q1a", 2, area_a, 2 * float(np.mean(S_ < 1)), 2 * se_p(0.8466))
num("Q1a", 3, area_a / 2, float(np.mean(S_ < 1)), se_p(0.8466))
tri = sp.integrate(sp.Max(0, 1 - x), (x, 0, 1))
num("Q1b", 1, tri, 2 * float(np.mean(L_ < 2)), 2 * se_p(.25))
num("Q1b", 2, tri / 2, float(np.mean(L_ < 2)), se_p(.25))
sel = L_ > 2
inter = sp.integrate(sp.Min(2, 1 / x) - sp.Max(0, 1 - x), (x, 0, 1))
num("Q1c", 1, 1 - tri / 2, float(sel.mean()))
num("Q1c", 2, inter, 2 * float(np.mean((S_ < 1) & sel)), 2 * se_p(0.5966))
num("Q1c", 3, inter / 2 / (1 - tri / 2), float((S_ < 1)[sel].mean()), se_p(0.7954, int(sel.sum())))
argued("Q1d", 0)
claim("Q1d claims", abs(np.mean(X * Y) - (np.mean(X) + np.mean(Y))) > 0.5 and abs(np.mean(X + Y) - 1.5) < 0.01 and abs(np.mean(X * Y) - 0.5) < 0.01,
      "E[XY]=0.5 (independence) while E[X]+E[Y]=1.5: the sum rule is not the product rule")
num("Q1d", 1, R(1, 2), float(np.mean(S_)), float(S_.std()) / math.sqrt(N))
num("Q1d", 2, R(1, 3) * R(4, 3), float(np.mean(S_ ** 2)), float((S_ ** 2).std()) / math.sqrt(N))
num("Q1d", 3, R(4, 9) - R(1, 4), float(np.var(S_)), float(np.var(S_)) * math.sqrt(2 / N) * 3)
argued("Q1e", 0)
VX = sp.integrate((x - R(1, 2)) ** 2, (x, 0, 1)); VY = sp.integrate((y - 1) ** 2 / 2, (y, 0, 2))
claim("Q1e claims", 4 * (VX + VY) == R(5, 3) and 2 * (VX + VY) == R(5, 6) and 4 * VX * VY == R(1, 9) and abs(np.var(L_) - 5 / 3) < 0.01,
      "4(VarX+VarY)=5/3 (mc %.4f); the distractors give 5/6 and 1/9" % np.var(L_))
num("Q1e", 1, VX, float(np.var(X)), float(np.var(X)) * math.sqrt(2 / N) * 3)
num("Q1e", 2, VY, float(np.var(Y)), float(np.var(Y)) * math.sqrt(2 / N) * 3)
num("Q1e", 3, 4 * (VX + VY), float(np.var(L_)), float(np.var(L_)) * math.sqrt(2 / N) * 3)

# ============================================================ Q2: running sum of a fair N-faced die ever equals N
def comps(n, k):
    return [c for c in itertools.product(range(1, n + 1), repeat=k) if sum(c) == n]


def PN(n):
    return sum(Fr(len(comps(n, k)), n ** k) for k in range(1, n + 1))


def hit_mc(n, trials):
    s = np.zeros(trials, dtype=int); hit = np.zeros(trials, dtype=bool)
    alive = np.ones(trials, dtype=bool)
    for _ in range(n):
        s = s + np.where(alive, rng.integers(1, n + 1, trials), 0)
        hit |= alive & (s == n)
        alive &= s < n
    return float(hit.mean())


for n_, qid, steps_ in ((3, "Q2a", [2, 1]), (4, "Q2b", [3, 3]), (5, "Q2c", [4, 6, 4])):
    argued(qid, 0)
    for j, kk in enumerate(range(2, 2 + len(steps_))):
        num(qid, 1 + j, len(comps(n_, kk)))
        assert len(comps(n_, kk)) == steps_[j]
    num(qid, 1 + len(steps_), PN(n_), hit_mc(n_, N))
    rec(qid + " closed form", PN(n_) == Fr(1, n_) * (1 + Fr(1, n_)) ** (n_ - 1), "P_N = p(1+p)^(N-1)")
claim("Q2a claims", PN(3) == Fr(16, 27) and PN(3) != Fr(1, 3) and PN(3) != 1 and (2, 2) in itertools.product(range(1, 4), repeat=2) and sum((2, 2)) > 3,
      "P_3=16/27, not 1/3 and not 1 (the sequence 2,2 jumps over 3)")
unordered4 = Fr(1, 4) + 2 * Fr(1, 16) + Fr(1, 64) + Fr(1, 256)        # {4},{2,2},{3,1} -> 2 p^2 ... (unordered counting)
claim("Q2b claims", float(unordered4) < float(PN(4)) and abs(float(unordered4) - 0.3945) < 5e-4 and 4 ** 2 != len(comps(4, 2)),
      "unordered counting gives %.4f < %.4f; 4^k counts sequences whose sum is not 4" % (float(unordered4), float(PN(4))))
claim("Q2c claims", Fr(1, 5) ** 5 != PN(5) and Fr(1, 5) != PN(5) and abs(float(PN(5)) - 0.41472) < 1e-9, "p^5 and p both differ from P_5=0.41472")
argued("Q2d", 0)
claim("Q2d claims", PN(6) == Fr(1, 6) * (Fr(7, 6)) ** 5 and abs(float(Fr(1, 6) * (1 - Fr(1, 6) ** 6) / (1 - Fr(1, 6))) - 0.2) < 1e-4 and abs(float(PN(6)) - 0.36023) < 1e-5,
      "geometric-series formula gives 0.2, N p = 1; the binomial-theorem value is 0.36023")
num("Q2d", 1, len(comps(6, 3)))
num("Q2d", 2, PN(6), hit_mc(6, N))

# ============================================================ Q3: two strings, N1=3, N2=2, p=0.3
p = Fr(3, 10)
bm = lambda n, k: math.comb(n, k) * p ** k * (1 - p) ** (n - k)
X1 = rng.binomial(3, .3, N); X2 = rng.binomial(2, .3, N)
argued("Q3a", 0)
claim("Q3a claims", max(range(4)) == 3 and sum(bm(3, k) for k in range(4)) == 1, "X1 takes values 0..N1 only (bounded); pmf sums to 1")
num("Q3a", 1, bm(3, 0), float(np.mean(X1 == 0)))
num("Q3a", 2, bm(3, 2), float(np.mean(X1 == 2)))
conv = lambda k: sum(bm(3, i) * bm(2, k - i) for i in range(max(0, k - 2), min(3, k) + 1))
argued("Q3b", 0)
claim("Q3b claims", all(conv(k) == bm(5, k) for k in range(6)) and conv(2) != math.comb(6, 2) * p ** 2 * (1 - p) ** 4 and 2 * p == Fr(3, 5) and 2 * Fr(9, 10) > 1,
      "convolution of the two pmfs equals Bin(5,p) exactly; Bin(6,p) (N1*N2) differs; 2p is not a probability for p>1/2")
num("Q3b", 1, 5)
num("Q3b", 2, bm(5, 2), float(np.mean(X1 + X2 == 2)))
Xt = X1 + X2
argued("Q3c", 0)
claim("Q3c claims", abs(bm(3, 1) * bm(5, 2) - 0.13613) < 1e-5 and bm(3, 1) * bm(5, 2) != bm(3, 1) * bm(2, 1) and abs(float(np.mean(X1 == 1) * np.mean(Xt == 2)) - float(np.mean((X1 == 1) & (Xt == 2)))) > 0.03,
      "P(X1=1)P(X=2)=0.1361 is not the joint 0.18522 (X1 and X are dependent)")
num("Q3c", 1, bm(5, 2), float(np.mean(Xt == 2)))
num("Q3c", 2, bm(3, 1) * bm(2, 1), float(np.mean((X1 == 1) & (X2 == 1))))
selc = Xt == 2
num("Q3c", 3, bm(3, 1) * bm(2, 1) / bm(5, 2), float(np.mean(X1[selc] == 1)), se_p(.6, int(selc.sum())))
argued("Q3d", 0)
hyp = lambda k: Fr(math.comb(3, k) * math.comb(2, 2 - k), math.comb(5, 2))
claim("Q3d claims", all(Fr(bm(3, k) * bm(2, 2 - k), bm(5, 2)) == hyp(k) for k in range(3)) and sum(k * hyp(k) for k in range(3)) == Fr(6, 5) and abs(0.9 - 1.2) > 0.1,
      "conditional pmf is hypergeometric for any p (p cancels); mean 6/5, not N1 p = 0.9")
num("Q3d", 1, hyp(0), float(np.mean(X1[selc] == 0)), se_p(.1, int(selc.sum())))
num("Q3d", 2, sum(k * hyp(k) for k in range(3)), float(X1[selc].mean()), float(X1[selc].std()) / math.sqrt(int(selc.sum())))

# ============================================================ Q4: f = c x/a on (0,a), c on (a,b); a=1, b=3/2, c=1
a_, b_, c_, t = sp.symbols("a b c t", positive=True)
norm = a_ * c_ / 2 + c_ * (b_ - a_)
eq_half = sp.Eq(a_ * c_ / 2, c_ * (b_ - a_))
sub = sp.solve([sp.Eq(norm, 1), eq_half], [c_, b_], dict=True)[0]
claim("Q4a derivation", sp.simplify(sub[c_] * a_) == 1 and sp.simplify(sub[b_] / a_) == R(3, 2), "norm + equal halves give ac=1 and b=3a/2")
meanE = sp.integrate(t * c_ * t / a_, (t, 0, a_)) + sp.integrate(t * c_, (t, a_, b_))
meanE_a = sp.simplify(meanE.subs(sub))
sol_a = sp.solve(sp.Eq(meanE_a, R(23, 24)), a_)
claim("Q4a mean", sp.simplify(meanE_a - R(23, 24) * a_) == 0 and sol_a == [1], "E[X]=23a/24 after substitution -> a=1")
half = sp.integrate(t, (t, 0, 1))
num("Q4a", 0, half)
num("Q4a", 1, (sub[c_] * a_))
num("Q4a", 2, (sub[b_] / a_))
num("Q4a", 3, sol_a[0])
u = rng.random(N)
Xp = np.where(u < .5, np.sqrt(2 * u), u + .5)
rec("Q4 MC mean", abs(Xp.mean() - 23 / 24) <= 4 * Xp.std() / math.sqrt(N), "mc E[X]=%.5f vs 23/24" % Xp.mean())
Fq = lambda tt: (R(tt) ** 2 / 2 if R(tt) < 1 else R(tt) - R(1, 2))
num("Q4b", 0, Fq(1), float(np.mean(Xp <= 1)))
num("Q4b", 1, Fq(R(1, 2)), float(np.mean(Xp <= .5)))
num("Q4b", 2, Fq(R(5, 4)), float(np.mean(Xp <= 1.25)))
tq = R(23, 24)
argued("Q4c", 0)
claim("Q4c claims", tq < 1 and abs(float(tq - R(1, 2)) - 0.4583) < 1e-4 and abs(float(tq ** 2 / 2) - 0.4592) < 1e-4, "23/24<1 so the parabolic branch applies; the wrong branch gives 0.4583 vs 0.4592")
num("Q4c", 1, tq ** 2 / 2, float(np.mean(Xp <= 23 / 24)))
num("Q4c", 2, 1 - tq ** 2 / 2, float(np.mean(Xp > 23 / 24)))

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


# ============================================================ Q6: bridges; Q1 middle E, Q2 middle A; p = 0.6
bridge = lambda tl, tr, bl, br, mid: bool((tl and tr) or (bl and br) or (tl and mid and br) or (bl and mid and tr))
q1w = lambda s: bridge(s[0], s[1], s[2], s[3], s[4])
q2w = lambda s: bridge(s[4], s[1], s[2], s[3], s[0])
p6 = Fr(3, 5)
def prob(f, g=lambda s: True):
    tot = Fr(0)
    for s in itertools.product((0, 1), repeat=5):
        if f(s) and g(s):
            tot += math.prod(p6 if v else 1 - p6 for v in s)
    return tot


U = rng.random((N, 5)) < .6
A_, B_, C_, D_, E_ = (U[:, i] for i in range(5))
m1 = (A_ & B_) | (C_ & D_) | (A_ & E_ & D_) | (C_ & E_ & B_)
m2 = (E_ & B_) | (C_ & D_) | (E_ & A_ & D_) | (C_ & A_ & B_)
P1, P2_, PI, PU = prob(q1w), prob(q2w), prob(lambda s: q1w(s) and q2w(s)), prob(lambda s: q1w(s) or q2w(s))
argued("Q6a", 0)
claim("Q6a claims", prob(lambda s: (s[0] and s[1]) or (s[2] and s[3])) == Fr(5904, 10000) != P1 and p6 ** 5 == Fr(7776, 100000) != P1,
      "ignoring E gives 0.5904, all-in-series 0.07776; both differ from 0.65952")
num("Q6a", 1, prob(q1w, lambda s: s[4]) / p6, float(m1[E_].mean()), se_p(.7056, int(E_.sum())))
num("Q6a", 2, prob(q1w, lambda s: not s[4]) / (1 - p6), float(m1[~E_].mean()), se_p(.5904, int((~E_).sum())))
num("Q6a", 3, P1, float(m1.mean()))
argued("Q6b", 0)
claim("Q6b claims", P1 * P2_ != PI and P1 * P2_ < Fr(45, 100) and P1 + P2_ > 1 and P1 == P2_, "P(Q1)P(Q2)=%s != P(Q1^Q2)=%s; sum > 1; symmetry P(Q1)=P(Q2)" % (float(P1 * P2_), float(PI)))
num("Q6b", 1, P1, float(m1.mean()))
num("Q6b", 2, prob(lambda s: q1w(s) and q2w(s), lambda s: s[0] and s[4]) / (p6 * p6), float((m1 & m2)[A_ & E_].mean()), se_p(.84, int((A_ & E_).sum())))
num("Q6b", 3, PI, float((m1 & m2).mean()))
num("Q6b", 4, PI / P1, float(m2[m1].mean()), se_p(float(PI / P1), int(m1.sum())))
argued("Q6c", 0)
claim("Q6c claims", P1 + P2_ > 1 and PU == P1 + P2_ - PI and PU != P1 * P2_ and PU == p6 ** 2 * (3 - 4 * p6 ** 2 + 2 * p6 ** 3), "inclusion-exclusion holds; the sum exceeds 1; the product is wrong; shipped closed form")
num("Q6c", 1, P1 + P2_, float(m1.mean() + m2.mean()), 2 * se_p(0.6595))
num("Q6c", 2, PI, float((m1 & m2).mean()))
num("Q6c", 3, PU, float((m1 | m2).mean()))
rec("Q6 closed forms", P1 == p6 ** 2 * (2 + 2 * p6 - 5 * p6 ** 2 + 2 * p6 ** 3) and PI == p6 ** 2 * (1 + 4 * p6 - 6 * p6 ** 2 + 2 * p6 ** 3), "shipped closed forms = enumeration at p=0.6")

finish()
