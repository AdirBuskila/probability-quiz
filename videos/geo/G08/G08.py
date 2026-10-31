# -*- coding: utf-8 -*-
"""G08 · סיפורים: פגישה, מקל, מלבן ונקודה בריבוע — video script (build: tools/video/vid.py G08).

Source: courses/geo/C08.js (lesson + goal). Exam anchor: 25S-B-Q1b (two clock hands at angles a1,a2~U(0,pi);
P(the angle between them, |a1-a2|, is acute) = 3/4), an open question (bank key None) that no guided quiz uses.
Avoided on purpose: the C08 quiz stories (meeting within a quarter hour, the broken stick, perimeter < 3 in
(0,1)x(0,2), X/2<Y<2X, near the boundary), 25S-B-Q1a (a2>2a1, a twin of C02-Q5) and 25S-C-Q1a/b (the isosceles
triangle: its event region lies where the triangle cannot exist, see the report). The boss 25A-A-Q1b is not touched.
Worked examples (original): a meeting with a 10-minute wait, |X-Y| < 1/6 hour -> 11/36 (and the same in minutes);
a bus within 15 minutes and you within 10 -> P(you arrive first) = 2/3.
Areas: exact polygons (the angle plane is drawn in units of pi), sympy with pi, and Monte Carlo.
"""
from fractions import Fraction as Fr
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

U = ((0, 1), (0, 1))
# meeting: X, Y ~ U(0,1) hours, |X - Y| < 1/6
c = Fr(1, 6)
BAND = [(1, -1, c, "<"), (1, -1, -c, ">")]
A1 = g.area(g.clip(BAND, *U))
assert A1 == 1 - (1 - c) ** 2 == Fr(11, 36)
assert Fr(3600 - 2 * 1250, 3600) == A1                        # the same in minutes: two triangles of 50*50/2
assert g.area(g.clip([(1, -1, c, ">")], *U)) == Fr(25, 72)    # each corner triangle
g.mc(lambda a, b: abs(a - b) < 1 / 6, *U, A1)

# bus: you X ~ U(0,10), bus Y ~ U(0,15) minutes; you are first: X < Y
RB = ((0, 10), (0, 15))
OMB = 150
CB = g.area(g.clip([(1, -1, 0, ">")], *RB))                     # the bus first: triangle under y = x
assert CB == 50 and 1 - Fr(CB, OMB) == Fr(2, 3)
g.mc(lambda a, b: a < b, *RB, Fr(2, 3))

# exam 25S-B-Q1b: a1, a2 ~ U(0, pi); acute: |a1 - a2| < pi/2
Q = BANK["25S-B-Q1b"]
assert "\\frac34" in Q["solution"].replace(" ", "") and Q["contextId"] == "25S-B-c1"
pi = sp.pi
SB = pi ** 2 - 2 * sp.Rational(1, 2) * (pi / 2) ** 2
assert sp.simplify(SB / pi ** 2 - sp.Rational(3, 4)) == 0
assert g.area(g.clip([(1, -1, Fr(1, 2), "<"), (1, -1, -Fr(1, 2), ">")], *U)) == Fr(3, 4)   # the same in units of pi
g.mc(lambda a, b: abs(a - b) < math.pi / 2, (0, math.pi), (0, math.pi), 0.75)
assert sp.simplify(SB / pi - 3 * pi / 4) == 0                   # the trap: dividing by pi gives 3pi/4 > 1

# ---------------------------------------------------------------- figures
pm = g.Plane("pm", *U, maxw=420, maxh=420, xticks=[(Fr(1, 6), "1/6"), (1, "1")], yticks=[(Fr(1, 6), "1/6"), (1, "1")])
pm.region("ev", BAND, "ev")
pm.region("t1", [(1, -1, c, ">")], "comp")
pm.region("t2", [(1, -1, -c, "<")], "comp")
pm.line("l1", -1, 1, c)
pm.line("l2", -1, 1, -c)
pm.text("tt1", .76, .24, "25/72")
pm.text("tt2", .24, .76, "25/72")
pm.text("t", .62, .55, "11/36")

pb = g.Plane("pb", *RB, maxw=300, maxh=450, xticks=[(10, "10")], yticks=[(10, "10"), (15, "15")])
pb.poly("om", [(0, 0), (10, 0), (10, 15), (0, 15)], "om")
pb.line("d", -1, 1, 0, label="y = x", at=(5, 5), dx=-10, dy=-14, anchor="end")
pb.region("ev", [(1, -1, 0, "<")], "ev")
pb.region("cp", [(1, -1, 0, ">")], "comp")
pb.text("tc", 7, 2.4, "50")
pb.text("t", 4, 10, "100")

pa = g.Plane("pa", *U, maxw=440, maxh=440, xlab='α<tspan dy="8" font-size="22">1</tspan>',
             ylab='α<tspan dy="8" font-size="22">2</tspan>', xticks=[(.5, "π/2"), (1, "π")], yticks=[(.5, "π/2"), (1, "π")])
pa.region("ev", [(1, -1, Fr(1, 2), "<"), (1, -1, -Fr(1, 2), ">")], "ev")
pa.region("t1", [(1, -1, Fr(1, 2), ">")], "comp")
pa.region("t2", [(1, -1, -Fr(1, 2), "<")], "comp")
pa.line("l1", -1, 1, .5)
pa.line("l2", -1, 1, -.5)
pa.text("tt1", .82, .17, "π²/8")
pa.text("tt2", .18, .82, "π²/8")
pa.text("t", .5, .45, "3π²/4")

FIG = st.raster("x-fig", "images/exams/25S-B-Q1-clock.png", 560, (580, 244))
STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>זוויות שני המחוגים '
        '<span class="nobr">$\\alpha_1,\\alpha_2\\sim U_c(0,\\pi)$</span> בלתי תלויות, והזווית ביניהם '
        '<span class="nobr">$\\beta=|\\alpha_1-\\alpha_2|$</span>. מה ההסתברות ש-$\\beta$ חדה?</div>')

title = Scene("title", "", [
    P("בסרטון הזה נפתור שאלות מילוליות: פגישות, אוטובוסים ומחוגים."),
    P("הקושי הוא התרגום. אחרי שמתרגמים, זו אותה שיטת השטח.", hold=0.4),
], stage='<div class="kicker">G08 · הסתברות גיאומטרית</div><h1>סיפורים: פגישה, אוטובוס ומחוגים</h1>'
         '<p>לתרגם סיפור מילולי לשני משתנים אחידים ולאי-שוויונות, ואז לפתור בשיטת השטח.</p>', layout="title")

idea = Scene("idea", "התרגום", [
    P("שלושה צעדים. ראשון: מגדירים מי $X$ ומי $Y$, ואת הטווח של כל אחד.", say="שלושה צעדים. ראשון: מגדירים מי אִקְס ומי וַואי, ואת הטווח של כל אחד.",
      do=show("i-1")),
    P("ומיד רושמים את השטח של אומגה.", hold=0.1),
    P("שני: מתרגמים כל תנאי בסיפור לאי-שוויון בין $x$ ל-$y$.", say="שני: מתרגמים כל תנאי בסיפור לאי-שוויון בין אִקְס לוַואי.",
      do=show("i-2")),
    P("למשל, מחכים זה לזה עד זמן מסוים: ההפרש בערך מוחלט קטן ממנו. ומגיע ראשון: אי-שוויון פשוט.", do=show("i-2a", "i-2b")),
    P("שלישי: מציירים, מחשבים שטח, ומחלקים בשטח של אומגה.", do=show("i-3"), hold=0.4),
], stage='<div class="geo-stack"><div class="geo-steps">'
         '<div id="i-2a" class="h">$|X-Y|&lt;c$</div><div id="i-2b" class="h">$X&lt;Y$</div></div></div>',
   panel=st.card("i-1", "rule", "🔑 א. $X$, $Y$, הטווחים, $|\\Omega|$")
         + st.card("i-2", "rule", "🔑 ב. כל תנאי: אי-שוויון")
         + st.card("i-3", "rule", "🔑 ג. ציור, שטח, חלוקה"))

meet = Scene("meet", "פגישה", [
    P("שני חברים קבעו להיפגש בין שבע לשמונה. כל אחד מגיע בזמן אחיד בשעה הזו, בלי תלות בשני.", do=show("a-q")),
    P("כל אחד מחכה לשני עשר דקות, ואז הולך. מה ההסתברות שהם נפגשים?"),
    P("מודדים בשעות: $X$ ו-$Y$ אחידים בין אפס לאחת. השטח של אומגה אחת.",
      say="מודדים בשעות: אִקְס ווַואי אחידים בין אפס לאחת. השטח של אומגה אחת.", do=show("a-1")),
    P("עשר דקות הן שישית שעה. הם נפגשים אם ההפרש בין זמני ההגעה קטן משישית.", do=show("a-2", "pm-l1", "pm-l2")),
    P("זו רצועה סביב האלכסון. בחוץ, שני משולשים עם ניצבים של חמש שישיות.",
      do=show("pm-ev", "pm-t1", "pm-t2", "pm-tt1", "pm-tt2")),
    P("כל משולש: חצי כפול חמש שישיות כפול חמש שישיות, כלומר עשרים וחמש חלקי שבעים ושתיים."),
    P("מורידים את שניהם מהריבוע, ונשאר אחת עשרה חלקי שלושים ושש.", do=show("pm-t", "a-3")),
    P("זה בערך שלושים אחוז.", hold=0.2),
    P("ובדקות? הריבוע בצלע שישים, המשולשים עם ניצבים חמישים, והתשובה זהה. היחידות מצטמצמות.", do=show("a-4"), hold=0.4),
], stage=f'<div class="geo-stack">{pm.svg()}</div>',
   panel=st.card("a-q", "ex", "מחכים עשר דקות, בתוך שעה אחת")
         + st.card("a-1", "plain", "$X,Y\\sim U_c(0,1)$ בשעות, $\\;|\\Omega|=1$")
         + st.card("a-2", "plain", "נפגשים: $|X-Y|<\\frac16$")
         + st.card("a-3", "rule", "🔑 $P=1-2\\cdot\\frac{25}{72}=\\frac{11}{36}\\approx0.31$")
         + st.card("a-4", "ex", "בדקות: $\\frac{3600-2\\cdot1250}{3600}=\\frac{11}{36}$"))

bus = Scene("bus", "אוטובוס", [
    P("ועוד סיפור: אוטובוס מגיע לתחנה בזמן אחיד ברבע השעה הקרובה.", do=show("b-q")),
    P("אתם מגיעים בזמן אחיד בעשר הדקות הקרובות, בלי תלות. מה ההסתברות שתגיעו לפני האוטובוס?"),
    P("$X$ הוא הזמן שלכם, בין אפס לעשר. $Y$ הוא הזמן של האוטובוס, בין אפס לחמש עשרה. השטח של אומגה מאה וחמישים.",
      say="אִקְס הוא הזמן שלכם, בין אפס לעשר. וַואי הוא הזמן של האוטובוס, בין אפס לחמש עשרה. השטח של אומגה מאה וחמישים.",
      do=show("pb-om", "b-1")),
    P("להגיע לפני האוטובוס: $X$ קטן מ-$Y$. כלומר מעל האלכסון.", say="להגיע לפני האוטובוס: אִקְס קטן מוַואי. כלומר מעל האלכסון.",
      do=show("pb-d", "pb-ev")),
    P("המשלים הוא המשולש מתחת לאלכסון, עם ניצבים עשר ועשר. השטח: חמישים.", do=show("pb-cp", "pb-tc")),
    P("נשאר מאה, מתוך מאה וחמישים: ההסתברות היא שני שלישים.", do=show("pb-t", "b-2"), hold=0.4),
], stage=f'<div class="geo-stack">{pb.svg()}</div>',
   panel=st.card("b-q", "ex", "אוטובוס: $15$ דקות. אתם: $10$ דקות")
         + st.card("b-1", "plain", "$X\\sim U_c(0,10)$, $\\;Y\\sim U_c(0,15)$, $\\;|\\Omega|=150$")
         + st.card("b-2", "rule", "🔑 $P(X<Y)=\\frac{150-50}{150}=\\frac23$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: שני מחוגים על חצי עיגול. הזווית של כל אחד אחידה בין אפס לפאי, והן בלתי תלויות."),
    P("הזווית ביניהם, בטא, היא ההפרש בערך מוחלט. מה ההסתברות שבטא היא זווית חדה?", hold=0.2),
    P("צעד ראשון: המשתנים הם שתי הזוויות. מרחב המדגם הוא ריבוע בצלע פאי, והשטח שלו פאי בריבוע.",
      do=hide("x-fig") + show("x-pl", "x-1")),
    P("צעד שני: זווית חדה היא זווית קטנה מתשעים מעלות, כלומר מחצי פאי.", do=show("x-2")),
    P("אז התנאי הוא: ההפרש בערך מוחלט קטן מחצי פאי. זו רצועה סביב האלכסון.", do=show("pa-l1", "pa-l2", "pa-ev")),
    P("צעד שלישי: בחוץ שני משולשים, עם ניצבים של חצי פאי. כל אחד: פאי בריבוע חלקי שמונה.",
      do=show("pa-t1", "pa-t2", "pa-tt1", "pa-tt2")),
    P("הרצועה: פאי בריבוע, פחות רבע פאי בריבוע. שלושה רבעים פאי בריבוע.", do=show("pa-t", "x-3")),
    P("ומחלקים בפאי בריבוע: ההסתברות היא שלושה רבעים. הפאי מצטמצם.", do=show("x-4"), hold=0.3),
    P("המלכודת: לחלק בפאי ולא בפאי בריבוע. יוצא מספר גדול מאחת, וזה סימן לטעות.", do=show("x-t"), hold=0.5),
], stage=(f'<div class="geo-swap" style="--swap-h:600px"><div id="x-fig">{FIG}</div>'
          f'<div id="x-pl" class="h">{pa.svg()}</div></div>'),
   panel=STEM
         + st.card("x-1", "plain", "$\\Omega=(0,\\pi)^2$, $\\;|\\Omega|=\\pi^2$")
         + st.card("x-2", "plain", "חדה: $|\\alpha_1-\\alpha_2|<\\frac{\\pi}{2}$")
         + st.card("x-3", "plain", "$\\pi^2-2\\cdot\\frac12\\left(\\frac{\\pi}{2}\\right)^2=\\frac34\\pi^2$")
         + st.card("x-4", "rule", "🔑 $P=\\frac{3\\pi^2/4}{\\pi^2}=\\frac34$")
         + st.card("x-t", "trap", "⚠️ חלוקה ב-$\\pi$: $\\frac{3\\pi}4>1$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בשאלה מילולית מתחילים מההגדרות, ולא מהחישוב.", do=show("r-1")),
    P("מי המשתנים, מה הטווחים, ומה השטח של אומגה.", do=show("r-2")),
    P("אחר כך כל משפט בסיפור הופך לאי-שוויון, וממשיכים בשיטת השטח.", do=show("r-3")),
    P("ויחידות, דקות או שעות או רדיאנים, מצטמצמות בחלוקה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="geo-stack"><div class="geo-big">$P=\\dfrac{S(A)}{|\\Omega|}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 קודם הגדרות, אחר כך חישוב")
         + st.card("r-2", "rule", "🔑 $X$, $Y$, טווחים, $|\\Omega|$")
         + st.card("r-3", "rule", "🔑 כל משפט: אי-שוויון")
         + st.card("r-4", "trap", "⚠️ היחידות מצטמצמות, אבל רק אם מחלקים ב-$|\\Omega|$ הנכון"))

VIDEO = Video("G08", "geo", "סיפורים: פגישה, אוטובוס ומחוגים", [title, idea, meet, bus, exam, recap],
              bank={"25S-B-Q1b": None})
