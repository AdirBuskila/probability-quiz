"""Independent refuter derivations for 25A-C (own code, no author helpers)."""
import itertools, math, random
import sympy as sp

x, y, t = sp.symbols('x y t', positive=True)
print("== Q1 ==")
# X~U(0,1), Y~U(0,2): density 1/2 on [0,1]x[0,2]; S=XY, L=2(X+Y)
# P(S<2/3) = 1 - P(XY>=2/3) ; XY>=2/3 -> y>=2/(3x), need 2/(3x)<=2 -> x>=1/3
PS = 1 - sp.integrate(sp.Rational(1, 2)*(2 - sp.Rational(2, 3)/x), (x, sp.Rational(1, 3), 1))
print("P(S<2/3)", sp.simplify(PS), float(PS))
# P(L<2): X+Y<1 ; area 1/2 *density 1/2
PL = sp.integrate(sp.Rational(1, 2)*(1 - x), (x, 0, 1))
print("P(L<2)", PL)
# P(L>2)=1-PL ; P(S<2/3 and L>2) = P(S<2/3) - P(S<2/3 and L<=2); L<2 => x+y<1 => xy<1/4<2/3 so all
cond = (PS - PL)/(1 - PL)
print("P(S<2/3|L>2)", sp.simplify(cond), float(cond))
EX, EY = sp.Rational(1, 2), 1
vX, vY = sp.Rational(1, 12), sp.Rational(4, 12)
print("E L, var L", 2*(EX+EY), 4*(vX+vY))
ES = EX*EY
ES2 = sp.Rational(1, 3)*sp.Rational(4, 3)
print("E S, var S", ES, sp.simplify(ES2-ES**2))
random.seed(1)
N = 2_000_000
c = [0]*6
sums = [0, 0, 0, 0]
for _ in range(N):
    X = random.random(); Y = 2*random.random(); S = X*Y; L = 2*(X+Y)
    c[0] += S < 2/3; c[1] += L < 2; c[2] += (L > 2 and S < 2/3); c[3] += L > 2
    sums[0] += L; sums[1] += L*L; sums[2] += S; sums[3] += S*S
print("MC P(S<2/3)", c[0]/N, "P(L<2)", c[1]/N, "cond", c[2]/c[3])
EL = sums[0]/N; print("MC E L", EL, "var L", sums[1]/N-EL**2)
ESm = sums[2]/N; print("MC E S", ESm, "var S", sums[3]/N-ESm**2)

print("== Q2 ==")
p, q, s = sp.symbols('p q s')
PAB = p+q-s
print("P(A|B)", sp.simplify(PAB/q))
print("P(B|~A)", sp.simplify((q-PAB)/(1-p)))
print("P(A|~B)", sp.simplify((p-PAB)/(1-q)))
print("P(~A|~B)", sp.simplify((1-s)/(1-q)))
print("indep: s=", sp.solve(sp.Eq(PAB, p*q), s))
print("disjoint: s=", sp.solve(sp.Eq(PAB, 0), s))
# MC on a random table
random.seed(2)
pv, qv, inter = 0.5, 0.4, 0.3
M = 1_000_000; n = [0]*5
for _ in range(M):
    u = random.random()
    # joint: A&B .3, A only .2, B only .1, neither .4
    A = u < .5; B = (u < .3) or (.5 <= u < .6)
    n[0] += B; n[1] += (A and B); n[2] += (not A); n[3] += ((not A) and B); n[4] += (not A and not B)
print("MC P(A|B)", n[1]/n[0], "exact", .3/.4, "P(B|~A)", n[3]/n[2], "exact", .1/.5, "P(~A|~B) approx", n[4]/(M-n[0]), .4/.6)

print("== Q3 ==")
a, b = sp.symbols('a b')
sol = sp.solve([sp.integrate(a*(1+x), (x, -1, 0)) + sp.integrate(b*sp.exp(-x), (x, 0, sp.oo)) - 1,
                sp.integrate(x*a*(1+x), (x, -1, 0)) + sp.integrate(x*b*sp.exp(-x), (x, 0, sp.oo))], [a, b])
print(sol)
A_, B_ = sol[a], sol[b]
tt = sp.symbols('tt', real=True)
F1 = sp.integrate(A_*(1+x), (x, -1, tt))
F2 = sp.integrate(A_*(1+x), (x, -1, 0)) + sp.integrate(B_*sp.exp(-x), (x, 0, tt))
print("F on [-1,0):", sp.expand(F1), " F on t>=0:", sp.simplify(F2))
Fn = lambda v: float(F1.subs(tt, v)) if v < 0 else float(F2.subs(tt, v))
cond3 = (Fn(0.5) - Fn(-0.5))/(1-Fn(-0.5))
print("P(X<1/2|X>-1/2)", cond3, "claim 1-(4/13)e^-1/2 =", 1-4/13*math.exp(-.5))
# MC by inverse transform: sample with rejection
random.seed(3)
cnt = tot = 0
for _ in range(1_000_000):
    # left piece prob 3/4 of mass? mass left = a/2
    if random.random() < float(A_/2):
        X = -1 + math.sqrt(random.random())
    else:
        X = -math.log(random.random())
    if X > -.5:
        tot += 1; cnt += X < .5
print("MC", cnt/tot)

print("== Q4 == circuits")
# nodes: L, T1, B1, T2, B2, O ; edges with units
units = {'A': ('L', 'T1'), 'B': ('L', 'B1'), 'E': ('T1', 'B1'), 'C': ('T1', 'T2'), 'D': ('B1', 'B2'),
         'F': ('T2', 'B2'), 'G': ('T2', 'O'), 'H': ('B2', 'O')}

def connected(up, nodes_edges):
    adj = {}
    for k in up:
        u, v = units[k]; adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    seen = {'L'}; st = ['L']
    while st:
        u = st.pop()
        for w in adj.get(u, ()):
            if w not in seen: seen.add(w); st.append(w)
    return 'O' in seen

P, Q = sp.symbols('p q')
names1 = list('ABCDEFG'); names2 = names1 + ['H']

def prob(names, hasH):
    tot = 0
    for bits in itertools.product([0, 1], repeat=len(names)):
        up = [n for n, bt in zip(names, bits) if bt]
        if hasH:
            ok = connected(up, None)
        else:
            ok = connected([u for u in up if u != 'H'], None)
        if ok:
            w = 1
            for n, bt in zip(names, bits):
                pr = Q if n == 'H' else P
                w *= pr if bt else 1-pr
            tot += w
    return sp.expand(tot)

# Q1 does not include H: Q1 uses G->O with no H edge.  Build Q1 by excluding H from graph.
def prob_Q1():
    tot = 0
    for bits in itertools.product([0, 1], repeat=7):
        up = [n for n, bt in zip(names1, bits) if bt]
        if connected(up, None):
            w = 1
            for bt in bits: w *= P if bt else 1-P
            tot += w
    return sp.expand(tot)
Q1p = prob_Q1()
Q2p = prob(names2, True)
print("Q1:", sp.factor(Q1p), "\n   expanded", Q1p)
print("Q2:", Q2p)
print("Q2 = Q1*? check: ", sp.factor(Q2p))
# Q2 works iff Q1-like (with G alone) or with H as alt route from B2
# at least one: P(Q1 or Q2) -- Q1 works => Q2 works (more edges)
print("P(Q1 or Q2) = P(Q2) =", Q2p)
# but they're not independent units? Q1 and Q2 share units?  The text: Q2 is Q1 with H added -> Q1 works implies Q2 works.
print("P(Q2|Q1) = 1  (Q1 works => Q2 works)")
# MC
random.seed(5)
pv, qv = 0.6, 0.7
M = 400_000
c1 = c2 = 0
for _ in range(M):
    up = [n for n in names1 if random.random() < pv]
    h = random.random() < qv
    w1 = connected(up, None)
    w2 = connected(up + (['H'] if h else []), None)
    c1 += w1; c2 += w2
    assert (not w1) or w2
print("MC Q1", c1/M, "exact", float(Q1p.subs(P, pv)), " MC Q2", c2/M, "exact", float(Q2p.subs({P: pv, Q: qv})))
print("Q2 numeric 0.6,0.7 unreduced", Q2p.subs({P: .6, Q: .7}))
