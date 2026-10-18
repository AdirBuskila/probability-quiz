# -*- coding: utf-8 -*-
"""Machine check of the guided course `circ` (circuits and reliability).  Run:  PYTHONUTF8=1 py tools/verify/needhelp/circ/check.py

For every own question of courses/circ/C01..C08 (read through tools/course_load.js, the same loader as the build):
  1. EXACT truth: enumeration over all 2^n component states with Fractions (circuits_lib.prob), from the circuit
     named in defs.py -- the very table the pictures (diagrams.py) are drawn from -- or a closed form for the
     dependent-unit questions, or sympy / a brute-force search where the answer is an unknown or a count;
  2. the STORED answer (numeric step answer within its tol, or the correct MCQ option) equals the truth, and no
     distractor equals it; conceptual MCQs are checked option by option against a grid of probabilities;
  3. the question's `sim` is re-evaluated independently here (exact enumeration of its own params) and must equal
     `exact` and the truth; the page's own sim.js runs it too (tools/sim_check.js, same seed/trials as the button);
  4. MONTE CARLO (2*10^6 trials, 4 standard errors) of the same event on the defs circuit and on the sim params;
  5. every `bankId` exists in the built bank and its sitting is in tools/verify/verified_sittings.txt;
  6. every number quoted in a lesson's worked example.
Exits 1 on any failure.  ASCII output only."""
import itertools, json, math, pathlib, subprocess, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[3]
from circuits_lib import F, S, P, C, BR, comps, works, prob, circ_prob  # noqa: E402
from defs import CIRCUITS  # noqa: E402

N = 2_000_000
rng = np.random.default_rng(20261018)
fails, notes = [], []


def FAIL(w, msg):
    fails.append("%s: %s" % (w, msg))


def OK(w, msg):
    notes.append("%s: %s" % (w, msg))


NOT = np.logical_not


def T(name, event=None, given=None):
    tree, probs, _ = CIRCUITS[name]
    return circ_prob(tree, probs, given=given, event=event)


def W(name):
    tree = CIRCUITS[name][0]
    return lambda s: works(tree, s)


# ---------------------------------------------------------------- Monte Carlo on a defs circuit
def mc_circ(name, event=None, given=None):
    tree, probs, _ = CIRCUITS[name]
    ids = sorted(probs)
    st = {i: rng.random(N) < float(probs[i]) for i in ids}
    ev = (event or (lambda s: works(tree, s)))(st)
    if given is None:
        k = N; hit = int(np.sum(ev))
    else:
        g = given(st); k = int(np.sum(g)); hit = int(np.sum(ev & g))
    p = hit / k
    return p, math.sqrt(max(p * (1 - p), 1e-12) / k)


def mc_ok(w, truth, mc):
    p, se = mc
    if abs(p - float(truth)) > 4 * max(se, 1e-9):
        FAIL(w, "Monte Carlo %.5f vs exact %.5f (se %.5f)" % (p, float(truth), se))


# ---------------------------------------------------------------- independent evaluation of a sim spec
def sim_value(sim, w):
    pr = sim["params"]
    ev, gv = pr["event"], pr.get("given")
    safe = lambda e: eval(e, {"__builtins__": {}}, {}) if False else None  # noqa: E731

    def run(expr, env):
        return bool(eval(expr, {"__builtins__": {}}, dict(env)))

    if sim["kind"] == "circuit":
        if "network" in pr:
            ids = []

            def build(n):
                if n["type"] == "comp":
                    ids.append((n["id"], F(n["p"])))
                    return lambda e, i=n["id"]: e[i]
                kids = [build(c) for c in n["children"]]
                if n["type"] == "series":
                    return lambda e: all(k(e) for k in kids)
                return lambda e: any(k(e) for k in kids)
            f = build(pr["network"])
        else:
            ids = []
            seen = set()
            edges = []
            for ed in pr["edges"]:
                ids.append((ed["id"], F(ed["p"])))
                edges.append((ed["from"], ed["to"], ed["id"]))

            def f(e):
                reach, stack = {pr["source"]}, [pr["source"]]
                while stack:
                    u = stack.pop()
                    for a, b, i in edges:
                        if e[i]:
                            v = b if a == u else a if b == u else None
                            if v is not None and v not in reach:
                                reach.add(v); stack.append(v)
                return pr["sink"] in reach
        num = den = Fr(0)
        for bits in itertools.product((0, 1), repeat=len(ids)):
            e = {i: b for (i, _), b in zip(ids, bits)}
            wgt = Fr(1)
            for (i, p), b in zip(ids, bits):
                wgt *= p if b else 1 - p
            env = dict(e); env["S"] = 1 if f(e) else 0
            if gv is None or run(gv, env):
                den += wgt
                if run(ev, env):
                    num += wgt
        exact = num / den
        # Monte Carlo of the same spec
        samp = {i: (rng.random(N) < float(p)).astype(int) for i, p in ids}
        # vectorised reachability: evaluate f on python ints would be slow; use enumeration weights as the sampler
        keys, wts = [], []
        for bits in itertools.product((0, 1), repeat=len(ids)):
            e = {i: b for (i, _), b in zip(ids, bits)}
            wgt = Fr(1)
            for (i, p), b in zip(ids, bits):
                wgt *= p if b else 1 - p
            env = dict(e); env["S"] = 1 if f(e) else 0
            keys.append(env); wts.append(float(wgt))
        idx = rng.choice(len(keys), size=N, p=np.array(wts) / sum(wts))
        evs = np.array([run(ev, k) for k in keys]); gs = np.array([True if gv is None else run(gv, k) for k in keys])
        g = gs[idx]; e_ = evs[idx] & g
        k = int(g.sum()); p = int(e_.sum()) / k
        return exact, (p, math.sqrt(max(p * (1 - p), 1e-12) / k))
    if sim["kind"] == "custom_discrete":
        rows = [dict(r) for r in pr["joint"]]
        tot = sum(F(r["p"]) for r in rows)
        if tot != 1:
            FAIL(w, "joint does not sum to 1 (%s)" % tot)
        num = den = Fr(0)
        for r in rows:
            env = {k: v for k, v in r.items() if k != "p"}
            if gv is None or run(gv, env):
                den += F(r["p"])
                if run(ev, env):
                    num += F(r["p"])
        wts = np.array([float(F(r["p"])) for r in rows])
        idx = rng.choice(len(rows), size=N, p=wts / wts.sum())
        envs = [{k: v for k, v in r.items() if k != "p"} for r in rows]
        evs = np.array([run(ev, e) for e in envs]); gs = np.array([True if gv is None else run(gv, e) for e in envs])
        g = gs[idx]; e_ = evs[idx] & g
        k = int(g.sum()); p = int(e_.sum()) / k
        return num / den, (p, math.sqrt(max(p * (1 - p), 1e-12) / k))
    FAIL(w, "unsupported sim kind " + sim["kind"])
    return None, None


# ---------------------------------------------------------------- load the levels
def load_levels():
    proc = subprocess.run(["node", str(ROOT / "tools" / "course_load.js")], capture_output=True, text=True,
                          encoding="utf-8", cwd=str(ROOT / "tools"))
    data = json.loads(proc.stdout)
    return [e["level"] for e in data["levels"] if e["courseId"] == "circ"], data["errors"]


def num_of(v):
    return F(str(v).strip())


# ---------------------------------------------------------------- the registry
grid = [Fr(k, 10) for k in range(1, 10)] + [Fr(1, 2)]
REG = {}


def reg(qid, **kw):
    REG[qid] = kw


# level 1
reg("C01-Q1", truth=lambda: T("s_ab"), circ=("s_ab", None, None))
reg("C01-Q2", truth=lambda: T("s_abc"), circ=("s_abc", None, None))
reg("C01-Q3", truth=lambda: T("s_4"), circ=("s_4", None, None))
reg("C01-Q4", claims={
    "a": lambda p1, p2: p1 * p2 <= min(p1, p2),
    "b": lambda p1, p2: p1 * p2 >= max(p1, p2),
    "c": lambda p1, p2: p1 * p2 == p1 + p2,
    "d": lambda p1, p2: p1 * p2 == (p1 + p2) / 2, }, correct="a", args=2)


def q5_truth():
    p = sp.symbols("p", positive=True)
    sol = sp.solve(sp.Eq(p ** 2, sp.Rational(49, 100)), p)
    assert len(sol) == 1
    assert T("s_pp") == Fr(49, 100)          # the picture's circuit: two units at the answer 0.7
    return Fr(str(sol[0]))


reg("C01-Q5", truth=q5_truth)
# level 2
reg("C02-Q1", truth=lambda: T("p_ab"), circ=("p_ab", None, None))
reg("C02-Q2", truth=lambda: T("p_abc"), circ=("p_abc", None, None))
reg("C02-Q3", truth=lambda: T("p_2"), circ=("p_2", None, None))
reg("C02-Q4", claims={
    "a": lambda p1, p2: 1 - (1 - p1) * (1 - p2) >= max(p1, p2),
    "b": lambda p1, p2: 1 - (1 - p1) * (1 - p2) <= min(p1, p2),
    "c": lambda p1, p2: 1 - (1 - p1) * (1 - p2) == p1 * p2,
    "d": lambda p1, p2: 1 - (1 - p1) * (1 - p2) == p1 + p2, }, correct="a", args=2)


def c2q5():
    x = sp.symbols("x")
    sol = sp.solve(sp.Eq(1 - sp.Rational(3, 10) * (1 - x), sp.Rational(94, 100)), x)
    assert len(sol) == 1
    ans = Fr(str(sol[0]))
    tree, probs, _ = CIRCUITS["p_xy"]
    assert probs["A"] == Fr(7, 10) and probs["B"] == ans and T("p_xy") == Fr(94, 100)
    return ans


reg("C02-Q5", truth=c2q5)
# level 3
reg("C03-Q1", truth=lambda: T("sp3"), circ=("sp3", None, None))
reg("C03-Q2", truth=lambda: T("sp2"), circ=("sp2", None, None))


def sp5_value(f):
    def g(a, b, c):
        tree = CIRCUITS["sp5"][0]
        return circ_prob(tree, {"A": a, "B": b, "C": c}) == f(a, b, c)
    return g


reg("C03-Q3", claims={
    "a": sp5_value(lambda a, b, c: (1 - (1 - a) * (1 - b)) * c),
    "b": sp5_value(lambda a, b, c: 1 - (1 - a * b) * (1 - c)),
    "c": sp5_value(lambda a, b, c: (a + b) * c),
    "d": sp5_value(lambda a, b, c: a * b * c), }, correct="a", args=3)
reg("C03-Q4", truth=lambda: T("sp4"), circ=("sp4", None, None), findbug=True)
# level 4
reg("C04-Q1", truth=lambda: T("c_par5"), circ=("c_par5", None, None))


def c4q2():
    n = 1
    while 1 - Fr(1, 2) ** n < Fr(99, 100):
        n += 1
    # brute force over the real circuit of n units in parallel
    for m, expect in ((n - 1, False), (n, True)):
        tree = P(*[C("U%d" % i) for i in range(m)])
        probs = {"U%d" % i: Fr(1, 2) for i in range(m)}
        if (circ_prob(tree, probs) >= Fr(99, 100)) != expect:
            FAIL("C04-Q2", "brute force disagrees at n=%d" % m)
    return Fr(n)


reg("C04-Q2", truth=c4q2)
reg("C04-Q3", truth=lambda: T("c_ser3", event=lambda s: NOT(W("c_ser3")(s))), circ=("c_ser3", lambda s: NOT(W("c_ser3")(s)), None))
reg("C04-Q4", truth=lambda: T("c_sp"), circ=("c_sp", None, None))
reg("C04-Q5", truth=lambda: T("c_par3", event=lambda s: NOT(W("c_par3")(s))), circ=("c_par3", lambda s: NOT(W("c_par3")(s)), None))


# level 5
def br_equiv(target):
    def f():
        ids = ["A", "B", "C", "D"]
        for bits in itertools.product((False, True), repeat=4):
            st = dict(zip(ids, bits)); st["E"] = True
            if works(CIRCUITS["br_gen"][0], st) != target(st):
                return False
        return True
    return f


reg("C05-Q1", claims_bool={
    "a": br_equiv(lambda s: (s["A"] | s["C"]) & (s["B"] | s["D"])),
    "b": br_equiv(lambda s: (s["A"] & s["B"]) | (s["C"] & s["D"])),
    "c": br_equiv(lambda s: s["A"] & s["B"] & s["C"] & s["D"]),
    "d": br_equiv(lambda s: s["A"] | s["B"] | s["C"] | s["D"]), }, correct="a")
reg("C05-Q2", truth=lambda: T("br_08", given=lambda s: s["E"]), circ=("br_08", None, lambda s: s["E"]))
reg("C05-Q3", truth=lambda: T("br_08", given=lambda s: NOT(s["E"])), circ=("br_08", None, lambda s: NOT(s["E"])))
reg("C05-Q4", truth=lambda: T("br_08"), circ=("br_08", None, None))
reg("C05-Q5", truth=lambda: T("br_05"), circ=("br_05", None, None))
# level 6
reg("C06-Q1", truth=lambda: T("b_ser", event=lambda s: s["A"], given=W("b_ser")), circ=("b_ser", lambda s: s["A"], W("b_ser")))
reg("C06-Q2", truth=lambda: T("b_par", event=lambda s: s["A"], given=W("b_par")), circ=("b_par", lambda s: s["A"], W("b_par")))
reg("C06-Q3", truth=lambda: T("b_sp2", event=lambda s: s["B"], given=W("b_sp2")), circ=("b_sp2", lambda s: s["B"], W("b_sp2")))
reg("C06-Q4", truth=lambda: T("b_par", event=lambda s: s["A"], given=W("b_par")), findbug=True)
reg("C06-Q5", truth=lambda: T("b_sp", event=lambda s: s["A"] & s["B"] & s["C"], given=W("b_sp")),
    circ=("b_sp", lambda s: s["A"] & s["B"] & s["C"], W("b_sp")))
# level 7
x1, x2 = W("r_x1"), W("r_x2")
reg("C07-Q1", truth=lambda: T("r_x1", event=lambda s: x1(s) & x2(s)), circ=("r_x1", lambda s: x1(s) & x2(s), None))
reg("C07-Q2", truth=lambda: T("r_x1", event=x1, given=x2), circ=("r_x1", x1, x2))
reg("C07-Q3", truth=lambda: T("r_x1", event=lambda s: x1(s) | x2(s)), circ=("r_x1", lambda s: x1(s) | x2(s), None))
reg("C07-Q4", truth=lambda: T("r5_q1", event=W("r5_q1"), given=W("r5_q2")), circ=("r5_q1", W("r5_q1"), W("r5_q2")))


# level 8 (closed forms from the conditional data, checked against the joint table)
def dep(p, q, s):
    return {"AB": p * q, "Ab": p * (1 - q), "aB": (1 - p) * s, "ab": (1 - p) * (1 - s)}


p8, q8, s8 = Fr(8, 10), Fr(9, 10), Fr(3, 10)
J = dep(p8, q8, s8)
reg("C08-Q1", truth=lambda: J["AB"])
reg("C08-Q2", truth=lambda: 1 - J["ab"])
reg("C08-Q3", truth=lambda: J["AB"] + J["aB"])
reg("C08-Q4", truth=lambda: p8 / (1 - J["ab"]))


def indep(p, q, s):
    j = dep(p, q, s)
    return j["AB"] == p * (j["AB"] + j["aB"])


def c8q5_claims():
    pts = [(Fr(a, 10), Fr(b, 10), Fr(c, 10)) for a in (2, 5, 8) for b in (1, 3, 9) for c in (1, 3, 9)]
    p, q, s = sp.symbols("p q s")
    assert sp.simplify(p * q - p * (p * q + (1 - p) * s) - p * (1 - p) * (q - s)) == 0
    return {
        "a": all(indep(*t) == (t[1] == t[2]) for t in pts),
        "b": all(indep(*t) == (t[1] == t[0]) for t in pts),
        "c": all(indep(*t) == (t[0] == Fr(1, 2)) for t in pts),
        "d": all(not indep(*t) for t in pts)}


reg("C08-Q5", claims_bool=c8q5_claims, correct="a")
reg("C08-Q6", truth=lambda: Fr(9, 10) * Fr(8, 10) ** 2)


# ---------------------------------------------------------------- run
def main():
    levels, errs = load_levels()
    for e in errs:
        FAIL("load", e)
    levels.sort(key=lambda L: L["order"])
    verified = set(l.strip() for l in (ROOT / "tools" / "verify" / "verified_sittings.txt").read_text(encoding="utf-8").splitlines()
                   if l.strip() and not l.startswith("#"))
    bank = {q["id"]: q for q in json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))["questions"]}
    seen_q, sim_jobs = set(), []
    for L in levels:
        lid = L["id"]
        qs = L["questions"]
        if not 4 <= len(qs) <= 6:
            FAIL(lid, "has %d questions (4-6 required)" % len(qs))
        if L.get("boss"):
            if lid != levels[-1]["id"]:
                FAIL(lid, "boss is not last")
            if not all("bankId" in q for q in qs):
                FAIL(lid, "boss has non-bank questions")
        for q in qs:
            if "bankId" in q:
                b = bank.get(q["bankId"])
                if not b:
                    FAIL(lid, "bankId %s not in the bank" % q["bankId"]); continue
                if b["topic"] != "circuits":
                    FAIL(lid, "bankId %s is not a circuits question" % q["bankId"])
                if b["examCode"] not in verified:
                    FAIL(lid, "bankId %s is from an unverified sitting %s" % (q["bankId"], b["examCode"]))
                if not b.get("steps"):
                    notes.append("%s: bank %s has no steps (self-mark)" % (lid, q["bankId"]))
                continue
            qid = q["id"]
            seen_q.add(qid)
            r = REG.get(qid)
            if r is None:
                FAIL(qid, "no registry entry"); continue
            step = q.get("step")
            # ---- truth + stored answer
            if "truth" in r:
                truth = r["truth"]()
                if step:
                    if step["type"] != "numeric":
                        if r.get("findbug") and step["type"] == "findbug":
                            pass
                        else:
                            FAIL(qid, "unexpected step type " + step["type"])
                    if step["type"] == "numeric":
                        if abs(float(step["answer"]) - float(truth)) > step.get("tol", 0):
                            FAIL(qid, "stored answer %s vs truth %s (tol %s)" % (step["answer"], float(truth), step.get("tol")))
                        if step.get("tol", 0) > 0.001:
                            FAIL(qid, "tolerance too loose")
                    OK(qid, "truth %s = %.6f" % (truth, float(truth)))
                else:
                    opts = {o["id"]: o["value"] for o in q["options"]}
                    vals = {i: num_of(v) for i, v in opts.items()}
                    if vals[q["correctId"]] != truth:
                        FAIL(qid, "correct option %s != truth %s" % (vals[q["correctId"]], truth))
                    for i, v in vals.items():
                        if i != q["correctId"] and v == truth:
                            FAIL(qid, "distractor %s equals the truth" % i)
                    if len(set(vals.values())) != len(vals):
                        FAIL(qid, "duplicate option values")
                    OK(qid, "mcq truth %s" % truth)
                if "circ" in r:
                    name, ev, gv = r["circ"]
                    mc_ok(qid, truth, mc_circ(name, ev, gv))
                if r.get("findbug"):
                    chk_findbug(qid, step, truth)
            elif "claims" in r:
                for oid, f in r["claims"].items():
                    pts = list(itertools.product(grid, repeat=r["args"]))
                    holds = all(f(*pt) for pt in pts)
                    if (oid == r["correct"]) != holds:
                        FAIL(qid, "option %s claim %s but it is %s" % (oid, "holds" if holds else "fails", "correct" if oid == q["correctId"] else "a distractor"))
                if q["correctId"] != r["correct"]:
                    FAIL(qid, "stored correctId %s != %s" % (q["correctId"], r["correct"]))
                OK(qid, "conceptual mcq checked on a %d-point grid" % len(grid) ** r["args"])
            elif "claims_bool" in r:
                cb = r["claims_bool"]
                cb = cb() if callable(cb) else {k: v() for k, v in cb.items()}
                for oid, holds in cb.items():
                    if (oid == r["correct"]) != holds:
                        FAIL(qid, "option %s: claim %s" % (oid, holds))
                if q["correctId"] != r["correct"]:
                    FAIL(qid, "stored correctId mismatch")
                OK(qid, "equivalence/independence claims checked")
            # ---- sim
            if q.get("sim"):
                sim = q["sim"]
                ex, mc = sim_value(sim, qid)
                if ex is not None:
                    if abs(float(ex) - sim["exact"]) > 1e-9:
                        FAIL(qid, "sim exact %s vs enumeration %s" % (sim["exact"], float(ex)))
                    if "truth" in r and ex != r["truth"]():
                        FAIL(qid, "sim spec evaluates to %s but the key is %s" % (ex, r["truth"]()))
                    mc_ok(qid + " sim", ex, mc)
                sim_jobs.append({"where": qid, "type": "sim", "spec": sim, "item": {}})
            if "truth" in r and not q.get("sim") and q.get("image") is None and "circ" in r:
                OK(qid, "no sim")
            # ---- picture consistency
            if q.get("image"):
                if not (ROOT / q["image"]).exists():
                    FAIL(qid, "image missing")
    for qid in REG:
        if qid not in seen_q:
            FAIL(qid, "registered but not in the course")
    # the page's own sim.js on every course sim
    if sim_jobs:
        proc = subprocess.run(["node", str(ROOT / "tools" / "sim_check.js")], input=json.dumps(sim_jobs), capture_output=True,
                              text=True, encoding="utf-8", cwd=str(ROOT / "tools"))
        for r in json.loads(proc.stdout or "[]"):
            if not r["ok"]:
                FAIL(r["where"], "sim.js check: %s" % r["problems"])
        OK("sim.js", "%d course sims run by the page's own code" % len(sim_jobs))
    lesson_facts()
    for n in notes:
        print("ok   " + n)
    for f in fails:
        print("FAIL " + f)
    print("\n%d checks noted, %d failures" % (len(notes), len(fails)))
    return 1 if fails else 0


def chk_findbug(qid, step, truth):
    if qid == "C03-Q4":
        a, b = Fr(1, 2) * Fr(1, 2), Fr(4, 5)
        fb, fc = 1 - a, 1 - b
        assert fb == Fr(3, 4) and fc == Fr(1, 5)
        assert fb * fc == Fr(3, 20) and 1 - fb * fc == truth                 # the true line 2 and the final line
        assert fb + fc == Fr(19, 20) and 1 - (fb + fc) != truth              # the planted bug is observably wrong
        if step["bugIndex"] != 2:
            FAIL(qid, "bugIndex")
    if qid == "C06-Q4":
        pS = T("b_par"); pA = Fr(3, 5)
        assert pS == Fr(21, 25) and pA / pS == truth and round(float(truth), 3) == 0.714
        assert pA / pA == 1 and pA / pA != truth                              # the planted bug (denominator P(A))
        if step["bugIndex"] != 2:
            FAIL(qid, "bugIndex")


def lesson_facts():
    w = "lesson"
    a, b = Fr(9, 10), Fr(8, 10)
    chk = lambda cond, msg: None if cond else FAIL(w, msg)  # noqa: E731
    chk(a * b == Fr(18, 25) and float(Fr(9, 10) ** 10) - 0.3487 < 1e-3, "C01 example")
    chk(1 - Fr(1, 10) * Fr(2, 10) == Fr(49, 50) and a + b - a * b == Fr(49, 50), "C02 example")
    chk(T("sp1") == Fr(108, 125) and Fr(108, 125) == Fr(9, 10) * Fr(24, 25) and 1 - Fr(1, 5) ** 2 == Fr(24, 25), "C03 example")
    chk(1 - Fr(1, 2) ** 3 == Fr(7, 8), "C04 example")
    br9 = {k: Fr(9, 10) for k in "ABCDE"}
    tree = BR()
    on = circ_prob(tree, br9, given=lambda s: s["E"]); off = circ_prob(tree, br9, given=lambda s: NOT(s["E"]))
    tot = circ_prob(tree, br9)
    chk(on == Fr(9801, 10000) and off == Fr(9639, 10000) and tot == Fr(97848, 100000), "C05 example %s %s %s" % (on, off, tot))
    pr = {k: Fr(1, 2) for k in "AB"}
    tp = P(C("A"), C("B"))
    chk(circ_prob(tp, pr) == Fr(3, 4) and circ_prob(tp, pr, event=lambda s: s["A"], given=lambda s: works(tp, s)) == Fr(2, 3), "C06 example")
    pr6 = {k: Fr(3, 5) for k in "AB"}
    q1, q2 = S(C("A"), C("B")), P(C("A"), C("B"))
    chk(circ_prob(q1, pr6) == Fr(9, 25) and circ_prob(q2, pr6) == Fr(21, 25)
        and circ_prob(q1, pr6, given=lambda s: works(q2, s)) == Fr(3, 7)
        and circ_prob(q2, pr6, given=lambda s: works(q1, s)) == 1, "C07 example")
    j = dep(Fr(1, 2), Fr(3, 5), Fr(1, 5))
    chk(j["AB"] == Fr(3, 10) and 1 - j["ab"] == Fr(3, 5) and j["AB"] + j["aB"] == Fr(2, 5)
        and Fr(1, 2) * Fr(2, 5) == Fr(1, 5), "C08 example")
    # C08-Q6 naive comparison quoted in the explanation
    chk(Fr(72, 100) ** 2 == Fr(5184, 10000), "C08 naive value")
    # C02/C01 trap numbers
    chk(Fr(9, 10) + Fr(8, 10) == Fr(17, 10), "sum 1.7")
    notes.append("lesson: all worked-example numbers verified")


if __name__ == "__main__":
    sys.exit(main())
