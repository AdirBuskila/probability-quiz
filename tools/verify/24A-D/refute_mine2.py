import numpy as np
from math import exp, factorial
rng = np.random.default_rng(99)
M = 6_000_000
pb = 1 / 365
# Poisson mean 3.65*100 is large; use lam=730 to get P(K=2) decent, but n-k ~ Poisson(lam*364/365)
# instead check conditional law via a smaller-lam variant where the identity is the same: lam=5, birth prob 0.3
for lam, pbb in ((5.0, 0.3), (730.0, 1 / 365)):
    X = rng.poisson(lam, size=M)
    K = rng.binomial(X, pbb)
    for k in (1, 2):
        sel = K == k
        mu = lam * (1 - pbb)
        for dn in (0, 1, 2, 3):
            n = k + dn
            cl = exp(-mu) * mu**dn / factorial(dn)
            if mu > 50:
                # use log-space
                from math import lgamma, log
                cl = exp(-mu + dn * log(mu) - lgamma(dn + 1))
            print(lam, pbb, "k", k, "n", n, "MC %.5f" % (X[sel] == n).mean(), "closed %.5f" % cl)
# conditional dice C2d with more trials: conditional by direct sampling
w = np.array([1, 2, 1, 2, 1, 2]) / 9
r1 = rng.choice(6, size=M, p=w) + 1
r2 = rng.choice(6, size=M, p=w) + 1
r3 = rng.choice(6, size=M, p=w) + 1
g = r1 + r2 == 2
print("C2d MC", ((r1 + r2 + r3 == 5) & g).sum() / g.sum(), "exact", 1 / 9)
