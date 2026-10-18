import itertools, math
from fractions import Fraction as F
import numpy as np
import sympy as sp

rng = np.random.default_rng(99)
N = 4_000_000

# ---- Q1
X = rng.random(N); Y = rng.random(N)
S = X * Y; L = np.hypot(X, Y)
print('Q1a P(S<1/2) MC', (S < .5).mean(), 'exact', 0.5 * (1 + math.log(2)))
print('Q1b P(L<1/2) MC', (L < .5).mean(), 'exact pi/16', math.pi / 16)
m = X > .5
print('Q1c P(S<1/5|X>1/2) MC', ((S < .2) & m).sum() / m.sum(), 'exact', 2 / 5 * math.log(2))
x = sp.symbols('x')
print('  sympy', sp.N(2 * sp.integrate(sp.Rational(1, 5) / x, (x, sp.Rational(1, 2), 1))))
print('Q1d E[S] MC', S.mean(), '1/4 ; var MC', S.var(), '7/144=', 7 / 144)

# ---- Q2
roots = [(a, b) for a in range(1, 7) for b in range(1, 7)]
print('Q2a equal roots', F(sum(1 for a, b in roots if a == b), 36))
print('Q2b integer roots', F(36, 36), '(roots are X1,X2 themselves)')
diff = [(a, b) for a, b in roots if a != b]
print('Q2c product odd | distinct', F(sum(1 for a, b in diff if (a * b) % 2 == 1), len(diff)))
print('Q2d diff even | distinct', F(sum(1 for a, b in diff if (a - b) % 2 == 0), len(diff)))
# sanity: roots via numpy
d = rng.integers(1, 7, (N, 2))
disc = (d.sum(1))**2 - 4 * d[:, 0] * d[:, 1]
rt = (d.sum(1) + np.sqrt(disc)) / 2
print('  MC equal roots', (disc == 0).mean(), ' integer roots', np.mean(np.abs(rt - np.round(rt)) < 1e-9))

# ---- Q3  X heads in first two, Y heads in all three
p = sp.symbols('p')
joint = {}
for t in itertools.product([0, 1], repeat=3):
    w = 1
    for v in t: w *= p if v else (1 - p)
    k = (t[0] + t[1], sum(t))
    joint[k] = joint.get(k, 0) + w
for k in sorted(joint): print('Q3a P(X=%d,Y=%d)=' % k, sp.factor(sp.expand(joint[k])))
print('   sum', sp.simplify(sum(joint.values())))
PX = {a: sp.factor(sp.expand(sum(v for (xx, yy), v in joint.items() if xx == a))) for a in range(3)}
PY = {a: sp.factor(sp.expand(sum(v for (xx, yy), v in joint.items() if yy == a))) for a in range(4)}
print('Q3b PX', PX, ' PY', PY)
EX = sp.simplify(sum(a * PX[a] for a in PX)); EY = sp.simplify(sum(a * PY[a] for a in PY))
print('Q3c E[X]', EX, ' E[Y]', EY, ' var X', sp.factor(sp.simplify(sum(a * a * PX[a] for a in PX) - EX**2)), ' var Y', sp.factor(sp.simplify(sum(a * a * PY[a] for a in PY) - EY**2)))
print('Q3d indep? P(2,0)=', joint.get((2, 0), 0), ' P(0,3)=', joint.get((0, 3), 0), ' PX(2)PY(0)=', sp.factor(PX[2] * PY[0]), ' => dependent')
pv = .35
t3 = rng.random((N, 3)) < pv
Xs = t3[:, 0].astype(int) + t3[:, 1]; Ys = t3.sum(1)
for k in sorted(joint):
    print('   MC', k, ((Xs == k[0]) & (Ys == k[1])).mean(), float(joint[k].subs(p, pv)))

# ---- Q4
a, b, t = sp.symbols('a b t', positive=True)
e = sp.E
eq1 = sp.integrate(a * sp.exp(x), (x, -sp.oo, -1)) + sp.Rational(1, 2) + sp.integrate(b * sp.exp(-x), (x, 1, sp.oo)) - 1
eq2 = sp.integrate(a * x * sp.exp(x), (x, -sp.oo, -1)) + 0 + sp.integrate(b * x * sp.exp(-x), (x, 1, sp.oo))
sol = sp.solve([eq1, eq2], [a, b]); print('Q4a', sol)
av = sol[a]
Fx = lambda tt: (av * sp.exp(tt) if tt < -1 else (sp.Rational(1, 4) + (tt + 1) / 4 if tt < 1 else 1 - av * sp.exp(-tt)))
print('Q4b F: t<-1: (e/4)e^t ; -1<=t<1: (t+2)/4 ; t>=1: 1-(e/4)e^-t ; checks F(-1)=', sp.simplify(Fx(-1)), 'F(1)=', sp.simplify(Fx(1) if False else sp.Rational(1, 4) + sp.Rational(1, 2)), ' 1-(e/4)e^-1=', sp.simplify(1 - av * sp.exp(-1)))
Pc = sp.simplify((Fx(3) - Fx(-2)) / Fx(3))
print('Q4c P(X>-2|X<3) =', Pc, '=', sp.N(Pc), ' [ref 1 - e^-1/(4 - e^-2)]=', sp.N(1 - sp.exp(-1) / (4 - sp.exp(-2))))
# MC
aN = float(av)
U = rng.random(N)
Xs = np.empty(N)
lo = U < 0.25
mid = (U >= .25) & (U < .75)
hi = U >= .75
Xs[lo] = np.log(U[lo] / aN)
Xs[mid] = 4 * U[mid] - 2
Xs[hi] = -np.log((1 - U[hi]) / aN)
print('   MC mean', Xs.mean(), ' P(X>-2|X<3)', ((Xs > -2) & (Xs < 3)).sum() / (Xs < 3).sum(), ' F(3) MC', (Xs < 3).mean(), float(Fx(3)), ' F(-2) MC', (Xs < -2).mean(), float(Fx(-2)))
print('   alt: 0.99-type value candidates: P(-2<X<3)=', float(Fx(3) - Fx(-2)), ' P(X>-2)=', 1 - float(Fx(-2)), ' P(X<3)=', float(Fx(3)))

# ---- Q5 urn: D red, N-D black ; M tosses; heads->+2 red ; one ball drawn
Dd, Nn, M, pv = 3, 7, 4, 0.4
H = rng.binomial(M, pv, N)
red = Dd + 2 * H; tot = Nn + 2 * M
draw_red = rng.random(N) < red / tot
print('Q5a P(red) MC', draw_red.mean(), ' formula (D+2Mp)/(N+2M)=', (Dd + 2 * M * pv) / (Nn + 2 * M))
sel = draw_red
for n in range(0, 2 * M + 1):
    mc = ((2 * H == n) & sel).sum() / sel.sum()
    h = n / 2
    fm = math.comb(M, int(h)) * pv**h * (1 - pv)**(M - h) * (Dd + n) / (Dd + 2 * M * pv) if n % 2 == 0 else 0
    print('   Q5b n=%d MC %.5f formula %.5f' % (n, mc, fm))

# ---- Q6 circuit: parallel(series2, series2, bridge5)
pp = sp.symbols('p')
# bridge: nodes t,l,r,b ; edges t-l, t-r (A), l-b, r-b, l-r (center)
names = ['tl', 'tr', 'lb', 'rb', 'c']
def bridge_ok(s):
    tl, tr, lb, rb, c = s
    return (tl and lb) or (tr and rb) or (tl and c and rb) or (tr and c and lb)
def w(s):
    r = 1
    for v in s: r *= pp if v else (1 - pp)
    return r
Pb = sp.expand(sum(w(s) for s in itertools.product([0, 1], repeat=5) if bridge_ok(s)))
print('Q6 bridge', sp.factor(Pb))
P0 = sp.expand(1 - (1 - pp**2)**2 * (1 - Pb))
print('Q6a P0 =', sp.factor(P0), '=', P0)
# P1 = P(A fails | works): A = 'tr'
PbA0 = sp.expand(sum(w(s) for s in itertools.product([0, 1], repeat=5) if bridge_ok(s) and not s[1]))
# joint (A fails and circuit works) = (1-p) * [1-(1-p^2)^2 (1 - Pb|A=0)] where Pb|A=0 given A=0 conditional = PbA0/(1-p)
PbgA0 = sp.simplify(PbA0 / (1 - pp))
joint_ = (1 - pp) * (1 - (1 - pp**2)**2 * (1 - PbgA0))
P1 = sp.factor(sp.simplify(joint_ / P0))
print('Q6b P1 =', P1)
pvv = 0.6
print('  values p=.6: P0', float(P0.subs(pp, pvv)), 'P1', float(P1.subs(pp, pvv)))
st = rng.random((N, 9)) < pvv
o1 = st[:, 0] & st[:, 1]; o2 = st[:, 2] & st[:, 3]
tl, tr, lb, rb, c = st[:, 4:9].T   # tr is A
br = (tl & lb) | (tr & rb) | (tl & c & rb) | (tr & c & lb)
ok = o1 | o2 | br
print('  MC p=.6: P0', ok.mean(), ' P1', ((~tr) & ok).sum() / ok.sum())
