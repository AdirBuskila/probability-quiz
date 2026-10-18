# Refuter's own derivation for 25S-B (independent of steps_lib / probsteps). Exact + Monte Carlo.
import itertools, random, math
from fractions import Fraction as F
import sympy as sp

random.seed(2)
N = 400000
p, lam, x = sp.symbols('p lambda x', positive=True)

print("== Q1 clock, u=a1/pi, v=a2/pi uniform on unit square")
u, v = sp.symbols('u v')
# P(v>2u)
P1 = sp.integrate(v / 2, (v, 0, 1))
# P(|u-v|<1/2) = 1 - 2*(1/2)(1/2)^2
P2 = 1 - 2 * sp.Rational(1, 2) * sp.Rational(1, 4)
# joint: u<v/2 and v-u<1/2 and u>=0
J = sp.integrate(sp.Piecewise((v / 2 - sp.Max(0, v - sp.Rational(1, 2)), True)), (v, 0, 1))
print("P(a2>2a1)", P1, " P(acute)", P2, " joint", J, " cond", J / P1)
c = [0, 0, 0]
for _ in range(N):
    a1, a2 = random.uniform(0, math.pi), random.uniform(0, math.pi)
    e = a2 > 2 * a1; ac = abs(a1 - a2) < math.pi / 2
    c[0] += e; c[1] += ac; c[2] += e and ac
print("MC", c[0] / N, c[1] / N, c[2] / c[0])

print("== Q2 numbers 1..2n+1")
def q2(n, repl):
    nums = list(range(1, 2 * n + 2))
    pairs = [(a, b) for a in nums for b in nums if repl or a != b]
    pe = F(sum(1 for a in nums if a % 2 == 0), len(nums))
    ps = F(sum(1 for a, b in pairs if (a + b) % 2 == 0), len(pairs))
    given = [t for t in pairs if t[0] % 2 == 0]
    pc = F(sum(1 for a, b in given if (a + b) % 2 == 0), len(given))
    return pe, ps, pc
for n in [1, 2, 3, 5, 10]:
    print("N=", n, "no-repl", q2(n, False), "repl", q2(n, True), " N/(2N+1)=", F(n, 2 * n + 1), " (N-1)/(2N)=", F(n - 1, 2 * n))

print("== Q3 restaurant: X~Poisson(lam), Y|X~Bin(X,p)")
k, n = sp.symbols('k n', integer=True, nonnegative=True)
# numeric check for lam=3, p=.4
lv, pv = 3.0, 0.4
def pois(m, l): return math.exp(-l) * l ** m / math.factorial(m)
def pY(kk): return sum(pois(nn, lv) * math.comb(nn, kk) * pv ** kk * (1 - pv) ** (nn - kk) for nn in range(kk, 120))
print("P(Y=k) exact-sum vs Poisson(lam p):", [(kk, round(pY(kk), 8), round(pois(kk, lv * pv), 8)) for kk in range(4)])
def pn_k(nn, kk): return pois(nn, lv) * math.comb(nn, kk) * pv ** kk * (1 - pv) ** (nn - kk) / pY(kk)
print("P(X=n|Y=k) vs Poisson(lam(1-p)) shifted:", [(nn, round(pn_k(nn, 2), 8), round(pois(nn - 2, lv * (1 - pv)), 8)) for nn in range(2, 6)])
cnt = {}
tot = 0
for _ in range(N):
    # sample poisson
    L = math.exp(-lv); kk = 0; pr = 1
    while True:
        pr *= random.random()
        if pr <= L: break
        kk += 1
    y = sum(random.random() < pv for _ in range(kk))
    cnt[y] = cnt.get(y, 0) + 1
print("MC P(Y=k)", [(kk, cnt.get(kk, 0) / N) for kk in range(4)])
print("identity sum x^n/(n-k)! = x^k e^x check k=2,x=.7:", sum(0.7 ** nn / math.factorial(nn - 2) for nn in range(2, 80)), 0.7 ** 2 * math.exp(0.7))

print("== Q4 pdf a + b x^{-3/2} + c x on (0,1]")
a, b, c_, mu = sp.symbols('a b c mu')
print("int_0^1 x^{-3/2} dx diverges:", sp.integrate(x ** sp.Rational(-3, 2), (x, 0, 1)))
a_s = 1 - c_ / 2
mu_s = sp.integrate(x * (a_s + c_ * x), (x, 0, 1))
print("a=", a_s, " mu(c)=", sp.simplify(mu_s))
cs = sp.solve(sp.Eq(mu_s, mu), c_)[0]
print("c(mu)=", cs, " a(mu)=", sp.simplify(a_s.subs(c_, cs)))
# nonneg: f(0)=a>=0 -> c<=2 ; f(1)=a+c>=0 -> c>=-2 ; f linear so these suffice
print("mu range", mu_s.subs(c_, -2), mu_s.subs(c_, 2))
Pleq = sp.integrate(a_s + c_ * x, (x, 0, sp.Rational(1, 2)))
print("P(X<=1/2)=", sp.simplify(Pleq), " in mu:", sp.simplify(Pleq.subs(c_, cs)))
# MC for mu=0.5 (c=0), mu=.6 (c=1.2): P(X<=1/2) = 1/2 - c/8
for cv in [0, 1.2, -1.5]:
    av = 1 - cv / 2; cnt = 0; tt = 0
    for _ in range(N):
        xx = random.random()
        if random.random() * max(av, av + cv) < av + cv * xx:
            tt += 1; cnt += xx <= .5
    print("c=", cv, "MC P(X<=1/2)", cnt / tt, "exact", .5 - cv / 8, " MC mean?")

print("== Q5 circuits")
def C1(A, B, C, D): return D and ((A and B) or C)
def C2(A, B, C, D): return B and (D or (A and C))
Pa = Pb = Pab = Pall = 0
for st in itertools.product([0, 1], repeat=4):
    w = sp.Integer(1)
    for s in st: w *= p if s else 1 - p
    c1, c2 = bool(C1(*st)), bool(C2(*st))
    Pa += w * int(c1); Pb += w * int(c2); Pab += w * int(c1 and c2); Pall += w * int(all(st))
print("P(C1)=", sp.factor(sp.expand(Pa)), sp.expand(Pa))
print("P(C2)=", sp.factor(sp.expand(Pb)), sp.expand(Pb))
print("P(both)=", sp.factor(sp.expand(Pab)), sp.expand(Pab))
print("P(all|both)=", sp.factor(sp.simplify(Pall / Pab)))
pp = .6
c = [0, 0, 0, 0]
for _ in range(N):
    st = [random.random() < pp for _ in range(4)]
    c1, c2 = bool(C1(*st)), bool(C2(*st))
    c[0] += c1; c[1] += c2; c[2] += c1 and c2; c[3] += c1 and c2 and all(st)
print("p=.6 exact", [float(e.subs(p, pp)) for e in (Pa, Pb, Pab)], float((Pall / Pab).subs(p, pp)))
print("p=.6 MC", c[0] / N, c[1] / N, c[2] / N, c[3] / c[2])

print("== Q6 dice min/max")
for Nf in [3, 4, 6]:
    pm = {}
    for a1, a2 in itertools.product(range(1, Nf + 1), repeat=2):
        key = (min(a1, a2), max(a1, a2)); pm[key] = pm.get(key, 0) + F(1, Nf * Nf)
    mn = {kk: sum(v_ for (a_, b_), v_ in pm.items() if a_ == kk) for kk in range(1, Nf + 1)}
    mx = {kk: sum(v_ for (a_, b_), v_ in pm.items() if b_ == kk) for kk in range(1, Nf + 1)}
    ok_mn = all(mn[kk] == F(2 * (Nf - kk) + 1, Nf * Nf) for kk in mn)
    ok_mx = all(mx[kk] == F(2 * kk - 1, Nf * Nf) for kk in mx)
    ok_j = all(pm[(a_, b_)] == (F(2, Nf * Nf) if a_ < b_ else F(1, Nf * Nf)) for (a_, b_) in pm)
    dep = any(pm.get((a_, b_), 0) != mn[a_] * mx[b_] for a_ in mn for b_ in mx)
    print("N=", Nf, "joint ok", ok_j, "min marg ok", ok_mn, "max marg ok", ok_mx, "dependent", dep, " P(min=2,max=1)=", pm.get((2, 1), 0), mn[2] * mx[1])
