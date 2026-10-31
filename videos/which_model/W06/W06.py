# -*- coding: utf-8 -*-
"""W06 · משפחה אקראית או ילד אקראי? הטיית גודל — video script (build: tools/video/vid.py W06).

Source: courses/which_model/C06.js (lesson + goal: tell choosing a group from choosing an item inside it; an item
picks its group with weight proportional to the group's size: P = k p_k / E[X], E = E[X^2] / E[X]).
Exam anchors: 24B-C-Q5a and 24B-C-Q5b (N boxes of screws n_1..n_N: the mean size of a random box, and of the box of a
random screw). Neither is a quiz/boss id. Its content twins 24B-A-Q5a/b and 25S-C-Q6a/b (families at a meeting) are
not used anywhere either; this video shows only the screws.
Not used on purpose (C06 quiz): the town with 1/3/4/2 families of sizes 1..4, the buses with 10, 20, 50; the lesson's
two families of 1 and 3. Worked example is new: a restaurant with 4 tables of 1, 2, 4, 5 diners (a random table: 3; a
random diner: 23/6; P(table of 5) = 5/12 vs 1/4), and the boxes 2, 5, 13 to put numbers on the exam's formulas.
Everything is exact (sympy Rationals) and simulated by picking a table / a diner / a screw literally (numpy).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_which_model as w
from w_which_model import R

# ---------------------------------------------------------------- example: tables of 1, 2, 4, 5 diners
T = [1, 2, 4, 5]
ET = R(sum(T), len(T))
assert ET == 3
DINERS = [s for s in T for _ in range(s)]                       # one entry per diner: the size of their table
ED = R(sum(DINERS), len(DINERS))
assert len(DINERS) == 12 and ED == R(46, 12) == R(23, 6) and w.dec(ED, 2) == "3.83"
assert ED == R(sum(s * s for s in T), sum(T))                   # E[X^2] / E[X]
EX2 = R(sum(s * s for s in T), len(T))
assert EX2 / ET == ED and ED - ET == (EX2 - ET ** 2) / ET       # the excess is Var/E >= 0
P5_table, P5_diner = R(1, 4), R(5, 12)
assert P5_diner == R(5 * 1, 4) / ET * 1 and P5_diner == R(DINERS.count(5), 12)   # k p_k / E[X]


def gen_rest(rng, n):
    return {"t": np.array(T)[rng.integers(0, 4, n)], "d": np.array(DINERS)[rng.integers(0, 12, n)]}


w.mc(gen_rest, [("Et", lambda d: d["t"], ET), ("Ed", lambda d: d["d"], ED), ("P5", lambda d: d["d"] == 5, P5_diner)])

# at least 4 at the table: a random table 2/4, a random diner 9/12
assert R(sum(1 for t in T if t >= 4), 4) == R(1, 2) and R(sum(1 for d in DINERS if d >= 4), 12) == R(3, 4)

# ---------------------------------------------------------------- spot it: a random day and the length of its month
MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
assert sum(MONTHS) == 365
EMON = R(365, 12)
EDAY = R(sum(m * m for m in MONTHS), 365)
assert EDAY == R(11111, 365) and w.dec(EMON, 2) == "30.42" and w.dec(EDAY, 2) == "30.44" and EDAY > EMON
DAYS = np.array([m for m in MONTHS for _ in range(m)])
w.mc(lambda rng, n: {"d": DAYS[rng.integers(0, 365, n)]}, [("Eday", lambda d: d["d"], EDAY)])

# ---------------------------------------------------------------- exam 24B-C-Q5a / Q5b
QA, QB = BANK["24B-C-Q5a"], BANK["24B-C-Q5b"]
assert "קופסאות" in w.ctx_text(QA) and "בורג אחד" in QB["question"]
assert "\\frac{n_1+n_2+\\cdots+n_N}{N}" in QA["solution"]
assert "\\frac{n_1^2+n_2^2+\\cdots+n_N^2}{n_1+n_2+\\cdots+n_N}" in QB["solution"]
BOX = [2, 5, 13]
EA = R(sum(BOX), 3)
EB = R(sum(b * b for b in BOX), sum(BOX))
assert EA == R(20, 3) and EB == R(198, 20) == R(99, 10) and EB > EA
# general: sum n^2 / sum n >= sum n / N (Cauchy-Schwarz), equality only when all the n_i are equal
n1, n2, n3 = sp.symbols("n1 n2 n3", positive=True)
diff = sp.together((n1**2 + n2**2 + n3**2) / (n1 + n2 + n3) - (n1 + n2 + n3) / 3)
assert sp.expand(sp.numer(diff) - ((n1 - n2)**2 + (n1 - n3)**2 + (n2 - n3)**2)) == 0


def gen_screws(rng, n):
    screws = np.array([b for b in BOX for _ in range(b)])
    return {"a": np.array(BOX)[rng.integers(0, 3, n)], "b": screws[rng.integers(0, len(screws), n)]}


w.mc(gen_screws, [("Ea", lambda d: d["a"], EA), ("Eb", lambda d: d["b"], EB)])

# ---------------------------------------------------------------- figures
TABLES = w.groups("tb", T, labels=[f"שולחן של {s}" if s > 1 else "שולחן של 1" for s in T], dot=30, per_row=3)
BOXES = w.groups("bx", BOX, labels=["2", "5", "13"], dot=24, per_row=5)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר מלכודת שאין לה שם של התפלגות בשאלה: הטיית גודל."),
    P("השאלה שמכריעה היא מה בוחרים באקראי: קבוצה, או פריט מתוך הקבוצות."),
    P("ובסוף נפתור שאלה ממבחן על קופסאות של ברגים.", hold=0.4),
], stage='<div class="kicker">W06 · איזה מודל זה?</div><h1>קבוצה אקראית או פריט אקראי?</h1>'
         '<p>להבדיל בין בחירת קבוצה לבחירת פריט מתוכה, ולהשתמש במשקלים הנכונים.</p>', layout="title")

rest = Scene("rest", "השולחנות", [
    P("במסעדה ארבעה שולחנות: עם סועד אחד, שניים, ארבעה וחמישה.", do=show("tb")),
    P("ניסוי ראשון: בוחרים **שולחן** אקראי. לכל שולחן סיכוי רבע, והגודל הממוצע הוא שלוש.", do=show("e-0", "e-1")),
    P("ניסוי שני: בוחרים **סועד** אקראי, מבין כל שנים עשר הסועדים, ושואלים כמה יושבים בשולחן שלו.",
      do=show(*[f"tb-gd{i}" for i in range(4)])),
    P("עכשיו השולחן של החמישה נבחר בכל פעם שבוחרים אחד מחמשת הסועדים שלו. חמישה מתוך שתים עשרה, ולא רבע.",
      do=show("tb-gh3", "e-2")),
    P("כל שולחן נספר כמספר הסועדים בו. לכן הממוצע הוא סכום הריבועים, חלקי שתים עשרה: שלוש נקודה שמונים ושלוש.",
      do=hide("tb-gh3") + show("e-3")),
    P("סועד אקראי רואה שולחן גדול יותר מהממוצע, פשוט כי רוב הסועדים יושבים בשולחנות הגדולים.", do=show("e-r")),
    P("והנוסחה הכללית: התוחלת של $X$ בריבוע, חלקי התוחלת של $X$. היא תמיד לפחות התוחלת הרגילה.", do=show("e-4"),
      say="והנוסחה הכללית: התוחלת של אִקְס בריבוע, חלקי התוחלת של אִקְס. היא תמיד לפחות התוחלת הרגילה."),
    P("וגם הסתברויות משתנות. שולחן של לפחות ארבעה: חצי מהשולחנות, אבל שלושה רבעים מהסועדים.",
      do=show("tb-gh2", "tb-gh3"), hold=0.4),
], stage=f'<div class="wm-col" style="gap:30px">{TABLES}</div>',
   panel=w.eqs("e", ["$P(\\text{table}=5)=\\frac14$", "$E[X]=\\frac{1+2+4+5}{4}=3$",
                     "$P(\\text{diner's table}=5)=\\frac{5}{12}$",
                     "$E[\\tilde X]=\\frac{1^2+2^2+4^2+5^2}{12}=\\frac{46}{12}\\approx3.83$",
                     "$E[\\tilde X]=\\dfrac{E[X^2]}{E[X]}\\ge E[X]$"], size=31, gap=12)
         + st.card("e-r", "rule", "🔑 בוחרים פריט: משקל כל קבוצה כגודלה"))

SPOT = [("s1", "בוחרים כיתה אקראית בבית הספר. כמה תלמידים בה?", "קבוצה: ממוצע רגיל"),
        ("s2", "שואלים תלמיד אקראי כמה תלמידים בכיתה שלו", "פריט: הטיית גודל"),
        ("s3", "בוחרים יום אקראי בשנה. כמה ימים בחודש שלו?", "פריט: הטיית גודל")]
spot = Scene("spot", "איך מזהים", [
    P("איך מזהים את זה בשאלה? מחפשים את מי שנבחר באקראי."),
    P("״בוחרים כיתה אקראית״: הקבוצה נבחרה. כל כיתה באותו משקל, ממוצע רגיל.", do=show("sp-r-s1", "sp-on-s1", "sp-a-s1")),
    P("״תלמיד אקראי, וכמה בכיתה שלו״: נבחר פריט, והכיתות הגדולות מקבלות משקל גדול יותר.",
      do=show("sp-r-s2", "sp-on-s2", "sp-a-s2")),
    P("ומקרה פחות צפוי: יום אקראי בשנה, וכמה ימים בחודש שלו. גם כאן נבחר פריט, יום, מתוך קבוצה, חודש.",
      do=show("sp-r-s3", "sp-on-s3", "sp-a-s3")),
    P("חודש אקראי: שלושים נקודה ארבעים ושתיים ימים בממוצע. יום אקראי: שלושים נקודה ארבעים וארבע. הבדל קטן.",
      do=show("sp-0", "sp-1")),
    P("ההטיה גדולה רק כשהגדלים שונים מאוד זה מזה, כמו בשולחנות.", do=show("sp-r"), hold=0.4),
], stage=f'<div class="wm-col">{w.checklist("sp", SPOT, size=29, hidden=True, width=1000)}</div>',
   panel=w.eqs("sp", [r"$\text{month: }\frac{365}{12}\approx30.42$",
                      r"$\text{day: }\frac{\sum m_i^2}{365}=\frac{11111}{365}\approx30.44$"], size=32, gap=14)
         + st.card("sp-r", "rule", r"🔑 ההפרש הוא $\mathrm{Var}(X)/E[X]$: גדל עם הפיזור"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. יש $N$ קופסאות ממוספרות, ובקופסה ה-$i$ יש $n_i$ ברגים.",
      say="ועכשיו שאלה ממבחן. יש אֶן קופסאות ממוספרות, ובקופסה ה-אַיי יש אֶן אַיי ברגים."),
    P("סעיף ראשון: בוחרים **קופסה** אקראית. כמה ברגים יש בה בממוצע?"),
    P("כל קופסה נבחרת בהסתברות אחת חלקי $N$, אז זה פשוט הממוצע של כל ה-$n_i$.", do=show("x-0"),
      say="כל קופסה נבחרת בהסתברות אחת חלקי אֶן, אז זה פשוט הממוצע של כל האֶן אַיי."),
    P("סעיף שני: שופכים את כל הברגים ומערבבים, ובוחרים **בורג** אקראי. כמה ברגים היו בקופסה שלו, בממוצע?"),
    P("עכשיו נבחר פריט. הבורג שייך לקופסה ה-$i$ בהסתברות $n_i$ חלקי מספר הברגים הכולל.", do=show("x-1"),
      say="עכשיו נבחר פריט. הבורג שייך לקופסה ה-אַיי בהסתברות אֶן אַיי, חלקי מספר הברגים הכולל."),
    P("ובקופסה הזאת $n_i$ ברגים. לכן התוחלת היא סכום הריבועים חלקי סכום ה-$n_i$.", do=show("x-2"),
      say="ובקופסה הזאת אֶן אַיי ברגים. לכן התוחלת היא סכום הריבועים חלקי סכום האֶן אַיי."),
    P("במספרים: קופסאות עם שניים, חמישה ושלושה עשר ברגים. קופסה אקראית: שש נקודה שישים ושבע בממוצע.",
      do=show("bxw", "x-3")),
    P("בורג אקראי: מאה תשעים ושמונה חלקי עשרים, תשע נקודה תשע. הקופסה הגדולה מושכת את רוב הברגים.",
      do=show("bx-gd2", "x-4")),
    P("המלכודת: לחשב גם בסעיף השני עם אחת חלקי $N$, ולקבל אותה תשובה כמו בראשון.", do=show("x-t"),
      say="המלכודת: לחשב גם בסעיף השני עם אחת חלקי אֶן, ולקבל אותה תשובה כמו בראשון.", hold=0.4),
], stage='<div class="wm-col" style="gap:16px">' + w.eqs("x", [
    "$E[X]=\\dfrac{n_1+\\dots+n_N}{N}$",
    "$P(\\text{box } i)=\\dfrac{n_i}{n_1+\\dots+n_N}$",
    "$E[Y]=\\dfrac{n_1^2+\\dots+n_N^2}{n_1+\\dots+n_N}$",
    "$E[X]=\\frac{2+5+13}{3}\\approx6.67$",
    "$E[Y]=\\frac{4+25+169}{20}=9.9$"], size=34, gap=10)
         + f'<div id="bxw" class="h">{BOXES}</div></div>',
   panel=w.stem(QA["id"] + " · " + QB["id"][-2:], "$N$ קופסאות, ובקופסה ה-$i$ יש $n_i$ ברגים. (א) בוחרים קופסה "
                "באקראי: כמה ברגים בממוצע? (ב) מערבבים את כל הברגים ובוחרים בורג: כמה ברגים בממוצע היו בקופסה שלו?",
                size=28)
         + st.card("x-t", "trap", "⚠️ בסעיף ב׳ לא $\\frac1N$: הבורג בוחר קופסה לפי גודלה"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לפני החישוב שואלים מי נבחר באקראי. הקבוצה, או פריט מתוכה?", do=show("r-1")),
    P("קבוצה אקראית: כל קבוצה באותו משקל, ממוצע רגיל.", do=show("r-2")),
    P("פריט אקראי: כל קבוצה במשקל של הגודל שלה, ולכן תוחלת הריבוע חלקי התוחלת.", do=show("r-3")),
    P("והתשובה השנייה תמיד גדולה או שווה לראשונה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="wm-col">{TABLES.replace("tb-", "rt-").replace(chr(34) + "tb" + chr(34), chr(34) + "rt" + chr(34))}</div>',
   panel=st.card("r-1", "rule", "🔑 מי נבחר: קבוצה או פריט?")
         + st.card("r-2", "rule", "🔑 קבוצה: $E[X]$")
         + st.card("r-3", "rule", "🔑 פריט: $E[X^2]/E[X]$")
         + st.card("r-4", "trap", "⚠️ $E[X^2]/E[X]\\ge E[X]$"))

VIDEO = Video("W06", "which_model", "משפחה אקראית או ילד אקראי? הטיית גודל", [title, rest, spot, exam, recap],
              bank={"24B-C-Q5a": None, "24B-C-Q5b": None})
