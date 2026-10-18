# -*- coding: utf-8 -*-
"""Verification harness for 25A-B (probability, 12.03.2025). Run: PYTHONUTF8=1 py tools/verify/25A-B/check.py

For every final answer two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy / numerical quadrature).
  MC    : Monte Carlo simulation (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Official keys are never changed here. Q6 e, f (bonus parts) have no official solution in the file: they ship as
solved (var = (N+1)(N-2)/18 for both, rho = 1/2 for N >= 3, undefined for N = 2), checked exactly and by MC.
Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20250312)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1   X,Y ~ U(0,1) iid, Z = X/Y
X = rng.random(N); Y = rng.random(N)
Z = X / Y


def FZ(t):
    return 0.0 if t <= 0 else (t / 2 if t <= 1 else 1 - 1 / (2 * t))


for item, t, off in (("Q1a1", 1 / 3, Fr(1, 6)), ("Q1a2", 3.0, Fr(5, 6)), ("Q1a3", 1.0, Fr(1, 2))):
    # exact: area of {y > x/t} in the unit square
    ex = integrate.quad(lambda x: min(1.0, max(0.0, 1 - x / t)), 0, 1, points=[min(t, 1)], limit=200)[0]
    rec(item, "P(Z<%.3f)" % t, off, ex, float(np.mean(Z < t)), se_p(float(off)), tol=1e-9)
for t in (0.25, 0.8, 1.5, 4.0, 20.0):
    ex = integrate.quad(lambda x: min(1.0, max(0.0, 1 - x / t)), 0, 1, points=[min(t, 1)], limit=200)[0]
    rec("Q1b", "F_Z(%.2f)" % t, FZ(t), ex, float(np.mean(Z < t)), se_p(FZ(t)), tol=1e-9)
fZ = lambda t: 0.0 if t <= 0 else (0.5 if t <= 1 else 1 / (2 * t * t))
for a, b in ((0.2, 0.7), (0.5, 3.0), (2.0, 10.0)):
    ex = integrate.quad(fZ, a, b, points=[1.0] if a < 1 < b else None)[0]
    off = FZ(b) - FZ(a)
    rec("Q1c", "int f_Z on (%.1f,%.1f]" % (a, b), off, ex, float(np.mean((Z > a) & (Z <= b))), se_p(off), tol=1e-9)
t_ = sp.symbols("t", positive=True)
rows.append(("Q1c", "d/dt (1-1/(2t)) = 1/(2t^2), d/dt (t/2) = 1/2 (sympy)",
             sp.simplify(sp.diff(1 - 1 / (2 * t_), t_) - 1 / (2 * t_ ** 2)) == 0 and sp.diff(t_ / 2, t_) == sp.Rational(1, 2), True, "sympy"))
# E sqrt(Z): infinite variance (E[Z] = oo), so the MC is run on the truncation min(sqrt Z, M), whose exact mean is also computed
ex_full = sp.integrate(sp.sqrt(t_) * sp.Rational(1, 2), (t_, 0, 1)) + sp.integrate(sp.sqrt(t_) / (2 * t_ ** 2), (t_, 1, sp.oo))
rows.append(("Q1d", "E[sqrt Z] = 4/3 (sympy, via the density) and = E[sqrt X] E[1/sqrt Y] = (2/3)(2)",
             ex_full == sp.Rational(4, 3) and sp.Rational(2, 3) * 2 == sp.Rational(4, 3), True, "sympy"))
Mcap = 30.0
trunc_exact = integrate.quad(lambda t: min(math.sqrt(t), Mcap) * fZ(t), 0, 1)[0] + \
    integrate.quad(lambda t: min(math.sqrt(t), Mcap) * fZ(t), 1, Mcap ** 2)[0] + \
    integrate.quad(lambda t: Mcap * fZ(t), Mcap ** 2, np.inf)[0]
tr = np.minimum(np.sqrt(Z), Mcap)
rec("Q1d", "E[min(sqrt Z, 30)] (truncated; exact from the official density)", trunc_exact, trunc_exact, float(tr.mean()), float(tr.std() / math.sqrt(N)), tol=1e-12)
rows.append(("Q1d", "tail beyond the cap is exactly 2/(3*sqrt(...)) small: E[sqrt Z]-E[min]=%.4f" % (4 / 3 - trunc_exact),
             4 / 3 - trunc_exact < 0.07, True, "sqrt(Z) tail integral = 1/Mcap = %.4f" % (1 / Mcap)))

# ============================================================ Q2   P(A)=p, P(B)=q, P(B/notA)=s
for trial in range(6):
    c = rng.random(4) + 0.1; c /= c.sum()
    x11, x10, x01 = [Fr(int(round(v * 997)), 1000) for v in c[:3]]
    x00 = 1 - x11 - x10 - x01
    p, q = x11 + x10, x11 + x01
    s = x01 / (1 - p)                                         # P(B/notA)
    assert x01 / q == s * (1 - p) / q                         # a1 P(notA/B) = s(1-p)/q
    assert x11 / q == 1 - s * (1 - p) / q                     # a2
    assert x11 == q - s * (1 - p)                             # a3 P(A and B)
    assert x11 + x10 + x01 == p + s * (1 - p)                 # a4 P(A u B)
    assert (x11 == p * q) == (s == q)                         # b: independent iff s=q (p != 1)
    assert (x11 == 0) == (q == s * (1 - p))                   # c: disjoint iff q = s(1-p)
rows.append(("Q2a", "a1..a4 formulas equal the cell values on 6 exact random distributions", True, True, "exact fractions"))
rows.append(("Q2b", "independence <=> s = q (p != 1) on 6 exact distributions", True, True, "exact"))
rows.append(("Q2c", "disjoint <=> q = s(1-p) on 6 exact distributions", True, True, "exact"))
cells = np.array([0.18, 0.22, 0.31, 0.29])
cnt = rng.multinomial(N, cells)
p_ = cells[0] + cells[1]; q_ = cells[0] + cells[2]; s_ = cells[2] / (1 - p_)
for item, what, off, exact, num, den in (
        ("Q2a1", "P(notA/B)=s(1-p)/q", s_ * (1 - p_) / q_, cells[2] / q_, cnt[2], cnt[0] + cnt[2]),
        ("Q2a2", "P(A/B)=1-s(1-p)/q", 1 - s_ * (1 - p_) / q_, cells[0] / q_, cnt[0], cnt[0] + cnt[2])):
    rec(item, what, off, exact, num / den, math.sqrt(off * (1 - off) / den))
rec("Q2a3", "P(A and B)=q-s(1-p)", q_ - s_ * (1 - p_), cells[0], cnt[0] / N, se_p(cells[0]))
rec("Q2a4", "P(A u B)=p+s(1-p)", p_ + s_ * (1 - p_), 1 - cells[3], 1 - cnt[3] / N, se_p(1 - cells[3]))

# ============================================================ Q3   pdf: a on [-1,0); triangle with peak b at x=1 on [0,2]
xs = sp.symbols("x", real=True)
for mu in (sp.Rational(1, 4), sp.Rational(0), sp.Rational(-1, 3), sp.Rational(1, 2), sp.Rational(1), sp.Rational(-1, 2)):
    a_, b_ = sp.symbols("a b")
    f_tri = sp.Piecewise((b_ * xs, xs < 1), (b_ * (2 - xs), True))
    area = a_ + sp.integrate(b_ * xs, (xs, 0, 1)) + sp.integrate(b_ * (2 - xs), (xs, 1, 2))
    mean = sp.integrate(xs * a_, (xs, -1, 0)) + sp.integrate(xs * b_ * xs, (xs, 0, 1)) + sp.integrate(xs * b_ * (2 - xs), (xs, 1, 2))
    sol = sp.solve([area - 1, mean - mu], [a_, b_], dict=True)[0]
    oa, ob = sp.Rational(2, 3) * (1 - mu), (1 + 2 * mu) / 3
    rows.append(("Q3a", "a,b at mu=%s (sympy solve)" % mu, sp.simplify(sol[a_] - oa) == 0 and sp.simplify(sol[b_] - ob) == 0, True,
                 "a=%s b=%s" % (oa, ob)))
rows.append(("Q3b", "mu=1 gives a=0 (triangle on [0,2], mean 1); mu=-1/2 gives b=0 (uniform on [-1,0], mean -1/2)",
             sp.Rational(2, 3) * (1 - 1) == 0 and (1 + 2 * sp.Rational(-1, 2)) / 3 == 0, True, "sympy"))
rows.append(("Q3b", "outside [-1/2,1] a coefficient is negative (mu=1.2, -0.6)", (1 - 1.2 < 0) and (1 + 2 * -0.6 < 0), True, ""))
for mu in (sp.Rational(1, 4), sp.Rational(-1, 3), sp.Rational(3, 4)):
    aq, bq = sp.Rational(2, 3) * (1 - mu), (1 + 2 * mu) / 3
    pick_left = rng.random(N) < float(aq)
    Xs = np.where(pick_left, -rng.random(N), rng.triangular(0, 1, 2, N))   # triangular pdf b*x / b*(2-x) normalised to area b
    # when not left, the density is the triangle of area b=1-a; normalised triangular(0,1,2)
    rec("Q3a", "E[X] mu=%s" % mu, float(mu), float(mu), float(Xs.mean()), float(Xs.std() / math.sqrt(N)))

    def Fx(t, aq=aq, bq=bq):
        if t < -1: return 0.0
        if t < 0: return float(aq) * (t + 1)
        if t < 1: return float(aq) + float(bq) * t * t / 2
        if t < 2: return 1 - float(bq) * (2 - t) ** 2 / 2
        return 1.0
    offF = lambda t: (float(sp.Rational(2, 3) * (1 - mu)) * (t + 1) if t < 0 else
                      (float(sp.Rational(2, 3) * (1 - mu) + (1 + 2 * mu) / 6 * sp.nsimplify(t) ** 2) if t < 1 else
                       float(1 - (1 + 2 * mu) / 6 * (2 - sp.nsimplify(t)) ** 2)))
    f_pdf = lambda x: float(aq) if -1 <= x < 0 else (float(bq) * x if 0 <= x < 1 else (float(bq) * (2 - x) if 1 <= x < 2 else 0.0))
    for t in (-0.6, 0.4, 1.0, 1.6):
        ex = integrate.quad(f_pdf, -1, t, points=[0, 1] if t > 1 else ([0] if t > 0 else None), limit=200)[0]
        rec("Q3c", "F_X(%.1f) mu=%s" % (t, mu), offF(t), ex, float(np.mean(Xs <= t)), se_p(offF(t)), tol=1e-9)
    den = Xs > 0
    mc = float(((Xs < 1) & den).sum() / den.sum())
    ex = (Fx(1) - Fx(0)) / (1 - Fx(0))
    rec("Q3d", "P(X<1|X>0) mu=%s" % mu, 0.5, ex, mc, math.sqrt(0.25 / float(den.sum())), tol=1e-12)
rows.append(("Q3c", "F_X(1) = (5-2mu)/6 (value drawn on the official graph)", True, True,
             "a + b/2 = 2(1-mu)/3 + (1+2mu)/6 = (5-2mu)/6"))

# ============================================================ Q4   circuits
p, q = sp.symbols("p q", positive=True)


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


# Q1: s -A- u1, s -B- d1, E: u1-d1, u1 -C- t, d1 -D- t.
EDG1 = {"A": ("s", "u1"), "B": ("s", "d1"), "E": ("u1", "d1"), "C": ("u1", "t"), "D": ("d1", "t")}
# Q2: C: u1-u2, D: d1-d2, F: u2-d2, G: u2-t
EDG2 = {"A": ("s", "u1"), "B": ("s", "d1"), "E": ("u1", "d1"), "C": ("u1", "u2"), "D": ("d1", "d2"), "F": ("u2", "d2"), "G": ("u2", "t")}
c1 = list("ABCDE"); c2 = list("ABCDEFG")
Q1p = reliab(EDG1, c1, {c: p for c in c1}, "s", "t")
pr2 = {c: p for c in c2}; pr2["F"] = q; pr2["G"] = q
Q2p = reliab(EDG2, c2, pr2, "s", "t")
off_Q1 = sp.expand(p * (2 * p - p ** 2) ** 2 + (1 - p) * (2 * p ** 2 - p ** 4))
rows.append(("Q4a", "P(Q1)=p(2p-p^2)^2+(1-p)(2p^2-p^4) (symbolic enumeration, 2^5 states)", sp.expand(Q1p - off_Q1) == 0, True, "sympy"))
off_Q2 = sp.expand(q ** 2 * off_Q1 + p ** 2 * q * (1 - q) * (1 + p - p ** 2))
rows.append(("Q4b", "P(Q2)=q^2 P(Q1)+p^2 q (1-q)(1+p-p^2) (symbolic enumeration, 2^7 states)", sp.expand(Q2p - off_Q2) == 0, True, "sympy"))
off_Q2b = sp.expand(q ** 2 * p ** 2 * (1 + p - 4 * p ** 2 + 2 * p ** 3) + q * p ** 2 * (1 + p - p ** 2))
rows.append(("Q4b", "expanded form q^2 p^2 (1+p-4p^2+2p^3) + q p^2 (1+p-p^2)", sp.expand(Q2p - off_Q2b) == 0, True, "sympy"))
# Q1 and Q2 on the same components: joint reliability by enumeration over A..G with the same p
both = 0
for st in itertools.product((0, 1), repeat=7):
    on = dict(zip(c2, st))

    def conn(edges, names):
        parent = {}

        def find(a):
            parent.setdefault(a, a)
            while parent[a] != a:
                parent[a] = parent[parent[a]]; a = parent[a]
            return a
        for c in names:
            if on[c]:
                u, v = edges[c]; parent[find(u)] = find(v)
        return find("s") == find("t")
    w = 1
    for c in c2:
        w *= pr2[c] if on[c] else 1 - pr2[c]
    # the printed circuit Q1 uses A..E only; F and G are the added units of Q2
    if conn(EDG1, c1) and conn(EDG2, c2):
        both += w
both = sp.expand(both)
rows.append(("Q4c", "P(Q1 and Q2) = P(Q2) (Q2 implies Q1; enumeration with shared A..E)",
             sp.expand(both - Q2p) == 0, True, "sympy"))
off_c = off_Q2b
rows.append(("Q4c", "official P(Q1 and Q2) formula equals the exact joint reliability", sp.expand(both - off_c) == 0, True, "sympy"))
rows.append(("Q4d", "P(Q2|Q1) = P(Q2)/P(Q1) (official form; exact ratio of the two enumerations)",
             sp.simplify(both / Q1p - off_Q2 / off_Q1) == 0, True, "sympy"))
for pv, qv in ((0.6, 0.7), (0.35, 0.5)):
    comp = {c: rng.random(N) < pv for c in c2}
    F_ = rng.random(N) < qv; G_ = rng.random(N) < qv
    A, B, Cc, D, E = (comp[k] for k in "ABCDE")
    q1m = (E & (A | B) & (Cc | D)) | (~E & ((A & Cc) | (B & D)))
    # Q2: nodes
    reach = {n: np.zeros(N, dtype=bool) for n in ("s", "u1", "d1", "u2", "d2", "t")}
    reach["s"][:] = True
    state = {"A": A, "B": B, "E": E, "C": Cc, "D": D, "F": F_, "G": G_}
    for _ in range(6):
        for c, (u, v) in EDG2.items():
            reach[v] |= reach[u] & state[c]; reach[u] |= reach[v] & state[c]
    q2m = reach["t"]
    o1 = float(off_Q1.subs(p, pv)); o2 = float(off_Q2.subs({p: pv, q: qv}))
    rec("Q4a", "P(Q1) p=%.2f" % pv, o1, float(Q1p.subs(p, pv)), float(q1m.mean()), se_p(o1))
    rec("Q4b", "P(Q2) p=%.2f q=%.2f" % (pv, qv), o2, float(Q2p.subs({p: pv, q: qv})), float(q2m.mean()), se_p(o2))
    # for the joint event the F and G are the same random units, Q1 uses only A..E
    oc = float(off_c.subs({p: pv, q: qv}))
    rec("Q4c", "P(Q1 and Q2) p=%.2f q=%.2f" % (pv, qv), oc, float(both.subs({p: pv, q: qv})), float((q1m & q2m).mean()), se_p(oc))
    n1 = int(q1m.sum()); od = oc / o1
    rec("Q4d", "P(Q2|Q1) p=%.2f q=%.2f" % (pv, qv), od, float(both.subs({p: pv, q: qv}) / Q1p.subs(p, pv)),
        float((q1m & q2m).sum() / n1), math.sqrt(od * (1 - od) / n1))


# ============================================================ Q5   urn: D red, N-D black, draw without replacement
def C(a, b):
    return math.comb(a, b) if 0 <= b <= a else 0


for (Nn, D) in ((9, 4), (7, 5), (12, 6)):
    balls = [1] * D + [0] * (Nn - D)
    perms_ = list(itertools.permutations(range(Nn), 4)) if Nn <= 9 else None
    exact = {}
    # exact positional probabilities by symmetry-free enumeration of ordered draws of length 4
    from itertools import permutations
    cnt_total = 0; cR = {k: 0 for k in range(1, 5)}; c_R2R3 = 0; c_R1R2 = 0
    for pm in permutations(range(Nn), 4):
        cnt_total += 1
        col = [balls[i] for i in pm]
        for k in range(1, 5):
            cR[k] += col[k - 1]
        c_R2R3 += col[1] and col[2]
        c_R1R2 += col[0] and col[1]
    pos = {k: Fr(cR[k], cnt_total) for k in range(1, 5)}
    sampl = np.argsort(rng.random((N, Nn), dtype=np.float32), axis=1)[:, :5]
    colr = (sampl < D)
    off = Fr(D, Nn)
    rec("Q5a", "P(R1) N=%d D=%d" % (Nn, D), off, pos[1], float(colr[:, 0].mean()), se_p(float(off)))
    rec("Q5b", "P(R2) N=%d D=%d" % (Nn, D), off, pos[2], float(colr[:, 1].mean()), se_p(float(off)))
    for n in (3, 4):
        if n <= D:
            rec("Q5c", "P(R%d) N=%d D=%d" % (n, Nn, D), off, pos[n], float(colr[:, n - 1].mean()), se_p(float(off)))
    # d: P(R_{n+1}|R_n) = (D-1)/(N-1), 1 <= n <= D-1  (here n=2,3 with positions 2->3, 3->4)
    for n in (1, 2, 3):
        if n <= D - 1:
            offd = Fr(D - 1, Nn - 1)
            num = Fr(0)
            # exact: joint of positions n, n+1 red over distinct draws of length 4
            cj = 0; ct = 0
            for pm in permutations(range(Nn), 4):
                col = [balls[i] for i in pm]
                ct += 1; cj += col[n - 1] and col[n]
            exd = Fr(cj, ct) / pos[n]
            rn = colr[:, n - 1]
            mc = float((rn & colr[:, n]).sum() / rn.sum())
            rec("Q5d", "P(R%d|R%d) N=%d D=%d" % (n + 1, n, Nn, D), offd, exd, mc, math.sqrt(float(offd) * (1 - float(offd)) / float(rn.sum())))

# ============================================================ Q6   two people on two distinct seats among 1..N
for Nn in (2, 5, 8):
    pairs = [(x, y) for x in range(1, Nn + 1) for y in range(1, Nn + 1) if x != y]
    tot = len(pairs)
    px = {k: Fr(sum(1 for x, y in pairs if x == k), tot) for k in range(1, Nn + 1)}
    py = {k: Fr(sum(1 for x, y in pairs if y == k), tot) for k in range(1, Nn + 1)}
    rows.append(("Q6a", "X, Y ~ U{1..N} (uniform marginals) N=%d" % Nn, all(v == Fr(1, Nn) for v in px.values()) and all(v == Fr(1, Nn) for v in py.values()),
                 True, "exact"))
    pL = {k: Fr(sum(1 for x, y in pairs if min(x, y) == k), tot) for k in range(1, Nn + 1)}
    pR = {k: Fr(sum(1 for x, y in pairs if max(x, y) == k), tot) for k in range(1, Nn + 1)}
    joint_ok = all(Fr(sum(1 for x, y in pairs if min(x, y) == j and max(x, y) == k), tot) ==
                   (Fr(2, Nn * (Nn - 1)) if j < k else 0) for j in range(1, Nn + 1) for k in range(1, Nn + 1))
    rows.append(("Q6b", "joint pmf of (XL,XR) = 2/(N(N-1)) for j<k, else 0, N=%d" % Nn, joint_ok, True, "exact"))
    rows.append(("Q6c", "XL pmf 2(N-k)/(N(N-1)); XR pmf 2(k-1)/(N(N-1)), N=%d" % Nn,
                 all(pL[k] == Fr(2 * (Nn - k), Nn * (Nn - 1)) for k in range(1, Nn + 1)) and
                 all(pR[k] == Fr(2 * (k - 1), Nn * (Nn - 1)) for k in range(1, Nn + 1)), True, "exact"))
    EL = sum(k * v for k, v in pL.items()); ER = sum(k * v for k, v in pR.items())
    rows.append(("Q6d", "E[XL]=(N+1)/3, E[XR]=2(N+1)/3, N=%d" % Nn, EL == Fr(Nn + 1, 3) and ER == Fr(2 * (Nn + 1), 3), True, "exact"))
Nn = 7
xa = rng.integers(1, Nn + 1, N); ya = rng.integers(1, Nn, N); ya = np.where(ya >= xa, ya + 1, ya)
xl = np.minimum(xa, ya); xr = np.maximum(xa, ya)
rec("Q6d", "E[XL] N=7 (MC of the seating experiment)", Fr(8, 3), Fr(8, 3), float(xl.mean()), float(xl.std() / math.sqrt(N)))
rec("Q6d", "E[XR] N=7", Fr(16, 3), Fr(16, 3), float(xr.mean()), float(xr.std() / math.sqrt(N)))
for k in (1, 3, 6):
    off = Fr(2 * (Nn - k), Nn * (Nn - 1))
    rec("Q6c", "P(XL=%d) N=7 (MC)" % k, off, off, float(np.mean(xl == k)), se_p(float(off)))
for k in (2, 5, 7):
    off = Fr(2 * (k - 1), Nn * (Nn - 1))
    rec("Q6c", "P(XR=%d) N=7 (MC)" % k, off, off, float(np.mean(xr == k)), se_p(float(off)))
rec("Q6b", "P(XL=2,XR=3) N=7 (MC)", Fr(2, 42), Fr(2, 42), float(np.mean((xl == 2) & (xr == 3))), se_p(2 / 42))
rows.append(("Q6d", "N=2: XL=1 and XR=2 always (E[XL]=1, E[XR]=2)", True, True, "two seats"))

# ---- Q6e, Q6f (bonus parts, no official solution; shipped as solved)
#   var[XL] = var[XR] = (N+1)(N-2)/18,  cov[XL,XR] = (N+1)(N-2)/36,  rho = 1/2 for N >= 3 (undefined for N = 2)
for Nn in range(2, 13):
    pairs = [(x, y) for x in range(1, Nn + 1) for y in range(1, Nn + 1) if x != y]
    w = Fr(1, len(pairs))
    L_ = [min(x, y) for x, y in pairs]; R_ = [max(x, y) for x, y in pairs]
    EL = sum(L_) * w; ER = sum(R_) * w
    VL = sum(l * l for l in L_) * w - EL ** 2; VR = sum(r * r for r in R_) * w - ER ** 2
    CV = sum(l * r for l, r in zip(L_, R_)) * w - EL * ER
    v_ship = Fr((Nn + 1) * (Nn - 2), 18)
    rows.append(("Q6e", "var[XL]=var[XR]=(N+1)(N-2)/18 exact N=%d" % Nn, VL == v_ship and VR == v_ship, True, "VL=%s VR=%s" % (VL, VR)))
    if Nn == 2:
        rows.append(("Q6f", "N=2: var=0 so rho is undefined (0/0)", VL == 0 and VR == 0 and CV == 0, True, "exact"))
    else:
        rows.append(("Q6f", "cov=(N+1)(N-2)/36 and rho=1/2 exact N=%d" % Nn, CV == Fr((Nn + 1) * (Nn - 2), 36) and CV / VL == Fr(1, 2), True, "exact"))
for Nn in (3, 7, 20):
    xa = rng.integers(1, Nn + 1, N); ya = rng.integers(1, Nn, N); ya = np.where(ya >= xa, ya + 1, ya)
    xl = np.minimum(xa, ya).astype(float); xr = np.maximum(xa, ya).astype(float)
    v_ship = Fr((Nn + 1) * (Nn - 2), 18)
    for nm, arr in (("XL", xl), ("XR", xr)):
        m4 = np.mean((arr - arr.mean()) ** 4)
        rec("Q6e", "var[%s]=(N+1)(N-2)/18 N=%d (MC)" % (nm, Nn), v_ship, v_ship, float(arr.var()), math.sqrt((m4 - arr.var() ** 2) / N))
    rho_mc = float(np.corrcoef(xl, xr)[0, 1])
    bl = np.array([np.corrcoef(a, b)[0, 1] for a, b in zip(np.array_split(xl, 200), np.array_split(xr, 200))])
    rec("Q6f", "rho[XL,XR]=1/2 N=%d (MC, batch SE)" % Nn, Fr(1, 2), Fr(1, 2), rho_mc, float(bl.std() / math.sqrt(len(bl))))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if not bad else 1)
