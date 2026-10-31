# -*- coding: utf-8 -*-
"""J07 · מינימום ומקסימום של בחירות בדידות — video script (build: tools/video/vid.py J07).

Source: courses/joint/C07.js (lesson + goal: the joint pmf of (min, max) of two or more discrete picks, with and
without replacement).
Exam part: an original question "בסגנון מבחן" (bank={}). The bank's 25A-C-Q5c (general n out of {1..N}) is NOT
used: with n = 2 its formula is the answer of the boss item 25A-B-Q6b (two chairs out of N). For the same reason
the video never shows the two-picks-without-replacement table or its 2/(N(N-1)) cell.
The exam-style question fixes n = 4 (four distinct numbers out of {1..N}): P(min = k, max = l) = C(l-k-1, 2)/C(N, 4)
for l - k >= 3; it reduces to neither the boss case (n = 2) nor the C07 quiz case (n = 3, N = 10, (2,7)).
Not used on purpose: every C07 quiz item (two fair dice with (2,5), (3,3) and max - min = 1; two of {1..6} without
replacement with (2,5) and the 15 positive cells; three of {1..10} with (2,7)).
Worked examples are new: a fair four-sided die rolled twice (the full 4x4 table: 1/16 on the diagonal, 1/8 above,
0 below), and N = 9, n = 4, (k, l) = (2, 7) (C(4,2)/C(9,4) = 6/126 = 1/21).
Every table is an exact enumeration (itertools, w_joint) and the exam formula is checked against full enumeration
for every N <= 9 and 2 <= n <= N, and by Monte Carlo.
"""
import itertools
from math import comb

import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, Space, Joint, eq

# ---------------------------------------------------------------- with replacement: a four-sided die, twice
D4 = Space.uniform([{"a": a, "b": b} for a in range(1, 5) for b in range(1, 5)])
JW = D4.joint(lambda o: min(o["a"], o["b"]), lambda o: max(o["a"], o["b"]))
JW = Joint({(j, k): JW(j, k) for j in range(1, 5) for k in range(1, 5)}, xs=[1, 2, 3, 4], ys=[1, 2, 3, 4])
for j in range(1, 5):
    for k in range(1, 5):
        assert JW(j, k) == (R(2, 16) if j < k else R(1, 16) if j == k else 0)
assert JW(1, 3) == R(1, 8) and JW(2, 2) == R(1, 16) and JW(3, 1) == 0
assert 4 * R(1, 16) + 6 * R(2, 16) == 1 and 4 * R(1, 16) + 6 * R(1, 16) == R(10, 16)

# ---------------------------------------------------------------- without replacement: two of {1,2,3,4}
U2 = Space.uniform([{"a": a, "b": b} for a in range(1, 5) for b in range(1, 5) if a != b])
JN = U2.joint(lambda o: min(o["a"], o["b"]), lambda o: max(o["a"], o["b"]))
JN = Joint({(j, k): JN(j, k) for j in range(1, 5) for k in range(1, 5)}, xs=[1, 2, 3, 4], ys=[1, 2, 3, 4])
for j in range(1, 5):
    for k in range(1, 5):
        assert JN(j, k) == (R(1, 6) if j < k else 0)
assert len(U2.out) == 12 and sum(1 for v in JN.c.values() if v) == 6


def gen_d4(rng, n):
    a, b = rng.integers(1, 5, n), rng.integers(1, 5, n)
    return {"m": np.minimum(a, b), "M": np.maximum(a, b)}


w.mc(gen_d4, [("P(1,3)", lambda d: (d["m"] == 1) & (d["M"] == 3), R(1, 8)),
              ("P(2,2)", lambda d: (d["m"] == 2) & (d["M"] == 2), R(1, 16))])

# ---------------------------------------------------------------- the min/max formula (checked for every n; shown for n = 4)


def formula(N, n, k, l):
    return R(comb(l - k - 1, n - 2), comb(N, n)) if (1 <= k < l <= N and l - k - 1 >= n - 2) else R(0)


for N in range(2, 10):
    for n in range(2, N + 1):
        cnt = {}
        for S in itertools.combinations(range(1, N + 1), n):
            cnt[(min(S), max(S))] = cnt.get((min(S), max(S)), 0) + 1
        tot = comb(N, n)
        for k in range(1, N + 1):
            for l in range(1, N + 1):
                assert R(cnt.get((k, l), 0), tot) == formula(N, n, k, l), (N, n, k, l)
        assert sum(comb(l - k - 1, n - 2) for k in range(1, N + 1) for l in range(k + 1, N + 1)) == tot
# the worked instance N = 9, n = 4, (k, l) = (2, 7)
assert comb(7 - 2 - 1, 4 - 2) == comb(4, 2) == 6 and comb(9, 4) == 126 and formula(9, 4, 2, 7) == R(1, 21)
assert comb(7 - 2, 4 - 2) == 10                                   # the pitfall: endpoints counted, 10/126
assert formula(9, 4, 2, 4) == 0 and comb(4 - 2 - 1, 2) == 0        # too close: l - k - 1 < n - 2
for N in range(4, 10):                                            # the n = 4 answer and its range l - k >= 3
    for k in range(1, N + 1):
        for l in range(1, N + 1):
            assert formula(N, 4, k, l) == (R(comb(l - k - 1, 2), comb(N, 4)) if l - k >= 3 else 0)
assert sum(comb(l - k - 1, 2) for k in range(1, 10) for l in range(k + 3, 10)) == 126


def gen_ex(rng, n):
    S = np.argsort(rng.random((n, 9)), axis=1)[:, :4] + 1
    return {"m": S.min(axis=1), "M": S.max(axis=1)}


w.mc(gen_ex, [("P(2,7)", lambda d: (d["m"] == 2) & (d["M"] == 7), R(1, 21)),
              ("P(2,4)", lambda d: (d["m"] == 2) & (d["M"] == 4), 0)])

TW = w.table("tw", JW, cells="frac", xname="j", yname="k", size=32, pad="8px 22px")
above = [(j - 1, k - 1) for j in range(1, 5) for k in range(1, 5) if j < k]
diag = [(i, i) for i in range(4)]
below = [(j - 1, k - 1) for j in range(1, 5) for k in range(1, 5) if j > k]
LINE = w.cards("nl", [[f"${i}$"] for i in range(1, 10)], size=34, minw=70, maxw=1000, shown=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבנה טבלה משותפת של המינימום והמקסימום של כמה בחירות."),
    P("נראה מה משתנה בין בחירה עם החזרה לבחירה בלי החזרה, ומה קורה כשבוחרים יותר משני מספרים."),
    P("ובסוף נפתור שאלה בסגנון מבחן.", hold=0.4),
], stage='<div class="kicker">J07 · משתנים משותפים</div><h1>מינימום ומקסימום של בחירות בדידות</h1>'
         '<p>למצוא את ההסתברות המשותפת של $(\\min,\\max)$, עם החזרה וללא החזרה, לשני מספרים או יותר.</p>',
   layout="title")

withr = Scene("with", "עם החזרה", [
    P("מטילים פעמיים קובייה הוגנת עם ארבע פאות. יש שש עשרה תוצאות מסודרות, כל אחת בהסתברות אחת חלקי שש עשרה.",
      do=show("w-0")),
    P("המינימום הוא השורה, והמקסימום הוא העמודה. ותמיד המינימום קטן או שווה למקסימום."),
    P("לכן כל התאים מתחת לאלכסון הם אפס.", do=show(*w.ids("tw", "v", below), *w.ids("tw", "w", below))),
    P("תא מעל האלכסון, למשל מינימום אחת ומקסימום שלוש. שתי תוצאות נותנות אותו: אחת ואז שלוש, או שלוש ואז אחת.",
      do=hide(*w.ids("tw", "w", below)) + show("tw-h-0-2", "tw-v-0-2", "w-c1")),
    P("לכן הוא שתיים חלקי שש עשרה, כלומר שמינית. וכך כל תא מעל האלכסון.",
      do=hide("tw-h-0-2") + show(*w.ids("tw", "v", above))),
    P("על האלכסון, למשל שתיים ושתיים: רק תוצאה אחת, שתיים ואז שתיים. אין סדר שני.",
      do=show("tw-h-1-1", "tw-v-1-1", "w-c2")),
    P("לכן תא באלכסון הוא אחת חלקי שש עשרה.", do=hide("tw-h-1-1") + show(*w.ids("tw", "v", diag))),
    P("בדיקה: ארבעה תאים באלכסון ושישה מעליו. ארבע חלקי שש עשרה ועוד שתים עשרה חלקי שש עשרה, בדיוק אחת.",
      do=show("w-ok")),
    P("המלכודת: לשכוח את הגורם שתיים מעל האלכסון. אז הסכום יוצא עשר חלקי שש עשרה, ולא אחת.", do=show("w-t")),
    P("ועוד מלכודת: לתת הסתברות לתא שבו המינימום גדול מהמקסימום. תא כזה תמיד אפס.", hold=0.4),
], stage=f'<div class="jt-col">{TW}</div>',
   panel=st.card("w-0", "plain", "$4^2=16$ תוצאות מסודרות, כל אחת $\\tfrac1{16}$")
         + st.card("w-c1", "rule", "🔑 $j&lt;k$: שני סדרים, $\\tfrac2{16}$")
         + st.card("w-c2", "rule", "🔑 $j=k$: סדר אחד, $\\tfrac1{16}$")
         + w.chip("w-ok", "$4\\cdot\\tfrac1{16}+6\\cdot\\tfrac2{16}=1$ ✓")
         + st.card("w-t", "trap", "⚠️ בלי ה-$2$: $4\\cdot\\tfrac1{16}+6\\cdot\\tfrac1{16}=\\tfrac{10}{16}$"))

exam = Scene("exam", "בסגנון מבחן", [
    P("ועכשיו שאלה בסגנון מבחן. בוחרים ארבעה מספרים שונים באקראי, בלי החזרה, מתוך אחת עד $N$.",
      say="ועכשיו שאלה בסגנון מבחן. בוחרים ארבעה מספרים שונים באקראי, בלי החזרה, מתוך אחת עד אֶן גדולה."),
    P("מבקשים את ההסתברות המשותפת שהמינימום הוא $k$ והמקסימום הוא $\\ell$.",
      say="מבקשים את ההסתברות המשותפת שהמינימום הוא קֵיי והמקסימום הוא אֶל."),
    P("כאן הסדר לא חשוב: כל קבוצה של ארבעה מספרים שווה הסתברות, ויש $N$ בחר ארבע קבוצות כאלה.", do=show("x-0"),
      say="כאן הסדר לא חשוב: כל קבוצה של ארבעה מספרים שווה הסתברות, ויש אֶן גדולה בחר ארבע קבוצות כאלה."),
    P("נראה דוגמה: תשעה מספרים, בוחרים ארבעה, ורוצים מינימום שתיים ומקסימום שבע.", do=show("nl")),
    P("אז שתיים ושבע חייבים להיבחר.", do=show("nl-oh-1", "nl-oh-6")),
    P("ואסור שייבחר משהו מתחת לשתיים או מעל שבע, אחרת המינימום או המקסימום ישתנו.",
      do=show("nl-ow-0", "nl-ow-7", "nl-ow-8")),
    P("שני המספרים הנותרים נבחרים **ממש בין** שתיים לשבע: מתוך שלוש, ארבע, חמש ושש.",
      do=hide("nl-ow-0", "nl-ow-7", "nl-ow-8") + show("nl-ow-2", "nl-ow-3", "nl-ow-4", "nl-ow-5")),
    P("ארבעה בחר שתיים, כלומר שש קבוצות. מתוך תשעה בחר ארבעה, מאה עשרים ושש. הסתברות אחת חלקי עשרים ואחת.",
      do=show("x-1")),
    P("ובאופן כללי: בין $k$ ל-$\\ell$ יש $\\ell$ פחות $k$ פחות אחת מספרים, ומהם בוחרים את שני הנותרים.",
      do=show("x-2"),
      say="ובאופן כללי: בין קֵיי לאֶל יש אֶל פחות קֵיי פחות אחת מספרים, ומהם בוחרים את שני הנותרים."),
    P("מחלקים במספר כל הקבוצות, וזו התשובה.", do=show("x-ok")),
    P("והערכים האפשריים: צריך מקום לשני מספרים באמצע, ולכן $\\ell$ גדול מ-$k$ לפחות בשלוש.",
      say="והערכים האפשריים: צריך מקום לשני מספרים באמצע, ולכן אֶל גדול מקֵיי לפחות בשלוש."),
    P("אם הם קרובים יותר, המקדם הבינומי אפס, וההסתברות אפס. למשל מינימום שתיים ומקסימום ארבע: רק שלוש באמצע.",
      say="אם הם קרובים יותר, המקדם הבינומי אפס, וההסתברות אפס. למשל מינימום שתיים ומקסימום ארבע: רק שלוש באמצע."),
    P("המלכודת: לספור גם את הקצוות, ולבחור מתוך $\\ell$ פחות $k$ מספרים. אבל $k$ ו-$\\ell$ כבר נבחרו.",
      do=show("x-t"),
      say="המלכודת: לספור גם את הקצוות, ולבחור מתוך אֶל פחות קֵיי מספרים. אבל קֵיי ואֶל כבר נבחרו."),
    P("וכל קבוצה נספרת פעם אחת בדיוק, אצל המינימום והמקסימום שלה. לכן סכום כל התאים הוא אחת.", hold=0.6),
], stage=f'<div class="jt-col" style="gap:30px">{LINE}'
         + w.eqs("x", ["$|\\Omega|=\\binom{N}{4}$", "$\\dfrac{\\binom42}{\\binom94}=\\dfrac6{126}=\\dfrac1{21}$",
                       "$P(X_{\\mathrm{min}}=k,\\ X_{\\mathrm{max}}=\\ell)=\\dfrac{\\binom{\\ell-k-1}{2}}{\\binom N4}$"], size=40, gap=18)
         + "</div>",
   panel=w.stem("בסגנון מבחן", "ארבעה מספרים נבחרים באקראי וללא החזרה מתוך $\\{1,\\dots,N\\}$. חשבו את "
                "$P(X_{\\mathrm{min}}=k,\\ X_{\\mathrm{max}}=\\ell)$ וציינו את הערכים האפשריים.")
         + w.chip("x-ok", "$1\\le k,\\ \\ k+3\\le\\ell\\le N$")
         + st.card("x-t", "trap", "⚠️ הקצוות כבר נבחרו: בוחרים מתוך $\\ell-k-1$ מספרים, ולא מתוך $\\ell-k$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: המינימום תמיד קטן או שווה למקסימום, ולכן מתחת לאלכסון הכול אפס.", do=show("r-1")),
    P("עם החזרה, תא מעל האלכסון מקבל שני סדרים, ותא באלכסון סדר אחד.", do=show("r-2")),
    P("בלי החזרה אי אפשר לקבל אותו מספר פעמיים, ולכן גם האלכסון אפס.", do=show("r-3")),
    P("וכשבוחרים כמה מספרים, שאר המספרים נבחרים ממש בין המינימום למקסימום. נתראה ברמה הבאה.", do=show("r-4"),
      hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$\\dfrac{\\binom{\\ell-k-1}{2}}{\\binom N4}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $\\min&gt;\\max$: $0$")
         + st.card("r-2", "rule", "🔑 עם החזרה: $\\tfrac2{N^2}$ מעל האלכסון, $\\tfrac1{N^2}$ עליו")
         + st.card("r-3", "trap", "⚠️ בלי החזרה: האלכסון $0$")
         + st.card("r-4", "rule", "🔑 השאר ממש בין $k$ ל-$\\ell$"))

VIDEO = Video("J07", "joint", "מינימום ומקסימום של בחירות בדידות", [title, withr, exam, recap],
              bank={})
