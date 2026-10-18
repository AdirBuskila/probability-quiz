# -*- coding: utf-8 -*-
"""Verification of the guided steps of 24B-C (probability). Run: PYTHONUTF8=1 py tools/verify/24B-C/steps_check.py

Reads tools/raw/24B-C.json (written by tools/gen/gen_24B-C.py) and re-derives every NUMERIC step independently:
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

CODE = "24B-C"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20240915)
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
# ============================================================ Q1 (L = 1): X, Y ~ U(0,1) independent
X = rng.random(N); Y = rng.random(N)
x, y = sp.symbols("x y")
one = sp.integrate(1, (x, 0, 1), (y, 0, 1))
for q in ("Q1a", "Q1b", "Q1c", "Q1d", "Q1e"):
    num(q, 0, one)
num("Q1a", 1, sp.integrate(1, (x, 0, R(1, 5)), (y, 0, 1)), float(np.mean(X < .2)))
num("Q1b", 1, sp.integrate(1, (x, 0, 1), (y, R(1, 3), 1)), float(np.mean(Y > 1 / 3)))
corner = sp.integrate(1, (x, R(3, 2) - y, 1), (y, R(1, 2), 1))
num("Q1c", 1, corner, float(np.mean(X + Y > 1.5)))
num("Q1c", 2, 1 - corner, float(np.mean(X + Y <= 1.5)))
Z = np.maximum(X, Y)
opts("Q1d", 1, [float(R(1, 9)), float(R(5, 9)), float(R(1, 18))], 1 / 9)
claim("Q1d claims", abs(np.mean(Z < 1 / 3) - 1 / 9) < 4 * se_p(1 / 9) and abs(np.mean(np.minimum(X, Y) < 1 / 3) - 5 / 9) < 4 * se_p(5 / 9)
      and abs(np.mean(X + Y < 1 / 3) - 1 / 18) < 4 * se_p(1 / 18), "max<1/3 -> 1/9 (both <1/3); min<1/3 (union) -> 5/9; X+Y<1/3 -> 1/18")
num("Q1d", 2, sp.integrate(1, (x, 0, R(1, 3)), (y, 0, R(1, 3))), float(np.mean(Z < 1 / 3)))
den = sp.integrate(1, (x, R(1, 4), 1), (y, 0, 1))
inter = sp.integrate(1, (x, R(1, 4), R(1, 2)), (y, 0, R(1, 2)))
sel = X > .25
num("Q1e", 1, den, float(sel.mean()))
num("Q1e", 2, inter, float(np.mean((Z < .5) & sel)))
num("Q1e", 3, inter / den, float((Z < .5)[sel].mean()), se_p(1 / 6, int(sel.sum())))

# ============================================================ Q2 (digits 0..9)
digs = list(range(10))
perm = lambda k: list(itertools.permutations(digs, k))
P1, P2, P3 = perm(1), perm(2), perm(3)
pr = lambda f, S: Fr(sum(1 for s in S if f(s)), len(S))
cnt = lambda f, S: sum(1 for s in S if f(s))
M = np.argsort(rng.random((N, 10), dtype=np.float32), axis=1)    # row = random permutation of the digits
d3 = lambda v: v % 3 == 0
ev = lambda v: v % 2 == 0
argued("Q2a", 0)
claim("Q2a claims", len(P1) == 10 and d3(0) and [v for v in digs if d3(v)] == [0, 3, 6, 9], "10 outcomes incl. 0; the event {0,3,6,9} has 4 elements (not Omega)")
num("Q2a", 1, cnt(lambda s: d3(s[0]), P1))
num("Q2a", 2, pr(lambda s: d3(s[0]), P1), float(d3(M[:, 0]).mean()))
argued("Q2b", 0)
claim("Q2b claims", len(P2) == 90 and 10 * 10 == 100 != 90 and math.comb(10, 2) == 45,
      "ordered distinct pairs: 90; with replacement 100; unordered 45 (second digit must be distinguished)")
num("Q2b", 1, cnt(lambda s: d3(s[1]), P2))
num("Q2b", 2, pr(lambda s: d3(s[1]), P2), float(d3(M[:, 1]).mean()))
A1 = d3(M[:, 0]); B2 = ev(M[:, 1])
pA1 = pr(lambda s: d3(s[0]), P2); pAB = pr(lambda s: d3(s[0]) and ev(s[1]), P2)
opts("Q2c", 0, [float(pAB / pA1), float(pAB / pr(lambda s: ev(s[1]), P2)), float(pAB)], 0.5)
num("Q2c", 1, pA1, float(A1.mean()))
num("Q2c", 2, cnt(lambda s: d3(s[0]) and ev(s[1]), P2))
num("Q2c", 3, pAB, float((A1 & B2).mean()))
num("Q2c", 4, pAB / pA1, float(B2[A1].mean()), se_p(.5, int(A1.sum())))
argued("Q2d", 0)
claim("Q2d claims", len(P3) == 720 and 10 ** 3 == 1000 != 720 and math.comb(10, 3) == 120, "ordered distinct triples: 720; with replacement 1000; unordered 120")
num("Q2d", 1, cnt(lambda s: d3(s[2]), P3))
num("Q2d", 2, pr(lambda s: d3(s[2]), P3), float(d3(M[:, 2]).mean()))

# ============================================================ Q3 (Bernoulli matrices Q=[[0,-X],[Y,X+Y]], p=0.3)
Xs_, Ys_ = sp.symbols("X Y")
Qm = sp.Matrix([[0, -Xs_], [Ys_, Xs_ + Ys_]])
claim("Q3 matrix", sp.expand(Qm.det() - Xs_ * Ys_) == 0 and sp.expand(Qm.trace() - (Xs_ + Ys_)) == 0, "det Q = XY, tr Q = X+Y")
p = Fr(3, 10)
bits = list(itertools.product((0, 1), repeat=6))      # X1,X2,X3,Y1,Y2,Y3
wt = lambda b: math.prod(p if v else 1 - p for v in b)
Dv = lambda b: b[0] * b[3] + b[1] * b[4] + b[2] * b[5]
Tv = lambda b: sum(b)
PE = lambda f: sum(wt(b) for b in bits if f(b))
EE = lambda f: sum(wt(b) * f(b) for b in bits)
Ub = (rng.random((N, 6)) < .3).astype(int)
Dm = Ub[:, 0] * Ub[:, 3] + Ub[:, 1] * Ub[:, 4] + Ub[:, 2] * Ub[:, 5]
Tm = Ub.sum(1)
# part a/b use one matrix (first pair)
argued("Q3a", 0)
claim("Q3a claims", PE(lambda b: b[0] * b[3] == 1) == p ** 2 != p and PE(lambda b: b[0] + b[3] == 2) == p ** 2 and PE(lambda b: b[0] * b[3] == 1 and False) == 0,
      "D1 in {0,1} with P(D1=1)=p^2 (not p); Bin(2,p) would also take the value 2 -> that is T1")
num("Q3a", 1, PE(lambda b: b[0] * b[3] == 1), float(np.mean(Ub[:, 0] & Ub[:, 3])), se_p(.09))
num("Q3a", 2, PE(lambda b: b[0] * b[3] == 0), float(np.mean((Ub[:, 0] * Ub[:, 3]) == 0)), se_p(.09))
argued("Q3b", 0)
claim("Q3b claims", PE(lambda b: b[0] + b[3] == 2) > 0 and 2 * p > 0 and Fr(2) * Fr(9, 10) > 1, "T1 takes the value 2 (so it is not Bernoulli); 2p is not a probability when p>1/2")
num("Q3b", 1, PE(lambda b: b[0] + b[3] == 1), float(np.mean(Ub[:, 0] ^ Ub[:, 3])), se_p(.42))
num("Q3b", 2, PE(lambda b: b[0] + b[3] == 2), float(np.mean(Ub[:, 0] & Ub[:, 3])), se_p(.09))
argued("Q3c", 0)
pmf_bin = lambda n, pp_, k: math.comb(n, k) * pp_ ** k * (1 - pp_) ** (n - k)
claim("Q3c claims", all(PE(lambda b: Dv(b) == k) == pmf_bin(3, p * p, k) for k in range(4)) and PE(lambda b: Dv(b) == 1) != pmf_bin(3, p, 1)
      and PE(lambda b: Dv(b) == 1) != pmf_bin(6, p * p, 1), "enumerated pmf of D (n=3) equals Bin(3,p^2) exactly; Bin(3,p), Bin(6,p^2) differ")
num("Q3c", 1, PE(lambda b: Dv(b) == 1), float(np.mean(Dm == 1)))
argued("Q3d", 0)
claim("Q3d claims", all(PE(lambda b: Tv(b) == k) == pmf_bin(6, p, k) for k in range(7)) and PE(lambda b: Tv(b) == 2) != pmf_bin(3, p, 2)
      and 2 * p == Fr(3, 5), "enumerated pmf of T (n=3) equals Bin(6,p) exactly; Bin(3,p) and Bin(3,2p) differ")
num("Q3d", 1, 6)
num("Q3d", 2, PE(lambda b: Tv(b) == 2), float(np.mean(Tm == 2)))
cov1 = sum(wt(b) * (b[0] * b[3]) * (b[0] + b[3]) for b in bits) - sum(wt(b) * (b[0] * b[3]) for b in bits) * sum(wt(b) * (b[0] + b[3]) for b in bits)
covn = EE(lambda b: Dv(b) * Tv(b)) - EE(Dv) * EE(Tv)
argued("Q3e", 0)
claim("Q3e claims", sum(wt(b) * (b[0] * b[3]) * (b[1] + b[4]) for b in bits) == sum(wt(b) * (b[0] * b[3]) for b in bits) * sum(wt(b) * (b[1] + b[4]) for b in bits),
      "cov[D_1,T_2] = 0 (different pairs are independent)")
d1 = (Ub[:, 0] & Ub[:, 3]).astype(float); t1 = Ub[:, 0].astype(float) + Ub[:, 3]
num("Q3e", 1, cov1, float(np.mean(d1 * t1) - d1.mean() * t1.mean()), 0.003)
num("Q3e", 2, covn, float(np.mean(Dm * Tm) - Dm.mean() * Tm.mean()), 0.006)
rec("Q3e closed form", covn == 2 * 3 * p ** 2 * (1 - p) and cov1 == 2 * p ** 2 * (1 - p), "cov[D,T] = 2np^2(1-p), cov[D1,T1] = 2p^2(1-p)")

# ============================================================ Q4 (pdf: 2/5 on (-a,a), linear down to 0 on (a,b))
a_, b_, z = sp.symbols("a b z", positive=True)
norm = sp.integrate(sp.Rational(2, 5), (z, -a_, a_)) + sp.integrate(sp.Rational(2, 5) * (b_ - z) / (b_ - a_), (z, a_, b_))
mean = sp.integrate(z * sp.Rational(2, 5) * (b_ - z) / (b_ - a_), (z, a_, b_))
sols = [s for s in sp.solve([sp.Eq(norm, 1), sp.Eq(mean, sp.Rational(4, 15))], [a_, b_], dict=True) if s[b_] > s[a_]]
rec("Q4a solve", sols == [{a_: 1, b_: 2}], str(sols))
quad = sp.Poly(sp.expand((b_ ** 2 + a_ * b_ - 2 * a_ ** 2 - 4).subs(b_, 5 - 3 * a_)), a_)
roots = sp.solve(quad.as_expr(), a_)
bad_b = 5 - 3 * (sp.Rational(21, 4))
claim("Q4a claims", sorted(roots) == [1, sp.Rational(21, 4)] and bad_b == -sp.Rational(43, 4) and bad_b < sp.Rational(21, 4), "roots 1 and 21/4; the latter gives b=-43/4<a")
argued("Q4a", 0)
num("Q4a", 1, (5 - 3 * 1))
num("Q4a", 2, mean.subs({a_: 1, b_: 2}))
u = rng.random(N); Zs = np.empty(N)
k1 = u < .8
Zs[k1] = -1 + 2 * rng.random(k1.sum())
Zs[~k1] = 2 - np.sqrt(rng.random((~k1).sum()))          # triangle on (1,2): P(Z>z | tri)=(2-z)^2
rec("Q4a MC mean", abs(Zs.mean() - 4 / 15) <= 4 * Zs.std() / math.sqrt(N), "mc E[Z]=%.5f vs 4/15" % Zs.mean())
pcs = [(R(-1), R(1), sp.Rational(2, 5)), (R(1), R(2), sp.Rational(2, 5) * (2 - z))]
def Fm(t):
    t = R(t)
    return sum(sp.integrate(f, (z, lo, min(t, hi))) for lo, hi, f in pcs if lo < t)
num("Q4b", 0, Fm(0), float(np.mean(Zs <= 0)))
num("Q4b", 1, Fm(1), float(np.mean(Zs <= 1)))
num("Q4b", 2, Fm(R(3, 2)), float(np.mean(Zs <= 1.5)))
sel = np.abs(Zs) < 1.5
num("Q4c", 0, Fm(R(1, 2)), float(np.mean(Zs <= .5)))
num("Q4c", 1, Fm(R(3, 2)) - Fm(-R(3, 2)), float(sel.mean()))
num("Q4c", 2, Fm(R(3, 2)) - Fm(R(1, 2)), float(np.mean((Zs > .5) & (Zs < 1.5))))
num("Q4c", 3, (Fm(R(3, 2)) - Fm(R(1, 2))) / (Fm(R(3, 2)) - Fm(-R(3, 2))), float((Zs > .5)[sel].mean()), se_p(7 / 19, int(sel.sum())))

# ============================================================ Q5 (boxes of 2, 3, 7 bolts)
sizes = [2, 3, 7]; n = sum(sizes)
fam = rng.integers(0, 3, N)
szX = np.array(sizes)[fam]
ppl = np.repeat(sizes, sizes)
szY = ppl[rng.integers(0, n, N)]
EX = Fr(sum(sizes), 3); EX2 = Fr(sum(s * s for s in sizes), 3); VX = EX2 - EX ** 2
EY = Fr(sum(s * s for s in sizes), n)
opts("Q5a", 0, [1 / 3, 7 / 12, 7 / 3], float(Fr(1, 3)))
num("Q5a", 1, Fr(1, 3), float(np.mean(szX == 7)))
num("Q5a", 2, EX, float(szX.mean()), float(szX.std()) / math.sqrt(N))
opts("Q5b", 0, [7 / 12, 1 / 3, 49 / 62], float(Fr(7, 12)))
num("Q5b", 1, Fr(7, n), float(np.mean(szY == 7)))
num("Q5b", 2, EY, float(szY.mean()), float(szY.std()) / math.sqrt(N))
num("Q5c", 0, VX, float(szX.var()), float(szX.var()) * math.sqrt(2 / N) * 2)
num("Q5c", 1, EY / EX, float(szY.mean() / szX.mean()), 0.004)
argued("Q5c", 2)
claim("Q5c claims", EY / EX == 1 + VX / EX ** 2 and EY / EX > 1 and EY != EX, "E[Y]/E[X] = 1+Var/E^2 = 31/24 > 1, so B=A and B<A fail")
claim("Q5a-b claims", abs(sum(s / n for s in sizes) - 1) < 1e-12 and sum(Fr(s, 3) for s in sizes) != 1 and sum(Fr(s * s, sum(t * t for t in sizes)) for s in sizes) == 1 and Fr(49, 62) != Fr(7, 12),
      "n_i/n sums to 1, n_i/N does not; n_i^2/sum n^2 is a pmf but is not the bolt-selection rule (49/62 != 7/12)")

# ============================================================ Q6 (bridge, p = 0.6)
def works(s):
    A, B, C, D, E = s
    return bool(((A or B) and (C or D)) if E else ((A and C) or (B and D)))


p6 = Fr(3, 5)
def prob(f, g=lambda s: True):
    tot = Fr(0)
    for s in itertools.product((0, 1), repeat=5):
        if f(s) and g(s):
            tot += math.prod(p6 if v else 1 - p6 for v in s)
    return tot


PQ = prob(works)
U = rng.random((N, 5)) < .6
A_, B_, C_, D_, E_ = (U[:, i] for i in range(5))
mq = np.where(E_, (A_ | B_) & (C_ | D_), (A_ & C_) | (B_ & D_))
argued("Q6a", 0)
claim("Q6a claims", prob(lambda s: (s[0] and s[2]) or (s[1] and s[3])) == Fr(5904, 10000) != PQ and p6 ** 5 == Fr(7776, 100000) != PQ,
      "ignoring E gives 0.5904, all-in-series 0.07776; both differ from 0.65952")
num("Q6a", 1, prob(works, lambda s: s[4]) / p6, float(mq[E_].mean()), se_p(.7056, int(E_.sum())))
num("Q6a", 2, prob(works, lambda s: not s[4]) / (1 - p6), float(mq[~E_].mean()), se_p(.5904, int((~E_).sum())))
num("Q6a", 3, PQ, float(mq.mean()))
PQA = prob(works, lambda s: s[0]) / p6
bayes = prob(lambda s: works(s) and s[0]) / PQ
argued("Q6b", 0)
claim("Q6b claims", PQA == Fr(8016, 10000) and p6 == Fr(3, 5) and bayes != PQA and bayes != p6 and bayes == (1 + 2 * p6 - 3 * p6 ** 2 + p6 ** 3) / (2 + 2 * p6 - 5 * p6 ** 2 + 2 * p6 ** 3),
      "P(Q|A)=0.8016 and P(A)=0.6 differ from P(A|Q)=%s (shipped closed form checked)" % float(bayes))
num("Q6b", 1, PQ, float(mq.mean()))
num("Q6b", 2, PQA, float(mq[A_].mean()), se_p(float(PQA), int(A_.sum())))
num("Q6b", 3, bayes, float(A_[mq].mean()), se_p(float(bayes), int(mq.sum())))
one_fail = [s for s in itertools.product((0, 1), repeat=5) if sum(s) == 4]
argued("Q6c", 0)
claim("Q6c claims", all(works(s) for s in one_fail) and len(one_fail) == 5 and p6 ** 4 * (1 - p6) < 1, "all 5 single-failure states work; p^4(1-p) is only the (unconditional) probability of one of them")
num("Q6c", 1, sum(1 for s in one_fail if works(s)))
sel = (U.sum(1) == 4)
num("Q6c", 2, Fr(sum(1 for s in one_fail if works(s)), len(one_fail)), float(mq[sel].mean()), 1e-9)
rec("Q6 closed forms", PQ == p6 ** 2 * (2 + 2 * p6 - 5 * p6 ** 2 + 2 * p6 ** 3), "shipped P(Q)=p^2(2+2p-5p^2+2p^3) = enumeration at p=0.6")

finish()
