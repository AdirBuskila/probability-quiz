# -*- coding: utf-8 -*-
"""J01 · טבלת ההתפלגות המשותפת — video script (build: tools/video/vid.py J01).

Source: courses/joint/C01.js (lesson + goal: build the joint table from the list of outcomes, check that it sums to
1, fill a missing cell).
Exam anchor: 24S-B-Q3a (a biased coin tossed three times, X = heads in the first two, Y = heads in all three; the
joint pmf and the normalization). No guided quiz uses it; it is NOT the boss item 24S-A-Q3a (there Y counts the last
two tosses, here all three: a different table with 4 columns).
Not used on purpose: every C01 quiz item (the table with k = 0.25, the cells 0.4/0.3/0.2/0.2, the fair three-toss
table of the lesson with its cells (1,1) and (2,0), the two dice with Y = [sum >= 10]).
Worked examples are new: an urn with two red balls and one blue, two draws without replacement (X = reds drawn,
Y = 1 if the first is red: two outcomes per cell and one impossible cell), and a 2x3 table with a missing cell
k = 0.15.
Every table is built by grouping an enumerated outcome list (w_joint.Space.joint, exact sympy) and cross-checked by a
Monte Carlo run of the real experiment.
"""
import pathlib
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, Space, Joint, eq

ROOT = pathlib.Path(__file__).resolve().parents[3]

# ---------------------------------------------------------------- example 1: urn {R1, R2, B}, two draws, no replacement
BALLS = ["R_1", "R_2", "B"]
ORD = [("R_1", "R_2"), ("R_2", "R_1"), ("R_1", "B"), ("R_2", "B"), ("B", "R_1"), ("B", "R_2")]
assert sorted(ORD) == sorted((a, b) for a in BALLS for b in BALLS if a != b)          # all 6 ordered draws
U = Space.uniform([{"a": a, "b": b} for a, b in ORD])
red = lambda s: 1 if s.startswith("R") else 0
fX = lambda o: red(o["a"]) + red(o["b"])           # reds drawn
fY = lambda o: red(o["a"])                         # 1 if the first ball is red
JU = U.joint(fX, fY)
assert JU.xs == [1, 2] and JU.ys == [0, 1]
assert JU(1, 0) == R(1, 3) and JU(1, 1) == R(1, 3) and JU(2, 1) == R(1, 3) and JU(2, 0) == 0
assert [(fX(o), fY(o)) for _, o in U.out].count((1, 0)) == 2                          # two outcomes in cell (1,0)


def gen_urn(rng, n):
    perm = np.argsort(rng.random((n, 3)), axis=1)    # a random order of the balls 0,1 (red) and 2 (blue)
    a, b = perm[:, 0], perm[:, 1]
    return {"X": (a < 2).astype(int) + (b < 2).astype(int), "Y": (a < 2).astype(int)}


w.mc(gen_urn, [(f"P({x},{y})", (lambda d, x=x, y=y: (d["X"] == x) & (d["Y"] == y)), JU(x, y))
               for x in JU.xs for y in JU.ys])

# ---------------------------------------------------------------- example 2: a missing cell
KNOWN = {(0, 0): R(12, 100), (0, 1): R(18, 100), (0, 2): R(30, 100), (1, 0): R(5, 100), (1, 2): R(20, 100)}
assert sum(KNOWN.values()) == R(85, 100)
K = 1 - sum(KNOWN.values())
assert K == R(15, 100) and 0 <= K <= 1
JK = Joint({**KNOWN, (1, 1): K})
JKcells = {k: (w.dec(v, 2, fixed=True), v) for k, v in KNOWN.items()}
JKcells[(1, 1)] = ("k", K)

# ---------------------------------------------------------------- exam 24S-B-Q3a
Q = BANK["24S-B-Q3a"]
CTX = "24S-B-c3"
import json
_ctx = json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))["contexts"][CTX]["text"]
assert Q["contextId"] == CTX and "בסדרה של שלוש ההטלות" in _ctx and "בשתי ההטלות הראשונות" in _ctx
S3 = Space.product({"X1": [(0, 1 - p), (1, p)], "X2": [(0, 1 - p), (1, p)], "X3": [(0, 1 - p), (1, p)]})
gX = lambda o: o["X1"] + o["X2"]
gY = lambda o: o["X1"] + o["X2"] + o["X3"]
J = S3.joint(gX, gY)
assert J.xs == [0, 1, 2] and J.ys == [0, 1, 2, 3]
CELLS = {(0, 0): ("(1-p)^3", (1 - p) ** 3), (0, 1): ("p(1-p)^2", p * (1 - p) ** 2),
         (1, 1): ("2p(1-p)^2", 2 * p * (1 - p) ** 2), (1, 2): ("2p^2(1-p)", 2 * p ** 2 * (1 - p)),
         (2, 2): ("p^2(1-p)", p ** 2 * (1 - p)), (2, 3): ("p^3", p ** 3)}
for x in J.xs:
    for y in J.ys:
        if (x, y) not in CELLS:
            CELLS[(x, y)] = ("0", 0)
            assert J(x, y) == 0 and not (x <= y <= x + 1)          # zero exactly where y is not x or x+1
        else:
            assert eq(J(x, y), CELLS[(x, y)][1]) and x <= y <= x + 1
assert sum(1 for v in J.c.values() if v != 0) == 6
assert eq(sum(e for _, e in CELLS.values()), ((1 - p) + p) ** 3) and eq(J.total(), 1)
# the official table agrees with ours
for t in ["(1-p)^3", "2p(1-p)^2", "2p^2(1-p)", "p^2(1-p)", "p^3"]:
    assert t in Q["solution"].replace(" ", ""), t
# the eight outcomes in the order shown, with (x, y) and probability
OUTS = ["000", "100", "010", "001", "110", "101", "011", "111"]
OUTP = []
for s in OUTS:
    o = {"X1": int(s[0]), "X2": int(s[1]), "X3": int(s[2])}
    h = s.count("1")
    pr = [wt for wt, oo in S3.out if oo == o][0]
    assert eq(pr, p ** h * (1 - p) ** (3 - h))
    OUTP.append((gX(o), gY(o), h))
PTEX = {0: "(1-p)^3", 1: "p(1-p)^2", 2: "p^2(1-p)", 3: "p^3"}


def gen3(rng, n, pv=0.3):
    t = (rng.random((n, 3)) < pv).astype(int)
    return {"X": t[:, 0] + t[:, 1], "Y": t.sum(axis=1)}


JN = J.subs({p: R(3, 10)})
w.mc(gen3, [(f"P({x},{y})", (lambda d, x=x, y=y: (d["X"] == x) & (d["Y"] == y)), JN(x, y))
            for x in J.xs for y in J.ys])

# ---------------------------------------------------------------- figures
UC = w.cards("u", [[f"${a}{b}$", f"$({fX({'a': a, 'b': b})},{fY({'a': a, 'b': b})})$", "$\\frac16$"] for a, b in ORD],
             size=30, minw=120)
UT = w.table("ut", JU, cells="frac", size=38, pad="10px 34px")
KT = w.table("kt", JK, cells=JKcells, size=36, shown=True, pad="10px 30px")
EC = w.cards("e", [[f"${s}$", f"$({x},{y})$", f"${PTEX[h]}$"] for s, (x, y, h) in zip(OUTS, OUTP)], size=26, minw=112, maxw=620)
ET = w.table("et", J, cells=CELLS, size=30, pad="8px 18px")
pos = lambda x, y: w.pos(J, x, y)
iu = lambda x, y: w.pos(JU, x, y)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את הטבלה המשותפת של שני משתנים מקריים."),
    P("נבנה אותה מרשימת התוצאות, נבדוק שהסכום שלה אחת, ונשלים תא חסר."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">J01 · משתנים משותפים</div><h1>טבלת ההתפלגות המשותפת</h1>'
         '<p>לבנות טבלה משותפת מרשימת כל התוצאות, לבדוק שהסכום שלה $1$, ולהשלים תא חסר.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("לפעמים בניסוי אחד מודדים שני משתנים מקריים, $X$ ו-$Y$.", say="לפעמים בניסוי אחד מודדים שני משתנים מקריים, אִקְס ווַואי."),
    P("ההסתברות המשותפת אומרת מה הסיכוי ששני ערכים מתקבלים **יחד**, באותה תוצאה.", do=show("i-f")),
    P("מסדרים אותה בטבלה: שורה לכל ערך של $X$, ועמודה לכל ערך של $Y$.", do=show("i-c1"),
      say="מסדרים אותה בטבלה: שורה לכל ערך של אִקְס, ועמודה לכל ערך של וַואי."),
    P("טבלה תקינה מקיימת שני תנאים. כל תא הוא מספר בין אפס לאחת.", do=show("i-c2")),
    P("וסכום **כל** התאים יחד הוא בדיוק אחת. זו תכונת הנרמול.", do=show("i-c3"), hold=0.4),
], stage='<div class="jt-col"><div id="i-f" class="jt-big h">$P_{XY}(x,y)=P(X=x,\\ Y=y)$</div>'
         + st.card("i-c1", "ex", "שורה לכל $x$, עמודה לכל $y$") + "</div>",
   panel=st.card("i-c2", "rule", "🔑 כל תא בין $0$ ל-$1$")
         + st.card("i-c3", "rule", "🔑 $\\displaystyle\\sum_x\\sum_y P_{XY}(x,y)=1$"))

urn = Scene("urn", "מתוצאות לטבלה", [
    P("דוגמה. בכד שני כדורים אדומים וכדור כחול אחד. מוציאים שניים, בזה אחר זה, בלי החזרה.", do=show("n-0")),
    P("$X$ הוא מספר האדומים שהוצאנו, ו-$Y$ שווה אחת אם הכדור הראשון אדום, ואפס אחרת.", do=show("n-1"),
      say="אִקְס הוא מספר האדומים שהוצאנו, ווַואי שווה אחת אם הכדור הראשון אדום, ואפס אחרת."),
    P("שלב ראשון: רושמים את כל התוצאות. יש שש הוצאות מסודרות, וכולן שוות הסתברות: שישית.",
      do=show(*[f"u-o-{k}" for k in range(6)])),
    P("לכל תוצאה מחשבים את הזוג. למשל, כחול ואחריו אדום: אדום אחד, והראשון לא אדום. הזוג אחת אפס.",
      do=show(*[f"u-l-{k}-1" for k in range(6)], *[f"u-l-{k}-2" for k in range(6)], "u-oh-4")),
    P("שלב שני: **מקבצים**. התא אחת אפס מקבל את כל התוצאות שנותנות את הזוג הזה.", do=show("ut", "u-oh-5")),
    P("יש שתיים כאלה, ולכן התא הוא שתי שישיות, כלומר שליש.",
      do=show(f"ut-h-{iu(1, 0)[0]}-{iu(1, 0)[1]}", f"ut-v-{iu(1, 0)[0]}-{iu(1, 0)[1]}")),
    P("באותו אופן, אדום ואחריו כחול נותן את הזוג אחת אחת. גם כאן שתי תוצאות, ושליש.",
      do=hide("u-oh-4", "u-oh-5", f"ut-h-{iu(1, 0)[0]}-{iu(1, 0)[1]}") + show("u-oh-2", "u-oh-3", f"ut-v-{iu(1, 1)[0]}-{iu(1, 1)[1]}")),
    P("ושני אדומים נותנים את הזוג שתיים אחת: שוב שליש.",
      do=hide("u-oh-2", "u-oh-3") + show("u-oh-0", "u-oh-1", f"ut-v-{iu(2, 1)[0]}-{iu(2, 1)[1]}")),
    P("ומה עם התא שתיים אפס? שני אדומים, והראשון לא אדום. זה בלתי אפשרי.",
      do=hide("u-oh-0", "u-oh-1") + show(f"ut-w-{iu(2, 0)[0]}-{iu(2, 0)[1]}")),
    P("אף תוצאה לא מגיעה אליו, ולכן רושמים בו **אפס**. לא משאירים תא ריק.",
      do=show(f"ut-v-{iu(2, 0)[0]}-{iu(2, 0)[1]}", "n-z")),
    P("בדיקה: שליש ועוד שליש ועוד שליש ועוד אפס. הסכום אחת, והטבלה תקינה.",
      do=hide(f"ut-w-{iu(2, 0)[0]}-{iu(2, 0)[1]}") + show("n-ok"), hold=0.4),
], stage=f'<div class="jt-col">{UC}{UT}</div>',
   panel=st.card("n-0", "plain", "כד: $R_1,\\ R_2,\\ B$. שתי הוצאות, בלי החזרה")
         + st.card("n-1", "ex", "$X$ = מספר האדומים<br>$Y=1$ אם הראשון אדום")
         + st.card("n-z", "rule", "🔑 תא שאף תוצאה לא מגיעה אליו: $0$")
         + w.chip("n-ok", "סכום $=1$ ✓"))

miss = Scene("miss", "תא חסר", [
    P("עכשיו טבלה שאחד התאים בה חסר, ומסומן באות $k$.", do=show("kt"),
      say="עכשיו טבלה שאחד התאים בה חסר, ומסומן באות קֵיי."),
    P("איך מוצאים אותו? בעזרת תכונת הנרמול: הסכום של כל התאים הוא אחת.", do=show("k-c1")),
    P("מחברים את חמשת התאים הידועים, ומקבלים אפס נקודה שמונים וחמש.", do=show("k-0")),
    P("לכן $k$ הוא אחת פחות אפס נקודה שמונים וחמש, כלומר אפס נקודה חמש עשרה.", do=show("k-1", "kt-h-1-1"),
      say="לכן קֵיי הוא אחת פחות אפס נקודה שמונים וחמש, כלומר אפס נקודה חמש עשרה."),
    P("והוא בין אפס לאחת, אז הטבלה תקינה.", do=show("k-ok")),
    P("ושימו לב: אילו התאים הידועים היו מסתכמים ביותר מאחת, $k$ היה יוצא שלילי.", do=show("k-t"),
      say="ושימו לב: אילו התאים הידועים היו מסתכמים ביותר מאחת, קֵיי היה יוצא שלילי."),
    P("אז אין שום $k$ שמתקן אותה, והטבלה פשוט לא תקינה.", hold=0.4,
      say="אז אין שום קֵיי שמתקן אותה, והטבלה פשוט לא תקינה."),
], stage=f'<div class="jt-col">{KT}'
         + w.eqs("k", ["$0.12+0.18+0.30+0.05+0.20=0.85$", "$k=1-0.85=0.15$"], size=38)
         + w.chip("k-ok", "$0\\le k\\le 1$ ✓") + "</div>",
   panel=st.card("k-c1", "rule", "🔑 תא חסר הוא $1$ פחות סכום כל השאר")
         + st.card("k-t", "trap", "⚠️ אם הידועים כבר מעל $1$: אין $k$ תקין"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. מטילים מטבע מוטה שלוש פעמים, ובכל הטלה עץ בהסתברות $p$.",
      say="ועכשיו סעיף ממבחן. מטילים מטבע מוטה שלוש פעמים, ובכל הטלה עץ בהסתברות פִּי."),
    P("$X$ הוא מספר העצים בשתי ההטלות הראשונות, ו-$Y$ הוא מספר העצים בכל שלוש ההטלות.",
      say="אִקְס הוא מספר העצים בשתי ההטלות הראשונות, ווַואי הוא מספר העצים בכל שלוש ההטלות."),
    P("מבקשים את הטבלה המשותפת, ולוודא שתכונת הנרמול מתקיימת."),
    P("שלב ראשון: שמונה התוצאות. הספרה אחת מסמנת עץ.", do=show(*[f"e-o-{k}" for k in range(8)])),
    P("לכל תוצאה מחשבים את הזוג. למשל, אחת אפס אחת: בשתי הראשונות עץ אחד, ובסך הכול שניים.",
      do=show(*[f"e-l-{k}-1" for k in range(8)], "e-oh-5")),
    P("ההסתברות של תוצאה היא מכפלה: $p$ לכל עץ, ואחת פחות $p$ לכל פלי, כי ההטלות בלתי תלויות.",
      do=hide("e-oh-5") + show(*[f"e-l-{k}-2" for k in range(8)]),
      say="ההסתברות של תוצאה היא מכפלה: פִּי לכל עץ, ואחת פחות פִּי לכל פלי, כי ההטלות בלתי תלויות."),
    P("שלב שני: מקבצים. לתא אחת אחת מגיעות **שתי** תוצאות: אחת אפס אפס, ואפס אחת אפס.",
      do=show("et", "e-oh-1", "e-oh-2", f"et-h-{pos(1, 1)[0]}-{pos(1, 1)[1]}")),
    P("כל אחת מהן היא $p$ כפול אחת פחות $p$, בסוגריים, בריבוע, ולכן התא הוא פעמיים זה.",
      do=show(f"et-v-{pos(1, 1)[0]}-{pos(1, 1)[1]}"),
      say="כל אחת מהן היא פִּי כפול אחת פחות פִּי, בסוגריים, בריבוע, ולכן התא הוא פעמיים זה."),
    P("גם לתא אחת שתיים מגיעות שתי תוצאות: אחת אפס אחת, ואפס אחת אחת.",
      do=hide("e-oh-1", "e-oh-2", f"et-h-{pos(1, 1)[0]}-{pos(1, 1)[1]}")
      + show("e-oh-5", "e-oh-6", f"et-h-{pos(1, 2)[0]}-{pos(1, 2)[1]}", f"et-v-{pos(1, 2)[0]}-{pos(1, 2)[1]}")),
    P("כל אחד מארבעת התאים האחרים מקבל תוצאה אחת בלבד.",
      do=hide("e-oh-5", "e-oh-6", f"et-h-{pos(1, 2)[0]}-{pos(1, 2)[1]}")
      + show(*[f"et-v-{pos(x, y)[0]}-{pos(x, y)[1]}" for x, y in [(0, 0), (0, 1), (2, 2), (2, 3)]])),
    P("ושישה תאים נשארים בלי אף תוצאה, ולכן הם אפס.",
      do=show(*[f"et-v-{pos(x, y)[0]}-{pos(x, y)[1]}" for x, y in CELLS if CELLS[(x, y)][1] == 0])),
    P("למה דווקא הם? כי $Y$ **כולל** את $X$: הוא $X$ ועוד ההטלה השלישית.", do=show("x-t"),
      say="למה דווקא הם? כי וַואי כולל את אִקְס: הוא אִקְס ועוד ההטלה השלישית."),
    P("לכן $Y$ שווה ל-$X$ או ל-$X$ ועוד אחת, וכל תא אחר בלתי אפשרי.", do=show(
        *[f"et-w-{pos(x, y)[0]}-{pos(x, y)[1]}" for x, y in CELLS if CELLS[(x, y)][1] == 0]),
      say="לכן וַואי שווה לאִקְס או לאִקְס ועוד אחת, וכל תא אחר בלתי אפשרי."),
    P("נשארה בדיקת הנרמול. מחברים את ששת התאים שאינם אפס.",
      do=hide(*[f"et-w-{pos(x, y)[0]}-{pos(x, y)[1]}" for x, y in CELLS if CELLS[(x, y)][1] == 0]) + show("x-0")),
    P("אלה בדיוק האיברים בפיתוח של אחת פחות $p$ ועוד $p$, בשלישית.", do=show("x-1"),
      say="אלה בדיוק האיברים בפיתוח של אחת פחות פִּי ועוד פִּי, בשלישית."),
    P("ואחת בשלישית היא אחת. תכונת הנרמול מתקיימת, לכל $p$.", do=show("x-ok"), hold=0.6,
      say="ואחת בשלישית היא אחת. תכונת הנרמול מתקיימת, לכל פִּי."),
], stage=f'<div class="jt-col" style="gap:22px">{EC}{ET}</div>',
   panel=w.stem(Q["id"], "מטבע מוטה מוטל שלוש פעמים, $P(H)=p$. $X$ הוא מספר העצים בשתי ההטלות הראשונות. "
                "$Y$ הוא מספר העצים בכל השלוש. מצאו את $P_{XY}(x,y)$ ובדקו נרמול.")
         + w.eqs("x", ["$(1-p)^3+3p(1-p)^2+3p^2(1-p)+p^3$", "$=\\left[(1-p)+p\\right]^3=1$"], size=30, gap=6)
         + st.card("x-t", "trap", "⚠️ $Y=X+X_3$: רק $y=x$ או $y=x+1$")
         + w.chip("x-ok", "נרמול ✓"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: רושמים את כל התוצאות, ולכל אחת מחשבים את הזוג ואת ההסתברות.", do=show("r-1")),
    P("מקבצים: תא הוא **סכום** ההסתברויות של כל התוצאות שנותנות אותו.", do=show("r-2")),
    P("תא שאף תוצאה לא מגיעה אליו הוא אפס, ותא חסר הוא אחת פחות סכום כל השאר.", do=show("r-3")),
    P("ותמיד בודקים שהסכום הכולל אחת. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$P_{XY}(x,y)=P(X=x,\\ Y=y)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 תוצאות $\\to$ זוג $(x,y)$ והסתברות")
         + st.card("r-2", "rule", "🔑 תא = סכום התוצאות שלו")
         + st.card("r-3", "trap", "⚠️ תא בלתי אפשרי: $0$, לא ריק")
         + st.card("r-4", "rule", "🔑 $\\sum\\sum P_{XY}=1$"))

VIDEO = Video("J01", "joint", "טבלת ההתפלגות המשותפת", [title, idea, urn, miss, exam, recap],
              bank={"24S-B-Q3a": None})
