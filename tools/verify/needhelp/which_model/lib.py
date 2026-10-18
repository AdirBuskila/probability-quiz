# -*- coding: utf-8 -*-
"""Exact helpers for the which_model course (Fractions where the data is rational, floats for Poisson)."""
from fractions import Fraction as F
from math import comb, exp, factorial


def bin_pmf(n, p, k):
    if k < 0 or k > n:
        return 0 * p
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def hyp_pmf(N, D, n, k):
    if k < 0 or k > min(D, n) or n - k > N - D or n - k < 0:
        return F(0)
    return F(comb(D, k) * comb(N - D, n - k), comb(N, n))


def geo_pmf(p, k):
    return (1 - p) ** (k - 1) * p if k >= 1 else 0 * p


def nb_pmf(m, p, k):
    return comb(k - 1, m - 1) * p ** m * (1 - p) ** (k - m) if k >= m else 0 * p


def poi_pmf(lam, k):
    return exp(-lam) * lam ** k / factorial(k)


def poi_probs(lam, K):
    """pmf of Poisson(lam) on 0..K, the tail folded into the last value so that the probabilities sum to 1."""
    ps = [poi_pmf(lam, k) for k in range(K + 1)]
    ps[-1] += 1.0 - sum(ps)
    return ps


def poi_cut(lam, tail=1e-11):
    K = 0
    while 1.0 - sum(poi_pmf(lam, k) for k in range(K + 1)) > tail:
        K += 1
    return K


def thin_poisson_rows(lam, q):
    """Joint table of (n, k): n ~ Poisson(lam), k | n ~ Bin(n, q). Tail beyond the cut folded into the last row."""
    K = poi_cut(lam)
    rows = []
    for n in range(K + 1):
        pn = poi_pmf(lam, n)
        for k in range(n + 1):
            rows.append({"p": pn * float(bin_pmf(n, F(q).limit_denominator(10 ** 6), k)), "n": n, "k": k})
    rows[-1]["p"] += 1.0 - sum(r["p"] for r in rows)
    return rows


def thin_binomial_rows(n, p, q):
    """Joint table of (a, y): a ~ Bin(n, p), y | a ~ Bin(a, q)."""
    p, q = F(p), F(q)
    return [{"p": float(bin_pmf(n, p, a) * bin_pmf(a, q, y)), "a": a, "y": y} for a in range(n + 1) for y in range(a + 1)]


def fmt(x, nd=4):
    """A decimal string without trailing zeros, for the Hebrew explanations."""
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s if s else "0"
