# -*- coding: utf-8 -*-
"""C08 · יחידות תלויות — video script (build: tools/video/vid.py C08).

Source: courses/circ/C08.js (lesson + goal). Exam anchor: 26A-B-Q3d (A, B, C in parallel; A and C independent with
P = p; P(B|A∩C)=q1, P(B|Ā∩C̄)=q2, P(B|A∩C̄)=q3, P(B|Ā∩C)=q4 as printed): P(Q2) = 1-(1-p)^2(1-q2). Open question (bank key
None), used by no guided quiz. The bank notes that the official solution swapped q2/q4; the video follows the printed
definitions (as the bank's corrected solution does).
Avoided on purpose: 26A-A-Q3a/b/d (pq, p+s(1-p): the symbolic twins of the C08 quiz items Q1/Q2); 26A-B-Q3a/Q3b
(P(B), P(A|B): conditional_bayes / independence topics, left to those courses); every C08 quiz case (p=0.8, q=0.9,
s=0.3 -> 0.72, 0.86, 0.78, 40/43; the q=s independence MCQ; the common source W at 0.9/0.8 -> 0.576) and the
lesson's 0.5/0.6/0.2.
Worked example: P(A)=0.6, P(B|A)=0.9, P(B|Ā)=0.5: series 0.54, parallel 0.8, P(B)=0.74; the independence shortcut
would give 0.444 and 0.896.
Every number is exact (the joint distribution enumerated, w_circ.sprob / Fractions).
"""
from fractions import Fraction as Fr
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

# ---------------------------------------------------------------- numbers (verified)
pA, qB, sB = Fr("0.6"), Fr("0.9"), Fr("0.5")
J = {(1, 1): pA * qB, (1, 0): pA * (1 - qB), (0, 1): (1 - pA) * sB, (0, 0): (1 - pA) * (1 - sB)}
assert J == {(1, 1): Fr("0.54"), (1, 0): Fr("0.06"), (0, 1): Fr("0.2"), (0, 0): Fr("0.2")} and sum(J.values()) == 1
ser = J[(1, 1)]
par = 1 - J[(0, 0)]
PB = J[(1, 1)] + J[(0, 1)]
assert (ser, par, PB) == (Fr("0.54"), Fr("0.8"), Fr("0.74"))
assert par == sum(v for (a, b), v in J.items() if a or b)
assert pA * PB == Fr("0.444") != ser                                   # the independence shortcut, series
assert 1 - (1 - pA) * (1 - PB) == Fr("0.896") != par                    # and parallel
assert w.fprob(lambda s: s["A"] and s["B"], {"A": pA, "B": PB}) == Fr("0.444")   # = what independent units would give

# exam 26A-B-Q3d
Q = BANK["26A-B-Q3d"]
assert Q["contextId"] == "26A-B-c3" and "1-(1-q_2)(1-p)^2" in Q["solution"].replace(" ", "")
p, q1, q2, q3, q4 = sp.symbols("p q1 q2 q3 q4", positive=True)
QB = {(1, 1): q1, (0, 0): q2, (1, 0): q3, (0, 1): q4}                   # (A, C) -> P(B | ...), printed definitions


def wdep(s):
    pb = QB[(int(s["A"]), int(s["C"]))]
    return (p if s["A"] else 1 - p) * (p if s["C"] else 1 - p) * (pb if s["B"] else 1 - pb)


wdep.ids = ["A", "B", "C"]
T2 = w.Pa(w.C("A"), w.C("B"), w.C("C"))
PQ2 = w.sprob(lambda s: w.works(T2, s), wdep)
assert w.eq(PQ2, 1 - (1 - p) ** 2 * (1 - q2))
assert w.eq(w.sprob(lambda s: not any(s.values()), wdep), (1 - p) ** 2 * (1 - q2))
assert not w.eq(PQ2, 1 - (1 - p) ** 2 * (1 - q4)) and not w.eq(PQ2, 1 - (1 - p) ** 2 * (1 - q1))
PBs = w.sprob(lambda s: s["B"], wdep)
assert not w.eq(PQ2, 1 - (1 - p) ** 2 * (1 - PBs))                      # the trap: P(B) as if independent

# ---------------------------------------------------------------- figures
cs = w.Circ("cs", w.S(w.C("A"), w.C("B")), scale=1.0)
cp = w.Circ("cp", w.Pa(w.C("A"), w.C("B")), scale=1.0)
cx = w.Circ("cx", T2, scale=0.95)
JT = w.table("jt", ["", "$B$", "$\\overline B$"], [
    ("$A$", "$0.6\\cdot0.9=0.54$", "$0.6\\cdot0.1=0.06$"),
    ("$\\overline A$", "$0.4\\cdot0.5=0.2$", "$0.4\\cdot0.5=0.2$")])

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>$A$ ו-$C$ בלתי תלויים, $P(A)=P(C)=p$. '
        'התקינות של $B$ תלויה בהם: $P(B\\mid\\overline A\\cap\\overline C)=q_2$ (ועוד שלוש). '
        'מחברים את שלושתם במקביל. מה $P(Q_2)$?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("עד עכשיו כל היחידות היו בלתי תלויות. בסרטון הזה הן כבר לא."),
    P("נראה איך מחשבים טור ומקביל, כשמצב של יחידה אחת משנה את הסיכוי של אחרת."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">C08 · מעגלים חשמליים</div><h1>יחידות תלויות</h1>'
         '<p>לחשב הסתברות של מעגל כשמצב יחידה אחת משנה את ההסתברות של האחרת.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("כשיחידות תלויות, השאלה נותנת הסתברויות מותנות. למשל: $P(A)$, ואת הסיכוי של $B$ בכל מצב של $A$.", do=show("i-1"),
      say="כשיחידות תלויות, השאלה נותנת הסתברויות מותנות. למשל: ההסתברות של אֵיי, ואת הסיכוי של בִּי בכל מצב של אֵיי."),
    P("את המכפלה $P(A)P(B)$ כבר אי אפשר לכתוב. במקומה: כלל הכפל.", do=show("i-r1"),
      say="את המכפלה של שתי ההסתברויות כבר אי אפשר לכתוב. במקומה: כלל הכפל."),
    P("ההסתברות ששתיהן פועלות היא $P(A)$, כפול הסיכוי של $B$ **בעולם שבו $A$ פועלת**.",
      say="ההסתברות ששתיהן פועלות היא ההסתברות של אֵיי, כפול הסיכוי של בִּי בעולם שבו אֵיי פועלת."),
    P("וזה עובד בכל צירוף: גם ששתיהן נכשלות, גם שרק אחת פועלת. בוחרים את ההתניה המתאימה.", do=show("i-r2"), hold=0.4),
], stage='<div class="circ-stack"><div class="circ-big">$P(A\\cap B)=P(A)\\cdot P(B\\mid A)$</div>'
         '<div class="circ-mid">$P(\\overline A\\cap\\overline B)=P(\\overline A)\\cdot P(\\overline B\\mid\\overline A)$</div></div>',
   panel=st.card("i-1", "plain", "נתון: $P(A)$, $P(B\\mid A)$, $P(B\\mid\\overline A)$")
         + st.card("i-r1", "rule", "🔑 כלל הכפל במקום מכפלה")
         + st.card("i-r2", "rule", "🔑 ההתניה לפי המצב של היחידה השנייה"))

ex1 = Scene("ex1", "דוגמה", [
    P("$A$ פועלת בהסתברות $0.6$. אם $A$ פועלת, $B$ פועלת ב-$0.9$. ואם לא, רק ב-$0.5$.", do=show("a-0"),
      say="אֵיי פועלת בהסתברות 0.6. אם אֵיי פועלת, בִּי פועלת ב0.9. ואם לא, רק ב0.5."),
    P("נבנה את כל ארבעת הצירופים. $A$ ו-$B$: $0.6$ כפול $0.9$, כלומר $0.54$.", do=show("jt-r-0"),
      say="נבנה את כל ארבעת הצירופים. אֵיי ובִּי: 0.6 כפול 0.9, כלומר 0.54."),
    P("$A$ לא פועלת: $0.4$. ואז $B$ פועלת בחצי מהמקרים: $0.2$, ונכשלת ב-$0.2$.", do=show("jt-r-1"),
      say="אֵיי לא פועלת: 0.4. ואז בִּי פועלת בחצי מהמקרים: 0.2, ונכשלת ב0.2."),
    P("בטור צריך את שתיהן: $0.54$. כבר מופיע בטבלה.", do=show("cs-ok-A", "cs-ok-B", "cs-on", "a-1"),
      say="בטור צריך את שתיהן: 0.54. כבר מופיע בטבלה."),
    P("במקביל המעגל נכשל רק כששתיהן נכשלות: $0.2$. ולכן הוא פועל ב-$0.8$.",
      do=show("cp-x-A", "cp-x-B", "cp-off", "a-2"), say="במקביל המעגל נכשל רק כששתיהן נכשלות: 0.2. ולכן הוא פועל ב0.8."),
    P("ומה הסיכוי של $B$ לבדה? סוכמים את העמודה שלה: $0.54$ ועוד $0.2$, כלומר $0.74$.", do=show("a-3"),
      say="ומה הסיכוי של בִּי לבדה? סוכמים את העמודה שלה: 0.54 ועוד 0.2, כלומר 0.74.", hold=0.3),
    P("וזו המלכודת: לקחת את $0.74$ ולכפול, כאילו הן בלתי תלויות.", do=show("a-t"),
      say="וזו המלכודת: לקחת את 0.74 ולכפול, כאילו הן בלתי תלויות."),
    P("בטור זה נותן $0.444$ במקום $0.54$, ובמקביל $0.896$ במקום $0.8$. שתי התשובות שגויות.", do=show("a-4"),
      say="בטור זה נותן 0.444 במקום 0.54, ובמקביל 0.896 במקום 0.8. שתי התשובות שגויות.", hold=0.4),
], stage=f'<div class="circ-stack">{JT}<div class="circ-row">{cs.svg()}{cp.svg()}</div></div>',
   panel=st.card("a-0", "plain", "$P(A)=0.6,\\ P(B\\mid A)=0.9,\\ P(B\\mid\\overline A)=0.5$")
         + st.card("a-1", "ex", "טור: $P(A\\cap B)=0.54$")
         + st.card("a-2", "ex", "מקביל: $1-0.2=0.8$")
         + st.card("a-3", "plain", "$P(B)=0.54+0.2=0.74$")
         + st.card("a-t", "trap", "⚠️ לא כופלים ב-$P(B)$ כשיש תלות")
         + st.card("a-4", "plain", "$0.6\\cdot0.74=0.444\\ne0.54$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: בקו ייצור מדפיסים שלושה רכיבים. $A$ ו-$C$ בלתי תלויים, כל אחד תקין בהסתברות $p$.",
      say="שאלה ממבחן: בקו ייצור מדפיסים שלושה רכיבים. אֵיי וסִי בלתי תלויים, כל אחד תקין בהסתברות פִּי."),
    P("הרכיב האמצעי, $B$, תלוי בשניהם. לכל אחד מארבעת המצבים של $A$ ו-$C$ נתונה הסתברות אחרת.", do=show("x-1"),
      say="הרכיב האמצעי, בִּי, תלוי בשניהם. לכל אחד מארבעת המצבים של אֵיי וסִי נתונה הסתברות אחרת."),
    P("מחברים את שלושתם במקביל. מה ההסתברות שהמעגל פועל?"),
    P("מקביל: הדרך הקלה היא המשלים. המעגל נכשל רק כששלושתם נכשלים.", do=show("cx-x-A", "cx-x-B", "cx-x-C", "cx-off")),
    P("קודם $A$ ו-$C$: הם בלתי תלויים, ולכן שניהם נכשלים בהסתברות $(1-p)^2$.", do=show("x-2"),
      say="קודם אֵיי וסִי: הם בלתי תלויים, ולכן שניהם נכשלים בהסתברות אחת פחות פִּי, בריבוע."),
    P("ועכשיו $B$, בעולם שבו $A$ ו-$C$ שניהם תקולים. שם הוא תקין בהסתברות $q_2$.",
      say="ועכשיו בִּי, בעולם שבו אֵיי וסִי שניהם תקולים. שם הוא תקין בהסתברות קְיוּ שתיים."),
    P("ולכן הוא תקול בהסתברות $1-q_2$.", do=show("x-3"), say="ולכן הוא תקול בהסתברות אחת פחות קְיוּ שתיים."),
    P("כלל הכפל: שלושתם נכשלים בהסתברות $(1-p)^2$ כפול $1-q_2$.",
      say="כלל הכפל: שלושתם נכשלים בהסתברות אחת פחות פִּי, בסוגריים, בריבוע, כפול אחת פחות קְיוּ שתיים."),
    P("וההסתברות שהמעגל פועל היא אחת פחות המכפלה הזאת.", do=hide("cx-x-A", "cx-x-B", "cx-x-C", "cx-off") + show("cx-on", "x-4"),
      say="וההסתברות שהמעגל פועל היא אחת פחות המכפלה הזאת.", hold=0.3),
    P("שימו לב: מתוך ארבע ההסתברויות המותנות, רק אחת נכנסת. במקביל צריך רק את המקרה שבו כולם נכשלים."),
    P("ובמבחן הזה קל להתבלבל בין $q_2$ ל-$q_4$. קראו בדיוק: $q_2$ היא ההתניה על $A$ וגם $C$ תקולים.", do=show("x-5"),
      say="ובמבחן הזה קל להתבלבל בין קְיוּ שתיים לקְיוּ ארבע. קראו בדיוק: קְיוּ שתיים היא ההתניה על אֵיי וגם סִי תקולים."),
    P("והמלכודת: להכניס את $P(B)$ במקום $q_2$, כאילו $B$ בלתי תלוי. זה פשוט מספר אחר.", do=show("x-t"),
      say="והמלכודת: להכניס את ההסתברות של בִּי במקום קְיוּ שתיים, כאילו בִּי בלתי תלוי. זה פשוט מספר אחר.", hold=0.5),
], stage='<div class="circ-stack">'
         + '<div class="circ-row">' + st.raster("xr", "images/exams/26A-B-Q3-circuits.png", 260, (480, 490))
         + f'{cx.svg()}</div>'
         + st.card("x-2", "plain", "$P(\\overline A\\cap\\overline C)=(1-p)^2$")
         + st.card("x-3", "plain", "$P(\\overline B\\mid\\overline A\\cap\\overline C)=1-q_2$")
         + st.card("x-4", "rule", "🔑 $P(Q_2)=1-(1-p)^2(1-q_2)$") + '</div>',
   panel=STEM
         + st.card("x-1", "plain", "$P(B\\mid A\\cap C)=q_1,\\ P(B\\mid\\overline A\\cap\\overline C)=q_2$")
         + st.card("x-5", "trap", "⚠️ $q_2$: שניהם תקולים, לא $q_4$")
         + st.card("x-t", "trap", "⚠️ לא $1-(1-p)^2(1-P(B))$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כשיחידות תלויות, כל מכפלה של שתי הסתברויות הופכת לכלל הכפל, עם ההתניה הנכונה.", do=show("r-1")),
    P("בטור צריך את המקרה שבו כולם פועלים, ובמקביל את המקרה שבו כולם נכשלים.", do=show("r-2")),
    P("וההסתברות של יחידה לבדה באה מהסתברות שלמה, אבל לא כופלים בה כשיש תלות.", do=show("r-3")),
    P("וקראו בעיון איזו הסתברות מותנית שייכת לאיזה מצב. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="circ-stack"><div class="circ-big">$P(A\\cap B)=P(A)\\,P(B\\mid A)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 כלל הכפל עם ההתניה")
         + st.card("r-2", "rule", "🔑 טור: כולם פועלים. מקביל: כולם נכשלים")
         + st.card("r-3", "trap", "⚠️ $P(B)$ שולית לא נכנסת למכפלה")
         + st.card("r-4", "trap", "⚠️ איזו התניה שייכת לאיזה מצב"))

VIDEO = Video("C08", "circ", "יחידות תלויות", [title, idea, ex1, exam, recap],
              bank={"26A-B-Q3d": None})
