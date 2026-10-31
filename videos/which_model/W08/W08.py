# -*- coding: utf-8 -*-
"""W08 · סקירה מעורבת וזוגיות של גאומטרית — video script (build: tools/video/vid.py W08).

Source: courses/which_model/C08.js (lesson + goal: recognize the model in mixed questions, in order (hidden first
stage? without replacement? stopping? rate? only a mean? an item from groups?), plus parity questions).
Exam anchor: 26A-A-Q2e (the bonus part of the coin race: the mean length of the game GIVEN a tie; the conditional
law is again geometric, with success probability 4Q/(1+Q)^2). Not a quiz/boss id; its context (26A-A-c2) is not the
boss context. W02 solved parts a/b of the same exam; this part is new.
Not used on purpose: 26A-B-Q2b (boss: first head on an even toss) and its sibling 26A-B-Q2c; any parity of a
geometric (the C08 quiz item, coin with 1/3, and the lesson's fair coin). The parity tool E[(-1)^X] is shown on a
Poisson instead: P(X even) = (1 + e^{-2 lambda}) / 2.
Not used on purpose (C08 quiz): emails at 6 an hour with spam 0.25, lotto 6 of 40. Worked examples are new: three
one-line stories (3 tickets of 15 with 4 winners; traffic lights until the first red with 0.3; accidents at 0.5 a
month over a year) and the parity of a Poisson with lambda = 1.
Every value is exact (sympy) and checked by long direct sums and by simulating the literal story (numpy).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R, hyp, geo, nbin, pois

# ---------------------------------------------------------------- rapid fire
assert hyp(15, 4, 3, 1) == R(4 * sp.binomial(11, 2), sp.binomial(15, 3))
assert geo(R(3, 10), 1) == R(3, 10) and 1 / R(3, 10) == R(10, 3)          # E = 10/3 lights
assert R(1, 2) * 12 == 6                                                    # lambda for a year
STORIES = [("s1", "קונים 3 כרטיסים מתוך 15, ומהם 4 זוכים. כמה זוכים קנינו?", "$\\mathrm{Hyp}(15,4,3)$"),
           ("s2", "נוסעים עד הרמזור האדום הראשון. כל רמזור אדום ב-$0.3$", "$G(0.3)$"),
           ("s3", "תאונות בצומת: $0.5$ בחודש בממוצע. כמה בשנה?", "$P(6)$")]

# ---------------------------------------------------------------- parity of a Poisson: E[(-1)^X] = e^{-2 lambda}
lmb = sp.symbols("lambda", positive=True)
j = sp.symbols("j", integer=True, nonnegative=True)
Esg = sp.simplify(sp.summation((-1) ** j * sp.exp(-lmb) * lmb ** j / sp.factorial(j), (j, 0, sp.oo)))
assert sp.simplify(Esg - sp.exp(-2 * lmb)) == 0
EVEN1 = (1 + sp.exp(-2)) / 2
assert w.dec(EVEN1) == "0.568"
assert abs(float(sum(pois(1, 2 * i) for i in range(40))) - float(EVEN1)) < 1e-15
w.mc(lambda rng, n: {"X": rng.poisson(1.0, n)}, [("even", lambda d: d["X"] % 2 == 0, EVEN1)])


def first(rng, n, p, cap=500):
    return (rng.random((n, cap)) < p).argmax(axis=1) + 1


# ---------------------------------------------------------------- exam 26A-A-Q2e
Q = BANK["26A-A-Q2e"]
assert "בהינתן שהסתיים בתיקו" in Q["question"] and "\\frac{(1+Q)^2}{4Q}" in Q["solution"]
p, Qs, k = sp.symbols("p Q k", positive=True)
q = 1 - p
# given a tie, P(T = k | tie) = P(both first heads at k) / P(tie) = p^2 q^{2(k-1)} / (p/(2-p))
cond = p ** 2 * q ** (2 * (k - 1)) / (p / (2 - p))
for pv_ in [R(1, 10), R(3, 10), R(7, 10)]:                                 # geometric with success 1 - q^2
    for kk in range(1, 8):
        qv_ = 1 - pv_
        assert cond.subs({p: pv_, k: kk}) == (1 - qv_ ** 2) * (qv_ ** 2) ** (kk - 1)
p0 = 1 - q ** 2
assert sp.simplify(p0 - p * (2 - p)) == 0
pQ = 2 * Qs / (1 + Qs)                                                        # from part b
assert sp.simplify(p0.subs(p, pQ) - 4 * Qs / (1 + Qs) ** 2) == 0
assert sp.simplify(1 / p0.subs(p, pQ) - (1 + Qs) ** 2 / (4 * Qs)) == 0
pv = R(3, 10)
Qv = pv / (2 - pv)
ET = 1 / (pv * (2 - pv))
assert Qv == R(3, 17) and ET == R(100, 51) and (1 + Qv) ** 2 / (4 * Qv) == ET and w.dec(ET, 2) == "1.96"
assert 1 / pv == R(10, 3)                                                     # the trap: the length of one player
assert abs(float(sum(kk * float(cond.subs({p: pv, k: kk})) for kk in range(1, 200))) - float(ET)) < 1e-12
_r = np.random.default_rng(4)
A, B = first(_r, 2_000_000, 0.3), first(_r, 2_000_000, 0.3)
L = A[A == B]
assert abs(L.mean() - float(ET)) < 5 * L.std() / np.sqrt(len(L))

# ---------------------------------------------------------------- figures
REVIEW = [("h", "שלב ראשון נסתר או אקראי?", "שלמה, בייס, דילול"),
          ("w", "בלי החזרה מאוסף סופי?", "היפרגאומטרית"),
          ("n", "$n$ ניסויים בלתי תלויים?", "בינומית"),
          ("s", "עוצרים בהצלחה?", "גאומטרית, שלילית"),
          ("r", "קצב, בלי תקרה?", "פואסון"),
          ("e", "רק תוחלת של ספירה?", "אינדיקטורים"),
          ("g", "פריט מתוך קבוצות?", "הטיית גודל")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחבר את כל מה שלמדנו לרשימת בדיקה אחת."),
    P("נתרגל זיהוי מהיר, ונכיר כלי לשאלות של זוגיות."),
    P("ובסוף נפתור סעיף בונוס ממבחן: גאומטרית שמסתתרת בתוך תנאי.", hold=0.4),
], stage='<div class="kicker">W08 · איזה מודל זה?</div><h1>סקירה מעורבת וזוגיות</h1>'
         '<p>לזהות את המודל בשאלות מכל הסוגים, כולל שאלות של זוגיות ושל תנאי.</p>', layout="title")

review = Scene("review", "רשימת הבדיקה", [
    P("זו הרשימה. עוברים עליה לפי הסדר, ועוצרים בשאלה הראשונה שהתשובה עליה כן.", do=show("ck")),
    P("קודם: האם יש שלב ראשון נסתר, כמו כד שנבחר או מספר מגיעים אקראי? הסתברות שלמה, בייס או דילול.",
      do=show("ck-on-h", "ck-a-h")),
    P("אחר כך הניסוי עצמו: בלי החזרה, היפרגאומטרית. מספר ניסויים קבוע, בינומית. עצירה בהצלחה, גאומטרית.",
      do=show("ck-on-w", "ck-a-w", "ck-on-n", "ck-a-n", "ck-on-s", "ck-a-s")),
    P("קצב בלי תקרה, פואסון. רק תוחלת, אינדיקטורים. ופריט שנבחר מתוך קבוצות, הטיית גודל.",
      do=show("ck-on-r", "ck-a-r", "ck-on-e", "ck-a-e", "ck-on-g", "ck-a-g"), hold=0.4),
], stage=f'<div class="wm-col">{w.checklist("ck", REVIEW, size=28, width=900)}</div>'.replace('class="wm-ck"', 'class="wm-ck h"'),
   panel=st.card("v-r", "rule", "🔑 קודם המודל, אחר כך החישוב").replace(' h"', '"'))

rapid = Scene("rapid", "זיהוי מהיר", [
    P("שלושה סיפורים, זיהוי מהיר."),
    P("קונים שלושה כרטיסים מתוך חמישה עשר, וארבעה מהם זוכים. כרטיס לא נקנה פעמיים: היפרגאומטרית.",
      do=show("rf-r-s1", "rf-on-s1", "rf-a-s1")),
    P("נוסעים עד הרמזור האדום הראשון: עוצרים בהצלחה הראשונה, גאומטרית עם שלוש עשיריות.",
      do=show("rf-r-s2", "rf-on-s2", "rf-a-s2")),
    P("תאונות בצומת, חצי בחודש, ושואלים על שנה: פואסון, ו-$\\lambda$ של החלון הוא שש.",
      do=show("rf-r-s3", "rf-on-s3", "rf-a-s3"), say="תאונות בצומת, חצי בחודש, ושואלים על שנה: פואסון, ולמדא של החלון הוא שש.",
      hold=0.4),
], stage=f'<div class="wm-col">{w.checklist("rf", STORIES, size=29, hidden=True, width=1000)}</div>')

parity = Scene("parity", "כלי לזוגיות", [
    P("שאלות זוגיות מופיעות במבחנים: מה הסיכוי שמשתנה מקרי יוצא **זוגי**? הכלי: מינוס אחת בחזקת $X$.",
      do=show("p-0"), say="שאלות זוגיות מופיעות במבחנים: מה הסיכוי שמשתנה מקרי יוצא זוגי? הכלי: מינוס אחת בחזקת אִקְס."),
    P("הביטוי אחת ועוד מינוס אחת בחזקת $X$, חלקי שתיים, שווה אחת כש-$X$ זוגי, ואפס כשהוא אי זוגי.", do=show("p-1"),
      say="הביטוי, אחת ועוד מינוס אחת בחזקת אִקְס, חלקי שתיים, שווה אחת כשאִקְס זוגי, ואפס כשהוא אי זוגי."),
    P("אז ההסתברות לזוגי היא התוחלת שלו: אחת ועוד התוחלת של מינוס אחת בחזקת $X$, חלקי שתיים.", do=show("p-2"),
      say="אז ההסתברות לזוגי היא התוחלת שלו: אחת, ועוד התוחלת של מינוס אחת בחזקת אִקְס, חלקי שתיים."),
    P("נפעיל על פואסון. מציבים מינוס אחת בפונקציית ההסתברות, וזה טור טיילור של $e$ בחזקת מינוס $\\lambda$.",
      do=show("p-3"), say="נפעיל על פואסון. מציבים מינוס אחת בפונקציית ההסתברות, וזה טור טיילור של אִי בחזקת מינוס למדא."),
    P("יחד עם $e$ בחזקת מינוס $\\lambda$ שבחוץ, יוצא $e$ בחזקת מינוס שתיים $\\lambda$.", do=show("p-4"),
      say="יחד עם אִי בחזקת מינוס למדא שבחוץ, יוצא אִי בחזקת, מינוס שתיים למדא."),
    P("למשל $\\lambda$ שווה אחת: אחת ועוד $e$ בחזקת מינוס שתיים, חלקי שתיים. בערך חמישים ושבעה אחוזים.",
      do=show("p-5", "p-ok"), say="למשל למדא שווה אחת: אחת ועוד אִי בחזקת מינוס שתיים, חלקי שתיים. בערך חמישים ושבעה אחוזים."),
    P("קצת יותר מחצי, כי אפס, הערך הסביר ביותר, הוא זוגי. הכלי הזה עובד לכל התפלגות שיודעים לסכם.", hold=0.4),
], stage='<div class="wm-col" style="gap:12px">' + w.eqs("p", [
    "$(-1)^X$",
    "$\\dfrac{1+(-1)^X}{2}=\\begin{cases}1 & X\\ \\text{even}\\\\ 0 & X\\ \\text{odd}\\end{cases}$",
    "$P(X\\ \\text{even})=\\dfrac{1+E[(-1)^X]}{2}$",
    "$X\\sim P(\\lambda):\\ E[(-1)^X]=e^{-\\lambda}\\sum_{j\\ge0}\\dfrac{(-\\lambda)^j}{j!}$",
    "$=e^{-\\lambda}e^{-\\lambda}=e^{-2\\lambda}$",
    "$\\lambda=1:\\ P(X\\ \\text{even})=\\dfrac{1+e^{-2}}{2}\\approx0.568$"], size=32, gap=8) + "</div>",
   panel=w.chip("p-ok", "$\\approx0.568$ ✓") + st.card("p-r", "rule", "🔑 $P(\\text{even})=\\dfrac{1+E[(-1)^X]}{2}$").replace(' h"', '"'))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף בונוס ממבחן. יוג׳ין ובוריס מטילים מטבעות מוטים זהים עד העץ הראשון. ההסתברות לתיקו היא $Q$.",
      say="ועכשיו סעיף בונוס ממבחן. יוג׳ין ובוריס מטילים מטבעות מוטים זהים עד העץ הראשון. ההסתברות לתיקו היא קְיוּ."),
    P("מה תוחלת אורך המשחק, **בהינתן** שהוא הסתיים בתיקו?"),
    P("זיהוי: כל שחקן גאומטרי, והם בלתי תלויים. אבל השאלה מותנית, אז קודם מוצאים את ההתפלגות **בתנאי**.",
      do=show("x-0")),
    P("תיקו באורך $k$: שניהם נכשלים $k$ פחות אחת פעמים, ואז שניהם מצליחים. מחלקים בהסתברות לתיקו.", do=show("x-1"),
      say="תיקו באורך קֵיי: שניהם נכשלים קֵיי פחות אחת פעמים, ואז שניהם מצליחים. מחלקים בהסתברות לתיקו."),
    P("ויוצא שוב גאומטרית! כל סיבוב הוא ניסוי: הוא נגמר אם לא שניהם נכשלו, בהסתברות אחת פחות $q$ בריבוע.",
      do=show("x-2", "x-pill"), say="ויוצא שוב גאומטרית! כל סיבוב הוא ניסוי: הוא נגמר אם לא שניהם נכשלו, בהסתברות אחת פחות קְיוּ בריבוע."),
    P("מהסעיף הקודם, $p$ שווה פעמיים $Q$ חלקי אחת ועוד $Q$. מציבים, וההסתברות להצלחה היא ארבע $Q$ חלקי אחת ועוד $Q$, בריבוע.",
      do=show("x-3"), say="מהסעיף הקודם, פִּי שווה פעמיים קְיוּ, חלקי אחת ועוד קְיוּ. מציבים, וההסתברות להצלחה היא ארבע קְיוּ, חלקי, בסוגריים אחת ועוד קְיוּ, בריבוע."),
    P("ותוחלת של גאומטרית היא אחת חלקי ההסתברות להצלחה.", do=show("x-4")),
    P("במספרים: אם הסיכוי לעץ הוא שלוש עשיריות, משחק שנגמר בתיקו נמשך בממוצע כמעט שני סיבובים.", do=show("x-5", "x-ok")),
    P("המלכודת: לענות אחת חלקי $p$, שזה האורך של שחקן אחד. בתנאי של תיקו, ההתפלגות היא גאומטרית **אחרת**.",
      do=show("x-t"), say="המלכודת: לענות אחת חלקי פִּי, שזה האורך של שחקן אחד. בתנאי של תיקו, ההתפלגות היא גאומטרית אחרת.",
      hold=0.4),
], stage='<div class="wm-col" style="gap:10px">' + w.eqs("x", [
    "$X_1,\\ X_2\\sim G(p),\\quad q=1-p$",
    "$P(T=k\\mid \\text{tie})=\\dfrac{p^2\\,q^{2(k-1)}}{Q}$",
    "$=(1-q^2)\\,(q^2)^{k-1}\\ \\Rightarrow\\ T\\mid\\text{tie}\\sim G(1-q^2)$",
    "$1-q^2=p(2-p)=\\dfrac{4Q}{(1+Q)^2}$",
    "$E[T\\mid\\text{tie}]=\\dfrac{(1+Q)^2}{4Q}$",
    "$p=0.3:\\ Q=\\tfrac{3}{17},\\ \\ E=\\tfrac{100}{51}\\approx1.96$"], size=32, gap=8) + "</div>",
   panel=w.stem(Q["id"], "יוג׳ין ובוריס מטילים מטבעות מוטים זהים עד ה״עץ״ הראשון; $P(\\text{tie})=Q$. "
                "מהי תוחלת אורך המשחק בהינתן שהסתיים בתיקו?", size=28)
         + w.pill("x-pill", "גאומטרית בתנאי")
         + st.card("x-t", "trap", "⚠️ לא $\\frac1p$: זו גאומטרית אחרת")
         + w.chip("x-ok", "סימולציה: $\\approx1.96$ ✓"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: עוברים על רשימת הבדיקה לפי הסדר, ובוחרים מודל לפני שמחשבים.", do=show("r-1")),
    P("שאלת זוגיות: התוחלת של מינוס אחת בחזקת $X$, ונוסחת הזוגיות.", do=show("r-2"),
      say="שאלת זוגיות: התוחלת של מינוס אחת בחזקת אִקְס, ונוסחת הזוגיות."),
    P("ושאלה מותנית: קודם ההתפלגות בתנאי. לפעמים היא שוב מודל מוכר, עם פרמטר חדש. נתראה ברמה הבאה.",
      do=show("r-3"), hold=0.6),
], stage=f'<div class="wm-col">{w.checklist("rk", REVIEW, size=28, width=900)}</div>',
   panel=st.card("r-1", "rule", "🔑 קודם המודל")
         + st.card("r-2", "rule", "🔑 $P(\\text{even})=\\frac{1+E[(-1)^X]}{2}$")
         + st.card("r-3", "rule", "🔑 בתנאי: התפלגות חדשה, לפעמים מוכרת"))

VIDEO = Video("W08", "which_model", "סקירה מעורבת וזוגיות של גאומטרית", [title, review, rapid, parity, exam, recap],
              bank={"26A-A-Q2e": None})
