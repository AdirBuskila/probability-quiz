# -*- coding: utf-8 -*-
"""F09 · מבחן גמר: שאלה 4 אמיתית — boss walkthrough (build: tools/video/vid.py F09).

Source: courses/pdf/C09.js (boss level: real question-4 parts; constants from normalization and the mean, the
conditional from F).
Exam anchors, one full question 4 that no guided quiz or boss uses: 25B-A-Q4a (a, b, c, g with E[X] = mu and a FINITE
variance: g = 0 from normalization, c/x^3 survives normalization and the mean but its x^2 moment diverges, so c = 0;
then a = 6(1-2mu)/5, b = 2(1+3mu)/5), 25B-A-Q4b (-1/3 <= mu <= 1/2 from a, b >= 0), 25B-A-Q4d
(P(X<1 | X>-1/2) = 1 because F(1) = 1).
Not used on purpose: the C09 boss items 24A-B-Q4a, 24S-A-Q4a, 25A-A-Q3a, 24A-C-Q4c, 24B-A-Q4c and every level quiz
of the course; 25B-A-Q4c (the F of this question) is only used through F(1) = 1 and F(-1/2) = a/8.
Every integral, constant, range and probability is computed with sympy and cross-checked numerically (w_pdf.Pdf).
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo, nint

a, b, c, g, mu = sp.symbols("a b c g mu", real=True)

# ---------------------------------------------------------------- 25B-A-Q4a
QA, QB, QD = BANK["25B-A-Q4a"], BANK["25B-A-Q4b"], BANK["25B-A-Q4d"]
assert "-1/2" in QD["question"]
assert sp.integrate(1, (x, 1, oo)) == oo                                   # g on [1, oo): g = 0
assert sp.integrate(x**-3, (x, 1, oo)) == R(1, 2)                           # c/x^3: normalization converges
assert sp.integrate(x * x**-3, (x, 1, oo)) == 1                             # ... and so does the mean
assert sp.integrate(x**2 * x**-3, (x, 1, oo)) == oo                         # ... but E[X^2] diverges: c = 0
assert abs(nint(x**-3, 1, oo) - 0.5) < 1e-9 and abs(nint(x**-2, 1, oo) - 1) < 1e-9
N = sp.integrate(a * (x + 1), (x, -1, 0)) + sp.integrate(b, (x, 0, 1))
M = sp.integrate(x * a * (x + 1), (x, -1, 0)) + sp.integrate(x * b, (x, 0, 1))
assert N == a / 2 + b and M == -a / 6 + b / 2
assert sp.integrate(x * (x + 1), (x, -1, 0)) == -R(1, 6)
S = sp.solve([N - 1, M - mu], [a, b])
A, B = S[a], S[b]
assert sp.simplify(A - R(6, 5) * (1 - 2 * mu)) == 0 and sp.simplify(B - R(2, 5) * (1 + 3 * mu)) == 0
assert sp.solve(N.subs(b, 1 - a / 2) - 1, a) == []                          # substitution check: N is an identity then
assert sp.simplify(M.subs(b, 1 - a / 2) - (R(1, 2) - R(5, 12) * a)) == 0

# ---------------------------------------------------------------- 25B-A-Q4b
assert sp.reduce_inequalities([A >= 0, B >= 0], mu).as_set() == sp.Interval(-R(1, 3), R(1, 2))
assert A.subs(mu, R(1, 2)) == 0 and B.subs(mu, R(1, 2)) == 1                # mu = 1/2: uniform on [0,1]
assert A.subs(mu, -R(1, 3)) == 2 and B.subs(mu, -R(1, 3)) == 0              # mu = -1/3: the triangle on [-1,0]
FAM = {}
for m in (-R(1, 3), sp.Integer(0), R(1, 2)):
    p = Pdf([(-1, 0, A.subs(mu, m) * (x + 1)), (0, 1, B.subs(mu, m))])
    assert p.total() == 1 and p.mean() == m and p.nonneg()
    assert p.moment(2) < oo                                                  # finite variance indeed
    FAM[m] = p

# ---------------------------------------------------------------- 25B-A-Q4d
for m, p in FAM.items():
    assert p.F(1) == 1
    assert p.F(-R(1, 2)) == A.subs(mu, m) / 8
    den = 1 - p.F(-R(1, 2))
    assert den > 0 and (p.F(1) - p.F(-R(1, 2))) / den == 1
assert sp.simplify((A / 2 * (t + 1)**2).subs(t, -R(1, 2)) - A / 8) == 0

# ---------------------------------------------------------------- figures
PA = w.Plot("pa", (-1.5, 3.4), (0, 1.25), w=820, h=380, xticks=[(-1, "-1"), (1, "1"), (2, "2"), (3, "3")],
            yticks=[(0.6, "a"), (1, "b")], pad=(56, 60, 40, 50))
PA.seg("pa-1", [(-1.45, 0), (-1, 0), (0, 0.6)], kind="b", hidden=False)
PA.seg("pa-2", [(0, 1), (1, 1)], kind="a", hidden=False)
PA.curve("pa-3", lambda v: 0.5 / v**3 + 0.15, 1, 3.3, kind="d", hidden=False)
PA.label("pa-l1", -0.75, 0.42, "a(x+1)", kind="b", hidden=False)
PA.label("pa-l2", 0.5, 1.08, "b", kind="a", hidden=False)
PA.label("pa-l3", 2.1, 0.36, "c/x³ + g", kind="d", hidden=False)
PA.seg("pa-x3", [(1, 0.02), (3.3, 0.02)], kind="bad")
PA.label("pa-lx", 2.15, 0.08, "c = g = 0", kind="bad")

PB = w.Plot("pb", (-1.4, 1.5), (0, 2.25), w=800, h=400, xticks=[(-1, "-1"), (1, "1")],
            yticks=[(0.4, "2/5"), (1, "1"), (1.2, "6/5"), (2, "2")])
PB.seg("pb-m", [(-1.35, 0), (-1, 0), (0, 2), (0, 0), (1.45, 0)], kind="b")
PB.seg("pb-0", [(-1, 0), (0, 1.2), (0, 0.4), (1, 0.4), (1, 0)], kind="a")
PB.seg("pb-p", [(-1, 0), (0, 0), (0, 1), (1, 1), (1, 0)], kind="d")
PB.label("pb-lm", -0.62, 1.55, "μ = −1/3", kind="b")
PB.label("pb-l0", 0.5, 0.5, "μ = 0", kind="a")
PB.label("pb-lp", 0.5, 1.1, "μ = 1/2", kind="d")

def fd(v):
    a0, b0 = 1.2, 0.4                                            # the mu = 0 member, for the picture
    return a0 * (v + 1) if -1 <= v < 0 else (b0 if 0 <= v < 1 else 0.0)


PD = w.Plot("pd", (-1.4, 1.6), (0, 1.4), w=800, h=380, xticks=[(-1, "-1"), (-0.5, "-½"), (1, "1")],
            yticks=[(0.4, "b"), (1.2, "a")])
PD.area("pd-cond", fd, -0.5, 1, kind="ink")
PD.area("pd-int", fd, -0.5, 1, kind="a")
PD.seg("pd-f", [(-1.35, 0), (-1, 0), (0, 1.2), (0, 0.4), (1, 0.4), (1, 0), (1.55, 0)], kind="b", hidden=False)
PD.vline("pd-v1", 1, 0, 1.3)
PD.label("pd-l1", 1.05, 1.15, "X < 1 ✓", kind="ok", anchor="start")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הגמר של הקורס: שאלה ארבע אמיתית ממבחן, סעיף אחרי סעיף."),
    P("נמצא ארבעה קבועים, את התחום של התוחלת, והסתברות מותנית."),
    P("והכלים הם בדיוק אלה שלמדנו בכל הרמות.", hold=0.4),
], stage='<div class="kicker">F09 · מבחן גמר</div><h1>מבחן גמר: שאלה 4 אמיתית</h1>'
         '<p>לפתור חלקים של שאלה 4 אמיתית מהמבחנים: קבועים מנרמול ותוחלת, ומותנית מתוך F.</p>', layout="title")

plan = Scene("plan", "המתכון", [
    P("לפני שמתחילים, המתכון. קוראים את הצורה, קטע אחרי קטע.", do=show("p-1")),
    P("נרמול: השטח הכולל אחת. ואם אינטגרל מתבדר, הקבוע שלפניו אפס.", do=show("p-2")),
    P("תוחלת: אינטגרל של $x$ כפול הצפיפות נותן משוואה שנייה.", do=show("p-3"),
      say="תוחלת: אינטגרל של אִקְס כפול הצפיפות נותן משוואה שנייה."),
    P("ובסוף, הסתברות מותנית מתוך $F$: החיתוך, חלקי התנאי.", do=show("p-4"), hold=0.4,
      say="ובסוף, הסתברות מותנית מתוך אֶף: החיתוך, חלקי התנאי."),
], stage='<div class="pd-col">'
         + st.card("p-1", "ex", "1. קוראים את הצורה, קטע אחרי קטע")
         + st.card("p-2", "ex", "2. נרמול $\\int f=1$; מתבדר ⇐ קבוע $0$")
         + st.card("p-3", "ex", "3. תוחלת $\\int x\\,f=\\mu$")
         + st.card("p-4", "ex", "4. מותנית: חיתוך חלקי תנאי") + "</div>",
   layout="full")

partA = Scene("a", "סעיף א", [
    P("השאלה: אפס לפני מינוס אחת, $a(x+1)$ עד אפס, הקבוע $b$ עד אחת, ומאחת: $c$ חלקי $x^3$, ועוד $g$.",
      say="השאלה: אפס לפני מינוס אחת, אֵיי כפול, בסוגריים, אִקְס ועוד אחת, עד אפס, הקבוע בִּי עד אחת, ומאחת: סִי חלקי אִקְס בשלישית, ועוד גִ'י."),
    P("נתון שהתוחלת $\\mu$, ושהשונות **סופית**. מבקשים את ארבעת הקבועים.",
      say="נתון שהתוחלת מְיוּ, ושהשונות סופית. מבקשים את ארבעת הקבועים."),
    P("מתחילים מהזנב. $g$ הוא קבוע על קרן אינסופית: השטח אינסופי, ולכן $g$ שווה אפס.", do=show("a-0"),
      say="מתחילים מהזנב. גִ'י הוא קבוע על קרן אינסופית: השטח אינסופי, ולכן גִ'י שווה אפס."),
    P("ועכשיו $c$ חלקי $x^3$. וזו המלכודת: הנרמול **לא** פוסל אותו. האינטגרל מאחת עד אינסוף הוא $c$ חצאים.",
      do=show("a-1", "a-t"),
      say="ועכשיו סִי חלקי אִקְס בשלישית. וזו המלכודת: הנרמול לא פוסל אותו. האינטגרל מאחת עד אינסוף הוא סִי חצאים."),
    P("גם התוחלת סופית: $x$ כפול $c$ חלקי $x^3$ זה $c$ חלקי $x^2$, ומתכנס.", do=show("a-2"),
      say="גם התוחלת סופית: אִקְס כפול סִי חלקי אִקְס בשלישית, זה סִי חלקי אִקְס בריבוע, ומתכנס."),
    P("אבל השונות צריכה את $x^2$ כפול הצפיפות. נשאר $c$ חלקי $x$, וזה מתבדר. לכן $c$ שווה אפס.", do=show("a-3", "pa-x3", "pa-lx"),
      say="אבל השונות צריכה את אִקְס בריבוע כפול הצפיפות. נשאר סִי חלקי אִקְס, וזה מתבדר. לכן סִי שווה אפס."),
    P("נשארו $a$ ו-$b$. נרמול: משולש בשטח $a$ חצאים, ומלבן בשטח $b$.", do=show("a-4"),
      say="נשארו אֵיי ובִּי. נרמול: משולש בשטח אֵיי חצאים, ומלבן בשטח בִּי."),
    P("תוחלת: האינטגרל של $x(x+1)$, ממינוס אחת עד אפס, הוא מינוס שישית. ומהמלבן $b$ חצאים.", do=show("a-5"),
      say="תוחלת: האינטגרל של אִקְס כפול, בסוגריים, אִקְס ועוד אחת, ממינוס אחת עד אפס, הוא מינוס שישית. ומהמלבן בִּי חצאים."),
    P("מציבים $b$ שווה אחת פחות $a$ חצאים, ופותרים.", do=show("a-6"),
      say="מציבים בִּי שווה אחת פחות אֵיי חצאים, ופותרים."),
    P("$a$ הוא שש חמישיות כפול אחת פחות שתיים $\\mu$, ו-$b$ שתי חמישיות כפול אחת ועוד שלוש $\\mu$.", do=show("a-ok"),
      hold=0.5,
      say="אֵיי הוא שש חמישיות, כפול אחת פחות שתיים מְיוּ. ובִּי, שתי חמישיות, כפול אחת ועוד שלוש מְיוּ."),
], stage=f'<div class="pd-col">{PA.svg()}'
         + st.card("a-t", "trap", "⚠️ $\\frac{c}{x^3}$ עובר נרמול ותוחלת; רק השונות פוסלת אותו")
         + w.chip("a-ok", "$a=\\tfrac65(1-2\\mu),\\ \\ b=\\tfrac25(1+3\\mu),\\ \\ c=g=0$") + "</div>",
   panel=w.stem(QA["id"], "$a(x+1)$ על $[-1,0)$, $\\ b$ על $[0,1)$, $\\ \\tfrac{c}{x^3}+g$ ל-$x\\ge1$; $E[X]=\\mu$, שונות סופית.")
         + w.eqs("a", ["$\\int_1^\\infty g\\,dx=\\infty\\ \\Rightarrow\\ g=0$", "$\\int_1^\\infty \\tfrac{c}{x^3}=\\tfrac c2$",
                       "$\\int_1^\\infty x\\cdot\\tfrac{c}{x^3}=c$", "$\\int_1^\\infty x^2\\cdot\\tfrac{c}{x^3}=\\infty\\ \\Rightarrow\\ c=0$",
                       "$\\tfrac a2+b=1$", "$-\\tfrac a6+\\tfrac b2=\\mu$", "$\\tfrac12-\\tfrac{5a}{12}=\\mu$"],
                 size=30, gap=2))

partB = Scene("b", "סעיף ב", [
    P("סעיף ב: מה הערך הקטן והגדול ביותר של $\\mu$? מנמקים.",
      say="סעיף ב: מה הערך הקטן והגדול ביותר של מְיוּ? מנמקים."),
    P("הצפיפות חייבת להיות אי-שלילית, ולכן גם $a$ וגם $b$ אי-שליליים.", do=show("b-0"),
      say="הצפיפות חייבת להיות אִי שלילית, ולכן גם אֵיי וגם בִּי אִי שליליים."),
    P("$a$ אי-שלילי כש-$\\mu$ קטן או שווה לחצי.", do=show("b-1"),
      say="אֵיי אִי שלילי כשמְיוּ קטן או שווה לחצי."),
    P("ו-$b$ אי-שלילי כש-$\\mu$ גדול או שווה למינוס שליש. המלכודת: לבדוק רק אחד מהם.", do=show("b-2", "b-t"),
      say="ובִּי אִי שלילי כשמְיוּ גדול או שווה למינוס שליש. המלכודת: לבדוק רק אחד מהם."),
    P("והקצוות מסתדרים. ב-$\\mu$ שווה חצי, $a$ אפס, ונשאר מלבן מאפס עד אחת. התוחלת שלו באמת חצי.",
      do=show("pb-p", "pb-lp"),
      say="והקצוות מסתדרים. במְיוּ שווה חצי, אֵיי אפס, ונשאר מלבן מאפס עד אחת. התוחלת שלו באמת חצי."),
    P("ב-$\\mu$ מינוס שליש, $b$ אפס, ונשאר משולש שקודקודו באפס. התוחלת שלו מינוס שליש.", do=show("pb-m", "pb-lm"),
      say="במְיוּ מינוס שליש, בִּי אפס, ונשאר משולש שקודקודו באפס. התוחלת שלו מינוס שליש."),
    P("ובאמצע, למשל $\\mu$ שווה אפס, יש גם משולש וגם מלבן.", do=show("pb-0", "pb-l0", "b-ok"), hold=0.5,
      say="ובאמצע, למשל מְיוּ שווה אפס, יש גם משולש וגם מלבן."),
], stage=f'<div class="pd-col">{PB.svg()}'
         + st.card("b-t", "trap", "⚠️ בודקים גם את $a$ וגם את $b$") + "</div>",
   panel=w.stem(QB["id"], "מהו הערך הקטן והגדול ביותר של התוחלת $\\mu$? נמקו.")
         + w.eqs("b", ["$a\\ge0,\\ \\ b\\ge0$", "$1-2\\mu\\ge0\\ \\Rightarrow\\ \\mu\\le\\tfrac12$",
                       "$1+3\\mu\\ge0\\ \\Rightarrow\\ \\mu\\ge-\\tfrac13$"], size=34, gap=8)
         + w.chip("b-ok", "$-\\tfrac13\\le\\mu\\le\\tfrac12$"))

partD = Scene("d", "סעיף ד", [
    P("סעיף ד: ההסתברות ש-$X$ קטן מאחת, בהינתן ש-$X$ גדול ממינוס חצי.",
      say="סעיף ד: ההסתברות שאִקְס קטן מאחת, בהינתן שאִקְס גדול ממינוס חצי."),
    P("המכנה: אחת פחות $F$ במינוס חצי. המונה: $F$ באחת, פחות $F$ במינוס חצי.", do=show("d-0", "pd-cond"),
      say="המכנה: אחת פחות אֶף במינוס חצי. המונה: אֶף באחת, פחות אֶף במינוס חצי."),
    P("עכשיו הרגע שחוסך את כל החישוב: מסעיף א, $c$ ו-$g$ אפס. אחרי אחת אין שום צפיפות.", do=show("pd-v1", "pd-l1"),
      say="עכשיו הרגע שחוסך את כל החישוב: מסעיף א, סִי וגִ'י אפס. אחרי אחת אין שום צפיפות."),
    P("לכן ההסתברות ש-$X$ גדול או שווה לאחת היא אפס, ו-$F$ באחת היא אחת.", do=show("d-1", "pd-int"),
      say="לכן ההסתברות שאִקְס גדול או שווה לאחת היא אפס, ואֶף באחת היא אחת."),
    P("כלומר החיתוך שווה לתנאי בהסתברות: המונה שווה בדיוק למכנה.", do=show("d-r")),
    P("התשובה אחת, לכל $\\mu$ בתחום. המכנה לא אפס, כי $F$ במינוס חצי היא רק $a$ חלקי שמונה.", do=show("d-2", "d-ok"),
      hold=0.5,
      say="התשובה אחת, לכל מְיוּ בתחום. המכנה לא אפס, כי אֶף במינוס חצי היא רק אֵיי חלקי שמונה."),
    P("והמלכודת: להחליף בין $F$ באחת ל-$F$ במינוס חצי. בודקים: האם התשובה הגיונית?", do=show("d-t"), hold=0.5,
      say="והמלכודת: להחליף בין אֶף באחת לאֶף במינוס חצי. בודקים: האם התשובה הגיונית?"),
], stage=f'<div class="pd-col">{PD.svg()}<div class="pd-note">בשרטוט: $\\mu=0$</div>'
         + st.card("d-t", "trap", "⚠️ לא להחליף בין $F(1)$ ל-$F(-\\tfrac12)$") + "</div>",
   panel=w.stem(QD["id"], "מהי ההסתברות המותנית $P(X<1\\,/\\,X>-1/2)$?")
         + w.eqs("d", ["$\\dfrac{F(1)-F(-\\frac12)}{1-F(-\\frac12)}$", "$F(1)=1$", "$F(-\\tfrac12)=\\tfrac a8<1$"],
                 size=34, gap=8)
         + st.card("d-r", "rule", "🔑 $P(X\\ge1)=0$ ⇐ התשובה $1$")
         + w.chip("d-ok", "$P=1$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום השאלה: זנב אינסופי עם קבוע נותן אפס כבר בנרמול.", do=show("r-1")),
    P("ושונות סופית דורשת עוד: גם $x^2$ כפול הצפיפות חייב להתכנס.", do=show("r-2"),
      say="ושונות סופית דורשת עוד: גם אִקְס בריבוע כפול הצפיפות חייב להתכנס."),
    P("התחום של $\\mu$ בא מאי-שליליות של כל הקבועים.", do=show("r-3"),
      say="התחום של מְיוּ בא מאִי שליליות של כל הקבועים."),
    P("ובמותנית, לפני שמחשבים, בודקים איפה יש צפיפות. אם מחוץ לאירוע אין צפיפות, התשובה אחת. בהצלחה במבחן!",
      do=show("r-4"), hold=0.6),
], stage='<div class="pd-col"><div class="pd-big">$\\int f=1,\\quad \\int x\\,f=\\mu,\\quad \\int x^2 f<\\infty$</div></div>',
   panel=st.card("r-1", "rule", "🔑 קבוע על קרן אינסופית ⇐ $0$")
         + st.card("r-2", "rule", "🔑 שונות סופית: $\\int x^2 f<\\infty$")
         + st.card("r-3", "ex", "$a,b\\ge0$ ⇐ התחום של $\\mu$")
         + st.card("r-4", "trap", "⚠️ $P(X\\ge1)=0$ ⇐ התשובה $1$"))

VIDEO = Video("F09", "pdf", "מבחן גמר: שאלה 4 אמיתית", w.fix_scenes([title, plan, partA, partB, partD, recap]),
              bank={"25B-A-Q4a": None, "25B-A-Q4b": None, "25B-A-Q4d": None})
