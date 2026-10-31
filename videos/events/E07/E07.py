# -*- coding: utf-8 -*-
"""E07 · בייס: הפיכת ההתניה — video script (build: tools/video/vid.py E07).

Source: courses/events/C07.js (lesson + goal: reverse a conditioning, P(A/B) = P(B/A)P(A)/P(B) with total probability
in the denominator; decide whether data with a conditional probability are possible). Exam anchor: 25B-A-Q3b (three
bridges with N1, N2, N3 gates, each open with probability p; given that Esther crossed, P(she could use bridge 2)),
an open question (bank key None) that no guided quiz uses. P(Q) (part 3a) is derived on screen as the denominator.
Avoided on purpose: the C07 quiz data (disease 1%/95%/5%, machines 60%/40% with 2%/5%, 0.3/0.5/0.4, the "q ≥ 1−s"
feasibility with s = 0.9) and 25B-A-Q2d / 25A-B-Q2a / 25A-C-Q2b (C10 boss and C07 quiz items).
Worked examples: a box of three coins, one of them two-headed (P(two-headed / heads) = 1/2); an impossible pair
P(A∩B)=0.3, P(A/B)=0.25 (it would force P(B)=1.2). Every value is exact and checked by enumeration + Monte Carlo;
the bridge formula is checked against a full enumeration of the gates for several (N1, N2, N3, p).
"""
import itertools
from fractions import Fraction as Fr
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- example: three coins
S = w.Space([({"c": c, "f": f}, Fr(1, 3) * pr) for c, faces in (("f1", "HT"), ("f2", "HT"), ("dd", "HH"))
             for f, pr in ((faces[0], Fr(1, 2)), (faces[1], Fr(1, 2)))])
PH = S.both(lambda o: o["f"] == "H")
assert PH == Fr(2, 3) * Fr(1, 2) + Fr(1, 3) * 1 == Fr(2, 3)
POST = S.both(lambda o: o["c"] == "dd", given=lambda o: o["f"] == "H")
assert POST == Fr(1, 3) / Fr(2, 3) == Fr(1, 2)
assert S.P(lambda o: o["f"] == "H", given=lambda o: o["c"] == "dd") == 1 != POST          # the reverse direction
assert S.P(lambda o: o["c"] == "dd") == Fr(1, 3) != POST                               # the prior
TC = w.Tree("tc", [
    ("f", "הוגן", (Fr(2, 3), "2/3"), [("h", "עץ", (Fr(1, 2), "1/2"), []), ("t", "פלי", (Fr(1, 2), "1/2"), [])]),
    ("d", "דו-עץ", (Fr(1, 3), "1/3"), [("h", "עץ", (Fr(1), "1"), [])]),
], w=760, h=480, xs=[30, 320, 600], prod_text={"fh": "= 1/3", "dh": "= 1/3"})
assert TC.leaf_prob("fh") == TC.leaf_prob("dh") == Fr(1, 3)

# ---------------------------------------------------------------- example: impossible data
pAB, pA_B = Fr("0.3"), Fr("0.25")
assert pAB / pA_B == Fr("1.2") > 1                                                     # P(B) would exceed 1

# ---------------------------------------------------------------- exam 25B-A-Q3b
Q = BANK["25B-A-Q3b"]
assert Q["contextId"] == "25B-A-c3" and "P(Q/A_2)=1" in Q["solution"].replace(" ", "")
p, N1, N2, N3 = sp.symbols("p N_1 N_2 N_3", positive=True)
PQ = 1 - (1 - p ** N1) * (1 - p ** N2) * (1 - p ** N3)
ANS = p ** N2 / PQ


def bridges(n1, n2, n3, pv):
    """enumerate every gate: exact P(A2 / Q) and P(Q)"""
    out = []
    for g in itertools.product((0, 1), repeat=n1 + n2 + n3):
        pr = Fr(1)
        for x in g:
            pr *= pv if x else 1 - pv
        a = (all(g[:n1]), all(g[n1:n1 + n2]), all(g[n1 + n2:]))
        out.append(({"a1": a[0], "a2": a[1], "a3": a[2]}, pr))
    return w.Space(out)


for n1, n2, n3, pv in [(2, 3, 1, Fr(1, 2)), (1, 2, 4, Fr(2, 3)), (3, 1, 2, Fr(3, 4))]:
    B = bridges(n1, n2, n3, pv)
    q_ = lambda o: o["a1"] or o["a2"] or o["a3"]
    sub = {p: sp.Rational(pv.numerator, pv.denominator), N1: n1, N2: n2, N3: n3}
    assert B.P(q_) == Fr(str(sp.nsimplify(PQ.subs(sub))))
    assert B.P(lambda o: o["a2"], given=q_) == Fr(str(sp.nsimplify(ANS.subs(sub))))
    assert B.P(q_, given=lambda o: o["a2"]) == 1                                        # P(Q / A2) = 1
B0 = bridges(2, 3, 1, Fr(1, 2))
EX = B0.both(lambda o: o["a2"], given=lambda o: o["a1"] or o["a2"] or o["a3"])
assert EX == Fr(1, 8) / (1 - Fr(3, 4) * Fr(7, 8) * Fr(1, 2)) == Fr(8, 43)

FIG = st.raster("x-fig", "images/exams/25B-A-Q3-bridges.png", 560, (447, 247))
STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>שלושה גשרים, עם $N_1$, $N_2$, $N_3$ שערים. כל שער '
        'פתוח בהסתברות $p$, ללא תלות. <b>אם ידוע</b> שאסתר עברה, מה ההסתברות שעשתה זאת בגשר השני?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד להפוך התניה: יודעים מה קורה בכל מקרה, ושואלים לאחור, מאיזה מקרה זה הגיע."),
    P("זו נוסחת בייס. נראה אותה על עץ, ונראה גם איך מזהים נתונים שבכלל אינם אפשריים."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">E07 · בייס</div><h1>בייס: הפיכת ההתניה</h1>'
         '<p>מ-$P(B/A)$ ל-$P(A/B)$, ולהכריע אם נתונים עם הסתברות מותנית אפשריים.</p>',
   layout="title")

idea = Scene("idea", "הנוסחה", [
    P("נתון מה קורה בכל מקרה: ההסתברות של $B$ בהינתן $A$. ושואלים הפוך: אם $B$ קרה, מה ההסתברות ל-$A$?",
      say="נתון מה קורה בכל מקרה: ההסתברות של בִּי בהינתן אֵיי. ושואלים הפוך: אם בִּי קרה, מה ההסתברות לאֵיי?"),
    P("מתחילים מההגדרה: החיתוך חלקי מה שידוע.", do=show("i-1")),
    P("את החיתוך מחשבים בכלל הכפל, בכיוון הנתון: $P(B/A)$ כפול $P(A)$.",
      say="את החיתוך מחשבים בכלל הכפל, בכיוון הנתון: פֵּה של בִּי בהינתן אֵיי, כפול פֵּה של אֵיי.", do=show("i-2")),
    P("ואת המכנה, $P(B)$, מחשבים בהסתברות שלמה: כל המסלולים שנגמרים ב-$B$.",
      say="ואת המכנה, פֵּה של בִּי, מחשבים בהסתברות שלמה: כל המסלולים שנגמרים בבִּי.", do=show("i-3")),
    P("בעץ: המונה הוא המסלול הרצוי, והמכנה הוא סכום כל המסלולים שמגיעים לאותה תוצאה.", do=show("i-4"), hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="i-1" class="h">$P(A/B)=\dfrac{P(A\cap B)}{P(B)}$</div>'
         r'<div id="i-2" class="h">$=\dfrac{P(B/A)\,P(A)}{P(B)}$</div>'
         r'<div id="i-3" class="h">$P(B)=P(B/A)P(A)+P(B/\overline{A})P(\overline{A})$</div></div></div>',
   panel=st.card("i-4", "rule", "🔑 מסלול רצוי, חלקי כל המסלולים שנגמרים בנתון"))

ex = Scene("ex", "דוגמה: המטבע המזויף", [
    P("דוגמה. בקופסה שלושה מטבעות: שניים הוגנים, ואחד שבשני צדדיו עץ.", do=show("a-0")),
    P("בוחרים מטבע באקראי, מטילים אותו, ויוצא עץ. מה ההסתברות שזה המטבע המזויף?", hold=0.2),
    P("העץ: המטבע נבחר קודם. הוגן בשני שלישים, מזויף בשליש.", do=show("tc-b-f", "tc-b-d")),
    P("אחר כך ההטלה: מטבע הוגן נותן עץ בחצי, והמזויף נותן עץ תמיד.", do=show("tc-b-fh", "tc-b-ft", "tc-b-dh")),
    P("שני מסלולים נגמרים בעץ: הוגן ועץ, שני שלישים כפול חצי, שליש. ומזויף ועץ, שליש כפול אחת, גם שליש.",
      do=show(*TC.path_hl("fh"), *TC.path_hl("dh"), "tc-p-fh", "tc-p-dh")),
    P("המכנה הוא שניהם יחד: שני שלישים. זו ההסתברות לעץ.", do=show("a-1")),
    P("המונה הוא רק המסלול של המזויף: שליש. ולכן התשובה: שליש חלקי שני שלישים, חצי.", do=show("a-2"), hold=0.3),
    P("התוצאה עץ הגדילה את החשד: לפני ההטלה המזויף היה רק שליש, ואחריה הוא חצי.", hold=0.2),
    P("והמלכודת: לענות אחת. אחת היא ההסתברות לעץ **בהינתן** מזויף, הכיוון ההפוך.", do=show("a-t"), hold=0.4),
], stage=f'<div class="ev-stack">{TC.svg()}</div>',
   panel=st.card("a-0", "plain", "שני מטבעות הוגנים, ואחד דו-עץ. $D$: המזויף, $H$: יצא עץ")
         + st.card("a-1", "ex", "$P(H)=\\frac13+\\frac13=\\frac23$")
         + st.card("a-2", "rule", "🔑 $P(D/H)=\\dfrac{1/3}{2/3}=\\dfrac12$")
         + st.card("a-t", "trap", "⚠️ $P(H/D)=1$ הוא הכיוון ההפוך"))

feas = Scene("feas", "האם זה אפשרי?", [
    P("עוד שימוש של הנוסחה: לבדוק אם נתונים בכלל אפשריים."),
    P("נניח שנתון: ההסתברות של החיתוך שלוש עשיריות, וההסתברות של $A$ בהינתן $B$ רבע.",
      say="נניח שנתון: ההסתברות של החיתוך שלוש עשיריות, וההסתברות של אֵיי בהינתן בִּי רבע.", do=show("f-1")),
    P("מההגדרה, $P(B)$ שווה החיתוך חלקי ההסתברות המותנית: שלוש עשיריות חלקי רבע.",
      say="מההגדרה, פֵּה של בִּי שווה החיתוך חלקי ההסתברות המותנית: שלוש עשיריות חלקי רבע.", do=show("f-2")),
    P("יוצא אחת נקודה שתיים. הסתברות גדולה מאחת? אין דבר כזה. הנתונים סותרים.", do=show("f-t"), hold=0.3),
    P("הכלל: מבטאים כל הסתברות לא ידועה בעזרת הנתונים, ובודקים שהיא בין אפס לאחת.", do=show("f-3"), hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="f-1" class="h">$P(A\cap B)=0.3,\quad P(A/B)=0.25$</div>'
         r'<div id="f-2" class="h">$P(B)=\dfrac{P(A\cap B)}{P(A/B)}=\dfrac{0.3}{0.25}=1.2$</div></div></div>',
   panel=st.card("f-t", "trap", "⚠️ $P(B)=1.2>1$: אין מאורעות כאלה")
         + st.card("f-3", "rule", "🔑 כל הסתברות שמחשבים חייבת להיות בין $0$ ל-$1$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. אסתר צריכה לעבור נהר, ויש שלושה גשרים.", do=show("x-stem")),
    P("על הגשר הראשון $N_1$ שערים, על השני $N_2$ ועל השלישי $N_3$. כל שער פתוח בהסתברות $p$, בלי תלות.",
      say="על הגשר הראשון אֶן אחת שערים, על השני אֶן שתיים ועל השלישי אֶן שלוש. כל שער פתוח בהסתברות פִּי, בלי תלות."),
    P("ידוע שאסתר עברה. מה ההסתברות שעשתה זאת בגשר השני?", hold=0.2),
    P("נסמן: $A_2$, הגשר השני פתוח, כלומר כל השערים עליו פתוחים. ההסתברות: $p$ בחזקת $N_2$.",
      say="נסמן: אֵיי שתיים, הגשר השני פתוח, כלומר כל השערים עליו פתוחים. ההסתברות: פִּי בחזקת אֶן שתיים.", do=show("x-1")),
    P("ו-$Q$: אסתר עוברת, כלומר לפחות גשר אחד פתוח. דרך המשלים: אחת פחות ההסתברות שכל השלושה סגורים.",
      say="וקְיוּ: אסתר עוברת, כלומר לפחות גשר אחד פתוח. דרך המשלים: אחת פחות ההסתברות שכל השלושה סגורים.", do=show("x-2")),
    P("הגשרים בלתי תלויים, ולכן זו מכפלה של שלושה גורמים, כל אחד מהם אחת פחות $p$ בחזקת מספר השערים.",
      say="הגשרים בלתי תלויים, ולכן זו מכפלה של שלושה גורמים, כל אחד מהם אחת פחות פִּי בחזקת מספר השערים.", hold=0.3),
    P("עכשיו בייס. המונה: ההסתברות לעבור בהינתן שהגשר השני פתוח, כפול ההסתברות שהוא פתוח.", do=show("x-3")),
    P("ואם הגשר השני פתוח, אסתר בטוח עוברת. ההסתברות המותנית הזו היא אחת!", do=show("x-4")),
    P("לכן המונה הוא פשוט $p$ בחזקת $N_2$, והמכנה הוא ההסתברות לעבור.",
      say="לכן המונה הוא פשוט פִּי בחזקת אֶן שתיים, והמכנה הוא ההסתברות לעבור.", do=show("x-5"), hold=0.3),
    P("בדיקה במספרים: שני שערים, שלושה שערים ושער אחד, ו-$p$ שווה חצי. יוצא שמונה חלקי ארבעים ושלוש, כמו בספירת כל השערים.",
      say="בדיקה במספרים: שני שערים, שלושה שערים ושער אחד, ופִּי שווה חצי. יוצא שמונה חלקי ארבעים ושלוש, וזה בדיוק מה שיוצא בספירה של כל השערים."),
    P("המלכודת: לענות $p$ בחזקת $N_2$ בלבד, ולשכוח את המידע שהיא עברה. או לענות אחת, שזה הכיוון ההפוך.",
      say="המלכודת: לענות פִּי בחזקת אֶן שתיים בלבד, ולשכוח את המידע שהיא עברה. או לענות אחת, שזה הכיוון ההפוך.",
      do=show("x-t"), hold=0.5),
], stage=f'<div class="ev-stack">{FIG}<div class="ev-eqs">'
         r'<div id="x-1" class="h">$P(A_2)=p^{N_2}$</div>'
         r'<div id="x-2" class="h">$P(Q)=1-(1-p^{N_1})(1-p^{N_2})(1-p^{N_3})$</div>'
         r'<div id="x-3" class="h">$P(A_2/Q)=\dfrac{P(Q/A_2)\,P(A_2)}{P(Q)}$</div></div></div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-4", "ex", "$P(Q/A_2)=1$")
         + st.card("x-5", "rule", "🔑 $P(A_2/Q)=\\dfrac{p^{N_2}}{P(Q)}$")
         + st.card("x-t", "trap", "⚠️ לא $p^{N_2}$, ולא $1$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בייס הופך את הכיוון של ההתניה.", do=show("r-1")),
    P("המונה: המסלול הרצוי, בכלל הכפל. המכנה: כל המסלולים שנגמרים במה שידוע, בהסתברות שלמה.", do=show("r-2")),
    P("ההסתברות של $A$ בהינתן $B$ ושל $B$ בהינתן $A$ הן שני מספרים שונים.",
      say="ההסתברות של אֵיי בהינתן בִּי ושל בִּי בהינתן אֵיי הן שני מספרים שונים.", do=show("r-3")),
    P("ונתונים שנותנים הסתברות מחוץ לאפס עד אחת, הם בלתי אפשריים. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$P(A/B)=\\dfrac{P(B/A)\\,P(A)}{P(B)}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 בייס: הופכים את ההתניה")
         + st.card("r-2", "rule", "🔑 מכנה: הסתברות שלמה")
         + st.card("r-3", "trap", "⚠️ $P(A/B)\\ne P(B/A)$")
         + st.card("r-4", "rule", "🔑 הסתברות מחוץ ל-$[0,1]$: נתונים סותרים"))

VIDEO = Video("E07", "events", "בייס: הפיכת ההתניה", [title, idea, ex, feas, exam, recap],
              bank={"25B-A-Q3b": None})
