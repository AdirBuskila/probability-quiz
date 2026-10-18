# -*- coding: utf-8 -*-
"""Figures for the guided course `pdf`, drawn from the SAME data as check.py (pdfdata.py).
Run:  PYTHONUTF8=1 py tools/verify/needhelp/pdf/figs.py      -> images/exams/crs-pdf-*.png
Latin-only labels (no bidi trouble). Output is ASCII only."""
import pathlib, sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pdfdata as D  # noqa: E402

OUT = HERE.parents[2].parent / "images" / "exams"
INK, GRID, BLUE, FILL = "#1f2937", "#d1d5db", "#2563eb", "#bfdbfe"
RED = "#dc2626"
plt.rcParams.update({"font.size": 12, "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
                     "text.color": INK, "mathtext.fontset": "cm"})


def fn(pdf):
    return D.fnum(pdf)


def style(ax, xlim, ylim, xl="$x$", yl="$f(x)$"):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl, rotation=0, labelpad=18)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def pdf_line(ax, pdf, color=BLUE):
    """draw each piece as a segment; vertical edges where the density jumps"""
    f = fn(pdf)
    for lo, hi, e in pdf:
        xs = np.linspace(float(lo), float(hi), 400)
        ys = np.array([float(e.subs(D.x, v)) for v in xs])
        ax.plot(xs, ys, color=color, lw=2.4)
    for lo, hi, e in pdf:
        for edge in (lo, hi):
            pass
    # edges to zero at the support ends and jumps between pieces
    edges = sorted({float(p[0]) for p in pdf} | {float(p[1]) for p in pdf})
    for xv in edges:
        left = sum(float(e.subs(D.x, xv)) for lo, hi, e in pdf if float(hi) == xv)
        right = sum(float(e.subs(D.x, xv)) for lo, hi, e in pdf if float(lo) == xv)
        if abs(left - right) > 1e-12:
            ax.plot([xv, xv], [left, right], color=color, lw=2.4)
    lo0, hi1 = edges[0], edges[-1]
    ax.plot([lo0 - 5, lo0], [0, 0], color=color, lw=2.4)
    ax.plot([hi1, hi1 + 5], [0, 0], color=color, lw=2.4)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


def cdf_vals(pdf, ts):
    return np.array([float(D.cdf_at(pdf, D.sp.nsimplify(v))) for v in ts])


def main():
    # ---- L1: area under f = 2x is a probability
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    xs = np.linspace(0.5, 1, 100)
    ax.fill_between(xs, 2 * xs, color=FILL, label="$P(\\frac12<X<1)$")
    pdf_line(ax, D.PDFS["tri"])
    style(ax, (-0.3, 1.4), (0, 2.3))
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["0", "1/2", "1"])
    ax.set_yticks([0, 1, 2])
    ax.text(0.78, 0.55, "shaded area\n= probability", ha="center", fontsize=11)
    save(fig, "crs-pdf-l1-area.png")

    # ---- L5: master pdf P1 and its CDF
    P1 = D.PDFS["P1"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.3), gridspec_kw={"wspace": 0.4})
    pdf_line(a1, P1)
    a1.fill_between(np.linspace(0, 1, 50), np.linspace(0, 1, 50), color=FILL)
    a1.fill_between(np.linspace(1, 2, 50), 0.5, color=FILL)
    style(a1, (-0.5, 2.5), (0, 1.25))
    a1.set_xticks([0, 1, 2])
    a1.set_title("density $f_X$", fontsize=12)
    ts = np.linspace(-0.5, 2.5, 601)
    ys = cdf_vals(P1, ts)
    a2.plot(ts, ys, color=RED, lw=2.4)
    style(a2, (-0.5, 2.5), (0, 1.15), xl="$t$", yl="$F_X(t)$")
    a2.set_xticks([0, 1, 2])
    a2.set_yticks([0, 0.5, 1])
    a2.set_yticklabels(["0", "1/2", "1"])
    a2.plot([1], [0.5], "o", color=RED)
    a2.set_title("cumulative $F_X$", fontsize=12)
    save(fig, "crs-pdf-l5-pdf-cdf.png")

    # ---- L5 question: four candidate graphs for F of P1 (A is right)
    ts = np.linspace(-0.5, 2.5, 601)

    def small(name, segs, extra=None):
        fig, ax = plt.subplots(figsize=(3.4, 2.5))
        for xs_, ys_ in segs:
            ax.plot(xs_, ys_, color=BLUE, lw=2.4)
        style(ax, (-0.5, 2.5), (-0.1, 1.5), xl="$t$", yl="")
        ax.set_xticks([0, 1, 2])
        ax.set_yticks([0, 0.5, 1])
        ax.set_yticklabels(["0", "1/2", "1"])
        save(fig, name)

    def seg(a, b, f):
        xs_ = np.linspace(a, b, 200)
        return xs_, f(xs_)
    # A: correct
    small("crs-pdf-l5-optA.png", [seg(-0.5, 0, lambda v: 0 * v), seg(0, 1, lambda v: v**2 / 2), seg(1, 2, lambda v: v / 2),
                                  seg(2, 2.5, lambda v: 0 * v + 1)][:3] + [seg(2, 2.5, lambda v: 0 * v + 1)])
    # B: forgot to accumulate: second piece (t-1)/2 -> jumps down to 0 at t=1
    small("crs-pdf-l5-optB.png", [seg(-0.5, 0, lambda v: 0 * v), seg(0, 1, lambda v: v**2 / 2), seg(1, 2, lambda v: (v - 1) / 2),
                                  seg(2, 2.5, lambda v: 0 * v + 0.5)])
    # C: kept t^2/2 on the second piece -> climbs above 1
    small("crs-pdf-l5-optC.png", [seg(-0.5, 0, lambda v: 0 * v), seg(0, 2, lambda v: v**2 / 2), seg(2, 2.5, lambda v: 0 * v + 2)])
    # D: the density drawn instead of the CDF
    small("crs-pdf-l5-optD.png", [seg(-0.5, 0, lambda v: 0 * v), seg(0, 1, lambda v: v), seg(1, 2, lambda v: 0 * v + 0.5),
                                  seg(2, 2.5, lambda v: 0 * v)])

    # ---- L8 figure A: trapezoid with unknown height c
    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    ax.fill_between([0, 1], [0, 1], color=FILL)
    ax.fill_between([1, 3], [1, 1], color=FILL)
    ax.plot([-1, 0, 1, 3, 3, 4], [0, 0, 1, 1, 0, 0], color=BLUE, lw=2.4)
    ax.plot([0, 1], [1, 1], ls="--", color=INK, lw=0.8)
    ax.plot([1, 1], [0, 1], ls="--", color=INK, lw=0.8)
    style(ax, (-0.7, 4.2), (0, 1.35))
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["0", "$c$"])
    save(fig, "crs-pdf-l8-trap.png")

    # ---- L8 figure B: tent with unknown apex height h
    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    ax.fill_between([0, 1, 3], [0, 1, 0], color=FILL)
    ax.plot([-1, 0, 1, 3, 4], [0, 0, 1, 0, 0], color=BLUE, lw=2.4)
    ax.plot([0, 1], [1, 1], ls="--", color=INK, lw=0.8)
    ax.plot([1, 1], [0, 1], ls="--", color=INK, lw=0.8)
    style(ax, (-0.7, 4.2), (0, 1.35))
    ax.set_xticks([0, 1, 2, 3])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["0", "$h$"])
    save(fig, "crs-pdf-l8-tent.png")


if __name__ == "__main__":
    main()
