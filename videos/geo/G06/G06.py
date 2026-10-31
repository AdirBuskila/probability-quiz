# -*- coding: utf-8 -*-
"""G06 · מקסימום ומינימום: התפלגות מצטברת — video script (build: tools/video/vid.py G06).

Source: courses/geo/C06.js (lesson + goal). Exam anchor: 25S-A-Q1b (grasshopper, X1~U(0,1), X2~U(0,2); P(at least
one jump shorter than 1/2) = P(min(X1,X2) < 1/2) = 5/8), an open question (bank key None) that no guided quiz uses.
Avoided on purpose: the C06 quiz cases (P(max<2/3), P(min>1/4), P(min<1/4), F_min(t) in the unit square, P(max<1/2) in
(0,1)x(0,2), E[max] in the unit square), so neither 1-(1-t)^2 nor E[max]=2/3 is ever shown; the boss 24B-A-Q1d
(min<L/3) and 24A-D-Q1b (both < 2/3); 24B-C-Q1d/e (their wording says "short" but defines the max).
Worked examples: F_max(t) = t^2 in the unit square (the lesson's rule, no quiz value plugged in), and Z = max(X,Y)
for X~U(0,1), Y~U(0,3): F piecewise (t^2/3, t/3), density (2t/3, 1/3), E[Z] = 14/9.
CDF pieces by exact polygons, density/mean by sympy, all cross-checked by Monte Carlo.
"""
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

U = ((0, 1), (0, 1))
t = sp.Symbol("t", positive=True)

# unit square: F_max(t) = t^2 (the square [0,t]^2), checked at a few t
for tv in (Fr(1, 5), Fr(3, 5), Fr(9, 10)):
    assert g.area(g.clip([(1, 0, tv, "<"), (0, 1, tv, "<")], *U)) == tv ** 2
assert sp.diff(t ** 2, t) == 2 * t

# rectangle (0,1) x (0,3), Z = max(X, Y)
R3 = ((0, 1), (0, 3))
OM3 = 3
F1, F2 = t ** 2 / 3, t / 3
for tv in (Fr(1, 2), Fr(9, 10)):
    assert g.area(g.clip([(1, 0, tv, "<"), (0, 1, tv, "<")], *R3)) / OM3 == F1.subs(t, tv)
for tv in (Fr(3, 2), Fr(5, 2)):
    assert g.area(g.clip([(1, 0, tv, "<"), (0, 1, tv, "<")], *R3)) / OM3 == F2.subs(t, tv)
assert F1.subs(t, 1) == F2.subs(t, 1) == sp.Rational(1, 3) and F2.subs(t, 3) == 1
f1, f2 = sp.diff(F1, t), sp.diff(F2, t)
assert f1 == 2 * t / 3 and f2 == sp.Rational(1, 3)
assert sp.integrate(f1, (t, 0, 1)) + sp.integrate(f2, (t, 1, 3)) == 1
EZ = sp.integrate(t * f1, (t, 0, 1)) + sp.integrate(t * f2, (t, 1, 3))
assert sp.integrate(t * f1, (t, 0, 1)) == sp.Rational(2, 9) and sp.integrate(t * f2, (t, 1, 3)) == sp.Rational(4, 3)
assert EZ == sp.Rational(14, 9)
_rng = np.random.default_rng(6)
_z = np.maximum(_rng.uniform(0, 1, 2_000_000), _rng.uniform(0, 3, 2_000_000))
assert abs(_z.mean() - 14 / 9) < 5 * _z.std() / np.sqrt(len(_z))
assert EZ > sp.Rational(3, 2)                                   # E[max] >= E[Y] = 3/2: a sanity check
g.mc(lambda a, b: np.maximum(a, b) < 2, *R3, F2.subs(t, 2))

# exam 25S-A-Q1b: x = X1 ~ U(0,1), y = X2 ~ U(0,2); P(min < 1/2)
Q = BANK["25S-A-Q1b"]
assert "\\frac58" in Q["solution"].replace(" ", "") and Q["contextId"] == "25S-A-c1"
R = ((0, 1), (0, 2))
CP = [(1, 0, Fr(1, 2), ">"), (0, 1, Fr(1, 2), ">")]            # the complement: both >= 1/2
SC = g.area(g.clip(CP, *R))
assert SC == Fr(1, 2) * Fr(3, 2) == Fr(3, 4) and 1 - SC / 2 == Fr(5, 8)
p1 = g.area(g.clip([(1, 0, Fr(1, 2), "<")], *R)) / 2
p2 = g.area(g.clip([(0, 1, Fr(1, 2), "<")], *R)) / 2
assert p1 == Fr(1, 2) and p2 == Fr(1, 4) and p1 + p2 - p1 * p2 == Fr(5, 8)   # inclusion-exclusion agrees
assert p1 + p2 == Fr(3, 4)                                       # the trap: the overlap counted twice
g.mc(lambda a, b: np.minimum(a, b) < .5, *R, Fr(5, 8))

# ---------------------------------------------------------------- figures
pa = g.Plane("pa", *U, maxw=420, maxh=420, xticks=[(.6, "t"), (1, "1")], yticks=[(.6, "t"), (1, "1")])
pa.region("sq", [(1, 0, Fr(3, 5), "<"), (0, 1, Fr(3, 5), "<")], "ev")
pa.seg("v", (.6, 0), (.6, .6))
pa.seg("h", (0, .6), (.6, .6))
pa.text("t", .3, .27, "t²")

pr = g.Plane("pr", *R3, maxw=300, maxh=480, xticks=[(1, "1")], yticks=[(1, "1"), (3, "3")])
pr.text("la1", .5, -.3, "t", cls="geo-lt")
pr.text("la2", -.17, .43, "t", cls="geo-lt")
pr.text("lb", -.17, 1.93, "t", cls="geo-lt")
pr.seg("lbs", (0, 2), (1, 2), cls="ln alt")
pr.poly("om", [(0, 0), (1, 0), (1, 3), (0, 3)], "om")
pr.region("a", [(1, 0, Fr(1, 2), "<"), (0, 1, Fr(1, 2), "<")], "ev")
pr.region("b", [(0, 1, 2, "<")], "warn")
pr.text("ta", .25, .12, "t²")
pr.text("tb", .5, 1.25, "1·t")

pf = g.Plane("pf", (0, 3), (0, 1), w=470, h=260, xlab="t", ylab="F(t)", frame=False,
             xticks=[(1, "1"), (3, "3")], yticks=[(Fr(1, 3), "1/3"), (1, "1")], view=((0, 3.3), (0, 1.12)))
pf.curve("c1", lambda s: s * s / 3, 0, 1, n=100, clip_box=False)
pf.curve("c2", lambda s: s / 3, 1, 3, n=50, clip_box=False)
pf.curve("c3", lambda s: 1, 3, 3.3, n=10, clip_box=False)
pf.seg("g1", (1, 0), (1, 1 / 3), dash=True, cls="ln alt")

px = g.Plane("px", *R, maxw=300, maxh=520, xlab='X<tspan dy="8" font-size="22">1</tspan>',
             ylab='X<tspan dy="8" font-size="22">2</tspan>', xticks=[(.5, "1/2"), (1, "1")],
             yticks=[(.5, "1/2"), (2, "2")])
px.poly("om", [(0, 0), (1, 0), (1, 2), (0, 2)], "om")
px.region("e1", [(1, 0, Fr(1, 2), "<")], "ev")
px.region("e2", [(0, 1, Fr(1, 2), "<"), (1, 0, Fr(1, 2), ">")], "ev")
px.region("cp", CP, "comp")
px.region("ov", [(1, 0, Fr(1, 2), "<"), (0, 1, Fr(1, 2), "<")], "warn")
px.text("tc", .75, 1.2, "3/4")

FIG = st.raster("x-fig", "images/exams/25S-A-Q1-grasshopper.png", 560, (478, 268))
STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>חגב קופץ פעמיים: '
        '<span class="nobr">$X_1\\sim U_c(0,1)$</span>, <span class="nobr">$X_2\\sim U_c(0,2)$</span>, בלתי תלויים. '
        'מה ההסתברות שלפחות אחת הקפיצות קצרה מחצי?</div>')

title = Scene("title", "", [
    P("בסרטון הזה נגדיר משתנה חדש: המקסימום, או המינימום, של שני משתנים אחידים."),
    P("נמצא את ההתפלגות המצטברת שלו בשיטת השטח, ומשם את הצפיפות והתוחלת.", hold=0.4),
], stage='<div class="kicker">G06 · הסתברות גיאומטרית</div><h1>מקסימום ומינימום: התפלגות מצטברת</h1>'
         '<p>לחשב את ההתפלגות המצטברת של $\\max(X,Y)$ ושל $\\min(X,Y)$, ואת הצפיפות והתוחלת שלהן.</p>',
   layout="title")

idea = Scene("idea", "המקסימום", [
    P("נגדיר את $Z$ כמקסימום של $X$ ו-$Y$, שניהם אחידים בין אפס לאחת.", say="נגדיר את זֶד כמקסימום של אִקְס ווַואי, שניהם אחידים בין אפס לאחת.",
      do=show("a-1")),
    P("ההתפלגות המצטברת היא $F$ של $t$: ההסתברות ש-$Z$ קטן או שווה ל-$t$.",
      say="ההתפלגות המצטברת היא אֶף של טִי: ההסתברות שזֶד קטן או שווה לטִי.", do=show("a-2")),
    P("מקבעים $t$, ומציירים את האזור שבו המקסימום קטן מ-$t$.", say="מקבעים טִי, ומציירים את האזור שבו המקסימום קטן מטִי."),
    P("המקסימום קטן מ-$t$ אם ורק אם **שניהם** קטנים מ-$t$. זה ריבוע בצלע $t$.",
      say="המקסימום קטן מטִי אם ורק אם שניהם קטנים מטִי. זה ריבוע בצלע טִי.", do=show("pa-sq", "pa-v", "pa-h", "a-3")),
    P("השטח שלו $t$ בריבוע, ולכן $F$ של $t$ שווה $t$ בריבוע, לכל $t$ בין אפס לאחת.",
      say="השטח שלו טִי בריבוע, ולכן אֶף של טִי שווה טִי בריבוע, לכל טִי בין אפס לאחת.", do=show("pa-t", "a-4")),
    P("הצפיפות היא הנגזרת של ההתפלגות המצטברת: שתיים $t$.", say="הצפיפות היא הנגזרת של ההתפלגות המצטברת: שתיים טִי.",
      do=show("a-5")),
    P("ובמינימום, הכיוון הפוך: המינימום **גדול** מ-$t$ כששניהם גדולים מ-$t$.",
      say="ובמינימום, הכיוון הפוך: המינימום גדול מטִי כששניהם גדולים מטִי.", do=show("a-6")),
    P("זה ריבוע בפינה הנגדית, ולכן למינימום עוברים דרך המשלים. נראה את זה בשאלת המבחן.", hold=0.4),
], stage=f'<div class="geo-stack">{pa.svg()}</div>',
   panel=st.card("a-1", "plain", "$Z=\\max(X,Y)$, $\\;X,Y\\sim U_c(0,1)$")
         + st.card("a-2", "plain", "$F_Z(t)=P(Z\\le t)$")
         + st.card("a-3", "rule", "🔑 $\\max(X,Y)\\le t\\iff X\\le t$ וגם $Y\\le t$")
         + st.card("a-4", "rule", "🔑 $F_{\\max}(t)=t^2$, $\\;0\\le t\\le1$")
         + st.card("a-5", "plain", "$f(t)=F'(t)=2t$")
         + st.card("a-6", "trap", "⚠️ $\\min(X,Y)>t\\iff X>t$ וגם $Y>t$"))

rect = Scene("rect", "במלבן", [
    P("ועכשיו במלבן: $X$ אחיד בין אפס לאחת, $Y$ אחיד בין אפס לשלוש, ו-$Z$ המקסימום.",
      say="ועכשיו במלבן: אִקְס אחיד בין אפס לאחת, וַואי אחיד בין אפס לשלוש, וזֶד המקסימום.", do=show("pr-om", "b-1")),
    P("השטח של אומגה שלוש. ושוב, המקסימום קטן מ-$t$ כששניהם קטנים מ-$t$.",
      say="השטח של אומגה שלוש. ושוב, המקסימום קטן מטִי כששניהם קטנים מטִי."),
    P("כש-$t$ בין אפס לאחת: ריבוע בצלע $t$, שטח $t$ בריבוע. מחלקים בשלוש.",
      say="כשטִי בין אפס לאחת: ריבוע בצלע טִי, שטח טִי בריבוע. מחלקים בשלוש.",
      do=show("pr-a", "pr-ta", "pr-la1", "pr-la2", "b-2")),
    P("אבל כש-$t$ גדול מאחת, התנאי על $X$ מתקיים תמיד. נשאר מלבן ברוחב אחת ובגובה $t$.",
      say="אבל כשטִי גדול מאחת, התנאי על אִקְס מתקיים תמיד. נשאר מלבן ברוחב אחת ובגובה טִי.",
      do=hide("pr-a", "pr-ta", "pr-la1", "pr-la2") + show("pr-b", "pr-tb", "pr-lb", "pr-lbs", "b-3")),
    P("השטח שלו אחת כפול $t$. מחלקים בשלוש: $t$ חלקי שלוש.", say="השטח שלו אחת כפול טִי. מחלקים בשלוש: טִי חלקי שלוש."),
    P("בדיקה: בנקודה אחת שתי הנוסחאות נותנות שליש, ובשלוש מקבלים אחת. ההתפלגות רציפה.", do=show("b-4", "pf-c1", "pf-c2", "pf-c3", "pf-g1")),
    P("גוזרים: הצפיפות היא שני שלישים $t$ עד אחת, ושליש מאחת עד שלוש.",
      say="גוזרים: הצפיפות היא שני שלישים טִי עד אחת, ושליש מאחת עד שלוש.", do=show("b-5")),
    P("התוחלת היא האינטגרל של $t$ כפול הצפיפות, בכל קטע בנפרד.", say="התוחלת היא האינטגרל של טִי כפול הצפיפות, בכל קטע בנפרד."),
    P("בקטע הראשון יוצא שתי תשיעיות, ובשני ארבעה שלישים. ביחד: ארבע עשרה תשיעיות.", do=show("b-6"), hold=0.3),
    P("וזה הגיוני: המקסימום תמיד לפחות $Y$, והתוחלת של $Y$ היא אחת וחצי.",
      say="וזה הגיוני: המקסימום תמיד לפחות וַואי, והתוחלת של וַואי היא אחת וחצי.", hold=0.4),
], stage=f'<div class="geo-row">{pr.svg()}{pf.svg()}</div>',
   panel=st.card("b-1", "plain", "$X\\sim U_c(0,1)$, $\\;Y\\sim U_c(0,3)$, $\\;|\\Omega|=3$")
         + st.card("b-2", "plain", "$0\\le t\\le1$: $\\;F(t)=\\frac{t^2}{3}$")
         + st.card("b-3", "plain", "$1\\le t\\le3$: $\\;F(t)=\\frac{1\\cdot t}{3}=\\frac t3$")
         + st.card("b-4", "ex", "$F(1)=\\frac13$ משני הצדדים, $\\;F(3)=1$")
         + st.card("b-5", "plain", "$f(t)=\\frac{2t}{3}$ על $(0,1)$, $\\;\\frac13$ על $(1,3)$")
         + st.card("b-6", "rule", "🔑 $E[Z]=\\int_0^1\\frac{2t^2}{3}dt+\\int_1^3\\frac t3dt=\\frac29+\\frac43=\\frac{14}9$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: חגב קופץ פעמיים. הקפיצה הראשונה אחידה בין אפס לאחת, והשנייה בין אפס לשתיים."),
    P("מה ההסתברות שלפחות אחת הקפיצות קצרה מחצי?", hold=0.2),
    P("לפחות אחת קצרה מחצי, פירושו שהמינימום של שתיהן קטן מחצי. זה **או**: איחוד.",
      do=hide("x-fig") + show("x-pl", "px-om", "x-1")),
    P("באיור זו צורה של זווית: רצועה אנכית ורצועה אופקית.", do=show("px-e1", "px-e2")),
    P("הכי קל דרך המשלים: שתי הקפיצות לפחות חצי. זה מלבן אחד.", do=show("px-cp")),
    P("הרוחב שלו חצי, והגובה שלו אחת וחצי. השטח: שלושה רבעים.", do=show("px-tc", "x-2")),
    P("השטח של אומגה שתיים, ולכן המשלים הוא שלוש שמיניות, וההסתברות: חמש שמיניות.", do=show("x-3"), hold=0.3),
    P("מלכודת ראשונה: ההסתברות שהשנייה קצרה מחצי היא רבע, לא חצי. הטווח שלה עד שתיים.", do=show("x-t1")),
    P("ומלכודת שנייה: לחבר חצי ועוד רבע, ולקבל שלושה רבעים.", do=show("x-t2")),
    P("אבל הריבוע הקטן בפינה שייך לשתי הרצועות, ולכן בסכום הזה הוא נספר פעמיים. הסכום גדול מדי.",
      do=show("px-ov")),
    P("בגלל זה עדיף כאן המשלים: מלבן אחד, בלי ספירה כפולה, ובלי לחשוב על החפיפה בכלל.", hold=0.5),
], stage=(f'<div class="geo-swap" style="--swap-h:640px"><div id="x-fig">{FIG}</div>'
          f'<div id="x-pl" class="h">{px.svg()}</div></div>'),
   panel=STEM
         + st.card("x-1", "plain", "$P\\left(\\min(X_1,X_2)<\\frac12\\right)$, $\\;|\\Omega|=2$")
         + st.card("x-2", "plain", "משלים: $\\frac12\\cdot\\frac32=\\frac34$")
         + st.card("x-3", "rule", "🔑 $P=1-\\frac{3/4}{2}=\\frac58$")
         + st.card("x-t1", "trap", "⚠️ $P\\left(X_2<\\frac12\\right)=\\frac14$, לא $\\frac12$")
         + st.card("x-t2", "trap", "⚠️ $\\frac12+\\frac14=\\frac34$: הפינה נספרה פעמיים"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כדי למצוא התפלגות מצטברת, מקבעים $t$ ומחשבים את השטח של האירוע.",
      say="לסיכום: כדי למצוא התפלגות מצטברת, מקבעים טִי ומחשבים את השטח של האירוע.", do=show("r-1")),
    P("המקסימום קטן מ-$t$ כששניהם קטנים. המינימום גדול מ-$t$ כששניהם גדולים.",
      say="המקסימום קטן מטִי כששניהם קטנים. המינימום גדול מטִי כששניהם גדולים.", do=show("r-2", "r-2b")),
    P("במלבן, הנוסחה משתנה כש-$t$ עובר את הטווח הקצר. בודקים רציפות בנקודת המעבר.",
      say="במלבן, הנוסחה משתנה כשטִי עובר את הטווח הקצר. בודקים רציפות בנקודת המעבר.", do=show("r-3")),
    P("ומשם: גוזרים לצפיפות, ומחשבים תוחלת בכל קטע. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="geo-stack"><div class="geo-big">$f=F\\,\'\\qquad E[Z]=\\int t\\,f(t)\\,dt$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $F_Z(t)$: שטח האירוע $\\{Z\\le t\\}$ חלקי $|\\Omega|$")
         + st.card("r-2", "rule", "🔑 $\\max(X,Y)\\le t$: שניהם $\\le t$")
         + st.card("r-2b", "rule", "🔑 $\\min(X,Y)>t$: שניהם $>t$")
         + st.card("r-3", "trap", "⚠️ במלבן: נוסחה לכל קטע של $t$")
         + st.card("r-4", "rule", "🔑 צפיפות: נגזרת. תוחלת: אינטגרל לכל קטע"))

VIDEO = Video("G06", "geo", "מקסימום ומינימום: התפלגות מצטברת", [title, idea, rect, exam, recap],
              bank={"25S-A-Q1b": None})
