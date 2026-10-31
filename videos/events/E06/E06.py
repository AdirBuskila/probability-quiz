# -*- coding: utf-8 -*-
"""E06 · הסתברות שלמה — video script (build: tools/video/vid.py E06).

Source: courses/events/C06.js (lesson + goal: split by cases of a partition and add, P(B) = Σ P(B/A_i) P(A_i)).
Exam anchor: 24B-C-Q2b (digits 0..9, two drawn without replacement; P(the second is divisible by 3)), an open
question (bank key None) that no guided quiz uses. The official solution counts ordered pairs; the video splits by the
first digit (total probability) and cross-checks with that count.
Avoided on purpose: the C06 quiz data (machines 60%/40% with 2%/5%, boxes 0.5/0.3/0.2, 3 red / 7 black second ball,
P(A)=0.4 with 0.5/0.2, 0.3 with 0.9/0.2, the dice partitions) and 24B-C-Q2d / 24B-B-Q2c (a third draw: twins of the
C09 quiz and its bank item) — the video never says anything about a third draw.
Worked example: three shifts 50%/30%/20% with 1%/2%/5% faulty. Every number is exact (Fractions) and checked on an
explicit space / the checker's urn space with Monte Carlo.
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- numbers (verified)
SH = {"m": (Fr("0.5"), Fr("0.01")), "e": (Fr("0.3"), Fr("0.02")), "n": (Fr("0.2"), Fr("0.05"))}
assert sum(pr for pr, _ in SH.values()) == 1                                 # the shifts are a partition
S = w.Space([({"sh": k, "D": d}, pr * (f if d else 1 - f)) for k, (pr, f) in SH.items() for d in (1, 0)])
PD = S.both(lambda o: o["D"] == 1, n=2_000_000)
assert PD == Fr("0.005") + Fr("0.006") + Fr("0.010") == Fr("0.021")
for k, (pr, f) in SH.items():
    assert S.P(lambda o: o["D"] == 1, given=lambda o, k=k: o["sh"] == k) == f
AVG = sum(f for _, f in SH.values()) / 3
assert AVG == Fr(8, 300) and AVG != PD                                       # the trap: an unweighted average
assert Fr("0.5") * Fr("0.05") + Fr("0.3") * Fr("0.02") + Fr("0.2") * Fr("0.01") == Fr("0.033") != PD   # wrong weights

TS = w.Tree("ts", [
    ("m", "בוקר", (Fr("0.5"), "0.5"), [("d", "פגום", (Fr("0.01"), "0.01"), []), ("o", "תקין", (Fr("0.99"), "0.99"), [])]),
    ("e", "ערב", (Fr("0.3"), "0.3"), [("d", "פגום", (Fr("0.02"), "0.02"), []), ("o", "תקין", (Fr("0.98"), "0.98"), [])]),
    ("n", "לילה", (Fr("0.2"), "0.2"), [("d", "פגום", (Fr("0.05"), "0.05"), []), ("o", "תקין", (Fr("0.95"), "0.95"), [])]),
], w=780, h=640, xs=[30, 330, 620], prod_text={"md": "= 0.005", "ed": "= 0.006", "nd": "= 0.010"})
assert TS.leaf_prob("md") + TS.leaf_prob("ed") + TS.leaf_prob("nd") == PD

# ---------------------------------------------------------------- exam 24B-C-Q2b
Q = BANK["24B-C-Q2b"]
assert Q["contextId"] == "24B-C-c2" and "\\frac{4\\cdot9}{90}=\\frac25" in Q["solution"].replace(" ", "")
U = w.Space.urn(values=list(range(10)), draws=2, replace=False)
A1 = lambda o: o["v1"] % 3 == 0
A2 = lambda o: o["v2"] % 3 == 0
assert [d for d in range(10) if d % 3 == 0] == [0, 3, 6, 9]
p1 = U.P(A1)
pA2_A1, pA2_nA1 = U.P(A2, given=A1), U.P(A2, given=lambda o: not A1(o))
assert (p1, pA2_A1, pA2_nA1) == (Fr(4, 10), Fr(3, 9), Fr(4, 9))
PA2 = U.both(A2)
assert PA2 == p1 * pA2_A1 + (1 - p1) * pA2_nA1 == Fr(12, 90) + Fr(24, 90) == Fr(36, 90) == Fr(2, 5)
assert U.count(A2) == 4 * 9 and len(U.out) == 90                              # the official count
assert PA2 == p1                                                             # the same as the first digit

TX = w.Tree("tx", [
    ("a", "מתחלקת ב-3", (Fr(4, 10), "4/10"), [("a", "מתחלקת", (Fr(3, 9), "3/9"), []), ("b", "לא", (Fr(6, 9), "6/9"), [])]),
    ("b", "לא מתחלקת", (Fr(6, 10), "6/10"), [("a", "מתחלקת", (Fr(4, 9), "4/9"), []), ("b", "לא", (Fr(5, 9), "5/9"), [])]),
], w=780, h=520, xs=[30, 320, 610], prod_text={"aa": "= 12/90", "ba": "= 24/90"})
UR = w.Urn("ur", [(str(d), "t" if d % 3 == 0 else "g") for d in range(10)], per_row=5, d=74)

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>באוסף 10 הספרות $0,1,\\dots,9$. '
        'מוציאים שתי ספרות <b>ללא החזרה</b>. מה ההסתברות שהספרה <b>השנייה</b> מתחלקת ב-3?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לחשב הסתברות כשהיא תלויה במקרה: מפצלים לפי המקרים, מחשבים בכל אחד, ומחברים."),
    P("זו נוסחת ההסתברות השלמה, ונראה למה היא בעצם ממוצע משוקלל."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">E06 · הסתברות שלמה</div><h1>הסתברות שלמה</h1>'
         '<p>לפצל מאורע לפי מקרים, לחשב בכל מקרה, ולחבר: $P(B)=\\sum P(B/A_i)P(A_i)$.</p>',
   layout="title")

idea = Scene("idea", "חלוקה והנוסחה", [
    P("לפעמים ההסתברות של $B$ לא נתונה, אבל ידוע מה קורה בכל מקרה אפשרי.",
      say="לפעמים ההסתברות של בִּי לא נתונה, אבל ידוע מה קורה בכל מקרה אפשרי."),
    P("המקרים צריכים להיות **חלוקה** של אומגה: זרים זה לזה, ויחד הם מכסים הכול.", do=show("i-1")),
    P("כלומר כל תוצאה שייכת לבדיוק מקרה אחד. הדוגמה הפשוטה ביותר: $A$ והמשלים שלו.",
      say="כלומר כל תוצאה שייכת לבדיוק מקרה אחד. הדוגמה הפשוטה ביותר: אֵיי והמשלים שלו.", hold=0.3),
    P("ואז: ההסתברות של $B$ היא סכום על כל המקרים, של ההסתברות של המקרה, כפול ההסתברות של $B$ בתוך המקרה.",
      say="ואז: ההסתברות של בִּי היא סכום על כל המקרים, של ההסתברות של המקרה, כפול ההסתברות של בִּי בתוך המקרה.",
      do=show("i-2")),
    P("למה זה נכון? כל מחובר הוא, לפי כלל הכפל, החיתוך של $B$ עם מקרה אחד.",
      say="למה זה נכון? כל מחובר הוא, לפי כלל הכפל, החיתוך של בִּי עם מקרה אחד.", do=show("i-3")),
    P("החיתוכים האלה זרים, ויחד הם כל $B$. ולכן ההסתברויות שלהם מתחברות בדיוק ל-$P(B)$.",
      say="החיתוכים האלה זרים, ויחד הם כל בִּי. ולכן ההסתברויות שלהם מתחברות בדיוק לפֵּה של בִּי.", hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="i-2" class="h">$P(B)=\sum_i P(B/A_i)\,P(A_i)$</div>'
         r'<div id="i-3" class="h">$P(B/A_i)\,P(A_i)=P(B\cap A_i)$</div></div></div>',
   panel=st.card("i-1", "rule", "🔑 חלוקה: $A_1,\\dots,A_n$ זרים בזוגות, ואיחודם $\\Omega$"))

ex = Scene("ex", "דוגמה: שלוש משמרות", [
    P("דוגמה. במפעל שלוש משמרות. משמרת הבוקר מייצרת חצי מהמוצרים, ערב שלושים אחוז, ולילה עשרים אחוז.",
      do=show("ts-b-m", "ts-b-e", "ts-b-n")),
    P("בבוקר אחוז אחד מהמוצרים פגום, בערב שני אחוזים, ובלילה חמישה אחוזים.",
      do=show("ts-b-md", "ts-b-mo", "ts-b-ed", "ts-b-eo", "ts-b-nd", "ts-b-no")),
    P("שימו לב לעץ: ההסתברות על הענף השני היא **מותנית**, בתוך המשמרת.", hold=0.2),
    P("שלוש המשמרות הן חלוקה: כל מוצר יוצא מבדיוק משמרת אחת, והמשקלים מסתכמים לאחת.", do=show("a-1")),
    P("מוצר אקראי פגום: כופלים לאורך כל מסלול שנגמר בפגום.",
      do=show(*TS.path_hl("md"), *TS.path_hl("ed"), *TS.path_hl("nd"))),
    P("בוקר: חמש אלפיות. ערב: שש אלפיות. ולילה: עשר אלפיות.", do=show("ts-p-md", "ts-p-ed", "ts-p-nd")),
    P("מחברים: עשרים ואחת אלפיות. כלומר שני אחוזים ועשירית.", do=show("a-2"), hold=0.3),
    P("זה **ממוצע משוקלל** של אחוז, שניים וחמישה: המשקלים הם גודל המשמרות.", do=show("a-3")),
    P("והמלכודת: ממוצע פשוט. אחת ועוד שתיים ועוד חמש, חלקי שלוש, נותן כמעט שלושה אחוזים, יותר מדי.",
      do=show("a-t")),
    P("משמרת הלילה, עם הכי הרבה פגמים, היא הקטנה ביותר. ולכן המשקל שלה קטן.", hold=0.4),
], stage=f'<div class="ev-stack">{TS.svg()}</div>',
   panel=st.card("a-1", "plain", "חלוקה: $0.5+0.3+0.2=1$")
         + st.card("a-2", "rule", "🔑 $P(D)=0.005+0.006+0.010=0.021$")
         + st.card("a-3", "ex", "ממוצע משוקלל של $1\\%,\\ 2\\%,\\ 5\\%$")
         + st.card("a-t", "trap", "⚠️ $\\frac{1\\%+2\\%+5\\%}{3}\\approx2.67\\%$: בלי משקלים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. באוסף עשר ספרות, מאפס עד תשע.", do=show("x-stem", "ur")),
    P("מוציאים שתי ספרות **בלי החזרה**. מה ההסתברות שהספרה **השנייה** מתחלקת בשלוש?"),
    P("מתחלקות בשלוש ארבע ספרות: אפס, שלוש, שש ותשע. שימו לב, גם אפס.", do=show("ur-h0", "ur-h3", "ur-h6", "ur-h9")),
    P("הבעיה: מה שנשאר באוסף תלוי בספרה הראשונה. אז נפצל לפי הספרה הראשונה, וזו החלוקה שלנו.",
      do=hide("ur") + show("txw", "tx-b-a", "tx-b-b")),
    P("אם הראשונה מתחלקת בשלוש, בהסתברות ארבע עשיריות, נשארו תשע ספרות ורק שלוש מתאימות.",
      do=show("tx-b-aa", "tx-b-ab")),
    P("ואם הראשונה לא מתחלקת, בהסתברות שש עשיריות, כל הארבע עוד באוסף: ארבע מתוך תשע.",
      do=show("tx-b-ba", "tx-b-bb"), hold=0.3),
    P("כופלים לאורך שני המסלולים: שתים עשרה חלקי תשעים, ועשרים וארבע חלקי תשעים.",
      do=show(*TX.path_hl("aa"), *TX.path_hl("ba"), "tx-p-aa", "tx-p-ba")),
    P("מחברים: שלושים ושש חלקי תשעים, כלומר שתי חמישיות.", do=show("x-1"), hold=0.3),
    P("בדיקה בספירה: לספרה השנייה ארבע אפשרויות, ולראשונה תשע. שלושים ושש מתוך תשעים זוגות. אותה תשובה.",
      do=show("x-2")),
    P("המלכודת: לענות שלוש תשיעיות או ארבע תשיעיות. כל אחת מהן היא רק מקרה אחד, ולא התמונה המלאה.", do=show("x-t")),
    P("ושימו לב: יצא בדיוק כמו ההסתברות של הספרה הראשונה, ארבע עשיריות. נחזור לזה בשלב על כדים.", hold=0.5),
], stage=f'<div class="ev-stack"><div class="ev-swap" style="--swap-h:520px"><div id="ur" class="h">{UR.svg()}</div>'
         f'<div id="txw" class="h">{TX.svg()}</div></div></div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-1", "rule", "🔑 $P(A_2)=\\frac{4}{10}\\cdot\\frac39+\\frac{6}{10}\\cdot\\frac49=\\frac{36}{90}=\\frac25$")
         + st.card("x-2", "ex", "ספירה: $\\frac{9\\cdot4}{10\\cdot9}=\\frac25$")
         + st.card("x-t", "trap", "⚠️ $\\frac39$ או $\\frac49$: רק מקרה אחד"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כשההסתברות תלויה במקרה, מפצלים לפי חלוקה: מקרים זרים שמכסים הכול.", do=show("r-1")),
    P("בכל מקרה מחשבים את ההסתברות המותנית, ומכפילים בהסתברות של המקרה.", do=show("r-2")),
    P("ומחברים. זה ממוצע משוקלל, והמשקלים הם ההסתברויות של המקרים.", do=show("r-3")),
    P("וכל מותנית מוכפלת במשקל של **המקרה שלה**, לא של מקרה אחר. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$P(B)=\\sum_i P(B/A_i)\\,P(A_i)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 חלוקה: זרים, ומכסים את $\\Omega$")
         + st.card("r-2", "rule", "🔑 בכל מקרה: $P(B/A_i)\\,P(A_i)$")
         + st.card("r-3", "rule", "🔑 מחברים: ממוצע משוקלל")
         + st.card("r-4", "trap", "⚠️ $P(B/A)$ הולך עם $P(A)$, לא עם $P(\\overline{A})$"))

VIDEO = Video("E06", "events", "הסתברות שלמה", [title, idea, ex, exam, recap],
              bank={"24B-C-Q2b": None})
