# -*- coding: utf-8 -*-
"""Numbers of chapters 08-12 (continuous RV, normal, area method, pdf constants, min/max)."""
import itertools
import math
from fractions import Fraction as Fr
from math import comb

import numpy as np
import sympy as sp
from scipy import integrate, stats

from common import chk, chk_eq, chk_mc, chk_mc_val, RNG

x, y, t = sp.symbols("x y t", real=True)


def sampler_from_pieces(pieces, n, rng, grid=400_001):
    """Inverse-CDF sampler for a piecewise pdf given as [(lo, hi, sympy expr in x)]."""
    xs = []
    for lo, hi, e in pieces:
        f = sp.lambdify(x, e, "numpy")
        g = np.linspace(lo, hi, grid // len(pieces) + 1)
        xs.append((g, np.broadcast_to(f(g), g.shape)))
    gx = np.concatenate([a for a, b in xs]); gf = np.concatenate([b for a, b in xs])
    cdf = np.concatenate([[0], np.cumsum((gf[1:] + gf[:-1]) / 2 * np.diff(gx))])
    cdf /= cdf[-1]
    u = rng.random(n)
    return np.interp(u, cdf, gx)


def run():
    rng = RNG
    n = 1_000_000
    # ---------------- chapter 08
    EX, EY = Fr(1, 2), Fr(1)
    EX2, EY2 = Fr(1, 3), Fr(4, 3)
    chk("ch08 E[S]=1/2", Fr(1, 2), EX * EY); chk("ch08 E[S^2]=4/9", Fr(4, 9), EX2 * EY2)
    chk("ch08 Var S=7/36", Fr(7, 36), EX2 * EY2 - (EX * EY) ** 2)
    chk("ch08 E[L]=3", 3, 2 * (EX + EY)); chk("ch08 Var L=5/3", Fr(5, 3), 4 * (Fr(1, 12) + Fr(4, 12)))
    X = rng.random(n); Y = 2 * rng.random(n)
    S = X * Y; L = 2 * (X + Y)
    chk_mc_val("ch08 MC E[S]", Fr(1, 2), S.mean(), S.std() / 1000)
    chk_mc_val("ch08 MC Var[S]", Fr(7, 36), S.var(), S.var() * math.sqrt(2 / n) * 1.5)
    chk_mc_val("ch08 MC E[L]", 3, L.mean(), L.std() / 1000)
    chk_mc_val("ch08 MC Var[L]", Fr(5, 3), L.var(), L.var() * math.sqrt(2 / n) * 1.5)
    chk("ch08 E sqrt Z two ways", Fr(4, 3), Fr(2, 3) * 2)
    q1 = sp.integrate(sp.sqrt(t) / 2, (t, 0, 1)) + sp.integrate(sp.sqrt(t) / (2 * t ** 2), (t, 1, sp.oo))
    chk("ch08 E[sqrt Z] via density", Fr(4, 3), Fr(str(sp.nsimplify(q1))))
    U1 = rng.random(n); U2 = rng.random(n)
    chk_mc_val("ch08 MC E[sqrt(X)] = 2/3", Fr(2, 3), np.sqrt(U1).mean(), np.sqrt(U1).std() / 1000)
    chk("ch08 E[1/sqrt(Y)] = 2 (integral)", 2, Fr(str(sp.integrate(1 / sp.sqrt(x), (x, 0, 1)))))
    chk("ch08 E[X] for 2(1-t)", Fr(1, 3), Fr(str(sp.integrate(t * 2 * (1 - t), (t, 0, 1)))))
    chk("ch08 normalisation of 2(1-t)", 1, Fr(str(sp.integrate(2 * (1 - t), (t, 0, 1)))))
    chk("ch08 Exp(2): P(Y>1)", math.exp(-2), 1 - stats.expon.cdf(1, scale=0.5), tol=1e-12)
    chk("ch08 Exp memoryless P(Y>3|Y>2)", math.exp(-2), stats.expon.sf(3, scale=0.5) / stats.expon.sf(2, scale=0.5), tol=1e-12)
    chk("ch08 Exp(2) mean", 0.5, stats.expon.mean(scale=0.5))
    chk("ch08 U(0,1/2) density 2, E=1/4, Var=1/48", Fr(1, 48), Fr(str(sp.integrate((t - sp.Rational(1, 4)) ** 2 * 2, (t, 0, sp.Rational(1, 2))))))

    # ---------------- chapter 09
    chk("ch09 P(9<X<13) table values", 0.6247, (0.5 + 0.4332) - (1 - (0.5 + 0.1915)), tol=1e-9)
    chk("ch09 P(9<X<13) exact", 0.6247, stats.norm.cdf(1.5) - stats.norm.cdf(-0.5), tol=6e-5)
    chk("ch09 Bin(100,.5) P(X<=55) approx (table)", 0.8643, 0.5 + 0.3643, tol=1e-9)
    chk("ch09 Bin P(X<=55) normal", 0.8643, stats.norm.cdf(1.1), tol=6e-5)
    chk("ch09 Bin exact", 0.8644, stats.binom.cdf(55, 100, 0.5), tol=6e-5)
    chk_eq("ch09 48 uniforms mean/var", (24, 4), (48 * 0.5, 48 / 12))
    chk("ch09 P(X>=26) table", 0.1587, 0.5 - 0.3413, tol=1e-9)
    s48 = rng.random((200_000, 48)).sum(axis=1)
    chk_mc("ch09 MC sum of 48 U(0,1) >= 26 ~ 0.1587", 0.1587, float((s48 >= 26).mean()), n=200_000)

    # ---------------- chapter 10 (area method)
    N_ = 1_000_000
    def quad_area(f_ineq, xr, yr):
        """exact-ish area of {f_ineq(x,y)} by integrating over y for each x (vectorized MC replaced by quadrature)."""
        pass
    u = rng.random(N_); v = rng.random(N_)
    # fence 1: X+Y<3/2
    chk("ch10 fence1 7/8", Fr(7, 8), 1 - Fr(1, 2) * Fr(1, 2) ** 2)
    chk_mc("ch10 fence1", Fr(7, 8), float((u + v < 1.5).mean()))
    # fence 2: X<Y<1-X
    chk("ch10 fence2 1/4", Fr(1, 4), Fr(1, 2) * 1 * Fr(1, 2))
    chk_mc("ch10 fence2", Fr(1, 4), float(((u < v) & (v < 1 - u)).mean()))
    # fence 3: rectangle (0,1)x(0,2), XY<1
    ex3 = (1 + math.log(2)) / 2
    q3 = integrate.quad(lambda xx: min(2.0, 1 / xx), 0, 1, points=[0.5])[0] / 2
    chk("ch10 fence3 (1+ln2)/2", ex3, q3, tol=1e-9); chk("ch10 fence3 value 0.847", 0.847, ex3, tol=5e-4)
    chk("ch10 fence3 json exact", 0.8465735902799727, ex3, tol=1e-15)
    X = u; Y = 2 * v
    chk_mc("ch10 fence3", ex3, float((X * Y < 1).mean()))
    # fence 4: conditional XY<1 | X+Y>1
    ex4 = 1 / 3 + 2 / 3 * math.log(2)
    given = X + Y > 1
    chk("ch10 fence4 json exact", 0.7954314537066301, ex4, tol=1e-15)
    chk("ch10 fence4 areas", ex4, ((1 + math.log(2)) - 0.5) / 1.5, tol=1e-12)
    chk_mc("ch10 fence4", ex4, float((X[given] * Y[given] < 1).mean()), n=int(given.sum()))
    chk("ch10 fence4 given area 3/2", 1.5, 2 - 0.5)
    # fence 5: min<1/3
    chk("ch10 fence5 5/9", Fr(5, 9), 1 - Fr(2, 3) ** 2)
    chk_mc("ch10 fence5", Fr(5, 9), float((np.minimum(u, v) < 1 / 3).mean()))
    chk("ch10 fence5 max<1/3 = 1/9", Fr(1, 9), Fr(1, 3) ** 2)
    # fence 6: three segments, left shortest
    a = rng.random(N_) / 2; b = rng.random(N_) / 2
    chk("ch10 fence6 area 5/48", Fr(5, 48), Fr(1, 2) * Fr(1, 2) * Fr(1, 2) - Fr(1, 2) * Fr(1, 4) * Fr(1, 6))
    chk("ch10 fence6 5/12", Fr(5, 12), Fr(5, 48) / Fr(1, 4))
    chk_mc("ch10 fence6 left shortest", Fr(5, 12), float(((a < b) & (a < 1 - a - b)).mean()))
    left = (a < b) & (a < 1 - a - b)
    mid = (1 - a - b > a) & (1 - a - b > b)
    chk_mc("ch10 middle longest 2/3", Fr(2, 3), float(mid.mean()))
    # 25S-A-Q1d conditional
    X1 = rng.random(N_); X2 = 2 * rng.random(N_)
    gv = X1 + X2 > 2
    chk("ch10 25S-A-Q1d 3/4", Fr(3, 4), Fr(3, 8) / Fr(1, 2))
    chk("ch10 trapezoid integral 3/8", Fr(3, 8), Fr(str(sp.integrate(x, (x, sp.Rational(1, 2), 1)))))
    chk_mc("ch10 25S-A-Q1d", Fr(3, 4), float((X1[gv] > 0.5).mean()), n=int(gv.sum()))
    # 25A-C-Q1 full example
    Xr = u; Yr = 2 * v
    Sx = Xr * Yr; Lx = 2 * (Xr + Yr)
    p1 = (1 + math.log(3)) / 3
    chk("ch10 25A-C a1 value 0.700", 0.700, p1, tol=5e-4)
    q = integrate.quad(lambda xx: min(2.0, 2 / (3 * xx)), 0, 1, points=[1 / 3])[0] / 2
    chk("ch10 25A-C a1 (1+ln3)/3", p1, q, tol=1e-9)
    chk_mc("ch10 25A-C a1", p1, float((Sx < 2 / 3).mean()))
    chk("ch10 25A-C a2 1/4", Fr(1, 4), Fr(1, 2) / 2)
    chk_mc("ch10 25A-C a2", Fr(1, 4), float((Lx < 2).mean()))
    p3 = (1 + 4 * math.log(3)) / 9
    chk("ch10 25A-C a3 value 0.599", 0.599, p3, tol=6e-4)
    chk("ch10 25A-C a3 via parts", p3, (p1 - 0.25) / 0.75, tol=1e-12)
    g = Lx > 2
    chk_mc("ch10 25A-C a3", p3, float((Sx[g] < 2 / 3).mean()), n=int(g.sum()))
    chk("ch10 trap2 wrong 0.4495", 0.4495, p1 - 0.25, tol=5e-5)
    chk("ch10 trap2 right 0.5994", 0.5994, p3, tol=5e-5)
    # other small ones
    chk_mc("ch10 24B-A-Q1e 2/3", Fr(2, 3), float((np.minimum(u, v)[u > 0.25] < 0.5).mean()), n=int((u > 0.25).sum()))
    chk("ch10 24B-A-Q1e areas", Fr(2, 3), Fr(1, 2) / Fr(3, 4))
    chk("ch10 24A-E-Q1d 1/6", Fr(1, 6), Fr(1, 3) / 2)
    XL = rng.random(N_); XR = 2 * rng.random(N_)
    chk_mc("ch10 24A-E-Q1d", Fr(1, 6), float(((XR > XL) & (XR - XL < 1 / 3)).mean()))
    chk("ch10 24S-A-Q1b pi/4", math.pi / 4, integrate.quad(lambda xx: math.sqrt(max(0, 1 - xx * xx)), 0, 1)[0], tol=1e-9)
    chk_mc("ch10 P(S1<S2)=1/2", Fr(1, 2), float((u < v).mean()))
    # derived CDF table (unit square)
    for tt in (0.35, 0.7):
        chk_mc("ch10 F_max(%s)" % tt, tt ** 2, float((np.maximum(u, v) <= tt).mean()))
        chk_mc("ch10 F_min(%s)" % tt, 2 * tt - tt * tt, float((np.minimum(u, v) <= tt).mean()))
        chk_mc("ch10 F_|X-Y|(%s)" % tt, 2 * tt - tt * tt, float((np.abs(u - v) <= tt).mean()))
        chk_mc("ch10 F_XY(%s)" % tt, tt - tt * math.log(tt), float((u * v <= tt).mean()))
        chk_mc("ch10 F_min/max(%s)" % tt, tt, float(((np.minimum(u, v) / np.maximum(u, v)) <= tt).mean()))
    chk_mc("ch10 F_X/Y(0.4)", 0.2, float((u / v <= 0.4).mean()))
    chk_mc("ch10 F_X/Y(2)", 1 - 1 / 4, float((u / v <= 2).mean()))
    chk_mc("ch10 F_{X+Y}(0.6)", 0.6 ** 2 / 2, float((u + v <= 0.6).mean()))
    chk_mc("ch10 F_{X+Y}(1.3)", 1 - (2 - 1.3) ** 2 / 2, float((u + v <= 1.3).mean()))
    # symbolic derivation of the |X-Y| and XY cdfs
    chk("ch10 |X-Y| cdf area", 2 * 0.5 - 0.25, 1 - 2 * 0.5 * 0.5 ** 2, tol=1e-15)
    chk("ch10 P(|X1-X2|<1/2)=3/4", Fr(3, 4), 1 - 2 * Fr(1, 2) * Fr(1, 2) ** 2)
    chk("ch10 E|X-Y| = 1/3", Fr(1, 3), Fr(str(sp.integrate(t * 2 * (1 - t), (t, 0, 1)))))
    chk("ch10 XY cdf derivative -ln t", True, True) if sp.simplify(sp.diff(t - t * sp.log(t), t) + sp.log(t)) == 0 else chk("ch10 XY cdf derivative -ln t", 1, 0)

    # ---------------- chapter 11 (pdf constants)
    a, b, c, mu = sp.symbols("a b c mu", real=True)
    # example A: graph form
    aa, bb, cc = sp.symbols("aa bb cc", positive=True)
    eqs = [aa * cc / 2 + cc * (bb - aa) - 1,               # normalisation (triangle + rectangle)
           aa * cc / 2 - cc * (bb - aa),                   # P(0<X<a) = P(a<X<b)
           cc * bb ** 2 / 2 - cc * aa ** 2 / 6 - sp.Rational(23, 24)]  # E[X] from the two pieces
    sol = sp.solve(eqs, [aa, bb, cc], dict=True)
    chk_eq("ch11 A solution a=1,b=3/2,c=1", {aa: 1, bb: sp.Rational(3, 2), cc: 1}, sol[0])
    chk_eq("ch11 A E[X] formula c b^2/2 - c a^2/6", True, sp.simplify(sp.integrate(x * cc * x / aa, (x, 0, aa)) + sp.integrate(x * cc, (x, aa, bb)) - (cc * bb ** 2 / 2 - cc * aa ** 2 / 6)) == 0)
    fA = sp.Piecewise((x, (x > 0) & (x < 1)), (1, (x >= 1) & (x < sp.Rational(3, 2))), (0, True))
    chk("ch11 A normalisation", 1, Fr(str(sp.integrate(x, (x, 0, 1)) + sp.integrate(1, (x, 1, sp.Rational(3, 2))))))
    chk("ch11 A E[X]=23/24", Fr(23, 24), Fr(str(sp.integrate(x * x, (x, 0, 1)) + sp.integrate(x, (x, 1, sp.Rational(3, 2))))))
    chk("ch11 A equal halves", Fr(1, 2), Fr(str(sp.integrate(x, (x, 0, 1)))))
    chk("ch11 A P(X>E)", 1 - 0.5 * (23 / 24) ** 2, 1 - (23 / 24) ** 2 / 2, tol=1e-15)
    chk("ch11 A P(X>E) value 0.541", 0.541, 1 - 0.5 * (23 / 24) ** 2, tol=6e-4)
    # sample
    smp = sampler_from_pieces([(0, 1, x), (1, 1.5, sp.Integer(1))], n, rng)
    chk_mc("ch11 A MC P(X>23/24)", 1 - 0.5 * (23 / 24) ** 2, float((smp > 23 / 24).mean()))
    chk("ch11 A F(1)=1/2", Fr(1, 2), Fr(1, 2))
    # example B: 25A-A-Q3
    aB, bB = sp.symbols("aB bB", real=True)
    solB = sp.solve([aB + bB / 2 - 1, -aB + bB / 3 - mu], [aB, bB], dict=True)[0]
    chk_eq("ch11 B a=(2-3mu)/5", True, sp.simplify(solB[aB] - (2 - 3 * mu) / 5) == 0)
    chk_eq("ch11 B b=6(mu+1)/5", True, sp.simplify(solB[bB] - 6 * (mu + 1) / 5) == 0)
    chk("ch11 B int x e^x = -1", -1, Fr(str(sp.integrate(x * sp.exp(x), (x, -sp.oo, 0)))))
    # range of mu for non-negativity
    chk("ch11 B mu max 2/3", Fr(2, 3), Fr(str(sp.solve(solB[aB], mu)[0])))
    chk("ch11 B mu min -1", -1, Fr(str(sp.solve(solB[bB], mu)[0])))
    chk("ch11 B mu=1 gives a=-1/5", Fr(-1, 5), Fr(str(solB[aB].subs(mu, 1))))
    chk("ch11 B F(0)=a at mu=0 is 2/5", Fr(2, 5), Fr(str(solB[aB].subs(mu, 0))))
    cdfB = solB[aB] + sp.Rational(3, 5) * (mu + 1) * t ** 2          # claimed F on [0,1)
    chk_eq("ch11 B F middle = a + (b/2) t^2", True, sp.simplify(cdfB - (solB[aB] + solB[bB] / 2 * t ** 2)) == 0)
    chk_eq("ch11 B F(1)=1 for all mu", 1, sp.simplify(cdfB.subs(t, 1)))
    chk_eq("ch11 B E[X]=mu check", True, sp.simplify(-solB[aB] + solB[bB] / 3 - mu) == 0)
    chk("ch11 B mu=0.2 a", 0.28, float(solB[aB].subs(mu, sp.Rational(1, 5))), tol=1e-12)
    chk("ch11 B mu=0.2 b", 1.44, float(solB[bB].subs(mu, sp.Rational(1, 5))), tol=1e-12)
    # example C: 24S-A-Q4
    solC = sp.solve([a + b - 1, -a / 2 + b], [a, b], dict=True)[0]
    chk_eq("ch11 C a=2/3 b=1/3", (sp.Rational(2, 3), sp.Rational(1, 3)), (solC[a], solC[b]))
    chk("ch11 C F(0)=2/3", Fr(2, 3), Fr(2, 3) * 1)
    FC = lambda tt: (2 / 3 * (tt + 1) if tt < 0 else 1 - math.exp(-tt) / 3)
    chk("ch11 C conditional (2e-1)/(3e-1)", (2 * math.e - 1) / (3 * math.e - 1), (FC(1) - FC(-0.5)) / FC(1), tol=1e-12)
    chk("ch11 C value 0.620", 0.620, (2 * math.e - 1) / (3 * math.e - 1), tol=6e-4)
    sC = np.where(rng.random(n) < 2 / 3, rng.random(n) - 1, rng.exponential(1, n))
    cond = sC < 1
    chk_mc("ch11 C MC conditional", (2 * math.e - 1) / (3 * math.e - 1), float((sC[cond] > -0.5).mean()), n=int(cond.sum()))
    chk("ch11 C E[X]=0", 0, -sp.Rational(2, 3) / 2 + sp.Rational(1, 3) * 1)
    # example D: triangle
    solD = sp.solve([aa * bb ** 2 - 1, aa * bb ** 4 - 4], [aa, bb], dict=True)[0]
    chk_eq("ch11 D a=1/4 b=2", (sp.Rational(1, 4), 2), (solD[aa], solD[bb]))
    fD = (2 - sp.Abs(x)) / 4
    chk("ch11 D normalisation", 1, Fr(str(sp.integrate((2 - x) / 4, (x, 0, 2)) * 2)))
    chk("ch11 D Var=2/3", Fr(2, 3), Fr(str(2 * sp.integrate(x ** 2 * (2 - x) / 4, (x, 0, 2)))))
    FDf = lambda tt: (0 if tt < -2 else (tt + 2) ** 2 / 8 if tt < 0 else 1 - (2 - tt) ** 2 / 8 if tt < 2 else 1)
    chk("ch11 D F(1)=7/8", Fr(7, 8), Fr(1) - Fr(1, 8))
    chk("ch11 D F(1/4)=79/128", Fr(79, 128), Fr(1) - Fr(1, 8) * Fr(49, 16))
    chk("ch11 D F(-1)=1/8", Fr(1, 8), Fr(1, 8))
    chk("ch11 D conditional 11/32", Fr(11, 32), (Fr(7, 8) - Fr(79, 128)) / (Fr(7, 8) - Fr(1, 8)))
    chk("ch11 D numerator 33/128", Fr(33, 128), Fr(7, 8) - Fr(79, 128))
    chk("ch11 D conditional vs F", Fr(11, 32), Fr(str((FDf(1) - FDf(0.25)) / (FDf(1) - FDf(-1)))).limit_denominator(1000))
    smpD = sampler_from_pieces([(-2, 0, (2 + x) / 4), (0, 2, (2 - x) / 4)], n, rng)
    cD = np.abs(smpD) < 1
    chk_mc("ch11 D MC conditional", Fr(11, 32), float((smpD[cD] > 0.25).mean()), n=int(cD.sum()))
    chk_eq("ch11 D Var = a b^4 / 6", True, sp.simplify(2 * aa * sp.integrate(x ** 2 * (bb - x), (x, 0, bb)) - aa * bb ** 4 / 6) == 0)
    # example E: 25B-B-Q4
    b_, c_, d_ = sp.symbols("b_ c_ d_", real=True)
    solE = sp.solve([c_ - b_ / 2 + d_ - 1, c_ - b_ / 2 - d_, b_ / 3 - c_ / 2 + d_ / 2 - mu], [b_, c_, d_], dict=True)[0]
    chk_eq("ch11 E d=1/2", sp.Rational(1, 2), sp.simplify(solE[d_]))
    chk_eq("ch11 E b=12mu", True, sp.simplify(solE[b_] - 12 * mu) == 0)
    chk_eq("ch11 E c=6mu+1/2", True, sp.simplify(solE[c_] - (6 * mu + sp.Rational(1, 2))) == 0)
    chk("ch11 E mu max 1/12", Fr(1, 12), Fr(str(sp.solve(sp.Rational(1, 2) - 6 * mu, mu)[0])))
    chk("ch11 E mu min -1/12", Fr(-1, 12), Fr(str(sp.solve(6 * mu + sp.Rational(1, 2), mu)[0])))
    chk("ch11 E F(-1/2)", Fr(1, 4) * (1 - 6 * Fr(1, 20)), Fr(str(sp.integrate((12 * sp.Rational(1, 20)) * x + 6 * sp.Rational(1, 20) + sp.Rational(1, 2), (x, -1, -sp.Rational(1, 2))))))
    # example F: 25S-B-Q4
    aF = sp.symbols("aF", real=True)
    cF = 2 - 2 * aF
    chk_eq("ch11 F normalisation a + c/2 = 1", 1, sp.simplify(aF + cF / 2))
    muF = sp.integrate(x * (aF + cF * x), (x, 0, 1))
    chk_eq("ch11 F mu = a/2+(2-2a)/3", True, sp.simplify(muF - (aF / 2 + (2 - 2 * aF) / 3)) == 0)
    solF = sp.solve(sp.Eq(muF, mu), aF)[0]
    chk_eq("ch11 F a=4-6mu", True, sp.simplify(solF - (4 - 6 * mu)) == 0)
    chk("ch11 F mu range low 1/3", Fr(1, 3), Fr(str(sp.solve(sp.Eq(4 - 6 * mu, 2), mu)[0])))
    chk("ch11 F mu range high 2/3", Fr(2, 3), Fr(str(sp.solve(sp.Eq(4 - 6 * mu, 0), mu)[0])))
    chk("ch11 F mu=0 gives a=4", 4, Fr(str(solF.subs(mu, 0))))
    chk_eq("ch11 F P(X<=1/2) = 5/4 - 3mu/2", True, sp.simplify(sp.integrate(solF + (2 - 2 * solF) * x, (x, 0, sp.Rational(1, 2))) - (sp.Rational(5, 4) - sp.Rational(3, 2) * mu)) == 0)
    # explainer shape: a/sqrt(x)+b : int = 2a+b
    chk("ch11 int a/sqrt(x)+b = 2a+b", True, True) if sp.simplify(sp.integrate(a / sp.sqrt(x) + b, (x, 0, 1)) - (2 * a + b)) == 0 else chk("ch11 int a/sqrt(x)+b", 1, 0)
    chk_eq("ch11 x^(-3/2) diverges at 0", sp.oo, sp.integrate(x ** sp.Rational(-3, 2), (x, 0, 1)))
    chk_eq("ch11 x^(-1/2) converges", 2, sp.integrate(x ** sp.Rational(-1, 2), (x, 0, 1)))
    chk_eq("ch11 1/x diverges at inf", sp.oo, sp.integrate(1 / x, (x, 1, sp.oo)))
    # table of integrals
    chk("ch11 int e^-x", 1, Fr(str(sp.integrate(sp.exp(-x), (x, 0, sp.oo)))))
    chk("ch11 int x e^-x", 1, Fr(str(sp.integrate(x * sp.exp(-x), (x, 0, sp.oo)))))
    chk("ch11 int x^2 e^-x", 2, Fr(str(sp.integrate(x ** 2 * sp.exp(-x), (x, 0, sp.oo)))))
    chk("ch11 int_{-b}^{b} x^2(b-|x|) = b^4/6 (b=3)", Fr(81, 6), Fr(str(2 * sp.integrate(x ** 2 * (3 - x), (x, 0, 3)))))

    # ---------------- chapter 12
    chk("ch12 E[max]=2/3", Fr(2, 3), Fr(str(sp.integrate(t * 2 * t, (t, 0, 1)))))
    chk("ch12 E[min]=1/3", Fr(1, 3), Fr(str(sp.integrate(t * 2 * (1 - t), (t, 0, 1)))))
    chk("ch12 E[min]+E[max]=E[X]+E[Y]", 1, Fr(2, 3) + Fr(1, 3))
    chk("ch12 Y=X^2 cdf sqrt(t), pdf", True, True) if sp.simplify(sp.diff(sp.sqrt(t), t) - 1 / (2 * sp.sqrt(t))) == 0 else chk("ch12 pdf", 1, 0)
    chk_mc("ch12 P(X^2<=0.3)", math.sqrt(0.3), float((u ** 2 <= 0.3).mean()))
    # stick
    xs = rng.random(n)
    eta = np.minimum(xs, 1 - xs)
    for tt in (0.2, 0.4):
        chk_mc("ch12 F_eta(%s)=2t" % tt, 2 * tt, float((eta <= tt).mean()))
    chk_mc_val("ch12 E[eta]=1/4", Fr(1, 4), eta.mean(), eta.std() / 1000)
    chk_mc_val("ch12 Var[eta]=1/48", Fr(1, 48), eta.var(), eta.var() * math.sqrt(2 / n) * 2)
    chk("ch12 E[eta^2]=1/12", Fr(1, 12), Fr(1, 48) + Fr(1, 16))
    e1 = np.minimum(xs, 1 - xs); xx2 = rng.random(n); e2 = np.minimum(xx2, 1 - xx2)
    X2 = e1 * e2
    chk_mc_val("ch12 E[X2]=1/16", Fr(1, 16), X2.mean(), X2.std() / 1000)
    chk("ch12 Var[X2]=7/2304", Fr(7, 2304), Fr(1, 144) - Fr(1, 256))
    chk_mc_val("ch12 Var[X2]", Fr(7, 2304), X2.var(), X2.var() * math.sqrt(2 / n) * 2)
    r1, r2, r3 = (np.minimum(w, 1 - w) for w in (rng.random(n), rng.random(n), rng.random(n)))
    X3 = r1 * r2 * r3
    chk_mc_val("ch12 E[X_3]=(1/4)^3", Fr(1, 64), X3.mean(), X3.std() / 1000)
    chk_mc_val("ch12 Var[X_3]", Fr(1, 12) ** 3 - Fr(1, 16) ** 3, X3.var(), X3.var() * math.sqrt(2 / n) * 3)
    chk("ch12 Var[X_n] closed form n=3", Fr(1, 1728) - Fr(1, 4096), Fr(1, 12) ** 3 - Fr(1, 16) ** 3)
    # discrete min/max without replacement
    for (N_, n_) in ((7, 3), (8, 4), (6, 2)):
        subs = list(itertools.combinations(range(1, N_ + 1), n_))
        tot = comb(N_, n_)
        chk_eq("ch12 count subsets N=%d n=%d" % (N_, n_), tot, len(subs))
        for k in range(1, N_ - n_ + 2):
            chk("ch12 P(min=%d) N=%d n=%d" % (k, N_, n_), Fr(comb(N_ - k, n_ - 1), tot), Fr(sum(1 for s in subs if min(s) == k), tot))
        for l in range(n_, N_ + 1):
            chk("ch12 P(max=%d) N=%d n=%d" % (l, N_, n_), Fr(comb(l - 1, n_ - 1), tot), Fr(sum(1 for s in subs if max(s) == l), tot))
        for k in range(1, N_ + 1):
            for l in range(k + 1, N_ + 1):
                claimed = Fr(comb(l - k - 1, n_ - 2), tot)
                real = Fr(sum(1 for s in subs if min(s) == k and max(s) == l), tot)
                if claimed != real:
                    chk("ch12 joint k=%d l=%d N=%d n=%d" % (k, l, N_, n_), claimed, real)
        chk("ch12 E[min]=(N+1)/(n+1) N=%d n=%d" % (N_, n_), Fr(N_ + 1, n_ + 1), Fr(sum(min(s) for s in subs), tot))
        chk("ch12 E[max]=n(N+1)/(n+1) N=%d n=%d" % (N_, n_), Fr(n_ * (N_ + 1), n_ + 1), Fr(sum(max(s) for s in subs), tot))
    chk("ch12 N=7 n=3 P(min=1)=3/7", Fr(3, 7), Fr(comb(6, 2), 35))
    # dice min/max with replacement
    for Nf in (4, 6):
        pairs = list(itertools.product(range(1, Nf + 1), repeat=2))
        for k in range(1, Nf + 1):
            chk("ch12 dice P(min=%d) N=%d" % (k, Nf), Fr(2 * (Nf - k) + 1, Nf * Nf), Fr(sum(1 for p_ in pairs if min(p_) == k), Nf * Nf))
            chk("ch12 dice P(max=%d) N=%d" % (k, Nf), Fr(2 * k - 1, Nf * Nf), Fr(sum(1 for p_ in pairs if max(p_) == k), Nf * Nf))
        chk("ch12 dice joint k<l N=%d" % Nf, Fr(2, Nf * Nf), Fr(sum(1 for p_ in pairs if min(p_) == 1 and max(p_) == 2), Nf * Nf))
    # two people on different chairs
    for Nc in (4, 6):
        ordered = list(itertools.permutations(range(1, Nc + 1), 2))
        chk("ch12 chairs joint N=%d" % Nc, Fr(2, Nc * (Nc - 1)), Fr(sum(1 for p_ in ordered if min(p_) == 1 and max(p_) == 2), len(ordered)))
        for k in range(1, Nc):
            chk("ch12 chairs P(XL=%d) N=%d" % (k, Nc), Fr(2 * (Nc - k), Nc * (Nc - 1)), Fr(sum(1 for p_ in ordered if min(p_) == k), len(ordered)))
