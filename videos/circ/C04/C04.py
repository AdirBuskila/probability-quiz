# -*- coding: utf-8 -*-
"""C04 · טריק המשלים — video script (build: tools/video/vid.py C04).

Source: courses/circ/C04.js (lesson + goal). Exam anchor: 25S-A-Q5a (road map: each road open with probability p,
independently; Eugene reaches the institute by road A or by the detour C, D, B): P1 = 1-(1-p)(1-p^3) = p+p^3-p^4.
Open question (bank key None), used by no guided quiz.
Avoided on purpose: every C04 quiz case (5 units of 0.3 in parallel, the smallest n for 0.5 and 0.99, "at least one
fails" for 3 units of 0.9 in series, AB||CD at 0.7, 3 units of 0.8 in parallel failing, 25B-A-Q3a gates/bridges)
and the lesson's 3 units of 0.5; 25S-A-Q5b/c (the same map) are kept for the boss video C09.
Worked examples: four units of 0.8 in series vs in parallel ("at least one fails" 0.5904 in both, "the circuit
fails" 0.5904 vs 0.0016); the smallest n of 0.6-units in parallel for 0.999 (n = 8).
Every number is exact (Fractions / sympy over the full truth table, w_circ).
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

# ---------------------------------------------------------------- numbers (verified)
U4 = "ABCD"
PR = w.same(U4, Fr("0.8"))
TS, TP = w.S(*[w.C(x) for x in U4]), w.Pa(*[w.C(x) for x in U4])
one_fails = w.fprob(lambda s: not all(s.values()), PR)
assert one_fails == 1 - Fr("0.8") ** 4 == Fr("0.5904")
assert 1 - w.fprob(lambda s: w.works(TS, s), PR) == one_fails          # series: "circuit fails" = "one fails"
assert 1 - w.fprob(lambda s: w.works(TP, s), PR) == Fr("0.2") ** 4 == Fr("0.0016")
assert w.fprob(lambda s: any(s.values()), PR) == 1 - Fr("0.0016") == Fr("0.9984")

pf = [Fr("0.4") ** n for n in range(1, 10)]
n_min = next(n for n in range(1, 10) if 1 - pf[n - 1] >= Fr("0.999"))
assert n_min == 8 and pf[6] == Fr("0.0016384") and pf[7] == Fr("0.00065536")
assert 1 - pf[6] < Fr("0.999") <= 1 - pf[7]
T8 = w.Pa(*[w.C(x) for x in "ABCDEFGH"])
assert w.fprob(lambda s: w.works(T8, s), w.same("ABCDEFGH", Fr("0.6"))) == 1 - pf[7]

# exam 25S-A-Q5a: Eugene reaches the institute through A, or through C, D, B (the pub and Serge's home)
Q = BANK["25S-A-Q5a"]
assert Q["contextId"] == "25S-A-c5" and "p+p^3-p^4" in Q["solution"].replace(" ", "")
p = w.p
TE = w.Pa(w.C("A"), w.N(w.S(w.C("C"), w.C("D"), w.C("B")), "cdb"))
PE = w.sprob(lambda s: w.works(TE, s), w.same("ABCD"))
assert w.eq(PE, p + p ** 3 - p ** 4) and w.eq(PE, 1 - (1 - p) * (1 - p ** 3))
assert w.eq(1 - PE, (1 - p) * (1 - p ** 3))
assert not w.eq(PE, p + p ** 3)                                         # the trap: adding the two routes

# ---------------------------------------------------------------- figures
cs = w.Circ("cs", TS, scale=0.95)
cp = w.Circ("cp", TP, scale=0.88)
cx = w.Circ("cx", TE, tags={"cdb": "p³"}, scale=1.0)
ROWS = [(f"${n}$", f"${float(pf[n - 1]):.6g}$", "✓" if 1 - pf[n - 1] >= Fr("0.999") else "✗") for n in (6, 7, 8)]
TAB = w.table("tn", ["$n$", "$0.4^n$", "$1-0.4^n\\ge0.999$"], ROWS)

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>כל אחד מהכבישים $A,B,C,D$ פתוח בהסתברות $p$, '
        'בלי תלות. יוג׳ין מגיע למכון ישירות בכביש $A$, או דרך הפאב וביתו של סרג׳. מה ההסתברות שהוא מגיע?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד את הכלי החזק ביותר בשאלות של לפחות ונכשל: המשלים."),
    P("נראה מתי הוא חוסך הרבה עבודה, ואיפה קל להתבלבל בין שני משלימים שונים."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">C04 · מעגלים חשמליים</div><h1>טריק המשלים</h1>'
         '<p>לחשב "לפחות אחת פועלת" ו"המעגל נכשל" דרך המשלים, גם כשיש הרבה יחידות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("לפעמים הדרך הישירה כוללת הרבה תרחישים. למשל: לפחות אחת מעשר יחידות פועלת."),
    P("זה אומר בדיוק אחת, או שתיים, או שלוש, וכן הלאה. הרבה מקרים לחבר.", do=show("i-1")),
    P("אבל למאורע ההפוך יש תרחיש **אחד** בלבד: אף יחידה לא פועלת.", do=show("i-2")),
    P("אז מחשבים את המשלים, שהוא בדרך כלל מכפלה, ומחסירים מאחת.", do=show("i-r1"), hold=0.3),
    P("ומה המשלים של כולן פועלות? לפחות אחת **נכשלת**. גם הוא מחושב כאחת פחות מכפלה.", do=show("i-r2"), hold=0.4),
], stage='<div class="circ-stack"><div class="circ-big">$P(\\text{at least one})=1-P(\\text{none})$</div></div>',
   panel=st.card("i-1", "plain", "ישירות: הרבה תרחישים")
         + st.card("i-2", "plain", "המשלים: תרחיש <b>אחד</b>")
         + st.card("i-r1", "rule", "🔑 לפחות אחת פועלת: $1-\\prod(1-p_i)$")
         + st.card("i-r2", "rule", "🔑 לפחות אחת נכשלת: $1-\\prod p_i$"))

ex1 = Scene("ex1", "שני משלימים", [
    P("ארבע יחידות, כל אחת פועלת בהסתברות $0.8$. נחבר אותן פעם בטור, ופעם במקביל.", do=show("a-0"),
      say="ארבע יחידות, כל אחת פועלת בהסתברות 0.8. נחבר אותן פעם בטור, ופעם במקביל."),
    P("השאלה הראשונה: מה ההסתברות שלפחות יחידה אחת נכשלת?"),
    P("המשלים: כל הארבע פועלות, $0.8$ בחזקת ארבע, כלומר $0.4096$.", do=show("cs-ok-A", "cs-ok-B", "cs-ok-C", "cs-ok-D", "a-1"),
      say="המשלים: כל הארבע פועלות, 0.8 בחזקת ארבע, כלומר 0.4096."),
    P("ולכן לפחות אחת נכשלת בהסתברות $0.5904$. וזה נכון בשני החיבורים: זו שאלה על היחידות, לא על המעגל.",
      do=hide("cs-ok-A", "cs-ok-B", "cs-ok-C", "cs-ok-D") + show("a-2"),
      say="ולכן לפחות אחת נכשלת בהסתברות 0.5904. וזה נכון בשני החיבורים: זו שאלה על היחידות, לא על המעגל."),
    P("השאלה השנייה: מה ההסתברות ש**המעגל** נכשל?", do=show("a-q2")),
    P("בטור, יחידה אחת שנכשלת מפילה את המעגל. ולכן גם כאן: $0.5904$.", do=show("cs-x-C", "cs-off", "a-3"),
      say="בטור, יחידה אחת שנכשלת מפילה את המעגל. ולכן גם כאן: 0.5904."),
    P("אבל במקביל המעגל נכשל רק כשכל הארבע נכשלות: $0.2$ בחזקת ארבע, $0.0016$.",
      do=show("cp-x-A", "cp-x-B", "cp-x-C", "cp-x-D", "cp-off", "a-4"),
      say="אבל במקביל המעגל נכשל רק כשכל הארבע נכשלות: 0.2 בחזקת ארבע, 0.0016."),
    P("זו המלכודת: לפחות אחת נכשלת, והמעגל נכשל, הם אותו דבר רק בטור.", do=show("a-t"), hold=0.4),
], stage=f'<div class="circ-stack">{cs.svg()}{cp.svg()}</div>',
   panel=st.card("a-0", "plain", "ארבע יחידות, כל אחת $0.8$")
         + st.card("a-1", "plain", "כולן פועלות: $0.8^4=0.4096$")
         + st.card("a-2", "ex", "לפחות אחת נכשלת: $1-0.4096=0.5904$")
         + st.card("a-q2", "plain", "ומתי <b>המעגל</b> נכשל?")
         + st.card("a-3", "plain", "בטור: $0.5904$")
         + st.card("a-4", "plain", "במקביל: $0.2^4=0.0016$")
         + st.card("a-t", "trap", "⚠️ יחידה נכשלת ≠ המעגל נכשל"))

ex2 = Scene("ex2", "כמה יחידות צריך?", [
    P("שאלה הפוכה: יחידות של $0.6$ במקביל. כמה צריך, כדי שהמעגל יפעל בהסתברות $0.999$ לפחות?",
      say="שאלה הפוכה: יחידות של 0.6 במקביל. כמה צריך, כדי שהמעגל יפעל בהסתברות 0.999 לפחות?", do=show("b-1")),
    P("עם $n$ יחידות, המעגל נכשל רק כשכולן נכשלות: $0.4$ בחזקת $n$.", do=show("b-2"),
      say="עם אֶן יחידות, המעגל נכשל רק כשכולן נכשלות: 0.4 בחזקת אֶן."),
    P("ולכן צריך שהכישלון הזה יהיה לכל היותר אחד חלקי אלף.", do=show("b-3")),
    P("שש יחידות: הכישלון גדול מדי. שבע: $0.0016$, עדיין גדול מאחד חלקי אלף.", do=show("tn-r-0", "tn-r-1"),
      say="שש יחידות: הכישלון גדול מדי. שבע: 0.0016, עדיין גדול מאחד חלקי אלף."),
    P("שמונה: $0.00066$ בקירוב. סוף סוף מתחת לסף.", do=show("tn-r-2"), say="שמונה: 0.00066 בקירוב. סוף סוף מתחת לסף."),
    P("אז צריך שמונה יחידות. ושימו לב: מחפשים את ה-$n$ הקטן ביותר שעובר, ובודקים גם את זה שלפניו.", do=show("b-r"),
      say="אז צריך שמונה יחידות. ושימו לב: מחפשים את האֶן הקטן ביותר שעובר, ובודקים גם את זה שלפניו.", hold=0.4),
], stage=f'<div class="circ-stack">{TAB}</div>',
   panel=st.card("b-1", "plain", "כל יחידה $0.6$, יעד: $P(S)\\ge0.999$")
         + st.card("b-2", "plain", "$P(\\text{fail})=0.4^n$")
         + st.card("b-3", "ex", "צריך $0.4^n\\le0.001$")
         + st.card("b-r", "rule", "🔑 $n=8$: הקטן ביותר שעובר את הסף"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מפת כבישים. כל כביש פתוח בהסתברות $p$, בלי תלות בשאר.",
      say="שאלה ממבחן: מפת כבישים. כל כביש פתוח בהסתברות פִּי, בלי תלות בשאר."),
    P("שימו לב: בשאלה כתוב שכביש **נסגר** בהסתברות $1-p$. כלומר פתוח בהסתברות $p$.",
      say="שימו לב: בשאלה כתוב שכביש נסגר בהסתברות אחת פחות פִּי. כלומר פתוח בהסתברות פִּי."),
    P("מה ההסתברות שיוג׳ין מגיע מביתו למכון?"),
    P("יש לו שתי דרכים. הראשונה: כביש $A$, ישירות.", do=show("xr-ring-a"), say="יש לו שתי דרכים. הראשונה: כביש אֵיי, ישירות."),
    P("השנייה: עקיפה. כביש $C$ לפאב, $D$ לבית של סרג׳, ו-$B$ למכון.", do=hide("xr-ring-a") + show("xr-ring-c", "xr-ring-d", "xr-ring-b"),
      say="השנייה: עקיפה. כביש סִי לפאב, דִּי לבית של סרג׳, ובִּי למכון."),
    P("זה בדיוק מעגל: $A$ במקביל לטור של $C$, $D$ ו-$B$.", do=hide("xr-ring-c", "xr-ring-d", "xr-ring-b") + show("cx"),
      say="זה בדיוק מעגל: אֵיי במקביל לטור של סִי, דִּי ובִּי."),
    P("עכשיו המשלים: יוג׳ין לא מגיע רק אם $A$ סגור, **וגם** הדרך העוקפת חסומה.", do=show("cx-x-A", "x-1"),
      say="עכשיו המשלים: יוג׳ין לא מגיע רק אם אֵיי סגור, וגם הדרך העוקפת חסומה."),
    P("הדרך העוקפת פתוחה כששלושת הכבישים פתוחים: $p^3$. ולכן היא חסומה בהסתברות $1-p^3$.",
      do=show("cx-blk-cdb", "cx-bt-cdb", "x-2"),
      say="הדרך העוקפת פתוחה כששלושת הכבישים פתוחים: פִּי בשלישית. ולכן היא חסומה בהסתברות אחת פחות, פִּי בשלישית."),
    P("כאן השתמשנו במשלים פעם שנייה: חסומה, פירושו שלפחות כביש אחד בה סגור."),
    P("שני האירועים בלתי תלויים, כי אין להם כבישים משותפים. מכפילים: $(1-p)(1-p^3)$.", do=show("x-3"),
      say="שני האירועים בלתי תלויים, כי אין להם כבישים משותפים. מכפילים: אחת פחות פִּי, כפול אחת פחות, פִּי בשלישית."),
    P("ולכן $P_1$ הוא אחת פחות המכפלה, כלומר $p+p^3-p^4$.", do=hide("cx-x-A") + show("cx-on", "x-4"),
      say="ולכן פֵּא אחת היא אחת פחות המכפלה, כלומר פִּי ועוד פִּי בשלישית פחות פִּי בחזקת ארבע.", hold=0.3),
    P("המלכודת: לחבר את שתי הדרכים, $p$ ועוד $p^3$. אבל הן יכולות להיות פתוחות יחד.", do=show("x-t"),
      say="המלכודת: לחבר את שתי הדרכים, פִּי ועוד פִּי בשלישית. אבל הן יכולות להיות פתוחות יחד."),
    P("את החיתוך הזה, $p^4$, צריך להחסיר. בדיוק מה שהמשלים עשה בשבילנו.", hold=0.5,
      say="את החיתוך הזה, פִּי בחזקת ארבע, צריך להחסיר. בדיוק מה שהמשלים עשה בשבילנו."),
], stage='<div class="circ-stack">'
         + '<div class="circ-row">' + st.raster("xr", "images/exams/25S-A-Q5-map.png", 340, (556, 482),
                                                 rings=[("a", 150, 125, 48), ("c", 150, 345, 48), ("d", 430, 350, 48),
                                                        ("b", 440, 120, 48)])
         + f'<div id="cx" class="h">{cx.svg()}</div></div>'
         + st.card("x-3", "ex", "$P(\\overline{Q_E})=(1-p)(1-p^3)$")
         + st.card("x-4", "rule", "🔑 $P_1=1-(1-p)(1-p^3)=p+p^3-p^4$") + '</div>',
   panel=STEM
         + st.card("x-1", "plain", "לא מגיע $\\iff$ $A$ סגור <b>וגם</b> העקיפה חסומה")
         + st.card("x-2", "plain", "העקיפה חסומה: $1-p^3$")
         + st.card("x-t", "trap", "⚠️ לא $p+p^3$: חסר $-p^4$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כשרואים לפחות, או נכשל, מחשבים קודם את המשלים ומחסירים מאחת.", do=show("r-1")),
    P("לפחות אחת פועלת: אחת פחות מכפלת הכישלונות. לפחות אחת נכשלת: אחת פחות מכפלת ההצלחות.", do=show("r-2")),
    P("לפחות יחידה אחת נכשלת, והמעגל נכשל, הם אותו דבר רק בטור.", do=show("r-3")),
    P("ובשאלת כמה יחידות צריך, בודקים את ה-$n$ הקטן ביותר שעובר את הסף. נתראה ברמה הבאה.", do=show("r-4"),
      say="ובשאלת כמה יחידות צריך, בודקים את האֶן הקטן ביותר שעובר את הסף. נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="circ-stack"><div class="circ-big">$P(A)=1-P(\\overline{A})$</div></div>',
   panel=st.card("r-1", "rule", "🔑 לפחות / נכשל: דרך המשלים")
         + st.card("r-2", "rule", "🔑 $1-\\prod(1-p_i)$ מול $1-\\prod p_i$")
         + st.card("r-3", "trap", "⚠️ יחידה נכשלת ≠ המעגל נכשל")
         + st.card("r-4", "rule", "🔑 $(1-p)^n\\le1-\\text{target}$"))

VIDEO = Video("C04", "circ", "טריק המשלים", [title, idea, ex1, ex2, exam, recap],
              bank={"25S-A-Q5a": None})
