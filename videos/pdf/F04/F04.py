# -*- coding: utf-8 -*-
"""F04 · שני קבועים: נרמול ותוחלת — video script (build: tools/video/vid.py F04).

Source: courses/pdf/C04.js (lesson + goal: two constants from normalization + the mean, also with a symbolic mu).
Exam anchor: 26A-A-Q4a (a e^x for x<0, b(1-x)^2 on [0,2), c for x>=2, E[X] = mu: c = 0 because a constant on a ray
is not integrable, then a + 2b/3 = 1 and -a + 2b/3 = mu, so a = (1-mu)/2, b = 3(1+mu)/4). No guided quiz uses it.
Not used on purpose: every C04 quiz item (a / b on [0,1),[1,2) with E = 7/6 or mu; ax / b; a on [-2,0) + b e^{-x};
a e^x + b on [0,1) with E = -1/3; the forgotten-x bug of ax / b). The worked example is new: a on [-1,0) and b x on
[0,2) with E[X] = 5/12 (a = 1/2, b = 1/4); its forgotten-x version gives a = 7/18, b = 11/36, whose mean is not 5/12.
Every integral and solution is computed with sympy and cross-checked numerically (w_pdf.Pdf / mpmath).
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo, nint

a, b, c, mu = sp.symbols("a b c mu", real=True)

# ---------------------------------------------------------------- example: a on [-1,0), b x on [0,2), E = 5/12
N1 = sp.integrate(a, (x, -1, 0)) + sp.integrate(b * x, (x, 0, 2))
M1 = sp.integrate(x * a, (x, -1, 0)) + sp.integrate(x * b * x, (x, 0, 2))
assert N1 == a + 2 * b and M1 == -a / 2 + R(8, 3) * b
S1 = sp.solve([N1 - 1, M1 - R(5, 12)], [a, b])
assert S1 == {a: R(1, 2), b: R(1, 4)}
assert sp.expand(M1.subs(a, 1 - 2 * b)) == -R(1, 2) + R(11, 3) * b      # after substituting a = 1 - 2b
E1 = Pdf([(-1, 0, R(1, 2)), (0, 2, x / 4)])
assert E1.total() == 1 and E1.mean() == R(5, 12) and E1.nonneg()
# the trap: x forgotten in the second piece
BAD = sp.solve([N1 - 1, -a / 2 + sp.integrate(b * x, (x, 0, 2)) - R(5, 12)], [a, b])
assert BAD == {a: R(7, 18), b: R(11, 36)}
assert Pdf([(-1, 0, BAD[a]), (0, 2, BAD[b] * x)]).mean() != R(5, 12)

# ---------------------------------------------------------------- exam 26A-A-Q4a
Q = BANK["26A-A-Q4a"]
assert "\\mu" in Q["question"]
assert sp.integrate(1, (x, 2, oo)) == oo                                 # c on [2, oo): diverges unless c = 0
I = {"e": sp.integrate(sp.exp(x), (x, -oo, 0)), "q": sp.integrate((1 - x)**2, (x, 0, 2)),
     "xe": sp.integrate(x * sp.exp(x), (x, -oo, 0)), "xq": sp.integrate(x * (1 - x)**2, (x, 0, 2))}
assert I == {"e": 1, "q": R(2, 3), "xe": -1, "xq": R(2, 3)}
SX = sp.solve([a + R(2, 3) * b - 1, -a + R(2, 3) * b - mu], [a, b])
assert sp.simplify(SX[a] - (1 - mu) / 2) == 0 and sp.simplify(SX[b] - R(3, 4) * (1 + mu)) == 0
assert sp.reduce_inequalities([SX[a] >= 0, SX[b] >= 0], mu).as_set() == sp.Interval(-1, 1)
for m in (R(-1, 2), 0, R(1, 3)):                                          # the solved density really has mean mu
    p = Pdf([(-oo, 0, SX[a].subs(mu, m) * sp.exp(x)), (0, 2, SX[b].subs(mu, m) * (1 - x)**2)])
    assert p.total() == 1 and p.mean() == m and p.nonneg()

# ---------------------------------------------------------------- figures
P1 = w.Plot("p1", (-1.4, 2.4), (0, 0.72), w=820, h=380, xticks=[(-1, "-1"), (1, "1"), (2, "2")],
            yticks=[(0.25, "1/4"), (0.5, "1/2")])
P1.area("p1-a1", lambda v: 0.5, -1, 0, kind="b")
P1.area("p1-a2", lambda v: v / 4, 0, 2, kind="a")
P1.seg("p1-f1", [(-1, 0.5), (0, 0.5)], kind="b", hidden=False)
P1.seg("p1-f2", [(0, 0), (2, 0.5)], kind="a", hidden=False)
P1.vline("p1-g1", -1, 0, 0.5, hidden=False)
P1.vline("p1-g2", 2, 0, 0.5, hidden=False)
P1.label("p1-l1", -0.5, 0.58, "a", kind="b", hidden=False)
P1.label("p1-l2", 1.25, 0.18, "b·x", kind="a", hidden=False)
P1.vline("p1-mu", 5 / 12, 0, 0.66)
P1.label("p1-lmu", 5 / 12 + 0.06, 0.62, "E[X] = 5/12", kind="ok", anchor="start")

P2 = w.Plot("p2", (-3.6, 2.5), (0, 0.95), w=820, h=380, xticks=[(-3, "-3"), (-2, "-2"), (-1, "-1"), (1, "1"), (2, "2")],
            yticks=[(0.5, "1/2"), (0.75, "3/4")])
P2.curve("p2-f1", lambda v: 0.5 * math.exp(v), -3.5, 0, kind="b")
P2.curve("p2-f2", lambda v: 0.75 * (1 - v)**2, 0, 2, kind="a")
P2.seg("p2-f3", [(2, 0), (2.4, 0)], kind="d")
P2.vline("p2-g", 2, 0, 0.75)
P2.label("p2-l1", -1.6, 0.28, "a·eˣ", kind="b")
P2.label("p2-l2", 1.0, 0.42, "b·(1−x)²", kind="a")
P2.label("p2-l3", 2.2, 0.1, "c", kind="d")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה יש בצפיפות **שני** קבועים לא ידועים."),
    P("משוואת הנרמול לבדה לא מספיקה, ולכן נשתמש גם בתוחלת."),
    P("ובסוף נפתור סעיף ממבחן שבו התוחלת נתונה כאות, $\\mu$.", hold=0.4,
      say="ובסוף נפתור סעיף ממבחן שבו התוחלת נתונה כאות, מְיוּ."),
], stage='<div class="kicker">F04 · משתנה רציף</div><h1>שני קבועים: נרמול ותוחלת</h1>'
         '<p>למצוא שני קבועים, גם כשהתוחלת נתונה כסימן μ, מהנרמול ומהמשוואה השנייה שנותנת את התוחלת.</p>',
   layout="title")

two = Scene("two", "שתי משוואות", [
    P("הנה צפיפות: הקבוע $a$ ממינוס אחת עד אפס, ואז $b$ כפול $x$ מאפס עד שתיים.", do=show("t-f"),
      say="הנה צפיפות: הקבוע אֵיי ממינוס אחת עד אפס, ואז בִּי כפול אִקְס מאפס עד שתיים."),
    P("ונתון שהתוחלת היא חמש חלקי שתים עשרה. שני נעלמים, ולכן צריך שתי משוואות."),
    P("הראשונה, הנרמול: מלבן בשטח $a$, ומשולש בשטח שתיים $b$. הסכום הוא אחת.", do=show("t-0", "p1-a1", "p1-a2"),
      say="הראשונה, הנרמול: מלבן בשטח אֵיי, ומשולש בשטח שתיים בִּי. הסכום הוא אחת."),
    P("השנייה, התוחלת: אותו דבר, אבל **מכפילים ב-$x$** לפני שמאנטגרלים.", do=show("t-r"),
      say="השנייה, התוחלת: אותו דבר, אבל מכפילים באִקְס לפני שמאנטגרלים."),
    P("בקטע הראשון: $x$ כפול $a$, ממינוס אחת עד אפס. זה מינוס $a$ חצאים, כי שם $x$ שלילי.", do=show("t-1"),
      say="בקטע הראשון: אִקְס כפול אֵיי, ממינוס אחת עד אפס. זה מינוס אֵיי חצאים, כי שם אִקְס שלילי."),
    P("בקטע השני: $x$ כפול $b x$, כלומר $b x^2$. מאפס עד שתיים זה שמונה $b$ שלישים.", do=show("t-2"),
      say="בקטע השני: אִקְס כפול בִּי אִקְס, כלומר בִּי אִקְס בריבוע. מאפס עד שתיים זה שמונה בִּי שלישים."),
    P("פותרים בהצבה: מהנרמול, $a$ שווה אחת פחות שתיים $b$.", do=show("t-3"),
      say="פותרים בהצבה: מהנרמול, אֵיי שווה אחת פחות שתיים בִּי."),
    P("מציבים בתוחלת: מינוס חצי, ועוד אחת עשרה $b$ שלישים, שווה חמש חלקי שתים עשרה.", do=show("t-4"),
      say="מציבים בתוחלת: מינוס חצי, ועוד אחת עשרה בִּי שלישים, שווה חמש חלקי שתים עשרה."),
    P("לכן $b$ הוא רבע, ו-$a$ הוא חצי.", do=show("t-ok"),
      say="לכן בִּי הוא רבע, ואֵיי הוא חצי."),
    P("ובדיקה: שני הקבועים חיוביים, והתוחלת נופלת בתוך התחום, קצת מימין לאפס.", do=show("p1-mu", "p1-lmu"), hold=0.4),
], stage=f'<div class="pd-col">{P1.svg()}'
         + w.chip("t-f", "$f=a$ על $[-1,0)$, $\\ f=b\\,x$ על $[0,2)$, $\\ E[X]=\\tfrac5{12}$", "warn") + "</div>",
   panel=w.eqs("t", ["$a+2b=1$", "$\\displaystyle\\int_{-1}^0 x\\,a\\,dx=-\\tfrac a2$",
                     "$\\displaystyle\\int_0^2 x\\cdot b\\,x\\,dx=\\tfrac{8b}{3}$", "$a=1-2b$",
                     "$-\\tfrac12+\\tfrac{11b}{3}=\\tfrac5{12}$"], size=36, gap=6)
         + st.card("t-r", "rule", "🔑 $E[X]=\\displaystyle\\int x\\,f(x)\\,dx$")
         + w.chip("t-ok", "$b=\\tfrac14,\\ \\ a=\\tfrac12$"))

trap = Scene("trap", "המלכודת", [
    P("והטעות הנפוצה: לשכוח את ה-$x$ באחד הקטעים.", do=show("k-0"),
      say="והטעות הנפוצה: לשכוח את האִקְס באחד הקטעים."),
    P("מי שכותב בקטע השני את האינטגרל של $b x$ בלבד, מקבל שתיים $b$: חלק מהנרמול, לא מהתוחלת.", do=show("k-1"),
      say="מי שכותב בקטע השני את האינטגרל של בִּי אִקְס בלבד, מקבל שתיים בִּי: חלק מהנרמול, לא מהתוחלת."),
    P("המערכת עדיין נפתרת, אבל לקבועים שגויים: שבע חלקי שמונה עשרה, ואחת עשרה חלקי שלושים ושש.", do=show("k-2")),
    P("ובדיקה פשוטה חושפת אותם: התוחלת של הצפיפות שיצאה איננה חמש חלקי שתים עשרה.", do=show("k-3")),
    P("הכלל: בתוחלת, **בכל** קטע, הצפיפות מוכפלת ב-$x$.", do=show("k-r"), hold=0.4,
      say="הכלל: בתוחלת, בכל קטע, הצפיפות מוכפלת באִקְס."),
], stage='<div class="pd-col">'
         + w.eqs("k", ["<span dir=\"rtl\">שגוי: $\\displaystyle\\int_0^2 b\\,x\\,dx=2b$ ✗</span>",
                       "$-\\tfrac a2+2b=\\tfrac5{12}$", "$a=\\tfrac7{18},\\ \\ b=\\tfrac{11}{36}$",
                       "<span dir=\"rtl\">התוחלת שלה $\\ne\\tfrac5{12}$</span>"], size=40, gap=16)
         + "</div>",
   panel=st.card("k-0", "trap", "⚠️ שוכחים את ה-$x$ בקטע השני")
         + st.card("k-r", "rule", "🔑 בכל קטע: $\\int x\\cdot f$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: $a$ כפול $e^x$ לפני אפס, $b$ כפול אחת פחות $x$ בריבוע עד שתיים, והקבוע $c$ משתיים והלאה.",
      do=show("p2-f1", "p2-f2", "p2-f3", "p2-g", "p2-l1", "p2-l2", "p2-l3", "p2-cap"),
      say="שאלה ממבחן: אֵיי כפול אִי בחזקת אִקְס לפני אפס, בִּי כפול אחת פחות אִקְס, בסוגריים, בריבוע, עד שתיים, והקבוע סִי משתיים והלאה."),
    P("התוחלת היא $\\mu$. מבקשים את שלושת הקבועים.",
      say="התוחלת היא מְיוּ. מבקשים את שלושת הקבועים."),
    P("קודם $c$: קבוע על קרן אינסופית נותן שטח אינסופי. לכן $c$ חייב להיות אפס.", do=show("x-0"),
      say="קודם סִי: קבוע על קרן אינסופית נותן שטח אינסופי. לכן סִי חייב להיות אפס."),
    P("הנרמול: האינטגרל של $e^x$ עד אפס הוא אחת, ושל אחת פחות $x$ בריבוע הוא שני שלישים.", do=show("x-1"),
      say="הנרמול: האינטגרל של אִי בחזקת אִקְס עד אפס הוא אחת, ושל אחת פחות אִקְס, בסוגריים, בריבוע, הוא שני שלישים."),
    P("אז $a$ ועוד שני שלישים $b$ שווה אחת.", do=show("x-2"),
      say="אז אֵיי ועוד שני שלישים בִּי שווה אחת."),
    P("התוחלת: האינטגרל של $x e^x$ עד אפס הוא **מינוס** אחת. השטח שם בצד השלילי.", do=show("x-3", "x-t"),
      say="התוחלת: האינטגרל של אִקְס, אִי בחזקת אִקְס, עד אפס, הוא מינוס אחת. השטח שם בצד השלילי."),
    P("ובקטע השני יוצא שוב שני שלישים. לכן מינוס $a$ ועוד שני שלישים $b$ שווה $\\mu$.", do=show("x-4"),
      say="ובקטע השני יוצא שוב שני שלישים. לכן מינוס אֵיי ועוד שני שלישים בִּי שווה מְיוּ."),
    P("מחסרים את המשוואות: שתיים $a$ שווה אחת פחות $\\mu$.", do=show("x-5"),
      say="מחסרים את המשוואות: שתיים אֵיי שווה אחת פחות מְיוּ."),
    P("ומחברים אותן: ארבעה שלישים $b$ שווה אחת ועוד $\\mu$.", do=show("x-6"),
      say="ומחברים אותן: ארבעה שלישים בִּי שווה אחת ועוד מְיוּ."),
    P("התשובה: $a$ הוא אחת פחות $\\mu$ חלקי שתיים, $b$ הוא שלושה רבעים כפול אחת ועוד $\\mu$, ו-$c$ אפס.",
      do=show("x-ok"), hold=0.3,
      say="התשובה: אֵיי הוא אחת פחות מְיוּ, חלקי שתיים. בִּי הוא שלושה רבעים, כפול אחת ועוד מְיוּ. וסִי אפס."),
    P("הקבועים יוצאים כביטויים ב-$\\mu$, וזה בסדר. בשרטוט רואים את המקרה $\\mu$ שווה אפס.",
      say="הקבועים יוצאים כביטויים במְיוּ, וזה בסדר. בשרטוט רואים את המקרה מְיוּ שווה אפס."),
    P("ובדיקה אחרונה: צפיפות לא שלילית, ולכן $a$ ו-$b$ אי-שליליים. זה קורה רק כש-$\\mu$ בין מינוס אחת לאחת.",
      do=show("x-m"), hold=0.6,
      say="ובדיקה אחרונה: צפיפות לא שלילית, ולכן אֵיי ובִּי אִי שליליים. זה קורה רק כשמְיוּ בין מינוס אחת לאחת."),
], stage=f'<div class="pd-col">{P2.svg()}<div id="p2-cap" class="pd-note h">בשרטוט, לדוגמה: $\\mu=0$</div>'
         + st.card("x-t", "trap", "⚠️ $\\int_{-\\infty}^0 x\\,e^x\\,dx=-1$, לא $+1$")
         + w.chip("x-ok", "$a=\\tfrac{1-\\mu}{2},\\ \\ b=\\tfrac34(1+\\mu),\\ \\ c=0$") + "</div>",
   panel=w.stem(Q["id"], "$f_X=a\\,e^x$ ל-$x<0$, $\\ b(1-x)^2$ ל-$0\\le x<2$, $\\ c$ ל-$x\\ge2$. נתון $E[X]=\\mu$. מצאו $a,b,c$.")
         + w.eqs("x", ["$c=0$", "$\\displaystyle\\int_{-\\infty}^0 e^x=1,\\ \\ \\int_0^2(1-x)^2=\\tfrac23$",
                       "$a+\\tfrac23 b=1$", "$\\displaystyle\\int_{-\\infty}^0 x\\,e^x=-1,\\ \\ \\int_0^2 x(1-x)^2=\\tfrac23$",
                       "$-a+\\tfrac23 b=\\mu$", "$2a=1-\\mu$", "$\\tfrac43 b=1+\\mu$"], size=30, gap=2)
         + w.chip("x-m", "$a,b\\ge0\\iff -1\\le\\mu\\le1$", "warn"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: שני קבועים צריכים שתי משוואות. הראשונה היא הנרמול.", do=show("r-1")),
    P("השנייה היא התוחלת: אינטגרל של $x$ כפול הצפיפות, בכל קטע.", do=show("r-2"),
      say="השנייה היא התוחלת: אינטגרל של אִקְס כפול הצפיפות, בכל קטע."),
    P("שתיהן ליניאריות בקבועים, ולכן פותרים בהצבה, או בחיבור וחיסור.", do=show("r-3")),
    P("ובצד השלילי, התרומה לתוחלת שלילית. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="pd-col"><div class="pd-big">$\\displaystyle\\int f=1,\\qquad \\int x\\,f=E[X]$</div></div>',
   panel=st.card("r-1", "rule", "🔑 נרמול: $\\int f=1$")
         + st.card("r-2", "rule", "🔑 תוחלת: $\\int x\\,f=E[X]$")
         + st.card("r-3", "ex", "מערכת $2\\times2$ ליניארית")
         + st.card("r-4", "trap", "⚠️ $\\int_{-\\infty}^0 x\\,e^x\\,dx=-1$"))

VIDEO = Video("F04", "pdf", "שני קבועים: נרמול ותוחלת", w.fix_scenes([title, two, trap, exam, recap]),
              bank={"26A-A-Q4a": None})
