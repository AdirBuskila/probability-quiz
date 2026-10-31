# -*- coding: utf-8 -*-
"""E04 · הסתברות מותנית: המכנה הנכון — video script (build: tools/video/vid.py E04).

Source: courses/events/C04.js (lesson + goal: P(A/B) = P(A∩B)/P(B); the numerator is "both", the denominator is what
is known). Exam anchor: 24A-B-Q2d (two dice multiplied; given the product is at most 18, P(both odd)), an open question
(bank key None) that no guided quiz uses.
Avoided on purpose: the C04 quiz cases (sum 8 & first even, "at least one 6" & sum ≥ 10, sum 6 & different, the
p,q,s data 0.5/0.4/0.7, "of those who passed math…") and 24A-B-Q2b / 25A-C-Q2a (C10 boss and C04 quiz: sum 5 &
first > 3, and P(A/B) from p, q, s — the p,q,s formula is never shown here). The worked example conditions on a
difference (not a sum) and asks about both dice (not the first one), so it is not a renumbered C04-Q1.
Worked example: two dice, given the dice differ by exactly 2, P(both even) = 4/8 = 1/2, and the reverse direction
P(differ by 2 / both even) = 4/9. Every count comes from the checker's dice(2) space (w_events.Space.dice), with
Monte Carlo.
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- numbers (verified)
S = w.Space.dice(2)
D2 = lambda o: abs(o["d1"] - o["d2"]) == 2
EE = lambda o: o["d1"] % 2 == 0 and o["d2"] % 2 == 0
pairs = sorted((o["d1"], o["d2"]) for o, _ in S.out if D2(o))
assert pairs == [(1, 3), (2, 4), (3, 1), (3, 5), (4, 2), (4, 6), (5, 3), (6, 4)]
assert S.count(D2) == 8 and S.count(lambda o: D2(o) and EE(o)) == 4 and S.count(EE) == 9
PA_B = S.both(EE, given=D2)
PB_A = S.both(D2, given=EE)
assert PA_B == Fr(1, 2) and PB_A == Fr(4, 9) and PA_B != PB_A
assert S.P(lambda o: D2(o) and EE(o)) == Fr(4, 36) == Fr(1, 9)            # the trap: dividing by |Ω|
assert S.P(EE) == Fr(1, 4) != PA_B                                          # here the information doubles P(A)

# exam 24A-B-Q2d
Q = BANK["24A-B-Q2d"]
assert "\\frac{8}{28}=\\frac27" in Q["solution"].replace(" ", "")
C = lambda o: o["d1"] * o["d2"] <= 18
D = lambda o: o["d1"] % 2 == 1 and o["d2"] % 2 == 1
assert S.count(C) == 28 and S.count(D) == 9 and S.count(lambda o: C(o) and D(o)) == 8
assert S.count(lambda o: not C(o)) == 8 and sorted((o["d1"], o["d2"]) for o, _ in S.out if not C(o)) == \
    [(4, 5), (4, 6), (5, 4), (5, 5), (5, 6), (6, 4), (6, 5), (6, 6)]
PD_C = S.both(D, given=C)
assert PD_C == Fr(8, 28) == Fr(2, 7)
assert S.P(lambda o: C(o) and D(o)) == Fr(8, 36) == Fr(2, 9)               # trap 1: dividing by 36
assert Fr(9, 28) != PD_C and S.P(D) == Fr(1, 4)                            # trap 2: counting 5·5 = 25 as well

# ---------------------------------------------------------------- figures
DIFF = lambda i, j: abs(i - j)


def grid(pfx, cond_shown=False):
    g = w.DiceGrid(pfx, values=DIFF)
    g.layer("dim", lambda i, j: abs(i - j) != 2, "dim")
    g.layer("B", lambda i, j: abs(i - j) == 2, "cond")
    g.layer("AB", lambda i, j: abs(i - j) == 2 and i % 2 == 0 and j % 2 == 0, "both")
    g.layer("A", lambda i, j: i % 2 == 0 and j % 2 == 0, "ev")
    svg = g.svg()
    if cond_shown:
        svg = svg.replace(f'<g id="{pfx}-dim" class="h">', f'<g id="{pfx}-dim">').replace(
            f'<g id="{pfx}-B" class="h">', f'<g id="{pfx}-B">')
    return svg


gx = w.DiceGrid("gx", values=lambda i, j: i * j)
gx.layer("nc", lambda i, j: i * j > 18, "dim")
gx.layer("C", lambda i, j: i * j <= 18, "cond")
gx.layer("D", lambda i, j: i % 2 == 1 and j % 2 == 1, "ev")
gx.layer("x55", lambda i, j: (i, j) == (5, 5), "bad")

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>מטילים קובייה מאוזנת פעמיים ומכפילים את התוצאות. '
        '<b>אם ידוע</b> שהמכפלה לא עולה על 18, מה ההסתברות ששתי התוצאות אי-זוגיות?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד הסתברות מותנית: מה ההסתברות למשהו, **אם ידוע** שקרה משהו אחר."),
    P("נראה שהטעות הנפוצה היא כמעט תמיד במכנה, ונלמד איך לבחור אותו נכון."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">E04 · הסתברות מותנית</div><h1>הסתברות מותנית: המכנה הנכון</h1>'
         '<p>לחשב $P(A/B)$: המונה הוא החיתוך, והמכנה הוא מה שידוע.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("מטילים שתי קוביות הוגנות. כל אחד משלושים ושישה הזוגות סביר באותה מידה. בכל משבצת כתוב ההפרש בין הקוביות.",
      do=show("i-0")),
    P("ועכשיו מישהו מספר לנו: **ההפרש בין הקוביות הוא בדיוק שתיים**. מה השתנה?", do=show("g1-B")),
    P("רוב הזוגות כבר לא אפשריים. נשארו רק שמונה: שני אלכסונים, אחד מכל צד.", do=show("g1-dim")),
    P("המידע **מצמצם את העולם**: מרחב המדגם החדש הוא שמונת הזוגות האלה, והם עדיין שווים בסבירות.",
      do=show("i-1"), hold=0.3),
    P("ההגדרה: ההסתברות של $A$ בהינתן $B$ היא ההסתברות של החיתוך, חלקי ההסתברות של $B$.",
      say="ההגדרה: ההסתברות של אֵיי בהינתן בִּי היא ההסתברות של החיתוך, חלקי ההסתברות של בִּי.", do=show("i-2")),
    P("במונה: שני התנאים יחד. במכנה: מה שידוע.", hold=0.2),
    P("וכשהתוצאות שוות בסבירות, זו פשוט ספירה: כמה תוצאות בחיתוך, מתוך כמה תוצאות ב-$B$.",
      say="וכשהתוצאות שוות בסבירות, זו פשוט ספירה: כמה תוצאות בחיתוך, מתוך כמה תוצאות בבִּי.", do=show("i-3"), hold=0.4),
], stage=f'<div class="ev-stack">{grid("g1")}</div>',
   panel=st.card("i-0", "plain", "$36$ זוגות, כל אחד בהסתברות $\\frac{1}{36}$")
         + st.card("i-1", "ex", "ידוע: הפרש $2$. נשארו $8$ זוגות")
         + st.card("i-2", "rule", "🔑 $P(A/B)=\\dfrac{P(A\\cap B)}{P(B)}$")
         + st.card("i-3", "rule", "🔑 בספירה: $\\dfrac{|A\\cap B|}{|B|}$"))

ex1 = Scene("ex1", "דוגמה: הפרש 2", [
    P("השאלה: אם ידוע שההפרש שתיים, מה ההסתברות ש**שתי** הקוביות זוגיות?", do=show("a-1")),
    P("$B$ הוא ההפרש שתיים: שמונה זוגות. זה המכנה.", say="בִּי הוא ההפרש שתיים: שמונה זוגות. זה המכנה.", do=show("a-2")),
    P("מתוכם, שתיהן זוגיות בארבעה: שתיים וארבע, ארבע ושתיים, ארבע ושש, ושש וארבע. זה המונה.",
      do=show("g2-AB", "a-3")),
    P("לכן ההסתברות היא ארבעה מתוך שמונה, כלומר חצי.", do=show("a-4"), hold=0.3),
    P("והמלכודת: לחלק בשלושים ושש. ארבע חלקי שלושים ושש היא ההסתברות ש**שני** הדברים קרו, בלי שום מידע מראש.",
      do=show("a-t")),
    P("אבל אחרי ש**ידוע** שההפרש שתיים, עשרים ושמונה זוגות אחרים כבר לא בתמונה. מחלקים רק במה שנשאר.", hold=0.4),
], stage=f'<div class="ev-stack">{grid("g2", cond_shown=True)}</div>',
   panel=st.card("a-1", "plain", "$A$: שתיהן זוגיות. $B$: הפרש $2$. $\\;P(A/B)=\\,?$")
         + st.card("a-2", "ex", "$|B|=8$")
         + st.card("a-3", "ex", "$|A\\cap B|=4$")
         + st.card("a-4", "rule", "🔑 $P(A/B)=\\frac48=\\frac12$")
         + st.card("a-t", "trap", "⚠️ $\\frac{4}{36}$ הוא $P(A\\cap B)$, לא $P(A/B)$"))

ex2 = Scene("ex2", "הכיוון ההפוך", [
    P("ועכשיו נהפוך את השאלה: אם ידוע ששתי הקוביות זוגיות, מה ההסתברות שההפרש שתיים?",
      do=hide("g3-dim", "g3-B") + show("g3-A", "b-1")),
    P("עכשיו מה שידוע הוא שתיהן זוגיות: שלוש שורות כפול שלוש עמודות, תשעה זוגות. זה המכנה החדש.", do=show("b-2")),
    P("החיתוך לא השתנה: אותם ארבעה זוגות. ולכן ההסתברות היא ארבע תשיעיות.", do=show("g3-AB", "b-3")),
    P("חצי מול ארבע תשיעיות. אותו חיתוך, מכנה אחר, ותשובה אחרת.", hold=0.3),
    P("הכלל: מה שכתוב אחרי הקו האלכסוני הוא מה שידוע, והוא המכנה.", do=show("b-4"), hold=0.4),
], stage=f'<div class="ev-stack">{grid("g3", cond_shown=True)}</div>',
   panel=st.card("b-1", "plain", "הכיוון ההפוך: $P(B/A)=\\,?$")
         + st.card("b-2", "ex", "$|A|=9$")
         + st.card("b-3", "ex", "$P(B/A)=\\frac{4}{9}\\ne\\frac12$")
         + st.card("b-4", "trap", "⚠️ $P(A/B)$ מחלקים ב-$P(B)$; $\\;P(B/A)$ מחלקים ב-$P(A)$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. מטילים קובייה מאוזנת פעמיים, ו**מכפילים** את התוצאות.", do=show("x-stem")),
    P("אם ידוע שהמכפלה לא עולה על שמונה עשרה, מה ההסתברות ששתי התוצאות אי-זוגיות?"),
    P("בכל משבצת כתובה המכפלה. נתחיל ממה שידוע: המכפלה שמונה עשרה לכל היותר.", do=show("gx-C")),
    P("מחוץ לתנאי יש רק שמונה זוגות, בפינה של המספרים הגדולים. נשארו עשרים ושמונה. זה המכנה.",
      do=show("gx-nc", "x-1")),
    P("עכשיו המונה: שתי התוצאות אי-זוגיות **וגם** בתוך התנאי.", do=show("gx-D")),
    P("זוגות אי-זוגיים יש תשעה. אבל חמש כפול חמש זה עשרים וחמש, יותר משמונה עשרה: הוא מחוץ לתנאי.",
      do=show("gx-x55", "x-2")),
    P("נשארו שמונה. ההסתברות: שמונה חלקי עשרים ושמונה, כלומר שתי שביעיות.", do=show("x-3"), hold=0.3),
    P("שתי מלכודות. הראשונה: לחלק בשלושים ושש, ולקבל שתי תשיעיות. זו ההסתברות בלי המידע.", do=show("x-t1")),
    P("השנייה: לספור את כל תשעת הזוגות האי-זוגיים, ולשכוח שאחד מהם בכלל לא אפשרי אחרי שהמידע ניתן.",
      do=show("x-t2")),
    P("המונה הוא תמיד חיתוך: מה ששואלים, וגם מה שידוע.", hold=0.5),
], stage=f'<div class="ev-stack">{gx.svg()}</div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-1", "ex", "$|C|=36-8=28$")
         + st.card("x-2", "ex", "$|C\\cap D|=9-1=8$")
         + st.card("x-3", "rule", "🔑 $P(D/C)=\\frac{8}{28}=\\frac27$")
         + st.card("x-t1", "trap", "⚠️ $\\frac{8}{36}$: חילקו ב-$|\\Omega|$. "
                   '<span id="x-t2" class="h">$\\frac{9}{28}$: גם $5\\cdot5$</span>'))

recap = Scene("recap", "סיכום", [
    P("לסיכום: אם ידוע ש-$B$ קרה, העולם מצטמצם ל-$B$.", say="לסיכום: אם ידוע שבִּי קרה, העולם מצטמצם לבִּי.", do=show("r-1")),
    P("במונה: החיתוך, מה ששואלים וגם מה שידוע. במכנה: מה שידוע.", do=show("r-2")),
    P("וכשהתוצאות שוות בסבירות, סופרים: חיתוך מתוך התנאי.", do=show("r-3")),
    P("ושימו לב לכיוון: מה שאחרי הקו האלכסוני הוא המכנה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$P(A/B)=\\dfrac{P(A\\cap B)}{P(B)}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 ידוע $B$: העולם הוא $B$")
         + st.card("r-2", "rule", "🔑 מונה: $A\\cap B$. מכנה: $B$")
         + st.card("r-3", "rule", "🔑 $\\dfrac{|A\\cap B|}{|B|}$, לא $\\dfrac{|A\\cap B|}{|\\Omega|}$")
         + st.card("r-4", "trap", "⚠️ $P(A/B)\\ne P(B/A)$"))

VIDEO = Video("E04", "events", "הסתברות מותנית: המכנה הנכון", [title, idea, ex1, ex2, exam, recap],
              bank={"24A-B-Q2d": None})
