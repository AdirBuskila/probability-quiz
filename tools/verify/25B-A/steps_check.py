# -*- coding: utf-8 -*-
"""Step verification for 25B-A (probability). Run: PYTHONUTF8=1 py tools/verify/25B-A/steps_check.py

Reads tools/raw/25B-A.json (written by tools/gen/gen_25B-A.py) and, for every numeric step,
re-derives the expected value INDEPENDENTLY of the generator:
  EXACT : fractions / enumeration / sympy;
  MC    : Monte Carlo (>= 10^6 trials) agrees within 4 standard errors, where a simulation applies.
Choice steps with a checkable claim (distractors that must fail) are asserted numerically.
Exit code 1 on any failure. Output is ASCII only.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = json.loads((ROOT / "raw" / "25B-A.json").read_text(encoding="utf-8"))
BY = {(q["num"], q.get("part")): q for q in RAW["questions"]}
N = 2_000_000
rng = np.random.default_rng(20250715)
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


# ---------------------------------------------------------------- Q1
ell = sp.symbols("ell", positive=True)
ex(1, "א", 0, sp.solve(sp.Eq(ell ** 2 / 2, sp.Rational(1, 2)), ell)[0], "leg length from area 1/2")
x, y = sp.symbols("x y", positive=True)
X = rng.random(N); Y = rng.random(N)
ex(1, "ב", 1, sp.integrate(1, (x, 0, 1), (y, 0, 1)), "|Omega|=1")
ex(1, "ב", 3, sp.pi / 4, "P(L<1)")
mc(1, "ב", 3, float((X**2 + Y**2 < 1).mean()), se_p(math.pi / 4), "P(L<1)")
quarter = sp.integrate(sp.sqrt(1 - x**2), (x, 0, 1))
claim("Q1b exact", sp.simplify(quarter - sp.pi / 4) == 0, "area of quarter disc = pi/4 (integral)")
ex(1, "ג", 0, 1, "|Omega|")
ex(1, "ג", 1, sp.solve(sp.Eq(1 / (2 * x), 1), x)[0], "hyperbola meets y=1 at x=1/2")
curve = sp.integrate(1 / (2 * x), (x, sp.Rational(1, 2), 1))
ex(1, "ג", 2, curve, "int_{1/2}^1 dx/(2x)")
ex(1, "ג", 3, sp.Rational(1, 2) + curve, "P(S<1/4)")
mc(1, "ג", 3, float((X * Y / 2 < .25).mean()), se_p(0.8465736), "P(S<1/4)")
ex(1, "ד", 0, 1, "|Omega|")
ex(1, "ד", 1, sp.Rational(1, 2) + curve, "P(S<1/4)")
sel = X * Y < .5
ex(1, "ד", 3, (sp.pi / 4) / (sp.Rational(1, 2) + curve), "P(L<1 | S<1/4)")
mc(1, "ד", 3, float(((X**2 + Y**2 < 1) & sel).sum() / sel.sum()), math.sqrt(.93 * .07 / sel.sum()), "P(L<1|S<1/4)")
claim("Q1d#2", bool((~((X**2 + Y**2 < 1) & ~sel)).all()) and not bool(((X**2 + Y**2 < 1) & (X * Y >= .5)).any()), "x^2+y^2<1 implies xy<1/2 on 2e6 samples")
EX_, EX2 = sp.integrate(x, (x, 0, 1)), sp.integrate(x**2, (x, 0, 1))
ex(1, "ה", 1, EX_**2 / 2, "E[S]"); ex(1, "ה", 2, EX2, "E[X^2]")
VarXY = EX2**2 - (EX_**2) ** 2
ex(1, "ה", 3, VarXY, "Var[XY]"); ex(1, "ה", 4, VarXY / 4, "Var[S]")
Sm = X * Y / 2
mc(1, "ה", 1, float(Sm.mean()), float(Sm.std()) / math.sqrt(N), "E[S]")
mc(1, "ה", 4, float(Sm.var()), float(Sm.var()) * math.sqrt(2 / N) * 1.5, "Var[S]")
claim("Q1e#0", abs(float(EX_ + EX_) - 1) < 1e-12 and abs(float(EX_ * EX_) - 0.25) < 1e-12, "E[X]+E[Y]=1 != E[XY]=1/4")

# ---------------------------------------------------------------- Q2: p=3/5, q=7/10, s=4/5; independent derivation by solving the linear system
PA, PB, PAB = sp.symbols("PA PB PAB")
sol = sp.solve([sp.Eq(PAB, sp.Rational(3, 5) * PB), sp.Eq(PA + PB - PAB, sp.Rational(4, 5)), sp.Eq(1 - sp.Rational(4, 5), sp.Rational(7, 10) * (1 - PB))], [PA, PB, PAB], dict=True)[0]
ex(2, "א", 1, sol[PB], "P(B)"); ex(2, "א", 2, sol[PA], "P(A)")
ex(2, "ב", 1, 1 - sol[PB], "P(not B) = 2/7"); ex(2, "ב", 2, sol[PB], "P(B)")
ex(2, "ג", 1, sol[PB], "P(B)"); ex(2, "ג", 2, sol[PAB], "P(A n B)")
ex(2, "ד", 0, 1 - sp.Rational(1, 5) / sp.Rational(1, 10), "P(B) at q=0.1, s=0.8")
ex(2, "ה", 1, 1 - sp.Rational(3, 10), "p = 1-q at q=0.3")
# check the joint table reproduces the three givens (Monte Carlo of the model)
pa, pb, pab = (float(sol[v]) for v in (PA, PB, PAB))
u = rng.random(N)
Am = u < pab + (pa - pab); Bm = np.where(Am, u < pab, (u >= pa) & (u < pa + pb - pab))
mc(2, "א", 2, float(Am.mean()), se_p(pa), "P(A)")
mc(2, "ב", 2, float(Bm.mean()), se_p(pb), "P(B)"); mc(2, "ג", 2, float((Am & Bm).mean()), se_p(pab), "P(A n B)")
claim("Q2 givens", abs(float(Am[Bm].mean()) - 0.6) < 0.002 and abs(float((~Am)[~Bm].mean()) - 0.7) < 0.002 and abs(float((Am | Bm).mean()) - 0.8) < 0.002,
      "model reproduces P(A/B)=0.6, P(~A/~B)=0.7, P(A u B)=0.8")
claim("Q2 independence", abs(0.7 - (1 - 0.3)) < 1e-12, "independent A,B with P(~A)=q=0.3 has p=P(A/B)=P(A)=0.7")

# ---------------------------------------------------------------- Q3: 3 bridges with (1,2,3) gates, p = 4/5, exact enumeration over 6 gates
p = Fr(4, 5)
gates = [0, 1, 1, 2, 2, 2]


def pr(pred):
    tot = Fr(0)
    for st in itertools.product([0, 1], repeat=6):
        w = Fr(1)
        for v in st:
            w *= p if v else 1 - p
        if pred(st):
            tot += w
    return tot


def bridge_open(st, j):
    return all(st[i] for i in range(6) if gates[i] == j)


PQ = pr(lambda st: any(bridge_open(st, j) for j in range(3)))
PA2 = pr(lambda st: bridge_open(st, 1))
PA2Q = pr(lambda st: bridge_open(st, 1) and any(bridge_open(st, j) for j in range(3))) / PQ
ex(3, "א", 1, PA2, "P(A2)"); ex(3, "א", 2, 1 - PQ, "P(all blocked)"); ex(3, "א", 3, PQ, "P(Q)")
ex(3, "ב", 1, PA2, "P(A2)"); ex(3, "ב", 2, PA2Q, "P(A2|Q)"); ex(3, "ג", 1, 1 - PA2Q, "P(not A2|Q)")
st = rng.random((N, 6)) < 0.8
opn = [st[:, [i for i in range(6) if gates[i] == j]].all(1) for j in range(3)]
Qm = opn[0] | opn[1] | opn[2]
mc(3, "א", 3, float(Qm.mean()), se_p(float(PQ)), "P(Q)")
mc(3, "ב", 2, float(opn[1][Qm].mean()), se_p(float(PA2Q), int(Qm.sum())), "P(A2|Q)")
mc(3, "ג", 1, float((~opn[1])[Qm].mean()), se_p(float(1 - PA2Q), int(Qm.sum())), "P(not A2|Q)")
claim("Q3a#0", abs(float(sum([p, p**2, p**3])) - float(PQ)) > 0.5 and abs(float(p * p**2 * p**3) - float(PQ)) > 0.5, "sum and product distractors are far from P(Q)")
claim("Q3b#0", pr(lambda st: bridge_open(st, 1) and any(bridge_open(st, j) for j in range(3))) == PA2, "A2 subset of Q so P(Q|A2)=1")

# ---------------------------------------------------------------- Q4: a(x+1) on [-1,0), b on [0,1)
a, b, mu, t = sp.symbols("a b mu t", real=True)
xs = sp.Symbol("xs", real=True)
norm = sp.integrate(a * (xs + 1), (xs, -1, 0)) + sp.integrate(b, (xs, 0, 1))
mean = sp.integrate(xs * a * (xs + 1), (xs, -1, 0)) + sp.integrate(xs * b, (xs, 0, 1))
solq = sp.solve([norm - 1, mean - mu], [a, b], dict=True)[0]
a0, b0 = solq[a].subs(mu, 0), solq[b].subs(mu, 0)
ex(4, "א", 2, a0, "a at mu=0"); ex(4, "א", 3, b0, "b at mu=0")
claim("Q4a general", sp.simplify(solq[a] - sp.Rational(6, 5) * (1 - 2 * mu)) == 0 and sp.simplify(solq[b] - sp.Rational(2, 5) * (1 + 3 * mu)) == 0, "a=6/5(1-2mu), b=2/5(1+3mu)")
claim("Q4a#1", sp.integrate(1 / xs**3, (xs, 1, sp.oo)) == sp.Rational(1, 2) and sp.integrate(xs**2 * (1 / xs**3), (xs, 1, sp.oo)) == sp.oo,
      "c/x^3 integrates (normalisation/mean fine) but x^2*c/x^3 = c/x diverges: only the variance forces c=0")
ex(4, "ב", 1, sp.solve(sp.Eq(solq[a], 0), mu)[0], "mu max (a=0)")
ex(4, "ב", 2, sp.solve(sp.Eq(solq[b], 0), mu)[0], "mu min (b=0)")
Fq = lambda tt: sp.integrate((a0 * (xs + 1)), (xs, -1, tt)) if tt < 0 else sp.integrate(a0 * (xs + 1), (xs, -1, 0)) + sp.integrate(b0, (xs, 0, tt))
ex(4, "ג", 1, Fq(sp.Rational(-1, 2)), "F(-1/2)"); ex(4, "ג", 2, Fq(0), "F(0)"); ex(4, "ג", 3, Fq(sp.Rational(1, 2)), "F(1/2)")
ex(4, "ד", 0, 1 - Fq(sp.Rational(-1, 2)), "P(X>-1/2)"); ex(4, "ד", 1, Fq(1) - Fq(sp.Rational(-1, 2)), "P(-1/2<X<1)")
ex(4, "ד", 2, (Fq(1) - Fq(sp.Rational(-1, 2))) / (1 - Fq(sp.Rational(-1, 2))), "P(X<1|X>-1/2)")
# sample from the mu = 0 density (inverse CDF) and check the cdf values
u = rng.random(N)
Xs = np.where(u < 0.6, -1 + np.sqrt(u / 0.6), (u - 0.6) / 0.4)
mc(4, "ג", 1, float((Xs <= -.5).mean()), se_p(.15), "F(-1/2)"); mc(4, "ג", 2, float((Xs <= 0).mean()), se_p(.6), "F(0)"); mc(4, "ג", 3, float((Xs <= .5).mean()), se_p(.8), "F(1/2)")
mc(4, "ד", 0, float((Xs > -.5).mean()), se_p(.85), "P(X>-1/2)")
claim("Q4 mean 0", abs(Xs.mean()) < 4 * Xs.std() / math.sqrt(N), "sampled density has mean 0")

# ---------------------------------------------------------------- Q5: p = 3/5; Q0 = A and (B or C); random arrangement (R = 1..6)
pc = Fr(3, 5)


def PRB(pred):
    tot = Fr(0)
    for A, B, C in itertools.product([0, 1], repeat=3):
        w = Fr(1)
        for v in (A, B, C):
            w *= pc if v else 1 - pc
        if pred(A, B, C):
            tot += w
    return tot


Q0 = lambda A, B, C: A and (B or C)
# arrangement as a permutation (first, second, third) of the units: Q' = first and (second or third)
perms = list(itertools.permutations(range(3)))


def Qp(units, perm):
    f, s_, t_ = perm
    return units[f] and (units[s_] or units[t_])


P0 = PRB(Q0)
PJ = sum(PRB(lambda A, B, C, pm=pm: Q0(A, B, C) and Qp((A, B, C), pm)) for pm in perms) / 6
PQp = sum(PRB(lambda A, B, C, pm=pm: Qp((A, B, C), pm)) for pm in perms) / 6
ex(5, "א", 1, PRB(lambda A, B, C: B or C), "P(B or C)"); ex(5, "א", 2, P0, "P(Q0)")
ex(5, "ב", 1, PQp, "P(Q')")
ex(5, "ג", 1, PRB(lambda A, B, C: Q0(A, B, C) and Qp((A, B, C), (0, 1, 2))), "P(Q0 n Q' | Q'=Q0)")
ex(5, "ג", 2, PRB(lambda A, B, C: Q0(A, B, C) and Qp((A, B, C), (1, 0, 2))), "P(Q0 n Q' | Q'=B(A or C))")
ex(5, "ג", 3, PJ, "P(Q0 n Q')")
ex(5, "ד", 0, P0, "P(Q0)"); ex(5, "ד", 1, PJ, "P(Q0 n Q')"); ex(5, "ד", 2, PJ / P0, "P(Q'|Q0)")
ex(5, "ה", 1, 1 - P0, "P(not Q0)"); ex(5, "ה", 2, PQp - PJ, "P(Q' n not Q0)"); ex(5, "ה", 3, (PQp - PJ) / (1 - P0), "P(Q'|not Q0)")
claim("Q5 independence trap", abs(float(P0 * PQp) - float(PJ)) > 0.1, "P(Q0)P(Q') != P(Q0 n Q')")
# MC with a random permutation
U = rng.random((N, 3)) < 0.6
perm_idx = rng.integers(0, 6, N)
P_arr = np.array(perms)
f_, s2, t2 = (P_arr[perm_idx, i] for i in range(3))
ar = np.arange(N)
Q0m = U[:, 0] & (U[:, 1] | U[:, 2])
Qpm = U[ar, f_] & (U[ar, s2] | U[ar, t2])
mc(5, "א", 2, float(Q0m.mean()), se_p(float(P0)), "P(Q0)"); mc(5, "ב", 1, float(Qpm.mean()), se_p(float(PQp)), "P(Q')")
mc(5, "ג", 3, float((Q0m & Qpm).mean()), se_p(float(PJ)), "P(Q0 n Q')")
mc(5, "ד", 2, float(Qpm[Q0m].mean()), se_p(float(PJ / P0), int(Q0m.sum())), "P(Q'|Q0)")
mc(5, "ה", 3, float(Qpm[~Q0m].mean()), se_p(float((PQp - PJ) / (1 - P0)), int((~Q0m).sum())), "P(Q'|not Q0)")
mc(5, "ה", 2, float((Qpm & ~Q0m).mean()), se_p(float(PQp - PJ)), "P(Q' n not Q0)")
claim("Q5 formulas", sp.simplify(sp.Rational(3, 5)**2 * (4 - sp.Rational(3, 5)) / 3 - sp.Rational(PJ.numerator, PJ.denominator)) == 0, "p^2(4-p)/3 at p=0.6")

# ---------------------------------------------------------------- Q6
from math import comb, exp, factorial
ex(6, "א", 1, comb(5, 2) * Fr(1, 5) ** 2 * Fr(4, 5) ** 3, "Bin(5,0.2) P(2)")
mc(6, "א", 1, float(((rng.random((N, 5)) < 0.2).sum(1) == 2).mean()), se_p(0.2048), "Bin(5,0.2) P(2)")
# Poisson thinning: X ~ Poisson(2), each counted w.p. 0.5
Xp = rng.poisson(2, N); Yp = rng.binomial(Xp, 0.5)
ex(6, "ב", 2, sp.exp(-1), "P(Y=0)"); ex(6, "ב", 3, sp.exp(-1) / 2, "P(Y=2)")
mc(6, "ב", 2, float((Yp == 0).mean()), se_p(math.exp(-1)), "P(Y=0)"); mc(6, "ב", 3, float((Yp == 2).mean()), se_p(math.exp(-1) / 2), "P(Y=2)")
# exact thinning via the series from the hint (finite truncation)
lam, pp = sp.Integer(2), sp.Rational(1, 2)
k = 2
series = sum(sp.binomial(j, k) * pp**k * (1 - pp) ** (j - k) * sp.exp(-lam) * lam**j / sp.factorial(j) for j in range(k, 80))
claim("Q6b series", abs(float(series) - math.exp(-1) / 2) < 1e-12, "hint series gives Poisson(lambda p)")
sel = Yp == 1
ex(6, "ג", 1, sp.exp(-1), "P(X=1|Y=1)"); ex(6, "ג", 2, sp.exp(-1) / 2, "P(X=3|Y=1)")
mc(6, "ג", 1, float((Xp[sel] == 1).mean()), se_p(math.exp(-1), int(sel.sum())), "P(X=1|Y=1)")
mc(6, "ג", 2, float((Xp[sel] == 3).mean()), se_p(math.exp(-1) / 2, int(sel.sum())), "P(X=3|Y=1)")

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
