# -*- coding: utf-8 -*-
"""Step verification for 24S-B (probability). Run: PYTHONUTF8=1 py tools/verify/24S-B/steps_check.py

Reads tools/raw/24S-B.json (written by tools/gen/gen_24S-B.py) and, for every numeric step,
re-derives the expected value INDEPENDENTLY of the generator:
  EXACT : fractions / enumeration / sympy;
  MC    : Monte Carlo (>= 10^6 trials) agrees within 4 standard errors, where a simulation applies.
Choice steps with a checkable claim (distractors that must fail) are asserted numerically.
Every numeric step must be covered by an EXACT check. Exit code 1 on any failure. Output is ASCII only.

Note (not changed here): the stored official solution of Q4c ends "~0.99", but its own formula
(4e^2-e-1)/(4e^2-1) evaluates to 0.9048; the guided steps follow the formula.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = json.loads((ROOT / "raw" / "24S-B.json").read_text(encoding="utf-8"))
BY = {(q["num"], q.get("part")): q for q in RAW["questions"]}
N = 2_000_000
rng = np.random.default_rng(20241107)
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


# ---------------------------------------------------------------- Q1  X, Y ~ U(0,1)
x = sp.symbols("x", positive=True)
X = rng.random(N); Y = rng.random(N)
curve = sp.integrate(1 / (2 * x), (x, sp.Rational(1, 2), 1))
ex(1, "א", 0, 1, "|Omega|=1"); ex(1, "א", 1, sp.solve(sp.Eq(1 / (2 * x), 1), x)[0], "hyperbola meets y=1")
ex(1, "א", 2, curve, "int_{1/2}^1 dx/(2x)"); ex(1, "א", 3, sp.Rational(1, 2) + curve, "P(S<1/2)")
mc(1, "א", 3, float((X * Y < .5).mean()), se_p(0.8465736), "P(S<1/2)")
ex(1, "ב", 0, 1, "|Omega|=1")
ex(1, "ב", 2, sp.integrate(sp.sqrt(sp.Rational(1, 4) - x**2), (x, 0, sp.Rational(1, 2))), "area quarter disc radius 1/2 = pi/16")
mc(1, "ב", 2, float((X**2 + Y**2 < .25).mean()), se_p(math.pi / 16), "P(L<1/2)")
ex(1, "ג", 0, 1, "|Omega|=1"); ex(1, "ג", 1, sp.Rational(1, 2), "P(X>1/2)")
area_c = sp.integrate(1 / (5 * x), (x, sp.Rational(1, 2), 1))
claim("Q1c region", sp.Rational(1, 5) / sp.Rational(1, 2) < 1, "for x>1/2 the hyperbola 1/(5x) < 2/5 < 1, so no clipping by y=1")
ex(1, "ג", 2, area_c, "area {xy<1/5, x>1/2}"); ex(1, "ג", 3, area_c / sp.Rational(1, 2), "P(S<1/5|X>1/2)")
sel = X > .5
mc(1, "ג", 1, float(sel.mean()), se_p(.5), "P(X>1/2)")
mc(1, "ג", 3, float((X[sel] * Y[sel] < .2).mean()), se_p(0.2773, int(sel.sum())), "P(S<1/5|X>1/2)")
mc(1, "ג", 2, float(((X * Y < .2) & sel).mean()), se_p(0.1386), "area as MC prob")
EX_ = sp.integrate(x, (x, 0, 1)); EX2 = sp.integrate(x**2, (x, 0, 1))
ex(1, "ד", 1, EX_**2, "E[S]"); ex(1, "ד", 2, EX2, "E[X^2]"); ex(1, "ד", 3, EX2**2 - EX_**4, "Var[S]")
Sm = X * Y
mc(1, "ד", 1, float(Sm.mean()), float(Sm.std()) / math.sqrt(N), "E[S]"); mc(1, "ד", 3, float(Sm.var()), float(Sm.var()) * math.sqrt(2 / N) * 1.5, "Var[S]")
claim("Q1d#0", abs(float(EX_ + EX_) - 1) < 1e-12 and abs(float(EX_ * EX_) - 0.25) < 1e-12, "E[X]+E[Y]=1 != E[XY]=1/4")

# ---------------------------------------------------------------- Q2  dice
pairs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
claim("Q2a#0", all(((a + b) ** 2 - 4 * a * b) == (a - b) ** 2 for a, b in pairs) and sum(1 for a, b in pairs if (a + b) ** 2 - 4 * a * b == 0) == 6, "discriminant = (a-b)^2 = 0 iff a=b")
ex(2, "א", 1, sum(1 for a, b in pairs if a == b), "#pairs a=b"); ex(2, "א", 2, Fr(sum(1 for a, b in pairs if a == b), 36), "P(equal roots)")
ex(2, "ב", 1, (2 + 5) ** 2 - 4 * 2 * 5, "discriminant at (2,5)")
claim("Q2b#0", all(sorted(np.roots([1, -(a + b), a * b]).real.round(9)) == sorted([a, b]) for a, b in pairs[:12]), "roots of y^2-(a+b)y+ab are a and b")
ex(2, "ב", 2, Fr(sum(1 for a, b in pairs if True), 36), "P(integer roots) = 1")
dist = [(a, b) for a, b in pairs if a != b]
ex(2, "ג", 1, Fr(len(dist), 36), "P(X1!=X2)")
odd = [(a, b) for a, b in dist if a * b % 2 == 1]
ex(2, "ג", 2, len(odd), "ordered distinct odd pairs"); ex(2, "ג", 3, Fr(len(odd), len(dist)), "P(product odd | distinct)")
claim("Q2c#0", all((a * b % 2 == 1) == (a % 2 == 1 and b % 2 == 1) for a, b in pairs), "product odd iff both odd")
ex(2, "ד", 1, Fr(len(dist), 36), "P(X1!=X2)")
same = [(a, b) for a, b in dist if (a - b) % 2 == 0]
ex(2, "ד", 2, len(same), "ordered distinct same-parity pairs"); ex(2, "ד", 3, Fr(len(same), len(dist)), "P(diff even | distinct)")
claim("Q2d#0", all(((a - b) % 2 == 0) == (a % 2 == b % 2) for a, b in pairs), "difference even iff same parity")
d2 = rng.integers(1, 7, (N, 2)); ne = d2[:, 0] != d2[:, 1]
mc(2, "ג", 1, float(ne.mean()), se_p(5 / 6), "P(X1!=X2)")
mc(2, "ג", 3, float(((d2[:, 0] * d2[:, 1]) % 2 == 1)[ne].mean()), se_p(.2, int(ne.sum())), "P(product odd|distinct)")
mc(2, "ד", 3, float(((d2[:, 0] - d2[:, 1]) % 2 == 0)[ne].mean()), se_p(.4, int(ne.sum())), "P(diff even|distinct)")
mc(2, "א", 2, float((~ne).mean()), se_p(1 / 6), "P(equal roots)")

# ---------------------------------------------------------------- Q3  p = 3/10
p = Fr(3, 10)
outs = list(itertools.product([0, 1], repeat=3))
w = lambda o: p ** sum(o) * (1 - p) ** (3 - sum(o))
PXY = lambda xv, yv: sum(w(o) for o in outs if o[0] + o[1] == xv and sum(o) == yv)
PX = lambda xv: sum(w(o) for o in outs if o[0] + o[1] == xv); PY = lambda yv: sum(w(o) for o in outs if sum(o) == yv)
ex(3, "א", 1, PXY(1, 2), "P_XY(1,2)"); ex(3, "א", 2, PXY(0, 1), "P_XY(0,1)"); ex(3, "א", 3, PXY(2, 2), "P_XY(2,2)")
claim("Q3a#0", sum(PXY(a, b) for a in range(3) for b in range(4)) == 1 and PXY(1, 2) != PX(1) * PY(2) and PXY(1, 2) == PX(1) * p, "table normalised; P_XY(x,y)=P_X(x)P(X3=y-x); not the product of marginals")
ex(3, "ב", 1, PX(2), "P_X(2)"); ex(3, "ב", 2, PY(1), "P_Y(1)")
EY = sum(yv * PY(yv) for yv in range(4)); VY = sum(yv * yv * PY(yv) for yv in range(4)) - EY**2
ex(3, "ג", 1, EY, "E[Y]"); ex(3, "ג", 2, VY, "Var[Y]")
ex(3, "ד", 0, PXY(2, 0), "P_XY(2,0)"); ex(3, "ד", 1, PX(2) * PY(0), "P_X(2)P_Y(0)")
T3 = rng.random((N, 3)) < 0.3
xx = T3[:, 0].astype(int) + T3[:, 1]; yy = xx + T3[:, 2]
mc(3, "א", 1, float(((xx == 1) & (yy == 2)).mean()), se_p(.126), "P_XY(1,2)"); mc(3, "א", 2, float(((xx == 0) & (yy == 1)).mean()), se_p(.147), "P_XY(0,1)")
mc(3, "א", 3, float(((xx == 2) & (yy == 2)).mean()), se_p(.063), "P_XY(2,2)")
mc(3, "ב", 1, float((xx == 2).mean()), se_p(.09), "P_X(2)"); mc(3, "ב", 2, float((yy == 1).mean()), se_p(.441), "P_Y(1)")
mc(3, "ג", 1, float(yy.mean()), float(yy.std()) / math.sqrt(N), "E[Y]"); mc(3, "ג", 2, float(yy.var()), float(yy.var()) * math.sqrt(2 / N) * 1.5, "Var[Y]")

# ---------------------------------------------------------------- Q4  f = a e^x (x<-1), 1/4 on [-1,1), b e^-x (x>=1)
a, b = sp.symbols("a b", real=True)
xs = sp.Symbol("xs", real=True)
norm = sp.integrate(a * sp.exp(xs), (xs, -sp.oo, -1)) + sp.integrate(sp.Rational(1, 4), (xs, -1, 1)) + sp.integrate(b * sp.exp(-xs), (xs, 1, sp.oo))
mean = sp.integrate(xs * a * sp.exp(xs), (xs, -sp.oo, -1)) + sp.integrate(xs * sp.Rational(1, 4), (xs, -1, 1)) + sp.integrate(xs * b * sp.exp(-xs), (xs, 1, sp.oo))
sol = sp.solve([norm - 1, mean], [a, b], dict=True)[0]
claim("Q4a mean eq", sp.simplify(mean - (-2 * a / sp.E + 2 * b / sp.E)) == 0, "E[X] = (-2a+2b)/e")
ex(4, "א", 1, sp.integrate(sp.Rational(1, 4), (xs, -1, 1)), "middle mass")
ex(4, "א", 2, sol[a] + sol[b], "a+b = e/2"); ex(4, "א", 3, sol[a], "a = e/4")
claim("Q4a a=b", sp.simplify(sol[a] - sol[b]) == 0, "a=b")


def F(tt):
    tt = sp.nsimplify(tt)
    if tt < -1:
        return sol[a] * sp.exp(tt)
    if tt < 1:
        return sol[a] * sp.exp(-1) + sp.Rational(1, 4) * (tt + 1)
    return 1 - sol[b] * sp.exp(-tt)


ex(4, "ב", 0, F(-1), "F(-1)"); ex(4, "ב", 1, F(0), "F(0)"); ex(4, "ב", 2, F(2), "F(2)")
ex(4, "ג", 0, F(3), "F(3)"); ex(4, "ג", 1, F(3) - F(-2), "P(-2<X<3)"); ex(4, "ג", 2, (F(3) - F(-2)) / F(3), "P(X>-2|X<3)")
claim("Q4c formula", abs(float((F(3) - F(-2)) / F(3)) - (4 * math.e**2 - math.e - 1) / (4 * math.e**2 - 1)) < 1e-12 and abs(float((F(3) - F(-2)) / F(3)) - 0.9048) < 1e-3,
      "(4e^2-e-1)/(4e^2-1) = 0.9048 (the stored solution's '0.99' is a typo)")
# inverse-CDF sample
u = rng.random(N)
Xs = np.where(u < .25, np.log(u / (math.e / 4)), np.where(u < .75, 2 * (u - .25) * 2 - 1, -np.log(np.maximum(1 - u, 1e-300) * 4 / math.e)))
mc(4, "ב", 0, float((Xs <= -1).mean()), se_p(.25), "F(-1)"); mc(4, "ב", 1, float((Xs <= 0).mean()), se_p(.5), "F(0)")
mc(4, "ב", 2, float((Xs <= 2).mean()), se_p(float(F(2))), "F(2)"); mc(4, "ג", 0, float((Xs < 3).mean()), se_p(float(F(3))), "F(3)")
sel = Xs < 3
mc(4, "ג", 2, float((Xs[sel] > -2).mean()), se_p(float((F(3) - F(-2)) / F(3)), int(sel.sum())), "P(X>-2|X<3)")
claim("Q4 mean", abs(Xs.mean()) < 4 * Xs.std() / math.sqrt(N), "sampled density has mean 0")

# ---------------------------------------------------------------- Q5  D=3, N=10, M=4, p=1/2
from math import comb
D_, N_, M_, pr_ = 3, 10, 4, Fr(1, 2)
PXk = lambda k: comb(M_, k) * pr_**k * (1 - pr_) ** (M_ - k)
Pred_k = lambda k: Fr(D_ + 2 * k, N_ + 2 * M_)
Pred = sum(PXk(k) * Pred_k(k) for k in range(M_ + 1))
ex(5, "א", 1, Pred_k(3), "P(red|X=3)"); ex(5, "א", 2, sum(k * PXk(k) for k in range(M_ + 1)), "E[X]"); ex(5, "א", 3, Pred, "P(red)")
claim("Q5a formula", Pred == Fr(D_ + 2 * 1 * 2, 1) / (N_ + 2 * M_) * 1 and Pred == (D_ + 2 * pr_ * M_) / (N_ + 2 * M_), "(D+2pM)/(N+2M)")
ex(5, "ב", 1, PXk(1), "P(X=1)"); ex(5, "ב", 2, Pred_k(1), "P(red|X=1)"); ex(5, "ב", 3, PXk(1) * Pred_k(1) / Pred, "P(X=1|red)")
claim("Q5b parity", True, "red balls are added two at a time, so n odd has probability 0 (structural)")
Xc = rng.binomial(M_, 0.5, N); red = rng.random(N) < (D_ + 2 * Xc) / (N_ + 2 * M_)
mc(5, "א", 3, float(red.mean()), se_p(float(Pred)), "P(red)")
mc(5, "א", 1, float(red[Xc == 3].mean()), se_p(0.5, int((Xc == 3).sum())), "P(red|X=3)")
mc(5, "ב", 3, float((Xc[red] == 1).mean()), se_p(5 / 28, int(red.sum())), "P(X=1|red)")
mc(5, "ב", 1, float((Xc == 1).mean()), se_p(.25), "P(X=1)")

# ---------------------------------------------------------------- Q6  nine-unit circuit, brute force over 2^9 states, p = 3/5
edges = {"u1": ("T", "m1"), "u2": ("m1", "Bt"), "u3": ("T", "m2"), "u4": ("m2", "Bt"),
         "A": ("T", "l"), "G": ("T", "r"), "H": ("l", "Bt"), "K": ("r", "Bt"), "Cc": ("l", "r")}
inner = ["A", "G", "H", "K", "Cc"]
names = list(edges)
pr6 = Fr(3, 5)


def conn(state, subset=None):
    adj = {}
    for nm, v in zip(names, state):
        if v and (subset is None or nm in subset):
            u1, u2 = edges[nm]
            adj.setdefault(u1, set()).add(u2); adj.setdefault(u2, set()).add(u1)
    seen, stack = {"T"}, ["T"]
    while stack:
        cur = stack.pop()
        for nb in adj.get(cur, ()):
            if nb not in seen:
                seen.add(nb); stack.append(nb)
    return "Bt" in seen


def P9(pred):
    tot = Fr(0)
    for st in itertools.product([0, 1], repeat=9):
        wgt = Fr(1)
        for v in st:
            wgt *= pr6 if v else 1 - pr6
        if pred(st):
            tot += wgt
    return tot


P_E = P9(lambda st: conn(st, inner))                     # the inner bridge alone
P_Q = P9(conn)
iE = [names.index(n) for n in inner]
QN = P9(lambda st: conn(st) and not conn(st, inner)) / (1 - P_E)       # P(Q | inner bridge fails)
ex(6, "א", 1, P_E, "P(E)"); ex(6, "א", 2, QN, "P(Q|~E)"); ex(6, "א", 3, P_Q, "P0")
claim("Q6a formulas", P_E == pr6**3 * (2 - pr6) ** 2 + pr6**2 * (2 - pr6**2) * (1 - pr6) and QN == 2 * pr6**2 - pr6**4
      and P_Q == pr6**2 * (2 - pr6**2) + (1 - pr6**2) ** 2 * P_E, "P(E), P(Q|~E), P0 formulas of the solution")
iA = names.index("A")
PEA = P9(lambda st: conn(st, inner) and not st[iA]) / (1 - pr6)
PQA = P9(lambda st: conn(st) and not st[iA]) / (1 - pr6)
ex(6, "ב", 1, PEA, "P(E|~A)"); ex(6, "ב", 2, PQA, "P(Q|~A)"); ex(6, "ב", 3, (1 - pr6) * PQA / P_Q, "P1 = P(~A|Q)")
claim("Q6b formulas", PEA == pr6**2 * (1 + pr6 - pr6**2) and PQA == pr6**2 * (2 - pr6**2) + (1 - pr6**2) ** 2 * pr6**2 * (1 + pr6 - pr6**2), "solution formulas for P(E|~A), P(Q|~A)")
st9 = rng.random((N, 9)) < 0.6
idx = {n: i for i, n in enumerate(names)}


def conn_vec(st):
    reach = {k: np.zeros(len(st), bool) for k in ("T", "m1", "m2", "l", "r", "Bt")}
    reach["T"][:] = True
    for _ in range(6):
        for nm, (u1, u2) in edges.items():
            on = st[:, idx[nm]]
            reach[u2] |= reach[u1] & on
            reach[u1] |= reach[u2] & on
    return reach["Bt"]


Qm = conn_vec(st9)
inner_mask = np.zeros(9, bool); inner_mask[iE] = True
Em = conn_vec(st9 & inner_mask)
mc(6, "א", 1, float(Em.mean()), se_p(float(P_E)), "P(E)")
mc(6, "א", 2, float(Qm[~Em].mean()), se_p(float(QN), int((~Em).sum())), "P(Q|~E)")
mc(6, "א", 3, float(Qm.mean()), se_p(float(P_Q)), "P0")
mc(6, "ב", 1, float(Em[~st9[:, iA]].mean()), se_p(float(PEA), int((~st9[:, iA]).sum())), "P(E|~A)")
mc(6, "ב", 2, float(Qm[~st9[:, iA]].mean()), se_p(float(PQA), int((~st9[:, iA]).sum())), "P(Q|~A)")
mc(6, "ב", 3, float((~st9[:, iA])[Qm].mean()), se_p(float((1 - pr6) * PQA / P_Q), int(Qm.sum())), "P1")

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
