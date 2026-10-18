"""Independent refuter derivations for 25S-A (own code)."""
import itertools, math, random
from fractions import Fraction as Fr
from math import comb
import sympy as sp

random.seed(21)
print("== Q1 grasshopper X1~U(0,1), X2~U(0,2) ==")
x, y = sp.symbols('x y', positive=True)
dens = sp.Rational(1, 2)
a1 = sp.integrate(dens*sp.integrate(1, (y, 0, x)), (x, 0, 1))
b1 = 1-sp.Rational(1, 2)*sp.Rational(3, 4)
c1 = sp.integrate(dens*sp.integrate(1, (y, 0, 1-x)), (x, 0, 1))
Psum2 = sp.integrate(dens*sp.integrate(1, (y, 2-x, 2)), (x, 0, 1))
Pj = sp.integrate(dens*sp.integrate(1, (y, 2-x, 2)), (x, sp.Rational(1, 2), 1))
print("P(X1>X2)", a1, " P(any<1/2)", b1, " P(sum<=1)", c1, " P(sum>2)", Psum2, " cond", Pj/Psum2)
N = 2_000_000; c = [0]*6
for _ in range(N):
    u = random.random(); v = 2*random.random()
    c[0] += u > v; c[1] += (u < .5 or v < .5); c[2] += u+v <= 1; c[3] += u+v > 2; c[4] += (u+v > 2 and u > .5)
print("MC", c[0]/N, c[1]/N, c[2]/N, c[4]/c[3])
# region areas for pictured events (on [0,1]x[0,2]): (b) x<1/2 or y<1/2
# area of union = 1*2 - area(x>=.5 & y>=.5) = 2 - .5*1.5 = 1.25 -> /2 = .625
print("union area", 2-.5*1.5, "prob", (2-.5*1.5)/2)

print("== Q2 ==")
p, q, s = sp.symbols('p q s', positive=True)
PB = q/s
PA = p+q
print("P(A)", PA, " P(B)", PB)
print("P(A|~B)", sp.simplify(p/(1-PB)), "  P(~A|B)", sp.simplify(1-s))
PAuB = p+PB
print("P(AuB)", sp.simplify(PAuB), "  P(~A|~B)", sp.simplify((1-PAuB)/(1-PB)))
print("s<q possible? P(B)=q/s<=1 => s>=q. (s<q needs P(B)>1) -> impossible")
print("independent:", sp.solve(sp.Eq(q, PA*PB), s))
# MC table at p=.2,q=.3,s=.6 -> P(B)=.5, P(A)=.5
pv, qv, sv = .2, .3, .6
PBv = qv/sv
joint = {(1, 1): qv, (1, 0): pv, (0, 1): PBv-qv, (0, 0): 1-pv-PBv}
assert min(joint.values()) >= 0
cs = {k: 0 for k in joint}
for _ in range(1_000_000):
    u = random.random(); acc = 0
    for k, w in joint.items():
        acc += w
        if u < acc: cs[k] += 1; break
B = cs[(1, 1)]+cs[(0, 1)]; nB = cs[(1, 0)]+cs[(0, 0)]
print("MC P(A|B)", cs[(1, 1)]/B, "(s=.6); P(A|~B)", cs[(1, 0)]/nB, "exact", pv*sv/(sv-qv), "; P(~A|~B)", cs[(0, 0)]/nB, "exact", (sv-pv*sv-qv)/(sv-qv))
# independence case: s=p+q: choose p=.2,q=.3 -> s=.5 -> P(B)=.6, P(A)=.5, P(AB)=.3 = .5*.6 ok
print("indep check:", .3, .5*(.3/.5))

print("== Q3 urn ==")
for Nn, D, n in [(7, 3, 3), (6, 2, 2), (8, 5, 4), (7, 4, 7)]:
    balls = [1]*D+[0]*(Nn-D)
    tot = Rn = Rl2 = 0
    for perm in itertools.permutations(range(Nn), n):
        tot += 1
        Rn += balls[perm[-1]]
        if n >= 2: Rl2 += balls[perm[-1]]*balls[perm[-2]]
    print(Nn, D, n, "P(R_n)", Fr(Rn, tot), Fr(D, Nn), "P(last two red)", Fr(Rl2, tot), Fr(D*(D-1), Nn*(Nn-1)))

print("== Q4 ==")
a, b, cc = sp.symbols('a b c', positive=True)
X = sp.symbols('X', positive=True)
f1 = cc/(2*a)*X; f2 = cc
P1 = sp.integrate(f1, (X, 0, a)); P2 = sp.integrate(f2, (X, a, b))
E = sp.integrate(X*f1, (X, 0, a))+sp.integrate(X*f2, (X, a, b))
sol = sp.solve([sp.Eq(P1, P2), sp.Eq(P1+P2, 1), sp.Eq(E, sp.Rational(43, 48))], [a, b, cc], dict=True)
print(sol)
S = sol[0]
t = sp.symbols('t', real=True)
Fa = sp.integrate((f1.subs(S)).subs(X, sp.Symbol('u')), (sp.Symbol('u'), 0, t))
Fb = P1.subs(S)+sp.integrate(f2.subs(S), (X, S[a], t))
print("F on [0,a):", sp.simplify(Fa), " on [a,b):", sp.expand(Fb), " F(b)=", Fb.subs(t, S[b]), " P(X>1)=", 1-Fb.subs(t, 1) if S[a] <= 1 else None)
# MC
random.seed(5); n = 1_000_000; sm = 0; gt = 0
av, bv, cv = float(S[a]), float(S[b]), float(S[cc])
for _ in range(n):
    u = random.random()
    if u < .5: xv = av*math.sqrt(random.random())          # density 2*(x/a^2) ... rising part has mass 1/2: pdf (x/a)*(c/(2)) c=2/a -> x/a^2 ; cdf (x/a)^2*0.5
    else: xv = av+(bv-av)*random.random()
    sm += xv; gt += xv > 1
print("MC mean", sm/n, "(43/48=%.5f)" % (43/48), "P(X>1)", gt/n)

print("== Q5 roads ==")
P = sp.symbols('p')
edges = {'A': ('E', 'H'), 'B': ('H', 'S'), 'C': ('E', 'Pb'), 'D': ('S', 'Pb')}
def reach(up, src, dst):
    adj = {}
    for k in up:
        u, v = edges[k]; adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    seen = {src}; st = [src]
    while st:
        u = st.pop()
        for w in adj.get(u, ()):
            if w not in seen: seen.add(w); st.append(w)
    return dst in seen
names = list('ABCD')
res = {'P1': 0, 'P2': 0, 'P3': 0}
both = 0
for bits in itertools.product([0, 1], repeat=4):
    up = [n for n, bt in zip(names, bits) if bt]
    w = 1
    for bt in bits: w *= P if bt else 1-P
    e = int(reach(up, 'E', 'H')); s_ = int(reach(up, 'S', 'H'))
    res['P1'] += w*e; res['P2'] += w*(e*s_); res['P3'] += w*(e*(1-s_))
for k in res: print(k, sp.factor(sp.expand(res[k])), "  expanded:", sp.expand(res[k]))
# P4: given both reach, prob both drive via the pub. interpretations:
# I1: both are FORCED via the pub (A and B closed, C,D open) -- the only way each can reach via pub
# I2: Eugene's only route is via pub (A closed) and Serge's only route via pub (B closed)
# enumerate which up-sets give both reaching, and classify who must use the pub
import collections
cnt = collections.defaultdict(lambda: 0)
for bits in itertools.product([0, 1], repeat=4):
    up = [n for n, bt in zip(names, bits) if bt]
    w = 1
    for bt in bits: w *= P if bt else 1-P
    e = int(reach(up, 'E', 'H')); s_ = int(reach(up, 'S', 'H'))
    if e and s_:
        eng_pub_forced = 'A' not in up   # Eugene must go through pub (A closed)
        ser_pub_forced = 'B' not in up
        cnt[(eng_pub_forced, ser_pub_forced)] += w
        print(bits, "E forced via pub:", eng_pub_forced, " S forced via pub:", ser_pub_forced)
den = sp.expand(res['P2'])
for k, v in cnt.items(): print(k, sp.factor(sp.simplify(v/den)))
