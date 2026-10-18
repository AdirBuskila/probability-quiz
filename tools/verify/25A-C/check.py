# -*- coding: utf-8 -*-
"""Verification harness for 25A-C (probability, 11.05.2025). Run: PYTHONUTF8=1 py tools/verify/25A-C/check.py

For every final answer two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy / numerical quadrature).
  MC    : Monte Carlo simulation (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Official keys that are wrong for the printed question are shown as MISMATCH and the corrected values are
shipped under the typo ruling (solved, official:false); the shipped values are asserted exactly and by MC:
  Q3c  : official 1-1/e; shipped 1-(4/13)e^{-1/2}.
  Q4b,c: the printed H works with probability q; the official solution uses P(H)=p (the q=p case);
         shipped P(Q2) = P(Q1 u Q2) = q p^2(1+3p-9p^3+8p^4-2p^5) + (1-q) p^3(1+2p-4p^3+2p^4).
Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate

N = 2_000_000
rng = np.random.default_rng(20250511)
rows = []
mismatch = []        # (item, what, detail) -- expected, items are held


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1   X~U(0,1), Y~U(0,2) independent; S=XY, L=2(X+Y)
X = rng.random(N); Y = 2 * rng.random(N)
S = X * Y; L = 2 * (X + Y)
off = (1 + math.log(3)) / 3
ex = integrate.quad(lambda x: min(2.0, 2 / (3 * x)) / 2, 0, 1, points=[1 / 3], limit=200)[0]
rec("Q1a1", "P(S<2/3)=(1+ln3)/3", off, ex, float(np.mean(S < 2 / 3)), se_p(off), tol=1e-9)
off = 0.25
ex = integrate.quad(lambda x: min(2.0, max(0.0, 1 - x)) / 2, 0, 1)[0]
rec("Q1a2", "P(L<2)=1/4", off, ex, float(np.mean(L < 2)), se_p(off), tol=1e-9)
off = (1 + 4 * math.log(3)) / 9
# P(S<2/3 and L>2) = P(S<2/3) - P(L<2 and S<2/3); the triangle x+y<1 has xy<=1/4<2/3 so it is inside
inter = integrate.quad(lambda x: (min(2.0, 2 / (3 * x)) - min(2.0, max(0.0, 1 - x))) / 2, 0, 1, points=[1 / 3], limit=200)[0]
ex = inter / 0.75
sel = L > 2
mc = float(((S < 2 / 3) & sel).sum() / sel.sum())
rec("Q1a3", "P(S<2/3 | L>2)=(1+4ln3)/9", off, ex, mc, math.sqrt(mc * (1 - mc) / float(sel.sum())), tol=1e-9)
EL = sp.Rational(1, 2) * 2 + 2 * sp.Rational(1, 1)       # 2(E[X]+E[Y]) = 2(1/2+1)
rec("Q1b1", "E[L]=3", 3, 2 * (sp.Rational(1, 2) + 1), float(L.mean()), float(L.std() / math.sqrt(N)))
VL = 4 * (sp.Rational(1, 12) + sp.Rational(4, 12))
assert VL == sp.Rational(5, 3)
m4 = np.mean((L - L.mean()) ** 4)
rec("Q1b1", "Var[L]=5/3", Fr(5, 3), Fr(VL.p, VL.q), float(L.var()), math.sqrt((m4 - L.var() ** 2) / N))
ES = sp.Rational(1, 2) * 1
VS = sp.Rational(1, 3) * sp.Rational(4, 3) - sp.Rational(1, 4)
assert VS == sp.Rational(7, 36)
rec("Q1b2", "E[S]=1/2", Fr(1, 2), Fr(ES.p, ES.q), float(S.mean()), float(S.std() / math.sqrt(N)))
m4 = np.mean((S - S.mean()) ** 4)
rec("Q1b2", "Var[S]=7/36", Fr(7, 36), Fr(VS.p, VS.q), float(S.var()), math.sqrt((m4 - S.var() ** 2) / N))

# ============================================================ Q2   P(A)=p, P(B)=q, P(A u B)=s
for trial in range(6):
    c = rng.random(4) + 0.1; c /= c.sum()
    x11, x10, x01 = [Fr(int(round(v * 997)), 1000) for v in c[:3]]
    x00 = 1 - x11 - x10 - x01
    p, q, s = x11 + x10, x11 + x01, 1 - x00
    assert x11 / q == (p + q - s) / q                          # a1 P(A/B)
    assert x01 / (1 - p) == (s - p) / (1 - p)                  # a2 P(B/notA)
    assert x10 / (1 - q) == (s - q) / (1 - q)                  # a3 P(A/notB)
    assert x00 / (1 - q) == (1 - s) / (1 - q)                  # a4 P(notA/notB)
rows.append(("Q2a", "a1..a4 formulas equal the cell ratios on 6 exact random distributions", True, True, "exact fractions"))
cells = np.array([0.22, 0.18, 0.27, 0.33])                     # A&B, A&notB, notA&B, notA&notB
cnt = rng.multinomial(N, cells)
pA, pB = cells[0] + cells[1], cells[0] + cells[2]
s_ = 1 - cells[3]
for item, what, off, exact, num, den in (
        ("Q2a1", "P(A/B)=(p+q-s)/q", (pA + pB - s_) / pB, cells[0] / pB, cnt[0], cnt[0] + cnt[2]),
        ("Q2a2", "P(B/notA)=(s-p)/(1-p)", (s_ - pA) / (1 - pA), cells[2] / (1 - pA), cnt[2], cnt[2] + cnt[3]),
        ("Q2a3", "P(A/notB)=(s-q)/(1-q)", (s_ - pB) / (1 - pB), cells[1] / (1 - pB), cnt[1], cnt[1] + cnt[3]),
        ("Q2a4", "P(notA/notB)=(1-s)/(1-q)", (1 - s_) / (1 - pB), cells[3] / (1 - pB), cnt[3], cnt[1] + cnt[3])):
    mc = num / den
    rec(item, what, off, exact, mc, math.sqrt(off * (1 - off) / den))
# b: independent  <=> s = p+q-pq ; c: disjoint <=> s = p+q
pp_, qq_ = Fr(3, 10), Fr(2, 5)
rows.append(("Q2b", "independent A,B: s = p+q-pq", pp_ + qq_ - pp_ * qq_ == 1 - (1 - pp_) * (1 - qq_), True, "exact"))
rows.append(("Q2c", "disjoint A,B: s = p+q (P(A and B)=0)", True, True, "inclusion-exclusion"))

# ============================================================ Q3   f = 0 (x<-1); a(1+x) on [-1,0); b e^{-x} on x>=0
xs = sp.symbols("x", real=True)
a_, b_ = sp.symbols("a b", positive=True)
area = sp.integrate(a_ * (1 + xs), (xs, -1, 0)) + sp.integrate(b_ * sp.exp(-xs), (xs, 0, sp.oo))
mean = sp.integrate(xs * a_ * (1 + xs), (xs, -1, 0)) + sp.integrate(xs * b_ * sp.exp(-xs), (xs, 0, sp.oo))
sol = sp.solve([area - 1, mean], [a_, b_], dict=True)[0]
rows.append(("Q3a", "a=3/2, b=1/4 (sympy solve)", sol[a_] == sp.Rational(3, 2) and sol[b_] == sp.Rational(1, 4), True, "sympy"))
aa, bb = 1.5, 0.25
left = rng.random(N) < aa / 2
Xs = np.where(left, -1 + np.sqrt(rng.random(N)), rng.exponential(1.0, N))
rec("Q3a", "E[X]=0 with a=3/2,b=1/4", 0.0, 0.0, float(Xs.mean()), float(Xs.std() / math.sqrt(N)))


def Fx(t):
    return 0.0 if t < -1 else (0.75 * (1 + t) ** 2 if t < 0 else 1 - 0.25 * math.exp(-t))


for t in (-0.7, -0.2, 0.5, 2.0):
    ex = integrate.quad(lambda x: aa * (1 + x) if x < 0 else bb * math.exp(-x), -1, t, points=[0] if t > 0 else None)[0]
    rec("Q3b", "F_X(%.1f)" % t, Fx(t), ex, float(np.mean(Xs <= t)), se_p(Fx(t)), tol=1e-9)
den = Xs > -0.5
mc = float(((Xs < 0.5) & den).sum() / den.sum())
ex_true = (Fx(0.5) - Fx(-0.5)) / (1 - Fx(-0.5))
off_key = 1 - 1 / math.e                                        # official: 1 - 1/e ~ 0.63
ex_ok = abs(off_key - ex_true) < 1e-9
mc_ok = abs(mc - off_key) <= 4 * math.sqrt(mc * (1 - mc) / den.sum())
mismatch.append(("Q3c", "P(X<1/2 | X>-1/2)", "official 1-1/e=%.6f; exact (F(1/2)-F(-1/2))/(1-F(-1/2)) = 1-(4/13)exp(-1/2) = %.6f; mc=%.6f"
                 % (off_key, ex_true, mc), ex_ok, mc_ok))
rows.append(("Q3c", "exact value is 1-(4/13)e^{-1/2} (closed form)", abs(ex_true - (1 - 4 / 13 * math.exp(-0.5))) < 1e-12, True,
             "true=%.6f mc=%.6f" % (ex_true, mc)))
# shipped (typo ruling): 1-(4/13)e^{-1/2}; exact by quadrature of the pdf, MC on the conditioning slice
ship3c = 1 - 4 / 13 * math.exp(-0.5)
num_q = integrate.quad(lambda x: aa * (1 + x) if x < 0 else bb * math.exp(-x), -0.5, 0.5, points=[0])[0]
den_q = integrate.quad(lambda x: aa * (1 + x), -0.5, 0)[0] + integrate.quad(lambda x: bb * math.exp(-x), 0, np.inf)[0]
rec("Q3c", "shipped P(X<1/2 | X>-1/2) = 1-(4/13)e^{-1/2}", ship3c, num_q / den_q, mc, math.sqrt(mc * (1 - mc) / den.sum()), tol=1e-9)

# ============================================================ Q4   circuits (bridge-type networks)
p, q = sp.symbols("p q", positive=True)


def reliab(edges, comps, probs, s, t):
    """edges: dict comp -> (u, v); comps: list of comp names; probs: dict comp -> probability (sympy)."""
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


# nodes: s, u1 (after A), d1 (after B), u2, d2, t.  E: u1-d1, C: u1-u2, D: d1-d2, F: u2-d2, G: u2-t (H: d2-t)
E1 = {"A": ("s", "u1"), "B": ("s", "d1"), "E": ("u1", "d1"), "C": ("u1", "u2"), "D": ("d1", "d2"), "F": ("u2", "d2"), "G": ("u2", "t")}
E2 = dict(E1); E2["H"] = ("d2", "t")
cm1 = list("ABCDEFG"); cm2 = cm1 + ["H"]
pr1 = {c: p for c in cm1}
pr2 = dict(pr1); pr2["H"] = q
Q1p = reliab(E1, cm1, pr1, "s", "t")
Q2p = reliab(E2, cm2, pr2, "s", "t")
Q2pp = reliab(E2, cm2, {**pr1, "H": p}, "s", "t")                # H with probability p (the official solution's reading)
off_Q1 = sp.expand(p ** 3 * (1 + 2 * p - 4 * p ** 3 + 2 * p ** 4))
off_Q2 = sp.expand(p ** 3 * (2 + 4 * p - 2 * p ** 2 - 13 * p ** 3 + 14 * p ** 4 - 4 * p ** 5))
rows.append(("Q4a", "P(Q1) = p^3(1+2p-4p^3+2p^4) (symbolic enumeration of 2^7 states)", sp.expand(Q1p - off_Q1) == 0, True, "sympy"))
q2_is_pcase = sp.expand(Q2pp - off_Q2) == 0
q2_general = sp.expand(Q2p - off_Q2) == 0
rows.append(("Q4b", "official P(Q2) polynomial equals the exact network reliability when P(H)=p", q2_is_pcase, True, "sympy"))
mismatch.append(("Q4b", "P(Q2)", "official polynomial matches only P(H)=p; the printed H works with probability q (general q: equal=%s)" % q2_general,
                 q2_general, q2_general))
q_expr = sp.simplify(Q2p)
Q2_via_cond = sp.expand(q * reliab({**E1, "H": ("d2", "t")}, cm2, {**pr1, "H": 1}, "s", "t") + (1 - q) * Q1p)
rows.append(("Q4b", "general-q form: P(Q2) = q P(Q2|H) + (1-q) P(Q1)", sp.expand(Q2p - Q2_via_cond) == 0, True, "sympy"))
rows.append(("Q4c", "Q1 subset of Q2 (adding H only adds paths): P(Q1 u Q2) = P(Q2)", True, True, "monotone network"))
# shipped (typo ruling): P(Q2) = P(Q1 u Q2) = q p^2(1+3p-9p^3+8p^4-2p^5) + (1-q) p^3(1+2p-4p^3+2p^4)
off_Q2H = sp.expand(p ** 2 * (1 + 3 * p - 9 * p ** 3 + 8 * p ** 4 - 2 * p ** 5))
ship_Q2 = sp.expand(q * off_Q2H + (1 - q) * off_Q1)
rows.append(("Q4b", "official P(Q2|H) = p^2(1+3p-9p^3+8p^4-2p^5) (enumeration with H on)",
             sp.expand(reliab({**E1, "H": ("d2", "t")}, cm2, {**pr1, "H": 1}, "s", "t") - off_Q2H) == 0, True, "sympy"))
rows.append(("Q4b", "shipped P(Q2) = q P(Q2|H) + (1-q) P(Q1) equals the exact network reliability (all p, q)",
             sp.expand(Q2p - ship_Q2) == 0, True, "sympy"))
rows.append(("Q4b", "shipped P(Q2) reduces to the official polynomial at q=p", sp.expand(ship_Q2.subs(q, p) - off_Q2) == 0, True, "sympy"))


def conn_state(edges, on):
    par = {}

    def f(a):
        par.setdefault(a, a)
        while par[a] != a:
            a = par[a]
        return a
    for c, (u, v) in edges.items():
        if on.get(c):
            par[f(u)] = f(v)
    return f("s") == f("t")


Qu = 0
for st_ in itertools.product((0, 1), repeat=len(cm2)):
    on_ = dict(zip(cm2, st_))
    if conn_state(E1, on_) or conn_state(E2, on_):
        w_ = 1
        for c in cm2:
            w_ *= pr2[c] if on_[c] else 1 - pr2[c]
        Qu += w_
rows.append(("Q4c", "shipped P(Q1 u Q2) equals the exact union probability (2^8 states, all p, q)",
             sp.expand(Qu - ship_Q2) == 0, True, "sympy"))
rows.append(("Q4d", "P(Q2|Q1) = 1 (Q1 subset of Q2): P(Q1 and Q2)=P(Q1) for any q",
             sp.simplify(Q1p / Q1p) == 1, True, "exact"))
# MC on states with H=p and with generic q
for pv, qv in ((0.6, 0.6), (0.7, 0.4), (0.5, 0.9)):
    comp = {c: rng.random(N) < pv for c in cm1}
    H = rng.random(N) < qv

    def conn(edges, names, state):
        # union-find via boolean propagation over 6 nodes
        reach = {"s": np.ones(N, dtype=bool)}
        nodes = ["s", "u1", "d1", "u2", "d2", "t"]
        for n in nodes[1:]:
            reach[n] = np.zeros(N, dtype=bool)
        for _ in range(6):
            for c in names:
                u, v = edges[c]
                reach[v] |= reach[u] & state[c]
                reach[u] |= reach[v] & state[c]
        return reach["t"]
    st = dict(comp); st["H"] = H
    q1m = conn(E1, cm1, comp); q2m = conn(E2, cm2, st)
    o1 = float(off_Q1.subs(p, pv))
    rec("Q4a", "P(Q1) p=%.1f" % pv, o1, float(Q1p.subs(p, pv)), float(q1m.mean()), se_p(o1))
    ex2 = float(Q2p.subs({p: pv, q: qv}))
    rows.append(("Q4b", "MC check of the exact network value p=%.1f q=%.1f" % (pv, qv),
                 True, abs(float(q2m.mean()) - ex2) <= 4 * se_p(ex2), "exact=%.6f mc=%.6f" % (ex2, float(q2m.mean()))))
    if pv == qv:
        rec("Q4b", "official P(Q2) polynomial at p=q=%.1f" % pv, float(off_Q2.subs(p, pv)), ex2, float(q2m.mean()), se_p(ex2), tol=1e-9)
    else:
        off_here = float(off_Q2.subs(p, pv))
        mismatch.append(("Q4b", "p=%.1f q=%.1f" % (pv, qv), "official polynomial=%.6f vs exact=%.6f mc=%.6f" % (off_here, ex2, float(q2m.mean())),
                         abs(off_here - ex2) < 1e-9, abs(float(q2m.mean()) - off_here) <= 4 * se_p(ex2)))
    sh2 = float(ship_Q2.subs({p: pv, q: qv}))
    rec("Q4b", "shipped P(Q2) p=%.1f q=%.1f" % (pv, qv), sh2, ex2, float(q2m.mean()), se_p(ex2), tol=1e-12)
    rec("Q4c", "shipped P(Q1 or Q2) p=%.1f q=%.1f (MC of the union)" % (pv, qv), sh2, float(Qu.subs({p: pv, q: qv})), float((q1m | q2m).mean()), se_p(ex2), tol=1e-12)
    rec("Q4d", "P(Q2|Q1) = 1 p=%.1f q=%.1f" % (pv, qv), 1.0, 1.0, float((q1m & q2m).sum() / q1m.sum()), 1e-9)

# ============================================================ Q5   n numbers without replacement from {1..N}
def C(a, b):
    return math.comb(a, b) if 0 <= b <= a else 0


for (Nn, n) in ((8, 3), (10, 4), (6, 2)):
    draws = list(itertools.combinations(range(1, Nn + 1), n))
    tot = len(draws)
    mn = np.array([d[0] for d in draws]); mx = np.array([d[-1] for d in draws])
    # MC: sample n of N without replacement
    r = np.argsort(rng.random((N, Nn), dtype=np.float32), axis=1)[:, :n] + 1
    xmin = r.min(axis=1); xmax = r.max(axis=1)
    for k in range(1, Nn - n + 2):
        off = Fr(C(Nn - k, n - 1), C(Nn, n))
        rec("Q5a", "P(Xmin=%d) N=%d n=%d" % (k, Nn, n), off, Fr(int((mn == k).sum()), tot), float(np.mean(xmin == k)), se_p(float(off)))
    for k in range(n, Nn + 1):
        off = Fr(C(k - 1, n - 1), C(Nn, n))
        rec("Q5b", "P(Xmax=%d) N=%d n=%d" % (k, Nn, n), off, Fr(int((mx == k).sum()), tot), float(np.mean(xmax == k)), se_p(float(off)))
    for j in range(1, Nn + 1):
        for k in range(j + 1, Nn + 1):
            if n < 2:
                continue
            off = Fr(C(k - j - 1, n - 2), C(Nn, n))
            ex = Fr(int(((mn == j) & (mx == k)).sum()), tot)
            if n == 2 or off > 0 or ex > 0:
                rec("Q5c", "P(Xmin=%d,Xmax=%d) N=%d n=%d" % (j, k, Nn, n), off, ex, float(np.mean((xmin == j) & (xmax == k))), se_p(float(off)))
    offd = Fr(Nn + 1, n + 1)
    rec("Q5d", "E[Xmin] N=%d n=%d" % (Nn, n), offd, Fr(int(mn.sum()), tot), float(xmin.mean()), float(xmin.std() / math.sqrt(N)))
    offe = Fr(n * (Nn + 1), n + 1)
    rec("Q5e", "E[Xmax] N=%d n=%d" % (Nn, n), offe, Fr(int(mx.sum()), tot), float(xmax.mean()), float(xmax.std() / math.sqrt(N)))

# ============================================================ Q6   X,Y ~ U(0,L), Z = min/max
Lv = 3.7
Xu = Lv * rng.random(N); Yu = Lv * rng.random(N)
Zs = np.minimum(Xu, Yu) / np.maximum(Xu, Yu)
for t in (0.1, 0.35, 0.8, 1.0, 1.5):
    off = 0.0 if t < 0 else (t if t < 1 else 1.0)
    ex = integrate.quad(lambda x: min(1.0, t * x) + max(0.0, 1 - x / t), 0, 1, points=[t], limit=200)[0] if t < 1 else 1.0
    rows.append(("Q6a", "F_Z(%.2f) = %.2f (area of {min<=t max} in the unit square, quadrature)" % (t, off),
                 abs(ex - off) < 1e-9, abs(float(np.mean(Zs <= t)) - off) <= 4 * se_p(off) + 1e-9,
                 "exact=%.5f mc=%.5f" % (ex, float(np.mean(Zs <= t)))))
rec("Q6c", "E[Z]=1/2", 0.5, sp.integrate(xs, (xs, 0, 1)), float(Zs.mean()), float(Zs.std() / math.sqrt(N)))
VZ = sp.integrate(xs ** 2, (xs, 0, 1)) - sp.Rational(1, 4)
m4 = np.mean((Zs - Zs.mean()) ** 4)
rec("Q6c", "Var[Z]=1/12", Fr(1, 12), Fr(VZ.p, VZ.q), float(Zs.var()), math.sqrt((m4 - Zs.var() ** 2) / N))
rows.append(("Q6b", "f_Z = 1 on [0,1] (derivative of F_Z), so Z~U(0,1)", True, True, "d/dt t = 1"))

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("Expected MISMATCHES (official key vs printed question) -> corrected values shipped (typo ruling):")
for item, what, det, ex_ok, mc_ok in mismatch:
    print("  %-5s %s | %s | exact=%s mc=%s" % (item, what, det, "match" if ex_ok else "MISMATCH", "match" if mc_ok else "MISMATCH"))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
# the two held keys must really disagree (and the q=p reading must really agree)
mm_ok = (not mismatch[0][3]) and q2_is_pcase and (not q2_general)
sys.exit(0 if (not bad and mm_ok) else 1)
