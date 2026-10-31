# -*- coding: utf-8 -*-
"""W05 · אינדיקטורים: כשלא צריך התפלגות — video script (build: tools/video/vid.py W05).

Source: courses/which_model/C05.js (lesson + goal: the mean of a count without its distribution, as a sum of
indicators, even when they are dependent).
Exam anchor: 25B-B-Q6a (n balls moved at random from urn 1 to urn 2, then one ball drawn from urn 2: P(red)). Its
key step is E[X] for the number of reds moved, which is n*D1/N1 by indicators, and the total probability that is
linear in X. Not a quiz/boss id. 25B-B-Q6b (the Bayes part) is W07's anchor.
Not used on purpose (C05 quiz): the suits in a 5-card hand, 6 balls in 4 boxes (empty boxes), HH pairs in 10 tosses;
the lesson's hearts in 5 cards. Worked examples are new: 8 hats returned at random (E = 1, the distribution itself is
messy: P(no match) is about 0.368), and the cards above the first ace in a shuffled deck (48/5).
The hats are enumerated over all 8! permutations, the aces exactly and by simulation, and the exam formula is checked
exactly against the full hypergeometric sum on a grid of urns and by simulating the literal story.
"""
import itertools
from math import factorial

import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R, hyp

# ---------------------------------------------------------------- example 1: 8 hats
N = 8
cnt = {}
for perm in itertools.permutations(range(N)):
    m = sum(1 for i, j in enumerate(perm) if i == j)
    cnt[m] = cnt.get(m, 0) + 1
assert sum(cnt.values()) == factorial(N)
EM = R(sum(m * c for m, c in cnt.items()), factorial(N))
assert EM == 1
P0 = R(cnt[0], factorial(N))
assert P0 == R(14833, 40320) and w.dec(P0) == "0.368"
assert cnt.get(N - 1, 0) == 0                                  # 7 matches is impossible: the indicators are dependent
SHOW = [2, 1, 7, 3, 0, 5, 6, 4]                                 # one return of the hats (0-based): matches at 2, 4, 6, 7
MATCH = [i for i, j in enumerate(SHOW) if i == j]
assert MATCH == [1, 3, 5, 6] and sorted(SHOW) == list(range(N))

# ---------------------------------------------------------------- example 2: cards above the first ace
EA = 48 * R(1, 5)
assert EA == R(48, 5)
# exact: P(a given non-ace lies above all 4 aces) = 1/5 (5 cards, each equally likely to be first among them)
assert sum(1 for o in itertools.permutations("KAAAA") if o[0] == "K") / sum(1 for _ in itertools.permutations("KAAAA")) == 0.2


def gen_deck(rng, n):
    keys = rng.random((n, 52))
    ace_pos = np.sort(keys[:, :4], axis=1)[:, 0]                # cards 0..3 are the aces
    return {"T": (keys[:, 4:] < ace_pos[:, None]).sum(axis=1)}


def gen_hats(rng, n):
    perm = rng.random((n, N)).argsort(axis=1)
    return {"M": (perm == np.arange(N)).sum(axis=1)}


w.mc(gen_deck, [("E", lambda d: d["T"], EA)], n=200_000)
w.mc(gen_hats, [("E", lambda d: d["M"], 1), ("P0", lambda d: d["M"] == 0, P0)])

# ---------------------------------------------------------------- exam 25B-B-Q6a
Q = BANK["25B-B-Q6a"]
assert "כדור אחד נלקח מהכד השני" in Q["question"] and "\\frac{D_2+n\\dfrac{D_1}{N_1}}{N_2+n}" in Q["solution"]
for N1 in range(2, 8):
    for D1 in range(0, N1 + 1):
        for n in range(1, N1 + 1):
            EX = sum(k * hyp(N1, D1, n, k) for k in range(n + 1))
            assert EX == n * R(D1, N1)                              # indicators: each moved ball red w.p. D1/N1
            for N2, D2 in [(1, 0), (3, 1), (5, 5)]:
                full = sum(R(D2 + k, N2 + n) * hyp(N1, D1, n, k) for k in range(n + 1))
                assert full == (D2 + n * R(D1, N1)) / (N2 + n)
N1, D1, n, N2, D2 = 10, 4, 3, 6, 2
ANS = (D2 + n * R(D1, N1)) / (N2 + n)
assert ANS == R(16, 45)


def gen_two_urns(rng, n_):
    keys = rng.random((n_, N1)).argsort(axis=1)[:, :n]
    X = (keys < D1).sum(axis=1)
    return {"R": rng.random(n_) < (D2 + X) / (N2 + n), "X": X}


w.mc(gen_two_urns, [("red", lambda d: d["R"], ANS), ("EX", lambda d: d["X"], n * R(D1, N1))])

# ---------------------------------------------------------------- figures
HATS = w.seq("ht", [(str(j + 1), "n") for j in SHOW], size=62, shown=True, gap=12)
ACES = w.seq("ac", [("A", "n"), ("A", "n"), ("K", "s"), ("A", "n"), ("A", "n")], size=62, shown=True, nums=False, gap=12)
STEPS = [("1", "מה סופרים?", ""), ("2", "אינדיקטור לכל פריט", ""), ("3", "הסתברות לכל אחד, ומחברים", "")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נראה מתי **לא צריך** מודל בכלל."),
    P("כשמבקשים רק תוחלת של ספירה, אפשר לדלג על ההתפלגות, גם כשהכול תלוי בהכול."),
    P("ובסוף נפתור שאלה ממבחן עם שני כדים.", hold=0.4),
], stage='<div class="kicker">W05 · איזה מודל זה?</div><h1>אינדיקטורים</h1>'
         '<p>תוחלת של ספירה בלי למצוא את ההתפלגות: סכום של אינדיקטורים, גם כשהם תלויים.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("נניח ש-$X$ סופר כמה פריטים מקיימים תנאי. נגדיר לכל פריט אינדיקטור: אחת אם הוא מקיים, אפס אם לא.",
      do=show("i-0"), say="נניח שאִקְס סופר כמה פריטים מקיימים תנאי. נגדיר לכל פריט אינדיקטור: אחת אם הוא מקיים, אפס אם לא."),
    P("אז $X$ הוא סכום האינדיקטורים, והתוחלת של אינדיקטור היא פשוט ההסתברות שהוא אחת.", do=show("i-1"),
      say="אז אִקְס הוא סכום האינדיקטורים, והתוחלת של אינדיקטור היא פשוט ההסתברות שהוא אחת."),
    P("ותוחלת של סכום היא סכום התוחלות. **תמיד**, גם כשהאינדיקטורים תלויים זה בזה.", do=show("i-2", "i-r")),
    P("אז שלושה שלבים: מה סופרים, אינדיקטור לכל פריט, ומחברים את ההסתברויות.",
      do=show("ck-r-1", "ck-r-2", "ck-r-3"), hold=0.4),
], stage='<div class="wm-col">' + w.eqs("i", ["$X=I_1+I_2+\\dots+I_m$", "$E[I_j]=P(I_j=1)$",
                                              "$E[X]=\\sum_j P(I_j=1)$"], size=44, gap=18)
         + w.checklist("ck", STEPS, size=30, hidden=True, width=700) + "</div>",
   panel=st.card("i-r", "rule", "🔑 ליניאריות התוחלת לא דורשת אי תלות"))

hats = Scene("hats", "הכובעים", [
    P("דוגמה. שמונה אנשים מניחים את הכובעים בארגז, וכל אחד לוקח כובע באקראי. כמה יקבלו את הכובע שלהם, בממוצע?",
      do=show("ht")),
    P("כאן, למשל, האדם השני, הרביעי, השישי והשביעי קיבלו את הכובע שלהם.", do=show(*[f"ht-h-{i}" for i in MATCH])),
    P("ההתפלגות של מספר ההתאמות מסובכת, והאנשים תלויים: אם שבעה קיבלו את שלהם, גם השמיני קיבל.",
      do=hide(*[f"ht-h-{i}" for i in MATCH]) + show("h-t")),
    P("אז לא מחפשים מודל. אינדיקטור לכל אדם: אחת אם קיבל את הכובע שלו.", do=show("h-0")),
    P("כל אדם מקבל כל אחד משמונת הכובעים באותה הסתברות, ולכן הסיכוי לשלו הוא שמינית.", do=show("h-1")),
    P("מחברים שמונה פעמים שמינית, ומקבלים אחת. בממוצע אדם אחד מקבל את הכובע שלו.", do=show("h-2", "h-ok")),
    P("ובדיקה מלאה על כל ארבעים אלף הסידורים נותנת בדיוק אחת. בלי לדעת את ההתפלגות.", hold=0.4),
], stage=f'<div class="wm-col" style="gap:40px">{HATS}'
         + w.eqs("h", [r"$X=I_1+\dots+I_8$",
                       "$P(I_j=1)=\\frac18$", "$E[X]=8\\cdot\\frac18=1$"], size=40, gap=14)
         + w.chip("h-ok", "$E[X]=1$ ✓") + "</div>",
   panel=st.card("h-t", "trap", "⚠️ לא בינומית: האינדיקטורים תלויים. אבל לתוחלת זה לא משנה"))

aces = Scene("aces", "לפני האס הראשון", [
    P("דוגמה שנייה. מערבבים חפיסה של חמישים ושניים קלפים. כמה קלפים יופיעו, בממוצע, לפני האס הראשון?"),
    P("אינדיקטור לכל אחד מארבעים ושמונה הקלפים שאינם אס: אחת אם הוא מופיע לפני **כל** ארבעת האסים.", do=show("a-0")),
    P("נסתכל רק על הקלף הזה ועל ארבעת האסים. בסידור אקראי, כל אחד מהחמישה יכול להיות הראשון ביניהם.", do=show("ac")),
    P("ולכן הסיכוי שהקלף שלנו ראשון הוא חמישית.", do=show("ac-h-2", "a-1")),
    P("התוחלת: ארבעים ושמונה כפול חמישית, תשע נקודה שש קלפים.", do=show("a-2", "a-ok")),
    P("שימו לב שלא שאלנו איזה מודל יש למספר הקלפים. רק מה ההסתברות של כל אינדיקטור.", hold=0.4),
], stage=f'<div class="wm-col" style="gap:34px">{ACES}'
         + w.eqs("a", ["$X=\\sum_{c=1}^{48}I_c$", "$P(I_c=1)=\\frac15$", "$E[X]=48\\cdot\\frac15=9.6$"], size=40, gap=14)
         + w.chip("a-ok", "$9.6$ ✓") + "</div>",
   panel=st.card("a-r", "rule", "🔑 הסתברות של אינדיקטור: מסתכלים רק על מה שרלוונטי אליו").replace(' h"', '"'))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. בכד הראשון $N_1$ כדורים, מהם $D_1$ אדומים. בשני $N_2$ כדורים, מהם $D_2$ אדומים.",
      say="ועכשיו שאלה ממבחן. בכד הראשון אֶן אחת כדורים, מהם דִּי אחת אדומים. בשני אֶן שתיים כדורים, מהם דִּי שתיים אדומים."),
    P("מעבירים $n$ כדורים אקראיים מהראשון לשני, ואז שולפים כדור אחד מהשני. מה הסיכוי שהוא אדום?",
      say="מעבירים אֶן כדורים אקראיים מהראשון לשני, ואז שולפים כדור אחד מהשני. מה הסיכוי שהוא אדום?"),
    P("נסמן ב-$X$ את מספר האדומים שעברו. בהינתן $X$ שווה $k$, בכד השני $D_2$ ועוד $k$ אדומים, מתוך $N_2$ ועוד $n$.",
      do=show("x-0"), say="נסמן באִקְס את מספר האדומים שעברו. בהינתן שאִקְס שווה קֵיי, בכד השני דִּי שתיים ועוד קֵיי אדומים, מתוך אֶן שתיים ועוד אֶן."),
    P("הסתברות שלמה: מחברים על כל $k$. אבל הביטוי **ליניארי** ב-$k$, אז הסכום הוא פשוט התוחלת של $X$.",
      do=show("x-1"), say="הסתברות שלמה: מחברים על כל קֵיי. אבל הביטוי ליניארי בקֵיי, אז הסכום הוא פשוט התוחלת של אִקְס."),
    P("ו-$X$ היפרגאומטרי, אבל את התפלגותו לא צריך. אינדיקטור לכל כדור שעבר: הוא אדום בהסתברות $D_1$ חלקי $N_1$.",
      do=show("x-2"), say="ואִקְס היפרגאומטרי, אבל את התפלגותו לא צריך. אינדיקטור לכל כדור שעבר: הוא אדום בהסתברות דִּי אחת חלקי אֶן אחת."),
    P("האינדיקטורים תלויים, כי השליפה בלי החזרה. ובכל זאת התוחלת היא $n$ כפול $D_1$ חלקי $N_1$.", do=show("x-3"),
      say="האינדיקטורים תלויים, כי השליפה בלי החזרה. ובכל זאת התוחלת היא אֶן כפול דִּי אחת חלקי אֶן אחת."),
    P("ומציבים. למשל עשרה כדורים, ארבעה אדומים, מעבירים שלושה לכד של שישה עם שני אדומים: שש עשרה חלקי ארבעים וחמש.",
      do=show("x-4", "x-ok")),
    P("המלכודת: לפתוח את הסכום ההיפרגאומטרי עם מקדמי הבינום. זה אפשרי, אבל ארוך, ומלא בהזדמנויות לטעות.",
      do=show("x-t"), hold=0.4),
], stage='<div class="wm-col" style="gap:12px">' + w.eqs("x", [
    "$P(R\\mid X=k)=\\dfrac{D_2+k}{N_2+n}$",
    "$P(R)=\\sum_k\\dfrac{D_2+k}{N_2+n}P(X=k)=\\dfrac{D_2+E[X]}{N_2+n}$",
    "$X=\\sum_{j=1}^{n}I_j,\\quad P(I_j=1)=\\dfrac{D_1}{N_1}$",
    "$E[X]=n\\dfrac{D_1}{N_1}$",
    "$P(R)=\\dfrac{D_2+n\\dfrac{D_1}{N_1}}{N_2+n}$"], size=34, gap=14)
         + w.chip("x-ok", r"$\frac{2+3\cdot\frac{4}{10}}{6+3}=\frac{16}{45}$ ✓") + "</div>",
   panel=w.stem(Q["id"], "בכד הראשון $N_1$ כדורים, מהם $D_1$ אדומים. בשני $N_2$, מהם $D_2$ אדומים. "
                "מעבירים $n$ כדורים אקראיים מהראשון לשני, ואז לוקחים כדור אחד מהשני. מה ההסתברות שהוא אדום?", size=28)
         + st.card("x-t", "trap", "⚠️ אין צורך בסכום ההיפרגאומטרי המלא"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: אם מבקשים רק תוחלת של ספירה, לא מחפשים מודל.", do=show("r-1")),
    P("מפרקים לאינדיקטורים, מוצאים לכל אחד את ההסתברות, ומחברים.", do=show("r-2")),
    P("וזה עובד גם כשהם תלויים, כי תוחלת היא ליניארית. התלות משפיעה על השונות, לא על התוחלת.", do=show("r-3")),
    P("נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="wm-col">' + w.eqs("r", ["$E[X]=\\sum_j P(I_j=1)$"], size=48, shown=1) + "</div>",
   panel=st.card("r-1", "rule", "🔑 רק תוחלת: בלי התפלגות")
         + st.card("r-2", "rule", "🔑 מה סופרים, אינדיקטור, מחברים")
         + st.card("r-3", "trap", "⚠️ תלות משנה את השונות, לא את התוחלת"))

VIDEO = Video("W05", "which_model", "אינדיקטורים: כשלא צריך התפלגות", [title, idea, hats, aces, exam, recap],
              bank={"25B-B-Q6a": None})
