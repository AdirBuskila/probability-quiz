# -*- coding: utf-8 -*-
"""W09 · בוס: שאלות מבחן אמיתיות — video script (build: tools/video/vid.py W09).

Source: courses/which_model/C09.js (boss: real exam parts where the model is hidden in the story). A walkthrough of
three exam parts, none of them a quiz/boss id and none a content twin of one:
  24A-A-Q3a/Q3b  two random letter strings, X1, X2 = the number of A's: binomials, and X1 + X2 ~ Bin(N1 + N2, p)
  24S-B-Q5a      an urn that gets 2 red or 2 black balls per coin toss, M tosses, then one ball: (D + 2pM)/(N + 2M)
  25A-A-Q5a      the number of zeros of cos(wt) on (0, T) with w ~ Exp(lambda): not Poisson, a continuous variable
                 cut into intervals (a geometric-shaped pmf)
Not used on purpose: the five C09 boss items (24A-A-Q5b, 25B-A-Q6b, 26A-B-Q2b, 24A-B-Q5a, 25A-B-Q5b) and their twins
(24S-A-Q5b, 24B-B-Q5b, 24A-D-Q5b, 24A-C-Q5a, 25A-B-Q5c, 25S-A-Q3d); 24A-B-Q5b / 24A-C-Q5b (their statement contains
the boss item 24A-B-Q5a); every quiz item of C01..C08.
Everything is exact (sympy) and simulated literally (numpy).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R, binom

# ---------------------------------------------------------------- part 1: 24A-A-Q3a / Q3b
Q1a, Q1b = BANK["24A-A-Q3a"], BANK["24A-A-Q3b"]
assert "שכיחות האות $A$" in w.ctx_text(Q1a) and "X\\sim\\mathrm{Bin}(N_1+N_2,p)" in Q1b["solution"]
assert any("N_1N_2" in s for s in Q1b["pitfalls"])
for N1, N2 in [(2, 3), (4, 1), (3, 3)]:
    for pv in [R(1, 3), R(2, 5)]:
        for j in range(N1 + N2 + 1):
            conv = sum(binom(N1, pv, i) * binom(N2, pv, j - i) for i in range(0, j + 1))
            assert conv == binom(N1 + N2, pv, j)
# with different p's the sum is NOT binomial (why the equal p matters)
conv = [sum(binom(2, R(1, 5), i) * binom(2, R(4, 5), j - i) for i in range(j + 1)) for j in range(5)]
assert all(conv[j] != binom(4, R(1, 2), j) for j in (0, 2))


def gen_letters(rng, n):
    return {"X": (rng.random((n, 3)) < 0.4).sum(axis=1) + (rng.random((n, 5)) < 0.4).sum(axis=1)}


w.mc(gen_letters, [(f"X={j}", lambda d, j=j: d["X"] == j, binom(8, R(2, 5), j)) for j in range(9)])

# ---------------------------------------------------------------- part 2: 24S-B-Q5a
Q2 = BANK["24S-B-Q5a"]
CT2 = w.ctx_text(Q2)
assert "שני כדורים אדומים" in CT2 and "$M$ פעמים" in CT2 and "\\frac{D+2pM}{N+2M}" in Q2["solution"]
p, Dn, Nn, Mn = sp.symbols("p D N M", positive=True)
for M in range(1, 6):
    full = sum(binom(M, p, k) * (Dn + 2 * k) / (Nn + 2 * M) for k in range(M + 1))
    assert sp.simplify(full - (Dn + 2 * p * M) / (Nn + 2 * M)) == 0
D0, N0, M0, p0 = 3, 10, 4, R(1, 4)
ANS2 = (D0 + 2 * p0 * M0) / (N0 + 2 * M0)
assert ANS2 == R(5, 18)


def gen_urn(rng, n):
    H = (rng.random((n, M0)) < 0.25).sum(axis=1)
    return {"R": rng.random(n) < (D0 + 2 * H) / (N0 + 2 * M0)}


w.mc(gen_urn, [("red", lambda d: d["R"], ANS2)])

# ---------------------------------------------------------------- part 3: 25A-A-Q5a
Q3 = BANK["25A-A-Q5a"]
assert "\\omega\\sim\\mathrm{Exp}(\\lambda)" in w.ctx_text(Q3) and any("פואסוני" in s for s in Q3["pitfalls"])
assert "1-e^{-\\lambda\\pi/(2T)}" in Q3["solution"]
lam, T, x = sp.symbols("lambda T x", positive=True)
k = sp.symbols("k", integer=True, positive=True)
f = lam * sp.exp(-lam * x)
P0 = sp.integrate(f, (x, 0, sp.pi / (2 * T)))
assert sp.simplify(P0 - (1 - sp.exp(-lam * sp.pi / (2 * T)))) == 0
Pk = sp.integrate(f, (x, sp.pi * (k - R(1, 2)) / T, sp.pi * (k + R(1, 2)) / T))
c = lam * sp.pi / T
assert sp.simplify(Pk - sp.exp(-c * k) * (sp.exp(c / 2) - sp.exp(-c / 2))) == 0
tot = P0 + sp.summation(sp.exp(-c * k) * (sp.exp(c / 2) - sp.exp(-c / 2)), (k, 1, sp.oo))
assert sp.simplify(tot) == 1
# the ratio of consecutive values is e^{-lambda pi / T}: geometric-shaped from k = 1 on
assert sp.simplify(Pk.subs(k, k + 1) / Pk - sp.exp(-c)) == 0                 # from k = 1 on
R10 = sp.simplify(Pk.subs(k, 1) / P0)                                          # but not from 0 to 1
assert sp.simplify(R10 - (sp.exp(-c / 2) + sp.exp(-c))) == 0 and sp.simplify(R10 - sp.exp(-c)) != 0
LV, TV = 1.0, 2.0


def gen_zeros(rng, n):
    om = rng.exponential(1 / LV, n)
    # zeros of cos(om t) in (0, T): t = (pi/2 + pi j)/om < T  <=>  j < om T / pi - 1/2
    return {"N": np.maximum(0, np.floor(om * TV / np.pi + 0.5)).astype(int)}


num = lambda e: e.subs({lam: 1, T: 2})
w.mc(gen_zeros, [("N0", lambda d: d["N"] == 0, num(P0))]
     + [(f"N{kk}", lambda d, kk=kk: d["N"] == kk, num(Pk.subs(k, kk))) for kk in (1, 2, 3)])
# and literally: count the roots of cos(om t) on a grid for a few draws
_rng = np.random.default_rng(2)
for om in _rng.exponential(1, 30):
    tt = np.linspace(1e-9, TV, 400001)
    s = np.sign(np.cos(om * tt))
    assert int((s[1:] != s[:-1]).sum()) == int(np.floor(om * TV / np.pi + 0.5))

# ---------------------------------------------------------------- figures
CK = [("q1", "אותיות בלתי תלויות, שכיחות $p$, אורך $N_1$", "בינומית"),
      ("q2", "$M$ הטלות קובעות את הכד, ואז שליפה", "שלמה + תוחלת"),
      ("q3", "תדירות $\\omega$ אחת אקראית, ״כמה אפסים״", "לא פואסון!")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הבוס של המסלול: שלושה סעיפים אמיתיים ממבחנים."),
    P("באף אחד מהם השאלה לא אומרת איזה מודל. נזהה אותו, ננמק, ונחשב."),
    P("ובכל אחד נראה איפה רוב הסטודנטים נופלים.", hold=0.4),
], stage='<div class="kicker">W09 · איזה מודל זה?</div><h1>בוס: שאלות מבחן אמיתיות</h1>'
         '<p>להתחיל שאלת מבחן שהמודל בה מוסתר: ״איזה מודל זה?״</p>', layout="title")

part1 = Scene("p1", "סעיף ראשון", [
    P("סעיף ראשון. מחשב מייצר שתי סדרות של אותיות $A$ ו-$B$, באורך $N_1$ ו-$N_2$. השכיחות של $A$ היא $p$.",
      say="סעיף ראשון. מחשב מייצר שתי סדרות של אותיות אֵיי ובִּי, באורך אֶן אחת ואֶן שתיים. השכיחות של אֵיי היא פִּי."),
    P("איך מפולג מספר ה-$A$ בכל סדרה? כל אות היא ניסוי ברנולי, בלי תלות, ומספר האותיות קבוע.",
      do=show("ck-r-q1", "ck-on-q1", "ck-a-q1", "a-0"), say="איך מפולג מספר האֵיי בכל סדרה? כל אות היא ניסוי ברנולי, בלי תלות, ומספר האותיות קבוע."),
    P("לכן בינומית: $X_1$ עם $N_1$ ו-$p$, ו-$X_2$ עם $N_2$ ו-$p$.", do=show("a-1"),
      say="לכן בינומית: אִקְס אחת עם אֶן אחת ופִּי, ואִקְס שתיים עם אֶן שתיים ופִּי."),
    P("ואיך מפולג הסכום? מפרקים כל אחד לסכום של משתני ברנולי.", do=show("a-2")),
    P("ביחד: $N_1$ ועוד $N_2$ ניסויי ברנולי בלתי תלויים, **עם אותו $p$**. אז שוב בינומית.", do=show("a-3", "a-ok"),
      say="ביחד: אֶן אחת ועוד אֶן שתיים ניסויי ברנולי בלתי תלויים, עם אותו פִּי. אז שוב בינומית."),
    P("המלכודות: לכתוב $N_1$ **כפול** $N_2$, או לשכוח לנמק שה-$p$ זהה. עם שני $p$ שונים הסכום כבר לא בינומי.",
      do=show("a-t"), say="המלכודות: לכתוב אֶן אחת כפול אֶן שתיים, או לשכוח לנמק שהפִּי זהה. עם שני פִּי שונים הסכום כבר לא בינומי.",
      hold=0.4),
], stage='<div class="wm-col" style="gap:14px">' + w.checklist("ck", [CK[0]], size=28, hidden=True, width=980)
         + w.eqs("a", ["$\\text{letter } j:\\ \\ Z_j\\sim\\mathrm{Ber}(p)\\ \\ \\text{i.i.d.}$",
                       "$X_1\\sim\\mathrm{Bin}(N_1,p),\\quad X_2\\sim\\mathrm{Bin}(N_2,p)$",
                       "$X_1=\\sum_{j=1}^{N_1}Z_j,\\quad X_2=\\sum_{k=1}^{N_2}W_k$",
                       "$X_1+X_2\\sim\\mathrm{Bin}(N_1+N_2,\\,p)$"], size=34, gap=10)
         + "</div>",
   panel=w.stem(Q1a["id"] + " · " + Q1b["id"][-2:], "שתי סדרות אותיות באורך $N_1$ ו-$N_2$, שכיחות $A$ היא $p$. "
                "איך מפולגים $X_1$, $X_2$ (מספר ה-$A$)? ואיך מפולג $X_1+X_2$? הוכיחו.", size=28)
         + w.chip("a-ok", "$\\mathrm{Bin}(N_1+N_2,p)$ ✓")
         + st.card("a-t", "trap", "⚠️ לא $N_1N_2$, וחייב אותו $p$"))

part2 = Scene("p2", "סעיף שני", [
    P("סעיף שני. בכד $D$ אדומים מתוך $N$. מטילים מטבע מוטה, עץ בהסתברות $p$, $M$ פעמים. עץ מוסיף שני אדומים, פלי שני שחורים.",
      say="סעיף שני. בכד דִּי אדומים מתוך אֶן. מטילים מטבע מוטה, עץ בהסתברות פִּי, אֶם פעמים. עץ מוסיף שני אדומים, פלי שני שחורים."),
    P("בסוף שולפים כדור אחד. מה הסיכוי שהוא אדום?"),
    P("זיהוי: יש שלב ראשון אקראי, ההטלות, שקובע את הכד. אז הסתברות שלמה לפי מספר העצים.",
      do=show("ck-r-q2", "ck-on-q2", "ck-a-q2")),
    P("מספר העצים $X$ בינומי, עם $M$ ו-$p$. אם $X$ שווה $k$, בכד $D$ ועוד שתיים $k$ אדומים, ו-$N$ ועוד שתיים $M$ כדורים בסך הכול.",
      do=show("b-0", "b-1"), say="מספר העצים אִקְס בינומי, עם אֶם ופִּי. אם אִקְס שווה קֵיי, בכד דִּי ועוד שתיים קֵיי אדומים, ואֶן ועוד שתיים אֶם כדורים."),
    P("שימו לב: המכנה קבוע, תמיד $N$ ועוד שתיים $M$. לכן הביטוי ליניארי ב-$k$.",
      say="שימו לב: המכנה קבוע, תמיד אֶן ועוד שתיים אֶם. לכן הביטוי ליניארי בקֵיי."),
    P("ובדיוק כמו בשלב האינדיקטורים: הסכום הופך לתוחלת של $X$, שהיא $p$ כפול $M$.", do=show("b-2", "b-3"),
      say="ובדיוק כמו בשלב האינדיקטורים: הסכום הופך לתוחלת של אִקְס, שהיא פִּי כפול אֶם."),
    P("בדיקה במספרים: שלושה אדומים מעשרה, ארבע הטלות, ורבע לעץ. יוצא חמש חלקי שמונה עשרה, והסימולציה מסכימה.",
      do=show("b-4", "b-ok")),
    P("המלכודת: לענות $D$ חלקי $N$, כאילו הכד לא השתנה.", do=show("b-t"),
      say="המלכודת: לענות דִּי חלקי אֶן, כאילו הכד לא השתנה.", hold=0.4),
], stage='<div class="wm-col" style="gap:14px">' + w.checklist("ck2", [CK[1]], size=28, width=980).replace("ck2-", "ck-")
         .replace('class="wm-row"', 'class="wm-row h"')
         + w.eqs("b", ["$X\\sim\\mathrm{Bin}(M,p)$",
                       "$P(R\\mid X=k)=\\dfrac{D+2k}{N+2M}$",
                       "$P(R)=\\sum_{k=0}^{M}\\dfrac{D+2k}{N+2M}P(X=k)=\\dfrac{D+2E[X]}{N+2M}$",
                       "$P(R)=\\dfrac{D+2pM}{N+2M}$",
                       "$D=3,\\ N=10,\\ M=4,\\ p=\\tfrac14:\\ \\ \\dfrac{3+2}{18}=\\dfrac{5}{18}$"], size=32, gap=10)
         + "</div>",
   panel=w.stem(Q2["id"], "בכד $D$ אדומים ו-$N-D$ שחורים. מטילים מטבע ($p$ ל״עץ״) $M$ פעמים: ״עץ״ מוסיף שני אדומים, "
                "״פלי״ שני שחורים. אחר כך מוציאים כדור אחד. מה ההסתברות שהוא אדום?", size=28)
         + w.chip("b-ok", "סימולציה ✓")
         + st.card("b-t", "trap", "⚠️ לא $\\frac DN$: הכד השתנה"))

part3 = Scene("p3", "סעיף שלישי", [
    P("סעיף שלישי, והכי מטעה. הפונקציה קוסינוס של אומגה טִי, והתדירות אומגה אקראית, מעריכית עם $\\lambda$.",
      say="סעיף שלישי, והכי מטעה. הפונקציה קוסינוס של אומגה טִי, והתדירות אומגה אקראית, מעריכית עם למדא."),
    P("$N_T$ הוא מספר האפסים של הפונקציה בקטע מאפס עד $T$. מצאו את פונקציית ההסתברות שלו.",
      say="אֶן טִי הוא מספר האפסים של הפונקציה בקטע מאפס עד טִי. מצאו את פונקציית ההסתברות שלו."),
    P("״מספר אירועים בקטע זמן״ נשמע כמו פואסון. אבל כאן כל האפסים נקבעים יחד, על ידי אומגה **אחת**. אין שום אי תלות.",
      do=show("ck-r-q3", "ck-no-q3", "ck-a-q3")),
    P("אז המודל הוא משתנה רציף, אומגה, שחותכים לקטעים. האפסים נמצאים בפאי חלקי אומגה, כפול $k$ פחות חצי.",
      do=show("c-0"), say="אז המודל הוא משתנה רציף, אומגה, שחותכים לקטעים. האפסים נמצאים בפאי חלקי אומגה, כפול, בסוגריים קֵיי פחות חצי."),
    P("יש בדיוק $k$ אפסים כשהאפס ה-$k$ לפני $T$, וה-$k$ ועוד אחת אחרי. וזה קורה כשאומגה בקטע הזה.", do=show("c-1"),
      say="יש בדיוק קֵיי אפסים כשהאפס ה-קֵיי לפני טִי, וה-קֵיי ועוד אחת אחרי. וזה קורה כשאומגה בקטע הזה."),
    P("ההסתברות של קטע במעריכית: הפרש של שני אקספוננטים. ולאפס אפסים: אומגה קטנה מפאי חלקי $2T$.",
      do=show("c-2", "c-3"), say="ההסתברות של קטע במעריכית: הפרש של שני אקספוננטים. ולאפס אפסים: אומגה קטנה מפאי חלקי, בסוגריים שתיים טִי."),
    P("ומה יצא? החל מ-$k=1$, כל ערך הוא הקודם כפול $e^{-\\lambda\\pi/T}$; הערך באפס שונה. צורה גאומטרית, לא פואסון.",
      do=show("c-4"), say="ומה יצא? החל מקֵיי שווה אחת, כל ערך הוא הקודם כפול אִי בחזקת מינוס למדא פאי חלקי טִי. הערך באפס שונה. צורה גאומטרית, לא פואסון."),
    P("והסכום של כל ההסתברויות, מאפס ועד אינסוף, הוא אחת.", do=show("c-ok")),
    P("המלכודת השנייה: האפס הראשון הוא בפאי חלקי **שתיים** אומגה, לא בפאי חלקי אומגה. מכאן החצי בגבולות.",
      do=show("c-t"), hold=0.4),
], stage='<div class="wm-col" style="gap:12px">' + w.checklist("ck3", [CK[2]], size=28, width=980).replace("ck3-", "ck-")
         .replace('class="wm-row"', 'class="wm-row h"')
         + w.eqs("c", ["$t_k=\\dfrac{\\pi(k-\\frac12)}{\\omega},\\quad k=1,2,\\dots$",
                       "$N_T=k\\iff \\dfrac{\\pi(k-\\frac12)}{T}<\\omega<\\dfrac{\\pi(k+\\frac12)}{T}$",
                       "$P(N_T=k)=e^{-\\lambda\\pi(k-\\frac12)/T}-e^{-\\lambda\\pi(k+\\frac12)/T}$",
                       "$P(N_T=0)=P\\left(\\omega<\\dfrac{\\pi}{2T}\\right)=1-e^{-\\lambda\\pi/(2T)}$",
                       "$\\dfrac{P(N_T=k+1)}{P(N_T=k)}=e^{-\\lambda\\pi/T},\\ \\ k\\ge1$"], size=31, gap=8)
         + "</div>",
   panel=w.stem(Q3["id"], "$y(t)=\\cos(\\omega t)$ עם $\\omega\\sim\\mathrm{Exp}(\\lambda)$. $N_T$ הוא מספר האפסים של "
                "$y$ בקטע $(0,T)$. מצאו את פונקציית ההסתברות של $N_T$.", size=28)
         + w.chip("c-ok", "סכום $=1$ ✓")
         + st.card("c-t", "trap", "⚠️ לא פואסון, והאפס הראשון ב-$\\frac{\\pi}{2\\omega}$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום שלושת הסעיפים: אותיות בלתי תלויות עם אותה שכיחות נותנות בינומית, וגם הסכום בינומי.", do=show("r-1")),
    P("כד שתלוי בהטלות: הסתברות שלמה, והליניאריות הופכת את הסכום לתוחלת.", do=show("r-2")),
    P("וספירה בקטע זמן היא לא תמיד פואסון. שואלים קודם מה אקראי באמת.", do=show("r-3")),
    P("בכל שאלה: קודם המודל, עם נימוק, ורק אז החישוב. בהצלחה במבחן!", hold=0.6),
], stage=f'<div class="wm-col">{w.checklist("rk", CK, size=28, width=980)}</div>',
   panel=st.card("r-1", "rule", "🔑 $\\mathrm{Bin}(N_1,p)+\\mathrm{Bin}(N_2,p)=\\mathrm{Bin}(N_1+N_2,p)$")
         + st.card("r-2", "rule", "🔑 שלב נסתר: שלמה, ותוחלת כשליניארי")
         + st.card("r-3", "trap", "⚠️ ״כמה בקטע״ לא תמיד פואסון"))

VIDEO = Video("W09", "which_model", "בוס: שאלות מבחן אמיתיות", [title, part1, part2, part3, recap],
              bank={"24A-A-Q3a": None, "24A-A-Q3b": None, "24S-B-Q5a": None, "25A-A-Q5a": None})
