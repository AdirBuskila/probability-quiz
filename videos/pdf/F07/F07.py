# -*- coding: utf-8 -*-
"""F07 · הסתברות מותנית מתוך F — video script (build: tools/video/vid.py F07).

Source: courses/pdf/C07.js (lesson + goal: P(A | B) for intervals as a ratio of differences of F, including a
condition with an absolute value).
Exam anchor: 24A-D-Q4d (f = (2 - |x|)/4 on [-2,2], a = 1/4 and b = 2 from part b: P(X > a / |X| < 1) =
(F(1) - F(1/4)) / (F(1) - F(-1)) = (33/128)/(3/4) = 11/32). No guided quiz uses it; parts b, c-1 are quoted as given.
Not used on purpose: every C07 quiz item (F = t^2/2, t/2: P(X>1/2 | X<3/2), P(X<1 | X>1/2), P(X<1/2 | X<1),
P(X<2 | 1/2<X<3/2), the bug with F(1/2) in the denominator; the tent 1+x, 1-x with P(X>1/4 | |X|<1/2)), and the
boss items 24A-C-Q4c and 24B-A-Q4c. The worked examples use F05's own density (1/2 on [-1,0), 1-x on [0,1)):
P(X>0 | X<1/2) = 3/7, P(X<1/4 | |X|<1/2) = 3/4, P(X<-1/2 | X<0) = 1/2.
Every value is computed with sympy (w_pdf.Pdf) and cross-checked numerically.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo

h = R(1, 2)
q = R(1, 4)

# ---------------------------------------------------------------- examples (F05's density)
E = Pdf([(-1, 0, h), (0, 1, 1 - x)])
assert E.F(h) == R(7, 8) and E.F(0) == h and E.F(-h) == q and E.F(q) == R(23, 32)
C1 = (E.F(h) - E.F(0)) / E.F(h)
assert C1 == R(3, 7) and E.prob(0, h) == R(3, 8)
C2 = (E.F(q) - E.F(-h)) / (E.F(h) - E.F(-h))
assert E.prob(-h, q) == R(15, 32) and E.prob(-h, h) == R(5, 8) and C2 == R(3, 4)
C3 = E.F(-h) / E.F(0)
assert C3 == h
assert E.prob(max(-1, 0), h) / E.prob(0, h) == 1               # B = (0,1/2) inside A = (-1,oo): A∩B = B, so 1
BAD = E.prob(0, h) / (E.F(-h))                              # dividing by the wrong probability can exceed 1
assert BAD > 1

# ---------------------------------------------------------------- exam 24A-D-Q4d
Q = BANK["24A-D-Q4d"]
assert "|X|<1" in Q["question"] and "a(b-|x|)" in Q["question"]
A_, B_ = sp.symbols("a b", positive=True)
SB = sp.solve([sp.integrate(A_ * (B_ - sp.Abs(x)), (x, -B_, B_)) - 1,
               2 * sp.integrate(x**2 * A_ * (B_ - x), (x, 0, B_)) - R(2, 3)], [A_, B_], dict=True)
assert SB == [{A_: R(1, 4), B_: 2}]                          # part b (var = 2/3)
X = Pdf([(-2, 0, (2 + x) / 4), (0, 2, (2 - x) / 4)])
assert X.total() == 1 and X.mean() == 0 and X.moment(2) == R(2, 3)
G0, G1 = X.Fpiece(0), X.Fpiece(1)
assert sp.expand(G0 - (t + 2)**2 / 8) == 0 and sp.expand(G1 - (1 - (2 - t)**2 / 8)) == 0
assert X.F(1) == R(7, 8) and X.F(-1) == R(1, 8) and X.F(q) == R(79, 128)
NUM, DEN = X.F(1) - X.F(q), X.F(1) - X.F(-1)
assert NUM == R(33, 128) and DEN == R(3, 4)
assert NUM / DEN == R(11, 32)
assert NUM / X.F(1) == R(33, 112)                              # the trap: dividing by P(X<1)
assert G0.subs(t, q) != X.F(q)                                  # the trap: the left branch at t = 1/4

# ---------------------------------------------------------------- figures
def ef(v):
    return 0.5 if -1 <= v < 0 else (1 - v if 0 <= v < 1 else 0.0)


def plot_e(p, cond, inter, labels):
    G = w.Plot(p, (-1.5, 1.5), (0, 1.15), w=760, h=330, xticks=[(-1, "-1"), (-0.5, "-½"), (0.25, "¼"), (0.5, "½"), (1, "1")],
               yticks=[(0.5, "1/2"), (1, "1")], pad=(60, 60, 40, 46))
    G.area(f"{p}-cond", ef, cond[0], cond[1], kind="ink")
    G.area(f"{p}-int", ef, inter[0], inter[1], kind="a")
    G.seg(f"{p}-f", [(-1.45, 0), (-1, 0), (-1, 0.5), (0, 0.5), (0, 1), (1, 0), (1.45, 0)], kind="b", hidden=False)
    for i, (xv, yv, s) in enumerate(labels):
        G.label(f"{p}-l{i}", xv, yv, s, kind="ok")
    return G.svg()


PA = plot_e("pa", (-1, 0.5), (0, 0.5), [(0.25, 0.25, "3/8")])
PB = plot_e("pb", (-0.5, 0.5), (-0.5, 0.25), [(-0.25, 0.2, "15/32")])

def ex(v):
    return (2 - abs(v)) / 4 if -2 <= v <= 2 else 0.0


PX = w.Plot("px", (-2.5, 2.5), (0, 0.62), w=780, h=380, xticks=[(-2, "-2"), (-1, "-1"), (0.25, "¼"), (1, "1"), (2, "2")],
            yticks=[(0.25, "1/4"), (0.5, "1/2")])
PX.area("px-cond", ex, -1, 1, kind="ink")
PX.area("px-int", ex, 0.25, 1, kind="a")
PX.seg("px-f", [(-2.45, 0), (-2, 0), (0, 0.5), (2, 0), (2.45, 0)], kind="b", hidden=False)
PX.label("px-lf", -1.35, 0.4, "(2 − |x|)/4", kind="b", hidden=False)
PX.label("px-li", 0.62, 0.12, "33/128", kind="ok")
PX.label("px-lc", 0.3, 0.56, "P(|X| < 1) = 3/4", kind="ink", anchor="start")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחשב הסתברות מותנית של קטעים, מתוך ההתפלגות המצטברת."),
    P("כולל תנאי עם ערך מוחלט, שמופיע הרבה במבחנים."),
    P("ובסוף נפתור סעיף ממבחן.", hold=0.4),
], stage='<div class="kicker">F07 · משתנה רציף</div><h1>הסתברות מותנית מתוך F</h1>'
         '<p>לחשב הסתברות מותנית של קטעים, כולל תנאי עם ערך מוחלט, כיחס של הפרשי F.</p>', layout="title")

idea = Scene("idea", "שלושה צעדים", [
    P("ההגדרה כמו תמיד: ההסתברות של החיתוך, חלקי ההסתברות של התנאי.", do=show("i-def")),
    P("נמשיך עם הצפיפות מהרמות הקודמות. השאלה: מה ההסתברות ש-$X$ חיובי, בהינתן ש-$X$ קטן מחצי?",
      say="נמשיך עם הצפיפות מהרמות הקודמות. השאלה: מה ההסתברות שאִקְס חיובי, בהינתן שאִקְס קטן מחצי?"),
    P("צעד ראשון, המכנה: ההסתברות של **התנאי**. $F$ בחצי, כלומר שבע שמיניות.", do=show("pa-cond", "i-0"),
      say="צעד ראשון, המכנה: ההסתברות של התנאי. אֶף בחצי, כלומר שבע שמיניות."),
    P("זה השטח האפור: העולם החדש שלנו. מה שמחוץ לו כבר לא קרה."),
    P("צעד שני, המונה: חותכים את שני הקטעים. חיובי וגם קטן מחצי: בין אפס לחצי.", do=show("pa-int", "i-1")),
    P("$F$ בחצי פחות $F$ באפס: שבע שמיניות פחות חצי, כלומר שלוש שמיניות.", do=show("pa-l0", "i-2"),
      say="אֶף בחצי פחות אֶף באפס: שבע שמיניות פחות חצי, כלומר שלוש שמיניות."),
    P("צעד שלישי, מחלקים: שלוש שמיניות חלקי שבע שמיניות, כלומר שלוש שביעיות.", do=show("i-ok"), hold=0.4),
], stage=f'<div class="pd-col">{PA}<div class="pd-note">אפור: התנאי $X<\\tfrac12$ · ירוק: החיתוך</div></div>',
   panel=st.card("i-def", "rule", "🔑 $P(A\\mid B)=\\dfrac{P(A\\cap B)}{P(B)}$")
         + w.eqs("i", ["$P(X<\\tfrac12)=F(\\tfrac12)=\\tfrac78$", "$A\\cap B=\\{0<X<\\tfrac12\\}$",
                       "$F(\\tfrac12)-F(0)=\\tfrac78-\\tfrac12=\\tfrac38$"], size=34, gap=8)
         + w.chip("i-ok", "$\\dfrac{3/8}{7/8}=\\dfrac37$"))

absv = Scene("abs", "ערך מוחלט", [
    P("עכשיו תנאי עם ערך מוחלט: $X$ קטן מרבע, בהינתן שהערך המוחלט של $X$ קטן מחצי.",
      say="עכשיו תנאי עם ערך מוחלט: אִקְס קטן מרבע, בהינתן שהערך המוחלט של אִקְס קטן מחצי."),
    P("ערך מוחלט קטן מחצי פירושו קטע אחד: בין מינוס חצי לחצי.", do=show("a-0", "pb-cond")),
    P("המכנה: $F$ בחצי פחות $F$ במינוס חצי. שבע שמיניות פחות רבע: חמש שמיניות.", do=show("a-1"),
      say="המכנה: אֶף בחצי פחות אֶף במינוס חצי. שבע שמיניות פחות רבע: חמש שמיניות."),
    P("החיתוך: קטן מרבע, וגם בין מינוס חצי לחצי. כלומר בין מינוס חצי לרבע.", do=show("a-2", "pb-int")),
    P("$F$ ברבע הוא עשרים ושלוש חלקי שלושים ושתיים. פחות רבע: חמש עשרה חלקי שלושים ושתיים.", do=show("a-3", "pb-l0"),
      say="אֶף ברבע הוא עשרים ושלוש חלקי שלושים ושתיים. פחות רבע: חמש עשרה חלקי שלושים ושתיים."),
    P("מחלקים: חמש עשרה חלקי עשרים. כלומר שלושה רבעים.", do=show("a-ok")),
    P("ושני מקרים שחוסכים עבודה: אם האירוע **בתוך** התנאי, החיתוך הוא האירוע עצמו.", do=show("a-r1")),
    P("למשל $X$ קטן ממינוס חצי, בהינתן ש-$X$ שלילי: רבע חלקי חצי, כלומר חצי.",
      say="למשל אִקְס קטן ממינוס חצי, בהינתן שאִקְס שלילי: רבע חלקי חצי, כלומר חצי."),
    P("ואם התנאי בתוך האירוע, התשובה היא פשוט אחת.", do=show("a-r2"), hold=0.4),
], stage=f'<div class="pd-col">{PB}<div class="pd-note">אפור: $|X|<\\tfrac12$ · ירוק: $-\\tfrac12<X<\\tfrac14$</div></div>',
   panel=w.eqs("a", ["$|X|<\\tfrac12\\iff -\\tfrac12<X<\\tfrac12$", "$F(\\tfrac12)-F(-\\tfrac12)=\\tfrac58$",
                     "$A\\cap B=\\{-\\tfrac12<X<\\tfrac14\\}$", "$\\tfrac{23}{32}-\\tfrac14=\\tfrac{15}{32}$"], size=32, gap=6)
         + w.chip("a-ok", "$\\dfrac{15/32}{5/8}=\\dfrac34$")
         + st.card("a-r1", "ex", "$A\\subseteq B$: $\\ P(A\\mid B)=\\dfrac{P(A)}{P(B)}$")
         + st.card("a-r2", "ex", "$B\\subseteq A$: $\\ P(A\\mid B)=1$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("סעיף ממבחן. הצפיפות היא משולש: $a$ כפול $b$ פחות הערך המוחלט של $x$.",
      say="סעיף ממבחן. הצפיפות היא משולש: אֵיי כפול, בסוגריים, בִּי פחות הערך המוחלט של אִקְס."),
    P("מהסעיף הקודם $a$ הוא רבע ו-$b$ שתיים. מבקשים את ההסתברות ש-$X$ גדול מ-$a$, בהינתן שהערך המוחלט קטן מאחת.",
      do=show("x-0"),
      say="מהסעיף הקודם אֵיי הוא רבע ובִּי שתיים. מבקשים את ההסתברות שאִקְס גדול מאֵיי, בהינתן שהערך המוחלט קטן מאחת."),
    P("שימו לב: $a$ כאן הוא מספר, רבע. אז האירוע הוא $X$ גדול מרבע.", do=show("x-1"),
      say="שימו לב: אֵיי כאן הוא מספר, רבע. אז האירוע הוא אִקְס גדול מרבע."),
    P("המכנה: ערך מוחלט קטן מאחת, כלומר בין מינוס אחת לאחת.", do=show("px-cond", "px-lc")),
    P("$F$ באחת היא שבע שמיניות, ובמינוס אחת שמינית. ההפרש שלושה רבעים.", do=show("x-2"),
      say="אֶף באחת היא שבע שמיניות, ובמינוס אחת שמינית. ההפרש שלושה רבעים."),
    P("המונה: גדול מרבע וגם בין מינוס אחת לאחת. כלומר בין רבע לאחת.", do=show("px-int", "x-3")),
    P("רבע נמצא בצד **הימני** של המשולש, ולכן מציבים בענף הימני: $1-\\frac{(2-t)^2}{8}$.",
      do=show("x-4"),
      say="רבע נמצא בצד הימני של המשולש, ולכן מציבים בענף הימני: אחת פחות, בסוגריים, שתיים פחות טִי, בריבוע, חלקי שמונה."),
    P("$F$ ברבע יוצאת שבעים ותשע חלקי מאה עשרים ושמונה. והמונה: שלושים ושלוש חלקי מאה עשרים ושמונה.",
      do=show("x-5", "px-li"),
      say="אֶף ברבע יוצאת שבעים ותשע חלקי מאה עשרים ושמונה. והמונה: שלושים ושלוש חלקי מאה עשרים ושמונה."),
    P("מחלקים בשלושה רבעים, ומקבלים אחת עשרה חלקי שלושים ושתיים.", do=show("x-ok")),
    P("המלכודת: לחלק ב-$F$ באחת, כאילו התנאי הוא רק $X$ קטן מאחת. התנאי כולל גם את הגבול השמאלי.", do=show("x-t"),
      hold=0.6,
      say="המלכודת: לחלק באֶף באחת, כאילו התנאי הוא רק אִקְס קטן מאחת. התנאי כולל גם את הגבול השמאלי."),
], stage=f'<div class="pd-col">{PX.svg()}'
         + st.card("x-t", "trap", "⚠️ לא $P(X<1)$: המכנה הוא $P(-1<X<1)$") + "</div>",
   panel=w.stem(Q["id"], "$f=a(b-|x|)$ על $[-b,b]$, עם $a=\\tfrac14,\\ b=2$. מצאו $P(X>a\\,/\\,|X|<1)$.")
         + w.eqs("x", ["$F=\\tfrac{(t+2)^2}{8}$ על $[-2,0)$, $\\ 1-\\tfrac{(2-t)^2}{8}$ על $[0,2)$",
                       "$P\\left(X>\\tfrac14\\,\\middle|\\,-1<X<1\\right)$",
                       "$F(1)-F(-1)=\\tfrac78-\\tfrac18=\\tfrac34$", "$\\tfrac14<X<1$",
                       "$F(\\tfrac14)=1-\\tfrac{(7/4)^2}{8}=\\tfrac{79}{128}$",
                       "$\\tfrac78-\\tfrac{79}{128}=\\tfrac{33}{128}$"], size=30, gap=4).replace(
             '<div id="x-0" class="pd-eq h">', '<div id="x-0" class="pd-eq h" dir="rtl">')
         + w.chip("x-ok", "$\\dfrac{33/128}{3/4}=\\dfrac{11}{32}$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הסתברות מותנית היא החיתוך, חלקי התנאי.", do=show("r-1")),
    P("המכנה הוא תמיד ההסתברות של **התנאי**. המונה הוא הקטע המשותף.", do=show("r-2")),
    P("ערך מוחלט קטן מ-$b$ הוא קטע אחד, ממינוס $b$ עד $b$.", do=show("r-3"),
      say="ערך מוחלט קטן מבִּי הוא קטע אחד, ממינוס בִּי עד בִּי."),
    P("ואם יצא מספר גדול מאחת, המכנה שגוי. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="pd-col"><div class="pd-big">$P(A\\mid B)=\\dfrac{P(A\\cap B)}{P(B)}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 חיתוך חלקי תנאי")
         + st.card("r-2", "rule", "🔑 המכנה: $P(B)$ של התנאי")
         + st.card("r-3", "ex", "$|X|<b\\iff -b<X<b$")
         + st.card("r-4", "trap", "⚠️ תוצאה מעל $1$ = טעות"))

VIDEO = Video("F07", "pdf", "הסתברות מותנית מתוך F", w.fix_scenes([title, idea, absv, exam, recap]),
              bank={"24A-D-Q4d": None})
