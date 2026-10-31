# -*- coding: utf-8 -*-
"""E09 · כדים: עם החזרה, בלי החזרה ובהינתן משיכה קודמת — video script (build: tools/video/vid.py E09).

Source: courses/events/C09.js (lesson + goal: urns with / without replacement, conditioning on an earlier draw, and
the symmetry P(R_2) = D/N when the earlier draw is unknown). Exam anchor: 24B-C-Q2c (digits 0..9, two drawn without
replacement; given the first is divisible by 3, P(the second is even)), an open question (bank key None) that no
guided quiz uses.
Avoided on purpose: every C09 quiz case (3 red / 5 black: 2/7 and 3/28; 4 red / 6 black: the third ball, and the third
given the second) and the bank items 24B-B-Q2c / 24B-B-Q2d (C09 quiz / C10 boss) and their twin 24B-C-Q2d: the video
never computes a third draw, and never conditions a later draw on a middle one.
Worked example: 2 red and 3 black balls (both red with / without replacement, and P(R_2) by total probability).
Every value is computed on the checker's urn space (w_events.Space.urn) with Monte Carlo.
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- example: 2 red, 3 black
U = w.Space.urn(counts={"r": 2, "k": 3}, draws=2, replace=False)
UR = w.Space.urn(counts={"r": 2, "k": 3}, draws=2, replace=True)
assert U.P(lambda o: o["r_2"], given=lambda o: o["r_1"]) == Fr(1, 4)         # (D-1)/(N-1)
assert U.P(lambda o: o["r_2"], given=lambda o: o["k_1"]) == Fr(2, 4)         # D/(N-1)
assert UR.P(lambda o: o["r_2"], given=lambda o: o["r_1"]) == Fr(2, 5)        # with replacement: unchanged
RR = U.both(lambda o: o["r"] == 2)
RRr = UR.both(lambda o: o["r"] == 2)
assert RR == Fr(2, 5) * Fr(1, 4) == Fr(1, 10) and RRr == Fr(4, 25) and RR != RRr
R2 = U.both(lambda o: o["r_2"])
assert R2 == Fr(2, 5) * Fr(1, 4) + Fr(3, 5) * Fr(2, 4) == Fr(8, 20) == Fr(2, 5) == U.P(lambda o: o["r_1"])
assert len(U.out) == 20 and U.count(lambda o: o["r_2"]) == 8                  # 20 ordered pairs, 8 with a red second

TU = w.Tree("tu", [
    ("r", "אדום", (Fr(2, 5), "2/5"), [("r", "אדום", (Fr(1, 4), "1/4"), []), ("k", "שחור", (Fr(3, 4), "3/4"), [])]),
    ("k", "שחור", (Fr(3, 5), "3/5"), [("r", "אדום", (Fr(2, 4), "2/4"), []), ("k", "שחור", (Fr(2, 4), "2/4"), [])]),
], w=760, h=480, xs=[30, 300, 580], prod_text={"rr": "= 2/20", "kr": "= 6/20"})
URN = w.Urn("un", [("", "r"), ("", "r"), ("", "k"), ("", "k"), ("", "k")], per_row=5, d=86)

# ---------------------------------------------------------------- exam 24B-C-Q2c
Q = BANK["24B-C-Q2c"]
assert Q["contextId"] == "24B-C-c2" and "=\\frac12" in Q["solution"].replace(" ", "")
D = w.Space.urn(values=list(range(10)), draws=2, replace=False)
A1 = lambda o: o["v1"] % 3 == 0
E2 = lambda o: o["v2"] % 2 == 0
ANS = D.both(E2, given=A1)
assert ANS == Fr(1, 2) and D.count(A1) == 36 and D.count(lambda o: A1(o) and E2(o)) == 18
assert D.P(lambda o: o["v1"] in (0, 6), given=A1) == Fr(1, 2)
assert D.P(E2, given=lambda o: o["v1"] in (0, 6)) == Fr(4, 9) and D.P(E2, given=lambda o: o["v1"] in (3, 9)) == Fr(5, 9)
assert Fr(1, 2) * Fr(4, 9) + Fr(1, 2) * Fr(5, 9) == ANS
assert 4 + 4 + 5 + 5 == 18 and Fr(18, 90) / Fr(36, 90) == ANS                   # the official count
assert D.P(E2) == Fr(1, 2) == ANS                                              # the condition happens not to change it

DG = w.Urn("dg", [(str(d), "t" if d % 2 == 0 else "g") for d in range(10)], per_row=5, d=74)
STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>באוסף הספרות $0,1,\\dots,9$. מוציאים שתי ספרות '
        '<b>ללא החזרה</b>. <b>אם ידוע</b> שהראשונה מתחלקת ב-3, מה ההסתברות שהשנייה זוגית?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נשלוף כדורים מכד: עם החזרה, בלי החזרה, וכשידוע מה יצא קודם."),
    P("ונגלה עובדה מפתיעה על הכדור השני, כשלא יודעים מה היה הראשון."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">E09 · כדים</div><h1>כדים: עם ובלי החזרה</h1>'
         '<p>לחשב הסתברויות בכד עם ובלי החזרה, גם בהינתן משיכה קודמת.</p>',
   layout="title")

idea = Scene("idea", "שני סוגי הוצאה", [
    P("בכד $N$ כדורים, ומתוכם $D$ אדומים.", say="בכד אֶן כדורים, ומתוכם דִּי אדומים.", do=show("i-0")),
    P("**עם החזרה**: אחרי כל משיכה מחזירים את הכדור. הכד תמיד אותו כד, ולכן כל משיכה אדומה בהסתברות $D$ חלקי $N$.",
      say="עם החזרה: אחרי כל משיכה מחזירים את הכדור. הכד תמיד אותו כד, ולכן כל משיכה אדומה בהסתברות דִּי חלקי אֶן.",
      do=show("i-1")),
    P("והמשיכות בלתי תלויות זו בזו.", hold=0.2),
    P("**בלי החזרה**: כל משיכה משנה את הכד. אם הראשון אדום, נשארו $N$ פחות אחד כדורים, ו-$D$ פחות אחד אדומים.",
      say="בלי החזרה: כל משיכה משנה את הכד. אם הראשון אדום, נשארו אֶן פחות אחד כדורים, ודִּי פחות אחד אדומים.",
      do=show("i-2")),
    P("ואם הראשון שחור, כל האדומים עוד בפנים, מתוך $N$ פחות אחד.",
      say="ואם הראשון שחור, כל האדומים עוד בפנים, מתוך אֶן פחות אחד.", do=show("i-3"), hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="i-1" class="h">$P(R_k)=\frac{D}{N}$</div>'
         r'<div id="i-2" class="h">$P(R_2/R_1)=\dfrac{D-1}{N-1}$</div>'
         r'<div id="i-3" class="h">$P(R_2/B_1)=\dfrac{D}{N-1}$</div></div></div>',
   panel=st.card("i-0", "plain", "$D$ אדומים מתוך $N$. $R_i$: הכדור ה-$i$ אדום, $B_i$: שחור"))

ex1 = Scene("ex1", "דוגמה: שני אדומים", [
    P("דוגמה. בכד חמישה כדורים: שניים אדומים ושלושה שחורים."),
    P("שני כדורים בלי החזרה. מה ההסתברות ששניהם אדומים?", hold=0.1),
    P("הראשון אדום בשתי חמישיות. אחריו נשארו ארבעה כדורים, ורק אדום אחד: רבע.", do=show("un-x0", "a-1")),
    P("שתי חמישיות כפול רבע: עשירית.", do=show("a-2"), hold=0.3),
    P("ועם החזרה? הכד חוזר לקדמותו: שתי חמישיות כפול שתי חמישיות, ארבע חלקי עשרים וחמש.",
      say="ועם החזרה? הכד חוזר לקדמותו: שתי חמישיות כפול שתי חמישיות, ארבע חלקי עשרים וחמש.", do=hide("un-x0") + show("a-3")),
    P("שתי תשובות שונות. כשמדובר בכמה כדורים **יחד**, החזרה משנה הכול.", hold=0.4),
], stage=f'<div class="ev-stack">{URN.svg()}</div>',
   panel=st.card("a-1", "plain", "$P(R_1)=\\frac25,\\quad P(R_2/R_1)=\\frac14$")
         + st.card("a-2", "rule", "🔑 בלי החזרה: $\\frac25\\cdot\\frac14=\\frac{1}{10}$")
         + st.card("a-3", "ex", "עם החזרה: $\\frac25\\cdot\\frac25=\\frac{4}{25}$"))

sym = Scene("sym", "הכדור השני", [
    P("ועכשיו שאלה מפתיעה: מה ההסתברות שהכדור **השני** אדום, כשלא יודעים מה יצא ראשון?"),
    P("מפצלים לפי הכדור הראשון. אדום ואז אדום: שתי חמישיות כפול רבע, שתיים חלקי עשרים.",
      do=show("tu-b-r", "tu-b-k", "tu-b-rr", "tu-b-rk", *TU.path_hl("rr"), "tu-p-rr")),
    P("שחור ואז אדום: שלוש חמישיות כפול שניים מתוך ארבעה, שש חלקי עשרים.",
      do=show("tu-b-kr", "tu-b-kk", *TU.path_hl("kr"), "tu-p-kr")),
    P("ביחד: שמונה חלקי עשרים, כלומר שתי חמישיות. בדיוק כמו הכדור הראשון!", do=show("s-1"), hold=0.3),
    P("למה? כי כל אחד מחמשת הכדורים סביר באותה מידה להיות זה שיוצא שני. ושניים מהם אדומים.", do=show("s-2")),
    P("אבל זה נכון רק כשלא יודעים מה יצא ראשון. ברגע שיודעים, חוזרים לכד שהשתנה.", do=show("s-t"), hold=0.4),
], stage=f'<div class="ev-stack">{TU.svg()}</div>',
   panel=st.card("s-1", "rule", "🔑 $P(R_2)=\\frac{2}{20}+\\frac{6}{20}=\\frac25=\\frac{D}{N}$")
         + st.card("s-2", "ex", "כל כדור סביר באותה מידה להיות שני")
         + st.card("s-t", "trap", "⚠️ רק כשהמשיכה הקודמת <b>לא ידועה</b>"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. באוסף עשר ספרות, מאפס עד תשע. מוציאים שתיים בלי החזרה.", do=show("x-stem")),
    P("ידוע שהספרה הראשונה מתחלקת בשלוש. מה ההסתברות שהשנייה זוגית?", hold=0.1),
    P("הראשונה היא אחת מארבע: אפס, שלוש, שש או תשע. כל אחת באותה סבירות.", do=show("dg-h0", "dg-h3", "dg-h6", "dg-h9")),
    P("אבל כאן יש פרט חשוב: אפס ושש זוגיות, ושלוש ותשע לא. וזה משנה את מה שנשאר באוסף.", do=show("x-1")),
    P("אם הראשונה אפס או שש, בהסתברות חצי, היא לקחה ספרה זוגית: נשארו ארבע זוגיות מתוך תשע.",
      do=show("dg-x0", "x-2")),
    P("ואם הראשונה שלוש או תשע, גם בהסתברות חצי, כל חמש הזוגיות עוד באוסף: חמש מתוך תשע.",
      do=hide("dg-x0") + show("dg-x3", "x-3")),
    P("מחברים לפי ההסתברות השלמה: חצי כפול ארבע תשיעיות, ועוד חצי כפול חמש תשיעיות. יוצא חצי.",
      do=hide("dg-x3") + show("x-4"), hold=0.3),
    P("בדיקה בספירה: שלושים ושישה זוגות שבהם הראשונה מתחלקת בשלוש. בשמונה עשר מהם השנייה זוגית. חצי.",
      do=show("x-5")),
    P("המלכודת: לענות ארבע תשיעיות, כאילו הספרה הראשונה תמיד זוגית. או חמש תשיעיות, כאילו אף פעם.", do=show("x-t")),
    P("כשהמידע על המשיכה הקודמת לא קובע אם היא הוציאה ספרה מתאימה, מפצלים לפי המקרים.", hold=0.5),
], stage=f'<div class="ev-stack">{DG.svg()}<div class="ev-eqs">'
         r'<div id="x-2" class="h">$\{0,6\}:\ \ P=\frac12,\quad \frac49$</div>'
         r'<div id="x-3" class="h">$\{3,9\}:\ \ P=\frac12,\quad \frac59$</div>'
         r'<div id="x-4" class="h">$\frac12\cdot\frac49+\frac12\cdot\frac59=\frac12$</div></div></div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-1", "plain", "מתחלקות ב-3: $0,3,6,9$. מהן זוגיות: $0,6$")
         + st.card("x-5", "rule", "🔑 $P(B_2/A_1)=\\frac{18}{36}=\\frac12$")
         + st.card("x-t", "trap", "⚠️ לא $\\frac49$ ולא $\\frac59$: מפצלים"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: עם החזרה, כל משיכה מכד זהה, והמשיכות בלתי תלויות.", do=show("r-1")),
    P("בלי החזרה, אחרי כל משיכה הכד משתנה: מורידים כדור מהסך, ומהצבע שיצא.", do=show("r-2")),
    P("כשלא יודעים מה יצא קודם, הכדור השני אדום באותה הסתברות כמו הראשון.", do=show("r-3")),
    P("וכשהמידע על משיכה קודמת חלקי, מפצלים לפי המקרים. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$P(R_2/R_1)=\\dfrac{D-1}{N-1}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 עם החזרה: תמיד $\\frac DN$")
         + st.card("r-2", "rule", "🔑 בלי החזרה: הכד משתנה")
         + st.card("r-3", "rule", "🔑 $P(R_2)=\\frac DN$ כשהראשון לא ידוע")
         + st.card("r-4", "trap", "⚠️ מידע חלקי: מפצלים למקרים"))

VIDEO = Video("E09", "events", "כדים: עם החזרה, בלי החזרה ובהינתן משיכה קודמת", [title, idea, ex1, sym, exam, recap],
              bank={"24B-C-Q2c": None})
