import itertools, math, random
import numpy as np
import sympy as sp

rng = np.random.default_rng(12345)
N = 4_000_000
out = {}

def line(k, exact, mc=None):
    s = f"{k}: exact={exact}  ~{float(sp.N(exact)) if not isinstance(exact,(int,float)) else exact:.6f}"
    if mc is not None:
        s += f"  MC={mc:.6f}"
    print(s)

# ---- Q1: X,Y iid U(0,1) (legs of length 1, distances from the right angle)
x, y = sp.symbols('x y', positive=True)
X = rng.random(N); Y = rng.random(N)
L = np.hypot(X, Y); S = X * Y / 2
line('Q1b P(L<1)', sp.pi/4, (L < 1).mean())
pS = sp.Rational(1, 2) * (1 + sp.log(2))
line('Q1c P(S<1/4)', pS, (S < .25).mean())
# exact via integration
pS2 = sp.integrate(sp.Min(1, 1/(2*x)) if False else 1, (x, 0, sp.Rational(1,2))) + sp.integrate(1/(2*x), (x, sp.Rational(1,2), 1))
line('Q1c integral check', pS2)
both = (L < 1) & (S < .25)
line('Q1d P(L<1|S<1/4)', sp.pi/4 / pS, both.sum() / (S < .25).sum())
print('  L<1 subset of S<1/4:', bool(np.all(~(L < 1) | (S < .25))))
ES = sp.Rational(1, 8); VS = sp.Rational(1, 9)/4 - sp.Rational(1, 64)
line('Q1e E[S]', ES, S.mean()); line('Q1e var[S]', VS, S.var())

# ---- Q2 symbolic
p, q, s = sp.symbols('p q s')
PB = (q + s - 1) / q
PAB = p * PB
PA = s - PB + PAB
print('Q2 P(A)=', sp.simplify(PA), ' P(B)=', sp.simplify(PB), ' P(AB)=', sp.simplify(PAB))
print('  indep condition P(AB)-P(A)P(B) =', sp.factor(sp.simplify(PAB - PA * PB)))
# MC for Q2: pick a joint distribution, derive p,q,s and compare
for trial in range(3):
    w = rng.dirichlet(np.ones(4))  # P(AB),P(AB'),P(A'B),P(A'B')
    pab, pab_, pa_b, pa_b_ = w
    pv = pab / (pab + pa_b); qv = pa_b_ / (pab_ + pa_b_); sv = 1 - pa_b_
    sub = {p: pv, q: qv, s: sv}
    print('  trial', trial, 'P(A) formula', float(PA.subs(sub)), 'true', pab + pab_, '| P(B)', float(PB.subs(sub)), 'true', pab + pa_b, '| P(AB)', float(PAB.subs(sub)), pab)
# P(A|B)=p, P(Abar|Bbar)=q, q >= 1-s always: q = (1-s)/P(Bbar), P(Bbar)<=1
# independence: P(A|B)=P(A|Bbar)=1-q -> p+q=1 (s free). verify with MC by building independent A,B
for pa_, pb_ in [(0.3, 0.6), (0.8, 0.1)]:
    A = rng.random(N) < pa_; B = rng.random(N) < pb_
    pv = (A & B).sum() / B.sum(); qv = (~A & ~B).sum() / (~B).sum()
    print('  indep MC: p+q =', pv + qv, ' s=', (A | B).mean())

# ---- Q3 bridge
p, N1, N2, N3 = sp.symbols('p N1 N2 N3', positive=True)
Ps = 1 - (1 - p**N1) * (1 - p**N2) * (1 - p**N3)
print('Q3a =', Ps)
print('Q3b =', p**N2 / Ps, '   Q3c =', 1 - p**N2 / Ps)
# MC
for (n1, n2, n3, pv) in [(2, 3, 1, .7), (4, 2, 3, .9)]:
    g = rng.random((N // 4, 3, 4)) < pv
    br = np.stack([g[:, 0, :n1].all(1), g[:, 1, :n2].all(1), g[:, 2, :n3].all(1)], 1)
    ok = br.any(1)
    print('  MC', (n1, n2, n3, pv), 'a', ok.mean(), 'formula', float(Ps.subs({N1: n1, N2: n2, N3: n3, p: pv})),
          '| b', (br[:, 1] & ok).sum() / ok.sum(), float((p**N2 / Ps).subs({N1: n1, N2: n2, N3: n3, p: pv})))

# ---- Q4
a, b, c, g, mu, t = sp.symbols('a b c g mu t', real=True)
# finite variance needs c=0 (int c/x dx diverges), integrability needs g=0
c_, g_ = 0, 0
eqs = [sp.integrate(a*(x+1), (x, -1, 0)) + b - 1, sp.integrate(a*x*(x+1), (x, -1, 0)) + sp.integrate(b*x, (x, 0, 1)) - mu]
sol = sp.solve(eqs, [a, b]); print('Q4a', sol)
aa, bb = sol[a], sol[b]
print('Q4b  a>=0 ->', sp.solve(aa >= 0, mu), ' b>=0 ->', sp.solve(bb >= 0, mu))
print('Q4c F: [-1,0):', sp.simplify(sp.integrate(aa*(x+1), (x, -1, t)).subs(x, t)), ' [0,1):', sp.simplify(aa/2 + bb*t))
print('Q4d P(X<1|X>-1/2) = P(-1/2<X<1)/P(X>-1/2)=', sp.simplify((1 - sp.integrate(aa*(x+1), (x, -1, -sp.Rational(1,2)))) / (1 - sp.integrate(aa*(x+1), (x, -1, -sp.Rational(1,2))))), '(all mass < 1)')
# MC with mu = 0.1, 0.5, -1/3
for muv in [0.1, 0.5, -1/3, 0.0]:
    av = float(aa.subs(mu, muv)); bv = float(bb.subs(mu, muv))
    # sample: P(left)=av/2
    U = rng.random(N)
    left = U < av / 2
    # left piece density a(x+1): CDF a(x+1)^2/2 -> x=-1+sqrt(2 u/a)
    Xs = np.where(left, -1 + np.sqrt(np.clip(2 * U / max(av, 1e-12), 0, 1)), rng.random(N))
    print('  mu', muv, 'a,b', av, bv, 'mean MC', Xs.mean(), ' P(X<1|X>-.5)=', ((Xs < 1) & (Xs > -.5)).sum() / (Xs > -.5).sum(), ' F(-.5) MC', (Xs < -.5).mean(), 'formula', av / 8)

# ---- Q5 circuit
pp = sp.symbols('p')
Q0 = pp * (1 - (1 - pp)**2)
Q0 = sp.expand(Q0); print('Q5a', Q0)
# placements: series unit index among (A,B,C) uniform; Q0 series=A
def works(st, ser):
    par = [i for i in range(3) if i != ser]
    return st[ser] and (st[par[0]] or st[par[1]])
def prob_pair(sa, sb, pv):
    tot = 0
    for st in itertools.product([0, 1], repeat=3):
        w = 1
        for v in st: w *= pv if v else (1 - pv)
        if works(st, sa) and works(st, sb): tot += w
    return tot
def sym_pair(sa, sb):
    tot = 0
    for st in itertools.product([0, 1], repeat=3):
        w = 1
        for v in st: w *= pp if v else (1 - pp)
        if works(st, sa) and works(st, sb): tot += w
    return sp.expand(tot)
both = sp.expand(sum(sym_pair(0, k) for k in range(3)) / 3)
print('Q5b-1 P(new works) =', Q0)
print('Q5b-2 both =', sp.factor(both), '=', both)
print('Q5b-3 =', sp.simplify(both / Q0))
print('Q5b-4 =', sp.simplify((Q0 - both) / (1 - Q0)))
# MC (random placement)
pv = 0.6
st = rng.random((N, 3)) < pv
ser = rng.integers(0, 3, N)
def w_vec(st, ser):
    r = np.zeros(len(st), bool)
    for k in range(3):
        m = ser == k
        par = [i for i in range(3) if i != k]
        r[m] = st[m, k] & (st[m, par[0]] | st[m, par[1]])
    return r
q0 = w_vec(st, np.zeros(N, int)); qn = w_vec(st, ser)
print('  MC p=.6: P(new)', qn.mean(), 'P(both)', (q0 & qn).mean(), ' |  b3', (q0 & qn).sum() / q0.sum(), ' b4', ((~q0) & qn).sum() / (~q0).sum())
print('  formula p=.6: new', float(Q0.subs(pp, pv)), 'both', float(both.subs(pp, pv)), 'b3', float((both / Q0).subs(pp, pv)), 'b4', float(((Q0 - both) / (1 - Q0)).subs(pp, pv)))

# ---- Q6 (birthdays uniform over 365 days)
r = sp.Rational(1, 365)
k, n, NN, lam = sp.symbols('k n N lambda', positive=True)
print('Q6a Bin(N,1/365)')
print('Q6b1 Poisson(lambda/365)')
print('Q6b2 n-k ~ Poisson(lambda*364/365), shift by k')
# MC for b1/b2
lamv = 6.0
Xn = rng.poisson(lamv, 400000)
Yk = rng.binomial(Xn, 1/365) if False else rng.binomial(Xn, 0.05)  # use big prob (1/20) to get data
rr = 0.05
for kk in [0, 1, 2]:
    print('  MC b1 k=%d' % kk, (Yk == kk).mean(), 'Poisson(lam r):', sp.N(sp.exp(-lamv*rr)*(lamv*rr)**kk/sp.factorial(kk)))
m = Yk == 1
print('  MC b2 (k=1) dist of n:', [(nn, round(((Xn == nn) & m).sum() / m.sum(), 4), round(float(sp.N(sp.exp(-lamv*(1-rr))*(lamv*(1-rr))**(nn-1)/sp.factorial(nn-1))), 4)) for nn in range(1, 6)])
mm = Yk == 0
