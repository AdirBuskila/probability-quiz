# -*- coding: utf-8 -*-
"""Verification harness for 25A-A (probability, 17.02.2025). Run: PYTHONUTF8=1 py tools/verify/25A-A/check.py

For every final answer two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy / numerical quadrature).
  MC    : Monte Carlo simulation (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Official keys are never changed here.
Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20250217)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1   X1~U(0,1/3), X2~U(0,2/3) independent
X1 = rng.random(N) / 3; X2 = rng.random(N) * 2 / 3
a_ev = X1 > X2
tri = (X1 + X2 >= 0.5) & (X1 <= 0.5) & (X2 <= 0.5)
area_tot = (1 / 3) * (2 / 3)
# exact (quadrature of the length of the x2-interval for each x1)
f_a = lambda x1: max(0.0, min(x1, 2 / 3))
ex_a = integrate.quad(f_a, 0, 1 / 3)[0] / area_tot
rec("Q1a", "P(X1>X2)=1/4", Fr(1, 4), ex_a, float(a_ev.mean()), se_p(0.25), tol=1e-9)
f_b = lambda x1: max(0.0, min(2 / 3, 0.5) - max(0.0, 0.5 - x1)) if x1 <= 0.5 else 0.0
ex_b = integrate.quad(f_b, 0, 1 / 3)[0] / area_tot
rec("Q1b", "P(triangle) = P(X1+X2>=1/2, X1<=1/2, X2<=1/2) = 1/4", Fr(1, 4), ex_b, float(tri.mean()), se_p(0.25), tol=1e-9)
f_c = lambda x1: max(0.0, min(x1, 0.5, 2 / 3) - max(0.0, 0.5 - x1))
ex_joint = integrate.quad(f_c, 0, 1 / 3, points=[0.25])[0] / area_tot
ex_c = ex_joint / 0.25
sel = a_ev
mc = float((tri & sel).sum() / sel.sum())
rec("Q1c", "P(triangle | X1>X2) = 1/8", Fr(1, 8), ex_c, mc, math.sqrt(mc * (1 - mc) / float(sel.sum())), tol=1e-9)
rec("Q1c", "joint area/|Omega| = 1/32", Fr(1, 32), ex_joint, float((tri & sel).mean()), se_p(1 / 32), tol=1e-9)

# ============================================================ Q2   3-digit numbers 100..999
Omega = list(range(100, 1000))
A2 = {n for n in Omega if n % 2 == 0}; A4 = {n for n in Omega if n % 4 == 0}; A8 = {n for n in Omega if n % 8 == 0}
rows.append(("Q2a", "|Omega|=900, |A2|=450, |A4|=225, |A8|=112 (enumeration)", (len(Omega), len(A2), len(A4), len(A8)) == (900, 450, 225, 112), True,
             "%s" % ((len(Omega), len(A2), len(A4), len(A8)),)))
draw = rng.integers(100, 1000, N)
for item, what, off, S_ in (("Q2a", "P(A2)=1/2", Fr(1, 2), A2), ("Q2a", "P(A4)=1/4", Fr(1, 4), A4), ("Q2a", "P(A8)=28/225", Fr(28, 225), A8)):
    mask = np.zeros(1000, dtype=bool); mask[list(S_)] = True
    rec(item, what, off, Fr(len(S_), 900), float(mask[draw].mean()), se_p(float(off)))
rows.append(("Q2a", "P(A8)=28/225 is not 1/8", Fr(28, 225) != Fr(1, 8), True, "exact"))
rows.append(("Q2b", "A2 and A4 are dependent: P(A2 & A4)=1/4 != 1/8 = P(A2)P(A4)",
             Fr(len(A2 & A4), 900) == Fr(1, 4) and Fr(len(A2 & A4), 900) != Fr(len(A2), 900) * Fr(len(A4), 900), True, "exact"))
rows.append(("Q2c", "A4 and A8 are dependent: P(A4 & A8)=28/225 != 7/450 = P(A4)P(A8)",
             Fr(len(A4 & A8), 900) == Fr(28, 225) and Fr(len(A4 & A8), 900) != Fr(len(A4), 900) * Fr(len(A8), 900), True, "exact"))
rows.append(("Q2d", "A8 != A2 & A4 (A2 & A4 = A4, 225 elements, A8 has 112): the claim is false", (A2 & A4) == A4 and A8 != (A2 & A4), True, "exact"))

# ============================================================ Q3   f = a e^x (x<0), b x (0<=x<1), c/x (x>=1)
xs = sp.symbols("x", real=True)
rows.append(("Q3a", "int_1^oo c/x dx diverges unless c=0", sp.integrate(1 / xs, (xs, 1, sp.oo)) == sp.oo, True, "sympy"))
for mu in (sp.Rational(0), sp.Rational(1, 3), sp.Rational(-1, 2), sp.Rational(2, 3), sp.Rational(-1)):
    a_, b_ = sp.symbols("a b")
    area = sp.integrate(a_ * sp.exp(xs), (xs, -sp.oo, 0)) + sp.integrate(b_ * xs, (xs, 0, 1))
    mean = sp.integrate(xs * a_ * sp.exp(xs), (xs, -sp.oo, 0)) + sp.integrate(xs * b_ * xs, (xs, 0, 1))
    sol = sp.solve([area - 1, mean - mu], [a_, b_], dict=True)[0]
    oa, ob = (2 - 3 * mu) / 5, sp.Rational(6, 5) * (mu + 1)
    rows.append(("Q3a", "a,b at mu=%s (sympy solve)" % mu, sp.simplify(sol[a_] - oa) == 0 and sp.simplify(sol[b_] - ob) == 0, True,
                 "a=%s b=%s" % (oa, ob)))
rows.append(("Q3b", "a>=0 needs mu<=2/3 and b>=0 needs mu>=-1, so mu=1 is impossible (a=-1/5)",
             (2 - 3 * 1) / 5 < 0 and sp.Rational(2, 3) < 1, True, "exact"))
rows.append(("Q3b", "mu=2/3 gives a=0 (uniform-type triangle, mean 2/3); mu=-1 gives b=0 (e^x on x<0, mean -1)",
             (2 - 3 * sp.Rational(2, 3)) / 5 == 0 and sp.Rational(6, 5) * (sp.Rational(-1) + 1) == 0 and
             sp.integrate(xs * sp.exp(xs), (xs, -sp.oo, 0)) == -1 and sp.integrate(xs * 2 * xs, (xs, 0, 1)) == sp.Rational(2, 3), True, "sympy"))
for mu in (sp.Rational(0), sp.Rational(1, 3), sp.Rational(-1, 2)):
    aq, bq = (2 - 3 * mu) / 5, sp.Rational(6, 5) * (mu + 1)
    pl = float(aq)
    left = rng.random(N) < pl
    Xs = np.where(left, np.log(rng.random(N)), np.sqrt(rng.random(N)))    # left: e^x on x<0 ; right: density 2x on (0,1)
    rec("Q3a", "E[X] mu=%s" % mu, float(mu), float(mu), float(Xs.mean()), float(Xs.std() / math.sqrt(N)))

    def offF(t):
        t = sp.nsimplify(t)
        return float(aq * sp.exp(t)) if t < 0 else float(aq + sp.Rational(3, 5) * (mu + 1) * t ** 2)
    for t in (-1.2, -0.3, 0.4, 0.9):
        ex = integrate.quad(lambda x: float(aq) * math.exp(x) if x < 0 else float(bq) * x, -60, t, points=[0] if t > 0 else None)[0]
        rec("Q3c", "F_X(%.1f) mu=%s" % (t, mu), offF(t), ex, float(np.mean(Xs <= t)), se_p(offF(t)), tol=1e-9)
    den = Xs > 0
    rec("Q3d", "P(X<1|X>0)=1 mu=%s" % mu, 1.0, 1.0, float(((Xs < 1) & den).sum() / den.sum()), 1e-9)

# ============================================================ Q4   bridge (Q1) and series/parallel (Q2)
p = sp.symbols("p", positive=True)


def reliab(edges, comps, probs, s, t):
    total = 0
    for st in itertools.product((0, 1), repeat=len(comps)):
        on = dict(zip(comps, st))
        parent = {}

        def find(a):
            parent.setdefault(a, a)
            while parent[a] != a:
                parent[a] = parent[parent[a]]; a = parent[a]
            return a
        for c in comps:
            if on[c]:
                u, v = edges[c]
                parent[find(u)] = find(v)
        if find(s) == find(t):
            w = 1
            for c in comps:
                w *= probs[c] if on[c] else 1 - probs[c]
            total += w
    return sp.expand(total)


comps = list("ABCDE")
pr = {c: p for c in comps}
# Q1 bridge: A: s-T, B: T-t, C: s-Bo, D: Bo-t, E: T-Bo
BR = {"A": ("s", "T"), "B": ("T", "t"), "C": ("s", "Bo"), "D": ("Bo", "t"), "E": ("T", "Bo")}
# Q2 chain: A: s-x, B and C parallel x-y, D and E parallel y-t
CH = {"A": ("s", "x"), "B": ("x", "y"), "C": ("x", "y"), "D": ("y", "t"), "E": ("y", "t")}
Q1p = reliab(BR, comps, pr, "s", "t")
Q2p = reliab(CH, comps, pr, "s", "t")
off_Q1 = sp.expand(p ** 3 * (2 - p) ** 2 + p ** 2 * (1 - p) * (2 - p ** 2))
off_Q2 = sp.expand(p ** 3 * (2 - p) ** 2)
rows.append(("Q4a", "P(Q1)=p^3(2-p)^2+p^2(1-p)(2-p^2) (symbolic enumeration)", sp.expand(Q1p - off_Q1) == 0, True, "sympy"))
rows.append(("Q4b", "P(Q2)=p(2p-p^2)^2=p^3(2-p)^2 (symbolic enumeration)", sp.expand(Q2p - off_Q2) == 0, True, "sympy"))


def both_poly():
    tot = 0
    for st in itertools.product((0, 1), repeat=5):
        on = dict(zip(comps, st))

        def conn(edges):
            parent = {}

            def find(a):
                parent.setdefault(a, a)
                while parent[a] != a:
                    parent[a] = parent[parent[a]]; a = parent[a]
                return a
            for c in comps:
                if on[c]:
                    u, v = edges[c]; parent[find(u)] = find(v)
            return find("s") == find("t")
        if conn(BR) and conn(CH):
            w = 1
            for c in comps:
                w *= p if on[c] else 1 - p
            tot += w
    return sp.expand(tot)


Qb = both_poly()
off_both = sp.expand(p ** 3 * (3 - 2 * p))
rows.append(("Q4c", "P(Q1 and Q2) = p^3(3-2p)", sp.expand(Qb - off_both) == 0, True, "sympy"))
rows.append(("Q4c", "P(Q1|Q2) = (3-2p)/(2-p)^2", sp.simplify(Qb / Q2p - (3 - 2 * p) / (2 - p) ** 2) == 0, True, "sympy"))
rows.append(("Q4d", "P(not Q1|Q2) = (1-p)^2/(2-p)^2", sp.simplify(1 - Qb / Q2p - (1 - p) ** 2 / (2 - p) ** 2) == 0, True, "sympy"))
for pv in (0.35, 0.6, 0.8):
    st = {c: rng.random(N) < pv for c in comps}
    A, B, Cc, D, E = (st[k] for k in "ABCDE")
    q1 = (E & (A | Cc) & (B | D)) | (~E & ((A & B) | (Cc & D)))
    q2 = A & (B | Cc) & (D | E)
    o1 = float(off_Q1.subs(p, pv)); o2 = float(off_Q2.subs(p, pv)); ob = float(off_both.subs(p, pv))
    rec("Q4a", "P(Q1) p=%.2f" % pv, o1, float(Q1p.subs(p, pv)), float(q1.mean()), se_p(o1))
    rec("Q4b", "P(Q2) p=%.2f" % pv, o2, float(Q2p.subs(p, pv)), float(q2.mean()), se_p(o2))
    n2 = int(q2.sum()); oc = ob / o2
    rec("Q4c", "P(Q1|Q2) p=%.2f" % pv, (3 - 2 * pv) / (2 - pv) ** 2, oc, float((q1 & q2).sum() / n2), math.sqrt(oc * (1 - oc) / n2))
    od = 1 - oc
    rec("Q4d", "P(not Q1|Q2) p=%.2f" % pv, (1 - pv) ** 2 / (2 - pv) ** 2, od, float((~q1 & q2).sum() / n2), math.sqrt(od * (1 - od) / n2))

# ============================================================ Q5   y(t)=cos(w t), w~Exp(lam); N_T = number of zeros in (0,T]
lam, T = 0.9, 2.5
w = rng.exponential(1 / lam, N)
NT = np.floor(w * T / math.pi + 0.5).astype(int)           # zeros pi/2 + pi*j (j>=0) not exceeding w*T


def pmf_off(k):
    if k == 0:
        return 1 - math.exp(-lam * math.pi / (2 * T))
    return math.exp(-lam * math.pi * k / T) * (math.exp(lam * math.pi / (2 * T)) - math.exp(-lam * math.pi / (2 * T)))


def pmf_exact(k):
    lo = 0.0 if k == 0 else math.pi * (k - 0.5) / T
    hi = math.pi * (k + 0.5) / T
    return integrate.quad(lambda x: lam * math.exp(-lam * x), lo, hi)[0]


for k in (0, 1, 2, 3, 5):
    rec("Q5a", "P(N_T=%d) lam=0.9 T=2.5" % k, pmf_off(k), pmf_exact(k), float(np.mean(NT == k)), se_p(pmf_off(k)), tol=1e-10)
rows.append(("Q5a", "sum of the official pmf over k=0..4000 equals 1", abs(sum(pmf_off(k) for k in range(0, 4000)) - 1) < 1e-10, True, "series"))
off_E = 1 / (math.exp(lam * math.pi / (2 * T)) - math.exp(-lam * math.pi / (2 * T)))
ex_E = sum(k * pmf_exact(k) for k in range(0, 600))
rec("Q5b", "E[N_T]=1/(e^{lam pi/2T}-e^{-lam pi/2T})", off_E, ex_E, float(NT.mean()), float(NT.std() / math.sqrt(N)), tol=1e-9)
for k in (1, 2, 4):
    # {t_{k+1}>T | t_k<T} = {N_T = k | N_T >= k}
    sel = NT >= k
    mc = float(((NT == k) & sel).sum() / sel.sum())
    off = 1 - math.exp(-lam * math.pi / T)
    ex = pmf_exact(k) / integrate.quad(lambda x: lam * math.exp(-lam * x), math.pi * (k - 0.5) / T, np.inf)[0]
    rec("Q5c", "P(t_{k+1}>T | t_k<T) k=%d" % k, off, ex, mc, math.sqrt(off * (1 - off) / float(sel.sum())), tol=1e-9)

# ============================================================ Q6   batteries: from A with prob q, defective with prob p (independent)
def C(a, b):
    return math.comb(a, b) if 0 <= b <= a else 0


for (n, pv, qv) in ((4, Fr(3, 10), Fr(2, 5)), (3, Fr(1, 2), Fr(7, 10)), (5, Fr(4, 5), Fr(1, 3))):
    # exact joint pmf of (X,Y) by enumerating the 4 outcomes (fromA, defective) of every battery
    joint = {}
    for outs in itertools.product(((1, 1), (1, 0), (0, 1), (0, 0)), repeat=n):
        w_ = Fr(1)
        for fa, de in outs:
            w_ *= (qv if fa else 1 - qv) * (pv if de else 1 - pv)
        x = sum(fa for fa, de in outs); y = sum(fa and de for fa, de in outs)
        joint[(x, y)] = joint.get((x, y), Fr(0)) + w_
    xs_ = rng.random((N, n)) < float(qv); ds_ = rng.random((N, n)) < float(pv)
    Xs = xs_.sum(1); Ys = (xs_ & ds_).sum(1)
    tag = "n=%d p=%s q=%s" % (n, pv, qv)
    for k in range(n + 1):
        offx = Fr(C(n, k)) * qv ** k * (1 - qv) ** (n - k)
        exx = sum(v for (x, y), v in joint.items() if x == k)
        rec("Q6a", "P(X=%d) %s" % (k, tag), offx, exx, float(np.mean(Xs == k)), se_p(float(offx)))
        offy = Fr(C(n, k)) * (pv * qv) ** k * (1 - pv * qv) ** (n - k)
        exy = sum(v for (x, y), v in joint.items() if y == k)
        rec("Q6b", "P(Y=%d) %s" % (k, tag), offy, exy, float(np.mean(Ys == k)), se_p(float(offy)))
    EX = sum(x * v for (x, y), v in joint.items()); EY = sum(y * v for (x, y), v in joint.items())
    cov = sum(x * y * v for (x, y), v in joint.items()) - EX * EY
    varx = sum(x * x * v for (x, y), v in joint.items()) - EX ** 2
    vary = sum(y * y * v for (x, y), v in joint.items()) - EY ** 2
    rho2_ex = cov * cov / (varx * vary)
    rho2_off = pv * (1 - qv) / (1 - pv * qv)
    rows.append(("Q6c1", "rho^2 = p(1-q)/(1-pq) exact %s" % tag, rho2_ex == rho2_off and cov == n * pv * qv * (1 - qv), True,
                 "cov=%s" % cov))
    rho_mc = float(np.corrcoef(Xs, Ys)[0, 1])
    rows.append(("Q6c1", "rho MC %s" % tag, True, abs(rho_mc - math.sqrt(float(rho2_off))) < 0.003,
                 "official=%.5f mc=%.5f" % (math.sqrt(float(rho2_off)), rho_mc)))
rows.append(("Q6c2", "p=1: Y=X so rho=1, and the formula gives sqrt(1*(1-q)/(1-q))=1",
             all(math.sqrt(1 * (1 - q_) / (1 - 1 * q_)) == 1.0 for q_ in (0.3, 0.6, 0.9)), True, "exact"))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if not bad else 1)
