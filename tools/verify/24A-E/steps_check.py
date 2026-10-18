# -*- coding: utf-8 -*-
"""Verification of the guided steps of 24A-E (probability). Run: PYTHONUTF8=1 py tools/verify/24A-E/steps_check.py

Reads tools/raw/24A-E.json (written by tools/gen/gen_24A-E.py) and re-derives every NUMERIC step independently:
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

CODE = "24A-E"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20240509)
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
# ============================================================ Q1: X_L~U(0,1), X_R~U(0,2)
XL = rng.random(N); XR = 2 * rng.random(N)
x, y = sp.symbols("x y")
OMG = sp.integrate(1, (x, 0, 1), (y, 0, 2))
for q in ("Q1a", "Q1b", "Q1c", "Q1d"):
    num(q, 0, OMG)
argued("Q1a", 1)
claim("Q1a claims", float(np.mean(XL == XR)) == 0.0 and OMG == 2 and abs(float(np.mean(np.abs(XL - XR) < 1e-9))) < 1e-5,
      "in 10^6 trials the two jumps never coincide exactly; the diagonal has area 0 (still a possible point)")
num("Q1a", 2, sp.integrate(0, (x, 0, 1)), float(np.mean(XL == XR)) * 2, 1e-9)
cmp_ = XR <= XL
num("Q1b", 1, sp.integrate(x, (x, 0, 1)), 2 * float(cmp_.mean()), 2 * se_p(.25))
num("Q1b", 2, 2 - sp.integrate(x, (x, 0, 1)), 2 * float((~cmp_).mean()), 2 * se_p(.75))
num("Q1b", 3, R(3, 4), float((~cmp_).mean()), se_p(.75))
num("Q1c", 1, sp.integrate(x, (x, 0, 1)), 2 * float(cmp_.mean()), 2 * se_p(.25))
num("Q1c", 2, R(1, 4), float(cmp_.mean()), se_p(.25))
strip = (XR > XL) & (XR < XL + 1 / 3)
num("Q1d", 1, sp.integrate(R(1, 3), (x, 0, 1)), 2 * float(strip.mean()), 2 * se_p(1 / 6))
num("Q1d", 2, R(1, 6), float(strip.mean()), se_p(1 / 6))

# ============================================================ Q2: y^2 + 2*X1*y + X2 = 0, two fair dice
pairs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
disc = lambda a, b: a * a - b
cplx = [s for s in pairs if disc(*s) < 0]
real = [s for s in pairs if disc(*s) >= 0]
isq = lambda d: d >= 0 and int(math.isqrt(d)) ** 2 == d
integ = [s for s in pairs if isq(disc(*s))]
D1 = rng.integers(1, 7, N); D2 = rng.integers(1, 7, N)
mc_c = D1 ** 2 < D2
mc_i = np.isin(D1 * D1 - D2, [0, 1, 4, 9, 16, 25])
# roots are really complex / integer (symbolic cross-check on the pairs)
yy = sp.Symbol("y")
cx_sym = [s for s in pairs if any(not r.is_real for r in sp.roots(yy ** 2 + 2 * s[0] * yy + s[1], yy))]
in_sym = [s for s in pairs if all(r.is_integer for r in sp.roots(yy ** 2 + 2 * s[0] * yy + s[1], yy)) and len(sp.roots(yy ** 2 + 2 * s[0] * yy + s[1], yy)) > 0]
claim("Q2 roots", sorted(cx_sym) == sorted(cplx) and sorted(in_sym) == sorted(integ) and sorted(integ) == [(1, 1), (2, 3), (2, 4), (3, 5)],
      "sympy roots agree with the discriminant rules; B={11,23,24,35}")
argued("Q2a", 0)
claim("Q2a claims", len([s for s in pairs if s[0] < s[1]]) == 15 and len([s for s in pairs if disc(*s) > 0]) == 27 and (2, 3) not in cplx and len(cplx) == 7,
      "X1<X2 has 15 pairs, X1^2>X2 has 27, the complex rule has 7")
num("Q2a", 1, len(cplx), float(mc_c.sum()) / N * 36, 36 * se_p(7 / 36))
num("Q2a", 2, Fr(len(cplx), 36), float(mc_c.mean()))
argued("Q2b", 0)
claim("Q2b claims", len([s for s in pairs if disc(*s) > 0]) != len(integ) and (2, 1) not in integ and (2, 2) not in integ and (1, 1) in integ and (2, 2)[0] % 2 == 0,
      "positive discriminant is not enough ((2,1) -> sqrt 3); parity is not the rule ((2,2) fails, (1,1) works)")
num("Q2b", 1, len(integ), float(mc_i.sum()) / N * 36, 36 * se_p(1 / 9))
num("Q2b", 2, Fr(len(integ), 36), float(mc_i.mean()))
opts_c = [float(Fr(1)), 0.0, float(Fr(len(integ), 36) * Fr(len(real), 36))]
claim("Q2c claims", all(s in real for s in integ) and len(set(integ)) > 0 and Fr(len(integ), 36) * Fr(29, 36) != Fr(len(integ), 36),
      "every integer-root pair has real roots (B subset of real); product 29/324 != 1/9")
argued("Q2c", 0)
mc_r = D1 ** 2 >= D2
num("Q2c", 1, Fr(len(real), 36), float(mc_r.mean()))
num("Q2c", 2, Fr(len([s for s in integ if s in real]), 36), float((mc_i & mc_r).mean()))
num("Q2c", 3, Fr(len([s for s in integ if s in real]), len(real)), float(mc_i[mc_r].mean()), se_p(4 / 29, int(mc_r.sum())))
argued("Q2d", 0)
c3 = [s for s in pairs if s[0] == 3]
claim("Q2d claims", [s for s in c3 if isq(disc(*s))] == [(3, 5)] and [9 - b for _, b in c3] == [8, 7, 6, 5, 4, 3] and 9 > 6,
      "with X1=3 only X2=5 gives a perfect square (9-5=4); X2=9 is not a die face")
m3 = D1 == 3
num("Q2d", 1, Fr(len(c3), 36), float(m3.mean()))
num("Q2d", 2, Fr(len([s for s in c3 if isq(disc(*s))]), 36), float((mc_i & m3).mean()))
num("Q2d", 3, Fr(len([s for s in c3 if isq(disc(*s))]), len(c3)), float(mc_i[m3].mean()), se_p(1 / 6, int(m3.sum())))
rts = sp.roots(yy ** 2 + 6 * yy + 5, yy)
num("Q2d", 4, max(rts))

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


# ============================================================ Q4: f(x) = a(b^2 - x^2) on [-b, b]; a=3/4, b=1
a_, b_, xx = sp.symbols("a b xx", positive=True)
fxp = a_ * (b_ ** 2 - xx ** 2)
nrm = sp.integrate(fxp, (xx, -b_, b_))
var = sp.integrate(xx ** 2 * fxp, (xx, -b_, b_))
half = sp.integrate(xx * fxp, (xx, 0, b_))
argued("Q4a", 0)
claim("Q4a claims", sp.integrate(xx * fxp, (xx, -b_, b_)) == 0 and sp.simplify(half - a_ * b_ ** 4 / 4) == 0, "E[X]=0 for all a,b; half-range integral is a b^4/4")
num("Q4a", 1, half.subs({a_: R(3, 4), b_: 1}))
num("Q4a", 2, sp.integrate(xx * fxp, (xx, -b_, b_)).subs({a_: R(3, 4), b_: 1}))
argued("Q4b", 0)
sol = sp.solve([sp.Eq(nrm, 1), sp.Eq(var, R(3, 15))], [a_, b_], dict=True)
claim("Q4b claims", sol == [{a_: R(3, 4), b_: 1}] and sp.simplify(nrm - 4 * a_ * b_ ** 3 / 3) == 0 and sp.simplify(var - 4 * a_ * b_ ** 5 / 15) == 0,
      "normalization 4ab^3/3=1, variance 4ab^5/15; unique positive solution a=3/4, b=1; E[X]=0 gives no equation")
num("Q4b", 1, sp.solve(sp.Eq(var / nrm * 5 / 1, 1), b_)[0] if False else sol[0][b_])
num("Q4b", 2, sol[0][a_])
fc = lambda t: sp.integrate(R(3, 4) * (1 - xx ** 2), (xx, -1, R(t)))
u = rng.random(N)
# sample X by rejection from the parabola on (-1,1)
cand = -1 + 2 * rng.random(3 * N); acc = rng.random(3 * N) < (1 - cand ** 2)
Xp = cand[acc][:N]
num("Q4c", 0, fc(0), float(np.mean(Xp <= 0)))
num("Q4c", 1, fc(R(1, 2)), float(np.mean(Xp <= .5)))
num("Q4c", 2, fc(-R(1, 2)), float(np.mean(Xp <= -.5)))
rec("Q4 MC", abs(Xp.mean()) <= 4 * Xp.std() / math.sqrt(N) and abs(Xp.var() - .2) < .003, "mc E[X]=%.5f var=%.5f (0 and 1/5)" % (Xp.mean(), Xp.var()))
num("Q4d", 0, fc(1) - fc(-1), float(np.mean(np.abs(Xp) < 1)))
num("Q4d", 1, fc(R(3, 4)), float(np.mean(Xp <= .75)))
num("Q4d", 2, (fc(1) - fc(R(3, 4))) / (fc(1) - fc(-1)), float(np.mean(Xp > .75)), se_p(11 / 256))

# ============================================================ Q5: Poisson thinning, lambda=3, p=0.4
lam, pt_ = 3.0, 0.4
Ysamp = rng.poisson(lam, N)
Xsamp = rng.binomial(Ysamp, pt_)
pois = lambda m, k: math.exp(-m) * m ** k / math.factorial(k)
argued("Q5a", 0)
claim("Q5a claims", abs(sum(pois(lam, k) * (1 - pt_) ** k for k in range(120)) - math.exp(-lam * pt_)) < 1e-12, "sum_j Poisson(3,j) (0.6)^j = e^{-1.2}: thinning gives Poisson(p lambda)")
num("Q5a", 1, Fr(216, 1000), float(np.mean(rng.binomial(3, pt_, N) == 0)))
num("Q5a", 2, math.exp(-1.2), float(np.mean(Xsamp == 0)))
argued("Q5b", 0)
claim("Q5b claims", abs(sum(1.2 ** k / math.factorial(k) for k in range(80)) - math.exp(1.2)) < 1e-12, "the series is exp(x), not a geometric series")
num("Q5b", 1, math.exp(1.2))
num("Q5b", 2, math.exp(-1.2) * math.exp(1.2))
argued("Q5c", 0)
claim("Q5c claims", abs(Xsamp.mean() - 1.2) < 4 * Xsamp.std() / math.sqrt(N) and abs(Xsamp.var() - 1.2) < 0.01 and abs(1.2 * 0.6 - 1.2) > 0.1,
      "mc mean=%.4f var=%.4f both 1.2; binomial-style variance 0.72 is wrong" % (Xsamp.mean(), Xsamp.var()))
num("Q5c", 1, Fr(6, 5), float(Xsamp.mean()), float(Xsamp.std()) / math.sqrt(N))
num("Q5c", 2, Fr(6, 5), float(Xsamp.var()), 0.01)
PX2 = pois(1.2, 2); PY4 = pois(3, 4)
PXgY = math.comb(4, 2) * 0.4 ** 2 * 0.6 ** 2
joint = PXgY * PY4
cond = joint / PX2
opts("Q5d", 0, [cond, PXgY, PY4], cond)
num("Q5d", 1, PX2, float(np.mean(Xsamp == 2)))
num("Q5d", 2, joint, float(np.mean((Xsamp == 2) & (Ysamp == 4))))
sel = Xsamp == 2
num("Q5d", 3, cond, float(np.mean(Ysamp[sel] == 4)), se_p(cond, int(sel.sum())))
rec("Q5d closed form", abs(cond - pois(1.8, 2)) < 1e-12, "P(Y=N|X=n) = Poisson(lambda(1-p)) at N-n: %.6f" % cond)

# ============================================================ Q6: Q1 = D(AB u C), Q2 = D(CB u A); p=0.6
q1w = lambda s: bool(s[3] and ((s[0] and s[1]) or s[2]))
q2w = lambda s: bool(s[3] and ((s[2] and s[1]) or s[0]))
p6 = Fr(3, 5)
def prob(f, g=lambda s: True):
    tot = Fr(0)
    for s in itertools.product((0, 1), repeat=4):
        if f(s) and g(s):
            tot += math.prod(p6 if v else 1 - p6 for v in s)
    return tot


U = rng.random((N, 4)) < .6
A_, B_, C_, D_ = (U[:, i] for i in range(4))
m1 = D_ & ((A_ & B_) | C_); m2 = D_ & ((C_ & B_) | A_)
P1 = prob(q1w); PU = prob(lambda s: q1w(s) or q2w(s)); PI = prob(lambda s: q1w(s) and q2w(s)); Pall = p6 ** 4
opts("Q6a", 0, [float(P1), float(prob(lambda s: s[3] and (s[0] or s[1] or s[2]))), float(Pall)], float(P1))
num("Q6a", 1, prob(lambda s: (s[0] and s[1]) or s[2]), float(((A_ & B_) | C_).mean()))
num("Q6a", 2, P1, float(m1.mean()))
opts("Q6b", 0, [float(PU), float(prob(lambda s: s[3] and (s[0] or s[1] or s[2]))), float(prob(lambda s: s[3] and s[0] and s[2]))], float(PU))
claim("Q6b union", all((q1w(s) or q2w(s)) == bool(s[3] and (s[0] or s[2])) for s in itertools.product((0, 1), repeat=4)), "Q1 u Q2 = D(A u C) for every state, B irrelevant")
num("Q6b", 1, 1 - (1 - p6) ** 2, float((A_ | C_).mean()))
num("Q6b", 2, PU, float((m1 | m2).mean()))
opts("Q6c", 0, [float(2 * P1 - PU), float(P1 * P1), float(PU - P1)], float(PI))
num("Q6c", 1, P1, float(m1.mean()))
num("Q6c", 2, PI, float((m1 & m2).mean()))
num("Q6c", 3, PI / P1, float(m2[m1].mean()), se_p(float(PI / P1), int(m1.sum())))
argued("Q6d", 0)
claim("Q6d claims", q1w((1, 1, 1, 1)) and q2w((1, 1, 1, 1)) and Pall != 1 and PI != Pall, "all-working state satisfies both circuits; p^4=0.1296 and P(Q1^Q2)=0.3888 are unconditional")
num("Q6d", 1, Pall, float((A_ & B_ & C_ & D_).mean()))
num("Q6d", 2, PI, float((m1 & m2).mean()))
num("Q6d", 3, Pall / PI, float((A_ & B_ & C_ & D_)[m1 & m2].mean()), se_p(1 / 3, int((m1 & m2).sum())))
rec("Q6 closed forms", P1 == p6 ** 2 * (1 + p6 - p6 ** 2) and PU == p6 ** 2 * (2 - p6) and PI == p6 ** 3 * (3 - 2 * p6), "shipped closed forms = enumeration at p=0.6")

finish()
