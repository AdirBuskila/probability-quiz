"""Independent refuter derivations for 25B-B Q5-Q6 (own code)."""
import itertools, random
from fractions import Fraction as Fr
from math import comb
import sympy as sp

p = sp.symbols('p')
print("== Q5 circuits ==")
# Q0 = (A and B) or C. New circuit: same topology, placement uniformly random among the 3 units for the lone (parallel) slot
def Q(lone, st):
    others = [u for u in 'ABC' if u != lone]
    return (st[others[0]] and st[others[1]]) or st[lone]
res = {}
for lone in 'ABC':
    tot = 0
    for bits in itertools.product([0, 1], repeat=3):
        st = dict(zip('ABC', bits)); w = 1
        for bt in bits: w *= p if bt else 1-p
        tot += w*int(bool(Q(lone, st)))
    res[lone] = sp.expand(tot)
print("P(Q) each placement:", res)
P0 = res['C']
# joint of Q0(lone=C) with Q_new(lone): average over uniform lone in {A,B,C} (all 6 permutations -> same)
def joint(lone):
    tot = 0; tot_nq0 = 0
    for bits in itertools.product([0, 1], repeat=3):
        st = dict(zip('ABC', bits)); w = 1
        for bt in bits: w *= p if bt else 1-p
        q0 = bool(Q('C', st)); qn = bool(Q(lone, st))
        tot += w*int(q0 and qn); tot_nq0 += w*int((not q0) and qn)
    return sp.expand(tot), sp.expand(tot_nq0)
J = {l: joint(l) for l in 'ABC'}
both = sp.expand(sum(J[l][0] for l in 'ABC')/3)
nq0 = sp.expand(sum(J[l][1] for l in 'ABC')/3)
print("P(Q0 & Qnew) =", sp.factor(both), "=", both)
print("P(Qnew | Q0) =", sp.factor(sp.simplify(both/P0)))
print("P(Qnew | not Q0) =", sp.factor(sp.simplify(nq0/(1-P0))))
print("P(Qnew)  = ", sp.factor(sp.expand(sum(res.values())/3)), "(equals P(Q0): all placements same prob)")
for pv in (.5, .7):
    print("p=", pv, "both", float(both.subs(p, pv)), "cond", float((both/P0).subs(p, pv)), "|notQ0", float((nq0/(1-P0)).subs(p, pv)))
# MC
random.seed(41)
for pv in (.5, .7):
    N = 800000; c0 = cb = cn = cnq = 0
    for _ in range(N):
        st = {u: random.random() < pv for u in 'ABC'}
        lone = random.choice('ABC')
        q0 = Q('C', st); qn = Q(lone, st)
        c0 += q0; cb += q0 and qn; cnq += (not q0) and qn
    print("MC p=", pv, "both", cb/N, " cond", cb/c0, " | notQ0", cnq/(N-c0))

print("== Q6 urns ==")
def exact(N1, D1, N2, D2, n):
    # enumerate all n-subsets of urn1 (balls distinct), then draw uniformly from urn2+subset
    balls = [1]*D1+[0]*(N1-D1)
    subs = list(itertools.combinations(range(N1), n))
    pred = Fr(0); pall = Fr(0); pred_swap = Fr(0)
    for s in subs:
        r = sum(balls[i] for i in s)
        pred += Fr(1, len(subs))*Fr(D2+r, N2+n)
        pred_swap += Fr(1, len(subs))*Fr(D2+(n-r), N2+n)
        if r == n:
            pall += Fr(1, len(subs))*Fr(D2+n, N2+n)
    return pred, pall, pred_swap
for N1, D1, N2, D2, n in [(6, 2, 5, 3, 3), (7, 4, 4, 1, 2), (5, 5, 6, 2, 5), (8, 3, 3, 2, 1)]:
    pred, pall, ps = exact(N1, D1, N2, D2, n)
    claim = Fr(D2*N1+n*D1, N1*(N2+n))
    # all-red given red
    allred = Fr(comb(D1, n), comb(N1, n))*Fr(D2+n, N2+n)/pred
    claim_sw = Fr(D2*N1+n*(N1-D1), N1*(N2+n))
    print((N1, D1, N2, D2, n), "P(red)", pred, claim, "| P(all red|red)", pall/pred, allred, "| swap", ps, claim_sw)
random.seed(43)
N1, D1, N2, D2, n = 9, 4, 6, 2, 4; M = 600000; r = ar = 0; sw = 0
for _ in range(M):
    s = random.sample(range(N1), n); k = sum(1 for i in s if i < D1)
    urn2 = D2+k; tot2 = N2+n
    red = random.random() < urn2/tot2
    r += red; ar += red and k == n
    urn2s = D2+(n-k); sw += random.random() < urn2s/tot2
print("MC", r/M, (D2*N1+n*D1)/(N1*(N2+n)), "|", ar/r, comb(D1, n)/comb(N1, n)*(D2+n)/(N2+n)/((D2*N1+n*D1)/(N1*(N2+n))), "| swap", sw/M, (D2*N1+n*(N1-D1))/(N1*(N2+n)))
