# -*- coding: utf-8 -*-
"""G02 · חצאי מישור: קו אחד וצד אחד — video script (build: tools/video/vid.py G02).

Source: courses/geo/C02.js (lesson + goal). Exam anchor: 24B-A-Q1c (two matches X,Y~U(0,L), P(X+Y<=4L/3) = 7/9),
an open question (bank key None) that no guided quiz uses.
Avoided on purpose: the C02 quiz cases (Y>X, X+Y<2/3, X+Y<5/4, Y>X in (0,1)x(0,2), Y>2X) and their bank twins
24A-D-Q1a (X1+X2<=2/3), 24A-B-Q1c (S1<S2 = Y>X), 25S-B-Q1a (a2>2a1); the lesson's X+Y<3/2 (24B-C-Q1c, 24A-B-Q1b).
Worked examples: P(2X+Y<1) = 1/4 (corner triangle), P(X+2Y<2) = 3/4 (the line leaves through a side: complement).
Every area is an exact polygon (w_geo.clip), cross-checked by the closed form and by Monte Carlo.
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

U = ((0, 1), (0, 1))
# example 1: 2X+Y<1
E1 = [(2, 1, 1, "<")]
A1 = g.area(g.clip(E1, *U))
assert A1 == Fr(1, 2) * Fr(1, 2) * 1 == Fr(1, 4)          # legs 1/2 (on the x axis) and 1 (on the y axis)
assert 2 * 0 + 0 < 1                                      # the test point (0,0) is on the event side
g.mc(lambda x, y: 2 * x + y < 1, *U, A1)

# example 2: X+2Y<2 ; the line y = 1 - x/2 runs from (0,1) to (1,1/2)
E2 = [(1, 2, 2, "<")]
A2 = g.area(g.clip(E2, *U))
C2 = g.area(g.clip([(1, 2, 2, ">")], *U))
assert C2 == Fr(1, 2) * 1 * Fr(1, 2) == Fr(1, 4) and A2 == 1 - C2 == Fr(3, 4)
assert A2 == (1 + Fr(1, 2)) / 2 * 1                       # the same area as a trapezoid
g.mc(lambda x, y: x + 2 * y < 2, *U, A2)

# exam 24B-A-Q1c in units of L: X+Y <= 4/3 in the unit square
Q = BANK["24B-A-Q1c"]
assert "4L/3" in Q["question"] and "\\frac79" in Q["solution"].replace(" ", "")
EX = [(1, 1, Fr(4, 3), "<")]
AX = g.area(g.clip(EX, *U))
CX = g.area(g.clip([(1, 1, Fr(4, 3), ">")], *U))
assert CX == Fr(1, 2) * Fr(2, 3) ** 2 == Fr(2, 9) and AX == Fr(7, 9)
assert Fr(1, 2) * Fr(4, 3) ** 2 == Fr(8, 9)               # the trap: the corner triangle at the origin does not fit
g.mc(lambda x, y: x + y <= 4 / 3, *U, AX)

# ---------------------------------------------------------------- figures
TK = [(Fr(1, 2), "1/2"), (1, "1")]
pa = g.Plane("pa", *U, maxw=430, maxh=430, xticks=TK, yticks=[(1, "1")])
pa.line("l", 2, 1, 1, label="2x + y = 1", at=(.5, 0), dx=14, dy=-60)
pa.pt("tp", 0, 0, "(0,0)", dx=14, dy=-16)
pa.region("ev", E1, "ev")
pa.text("t", .17, .27, "1/4")

pb = g.Plane("pb", *U, maxw=430, maxh=430, xticks=[(1, "1")], yticks=TK + [])
pb.line("l", 1, 2, 2, label="x + 2y = 2", at=(.35, .82), dx=0, dy=-16)
pb.region("ev", E2, "ev")
pb.region("cp", [(1, 2, 2, ">")], "comp")
pb.text("tc", .78, .86, "1/4")
pb.text("t", .5, .38, "3/4")

px = g.Plane("px", *U, maxw=500, maxh=500, xlab="X", ylab="Y",
             xticks=[(Fr(1, 3), "L/3"), (1, "L"), (Fr(4, 3), "4L/3")],
             yticks=[(Fr(1, 3), "L/3"), (1, "L"), (Fr(4, 3), "4L/3")], view=((0, 1.4), (0, 1.4)))
px.line("l", 1, 1, 4 / 3)
px.region("ev", EX, "ev")
px.region("cp", [(1, 1, Fr(4, 3), ">")], "comp")
px.seg("big", (0, 4 / 3), (4 / 3, 0), cls="ln alt", dash=True)
px.text("tc", .79, .8, "2/9")
px.text("t", .4, .4, "7/9")

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>שני גפרורים באורכים בלתי תלויים '
        '<span class="nobr">$X,Y\\sim U_c(0,L)$</span>. חשבו את $P\\left(X+Y\\le \\frac43L\\right)$.</div>')

title = Scene("title", "", [
    P("בסרטון הזה נלמד לתרגם אי-שוויון בין שני משתנים לאזור במלבן."),
    P("קו אחד, צד אחד, ושטח של משולש. ולפעמים, שטח של מה שנשאר בחוץ."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">G02 · הסתברות גיאומטרית</div><h1>חצאי מישור: קו אחד וצד אחד</h1>'
         '<p>לתרגם אי-שוויון בין $X$ ל-$Y$ לצד של קו, לבחור את הצד הנכון, ולחשב את שטח המשולש או המשלים.</p>',
   layout="title")

iA = g.Plane("iA", *U, maxw=260, maxh=260, xticks=[(Fr(2, 5), "c")], yticks=[(1, "1")])
iA.line("l", 1, 0, Fr(2, 5), shown=True)
iA.region("r", [(1, 0, Fr(2, 5), "<")], "ev", shown=True)
iB = g.Plane("iB", *U, maxw=260, maxh=260, xticks=[(1, "1")], yticks=[(1, "1")])
iB.line("l", -1, 1, 0, shown=True)
iB.region("r", [(-1, 1, 0, ">")], "ev", shown=True)
iC = g.Plane("iC", *U, maxw=260, maxh=260, xticks=[(Fr(7, 10), "c")], yticks=[(Fr(7, 10), "c")])
iC.line("l", 1, 1, Fr(7, 10), shown=True)
iC.region("r", [(1, 1, Fr(7, 10), "<")], "ev", shown=True)

idea = Scene("idea", "הרעיון", [
    P("אירוע כמו $X+Y<c$ הוא אי-שוויון בין $x$ ל-$y$.", say="אירוע כמו אִקְס ועוד וַואי קטן מסִי הוא אי-שוויון בין אִקְס לוַואי."),
    P("כל אי-שוויון כזה מחלק את המישור לשני צדדים של קו, והאירוע הוא אחד הצדדים.", hold=0.2),
    P("$X$ קטן מ-$c$: קו אנכי, והאירוע הוא הרצועה משמאל לו.", say="אִקְס קטן מסִי: קו אנכי, והאירוע הוא הרצועה משמאל לו.",
      do=show("i-a")),
    P("$Y$ גדול מ-$X$: האלכסון, והאירוע הוא מה שמעליו.", say="וַואי גדול מאִקְס: האלכסון, והאירוע הוא מה שמעליו.",
      do=show("i-b")),
    P("$X+Y$ קטן מ-$c$: קו יורד, והאירוע הוא הפינה של הראשית.",
      say="אִקְס ועוד וַואי קטן מסִי: קו יורד, והאירוע הוא הפינה של הראשית.", do=show("i-c"), hold=0.4),
    P("ואיך יודעים איזה צד? ואיך מחשבים את השטח? זה בדיוק מה שנעשה עכשיו."),
], stage=(f'<div class="geo-row"><div id="i-a" class="h">{iA.svg()}</div><div id="i-b" class="h">{iB.svg()}</div>'
          f'<div id="i-c" class="h">{iC.svg()}</div></div>'),
   layout="full")

ex1 = Scene("ex1", "ארבעה צעדים", [
    P("ניקח את ריבוע היחידה, ונשאל: מה ההסתברות ש-$2X+Y$ קטן מאחת?",
      say="ניקח את ריבוע היחידה, ונשאל: מה ההסתברות ששתיים אִקְס ועוד וַואי קטן מאחת?", do=show("a-q")),
    P("צעד ראשון: מחליפים את סימן האי-שוויון בשוויון, ומציירים את הקו.", do=show("a-1")),
    P("שתי נקודות מספיקות: כש-$x$ אפס, $y$ אחת. וכש-$y$ אפס, $x$ חצי.",
      say="שתי נקודות מספיקות: כשאִקְס אפס, וַואי אחת. וכשוַואי אפס, אִקְס חצי.", do=show("pa-l")),
    P("צעד שני: נקודת מבחן. הראשית, אפס ואפס, נותנת אפס, שבאמת קטן מאחת.", do=show("a-2", "pa-tp")),
    P("לכן האירוע הוא הצד של הקו שבו נמצאת הראשית.", do=show("pa-ev")),
    P("צעד שלישי: השטח. זה משולש ישר זווית עם ניצבים חצי ואחת. השטח: רבע.", do=show("a-3", "pa-t")),
    P("צעד רביעי: מחלקים בשטח של אומגה, שהוא אחת. ההסתברות היא רבע.", do=show("a-4"), hold=0.4),
], stage=f'<div class="geo-stack">{pa.svg()}</div>',
   panel=st.card("a-q", "ex", "$P(2X+Y<1)=\\,?\\quad X,Y\\sim U_c(0,1)$")
         + st.card("a-1", "plain", "א. הקו: $2x+y=1$, דרך $(0,1)$ ו-$\\left(\\frac12,0\\right)$")
         + st.card("a-2", "plain", "ב. נקודת מבחן: $2\\cdot0+0=0<1$ ✓")
         + st.card("a-3", "plain", "ג. השטח: $\\frac12\\cdot\\frac12\\cdot1=\\frac14$")
         + st.card("a-4", "rule", "🔑 ד. $P=\\dfrac{1/4}{1}=\\dfrac14$"))

ex2 = Scene("ex2", "המשלים", [
    P("ועכשיו: מה ההסתברות ש-$X+2Y$ קטן משתיים?", say="ועכשיו: מה ההסתברות שאִקְס ועוד שתיים וַואי קטן משתיים?",
      do=show("b-q")),
    P("הקו עובר בנקודה אפס ואחת, ובנקודה שבה $x$ אחת והגובה חצי.",
      say="הקו עובר בנקודה אפס ואחת, ובנקודה שבה אִקְס אחת והגובה חצי.", do=show("pb-l", "b-1")),
    P("שימו לב: הוא לא מגיע לציר האופקי בתוך הריבוע. הוא יוצא מהצלע הימנית.", hold=0.2),
    P("הראשית מקיימת את האי-שוויון, ולכן האירוע הוא כל מה שמתחת לקו.", do=show("pb-ev")),
    P("זה כבר לא משולש. אבל מה שנשאר בחוץ, מעל הקו, הוא משולש קטן.", do=show("pb-cp", "b-2")),
    P("הניצבים שלו: אחת לאורך הצלע העליונה, וחצי לאורך הצלע הימנית. השטח: רבע.", do=show("pb-tc")),
    P("לכן השטח של האירוע הוא אחת פחות רבע, כלומר שלושה רבעים.", do=show("pb-t", "b-3")),
    P("וזה הכלל: כשהאזור אינו משולש, כי הקו יוצא דרך צלע, מחשבים את המשלים ומחסירים.", do=show("b-4"), hold=0.4),
], stage=f'<div class="geo-stack">{pb.svg()}</div>',
   panel=st.card("b-q", "ex", "$P(X+2Y<2)=\\,?$")
         + st.card("b-1", "plain", "הקו: $(0,1)\\to\\left(1,\\frac12\\right)$")
         + st.card("b-2", "plain", "המשלים: משולש, $\\frac12\\cdot1\\cdot\\frac12=\\frac14$")
         + st.card("b-3", "rule", "🔑 $P=1-\\frac14=\\frac34$")
         + st.card("b-4", "rule", "🔑 האזור אינו משולש (הקו יוצא דרך צלע): משלים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: שני גפרורים, האורך של כל אחד אחיד בין אפס ל-$L$, והם בלתי תלויים.",
      say="שאלה ממבחן: שני גפרורים, האורך של כל אחד אחיד בין אפס לאֶל, והם בלתי תלויים."),
    P("מה ההסתברות שסכום האורכים לא עולה על ארבעה שלישים $L$?", say="מה ההסתברות שסכום האורכים לא עולה על ארבעה שלישים אֶל?"),
    P("מרחב המדגם: ריבוע בצלע $L$, והשטח שלו $L^2$.", say="מרחב המדגם: ריבוע בצלע אֶל, והשטח שלו אֶל בריבוע.",
      do=show("x-1")),
    P("הקו פוגש את הצלע העליונה בשליש $L$, ואת הצלע הימנית בגובה שליש $L$.",
      say="הקו פוגש את הצלע העליונה בשליש אֶל, ואת הצלע הימנית בגובה שליש אֶל.", do=show("px-l")),
    P("הראשית מקיימת את האי-שוויון, ולכן האירוע הוא הכל חוץ מהפינה הימנית העליונה.", do=show("px-ev", "px-cp")),
    P("הפינה הזו היא משולש עם ניצבים של שני שלישים $L$. השטח: שתי תשיעיות $L$ בריבוע.",
      say="הפינה הזו היא משולש עם ניצבים של שני שלישים אֶל. השטח: שתי תשיעיות אֶל בריבוע.", do=show("px-tc", "x-2")),
    P("מחלקים ב-$L^2$ ומחסירים מאחת: שבע תשיעיות.", say="מחלקים באֶל בריבוע ומחסירים מאחת: שבע תשיעיות.",
      do=show("px-t", "x-3"), hold=0.3),
    P("ושתי מלכודות. הראשונה: לעצור בשתי תשיעיות, ולשכוח שזה המשלים.", do=show("x-t1")),
    P("השנייה: לחשב משולש בפינת הראשית עם ניצבים ארבעה שלישים. יוצא שמונה תשיעיות.", do=show("px-big", "x-t2")),
    P("אבל המשולש הזה חורג מהריבוע: הקו יוצא מהצלעות לפני שהוא מגיע לצירים.", hold=0.5),
], stage=f'<div class="geo-stack">{px.svg()}</div>',
   panel=STEM
         + st.card("x-1", "plain", "$|\\Omega|=L^2$, והקו $x+y=\\frac43L$")
         + st.card("x-2", "plain", "משלים: $\\frac12\\left(\\frac23L\\right)^2=\\frac29L^2$")
         + st.card("x-3", "rule", "🔑 $P=1-\\frac29=\\frac79$")
         + st.card("x-t1", "trap", "⚠️ $\\frac29$ הוא המשלים")
         + st.card("x-t2", "trap", "⚠️ $\\frac12\\left(\\frac43\\right)^2=\\frac89$: המשולש חורג מהריבוע"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ארבעה צעדים. מציירים את הקו בעזרת שתי נקודות.", do=show("r-1")),
    P("בוחרים צד בעזרת נקודת מבחן, כמו הראשית.", do=show("r-2")),
    P("מחשבים את השטח: חצי, ניצב, כפול ניצב. ואם האזור גדול, דרך המשלים.", do=show("r-3")),
    P("ובודקים איפה הקו יוצא מהמלבן לפני שמחשבים משולש. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="geo-stack"><div class="geo-big">$\\text{S}=\\frac12\\cdot a\\cdot b$</div></div>',
   panel=st.card("r-1", "rule", "🔑 א. הקו: שתי נקודות")
         + st.card("r-2", "rule", "🔑 ב. הצד: נקודת מבחן")
         + st.card("r-3", "rule", "🔑 ג. השטח, או $1-$ המשלים")
         + st.card("r-4", "trap", "⚠️ קודם בודקים איפה הקו חותך את המלבן"))

VIDEO = Video("G02", "geo", "חצאי מישור: קו אחד וצד אחד", [title, idea, ex1, ex2, exam, recap],
              bank={"24B-A-Q1c": None})
