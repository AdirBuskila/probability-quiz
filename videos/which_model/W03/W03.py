# -*- coding: utf-8 -*-
"""W03 · אירועים נדירים: פואסון והקירוב — video script (build: tools/video/vid.py W03).

Source: courses/which_model/C03.js (lesson + goal: recognize a Poisson count, scale lambda with the window, use the
Poisson approximation of a binomial with large n and small p).
Exam part: an original "בסגנון מבחן" question (bank={}): typos at an average 0.3 per page, a 10-page chapter: P(at
least one) = 1 - e^{-3}; and the twist "at most one typo per page, with probability 0.3" -> Bin(10, 0.3). The bank has
no pure-Poisson exam part that is not a thinning question (24A-E-Q5 / 25S-B-Q3 are thinning, the C04 and boss
pattern of 25B-A-Q6b; 24A-D-Q5 is the twin of the boss context), so none is used here.
Not used on purpose (C03 quiz): 1.5 calls an hour in a 2-hour window (lambda 3, P(X = 3)), 100 chips with p = 0.02
(P(X >= 2) = 1 - 3e^{-2}); the lesson's 2 faults an hour, half an hour, e^{-1}. Worked examples are new: 5 calls an
hour, a half-hour window (lambda 2.5, P(X = 0) and P(X <= 2)), and 300 bulbs with p = 0.01 against P(3).
Every value is exact (sympy, e symbolic) and cross-checked by simulating the literal story (numpy).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide
import stage as st
import w_which_model as w
from w_which_model import R, binom, pois

# ---------------------------------------------------------------- example 1: 5 calls an hour, half an hour
rate, win = 5, R(1, 2)
lam = rate * win
assert lam == R(5, 2)
P0 = pois(lam, 0)
Ple2 = sum(pois(lam, k) for k in range(3))
assert sp.simplify(Ple2 - R(53, 8) * sp.exp(-R(5, 2))) == 0           # (1 + 2.5 + 3.125) e^{-2.5}
assert w.dec(P0) == "0.082" and w.dec(Ple2) == "0.544"
assert abs(float(sum(k * pois(lam, k) for k in range(80))) - float(lam)) < 1e-12   # mean = lambda (truncated series)
KS = list(range(8))
PO = {k: pois(lam, k) for k in KS}
assert max(PO, key=lambda k: float(PO[k])) == 2


def proc(rng, n, rate, T, cap=60):
    gaps = rng.exponential(1 / rate, (n, cap))
    return (np.cumsum(gaps, axis=1) <= T).sum(axis=1)


def gen_calls(rng, n):
    return {"X": proc(rng, n, 5.0, 0.5)}


w.mc(gen_calls, [("P0", lambda d: d["X"] == 0, P0), ("Ple2", lambda d: d["X"] <= 2, Ple2), ("E", lambda d: d["X"], lam)])

# one realization of the process over two hours, for the picture (counts per half hour are read off it)
_rng = np.random.default_rng(31)
TIMES = []
t_ = 0.0
while True:
    t_ += _rng.exponential(1 / 5)
    if t_ > 2:
        break
    TIMES.append(round(t_, 3))
CNT = [sum(1 for t in TIMES if a < t <= a + 0.5) for a in (0, 0.5, 1.0, 1.5)]
assert sum(CNT) == len(TIMES) and CNT[:2] == [2, 6]                 # different half hours, different counts

# ---------------------------------------------------------------- example 2: 300 bulbs, p = 0.01
n2, p2 = 300, R(1, 100)
lam2 = n2 * p2
assert lam2 == 3
EX0, AP0 = binom(n2, p2, 0), pois(lam2, 0)
assert w.dec(EX0, 4) == "0.049" and w.dec(AP0, 4) == "0.0498"
assert abs(float(EX0) - float(AP0)) < 0.001
B2 = {k: binom(n2, p2, k) for k in KS}
P2 = {k: pois(lam2, k) for k in KS}
assert max(abs(float(B2[k]) - float(P2[k])) for k in KS) < 0.003


def gen_bulbs(rng, n):
    return {"X": rng.binomial(n2, 0.01, n)}


w.mc(gen_bulbs, [("X0", lambda d: d["X"] == 0, EX0)])

# ---------------------------------------------------------------- exam-style: typos
lam3 = R(3, 10) * 10
assert lam3 == 3
A1 = 1 - pois(lam3, 0)
A2 = 1 - binom(10, R(3, 10), 0)
assert w.dec(A1) == "0.95" and w.dec(A2) == "0.972"
assert A2 == 1 - R(7, 10) ** 10 and float(A2) > float(A1)
assert w.dec(R(7, 10) ** 10, 4) == "0.0282" and w.dec(sp.exp(-3), 4) == "0.0498"


def gen_typos(rng, n):
    return {"P": proc(rng, n, 0.3, 10.0), "B": (rng.random((n, 10)) < 0.3).sum(axis=1)}


w.mc(gen_typos, [("pois>=1", lambda d: d["P"] >= 1, A1), ("bin>=1", lambda d: d["B"] >= 1, A2)])

# ---------------------------------------------------------------- figures
TL = w.timeline("tl", TIMES, 2, windows=[("w1", 0, 0.5, "{n} שיחות"), ("w2", 0.5, 1.0, "{n} שיחות")],
                ticks=[(0, "0"), (0.5, "½"), (1, "1"), (1.5, "1½"), (2, "2")], w=940, h=220)
PB = w.bars("pb", KS, [("po", PO, "a", None)], w=900, h=380, nd=3, title="P(2.5)", shown=("po",))
CMP = w.bars("cb", KS, [("bin", B2, "b", "בינומית מדויקת"), ("poi", P2, "a", "פואסון, קירוב")], w=900, h=420, nd=3)
CK = [("rate", "אירועים בקצב ממוצע, בזמן או בשטח", "פואסון"),
      ("cap", "אין תקרה ואין מספר ניסויים נתון", "פואסון"),
      ("np", "$n$ גדול, $p$ קטן, ומבקשים קירוב", "$P(np)$")]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את המודל של אירועים נדירים: פואסון."),
    P("נלמד לזהות אותו, להתאים את הפרמטר לאורך החלון, ולהשתמש בו כקירוב לבינומית."),
    P("ובסוף נפתור שאלה בסגנון מבחן, עם תפנית.", hold=0.4),
], stage='<div class="kicker">W03 · איזה מודל זה?</div><h1>אירועים נדירים: פואסון</h1>'
         '<p>לזהות פואסון, להתאים את $\\lambda$ לאורך החלון, ולקרב בינומית עם $n$ גדול ו-$p$ קטן.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("פואסון סופר אירועים שקורים בקצב ממוצע קבוע, בזמן או בשטח, ובלי תלות זה בזה.", do=show("ck-r-rate", "ck-on-rate", "ck-a-rate")),
    P("למשל שיחות למוקד. כל נקודה כאן היא שיחה, וחוץ מהקצב אין שום סדר.", do=show("tl-ev")),
    P("שימו לב מה **אין** כאן: אין מספר ניסויים נתון, ואין תקרה. בכל חלון יכולות להגיע כמה שיחות שרוצים.",
      do=show("ck-r-cap", "ck-on-cap", "ck-a-cap")),
    P("בחצי השעה הראשונה הגיעו כאן שתי שיחות, ובשנייה שש. המספר עצמו אקראי.",
      do=show("tl-win-w1", "tl-cnt-w1", "tl-win-w2", "tl-cnt-w2")),
    P("הנוסחה: $e$ בחזקת מינוס $\\lambda$, כפול $\\lambda$ בחזקת $k$, חלקי $k$ עצרת. והתוחלת והשונות שתיהן $\\lambda$.",
      do=show("i-0", "i-1"),
      say="הנוסחה: אִי בחזקת מינוס למדא, כפול למדא בחזקת קֵיי, חלקי קֵיי עצרת. והתוחלת והשונות שתיהן למדא.", hold=0.4),
], stage=f'<div class="wm-col" style="gap:30px">{TL}{w.checklist("ck", CK, size=30, hidden=True, width=900)}</div>',
   panel=w.eqs("i", ["$P(X=k)=e^{-\\lambda}\\dfrac{\\lambda^k}{k!},\\quad k=0,1,2,\\dots$",
                     "$E[X]=\\mathrm{Var}(X)=\\lambda$"], size=34, gap=24))

window = Scene("window", "הפרמטר גדל עם החלון", [
    P("דוגמה. למוקד מגיעות בממוצע חמש שיחות בשעה. מה הסיכוי שבחצי שעה לא תגיע אף שיחה?", do=show("w-q")),
    P("הצעד הראשון הוא $\\lambda$ של **החלון**, לא של שעה. הקצב כפול אורך החלון: חמש כפול חצי, שתיים וחצי.",
      do=show("w-0", "w-r"), say="הצעד הראשון הוא למדא של החלון, לא של שעה. הקצב כפול אורך החלון: חמש כפול חצי, שתיים וחצי."),
    P("ועכשיו אפס שיחות: $e$ בחזקת מינוס שתיים וחצי, בערך שמונה אחוזים.", do=show("pb", "w-1", "pb-c-0", "pb-v-po-0"),
      say="ועכשיו אפס שיחות: אִי בחזקת מינוס שתיים וחצי, בערך שמונה אחוזים."),
    P("ולכל היותר שתי שיחות: מחברים את שלוש העמודות הראשונות.", do=show("pb-c-1", "pb-c-2", "pb-v-po-1", "pb-v-po-2", "w-2")),
    P("אחת, ועוד שתיים וחצי, ועוד שתיים וחצי בריבוע חלקי שתיים. כפול $e$ בחזקת מינוס שתיים וחצי. בערך חמישים וארבעה אחוזים.",
      do=show("w-3"), say="אחת, ועוד שתיים וחצי, ועוד שתיים וחצי בריבוע חלקי שתיים. כפול אִי בחזקת מינוס שתיים וחצי. בערך חמישים וארבעה אחוזים."),
    P("המלכודת: להשתמש בחמש, הקצב לשעה, כשהחלון הוא חצי שעה.", do=show("w-t"), hold=0.4),
], stage=f'<div class="wm-col">{PB}</div>',
   panel=w.box("w-q", "5 שיחות בשעה בממוצע. חלון: חצי שעה.", size=28)
         + w.eqs("w", ["$\\lambda=5\\cdot\\frac12=2.5$", "$P(X=0)=e^{-2.5}\\approx0.082$",
                       "$P(X\\le2)=e^{-2.5}\\left(1+2.5+\\frac{2.5^2}{2}\\right)$", "$\\approx0.544$"], size=32, gap=10)
         + st.card("w-r", "rule", "🔑 $\\lambda=$ קצב $\\times$ אורך החלון")
         + st.card("w-t", "trap", "⚠️ לא $\\lambda=5$: זה הקצב לשעה"))

approx = Scene("approx", "קירוב לבינומית", [
    P("שימוש שני של פואסון: קירוב. במשלוח שלוש מאות נורות, וכל אחת פגומה בהסתברות אחוז אחד, בלי תלות.", do=show("a-q")),
    P("המודל המדויק הוא בינומית, כי יש מספר קבוע של ניסיונות. אבל $n$ גדול ו-$p$ קטן.", do=show("cb", "cb-s-bin"),
      say="המודל המדויק הוא בינומית, כי יש מספר קבוע של ניסיונות. אבל אֶן גדול ופִּי קטן."),
    P("במצב כזה הבינומית כמעט זהה לפואסון עם $\\lambda$ שווה $n$ כפול $p$, כלומר שלוש.", do=show("cb-s-poi", "a-0"),
      say="במצב כזה הבינומית כמעט זהה לפואסון עם למדא שווה אֶן כפול פִּי, כלומר שלוש."),
    P("למשל אף נורה פגומה: הבינומית נותנת אפס נקודה תשעים ותשע בחזקת שלוש מאות. הקירוב נותן $e$ בחזקת מינוס שלוש.",
      do=show("cb-c-0", "a-1", "a-2"),
      say="למשל אף נורה פגומה: הבינומית נותנת אפס נקודה תשעים ותשע בחזקת שלוש מאות. הקירוב נותן אִי בחזקת מינוס שלוש."),
    P("שני המספרים קרובים מאוד, והקירוב חוסך מקדמי בינום וחזקות ענקיות.", do=show("a-r")),
    P("אבל קירוב הוא קירוב. משתמשים בו כשהשאלה מבקשת אותו, או כשאין דרך אחרת לחשב.", hold=0.4),
], stage=f'<div class="wm-col">{CMP}</div>',
   panel=w.box("a-q", "300 נורות, כל אחת פגומה בהסתברות $0.01$", size=28)
         + w.eqs("a", ["$\\lambda=np=300\\cdot0.01=3$", "$\\mathrm{Bin}:\\ 0.99^{300}\\approx0.0490$",
                       "$P(3):\\ e^{-3}\\approx0.0498$"], size=32, gap=10)
         + st.card("a-r", "rule", "🔑 $n$ גדול, $p$ קטן: $\\mathrm{Bin}(n,p)\\approx P(np)$"))

exam = Scene("exam", "בסגנון מבחן", [
    P("ועכשיו שאלה בסגנון מבחן. בספר מופיעות שגיאות דפוס בקצב ממוצע של שלוש עשיריות לעמוד, בלי תלות."),
    P("מה הסיכוי שבפרק של עשרה עמודים תהיה לפחות שגיאה אחת?"),
    P("זיהוי: קצב ממוצע, בלי תקרה לשגיאות בעמוד, ובלי מספר ניסיונות. פואסון.", do=show("x-pill1")),
    P("$\\lambda$ של הפרק: שלוש עשיריות כפול עשרה, כלומר שלוש.", do=show("x-0"),
      say="למדא של הפרק: שלוש עשיריות כפול עשרה, כלומר שלוש."),
    P("ו״לפחות אחת״ מחשבים דרך המשלים: אחת פחות $e$ בחזקת מינוס שלוש, בערך תשעים וחמישה אחוזים.", do=show("x-1"),
      say="ולפחות אחת, מחשבים דרך המשלים: אחת פחות אִי בחזקת מינוס שלוש, בערך תשעים וחמישה אחוזים."),
    P("התפנית: נניח שבכל עמוד יש **לכל היותר** שגיאה אחת, והיא מופיעה בהסתברות שלוש עשיריות.", do=show("x-q2")),
    P("עכשיו יש תקרה: לכל היותר עשר שגיאות, ועשרה ניסיונות בלתי תלויים. זו כבר בינומית.", do=show("x-pill2", "x-2")),
    P("אין אף שגיאה רק אם כל עשרת העמודים נקיים. לכן אחת פחות שבע עשיריות בחזקת עשר: תשעים ושבעה אחוזים.", do=show("x-3")),
    P("אותו ממוצע, שלוש שגיאות, אבל מודל אחר ותשובה אחרת. מה שהכריע הוא התקרה.", do=show("x-t"), hold=0.4),
], stage=f'<div class="wm-col" style="gap:16px">{w.pill("x-pill1", "פואסון: קצב, בלי תקרה")}'
         + w.eqs("x", ["$\\lambda=0.3\\cdot10=3$", "$P(X\\ge1)=1-e^{-3}\\approx0.950$",
                       "$X\\sim\\mathrm{Bin}(10,\\,0.3)$", "$P(X\\ge1)=1-0.7^{10}\\approx0.972$"], size=38, gap=14)
         + w.pill("x-pill2", "בינומית: לכל היותר אחת בעמוד") + "</div>",
   panel=w.stem("בסגנון מבחן", "בספר יש שגיאות דפוס בקצב ממוצע של $0.3$ לעמוד, בלי תלות. מה ההסתברות שבפרק של 10 עמודים "
                "יש לפחות שגיאה אחת?", size=28)
         + w.box("x-q2", "ואם בכל עמוד יש <b>לכל היותר</b> שגיאה אחת, והיא מופיעה בהסתברות $0.3$ בלי תלות?", size=28)
         + st.card("x-t", "trap", "⚠️ יש תקרה או מספר ניסיונות ידוע: לא פואסון"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: פואסון סופר אירועים בקצב ממוצע, בלי תקרה ובלי מספר ניסיונות נתון.", do=show("r-1")),
    P("$\\lambda$ הוא הקצב כפול אורך החלון, ותמיד מחשבים אותו מחדש לחלון של השאלה.", do=show("r-2"),
      say="למדא הוא הקצב כפול אורך החלון, ותמיד מחשבים אותו מחדש לחלון של השאלה."),
    P("בינומית עם $n$ גדול ו-$p$ קטן מתקרבת לפואסון עם $n$ כפול $p$.", do=show("r-3"),
      say="בינומית עם אֶן גדול ופִּי קטן מתקרבת לפואסון עם אֶן כפול פִּי."),
    P("ואם יש תקרה, זה לא פואסון. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="wm-col">{w.checklist("rk", CK, size=30, width=900)}</div>',
   panel=st.card("r-1", "rule", "🔑 קצב, בלי תקרה: $P(\\lambda)$")
         + st.card("r-2", "rule", "🔑 $\\lambda=$ קצב $\\times$ חלון")
         + st.card("r-3", "rule", "🔑 $\\mathrm{Bin}(n,p)\\approx P(np)$")
         + st.card("r-4", "trap", "⚠️ יש תקרה: לא פואסון"))

VIDEO = Video("W03", "which_model", "אירועים נדירים: פואסון והקירוב",
              [title, idea, window, approx, exam, recap], bank={})
