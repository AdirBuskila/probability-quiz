# -*- coding: utf-8 -*-
"""Shared helpers of the "circ" guided course (circuits and reliability).

One circuit description feeds everything, so a picture, a stored answer and a simulation can never describe
different circuits:
  * a TREE:  ("S", [children])  series        ("P", [children])  parallel        ("C", "A")  a component
             ("BR", ("A", "B", "C", "D", "E"))  the bridge: A top-left, B top-right, C bottom-left, D bottom-right,
             E in the middle joining the two middle nodes (undirected, like the exam's Q1)
  * probs:   {"A": Fraction, ...}
  * works(tree, state)            does the circuit work in this 0/1 state
  * prob(tree, probs, event, given)   EXACT probability by enumerating all 2^n component states (Fractions)
  * draw(...) in diagrams.py       the SVG
Output is ASCII only.
"""
import itertools
from fractions import Fraction as Fr


def F(x):
    return x if isinstance(x, Fr) else Fr(str(x))


def S(*kids):
    return ("S", list(kids))


def P(*kids):
    return ("P", list(kids))


def C(i):
    return ("C", i)


def BR(a="A", b="B", c="C", d="D", e="E"):
    return ("BR", (a, b, c, d, e))


def comps(tree):
    k, v = tree
    if k == "C":
        return [v]
    if k == "BR":
        return [v[0], v[1], v[2], v[3], v[4]]
    out = []
    for ch in v:
        out += comps(ch)
    return out


def works(tree, st):
    """Works for python bools and for numpy bool arrays alike (only & and | are used)."""
    k, v = tree
    if k == "C":
        return st[v]
    if k == "S":
        r = works(v[0], st)
        for ch in v[1:]:
            r = r & works(ch, st)
        return r
    if k == "P":
        r = works(v[0], st)
        for ch in v[1:]:
            r = r | works(ch, st)
        return r
    if k == "BR":
        a, b, c, d, e = (st[x] for x in v)
        return (a & b) | (c & d) | (a & e & d) | (c & e & b)
    raise ValueError(k)


def prob(event, probs, given=None):
    """event, given: callables state-dict -> bool. Exact Fraction by enumeration over the ids in probs."""
    ids = sorted(probs)
    num = den = Fr(0)
    for bits in itertools.product((0, 1), repeat=len(ids)):
        st = {i: bool(x) for i, x in zip(ids, bits)}
        w = Fr(1)
        for i in ids:
            w *= probs[i] if st[i] else 1 - probs[i]
        if w == 0:
            continue
        if given is None or given(st):
            den += w
            if event(st):
                num += w
    if den == 0:
        raise ZeroDivisionError("given has probability 0")
    return num / den


def circ_prob(tree, probs, given=None, event=None):
    ev = event or (lambda st: works(tree, st))
    return prob(ev, probs, given)


def same(ids, p):
    p = F(p)
    return {i: p for i in ids}


def sim_network(tree, probs):
    """The sim.js `network` (series/parallel) or `edges` (bridge) params for this circuit, as a dict."""
    def node(t):
        k, v = t
        if k == "C":
            return {"type": "comp", "id": v, "p": float(probs[v])}
        return {"type": "series" if k == "S" else "parallel", "children": [node(c) for c in v]}
    if tree[0] == "BR":
        a, b, c, d, e = tree[1]
        pr = lambda x: float(probs[x])
        return {"edges": [{"id": a, "from": "L", "to": "T", "p": pr(a)}, {"id": b, "from": "T", "to": "R", "p": pr(b)},
                          {"id": c, "from": "L", "to": "U", "p": pr(c)}, {"id": d, "from": "U", "to": "R", "p": pr(d)},
                          {"id": e, "from": "T", "to": "U", "p": pr(e)}], "source": "L", "sink": "R"}
    return {"network": node(tree)}
