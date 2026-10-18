# -*- coding: utf-8 -*-
"""Shared helper for tools/verify/<CODE>/steps_check.py (probability app).

Reads tools/raw/<CODE>.json and compares every machine-checkable guided step with an INDEPENDENT computation
(fractions / enumeration / sympy, plus Monte Carlo where a simulation applies). ASCII output only.

    c = Chk("26A-A")
    c.num("Q1a", 2, exact=Fraction(5, 48), mc=(est, se))     # numeric step: stored answer == exact; MC within 4 SE
    c.formula("Q2b", 2, truth_fn, {"a": fn_a, "b": fn_b, ...}, samples)   # choice step whose options are formulas
    c.vals("Q1b", 0, {"a": value_a, ...}, truth)              # choice step: each option's computed value; only the
                                                              # correct one equals `truth`
    c.fact("Q1e", 1, "description", bool_expr)                # any other checked claim
    c.finish()
"""
import json
import math
import pathlib
import sys

HEB = "אבגדהוזחטיכלמנסעפצקרשת"
FOLD = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}


def part_key(part):
    part = FOLD.get(part, part)
    return chr(ord("a") + HEB.index(part)) if part in HEB else part


class Chk:
    def __init__(self, code):
        self.code = code
        root = pathlib.Path(__file__).resolve().parents[2]
        data = json.loads((root / "tools" / "raw" / f"{code}.json").read_text(encoding="utf-8"))
        self.items = {}
        for q in data["questions"]:
            self.items[f"Q{q['num']}{part_key(q['part']) if q.get('part') else ''}"] = q
        self.rows = []
        self.used = set()

    def _step(self, key, idx, typ):
        q = self.items[key]
        s = q["steps"][idx]
        assert s["type"] == typ, f"{key} step {idx}: type {s['type']} != {typ}"
        self.used.add((key, idx))
        return s

    def _rec(self, key, idx, what, ok, det=""):
        self.rows.append((f"{key}.{idx}", what, bool(ok), det))

    def num(self, key, idx, exact, mc=None, what=""):
        """Numeric step: stored answer must equal the independently computed exact value; mc=(estimate, se)."""
        s = self._step(key, idx, "numeric")
        ex = float(exact)
        self._rec(key, idx, what or "exact", abs(s["answer"] - ex) <= 1e-9 * max(1.0, abs(ex)),
                  "stored=%.9g exact=%.9g tol=%.3g" % (s["answer"], ex, s.get("tol", 0)))
        # the tolerance must still reject a clearly different value: 5% off is a miss
        if ex != 0:
            self._rec(key, idx, "tol small", s.get("tol", 0) < 0.05 * abs(ex), "tol=%.3g" % s.get("tol", 0))
        if mc is not None:
            est, se = mc
            self._rec(key, idx, "MC", abs(est - s["answer"]) <= 4 * se + 1e-12,
                      "mc=%.6f se=%.6f stored=%.6f" % (est, se, s["answer"]))

    def formula(self, key, idx, truth, opts, samples, what="formula options"):
        """Choice step whose options are formulas. opts: {option id: fn(**sample)}; the correct option must match
        `truth` at every sample point and every other option must differ at >= 1 sample point."""
        s = self._step(key, idx, "choice")
        ids = {o["id"] for o in s["options"]}
        self._rec(key, idx, "option ids covered", ids == set(opts), "%s vs %s" % (sorted(ids), sorted(opts)))
        good = s["correctId"]
        for oid, fn in opts.items():
            agree = all(abs(fn(**sm) - truth(**sm)) <= 1e-9 * max(1, abs(truth(**sm))) for sm in samples)
            if oid == good:
                self._rec(key, idx, "correct option %s matches truth" % oid, agree)
            else:
                self._rec(key, idx, "distractor %s differs" % oid, not agree)

    def vals(self, key, idx, optvals, truth, what="option values", tol=1e-9):
        """Choice step where each option has a computed value; the correct one equals truth, the others do not.
        tol: absolute tolerance (use ~3e-3 when the values come from Monte Carlo)."""
        s = self._step(key, idx, "choice")
        ids = {o["id"] for o in s["options"]}
        self._rec(key, idx, "option ids covered", ids == set(optvals), "%s vs %s" % (sorted(ids), sorted(optvals)))
        good = s["correctId"]
        for oid, v in optvals.items():
            same = abs(float(v) - float(truth)) <= tol * max(1.0, abs(float(truth))) if tol <= 1e-9 else abs(float(v) - float(truth)) <= tol
            if oid == good:
                self._rec(key, idx, "correct option %s = truth" % oid, same, "%.6g vs %.6g" % (float(v), float(truth)))
            else:
                self._rec(key, idx, "distractor %s differs" % oid, not same, "%.6g vs %.6g" % (float(v), float(truth)))

    def fact(self, key, idx, what, cond, det=""):
        s = self.items[key]["steps"][idx]
        self.used.add((key, idx))
        self._rec(key, idx, what, cond, det)

    def correct(self, key, idx, letter):
        """Pin the correct option id so a later edit of the generator that moves it is caught."""
        s = self._step(key, idx, "choice")
        self._rec(key, idx, "correctId == %s" % letter, s["correctId"] == letter)

    def finish(self):
        # every numeric / choice step of the sitting must have been looked at by a check
        for key, q in self.items.items():
            for i, s in enumerate(q.get("steps", [])):
                if (key, i) not in self.used:
                    self.rows.append((f"{key}.{i}", "step has no check", False, s["type"]))
        bad = [r for r in self.rows if not r[2]]
        for item, what, ok, det in self.rows:
            print("%-8s %-4s %s | %s" % (item, "ok" if ok else "FAIL", what, det))
        print()
        print("%s steps_check: %d checks, %d failing" % (self.code, len(self.rows), len(bad)))
        sys.exit(1 if bad else 0)
