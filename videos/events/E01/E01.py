# -*- coding: utf-8 -*-
"""E01 · אלגברה של מאורעות — video script (build: tools/video/vid.py E01).

Source: courses/events/C01.js (lesson + goal: translate "at least one / none / exactly one" into events, count them,
De Morgan). Exam anchor: 25S-A-Q2a (P(A∖B)=p, P(A∩B)=q, P(A/B)=s; find P(A)), an open question (bank key None) that
no guided quiz uses.
Avoided on purpose: the die with A = "even", B = "greater than 3" (every C01 quiz question and the lesson example) and
its numbers {2,4,6}, {4,5,6}; 25A-A-Q2d (the C10 boss: A8 = A2 ∩ A4?).
Worked example: a number drawn from 1..12, A = "divisible by 2", B = "divisible by 3"; every region, size and
probability below is computed from the sets and checked by enumeration + Monte Carlo (w_events.Space).
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- numbers (verified)
OM = set(range(1, 13))
A = {x for x in OM if x % 2 == 0}
B = {x for x in OM if x % 3 == 0}
assert A == {2, 4, 6, 8, 10, 12} and B == {3, 6, 9, 12}
ONLY_A, BOTH, ONLY_B, NONE = A - B, A & B, B - A, OM - (A | B)
assert (ONLY_A, BOTH, ONLY_B, NONE) == ({2, 4, 8, 10}, {6, 12}, {3, 9}, {1, 5, 7, 11})
S = w.Space.uniform([{"x": x} for x in sorted(OM)])
inA, inB = (lambda o: o["x"] % 2 == 0), (lambda o: o["x"] % 3 == 0)
P_UNION = S.both(lambda o: inA(o) or inB(o))
P_BOTH = S.both(lambda o: inA(o) and inB(o))
P_ONE = S.both(lambda o: inA(o) != inB(o))
P_NONE = S.both(lambda o: not inA(o) and not inB(o))
P_NOTBOTH = S.both(lambda o: not (inA(o) and inB(o)))
assert len(A | B) == 8 and P_UNION == Fr(2, 3)
assert P_BOTH == Fr(1, 6) and P_ONE == Fr(1, 2) and P_NONE == Fr(1, 3) and P_NOTBOTH == Fr(5, 6)
assert P_BOTH + P_ONE + P_NONE == 1                                      # the three pieces cover Ω
assert len(A) + len(B) == 10 != len(A | B)                               # the trap: 6 and 12 counted twice
# De Morgan on this example, both laws
assert OM - (A | B) == (OM - A) & (OM - B) == {1, 5, 7, 11}
assert OM - (A & B) == (OM - A) | (OM - B) and len(OM - (A & B)) == 10
assert (OM - A) | (OM - B) != (OM - A) & (OM - B)                        # "not both" is NOT "none"

# exam 25S-A-Q2a: A splits into A∖B and A∩B, disjoint, so P(A) = p + q
Q = BANK["25S-A-Q2a"]
assert Q["contextId"] == "25S-A-c2" and "P(A)=P(A\\setminusB)+P(A\\capB)=p+q" in Q["solution"].replace(" ", "")
for ab, a_only in [(Fr(1, 5), Fr(3, 10)), (Fr(1, 10), Fr(1, 2)), (Fr(0), Fr(2, 5))]:     # random 4-cell tables
    cells = w.Space([({"A": 1, "B": 1}, ab), ({"A": 1, "B": 0}, a_only),
                     ({"A": 0, "B": 1}, Fr(1, 5)), ({"A": 0, "B": 0}, 1 - ab - a_only - Fr(1, 5))])
    assert cells.P(lambda o: o["A"] == 1) == a_only + ab                # P(A) = P(A∖B) + P(A∩B), every table

# ---------------------------------------------------------------- figures
v0 = w.Venn("v0")
v0.fill("un", ["a", "ab", "b"], "ev")
v0.fill("in", ["ab"], "ev")
v0.fill("co", ["b", "o"], "alt")
v0.fill("df", ["a"], "warn")

v1 = w.Venn("v1")
v1.fill("un", ["a", "ab", "b"], "ev")
v1.fill("in", ["ab"], "ev")
v1.fill("one", ["a", "b"], "warn")
v1.fill("none", ["o"], "alt")
v1.fill("nab", ["a", "b", "o"], "bad")
v1.text("ta", "a", ["2  4", "8  10"])
v1.text("tab", "ab", ["6", "12"])
v1.text("tb", "b", ["3", "9"])
v1.text("to", (590, 400), "1  5  7  11")

# the De Morgan scene keeps the same numbers on screen, in a second diagram with its own ids
v2 = w.Venn("v2")
v2.fill("none", ["o"], "alt")
v2.fill("nab", ["a", "b", "o"], "bad")
v2.text("ta", "a", ["2  4", "8  10"], shown=True)
v2.text("tab", "ab", ["6", "12"], shown=True)
v2.text("tb", "b", ["3", "9"], shown=True)
v2.text("to", (590, 400), "1  5  7  11", shown=True)

vx = w.Venn("vx")
vx.fill("a", ["a"], "warn")
vx.fill("ab", ["ab"], "ev")
vx.text("p", "a", "p", cls="big it")
vx.text("q", "ab", "q", cls="big it")

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>$A$ ו-$B$ מאורעות לא ריקים. נתון '
        '<span class="nobr">$P(A\\setminus B)=p$</span>, <span class="nobr">$P(A\\cap B)=q$</span> '
        'ו-<span class="nobr">$P(A/B)=s$</span>. חשבו את $P(A)$.</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לתרגם משפטים במילים למאורעות."),
    P("לפחות אחד, אף אחד, בדיוק אחד, ושניהם: נראה איך כל אחד מהם נראה בציור, ואיך סופרים אותו."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">E01 · מאורעות</div><h1>אלגברה של מאורעות</h1>'
         '<p>איחוד, חיתוך, משלים והפרש, וחוקי דה מורגן: לתרגם "לפחות אחד", "אף אחד" ו"בדיוק אחד" למאורע ולחשב אותו.</p>',
   layout="title")

idea = Scene("idea", "הפעולות", [
    P("מרחב המדגם, $\\Omega$, הוא אוסף כל התוצאות האפשריות של הניסוי.", do=show("i-1")),
    P("מאורע הוא תת-קבוצה של $\\Omega$: אוסף של תוצאות. בציור, עיגול בתוך המלבן."),
    P("כשכל התוצאות שוות בסבירות, ההסתברות היא ספירה: גודל המאורע, חלקי גודל אומגה.", do=show("i-3")),
    P("$A$ או $B$, כלומר לפחות אחד מהם: זה האיחוד. כל התוצאות שבאחד מהם לפחות.", do=show("v0-un", "i-4")),
    P("$A$ וגם $B$, כלומר שניהם: זה החיתוך. רק מה שבשני העיגולים יחד.", do=hide("v0-un") + show("v0-in", "i-5")),
    P("לא $A$: זה המשלים. כל מה שבאומגה ומחוץ ל-$A$.", do=hide("v0-in") + show("v0-co", "i-6")),
    P("ו-$A$ אבל לא $B$: זה ההפרש. החלק של $A$ שמחוץ ל-$B$.",
      say="ואֵיי אבל לא בִּי: זה ההפרש. החלק של אֵיי שמחוץ לבִּי.", do=hide("v0-co") + show("v0-df", "i-7")),
    P("ההפרש הוא בעצם חיתוך: $A$ וגם המשלים של $B$.", hold=0.3),
    P("ועוד מושג אחד: מאורעות **זרים** הם מאורעות בלי אף תוצאה משותפת. החיתוך שלהם ריק.",
      do=hide("v0-df") + show("i-8"), hold=0.4),
], stage=f'<div class="ev-stack">{v0.svg()}</div>',
   panel=st.card("i-1", "plain", "$\\Omega$: כל התוצאות. מאורע: תת-קבוצה של $\\Omega$")
         + st.card("i-3", "rule", "🔑 $P(A)=\\dfrac{|A|}{|\\Omega|}$")
         + st.card("i-4", "ex", "לפחות אחד: $A\\cup B$")
         + st.card("i-5", "ex", "שניהם: $A\\cap B$")
         + st.card("i-6", "ex", "לא $A$: $\\overline{A}$")
         + st.card("i-7", "ex", "$A$ אבל לא $B$: $A\\setminus B=A\\cap\\overline{B}$")
         + st.card("i-8", "plain", "זרים: $A\\cap B=\\varnothing$"))

ex = Scene("ex", "דוגמה: מספר מ-1 עד 12", [
    P("דוגמה. בוחרים באקראי מספר שלם מאחת עד שתים עשרה. אומגה כוללת שתים עשרה תוצאות.", do=show("e-1")),
    P("$A$: המספר מתחלק בשתיים. $B$: המספר מתחלק בשלוש.", do=show("e-2")),
    P("נפזר את המספרים בציור. שש ושתים עשרה מתחלקים גם בשתיים וגם בשלוש: הם בחיתוך.", do=show("v1-tab")),
    P("שתיים, ארבע, שמונה ועשר: רק בשתיים. שלוש ותשע: רק בשלוש.", do=show("v1-ta", "v1-tb")),
    P("ואחת, חמש, שבע ואחת עשרה לא שייכים לאף אחד מהם: הם מחוץ לשני העיגולים.", do=show("v1-to"), hold=0.3),
    P("**לפחות אחד** הוא האיחוד: ארבעה, ועוד שניים, ועוד שניים. שמונה מספרים.", do=show("v1-un", "e-3")),
    P("ההסתברות: שמונה חלקי שתים עשרה, כלומר שני שלישים.", hold=0.2),
    P("**שניהם** הוא החיתוך: רק שש ושתים עשרה. ההסתברות שתיים חלקי שתים עשרה, שישית.",
      do=hide("v1-un") + show("v1-in", "e-4")),
    P("**בדיוק אחד**: האיחוד בלי החיתוך. ארבעה ועוד שניים, שישה מספרים: חצי.",
      do=hide("v1-in") + show("v1-one", "e-5")),
    P("ו**אף אחד**: מה שמחוץ לשני העיגולים. ארבעה מספרים, כלומר שליש.", do=hide("v1-one") + show("v1-none", "e-6")),
    P("שימו לב: שניהם, בדיוק אחד ואף אחד מכסים יחד את כל אומגה. שישית ועוד חצי ועוד שליש זה אחת.", hold=0.3),
    P("והמלכודת: גודל האיחוד אינו שש ועוד ארבע. במקרה הזה זה היה עשר, אבל באיחוד יש רק שמונה.",
      do=hide("v1-none") + show("e-t")),
    P("שש ושתים עשרה נספרו פעמיים, פעם בכל עיגול.", hold=0.4),
], stage=f'<div class="ev-stack">{v1.svg()}</div>',
   panel=st.card("e-1", "plain", "$\\Omega=\\{1,2,\\dots,12\\}$")
         + st.card("e-2", "plain", "$A$: מתחלק ב-2. $\\;B$: מתחלק ב-3")
         + st.card("e-3", "ex", "לפחות אחד: $P(A\\cup B)=\\frac{8}{12}=\\frac23$")
         + st.card("e-4", "ex", "שניהם: $P(A\\cap B)=\\frac{2}{12}=\\frac16$")
         + st.card("e-5", "ex", "בדיוק אחד: $\\frac{6}{12}=\\frac12$")
         + st.card("e-6", "ex", "אף אחד: $\\frac{4}{12}=\\frac13$")
         + st.card("e-t", "trap", "⚠️ $|A\\cup B|=8$, לא $6+4=10$"))

dm = Scene("dm", "חוקי דה מורגן", [
    P("עכשיו נבין את **אף אחד** בעזרת משלימים.", do=show("v2-none")),
    P("אף אחד, זה המשלים של לפחות אחד: המשלים של האיחוד.", do=show("d-1")),
    P("ובמילים אחרות: גם $A$ לא קרה, וגם $B$ לא קרה. חיתוך של שני המשלימים.", do=show("d-2")),
    P("זה חוק דה מורגן הראשון: המשלים של איחוד הוא חיתוך המשלימים.", do=show("d-3"), hold=0.3),
    P("בדוגמה: המשלים של $A$ הוא המספרים האי-זוגיים, והמשלים של $B$ הוא מה שלא מתחלק בשלוש.",
      say="בדוגמה: המשלים של אֵיי הוא המספרים האי זוגיים, והמשלים של בִּי הוא מה שלא מתחלק בשלוש."),
    P("המשותף להם: אחת, חמש, שבע ואחת עשרה. בדיוק הקבוצה שמצאנו קודם.", hold=0.3),
    P("החוק השני הפוך: המשלים של חיתוך הוא איחוד המשלימים. במילים: **לא שניהם**.",
      do=hide("v2-none") + show("v2-nab", "d-4")),
    P("לא שניהם, פירושו שלפחות אחד מהם לא קרה. כל המספרים חוץ משש ושתים עשרה: עשרה מתוך שתים עשרה.",
      do=show("d-5")),
    P("וזו המלכודת: **אף אחד** ו**לא שניהם** נשמעים דומים, אבל אלה שני מאורעות שונים: ארבעה מספרים מול עשרה.",
      do=show("d-t")),
    P("המשלים הופך **או** ל**וגם**, ו**וגם** ל**או**.", hold=0.4),
], stage=f'<div class="ev-stack">{v2.svg()}</div>',
   panel=(st.card("d-1", "plain", "אף אחד $=\\overline{A\\cup B}$")
            + st.card("d-2", "plain", "$=\\overline{A}\\cap\\overline{B}$: גם לא $A$ וגם לא $B$")
            + st.card("d-3", "rule", "🔑 $\\overline{A\\cup B}=\\overline{A}\\cap\\overline{B}$")
            + st.card("d-4", "rule", "🔑 $\\overline{A\\cap B}=\\overline{A}\\cup\\overline{B}$")
            + st.card("d-5", "ex", "לא שניהם: $\\frac{10}{12}=\\frac56$")
            + st.card("d-t", "trap", "⚠️ אף אחד $\\ne$ לא שניהם")))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. $A$ ו-$B$ מאורעות לא ריקים, ונתונות שלוש הסתברויות.", do=show("x-stem")),
    P("ההסתברות של $A$ פחות $B$ היא $p$, וההסתברות של החיתוך היא $q$.",
      say="ההסתברות של אֵיי פחות בִּי היא פִּי, וההסתברות של החיתוך היא קְיוּ."),
    P("והנתון השלישי הוא הסתברות מותנית, $s$. נגיע אליה בהמשך הקורס. השאלה: כמה זה $P(A)$?",
      say="והנתון השלישי הוא הסתברות מותנית, אֶס. נגיע אליה בהמשך הקורס. השאלה: כמה זה פֵּה של אֵיי?"),
    P("נצייר. $A$ פחות $B$ הוא החלק של העיגול $A$ שמחוץ ל-$B$. ההסתברות שלו $p$.",
      say="נצייר. אֵיי פחות בִּי הוא החלק של העיגול אֵיי שמחוץ לבִּי. ההסתברות שלו פִּי.", do=show("vx-a", "vx-p")),
    P("והחיתוך הוא החלק של $A$ שבתוך $B$. ההסתברות שלו $q$.",
      say="והחיתוך הוא החלק של אֵיי שבתוך בִּי. ההסתברות שלו קְיוּ.", do=show("vx-ab", "vx-q")),
    P("שני החלקים האלה זרים: אין תוצאה שגם מחוץ ל-$B$ וגם בתוך $B$.",
      say="שני החלקים האלה זרים: אין תוצאה שגם מחוץ לבִּי וגם בתוך בִּי.", do=show("x-1")),
    P("ויחד הם בדיוק $A$. ולכן ההסתברויות שלהם מתחברות.", do=show("x-2")),
    P("$P(A)$ שווה $p$ ועוד $q$.", say="פֵּה של אֵיי שווה פִּי ועוד קְיוּ.", do=show("x-3"), hold=0.3),
    P("המלכודת: לחשוב ש-$p$ הוא כבר $P(A)$. ההפרש הוא רק החלק של $A$ שמחוץ ל-$B$.",
      say="המלכודת: לחשוב שפִּי הוא כבר פֵּה של אֵיי. ההפרש הוא רק החלק של אֵיי שמחוץ לבִּי.", do=show("x-t")),
    P("ולמה מותר לחבר? רק כי החלקים זרים. מאורעות שנחתכים אי אפשר פשוט לחבר, וזה הנושא של הסרטון הבא.", hold=0.5),
], stage=f'<div class="ev-stack">{vx.svg()}</div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-1", "plain", "$(A\\setminus B)\\cap(A\\cap B)=\\varnothing$")
         + st.card("x-2", "plain", "$(A\\setminus B)\\cup(A\\cap B)=A$")
         + st.card("x-3", "rule", "🔑 $P(A)=p+q$")
         + st.card("x-t", "trap", "⚠️ $P(A\\setminus B)=p$ הוא לא $P(A)$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לפחות אחד הוא איחוד, ושניהם הוא חיתוך.", do=show("r-1")),
    P("בדיוק אחד הוא האיחוד בלי החיתוך, ואף אחד הוא המשלים של האיחוד.", do=show("r-2")),
    P("דה מורגן: המשלים הופך איחוד לחיתוך, וחיתוך לאיחוד.", do=show("r-3")),
    P("וכשמחלקים מאורע לחלקים זרים, ההסתברויות מתחברות. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$\\overline{A\\cup B}=\\overline{A}\\cap\\overline{B}$</div>'
         '<div class="ev-big">$\\overline{A\\cap B}=\\overline{A}\\cup\\overline{B}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 לפחות אחד: $A\\cup B$. שניהם: $A\\cap B$")
         + st.card("r-2", "rule", "🔑 בדיוק אחד: $(A\\setminus B)\\cup(B\\setminus A)$")
         + st.card("r-3", "rule", "🔑 אף אחד: $\\overline{A}\\cap\\overline{B}$")
         + st.card("r-4", "trap", "⚠️ מחברים הסתברויות רק של חלקים זרים"))

VIDEO = Video("E01", "events", "אלגברה של מאורעות", [title, idea, ex, dm, exam, recap],
              bank={"25S-A-Q2a": None})
