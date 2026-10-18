# -*- coding: utf-8 -*-
"""Verification harness for 25B-A (probability, 15.07.2025). Run: PYTHONUTF8=1 py tools/verify/25B-A/check.py

For every final answer two independent checks:
  EXACT : the official formula (at sample parameters) equals an independent exact computation
          (fractions / enumeration / sympy / numerical quadrature).
  MC    : Monte Carlo simulation (>= 10^6 trials) agrees with the official formula within 4 standard errors.
Symbolic answers are checked at sample parameter values. Official keys are never changed here.
Output is ASCII only.
"""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy import integrate
from scipy import stats

N = 2_000_000
rng = np.random.default_rng(20250715)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1  (X, Y ~ U(0,1) independent; S = XY/2, L = sqrt(X^2+Y^2))
X = rng.random(N); Y = rng.random(N)
L = np.hypot(X, Y); S = X * Y / 2
off = math.pi / 4
ex = integrate.quad(lambda x: math.sqrt(1 - x * x), 0, 1)[0]
rec("Q1b", "P(L<1)=pi/4", off, ex, float(np.mean(L < 1)), se_p(off), tol=1e-9)
off = 0.5 * (1 + math.log(2))
ex = integrate.quad(lambda x: min(1.0, 1 / (2 * x)), 0, 1, points=[0.5], limit=200)[0]
rec("Q1c", "P(S<1/4)=(1+ln2)/2", off, ex, float(np.mean(S < 0.25)), se_p(off), tol=1e-9)
off = math.pi / (2 * (1 + math.log(2)))
inter = integrate.quad(lambda x: min(math.sqrt(1 - x * x), 1 / (2 * x)), 0, 1, points=[1 / math.sqrt(2)], limit=200)[0]
ex = inter / (0.5 * (1 + math.log(2)))
sel = S < 0.25
mc = float(((L < 1) & sel).sum() / sel.sum())
rec("Q1d", "P(L<1 | S<1/4)", off, ex, mc, math.sqrt(mc * (1 - mc) / float(sel.sum())), tol=1e-9)
rows.append(("Q1d", "{L<1} lies inside {S<1/4} (so the intersection area is pi/4)",
             bool(np.all(S[L < 1] < 0.25)), True, "pointwise on the sample"))
x_, y_ = sp.symbols("x y", positive=True)
ES = sp.integrate(sp.integrate(x_ * y_ / 2, (x_, 0, 1)), (y_, 0, 1))
VS = sp.Rational(1, 4) * (sp.Rational(1, 9) - sp.Rational(1, 16))
assert ES == sp.Rational(1, 8) and VS == sp.Rational(7, 576)
rec("Q1e", "E[S]=1/8", Fr(1, 8), Fr(ES.p, ES.q), float(S.mean()), float(S.std() / math.sqrt(N)))
m4 = np.mean((S - S.mean()) ** 4)
rec("Q1e", "Var[S]=7/576", Fr(7, 576), Fr(VS.p, VS.q), float(S.var()), math.sqrt((m4 - S.var() ** 2) / N))

# ============================================================ Q2  P(A/B)=p, P(not-A / not-B)=q, P(A u B)=s
for trial in range(6):
    c = rng.random(4) + 0.1; c /= c.sum()
    x11, x10, x01 = [Fr(int(round(v * 997)), 1000) for v in c[:3]]
    x00 = 1 - x11 - x10 - x01
    pA = x11 + x10; pB = x11 + x01
    p_ = x11 / pB; q_ = x00 / (x00 + x10); s_ = 1 - x00
    off_PB = 1 - (1 - s_) / q_
    off_PA = s_ - (1 - p_) * off_PB
    off_PAB = p_ * off_PB
    assert off_PB == pB and off_PA == pA and off_PAB == x11
    assert q_ >= 1 - s_                                     # b: q < 1-s is impossible
rows.append(("Q2a", "P(A), P(B), P(A and B) formulas equal the cell sums on 6 exact random distributions", True, True, "exact fractions"))
rows.append(("Q2b", "q >= 1-s on 6 exact random distributions (q<1-s impossible)", True, True, "exact fractions"))
cells = np.array([0.30, 0.15, 0.20, 0.35])                    # (A&B, A&notB, notA&B, notA&notB)
cnt = rng.multinomial(N, cells)
cA = (cnt[0] + cnt[1]) / N; cB = (cnt[0] + cnt[2]) / N; cAB = cnt[0] / N
pB_ = cells[0] + cells[2]
p_ = cells[0] / pB_; q_ = cells[3] / (cells[3] + cells[1]); s_ = 1 - cells[3]
PBf = 1 - (1 - s_) / q_; PAf = s_ - (1 - p_) * PBf; PABf = p_ * PBf
rec("Q2a", "P(A) formula", PAf, cells[0] + cells[1], cA, se_p(PAf))
rec("Q2a", "P(B) formula", PBf, pB_, cB, se_p(PBf))
rec("Q2a", "P(A and B) formula", PABf, cells[0], cAB, se_p(PABf))
a11, a10, a01, a00 = sp.symbols("x11 x10 x01 x00", positive=True)
pp = a11 / (a11 + a01); qq = a00 / (a00 + a10)
num = sp.simplify((pp + qq - 1) * (a11 + a01) * (a00 + a10))
rows.append(("Q2c", "p+q-1 has numerator x11*x00 - x10*x01 (independence), so independence <=> p = 1-q",
             sp.simplify(num - (a11 * a00 - a10 * a01)) == 0, True, "sympy"))
pa, pb = Fr(3, 10), Fr(2, 5)
x11, x10, x01, x00 = pa * pb, pa * (1 - pb), (1 - pa) * pb, (1 - pa) * (1 - pb)
rows.append(("Q2c", "independent A,B => p + q = 1", x11 / (x11 + x01) + x00 / (x00 + x10) == 1, True, "exact"))


# ============================================================ Q3  three bridges, N1,N2,N3 gates each open w.p. p
def bridge_exact(Ns, p):
    pQ = Fr(0); pA2 = Fr(0)
    for st in itertools.product((0, 1), repeat=sum(Ns)):
        w = Fr(1)
        for s in st:
            w *= p if s else 1 - p
        i = 0; ok = []
        for n in Ns:
            ok.append(all(st[i:i + n])); i += n
        if any(ok):
            pQ += w
            if ok[1]:
                pA2 += w
    return pQ, pA2 / pQ, 1 - pA2 / pQ


for Ns, p in (((2, 1, 3), Fr(3, 5)), ((1, 2, 2), Fr(1, 2)), ((3, 2, 1), Fr(7, 10))):
    N1, N2, N3 = Ns
    pf = float(p)
    offQ = 1 - (1 - p ** N1) * (1 - p ** N2) * (1 - p ** N3)
    offB = p ** N2 / offQ
    offC = 1 - offB
    exQ, exB, exC = bridge_exact(Ns, p)
    ok1 = (rng.random((N, N1)) < pf).all(axis=1)
    ok2 = (rng.random((N, N2)) < pf).all(axis=1)
    ok3 = (rng.random((N, N3)) < pf).all(axis=1)
    Qm = ok1 | ok2 | ok3
    nQ = int(Qm.sum())
    mcQ = float(Qm.mean()); mcB = float((ok2 & Qm).sum() / nQ); mcC = 1 - mcB
    tag = "N=%s p=%s" % (Ns, p)
    seB = math.sqrt(float(offB) * (1 - float(offB)) / nQ)
    rec("Q3a", "P(Q) " + tag, offQ, exQ, mcQ, se_p(float(offQ)))
    rec("Q3b", "P(A2|Q) " + tag, offB, exB, mcB, seB)
    rec("Q3c", "P(not A2|Q) " + tag, offC, exC, mcC, seB)

# ============================================================ Q4  f = 0 (x<-1); a(x+1) on [-1,0); b on [0,1); c/x^3+g on x>=1
xs = sp.symbols("x", real=True)
rows.append(("Q4a", "int_1^oo 1/x dx and int_1^oo 1 dx diverge: finite variance forces c=0 and g=0",
             sp.integrate(1 / xs, (xs, 1, sp.oo)) == sp.oo and sp.integrate(1 + 0 * xs, (xs, 1, sp.oo)) == sp.oo, True, "sympy"))
for mu in (sp.Rational(1, 4), sp.Rational(0), sp.Rational(-1, 5), sp.Rational(1, 2), sp.Rational(-1, 3)):
    a_, b_ = sp.symbols("a b")
    area = sp.integrate(a_ * (xs + 1), (xs, -1, 0)) + sp.integrate(b_, (xs, 0, 1))
    mean = sp.integrate(xs * a_ * (xs + 1), (xs, -1, 0)) + sp.integrate(xs * b_, (xs, 0, 1))
    sol = sp.solve([area - 1, mean - mu], [a_, b_], dict=True)[0]
    oa, ob = sp.Rational(6, 5) * (1 - 2 * mu), sp.Rational(2, 5) * (1 + 3 * mu)
    rows.append(("Q4a", "a,b at mu=%s (sympy solve)" % mu,
                 sp.simplify(sol[a_] - oa) == 0 and sp.simplify(sol[b_] - ob) == 0, True, "a=%s b=%s" % (oa, ob)))
rows.append(("Q4b", "mu=1/2 gives a=0 (mean of U(0,1)); mu=-1/3 gives b=0 (mean of 2(x+1) on [-1,0])",
             sp.Rational(6, 5) * (1 - 2 * sp.Rational(1, 2)) == 0 and sp.Rational(2, 5) * (1 + 3 * sp.Rational(-1, 3)) == 0 and
             sp.integrate(xs * 2 * (xs + 1), (xs, -1, 0)) == sp.Rational(-1, 3), True, "sympy"))
rows.append(("Q4b", "outside [-1/3,1/2] a coefficient is negative (mu=0.6, -0.4)",
             (1 - 2 * 0.6 < 0) and (1 + 3 * -0.4 < 0), True, ""))
for mu in (sp.Rational(1, 4), sp.Rational(-1, 5), sp.Rational(1, 3)):
    aq, bq = sp.Rational(6, 5) * (1 - 2 * mu), sp.Rational(2, 5) * (1 + 3 * mu)
    left = rng.random(N) < float(aq / 2)
    Xs = np.where(left, -1 + np.sqrt(rng.random(N)), rng.random(N))   # left density 2(x+1) on [-1,0]; right uniform on [0,1)
    rec("Q4a", "E[X] mu=%s" % mu, float(mu),
        float(sp.integrate(xs * aq * (xs + 1), (xs, -1, 0)) + sp.integrate(xs * bq, (xs, 0, 1))),
        float(Xs.mean()), float(Xs.std() / math.sqrt(N)))
    for t in (-0.5, 0.3, 0.8):
        tt = sp.nsimplify(t)
        offF = float(sp.Rational(3, 5) * (1 - 2 * mu) * (tt + 1) ** 2) if t < 0 else \
            float(sp.Rational(3, 5) * (1 - 2 * mu) + sp.Rational(2, 5) * (1 + 3 * mu) * tt)
        exF = float(sp.integrate(aq * (xs + 1), (xs, -1, min(tt, 0))) + (sp.integrate(bq, (xs, 0, tt)) if t > 0 else 0))
        rec("Q4c", "F_X(%.1f) mu=%s" % (t, mu), offF, exF, float(np.mean(Xs <= t)), se_p(offF))
    den = Xs > -0.5
    rec("Q4d", "P(X<1 | X>-1/2) mu=%s (printed question; support ends at 1)" % mu, 1.0, 1.0,
        float(((Xs < 1) & den).sum() / den.sum()), 1e-9)


# ============================================================ Q5  circuits: Q0 = A and (B or C)
def Q0(a, b, c):
    return a and (b or c)


def weight(st, p):
    w = Fr(1)
    for s in st:
        w *= p if s else 1 - p
    return w


def reliability(fn, p):
    return sum((weight(st, p) for st in itertools.product((0, 1), repeat=3) if fn(*st)), Fr(0))


perms = list(itertools.permutations(range(3)))


def newcirc(perm):
    return lambda a, b, c: (lambda v: v[perm[0]] and (v[perm[1]] or v[perm[2]]))((a, b, c))


for p in (Fr(3, 10), Fr(7, 10), Fr(1, 2)):
    pf = float(p)
    offQ0 = p * p * (2 - p)
    exQ0 = reliability(Q0, p)
    comp = rng.random((N, 3)) < pf
    A_, B_, C_ = comp[:, 0], comp[:, 1], comp[:, 2]
    q0 = A_ & (B_ | C_)
    rec("Q5a", "P(Q0) p=%s" % p, offQ0, exQ0, float(q0.mean()), se_p(float(offQ0)))
    # new circuit = the same three units placed uniformly at random (6 equally likely arrangements)
    exQnew = sum(reliability(newcirc(pm), p) for pm in perms) / 6
    pick = rng.integers(0, 6, N)
    qn = np.zeros(N, dtype=bool)
    v = [A_, B_, C_]
    for k, pm in enumerate(perms):
        qn |= (pick == k) & (v[pm[0]] & (v[pm[1]] | v[pm[2]]))
    rec("Q5b1", "P(Q') p=%s" % p, offQ0, exQnew, float(qn.mean()), se_p(float(offQ0)))
    offBoth = p * p * (4 - p) / 3
    exBoth = sum((sum((weight(st, p) for st in itertools.product((0, 1), repeat=3)
                       if Q0(*st) and newcirc(pm)(*st)), Fr(0)) for pm in perms), Fr(0)) / 6
    rec("Q5b2", "P(Q0 and Q') p=%s" % p, offBoth, exBoth, float((q0 & qn).mean()), se_p(float(offBoth)))
    off3 = (4 - p) / (3 * (2 - p))
    n0 = int(q0.sum())
    mc3 = float((q0 & qn).sum() / n0)
    rec("Q5b3", "P(Q'|Q0) p=%s" % p, off3, exBoth / exQ0, mc3, math.sqrt(float(off3) * (1 - float(off3)) / n0))
    off4 = Fr(2, 3) * p * p * (1 - p) / (1 - p * p * (2 - p))
    nn0 = int((~q0).sum())
    mc4 = float((qn & ~q0).sum() / nn0)
    rec("Q5b4", "P(Q'|not Q0) p=%s" % p, off4, (exQnew - exBoth) / (1 - exQ0), mc4,
        math.sqrt(float(off4) * (1 - float(off4)) / nn0))

# ============================================================ Q6  W~Bin(N,1/365); Y~Poisson(lam p); X|Y=k
pr = 1 / 365
for Nn, k in ((365, 1), (600, 2), (30, 0)):
    off = math.comb(Nn, k) * pr ** k * (1 - pr) ** (Nn - k)
    rec("Q6a", "P(W=%d) N=%d" % (k, Nn), off, float(stats.binom.pmf(k, Nn, pr)),
        float(np.mean(rng.binomial(Nn, pr, N) == k)), se_p(off), tol=1e-12)
lam = 400.0
Xp = rng.poisson(lam, N)
Yp = rng.binomial(Xp, pr)
for k in (0, 1, 2, 3):
    off = (lam * pr) ** k * math.exp(-lam * pr) / math.factorial(k)
    ex = sum(stats.poisson.pmf(j, lam) * stats.binom.pmf(k, j, pr) for j in range(k, 2000))
    rec("Q6b1", "P(Y=%d) lam=400 p=1/365" % k, off, ex, float(np.mean(Yp == k)), se_p(off), tol=1e-10)
for k in (1, 2):
    sel = Yp == k
    nk = int(sel.sum())
    den = sum(stats.poisson.pmf(j, lam) * stats.binom.pmf(k, j, pr) for j in range(k, 2000))
    for m in (385, 399, 410):
        n = m + k
        off = math.exp(m * math.log(lam * (1 - pr)) - lam * (1 - pr) - math.lgamma(m + 1))
        ex = stats.poisson.pmf(n, lam) * stats.binom.pmf(k, n, pr) / den
        rec("Q6b2", "P(X=%d | Y=%d)" % (n, k), off, ex, float(np.mean(Xp[sel] == n)),
            math.sqrt(max(off * (1 - off), 1e-12) / nk), tol=1e-9)

# ============================================================ report
bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(0 if not bad else 1)
