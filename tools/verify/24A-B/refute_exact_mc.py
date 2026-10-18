# Refuter's own derivation for 24A-B (independent of author harness).
import numpy as np, sympy as sp, itertools
from fractions import Fraction as F
rng = np.random.default_rng(11)
N = 4_000_000

# Q1: point (X,Y) in unit square; triangles on sides: left S1 = X/2, bottom S2 = Y/2, right S3=(1-X)/2, top S4=(1-Y)/2
x, y = rng.random(N), rng.random(N)
S1, S2, S3, S4 = x/2, y/2, (1-x)/2, (1-y)/2
assert np.allclose(S1+S2+S3+S4, 1)
print("1a exact 1/4  mc", (S1 < 1/8).mean())
print("1b exact 7/8  mc", (S1+S2 < 3/4).mean())
print("1c exact 1/2  mc", (S1 < S2).mean())
print("1d exact 1/4  mc", ((S1 < S2) & (S2 < S3)).mean())
# exact via sympy: 1d region x<y<1-x
xs = sp.Symbol('x')
print("1d sympy", sp.integrate((1-xs)-xs, (xs, 0, sp.Rational(1, 2))))

# Q2 dice
rolls = list(itertools.product(range(1, 7), repeat=2))
s5 = [r for r in rolls if sum(r) == 5]
print("2a", F(len(s5), 36), " 2b", F(len([r for r in s5 if r[0] > 3]), len(s5)))
le18 = [r for r in rolls if r[0]*r[1] <= 18]
print("2c", F(len(le18), 36), " 2d", F(len([r for r in le18 if r[0] % 2 and r[1] % 2]), len(le18)))
d = rng.integers(1, 7, (N, 2))
sm = d.sum(1); pr = d[:, 0]*d[:, 1]
print("MC 2a", (sm == 5).mean(), " 2b", ((sm == 5) & (d[:, 0] > 3)).sum()/(sm == 5).sum(),
      " 2c", (pr <= 18).mean(), " 2d", ((pr <= 18) & (d[:, 0] % 2 == 1) & (d[:, 1] % 2 == 1)).sum()/(pr <= 18).sum())

# Q3: Q=[[XY,-X],[Y,X+Y-XY]]
p = sp.symbols('p', positive=True)
joint = {}
for X, Y in itertools.product([0, 1], repeat=2):
    Q = sp.Matrix([[X*Y, -X], [Y, X+Y-X*Y]])
    D, T = Q.det(), Q.trace()
    pr = (p if X else 1-p)*(p if Y else 1-p)
    joint[(D, T)] = joint.get((D, T), 0) + pr
print("joint", {k: sp.factor(v) for k, v in joint.items()})
PD = {}; PT = {}
for (dd, tt), v in joint.items():
    PD[dd] = PD.get(dd, 0)+v; PT[tt] = PT.get(tt, 0)+v
print("PD", {k: sp.factor(v) for k, v in PD.items()}, " PT", {k: sp.factor(v) for k, v in PT.items()})
E = lambda f: sum(f(a, b)*v for (a, b), v in joint.items())
print("cov", sp.factor(sp.simplify(E(lambda a, b: a*b)-E(lambda a, b: a)*E(lambda a, b: b))))
print("indep gap (D=0,T=2) :", sp.simplify(joint.get((0, 2), 0)-PD[0]*PT[2]))
pv = .3
X = rng.random(N) < pv; Y = rng.random(N) < pv
Xi, Yi = X.astype(int), Y.astype(int)
Dm = (Xi*Yi)*(Xi+Yi-Xi*Yi) + Xi*Yi   # det = XY(X+Y-XY) - (-X)(Y)
Tm = Xi*Yi + Xi+Yi-Xi*Yi
print("MC p=.3: P(D=2)", (Dm == 2).mean(), "exact .09; D values", set(Dm.tolist()), " cov", np.cov(Dm, Tm)[0, 1], "exact", 4*.09*.7)

# Q4: density c on [0,a], 1 on [a,b]
a, b, c = sp.symbols('a b c', positive=True)
sol = sp.solve([sp.Eq(c*a, 2*(b-a)), sp.Eq(c*a+(b-a), 1), sp.Eq(c*a**2/2+(b**2-a**2)/2, sp.Rational(5, 9))], [a, b, c], dict=True)
print("Q4 sol", sol)
s = sol[0]
av, bv, cv = float(s[a]), float(s[b]), float(s[c])
print("P(X<=5/9) exact", cv*5/9, " F(a)=", cv*av)
# MC: sample piecewise
u = rng.random(N)
Fa = cv*av
X4 = np.where(u < Fa, u/cv, av + (u-Fa))
print("MC E[X]", X4.mean(), " P(X<=5/9)", (X4 <= 5/9).mean(), " P(0..a)/P(a..b)", (X4 < av).mean()/((X4 >= av).mean()))

# Q5
n, r, q = sp.symbols('n r q', positive=True)
# Z | G=g ~ Bin(g, r), G~Geom(p) on {1,2,...}
pp = sp.symbols('pp', positive=True)
g = sp.Symbol('g', integer=True, positive=True)
qq = 1-pp; ss = 1-r
P0 = sp.simplify(sp.summation(pp*qq**(g-1)*ss**g, (g, 1, sp.oo)).rewrite(sp.Piecewise))
print("P(Z=0) closed (sympy)", sp.simplify(pp*ss/(1-qq*ss)))
def pk_closed(k, pv, rv):
    qv = 1-pv; sv = 1-rv
    return pv*rv**k*qv**(k-1)/(1-qv*sv)**(k+1)
def pk_brute(k, pv, rv, G=4000):
    from math import comb
    tot = 0.0
    for gg in range(max(k, 1), G):
        tot += pv*(1-pv)**(gg-1)*comb(gg, k)*rv**k*(1-rv)**(gg-k)
    return tot
for (pv, rv) in [(.3, .4), (.5, .5), (.2, .7)]:
    for k in (1, 2, 5):
        print("Q5 k", k, "p", pv, "r", rv, "closed", pk_closed(k, pv, rv), "brute", pk_brute(k, pv, rv))
# MC
pv, rv = .3, .4
G = rng.geometric(pv, 1_000_000); Zs = rng.binomial(G, rv)
print("MC P(Z=0)", (Zs == 0).mean(), "closed", pv*(1-rv)/(1-(1-pv)*(1-rv)), " P(Z=2)", (Zs == 2).mean(), pk_closed(2, pv, rv))
# Also: does the closed form hold with k>=1 only? and is P(Z=0) form consistent with k=0 formula pp*(...)
print("k=0 of the closed formula p*r^0*q^-1/(1-qs) =", pk_closed(0, pv, rv), " vs true", pv*(1-rv)/(1-(1-pv)*(1-rv)))

# Q6: Q1 bridge: A: L-m1, B: m1-R, C: L-m2, D: m2-R, E: m1-m2. Q2: (A||B) series (C||D)
P_ = sp.Symbol('p', positive=True)
tot1 = tot2 = both = 0
for bits in itertools.product([0, 1], repeat=5):
    A_, B_, C_, D_, E_ = bits
    pr = 1
    for v in bits: pr *= P_ if v else 1-P_
    # bridge connectivity via explicit graph search
    edges = []
    if A_: edges.append(('L', 'm1'))
    if C_: edges.append(('L', 'm2'))
    if B_: edges.append(('m1', 'R'))
    if D_: edges.append(('m2', 'R'))
    if E_: edges.append(('m1', 'm2'))
    seen = {'L'}; ch = True
    while ch:
        ch = False
        for u_, v_ in edges:
            if (u_ in seen) != (v_ in seen):
                seen |= {u_, v_}; ch = True
    s1 = 'R' in seen
    s2 = (A_ or B_) and (C_ or D_)
    if s1: tot1 += pr
    if s2: tot2 += pr
    if s1 and s2: both += pr
tot1, tot2, both = map(sp.expand, (tot1, tot2, both))
print("Q6a", sp.factor(tot1), "=", tot1)
print("Q6b", sp.factor(tot2), "=", tot2)
print("Q6c", sp.factor(sp.simplify(both/tot2)), " (both == tot1?)", sp.simplify(both-tot1) == 0)
pv = .6
A = rng.random(N) < pv; B = rng.random(N) < pv; C = rng.random(N) < pv; Dd = rng.random(N) < pv; Ee = rng.random(N) < pv
bridge = (A & B) | (C & Dd) | (A & Ee & Dd) | (C & Ee & B)
two = (A | B) & (C | Dd)
print("MC p=.6 Q1", bridge.mean(), float(tot1.subs(P_, pv)), " Q2", two.mean(), float(tot2.subs(P_, pv)), " Q1|Q2", (bridge & two).sum()/two.sum(), float((both/tot2).subs(P_, pv)))
