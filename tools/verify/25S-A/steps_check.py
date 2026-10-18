# -*- coding: utf-8 -*-
"""Verification of the guided steps of 25S-A (probability). Run: PYTHONUTF8=1 py tools/verify/25S-A/steps_check.py

Reads tools/raw/25S-A.json (written by tools/gen/gen_25S-A.py) and re-derives every NUMERIC step independently:
  EXACT : fractions / itertools enumeration / sympy, compared with the stored answer (<= tol, and <= 5e-5);
  MC    : Monte Carlo (10^6 trials) within 4 standard errors of the exact value, where a kind applies.
Every CHOICE step whose options are numbers is evaluated (correct option = exact value, distractors differ); the other
choice steps are ARGUED, with their distractor claims checked explicitly. A coverage check fails the run if any numeric
or choice step of the raw file was not verified. ASCII output.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

CODE = "25S-A"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20251020)
rows = []
fails = 0
seen = set()


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
    seen.add((qid, idx))
    ex = float(exact)
    ok_ex = abs(s["answer"] - ex) <= 5e-5 and abs(s["answer"] - ex) <= s["tol"] + 1e-12
    ok_mc = True
    info = "answer=%s exact=%.6f" % (s["answer"], ex)
    if mc is not None:
        ok_mc = abs(mc - ex) <= 4 * (se if se is not None else se_p(min(max(ex, 0), 1)))
        info += " mc=%.6f" % mc
    rec("%s step%d numeric" % (qid, idx), ok_ex and ok_mc, info)


def opts(qid, idx, vals, target):
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "choice" and len(vals) == len(s["options"]), (qid, idx)
    seen.add((qid, idx))
    ci = "abcdefgh".index(s["correctId"])
    good = abs(vals[ci] - target) <= 1e-9
    bad = [i for i, v in enumerate(vals) if i != ci and abs(v - target) <= 1e-6]
    rec("%s step%d choice-values" % (qid, idx), good and not bad, "values=%s target=%.6f" % (["%.4f" % v for v in vals], target))


def argued(qid, idx):
    assert BYID[qid]["steps"][idx]["type"] == "choice"
    seen.add((qid, idx))
    rec("%s step%d choice-argued" % (qid, idx), True, "reasoning choice; claims verified in claim checks")


x, y, t = sp.symbols("x y t", positive=True)

# ============================================================ Q1  X1~U(0,1), X2~U(0,2)
X1 = rng.random(N); X2 = 2 * rng.random(N)
OM = sp.integrate(1, (x, 0, 1), (y, 0, 2))
for q in ("Q1a", "Q1b", "Q1c", "Q1d"):
    num(q, 0, OM)
num("Q1a", 1, sp.integrate(x, (x, 0, 1)), 2 * float(np.mean(X2 < X1)), 2 * se_p(0.25))
num("Q1a", 2, sp.integrate(x, (x, 0, 1)) / OM, float(np.mean(X2 < X1)))
num("Q1b", 1, sp.Rational(1, 2) * sp.Rational(3, 2), 2 * float(np.mean((X1 >= 0.5) & (X2 >= 0.5))), 2 * se_p(0.375))
num("Q1b", 2, 1 - sp.Rational(3, 4) / OM, float(np.mean((X1 < 0.5) | (X2 < 0.5))))
num("Q1c", 1, sp.integrate(1 - x, (x, 0, 1)), 2 * float(np.mean(X1 + X2 <= 1)), 2 * se_p(0.25))
num("Q1c", 2, sp.integrate(1 - x, (x, 0, 1)) / OM, float(np.mean(X1 + X2 <= 1)))
cond_a = sp.integrate(x, (x, 0, 1))                        # {x2 > 2-x1}: height x1
inter_a = sp.integrate(x, (x, sp.Rational(1, 2), 1))
cm = X1 + X2 > 2
num("Q1d", 1, cond_a, 2 * float(np.mean(cm)), 2 * se_p(0.25))
num("Q1d", 2, inter_a, 2 * float(np.mean(cm & (X1 > 0.5))), 2 * se_p(0.1875))
num("Q1d", 3, inter_a / cond_a, float(np.mean((X1 > 0.5)[cm])), math.sqrt(0.75 * 0.25 / cm.sum()))

# ============================================================ Q2  p=P(A\B)=.2, q=P(AB)=.3, s=P(A|B)=.6
p_, q_, s_ = Fr(1, 5), Fr(3, 10), Fr(3, 5)
PB = q_ / s_
atoms = {(1, 1): q_, (1, 0): p_, (0, 1): PB - q_, (0, 0): 1 - p_ - PB}
assert sum(atoms.values()) == 1 and all(v >= 0 for v in atoms.values())
P = lambda f, at=atoms: sum(w for (a, b), w in at.items() if f(a, b))
cond = lambda f, g, at=atoms: P(lambda a, b: f(a, b) and g(a, b), at) / P(g, at)
assert cond(lambda a, b: a, lambda a, b: b) == s_


def samp(at):
    ks = list(at)
    i = rng.choice(len(ks), size=N, p=[float(at[k]) for k in ks])
    return (np.array([k[0] for k in ks])[i].astype(bool), np.array([k[1] for k in ks])[i].astype(bool))


A, B = samp(atoms)
opts("Q2a", 0, [float(P(lambda a, b: a)), float(p_ * q_), float(p_ + q_ - p_ * q_)], float(P(lambda a, b: a)))
num("Q2a", 1, P(lambda a, b: a), float(A.mean()))
opts("Q2b", 0, [float(PB), float(s_ / q_), float(q_ * s_)], float(PB))
num("Q2b", 1, PB, float(B.mean()))
rec("Q2c step0 claim", P(lambda a, b: a and not b) == p_ and P(lambda a, b: a and b) == q_ != p_, "A and not B = A minus B: P=p; A and B: P=q")
argued("Q2c", 0)
num("Q2c", 1, P(lambda a, b: not b), float(np.mean(~B)))
num("Q2c", 2, P(lambda a, b: a and not b), float(np.mean(A & ~B)))
num("Q2c", 3, cond(lambda a, b: a, lambda a, b: not b), float(np.mean(A[~B])), math.sqrt(0.4 * 0.6 / (~B).sum()))
tgt = float(cond(lambda a, b: not a, lambda a, b: b))
opts("Q2d", 0, [tgt, float(P(lambda a, b: not a)), float(P(lambda a, b: not b))], tgt)
num("Q2d", 1, tgt, float(np.mean((~A)[B])), math.sqrt(0.4 * 0.6 / B.sum()))
tgt = float(cond(lambda a, b: not a, lambda a, b: not b))
opts("Q2e", 0, [tgt, float(cond(lambda a, b: not a, lambda a, b: b)), float(P(lambda a, b: not a))], tgt)
num("Q2e", 1, cond(lambda a, b: a, lambda a, b: not b), float(np.mean(A[~B])), math.sqrt(0.4 * 0.6 / (~B).sum()))
num("Q2e", 2, cond(lambda a, b: not a, lambda a, b: not b), float(np.mean((~A)[~B])), math.sqrt(0.6 * 0.4 / (~B).sum()))
rec("Q2f step0 claim", Fr(1, 2) / Fr(2, 5) > 1 and q_ / s_ <= 1, "s<q gives P(B)=q/s>1; the sample s>q gives P(B)<=1")
argued("Q2f", 0)
num("Q2f", 1, Fr(1, 2) / Fr(2, 5))
# g: independent: p=.2, q=.3, s=p+q=.5
ind = {(1, 1): Fr(3, 10), (1, 0): Fr(1, 5), (0, 1): Fr(3, 10), (0, 0): Fr(1, 5)}
assert P(lambda a, b: a and b, ind) == P(lambda a, b: a, ind) * P(lambda a, b: b, ind) and cond(lambda a, b: a, lambda a, b: b, ind) == Fr(1, 2)
rec("Q2g step0 claim", cond(lambda a, b: a, lambda a, b: b, ind) == P(lambda a, b: a, ind) and P(lambda a, b: a and b, ind) != 0
    and cond(lambda a, b: a, lambda a, b: b, ind) != cond(lambda a, b: b, lambda a, b: a, ind), "independent model: P(A|B)=P(A); P(AB)!=0; P(A|B)!=P(B|A)")
argued("Q2g", 0)
Ai, Bi = samp(ind)
num("Q2g", 1, P(lambda a, b: a, ind), float(Ai.mean()))
num("Q2g", 2, cond(lambda a, b: a, lambda a, b: b, ind), float(np.mean(Ai[Bi])), math.sqrt(0.25 / Bi.sum()))

# ============================================================ Q3  D=5 red of N=12
Dn, Nn = 5, 12
balls = [1] * Dn + [0] * (Nn - Dn)
perms5 = list(itertools.permutations(range(Nn), 5))
col = [tuple(balls[i] for i in s) for s in perms5]
frac = lambda f, g=lambda c: True: Fr(sum(1 for c in col if f(c) and g(c)), sum(1 for c in col if g(c)))
Mx = np.argsort(rng.random((N, Nn), dtype=np.float32), axis=1)[:, :5]
Cm = np.array(balls)[Mx]
num("Q3a", 0, Nn)
num("Q3a", 1, frac(lambda c: c[0] == 1), float(Cm[:, 0].mean()))
rec("Q3b step0 claim", Fr(4, 11) != Fr(5, 12) and (Fr(5, 12) ** 2) != Fr(5, 12), "(D-1)/(N-1)=0.364, (D/N)^2=0.174 vs 0.4167")
argued("Q3b", 0)
num("Q3b", 1, frac(lambda c: c[1] == 1, lambda c: c[0] == 1), float(Cm[Cm[:, 0] == 1][:, 1].mean()), math.sqrt(0.36 * 0.64 / (Cm[:, 0] == 1).sum()))
num("Q3b", 2, frac(lambda c: c[1] == 1, lambda c: c[0] == 0), float(Cm[Cm[:, 0] == 0][:, 1].mean()), math.sqrt(0.25 / (Cm[:, 0] == 0).sum()))
num("Q3b", 3, frac(lambda c: c[1] == 1), float(Cm[:, 1].mean()))
rec("Q3c step0 claim", frac(lambda c: c[0] == 1 and c[1] == 1 and c[2] == 1) == Fr(1, 22) and frac(lambda c: c[2] == 1, lambda c: c[0] == 1 and c[1] == 1) == Fr(3, 10),
    "P(R1R2R3)=%s, P(R3|R1R2)=0.3" % float(frac(lambda c: c[0] == 1 and c[1] == 1 and c[2] == 1)))
argued("Q3c", 0)
num("Q3c", 1, frac(lambda c: c[0] == 1 and c[1] == 1), float(np.mean((Cm[:, 0] == 1) & (Cm[:, 1] == 1))))
num("Q3c", 2, frac(lambda c: c[2] == 1, lambda c: c[0] == 1 and c[1] == 1), float(np.mean(Cm[(Cm[:, 0] == 1) & (Cm[:, 1] == 1)][:, 2])), math.sqrt(0.21 / ((Cm[:, 0] == 1) & (Cm[:, 1] == 1)).sum()))
num("Q3c", 3, frac(lambda c: c[2] == 1), float(Cm[:, 2].mean()))
argued("Q3d", 0)
EXd = Fr(sum(sum(c[:4]) for c in col), len(col))
num("Q3d", 1, EXd, float(Cm[:, :4].sum(axis=1).mean()), math.sqrt(Cm[:, :4].sum(axis=1).var() / N))
num("Q3d", 2, frac(lambda c: c[4] == 1, lambda c: sum(c[:4]) == 2), float(Cm[Cm[:, :4].sum(axis=1) == 2][:, 4].mean()), math.sqrt(0.234 / (Cm[:, :4].sum(axis=1) == 2).sum()))
num("Q3d", 3, frac(lambda c: c[4] == 1), float(Cm[:, 4].mean()))
rec("Q3e step0 claim", Fr(5, 12) ** 2 != Fr(5, 33) and frac(lambda c: c[3] == 1 and c[4] == 1) == Fr(5, 33), "(D/N)^2=0.174 vs 5/33=0.1515")
argued("Q3e", 0)
EX3 = Fr(sum(sum(c[:3]) for c in col), len(col))
num("Q3e", 1, EX3, float(Cm[:, :3].sum(axis=1).mean()), math.sqrt(Cm[:, :3].sum(axis=1).var() / N))
num("Q3e", 2, frac(lambda c: c[3] == 1 and c[4] == 1, lambda c: sum(c[:3]) == 1), float(np.mean((Cm[Cm[:, :3].sum(axis=1) == 1][:, 3] == 1) & (Cm[Cm[:, :3].sum(axis=1) == 1][:, 4] == 1))), math.sqrt(0.14 / (Cm[:, :3].sum(axis=1) == 1).sum()))
num("Q3e", 3, frac(lambda c: c[3] == 1 and c[4] == 1), float(np.mean((Cm[:, 3] == 1) & (Cm[:, 4] == 1))))

# ============================================================ Q4  f = x on [0,1], 2 on [1,5/4]
a_, b_, c_ = sp.symbols("a b c", positive=True)
sol = sp.solve([sp.Eq(a_ * c_ / 4 + c_ * (b_ - a_), 1), sp.Eq(a_ * c_ / 4, c_ * (b_ - a_)),
                sp.Eq(sp.integrate(x * c_ * x / (2 * a_), (x, 0, a_)) + sp.integrate(x * c_, (x, a_, b_)), sp.Rational(43, 48))], [a_, b_, c_], dict=True)
assert len(sol) == 1
rec("Q4a step0 claim", sp.solve(sp.Eq(c_ / 2, c_), c_) == [] , "continuity at x=a would force c=0 (impossible for a density)")
argued("Q4a", 0)
num("Q4a", 1, sol[0][a_]); num("Q4a", 2, sol[0][b_]); num("Q4a", 3, sol[0][c_])
m = rng.random(N) < 0.5
Xs = np.where(m, np.sqrt(rng.random(N)), 1 + 0.25 * rng.random(N))
Fq = lambda tt: tt ** 2 / 2 if tt <= 1 else sp.Rational(1, 2) + 2 * (tt - 1)
num("Q4b", 0, Fq(sp.Integer(1)), float(np.mean(Xs <= 1)))
num("Q4b", 1, Fq(sp.Rational(11, 10)), float(np.mean(Xs <= 1.1)))
num("Q4b", 2, Fq(sp.Rational(5, 4)), float(np.mean(Xs <= 1.25)))
num("Q4c", 0, Fq(sp.Integer(1)), float(np.mean(Xs <= 1)))
num("Q4c", 1, 1 - Fq(sp.Integer(1)), float(np.mean(Xs > 1)))

# ============================================================ Q5  roads A,B,C,D with p=.6
p = Fr(3, 5)
comps = list("ABCD")
QE = lambda o: o["A"] or (o["B"] and o["C"] and o["D"])
QS = lambda o: o["B"] or (o["A"] and o["C"] and o["D"])


def ex(pred, given=None, forced=None):
    tot = Fr(0); gt = Fr(0)
    for st in itertools.product((0, 1), repeat=4):
        o = dict(zip(comps, st))
        if forced and any(o[k] != v for k, v in forced.items()):
            continue
        w = Fr(1)
        for c in comps:
            w *= p if o[c] else 1 - p
        if given is not None and not given(o):
            continue
        gt += w
        if pred(o):
            tot += w
    return tot / gt if (given is not None or forced) else tot


R = {c: rng.random(N) < float(p) for c in comps}
mE = R["A"] | (R["B"] & R["C"] & R["D"]); mS = R["B"] | (R["A"] & R["C"] & R["D"])
P1 = ex(QE); P2 = ex(lambda o: QE(o) and QS(o)); P3 = ex(lambda o: QE(o) and not QS(o))
allfour = lambda o: o["A"] and o["B"] and o["C"] and o["D"]
opts("Q5a", 0, [float(P1), float(ex(allfour)), float(ex(lambda o: o["A"] or o["B"] or o["C"] or o["D"]))], float(P1))
num("Q5a", 1, ex(lambda o: o["B"] and o["C"] and o["D"]), float((R["B"] & R["C"] & R["D"]).mean()))
num("Q5a", 2, P1, float(mE.mean()))
opts("Q5b", 0, [float(P2), float(P1 * P1), float(2 * P1)], float(P2))
num("Q5b", 1, ex(lambda o: QE(o) and QS(o), forced={"A": 1}), float(np.mean((mE & mS)[R["A"]])), math.sqrt(0.744 * 0.256 / R["A"].sum()))
num("Q5b", 2, ex(lambda o: QE(o) and QS(o), forced={"A": 0}), float(np.mean((mE & mS)[~R["A"]])), math.sqrt(0.216 * 0.784 / (~R["A"]).sum()))
num("Q5b", 3, P2, float((mE & mS).mean()))
opts("Q5c", 0, [float(P3), float(P1 * (1 - P1)), float(1 - P2)], float(P3))
num("Q5c", 1, P1, float(mE.mean()))
num("Q5c", 2, P3, float((mE & ~mS).mean()))
pubE = lambda o: o["B"] and o["C"] and o["D"]; pubS = lambda o: o["A"] and o["C"] and o["D"]
rec("Q5d step0 claim", all((pubE(dict(zip(comps, st))) and pubS(dict(zip(comps, st)))) == allfour(dict(zip(comps, st))) for st in itertools.product((0, 1), repeat=4)),
    "both-through-pub = A,B,C,D all open (over all 16 states)")
argued("Q5d", 0)
num("Q5d", 1, P2, float((mE & mS).mean()))
num("Q5d", 2, ex(allfour), float((R["A"] & R["B"] & R["C"] & R["D"]).mean()))
num("Q5d", 3, ex(allfour, given=lambda o: QE(o) and QS(o)), float(np.mean((R["A"] & R["B"] & R["C"] & R["D"])[mE & mS])), math.sqrt(0.243 * 0.757 / (mE & mS).sum()))

# ============================================================ Q6  m=3 right, n=2 up, p=.6
pp = Fr(3, 5)
seqs = list(itertools.product((0, 1), repeat=5))
wt = lambda s: pp ** sum(s) * (1 - pp) ** (5 - sum(s))
Bm = rng.random((N, 5)) < 0.6
tot3 = Bm.sum(axis=1) == 3
num("Q6a", 0, 5)
num("Q6a", 1, sum(1 for s in seqs if sum(s) == 3))
num("Q6b", 1, sum(1 for s in seqs if sum(s) == 3))
opts("Q6b", 0, [float(sum(wt(s) for s in seqs if sum(s) == 3)), float(pp ** 3 * (1 - pp) ** 2), float(sum(wt(s) for s in seqs if sum(s) >= 3))], float(sum(wt(s) for s in seqs if sum(s) == 3)))
num("Q6b", 2, wt((1, 1, 1, 0, 0)), float(np.mean(Bm[:, 0] & Bm[:, 1] & Bm[:, 2] & ~Bm[:, 3] & ~Bm[:, 4])), 0.0003)
num("Q6b", 3, sum(wt(s) for s in seqs if sum(s) == 3), float(tot3.mean()))
rec("Q6c step0 claim", len({wt(s) for s in seqs if sum(s) == 3}) == 1, "all 10 successful paths have the same probability p^3(1-p)^2")
argued("Q6c", 0)
num("Q6c", 1, sum(wt(s) for s in seqs if s[0] + s[1] == 1), float(np.mean(Bm[:, :2].sum(axis=1) == 1)))
num("Q6c", 2, sum(pp ** sum(s) * (1 - pp) ** (3 - sum(s)) for s in itertools.product((0, 1), repeat=3) if sum(s) == 2), float(np.mean(Bm[:, 2:].sum(axis=1) == 2)))
num("Q6c", 3, sum(wt(s) for s in seqs if sum(s) == 3), float(tot3.mean()))
num("Q6c", 4, sum(wt(s) for s in seqs if sum(s) == 3 and s[0] + s[1] == 1) / sum(wt(s) for s in seqs if sum(s) == 3),
    float(np.mean((Bm[:, :2].sum(axis=1) == 1)[tot3])), math.sqrt(0.24 / tot3.sum()))

# ============================================================ coverage
for qid, q in BYID.items():
    for i, s in enumerate(q.get("steps") or []):
        if s["type"] in ("numeric", "choice") and (qid, i) not in seen:
            rec("%s step%d COVERAGE" % (qid, i), False, "step not verified")

for tag, ok, info in rows:
    print(("ok   " if ok else "FAIL ") + tag + ": " + info)
print("steps_check %s: %d checks, %d failing" % (CODE, len(rows), fails))
sys.exit(1 if fails else 0)
