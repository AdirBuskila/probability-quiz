# -*- coding: utf-8 -*-
"""J06 · התפלגות מותנית ותוחלת מותנית מטבלה — video script (build: tools/video/vid.py J06).

Source: courses/joint/C06.js (lesson + goal: P(X=x | Y=y) and E[X | Y=y] from a joint table, and the total
expectation E[X] = sum_y P_Y(y) E[X | Y=y]).
Exam part: no bank question asks for a conditional pmf from a joint table (26A-B-Q5d is a hypergeometric formula,
not a table, and belongs to the events topic), so the exam scene is an original question "בסגנון מבחן" (bank={})
on the setup of sitting 24S-B (biased coin tossed three times, X = heads in the first two, Y = heads in all three):
P(X = x | Y = 2), E[X | Y = 2], then E[X | Y = y] = 2y/3 for every y and E[X] = 2p by total expectation.
Not used on purpose: every C06 quiz item (the fair three-toss table of 24S-A with P(X=0|Y=0), E[X|Y=0], E[X|Y=2],
P(Y=0|X=1), total expectation = 1; the (D,T) table with P(T=1|D=0)) and the lesson's 2x2 table 0.1/0.3/0.2/0.4.
Worked example is new: the 2x3 table on x in {0,1}, y in {1,2,3} (column y = 3: 2/7, 5/7, E[X|Y=3] = 5/7; the
row trap P(Y=3|X=1) = 5/12; total expectation 0.3 + 0.05 + 0.25 = 0.6 = E[X]).
Everything exact (w_joint, sympy) and cross-checked by Monte Carlo (conditioning by rejection).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, Space, Joint, eq

# ---------------------------------------------------------------- example
A = Joint({(0, 1): R(10, 100), (0, 2): R(20, 100), (0, 3): R(10, 100),
           (1, 1): R(30, 100), (1, 2): R(5, 100), (1, 3): R(25, 100)})
assert A.PY(3) == R(35, 100)
assert A.cond_x(3) == {0: R(2, 7), 1: R(5, 7)} and A.Ecx(3) == R(5, 7)
assert A.cond_y(1)[3] == R(5, 12) and A.PX(1) == R(6, 10)
assert A.Ecx(1) == R(3, 4) and A.Ecx(2) == R(1, 5)
TOT = [A.PY(y) * A.Ecx(y) for y in A.ys]
assert TOT == [R(3, 10), R(5, 100), R(25, 100)] and sum(TOT) == A.EX == R(6, 10)


def genA(rng, n):
    keys = list(A.c)
    idx = rng.choice(len(keys), size=n, p=[float(A.c[k]) for k in keys])
    return {"X": np.array([k[0] for k in keys])[idx], "Y": np.array([k[1] for k in keys])[idx]}


_d = genA(np.random.default_rng(3), 600_000)
_m = _d["Y"] == 3
assert abs(_d["X"][_m].mean() - 5 / 7) < 5 * _d["X"][_m].std() / np.sqrt(_m.sum())
_r = _d["X"] == 1
assert abs((_d["Y"][_r] == 3).mean() - 5 / 12) < 0.004

d2 = lambda v: w.dec(v, 2, fixed=True)
AT = w.table("at", A, cells={k: (d2(v), v) for k, v in A.c.items()},
             mx={x: (d2(A.PX(x)), A.PX(x)) for x in A.xs}, my={y: (d2(A.PY(y)), A.PY(y)) for y in A.ys},
             shown=True, size=36, pad="10px 28px", mshown=True)
ac = lambda x, y, k="h": f"at-{k}-%d-%d" % w.pos(A, x, y)

# ---------------------------------------------------------------- exam-style: the 24S-B setup
assert BANK["24S-B-Q3a"]["contextId"] == "24S-B-c3"
S3 = Space.product({"X1": [(0, 1 - p), (1, p)], "X2": [(0, 1 - p), (1, p)], "X3": [(0, 1 - p), (1, p)]})
J = S3.joint(lambda o: o["X1"] + o["X2"], lambda o: o["X1"] + o["X2"] + o["X3"])
assert eq(J.PY(2), 3 * p ** 2 * (1 - p))
C2 = J.cond_x(2)
assert C2 == {0: 0, 1: R(2, 3), 2: R(1, 3)}                     # free of p
assert J.Ecx(2) == R(4, 3)
for y in J.ys:
    assert eq(J.Ecx(y), R(2, 3) * y)                             # E[X | Y=y] = 2y/3
assert eq(sum(J.PY(y) * J.Ecx(y) for y in J.ys), 2 * p) and eq(J.EX, 2 * p) and eq(J.EY, 3 * p)
assert eq(J(1, 2), 2 * p ** 2 * (1 - p)) and eq(J(2, 2), p ** 2 * (1 - p))


def gen3(rng, n, pv=0.3):
    t = (rng.random((n, 3)) < pv).astype(int)
    return {"X": t[:, 0] + t[:, 1], "Y": t.sum(axis=1)}


_d = gen3(np.random.default_rng(5), 800_000)
for y in range(4):
    m = _d["Y"] == y
    se = max(_d["X"][m].std(), 1e-9) / np.sqrt(m.sum())
    assert abs(_d["X"][m].mean() - 2 * y / 3) < 5 * se + 1e-9, y
m = _d["Y"] == 2
assert abs((_d["X"][m] == 1).mean() - 2 / 3) < 0.005

CELLS = {(0, 0): ("(1-p)^3", (1 - p) ** 3), (0, 1): ("p(1-p)^2", p * (1 - p) ** 2),
         (1, 1): ("2p(1-p)^2", 2 * p * (1 - p) ** 2), (1, 2): ("2p^2(1-p)", 2 * p ** 2 * (1 - p)),
         (2, 2): ("p^2(1-p)", p ** 2 * (1 - p)), (2, 3): ("p^3", p ** 3)}
for x in J.xs:
    for y in J.ys:
        CELLS.setdefault((x, y), ("0", 0))
MY = {0: ("(1-p)^3", (1 - p) ** 3), 1: ("3p(1-p)^2", 3 * p * (1 - p) ** 2), 2: ("3p^2(1-p)", 3 * p ** 2 * (1 - p)),
      3: ("p^3", p ** 3)}
ET = w.table("et", J, cells=CELLS, my=MY, shown=True, size=30, pad="8px 16px", mshown=True)
col2 = ["et-h-%d-2" % i for i in range(3)]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד להתנות בטבלה משותפת: מה ההתפלגות של $X$, כשכבר יודעים את $Y$.",
      say="בסרטון הזה נלמד להתנות בטבלה משותפת: מה ההתפלגות של אִקְס, כשכבר יודעים את וַואי."),
    P("נחשב הסתברות מותנית, תוחלת מותנית, ונשתמש בהן כדי לקבל את התוחלת הכללית."),
    P("ובסוף נפתור שאלה בסגנון מבחן.", hold=0.4),
], stage='<div class="kicker">J06 · משתנים משותפים</div><h1>התפלגות מותנית ותוחלת מותנית</h1>'
         '<p>לחשב מטבלה משותפת $P(X=x\\mid Y=y)$ ו-$E[X\\mid Y=y]$, ולהשתמש בהן לחישוב $E[X]$.</p>', layout="title")

col = Scene("col", "עמודה אחת", [
    P("״בהינתן ש-$Y$ שווה שלוש״ אומר: אנחנו כבר יודעים שהתוצאה נמצאת בעמודה של שלוש.", do=show(ac(0, 3), ac(1, 3)),
      say="בהינתן שוַואי שווה שלוש אומר: אנחנו כבר יודעים שהתוצאה נמצאת בעמודה של שלוש."),
    P("כל שאר הטבלה כבר לא רלוונטית. אבל שני התאים בעמודה מסתכמים רק לאפס נקודה שלושים וחמש.",
      do=show("at-hn-2")),
    P("לכן מנרמלים: מחלקים כל תא בסכום העמודה, כדי שביחד יתנו אחת.", do=show("c-f")),
    P("$X$ שווה אפס: אפס נקודה עשר חלקי אפס נקודה שלושים וחמש, כלומר שתי שביעיות.", do=show("c-0"),
      say="אִקְס שווה אפס: אפס נקודה עשר חלקי אפס נקודה שלושים וחמש, כלומר שתי שביעיות."),
    P("$X$ שווה אחת: אפס נקודה עשרים וחמש חלקי אפס נקודה שלושים וחמש, כלומר חמש שביעיות.", do=show("c-1"),
      say="אִקְס שווה אחת: אפס נקודה עשרים וחמש חלקי אפס נקודה שלושים וחמש, כלומר חמש שביעיות."),
    P("זו התפלגות לכל דבר, ואפשר לחשב לה תוחלת: אפס כפול שתי שביעיות ועוד אחת כפול חמש שביעיות.",
      do=show("c-2")),
    P("התוחלת המותנית יוצאת חמש שביעיות.", do=show("c-ok")),
    P("ועכשיו המלכודת: ההתניה ההפוכה. ההסתברות ש-$Y$ שלוש, בהינתן ש-$X$ אחת.",
      do=hide(ac(0, 3), "at-hn-2") + show(ac(1, 3, "w"), "at-hm-1", "c-t"),
      say="ועכשיו המלכודת: ההתניה ההפוכה. ההסתברות שוַואי שלוש, בהינתן שאִקְס אחת."),
    P("כאן התנאי הוא על $X$, ולכן מסתכלים על **השורה** של אחת ומחלקים בסכום שלה, אפס נקודה שש.",
      do=show("c-3"),
      say="כאן התנאי הוא על אִקְס, ולכן מסתכלים על השורה של אחת ומחלקים בסכום שלה, אפס נקודה שש."),
    P("יוצא חמש חלקי שתים עשרה, ולא חמש שביעיות. אותו תא, מכנה אחר.", hold=0.4),
], stage=f'<div class="jt-col" style="gap:18px">{AT}'
         + w.eqs("c", ["$P(X=0\\mid Y=3)=\\dfrac{0.10}{0.35}=\\dfrac27$", "$P(X=1\\mid Y=3)=\\dfrac{0.25}{0.35}=\\dfrac57$",
                       "$E[X\\mid Y=3]=0\\cdot\\tfrac27+1\\cdot\\tfrac57=\\tfrac57$",
                       "$P(Y=3\\mid X=1)=\\dfrac{0.25}{0.60}=\\dfrac5{12}$"], size=28, gap=14) + "</div>",
   panel=st.card("c-f", "rule", "🔑 $P(X=x\\mid Y=y)=\\dfrac{P_{XY}(x,y)}{P_Y(y)}$")
         + w.chip("c-ok", "$E[X\\mid Y=3]=\\tfrac57$")
         + st.card("c-t", "trap", "⚠️ בהינתן $X$: מחלקים בסכום <b>השורה</b>, לא העמודה"))

tot = Scene("tot", "תוחלת שלמה", [
    P("לכל עמודה יש תוחלת מותנית משלה. בעמודה אחת: אפס נקודה שלוש חלקי אפס נקודה ארבע, שלושה רבעים.",
      do=show("t-0")),
    P("בעמודה שתיים: אפס נקודה אפס חמש חלקי אפס נקודה עשרים וחמש, חמישית. ובעמודה שלוש, חמש שביעיות.",
      do=show("t-1")),
    P("התוחלת הכללית היא ממוצע משוקלל שלהן: כל תוחלת מותנית כפול ההסתברות של העמודה שלה.", do=show("t-f")),
    P("שלושה רבעים כפול אפס נקודה ארבע, זה אפס נקודה שלוש. חמישית כפול רבע, אפס נקודה אפס חמש.", do=show("t-2")),
    P("וחמש שביעיות כפול אפס נקודה שלושים וחמש, אפס נקודה עשרים וחמש. הסכום אפס נקודה שש.", do=show("t-3")),
    P("ובדיקה מהשוליים: $X$ שווה אחת בהסתברות אפס נקודה שש, ולכן גם $E[X]$ אפס נקודה שש.", do=show("t-ok"),
      say="ובדיקה מהשוליים: אִקְס שווה אחת בהסתברות אפס נקודה שש, ולכן גם התוחלת שלו אפס נקודה שש.", hold=0.4),
], stage=w.eqs("t", ["$E[X\\mid Y=1]=\\tfrac{0.30}{0.40}=\\tfrac34$",
                     "$E[X\\mid Y=2]=\\tfrac{0.05}{0.25}=\\tfrac15,\\ \\ E[X\\mid Y=3]=\\tfrac57$",
                     "$E[X]=0.40\\cdot\\tfrac34+0.25\\cdot\\tfrac15+0.35\\cdot\\tfrac57$",
                     "$=0.3+0.05+0.25=0.6$"], size=40, gap=22),
   panel=st.card("t-f", "rule", "🔑 $E[X]=\\displaystyle\\sum_y P_Y(y)\\,E[X\\mid Y=y]$")
         + w.chip("t-ok", "$E[X]=P_X(1)=0.6$ ✓"))

exam = Scene("exam", "בסגנון מבחן", [
    P("ועכשיו שאלה בסגנון מבחן. שוב מטבע מוטה, שלוש הטלות.",),
    P("$X$ סופר עצים בשתי הראשונות, ו-$Y$ בכל השלוש. ידוע שבסך הכול יצאו שני עצים. מה ההתפלגות של $X$?",
      say="אִקְס סופר עצים בשתי הראשונות, ווַואי בכל השלוש. ידוע שבסך הכול יצאו שני עצים. מה ההתפלגות של אִקְס?"),
    P("התנאי הוא על $Y$, ולכן לוקחים את העמודה של שתיים. הסכום שלה: שלוש $p$ בריבוע כפול אחת פחות $p$.",
      do=show(*col2, "et-hn-2"),
      say="התנאי הוא על וַואי, ולכן לוקחים את העמודה של שתיים. הסכום שלה: שלוש פִּי בריבוע כפול אחת פחות פִּי."),
    P("$X$ שווה אחת: פעמיים $p$ בריבוע כפול אחת פחות $p$, חלקי הסכום. נשאר שני שלישים.", do=show("x-0"),
      say="אִקְס שווה אחת: פעמיים פִּי בריבוע כפול אחת פחות פִּי, חלקי הסכום. נשאר שני שלישים."),
    P("$X$ שווה שתיים: שליש. ו-$X$ שווה אפס: התא אפס, ולכן אפס.", do=show("x-1"),
      say="אִקְס שווה שתיים: שליש. ואִקְס שווה אפס: התא אפס, ולכן אפס."),
    P("שימו לב: $p$ נעלם לגמרי. למה? יש שלוש הטלות ובהן בדיוק פלי אחד.", do=show("x-c"),
      say="שימו לב: פִּי נעלם לגמרי. למה? יש שלוש הטלות ובהן בדיוק פלי אחד."),
    P("כל מיקום של הפלי סביר באותה מידה. רק כשהוא בהטלה השלישית, $X$ שווה שתיים. סיכוי של שליש.",
      say="כל מיקום של הפלי סביר באותה מידה. רק כשהוא בהטלה השלישית, אִקְס שווה שתיים. סיכוי של שליש."),
    P("התוחלת המותנית: אחת כפול שני שלישים, ועוד שתיים כפול שליש. ארבעה שלישים.", do=show("x-2")),
    P("באותה דרך, בכל עמודה יוצא שני שלישים כפול $y$. כל עץ נמצא בשתי הראשונות בסיכוי שני שלישים.",
      do=hide(*col2, "et-hn-2") + show("x-3"),
      say="באותה דרך, בכל עמודה יוצא שני שלישים כפול וַואי. כל עץ נמצא בשתי הראשונות בסיכוי שני שלישים."),
    P("ומכאן, בתוחלת שלמה: שני שלישים כפול התוחלת של $Y$, שהיא שלוש $p$. כלומר פעמיים $p$.", do=show("x-4"),
      say="ומכאן, בתוחלת שלמה: שני שלישים כפול התוחלת של וַואי, שהיא שלוש פִּי. כלומר פעמיים פִּי."),
    P("וזו בדיוק התוחלת של בינומית עם שתי הטלות. הבדיקה מסתדרת.", do=show("x-ok"), hold=0.6),
], stage=f'<div class="jt-col">{ET}</div>',
   panel='<div class="qstem"><span class="qid">בסגנון מבחן</span>מטבע מוטה, שלוש הטלות: $X$ עצים בשתי '
         'הראשונות, $Y$ עצים בכל השלוש. מצאו $P(X=x\\mid Y=2)$ ו-$E[X\\mid Y=2]$.</div>'
         + w.eqs("x", ["$P(X=1\\mid Y=2)=\\dfrac{2p^2(1-p)}{3p^2(1-p)}=\\dfrac23$",
                       "$P(X=2\\mid Y=2)=\\tfrac13,\\ \\ P(X=0\\mid Y=2)=0$",
                       "$E[X\\mid Y=2]=1\\cdot\\tfrac23+2\\cdot\\tfrac13=\\tfrac43$",
                       "$E[X\\mid Y=y]=\\tfrac23\\,y$", "$E[X]=\\tfrac23\\,E[Y]=\\tfrac23\\cdot3p=2p$"], size=27, gap=2)
         + st.card("x-c", "ex", "$p$ מתבטל: הפלי היחיד נמצא בכל מקום בסיכוי $\\tfrac13$")
         + w.chip("x-ok", "$E[X]=2p$ ✓"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בהינתן $Y$, לוקחים את העמודה שלו ומחלקים בסכום שלה.", do=show("r-1"),
      say="לסיכום: בהינתן וַואי, לוקחים את העמודה שלו ומחלקים בסכום שלה."),
    P("בהינתן $X$, לוקחים את השורה ומחלקים בסכום השורה.", do=show("r-2"),
      say="בהינתן אִקְס, לוקחים את השורה ומחלקים בסכום השורה."),
    P("תוחלת מותנית היא תוחלת רגילה, לפי ההתפלגות המותנית.", do=show("r-3")),
    P("והתוחלת הכללית היא ממוצע משוקלל של התוחלות המותנות. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$P(X=x\\mid Y=y)=\\dfrac{P_{XY}(x,y)}{P_Y(y)}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 בהינתן $Y=y$: עמודה, חלקי $P_Y(y)$")
         + st.card("r-2", "trap", "⚠️ בהינתן $X=x$: שורה, חלקי $P_X(x)$")
         + st.card("r-3", "rule", "🔑 $E[X\\mid Y=y]=\\sum_x x\\,P(X=x\\mid Y=y)$")
         + st.card("r-4", "rule", "🔑 $E[X]=\\sum_y P_Y(y)\\,E[X\\mid Y=y]$"))

VIDEO = Video("J06", "joint", "התפלגות מותנית ותוחלת מותנית מטבלה", [title, col, tot, exam, recap], bank={})
