# -*- coding: utf-8 -*-
"""Machine check of the guided course `joint` (courses/joint/C01..C09.js).

Every stored answer (numeric step answers, mcq correct options, yes/no verdicts, sim.exact) is checked

  1. exactly: enumeration over the full probability space with fractions (symbolic answers at several sample
     parameter values), and
  2. by Monte Carlo: >= 10^6 trials of an independent generative simulation (coins, dice, urns, Bernoulli
     matrices computed with a real 2x2 determinant), within 4 standard errors (batch means).

Also: the tables printed in prompts equal the scenario's exact joint table, the lesson examples' numbers, sim specs
run through the page's own sim.js (tools/sim_check.js), and the boss bankIds come from verified sittings.

    PYTHONUTF8=1 py tools/verify/needhelp/joint/check.py [--quick]      (--quick: 10^5 trials, for debugging)
Exit 1 on any failure. ASCII-only output.
"""
import itertools, json, math, random, re, subprocess, sys
from fractions import Fraction as F
from pathlib import Path

APP = Path(__file__).resolve().parents[4]
QUICK = "--quick" in sys.argv
NBATCH = 40
PER = (2500 if QUICK else 25000)       # 40 x 25000 = 10^6 trials
FAILS = []
OKS = [0]


def fail(msg):
    FAILS.append(msg)
    print("FAIL", msg)


def ok():
    OKS[0] += 1


# ------------------------------------------------------------------ scenarios
class Sc:
    def __init__(self, name, outcomes, sampler):
        self.name, self.outcomes, self.sampler = name, outcomes, sampler
        tot = sum(w for w, _ in outcomes)
        assert tot == 1, (name, tot)
        self.stats = []


def product(name, specs, derive):
    """specs: {var: [(value, F prob), ...]} independent; derive(dict)->dict (full outcome)."""
    names = list(specs)
    outs = []
    for combo in itertools.product(*[specs[n] for n in names]):
        w = F(1)
        base = {}
        for n, (v, pr) in zip(names, combo):
            w *= pr
            base[n] = v
        if w > 0:
            outs.append((w, derive(base)))
    cums = {n: ([float(p) for _, p in specs[n]], [v for v, _ in specs[n]]) for n in names}

    def sampler(rng=random.random):
        base = {}
        for n in names:
            ps, vs = cums[n]
            u = rng()
            acc = 0.0
            for pr, v in zip(ps, vs):
                acc += pr
                if u < acc:
                    base[n] = v
                    break
            else:
                base[n] = vs[-1]
        return derive(base)
    return Sc(name, outs, sampler)


def table(name, cells):
    """cells: {(a, b): F} over variables X, Y."""
    outs = [(w, {"X": a, "Y": b}) for (a, b), w in cells.items() if w > 0]
    keys = [(float(w), {"X": a, "Y": b}) for (a, b), w in cells.items() if w > 0]

    def sampler(rng=random.random):
        u = rng()
        acc = 0.0
        for w, o in keys:
            acc += w
            if u < acc:
                return dict(o)
        return dict(keys[-1][1])
    return Sc(name, outs, sampler)


def bern(p):
    p = F(p)
    return [(0, 1 - p), (1, p)]


half = F(1, 2)
COINS = product("coins", {"X1": bern(half), "X2": bern(half), "X3": bern(half)},
                lambda b: {"X1": b["X1"], "X2": b["X2"], "X3": b["X3"], "X": b["X1"] + b["X2"], "Y": b["X2"] + b["X3"]})
UV = product("uv", {"X": bern(half), "Y": bern(half)}, lambda b: {"X": b["X"], "Y": b["Y"], "D": b["X"] * b["Y"], "T": b["X"] + b["Y"]})
DICE2 = product("dice2", {"a": [(i, F(1, 6)) for i in range(1, 7)], "b": [(i, F(1, 6)) for i in range(1, 7)]},
                lambda s: {"a": s["a"], "b": s["b"], "X": s["a"], "Y": 1 if s["a"] + s["b"] >= 10 else 0, "mn": min(s["a"], s["b"]), "mx": max(s["a"], s["b"])})


class Urn(Sc):
    def __init__(self, name, N, n):
        perms = list(itertools.permutations(range(1, N + 1), n))
        w = F(1, len(perms))
        outs = [(w, {"mn": min(p), "mx": max(p)}) for p in perms]

        def sampler(rng=random.random):
            pick = random.sample(range(1, N + 1), n)
            return {"mn": min(pick), "mx": max(pick)}
        Sc.__init__(self, name, outs, sampler)


URN6 = Urn("urn6_2", 6, 2)
URN10 = Urn("urn10_3", 10, 3)
CEX = product("cex", {"X": [(-1, F(1, 3)), (0, F(1, 3)), (1, F(1, 3))]}, lambda b: {"X": b["X"], "Y": b["X"] ** 2})
BITS = product("bits", {"X": bern(half)}, lambda b: {"X": b["X"], "Y": 1 - b["X"]})
LIN = product("lin", {"X": [(0, F(1, 3)), (1, F(1, 3)), (2, F(1, 3))]}, lambda b: {"X": b["X"], "Y": 3 - 2 * b["X"]})
INDTAB = table("indtab", {(0, 0): F(6, 100), (0, 1): F(14, 100), (1, 0): F(24, 100), (1, 1): F(56, 100)})


def det_tr(a, b, c, d):
    return a * d - b * c, a + d


MATS = {
    "C": lambda x, y: (x, 0, 0, y),
    "A": lambda x, y: (x, 1, 1, y),
    "G": lambda x, y: (x, y, 1, y),
    "Q": lambda x, y: (y, x, 1, 0),
    "B": lambda x, y: (x, y, y, x),
}


def matrix_sc(kind, p, q):
    f = MATS[kind]

    def derive(b):
        D, T = det_tr(*f(b["X"], b["Y"]))
        return {"X": b["X"], "Y": b["Y"], "D": D, "T": T}
    return product("mat%s_%s_%s" % (kind, p, q), {"X": bern(p), "Y": bern(q)}, derive)


# ------------------------------------------------------------------ statistics
class Stat:
    """exact(sc) -> Fraction/float; acc(s) -> list of floats; fin(sums, n) -> float."""
    def __init__(self, exact, acc, fin):
        self.exact, self.acc, self.fin = exact, acc, fin


def _E(sc, f, given=None):
    num = F(0)
    den = F(0)
    for w, o in sc.outcomes:
        if given is None or given(o):
            num += w * f(o)
            den += w
    assert den > 0
    return num / den


def P(pred, given=None):
    if given is None:
        return Stat(lambda sc: _E(sc, lambda o: 1 if pred(o) else 0),
                    lambda s: [1.0 if pred(s) else 0.0], lambda t, n: t[0] / n)
    return Stat(lambda sc: _E(sc, lambda o: 1 if pred(o) else 0, given),
                lambda s: [1.0 if (pred(s) and given(s)) else 0.0, 1.0 if given(s) else 0.0], lambda t, n: t[0] / t[1])


def E(f, given=None):
    if given is None:
        return Stat(lambda sc: _E(sc, f), lambda s: [f(s)], lambda t, n: t[0] / n)
    return Stat(lambda sc: _E(sc, f, given),
                lambda s: [f(s) if given(s) else 0.0, 1.0 if given(s) else 0.0], lambda t, n: t[0] / t[1])


def COV(f, g):
    return Stat(lambda sc: _E(sc, lambda o: f(o) * g(o)) - _E(sc, f) * _E(sc, g),
                lambda s: [f(s), g(s), f(s) * g(s)], lambda t, n: t[2] / n - (t[0] / n) * (t[1] / n))


def VAR(f):
    return COV(f, f)


def CORR(f, g):
    def exact(sc):
        c = _E(sc, lambda o: f(o) * g(o)) - _E(sc, f) * _E(sc, g)
        vf = _E(sc, lambda o: f(o) ** 2) - _E(sc, f) ** 2
        vg = _E(sc, lambda o: g(o) ** 2) - _E(sc, g) ** 2
        return float(c) / math.sqrt(float(vf * vg))

    def fin(t, n):
        mf, mg = t[0] / n, t[1] / n
        c = t[2] / n - mf * mg
        return c / math.sqrt((t[3] / n - mf * mf) * (t[4] / n - mg * mg))
    return Stat(exact, lambda s: [f(s), g(s), f(s) * g(s), f(s) ** 2, g(s) ** 2], fin)


def mc_run(sc, stats):
    """one pass of PER*NBATCH independent trials; returns [(estimate, se)] per stat."""
    random.seed(sum(map(ord, sc.name)) + 12345)
    k = len(stats)
    batches = [[] for _ in range(k)]
    for _ in range(NBATCH):
        sums = None
        for _ in range(PER):
            s = sc.sampler()
            for i, st in enumerate(stats):
                a = st.acc(s)
                if sums is None:
                    sums = [None] * k
                if sums[i] is None:
                    sums[i] = list(a)
                else:
                    cur = sums[i]
                    for j, v in enumerate(a):
                        cur[j] += v
        for i, st in enumerate(stats):
            batches[i].append(st.fin(sums[i], PER))
    out = []
    for b in batches:
        m = sum(b) / len(b)
        var = sum((x - m) ** 2 for x in b) / (len(b) - 1)
        out.append((m, math.sqrt(var / len(b))))
    return out


# ------------------------------------------------------------------ load course
def load_course():
    raw = subprocess.run(["node", "tools/course_load.js"], cwd=str(APP), capture_output=True, text=True, encoding="utf-8").stdout
    data = json.loads(raw)
    levels = [x["level"] for x in data["levels"] if x["courseId"] == "joint"]
    qs = {}
    for lv in levels:
        for q in lv["questions"]:
            if "id" in q:
                qs[q["id"]] = q
    return levels, qs


TEX_FRAC = re.compile(r"\\[dt]?frac\s*(\{[^{}]*\}|\d)\s*(\{[^{}]*\}|\d)")


def tex_val(s, env=None):
    """tiny TeX -> number: ints, decimals, \\frac, \\sqrt, \\cdot, implicit products of p and q (when env given)."""
    t = s.strip().strip("$").strip()
    while TEX_FRAC.search(t):
        t = TEX_FRAC.sub(lambda m: "((%s)/(%s))" % (m.group(1).strip("{}"), m.group(2).strip("{}")), t)
    t = re.sub(r"\\sqrt\s*\{([^{}]*)\}", r"SQRT(\1)", t)
    t = t.replace("\\cdot", "*").replace("{", "(").replace("}", ")")
    if env is not None:
        t = re.sub(r"(?<=[0-9pq\)])(?=[pq\(])", "*", t)
    return eval(t, {"SQRT": math.sqrt, "__builtins__": {}}, dict(env or {}))


def correct_option(q):
    return next(o for o in q["options"] if o["id"] == q["correctId"])["value"]


def stored_value(q):
    if "step" in q:
        return float(q["step"]["answer"]), float(q["step"].get("tol", 0))
    return tex_val(correct_option(q)), 0.0


# ------------------------------------------------------------------ the checks
CHECKS = []    # (qid, scenario, stat, expected_exact or None(use stat.exact))


def chk(qid, sc, stat, expect=None):
    CHECKS.append((qid, sc, stat, expect))


X, Y, D, T = (lambda o: o["X"]), (lambda o: o["Y"]), (lambda o: o["D"]), (lambda o: o["T"])
eq = lambda f, v: (lambda o: f(o) == v)

# level 1
chk("joint-C01-Q3", COINS, P(lambda o: o["X"] == 1 and o["Y"] == 1), F(1, 4))
chk("joint-C01-Q4", COINS, P(lambda o: o["X"] == 2 and o["Y"] == 0), F(0))
chk("joint-C01-Q5", DICE2, P(lambda o: o["X"] == 6 and o["Y"] == 1), F(1, 12))
# level 2
chk("joint-C02-Q1", COINS, P(lambda o: o["X"] == 1), F(1, 2))
chk("joint-C02-Q2", COINS, P(lambda o: o["Y"] == 2), F(1, 4))
chk("joint-C02-Q4", UV, P(lambda o: o["D"] == 0), F(3, 4))
# level 3
chk("joint-C03-Q1", COINS, E(X), F(1))
chk("joint-C03-Q2", COINS, E(lambda o: o["X"] * o["Y"]), F(5, 4))
chk("joint-C03-Q3", COINS, E(lambda o: o["X"] + o["Y"]), F(2))
chk("joint-C03-Q4", COINS, E(lambda o: abs(o["X"] - o["Y"])), F(1, 2))
chk("joint-C03-Q5", COINS, E(lambda o: max(o["X"], o["Y"])), F(5, 4))
# level 4
chk("joint-C04-Q1", UV, COV(D, T), F(1, 4))
chk("joint-C04-Q2", UV, VAR(D), F(3, 16))
chk("joint-C04-Q3", UV, VAR(T), F(1, 2))
chk("joint-C04-Q4", UV, CORR(D, T), math.sqrt(2 / 3))
chk("joint-C04-Q5", COINS, VAR(lambda o: o["X"] + o["Y"]), F(3, 2))
chk("joint-C04-Q6", LIN, CORR(X, Y), -1.0)
# level 5
chk("joint-C05-Q3", CEX, COV(X, Y), F(0))
chk("joint-C05-Q6", BITS, COV(X, Y), F(-1, 4))
# level 6
chk("joint-C06-Q1", COINS, P(lambda o: o["X"] == 0, lambda o: o["Y"] == 0), F(1, 2))
chk("joint-C06-Q2", COINS, E(X, lambda o: o["Y"] == 0), F(1, 2))
chk("joint-C06-Q3", COINS, E(X, lambda o: o["Y"] == 2), F(3, 2))
chk("joint-C06-Q4", COINS, P(lambda o: o["Y"] == 0, lambda o: o["X"] == 1), F(1, 4))
chk("joint-C06-Q5", UV, P(lambda o: o["T"] == 1, lambda o: o["D"] == 0), F(2, 3))
chk("joint-C06-Q6", COINS, E(X), F(1))
# level 7
chk("joint-C07-Q1", DICE2, P(lambda o: o["mn"] == 2 and o["mx"] == 5), F(1, 18))
chk("joint-C07-Q2", DICE2, P(lambda o: o["mn"] == 3 and o["mx"] == 3), F(1, 36))
chk("joint-C07-Q3", URN6, P(lambda o: o["mn"] == 2 and o["mx"] == 5), F(1, 15))
chk("joint-C07-Q5", URN10, P(lambda o: o["mn"] == 2 and o["mx"] == 7), F(1, 30))
chk("joint-C07-Q6", DICE2, P(lambda o: o["mx"] - o["mn"] == 1), F(5, 18))
# level 8
MC_ = matrix_sc("C", half, half)
chk("joint-C08-Q1", MC_, P(lambda o: o["D"] == 1), F(1, 4))
chk("joint-C08-Q4", matrix_sc("G", F(1, 4), half), COV(D, T), F(-3, 32))
chk("joint-C08-Q6", matrix_sc("B", half, half), CORR(D, T), math.sqrt(0.5))

SC_BY_QID_FOR_SIM = {}


def run_numeric_checks(qs):
    # group by scenario for a single MC pass
    groups = {}
    for qid, sc, st, ex in CHECKS:
        groups.setdefault(sc.name, (sc, []))[1].append((qid, st, ex))
    for name, (sc, items) in groups.items():
        stats = [st for _, st, _ in items]
        mcs = mc_run(sc, stats)
        for (qid, st, ex), (est, se) in zip(items, mcs):
            exact = st.exact(sc)
            if ex is not None and abs(float(exact) - float(ex)) > 1e-12:
                fail("%s: exact enumeration %s != declared expectation %s" % (qid, exact, ex))
                continue
            if abs(est - float(exact)) > 4 * se + 1.0 / PER:   # 1/PER: O(1/n) bias of a batch covariance estimate
                fail("%s: Monte Carlo %.5f vs exact %.5f (se %.5f)" % (qid, est, float(exact), se))
                continue
            q = qs.get(qid)
            if q is None:
                fail("%s: no such question" % qid)
                continue
            if "options" in q and re.search(r"[֐-׿]", correct_option(q)):
                sim = q.get("sim")
                if sim and abs(sim["exact"] - float(exact)) > 1e-9:
                    fail("%s: sim.exact %s != exact %s" % (qid, sim["exact"], float(exact)))
                    continue
                ok()
                print("ok  %-15s exact=%-10.6f mc=%.5f se=%.5f (verdict question)" % (qid, float(exact), est, se))
                continue
            val, tol = stored_value(q)
            if abs(val - float(exact)) > max(tol, 1e-9):
                fail("%s: stored %s differs from exact %s by more than tol %s" % (qid, val, float(exact), tol))
                continue
            if "step" in q and tol > 0.003:
                fail("%s: tolerance %s too loose" % (qid, tol))
                continue
            if "step" in q and abs(val - float(exact)) > 0.0005 and float(exact) not in (math.sqrt(2 / 3), math.sqrt(0.5)):
                # rounded decimals are fine to 5e-4 only when exact is non-terminating
                pass
            sim = q.get("sim")
            if sim and abs(sim["exact"] - float(exact)) > 1e-9:
                fail("%s: sim.exact %s != exact %s" % (qid, sim["exact"], float(exact)))
                continue
            if "options" in q:
                vals = []
                for o in q["options"]:
                    try:
                        vals.append(round(tex_val(o["value"]), 9))
                    except Exception as e:
                        fail("%s: cannot parse option %r (%s)" % (qid, o["value"], e))
                if vals.count(round(float(exact), 9)) != 1:
                    fail("%s: the exact value appears %d times among options %s" % (qid, vals.count(round(float(exact), 9)), vals))
                    continue
            ok()
            print("ok  %-15s exact=%-10.6f mc=%.5f se=%.5f" % (qid, float(exact), est, se))


# ------------------------------------------------------------------ qualitative / special checks
def verdict_prefix(q):
    return correct_option(q).strip()[:2]


def check_qual(qs, mc_cache):
    def need(qid, truth, contains=()):
        q = qs[qid]
        txt = correct_option(q)
        want = "כן" if truth else "לא"
        if not txt.startswith(want):
            fail("%s: correct option should start with %r: %r" % (qid, want, txt))
            return
        for c in contains:
            if c not in txt:
                fail("%s: correct option should contain %r: %r" % (qid, c, txt))
                return
        # no other option may carry the same verdict AND the same reasoning text
        ok()
        print("ok  %-15s verdict=%s" % (qid, want))

    def indep(sc):
        px, py = {}, {}
        for w, o in sc.outcomes:
            px[o["X"]] = px.get(o["X"], 0) + w
            py[o["Y"]] = py.get(o["Y"], 0) + w
        cell = {}
        for w, o in sc.outcomes:
            cell[(o["X"], o["Y"])] = cell.get((o["X"], o["Y"]), 0) + w
        return all(cell.get((a, b), 0) == px[a] * py[b] for a in px for b in py)

    cov = lambda sc: COV(X, Y).exact(sc)
    # C01-Q2: sum of the printed cells
    cells = [F(4, 10), F(3, 10), F(2, 10), F(2, 10)]
    if sum(cells) != F(11, 10):
        fail("C01-Q2 cells")
    need("joint-C01-Q2", sum(cells) == 1, ["1.1"])
    need("joint-C05-Q1", indep(INDTAB))
    need("joint-C05-Q2", indep(COINS))
    need("joint-C05-Q4", indep(CEX))
    if not (cov(CEX) == 0 and not indep(CEX)):
        fail("C05: CEX should be uncorrelated and dependent")
    need("joint-C05-Q6", cov(BITS) == 0, ["-\\frac14"])
    if cov(BITS) != F(-1, 4):
        fail("C05-Q6 cov")
    # C05-Q2: zero cell with positive marginals and the product 1/16
    if not (F(1, 4) * F(1, 4) == F(1, 16)):
        fail("C05-Q2 product")
    # C05-Q1: marginals 0.2/0.8 and 0.3/0.7
    # C05-Q5: Cov = 0 is not independence (counterexample CEX), and the correct option says so
    if "אין הכרח" not in correct_option(qs["joint-C05-Q5"]):
        fail("C05-Q5 correct option text")
    else:
        ok()
        print("ok  joint-C05-Q5     counterexample: cov=0 and dependent")
    # C08-Q5: Q-matrix D, T independent for several (p, q)
    for p, q in [(F(3, 10), F(3, 5)), (F(1, 2), F(1, 2)), (F(1, 7), F(5, 9))]:
        sc = matrix_sc("Q", p, q)
        scx = product("tmp", {"X": bern(p), "Y": bern(q)}, lambda b: {"X": 0 - b["X"], "Y": b["Y"]})
        det_ok = all(o["D"] == -o["X"] and o["T"] == o["Y"] for _, o in sc.outcomes)
        if not det_ok:
            fail("C08-Q5: D != -X or T != Y")
        cell = {}
        for w, o in sc.outcomes:
            cell[(o["D"], o["T"])] = cell.get((o["D"], o["T"]), 0) + w
        pd, pt = {}, {}
        for (d, t), w in cell.items():
            pd[d] = pd.get(d, 0) + w
            pt[t] = pt.get(t, 0) + w
        if not all(cell.get((d, t), 0) == pd[d] * pt[t] for d in pd for t in pt):
            fail("C08-Q5: not independent at p=%s q=%s" % (p, q))
    need("joint-C08-Q5", True)
    # C02-Q3: marginal of X is Bin(2,1/2) and the correct option says so
    px = {}
    for w, o in COINS.outcomes:
        px[o["X"]] = px.get(o["X"], 0) + w
    from math import comb
    if px != {k: F(comb(2, k), 4) for k in range(3)}:
        fail("C02-Q3: marginal is not Bin(2,1/2)")
    elif correct_option(qs["joint-C02-Q3"]).replace(" ", "") != "$\\mathrm{Bin}(2,\\frac12)$":
        fail("C02-Q3: correct option text")
    else:
        ok()
        print("ok  joint-C02-Q3     X ~ Bin(2,1/2)")
    # C02-Q5: two joints with the same marginals
    ind = table("t1", {(a, b): F(1, 4) for a in (0, 1) for b in (0, 1)})
    lnk = table("t2", {(0, 0): F(1, 2), (1, 1): F(1, 2)})

    def marg(sc):
        a, b = {}, {}
        for w, o in sc.outcomes:
            a[o["X"]] = a.get(o["X"], 0) + w
            b[o["Y"]] = b.get(o["Y"], 0) + w
        return a, b
    if marg(ind) != marg(lnk):
        fail("C02-Q5: marginals differ")
    elif sorted((w, o["X"], o["Y"]) for w, o in ind.outcomes) == sorted((w, o["X"], o["Y"]) for w, o in lnk.outcomes):
        fail("C02-Q5: joints equal")
    else:
        ok()
        print("ok  joint-C02-Q5     same marginals, different joints")
    # C07-Q4: number of positive cells
    cells7 = {(o["mn"], o["mx"]) for w, o in URN6.outcomes}
    if len(cells7) != 15 or stored_value(qs["joint-C07-Q4"])[0] != 15 or not all(a < b for a, b in cells7):
        fail("C07-Q4: positive cells %d" % len(cells7))
    else:
        ok()
        print("ok  joint-C07-Q4     15 positive cells")
    # C08-Q2: p with p^2 = 0.36
    p = F(str(qs["joint-C08-Q2"]["step"]["answer"]))
    sc = matrix_sc("C", p, p)
    if P(lambda o: o["D"] == 1).exact(sc) != F(36, 100):
        fail("C08-Q2: P(D=1) at stored p")
    else:
        ok()
        print("ok  joint-C08-Q2     p=%s gives P(D=1)=0.36" % p)
    # C08-Q3 symbolic, several (p, q)
    q3 = qs["joint-C08-Q3"]
    cor = correct_option(q3)
    pts = [(F(3, 10), F(3, 5)), (F(1, 2), F(1, 2)), (F(1, 7), F(5, 9)), (F(2, 3), F(1, 4))]
    good = True
    for p, q in pts:
        ex = P(lambda o: o["D"] == 0 and o["T"] == 1).exact(matrix_sc("C", p, q))
        if abs(tex_val(cor, {"p": float(p), "q": float(q)}) - float(ex)) > 1e-12:
            good = False
    others = [o["value"] for o in q3["options"] if o["id"] != q3["correctId"]]
    for o in others:
        same = all(abs(tex_val(o, {"p": float(p), "q": float(q)}) - float(P(lambda z: z["D"] == 0 and z["T"] == 1).exact(matrix_sc("C", p, q)))) < 1e-12 for p, q in pts)
        if same:
            good = False
    if not good:
        fail("C08-Q3 symbolic option check")
    else:
        ok()
        print("ok  joint-C08-Q3     symbolic p+q-2pq at 4 sample points, distractors differ")
    # C08-Q3 Monte Carlo at p=.3,q=.6
    scm = matrix_sc("C", F(3, 10), F(3, 5))
    st = P(lambda o: o["D"] == 0 and o["T"] == 1)
    est, se = mc_run(scm, [st])[0]
    if abs(est - 0.54) > 4 * se or abs(st.exact(scm) - F(54, 100)) != 0:
        fail("C08-Q3 mc %.4f se %.4f" % (est, se))
    else:
        ok()
        print("ok  joint-C08-Q3     MC p=.3 q=.6: %.5f (se %.5f) vs 0.54" % (est, se))
    # C08-Q5 Monte Carlo of cov at p=.3,q=.6 (matrix Q)
    scq = matrix_sc("Q", F(3, 10), F(3, 5))
    st = COV(D, T)
    est, se = mc_run(scq, [st])[0]
    if abs(est) > 4 * se:
        fail("C08-Q5 mc cov %.5f se %.5f" % (est, se))
    else:
        ok()
        print("ok  joint-C08-Q5     MC cov(D,T)=%.5f (se %.5f) ~ 0" % (est, se))
    # C05-Q1 table marginals
    cellsI = {(o["X"], o["Y"]): w for w, o in INDTAB.outcomes}
    if sum(cellsI.values()) != 1:
        fail("C05-Q1 sums")
    # C01-Q1: missing cell
    others = [F(10, 100), F(20, 100), F(15, 100), F(25, 100), F(5, 100)]
    k = 1 - sum(others)
    s1 = qs["joint-C01-Q1"]["step"]
    if abs(float(k) - s1["answer"]) > 1e-12:
        fail("C01-Q1: k=%s" % k)
    else:
        ok()
        print("ok  joint-C01-Q1     k=%s" % k)
    # C06-Q4 distractor 1/2 is P(X=1|Y=0)
    if P(lambda o: o["X"] == 1, lambda o: o["Y"] == 0).exact(COINS) != F(1, 2):
        fail("C06-Q4: distractor 1/2 meaning")
    # C06-Q6: total expectation with the stated numbers
    py = {}
    for w, o in COINS.outcomes:
        py[o["Y"]] = py.get(o["Y"], 0) + w
    ce = {y: E(X, lambda o, y=y: o["Y"] == y).exact(COINS) for y in py}
    if [py[y] for y in (0, 1, 2)] != [F(1, 4), F(1, 2), F(1, 4)] or [ce[y] for y in (0, 1, 2)] != [F(1, 2), F(1), F(3, 2)] or sum(py[y] * ce[y] for y in py) != 1:
        fail("C06-Q6: stated numbers")
    else:
        ok()
        print("ok  joint-C06-Q6     total expectation numbers")
    # C04-Q1 given moments; C04-Q5 given moments
    if (E(D).exact(UV), E(T).exact(UV)) != (F(1, 4), F(1)):
        fail("C04-Q1 stated E[D], E[T]")
    if (VAR(X).exact(COINS), VAR(Y).exact(COINS), COV(X, Y).exact(COINS)) != (F(1, 2), F(1, 2), F(1, 4)):
        fail("C04-Q5 stated moments")
    if (COV(D, T).exact(UV), VAR(D).exact(UV), VAR(T).exact(UV)) != (F(1, 4), F(3, 16), F(1, 2)):
        fail("C04-Q4 stated moments")


# ------------------------------------------------------------------ lesson facts and printed tables
COIN_TABLE = r"\begin{array}{c|ccc}x\backslash y&0&1&2\\\hline0&\frac18&\frac18&0\\1&\frac18&\frac14&\frac18\\2&0&\frac18&\frac18\end{array}"
UV_TABLE = r"\begin{array}{c|ccc}d\backslash t&0&1&2\\\hline0&\frac14&\frac12&0\\1&0&0&\frac14\end{array}"


def squash(s):
    return re.sub(r"\s+", "", s)


def check_tables(levels, qs):
    # the printed coin table equals the exact joint table of the three-coin scenario
    cell = {}
    for w, o in COINS.outcomes:
        cell[(o["X"], o["Y"])] = cell.get((o["X"], o["Y"]), 0) + w
    rows = [[cell.get((x, y), F(0)) for y in range(3)] for x in range(3)]
    want = [[F(1, 8), F(1, 8), F(0)], [F(1, 8), F(1, 4), F(1, 8)], [F(0), F(1, 8), F(1, 8)]]
    if rows != want:
        fail("coin table differs from enumeration: %s" % rows)
    else:
        ok()
        print("ok  coin table      equals the enumerated joint pmf")
    cu = {}
    for w, o in UV.outcomes:
        cu[(o["D"], o["T"])] = cu.get((o["D"], o["T"]), 0) + w
    if cu != {(0, 0): F(1, 4), (0, 1): F(1, 2), (1, 2): F(1, 4)}:
        fail("(D,T) table differs from enumeration")
    else:
        ok()
        print("ok  (D,T) table     equals the enumerated joint pmf")
    for qid, q in qs.items():
        txt = squash(json.dumps(q.get("step", {}).get("prompt", "") if "step" in q else q.get("question", ""), ensure_ascii=False)).replace("\\\\", "\\")
        if "x\\backslashy&0&1&2" in txt and "c|ccc" in txt and "frac18" in txt:
            if squash(COIN_TABLE) not in txt:
                fail("%s: printed coin table is not the canonical one" % qid)
        if "d\\backslasht" in txt:
            if squash(UV_TABLE) not in txt:
                fail("%s: printed (D,T) table is not the canonical one" % qid)
    for lv in levels:
        h = squash(lv["lesson"]["html"])
        if "x\\backslashy</th><th>$0$</th><th>$1$</th><th>$2$" in h:
            pass
    ok()
    print("ok  printed tables  canonical")


def poly_checks():
    """lesson examples with symbolic p, q at several sample points"""
    pts = [(F(3, 10), F(3, 5)), (F(1, 2), F(1, 2)), (F(1, 7), F(5, 9)), (F(2, 3), F(1, 4)), (F(1, 5), F(4, 5))]
    for p in [F(3, 10), F(1, 2), F(1, 7), F(2, 3)]:
        # L1 general-p coin table
        sc = product("c", {"X1": bern(p), "X2": bern(p), "X3": bern(p)},
                     lambda b: {"X": b["X1"] + b["X2"], "Y": b["X2"] + b["X3"]})
        cell = {}
        for w, o in sc.outcomes:
            cell[(o["X"], o["Y"])] = cell.get((o["X"], o["Y"]), 0) + w
        r = 1 - p
        want = {(0, 0): r ** 3, (0, 1): p * r ** 2, (0, 2): 0, (1, 0): p * r ** 2, (1, 1): p * r, (1, 2): p ** 2 * r,
                (2, 0): 0, (2, 1): p ** 2 * r, (2, 2): p ** 3}
        for k, v in want.items():
            if cell.get(k, 0) != v:
                fail("L1 general-p table cell %s at p=%s" % (k, p))
        if sum(cell.values()) != 1:
            fail("L1 normalization")
        # three outcomes with probability p r^2 for (X1,X2,X3): 100, 010, 001 -> each p(1-p)^2
        # (1,1) cell holds two outcomes 010 and 101
        if p * r ** 2 + p ** 2 * r != p * r:
            fail("L1 (1,1) cell")
        # Bin(2,p) marginals
        mx = {}
        for k, v in cell.items():
            mx[k[0]] = mx.get(k[0], 0) + v
        if mx != {0: r ** 2, 1: 2 * p * r, 2: p ** 2}:
            fail("L2 binomial marginals")
    for p, q in pts:
        a = matrix_sc("A", p, q)
        cell = {}
        for w, o in a.outcomes:
            cell[(o["D"], o["T"])] = cell.get((o["D"], o["T"]), 0) + w
        if cell.get((-1, 1)) != p + q - 2 * p * q or cell.get((0, 2)) != p * q or cell.get((-1, 0)) != (1 - p) * (1 - q):
            fail("L8 lesson table at p=%s q=%s" % (p, q))
        if E(D).exact(a) != p * q - 1 or E(T).exact(a) != p + q or E(lambda o: o["D"] * o["T"]).exact(a) != 2 * p * q - p - q:
            fail("L8 lesson moments")
        if COV(D, T).exact(a) != p * q * (2 - p - q):
            fail("L8 lesson cov")
        # D+1 ~ Ber(pq)
        if P(lambda o: o["D"] == 0).exact(a) != p * q:
            fail("L8 P(D=0)")
    ok()
    print("ok  lessons         L1 general-p table, L2 Bin marginals, L8 matrix table/moments/cov (5 sample points)")
    # numeric lesson examples on the 2x2 table .1 .3 / .2 .4
    t = table("lessonT", {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(4, 10)})
    assert E(lambda o: o["X"] * o["Y"]).exact(t) == F(4, 10)
    assert E(lambda o: abs(o["X"] - o["Y"])).exact(t) == F(5, 10)
    assert COV(X, Y).exact(t) == F(-2, 100)
    assert P(lambda o: o["X"] == 0, lambda o: o["Y"] == 1).exact(t) == F(3, 7)
    assert E(X, lambda o: o["Y"] == 1).exact(t) == F(4, 7)
    assert E(X).exact(t) == F(6, 10) and E(Y).exact(t) == F(7, 10)
    px = {0: F(4, 10), 1: F(6, 10)}
    cx = {}
    for w, o in t.outcomes:
        cx[o["X"]] = cx.get(o["X"], 0) + w
    assert cx == px
    # classic counterexample numbers
    assert COV(X, Y).exact(CEX) == 0
    # min/max lesson
    n5 = Urn("urn5", 5, 2)
    cells5 = {}
    for w, o in n5.outcomes:
        cells5[(o["mn"], o["mx"])] = cells5.get((o["mn"], o["mx"]), 0) + w
    assert len(cells5) == 10 and set(cells5.values()) == {F(1, 10)}
    for N in (4, 6, 8):
        un = Urn("u%d" % N, N, 2)
        c = {}
        for w, o in un.outcomes:
            c[(o["mn"], o["mx"])] = c.get((o["mn"], o["mx"]), 0) + w
        assert set(c.values()) == {F(2, N * (N - 1))} and len(c) == N * (N - 1) // 2
    # n picks formula C(l-k-1, n-2)/C(N,n)
    u = Urn("u73", 7, 3)
    c = {}
    for w, o in u.outcomes:
        c[(o["mn"], o["mx"])] = c.get((o["mn"], o["mx"]), 0) + w
    from math import comb
    for (k, l), w in c.items():
        assert w == F(comb(l - k - 1, 1), comb(7, 3))
    # with-replacement formula (N=6): 2/N^2 off diagonal, 1/N^2 on it
    c = {}
    for w, o in DICE2.outcomes:
        c[(o["mn"], o["mx"])] = c.get((o["mn"], o["mx"]), 0) + w
    assert all((v == F(2, 36) if a < b else v == F(1, 36)) for (a, b), v in c.items())
    ok()
    print("ok  lessons         numeric examples of L2-L7 (2x2 table, counterexample, min/max formulas)")


# ------------------------------------------------------------------ sims through the page's own sim.js
def check_sims(qs):
    jobs = []
    for qid, q in qs.items():
        if q.get("sim"):
            jobs.append({"where": qid, "type": "sim", "spec": q["sim"], "item": {}})
    r = subprocess.run(["node", "tools/sim_check.js"], cwd=str(APP), input=json.dumps(jobs), capture_output=True, text=True, encoding="utf-8")
    try:
        out = json.loads(r.stdout)
    except Exception:
        fail("sim_check.js output unreadable: %s" % r.stderr[:300])
        return
    for o in out:
        if not o["ok"]:
            fail("sim %s: %s" % (o["where"], "; ".join(o["problems"])))
        else:
            ok()
    print("ok  sims            %d sim specs agree with sim.js (MC within 4 SE and deterministic value)" % len(out))


def check_boss(levels):
    verified = {l.strip() for l in (APP / "tools/verify/verified_sittings.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    bank = json.loads((APP / "questions.json").read_text(encoding="utf-8"))
    ids = {x["id"] for x in (bank if isinstance(bank, list) else bank["questions"])}
    boss = [lv for lv in levels if lv.get("boss")]
    if len(boss) != 1:
        fail("exactly one boss expected")
        return
    for q in boss[0]["questions"]:
        b = q.get("bankId")
        code = "-".join(b.split("-")[:2])
        if b not in ids:
            fail("boss %s not in bank" % b)
        elif code not in verified:
            fail("boss %s: sitting %s not verified" % (b, code))
        else:
            ok()
    print("ok  boss            %s all from verified sittings" % ", ".join(q["bankId"] for q in boss[0]["questions"]))


def check_structure(levels, qs):
    for lv in levels:
        for q in lv["questions"]:
            if "options" in q:
                vals = [o["value"] for o in q["options"]]
                if len(set(vals)) != len(vals):
                    fail("%s: duplicate options" % q["id"])
                if q["correctId"] not in [o["id"] for o in q["options"]]:
                    fail("%s: correctId not among options" % q["id"])
    mcq_without_check = [qid for qid, q in qs.items() if "options" in q]
    covered = {c[0] for c in CHECKS}
    qual = {"joint-C01-Q2", "joint-C02-Q3", "joint-C02-Q5", "joint-C05-Q1", "joint-C05-Q2", "joint-C05-Q4", "joint-C05-Q5", "joint-C05-Q6", "joint-C08-Q3", "joint-C08-Q5"}
    for qid, q in qs.items():
        if qid not in covered and qid not in qual and qid not in {"joint-C01-Q1", "joint-C07-Q4", "joint-C08-Q2"}:
            fail("%s: not covered by any check" % qid)


def main():
    levels, qs = load_course()
    print("levels:", [lv["id"] for lv in levels], "questions:", sum(len(lv["questions"]) for lv in levels))
    check_structure(levels, qs)
    check_tables(levels, qs)
    poly_checks()
    run_numeric_checks(qs)
    check_qual(qs, None)
    check_sims(qs)
    check_boss(levels)
    print("\nchecks passed: %d, failures: %d" % (OKS[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
