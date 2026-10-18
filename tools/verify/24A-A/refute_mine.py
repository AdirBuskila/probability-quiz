# Refuter's own derivation for 24A-A. Exact + Monte Carlo.
import itertools
from fractions import Fraction as F
from math import comb
import numpy as np
import sympy as sp

rng = np.random.default_rng(1357)
M = 4_000_000
p = sp.symbols("p")

# ---------- Q1 rectangle X~U(0,1), Y~U(0,2); S = XY, L = 2(X+Y)
x, y = sp.symbols("x y", positive=True)
X = rng.uniform(0, 1, M); Y = rng.uniform(0, 2, M)
S = X * Y; L = 2 * (X + Y)
# joint density 1/2.  P(XY<1): y<1/x ; for x<=1/2, 1/x>=2 -> all y.
e1 = sp.Rational(1, 2) * (sp.Rational(1, 2) * 2 + sp.integrate(1 / x, (x, sp.Rational(1, 2), 1)))
print("1a P(S<1) exact", sp.simplify(e1), float(e1), " MC", (S < 1).mean())
e2 = sp.Rational(1, 2) * sp.Rational(1, 2)
print("1b P(L<2) exact", e2, " MC", (L < 2).mean())
# P(S<1 and L>2) = P(S<1) - P(S<1 and X+Y<=1)= P(S<1) - P(X+Y<=1) since X+Y<=1 => XY<=1/4<1
e3 = (e1 - e2) / (1 - e2)
print("1c P(S<1|L>2) exact", sp.simplify(e3), float(e3), " MC", ((S < 1) & (L > 2)).sum() / (L > 2).sum())
ES = sp.Rational(1, 2) * 1
VS = sp.Rational(1, 3) * sp.Rational(4, 3) - ES ** 2
print("1d E[S]=", ES, " var[S]=", VS, " MC", S.mean(), S.var(), float(VS))
EL = 2 * (sp.Rational(1, 2) + 1)
VL = 4 * (sp.Rational(1, 12) + sp.Rational(4, 12))
print("1e E[L]=", EL, " var[L]=", VL, " MC", L.mean(), L.var(), float(VL))

# ---------- Q2 renewal: probability of ever hitting sum N with N-sided fair die
def hit(N):
    u = [F(1)]
    for n in range(1, N + 1):
        u.append(sum(u[n - k] for k in range(1, min(n, N) + 1)) / N)
    return u[N]
for N in (3, 4, 5, 6, 7, 10):
    print(f"2 P_{N} =", hit(N), float(hit(N)), " formula (1/N)(1+1/N)^(N-1) =", F(1, N) * (1 + F(1, N)) ** (N - 1))
    assert hit(N) == F(1, N) * (1 + F(1, N)) ** (N - 1)
def mc_hit(N, trials=400000):
    s = np.zeros(trials, dtype=np.int64); hitv = np.zeros(trials, bool); active = np.ones(trials, bool)
    while active.any():
        idx = np.where(active)[0]
        s[idx] += rng.integers(1, N + 1, len(idx))
        hitv[idx[s[idx] == N]] = True
        active[idx[s[idx] >= N]] = False
    return hitv.mean()
print("   MC P3,P4,P5:", mc_hit(3), mc_hit(4), mc_hit(5), " exact", 16 / 27, 125 / 256, 1296 / 3125)

# ---------- Q3 binomials
N1, N2, pv, n = 6, 9, sp.Rational(3, 10), 5
# P(X1=k | X=n) hypergeometric, E = n N1/(N1+N2)
for k in range(0, n + 1):
    lhs = sp.Integer(comb(N1, k)) * pv ** k * (1 - pv) ** (N1 - k) * comb(N2, n - k) * pv ** (n - k) * (1 - pv) ** (N2 - n + k) / (comb(N1 + N2, n) * pv ** n * (1 - pv) ** (N1 + N2 - n))
    assert sp.simplify(lhs - sp.Rational(comb(N1, k) * comb(N2, n - k), comb(N1 + N2, n))) == 0
print("3c hypergeometric C(N1,k)C(N2,n-k)/C(N1+N2,n) confirmed; sum of X1+X2 pmf = Bin(N1+N2,p) confirmed via convolution:")
for m in range(0, N1 + N2 + 1):
    cv = sum(sp.Integer(comb(N1, k)) * pv ** k * (1 - pv) ** (N1 - k) * comb(N2, m - k) * pv ** (m - k) * (1 - pv) ** (N2 - m + k) for k in range(0, m + 1) if m - k <= N2 and k <= N1)
    assert sp.simplify(cv - comb(N1 + N2, m) * pv ** m * (1 - pv) ** (N1 + N2 - m)) == 0
hyp_mean = sum(k * sp.Rational(comb(N1, k) * comb(N2, n - k), comb(N1 + N2, n)) for k in range(0, n + 1))
print("3d E[X1|X=n] =", hyp_mean, " vs n N1/(N1+N2) =", sp.Rational(n * N1, N1 + N2))
x1 = rng.binomial(N1, .3, M); x2 = rng.binomial(N2, .3, M)
sel = (x1 + x2) == n
print("   MC E[X1|X=5]", x1[sel].mean(), float(hyp_mean))

# ---------- Q4: f rises linearly 0->c on [0,a], constant c on [a,b]
a, b, c, xx = sp.symbols("a b c xx", positive=True)
A1 = a * c / 2; A2 = c * (b - a)
mean = sp.integrate(xx * c * xx / a, (xx, 0, a)) + sp.integrate(xx * c, (xx, a, b))
sols = sp.solve([sp.Eq(A1, A2), sp.Eq(A1 + A2, 1), sp.Eq(mean, sp.Rational(23, 24))], [a, b, c], dict=True)
print("4a solutions:", sols)
good = [s for s in sols if s[b] > s[a] > 0 and s[c] > 0]
av, bv, cv = good[0][a], good[0][b], good[0][c]
print("   a,b,c =", av, bv, cv)
t = sp.symbols("t", real=True)
F1 = sp.integrate(cv * xx / av, (xx, 0, t)); F2 = sp.Rational(1, 2) + cv * (t - av)
print("4b F(t): t<0: 0 ; 0<=t<=a:", F1, " ; a<=t<=b:", sp.expand(F2), "; F(b)=", F2.subs(t, bv), " F(a)=", F1.subs(t, av))
Em = sp.Rational(23, 24)
print("4c P(X>E[X]) =", 1 - F2.subs(t, Em) if Em > av else 1 - F1.subs(t, Em), " (E[X] > a?", Em > av, ")")
# MC
tab = np.linspace(0, float(bv), 400001)
dens = np.where(tab < float(av), float(cv) * tab / float(av), float(cv))
cdf = np.cumsum(dens); cdf /= cdf[-1]
Xs = np.interp(rng.uniform(size=M), cdf, tab)
print("   MC E[X]", Xs.mean(), "P(X<=a)", (Xs <= float(av)).mean(), " P(X>E)", (Xs > 23 / 24).mean())

# ---------- Q5 thinning (q = 1/365 assumed, to be checked against page)
q = sp.Rational(1, 365); Np = 7; pp = sp.Rational(2, 5)
def pmfY(j):
    return sum(sp.Integer(comb(Np, m)) * pp ** m * (1 - pp) ** (Np - m) * comb(m, j) * q ** j * (1 - q) ** (m - j) for m in range(j, Np + 1))
for j in range(Np + 1):
    assert sp.simplify(pmfY(j) - comb(Np, j) * (pp * q) ** j * (1 - pp * q) ** (Np - j)) == 0
print("5b Y~Bin(N,pq) confirmed (enumeration)")
kk = 2
for nn in range(kk, Np + 1):
    lhs = sp.Integer(comb(Np, nn)) * pp ** nn * (1 - pp) ** (Np - nn) * comb(nn, kk) * q ** kk * (1 - q) ** (nn - kk) / pmfY(kk)
    r = pp * (1 - q) / (1 - pp * q)
    assert sp.simplify(lhs - comb(Np - kk, nn - kk) * r ** (nn - kk) * (1 - r) ** (Np - nn)) == 0
print("5c  n-k ~ Bin(N-k, p(1-q)/(1-pq)) confirmed")

# ---------- Q6 bridge Q1 (A: L-T, B: T-R, C: L-U, D: U-R, E: T-U); Q2: E: L-T, B: T-R, C: L-U, D: U-R, A: T-U
comps = ["A", "B", "C", "D", "E"]
def connected(s, edges):
    par = {v: v for v in "LTUR"}
    def f(v):
        while par[v] != v: v = par[v]
        return v
    for k, (u, v) in edges.items():
        if s[k]: par[f(u)] = f(v)
    return f("L") == f("R")
E1 = {"A": ("L", "T"), "B": ("T", "R"), "C": ("L", "U"), "D": ("U", "R"), "E": ("T", "U")}
E2 = {"E": ("L", "T"), "B": ("T", "R"), "C": ("L", "U"), "D": ("U", "R"), "A": ("T", "U")}
def poly(pred):
    tot = 0
    for st in itertools.product([0, 1], repeat=5):
        s = dict(zip(comps, st))
        if pred(s):
            kx = sum(st); tot += p ** kx * (1 - p) ** (5 - kx)
    return sp.expand(tot)
q1 = lambda s: connected(s, E1); q2 = lambda s: connected(s, E2)
P1 = poly(q1); P2 = poly(q2); Pi = poly(lambda s: q1(s) and q2(s)); Pu = poly(lambda s: q1(s) or q2(s))
print("6a P(Q1) =", P1, " P(Q2) =", P2)
print("6b P(Q2|Q1) =", sp.factor(sp.simplify(Pi / P1)), " P(Q1&Q2)=", sp.factor(Pi))
print("6c P(Q1 or Q2) =", sp.expand(Pu), "=", sp.factor(Pu))
pv = 0.6
Sm = rng.uniform(size=(2_000_000, 5)) < pv
a_, b_, c_, d_, e_ = Sm.T
Q1 = (a_ & b_) | (c_ & d_) | (a_ & e_ & d_) | (c_ & e_ & b_)
# Q2: E: L-T, B: T-R, C: L-U, D: U-R, A: T-U
Q2 = (e_ & b_) | (c_ & d_) | (e_ & a_ & d_) | (c_ & a_ & b_)
print("   MC p=.6: P(Q1)", Q1.mean(), float(P1.subs(p, pv)), " P(Q2|Q1)", (Q1 & Q2).sum() / Q1.sum(), float((Pi / P1).subs(p, pv)),
      " P(Q1 or Q2)", (Q1 | Q2).mean(), float(Pu.subs(p, pv)))
