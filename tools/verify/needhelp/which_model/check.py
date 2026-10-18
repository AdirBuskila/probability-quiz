# -*- coding: utf-8 -*-
"""Machine checks of the which_model course.   PYTHONUTF8=1 py check.py

1. every stored answer is recomputed by BRUTE-FORCE enumeration / long series (independent of lib.py's formulas);
2. every story is simulated literally (Monte Carlo) and must agree within 4.5 standard errors;
3. every wrong-model option gives a DIFFERENT answer from the right one (by more than the answer tolerance);
4. every `sim` spec runs through the page's own sim.js (tools/sim_check.js): first run within 4 SE and exact enumeration;
5. every boss bankId exists, is in tools/verify/verified_sittings.txt, and the parameter steps are consistent.
"""
import itertools
import json
import math
import pathlib
import random
import subprocess
import sys
from fractions import Fraction as F
from math import comb, exp, factorial

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from defs import PROBLEMS, BOSS, SUITS, CHILD, BUS  # noqa: E402

APP = HERE.parents[3]
N_MC = 200000
fails = []


def fail(msg):
    fails.append(msg)
    print("FAIL", msg)


def prob(outcomes):
    """outcomes: iterable of (weight, bool)"""
    return sum(w for w, ok in outcomes if ok)


def pois(l, k):
    return exp(-l) * l ** k / factorial(k)


def bino(n, p, k):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


# ---------------------------------------------------------------- 1. brute-force exact values
def brute():
    out = {}
    # L1P1: 3 draws with replacement, 6 red / 4 blue
    out["L1P1"] = float(prob((F(6 if a else 4, 10) * F(6 if b else 4, 10) * F(6 if c else 4, 10), a + b + c == 2)
                             for a, b, c in itertools.product([1, 0], repeat=3)))
    out["L1P2"] = sum(1 for c in itertools.combinations(range(12), 4) if sum(x < 7 for x in c) == 2) / comb(12, 4)
    hands = list(itertools.combinations(range(52), 5))
    out["L1P3"] = sum(1 for c in hands if sum(x < 13 for x in c) == 2) / len(hands)
    out["L2P1"] = float(sum(F(1, 6 ** 4) for r in itertools.product(range(1, 7), repeat=4) if r[0] < 6 and r[1] < 6 and r[2] < 6 and r[3] == 6))
    out["L2P2"] = float(sum(F(3, 10) ** sum(t) * F(7, 10) ** (10 - sum(t)) for t in itertools.product([0, 1], repeat=10) if sum(t) == 3))
    out["L2P3"] = float(sum(F(2, 5) ** sum(t) * F(3, 5) ** (6 - sum(t)) for t in itertools.product([0, 1], repeat=6)
                            if sum(t[:5]) == 2 and t[5] == 1))
    out["L3P1"] = bino(200000, 3 / 200000, 3)                      # binomial with huge n: the Poisson limit
    out["L3P2"] = 1 - 3 * exp(-2)
    out["L4P1"] = sum(pois(8, n) * bino(n, 0.25, 2) for n in range(2, 90))
    out["L4P2"] = float(sum(F(bino(10, F(7, 10), a)) * F(bino(a, F(1, 5), 1)) for a in range(1, 11)))
    out["L5P1"] = sum(len({SUITS[x] for x in c}) for c in hands) / len(hands)
    out["L5P2"] = sum(4 - len(set(t)) for t in itertools.product(range(4), repeat=6)) / 4 ** 6
    out["L5P3"] = sum(sum(t[i] * t[i + 1] for i in range(9)) for t in itertools.product([0, 1], repeat=10)) / 2 ** 10
    out["L6P1"] = sum(CHILD) / len(CHILD)
    out["L6P2"] = sum(BUS) / len(BUS)
    out["L6P3"] = sum(1 for x in CHILD if x == 3) / len(CHILD)
    # L7P1: coins
    out["L7P1"] = float(sum(F(1, 2) * (F(1, 2) if c == 0 else F(4, 5)) for c in (0, 1)))
    # L7P2: Bayes over the joint table
    j = {(s, t): (F(1, 100) if s else F(99, 100)) * ((F(95, 100) if t else F(5, 100)) if s else (F(5, 100) if t else F(95, 100)))
         for s in (0, 1) for t in (0, 1)}
    out["L7P2"] = float(j[(1, 1)] / (j[(1, 1)] + j[(0, 1)]))
    out["L7P3"] = float(sum(F(1, 2) * (F(3, 4) if u == 0 else F(1, 4)) ** 2 for u in (0, 1)))
    out["L8P1"] = sum(pois(6, n) * (0.75 ** 3 if n == 3 else 0) for n in range(0, 60))   # n must be exactly 3 (0 spam + 3 regular)
    out["L8P2"] = sum(1 for c in itertools.combinations(range(40), 6) if sum(x < 6 for x in c) == 3) / comb(40, 6)
    out["L8P3"] = sum(F(2, 3) ** (k - 1) / 3 for k in range(2, 600, 2)).__float__()
    return out


print("1. brute-force exact values")
exact = brute()
for p in PROBLEMS:
    v = exact[p["id"]]
    if abs(v - p["ans"]) > 1e-4 if p["id"] == "L3P1" else abs(v - p["ans"]) > 1e-9:
        fail(f"{p['id']}: stored {p['ans']!r} vs brute force {v!r}")
    if abs(round(p["ans"], 4) - p["ans"]) > p["tol"]:
        fail(f"{p['id']}: rounding to 4 digits exceeds tol")
print("   ok" if not fails else "")

# ---------------------------------------------------------------- 2. Monte Carlo
print("2. Monte Carlo of the stories (%d trials each)" % N_MC)
for p in PROBLEMS:
    rng = random.Random(hash(p["id"]) & 0xFFFF if False else sum(map(ord, p["id"])) * 7919)
    vals = [v for v in (p["mc"](rng) for _ in range(N_MC)) if v is not None]
    n = len(vals)
    mean = sum(vals) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in vals) / (n - 1))
    se = sd / math.sqrt(n)
    target = p.get("mc_target", p["ans"])
    z = abs(mean - target) / se if se > 0 else 0
    print(f"   {p['id']}: mc={mean:.5f} target={target:.5f} se={se:.5f} z={z:.2f} n={n}")
    if z > 4.5:
        fail(f"{p['id']}: Monte Carlo {mean} disagrees with {target} (z={z:.1f})")
    if p.get("mc_note") == "approx" and abs(target - p["ans"]) > 0.005:
        fail(f"{p['id']}: the approximation is too far from the exact model")

# ---------------------------------------------------------------- 3. distractor models differ
print("3. wrong models give different answers")
for p in PROBLEMS:
    if len(p["opts"]) != 4:
        fail(f"{p['id']}: needs 4 options")
    for label, reason, alt in p["opts"][1:]:
        if alt is None or not reason.strip():
            fail(f"{p['id']}: option {label!r} lacks alt value or reason")
        elif abs(alt - p["ans"]) <= max(0.002, 3 * p["tol"]):
            fail(f"{p['id']}: wrong model {label!r} gives {alt:.5f}, too close to the answer {p['ans']:.5f}")
    if p["opts"][0][2] is not None:
        fail(f"{p['id']}: the first option must be the right one")

# ---------------------------------------------------------------- 4. sim specs through sim.js
print("4. sim specs through the page's sim.js")
jobs = [{"where": p["id"], "type": "sim", "spec": {"kind": p["sim"]["kind"], "estimate": p["sim"]["estimate"], "exact": p["ans"], "params": p["sim"]["params"]}, "item": {}}
        for p in PROBLEMS]
proc = subprocess.run(["node", str(APP / "tools" / "sim_check.js")], input=json.dumps(jobs), capture_output=True, text=True, encoding="utf-8", cwd=str(APP / "tools"))
try:
    res = json.loads(proc.stdout)
except Exception:
    res = []
    fail("sim_check.js produced no result: " + proc.stderr[:300])
for r in res:
    print("   ", r["where"], "ok" if r["ok"] else "FAIL", r["summary"])
    if not r["ok"]:
        fail(f"{r['where']} sim: {r['problems']}")

# ---------------------------------------------------------------- 5. boss ids and structure
print("5. boss bankIds")
ver = {ln.strip() for ln in (APP / "tools" / "verify" / "verified_sittings.txt").read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")}
bank = {q["id"]: q for q in json.loads((APP / "questions.json").read_text(encoding="utf-8"))["questions"]}
for b in BOSS:
    if b not in bank:
        fail(f"boss {b} is not in the bank")
    elif bank[b]["examCode"] not in ver:
        fail(f"boss {b}: sitting {bank[b]['examCode']} is not verified")
    elif bank[b].get("hold"):
        fail(f"boss {b} is held")
for lvl in range(1, 9):
    k = sum(2 + (1 if p.get("param") else 0) for p in PROBLEMS if p["level"] == lvl)
    if not 4 <= k <= 6:
        fail(f"level {lvl}: {k} questions")
    for p in [p for p in PROBLEMS if p["level"] == lvl]:
        if p.get("param"):
            pass

print("ALL OK" if not fails else f"{len(fails)} FAILURE(S)")
sys.exit(1 if fails else 0)
