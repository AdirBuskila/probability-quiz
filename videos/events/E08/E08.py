# -*- coding: utf-8 -*-
"""E08 · בלתי תלויים מול זרים — video script (build: tools/video/vid.py E08).

Source: courses/events/C08.js (lesson + goal: decide independent / disjoint / both, never confuse them).
Exam part: an original question in exam style (bank={}): a random two-digit number, are A3 = "divisible by 3" and
A6 = "divisible by 6" independent? The bank's own version (25A-A-Q2c, A4 and A8 among three-digit numbers) is NOT
used: together with E02 it would give away the C10 boss 25A-A-Q2d (A8 = A2 ∩ A4?).
Avoided on purpose: the C08 quiz cases (disjoint 0.3/0.4, independent 0.3/0.4 union, one die "even" vs "> 3", two dice
"first even" & "second > 3", 1/2 & 1/3 disjoint, 0.4 & union 0.7) and 25A-A-Q2b / 25A-A-Q2d (A2 with A4; the
C10 boss asks whether A8 = A2 ∩ A4): the video never mentions A2, A4 or A8.
Worked example: one fair die, A = {1,2}, B = {1,3,5} (independent, not disjoint; also A with B̄), C = {5,6}
(disjoint from A, hence dependent). Every value comes from enumeration + Monte Carlo (w_events.Space).
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- numbers (verified)
S = w.Space.dice(1)
A = lambda o: o["d1"] in (1, 2)
B = lambda o: o["d1"] in (1, 3, 5)
C = lambda o: o["d1"] in (5, 6)
pA, pB, pC = S.P(A), S.P(B), S.P(C)
assert (pA, pB, pC) == (Fr(1, 3), Fr(1, 2), Fr(1, 3))
pAB = S.both(lambda o: A(o) and B(o))
assert pAB == Fr(1, 6) == pA * pB                                               # independent
assert pAB != 0                                                                 # not disjoint
assert S.P(A, given=B) == pA == Fr(1, 3)                                        # knowing B changes nothing
assert S.both(lambda o: A(o) and not B(o)) == pA * (1 - pB) == Fr(1, 6)         # A and B̄ independent too
pAC = S.both(lambda o: A(o) and C(o))
assert pAC == 0 != pA * pC == Fr(1, 9)                                          # disjoint, hence dependent
assert S.P(C, given=A) == 0 != pC

# exam-style part (original): two-digit numbers, A3 and A6
SX = w.Space.uniform([{"x": x} for x in range(10, 100)])
A3 = lambda o: o["x"] % 3 == 0
A6 = lambda o: o["x"] % 6 == 0
p3, p6 = SX.P(A3), SX.P(A6)
assert (SX.count(A3), SX.count(A6)) == (30, 15) and (99 // 6, 9 // 6) == (16, 1)
assert (p3, p6) == (Fr(1, 3), Fr(1, 6))
assert all(A3(o) for o, _ in SX.out if A6(o))                                   # A6 ⊆ A3
p36 = SX.both(lambda o: A3(o) and A6(o))
assert p36 == p6 == Fr(1, 6) and p3 * p6 == Fr(1, 18) and p36 != p3 * p6
assert SX.P(A3, given=A6) == 1 != p3                                            # knowing A6 makes A3 certain

V = w.Venn("v1")
V.fill("AB", ["ab"], "ev")
V.text("ta", "a", "2", shown=True)
V.text("tab", "ab", "1", shown=True)
V.text("tb", "b", "3   5", shown=True)
V.text("to", (600, 400), "4   6", shown=True)
# draw the disjoint pair honestly: two circles that do not overlap
V2 = w.Venn("v2", names=("A", "C"), r=130, gap=1.12)
V2.text("ta", "a", "1   2", shown=True)
V2.text("tb", "b", "5   6", shown=True)
V2.text("to", (350, 410), "3   4", shown=True)

ROWS = ('<table class="ev-tab" id="cmp"><thead><tr><th></th><th>התנאי</th><th>המשמעות</th></tr></thead><tbody>'
        '<tr><th class="ev-rh">זרים</th><td>$P(A\\cap B)=0$</td><td>אחד מונע את השני</td></tr>'
        '<tr><th class="ev-rh">בלתי תלויים</th><td>$P(A\\cap B)=P(A)P(B)$</td><td>אחד לא משנה את השני</td></tr>'
        '</tbody></table>')


STEM = ('<div class="qstem"><span class="qid">בסגנון מבחן</span>בוחרים מספר דו-ספרתי באקראי. '
        '$A_3$: מתחלק ב-3, $A_6$: מתחלק ב-6. האם $A_3$ ו-$A_6$ בלתי תלויים?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נפריד בין שני מושגים שמתבלבלים כל הזמן: מאורעות **זרים**, ומאורעות **בלתי תלויים**."),
    P("נראה שהם לא רק שונים, אלא כמעט הפוכים."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">E08 · אי-תלות</div><h1>בלתי תלויים מול זרים</h1>'
         '<p>להכריע אם שני מאורעות בלתי תלויים, זרים, או אף אחד מהשניים.</p>',
   layout="title")

idea = Scene("idea", "שתי הגדרות", [
    P("**זרים**: אין להם אף תוצאה משותפת. ההסתברות של החיתוך היא אפס.", do=show("cmp")),
    P("כלומר אם אחד קרה, השני בוודאות לא קרה. זה מידע חזק מאוד: הם **תלויים** מאוד."),
    P("**בלתי תלויים**: ההסתברות של החיתוך שווה למכפלת ההסתברויות.", hold=0.2),
    P("ובמילים: לדעת שאחד קרה לא משנה את ההסתברות של השני.", do=show("i-1")),
    P("ומכאן המסקנה: אם לשניהם הסתברות חיובית, הם לא יכולים להיות גם זרים וגם בלתי תלויים.", do=show("i-2")),
    P("כי לזרים החיתוך אפס, אבל המכפלה של שתי הסתברויות חיוביות אינה אפס.", hold=0.4),
], stage=f'<div class="ev-stack">{ROWS}</div>',
   panel=st.card("i-1", "ex", "בלתי תלויים: $P(A/B)=P(A)$")
         + st.card("i-2", "rule", "🔑 הסתברויות חיוביות: זרים $\\Rightarrow$ תלויים"))
idea.phrases[0].do = []

ex1 = Scene("ex1", "דוגמה: קובייה אחת", [
    P("דוגמה עם קובייה אחת. $A$: יצא אחת או שתיים. $B$: יצא מספר אי-זוגי.",
      say="דוגמה עם קובייה אחת. אֵיי: יצא אחת או שתיים. בִּי: יצא מספר אי זוגי.", do=show("a-0")),
    P("ההסתברות של $A$ היא שליש, ושל $B$ חצי.", say="ההסתברות של אֵיי היא שליש, ושל בִּי חצי."),
    P("החיתוך: רק התוצאה אחת. ההסתברות שלו שישית.", do=show("v1-AB", "a-1")),
    P("והמכפלה: שליש כפול חצי, גם שישית. שוות! ולכן $A$ ו-$B$ **בלתי תלויים**, אפילו בהטלה אחת.",
      say="והמכפלה: שליש כפול חצי, גם שישית. שוות! ולכן אֵיי ובִּי בלתי תלויים, אפילו בהטלה אחת.", do=show("a-2")),
    P("בדיקה בעזרת התניה: אם ידוע שיצא אי-זוגי, נשארו אחת, שלוש וחמש. רק אחת מהן ב-$A$: שליש. כמו קודם.",
      say="בדיקה בעזרת התניה: אם ידוע שיצא אי זוגי, נשארו אחת, שלוש וחמש. רק אחת מהן באֵיי: שליש. כמו קודם.",
      do=show("a-3"), hold=0.3),
    P("והם לא זרים: התוצאה אחת שייכת לשניהם. אי-תלות דווקא **מחייבת** חיתוך.", hold=0.2),
    P("ועוד דבר: גם $A$ והמשלים של $B$ בלתי תלויים. החיתוך הוא רק שתיים, שישית, שוב שליש כפול חצי.",
      say="ועוד דבר: גם אֵיי והמשלים של בִּי בלתי תלויים. החיתוך הוא רק שתיים, שישית, שוב שליש כפול חצי.",
      do=show("a-4"), hold=0.4),
], stage=f'<div class="ev-stack">{V.svg()}</div>',
   panel=st.card("a-0", "plain", "$A=\\{1,2\\},\\ B=\\{1,3,5\\}$")
         + st.card("a-1", "ex", "$P(A\\cap B)=P(\\{1\\})=\\frac16$")
         + st.card("a-2", "rule", "🔑 $P(A)P(B)=\\frac13\\cdot\\frac12=\\frac16$: בלתי תלויים")
         + st.card("a-3", "ex", "$P(A/B)=\\frac13=P(A)$")
         + st.card("a-4", "ex", "$P(A\\cap\\overline{B})=\\frac16=P(A)P(\\overline{B})$"))

ex2 = Scene("ex2", "זרים הם תלויים", [
    P("ועכשיו $C$: יצא חמש או שש. ההסתברות שליש.", say="ועכשיו סִי: יצא חמש או שש. ההסתברות שליש.", do=show("b-0")),
    P("$A$ ו-$C$ זרים: אין להם תוצאה משותפת, החיתוך אפס.", say="אֵיי וסִי זרים: אין להם תוצאה משותפת, החיתוך אפס.",
      do=show("b-1")),
    P("והמכפלה שליש כפול שליש, תשיעית. אפס שונה מתשיעית, ולכן הם **תלויים**.", do=show("b-2")),
    P("ובמילים: אם ידוע שיצא אחת או שתיים, ההסתברות לחמש או שש קפצה משליש לאפס. המידע שינה הכול.",
      do=show("b-3"), hold=0.3),
    P("והמלכודת: הם זרים, ולכן בלתי תלויים. זה בדיוק הפוך. זרים אומר שאחד **מונע** את השני.",
      do=show("b-t"), hold=0.4),
], stage=f'<div class="ev-stack">{V2.svg()}</div>',
   panel=st.card("b-0", "plain", "$C=\\{5,6\\}$, $\\;P(C)=\\frac13$")
         + st.card("b-1", "ex", "$P(A\\cap C)=0$")
         + st.card("b-2", "rule", "🔑 $P(A)P(C)=\\frac19\\ne0$: תלויים")
         + st.card("b-3", "ex", "$P(C/A)=0\\ne\\frac13$")
         + st.card("b-t", "trap", "⚠️ זרים $\\ne$ בלתי תלויים"))

exam = Scene("exam", "בסגנון מבחן", [
    P("ועכשיו שאלה בסגנון מבחן. בוחרים מספר דו-ספרתי באקראי, מעשר עד תשעים ותשע.", do=show("x-stem")),
    P("$A_3$: המספר מתחלק בשלוש. $A_6$: מתחלק בשש. האם הם בלתי תלויים?",
      say="אֵיי שלוש: המספר מתחלק בשלוש. אֵיי שש: מתחלק בשש. האם הם בלתי תלויים?"),
    P("ספירת מכפלות: שלושים מתחלקים בשלוש, וחמישה עשר מתחלקים בשש. מתוך תשעים: שליש, ושישית.",
      do=show("x-1")),
    P("עכשיו החיתוך. כל מספר שמתחלק בשש מתחלק גם בשלוש. כלומר $A_6$ מוכל ב-$A_3$.",
      say="עכשיו החיתוך. כל מספר שמתחלק בשש מתחלק גם בשלוש. כלומר אֵיי שש מוכל באֵיי שלוש.", do=show("x-2")),
    P("ולכן החיתוך הוא $A_6$ עצמו, וההסתברות שלו שישית.",
      say="ולכן החיתוך הוא אֵיי שש עצמו, וההסתברות שלו שישית.", do=show("x-3")),
    P("המכפלה: שליש כפול שישית, כלומר אחת חלקי שמונה עשרה. לא שווה. הם **תלויים**.", do=show("x-4"), hold=0.3),
    P("ואפשר גם בלי מספרים: אילו היו בלתי תלויים, היינו מקבלים שההסתברות של $A_3$ היא אחת. והיא שליש.",
      say="ואפשר גם בלי מספרים: אילו היו בלתי תלויים, היינו מקבלים שההסתברות של אֵיי שלוש היא אחת. והיא שליש.",
      do=show("x-5")),
    P("במילים: אם ידוע שהמספר מתחלק בשש, הוא בוודאות מתחלק בשלוש. המידע שינה את ההסתברות משליש לאחת.", hold=0.2),
    P("המלכודת: לחשוב שהם בלתי תלויים כי הם לא זרים. חיתוך לא ריק לבדו לא מוכיח כלום. משווים למכפלה.",
      do=show("x-t"), hold=0.5),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="x-1" class="h">$P(A_3)=\frac{30}{90}=\frac13,\quad P(A_6)=\frac{15}{90}=\frac16$</div>'
         r'<div id="x-2" class="h">$A_6\subseteq A_3\ \Rightarrow\ A_3\cap A_6=A_6$</div>'
         r'<div id="x-3" class="h">$P(A_3\cap A_6)=\frac16$</div>'
         r'<div id="x-4" class="h">$P(A_3)P(A_6)=\frac{1}{18}\ne\frac16$</div></div></div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-5", "rule", r"🔑 $P(A_6)=P(A_3)P(A_6)\Rightarrow P(A_3)=1$, סתירה")
         + st.card("x-t", "trap", "⚠️ לא זרים לא אומר בלתי תלויים"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: זרים, החיתוך אפס. בלתי תלויים, החיתוך שווה למכפלה.", do=show("r-1")),
    P("עם הסתברויות חיוביות, זרים הם תמיד תלויים, ובלתי תלויים הם אף פעם לא זרים.", do=show("r-2")),
    P("גם מאורע שמוכל במאורע אחר תלוי בו, ובתנאי שלקטן הסתברות חיובית, אלא אם הגדול הוא ודאי.", do=show("r-3")),
    P("ותמיד בודקים במספרים: מחשבים את החיתוך ומשווים למכפלה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="ev-stack">{ROWS.replace("id=\"cmp\"", "id=\"cmp2\"")}</div>',
   panel=st.card("r-1", "rule", "🔑 זרים: $0$. בלתי תלויים: $P(A)P(B)$")
         + st.card("r-2", "rule", "🔑 זרים $\\Rightarrow$ תלויים")
         + st.card("r-3", "rule", "🔑 $B\\subseteq A$, $P(B)>0$, $P(A)<1$ $\\Rightarrow$ תלויים")
         + st.card("r-4", "trap", "⚠️ משווים חיתוך למכפלה, לא מנחשים"))

VIDEO = Video("E08", "events", "בלתי תלויים מול זרים", [title, idea, ex1, ex2, exam, recap],
              bank={})
