# Refuter's own derivation for 24B-C. Exact (sympy/fractions/enumeration) + Monte Carlo.
import itertools
from fractions import Fraction as F
import numpy as np
import sympy as sp

rng = np.random.default_rng(777)
M = 4_000_000
p = sp.symbols("p")


def show(k, exact, mc=None):
    print(f"{k:6s} exact={exact}  mc={mc if mc is None else round(float(mc), 5)}")


# ---------- Q1  X,Y ~ U(0,1) (L=1)
X = rng.uniform(size=M); Y = rng.uniform(size=M)
show("1a", sp.Rational(1, 5), (X < .2).mean())
show("1b", sp.Rational(2, 3), (Y > 1 / 3).mean())
show("1c", 1 - sp.Rational(1, 2) * sp.Rational(1, 2) ** 2, (X + Y <= 1.5).mean())
# Z = max(X,Y) (as DEFINED in printed formula) and Z = min (as the Hebrew word "short" suggests)
mx = np.maximum(X, Y); mn = np.minimum(X, Y)
show("1d max", sp.Rational(1, 9), (mx < 1 / 3).mean())
show("1d min", 1 - sp.Rational(2, 3) ** 2, (mn < 1 / 3).mean())
c = X > .25
show("1e max", sp.Rational(1, 6), ((mx < .5) & c).sum() / c.sum())
# min: P(min<1/2 and X>1/4)/(3/4) = [P(X>1/4) - P(X>1/2... )]
# P(min<1/2, X>1/4) = P(X>1/4) - P(X>=1/2? no: min>=1/2 & X>1/4) = 3/4 - 1/4 = 1/2 -> 2/3
show("1e min", sp.Rational(2, 3), ((mn < .5) & c).sum() / c.sum())

# ---------- Q2 digits 0..9
dig = list(range(10))
d3 = lambda v: v % 3 == 0
show("2a", F(sum(d3(v) for v in dig), 10))
pr2 = list(itertools.permutations(dig, 2))
show("2b", F(sum(d3(t[1]) for t in pr2), len(pr2)))
cond = [t for t in pr2 if d3(t[0])]
show("2c", F(sum(t[1] % 2 == 0 for t in cond), len(cond)))
pr3 = list(itertools.permutations(dig, 3))
show("2d", F(sum(d3(t[2]) for t in pr3), len(pr3)))
mc = np.array([rng.permutation(10)[:3] for _ in range(300000)])
print("   MC 2b,2c,2d:", (mc[:, 1] % 3 == 0).mean(),
      ((mc[:, 1] % 2 == 0) & (mc[:, 0] % 3 == 0)).sum() / (mc[:, 0] % 3 == 0).sum(), (mc[:, 2] % 3 == 0).mean())

# ---------- Q3 Bernoulli matrices [[0,-X],[Y,X+Y]]
Dd = {}; Tt = {}
joint = {}
for xv, yv in itertools.product([0, 1], repeat=2):
    pr = (p if xv else 1 - p) * (p if yv else 1 - p)
    det = 0 * (xv + yv) - (-xv) * yv
    tr = 0 + xv + yv
    Dd[det] = Dd.get(det, 0) + pr
    Tt[tr] = Tt.get(tr, 0) + pr
    joint[(det, tr)] = joint.get((det, tr), 0) + pr
print("   D1 pmf", {k: sp.factor(v) for k, v in Dd.items()}, "| T1 pmf", {k: sp.factor(sp.expand(v)) for k, v in Tt.items()})
ED = sum(k * v for k, v in Dd.items()); ET = sum(k * v for k, v in Tt.items())
EDT = sum(d * t * v for (d, t), v in joint.items())
cov1 = sp.factor(sp.expand(EDT - ED * ET))
print("   cov(D1,T1) =", cov1, " => cov[D,T] = n *", cov1)
Xb = (rng.uniform(size=(M, 4)) < 0.3)
n_ = 2  # not needed; use per-matrix and then check additivity with n=5
n = 5
xs = rng.uniform(size=(1_000_000, n)) < 0.3; ys = rng.uniform(size=(1_000_000, n)) < 0.3
Dn = (xs & ys).sum(1); Tn = xs.sum(1) + ys.sum(1)
print("   MC n=5,p=.3: cov =", np.cov(Dn, Tn)[0, 1], " formula 2 n p^2 (1-p) =", 2 * 5 * .09 * .7,
      "| D~Bin(5,.09): mean", Dn.mean(), 5 * .09, "var", Dn.var(), 5 * .09 * .91,
      "| T~Bin(10,.3): mean", Tn.mean(), "var", Tn.var(), 10 * .3 * .7)

# ---------- Q4 f=2/5 on (-a,a), linear 2/5 -> 0 on (a,b)
a, b, z = sp.symbols("a b z", positive=True)
area = sp.Rational(2, 5) * 2 * a + sp.Rational(1, 2) * (b - a) * sp.Rational(2, 5)
mean = sp.integrate(z * sp.Rational(2, 5) * (b - z) / (b - a), (z, a, b))
sols = sp.solve([sp.Eq(area, 1), sp.Eq(mean, sp.Rational(4, 15))], [a, b], dict=True)
print("   Q4a solutions:", sols)
for s in sols:
    print("     numeric", {k: float(v) for k, v in s.items()})
# pick a,b>0, b>a
good = [s for s in sols if s[b] > s[a] > 0]
print("   admissible:", good)
av, bv = good[0][a], good[0][b]
fz = lambda zz: sp.Piecewise((0, zz < -av), (sp.Rational(2, 5), zz < av), (sp.Rational(2, 5) * (bv - zz) / (bv - av), zz <= bv), (0, True))
zz = sp.symbols("zz", real=True)
t = sp.symbols("t", real=True)
mid = sp.simplify(sp.integrate(sp.Rational(2, 5), (zz, -av, t)))
tail = sp.simplify(sp.Rational(4, 5) * av + sp.integrate(sp.Rational(2, 5) * (bv - zz) / (bv - av), (zz, av, t)))
print("   F(t) on [-a,a]:", mid, " | on [a,b]:", tail, " | F(b) =", sp.simplify(tail.subs(t, bv)))
num_ = sp.integrate(sp.Rational(2, 5), (zz, sp.Rational(1, 2), av)) + sp.integrate(sp.Rational(2, 5) * (bv - zz) / (bv - av), (zz, av, sp.Rational(3, 2)))
num_ = sp.simplify(num_)
den_ = sp.integrate(sp.Rational(2, 5), (zz, -av, av)) + sp.integrate(sp.Rational(2, 5) * (bv - zz) / (bv - av), (zz, av, sp.Rational(3, 2)))
print("   4c exact:", sp.nsimplify(num_ / den_), " parts", num_, den_, float(num_ / den_))
# MC: inverse-transform via fine tabulation
grid = np.linspace(float(-av), float(bv), 200001)
dens = np.where(np.abs(grid) < float(av), .4, np.where(grid >= float(av), .4 * (float(bv) - grid) / (float(bv) - float(av)), 0))
cdf = np.cumsum(dens); cdf /= cdf[-1]
Zs = np.interp(rng.uniform(size=M), cdf, grid)
print("   MC: E[Z]=", Zs.mean(), "(4/15 =", 4 / 15, ")  P(Z>1/2 | |Z|<3/2)=", ((Zs > .5) & (np.abs(Zs) < 1.5)).sum() / (np.abs(Zs) < 1.5).sum())

# ---------- Q5 boxes
ns = sp.symbols("n1:6", positive=True)
Av = sp.Symbol("A")
print("   5a: E = mean(n_i);  5b: E = sum n_i^2 / sum n_i;   B-A = N*var / sum n_i >= 0")
for trial in range(3):
    arr = rng.choice(np.arange(1, 50), size=7, replace=False)
    A_ = arr.mean(); B_ = (arr ** 2).sum() / arr.sum()
    # MC for B
    pick = rng.choice(np.repeat(arr, arr), size=400000)
    print("   ex", arr, "A=", A_, "B=", B_, "MC B=", pick.mean(), "B-A", B_ - A_, " = var/mean:", arr.var() / A_)

# ---------- Q6 bridge: nodes L,T,U,R; A: L-T, B: L-U, C: T-R, D: U-R, E: T-U
comps = ["A", "B", "C", "D", "E"]
def poly(pred, cond=lambda s: True):
    tot = 0
    for st in itertools.product([0, 1], repeat=5):
        s = dict(zip(comps, st))
        if cond(s) and pred(s):
            k = sum(st)
            tot += p ** k * (1 - p) ** (5 - k)
    return sp.expand(tot)
def conn(s):
    # union-find over edges that work
    edges = {"A": ("L", "T"), "B": ("L", "U"), "C": ("T", "R"), "D": ("U", "R"), "E": ("T", "U")}
    par = {v: v for v in "LTUR"}
    def f(v):
        while par[v] != v: v = par[v]
        return v
    for k, (u, v) in edges.items():
        if s[k]: par[f(u)] = f(v)
    return f("L") == f("R")
Pw = poly(conn)
print("   6a poly:", Pw, "|", sp.factor(Pw))
PA = poly(lambda s: s["A"] and conn(s))
print("   6b: P(A and works) =", sp.factor(PA), "; P(A|works) =", sp.simplify(PA / Pw))
P1f = poly(lambda s: conn(s) and sum(s.values()) == 4)
P1 = poly(lambda s: sum(s.values()) == 4)
print("   6c: P(works | exactly one fails) =", sp.simplify(P1f / P1))
pv = 0.55
S = rng.uniform(size=(2_000_000, 5)) < pv
A_, B_, C_, D_, E_ = S.T
W = (A_ & C_) | (B_ & D_) | (A_ & E_ & D_) | (B_ & E_ & C_)
print("   MC p=.55: P(W)=", W.mean(), float(Pw.subs(p, pv)), "| P(A|W)=", (A_ & W).sum() / W.sum(), float((PA / Pw).subs(p, pv)))
k4 = S.sum(1) == 4
print("   MC P(W | exactly one fails) =", (W & k4).sum() / k4.sum())
