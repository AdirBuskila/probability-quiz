"""Independent refuter derivations for 25B-B Q1-Q4 (own code)."""
import itertools, math, random
from fractions import Fraction as Fr
import sympy as sp

random.seed(31)
print("== Q1 flute ==")
M = 2_000_000
d = [abs(random.random()-random.random()) for _ in range(M)]
print("MC P(X<1/2)", sum(v < .5 for v in d)/M, "(3/4)  P(X>3/2)", sum(v > 1.5 for v in d)/M, "(0)  E", sum(d)/M, "(1/3)")
t, x, y = sp.symbols('t x y', positive=True)
# F(t)=P(|X1-X2|<=t) = 1-(1-t)^2 for 0<=t<=1
Ft = 1-(1-t)**2
print("F", sp.expand(Ft), " f", sp.diff(Ft, t), " E", sp.integrate(t*sp.diff(Ft, t), (t, 0, 1)), " F(1/2)", Ft.subs(t, sp.Rational(1, 2)))
for tv in (.2, .5, .9): print("MC F(%.1f)" % tv, sum(v <= tv for v in d)/M, "exact", 1-(1-tv)**2)

print("== Q2 ==")
p, q, s, b = sp.symbols('p q s b')
# unknown P(B)=b ; P(A&B)=(1-p) b ; P(A&~B)=q(1-b); P(AuB)=b+q(1-b)=s
bsol = sp.solve(sp.Eq(b+q*(1-b), s), b)[0]
PB = sp.simplify(bsol)
PAB = sp.simplify((1-p)*PB)
PA = sp.simplify(PAB+q*(1-PB))
print("P(B)", PB, "| P(A&B)", PAB, "| P(A)", sp.simplify(PA), "| combined:", sp.factor(sp.together(PA)))
print("P(A) alt simple:", sp.simplify(PA-(q*(1-q)+(s-q)*(1-p-q))/(1-q)))
print("q>s impossible since s = P(AuB) >= P(A&~B) >= ... : s-q = b(1-q) >=0")
print("independence: P(A&B)-P(A)P(B) factor:", sp.factor(sp.simplify(PAB-PA*PB)))
print("disjoint: P(A&B)=0 =>", sp.solve(sp.Eq(PAB, 0), p), " (b>0 i.e. s>q)")
# MC with p=.3,q=.2,s=.6 -> b=.5
pv, qv, sv = .3, .2, .6
bv = (sv-qv)/(1-qv)
joint = {(1, 1): (1-pv)*bv, (0, 1): pv*bv, (1, 0): qv*(1-bv), (0, 0): (1-qv)*(1-bv)}
cs = {k: 0 for k in joint}
N = 1_000_000
for _ in range(N):
    u = random.random(); acc = 0
    for k, w in joint.items():
        acc += w
        if u < acc: cs[k] += 1; break
print("MC P(B)", (cs[(1, 1)]+cs[(0, 1)])/N, "exact", bv, " P(A)", (cs[(1, 1)]+cs[(1, 0)])/N, "exact", float(PA.subs({p: pv, q: qv, s: sv})),
      " P(AuB)", 1-cs[(0, 0)]/N, "(.6) P(AB)", cs[(1, 1)]/N, float(PAB.subs({p: pv, q: qv, s: sv})))
# independent case p+q=1: p=.3,q=.7, s=.8 -> b=(0.1)/(0.3)
pv, qv, sv = .3, .7, .8; bv = (sv-qv)/(1-qv)
PAv = float(PA.subs({p: pv, q: qv, s: sv})); PABv = float(PAB.subs({p: pv, q: qv, s: sv}))
print("p+q=1 -> P(AB)", PABv, "P(A)P(B)", PAv*bv)
pv, qv, sv = .3, .2, .6
print("p+q!=1 -> P(AB)", float(PAB.subs({p: pv, q: qv, s: sv})), "P(A)P(B)", float(PA.subs({p: pv, q: qv, s: sv}))*(sv-qv)/(1-qv))

print("== Q3 guessing ==")
def p_neighbor(Nn):
    # guesser picks uniformly among 1..N, Eugene's number uniform; neighbor = |g-k|==1
    c = sum(1 for k in range(1, Nn+1) for g in range(1, Nn+1) if abs(g-k) == 1)
    return Fr(c, Nn*Nn)
for Nn in (2, 3, 5, 8):
    print(Nn, p_neighbor(Nn), Fr(2*(Nn-1), Nn*Nn))
for Nn, Mm in [(3, 4), (5, 2), (6, 6)]:
    both = Fr(1, Nn*Mm)
    cnt_any = sum(1 for k in range(1, Nn+1) for e in range(1, Mm+1) for g1 in range(1, Nn+1) for g2 in range(1, Mm+1) if g1 == k or g2 == e)
    tot = (Nn*Mm)**2
    c_nb = sum(1 for k in range(1, Nn+1) for e in range(1, Mm+1) for g1 in range(1, Nn+1) for g2 in range(1, Mm+1) if g1 == k and abs(g2-e) == 1)
    print(Nn, Mm, "any", Fr(cnt_any, tot), Fr(1, Nn)+Fr(1, Mm)-Fr(1, Nn*Mm), " k-right & e-neighbor", Fr(c_nb, tot), Fr(2*(Mm-1), Nn*Mm*Mm))

print("== Q4 ==")
a, B, c, dd, g, h, mu = sp.symbols('a b c d g h mu', real=True)
X = sp.symbols('X', real=True)
print("a must be 0 (integrable on x<-1); h must be 0 and g 0 on x>=1 (g/x+h not integrable unless g=h=0)")
eq_half = sp.Eq(sp.integrate(B*X+c, (X, -1, 0)), sp.Rational(1, 2))
eq_d = sp.Eq(dd*1, sp.Rational(1, 2))
mean = sp.integrate(X*(B*X+c), (X, -1, 0))+sp.integrate(X*dd, (X, 0, 1))
sol = sp.solve([eq_half, eq_d, sp.Eq(mean, mu)], [B, c, dd], dict=True)[0]
print(sol)
fl = (B*X+c).subs(sol)
print("f on [-1,0):", sp.expand(fl), " f(-1)>=0 ->", sp.solve(fl.subs(X, -1) >= 0, mu), "  f(0)>=0 ->", sp.solve(fl.subs(X, 0) >= 0, mu))
# CDF
tt = sp.symbols('tt', real=True)
F1 = sp.integrate(fl.subs(X, sp.Symbol('u')), (sp.Symbol('u'), -1, tt))
print("F[-1,0):", sp.expand(F1), " F(0)=", sp.simplify(F1.subs(tt, 0)), " F[0,1):", sp.Rational(1, 2)+sol[dd]*tt)
num = sp.integrate(fl, (X, -sp.Rational(1, 2), 0)); den = num+sp.Rational(1, 2)
print("P(X<0|X>-1/2) =", sp.simplify(num/den), "  num", sp.simplify(num))
# MC at mu=.05
muv = .05; bv = float(sol[B].subs(mu, muv)); cv = float(sol[c].subs(mu, muv)); print("b,c at mu=.05", bv, cv)
# sample neg part by rejection: density bx+c on [-1,0] max at one end
mx = max(cv-bv, cv)
def sample():
    if random.random() < .5:
        while True:
            xv = -random.random()
            if random.random()*mx < bv*xv+cv: return xv
    return random.random()
n = 1_000_000; sm = 0; cnt = tot = 0
for _ in range(n):
    xv = sample(); sm += xv
    if xv > -.5:
        tot += 1; cnt += xv < 0
print("MC mean", sm/n, "(target .05)  P(X<0|X>-1/2)", cnt/tot, "exact", float(((1+6*sp.Rational(5, 100))/(3+6*sp.Rational(5, 100)))))
