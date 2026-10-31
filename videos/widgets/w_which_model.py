# -*- coding: utf-8 -*-
"""Model-choice widgets for the הסתברות videos of course `which_model` (W01..W09), plus the exact checks the scripts
assert with. Every CSS class is prefixed wm- so other courses are untouched.

Exact math (sympy Rationals; e stays symbolic):
  binom(n, p, k)  hyp(N, D, n, k)  geo(p, k)  nbin(m, p, k)  pois(lam, k)     exact pmfs (Hyp(N, D, n) as in the lesson)
  agree_lib()                       the pmfs above agree with the course checker's lib.py on a grid (asserted at import)
  mc(gen, checks, n, seed)          Monte Carlo of the literal story (numpy): each mean within 5 SE of the exact value
  eq(a, b)   frac(v) -> TeX   dec(v, nd) -> "0.432" (asserts the rounding is honest: |v - shown| < half a unit)

Stage widgets (HTML / SVG; SVG never contains TeX, labels are plain unicode text):
  checklist(pfx, rows)      the decision checklist: rows = [(key, question html, verdict html)].
       ids {pfx}-r-<key> row, {pfx}-on-<key> lit (teal), {pfx}-no-<key> ruled out (dim red), {pfx}-a-<key> the verdict
  bars(pfx, ks, series)     PMF bar chart, series = [(name, {k: value}, cls, legend)], cls a | b | w (teal, blue, amber).
       ids {pfx}-s-<name> a whole series (hidden), {pfx}-v-<name>-<k> a value label (hidden), {pfx}-c-<k> column glow
  seq(pfx, toks)            a row of trials: toks = [(text, cls)], cls s (success) | f (failure) | n (neutral).
       ids {pfx}-c-<i> cell (hidden unless shown), {pfx}-h-<i> teal ring, {pfx}-w-<i> amber ring, {pfx}-n-<i> number
  urn(pfx, balls)           balls = ['r', 'k', 'b', ...]: ids {pfx}-k<i> ball, {pfx}-h<i> ring, {pfx}-x<i> taken out
  groups(pfx, sizes)        boxes of dots (families, boxes of screws): ids {pfx}-g<i> box, {pfx}-gh<i> box glow,
       {pfx}-gd<i> all dots of box i lit, {pfx}-gl<i> the label under box i
  timeline(pfx, times, T)   events on a time axis [0, T]: ids {pfx}-ev (the events), {pfx}-evm (the marked ones,
       marked=[bool per event]), {pfx}-win-<name> window
       (add with windows=[(name, a, b, text)]), {pfx}-cnt-<name> the count label of a window
  eqs(pfx, lines)  chip(id, html, kind)  stem(qid, html)  box(id, html)  pill(id, html)
"""
import html as _html
import math

import numpy as np
import sympy as sp

R = sp.Rational
E = sp.E


# ---------------------------------------------------------------- exact pmfs
def _r(v):
    return sp.nsimplify(v) if not isinstance(v, sp.Basic) else v


def binom(n, p, k):
    p = _r(p)
    return sp.binomial(n, k) * p ** k * (1 - p) ** (n - k) if 0 <= k <= n else sp.Integer(0)


def hyp(N, D, n, k):
    if k < 0 or k > min(D, n) or n - k > N - D or n - k < 0:
        return sp.Integer(0)
    return sp.Rational(sp.binomial(D, k) * sp.binomial(N - D, n - k), sp.binomial(N, n))


def geo(p, k):
    p = _r(p)
    return (1 - p) ** (k - 1) * p if k >= 1 else sp.Integer(0)


def nbin(m, p, k):
    p = _r(p)
    return sp.binomial(k - 1, m - 1) * p ** m * (1 - p) ** (k - m) if k >= m else sp.Integer(0)


def pois(lam, k):
    lam = _r(lam)
    return sp.exp(-lam) * lam ** k / sp.factorial(k)


def eq(a, b):
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


def agree_lib():
    """the exact pmfs agree with the course checker's own lib.py (tools/verify/needhelp/which_model/lib.py)"""
    from fractions import Fraction as F
    from which_model import lib
    for n in range(1, 8):
        for k in range(0, n + 1):
            assert binom(n, R(2, 7), k) == sp.Rational(str(lib.bin_pmf(n, F(2, 7), k)))
            assert hyp(12, 5, n, k) == sp.Rational(str(lib.hyp_pmf(12, 5, n, k)))
            assert nbin(min(n, 3), R(1, 3), k + 3) == sp.Rational(str(lib.nb_pmf(min(n, 3), F(1, 3), k + 3)))
        assert geo(R(1, 6), n) == sp.Rational(str(lib.geo_pmf(F(1, 6), n)))
        assert abs(float(pois(R(5, 2), n)) - lib.poi_pmf(2.5, n)) < 1e-15
    return True


assert agree_lib()


def mc(gen, checks, n=400_000, seed=7):
    """gen(rng, n) -> {name: numpy array}; checks: [(label, f(d) -> array, exact)]: mean of f within 5 SE of exact"""
    rng = np.random.default_rng(seed)
    d = gen(rng, n)
    for label, f, exact in checks:
        v = np.asarray(f(d), dtype=float)
        m, se = v.mean(), v.std() / np.sqrt(len(v))
        assert abs(m - float(exact)) <= 5 * se + 1e-9, (label, m, float(exact), se)
    return True


# ---------------------------------------------------------------- formatting
def frac(v):
    v = sp.nsimplify(v)
    assert v.is_Rational, v
    if v.q == 1:
        return str(v.p)
    s = "-" if v < 0 else ""
    return f"{s}\\frac{{{abs(v.p)}}}{{{v.q}}}"


def dec(v, nd=3):
    """a value shown with nd decimals (trailing zeros dropped); asserts the shown text is the honest rounding"""
    f = float(sp.N(v, 30))
    s = f"{f:.{nd}f}"
    assert abs(f - float(s)) <= 0.5 * 10 ** (-nd) + 1e-15, (v, s)
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s


def esc(s):
    return _html.escape(str(s), quote=True)


# ---------------------------------------------------------------- widgets
def checklist(pfx, rows, size=30, hidden=False, width=660):
    out = []
    for key, q, a in rows:
        out.append(f'<div class="wm-row{" h" if hidden else ""}" id="{pfx}-r-{key}">'
                   f'<i id="{pfx}-on-{key}" class="wm-lit h"></i><i id="{pfx}-no-{key}" class="wm-lit k-no h"></i>'
                   f'<span class="wm-q">{q}</span><span id="{pfx}-a-{key}" class="wm-a h">{a}</span></div>')
    return f'<div class="wm-ck" id="{pfx}" style="font-size:{size}px;width:{width}px">{"".join(out)}</div>'


def bars(pfx, ks, series, w=920, h=430, ymax=None, nd=3, klab=None, shown=(), vals=True, fs=24, title=None):
    """series = [(name, {k: exact or float}, cls, legend text)]. Bars of one k sit side by side."""
    klab = klab or {k: str(k) for k in ks}
    ymax = ymax or max(float(sp.N(v)) for _, d, _, _ in series for v in d.values()) * 1.18
    L, Rm, T, B = 30, 20, 58 if title is None else 92, 50
    pw, ph = w - L - Rm, h - T - B
    gw = pw / len(ks)
    ns = len(series)
    bw = min(64, gw * 0.78 / ns)
    o = [f'<svg class="wm-bars" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">']
    if title:
        o.append(f'<text x="{w / 2}" y="34" class="wm-btitle">{esc(title)}</text>')
    for i, k in enumerate(ks):
        cx = L + gw * (i + 0.5)
        o.append(f'<rect id="{pfx}-c-{k}" class="wm-colhi h" x="{cx - gw / 2 + 4:.1f}" y="{T - 8}" '
                 f'width="{gw - 8:.1f}" height="{ph + 8 + 44}" rx="10"/>')
    o.append(f'<line x1="{L}" y1="{T + ph}" x2="{L + pw}" y2="{T + ph}" class="wm-axis"/>')
    for i, k in enumerate(ks):
        cx = L + gw * (i + 0.5)
        o.append(f'<text x="{cx:.1f}" y="{T + ph + 36}" class="wm-klab">{esc(klab[k])}</text>')
    for j, (name, d, cls, legend) in enumerate(series):
        hid = "" if name in shown else " h"
        g = [f'<g id="{pfx}-s-{name}" class="wm-ser k-{cls}{hid}">']
        lx = L + 10 + j * (pw / max(ns, 1))
        if legend:
            g.append(f'<rect x="{lx:.1f}" y="{T - 46}" width="26" height="26" rx="5" class="wm-bar"/>'
                     f'<text x="{lx + 36:.1f}" y="{T - 25}" class="wm-leg">{esc(legend)}</text>')
        for i, k in enumerate(ks):
            v = float(sp.N(d.get(k, 0)))
            bh = ph * v / ymax
            x0 = L + gw * (i + 0.5) - ns * bw / 2 + j * bw
            g.append(f'<rect x="{x0 + 3:.1f}" y="{T + ph - bh:.1f}" width="{bw - 6:.1f}" height="{max(bh, 0):.1f}" rx="4" class="wm-bar"/>')
            if vals:
                g.append(f'<text id="{pfx}-v-{name}-{k}" x="{x0 + bw / 2:.1f}" y="{T + ph - bh - 10:.1f}" '
                         f'class="wm-val h" font-size="{fs}">{dec(d.get(k, 0), nd)}</text>')
        g.append("</g>")
        o += g
    o.append("</svg>")
    return "".join(o)


def seq(pfx, toks, size=56, shown=False, nums=True, gap=10, fs=None, wide=None):
    out = []
    for i, (t, cls) in enumerate(toks):
        n = f'<span id="{pfx}-n-{i}" class="wm-sn">{i + 1}</span>' if nums else ""
        out.append(f'<span id="{pfx}-c-{i}" class="wm-sc k-{cls}{"" if shown else " h"}" style="width:{wide or size}px;height:{size}px;'
                   f'font-size:{fs or size * 0.5:.0f}px"><i id="{pfx}-h-{i}" class="wm-ring h"></i>'
                   f'<i id="{pfx}-w-{i}" class="wm-ring k-w h"></i><b>{t}</b>{n}</span>')
    return f'<div class="wm-seq" id="{pfx}" style="gap:{gap}px">{"".join(out)}</div>'


def urn(pfx, balls, size=46, per_row=8, label=None, hidden=False):
    out = []
    for i, c in enumerate(balls):
        out.append(f'<span id="{pfx}-k{i}" class="wm-ball k-{c}" style="width:{size}px;height:{size}px">'
                   f'<i id="{pfx}-h{i}" class="wm-ring h"></i><i id="{pfx}-x{i}" class="wm-out h"></i></span>')
    lab = f'<div class="wm-ulab">{label}</div>' if label else ""
    return (f'<div class="wm-urn{" h" if hidden else ""}" id="{pfx}"><div class="wm-ubody" '
            f'style="max-width:{per_row * (size + 10) + 30}px">{"".join(out)}</div>{lab}</div>')


def groups(pfx, sizes, labels=None, dot=22, per_row=4, hidden=False):
    labels = labels or [str(s) for s in sizes]
    out = []
    for i, s in enumerate(sizes):
        dots = "".join(f'<span class="wm-dot" style="width:{dot}px;height:{dot}px"></span>' for _ in range(s))
        cols = min(s, per_row)
        wbox = cols * (dot + 6) + 6
        out.append(f'<div class="wm-gwrap{" h" if hidden else ""}" id="{pfx}-g{i}"><div class="wm-gbox" style="width:{wbox}px">'
                   f'<i id="{pfx}-gh{i}" class="wm-ghl h"></i>'
                   f'<div class="wm-gdots" style="grid-template-columns:repeat({cols},{dot}px)">{dots}</div>'
                   f'<i id="{pfx}-gd{i}" class="wm-glit h"></i>'
                   f'</div><div id="{pfx}-gl{i}" class="wm-glab">{labels[i]}</div></div>')
    return f'<div class="wm-groups" id="{pfx}">{"".join(out)}</div>'


def timeline(pfx, times, T, windows=(), w=940, h=210, ticks=None, marked=None):
    L, Rm = 30, 30
    pw = w - L - Rm
    X = lambda t: L + pw * t / T
    y = 120
    o = [f'<svg class="wm-tl" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">']
    for name, a, b, text in windows:
        o.append(f'<g id="{pfx}-win-{name}" class="h"><rect x="{X(a):.1f}" y="{y - 70}" width="{X(b) - X(a):.1f}" height="100" '
                 f'rx="10" class="wm-win"/></g>')
        cnt = sum(1 for t in times if a < t <= b)
        o.append(f'<text id="{pfx}-cnt-{name}" x="{(X(a) + X(b)) / 2:.1f}" y="{y - 80}" class="wm-cnt h">{esc(text.format(n=cnt))}</text>')
    o.append(f'<line x1="{L}" y1="{y}" x2="{L + pw}" y2="{y}" class="wm-axis"/>')
    for t, s in (ticks or [(0, "0"), (T, str(T))]):
        o.append(f'<line x1="{X(t):.1f}" y1="{y - 8}" x2="{X(t):.1f}" y2="{y + 8}" class="wm-axis"/>'
                 f'<text x="{X(t):.1f}" y="{y + 44}" class="wm-klab">{esc(s)}</text>')
    o.append(f'<g id="{pfx}-ev" class="h">' + "".join(
        f'<circle cx="{X(t):.1f}" cy="{y}" r="11" class="wm-ev"/>' for t in times) + "</g>")
    if marked:      # a second layer: the marked events (e.g. the ones that pass a filter), drawn bigger in amber
        o.append(f'<g id="{pfx}-evm" class="h">' + "".join(
            f'<circle cx="{X(t):.1f}" cy="{y}" r="15" class="wm-ev k-m"/>' for t, m in zip(times, marked) if m) + "</g>")
    o.append("</svg>")
    return "".join(o)


def eqs(pfx, lines, size=36, gap=10, shown=0):
    rows = "".join(f'<div id="{pfx}-{i}" class="wm-eq{"" if i < shown else " h"}">{s}</div>' for i, s in enumerate(lines))
    return f'<div class="wm-eqs" style="font-size:{size}px;gap:{gap}px">{rows}</div>'


def chip(id_, html_, kind="ok", hidden=True):
    return f'<div id="{id_}" class="wm-chip {kind}{" h" if hidden else ""}">{html_}</div>'


def pill(id_, html_, hidden=True):
    """the model's name, big"""
    return f'<div id="{id_}" class="wm-pill{" h" if hidden else ""}">{html_}</div>'


def stem(qid, html_, size=30):
    return f'<div class="qstem" style="font-size:{size}px"><span class="qid">{esc(qid)}</span>{html_}</div>'


def box(id_, html_, size=30, hidden=True):
    return f'<div id="{id_}" class="wm-box{" h" if hidden else ""}" style="font-size:{size}px">{html_}</div>'


_CTX = None


def ctx_text(q):
    """the shared statement (context) of a bank question, '' if it has none"""
    global _CTX
    if _CTX is None:
        import json, pathlib
        _CTX = json.loads((pathlib.Path(__file__).resolve().parents[2] / "questions.json").read_text(encoding="utf-8"))["contexts"]
    c = _CTX.get(q.get("contextId"), {})
    return c.get("text") or c.get("caption") or ""
