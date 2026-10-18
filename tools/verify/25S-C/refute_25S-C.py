# Refuter's own derivation for 25S-C (independent of steps_lib / probsteps). Exact + Monte Carlo.
import itertools, random
from fractions import Fraction as F
import sympy as sp

random.seed(1)
N = 400000

print("== Q1 triangle: b~U(0,1), L~U(1,2), a=(L-b)/2")
b, u = sp.symbols('b u')   # u = L-1 in (0,1)
# a<1/4  <=> L-b<1/2 <=> u+1-b<1/2 <=> u<b-1/2
p1 = sp.integrate(sp.Max(0, b - sp.Rational(1, 2)), (b, 0, 1))
p2 = 1 - sp.integrate(sp.Max(0, 1 - (b + sp.Rational(1, 3))), (b, 0, 1))  # a>=2/3 <=> u>=b+1/3
print("P(a<1/4)=", p1, " P(a<2/3)=", p2)
Eb, Ebb = sp.Rational(1, 2), sp.Rational(1, 3)
EL, ELL = sp.Rational(3, 2), sp.integrate((u + 1) ** 2, (u, 0, 1))
Ea = (EL - Eb) / 2
Ea2 = sp.integrate(sp.integrate(((u + 1 - b) / 2) ** 2, (u, 0, 1)), (b, 0, 1))
print("E[a]=", Ea, " var[a]=", sp.simplify(Ea2 - Ea ** 2))
Eab = sp.integrate(sp.integrate((u + 1 - b) / 2 * b, (u, 0, 1)), (b, 0, 1))
print("cov(a,b)=", sp.simplify(Eab - Ea * Eb))
c = [0, 0, 0, 0, 0]
for _ in range(N):
    bb = random.random(); L = 1 + random.random(); a = (L - bb) / 2
    c[0] += a < .25; c[1] += a < 2 / 3; c[2] += a; c[3] += a * a; c[4] += a * bb
print("MC", c[0] / N, c[1] / N, c[2] / N, c[3] / N - (c[2] / N) ** 2, c[4] / N - (c[2] / N) * .5)
# triangle inequality caveat: a > b/2  <=> L > 2b
print("P(triangle valid, L>2b)=", sp.integrate(sp.integrate(sp.Piecewise((1, u + 1 > 2 * b), (0, True)), (u, 0, 1)), (b, 0, 1)))

print("== Q2 two-digit")
nums = [(x, y) for x in range(1, 10) for y in range(1, 10) if x != y]
def prob(f, space=nums): return F(sum(1 for t in space if f(t)), len(space))
print("odd", prob(lambda t: t[1] % 2 == 1))
print("div3", prob(lambda t: (10 * t[0] + t[1]) % 3 == 0))
print("div5", prob(lambda t: (10 * t[0] + t[1]) % 5 == 0))
ev = [t for t in nums if (t[0] + t[1]) % 2 == 0]
print("odd|sum even", prob(lambda t: t[1] % 2 == 1, ev))
c = [0, 0, 0, 0]
for _ in range(N):
    x, y = random.sample(range(1, 10), 2)
    n = 10 * x + y
    c[0] += y % 2; c[1] += n % 3 == 0; c[2] += n % 5 == 0
    if (x + y) % 2 == 0:
        c[3] += 1
        # count odd inside evens separately
print("MC odd, div3, div5:", c[0] / N, c[1] / N, c[2] / N)
k = tot = 0
for _ in range(N):
    x, y = random.sample(range(1, 10), 2)
    if (x + y) % 2 == 0:
        tot += 1; k += y % 2
print("MC odd|even sum", k / tot)

print("== Q3 Bernoulli matrix")
p = sp.symbols('p')
joint = {}
for X, Y in itertools.product([0, 1], repeat=2):
    Q = sp.Matrix([[X * Y, -X], [Y, X + Y - X * Y]])
    key = (Q.det(), Q.trace())
    w = (p if X else 1 - p) * (p if Y else 1 - p)
    joint[key] = joint.get(key, 0) + w
for k_, v in sorted(joint.items()):
    print("(D,T)=", k_, sp.factor(v))
pD, pT = {}, {}
for (d, t), v in joint.items():
    pD[d] = pD.get(d, 0) + v; pT[t] = pT.get(t, 0) + v
print("D marg", {k_: sp.factor(v) for k_, v in pD.items()})
print("T marg", {k_: sp.factor(v) for k_, v in pT.items()})
indep = all(sp.simplify(joint.get((d, t), 0) - pD[d] * pT[t]) == 0 for d in pD for t in pT)
print("independent?", indep)
ED = sum(d * v for d, v in pD.items()); ET = sum(t * v for t, v in pT.items())
EDT = sum(d * t * v for (d, t), v in joint.items())
print("cov(D,T)=", sp.factor(sp.simplify(EDT - ED * ET)))

print("== Q4 pdf")
a_, b_ = sp.symbols('a b', positive=True)
area = a_ / 2 + (b_ - a_)
mean = sp.integrate(sp.Symbol('x') * sp.Symbol('x') / a_, (sp.Symbol('x'), 0, a_)) + sp.integrate(sp.Symbol('x'), (sp.Symbol('x'), a_, b_))
sol = sp.solve([area - 1, mean - sp.Rational(23, 24)], [a_, b_], dict=True)
print(sol)
x, t = sp.symbols('x t')
for s in sol:
    av, bv = s[a_], s[b_]
    if av <= 0 or bv < av: continue
    f1 = x / av
    Fa = sp.integrate(f1, (x, 0, av)); print("valid", av, bv, "F(a)=", Fa, "F(b)=", 1)
    def Fx(tt):
        if tt <= 0: return 0
        if tt <= av: return tt ** 2 / (2 * av)
        if tt <= bv: return av / 2 + (tt - av)
        return 1
    P = Fx(sp.Rational(5, 4)) - Fx(sp.Rational(1, 2))
    print("P(X<=5/4 | X>1/2)=", sp.nsimplify(P / (1 - Fx(sp.Rational(1, 2)))), " F pieces: t^2/(2a), t-a/2, ...")
    # MC via inverse transform by rejection
    cnt = tot = 0
    avf, bvf = float(av), float(bv)
    for _ in range(N):
        xx = random.uniform(0, bvf)
        h = xx / avf if xx < avf else 1
        if random.random() < h:
            if xx > .5:
                tot += 1; cnt += xx <= 1.25
    print("MC", cnt / tot)

print("== Q5 circuits (own structure functions)")
def Q1(A, B, C, D, E):   # bridge: A-B top, C-D bottom, E vertical middle
    return (A and B) or (C and D) or (A and E and D) or (C and E and B)
def Q2(A, B, C, D, E):
    return (A or B) and (C or D or E)
P1 = P2 = P12 = 0
for st in itertools.product([0, 1], repeat=5):
    w = sp.Integer(1)
    for s in st: w *= p if s else 1 - p
    q1, q2 = bool(Q1(*st)), bool(Q2(*st))
    P1 += w * int(q1); P2 += w * int(q2); P12 += w * int(q1 and q2)
print("P(Q1)=", sp.factor(sp.expand(P1)), " expanded ", sp.expand(P1))
print("P(Q2)=", sp.factor(sp.expand(P2)), " expanded ", sp.expand(P2))
print("P(Q1 and Q2)=", sp.factor(sp.expand(P12)))
print("P(Q1|Q2)=", sp.factor(sp.simplify(P12 / P2)))
print("p=.7:", float(P1.subs(p, .7)), float(P2.subs(p, .7)), float((P12 / P2).subs(p, .7)))
c = [0, 0, 0]
pp = .7
for _ in range(N):
    st = [random.random() < pp for _ in range(5)]
    q1, q2 = bool(Q1(*st)), bool(Q2(*st))
    c[0] += q1; c[1] += q2; c[2] += q1 and q2
print("MC p=.7:", c[0] / N, c[1] / N, c[2] / c[1])

print("== Q6 families")
n = sp.symbols('n1:4')
print("E[X]=sum n_i/N; E[Y]=sum n_i^2/sum n_i;  E[Y]-E[X] = N*var/ sum n_i (>=0)")
for ns in [(1, 2, 3), (2, 5, 9, 11)]:
    EX = F(sum(ns), len(ns)); EY = F(sum(m * m for m in ns), sum(ns))
    print(ns, EX, EY, EY > EX, "check identity", EY - EX == F(len(ns) * sum((m - EX) ** 2 for m in ns) / len(ns), sum(ns)))
