# -*- coding: utf-8 -*-
"""J04 · שונות משותפת ומקדם מתאם — video script (build: tools/video/vid.py J04).

Source: courses/joint/C04.js (lesson + goal: Cov, Var and rho from a joint table, and Var of a sum).
Exam anchor: 24A-D-Q3c (Q = [[0, X], [Y, X+Y]], X~Ber(p), Y~Ber(q) independent, D = det Q, T = tr Q: cov[D,T]).
No guided quiz uses it; E[D] = -pq of part 24A-D-Q3a is quoted (J03 solves it). Not a twin of the boss item
24A-C-Q3d (another matrix, [[-1,-X^2],[Y^2,X+Y]], other D and T).
Not used on purpose: every C04 quiz item (the (D,T) table of two fair bits with Cov 1/4, Var 3/16 and 1/2,
rho = sqrt(2/3); Var[X+Y] = 3/2 for the three tosses; rho for Y = 3 - 2X) and the lesson's table 0.1/0.3/0.2/0.4.
Worked example is new: the 2x3 table on x in {1,2}, y in {0,1,2} (Cov = 0.1, Var X = 0.24, Var Y = 0.6,
rho = 0.1/sqrt(0.144) ~ 0.264, Var[X+Y] = 1.04, also checked as E[(X+Y)^2] - 2.6^2).
Every value is exact (w_joint, sympy) and cross-checked by Monte Carlo (the exam with a real 2x2 determinant).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, q, Space, Joint, eq

# ---------------------------------------------------------------- example
B = Joint({(1, 0): R(2, 10), (1, 1): R(1, 10), (1, 2): R(1, 10),
           (2, 0): R(1, 10), (2, 1): R(3, 10), (2, 2): R(2, 10)})
assert (B.EX, B.EY, B.EXY) == (R(16, 10), 1, R(17, 10))
assert B.cov == R(1, 10)
assert B.E(lambda x, y: x * x) == R(28, 10) and B.VX == R(24, 100)
assert B.E(lambda x, y: y * y) == R(16, 10) and B.VY == R(6, 10)
assert B.VX * B.VY == R(144, 1000)
RHO = B.rho
assert eq(RHO, R(1, 10) / sp.sqrt(R(144, 1000))) and abs(float(RHO) - 0.2635) < 5e-4 and -1 <= RHO <= 1
VS = B.E(lambda x, y: (x + y) ** 2) - (B.EX + B.EY) ** 2
assert B.E(lambda x, y: (x + y) ** 2) == R(78, 10) and VS == R(104, 100) == B.VX + B.VY + 2 * B.cov


def genB(rng, n):
    keys = list(B.c)
    idx = rng.choice(len(keys), size=n, p=[float(B.c[k]) for k in keys])
    return {"X": np.array([k[0] for k in keys])[idx], "Y": np.array([k[1] for k in keys])[idx]}


w.mc(genB, [("Cov", lambda d: (d["X"] - 1.6) * (d["Y"] - 1.0), B.cov),
            ("VarX", lambda d: (d["X"] - 1.6) ** 2, B.VX), ("Var(X+Y)", lambda d: (d["X"] + d["Y"] - 2.6) ** 2, VS)])

BT = w.table("bt", B, cells={k: (w.dec(v, 1, fixed=True), v) for k, v in B.c.items()},
             mx={x: (w.dec(B.PX(x), 1, fixed=True), B.PX(x)) for x in B.xs},
             my={y: (w.dec(B.PY(y), 1, fixed=True), B.PY(y)) for y in B.ys}, shown=True, size=34, pad="8px 26px",
             mshown=True)

# ---------------------------------------------------------------- exam 24A-D-Q3c
Q = BANK["24A-D-Q3c"]
assert Q["contextId"] == "24A-D-c3" and "pq\\,(-2+p+q)" in Q["solution"]
M = lambda X, Y: sp.Matrix([[0, X], [Y, X + Y]])
S = Space.product({"X": [(0, 1 - p), (1, p)], "Y": [(0, 1 - q), (1, q)]})
fD = lambda o: M(o["X"], o["Y"]).det()
fT = lambda o: M(o["X"], o["Y"]).trace()
STATES = [(0, 0), (0, 1), (1, 0), (1, 1)]
VALS = [(fD({"X": a, "Y": b}), fT({"X": a, "Y": b})) for a, b in STATES]
assert VALS == [(0, 0), (0, 1), (0, 1), (-1, 2)]
ED, ET, EDT = S.E(fD), S.E(fT), S.E(lambda o: fD(o) * fT(o))
assert eq(ED, -p * q) and eq(ET, p + q) and eq(EDT, -2 * p * q)
COV = sp.factor(EDT - ED * ET)
assert eq(COV, p * q * (p + q - 2))
assert not eq(EDT, -p ** 2 * q - p * q ** 2)                       # the pitfall E[X^2 Y] = p^2 q
for pv in (R(1, 10), R(1, 2), R(9, 10)):                            # negative on the whole open square
    for qv in (R(1, 10), R(1, 2), R(9, 10)):
        assert COV.subs({p: pv, q: qv}) < 0
JD = S.joint(fD, fT)
assert eq(JD.cov, COV)


def genM(rng, n, pv=0.3, qv=0.6):
    X = (rng.random(n) < pv).astype(float)
    Y = (rng.random(n) < qv).astype(float)
    mats = np.zeros((n, 2, 2))
    mats[:, 0, 1], mats[:, 1, 0], mats[:, 1, 1] = X, Y, X + Y
    return {"D": np.round(np.linalg.det(mats)), "T": np.trace(mats, axis1=1, axis2=2)}


nv = {p: R(3, 10), q: R(6, 10)}
mD, mT = float(ED.subs(nv)), float(ET.subs(nv))
w.mc(genM, [("Cov(D,T)", lambda d: (d["D"] - mD) * (d["T"] - mT), COV.subs(nv)),
            ("E[DT]", lambda d: d["D"] * d["T"], EDT.subs(nv))])

PST = {(0, 0): "(1-p)(1-q)", (0, 1): "(1-p)q", (1, 0): "p(1-q)", (1, 1): "pq"}
EC = w.cards("s", [[f"$({a},{b})$", f"${PST[(a, b)]}$", f"$D={d},\\ T={t}$", f"$DT={d * t}$"]
                   for (a, b), (d, t) in zip(STATES, VALS)], size=30, minw=200, maxw=1000)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נמדוד את הקשר בין שני משתנים: שונות משותפת ומקדם מתאם."),
    P("נחשב אותם מטבלה, ונראה גם איך הם משפיעים על השונות של סכום."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">J04 · משתנים משותפים</div><h1>שונות משותפת ומקדם מתאם</h1>'
         '<p>לחשב $\\mathrm{Cov}$, שונות ומקדם מתאם $\\rho$ מתוך טבלה משותפת, ושונות של סכום.</p>', layout="title")

idea = Scene("idea", "ההגדרות", [
    P("השונות המשותפת אומרת אם שני המשתנים נוטים לגדול יחד, או להפך.", do=show("i-0")),
    P("מחשבים אותה כך: התוחלת של המכפלה, פחות מכפלת התוחלות.",
      say="מחשבים אותה כך: התוחלת של המכפלה, פחות מכפלת התוחלות."),
    P("חיובית: כשאחד גדול, גם השני נוטה להיות גדול. שלילית: כשאחד גדול, השני נוטה להיות קטן.", do=show("i-c1")),
    P("והשונות הרגילה היא מקרה פרטי: התוחלת של הריבוע פחות ריבוע התוחלת.", do=show("i-1")),
    P("מקדם המתאם מנרמל את השונות המשותפת: מחלקים בשורש של מכפלת השונויות.", do=show("i-2")),
    P("הוא תמיד בין מינוס אחת לאחת. ואם התקבל ערך מחוץ לטווח, יש טעות בחישוב.", do=show("i-c2"), hold=0.4),
], stage=w.eqs("i", ["$\\mathrm{Cov}(X,Y)=E[XY]-E[X]\\,E[Y]$", "$\\mathrm{Var}[X]=E[X^2]-E[X]^2$",
                     "$\\rho(X,Y)=\\dfrac{\\mathrm{Cov}(X,Y)}{\\sqrt{\\mathrm{Var}[X]\\,\\mathrm{Var}[Y]}}$"], size=44, gap=28),
   panel=st.card("i-c1", "ex", "$\\mathrm{Cov}&gt;0$: גדלים יחד. $\\mathrm{Cov}&lt;0$: בכיוונים הפוכים")
         + st.card("i-c2", "rule", "🔑 $-1\\le\\rho\\le1$, ו-$\\mathrm{Var}\\ge0$ תמיד"))

ex = Scene("ex", "דוגמה מטבלה", [
    P("נחשב על הטבלה הזו. כבר יודעים מהשלב הקודם: $E[X]$ אחת נקודה שש, $E[Y]$ אחת, ו-$E[XY]$ אחת נקודה שבע.",
      do=show("e-0"),
      say="נחשב על הטבלה הזו. כבר יודעים מהשלב הקודם: התוחלת של אִקְס אחת נקודה שש, של וַואי אחת, ושל המכפלה אחת נקודה שבע."),
    P("לכן השונות המשותפת: אחת נקודה שבע פחות אחת נקודה שש. כלומר אפס נקודה אחת, חיובית.", do=show("e-1")),
    P("עכשיו השונויות. התוחלת של $X$ בריבוע: אחת כפול אפס נקודה ארבע, ועוד ארבע כפול אפס נקודה שש. שתיים נקודה שמונה.",
      do=show("bt-hm-0", "bt-hm-1", "e-2"),
      say="עכשיו השונויות. התוחלת של אִקְס בריבוע: אחת כפול אפס נקודה ארבע, ועוד ארבע כפול אפס נקודה שש. שתיים נקודה שמונה."),
    P("פחות אחת נקודה שש בריבוע, שהוא שתיים נקודה חמישים ושש. נשאר אפס נקודה עשרים וארבע."),
    P("ובאותו אופן, השונות של $Y$ היא אחת נקודה שש פחות אחת, כלומר אפס נקודה שש.",
      do=hide("bt-hm-0", "bt-hm-1") + show("bt-hn-1", "bt-hn-2", "e-3"),
      say="ובאותו אופן, השונות של וַואי היא אחת נקודה שש פחות אחת, כלומר אפס נקודה שש."),
    P("מקדם המתאם: אפס נקודה אחת, חלקי השורש של אפס נקודה עשרים וארבע כפול אפס נקודה שש.",
      do=hide("bt-hn-1", "bt-hn-2") + show("e-4")),
    P("יוצא בערך אפס נקודה עשרים ושש. קשר חיובי, אבל חלש.", do=show("e-ok")),
    P("ועוד שימוש חשוב: השונות של סכום. מחברים את השונויות, **ועוד פעמיים** השונות המשותפת.", do=show("e-c")),
    P("כאן: אפס נקודה עשרים וארבע, ועוד אפס נקודה שש, ועוד אפס נקודה שתיים. כלומר אחת נקודה אפס ארבע.",
      do=show("e-5")),
    P("מי ששוכח את השונות המשותפת מקבל אפס נקודה שמונים וארבע, וזה נכון רק כשהיא אפס.", do=show("e-t"), hold=0.4),
], stage=f'<div class="jt-col" style="gap:18px">{BT}'
         + w.eqs("e", ["$E[X]=1.6,\\ \\ E[Y]=1,\\ \\ E[XY]=1.7$", "$\\mathrm{Cov}=1.7-1.6\\cdot1=0.1$",
                       "$\\mathrm{Var}[X]=2.8-1.6^2=0.24$", "$\\mathrm{Var}[Y]=1.6-1^2=0.6$",
                       "$\\rho=\\dfrac{0.1}{\\sqrt{0.24\\cdot0.6}}\\approx0.26$",
                       "$\\mathrm{Var}[X+Y]=0.24+0.6+2\\cdot0.1=1.04$"], size=30, gap=2) + "</div>",
   panel=w.chip("e-ok", "$\\rho\\approx0.26$: קשר חיובי חלש")
         + st.card("e-c", "rule", "🔑 שונות של סכום:<br><span style=\"font-size:29px\">"
                   "$\\mathrm{Var}[X+Y]=\\mathrm{Var}[X]+\\mathrm{Var}[Y]+2\\,\\mathrm{Cov}$</span>")
         + st.card("e-t", "trap", "⚠️ בלי $2\\,\\mathrm{Cov}$ יוצא $0.84$, וזה נכון רק אם $\\mathrm{Cov}=0$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. המטריצה: אפס ו-$X$ למעלה, $Y$ ו-$X$ ועוד $Y$ למטה.",
      say="ועכשיו סעיף ממבחן. המטריצה: אפס ואִקְס למעלה, וַואי ואִקְס ועוד וַואי למטה."),
    P("$X$ ברנולי עם $p$, $Y$ ברנולי עם $q$, בלתי תלויים. מבקשים את השונות המשותפת של $D$ ו-$T$.",
      say="אִקְס ברנולי עם פִּי, וַואי ברנולי עם קְיוּ, בלתי תלויים. מבקשים את השונות המשותפת של דִּי וטִי."),
    P("$D$ היא הדטרמיננטה, מינוס $X$ כפול $Y$. ו-$T$ היא העקבה, סכום האלכסון: $X$ ועוד $Y$.", do=show("x-0"),
      say="דִּי היא הדטרמיננטה, מינוס אִקְס כפול וַואי. וטִי היא העקבה, סכום האלכסון: אִקְס ועוד וַואי."),
    P("צריך שלוש תוחלות. $E[D]$ מצאנו בסעיף הקודם: מינוס $p$ $q$.", do=show("x-1"),
      say="צריך שלוש תוחלות. את התוחלת של דִּי מצאנו בסעיף הקודם: מינוס פִּי קְיוּ."),
    P("$E[T]$ לפי ליניאריות: $p$ ועוד $q$.", do=show("x-2"),
      say="את התוחלת של טִי לפי ליניאריות: פִּי ועוד קְיוּ."),
    P("ו-$E[DT]$ נחשב בארבעת המצבים, כמו תוחלת של כל פונקציה.", do=show(*[f"s-o-{k}" for k in range(4)]),
      say="ואת התוחלת של דִּי כפול טִי נחשב בארבעת המצבים, כמו תוחלת של כל פונקציה."),
    P("בשלושה מצבים $D$ שווה אפס, ולכן גם המכפלה אפס.",
      do=show(*[f"s-l-{k}-{r}" for k in range(4) for r in (1, 2, 3)]) + show("s-ow-0", "s-ow-1", "s-ow-2"),
      say="בשלושה מצבים דִּי שווה אפס, ולכן גם המכפלה אפס."),
    P("רק כששניהם אחת: $D$ מינוס אחת, $T$ שתיים, והמכפלה מינוס שתיים. בהסתברות $p$ $q$.",
      do=hide("s-ow-0", "s-ow-1", "s-ow-2") + show("s-oh-3", "x-3"),
      say="רק כששניהם אחת: דִּי מינוס אחת, טִי שתיים, והמכפלה מינוס שתיים. בהסתברות פִּי קְיוּ."),
    P("מציבים: מינוס פעמיים $p$ $q$, פחות מינוס $p$ $q$ כפול $p$ ועוד $q$.", do=show("x-4"),
      say="מציבים: מינוס פעמיים פִּי קְיוּ, פחות מינוס פִּי קְיוּ כפול פִּי ועוד קְיוּ."),
    P("מוציאים $p$ $q$ החוצה: $p$ $q$ כפול, בסוגריים, $p$ ועוד $q$ פחות שתיים.", do=show("x-ok"),
      say="מוציאים פִּי קְיוּ החוצה: פִּי קְיוּ כפול, בסוגריים, פִּי ועוד קְיוּ פחות שתיים."),
    P("ובגלל ש-$p$ ו-$q$ קטנים מאחת, הסוגריים שליליים. כשהעקבה גדלה, הדטרמיננטה נוטה לרדת.",
      say="ובגלל שפִּי וקְיוּ קטנים מאחת, הסוגריים שליליים. כשהעקבה גדלה, הדטרמיננטה נוטה לרדת."),
    P("המלכודת באלגברה: $X$ בריבוע כפול $Y$. לביט, $X$ בריבוע הוא $X$, והתוחלת היא $p$ $q$, לא $p$ בריבוע $q$.",
      do=show("x-t"),
      say="המלכודת באלגברה: אִקְס בריבוע כפול וַואי. לביט, אִקְס בריבוע הוא אִקְס, והתוחלת היא פִּי קְיוּ, לא פִּי בריבוע קְיוּ."),
    P("והמלכודת השנייה: לאבד את המינוס של הדטרמיננטה בדרך.", hold=0.6),
], stage=f'<div class="jt-col" style="gap:26px">'
         '<div class="jt-big">$Q=\\begin{pmatrix}0&X\\\\Y&X+Y\\end{pmatrix}$</div>' + EC + "</div>",
   panel=w.stem(Q["id"], "$X\\sim\\mathrm{Ber}(p)$, $Y\\sim\\mathrm{Ber}(q)$ בלתי תלויים. חשבו את $\\mathrm{Cov}[D,T]$.")
         + w.eqs("x", ["$D=-XY,\\quad T=X+Y$", "$E[D]=-pq$", "$E[T]=p+q$", "$E[DT]=(-2)\\cdot pq=-2pq$",
                       "$\\mathrm{Cov}=-2pq-(-pq)(p+q)$"], size=30, gap=4)
         + w.chip("x-ok", "$\\mathrm{Cov}[D,T]=pq\\,(p+q-2)$")
         + st.card("x-t", "trap", "⚠️ $E[X^2Y]=E[XY]=pq$, כי $X^2=X$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: שונות משותפת היא התוחלת של המכפלה פחות מכפלת התוחלות.", do=show("r-1")),
    P("מקדם המתאם מחלק אותה בשורש מכפלת השונויות, והוא תמיד בין מינוס אחת לאחת.", do=show("r-2")),
    P("בשונות של סכום לא לשכוח פעמיים את השונות המשותפת.", do=show("r-3")),
    P("ושונות של משתנה אחד לעולם לא שלילית. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$\\mathrm{Cov}(X,Y)=E[XY]-E[X]\\,E[Y]$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $\\mathrm{Cov}=E[XY]-E[X]E[Y]$")
         + st.card("r-2", "rule", "🔑 $\\rho=\\mathrm{Cov}/\\sqrt{\\mathrm{Var}\\,\\mathrm{Var}}\\in[-1,1]$")
         + st.card("r-3", "rule", "🔑 $\\mathrm{Var}[X+Y]$ כולל $2\\,\\mathrm{Cov}$")
         + st.card("r-4", "trap", "⚠️ $\\mathrm{Var}&lt;0$ או $|\\rho|&gt;1$: טעות חישוב"))

VIDEO = Video("J04", "joint", "שונות משותפת ומקדם מתאם", [title, idea, ex, exam, recap],
              bank={"24A-D-Q3c": None})
