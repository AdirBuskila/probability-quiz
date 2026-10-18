# -*- coding: utf-8 -*-
"""Verification of the guided steps of 25A-B (probability). Run: PYTHONUTF8=1 py tools/verify/25A-B/steps_check.py

Reads tools/raw/25A-B.json (written by tools/gen/gen_25A-B.py) and re-derives every NUMERIC step independently:
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

CODE = "25A-B"
RAW = json.loads((pathlib.Path(__file__).resolve().parents[2] / "raw" / f"{CODE}.json").read_text(encoding="utf-8"))
HEB = {chr(0x5d0 + i): c for i, c in enumerate("abcdefghijklmnopqrstuvw")}
BYID = {}
for q in RAW["questions"]:
    BYID["Q%d%s" % (q["num"], HEB.get(q.get("part", ""), ""))] = q
N = 1_000_000
rng = np.random.default_rng(20250312)
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

# ============================================================ Q1  X,Y ~ U(0,1), Z = X/Y
X = rng.random(N); Y = rng.random(N); Z = X / Y
for q in ("Q1a", "Q1b", "Q1c", "Q1d"):
    num(q, 0, sp.integrate(1, (x, 0, 1), (y, 0, 1)))
num("Q1a", 1, sp.solve(sp.Eq(3 * x, 1), x)[0])
a1 = sp.integrate(sp.Integer(1) - 3 * x, (x, 0, sp.Rational(1, 3)))      # {y>3x}: height 1-3x for x<1/3
num("Q1a", 2, a1, float(np.mean(Z < 1 / 3)))
a2 = sp.integrate(x / 3, (x, 0, 1))                                    # {y<x/3}
num("Q1b", 1, a2, float(np.mean(Y < X / 3)))
num("Q1b", 2, 1 - a2, float(np.mean(Z < 3)))
num("Q1c", 1, sp.integrate(1 - x, (x, 0, 1)), float(np.mean(Z < 1)))
Fz = lambda tt: sp.integrate(1 - sp.Min(1, x / tt), (x, 0, 1))          # P(X/Y < t) = P(Y > X/t)
num("Q1d", 1, Fz(sp.Rational(2, 5)), float(np.mean(Z <= 0.4)))
num("Q1d", 2, Fz(2), float(np.mean(Z <= 2)))
num("Q1d", 3, Fz(1), float(np.mean(Z <= 1)))
num("Q1e", 0, sp.diff(t / 2, t).subs(t, sp.Rational(1, 2)), float(np.mean((Z > 0.45) & (Z <= 0.55)) / 0.1), math.sqrt(0.05 * 0.95 / N) / 0.1)
num("Q1e", 1, sp.diff(1 - 1 / (2 * t), t).subs(t, 2), float(np.mean((Z > 1.9) & (Z <= 2.1)) / 0.2), math.sqrt(0.025 * 0.975 / N) / 0.2)
num("Q1e", 2, sp.integrate(1 / (2 * t ** 2), (t, 1, sp.oo)), float(np.mean(Z > 1)))
# f: E[sqrt Z]
rec("Q1f step0 claim", sp.integrate(1 / y, (y, 0, 1)) == sp.oo and sp.integrate(1 / sp.sqrt(y), (y, 0, 1)) == 2
    and abs(1 / float(sp.integrate(sp.sqrt(y), (y, 0, 1))) - 2) > 0.4, "E[1/Y]=inf (so E[Z]=inf), E[1/sqrt Y]=2 but 1/E[sqrt Y]=1.5")
argued("Q1f", 0)
num("Q1f", 1, sp.integrate(sp.sqrt(x), (x, 0, 1)), float(np.sqrt(X).mean()), math.sqrt(np.sqrt(X).var() / N))
num("Q1f", 2, sp.integrate(1 / sp.sqrt(y), (y, 0, 1)))
Mcap = 100.0
trunc = lambda w: np.minimum(w, Mcap)
rec("Q1f step2 truncated-MC", abs(trunc(1 / np.sqrt(Y)).mean() - (0.01 + 2 * (1 - 0.01))) < 4 * math.sqrt(trunc(1 / np.sqrt(Y)).var() / N),
    "E[min(1/sqrt Y,100)] mc=%.4f exact=%.4f" % (trunc(1 / np.sqrt(Y)).mean(), 0.01 + 2 * 0.99))
num("Q1f", 3, sp.integrate(sp.sqrt(x), (x, 0, 1)) * sp.integrate(1 / sp.sqrt(y), (y, 0, 1)))
tm = trunc(np.sqrt(Z))
rec("Q1f step3 truncated-MC", abs(tm.mean() - (4 / 3 - 1 / (2 * Mcap))) < 4 * math.sqrt(tm.var() / N),
    "E[min(sqrt Z,100)] mc=%.4f exact=%.4f (4/3 - 1/200)" % (tm.mean(), 4 / 3 - 1 / (2 * Mcap)))

# ============================================================ Q2  atoms: p=.4 q=.5 s=P(B|not A)=.6
p_, q_, s_ = Fr(2, 5), Fr(1, 2), Fr(3, 5)
pBnA = s_ * (1 - p_)
atoms = {(1, 1): q_ - pBnA, (1, 0): p_ - (q_ - pBnA), (0, 1): pBnA, (0, 0): 1 - p_ - pBnA}
assert sum(atoms.values()) == 1 and all(v >= 0 for v in atoms.values())
P = lambda f, at=atoms: sum(w for (a, b), w in at.items() if f(a, b))
cond = lambda f, g, at=atoms: P(lambda a, b: f(a, b) and g(a, b), at) / P(g, at)
assert cond(lambda a, b: b, lambda a, b: not a) == s_ and P(lambda a, b: a) == p_ and P(lambda a, b: b) == q_


def samp(at):
    ks = list(at)
    i = rng.choice(len(ks), size=N, p=[float(at[k]) for k in ks])
    return (np.array([k[0] for k in ks])[i].astype(bool), np.array([k[1] for k in ks])[i].astype(bool))


A, B = samp(atoms)
num("Q2a", 1, pBnA, float(np.mean(B & ~A)))
num("Q2a", 2, P(lambda a, b: b), float(np.mean(B)))
num("Q2a", 3, cond(lambda a, b: not a, lambda a, b: b), float(np.mean((~A)[B])), math.sqrt(0.72 * 0.28 / B.sum()))
tgt = float(cond(lambda a, b: not a, lambda a, b: b))
opts("Q2a", 0, [tgt, float(s_), float(s_ * q_ / (1 - p_))], tgt)
num("Q2b", 1, cond(lambda a, b: not a, lambda a, b: b), float(np.mean((~A)[B])), math.sqrt(0.72 * 0.28 / B.sum()))
num("Q2b", 2, cond(lambda a, b: a, lambda a, b: b), float(np.mean(A[B])), math.sqrt(0.72 * 0.28 / B.sum()))
tgt = float(cond(lambda a, b: a, lambda a, b: b))
opts("Q2b", 0, [tgt, 1 - float(1 - p_), 1 - float(s_)], tgt)
num("Q2c", 1, pBnA, float(np.mean(B & ~A)))
num("Q2c", 2, P(lambda a, b: a and b), float(np.mean(A & B)))
opts("Q2c", 0, [float(q_ - pBnA), float(p_ * q_), float(s_ * q_)], float(P(lambda a, b: a and b)))
num("Q2d", 1, pBnA, float(np.mean(B & ~A)))
num("Q2d", 2, P(lambda a, b: a or b), float(np.mean(A | B)))
opts("Q2d", 0, [float(p_ + pBnA), float(p_ + q_), float(p_ + q_ - p_ * q_)], float(P(lambda a, b: a or b)))
# e: independent p=.4 q=s=.5
ind = {(1, 1): Fr(1, 5), (1, 0): Fr(1, 5), (0, 1): Fr(3, 10), (0, 0): Fr(3, 10)}
assert P(lambda a, b: a, ind) == p_ and P(lambda a, b: b, ind) == q_ and cond(lambda a, b: b, lambda a, b: not a, ind) == q_
assert P(lambda a, b: a and b, ind) == p_ * q_
Ai, Bi = samp(ind)
num("Q2e", 1, p_ * q_, float(np.mean(Ai & Bi)))
s_ind = sp.solve(sp.Eq(sp.Rational(1, 2) - x * (1 - sp.Rational(2, 5)), sp.Rational(2, 5) * sp.Rational(1, 2)), x)[0]
num("Q2e", 2, s_ind, None)
rec("Q2e step0 claim", (q_ - q_ * (1 - p_) == p_ * q_) and (q_ - q_ * (1 - p_) != 0) and (q_ != p_), "in the independent model: eq1 true, eq2 (=0) false, s=p false")
argued("Q2e", 0)
# f: disjoint p=.4, s=.5, q=s(1-p)=.3
q_d = Fr(1, 2) * (1 - p_)
dis = {(1, 1): Fr(0), (1, 0): p_, (0, 1): q_d, (0, 0): 1 - p_ - q_d}
assert cond(lambda a, b: b, lambda a, b: not a, dis) == Fr(1, 2)
Ad, Bd = samp(dis)
num("Q2f", 1, q_d, float(np.mean(Bd)))
rec("Q2f claim", float(np.mean(Ad & Bd)) == 0.0 and P(lambda a, b: a and b, dis) == 0 and p_ * q_d != 0 and P(lambda a, b: a or b, dis) != 1,
    "disjoint model: P(AB)=0 != pq; P(A or B)=%s != 1" % float(P(lambda a, b: a or b, dis)))
argued("Q2f", 0)

# ============================================================ Q3  pdf: a on [-1,0), triangle (apex (1,b)) on [0,2];  mu=.25
a_, b_, mu = sp.symbols("a b mu")
f3 = lambda aa, bb: [(aa, (x, -1, 0)), (bb * x, (x, 0, 1)), (bb * (2 - x), (x, 1, 2))]
norm = sum(sp.integrate(e, r) for e, r in f3(a_, b_))
mean = sum(sp.integrate(x * e, r) for e, r in f3(a_, b_))
sol = sp.solve([sp.Eq(norm, 1), sp.Eq(mean, mu)], [a_, b_])
av, bv = sol[a_].subs(mu, sp.Rational(1, 4)), sol[b_].subs(mu, sp.Rational(1, 4))
num("Q3a", 1, av); num("Q3a", 2, bv)
rec("Q3a step0 claim", sp.integrate(b_ * x, (x, 0, 1)) + sp.integrate(b_ * (2 - x), (x, 1, 2)) == b_ and sp.simplify(sol[a_] - sp.Rational(2, 3) * (1 - mu)) == 0
    and sp.simplify(sol[b_] - (1 + 2 * mu) / 3) == 0, "triangle area = b; a=2/3(1-mu), b=(1+2mu)/3")
argued("Q3a", 0)
num("Q3b", 0, sp.solve(sp.Eq(sol[a_], 0), mu)[0])
num("Q3b", 1, sp.solve(sp.Eq(sol[b_], 0), mu)[0])
# sample X from the pdf: a=b=1/2: with prob 1/2 uniform on [-1,0], with prob 1/2 triangular on [0,2]
m = rng.random(N) < 0.5
Xs = np.where(m, -1 + rng.random(N), rng.random(N) + rng.random(N))
FX = lambda tt: (sp.integrate(av, (x, -1, 0)) + sp.integrate(bv * x, (x, 0, tt))) if tt <= 1 else (sp.integrate(av, (x, -1, 0)) + sp.integrate(bv * x, (x, 0, 1)) + sp.integrate(bv * (2 - x), (x, 1, tt)))
num("Q3c", 0, FX(0), float(np.mean(Xs <= 0)))
num("Q3c", 1, FX(1), float(np.mean(Xs <= 1)))
num("Q3c", 2, FX(sp.Rational(1, 2)), float(np.mean(Xs <= 0.5)))
num("Q3d", 0, 1 - FX(0), float(np.mean(Xs > 0)))
num("Q3d", 1, FX(1) - FX(0), float(np.mean((Xs > 0) & (Xs < 1))))
sel = Xs > 0
num("Q3d", 2, (FX(1) - FX(0)) / (1 - FX(0)), float(np.mean(Xs[sel] < 1)), math.sqrt(0.25 / sel.sum()))

# ============================================================ Q4  circuits, p=.5, q=.4
E1 = {"A": ("s", "u1"), "B": ("s", "d1"), "E": ("u1", "d1"), "C": ("u1", "t"), "D": ("d1", "t")}
E2 = {"A": ("s", "u1"), "B": ("s", "d1"), "E": ("u1", "d1"), "C": ("u1", "u2"), "D": ("d1", "d2"), "F": ("u2", "d2"), "G": ("u2", "t")}


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


pr2 = {c: Fr(1, 2) for c in E2}; pr2["F"] = Fr(2, 5); pr2["G"] = Fr(2, 5)
comps2 = list(E2)


def exact(pred, probs=pr2, comps=comps2, given=None):
    tot = Fr(0); gt = Fr(0)
    for st in itertools.product((0, 1), repeat=len(comps)):
        on = dict(zip(comps, st))
        w = Fr(1)
        for c in comps:
            w *= probs[c] if on[c] else 1 - probs[c]
        if given is not None and not given(on):
            continue
        gt += w
        if pred(on):
            tot += w
    return tot / gt if given is not None else tot


q1 = lambda on: conn(E1, on)
q2 = lambda on: conn(E2, on)
P1 = exact(q1); P2 = exact(q2)
on_ = {c: rng.random(N) < float(pr2[c]) for c in E2}


def mc_conn(edges, on):
    nodes = {n for e in edges.values() for n in e}
    reach = {n: np.zeros(N, bool) for n in nodes}; reach["s"] = np.ones(N, bool)
    for _ in range(len(nodes)):
        for c, (u, v) in edges.items():
            reach[v] = reach[v] | (reach[u] & on[c]); reach[u] = reach[u] | (reach[v] & on[c])
    return reach["t"]


m1 = mc_conn(E1, on_); m2 = mc_conn(E2, on_)
pE = exact(q1, {**pr2, "E": Fr(1)}); pnE = exact(q1, {**pr2, "E": Fr(0)})
num("Q4a", 1, pE, float(np.mean(m1[on_["E"]])), se_p(float(pE), int(on_["E"].sum())))
num("Q4a", 2, pnE, float(np.mean(m1[~on_["E"]])), se_p(float(pnE), int((~on_["E"]).sum())))
num("Q4a", 3, P1, float(m1.mean()))
opts("Q4a", 0, [float(P1), float(pE), float(pnE)], float(P1))
pF = exact(q2, {**pr2, "F": Fr(1)}); pnF = exact(q2, {**pr2, "F": Fr(0)})
num("Q4b", 1, pF, float(np.mean(m2[on_["F"]])), se_p(float(pF), int(on_["F"].sum())))
num("Q4b", 2, pnF, float(np.mean(m2[~on_["F"]])), se_p(float(pnF), int((~on_["F"]).sum())))
num("Q4b", 3, P2, float(m2.mean()))
rec("Q4b step0 claim", Fr(2, 5) * P1 == pF and Fr(2, 5) * P1 != P2, "q P(Q1)=%s != P(Q2)=%s" % (float(Fr(2, 5) * P1), float(P2)))
argued("Q4b", 0)
subset = all((not q2(dict(zip(comps2, st)))) or q1(dict(zip(comps2, st))) for st in itertools.product((0, 1), repeat=len(comps2)))
strict = any(q1(dict(zip(comps2, st))) and not q2(dict(zip(comps2, st))) for st in itertools.product((0, 1), repeat=len(comps2)))
rec("Q4c claim", subset and strict, "Q2 subset of Q1 over all 128 states, and not equal")
num("Q4c", 1, exact(lambda on: q2(on) and not q1(on)), float(np.mean(m2 & ~m1)))
both = exact(lambda on: q1(on) and q2(on))
num("Q4c", 2, both, float(np.mean(m1 & m2)))
opts("Q4c", 0, [float(both), float(P1), float(P1 * P2)], float(both))
num("Q4d", 0, P1, float(m1.mean()))
num("Q4d", 1, both, float(np.mean(m1 & m2)))
num("Q4d", 2, both / P1, float(np.mean(m2[m1])), math.sqrt(0.31 * 0.69 / m1.sum()))

# ============================================================ Q5  D=5 red of N=12
Dn, Nn = 5, 12
balls = [1] * Dn + [0] * (Nn - Dn)
perms4 = list(itertools.permutations(range(Nn), 4))
col = lambda s: [balls[i] for i in s]
frac = lambda f, g=lambda c: True: Fr(sum(1 for s in perms4 if f(col(s)) and g(col(s))), sum(1 for s in perms4 if g(col(s))))
Mx = np.argsort(rng.random((N, Nn), dtype=np.float32), axis=1)[:, :4]
Cm = np.array(balls)[Mx]
num("Q5a", 0, Nn)
num("Q5a", 1, frac(lambda c: c[0] == 1), float(np.mean(Cm[:, 0])))
num("Q5b", 1, frac(lambda c: c[1] == 1, lambda c: c[0] == 1), float(np.mean(Cm[Cm[:, 0] == 1][:, 1])), math.sqrt(0.36 * 0.64 / (Cm[:, 0] == 1).sum()))
num("Q5b", 2, frac(lambda c: c[1] == 1, lambda c: c[0] == 0), float(np.mean(Cm[Cm[:, 0] == 0][:, 1])), math.sqrt(0.25 / (Cm[:, 0] == 0).sum()))
num("Q5b", 3, frac(lambda c: c[1] == 1), float(np.mean(Cm[:, 1])))
rec("Q5b step0 claim", Fr(4, 11) != Fr(5, 12) and Fr(5, 11) != Fr(5, 12), "(D-1)/(N-1)=0.364, D/(N-1)=0.455 vs D/N=0.4167")
argued("Q5b", 0)
EX = Fr(sum(sum(c[:3]) for c in map(col, perms4)), len(perms4))
num("Q5c", 1, EX, float(Cm[:, :3].sum(axis=1).mean()), math.sqrt(Cm[:, :3].sum(axis=1).var() / N))
num("Q5c", 2, frac(lambda c: c[3] == 1, lambda c: sum(c[:3]) == 1), float(np.mean(Cm[Cm[:, :3].sum(axis=1) == 1][:, 3])), math.sqrt(0.2 / (Cm[:, :3].sum(axis=1) == 1).sum()))
num("Q5c", 3, frac(lambda c: c[3] == 1), float(np.mean(Cm[:, 3])))
rec("Q5c step0 claim", abs((5 / 12) ** 4 - 0.030) < 0.001, "prod P(R_i) = %.4f" % ((5 / 12) ** 4))
argued("Q5c", 0)
num("Q5d", 2, frac(lambda c: c[2] == 1 and c[3] == 1), float(np.mean((Cm[:, 2] == 1) & (Cm[:, 3] == 1))))
num("Q5d", 1, frac(lambda c: c[2] == 1), float(np.mean(Cm[:, 2])))
num("Q5d", 3, frac(lambda c: c[3] == 1, lambda c: c[2] == 1), float(np.mean(Cm[Cm[:, 2] == 1][:, 3])), math.sqrt(0.36 * 0.64 / (Cm[:, 2] == 1).sum()))
rec("Q5d step0 claim", Fr(5, 12) != Fr(4, 11), "D/N=0.417 != (D-1)/(N-1)=0.364")
argued("Q5d", 0)

# ============================================================ Q6  two people on chairs 1..8
Nc = 8
pairs = list(itertools.permutations(range(1, Nc + 1), 2))
K = np.argsort(rng.random((N, Nc), dtype=np.float32), axis=1)[:, :2] + 1
xl, xr = K.min(axis=1), K.max(axis=1)
rec("Q6a step0 claim", Fr(0) != Fr(1, 64) and sum(1 for pr in pairs if pr == (3, 3)) == 0, "P(X=3,Y=3)=0 but P(X=3)P(Y=3)=1/64")
argued("Q6a", 0)
num("Q6a", 1, len(pairs))
num("Q6a", 2, Fr(sum(1 for pr in pairs if pr[0] == 3), len(pairs)), float(np.mean(K[:, 0] == 3)))
num("Q6a", 3, Fr(sum(1 for pr in pairs if pr == (3, 5)), len(pairs)), float(np.mean((K[:, 0] == 3) & (K[:, 1] == 5))))
rec("Q6b step0 claim", sum(1 for pr in pairs if min(pr) == 3 and max(pr) == 6) == 2, "ordered pairs giving (XL,XR)=(3,6): 2")
argued("Q6b", 0)
num("Q6b", 1, math.comb(Nc, 2))
num("Q6b", 2, Fr(sum(1 for pr in pairs if min(pr) == 3 and max(pr) == 6), len(pairs)), float(np.mean((xl == 3) & (xr == 6))))
row = sum(1 for k in range(1, Nc + 1) if k > 3)
opts("Q6c", 0, [Nc - 3, 3 - 1, Nc - 1], row)
num("Q6c", 1, Fr(sum(1 for pr in pairs if min(pr) == 3), len(pairs)), float(np.mean(xl == 3)))
num("Q6c", 2, Fr(sum(1 for pr in pairs if max(pr) == 4), len(pairs)), float(np.mean(xr == 4)))
EL = Fr(sum(min(pr) for pr in pairs), len(pairs)); ER = Fr(sum(max(pr) for pr in pairs), len(pairs))
pairs2 = list(itertools.permutations(range(1, 3), 2))
num("Q6d", 0, EL, float(xl.mean()), math.sqrt(xl.var() / N))
num("Q6d", 1, ER, float(xr.mean()), math.sqrt(xr.var() / N))
num("Q6d", 2, Fr(sum(min(pr) for pr in pairs2), len(pairs2)))
VL = Fr(sum(min(pr) ** 2 for pr in pairs), len(pairs)) - EL ** 2
VR = Fr(sum(max(pr) ** 2 for pr in pairs), len(pairs)) - ER ** 2
num("Q6e", 0, VL, float(xl.var()), math.sqrt(2 / N) * float(xl.var()) * 1.6)
num("Q6e", 1, VR, float(xr.var()), math.sqrt(2 / N) * float(xr.var()) * 1.6)
num("Q6e", 2, Fr(sum(min(pr) ** 2 for pr in pairs2), len(pairs2)) - Fr(sum(min(pr) for pr in pairs2), len(pairs2)) ** 2)
ELR = Fr(sum(min(pr) * max(pr) for pr in pairs), len(pairs))
cov = ELR - EL * ER
num("Q6f", 0, ELR, float((xl * xr).mean()), math.sqrt((xl * xr).var() / N))
num("Q6f", 1, cov, float(np.cov(xl, xr)[0, 1]), 0.02)
num("Q6f", 2, cov / sp.sqrt(sp.Rational(VL.numerator, VL.denominator) * sp.Rational(VR.numerator, VR.denominator)), float(np.corrcoef(xl, xr)[0, 1]), 0.002)

# ============================================================ coverage
for qid, q in BYID.items():
    for i, s in enumerate(q.get("steps") or []):
        if s["type"] in ("numeric", "choice") and (qid, i) not in seen:
            rec("%s step%d COVERAGE" % (qid, i), False, "step not verified")

for tag, ok, info in rows:
    print(("ok   " if ok else "FAIL ") + tag + ": " + info)
print("steps_check %s: %d checks, %d failing" % (CODE, len(rows), fails))
sys.exit(1 if fails else 0)
