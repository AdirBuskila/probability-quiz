# -*- coding: utf-8 -*-
"""J05 · בלתי תלויים לעומת בלתי מתואמים — video script (build: tools/video/vid.py J05).

Source: courses/joint/C05.js (lesson + goal: decide from a table whether two variables are independent and whether
they are uncorrelated; independence implies Cov = 0, not the other way).
Exam anchor: 24S-B-Q3d (X = heads in the first two of three biased tosses, Y = heads in all three: independent?).
No guided quiz uses it; the table of 24S-B-Q3a is quoted as given (J01 builds it). It is not the boss item: the
sitting 24S-A (Y = last two tosses) is the one in the boss, and its part Q3d is avoided too.
Not used on purpose: every C05 quiz item (the product table 0.06/0.14/0.24/0.56, the fair three-toss table and its
cell (0,2), X uniform on {-1,0,1} with Y = X^2, Cov = 0 statements, Y = 1 - X).
Worked examples are new: a product table with margins (0.3, 0.7) x (0.4, 0.6), and X uniform on {-2,-1,1,2} with
Y = |X| (Cov = 0 but dependent: P(X=1, Y=2) = 0 while P_X(1) P_Y(2) = 1/8).
Every verdict is exact (w_joint.Joint.independent / witness, sympy) and cross-checked by Monte Carlo.
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, Space, Joint, eq

# ---------------------------------------------------------------- example 1: a product table
PXv, PYv = [R(3, 10), R(7, 10)], [R(4, 10), R(6, 10)]
A = Joint({(x, y): PXv[x] * PYv[y] for x in (0, 1) for y in (0, 1)})
assert [A(0, 0), A(0, 1), A(1, 0), A(1, 1)] == [R(12, 100), R(18, 100), R(28, 100), R(42, 100)]
assert A.independent() and A.cov == 0
d2 = lambda v: w.dec(v, 2, fixed=True)
AT = w.table("at", A, cells={k: (d2(v), v) for k, v in A.c.items()},
             mx={x: (w.dec(A.PX(x), 1, fixed=True), A.PX(x)) for x in A.xs},
             my={y: (w.dec(A.PY(y), 1, fixed=True), A.PY(y)) for y in A.ys}, shown=True, size=36, pad="10px 28px",
             mshown=True)

# ---------------------------------------------------------------- example 2: Y = |X|, X uniform on {-2,-1,1,2}
U = Space.uniform([{"X": v} for v in (-2, -1, 1, 2)])
B = U.joint(lambda o: o["X"], lambda o: abs(o["X"]))
assert B.xs == [-2, -1, 1, 2] and B.ys == [1, 2]
assert B.EX == 0 and B.EXY == 0 and B.cov == 0
assert [(-2) * 2, (-1) * 1, 1 * 1, 2 * 2] == [-4, -1, 1, 4] and sum([-4, -1, 1, 4]) == 0
assert B(1, 2) == 0 and B.PX(1) * B.PY(2) == R(1, 8) and not B.independent()
assert B.witness() is not None


def genB(rng, n):
    x = rng.choice([-2, -1, 1, 2], size=n)
    return {"X": x, "Y": np.abs(x)}


w.mc(genB, [("Cov", lambda d: d["X"] * (d["Y"] - 1.5), 0), ("P(1,2)", lambda d: (d["X"] == 1) & (d["Y"] == 2), 0),
            ("PX(1)PY(2) part", lambda d: d["Y"] == 2, R(1, 2))])
BT = w.table("bt", B, cells="frac", mx="frac", my="frac", shown=True, size=34, pad="6px 30px", mshown=True)
bi = lambda x, y, k="h": f"bt-{k}-%d-%d" % w.pos(B, x, y)

# ---------------------------------------------------------------- exam 24S-B-Q3d
Q = BANK["24S-B-Q3d"]
assert Q["contextId"] == "24S-B-c3" and "P_{XY}(2,0)=0" in Q["solution"] and "p^2(1-p)^3" in Q["solution"]
S3 = Space.product({"X1": [(0, 1 - p), (1, p)], "X2": [(0, 1 - p), (1, p)], "X3": [(0, 1 - p), (1, p)]})
J = S3.joint(lambda o: o["X1"] + o["X2"], lambda o: o["X1"] + o["X2"] + o["X3"])
assert J(2, 0) == 0 and eq(J.PX(2) * J.PY(0), p ** 2 * (1 - p) ** 3)
for pv in (R(1, 100), R(1, 2), R(99, 100)):
    assert (J.PX(2) * J.PY(0)).subs(p, pv) > 0
assert not J.independent()
assert eq(J.cov, 2 * p * (1 - p))                          # and they are correlated as well
CELLS = {(0, 0): ("(1-p)^3", (1 - p) ** 3), (0, 1): ("p(1-p)^2", p * (1 - p) ** 2),
         (1, 1): ("2p(1-p)^2", 2 * p * (1 - p) ** 2), (1, 2): ("2p^2(1-p)", 2 * p ** 2 * (1 - p)),
         (2, 2): ("p^2(1-p)", p ** 2 * (1 - p)), (2, 3): ("p^3", p ** 3)}
for x in J.xs:
    for y in J.ys:
        CELLS.setdefault((x, y), ("0", 0))
MX = {0: ("(1-p)^2", (1 - p) ** 2), 1: ("2p(1-p)", 2 * p * (1 - p)), 2: ("p^2", p ** 2)}
MY = {0: ("(1-p)^3", (1 - p) ** 3), 1: ("3p(1-p)^2", 3 * p * (1 - p) ** 2), 2: ("3p^2(1-p)", 3 * p ** 2 * (1 - p)),
      3: ("p^3", p ** 3)}


def gen3(rng, n, pv=0.4):
    t = (rng.random((n, 3)) < pv).astype(int)
    return {"X": t[:, 0] + t[:, 1], "Y": t.sum(axis=1)}


JN = J.subs({p: R(4, 10)})
w.mc(gen3, [("P(2,0)", lambda d: (d["X"] == 2) & (d["Y"] == 0), 0),
            ("PX(2)", lambda d: d["X"] == 2, JN.PX(2)), ("PY(0)", lambda d: d["Y"] == 0, JN.PY(0)),
            ("Cov", lambda d: (d["X"] - 0.8) * (d["Y"] - 1.2), JN.cov)])
ET = w.table("et", J, cells=CELLS, mx=MX, my=MY, shown=True, size=29, pad="8px 14px", mshown=True)
e20 = "et-%s-%d-%d"

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבדיל בין שני מושגים שקל לבלבל: בלתי תלויים, ובלתי מתואמים."),
    P("נלמד לבדוק כל אחד מהם בטבלה, ונראה למה הם לא אותו דבר."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">J05 · משתנים משותפים</div><h1>בלתי תלויים לעומת בלתי מתואמים</h1>'
         '<p>להכריע מטבלה אם שני משתנים בלתי תלויים ואם הם בלתי מתואמים, ולהסביר למה אלה שני דברים שונים.</p>',
   layout="title")

idea = Scene("idea", "שתי הגדרות", [
    P("בלתי תלויים: **כל** תא בטבלה שווה למכפלת השוליים שלו.", do=show("i-0", "i-c1")),
    P("בלתי מתואמים: השונות המשותפת היא אפס. כלומר התוחלת של המכפלה שווה למכפלת התוחלות.", do=show("i-1", "i-c2")),
    P("אי תלות גוררת אי מתאם. אבל הכיוון ההפוך לא נכון.", do=show("i-c3")),
    P("ואיך בודקים? כדי להוכיח **תלות** מספיק תא אחד שבו השוויון נשבר."),
    P("הכי מהיר: למצוא אפס בטבלה, בתא שהשוליים שלו חיוביים.", do=show("i-c4")),
    P("וכדי להוכיח אי תלות, אין קיצור דרך: בודקים את כל התאים.", hold=0.4),
], stage=w.eqs("i", ["$P_{XY}(x,y)=P_X(x)\\,P_Y(y)\\ \\ \\forall x,y$", "$\\mathrm{Cov}(X,Y)=0$"], size=46, gap=40),
   panel=st.card("i-c1", "rule", "🔑 בלתי תלויים: מכפלה בכל תא")
         + st.card("i-c2", "rule", "🔑 בלתי מתואמים: $E[XY]=E[X]\\,E[Y]$")
         + st.card("i-c3", "trap", "⚠️ בלתי תלויים $\\Rightarrow$ בלתי מתואמים. לא להפך!")
         + st.card("i-c4", "ex", "תלות: אפס בתא ששוליו חיוביים"))

ind = Scene("ind", "טבלה של מכפלה", [
    P("הנה טבלה. השוליים: $X$ אפס בשלוש עשיריות, ו-$Y$ אפס בארבע עשיריות.",
      say="הנה טבלה. השוליים: אִקְס אפס בשלוש עשיריות, ווַואי אפס בארבע עשיריות."),
    P("התא אפס אפס: אפס נקודה שלוש כפול אפס נקודה ארבע, זה אפס נקודה שתים עשרה. שווה.",
      do=show("at-h-0-0", "at-hm-0", "at-hn-0", "a-0")),
    P("אפס אחת: אפס נקודה שלוש כפול אפס נקודה שש, אפס נקודה שמונה עשרה. שווה.",
      do=hide("at-h-0-0", "at-hn-0") + show("at-h-0-1", "at-hn-1", "a-1")),
    P("וגם שני התאים בשורה השנייה: אפס נקודה עשרים ושמונה, ואפס נקודה ארבעים ושתיים.",
      do=hide("at-h-0-1", "at-hm-0", "at-hn-1") + show("at-h-1-0", "at-h-1-1", "a-2")),
    P("כל ארבעת התאים שווים למכפלה. לכן הם בלתי תלויים, ולכן גם השונות המשותפת אפס.", do=show("a-ok"), hold=0.4),
], stage=f'<div class="jt-col" style="gap:20px">{AT}'
         + w.eqs("a", ["$0.3\\cdot0.4=0.12\\ \\checkmark$", "$0.3\\cdot0.6=0.18\\ \\checkmark$",
                       "$0.7\\cdot0.4=0.28,\\ \\ 0.7\\cdot0.6=0.42\\ \\checkmark$"], size=32, gap=4)
         + w.chip("a-ok", "בלתי תלויים, ולכן $\\mathrm{Cov}=0$") + "</div>",
   layout="full")

unc = Scene("unc", "מתאם אפס, ובכל זאת תלויים", [
    P("ועכשיו הפתעה. $X$ מקבל אחד מארבעה ערכים, מינוס שתיים, מינוס אחת, אחת או שתיים, כל אחד ברבע.",
      say="ועכשיו הפתעה. אִקְס מקבל אחד מארבעה ערכים, מינוס שתיים, מינוס אחת, אחת או שתיים, כל אחד ברבע."),
    P("ו-$Y$ הוא הערך המוחלט של $X$. כלומר $Y$ נקבע לגמרי על ידי $X$.", do=show("u-d"),
      say="ווַואי הוא הערך המוחלט של אִקְס. כלומר וַואי נקבע לגמרי על ידי אִקְס."),
    P("השונות המשותפת: התוחלת של $X$ היא אפס, בגלל הסימטריה.", do=show("u-0"),
      say="השונות המשותפת: התוחלת של אִקְס היא אפס, בגלל הסימטריה."),
    P("והתוחלת של המכפלה: מינוס ארבע, מינוס אחת, אחת וארבע, כל אחד ברבע. הסכום אפס.",
      do=show(bi(-2, 2), bi(-1, 1), bi(1, 1), bi(2, 2), "u-1")),
    P("לכן השונות המשותפת היא אפס פחות אפס: הם **בלתי מתואמים**.", do=hide(bi(-2, 2), bi(-1, 1), bi(1, 1), bi(2, 2))
      + show("u-ok")),
    P("אבל הם בוודאי תלויים. הנה תא אפס: $X$ אחת וגם $Y$ שתיים, בלתי אפשרי.", do=show(bi(1, 2, "w")),
      say="אבל הם בוודאי תלויים. הנה תא אפס: אִקְס אחת וגם וַואי שתיים, בלתי אפשרי."),
    P("ומכפלת השוליים שלו: רבע כפול חצי, כלומר שמינית. לא אפס, ולכן תלויים.",
      do=show("bt-hm-2", "bt-hn-1", "u-2", "u-no")),
    P("השונות המשותפת אפס בגלל הסימטריה: המכפלה מקבלת ערכים נגדיים בהסתברויות שוות, והם מתבטלים. וזה לא אומר שאין קשר.", do=show("u-t"), hold=0.4),
], stage=f'<div class="jt-col" style="gap:14px">{BT}</div>',
   panel=st.card("u-d", "plain", "$X$ אחיד על $\\{-2,-1,1,2\\}$, ו-$Y=|X|$")
         + w.eqs("u", ["$E[X]=0$", "$E[XY]=\\tfrac14(-4-1+1+4)=0$", "$P_X(1)\\,P_Y(2)=\\tfrac14\\cdot\\tfrac12=\\tfrac18\\ne0$"],
                 size=32, gap=4)
         + w.chip("u-ok", "$\\mathrm{Cov}=0$: בלתי מתואמים") + w.chip("u-no", "אבל תלויים", "bad")
         + st.card("u-t", "trap", "⚠️ $\\mathrm{Cov}=0$ לא מוכיח אי-תלות"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. שוב שלוש הטלות של מטבע מוטה.",),
    P("$X$ סופר עצים בשתי ההטלות הראשונות, ו-$Y$ סופר עצים בכל השלוש. האם הם בלתי תלויים?",
      say="אִקְס סופר עצים בשתי ההטלות הראשונות, ווַואי סופר עצים בכל השלוש. האם הם בלתי תלויים?"),
    P("זו הטבלה מהסעיפים הקודמים, עם השוליים. מחפשים תא אפס עם שוליים חיוביים."),
    P("למשל התא שתיים אפס: שתי ההטלות הראשונות עץ, ובסך הכול אפס עצים. בלתי אפשרי, ולכן אפס.",
      do=show(e20 % ("w", 2, 0), "x-0"),
      say="למשל התא שתיים אפס: שתי ההטלות הראשונות עץ, ובסך הכול אפס עצים. בלתי אפשרי, ולכן אפס."),
    P("השוליים שלו: $p$ בריבוע, ואחת פחות $p$, בסוגריים, בשלישית.", do=show("et-hm-2", "et-hn-0"),
      say="השוליים שלו: פִּי בריבוע, ואחת פחות פִּי, בסוגריים, בשלישית."),
    P("המכפלה שלהם חיובית לכל $p$ בין אפס לאחת. התא אפס, והמכפלה לא. לכן הם **תלויים**.", do=show("x-1", "x-ok"),
      say="המכפלה שלהם חיובית לכל פִּי בין אפס לאחת. התא אפס, והמכפלה לא. לכן הם תלויים."),
    P("המלכודת: לחשוב שההטלה השלישית מוסיפה מידע חדש, ולכן הם בלתי תלויים.", do=show("x-t")),
    P("אבל $Y$ **כולל** את $X$: הוא $X$ ועוד ההטלה השלישית. מי שיודע את $X$ יודע הרבה על $Y$.",
      say="אבל וַואי כולל את אִקְס: הוא אִקְס ועוד ההטלה השלישית. מי שיודע את אִקְס יודע הרבה על וַואי."),
    P("ולשם השוואה: כאן הם גם מתואמים. השונות המשותפת יוצאת פעמיים $p$ כפול אחת פחות $p$, לא אפס.",
      do=show("x-2"),
      say="ולשם השוואה: כאן הם גם מתואמים. השונות המשותפת יוצאת פעמיים פִּי כפול אחת פחות פִּי, לא אפס."),
    P("אבל לשאלת התלות הספיק תא אחד. לא צריך לחשב שום תוחלת.", hold=0.6),
], stage=f'<div class="jt-col">{ET}</div>',
   panel=w.stem(Q["id"], "$X$ סופר עצים בשתי ההטלות הראשונות, ו-$Y$ בכל השלוש. האם $X$ ו-$Y$ בלתי תלויים?")
         + w.eqs("x", ["$P_{XY}(2,0)=0$", "$P_X(2)\\,P_Y(0)=p^2(1-p)^3&gt;0$", "$\\mathrm{Cov}(X,Y)=2p(1-p)\\ne0$"],
                 size=31, gap=6)
         + w.chip("x-ok", "תלויים", "bad")
         + st.card("x-t", "trap", "⚠️ $Y=X+X_3$ כולל את $X$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בלתי תלויים זה מכפלת השוליים בכל תא. בלתי מתואמים זה שונות משותפת אפס.", do=show("r-1")),
    P("אי תלות גוררת אי מתאם, אבל לא להפך.", do=show("r-2")),
    P("להוכחת תלות מספיק תא אחד, והכי נוח תא אפס ששוליו חיוביים.", do=show("r-3")),
    P("ולהוכחת אי תלות בודקים את כל התאים. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">בלתי תלויים $\\Rightarrow$ $\\mathrm{Cov}=0$</div>'
         '<div class="jt-big" style="color:var(--bad)">$\\mathrm{Cov}=0\\ \\not\\Rightarrow$ בלתי תלויים</div></div>',
   panel=st.card("r-1", "rule", "🔑 אי-תלות: $P_{XY}=P_XP_Y$ בכל תא")
         + st.card("r-2", "trap", "⚠️ $\\mathrm{Cov}=0$ לא מספיק")
         + st.card("r-3", "rule", "🔑 תלות: תא אחד מספיק")
         + st.card("r-4", "rule", "🔑 אי-תלות: כל התאים"))

VIDEO = Video("J05", "joint", "בלתי תלויים לעומת בלתי מתואמים", [title, idea, ind, unc, exam, recap],
              bank={"24S-B-Q3d": None})
