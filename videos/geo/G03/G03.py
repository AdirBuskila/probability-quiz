# -*- coding: utf-8 -*-
"""G03 · רצועות ומשולשים — video script (build: tools/video/vid.py G03).

Source: courses/geo/C03.js (lesson + goal). Exam anchor: 24A-E-Q1d (the grasshopper: X_L~U(0,1) left, X_R~U(0,2)
right; P(it ends right of O within 1/3) = P(0 < X_R - X_L < 1/3) = 1/6), an open question (bank key None) that no
guided quiz uses.
Avoided on purpose: the C03 quiz cases (|X-Y|<1/3, |X-Y|>1/4, X<Y & X+Y<1/2, 1/2<X+Y<3/2, |X-Y|<1/2 in (0,1)x(0,2)),
their twins 24S-A-Q1c (boss), 25B-B-Q1b / 25S-B-Q1b (the lesson's |X-Y|<1/2 band), C08's meeting (|X-Y|<1/4) and the
boss 24A-B-Q1d (X<Y<1-X, and its mirror Y>X & X+Y>1).
Worked examples: P(|X-Y|<2/3) = 8/9 (band = square minus two corner triangles), P(Y>3X and X+Y<1) = 1/8.
Every area is an exact polygon (w_geo.clip), cross-checked by the closed form and by Monte Carlo.
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

U = ((0, 1), (0, 1))
c = Fr(2, 3)
BAND = [(1, -1, c, "<"), (1, -1, -c, ">")]                 # -c < x - y < c
A1 = g.area(g.clip(BAND, *U))
T1 = g.area(g.clip([(1, -1, c, ">")], *U))                 # corner triangle x - y > 2/3
assert T1 == Fr(1, 2) * (1 - c) ** 2 == Fr(1, 18)
assert A1 == 1 - 2 * T1 == Fr(8, 9)
g.mc(lambda x, y: abs(x - y) < 2 / 3, *U, A1)

TWO = [(-3, 1, 0, ">"), (1, 1, 1, "<")]                     # y > 3x and x + y < 1
P2 = g.clip(TWO, *U)
A2 = g.area(P2)
assert set(P2) == {(0, 0), (0, 1), (Fr(1, 4), Fr(3, 4))}   # the two lines meet at (1/4, 3/4)
assert A2 == Fr(1, 2) * 1 * Fr(1, 4) == Fr(1, 8)           # base 1 on the y axis, height 1/4
g.mc(lambda x, y: (y > 3 * x) & (x + y < 1), *U, A2)

# exam 24A-E-Q1d: x = X_L ~ U(0,1), y = X_R ~ U(0,2); final position X_R - X_L, right of O within 1/3
Q = BANK["24A-E-Q1d"]
assert "\\frac16" in Q["solution"].replace(" ", "") and Q["contextId"] == "24A-E-c1"
R = ((0, 1), (0, 2))
OM = 2
EX = [(-1, 1, 0, ">"), (-1, 1, Fr(1, 3), "<")]            # 0 < y - x < 1/3
AX = g.area(g.clip(EX, *R))
assert AX == Fr(1, 3) and AX / OM == Fr(1, 6)              # a parallelogram: width 1, vertical thickness 1/3
assert 1 + Fr(1, 3) < 2                                    # it never reaches the top side y = 2
g.mc(lambda x, y: (y - x > 0) & (y - x < 1 / 3), *R, Fr(1, 6))

# ---------------------------------------------------------------- figures
pa = g.Plane("pa", *U, maxw=440, maxh=440, xticks=[(Fr(2, 3), "2/3"), (1, "1")],
             yticks=[(Fr(2, 3), "2/3"), (1, "1")])
pa.line("d", -1, 1, 0, cls="ln alt", label="y = x", at=(.86, .86), dx=-18, dy=-22, anchor="end")
pa.region("ev", BAND, "ev")
pa.region("t1", [(1, -1, c, ">")], "comp")
pa.region("t2", [(1, -1, -c, "<")], "comp")
pa.line("l1", -1, 1, c, label="y = x + 2/3", at=(1 / 3, 1), dx=8, dy=-14)
pa.line("l2", -1, 1, -c, label="y = x − 2/3", at=(2 / 3, 0), dx=-10, dy=-14, anchor="end")
pa.text("tt1", .89, .09, "1/18")
pa.text("tt2", .11, .88, "1/18")
pa.text("t", .5, .45, "8/9")

pb = g.Plane("pb", *U, maxw=440, maxh=440, xticks=[(Fr(1, 4), "1/4"), (1, "1")],
             yticks=[(Fr(3, 4), "3/4"), (1, "1")])
pb.line("l1", -3, 1, 0, label="y = 3x", at=(1 / 3, 1), dx=12, dy=-10)
pb.line("l2", 1, 1, 1, cls="ln alt", label="x + y = 1", at=(.7, .3), dx=10, dy=-8)
pb.region("ev", TWO, "ev")
pb.pt("m", Fr(1, 4), Fr(3, 4), "(1/4, 3/4)", dx=14, dy=-6)

px = g.Plane("px", *R, maxw=300, maxh=520, xlab='X<tspan dy="8" font-size="22">L</tspan>', ylab='X<tspan dy="8" font-size="22">R</tspan>', xticks=[(1, "1")],
             yticks=[(Fr(1, 3), "1/3"), (1, "1"), (Fr(4, 3), "4/3"), (2, "2")])
px.poly("om", [(0, 0), (1, 0), (1, 2), (0, 2)], "om")
px.line("d", -1, 1, 0, cls="ln alt")
px.region("ev", EX, "ev")
px.line("l", -1, 1, Fr(1, 3))
px.region("low", [(-1, 1, 0, "<"), (-1, 1, -Fr(1, 3), ">")], "comp")

FIG = st.raster("x-fig", "images/exams/24A-E-Q1-grasshopper.png", 560, (812, 502))
STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>חגב קופץ שמאלה <span class="nobr">$X_L\\sim U_c(0,1)$</span>'
        ' ואחר כך ימינה <span class="nobr">$X_R\\sim U_c(0,2)$</span>, בלתי תלויים. מה ההסתברות שבסוף הוא <b>ימינה</b>'
        ' מ-$O$, במרחק של שליש לכל היותר?</div>')

title = Scene("title", "", [
    P("בסרטון הזה נחשב הסתברות של רצועה סביב האלכסון, ושל שני אי-שוויונות יחד."),
    P("הכלי המרכזי: לחתוך את הריבוע לחלקים שיודעים לחשב, ולהחסיר.", hold=0.4),
], stage='<div class="kicker">G03 · הסתברות גיאומטרית</div><h1>רצועות ומשולשים</h1>'
         '<p>לחשב הסתברות של רצועה סביב האלכסון ושל חיתוך של שני אי-שוויונות.</p>', layout="title")

band = Scene("band", "רצועה", [
    P("הרבה שאלות שואלות אם שני מספרים קרובים: ההפרש ביניהם קטן מקבוע.", do=show("a-0")),
    P("ניקח את ריבוע היחידה, ונשאל: מה ההסתברות שההפרש בערך מוחלט קטן משני שלישים?", do=show("a-q")),
    P("ערך מוחלט קטן מ-$c$ פירושו שני אי-שוויונות: ההפרש בין מינוס $c$ ל-$c$.",
      say="ערך מוחלט קטן מסִי פירושו שני אי-שוויונות: ההפרש בין מינוס סִי לסִי.", do=show("a-1")),
    P("כלומר $y$ בין $x$ פחות שני שלישים, לבין $x$ ועוד שני שלישים.",
      say="כלומר וַואי בין אִקְס פחות שני שלישים, לבין אִקְס ועוד שני שלישים.", do=show("pa-d", "pa-l1", "pa-l2")),
    P("זו **רצועה** סביב האלכסון, בין שני קווים מקבילים.", do=show("pa-ev")),
    P("את השטח שלה הכי קל לחשב דרך מה שבחוץ: שני משולשים בפינות.", do=show("pa-t1", "pa-t2")),
    P("לכל משולש ניצבים של אחת פחות שני שלישים, כלומר שליש. השטח: חצי כפול שליש כפול שליש.",
      do=show("a-2", "pa-tt1", "pa-tt2")),
    P("זו אחת חלקי שמונה עשרה לכל משולש. שניהם יחד: תשיעית."),
    P("והרצועה: אחת פחות תשיעית, כלומר שמונה תשיעיות.", do=show("pa-t", "a-3"), hold=0.3),
    P("שימו לב לכיוון: ההפרש **גדול** מקבוע הוא דווקא שני המשולשים, לא הרצועה.", do=show("a-4"), hold=0.4),
], stage=f'<div class="geo-stack">{pa.svg()}</div>',
   panel=st.card("a-0", "plain", "$X,Y\\sim U_c(0,1)$ בלתי תלויים")
         + st.card("a-q", "ex", "$P\\left(|X-Y|<\\frac23\\right)=\\,?$")
         + st.card("a-1", "rule", "🔑 $|X-Y|<c\\iff x-c<y<x+c$")
         + st.card("a-2", "plain", "משולש: $\\frac12\\cdot\\frac13\\cdot\\frac13=\\frac1{18}$")
         + st.card("a-3", "rule", "🔑 $P=1-2\\cdot\\frac1{18}=\\frac89$")
         + st.card("a-4", "trap", "⚠️ $|X-Y|>c$: שני משולשי הפינה"))

two = Scene("two", "שני אי-שוויונות", [
    P("עכשיו שני אי-שוויונות יחד: $Y$ גדול משלוש $X$, **וגם** $X+Y$ קטן מאחת.",
      say="עכשיו שני אי-שוויונות יחד: וַואי גדול משלוש אִקְס, וגם אִקְס ועוד וַואי קטן מאחת.", do=show("b-q")),
    P("וגם פירושו חיתוך: הנקודות שמקיימות את שני התנאים בבת אחת.", do=show("b-1")),
    P("הקו הראשון יוצא מהראשית בשיפוע שלוש. האזור שמעליו.", do=show("pb-l1")),
    P("הקו השני יורד מהנקודה אפס ואחת. האזור שמתחתיו.", do=show("pb-l2")),
    P("הקווים נפגשים כששלוש $x$ שווה לאחת פחות $x$: ב-$x$ רבע, $y$ שלושה רבעים.",
      say="הקווים נפגשים כששלוש אִקְס שווה לאחת פחות אִקְס: באִקְס רבע, וַואי שלושה רבעים.", do=show("pb-m", "b-2")),
    P("החיתוך הוא משולש. הבסיס שלו על ציר $y$, מאפס עד אחת. והגובה: רבע.",
      say="החיתוך הוא משולש. הבסיס שלו על ציר וַואי, מאפס עד אחת. והגובה: רבע.", do=show("pb-ev")),
    P("השטח: חצי כפול אחת כפול רבע, כלומר שמינית. וזו ההסתברות.", do=show("b-3"), hold=0.4),
], stage=f'<div class="geo-stack">{pb.svg()}</div>',
   panel=st.card("b-q", "ex", "$P(Y>3X,\\ X+Y<1)=\\,?$")
         + st.card("b-1", "rule", "🔑 \"וגם\" = חיתוך")
         + st.card("b-2", "plain", "מפגש: $3x=1-x\\Rightarrow x=\\frac14$")
         + st.card("b-3", "rule", "🔑 $P=\\frac12\\cdot1\\cdot\\frac14=\\frac18$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: חגב בנקודה $O$ קופץ קודם שמאלה, למרחק אחיד בין אפס לאחת.",
      say="שאלה ממבחן: חגב בנקודה אוֹ קופץ קודם שמאלה, למרחק אחיד בין אפס לאחת."),
    P("אחר כך הוא קופץ ימינה, למרחק אחיד בין אפס לשתיים, בלי תלות בקפיצה הראשונה."),
    P("מה ההסתברות שבסוף הוא ימינה מ-$O$, במרחק של שליש לכל היותר?", say="מה ההסתברות שבסוף הוא ימינה מאוֹ, במרחק של שליש לכל היותר?"),
    P("המיקום הסופי ביחס ל-$O$ הוא הקפיצה ימינה פחות הקפיצה שמאלה.", say="המיקום הסופי ביחס לאוֹ הוא הקפיצה ימינה פחות הקפיצה שמאלה.",
      do=show("x-1")),
    P("ימינה במרחק עד שליש: ההפרש הזה בין אפס לשליש. שני אי-שוויונות."),
    P("מרחב המדגם הוא מלבן ברוחב אחת ובגובה שתיים. השטח שלו: שתיים.",
      do=hide("x-fig") + show("x-pl", "px-om")),
    P("התנאי הראשון: מעל האלכסון. התנאי השני: מתחת לקו המקביל, שליש מעליו.", do=show("px-d", "px-l")),
    P("האזור הוא מקבילית: ברוחב אחת, ובעובי אנכי של שליש. השטח שלה שליש.", do=show("px-ev", "x-4")),
    P("והיא כולה בתוך המלבן: הקו העליון מגיע לגובה ארבעה שלישים בלבד.", hold=0.2),
    P("מחלקים בשתיים: ההסתברות היא שישית.", do=show("x-5"), hold=0.3),
    P("המלכודת: לכתוב ערך מוחלט. אז נכנסת גם הרצועה שמתחת לאלכסון, כלומר שמאלה מ-$O$.",
      say="המלכודת: לכתוב ערך מוחלט. אז נכנסת גם הרצועה שמתחת לאלכסון, כלומר שמאלה מאוֹ.", do=show("px-low", "x-t")),
    P("והמלכודת השנייה: לשכוח לחלק בשתיים, ולענות שליש.", hold=0.5),
], stage=(f'<div class="geo-swap" style="--swap-h:640px"><div id="x-fig">{FIG}</div>'
          f'<div id="x-pl" class="h">{px.svg()}</div></div>'),
   panel=STEM
         + st.card("x-1", "plain", "המיקום הסופי: $X_R-X_L$; האירוע: $0<X_R-X_L<\\frac13$")
         + st.card("x-4", "plain", "$|\\Omega|=2$; מקבילית: $1\\cdot\\frac13=\\frac13$")
         + st.card("x-5", "rule", "🔑 $P=\\dfrac{1/3}{2}=\\dfrac16$")
         + st.card("x-t", "trap", "⚠️ \"ימינה\" הוא צד אחד של האלכסון"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הפרש בערך מוחלט קטן מקבוע הוא רצועה סביב האלכסון.", do=show("r-1")),
    P("את הרצועה מחשבים דרך שני משולשי הפינה: מורידים אותם מהריבוע.", do=show("r-2")),
    P("וגם בין שני אי-שוויונות הוא חיתוך: מוצאים את נקודת המפגש, ומחשבים משולש.", do=show("r-3")),
    P("ובמלבן שאינו ריבוע, בודקים שהאזור בתוכו, ומחלקים בשטח של אומגה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="geo-stack"><div class="geo-big">$|X-Y|<c\\iff x-c<y<x+c$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $|X-Y|<c$: רצועה סביב האלכסון")
         + st.card("r-2", "rule", "🔑 הרצועה: הריבוע פחות שני משולשי הפינה")
         + st.card("r-3", "rule", "🔑 \"וגם\": חיתוך, נקודת מפגש, משולש")
         + st.card("r-4", "trap", "⚠️ במלבן: מחלקים ב-$|\\Omega|$"))

VIDEO = Video("G03", "geo", "רצועות ומשולשים", [title, band, two, exam, recap], bank={"24A-E-Q1d": None})
