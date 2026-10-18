# -*- coding: utf-8 -*-
"""Shared helpers for the learn-mode number checks (tools/verify/learn/).
Every number printed in docs/briefs/*.md is checked here exactly (fractions / sympy / enumeration / quadrature)
and, for the probabilistic ones, by Monte Carlo as well (4 standard errors). Output is ASCII only."""
import math
import sys
from fractions import Fraction as Fr

import numpy as np

ROWS = []
RNG = np.random.default_rng(20261018)
N_MC = 1_000_000


def chk(name, claimed, computed, tol=1e-12):
    """Exact claim vs independently computed value (Fraction or float)."""
    ok = abs(float(claimed) - float(computed)) <= tol
    ROWS.append((name, ok, "claimed=%.10g computed=%.10g" % (float(claimed), float(computed))))
    return ok


def chk_eq(name, claimed, computed):
    ok = claimed == computed
    ROWS.append((name, ok, "claimed=%s computed=%s" % (claimed, computed)))
    return ok


def chk_mc(name, claimed, estimate, n=N_MC, p=None):
    """Monte Carlo estimate of a probability within 4 SE of the claimed value."""
    q = float(claimed) if p is None else p
    se = math.sqrt(max(q * (1 - q), 1e-12) / n)
    ok = abs(estimate - float(claimed)) <= 4 * se
    ROWS.append((name + " [MC]", ok, "claimed=%.6f mc=%.6f se=%.6f" % (float(claimed), estimate, se)))
    return ok


def chk_mc_val(name, claimed, estimate, se):
    """Monte Carlo estimate of a mean/variance with a given standard error."""
    ok = abs(estimate - float(claimed)) <= 4 * se
    ROWS.append((name + " [MC]", ok, "claimed=%.6f mc=%.6f se=%.6f" % (float(claimed), estimate, se)))
    return ok


def report():
    bad = 0
    for name, ok, info in ROWS:
        print(("OK   " if ok else "FAIL ") + name + "  " + info)
        bad += (not ok)
    print("%d checks, %d failed" % (len(ROWS), bad))
    return bad
