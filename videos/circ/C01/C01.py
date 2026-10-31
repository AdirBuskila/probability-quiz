# -*- coding: utf-8 -*-
"""C01 · טור: כולם חייבים לעבוד — video script (build: tools/video/vid.py C01).

Source: courses/circ/C01.js (lesson + goal). Exam anchor: 26A-B-Q3c (three printed components A, B, C in series;
A and C independent with P = p, B depends on them through q1..q4): P(Q1) = q1 p^2. Open question (bank key None),
used by no guided quiz.
Avoided on purpose: every C01 quiz case (0.9·0.8, 0.9·0.9·0.5, 0.9^4, the p1p2 <= min claim as an MCQ, p^2 = 0.49)
and the lesson's 0.9·0.8 / 0.9^10; 26A-A-Q3a (P(A)P(B|A) = pq), the symbolic twin of the C08 quiz.
Worked examples: 0.95·0.8·0.9 = 0.684; how many units of 0.98 in series keep P(S) >= 0.9 (five).
Every number is exact (Fractions over the full truth table, w_circ.fprob / sprob).
"""
from fractions import Fraction as Fr
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

# ---------------------------------------------------------------- numbers (verified)
T2 = w.S(w.C("A"), w.C("B"))
assert w.fprob(lambda s: w.works(T2, s), {"A": Fr(1, 2), "B": Fr(1, 2)}) == Fr(1, 4)
for a, b in [(1, 1), (1, 0), (0, 1), (0, 0)]:                      # series works only in the all-1 state
    assert bool(w.works(T2, {"A": bool(a), "B": bool(b)})) == (a == b == 1)

T3 = w.S(w.C("A"), w.C("B"), w.C("C"))
PR3 = {"A": Fr("0.95"), "B": Fr("0.8"), "C": Fr("0.9")}
P3 = w.fprob(lambda s: w.works(T3, s), PR3)
assert P3 == Fr("0.684") and P3 < min(PR3.values())
assert w.fprob(lambda s: w.works(T3, s), PR3, given=lambda s: not s["B"]) == 0     # B fails -> the circuit fails

pw = [Fr("0.98") ** n for n in range(1, 7)]
assert [round(float(x), 4) for x in pw] == [0.98, 0.9604, 0.9412, 0.9224, 0.9039, 0.8858]
assert pw[4] >= Fr("0.9") > pw[5]                                    # five units are fine, the sixth breaks 0.9
T5 = w.S(*[w.C(x) for x in "ABCDE"])
assert w.fprob(lambda s: w.works(T5, s), w.same("ABCDE", Fr("0.98"))) == pw[4]

# exam 26A-B-Q3c: P(A)=P(C)=p independent; P(B|A∩C)=q1, P(B|Ā∩C̄)=q2, P(B|A∩C̄)=q3, P(B|Ā∩C)=q4
Q = BANK["26A-B-Q3c"]
assert Q["contextId"] == "26A-B-c3" and "q_1p^2" in Q["solution"].replace(" ", "")
p, q1, q2, q3, q4 = sp.symbols("p q1 q2 q3 q4", positive=True)
QB = {(1, 1): q1, (0, 0): q2, (1, 0): q3, (0, 1): q4}


def wdep(s):
    pb = QB[(int(s["A"]), int(s["C"]))]
    return ((p if s["A"] else 1 - p) * (p if s["C"] else 1 - p) * (pb if s["B"] else 1 - pb))


wdep.ids = ["A", "B", "C"]
PQ1 = w.sprob(lambda s: w.works(T3, s), wdep)
assert w.eq(PQ1, q1 * p ** 2)
PB = w.sprob(lambda s: s["B"], wdep)                                 # the trap uses P(B), which depends on q2..q4
assert not w.eq(p * PB * p, PQ1)

# ---------------------------------------------------------------- figures
c2 = w.Circ("c2", T2, scale=1.8)
c3 = w.Circ("c3", T3, probs={"A": "0.95", "B": "0.8", "C": "0.9"}, scale=1.25)
c5 = w.Circ("c5", T5, probs=w.same("ABCDE", "0.98"), scale=1.0)
cx = w.Circ("cx", T3, scale=1.1)

ROWS = [(f"${n}$", f"${float(pw[n - 1]):.4f}$",
         "✓" if pw[n - 1] >= Fr("0.9") else "✗") for n in range(1, 7)]
TAB = w.table("tn", ["$n$", "$0.98^n$", "$\\ge 0.9$"], ROWS)

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>שלושה רכיבים: $A$ ו-$C$ בלתי תלויים, '
        '$P(A)=P(C)=p$. התקינות של $B$ תלויה בהם, למשל $P(B\\mid A\\cap C)=q_1$. '
        'מחברים את שלושתם בטור. מה $P(Q_1)$?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד את החיבור הפשוט ביותר במעגל: חיבור בטור."),
    P("נראה למה בטור מכפילים הסתברויות, ולמה כל יחידה נוספת מורידה את האמינות."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">C01 · מעגלים חשמליים</div><h1>טור: כולם חייבים לעבוד</h1>'
         '<p>לחשב את ההסתברות שמעגל בטור פועל, ולזהות מתי הוא פחות אמין מכל יחידה לבדה.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("מעגל בנוי מיחידות. כל יחידה פועלת בהסתברות משלה, בלי תלות באחרות.", do=show("i-c1")),
    P("המעגל פועל אם הזרם יכול לעבור מהכניסה משמאל ליציאה מימין."),
    P("בחיבור **בטור** הזרם עובר דרך כל היחידות, אחת אחרי השנייה.", do=show("c2-ok-A", "c2-ok-B", "c2-on")),
    P("אם $B$ נכשלת, הזרם נעצר בה, וכל המעגל לא פועל.",
      do=hide("c2-ok-B", "c2-on") + show("c2-x-B", "c2-off")),
    P("אותו דבר אם $A$ נכשלת. אין דרך לעקוף יחידה שבטור.",
      do=hide("c2-x-B", "c2-ok-A") + show("c2-ok-B", "c2-x-A")),
    P("לכן המעגל פועל רק כש**גם** $A$ **וגם** $B$ פועלות: זה החיתוך שלהן.",
      do=hide("c2-x-A", "c2-off") + show("c2-ok-A", "c2-on", "i-c2")),
    P("והיחידות בלתי תלויות, ולכן ההסתברות של החיתוך היא מכפלה.", do=show("i-r1"), hold=0.4),
], stage=f'<div class="circ-stack">{c2.svg()}</div>',
   panel=st.card("i-c1", "plain", "$S$ = המעגל פועל")
         + st.card("i-c2", "ex", "$S=A\\cap B$")
         + st.card("i-r1", "rule", "🔑 $P(S)=P(A)\\cdot P(B)$"))

ex1 = Scene("ex1", "שלוש יחידות", [
    P("שלוש יחידות בטור: $0.95$, $0.8$ ו-$0.9$.", do=show("a-1")),
    P("המעגל פועל רק כששלושתן פועלות, ולכן מכפילים את שלוש ההסתברויות.",
      do=show("c3-ok-A", "c3-ok-B", "c3-ok-C", "c3-on")),
    P("$0.95$ כפול $0.8$ זה $0.76$. ועוד כפול $0.9$: $0.684$.", do=show("a-2"),
      say="0.95 כפול 0.8 זה 0.76. ועוד כפול 0.9: 0.684."),
    P("עכשיו בדיקת שפיות. היחידה החלשה היא $B$, עם $0.8$.",
      do=hide("c3-ok-A", "c3-ok-C", "c3-on") + show("a-3")),
    P("והתוצאה, $0.684$, קטנה ממנה. כך זה חייב להיות תמיד."),
    P("כי כל כפל במספר שקטן מאחת רק מקטין את התוצאה.", hold=0.3),
    P("אז אם יצא לכם מעגל בטור שאמין יותר מהיחידה החלשה שלו, יש טעות בחישוב.", do=show("a-r")),
    P("ושימו לב: לא מחברים ולא עושים ממוצע. בטור כל יחידה היא עוד תנאי שחייב להתקיים.", do=show("a-t"), hold=0.4),
], stage=f'<div class="circ-stack">{c3.svg()}</div>',
   panel=st.card("a-1", "plain", "$P(A)=0.95,\\ P(B)=0.8,\\ P(C)=0.9$")
         + st.card("a-2", "ex", "$P(S)=0.95\\cdot0.8\\cdot0.9=0.684$")
         + st.card("a-3", "plain", "החלשה: $0.8$, ו-$0.684<0.8$ ✓")
         + st.card("a-r", "rule", "🔑 בטור: $P(S)\\le\\min_i p_i$")
         + st.card("a-t", "trap", "⚠️ לא סכום ולא ממוצע: כל יחידה היא עוד <b>וגם</b>"))

ex2 = Scene("ex2", "עוד יחידה, פחות אמינות", [
    P("ועכשיו יחידות זהות, כל אחת פועלת בהסתברות $0.98$. זו יחידה אמינה מאוד.", do=show("b-1")),
    P("כשיש $n$ יחידות זהות בטור, מכפילים $n$ פעמים את אותו מספר: $p$ בחזקת $n$.", do=show("b-2"),
      say="כשיש אֶן יחידות זהות בטור, מכפילים אֶן פעמים את אותו מספר: פִּי בחזקת אֶן."),
    P("השאלה: כמה יחידות כאלה אפשר לשים בטור, כך שהמעגל עדיין יפעל בהסתברות $0.9$ לפחות?",
      say="השאלה: כמה יחידות כאלה אפשר לשים בטור, כך שהמעגל עדיין יפעל בהסתברות 0.9 לפחות?", do=show("b-3")),
    P("יחידה אחת: $0.98$. שתיים: $0.9604$. שלוש: $0.9412$.", do=show("tn-r-0", "tn-r-1", "tn-r-2"),
      say="יחידה אחת: 0.98. שתיים: 0.9604. שלוש: 0.9412."),
    P("ארבע: $0.9224$. חמש: $0.9039$, עדיין מעל $0.9$.", do=show("tn-r-3", "tn-r-4"),
      say="ארבע: 0.9224. חמש: 0.9039, עדיין מעל 0.9."),
    P("ובשש יחידות יורדים ל-$0.8858$, מתחת לסף.", do=show("tn-r-5"), say="ובשש יחידות יורדים ל0.8858, מתחת לסף."),
    P("אז מותר לכל היותר חמש יחידות. יחידות מצוינות, אבל כל אחת מוסיפה עוד סיכוי לתקלה.", do=show("b-4"), hold=0.4),
], stage=f'<div class="circ-stack">{c5.svg()}{TAB}</div>',
   panel=st.card("b-1", "plain", "כל יחידה: $p=0.98$")
         + st.card("b-2", "rule", "🔑 $n$ יחידות זהות בטור: $P(S)=p^n$")
         + st.card("b-3", "ex", "מה ה-$n$ הגדול ביותר עם $0.98^n\\ge0.9$?")
         + st.card("b-4", "rule", "🔑 $n=5$: יותר יחידות בטור = פחות אמינות"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: בקו ייצור מדפיסים שלושה רכיבים, $A$, $B$ ו-$C$, זה לצד זה.",
      say="שאלה ממבחן: בקו ייצור מדפיסים שלושה רכיבים, אֵיי, בִּי וסִי, זה לצד זה."),
    P("$A$ ו-$C$ בלתי תלויים, וכל אחד מהם תקין בהסתברות $p$.", do=show("x-1"),
      say="אֵיי וסִי בלתי תלויים, וכל אחד מהם תקין בהסתברות פִּי."),
    P("אבל $B$ תלוי בהם: לכל מצב של $A$ ו-$C$ נתונה ההסתברות ש-$B$ תקין.", do=show("x-2"),
      say="אבל בִּי תלוי בהם: לכל מצב של אֵיי וסִי נתונה ההסתברות שבִּי תקין."),
    P("למשל, אם $A$ ו-$C$ שניהם תקינים, $B$ תקין בהסתברות $q_1$.",
      say="למשל, אם אֵיי וסִי שניהם תקינים, בִּי תקין בהסתברות קְיוּ אחת."),
    P("מחברים את שלושתם בטור. מה ההסתברות שהמעגל פועל?", do=show("xr-ring-q1")),
    P("בטור כולם חייבים לעבוד, ולכן המאורע הוא החיתוך של שלושתם.", do=hide("xr-ring-q1") + show("cx-ok-A", "cx-ok-B", "cx-ok-C", "x-3"),
      say="בטור כולם חייבים לעבוד, ולכן המאורע הוא החיתוך של שלושתם."),
    P("קודם $A$ ו-$C$: הם בלתי תלויים, ולכן שניהם תקינים בהסתברות $p$ בריבוע.",
      say="קודם אֵיי וסִי: הם בלתי תלויים, ולכן שניהם תקינים בהסתברות פִּי בריבוע."),
    P("ועכשיו $B$. אנחנו כבר בעולם שבו $A$ ו-$C$ תקינים, ושם $B$ תקין בהסתברות $q_1$.", do=show("x-4"),
      say="ועכשיו בִּי. אנחנו כבר בעולם שבו אֵיי וסִי תקינים, ושם בִּי תקין בהסתברות קְיוּ אחת."),
    P("כלל הכפל נותן: $p$ בריבוע כפול $q_1$.", do=show("x-5"), say="כלל הכפל נותן: פִּי בריבוע כפול קְיוּ אחת.", hold=0.3),
    P("שלוש ההסתברויות המותנות האחרות לא נכנסות בכלל: בטור צריך רק את המקרה שבו כולם תקינים."),
    P("והמלכודת: לכפול $p$ כפול $P(B)$ כפול $p$, כאילו $B$ בלתי תלוי.", do=show("x-t"),
      say="והמלכודת: לכפול פִּי כפול ההסתברות של בִּי כפול פִּי, כאילו בִּי בלתי תלוי."),
    P("אבל $B$ תלוי ב-$A$ וב-$C$, ולכן את ההסתברות שלו כופלים רק בגרסה המותנית.", hold=0.5,
      say="אבל בִּי תלוי באֵיי ובסִי, ולכן את ההסתברות שלו כופלים רק בגרסה המותנית."),
], stage='<div class="circ-stack">'
         + '<div class="circ-row">' + st.raster("xr", "images/exams/26A-B-Q3-circuits.png", 250, (480, 490),
                                                 rings=[("q1", 232, 100, 120)])
         + f'{cx.svg()}</div>'
         + st.card("x-3", "ex", r"$Q_1=A\cap B\cap C$")
         + st.card("x-4", "ex", r"$P(Q_1)=P(A\cap C)\cdot P(B\mid A\cap C)$")
         + st.card("x-5", "rule", r"🔑 $P(Q_1)=p^2\,q_1$") + '</div>',
   panel=STEM
         + st.card("x-1", "plain", r"$P(A)=P(C)=p$, בלתי תלויים")
         + st.card("x-2", "plain", r"$P(B\mid A\cap C)=q_1$ (ועוד שלוש)")
         + st.card("x-t", "trap", r"⚠️ לא $p\cdot P(B)\cdot p$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בטור הזרם עובר דרך כל היחידות, ולכן המעגל פועל רק כשכולן פועלות.", do=show("r-1")),
    P("ליחידות בלתי תלויות מכפילים את כל ההסתברויות, וליחידות זהות: $p$ בחזקת $n$.", do=show("r-2"),
      say="ליחידות בלתי תלויות מכפילים את כל ההסתברויות, וליחידות זהות: פִּי בחזקת אֶן."),
    P("התוצאה תמיד קטנה מהיחידה החלשה, וכל יחידה נוספת מורידה אותה.", do=show("r-3")),
    P("וכשיחידה תלויה באחרות, כופלים בהסתברות המותנית שלה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="circ-stack"><div class="circ-big">$P(S)=p_1\\cdot p_2\\cdots p_n$</div></div>',
   panel=st.card("r-1", "rule", "🔑 טור = <b>וגם</b> = חיתוך")
         + st.card("r-2", "rule", "🔑 מכפלה, ו-$p^n$ ליחידות זהות")
         + st.card("r-3", "rule", "🔑 $P(S)\\le\\min_i p_i$")
         + st.card("r-4", "trap", "⚠️ יחידה תלויה: $P(B\\mid\\ldots)$, לא $P(B)$"))

VIDEO = Video("C01", "circ", "טור: כולם חייבים לעבוד", [title, idea, ex1, ex2, exam, recap],
              bank={"26A-B-Q3c": None})
