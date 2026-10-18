import itertools, random
from fractions import Fraction as Fr
from math import comb
import sympy as sp

p = sp.symbols('p')
print("== Q6 grid: m cells wide, n tall; corners = lattice points (0,0) -> (m,n) ==")
for m, n in [(3, 2), (5, 4), (4, 4)]:
    tot = 0; paths = []
    for steps in itertools.product('RU', repeat=m+n):
        if steps.count('R') == m:
            w = p**m*(1-p)**n
            tot += w; paths.append(steps)
    print(m, n, "#paths", len(paths), comb(m+n, m), " P(reach)", sp.factor(tot), " claim C(m+n,m)p^m(1-p)^n", sp.simplify(tot-comb(m+n, m)*p**m*(1-p)**n))
    # through point (X,Y): count paths through lattice point
    for X, Y in [(2, 1), (3, 2), (1, 1), (0, 0), (m, n)]:
        if X > m or Y > n: continue
        thr = 0
        for steps in paths:
            xx = yy = 0; hit = (xx, yy) == (X, Y)
            for st in steps:
                if st == 'R': xx += 1
                else: yy += 1
                hit |= (xx, yy) == (X, Y)
            thr += hit
        claim = Fr(comb(X+Y, X)*comb(m+n-X-Y, m-X), comb(m+n, m))
        print("   (X,Y)=", (X, Y), "frac of paths", Fr(thr, len(paths)), "claim", claim)
# MC: probability through (X,Y) given reached, two different p
random.seed(9)
m, n, X, Y = 5, 4, 3, 2
for pv in (.3, .7):
    reach = thr = 0
    for _ in range(600000):
        xx = yy = 0; hit = False
        for _s in range(m+n):
            if random.random() < pv: xx += 1
            else: yy += 1
            if (xx, yy) == (X, Y): hit = True
        if (xx, yy) == (m, n):
            reach += 1; thr += hit
    print("p", pv, "MC P(reach)", reach/600000, "exact", comb(m+n, m)*pv**m*(1-pv)**n, " P(thru|reach)", thr/reach, "exact", comb(X+Y, X)*comb(m+n-X-Y, m-X)/comb(m+n, m))
