# -*- coding: utf-8 -*-
"""G04 · הסתברות מותנית: שטח החיתוך חלקי שטח התנאי — video script (build: tools/video/vid.py G04).

Source: courses/geo/C04.js (lesson + goal). Exam anchor: 25S-A-Q1d (grasshopper, X1~U(0,1), X2~U(0,2);
P(X1>1/2 | X1+X2>2) = 3/4), an open question (bank key None) that no guided quiz uses.
Avoided on purpose: the C04 quiz cases (the condition X+Y<1 and its area 1/2, X<1/4 | X+Y<1, Y<1 | X+Y>1 in
(0,1)x(0,2), X>1/2 | Y>X), the lesson example (X+Y<1 | X<1/2) and the bank conditionals given the triangle X+Y<=1
(24A-C-Q1b..d, 24A-D-Q1c), whose denominator is the C04-Q1 answer.
Worked example: P(X+Y>1 | X>1/3) = (4/9)/(2/3) = 2/3 in the unit square.
Every area is an exact polygon (w_geo.clip), cross-checked by the closed form and by Monte Carlo (conditional).
"""
from fractions import Fraction as Fr
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

U = ((0, 1), (0, 1))
x = sp.Symbol("x")
B1 = [(1, 0, Fr(1, 3), ">")]
AB1 = B1 + [(1, 1, 1, ">")]
SB1 = g.area(g.clip(B1, *U))
SAB1 = g.area(g.clip(AB1, *U))
assert SB1 == Fr(2, 3)
assert SAB1 == Fr(4, 9) == sp.integrate(x, (x, Fr(1, 3), 1))          # height above y = 1 - x is x
assert SAB1 == (Fr(1, 3) + 1) / 2 * Fr(2, 3)                          # trapezoid: sides 1/3 and 1, width 2/3
P1 = SAB1 / SB1
assert P1 == Fr(2, 3)
g.mc(lambda a, b: a + b > 1, *U, P1, given=lambda a, b: a > 1 / 3)
assert g.area(g.clip([(1, 1, 1, ">")], *U)) == Fr(1, 2)               # the trap: unconditioned P(X+Y>1)

# example 2: P(X<Y | Y<2/3) = (2/9)/(2/3) = 1/3
B2 = [(0, 1, Fr(2, 3), "<")]
AB2 = B2 + [(1, -1, 0, "<")]
SB2, SAB2 = g.area(g.clip(B2, *U)), g.area(g.clip(AB2, *U))
assert SB2 == Fr(2, 3) and SAB2 == Fr(1, 2) * Fr(2, 3) ** 2 == Fr(2, 9) and SAB2 / SB2 == Fr(1, 3)
g.mc(lambda a, b: a < b, *U, Fr(1, 3), given=lambda a, b: b < 2 / 3)

# exam 25S-A-Q1d: x = X1 ~ U(0,1), y = X2 ~ U(0,2)
Q = BANK["25S-A-Q1d"]
assert "\\frac34" in Q["solution"].replace(" ", "") and Q["contextId"] == "25S-A-c1"
R = ((0, 1), (0, 2))
B = [(1, 1, 2, ">")]
AB = B + [(1, 0, Fr(1, 2), ">")]
SB, SAB = g.area(g.clip(B, *R)), g.area(g.clip(AB, *R))
assert SB == Fr(1, 2) and SAB == Fr(3, 8)
assert SAB == sp.integrate(x, (x, Fr(1, 2), 1)) == (Fr(1, 2) + 1) / 2 * Fr(1, 2)
assert SAB / SB == Fr(3, 4)
assert (SAB / 2) == Fr(3, 16)                                         # the trap: dividing by |Omega| = 2
g.mc(lambda a, b: a > .5, *R, Fr(3, 4), given=lambda a, b: a + b > 2)

# ---------------------------------------------------------------- figures
pa = g.Plane("pa", *U, maxw=440, maxh=440, xticks=[(Fr(1, 3), "1/3"), (1, "1")], yticks=[(Fr(2, 3), "2/3"), (1, "1")])
pa.region("B", B1, "given")
pa.line("lb", 1, 0, 1 / 3, cls="ln alt", label="x = 1/3", at=(1 / 3, 1), dx=8, dy=-14)
pa.line("la", 1, 1, 1, label="x + y = 1", at=(.72, .28), dx=12, dy=-12)
pa.region("AB", AB1, "both")
pa.region("Aout", [(1, 0, Fr(1, 3), "<"), (1, 1, 1, ">")], "comp")
pa.text("tb", .8, .07, "2/3")
pa.text("tab", .75, .62, "4/9")

pb = g.Plane("pb", *U, maxw=440, maxh=440, xticks=[(Fr(2, 3), "2/3"), (1, "1")], yticks=[(Fr(2, 3), "2/3"), (1, "1")])
pb.region("B", B2, "given")
pb.line("lb", 0, 1, 2 / 3, cls="ln alt", label="y = 2/3", at=(.75, 2 / 3), dx=0, dy=-14)
pb.line("la", -1, 1, 0, label="y = x", at=(.9, .9), dx=-14, dy=-6, anchor="end")
pb.region("AB", AB2, "both")
pb.region("Aout", [(0, 1, Fr(2, 3), ">"), (1, -1, 0, "<")], "comp")
pb.text("tab", .2, .45, "2/9")

px = g.Plane("px", *R, maxw=300, maxh=520, xlab='X<tspan dy="8" font-size="22">1</tspan>',
             ylab='X<tspan dy="8" font-size="22">2</tspan>', xticks=[(Fr(1, 2), "1/2"), (1, "1")],
             yticks=[(1, "1"), (Fr(3, 2), "3/2"), (2, "2")])
px.poly("om", [(0, 0), (1, 0), (1, 2), (0, 2)], "om")
px.line("lb", 1, 1, 2, cls="ln alt")
px.region("B", B, "given")
px.line("la", 1, 0, .5)
px.region("AB", AB, "both")
px.text("tab", .8, 1.72, "3/8")

FIG = st.raster("x-fig", "images/exams/25S-A-Q1-grasshopper.png", 560, (478, 268))
STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>חגב קופץ פעמיים באותו כיוון: '
        '<span class="nobr">$X_1\\sim U_c(0,1)$</span>, <span class="nobr">$X_2\\sim U_c(0,2)$</span>, בלתי תלויים. '
        'אם ידוע שהאורך הכולל גדול מ-$2$, מה ההסתברות שהקפיצה הראשונה ארוכה מחצי?</div>')

title = Scene("title", "", [
    P("בסרטון הזה נחשב הסתברות מותנית בשיטת השטח."),
    P("נראה למה התנאי מקטין את העולם, ולמה מחלקים בשטח שלו ולא בשטח של המלבן.", hold=0.4),
], stage='<div class="kicker">G04 · הסתברות גיאומטרית</div><h1>הסתברות מותנית</h1>'
         '<p>לחשב $P(A\\mid B)$ בשיטת השטח: לצייר את התנאי, את החיתוך, ולחלק את שני השטחים.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("בהינתן $B$, פירושו: כבר ידוע לנו שהנקודה נפלה בתוך האזור $B$.", say="בהינתן בִּי, פירושו: כבר ידוע לנו שהנקודה נפלה בתוך האזור בִּי.",
      do=show("i-1")),
    P("אז העולם החדש הוא $B$ בלבד. וגם בתוכו, הנקודה אחידה.", say="אז העולם החדש הוא בִּי בלבד. וגם בתוכו, הנקודה אחידה.",
      do=show("i-2")),
    P("ההסתברות של $A$ היא החלק של $B$ שנמצא גם ב-$A$: שטח החיתוך, חלקי שטח התנאי.",
      say="ההסתברות של אֵיי היא החלק של בִּי שנמצא גם באֵיי: שטח החיתוך, חלקי שטח התנאי.", do=show("i-3")),
    P("והשטח של אומגה? הוא מופיע גם במונה וגם במכנה, ולכן מצטמצם.", do=show("i-4"), hold=0.4),
], stage='<div class="geo-stack"><div id="i-3" class="geo-big h">'
         '$P(A\\mid B)=\\dfrac{P(A\\cap B)}{P(B)}=\\dfrac{S(A\\cap B)}{S(B)}$</div></div>',
   panel=st.card("i-1", "plain", "$B$ ידוע: הנקודה בתוך $B$")
         + st.card("i-2", "rule", "🔑 העולם החדש: $B$, ובתוכו אחידות")
         + st.card("i-4", "trap", "⚠️ המכנה הוא $S(B)$, לא $|\\Omega|$"))

ex1 = Scene("ex1", "דוגמה", [
    P("בריבוע היחידה: מה ההסתברות ש-$X+Y$ גדול מאחת, בהינתן ש-$X$ גדול משליש?",
      say="בריבוע היחידה: מה ההסתברות שאִקְס ועוד וַואי גדול מאחת, בהינתן שאִקְס גדול משליש?", do=show("a-q")),
    P("צעד ראשון: התנאי. ימינה מהקו $x$ שווה שליש: רצועה ברוחב שני שלישים.",
      say="צעד ראשון: התנאי. ימינה מהקו אִקְס שווה שליש: רצועה ברוחב שני שלישים.", do=show("pa-B", "pa-lb")),
    P("השטח שלה שני שלישים. זה המכנה.", do=show("pa-tb", "a-1")),
    P("צעד שני: החיתוך. בתוך הרצועה, רק החלק שמעל הקו $x+y$ שווה אחת.",
      say="צעד שני: החיתוך. בתוך הרצועה, רק החלק שמעל הקו אִקְס ועוד וַואי שווה אחת.", do=show("pa-la", "pa-AB")),
    P("לחלק הזה, שמשמאל לרצועה, אין משמעות: הוא בחוץ, כי שם התנאי לא מתקיים.", do=show("pa-Aout")),
    P("החיתוך הוא טרפז: צלע של שליש ב-$x$ שווה שליש, וצלע של אחת ב-$x$ שווה אחת.",
      say="החיתוך הוא טרפז: צלע של שליש באִקְס שווה שליש, וצלע של אחת באִקְס שווה אחת."),
    P("הרוחב שני שלישים. השטח: ממוצע הצלעות כפול הרוחב, ארבע תשיעיות.", do=show("pa-tab", "a-2")),
    P("צעד שלישי: מחלקים. ארבע תשיעיות חלקי שני שלישים: שני שלישים.", do=show("a-3"), hold=0.3),
    P("שימו לב: בלי התנאי ההסתברות היא חצי. התנאי הזיז אותה.", do=show("a-4")),
    P("ואם מחלקים בטעות באחת, השטח של אומגה, יוצא ארבע תשיעיות. זו בדיוק הטעות שצריך להימנע ממנה.", hold=0.4),
], stage=f'<div class="geo-stack">{pa.svg()}</div>',
   panel=st.card("a-q", "ex", "$P\\left(X+Y>1\\mid X>\\frac13\\right)=\\,?$")
         + st.card("a-1", "plain", "המכנה: $S(B)=\\frac23$")
         + st.card("a-2", "plain", "המונה: $S(A\\cap B)=\\frac{\\frac13+1}{2}\\cdot\\frac23=\\frac49$")
         + st.card("a-3", "rule", "🔑 $P=\\dfrac{4/9}{2/3}=\\dfrac23$")
         + st.card("a-4", "trap", "⚠️ בלי התנאי: $\\frac12$. חלוקה ב-$|\\Omega|$: $\\frac49$"))

ex2 = Scene("ex2", "החיתוך בלבד", [
    P("עוד דוגמה קצרה: מה ההסתברות ש-$X$ קטן מ-$Y$, בהינתן ש-$Y$ קטן משני שלישים?",
      say="עוד דוגמה קצרה: מה ההסתברות שאִקְס קטן מוַואי, בהינתן שוַואי קטן משני שלישים?", do=show("b-q")),
    P("התנאי: רצועה אופקית בגובה שני שלישים. השטח שלה שני שלישים.", do=show("pb-B", "pb-lb", "b-1")),
    P("האירוע כולו, מעל האלכסון, גדול הרבה יותר. אבל רוב השטח שלו מחוץ לתנאי.", do=show("pb-la", "pb-Aout")),
    P("נשאר רק המשולש שמתחת לקו: ניצבים של שני שלישים, ושטח של שתי תשיעיות.", do=show("pb-AB", "pb-tab", "b-2")),
    P("ההסתברות: שתי תשיעיות חלקי שני שלישים, כלומר שליש.", do=show("b-3"), hold=0.4),
], stage=f'<div class="geo-stack">{pb.svg()}</div>',
   panel=st.card("b-q", "ex", "$P\\left(X<Y\\mid Y<\\frac23\\right)=\\,?$")
         + st.card("b-1", "plain", "המכנה: $S(B)=\\frac23$")
         + st.card("b-2", "plain", "המונה: $\\frac12\\cdot\\left(\\frac23\\right)^2=\\frac29$")
         + st.card("b-3", "rule", "🔑 $P=\\dfrac{2/9}{2/3}=\\dfrac13$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: חגב קופץ פעמיים באותו כיוון. הקפיצה הראשונה אחידה בין אפס לאחת."),
    P("השנייה אחידה בין אפס לשתיים, והן בלתי תלויות."),
    P("אם ידוע שהאורך הכולל גדול משתיים, מה ההסתברות שהקפיצה הראשונה ארוכה מחצי?", hold=0.2),
    P("מרחב המדגם: מלבן ברוחב אחת ובגובה שתיים.", do=hide("x-fig") + show("x-pl", "px-om")),
    P("התנאי: מעל הקו $x_1+x_2$ שווה שתיים. הוא יוצא מהפינה השמאלית העליונה, ופוגש את הצלע הימנית בגובה אחת.",
      say="התנאי: מעל הקו אִקְס אחת ועוד אִקְס שתיים שווה שתיים. הוא יוצא מהפינה השמאלית העליונה, ופוגש את הצלע הימנית בגובה אחת.",
      do=show("px-lb", "px-B")),
    P("זה משולש עם ניצבים אחת ואחת. השטח שלו חצי. זה המכנה.", do=show("x-1")),
    P("החיתוך: החלק של המשולש שמימין ל-$x_1$ שווה חצי.", say="החיתוך: החלק של המשולש שמימין לאִקְס אחת שווה חצי.",
      do=show("px-la", "px-AB")),
    P("זה טרפז: צלע של חצי ב-$x_1$ שווה חצי, וצלע של אחת בצלע הימנית. הרוחב חצי.",
      say="זה טרפז: צלע של חצי באִקְס אחת שווה חצי, וצלע של אחת בצלע הימנית. הרוחב חצי."),
    P("השטח: ממוצע הצלעות, שלושה רבעים, כפול חצי. שלוש שמיניות.", do=show("px-tab", "x-2")),
    P("מחלקים: שלוש שמיניות חלקי חצי. ההסתברות היא שלושה רבעים.", do=show("x-3"), hold=0.3),
    P("והמלכודת: לחלק בשתיים, השטח של המלבן. אז יוצא שלוש חלקי שש עשרה, וזו טעות.",
      say="והמלכודת: לחלק בשתיים, השטח של המלבן. אז יוצא שלוש חלקי שש עשרה, וזו טעות.", do=show("x-t"), hold=0.5),
], stage=(f'<div class="geo-swap" style="--swap-h:640px"><div id="x-fig">{FIG}</div>'
          f'<div id="x-pl" class="h">{px.svg()}</div></div>'),
   panel=STEM
         + st.card("x-1", "plain", "$B=\\{X_1+X_2>2\\}$: $\\;S(B)=\\frac12$")
         + st.card("x-2", "plain", "$S(A\\cap B)=\\frac{\\frac12+1}{2}\\cdot\\frac12=\\frac38$")
         + st.card("x-3", "rule", "🔑 $P=\\dfrac{3/8}{1/2}=\\dfrac34$")
         + st.card("x-t", "trap", "⚠️ חלוקה ב-$|\\Omega|=2$ נותנת $\\frac3{16}$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בהינתן $B$, העולם מצטמצם ל-$B$.", say="לסיכום: בהינתן בִּי, העולם מצטמצם לבִּי.", do=show("r-1")),
    P("מציירים את התנאי ומחשבים את השטח שלו: זה המכנה.", do=show("r-2")),
    P("מציירים רק את החלק של $A$ שבתוך $B$: זה המונה.", say="מציירים רק את החלק של אֵיי שבתוך בִּי: זה המונה.", do=show("r-3")),
    P("ולא מחלקים בשטח של אומגה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="geo-stack"><div class="geo-big">$P(A\\mid B)=\\dfrac{S(A\\cap B)}{S(B)}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 התנאי $B$ הוא העולם החדש")
         + st.card("r-2", "rule", "🔑 המכנה: $S(B)$")
         + st.card("r-3", "rule", "🔑 המונה: $S(A\\cap B)$, רק בתוך $B$")
         + st.card("r-4", "trap", "⚠️ לא $|\\Omega|$ במכנה"))

VIDEO = Video("G04", "geo", "הסתברות מותנית: שטח החיתוך חלקי שטח התנאי", [title, idea, ex1, ex2, exam, recap],
              bank={"25S-A-Q1d": None})
