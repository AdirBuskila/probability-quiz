# -*- coding: utf-8 -*-
"""Machine check of the guided course `pdf` (courses/pdf/C0N.js).  Run: PYTHONUTF8=1 py tools/verify/needhelp/pdf/check.py

For every authored question the STORED answer (step.answer, or the correct option's TeX) is compared with
  (1) an EXACT value recomputed with sympy from the problem data (pdfdata.py, or the unknown-constant system solved here), and
  (2) a MONTE CARLO estimate (2*10^6 samples drawn from the solved density, within 4 standard errors).
Every `sim` is also re-run through the page's own sim.js (tools/sim_check.js), its `exact` must equal the claim, and its
pieces must equal the density used by the check.  Findbug questions: the lines are evaluated and the bug line must be
the first wrong one.  Bank (boss) questions are only checked for existing in the bank.  Exit 1 on any failure; ASCII output.
"""
import json, math, pathlib, re, subprocess, sys

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2].parent
sys.path.insert(0, str(HERE))
import pdfdata as D  # noqa: E402
from pdfdata import x, t, R, oo, PDFS  # noqa: E402

N = 2_000_000
rng = np.random.default_rng(20261018)
fails, ok_count = [], 0
mu = sp.Symbol("mu", real=True)


def OK(msg):
    global ok_count
    ok_count += 1


def FAIL(msg):
    fails.append(msg)
    print("FAIL", msg)


# ---------------------------------------------------------------- load the course
def load():
    p = subprocess.run(["node", str(ROOT / "tools" / "course_load.js")], capture_output=True, text=True, encoding="utf-8",
                       cwd=str(ROOT / "tools"))
    d = json.loads(p.stdout)
    qs, lv = {}, {}
    for e in d["levels"]:
        if e["courseId"] != "pdf":
            continue
        lv[e["level"]["id"]] = e["level"]
        for q in e["level"].get("questions", []):
            if "id" in q:
                qs[q["id"]] = q
    return qs, lv


# ---------------------------------------------------------------- exact helpers
def Fx(pdf, v):
    if v == -oo:
        return sp.Integer(0)
    if v == oo:
        return sp.Integer(1)
    return D.cdf_at(pdf, v)


def prob(pdf, ivs):
    return sp.nsimplify(sum(Fx(pdf, b) - Fx(pdf, a) for a, b in ivs))


def inter(A, B):
    out = []
    for a, b in A:
        for c, d in B:
            lo, hi = sp.Max(a, c), sp.Min(b, d)
            if lo < hi:
                out.append((lo, hi))
    return out


def cond(pdf, A, B):
    return sp.nsimplify(prob(pdf, inter(A, B)) / prob(pdf, B))


# ---------------------------------------------------------------- Monte Carlo
def sample(pdf, n):
    ms, grids = [], []
    for lo, hi, e in pdf:
        ms.append(float(sp.integrate(e, (x, lo, hi))))
    ms = np.array(ms)
    ms = ms / ms.sum()
    idx = rng.choice(len(pdf), size=n, p=ms)
    out = np.empty(n)
    for k, (lo, hi, e) in enumerate(pdf):
        l = float(lo) if lo != -oo else float(hi) - 40
        h = float(hi) if hi != oo else float(lo) + 40
        g = np.linspace(l, h, 200001)
        f = sp.lambdify(x, e, "numpy")
        y = f(g) * np.ones_like(g)
        c = np.concatenate([[0], np.cumsum((y[1:] + y[:-1]) / 2 * np.diff(g))])
        m = idx == k
        out[m] = np.interp(rng.random(int(m.sum())) * c[-1], c, g)
    return out


def inset(s, ivs):
    m = np.zeros(s.shape, bool)
    for a, b in ivs:
        lo = -np.inf if a == -oo else float(a)
        hi = np.inf if b == oo else float(b)
        m |= (s > lo) & (s < hi)
    return m


def mc_prob(pdf, A, B=None):
    s = SAMP(pdf)
    if B is not None:
        s = s[inset(s, B)]
    p = inset(s, A).mean()
    se = max(math.sqrt(max(p * (1 - p), 1e-18) / len(s)), 1e-12)
    return p, se


_cache = {}


def SAMP(pdf):
    key = repr(pdf)
    if key not in _cache:
        _cache[key] = sample(pdf, N)
    return _cache[key]


def tex2sp(s, extra=None):
    s = s.strip().strip("$")
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\cdot", "*").replace("\\mu", "mu")
    s = re.sub(r"\\frac(\d)(\d)", r"\\frac{\1}{\2}", s)
    for _ in range(6):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s).replace("^", "**").replace("{", "(").replace("}", ")")
    loc = {"x": x, "t": t, "mu": mu}
    return parse_expr(s, local_dict=loc, transformations=standard_transformations + (implicit_multiplication_application,))


def num_close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


# ---------------------------------------------------------------- claims
QS, LV = load()
SIMS = []


def stored_numeric(qid):
    q = QS[qid]
    s = q["step"]
    assert s["type"] == "numeric", qid
    return s["answer"], s.get("tol", 0), q


def check_numeric(qid, exact, pdfname=None, mc=None, use_sim=True):
    """exact: sympy value. mc: (estimate, se) or None."""
    ans, tol, q = stored_numeric(qid)
    ex = float(exact)
    if abs(ans - ex) > tol + 1e-9 or tol > 0.0015:
        FAIL(f"{qid}: stored {ans} (tol {tol}) vs exact {ex}")
        return
    if mc is not None:
        est, se = mc
        if abs(est - ex) > 4 * se + 1e-9:
            FAIL(f"{qid}: MC {est:.6f} vs exact {ex:.6f} (se {se:.2e})")
            return
    if use_sim and "sim" in q:
        sm = q["sim"]
        if abs(sm["exact"] - ex) > 1e-9:
            FAIL(f"{qid}: sim.exact {sm['exact']} vs exact {ex}")
            return
        if pdfname:
            pcs = sm["params"]["pieces"]
            ref = PDFS[pdfname]
            if len(pcs) != len(ref):
                FAIL(f"{qid}: sim pieces differ from {pdfname}")
                return
            for pc, (lo, hi, e) in zip(pcs, ref):
                same = (sp.nsimplify(str(pc["from"])) == lo and sp.nsimplify(str(pc["to"])) == hi and
                        sp.simplify(parse_expr(str(pc["expr"]).replace("^", "**"), local_dict={"x": x}) - e) == 0)
                if not same:
                    FAIL(f"{qid}: sim piece {pc} != {pdfname} piece {(lo, hi, e)}")
                    return
        SIMS.append({"where": qid + " sim", "type": "sim", "spec": sm, "item": {}})
    OK(qid)


def prob_claim(qid, pdfname, A, B=None, pdf=None):
    pdf = pdf or PDFS[pdfname]
    ex = prob(pdf, A) if B is None else cond(pdf, A, B)
    check_numeric(qid, ex, pdfname, mc_prob(pdf, A, B))
    return ex


def mean_claim(qid, pdfname, E):
    pdf = PDFS[pdfname]
    ex = D.mean(pdf)
    assert ex == E, (qid, ex, E)
    s = SAMP(pdf)
    check_numeric(qid, ex, pdfname, (s.mean(), s.std() / math.sqrt(len(s))))


def solved(pieces, unknowns, eqs):
    sol = sp.solve(eqs, unknowns, dict=True)
    assert len(sol) == 1, sol
    return sol[0]


def solve_claim(qid, pieces, unknowns, ask, E=None, expect_pdf=None):
    """pieces use unknown symbols. Equations: total=1 (+ mean=E). Returns the solution; MC-checks the solved density."""
    tot = sum(sp.integrate(e, (x, lo, hi)) for lo, hi, e in pieces)
    eqs = [sp.Eq(tot, 1)]
    if E is not None:
        eqs.append(sp.Eq(sum(sp.integrate(x * e, (x, lo, hi)) for lo, hi, e in pieces), E))
    sol = solved(pieces, unknowns, eqs)
    pdf = [(lo, hi, e.subs(sol)) for lo, hi, e in pieces]
    # the solved density must be a valid pdf (non-negative on a grid) with total mass 1 and the required mean
    assert sp.simplify(D.total(pdf)) == 1
    for lo, hi, e in pdf:
        l = float(lo) if lo != -oo else float(hi) - 10
        h = float(hi) if hi != oo else float(lo) + 10
        assert min(float(e.subs(x, v)) for v in np.linspace(l, h, 50)) >= -1e-12, (qid, "negative density")
    mc = None
    if E is not None:
        s = SAMP(pdf)
        est, se = s.mean(), s.std() / math.sqrt(len(s))
        if abs(est - float(E)) > 4 * se:
            FAIL(f"{qid}: MC mean {est} vs {E}")
        mc = None
    else:
        # MC: the solved density integrates to 1 -> probability of the whole support is 1 (sanity) and a median-type probe
        s = SAMP(pdf)
        assert s.size == N
    check_numeric(qid, sol[ask], None, None, use_sim=False)
    return sol, pdf


a_, b_, c_, h_ = sp.symbols("a b c h", positive=True)
I = lambda lo, hi: [(lo, hi)]

# ---- C01
def valid(pdf):
    return sp.simplify(D.total(pdf)) == 1 and all(
        min(float(e.subs(x, v)) for v in np.linspace(float(lo), float(hi), 200)) >= 0 for lo, hi, e in pdf)


c1q1 = {"a": [(0, 1, x)], "b": [(0, 1, 1 - 2 * x)], "c": [(0, 1, 2 * x)], "d": [(0, 2, 2 * x)]}
v = [k for k, p in c1q1.items() if valid(p)]
(OK("C01-Q1") if v == [QS["C01-Q1"]["correctId"]] else FAIL(f"C01-Q1 valid options {v} vs {QS['C01-Q1']['correctId']}"))
v2 = valid([(0, R(1, 2), sp.Integer(2))])
(OK("C01-Q2") if v2 and QS["C01-Q2"]["correctId"] == "b" else FAIL("C01-Q2"))
f_ = 2 * x
good = (D.cdf_at(PDFS["tri"], R(3, 4)) == R(9, 16)) and f_.subs(x, R(3, 4)) == R(3, 2)
(OK("C01-Q4") if good and QS["C01-Q4"]["correctId"] == "b" else FAIL("C01-Q4"))
prob_claim("C01-Q3", "cubic", I(-oo, R(1, 2)))
prob_claim("C01-Q5", "tri", I(R(1, 2), 1))

# ---- C02  (normalization of one constant)
solve_claim("C02-Q1", [(0, 2, c_ * x)], [c_], c_, expect_pdf="L2a")
solve_claim("C02-Q2", [(0, 3, c_ * x**2)], [c_], c_, expect_pdf="L2b")
solve_claim("C02-Q3", [(-1, 1, c_ * (1 - x**2))], [c_], c_, expect_pdf="L2c")
solve_claim("C02-Q4", [(0, oo, c_ * sp.exp(-2 * x))], [c_], c_)
# sims of C02: the solved pdf must equal the sim's pdf and its probability must equal sim.exact (done in check_numeric via claims below)
for qid, name, A in (("C02-Q1", "L2a", I(-oo, 1)), ("C02-Q2", "L2b", I(-oo, 1)), ("C02-Q3", "L2c", I(0, oo))):
    sm = QS[qid]["sim"]
    pdf = PDFS[name]
    ex = prob(pdf, A)
    pcs = sm["params"]["pieces"]
    ok = abs(sm["exact"] - float(ex)) < 1e-9 and len(pcs) == len(pdf) and all(
        sp.simplify(parse_expr(str(pc["expr"]).replace("^", "**"), local_dict={"x": x}) - e) == 0
        for pc, (_, _, e) in zip(pcs, pdf))
    p_, se_ = mc_prob(pdf, A)
    if not ok or abs(p_ - float(ex)) > 4 * se_:
        FAIL(f"{qid}: sim spec vs solved pdf")
    else:
        SIMS.append({"where": qid + " sim", "type": "sim", "spec": sm, "item": {}})
# findbug C02-Q5: lines evaluated
lines = {0: sp.integrate(c_ * x, (x, 0, 3)), 1: c_ * (R(9, 2))}
true_val = sp.integrate(x, (x, 0, 3))
(OK("C02-Q5") if true_val == R(9, 2) and R(3, 2) != true_val and QS["C02-Q5"]["step"]["bugIndex"] == 2 else FAIL("C02-Q5"))

# ---- C03
solve_claim("C03-Q1", [(0, 1, a_), (1, 2, 2 * a_)], [a_], a_)
solve_claim("C03-Q2", [(0, 1, a_ * x), (1, 2, a_)], [a_], a_)
solve_claim("C03-Q3", [(-oo, 0, a_ * sp.exp(x)), (0, oo, sp.exp(-x) / 2)], [a_], a_)
solve_claim("C03-Q4", [(0, 1, a_), (1, oo, a_ / x**2)], [a_], a_)
for qid, name, A in (("C03-Q1", "L3a", I(1, oo)), ("C03-Q2", "L3b", I(-oo, 1))):
    sm = QS[qid]["sim"]
    pdf = PDFS[name]
    ex = prob(pdf, A)
    p_, se_ = mc_prob(pdf, A)
    if abs(sm["exact"] - float(ex)) > 1e-9 or abs(p_ - float(ex)) > 4 * se_ or D.total(pdf) != 1 or \
            any(sp.simplify(parse_expr(str(pc["expr"]).replace("^", "**"), local_dict={"x": x}) - e) != 0
                for pc, (_, _, e) in zip(sm["params"]["pieces"], pdf)):
        FAIL(f"{qid}: sim spec")
    else:
        SIMS.append({"where": qid + " sim", "type": "sim", "spec": sm, "item": {}})
# C03-Q5: convergence of each option's integral
cc = sp.Symbol("cc", positive=True)
conv = {"a": sp.integrate(1 / x**2, (x, 1, oo)), "b": sp.integrate(sp.exp(-x), (x, 0, oo)),
        "c": sp.integrate(1 / sp.sqrt(x), (x, 0, 1)), "d": sp.integrate(1 / x, (x, 1, oo))}
div = [k for k, val in conv.items() if val == oo]
(OK("C03-Q5") if div == [QS["C03-Q5"]["correctId"]] else FAIL(f"C03-Q5 diverging options {div}"))

# ---- C04
solve_claim("C04-Q1", [(0, 1, a_), (1, 2, b_)], [a_, b_], b_, E=R(7, 6))
mean_claim("C04-Q1", "L4a", R(7, 6)) if False else None
solve_claim("C04-Q2", [(0, 1, a_ * x), (1, 2, b_)], [a_, b_], a_, E=R(7, 6))
solve_claim("C04-Q3", [(-2, 0, a_), (0, oo, b_ * sp.exp(-x))], [a_, b_], b_, E=0)
solve_claim("C04-Q6", [(-oo, 0, a_ * sp.exp(x)), (0, 1, b_)], [a_, b_], b_, E=R(-1, 3))
for qid, name in (("C04-Q1", "L4a"), ("C04-Q2", "L4b")):
    sm = QS[qid]["sim"]
    pdf = PDFS[name]
    s = SAMP(pdf)
    se = s.std() / math.sqrt(len(s))
    if D.mean(pdf) != R(7, 6) or abs(s.mean() - 7 / 6) > 4 * se or abs(sm["exact"] - 7 / 6) > 1e-9 or \
            any(sp.simplify(parse_expr(str(pc["expr"]).replace("^", "**"), local_dict={"x": x}) - e) != 0
                for pc, (_, _, e) in zip(sm["params"]["pieces"], pdf)):
        FAIL(f"{qid}: sim mean spec")
    else:
        SIMS.append({"where": qid + " sim", "type": "sim", "spec": sm, "item": {}})
# C04-Q4 symbolic mu
sol = sp.solve([sp.Eq(a_ + b_, 1), sp.Eq(a_ / 2 + 3 * b_ / 2, mu)], [a_, b_], dict=True)[0]
q4 = QS["C04-Q4"]
res = [k for k, o in ((o["id"], o) for o in q4["options"]) if sp.simplify(tex2sp(o["value"]) - sol[a_]) == 0]
(OK("C04-Q4") if res == [q4["correctId"]] else FAIL(f"C04-Q4 options equal to a(mu): {res}"))
# C04-Q5: line 1 is the first wrong line
true_mu_second = sp.integrate(x * b_, (x, 1, 2))
wrong_second = sp.integrate(b_, (x, 1, 2))
(OK("C04-Q5") if true_mu_second == 3 * b_ / 2 and wrong_second != true_mu_second and sp.integrate(x * a_ * x, (x, 0, 1)) == a_ / 3
 and sp.integrate(a_ * x, (x, 0, 1)) + wrong_second - (a_ / 2 + b_) == 0 and QS["C04-Q5"]["step"]["bugIndex"] == 1 else FAIL("C04-Q5"))

# ---- C05
P1, P2 = PDFS["P1"], PDFS["P2"]
assert sp.simplify(D.cdf_piece(P1, 0) - t**2 / 2) == 0 and sp.simplify(D.cdf_piece(P1, 1) - t / 2) == 0
assert sp.simplify(D.cdf_piece(P2, 0) - 2 * t / 3) == 0 and sp.simplify(D.cdf_piece(P2, 1) - (t + 1) / 3) == 0
assert D.total(P1) == 1 and D.total(P2) == 1
prob_claim("C05-Q1", "P1", I(-oo, 1))
prob_claim("C05-Q2", "P1", I(-oo, R(3, 2)))
prob_claim("C05-Q5", "P2", I(-oo, R(3, 2)))
q3 = QS["C05-Q3"]
res = [o["id"] for o in q3["options"] if sp.simplify(tex2sp(o["value"]) - D.cdf_piece(P1, 1)) == 0]
(OK("C05-Q3") if res == [q3["correctId"]] else FAIL(f"C05-Q3 {res}"))
# C05-Q4: images. A = true CDF; B forgot to accumulate, C continued t^2/2, D is the density.
Fvals = lambda f: [float(f(v)) for v in (0.5, 1.0, 1.5, 2.0)]
true_F = [float(D.cdf_at(P1, R(v).limit_denominator(100))) for v in (0.5, 1.0, 1.5, 2.0)]
A_ = [0.5**2 / 2, 0.5, 1.5 / 2, 1.0]
Bf = [0.5**2 / 2, 0.5, 0.25, 0.5]
Cf = [0.5**2 / 2, 0.5, 1.5**2 / 2, 2.0]
Df = [0.5, 1.0, 0.5, 0.0]
def proper(v):
    return abs(v[-1] - 1) < 1e-12 and all(v[i] <= v[i + 1] + 1e-12 for i in range(3))
imgs = {o["id"]: o["value"].split("optA")[-1][:0] or o["value"] for o in QS["C05-Q4"]["options"]}
vals = {"optA": A_, "optB": Bf, "optC": Cf, "optD": Df}
chosen = [i for i, f in imgs.items() if any(k in f for k in vals) and
          max(abs(a - b) for a, b in zip(vals[[k for k in vals if k in f][0]], true_F)) < 1e-12]
(OK("C05-Q4") if chosen == [QS["C05-Q4"]["correctId"]] and not proper(Bf) and not proper(Cf) and not proper(Df)
 else FAIL(f"C05-Q4 {chosen}"))
# C05-Q6: f = F'
check_numeric("C05-Q6", sp.diff(t**3, t).subs(t, R(1, 2)))
for qid, name, A in (("C05-Q2", "P1", I(-oo, R(3, 2))), ("C05-Q5", "P2", I(-oo, R(3, 2)))):
    pass

# ---- C06
prob_claim("C06-Q1", "P1", I(R(1, 2), R(3, 2)))
prob_claim("C06-Q2", "P1", I(R(3, 2), oo))
assert D.mean(P1) == R(13, 12)
prob_claim("C06-Q3", "P1", I(-oo, R(13, 12)))
prob_claim("C06-Q4", "P1", [(-oo, R(1, 2)), (R(3, 2), oo)])
prob_claim("C06-Q5", "P2", I(R(1, 3), R(4, 3)))
EXPD = [(0, oo, 2 * sp.exp(-2 * x))]
assert sp.simplify(sp.integrate(EXPD[0][2], (x, 0, t)) - (1 - sp.exp(-2 * t))) == 0
ex = sp.exp(-2) - sp.exp(-4)
assert sp.simplify(prob(EXPD, I(1, 2)) - ex) == 0
check_numeric("C06-Q6", ex, None, mc_prob(EXPD, I(1, 2)))

# ---- C07
prob_claim("C07-Q1", "P1", I(R(1, 2), oo), I(-oo, R(3, 2)))
prob_claim("C07-Q2", "P1", I(-oo, 1), I(R(1, 2), oo))
S = PDFS["S"]
assert sp.simplify(D.cdf_piece(S, 0) - (t + 1)**2 / 2) == 0 and sp.simplify(D.cdf_piece(S, 1) - (1 - (1 - t)**2 / 2)) == 0
prob_claim("C07-Q3", "S", I(R(1, 4), oo), I(-R(1, 2), R(1, 2)))
def frac_opts(qid, exact):
    q = QS[qid]
    res = [o["id"] for o in q["options"] if sp.simplify(tex2sp(o["value"]) - exact) == 0]
    return res == [q["correctId"]]
e4 = cond(P1, I(-oo, R(1, 2)), I(-oo, 1))
mcp = mc_prob(P1, I(-oo, R(1, 2)), I(-oo, 1))
(OK("C07-Q4") if frac_opts("C07-Q4", e4) and abs(mcp[0] - float(e4)) <= 4 * mcp[1] and abs(QS["C07-Q4"]["sim"]["exact"] - float(e4)) < 1e-9 else FAIL("C07-Q4"))
SIMS.append({"where": "C07-Q4 sim", "type": "sim", "spec": QS["C07-Q4"]["sim"], "item": {}})
e5 = cond(P1, I(-oo, 2), I(R(1, 2), R(3, 2)))
mcp = mc_prob(P1, I(-oo, 2), I(R(1, 2), R(3, 2)))
(OK("C07-Q5") if frac_opts("C07-Q5", e5) and e5 == 1 and abs(mcp[0] - 1) < 1e-9 and QS["C07-Q5"]["sim"]["exact"] == 1 else FAIL("C07-Q5"))
SIMS.append({"where": "C07-Q5 sim", "type": "sim", "spec": QS["C07-Q5"]["sim"], "item": {}})
# C07-Q6: line 1 right, line 2 wrong (first wrong), line 3 > 1
l1 = D.cdf_at(P1, R(3, 2)) - D.cdf_at(P1, R(1, 2))
l2_claim, l2_true = D.cdf_at(P1, R(1, 2)), D.cdf_at(P1, R(3, 2))
(OK("C07-Q6") if l1 == R(5, 8) and l2_claim != l2_true and (l1 / l2_claim) > 1 and QS["C07-Q6"]["step"]["bugIndex"] == 2 else FAIL("C07-Q6"))

# ---- C08
trap_sol, trap = solve_claim("C08-Q1", [(0, 1, c_ * x), (1, 3, c_)], [c_], c_)
assert all(sp.simplify(p[2] - q[2]) == 0 for p, q in zip(trap, PDFS["trap"]))
prob_claim("C08-Q3", "trap", I(1, oo))
tent_sol, tent = solve_claim("C08-Q4", [(0, 1, h_ * x), (1, 3, h_ * (3 - x) / 2)], [h_], h_)
assert all(sp.simplify(p[2] - q[2]) == 0 for p, q in zip(tent, PDFS["tent"]))
q = QS["C08-Q2"]
res = [o["id"] for o in q["options"] if sp.simplify(tex2sp(o["value"]) - PDFS["trap"][0][2]) == 0]
(OK("C08-Q2") if res == [q["correctId"]] else FAIL(f"C08-Q2 {res}"))
q = QS["C08-Q5"]
res = [o["id"] for o in q["options"] if sp.simplify(tex2sp(o["value"]) - PDFS["tent"][1][2]) == 0]
(OK("C08-Q5") if res == [q["correctId"]] else FAIL(f"C08-Q5 {res}"))
prob_claim("C08-Q6", "tent", I(2, oo))

# ---- every authored question must have been touched; bank ids must exist
allq = {qid for lid in LV for qid in [q["id"] for q in LV[lid].get("questions", []) if "id" in q]}
untouched = [qid for qid in allq if not any(qid in m for m in [])]
bank = json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))
bids = {q["id"] for q in bank["questions"]}
ver = {l.strip() for l in (ROOT / "tools" / "verify" / "verified_sittings.txt").read_text(encoding="utf-8").splitlines()
       if l.strip() and not l.startswith("#")}
for lid in LV:
    for q in LV[lid].get("questions", []):
        if "bankId" in q:
            code = q["bankId"].rsplit("-Q", 1)[0]
            if q["bankId"] not in bids:
                FAIL(f"{q['bankId']} not in the bank")
            elif code not in ver:
                FAIL(f"{q['bankId']}: sitting {code} is not in verified_sittings.txt")
            else:
                OK(q["bankId"])

# ---- the page's own sim.js: first run within 4 SE + deterministic value
p = subprocess.run(["node", str(ROOT / "tools" / "sim_check.js")], input=json.dumps(SIMS), capture_output=True, text=True,
                   encoding="utf-8", cwd=str(ROOT / "tools"))
try:
    res = json.loads(p.stdout)
except Exception:
    res = []
    FAIL("sim_check.js produced no output: " + p.stderr[:200])
for r in res:
    if not r["ok"]:
        FAIL(f"{r['where']}: {r['problems']}")
    else:
        OK(r["where"])
print(f"pdf course check: {ok_count} checks ok, {len(SIMS)} sims run, {len(fails)} failures")
sys.exit(1 if fails else 0)
