# -*- coding: utf-8 -*-
"""Verification of the guided steps of 24A-B (probability). Run: PYTHONUTF8=1 py tools/verify/24A-B/steps_check.py

Reads tools/raw/24A-B.json (written by tools/gen/gen_24A-B.py) and re-derives every NUMERIC step independently:
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

CODE = "24A-B"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    k = "Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))
    BYID[k] = q
N = 1_000_000
rng = np.random.default_rng(20240417)
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


# ============================================================ Q1 (unit square; S1=X/2, S2=Y/2, S3=(1-X)/2)
X = rng.random(N); Y = rng.random(N)
S1, S2, S3 = X / 2, Y / 2, (1 - X) / 2
x, y = sp.symbols("x y")
R = sp.Rational
one = sp.integrate(1, (x, 0, 1), (y, 0, 1))
for q in ("Q1a", "Q1b", "Q1c", "Q1d"):
    num(q, 0, one)
opts("Q1a", 1, [float(np.mean(X < .25)), float(np.mean(X < .125)), float(np.mean(X < .5))], float(np.mean(S1 < 1 / 8)))
num("Q1a", 2, sp.integrate(1, (x, 0, R(1, 4)), (y, 0, 1)), float(np.mean(X < .25)))
opts("Q1b", 1, [float(np.mean(X + Y < 1.5)), float(np.mean(X + Y < .75)), float(np.mean(X + Y < 3))], float(np.mean(S1 + S2 < .75)))
corner = sp.integrate(1, (x, R(3, 2) - y, 1), (y, R(1, 2), 1))
num("Q1b", 2, corner, float(np.mean(X + Y >= 1.5)))
num("Q1b", 3, 1 - corner, float(np.mean(S1 + S2 < .75)))
opts("Q1c", 1, [float(np.mean(Y > X)), float(np.mean(Y > 2 * X)), float(np.mean(Y > X / 2))], float(np.mean(S1 < S2)))
num("Q1c", 2, sp.integrate(1, (y, x, 1), (x, 0, 1)), float(np.mean(Y > X)))
opts("Q1d", 1, [float(np.mean((X < Y) & (Y < 1 - X))), float(np.mean((X < Y) & (Y < 1 - Y))), float(np.mean((Y < X) & (X < 1 - X)))],
     float(np.mean((S1 < S2) & (S2 < S3))))
tri = sp.integrate(1, (y, x, 1 - x), (x, 0, R(1, 2)))
num("Q1d", 2, tri, float(np.mean((S1 < S2) & (S2 < S3))))

# ============================================================ Q2 (two fair dice)
pairs = list(itertools.product(range(1, 7), repeat=2))
D1 = rng.integers(1, 7, N); D2 = rng.integers(1, 7, N)
A = [s for s in pairs if sum(s) == 5]
sums = [sum(s) for s in pairs]
rec("Q2a step0 claims", sums.count(7) == 6 * sums.count(2) and Fr(len(A), 36) != Fr(1, 11), "sum is not uniform: #(7)=%d #(2)=%d" % (sums.count(7), sums.count(2)))
argued("Q2a", 0)
num("Q2a", 1, len(A))
num("Q2a", 2, Fr(len(A), 36), float(np.mean(D1 + D2 == 5)))
BA = [s for s in A if s[0] > 3]
selA = (D1 + D2 == 5)
opts("Q2b", 0, [float(Fr(len(BA), len(A))), 0.5, float(Fr(len(A), 36) * Fr(1, 2))], float(np.mean(D1[selA] > 3)))
num("Q2b", 1, Fr(len(A), 36), float(np.mean(selA)))
num("Q2b", 2, Fr(len(BA), 36), float(np.mean(selA & (D1 > 3))))
num("Q2b", 3, Fr(len(BA), len(A)), float(np.mean(D1[selA] > 3)), math.sqrt(.25 * .75 / selA.sum()))
C = [s for s in pairs if s[0] * s[1] <= 18]
num("Q2c", 0, len(pairs))
num("Q2c", 1, len(pairs) - len(C))
num("Q2c", 2, Fr(len(C), 36), float(np.mean(D1 * D2 <= 18)))
CD = [s for s in C if s[0] % 2 == 1 and s[1] % 2 == 1]
selC = D1 * D2 <= 18
num("Q2d", 0, Fr(len(C), 36), float(np.mean(selC)))
num("Q2d", 1, Fr(len(CD), 36), float(np.mean(selC & (D1 % 2 == 1) & (D2 % 2 == 1))))
num("Q2d", 2, Fr(len(CD), len(C)), float(np.mean(((D1 % 2 == 1) & (D2 % 2 == 1))[selC])), math.sqrt(2 / 7 * 5 / 7 / selC.sum()))

# ============================================================ Q3 (matrix, X,Y ~ Ber(p), p = 0.3)
Xs, Ys = sp.symbols("X Y")
Qm = sp.Matrix([[Xs * Ys, -Xs], [Ys, Xs + Ys - Xs * Ys]])
DET = lambda a, b: int(Qm.det().subs({Xs: a, Ys: b})); TR = lambda a, b: int(Qm.trace().subs({Xs: a, Ys: b}))
p = Fr(3, 10); pm = {0: 1 - p, 1: p}
joint = {}
for a in (0, 1):
    for b in (0, 1):
        k = (DET(a, b), TR(a, b)); joint[k] = joint.get(k, 0) + pm[a] * pm[b]
Ex = lambda f: sum(pr * f(d, t) for (d, t), pr in joint.items())
Xm = (rng.random(N) < .3).astype(int); Ym = (rng.random(N) < .3).astype(int)
Dm = Xm * Ym * (Xm + Ym - Xm * Ym) + Xm * Ym; Tm = Xm * Ym + (Xm + Ym - Xm * Ym)
PD = lambda v: sum(pr for (d, t), pr in joint.items() if d == v); PT = lambda v: sum(pr for (d, t), pr in joint.items() if t == v)
rec("Q3a step0 claims", sorted({d for d, t in joint}) == [0, 2] and joint.get((2, 0), 0) == 0 and PD(2) * PT(0) > 0,
    "D in {0,2}; P(D=2,T=0)=0 but product>0")
argued("Q3a", 0)
num("Q3a", 1, DET(1, 1))
num("Q3a", 2, joint[(0, 1)], float(np.mean((Dm == 0) & (Tm == 1))))
num("Q3a", 3, 2 * 3 - len(joint))
opts("Q3b", 0, [float(p ** 2), float(p), float(2 * p * (1 - p))], float(PD(2)))
num("Q3b", 1, PD(2), float(np.mean(Dm == 2)))
num("Q3b", 2, Ex(lambda d, t: d), float(np.mean(Dm)), 0.003)
opts("Q3c", 0, [float(PT(1)), float(2 * p), float(2 * p ** 2 * (1 - p ** 2))], float(PT(1)))
rec("Q3c step0 claims", 2 in {t for d, t in joint} and 2 * p != PT(1), "T takes value 2, so Ber(2p) is impossible; P(T=1)=%s" % PT(1))
num("Q3c", 1, PT(0), float(np.mean(Tm == 0)))
num("Q3c", 2, PT(1), float(np.mean(Tm == 1)))
num("Q3d", 0, joint.get((2, 0), 0), float(np.mean((Dm == 2) & (Tm == 0))), 1e-6)
num("Q3d", 1, PD(2) * PT(0))
rec("Q3d step2 verdict", joint.get((2, 0), 0) != PD(2) * PT(0), "joint != product -> dependent")
ED, ET = Ex(lambda d, t: d), Ex(lambda d, t: t)
num("Q3e", 0, Ex(lambda d, t: d * t), float(np.mean(Dm * Tm)))
num("Q3e", 1, ED * ET)
num("Q3e", 2, Ex(lambda d, t: d * t) - ED * ET, float(np.mean(Dm * Tm) - np.mean(Dm) * np.mean(Tm)), 0.004)

# ============================================================ Q4 (pdf: c on [0,a], 1 on [a,b])
a_, b_, c_, z = sp.symbols("a b c z", positive=True)
mass1 = a_ * c_; mass2 = b_ - a_
mean = c_ * a_ ** 2 / 2 + (b_ ** 2 - a_ ** 2) / 2
eqs = [sp.Eq(mass1 + mass2, 1), sp.Eq(mass1, 2 * mass2), sp.Eq(mean, R(5, 9))]
sol = sp.solve(eqs, [a_, b_, c_], dict=True)
rec("Q4a solve", sol == [{a_: R(3, 4), b_: R(13, 12), c_: R(8, 9)}], str(sol))
two = sp.solve([eqs[0], eqs[2]], [b_, c_], dict=True)
free = sp.solve([eqs[0], eqs[2]], [b_, c_], dict=True)
vals_a = [0.6, 0.75]
ok_free = len({round(float(free[0][b_].subs(a_, v)), 6) for v in vals_a}) == 2
rec("Q4a step0 underdetermined", ok_free, "two equations give different (b,c) for different a")
num("Q4a", 1, sol[0][b_] - sol[0][a_])
num("Q4a", 2, sol[0][a_])
num("Q4a", 3, sol[0][c_])
a0, b0, c0 = R(3, 4), R(13, 12), R(8, 9)
u = rng.random(N)
Xp = np.where(u < 2 / 3, rng.random(N) * 0.75, 0.75 + rng.random(N) * (13 / 12 - 0.75))
rec("Q4 MC checks", abs(Xp.mean() - 5 / 9) <= 4 * Xp.std() / math.sqrt(N) and abs(np.mean(Xp <= .75) - 2 / 3) < 4 * se_p(2 / 3),
    "mean=%.5f P(X<=a)=%.5f" % (Xp.mean(), np.mean(Xp <= .75)))
Fp = lambda t: sp.integrate(c0, (z, 0, min(t, a0))) + (sp.integrate(1, (z, a0, t)) if t > a0 else 0)
num("Q4b", 0, Fp(a0), float(np.mean(Xp <= .75)))
tq = R(9, 10)
opts("Q4b", 1, [float(tq - R(1, 12)), float(tq), float(R(8, 9) * tq)], float(Fp(tq)))
num("Q4b", 2, Fp(R(1)), float(np.mean(Xp <= 1)))
num("Q4c", 0, c0)
tm = R(5, 9)
opts("Q4c", 1, [float(R(8, 9) * tm), float(tm - R(1, 12)), float(tm)], float(Fp(tm)))
num("Q4c", 2, Fp(tm), float(np.mean(Xp <= 5 / 9)))

# ============================================================ Q5 (D=2, N=5, Q=0.4, p=0.5, n=4)
Q, pg = Fr(2, 5), Fr(1, 2)
binom = lambda n, k: Fr(math.comb(n, k)) * Q ** k * (1 - Q) ** (n - k)
red = rng.random((N, 4)) < 0.4
hyper = Fr(math.comb(2, 2) * math.comb(3, 2), math.comb(5, 4))
rec("Q5a step0 claims", hyper != binom(4, 2), "without replacement P(X=2)=%s != with replacement %s" % (hyper, binom(4, 2)))
argued("Q5a", 0)
num("Q5a", 1, Q)
num("Q5a", 2, binom(4, 2), float(np.mean(red.sum(1) == 2)))
Yg = rng.geometric(0.5, N); Zg = rng.binomial(Yg, 0.4)
# exact series, truncated far out (the tail is below 1e-30)
def pz(k, J=200):
    return sum(Fr(math.comb(j, k)) * Q ** k * (1 - Q) ** (j - k) * pg * (1 - pg) ** (j - 1) for j in range(max(k, 1), J))
num("Q5b", 1, (1 - Q) ** 2)
r_ = (1 - Q) * (1 - pg)
num("Q5b", 2, r_)
num("Q5b", 3, pz(0), float(np.mean(Zg == 0)))
rec("Q5b closed form", abs(float(pz(0)) - 3 / 7) < 1e-12, "series=%.12f" % float(pz(0)))
argued("Q5b", 0)
rec("Q5b step0 claim: Y random", float(np.mean(Zg == 0)) != float((1 - Q) ** 4) and abs(float(np.mean(Zg == 0)) - 3 / 7) < 4 * se_p(3 / 7), "P(Z=0)=3/7 not (1-Q)^n")
ssum = sum(Fr(math.comb(j, 2)) * Fr(3, 10) ** j for j in range(2, 200))
num("Q5c", 1, ssum)
num("Q5c", 2, pz(2), float(np.mean(Zg == 2)))
rec("Q5c closed form", abs(float(pz(2)) - 40 / 343) < 1e-12 and abs(float(ssum) - 0.09 / 0.343) < 1e-12, "series=%.12f" % float(pz(2)))
ra = [float(pz(k + 1) / pz(k)) for k in (1, 2, 3, 4)]
rec("Q5c step0 claims", max(ra) - min(ra) < 1e-12 and abs(ra[0] - 2 / 7) < 1e-12, "ratio P(k+1)/P(k)=%s constant for k>=1" % ra)
argued("Q5c", 0)

# ============================================================ Q6 (bridge; p = 0.6)
pp = Fr(3, 5)
EDGES = {"A": ("L", "T"), "B": ("T", "R"), "C": ("L", "U"), "D": ("U", "R"), "E": ("T", "U")}
def connected(st, edges=EDGES, s0="L", t0="R"):
    seen = {s0}; stack = [s0]
    while stack:
        u = stack.pop()
        for k, (a, b) in edges.items():
            if st[k]:
                v = b if a == u else a if b == u else None
                if v and v not in seen:
                    seen.add(v); stack.append(v)
    return t0 in seen
Q2f = lambda st: (st["A"] or st["B"]) and (st["C"] or st["D"])
def prob(f, given=None, fixed=None):
    tot = Fr(0); den_ = Fr(0)
    for bits in itertools.product((0, 1), repeat=5):
        st = dict(zip("ABCDE", bits))
        if fixed and any(st[k] != v for k, v in fixed.items()):
            continue
        w = Fr(1)
        for v in bits:
            w *= pp if v else 1 - pp
        if given is None or given(st):
            den_ += w; tot += w if f(st) else 0
    return tot / den_ if given is not None else tot
U5 = rng.random((N, 5)) < 0.6
st = {k: U5[:, i] for i, k in enumerate("ABCDE")}
q1m = (st["A"] & st["B"]) | (st["C"] & st["D"]) | (st["A"] & st["E"] & st["D"]) | (st["C"] & st["E"] & st["B"])
q2m = (st["A"] | st["B"]) & (st["C"] | st["D"])
rec("Q6 bridge formula", all(connected(dict(zip("ABCDE", b))) == bool(q1m_f) for b, q1m_f in
    [(b, (b[0] and b[1]) or (b[2] and b[3]) or (b[0] and b[4] and b[3]) or (b[2] and b[4] and b[1])) for b in itertools.product((0, 1), repeat=5)]),
    "graph connectivity == path-set formula for all 32 states")
P1 = prob(connected)
opts("Q6a", 0, [float(P1), float(prob(Q2f)), float(prob(connected, fixed={"E": 0}) / (1 - pp))], float(P1))
num("Q6a", 1, prob(connected, fixed={"E": 1}) / pp, float(np.mean(q1m[st["E"]])))
num("Q6a", 2, prob(connected, fixed={"E": 0}) / (1 - pp), float(np.mean(q1m[~st["E"]])))
num("Q6a", 3, P1, float(np.mean(q1m)))
P2 = prob(Q2f)
opts("Q6b", 0, [float(P2), float(pp ** 4), float(1 - (1 - pp) ** 4)], float(np.mean(q2m)))
num("Q6b", 1, 1 - (1 - pp) ** 2, float(np.mean(st["A"] | st["B"])))
num("Q6b", 2, P2, float(np.mean(q2m)))
both = lambda s_: connected(s_) and Q2f(s_)
opts("Q6c", 0, [float(prob(both)), float(P1 * P2), float(P1 + P2 - 1)], float(np.mean(q1m & q2m)))
num("Q6c", 1, P2, float(np.mean(q2m)))
num("Q6c", 2, prob(both, fixed={"E": 1}) / pp, float(np.mean((q1m & q2m)[st["E"]])))
num("Q6c", 3, prob(both, fixed={"E": 0}) / (1 - pp), float(np.mean((q1m & q2m)[~st["E"]])))
num("Q6c", 4, prob(both) / P2, float(np.mean(q1m[q2m])), math.sqrt(.7714 * .2286 / q2m.sum()))
pq = pp
rec("Q6 formulas", P1 == pq ** 2 * (2 + 2 * pq - 5 * pq ** 2 + 2 * pq ** 3) and prob(both) == pq ** 3 * (6 - 7 * pq + 2 * pq ** 2)
    and prob(both) / P2 == pq * (3 - 2 * pq) / (2 - pq), "official closed forms = enumeration")

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
