# -*- coding: utf-8 -*-
"""Verification harness for 26A-B (probability, flagship). Run: PYTHONUTF8=1 py tools/verify/26A-B/check.py

For every final answer two independent checks:
  EXACT : the official formula (evaluated at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy / numerical quadrature).
  MC    : Monte Carlo simulation (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Symbolic answers are checked at sample parameter values. Official keys are never changed here:
a disagreement is reported as MISMATCH and the item is held (see Q3 below).
Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20260430)
rows = []          # (item, what, exact_ok, mc_ok, detail)


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


def C(a, b):
    return math.comb(a, b) if 0 <= b <= a else 0


# ============================================================ Q1
X = rng.random(N); Y = rng.random(N); D = X * Y
FD = lambda t: t - t * math.log(t)
for t in (0.1, 0.3, 0.7):
    exact = integrate.quad(lambda x: min(1.0, t / x), 0, 1, points=[t], limit=200)[0]
    mc = float(np.mean(D <= t))
    rec("Q1a", "F_D(%.1f)" % t, FD(t), exact, mc, se_p(FD(t)), tol=1e-9)
t_ = sp.symbols("t", positive=True)
assert sp.simplify(sp.diff(t_ - t_ * sp.log(t_), t_) + sp.log(t_)) == 0
rows.append(("Q1b", "dF/dt = -ln t (sympy)", True, True, "symbolic identity"))
assert sp.integrate(-sp.log(t_), (t_, 0, 1)) == 1
fD = lambda t: -math.log(t)
for a, b in ((0.05, 0.2), (0.3, 0.9), (0.01, 0.5)):
    exact = integrate.quad(fD, a, b)[0]
    off = FD(b) - FD(a)
    mc = float(np.mean((D > a) & (D <= b)))
    rec("Q1b", "int f_D on (%.2f,%.2f]" % (a, b), off, exact, mc, se_p(off), tol=1e-9)
ED = sp.integrate(t_ * -sp.log(t_), (t_, 0, 1))
VD = sp.integrate(t_ ** 2 * -sp.log(t_), (t_, 0, 1)) - ED ** 2
assert ED == sp.Rational(1, 4) and VD == sp.Rational(7, 144)
sd = D.std(); m4 = np.mean((D - D.mean()) ** 4)
rec("Q1c", "E[D]", Fr(1, 4), Fr(ED.p, ED.q), float(D.mean()), sd / math.sqrt(N))
rec("Q1c", "Var[D]", Fr(7, 144), Fr(VD.p, VD.q), float(D.var()), math.sqrt((m4 - D.var() ** 2) / N))

# ============================================================ Q2
def q2a_exact(n, p):  # enumerate all sequences: first tail occurs at position >= 2 (after a head)
    tot = Fr(0)
    for seq in itertools.product((0, 1), repeat=n):  # 1 = head
        pr = Fr(1)
        for s in seq:
            pr *= p if s else 1 - p
        if 0 in seq and seq.index(0) >= 1:
            tot += pr
    return tot


for n, p in ((5, Fr(3, 10)), (2, Fr(7, 10)), (7, Fr(1, 2))):
    off = p * (1 - p ** (n - 1))
    tosses = rng.random((N, n)) < float(p)
    has_tail = ~tosses.all(axis=1)
    first_tail = np.argmin(tosses, axis=1)
    mc = float(np.mean(has_tail & (first_tail >= 1)))
    rec("Q2a", "n=%d p=%s" % (n, p), off, q2a_exact(n, p), mc, se_p(float(off)), tol=1e-12)


def parity_series(p, m, odd, K=900):
    s = Fr(0)
    for k in range(m, K):
        if (k % 2 == 1) == odd:
            s += C(k - 1, m - 1) * p ** m * (1 - p) ** (k - m)
    return s


for p in (Fr(3, 10), Fr(3, 5)):
    off = (1 - p) / (2 - p)
    ex = parity_series(p, 1, False)
    Xg = rng.geometric(float(p), N)
    rec("Q2b", "p=%s" % p, off, ex, float(np.mean(Xg % 2 == 0)), se_p(float(off)), tol=1e-30)
for m, p in ((3, Fr(2, 5)), (1, Fr(1, 3)), (4, Fr(7, 10)), (2, Fr(1, 2))):
    off = (1 - (-1) ** m * (p / (2 - p)) ** m) / 2
    ex = parity_series(p, m, True)
    Yv = m + rng.negative_binomial(m, float(p), N)
    rec("Q2c", "m=%d p=%s" % (m, p), off, ex, float(np.mean(Yv % 2 == 1)), se_p(float(off)), tol=1e-30)

# ============================================================ Q3
# Printed labelling (exam p.2): q1=P(B|AC) q2=P(B|~A~C) q3=P(B|A~C) q4=P(B|~AC)
# Solution labelling (official key): q1=P(B|AC) q2=P(B|~AC) q3=P(B|A~C) q4=P(B|~A~C)
p = Fr(3, 10)
q = {1: Fr(9, 10), 2: Fr(7, 10), 3: Fr(1, 2), 4: Fr(3, 10)}


def cond_table(labelling):
    cond = {(1, 1): q[1], (1, 0): q[3]}
    if labelling == "printed":
        cond[(0, 0)] = q[2]; cond[(0, 1)] = q[4]
    else:
        cond[(0, 1)] = q[2]; cond[(0, 0)] = q[4]
    return cond


def q3_exact(labelling):
    cond = cond_table(labelling)
    pa = {1: p, 0: 1 - p}
    PB = PAB = Fr(0)
    for a in (0, 1):
        for c in (0, 1):
            w = pa[a] * pa[c]
            PB += w * cond[(a, c)]
            if a == 1:
                PAB += w * cond[(a, c)]
    PQ1 = p * p * cond[(1, 1)]
    PQ2 = 1 - (1 - cond[(0, 0)]) * (1 - p) ** 2
    return PB, PAB / PB, PQ1, PQ2, cond


off_PB = q[1] * p ** 2 + (q[2] + q[3]) * p * (1 - p) + q[4] * (1 - p) ** 2
off_PAgB = (q[1] * p ** 2 + q[3] * p * (1 - p)) / off_PB
off_PQ1 = q[1] * p ** 2
off_PQ2 = 1 - (1 - q[4]) * (1 - p) ** 2
hold_report = []
for lab in ("solution", "printed"):
    PB, PAgB, PQ1, PQ2, cond = q3_exact(lab)
    A = rng.random(N) < float(p); Cc = rng.random(N) < float(p)
    pb = np.where(A & Cc, float(cond[(1, 1)]), np.where(A & ~Cc, float(cond[(1, 0)]),
         np.where(~A & Cc, float(cond[(0, 1)]), float(cond[(0, 0)]))))
    B = rng.random(N) < pb
    mc_PB = float(B.mean()); nB = int(B.sum()); mc_PAgB = float((A & B).sum() / nB)
    mc_Q1 = float((A & B & Cc).mean())
    # circuit in parallel works iff at least one of A, B, C works
    mc_Q2 = float((A | B | Cc).mean())
    for item, what, off, ex, mc, se in (
            ("Q3a", "P(B)", off_PB, PB, mc_PB, se_p(float(PB))),
            ("Q3b", "P(A|B)", off_PAgB, PAgB, mc_PAgB, math.sqrt(float(PAgB) * (1 - float(PAgB)) / nB)),
            ("Q3c", "P(Q1)", off_PQ1, PQ1, mc_Q1, se_p(float(PQ1))),
            ("Q3d", "P(Q2)", off_PQ2, PQ2, mc_Q2, se_p(float(PQ2)))):
        hold_report.append((item, what, lab, off == ex, abs(mc - float(off)) <= 4 * se, float(off), float(ex), mc))

# independence condition, symbolic, both labellings
pp, a1, a2, a3, a4 = sp.symbols("p q1 q2 q3 q4")


def indep_diff(lab):
    q_nac = a2 if lab == "solution" else a4      # P(B | not-A, C)
    q_nacn = a4 if lab == "solution" else a2     # P(B | not-A, not-C)
    PBs = a1 * pp ** 2 + q_nac * (1 - pp) * pp + a3 * pp * (1 - pp) + q_nacn * (1 - pp) ** 2
    PAB = a1 * pp ** 2 + a3 * pp * (1 - pp)
    return sp.expand(PAB - pp * PBs)


off_cond = pp * a1 + (1 - pp) * a3 - (pp * a2 + (1 - pp) * a4)       # official: p q1+(1-p) q3 = p q2+(1-p) q4
indep_sol_ok = sp.simplify(indep_diff("solution") - pp * (1 - pp) * off_cond) == 0
indep_prt_ok = sp.simplify(indep_diff("printed") - pp * (1 - pp) * off_cond) == 0

# ============================================================ Q4
x = sp.symbols("x", real=True)
for mu in (sp.Rational(1), sp.Rational(3, 2), sp.Rational(7, 8), sp.Rational(3, 4), sp.Rational(2)):
    b_, c_ = sp.symbols("b c")
    area = sp.integrate(b_ * x ** 2, (x, 0, 1)) + sp.integrate(c_ * sp.exp(-(x - 1)), (x, 1, sp.oo))
    mean = sp.integrate(x * b_ * x ** 2, (x, 0, 1)) + sp.integrate(x * c_ * sp.exp(-(x - 1)), (x, 1, sp.oo))
    sol = sp.solve([area - 1, mean - mu], [b_, c_], dict=True)[0]
    ob, oc = sp.Rational(12, 5) * (2 - mu), (4 * mu - 3) / 5
    ok = sp.simplify(sol[b_] - ob) == 0 and sp.simplify(sol[c_] - oc) == 0
    rows.append(("Q4a", "b,c at mu=%s (sympy solve)" % mu, ok, True, "b=%s c=%s" % (ob, oc)))
    if mu in (sp.Rational(3, 4), sp.Rational(2)):
        rows.append(("Q4b", "extreme mu=%s: one coefficient is 0" % mu, (oc == 0) or (ob == 0), True, ""))
rows.append(("Q4b", "outside [3/4,2] a coefficient is negative (mu=0.7, 2.1)",
             (4 * 0.7 - 3 < 0) and (12 * (2 - 2.1) < 0), True, ""))
for mu in (sp.Rational(1), sp.Rational(3, 2), sp.Rational(7, 8)):
    bq, cq = sp.Rational(12, 5) * (2 - mu), (4 * mu - 3) / 5
    pick = rng.random(N) < float(bq / 3)
    Xs = np.where(pick, rng.random(N) ** (1 / 3), 1 + rng.exponential(1.0, N))
    ex_mean = float(sp.integrate(x * bq * x ** 2, (x, 0, 1)) + sp.integrate(x * cq * sp.exp(-(x - 1)), (x, 1, sp.oo)))
    rec("Q4a", "E[X] mu=%s" % mu, float(mu), ex_mean, float(Xs.mean()), float(Xs.std() / math.sqrt(N)))

    def Fx(t, bq=bq, cq=cq):
        return 0.0 if t < 0 else (float(bq) / 3 * t ** 3 if t < 1 else 1 - float(cq) * math.exp(-(t - 1)))
    for t in (0.5, 1.0, 2.5):
        ex = float(sp.integrate(bq * x ** 2, (x, 0, min(t, 1))) +
                   (sp.integrate(cq * sp.exp(-(x - 1)), (x, 1, t)) if t > 1 else 0))
        rec("Q4c", "F_X(%.1f) mu=%s" % (t, mu), Fx(t), ex, float(np.mean(Xs <= t)), se_p(Fx(t)))
    off4d = float(mu ** 3 * (2 - mu) / 10)
    ex4d = float(sp.integrate(bq * x ** 2, (x, 0, mu / 2)))
    rec("Q4d", "P(0<X<mu/2) mu=%s" % mu, off4d, ex4d, float(np.mean((Xs > 0) & (Xs < float(mu) / 2))), se_p(off4d))


# ============================================================ Q5
def urn_exact(N1, D1, N2, D2, n, m):
    """Exact joint pmf of (X,Y) by enumerating every draw (balls are distinct)."""
    c1 = [1] * D1 + [0] * (N1 - D1)
    joint = {}
    for s1 in itertools.combinations(range(N1), n):
        k = sum(c1[i] for i in s1)
        urn2 = [1] * D2 + [0] * (N2 - D2) + [c1[i] for i in s1]
        w1 = Fr(1, C(N1, n))
        den = C(N2 + n, m)
        cnt = {}
        for s2 in itertools.combinations(range(N2 + n), m):
            l = sum(urn2[i] for i in s2)
            cnt[l] = cnt.get(l, 0) + 1
        for l, ct in cnt.items():
            joint[(k, l)] = joint.get((k, l), Fr(0)) + w1 * Fr(ct, den)
    return joint


def urn_mc(N1, D1, N2, D2, n, m, total=N, chunk=250_000):
    Xs, Ys = [], []
    for _ in range(total // chunk):
        r1 = np.argsort(rng.random((chunk, N1), dtype=np.float32), axis=1)[:, :n]
        col1 = (r1 < D1).astype(np.int8)
        urn2 = np.concatenate([np.tile((np.arange(N2) < D2).astype(np.int8), (chunk, 1)), col1], axis=1)
        r2 = np.argsort(rng.random((chunk, N2 + n), dtype=np.float32), axis=1)[:, :m]
        Xs.append(col1.sum(1).astype(int)); Ys.append(np.take_along_axis(urn2, r2, axis=1).sum(1).astype(int))
    return np.concatenate(Xs), np.concatenate(Ys)


for (N1, D1, N2, D2, n, m) in ((10, 4, 12, 5, 3, 4), (7, 3, 6, 2, 4, 2), (6, 5, 5, 1, 4, 3)):
    tag = "N1=%d D1=%d N2=%d D2=%d n=%d m=%d" % (N1, D1, N2, D2, n, m)
    joint = urn_exact(N1, D1, N2, D2, n, m)
    Xs, Ys = urn_mc(N1, D1, N2, D2, n, m)
    nn = len(Xs)
    ks = range(0, n + 1)
    for k in ks:                                   # a1: marginal of X
        off = Fr(C(D1, k) * C(N1 - D1, n - k), C(N1, n))
        ex = sum(v for (kk, l), v in joint.items() if kk == k)
        rec("Q5a", "A-1 P(X=%d) %s" % (k, tag), off, ex, float(np.mean(Xs == k)), se_p(float(off), nn))
    Xt = n - Xs
    for r in ks:                                   # a2: marginal of X~ = n - X
        off = Fr(C(N1 - D1, r) * C(D1, n - r), C(N1, n))
        ex = sum(v for (kk, l), v in joint.items() if n - kk == r)
        rec("Q5b", "A-2 P(X~=%d) %s" % (r, tag), off, ex, float(np.mean(Xt == r)), se_p(float(off), nn))
    EX = sum(kk * v for (kk, l), v in joint.items()); EX2 = sum(kk * kk * v for (kk, l), v in joint.items())
    var = EX2 - EX ** 2                            # a3: correlation, from the exact joint pmf
    cov_calc = sum((kk - EX) * ((n - kk) - (n - EX)) * v for (kk, l), v in joint.items())
    rho_ex = float(cov_calc / var) if var != 0 else float("nan")
    rho_mc = float(np.corrcoef(Xs, Xt)[0, 1])
    rec("Q5c", "A-3 rho(X,X~) %s" % tag, -1.0, rho_ex, rho_mc, 1e-9)
    for k in ks:                                   # b1: conditional
        pk = sum(v for (kk, l), v in joint.items() if kk == k)
        if pk == 0:
            continue
        nk = int(np.sum(Xs == k))
        for l in range(0, m + 1):
            off = Fr(C(D2 + k, l) * C(N2 + n - D2 - k, m - l), C(N2 + n, m))
            ex = joint.get((k, l), Fr(0)) / pk
            mc = float(np.mean(Ys[Xs == k] == l))
            rec("Q5d", "B-1 P(Y=%d|X=%d) %s" % (l, k, tag), off, ex, mc,
                max(math.sqrt(float(off) * (1 - float(off)) / nk), 1e-9))
    for k in ks:                                   # b2: joint
        for l in range(0, m + 1):
            off = (Fr(C(D1, k) * C(N1 - D1, n - k), C(N1, n)) *
                   Fr(C(D2 + k, l) * C(N2 + n - D2 - k, m - l), C(N2 + n, m)))
            ex = joint.get((k, l), Fr(0))
            rec("Q5e", "B-2 P(X=%d,Y=%d) %s" % (k, l, tag), off, ex, float(np.mean((Xs == k) & (Ys == l))),
                max(se_p(float(off), nn), 1e-9))


# ============================================================ Q6
def is_v(cells):
    cs = set(cells)
    for a, b in itertools.combinations(cells, 2):
        for third in cs - {a, b}:
            if a[0] == b[0] and abs(a[1] - b[1]) == 2:                     # same row, distance 2
                if third[1] == (a[1] + b[1]) // 2 and abs(third[0] - a[0]) == 1:
                    return True
            if a[1] == b[1] and abs(a[0] - b[0]) == 2:                     # same column, distance 2
                if third[0] == (a[0] + b[0]) // 2 and abs(third[1] - a[1]) == 1:
                    return True
    return False


def v_count(R, Cn):
    cells = [(r, c) for r in range(R) for c in range(Cn)]
    return sum(1 for t in itertools.combinations(cells, 3) if is_v(t)), C(R * Cn, 3)


def v_mc(Mm, Nn, trials):
    idx = np.argsort(rng.random((trials, Mm * Nn), dtype=np.float32), axis=1)[:, :3]
    rr = idx // Nn; cc = idx % Nn
    hit = np.zeros(len(idx), dtype=bool)
    for (i, j, k) in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        h1 = ((rr[:, i] == rr[:, j]) & (np.abs(cc[:, i] - cc[:, j]) == 2) &
              (cc[:, k] * 2 == cc[:, i] + cc[:, j]) & (np.abs(rr[:, k] - rr[:, i]) == 1))
        h2 = ((cc[:, i] == cc[:, j]) & (np.abs(rr[:, i] - rr[:, j]) == 2) &
              (rr[:, k] * 2 == rr[:, i] + rr[:, j]) & (np.abs(cc[:, k] - cc[:, i]) == 1))
        hit |= h1 | h2
    return float(hit.mean())


rec("Q6a", "A-1 C(12,3)", 220, C(12, 3), 220.0, 1e-9)
rows.append(("Q6a", "A-1 C(12,3) == len(combinations of 12 cells)", C(12, 3) == sum(1 for _ in itertools.combinations(range(12), 3)), True, ""))
for (Mm, Nn) in ((3, 4), (3, 3), (4, 5), (5, 3), (6, 7)):
    cnt, tot = v_count(Mm, Nn)
    off_cnt = 2 * (Mm - 1) * (Nn - 2) + 2 * (Mm - 2) * (Nn - 1)
    off = Fr(off_cnt, C(Mm * Nn, 3))
    trials = 1_000_000
    mc = v_mc(Mm, Nn, trials)
    item = "Q6b" if (Mm, Nn) == (3, 4) else "Q6d"
    rec(item, "P(V) %dx%d = %d/%d" % (Mm, Nn, off_cnt, tot), off, Fr(cnt, tot), mc, se_p(float(off), trials))
    rows.append((item, "4MN-6M-6N+8 == official count at %dx%d" % (Mm, Nn),
                 4 * Mm * Nn - 6 * Mm - 6 * Nn + 8 == off_cnt, True, ""))
    rows.append(("Q6c", "C(MN,3) at %dx%d" % (Mm, Nn),
                 tot == sum(1 for _ in itertools.combinations(range(Mm * Nn), 3)), True, ""))
rows.append(("Q6b", "P(V) 4x3 = 7/110", Fr(14, 220) == Fr(7, 110), True, ""))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("Q3 labelling check (official formulas vs exact enumeration and MC):")
for item, what, lab, ex_ok, mc_ok, off, ex, mc in hold_report:
    print("  %-4s %-7s labelling=%-8s exact=%s mc=%s official=%.6f true=%.6f mc=%.6f" % (
        item, what, lab, "match" if ex_ok else "MISMATCH", "match" if mc_ok else "MISMATCH", off, ex, mc))
print("  independence condition p*q1+(1-p)*q3 = p*q2+(1-p)*q4 is equivalent to A,B independent: "
      "solution labelling=%s printed labelling=%s" % (indep_sol_ok, indep_prt_ok))
sol_ok = all(h[3] and h[4] for h in hold_report if h[2] == "solution") and indep_sol_ok
prt_mismatch_items = sorted(h[0] for h in hold_report if h[2] == "printed" and not (h[3] and h[4]))
print("  official key matches the SOLUTION labelling everywhere: %s" % sol_ok)
print("  items whose official key does NOT match the PRINTED labelling: %s (independence condition: %s)" % (
    prt_mismatch_items, "ok" if indep_prt_ok else "wrong"))
print("  => Q3a, Q3b, Q3d held (key vs printed question); Q3c unaffected.")
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
expected_hold_ok = sol_ok and prt_mismatch_items == ["Q3a", "Q3b", "Q3d"] and not indep_prt_ok
sys.exit(0 if (not bad and expected_hold_ok) else 1)
