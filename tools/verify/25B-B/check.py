# -*- coding: utf-8 -*-
"""Verification harness for 25B-B (probability). Run: PYTHONUTF8=1 py tools/verify/25B-B/check.py
Each final answer: EXACT (fractions / enumeration / sympy) and MC (>= 10^6 trials, within 4 SE). ASCII output only.
Symbolic answers are checked at sample parameter values (and as polynomial identities with sympy where possible).
Q2 part f (bonus, disjoint events): the official key s=q DISAGREES with the exact analysis (see the end of this file);
the item is held and the disagreement is reported, the official key is never changed."""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20250812)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se + 1e-12
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


def clip(poly, a, b, c):  # keep a*x+b*y+c >= 0
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * p[0] + b * p[1] + c, a * q[0] + b * q[1] + c
        if fp >= 0:
            out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def area(poly):
    s = Fr(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


# ============================================================ Q1  (|X1-X2| for independent uniforms on (0,1))
sq = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(1), Fr(1)), (Fr(0), Fr(1))]
X1 = rng.random(N)
X2 = rng.random(N)
Xd = np.abs(X1 - X2)


def band(t):
    poly = clip(sq, Fr(1), Fr(-1), t)       # x1 - x2 + t >= 0
    poly = clip(poly, Fr(-1), Fr(1), t)     # x2 - x1 + t >= 0
    return area(poly) if len(poly) >= 3 else Fr(0)


rec("Q1b", "P(X<1/2)=3/4", Fr(3, 4), band(Fr(1, 2)), float((Xd < 0.5).mean()), se_p(0.75), tol=0)
rec("Q1c", "P(X>3/2)=0", 0, 1 - band(Fr(3, 2)), float((Xd > 1.5).mean()), 1e-9, tol=0)
for t in (Fr(1, 10), Fr(1, 3), Fr(7, 10), Fr(9, 10)):
    off = 2 * t - t * t
    rec("Q1d", "F(%s)" % t, off, band(t), float((Xd <= float(t)).mean()), se_p(float(off)), tol=0)
tt = sp.symbols("t")
F_sym = 2 * tt - tt ** 2
rows.append(("Q1e", "f=F'=2(1-t), integral over (0,1) = 1", sp.simplify(sp.diff(F_sym, tt) - 2 * (1 - tt)) == 0 and sp.integrate(2 * (1 - tt), (tt, 0, 1)) == 1, True, ""))
Ex = sp.integrate(tt * 2 * (1 - tt), (tt, 0, 1))
rec("Q1f", "E[X]=1/3", Fr(1, 3), Fr(Ex.p, Ex.q), float(Xd.mean()), se_mean(Xd), tol=0)

# ============================================================ Q2  (P(~A|B)=p, P(A|~B)=q, P(A or B)=s)
rows_q2 = []
for (a, b, c) in ((Fr(1, 10), Fr(2, 10), Fr(15, 100)), (Fr(2, 10), Fr(1, 10), Fr(3, 10)), (Fr(5, 100), Fr(3, 10), Fr(1, 10))):
    d = 1 - a - b - c
    pp = c / (a + c)             # P(~A|B)
    qq = b / (b + d)             # P(A|~B)
    ss = a + b + c               # P(A or B)
    PB = (ss - qq) / (1 - qq)
    PA = ss - pp * PB
    PAB = (1 - pp) * PB
    cum = np.cumsum([float(a), float(b), float(c), float(d)])
    idx = np.searchsorted(cum, rng.random(N))
    A = (idx == 0) | (idx == 1)
    B = (idx == 0) | (idx == 2)
    rec("Q2a", "P(A) (%s,%s,%s)" % (a, b, c), PA, a + b, float(A.mean()), se_p(float(PA)), tol=0)
    rec("Q2b", "P(B)", PB, a + c, float(B.mean()), se_p(float(PB)), tol=0)
    rec("Q2c", "P(A&B)", PAB, a, float((A & B).mean()), se_p(float(PAB)), tol=0)
    rows.append(("Q2d", "q<=s here (s-q>=0 gives P(B)>=0)", qq <= ss, True, ""))
# q > s forces a negative P(B) (for q<1)
rows.append(("Q2d", "q>s => P(B)=(s-q)/(1-q)<0", all((s_ - q_) / (1 - q_) < 0 for q_, s_ in ((Fr(1, 2), Fr(1, 4)), (Fr(3, 5), Fr(1, 5)))), True, ""))
# independence iff p = 1-q: build an independent pair and a dependent pair
pa_, pb_ = Fr(2, 5), Fr(1, 3)
a_ = pa_ * pb_
b_ = pa_ - a_
c_ = pb_ - a_
d_ = 1 - a_ - b_ - c_
p_ind = c_ / (a_ + c_)
q_ind = b_ / (b_ + d_)
rows.append(("Q2e", "independent pair: p=1-q", p_ind == 1 - q_ind, True, "p=%s q=%s" % (p_ind, q_ind)))
dep = (Fr(1, 10), Fr(2, 10), Fr(15, 100))
rows.append(("Q2e", "dependent pair: p != 1-q", dep[2] / (dep[0] + dep[2]) != 1 - dep[1] / (dep[1] + (1 - sum(dep))), True, ""))
# DISAGREEMENT (Q2f, bonus): disjoint A,B (P(A&B)=0, B non-empty prob>0) forces p = P(~A|B) = 1, and s,q are then free.
a0, b0, c0 = Fr(0), Fr(1, 4), Fr(1, 5)
d0 = 1 - b0 - c0
p0 = c0 / (a0 + c0)
q0 = b0 / (b0 + d0)
s0 = b0 + c0
q2f_official_ok = (s0 == q0)           # official key says disjoint iff s = q
q2f_true = (p0 == 1)
print("Q2f disjoint example: p=%s q=%s s=%s | official key (s=q) holds: %s | true condition (p=1) holds: %s" % (p0, q0, s0, q2f_official_ok, q2f_true))
print("Q2f also: s=q gives P(B)=(s-q)/(1-q)=0, i.e. B has probability zero, not a nonempty-event disjointness condition.")
Q2F_DISAGREES = (not q2f_official_ok) and q2f_true

# ============================================================ Q3  (head's guess vs number, N^2 pairs)
for n, m in ((5, 7), (9, 4), (2, 6)):
    pairs = [(g, j) for g in range(1, n + 1) for j in range(1, n + 1)]
    g1 = rng.integers(1, n + 1, N)
    j1 = rng.integers(1, n + 1, N)
    rec("Q3a", "N=%d P(correct)=1/N" % n, Fr(1, n), Fr(sum(1 for g, j in pairs if g == j), len(pairs)), float((g1 == j1).mean()), se_p(1 / n), tol=0)
    off = Fr(2 * (n - 1), n * n)
    rec("Q3b", "N=%d P(neighbour)=2(N-1)/N^2" % n, off, Fr(sum(1 for g, j in pairs if abs(g - j) == 1), len(pairs)), float((np.abs(g1 - j1) == 1).mean()), se_p(float(off)), tol=0)
    g2 = rng.integers(1, m + 1, N)
    j2 = rng.integers(1, m + 1, N)
    A1 = g1 == j1
    A2 = g2 == j2
    rec("Q3c", "N=%d M=%d both correct" % (n, m), Fr(1, n * m), Fr(1, n) * Fr(1, m), float((A1 & A2).mean()), se_p(1 / (n * m)), tol=0)
    off = Fr(1, n) + Fr(1, m) - Fr(1, n * m)
    rec("Q3d", "N=%d M=%d at least one" % (n, m), off, 1 - (1 - Fr(1, n)) * (1 - Fr(1, m)), float((A1 | A2).mean()), se_p(float(off)), tol=0)
    off = Fr(1, n) * Fr(2 * (m - 1), m * m)
    nb2 = np.abs(g2 - j2) == 1
    rec("Q3e", "N=%d M=%d eugene correct and esther neighbour" % (n, m), off, Fr(1, n) * Fr(sum(1 for g in range(1, m + 1) for j in range(1, m + 1) if abs(g - j) == 1), m * m),
        float((A1 & nb2).mean()), se_p(float(off)), tol=0)

# ============================================================ Q4
x = sp.symbols("x", real=True)
a_, b_, c_, d_ = sp.symbols("a b c d")
mu = sp.symbols("mu")
norm = sp.integrate(b_ * x + c_, (x, -1, 0)) + sp.integrate(d_, (x, 0, 1)) - 1
sym = sp.integrate(b_ * x + c_, (x, -1, 0)) - sp.integrate(d_, (x, 0, 1))
mean = sp.integrate(x * (b_ * x + c_), (x, -1, 0)) + sp.integrate(x * d_, (x, 0, 1)) - mu
sol = sp.solve([norm, sym, mean], [b_, c_, d_], dict=True)[0]
rows.append(("Q4a", "b=12mu, c=6mu+1/2, d=1/2 (sympy)", sp.simplify(sol[b_] - 12 * mu) == 0 and sp.simplify(sol[c_] - (6 * mu + sp.Rational(1, 2))) == 0 and sol[d_] == sp.Rational(1, 2), True, ""))
rows.append(("Q4a", "a=0 and g=h=0 needed for convergence", sp.integrate(1 / x, (x, 1, sp.oo)) == sp.oo, True, "int 1/x diverges"))
for mv in (sp.Rational(-1, 12), sp.Rational(-1, 24), sp.Rational(1, 24), sp.Rational(1, 12)):
    mf = float(mv)
    bb = 12 * mf
    cc = 6 * mf + 0.5
    # sample: left mass 1/2 with density bb x + cc on [-1,0] (inverse cdf), right mass 1/2 uniform on [0,1]
    left = rng.random(N) < 0.5
    u = rng.random(N)
    # conditional cdf on [-1,0]: G(t) = 2*[(bb/2)(t^2-1) + cc (t+1)]
    if abs(bb) < 1e-12:
        Xl = -1 + u
    else:
        # solve (bb/2) t^2 + cc t + (cc - bb/2) - u/2 = 0 for t in [-1,0]
        A_ = bb / 2
        B_ = cc
        C_ = cc - bb / 2 - u / 2
        disc = B_ * B_ - 4 * A_ * C_
        r1 = (-B_ + np.sqrt(disc)) / (2 * A_)
        r2 = (-B_ - np.sqrt(disc)) / (2 * A_)
        Xl = np.where((r1 >= -1 - 1e-9) & (r1 <= 1e-9), r1, r2)
    Xs = np.where(left, Xl, rng.random(N))
    rec("Q4a", "E[X] mu=%s" % mv, mf, float(sp.integrate(x * (12 * mv * x + 6 * mv + sp.Rational(1, 2)), (x, -1, 0)) + sp.integrate(x / 2, (x, 0, 1))), float(Xs.mean()), se_mean(Xs), tol=1e-12)

    def Fo(t, m_=mf):
        if t < -1:
            return 0.0
        if t < 0:
            return 0.5 * (t + 1) * (12 * m_ * t + 1)
        return (t + 1) / 2 if t < 1 else 1.0

    def Fex(t, mv=mv):
        if t < -1:
            return 0.0
        if t < 0:
            return float(sp.integrate(12 * mv * x + 6 * mv + sp.Rational(1, 2), (x, -1, t)))
        return float(sp.integrate(12 * mv * x + 6 * mv + sp.Rational(1, 2), (x, -1, 0)) + sp.integrate(sp.Rational(1, 2), (x, 0, t))) if t < 1 else 1.0

    for t in (-0.7, -0.5, -0.2, 0.3, 0.8):
        rec("Q4c", "F(%.1f) mu=%s" % (t, mv), Fo(t), Fex(t), float((Xs <= t).mean()), se_p(Fo(t)), tol=1e-12)
    off = (1 + 6 * mf) / (3 + 6 * mf)
    ev = Xs > -0.5
    rec("Q4d", "P(X<0|X>-1/2) mu=%s" % mv, off, (Fex(0) - Fex(-0.5)) / (1 - Fex(-0.5)), float((Xs[ev] < 0).mean()), se_p(off, int(ev.sum())), tol=1e-12)
rows.append(("Q4b", "f>=0 at both ends iff |mu|<=1/12",
             all(((0.5 - 6 * m_ >= 0 and 6 * m_ + 0.5 >= 0) == (abs(m_) <= 1 / 12 + 1e-15)) for m_ in (-0.1, -1 / 12, 0, 1 / 12, 0.1)), True, ""))

# ============================================================ Q5  (new circuit with random placement of A,B,C)
p = sp.symbols("p")


def q0(A, B, C):
    return (A and B) or C


def prob_poly(f):
    tot = 0
    for st in itertools.product((0, 1), repeat=3):
        if f(*st):
            k = sum(st)
            tot += p ** k * (1 - p) ** (3 - k)
    return sp.expand(tot)


perms = list(itertools.permutations(range(3)))          # placement of (A,B,C) into (R1,R2,L1)


def qprime(perm, st):
    r1, r2, l1 = st[perm[0]], st[perm[1]], st[perm[2]]
    return (r1 and r2) or l1


P0 = prob_poly(q0)
P0Q = sum(prob_poly(lambda *st, pm=pm: q0(*st) and qprime(pm, st)) for pm in perms) / 6
Pq = sum(prob_poly(lambda *st, pm=pm: qprime(pm, st)) for pm in perms) / 6
rows.append(("Q5a", "P(Q0)=p(1+p-p^2)", sp.expand(P0 - p * (1 + p - p ** 2)) == 0, True, ""))
rows.append(("Q5b", "P(any placed circuit) = p(1+p-p^2)", sp.expand(Pq - p * (1 + p - p ** 2)) == 0, True, ""))
rows.append(("Q5c", "P(Q0 and Q') = p(1+7p-5p^2)/3", sp.expand(P0Q - p * (1 + 7 * p - 5 * p ** 2) / 3) == 0, True, ""))
rows.append(("Q5d", "P(Q'|Q0) = (1+7p-5p^2)/(3(1+p-p^2))", sp.simplify(P0Q / P0 - (1 + 7 * p - 5 * p ** 2) / (3 * (1 + p - p ** 2))) == 0, True, ""))
rows.append(("Q5e", "P(Q'|~Q0) = 2p/(3(1+p))", sp.simplify((Pq - P0Q) / (1 - P0) - 2 * p / (3 * (1 + p))) == 0, True, ""))
rows.append(("Q5c", "III placement P(Q0 and Q3)=3p^2-2p^3",
             sp.expand(prob_poly(lambda A, B, C: q0(A, B, C) and ((A and C) or B)) - (3 * p ** 2 - 2 * p ** 3)) == 0, True, ""))
for pf in (0.3, 0.6, 0.85):
    st = rng.random((N, 3)) < pf
    A_, B_, C_ = st[:, 0], st[:, 1], st[:, 2]
    q0v = (A_ & B_) | C_
    pm_idx = rng.integers(0, 6, N)
    qp = np.zeros(N, dtype=bool)
    for i, pm in enumerate(perms):
        cols = [st[:, pm[0]], st[:, pm[1]], st[:, pm[2]]]
        qp |= (pm_idx == i) & ((cols[0] & cols[1]) | cols[2])
    v0 = pf * (1 + pf - pf ** 2)
    v02 = pf * (1 + 7 * pf - 5 * pf ** 2) / 3
    rec("Q5a", "P(Q0) p=%.2f" % pf, v0, float(P0.subs(p, pf)), float(q0v.mean()), se_p(v0), tol=1e-12)
    rec("Q5c", "P(Q0&Q') p=%.2f" % pf, v02, float(P0Q.subs(p, pf)), float((q0v & qp).mean()), se_p(v02), tol=1e-12)
    vc = (1 + 7 * pf - 5 * pf ** 2) / (3 * (1 + pf - pf ** 2))
    rec("Q5d", "P(Q'|Q0) p=%.2f" % pf, vc, float((P0Q / P0).subs(p, pf)), float(qp[q0v].mean()), se_p(vc, int(q0v.sum())), tol=1e-12)
    ve = 2 * pf / (3 * (1 + pf))
    rec("Q5e", "P(Q'|~Q0) p=%.2f" % pf, ve, float(((Pq - P0Q) / (1 - P0)).subs(p, pf)), float(qp[~q0v].mean()), se_p(ve, int((~q0v).sum())), tol=1e-12)


# ============================================================ Q6  (two urns, n balls moved)
def urn_exact(N1, D1, N2, D2, n, swap=False):
    """exact P(red from urn 2) and P(all moved are original-red | red) by enumerating subsets of urn 1."""
    c1 = [1] * D1 + [0] * (N1 - D1)
    tot = Fr(0)
    allred = Fr(0)
    cnt = 0
    for s1 in itertools.combinations(range(N1), n):
        cnt += 1
        reds = sum(c1[i] for i in s1)
        moved_red = (n - reds) if swap else reds
        pr = Fr(D2 + moved_red, N2 + n)
        tot += pr
        if reds == n:
            allred += pr
    tot /= cnt
    allred /= cnt
    return tot, allred / tot


for (N1, D1, N2, D2, n) in ((8, 3, 6, 2, 3), (7, 5, 5, 1, 4), (9, 4, 4, 3, 2)):
    p_red, p_all = urn_exact(N1, D1, N2, D2, n)
    off1 = (D2 + Fr(n * D1, N1)) / (N2 + n)
    off2 = Fr(D2 + n, N2 + n) * Fr(math.comb(D1, n), math.comb(N1, n)) / ((D2 + Fr(n * D1, N1)) / (N2 + n))
    p_red_sw, _ = urn_exact(N1, D1, N2, D2, n, swap=True)
    off3 = (D2 + n * (1 - Fr(D1, N1))) / (N2 + n)
    # Monte Carlo
    M = 1_000_000
    r1 = np.argsort(rng.random((M, N1), dtype=np.float32), axis=1)[:, :n]
    nred = (r1 < D1).sum(axis=1)
    r2 = np.argsort(rng.random((M, N2 + n), dtype=np.float32), axis=1)[:, 0]
    # urn 2 holds D2 red + (N2-D2) black + moved balls; index < D2 -> red, index in [N2, N2+k) -> moved red
    def drew_red(moved_red):
        return (r2 < D2) | ((r2 >= N2) & (r2 < N2 + moved_red))
    red1 = drew_red(nred)
    tag = "N1=%d D1=%d N2=%d D2=%d n=%d" % (N1, D1, N2, D2, n)
    rec("Q6a", "P(red) " + tag, off1, p_red, float(red1.mean()), se_p(float(off1), M), tol=0)
    rec("Q6b", "P(all moved red | red) " + tag, off2, p_all, float((nred == n)[red1].mean()), se_p(float(off2), int(red1.sum())), tol=0)
    red2 = drew_red(n - nred)
    rec("Q6c", "P(red) swapped " + tag, off3, p_red_sw, float(red2.mean()), se_p(float(off3), M), tol=0)

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
print("Q2f official key (s=q) disagrees with exact analysis (true condition: p=1): %s -> item held" % Q2F_DISAGREES)
sys.exit(1 if (bad or not Q2F_DISAGREES) else 0)
