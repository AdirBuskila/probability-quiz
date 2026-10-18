# Compare claims in raw JSON with my own independently derived values. ASCII output.
import json, math, itertools
from fractions import Fraction as F
import sympy as sp

R = "C:/Users/Adir/Desktop/Coding/Dev/probability-quiz/tools/raw/"
e = math.e
N = None  # non-numeric step placeholder
ex = {
 "24A-C": {
  (1,"א"): [1, F(1,2)],
  (1,"ב"): [1, F(1,2), N, F(4,9), F(8,9)],
  (1,"ג"): [1, F(1,2), N, F(5,18), F(5,9)],
  (1,"ד"): [1, F(1,2), N, F(1,4), F(1,2)],
  (2,"א"): [N, 9, F(1,9)],
  (2,"ב"): [N, F(2,81), F(8,81)],
  (2,"ג"): [N, 6, F(4,729), F(5,243)],
  (2,"ד"): [N, F(1,81), F(1,729), F(1,9)],
  (2,"ה"): [N, F(11,27), F(5,729), F(5,297)],
  (3,"א"): [N, -1, 0.54, 3],
  (3,"ב"): [0.72, -0.72, 0.2016],
  (3,"ג"): [N, -0.1, 0.45],
  (3,"ד"): [-0.18, 0.072, -0.252],
  (3,"ה"): [0, 0.1512, N],
  (3,"ו"): [-0.252, N],
  (4,"א"): [N, 1.5, 1, F(23,24)],
  (4,"ב"): [F(1,2), N, 0.7],
  (4,"ג"): [F(7,8), F(5,8), F(5,7)],
  (5,"א"): [N, 0.4, 0.3456],
  (5,"ב"): [N, 0.36, 0.3, F(3,7)],
  (5,"ג"): [N, 0.09/0.343, F(40,343)],
  (6,"א"): [N, 0.7056, 0.5904, 0.65952],
  (6,"ב"): [N, 0.936, 0.78624],
  (6,"ג"): [N, 0.78624, 0.936, 0.504, 0.57888/0.78624],
 },
 "24A-D": {
  (1,"א"): [1, N, F(2,9)],
  (1,"ב"): [1, N, F(2,3), F(4,9)],
  (1,"ג"): [1, F(2,3), F(4,9), F(2,3)],
  (2,"א"): [N, 5, F(5,36)],
  (2,"ב"): [N, 216, 10, F(5,108)],
  (2,"ג"): [N, F(1,36), F(1,216), F(1,6)],
  (2,"ד"): [N, F(5,12), F(1,54), F(2,45)],
  (2,"ה"): [N, F(1,6), F(1,108), F(1,18)],
  (3,"א"): [N, -0.18, 0.1476],
  (3,"ב"): [N, 0.9, 0.45],
  (3,"ג"): [-0.36, -0.162, -0.198],
  (4,"א"): [N, 0],
  (4,"ב"): [N, 4, 2, 0.25],
  (4,"ג"): [F(1,2), N, F(7,8)],
  (4,"ד"): [F(3,4), F(33,128), F(11,32)],
  (5,"א"): [N, 1/365, 1215/4096],
  (5,"ב"): [N, 1, e**-1/2],
  (5,"ג"): [N, 3, 9*e**-3/2],
  (6,"א"): [N, 0.7056, 0.5904, 0.65952],
  (6,"ב"): [N, 0.5904, 0.83616],
  (6,"ג"): [N, 0.65952, 0.65952, 1],
 },
}
bad = 0
for code, tab in ex.items():
    d = json.load(open(R + code + ".json", encoding="utf8"))
    seen = set()
    for q in d["questions"]:
        k = (q["num"], q["part"]); seen.add(k)
        exp = tab[k]
        st = q["steps"]
        if len(st) != len(exp):
            print(code, k, "STEP COUNT", len(st), len(exp)); bad += 1; continue
        for i, (s, v) in enumerate(zip(st, exp)):
            if s["type"] == "numeric":
                if v is None:
                    print(code, k, i, "numeric but no expectation"); bad += 1; continue
                tol = max(s.get("tol", 0), 1e-9)
                if abs(s["answer"] - float(v)) > tol:
                    print(code, k, i, "DISAGREE numeric", s["answer"], float(v), "tol", tol); bad += 1
            else:
                if v is not None:
                    print(code, k, i, "non-numeric but expectation given"); bad += 1
        # order/findbug/fillblank/text steps? list types
        for s in st:
            if s["type"] not in ("numeric", "choice"):
                print(code, k, "non numeric/choice step type", s["type"])
        # choice: unique correct id exists, options ids
        for s in st:
            if s["type"] == "choice":
                ids = [o["id"] for o in s["options"]]
                assert s["correctId"] in ids and len(set(ids)) == len(ids)
        # rubric sum vs points
        if q.get("rubric"):
            sm = sum(r["points"] for r in q["rubric"])
            if sm != q.get("points"):
                print(code, k, "RUBRIC SUM", sm, "points", q.get("points")); bad += 1
        # sim/exact vs region exact
        if q.get("region") and q.get("sim") and abs(q["region"]["exact"] - q["sim"]["exact"]) > 1e-12:
            print(code, k, "region/sim exact differ"); bad += 1
    assert seen == set(tab), (seen ^ set(tab))
print("mismatches:", bad)

# ---- sim exact values vs mine
sims = {
 ("24A-C", 1, "א"): 0.5, ("24A-C", 1, "ב"): 8/9, ("24A-C", 1, "ג"): 5/9, ("24A-C", 1, "ד"): 0.5,
 ("24A-C", 2, "ב"): 8/81, ("24A-C", 2, "ג"): 5/243, ("24A-C", 2, "ד"): 1/9, ("24A-C", 2, "ה"): 5/297,
 ("24A-C", 3, "א"): 0.54, ("24A-C", 3, "ב"): 0.2016, ("24A-C", 3, "ג"): 0.45, ("24A-C", 3, "ד"): -0.252,
 ("24A-C", 3, "ה"): 0, ("24A-C", 3, "ו"): -0.252,
 ("24A-C", 4, "א"): 23/24, ("24A-C", 4, "ב"): 0.7, ("24A-C", 4, "ג"): 5/7,
 ("24A-C", 5, "א"): 0.3456, ("24A-C", 5, "ב"): 3/7, ("24A-C", 5, "ג"): 40/343,
 ("24A-C", 6, "א"): 0.65952, ("24A-C", 6, "ב"): 0.78624, ("24A-C", 6, "ג"): 0.57888/0.78624,
 ("24A-D", 1, "א"): 2/9, ("24A-D", 1, "ב"): 4/9, ("24A-D", 1, "ג"): 2/3,
 ("24A-D", 2, "א"): 5/36, ("24A-D", 2, "ב"): 5/108, ("24A-D", 2, "ג"): 1/6, ("24A-D", 2, "ד"): 2/45, ("24A-D", 2, "ה"): 1/18,
 ("24A-D", 3, "א"): 0.1476, ("24A-D", 3, "ב"): 0.45, ("24A-D", 3, "ג"): -0.198,
 ("24A-D", 4, "א"): 0, ("24A-D", 4, "ב"): 2/3, ("24A-D", 4, "ג"): 0.125, ("24A-D", 4, "ד"): 11/32,
 ("24A-D", 5, "א"): 1215/4096, ("24A-D", 5, "ב"): e**-1/2, ("24A-D", 5, "ג"): 9*e**-3/2,
 ("24A-D", 6, "א"): 0.65952, ("24A-D", 6, "ב"): 0.83616, ("24A-D", 6, "ג"): 1.0,
}
for code in ("24A-C", "24A-D"):
    d = json.load(open(R + code + ".json", encoding="utf8"))
    for q in d["questions"]:
        k = (code, q["num"], q["part"])
        s = q.get("sim")
        if s is None:
            print(k, "NO SIM"); continue
        if abs(s["exact"] - sims[k]) > 1e-9:
            print(k, "SIM EXACT DISAGREE", s["exact"], sims[k])
print("sim exacts compared")

# ---- truncation errors of the compound sims
p, Q = 0.5, 0.4
# C5b: Y truncated at 30 with tail lumped onto Y=30
pm = [p * (1 - p) ** (j - 1) for j in range(1, 30)] + [(1 - p) ** 29]
tz0 = sum(pm[j - 1] * (1 - Q) ** j for j in range(1, 31))
print("C5b trunc P(Z=0)", tz0, "closed", 3 / 7, "err", abs(tz0 - 3 / 7))
tz2 = sum(pm[j - 1] * math.comb(j, 2) * Q**2 * (1 - Q) ** (j - 2) for j in range(2, 31))
cl2 = 40 / 343
print("C5c trunc P(Z=2)", tz2, "closed", cl2, "err", abs(tz2 - cl2))
# also P(Y=30) lumped means weights sum:
print("sum pm", sum(pm))
lam, pb = 4, 0.25
pois = [math.exp(-lam) * lam**j / math.factorial(j) for j in range(26)]
print("D5 poisson trunc tail", 1 - sum(pois))
pz2 = sum(pois[j] * math.comb(j, 2) * pb**2 * (1 - pb) ** (j - 2) for j in range(2, 26))
print("D5b trunc P(Y=2)", pz2, "closed", math.exp(-1) / 2, "err", abs(pz2 - math.exp(-1) / 2))
num = pois[4] * math.comb(4, 2) * pb**2 * (1 - pb) ** 2
den = pz2
print("D5c trunc cond", num / den, "closed", 9 * math.exp(-3) / 2, "err", abs(num / den - 9 * math.exp(-3) / 2))

# ---- symbolic checks of circuit decompositions
P = sp.symbols("p")
Q1 = P * (2 * P - P**2) ** 2 + (1 - P) * (2 * P**2 - P**4)
print("Q1 formula = 2p^2+2p^3-5p^4+2p^5:", sp.expand(Q1 - (2 * P**2 + 2 * P**3 - 5 * P**4 + 2 * P**5)) == 0)
print("C6c inter 3p^5-9p^4+7p^3:", sp.expand(P**2 * (1 - (1 - P) ** 3) + 2 * P * (1 - P) * P * (2 * P - P**2) - (3 * P**5 - 9 * P**4 + 7 * P**3)) == 0)
Qd = (2 * P - P**2) * P**2 + P**2 * (1 - P) ** 2 + P * (1 - P) * (P + P**2 - P**3) + P**2 * (1 - P) * (2 * P - P**2)
print("D6c inter == P(Q1):", sp.expand(Qd - Q1) == 0)
Q2d = P + (1 - P) * (2 * P**2 - P**4)
print("D6b p+(1-p)(2p^2-p^4) == 1-(1-p)(1-p^2)^2:", sp.expand(Q2d - (1 - (1 - P) * (1 - P**2) ** 2)) == 0)
Q2c = (2 * P - P**2) * (1 - (1 - P) ** 3)
print("C6b expansion 6p^2-9p^3+5p^4-p^5:", sp.expand(Q2c - (6 * P**2 - 9 * P**3 + 5 * P**4 - P**5)) == 0)
# C6c final ratio
rat = P * (7 - 9 * P + 3 * P**2) / (6 - 9 * P + 5 * P**2 - P**3)
print("C6c ratio simplifies equal to (3p^5-9p^4+7p^3)/(6p^2-9p^3+5p^4-p^5):", sp.simplify(rat - (3 * P**5 - 9 * P**4 + 7 * P**3) / (6 * P**2 - 9 * P**3 + 5 * P**4 - P**5)) == 0)
# C5b alt form
Qs, ps = sp.symbols("Q p_")
print("C5b forms equal:", sp.simplify(ps * (1 - Qs) / (1 - (1 - Qs) * (1 - ps)) - ps * (1 - Qs) / (ps * (1 - Qs) + Qs)) == 0)
# C3 cov simplified vs unsimplified
pp, qq = sp.symbols("pp qq")
print("C3d cov forms equal:", sp.expand(-pp * qq - (pp * qq - pp - qq) * (pp + qq - 1) + (pp + qq) * (1 - pp) * (1 - qq)) == 0)
# D4 symbolic var
a, b, x = sp.symbols("a b x", positive=True)
print("D4 var:", sp.simplify(2 * sp.integrate(x**2 * a * (b - x), (x, 0, b))))
# E|X| = b/3 under ab^2=1
print("D4 E|X|:", sp.simplify(2 * sp.integrate(x * a * (b - x), (x, 0, b)).subs(a, 1 / b**2)))
