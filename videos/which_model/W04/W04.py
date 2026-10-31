# -*- coding: utf-8 -*-
"""W04 · דילול ופיצול: מודל בתוך מודל — video script (build: tools/video/vid.py W04).

Source: courses/which_model/C04.js (lesson + goal: two filters one after the other become one distribution with a
multiplied parameter: Poisson thinning P(lambda p), and binomial of binomial Bin(n, pq)).
Exam anchors: 24A-E-Q5a (callers ~ P(lambda), each wins by a coin with probability p: the pmf of the number of
winners) and 24A-E-Q5c (its mean and variance). Neither is a quiz/boss id. Every thinning exam part has the same
structure as the boss items (25B-A-Q6b: registrants ~ P(lambda), born on that day; 24A-A-Q5b: students arrive, born
today), so this video takes a different story (prize callers) and never touches the "born on the day" stories;
not used on purpose: 25B-A-Q6b, 24A-D-Q5b (its twin), 24A-A-Q5b, 24S-A-Q5b, 24B-B-Q5b (its twins), 25A-A-Q6b, 25S-B-Q3b.
Not used on purpose (C04 quiz): 8 customers an hour buying with 0.25 (P(2)), 10 candidates with 0.7 and 0.2
(Bin(10, 0.14)); the lesson's lambda = 10, p = 0.1. Worked examples are new: 15 cars an hour past a camera, each
speeding with 0.2 (speeders P(3), the others P(12)), and two filters in a row on a Poisson stream (30 calls an hour,
a complaint with 1/5, escalated with 1/2: escalations P(3), P(at most one) = 4e^{-3}). No binomial-of-binomial example
and no step-by-step thinning proof on screen (the boss items 24A-A-Q5b / 25B-A-Q6b ask exactly for those); the exam
scene identifies the model, states the rule with its reason and reads off the mean and variance. The proof is still
checked symbolically in this file.
Every value is exact (sympy); every story is simulated literally (numpy).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R, binom, pois

# ---------------------------------------------------------------- example 1: 15 cars an hour, each speeds with 0.2
lam1, p1 = 15, R(1, 5)
assert lam1 * p1 == 3 and lam1 * (1 - p1) == 12
P0 = pois(3, 0)
assert w.dec(P0, 4) == "0.0498"
WRONG = binom(15, p1, 0)                                        # treating the average 15 as a fixed number of cars
assert w.dec(WRONG, 3) == "0.035" and abs(float(WRONG) - float(P0)) > 0.01
# independence of the split: P(speeders = a, others = b) = P(3)(a) * P(12)(b), from the two-stage story
for a in range(4):
    for b in range(4):
        joint = pois(15, a + b) * binom(a + b, p1, a)
        assert sp.simplify(joint - pois(3, a) * pois(12, b)) == 0


def proc(rng, n, rate, T=1.0, cap=80):
    return (np.cumsum(rng.exponential(1 / rate, (n, cap)), axis=1) <= T).sum(axis=1)


def gen_cars(rng, n):
    N = proc(rng, n, 15.0)
    S = rng.binomial(N, 0.2)
    return {"S": S, "O": N - S}


w.mc(gen_cars, [("S0", lambda d: d["S"] == 0, P0), ("ES", lambda d: d["S"], 3), ("EO", lambda d: d["O"], 12),
                ("S0O12", lambda d: (d["S"] == 0) & (d["O"] == 12), pois(3, 0) * pois(12, 12))])

# one realization for the picture: cars in one hour, the speeders marked
_rng = np.random.default_rng(5)
TIMES, t_ = [], 0.0
while True:
    t_ += _rng.exponential(1 / 15)
    if t_ > 1:
        break
    TIMES.append(t_)
MARK = list(_rng.random(len(TIMES)) < 0.2)
assert len(TIMES) == 16 and sum(MARK) == 4

# ---------------------------------------------------------------- example 2: two filters on a Poisson stream
lam2, q1, q2 = 30, R(1, 5), R(1, 2)
assert lam2 * q1 * q2 == 3
LE1 = pois(3, 0) + pois(3, 1)
assert sp.simplify(LE1 - 4 * sp.exp(-3)) == 0 and w.dec(LE1) == "0.199"
# two filters in a row = one filter with q1*q2 (each call is escalated with q1 q2, independently)
for kk in range(4):
    two = sum(float(pois(lam2, j)) * float(binom(j, q1, a_) * binom(a_, q2, kk)) for j in range(0, 90) for a_ in range(kk, j + 1))
    assert abs(float(two) - float(pois(3, kk))) < 1e-12


def gen_calls2(rng, n):
    N = proc(rng, n, 30.0, cap=90)
    C = rng.binomial(N, 0.2)
    return {"E": rng.binomial(C, 0.5)}


w.mc(gen_calls2, [("le1", lambda d: d["E"] <= 1, LE1), ("EE", lambda d: d["E"], 3)])

# ---------------------------------------------------------------- exam 24A-E-Q5a / Q5c
QA, QC = BANK["24A-E-Q5a"], BANK["24A-E-Q5c"]
assert "מטבע מוטה" in w.ctx_text(QA) and "משתנה פואסון בעל פרמטר $\\lambda>0$" in QA["question"]
assert "X\\sim P(p\\lambda)" in QA["solution"] and "\\operatorname{Var}[X]=p\\lambda" in QC["solution"]
j = sp.symbols("j", integer=True, nonnegative=True)
lam, p = sp.symbols("lambda p", positive=True)
for kk in range(4):
    s = sp.summation(sp.binomial(j, kk) * p ** kk * (1 - p) ** (j - kk) * sp.exp(-lam) * lam ** j / sp.factorial(j),
                     (j, kk, sp.oo))
    assert sp.simplify(s - sp.exp(-lam * p) * (lam * p) ** kk / sp.factorial(kk)) == 0
assert sp.simplify(sp.summation(sp.exp(-lam * p) * (lam * p) ** j / sp.factorial(j), (j, 0, sp.oo))) == 1


def gen_calls(rng, n, lv=4.4, pv=0.35):
    Y = rng.poisson(lv, n)
    return {"X": rng.binomial(Y, pv)}


LV, PV = R(44, 10), R(35, 100)
w.mc(gen_calls, [(f"X={kk}", lambda d, kk=kk: d["X"] == kk, pois(LV * PV, kk)) for kk in range(5)]
     + [("EX", lambda d: d["X"], LV * PV), ("VX", lambda d: (d["X"] - float(LV * PV)) ** 2, LV * PV)])

# ---------------------------------------------------------------- figures
TL = w.timeline("tl", TIMES, 1, ticks=[(0, "0"), (0.5, "½"), (1, "1")], marked=MARK, w=940, h=200)
PIPE = ('<div class="wm-rowx" style="gap:18px;font-size:34px;direction:rtl">'
        + w.box("pp-0", "מגיעים: $P(\\lambda)$", size=32, hidden=False) + '<span class="wm-big">←</span>'
        + w.box("pp-1", "עוברים מסנן: $p$", size=32, hidden=False) + "</div>")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר שאלות עם שני מסננים: קודם כמה הגיעו, ואז כמה מהם מקיימים עוד תכונה."),
    P("נראה שאין צורך בסכום ארוך: מחליפים הכול בהתפלגות אחת, עם פרמטר מוכפל."),
    P("ובסוף נפתור שאלה ממבחן מההתחלה ועד הסוף.", hold=0.4),
], stage='<div class="kicker">W04 · איזה מודל זה?</div><h1>דילול ופיצול</h1>'
         '<p>שני מסננים בזה אחר זה: $P(\\lambda)$ ואז $p$ נותן $P(\\lambda p)$, ו-$\\mathrm{Bin}(n,p)$ ואז $q$ נותן '
         '$\\mathrm{Bin}(n,pq)$.</p>', layout="title")

cars = Scene("cars", "דילול פואסון", [
    P("דוגמה. ליד מצלמה עוברות בממוצע חמש עשרה מכוניות בשעה, לפי פואסון.", do=show("tl-ev", "c-0")),
    P("כל מכונית חורגת מהמהירות בהסתברות חמישית, בלי תלות באחרות.", do=show("tl-evm", "c-1")),
    P("מה הסיכוי שבשעה מסוימת לא תעבור אף מכונית שחורגת?", do=show("c-q")),
    P("זה מודל בתוך מודל: המספר שהגיע אקראי, ומכל מי שהגיע רק חלק עובר את המסנן.", do=show("c-pipe")),
    P("והכלל: פואסון שכל אחד ממנו נספר בהסתברות $p$, בלי תלות, הוא שוב פואסון, עם $\\lambda$ כפול $p$.", do=show("c-r"),
      say="והכלל: פואסון שכל אחד ממנו נספר בהסתברות פִּי, בלי תלות, הוא שוב פואסון, עם למדא כפול פִּי."),
    P("כאן חמש עשרה כפול חמישית, שלוש. ואפס חורגות: $e$ בחזקת מינוס שלוש, בערך חמישה אחוזים.", do=show("c-2", "c-3"),
      say="כאן חמש עשרה כפול חמישית, שלוש. ואפס חורגות: אִי בחזקת מינוס שלוש, בערך חמישה אחוזים."),
    P("המלכודת: בינומית עם חמש עשרה ניסיונות. אבל חמש עשרה הוא רק **ממוצע**, לא מספר קבוע של מכוניות.", do=show("c-t", "c-4")),
    P("ובונוס, הפיצול: מספר המכוניות שלא חרגו הוא פואסון עם שתים עשרה, והוא **בלתי תלוי** במספר החורגות.",
      do=show("c-5"), hold=0.4),
], stage=f'<div class="wm-col" style="gap:26px">{TL}<div id="c-pipe" class="h">{PIPE}</div></div>',
   panel=w.eqs("c", ["$N\\sim P(15)$", "$p=0.2$", "$S\\sim P(15\\cdot0.2)=P(3)$", "$P(S=0)=e^{-3}\\approx0.0498$",
                     r"$\mathrm{Bin}(15,0.2):\ 0.8^{15}\approx0.035$ ✗",
                     r"$N-S\sim P(12)$"],
               size=32, gap=8)
         + w.box("c-q", "$P(S=0)$?", size=28)
         + st.card("c-r", "rule", "🔑 $P(\\lambda)$ ואז מסנן $p$: $P(\\lambda p)$")
         + st.card("c-t", "trap", "⚠️ $\\lambda$ הוא ממוצע, לא מספר ניסיונות"))

two = Scene("two", "שני מסננים ברצף", [
    P("ומה אם יש שני מסננים? למוקד מגיעות בממוצע שלושים שיחות בשעה, לפי פואסון.", do=show("s-0")),
    P("כל שיחה היא תלונה בהסתברות חמישית, וכל תלונה מועברת למנהל בהסתברות חצי. כמה שיחות מגיעות למנהל?",
      do=show("s-1")),
    P("לא צריך לפרק לפי מספר השיחות או התלונות. כל שיחה **עוברת את שני המסננים** בהסתברות חמישית כפול חצי, עשירית.",
      do=show("s-2")),
    P("ושיחות שונות לא תלויות זו בזו. אז זה דילול אחד, עם עשירית: פואסון עם שלושים כפול עשירית, כלומר שלוש.",
      do=show("s-pill", "s-3")),
    P("למשל לכל היותר שיחה אחת למנהל: $e$ בחזקת מינוס שלוש, כפול אחת ועוד שלוש. בערך עשרים אחוז.",
      do=show("s-4"), say="למשל לכל היותר שיחה אחת למנהל: אִי בחזקת מינוס שלוש, כפול אחת ועוד שלוש. בערך עשרים אחוז."),
    P("המלכודת: להשתמש רק במסנן אחד, חמישית או חצי. צריך את שניהם, מוכפלים.", do=show("s-t"), hold=0.4),
], stage=f'<div class="wm-col" style="gap:20px">{w.pill("s-pill", "פואסון: $P(30\\cdot\\tfrac15\\cdot\\tfrac12)=P(3)$")}'
         + w.eqs("s", ["$N\\sim P(30)$", "$\\text{complaint: }\\tfrac15,\\quad\\text{escalated: }\\tfrac12$",
                       "$\\tfrac15\\cdot\\tfrac12=\\tfrac1{10}$", "$E\\sim P(3)$",
                       "$P(E\\le1)=e^{-3}(1+3)\\approx0.199$"], size=38, gap=12) + "</div>",
   panel=st.card("s-r", "rule", "🔑 כמה מסננים בלתי תלויים: מכפילים את כולם").replace(' h"', '"')
         + st.card("s-t", "trap", "⚠️ רק מסנן אחד: $P(6)$ או $P(15)$ ✗"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. למוקד של מפעל הפיס מתקשרים אנשים, ומספר הפונים במשמרת הוא פואסוני עם $\\lambda$.",
      say="ועכשיו שאלה ממבחן. למוקד של מפעל הפיס מתקשרים אנשים, ומספר הפונים במשמרת הוא פואסוני עם למדא."),
    P("לכל פונה מטילים מטבע מוטה. אם יוצא עץ, בהסתברות $p$, הוא זוכה בפרס. מצאו את ההתפלגות של מספר הזוכים.",
      say="לכל פונה מטילים מטבע מוטה. אם יוצא עץ, בהסתברות פִּי, הוא זוכה בפרס. מצאו את ההתפלגות של מספר הזוכים."),
    P("זיהוי: שני שלבים. מספר הפונים פואסוני, ומכל פונה מטבע נפרד, בלתי תלוי באחרים. זה דילול.",
      do=show("x-pill", "x-0")),
    P("ולכן מספר הזוכים הוא שוב פואסון, עם $\\lambda$ כפול $p$.", do=show("x-1"),
      say="ולכן מספר הזוכים הוא שוב פואסון, עם למדא כפול פִּי."),
    P("במבחן מבקשים להראות את זה. הכלי הוא הסתברות שלמה לפי מספר הפונים, ובהינתן מספר הפונים, מספר הזוכים בינומי.",
      do=show("x-2")),
    P("בסוף הסכום מתקפל לטור של אקספוננט, ויוצא בדיוק פואסון עם $\\lambda p$.", do=show("x-ok"),
      say="בסוף הסכום מתקפל לטור של אקספוננט, ויוצא בדיוק פואסון עם למדא פִּי."),
    P("ולכן בסעיף הבא, התוחלת והשונות שתיהן $\\lambda p$, בלי שום חישוב נוסף.", do=show("x-3"),
      say="ולכן בסעיף הבא, התוחלת והשונות שתיהן למדא פִּי, בלי שום חישוב נוסף."),
    P("וגם הפונים שלא זכו הם פואסון, עם $\\lambda$ כפול אחת פחות $p$, ובלתי תלויים במספר הזוכים.", do=show("x-4"),
      say="וגם הפונים שלא זכו הם פואסון, עם למדא כפול, בסוגריים אחת פחות פִּי, ובלתי תלויים במספר הזוכים."),
    P("המלכודת: לכתוב בינומית עם $\\lambda$ ניסיונות. $\\lambda$ אפילו לא חייב להיות שלם.", do=show("x-t"),
      say="המלכודת: לכתוב בינומית עם למדא ניסיונות. למדא אפילו לא חייב להיות שלם.", hold=0.4),
], stage=f'<div class="wm-col" style="gap:16px">{w.pill("x-pill", "דילול פואסון")}'
         + w.eqs("x", ["$Y\\sim P(\\lambda),\\quad \\text{each caller wins w.p. } p$",
                       "$X\\sim P(\\lambda p)$",
                       "$P(X=k)=\\sum_{j\\ge k}P(X=k\\mid Y=j)\\,P(Y=j)$",
                       "$E[X]=\\mathrm{Var}(X)=\\lambda p$",
                       "$Y-X\\sim P(\\lambda(1-p))$"], size=36, gap=14)
         + w.chip("x-ok", "$P(X=k)=e^{-\\lambda p}\\dfrac{(\\lambda p)^k}{k!}$ ✓") + "</div>",
   panel=w.stem(QA["id"] + " · " + QC["id"][-2:], "מספר הפונים למוקד במשמרת $Y\\sim P(\\lambda)$. לכל פונה מטילים מטבע: "
                "״עץ״ (בהסתברות $p$) מזכה בפרס. $X$ הוא מספר הזוכים. מצאו את פונקציית ההסתברות של $X$, "
                "ואת $E[X]$ ו-$\\mathrm{Var}(X)$.", size=28)
         + st.card("x-t", "trap", "⚠️ לא $\\mathrm{Bin}(\\lambda,p)$: מספר הפונים אקראי"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כשיש שני מסננים בזה אחר זה, מכפילים את ההסתברויות שלהם.", do=show("r-1")),
    P("פואסון ואז מסנן: פואסון עם $\\lambda p$. והחלק שלא עבר הוא פואסון נפרד, בלתי תלוי.", do=show("r-2"),
      say="פואסון ואז מסנן: פואסון עם למדא פִּי. והחלק שלא עבר הוא פואסון נפרד, בלתי תלוי."),
    P("בינומית ואז מסנן: בינומית עם $n$ ועם $p$ כפול $q$.", do=show("r-3"),
      say="בינומית ואז מסנן: בינומית עם אֶן ועם פִּי כפול קְיוּ."),
    P("והממוצע $\\lambda$ הוא לא מספר קבוע של ניסיונות. נתראה ברמה הבאה.", do=show("r-4"),
      say="והממוצע למדא הוא לא מספר קבוע של ניסיונות. נתראה ברמה הבאה.", hold=0.6),
], stage=f'<div class="wm-col">{PIPE}</div>',
   panel=st.card("r-1", "rule", "🔑 שני מסננים: מכפילים")
         + st.card("r-2", "rule", "🔑 $P(\\lambda)\\to P(\\lambda p)$, ו-$P(\\lambda(1-p))$ בלתי תלוי")
         + st.card("r-3", "rule", "🔑 $\\mathrm{Bin}(n,p)\\to\\mathrm{Bin}(n,pq)$")
         + st.card("r-4", "trap", "⚠️ לא $\\mathrm{Bin}(\\lambda,p)$"))

VIDEO = Video("W04", "which_model", "דילול ופיצול: מודל בתוך מודל", [title, cars, two, exam, recap],
              bank={"24A-E-Q5a": None, "24A-E-Q5c": None})
