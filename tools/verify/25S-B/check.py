# -*- coding: utf-8 -*-
"""Verification harness for 25S-B (probability). Run: PYTHONUTF8=1 py tools/verify/25S-B/check.py
Each final answer: EXACT (fractions / enumeration / sympy / series) and MC (>= 10^6 trials, within 4 SE). ASCII output only.
Symbolic answers are checked at sample parameter values (and as polynomial identities with sympy where possible)."""
import itertools, math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

N = 2_000_000
rng = np.random.default_rng(20251110)
rows = []


def se_p(p, n=N):
    return math.sqrt(max(p * (1 - p), 1e-300) / n)


def rec(item, what, official, exact, mc, se, tol=1e-12):
    ex_ok = abs(float(official) - float(exact)) <= tol
    mc_ok = abs(mc - float(official)) <= 4 * se + 1e-12
    rows.append((item, what, ex_ok, mc_ok,
                 "official=%.6f exact=%.6f mc=%.6f se=%.6f" % (float(official), float(exact), mc, se)))


# ============================================================ Q1  (alpha1, alpha2 ~ U(0,pi); scale-free, use unit square)
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


sq = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(1), Fr(1)), (Fr(0), Fr(1))]
half = Fr(1, 2)
tri = clip(sq, Fr(-2), Fr(1), Fr(0))                       # y > 2x
band = clip(clip(sq, Fr(1), Fr(-1), half), Fr(-1), Fr(1), half)   # |x-y| < 1/2
both = clip(clip(tri, Fr(1), Fr(-1), half), Fr(-1), Fr(1), half)
a1 = rng.random(N)
a2 = rng.random(N)
ev_t = a2 > 2 * a1
ev_b = np.abs(a1 - a2) < 0.5
rec("Q1a", "P(a2>2a1)=1/4", Fr(1, 4), area(tri), float(ev_t.mean()), se_p(0.25), tol=0)
rec("Q1b", "P(|a1-a2|<pi/2)=3/4", Fr(3, 4), area(band), float(ev_b.mean()), se_p(0.75), tol=0)
rec("Q1c", "P(both)=1/8 (area)", Fr(1, 8), area(both), float((ev_t & ev_b).mean()), se_p(0.125), tol=0)
rec("Q1c", "P(acute | a2>2a1)=1/2", Fr(1, 2), area(both) / area(tri), float(ev_b[ev_t].mean()), se_p(0.5, int(ev_t.sum())), tol=0)

# ============================================================ Q2  (numbers 1..2N+1, two draws without replacement)
for n in (2, 3, 5, 10):
    M = 2 * n + 1
    pairs = [(x, y) for x in range(1, M + 1) for y in range(1, M + 1) if x != y]
    ev_even = lambda t: t % 2 == 0
    p_a = Fr(sum(1 for x in range(1, M + 1) if x % 2 == 0), M)
    p_b = Fr(sum(1 for x, y in pairs if (x + y) % 2 == 0), len(pairs))
    first_even = [(x, y) for x, y in pairs if x % 2 == 0]
    p_c = Fr(sum(1 for x, y in first_even if (x + y) % 2 == 0), len(first_even))
    x1 = rng.integers(1, M + 1, N)
    x2 = rng.integers(1, M, N)
    x2 = np.where(x2 >= x1, x2 + 1, x2)
    rec("Q2a", "N=%d P(even)=N/(2N+1)" % n, Fr(n, M), p_a, float((x1 % 2 == 0).mean()), se_p(n / M), tol=0)
    rec("Q2b", "N=%d P(sum even)=N/(2N+1)" % n, Fr(n, M), p_b, float(((x1 + x2) % 2 == 0).mean()), se_p(n / M), tol=0)
    ev = x1 % 2 == 0
    rec("Q2c", "N=%d P(sum even | first even)=(N-1)/(2N)" % n, Fr(n - 1, 2 * n), p_c, float(((x1 + x2) % 2 == 0)[ev].mean()),
        se_p((n - 1) / (2 * n), int(ev.sum())), tol=0)

# ============================================================ Q3  (Poisson thinning)
for lam, pp in ((2.5, 0.3), (4.0, 0.6)):
    Xp = rng.poisson(lam, N)
    Yp = rng.binomial(Xp, pp)

    def pois(m, mu):
        return math.exp(-mu) * mu ** m / math.factorial(m)

    for k in (0, 1, 3):
        off = pois(k, lam * pp)
        ex = sum(math.comb(n_, k) * pp ** k * (1 - pp) ** (n_ - k) * pois(n_, lam) for n_ in range(k, 120))
        rec("Q3b", "P(Y=%d) lam=%s p=%s" % (k, lam, pp), off, ex, float((Yp == k).mean()), se_p(off), tol=1e-12)
        ev = Yp == k
        for n_ in (k, k + 1, k + 3):
            offc = math.exp(-lam * (1 - pp)) * (lam * (1 - pp)) ** (n_ - k) / math.factorial(n_ - k)
            exc = math.comb(n_, k) * pp ** k * (1 - pp) ** (n_ - k) * pois(n_, lam) / ex
            rec("Q3d", "P(X=%d|Y=%d) lam=%s p=%s" % (n_, k, lam, pp), offc, exc, float((Xp[ev] == n_).mean()),
                se_p(offc, int(ev.sum())), tol=1e-12)
    for n_ in (4, 7):
        ev = Xp == n_
        for k in (0, 2, 4):
            off = math.comb(n_, k) * pp ** k * (1 - pp) ** (n_ - k)
            rec("Q3c", "P(Y=%d|X=%d) p=%s" % (k, n_, pp), off, off, float((Yp[ev] == k).mean()), se_p(off, int(ev.sum())), tol=0)
rows.append(("Q3a", "Y takes 0,1,2,... (X unbounded)", True, bool(rng.poisson(2.5, N).max() > 8), "support unbounded"))

# ============================================================ Q4
x = sp.symbols("x", positive=True)
a_, b_, c_ = sp.symbols("a b c")
# b must vanish: integral of x^(-3/2) from 0 diverges
rows.append(("Q4a", "int_0^1 x^(-3/2) dx diverges => b=0", sp.integrate(x ** sp.Rational(-3, 2), (x, 0, 1)) == sp.oo, True, ""))
norm = sp.integrate(a_ + c_ * x, (x, 0, 1)) - 1
csol = sp.solve(norm, c_)[0]
rows.append(("Q4a", "c=2-2a from normalisation", sp.simplify(csol - (2 - 2 * a_)) == 0, True, ""))
rows.append(("Q4a", "f>=0 on (0,1] iff 0<=a<=2 (ends a and 2-a)",
             all(((a >= 0 and 2 - a >= 0) == (0 <= a <= 2)) for a in (-0.5, 0, 1, 2, 2.5)), True, ""))
mu_sym = sp.integrate(x * (a_ + (2 - 2 * a_) * x), (x, 0, 1))
rows.append(("Q4b", "E[X]=a/2+(2-2a)/3 -> a=4-6mu, c=12mu-6", sp.simplify(sp.solve(mu_sym - sp.Symbol("mu"), a_)[0] - (4 - 6 * sp.Symbol("mu"))) == 0, True, ""))
rows.append(("Q4c", "mu=0 gives a=4 outside [0,2]", 4 - 6 * 0 > 2, True, ""))
rows.append(("Q4d", "mu in [1/3, 2/3] from 0<=4-6mu<=2", (4 - 6 * (1 / 3) <= 2 + 1e-12) and (4 - 6 * (2 / 3) >= -1e-12), True, "mu_min=1/3 mu_max=2/3"))
for mu in (sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(3, 5), sp.Rational(2, 3)):
    av = 4 - 6 * mu
    af = float(av)
    # sample: F(t) = a t + (1-a) t^2
    u = rng.random(N)
    if abs(1 - af) < 1e-12:
        Xs = u
    else:
        Xs = (-af + np.sqrt(af * af + 4 * (1 - af) * u)) / (2 * (1 - af))
    rec("Q4b", "E[X] mu=%s" % mu, float(mu), float(sp.integrate(x * (av + (2 - 2 * av) * x), (x, 0, 1))), float(Xs.mean()), float(Xs.std() / math.sqrt(N)), tol=1e-12)
    off = 5 / 4 - 3 * float(mu) / 2
    ex = float(sp.integrate(av + (2 - 2 * av) * x, (x, 0, sp.Rational(1, 2))))
    rec("Q4e", "P(X<=1/2) mu=%s" % mu, off, ex, float((Xs <= 0.5).mean()), se_p(off), tol=1e-12)

# ============================================================ Q5  (circuits, enumerate 16 states)
p = sp.symbols("p")


def q1_works(A, B, C, D):
    return D and ((A and B) or C)


def q2_works(A, B, C, D):
    return B and (D or (A and C))


def poly_prob(f):
    tot = 0
    for st in itertools.product((0, 1), repeat=4):
        if f(*st):
            k = sum(st)
            tot += p ** k * (1 - p) ** (4 - k)
    return sp.expand(tot)


P1 = poly_prob(q1_works)
PG = poly_prob(lambda *s: q1_works(*s) and q2_works(*s))
P_all = p ** 4
rows.append(("Q5a", "P(Q1)=p^3+p^2-p^4 (enumeration)", sp.expand(P1 - (p ** 3 + p ** 2 - p ** 4)) == 0, True, ""))
rows.append(("Q5b", "P(Q1 and Q2)=2p^3-p^4 (enumeration)", sp.expand(PG - (2 * p ** 3 - p ** 4)) == 0, True, ""))
rows.append(("Q5c", "P(all|G)=p/(2-p)", sp.simplify(P_all / PG - p / (2 - p)) == 0, True, ""))
for pf in (0.3, 0.55, 0.8):
    st = rng.random((N, 4)) < pf
    A, B, C, D = (st[:, i] for i in range(4))
    q1 = D & ((A & B) | C)
    q2 = B & (D | (A & C))
    g = q1 & q2
    v1 = pf ** 3 + pf ** 2 - pf ** 4
    vg = 2 * pf ** 3 - pf ** 4
    rec("Q5a", "P(Q1) p=%.2f" % pf, v1, float(P1.subs(p, pf)), float(q1.mean()), se_p(v1), tol=1e-12)
    rec("Q5b", "P(Q1&Q2) p=%.2f" % pf, vg, float(PG.subs(p, pf)), float(g.mean()), se_p(vg), tol=1e-12)
    vc = pf / (2 - pf)
    rec("Q5c", "P(all|G) p=%.2f" % pf, vc, float((P_all / PG).subs(p, pf)), float((A & B & C & D)[g].mean()), se_p(vc, int(g.sum())), tol=1e-12)

# ============================================================ Q6  (two rolls of an N-sided die)
for n in (2, 3, 6, 10):
    r1 = rng.integers(1, n + 1, N)
    r2 = rng.integers(1, n + 1, N)
    mn = np.minimum(r1, r2)
    mx = np.maximum(r1, r2)
    joint = {}
    for a, b in itertools.product(range(1, n + 1), repeat=2):
        key = (min(a, b), max(a, b))
        joint[key] = joint.get(key, Fr(0)) + Fr(1, n * n)
    for k, l in ((1, 1), (1, n), (2, n), (n, n)):
        off = Fr(1, n * n) if k == l else Fr(2, n * n)
        rec("Q6a", "N=%d P(min=%d,max=%d)" % (n, k, l), off, joint.get((k, l), Fr(0)), float(((mn == k) & (mx == l)).mean()), se_p(float(off)), tol=0)
    rows.append(("Q6a", "N=%d P(min=k,max=l)=0 for k>l" % n, all(joint.get((k, l), 0) == 0 for k in range(1, n + 1) for l in range(1, k)), True, ""))
    for k in range(1, n + 1):
        off = Fr(1 + 2 * (n - k), n * n)
        rec("Q6b", "N=%d P(min=%d)" % (n, k), off, sum(v for (a, b), v in joint.items() if a == k), float((mn == k).mean()), se_p(float(off)), tol=0)
        off = Fr(1 + 2 * (k - 1), n * n)
        rec("Q6c", "N=%d P(max=%d)" % (n, k), off, sum(v for (a, b), v in joint.items() if b == k), float((mx == k).mean()), se_p(float(off)), tol=0)
    if n >= 2:
        prod = Fr(1 + 2 * (n - 2), n * n) * Fr(1, n * n)
        rec("Q6d", "N=%d P(min=2,max=1)=0 != product" % n, 0, joint.get((2, 1), Fr(0)), float(((mn == 2) & (mx == 1)).mean()), 1e-9, tol=0)
        rows.append(("Q6d", "N=%d product %s > 0 => dependent" % (n, prod), prod > 0, True, ""))

bad = [r for r in rows if not (r[2] and r[3])]
for item, what, ex, mc, det in rows:
    print("%-5s ex=%-4s mc=%-4s %s | %s" % (item, "ok" if ex else "FAIL", "ok" if mc else "FAIL", what, det))
print()
print("TOTAL checks: %d, failing: %d" % (len(rows), len(bad)))
for r in bad:
    print("  FAIL:", r[0], r[1], r[4])
sys.exit(1 if bad else 0)
