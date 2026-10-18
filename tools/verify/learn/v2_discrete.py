# -*- coding: utf-8 -*-
"""Numbers of chapters 05-07 (discrete RV, special discrete, joint discrete)."""
import itertools
import math
from fractions import Fraction as Fr
from math import comb

import numpy as np
from scipy import stats

from common import chk, chk_eq, chk_mc, chk_mc_val, RNG


def run():
    rng = RNG
    # ---------------- chapter 05
    q = Fr(1, 9)
    pm = {1: q, 3: q, 5: q, 2: 2 * q, 4: 2 * q, 6: 2 * q}
    E = sum(x * p for x, p in pm.items()); E2 = sum(x * x * p for x, p in pm.items())
    chk("ch05 E[X]=11/3", Fr(11, 3), E); chk("ch05 E[X^2]=49/3", Fr(49, 3), E2); chk("ch05 Var=26/9", Fr(26, 9), E2 - E * E)
    # MC for the unfair die
    xs = rng.choice(list(pm.keys()), size=1_000_000, p=[float(v) for v in pm.values()])
    chk_mc_val("ch05 unfair die mean", Fr(11, 3), xs.mean(), xs.std() / 1000)
    sizes = [2, 3, 7]
    EX = Fr(sum(sizes), len(sizes)); EXsq = Fr(sum(s * s for s in sizes), len(sizes))
    EY = Fr(sum(s * s for s in sizes), sum(sizes))
    chk("ch05 E[X]=4", 4, EX); chk("ch05 E[Y]=31/6", Fr(31, 6), EY)
    chk("ch05 Var[X]=14/3", Fr(14, 3), EXsq - EX ** 2)
    chk("ch05 E[Y]/E[X] = 1+Var/E^2", EY / EX, 1 + (EXsq - EX ** 2) / EX ** 2)
    chk("ch05 31/24", Fr(31, 24), EY / EX)
    # MC for size-bias
    fam = np.repeat(sizes, sizes)
    pick = rng.choice(fam, size=1_000_000)
    chk_mc_val("ch05 E[Y] size-biased", Fr(31, 6), pick.mean(), pick.std() / 1000)
    for Nn in range(2, 9):
        pairs = list(itertools.combinations(range(1, Nn + 1), 2))
        eL = Fr(sum(a for a, b in pairs), len(pairs)); eR = Fr(sum(b for a, b in pairs), len(pairs))
        chk("ch05 E[XL]=(N+1)/3 N=%d" % Nn, Fr(Nn + 1, 3), eL)
        chk("ch05 E[XR]=2(N+1)/3 N=%d" % Nn, Fr(2 * (Nn + 1), 3), eR)
        pk = {k: Fr(Nn - k, len(pairs)) for k in range(1, Nn)}
        chk("ch05 P(XL=k) sums to 1 N=%d" % Nn, 1, sum(pk.values()))
    chk("ch05 U_d(1,6) E", Fr(7, 2), Fr(sum(range(1, 7)), 6))
    chk("ch05 U_d(1,6) Var=35/12", Fr(35, 12), Fr(sum(k * k for k in range(1, 7)), 6) - Fr(7, 2) ** 2)

    # ---------------- chapter 06
    # Bin(N,pQ) by total probability
    Nn, p, Q = 5, Fr(3, 5), Fr(1, 4)
    for k in range(Nn + 1):
        tot = sum(comb(j, k) * Q ** k * (1 - Q) ** (j - k) * comb(Nn, j) * p ** j * (1 - p) ** (Nn - j) for j in range(k, Nn + 1))
        chk("ch06 Bin(N,pQ) k=%d" % k, comb(Nn, k) * (p * Q) ** k * (1 - p * Q) ** (Nn - k), tot)
    # Bayes after binomial thinning
    pt = (1 - p) / (1 - p * Q)
    for k in range(Nn + 1):
        py = comb(Nn, k) * (p * Q) ** k * (1 - p * Q) ** (Nn - k)
        s_ = Fr(0)
        for n in range(k, Nn + 1):
            joint = comb(n, k) * Q ** k * (1 - Q) ** (n - k) * comb(Nn, n) * p ** n * (1 - p) ** (Nn - n)
            claimed = comb(Nn - k, Nn - n) * pt ** (Nn - n) * (1 - pt) ** (n - k)
            chk("ch06 Bayes bin n=%d k=%d" % (n, k), claimed, joint / py)
            s_ += claimed
        chk("ch06 Bayes bin sums to 1 k=%d" % k, 1, s_)
    # Poisson thinning
    lam, pp = 3.0, 0.4
    for k in range(0, 6):
        tot = sum(comb(n, k) * pp ** k * (1 - pp) ** (n - k) * stats.poisson.pmf(n, lam) for n in range(k, 120))
        chk("ch06 Poisson thinning k=%d" % k, stats.poisson.pmf(k, lam * pp), tot, tol=1e-12)
    # Bayes after Poisson thinning: n-k ~ P(lam(1-p))
    k = 2
    py = stats.poisson.pmf(k, lam * pp)
    for n in range(k, k + 6):
        post = comb(n, k) * pp ** k * (1 - pp) ** (n - k) * stats.poisson.pmf(n, lam) / py
        chk("ch06 Poisson Bayes n=%d" % n, stats.poisson.pmf(n - k, lam * (1 - pp)), post, tol=1e-12)
    # geometric parity
    for pv in (0.3, 0.5):
        ev = sum(pv * (1 - pv) ** (k - 1) for k in range(2, 4000, 2))
        chk("ch06 P(G even) p=%s" % pv, (1 - pv) / (2 - pv), ev, tol=1e-12)
        e_alt = sum((-1) ** k * pv * (1 - pv) ** (k - 1) for k in range(1, 4000))
        chk("ch06 E[(-1)^X] geometric p=%s" % pv, -pv / (2 - pv), e_alt, tol=1e-12)
    # negbin odd
    for m_, pv in ((3, 0.4), (2, 0.6), (4, 0.25)):
        odd = sum(comb(k - 1, m_ - 1) * pv ** m_ * (1 - pv) ** (k - m_) for k in range(m_, 3000) if k % 2 == 1)
        chk("ch06 P(NegBin odd) m=%d p=%s" % (m_, pv), 0.5 * (1 - (-pv / (2 - pv)) ** m_), odd, tol=1e-10)
    # tie game
    for pv in (0.3, 0.55):
        Qt = sum((pv * (1 - pv) ** (k - 1)) ** 2 for k in range(1, 3000))
        chk("ch06 P(tie)=p/(2-p) p=%s" % pv, pv / (2 - pv), Qt, tol=1e-12)
        pw = sum(pv * (1 - pv) ** (k - 1) * (1 - pv) ** k for k in range(1, 3000))
        chk("ch06 P(win)=(1-p)/(2-p) p=%s" % pv, (1 - pv) / (2 - pv), pw, tol=1e-12)
        chk("ch06 1-Q over 2 = P(win) p=%s" % pv, (1 - Qt) / 2, pw, tol=1e-12)
        for k in (1, 2, 5):
            tie_k = (pv * (1 - pv) ** (k - 1)) ** 2 / Qt
            chk("ch06 P(k|tie) geometric p(2-p) k=%d p=%s" % (k, pv), pv * (2 - pv) * (1 - pv) ** (2 * (k - 1)), tie_k, tol=1e-12)
            win_k = pv * (1 - pv) ** (k - 1) * (1 - pv) ** k / pw
            chk("ch06 P(k|B wins) geometric p(2-p) k=%d p=%s" % (k, pv), pv * (2 - pv) * (1 - pv) ** (2 * (k - 1)), win_k, tol=1e-12)
    # hypergeometric example
    chk("ch06 Hyp P(X=2)=14/33", Fr(14, 33), Fr(comb(5, 2) * comb(7, 2), comb(12, 4)))
    chk("ch06 Hyp scipy", 14 / 33, stats.hypergeom.pmf(2, 12, 5, 4))
    chk("ch06 Hyp E=5/3", Fr(5, 3), Fr(4 * 5, 12))
    chk("ch06 Bin(4,5/12) P(2)=1225/3456", Fr(1225, 3456), comb(4, 2) * Fr(5, 12) ** 2 * Fr(7, 12) ** 2)
    chk("ch06 Bin(4,5/12) P(2) float", 0.354, float(Fr(1225, 3456)), tol=5e-4)
    # mixture (24A-B-Q5c shape)
    for p_, Q_ in ((0.35, 0.3), (0.5, 0.2)):
        P0 = sum(p_ * (1 - p_) ** (j - 1) * (1 - Q_) ** j for j in range(1, 4000))
        chk("ch06 P(Z=0) p=%s Q=%s" % (p_, Q_), p_ * (1 - Q_) / (p_ * (1 - Q_) + Q_), P0, tol=1e-12)
        tot = P0
        for k in range(1, 8):
            Pk = sum(p_ * (1 - p_) ** (j - 1) * comb(j, k) * Q_ ** k * (1 - Q_) ** (j - k) for j in range(k, 4000))
            den = p_ * (1 - Q_) + Q_
            claimed = p_ / (1 - p_) / den * (Q_ * (1 - p_) / den) ** k
            chk("ch06 P(Z=%d) p=%s Q=%s" % (k, p_, Q_), claimed, Pk, tol=1e-12)
        den = p_ * (1 - Q_) + Q_
        r = Q_ * (1 - p_) / den
        tot = P0 + p_ / (1 - p_) / den * r / (1 - r)
        chk("ch06 Z pmf sums to 1 p=%s Q=%s" % (p_, Q_), 1, tot, tol=1e-12)
    for a_, k in ((0.3, 3), (0.5, 2)):
        s_ = sum(comb(j, k) * a_ ** j for j in range(k, 3000))
        chk("ch06 hint sum C(j,k)a^j a=%s k=%d" % (a_, k), a_ ** k / (1 - a_) ** (k + 1), s_, tol=1e-9)
    # hint of 24A-A-Q5b identity
    for Nn_, m_, a_ in ((6, 2, 0.7), (5, 3, 1.3)):
        s_ = sum(comb(j, m_) * comb(Nn_, j) * a_ ** j for j in range(m_, Nn_ + 1))
        chk("ch06 hint identity N=%d m=%d" % (Nn_, m_), comb(Nn_, m_) * a_ ** m_ * (1 + a_) ** (Nn_ - m_), s_, tol=1e-9)
    # NegBin pmf example (not printed) skipped. Poisson parity (cheat sheet) and binomial parity
    chk("ch06 Poisson P(even)=(1+e^{-2 lam})/2", 0.5 * (1 + math.exp(-3.0)), sum(stats.poisson.pmf(k, 1.5) for k in range(0, 200, 2)), tol=1e-12)
    chk("ch06 Bin P(even)=(1+(1-2p)^n)/2", 0.5 * (1 + (1 - 0.6) ** 7), sum(stats.binom.pmf(k, 7, 0.3) for k in range(0, 8, 2)), tol=1e-12)
    # MC: tie game
    n = 1_000_000
    pv = 0.3
    g1 = rng.geometric(pv, size=n); g2 = rng.geometric(pv, size=n)
    chk_mc("ch06 MC P(tie)", pv / (2 - pv), float((g1 == g2).mean()), n=n)
    chk_mc("ch06 MC P(Boris wins)", (1 - pv) / (2 - pv), float((g2 < g1).mean()), n=n)
    # MC: thinning binomial N=5
    X = rng.binomial(Nn, float(p), size=n); Y = rng.binomial(X, float(Q))
    chk_mc("ch06 MC P(Y=1) thinning", comb(Nn, 1) * float(p * Q) * float(1 - p * Q) ** (Nn - 1), float((Y == 1).mean()), n=n)

    # ---------------- chapter 07
    p_, q_ = Fr(1, 2), Fr(1, 2)
    states = {(a, b): (p_ if a else 1 - p_) * (q_ if b else 1 - q_) for a in (0, 1) for b in (0, 1)}
    Dv = lambda a, b: a * b - a - b
    Tv = lambda a, b: a + b - 1
    joint = {}
    for (a, b), w in states.items():
        joint[(Dv(a, b), Tv(a, b))] = joint.get((Dv(a, b), Tv(a, b)), 0) + w
    chk_eq("ch07 joint table", {(-1, 0): Fr(1, 2), (-1, 1): Fr(1, 4), (0, -1): Fr(1, 4)}, {k: v for k, v in joint.items() if v})
    ED = sum(d * w for (d, t), w in joint.items()); ET = sum(t * w for (d, t), w in joint.items())
    ED2 = sum(d * d * w for (d, t), w in joint.items()); ET2 = sum(t * t * w for (d, t), w in joint.items())
    EDT = sum(d * t * w for (d, t), w in joint.items())
    chk("ch07 E[D]=-3/4", Fr(-3, 4), ED); chk("ch07 E[D^2]=3/4", Fr(3, 4), ED2); chk("ch07 Var D=3/16", Fr(3, 16), ED2 - ED ** 2)
    chk("ch07 E[T]=0", 0, ET); chk("ch07 Var T=1/2", Fr(1, 2), ET2 - ET ** 2)
    chk("ch07 E[DT]=-1/4", Fr(-1, 4), EDT); cov = EDT - ED * ET
    chk("ch07 Cov=-1/4", Fr(-1, 4), cov)
    rho = float(cov) / math.sqrt(float((ED2 - ED ** 2) * (ET2 - ET ** 2)))
    chk("ch07 rho=-sqrt(2/3)", -math.sqrt(2 / 3), rho, tol=1e-12)
    chk("ch07 rho approx -0.816", -0.816, rho, tol=1e-3)
    pD = {}
    pT = {}
    for (d, t), w in joint.items():
        pD[d] = pD.get(d, 0) + w; pT[t] = pT.get(t, 0) + w
    chk_eq("ch07 P_D", {-1: Fr(3, 4), 0: Fr(1, 4)}, pD)
    chk_eq("ch07 P_T", {-1: Fr(1, 4), 0: Fr(1, 2), 1: Fr(1, 4)}, pT)
    # MC for the matrix
    n = 1_000_000
    Xb = rng.random(n) < 0.5; Yb = rng.random(n) < 0.5
    Dm = (Xb & Yb).astype(int) - Xb - Yb; Tm = Xb.astype(int) + Yb - 1
    chk_mc_val("ch07 MC Cov(D,T)", Fr(-1, 4), float(np.cov(Dm, Tm)[0, 1]), 0.5 / 1000)
    # coins overlapped, p=0.3
    pv = Fr(3, 10)
    J = {}
    for x1, x2, x3 in itertools.product((0, 1), repeat=3):
        w = 1
        for b in (x1, x2, x3):
            w *= pv if b else 1 - pv
        J[(x1 + x2, x2 + x3)] = J.get((x1 + x2, x2 + x3), 0) + w
    chk("ch07 coins P(1,1)=p(1-p)", pv * (1 - pv), J[(1, 1)]); chk("ch07 coins P(1,1)=0.21", Fr(21, 100), J[(1, 1)])
    chk("ch07 coins P(0,0)", (1 - pv) ** 3, J[(0, 0)]); chk("ch07 coins P(1,2)", pv ** 2 * (1 - pv), J[(1, 2)])
    chk("ch07 coins P(2,0)=0", 0, J.get((2, 0), 0))
    EXv = sum(x * w for (x, y), w in J.items()); EYv = sum(y * w for (x, y), w in J.items())
    EXY = sum(x * y * w for (x, y), w in J.items())
    VX = sum(x * x * w for (x, y), w in J.items()) - EXv ** 2; VY = sum(y * y * w for (x, y), w in J.items()) - EYv ** 2
    chk("ch07 coins Cov=p(1-p)", pv * (1 - pv), EXY - EXv * EYv)
    chk("ch07 coins Var X=2p(1-p)", 2 * pv * (1 - pv), VX)
    chk("ch07 coins rho=1/2", 0.5, float(EXY - EXv * EYv) / math.sqrt(float(VX * VY)), tol=1e-12)
    chk("ch07 coins P(X=1)=0.42", Fr(42, 100), sum(w for (x, y), w in J.items() if x == 1))
    # hypergeometric conditional (24A-A-Q3c)
    N1, N2, nn, pp = 4, 6, 5, Fr(3, 10)
    for k in range(0, nn + 1):
        num = comb(N1, k) * pp ** k * (1 - pp) ** (N1 - k) * comb(N2, nn - k) * pp ** (nn - k) * (1 - pp) ** (N2 - nn + k)
        den = comb(N1 + N2, nn) * pp ** nn * (1 - pp) ** (N1 + N2 - nn)
        chk("ch07 conditional hypergeometric k=%d" % k, Fr(comb(N1, k) * comb(N2, nn - k), comb(N1 + N2, nn)), num / den)
    chk("ch07 E[X1|X=n]=n N1/(N1+N2)", Fr(nn * N1, N1 + N2), sum(k * Fr(comb(N1, k) * comb(N2, nn - k), comb(N1 + N2, nn)) for k in range(nn + 1)))
    # batteries rho (25A-A-Q6c)
    for (n_, pb, qb) in ((3, Fr(1, 5), Fr(1, 2)), (4, Fr(7, 10), Fr(2, 5))):
        # categories per battery: not A (1-q), A good (q(1-p)), A defective (qp)
        cats = [(0, 0, 1 - qb), (1, 0, qb * (1 - pb)), (1, 1, qb * pb)]
        EXx = EYy = EXYy = EX2 = EY2 = Fr(0)
        for combo in itertools.product(cats, repeat=n_):
            w = Fr(1)
            for c in combo:
                w *= c[2]
            xs_ = sum(c[0] for c in combo); ys_ = sum(c[1] for c in combo)
            EXx += w * xs_; EYy += w * ys_; EXYy += w * xs_ * ys_; EX2 += w * xs_ ** 2; EY2 += w * ys_ ** 2
        cv = EXYy - EXx * EYy
        chk("ch07 battery Cov=npq(1-q) n=%d" % n_, n_ * pb * qb * (1 - qb), cv)
        chk("ch07 battery E[XY]", pb * qb * n_ + n_ * (n_ - 1) * pb * qb ** 2, EXYy)
        rho_ = float(cv) / math.sqrt(float((EX2 - EXx ** 2) * (EY2 - EYy ** 2)))
        chk("ch07 battery rho n=%d" % n_, math.sqrt(float(pb * (1 - qb) / (1 - pb * qb))), rho_, tol=1e-12)
    chk("ch07 battery rho at p=1", 1.0, math.sqrt(1.0 * (1 - 0.4) / (1 - 0.4)))
