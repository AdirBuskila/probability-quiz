# Refuter's own derivation for 24B-B (independent of the author's check.py). Exact (sympy/fractions) + Monte Carlo.
import itertools, json, sys
from fractions import Fraction as F
import numpy as np
import sympy as sp

rng = np.random.default_rng(12345)
M = 4_000_000
out = {}


def rep(k, exact, mc=None, note=""):
    try:
        fl = float(exact)
    except TypeError:
        fl = None
    out[k] = {"exact": str(exact), "float": fl, "mc": None if mc is None else float(mc)}
    print(f"{k:6s} exact={exact}  ({fl})  mc={mc if mc is None else round(float(mc), 5)} {note}")


# ---------- Q1 (L = 1)
x, y = sp.symbols("x y", positive=True)
# X1~U(0,1), X2~U(0,2); joint density 1/2 on [0,1]x[0,2]
X1 = rng.uniform(0, 1, M); X2 = rng.uniform(0, 2, M)
rep("1a", sp.Rational(1, 5), (X1 < .2).mean())
# P(X1+X2>1)=1-P(X1+X2<=1) = 1 - (1/2*1*1)/2
e = 1 - sp.integrate(sp.integrate(sp.Rational(1, 2), (y, 0, 1 - x)), (x, 0, 1))
rep("1b", e, (X1 + X2 > 1).mean())
e = sp.integrate(sp.integrate(sp.Rational(1, 2), (y, 0, x)), (x, 0, 1))
rep("1c", e, (X1 > X2).mean())
p = sp.symbols("p")
coin = rng.uniform(size=M)
for pv in (0.3, 0.7):
    Y = np.where(coin < pv, X1, X2)
    print("   p=", pv, "P(Y<1) mc", (Y < 1).mean(), "formula", pv + (1 - pv) / 2,
          "| P(.5<Y<1.5) mc", ((Y > .5) & (Y < 1.5)).mean())
rep("1d", p + (1 - p) / 2)
# P(.5<X1<1.5)=1/2 ; P(.5<X2<1.5)=1/2 -> 1/2 for any p
rep("1e", sp.Rational(1, 2))

# ---------- Q2 urn: D red, N-D black. exact via enumeration on small cases + symbolic
D, N = sp.symbols("D N", positive=True)
rep("2a", D / N)
# brute force check with specific (D,N)
def urn_probs(Dv, Nv):
    balls = [1] * Dv + [0] * (Nv - Dv)
    perms3 = list(itertools.permutations(range(Nv), 3))
    n = len(perms3)
    p2 = F(sum(balls[a[1]] for a in perms3), n)
    p3 = F(sum(balls[a[2]] for a in perms3), n)
    cond = F(sum(balls[a[1]] * balls[a[2]] for a in perms3), sum(balls[a[1]] for a in perms3))
    return p2, p3, cond
for Dv, Nv in [(3, 7), (4, 9), (2, 5)]:
    p2, p3, c = urn_probs(Dv, Nv)
    assert p2 == F(Dv, Nv) and p3 == F(Dv, Nv) and c == F(Dv - 1, Nv - 1), (Dv, Nv, p2, p3, c)
print("   urn brute force D/N, D/N, (D-1)/(N-1) confirmed on 3 cases")
rep("2b", D / N); rep("2c", D / N); rep("2d", (D - 1) / (N - 1))
# MC
Dv, Nv = 3, 7
perm = np.array([rng.permutation(Nv)[:3] for _ in range(300000)])
red = (perm < Dv)
print("   MC (D=3,N=7): P(2nd red)=", red[:, 1].mean(), "P(3rd red)=", red[:, 2].mean(),
      "P(3rd|2nd)=", (red[:, 1] & red[:, 2]).sum() / red[:, 1].sum(), " vs", 3 / 7, 3 / 7, 2 / 6)

# ---------- Q3 two digits from 1..9 without replacement (ordered)
pairs = list(itertools.permutations(range(1, 10), 2))
tot = len(pairs)
num = lambda t: 10 * t[0] + t[1]
rep("3a", F(sum(num(t) % 2 == 0 for t in pairs), tot))
rep("3b", F(sum(num(t) % 3 == 0 for t in pairs), tot))
rep("3c", F(sum(num(t) % 5 == 0 for t in pairs), tot))
odd_sum = [t for t in pairs if (t[0] + t[1]) % 2 == 1]
rep("3d", F(sum(num(t) % 2 == 0 for t in odd_sum), len(odd_sum)))
mc = np.array([rng.permutation(np.arange(1, 10))[:2] for _ in range(300000)])
n_ = 10 * mc[:, 0] + mc[:, 1]; s_ = mc.sum(1)
print("   MC 3a,b,c,d:", (n_ % 2 == 0).mean(), (n_ % 3 == 0).mean(), (n_ % 5 == 0).mean(),
      ((n_ % 2 == 0) & (s_ % 2 == 1)).sum() / (s_ % 2 == 1).sum())

# ---------- Q4: f = 1-|z|/a on [-a,a] (peak 1), then 1 on [a,b]
a, b, z, t = sp.symbols("a b z t", positive=True)
tri = sp.integrate(1 - z / a, (z, 0, a)) * 2
uni = (b - a) * 1
sol = sp.solve([sp.Eq(tri + uni, 1), sp.Eq(sp.integrate(z * 1, (z, a, b)) + 0, sp.Rational(4, 9))], [a, b], dict=True)
print("   Q4a solutions", sol)
av, bv = sp.Rational(1, 3), 1
assert any(s[a] == av and s[b] == bv for s in sol)
rep("4a_a", av); rep("4a_b", bv)
f = lambda zz: sp.Piecewise((0, zz < -av), (1 + zz / av, zz < 0), (1 - zz / av, zz < av), (0, zz < av), (1, zz <= bv), (0, True))
zz = sp.symbols("zz", real=True)
Fs = lambda tt: sp.integrate(sp.Piecewise((1 + zz / av, (zz >= -av) & (zz < 0)), (1 - zz / av, (zz >= 0) & (zz < av)),
                                          (1, (zz >= av) & (zz <= bv)), (0, True)), (zz, -av, tt))
print("   CDF pieces: F(-1/3)=0, F(0)=", Fs(0), " F(1/3)=", Fs(av), " F(1)=", Fs(1))
print("   F(t) on (-1/3,0]:", sp.simplify(Fs(sp.Symbol('t', real=True)) ) if False else "1/2*(1+3t)^2/3 =", sp.integrate(1 + zz / av, (zz, -av, t)).simplify())
print("   F(t) on (0,1/3]:", sp.simplify(sp.Rational(1, 6) + sp.integrate(1 - zz / av, (zz, 0, t))))
print("   F(t) on (1/3,1]:", sp.simplify(sp.Rational(1, 3) + t - av))
num_ = (sp.integrate(1 - 3 * zz, (zz, sp.Rational(1, 4), av)) + (sp.Rational(3, 4) - av))
den_ = (sp.integrate(1 - 3 * zz, (zz, 0, av)) * 2 + (sp.Rational(3, 4) - av))
rep("4c", num_ / den_)
# MC: sample from the mixture
u = rng.uniform(size=M)
Z = np.empty(M)
tri_mask = u < 1 / 3
k = tri_mask.sum()
Z[tri_mask] = rng.triangular(-1 / 3, 0, 1 / 3, size=k)
Z[~tri_mask] = rng.uniform(1 / 3, 1, size=M - k)
print("   MC E[Z] =", Z.mean(), "(4/9=", 4 / 9, ")  P(Z>1/4 | |Z|<3/4) =", ((Z > .25) & (np.abs(Z) < .75)).sum() / (np.abs(Z) < .75).sum())

# ---------- Q5 (q = 1/365 assumed; verified against page separately)
q = sp.Rational(1, 365)
Np_, pp = 8, sp.Rational(3, 5)
# thinning: Y ~ Bin(N, p*q). verify by full enumeration over X then Y|X
from math import comb
def pmfY(Nv, pv, qv, j):
    return sum(sp.Integer(comb(Nv, m)) * pv ** m * (1 - pv) ** (Nv - m) * comb(m, j) * qv ** j * (1 - qv) ** (m - j) for m in range(j, Nv + 1))
for j in range(0, Np_ + 1):
    assert sp.simplify(pmfY(Np_, pp, q, j) - comb(Np_, j) * (pp * q) ** j * (1 - pp * q) ** (Np_ - j)) == 0
print("   Y ~ Bin(N, p q) confirmed (enumeration N=8)")
# 5c: P(X=n | Y=k)
kk = 2
for nn in range(kk, Np_ + 1):
    lhs = (sp.Integer(comb(Np_, nn)) * pp ** nn * (1 - pp) ** (Np_ - nn) * comb(nn, kk) * q ** kk * (1 - q) ** (nn - kk)) / pmfY(Np_, pp, q, kk)
    r = p * (1 - q) / (1 - p * q)
    rhs = comb(Np_ - kk, nn - kk) * (pp * (1 - q) / (1 - pp * q)) ** (nn - kk) * (1 - pp * (1 - q) / (1 - pp * q)) ** (Np_ - nn)
    assert sp.simplify(lhs - rhs) == 0
print("   5c: n-k ~ Bin(N-k, p(1-q)/(1-pq)) confirmed")
# MC for Y~Bin
Xs = rng.binomial(Np_, 0.6, 2_000_000); Ys = rng.binomial(Xs, 1 / 365)
print("   MC E[Y]=", Ys.mean(), " vs N p q =", Np_ * 0.6 / 365)
# MC conditional with larger q to be measurable
qq = 0.3
Xs = rng.binomial(Np_, 0.6, 3_000_000); Ys = rng.binomial(Xs, qq)
sel = Ys == 2
emp = np.bincount(Xs[sel], minlength=Np_ + 1) / sel.sum()
th = [0] * 2 + [comb(Np_ - 2, nn - 2) * (0.6 * (1 - qq) / (1 - 0.6 * qq)) ** (nn - 2) * (1 - 0.6 * (1 - qq) / (1 - 0.6 * qq)) ** (Np_ - nn) for nn in range(2, Np_ + 1)]
print("   MC P(X=n|Y=2) q=.3:", np.round(emp, 4), "\n   theory:", np.round(th, 4))

# ---------- Q6 circuits: enumerate over component states, polynomial in p
A, B, C, Dd, E = sp.symbols("A B C D E")
comps = ["A", "B", "C", "D", "E"]
def poly(pred, cond=lambda s: True):
    tot = 0
    for st in itertools.product([0, 1], repeat=5):
        s = dict(zip(comps, st))
        if cond(s) and pred(s):
            k = sum(st)
            tot += p ** k * (1 - p) ** (5 - k)
    return sp.expand(tot)
def q1(s):  # bridge: nodes L,T,U,R ; A: L-T, B: T-R, C: L-U, D: U-R, E: T-U
    return (s["A"] and s["B"]) or (s["C"] and s["D"]) or (s["A"] and s["E"] and s["D"]) or (s["C"] and s["E"] and s["B"])
def q2(s):
    return (s["A"] or s["B"]) and (s["C"] or s["D"] or s["E"])
P1 = poly(q1); P2 = poly(q2); P12 = poly(lambda s: q1(s) and q2(s))
print("   Q1 poly", P1, "| Q2 poly", sp.factor(P2), sp.expand(P2))
rep("6a", P1); rep("6b", P2)
print("   Q1|Q2 =", sp.simplify(P12 / P2), " P12 poly", sp.factor(P12))
# note Q1 -> Q2? Q1 works implies Q2 works?  check
print("   Q1 subset of Q2?", all((not q1(dict(zip(comps, st)))) or q2(dict(zip(comps, st))) for st in itertools.product([0, 1], repeat=5)))
# MC at p=0.6
pv = 0.6
S = rng.uniform(size=(2_000_000, 5)) < pv
a_, b_, c_, d_, e_ = S.T
Q1 = (a_ & b_) | (c_ & d_) | (a_ & e_ & d_) | (c_ & e_ & b_)
Q2 = (a_ | b_) & (c_ | d_ | e_)
print("   MC p=.6: P(Q1)=", Q1.mean(), "exact", float(P1.subs(p, pv)), "| P(Q2)=", Q2.mean(), float(P2.subs(p, pv)),
      "| P(Q1|Q2)=", (Q1 & Q2).sum() / Q2.sum(), float((P12 / P2).subs(p, pv)))
json.dump(out, open(sys.argv[0].replace("refute_mine.py", "refute_mine_out.json"), "w"), indent=1)
