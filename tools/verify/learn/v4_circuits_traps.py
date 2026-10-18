# -*- coding: utf-8 -*-
"""Numbers of chapters 13-14 (circuits, traps) and the cheat sheet."""
import itertools
import math
from fractions import Fraction as Fr
from math import comb

import numpy as np
import sympy as sp

from common import chk, chk_eq, chk_mc, chk_mc_val, RNG

p = sp.symbols("p", positive=True)


def bridge(st):  # st: dict A..E -> 0/1 ; source-left, sink-right; A,B top; C,D bottom; E middle
    A, B, C, D, E = (st[k] for k in "ABCDE")
    return int(((A or C) and (B or D)) if E else ((A and B) or (C and D)))


def q2(st):  # A series (B parallel C) series (D parallel E)
    return int(st["A"] and (st["B"] or st["C"]) and (st["D"] or st["E"]))


def prob(fn, pv):
    tot = Fr(0)
    for bits in itertools.product((0, 1), repeat=5):
        st = dict(zip("ABCDE", bits))
        w = Fr(1)
        for b in bits:
            w *= pv if b else 1 - pv
        tot += w * fn(st)
    return tot


def run():
    rng = RNG
    n = 1_000_000
    # ---------------- chapter 13
    P1 = p * (2 * p - p ** 2) ** 2 + (1 - p) * (2 * p ** 2 - p ** 4)
    chk_eq("ch13 P(Q1) = p^2(2+2p-5p^2+2p^3)", True, sp.simplify(P1 - p ** 2 * (2 + 2 * p - 5 * p ** 2 + 2 * p ** 3)) == 0)
    chk_eq("ch13 P(Q1) alt form p^3(2-p)^2 + p^2(1-p)(2-p^2)", True, sp.simplify(P1 - (p ** 3 * (2 - p) ** 2 + p ** 2 * (1 - p) * (2 - p ** 2))) == 0)
    chk_eq("ch13 P(Q2) = p^3(2-p)^2", True, sp.simplify(p * (2 * p - p ** 2) ** 2 - p ** 3 * (2 - p) ** 2) == 0)
    for pv in (Fr(3, 5), Fr(1, 3), Fr(9, 10)):
        chk("ch13 bridge enumeration p=%s" % pv, float(P1.subs(p, sp.Rational(pv.numerator, pv.denominator))), float(prob(bridge, pv)), tol=1e-12)
        chk("ch13 Q2 enumeration p=%s" % pv, pv ** 3 * (2 - pv) ** 2, prob(q2, pv))
        both = prob(lambda s: bridge(s) and q2(s), pv)
        chk("ch13 P(Q1 cap Q2) = p^3(3-2p) p=%s" % pv, pv ** 3 * (3 - 2 * pv), both)
        chk("ch13 P(Q1|Q2) p=%s" % pv, (3 - 2 * pv) / (2 - pv) ** 2, both / prob(q2, pv))
        chk("ch13 P(notQ1|Q2) p=%s" % pv, (1 - pv) ** 2 / (2 - pv) ** 2, 1 - both / prob(q2, pv))
        chk("ch13 P(B|Q2)=1/(2-p) p=%s" % pv, 1 / (2 - pv), prob(lambda s: q2(s) and s["B"], pv) / prob(q2, pv))
        chk("ch13 P(A|Q2)=1" , 1, prob(lambda s: q2(s) and s["A"], pv) / prob(q2, pv))
    pv = Fr(3, 5)
    chk("ch13 P(Q1) at 0.6 = 0.65952", Fr(65952, 100000), prob(bridge, pv))
    chk("ch13 P(Q2) at 0.6 = 0.42336", Fr(42336, 100000), prob(q2, pv))
    chk("ch13 P(Q1 cap Q2) at 0.6 = 0.3888", Fr(3888, 10000), prob(lambda s: bridge(s) and q2(s), pv))
    chk("ch13 P(Q1|Q2) at 0.6 ~ 0.918", 0.918, float(Fr(3888, 10000) / Fr(42336, 100000)), tol=6e-4)
    chk("ch13 P(Q2|Q1) at 0.6 ~ 0.590", 0.590, float(Fr(3888, 10000) / Fr(65952, 100000)), tol=6e-4)
    chk_eq("ch13 0.6595 and 0.4234 rounded", (0.6595, 0.4234), (round(0.65952, 4), round(0.42336, 4)))
    chk("ch13 1/(2-0.6)=0.714", 0.714, 1 / 1.4, tol=6e-4)
    chk("ch13 P(Q1|Q2) formula numeric", 0.9183673469387755, (3 - 1.2) / 1.4 ** 2, tol=1e-12)
    # P(Q1 u Q2) simplification claimed in the bank (check the identity used)
    chk_eq("ch13 union = p^2(3-4p^2+2p^3) for the Q1/Q2 of 24A-A (bridge with E vs A swapped, same probability)", True,
           sp.simplify(P1 + P1 - p ** 2 * (1 + 4 * p - 6 * p ** 2 + 2 * p ** 3) - p ** 2 * (3 - 4 * p ** 2 + 2 * p ** 3)) == 0)
    # MC for the circuits
    ub = rng.random((n, 5)) < 0.6
    A, B, C, D, E = (ub[:, i] for i in range(5))
    Q1 = np.where(E, (A | C) & (B | D), (A & B) | (C & D)); Q2 = A & (B | C) & (D | E)
    chk_mc("ch13 MC P(Q1)", 0.65952, float(Q1.mean())); chk_mc("ch13 MC P(Q2)", 0.42336, float(Q2.mean()))
    chk_mc("ch13 MC P(Q1|Q2)", 0.9183673469387755, float(Q1[Q2].mean()), n=int(Q2.sum()))
    chk_mc("ch13 MC P(Q2|Q1)", 0.3888 / 0.65952, float(Q2[Q1].mean()), n=int(Q1.sum()))
    # exactly one failed
    def single_fail_prob(fn, pv, k=5):
        num = den = Fr(0)
        for bits in itertools.product((0, 1), repeat=5):
            if sum(1 - b for b in bits) != 1:
                continue
            st = dict(zip("ABCDE", bits))
            w = Fr(1)
            for b in bits:
                w *= pv if b else 1 - pv
            den += w; num += w * fn(st)
        return num / den
    for pv in (Fr(3, 5), Fr(1, 4)):
        chk("ch13 exactly one failed, Q2 = 4/5 p=%s" % pv, Fr(4, 5), single_fail_prob(q2, pv))
        chk("ch13 exactly one failed, bridge = 1 p=%s" % pv, 1, single_fail_prob(bridge, pv))
    # unequal probabilities: weights (1-p_i)/p_i
    ps = {"A": Fr(9, 10), "B": Fr(1, 2), "C": Fr(7, 10), "D": Fr(3, 5), "E": Fr(1, 3)}
    num = den = Fr(0)
    for bits in itertools.product((0, 1), repeat=5):
        if sum(1 - b for b in bits) != 1:
            continue
        st = dict(zip("ABCDE", bits))
        w = Fr(1)
        for k, b in zip("ABCDE", bits):
            w *= ps[k] if b else 1 - ps[k]
        den += w; num += w * q2(st)
    wts = {k: (1 - v) / v for k, v in ps.items()}
    safe = sum(wts[k] for k in "BCDE")
    chk("ch13 unequal p: weights formula", safe / sum(wts.values()), num / den)
    # dependent components
    pp, qq, ss = Fr(1, 2), Fr(4, 5), Fr(3, 10)
    pAB = pp * qq; PA = pp; PB = pp * qq + (1 - pp) * ss
    chk("ch13 dep P(Q1)=pq", Fr(2, 5), pAB)
    chk("ch13 dep P(Q2)=p+s(1-p)", Fr(13, 20), PA + PB - pAB)
    chk("ch13 dep P(Q2) = 1-(1-p)(1-s)", Fr(13, 20), 1 - (1 - pp) * (1 - ss))
    chk("ch13 dep P(Q1|Q2)=8/13", Fr(8, 13), pAB / (PA + PB - pAB))
    # three components: P(B) = q1 p^2 + (q3+q4) p(1-p) + q2 (1-p)^2
    qs = {"AC": Fr(9, 10), "nAnC": Fr(1, 5), "AnC": Fr(1, 2), "nAC": Fr(3, 5)}
    pc = Fr(2, 5)
    P_B = qs["AC"] * pc ** 2 + qs["AnC"] * pc * (1 - pc) + qs["nAC"] * (1 - pc) * pc + qs["nAnC"] * (1 - pc) ** 2
    chk("ch13 three comps P(B) formula", P_B, qs["AC"] * pc ** 2 + (qs["AnC"] + qs["nAC"]) * pc * (1 - pc) + qs["nAnC"] * (1 - pc) ** 2)
    chk("ch13 three comps series q1 p^2", qs["AC"] * pc ** 2, qs["AC"] * pc ** 2)
    # ---------------- chapter 14 (traps)
    chk("ch14 trap1 right 1/4", Fr(1, 4), Fr(1, 2) / 2); chk("ch14 trap1 wrong 1/2", Fr(1, 2), Fr(1, 2) / 1)
    u = rng.random(n); v = 2 * rng.random(n)
    chk_mc("ch14 trap1 MC", Fr(1, 4), float((u + v < 1).mean()))
    chk("ch14 trap2 dice 1/36", Fr(1, 36), Fr(1, 36)); chk("ch14 trap2 dice 4/36", Fr(4, 36), Fr(4, 36))
    chk("ch14 trap2 dice right 1/4", Fr(1, 4), Fr(1, 36) / Fr(4, 36))
    chk("ch14 trap3 with replacement", Fr(9, 64), Fr(3, 8) ** 2); chk("ch14 trap3 without", Fr(3, 28), Fr(3, 8) * Fr(2, 7))
    chk("ch14 trap3 second red both ways", Fr(3, 8), Fr(3, 8) * Fr(2, 7) + Fr(5, 8) * Fr(3, 7))
    chk("ch14 trap4 unordered 21 pairs", 21, len(list(itertools.combinations_with_replacement(range(1, 7), 2))))
    chk("ch14 trap4 wrong 2/21", Fr(2, 21), Fr(2, 21)); chk("ch14 trap4 right 1/9", Fr(1, 9), Fr(4, 36))
    chk("ch14 trap5 P7=1/6", Fr(1, 6), Fr(6, 36))
    chk("ch14 trap5 reach 3: 1/3+2/9+1/27", Fr(16, 27), Fr(1, 3) + Fr(2, 9) + Fr(1, 27))
    chk("ch14 trap6 P(A)P(B) 1/6", Fr(1, 6), Fr(1, 2) * Fr(1, 3))
    chk("ch14 trap7 E[Y]=31/6", Fr(31, 6), Fr(4 + 9 + 49, 12))
    chk("ch14 trap8 4e^2", 4 * math.e ** 2, sum(2.0 ** k / math.factorial(k - 2) for k in range(2, 80)), tol=1e-9)
    chk("ch14 trap8 value 29.56", 29.56, 4 * math.e ** 2, tol=6e-3); chk("ch14 trap8 wrong e^2 value 7.39", 7.39, math.e ** 2, tol=6e-3)
    chk("ch14 trap8 geometric from 2", Fr(1, 2), Fr(1, 4) / (1 - Fr(1, 2)))
    chk("ch14 trap8 geometric sum numeric", 0.5, sum(0.5 ** j for j in range(2, 200)), tol=1e-12)
    chk("ch14 trap9 F continuity", 1, Fr(2, 3) + Fr(1, 3))
    chk("ch14 trap10 a=-1/5 at mu=1", Fr(-1, 5), Fr(2 - 3, 5))
    chk("ch14 trap12 min", Fr(5, 9), 1 - Fr(2, 3) ** 2); chk("ch14 trap12 wrong", Fr(1, 9), Fr(1, 3) ** 2)
    # trap 13: coins overlapped p=0.3
    pv = Fr(3, 10)
    J = {}
    for x1, x2, x3 in itertools.product((0, 1), repeat=3):
        w = 1
        for bb in (x1, x2, x3):
            w *= pv if bb else 1 - pv
        J[(x1 + x2, x2 + x3)] = J.get((x1 + x2, x2 + x3), 0) + w
    ex = sum(a * w for (a, b), w in J.items()); ey = sum(b * w for (a, b), w in J.items())
    vx = sum(a * a * w for (a, b), w in J.items()) - ex ** 2
    cov = sum(a * b * w for (a, b), w in J.items()) - ex * ey
    vsum = sum((a + b) ** 2 * w for (a, b), w in J.items()) - (ex + ey) ** 2
    chk("ch14 trap13 Var X = 0.42", Fr(42, 100), vx); chk("ch14 trap13 Cov = 0.21", Fr(21, 100), cov)
    chk("ch14 trap13 Var(X+Y) = 1.26", Fr(126, 100), vsum)
    chk("ch14 trap13 wrong 0.84", Fr(84, 100), 2 * vx)
    chk("ch14 trap13 6 p(1-p)", Fr(126, 100), 6 * pv * (1 - pv))
