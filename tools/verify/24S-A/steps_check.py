# -*- coding: utf-8 -*-
"""Step verification for 24S-A (probability). Run: PYTHONUTF8=1 py tools/verify/24S-A/steps_check.py

Reads tools/raw/24S-A.json (written by tools/gen/gen_24S-A.py) and, for every numeric step,
re-derives the expected value INDEPENDENTLY of the generator:
  EXACT : fractions / enumeration / sympy / exact clipping;
  MC    : Monte Carlo (>= 10^6 trials) agrees within 4 standard errors, where a simulation applies.
Choice steps with a checkable claim (distractors that must fail) are asserted numerically.
Every numeric step must be covered by an EXACT check. Exit code 1 on any failure. Output is ASCII only.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = json.loads((ROOT / "raw" / "24S-A.json").read_text(encoding="utf-8"))
BY = {(q["num"], q.get("part")): q for q in RAW["questions"]}
N = 2_000_000
rng = np.random.default_rng(20241014)
rows = []
checked = set()


def S(num, part, i):
    return BY[(num, part)]["steps"][i]


def ex(num, part, i, val, what):
    checked.add((num, part, i))
    s = S(num, part, i)
    ok = s["type"] == "numeric" and abs(s["answer"] - float(val)) <= 1e-9
    rows.append((f"Q{num}{part}#{i}", "EXACT " + what, ok, f"stored={s.get('answer')} exact={float(val):.9f}"))


def mc(num, part, i, est, se, what):
    s = S(num, part, i)
    ok = abs(s["answer"] - est) <= 4 * se + 1e-12
    rows.append((f"Q{num}{part}#{i}", "MC    " + what, ok, f"stored={s['answer']:.6f} mc={est:.6f} se={se:.6f}"))


def claim(tag, ok, what):
    rows.append((tag, "CLAIM " + what, bool(ok), ""))


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-12) / n)


# ---------------------------------------------------------------- Q1  unit square
x, y = sp.symbols("x y", positive=True)
ex(1, "א", 0, sp.solve(sp.Eq(x**2, 1), x)[0], "side of a square of area 1")
X = rng.random(N); Y = rng.random(N)
quarter = sp.integrate(sp.sqrt(1 - x**2), (x, 0, 1))
small = sp.integrate(sp.sqrt(sp.Rational(1, 4) - x**2), (x, 0, sp.Rational(1, 2)))
ex(1, "ב", 1, 1, "|Omega|=1")
ex(1, "ב", 2, quarter, "P(L<1) = area of quarter disc"); ex(1, "ב", 3, small, "area quarter disc radius 1/2 = pi/16")
ex(1, "ב", 4, quarter - small, "P(1/2<L<1)")
Rr = np.sqrt(X**2 + Y**2)
mc(1, "ב", 2, float((Rr < 1).mean()), se_p(math.pi / 4), "P(L<1)")
mc(1, "ב", 3, float((Rr < .5).mean()), se_p(math.pi / 16), "P(L<1/2)")
mc(1, "ב", 4, float(((Rr > .5) & (Rr < 1)).mean()), se_p(3 * math.pi / 16), "P(1/2<L<1)")
# square-side claim for the parallel sides: L = sqrt(1+(X-Y)^2) and the equivalence with |X-Y|<1/3
Lp = np.sqrt(1 + (X - Y) ** 2)
claim("Q1c#0", bool(((Lp < math.sqrt(10) / 3) == (np.abs(X - Y) < 1 / 3)).all()) and bool(((Lp < math.sqrt(10) / 3) != (np.abs(X - Y) < 1 / 9)).any()),
      "L<sqrt(10)/3 <=> |X-Y|<1/3 (and not |X-Y|<1/9)")


def clip(poly, a, b, c):
    out = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * P[0] + b * P[1] - c, a * Q[0] + b * Q[1] - c
        if fp >= 0:
            out.append(P)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out


def area(poly):
    if len(poly) < 3:
        return Fr(0)
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))) / 2


SQ = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(1), Fr(1)), (Fr(0), Fr(1))]
third = Fr(1, 3)
band = area(clip(clip(SQ, Fr(1), Fr(-1), -third), Fr(-1), Fr(1), -third))      # x-y >= -1/3 and y-x >= -1/3
corners = 1 - band
ex(1, "ג", 1, 1, "|Omega|=1"); ex(1, "ג", 2, corners, "two corner triangles"); ex(1, "ג", 3, band, "P(|X-Y|<1/3) = 5/9")
mc(1, "ג", 3, float((Lp < math.sqrt(10) / 3).mean()), se_p(5 / 9), "P(L<sqrt(10)/3)")

# ---------------------------------------------------------------- Q2  dice
def seqs(total, k):
    return sum(1 for s in itertools.product(range(1, 7), repeat=k) if sum(s) == total)


counts = [seqs(5, k) for k in range(1, 6)]
claim("Q2a counts", counts == [1, 4, 6, 4, 1], "ordered compositions of 5 into k rolls: 1,4,6,4,1")
ever = sum(Fr(c, 6**k) for k, c in zip(range(1, 6), counts))
ex(2, "א", 1, Fr(counts[1], 36), "P(sum=5 in 2 rolls)"); ex(2, "א", 2, Fr(counts[2], 216), "P(sum=5 in 3 rolls)")
ex(2, "א", 3, ever, "P(sum ever = 5)")
claim("Q2a closed form", ever == Fr(7**4, 6**5), "equals 7^4/6^5")
rolls = rng.integers(1, 7, (N, 6)); cs = rolls.cumsum(1)
hit = (cs == 5).any(1)
mc(2, "א", 3, float(hit.mean()), se_p(float(ever)), "P(sum ever = 5)")
claim("Q2a#0", abs(float(ever) - 1 / 3.5) > 0.02, "1/3.5 is only an approximation of the exact value")
pairs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
ex(2, "ב", 1, sum(1 for a, b in pairs if a + b == 5), "pairs with sum 5"); ex(2, "ב", 2, Fr(4, 36), "P(sum 2 rolls = 5)")
claim("Q2b#0", len(pairs) == 36 and Fr(sum(1 for a, b in pairs if a + b == 7), 36) != Fr(sum(1 for a, b in pairs if a + b == 2), 36), "36 ordered pairs; sums are not equally likely")
ex(2, "ג", 0, 6**3, "|Omega|=216"); ex(2, "ג", 1, seqs(5, 3), "triples with sum 5"); ex(2, "ג", 2, Fr(seqs(5, 3), 216), "P")
D = [(a, b, c) for a, b, c in itertools.product(range(1, 7), repeat=3) if a + b == 3]
CD = [t for t in D if sum(t) == 5]
ex(2, "ד", 1, Fr(len(D), 216), "P(D)"); ex(2, "ד", 2, Fr(len(CD), 216), "P(C n D)"); ex(2, "ד", 3, Fr(len(CD), len(D)), "P(C|D)")
claim("Q2d#0", all(t[2] == 2 for t in CD), "third roll must be 2")
r3 = rng.integers(1, 7, (N, 3)); Dm = (r3[:, 0] + r3[:, 1]) == 3; Cm = r3.sum(1) == 5
mc(2, "ד", 1, float(Dm.mean()), se_p(1 / 18), "P(D)"); mc(2, "ד", 3, float(Cm[Dm].mean()), se_p(1 / 6, int(Dm.sum())), "P(C|D)")

# ---------------------------------------------------------------- Q3  three tosses, p = 0.3
p = Fr(3, 10)
outs = list(itertools.product([0, 1], repeat=3))
w = lambda o: p ** sum(o) * (1 - p) ** (3 - sum(o))
PXY = lambda xv, yv: sum(w(o) for o in outs if o[0] + o[1] == xv and o[1] + o[2] == yv)
ex(3, "א", 1, PXY(1, 1), "P_XY(1,1)"); ex(3, "א", 2, PXY(0, 1), "P_XY(0,1)"); ex(3, "א", 3, PXY(2, 1), "P_XY(2,1)")
claim("Q3a#0", sum(PXY(a, b) for a in range(3) for b in range(3)) == 1 and PXY(1, 1) != Fr(42, 100) * Fr(42, 100), "table normalised; (1,1) differs from the product of marginals")
PX = lambda xv: sum(w(o) for o in outs if o[0] + o[1] == xv); PY = lambda yv: sum(w(o) for o in outs if o[1] + o[2] == yv)
ex(3, "ב", 1, PX(1), "P_X(1)"); ex(3, "ב", 2, PY(2), "P_Y(2)")
EXv = sum(xv * PX(xv) for xv in range(3)); VarX = sum(xv * xv * PX(xv) for xv in range(3)) - EXv**2
ex(3, "ג", 1, EXv, "E[X]"); ex(3, "ג", 2, VarX, "Var[X]")
ex(3, "ד", 0, PXY(2, 0), "P_XY(2,0)"); ex(3, "ד", 1, PX(2) * PY(0), "P_X(2)P_Y(0)")
T3 = rng.random((N, 3)) < 0.3
xx = T3[:, 0].astype(int) + T3[:, 1]; yy = T3[:, 1].astype(int) + T3[:, 2]
mc(3, "א", 1, float(((xx == 1) & (yy == 1)).mean()), se_p(.21), "P_XY(1,1)"); mc(3, "א", 2, float(((xx == 0) & (yy == 1)).mean()), se_p(.147), "P_XY(0,1)")
mc(3, "א", 3, float(((xx == 2) & (yy == 1)).mean()), se_p(.063), "P_XY(2,1)")
mc(3, "ב", 1, float((xx == 1).mean()), se_p(.42), "P_X(1)"); mc(3, "ב", 2, float((yy == 2).mean()), se_p(.09), "P_Y(2)")
mc(3, "ג", 1, float(xx.mean()), float(xx.std()) / math.sqrt(N), "E[X]"); mc(3, "ג", 2, float(xx.var()), float(xx.var()) * math.sqrt(2 / N) * 1.5, "Var[X]")

# ---------------------------------------------------------------- Q4  f = a on [-1,0), b e^-x on [0,oo)
a, b, t = sp.symbols("a b t", real=True)
xs = sp.Symbol("xs", real=True)
sol = sp.solve([sp.integrate(a, (xs, -1, 0)) + sp.integrate(b * sp.exp(-xs), (xs, 0, sp.oo)) - 1,
                sp.integrate(xs * a, (xs, -1, 0)) + sp.integrate(xs * b * sp.exp(-xs), (xs, 0, sp.oo))], [a, b], dict=True)[0]
ex(4, "א", 2, sol[a], "a"); ex(4, "א", 3, sol[b], "b")
claim("Q4a#1", sp.integrate(xs, (xs, -1, 0)) == sp.Rational(-1, 2) and sp.integrate(xs * sp.exp(-xs), (xs, 0, sp.oo)) == 1, "-a/2 + b = 0 is the mean equation")
Fx = lambda tt: sol[a] * (tt + 1) if tt < 0 else sol[a] + sol[b] * (1 - sp.exp(-tt))
ex(4, "ב", 0, Fx(sp.Rational(-1, 2)), "F(-1/2)"); ex(4, "ב", 1, Fx(0), "F(0)"); ex(4, "ב", 2, Fx(2), "F(2)")
ex(4, "ג", 0, Fx(1), "F(1)"); ex(4, "ג", 1, Fx(1) - Fx(sp.Rational(-1, 2)), "P(-1/2<X<1)"); ex(4, "ג", 2, (Fx(1) - Fx(sp.Rational(-1, 2))) / Fx(1), "P(X>-1/2|X<1)")
claim("Q4c closed form", abs(float((Fx(1) - Fx(sp.Rational(-1, 2))) / Fx(1)) - (2 * math.e - 1) / (3 * math.e - 1)) < 1e-12, "= (2e-1)/(3e-1)")
u = rng.random(N)
Xs = np.where(u < 2 / 3, u * 1.5 - 1, -np.log(np.maximum(1 - u, 1e-300) * 3))
mc(4, "ב", 0, float((Xs <= -.5).mean()), se_p(1 / 3), "F(-1/2)"); mc(4, "ב", 1, float((Xs <= 0).mean()), se_p(2 / 3), "F(0)")
mc(4, "ב", 2, float((Xs <= 2).mean()), se_p(float(Fx(2))), "F(2)"); mc(4, "ג", 0, float((Xs < 1).mean()), se_p(float(Fx(1))), "F(1)")
sel = Xs < 1
mc(4, "ג", 2, float((Xs[sel] > -.5).mean()), se_p(0.62, int(sel.sum())), "P(X>-1/2|X<1)")
claim("Q4 mean", abs(Xs.mean()) < 4 * Xs.std() / math.sqrt(N), "sampled density has mean 0")

# ---------------------------------------------------------------- Q5  students
from math import comb
ex(5, "א", 1, comb(5, 2) * Fr(3, 10) ** 2 * Fr(7, 10) ** 3, "Bin(5,0.3) P(2)")
mc(5, "א", 1, float(((rng.random((N, 5)) < 0.3).sum(1) == 2).mean()), se_p(0.3087), "Bin(5,0.3) P(2)")
pa, Qb = Fr(1, 2), Fr(1, 5)
ex(5, "ב", 1, pa * Qb, "pQ"); ex(5, "ב", 2, (1 - pa * Qb) ** 5, "P(Y=0)"); ex(5, "ב", 3, 5 * pa * Qb * (1 - pa * Qb) ** 4, "P(Y=1)")
came = rng.random((N, 5)) < 0.5; born = rng.random((N, 5)) < 0.2
Y = (came & born).sum(1); Xc = came.sum(1)
mc(5, "ב", 2, float((Y == 0).mean()), se_p(0.59049), "P(Y=0)"); mc(5, "ב", 3, float((Y == 1).mean()), se_p(0.32805), "P(Y=1)")
# exact joint (X, Y): X ~ Bin(5, 1/2), Y | X ~ Bin(X, 1/5)
joint = {(j, k): comb(5, j) * Fr(1, 2) ** 5 * comb(j, k) * Qb**k * (1 - Qb) ** (j - k) for j in range(6) for k in range(j + 1)}
PYk = lambda k: sum(v for (j, kk), v in joint.items() if kk == k)
ex(5, "ג", 1, (1 - pa) / (1 - pa * Qb), "p tilde")
ex(5, "ג", 2, joint[(3, 1)] / PYk(1), "P(X=3|Y=1)")
claim("Q5b closed form", all(abs(float(PYk(k)) - comb(5, k) * 0.1**k * 0.9 ** (5 - k)) < 1e-12 for k in range(6)), "Y ~ Bin(5, pQ) exactly")
pt = (1 - pa) / (1 - pa * Qb)
claim("Q5c closed form", joint[(3, 1)] / PYk(1) == comb(4, 2) * pt**2 * (1 - pt) ** 2, "binomial in p tilde")
sel = Y == 1
mc(5, "ג", 2, float((Xc[sel] == 3).mean()), se_p(float(joint[(3, 1)] / PYk(1)), int(sel.sum())), "P(X=3|Y=1)")

# ---------------------------------------------------------------- Q6  graph on four nodes, brute force over 2^6 unit states, p = 3/5
edges = {"A": ("L", "T"), "C": ("T", "R"), "B": ("T", "M"), "D": ("L", "M"), "E": ("M", "R"), "F": ("L", "R")}
names = list(edges)
pr6 = Fr(3, 5)


def works(state):
    adj = {}
    for nm, v in zip(names, state):
        if v:
            u1, u2 = edges[nm]
            adj.setdefault(u1, set()).add(u2); adj.setdefault(u2, set()).add(u1)
    seen, stack = {"L"}, ["L"]
    while stack:
        cur = stack.pop()
        for nb in adj.get(cur, ()):
            if nb not in seen:
                seen.add(nb); stack.append(nb)
    return "R" in seen


def P6(pred):
    tot = Fr(0)
    for st in itertools.product([0, 1], repeat=6):
        wgt = Fr(1)
        for v in st:
            wgt *= pr6 if v else 1 - pr6
        if pred(st):
            tot += wgt
    return tot


iB = names.index("B")
PQ6 = P6(works)
PQB = P6(lambda st: works(st) and st[iB]) / pr6
PQN = P6(lambda st: works(st) and not st[iB]) / (1 - pr6)
ex(6, "א", 1, PQB, "P(Q|B)"); ex(6, "א", 2, PQN, "P(Q|~B)"); ex(6, "א", 3, PQ6, "P(Q)")
pp = sp.Rational(3, 5)
claim("Q6a poly", sp.Rational(PQ6.numerator, PQ6.denominator) == pp * (1 + 2 * pp - 7 * pp**3 + 7 * pp**4 - 2 * pp**5), "P(Q)=p(1+2p-7p^3+7p^4-2p^5)")
ex(6, "ב", 1, PQN, "P(Q|~B)"); ex(6, "ב", 2, PQ6, "P(Q)"); ex(6, "ב", 3, (1 - pr6) * PQN / PQ6, "P(~B|Q)")
one_fail = [st for st in itertools.product([0, 1], repeat=6) if sum(st) == 5]
ex(6, "ג", 0, sum(1 for st in one_fail if not works(st)), "single-failure states that break the circuit")
ex(6, "ג", 1, P6(lambda st: works(st) and sum(st) == 5) / P6(lambda st: sum(st) == 5), "P(Q | exactly one fails)")
claim("Q6c min cut", min(sum(1 - v for v in st) for st in itertools.product([0, 1], repeat=6) if not works(st)) >= 2, "every failing state has >= 2 failed units")
ex(6, "ד", 0, PQ6, "P(Q)"); ex(6, "ד", 1, pr6**6, "P(all work)"); ex(6, "ד", 2, pr6**6 / PQ6, "P(all|Q)")
st6 = rng.random((N, 6)) < 0.6
# vectorised reachability by iterating label propagation
def works_vec(st):
    idx = {n: i for i, n in enumerate(names)}
    reach = {"L": np.ones(len(st), bool), "T": np.zeros(len(st), bool), "M": np.zeros(len(st), bool), "R": np.zeros(len(st), bool)}
    for _ in range(4):
        for nm, (u1, u2) in edges.items():
            on = st[:, idx[nm]]
            reach[u2] = reach[u2] | (reach[u1] & on)
            reach[u1] = reach[u1] | (reach[u2] & on)
    return reach["R"]


Qm = works_vec(st6)
mc(6, "א", 3, float(Qm.mean()), se_p(float(PQ6)), "P(Q)")
mc(6, "א", 1, float(Qm[st6[:, iB]].mean()), se_p(float(PQB), int(st6[:, iB].sum())), "P(Q|B)")
mc(6, "א", 2, float(Qm[~st6[:, iB]].mean()), se_p(float(PQN), int((~st6[:, iB]).sum())), "P(Q|~B)")
mc(6, "ב", 3, float((~st6[:, iB])[Qm].mean()), se_p(float((1 - pr6) * PQN / PQ6), int(Qm.sum())), "P(~B|Q)")
mc(6, "ד", 2, float((st6.all(1))[Qm].mean()), se_p(float(pr6**6 / PQ6), int(Qm.sum())), "P(all|Q)")
mc(6, "ד", 1, float(st6.all(1).mean()), se_p(float(pr6**6)), "P(all work)")

# ---------------------------------------------------------------- coverage: every numeric step must have an EXACT check
for (num_, part_), q_ in BY.items():
    for i_, st_ in enumerate(q_.get("steps", [])):
        if st_["type"] == "numeric" and (num_, part_, i_) not in checked:
            rows.append((f"Q{num_}{part_}#{i_}", "COVERAGE numeric step without an exact check", False, ""))

# ---------------------------------------------------------------- report
bad = 0
for item, what, ok, detail in rows:
    bad += not ok
    print(("ok   " if ok else "FAIL ") + f"{item:8s} {what}  {detail}")
print(f"\n{len(rows)} checks, {bad} failures")
sys.exit(1 if bad else 0)
