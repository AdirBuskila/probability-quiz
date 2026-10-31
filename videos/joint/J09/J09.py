# -*- coding: utf-8 -*-
"""J09 · אתגר המבחן: משתנים משותפים — boss walkthrough (build: tools/video/vid.py J09).

Source: courses/joint/C09.js (boss level: real exam parts on joint variables, Cov and correlation).
Exam anchors (none is a quiz or boss item, none is a content twin of one):
  25A-A-Q6c  batteries from factories A (proportion q) and B, defective with probability p; X = from A,
             Y = from A and defective: rho[X,Y] = sqrt(p(1-q)/(1-pq)). The marginals Bin(n,q), Bin(n,pq) of parts
             25A-A-Q6a/b are quoted as given.
  25A-A-Q6d  the formula at p = 1: rho = 1, because then Y = X.
  26A-B-Q5c  red X and black X~ among n balls drawn from an urn: X~ = n - X, rho = -1.
Not used on purpose: the C09 boss items (24S-A-Q3a/b, 24A-C-Q3a/d, 25S-C-Q3e, 25A-B-Q6b) and their sittings' other
parts, every quiz item of C01..C08.
Checks: rho of 25A-A by exact enumeration of all 4^n battery outcomes (n = 1..3, symbolic p, q), the indicator
argument term by term, Monte Carlo; rho = -1 by exact hypergeometric enumeration for several urns.
"""
import itertools
from math import comb

import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, q, Space, Joint, eq

n_ = sp.Symbol("n", positive=True, integer=True)

# ---------------------------------------------------------------- 25A-A-Q6c / Q6d
Q1, Q2 = BANK["25A-A-Q6c"], BANK["25A-A-Q6d"]
assert Q1["contextId"] == Q2["contextId"] == "25A-A-c6"
assert "\\sqrt{\\frac{p(1-q)}{1-pq}}" in Q1["solution"].replace(" ", "")
RHO = sp.sqrt(p * (1 - q) / (1 - p * q))
COVn = n_ * p * q * (1 - q)
VX, VY = n_ * q * (1 - q), n_ * p * q * (1 - p * q)
assert eq(sp.simplify(COVn / sp.sqrt(VX * VY) - RHO), 0) or eq(sp.simplify((COVn / sp.sqrt(VX * VY)) ** 2 - RHO ** 2), 0)
# one battery: A ~ Ber(q), Z (defective) ~ Ber(p) independent; X_j = A, Y_j = A Z
one = Space.product({"A": [(0, 1 - q), (1, q)], "Z": [(0, 1 - p), (1, p)]})
assert eq(one.E(lambda o: o["A"] ** 2 * o["Z"]), p * q)                       # E[X_j^2 Z_j] = pq
assert eq(one.E(lambda o: o["A"] * o["A"] * o["Z"]) - q * p * q, p * q * (1 - q))
for n in (1, 2, 3):
    S = Space.product({f"{k}{j}": ([(0, 1 - q), (1, q)] if k == "A" else [(0, 1 - p), (1, p)])
                       for j in range(n) for k in "AZ"})
    fX = lambda o, n=n: sum(o[f"A{j}"] for j in range(n))
    fY = lambda o, n=n: sum(o[f"A{j}"] * o[f"Z{j}"] for j in range(n))
    J = S.joint(fX, fY)
    assert eq(J.cov, n * p * q * (1 - q)) and eq(J.VX, n * q * (1 - q)) and eq(J.VY, n * p * q * (1 - p * q))
    assert eq(J.cov ** 2 / (J.VX * J.VY), RHO ** 2)
    assert not J.independent()                                                 # the pitfall "independent => 0"
assert sp.simplify(RHO.subs(p, 1)) == 1
assert sp.limit(RHO, p, 0, "+") == 0                                           # small p: weak correlation
assert sp.simplify(sp.diff(RHO ** 2, p) - (1 - q) / (1 - p * q) ** 2) == 0     # rho grows with p (0 < q < 1)
assert 0 < float(RHO.subs({p: R(3, 10), q: R(4, 10)})) < 1


def genB(rng, m, n=6, pv=0.3, qv=0.4):
    A = rng.random((m, n)) < qv
    Z = rng.random((m, n)) < pv
    return {"X": A.sum(axis=1), "Y": (A & Z).sum(axis=1)}


nv = {n_: 6, p: R(3, 10), q: R(4, 10)}
w.mc(genB, [("Cov", lambda d: (d["X"] - 2.4) * (d["Y"] - 0.72), COVn.subs(nv)),
            ("VarY", lambda d: (d["Y"] - 0.72) ** 2, VY.subs(nv))])
_d = genB(np.random.default_rng(11), 400_000)
assert abs(np.corrcoef(_d["X"], _d["Y"])[0, 1] - float(RHO.subs(nv))) < 0.01

# ---------------------------------------------------------------- 26A-B-Q5c
Q3 = BANK["26A-B-Q5c"]
assert Q3["contextId"] == "26A-B-c5" and "-1" in Q3["solution"]
for N1, D1, n in [(7, 3, 4), (10, 4, 3), (5, 2, 2)]:
    cells = {}
    for S in itertools.combinations(range(N1), n):
        r = sum(1 for b in S if b < D1)
        cells[(r, n - r)] = cells.get((r, n - r), 0) + R(1, comb(N1, n))
    J = Joint(cells)
    assert J.VX > 0 and eq(J.cov, -J.VX) and J.VY == J.VX and J.rho == -1

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון האתגר של הקורס: שאלות אמיתיות ממבחנים, על שונות משותפת ומקדם מתאם."),
    P("נפתור שלושה סעיפים, ובכל אחד נעצור על המלכודת שלו.", hold=0.4),
], stage='<div class="kicker">J09 · אתגר המבחן</div><h1>אתגר המבחן: משתנים משותפים</h1>'
         '<p>שלושה סעיפים אמיתיים: מקדם מתאם בעזרת אינדיקטורים, מקרה קצה, וקשר ליניארי.</p>', layout="title")

bat = Scene("bat", "סעיף 1: סוללות", [
    P("במחסן סוללות משני מפעלים. חלק $q$ מהן ממפעל אָלֶף, וכל סוללה פגומה בהסתברות $p$, בלי קשר למפעל.",
      say="במחסן סוללות משני מפעלים. חלק קְיוּ מהן ממפעל אָלֶף, וכל סוללה פגומה בהסתברות פִּי, בלי קשר למפעל."),
    P("שולחים $n$ סוללות. $X$ סופר סוללות ממפעל אָלֶף, ו-$Y$ סופר סוללות ממפעל אָלֶף שגם פגומות.",
      say="שולחים אֶן סוללות. אִקְס סופר סוללות ממפעל אָלֶף, ווַואי סופר סוללות ממפעל אָלֶף שגם פגומות."),
    P("מהסעיפים הקודמים: $X$ בינומי עם $n$ ו-$q$, ו-$Y$ בינומי עם $n$ ו-$pq$. מבקשים את מקדם המתאם.",
      do=show("b-0", "b-1"),
      say="מהסעיפים הקודמים: אִקְס בינומי עם אֶן וקְיוּ, ווַואי בינומי עם אֶן ופִּי קְיוּ. מבקשים את מקדם המתאם."),
    P("השונויות ידועות מהבינומית. נשאר למצוא את השונות המשותפת.", do=show("b-2")),
    P("נפרק לאינדיקטורים: לכל סוללה, $X_j$ אומר אם היא ממפעל אָלֶף, ו-$Z_j$ אם היא פגומה.", do=show("b-3"),
      say="נפרק לאינדיקטורים: לכל סוללה, אִקְס גֵ'יי אומר אם היא ממפעל אָלֶף, וזֶד גֵ'יי אם היא פגומה."),
    P("השונות המשותפת היא בילינארית: סכום של שונויות משותפות של זוגות, סוללה מול סוללה.", do=show("b-4")),
    P("כשמדובר בשתי סוללות **שונות**, הן בלתי תלויות, והאיבר אפס.", do=show("b-5")),
    P("נשארים $n$ איברים של אותה סוללה. שם צריך את התוחלת של $X_j$ בריבוע כפול $Z_j$.",
      say="נשארים אֶן איברים של אותה סוללה. שם צריך את התוחלת של אִקְס גֵ'יי בריבוע כפול זֶד גֵ'יי."),
    P("$X_j$ הוא ביט, ולכן בריבוע הוא הוא עצמו. התוחלת $p$ $q$. פחות $q$ כפול $p$ $q$.", do=show("b-6"),
      say="אִקְס גֵ'יי הוא ביט, ולכן בריבוע הוא הוא עצמו. התוחלת פִּי קְיוּ. פחות קְיוּ כפול פִּי קְיוּ."),
    P("לכן השונות המשותפת היא $n$ $p$ $q$ כפול אחת פחות $q$.", do=show("b-7"),
      say="לכן השונות המשותפת היא אֶן פִּי קְיוּ כפול אחת פחות קְיוּ."),
    P("מחלקים בשורש מכפלת השונויות. $n$ מתבטל, $q$ מתבטל, ונשאר שורש של $p$ כפול אחת פחות $q$, חלקי אחת פחות $p$ $q$.",
      do=show("b-ok"),
      say="מחלקים בשורש מכפלת השונויות. אֶן מתבטל, קְיוּ מתבטל, ונשאר שורש של פִּי כפול אחת פחות קְיוּ, חלקי אחת פחות פִּי קְיוּ."),
    P("המלכודת: להניח ש-$X$ ו-$Y$ בלתי תלויים ולענות אפס. אבל $Y$ נספר **מתוך** $X$.", do=show("b-t"),
      say="המלכודת: להניח שאִקְס ווַואי בלתי תלויים ולענות אפס. אבל וַואי נספר מתוך אִקְס."),
    P("ומלכודת שנייה: לשכוח את האיברים של אותה סוללה. בדיוק הם נותנים את כל התשובה.", hold=0.5),
], stage=w.eqs("b", ["$X\\sim\\mathrm{Bin}(n,q),\\ \\ Y\\sim\\mathrm{Bin}(n,pq)$",
                     "$\\mathrm{Var}X=nq(1-q),\\ \\ \\mathrm{Var}Y=npq(1-pq)$",
                     "$\\mathrm{Cov}(X,Y)=\\ ?$",
                     "$X=\\sum_j X_j,\\ \\ Y=\\sum_k X_kZ_k$",
                     "$\\mathrm{Cov}(X,Y)=\\sum_j\\sum_k \\mathrm{Cov}(X_j,\\,X_kZ_k)$",
                     "$j\\ne k:\\ \\ 0$",
                     "$j=k:\\ \\ E[X_j^2Z_j]-q\\cdot pq=pq-pq^2$",
                     "$\\mathrm{Cov}(X,Y)=npq(1-q)$"], size=33, gap=8),
   panel=w.stem(Q1["id"], "חשבו את מקדם המתאם $\\rho[X,Y]$.")
         + w.chip("b-ok", "$\\rho=\\sqrt{\\dfrac{p(1-q)}{1-pq}}$")
         + st.card("b-t", "trap", "⚠️ $Y$ נספר מתוך $X$: הם תלויים, ו-$\\mathrm{Cov}\\ne0$"))

edge = Scene("edge", "סעיף 2: מקרה קצה", [
    P("הסעיף הבא שואל: מה הנוסחה נותנת כש-$p$ שווה אחת?", say="הסעיף הבא שואל: מה הנוסחה נותנת כשפִּי שווה אחת?"),
    P("מציבים: אחת פחות $q$, חלקי אחת פחות $q$. השורש של אחת הוא אחת.", do=show("d-0"),
      say="מציבים: אחת פחות קְיוּ, חלקי אחת פחות קְיוּ. השורש של אחת הוא אחת."),
    P("וזה הגיוני: כש-$p$ אחת, כל הסוללות פגומות. אז $Y$ פשוט שווה ל-$X$.", do=show("d-1"),
      say="וזה הגיוני: כשפִּי אחת, כל הסוללות פגומות. אז וַואי פשוט שווה לאִקְס."),
    P("ומשתנה עם עצמו מתואם לגמרי: השונות המשותפת שלו עם עצמו היא השונות שלו, ומקדם המתאם אחת.", do=show("d-ok")),
    P("ושימו לב לכיוון ההפוך: כש-$p$ קטן, המתאם קטן. מעט סוללות פגומות, ולכן $Y$ מגלה מעט על $X$.",
      say="ושימו לב לכיוון ההפוך: כשפִּי קטן, המתאם קטן. מעט סוללות פגומות, ולכן וַואי מגלה מעט על אִקְס."),
    P("ושימו לב: מתאם אחת הוא הקשר הליניארי החזק ביותר שיש. כאן $Y$ נקבע לגמרי לפי $X$.", do=show("d-t"), hold=0.5,
      say="ושימו לב: מתאם אחת הוא הקשר הליניארי החזק ביותר שיש. כאן וַואי נקבע לגמרי לפי אִקְס."),
], stage=w.eqs("d", ["$\\rho\\big|_{p=1}=\\sqrt{\\dfrac{1-q}{1-q}}=1$",
                     "$p=1\\ \\Rightarrow\\ Y=X$"], size=44, gap=30),
   panel=w.stem(Q2["id"], "מה נותנת הנוסחה מהסעיף הקודם עבור $p=1$? הסבירו.")
         + w.chip("d-ok", "$\\rho[X,X]=\\dfrac{\\mathrm{Var}X}{\\mathrm{Var}X}=1$")
         + st.card("d-t", "rule", "🔑 $\\rho=1$: קשר ליניארי מלא, $Y=X$"))

urn = Scene("urn", "סעיף 3: כד", [
    P("סעיף מבחינה אחרת. בכד כדורים אדומים ושחורים, ומוציאים $n$ כדורים בלי החזרה.",
      say="סעיף מבחינה אחרת. בכד כדורים אדומים ושחורים, ומוציאים אֶן כדורים בלי החזרה."),
    P("$X$ סופר את האדומים שהוצאו, ו-$X$ גל סופר את השחורים. מה מקדם המתאם ביניהם?",
      say="אִקְס סופר את האדומים שהוצאו, ואִקְס גל סופר את השחורים. מה מקדם המתאם ביניהם?"),
    P("אין צורך בשום התפלגות. כל כדור שהוצא הוא אדום או שחור, ולכן השחורים הם $n$ פחות האדומים.", do=show("u-0"),
      say="אין צורך בשום התפלגות. כל כדור שהוצא הוא אדום או שחור, ולכן השחורים הם אֶן פחות האדומים."),
    P("זה קשר ליניארי עם שיפוע מינוס אחת. השונות המשותפת היא מינוס השונות של $X$.", do=show("u-1"),
      say="זה קשר ליניארי עם שיפוע מינוס אחת. השונות המשותפת היא מינוס השונות של אִקְס."),
    P("ולשניהם אותה שונות, כי הוספת קבוע והחלפת סימן לא משנות שונות. לכן מקדם המתאם מינוס אחת.",
      do=show("u-2", "u-ok")),
    P("בתנאי אחד: ש-$X$ באמת משתנה, כלומר בכד יש משני הצבעים ולא מוציאים את כולו.",
      say="בתנאי אחד: שאִקְס באמת משתנה, כלומר בכד יש משני הצבעים ולא מוציאים את כולו."),
    P("המלכודת: לענות אפס כי ״הדגימה אקראית״. אקראיות לא אומרת חוסר קשר.", do=show("u-t"), hold=0.6),
], stage=w.eqs("u", ["$\\tilde X=n-X$", "$\\mathrm{Cov}(X,\\,n-X)=-\\mathrm{Var}X$",
                     "$\\rho=\\dfrac{-\\mathrm{Var}X}{\\sqrt{\\mathrm{Var}X\\cdot\\mathrm{Var}X}}=-1$"], size=42, gap=26),
   panel=w.stem(Q3["id"], "$X$ ו-$\\tilde X$ סופרים אדומים ושחורים בין $n$ הכדורים שהוצאו. מהו $\\rho[X,\\tilde X]$?")
         + w.chip("u-ok", "$\\rho[X,\\tilde X]=-1$")
         + st.card("u-t", "trap", "⚠️ ״אקראי״ לא אומר $\\rho=0$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כשמשתנה הוא סכום של אינדיקטורים, מפרקים את השונות המשותפת לזוגות.", do=show("r-1")),
    P("זוגות בלתי תלויים נותנים אפס, ונשארים רק האיברים שבאמת קשורים.", do=show("r-2")),
    P("ביטים בריבוע הם הביטים עצמם.", do=show("r-3")),
    P("וקשר ליניארי נותן מתאם אחת או מינוס אחת, לפי סימן השיפוע. בהצלחה במבחן!", do=show("r-4"), hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$\\rho=\\dfrac{\\mathrm{Cov}(X,Y)}{\\sqrt{\\mathrm{Var}X\\,\\mathrm{Var}Y}}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $\\mathrm{Cov}(\\sum_j,\\sum_k)=\\sum_j\\sum_k\\mathrm{Cov}$")
         + st.card("r-2", "rule", "🔑 זוג בלתי תלוי: $0$")
         + st.card("r-3", "rule", "🔑 $X_j^2=X_j$")
         + st.card("r-4", "trap", "⚠️ $Y=aX+b$: $\\rho=\\pm1$"))

VIDEO = Video("J09", "joint", "אתגר המבחן: משתנים משותפים", [title, bat, edge, urn, recap],
              bank={"25A-A-Q6c": None, "25A-A-Q6d": None, "26A-B-Q5c": None})
