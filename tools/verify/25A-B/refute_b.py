import itertools, random
from fractions import Fraction as Fr
from math import comb
import sympy as sp

print("== Q4 circuits ==")
# Q1: L -A- T1, L -B- B1, T1 -E- B1, T1 -C- O, B1 -D- O.
# Q2: same but C->T2, D->B2, F: T2-B2, G: T2-O  (G in series after the C/F junction)
e1 = {'A': ('L', 'T1'), 'B': ('L', 'B1'), 'E': ('T1', 'B1'), 'C': ('T1', 'O'), 'D': ('B1', 'O')}
e2 = {'A': ('L', 'T1'), 'B': ('L', 'B1'), 'E': ('T1', 'B1'), 'C': ('T1', 'T2'), 'D': ('B1', 'B2'),
      'F': ('T2', 'B2'), 'G': ('T2', 'O')}

def conn(edges, up):
    adj = {}
    for k in up:
        u, v = edges[k]; adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    seen = {'L'}; st = ['L']
    while st:
        u = st.pop()
        for w in adj.get(u, ()):
            if w not in seen: seen.add(w); st.append(w)
    return 'O' in seen

p, q = sp.symbols('p q')
names = list('ABCDEFG')
pr = {n: (p if n in 'ABCDE' else q) for n in names}
tot1 = tot2 = totb = totu = 0
for bits in itertools.product([0, 1], repeat=7):
    up = [n for n, b in zip(names, bits) if b]
    w = 1
    for n, b in zip(names, bits): w *= pr[n] if b else 1-pr[n]
    w1 = int(conn(e1, [u for u in up if u in e1])); w2 = int(conn(e2, up))
    tot1 += w*w1; tot2 += w*w2; totb += w*(w1*w2); totu += w*max(w1, w2)
Q1, Q2, Qb, Qu = [sp.expand(v) for v in (tot1, tot2, totb, totu)]
print("P(Q1)=", sp.factor(Q1)); print("P(Q2)=", Q2); print("P(Q1&Q2)=", Qb)
print("P(Q2|Q1)=", sp.factor(sp.simplify(Qb/Q1)))
print("Q1 subset Q2? P(Q1 & ~Q2) =", sp.simplify(Q1-Qb))
for pv, qv in [(.5, .4), (.5, .5), (.7, .3)]:
    print(pv, qv, "Q1", float(Q1.subs(p, pv)), "Q2", float(Q2.subs({p: pv, q: qv})), "both", float(Qb.subs({p: pv, q: qv})),
          "cond", float((Qb/Q1).subs({p: pv, q: qv})))
# MC
random.seed(3); pv, qv = .6, .7; M = 600000; c1 = c2 = cb = 0
for _ in range(M):
    up = [n for n in names if random.random() < (pv if n in 'ABCDE' else qv)]
    w1 = int(conn(e1, [u for u in up if u in e1])); w2 = int(conn(e2, up))
    c1 += w1; c2 += w2; cb += w1 and w2
print("MC", c1/M, c2/M, cb/M, "cond", cb/c1, "| exact", float(Q1.subs(p, pv)), float(Q2.subs({p: pv, q: qv})), float(Qb.subs({p: pv, q: qv})), float((Qb/Q1).subs({p: pv, q: qv})))

print("== Q5 urn ==")
for N, D, n in [(7, 3, 4), (6, 4, 3), (8, 5, 2)]:
    # enumerate ordered draws
    cnt = tot = 0; cnt2 = tot2 = 0
    balls = [1]*D+[0]*(N-D)
    from itertools import permutations
    Rn = 0; total = 0; Rn_and_next = 0
    for perm in permutations(range(N), n+1):
        total += 1
        if balls[perm[n-1]]:
            Rn += 1
            Rn_and_next += balls[perm[n]]
    print(N, D, n, "P(R_n)", Fr(Rn, total), Fr(D, N), " P(R_{n+1}|R_n)", Fr(Rn_and_next, Rn), Fr(D-1, N-1))
random.seed(4); N, D, n = 12, 5, 6; M = 400000; r = rn = 0
for _ in range(M):
    s = random.sample(range(N), n+1)
    if s[n-1] < D:
        r += 1; rn += s[n] < D
print("MC P(R_n)", r/M, D/N, "cond", rn/r, (D-1)/(N-1))

print("== Q6 chairs ==")
for N in (2, 3, 4, 5, 8):
    pairs = [(x, y) for x in range(1, N+1) for y in range(1, N+1) if x != y]
    T = len(pairs)
    L = [min(a, b) for a, b in pairs]; R = [max(a, b) for a, b in pairs]
    # marginals of X, Y
    px = {k: Fr(sum(1 for a, b in pairs if a == k), T) for k in range(1, N+1)}
    assert all(v == Fr(1, N) for v in px.values())
    EL = Fr(sum(L), T); ER = Fr(sum(R), T)
    VL = Fr(sum(v*v for v in L), T)-EL**2; VR = Fr(sum(v*v for v in R), T)-ER**2
    cov = Fr(sum(a*b for a, b in zip(L, R)), T)-EL*ER
    rho = (cov/ sp.sqrt(sp.Rational(VL.numerator, VL.denominator)*sp.Rational(VR.numerator, VR.denominator))) if VL > 0 else None
    print(N, "E", EL, ER, "claim", Fr(N+1, 3), Fr(2*(N+1), 3), "var", VL, VR, "claim", Fr((N+1)*(N-2), 18), "rho", rho)
    # joint and marginals
    for k in range(1, N+1):
        assert Fr(L.count(k), T) == Fr(2*(N-k), N*(N-1))
        assert Fr(R.count(k), T) == Fr(2*(k-1), N*(N-1))
random.seed(5); N = 9; M = 400000; ls = []; rs = []
for _ in range(M):
    a, b = random.sample(range(1, N+1), 2); ls.append(min(a, b)); rs.append(max(a, b))
import statistics as st
print("MC N=9: EL", st.mean(ls), 10/3, "var L", st.pvariance(ls), 10*7/18, "corr", st.correlation(ls, rs))
# if sitting WITH replacement allowed (X may equal Y)? the question says two people two chairs -> distinct. Check ENV: "N>=2" given -> distinct.
