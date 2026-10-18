# -*- coding: utf-8 -*-
"""Step verification for 25A-A (probability). Run: PYTHONUTF8=1 py tools/verify/25A-A/steps_check.py

Reads tools/raw/25A-A.json (written by tools/gen/gen_25A-A.py) and, for every numeric step,
re-derives the expected value INDEPENDENTLY of the generator:
  EXACT : fractions / enumeration / sympy / exact half-plane clipping;
  MC    : Monte Carlo (>= 10^6 trials) agrees within 4 standard errors, where a simulation applies.
For choice steps with a checkable claim (distractors that must fail) the claim is asserted numerically.
Exit code 1 on any failure. Output is ASCII only.
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = json.loads((ROOT / "raw" / "25A-A.json").read_text(encoding="utf-8"))
BY = {(q["num"], q.get("part")): q for q in RAW["questions"]}
N = 2_000_000
rng = np.random.default_rng(20250217)
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


# ---------------------------------------------------------------- exact half-plane clipping (Fractions)
def clip(poly, a, b, c):
    """keep a*x + b*y >= c"""
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


RECT = [(Fr(0), Fr(0)), (Fr(1, 3), Fr(0)), (Fr(1, 3), Fr(2, 3)), (Fr(0), Fr(2, 3))]
half = Fr(1, 2)
Om = area(RECT)
A_gt = area(clip(RECT, Fr(1), Fr(-1), Fr(0)))                       # x1 >= x2
tri_poly = clip(clip(clip(RECT, Fr(1), Fr(1), half), Fr(-1), Fr(0), -half), Fr(0), Fr(-1), -half)
A_tri = area(tri_poly)
A_both = area(clip(tri_poly, Fr(1), Fr(-1), Fr(0)))
ex(1, "א", 1, Om, "|Omega|=2/9"); ex(1, "ב", 0, Om, "|Omega|"); ex(1, "ג", 0, Om, "|Omega|")
ex(1, "א", 2, A_gt, "area x2<x1 = 1/18"); ex(1, "א", 3, A_gt / Om, "P(X1>X2)")
ex(1, "ב", 2, A_tri, "area of triangle region = 1/18"); ex(1, "ב", 3, A_tri / Om, "P(triangle)")
ex(1, "ג", 1, A_gt / Om, "P(X1>X2)"); ex(1, "ג", 2, A_both, "area intersection = 1/144"); ex(1, "ג", 3, (A_both / Om) / (A_gt / Om), "P(tri|X1>X2)")
x1 = rng.random(N) / 3; x2 = rng.random(N) * 2 / 3
gt = x1 > x2; tri = (x1 + x2 >= .5) & (x1 <= .5) & (x2 <= .5)
mc(1, "א", 3, float(gt.mean()), se_p(.25), "P(X1>X2)")
mc(1, "ב", 3, float(tri.mean()), se_p(.25), "P(triangle)")
mc(1, "ג", 3, float((tri & gt).sum() / gt.sum()), math.sqrt(.125 * .875 / gt.sum()), "P(tri|X1>X2)")
mc(1, "ג", 1, float(gt.mean()), se_p(.25), "P(X1>X2) as conditioning prob")
mc(1, "ג", 2, float((tri & gt).mean()) * float(Om), se_p(1 / 32) * float(Om), "area intersection (as MC prob * |Omega|)")
claim("Q1b#1", (x1 <= .5).all() and (x2 > .5).any() and (tri != ((x1 + x2 >= .5) & (x2 <= .5))).sum() == 0 and ((x1 + x2 >= .5) != tri).any(),
      "X1<=1/2 always true; X2<=1/2 and X1+X2>=1/2 both cut")

# ---------------------------------------------------------------- Q2
Omega = range(100, 1000)
A2 = [n for n in Omega if n % 2 == 0]; A4 = [n for n in Omega if n % 4 == 0]; A8 = [n for n in Omega if n % 8 == 0]
ex(2, "א", 1, len(Omega), "|Omega|=900"); ex(2, "א", 2, len(A8), "|A8|=112"); ex(2, "א", 3, Fr(len(A8), len(Omega)), "P(A8)")
ex(2, "ב", 1, Fr(len(set(A2) & set(A4)), 900), "P(A2 n A4)"); ex(2, "ב", 2, Fr(len(A2), 900) * Fr(len(A4), 900), "P(A2)P(A4)")
ex(2, "ג", 0, Fr(len(set(A4) & set(A8)), 900), "P(A4 n A8)"); ex(2, "ג", 1, Fr(len(A4), 900) * Fr(len(A8), 900), "P(A4)P(A8)")
ex(2, "ד", 0, len(set(A2) & set(A4)), "|A2 n A4|"); ex(2, "ד", 1, len(A8), "|A8|")
claim("Q2d#2", 100 in A4 and 100 not in A8 and 104 in A8 and 104 in A4 and 102 not in A4 and 101 not in A2, "only 100 separates A8 from A2 n A4 among the options")
claim("Q2a#0", 900 % 8 != 0, "900 is not divisible by 8")
claim("Q2b/c", len(set(A2) & set(A4)) / 900 != len(A2) / 900 * len(A4) / 900 and len(A8) / 900 != 0.25 * len(A8) / 900, "dependent")

# ---------------------------------------------------------------- Q3  (sympy)
a, b, c, mu, x, t = sp.symbols("a b c mu x t", real=True)
norm = sp.integrate(a * sp.exp(x), (x, -sp.oo, 0)) + sp.integrate(b * x, (x, 0, 1))
mean = sp.integrate(x * a * sp.exp(x), (x, -sp.oo, 0)) + sp.integrate(x * b * x, (x, 0, 1))
sol = sp.solve([norm - 1, mean - mu], [a, b], dict=True)[0]
claim("Q3a#1", sp.integrate(1 / x, (x, 1, sp.oo)) == sp.oo, "int_1^oo dx/x diverges so c=0")
ex(3, "א", 1, 0, "c = 0 (forced by divergence, previous claim)"); ex(3, "א", 2, sol[a].subs(mu, 0), "a at mu=0"); ex(3, "א", 3, sol[b].subs(mu, 0), "b at mu=0")
ex(3, "ב", 0, sol[a].subs(mu, 1), "a at mu=1")
fa, fb = sol[a].subs(mu, 0), sol[b].subs(mu, 0)
F = lambda tt: (fa * sp.exp(tt) if tt < 0 else fa + fb * sp.integrate(x, (x, 0, tt)))
ex(3, "ג", 0, F(0), "F(0)"); ex(3, "ג", 1, F(sp.Rational(1, 2)), "F(1/2)"); ex(3, "ג", 2, F(-1), "F(-1)")
ex(3, "ד", 0, 1 - F(0), "P(X>0)"); ex(3, "ד", 1, F(1) - F(0), "P(0<X<1)"); ex(3, "ד", 2, (F(1) - F(0)) / (1 - F(0)), "P(X<1|X>0)")
# Monte Carlo of the mu = 0 density (inverse CDF) for F values
u = rng.random(N)
Xs = np.where(u < 0.4, np.log(u / 0.4), np.sqrt((u - 0.4) / 0.6))
mc(3, "ג", 0, float((Xs <= 0).mean()), se_p(.4), "F(0)"); mc(3, "ג", 1, float((Xs <= .5).mean()), se_p(.55), "F(1/2)")
mc(3, "ג", 2, float((Xs <= -1).mean()), se_p(.1471518), "F(-1)")
mc(3, "ד", 2, float(((Xs < 1) & (Xs > 0)).sum() / (Xs > 0).sum()), 1e-9, "P(X<1|X>0)")

# ---------------------------------------------------------------- Q4 circuits, brute force over 2^5 states, p = 3/5
p = Fr(3, 5)
def prob(pred):
    tot = Fr(0)
    for st in itertools.product([0, 1], repeat=5):
        A, B, C, D, E = st
        w = Fr(1)
        for v in st:
            w *= p if v else 1 - p
        if pred(A, B, C, D, E):
            tot += w
    return tot
q1 = lambda A, B, C, D, E: (A and B) or (C and D) or (A and E and D) or (C and E and B)       # bridge: A-B, C-D, E joins the middle nodes
q2 = lambda A, B, C, D, E: A and (B or C) and (D or E)
P1, P2 = prob(q1), prob(q2)
PJ = prob(lambda *s: q1(*s) and q2(*s))
PC = PJ / P2
PE1 = prob(lambda A, B, C, D, E: E and q1(A, B, C, D, E)) / p
PE0 = prob(lambda A, B, C, D, E: (not E) and q1(A, B, C, D, E)) / (1 - p)
ex(4, "א", 1, PE1, "P(Q1|E)"); ex(4, "א", 2, PE0, "P(Q1|~E)"); ex(4, "א", 3, P1, "P(Q1)")
ex(4, "ב", 1, prob(lambda A, B, C, D, E: B or C), "P(B or C)"); ex(4, "ב", 2, P2, "P(Q2)")
ex(4, "ג", 1, P2, "P(Q2)"); ex(4, "ג", 2, PJ, "P(Q1 and Q2)"); ex(4, "ג", 3, PC, "P(Q1|Q2)")
ex(4, "ד", 1, PC, "P(Q1|Q2)"); ex(4, "ד", 2, 1 - PC, "P(~Q1|Q2)")
claim("Q4c#0", PJ != P1 * P2 and abs(float(P1 * P2) - 0.279) < 0.001, "Q1,Q2 dependent: P(Q1)P(Q2) != P(Q1 n Q2)")
st = (rng.random((N, 5)) < 0.6)
A_, B_, C_, D_, E_ = st.T
Q1m = (A_ & B_) | (C_ & D_) | (A_ & E_ & D_) | (C_ & E_ & B_); Q2m = A_ & (B_ | C_) & (D_ | E_)
mc(4, "א", 3, float(Q1m.mean()), se_p(float(P1)), "P(Q1)"); mc(4, "א", 1, float(Q1m[E_].mean()), se_p(float(PE1), int(E_.sum())), "P(Q1|E)")
mc(4, "א", 2, float(Q1m[~E_].mean()), se_p(float(PE0), int((~E_).sum())), "P(Q1|~E)")
mc(4, "ב", 2, float(Q2m.mean()), se_p(float(P2)), "P(Q2)"); mc(4, "ב", 1, float((B_ | C_).mean()), se_p(.84), "P(B or C)")
mc(4, "ג", 2, float((Q1m & Q2m).mean()), se_p(float(PJ)), "P(Q1 n Q2)")
mc(4, "ג", 3, float(Q1m[Q2m].mean()), se_p(float(PC), int(Q2m.sum())), "P(Q1|Q2)")
mc(4, "ד", 2, float((~Q1m)[Q2m].mean()), se_p(float(1 - PC), int(Q2m.sum())), "P(~Q1|Q2)")
# the two solution formulas, symbolic check
ps = sp.symbols("p")
claim("Q4 formulas", sp.simplify(ps**3 * (3 - 2 * ps) - sp.Rational(1) * (ps**3 * (3 - 2 * ps))) == 0 and
      abs(float(sp.Rational(3, 5)**3 * (3 - 2 * sp.Rational(3, 5))) - float(PJ)) < 1e-12 and
      abs(float(P2) - float(sp.Rational(3, 5)**3 * (2 - sp.Rational(3, 5))**2)) < 1e-12, "p^3(3-2p) and p^3(2-p)^2 at p=0.6")

# ---------------------------------------------------------------- Q5  omega ~ Exp(2), T = pi, zeros of cos(omega t) counted explicitly
lam, T = 2, math.pi
w = rng.exponential(1 / lam, N)
cnt = np.zeros(N, dtype=int)
for k in range(1, 40):
    cnt += (math.pi * (k - .5) / w < T)
ex(5, "א", 2, 1 - sp.exp(-1), "P(N=0)"); ex(5, "א", 3, sp.exp(-1) - sp.exp(-3), "P(N=1)")
mc(5, "א", 2, float((cnt == 0).mean()), se_p(1 - math.exp(-1)), "P(N=0)"); mc(5, "א", 3, float((cnt == 1).mean()), se_p(math.exp(-1) - math.exp(-3)), "P(N=1)")
# interval claim: N=k iff pi(k-1/2)/T < omega < pi(k+1/2)/T
kk = rng.integers(1, 6, 200000); ww = rng.exponential(1 / lam, 200000)
nn = np.zeros(200000, dtype=int)
for k in range(1, 40):
    nn += (math.pi * (k - .5) / ww < T)
claim("Q5a#1", ((nn == kk) == ((math.pi * (kk - .5) / T < ww) & (ww < math.pi * (kk + .5) / T))).all(), "N_T=k <=> omega in (pi(k-1/2)/T, pi(k+1/2)/T)")
q = sp.exp(-2); Ssum = sp.summation(sp.Symbol("k", integer=True, positive=True) * q ** sp.Symbol("k", integer=True, positive=True), (sp.Symbol("k", integer=True, positive=True), 1, sp.oo))
pref = sp.exp(1) - sp.exp(-1)
Esum = sum(kv * (sp.exp(-2 * kv) * pref) for kv in range(1, 60))
ex(5, "ב", 1, q, "q=e^-2"); ex(5, "ב", 2, q / (1 - q) ** 2, "sum k q^k closed form")
ex(5, "ב", 3, 1 / pref, "E[N_T] closed form")
claim("Q5b series", abs(float(sum(kv * sp.exp(-2 * kv) for kv in range(1, 80))) - float(q / (1 - q) ** 2)) < 1e-12 and abs(float(Esum) - float(1 / pref)) < 1e-12,
      "series sum matches closed form and E[N]")
mc(5, "ב", 3, float(cnt.mean()), float(cnt.std()) / math.sqrt(N), "E[N_T]")
claim("Q5b#0", abs(T / math.pi * (1 / lam) - 0.5) < 1e-12 and abs(float(1 / pref) - 0.5) > 0.07 and abs(lam * T - 6.283) < 1e-3, "distractors give 0.5 / lam*T, not 0.4254")
# P(t_k < T) etc. with k = 2
tk = (math.pi * (2 - .5) / w) < T
ex(5, "ג", 1, sp.exp(-3), "P(t2<T)"); ex(5, "ג", 2, sp.exp(-4) * pref, "P(N=2)"); ex(5, "ג", 3, 1 - sp.exp(-2), "P(t3>T|t2<T)")
mc(5, "ג", 1, float(tk.mean()), se_p(math.exp(-3)), "P(t2<T)"); mc(5, "ג", 2, float((cnt == 2).mean()), se_p(math.exp(-4) * float(pref)), "P(N=2)")
sel = tk
mc(5, "ג", 3, float((cnt[sel] == 2).mean()), se_p(1 - math.exp(-2), int(sel.sum())), "P(t3>T|t2<T)")

# ---------------------------------------------------------------- Q6
from math import comb
ex(6, "א", 1, comb(5, 2) * Fr(3, 10) ** 2 * Fr(7, 10) ** 3, "Bin(5,0.3) P(2)")
ex(6, "ב", 1, Fr(1, 5) * Fr(1, 2), "pq"); ex(6, "ב", 2, Fr(9, 10) ** 4, "P(Y=0)"); ex(6, "ב", 3, 4 * Fr(1, 10) * Fr(9, 10) ** 3, "P(Y=1)")
m = rng.random((N, 5)) < 0.3
mc(6, "א", 1, float((m.sum(1) == 2).mean()), se_p(0.3087), "Bin(5,0.3) P(2)")
# thinning simulation: n=4 batteries, A w.p. 0.5, defective w.p. 0.2
Xs_ = rng.random((N, 4)) < 0.5; Zs_ = rng.random((N, 4)) < 0.2
Y_ = (Xs_ & Zs_).sum(1); X_ = Xs_.sum(1)
mc(6, "ב", 2, float((Y_ == 0).mean()), se_p(.6561), "P(Y=0)"); mc(6, "ב", 3, float((Y_ == 1).mean()), se_p(.2916), "P(Y=1)")
n_, pp, qq = 4, Fr(1, 5), Fr(1, 2)
ex(6, "ג", 1, n_ * pp * qq * (1 - qq), "Cov"); ex(6, "ג", 2, n_ * qq * (1 - qq), "Var X"); ex(6, "ג", 3, n_ * pp * qq * (1 - pp * qq), "Var Y")
ex(6, "ג", 4, sp.sqrt(sp.Rational(1, 5) * sp.Rational(1, 2) / (1 - sp.Rational(1, 10))), "rho closed form")
claim("Q6c empirical", abs(np.cov(X_, Y_)[0, 1] - 0.2) < 0.004 and abs(np.corrcoef(X_, Y_)[0, 1] - 1 / 3) < 0.002 and abs(X_.var() - 1) < 0.01 and abs(Y_.var() - .36) < 0.01,
      "empirical cov/var/rho match 0.2, 1, 0.36, 1/3")
ex(6, "ד", 0, sp.sqrt(sp.Rational(1, 2) / sp.Rational(1, 2)), "rho at p=1")

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
