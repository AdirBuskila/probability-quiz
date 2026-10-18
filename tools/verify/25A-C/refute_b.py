import itertools, random
from fractions import Fraction as Fr
from math import comb

# Q5: brute force over all n-subsets of {1..N}
for N, n in [(6, 3), (7, 2), (8, 4), (5, 5)]:
    subs = list(itertools.combinations(range(1, N+1), n))
    T = len(subs)
    pmin = {}; pmax = {}; joint = {}
    for s in subs:
        pmin[s[0]] = pmin.get(s[0], 0)+1; pmax[s[-1]] = pmax.get(s[-1], 0)+1
        joint[(s[0], s[-1])] = joint.get((s[0], s[-1]), 0)+1
    ok = True
    for k in range(1, N+1):
        ok &= Fr(pmin.get(k, 0), T) == Fr(comb(N-k, n-1), comb(N, n))
        ok &= Fr(pmax.get(k, 0), T) == Fr(comb(k-1, n-1), comb(N, n))
    for (k, l), c in joint.items():
        ok &= Fr(c, T) == (Fr(comb(l-k-1, n-2), comb(N, n)) if n >= 2 else None)
    Emin = sum(Fr(s[0]) for s in subs)/T; Emax = sum(Fr(s[-1]) for s in subs)/T
    print(N, n, ok, "support min 1..", N-n+1, sorted(pmin)[-1], "max from", sorted(pmax)[0],
          "Emin", Emin, Fr(N+1, n+1), "Emax", Emax, Fr(n*(N+1), n+1))
# MC check of expectations
random.seed(1); N, n = 20, 6; M = 300000; a = b = 0
for _ in range(M):
    s = random.sample(range(1, N+1), n); a += min(s); b += max(s)
print("MC", a/M, (N+1)/(n+1), b/M, n*(N+1)/(n+1))

# Q6: Z=min/max of two iid U(0,L)
random.seed(2); M = 1000000; Lv = 3.7
zs = []
for _ in range(M):
    u, v = random.random()*Lv, random.random()*Lv
    zs.append(min(u, v)/max(u, v))
for t in (.1, .25, .5, .9):
    print("F(t)", t, sum(z <= t for z in zs)/M)
m = sum(zs)/M; print("E", m, "var", sum(z*z for z in zs)/M-m*m, "expected 1/2, 1/12=", 1/12)
import sympy as sp
t, x, y = sp.symbols('t x y', positive=True)
print("exact F(t) =", sp.integrate(2*sp.integrate(1, (x, 0, t*y)), (y, 0, 1)))
