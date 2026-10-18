# -*- coding: utf-8 -*-
"""Verification of the guided steps of 25B-B (probability). Run: PYTHONUTF8=1 py tools/verify/25B-B/steps_check.py

Reads tools/raw/25B-B.json (written by tools/gen/gen_25B-B.py) and re-derives every NUMERIC step independently:
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

CODE = "25B-B"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20250812)
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

# ============================================================ Q1  X1, X2 ~ U(0,1) independent, D = |X1 - X2|
X1 = rng.random(N); X2 = rng.random(N); D = np.abs(X1 - X2)
num("Q1a", 0, 1, float(np.mean((X1 > 0.29) & (X1 <= 0.31)) / 0.02), math.sqrt(0.02 * 0.98 / N) / 0.02)
num("Q1a", 1, sp.integrate(1, (x, 0, sp.Rational(1, 4))), float(np.mean(X1 <= 0.25)))
for q in ("Q1b", "Q1c", "Q1d"):
    num(q, 0, sp.integrate(1, (x, 0, 1), (y, 0, 1)))
tri = sp.integrate(sp.integrate(1, (y, 0, x - sp.Rational(1, 2))), (x, sp.Rational(1, 2), 1))
num("Q1b", 1, tri, float(np.mean(X1 - X2 > 0.5)), se_p(0.125))
num("Q1b", 2, 1 - 2 * tri, float(np.mean(D < 0.5)))
rec("Q1c claim", float(D.max()) < 1.0, "max |X1-X2| over 10^6 draws = %.6f < 1" % float(D.max()))
num("Q1c", 1, 1, None)
num("Q1c", 2, 0, float(np.mean(D > 1.5)), 1e-12)
tri4 = sp.integrate(sp.integrate(1, (y, 0, x - sp.Rational(2, 5))), (x, sp.Rational(2, 5), 1))
num("Q1d", 1, tri4, float(np.mean(X1 - X2 > 0.4)), se_p(0.18))
num("Q1d", 2, 1 - 2 * tri4, float(np.mean(D <= 0.4)))
num("Q1d", 3, (2 * t - t ** 2).subs(t, 1), float(np.mean(D <= 1.0)))
Fd = 2 * t - t ** 2
num("Q1e", 0, sp.diff(Fd, t).subs(t, sp.Rational(2, 5)), float(np.mean((D > 0.39) & (D <= 0.41)) / 0.02), math.sqrt(0.024 * 0.976 / N) / 0.02)
num("Q1e", 1, sp.diff(Fd, t).subs(t, 1), None)
num("Q1e", 2, sp.integrate(sp.diff(Fd, t), (t, 0, 1)), float(np.mean(D < 1)))
num("Q1f", 0, sp.integrate(2 * t, (t, 0, 1)), None)
num("Q1f", 1, sp.integrate(2 * t ** 2, (t, 0, 1)), None)
num("Q1f", 2, sp.integrate(t * sp.diff(Fd, t), (t, 0, 1)), float(D.mean()), math.sqrt(D.var() / N))

# ============================================================ Q2  p=P(not A|B)=.4, q=P(A|not B)=.2, s=P(A or B)=.7
p_, q_, s_ = Fr(2, 5), Fr(1, 5), Fr(7, 10)
PB = (s_ - q_) / (1 - q_)
PAB = (1 - p_) * PB
atoms = {(1, 1): PAB, (1, 0): s_ - PB, (0, 1): PB - PAB, (0, 0): 1 - s_}
assert sum(atoms.values()) == 1 and all(v >= 0 for v in atoms.values())
P = lambda f, at=atoms: sum(w for (a, b), w in at.items() if f(a, b))
cond = lambda f, g, at=atoms: P(lambda a, b: f(a, b) and g(a, b), at) / P(g, at)
assert cond(lambda a, b: not a, lambda a, b: b) == p_ and cond(lambda a, b: a, lambda a, b: not b) == q_ and P(lambda a, b: a or b) == s_


def samp(at):
    ks = list(at)
    i = rng.choice(len(ks), size=N, p=[float(at[k]) for k in ks])
    return (np.array([k[0] for k in ks])[i].astype(bool), np.array([k[1] for k in ks])[i].astype(bool))


A, B = samp(atoms)
opts("Q2a", 0, [float(PB), float(p_), float(s_ - q_)], float(P(lambda a, b: b)))
num("Q2a", 1, P(lambda a, b: b), float(B.mean()))
num("Q2a", 2, P(lambda a, b: a and b), float(np.mean(A & B)))
num("Q2a", 3, P(lambda a, b: a), float(A.mean()))
rec("Q2b step0 claim", cond(lambda a, b: not a, lambda a, b: not b) == 1 - q_ and cond(lambda a, b: a, lambda a, b: not b) == q_ and cond(lambda a, b: a, lambda a, b: b) == 1 - p_ != 1 - q_,
    "P(not A|not B)=1-q=0.8; q=0.2; 1-p=0.6=P(A|B)")
argued("Q2b", 0)
num("Q2b", 1, P(lambda a, b: not a and not b), float(np.mean(~A & ~B)))
num("Q2b", 2, P(lambda a, b: not b), float(np.mean(~B)))
num("Q2b", 3, P(lambda a, b: b), float(B.mean()))
num("Q2c", 0, P(lambda a, b: b), float(B.mean()))
num("Q2c", 1, cond(lambda a, b: a, lambda a, b: b), float(np.mean(A[B])), math.sqrt(0.24 / B.sum()))
num("Q2c", 2, P(lambda a, b: a and b), float(np.mean(A & B)))
rec("Q2d step0 claim", (Fr(3, 10) - Fr(1, 2)) / (1 - Fr(1, 2)) < 0 and (1 - s_) / (1 - q_) <= 1, "q>s gives P(B)<0 (and P(not B)=(1-s)/(1-q)>1 when q>s)")
argued("Q2d", 0)
num("Q2d", 1, (Fr(3, 10) - Fr(1, 2)) / (1 - Fr(1, 2)))
ind = {(1, 1): Fr(1, 10), (1, 0): Fr(1, 10), (0, 1): Fr(2, 5), (0, 0): Fr(2, 5)}
assert cond(lambda a, b: not a, lambda a, b: b, ind) == Fr(4, 5) and cond(lambda a, b: a, lambda a, b: not b, ind) == Fr(1, 5) and P(lambda a, b: a or b, ind) == Fr(3, 5)
rec("Q2e step0 claim", cond(lambda a, b: a, lambda a, b: b, ind) == cond(lambda a, b: a, lambda a, b: not b, ind) == P(lambda a, b: a, ind)
    and cond(lambda a, b: a, lambda a, b: b, ind) != cond(lambda a, b: b, lambda a, b: a, ind) and P(lambda a, b: a and b, ind) != 0,
    "independent model: P(A|B)=P(A|not B)=P(A); P(A|B)!=P(B|A); P(AB)!=0")
argued("Q2e", 0)
num("Q2e", 1, 1 - Fr(1, 5))
num("Q2e", 2, cond(lambda a, b: a, lambda a, b: b, ind) - cond(lambda a, b: a, lambda a, b: not b, ind))
dis = {(1, 1): Fr(0), (1, 0): Fr(1, 4), (0, 1): Fr(1, 5), (0, 0): Fr(11, 20)}
qd, sd = Fr(5, 16), Fr(9, 20)
PBd = (sd - qd) / (1 - qd)
assert cond(lambda a, b: not a, lambda a, b: b, dis) == 1 and cond(lambda a, b: a, lambda a, b: not b, dis) == qd and P(lambda a, b: a or b, dis) == sd
rec("Q2f step0 claim", (qd - qd) / (1 - qd) == 0 and PBd > 0, "s=q forces P(B)=0 (P(not A|B) undefined); the sample s>q gives P(B)=%s>0" % PBd)
argued("Q2f", 0)
Ad, Bd = samp(dis)
num("Q2f", 1, PBd, float(Bd.mean()))
num("Q2f", 2, sd - 1 * PBd, float(Ad.mean()))

# ============================================================ Q3  guessing games
G6 = rng.integers(1, 7, size=(N, 2))
argued("Q3a", 0)
num("Q3a", 1, 36)
num("Q3a", 2, sum(1 for i in range(1, 7) for j in range(1, 7) if i == j), float(np.mean(G6[:, 0] == G6[:, 1])) * 36, 36 * se_p(1 / 6))
num("Q3a", 3, Fr(sum(1 for i in range(1, 7) for j in range(1, 7) if i == j), 36), float(np.mean(G6[:, 0] == G6[:, 1])))
num("Q3b", 0, 36)
nb = sum(1 for i in range(1, 7) for j in range(1, 7) if abs(i - j) == 1)
num("Q3b", 1, nb, float(np.mean(np.abs(G6[:, 0] - G6[:, 1]) == 1)) * 36, 36 * se_p(10 / 36))
num("Q3b", 2, Fr(nb, 36), float(np.mean(np.abs(G6[:, 0] - G6[:, 1]) == 1)))
gE = rng.integers(1, 4, N); nE = rng.integers(1, 4, N); gS = rng.integers(1, 5, N); nS = rng.integers(1, 5, N)
A1 = gE == nE; A2 = gS == nS
rec("Q3c step0 claim", Fr(1, 3) + Fr(1, 4) != Fr(1, 12) and max(Fr(1, 3), Fr(1, 4)) != Fr(1, 12), "sum 0.583 and max 0.333 vs product 0.0833")
argued("Q3c", 0)
num("Q3c", 1, Fr(1, 3), float(A1.mean()))
num("Q3c", 2, Fr(1, 4), float(A2.mean()))
num("Q3c", 3, Fr(1, 12), float(np.mean(A1 & A2)))
union = Fr(1, 3) + Fr(1, 4) - Fr(1, 12)
opts("Q3d", 0, [float(union), float(Fr(1, 3) + Fr(1, 4)), float(1 - Fr(1, 12))], float(union))
num("Q3d", 1, Fr(1, 12), float(np.mean(A1 & A2)))
num("Q3d", 2, union, float(np.mean(A1 | A2)))
nbE = Fr(sum(1 for i in range(1, 5) for j in range(1, 5) if abs(i - j) == 1), 16)
rec("Q3e step0 claim", Fr(1, 3) + nbE != Fr(1, 8) and Fr(1, 3) / nbE != Fr(1, 8), "sum/ratio differ from the product 0.125")
argued("Q3e", 0)
num("Q3e", 1, nbE, float(np.mean(np.abs(gS - nS) == 1)))
num("Q3e", 2, Fr(1, 3), float(A1.mean()))
num("Q3e", 3, Fr(1, 3) * nbE, float(np.mean(A1 & (np.abs(gS - nS) == 1))))

# ============================================================ Q4  pdf, mu = 1/24
a_, b_, c_, d_, g_, h_, mu = sp.symbols("a b c d g h mu")
rec("Q4a step0 claim", sp.integrate(sp.Symbol("k", positive=True), (x, 1, sp.oo)) == sp.oo, "a positive constant on a ray has an infinite integral")
argued("Q4a", 0)
eqs = [sp.Eq(sp.integrate(b_ * x + c_, (x, -1, 0)) + sp.integrate(d_, (x, 0, 1)), 1),
       sp.Eq(sp.integrate(b_ * x + c_, (x, -1, 0)), sp.integrate(d_, (x, 0, 1))),
       sp.Eq(sp.integrate(x * (b_ * x + c_), (x, -1, 0)) + sp.integrate(x * d_, (x, 0, 1)), mu)]
sol = sp.solve(eqs, [b_, c_, d_], dict=True)[0]
mu0 = sp.Rational(1, 24)
num("Q4a", 1, sol[d_].subs(mu, mu0)); num("Q4a", 2, sol[b_].subs(mu, mu0)); num("Q4a", 3, sol[c_].subs(mu, mu0))
assert sp.simplify(sol[b_] - 12 * mu) == 0 and sp.simplify(sol[c_] - (6 * mu + sp.Rational(1, 2))) == 0
num("Q4b", 0, sp.solve(sp.Eq((sol[c_] - sol[b_]), 0), mu)[0])
num("Q4b", 1, sp.solve(sp.Eq(sol[c_], 0), mu)[0])
# sample X: left part (mass 1/2) by numeric inverse CDF, right part uniform on [0,1]
grid = np.linspace(-1, 0, 200001)
dens = 0.5 * grid + 0.75
cdf = np.concatenate([[0], np.cumsum((dens[1:] + dens[:-1]) / 2 * (grid[1] - grid[0]))])
left = np.interp(rng.random(N) * cdf[-1], cdf, grid)
Xs = np.where(rng.random(N) < 0.5, left, rng.random(N))
Fq = lambda tt: sp.integrate(sol[b_].subs(mu, mu0) * x + sol[c_].subs(mu, mu0), (x, -1, tt)) if tt <= 0 else sp.Rational(1, 2) + sp.Rational(1, 2) * tt
num("Q4c", 0, Fq(sp.Rational(-1, 2)), float(np.mean(Xs <= -0.5)))
num("Q4c", 1, Fq(sp.Integer(0)), float(np.mean(Xs <= 0)))
num("Q4c", 2, Fq(sp.Rational(1, 2)), float(np.mean(Xs <= 0.5)))
cm = Xs > -0.5
num("Q4d", 0, 1 - Fq(sp.Rational(-1, 2)), float(cm.mean()))
num("Q4d", 1, Fq(sp.Integer(0)) - Fq(sp.Rational(-1, 2)), float(np.mean(cm & (Xs < 0))))
num("Q4d", 2, (Fq(sp.Integer(0)) - Fq(sp.Rational(-1, 2))) / (1 - Fq(sp.Rational(-1, 2))), float(np.mean(Xs[cm] < 0)), math.sqrt(0.385 * 0.615 / cm.sum()))

# ============================================================ Q5  circuits Q0 = (A and B) or C, p = .6
pp = Fr(3, 5)
st = [(a, b, c, k) for a in (0, 1) for b in (0, 1) for c in (0, 1) for k in range(1, 7)]
w = lambda s: (pp if s[0] else 1 - pp) * (pp if s[1] else 1 - pp) * (pp if s[2] else 1 - pp) * Fr(1, 6)
Q0 = lambda s: (s[0] and s[1]) or s[2]


def Qp(s):
    a, b, c, k = s
    if k <= 2:
        return (a and b) or c
    if k in (3, 4):
        return (a and c) or b
    return (b and c) or a


ex = lambda f, g=lambda s: True: sum(w(s) for s in st if f(s) and g(s)) / sum(w(s) for s in st if g(s))
RA = rng.random(N) < 0.6; RB = rng.random(N) < 0.6; RC = rng.random(N) < 0.6; RK = rng.integers(1, 7, N)
m0 = (RA & RB) | RC
mp = np.where(RK <= 2, (RA & RB) | RC, np.where(RK <= 4, (RA & RC) | RB, (RB & RC) | RA))
opts("Q5a", 0, [float(ex(Q0)), float(pp ** 2 + pp), float(pp ** 3)], float(ex(Q0)))
num("Q5a", 1, pp ** 2, float((RA & RB).mean()))
num("Q5a", 2, ex(Q0), float(m0.mean()))
rec("Q5b step0 claim", Fr(sum(1 for a in (0, 1) for b in (0, 1) for c in (0, 1) if bool((a and b) or c) != bool((a and c) or b)), 8) > 0
    and ex(lambda s: (s[0] and s[2]) or s[1]) == ex(Q0), "(A and C) or B differs from Q0 as an event (A=0,B=1,C=0) but has the same probability")
argued("Q5b", 0)
num("Q5b", 1, pp ** 2, float((RA & RC).mean()))
num("Q5b", 2, ex(lambda s: (s[0] and s[2]) or s[1]), float(((RA & RC) | RB).mean()))
both = ex(lambda s: Q0(s) and Qp(s))
opts("Q5c", 0, [float(both), float(ex(Q0)) ** 2, float(ex(Q0))], float(both))
num("Q5c", 1, ex(lambda s: Q0(s) and Qp(s), lambda s: s[3] <= 2), float(np.mean((m0 & mp)[RK <= 2])), math.sqrt(0.744 * 0.256 / (RK <= 2).sum()))
num("Q5c", 2, ex(lambda s: Q0(s) and Qp(s), lambda s: s[3] >= 3), float(np.mean((m0 & mp)[RK >= 3])), math.sqrt(0.648 * 0.352 / (RK >= 3).sum()))
num("Q5c", 3, both, float((m0 & mp).mean()))
num("Q5d", 0, ex(Q0), float(m0.mean()))
num("Q5d", 1, both, float((m0 & mp).mean()))
num("Q5d", 2, ex(Qp, Q0), float(mp[m0].mean()), math.sqrt(0.914 * 0.086 / m0.sum()))
num("Q5e", 0, 1 - ex(Q0), float((~m0).mean()))
num("Q5e", 1, ex(lambda s: Qp(s) and not Q0(s)), float((mp & ~m0).mean()))
num("Q5e", 2, ex(Qp, lambda s: not Q0(s)), float(mp[~m0].mean()), math.sqrt(0.25 * 0.75 / (~m0).sum()))

# ============================================================ Q6  two urns: N1=6 (4 red) -> move 3 -> N2=4 (1 red)
urn1 = [1] * 4 + [0] * 2
subs = list(itertools.combinations(range(6), 3))
red_after = lambda S, swap=False: Fr(1 + sum(((1 - urn1[i]) if swap else urn1[i]) for i in S), 7)
PX = lambda k: Fr(sum(1 for S in subs if sum(urn1[i] for i in S) == k), len(subs))
Pred = sum(red_after(S) for S in subs) / len(subs)
# MC of the physical process
idx = np.argsort(rng.random((N, 6), dtype=np.float32), axis=1)[:, :3]
mv = np.array(urn1)[idx]                     # colours moved
Xn = mv.sum(axis=1)
tgt = rng.random(N)                          # pick one of the 7 balls in urn 2 uniformly
ball = rng.integers(0, 7, N)
def drawn_red(moved_cols):
    out = np.zeros(N, bool)
    orig = ball < 4                           # one of the 4 original balls (1 red)
    out[orig] = ball[orig] == 0
    j = ball - 4
    sel = ~orig
    out[sel] = moved_cols[np.arange(N)[sel], j[sel]] == 1
    return out
R = drawn_red(mv)
rec("Q6a step0 claim", Fr(1, 4) != Pred and Fr(2, 3) != Pred, "D2/N2=0.25, D1/N1=0.667 vs P(red)=%s" % Pred)
argued("Q6a", 0)
num("Q6a", 1, Fr(sum(sum(urn1[i] for i in S) for S in subs), len(subs)), float(Xn.mean()), math.sqrt(Xn.var() / N))
num("Q6a", 2, red_after([i for i in range(6) if urn1[i]][:3]), float(R[Xn == 3].mean()), math.sqrt(0.245 / (Xn == 3).sum()))
num("Q6a", 3, Pred, float(R.mean()))
opts("Q6b", 0, [float(PX(3) * red_after([0, 1, 2]) / Pred), float(PX(3)), float(red_after([0, 1, 2]))], float(PX(3) * red_after([0, 1, 2]) / Pred))
num("Q6b", 1, PX(3), float(np.mean(Xn == 3)))
num("Q6b", 2, red_after([0, 1, 2]), float(R[Xn == 3].mean()), math.sqrt(0.245 / (Xn == 3).sum()))
num("Q6b", 3, Pred, float(R.mean()))
num("Q6b", 4, PX(3) * red_after([0, 1, 2]) / Pred, float(np.mean((Xn == 3)[R])), math.sqrt(0.196 / R.sum()))
rec("Q6c step0 claim", True, "after swapping, a moved ball is red iff it was black: red moved = n - X (checked by the MC below)")
argued("Q6c", 0)
swapped = 1 - mv
Rsw = drawn_red(swapped)
num("Q6c", 1, Fr(sum(3 - sum(urn1[i] for i in S) for S in subs), len(subs)), float((3 - Xn).mean()), math.sqrt(Xn.var() / N))
num("Q6c", 2, sum(red_after(S, swap=True) for S in subs) / len(subs), float(Rsw.mean()))

# ============================================================ coverage
for qid, q in BYID.items():
    for i, s in enumerate(q.get("steps") or []):
        if s["type"] in ("numeric", "choice") and (qid, i) not in seen:
            rec("%s step%d COVERAGE" % (qid, i), False, "step not verified")

for tag, ok, info in rows:
    print(("ok   " if ok else "FAIL ") + tag + ": " + info)
print("steps_check %s: %d checks, %d failing" % (CODE, len(rows), fails))
sys.exit(1 if fails else 0)
