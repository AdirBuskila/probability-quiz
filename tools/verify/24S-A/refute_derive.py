import itertools, math
from fractions import Fraction as F
import numpy as np
import sympy as sp

rng = np.random.default_rng(2024)
N = 4_000_000

# ---- Q1
X = rng.random(N); Y = rng.random(N)
L = np.hypot(X, Y)
print('Q1a  X,Y iid U(0,1)')
print('Q1b P(L<1) MC', (L < 1).mean(), 'exact pi/4=', math.pi / 4, '| P(1/2<L<1) MC', ((L > .5) & (L < 1)).mean(), 'exact 3pi/16=', 3 * math.pi / 16)
Lp = np.sqrt(1 + (X - Y)**2)
print('Q1c P(L<sqrt10/3) MC', (Lp < math.sqrt(10) / 3).mean(), 'exact 5/9=', 5 / 9)
# sympy exact for parallel
x, y = sp.symbols('x y')
print('  sympy P(|X-Y|<1/3)=', 1 - (1 - sp.Rational(1, 3))**2)

# ---- Q2
# a: ever hit 5
u = [F(1)] + [F(0)] * 5
for n in range(1, 6):
    u[n] = sum(u[n - i] for i in range(1, 7) if n - i >= 0) / 6
print('Q2a ever sum==5 exact', u[5], float(u[5]))
sims = 400000
hit = 0
d = rng.integers(1, 7, (sims, 12))
cs = np.cumsum(d, 1)
print('   MC', (cs == 5).any(1).mean())
two = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 5)
print('Q2b', F(two, 36))
three = sum(1 for t in itertools.product(range(1, 7), repeat=3) if sum(t) == 5)
print('Q2c', F(three, 216))
num = sum(1 for t in itertools.product(range(1, 7), repeat=3) if sum(t) == 5 and t[0] + t[1] == 3)
den = sum(1 for t in itertools.product(range(1, 7), repeat=3) if t[0] + t[1] == 3)
print('Q2d', F(num, den))
d3 = rng.integers(1, 7, (N, 3))
print('   MC b', ((d3[:, 0] + d3[:, 1]) == 5).mean(), ' c', (d3.sum(1) == 5).mean(), ' d', ((d3.sum(1) == 5) & (d3[:, :2].sum(1) == 3)).sum() / (d3[:, :2].sum(1) == 3).sum())

# ---- Q3
pp = sp.symbols('p')
joint = {}
for t in itertools.product([0, 1], repeat=3):
    w = 1
    for v in t: w *= pp if v else (1 - pp)
    xx = t[0] + t[1]; yy = t[1] + t[2]
    joint[(xx, yy)] = joint.get((xx, yy), 0) + w
for k in sorted(joint): print('Q3a P(X=%d,Y=%d) =' % k, sp.factor(sp.expand(joint[k])))
print('   sum =', sp.simplify(sum(joint.values())))
PX = {a: sp.factor(sp.expand(sum(v for (xx, yy), v in joint.items() if xx == a))) for a in range(3)}
print('Q3b marginals', PX)
EX = sp.simplify(sum(a * PX[a] for a in range(3))); VX = sp.factor(sp.simplify(sum(a * a * PX[a] for a in range(3)) - EX**2))
print('Q3c E', EX, 'var', VX)
print('Q3d independent? P(0,2)=', joint.get((0, 2), 0), ' vs P_X(0)P_Y(2)=', sp.factor(PX[0] * PX[2]))
pv = .3
t3 = rng.random((N, 3)) < pv
Xs = t3[:, 0].astype(int) + t3[:, 1]; Ys = t3[:, 1].astype(int) + t3[:, 2]
for k in [(1, 1), (0, 1), (2, 1), (1, 2), (0, 2), (2, 2)]:
    print('   MC', k, ((Xs == k[0]) & (Ys == k[1])).mean(), float(joint.get(k, 0).subs(pp, pv)) if joint.get(k, 0) != 0 else 0)
print('   MC E', Xs.mean(), Ys.mean(), ' var', Xs.var(), Ys.var(), 'formula', 2 * pv, 2 * pv * (1 - pv))

# ---- Q4  f = a on [-1,0), b e^-x on x>=0 ; E[X]=0
a, b, t = sp.symbols('a b t')
sol = sp.solve([a + b - 1, sp.integrate(a * x, (x, -1, 0)) + sp.integrate(b * x * sp.exp(-x), (x, 0, sp.oo))], [a, b])
print('Q4a', sol)
av, bv = sol[a], sol[b]
print('Q4b F: -1<=t<0:', sp.simplify(av * (t + 1)), ' t>=0:', sp.simplify(av + bv * (1 - sp.exp(-t))))
Pn = sp.simplify((av + bv * (1 - sp.exp(-1)) - av / 2) / (av + bv * (1 - sp.exp(-1))))
print('Q4c P(X>-1/2 | X<1) =', Pn, '=', sp.N(Pn))
U = rng.random(N)
av_, bv_ = float(av), float(bv)
Xs = np.where(U < av_, -1 + U / av_, -np.log(1 - (U - av_) / bv_))
print('   MC mean', Xs.mean(), ' P(X>-.5|X<1)', ((Xs > -.5) & (Xs < 1)).sum() / (Xs < 1).sum(), float(sp.N(Pn)))

# ---- Q5
r = sp.Rational(1, 365)
print('Q5a X~Bin(N,p)')
print('Q5b Y~Bin(N,p/365)')
print('Q5c X-k | Y=k ~ Bin(N-k, p(1-r)/(1-p r)) ')
Nn, pv, rr = 8, 0.6, 0.1   # large r for MC visibility
Xn = rng.binomial(Nn, pv, 2_000_000); Yn = rng.binomial(Xn, rr)
for k in [0, 1, 2]:
    print('   MC P(Y=%d)' % k, (Yn == k).mean(), ' Bin(N,pr)', math.comb(Nn, k) * (pv * rr)**k * (1 - pv * rr)**(Nn - k))
k = 2
m = Yn == k
s_ = pv * (1 - rr) / (1 - pv * rr)
print('   MC cond', [round(((Xn == n) & m).sum() / m.sum(), 4) for n in range(k, Nn + 1)])
print('   formula ', [round(math.comb(Nn - k, n - k) * s_**(n - k) * (1 - s_)**(Nn - n), 4) for n in range(k, Nn + 1)])

# ---- Q6 circuit  nodes L,T,M,R ; A:L-T C:T-R B:T-M D:L-M E:M-R F:L-R
edges = {'A': ('L', 'T'), 'C': ('T', 'R'), 'B': ('T', 'M'), 'D': ('L', 'M'), 'E': ('M', 'R'), 'F': ('L', 'R')}
names = list('ABCDEF')
def connected(state):
    adj = {}
    for nm, up in zip(names, state):
        if up:
            u_, v_ = edges[nm]
            adj.setdefault(u_, set()).add(v_); adj.setdefault(v_, set()).add(u_)
    seen = {'L'}; stack = ['L']
    while stack:
        z = stack.pop()
        for w in adj.get(z, ()):
            if w not in seen: seen.add(w); stack.append(w)
    return 'R' in seen
P = pp
def weight(state):
    w = 1
    for v in state: w *= P if v else (1 - P)
    return w
tot = sp.expand(sum(weight(s) for s in itertools.product([0, 1], repeat=6) if connected(s)))
print('Q6a', sp.factor(tot), '=', tot)
bfail = sp.expand(sum(weight(s) for s in itertools.product([0, 1], repeat=6) if connected(s) and not s[names.index('B')]))
print('Q6b', sp.factor(sp.simplify(bfail / tot)))
one = sp.expand(sum(weight(s) for s in itertools.product([0, 1], repeat=6) if sum(s) == 5))
onew = sp.expand(sum(weight(s) for s in itertools.product([0, 1], repeat=6) if sum(s) == 5 and connected(s)))
print('Q6c', sp.simplify(onew / one), ' (cases: which single unit fails ->', [connected(tuple(0 if i == j else 1 for i in range(6))) for j in range(6)], ')')
print('Q6d', sp.factor(sp.simplify(P**6 / tot)))
pv = 0.6
st = rng.random((N, 6)) < pv
def conn_vec(st):
    A_, B_, C_, D_, E_, F_ = st.T
    # path enumeration L->R : F ; A-C ; D-E ; A-B-E ; D-B-C
    return F_ | (A_ & C_) | (D_ & E_) | (A_ & B_ & E_) | (D_ & B_ & C_)
cv = conn_vec(st)
print('   MC a', cv.mean(), float(tot.subs(pp, pv)), ' b', ((~st[:, 1]) & cv).sum() / cv.sum(), float((bfail / tot).subs(pp, pv)),
      ' c', (cv & (st.sum(1) == 5)).sum() / (st.sum(1) == 5).sum(), ' d', st.all(1).sum() / cv.sum(), float((P**6 / tot).subs(pp, pv)))
