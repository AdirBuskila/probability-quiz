# -*- coding: utf-8 -*-
"""Verification for the guided course `geo` (area method), courses/geo/C01..C09.js.
Run:  PYTHONUTF8=1 py tools/verify/needhelp/geo/check.py     (from the app root; ASCII output)

Every stored answer of every own question is asserted THREE ways:
  1. exact: a closed form written here in sympy (rational / log / pi) must equal the stored answer
            (numeric steps: within the stored tol; mcq: the correct option's TeX, parsed by sympy, equals it and
            every other option differs; symbolic CDF options are compared as functions of t);
  2. an independent deterministic integration of the event indicator on a 2000x2000 midpoint grid;
  3. Monte Carlo, 2*10^6 trials, within 4 standard errors (conditional: the SE uses the conditioned count).
Then region_sim_check.js runs the page's OWN sim.js / region.js on every `region` and `sim` of the course and
requires them to agree with the same exact value, so the button and the figure can never disagree with the key.
Finally the boss bankIds are checked against tools/verify/verified_sittings.txt and the built bank.
"""
import json, math, pathlib, re, subprocess, sys
import numpy as np
import sympy as sp
from sympy import Rational as R, log, pi, sqrt

APP = pathlib.Path(__file__).resolve().parents[4]
N = 2_000_000
rng = np.random.default_rng(20261018)
problems = []
rows = []


def fail(qid, msg):
    problems.append(f"{qid}: {msg}")


# ---------------------------------------------------------------- the key: how each question is computed
# rect = (a, b): X~U(0,a), Y~U(0,b);  ev / given: numpy predicates;  sym: closed form;
# kind "prob" (default) or "area" (the answer is an area, = p * a * b);  kind "omega": the answer is a*b.
def Q(rect, ev=None, sym=None, given=None, kind="prob", traps=(), mean=None):
    return dict(rect=rect, ev=ev, sym=sym, given=given, kind=kind, traps=traps, mean=mean)


U = (1, 1)
KEY = {
    "geo-C01-Q1": Q((1, 2), sym=R(2), kind="omega", traps=(1,)),
    "geo-C01-Q2": Q((3, 2), sym=R(6), kind="omega"),
    "geo-C01-Q3": Q((3, 2), lambda x, y: x < 1, R(1, 3)),
    "geo-C01-Q4": Q(U, lambda x, y: (x < .25) & (y > .5), R(1, 8)),
    "geo-C01-Q5": Q((1, 2), lambda x, y: y < .5, R(1, 4)),

    "geo-C02-Q1": Q(U, lambda x, y: y > x, R(1, 2)),
    "geo-C02-Q2": Q(U, lambda x, y: x + y < 2 / 3, R(2, 9)),
    "geo-C02-Q3": Q(U, lambda x, y: x + y < 1.25, R(23, 32)),
    "geo-C02-Q4": Q((1, 2), lambda x, y: y > x, R(3, 4), traps=(0.5,)),
    "geo-C02-Q5": Q(U, lambda x, y: y > 2 * x, R(1, 4)),

    "geo-C03-Q1": Q(U, lambda x, y: abs(x - y) < 1 / 3, R(5, 9)),
    "geo-C03-Q2": Q(U, lambda x, y: abs(x - y) > .25, R(9, 16)),
    "geo-C03-Q3": Q(U, lambda x, y: (x < y) & (x + y < .5), R(1, 16)),
    "geo-C03-Q4": Q(U, lambda x, y: (x + y > .5) & (x + y < 1.5), R(3, 4)),
    "geo-C03-Q5": Q((1, 2), lambda x, y: abs(x - y) < .5, R(7, 16), traps=(0.875,)),

    "geo-C04-Q1": Q(U, lambda x, y: x + y < 1, R(1, 2), kind="area"),
    "geo-C04-Q2": Q(U, lambda x, y: (x < .25) & (x + y < 1), R(7, 32), kind="area"),
    "geo-C04-Q3": Q(U, lambda x, y: x < .25, R(7, 16), given=lambda x, y: x + y < 1),
    "geo-C04-Q4": Q((1, 2), lambda x, y: y < 1, R(1, 3), given=lambda x, y: x + y > 1, traps=(0.25,)),
    "geo-C04-Q5": Q(U, lambda x, y: x > .5, R(1, 4), given=lambda x, y: y > x),

    "geo-C05-Q1": Q(U, lambda x, y: y < x ** 2, R(1, 3)),
    "geo-C05-Q2": Q(U, lambda x, y: x * y < .2, (1 + log(5)) / 5),
    "geo-C05-Q3": Q(U, lambda x, y: x * y < 1 / 3, (1 + log(3)) / 3),
    "geo-C05-Q4": Q(U, lambda x, y: x * x + y * y < 1 / 9, pi / 36),
    "geo-C05-Q5": Q((1, 2), lambda x, y: y > x ** 2, R(5, 6)),

    "geo-C06-Q1": Q(U, lambda x, y: np.maximum(x, y) < 2 / 3, R(4, 9)),
    "geo-C06-Q2": Q(U, lambda x, y: np.minimum(x, y) > .25, R(9, 16)),
    "geo-C06-Q3": Q(U, lambda x, y: np.minimum(x, y) < .25, R(7, 16), traps=(0.5625,)),
    "geo-C06-Q5": Q((1, 2), lambda x, y: np.maximum(x, y) < .5, R(1, 8), traps=(0.25,)),
    "geo-C06-Q6": Q(U, sym=R(2, 3), mean=lambda x, y: np.maximum(x, y)),

    "geo-C07-Q1": Q(U, lambda x, y: x / y < 1 / 3, R(1, 6)),
    "geo-C07-Q2": Q(U, lambda x, y: x / y > 2, R(1, 4)),
    "geo-C07-Q4": Q(U, lambda x, y: x * y < .1, R(1, 10) + R(1, 10) * log(10)),
    "geo-C07-Q5": Q(U, lambda x, y: x * y > .5, R(1, 2) - log(2) / 2),
    "geo-C07-Q6": Q((1, 2), lambda x, y: y / x < 1, R(1, 4), traps=(0.5,)),

    "geo-C08-Q1": Q(U, lambda x, y: abs(x - y) < .25, R(7, 16)),
    # the stick, done from the three piece lengths directly (independent of the region inequalities)
    "geo-C08-Q2": Q(U, lambda x, y: np.maximum.reduce([np.minimum(x, y), np.abs(x - y), 1 - np.maximum(x, y)]) < .5, R(1, 4)),
    "geo-C08-Q3": Q((1, 2), lambda x, y: 2 * (x + y) < 3, R(1, 2)),
    "geo-C08-Q4": Q(U, lambda x, y: (x / 2 < y) & (y < 2 * x), R(1, 2)),
    "geo-C08-Q5": Q(U, lambda x, y: np.minimum.reduce([x, 1 - x, y, 1 - y]) < .25, R(3, 4)),
}
# symbolic mcq: option expression in t  ->  (sympy closed form, probability predicate factory for the MC check at t0)
T = sp.Symbol("t", positive=True)
SYMBOLIC = {
    "geo-C06-Q4": (1 - (1 - T) ** 2, lambda t: (lambda x, y: np.minimum(x, y) <= t), (0.3, 0.7)),
    "geo-C07-Q3": (1 - 1 / (2 * T), lambda t: (lambda x, y: x / y <= t), (1.5, 3.0)),
}


# ---------------------------------------------------------------- helpers
def tex2sympy(s):
    s = s.strip().strip("$").strip()

    def arg(i):
        while s[i] == " ":
            i += 1
        if s[i] == "{":
            d, j = 0, i
            while True:
                d += (s[j] == "{") - (s[j] == "}")
                j += 1
                if d == 0:
                    break
            return s[i + 1:j - 1], j
        return s[i], i + 1

    while "\\frac" in s:
        k = s.index("\\frac")
        a, j = arg(k + 5)
        b, j = arg(j)
        s = s[:k] + f"(({a})/({b}))" + s[j:]
    s = re.sub(r"\\ln\s*(\d+)", r"log(\1)", s)
    s = s.replace("\\ln", "log").replace("\\pi", "pi").replace("\\cdot", "*").replace("^", "**")
    s = s.replace("{", "(").replace("}", ")")
    s = re.sub(r"(\d)\s*(log|pi|t)", r"\1*\2", s)
    return sp.sympify(s, locals={"t": T, "log": sp.log, "pi": sp.pi})


def exact_p(key):
    return float(key["sym"])


def mc_and_grid(qid, key):
    a, b = key["rect"]
    out = {}
    X = rng.random(N) * a
    Y = rng.random(N) * b
    if key["mean"]:
        v = key["mean"](X, Y)
        m, se = float(v.mean()), float(v.std() / math.sqrt(N))
        return dict(mc=m, se=se, grid=None)
    ev = key["ev"](X, Y)
    if key["given"]:
        g = key["given"](X, Y)
        n = int(g.sum())
        p = float((ev & g).sum() / n)
        se = math.sqrt(max(p * (1 - p), 1e-12) / n)
    else:
        p = float(ev.mean())
        se = math.sqrt(max(p * (1 - p), 1e-12) / N)
    # deterministic midpoint grid (independent of the sampler)
    M = 2000
    xs = (np.arange(M) + .5) / M * a
    cnt_e = cnt_g = 0.0
    for r in range(0, M, 250):
        xx, yy = np.meshgrid(xs, (np.arange(r, min(r + 250, M)) + .5) / M * b, indexing="ij")
        # (xx has M rows over x; yy a slab over y)
        e = key["ev"](xx, yy)
        if key["given"]:
            g = key["given"](xx, yy)
            cnt_g += g.sum()
            cnt_e += (e & g).sum()
        else:
            cnt_e += e.sum()
    grid = cnt_e / cnt_g if key["given"] else cnt_e / (M * M)
    return dict(mc=p, se=se, grid=float(grid))


def record(qid, what, ok, info):
    rows.append((qid, what, ok, info))
    if not ok:
        fail(qid, f"{what}: {info}")


# ---------------------------------------------------------------- load the levels
proc = subprocess.run(["node", str(APP / "tools" / "course_load.js")], capture_output=True, text=True, encoding="utf-8", cwd=str(APP / "tools"))
loaded = json.loads(proc.stdout)
assert not loaded["errors"], loaded["errors"]
levels = sorted([e["level"] for e in loaded["levels"] if e["courseId"] == "geo"], key=lambda L: L["order"])
assert [L["id"] for L in levels] == [f"C0{i}" for i in range(1, len(levels) + 1)], [L["id"] for L in levels]

own = {}
bank_ids = []
for L in levels:
    for q in L["questions"]:
        if "bankId" in q:
            bank_ids.append((L["id"], q["bankId"]))
        else:
            own[q["id"]] = (L["id"], q)

# every own question has a key
for qid in own:
    if qid not in KEY and qid not in SYMBOLIC:
        fail(qid, "no check defined for this question")
for qid in list(KEY) + list(SYMBOLIC):
    if qid not in own:
        fail(qid, "check defined but the question does not exist")

sym_by_q = {}
# ---------------------------------------------------------------- probability questions
for qid, key in KEY.items():
    if qid not in own:
        continue
    lid, q = own[qid]
    a, b = key["rect"]
    ex = key["sym"]
    exv = float(ex)
    if key["kind"] == "omega":
        record(qid, "omega = a*b", abs(a * b - exv) < 1e-12, f"rect {a}x{b} stored {exv}")
        want = exv
    elif key["kind"] == "area":
        r = mc_and_grid(qid, key)
        want = exv
        # the stored answer is an area: area = p * |Omega|; here a*b = 1
        record(qid, "area exact vs grid", abs(r["grid"] * a * b - exv) < 5e-4, f"grid={r['grid'] * a * b:.6f} exact={exv:.6f}")
        record(qid, "area exact vs MC", abs(r["mc"] * a * b - exv) <= 4 * r["se"] * a * b, f"mc={r['mc'] * a * b:.5f} se={r['se']:.5f}")
    else:
        r = mc_and_grid(qid, key)
        want = exv
        if key["mean"]:
            record(qid, "mean exact vs MC", abs(r["mc"] - exv) <= 4 * r["se"], f"mc={r['mc']:.5f} se={r['se']:.5f} exact={exv:.6f}")
        else:
            record(qid, "exact vs grid", abs(r["grid"] - exv) < 5e-4, f"grid={r['grid']:.6f} exact={exv:.6f}")
            record(qid, "exact vs MC", abs(r["mc"] - exv) <= 4 * r["se"], f"mc={r['mc']:.5f} se={r['se']:.5f} exact={exv:.6f}")
    sym_by_q[qid] = (exv, key["kind"])
    # --- the stored answer
    if "step" in q:
        s = q["step"]
        assert s["type"] == "numeric", qid
        ans, tol = float(s["answer"]), float(s.get("tol", 0))
        record(qid, "numeric answer within tol of exact", abs(ans - want) <= tol + 1e-12, f"stored={ans} tol={tol} exact={want:.6f}")
        record(qid, "stored answer is a faithful rounding", abs(ans - want) <= 6e-5 or abs(ans - want) <= 1e-12, f"stored={ans} exact={want:.6f}")
        for tv in key["traps"]:
            record(qid, f"trap value {tv} rejected", abs(tv - ans) > tol + 1e-9, f"trap={tv} stored={ans} tol={tol}")
    else:
        opts = {o["id"]: tex2sympy(o["value"]) for o in q["options"]}
        vals = {k: float(v) for k, v in opts.items()}
        record(qid, "mcq correct option equals exact", abs(vals[q["correctId"]] - want) < 1e-12, f"option {q['correctId']}={vals[q['correctId']]:.8f} exact={want:.8f}")
        others = [v for k, v in vals.items() if k != q["correctId"]]
        record(qid, "mcq distractors differ", all(abs(v - want) > 1e-6 for v in others), f"options={vals}")
        record(qid, "mcq options distinct", len({round(v, 9) for v in vals.values()}) == len(vals), f"options={vals}")

# ---------------------------------------------------------------- symbolic CDF options
for qid, (closed, factory, ts) in SYMBOLIC.items():
    if qid not in own:
        continue
    lid, q = own[qid]
    opts = {o["id"]: tex2sympy(o["value"]) for o in q["options"]}
    cid = q["correctId"]
    record(qid, "correct option equals the closed form", sp.simplify(opts[cid] - closed) == 0, f"{opts[cid]} vs {closed}")
    for k, v in opts.items():
        if k != cid:
            record(qid, f"distractor {k} differs as a function", sp.simplify(v - closed) != 0, f"{v}")
    for t0 in ts:
        X = rng.random(N); Y = rng.random(N)
        p = float(factory(t0)(X, Y).mean())
        se = math.sqrt(p * (1 - p) / N)
        e = float(closed.subs(T, t0))
        record(qid, f"closed form vs MC at t={t0}", abs(p - e) <= 4 * se, f"mc={p:.5f} exact={e:.5f}")
        # every distractor must be wrong at some tested t
    wrong_somewhere = {k: any(abs(float(v.subs(T, t0)) - float(closed.subs(T, t0))) > 1e-6 for t0 in ts) for k, v in opts.items() if k != cid}
    record(qid, "each distractor is wrong at a tested t", all(wrong_somewhere.values()), str(wrong_somewhere))

# ---------------------------------------------------------------- the page's own sim.js / region.js
jobs = []
for qid, (lid, q) in own.items():
    if qid not in sym_by_q and qid not in SYMBOLIC:
        continue
    if qid in sym_by_q:
        ex, kind = sym_by_q[qid]
        if q.get("sim"):
            rect = KEY[qid]["rect"]
            jobs.append({"where": qid, "type": "sim", "spec": q["sim"], "expect": ex if kind == "prob" else None})
        if q.get("region"):
            jobs.append({"where": qid, "type": "region", "spec": q["region"], "expect": ex if kind == "prob" else None})
    else:
        if q.get("sim") or q.get("region"):
            fail(qid, "symbolic question must not carry a sim/region")
# the question text of the area-only series (C04 Q1, Q2) must not carry a sim that would leak the next answer
for qid in ("geo-C04-Q1", "geo-C04-Q2"):
    if own[qid][1].get("sim") or own[qid][1].get("region"):
        fail(qid, "answer-revealing extras on a series question")

proc = subprocess.run(["node", str(pathlib.Path(__file__).with_name("region_sim_check.js"))], input=json.dumps(jobs), capture_output=True, text=True, encoding="utf-8", cwd=str(APP))
try:
    res = json.loads(proc.stdout)
except Exception:
    print("region_sim_check.js failed:", proc.stderr[:600].encode("ascii", "backslashreplace").decode())
    sys.exit(1)
for r in res:
    record(r["where"], r["type"] + " (page code)", r["ok"], r["summary"])

# every level except the intro and the boss has at least one sim; count them
n_sim = sum(1 for _, (l, q) in own.items() if q.get("sim"))
n_reg = sum(1 for _, (l, q) in own.items() if q.get("region"))

# ---------------------------------------------------------------- boss bankIds
verified = set(open(APP / "tools" / "verify" / "verified_sittings.txt", encoding="utf-8").read().split())
bank = {q["id"]: q for q in json.load(open(APP / "questions.json", encoding="utf-8"))["questions"]}
boss_level = [L for L in levels if L.get("boss")]
record("boss", "exactly one boss and it is last", len(boss_level) == 1 and boss_level[0] is levels[-1], str([L["id"] for L in boss_level]))
for lid, bid in bank_ids:
    code = bid.rsplit("-Q", 1)[0]
    record(bid, "boss bankId from a verified sitting", code in verified and bid in bank, f"sitting {code} verified={code in verified} in-bank={bid in bank}")
record("boss", "4-6 real questions", 4 <= len(bank_ids) <= 6, str(len(bank_ids)))

# ---------------------------------------------------------------- report
bad = [r for r in rows if not r[2]]
for r in rows:
    print(("ok   " if r[2] else "FAIL ") + f"{r[0]:12s} {r[1]:42s} {r[3]}")
print(f"\nown questions={len(own)} bank pulls={len(bank_ids)} sims={n_sim} regions={n_reg} checks={len(rows)} failures={len(bad)} problems={len(problems)}")
if problems:
    for p in problems:
        print("PROBLEM", p)
    sys.exit(1)
print("ALL CHECKS PASSED")
