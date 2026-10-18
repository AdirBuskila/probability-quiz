# -*- coding: utf-8 -*-
"""Draws the pdf/CDF sketches used by docs/briefs/11 - pdf_constants.md (own figures, ASCII labels only).
Run: PYTHONUTF8=1 py tools/verify/learn/make_figs.py   -> images/exams/learn-*.png"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "images", "exams"))
INK = "#1f2937"
ACC = "#c2410c"
FILL = "#fdba74"


def style(ax, xlabel):
    ax.set_xlabel(xlabel, color=INK)
    ax.grid(True, color="#e5e7eb", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK)


def fig_two(path, xs_pdf, f, xs_cdf, F, pdf_title, cdf_title, xticks, pdf_pts=None, cdf_pts=None, ylim_pdf=None):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.2), dpi=150)
    fig.patch.set_facecolor("white")
    for seg in xs_pdf:
        x = np.linspace(seg[0], seg[1], 200)
        y = f(x)
        a1.plot(x, y, color=ACC, lw=2.2)
        a1.fill_between(x, 0, y, color=FILL, alpha=0.45)
    a1.set_title(pdf_title, color=INK, fontsize=11)
    style(a1, "x")
    a1.set_xticks(xticks)
    if ylim_pdf:
        a1.set_ylim(*ylim_pdf)
    for seg in xs_cdf:
        x = np.linspace(seg[0], seg[1], 200)
        a2.plot(x, F(x), color=ACC, lw=2.2)
    a2.set_title(cdf_title, color=INK, fontsize=11)
    style(a2, "t")
    a2.set_xticks(xticks)
    a2.set_ylim(-0.05, 1.08)
    if pdf_pts:
        for (x, y, lab) in pdf_pts:
            a1.plot([x], [y], "o", color=INK, ms=4)
            a1.annotate(lab, (x, y), textcoords="offset points", xytext=(5, 5), color=INK, fontsize=9)
    if cdf_pts:
        for (x, y, lab) in cdf_pts:
            a2.plot([x], [y], "o", color=INK, ms=4)
            a2.annotate(lab, (x, y), textcoords="offset points", xytext=(5, -13), color=INK, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, facecolor="white")
    plt.close(fig)


# Example 1 (piecewise constant + exponential tail): f = 2/3 on [-1,0), (1/3)e^{-x} for x >= 0
def f1(x):
    return np.where(x < 0, 2 / 3, np.exp(-np.clip(x, 0, None)) / 3)


def F1(x):
    return np.where(x < 0, 2 / 3 * (x + 1), 1 - np.exp(-np.clip(x, 0, None)) / 3)


fig_two(os.path.join(OUT, "learn-pdf-ex1.png"), [(-1, 0), (0, 4)], f1, [(-1.8, -1), (-1, 0), (0, 4)],
        lambda x: np.where(x < -1, 0.0, F1(x)),
        "pdf f(x): 2/3 on [-1,0), (1/3)e^(-x) for x>=0", "CDF F(t): line up to 2/3, then 1-(1/3)e^(-t)",
        [-1, 0, 1, 2, 3, 4], pdf_pts=[(0, 2 / 3, "2/3"), (0, 1 / 3, "1/3")], cdf_pts=[(0, 2 / 3, "2/3")], ylim_pdf=(0, 0.8))

# Example 2 (graph form): f = x on (0,1), 1 on (1,3/2)
fig_two(os.path.join(OUT, "learn-pdf-ex2.png"), [(0, 1), (1, 1.5)], lambda x: np.where(x < 1, x, 1.0),
        [(-0.5, 0), (0, 1), (1, 1.5), (1.5, 2.0)],
        lambda x: np.where(x < 0, 0.0, np.where(x < 1, x * x / 2, np.where(x < 1.5, x - 0.5, 1.0))),
        "pdf f(x): rises from 0 to 1, then flat to 3/2", "CDF F(t): t^2/2, then t-1/2, then 1",
        [0, 0.5, 1, 1.5, 2], pdf_pts=[(1, 1, "1")], cdf_pts=[(1, 0.5, "1/2"), (1.5, 1, "1")], ylim_pdf=(0, 1.3))

# Example 3: triangle pdf a(b-|x|) with b=2, a=1/4
fig_two(os.path.join(OUT, "learn-pdf-ex3.png"), [(-2, 0), (0, 2)], lambda x: (2 - np.abs(x)) / 4,
        [(-3, -2), (-2, 0), (0, 2), (2, 3)],
        lambda x: np.where(x < -2, 0.0, np.where(x < 0, (x + 2) ** 2 / 8, np.where(x < 2, 1 - (2 - x) ** 2 / 8, 1.0))),
        "pdf f(x) = (2-|x|)/4 on [-2,2]", "CDF F(t): (t+2)^2/8, then 1-(2-t)^2/8",
        [-2, -1, 0, 1, 2], pdf_pts=[(0, 0.5, "1/2")], cdf_pts=[(0, 0.5, "1/2")], ylim_pdf=(0, 0.65))
print("figures written to " + OUT)
