# -*- coding: utf-8 -*-
"""Verification harness for 26A-A (probability). Run: PYTHONUTF8=1 py tools/verify/26A-A/check.py
Each final answer: EXACT (fractions / enumeration / sympy) and MC (>= 10^6 trials, within 4 SE). ASCII output only.
Symbolic answers are checked at sample parameter values."""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20260209)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_cond(p, n):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def se_mean(v):
    return float(v.std() / math.sqrt(len(v)))


def se_var(v):
    return math.sqrt((np.mean((v - v.mean()) ** 4) - v.var() ** 2) / len(v))


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se + 1e-12
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1  (exact area by half-plane clipping, Fractions)
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


h = Fr(1, 2)
sq = [(Fr(0), Fr(0)), (h, Fr(0)), (h, h), (Fr(0), h)]
# half-planes a*x1 + b*x2 + c >= 0 ; mid = 1 - x1 - x2
L_lt_R = (-1, 1, 0)       # x2 > x1
L_lt_M = (-2, -1, 1)      # 1 - 2x1 - x2 > 0
R_gt_M = (1, 2, -1)       # x1 + 2x2 - 1 > 0
M_gt_R = (-1, -2, 1)      # 1 - x1 - 2x2 > 0


def prob(conds):
    poly = sq
    for a, b, c in conds:
        poly = clip(poly, Fr(a), Fr(b), Fr(c))
    return area(poly) / Fr(1, 4) if len(poly) >= 3 else Fr(0)


X1 = rng.random(N) / 2
X2 = rng.random(N) / 2
M = 1 - X1 - X2
cases = {
    "Q1a": (Fr(5, 12), [L_lt_R, L_lt_M], (X1 < X2) & (X1 < M)),
    "Q1b": (Fr(1, 6), [L_lt_R, R_gt_M], (X2 > X1) & (X2 > M)),
    "Q1c": (Fr(1, 12), [L_lt_R, L_lt_M, R_gt_M], (X1 < X2) & (X1 < M) & (X2 > M)),
    "Q1d": (Fr(2, 3), [L_lt_M, M_gt_R], (M > X1) & (M > X2)),
}
for k, (off, conds, ev) in cases.items():
    rec(k, "P", off, prob(conds), float(ev.mean()), se_p(float(off)), tol=0)
near = (np.abs(X1 - X2) < 1e-6) & (np.abs(X1 - M) < 1e-6)
rec("Q1e", "P(all equal)=0 (measure zero; MC of 1e-6 near-equality)", 0, 0, float(near.mean()), 1e-6)

# ============================================================ Q2  (geometric duel, Q = p/(2-p))
for p in (Fr(3, 10), Fr(1, 2), Fr(4, 5)):
    Qv = p / (2 - p)
    pf = float(p)
    K = 600
    ge = [pf * (1 - pf) ** (k - 1) for k in range(1, K)]
    tail = [(1 - pf) ** k for k in range(1, K)]
    tie = sum(g * g for g in ge)
    win_B = sum(ge[k - 1] * tail[k - 1] for k in range(1, K))
    g1 = rng.geometric(pf, N)
    g2 = rng.geometric(pf, N)
    rec("Q2b", "Q=p/(2-p) at p=%s" % p, Qv, tie, float(np.mean(g1 == g2)), se_p(float(Qv)), tol=1e-12)
    rec("Q2b", "p=2Q/(1+Q) at p=%s" % p, p, 2 * Qv / (1 + Qv), float(p), 0, tol=0)
    rec("Q2a", "P_B=(1-Q)/2 at p=%s" % p, (1 - Qv) / 2, win_B, float(np.mean(g2 < g1)), se_p(float((1 - Qv) / 2)), tol=1e-12)
    for k in (1, 2, 5):
        off = 4 * Qv / (1 + Qv) ** 2 * ((1 - Qv) / (1 + Qv)) ** (2 * (k - 1))
        ev = g1 == g2
        rec("Q2c", "p=%s k=%d" % (p, k), off, ge[k - 1] ** 2 / tie, float(np.mean(g1[ev] == k)),
            se_cond(float(off), int(ev.sum())), tol=1e-12)
        ev = g2 < g1
        rec("Q2d", "p=%s k=%d" % (p, k), off, ge[k - 1] * tail[k - 1] / win_B, float(np.mean(g2[ev] == k)),
            se_cond(float(off), int(ev.sum())), tol=1e-12)
    ev = g1 == g2
    off_e = (1 + Qv) ** 2 / (4 * Qv)
    ex_e = sum(k * ge[k - 1] ** 2 for k in range(1, K)) / tie
    rec("Q2e", "E[T|tie] p=%s" % p, off_e, ex_e, float(g1[ev].mean()), se_mean(g1[ev]), tol=1e-9)

# ============================================================ Q3  (P(A)=p, P(B|A)=q, P(B|~A)=s)
p, q, s = Fr(3, 10), Fr(7, 10), Fr(2, 5)
pmf = {(1, 1): p * q, (1, 0): p * (1 - q), (0, 1): (1 - p) * s, (0, 0): (1 - p) * (1 - s)}
Aa = rng.random(N) < float(p)
Bb = np.where(Aa, rng.random(N) < float(q), rng.random(N) < float(s))
S1 = Aa & Bb
S2 = Aa | Bb
ex_Q1 = pmf[(1, 1)]
ex_Q2 = sum(v for (a, b), v in pmf.items() if a or b)
rec("Q3a", "P(Q1)=pq", p * q, ex_Q1, float(S1.mean()), se_p(float(p * q)), tol=0)
rec("Q3b", "P(Q2)=p+s(1-p)", p + s * (1 - p), ex_Q2, float(S2.mean()), se_p(float(p + s * (1 - p))), tol=0)
off = p * q / (p + s * (1 - p))
rec("Q3c", "P(Q1|Q2)", off, ex_Q1 / ex_Q2, float(S1[S2].mean()), se_cond(float(off), int(S2.sum())), tol=0)
rec("Q3d", "P(Q1 or Q2)=P(Q2)", p + s * (1 - p), ex_Q2, float((S1 | S2).mean()), se_p(float(ex_Q2)), tol=0)

# ============================================================ Q4
x = sp.symbols("x", real=True)
for mu in (sp.Rational(1, 2), sp.Rational(-1, 3), sp.Rational(1), sp.Rational(-1), sp.Rational(0), sp.Rational(3, 4)):
    a_, b_ = sp.symbols("a b")
    area_ = a_ * sp.integrate(sp.exp(x), (x, -sp.oo, 0)) + b_ * sp.integrate((1 - x) ** 2, (x, 0, 2))
    mean_ = a_ * sp.integrate(x * sp.exp(x), (x, -sp.oo, 0)) + b_ * sp.integrate(x * (1 - x) ** 2, (x, 0, 2))
    sol = sp.solve([area_ - 1, mean_ - mu], [a_, b_], dict=True)[0]
    oa, ob = (1 - mu) / 2, sp.Rational(3, 4) * (1 + mu)
    rows.append(("Q4a", "a,b at mu=%s (sympy solve)" % mu,
                 sp.simplify(sol[a_] - oa) == 0 and sp.simplify(sol[b_] - ob) == 0, True, "a=%s b=%s c=0" % (oa, ob)))
    ma, mb = float(oa), float(ob)
    # sample: with prob ma the exponential left tail, else the [0,2] part by inverse CDF of b(1-x)^2 : F=(b/3)((t-1)^3+1)
    pick = rng.random(N) < ma
    u = rng.random(N)                      # conditional cdf on [0,2] is u (mass mb*2/3 = 1-ma)
    right = 1 + np.cbrt(3 * (1 - ma) * u / mb - 1) if mb > 0 else np.zeros(N)
    Xs = np.where(pick, -rng.exponential(1.0, N), right)
    ex_mean = float(sp.integrate(x * ma * sp.exp(x), (x, -sp.oo, 0)) + sp.integrate(x * mb * (1 - x) ** 2, (x, 0, 2)))
    rec("Q4a", "E[X] mu=%s" % mu, float(mu), ex_mean, float(Xs.mean()), se_mean(Xs), tol=1e-12)

    def Fo(t, mu=float(mu)):
        if t < 0:
            return (1 - mu) / 2 * math.exp(t)
        return 1.0 if t >= 2 else (3 - mu) / 4 + (1 + mu) / 4 * (t - 1) ** 3

    def Fex(t, ma=ma, mb=mb):  # from the density directly
        if t < 0:
            return ma * math.exp(t)
        return 1.0 if t >= 2 else ma + mb / 3 * ((t - 1) ** 3 + 1)

    for t in (-1.0, 0.5, 1.5):
        rec("Q4c", "F(%.1f) mu=%s" % (t, mu), Fo(t), Fex(t), float(np.mean(Xs <= t)), se_p(Fo(t)), tol=1e-12)
    m = abs(float(mu))
    off4 = (1 + float(mu)) / 4 * (1 - (1 - m) ** 3)
    rec("Q4d", "P(0<X<|mu|) mu=%s" % mu, off4, Fex(m) - Fex(0), float(np.mean((Xs > 0) & (Xs < m))), se_p(off4), tol=1e-12)
rows.append(("Q4b", "a,b>=0 iff -1<=mu<=1",
             all((((1 - m_) / 2 >= 0 and 0.75 * (1 + m_) >= 0) == (-1 <= m_ <= 1)) for m_ in (-1.5, -1, 0, 1, 1.5)), True, ""))

# ============================================================ Q5  (eta1 = min(x, L-x)/L)
xb = rng.random(N)
eta1 = np.minimum(xb, 1 - xb)
for t in (0.1, 0.25, 0.4, 0.6):
    off = min(2 * t, 1.0)
    rec("Q5a", "F_eta1(%.2f)" % t, off, off, float(np.mean(eta1 <= t)), se_p(off))
tt = sp.symbols("t")
Ee = sp.integrate(2 * tt, (tt, 0, sp.Rational(1, 2)))
Ve = sp.integrate(2 * tt ** 2, (tt, 0, sp.Rational(1, 2))) - Ee ** 2
assert Ee == sp.Rational(1, 4) and Ve == sp.Rational(1, 48)
rec("Q5c", "E[eta1]=1/4", Fr(1, 4), Fr(Ee.p, Ee.q), float(eta1.mean()), se_mean(eta1))
rec("Q5c", "Var[eta1]=1/48", Fr(1, 48), Fr(Ve.p, Ve.q), float(eta1.var()), se_var(eta1))
for Lv in (1.0, 3.7):
    chain = [Lv * eta1]
    cur = chain[0]
    for n in range(2, 5):
        xx = rng.random(N)
        cur = cur * np.minimum(xx, 1 - xx)
        chain.append(cur)
    X2v = chain[1]
    rec("Q5d", "E[X2] L=%s" % Lv, Lv / 16, Lv * float(Ee) ** 2, float(X2v.mean()), se_mean(X2v))
    exact_v = Lv ** 2 * float(Fr(1, 144) - Fr(1, 256))
    rec("Q5d", "Var[X2] L=%s" % Lv, 7 * Lv ** 2 / 2304, exact_v, float(X2v.var()), se_var(X2v))
    for n in (1, 3, 4):
        Xn = chain[n - 1]
        offm = Lv * 0.25 ** n
        offv = Lv ** 2 * ((1 / 12) ** n - (1 / 16) ** n)
        rec("Q5e", "E[Xn] n=%d L=%s" % (n, Lv), offm, Lv * (1 / 4) ** n, float(Xn.mean()), se_mean(Xn))
        rec("Q5e", "Var[Xn] n=%d L=%s" % (n, Lv), offv, Lv ** 2 * ((1 / 12) ** n - (1 / 16) ** n), float(Xn.var()), se_var(Xn))


# ============================================================ Q6  (brute force)
def run_counts(n, k):
    allc = [(r, c) for r in range(n) for c in range(n)]
    hv = dg = tot = 0
    for t in itertools.combinations(allc, k):
        tot += 1
        st = set(t)
        for (dr, dc), kind in (((0, 1), "hv"), ((1, 0), "hv"), ((1, 1), "d"), ((1, -1), "d")):
            if any(all((c0[0] + i * dr, c0[1] + i * dc) in st for i in range(k)) for c0 in t):
                if kind == "hv":
                    hv += 1
                else:
                    dg += 1
                break
    return hv, dg, tot


rec("Q6a", "C(9,2)=36", 36, math.comb(9, 2), 36.0, 1e-9)
for n, k in ((3, 2), (4, 2), (5, 2), (4, 3), (5, 3), (5, 4), (6, 5), (5, 5)):
    hv, dg, tot = run_counts(n, k)
    total_official = 2 * (n - k + 1) * (2 * n - k + 1)
    rec("Q6g", "run count n=%d k=%d" % (n, k), total_official, hv + dg, float(total_official), 1e-9, tol=0)
    rec("Q6d", "C(N^2,k) total n=%d k=%d" % (n, k), math.comb(n * n, k), tot, float(math.comb(n * n, k)), 1e-9, tol=0)
    if k == 2:
        rec("Q6e", "hv count n=%d" % n, 2 * n * (n - 1), hv, float(2 * n * (n - 1)), 1e-9, tol=0)
        rec("Q6f", "diag count n=%d" % n, 2 * (n - 1) ** 2, dg, float(2 * (n - 1) ** 2), 1e-9, tol=0)
        rec("Q6e", "P hv n=%d" % n, Fr(4, n * (n + 1)), Fr(hv, tot), float(Fr(4, n * (n + 1))), 1e-9, tol=0)
        rec("Q6f", "P diag n=%d" % n, Fr(4 * (n - 1), n * n * (n + 1)), Fr(dg, tot), float(Fr(4 * (n - 1), n * n * (n + 1))), 1e-9, tol=0)
hv, dg, tot = run_counts(3, 2)
rec("Q6b", "P hv or vert 3x3 = 1/3", Fr(1, 3), Fr(hv, tot), float(Fr(1, 3)), 1e-9, tol=0)
rec("Q6c", "P diag 3x3 = 2/9", Fr(2, 9), Fr(dg, tot), float(Fr(2, 9)), 1e-9, tol=0)
TR = 1_000_000
for n, k in ((3, 2), (5, 2), (5, 3)):
    idx = np.argsort(rng.random((TR, n * n), dtype=np.float32), axis=1)[:, :k]
    r = idx // n
    c = idx % n
    o = np.argsort(r * n + c, axis=1)
    rs = np.take_along_axis(r, o, 1)
    cs = np.take_along_axis(c, o, 1)
    hit = np.zeros(TR, dtype=bool)
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        ok = np.ones(TR, dtype=bool)
        for i in range(1, k):
            ok &= (rs[:, i] - rs[:, i - 1] == dr) & (cs[:, i] - cs[:, i - 1] == dc)
        hit |= ok
    # anti-diagonal runs sort as (+1,-1) in (row,col) order
    off = Fr(2 * (n - k + 1) * (2 * n - k + 1), math.comb(n * n, k))
    rec("Q6g", "MC P(run) n=%d k=%d" % (n, k), off, off, float(hit.mean()), se_p(float(off), TR), tol=0)

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(1 if bad else 0)
