# -*- coding: utf-8 -*-
"""F06 · הסתברות של קטע מתוך F — video script (build: tools/video/vid.py F06).

Source: courses/pdf/C06.js (lesson + goal: probabilities of an interval, a tail and two tails straight from F,
including P(X <= E[X])).
Exam anchor: 26A-B-Q4d (P(0 < X < mu/2) for f = b x^2 on [0,1), c e^{-(x-1)} for x >= 1, with b = 12(2-mu)/5,
c = (4mu-3)/5 and 3/4 <= mu <= 2 from parts a, b: mu/2 lies in [3/8, 1], so the first branch F = 4(2-mu)t^3/5 gives
mu^3(2-mu)/10). No guided quiz uses it; parts a, b are quoted as given.
Not used on purpose: every C06 quiz item (F = t^2/2, t/2: P(1/2<X<3/2), P(X>3/2), P(X<=13/12), two tails 1/2, 3/2;
F = 2t/3, (t+1)/3; 1 - e^{-2t}). The worked example reuses F05's own example (f = 1/2 on [-1,0), 1-x on [0,1)):
P(-1/2<X<1/2) = 5/8, P(X>1/2) = 1/8, two tails 3/8, E[X] = -1/12, P(X <= E[X]) = 11/24.
Every value is computed with sympy (w_pdf.Pdf) and cross-checked numerically.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo

mu = sp.Symbol("mu", real=True)
h = R(1, 2)

# ---------------------------------------------------------------- example (F05's density)
E = Pdf([(-1, 0, h), (0, 1, 1 - x)])
F0, F1 = E.Fpiece(0), E.Fpiece(1)
assert F0.subs(t, -h) == R(1, 4) and F1.subs(t, h) == R(7, 8)
assert E.F(-h) == R(1, 4) and E.F(h) == R(7, 8)
assert E.prob(-h, h) == R(5, 8)
assert 1 - E.F(h) == R(1, 8)
assert E.F(-h) + 1 - E.F(h) == R(3, 8) == 1 - E.prob(-h, h)
WRONG = F0.subs(t, h)                                  # 1/2 put into the first branch
assert WRONG == R(3, 4) and WRONG != E.F(h)
MU = E.mean()
assert MU == -R(1, 12) and -1 <= MU < 0
assert F0.subs(t, MU) == R(11, 24) == E.F(MU)

# ---------------------------------------------------------------- exam 26A-B-Q4d
Q = BANK["26A-B-Q4d"]
assert "\\mu/2" in Q["question"]
b_ = 12 * (2 - mu) / 5
c_ = (4 * mu - 3) / 5
a, b, c = sp.symbols("a b c", real=True)
assert sp.integrate(1, (x, -oo, 0)) == oo                                       # part a: a = 0
SB = sp.solve([sp.integrate(b * x**2, (x, 0, 1)) + sp.integrate(c * sp.exp(-(x - 1)), (x, 1, oo)) - 1,
               sp.integrate(x * b * x**2, (x, 0, 1)) + sp.integrate(x * c * sp.exp(-(x - 1)), (x, 1, oo)) - mu], [b, c])
assert sp.simplify(SB[b] - b_) == 0 and sp.simplify(SB[c] - c_) == 0
assert sp.reduce_inequalities([b_ >= 0, c_ >= 0], mu).as_set() == sp.Interval(R(3, 4), 2)   # part b
G0 = sp.simplify(sp.integrate(b_ * x**2, (x, 0, t)))
assert sp.simplify(G0 - R(4, 5) * (2 - mu) * t**3) == 0
ANS = sp.simplify(G0.subs(t, mu / 2) - G0.subs(t, 0))
assert sp.simplify(ANS - mu**3 * (2 - mu) / 10) == 0
assert (mu / 2).subs(mu, R(3, 4)) == R(3, 8) and (mu / 2).subs(mu, 2) == 1    # mu/2 in [3/8, 1]: first branch
assert sp.simplify(((mu / 2)**3) - mu**3 / 8) == 0
for m in (R(3, 4), sp.Integer(1), R(3, 2), sp.Integer(2)):
    p = Pdf([(0, 1, b_.subs(mu, m) * x**2), (1, oo, c_.subs(mu, m) * sp.exp(-(x - 1)))])
    assert p.total() == 1 and p.mean() == m and p.prob(0, m / 2) == ANS.subs(mu, m)
assert ANS.subs(mu, R(3, 2)) == R(27, 160)

# ---------------------------------------------------------------- figures
def eF(v):
    return 0.0 if v < -1 else ((v + 1) / 2 if v < 0 else (0.5 + v - v * v / 2 if v < 1 else 1.0))


PF = w.Plot("pF", (-1.6, 1.6), (0, 1.12), w=800, h=430, xticks=[(-1, "-1"), (-0.5, "-½"), (0.5, "½"), (1, "1")],
            yticks=[(0.25, "1/4"), (0.875, "7/8"), (1, "1")], xname="t", yname="F(t)")
PF.seg("pF-0", [(-1.55, 0), (-1, 0), (0, 0.5)], kind="b", hidden=False)
PF.curve("pF-1", eF, 0, 1, kind="a", hidden=False)
PF.seg("pF-2", [(1, 1), (1.55, 1)], kind="ink", hidden=False)
PF.vline("pF-va", -0.5, 0, 0.25)
PF.vline("pF-vb", 0.5, 0, 0.875)
PF.dot("pF-da", -0.5, 0.25, "F(−½) = 1/4", dx=-14, dy=-18, anchor="end", kind="b")
PF.dot("pF-db", 0.5, 0.875, "F(½) = 7/8", dx=16, dy=34, kind="a")
PF.seg("pF-gap", [(0.08, 0.25), (0.08, 0.875)], kind="d")
PF.label("pF-lgap", 0.13, 0.55, "5/8", kind="d", anchor="start")
PF.seg("pF-tail", [(1.25, 0.875), (1.25, 1)], kind="c")
PF.label("pF-ltail", 1.3, 0.9, "1/8", kind="c", anchor="start")
PF.seg("pF-tail0", [(-1.3, 0), (-1.3, 0.25)], kind="c")
PF.label("pF-ltail0", -1.25, 0.09, "1/4", kind="c", anchor="start")
PF.vline("pF-vmu", -1 / 12, 0, 11 / 24)
PF.dot("pF-dmu", -1 / 12, 11 / 24, "F(−1/12) = 11/24", dx=-16, dy=-16, anchor="end", kind="ok")
PF.dot("pF-wrong", 0.5, 0.75, "3/4 ✗", dx=16, dy=-8, kind="bad")
PF.seg("pF-wline", [(0, 0.5), (0.5, 0.75)], kind="bad", dash=True)

M = 1.5                                       # a sample mu for the sketch
bm, cm = float(b_.subs(mu, M)), float(c_.subs(mu, M))
import math
PX = w.Plot("px", (-0.4, 3.4), (0, 1.12), w=780, h=380, xticks=[(0.375, "3/8"), (1, "1"), (2, "2"), (3, "3")],
            yticks=[(0.4, "2/5"), (1, "1")], xname="t", yname="F(t)")
PX.seg("px-0", [(-0.35, 0), (0, 0)], kind="ink", hidden=False)
PX.curve("px-1", lambda v: bm / 3 * v**3, 0, 1, kind="a", hidden=False)
PX.curve("px-2", lambda v: 1 - cm * math.exp(-(v - 1)), 1, 3.35, kind="b", hidden=False)
PX.seg("px-range", [(0.375, 0.02), (1, 0.02)], kind="d")
PX.label("px-lr", 0.34, 0.09, "μ/2 ∈", kind="d", anchor="end")
PX.label("px-l1", 1.12, 0.2, "4(2−μ)t³/5", kind="a", anchor="start")
PX.label("px-l2", 2.0, 0.6, "1 − c·e⁻⁽ᵗ⁻¹⁾", kind="b", anchor="start")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחשב הסתברויות ישירות מתוך ההתפלגות המצטברת."),
    P("קטע, זנב, שני זנבות, וגם ההסתברות להיות מתחת לתוחלת."),
    P("ובסוף נפתור סעיף ממבחן עם $\\mu$ כפרמטר.", hold=0.4, say="ובסוף נפתור סעיף ממבחן עם מְיוּ כפרמטר."),
], stage='<div class="kicker">F06 · משתנה רציף</div><h1>הסתברות של קטע מתוך F</h1>'
         '<p>לחשב הסתברות של קטע, של זנב ושל שני זנבות ישירות מההתפלגות המצטברת, כולל ההסתברות להיות מתחת לתוחלת.</p>',
   layout="title")

rules = Scene("rules", "ארבע נוסחאות", [
    P("נמשיך עם הדוגמה מהרמה הקודמת: $F$ היא $t$ ועוד אחת חלקי שתיים, ואחר כך חצי ועוד $t$ פחות $t^2$ חלקי שתיים.",
      do=show("u-F"),
      say="נמשיך עם הדוגמה מהרמה הקודמת: אֶף היא, בסוגריים, טִי ועוד אחת, חלקי שתיים, ואחר כך חצי ועוד טִי פחות טִי בריבוע חלקי שתיים."),
    P("ברגע שיש $F$, לא צריך לאנטגרל שוב. כל הסתברות היא חיסור, או משלים.",
      say="ברגע שיש אֶף, לא צריך לאנטגרל שוב. כל הסתברות היא חיסור, או משלים."),
    P("ההסתברות לקטע: $F$ בקצה הגדול, פחות $F$ בקצה הקטן.", do=show("u-1"),
      say="ההסתברות לקטע: אֶף בקצה הגדול, פחות אֶף בקצה הקטן."),
    P("נחשב את ההסתברות ש-$X$ בין מינוס חצי לחצי. מינוס חצי נמצא בענף הראשון: $F$ שם רבע.", do=show("pF-va", "pF-da"),
      say="נחשב את ההסתברות שאִקְס בין מינוס חצי לחצי. מינוס חצי נמצא בענף הראשון: אֶף שם רבע."),
    P("וחצי נמצא בענף השני: חצי ועוד חצי פחות שמינית. כלומר שבע שמיניות.", do=show("pF-vb", "pF-db")),
    P("ההפרש הוא חמש שמיניות.", do=show("pF-gap", "pF-lgap", "u-ok1")),
    P("זנב ימני: אחת פחות $F$. ההסתברות ש-$X$ גדול מחצי היא אחת פחות שבע שמיניות: שמינית.", do=show("u-2", "pF-tail", "pF-ltail"),
      say="זנב ימני: אחת פחות אֶף. ההסתברות שאִקְס גדול מחצי היא אחת פחות שבע שמיניות: שמינית."),
    P("ושני זנבות: מתחת למינוס חצי, או מעל חצי. רבע ועוד שמינית: שלוש שמיניות.", do=show("u-3", "pF-tail0", "pF-ltail0"),
      say="ושני זנבות: מתחת למינוס חצי, או מעל חצי. רבע ועוד שמינית: שלוש שמיניות."),
    P("בדיקה: שלוש שמיניות ועוד חמש שמיניות, בדיוק אחת. הם משלימים.", hold=0.4),
], stage=f'<div class="pd-col">{PF.svg()}</div>',
   panel=w.chip("u-F", "$F=\\tfrac{t+1}{2}$ על $[-1,0)$, $\\ \\tfrac12+t-\\tfrac{t^2}{2}$ על $[0,1)$", "warn")
         + st.card("u-1", "rule", "🔑 $P(a<X<b)=F(b)-F(a)$")
         + w.chip("u-ok1", "$\\tfrac78-\\tfrac14=\\tfrac58$")
         + st.card("u-2", "rule", "🔑 $P(X>a)=1-F(a)$")
         + st.card("u-3", "rule", "🔑 שני זנבות: $F(a)+1-F(b)$"))

mean = Scene("mean", "מתחת לתוחלת", [
    P("שאלה קלאסית: מה ההסתברות ש-$X$ קטן או שווה לתוחלת שלו?",
      say="שאלה קלאסית: מה ההסתברות שאִקְס קטן או שווה לתוחלת שלו?"),
    P("אין כאן קסם. התוחלת היא מספר: מחשבים אותו, ומציבים ב-$F$.",
      say="אין כאן קסם. התוחלת היא מספר: מחשבים אותו, ומציבים באֶף."),
    P("התוחלת: מהקטע הראשון מינוס רבע, ומהשני שישית. יחד מינוס אחת חלקי שתים עשרה.", do=show("m-0")),
    P("מינוס אחת חלקי שתים עשרה נמצא בענף הראשון. מציבים שם, ומקבלים אחת עשרה חלקי עשרים וארבע.",
      do=show("m-1", "pF2-vmu", "pF2-dmu")),
    P("ושימו לב: זה לא חצי. ההסתברות להיות מתחת לתוחלת תלויה בצורה של הצפיפות.", do=show("m-r")),
    P("והמלכודת של הפרק כולו: להציב בענף הלא נכון.", do=show("m-t")),
    P("מי שמציב חצי בענף הראשון, מקבל שלושה רבעים במקום שבע שמיניות.", do=show("pF2-wrong", "pF2-wline")),
    P("לפני כל הצבה, בודקים באיזה קטע נמצא הערך.", hold=0.4),
], stage=f'<div class="pd-col">{PF.svg().replace("pF", "pF2")}</div>',
   panel=w.eqs("m", ["$E[X]=-\\tfrac14+\\tfrac16=-\\tfrac1{12}$",
                     "$F\\left(-\\tfrac1{12}\\right)=\\tfrac{11/12}{2}=\\tfrac{11}{24}$"], size=36, gap=10)
         + st.card("m-r", "rule", "🔑 $P(X\\le E[X])=F(E[X])$")
         + st.card("m-t", "trap", "⚠️ כל ערך בענף של הקטע שלו"))

exam = Scene("exam", "שאלה ממבחן", [
    P("סעיף ממבחן. מהסעיפים הקודמים: הצפיפות היא $b x^2$ מאפס עד אחת, ומאחת והלאה אקספוננט יורד.",
      say="סעיף ממבחן. מהסעיפים הקודמים: הצפיפות היא בִּי אִקְס בריבוע מאפס עד אחת, ומאחת והלאה אקספוננט יורד."),
    P("$b$ הוא שתים עשרה חמישיות כפול שתיים פחות $\\mu$, ו-$\\mu$ בין שלושה רבעים לשתיים.", do=show("x-0"),
      say="בִּי הוא שתים עשרה חמישיות כפול, בסוגריים, שתיים פחות מְיוּ. ומְיוּ בין שלושה רבעים לשתיים."),
    P("מבקשים את ההסתברות ש-$X$ בין אפס ל-$\\mu$ חלקי שתיים.",
      say="מבקשים את ההסתברות שאִקְס בין אפס למְיוּ חלקי שתיים."),
    P("זה $F$ ב-$\\mu$ חלקי שתיים, פחות $F$ באפס, ו-$F$ באפס היא אפס.", do=show("x-1"),
      say="זה אֶף במְיוּ חלקי שתיים, פחות אֶף באפס. ואֶף באפס היא אפס."),
    P("אבל באיזה ענף? $\\mu$ בין שלושה רבעים לשתיים, ולכן $\\mu$ חלקי שתיים בין שלוש שמיניות לאחת.",
      do=show("x-2", "px-range", "px-lr"),
      say="אבל באיזה ענף? מְיוּ בין שלושה רבעים לשתיים, ולכן מְיוּ חלקי שתיים בין שלוש שמיניות לאחת."),
    P("זה תמיד בענף הראשון. שם $F$ היא $b$ שלישים כפול $t^3$.", do=show("x-3", "px-l1"),
      say="זה תמיד בענף הראשון. שם אֶף היא בִּי שלישים כפול טִי בשלישית."),
    P("מציבים: $\\mu$ חלקי שתיים, בשלישית, זה $\\mu^3$ חלקי **שמונה**.", do=show("x-4"),
      say="מציבים: מְיוּ חלקי שתיים, בשלישית, זה מְיוּ בשלישית חלקי שמונה."),
    P("ארבע חמישיות כפול שתיים פחות $\\mu$, כפול $\\mu^3$ חלקי שמונה.", do=show("x-5"),
      say="ארבע חמישיות כפול, בסוגריים, שתיים פחות מְיוּ, כפול מְיוּ בשלישית חלקי שמונה."),
    P("התשובה: $\\mu^3$ כפול שתיים פחות $\\mu$, חלקי עשר.", do=show("x-ok"),
      say="התשובה: מְיוּ בשלישית כפול, בסוגריים, שתיים פחות מְיוּ, חלקי עשר."),
    P("בדיקה במספר: עבור $\\mu$ שלושה חצאים יוצא עשרים ושבע חלקי מאה שישים. אותו ערך מתקבל מאינטגרל ישיר של הצפיפות.",
      say="בדיקה במספר: עבור מְיוּ שלושה חצאים, יוצא עשרים ושבע חלקי מאה ושישים. אותו ערך מתקבל מאינטגרל ישיר של הצפיפות."),
    P("ובקצוות: כש-$\\mu$ שתיים התשובה אפס, כי אז $b$ אפס, ואין שום צפיפות לפני אחת.",
      say="ובקצוות: כשמְיוּ שתיים התשובה אפס, כי אז בִּי אפס, ואין שום צפיפות לפני אחת."),
    P("שתי מלכודות: להשתמש בענף האקספוננציאלי, או לשכוח שגם השתיים שבמכנה עולה בשלישית.", do=show("x-t", "px-l2"), hold=0.6),
], stage=f'<div class="pd-col">{PX.svg()}'
         + st.card("x-t", "trap", "⚠️ לא הענף של $e^{-(t-1)}$; $\\ (\\tfrac{\\mu}{2})^3=\\tfrac{\\mu^3}{8}$") + "</div>",
   panel=w.stem(Q["id"], "$f=b\\,x^2$ על $[0,1)$, $\\ c\\,e^{-(x-1)}$ ל-$x\\ge1$. חשבו את $P(0<X<\\mu/2)$.")
         + w.eqs("x", ["$b=\\tfrac{12(2-\\mu)}{5},\\ \\ \\tfrac34\\le\\mu\\le2$", "$P=F(\\tfrac\\mu2)-F(0)$",
                       "$\\tfrac38\\le\\tfrac\\mu2\\le1$", "$F(t)=\\tfrac b3t^3=\\tfrac{4(2-\\mu)}{5}t^3$",
                       "$\\left(\\tfrac\\mu2\\right)^3=\\tfrac{\\mu^3}{8}$",
                       "$\\tfrac{4(2-\\mu)}{5}\\cdot\\tfrac{\\mu^3}{8}$"], size=32, gap=4)
         + w.chip("x-ok", "$P(0<X<\\tfrac\\mu2)=\\tfrac{\\mu^3(2-\\mu)}{10}$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הסתברות של קטע היא $F$ בקצה הגדול, פחות $F$ בקצה הקטן.", do=show("r-1"),
      say="לסיכום: הסתברות של קטע היא אֶף בקצה הגדול, פחות אֶף בקצה הקטן."),
    P("זנב ימני הוא אחת פחות $F$, ושני זנבות הם סכום של שניהם.", do=show("r-2"),
      say="זנב ימני הוא אחת פחות אֶף, ושני זנבות הם סכום של שניהם."),
    P("מתחת לתוחלת: מציבים את התוחלת ב-$F$.", do=show("r-3"), say="מתחת לתוחלת: מציבים את התוחלת באֶף."),
    P("ולפני כל הצבה, בודקים באיזה ענף נמצא הערך. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="pd-col"><div class="pd-big">$P(a<X<b)=F(b)-F(a)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $F(b)-F(a)$")
         + st.card("r-2", "rule", "🔑 $1-F(a)$, $\\ F(a)+1-F(b)$")
         + st.card("r-3", "ex", "$P(X\\le E[X])=F(E[X])$")
         + st.card("r-4", "trap", "⚠️ הענף הנכון"))

VIDEO = Video("F06", "pdf", "הסתברות של קטע מתוך F", w.fix_scenes([title, rules, mean, exam, recap]),
              bank={"26A-B-Q4d": None})
