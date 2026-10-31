# -*- coding: utf-8 -*-
"""W07 · הסתברות שלמה, בייס או ספירה ישירה — video script (build: tools/video/vid.py W07).

Source: courses/which_model/C07.js (lesson + goal: asking about the outcome -> total probability; the outcome is
known and the question is about the cause -> Bayes; one equally likely space -> plain counting).
Exam anchor: 25B-B-Q6b (n balls moved from urn 1 to urn 2, a red ball drawn from urn 2: the probability that all n
moved balls were red). Not a quiz/boss id. Its denominator P(red) is 25B-B-Q6a (W05's anchor), quoted here.
Not used on purpose (C07 quiz): a fair coin and a 0.8 coin, the 1% disease test with 0.95 / 0.05, urns A (3R+1B) and
B (1R+3B) with two draws; the lesson's coin example. Also not used: 24A-B-Q2b (an events-course quiz item, sums of
two dice given the sum). Worked examples are new: three machines making 50/30/20% of the items with 1/2/5% defects
(P(D) = 0.021, P(C | D) = 10/21), and two cards out of ten numbered 1..10 given the sum is 11 (1/5 by counting).
Every value is exact (Fractions / sympy) and simulated literally (numpy); the exam formula is checked exactly on a
grid of urns against a direct joint computation.
"""
import itertools

import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R, hyp

# ---------------------------------------------------------------- example 1: three machines
PM = {"A": R(1, 2), "B": R(3, 10), "C": R(1, 5)}
PD = {"A": R(1, 100), "B": R(2, 100), "C": R(5, 100)}
PDt = sum(PM[m] * PD[m] for m in PM)
assert [PM[m] * PD[m] for m in PM] == [R(5, 1000), R(6, 1000), R(10, 1000)] and PDt == R(21, 1000)
PCD = PM["C"] * PD["C"] / PDt
assert PCD == R(10, 21) and w.dec(PCD) == "0.476"
assert PCD > PM["C"]                                            # seeing a defect raises the weight of the bad machine


def gen_mach(rng, n):
    m = rng.choice(3, n, p=[0.5, 0.3, 0.2])
    d = rng.random(n) < np.array([0.01, 0.02, 0.05])[m]
    return {"m": m, "d": d}


w.mc(gen_mach, [("PD", lambda d: d["d"], PDt), ("C&D", lambda d: (d["m"] == 2) & d["d"], R(10, 1000))], n=1_000_000)
_r = np.random.default_rng(11)
_d = gen_mach(_r, 2_000_000)
_cond = _d["m"][_d["d"]] == 2
assert abs(_cond.mean() - float(PCD)) < 5 * _cond.std() / np.sqrt(len(_cond))

# ---------------------------------------------------------------- example 2: two of ten cards, the sum is 11
pairs = list(itertools.combinations(range(1, 11), 2))
given = [pr for pr in pairs if sum(pr) == 11]
assert len(pairs) == 45 and len(given) == 5 and R(sum(1 for pr in given if 1 in pr), len(given)) == R(1, 5)

# ---------------------------------------------------------------- exam 25B-B-Q6b
Q = BANK["25B-B-Q6b"]
assert "אם ידוע כי צבעו של הכדור שנלקח מהכד השני היה אדום" in Q["question"]
assert "\\frac{D_2+n}{D_2+n\\dfrac{D_1}{N_1}}\\cdot\\frac{\\binom{D_1}{n}}{\\binom{N_1}{n}}" in Q["solution"]


def bayes_formula(N1, D1, n, N2, D2):
    return R(D2 + n) / (D2 + n * R(D1, N1)) * hyp(N1, D1, n, n)


for N1 in range(2, 7):
    for D1 in range(0, N1 + 1):
        for n in range(1, N1 + 1):
            for N2, D2 in [(2, 1), (4, 0), (3, 3)]:
                pred = sum(R(D2 + k, N2 + n) * hyp(N1, D1, n, k) for k in range(n + 1))
                if pred == 0:
                    continue
                joint = R(D2 + n, N2 + n) * hyp(N1, D1, n, n)
                assert joint / pred == bayes_formula(N1, D1, n, N2, D2)
N1, D1, n, N2, D2 = 6, 4, 2, 5, 1
ANS = bayes_formula(N1, D1, n, N2, D2)
PRIOR = hyp(N1, D1, n, n)
assert PRIOR == R(6, 15) == R(2, 5) and ANS == R(3, 1) / (1 + 2 * R(4, 6)) * R(2, 5) == R(18, 35) and ANS > PRIOR and w.dec(ANS) == "0.514"


def gen_ex(rng, n_):
    keys = rng.random((n_, N1)).argsort(axis=1)[:, :n]
    X = (keys < D1).sum(axis=1)
    red = rng.random(n_) < (D2 + X) / (N2 + n)
    return {"X": X, "red": red}


_e = gen_ex(np.random.default_rng(3), 1_000_000)
_c = (_e["X"][_e["red"]] == n)
assert abs(_c.mean() - float(ANS)) < 5 * _c.std() / np.sqrt(len(_c))

# ---------------------------------------------------------------- figures
CK = [("tot", "שואלים על **התוצאה**, והשלב הראשון לא ידוע", "שלמה"),
      ("bay", "״ידוע ש...״ התוצאה קרתה, ושואלים על **הסיבה**", "בייס"),
      ("cnt", "מרחב אחד שבו כל התוצאות שוות סיכוי", "ספירה")]
CK = [(k, q.replace("**", "<b>", 1).replace("**", "</b>", 1), a) for k, q, a in CK]
CARDS = w.seq("cd", [(f"{a}+{b}", "s" if 1 in (a, b) else "n") for a, b in given], size=90, wide=150, fs=44, shown=True, nums=False, gap=14)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לבחור כלי: הסתברות שלמה, בייס, או פשוט ספירה."),
    P("ההכרעה תלויה במה שהשאלה יודעת, ובמה שהיא שואלת."),
    P("ובסוף נפתור שאלת בייס אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">W07 · איזה מודל זה?</div><h1>שלמה, בייס או ספירה?</h1>'
         '<p>שואלים על התוצאה: הסתברות שלמה. התוצאה ידועה ושואלים על הסיבה: בייס. מרחב שווה סיכוי: ספירה.</p>',
   layout="title")

mach = Scene("mach", "שלוש מכונות", [
    P("במפעל שלוש מכונות. מכונה א׳ מייצרת חצי מהמוצרים, ב׳ שלושים אחוז, וג׳ עשרים אחוז.", do=show("m-0")),
    P("אחוז הפגומים: אחד, שניים וחמישה, בהתאמה. שתי שאלות על אותו סיפור.", do=show("m-1")),
    P("שאלה ראשונה: מוצר אקראי. מה הסיכוי שהוא פגום? המכונה לא ידועה, ושואלים על **התוצאה**.",
      do=show("ck-r-tot", "ck-on-tot", "ck-a-tot")),
    P("הסתברות שלמה: מפצלים לפי המכונה, ומחברים שלושה מסלולים. יוצא אפס נקודה אפס עשרים ואחת.", do=show("m-2", "m-3")),
    P("שאלה שנייה: **ידוע** שהמוצר פגום. מה הסיכוי שהוא ממכונה ג׳? עכשיו התוצאה ידועה, ושואלים על **הסיבה**.",
      do=show("ck-r-bay", "ck-on-bay", "ck-a-bay")),
    P("בייס: המסלול של ג׳ חלקי כל המסלולים. עשר חלקי עשרים ואחת, כמעט חצי.", do=show("m-4")),
    P("שימו לב: המכנה של בייס הוא בדיוק התשובה לשאלה הראשונה. ההסתברות השלמה היא תמיד חלק מבייס.", do=show("m-r")),
    P("ומכונה ג׳, שמייצרת רק חמישית, אחראית לכמעט חצי מהפגומים. כי היא הגרועה.", hold=0.4),
], stage=f'<div class="wm-col">{w.checklist("ck", CK, size=30, hidden=True, width=980)}</div>',
   panel=w.eqs("m", ["$P(A,B,C)=0.5,\\ 0.3,\\ 0.2$", "$P(D\\mid\\cdot)=0.01,\\ 0.02,\\ 0.05$",
                     "$P(D)=0.005+0.006+0.010$", "$=0.021$",
                     "$P(C\\mid D)=\\dfrac{0.010}{0.021}=\\dfrac{10}{21}\\approx0.476$"], size=32, gap=10)
         + st.card("m-r", "rule", "🔑 המכנה של בייס הוא ההסתברות השלמה"))

count = Scene("count", "לפעמים די בספירה", [
    P("ולפעמים לא צריך אף נוסחה. שולפים שני קלפים מתוך עשרה, ממוספרים מאחת עד עשר."),
    P("**ידוע** שסכום שני הקלפים הוא אחת עשרה. מה הסיכוי שאחד מהם הוא אחת?"),
    P("המילה ״ידוע״ מזמינה את בייס, אבל כל זוגות הקלפים שווי סיכוי. אז פשוט מצמצמים את המרחב.",
      do=show("c-r")),
    P("יש חמישה זוגות שסכומם אחת עשרה.", do=show("cdw")),
    P("ורק באחד מהם יש את הקלף אחת. התשובה: חמישית.", do=show("cd-h-0", "c-0")),
    P("בייס היה נותן אותה תשובה, אבל בדרך ארוכה יותר. כשהמרחב שווה סיכוי, סופרים.", hold=0.4),
], stage=f'<div class="wm-col" style="gap:30px"><div id="cdw" class="h">{CARDS}</div>'
         + w.eqs("c", ["$P=\\frac15$"], size=48) + "</div>",
   panel=st.card("c-r", "rule", "🔑 ״ידוע ש...״ במרחב שווה סיכוי: מצמצמים את המרחב וסופרים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. שוב שני הכדים: מעבירים $n$ כדורים מהכד הראשון לשני, ושולפים כדור מהשני.",
      say="ועכשיו שאלה ממבחן. שוב שני הכדים: מעבירים אֶן כדורים מהכד הראשון לשני, ושולפים כדור מהשני."),
    P("**ידוע** שהכדור שנשלף אדום. מה הסיכוי שכל הכדורים שהועברו היו אדומים?"),
    P("זיהוי: התוצאה ידועה, ושואלים על מה שקרה קודם, על הסיבה. בייס.", do=show("x-pill")),
    P("המונה: הסיכוי שכולם אדומים, כפול הסיכוי לאדום בהינתן זה.", do=show("x-0")),
    P("ש$X$ שווה $n$: היפרגאומטרית, בוחרים את כל ה-$n$ מתוך האדומים.", do=show("x-1"),
      say="שאִקְס שווה אֶן: היפרגאומטרית, בוחרים את כל האֶן מתוך האדומים."),
    P("ואם כולם אדומים, בכד השני $D_2$ ועוד $n$ אדומים מתוך $N_2$ ועוד $n$.", do=show("x-2"),
      say="ואם כולם אדומים, בכד השני דִּי שתיים ועוד אֶן אדומים, מתוך אֶן שתיים ועוד אֶן."),
    P("המכנה: הסיכוי לאדום בכלל. זו ההסתברות השלמה, שחישבנו בעזרת התוחלת של $X$.", do=show("x-3"),
      say="המכנה: הסיכוי לאדום בכלל. זו ההסתברות השלמה, שחישבנו בעזרת התוחלת של אִקְס."),
    P("מחלקים, והמכנה $N_2$ ועוד $n$ מצטמצם.", do=show("x-4"),
      say="מחלקים, והמכנה, אֶן שתיים ועוד אֶן, מצטמצם."),
    P("במספרים: בכד הראשון שישה כדורים, ארבעה אדומים, ובשני חמישה כדורים, אחד אדום. מעבירים שניים.",
      do=show("x-5")),
    P("בלי שום מידע, הסיכוי ששני הכדורים שעברו אדומים הוא שתי חמישיות."),
    P("ואחרי שראינו אדום, הסיכוי עולה לשמונה עשרה חלקי שלושים וחמש, יותר מחצי. אדום מחזק את ההשערה שעברו אדומים.",
      do=show("x-6", "x-ok")),
    P("המלכודת: לענות רק בסיכוי שכולם אדומים, בלי התנאי. זו ההסתברות **לפני** שראינו את הכדור.", do=show("x-t"),
      hold=0.4),
], stage='<div class="wm-col" style="gap:10px">'
         + w.eqs("x", ["$P(X=n\\mid R)=\\dfrac{P(R\\mid X=n)\\,P(X=n)}{P(R)}$",
                       "$P(X=n)=\\dfrac{\\binom{D_1}{n}}{\\binom{N_1}{n}}$",
                       "$P(R\\mid X=n)=\\dfrac{D_2+n}{N_2+n}$",
                       "$P(R)=\\dfrac{D_2+n\\frac{D_1}{N_1}}{N_2+n}$",
                       "$P(X=n\\mid R)=\\dfrac{D_2+n}{D_2+n\\frac{D_1}{N_1}}\\cdot\\dfrac{\\binom{D_1}{n}}{\\binom{N_1}{n}}$",
                       "$N_1=6,\\ D_1=4,\\ n=2,\\ N_2=5,\\ D_2=1:\\ \\ P(X=2)=\\frac25$",
                       "$P(X=2\\mid R)=\\frac{3}{1+2\\cdot\\frac46}\\cdot\\frac25=\\frac{18}{35}\\approx0.514$"], size=29, gap=6)
         + "</div>",
   panel=w.stem(Q["id"], "מעבירים $n$ כדורים אקראיים מכד ראשון ($N_1$ כדורים, $D_1$ אדומים) לשני ($N_2$, $D_2$), "
                "ולוקחים כדור מהשני. ידוע שהוא אדום. מה ההסתברות שכל $n$ הכדורים שהועברו היו אדומים?", size=28)
         + w.pill("x-pill", "בייס: ידוע אדום")
         + st.card("x-t", "trap", "⚠️ $P(X=n)$ לבד: זה לפני התצפית")
         + w.chip("x-ok", "סימולציה: $\\approx0.514$ ✓"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: שואלים על התוצאה, והשלב הראשון לא ידוע: הסתברות שלמה.", do=show("r-1")),
    P("התוצאה ידועה ושואלים על הסיבה: בייס, והמכנה שלו הוא ההסתברות השלמה.", do=show("r-2")),
    P("ואם כל התוצאות שוות סיכוי, מצמצמים את המרחב וסופרים. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=f'<div class="wm-col">{w.checklist("rk", CK, size=30, width=980)}</div>',
   panel=st.card("r-1", "rule", "🔑 $P(A)=\\sum_i P(A\\mid B_i)P(B_i)$")
         + st.card("r-2", "rule", "🔑 $P(B_i\\mid A)=\\dfrac{P(A\\mid B_i)P(B_i)}{P(A)}$")
         + st.card("r-3", "trap", "⚠️ $P(A\\mid B)\\ne P(B\\mid A)$"))

VIDEO = Video("W07", "which_model", "הסתברות שלמה, בייס או ספירה ישירה", [title, mach, count, exam, recap],
              bank={"25B-B-Q6b": None})
