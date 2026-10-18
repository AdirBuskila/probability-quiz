# Refuter's own derivation for 26A-B (independent of steps_lib / probsteps). Exact + Monte Carlo.
import itertools, random, math
from fractions import Fraction as F
import sympy as sp

random.seed(4)
N = 400000

print("== Q1 D = det[[X,1],[0,Y]] = X*Y, X,Y ~ U(0,1)")
t = sp.symbols('t', positive=True)
x, y = sp.symbols('x y', positive=True)
Fd = sp.integrate(sp.integrate(1, (y, 0, sp.Min(1, t / x))), (x, 0, 1)) if False else None
# P(XY<=t) = t + int_t^1 (t/x) dx = t - t ln t
Fd = t + sp.integrate(t / x, (x, t, 1))
print("F_D(t) 0<t<1:", sp.simplify(Fd), " density:", sp.simplify(sp.diff(Fd, t)))
fd = -sp.log(t)
ED = sp.integrate(t * fd, (t, 0, 1)); ED2 = sp.integrate(t ** 2 * fd, (t, 0, 1))
print("E[D]=", ED, " var=", sp.simplify(ED2 - ED ** 2), " (E[D^2]=", ED2, ")")
c = [0] * 4; ts = [0.1, 0.5]
for _ in range(N):
    d = random.random() * random.random(); c[0] += d; c[1] += d * d; c[2] += d <= .1; c[3] += d <= .5
print("MC mean/var", c[0] / N, c[1] / N - (c[0] / N) ** 2, " F(.1),F(.5)", c[2] / N, c[3] / N, " exact", float(Fd.subs(t, .1)), float(Fd.subs(t, .5)), " 7/144=", 7 / 144)

print("== Q2 coin")
p = sp.symbols('p', positive=True)
q = 1 - p
# (a) n tosses, tail first appears only after a head: first toss H, and at least one T among n tosses
def q2a(n, pv):
    tot = 0
    for seq in itertools.product('HT', repeat=n):
        if seq[0] == 'H' and 'T' in seq:
            pr = 1
            for s_ in seq: pr *= pv if s_ == 'H' else 1 - pv
            tot += pr
    return tot
for n in [2, 3, 5]:
    print("n=", n, "enum", q2a(n, .3), " p(1-p^(n-1))=", .3 * (1 - .3 ** (n - 1)), " alt p(1-p^n)?", .3 * (1 - .3 ** n), " (1-p)-(1-p)^n..:", (1 - .3) - (1 - .3) ** n)
# alt reading: the first T comes after the first H, where tail may not occur (no T needed): P(first toss H) = p
print("alt reading (no T required): p")
# (b) first head at even toss
k = sp.symbols('k', integer=True, positive=True)
pb = sp.simplify(sum(p * q ** (2 * j - 1) for j in range(1, 400)).subs(p, sp.Rational(3, 10)))
print("(b) numeric p=.3:", float(pb), " (1-p)/(2-p)=", .7 / 1.7)
# (c) m-th head at odd toss
def q2c(m, pv, K=3000):
    return sum(math.comb(kk - 1, m - 1) * pv ** m * (1 - pv) ** (kk - m) for kk in range(m, K) if kk % 2 == 1)
for m in [1, 2, 3, 5]:
    pv = .3
    print("m=", m, "series", q2c(m, pv, 600), " (1-(-p/(2-p))^m)/2 =", (1 - (-pv / (2 - pv)) ** m) / 2)
cc = {1: 0, 2: 0, 3: 0}
for _ in range(N):
    heads = 0; kk = 0
    first = None
    while heads < 3:
        kk += 1
        if random.random() < .3:
            heads += 1
            if heads == 1: f1 = kk
            if heads == 2: f2 = kk
    cc[1] += f1 % 2 == 1; cc[2] += f2 % 2 == 1; cc[3] += kk % 2 == 1
print("MC odd for m=1,2,3 (p=.3):", [cc[i] / N for i in (1, 2, 3)], " exact", [(1 - (-.3 / 1.7) ** m) / 2 for m in (1, 2, 3)])
# MC (b)
ce = 0
for _ in range(N):
    kk = 1
    while random.random() >= .3: kk += 1
    ce += kk % 2 == 0
print("MC (b):", ce / N, "exact", .7 / 1.7)
cn = {2: 0, 5: 0}
for n_ in (2, 5):
    for _ in range(N):
        s_ = [random.random() < .3 for _ in range(n_)]
        cn[n_] += s_[0] and (not all(s_))
print("MC (a) n=2,5:", cn[2] / N, cn[5] / N, "exact", .3 * (1 - .3), .3 * (1 - .3 ** 4))

print("== Q3 three components; P(A)=P(C)=p; B|AC=q1, B|~A~C=q2, B|A~C=q3, B|~AC=q4 (labels as printed)")
p, q1, q2, q3, q4 = sp.symbols('p q1 q2 q3 q4', positive=True)
pAC, pnAnC, pAnC, pnAC = p * p, (1 - p) ** 2, p * (1 - p), (1 - p) * p
PB = pAC * q1 + pnAnC * q2 + pAnC * q3 + pnAC * q4
print("P(B)=", sp.expand(PB))
PAB = p * (p * q1 + (1 - p) * q3)   # P(A and B) = P(A) [P(C)P(B|AC)+P(~C)P(B|A~C)]
PAgB = sp.simplify(PAB / PB)
print("P(A)P(B)-P(A,B)=", sp.factor(sp.simplify(p * PB - PAB)), "  -> dependent unless zero;  P(A|B)=", sp.factor(PAgB))
print("P(Q1 series)=P(ABC)= p^2 q1 :", p ** 2 * q1)
print("P(Q2 parallel)=1-P(~A~B~C)=", sp.expand(1 - pnAnC * (1 - q2)))
vals = {p: .6, q1: .9, q2: .2, q3: .5, q4: .7}
c = [0] * 5
for _ in range(N):
    A = random.random() < .6; C = random.random() < .6
    pb = {(1, 1): .9, (0, 0): .2, (1, 0): .5, (0, 1): .7}[(int(A), int(C))]
    B = random.random() < pb
    c[0] += B; c[1] += A and B; c[2] += A and B and C; c[3] += A or B or C
print("MC P(B), P(A,B), P(Q1), P(Q2):", c[0] / N, c[1] / N, c[2] / N, c[3] / N)
print("exact:", [float(e.subs(vals)) for e in (PB, PAB, p ** 2 * q1, 1 - pnAnC * (1 - q2))], " P(A|B)=", float(PAgB.subs(vals)), c[1] / c[0])
# swapped labelling check (q3 for ~A C, q4 for A ~C): same P(B) only if symmetric; show P(A|B) differs
PAB_sw = p * (p * q1 + (1 - p) * q4)
print("if q3/q4 swapped: P(A|B)=", sp.simplify(PAB_sw / (pAC * q1 + pnAnC * q2 + pAnC * q4 + pnAC * q3)))

print("== Q4 pdf a (x<0), b x^2 [0,1), c e^-(x-1) x>=1")
a, b, c_, mu, x = sp.symbols('a b c mu x', real=True)
print("a on (-inf,0): diverges unless a=0")
Ib = sp.integrate(b * x ** 2, (x, 0, 1)); Ic = sp.integrate(c_ * sp.exp(-(x - 1)), (x, 1, sp.oo))
Mb = sp.integrate(x * b * x ** 2, (x, 0, 1)); Mc = sp.integrate(x * c_ * sp.exp(-(x - 1)), (x, 1, sp.oo))
print("norm:", Ib, "+", Ic, "=1 ; mean:", Mb, "+", Mc)
csol = 1 - Ib / b * b / 1
c_val = sp.solve(sp.Eq(Ib + Ic, 1), c_)[0]
mean = sp.simplify((Mb + Mc).subs(c_, c_val))
print("c=", c_val, " mu(b)=", mean)
bmu = sp.solve(sp.Eq(mean, mu), b)[0]
print("b(mu)=", bmu, " c(mu)=", sp.simplify(c_val.subs(b, bmu)), " range: b in [0,3]:", mean.subs(b, 3), mean.subs(b, 0))
tt = sp.symbols('t', positive=True)
F1 = sp.integrate(b * x ** 2, (x, 0, tt)); F2 = sp.integrate(c_ * sp.exp(-(x - 1)), (x, 1, tt))
print("F(t) 0<=t<1 :", sp.simplify(F1.subs(b, bmu)), "  t>=1:", sp.simplify((Ib + F2).subs({b: bmu}).subs(c_, sp.simplify(c_val.subs(b, bmu)))))
Pm = sp.simplify(F1.subs(b, bmu).subs(tt, mu / 2))
print("P(0<X<mu/2) =", sp.factor(Pm))
for muv in [1.0, 1.5, 2.0, 0.75]:
    bv = float(bmu.subs(mu, muv)); cv = float(sp.simplify(c_val.subs(b, bmu)).subs(mu, muv))
    cnt = tot = 0; sm = 0
    for _ in range(N):
        if random.random() < bv / 3:
            xx = random.random() ** (1 / 3)          # density 3x^2 on [0,1]
        else:
            xx = 1 + random.expovariate(1.0)
        tot += 1; sm += xx; cnt += 0 < xx < muv / 2
    print("mu=", muv, "b,c=", bv, cv, " MC mean", sm / tot, " MC P(0<X<mu/2)", cnt / tot, " exact", float(Pm.subs(mu, muv)))

print("== Q5 urns")
from math import comb
def hyper(Nn, D, n, k): return F(comb(D, k) * comb(Nn - D, n - k), comb(Nn, n))
N1, D1, N2, D2, n, m = 10, 4, 8, 3, 4, 3
print("X pmf sums:", sum(hyper(N1, D1, n, k) for k in range(n + 1)))
def cond(l, k):  # Y=l given X=k
    Nn = N2 + n; D = D2 + k
    return F(comb(D, l) * comb(Nn - D, m - l), comb(Nn, m)) if 0 <= l <= m else F(0)
joint = {(k, l): hyper(N1, D1, n, k) * cond(l, k) for k in range(n + 1) for l in range(m + 1)}
print("joint sums:", sum(joint.values()))
# correlation rho(X, n-X) = -1
EX = sum(k * hyper(N1, D1, n, k) for k in range(n + 1)); VarX = sum(k * k * hyper(N1, D1, n, k) for k in range(n + 1)) - EX ** 2
print("EX", EX, "var", VarX, " n*D1/N1 =", F(n * D1, N1), " var formula n D/N (1-D/N)(N-n)/(N-1)=", F(n * D1, N1) * (1 - F(D1, N1)) * F(N1 - n, N1 - 1))
EXt = n - EX; cov = sum(k * (n - k) * hyper(N1, D1, n, k) for k in range(n + 1)) - EX * EXt
print("cov(X,n-X)=", cov, " = -var:", cov == -VarX)
cnt = {}
for _ in range(N // 4):
    urn1 = [1] * D1 + [0] * (N1 - D1); random.shuffle(urn1); moved = urn1[:n]
    urn2 = [1] * D2 + [0] * (N2 - D2) + moved; random.shuffle(urn2)
    kk = sum(moved); ll = sum(urn2[:m]); cnt[(kk, ll)] = cnt.get((kk, ll), 0) + 1
tot = sum(cnt.values())
print("max |MC-exact| joint:", max(abs(cnt.get(kl, 0) / tot - float(v)) for kl, v in joint.items()))
print("P(Y=l|X=k) conditional: hypergeometric(N2+n, D2+k, m)")

print("== Q6 grid / V shapes")
def vcount(R, C):
    cells = [(r, c) for r in range(R) for c in range(C)]
    shapes = [[(0, 0), (1, 1), (0, 2)],   # V:  X . X on top, X in middle bottom
              [(1, 0), (0, 1), (1, 2)],   # ^
              [(0, 1), (1, 0), (2, 1)],   # <  (left vertex)
              [(0, 0), (1, 1), (2, 0)]]   # >
    S = set()
    for sh in shapes:
        for r0 in range(R):
            for c0 in range(C):
                pts = [(r0 + a, c0 + b) for a, b in sh]
                if all(0 <= r < R and 0 <= c < C for r, c in pts): S.add(frozenset(pts))
    return len(S)
# check shapes against picture: picture shows (1) '<'-like: top-right, mid-left, bottom-right ; (2) V ; (3) ^ ; (4) '>' : top-left, mid-right, bottom-left
shapes_pic = [[(0, 1), (1, 0), (2, 1)], [(0, 0), (1, 1), (0, 2)], [(1, 0), (0, 1), (1, 2)], [(0, 0), (1, 1), (2, 0)]]
for R, C in [(4, 3), (3, 4), (3, 3), (5, 6)]:
    S = set()
    for sh in shapes_pic:
        for r0 in range(R):
            for c0 in range(C):
                pts = [(r0 + a, c0 + b) for a, b in sh]
                if all(0 <= r < R and 0 <= c < C for r, c in pts): S.add(frozenset(pts))
    form = 2 * (R - 1) * (C - 2) + 2 * (R - 2) * (C - 1)
    print(R, "x", C, "V placements", len(S), "formula 2(N-1)(M-2)+2(N-2)(M-1)=", form, " C(NM,3)=", comb(R * C, 3), " prob", F(len(S), comb(R * C, 3)))
# (a-1) 4x3: C(12,3)
print("C(12,3)=", comb(12, 3), " general C(NM,3)")
