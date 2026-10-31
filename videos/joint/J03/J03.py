# -*- coding: utf-8 -*-
"""J03 · תוחלת של פונקציה של (X,Y) — video script (build: tools/video/vid.py J03).

Source: courses/joint/C03.js (lesson + goal: E[g(X,Y)] straight from the joint table, in particular E[X], E[X+Y],
E[XY]).
Exam anchor: 24A-D-Q3a (Q = [[0, X], [Y, X+Y]], X~Ber(p), Y~Ber(q) independent, D = det Q: E[D] and var[D]). No
guided quiz uses it; it is not a twin of the boss items 24A-C-Q3a/d (another matrix, [[-1,-X^2],[Y^2,X+Y]]).
Not used on purpose: every C03 quiz item (the fair three-toss table and its E[X], E[XY] = 5/4, E[X+Y], E|X-Y|,
E[max]) and the lesson's 2x2 table 0.1/0.3/0.2/0.4.
Worked example is new: a 2x3 table on x in {1,2}, y in {0,1,2} (E[XY] = 1.7, E[X] = 1.6, E[Y] = 1, E[X+Y] = 2.6,
E[(X-Y)^2] = 1).
Every expectation is exact (w_joint, sympy) and cross-checked by Monte Carlo (the exam with a real 2x2 determinant).
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, q, Space, Joint, eq

# ---------------------------------------------------------------- example table
B = Joint({(1, 0): R(2, 10), (1, 1): R(1, 10), (1, 2): R(1, 10),
           (2, 0): R(1, 10), (2, 1): R(3, 10), (2, 2): R(2, 10)})
assert B.EXY == R(17, 10)
assert [1 * 1 * B(1, 1), 1 * 2 * B(1, 2), 2 * 1 * B(2, 1), 2 * 2 * B(2, 2)] == [R(1, 10), R(2, 10), R(6, 10), R(8, 10)]
assert B.PX(1) == R(4, 10) and B.PX(2) == R(6, 10) and B.EX == R(16, 10)
assert [B.PY(y) for y in B.ys] == [R(3, 10), R(4, 10), R(3, 10)] and B.EY == 1
assert B.E(lambda x, y: x + y) == B.EX + B.EY == R(26, 10)
assert B.EX * B.EY == R(16, 10) and B.EXY != B.EX * B.EY                  # the trap: 1.7 vs 1.6
G = B.E(lambda x, y: (x - y) ** 2)
assert G == 1
assert [(x - y) ** 2 for x, y in [(1, 0), (1, 2), (2, 0), (2, 1)]] == [1, 1, 4, 1]


def genB(rng, n):
    keys = list(B.c)
    idx = rng.choice(len(keys), size=n, p=[float(B.c[k]) for k in keys])
    xs = np.array([k[0] for k in keys])[idx]
    ys = np.array([k[1] for k in keys])[idx]
    return {"X": xs, "Y": ys}


w.mc(genB, [("E[XY]", lambda d: d["X"] * d["Y"], B.EXY), ("E[X+Y]", lambda d: d["X"] + d["Y"], B.EX + B.EY),
            ("E[(X-Y)^2]", lambda d: (d["X"] - d["Y"]) ** 2, G)])

mkB = lambda pf: w.table(pf, B, cells={k: (w.dec(v, 1, fixed=True), v) for k, v in B.c.items()},
                         mx={x: (w.dec(B.PX(x), 1, fixed=True), B.PX(x)) for x in B.xs},
                         my={y: (w.dec(B.PY(y), 1, fixed=True), B.PY(y)) for y in B.ys}, shown=True, size=36,
                         pad="10px 28px", mshown=True)
BT, BT2 = mkB("bt"), mkB("bo")
bi = lambda x, y, pf="bt": f"{pf}-h-%d-%d" % w.pos(B, x, y)
bw = lambda x, y, pf="bt": f"{pf}-w-%d-%d" % w.pos(B, x, y)

# ---------------------------------------------------------------- exam 24A-D-Q3a
Q = BANK["24A-D-Q3a"]
assert Q["contextId"] == "24A-D-c3" and "pq(1-pq)" in Q["solution"].replace(" ", "")
M = lambda X, Y: sp.Matrix([[0, X], [Y, X + Y]])
S = Space.product({"X": [(0, 1 - p), (1, p)], "Y": [(0, 1 - q), (1, q)]})
fD = lambda o: M(o["X"], o["Y"]).det()
assert sp.expand(M(*sp.symbols("X Y")).det()) == -sp.Symbol("X") * sp.Symbol("Y")
STATES = [(0, 0), (0, 1), (1, 0), (1, 1)]
assert [fD({"X": a, "Y": b}) for a, b in STATES] == [0, 0, 0, -1]
ED = S.E(fD)
ED2 = S.E(lambda o: fD(o) ** 2)
VD = sp.factor(ED2 - ED ** 2)
assert eq(ED, -p * q) and eq(ED2, p * q) and eq(VD, p * q * (1 - p * q))
assert not eq(ED2 - ED ** 2, 0) and not eq(ED, p * q)                     # the two pitfalls: Var = 0, E = +pq
PST = {(0, 0): "(1-p)(1-q)", (0, 1): "(1-p)q", (1, 0): "p(1-q)", (1, 1): "pq"}
for (a, b), t in PST.items():
    assert eq(dict(((o["X"], o["Y"]), wt) for wt, o in S.out)[(a, b)],
              {"(1-p)(1-q)": (1 - p) * (1 - q), "(1-p)q": (1 - p) * q, "p(1-q)": p * (1 - q), "pq": p * q}[t])


def genM(rng, n, pv=0.3, qv=0.6):
    X = (rng.random(n) < pv).astype(float)
    Y = (rng.random(n) < qv).astype(float)
    mats = np.zeros((n, 2, 2))
    mats[:, 0, 1], mats[:, 1, 0], mats[:, 1, 1] = X, Y, X + Y
    return {"D": np.round(np.linalg.det(mats))}


nv = {p: R(3, 10), q: R(6, 10)}
w.mc(genM, [("E[D]", lambda d: d["D"], ED.subs(nv)), ("E[D^2]", lambda d: d["D"] ** 2, ED2.subs(nv))])

EC = w.cards("s", [[f"$({a},{b})$", f"${PST[(a, b)]}$", f"$D={fD({'X': a, 'Y': b})}$"] for a, b in STATES],
             size=32, minw=200, maxw=1000)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחשב תוחלת של ביטוי שתלוי בשני משתנים."),
    P("נראה שאין צורך למצוא קודם את ההתפלגות שלו: עוברים על הטבלה, תא אחר תא."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">J03 · משתנים משותפים</div><h1>תוחלת של פונקציה של $(X,Y)$</h1>'
         '<p>לחשב $E[g(X,Y)]$ ישירות מהטבלה המשותפת, ובפרט $E[X]$, $E[X+Y]$ ו-$E[XY]$.</p>', layout="title")

idea = Scene("idea", "תא אחר תא", [
    P("נניח שרוצים את התוחלת של מכפלה, $X$ כפול $Y$.", say="נניח שרוצים את התוחלת של מכפלה, אִקְס כפול וַואי."),
    P("אפשר היה למצוא קודם את ההתפלגות של המכפלה, אבל אין צורך."),
    P("לוקחים כל תא, מציבים בו את הביטוי, וכופלים בהסתברות של התא. ואז מחברים הכול.", do=show("i-f")),
    P("נעבוד על הטבלה הזו. בעמודה של $y$ שווה אפס המכפלה היא אפס, ולכן שני התאים שם לא תורמים.",
      do=show(bw(1, 0), bw(2, 0)),
      say="נעבוד על הטבלה הזו. בעמודה של וַואי שווה אפס המכפלה היא אפס, ולכן התאים שם לא תורמים."),
    P("נשארו ארבעה תאים. אחת כפול אחת כפול אפס נקודה אחת, ואחת כפול שתיים כפול אפס נקודה אחת.",
      do=hide(bw(1, 0), bw(2, 0)) + show(bi(1, 1), bi(1, 2), "i-0")),
    P("שתיים כפול אחת כפול אפס נקודה שלוש, ושתיים כפול שתיים כפול אפס נקודה שתיים.",
      do=show(bi(2, 1), bi(2, 2))),
    P("הסכום: אחת נקודה שבע.", do=show("i-1")),
    P("ואת $E[X]$ לוקחים מהשוליים: אחת כפול אפס נקודה ארבע, ועוד שתיים כפול אפס נקודה שש. אחת נקודה שש.",
      do=hide(bi(1, 1), bi(1, 2), bi(2, 1), bi(2, 2)) + show("bt-hm-0", "bt-hm-1", "i-2"),
      say="ואת התוחלת של אִקְס לוקחים מהשוליים: אחת כפול אפס נקודה ארבע, ועוד שתיים כפול אפס נקודה שש. אחת נקודה שש."),
    P("ו-$E[Y]$ מהשורה התחתונה: אפס נקודה ארבע ועוד פעמיים אפס נקודה שלוש. בדיוק אחת.",
      do=hide("bt-hm-0", "bt-hm-1") + show("bt-hn-0", "bt-hn-1", "bt-hn-2", "i-3"),
      say="והתוחלת של וַואי מהשורה התחתונה: אפס נקודה ארבע ועוד פעמיים אפס נקודה שלוש. בדיוק אחת."),
    P("תוחלת של סכום היא תמיד סכום התוחלות: אחת נקודה שש ועוד אחת, כלומר שתיים נקודה שש.",
      do=hide("bt-hn-0", "bt-hn-1", "bt-hn-2") + show("i-4", "i-c1")),
    P("אבל במכפלה אין כלל כזה: אחת נקודה שש כפול אחת זה אחת נקודה שש, ולא אחת נקודה שבע.", do=show("i-t")),
    P("לכן את התוחלת של מכפלה מחשבים מהטבלה, תא אחר תא.", hold=0.4),
], stage=f'<div class="jt-col" style="gap:24px">{BT}'
         + w.eqs("i", ["$E[XY]=1\\cdot1\\cdot0.1+1\\cdot2\\cdot0.1+2\\cdot1\\cdot0.3+2\\cdot2\\cdot0.2$",
                       "$=0.1+0.2+0.6+0.8=1.7$", "$E[X]=1\\cdot0.4+2\\cdot0.6=1.6$", "$E[Y]=1\\cdot0.4+2\\cdot0.3=1$",
                       "$E[X+Y]=1.6+1=2.6$"], size=31, gap=4) + "</div>",
   panel=st.card("i-f", "rule", "🔑 $E[g(X,Y)]=\\displaystyle\\sum_x\\sum_y g(x,y)\\,P_{XY}(x,y)$")
         + st.card("i-c1", "rule", "🔑 $E[X+Y]=E[X]+E[Y]$, תמיד")
         + st.card("i-t", "trap", "⚠️ $E[XY]=1.7\\ne E[X]\\,E[Y]=1.6$"))

other = Scene("other", "כל פונקציה", [
    P("המתכון עובד לכל ביטוי. למשל, ההפרש בין $X$ ל-$Y$, בריבוע.", do=show("o-0"),
      say="המתכון עובד לכל ביטוי. למשל, ההפרש בין אִקְס לוַואי, בריבוע."),
    P("בתאים שעל האלכסון, אחת אחת ושתיים שתיים, ההפרש אפס.", do=show(bw(1, 1, "bo"), bw(2, 2, "bo"))),
    P("בתא שתיים אפס ההפרש שתיים, ובריבוע ארבע. בשלושת התאים האחרים הריבוע הוא אחת.",
      do=hide(bw(1, 1, "bo"), bw(2, 2, "bo")) + show(*[bi(x, y, "bo") for x, y in [(2, 0), (1, 0), (1, 2), (2, 1)]])),
    P("לכן: אפס נקודה שתיים ועוד אפס נקודה אחת ועוד ארבע כפול אפס נקודה אחת ועוד אפס נקודה שלוש. בדיוק אחת.",
      do=show("o-1", "o-ok")),
    P("שימו לב שלא היינו צריכים לדעת מה ההתפלגות של ההפרש בריבוע. רק את הערך שלו בכל תא.", hold=0.4),
], stage=f'<div class="jt-col" style="gap:24px">{BT2}'
         + w.eqs("o", ["$E[(X-Y)^2]=\\displaystyle\\sum_x\\sum_y (x-y)^2\\,P_{XY}(x,y)$",
                       "$=0.2+0.1+4\\cdot0.1+0.3=1$"], size=33, gap=6)
         + w.chip("o-ok", "$E[(X-Y)^2]=1$") + "</div>",
   layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. נתונה מטריצה: אפס ו-$X$ בשורה העליונה, $Y$ ו-$X$ ועוד $Y$ בתחתונה.",
      say="ועכשיו סעיף ממבחן. נתונה מטריצה: אפס ואִקְס בשורה העליונה, וַואי ואִקְס ועוד וַואי בתחתונה."),
    P("$X$ ברנולי עם $p$, ו-$Y$ ברנולי עם $q$, בלתי תלויים. $D$ היא הדטרמיננטה.",
      say="אִקְס ברנולי עם פִּי, ווַואי ברנולי עם קְיוּ, בלתי תלויים. דִּי היא הדטרמיננטה."),
    P("מבקשים את התוחלת ואת השונות של $D$.", say="מבקשים את התוחלת ואת השונות של דִּי."),
    P("דטרמיננטה: אלכסון ראשי פחות אלכסון משני. אפס כפול משהו, פחות $X$ כפול $Y$.", do=show("x-0"),
      say="דטרמיננטה: אלכסון ראשי פחות אלכסון משני. אפס כפול משהו, פחות אִקְס כפול וַואי."),
    P("כלומר $D$ שווה מינוס $X$ כפול $Y$. זו פונקציה של הזוג, ונחשב אותה בכל אחד מארבעת המצבים.",
      do=show(*[f"s-o-{k}" for k in range(4)]),
      say="כלומר דִּי שווה מינוס אִקְס כפול וַואי. זו פונקציה של הזוג, ונחשב אותה בכל אחד מארבעת המצבים."),
    P("ההסתברות של כל מצב היא מכפלה, כי $X$ ו-$Y$ בלתי תלויים.", do=show(*[f"s-l-{k}-1" for k in range(4)]),
      say="ההסתברות של כל מצב היא מכפלה, כי אִקְס ווַואי בלתי תלויים."),
    P("ובשלושה מצבים $D$ שווה אפס. רק כששניהם אחת, $D$ שווה מינוס אחת.",
      do=show(*[f"s-l-{k}-2" for k in range(4)], "s-oh-3"),
      say="ובשלושה מצבים דִּי שווה אפס. רק כששניהם אחת, דִּי שווה מינוס אחת."),
    P("לכן התוחלת: מינוס אחת כפול $p$ כפול $q$. כלומר מינוס $p$ $q$.", do=show("x-1"),
      say="לכן התוחלת: מינוס אחת כפול פִּי כפול קְיוּ. כלומר מינוס פִּי קְיוּ."),
    P("לשונות צריך גם את התוחלת של $D$ בריבוע. זו שוב תוחלת של פונקציה: מציבים את הריבוע בכל מצב.",
      say="לשונות צריך גם את התוחלת של דִּי בריבוע. זו שוב תוחלת של פונקציה: מציבים את הריבוע בכל מצב."),
    P("מינוס אחת בריבוע זה אחת, ולכן התוחלת של הריבוע היא $p$ $q$, **בלי** מינוס.", do=show("x-2"),
      say="מינוס אחת בריבוע זה אחת, ולכן התוחלת של הריבוע היא פִּי קְיוּ, בלי מינוס."),
    P("השונות: התוחלת של הריבוע פחות ריבוע התוחלת. $p$ $q$ פחות $p$ $q$ בריבוע.", do=show("x-3"),
      say="השונות: התוחלת של הריבוע פחות ריבוע התוחלת. פִּי קְיוּ פחות פִּי קְיוּ בריבוע."),
    P("ובצורה מסודרת: $p$ $q$ כפול, בסוגריים, אחת פחות $p$ $q$.", do=show("x-ok"),
      say="ובצורה מסודרת: פִּי קְיוּ כפול, בסוגריים, אחת פחות פִּי קְיוּ."),
    P("שתי מלכודות: לשכוח את המינוס בתוחלת, ולבלבל בין התוחלת של הריבוע לבין ריבוע התוחלת.", do=show("x-t")),
    P("מי שמבלבל ביניהן מקבל שונות אפס, וזה כמובן לא נכון.", hold=0.6),
], stage=f'<div class="jt-col" style="gap:26px">'
         '<div class="jt-big">$Q=\\begin{pmatrix}0&X\\\\Y&X+Y\\end{pmatrix}$</div>' + EC + "</div>",
   panel=w.stem(Q["id"], "$X\\sim\\mathrm{Ber}(p)$, $Y\\sim\\mathrm{Ber}(q)$ בלתי תלויים, $D=\\det(Q)$. "
                "חשבו את $E[D]$ ואת $\\mathrm{Var}[D]$.")
         + w.eqs("x", ["$D=0\\cdot(X+Y)-XY=-XY$", "$E[D]=(-1)\\cdot pq=-pq$", "$E[D^2]=1\\cdot pq=pq$",
                       "$\\mathrm{Var}[D]=pq-(pq)^2$"], size=31, gap=6)
         + w.chip("x-ok", "$\\mathrm{Var}[D]=pq(1-pq)$")
         + st.card("x-t", "trap", "⚠️ $E[D^2]\\ne(E[D])^2$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: תוחלת של כל ביטוי בשני המשתנים מחשבים תא אחר תא.", do=show("r-1")),
    P("ערך הביטוי בתא, כפול ההסתברות של התא, ומחברים.", do=show("r-2")),
    P("תוחלת של סכום היא תמיד סכום התוחלות. אבל תוחלת של מכפלה מחשבים מהטבלה.", do=show("r-3")),
    P("ולשונות צריך את התוחלת של הריבוע, שהיא עוד תוחלת של פונקציה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$E[g(X,Y)]=\\displaystyle\\sum_x\\sum_y g(x,y)\\,P_{XY}(x,y)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 תא אחר תא")
         + st.card("r-2", "rule", "🔑 $g(x,y)\\cdot P_{XY}(x,y)$, ומחברים")
         + st.card("r-3", "trap", "⚠️ $E[X+Y]=E[X]+E[Y]$ תמיד, $E[XY]$ מהטבלה")
         + st.card("r-4", "rule", "🔑 $\\mathrm{Var}=E[D^2]-(E[D])^2$"))

VIDEO = Video("J03", "joint", "תוחלת של פונקציה של (X,Y)", [title, idea, other, exam, recap],
              bank={"24A-D-Q3a": None})
