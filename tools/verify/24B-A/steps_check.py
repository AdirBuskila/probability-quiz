# -*- coding: utf-8 -*-
"""Verification of the guided steps of 24B-A (probability). Run: PYTHONUTF8=1 py tools/verify/24B-A/steps_check.py

Reads tools/raw/24B-A.json (written by tools/gen/gen_24B-A.py) and re-derives every NUMERIC step independently:
  EXACT : fractions / itertools enumeration / sympy, compared with the stored answer (within 5e-5, and <= tol);
  MC    : Monte Carlo (10^6 trials) within 4 standard errors of the exact value, where a sim applies.
Every CHOICE step whose options are formulas or probabilities is evaluated numerically: the correct option must equal
the exact value and every distractor must differ. Pure reasoning choices are listed as ARGUED (their distractor claims
are verified by the explicit claim checks at the bottom). Exits 1 on any failure. ASCII output.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

CODE = "24B-A"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    k = "Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))
    BYID[k] = q
N = 1_000_000
rng = np.random.default_rng(20240716)
rows = []
fails = 0


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
    ex = float(exact)
    ok_ex = abs(s["answer"] - ex) <= 5e-5 and abs(s["answer"] - ex) <= s["tol"] + 1e-12
    ok_mc = True
    info = "answer=%s exact=%.6f" % (s["answer"], ex)
    if mc is not None:
        ok_mc = abs(mc - ex) <= 4 * (se if se is not None else se_p(ex))
        info += " mc=%.6f" % mc
    rec("%s step%d numeric" % (qid, idx), ok_ex and ok_mc, info)


def opts(qid, idx, vals, target):
    """choice step whose options are numbers: vals[i] is the numeric value of option i."""
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "choice" and len(vals) == len(s["options"]), (qid, idx)
    ci = "abcdefgh".index(s["correctId"])
    good = abs(vals[ci] - target) <= 1e-9 or abs(vals[ci] - target) <= 4 * se_p(target)
    bad = [i for i, v in enumerate(vals) if i != ci and abs(v - target) <= 1e-3]
    rec("%s step%d choice-values" % (qid, idx), good and not bad, "values=%s target=%.6f" % (["%.4f" % v for v in vals], target))


def argued(qid, idx):
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "choice"
    rec("%s step%d choice-argued" % (qid, idx), True, "reasoning choice; claims verified below")


# ============================================================ Q1 (L = 1)
X = rng.random(N); Y = rng.random(N)
x, y = sp.symbols("x y")
one = sp.integrate(1, (x, 0, 1), (y, 0, 1))
for q in ("Q1a", "Q1b", "Q1c", "Q1d", "Q1e"):
    num(q, 0, one)
num("Q1a", 1, sp.integrate(1, (x, 0, sp.Rational(1, 3)), (y, 0, 1)), float(np.mean(X < 1 / 3)))
num("Q1b", 1, sp.integrate(1, (x, 0, 1), (y, sp.Rational(1, 4), 1)), float(np.mean(Y > .25)))
corner = sp.integrate(1, (x, sp.Rational(4, 3) - y, 1), (y, sp.Rational(1, 3), 1))
num("Q1c", 1, corner, float(np.mean(X + Y > 4 / 3)))
num("Q1c", 2, 1 - corner, float(np.mean(X + Y <= 4 / 3)))
Z = np.minimum(X, Y)
opts("Q1d", 1, [float(np.mean(Z < 1 / 3)), float(np.mean(np.maximum(X, Y) < 1 / 3)), float(np.mean(X + Y < 1 / 3))], 5 / 9)
num("Q1d", 2, sp.Rational(2, 3) ** 2, float(np.mean((X >= 1 / 3) & (Y >= 1 / 3))))
num("Q1d", 3, 1 - sp.Rational(2, 3) ** 2, float(np.mean(Z < 1 / 3)))
# conditional: the area of {X>1/4} and of the intersection (piecewise integration)
num("Q1e", 1, sp.integrate(1, (x, sp.Rational(1, 4), 1), (y, 0, 1)), float(np.mean(X > .25)))
inter = sp.integrate(1, (x, sp.Rational(1, 4), sp.Rational(1, 2)), (y, 0, 1)) + sp.integrate(1, (x, sp.Rational(1, 2), 1), (y, 0, sp.Rational(1, 2)))
num("Q1e", 2, inter, float(np.mean((Z < .5) & (X > .25))))
sel = X > .25
num("Q1e", 3, inter / sp.Rational(3, 4), float(np.mean((Z < .5) & sel) / np.mean(sel)), math.sqrt(2 / 3 * 1 / 3 / sel.sum()))

# ============================================================ Q2 (digits 0..9, without replacement)
digs = list(range(10))
P3 = lambda k: Fr(sum(1 for s in itertools.permutations(digs, k) if s[-1] == 3), math.perm(10, k))
M = np.argsort(rng.random((N, 10), dtype=np.float32), axis=1)
num("Q2a", 1, P3(1), float(np.mean(M[:, 0] == 3)))
argued("Q2a", 0)
perm2 = list(itertools.permutations(digs, 2)); perm3 = list(itertools.permutations(digs, 3))
num("Q2b", 1, Fr(sum(1 for s in perm2 if s[0] != 3), len(perm2)), float(np.mean(M[:, 0] != 3)))
fn = [s for s in perm2 if s[0] != 3]
num("Q2b", 2, Fr(sum(1 for s in fn if s[1] == 3), len(fn)), float(np.mean(M[M[:, 0] != 3][:, 1] == 3)),
    se_p(1 / 9, int((M[:, 0] != 3).sum())))
num("Q2b", 3, P3(2), float(np.mean(M[:, 1] == 3)))
argued("Q2b", 0)
nn = [s for s in perm3 if s[0] != 3 and s[1] != 3]
num("Q2c", 1, Fr(len(nn), len(perm3)), float(np.mean((M[:, 0] != 3) & (M[:, 1] != 3))))
num("Q2c", 2, Fr(sum(1 for s in nn if s[2] == 3), len(nn)), None)
num("Q2c", 3, P3(3), float(np.mean(M[:, 2] == 3)))
argued("Q2c", 0)
# 9! and 10! by brute force over all 10! permutations
last3 = 0; tot = 0
for p_ in itertools.permutations(digs):
    tot += 1
    last3 += (p_[-1] == 3)
num("Q2d", 1, last3)
num("Q2d", 2, tot)
num("Q2d", 3, Fr(last3, tot), float(np.mean(M[:, 9] == 3)))
rec("Q2d step0 choice-values", Fr(last3, tot) == Fr(1, 10) and abs(0.9 ** 9 * 0.1 - 0.1) > 0.05,
    "uniform perms=%s geometric=%.4f" % (Fr(last3, tot), 0.9 ** 9 * 0.1))

# ============================================================ Q3 (X,Y ~ Ber(p) independent)
Xs, Ys = sp.symbols("X Y")
Qm = sp.Matrix([[Xs, -Xs ** 2], [Ys ** 2, Xs - Ys]])
DET = lambda a, b: Qm.det().subs({Xs: a, Ys: b}); TR = lambda a, b: Qm.trace().subs({Xs: a, Ys: b})
p = Fr(3, 10)
pm = {0: 1 - p, 1: p}
joint = {}
for a in (0, 1):
    for b in (0, 1):
        joint[(int(DET(a, b)), int(TR(a, b)))] = joint.get((int(DET(a, b)), int(TR(a, b))), 0) + pm[a] * pm[b]
Ex = lambda f: sum(pr * f(d, t) for (d, t), pr in joint.items())
ED, ET = Ex(lambda d, t: d), Ex(lambda d, t: t)
VD = Ex(lambda d, t: d * d) - ED ** 2; VT = Ex(lambda d, t: t * t) - ET ** 2
EDT = Ex(lambda d, t: d * t); COV = EDT - ED * ET
Xm = (rng.random(N) < .3).astype(int); Ym = (rng.random(N) < .3).astype(int)
Dm = Xm * (Xm - Ym) + Xm ** 2 * Ym ** 2; Tm = Xm + (Xm - Ym)
num("Q3a", 1, TR(0, 1))
num("Q3a", 2, joint[(1, 2)], float(np.mean((Dm == 1) & (Tm == 2))))
dvals = sorted({d for d, t in joint}); tvals = sorted({t for d, t in joint})
num("Q3a", 3, len(dvals) * len(tvals) - len(joint))
rec("Q3a step0 claims", dvals == [0, 1] and tvals == [-1, 0, 1, 2] and joint.get((0, 1), 0) == 0 and
    (sum(pr for (d, t), pr in joint.items() if d == 0) * sum(pr for (d, t), pr in joint.items() if t == 1)) > 0,
    "support D=%s T=%s; P(0,1)=0 but marginal product>0" % (dvals, tvals))
rec("Q3b step0 claims", Ex(lambda d, t: d) == p and Fr(sum(pr for (d, t), pr in joint.items() if d == 1)) == p and p ** 2 != p and max(dvals) == 1,
    "P(D=1)=%s != p^2=%s; D in {0,1}" % (p, p ** 2))
num("Q3b", 1, VD, float(np.var(Dm)), math.sqrt(float(VD) ** 2 * 2 / N))
vopt = [float(4 * p * (1 - p) + p * (1 - p)), float(2 * p * (1 - p) - p * (1 - p)), float(p * (1 - p))]
opts("Q3c", 0, vopt, float(VT))
num("Q3c", 1, ET, float(np.mean(Tm)))
num("Q3c", 2, VT, float(np.var(Tm)), math.sqrt(float(VT) ** 2 * 2 / N))
num("Q3d", 0, EDT, float(np.mean(Dm * Tm)))
num("Q3d", 1, ED * ET)
num("Q3d", 2, COV, float(np.mean(Dm * Tm) - np.mean(Dm) * np.mean(Tm)), 0.004)
num("Q3e", 0, joint.get((0, 1), 0), float(np.mean((Dm == 0) & (Tm == 1))), 1e-6)
PD0 = sum(pr for (d, t), pr in joint.items() if d == 0); PT1 = sum(pr for (d, t), pr in joint.items() if t == 1)
num("Q3e", 1, PD0 * PT1)
rec("Q3e step2 verdict", joint.get((0, 1), 0) != PD0 * PT1, "joint != product -> dependent")
num("Q3f", 0, COV, None)
rec("Q3f step1 claims", COV != 0, "cov=%s != 0 (uncorrelated would need cov=0)" % COV)

# ============================================================ Q4 (a, b of the pdf)
a_, b_ = sp.symbols("a b", positive=True)
fpieces = [(-a_, 0, -sp.Symbol("z") / a_), (0, a_, sp.Symbol("z") / a_), (a_, b_, 1)]
zz = sp.Symbol("z")
norm = sum(sp.integrate(f, (zz, lo, hi)) for lo, hi, f in fpieces)
mean = sum(sp.integrate(zz * f, (zz, lo, hi)) for lo, hi, f in fpieces)
sol = sp.solve([sp.Eq(norm, 1), sp.Eq(mean, sp.Rational(3, 8))], [a_, b_], dict=True)
rec("Q4a solve", sol == [{a_: sp.Rational(1, 2), b_: 1}], str(sol))
bsol = sp.solve(sp.Eq(norm, 1), b_)
rec("Q4a step0 claims", bsol == [1] and sp.simplify(mean.subs(b_, 1) - (1 - a_ ** 2) / 2) == 0, "normalization gives b=1 for every a; E[Z]=(1-a^2)/2 depends on a")
num("Q4a", 1, sp.solve(sp.Eq(norm, 1), b_)[0])
num("Q4a", 2, sp.Rational(1, 4))
num("Q4a", 3, sol[0][a_])
# MC of E[Z] at a=1/2, b=1: mixture sampling
u = rng.random(N)
Zs = np.empty(N)
k1 = u < .25; k2 = (u >= .25) & (u < .5); k3 = u >= .5
Zs[k1] = -0.5 * np.sqrt(rng.random(k1.sum()))
Zs[k2] = 0.5 * np.sqrt(rng.random(k2.sum()))
Zs[k3] = 0.5 + 0.5 * rng.random(k3.sum())
rec("Q4a MC mean", abs(Zs.mean() - 0.375) <= 4 * Zs.std() / math.sqrt(N), "mc E[Z]=%.5f" % Zs.mean())
# cdf
t_ = sp.Symbol("t")
f_ = {"l": -2 * zz, "r": 2 * zz}
Fm = lambda t: (sp.integrate(-2 * zz, (zz, -sp.Rational(1, 2), t)) if t < 0 else
                sp.Rational(1, 4) + (sp.integrate(2 * zz, (zz, 0, t)) if t < sp.Rational(1, 2) else sp.Rational(1, 4))
                + (sp.integrate(1, (zz, sp.Rational(1, 2), t)) if t >= sp.Rational(1, 2) else 0))
num("Q4b", 0, Fm(sp.Integer(0)), float(np.mean(Zs <= 0)))
tq = sp.Rational(1, 4)
opts("Q4b", 1, [float(sp.Rational(1, 4) + tq ** 2), float(tq ** 2), float(sp.Rational(1, 4) - tq ** 2), float(2 * tq)], float(Fm(tq)))
num("Q4b", 2, Fm(tq), float(np.mean(Zs <= .25)))
num("Q4b", 3, Fm(sp.Rational(3, 4)), float(np.mean(Zs <= .75)))
den = Fm(sp.Rational(1, 2)) - Fm(-sp.Rational(1, 2)); numr = Fm(sp.Rational(1, 2)) - Fm(sp.Rational(1, 4))
sel = np.abs(Zs) < .5
num("Q4c", 0, den, float(np.mean(sel)))
num("Q4c", 1, numr, float(np.mean((Zs > .25) & (Zs < .5))))
num("Q4c", 2, numr / den, float(np.mean(Zs[sel] > .25)), math.sqrt(.375 * .625 / sel.sum()))

# ============================================================ Q5 (sizes 2,3,7)
sizes = [2, 3, 7]; n = sum(sizes)
fam = rng.integers(0, 3, N)
szX = np.array(sizes)[fam]
ppl = np.repeat(sizes, sizes)                 # one entry per participant: the size of his family
szY = ppl[rng.integers(0, n, N)]
EX = Fr(sum(sizes), 3); EX2 = Fr(sum(s * s for s in sizes), 3); VX = EX2 - EX ** 2
EY = Fr(sum(s * s for s in sizes), n)
opts("Q5a", 0, [1 / 3, 7 / 12, 7 / 3], float(np.mean(szX == 7)))
num("Q5a", 1, Fr(1, 3), float(np.mean(szX == 7)))
num("Q5a", 2, EX, float(szX.mean()), float(szX.std()) / math.sqrt(N))
opts("Q5b", 0, [7 / 12, 1 / 3, 49 / 62], float(np.mean(szY == 7)))
num("Q5b", 1, Fr(7, n), float(np.mean(szY == 7)))
num("Q5b", 2, EY, float(szY.mean()), float(szY.std()) / math.sqrt(N))
num("Q5c", 0, VX, float(szX.var()), float(szX.var()) * math.sqrt(2 / N) * 2)
num("Q5c", 1, EY / EX, float(szY.mean() / szX.mean()), 0.004)
rec("Q5c step2 claims", EY / EX == 1 + VX / EX ** 2 and EY / EX > 1, "E[Y]/E[X]=%s=1+Var/E^2" % (EY / EX))
rec("Q5a-b claims", abs(sum(s / n for s in sizes) - 1) < 1e-12 and sum(Fr(s, 3) for s in sizes) != 1, "n_i/n sums to 1, n_i/N does not")

# ============================================================ Q6 (circuits; p=0.6 on A..D, q=0.5 on E)
pp, qq = Fr(3, 5), Fr(1, 2)
pr_ = {"A": pp, "B": pp, "C": pp, "D": pp, "E": qq}
Q1f = lambda e: e["D"] and ((e["A"] and e["B"]) or e["C"])
Q2f = lambda e: e["D"] and (e["A"] or (e["E"] and e["B"]))
def prob(f, given=None, fixed=None):
    tot = Fr(0); den_ = Fr(0)
    for bits in itertools.product((0, 1), repeat=5):
        e = dict(zip("ABCDE", bits))
        if fixed and any(e[k] != v for k, v in fixed.items()):
            continue
        w = Fr(1)
        for k, v in e.items():
            w *= pr_[k] if v else 1 - pr_[k]
        if given is None or given(e):
            den_ += w
            tot += w if f(e) else 0
    return tot / den_ if given is not None else tot
U = rng.random((N, 5)); E5 = {k: (U[:, i] < float(pr_[k])) for i, k in enumerate("ABCDE")}
q1m = E5["D"] & ((E5["A"] & E5["B"]) | E5["C"]); q2m = E5["D"] & (E5["A"] | (E5["E"] & E5["B"]))
parallel_abc = (E5["A"] & E5["B"]) | E5["C"]
num("Q6a", 1, Fr(1) - (1 - pp ** 2) * (1 - pp), float(np.mean(parallel_abc)))
num("Q6a", 2, prob(Q1f), float(np.mean(q1m)))
opts("Q6a", 0, [float(prob(Q1f)), float(pp * (1 - (1 - pp) ** 3)), float(pp ** 4)], float(prob(Q1f)))
both = lambda e: Q1f(e) and Q2f(e)
opts("Q6b", 0, [float(prob(both)), float(prob(Q1f) * prob(Q2f)), float(prob(Q1f) + prob(Q2f))], float(prob(both)))
num("Q6b", 1, prob(both, fixed={"A": 1}) / pp, float(np.mean((q1m & q2m)[E5["A"]])))
num("Q6b", 2, prob(both, fixed={"A": 0}) / (1 - pp), float(np.mean((q1m & q2m)[~E5["A"]])))
num("Q6b", 3, prob(both), float(np.mean(q1m & q2m)))
num("Q6c", 0, prob(Q1f), float(np.mean(q1m)))
num("Q6c", 1, prob(both), float(np.mean(q1m & q2m)))
num("Q6c", 2, prob(Q2f, given=Q1f), float(np.mean(q2m[q1m])), math.sqrt(.7742 * .2258 / q1m.sum()))
# the official closed forms agree with the enumeration (formula sheet of the key)
p_, q_ = pp, qq
rec("Q6 formulas", prob(Q1f) == p_ ** 2 * (1 + p_ - p_ ** 2) and prob(both) == p_ ** 3 * (1 + (1 - p_) * (1 + q_)), "official closed forms = enumeration")

# ---------------------------------------------------------------- report
for tag, ok, info in rows:
    print("%s %-26s %s" % ("ok  " if ok else "FAIL", tag, info))
steps_total = sum(len(q.get("steps", [])) for q in RAW["questions"])
covered = sum(1 for t, _, _ in rows if " step" in t)
print("steps in raw: %d; checked step rows: %d; failures: %d" % (steps_total, covered, fails))
sys.exit(1 if fails else 0)
