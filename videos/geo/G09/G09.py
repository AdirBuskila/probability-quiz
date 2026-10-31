# -*- coding: utf-8 -*-
"""G09 · מבחן גמר: שאלה 1 מהמבחנים האמיתיים — boss walkthrough (build: tools/video/vid.py G09).

Source: courses/geo/C09.js (boss: the area-method checklist). Exam anchors, all open questions (bank key None) of one
real question 1, none used by any guided quiz or boss: 26A-A-Q1a (the left piece is the shortest: 5/12),
26A-A-Q1d (the middle piece is the longest: 2/3), 26A-A-Q1e (all three pieces equal: 0).
Context 26A-A-c1: a unit segment cut into three pieces, X1 = left ~ U(0,1/2), X2 = right ~ U(0,1/2), middle 1-X1-X2.
Avoided on purpose: the six C09 boss parts (24A-B-Q1d, 24S-A-Q1c, 24B-A-Q1d, 25A-A-Q1b, 24S-B-Q1c, 25B-A-Q1d) and their
context-mates that would reveal them (25A-A-Q1c, 25B-A-Q1b/c, 24S-B-Q1a), every C01..C08 quiz case, and the parts
already solved in G01..G08 (24B-B-Q1a, 24B-A-Q1c, 24A-E-Q1d, 25S-A-Q1d, 24S-B-Q1b, 25S-A-Q1b, 26A-B-Q1a, 25S-B-Q1b).
Every area is an exact polygon (w_geo.clip), cross-checked by the closed form and by Monte Carlo.
"""
from fractions import Fraction as Fr
import numpy as np
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_geo as g

H = Fr(1, 2)
B = ((0, H), (0, H))
OM = H * H
assert OM == Fr(1, 4)

# (a) the left piece is the shortest: x1 < x2 and x1 < 1 - x1 - x2  <=>  x1 < x2 < 1 - 2 x1
QA = BANK["26A-A-Q1a"]
assert "\\frac{5}{12}" in QA["solution"].replace(" ", "") and QA["contextId"] == "26A-A-c1"
EA = [(1, -1, 0, "<"), (2, 1, 1, "<")]
PA = g.clip(EA, *B)
assert set(PA) == {(0, 0), (0, H), (Fr(1, 4), H), (Fr(1, 3), Fr(1, 3))}
SA = g.area(PA)
TRI = Fr(1, 2) * H * H                                     # the triangle above the diagonal, legs 1/2
CUT = Fr(1, 2) * Fr(1, 4) * (H - Fr(1, 3))                 # cut off by x2 = 1 - 2 x1: base 1/4, height 1/6
assert TRI == Fr(1, 8) and CUT == Fr(1, 48) and SA == TRI - CUT == Fr(5, 48)
assert SA / OM == Fr(5, 12)
g.mc(lambda a, b: (a < b) & (a < 1 - a - b), (0, .5), (0, .5), Fr(5, 12))
assert TRI / OM == Fr(1, 2)                                 # the trap: only "left shorter than right"

# (d) the middle piece is the longest: 1-x1-x2 > x1 and > x2  <=>  x2 < 1 - 2 x1 and x2 < (1 - x1)/2
QD = BANK["26A-A-Q1d"]
assert "\\frac23" in QD["solution"].replace(" ", "") and QD["contextId"] == "26A-A-c1"
ED = [(2, 1, 1, "<"), (1, 2, 1, "<")]
PD = g.clip(ED, *B)
assert set(PD) == {(0, 0), (H, 0), (Fr(1, 3), Fr(1, 3)), (0, H)}
SD = g.area(PD)
C1 = g.area(g.clip([(2, 1, 1, ">"), (1, -1, 0, ">")], *B))      # X1 is the longest
C2 = g.area(g.clip([(1, 2, 1, ">"), (1, -1, 0, "<")], *B))      # X2 is the longest
assert C1 == C2 == Fr(1, 24) and SD == OM - C1 - C2 == Fr(1, 6) and SD / OM == Fr(2, 3)
g.mc(lambda a, b: (1 - a - b > a) & (1 - a - b > b), (0, .5), (0, .5), Fr(2, 3))

assert 1 - 2 * Fr(1, 4) == Fr(1, 2)                         # averages: E[X1] = E[X2] = 1/4, the middle 1/2

# (e) all three equal: x1 = x2 = 1 - x1 - x2 -> the single point (1/3, 1/3), area 0
QE = BANK["26A-A-Q1e"]
assert "=0" in QE["solution"].replace(" ", "") and QE["contextId"] == "26A-A-c1"
import sympy as sp
a1, a2 = sp.symbols("a1 a2")
assert sp.solve([a1 - a2, a2 - (1 - a1 - a2)], [a1, a2]) == {a1: sp.Rational(1, 3), a2: sp.Rational(1, 3)}

# ---------------------------------------------------------------- figures
TK = [(Fr(1, 4), "1/4"), (Fr(1, 3), "1/3"), (H, "1/2")]
X1 = 'X<tspan dy="8" font-size="22">1</tspan>'
X2 = 'X<tspan dy="8" font-size="22">2</tspan>'
pa = g.Plane("pa", *B, maxw=440, maxh=440, xlab=X1, ylab=X2, xticks=TK, yticks=[(Fr(1, 3), "1/3"), (H, "1/2")])
pa.line("d", -1, 1, 0, cls="ln alt", label="x₂ = x₁", at=(.2, .2), dx=14, dy=26)
pa.region("tri", [(1, -1, 0, "<")], "warn")
pa.region("ev", EA, "ev")
pa.region("cut", [(1, -1, 0, "<"), (2, 1, 1, ">")], "comp")
pa.line("l", 2, 1, 1, label="x₂ = 1 − 2x₁", at=(.47, .06), dx=12, dy=-8)
pa.pt("m", Fr(1, 3), Fr(1, 3), "", dx=0, dy=0)
pa.text("t", .1, .3, "5/48")
pa.text("tc", .36, .45, "1/48", cls="geo-tag")

pd = g.Plane("pd", *B, maxw=440, maxh=440, xlab=X1, ylab=X2, xticks=[(Fr(1, 3), "1/3"), (H, "1/2")],
             yticks=[(Fr(1, 3), "1/3"), (H, "1/2")])
pd.region("ev", ED, "ev")
pd.region("c1", [(2, 1, 1, ">"), (1, -1, 0, ">")], "comp")
pd.region("c2", [(1, 2, 1, ">"), (1, -1, 0, "<")], "comp")
pd.line("l1", 2, 1, 1)
pd.line("l2", 1, 2, 1, cls="ln alt")
pd.seg("dg", (Fr(1, 3), Fr(1, 3)), (H, H), dash=True)
pd.pt("m", Fr(1, 3), Fr(1, 3), "(1/3, 1/3)", dx=-14, dy=-14, anchor="end")
pd.text("t1", .44, .19, "1/24")
pd.text("t2", .2, .47, "1/24")
pd.text("t", .17, .14, "1/6")

FIG = st.raster("x-fig", "images/exams/26A-A-c1-segment.png", 420, (306, 212))
CTX = ('<div class="qstem"><span class="qid">26A-A-Q1</span>קטע באורך $1$ נחתך בשתי נקודות לשלושה קטעים. '
       'השמאלי <span class="nobr">$X_1\\sim U_c\\left(0,\\frac12\\right)$</span>, הימני '
       '<span class="nobr">$X_2\\sim U_c\\left(0,\\frac12\\right)$</span>, בלתי תלויים, והאמצעי '
       '<span class="nobr">$1-X_1-X_2$</span>.</div>')

title = Scene("title", "", [
    P("זה הסרטון האחרון בקורס: נפתור יחד שאלה אחת מלאה ממבחן, שלושה סעיפים."),
    P("בכל סעיף נעבור על רשימת הבדיקה של שיטת השטח, צעד אחר צעד.", hold=0.4),
], stage='<div class="kicker">G09 · הסתברות גיאומטרית</div><h1>מבחן גמר: שאלה 1 מהמבחנים האמיתיים</h1>'
         '<p>לפתור סעיפים מלאים משאלה 1 האמיתית: אירוע, חיתוך, משלים, ומאורע בעל שטח אפס.</p>', layout="title")

check = Scene("check", "רשימת הבדיקה", [
    P("השאלה: קטע באורך אחת נחתך בשתי נקודות לשלושה קטעים."),
    P("הקטע השמאלי אחיד בין אפס לחצי, וגם הימני, בלי תלות. האמצעי הוא מה שנשאר.", hold=0.2),
    P("רשימת הבדיקה. אחת: מי המשתנים, מה הטווחים, ומה השטח של אומגה.", do=show("c-1")),
    P("שתיים: מה האי-שוויון. קו ישר או עקום, ואיזה צד שלו.", do=show("c-2")),
    P("שלוש: וגם זה חיתוך. או זה איחוד, ועדיף לעבור למשלים.", do=show("c-3")),
    P("וארבע: התוצאה בין אפס לאחת, ומתאימה לאיור. ובמבחן כותבים את כל הדרך, לא רק את התשובה.", do=show("c-4"), hold=0.4),
], stage=f'<div class="geo-stack">{FIG}{CTX}</div>',
   panel=st.card("c-1", "rule", "🔑 משתנים, טווחים, $|\\Omega|$")
         + st.card("c-2", "rule", "🔑 אי-שוויון: קו או עקום, ואיזה צד")
         + st.card("c-3", "rule", "🔑 \"וגם\": חיתוך. \"או\": משלים")
         + st.card("c-4", "trap", "⚠️ בודקים: בין $0$ ל-$1$, ומתאים לאיור"))

part_a = Scene("a", "סעיף א", [
    P("סעיף א: מה ההסתברות שהקטע השמאלי הוא הקצר ביותר?", do=show("a-q")),
    P("משתנים: שני הקטעים הצדדיים. מרחב המדגם הוא ריבוע בצלע חצי, והשטח שלו רבע."),
    P("השמאלי הקצר ביותר, פירושו: קצר מהימני, **וגם** קצר מהאמצעי. שני אי-שוויונות, חיתוך.", do=show("a-2")),
    P("קצר מהימני: מעל האלכסון. זה משולש עם ניצבים חצי, ושטח שמינית.", do=show("pa-d", "pa-tri")),
    P("קצר מהאמצעי: $x_1$ קטן מאחת פחות $x_1$ פחות $x_2$. כלומר $x_2$ קטן מאחת פחות שתיים $x_1$.",
      say="קצר מהאמצעי: אִקְס אחת קטן מאחת פחות אִקְס אחת פחות אִקְס שתיים. כלומר אִקְס שתיים קטן מאחת פחות שתיים אִקְס אחת.",
      do=show("pa-l")),
    P("הקו הזה פוגש את הצלע העליונה ברבע, ואת האלכסון בשליש.", do=show("pa-m", "a-3")),
    P("הוא חותך מהמשולש פינה קטנה: בסיס של רבע למעלה, וגובה של חצי פחות שליש, כלומר שישית.", do=show("pa-cut", "pa-tc")),
    P("השטח שלה: חצי כפול רבע כפול שישית, כלומר אחת חלקי ארבעים ושמונה.", say="השטח שלה: חצי כפול רבע כפול שישית, כלומר אחת חלקי ארבעים ושמונה."),
    P("נשאר שמינית פחות אחת חלקי ארבעים ושמונה: חמש חלקי ארבעים ושמונה.", do=show("pa-ev", "pa-t", "a-4")),
    P("ומחלקים ברבע: ההסתברות היא חמש חלקי שתים עשרה.", do=show("a-5"), hold=0.3),
    P("המלכודת: לעצור אחרי התנאי הראשון. אז יוצא חצי, ושוכחים שהשמאלי צריך להיות קצר גם מהאמצעי.", do=show("a-t"), hold=0.4),
], stage=f'<div class="geo-stack">{pa.svg()}</div>',
   panel=st.card("a-q", "ex", "א. השמאלי הקצר ביותר? $\\;|\\Omega|=\\frac14$")
         + st.card("a-2", "plain", "$x_1<x_2$ וגם $x_2<1-2x_1$")
         + st.card("a-3", "plain", "מפגש: $\\left(\\frac13,\\frac13\\right)$; צלע עליונה: $x_1=\\frac14$")
         + st.card("a-4", "plain", "$\\frac18-\\frac12\\cdot\\frac14\\cdot\\frac16=\\frac5{48}$")
         + st.card("a-5", "rule", "🔑 $P=\\frac{5/48}{1/4}=\\frac5{12}$")
         + st.card("a-t", "trap", "⚠️ רק $X_1<X_2$ נותן $\\frac12$"))

part_d = Scene("d", "סעיף ד", [
    P("סעיף ד: מה ההסתברות שהקטע האמצעי הוא הארוך ביותר?", do=show("d-q")),
    P("האמצעי ארוך מהשמאלי: $x_2$ קטן מאחת פחות שתיים $x_1$. אותו קו כמו קודם.",
      say="האמצעי ארוך מהשמאלי: אִקְס שתיים קטן מאחת פחות שתיים אִקְס אחת. אותו קו כמו קודם.", do=show("pd-l1", "d-1")),
    P("והאמצעי ארוך מהימני: $x_2$ קטן מאחת פחות $x_1$, חלקי שתיים.",
      say="והאמצעי ארוך מהימני: אִקְס שתיים קטן מאחת פחות אִקְס אחת, חלקי שתיים.", do=show("pd-l2")),
    P("שני הקווים נפגשים בנקודה שליש ושליש. האזור הוא מתחת לשניהם.", do=show("pd-m", "pd-ev")),
    P("זה מרובע. קל יותר לחשב את המשלים: שני משולשים, אחד ליד כל צלע.", do=show("pd-c1", "pd-c2", "pd-dg")),
    P("המשולש הימני הוא המקרה שבו השמאלי הכי ארוך. הבסיס שלו חצי, על הצלע הימנית, והגובה שישית.",
      do=show("pd-t1", "d-2")),
    P("השטח: אחת חלקי עשרים וארבע. והשני זהה לו, בגלל הסימטריה בין שני הקטעים.", do=show("pd-t2")),
    P("נשאר רבע פחות שתיים חלקי עשרים וארבע: שישית. ומחלקים ברבע: שני שלישים.", do=show("pd-t", "d-3"), hold=0.3),
    P("בדיקת היגיון: בממוצע כל קטע צדדי הוא רבע, והאמצעי הוא חצי. לכן לא מפתיע שהאמצעי הוא בדרך כלל הארוך.", hold=0.4),
], stage=f'<div class="geo-stack">{pd.svg()}</div>',
   panel=st.card("d-q", "ex", "ד. האמצעי הארוך ביותר? ($5$ נק׳)")
         + st.card("d-1", "plain", "$x_2<1-2x_1$ וגם $x_2<\\frac{1-x_1}{2}$")
         + st.card("d-2", "plain", "משלים: $2\\cdot\\frac12\\cdot\\frac12\\cdot\\frac16=\\frac1{12}$")
         + st.card("d-3", "rule", "🔑 $P=\\frac{1/4-1/12}{1/4}=\\frac23$"))

part_e = Scene("e", "סעיף ה", [
    P("סעיף ה: מה ההסתברות שלשלושת הקטעים יש אותו אורך?", do=show("e-q")),
    P("שלושה אורכים שווים, וסכומם אחת: כל אחד שליש. זו נקודה אחת במישור, שליש ושליש.", do=show("e-1")),
    P("לנקודה אין שטח. ולכן ההסתברות היא אפס, אף שהמאורע אפשרי.", do=show("e-2"), hold=0.3),
    P("אותו דבר לכל קו: למשל ההסתברות ששני הקטעים הצדדיים שווים היא אפס. במשתנים רציפים, רק אזור עם שטח נותן הסתברות חיובית.",
      do=show("e-3"), hold=0.4),
], stage=f'<div class="geo-stack">{FIG}</div>',
   panel=st.card("e-q", "ex", "ה. שלושת הקטעים שווים? ($5$ נק׳)")
         + st.card("e-1", "plain", "$X_1=X_2=1-X_1-X_2\\iff X_1=X_2=\\frac13$")
         + st.card("e-2", "rule", "🔑 נקודה: שטח $0$, ולכן $P=0$")
         + st.card("e-3", "trap", "⚠️ אפשרי, ובכל זאת הסתברות $0$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: שאלה אחת, שלושה סעיפים, ואותה שיטה בכל אחד.", do=show("r-1")),
    P("הקצר ביותר או הארוך ביותר הוא כמה אי-שוויונות יחד: חיתוך.", do=show("r-2")),
    P("כשהאזור מסובך, עוברים למשלים. וכשהמאורע הוא קו או נקודה, ההסתברות אפס.", do=show("r-3")),
    P("זה הסוף של הקורס. בהצלחה במבחן!", do=show("r-4"), hold=0.8),
], stage='<div class="geo-stack"><div class="geo-big">$P(A)=\\dfrac{S(A)}{|\\Omega|}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $|\\Omega|$ קודם, תמיד")
         + st.card("r-2", "rule", "🔑 \"הכי\": כמה אי-שוויונות, חיתוך")
         + st.card("r-3", "rule", "🔑 אזור מסובך: משלים. נקודה או קו: $0$")
         + st.card("r-4", "ex", "בהצלחה במבחן!"))

VIDEO = Video("G09", "geo", "מבחן גמר: שאלה 1 מהמבחנים האמיתיים", [title, check, part_a, part_d, part_e, recap],
              bank={"26A-A-Q1a": None, "26A-A-Q1d": None, "26A-A-Q1e": None})
