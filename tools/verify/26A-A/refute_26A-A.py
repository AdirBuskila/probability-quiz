# Refuter's own derivation for 26A-A (independent of steps_lib / probsteps). Exact + Monte Carlo.
import itertools, random, math
from fractions import Fraction as F
import sympy as sp

random.seed(3)
N = 400000

print("== Q1 three segments, X1,X2 ~ U(0,1/2); L=X1, R=X2, M=1-X1-X2")
def clip(poly, a, b, c):  # keep a*x+b*y<=c  (Sutherland-Hodgman, Fractions)
    out = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]
        fP, fQ = a * P[0] + b * P[1] - c, a * Q[0] + b * Q[1] - c
        if fP <= 0: out.append(P)
        if (fP < 0 < fQ) or (fQ < 0 < fP):
            t = fP / (fP - fQ)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out
def area(poly):
    s = F(0)
    for i in range(len(poly)):
        s += poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
    return abs(s) / 2
half = F(1, 2)
sq = [(F(0), F(0)), (half, F(0)), (half, half), (F(0), half)]
def prob(cons):  # list of (a,b,c): a*x1+b*x2<=c
    poly = sq
    for a, b, c in cons:
        poly = clip(poly, F(a), F(b), F(c))
        if not poly: return F(0)
    return area(poly) / area(sq)
# L<R: x1-x2<=0 ; L<M: 2x1+x2<=1 ; R>L, R>M: -(x2-x1)<=0 i.e. x1-x2<=0 ; M<R: 1-x1-x2<x2 -> -x1-2x2<=-1
pa = prob([(1, -1, 0), (2, 1, 1)])           # left shortest
pb = prob([(1, -1, 0), (-1, -2, -1)])        # right longest: R>L and R>M
pc = prob([(1, -1, 0), (2, 1, 1), (-1, -2, -1)])   # left shortest and right longest
pd = prob([(-1, -1, F(-1, 2)) if False else (1, 1, F(1, 2))]) if False else None
# middle longest: M>L: 2x1+x2<=1 ; M>R: x1+2x2<=1
pd = prob([(2, 1, 1), (1, 2, 1)])
print("left shortest", pa, " right longest", pb, " left shortest & right longest", pc, " middle longest", pd)
c = [0] * 5
for _ in range(N):
    x1, x2 = random.uniform(0, .5), random.uniform(0, .5); m = 1 - x1 - x2
    c[0] += x1 < x2 and x1 < m; c[1] += x2 > x1 and x2 > m; c[2] += x1 < m < x2 or (x1 < x2 and x1 < m and x2 > m); c[3] += m > x1 and m > x2
print("MC", [x / N for x in c[:4]], " (left shortest&right longest means L<M<R) ")
cc = 0
for _ in range(N):
    x1, x2 = random.uniform(0, .5), random.uniform(0, .5); m = 1 - x1 - x2
    cc += x1 < m < x2
print("MC L<M<R", cc / N, " sums: P(M longest)+P(L longest)+P(R longest)=1 check:", pd, F(1) - pd)
print("all equal: measure zero (X1=X2=1/3 single point) -> 0")

print("== Q2 Eugene & Boris")
p, q, Q, k = sp.symbols('p q Q k', positive=True)
qq = 1 - p
tie = sp.simplify(p**2 / (1 - qq**2))  # sum_k (p q^(k-1))^2, geometric
print("tie Q(p)=", sp.simplify(tie), " -> p(Q)=", sp.solve(sp.Eq(tie, Q), p))
pe = sp.simplify(p * qq / (1 - qq**2))  # sum_k p q^(k-1) q^k
print("P(Boris wins) = P(Eugene wins)=", sp.simplify(pe), " vs (1-Q)/2 =", sp.simplify((1 - tie) / 2 - pe))
pQ = sp.solve(sp.Eq(tie, Q), p)[0]
print("p in Q:", sp.simplify(pQ), " (1-Q)/2 =", (1 - Q) / 2)
# given tie, both first head at k : (p q^{k-1})^2 / Q
cond_tie = sp.simplify((p * qq ** (k - 1)) ** 2 / tie)
print("P(k|tie)=", sp.factor(cond_tie), " in Q:", sp.simplify(cond_tie.subs(p, pQ)))
cond_b = sp.simplify(p * qq ** (k - 1) * qq ** k / pe)
print("P(k|Boris wins)=", sp.factor(cond_b), " in Q:", sp.simplify(cond_b.subs(p, pQ)))
r_ = qq**2
Etie = sp.simplify(1 / (1 - r_))  # geometric(1-q^2) mean
print("E[length|tie] =", Etie, " in Q:", sp.simplify(Etie.subs(p, pQ)), " (if length counts both players' flips: 2x)")
# MC
pv = .35
cnt = {"tie": 0, "B": 0, "E": 0}; ksum = 0; kB = {}
def geom(pp):
    n = 1
    while random.random() >= pp: n += 1
    return n
for _ in range(N):
    e, b = geom(pv), geom(pv)
    if e == b: cnt["tie"] += 1; ksum += e
    elif b < e: cnt["B"] += 1; kB[b] = kB.get(b, 0) + 1
    else: cnt["E"] += 1
Qv = pv / (2 - pv)
print("MC p=.35: tie", cnt["tie"] / N, "exact", Qv, " win each", cnt["B"] / N, cnt["E"] / N, "exact", (1 - Qv) / 2,
      " E[len|tie]", ksum / cnt["tie"], "exact", float(Etie.subs(p, pv)), " P(k=2|B)", kB[2] / cnt["B"], float(cond_b.subs({p: pv, k: 2})))

print("== Q3 circuits: P(A)=p, P(B|A)=q, P(B|~A)=s")
p, qv, s = sp.symbols('p q s', positive=True)
ser = p * qv
par = 1 - (1 - p) * (1 - s)
print("series", ser, " parallel", sp.expand(par), " P(Q1|Q2)=", sp.simplify(ser / par), " P(Q1 or Q2)=", sp.expand(par), "(Q1 subset Q2)")
pv, qvv, sv = .6, .7, .2
c = [0] * 4
for _ in range(N):
    A = random.random() < pv; B = random.random() < (qvv if A else sv)
    c[0] += A and B; c[1] += A or B; c[2] += (A and B) and (A or B); c[3] += (A and B) or (A or B)
print("MC", c[0] / N, c[1] / N, c[2] / c[1], c[3] / N, "exact", pv * qvv, 1 - .4 * .8, pv * qvv / (1 - .4 * .8))

print("== Q4 pdf a e^x (x<0), b(1-x)^2 [0,2), c (x>=2)")
x, a, b, c_, mu = sp.symbols('x a b c mu', real=True)
print("c on [2,inf) diverges unless c=0 -> int:", sp.integrate(sp.Symbol('c') * 1, (x, 2, sp.oo)))
Ia = sp.integrate(a * sp.exp(x), (x, -sp.oo, 0)); Ib = sp.integrate(b * (1 - x) ** 2, (x, 0, 2))
print("norm:", Ia, "+", Ib, "= 1")
Ma = sp.integrate(x * a * sp.exp(x), (x, -sp.oo, 0)); Mb = sp.integrate(x * b * (1 - x) ** 2, (x, 0, 2))
print("mean:", Ma, "+", sp.simplify(Mb))
asol = 1 - Ib
mean = sp.simplify((Ma + Mb).subs(a, 1 - Ib))
print("a=", asol, " mu(b)=", mean)
bmu = sp.solve(sp.Eq(mean, mu), b)[0]
print("b(mu)=", bmu, " a(mu)=", sp.simplify(asol.subs(b, bmu)), " c=0")
print("range: b>=0, a>=0:", mean.subs(b, 0), mean.subs(b, sp.Rational(3, 2)))
t = sp.symbols('t')
Pm = sp.simplify(sp.integrate(b * (1 - x) ** 2, (x, 0, t)))
Pmu = sp.factor(sp.simplify(Pm.subs(b, bmu).subs(t, sp.Abs(mu))))
print("P(0<X<|mu|) for mu>=0:", sp.factor(sp.simplify(Pm.subs(b, bmu).subs(t, mu))), "  for mu<0:", sp.factor(sp.simplify(Pm.subs(b, bmu).subs(t, -mu))))
# CDF pieces
print("F(t) x<0: a e^t ; 0<=t<2: a + b((1-(1-t)^3)/3)... ", sp.simplify(Pm * 1))
for muv in [-.5, .0, .5, .8]:
    bv = float(bmu.subs(mu, muv)); av = 1 - 2 * bv / 3
    pd = lambda xx: av * math.exp(xx) if xx < 0 else (bv * (1 - xx) ** 2 if xx < 2 else 0)
    hm = max(av, bv)
    cnt = tt = 0; s_ = 0
    for _ in range(N):
        xx = random.uniform(-12, 2)
        if random.random() * hm < pd(xx):
            tt += 1; s_ += xx; cnt += 0 < xx < abs(muv)
    print("mu=", muv, "a,b=", av, bv, " MC mean", s_ / tt, " MC P(0<X<|mu|)", cnt / tt, " exact", float(Pm.subs(b, bmu).subs(t, abs(muv)).subs(mu, muv)))

print("== Q5 stick")
t = sp.symbols('t', positive=True)
print("eta=min(U,1-U), U~U(0,1): F(t)=2t on [0,1/2], density 2 -> U(0,1/2): E=1/4, var=1/48")
E1, V1 = sp.Rational(1, 4), sp.Rational(1, 48)
E1sq = V1 + E1 ** 2
print("E[eta^2]=", E1sq)
EX2 = E1 * E1; EX2sq = E1sq * E1sq
print("X2 (L=1): mean", EX2, " var", sp.simplify(EX2sq - EX2 ** 2), " = 7/2304?", sp.Rational(7, 2304))
n = sp.symbols('n', positive=True, integer=True)
print("X_n: mean 4^-n L ; var L^2 (12^-n - 16^-n)")
c = [0, 0, 0, 0]
for _ in range(N):
    u1 = random.random(); e1 = min(u1, 1 - u1)
    u2 = random.random(); e2 = min(u2, 1 - u2)
    x2 = e1 * e2
    c[0] += e1; c[1] += e1 * e1; c[2] += x2; c[3] += x2 * x2
print("MC eta mean/var", c[0] / N, c[1] / N - (c[0] / N) ** 2, " X2 mean/var", c[2] / N, c[3] / N - (c[2] / N) ** 2, " exact", 1 / 4, 1 / 48, 1 / 16, 7 / 2304)
# n=3
m3 = v3 = 0
for _ in range(N):
    pr = 1
    for _ in range(3):
        u = random.random(); pr *= min(u, 1 - u)
    m3 += pr; v3 += pr * pr
print("n=3 MC mean", m3 / N, "exact", 4 ** -3, " var", v3 / N - (m3 / N) ** 2, "exact", 12 ** -3 - 16 ** -3)

print("== Q6 grids")
def cells(R, C): return [(r, c) for r in range(R) for c in range(C)]
def classify(Nn, kk=2):
    cs = cells(Nn, Nn); res = {"all": 0, "hv": 0, "diag": 0}
    for pr in itertools.combinations(cs, 2):
        (r1, c1), (r2, c2) = pr; res["all"] += 1
        dr, dc = abs(r1 - r2), abs(c1 - c2)
        if (dr == 0 and dc == 1) or (dr == 1 and dc == 0): res["hv"] += 1
        if dr == 1 and dc == 1: res["diag"] += 1
    return res
for Nn in [2, 3, 4, 5]:
    r = classify(Nn)
    print("N=", Nn, r, "hv", F(r["hv"], r["all"]), F(4, Nn * (Nn + 1)), " diag", F(r["diag"], r["all"]), F(4 * (Nn - 1), Nn ** 2 * (Nn + 1)))
def line_count(Nn, kk):
    cs = cells(Nn, Nn); cnt = 0
    for sub in itertools.combinations(cs, kk):
        rs = sorted(r for r, c in sub); cs_ = sorted(c for r, c in sub)
        # consecutive in a row / column / diagonal / antidiagonal
        if len(set(rs)) == 1 and cs_ == list(range(cs_[0], cs_[0] + kk)): cnt += 1
        elif len(set(cs_)) == 1 and rs == list(range(rs[0], rs[0] + kk)): cnt += 1
        else:
            pts = sorted(sub)
            if all(pts[i + 1] == (pts[i][0] + 1, pts[i][1] + 1) for i in range(kk - 1)): cnt += 1
            elif all(pts[i + 1] == (pts[i][0] + 1, pts[i][1] - 1) for i in range(kk - 1)): cnt += 1
    return cnt
for Nn in [3, 4, 5]:
    for kk in range(2, Nn + 1):
        cnt = line_count(Nn, kk)
        form = 2 * (Nn - kk + 1) * (2 * Nn - kk + 1) if kk >= 2 else None
        print("N=", Nn, "k=", kk, "count", cnt, "formula 2(N-k+1)(2N-k+1)=", form, " prob", F(cnt, math.comb(Nn * Nn, kk)))
