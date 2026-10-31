# -*- coding: utf-8 -*-
"""G07 · יחס ומכפלה — video script (build: tools/video/vid.py G07).

Source: courses/geo/C07.js (lesson + goal). Exam anchor: 26A-B-Q1a (Q = [[X,1],[0,Y]], X,Y~U(0,1); the CDF of
D = det Q = XY: F_D(t) = t - t ln t on (0,1)), an open question (bank key None) that no guided quiz uses.
Avoided on purpose: the C07 quiz cases (X/Y<1/3, X/Y>2, the formula F(t) for t>1, XY<1/10, XY>1/2, Y/X<1 in
(0,1)x(0,2)) and their twins 25A-B-Q1a..d (Z = X/Y); no ratio formula for general t is stated, and the product CDF is
never evaluated at a quiz value. Worked examples: P(X/Y<2/5) = 1/5 (a triangle under the top side) and
P(X/Y<4) = 7/8 (the complement triangle on the right side).
Areas: exact polygons for the ratio, sympy for the product; Monte Carlo for both.
"""
from fractions import Fraction as Fr
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

U = ((0, 1), (0, 1))
# ratio X/Y < t  <=>  y > x/t  (y > 0):  a*x + b*y < 0 with a = 1, b = -t
E1 = [(1, -Fr(2, 5), 0, "<")]
A1 = g.area(g.clip(E1, *U))
assert set(g.clip(E1, *U)) == {(0, 0), (0, 1), (Fr(2, 5), 1)} and A1 == Fr(1, 5)
g.mc(lambda a, b: a / b < .4, *U, A1)
E2 = [(1, -4, 0, "<")]
A2 = g.area(g.clip(E2, *U))
C2 = g.area(g.clip([(1, -4, 0, ">")], *U))
assert C2 == Fr(1, 2) * 1 * Fr(1, 4) == Fr(1, 8) and A2 == Fr(7, 8)
g.mc(lambda a, b: a / b < 4, *U, A2)

# exam 26A-B-Q1a: D = det [[X,1],[0,Y]] = XY
Q = BANK["26A-B-Q1a"]
assert "t-t\\lnt" in Q["solution"].replace(" ", "") and Q["contextId"] == "26A-B-c1"
X, Y, t, x = sp.symbols("X Y t x", positive=True)
assert sp.Matrix([[X, 1], [0, Y]]).det() == X * Y
F = sp.simplify(t + sp.integrate(t / x, (x, t, 1)))            # the strip x < t, then the hyperbola y = t/x
assert sp.simplify(F - (t - t * sp.log(t))) == 0
assert sp.limit(F, t, 0, "+") == 0 and F.subs(t, 1) == 1
assert sp.simplify(sp.diff(F, t) + sp.log(t)) == 0              # density -ln t > 0 on (0,1): F increases
for tv in (0.3, 0.7):
    g.mc(lambda a, b: a * b <= tv, *U, float(F.subs(t, tv)))
F03 = float(F.subs(t, sp.Rational(3, 10)))
assert abs(F03 - 0.6612) < 1e-4
assert (-t * sp.log(t)).subs(t, 1) == 0                         # the trap: the integral alone gives 0 at t = 1

# ---------------------------------------------------------------- figures
pa = g.Plane("pa", *U, maxw=420, maxh=420, xticks=[(Fr(2, 5), "2/5"), (1, "1")], yticks=[(1, "1")])
pa.line("l", 5, -2, 0, label="y = 5x/2", at=(.4, 1), dx=10, dy=-14)
pa.region("ev", E1, "ev")
pa.text("t", .12, .7, "1/5")

pb = g.Plane("pb", *U, maxw=420, maxh=420, xticks=[(1, "1")], yticks=[(Fr(1, 4), "1/4"), (1, "1")])
pb.line("l", 1, -4, 0, label="y = x/4", at=(.55, .55 / 4), dx=-6, dy=-16, anchor="end")
pb.region("ev", E2, "ev")
pb.region("cp", [(1, -4, 0, ">")], "comp")
pb.text("tc", .82, .06, "1/8")
pb.text("t", .4, .6, "7/8")

TV = .3
px = g.Plane("px", *U, maxw=360, maxh=360, xticks=[(TV, "t"), (1, "1")], yticks=[(TV, "t"), (1, "1")])
s1 = px.slab("s1", lambda s: 0, lambda s: 1, 0, TV, "warn")
s2 = px.slab("s2", lambda s: 0, lambda s: TV / s, TV, 1, "ev")
assert abs(s1 + s2 - F03) < 2e-4
px.curve("c", lambda s: TV / s, .29, 1, label="y = t/x", at=(.62, TV / .62), dx=6, dy=-12)
px.text("a1", TV / 2, .5, "t")

pf = g.Plane("pf", (0, 1), (0, 1), w=340, h=300, xlab="t", ylab="F(t)", frame=False,
             xticks=[(0, "0"), (1, "1")], yticks=[(1, "1")], view=((-.3, 1.3), (0, 1.1)))
pf.curve("c0", lambda s: 0, -.3, 0, n=5, clip_box=False)
pf.curve("c1", lambda s: s - s * math.log(s) if s > 0 else 0, 1e-6, 1, n=200, clip_box=False)
pf.curve("c2", lambda s: 1, 1, 1.3, n=5, clip_box=False)
pf.curve("bad", lambda s: -s * math.log(s) if s > 0 else 0, 1e-6, 1, n=200, cls="ln alt", clip_box=False)

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>'
        '$\\boldsymbol{Q}=\\begin{pmatrix}X&amp;1\\\\0&amp;Y\\end{pmatrix}$, '
        '<span class="nobr">$X,Y\\sim U_c(0,1)$</span> בלתי תלויים, ו-$D=\\det\\boldsymbol{Q}$. '
        'חשבו את $F_D(t)$.</div>')

title = Scene("title", "", [
    P("בסרטון הזה נחשב התפלגות מצטברת של יחס בין שני משתנים, ושל מכפלה שלהם."),
    P("היחס נותן קו דרך הראשית, והמכפלה נותנת היפרבולה.", hold=0.4),
], stage='<div class="kicker">G07 · הסתברות גיאומטרית</div><h1>יחס ומכפלה</h1>'
         '<p>לחשב את ההתפלגות המצטברת של היחס $X/Y$ ושל המכפלה $XY$, ולהשתמש בה לחישוב הסתברויות.</p>',
   layout="title")

mini = []
for k, (tv, lab) in enumerate([(Fr(1, 2), "t = 1/2"), (Fr(1), "t = 1"), (Fr(2), "t = 2")]):
    m = g.Plane(f"m{k}", *U, maxw=250, maxh=250, xticks=[(1, "1")], yticks=[(1, "1")])
    m.region("r", [(1, -tv, 0, "<")], "ev", shown=True)
    m.line("l", 1, -tv, 0, shown=True)
    m.text("lab", .5, -.42, lab, shown=True, cls="geo-lt")
    mini.append(m)

idea = Scene("idea", "הרעיון", [
    P("כשמגדירים משתנה חדש מתוך $X$ ו-$Y$, למשל יחס או מכפלה, מחפשים את ההתפלגות המצטברת שלו.",
      say="כשמגדירים משתנה חדש מתוך אִקְס ווַואי, למשל יחס או מכפלה, מחפשים את ההתפלגות המצטברת שלו."),
    P("$F$ של $t$ היא השטח של האזור שבו המשתנה קטן מ-$t$. לכל $t$, אזור אחר.",
      say="אֶף של טִי היא השטח של האזור שבו המשתנה קטן מטִי. לכל טִי, אזור אחר.", do=show("i-0")),
    P("ביחס, האזור תמיד מעל קו שיוצא מהראשית. וכש-$t$ גדל, הקו נעשה מתון יותר.",
      say="ביחס, האזור תמיד מעל קו שיוצא מהראשית. וכשטִי גדל, הקו נעשה מתון יותר.", do=show("i-1", "i-2", "i-3")),
    P("השאלה החשובה: איפה הקו יוצא מהריבוע. מזה נקבעת הצורה, וגם הנוסחה.", hold=0.4),
], stage=(f'<div class="geo-stack"><div id="i-0" class="geo-mid h">$F_Z(t)=P(Z\\le t)=\\dfrac{{S(\\{{Z\\le t\\}})}}{{|\\Omega|}}$</div>'
          f'<div class="geo-row"><div id="i-1" class="h">{mini[0].svg()}</div><div id="i-2" class="h">{mini[1].svg()}</div>'
          f'<div id="i-3" class="h">{mini[2].svg()}</div></div></div>'), layout="full")

ratio = Scene("ratio", "היחס", [
    P("נתחיל ביחס: מה ההסתברות ש-$X$ חלקי $Y$ קטן משתי חמישיות, בריבוע היחידה?",
      say="נתחיל ביחס: מה ההסתברות שאִקְס חלקי וַואי קטן משתי חמישיות, בריבוע היחידה?", do=show("a-q")),
    P("$Y$ חיובי, אז מותר לכפול בו בלי להפוך את סימן האי-שוויון.", say="וַואי חיובי, אז מותר לכפול בו בלי להפוך את סימן האי-שוויון.",
      do=show("a-1")),
    P("מקבלים: $y$ גדול מחמישה חצאים $x$. זה האזור מעל קו שיוצא מהראשית.",
      say="מקבלים: וַואי גדול מחמישה חצאים אִקְס. זה האזור מעל קו שיוצא מהראשית.", do=show("pa-l")),
    P("הקו תלול, ולכן הוא פוגש קודם את הצלע העליונה: ב-$x$ שתי חמישיות.", say="הקו תלול, ולכן הוא פוגש קודם את הצלע העליונה: באִקְס שתי חמישיות.",
      do=show("pa-ev")),
    P("האזור הוא משולש: בסיס של שתי חמישיות למעלה, וגובה אחת. השטח: חמישית.", do=show("pa-t", "a-2"), hold=0.4),
], stage=f'<div class="geo-stack">{pa.svg()}</div>',
   panel=st.card("a-q", "ex", "$P\\left(\\frac XY<\\frac25\\right)=\\,?\\quad X,Y\\sim U_c(0,1)$")
         + st.card("a-1", "rule", "🔑 $\\frac XY<t\\iff y>\\frac xt$ (כי $Y>0$)")
         + st.card("a-2", "rule", "🔑 משולש: $\\frac12\\cdot\\frac25\\cdot1=\\frac15$"))

ratio2 = Scene("ratio2", "יחס גדול מאחת", [
    P("ועכשיו: מה ההסתברות ש-$X$ חלקי $Y$ קטן מארבע?", say="ועכשיו: מה ההסתברות שאִקְס חלקי וַואי קטן מארבע?", do=show("b-q")),
    P("הקו הוא $y$ שווה $x$ חלקי ארבע. הוא מתון, ופוגש את הצלע הימנית בגובה רבע.",
      say="הקו הוא וַואי שווה אִקְס חלקי ארבע. הוא מתון, ופוגש את הצלע הימנית בגובה רבע.", do=show("pb-l")),
    P("האירוע הוא מעל הקו: כמעט כל הריבוע. אז מחשבים את המשלים, המשולש שמתחת.", do=show("pb-ev", "pb-cp")),
    P("בסיס אחת, גובה רבע: שמינית. וההסתברות: שבע שמיניות.", do=show("pb-tc", "pb-t", "b-1")),
    P("ההבדל בין שתי הדוגמאות: כשהסף קטן מאחת הקו יוצא מהצלע העליונה, וכשהוא גדול מאחת, מהצלע הימנית.",
      do=show("b-2")),
    P("בסף אחת בדיוק, הקו הוא האלכסון. לכן תמיד בודקים קודם איפה הקו יוצא מהריבוע.", hold=0.4),
], stage=f'<div class="geo-stack">{pb.svg()}</div>',
   panel=st.card("b-q", "ex", "$P\\left(\\frac XY<4\\right)=\\,?$")
         + st.card("b-1", "rule", "🔑 $1-\\frac12\\cdot1\\cdot\\frac14=\\frac78$")
         + st.card("b-2", "trap", "⚠️ סף קטן מ-$1$: צלע עליונה. גדול מ-$1$: צלע ימנית"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מטריצה בגודל שתיים על שתיים. באלכסון $X$ ו-$Y$, אחידים בין אפס לאחת ובלתי תלויים.",
      say="שאלה ממבחן: מטריצה בגודל שתיים על שתיים. באלכסון אִקְס ווַואי, אחידים בין אפס לאחת ובלתי תלויים."),
    P("מעל האלכסון אחת, ומתחתיו אפס. מצאו את ההתפלגות המצטברת של הדטרמיננטה."),
    P("המטריצה משולשית, ולכן הדטרמיננטה היא מכפלת האלכסון: $X$ כפול $Y$. האחת לא משפיעה.",
      say="המטריצה משולשית, ולכן הדטרמיננטה היא מכפלת האלכסון: אִקְס כפול וַואי. האחת לא משפיעה."),
    P("המכפלה תמיד בין אפס לאחת. לכן מתחת לאפס, ההתפלגות המצטברת היא אפס, ומאחת והלאה, אחת.",
      do=show("x-1", "pf-c0", "pf-c2")),
    P("עבור $t$ בין אפס לאחת, מציירים את האזור: $y$ קטן מ-$t$ חלקי $x$.",
      say="עבור טִי בין אפס לאחת, מציירים את האזור: וַואי קטן מטִי חלקי אִקְס.", do=show("px-c")),
    P("משמאל ל-$x$ שווה $t$, ההיפרבולה מעל הריבוע: רצועה מלאה בשטח $t$.",
      say="משמאל לאִקְס שווה טִי, ההיפרבולה מעל הריבוע: רצועה מלאה בשטח טִי.", do=show("px-s1", "px-a1")),
    P("ומימין, האינטגרל של $t$ חלקי $x$, מ-$t$ עד אחת. זה מינוס $t$ כפול לוגריתם של $t$.",
      say="ומימין, האינטגרל של טִי חלקי אִקְס, מטִי עד אחת. זה מינוס טִי כפול לוגריתם של טִי.", do=show("px-s2", "x-3")),
    P("וזה חיובי, כי הלוגריתם של מספר קטן מאחת הוא שלילי.", hold=0.2),
    P("ביחד: $t$ פחות $t$ לוגריתם $t$. השטח של אומגה אחת, וזו ההתפלגות המצטברת.",
      say="ביחד: טִי פחות טִי לוגריתם טִי. השטח של אומגה אחת, וזו ההתפלגות המצטברת.", do=show("x-4", "pf-c1"), hold=0.3),
    P("בדיקה: כש-$t$ שואף לאפס, מקבלים אפס. וב-$t$ שווה אחת, מקבלים אחת. הגרף רציף.",
      say="בדיקה: כשטִי שואף לאפס, מקבלים אפס. ובטִי שווה אחת, מקבלים אחת. הגרף רציף."),
    P("והמלכודת: לשכוח את הרצועה. אז ב-$t$ שווה אחת יוצא אפס, וזו לא יכולה להיות התפלגות מצטברת.",
      say="והמלכודת: לשכוח את הרצועה. אז בטִי שווה אחת יוצא אפס, וזו לא יכולה להיות התפלגות מצטברת.", do=show("pf-bad", "x-t"), hold=0.5),
], stage=f'<div class="geo-row">{px.svg()}{pf.svg()}</div>',
   panel=STEM
         + st.card("x-1", "plain", "$D=XY$<br>$F_D=0$ עבור $t<0$, ו-$F_D=1$ עבור $t\\ge1$")
         + st.card("x-3", "plain", "$t+\\int_t^1\\frac tx\\,dx=t-t\\,\\ln t$")
         + st.card("x-4", "rule", "🔑 $F_D(t)=t-t\\,\\ln t$, $\\;0<t<1$")
         + st.card("x-t", "trap", "⚠️ בלי הרצועה: $-t\\,\\ln t$, ו-$F(1)=0$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: יחס קטן מ-$t$ הוא האזור מעל קו דרך הראשית.", say="לסיכום: יחס קטן מטִי הוא האזור מעל קו דרך הראשית.", do=show("r-1")),
    P("איפה הקו יוצא מהריבוע, בצלע העליונה או בימנית, קובע את הצורה.", do=show("r-2")),
    P("מכפלה קטנה מ-$t$ היא האזור מתחת להיפרבולה: רצועה מלאה, ועוד אינטגרל.",
      say="מכפלה קטנה מטִי היא האזור מתחת להיפרבולה: רצועה מלאה, ועוד אינטגרל.", do=show("r-3")),
    P("ובסוף בודקים: התפלגות מצטברת מתחילה באפס, עולה, ומגיעה לאחת. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="geo-stack"><div class="geo-big">$\\frac XY<t\\iff y>\\frac xt\\qquad XY<t\\iff y<\\frac tx$</div></div>',
   panel=st.card("r-1", "rule", "🔑 יחס: קו דרך הראשית")
         + st.card("r-2", "rule", "🔑 צלע עליונה: משולש. צלע ימנית: משלים")
         + st.card("r-3", "rule", "🔑 מכפלה: רצועה $t$ ועוד $\\int_t^1\\frac tx\\,dx$")
         + st.card("r-4", "trap", "⚠️ בודקים $F(0)=0$ ו-$F(1)=1$"))

VIDEO = Video("G07", "geo", "יחס ומכפלה", [title, idea, ratio, ratio2, exam, recap], bank={"26A-B-Q1a": None})
