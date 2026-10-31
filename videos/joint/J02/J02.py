# -*- coding: utf-8 -*-
"""J02 · התפלגויות שוליות — video script (build: tools/video/vid.py J02).

Source: courses/joint/C02.js (lesson + goal: P_X = row sums, P_Y = column sums; the margins do not determine the
joint table).
Exam anchor: 24S-B-Q3b (the marginals of X = heads in the first two of three biased tosses and Y = heads in all
three: Bin(2,p) and Bin(3,p)). No guided quiz uses it; the table of part 24S-B-Q3a is quoted as given (J01 builds
it). It is NOT the boss item 24S-A-Q3b (there Y counts the last two tosses, Bin(2,p)).
Not used on purpose: every C02 quiz item (the fair three-toss table and its P_X(1), P_Y(2), Bin(2,1/2); the (D,T)
table of two bits with P_D(0); two fair coins, independent vs Y = X, as the "same margins" example).
Worked examples are new: a 2x3 decimal table (margins 0.4/0.6 and 0.40/0.25/0.35), and two different 2x2 tables
with the same margins (0.4, 0.6) x (0.5, 0.5).
Every margin is computed by w_joint.Joint (exact), and the exam margins are cross-checked against the binomial pmf
and by Monte Carlo.
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, Space, Joint, eq

# ---------------------------------------------------------------- example: a 2x3 table
A = Joint({(0, 1): R(10, 100), (0, 2): R(20, 100), (0, 3): R(10, 100),
           (1, 1): R(30, 100), (1, 2): R(5, 100), (1, 3): R(25, 100)})
assert [A.PX(x) for x in A.xs] == [R(40, 100), R(60, 100)]
assert [A.PY(y) for y in A.ys] == [R(40, 100), R(25, 100), R(35, 100)]
assert sum(A.PX(x) for x in A.xs) == 1 and sum(A.PY(y) for y in A.ys) == 1
d2 = lambda v: w.dec(v, 2, fixed=True)
Acells = {k: (d2(v), v) for k, v in A.c.items()}
AT = w.table("at", A, cells=Acells, mx={x: (d2(A.PX(x)), A.PX(x)) for x in A.xs},
             my={y: (d2(A.PY(y)), A.PY(y)) for y in A.ys}, tot=True, shown=True, size=36, pad="10px 28px")

# ---------------------------------------------------------------- trap: same margins, different tables
T1 = Joint({(0, 0): R(2, 10), (0, 1): R(2, 10), (1, 0): R(3, 10), (1, 1): R(3, 10)})
T2 = Joint({(0, 0): R(1, 10), (0, 1): R(3, 10), (1, 0): R(4, 10), (1, 1): R(2, 10)})
for T in (T1, T2):
    assert [T.PX(0), T.PX(1)] == [R(4, 10), R(6, 10)] and [T.PY(0), T.PY(1)] == [R(1, 2), R(1, 2)]
assert T1.c != T2.c
assert T1.independent() and not T2.independent()          # one is the product of its margins, the other is not
mk = lambda T, pf: w.table(pf, T, cells={k: (w.dec(v, 1, fixed=True), v) for k, v in T.c.items()},
                           mx={x: (w.dec(T.PX(x), 1, fixed=True), T.PX(x)) for x in T.xs},
                           my={y: (w.dec(T.PY(y), 1, fixed=True), T.PY(y)) for y in T.ys}, shown=True, size=34,
                           pad="8px 22px", mshown=True)
TT1, TT2 = mk(T1, "s1"), mk(T2, "s2")

# ---------------------------------------------------------------- exam 24S-B-Q3b
Q = BANK["24S-B-Q3b"]
assert Q["contextId"] == "24S-B-c3" and "Bin}(3,p)" in Q["solution"] and "Bin}(2,p)" in Q["solution"]
S3 = Space.product({"X1": [(0, 1 - p), (1, p)], "X2": [(0, 1 - p), (1, p)], "X3": [(0, 1 - p), (1, p)]})
J = S3.joint(lambda o: o["X1"] + o["X2"], lambda o: o["X1"] + o["X2"] + o["X3"])
CELLS = {(0, 0): ("(1-p)^3", (1 - p) ** 3), (0, 1): ("p(1-p)^2", p * (1 - p) ** 2),
         (1, 1): ("2p(1-p)^2", 2 * p * (1 - p) ** 2), (1, 2): ("2p^2(1-p)", 2 * p ** 2 * (1 - p)),
         (2, 2): ("p^2(1-p)", p ** 2 * (1 - p)), (2, 3): ("p^3", p ** 3)}
for x in J.xs:
    for y in J.ys:
        CELLS.setdefault((x, y), ("0", 0))
MX = {0: ("(1-p)^2", (1 - p) ** 2), 1: ("2p(1-p)", 2 * p * (1 - p)), 2: ("p^2", p ** 2)}
MY = {0: ("(1-p)^3", (1 - p) ** 3), 1: ("3p(1-p)^2", 3 * p * (1 - p) ** 2), 2: ("3p^2(1-p)", 3 * p ** 2 * (1 - p)),
      3: ("p^3", p ** 3)}
for x in J.xs:                                             # the margins are exactly the binomial pmfs
    assert eq(J.PX(x), sp.binomial(2, x) * p ** x * (1 - p) ** (2 - x)) and eq(J.PX(x), MX[x][1])
for y in J.ys:
    assert eq(J.PY(y), sp.binomial(3, y) * p ** y * (1 - p) ** (3 - y)) and eq(J.PY(y), MY[y][1])
assert eq((1 - p) ** 3 + p * (1 - p) ** 2, (1 - p) ** 2 * ((1 - p) + p))      # the factoring shown for row 0
assert len(J.ys) == 4                                                          # Y takes four values
assert not J.independent()                                                     # margins' product != table
assert not eq(J.PX(0) * J.PY(2), J(0, 2)) and J(0, 2) == 0


def gen3(rng, n, pv=0.35):
    t = (rng.random((n, 3)) < pv).astype(int)
    return {"X": t[:, 0] + t[:, 1], "Y": t.sum(axis=1)}


JN = J.subs({p: R(35, 100)})
w.mc(gen3, [(f"PX({x})", (lambda d, x=x: d["X"] == x), JN.PX(x)) for x in J.xs]
     + [(f"PY({y})", (lambda d, y=y: d["Y"] == y), JN.PY(y)) for y in J.ys])

ET = w.table("et", J, cells=CELLS, mx=MX, my=MY, shown=True, size=29, pad="8px 14px")
row = lambda i: [f"et-h-{i}-{j}" for j in range(4)]
col = lambda j: [f"et-h-{i}-{j}" for i in range(3)]
arow = lambda i: [f"at-h-{i}-{j}" for j in range(3)]
acol = lambda j: [f"at-h-{i}-{j}" for i in range(2)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נוציא מהטבלה המשותפת את ההתפלגות של כל משתנה לבד."),
    P("אלה ההתפלגויות השוליות: סכומי שורות וסכומי עמודות."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">J02 · משתנים משותפים</div><h1>התפלגויות שוליות</h1>'
         '<p>לקבל את ההתפלגות של $X$ לבדו ושל $Y$ לבדו מתוך הטבלה המשותפת, ולהבין למה השוליים לא קובעים את הטבלה.</p>',
   layout="title")

idea = Scene("idea", "סכום שורה, סכום עמודה", [
    P("נתונה טבלה משותפת. רוצים את ההתפלגות של $X$ לבד, בלי קשר ל-$Y$.",
      say="נתונה טבלה משותפת. רוצים את ההתפלגות של אִקְס לבד, בלי קשר לוַואי."),
    P("המאורע $X$ שווה אפס מתפרק לפי הערך של $Y$: אפס ואחת, אפס ושתיים, אפס ושלוש.", do=show(*arow(0)),
      say="המאורע אִקְס שווה אפס מתפרק לפי הערך של וַואי: אפס ואחת, אפס ושתיים, אפס ושלוש."),
    P("אלה מאורעות זרים, ולכן מחברים: סכום השורה הוא אפס נקודה ארבעים.", do=show("at-mxh", "at-mx-0", "i-c1")),
    P("והשורה השנייה נותנת אפס נקודה שישים.", do=hide(*arow(0)) + show(*arow(1), "at-mx-1")),
    P("באותו אופן, ההתפלגות של $Y$ היא סכום **העמודה**.", do=hide(*arow(1)) + show(*acol(0), "at-myh", "at-my-0", "i-c2"),
      say="באותו אופן, ההתפלגות של וַואי היא סכום העמודה."),
    P("עמודה אחת: אפס נקודה ארבעים. עמודה שתיים: אפס נקודה עשרים וחמש. עמודה שלוש: אפס נקודה שלושים וחמש.",
      do=hide(*acol(0)) + show("at-my-1", "at-my-2")),
    P("ובדיקה: כל התפלגות שולית מסתכמת לאחת. בשוליים הימניים וגם בשורה התחתונה.", do=show("at-tot", "i-ok"),
      hold=0.4),
], stage=f'<div class="jt-col">{AT}</div>',
   panel=st.card("i-c1", "rule", "🔑 $P_X(x)=\\displaystyle\\sum_y P_{XY}(x,y)$: סכום <b>שורה</b>")
         + st.card("i-c2", "rule", "🔑 $P_Y(y)=\\displaystyle\\sum_x P_{XY}(x,y)$: סכום <b>עמודה</b>")
         + w.chip("i-ok", "$0.40+0.60=1$ ✓"))

same = Scene("same", "השוליים לא קובעים", [
    P("ועכשיו כיוון הפוך: אם יודעים רק את השוליים, אפשר לשחזר את הטבלה?", do=show("m-1")),
    P("לא. הנה שתי טבלאות שונות.", do=show("m-2")),
    P("בשתיהן $X$ מקבל אפס בהסתברות אפס נקודה ארבע, ו-$Y$ מקבל אפס בהסתברות חצי.",
      do=show("s1-hm-0", "s2-hm-0", "s1-hn-0", "s2-hn-0"),
      say="בשתיהן אִקְס מקבל אפס בהסתברות אפס נקודה ארבע, ווַואי מקבל אפס בהסתברות חצי."),
    P("השוליים זהים לגמרי, אבל התאים שונים. למשל בפינה: אפס נקודה שתיים מול אפס נקודה אחת.",
      do=hide("s1-hm-0", "s2-hm-0", "s1-hn-0", "s2-hn-0") + show("s1-w-0-0", "s2-w-0-0")),
    P("השוליים מספרים על כל משתנה לבד. הם לא מספרים איך המשתנים מתנהגים **יחד**.", do=show("m-t")),
    P("הטבלה השמאלית היא בדיוק מכפלת השוליים שלה: אפס נקודה ארבע כפול חצי זה אפס נקודה שתיים.", do=show("s1-hm-0", "s1-hn-0")),
    P("בימנית זה לא כך. על ההבדל הזה, תלות ואי תלות, נדבר בהמשך הקורס.", do=hide("s1-hm-0", "s1-hn-0")),
    P("אז מהטבלה לשוליים תמיד אפשר. מהשוליים לטבלה, בדרך כלל לא.", hold=0.4),
], stage=f'<div class="jt-row" style="gap:60px">{TT1}{TT2}</div>',
   panel=st.card("m-1", "plain", "אפשר לשחזר את הטבלה מהשוליים?")
         + st.card("m-2", "ex", "שתי טבלאות, אותם שוליים בדיוק")
         + st.card("m-t", "trap", "⚠️ השוליים <b>לא</b> קובעים את הטבלה המשותפת"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. מטבע מוטה מוטל שלוש פעמים, ובכל הטלה עץ בהסתברות $p$.",
      say="ועכשיו סעיף ממבחן. מטבע מוטה מוטל שלוש פעמים, ובכל הטלה עץ בהסתברות פִּי."),
    P("$X$ סופר עצים בשתי ההטלות הראשונות, ו-$Y$ בכל השלוש. את הטבלה המשותפת בנינו בסעיף הקודם.",
      say="אִקְס סופר עצים בשתי ההטלות הראשונות, ווַואי בכל השלוש. את הטבלה המשותפת בנינו בסעיף הקודם."),
    P("עכשיו מבקשים את שתי ההתפלגויות השוליות."),
    P("שורה אפס: אחת פחות $p$, בסוגריים, בשלישית, ועוד $p$ כפול אחת פחות $p$, בסוגריים, בריבוע.", do=show(*row(0)),
      say="שורה אפס: אחת פחות פִּי, בסוגריים, בשלישית, ועוד פִּי כפול אחת פחות פִּי, בסוגריים, בריבוע."),
    P("מוציאים גורם משותף, אחת פחות $p$, בסוגריים, בריבוע. בסוגריים נשאר אחת פחות $p$ ועוד $p$, כלומר אחת.", do=show("x-0"),
      say="מוציאים גורם משותף, אחת פחות פִּי, בסוגריים, בריבוע. בסוגריים נשאר אחת פחות פִּי ועוד פִּי, כלומר אחת."),
    P("לכן הסכום הוא אחת פחות $p$, בסוגריים, בריבוע.", do=show("et-mxh", "et-mx-0"),
      say="לכן הסכום הוא אחת פחות פִּי, בסוגריים, בריבוע."),
    P("באותו אופן, שורה אחת נותנת פעמיים $p$ כפול אחת פחות $p$, ושורה שתיים נותנת $p$ בריבוע.",
      do=hide(*row(0)) + show("et-mx-1", "et-mx-2"),
      say="באותו אופן, שורה אחת נותנת פעמיים פִּי כפול אחת פחות פִּי, ושורה שתיים נותנת פִּי בריבוע."),
    P("זו בדיוק ההתפלגות הבינומית עם שני ניסויים והסתברות $p$. וזה הגיוני.", do=show("x-1"),
      say="זו בדיוק ההתפלגות הבינומית עם שני ניסויים והסתברות פִּי. וזה הגיוני."),
    P("כי $X$ סופר הצלחות בשתי הטלות בלתי תלויות, כל אחת עם סיכוי $p$.",
      say="כי אִקְס סופר הצלחות בשתי הטלות בלתי תלויות, כל אחת עם סיכוי פִּי."),
    P("ועכשיו העמודות. בעמודה אחת יש שני תאים: $p$ כפול אחת פחות $p$, בסוגריים, בריבוע, ופעמיים אותו דבר.", do=show(*col(1)),
      say="ועכשיו העמודות. בעמודה אחת יש שני תאים: פִּי כפול אחת פחות פִּי, בסוגריים, בריבוע, ופעמיים אותו דבר."),
    P("ביחד: שלוש פעמים $p$ כפול אחת פחות $p$, בסוגריים, בריבוע.", do=show("et-myh", "et-my-1"),
      say="ביחד: שלוש פעמים פִּי כפול אחת פחות פִּי, בסוגריים, בריבוע."),
    P("ושאר העמודות נותנות את המקדמים אחת, שלוש, שלוש, אחת.", do=hide(*col(1)) + show("et-my-0", "et-my-2", "et-my-3")),
    P("ובדיקה: שולי העמודות הם האיברים בפיתוח של אחת פחות $p$ ועוד $p$, בשלישית. הסכום אחת.",
      say="ובדיקה: ארבעת השוליים של העמודות הם בדיוק האיברים בפיתוח של אחת פחות פִּי ועוד פִּי, בשלישית. הסכום אחת."),
    P("כלומר בינומית עם **שלושה** ניסויים: $Y$ סופר הצלחות בכל שלוש ההטלות.", do=show("x-2"),
      say="כלומר בינומית עם שלושה ניסויים: וַואי סופר הצלחות בכל שלוש ההטלות."),
    P("המלכודת: לכתוב בינומית עם שניים גם ל-$Y$. אבל ל-$Y$ יש ארבעה ערכים, מאפס עד שלוש.", do=show("x-t"),
      say="המלכודת: לכתוב בינומית עם שניים גם לוַואי. אבל לוַואי יש ארבעה ערכים, מאפס עד שלוש."),
    P("וגם לא לנסות לחזור מהשוליים לטבלה: כאן המכפלה שלהם בכלל לא שווה לטבלה.", hold=0.6),
], stage=f'<div class="jt-col">{ET}</div>',
   panel=w.stem(Q["id"], "מטבע מוטה, שלוש הטלות. $X$ סופר עצים בשתי הראשונות ו-$Y$ בכל השלוש. "
                "מצאו את $P_X(x)$ ואת $P_Y(y)$.")
         + w.eqs("x", ["$(1-p)^3+p(1-p)^2=(1-p)^2$", "$X=X_1+X_2\\sim\\mathrm{Bin}(2,p)$",
                       "$Y=X_1+X_2+X_3\\sim\\mathrm{Bin}(3,p)$"], size=30, gap=8)
         + st.card("x-t", "trap", "⚠️ $Y$ מקבל $0,1,2,3$: בינומית עם $3$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ההתפלגות של $X$ היא סכום השורות.", do=show("r-1"), say="לסיכום: ההתפלגות של אִקְס היא סכום השורות."),
    P("וההתפלגות של $Y$ היא סכום העמודות.", do=show("r-2"), say="וההתפלגות של וַואי היא סכום העמודות."),
    P("כל אחת מהן מסתכמת לאחת, וזו בדיקה טובה.", do=show("r-3")),
    P("והשוליים לא קובעים את הטבלה: הם לא רואים איך המשתנים מתנהגים יחד. נתראה ברמה הבאה.", do=show("r-4"),
      hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$P_X(x)=\\displaystyle\\sum_y P_{XY}(x,y)$</div>'
         '<div class="jt-big">$P_Y(y)=\\displaystyle\\sum_x P_{XY}(x,y)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $P_X$: סכום שורה")
         + st.card("r-2", "rule", "🔑 $P_Y$: סכום עמודה")
         + st.card("r-3", "rule", "🔑 $\\sum_x P_X(x)=1$")
         + st.card("r-4", "trap", "⚠️ שוליים $\\not\\Rightarrow$ טבלה"))

VIDEO = Video("J02", "joint", "התפלגויות שוליות: סכום שורות וסכום עמודות", [title, idea, same, exam, recap],
              bank={"24S-B-Q3b": None})
