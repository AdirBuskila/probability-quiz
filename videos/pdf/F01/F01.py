# -*- coding: utf-8 -*-
"""F01 · מהי פונקציית צפיפות — video script (build: tools/video/vid.py F01).

Source: courses/pdf/C01.js (lesson + goal: decide whether a function is a valid density; probability = area).
Exam anchor: 26A-B-Q1b (from F_D(t) = t - t ln t to the density -ln t on (0,1), unbounded and still valid). No guided
quiz uses it (vid.py refuses quiz ids); the F_D of part a (26A-B-Q1a) is quoted as given.
Not used on purpose: every C01 quiz item (2x and x and 1-2x on [0,1], 2x on [0,2], the constant 2 on [0,1/2], 3x^2,
P(X=3/4)); the worked examples use new functions: (3/8)x^2 on [0,2], and the candidates x-1/2 on [0,2], 4 on [0,1/4],
x/4 on [0,2].
Every area, probability and verdict below is computed with sympy (exact) and cross-checked by mpmath quadrature
(w_pdf.Pdf asserts both).
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf

# ---------------------------------------------------------------- example: f = 3/8 x^2 on [0, 2]
E = Pdf([(0, 2, R(3, 8) * x**2)])
assert E.nonneg() and E.total() == 1
assert E.prob(1, 2) == R(7, 8)
assert E.F(1) == R(1, 8)

# candidates
G1 = Pdf([(0, 2, x - R(1, 2))])
assert G1.total() == 1 and not G1.nonneg()            # area 1, but negative on [0, 1/2)
assert sp.solve(x - R(1, 2), x) == [R(1, 2)]
G2 = Pdf([(0, R(1, 4), 4)])
assert G2.total() == 1 and G2.nonneg()                 # valid, height 4 > 1
G3 = Pdf([(0, 2, x / 4)])
assert G3.total() == R(1, 2) and G3.nonneg()           # area 1/2: not a density

# exam 26A-B-Q1b
Q = BANK["26A-B-Q1b"]
assert "f_D(t)" in Q["question"]
FD = t - t * sp.log(t)
fD = sp.simplify(sp.diff(FD, t))
assert fD == -sp.log(t)
assert sp.diff(t * sp.log(t), t) == sp.log(t) + 1
assert sp.limit(FD, t, 0, "+") == 0 and FD.subs(t, 1) == 1
D = Pdf([(0, 1, -sp.log(x))])
assert D.total() == 1 and D.nonneg()
assert sp.limit(-sp.log(t), t, 0, "+") == sp.oo
assert sp.solve(sp.Eq(-sp.log(t), 1), t) == [sp.exp(-1)]
assert D.F(sp.exp(-1)) == 2 / sp.E                     # the part where f > 1 holds 2/e of the mass (< 1)
assert abs(float(2 / sp.E) - 0.7358) < 1e-4

# ---------------------------------------------------------------- figures
fE = lambda v: 3 / 8 * v * v


def plot_a(pfx):
    A = w.Plot(pfx, (-0.15, 2.3), (0, 1.65), w=820, h=430, xticks=[(1, "1"), (2, "2")],
               yticks=[(0.5, "0.5"), (1, "1"), (1.5, "1.5")])
    A.curve(f"{pfx}-f", fE, 0, 2, hidden=False)
    A.seg(f"{pfx}-out", [(-0.15, 0), (0, 0)], kind="a", hidden=False)
    A.seg(f"{pfx}-out2", [(2, 0), (2.25, 0)], kind="a", hidden=False)
    A.vline(f"{pfx}-g2", 2, 0, 1.5, hidden=False)
    A.area(f"{pfx}-12", fE, 1, 2, kind="a")
    A.area(f"{pfx}-all", fE, 0, 2, kind="b")
    A.label(f"{pfx}-l", 1.15, 1.25, "f(x) = 3x²/8", kind="a", hidden=False)
    A.dot(f"{pfx}-p1", 1, 0.375, "(1, 3/8)", dx=-16, dy=-18, anchor="end")
    return A.svg()


def small(pfx, pts, fill_pts, yr, yt, lab, bad=None):
    p = w.Plot(pfx, (-0.15, 2.25), yr, w=320, h=300, xticks=[(1, "1"), (2, "2")], yticks=yt, yname="", pad=(46, 40, 30, 46))
    p.seg(f"{pfx}-f", pts, kind="a", hidden=False)
    p.layers["fill"].append(f'<path class="pd-fill k-a" d="{p._d(fill_pts, True)}"/>')
    if bad:
        p.seg(f"{pfx}-bad", bad, kind="bad")
    return p.svg()


S1 = small("c1", [(0, -0.5), (2, 1.5)], [(0.5, 0), (2, 1.5), (2, 0)] + [(0.5, 0)], (-0.6, 1.6),
           [(-0.5, "-0.5"), (1, "1")], "", bad=[(0, -0.5), (0.5, 0)])
S2 = small("c2", [(0, 4), (0.25, 4)], [(0, 0), (0, 4), (0.25, 4), (0.25, 0)], (0, 4.4), [(2, "2"), (4, "4")], "")
S3 = small("c3", [(0, 0), (2, 0.5)], [(0, 0), (2, 0.5), (2, 0)], (0, 1.1), [(0.5, "0.5"), (1, "1")], "")

DP = w.Plot("pd", (-0.08, 1.25), (0, 3.4), w=760, h=400, xticks=[(1, "1"), (float(sp.exp(-1)), "1/e")],
            yticks=[(1, "1"), (2, "2"), (3, "3")], xname="t", yname="f(t)")
fd = lambda v: -__import__("math").log(v) if v > 0 else 99
DP.area("pd-a", fd, 0.0005, 1, kind="a", clip=3.4, n=400)
DP.area("pd-big", fd, 0.0005, float(sp.exp(-1)), kind="b", clip=3.4, n=300)
DP.curve("pd-f", fd, 0.012, 1, kind="a", n=400, clip=3.4)
DP.hline("pd-one", 1, 0, 1.2)
DP.label("pd-l", 0.55, 1.6, "f(t) = −ln t", kind="a")
DP.label("pd-inf", 0.1, 3.15, "↑ ∞", kind="b", anchor="start")
DP.dot("pd-p1", 1, 0, "(1, 0)", dx=0, dy=-20, anchor="middle")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבין מהי פונקציית צפיפות של משתנה מקרי רציף."),
    P("נלמד לבדוק אם פונקציה היא צפיפות תקינה, ולחשב הסתברות כשטח."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">F01 · משתנה רציף</div><h1>מהי פונקציית צפיפות</h1>'
         '<p>להכריע אם פונקציה היא צפיפות תקינה, ולחשב הסתברות כשטח מתחת לצפיפות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("משתנה רציף, כמו זמן המתנה, יכול לקבל כל ערך בקטע.", do=show("i-c1")),
    P("לכל ערך בודד ההסתברות היא אפס. לכן מתארים אותו בפונקציה אחרת: **צפיפות**."),
    P("הנה צפיפות לדוגמה: שלוש שמיניות כפול $x^2$, בקטע מאפס עד שתיים.",
      say="הנה צפיפות לדוגמה: שלוש שמיניות כפול אִקְס בריבוע, בקטע מאפס עד שתיים."),
    P("מחוץ לקטע הצפיפות שווה אפס."),
    P("והכלל המרכזי: **הסתברות היא שטח** מתחת לצפיפות.", do=show("i-f")),
    P("למשל, ההסתברות ש-$X$ בין אחת לשתיים היא השטח המוצלל.", do=show("pa-12"),
      say="למשל, ההסתברות שאִקְס בין אחת לשתיים היא השטח המוצלל."),
    P("מחשבים: הפונקציה הקדומה היא $x^3$ חלקי שמונה.", do=show("i-0"),
      say="מחשבים: הפונקציה הקדומה היא אִקְס בשלישית חלקי שמונה."),
    P("מציבים שתיים ואחת: שמונה שמיניות פחות שמינית, כלומר שבע שמיניות.", do=show("i-1", "i-ok")),
    P("ושימו לב: בנקודה בודדת אין רוחב, ולכן אין שטח.", do=show("pa-p1", "i-c2")),
    P("לכן $P(X=1)=0$, ו״קטן מ״ שווה ל״קטן או שווה ל״.", hold=0.4,
      say="לכן ההסתברות שאִקְס שווה אחת היא אפס, וקטן מ שווה לקטן או שווה ל."),
], stage=f'<div class="pd-col">{plot_a('pa')}'
         + w.eqs("i", ["$\\displaystyle\\int_1^2 \\tfrac38 x^2\\,dx=\\left[\\tfrac{x^3}{8}\\right]_1^2$",
                       "$=\\tfrac88-\\tfrac18$"], size=38)
         + w.chip("i-ok", "$=\\tfrac78$") + "</div>",
   panel=st.card("i-c1", "plain", "משתנה רציף: כל ערך בקטע")
         + st.card("i-f", "rule", "🔑 $P(a<X<b)=\\displaystyle\\int_a^b f(x)\\,dx$")
         + st.card("i-c2", "ex", "$P(X=1)=0$, ולכן $P(X<b)=P(X\\le b)$"))

cond = Scene("cond", "שני התנאים", [
    P("מתי פונקציה היא צפיפות תקינה? בדיוק כשמתקיימים שני תנאים.", hold=0.2),
    P("ראשון: **אי-שליליות**. הצפיפות לא יורדת מתחת לאפס, באף נקודה.", do=show("k-1"),
      say="ראשון: אִי שְׁלִילִיּוּת. הצפיפות לא יורדת מתחת לאפס, באף נקודה."),
    P("כי שטח מתחת לחלק שלילי היה נותן הסתברות שלילית."),
    P("שני: **נרמול**. השטח הכולל מתחת לצפיפות הוא בדיוק אחת.", do=show("k-2")),
    P("כי ההסתברות ש-$X$ יקבל ערך כלשהו היא אחת.",
      say="כי ההסתברות שאִקְס יקבל ערך כלשהו היא אחת."),
    P("נבדוק את הדוגמה שלנו. היא אי-שלילית: $x^2$ לא שלילי.", do=show("pb-all"),
      say="נבדוק את הדוגמה שלנו. היא אי שלילית: אִקְס בריבוע לא שלילי."),
    P("והשטח הכולל: $x^3$ חלקי שמונה, בין אפס לשתיים, הוא שמונה שמיניות. כלומר אחת.", do=show("k-0"),
      say="והשטח הכולל: אִקְס בשלישית חלקי שמונה, בין אפס לשתיים, הוא שמונה שמיניות. כלומר אחת."),
    P("שני התנאים מתקיימים, ולכן זו צפיפות תקינה.", do=show("k-ok"), hold=0.4),
], stage=f'<div class="pd-col">{plot_a('pb')}'
         + w.eqs("k", ["$\\displaystyle\\int_0^2 \\tfrac38 x^2\\,dx=\\left[\\tfrac{x^3}{8}\\right]_0^2=\\tfrac88=1$"], size=38)
         + w.chip("k-ok", "צפיפות תקינה ✓") + "</div>",
   panel=st.card("k-1", "rule", "🔑 $f(x)\\ge 0$ לכל $x$")
         + st.card("k-2", "rule", "🔑 $\\displaystyle\\int_{-\\infty}^{\\infty} f(x)\\,dx=1$"))

cand = Scene("cand", "שלוש מועמדות", [
    P("עכשיו שלוש מועמדות. כל אחת מוגדרת בקטע שלה, ואפס מחוצה לו."),
    P("הראשונה: $x$ פחות חצי, בקטע מאפס עד שתיים.", do=show("m1"),
      say="הראשונה: אִקְס פחות חצי, בקטע מאפס עד שתיים."),
    P("השטח שלה הוא שתיים פחות אחת, כלומר אחת. נראה טוב?", do=show("m1-a")),
    P("לא. מתחת לחצי היא **שלילית**. התנאי הראשון נכשל.", do=show("c1-bad", "m1-x")),
    P("השנייה: ארבע, בקטע מאפס עד רבע. הגובה שלה ארבע, הרבה מעל אחת.", do=show("m2")),
    P("אבל השטח הוא מלבן: ארבע כפול רבע, כלומר אחת. והיא חיובית.", do=show("m2-a")),
    P("לכן היא צפיפות תקינה. צפיפות היא **גובה**, לא הסתברות, ומותר לה לעלות על אחת.", do=show("m2-ok")),
    P("השלישית: $x$ חלקי ארבע, מאפס עד שתיים. היא אי-שלילית.", do=show("m3"),
      say="השלישית: אִקְס חלקי ארבע, מאפס עד שתיים. היא אי שלילית."),
    P("אבל השטח הוא משולש: שתיים כפול חצי, חלקי שתיים. כלומר חצי, ולא אחת.", do=show("m3-a")),
    P("התנאי השני נכשל, ולכן גם היא לא צפיפות.", do=show("m3-x"), hold=0.4),
], stage='<div class="pd-row" style="gap:16px;align-items:flex-start">'
         f'<div id="m1" class="pd-col h" style="gap:8px">{S1}<div class="pd-mid">$x-\\tfrac12$</div>'
         + w.chip("m1-a", "שטח $=1$", "warn") + w.chip("m1-x", "✗ שלילית", "bad") + '</div>'
         f'<div id="m2" class="pd-col h" style="gap:8px">{S2}<div class="pd-note" style="color:var(--ink);font-size:34px">$4$ על $[0,\\tfrac14]$</div>'
         + w.chip("m2-a", "שטח $=1$", "warn") + w.chip("m2-ok", "✓ תקינה", "ok") + '</div>'
         f'<div id="m3" class="pd-col h" style="gap:8px">{S3}<div class="pd-mid">$\\tfrac{{x}}{{4}}$</div>'
         + w.chip("m3-a", "שטח $=\\tfrac12$", "warn") + w.chip("m3-x", "✗ שטח לא 1", "bad") + '</div></div>',
   layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. $D$ הוא משתנה רציף, ובסעיף הקודם מצאו את ההתפלגות המצטברת שלו.",
      say="ועכשיו סעיף ממבחן. דִּי הוא משתנה רציף, ובסעיף הקודם מצאו את ההתפלגות המצטברת שלו."),
    P("בין אפס לאחת היא $t$ פחות $t$ כפול לוגריתם טבעי של $t$. מבקשים את הצפיפות ושרטוט.", do=show("x-0"),
      say="בין אפס לאחת היא טִי פחות טִי כפול לוגריתם טבעי של טִי. מבקשים את הצפיפות ושרטוט."),
    P("הצפיפות היא הנגזרת של ההתפלגות המצטברת. גוזרים איבר איבר.", do=show("x-1")),
    P("הנגזרת של $t$ היא אחת. ואת המכפלה גוזרים לפי כלל המכפלה: לוגריתם של $t$, ועוד אחת.", do=show("x-2"),
      say="הנגזרת של טִי היא אחת. ואת המכפלה גוזרים לפי כלל המכפלה: לוגריתם של טִי, ועוד אחת."),
    P("האחדות מתבטלות, ונשאר: מינוס הלוגריתם הטבעי של $t$, בקטע מאפס עד אחת. ומחוץ לו אפס.", do=show("x-3", "pd-f", "pd-l"),
      say="האחדות מתבטלות, ונשאר: מינוס הלוגריתם הטבעי של טִי, בקטע מאפס עד אחת. ומחוץ לו אפס."),
    P("השרטוט: באחת הצפיפות היא אפס, וכשמתקרבים לאפס היא שואפת לאינסוף.", do=show("pd-p1", "pd-inf")),
    P("וזו המלכודת: צפיפות שעולה עד אינסוף, האם היא תקינה?", do=show("x-t")),
    P("בודקים את שני התנאים. בין אפס לאחת הלוגריתם שלילי, ולכן מינוס הלוגריתם **חיובי**.", do=show("x-c1")),
    P("והשטח הכולל הוא ההתפלגות המצטברת באחת, פחות הגבול שלה באפס: אחת פחות אפס.", do=show("pd-a", "x-c2")),
    P("כן, השטח הוא אחת. הצפיפות לא חסומה, אבל השטח שמתחתיה סופי.", hold=0.3),
    P("היא מעל אחת בכל הקטע עד אחת חלקי $e$, וגם זה בסדר: גובה, לא הסתברות.", do=show("pd-one", "pd-big"),
      say="היא מעל אחת בכל הקטע עד אחת חלקי אִי, וגם זה בסדר: גובה, לא הסתברות."),
    P("אז התשובה: מינוס לוגריתם טבעי של $t$ בין אפס לאחת, ואפס בכל מקום אחר.", do=show("x-ok"), hold=0.6,
      say="אז התשובה: מינוס לוגריתם טבעי של טִי בין אפס לאחת, ואפס בכל מקום אחר."),
], stage=f'<div class="pd-col">{DP.svg()}<div class="pd-row" style="gap:18px">'
         + st.card("x-c1", "ex", "$\\ln t<0 \\Rightarrow -\\ln t>0$")
         + st.card("x-c2", "ex", "שטח $=F_D(1)-F_D(0^+)=1$")
         + "</div>" + w.chip("x-ok", "צפיפות תקינה ✓") + "</div>",
   panel=w.stem(Q["id"], "נתון $F_D(t)=t-t\\ln t$ עבור $0<t<1$. מצאו את $f_D(t)$ ושרטטו אותה.")
         + w.eqs("x", ["$F_D(t)=t-t\\ln t$", "$f_D(t)=F_D'(t)$", "$=1-(\\ln t+1)$", "$=-\\ln t,\\ \\ 0<t<1$"], size=36, gap=6)
         + st.card("x-t", "trap", "⚠️ שואפת ל-$\\infty$ ליד $0$: עדיין תקינה?"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הסתברות של משתנה רציף היא שטח מתחת לצפיפות.", do=show("r-1")),
    P("צפיפות תקינה: אי-שלילית בכל מקום, והשטח הכולל שלה אחת.", do=show("r-2"),
      say="צפיפות תקינה: אִי שלילית בכל מקום, והשטח הכולל שלה אחת."),
    P("בנקודה בודדת ההסתברות אפס, ולכן קטן וקטן-שווה זה אותו דבר.", do=show("r-3"),
      say="בנקודה בודדת ההסתברות אפס, ולכן קטן, וקטן או שווה, זה אותו דבר."),
    P("וצפיפות היא גובה: מותר לה לעלות על אחת, ואפילו לשאוף לאינסוף. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="pd-col"><div class="pd-big">$P(a<X<b)=\\displaystyle\\int_a^b f(x)\\,dx$</div></div>',
   panel=st.card("r-1", "rule", "🔑 הסתברות = שטח")
         + st.card("r-2", "rule", "🔑 $f\\ge0$ ושטח כולל $1$")
         + st.card("r-3", "rule", "🔑 $P(X=x)=0$")
         + st.card("r-4", "trap", "⚠️ $f$ היא גובה, לא הסתברות"))

VIDEO = Video("F01", "pdf", "מהי פונקציית צפיפות", w.fix_scenes([title, idea, cond, cand, exam, recap]),
              bank={"26A-B-Q1b": None})
