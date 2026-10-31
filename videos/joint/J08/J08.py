# -*- coding: utf-8 -*-
"""J08 · מטריצות ברנולי: דטרמיננטה ועקבה — video script (build: tools/video/vid.py J08).

Source: courses/joint/C08.js (lesson + goal: for a 2x2 matrix built from two Bernoulli bits, the joint pmf of
(D, T) = (det, tr), when D is Bernoulli, dependence and correlation).
Exam anchors: 24B-A-Q3a (Q = [[X, -X^2], [Y^2, X-Y]], X, Y ~ Ber(p) independent: the joint pmf of (D,T)),
24B-A-Q3d (cov[D,T]) and 24B-A-Q3f (uncorrelated?). No guided quiz uses them, and no quiz/boss item uses this matrix
(the boss matrices are [[-1,-X^2],[Y^2,X+Y]] of 24A-C and [[XY,-X],[Y,X+Y-XY]] of 25S-C).
Not used on purpose: every C08 quiz item (diag(X, Y) with P(D=1), p^2 = 0.36 and P(D=0,T=1); [[X,Y],[1,Y]] with
Cov = -3/32; [[Y,X],[1,0]]; [[X,Y],[Y,X]] with rho = 1/sqrt 2) and the lesson's [[X,1],[1,Y]].
Worked example is new: A = [[1, X], [Y, X]], X~Ber(p), Y~Ber(q): D = X(1-Y), T = 1+X; two states share the cell
(0,1), D ~ Ber(p(1-q)), and the zero cell (1,1) proves dependence.
Every determinant is a real sympy det of the matrix in each state; tables are grouped enumerations (w_joint), and
Monte Carlo runs numpy determinants of random matrices.
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_joint as w
from w_joint import R, p, q, Space, Joint, eq

Xs, Ys = sp.symbols("X Y")
STATES = [(0, 0), (0, 1), (1, 0), (1, 1)]

# ---------------------------------------------------------------- example: A = [[1, X], [Y, X]]
MA = lambda X, Y: sp.Matrix([[1, X], [Y, X]])
assert sp.expand(MA(Xs, Ys).det()) == Xs - Xs * Ys and MA(Xs, Ys).trace() == 1 + Xs
SA = Space.product({"X": [(0, 1 - p), (1, p)], "Y": [(0, 1 - q), (1, q)]})
fDA = lambda o: MA(o["X"], o["Y"]).det()
fTA = lambda o: MA(o["X"], o["Y"]).trace()
VA = [(fDA({"X": a, "Y": b}), fTA({"X": a, "Y": b})) for a, b in STATES]
assert VA == [(0, 1), (0, 1), (1, 2), (0, 2)]
JA = SA.joint(fDA, fTA)
JA = Joint({(d, t): JA(d, t) for d in (0, 1) for t in (1, 2)}, xs=[0, 1], ys=[1, 2])
assert eq(JA(0, 1), 1 - p) and eq(JA(0, 2), p * q) and JA(1, 1) == 0 and eq(JA(1, 2), p * (1 - q))
assert eq(JA.PX(1), p * (1 - q))                                      # D ~ Ber(p(1-q))
assert not JA.independent() and eq(JA.PX(1) * JA.PY(1), p * (1 - q) * (1 - p))
PSA = {(0, 0): "(1-p)(1-q)", (0, 1): "(1-p)q", (1, 0): "p(1-q)", (1, 1): "pq"}
CA = {(0, 1): ("1-p", 1 - p), (0, 2): ("pq", p * q), (1, 1): ("0", 0), (1, 2): ("p(1-q)", p * (1 - q))}
MXA = {0: ("1-p(1-q)", 1 - p * (1 - q)), 1: ("p(1-q)", p * (1 - q))}
MYA = {1: ("1-p", 1 - p), 2: ("p", p)}
TA = w.table("ta", JA, cells=CA, mx=MXA, my=MYA, xname="d", yname="t", mxh="P_D(d)", myh="P_T(t)", size=32,
             pad="8px 20px", mshown=False)
CARDA = w.cards("a", [[f"$({a},{b})$", f"${PSA[(a, b)]}$", f"$D={d},\\ T={t}$"] for (a, b), (d, t) in zip(STATES, VA)],
                size=28, minw=190, maxw=1000)

# ---------------------------------------------------------------- exam 24B-A
QA, QD, QF = BANK["24B-A-Q3a"], BANK["24B-A-Q3d"], BANK["24B-A-Q3f"]
assert QA["contextId"] == QD["contextId"] == QF["contextId"] == "24B-A-c3"
assert "2p(1-p)" in QD["solution"].replace(" ", "") and "מתואמים" in QF["solution"]
MQ = lambda X, Y: sp.Matrix([[X, -X ** 2], [Y ** 2, X - Y]])
detQ = sp.expand(MQ(Xs, Ys).det())
assert detQ == Xs ** 2 - Xs * Ys + Xs ** 2 * Ys ** 2
bits = lambda e: sp.expand(e).replace(lambda z: z.is_Pow and z.base in (Xs, Ys), lambda z: z.base)
assert bits(detQ) == Xs and sp.expand(MQ(Xs, Ys).trace()) == 2 * Xs - Ys      # with X^2 = X, Y^2 = Y
S = Space.product({"X": [(0, 1 - p), (1, p)], "Y": [(0, 1 - p), (1, p)]})
fD = lambda o: MQ(o["X"], o["Y"]).det()
fT = lambda o: MQ(o["X"], o["Y"]).trace()
V = [(fD({"X": a, "Y": b}), fT({"X": a, "Y": b})) for a, b in STATES]
assert V == [(0, 0), (0, -1), (1, 2), (1, 1)]
J = S.joint(fD, fT)
J = Joint({(d, t): J(d, t) for d in (0, 1) for t in (-1, 0, 1, 2)}, xs=[0, 1], ys=[-1, 0, 1, 2])
CQ = {(0, -1): ("p(1-p)", p * (1 - p)), (0, 0): ("(1-p)^2", (1 - p) ** 2), (0, 1): ("0", 0), (0, 2): ("0", 0),
      (1, -1): ("0", 0), (1, 0): ("0", 0), (1, 1): ("p^2", p ** 2), (1, 2): ("p(1-p)", p * (1 - p))}
MXQ = {0: ("1-p", 1 - p), 1: ("p", p)}
for t in ["p(1-p)", "(1-p)^2", "p^2"]:
    assert t in QA["solution"].replace(" ", "")
assert eq(J.PX(1), p) and eq(J.EX, p) and eq(J.EY, p)
EDT = J.EXY
assert eq(EDT, 2 * p - p ** 2) and eq(EDT, 1 * 1 * p ** 2 + 1 * 2 * p * (1 - p))
COV = sp.factor(J.cov)
assert eq(COV, 2 * p * (1 - p))
assert not eq(2 * p - p ** 2 - p * p, 2 * p ** 2 - p ** 2 - p ** 2)                # pitfall E[X^2] = p^2 gives 0
for pv in (R(1, 10), R(1, 2), R(9, 10)):
    assert COV.subs(p, pv) > 0
assert COV.subs(p, 0) == 0 and COV.subs(p, 1) == 0                                 # degenerate ends
assert not J.independent()


def genQ(rng, n, pv=0.35):
    X = (rng.random(n) < pv).astype(float)
    Y = (rng.random(n) < pv).astype(float)
    m = np.zeros((n, 2, 2))
    m[:, 0, 0], m[:, 0, 1], m[:, 1, 0], m[:, 1, 1] = X, -X ** 2, Y ** 2, X - Y
    return {"D": np.round(np.linalg.det(m)), "T": np.trace(m, axis1=1, axis2=2)}


nv = {p: R(35, 100)}
JNv = J.subs(nv)
w.mc(genQ, [(f"P({d},{t})", (lambda dd, d=d, t=t: (dd["D"] == d) & (dd["T"] == t)), JNv(d, t))
            for d in J.xs for t in J.ys]
     + [("Cov", lambda dd: (dd["D"] - 0.35) * (dd["T"] - 0.35), COV.subs(nv))])


def genA(rng, n, pv=0.3, qv=0.6):
    X = (rng.random(n) < pv).astype(float)
    Y = (rng.random(n) < qv).astype(float)
    m = np.zeros((n, 2, 2))
    m[:, 0, 0], m[:, 0, 1], m[:, 1, 0], m[:, 1, 1] = 1, X, Y, X
    return {"D": np.round(np.linalg.det(m)), "T": np.trace(m, axis1=1, axis2=2)}


JAv = JA.subs({p: R(3, 10), q: R(6, 10)})
w.mc(genA, [(f"P({d},{t})", (lambda dd, d=d, t=t: (dd["D"] == d) & (dd["T"] == t)), JAv(d, t))
            for d in JA.xs for t in JA.ys])

TQ = w.table("tq", J, cells=CQ, mx=MXQ, xname="d", yname="t", mxh="P_D(d)", size=30, pad="8px 16px")
CARDQ = w.cards("c", [[f"$({a},{b})$", f"${PSA[(a, b)].replace('q', 'p')}$", f"$D={d},\\ T={t}$"]
                      for (a, b), (d, t) in zip(STATES, V)], size=26, minw=170, maxw=1000)
assert [PSA[s].replace("q", "p") for s in STATES] == ["(1-p)(1-p)", "(1-p)p", "p(1-p)", "pp"]
CARDQ = CARDQ.replace("$(1-p)(1-p)$", "$(1-p)^2$").replace("$(1-p)p$", "$p(1-p)$").replace("$pp$", "$p^2$")
tq = lambda d, t, k="v": f"tq-{k}-%d-%d" % w.pos(J, d, t)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נפתור את משפחת השאלות של מטריצות ברנולי."),
    P("מטריצה שהאיברים שלה בנויים משני ביטים, ומהדטרמיננטה והעקבה שלה בונים טבלה משותפת."),
    P("ובסוף נפתור שאלה אמיתית ממבחן, שלושה סעיפים.", hold=0.4),
], stage='<div class="kicker">J08 · משתנים משותפים</div><h1>מטריצות ברנולי: דטרמיננטה ועקבה</h1>'
         '<p>מטריצה שאיבריה מבוססים על שני ביטים: ההתפלגות המשותפת של $(D,T)$, מתי $D$ ברנולי, תלות ומתאם.</p>',
   layout="title")

recipe = Scene("recipe", "המתכון", [
    P("שני ביטים בלתי תלויים: $X$ ברנולי עם $p$, ו-$Y$ ברנולי עם $q$.", do=show("m-0"),
      say="שני ביטים בלתי תלויים: אִקְס ברנולי עם פִּי, ווַואי ברנולי עם קְיוּ."),
    P("$D$ היא הדטרמיננטה: אלכסון ראשי כפול, פחות אלכסון משני כפול. $T$ היא העקבה: סכום האלכסון הראשי.",
      do=show("m-1"),
      say="דִּי היא הדטרמיננטה: אלכסון ראשי כפול, פחות אלכסון משני כפול. טִי היא העקבה: סכום האלכסון הראשי."),
    P("וכלל הזהב לביטים: $X$ בריבוע שווה $X$, כי אפס בריבוע הוא אפס ואחת בריבוע היא אחת.", do=show("m-2"),
      say="וכלל הזהב לביטים: אִקְס בריבוע שווה אִקְס, כי אפס בריבוע הוא אפס ואחת בריבוע היא אחת."),
    P("המתכון: מפשטים את $D$ ואת $T$. רושמים את ארבעת המצבים של הזוג. ומקבצים לתאים.", do=show("m-3"),
      say="המתכון: מפשטים את דִּי ואת טִי. רושמים את ארבעת המצבים של הזוג. ומקבצים לתאים.", hold=0.4),
], stage=w.eqs("m", ["$X\\sim\\mathrm{Ber}(p),\\ \\ Y\\sim\\mathrm{Ber}(q)$",
                     "$\\det\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}=ad-bc,\\ \\ \\mathrm{tr}=a+d$",
                     "$X^2=X,\\ \\ Y^2=Y$"], size=42, gap=30),
   panel=st.card("m-3", "rule", "🔑 מפשטים $\\to$ ארבעה מצבים $\\to$ מקבצים לתאים"))

ex = Scene("ex", "דוגמה", [
    P("דוגמה. אחת ו-$X$ בשורה העליונה, $Y$ ו-$X$ בתחתונה.", do=show("e-0"),
      say="דוגמה. אחת ואִקְס בשורה העליונה, וַואי ואִקְס בתחתונה."),
    P("$D$: אחת כפול $X$, פחות $X$ כפול $Y$. ו-$T$: אחת ועוד $X$.", do=show("e-1"),
      say="דִּי: אחת כפול אִקְס, פחות אִקְס כפול וַואי. וטִי: אחת ועוד אִקְס."),
    P("ארבעת המצבים, ההסתברויות שלהם, וערכי $D$ ו-$T$ בכל אחד.",
      do=show(*[f"a-o-{k}" for k in range(4)], *[f"a-l-{k}-{r}" for k in range(4) for r in (1, 2)]),
      say="ארבעת המצבים, ההסתברויות שלהם, וערכי דִּי וטִי בכל אחד."),
    P("שני המצבים הראשונים נותנים את אותו זוג: אפס ואחת. לכן מחברים: אחת פחות $p$, כפול סכום שהוא אחת.",
      do=show("a-oh-0", "a-oh-1", "ta", "ta-h-0-0", "ta-v-0-0"),
      say="שני המצבים הראשונים נותנים את אותו זוג: אפס ואחת. לכן מחברים: אחת פחות פִּי, כפול סכום שהוא אחת."),
    P("שני המצבים האחרים נכנסים כל אחד לתא משלו.",
      do=hide("a-oh-0", "a-oh-1", "ta-h-0-0") + show("ta-v-1-1", "ta-v-0-1")),
    P("אף מצב לא מגיע לתא אחת אחת, ולכן הוא אפס.", do=show("ta-v-1-0", "ta-w-1-0"),
      ),
    P("סכום השורה של אחת נותן ש-$D$ הוא ברנולי, עם פרמטר $p$ כפול אחת פחות $q$.",
      do=hide("ta-w-1-0") + show("ta-mxh", "ta-mx-0", "ta-mx-1", "e-c1"),
      say="סכום השורה של אחת נותן שדִּי הוא ברנולי, עם פרמטר פִּי כפול אחת פחות קְיוּ."),
    P("ותלות? התא אחת אחת הוא אפס, אבל השוליים שלו חיוביים. לכן $D$ ו-$T$ תלויים.",
      do=show("ta-myh", "ta-my-0", "ta-my-1", "ta-w-1-0", "e-c2"),
      say="ותלות? התא אחת אחת הוא אפס, אבל השוליים שלו חיוביים. לכן דִּי וטִי תלויים.", hold=0.4),
], stage=f'<div class="jt-col" style="gap:20px">{CARDA}{TA}</div>',
   panel='<div id="e-0" class="jt-big h">$A=\\begin{pmatrix}1&X\\\\Y&X\\end{pmatrix}$</div>'
         + '<div id="e-1" class="jt-mid h">$D=X-XY,\\ \\ T=1+X$</div>'
         + st.card("e-c1", "rule", "🔑 $D\\sim\\mathrm{Ber}\\big(p(1-q)\\big)$")
         + st.card("e-c2", "trap", "⚠️ אפס בתא ששוליו חיוביים: תלויים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. המטריצה: $X$ ומינוס $X$ בריבוע למעלה. $Y$ בריבוע ו-$X$ פחות $Y$ למטה.",
      say="ועכשיו שאלה ממבחן. המטריצה: אִקְס ומינוס אִקְס בריבוע למעלה. וַואי בריבוע ואִקְס פחות וַואי למטה."),
    P("הפעם $X$ ו-$Y$ שניהם ברנולי עם אותו $p$. סעיף ראשון: הטבלה המשותפת של $D$ ו-$T$.",
      say="הפעם אִקְס ווַואי שניהם ברנולי עם אותו פִּי. סעיף ראשון: הטבלה המשותפת של דִּי וטִי."),
    P("הדטרמיננטה: $X$ כפול, בסוגריים, $X$ פחות $Y$, פחות מינוס $X$ בריבוע כפול $Y$ בריבוע.", do=show("x-0"),
      say="הדטרמיננטה: אִקְס כפול, בסוגריים, אִקְס פחות וַואי, פחות מינוס אִקְס בריבוע כפול וַואי בריבוע."),
    P("עכשיו כלל הזהב: כל ריבוע של ביט הוא הביט עצמו. נשאר $X$ פחות $X$ $Y$ ועוד $X$ $Y$. כלומר רק $X$.",
      do=show("x-1"),
      say="עכשיו כלל הזהב: כל ריבוע של ביט הוא הביט עצמו. נשאר אִקְס פחות אִקְס וַואי ועוד אִקְס וַואי. כלומר רק אִקְס."),
    P("והעקבה: $X$ ועוד $X$ פחות $Y$, כלומר פעמיים $X$ פחות $Y$.", do=show("x-2"),
      say="והעקבה: אִקְס ועוד אִקְס פחות וַואי, כלומר פעמיים אִקְס פחות וַואי."),
    P("ארבעת המצבים. כאן כל מצב נותן זוג אחר, ולכן כל אחד ממלא תא משלו.",
      do=show(*[f"c-o-{k}" for k in range(4)], *[f"c-l-{k}-{r}" for k in range(4) for r in (1, 2)])),
    P("למשל, $X$ אפס ו-$Y$ אחת: $D$ אפס ו-$T$ מינוס אחת, בהסתברות $p$ כפול אחת פחות $p$.",
      do=show("c-oh-1", tq(0, -1, "h"), tq(0, -1)),
      say="למשל, אִקְס אפס ווַואי אחת: דִּי אפס וטִי מינוס אחת, בהסתברות פִּי כפול אחת פחות פִּי."),
    P("וכך שאר המצבים. ארבעה תאים מקבלים הסתברות, וארבעה נשארים אפס.",
      do=hide("c-oh-1", tq(0, -1, "h")) + show(*[tq(d, t) for d in J.xs for t in J.ys], "tq-mxh", "tq-mx-0",
                                                  "tq-mx-1")),
    P("סעיף שני: השונות המשותפת. התוחלת של המכפלה: אחת כפול אחת כפול $p$ בריבוע, ועוד אחת כפול שתיים כפול $p$ כפול אחת פחות $p$.",
      do=show(tq(1, 1, "h"), tq(1, 2, "h"), "x-3"),
      say="סעיף שני: השונות המשותפת. התוחלת של המכפלה: אחת כפול אחת כפול פִּי בריבוע, ועוד אחת כפול שתיים כפול פִּי כפול אחת פחות פִּי."),
    P("יוצא פעמיים $p$ פחות $p$ בריבוע. והתוחלות: $E[D]$ הוא $p$, ו-$E[T]$ הוא פעמיים $p$ פחות $p$, כלומר $p$.",
      do=hide(tq(1, 1, "h"), tq(1, 2, "h")) + show("x-4"),
      say="יוצא פעמיים פִּי פחות פִּי בריבוע. והתוחלות: של דִּי היא פִּי, ושל טִי היא פעמיים פִּי פחות פִּי, כלומר פִּי."),
    P("השונות המשותפת: פעמיים $p$ פחות $p$ בריבוע, פחות $p$ בריבוע. כלומר פעמיים $p$ כפול אחת פחות $p$.",
      do=show("x-5", "x-ok"),
      say="השונות המשותפת: פעמיים פִּי פחות פִּי בריבוע, פחות פִּי בריבוע. כלומר פעמיים פִּי כפול אחת פחות פִּי."),
    P("סעיף שלישי: האם הם בלתי מתואמים? לא. לכל $p$ בין אפס לאחת השונות המשותפת חיובית, ולכן הם מתואמים.",
      do=show("x-no"),
      say="סעיף שלישי: האם הם בלתי מתואמים? לא. לכל פִּי בין אפס לאחת השונות המשותפת חיובית, ולכן הם מתואמים."),
    P("שתי מלכודות: להשאיר את הריבועים בלי לפשט, ולהסיק אפס מתאם רק כי $X$ ו-$Y$ בלתי תלויים.", do=show("x-t"),
      say="שתי מלכודות: להשאיר את הריבועים בלי לפשט, ולהסיק אפס מתאם רק כי אִקְס ווַואי בלתי תלויים."),
    P("$D$ ו-$T$ בנויים מאותו $X$, ולכן הם בהחלט יכולים להיות מתואמים.", hold=0.6,
      say="דִּי וטִי בנויים מאותו אִקְס, ולכן הם בהחלט יכולים להיות מתואמים."),
], stage=f'<div class="jt-col" style="gap:20px">{CARDQ}{TQ}</div>',
   panel=w.stem("24B-A-Q3a/d/f", "$Q=\\begin{pmatrix}X&-X^2\\\\Y^2&X-Y\\end{pmatrix}$, $X,Y\\sim\\mathrm{Ber}(p)$. "
                "הטבלה של $(D,T)$, $\\mathrm{Cov}[D,T]$, ומתואמים?")
         + w.eqs("x", ["$D=X(X-Y)+X^2Y^2$", "$=X-XY+XY=X$", "$T=X+(X-Y)=2X-Y$", "$E[DT]=p^2+2p(1-p)=2p-p^2$",
                       "$E[D]=p,\\ \\ E[T]=2p-p=p$", "$\\mathrm{Cov}=2p-p^2-p^2$"], size=27, gap=0)
         + '<div class="jt-row" style="gap:14px">' + w.chip("x-ok", "$2p(1-p)$") + w.chip("x-no", "מתואמים", "bad")
         + "</div>"
         + st.card("x-t", "trap", "⚠️ לפשט $X^2=X$. ואי-תלות של $X,Y$ לא אומרת ש-$\\mathrm{Cov}(D,T)=0$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מחשבים את הדטרמיננטה ואת העקבה, ומפשטים עם $X$ בריבוע שווה $X$.", do=show("r-1"),
      say="לסיכום: מחשבים את הדטרמיננטה ואת העקבה, ומפשטים עם אִקְס בריבוע שווה אִקְס."),
    P("רושמים ארבעה מצבים, ומקבצים מצבים שנותנים אותו זוג.", do=show("r-2")),
    P("מהטבלה: שוליים, תוחלות ושונות משותפת, כמו בכל טבלה.", do=show("r-3")),
    P("ותלות או מתאם מוכיחים בחישוב, לא בתחושה. נתראה באתגר המבחן.", do=show("r-4"), hold=0.6),
], stage='<div class="jt-col"><div class="jt-big">$D=\\det,\\ \\ T=\\mathrm{tr},\\ \\ X^2=X$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $X^2=X$ לביט")
         + st.card("r-2", "rule", "🔑 ארבעה מצבים $\\to$ קיבוץ")
         + st.card("r-3", "rule", "🔑 $\\mathrm{Cov}=E[DT]-E[D]E[T]$")
         + st.card("r-4", "trap", "⚠️ תלות: תא אפס. מתאם: $\\mathrm{Cov}\\ne0$"))

VIDEO = Video("J08", "joint", "מטריצות ברנולי: דטרמיננטה ועקבה", [title, recipe, ex, exam, recap],
              bank={"24B-A-Q3a": None, "24B-A-Q3d": None, "24B-A-Q3f": None})
