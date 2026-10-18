# -*- coding: utf-8 -*-
"""Small helpers shared by the step-author data files tools/gen/steps_<CODE>.py (probability app).

A steps file builds DATA = {(num, part): item(...)} and the generator calls apply(questions, DATA) just before the
exam dict is written. Every expected value stored here is re-derived independently (exact fractions / sympy and
Monte Carlo) in tools/verify/<CODE>/steps_check.py, which reads the raw JSON back and compares.
"""
import math
from fractions import Fraction

LETTERS = "abcdefgh"


def _tol(ans):
    """Default tolerance for a numeric step: exact when the stored value has <= 3 decimals, else 0.2% relative."""
    if round(ans, 3) == ans:
        return 0
    return max(abs(ans) * 0.002, 1e-6)


def num(prompt, ans, explain, tol=None, region=None):
    a = float(ans)
    s = {"type": "numeric", "prompt": prompt, "answer": a, "tol": _tol(a) if tol is None else tol, "explain": explain}
    if region is not None:
        s["region"] = region
    return s


def choice(prompt, options, ok, explain, math_opts=False, region=None):
    """options: list of strings (TeX without $ when math_opts); ok: index of the single correct option."""
    assert 0 <= ok < len(options) and 2 <= len(options) <= 5
    opts = []
    for i, v in enumerate(options):
        o = {"id": LETTERS[i], "value": v}
        if math_opts:
            o["type"] = "math"
        opts.append(o)
    s = {"type": "choice", "prompt": prompt, "options": opts, "correctId": LETTERS[ok], "explain": explain}
    if region is not None:
        s["region"] = region
    return s


def item(rubric, pitfalls, steps):
    """rubric: list of (text, points)."""
    return {"rubric": [{"text": t, "points": p} for t, p in rubric], "pitfalls": list(pitfalls), "steps": list(steps)}


def apply(questions, data, code):
    seen = set()
    for q in questions:
        k = (q["num"], q.get("part"))
        if k not in data:
            continue
        d = data[k]
        tot = sum(r["points"] for r in d["rubric"])
        assert "points" not in q or abs(tot - q["points"]) < 1e-9, f"{code} Q{k}: rubric sum {tot} != points {q['points']}"
        assert 2 <= len(d["steps"]) <= 5, f"{code} Q{k}: {len(d['steps'])} steps"
        q["rubric"] = d["rubric"]
        q["pitfalls"] = d["pitfalls"]
        q["steps"] = d["steps"]
        q.update({"rubricSource": "ai-draft", "stepsSource": "ai-draft"})
        seen.add(k)
    missing = set(data) - seen
    assert not missing, f"{code}: steps for unknown items {missing}"
    return len(seen)
