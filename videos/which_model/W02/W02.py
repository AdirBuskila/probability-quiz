# -*- coding: utf-8 -*-
"""W02 · עד מתי מטילים? גאומטרית ובינומית שלילית — video script (build: tools/video/vid.py W02).

Source: courses/which_model/C02.js (lesson + goal: read the stopping rule; a fixed number of trials counts successes
(binomial), stopping at the first / m-th success counts trials (geometric / negative binomial)).
Exam anchors: 26A-A-Q2a and 26A-A-Q2b (two players toss equal biased coins until the first head; the tie has
probability Q; who wins, and p from Q). Neither is a quiz/boss id. Not used on purpose: 26A-B-Q2b (the boss item:
first head on an even toss) and its sibling 26A-B-Q2c (that one is W08's anchor).
Not used on purpose (C02 quiz): a die until the first 6 at roll 4, 10 free throws with p = 0.3, the third hit at
throw 6 with p = 0.4; the lesson's fair coin with the first head at toss 3. Worked examples are new: a shooter with
p = 1/4 and the same five shots read three ways (Bin(5, 1/4): exactly one hit; G(1/4): first hit at shot 5;
NegBin(2, 1/4): second hit at shot 5), then "exactly at k" vs "at most k" (P(X <= 3) = 1 - (3/4)^3).
Every value is exact (sympy) and the stories are simulated literally (numpy) within 5 standard errors.
"""
import itertools

import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R, binom, geo, nbin

# ---------------------------------------------------------------- shooter, p = 1/4, five shots
p0 = R(1, 4)
B1 = binom(5, p0, 1)
G5 = geo(p0, 5)
N5 = nbin(2, p0, 5)
assert B1 == R(405, 1024) and G5 == R(81, 1024) and N5 == R(108, 1024)
assert B1 == 5 * G5                                           # five places for the single hit; geometric keeps one
ARR = [s for s in itertools.product("FS", repeat=5) if s.count("S") == 1]
assert len(ARR) == 5 and ARR[0] == tuple("FFFFS")              # the arrangement with the hit last comes first
NB = [s for s in itertools.product("FS", repeat=5) if s.count("S") == 2 and s[-1] == "S"]
assert len(NB) == 4 == sp.binomial(4, 1)                      # one hit among the first four, then a hit
assert sum(p0 ** 2 * (1 - p0) ** 3 for _ in NB) == N5
assert 1 / p0 == 4 and 2 / p0 == 8                           # E[G] = 1/p, E[NegBin] = m/p
ATMOST3 = sum(geo(p0, k) for k in range(1, 4))
assert ATMOST3 == 1 - (1 - p0) ** 3 == R(37, 64)
assert geo(p0, 3) == R(9, 64)


def first_success(rng, n, p, m=1, cap=400):
    hits = rng.random((n, cap)) < p
    c = np.cumsum(hits, axis=1)
    return (c >= m).argmax(axis=1) + 1


def gen_shots(rng, n):
    return {"B": (rng.random((n, 5)) < 0.25).sum(axis=1), "G": first_success(rng, n, 0.25),
            "N": first_success(rng, n, 0.25, m=2)}


w.mc(gen_shots, [("bin1", lambda d: d["B"] == 1, B1), ("geo5", lambda d: d["G"] == 5, G5),
                 ("nb5", lambda d: d["N"] == 5, N5), ("le3", lambda d: d["G"] <= 3, ATMOST3),
                 ("EG", lambda d: d["G"], 4), ("EN", lambda d: d["N"], 8)])

# ---------------------------------------------------------------- exam 26A-A-Q2
QA, QB = BANK["26A-A-Q2a"], BANK["26A-A-Q2b"]
CT = w.ctx_text(QA)
assert "עד קבלת התוצאה ״עץ״ בפעם הראשונה" in CT and "ההסתברות לתיקו במשחק היא $Q$" in CT
assert r"P_E=P_B=\frac{1-Q}{2}" in QA["solution"] and r"p=\frac{2Q}{1+Q}" in QB["solution"]
p, k, Qs = sp.symbols("p k Q", positive=True)
tie = p ** 2 / (1 - (1 - p) ** 2)                               # geometric series with ratio (1-p)^2 < 1
assert sp.simplify(tie - p / (2 - p)) == 0
for pv in [R(1, 10), R(1, 2), R(9, 10)]:                        # the series itself, summed far out
    assert abs(float(sum(pv ** 2 * ((1 - pv) ** 2) ** (j - 1) for j in range(1, 300))) - float(tie.subs(p, pv))) < 1e-12
assert sp.solve(sp.Eq(Qs, p / (2 - p)), p) == [2 * Qs / (Qs + 1)]
for pv in [R(1, 10), R(3, 10), R(1, 2), R(9, 10)]:
    Qv = pv / (2 - pv)
    assert 0 < Qv <= 1 and 2 * Qv / (1 + Qv) == pv
    win = sum(geo(pv, j) * (1 - pv) ** j for j in range(1, 400))     # Eugene's first head strictly earlier
    assert abs(float(win) - float((1 - Qv) / 2)) < 1e-12
assert R(3, 10) / (2 - R(3, 10)) == R(3, 17)


def gen_race(rng, n):
    return {"A": first_success(rng, n, 0.3), "B": first_success(rng, n, 0.3)}


w.mc(gen_race, [("tie", lambda d: d["A"] == d["B"], R(3, 17)), ("winA", lambda d: d["A"] < d["B"], (1 - R(3, 17)) / 2)])

# ---------------------------------------------------------------- figures
SYM = {"S": ("✓", "s"), "F": ("✗", "f")}
ROWS = "".join(f'<div class="wm-rowx" style="gap:18px">' + w.seq(f"a{i}", [SYM[c] for c in s], size=46, shown=True,
                                                                     nums=(i == 4), gap=8) + "</div>"
               for i, s in enumerate(ARR))
NBS = w.seq("nb", [SYM[c] for c in "FSFFS"], size=46, shown=True, gap=8)
CK = [("n", "מספר הניסויים קבוע, וסופרים הצלחות", "בינומית"),
      ("g", "עוצרים בהצלחה הראשונה, וסופרים ניסויים", "גאומטרית"),
      ("m", "עוצרים בהצלחה ה-$m$, וסופרים ניסויים", "בינומית שלילית")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לקרוא את **כלל העצירה** של ניסוי."),
    P("הוא מה שמבדיל בין בינומית, גאומטרית ובינומית שלילית."),
    P("ובסוף נפתור שאלה ממבחן על משחק בין שני שחקנים.", hold=0.4),
], stage='<div class="kicker">W02 · איזה מודל זה?</div><h1>עד מתי מטילים?</h1>'
         '<p>לזהות לפי כלל העצירה אם סופרים הצלחות (בינומית) או ניסויים (גאומטרית, בינומית שלילית).</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("בשלושת המודלים יש רצף של ניסויים בלתי תלויים, ובכל אחד הצלחה בהסתברות $p$.",
      say="בשלושת המודלים יש רצף של ניסויים בלתי תלויים, ובכל אחד הצלחה בהסתברות פִּי."),
    P("ההבדל הוא מה קבוע ומה אקראי. אם מספר הניסויים קבוע מראש, סופרים הצלחות: בינומית.",
      do=show("ck-r-n", "ck-on-n", "ck-a-n", "i-0")),
    P("אם ממשיכים **עד** ההצלחה הראשונה, המשתנה הוא מספר הניסויים: גאומטרית.",
      do=show("ck-r-g", "ck-on-g", "ck-a-g", "i-1")),
    P("ואם ממשיכים עד ההצלחה ה-$m$, זו בינומית שלילית.", do=show("ck-r-m", "ck-on-m", "ck-a-m", "i-2"),
      say="ואם ממשיכים עד ההצלחה ה-אֶם, זו בינומית שלילית."),
    P("כלומר בבינומית ההצלחות אקראיות. בשני האחרים מספר ההצלחות קבוע, ואורך הרצף אקראי.", do=show("i-k"), hold=0.4),
], stage=f'<div class="wm-col">{w.checklist("ck", CK, size=32, hidden=True, width=920)}</div>',
   panel=w.eqs("i", ["$\\mathrm{Bin}(n,p):\\ \\binom nk p^k(1-p)^{n-k}$", "$G(p):\\ (1-p)^{k-1}p$",
                     "$\\mathrm{NegBin}(m,p):\\ \\binom{k-1}{m-1}p^m(1-p)^{k-m}$"], size=32, gap=22)
         + st.card("i-k", "rule", "🔑 קודם שואלים: מה קבוע, ומה סופרים?"))

shots = Scene("shots", "אותן חמש יריות", [
    P("קלע פוגע במטרה בהסתברות רבע בכל ירייה, בלי תלות. נקרא את אותן חמש יריות בשלוש דרכים."),
    P("ראשונה: הוא יורה בדיוק חמש פעמים. מה הסיכוי לפגיעה אחת בדיוק? זו בינומית.", do=show("s-q1")),
    P("הפגיעה יכולה להיות בכל אחד מחמשת המקומות. חמישה סידורים, ולכן מקדם בינום חמש.",
      do=show(*[f"a{i}-h-{4 - i}" for i in range(5)], "s-0")),
    P("שנייה: הוא יורה **עד** הפגיעה הראשונה. מה הסיכוי שזה יקרה בדיוק בירייה החמישית?",
      do=hide(*[f"a{i}-h-{4 - i}" for i in range(5)]) + show("s-q2")),
    P("כאן רק סידור אחד מתאים: ארבע החטאות, ואז פגיעה. זו גאומטרית, והסיכוי קטן פי חמישה.",
      do=show("a0-w-4", "s-1")),
    P("שלישית: עד הפגיעה **השנייה**. הירייה האחרונה חייבת להיות פגיעה.", do=hide("a0-w-4") + show("s-q3", "nbw", "nb-h-4")),
    P("ובארבע הראשונות פגיעה אחת בדיוק, באחד מארבעה מקומות. זו בינומית שלילית.", do=show("nb-w-1", "s-2")),
    P("אותם נתונים, שלוש תשובות שונות. מה שהכריע הוא רק כלל העצירה.", do=show("s-k"), hold=0.4),
], stage=f'<div class="wm-col" style="gap:10px">{ROWS}<div id="nbw" class="h" style="margin-top:14px">{NBS}</div></div>',
   panel=w.box("s-q1", "חמש יריות קבועות, פגיעה אחת: בינומית", size=26)
         + r'<div id="s-0" class="wm-eq h" style="font-size:30px;direction:ltr">$\binom51\cdot\frac14\left(\frac34\right)^4=\frac{405}{1024}\approx0.396$</div>'
         + w.box("s-q2", "עד הפגיעה הראשונה, בירייה 5: גאומטרית", size=26)
         + r'<div id="s-1" class="wm-eq h" style="font-size:30px;direction:ltr">$\left(\frac34\right)^4\cdot\frac14=\frac{81}{1024}\approx0.079$</div>'
         + w.box("s-q3", "עד הפגיעה השנייה, בירייה 5: בינומית שלילית", size=26)
         + r'<div id="s-2" class="wm-eq h" style="font-size:30px;direction:ltr">$\binom41\left(\frac14\right)^2\left(\frac34\right)^3=\frac{108}{1024}\approx0.105$</div>'
         + st.card("s-k", "rule", "🔑 כלל העצירה קובע את המודל"))

atmost = Scene("atmost", "בדיוק או לכל היותר", [
    P("ועוד מלכודת של המודל הגאומטרי: ״בדיוק בירייה $k$״ זה לא ״עד הירייה $k$, לכל היותר״.",
      say="ועוד מלכודת של המודל הגאומטרי: בדיוק בירייה קֵיי, זה לא עד הירייה קֵיי, לכל היותר."),
    P("בדיוק בשלישית: שתי החטאות ואז פגיעה. שלושה רבעים בריבוע, כפול רבע. תשעה חלקי שישים וארבע.", do=show("m-0")),
    P("לכל היותר שלוש: הפגיעה הראשונה בראשונה, בשנייה או בשלישית. צריך לחבר שלושה איברים.", do=show("m-1")),
    P("או בדרך קצרה: המאורע המשלים הוא שלוש החטאות ראשונות. לכן אחת פחות שלושה רבעים בשלישית.", do=show("m-2", "m-r")),
    P("שלושים ושבעה חלקי שישים וארבע, כמעט שישים אחוז. הרבה יותר מתשעה חלקי שישים וארבע.", do=show("m-3"), hold=0.4),
], stage='<div class="wm-col">' + w.eqs("m", [
    "$P(X=3)=\\left(\\frac34\\right)^2\\cdot\\frac14=\\frac{9}{64}$",
    "$P(X\\le3)=P(1)+P(2)+P(3)$",
    "$P(X\\le3)=1-P(X>3)=1-\\left(\\frac34\\right)^3$",
    "$=\\frac{37}{64}\\approx0.578$"], size=40, gap=22) + "</div>",
   panel=st.card("m-r", "rule", "🔑 $P(X>k)=(1-p)^k$: $k$ כישלונות ראשונים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. שני שחקנים, יוג׳ין ובוריס, מטילים כל אחד מטבע מוטה **עד** העץ הראשון."),
    P("המטבעות מוטים באותו אופן. הראשון שמקבל עץ מנצח, ונתון שההסתברות לתיקו היא $Q$.",
      say="המטבעות מוטים באותו אופן. הראשון שמקבל עץ מנצח, ונתון שההסתברות לתיקו היא קְיוּ."),
    P("זיהוי המודל: עוצרים בהצלחה הראשונה, אז מספר ההטלות של כל שחקן גאומטרי, ושני השחקנים בלתי תלויים.",
      do=show("x-pill", "x-0")),
    P("סעיף ראשון: מי מנצח? המצב סימטרי, אז לשניהם אותו סיכוי לנצח.", do=show("x-1")),
    P("ושלוש התוצאות, ניצחון של כל אחד או תיקו, הן חלוקה. לכן כל אחד מנצח בהסתברות אחת פחות $Q$, חלקי שתיים.",
      do=show("x-2"), say="ושלוש התוצאות, ניצחון של כל אחד או תיקו, הן חלוקה. לכן כל אחד מנצח בהסתברות אחת פחות קְיוּ, חלקי שתיים."),
    P("סעיף שני: מה $p$? תיקו פירושו ששני המספרים שווים. מחברים על כל $k$ את הסיכוי ששניהם שווים $k$.",
      do=show("x-3"), say="סעיף שני: מה פִּי? תיקו פירושו ששני המספרים שווים. מחברים על כל קֵיי את הסיכוי ששניהם שווים קֵיי."),
    P("בגלל אי התלות זו מכפלה, ויוצא טור הנדסי עם מנה אחת פחות $p$, בריבוע.", do=show("x-4"),
      say="בגלל אי התלות זו מכפלה, ויוצא טור הנדסי עם מנה אחת פחות פִּי, בריבוע."),
    P("סכום הטור הוא $p$ חלקי שתיים פחות $p$. זה $Q$.", do=show("x-5"),
      say="סכום הטור הוא פִּי חלקי, שתיים פחות פִּי. זה קְיוּ."),
    P("ומחלצים: $p$ שווה פעמיים $Q$, חלקי אחת ועוד $Q$.", do=show("x-6"),
      say="ומחלצים: פִּי שווה פעמיים קְיוּ, חלקי אחת ועוד קְיוּ."),
    P("המלכודת: לכפול את שתי ההסתברויות בהטלה אחת ולקבל $p$ בריבוע. תיקו יכול לקרות בכל סיבוב, לא רק בראשון.",
      do=show("x-t"), say="המלכודת: לכפול את שתי ההסתברויות בהטלה אחת ולקבל פִּי בריבוע. תיקו יכול לקרות בכל סיבוב, לא רק בראשון.",
      hold=0.4),
], stage=f'<div class="wm-col" style="gap:12px">{w.pill("x-pill", "גאומטרית: עד העץ הראשון")}'
         + w.eqs("x", ["$X_1,\\ X_2\\sim G(p)$",
                       "$P_E=P_B$",
                       "$P_E+P_B+Q=1\\ \\Rightarrow\\ P_E=P_B=\\dfrac{1-Q}{2}$",
                       "$Q=P(X_1=X_2)=\\sum_{k\\ge1}P(X_1=k)\\,P(X_2=k)$",
                       "$=\\sum_{k\\ge1}p^2\\left[(1-p)^2\\right]^{k-1}=\\dfrac{p^2}{1-(1-p)^2}$",
                       "$Q=\\dfrac{p}{2-p}$",
                       "$p=\\dfrac{2Q}{1+Q}$"], size=34, gap=8) + "</div>",
   panel=w.stem(QA["id"] + " · " + QB["id"][-2:], "יוג׳ין ובוריס מטילים מטבעות מוטים זהים עד ה״עץ״ הראשון. "
                "הראשון שמקבל ״עץ״ מנצח. $P(\\text{tie})=Q$. מהי ההסתברות של כל אחד לנצח? מהו $p$?", size=28)
         + st.card("x-t", "trap", "⚠️ $Q\\ne p^2$: תיקו בכל סיבוב $k$, לא רק בראשון"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לפני החישוב, קוראים את כלל העצירה.", do=show("r-1")),
    P("מספר ניסויים קבוע: סופרים הצלחות, בינומית.", do=show("r-2")),
    P("עד ההצלחה הראשונה: גאומטרית. עד ההצלחה ה-$m$: בינומית שלילית, והאחרונה תמיד הצלחה.", do=show("r-3"),
      say="עד ההצלחה הראשונה: גאומטרית. עד ההצלחה ה-אֶם: בינומית שלילית, והאחרונה תמיד הצלחה."),
    P("ו״לכל היותר $k$״ מחשבים דרך המשלים. נתראה ברמה הבאה.", do=show("r-4"),
      say="ולכל היותר קֵיי, מחשבים דרך המשלים. נתראה ברמה הבאה.", hold=0.6),
], stage=f'<div class="wm-col">{w.checklist("rk", CK, size=32, width=920)}</div>',
   panel=st.card("r-1", "rule", "🔑 מה קבוע, ומה סופרים?")
         + st.card("r-2", "rule", "🔑 $n$ קבוע: $\\mathrm{Bin}(n,p)$")
         + st.card("r-3", "rule", "🔑 עד הצלחה: $G(p)$, $\\ \\mathrm{NegBin}(m,p)$")
         + st.card("r-4", "trap", "⚠️ $P(X\\le k)=1-(1-p)^k$"))

VIDEO = Video("W02", "which_model", "עד מתי מטילים? גאומטרית ובינומית שלילית",
              [title, idea, shots, atmost, exam, recap],
              bank={"26A-A-Q2a": None, "26A-A-Q2b": None})
