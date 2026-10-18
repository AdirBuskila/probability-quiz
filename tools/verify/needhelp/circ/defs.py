# -*- coding: utf-8 -*-
"""Every circuit of the "circ" course, by name: (tree, probs, show_p). Pictures (diagrams.py) and the exact/Monte
Carlo checks (check.py) both read this table. show_p False = the picture shows only the unit letters."""
from circuits_lib import S, P, C, BR, F, same, comps

CIRCUITS = {}


def add(name, tree, probs=None, p=None, show=True):
    ids = comps(tree)
    if probs is None:
        probs = same(ids, p)
    else:
        probs = {k: F(v) for k, v in probs.items()}
    CIRCUITS[name] = (tree, probs, show)


# level 1 -- series
add("s_ab", S(C("A"), C("B")), {"A": "0.9", "B": "0.8"})
add("s_abc", S(C("A"), C("B"), C("C")), {"A": "0.9", "B": "0.9", "C": "0.5"})
add("s_4", S(C("A"), C("B"), C("C"), C("D")), p="0.9")
add("s_pp", S(C("A"), C("B")), p="0.7", show=False)          # p unknown in the question (inverse problem)
add("s_3", S(C("A"), C("B"), C("C")), p="0.9")
# level 2 -- parallel
add("p_ab", P(C("A"), C("B")), {"A": "0.9", "B": "0.8"})
add("p_abc", P(C("A"), C("B"), C("C")), {"A": "0.5", "B": "0.5", "C": "0.6"})
add("p_2", P(C("A"), C("B")), p="0.6")
add("p_xy", P(C("A"), C("B")), {"A": "0.7", "B": "0.8"}, show=False)
# level 3 -- series-parallel
add("sp1", S(C("A"), P(C("B"), C("C"))), {"A": "0.9", "B": "0.8", "C": "0.8"})
add("sp2", S(P(C("A"), C("B")), P(C("C"), C("D"))), p="0.5")
add("sp3", P(S(C("A"), C("B")), S(C("C"), C("D"))), p="0.9")
add("sp4", P(S(C("A"), C("B")), C("C")), {"A": "0.5", "B": "0.5", "C": "0.8"})
add("sp5", S(P(C("A"), C("B")), C("C")), p="0.5", show=False)
# level 4 -- complement
add("c_par5", P(*[C(x) for x in "ABCDE"]), p="0.3")
add("c_par_n", P(C("A"), C("B"), C("C")), p="0.5", show=False)
add("c_ser3", S(C("A"), C("B"), C("C")), p="0.9")
add("c_sp", P(S(C("A"), C("B")), S(C("C"), C("D"))), p="0.7")
add("c_par3", P(C("A"), C("B"), C("C")), p="0.8")
# level 5 -- the bridge
add("br_gen", BR(), p="0.5", show=False)
add("br_08", BR(), p="0.8")
add("br_05", BR(), p="0.5")
add("br_06", BR(), p="0.6")
add("br_on", S(P(C("A"), C("C")), P(C("B"), C("D"))), p="0.5", show=False)
add("br_off", P(S(C("A"), C("B")), S(C("C"), C("D"))), p="0.5", show=False)
add("br_dead", BR(), {"A": "0.9", "B": "0.9", "C": "0.9", "D": "0.9", "E": "0"})
# level 6 -- Bayes on circuits
add("b_par", P(C("A"), C("B")), p="0.6")
add("b_ser", S(C("A"), C("B")), p="0.7")
add("b_sp", S(C("A"), P(C("B"), C("C"))), p="0.6")
add("b_sp2", S(C("A"), P(C("B"), C("C"))), {"A": "0.9", "B": "0.5", "C": "0.8"})
# level 7 -- rebuild into a new circuit
add("r_q1", S(C("A"), C("B")), p="0.6")
add("r_q2", P(C("A"), C("B")), p="0.6")
add("r5_q1", S(C("A"), C("B")), p="0.5")
add("r5_q2", P(C("A"), C("B")), p="0.5")
add("r_x1", S(C("A"), P(C("B"), C("C"))), p="0.5")
add("r_x2", S(C("B"), P(C("A"), C("C"))), p="0.5")

# pictures: file -> [(caption or None, circuit name)]
DIAGRAMS = {
    "s_ab": [(None, "s_ab")], "s_abc": [(None, "s_abc")], "s_4": [(None, "s_4")], "s_pp": [(None, "s_pp")],
    "p_ab": [(None, "p_ab")], "p_abc": [(None, "p_abc")], "p_2": [(None, "p_2")],
    "sp1": [(None, "sp1")], "sp2": [(None, "sp2")], "sp3": [(None, "sp3")], "sp4": [(None, "sp4")], "sp5": [(None, "sp5")],
    "c_par5": [(None, "c_par5")], "c_ser3": [(None, "c_ser3")], "c_sp": [(None, "c_sp")], "c_par3": [(None, "c_par3")],
    "br_gen": [(None, "br_gen")], "br_08": [(None, "br_08")], "br_05": [(None, "br_05")],
    "b_par": [(None, "b_par")], "b_ser": [(None, "b_ser")], "b_sp": [(None, "b_sp")], "b_sp2": [(None, "b_sp2")],
    "r_pair": [("Q1", "r_q1"), ("Q2", "r_q2")],
    "r_pair5": [("Q1", "r5_q1"), ("Q2", "r5_q2")],
    "r_pair2": [("Q1", "r_x1"), ("Q2", "r_x2")],
    # lesson figures (no probabilities, to show the shapes)
    "fig_series": [(None, "s_pp")], "fig_parallel": [(None, "p_xy")],
    "br_cases": [("E works", "br_on"), ("E fails", "br_off")],
}
