# -*- coding: utf-8 -*-
"""W01 · עם החזרה או בלי? בינומית מול היפרגאומטרית — video script (build: tools/video/vid.py W01).

Source: courses/which_model/C01.js (lesson + goal: decide between binomial and hypergeometric by one question, does the
composition change between the draws).
Exam anchors: 26A-B-Q5a (X = reds among n balls taken WITHOUT replacement from urn 1: Hyp, with its range of values)
and 25A-A-Q6a (a shipment of n batteries from a store where a PROPORTION q comes from factory A: Bin(n, q); the
official pitfall is using the hypergeometric). Neither is a quiz/boss id. Not used on purpose: 24A-B-Q5a / 24A-C-Q5a
(the boss item and its twin: n balls WITH replacement), 25A-A-Q6b (binomial of binomial, the C04 / boss pattern).
Not used on purpose (C01 quiz): 6 red + 4 blue with replacement, the committee 7 women + 5 men, 5 cards / 2 hearts,
and the lesson's bag 3 red + 2 blue. Worked examples are new: a bag of 4 red + 4 black, 3 draws, both ways (the two
pmfs side by side, equal means 3/2), and three one-line stories (dice, choosing 3 of 20 pupils, 4 of 30 bulbs).
Every pmf is exact (sympy) and agrees with the course checker's lib.py (w_which_model.agree_lib); every story is
simulated literally (numpy) within 5 standard errors.
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R, binom, hyp

# ---------------------------------------------------------------- example: 4 red + 4 black, 3 draws
KS = [0, 1, 2, 3]
BIN = {k: binom(3, R(1, 2), k) for k in KS}
HYP = {k: hyp(8, 4, 3, k) for k in KS}
assert [BIN[k] for k in KS] == [R(1, 8), R(3, 8), R(3, 8), R(1, 8)]
assert [HYP[k] for k in KS] == [R(1, 14), R(3, 7), R(3, 7), R(1, 14)]
assert sum(BIN.values()) == 1 and sum(HYP.values()) == 1
assert sum(k * v for k, v in BIN.items()) == R(3, 2) == sum(k * v for k, v in HYP.items())     # same mean, n*D/N
assert HYP[3] == R(sp.binomial(4, 3), sp.binomial(8, 3)) == R(4, 56)
# without replacement the chance of red moves: 4/8, then 3/7 after a red, then 2/6
assert [R(4 - i, 8 - i) for i in range(3)] == [R(1, 2), R(3, 7), R(1, 3)]
assert R(4, 8) * R(3, 7) * R(2, 6) == HYP[3]


def gen_bag(rng, n):
    keys = rng.random((n, 8)).argsort(axis=1)[:, :3]        # 3 balls without replacement; balls 0..3 are red
    rep = rng.integers(0, 8, (n, 3))                         # 3 balls with replacement
    return {"H": (keys < 4).sum(axis=1), "B": (rep < 4).sum(axis=1)}


w.mc(gen_bag, [(f"hyp{k}", lambda d, k=k: d["H"] == k, HYP[k]) for k in KS]
     + [(f"bin{k}", lambda d, k=k: d["B"] == k, BIN[k]) for k in KS])

# ---------------------------------------------------------------- the three one-line stories
# dice: 5 rolls, number of sixes -> Bin(5, 1/6);  3 of 20 pupils (8 girls) -> Hyp(20, 8, 3);  4 of 30 bulbs (5 burnt)
assert binom(5, R(1, 6), 1) == 5 * R(1, 6) * R(5, 6) ** 4
assert hyp(20, 8, 3, 3) == R(8 * 7 * 6, 20 * 19 * 18)
assert hyp(30, 5, 4, 0) == R(sp.binomial(25, 4), sp.binomial(30, 4))

# ---------------------------------------------------------------- exam 26A-B-Q5a
Q1 = BANK["26A-B-Q5a"]
assert "וללא החזרה" in w.ctx_text(Q1) and "מהכד הראשון" in Q1["question"]
assert r"\binom{D_1}{k}\binom{N_1-D_1}{n-k}" in Q1["solution"] and r"\max\{0,\,n-(N_1-D_1)\}" in Q1["solution"]
N1, D1, n1 = 10, 7, 5                                        # a concrete urn to show the range of values
lo, hi = max(0, n1 - (N1 - D1)), min(n1, D1)
assert (lo, hi) == (2, 5)
assert [k for k in range(0, n1 + 1) if hyp(N1, D1, n1, k) > 0] == list(range(lo, hi + 1))
assert sum(hyp(N1, D1, n1, k) for k in range(lo, hi + 1)) == 1
for NN in range(2, 9):                                       # the pmf sums to 1 for every urn (Vandermonde), on a grid
    for DD in range(0, NN + 1):
        for nn in range(1, NN + 1):
            assert sum(hyp(NN, DD, nn, k) for k in range(0, nn + 1)) == 1


def gen_urn1(rng, n):
    keys = rng.random((n, N1)).argsort(axis=1)[:, :n1]
    return {"X": (keys < D1).sum(axis=1)}


w.mc(gen_urn1, [(f"X={k}", lambda d, k=k: d["X"] == k, hyp(N1, D1, n1, k)) for k in range(0, n1 + 1)])

# ---------------------------------------------------------------- exam 25A-A-Q6a
Q2 = BANK["25A-A-Q6a"]
assert r"X\sim\mathrm{Bin}(n,q)" in Q2["solution"] and any("היפרגאומטרית" in s for s in Q2["pitfalls"])
q_ = sp.symbols("q", positive=True)
nn_ = 6
assert sp.simplify(sum(sp.binomial(nn_, k) * q_ ** k * (1 - q_) ** (nn_ - k) for k in range(nn_ + 1)) - 1) == 0


def gen_ship(rng, n, qv=0.35):
    return {"X": (rng.random((n, nn_)) < qv).sum(axis=1)}


w.mc(gen_ship, [(f"X={k}", lambda d, k=k: d["X"] == k, binom(nn_, R(35, 100), k)) for k in range(nn_ + 1)])

# ---------------------------------------------------------------- figures
BAG = w.urn("bag", ["r"] * 4 + ["k"] * 4, size=50, per_row=8)
BARS = w.bars("pm", KS, [("bin", BIN, "b", "עם החזרה"), ("hyp", HYP, "a", "בלי החזרה")],
              w=900, h=400, nd=3)
CK = [("same", "אותו הרכב בכל שליפה? (החזרה, הטלות)", "בינומית"),
      ("chg", "ההרכב משתנה? (בלי החזרה מאוסף סופי)", "היפרגאומטרית")]
STORIES = [("s1", "מטילים קובייה 5 פעמים. כמה שישיות?", "בינומית"),
           ("s2", "בוחרים 3 נציגים מכיתה של 20, ובה 8 בנות. כמה בנות?", "היפרגאומטרית"),
           ("s3", "בודקים 4 נורות שונות מתוך 30, מהן 5 שרופות. כמה שרופות?", "היפרגאומטרית")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד להכריע בין שני מודלים שמתבלבלים ביניהם הכי הרבה."),
    P("בינומית מול היפרגאומטרית, לפי שאלה אחת בלבד."),
    P("ובסוף נפתור שני סעיפים אמיתיים ממבחנים.", hold=0.4),
], stage='<div class="kicker">W01 · איזה מודל זה?</div><h1>עם החזרה או בלי?</h1>'
         '<p>בינומית מול היפרגאומטרית: שאלה אחת מכריעה, האם ההרכב משתנה בין השליפות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("בשני המודלים סופרים הצלחות מתוך מספר קבוע של ניסיונות. ההבדל הוא במה שקורה בין ניסיון לניסיון."),
    P("בבינומית יש $n$ ניסויים בלתי תלויים, ובכל אחד ההצלחה באותה הסתברות $p$.", do=show("i-b"),
      say="בבינומית יש אֶן ניסויים בלתי תלויים, ובכל אחד ההצלחה באותה הסתברות פִּי."),
    P("זה מה שקורה כששולפים **עם החזרה**, או מטילים מטבע וקובייה: ההרכב לא משתנה.", do=show("ck-r-same", "ck-on-same", "ck-a-same")),
    P("בהיפרגאומטרית יש אוסף של $N$ פריטים, $D$ מהם מסומנים, ושולפים $n$ **בלי החזרה**.", do=show("i-h"),
      say="בהיפרגאומטרית יש אוסף של אֶן גדולה פריטים, דִּי מהם מסומנים, ושולפים אֶן קטנה בלי החזרה."),
    P("כאן כל שליפה משנה את מה שנשאר באוסף, ולכן הניסיונות **תלויים**.", do=show("ck-r-chg", "ck-on-chg", "ck-a-chg")),
    P("אז השאלה המכריעה היא אחת: האם ההרכב משתנה בין השליפות?", do=show("i-k"), hold=0.4),
], stage=f'<div class="wm-col">{w.checklist("ck", CK, size=32, hidden=True, width=900)}'
         + st.card("i-k", "rule", "🔑 ההרכב משתנה בין השליפות? כן: היפרגאומטרית. לא: בינומית") + "</div>",
   panel=w.box("i-b", "<b>בינומית</b> $\\mathrm{Bin}(n,p)$<br>$P(X=k)=\\binom nk p^k(1-p)^{n-k}$", size=30)
         + w.box("i-h", "<b>היפרגאומטרית</b> $\\mathrm{Hyp}(N,D,n)$<br>"
                 "$P(X=k)=\\dfrac{\\binom Dk\\binom{N-D}{n-k}}{\\binom Nn}$", size=30))

bag = Scene("bag", "אותו שק, שני מודלים", [
    P("דוגמה. בשק 4 כדורים אדומים ו-4 שחורים, ושולפים 3. $X$ הוא מספר האדומים.", do=show("bag"),
      say="דוגמה. בשק ארבעה כדורים אדומים וארבעה שחורים, ושולפים שלושה. אִקְס הוא מספר האדומים."),
    P("עם החזרה: בכל שליפה הסיכוי לאדום הוא חצי, תמיד. זו בינומית עם $n=3$ ו-$p=\\frac12$.", do=show("b-0"),
      say="עם החזרה: בכל שליפה הסיכוי לאדום הוא חצי, תמיד. זו בינומית עם אֶן שווה שלוש, ופִּי שווה חצי."),
    P("בלי החזרה: שלפנו אדום, והוא לא חוזר.", do=show("bag-h0", "bag-x0")),
    P("עכשיו נשארו 3 אדומים מתוך 7. הסיכוי לאדום ירד לשלוש שביעיות.", do=show("b-1")),
    P("ואחרי אדום נוסף: שניים מתוך שישה, כלומר שליש. ההרכב משתנה, ולכן זו היפרגאומטרית.",
      do=show("bag-h1", "bag-x1", "b-2")),
    P("נשווה את שתי ההתפלגויות. בכחול: עם החזרה.", do=hide("bag-h0", "bag-h1") + show("pm", "pm-s-bin")),
    P("ובטורקיז: בלי החזרה. הקצוות, אפס או שלושה אדומים, קטנים יותר.", do=show("pm-s-hyp")),
    P("למשל שלושה אדומים: עם החזרה שמינית. בלי החזרה ארבעה חלקי חמישים ושש, כלומר אחד חלקי ארבע עשרה.",
      do=show("pm-c-3", "pm-v-bin-3", "pm-v-hyp-3", "b-3")),
    P("למה? בלי החזרה, כל אדום שיצא מקטין את הסיכוי לאדום הבא. אז רצף של אדומים פחות סביר."),
    P("ושימו לב: התוחלת זהה בשניהם, אחת וחצי. המודל משנה את ההתפלגות, לא את הממוצע.", do=show("b-4"), hold=0.4),
], stage=f'<div class="wm-col" style="gap:14px">{BAG}{BARS}</div>',
   panel=w.eqs("b", ["$p_1=\\frac48=\\frac12$", "$p_2=\\frac37$", "$p_3=\\frac26=\\frac13$",
                     "$P(X=3):\\ \\frac18\\ \\text{vs}\\ \\frac{4}{56}=\\frac1{14}$",
                     "$E[X]=3\\cdot\\frac12=3\\cdot\\frac48=1.5$"], size=36, gap=14))

stories = Scene("stories", "שלוש שאלות קצרות", [
    P("נתרגל את השאלה המכריעה על שלושה סיפורים קצרים."),
    P("קובייה מוטלת חמש פעמים, וסופרים שישיות. אין כאן אוסף שמתרוקן: כל הטלה מתחילה מחדש.", do=show("st-r-s1")),
    P("לכן בינומית, עם $n=5$ ו-$p=\\frac16$.", do=show("st-on-s1", "st-a-s1"),
      say="לכן בינומית, עם אֶן שווה חמש, ופִּי שווה שישית."),
    P("בוחרים שלושה נציגים מכיתה של עשרים, ובה שמונה בנות, וסופרים כמה בנות. אותו תלמיד לא נבחר פעמיים.", do=show("st-r-s2")),
    P("המילה ״בוחרים״ אומרת בלי החזרה, מאוסף סופי. היפרגאומטרית.", do=show("st-on-s2", "st-a-s2")),
    P("בודקים ארבע נורות **שונות** מתוך שלושים. שוב אוסף סופי, ונורה שנבדקה יוצאת ממנו.", do=show("st-r-s3")),
    P("היפרגאומטרית, עם $N$ שלושים, $D$ חמש ו-$n$ ארבע.", do=show("st-on-s3", "st-a-s3", "st-t"),
      say="היפרגאומטרית, עם אֶן גדולה שלושים, דִּי חמש, ואֶן קטנה ארבע.", hold=0.4),
], stage=f'<div class="wm-col">{w.checklist("st", STORIES, size=30, hidden=True, width=1000)}</div>',
   panel=st.card("st-t", "trap", "⚠️ ״בוחרים״, ״מחלקים״, ״בודקים שונים״ בלי המילה ״מחזירים״: כמעט תמיד בלי החזרה"))

exam1 = Scene("exam1", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. בכד הראשון $N_1$ כדורים, ומהם $D_1$ אדומים.",
      say="ועכשיו סעיף ממבחן. בכד הראשון אֶן אחת כדורים, ומהם דִּי אחת אדומים."),
    P("לוקחים ממנו $n$ כדורים באקראי וללא החזרה. $X$ הוא מספר האדומים ביניהם. מהי פונקציית ההסתברות?",
      say="לוקחים ממנו אֶן כדורים באקראי וללא החזרה. אִקְס הוא מספר האדומים ביניהם. מהי פונקציית ההסתברות?"),
    P("שלב ראשון, לזהות את המודל. אוסף סופי, שליפה ללא החזרה: ההרכב משתנה. היפרגאומטרית.", do=show("x-pill")),
    P("מונים כמו בבחירת ועדה: בוחרים $k$ אדומים מתוך $D_1$, ואת השאר מתוך השחורים.", do=show("x-0"),
      say="מונים כמו בבחירת ועדה: בוחרים קֵיי אדומים מתוך דִּי אחת, ואת השאר מתוך השחורים."),
    P("ומחלקים במספר כל הבחירות של $n$ כדורים מתוך $N_1$.", do=hide("x-0") + show("x-1"),
      say="ומחלקים במספר כל הבחירות של אֶן כדורים מתוך אֶן אחת."),
    P("חלק שמפספסים: **אילו ערכים** $k$ יכול לקבל? לא תמיד מאפס עד $n$.", do=show("x-t"),
      say="חלק שמפספסים: אילו ערכים קֵיי יכול לקבל? לא תמיד מאפס עד אֶן."),
    P("למשל עשרה כדורים, שבעה מהם אדומים, ושולפים חמישה. יש רק שלושה שחורים.", do=show("x-2")),
    P("אז בין החמישה יש לפחות שני אדומים. ולמעלה, אי אפשר יותר מחמישה.", do=show("x-3")),
    P("בכלליות: $k$ בין המקסימום של אפס ו-$n$ פחות מספר השחורים, לבין המינימום של $n$ ו-$D_1$.", do=show("x-4"),
      say="בכלליות: קֵיי בין המקסימום של אפס, ואֶן פחות מספר השחורים, לבין המינימום של אֶן ודִּי אחת."),
    P("ובדיקה: סכום ההסתברויות על הערכים האלה הוא אחת, כמו שצריך.", do=show("x-ok"), hold=0.4),
], stage=f'<div class="wm-col" style="gap:16px">{w.pill("x-pill", "היפרגאומטרית: ללא החזרה")}'
         + w.eqs("x", ["$\\binom{D_1}{k}\\binom{N_1-D_1}{n-k}$",
                       "$P(X=k)=\\dfrac{\\binom{D_1}{k}\\binom{N_1-D_1}{n-k}}{\\binom{N_1}{n}}$",
                       "$N_1=10,\\ D_1=7,\\ n=5:\\ \\ N_1-D_1=3$",
                       "$2\\le k\\le 5$",
                       "$\\max\\{0,\\,n-(N_1-D_1)\\}\\le k\\le\\min\\{n,\\,D_1\\}$"], size=36, gap=12)
         + w.chip("x-ok", "סכום $=1$ ✓") + "</div>",
   panel=w.stem(Q1["id"], "בכד $N_1$ כדורים, מהם $D_1$ אדומים. לוקחים $n$ כדורים באקראי וללא החזרה. "
                "$X$ הוא מספר האדומים ביניהם. מהי פונקציית ההסתברות של $X$?")
         + st.card("x-t", "trap", "⚠️ הטווח של $k$: לא תמיד $0,\\dots,n$"))

exam2 = Scene("exam2", "ובכיוון ההפוך", [
    P("ועכשיו סעיף ממבחן אחר, שבו המלכודת הפוכה."),
    P("במחסן סוללות משני מפעלים, ו**הפרופורציה** של הסוללות ממפעל א׳ היא $q$. לוקחים למשלוח $n$ סוללות.",
      say="במחסן סוללות משני מפעלים, והפרופורציה של הסוללות ממפעל א היא קְיוּ. לוקחים למשלוח אֶן סוללות."),
    P("$X$ הוא מספר הסוללות ממפעל א׳ במשלוח. איך הוא מפולג?", say="אִקְס הוא מספר הסוללות ממפעל א במשלוח. איך הוא מפולג?"),
    P("כאן לא נתון גודל המחסן, ולא כמה סוללות בדיוק יש מכל מפעל. נתון רק **שיעור**.", do=show("y-c1")),
    P("לכן כל סוללה במשלוח היא ממפעל א׳ בהסתברות $q$, בלי תלות באחרות. זה ניסוי ברנולי.", do=show("y-0"),
      say="לכן כל סוללה במשלוח היא ממפעל א בהסתברות קְיוּ, בלי תלות באחרות. זה ניסוי ברנולי."),
    P("ו-$X$ הוא סכום של $n$ ניסויי ברנולי בלתי תלויים: בינומית, עם $n$ ו-$q$.", do=show("y-pill", "y-1"),
      say="ואִקְס הוא סכום של אֶן ניסויי ברנולי בלתי תלויים: בינומית, עם אֶן וקְיוּ."),
    P("המלכודת: לכתוב היפרגאומטרית. בשבילה צריך אוסף סופי עם $N$ ו-$D$ ידועים, וכאן אין כאלה.", do=show("y-t"),
      say="המלכודת: לכתוב היפרגאומטרית. בשבילה צריך אוסף סופי עם אֶן ודִּי ידועים, וכאן אין כאלה.", hold=0.4),
], stage=f'<div class="wm-col" style="gap:20px">{w.pill("y-pill", "בינומית: שיעור קבוע")}'
         + w.eqs("y", ["$X=\\sum_{j=1}^{n}X_j,\\qquad X_j\\sim\\mathrm{Ber}(q)$",
                       "$P(X=k)=\\binom nk q^k(1-q)^{n-k},\\quad k=0,\\dots,n$"], size=38, gap=18)
         + st.card("y-t", "trap", "⚠️ פרופורציה בלי גודל אוסף: לא היפרגאומטרית") + "</div>",
   panel=w.stem(Q2["id"], "במחסן סוללות משני מפעלים, ופרופורציית הסוללות ממפעל $A$ היא $q$. "
                "מכינים משלוח של $n$ סוללות. $X$ הוא מספר הסוללות ממפעל $A$. מצאו את פונקציית ההסתברות.")
         + st.card("y-c1", "ex", "נתון שיעור $q$, לא $N$ ו-$D$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לפני כל חישוב, שואלים אם ההרכב משתנה בין השליפות.", do=show("r-1")),
    P("לא משתנה, כי מחזירים או מטילים, או כי נתון רק שיעור: בינומית.", do=show("r-2")),
    P("משתנה, כי בוחרים בלי החזרה מאוסף סופי: היפרגאומטרית, ובודקים את טווח הערכים.", do=show("r-3")),
    P("והתוחלת זהה בשניהם, אבל ההסתברויות לא. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="wm-col">{w.checklist("rk", CK, size=32, width=900)}</div>',
   panel=st.card("r-1", "rule", "🔑 ההרכב משתנה בין השליפות?")
         + st.card("r-2", "rule", "🔑 לא: $\\mathrm{Bin}(n,p)$")
         + st.card("r-3", "rule", "🔑 כן: $\\mathrm{Hyp}(N,D,n)$ וטווח הערכים")
         + st.card("r-4", "trap", "⚠️ אותה תוחלת, התפלגות שונה"))

VIDEO = Video("W01", "which_model", "עם החזרה או בלי? בינומית מול היפרגאומטרית",
              [title, idea, bag, stories, exam1, exam2, recap],
              bank={"26A-B-Q5a": None, "25A-A-Q6a": None})
