# -*- coding: utf-8 -*-
"""F02 · נרמול: מציאת קבוע אחד — video script (build: tools/video/vid.py F02).

Source: courses/pdf/C02.js (lesson + goal: find one unknown constant from "total area = 1").
Exam anchor: 25B-B-Q1e (from F_X(t) = 2t - t^2 to the density 2(1-t) on [0,1), sketch, verify normalization). No
guided quiz uses it; F_X of part 25B-B-Q1d is quoted as given. The normalization recipe is then run on the shape
c(1-t) and gives back c = 2.
Not used on purpose: every C02 quiz item (cx on [0,2], cx^2 on [0,3], c(1-x^2) on [-1,1], ce^{-2x}, cx on [0,3]
with its bug). Worked examples use new functions: cx^3 on [0,2] (c = 1/4), cx on [1,3] (c = 1/4; the forgotten lower
limit gives 2/9, whose area is 8/9), ce^{-x/3} on [0,oo) (c = 1/3).
Every constant and area is solved with sympy and cross-checked by mpmath quadrature (w_pdf.Pdf).
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo

c = sp.Symbol("c", positive=True)

# ---------------------------------------------------------------- example 1: c x^3 on [0, 2]
I1 = sp.integrate(c * x**3, (x, 0, 2))
assert I1 == 4 * c and sp.solve(I1 - 1, c) == [R(1, 4)]
assert Pdf([(0, 2, x**3 / 4)]).total() == 1 and Pdf([(0, 2, x**3 / 4)]).nonneg()

# ---------------------------------------------------------------- example 2 (trap): c x on [1, 3]
I2 = sp.integrate(c * x, (x, 1, 3))
assert I2 == 4 * c and sp.solve(I2 - 1, c) == [R(1, 4)]
assert sp.integrate(x, (x, 0, 3)) == R(9, 2)              # the wrong value: only the upper limit, 9/2 (times c)
WRONG = sp.solve(c * R(9, 2) - 1, c)[0]
assert WRONG == R(2, 9)
assert Pdf([(1, 3, WRONG * x)]).total() == R(8, 9)        # the check exposes it: area 8/9, not 1
assert Pdf([(1, 3, x / 4)]).total() == 1

# ---------------------------------------------------------------- example 3: c e^{-x/3} on [0, oo)
I3 = sp.integrate(c * sp.exp(-x / 3), (x, 0, oo))
assert I3 == 3 * c and sp.solve(I3 - 1, c) == [R(1, 3)]
assert Pdf([(0, oo, sp.exp(-x / 3) / 3)]).total() == 1

# ---------------------------------------------------------------- exam 25B-B-Q1e
Q = BANK["25B-B-Q1e"]
assert "f_X(t)" in Q["question"] and "2(1-t)" in Q["solution"]
FX = 2 * t - t**2
fX = sp.diff(FX, t)
assert sp.expand(fX - 2 * (1 - t)) == 0
assert FX.subs(t, 0) == 0 and FX.subs(t, 1) == 1          # F joins 0 and 1 continuously
EX = Pdf([(0, 1, 2 * (1 - x))])
assert EX.total() == 1 and EX.nonneg()
assert R(1, 2) * 1 * 2 == 1                                # the triangle: base 1, height 2
assert sp.solve(sp.integrate(c * (1 - x), (x, 0, 1)) - 1, c) == [2]

# ---------------------------------------------------------------- figures
P1 = w.Plot("p1", (-0.15, 2.35), (0, 2.25), w=760, h=400, xticks=[(1, "1"), (2, "2")], yticks=[(1, "1"), (2, "2")])
P1.curve("p1-f", lambda v: v**3 / 4, 0, 2)
P1.area("p1-a", lambda v: v**3 / 4, 0, 2, kind="a")
P1.vline("p1-g", 2, 0, 2)
P1.label("p1-l", 1.0, 1.25, "f(x) = x³/4", kind="a")

P2 = w.Plot("p2", (-0.15, 3.35), (0, 0.95), w=760, h=380, xticks=[(1, "1"), (2, "2"), (3, "3")],
            yticks=[(0.25, "0.25"), (0.75, "0.75")])
P2.area("p2-ok", lambda v: v / 4, 1, 3, kind="a")
P2.area("p2-bad", lambda v: v / 4, 0, 1, kind="c")
P2.curve("p2-f", lambda v: v / 4, 1, 3)
P2.curve("p2-ghost", lambda v: v / 4, 0, 1, kind="c", dash=True)
P2.vline("p2-g1", 1, 0, 0.25, hidden=False)
P2.vline("p2-g3", 3, 0, 0.75, hidden=False)
P2.label("p2-l", 1.6, 0.62, "f(x) = x/4", kind="a")
P2.label("p2-lb", 0.5, 0.3, "לא בתחום", kind="bad")

P3 = w.Plot("p3", (-0.3, 9.3), (0, 0.42), w=760, h=380, xticks=[(3, "3"), (6, "6"), (9, "9")],
            yticks=[(1 / 3, "1/3")])
f3 = lambda v: math.exp(-v / 3) / 3
P3.area("p3-a", f3, 0, 9.1, kind="a")
P3.curve("p3-f", f3, 0, 9.1)
P3.label("p3-dots", 8.6, 0.06, "→ ∞", kind="ink")

P4 = w.Plot("p4", (-0.35, 1.45), (0, 2.3), w=700, h=400, xticks=[(1, "1")], yticks=[(1, "1"), (2, "2")],
            xname="t", yname="f(t)")
P4.seg("p4-f", [(0, 2), (1, 0)])
P4.seg("p4-z1", [(-0.33, 0), (0, 0)])
P4.seg("p4-z2", [(1, 0), (1.4, 0)])
P4.area("p4-a", lambda v: 2 * (1 - v), 0, 1, kind="a")
P4.dot("p4-d0", 0, 2, "(0, 2)", dx=16, dy=-10)
P4.dot("p4-d1", 1, 0, "(1, 0)", dx=0, dy=-20, anchor="middle")
P4.label("p4-l", 0.62, 1.15, "2(1 − t)", kind="a")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נמצא קבוע לא ידוע בתוך צפיפות."),
    P("הכלי היחיד שנצטרך הוא תנאי הנרמול: השטח הכולל הוא אחת."),
    P("ובסוף נפתור סעיף ממבחן שבו בודקים בדיוק את התנאי הזה.", hold=0.4),
], stage='<div class="kicker">F02 · משתנה רציף</div><h1>נרמול: מציאת קבוע אחד</h1>'
         '<p>למצוא קבוע לא ידוע בצפיפות מהתנאי שהשטח הכולל הוא 1.</p>', layout="title")

recipe = Scene("recipe", "המתכון", [
    P("במבחן נותנים צפיפות עם קבוע, למשל $c$ כפול $x^3$ בקטע מאפס עד שתיים, ושואלים מהו $c$.",
      do=show("a-f", "p1-f", "p1-l"),
      say="במבחן נותנים צפיפות עם קבוע, למשל סִי כפול אִקְס בשלישית בקטע מאפס עד שתיים, ושואלים מהו סִי."),
    P("יש רק תנאי אחד שקובע אותו: השטח הכולל חייב להיות אחת.", do=show("r-1")),
    P("צעד ראשון: כותבים את האינטגרל על התחום, ומשווים לאחת.", do=show("a-0")),
    P("צעד שני: $c$ הוא קבוע, ולכן הוא יוצא מהאינטגרל.", do=show("a-1", "r-2"),
      say="צעד שני: סִי הוא קבוע, ולכן הוא יוצא מהאינטגרל."),
    P("הפונקציה הקדומה של $x^3$ היא $x^4$ חלקי ארבע. בשתיים זה שש עשרה חלקי ארבע, כלומר ארבע.",
      do=show("a-2"),
      say="הפונקציה הקדומה של אִקְס בשלישית היא אִקְס ברביעית חלקי ארבע. בשתיים זה שש עשרה חלקי ארבע, כלומר ארבע."),
    P("צעד שלישי: משוואה פשוטה. ארבע $c$ שווה אחת, ולכן $c$ הוא רבע.", do=show("a-3", "r-3"),
      say="צעד שלישי: משוואה פשוטה. ארבע סִי שווה אחת, ולכן סִי הוא רבע."),
    P("בדיקה מהירה: $c$ חיובי, ולכן הצפיפות אי-שלילית. והשטח הוא אחת מעצם הפתרון.", do=show("p1-a", "p1-g"), hold=0.4,
      say="בדיקה מהירה: סִי חיובי, ולכן הצפיפות אי שלילית. והשטח הוא אחת מעצם הפתרון."),
], stage=f'<div class="pd-col">{P1.svg()}'
         + w.chip("a-f", "$f(x)=c\\,x^3,\\ \\ 0\\le x\\le 2$", "warn") + "</div>",
   panel=w.eqs("a", ["$\\displaystyle\\int_0^2 c\\,x^3\\,dx=1$", "$c\\left[\\tfrac{x^4}{4}\\right]_0^2=1$",
                     "$c\\cdot\\tfrac{16}{4}=4c=1$", "$c=\\tfrac14$"], size=40, gap=10)
         + st.card("r-1", "rule", "🔑 $\\displaystyle\\int f=1$ על התחום")
         + st.card("r-2", "ex", "הקבוע יוצא מהאינטגרל")
         + st.card("r-3", "ex", "משוואה ליניארית אחת ב-$c$"))

trap = Scene("trap", "המלכודת", [
    P("עכשיו צפיפות שהתחום שלה לא מתחיל באפס: $c$ כפול $x$, בקטע מאחת עד שלוש.", do=show("p2-f", "p2-l", "b-f"),
      say="עכשיו צפיפות שהתחום שלה לא מתחיל באפס: סִי כפול אִקְס, בקטע מאחת עד שלוש."),
    P("הפונקציה הקדומה היא $x^2$ חלקי שתיים. מציבים את **שני** הגבולות.", do=show("b-0"),
      say="הפונקציה הקדומה היא אִקְס בריבוע חלקי שתיים. מציבים את שני הגבולות."),
    P("תשעה חצאים, פחות חצי. זה ארבע.", do=show("b-1")),
    P("לכן ארבע $c$ שווה אחת, ושוב $c$ הוא רבע.", do=show("b-2", "p2-ok"),
      say="לכן ארבע סִי שווה אחת, ושוב סִי הוא רבע."),
    P("והטעות הנפוצה: מציבים רק את שלוש, ושוכחים את הגבול התחתון.", do=show("t-1")),
    P("מקבלים תשעה חצאים $c$ שווה אחת, כלומר $c$ שווה שתיים תשיעיות.", do=show("t-2"),
      say="מקבלים תשעה חצאים סִי שווה אחת, כלומר סִי שווה שתיים תשיעיות."),
    P("זה בעצם אינטגרל מאפס, שכולל גם את המשולש הוורוד, שבכלל לא בתחום.", do=show("p2-bad", "p2-ghost", "p2-lb")),
    P("והבדיקה תופסת את זה: עם שתיים תשיעיות, השטח בקטע מאחת עד שלוש יוצא שמונה תשיעיות, ולא אחת.",
      do=show("t-3"), hold=0.4),
], stage=f'<div class="pd-col">{P2.svg()}'
         + w.chip("b-f", "$f(x)=c\\,x,\\ \\ 1\\le x\\le 3$", "warn") + "</div>",
   panel=w.eqs("b", ["$c\\left[\\tfrac{x^2}{2}\\right]_1^3=1$", "$c\\left(\\tfrac92-\\tfrac12\\right)=4c$",
                     "$c=\\tfrac14\\ \\checkmark$"], size=40, gap=10)
         + st.card("t-1", "trap", "⚠️ שוכחים את הגבול התחתון:")
         + st.card("t-2", "ex", "$\\tfrac92 c=1 \\Rightarrow c=\\tfrac29$ ✗")
         + st.card("t-3", "ex", "בדיקה: $\\displaystyle\\int_1^3 \\tfrac29 x\\,dx=\\tfrac89\\ne1$"))

expo = Scene("expo", "תחום אינסופי", [
    P("ומה אם התחום אינסופי? $c$ כפול $e$ בחזקת מינוס $x$ שלישים, לכל $x$ חיובי.", do=show("p3-f", "e-f"),
      say="ומה אם התחום אינסופי? סִי כפול אִי בחזקת מינוס אִקְס שלישים, לכל אִקְס חיובי."),
    P("יש נוסחה שכדאי לזכור: האינטגרל מאפס עד אינסוף של $e$ בחזקת מינוס $k x$ הוא אחד חלקי $k$.", do=show("e-r"),
      say="יש נוסחה שכדאי לזכור: האינטגרל מאפס עד אינסוף של אִי בחזקת מינוס קֵיי אִקְס, הוא אחד חלקי קֵיי."),
    P("כאן $k$ הוא שליש, ולכן האינטגרל הוא שלוש.", do=show("e-0"),
      say="כאן קֵיי הוא שליש, ולכן האינטגרל הוא שלוש."),
    P("שלוש $c$ שווה אחת, ולכן $c$ הוא שליש.", do=show("e-1", "p3-a", "p3-dots"),
      say="שלוש סִי שווה אחת, ולכן סִי הוא שליש."),
    P("השטח נמשך עד אינסוף, אבל הוא סופי, ושווה בדיוק אחת.", hold=0.4),
], stage=f'<div class="pd-col">{P3.svg()}'
         + w.chip("e-f", "$f(x)=c\\,e^{-x/3},\\ \\ x\\ge0$", "warn") + "</div>",
   panel=st.card("e-r", "rule", "🔑 $\\displaystyle\\int_0^\\infty e^{-kx}\\,dx=\\frac1k$, עבור $k>0$")
         + w.eqs("e", ["$\\displaystyle c\\int_0^\\infty e^{-x/3}\\,dx=3c$", "$3c=1\\ \\Rightarrow\\ c=\\tfrac13$"],
                 size=40, gap=12))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו סעיף ממבחן. בסעיף הקודם מצאו את ההתפלגות המצטברת: שתיים $t$ פחות $t^2$, בין אפס לאחת.",
      say="ועכשיו סעיף ממבחן. בסעיף הקודם מצאו את ההתפלגות המצטברת: שתיים טִי פחות טִי בריבוע, בין אפס לאחת."),
    P("לפני אפס היא אפס, ומאחת והלאה היא אחת. מבקשים צפיפות, שרטוט, ובדיקה של הנרמול."),
    P("הצפיפות היא הנגזרת של ההתפלגות המצטברת: שתיים פחות שתיים $t$.", do=show("x-0"),
      say="הצפיפות היא הנגזרת של ההתפלגות המצטברת: שתיים פחות שתיים טִי."),
    P("וזו המלכודת של הסעיף: מחוץ לקטע ההתפלגות המצטברת קבועה, ולכן שם הצפיפות **אפס**.", do=show("x-1", "x-t"),
      say="וזו המלכודת של הסעיף: מחוץ לקטע ההתפלגות המצטברת קבועה, ולכן שם הצפיפות אפס."),
    P("השרטוט: ישר יורד, משתיים באפס, עד אפס באחת.", do=show("p4-f", "p4-z1", "p4-z2", "p4-d0", "p4-d1", "p4-l")),
    P("ועכשיו הנרמול. השטח הוא משולש: בסיס אחת, גובה שתיים.", do=show("p4-a")),
    P("חצי כפול אחת כפול שתיים, וזה בדיוק אחת. הנרמול מתקיים.", do=show("x-2", "x-ok")),
    P("ועכשיו נעשה את זה הפוך: נניח שידענו רק את הצורה, $c$ כפול אחת פחות $t$.", do=show("x-3"),
      say="ועכשיו נעשה את זה הפוך: נניח שידענו רק את הצורה, סִי כפול, אחת פחות טִי."),
    P("האינטגרל של אחת פחות $t$ מאפס עד אחת הוא חצי. חצי $c$ שווה אחת, ולכן $c$ שווה שתיים.",
      do=show("x-4"),
      say="האינטגרל של אחת פחות טִי מאפס עד אחת הוא חצי. חצי סִי שווה אחת, ולכן סִי שווה שתיים."),
    P("בדיוק הקבוע שקיבלנו מהנגזרת. הנרמול קובע את הקבוע.", hold=0.6),
], stage=f'<div class="pd-col">{P4.svg()}</div>',
   panel=w.stem(Q["id"], "נתון $F_X(t)=2t-t^2$ עבור $0\\le t<1$. מצאו את $f_X(t)$, שרטטו, ובדקו נרמול.")
         + w.eqs("x", ["$f_X(t)=F_X'(t)=2-2t$", "<span dir=\"rtl\">$f_X=0$ מחוץ ל-$[0,1)$</span>", "<span dir=\"rtl\">שטח $=\\tfrac12\\cdot1\\cdot2=1$</span>",
                       "$f=c\\,(1-t)$", "$\\tfrac c2=1\\ \\Rightarrow\\ c=2$"], size=34, gap=4)
         + st.card("x-t", "trap", "⚠️ לשכוח את האפס מחוץ לקטע")
         + w.chip("x-ok", "הנרמול מתקיים ✓"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: קבוע לא ידוע בצפיפות נקבע מהנרמול. כותבים שהשטח הכולל הוא אחת.", do=show("r-a")),
    P("הקבוע יוצא מהאינטגרל, ונשארת משוואה ליניארית אחת.", do=show("r-b")),
    P("מציבים את **שני** הגבולות, ובודקים שהשטח יוצא אחת.", do=show("r-c")),
    P("ובתחום אינסופי, האינטגרל של $e$ בחזקת מינוס $k x$ הוא אחד חלקי $k$. נתראה ברמה הבאה.", do=show("r-d"), hold=0.6,
      say="ובתחום אינסופי, האינטגרל של אִי בחזקת מינוס קֵיי אִקְס הוא אחד חלקי קֵיי. נתראה ברמה הבאה."),
], stage='<div class="pd-col"><div class="pd-big">$\\displaystyle\\int_{-\\infty}^{\\infty} f(x)\\,dx=1$</div></div>',
   panel=st.card("r-a", "rule", "🔑 $\\int f=1$ קובע את הקבוע")
         + st.card("r-b", "rule", "🔑 הקבוע יוצא החוצה: משוואה ליניארית")
         + st.card("r-c", "trap", "⚠️ גם הגבול התחתון")
         + st.card("r-d", "rule", "🔑 $\\int_0^\\infty e^{-kx}\\,dx=\\frac1k$"))

VIDEO = Video("F02", "pdf", "נרמול: מציאת קבוע אחד", w.fix_scenes([title, recipe, trap, expo, exam, recap]),
              bank={"25B-B-Q1e": None})
