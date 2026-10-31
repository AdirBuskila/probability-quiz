# -*- coding: utf-8 -*-
"""G05 · קימורים: היפרבולה, פרבולה ומעגל — video script (build: tools/video/vid.py G05).

Source: courses/geo/C05.js (lesson + goal). Exam anchor: 24S-B-Q1b (a rectangle with sides X,Y~U(0,1), diagonal
L = sqrt(X^2+Y^2); P(L<1/2) = pi/16), an open question (bank key None) that no guided quiz uses.
Avoided on purpose: the C05 quiz cases (Y<X^2, XY<1/5, XY<1/3, radius 1/3, Y>X^2 in (0,1)x(0,2)), C07's XY<1/10 and
XY>1/2, the lesson's XY<1/4, and every bank hyperbola part (24S-B-Q1a, 25B-A-Q1c, 24A-A-Q1a, 25A-C-Q1a: each is a
quiz value in disguise or the boss 25B-A-Q1d denominator); also P(L<1) = pi/4 (24S-A-Q1b, 25B-A-Q1b: the boss numerator).
Worked examples: P(XY<1/6) = (1+ln 6)/6 (two pieces), P(Y<3X^2/4) = 1/4 (one integral).
Areas: sympy integrals, the drawn polygon's shoelace area, and Monte Carlo must all agree.
"""
from fractions import Fraction as Fr
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

U = ((0, 1), (0, 1))
x = sp.Symbol("x", positive=True)
c = sp.Rational(1, 6)
S1a = c * 1                                                    # 0 < x < 1/6: the curve is above 1
S1b = sp.integrate(c / x, (x, c, 1))
S1 = sp.simplify(S1a + S1b)
assert sp.simplify(S1b - c * sp.log(6)) == 0 and sp.simplify(S1 - (1 + sp.log(6)) / 6) == 0
V1 = float(S1)
assert abs(V1 - 0.46529) < 1e-4
g.mc(lambda a, b: a * b < 1 / 6, *U, V1)
assert abs(float(S1b) - 0.29863) < 1e-4                      # the trap: the integral alone

S2 = sp.integrate(sp.Rational(3, 4) * x ** 2, (x, 0, 1))
assert S2 == sp.Rational(1, 4)                                 # the parabola y = 3x^2/4 stays below 3/4 < 1
g.mc(lambda a, b: b < .75 * a ** 2, *U, 0.25)

# exam 24S-B-Q1b: X^2 + Y^2 < 1/4 in the unit square
Q = BANK["24S-B-Q1b"]
assert "\\frac\\pi{16}" in Q["solution"].replace(" ", "") and Q["contextId"] == "24S-B-c1"
r = sp.Rational(1, 2)
SX = sp.integrate(sp.sqrt(r ** 2 - x ** 2), (x, 0, r))
assert sp.simplify(SX - sp.pi / 16) == 0 and r <= 1             # a quarter disc that fits in the square
g.mc(lambda a, b: a * a + b * b < .25, *U, math.pi / 16)
assert sp.simplify(sp.pi * r ** 2 - sp.pi / 4) == 0             # the whole disc: pi/4, four times too much

# ---------------------------------------------------------------- figures
pa = g.Plane("pa", *U, maxw=440, maxh=440, xticks=[(1 / 6, "1/6"), (1, "1")], yticks=[(1, "1")])
ar1 = pa.slab("s1", lambda t: 0, lambda t: 1, 0, 1 / 6, "warn")
ar2 = pa.slab("s2", lambda t: 0, lambda t: 1 / (6 * t), 1 / 6, 1, "ev")
assert abs(ar1 - 1 / 6) < 1e-9 and abs(ar1 + ar2 - V1) < 2e-4
pa.curve("c", lambda t: 1 / (6 * t), 0.15, 1, label="y = 1/(6x)", at=(.45, 1 / 2.7), dx=6, dy=-12)
pa.seg("v", (1 / 6, 0), (1 / 6, 1), cls="ln alt", dash=True)
pa.text("t1", 1 / 12, .5, "1/6")

pb = g.Plane("pb", *U, maxw=440, maxh=440, xticks=[(1, "1")], yticks=[(.75, "3/4"), (1, "1")])
ar3 = pb.slab("s", lambda t: 0, lambda t: .75 * t * t, 0, 1, "ev")
assert abs(ar3 - .25) < 1e-3
pb.curve("c", lambda t: .75 * t * t, 0, 1, label="y = 3x²/4", at=(.55, .75 * .55 ** 2), dx=-10, dy=-22, anchor="end")
pb.text("t", .8, .18, "1/4")

px = g.Plane("px", *U, maxw=440, maxh=440, xticks=[(.5, "1/2"), (1, "1")], yticks=[(.5, "1/2"), (1, "1")])
ar4 = px.slab("s", lambda t: 0, lambda t: math.sqrt(max(.25 - t * t, 0)), 0, .5, "ev", n=400)
assert abs(ar4 - math.pi / 16) < 1e-4
px.curve("c", lambda t: math.sqrt(max(.25 - t * t, 0)), 0, .5, n=400, label="x² + y² = 1/4", at=(.36, .36),
         dx=10, dy=-6)
px.text("t", .2, .17, "π/16")

FIG = st.raster("x-fig", "images/exams/24S-B-Q1-rect.png", 420, (613, 409))
STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>מלבן עם צלעות '
        '<span class="nobr">$X,Y\\sim U_c(0,1)$</span> בלתי תלויות, ואלכסון $L$. מצאו את '
        '$P\\left(L<\\frac12\\right)$.</div>')

title = Scene("title", "", [
    P("בסרטון הזה הגבול של האירוע כבר לא קו ישר, אלא עקום."),
    P("נחשב שטח מתחת להיפרבולה, מתחת לפרבולה, וברבע עיגול.", hold=0.4),
], stage='<div class="kicker">G05 · הסתברות גיאומטרית</div><h1>קימורים: היפרבולה, פרבולה ומעגל</h1>'
         '<p>לחשב שטח מתחת לעקום וברבע עיגול, ולהפוך אותו להסתברות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("עד עכשיו הגבולות היו קווים ישרים, והשטחים היו משולשים ומלבנים."),
    P("כשהאירוע הוא $Y$ קטן מ-$f$ של $X$, הגבול הוא העקום $y$ שווה $f$ של $x$.",
      say="כשהאירוע הוא וַואי קטן מאֶף של אִקְס, הגבול הוא העקום וַואי שווה אֶף של אִקְס.", do=show("i-1")),
    P("לכל $x$, הנקודות המתאימות הן קטע אנכי מאפס עד העקום. אבל לא מעל הצלע העליונה.",
      say="לכל אִקְס, הנקודות המתאימות הן קטע אנכי מאפס עד העקום. אבל לא מעל הצלע העליונה.", do=show("i-2")),
    P("השטח הוא סכום הקטעים האלה: האינטגרל של הגובה.", do=show("i-3"), hold=0.4),
], stage='<div class="geo-stack"><div id="i-3" class="geo-big h">$S=\\int_0^1\\min\\big(f(x),\\,1\\big)\\,dx$</div></div>',
   panel=st.card("i-1", "plain", "האירוע $Y<f(X)$: מתחת לעקום")
         + st.card("i-2", "rule", "🔑 לכל $x$: גובה $\\min(f(x),1)$"))

hyp = Scene("hyp", "היפרבולה", [
    P("נתחיל במכפלה: מה ההסתברות ש-$XY$ קטן משישית, בריבוע היחידה?",
      say="נתחיל במכפלה: מה ההסתברות שאִקְס כפול וַואי קטן משישית, בריבוע היחידה?", do=show("a-q")),
    P("מבודדים את $y$: הוא צריך להיות קטן משישית חלקי $x$. זו היפרבולה.",
      say="מבודדים את וַואי: הוא צריך להיות קטן משישית חלקי אִקְס. זו היפרבולה.", do=show("pa-c", "a-1")),
    P("הדרך לא משתנה: מציירים את הגבול, בוחרים צד, ומחשבים שטח. רק שהשטח הוא אינטגרל."),
    P("אבל שימו לב: כש-$x$ קטן משישית, העקום נמצא מעל הריבוע.", say="אבל שימו לב: כשאִקְס קטן משישית, העקום נמצא מעל הריבוע.",
      do=show("pa-v")),
    P("שם כל $y$ בין אפס לאחת מתאים. זו רצועה מלאה, והשטח שלה שישית.",
      say="שם כל וַואי בין אפס לאחת מתאים. זו רצועה מלאה, והשטח שלה שישית.", do=show("pa-s1", "pa-t1", "a-2")),
    P("ומשישית עד אחת, הגובה הוא העקום עצמו: אינטגרל של שישית חלקי $x$.",
      say="ומשישית עד אחת, הגובה הוא העקום עצמו: אינטגרל של שישית חלקי אִקְס.", do=show("pa-s2")),
    P("האינטגרל של אחת חלקי $x$ הוא לוגריתם טבעי. מציבים: שישית כפול לוגריתם של שש.",
      say="האינטגרל של אחת חלקי אִקְס הוא לוגריתם טבעי. מציבים: שישית כפול לוגריתם של שש.", do=show("a-3")),
    P("למה לוגריתם של שש? בגבול העליון, לוגריתם של אחת הוא אפס. ומחסירים את לוגריתם של שישית, שהוא מינוס לוגריתם של שש."),
    P("סך הכול: אחת ועוד לוגריתם של שש, חלקי שש. בערך ארבעים ושש וחצי אחוז.", do=show("a-4"), hold=0.3),
    P("המלכודת: לשכוח את הרצועה המלאה, ולענות רק את האינטגרל. אז השטח קטן מדי.", do=show("a-5"), hold=0.4),
], stage=f'<div class="geo-stack">{pa.svg()}</div>',
   panel=st.card("a-q", "ex", "$P\\left(XY<\\frac16\\right)=\\,?\\quad X,Y\\sim U_c(0,1)$")
         + st.card("a-1", "plain", "$XY<\\frac16\\iff y<\\frac1{6x}$")
         + st.card("a-2", "plain", "$0<x<\\frac16$: הכול, שטח $\\frac16$")
         + st.card("a-3", "plain", "$\\int_{1/6}^{1}\\frac{dx}{6x}=\\frac16\\ln6$")
         + st.card("a-4", "rule", "🔑 $P=\\dfrac{1+\\ln6}{6}\\approx0.465$")
         + st.card("a-5", "trap", "⚠️ בלי הרצועה: $\\frac{\\ln 6}{6}\\approx0.299$"))

pow3 = Scene("pow3", "פרבולה", [
    P("ועכשיו פרבולה שלא יוצאת מהריבוע: מה ההסתברות ש-$Y$ קטן משלושה רבעים, כפול $X$ בריבוע?",
      say="ועכשיו פרבולה שלא יוצאת מהריבוע: מה ההסתברות שוַואי קטן משלושה רבעים, כפול אִקְס בריבוע?", do=show("b-q", "pb-c")),
    P("הגובה של הפרבולה תמיד בין אפס לשלושה רבעים, כלומר בתוך הריבוע. לכן מספיק אינטגרל אחד.", do=show("pb-s")),
    P("האינטגרל של שלושה רבעים, כפול $x$ בריבוע, מאפס עד אחת: שלושה רבעים כפול שליש, כלומר רבע.",
      say="האינטגרל של שלושה רבעים, כפול אִקְס בריבוע, מאפס עד אחת: שלושה רבעים כפול שליש, כלומר רבע.", do=show("pb-t", "b-1")),
    P("הכלל: בכל קטע של $x$ שואלים מי הגבול העליון, העקום או הצלע של הריבוע.",
      say="הכלל: בכל קטע של אִקְס שואלים מי הגבול העליון, העקום או הצלע של הריבוע.", do=show("b-2"), hold=0.4),
], stage=f'<div class="geo-stack">{pb.svg()}</div>',
   panel=st.card("b-q", "ex", "$P\\left(Y<\\frac34X^2\\right)=\\,?$")
         + st.card("b-1", "rule", "🔑 $\\int_0^1\\frac34x^2\\,dx=\\frac34\\cdot\\frac13=\\frac14$")
         + st.card("b-2", "rule", "🔑 בכל קטע: הגבול העליון הוא העקום או הצלע"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מלבן שאורכי הצלעות שלו אחידים בין אפס לאחת, ובלתי תלויים."),
    P("יהי $L$ אורך האלכסון. מה ההסתברות ש-$L$ קטן מחצי?", say="יהי אֶל אורך האלכסון. מה ההסתברות שאֶל קטן מחצי?"),
    P("לפי פיתגורס, האלכסון הוא שורש של $X$ בריבוע ועוד $Y$ בריבוע.",
      say="לפי פיתגורס, האלכסון הוא שורש של אִקְס בריבוע ועוד וַואי בריבוע."),
    P("שני הצדדים חיוביים, אז מעלים בריבוע: $x$ בריבוע ועוד $y$ בריבוע, קטן מרבע.",
      say="שני הצדדים חיוביים, אז מעלים בריבוע: אִקְס בריבוע ועוד וַואי בריבוע, קטן מרבע.", do=show("x-1")),
    P("אלה הנקודות שהמרחק שלהן מהראשית קטן מחצי: עיגול ברדיוס חצי.",
      do=hide("x-fig") + show("x-pl", "px-c", "px-s")),
    P("הרדיוס הוא השורש של רבע, כלומר חצי. לא רבע.", do=show("x-3")),
    P("ובתוך הריבוע נמצא רק רבע מהעיגול, ברבע הראשון.", hold=0.2),
    P("השטח: רבע כפול פאי כפול רדיוס בריבוע. כלומר פאי חלקי שש עשרה.", do=show("px-t")),
    P("השטח של אומגה הוא אחת, ולכן ההסתברות היא פאי חלקי שש עשרה, בערך עשרים אחוז.", hold=0.3),
    P("שתי מלכודות: לקחת רבע בתור הרדיוס, או לחשב את כל העיגול. שתיהן נותנות תשובה לא נכונה.", do=show("x-t"), hold=0.3),
    P("ועוד שאלה בסגנון מבחן: ומה ההסתברות שהאלכסון קצר משלושה חצאים?", do=show("x-6")),
    P("האלכסון הארוך ביותר האפשרי הוא שורש שתיים, בערך אחת נקודה ארבע. לכן זה קורה תמיד: ההסתברות אחת.", hold=0.5),
], stage=(f'<div class="geo-swap" style="--swap-h:560px"><div id="x-fig">{FIG}</div>'
          f'<div id="x-pl" class="h">{px.svg()}</div></div>'),
   panel=STEM
         + st.card("x-1", "plain", "$L=\\sqrt{X^2+Y^2}<\\frac12\\iff x^2+y^2<\\frac14$")
         + st.card("x-3", "rule", "🔑 $r=\\frac12,\\ \\ P=\\frac{\\pi r^2}{4}=\\frac{\\pi}{16}\\approx0.196$")
         + st.card("x-t", "trap", "⚠️ לא רדיוס $\\frac14$, ולא עיגול שלם")
         + st.card("x-6", "ex", "$L<\\frac32$: תמיד, כי $L\\le\\sqrt2<\\frac32$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: עקום במקום קו? אותה שיטה, והשטח הוא אינטגרל.", do=show("r-1")),
    P("כשהעקום יוצא מהריבוע, מפצלים לקטעים: רצועה מלאה, ואחריה אינטגרל.", do=show("r-2")),
    P("ואינטגרל של אחת חלקי $x$ הוא לוגריתם טבעי.", say="ואינטגרל של אחת חלקי אִקְס הוא לוגריתם טבעי.", do=show("r-3")),
    P("ו-$x$ בריבוע ועוד $y$ בריבוע קטן מ-$r$ בריבוע: רבע עיגול ברדיוס $r$, כש-$r$ לכל היותר אחת. נתראה ברמה הבאה.",
      say="ואִקְס בריבוע ועוד וַואי בריבוע קטן מאָר בריבוע: רבע עיגול ברדיוס אָר, כשאָר לכל היותר אחת. נתראה ברמה הבאה.",
      do=show("r-4"), hold=0.6),
], stage='<div class="geo-stack"><div class="geo-big">$S=\\int_a^b f(x)\\,dx$</div></div>',
   panel=st.card("r-1", "rule", "🔑 עקום: השטח הוא אינטגרל")
         + st.card("r-2", "rule", "🔑 העקום מעל הריבוע? רצועה מלאה")
         + st.card("r-3", "rule", "🔑 $\\int\\frac{dx}{x}=\\ln x$")
         + st.card("r-4", "rule", "🔑 $x^2+y^2<r^2$, כש-$r\\le1$: רבע עיגול, $\\frac{\\pi r^2}{4}$"))

VIDEO = Video("G05", "geo", "קימורים: היפרבולה, פרבולה ומעגל", [title, idea, hyp, pow3, exam, recap], bank={"24S-B-Q1b": None})
