# -*- coding: utf-8 -*-
"""E02 · משלים, הכלה והפרדה — video script (build: tools/video/vid.py E02).

Source: courses/events/C02.js (lesson + goal: union, complement, difference, "exactly one", counting multiples of k in
a range). Exam anchor: 25A-A-Q2a (a random three-digit number: P(A2), P(A4), P(A8)), an open question (bank key None)
that no guided quiz uses.
Avoided on purpose: the C02 quiz data (0.5/0.3/0.1, 0.5/0.4/0.1, the 60%/50%/30% class, multiples of 7, "2 or 5" among
three-digit numbers) and 25A-A-Q2d (C10 boss: is A8 = A2 ∩ A4?): the video never intersects A2 with A4.
Worked examples: P(A)=0.6, P(B)=0.45, P(A∩B)=0.25 (languages at a company); two-digit numbers divisible by 3 or 4.
Every value is computed from an explicit four-cell space or by enumerating the numbers, plus Monte Carlo.
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- numbers (verified)
pA, pB, pAB = Fr("0.6"), Fr("0.45"), Fr("0.25")
S = w.Space([({"A": 1, "B": 1}, pAB), ({"A": 1, "B": 0}, pA - pAB), ({"A": 0, "B": 1}, pB - pAB),
             ({"A": 0, "B": 0}, 1 - pA - pB + pAB)])
assert S.P(lambda o: o["A"]) == pA and S.P(lambda o: o["B"]) == pB
U = S.both(lambda o: o["A"] or o["B"])
NONE = S.both(lambda o: not o["A"] and not o["B"])
DIFF = S.both(lambda o: o["A"] and not o["B"])
ONE = S.both(lambda o: o["A"] != o["B"])
assert U == Fr("0.8") == pA + pB - pAB and NONE == Fr("0.2") == 1 - U
assert DIFF == Fr("0.35") == pA - pAB and ONE == Fr("0.55") == pA + pB - 2 * pAB
assert pA + pB == Fr("1.05") > 1                                    # the trap: P(A)+P(B) is not a probability here
CELLS = {"ab": pAB, "a": pA - pAB, "b": pB - pAB, "o": 1 - U}
assert sum(CELLS.values()) == 1 and CELLS == {"ab": Fr("0.25"), "a": Fr("0.35"), "b": Fr("0.2"), "o": Fr("0.2")}


def count(k, a, b):
    """multiples of k in [a, b]: floor(b/k) - floor((a-1)/k), cross-checked by enumeration"""
    n = b // k - (a - 1) // k
    assert n == sum(1 for x in range(a, b + 1) if x % k == 0)
    return n


# two-digit numbers divisible by 3 or by 4
N2 = 90
c3, c4, c12 = count(3, 10, 99), count(4, 10, 99), count(12, 10, 99)
assert (c3, c4, c12) == (30, 22, 8) and (99 // 3, 9 // 3, 99 // 4, 9 // 4, 99 // 12) == (33, 3, 24, 2, 8)
S2 = w.Space.uniform([{"x": x} for x in range(10, 100)])
P34 = S2.both(lambda o: o["x"] % 3 == 0 or o["x"] % 4 == 0)
assert c3 + c4 - c12 == 44 and P34 == Fr(44, 90) == Fr(22, 45)
assert S2.P(lambda o: o["x"] % 3 == 0 and o["x"] % 4 == 0) == Fr(c12, N2)      # 3 and 4 <=> 12
assert Fr(c3 + c4, N2) == Fr(26, 45)                                          # the trap: no subtraction

# exam 25A-A-Q2a: Ω = {100..999}
Q = BANK["25A-A-Q2a"]
assert Q["contextId"] == "25A-A-c2" and "|\\Omega|=900" in Q["solution"].replace(" ", "")
SX = w.Space.uniform([{"x": x} for x in range(100, 1000)])
c2_, c4_, c8_ = count(2, 100, 999), count(4, 100, 999), count(8, 100, 999)
assert (c2_, c4_, c8_) == (450, 225, 112)
assert (999 // 2, 99 // 2, 999 // 4, 99 // 4, 999 // 8, 99 // 8) == (499, 49, 249, 24, 124, 12)
P2, P4, P8 = (SX.both(lambda o, k=k: o["x"] % k == 0) for k in (2, 4, 8))
assert (P2, P4, P8) == (Fr(1, 2), Fr(1, 4), Fr(28, 225)) and P8 != Fr(1, 8)
assert Fr(900, 8) == Fr("112.5") and 900 % 2 == 900 % 4 == 0 != 900 % 8                   # the trap
for frag in ("\\frac{450}{900}=\\frac12", "\\frac{225}{900}=\\frac14", "\\frac{112}{900}=\\frac{28}{225}"):
    assert frag in Q["solution"].replace(" ", ""), frag

# ---------------------------------------------------------------- figures
v0 = w.Venn("v0")
v0.fill("A", ["a", "ab"], "ev")
v0.fill("B", ["b", "ab"], "ev")
v0.fill("x", ["ab"], "warn")
v0.text("tx", "ab", "×2", cls="big")

v1 = w.Venn("v1")
v1.fill("un", ["a", "ab", "b"], "ev")
v1.fill("no", ["o"], "alt")
v1.fill("df", ["a"], "warn")
v1.fill("one", ["a", "b"], "warn")
v1.text("ab", "ab", w.dec(CELLS["ab"]))
v1.text("a", "a", w.dec(CELLS["a"]))
v1.text("b", "b", w.dec(CELLS["b"]))
v1.text("o", (600, 400), w.dec(CELLS["o"]))

v2 = w.Venn("v2", names=("A₃", "A₄"))
v2.text("ab", "ab", f"{c12}", cls="big")
v2.text("a", "a", f"{c3 - c12}", cls="big")
v2.text("b", "b", f"{c4 - c12}", cls="big")

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>בוחרים מספר תלת-ספרתי באקראי. '
        '$A_2,A_4,A_8$: המספר מתחלק ב-2, ב-4, ב-8. מצאו את $P(A_2)$, $P(A_4)$ ו-$P(A_8)$.</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחשב הסתברויות של מאורעות מורכבים, בלי לספור כל תוצאה מחדש."),
    P("משלים, איחוד, הפרש ובדיוק אחד, ואיך סופרים מספרים שמתחלקים במספר נתון."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">E02 · מאורעות</div><h1>משלים, הכלה והפרדה</h1>'
         '<p>לחשב הסתברות של איחוד, של משלים, של הפרש ושל "בדיוק אחד", ולספור מכפלות של מספר בטווח.</p>',
   layout="title")

idea = Scene("idea", "שני הכללים", [
    P("הכלל הראשון הוא המשלים: המאורע ומשלימו מכסים יחד את כל אומגה, בלי חפיפה.", do=show("i-1")),
    P("לכן ההסתברות של לא $A$ היא אחת פחות ההסתברות של $A$.",
      say="לכן ההסתברות של לא אֵיי היא אחת פחות ההסתברות של אֵיי.", hold=0.3),
    P("הכלל השני הוא האיחוד. נחבר את ההסתברות של $A$...", say="הכלל השני הוא האיחוד. נחבר את ההסתברות של אֵיי...",
      do=show("v0-A")),
    P("...ועוד ההסתברות של $B$. מה קרה בחיתוך?", say="ועוד ההסתברות של בִּי. מה קרה בחיתוך?", do=show("v0-B")),
    P("התוצאות של החיתוך נספרו פעמיים: פעם בתוך $A$, ופעם בתוך $B$.",
      say="התוצאות של החיתוך נספרו פעמיים: פעם בתוך אֵיי, ופעם בתוך בִּי.", do=show("v0-x", "v0-tx")),
    P("ולכן מחסירים אותו פעם אחת. זה כלל ההכלה וההפרדה.", do=show("i-2"),
      say="ולכן מחסירים אותו פעם אחת. זה כלל ההכלה וההפרדה."),
    P("ההסתברות של האיחוד שווה לסכום ההסתברויות, פחות ההסתברות של החיתוך.", hold=0.3),
    P("ואם $A$ ו-$B$ זרים? החיתוך ריק, ואז מותר פשוט לחבר.", say="ואם אֵיי ובִּי זרים? החיתוך ריק, ואז מותר פשוט לחבר.",
      do=show("i-3"), hold=0.4),
], stage=f'<div class="ev-stack">{v0.svg()}</div>',
   panel=st.card("i-1", "rule", "🔑 $P(\\overline{A})=1-P(A)$")
         + st.card("i-2", "rule", "🔑 $P(A\\cup B)=P(A)+P(B)-P(A\\cap B)$")
         + st.card("i-3", "plain", "זרים: $P(A\\cup B)=P(A)+P(B)$"))

rules = Scene("rules", "דוגמה: עוד שלושה כללים", [
    P("דוגמה. בחברה גדולה, שישים אחוז מהעובדים דוברים אנגלית, וארבעים וחמישה אחוז דוברים ערבית.", do=show("r-0")),
    P("ועשרים וחמישה אחוז דוברים את שתי השפות. בוחרים עובד באקראי.", hold=0.2),
    P("קודם כל נמלא את הציור. החיתוך: אפס נקודה עשרים וחמש.", do=show("v1-ab")),
    P("רק אנגלית: שישים אחוז פחות החיתוך, כלומר אפס נקודה שלושים וחמש. רק ערבית: אפס נקודה עשרים.",
      do=show("v1-a", "v1-b")),
    P("**לפחות שפה אחת**: שש עשיריות, ועוד ארבעים וחמש מאיות, פחות עשרים וחמש מאיות. יוצא אפס נקודה שמונה.",
      do=show("v1-un", "r-1")),
    P("**אף שפה**: המשלים של האיחוד. אחת פחות אפס נקודה שמונה, כלומר אפס נקודה שתיים.",
      do=hide("v1-un") + show("v1-no", "v1-o", "r-2")),
    P("**אנגלית אבל לא ערבית**, ההפרש: מ-$A$ מורידים את החלק שגם ב-$B$. אפס נקודה שלושים וחמש.",
      say="אנגלית אבל לא ערבית, ההפרש: מאֵיי מורידים את החלק שגם בבִּי. אפס נקודה שלושים וחמש.",
      do=hide("v1-no") + show("v1-df", "r-3")),
    P("ו**בדיוק שפה אחת**: כאן מחסירים את החיתוך **פעמיים**.", do=hide("v1-df") + show("v1-one", "r-4")),
    P("פעם אחת כי נספר פעמיים, ועוד פעם כי הוא בכלל לא חלק מבדיוק אחד. יוצא אפס נקודה חמישים וחמש.", hold=0.3),
    P("בדיקה: שתי הסתברויות האזורים בציור, אפס נקודה שלושים וחמש ועוד אפס נקודה עשרים. נכון, אפס נקודה חמישים וחמש."),
    P("והמלכודת: לחבר שישים ועוד ארבעים וחמש אחוז. מקבלים מאה וחמישה אחוז, וזו כבר לא הסתברות.",
      do=hide("v1-one") + show("r-t"), hold=0.4),
], stage=f'<div class="ev-stack">{v1.svg()}</div>',
   panel=st.card("r-0", "plain", "$P(A)=0.6,\\ P(B)=0.45,\\ P(A\\cap B)=0.25$")
         + st.card("r-1", "ex", "לפחות אחת: $0.6+0.45-0.25=0.8$")
         + st.card("r-2", "ex", "אף אחת: $1-0.8=0.2$")
         + st.card("r-3", "ex", "הפרש: $P(A)-P(A\\cap B)=0.35$")
         + st.card("r-4", "rule", "🔑 בדיוק אחד: $P(A)+P(B)-2P(A\\cap B)=0.55$")
         + st.card("r-t", "trap", "⚠️ $P(A)+P(B)=1.05$: החיתוך נספר פעמיים"))

count_ = Scene("count", "ספירת מכפלות", [
    P("נושא שחוזר במבחנים: כמה מספרים בטווח מתחלקים במספר נתון?"),
    P("הנוסחה: החלק השלם של הקצה העליון חלקי $k$, פחות החלק השלם של המספר שלפני הקצה התחתון, חלקי $k$.",
      say="הנוסחה: החלק השלם של הקצה העליון חלקי קֵיי, פחות החלק השלם של המספר שלפני הקצה התחתון, חלקי קֵיי.",
      do=show("c-1")),
    P("למה? הראשון סופר את כל המכפלות מאחת ועד הסוף. השני מוריד את אלה שקטנות מהטווח.", hold=0.3),
    P("דוגמה: בוחרים מספר דו-ספרתי, מעשר עד תשעים ותשע. תשעים מספרים.", do=show("c-2")),
    P("מתחלקים בשלוש: שלושים ושלוש פחות שלוש, כלומר שלושים.", do=show("c-3")),
    P("מתחלקים בארבע: עשרים וארבע פחות שתיים, כלומר עשרים ושתיים.", do=show("c-4")),
    P("ומתחלקים גם בשלוש וגם בארבע? זה בדיוק מתחלקים בשתים עשרה: שמונה מספרים.", do=show("c-5", "v2-ab")),
    P("בציור: שמונה בחיתוך, עשרים ושניים רק בשלוש, וארבעה עשר רק בארבע.", do=show("v2-a", "v2-b")),
    P("האיחוד: שלושים ועוד עשרים ושתיים פחות שמונה, כלומר ארבעים וארבעה. ההסתברות: ארבעים וארבעה חלקי תשעים.",
      do=show("c-6")),
    P("שזה עשרים ושתיים חלקי ארבעים וחמש. בלי להחסיר את החיתוך היינו מקבלים יותר מדי.", hold=0.4),
], stage=f'<div class="ev-stack">{v2.svg()}</div>',
   panel=st.card("c-1", "rule", "🔑 $\\left\\lfloor \\frac{b}{k}\\right\\rfloor-\\left\\lfloor \\frac{a-1}{k}\\right\\rfloor$ מכפלות של $k$ בין $a$ ל-$b$")
         + st.card("c-2", "plain", "$\\Omega=\\{10,\\dots,99\\}$, $\\;|\\Omega|=90$")
         + st.card("c-3", "ex", "$|A_3|=33-3=30$")
         + st.card("c-4", "ex", "$|A_4|=24-2=22$")
         + st.card("c-5", "ex", "$|A_3\\cap A_4|=|A_{12}|=8$")
         + st.card("c-6", "rule", "🔑 $P=\\frac{30+22-8}{90}=\\frac{44}{90}=\\frac{22}{45}$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. בוחרים באקראי מספר תלת-ספרתי.", do=show("x-stem")),
    P("המאורעות: המספר מתחלק בשתיים, בארבע ובשמונה. צריך את שלוש ההסתברויות."),
    P("מרחב המדגם: מאה עד תשע מאות תשעים ותשע. תשע מאות מספרים.", do=show("x-1")),
    P("מתחלקים בשתיים: ארבע מאות תשעים ותשע, פחות ארבעים ותשע. ארבע מאות וחמישים, כלומר חצי.", do=show("x-2")),
    P("מתחלקים בארבע: מאתיים ארבעים ותשע, פחות עשרים וארבע. מאתיים עשרים וחמש, כלומר רבע.", do=show("x-3")),
    P("ומתחלקים בשמונה: מאה עשרים וארבע, פחות שתים עשרה. מאה ושתים עשרה.", do=show("x-4")),
    P("ההסתברות: מאה ושתים עשרה חלקי תשע מאות, כלומר עשרים ושמונה חלקי מאתיים עשרים וחמש.", do=show("x-5"), hold=0.3),
    P("וזו המלכודת של הסעיף: התשובה **אינה** שמינית.", do=show("x-t")),
    P("תשע מאות חלקי שמונה הוא מאה ושתים עשרה וחצי, ומספר המכפלות חייב להיות שלם.",
      say="תשע מאות חלקי שמונה הוא מאה ושתים עשרה וחצי, ומספר המכפלות חייב להיות שלם."),
    P("בשתיים ובארבע זה עבד, כי תשע מאות מתחלק בהם. בשמונה לא. לכן תמיד משתמשים בנוסחת הספירה.", hold=0.5),
], stage='<div class="ev-stack"><div class="ev-eqs">'
         '<div id="x-1" class="h">$|\\Omega|=999-100+1=900$</div>'
         '<div id="x-2" class="h">$|A_2|=499-49=450,\\quad P(A_2)=\\frac12$</div>'
         '<div id="x-3" class="h">$|A_4|=249-24=225,\\quad P(A_4)=\\frac14$</div>'
         '<div id="x-4" class="h">$|A_8|=124-12=112$</div>'
         '<div id="x-5" class="h">$P(A_8)=\\frac{112}{900}=\\frac{28}{225}$</div></div></div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-t", "trap", "⚠️ $P(A_8)\\ne\\frac18$: $\\;\\frac{900}{8}=112.5$ אינו מספר שלם"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: משלים, אחת פחות ההסתברות.", do=show("s-1")),
    P("איחוד: מחברים, ומחסירים את החיתוך פעם אחת. בדיוק אחד: מחסירים אותו פעמיים.", do=show("s-2", "s-3")),
    P("הפרש: מורידים את החלק המשותף.", do=show("s-4")),
    P("ומכפלות בטווח: סופרים עם הנוסחה, לא מחלקים את גודל הטווח. נתראה ברמה הבאה.", do=show("s-5"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$P(A\\cup B)=P(A)+P(B)-P(A\\cap B)$</div></div>',
   panel=st.card("s-1", "rule", "🔑 $P(\\overline{A})=1-P(A)$")
         + st.card("s-2", "rule", "🔑 איחוד: חיתוך פעם אחת")
         + st.card("s-3", "rule", "🔑 בדיוק אחד: חיתוך פעמיים")
         + st.card("s-4", "rule", "🔑 $P(A\\setminus B)=P(A)-P(A\\cap B)$")
         + st.card("s-5", "trap", "⚠️ $\\left\\lfloor \\frac{b}{k}\\right\\rfloor-\\left\\lfloor \\frac{a-1}{k}\\right\\rfloor$, לא $\\frac{b-a+1}{k}$"))

VIDEO = Video("E02", "events", "משלים, הכלה והפרדה", [title, idea, rules, count_, exam, recap],
              bank={"25A-A-Q2a": None})
