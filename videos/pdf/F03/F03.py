# -*- coding: utf-8 -*-
"""F03 · צפיפות מחולקת לקטעים — video script (build: tools/video/vid.py F03).

Source: courses/pdf/C03.js (lesson + goal: normalize a piecewise density; a divergent piece forces its constant to 0).
Exam anchor: 25S-B-Q4a (f = a + b/(x sqrt x) + c x on (0,1]: b = 0 because x^{-3/2} is not integrable at 0, then
c = 2 - 2a, and f >= 0 at both ends gives 0 <= a <= 2, -2 <= c <= 2). No guided quiz uses it.
Not used on purpose: every C03 quiz item (a / 2a on [0,1),[1,2); ax / a; a e^x with e^{-x}/2; a with a/x^2; the
divergence multiple choice with c/x^2, c e^{-x}, c/sqrt x on (0,1], c/x). Worked examples use new functions:
a x^2 on [0,1) + a on [1,3) (a = 3/7), and a on [0,1) + b/sqrt x on [1,oo) (b = 0, a = 1), compared with b/x^3.
Every integral, constant and range is computed with sympy and cross-checked numerically (w_pdf.Pdf / mpmath).
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo, nint

a, b, c = sp.symbols("a b c", real=True)

# ---------------------------------------------------------------- example 1: a x^2 on [0,1), a on [1,3)
m1, m2 = sp.integrate(a * x**2, (x, 0, 1)), sp.integrate(a, (x, 1, 3))
assert m1 == a / 3 and m2 == 2 * a
A1 = sp.solve(m1 + m2 - 1, a)[0]
assert A1 == R(3, 7)
E1 = Pdf([(0, 1, A1 * x**2), (1, 3, A1)])
assert E1.total() == 1 and E1.nonneg()
assert E1.prob(0, 1) == R(1, 7) and E1.prob(1, 3) == R(6, 7)

# ---------------------------------------------------------------- example 2: a on [0,1), b/sqrt(x) on [1, oo)
assert sp.integrate(1 / sp.sqrt(x), (x, 1, oo)) == oo           # p = 1/2 <= 1 at infinity: diverges
assert sp.limit(2 * sp.sqrt(t) - 2, t, oo) == oo                 # its antiderivative 2 sqrt(x) grows without bound
assert sp.integrate(x**-3, (x, 1, oo)) == R(1, 2)                # p = 3 > 1: converges, 1/(p-1)
assert abs(nint(x**-3, 1, oo) - 0.5) < 1e-9
assert Pdf([(0, 1, 1)]).total() == 1                             # b = 0 leaves a = 1
assert abs(1 / math.sqrt(100) - 0.1) < 1e-12 and abs(100.0**-3 - 1e-6) < 1e-18

# ---------------------------------------------------------------- exam 25S-B-Q4a
Q = BANK["25S-B-Q4a"]
assert "x\\sqrt x" in BANK["25S-B-Q4a"]["solution"] or "x\\sqrt x" in str(Q)
assert sp.integrate(x**R(-3, 2), (x, 0, 1)) == oo                # p = 3/2 >= 1 at 0: diverges, so b = 0
assert sp.limit(-2 / sp.sqrt(t), t, 0, "+") == -oo               # antiderivative -2 x^{-1/2} blows up at 0
assert sp.integrate(a + c * x, (x, 0, 1)) == a + c / 2
csol = sp.solve(a + c / 2 - 1, c)[0]
assert csol == 2 - 2 * a
fa = a + csol * x
assert fa.subs(x, 0) == a and sp.expand(fa.subs(x, 1)) == 2 - a
assert sp.reduce_inequalities([a >= 0, 2 - a >= 0], a).as_set() == sp.Interval(0, 2)
assert csol.subs(a, 0) == 2 and csol.subs(a, 2) == -2
FAM = {}
for av in (0, 1, 2, R(5, 2)):
    p = Pdf([(0, 1, fa.subs(a, av))])
    assert p.total() == 1
    FAM[av] = p.nonneg()
assert FAM == {0: True, 1: True, 2: True, R(5, 2): False}       # a = 5/2: area 1 but f(1) = -1/2

# ---------------------------------------------------------------- figures
P1 = w.Plot("p1", (-0.15, 3.4), (0, 0.62), w=820, h=380, xticks=[(1, "1"), (2, "2"), (3, "3")],
            yticks=[(3 / 7, "3/7")])
fp = lambda v: 3 / 7 * v * v if v < 1 else 3 / 7
P1.area("p1-a1", lambda v: 3 / 7 * v * v, 0, 1, kind="a")
P1.area("p1-a2", lambda v: 3 / 7, 1, 3, kind="b")
P1.curve("p1-f1", lambda v: 3 / 7 * v * v, 0, 1, hidden=False)
P1.seg("p1-f2", [(1, 3 / 7), (3, 3 / 7)], kind="b", hidden=False)
P1.vline("p1-g", 1, 0, 3 / 7, hidden=False)
P1.vline("p1-g3", 3, 0, 3 / 7, hidden=False)
P1.label("p1-l1", 0.45, 0.25, "a·x²", kind="a", hidden=False)
P1.label("p1-l2", 2.0, 0.5, "a", kind="b", hidden=False)

P2 = w.Plot("p2", (-0.2, 8.6), (0, 1.25), w=820, h=380, xticks=[(1, "1"), (4, "4"), (8, "8")],
            yticks=[(0.5, "0.5"), (1, "1")])
P2.seg("p2-a", [(0, 1), (1, 1)], kind="ink", hidden=False)
P2.curve("p2-s", lambda v: 1 / math.sqrt(v), 1, 8.4, kind="c")
P2.curve("p2-c", lambda v: v**-3, 1, 8.4, kind="b")
P2.label("p2-ls", 6.2, 0.52, "1/√x", kind="c")
P2.label("p2-lc", 2.6, 0.16, "1/x³", kind="b")

P3 = w.Plot("p3", (-0.08, 1.25), (-0.75, 2.75), w=760, h=400, xticks=[(1, "1")], yticks=[(1, "1"), (2, "2")])
P3.seg("p3-0", [(0, 0), (1, 2)], kind="a")
P3.seg("p3-1", [(0, 1), (1, 1)], kind="b")
P3.seg("p3-2", [(0, 2), (1, 0)], kind="d")
P3.seg("p3-bad", [(0, 2.5), (1, -0.5)], kind="bad", dash=True)
P3.label("p3-l0", 1.04, 2.0, "a = 0", kind="a", anchor="start")
P3.label("p3-l1", 1.04, 1.0, "a = 1", kind="b", anchor="start")
P3.label("p3-l2", 1.04, 0.12, "a = 2", kind="d", anchor="start")
P3.label("p3-lb", 1.04, -0.55, "a = 5/2 ✗", kind="bad", anchor="start")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה ננרמל צפיפות שהנוסחה שלה משתנה מקטע לקטע."),
    P("ונלמד כלל חשוב: כשאינטגרל של חלק מתבדר, הקבוע שלפניו חייב להיות אפס."),
    P("ובסוף נפתור סעיף ממבחן שבנוי בדיוק על הכלל הזה.", hold=0.4),
], stage='<div class="kicker">F03 · משתנה רציף</div><h1>צפיפות מחולקת לקטעים</h1>'
         '<p>לנרמל צפיפות שנוסחתה משתנה בין קטעים, ולזהות מתי אינטגרל מתבדר ולכן קבוע חייב להיות 0.</p>',
   layout="title")

split = Scene("split", "מפצלים לקטעים", [
    P("הנה צפיפות בשני קטעים: $a$ כפול $x^2$ מאפס עד אחת, ואז הקבוע $a$ עד שלוש.", do=show("s-f"),
      say="הנה צפיפות בשני קטעים: אֵיי כפול אִקְס בריבוע מאפס עד אחת, ואז הקבוע אֵיי עד שלוש."),
    P("אין כאן שום דבר חדש: מפצלים את האינטגרל לפי הקטעים, ומחברים.", do=show("s-r")),
    P("החלק הראשון: האינטגרל של $a x^2$ מאפס עד אחת הוא $a$ שלישים.", do=show("s-0", "p1-a1"),
      say="החלק הראשון: האינטגרל של אֵיי אִקְס בריבוע מאפס עד אחת הוא אֵיי שלישים."),
    P("החלק השני הוא מלבן: רוחב שתיים, גובה $a$. כלומר שתיים $a$.", do=show("s-1", "p1-a2"),
      say="החלק השני הוא מלבן: רוחב שתיים, גובה אֵיי. כלומר שתיים אֵיי."),
    P("הסכום הוא שבע $a$ שלישים, והוא שווה אחת. לכן $a$ הוא שלוש שביעיות.", do=show("s-2", "s-ok"),
      say="הסכום הוא שבע אֵיי שלישים, והוא שווה אחת. לכן אֵיי הוא שלוש שביעיות."),
    P("ומחוץ לשני הקטעים הצפיפות אפס, ולכן שם אין שום תרומה.", hold=0.4),
], stage=f'<div class="pd-col">{P1.svg()}'
         + w.chip("s-f", "$f=a\\,x^2$ על $[0,1)$, $\\ f=a$ על $[1,3)$", "warn") + "</div>",
   panel=st.card("s-r", "rule", "🔑 $\\int f=\\int_{I_1} f+\\int_{I_2} f=1$")
         + w.eqs("s", ["$\\displaystyle\\int_0^1 a\\,x^2\\,dx=\\tfrac a3$", "$\\displaystyle\\int_1^3 a\\,dx=2a$",
                       "$\\tfrac a3+2a=\\tfrac{7a}{3}=1$"], size=38, gap=10)
         + w.chip("s-ok", "$a=\\tfrac37$"))

zero = Scene("zero", "כלל האפס", [
    P("ועכשיו קטע אינסופי: $a$ מאפס עד אחת, ו-$b$ חלקי שורש $x$ מאחת עד אינסוף.", do=show("z-f", "p2-s", "p2-ls"),
      say="ועכשיו קטע אינסופי: אֵיי מאפס עד אחת, ובִּי חלקי שורש אִקְס מאחת עד אינסוף."),
    P("הצפיפות יורדת, אבל לאט מדי. הפונקציה הקדומה של אחד חלקי שורש $x$ היא שתיים שורש $x$.", do=show("z-0"),
      say="הצפיפות יורדת, אבל לאט מדי. הפונקציה הקדומה של אחד חלקי שורש אִקְס היא שתיים שורש אִקְס."),
    P("ושתיים שורש $x$ גדל בלי גבול. האינטגרל **מתבדר**.", do=show("z-1"),
      say="ושתיים שורש אִקְס גדל בלי גבול. האינטגרל מתבדר."),
    P("אם $b$ לא אפס, השטח הכולל אינסופי, ולא אחת. לכן חייב להיות $b$ שווה אפס.", do=show("z-ok"),
      say="אם בִּי לא אפס, השטח הכולל אינסופי, ולא אחת. לכן חייב להיות בִּי שווה אפס."),
    P("ואז נשאר רק המלבן הראשון, ו-$a$ שווה אחת.", do=show("z-2"),
      say="ואז נשאר רק המלבן הראשון, ואֵיי שווה אחת."),
    P("השוו ל-$b$ חלקי $x^3$: הוא יורד מהר, והאינטגרל מאחת עד אינסוף הוא חצי.", do=show("p2-c", "p2-lc", "z-3"),
      say="השוו לבִּי חלקי אִקְס בשלישית: הוא יורד מהר, והאינטגרל מאחת עד אינסוף הוא חצי."),
    P("הכלל: אחד חלקי $x$ בחזקת $p$, מאחת עד אינסוף, מתכנס רק כש-$p$ גדול מאחת.", do=show("z-r1"),
      say="הכלל: אחד חלקי אִקְס בחזקת פִּי, מאחת עד אינסוף, מתכנס רק כשפִּי גדול מאחת."),
    P("וליד אפס זה הפוך: מאפס עד אחת הוא מתכנס רק כש-$p$ קטן מאחת.", do=show("z-r2"), hold=0.4,
      say="וליד אפס זה הפוך: מאפס עד אחת הוא מתכנס רק כשפִּי קטן מאחת."),
], stage=f'<div class="pd-col">{P2.svg()}'
         + w.chip("z-f", "$f=a$ על $[0,1)$, $\\ f=\\tfrac{b}{\\sqrt x}$ על $[1,\\infty)$", "warn") + "</div>",
   panel=w.eqs("z", ["$\\displaystyle\\int_1^M \\tfrac{dx}{\\sqrt x}=2\\sqrt M-2$", "$\\to\\infty$",
                     "$a\\cdot 1=1\\ \\Rightarrow\\ a=1$", "$\\displaystyle\\int_1^\\infty \\tfrac{dx}{x^3}=\\tfrac12$"],
                 size=36, gap=6)
         + w.chip("z-ok", "$b=0$")
         + st.card("z-r1", "rule", "🔑 $\\int_1^\\infty x^{-p}\\,dx$ מתכנס רק אם $p>1$")
         + st.card("z-r2", "rule", "🔑 $\\int_0^1 x^{-p}\\,dx$ מתכנס רק אם $p<1$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: הצפיפות היא $a$, ועוד $b$ חלקי $x$ שורש $x$, ועוד $c x$, בין אפס לאחת.",
      say="שאלה ממבחן: הצפיפות היא אֵיי, ועוד בִּי חלקי אִקְס שורש אִקְס, ועוד סִי אִקְס, בין אפס לאחת."),
    P("שואלים: מהן המגבלות על $a$, $b$ ו-$c$? ומבקשים לנמק.",
      say="שואלים: מהן המגבלות על אֵיי, בִּי וסִי? ומבקשים לנמק."),
    P("מתחילים בנרמול. האיבר האמצעי הוא $x$ בחזקת מינוס שלושה חצאים, ליד אפס.", do=show("x-0"),
      say="מתחילים בנרמול. האיבר האמצעי הוא אִקְס בחזקת מינוס שלושה חצאים, ליד אפס."),
    P("ליד אפס צריך חזקה קטנה מאחת, ושלושה חצאים גדול מאחת. האינטגרל מתבדר.", do=show("x-1")),
    P("ושימו לב למלכודת: הפונקציה הקדומה מינוס שתיים חלקי שורש $x$, ובאפס היא מתפוצצת. היא לא נותנת שתיים.",
      do=show("x-t"),
      say="ושימו לב למלכודת: הפונקציה הקדומה היא מינוס שתיים חלקי שורש אִקְס, ובאפס היא מתפוצצת. היא לא נותנת שתיים."),
    P("השאר סופי, ולכן שום דבר לא יכול לבטל את האינסוף. מכאן $b$ שווה אפס.", do=show("x-2"),
      say="השאר סופי, ולכן שום דבר לא יכול לבטל את האינסוף. מכאן בִּי שווה אפס."),
    P("עכשיו הנרמול של מה שנשאר: $a$ ועוד $c$ חצאים שווה אחת. כלומר $c$ שווה שתיים פחות שתיים $a$.", do=show("x-3"),
      say="עכשיו הנרמול של מה שנשאר: אֵיי ועוד סִי חצאים שווה אחת. כלומר סִי שווה שתיים פחות שתיים אֵיי."),
    P("אבל זה עוד לא הכול: הצפיפות חייבת להיות גם אי-שלילית.", do=show("p3-1", "p3-l1"),
      say="אבל זה עוד לא הכול: הצפיפות חייבת להיות גם אִי שלילית."),
    P("כל הישרים האלה הם בעלי שטח אחת. למשל $a$ שווה חמישה חצאים: השטח אחת, אבל באחת הישר יורד מתחת לאפס.",
      do=show("p3-bad", "p3-lb"),
      say="כל הישרים האלה הם בעלי שטח אחת. למשל אֵיי שווה חמישה חצאים: השטח אחת, אבל באחת הישר יורד מתחת לאפס."),
    P("ישר הוא אי-שלילי בקטע רק אם שני הקצוות שלו אי-שליליים. באפס הערך הוא $a$, ובאחת הוא שתיים פחות $a$.",
      do=show("x-4", "p3-0", "p3-l0", "p3-2", "p3-l2"),
      say="ישר הוא אִי שלילי בקטע רק אם שני הקצוות שלו אִי שליליים. באפס הערך הוא אֵיי, ובאחת הוא שתיים פחות אֵיי."),
    P("לכן $a$ בין אפס לשתיים, ו-$c$ בין מינוס שתיים לשתיים.", do=show("x-5", "x-ok"),
      say="לכן אֵיי בין אפס לשתיים, וסִי בין מינוס שתיים לשתיים."),
    P("והמלכודת השנייה: לבדוק אי-שליליות רק בקצה אחד. צריך את שניהם.", hold=0.6,
      say="והמלכודת השנייה: לבדוק אִי שליליות רק בקצה אחד. צריך את שניהם."),
], stage=f'<div class="pd-col">{P3.svg()}'
         + st.card("x-t", "trap", "⚠️ $\\int_0^1 x^{-3/2}\\,dx$ אינו $2$: הוא $\\infty$")
         + w.chip("x-ok", "$b=0,\\ c=2-2a,\\ 0\\le a\\le 2$") + "</div>",
   panel=w.stem(Q["id"], "$f_X(x)=a+\\dfrac{b}{x\\sqrt x}+c\\,x$ עבור $0<x\\le1$. מהן המגבלות על $a,b,c$?")
         + w.eqs("x", ["$\\dfrac{b}{x\\sqrt x}=b\\,x^{-3/2}$", "<span dir=\"rtl\">$p=\\tfrac32\\ge1$: מתבדר ליד $0$</span>",
                       "$b=0$", "$a+\\tfrac c2=1\\ \\Rightarrow\\ c=2-2a$", "$f(0)=a\\ge0,\\ \\ f(1)=2-a\\ge0$",
                       "$0\\le a\\le2,\\ \\ -2\\le c\\le2$"], size=32, gap=4))

recap = Scene("recap", "סיכום", [
    P("לסיכום: צפיפות בקטעים מנרמלים קטע אחר קטע, ומחברים את השטחים.", do=show("r-1")),
    P("אינטגרל שמתבדר מכריח את הקבוע שלפניו להיות אפס.", do=show("r-2")),
    P("אחד חלקי $x$ בחזקת $p$: באינסוף צריך $p$ גדול מאחת, וליד אפס צריך $p$ קטן מאחת.", do=show("r-3"),
      say="אחד חלקי אִקְס בחזקת פִּי: באינסוף צריך פִּי גדול מאחת, וליד אפס צריך פִּי קטן מאחת."),
    P("ואחרי הנרמול, בודקים אי-שליליות בכל הקטע. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6,
      say="ואחרי הנרמול, בודקים אִי שליליות בכל הקטע. נתראה ברמה הבאה."),
], stage='<div class="pd-col"><div class="pd-big">$\\displaystyle\\int f=\\int_{I_1}f+\\int_{I_2}f+\\cdots=1$</div></div>',
   panel=st.card("r-1", "rule", "🔑 מפצלים לפי הקטעים ומחברים")
         + st.card("r-2", "rule", "🔑 אינטגרל מתבדר ⇐ הקבוע $=0$")
         + st.card("r-3", "ex", "$[1,\\infty)$: $p>1$, $\\ (0,1]$: $p<1$")
         + st.card("r-4", "trap", "⚠️ $f\\ge0$ בכל הקטע, לא בנקודה אחת"))

VIDEO = Video("F03", "pdf", "צפיפות מחולקת לקטעים", w.fix_scenes([title, split, zero, exam, recap]),
              bank={"25S-B-Q4a": None})
