# Refuter: rubric-sum check on all four sittings + independent recomputation of the thinned-binomial / Poisson numeric steps.
import json, math, pathlib, sys
from math import comb, exp, factorial

ROOT = pathlib.Path(__file__).resolve().parents[3]
for code in ("24B-B", "24B-C", "24A-E", "24A-A"):
    d = json.load(open(ROOT / "tools" / "raw" / f"{code}.json", encoding="utf-8"))
    bad = []
    for q in d["questions"]:
        r = q.get("rubric")
        if r:
            s = sum(x["points"] for x in r)
            if s != q.get("points"):
                bad.append((q["num"], q.get("part"), s, q.get("points")))
        # structural checks on steps
        for i, st in enumerate(q.get("steps") or []):
            if st["type"] == "choice":
                ids = [o["id"] for o in st["options"]]
                assert st["correctId"] in ids, (code, q["num"], q.get("part"), i)
            if st["type"] == "numeric":
                assert st.get("tol", 0) >= 0
    print(code, "rubric sum != points:", bad or "none")

# thinned binomial values, N=5, p=.6, Q=1/365
N, p, Q = 5, 0.6, 1 / 365
pQ = p * Q
py0 = (1 - pQ) ** N; py1 = N * pQ * (1 - pQ) ** (N - 1)
px2 = comb(5, 2) * p ** 2 * (1 - p) ** 3
joint = 2 * Q * (1 - Q) * px2
print("P(Y=0)", py0, "P(Y=1)", py1, "P(X=2,Y=1)", joint, "P(X=2|Y=1)", joint / py1, "P(Y=1|X=2)", 2 * Q * (1 - Q), "P(X=2)", px2)
# brute-force the joint: enumerate X in 0..5, then Y|X
tot_y1 = sum(comb(5, j) * p ** j * (1 - p) ** (5 - j) * j * Q * (1 - Q) ** (j - 1) for j in range(1, 6))
print("brute P(Y=1)", tot_y1)
# Poisson step values (24A-E 5d): lam=3, p=.4
lam, pp = 3, 0.4
px = lambda k: exp(-lam * pp) * (lam * pp) ** k / factorial(k)
print("P(X=2)", px(2), "P(X=0)", px(0), "e^1.2", exp(1.2))
joint_ = comb(4, 2) * pp ** 2 * (1 - pp) ** 2 * lam ** 4 / factorial(4) * exp(-lam)
print("P(X=2,Y=4)", joint_, "P(Y=4|X=2)", joint_ / px(2), "alt", (lam * (1 - pp)) ** 2 / 2 * exp(-lam * (1 - pp)),
      "P(X=2|Y=4)", comb(4, 2) * pp ** 2 * (1 - pp) ** 2, "P(Y=4)", lam ** 4 / 24 * exp(-lam))
# 24A-A: 623/1152
print("P(X>23/24) 24A-A", 1 - 0.5 * (23 / 24) ** 2, 623 / 1152)
# 24B-C Q5 example boxes 2,3,7
ns = [2, 3, 7]
A = sum(ns) / 3; B = sum(n * n for n in ns) / sum(ns)
var = sum(n * n for n in ns) / 3 - A ** 2
print("A", A, "B", B, "var", var, "B/A", B / A, "1+var/A^2", 1 + var / A ** 2, "P(Y=7)", 7 / 12)
# 24B-C Q6b at p=.6 and 24B-B Q6c
pv = 0.6
PQ = 2 * pv**2 + 2 * pv**3 - 5 * pv**4 + 2 * pv**5
PAQ = pv * (pv + 2 * pv**2 - 3 * pv**3 + pv**4)
print("24B-C 6: P(Q)", PQ, "P(Q|A)", pv + pv * (1 - pv) * (2 * pv - pv**2), "P(A|Q)", PAQ / PQ)
