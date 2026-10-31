# -*- coding: utf-8 -*-
"""E05 · כלל הכפל ועצי הסתברות — video script (build: tools/video/vid.py E05).

Source: courses/events/C05.js (lesson + goal: P(A∩B) = P(A)·P(B/A), the chain rule, trees: multiply along a path,
add paths). Exam anchor: 25S-B-Q2b (two different numbers drawn from 1..2N+1; P(the sum is even)), an open question
(bank key None) that no guided quiz uses. As in the official solution, the two numbers are different (no replacement).
Avoided on purpose: the C05 quiz cases (4 red / 6 black two reds, 5/5 three reds, the machine 0.9/0.8/0.3,
0.6·0.25, 0.5·0.6·0.4) and the C09 urns (3 red / 5 black); 25S-B-Q2c (given the first is even) is not solved.
Worked example: 6 good and 2 faulty bulbs, two (then three) drawn without replacement. Every branch and product is
computed exactly and checked on the checker's urn space (w_events.Space.urn) with Monte Carlo; the exam result is
proved with sympy and enumerated for N = 1..8.
"""
from fractions import Fraction as Fr
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- numbers (verified)
U2 = w.Space.urn(counts={"g": 6, "d": 2}, draws=2, replace=False)
GG = U2.both(lambda o: o["g_1"] and o["g_2"])
GD = U2.both(lambda o: o["g_1"] and o["d_2"])
DG = U2.both(lambda o: o["d_1"] and o["g_2"])
DD = U2.both(lambda o: o["d_1"] and o["d_2"])
assert (GG, GD, DG, DD) == (Fr(6, 8) * Fr(5, 7), Fr(6, 8) * Fr(2, 7), Fr(2, 8) * Fr(6, 7), Fr(2, 8) * Fr(1, 7))
assert (GG, GD, DG, DD) == (Fr(30, 56), Fr(12, 56), Fr(12, 56), Fr(2, 56)) and GG + GD + DG + DD == 1
assert U2.P(lambda o: o["g_2"], given=lambda o: o["g_1"]) == Fr(5, 7)        # the conditional branch
ONE = U2.both(lambda o: o["d"] == 1)
assert ONE == GD + DG == Fr(24, 56) == Fr(3, 7)
U2r = w.Space.urn(counts={"g": 6, "d": 2}, draws=2, replace=True)
assert U2r.P(lambda o: o["g_1"] and o["g_2"]) == Fr(9, 16) != GG                # the trap: as if with replacement
U3 = w.Space.urn(counts={"g": 6, "d": 2}, draws=3, replace=False)
GGG = U3.both(lambda o: o["g"] == 3)
assert GGG == Fr(6, 8) * Fr(5, 7) * Fr(4, 6) == Fr(120, 336) == Fr(5, 14)

T1 = w.Tree("t1", [
    ("G", "תקינה", (Fr(6, 8), "6/8"), [("G", "תקינה", Fr(5, 7), []), ("D", "פגומה", Fr(2, 7), [])]),
    ("D", "פגומה", (Fr(2, 8), "2/8"), [("G", "תקינה", Fr(6, 7), []), ("D", "פגומה", Fr(1, 7), [])]),
], w=760, h=540, prod_text={"GG": "= 30/56", "GD": "= 12/56", "DG": "= 12/56", "DD": "= 2/56"})
for pth, val in {"GG": GG, "GD": GD, "DG": DG, "DD": DD}.items():
    assert T1.leaf_prob(pth) == val

# ---------------------------------------------------------------- exam 25S-B-Q2b
Q = BANK["25S-B-Q2b"]
assert Q["contextId"] == "25S-B-c2" and "\\frac N{2N+1}" in Q["solution"].replace("P(C)=", "")
N = sp.symbols("N", positive=True, integer=True)
pE1, pO1 = N / (2 * N + 1), (N + 1) / (2 * N + 1)
pEE, pOO = (N - 1) / (2 * N), N / (2 * N)
total = sp.simplify(pE1 * pEE + pO1 * pOO)
assert sp.simplify(total - N / (2 * N + 1)) == 0
assert sp.simplify(pE1 * pEE - (N - 1) / (2 * (2 * N + 1))) == 0 and sp.simplify(pO1 * pOO - (N + 1) / (2 * (2 * N + 1))) == 0
for n in range(1, 9):                                                         # enumerate ordered pairs of distinct numbers
    Sn = w.Space.urn(values=list(range(1, 2 * n + 2)), draws=2, replace=False)
    assert Sn.P(lambda o: o["sum"] % 2 == 0) == Fr(n, 2 * n + 1) == Fr(int(total.subs(N, n).p), int(total.subs(N, n).q))
S3 = w.Space.urn(values=list(range(1, 8)), draws=2, replace=False)            # N = 3, with Monte Carlo
assert S3.both(lambda o: o["sum"] % 2 == 0) == Fr(3, 7)
trap = sp.simplify(pE1 ** 2 + pO1 ** 2)                                       # the trap: as if drawn with replacement
assert sp.simplify(trap - total) != 0 and trap.subs(N, 3) == sp.Rational(25, 49)

TX = w.Tree("tx", [
    ("E", "זוגי", (pE1, "N/(2N+1)"), [("E", "זוגי", (pEE, "(N−1)/(2N)"), []), ("O", "אי-זוגי", (1 - pEE, "(N+1)/(2N)"), [])]),
    ("O", "אי-זוגי", (pO1, "(N+1)/(2N+1)"), [("E", "זוגי", (1 - pOO, "N/(2N)"), []), ("O", "אי-זוגי", (pOO, "N/(2N)"), [])]),
], w=820, h=540, xs=[30, 330, 640])

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>ברשימה המספרים העוקבים מ-$1$ עד $2N+1$. '
        'בוחרים באקראי שני מספרים, אחד אחרי השני (שונים זה מזה). מה ההסתברות שסכומם זוגי?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחשב הסתברות של **קרה זה, ואחר כך זה**."),
    P("נכיר את כלל הכפל ואת כלל השרשרת, ונצייר אותם כעץ הסתברות."),
    P("ובסוף נפתור סעיף אמיתי ממבחן, עם עץ.", hold=0.4),
], stage='<div class="kicker">E05 · הסתברות מותנית</div><h1>כלל הכפל ועצי הסתברות</h1>'
         '<p>לחשב הסתברות של "קרה זה ואחר כך זה" בעזרת כלל הכפל, כלל השרשרת ועץ.</p>',
   layout="title")

idea = Scene("idea", "כלל הכפל", [
    P("נתחיל מההגדרה של הסתברות מותנית: החיתוך, חלקי מה שידוע.", do=show("i-1")),
    P("נעביר אגפים, ונקבל את **כלל הכפל**: ההסתברות של $A$ וגם $B$...", say="נעביר אגפים, ונקבל את כלל הכפל: ההסתברות של אֵיי וגם בִּי...",
      do=show("i-2")),
    P("...שווה להסתברות של $A$, כפול ההסתברות של $B$ **בהינתן** $A$.",
      say="שווה להסתברות של אֵיי, כפול ההסתברות של בִּי בהינתן אֵיי."),
    P("במילים: קודם $A$ צריך לקרות. ואז, בעולם שבו $A$ כבר קרה, צריך גם $B$ לקרות.",
      say="במילים: קודם אֵיי צריך לקרות. ואז, בעולם שבו אֵיי כבר קרה, צריך גם בִּי לקרות.", hold=0.3),
    P("ולשלושה שלבים, **כלל השרשרת**: כל גורם מותנה בכל מה שקרה לפניו.", do=show("i-3")),
    P("עץ הסתברות מצייר את זה. כל ענף הוא שלב, ועל כל ענף כתובה ההסתברות **המותנית** שלו.", do=show("i-4")),
    P("לאורך מסלול **כופלים**, ומסלולים שונים של אותו מאורע **מחברים**.", do=show("i-5"), hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs">'
         '<div id="i-1" class="h">$P(B/A)=\\dfrac{P(A\\cap B)}{P(A)}$</div>'
         '<div id="i-2" class="h">$P(A\\cap B)=P(A)\\cdot P(B/A)$</div>'
         '<div id="i-3" class="h">$P(A_1\\cap A_2\\cap A_3)=P(A_1)\\,P(A_2/A_1)\\,P(A_3/A_1\\cap A_2)$</div></div></div>',
   panel=st.card("i-4", "rule", "🔑 על ענף: הסתברות מותנית")
         + st.card("i-5", "rule", "🔑 לאורך מסלול כופלים; בין מסלולים מחברים"))

ex1 = Scene("ex1", "דוגמה: נורות", [
    P("דוגמה. בקופסה שמונה נורות: שש תקינות ושתיים פגומות. מוציאים שתיים, בזו אחר זו, **בלי החזרה**.", do=show("a-0")),
    P("השלב הראשון: הנורה הראשונה תקינה בהסתברות שש שמיניות, ופגומה בשתי שמיניות.", do=show("t1-b-G", "t1-b-D")),
    P("השלב השני תלוי במה שקרה. אם הראשונה תקינה, נשארו שבע נורות, חמש מהן תקינות.", do=show("t1-b-GG", "t1-b-GD")),
    P("ואם הראשונה פגומה, נשארו שבע, ושש מהן תקינות.", do=show("t1-b-DG", "t1-b-DD"), hold=0.3),
    P("שתיהן תקינות: כופלים לאורך המסלול. שש שמיניות כפול חמש שביעיות: שלושים חלקי חמישים ושש.",
      do=show(*T1.path_hl("GG"), "t1-p-GG", "a-1")),
    P("**בדיוק אחת פגומה**: יש לזה שני מסלולים. תקינה ואז פגומה, או פגומה ואז תקינה.",
      do=hide(*T1.path_hl("GG")) + show(*T1.path_hl("GD"), *T1.path_hl("DG"), "t1-p-GD", "t1-p-DG")),
    P("שתים עשרה חלקי חמישים ושש לכל אחד, ומחברים: עשרים וארבע חלקי חמישים ושש, כלומר שלוש שביעיות.",
      do=show("a-2"), hold=0.3),
    P("בדיקה: ארבעת המסלולים יחד מסתכמים לאחת.", do=show("t1-p-DD")),
    P("והמלכודת: לכפול שש שמיניות בשש שמיניות. זה נכון רק **עם** החזרה, כשהקופסה חוזרת לקדמותה.", do=show("a-t")),
    P("בלי החזרה, הענף השני תמיד מותנה במה שיצא בראשון.", hold=0.4),
], stage=f'<div class="ev-stack">{T1.svg()}</div>',
   panel=st.card("a-0", "plain", "$6$ תקינות, $2$ פגומות, בלי החזרה. $T_i$: הנורה ה-$i$ תקינה")
         + st.card("a-1", "ex", "$P(T_1\\cap T_2)=\\frac68\\cdot\\frac57=\\frac{30}{56}$")
         + st.card("a-2", "rule", "🔑 בדיוק אחת: $\\frac{12}{56}+\\frac{12}{56}=\\frac37$")
         + st.card("a-t", "trap", "⚠️ $\\frac68\\cdot\\frac68$ רק עם החזרה"))

chain = Scene("chain", "כלל השרשרת", [
    P("ועכשיו שלוש נורות, ושואלים: מה ההסתברות שכל השלוש תקינות?", do=show("c-1")),
    P("הראשונה: שש שמיניות. השנייה, בהינתן שהראשונה תקינה: חמש שביעיות.", do=show("c-2")),
    P("והשלישית, בהינתן ששתי הראשונות תקינות: נשארו שש נורות, ארבע מהן תקינות. ארבע שישיות.", do=show("c-3")),
    P("כופלים: מאה ועשרים חלקי שלוש מאות שלושים ושש, כלומר חמש חלקי ארבע עשרה.",
      say="כופלים: מאה ועשרים חלקי שלוש מאות שלושים ושש, כלומר חמש חלקי ארבע עשרה.", do=show("c-4")),
    P("כל גורם מותנה בכל מה שקרה לפניו. זה כל הסוד של כלל השרשרת.", hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="c-1" class="h">$P(T_1\cap T_2\cap T_3)=P(T_1)\,P(T_2/T_1)\,P(T_3/T_1\cap T_2)$</div>'
         r'<div><span id="c-2" class="h">$=\frac68\cdot\frac57$</span><span id="c-3" class="h">$\;\cdot\;\frac46$</span></div>'
         r'<div id="c-4" class="h">$=\frac{120}{336}=\frac{5}{14}$</div></div></div>',
   panel=st.card("c-5", "rule", "🔑 שרשרת: כל שלב מותנה בכל מה שלפניו"),
   layout="split")
chain.phrases[-1].do = show("c-5")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. ברשימה המספרים מאחת עד שתיים $N$ ועוד אחת.", say="ועכשיו סעיף ממבחן. ברשימה המספרים מאחת עד שתיים אֶן ועוד אחת.",
      do=show("x-stem")),
    P("בוחרים שני מספרים שונים, אחד אחרי השני. מה ההסתברות שהסכום זוגי?"),
    P("קודם נספור: יש $N$ מספרים זוגיים, ו-$N$ ועוד אחד אי-זוגיים, כי הרשימה מתחילה ונגמרת באי-זוגי.",
      say="קודם נספור: יש אֶן מספרים זוגיים, ואֶן ועוד אחד אי זוגיים, כי הרשימה מתחילה ונגמרת באי זוגי.", do=show("x-1")),
    P("סכום זוגי פירושו: שניהם זוגיים, או שניהם אי-זוגיים. אלה שני מסלולים בעץ.", do=show("x-2")),
    P("השלב הראשון: זוגי בהסתברות $N$ חלקי $2N+1$.",
      say="השלב הראשון: זוגי בהסתברות אֶן חלקי, בסוגריים, שתיים אֶן ועוד אחת.", do=show("tx-b-E", "tx-b-O")),
    P("אם הראשון זוגי, נשארו שתיים $N$ מספרים, ורק $N$ פחות אחד מהם זוגיים.",
      say="אם הראשון זוגי, נשארו שתיים אֶן מספרים, ורק אֶן פחות אחד מהם זוגיים.", do=show("tx-b-EE", "tx-b-EO")),
    P("ואם הראשון אי-זוגי, נשארו $N$ אי-זוגיים מתוך שתיים $N$.",
      say="ואם הראשון אי זוגי, נשארו אֶן אי זוגיים מתוך שתיים אֶן.", do=show("tx-b-OE", "tx-b-OO"), hold=0.3),
    P("כופלים לאורך כל מסלול, ומחברים את שני המסלולים הטובים.", do=show(*TX.path_hl("EE"), *TX.path_hl("OO"), "x-3")),
    P("במונה יוצא $N(N-1)+(N+1)N$, כלומר פעמיים $N$ בריבוע.",
      say="במונה יוצא אֶן כפול, בסוגריים, אֶן פחות אחת, ועוד, בסוגריים, אֶן ועוד אחת, כפול אֶן. כלומר פעמיים אֶן בריבוע."),
    P("מצמצמים, והתשובה: $N$ חלקי $2N+1$.", say="מצמצמים, והתשובה: אֶן חלקי, בסוגריים, שתיים אֶן ועוד אחת.",
      do=show("x-4"), hold=0.3),
    P("המלכודת: להשתמש באותה הסתברות גם בשלב השני, כאילו המספר הראשון חזר לרשימה. כך הענף השני לא מותנה.",
      do=show("x-t")),
    P("בדיקה עם $N$ שווה אחת: הרשימה אחת, שתיים, שלוש. הסכום זוגי רק באחת ושלוש: שניים מתוך שישה זוגות, שליש.",
      say="בדיקה עם אֶן שווה אחת: הרשימה אחת, שתיים, שלוש. הסכום זוגי רק באחת ושלוש: שניים מתוך שישה זוגות, שליש.",
      hold=0.5),
], stage=f'<div class="ev-stack">{TX.svg()}</div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-1", "plain", "זוגיים: $N$. אי-זוגיים: $N+1$")
         + st.card("x-2", "plain", "סכום זוגי: שניהם זוגיים, או שניהם אי-זוגיים")
         + st.card("x-3", "ex", "$\\frac{N}{2N+1}\\cdot\\frac{N-1}{2N}+\\frac{N+1}{2N+1}\\cdot\\frac{N}{2N}$")
         + st.card("x-4", "rule", "🔑 $P=\\dfrac{2N^2}{2N(2N+1)}=\\dfrac{N}{2N+1}$")
         + st.card("x-t", "trap", "⚠️ בשלב השני המכנה הוא $2N$, לא $2N+1$"))
assert total.subs(N, 1) == sp.Rational(2, 6)                                   # the N = 1 check said aloud

recap = Scene("recap", "סיכום", [
    P("לסיכום: כלל הכפל. ההסתברות של שניהם היא ההסתברות של הראשון, כפול ההסתברות המותנית של השני.", do=show("r-1")),
    P("כלל השרשרת: כל שלב מותנה בכל מה שקרה לפניו.", do=show("r-2")),
    P("בעץ: על כל ענף ההסתברות המותנית שלו. לאורך מסלול כופלים, ובין מסלולים מחברים.", do=show("r-3")),
    P("ובלי החזרה, השלב השני תמיד תלוי בראשון. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$P(A\\cap B)=P(A)\\cdot P(B/A)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $P(A\\cap B)=P(A)\\,P(B/A)$")
         + st.card("r-2", "rule", "🔑 שרשרת: מותנה בכל מה שקדם")
         + st.card("r-3", "rule", "🔑 עץ: כופלים לאורך, מחברים בין מסלולים")
         + st.card("r-4", "trap", "⚠️ בלי החזרה: $P(B/A)$, לא $P(B)$"))

VIDEO = Video("E05", "events", "כלל הכפל ועצי הסתברות", [title, idea, ex1, chain, exam, recap],
              bank={"25S-B-Q2b": None})
