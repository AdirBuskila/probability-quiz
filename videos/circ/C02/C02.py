# -*- coding: utf-8 -*-
"""C02 · מקביל: מספיקה יחידה אחת — video script (build: tools/video/vid.py C02).

Source: courses/circ/C02.js (lesson + goal). Exam part: an original question in exam style (bank={}): three units in
parallel, P(A)=p, P(B)=P(C)=q: P(S) = 1-(1-p)(1-q)^2; reversed at p = 1/2: P(S) >= 0.98 iff q >= 0.8.
Why no bank anchor: the plain-parallel exam parts are either the (A-B)||C block (25B-B-Q5a, which is most of the C03
quiz item 24B-A-Q6a and the denominator of the C09 boss item 24B-A-Q6c), dependent units (26A-B-Q3d, used in C08)
or twins of C08 quiz items (26A-A-Q3b).
Avoided on purpose: every C02 quiz case (0.9||0.8 -> 0.98, 0.5||0.5||0.6 -> 0.9, 0.6||0.6 -> 0.84, the >= max claim,
0.7||x = 0.94) and the lesson's 0.9||0.8; the (A-B)||C block in any form.
Worked examples: 0.7||0.6 = 0.88 (and the sum 1.3 that is no probability); 0.5||0.6||0.8 = 0.96.
Every number is exact (Fractions / sympy over the full truth table, w_circ).
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

# ---------------------------------------------------------------- numbers (verified)
T2 = w.Pa(w.C("A"), w.C("B"))
PR2 = {"A": Fr("0.7"), "B": Fr("0.6")}
P2 = w.fprob(lambda s: w.works(T2, s), PR2)
assert P2 == Fr("0.88") == 1 - Fr("0.3") * Fr("0.4")
assert P2 == PR2["A"] + PR2["B"] - PR2["A"] * PR2["B"]                # inclusion-exclusion agrees
assert PR2["A"] + PR2["B"] == Fr("1.3") > 1                            # the sum is not a probability
assert w.fprob(lambda s: s["A"] and s["B"], PR2) == Fr("0.42")
for a, b in [(1, 1), (1, 0), (0, 1), (0, 0)]:                          # parallel fails only in the all-0 state
    assert bool(w.works(T2, {"A": bool(a), "B": bool(b)})) == (a or b)

T3 = w.Pa(w.C("A"), w.C("B"), w.C("C"))
PR3 = {"A": Fr("0.5"), "B": Fr("0.6"), "C": Fr("0.8")}
P3 = w.fprob(lambda s: w.works(T3, s), PR3)
assert P3 == Fr("0.96") and 1 - P3 == Fr("0.5") * Fr("0.4") * Fr("0.2") == Fr("0.04")
assert P3 >= max(PR3.values())

# exam-style (original): A with p, B and C with q, all three in parallel
import sympy as sp
p, q = w.p, w.q
T0 = w.Pa(w.C("A"), w.C("B"), w.C("C"))
PQ0 = w.sprob(lambda s: w.works(T0, s), {"A": p, "B": q, "C": q})
assert w.eq(PQ0, 1 - (1 - p) * (1 - q) ** 2)
assert not w.eq(PQ0, p + 2 * q)                                         # the trap: adding
half = PQ0.subs(p, sp.Rational(1, 2))
assert half.subs(q, Fr(4, 5)) == Fr(49, 50)                              # q = 0.8 gives exactly 0.98
assert half.subs(q, Fr(79, 100)) < Fr(98, 100) <= half.subs(q, Fr(81, 100))   # increasing in q: q >= 0.8 is the answer
assert w.fprob(lambda s: w.works(T0, s), {"A": Fr(1, 2), "B": Fr(4, 5), "C": Fr(4, 5)}) == Fr(49, 50)

# ---------------------------------------------------------------- figures
c2 = w.Circ("c2", T2, scale=1.8)
d2 = w.Circ("d2", T2, probs={"A": "0.7", "B": "0.6"}, scale=1.5)
c3 = w.Circ("c3", T3, probs={"A": "0.5", "B": "0.6", "C": "0.8"}, scale=1.3)
c0 = w.Circ("c0", T0, probs={"A": "p", "B": "q", "C": "q"}, scale=0.9)

STEM = ('<div class="qstem"><span class="qid">בסגנון מבחן</span>שלוש יחידות במקביל, בלתי תלויות: $P(A)=p$, '
        '$P(B)=P(C)=q$. (1) מה ההסתברות שהמעגל פועל? (2) אם $p=\\frac12$, מה ה-$q$ הקטן ביותר שנותן לפחות $0.98$?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד את החיבור השני: חיבור במקביל."),
    P("נראה למה כאן כדאי לחשב דווקא את הכישלון, ולמה אסור לחבר הסתברויות."),
    P("ובסוף נפתור שאלה בסגנון מבחן.", hold=0.4),
], stage='<div class="kicker">C02 · מעגלים חשמליים</div><h1>מקביל: מספיקה יחידה אחת</h1>'
         '<p>לחשב את ההסתברות שמעגל מקבילי פועל, ולהימנע מהטעות של חיבור הסתברויות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("במקביל יש לזרם כמה ענפים, והוא צריך רק אחד מהם.", do=show("c2-ok-A", "c2-ok-B", "c2-on")),
    P("אם $A$ נכשלת, הזרם עובר דרך $B$, והמעגל עדיין פועל.", do=hide("c2-ok-A") + show("c2-x-A")),
    P("ואם $B$ נכשלת ו-$A$ פועלת, שוב הכול בסדר.", do=hide("c2-x-A", "c2-ok-B") + show("c2-ok-A", "c2-x-B")),
    P("המעגל נכשל רק במצב אחד: כששתי היחידות נכשלות יחד.",
      do=hide("c2-ok-A", "c2-on") + show("c2-x-A", "c2-off", "i-1")),
    P("לכן הכי קל לחשב את הכישלון, ולהחסיר אותו מאחת.", do=show("i-r1"), hold=0.3),
    P("הכישלונות בלתי תלויים, ולכן ההסתברות ששתיהן נכשלות היא מכפלה של שני הכישלונות.", do=show("i-r2"), hold=0.4),
], stage=f'<div class="circ-stack">{c2.svg()}</div>',
   panel=st.card("i-1", "plain", "המעגל נכשל $\\iff$ $A$ נכשלת <b>וגם</b> $B$ נכשלת")
         + st.card("i-r1", "rule", "🔑 $P(S)=1-P(\\text{fail})$")
         + st.card("i-r2", "rule", "🔑 $P(S)=1-(1-p_A)(1-p_B)$"))

ex1 = Scene("ex1", "שתי יחידות", [
    P("נחשב: $A$ פועלת בהסתברות $0.7$, ו-$B$ בהסתברות $0.6$.", do=show("a-1"),
      say="נחשב: אֵיי פועלת בהסתברות 0.7, ובִּי בהסתברות 0.6."),
    P("$A$ נכשלת בהסתברות $0.3$, ו-$B$ נכשלת בהסתברות $0.4$.", do=show("d2-x-A", "d2-x-B", "a-2"),
      say="אֵיי נכשלת בהסתברות 0.3, ובִּי נכשלת בהסתברות 0.4."),
    P("שתיהן נכשלות יחד בהסתברות $0.3$ כפול $0.4$, כלומר $0.12$.", do=show("d2-off"),
      say="שתיהן נכשלות יחד בהסתברות 0.3 כפול 0.4, כלומר 0.12."),
    P("ולכן המעגל פועל בהסתברות אחת פחות $0.12$: $0.88$.",
      do=hide("d2-x-A", "d2-x-B", "d2-off") + show("d2-on", "a-3"), say="ולכן המעגל פועל בהסתברות אחת פחות 0.12: 0.88."),
    P("והמלכודת: לחבר. $0.7$ ועוד $0.6$ זה $1.3$, ואין הסתברות גדולה מאחת.", do=show("a-t"),
      say="והמלכודת: לחבר. 0.7 ועוד 0.6 זה 1.3, ואין הסתברות גדולה מאחת."),
    P("החיבור סופר פעמיים את המקרה ששתיהן פועלות. צריך להחסיר אותו, $0.42$.", do=show("a-4"),
      say="החיבור סופר פעמיים את המקרה ששתיהן פועלות. צריך להחסיר אותו, 0.42."),
    P("ואז מקבלים שוב $0.88$. שתי הדרכים מסכימות.", say="ואז מקבלים שוב 0.88. שתי הדרכים מסכימות.", hold=0.4),
], stage=f'<div class="circ-stack">{d2.svg()}</div>',
   panel=st.card("a-1", "plain", "$P(A)=0.7,\\ P(B)=0.6$")
         + st.card("a-2", "plain", "כישלונות: $0.3$ ו-$0.4$")
         + st.card("a-3", "ex", "$P(S)=1-0.3\\cdot0.4=0.88$")
         + st.card("a-t", "trap", "⚠️ $0.7+0.6=1.3$: לא הסתברות")
         + st.card("a-4", "ex", "$0.7+0.6-0.42=0.88$ ✓"))

ex2 = Scene("ex2", "שלוש יחידות", [
    P("שלוש יחידות במקביל: $0.5$, $0.6$ ו-$0.8$.", do=show("b-1")),
    P("הכישלונות: $0.5$, $0.4$ ו-$0.2$. המעגל נכשל רק אם שלושתן נכשלות.",
      do=show("c3-x-A", "c3-x-B", "c3-x-C", "c3-off", "b-2"), say="הכישלונות: 0.5, 0.4 ו0.2. המעגל נכשל רק אם שלושתן נכשלות."),
    P("זה $0.5$ כפול $0.4$ כפול $0.2$, כלומר $0.04$.", say="זה 0.5 כפול 0.4 כפול 0.2, כלומר 0.04."),
    P("ולכן המעגל פועל בהסתברות $0.96$.", do=hide("c3-x-A", "c3-x-B", "c3-x-C", "c3-off") + show("c3-on", "b-3")),
    P("בדיקת שפיות: היחידה הטובה ביותר היא $0.8$, והמעגל טוב ממנה.", do=show("b-4"),
      say="בדיקת שפיות: היחידה הטובה ביותר היא 0.8, והמעגל טוב ממנה."),
    P("במקביל זה תמיד כך: כל ענף נוסף רק נותן לזרם עוד דרך, ולכן הוא לא יכול להזיק.", do=show("b-r"), hold=0.4),
], stage=f'<div class="circ-stack">{c3.svg()}</div>',
   panel=st.card("b-1", "plain", "$P(A)=0.5,\\ P(B)=0.6,\\ P(C)=0.8$")
         + st.card("b-2", "plain", "כולן נכשלות: $0.5\\cdot0.4\\cdot0.2=0.04$")
         + st.card("b-3", "ex", "$P(S)=1-0.04=0.96$")
         + st.card("b-4", "plain", "הטובה ביותר: $0.8$, ו-$0.96>0.8$ ✓")
         + st.card("b-r", "rule", "🔑 במקביל: $P(S)\\ge\\max_i p_i$"))

exam = Scene("exam", "בסגנון מבחן", [
    P("שאלה בסגנון מבחן: שלוש יחידות במקביל. $A$ פועלת בהסתברות $p$, ו-$B$, $C$ בהסתברות $q$.",
      say="שאלה בסגנון מבחן: שלוש יחידות במקביל. אֵיי פועלת בהסתברות פִּי, ובִּי, סִי בהסתברות קְיוּ."),
    P("הן בלתי תלויות. מה ההסתברות שהמעגל פועל?"),
    P("המעגל נכשל רק כששלושתן נכשלות.", do=show("c0-x-A", "c0-x-B", "c0-x-C", "c0-off")),
    P("$A$ נכשלת בהסתברות $1-p$, וכל אחת מהשתיים האחרות בהסתברות $1-q$.", do=show("x-1"),
      say="אֵיי נכשלת בהסתברות אחת פחות פִּי, וכל אחת מהשתיים האחרות בהסתברות אחת פחות קְיוּ."),
    P("מכפילים את שלושת הכישלונות: $(1-p)(1-q)^2$.", do=show("x-2"),
      say="מכפילים את שלושת הכישלונות: אחת פחות פִּי, כפול אחת פחות קְיוּ, בסוגריים, בריבוע."),
    P("ולכן המעגל פועל בהסתברות אחת פחות המכפלה הזאת.",
      do=hide("c0-x-A", "c0-x-B", "c0-x-C", "c0-off") + show("c0-on", "x-3"), hold=0.3),
    P("המלכודת: לחבר, $p$ ועוד $2q$. עם $p=0.5$ ו-$q=0.8$ זה כבר $2.1$.", do=show("x-t"),
      say="המלכודת: לחבר, פִּי ועוד שתיים קְיוּ. עם פִּי שווה 0.5 וקְיוּ שווה 0.8 זה כבר 2.1."),
    P("סעיף שני: $p$ הוא חצי. מה ה-$q$ הקטן ביותר, כך שהמעגל יפעל בהסתברות $0.98$ לפחות?", do=show("x-4"),
      say="סעיף שני: פִּי הוא חצי. מה הקְיוּ הקטן ביותר, כך שהמעגל יפעל בהסתברות 0.98 לפחות?"),
    P("צריך שהכישלון יהיה לכל היותר $0.02$: חצי, כפול $(1-q)^2$, לכל היותר $0.02$.",
      say="צריך שהכישלון יהיה לכל היותר 0.02: חצי, כפול אחת פחות קְיוּ, בסוגריים, בריבוע, לכל היותר 0.02."),
    P("כלומר $(1-q)^2$ לכל היותר $0.04$, ולכן $1-q$ לכל היותר $0.2$.",
      say="כלומר אחת פחות קְיוּ, בסוגריים, בריבוע, לכל היותר 0.04, ולכן אחת פחות קְיוּ לכל היותר 0.2."),
    P("התשובה: $q$ לפחות $0.8$. ובדיקה: עם $0.8$ יוצא בדיוק $0.98$.", do=show("x-5"),
      say="התשובה: קְיוּ לפחות 0.8. ובדיקה: עם 0.8 יוצא בדיוק 0.98.", hold=0.5),
], stage=f'<div class="circ-stack">{c0.svg()}'
         + st.card("x-3", "rule", "🔑 $P(S)=1-(1-p)(1-q)^2$")
         + st.card("x-5", "rule", "🔑 $\\frac12(1-q)^2\\le0.02\\iff q\\ge0.8$") + '</div>',
   panel=STEM
         + st.card("x-1", "plain", "כישלונות: $1-p$, $1-q$, $1-q$")
         + st.card("x-2", "plain", "כולן נכשלות: $(1-p)(1-q)^2$")
         + st.card("x-t", "trap", "⚠️ לא $p+2q$")
         + st.card("x-4", "ex", "$p=\\frac12$: מתי $P(S)\\ge0.98$?"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: במקביל מספיק ענף אחד שפועל, והמעגל נכשל רק כשכל הענפים נכשלים.", do=show("r-1")),
    P("לכן מחשבים את הכישלון, מכפלת הכישלונות, ומחסירים מאחת.", do=show("r-2")),
    P("לא מחברים הסתברויות: יחידות בלתי תלויות אינן זרות, ואפשר לעבור את אחת.", do=show("r-3")),
    P("והתוצאה תמיד גדולה מהיחידה הטובה ביותר. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="circ-stack"><div class="circ-big">$P(S)=1-(1-p_1)(1-p_2)\\cdots(1-p_n)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 מקביל = <b>לפחות אחת</b> = איחוד")
         + st.card("r-2", "rule", "🔑 $1-\\prod(1-p_i)$")
         + st.card("r-3", "trap", "⚠️ לא $p_1+p_2$")
         + st.card("r-4", "rule", "🔑 $P(S)\\ge\\max_i p_i$"))

VIDEO = Video("C02", "circ", "מקביל: מספיקה יחידה אחת", [title, idea, ex1, ex2, exam, recap],
              bank={})
