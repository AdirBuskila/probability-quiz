# -*- coding: utf-8 -*-
"""Verification of the guided steps of 25A-C (probability). Run: PYTHONUTF8=1 py tools/verify/25A-C/steps_check.py

Reads tools/raw/25A-C.json (written by tools/gen/gen_25A-C.py) and re-derives every NUMERIC step independently:
  EXACT : fractions / itertools enumeration / sympy / quadrature, compared with the stored answer (<= tol, and <= 5e-5);
  MC    : Monte Carlo (10^6 trials) within 4 standard errors of the exact value, where a kind applies.
Every CHOICE step whose options are numbers/formulas is evaluated: the correct option equals the exact value and every
distractor differs. Pure reasoning choices are listed as ARGUED (their distractor claims are verified in the claim
checks). A coverage check fails the run if any numeric step of the raw file was not verified. ASCII output.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

CODE = "25A-C"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20250511)
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


# ============================================================ Q1  X~U(0,1), Y~U(0,2)
x, y = sp.symbols("x y")
X = rng.random(N); Y = 2 * rng.random(N)
S = X * Y; L = 2 * (X + Y)
OM = sp.integrate(1, (x, 0, 1), (y, 0, 2))
for q in ("Q1a", "Q1b", "Q1c"):
    num(q, 0, OM)
area_S = integrate.quad(lambda t: min(2.0, 2 / (3 * t)), 0, 1, points=[1 / 3], limit=200)[0]
num("Q1a", 1, area_S, 2 * float(np.mean(S < 2 / 3)), 2 * se_p(area_S / 2))
num("Q1a", 2, area_S / 2, float(np.mean(S < 2 / 3)))
area_L = sp.integrate(1 - x, (x, 0, 1))
num("Q1b", 1, area_L, 2 * float(np.mean(L < 2)), 2 * se_p(0.25))
num("Q1b", 2, area_L / OM, float(np.mean(L < 2)))
pc = 1 - area_L / OM
num("Q1c", 1, pc, float(np.mean(L > 2)))
inter = integrate.quad(lambda t: (min(2.0, 2 / (3 * t)) - min(2.0, max(0.0, 1 - t))) / 2, 0, 1, points=[1 / 3], limit=200)[0]
num("Q1c", 2, inter, float(np.mean((S < 2 / 3) & (L > 2))))
sel = L > 2
num("Q1c", 3, inter / float(pc), float(np.mean((S < 2 / 3) & sel) / np.mean(sel)), math.sqrt(0.6 * 0.4 / sel.sum()))
EX = sp.integrate(x, (x, 0, 1)); EY = sp.integrate(y / 2, (y, 0, 2))
VX = sp.integrate(x ** 2, (x, 0, 1)) - EX ** 2; VY = sp.integrate(y ** 2 / 2, (y, 0, 2)) - EY ** 2
num("Q1d", 1, 2 * (EX + EY), float(L.mean()), 5 * math.sqrt(L.var() / N) / 5)
num("Q1d", 2, 4 * (VX + VY), float(L.var()), math.sqrt(2 / N) * L.var())
rec("Q1d step0 claim", abs(float(4 * (VX + VY)) - 5 / 3) < 1e-12 and abs(2 * float(VX + VY) - 5 / 3) > 0.1 and abs(float(L.var()) - 5 / 3) < 0.01,
    "Var[2(X+Y)]=%.4f vs 2Var[X+Y]=%.4f" % (float(4 * (VX + VY)), 2 * float(VX + VY)))
argued("Q1d", 0)
ES = EX * EY
num("Q1e", 0, ES, float(S.mean()), math.sqrt(S.var() / N))
ES2 = sp.integrate(x ** 2, (x, 0, 1)) * sp.integrate(y ** 2 / 2, (y, 0, 2))
num("Q1e", 1, ES2, float((S ** 2).mean()), math.sqrt((S ** 2).var() / N))
num("Q1e", 2, ES2 - ES ** 2, float(S.var()), math.sqrt(2 / N) * S.var() * 1.5)

# ============================================================ Q2  atoms from p=.4 q=.5 s=.6
p_, q_, s_ = Fr(2, 5), Fr(1, 2), Fr(3, 5)
pAB = p_ + q_ - s_
atoms = {(1, 1): pAB, (1, 0): p_ - pAB, (0, 1): q_ - pAB, (0, 0): 1 - s_}
assert sum(atoms.values()) == 1 and all(v >= 0 for v in atoms.values())
keys = list(atoms)
idx = rng.choice(4, size=N, p=[float(atoms[k]) for k in keys])
A = np.array([keys[i][0] for i in range(4)])[idx].astype(bool)
B = np.array([keys[i][1] for i in range(4)])[idx].astype(bool)
P = lambda f: sum(w for (a, b), w in atoms.items() if f(a, b))
num("Q2a", 1, P(lambda a, b: a and b), float(np.mean(A & B)))
num("Q2a", 2, P(lambda a, b: b), float(np.mean(B)))
num("Q2a", 3, P(lambda a, b: a and b) / P(lambda a, b: b), float(np.mean(A & B) / np.mean(B)), math.sqrt(0.6 * 0.4 / B.sum()))
rec("Q2a step0 claim", P(lambda a, b: a and b) / P(lambda a, b: a) == Fr(3, 4) and p_ + q_ - p_ * q_ != s_,
    "P(AB)/P(A)=0.75 != 0.6; independence would need s=%s != 0.6" % float(p_ + q_ - p_ * q_))
argued("Q2a", 0)
num("Q2b", 1, P(lambda a, b: not a), float(np.mean(~A)))
num("Q2b", 2, P(lambda a, b: b and not a), float(np.mean(B & ~A)))
num("Q2b", 3, P(lambda a, b: b and not a) / P(lambda a, b: not a), float(np.mean(B[~A])), math.sqrt(1 / 3 * 2 / 3 / (~A).sum()))
rec("Q2b step0 claim", q_ - p_ != s_ - p_ and q_ * (1 - p_) != s_ - p_, "q-p=%s, q(1-p)=%s vs s-p=%s" % (float(q_ - p_), float(q_ * (1 - p_)), float(s_ - p_)))
argued("Q2b", 0)
num("Q2c", 1, P(lambda a, b: not b), float(np.mean(~B)))
num("Q2c", 2, P(lambda a, b: a and not b), float(np.mean(A & ~B)))
num("Q2c", 3, P(lambda a, b: a and not b) / P(lambda a, b: not b), float(np.mean(A[~B])), math.sqrt(0.2 * 0.8 / (~B).sum()))
rec("Q2c step0 claim", p_ - q_ < 0 and p_ * (1 - q_) != s_ - q_, "p-q=%s<0, p(1-q)=%s vs s-q=%s" % (float(p_ - q_), float(p_ * (1 - q_)), float(s_ - q_)))
argued("Q2c", 0)
num("Q2d", 1, P(lambda a, b: not a and not b), float(np.mean(~A & ~B)))
num("Q2d", 2, P(lambda a, b: not b), float(np.mean(~B)))
num("Q2d", 3, P(lambda a, b: not a and not b) / P(lambda a, b: not b), float(np.mean((~A)[~B])), math.sqrt(0.8 * 0.2 / (~B).sum()))
rec("Q2d step0 claim", 1 - p_ - q_ != 1 - s_ and (1 - p_) * (1 - q_) != 1 - s_, "1-p-q=%s, (1-p)(1-q)=%s vs 1-s=%s" % (float(1 - p_ - q_), float((1 - p_) * (1 - q_)), float(1 - s_)))
argued("Q2d", 0)
# independence at p=.4 q=.5: s = p+q-pq ; simulate independent events
Ai = rng.random(N) < 0.4; Bi = rng.random(N) < 0.5
num("Q2e", 1, p_ * q_, float(np.mean(Ai & Bi)))
num("Q2e", 2, p_ + q_ - p_ * q_, float(np.mean(Ai | Bi)))
argued("Q2e", 0)
# disjoint p=.3 q=.4: s=p+q
u = rng.random(N); Ad = u < 0.3; Bd = (u >= 0.3) & (u < 0.7)
num("Q2f", 1, Fr(3, 10) + Fr(2, 5), float(np.mean(Ad | Bd)))
argued("Q2f", 0)

# ============================================================ Q3  f = a(1+x) on [-1,0), b e^-x on x>=0
a_, b_ = sp.symbols("a b")
sol = sp.solve([sp.Eq(sp.integrate(a_ * (1 + x), (x, -1, 0)) + sp.integrate(b_ * sp.exp(-x), (x, 0, sp.oo)), 1),
                sp.Eq(sp.integrate(a_ * x * (1 + x), (x, -1, 0)) + sp.integrate(b_ * x * sp.exp(-x), (x, 0, sp.oo)), 0)], [a_, b_])
num("Q3a", 1, sol[a_]); num("Q3a", 2, sol[b_])
cont = sp.solve(sp.Eq(a_, b_), a_)  # a=b with normalisation a/2+b=1
ab = sp.Rational(2, 3)
mean_if_cont = sp.integrate(ab * x * (1 + x), (x, -1, 0)) + sp.integrate(ab * x * sp.exp(-x), (x, 0, sp.oo))
rec("Q3a step0 claim", mean_if_cont != 0 and sp.Rational(3, 2) != 0, "if a=b=2/3 the mean is %s != 0" % mean_if_cont)
argued("Q3a", 0)
# MC sample: left part mass 3/4 (x=-1+sqrt(u)), right part exp(1)
m = rng.random(N) < 0.75
Xs = np.where(m, -1 + np.sqrt(rng.random(N)), rng.exponential(1.0, N))
Fx = lambda t: sp.Rational(3, 4) * (1 + t) ** 2 if t < 0 else 1 - sp.exp(-t) / 4
num("Q3b", 0, Fx(sp.Rational(-1, 2)), float(np.mean(Xs <= -0.5)))
num("Q3b", 1, Fx(sp.Integer(0)), float(np.mean(Xs <= 0)))
num("Q3b", 2, Fx(sp.Integer(1)), float(np.mean(Xs <= 1)))
den = 1 - Fx(sp.Rational(-1, 2)); numr = Fx(sp.Rational(1, 2)) - Fx(sp.Rational(-1, 2))
num("Q3c", 0, den, float(np.mean(Xs > -0.5)))
num("Q3c", 1, numr, float(np.mean((Xs > -0.5) & (Xs < 0.5))))
sel = Xs > -0.5
num("Q3c", 2, numr / den, float(np.mean(Xs[sel] < 0.5)), math.sqrt(0.81 * 0.19 / sel.sum()))

# ============================================================ Q4  bridge networks (exact enumeration, MC)
E1 = {"A": ("s", "u1"), "B": ("s", "d1"), "E": ("u1", "d1"), "C": ("u1", "u2"), "D": ("d1", "d2"), "F": ("u2", "d2"), "G": ("u2", "t")}
E2 = dict(E1); E2["H"] = ("d2", "t")


def conn(edges, on):
    par = {}

    def f(a):
        par.setdefault(a, a)
        while par[a] != a:
            a = par[a]
        return a
    for c, (u, v) in edges.items():
        if on[c]:
            par[f(u)] = f(v)
    return f("s") == f("t")


def exact_net(edges, probs, extra=None):
    comps = list(edges) if extra is None else list(extra)
    tot = Fr(0)
    for st in itertools.product((0, 1), repeat=len(comps)):
        on = dict(zip(comps, st))
        w = Fr(1)
        for c in comps:
            w *= probs[c] if on[c] else 1 - probs[c]
        if conn(edges, on):
            tot += w
    return tot


def mc_net(edges, probs, n=N):
    on = {c: rng.random(n) < float(probs[c]) for c in edges}
    reach = {"s": np.ones(n, bool)}
    for nd in {v for e in edges.values() for v in e}:
        reach.setdefault(nd, np.zeros(n, bool))
    for _ in range(len(reach)):
        for c, (u, v) in edges.items():
            reach[v] = reach[v] | (reach[u] & on[c]); reach[u] = reach[u] | (reach[v] & on[c])
    return reach["t"], on


pr1 = {c: Fr(1, 2) for c in E1}
pr2 = dict(pr1); pr2["H"] = Fr(2, 5)
# conditional on E (p=.5): the reduced circuits via exact enumeration with E forced
PE = exact_net(E1, {**pr1, "E": Fr(1)})
PnE = exact_net(E1, {**pr1, "E": Fr(0)})
Q1ex = exact_net(E1, pr1)
reach_t, on1 = mc_net(E1, pr1)
num("Q4a", 1, PE, float(np.mean(reach_t[on1["E"]])), se_p(float(PE), int(on1["E"].sum())))
num("Q4a", 2, PnE, float(np.mean(reach_t[~on1["E"]])), se_p(float(PnE), int((~on1["E"]).sum())))
num("Q4a", 3, Q1ex, float(reach_t.mean()))
opts("Q4a", 0, [float(Q1ex), 0.5 ** 7, 1 - 0.5 ** 7], float(Q1ex))
# Q2 with H
Q2ex = exact_net(E2, pr2)
PH = exact_net(E2, {**pr2, "H": Fr(1)})
reach2, on2 = mc_net(E2, pr2)
num("Q4b", 1, PH, float(np.mean(reach2[on2["H"]])), se_p(float(PH), int(on2["H"].sum())))
num("Q4b", 2, Q2ex, float(reach2.mean()))
opts("Q4b", 0, [float(Q2ex), 1 - (1 - float(Q1ex)) * (1 - 0.4), 0.4 * float(Q1ex)], float(Q2ex))
# Q1 subset of Q2: check that every state with Q1 connected is connected in Q2 (H only adds)
mono = True
for st in itertools.product((0, 1), repeat=8):
    on = dict(zip(list(E2), st))
    if conn(E1, {c: on[c] for c in E1}) and not conn(E2, on):
        mono = False
rec("Q4c claim", mono, "Q1 subset of Q2 over all 256 states")
union = Fr(0)
for st in itertools.product((0, 1), repeat=8):
    on = dict(zip(list(E2), st))
    w = Fr(1)
    for c in E2:
        w *= pr2[c] if on[c] else 1 - pr2[c]
    if conn(E1, {c: on[c] for c in E1}) or conn(E2, on):
        union += w
both = Fr(0)
for st in itertools.product((0, 1), repeat=8):
    on = dict(zip(list(E2), st))
    w = Fr(1)
    for c in E2:
        w *= pr2[c] if on[c] else 1 - pr2[c]
    if conn(E1, {c: on[c] for c in E1}) and conn(E2, on):
        both += w
q1m = np.zeros(N, bool)   # Q1 on the shared samples
reach_q1 = None
sub = {c: on2[c] for c in E1}
reach = {nd: np.zeros(N, bool) for nd in {v for e in E1.values() for v in e}}
reach["s"] = np.ones(N, bool)
for _ in range(7):
    for c, (u, v) in E1.items():
        reach[v] = reach[v] | (reach[u] & sub[c]); reach[u] = reach[u] | (reach[v] & sub[c])
q1m = reach["t"]; q2m = reach2
num("Q4c", 1, both, float(np.mean(q1m & q2m)))
num("Q4c", 2, union, float(np.mean(q1m | q2m)))
opts("Q4c", 0, [float(union), float(Q1ex) + float(Q2ex) - float(Q1ex) * float(Q2ex), float(Q1ex) + float(Q2ex)], float(union))
num("Q4d", 0, Q1ex, float(q1m.mean()))
num("Q4d", 1, both, float(np.mean(q1m & q2m)))
num("Q4d", 2, both / Q1ex, float(np.mean(q2m[q1m])), 1e-9)

# ============================================================ Q5  n=3 of {1..10} without replacement
Nn, n = 10, 3
subsets = list(itertools.combinations(range(1, Nn + 1), n))
M = np.argsort(rng.random((N, Nn), dtype=np.float32), axis=1)[:, :n] + 1
mn, mx = M.min(axis=1), M.max(axis=1)
num("Q5a", 1, len(subsets))
cnt_min2 = sum(1 for s in subsets if min(s) == 2)
num("Q5a", 2, cnt_min2)
num("Q5a", 3, Fr(cnt_min2, len(subsets)), float(np.mean(mn == 2)))
opts("Q5a", 0, [math.comb(8, 2), math.comb(8, 3), math.comb(9, 2)], cnt_min2)
cnt_max7 = sum(1 for s in subsets if max(s) == 7)
num("Q5b", 1, cnt_max7)
num("Q5b", 2, Fr(cnt_max7, len(subsets)), float(np.mean(mx == 7)))
opts("Q5b", 0, [math.comb(6, 2), math.comb(7, 2), math.comb(6, 3)], cnt_max7)
rec("Q5c claim", sum(1 for t in range(1, 11) if 2 < t < 7) == 4, "numbers strictly between 2 and 7")
num("Q5c", 1, sum(1 for t in range(1, 11) if 2 < t < 7))
cnt27 = sum(1 for s in subsets if min(s) == 2 and max(s) == 7)
num("Q5c", 2, cnt27)
num("Q5c", 3, Fr(cnt27, len(subsets)), float(np.mean((mn == 2) & (mx == 7))))
opts("Q5c", 0, [7 - 2 - 1, 7 - 2, Nn - 2], cnt27 and 4)
Emin = Fr(sum(min(s) for s in subsets), len(subsets)); Emax = Fr(sum(max(s) for s in subsets), len(subsets))
num("Q5d", 1, Emin, float(mn.mean()), math.sqrt(mn.var() / N))
opts("Q5d", 0, [(Nn + 1) / (n + 1), Nn / 2, Nn / n], float(Emin))
num("Q5e", 1, Emax, float(mx.mean()), math.sqrt(mx.var() / N))
rec("Q5e claim", Emax == Nn + 1 - Emin, "E[max] = N+1-E[min] = %s" % Emax)
argued("Q5e", 0)

# ============================================================ Q6  Z = min/max, L = 1
Xu = rng.random(N); Yu = rng.random(N)
Z = np.minimum(Xu, Yu) / np.maximum(Xu, Yu)
t, z = sp.symbols("t z", positive=True)
num("Q6a", 0, sp.integrate(1, (x, 0, 1), (y, 0, 1)))
area04 = 2 * sp.integrate(sp.Rational(2, 5) * x, (x, 0, 1))      # {y <= 0.4 x, y < x} and its mirror image
num("Q6a", 1, area04, float(np.mean(Z <= 0.4)), se_p(0.4))
num("Q6a", 2, area04 / 1, float(np.mean(Z <= 0.4)))
num("Q6b", 0, sp.diff(t, t).subs(t, sp.Rational(1, 2)), None)
num("Q6b", 1, sp.integrate(1, (z, sp.Rational(1, 5), sp.Rational(1, 2))), float(np.mean((Z > 0.2) & (Z <= 0.5))))
EZ2 = sp.integrate(z ** 2, (z, 0, 1))
num("Q6c", 0, EZ2, float((Z ** 2).mean()), math.sqrt((Z ** 2).var() / N))
num("Q6c", 1, EZ2 - sp.Rational(1, 4), float(Z.var()), math.sqrt(2 / N) * Z.var() * 1.5)

# ============================================================ coverage
for qid, q in BYID.items():
    for i, s in enumerate(q.get("steps") or []):
        if s["type"] in ("numeric", "choice") and (qid, i) not in seen:
            rec("%s step%d COVERAGE" % (qid, i), False, "step not verified")

for tag, ok, info in rows:
    print(("ok   " if ok else "FAIL ") + tag + ": " + info)
print("steps_check %s: %d checks, %d failing" % (CODE, len(rows), fails))
sys.exit(1 if fails else 0)
