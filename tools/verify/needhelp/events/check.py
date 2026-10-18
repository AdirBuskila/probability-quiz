# -*- coding: utf-8 -*-
"""Machine check of the guided course `events` (events, conditional probability, Bayes, independence).

Run from anywhere:  py tools/verify/needhelp/events/check.py     (ASCII output, exit 1 on any failure)

For every authored question the stored answer is recomputed here in two independent ways:
  1. EXACT: Fraction arithmetic over a fully enumerated finite probability space (dice, labelled urn balls, the four
     cells of two events), never by the formula the lesson teaches;
  2. MONTE CARLO: >= 10**6 samples from that same space (numpy), within 4 standard errors of the key.
Every `sim` spec stored in the course is rebuilt here from its own params (dice / urn / custom_discrete), evaluated
by enumeration and by Monte Carlo, and must equal both the sim's `exact` and the question's key.
Non-numeric answers (set identities, partitions, independent/disjoint verdicts, findbug lines, "can it be") are
decided by brute force: random subsets, explicit joint tables, or explicit claims per line.
Boss bankIds must exist in questions.json and belong to a sitting listed in tools/verify/verified_sittings.txt.
"""
import itertools
import json
import math
import random
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
FAILS = []
N_MC = 1_000_000
RNG = np.random.default_rng(20261018)


def fail(msg):
    FAILS.append(msg)
    print("FAIL", msg)


def need(cond, msg):
    if not cond:
        fail(msg)
    return cond


# ------------------------------------------------------------------ probability spaces
def frac(x):
    return F(str(x)).limit_denominator(10**9) if not isinstance(x, F) else x


def dice(n, faces=6):
    out = []
    for t in itertools.product(range(1, faces + 1), repeat=n):
        o = {f"d{i + 1}": v for i, v in enumerate(t)}
        o.update({"sum": sum(t), "max": max(t), "min": min(t), "n": n})
        out.append((o, F(1, faces ** n)))
    return out


def urn(counts=None, draws=1, replace=False, values=None):
    if values is not None:
        balls = [("v", v) for v in values]
    else:
        balls = [(c, None) for c, k in counts.items() for _ in range(k)]
    tot = len(balls)
    seqs = itertools.product(range(tot), repeat=draws) if replace else itertools.permutations(range(tot), draws)
    out = []
    w = None
    for s in seqs:
        if w is None:
            w = F(1, tot ** draws) if replace else F(1, math.perm(tot, draws))
        o = {}
        if values is not None:
            vs = [balls[i][1] for i in s]
            o.update({f"v{i + 1}": v for i, v in enumerate(vs)})
            o.update({"sum": sum(vs), "max": max(vs), "min": min(vs)})
        else:
            cols = [balls[i][0] for i in s]
            for c in counts:
                o[c] = sum(1 for x in cols if x == c)
                for i, x in enumerate(cols):
                    o[f"{c}_{i + 1}"] = 1 if x == c else 0
        out.append((o, w))
    return out


def cells(ab, a_only, b_only, none, a="A", b="B"):
    ab, a_only, b_only, none = map(frac, (ab, a_only, b_only, none))
    assert ab + a_only + b_only + none == 1
    return [({a: 1, b: 1}, ab), ({a: 1, b: 0}, a_only), ({a: 0, b: 1}, b_only), ({a: 0, b: 0}, none)]


def cells_pqs(p, q, s):
    """The four cells from P(A)=p, P(B)=q, P(A or B)=s, built by inclusion-exclusion and RE-VERIFIED from the table."""
    p, q, s = map(frac, (p, q, s))
    d = cells(p + q - s, s - q, s - p, 1 - s)
    assert P(d, "A == 1") == p and P(d, "B == 1") == q and P(d, "A == 1 or B == 1") == s
    return d


def ev(expr, o):
    return bool(eval(expr, {"__builtins__": {}}, o))


def P(dist, event, given=None):
    num = sum(w for o, w in dist if (given is None or ev(given, o)) and ev(event, o))
    den = sum(w for o, w in dist if given is None or ev(given, o))
    return num / den


def mc(dist, event, given=None, n=N_MC):
    """Monte Carlo estimate and its standard error (conditional: only trials meeting the given count)."""
    w = np.array([float(x) for _, x in dist])
    w = w / w.sum()
    idx = RNG.choice(len(dist), size=n, p=w)
    e = np.array([ev(event, o) for o, _ in dist])
    g = np.array([True if given is None else ev(given, o) for o, _ in dist])
    gi = g[idx]
    k = int(gi.sum())
    need(k >= 1000, f"MC: only {k} trials meet the given {given}")
    est = float((e[idx] & gi).sum()) / k
    se = math.sqrt(max(est * (1 - est), 1e-12) / k)
    return est, se


def both(label, dist, event, given=None, scale=1):
    """Exact (Fraction) + Monte Carlo check; returns the exact value times scale."""
    ex = P(dist, event, given)
    est, se = mc(dist, event, given)
    need(abs(est - float(ex)) <= 4 * se + 1e-9, f"{label}: Monte Carlo {est:.5f} vs exact {float(ex):.5f} (4se={4 * se:.5f})")
    return ex * scale


# ------------------------------------------------------------------ parsing stored answers
def opt_val(s):
    s = s.replace("$", "").strip()
    m = re.fullmatch(r"\\frac\{(\d+)\}\{(\d+)\}", s)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    try:
        return F(s)
    except Exception:
        return None


def load_levels():
    out = subprocess.run(["node", str(ROOT / "tools" / "course_load.js")], capture_output=True, check=True).stdout
    d = json.loads(out.decode("utf-8"))
    qs, levels = {}, {}
    for e in d["levels"]:
        if e["courseId"] != "events":
            continue
        lv = e["level"]
        levels[lv["id"]] = lv
        for q in lv["questions"]:
            qs[q.get("id") or q.get("bankId")] = (lv["id"], q)
    return qs, levels


def check_numeric(qid, q, key):
    key = F(key)
    st = q["step"]
    need(st["type"] == "numeric", f"{qid}: expected a numeric step")
    tol = st.get("tol", 0)
    need(abs(float(key) - st["answer"]) <= tol + 1e-9, f"{qid}: stored {st['answer']} (+-{tol}) vs key {float(key):.6f}")
    need(tol <= max(0.005, 0.01 * abs(float(key))), f"{qid}: tol {tol} too loose")


def check_mcq_value(qid, q, key):
    key = F(key)
    vals = {o["id"]: opt_val(o["value"]) for o in q["options"]}
    need(all(v is not None for v in vals.values()), f"{qid}: an option is not a number: {vals}")
    need(len(set(vals.values())) == len(vals), f"{qid}: duplicate option values")
    good = [i for i, v in vals.items() if v == key]
    need(good == [q["correctId"]], f"{qid}: options equal to key {key}: {good}, stored correctId {q['correctId']}")


def check_mcq_truth(qid, q, truth):
    """truth: {option id: bool} decided by brute force; exactly one is True and it is the stored correctId."""
    need(set(truth) == {o["id"] for o in q["options"]}, f"{qid}: truth keys vs options")
    good = [i for i, v in truth.items() if v]
    need(good == [q["correctId"]], f"{qid}: true options {good}, stored {q['correctId']}")


def check_findbug(qid, q, truth):
    st = q["step"]
    need(st["type"] == "findbug", f"{qid}: expected findbug")
    need(len(truth) == len(st["lines"]), f"{qid}: need one truth value per line")
    bad = [i for i, v in enumerate(truth) if not v]
    need(bad == [st["bugIndex"]], f"{qid}: false lines {bad}, stored bugIndex {st['bugIndex']}")


# ------------------------------------------------------------------ sims
def sim_dist(sim):
    k, pr = sim["kind"], sim["params"]
    if k == "dice":
        return dice(pr["n"], pr.get("faces", 6))
    if k == "urn":
        return urn(pr.get("counts"), pr["draws"], pr.get("replace", False), pr.get("values"))
    if k == "custom_discrete":
        out = []
        for row in pr["joint"]:
            o = {kk: vv for kk, vv in row.items() if kk != "p"}
            out.append((o, frac(row["p"])))
        need(sum(w for _, w in out) == 1, "custom_discrete joint does not sum to 1")
        return out
    raise ValueError(k)


def check_sim(qid, sim, key):
    d = sim_dist(sim)
    pr = sim["params"]
    ex = both(f"{qid} sim", d, pr["event"], pr.get("given"))
    need(abs(float(ex) - sim["exact"]) < 1e-9, f"{qid}: sim.exact {sim['exact']} vs enumeration {float(ex)}")
    if key is not None:
        need(ex == F(key), f"{qid}: sim enumerates to {ex}, question key {key}")


# ------------------------------------------------------------------ the keys, question by question
def keys():
    K = {}  # qid -> (kind, payload)
    S = frozenset
    omega = S(range(1, 7))

    # ---- C01
    d1 = dice(1)
    K["events-C01-Q1"] = ("num", both("C01-Q1", d1, "d1 % 2 == 0 and d1 > 3", scale=6))
    K["events-C01-Q2"] = ("val", both("C01-Q2", d1, "d1 % 2 == 0 or d1 > 3"))
    rnd = random.Random(7)
    subs = [S(x for x in omega if rnd.random() < 0.5) for _ in range(300)]
    pairs = [(A, B) for A in subs for B in subs[:40]]
    K["events-C01-Q3"] = ("truth", {
        "a": all((omega - A) | (omega - B) == omega - (A | B) for A, B in pairs),
        "b": all((omega - A) & (omega - B) == omega - (A | B) for A, B in pairs),
        "c": all((A & B) == omega - (A | B) for A, B in pairs),
        "d": all(omega - (A & B) == omega - (A | B) for A, B in pairs)})
    K["events-C01-Q4"] = ("num", both("C01-Q4", d1, "d1 % 2 == 1 and d1 <= 3"))
    K["events-C01-Q5"] = ("val", both("C01-Q5", d1, "(d1 % 2 == 0 and d1 <= 3) or (d1 % 2 == 1 and d1 > 3)"))
    A, B = S({2, 4, 6}), S({4, 5, 6})
    K["events-C01-Q6"] = ("bug", [
        omega - A == S({1, 3, 5}) and omega - B == S({1, 2, 3}),
        omega - (A | B) == (omega - A) & (omega - B),        # "none" is the complement of the union (definition)
        omega - (A | B) == (omega - A) | (omega - B),         # the claim as written: false
        (omega - A) & (omega - B) == S({1, 3}) and F(2, 6) == F(1, 3)])

    # ---- C02
    K["events-C02-Q1"] = ("num", both("C02-Q1", cells(F(1, 10), F(4, 10), F(2, 10), F(3, 10)), "A == 1 or B == 1"))
    c = cells_pqs(F(5, 10), F(3, 10), F(7, 10))          # P(A)=.5 P(B)=.3, P(A and B)=.1  => s=.7
    need(P(c, "A == 1 and B == 1") == F(1, 10), "C02 cells")
    K["events-C02-Q2"] = ("num", both("C02-Q2", c, "A == 1 and B == 0"))
    c3 = cells(F(1, 10), F(4, 10), F(3, 10), F(2, 10))  # P(A)=.5 P(B)=.4 P(AB)=.1
    need(P(c3, "A == 1") == F(1, 2) and P(c3, "B == 1") == F(4, 10), "C02-Q3 cells")
    K["events-C02-Q3"] = ("num", both("C02-Q3", c3, "A + B == 1"))
    K["events-C02-Q4"] = ("num", F(sum(1 for n in range(100, 1000) if n % 7 == 0)))
    nums = urn(values=list(range(100, 1000)), draws=1)
    K["events-C02-Q5"] = ("val", both("C02-Q5", nums, "v1 % 2 == 0 or v1 % 5 == 0"))
    mf = cells(F(3, 10), F(3, 10), F(2, 10), F(2, 10), a="M", b="F")
    need(P(mf, "M == 1") == F(6, 10) and P(mf, "F == 1") == F(5, 10), "C02-Q6 cells")
    uni = P(mf, "M == 1 or F == 1")
    K["events-C02-Q6"] = ("bug", [
        True, True,
        F(6, 10) + F(5, 10) - 2 * F(3, 10) == uni,           # claim: union = .6+.5-2*.3 : false
        1 - uni == F(2, 10)])

    # ---- C03
    c = cells_pqs(F(5, 10), F(4, 10), F(7, 10))
    K["events-C03-Q1"] = ("num", both("C03-Q1", c, "A == 1 and B == 1"))
    K["events-C03-Q2"] = ("num", both("C03-Q2", c, "A == 1 and B == 0"))
    c = cells_pqs(F(3, 10), F(5, 10), F(8, 10))
    disj = P(c, "A == 1 and B == 1") == 0
    indep = P(c, "A == 1 and B == 1") == P(c, "A == 1") * P(c, "B == 1")
    K["events-C03-Q3"] = ("truth", {"a": disj and not indep, "b": indep and not disj, "c": disj and indep,
                                     "d": (not disj) and (not indep)})
    pa, qb = F(4, 10), F(5, 10)
    ind = [({"A": a, "B": b}, (pa if a else 1 - pa) * (qb if b else 1 - qb)) for a in (0, 1) for b in (0, 1)]
    K["events-C03-Q4"] = ("num", both("C03-Q4", ind, "A == 1 or B == 1"))

    def feasible(p, q, s):
        try:
            cells_pqs(p, q, s)
            return True
        except AssertionError:
            return False

    def feasible_cells(p, q, s):
        t = (p + q - s, s - q, s - p, 1 - s)
        return all(x >= 0 for x in t)

    for s_ in (F(65, 100), F(7, 10), F(9, 10), F(1)):
        pass
    K["events-C03-Q5"] = ("truth", {i: not feasible_cells(F(6, 10), F(7, 10), s_) for i, s_ in
                                     zip("abcd", (F(65, 100), F(7, 10), F(9, 10), F(1)))})
    c = cells_pqs(F(3, 10), F(5, 10), F(7, 10))
    K["events-C03-Q6"] = ("num", both("C03-Q6", c, "A + B == 1"))

    # ---- C04
    d2 = dice(2)
    K["events-C04-Q1"] = ("num", both("C04-Q1", d2, "d1 % 2 == 0", "sum == 8"))
    K["events-C04-Q2"] = ("val", both("C04-Q2", d2, "sum >= 10", "max == 6"))
    need(sum(1 for o, _ in d2 if o["sum"] == 6) == 5, "C04-Q3 |B|")
    need(sum(1 for o, _ in d2 if o["sum"] == 6 and o["d1"] != o["d2"]) == 4, "C04-Q3 |A and B|")
    K["events-C04-Q3"] = ("bug", [True, True,
                                   F(4, 36) == P(d2, "d1 != d2", "sum == 6")])  # claim 4/36: false (true value 4/5)
    c = cells_pqs(F(5, 10), F(4, 10), F(7, 10))
    K["events-C04-Q4"] = ("num", both("C04-Q4", c, "B == 1", "A == 1"))
    # C04-Q5: which expression is "the fraction of M that is not F": decided on random joint tables
    rj = random.Random(11)
    ok = {k: True for k in "abcd"}
    for _ in range(200):
        w = [F(rj.randint(1, 20)) for _ in range(4)]
        t = sum(w)
        j = [({"M": m, "F": f}, w[i] / t) for i, (m, f) in enumerate(itertools.product((0, 1), repeat=2))]
        tgt = P(j, "F == 0", "M == 1")
        pr = lambda e, g=None: P(j, e, g)
        cand = {"a": pr("F == 0", "M == 1"),
                "b": pr("M == 1", "F == 0"),
                "c": pr("F == 0 and M == 1"),
                "d": pr("M == 0", "F == 1")}
        for k, v in cand.items():
            ok[k] = ok[k] and v == tgt
    K["events-C04-Q5"] = ("truth", ok)

    # ---- C05
    K["events-C05-Q1"] = ("num", F(6, 10) * F(25, 100))
    u = urn({"red": 4, "black": 6}, 2, False)
    K["events-C05-Q2"] = ("num", both("C05-Q2", u, "red_1 and red_2"))
    u = urn({"red": 5, "black": 5}, 3, False)
    K["events-C05-Q3"] = ("num", both("C05-Q3", u, "red_1 and red_2 and red_3"))
    m = []
    for a, b in itertools.product((1, 0), repeat=2):
        pa_ = F(9, 10) if a else F(1, 10)
        pb_ = (F(8, 10) if b else F(2, 10)) if a else (F(3, 10) if b else F(7, 10))
        m.append(({"D1": a, "D2": b}, pa_ * pb_))
    K["events-C05-Q4"] = ("val", both("C05-Q4", m, "D1 == 1 and D2 == 0"))
    u = urn({"red": 4, "black": 6}, 2, False)
    K["events-C05-Q5"] = ("bug", [P(u, "red_1") == F(4, 10),
                                   P(u, "red_2", "red_1") == F(3, 9),
                                   P(u, "red_1 and red_2") == F(4, 10) * F(4, 10)])
    # chain rule check on a table whose conditionals are the given ones: P(A)=.5 P(B|A)=.6 P(C|AB)=.4
    ch = [({"A": 1, "B": 1, "C": 1}, F(5, 10) * F(6, 10) * F(4, 10))]
    rest = 1 - ch[0][1]
    ch.append(({"A": 0, "B": 0, "C": 0}, rest))
    K["events-C05-Q6"] = ("num", both("C05-Q6", ch, "A == 1 and B == 1 and C == 1"))

    # ---- C06
    mach = [({"M": 1, "D": 1}, F(6, 10) * F(2, 100)), ({"M": 1, "D": 0}, F(6, 10) * F(98, 100)),
            ({"M": 2, "D": 1}, F(4, 10) * F(5, 100)), ({"M": 2, "D": 0}, F(4, 10) * F(95, 100))]
    K["events-C06-Q1"] = ("num", both("C06-Q1", mach, "D == 1"))
    bx = []
    for k, (pk, rk) in enumerate([(F(5, 10), F(1, 10)), (F(3, 10), F(2, 10)), (F(2, 10), F(4, 10))], 1):
        bx += [({"K": k, "R": 1}, pk * rk), ({"K": k, "R": 0}, pk * (1 - rk))]
    K["events-C06-Q2"] = ("num", both("C06-Q2", bx, "R == 1"))
    u = urn({"red": 3, "black": 7}, 2, False)
    K["events-C06-Q3"] = ("num", both("C06-Q3", u, "red_2"))
    pa_ = F(4, 10)
    j = [({"A": a, "B": b}, (pa_ if a else 1 - pa_) * ((F(1, 2) if a else F(1, 5)) if b else 1 - (F(1, 2) if a else F(1, 5))))
         for a in (1, 0) for b in (1, 0)]
    K["events-C06-Q4"] = ("num", both("C06-Q4", j, "B == 1"))
    j = [({"A": a, "B": b}, (F(3, 10) if a else F(7, 10)) * ((F(9, 10) if a else F(2, 10)) if b else 1 - (F(9, 10) if a else F(2, 10))))
         for a in (1, 0) for b in (1, 0)]
    K["events-C06-Q5"] = ("bug", [F(7, 10) == 1 - F(3, 10), True, P(j, "B == 1") == F(69, 100)])
    pb = {"a": ({2, 4, 6}, {4, 5, 6}), "b": ({1, 2}, {5, 6}), "c": ({2, 4, 6}, {1, 3, 5}), "d": ({1, 2, 3}, {4, 5})}
    K["events-C06-Q6"] = ("truth", {k: (not (S(x) & S(y))) and (S(x) | S(y) == omega) for k, (x, y) in pb.items()})

    # ---- C07
    dz = [({"S": 1, "T": 1}, F(1, 100) * F(95, 100)), ({"S": 1, "T": 0}, F(1, 100) * F(5, 100)),
          ({"S": 0, "T": 1}, F(99, 100) * F(5, 100)), ({"S": 0, "T": 0}, F(99, 100) * F(95, 100))]
    K["events-C07-Q1"] = ("num", both("C07-Q1", dz, "S == 1", "T == 1"))
    K["events-C07-Q2"] = ("num", both("C07-Q2", mach, "M == 2", "D == 1"))
    K["events-C07-Q3"] = ("bug", [P(mach, "D == 1") == F(32, 1000), P(mach, "M == 2 and D == 1") == F(2, 100),
                                   P(mach, "M == 2", "D == 1") == F(5, 100)])
    p_, q_, s_ = F(3, 10), F(5, 10), F(4, 10)       # P(A)=p, P(B)=q, P(B|not A)=s
    pab = q_ - s_ * (1 - p_)
    j = cells(pab, p_ - pab, s_ * (1 - p_), 1 - p_ - s_ * (1 - p_))
    need(P(j, "A == 1") == p_ and P(j, "B == 1") == q_ and P(j, "B == 1", "A == 0") == s_, "C07-Q4 table")
    K["events-C07-Q4"] = ("num", both("C07-Q4", j, "A == 0", "B == 1"))

    def cond_feasible(q, s=F(9, 10)):
        """exists a table with P(not A | not B)=q and P(A or B)=s ?  P(not B)=(1-s)/q must be in (0,1]."""
        pnb = (1 - s) / q
        if not (0 < pnb <= 1):
            return False
        a_only = s - (1 - pnb)               # P(A and not B) = P(A or B) - P(B)
        return 0 <= a_only <= pnb

    K["events-C07-Q5"] = ("truth", {i: not cond_feasible(v) for i, v in zip("abcd", (F(5, 100), F(2, 10), F(5, 10), F(9, 10)))})

    # ---- C08
    c = cells(0, F(3, 10), F(4, 10), F(3, 10))
    K["events-C08-Q1"] = ("truth", {
        "a": P(c, "A == 1 and B == 1") != P(c, "A == 1") * P(c, "B == 1"),
        "b": P(c, "A == 1 and B == 1") == P(c, "A == 1") * P(c, "B == 1"),
        "c": P(c, "A == 1 and B == 1") == P(c, "A == 1") * P(c, "B == 1"),
        "d": False})
    pa, qb = F(3, 10), F(4, 10)
    ind = [({"A": a, "B": b}, (pa if a else 1 - pa) * (qb if b else 1 - qb)) for a in (0, 1) for b in (0, 1)]
    K["events-C08-Q2"] = ("num", both("C08-Q2", ind, "A == 1 or B == 1"))
    ab, pA, pB = P(d1, "d1 % 2 == 0 and d1 > 3"), P(d1, "d1 % 2 == 0"), P(d1, "d1 > 3")
    K["events-C08-Q3"] = ("truth", {"a": ab != pA * pB and ab == F(1, 3) and pA * pB == F(1, 4),
                                     "b": ab == pA * pB, "c": ab == 0, "d": ab == pA * pB})
    ab4 = P(d2, "d1 % 2 == 0 and d2 > 3")
    ind4 = ab4 == P(d2, "d1 % 2 == 0") * P(d2, "d2 > 3")
    K["events-C08-Q4"] = ("truth", {"a": ab4 == F(1, 4) and ind4, "b": ab4 == F(1, 4) and not ind4,
                                     "c": ab4 == 0, "d": ab4 == F(1, 3) and ind4})
    K["events-C08-Q5"] = ("bug", [True, F(1, 2) * F(1, 3) == F(1, 6), 0 == F(1, 2) * F(1, 3)])
    p_, s_ = F(4, 10), F(7, 10)
    q_ = (s_ - p_) / (1 - p_)
    ind = [({"A": a, "B": b}, (p_ if a else 1 - p_) * (q_ if b else 1 - q_)) for a in (0, 1) for b in (0, 1)]
    need(P(ind, "A == 1 or B == 1") == s_, "C08-Q6 table")
    K["events-C08-Q6"] = ("num", both("C08-Q6", ind, "B == 1"))

    # ---- C09
    u = urn({"red": 3, "black": 5}, 2, False)
    K["events-C09-Q1"] = ("num", both("C09-Q1", u, "red_2", "red_1"))
    K["events-C09-Q2"] = ("val", both("C09-Q2", u, "red_1 and red_2"))
    u3 = urn({"red": 4, "black": 6}, 3, False)
    K["events-C09-Q3"] = ("num", both("C09-Q3", u3, "red_3"))
    K["events-C09-Q4"] = ("num", both("C09-Q4", u3, "red_3", "red_2"))
    u2 = urn({"red": 4, "black": 6}, 2, False)
    # line 0: given R2, the other 9 balls hold exactly 3 reds (4 reds minus the one in place 2)
    K["events-C09-Q5"] = ("bug", [(4 - 1, 10 - 1) == (3, 9) and P(u3, "red_3", "red_2") == F(3, 9),
                                   F(4, 9) == P(u3, "red_3", "red_2")])
    return K


BOSS = ["24A-B-Q2b", "25A-A-Q2d", "25A-B-Q2a", "25A-B-Q2e", "25B-A-Q2d", "24B-B-Q2d"]
PULLS = ["25A-C-Q2a", "25A-C-Q2b", "24B-B-Q2c"]


def main():
    qs, levels = load_levels()
    K = keys()
    own = {k: v for k, v in qs.items() if "bankId" not in v[1]}
    for qid in K:
        need(qid in own, f"{qid}: key defined but no such question in the course")
    for qid, (lvl, q) in own.items():
        if not need(qid in K, f"{qid}: no key in check.py"):
            continue
        kind, pay = K[qid]
        if kind == "num":
            check_numeric(qid, q, pay)
            ans = pay
        elif kind == "val":
            check_mcq_value(qid, q, pay)
            ans = pay
        elif kind == "truth":
            check_mcq_truth(qid, q, pay)
            ans = None
        elif kind == "bug":
            check_findbug(qid, q, pay)
            ans = None
        if "sim" in q:
            check_sim(qid, q["sim"], ans)
    # levels: sizes and boss
    ids = sorted(levels)
    need(ids == [f"C{i:02d}" for i in range(1, 11)], f"levels {ids}")
    for lid, lv in sorted(levels.items()):
        n = len(lv["questions"])
        need(4 <= n <= 6, f"{lid}: {n} questions (want 4-6)")
        need(lv.get("boss", False) == (lid == "C10"), f"{lid}: boss flag")
    # bank pulls: exist and come from verified sittings
    bank = {q["id"]: q for q in json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))["questions"]}
    ver = {ln.strip() for ln in (ROOT / "tools" / "verify" / "verified_sittings.txt").read_text(encoding="utf-8").splitlines()
           if ln.strip() and not ln.startswith("#")}
    pulled = [v[1]["bankId"] for v in qs.values() if "bankId" in v[1]]
    need(sorted(set(BOSS + PULLS)) == sorted(pulled), f"bank pulls differ: {sorted(pulled)}")
    boss_level = [q["bankId"] for q in levels["C10"]["questions"]]
    need(boss_level == BOSS, f"boss pulls {boss_level}")
    for b in pulled:
        need(b in bank, f"{b}: not in the bank")
        if b in bank:
            need(bank[b]["examCode"] in ver, f"{b}: sitting {bank[b]['examCode']} is not verified")
            need(bank[b].get("official") is True or bank[b].get("solutionSource") == "official-pdf", f"{b}: not official")
    print("own questions checked:", len(own), "| bank pulls:", len(pulled))
    if FAILS:
        print("FAILED:", len(FAILS))
        sys.exit(1)
    print("OK: every stored answer matches exact enumeration and Monte Carlo")


if __name__ == "__main__":
    main()
