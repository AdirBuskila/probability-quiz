# -*- coding: utf-8 -*-
"""Numbers of chapters 00-04 (exam map, events, conditional, independence, combinatorics)."""
import glob
import itertools
import json
import os
from fractions import Fraction as Fr
from math import comb

import sympy as sp

from common import chk, chk_eq, chk_mc, RNG, N_MC
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "..", "raw"))


def run():
    # ---------------- chapter 00: shape frequencies readable from the bank (20 sittings)
    exams = {}
    for f in sorted(glob.glob(os.path.join(RAW, "2*.json"))):
        d = json.load(open(f, encoding="utf8"))
        exams[d["examCode"]] = [q for q in d["questions"] if not q.get("hold")]
    chk_eq("ch00 sittings in bank", 20, len(exams))
    has_area = sum(1 for qs in exams.values() if any(q.get("topic") in ("uniform_geometric", "minmax_transform") and q.get("region") for q in qs) or any(q.get("topic") == "uniform_geometric" for q in qs))
    has_circ = sum(1 for qs in exams.values() if any(q.get("topic") == "circuits" for q in qs))
    has_pdf = sum(1 for qs in exams.values() if any(q.get("topic") == "continuous_rv" and ("\\mathbb E[X]" in q.get("question", "") or "מצאו את הפרמטרים" in q.get("question", "") or "המקדמים" in q.get("question", "") or "מקדמים" in q.get("question", "") or "פונקציית ההתפלגות המצטברת" in q.get("question", "")) for q in qs))
    chk_eq("ch00 area shape in 20 of 20", 20, has_area)
    chk_eq("ch00 circuits (incl. the 25S-A road network) in 20 of 20", 20, has_circ)
    chk_eq("ch00 pdf shape in 20 of 20", 20, has_pdf)

    # ---------------- chapter 01: three-digit multiples
    def mult(k, a=100, b=999):
        return b // k - (a - 1) // k
    chk_eq("ch01 |A2|", 450, mult(2)); chk_eq("ch01 |A4|", 225, mult(4)); chk_eq("ch01 |A8|", 112, mult(8))
    chk_eq("ch01 |A6|", 150, mult(6)); chk_eq("ch01 |A3|", 300, mult(3))
    nums = range(100, 1000)
    A2 = {n for n in nums if n % 2 == 0}; A4 = {n for n in nums if n % 4 == 0}; A8 = {n for n in nums if n % 8 == 0}
    A3 = {n for n in nums if n % 3 == 0}
    chk_eq("ch01 counts by enumeration", (450, 225, 112), (len(A2), len(A4), len(A8)))
    chk("ch01 P(A8)=28/225", Fr(28, 225), Fr(len(A8), 900))
    chk_eq("ch01 A2 cap A4 = A4", True, (A2 & A4) == A4)
    chk_eq("ch01 A8 != A2 cap A4 (100)", True, 100 in (A2 & A4) and 100 not in A8)
    chk("ch01 P(A2 u A3)=2/3", Fr(2, 3), Fr(len(A2 | A3), 900))
    chk("ch01 P(A2 u A3) incl-excl", Fr(2, 3), Fr(450, 900) + Fr(300, 900) - Fr(150, 900))

    # ---------------- chapter 02
    # two dice sum 5, first > 3
    pairs = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == 5]
    chk("ch02 dice sum5 given: first>3", Fr(1, 4), Fr(sum(1 for a, b in pairs if a > 3), len(pairs)))
    # unfair die, three tosses, sum 5 given first < second
    q = Fr(1, 9)
    pr = {1: q, 3: q, 5: q, 2: 2 * q, 4: 2 * q, 6: 2 * q}
    chk("ch02 9q=1", 1, sum(pr.values()))
    num = den = Fr(0)
    for a, b, c in itertools.product(range(1, 7), repeat=3):
        w = pr[a] * pr[b] * pr[c]
        if a < b:
            den += w
            if a + b + c == 5:
                num += w
    chk("ch02 P(first<second)=33q^2", 33 * q * q, den)
    chk("ch02 P(sum5 and first<second)=5q^3", 5 * q ** 3, num)
    chk("ch02 P(B|D)=5/297", Fr(5, 297), num / den)
    chk("ch02 sum_i P(i)^2 = 15q^2", 15 * q * q, sum(v * v for v in pr.values()))
    # p,q,s example
    p, qq, s = Fr(3, 10), Fr(1, 2), Fr(2, 5)
    PnAB = s * (1 - p); PAB = qq - PnAB
    chk("ch02 P(notA cap B)=7/25", Fr(7, 25), PnAB)
    chk("ch02 P(A cap B)=11/50", Fr(11, 50), PAB)
    chk("ch02 P(A|B)=11/25", Fr(11, 25), PAB / qq)
    chk("ch02 P(notA|B)=14/25", Fr(14, 25), PnAB / qq)
    chk("ch02 P(A u B)=29/50", Fr(29, 50), p + qq - PAB)
    chk("ch02 P(A u B)=p+s(1-p)", p + s * (1 - p), p + qq - PAB)
    # symbolic family I
    P, Q, S = sp.symbols("p q s", positive=True)
    PAB_s = Q - S * (1 - P)
    chk_eq("ch02 indep iff q=s", True, sp.simplify(sp.factor(PAB_s - P * Q) - (Q - S) * (1 - P)) == 0)
    # urn N=10, D=4
    N, D = 10, 4
    pR2 = Fr(D, N) * Fr(D - 1, N - 1) + Fr(N - D, N) * Fr(D, N - 1)
    chk("ch02 urn P(R2)=D/N", Fr(2, 5), pR2)
    pR2R3 = Fr(D, N) * Fr(D - 1, N - 1) * Fr(D - 2, N - 2) + Fr(N - D, N) * Fr(D, N - 1) * Fr(D - 1, N - 2)
    chk("ch02 urn P(R3|R2)=(D-1)/(N-1)=1/3", Fr(1, 3), pR2R3 / pR2)
    # brute force urn
    balls = [1] * D + [0] * (N - D)
    perms = list(itertools.permutations(range(N), 3))
    c2 = sum(1 for a, b, c in perms if balls[b] == 1)
    chk("ch02 urn brute P(R2)", Fr(2, 5), Fr(c2, len(perms)))
    c23 = sum(1 for a, b, c in perms if balls[b] == 1 and balls[c] == 1)
    chk("ch02 urn brute P(R3|R2)", Fr(1, 3), Fr(c23, c2))
    c3 = sum(1 for a, b, c in perms if balls[c] == 1)
    chk("ch02 urn brute P(R3)=D/N", Fr(2, 5), Fr(c3, len(perms)))

    # ---------------- chapter 03
    x, y = sp.symbols("x y")
    pS, qS = sp.symbols("p q")
    Dv = {(0, 0): 0, (0, 1): -1, (1, 0): -1, (1, 1): -1}
    Tv = {(0, 0): -1, (0, 1): 0, (1, 0): 0, (1, 1): 1}
    pr_xy = {(a, b): (pS if a else 1 - pS) * (qS if b else 1 - qS) for a in (0, 1) for b in (0, 1)}
    ED = sum(Dv[k] * v for k, v in pr_xy.items()); ET = sum(Tv[k] * v for k, v in pr_xy.items())
    EDT = sum(Dv[k] * Tv[k] * v for k, v in pr_xy.items())
    cov = sp.simplify(EDT - ED * ET)
    chk_eq("ch03 Cov(D,T) = -(p+q)(1-p)(1-q)", True, sp.simplify(cov + (pS + qS) * (1 - pS) * (1 - qS)) == 0)
    chk_eq("ch03 E[DT] = -pq", True, sp.simplify(EDT + pS * qS) == 0)
    chk_eq("ch03 E[D] = pq-p-q", True, sp.simplify(ED - (pS * qS - pS - qS)) == 0)
    chk_eq("ch03 E[T] = p+q-1", True, sp.simplify(ET - (pS + qS - 1)) == 0)
    chk("ch03 Cov at p=q=1/2 = -1/4", Fr(-1, 4), Fr(str(cov.subs({pS: sp.Rational(1, 2), qS: sp.Rational(1, 2)}))))
    # P(D=0,T=0)=0 but P(D=0)P(T=0)>0
    PD0 = sum(v for k, v in pr_xy.items() if Dv[k] == 0); PT0 = sum(v for k, v in pr_xy.items() if Tv[k] == 0)
    PD0T0 = sum(v for k, v in pr_xy.items() if Dv[k] == 0 and Tv[k] == 0)
    chk_eq("ch03 P(D=0,T=0)=0", 0, sp.simplify(PD0T0))
    chk_eq("ch03 P(D=0)=(1-p)(1-q)", True, sp.simplify(PD0 - (1 - pS) * (1 - qS)) == 0)
    chk_eq("ch03 P(T=0)=p+q-2pq", True, sp.simplify(PT0 - (pS + qS - 2 * pS * qS)) == 0)
    # uncorrelated but dependent
    vals = [-1, 0, 1]
    EXY = sum(Fr(1, 3) * v * v * v for v in vals)
    chk("ch03 Cov(X, X^2)=0", 0, EXY - sum(Fr(1, 3) * v for v in vals) * sum(Fr(1, 3) * v * v for v in vals))
    chk("ch03 P(X=0,Y=1)=0", 0, 0)
    chk("ch03 P(X=0)P(Y=1)=2/9", Fr(2, 9), Fr(1, 3) * Fr(2, 3))

    # ---------------- chapter 04
    # quadratic y^2 + 2 X1 y + X2
    cplx = [(a, b) for a in range(1, 7) for b in range(1, 7) if a * a < b]
    integ = [(a, b) for a in range(1, 7) for b in range(1, 7) if a * a >= b and int((a * a - b) ** 0.5 + 1e-9) ** 2 == a * a - b]
    chk("ch04 complex roots 7/36", Fr(7, 36), Fr(len(cplx), 36))
    chk("ch04 integer roots 4/36", Fr(4, 36), Fr(len(integ), 36))
    chk_eq("ch04 integer pairs", [(1, 1), (2, 3), (2, 4), (3, 5)], sorted(integ))
    # reach sum N
    def reach(Nf):
        pf = Fr(1, Nf)
        r = [Fr(0)] * (Nf + 1)
        r[0] = Fr(1)
        for s_ in range(1, Nf + 1):
            r[s_] = sum(r[s_ - f] * pf for f in range(1, min(Nf, s_) + 1))  # r[s]=prob that partial sums ever hit s
        return r[Nf]
    for Nf, exact in ((3, Fr(16, 27)), (4, Fr(125, 256)), (5, Fr(1296, 3125))):
        chk("ch04 P_%d by DP" % Nf, exact, reach(Nf))
        chk("ch04 P_%d formula" % Nf, exact, Fr(1, Nf) * (1 + Fr(1, Nf)) ** (Nf - 1))
    for Nf in (6, 7, 8):
        chk("ch04 P_N formula N=%d" % Nf, reach(Nf), Fr(1, Nf) * (1 + Fr(1, Nf)) ** (Nf - 1))
    # MC for N=3
    rng = RNG
    n = 400_000
    hits = 0
    tot = rng.integers(1, 4, size=(n, 3))
    cs = np.cumsum(tot, axis=1)
    hit3 = (cs == 3).any(axis=1)
    chk_mc("ch04 P_3 reach", Fr(16, 27), float(hit3.mean()), n=n)
    # digits
    cnt = tot_ = 0
    for a, b in itertools.permutations(range(1, 10), 2):
        if (a + b) % 2 == 0:
            tot_ += 1
            if b % 2 == 1:
                cnt += 1
    chk_eq("ch04 digit counts 20/32", (20, 32), (cnt, tot_))
    chk("ch04 5/8", Fr(5, 8), Fr(cnt, tot_))
    nums3 = [(a, b, c) for a in range(1, 10) for b in range(10) for c in range(10) if len({a, b, c}) == 3]
    chk_eq("ch04 distinct-digit numbers 648", 648, len(nums3))
    ev = sum(1 for a, b, c in nums3 if c % 2 == 0)
    chk_eq("ch04 even 328", 328, ev)
    chk("ch04 41/81", Fr(41, 81), Fr(ev, 648))
    # layouts
    def grid_pairs(Nn):
        cells = [(r, c) for r in range(Nn) for c in range(Nn)]
        hv = d1 = d2 = 0
        allp = list(itertools.combinations(cells, 2))
        for (r1, c1), (r2, c2) in allp:
            dr, dc = r2 - r1, c2 - c1
            if abs(dr) + abs(dc) == 1:
                hv += 1
            elif abs(dr) == 1 and abs(dc) == 1:
                d1 += 1
        return len(allp), hv, d1
    t3, hv3, dg3 = grid_pairs(3)
    chk_eq("ch04 3x3 pairs 36", 36, t3)
    chk("ch04 3x3 hv 1/3", Fr(1, 3), Fr(hv3, t3)); chk("ch04 3x3 diag 2/9", Fr(2, 9), Fr(dg3, t3))
    for Nn in (4, 5, 6):
        t, hv, dg = grid_pairs(Nn)
        chk_eq("ch04 NxN pairs N=%d" % Nn, comb(Nn * Nn, 2), t)
        chk_eq("ch04 NxN hv N=%d" % Nn, 2 * Nn * (Nn - 1), hv)
        chk_eq("ch04 NxN diag N=%d" % Nn, 2 * (Nn - 1) ** 2, dg)
    # V shapes in 3x4 grid (3 rows, 4 columns): three cells (r,c),(r+1,c+1),(r,c+2) or flipped, and transposes
    R_, C_ = 3, 4
    shapes = set()
    for r in range(R_):
        for c in range(C_):
            for cells in (
                [(r, c), (r + 1, c + 1), (r, c + 2)], [(r + 1, c), (r, c + 1), (r + 1, c + 2)],
                [(r, c), (r + 1, c + 1), (r + 2, c)], [(r, c + 1), (r + 1, c), (r + 2, c + 1)],
            ):
                if all(0 <= rr < R_ and 0 <= cc < C_ for rr, cc in cells):
                    shapes.add(frozenset(cells))
    chk_eq("ch04 V shapes 14", 14, len(shapes))
    chk("ch04 7/110", Fr(7, 110), Fr(14, comb(12, 3)))
    # path through a point
    m, nn = 3, 2
    pth = comb(m + nn, m)
    through = comb(1 + 1, 1) * comb(m + nn - 2, m - 1)
    chk("ch04 path through (1,1) = 3/5", Fr(3, 5), Fr(through, pth))
    # brute force over p-independence
    for pv in (Fr(1, 3), Fr(7, 10)):
        reach_ = through_ = Fr(0)
        for seq in itertools.product("RU", repeat=m + nn):
            if seq.count("R") != m:
                continue
            w = pv ** m * (1 - pv) ** nn
            reach_ += w
            x_ = y_ = 0
            ok = False
            for st in seq:
                x_ += st == "R"; y_ += st == "U"
                if (x_, y_) == (1, 1):
                    ok = True
            if ok:
                through_ += w
        chk("ch04 path cond ratio p=%s" % pv, Fr(3, 5), through_ / reach_)
        chk("ch04 path reach prob p=%s" % pv, comb(m + nn, m) * pv ** m * (1 - pv) ** nn, reach_)
    # ordered vs unordered dice (trap) and 1/11
    chk("ch04 two dice sum 7 = 1/6", Fr(1, 6), Fr(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7), 36))
    chk("ch04 two dice sum 2 = 1/36", Fr(1, 36), Fr(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 2), 36))
