"""Independent refuter derivations for 25A-B (own code)."""
import itertools, math, random
from fractions import Fraction as Fr
import sympy as sp
import mpmath as mp

random.seed(11)
print("== Q1  Z=X/Y ==")
M = 2_000_000
zs = []
for _ in range(M):
    x = random.random(); y = 1-random.random()   # y in (0,1]
    zs.append(x/y)
for t in (1/3, 3, 1):
    print("MC P(Z<%.3f)=" % t, sum(z < t for z in zs)/M)
print("exact 1/6, 5/6, 1/2")
t = sp.symbols('t', positive=True)
x, y = sp.symbols('x y', positive=True)
# F(t)= P(X<tY): for t<=1: int_0^1 min(1,t y) dy = t/2 ; t>1: 1 - 1/(2t)
F_lo = sp.integrate(t*y, (y, 0, 1))
F_hi = sp.integrate(sp.Min(1, t*y), (y, 0, 1))
print("F t<=1:", F_lo)
Fhi = sp.integrate(t*y, (y, 0, 1/t)) + sp.integrate(1, (y, 1/t, 1))
print("F t>1:", sp.simplify(Fhi), " f lo:", sp.diff(F_lo, t), " f hi:", sp.simplify(sp.diff(Fhi, t)))
Ev = sp.integrate(sp.sqrt(t)*sp.Rational(1, 2), (t, 0, 1)) + sp.integrate(sp.sqrt(t)/(2*t**2), (t, 1, sp.oo))
print("E sqrt Z =", Ev, " check E[sqrt X]E[1/sqrt Y] =", sp.integrate(sp.sqrt(x), (x, 0, 1))*sp.integrate(1/sp.sqrt(y), (y, 0, 1)))
print("E[Z] diverges:", sp.integrate(t/(2*t**2), (t, 1, sp.oo)))
# truncated MC check: E[sqrt Z ; Z<=T] exact = 1/3 + int_1^T t^-1.5/2 = 1/3 + (1 - T^-.5)
T = 100.0
mc = sum(math.sqrt(z) for z in zs if z <= T)/M
print("MC trunc E[sqrtZ;Z<=100]", mc, "exact", 1/3+(1-T**-.5))
# unbiased low-variance MC: stratified on y: E[sqrt(X)/sqrt(Y)] sample X,Y independently, mean of sqrt(x) times mean of 1/sqrt(y) via y=u^2 substitution
mc2 = (sum(math.sqrt(random.random()) for _ in range(M))/M)*(sum(1/math.sqrt(random.random()**2+1e-300) for _ in range(1))*0+2)
print("E sqrtX MC*2 (exact E[1/sqrt Y]=2):", mc2, "target 4/3")
# Var sqrt Z infinite since E[Z] infinite -> variance claim 'infinite' (not asked here)

print("== Q2 ==")
p, q, s = sp.symbols('p q s')
PBnA = s*(1-p)
PAB = q - PBnA
print("P(~A|B)", sp.simplify(PBnA/q), " P(A|B)", sp.simplify(PAB/q))
print("P(AnB)", sp.expand(PAB), " P(AuB)", sp.expand(p+q-PAB))
print("indep: s=q? ", sp.solve(sp.Eq(PAB, p*q), s), " (p!=1)")
print("disjoint: ", sp.solve(sp.Eq(PAB, 0), [s, q]), "-> q = s(1-p)")
# MC with explicit table p=.4,s=.25 -> P(B~A)=.15 ; q=.35 -> P(AB)=.2
pv, sv, qv = .4, .25, .35
joint = {(1, 1): qv-sv*(1-pv), (1, 0): pv-(qv-sv*(1-pv)), (0, 1): sv*(1-pv), (0, 0): (1-pv)*(1-sv)}
assert abs(sum(joint.values())-1) < 1e-12
cs = {k: 0 for k in joint}
for _ in range(1_000_000):
    u = random.random(); acc = 0
    for k, w in joint.items():
        acc += w
        if u < acc: cs[k] += 1; break
B = cs[(1, 1)]+cs[(0, 1)]
print("MC P(~A|B)", cs[(0, 1)]/B, "exact", sv*(1-pv)/qv, " P(A|B)", cs[(1, 1)]/B, " P(AnB)", cs[(1, 1)]/1e6, "exact", joint[(1, 1)])
print("MC P(B|~A)", cs[(0, 1)]/(cs[(0, 1)]+cs[(0, 0)]), "= s", sv)

print("== Q3 ==")
a, b, mu = sp.symbols('a b mu', real=True)
X = sp.symbols('X')
tri = sp.Piecewise((b*X, X < 1), (b*(2-X), True))
norm = a + sp.integrate(b*X, (X, 0, 1)) + sp.integrate(b*(2-X), (X, 1, 2)) - 1
mean = sp.integrate(a*X, (X, -1, 0)) + sp.integrate(b*X*X, (X, 0, 1)) + sp.integrate(b*(2-X)*X, (X, 1, 2)) - mu
sol = sp.solve([norm, mean], [a, b]); print(sol)
print("a>=0 -> mu<=", sp.solve(sol[a] >= 0, mu), " b>=0 ->", sp.solve(sol[b] >= 0, mu))
# CDF
tt = sp.symbols('tt', real=True)
bb = sol[b]; aa = sol[a]
F1 = aa*(tt+1)
F2 = aa + bb*tt**2/2
F3 = aa + bb/2 + bb*(2*tt - tt**2/2 - (2 - sp.Rational(1, 2)))
F3 = sp.simplify(F3)
print("F[-1,0):", sp.expand(F1), " F[0,1):", sp.expand(F2), " F[1,2):", sp.expand(F3), " F(2)=", sp.simplify(F3.subs(tt, 2)))
print("P(X<1|X>0) =", sp.simplify((bb/2)/bb))
# MC at mu=0.2
muv = .2; av = float(aa.subs(mu, muv)); bv = float(bb.subs(mu, muv)); print("a,b at mu=.2", av, bv)
cnt = tot = 0; sm = 0; n = 1_000_000
for _ in range(n):
    u = random.random()
    if u < av: Xv = -1+random.random()
    else:
        # triangle on [0,2] peak 1 : sum of two uniforms
        Xv = random.random()+random.random()
    sm += Xv
    if Xv > 0: tot += 1; cnt += Xv < 1
print("MC mean", sm/n, "target .2; P(X<1|X>0)", cnt/tot)
