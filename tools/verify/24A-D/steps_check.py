# -*- coding: utf-8 -*-
"""Verification of the guided steps of 24A-D (probability). Run: PYTHONUTF8=1 py tools/verify/24A-D/steps_check.py

Reads tools/raw/24A-D.json (written by tools/gen/gen_24A-D.py) and re-derives every NUMERIC step independently:
  EXACT : fractions / itertools enumeration / sympy, compared with the stored answer (within 5e-5, and <= tol);
  MC    : Monte Carlo (10^6 trials) within 4 standard errors of the exact value, where a sim applies.
Every CHOICE step whose options are formulas or probabilities is evaluated numerically: the correct option must equal
the exact value and every distractor must differ. Pure reasoning choices are listed as ARGUED (their distractor claims
are verified by the explicit claim checks at the bottom). Exits 1 on any failure. ASCII output.
"""
import itertools, json, math, pathlib, re, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

CODE = "24A-D"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    k = "Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))
    BYID[k] = q
N = 1_000_000
rng = np.random.default_rng(20240403)
rows = []
fails = 0
COVERED = set()


def rec(tag, ok, info):
    global fails
    m = re.match(r"(Q\w+) step(\d+)", tag)
    if m:
        COVERED.add((m.group(1), int(m.group(2))))
    rows.append((tag, ok, info))
    if not ok:
        fails += 1


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-12) / n)


def num(qid, idx, exact, mc=None, se=None):
    COVERED.add((qid, idx))
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


def opts(qid, idx, vals, target, se=None):
    """choice step whose options are numbers: vals[i] is the numeric value of option i."""
    COVERED.add((qid, idx))
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "choice" and len(vals) == len(s["options"]), (qid, idx)
    ci = "abcdefgh".index(s["correctId"])
    good = abs(vals[ci] - target) <= 1e-9 or abs(vals[ci] - target) <= 4 * (se if se is not None else se_p(target))
    bad = [i for i, v in enumerate(vals) if i != ci and abs(v - target) <= 1e-3]
    rec("%s step%d choice-values" % (qid, idx), good and not bad, "values=%s target=%.6f" % (["%.4f" % v for v in vals], target))


def argued(qid, idx):
    COVERED.add((qid, idx))
    s = BYID[qid]["steps"][idx]
    assert s["type"] == "choice"
    rec("%s step%d choice-argued" % (qid, idx), True, "reasoning choice; claims verified below")


# ============================================================ Q1 (grasshopper: X1, X2 ~ U(0,1) independent)
x, y = sp.symbols("x y")
R = sp.Rational
X1 = rng.random(N); X2 = rng.random(N)
for q in ("Q1a", "Q1b", "Q1c"):
    num(q, 0, sp.integrate(1, (x, 0, 1), (y, 0, 1)))
opts("Q1a", 1, [float(np.mean(X1 + X2 <= 2 / 3)), float(np.mean(np.maximum(X1, X2) < 2 / 3)), float(np.mean(X1 + X2 <= 1 / 3))], float(np.mean(X1 + X2 <= 2 / 3)))
num("Q1a", 2, sp.integrate(1, (y, 0, R(2, 3) - x), (x, 0, R(2, 3))), float(np.mean(X1 + X2 <= 2 / 3)))
opts("Q1b", 1, [float(np.mean((X1 < 2 / 3) & (X2 < 2 / 3))), float(np.mean(X1 < 2 / 3)), float(np.mean(X1 + X2 < 2 / 3))], float(np.mean((X1 < 2 / 3) & (X2 < 2 / 3))))
num("Q1b", 2, sp.integrate(1, (x, 0, R(2, 3)), (y, 0, 1)), float(np.mean(X1 < 2 / 3)))
num("Q1b", 3, sp.integrate(1, (x, 0, R(2, 3)), (y, 0, R(2, 3))), float(np.mean((X1 < 2 / 3) & (X2 < 2 / 3))))
selX = X1 <= 2 / 3
inter = sp.integrate(1, (y, 0, 1 - x), (x, 0, R(2, 3)))
num("Q1c", 1, sp.integrate(1, (x, 0, R(2, 3)), (y, 0, 1)), float(np.mean(selX)))
num("Q1c", 2, inter, float(np.mean(selX & (X1 + X2 <= 1))))
num("Q1c", 3, inter / R(2, 3), float(np.mean((X1 + X2 <= 1)[selX])), math.sqrt(2 / 3 * 1 / 3 / selX.sum()))

# ============================================================ Q2 (fair dice)
NB = 4_000_000
d = rng.integers(1, 7, (NB, 3))
d1, d2, d3 = d[:, 0], d[:, 1], d[:, 2]
pairs = list(itertools.product(range(1, 7), repeat=2)); trip = list(itertools.product(range(1, 7), repeat=3))
s2 = [sum(s) for s in pairs]
rec("Q2a step0 claims", s2.count(7) == 6 * s2.count(2) and Fr(s2.count(6), 36) != Fr(1, 11), "sum not uniform: #7=%d #2=%d" % (s2.count(7), s2.count(2)))
argued("Q2a", 0)
num("Q2a", 1, s2.count(6))
num("Q2a", 2, Fr(s2.count(6), 36), float(np.mean(d1 + d2 == 6)), math.sqrt(5 / 36 * 31 / 36 / NB))
B = [s for s in trip if sum(s) == 6]
argued("Q2b", 0)
num("Q2b", 1, len(trip))
num("Q2b", 2, len(B))
num("Q2b", 3, Fr(len(B), 216), float(np.mean(d1 + d2 + d3 == 6)), math.sqrt(5 / 108 * 103 / 108 / NB))
sB = (d1 + d2 + d3 == 6)
Cs = [s for s in trip if s[0] + s[1] == 2]
selC = (d1 + d2 == 2)
opts("Q2c", 0, [1 / 6, float(Fr(len(B), 216)), 1 / 36], float(np.mean(sB[selC])), math.sqrt(1 / 6 * 5 / 6 / selC.sum()))
num("Q2c", 1, Fr(len(Cs), 216), float(np.mean(selC)), math.sqrt(1 / 36 * 35 / 36 / NB))
num("Q2c", 2, Fr(sum(1 for s in Cs if sum(s) == 6), 216), float(np.mean(selC & sB)), math.sqrt(1 / 216 / NB))
num("Q2c", 3, Fr(sum(1 for s in Cs if sum(s) == 6), len(Cs)), float(np.mean(sB[selC])), math.sqrt(1 / 6 * 5 / 6 / selC.sum()))
Ds = [s for s in trip if s[0] < s[1]]; selD = d1 < d2
BD = [s for s in Ds if sum(s) == 6]
opts("Q2d", 0, [float(Fr(len(BD), len(Ds))), float(Fr(len(B), 216)), 1 / 6], float(np.mean(sB[selD])), math.sqrt(2 / 45 * 43 / 45 / selD.sum()))
num("Q2d", 1, Fr(len(Ds), 216), float(np.mean(selD)), math.sqrt(5 / 12 * 7 / 12 / NB))
num("Q2d", 2, Fr(len(BD), 216), float(np.mean(selD & sB)), math.sqrt(1 / 54 / NB))
num("Q2d", 3, Fr(len(BD), len(Ds)), float(np.mean(sB[selD])), math.sqrt(2 / 45 * 43 / 45 / selD.sum()))
Es = [s for s in trip if s[0] == s[1]]; selE = d1 == d2
BE = [s for s in Es if sum(s) == 6]
opts("Q2e", 0, [float(Fr(len(BE), len(Es))), float(Fr(len(B), 216)), 1 / 6], float(np.mean(sB[selE])), math.sqrt(1 / 18 * 17 / 18 / selE.sum()))
num("Q2e", 1, Fr(len(Es), 216), float(np.mean(selE)), math.sqrt(1 / 6 * 5 / 6 / NB))
num("Q2e", 2, Fr(len(BE), 216), float(np.mean(selE & sB)), math.sqrt(1 / 108 / NB))
num("Q2e", 3, Fr(len(BE), len(Es)), float(np.mean(sB[selE])), math.sqrt(1 / 18 * 17 / 18 / selE.sum()))

# ============================================================ Q3 (matrix [[0,X],[Y,X+Y]], X~Ber(.3), Y~Ber(.6))
Xs, Ys = sp.symbols("X Y")
Qm = sp.Matrix([[0, Xs], [Ys, Xs + Ys]])
DET = lambda a, b: int(Qm.det().subs({Xs: a, Ys: b})); TR = lambda a, b: int(Qm.trace().subs({Xs: a, Ys: b}))
pa, qb = Fr(3, 10), Fr(3, 5)
pmx = {0: 1 - pa, 1: pa}; pmy = {0: 1 - qb, 1: qb}
joint = {}
for a in (0, 1):
    for b in (0, 1):
        k = (DET(a, b), TR(a, b)); joint[k] = joint.get(k, 0) + pmx[a] * pmy[b]
Ex = lambda f: sum(pr * f(dd, tt) for (dd, tt), pr in joint.items())
Xm = (rng.random(N) < .3).astype(int); Ym = (rng.random(N) < .6).astype(int)
Dm = 0 * (Xm + Ym) - Xm * Ym; Tm = Xm + Ym
PD = lambda v: sum(pr for (dd, tt), pr in joint.items() if dd == v)
ED, ET = Ex(lambda dd, tt: dd), Ex(lambda dd, tt: tt)
VD = Ex(lambda dd, tt: dd * dd) - ED ** 2; VT = Ex(lambda dd, tt: tt * tt) - ET ** 2
COV = Ex(lambda dd, tt: dd * tt) - ED * ET
opts("Q3a", 0, [float(pa * qb), float(pa + qb - pa * qb), float(pa + qb)], float(PD(-1)))
num("Q3a", 1, ED, float(np.mean(Dm)), 0.0004)
num("Q3a", 2, VD, float(np.var(Dm)), 0.0008)
opts("Q3b", 0, [float(pa * (1 - pa) + qb * (1 - qb)), float(pa * (1 - pa) + qb * (1 - qb) + 2 * pa * qb), float(pa * (1 - pa) * qb * (1 - qb))], float(VT))
num("Q3b", 1, ET, float(np.mean(Tm)), 0.003)
num("Q3b", 2, VT, float(np.var(Tm)), 0.004)
num("Q3c", 0, Ex(lambda dd, tt: dd * tt), float(np.mean(Dm * Tm)), 0.001)
num("Q3c", 1, ED * ET)
num("Q3c", 2, COV, float(np.mean(Dm * Tm) - np.mean(Dm) * np.mean(Tm)), 0.002)
rec("Q3c closed form", COV == pa * qb * (pa + qb - 2) and Ex(lambda dd, tt: dd * tt) == -2 * pa * qb, "cov = pq(p+q-2), E[DT] = -2pq")

# ============================================================ Q4 (pdf a(b-|x|) on [-b,b]; a=1/4, b=2)
a_, b_, z = sp.symbols("a b z", positive=True)
f1 = a_ * (b_ + z); f2 = a_ * (b_ - z)
mean = sp.integrate(z * f1, (z, -b_, 0)) + sp.integrate(z * f2, (z, 0, b_))
m2 = sp.integrate(z ** 2 * f1, (z, -b_, 0)) + sp.integrate(z ** 2 * f2, (z, 0, b_))
area = sp.integrate(f1, (z, -b_, 0)) + sp.integrate(f2, (z, 0, b_))
rec("Q4 symbolic", sp.simplify(mean) == 0 and sp.simplify(area - a_ * b_ ** 2) == 0 and sp.simplify(m2 - a_ * b_ ** 4 / 6) == 0, "E[X]=0, area=ab^2, E[X^2]=ab^4/6")
solb = sp.solve([sp.Eq(area, 1), sp.Eq(m2, R(2, 3))], [a_, b_], dict=True)
rec("Q4b solve", solb == [{a_: R(1, 4), b_: 2}], str(solb))
fa, fb = R(1, 4), 2
opts("Q4a", 0, [float(mean.subs({a_: fa, b_: fb})), float(fb / 2), float(fb / 3)], 0.0)
num("Q4a", 1, mean.subs({a_: fa, b_: fb}))
argued("Q4b", 0)
rec("Q4b step0 claims", sp.simplify(mean) == 0, "E[X]=0 for every a,b: gives no equation")
num("Q4b", 1, sp.simplify((a_ * b_ ** 4).subs({a_: fa, b_: fb})))
num("Q4b", 2, solb[0][b_])
num("Q4b", 3, solb[0][a_])
u = rng.random(N)
Xt = np.where(u < .5, -2 * (1 - np.sqrt(1 - rng.random(N))), 2 * (1 - np.sqrt(1 - rng.random(N))))
rec("Q4 MC mean/var", abs(Xt.mean()) <= 4 * Xt.std() / math.sqrt(N) and abs(Xt.var() - 2 / 3) < 0.01, "mean=%.5f var=%.5f" % (Xt.mean(), Xt.var()))
Fm = lambda t: sp.integrate(f1.subs({a_: fa, b_: fb}), (z, -fb, min(t, 0))) if t < 0 else R(1, 2) + sp.integrate(f2.subs({a_: fa, b_: fb}), (z, 0, min(t, fb)))
num("Q4c", 0, Fm(R(0)), float(np.mean(Xt <= 0)))
tq = -1.0
opts("Q4c", 1, [(tq + 2) ** 2 / 8, (tq + 2) ** 2 / 4, (2 - tq) ** 2 / 8], float(Fm(R(-1))))
rec("Q4c MC F(-1)", abs(np.mean(Xt <= -1) - float(Fm(R(-1)))) < 4 * se_p(0.125), "F(-1)=%s; MC=%.5f" % (Fm(R(-1)), np.mean(Xt <= -1)))
num("Q4c", 2, Fm(R(1)), float(np.mean(Xt <= 1)))
den = Fm(R(1)) - Fm(R(-1)); numr = Fm(R(1)) - Fm(R(1, 4))
selA = np.abs(Xt) < 1
num("Q4d", 0, den, float(np.mean(selA)))
num("Q4d", 1, numr, float(np.mean((Xt > .25) & (Xt < 1))))
num("Q4d", 2, numr / den, float(np.mean(Xt[selA] > .25)), math.sqrt(11 / 32 * 21 / 32 / selA.sum()))

# ============================================================ Q5 (thinning: N candidates, each born that day with probability p)
p5 = Fr(1, 4)
hit = rng.random((N, 6)) < 0.25
bin6 = lambda k: Fr(math.comb(6, k)) * p5 ** k * (1 - p5) ** (6 - k)
rec("Q5a step0 claims", bin6(2) == Fr(1215, 4096) and abs(math.exp(-1.5) * 1.5 ** 2 / 2 - float(bin6(2))) > 0.01, "Bin(6,1/4): P(W=2)=%s; a Poisson(1.5) model would give %.4f" % (bin6(2), math.exp(-1.5) * 1.5 ** 2 / 2))
argued("Q5a", 0)
num("Q5a", 1, Fr(1, 365))
num("Q5a", 2, bin6(2), float(np.mean(hit.sum(1) == 2)))
lam, pt = 4, 0.25
Xp = rng.poisson(lam, N); Yp = rng.binomial(Xp, pt)
pois = lambda m, k: math.exp(-m) * m ** k / math.factorial(k)
binom4 = lambda k, pp_: math.comb(4, k) * pp_ ** k * (1 - pp_) ** (4 - k)
opts("Q5b", 0, [pois(1, 2), binom4(2, .25), pois(4, 2)], float(np.mean(Yp == 2)))
num("Q5b", 1, lam * pt)
num("Q5b", 2, Fr(pois(1, 2)), float(np.mean(Yp == 2)))
selY = Yp == 2
opts("Q5c", 0, [pois(3, 2), pois(4, 4), binom4(2, .75)], float(np.mean(Xp[selY] == 4)), math.sqrt(.224 * .776 / selY.sum()))
num("Q5c", 1, lam * (1 - pt))
num("Q5c", 2, Fr(pois(3, 2)), float(np.mean(Xp[selY] == 4)), math.sqrt(.224 * .776 / selY.sum()))
# exact thinning identity by direct (truncated) summation: P(Y=k) = sum_j C(j,k) p^k (1-p)^(j-k) Pois(j; lam)
py = lambda k: sum(math.comb(j, k) * pt ** k * (1 - pt) ** (j - k) * pois(lam, j) for j in range(k, 120))
rec("Q5 thinning exact", abs(py(2) - pois(1, 2)) < 1e-12 and abs(pois(lam, 4) * math.comb(4, 2) * pt ** 2 * (1 - pt) ** 2 / py(2) - pois(3, 2)) < 1e-12,
    "P(Y=2)=%.12f, P(X=4|Y=2)=%.12f" % (py(2), pois(lam, 4) * math.comb(4, 2) * pt ** 2 * (1 - pt) ** 2 / py(2)))

# ============================================================ Q6 (bridge Q1; Q2 = A || (E-B) || (C-D); p = 0.6)
pp = Fr(3, 5)
E1 = {"A": ("L", "T"), "B": ("T", "R"), "C": ("L", "U"), "D": ("U", "R"), "E": ("T", "U")}
E2 = {"A": ("L", "R"), "E": ("L", "T"), "B": ("T", "R"), "C": ("L", "U"), "D": ("U", "R")}
def connected(st_, edges, s0="L", t0="R"):
    seen = {s0}; stack = [s0]
    while stack:
        u_ = stack.pop()
        for k, (a, b) in edges.items():
            if st_[k]:
                v = b if a == u_ else a if b == u_ else None
                if v and v not in seen:
                    seen.add(v); stack.append(v)
    return t0 in seen
c1 = lambda s_: connected(s_, E1)
c2 = lambda s_: connected(s_, E2)
def prob(f, given=None, fixed=None):
    tot = Fr(0); den_ = Fr(0)
    for bits in itertools.product((0, 1), repeat=5):
        s_ = dict(zip("ABCDE", bits))
        if fixed and any(s_[k] != v for k, v in fixed.items()):
            continue
        w_ = Fr(1)
        for v in bits:
            w_ *= pp if v else 1 - pp
        if given is None or given(s_):
            den_ += w_; tot += w_ if f(s_) else 0
    return tot / den_ if given is not None else tot
U5 = rng.random((N, 5)) < 0.6
st = {k: U5[:, i] for i, k in enumerate("ABCDE")}
q1m = (st["A"] & st["B"]) | (st["C"] & st["D"]) | (st["A"] & st["E"] & st["D"]) | (st["C"] & st["E"] & st["B"])
q2m = st["A"] | (st["E"] & st["B"]) | (st["C"] & st["D"])
rec("Q6 path formulas", all(c1(dict(zip("ABCDE", b))) == bool(q1m_) and c2(dict(zip("ABCDE", b))) == bool(q2m_) for b, q1m_, q2m_ in
    [(b, (b[0] and b[1]) or (b[2] and b[3]) or (b[0] and b[4] and b[3]) or (b[2] and b[4] and b[1]), b[0] or (b[4] and b[1]) or (b[2] and b[3]))
     for b in itertools.product((0, 1), repeat=5)]), "graph connectivity == path-set formulas for all 32 states")
P1 = prob(c1); P2 = prob(c2)
opts("Q6a", 0, [float(P1), float(prob(lambda s_: (s_["A"] or s_["B"]) and (s_["C"] or s_["D"]))), float(prob(c1, fixed={"E": 0}) / (1 - pp))], float(P1))
num("Q6a", 1, prob(c1, fixed={"E": 1}) / pp, float(np.mean(q1m[st["E"]])))
num("Q6a", 2, prob(c1, fixed={"E": 0}) / (1 - pp), float(np.mean(q1m[~st["E"]])))
num("Q6a", 3, P1, float(np.mean(q1m)))
opts("Q6b", 0, [float(P2), float(pp * prob(lambda s_: (s_["E"] and s_["B"]) or (s_["C"] and s_["D"]))), float(P1)], float(np.mean(q2m)))
num("Q6b", 1, prob(c2, fixed={"A": 0}) / (1 - pp), float(np.mean(q2m[~st["A"]])))
num("Q6b", 2, P2, float(np.mean(q2m)))
both = lambda s_: c1(s_) and c2(s_)
rec("Q6c claim Q1 subset Q2", all((not c1(dict(zip("ABCDE", b)))) or c2(dict(zip("ABCDE", b))) for b in itertools.product((0, 1), repeat=5)), "Q1 => Q2 in all 32 states")
opts("Q6c", 0, [1.0, float(P2), float(P1)], float(np.mean(q2m[q1m])))
num("Q6c", 1, P1, float(np.mean(q1m)))
num("Q6c", 2, prob(both), float(np.mean(q1m & q2m)))
num("Q6c", 3, prob(c2, given=c1), float(np.mean(q2m[q1m])), 1e-9)
pq = pp
rec("Q6 formulas", P1 == pq * (2 * pq - pq ** 2) ** 2 + (1 - pq) * (2 * pq ** 2 - pq ** 4) and P2 == pq + (1 - pq) * (2 * pq ** 2 - pq ** 4), "official closed forms = enumeration")

# ---------------------------------------------------------------- report
for tag, ok, info in rows:
    print("%s %-26s %s" % ("ok  " if ok else "FAIL", tag, info))
steps_total = sum(len(q.get("steps", [])) for q in RAW["questions"])
allsteps = {(k, i) for k, q in BYID.items() for i in range(len(q.get("steps", [])))}
missing = sorted(allsteps - COVERED)
if missing:
    print("UNCHECKED STEPS:", missing)
    fails += 1
covered = len(COVERED)
print("steps in raw: %d; checked step rows: %d; failures: %d" % (steps_total, covered, fails))
sys.exit(1 if fails else 0)
