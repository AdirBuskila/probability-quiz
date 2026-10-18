import itertools
from fractions import Fraction as F
import numpy as np
import sympy as sp

rng = np.random.default_rng(777)
N = 4_000_000

# ---- Q1: X1~U(0,1/3), X2~U(0,2/3)
X1 = rng.random(N) / 3; X2 = rng.random(N) * 2 / 3
print('Q1a P(X1>X2)  MC', (X1 > X2).mean(), ' exact 1/4')
m = 1 - X1 - X2
tri = (X1 < X2 + m) & (X2 < X1 + m) & (m < X1 + X2) & (m > 0)
print('Q1b triangle  MC', tri.mean(), ' exact 1/4')
g = X1 > X2
print('Q1c tri|X1>X2 MC', (tri & g).sum() / g.sum(), ' exact 1/8')
# exact via sympy
x1, x2 = sp.symbols('x1 x2')
dens = sp.Rational(9, 2)
A = sp.integrate(sp.integrate(dens, (x2, 0, x1)), (x1, 0, sp.Rational(1, 3)))
B = sp.integrate(sp.integrate(dens, (x2, sp.Max(0, sp.Rational(1, 2) - x1), sp.Rational(1, 2))), (x1, 0, sp.Rational(1, 3)))
print('  sympy A', A, 'B', B)
C = sp.integrate(sp.integrate(dens, (x2, sp.Rational(1, 2) - x1, x1)), (x1, sp.Rational(1, 4), sp.Rational(1, 3)))
print('  sympy tri&X1>X2', C, ' ratio', C / A)

# ---- Q2: both readings
for name, omega in [('100..999', range(100, 1000)), ('000..999 strings', range(0, 1000))]:
    om = list(omega); n = len(om)
    e2 = {k: F(sum(1 for v in om if v % k == 0), n) for k in (2, 4, 8)}
    print('Q2a', name, e2)
    p2, p4, p8 = e2[2], e2[4], e2[8]
    p24 = F(sum(1 for v in om if v % 4 == 0), n)  # A2&A4 = A4
    p48 = p8
    print('  A2,A4 independent?', p24 == p2 * p4, ' A4,A8 independent?', p48 == p4 * p8,
          ' A8 == A2&A4?', {v for v in om if v % 8 == 0} == {v for v in om if v % 2 == 0 and v % 4 == 0})

# ---- Q3
a, b, c, mu, t, x = sp.symbols('a b c mu t x', real=True)
# c/x on x>=1 not integrable -> c=0
eq1 = sp.integrate(a * sp.exp(x), (x, -sp.oo, 0)) + sp.integrate(b * x, (x, 0, 1)) - 1
eq2 = sp.integrate(a * x * sp.exp(x), (x, -sp.oo, 0)) + sp.integrate(b * x * x, (x, 0, 1)) - mu
sol = sp.solve([eq1, eq2], [a, b]); print('Q3a', sol, ' c=0')
print('Q3b  a>=0:', sp.solve(sol[a] >= 0, mu), ' b>=0:', sp.solve(sol[b] >= 0, mu))
print('Q3c  F:  t<0:  a e^t ; 0<=t<1: a + b t^2/2 ; t>=1: 1')
print('Q3d  P(X<1|X>0)= 1 since c=0')
for muv in [0.0, 0.5, -0.5]:
    av = float(sol[a].subs(mu, muv)); bv = float(sol[b].subs(mu, muv))
    U = rng.random(N)
    Xs = np.where(U < av, np.log(np.clip(U / av, 1e-300, 1)), np.sqrt(np.clip(2 * (U - av) / bv, 0, 1)) if bv > 0 else 0)
    print('  mu', muv, 'a,b', av, bv, 'mean MC', Xs.mean(), ' P(X<1|X>0)', ((Xs < 1) & (Xs > 0)).sum() / (Xs > 0).sum(), ' P(X<0) MC', (Xs < 0).mean(), 'vs a', av)

# ---- Q4 circuits
p = sp.symbols('p')
def prob_sym(fn, n):
    tot = 0
    for st in itertools.product([0, 1], repeat=n):
        w = 1
        for v in st: w *= p if v else (1 - p)
        if fn(st): tot += w
    return sp.expand(tot)
# nodes: left, top, bottom, right. A:L-T, B:T-R, C:L-B, D:B-R, E:T-B
def q1(st):
    A_, B_, C_, D_, E_ = st
    return (A_ and B_) or (C_ and D_) or (A_ and E_ and D_) or (C_ and E_ and B_)
def q2(st):
    A_, B_, C_, D_, E_ = st
    return A_ and (B_ or C_) and (D_ or E_)
P1 = prob_sym(q1, 5); P2 = prob_sym(q2, 5)
both = prob_sym(lambda s: q1(s) and q2(s), 5)
print('Q4a', sp.factor(P1), '=', P1)
print('Q4b', sp.factor(P2), '=', P2)
print('Q4c P(Q1|Q2)', sp.factor(sp.simplify(both / P2)))
print('Q4d P(~Q1|Q2)', sp.factor(sp.simplify(1 - both / P2)))
pv = 0.7
st = rng.random((N, 5)) < pv
A_, B_, C_, D_, E_ = st.T
Q1 = (A_ & B_) | (C_ & D_) | (A_ & E_ & D_) | (C_ & E_ & B_)
Q2 = A_ & (B_ | C_) & (D_ | E_)
print('  MC p=.7: Q1', Q1.mean(), 'f', float(P1.subs(p, pv)), ' Q2', Q2.mean(), 'f', float(P2.subs(p, pv)), ' Q1|Q2', (Q1 & Q2).sum() / Q2.sum(), 'f', float((both / P2).subs(p, pv)), ' ~Q1|Q2', ((~Q1) & Q2).sum() / Q2.sum())
print('  Q2 subset Q1?', not np.any(Q2 & ~Q1))

# ---- Q5 zeros of cos(w t) on (0,T), w~Exp(lam)
lam, T = 1.3, 2.0
w = rng.exponential(1 / lam, N)
# zeros of cos(w t) at w t = pi/2 + k pi ; count in (0,T) = floor(wT/pi + 1/2)
Nt = np.floor(w * T / np.pi + 0.5).astype(int)
q = np.exp(-lam * np.pi / T)
print('Q5a  P(N=k)=q^(k-1/2)(1-q) (k>=1), P(N=0)=1-sqrt(q)')
print('  MC', [round((Nt == k).mean(), 5) for k in range(4)], ' formula', [round(1 - q**.5, 5)] + [round(q**(k - .5) * (1 - q), 5) for k in range(1, 4)])
print('Q5b  E[N] MC', Nt.mean(), ' formula', q**.5 / (1 - q))
for k in (1, 2, 3):
    # t_{k+1}>T and t_k<T  <=> N==k ; given N>=k
    print('Q5c k=%d MC' % k, (Nt == k).sum() / (Nt >= k).sum(), ' formula 1-q =', 1 - q)

# ---- Q6
n_, qq, pp = 10, 0.35, 0.6
M = 1_000_000
Xa = rng.random((M, n_)) < qq
Dd = rng.random((M, n_)) < pp
Xc = Xa.sum(1); Yc = (Xa & Dd).sum(1)
print('Q6a X~Bin(n,q): mean', Xc.mean(), n_ * qq, ' var', Xc.var(), n_ * qq * (1 - qq))
print('Q6b Y~Bin(n,pq): mean', Yc.mean(), n_ * qq * pp, ' var', Yc.var(), n_ * qq * pp * (1 - qq * pp))
import math
print('  P(Y=3) MC', (Yc == 3).mean(), ' Bin', math.comb(n_, 3) * (qq * pp)**3 * (1 - qq * pp)**7)
print('Q6c rho MC', np.corrcoef(Xc, Yc)[0, 1], ' formula sqrt(p(1-q)/(1-pq))', math.sqrt(pp * (1 - qq) / (1 - pp * qq)))
Dd1 = np.ones_like(Dd)
Yc1 = (Xa & Dd1).sum(1)
print('Q6d p=1: rho', np.corrcoef(Xc, Yc1)[0, 1], ' (Y=X)')
