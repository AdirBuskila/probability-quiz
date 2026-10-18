# Refuter's own derivation for 24A-E. Exact + Monte Carlo.
import itertools, math
from fractions import Fraction as F
import numpy as np
import sympy as sp

rng = np.random.default_rng(2468)
M = 4_000_000
p = sp.symbols("p")

# ---------- Q1 grasshopper: position = XR - XL, XL~U(0,1), XR~U(0,2)
XL = rng.uniform(0, 1, M); XR = rng.uniform(0, 2, M)
pos = XR - XL
x, y = sp.symbols("x y")
print("1a  exact 0 (the set XR=XL has area 0); MC |pos|<1e-4:", (np.abs(pos) < 1e-4).mean(), " (~ 2e-4 * density 1/2*... small)")
# P(XR>XL) = 1 - P(XR<XL) ; P(XR<XL)=area{0<y<x<1}/2
pl = sp.integrate(sp.integrate(sp.Rational(1, 2), (y, 0, x)), (x, 0, 1))
print("1b  exact", 1 - pl, " MC", (pos > 0).mean())
print("1c  exact", pl, " MC", (pos < 0).mean())
pd_ = sp.integrate(sp.integrate(sp.Rational(1, 2), (y, x, x + sp.Rational(1, 3))), (x, 0, 1))
print("1d  exact", pd_, " MC", ((pos > 0) & (pos <= 1 / 3)).mean())

# ---------- Q2 y^2 + 2 X1 y + X2 = 0, fair die twice
pairs = list(itertools.product(range(1, 7), repeat=2))
disc = lambda t: t[0] ** 2 - t[1]
cx = [t for t in pairs if disc(t) < 0]
re_ = [t for t in pairs if disc(t) >= 0]
integ = [t for t in pairs if disc(t) >= 0 and int(round(math.sqrt(disc(t)))) ** 2 == disc(t)]
print("2a  complex:", F(len(cx), 36), cx)
print("2b  integer roots:", F(len(integ), 36), integ)
print("2c  integer | real:", F(len(integ), len(re_)), "(real count", len(re_), ")")
d3 = [t for t in pairs if t[0] == 3]
i3 = [t for t in d3 if disc(t) >= 0 and int(round(math.sqrt(disc(t)))) ** 2 == disc(t)]
print("2d  X1=3: integer-root cases", i3, "prob", F(len(i3), 6))
for t in i3:
    X1, X2 = t
    ys = sp.solve(sp.Symbol("y") ** 2 + 2 * X1 * sp.Symbol("y") + X2, sp.Symbol("y"))
    print("    roots for", t, ys)
# MC
d1 = rng.integers(1, 7, M); d2 = rng.integers(1, 7, M)
dc = d1 ** 2 - d2
sq = np.sqrt(np.maximum(dc, 0)).round() ** 2 == dc
print("   MC complex", (dc < 0).mean(), "integer", ((dc >= 0) & sq).mean(), "int|real", ((dc >= 0) & sq).sum() / (dc >= 0).sum(),
      "int | X1=3", ((dc >= 0) & sq & (d1 == 3)).sum() / (d1 == 3).sum())

# ---------- Q3 same Bernoulli matrices
joint = {}
for xv, yv in itertools.product([0, 1], repeat=2):
    pr = (p if xv else 1 - p) * (p if yv else 1 - p)
    det = 0 * (xv + yv) + xv * yv
    tr = xv + yv
    joint[(det, tr)] = joint.get((det, tr), 0) + pr
pD = {}; pT = {}
for (d, t), v in joint.items():
    pD[d] = pD.get(d, 0) + v; pT[t] = pT.get(t, 0) + v
print("3a D1 pmf:", {k: sp.factor(v) for k, v in pD.items()}, " 3b T1 pmf:", {k: sp.expand(v) for k, v in pT.items()})
cov1 = sp.factor(sp.expand(sum(d * t * v for (d, t), v in joint.items()) - sum(k * v for k, v in pD.items()) * sum(k * v for k, v in pT.items())))
print("3e cov(D1,T1) =", cov1)
n = 6; pv = 0.35
xs = rng.uniform(size=(1_000_000, n)) < pv; ys = rng.uniform(size=(1_000_000, n)) < pv
Dn = (xs & ys).sum(1); Tn = xs.sum(1) + ys.sum(1)
print("   MC cov =", np.cov(Dn, Tn)[0, 1], " 2np^2(1-p)=", 2 * n * pv ** 2 * (1 - pv),
      "| D mean/var", Dn.mean(), Dn.var(), n * pv ** 2, n * pv ** 2 * (1 - pv ** 2),
      "| T mean/var", Tn.mean(), Tn.var(), 2 * n * pv, 2 * n * pv * (1 - pv))
# check D ~ Bin(n,p^2) pmf
from math import comb
emp = np.bincount(Dn, minlength=n + 1) / len(Dn)
print("   D pmf emp ", np.round(emp, 4), "\n   Bin(n,p^2)", np.round([comb(n, k) * (pv ** 2) ** k * (1 - pv ** 2) ** (n - k) for k in range(n + 1)], 4))

# ---------- Q4 f = a(b^2 - x^2) on [-b,b]
a, b, xx, t = sp.symbols("a b xx t", positive=True)
norm = sp.integrate(a * (b ** 2 - xx ** 2), (xx, -b, b))
var = sp.integrate(xx ** 2 * a * (b ** 2 - xx ** 2), (xx, -b, b))
print("4a E[X] = ", sp.integrate(xx * a * (b ** 2 - xx ** 2), (xx, -b, b)), "(odd integrand)")
sol = sp.solve([sp.Eq(norm, 1), sp.Eq(var, sp.Rational(3, 15))], [a, b], dict=True)
print("4b solutions", sol)
av, bv = sol[0][a], sol[0][b]
tt = sp.symbols("tt", real=True)
Ft = sp.simplify(sp.integrate(av * (bv ** 2 - xx ** 2), (xx, -bv, tt)))
print("4c F(t) on [-b,b] =", sp.expand(Ft), " F(-1)=", Ft.subs(tt, -bv), "F(1)=", Ft.subs(tt, bv))
# P(X > a | |X|<b) with a=3/4,b=1
num_ = sp.integrate(av * (bv ** 2 - xx ** 2), (xx, av, bv))
den_ = sp.integrate(av * (bv ** 2 - xx ** 2), (xx, -bv, bv))
print("4d  P(X>a | |X|<b) =", num_ / den_, float(num_ / den_), " (threshold a =", av, ")")
# alt reading: threshold something else? print P(X>3/4), P(X>1/2)
print("    P(X>1/2)=", sp.integrate(av * (bv ** 2 - xx ** 2), (xx, sp.Rational(1, 2), bv)))
# MC via rejection: f(x) = 3/4 (1-x^2)
u = rng.uniform(-1, 1, M * 2); w = rng.uniform(0, .75, M * 2)
Xs = u[w < .75 * (1 - u ** 2)]
print("   MC var", Xs.var(), "(0.2)  P(X>.75)", (Xs > .75).mean(), " P(X>a|..)", (Xs > .75).sum() / (np.abs(Xs) < 1).sum())

# ---------- Q5 thinned Poisson
lam = sp.symbols("lambda", positive=True)
k = sp.symbols("k", integer=True, nonnegative=True)
j = sp.symbols("j", integer=True, nonnegative=True)
# P(X=k) = sum_{N>=k} e^{-lam} lam^N/N! C(N,k) p^k (1-p)^{N-k}
lv = sp.Rational(7, 2); pv_ = sp.Rational(2, 5)
for kk in range(0, 4):
    s = sp.summation(sp.exp(-lv) * lv ** j / sp.factorial(j) * sp.binomial(j, kk) * pv_ ** kk * (1 - pv_) ** (j - kk), (j, kk, sp.oo))
    th = sp.exp(-lv * pv_) * (lv * pv_) ** kk / sp.factorial(kk)
    print("5a k=", kk, sp.simplify(s - th) == 0 or float(abs(s - th)) < 1e-12)
# normalization & mean/var of Poisson(lam p)
q_ = sp.symbols("q", positive=True)
print("5b normalization sum e^{-q} q^k/k! =", sp.simplify(sp.summation(sp.exp(-q_) * q_ ** k / sp.factorial(k), (k, 0, sp.oo))))
EX = sp.simplify(sp.summation(k * sp.exp(-q_) * q_ ** k / sp.factorial(k), (k, 0, sp.oo)))
EX2 = sp.simplify(sp.summation(k ** 2 * sp.exp(-q_) * q_ ** k / sp.factorial(k), (k, 0, sp.oo)))
print("5c E =", EX, " var =", sp.simplify(EX2 - EX ** 2))
# 5d: P(N=Nn | X=n)
nn = 2
tot = sp.summation(sp.exp(-lv) * lv ** j / sp.factorial(j) * sp.binomial(j, nn) * pv_ ** nn * (1 - pv_) ** (j - nn), (j, nn, sp.oo))
for Nn in range(nn, nn + 5):
    lhs = sp.exp(-lv) * lv ** Nn / sp.factorial(Nn) * sp.binomial(Nn, nn) * pv_ ** nn * (1 - pv_) ** (Nn - nn) / tot
    rhs = sp.exp(-lv * (1 - pv_)) * (lv * (1 - pv_)) ** (Nn - nn) / sp.factorial(Nn - nn)
    assert sp.simplify(lhs - rhs) == 0
print("5d  N - n ~ Poisson(lam(1-p)) confirmed")
Ns = rng.poisson(2.0, M); Xw = rng.binomial(Ns, 0.4)
sel = Xw == 1
print("   MC: E[X]", Xw.mean(), "var", Xw.var(), " (0.8)  E[N - n | X=1] =", (Ns[sel] - 1).mean(), " vs lam(1-p)=1.2")

# ---------- Q6 circuits
comps = ["A", "B", "C", "D"]
def poly(pred):
    tot = 0
    for st in itertools.product([0, 1], repeat=4):
        s = dict(zip(comps, st))
        if pred(s):
            kx = sum(st); tot += p ** kx * (1 - p) ** (4 - kx)
    return sp.expand(tot)
Q1 = lambda s: s["D"] and ((s["A"] and s["B"]) or s["C"])
Q2 = lambda s: s["D"] and ((s["C"] and s["B"]) or s["A"])
P1 = poly(Q1); P2 = poly(Q2)
Pu = poly(lambda s: Q1(s) or Q2(s)); Pi = poly(lambda s: Q1(s) and Q2(s))
print("6a P(Q1)=", P1, "=", sp.factor(P1), " P(Q2)=", sp.factor(P2))
print("6b P(Q1 or Q2)=", sp.factor(Pu), "=", sp.expand(Pu))
print("6c P(Q2|Q1)=", sp.simplify(Pi / P1), " P(Q1 and Q2)=", sp.factor(Pi))
Pall = poly(lambda s: all(s.values()))
print("6d P(all|both)=", sp.simplify(Pall / Pi), " Pi=", sp.factor(Pi))
pv = 0.6
S = rng.uniform(size=(2_000_000, 4)) < pv
A_, B_, C_, D_ = S.T
q1 = D_ & ((A_ & B_) | C_); q2 = D_ & ((C_ & B_) | A_)
print("   MC p=.6: P(Q1)", q1.mean(), float(P1.subs(p, pv)), " P(Q1|Q2)", (q1 | q2).mean(), float(Pu.subs(p, pv)),
      " P(Q2|Q1)", (q1 & q2).sum() / q1.sum(), float((Pi / P1).subs(p, pv)),
      " P(all|both)", (A_ & B_ & C_ & D_).sum() / (q1 & q2).sum(), float((Pall / Pi).subs(p, pv)))
