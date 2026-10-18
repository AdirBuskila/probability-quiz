# -*- coding: utf-8 -*-
# Refuter's own derivation, exact (fractions/sympy/brute force) + own Monte Carlo. ASCII output.
import itertools
from fractions import Fraction as F
import numpy as np
import sympy as sp

rng = np.random.default_rng(777)
M = 4_000_000
out = []


def show(name, exact, mc=None):
    s = f"{name}: exact={exact}"
    if mc is not None:
        s += f"  mc={mc:.5f}  (exact={float(exact):.5f})"
    print(s)


# ---------- helpers
def dice_dist(w):
    return {i + 1: F(w[i]) for i in range(6)}


def enum_dice(w, n, ev, given=lambda r: True):
    d = dice_dist(w)
    num = den = F(0)
    for r in itertools.product(range(1, 7), repeat=n):
        pr = F(1)
        for x in r:
            pr *= d[x]
        if given(r):
            den += pr
            if ev(r):
                num += pr
    return num / den


def mc_dice(w, n, ev, given=lambda r: np.ones(len(r), bool)):
    w = np.array([float(x) for x in w])
    r = rng.choice(6, size=(M, n), p=w / w.sum()) + 1
    g = given(r)
    e = ev(r)
    return (g & e).sum() / g.sum()


print("===== 24A-C =====")
# Q1: S1=X/2, S2=Y/2, S3=(1-X-Y)/2
x = rng.random(M); y = rng.random(M)
inside = x + y < 1
S1 = x / 2; S2 = y / 2; S3 = (1 - x - y) / 2
show("C1a P(inside)", F(1, 2), inside.mean())
show("C1b P(S1<1/3|in)", F(8, 9), ((S1 < 1 / 3) & inside).sum() / inside.sum())
show("C1c P(S1+S2>1/3|in)", F(5, 9), ((S1 + S2 > 1 / 3) & inside).sum() / inside.sum())
show("C1d P(S3>S1|in)", F(1, 2), ((S3 > S1) & inside).sum() / inside.sum())
# exact by sympy
X, Y = sp.symbols('x y', positive=True)
print("  sympy C1b:", sp.integrate(sp.integrate(1, (Y, 0, 1 - X)), (X, 0, sp.Rational(2, 3))) * 2)  # area X<2/3 inside /(1/2)

# Q2
w = [1, 2, 1, 2, 1, 2]
w = [F(a, 9) for a in w]
print("  sum w =", sum(w))
show("C2a q", F(1, 9))
show("C2b P(sum2=5)", enum_dice(w, 2, lambda r: sum(r) == 5), mc_dice(w, 2, lambda r: r.sum(1) == 5))
show("C2c P(sum3=5)", enum_dice(w, 3, lambda r: sum(r) == 5), mc_dice(w, 3, lambda r: r.sum(1) == 5))
show("C2d P(sum3=5|r1+r2=2)", enum_dice(w, 3, lambda r: sum(r) == 5, lambda r: r[0] + r[1] == 2),
     mc_dice(w, 3, lambda r: r.sum(1) == 5, lambda r: r[:, 0] + r[:, 1] == 2))
show("C2e P(sum3=5|r1<r2)", enum_dice(w, 3, lambda r: sum(r) == 5, lambda r: r[0] < r[1]),
     mc_dice(w, 3, lambda r: r.sum(1) == 5, lambda r: r[:, 0] < r[:, 1]))

# Q3 symbolic
p, q = sp.symbols('p q', positive=True)
def joint(dfun, tfun):
    J = {}
    for xv, yv in itertools.product([0, 1], repeat=2):
        pr = (p if xv else 1 - p) * (q if yv else 1 - q)
        k = (dfun(xv, yv), tfun(xv, yv))
        J[k] = J.get(k, 0) + pr
    return {k: sp.expand(v) for k, v in J.items()}
def moments(J):
    ED = sum(k[0] * v for k, v in J.items()); ET = sum(k[1] * v for k, v in J.items())
    VD = sum(k[0] ** 2 * v for k, v in J.items()) - ED ** 2
    VT = sum(k[1] ** 2 * v for k, v in J.items()) - ET ** 2
    C = sum(k[0] * k[1] * v for k, v in J.items()) - ED * ET
    return [sp.factor(sp.simplify(z)) for z in (ED, VD, ET, VT, C)]
# C: Q=[[-1,-X^2],[Y^2,X+Y]]: det = -(X+Y)+X^2Y^2 ; tr = -1+X+Y
JC = joint(lambda a, b: -1 * (a + b) + a * a * b * b, lambda a, b: -1 + a + b)
print("  C3 joint:", JC)
print("  C3 E[D],V[D],E[T],V[T],cov:", moments(JC))
# independence?
margD = {}; margT = {}
for k, v in JC.items():
    margD[k[0]] = margD.get(k[0], 0) + v; margT[k[1]] = margT.get(k[1], 0) + v
print("  C3 independence defects:", [sp.factor(sp.simplify(JC.get((d, t), 0) - margD[d] * margT[t])) for d in margD for t in margT])
# MC at p=.3,q=.6
pv, qv = .3, .6
xs = rng.random(M) < pv; ys = rng.random(M) < qv
Dm = -(xs.astype(int) + ys) + (xs & ys); Tm = -1 + xs.astype(int) + ys
sub = {p: pv, q: qv}
print("  C3 MC at p=.3,q=.6: E[D]=%.4f V[D]=%.4f E[T]=%.4f V[T]=%.4f cov=%.4f" % (Dm.mean(), Dm.var(), Tm.mean(), Tm.var(), np.cov(Dm, Tm, bias=True)[0, 1]))
print("  C3 exact at p=.3,q=.6:", [float(z.subs(sub)) for z in moments(JC)])

# Q4: f = x/a on [0,a], 1 on [a,b]
a, b, t = sp.symbols('a b t', positive=True)
sol = sp.solve([a / 2 + (b - a) - 1, a**2 / 3 + (b**2 - a**2) / 2 - sp.Rational(23, 24)], [a, b], dict=True)
print("  C4a a,b sols:", sol)
av, bv = [(s[a], s[b]) for s in sol if s[b] > s[a]][0]
print("  C4 chosen", av, bv)
Xs = sp.symbols('X')
def pdf(xx):
    return np.where((xx >= 0) & (xx < float(av)), xx / float(av), np.where((xx >= float(av)) & (xx <= float(bv)), 1.0, 0.0))
# sample by inverse cdf
u = rng.random(M)
A_, B_ = float(av), float(bv)
# cdf: x^2/(2a) for x<=a ; a/2 + (x-a) after
xs_ = np.where(u <= A_ / 2, np.sqrt(2 * A_ * u), u + A_ / 2)
print("  C4 MC mean=%.5f (23/24=%.5f)" % (xs_.mean(), 23 / 24))
cdf = sp.Piecewise((0, t < 0), (t**2 / (2 * av), t < av), (av / 2 + t - av, t < bv), (1, True))
print("  C4b cdf:", cdf)
P1 = (sp.Rational(5, 4) - sp.Rational(1, 2))  # x>1/2 interval
def Fcdf(v): return float(cdf.subs(t, v))
exact_c = (Fcdf(1.25) - Fcdf(0.5)) / (1 - Fcdf(0.5))
print("  C4c exact:", sp.nsimplify(exact_c), " mc: %.5f" % (((xs_ <= 1.25) & (xs_ > .5)).sum() / (xs_ > .5).sum()))

# Q5 numeric check of closed forms, N=10, D=3, p=.4, n=4
Nn, Dd, pp, nn = 10, 3, .4, 4
r = Dd / Nn; s = 1 - r
print("  C5a Bin(n, D/N): P(X=2)=", sp.binomial(nn, 2) * r**2 * s**2)
J = rng.geometric(pp, size=M)  # number of tosses until first head, support 1..
Z = rng.binomial(J, r)
print("  C5b MC P(Z=0)=%.5f closed p*s/(1-(1-p)s)=%.5f" % ((Z == 0).mean(), pp * s / (1 - (1 - pp) * s)))
for k in (1, 2, 3):
    cl = pp / (1 - pp) * (r * (1 - pp))**k / (1 - (1 - pp) * s)**(k + 1)
    print("  C5c MC P(Z=%d)=%.5f closed=%.5f" % (k, (Z == k).mean(), cl))

# Q6 bridge, symbolic enumeration; nodes: S,T,B,K ; A:S-T, C:S-B, B:T-K, D:B-K, E:T-B
def conn(edges, src, snk):
    seen = {src}; ch = True
    while ch:
        ch = False
        for u_, v_ in edges:
            if (u_ in seen) != (v_ in seen):
                seen |= {u_, v_}; ch = True
    return snk in seen
EDG1 = {'A': ('S', 'T'), 'C': ('S', 'B'), 'B': ('T', 'K'), 'D': ('B', 'K'), 'E': ('T', 'B')}
names = list('ABCDE')
def prob_expr(cond):
    tot = 0
    for st in itertools.product([0, 1], repeat=5):
        d = dict(zip(names, st))
        pr = 1
        for n_ in names:
            pr *= p if d[n_] else 1 - p
        if cond(d):
            tot += pr
    return sp.factor(sp.expand(tot))
q1 = lambda d: conn([EDG1[n_] for n_ in names if d[n_]], 'S', 'K')
q2c = lambda d: (d['A'] and d['B']) or False
# Q2 of 24A-C: (A||B) series (C||D||E)
q2_c = lambda d: (d['A'] or d['B']) and (d['C'] or d['D'] or d['E'])
# Q2 of 24A-D: A || (E-B) || (C-D)
q2_d = lambda d: d['A'] or (d['E'] and d['B']) or (d['C'] and d['D'])
P1 = prob_expr(q1)
print("  Q1 prob:", sp.expand(P1))
P2c = prob_expr(q2_c)
print("  C6b Q2 prob:", sp.expand(P2c), "check", sp.simplify(P2c - (1 - (1 - p)**2) * (1 - (1 - p)**3)))
Pb = prob_expr(lambda d: q1(d) and q2_c(d))
cc = sp.factor(sp.simplify(Pb / P2c))
print("  C6c P(Q1|Q2) =", cc)
pv = 0.6
Sm = rng.random((M, 5)) < pv
dd = {n_: Sm[:, i] for i, n_ in enumerate(names)}
# vectorised bridge: Q1 works iff (A&B)|(C&D)|(A&E&D)|(C&E&B)
q1v = (dd['A'] & dd['B']) | (dd['C'] & dd['D']) | (dd['A'] & dd['E'] & dd['D']) | (dd['C'] & dd['E'] & dd['B'])
q2cv = (dd['A'] | dd['B']) & (dd['C'] | dd['D'] | dd['E'])
print("  C6 MC p=.6: Q1=%.5f exactQ1=%.5f; Q2=%.5f exact=%.5f; Q1|Q2=%.5f exact=%.5f" % (q1v.mean(), float(P1.subs(p, pv)), q2cv.mean(), float(P2c.subs(p, pv)), (q1v & q2cv).sum() / q2cv.sum(), float(cc.subs(p, pv))))

print("===== 24A-D =====")
# Q1: grasshopper
x = rng.random(M); y = rng.random(M)
show("D1a P(X1+X2<=2/3)", F(2, 9), (x + y <= 2 / 3).mean())
show("D1b P(both<2/3)", F(4, 9), ((x < 2 / 3) & (y < 2 / 3)).mean())
show("D1c P(sum<=1|X1<=2/3)", F(2, 3), ((x + y <= 1) & (x <= 2 / 3)).sum() / (x <= 2 / 3).sum())
# Q2
fair = [F(1, 6)] * 6
show("D2a", enum_dice(fair, 2, lambda r: sum(r) == 6), mc_dice(fair, 2, lambda r: r.sum(1) == 6))
show("D2b", enum_dice(fair, 3, lambda r: sum(r) == 6), mc_dice(fair, 3, lambda r: r.sum(1) == 6))
show("D2c", enum_dice(fair, 3, lambda r: sum(r) == 6, lambda r: r[0] + r[1] == 2), mc_dice(fair, 3, lambda r: r.sum(1) == 6, lambda r: r[:, 0] + r[:, 1] == 2))
show("D2d", enum_dice(fair, 3, lambda r: sum(r) == 6, lambda r: r[0] < r[1]), mc_dice(fair, 3, lambda r: r.sum(1) == 6, lambda r: r[:, 0] < r[:, 1]))
show("D2e", enum_dice(fair, 3, lambda r: sum(r) == 6, lambda r: r[0] == r[1]), mc_dice(fair, 3, lambda r: r.sum(1) == 6, lambda r: r[:, 0] == r[:, 1]))
# Q3: Q=[[0,X],[Y,X+Y]] det=-XY tr=X+Y
JD = joint(lambda a_, b_: -a_ * b_, lambda a_, b_: a_ + b_)
print("  D3 joint:", JD)
print("  D3 E[D],V[D],E[T],V[T],cov:", moments(JD))
pv, qv = .3, .6
xs = rng.random(M) < pv; ys = rng.random(M) < qv
Dm = -(xs & ys).astype(int); Tm = xs.astype(int) + ys
print("  D3 MC: E[D]=%.4f V[D]=%.4f E[T]=%.4f V[T]=%.4f cov=%.4f" % (Dm.mean(), Dm.var(), Tm.mean(), Tm.var(), np.cov(Dm, Tm, bias=True)[0, 1]))
print("  D3 exact:", [float(z.subs({p: pv, q: qv})) for z in moments(JD)])
# Q4
a, b, x_ = sp.symbols('a b x', positive=True)
area = sp.integrate(a * (b - sp.Abs(x_)), (x_, -b, b)) if False else 2 * sp.integrate(a * (b - x_), (x_, 0, b))
EX = 0
VX = 2 * sp.integrate(x_**2 * a * (b - x_), (x_, 0, b))
print("  D4 area", sp.simplify(area), " var", sp.simplify(VX))
s1 = sp.solve([sp.simplify(area) - 1, sp.simplify(VX) - sp.Rational(2, 3)], [a, b], dict=True)
print("  D4b sols", s1)
av, bv = s1[0][a], s1[0][b]
tt = sp.symbols('t', real=True)
Fm = sp.integrate(av * (bv - sp.Abs(x_)), (x_, -bv, tt)) if False else None
# cdf piecewise
cdfL = sp.integrate(av * (bv + x_), (x_, -bv, tt))   # -b<=t<=0
cdfR = sp.Rational(1, 2) + sp.integrate(av * (bv - x_), (x_, 0, tt))
print("  D4c cdf: t<-b:0; -b<=t<0:", sp.expand(cdfL), "; 0<=t<b:", sp.expand(cdfR), "; t>=b: 1")
num = sp.integrate(av * (bv - x_), (x_, av, 1)); den = 2 * sp.integrate(av * (bv - x_), (x_, 0, 1))
print("  D4d exact:", sp.nsimplify(num / den))
# MC triangular on [-b,b]
A_, B_ = float(av), float(bv)
Xs_ = (rng.random(M) + rng.random(M) - 1) * B_
print("  D4 MC: E=%.4f var=%.4f (2/3=%.4f) ; P(X>a| |X|<1)=%.5f" % (Xs_.mean(), Xs_.var(), 2 / 3, ((Xs_ > A_) & (np.abs(Xs_) < 1)).sum() / (np.abs(Xs_) < 1).sum()))
# Q5: births, P(birth on day)=1/365
lam = 7.0; pb = 1 / 365
print("  D5 note: birth-on-day prob 1/365 is not in the printed question text (check page)")
# a) Bin(N,1/365); b) Poisson(lam/365); c) n-k ~ Poisson(lam*364/365)
Xp = rng.poisson(lam, size=M * 1)
Kb = rng.binomial(Xp, pb)
# larger lam so events non-negligible
lam2 = 700.0
Xp2 = rng.poisson(lam2, size=M); Kb2 = rng.binomial(Xp2, pb)
for k in (0, 1, 2, 3):
    from math import exp, factorial
    cl = exp(-lam2 * pb) * (lam2 * pb)**k / factorial(k)
    print("  D5b k=%d MC=%.5f  Poisson(lam/365)=%.5f" % (k, (Kb2 == k).mean(), cl))
k = 2
sel = Kb2 == k
for n in (k, k + 1, k + 2, k + 3):
    from math import exp, factorial
    mu = lam2 * (1 - pb)
    cl = exp(-mu) * mu**(n - k) / factorial(n - k)
    print("  D5c n=%d MC=%.5f closed(n-k~Poisson(lam*364/365))=%.5f" % (n, (Xp2[sel] == n).mean(), cl))

# Q6 24A-D: Q1 bridge (as C), Q2 = A || (E-B) || (C-D)
P2d = prob_expr(q2_d)
print("  D6a Q1:", sp.expand(P1))
print("  D6b Q2:", sp.expand(P2d), " check 1-(1-p)(1-p^2)^2:", sp.simplify(P2d - (1 - (1 - p) * (1 - p**2)**2)))
Pbd = prob_expr(lambda d: q1(d) and q2_d(d))
dc = sp.factor(sp.simplify(Pbd / P1))
print("  D6c P(Q2|Q1) =", dc, "  expanded num/den:", sp.expand(Pbd), "/", sp.expand(P1))
pv = 0.6
q2dv = dd['A'] | (dd['E'] & dd['B']) | (dd['C'] & dd['D'])
print("  D6 MC p=.6: Q2=%.5f exact=%.5f; Q2|Q1=%.5f exact=%.5f" % (q2dv.mean(), float(P2d.subs(p, pv)), (q1v & q2dv).sum() / q1v.sum(), float(dc.subs(p, pv))))
