# Refuter's own derivation for 24B-A (independent of author harness).
import numpy as np, sympy as sp, itertools
from fractions import Fraction as F
rng = np.random.default_rng(7)
N = 4_000_000
out = {}
def show(name, exact, mc):
    print(f"{name:10s} exact={exact!s:28s} mc={mc:.5f}")

# Q1 (L=1)
x, y = rng.random(N), rng.random(N)
show("1a", F(1, 3), (x < 1/3).mean())
show("1b", F(3, 4), (y > 1/4).mean())
show("1c", F(7, 9), (x + y <= 4/3).mean())
z = np.minimum(x, y)
show("1d", F(5, 9), (z < 1/3).mean())
m = x > 1/4
show("1e", F(2, 3), ((z < .5) & m).sum() / m.sum())

# Q2 : P(k-th = 3) over permutations of 10 digits
for k in (1, 2, 3, 10):
    perms = np.argsort(rng.random((200000, 10)), axis=1)
    show(f"2 k={k}", F(1, 10), (perms[:, k-1] == 3).mean())

# Q3 exact joint via enumeration with sympy p
p = sp.symbols('p', positive=True)
joint = {}
for X, Y in itertools.product([0, 1], repeat=2):
    Q = sp.Matrix([[X, -X**2], [Y**2, X - Y]])
    D, T = Q.det(), Q.trace()
    pr = (p if X else 1-p) * (p if Y else 1-p)
    joint[(D, T)] = joint.get((D, T), 0) + pr
print("joint", {k: sp.factor(v) for k, v in joint.items()})
E = lambda f: sp.simplify(sum(f(d, t) * pr for (d, t), pr in joint.items()))
ED, ET = E(lambda d, t: d), E(lambda d, t: t)
print("E[D]", ED, "var D", sp.factor(E(lambda d, t: d**2) - ED**2))
print("E[T]", ET, "var T", sp.factor(E(lambda d, t: t**2) - ET**2))
print("cov", sp.factor(E(lambda d, t: d*t) - ED*ET))
pD0 = sum(v for (d, t), v in joint.items() if d == 0)
pT0 = sum(v for (d, t), v in joint.items() if t == 0)
print("P(D0,T0)-P(D0)P(T0)=", sp.factor(joint[(0, 0)] - pD0*pT0))
# MC at p=0.3
pv = 0.3
X = rng.random(N) < pv; Y = rng.random(N) < pv
Xi, Yi = X.astype(int), Y.astype(int)
D = Xi*(Xi-Yi) + Xi**2 * Yi**2   # det of [[X,-X^2],[Y^2,X-Y]] = X(X-Y)+X^2 Y^2
T = Xi + Xi - Yi
print("MC p=.3: ED", D.mean(), "varD", D.var(), "ET", T.mean(), "varT", T.var(), "cov", np.cov(D, T)[0, 1])
print("exact p=.3: ED .3 varD", .21, "ET .3 varT", 5*.21, "cov", 2*.21)

# Q4
a, b, t = sp.symbols('a b t', positive=True)
total = sp.integrate(-sp.Symbol('z')/a, (sp.Symbol('z'), -a, 0)) + sp.integrate(sp.Symbol('z')/a, (sp.Symbol('z'), 0, a)) + (b - a)
sol = sp.solve([sp.Eq(total, 1)], b)
bb = sol[b]
Ez = sp.integrate(sp.Symbol('z') * 1, (sp.Symbol('z'), a, bb))  # symmetric part has mean 0
asol = sp.solve(sp.Eq(Ez, sp.Rational(3, 8)), a)
print("Q4a: b=", bb, "a=", asol)
# MC for Q4 : sample from pdf f=2|z| on [-1/2,1/2], 1 on [1/2,1]
u = rng.random(N)
# inverse via CDF: F(t): t<-1/2:0; -1/2..0: 1/4-t^2 ; 0..1/2: 1/4+t^2; 1/2..1: t
def inv(u):
    zz = np.empty_like(u)
    c1 = u < .25; c2 = (u >= .25) & (u < .5); c3 = (u >= .5) & (u < .75); c4 = u >= .75
    # region -1/2..0: u = 1/4 - t^2 ... wait CDF at -1/2 = 0, so u=1/4-t^2 for u in [0,1/4]
    zz[c1] = -np.sqrt(.25 - u[c1])
    zz[c2] = -np.sqrt(.25 - u[c2]) * 0  # placeholder replaced below
    return zz
# simpler: rejection sampling from uniform(-1,1) with bound 1
cand = rng.uniform(-1, 1, 6_000_000); h = np.where(np.abs(cand) < .5, 2*np.abs(cand), np.where(cand > 0, 1.0, 0.0))
Z = cand[rng.random(cand.size) < h]
print("MC E[Z]", Z.mean(), "expect .375; P(Z<=-.25)", (Z <= -.25).mean(), "exact CDF 1/4-1/16=", .25-1/16,
      "P(Z<=.25)", (Z <= .25).mean(), "exact", .25+1/16, "P(Z<=.75)", (Z <= .75).mean(), "exact .75")
sel = np.abs(Z) < .5
print("Q4c MC", ((Z > .25) & sel).sum()/sel.sum(), "exact 3/8")
# exact 4c
zs = sp.Symbol('z')
print("Q4c exact", sp.integrate(2*zs, (zs, sp.Rational(1, 4), sp.Rational(1, 2))) / sp.integrate(2*sp.Abs(zs), (zs, -sp.Rational(1, 2), sp.Rational(1, 2))))

# Q5 : families with distinct sizes
ns = [1, 2, 5, 9]
EX = F(sum(ns), len(ns)); EY = F(sum(n*n for n in ns), sum(ns))
print("Q5 E[X]", EX, "E[Y]", EY, "Y>X", EY > EX)
for _ in range(2000):
    k = int(rng.integers(2, 8)); ns2 = list(rng.choice(np.arange(1, 50), k, replace=False))
    assert F(sum(n*n for n in ns2), sum(ns2)) > F(sum(ns2), k)
print("Q5 strictness holds on 2000 random distinct-size sets")
# MC: pick family vs pick person
fam = rng.choice(ns, 500000)
persons = np.repeat(ns, ns); per = rng.choice(persons, 500000)
print("MC EX", fam.mean(), "MC EY", np.array([ns for ns in [None]]).size and per.mean())

# Q6 circuits
def work(A, B, C, Dd, E_=None, which=1):
    if which == 1: return Dd & ((A & B) | C)
    return Dd & ((E_ & B) | A)
ps = sp.symbols('p q', positive=True); P_, Q_ = ps
s = {}
tot1 = 0; both = 0
for bits in itertools.product([0, 1], repeat=5):
    A_, B_, C_, D_, E__ = bits
    pr = 1
    for v in (A_, B_, C_, D_): pr *= P_ if v else 1-P_
    pr *= Q_ if E__ else 1-Q_
    s1 = D_ and ((A_ and B_) or C_); s2 = D_ and ((E__ and B_) or A_)
    if s1: tot1 += pr
    if s1 and s2: both += pr
print("Q6a", sp.factor(sp.expand(tot1.subs(Q_, 0) if False else tot1)))
tot1 = sp.expand(tot1); both = sp.expand(both)
print("Q6a P(Q1)=", sp.factor(tot1), "=", sp.expand(tot1))
print("Q6b P(both)=", sp.factor(both))
print("Q6c =", sp.factor(sp.simplify(both / tot1)))
# MC p=.6 q=.4
pv, qv = .6, .4
A = rng.random(N) < pv; B = rng.random(N) < pv; C = rng.random(N) < pv; Dd = rng.random(N) < pv; Ee = rng.random(N) < qv
s1 = Dd & ((A & B) | C); s2 = Dd & ((Ee & B) | A)
print("MC p=.6 q=.4: P1", s1.mean(), "exact", float(tot1.subs({P_: pv, Q_: qv})), " both", (s1 & s2).mean(), float(both.subs({P_: pv, Q_: qv})), " cond", (s1 & s2).sum()/s1.sum(), float((both/tot1).subs({P_: pv, Q_: qv})))
