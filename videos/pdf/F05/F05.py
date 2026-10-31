# -*- coding: utf-8 -*-
"""F05 · התפלגות מצטברת קטע אחר קטע — video script (build: tools/video/vid.py F05).

Source: courses/pdf/C05.js (lesson + goal: build F piece by piece from a piecewise density, check continuity at the
joints, recognize the right graph).
Exam anchor: 25A-C-Q3b (F for f = (3/2)(1+x) on [-1,0) and (1/4)e^{-x} for x >= 0, the constants of part a:
F = (3/4)(1+t)^2, then 1 - e^{-t}/4). No guided quiz uses it; part a's a = 3/2, b = 1/4 is quoted as given.
Not used on purpose: every C05 quiz item (x on [0,1) + 1/2 on [1,2): F(1), F(3/2), the branch t/2, the graph;
2/3 + 1/3: F(3/2); F = t^3 -> f(1/2)). The worked example is new: f = 1/2 on [-1,0) and 1 - x on [0,1)
(F = (t+1)/2, then 1/2 + t - t^2/2); its forgotten-accumulation version t - t^2/2 drops to 0 at t = 0 and ends at 1/2.
Every F piece, joint value and limit is computed with sympy (w_pdf.Pdf.Fpiece), numerically cross-checked.
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo

# ---------------------------------------------------------------- example: 1/2 on [-1,0), 1-x on [0,1)
E = Pdf([(-1, 0, R(1, 2)), (0, 1, 1 - x)])
assert E.total() == 1 and E.nonneg()
F0, F1 = E.Fpiece(0), E.Fpiece(1)
assert sp.expand(F0 - (t + 1) / 2) == 0
assert sp.expand(F1 - (R(1, 2) + t - t**2 / 2)) == 0
assert F0.subs(t, -1) == 0 and F0.subs(t, 0) == R(1, 2) == F1.subs(t, 0) and F1.subs(t, 1) == 1
assert sp.integrate(1 - x, (x, 0, t)) == t - t**2 / 2
assert sp.solve(sp.diff(F1, t), t) == [1]                                   # F increases on [0,1)
BAD = t - t**2 / 2                                                           # the forgotten F(0) = 1/2
assert BAD.subs(t, 0) == 0 and BAD.subs(t, 1) == R(1, 2)
assert E.F(R(1, 2)) == R(7, 8)
assert sp.diff(F0, t) == R(1, 2) and sp.expand(sp.diff(F1, t)) == 1 - t      # F' = f on both pieces
assert sp.diff((t + 1) / 2, t).subs(t, 0) != (1 - x).subs(x, 0)           # the straight-line candidate has the wrong slope at 0+

# ---------------------------------------------------------------- exam 25A-C-Q3b
Q = BANK["25A-C-Q3b"]
assert "F_X(t)" in Q["question"]
a_, b_ = sp.symbols("a b", real=True)
SA = sp.solve([sp.integrate(a_ * (1 + x), (x, -1, 0)) + sp.integrate(b_ * sp.exp(-x), (x, 0, oo)) - 1,
               sp.integrate(x * a_ * (1 + x), (x, -1, 0)) + sp.integrate(x * b_ * sp.exp(-x), (x, 0, oo))], [a_, b_])
assert SA == {a_: R(3, 2), b_: R(1, 4)}                                       # part a, E[X] = 0
X = Pdf([(-1, 0, R(3, 2) * (1 + x)), (0, oo, sp.exp(-x) / 4)])
assert X.total() == 1 and X.mean() == 0
G0, G1 = X.Fpiece(0), X.Fpiece(1)
assert sp.expand(G0 - R(3, 4) * (1 + t)**2) == 0
assert sp.simplify(G1 - (1 - sp.exp(-t) / 4)) == 0
assert G0.subs(t, 0) == R(3, 4) == G1.subs(t, 0) and sp.limit(G1, t, oo) == 1 and G0.subs(t, -1) == 0
assert sp.simplify(sp.integrate(sp.exp(-x) / 4, (x, 0, t)) - (1 - sp.exp(-t)) / 4) == 0

# ---------------------------------------------------------------- figures
def ef(v):
    return 0.5 if -1 <= v < 0 else (1 - v if 0 <= v < 1 else 0.0)


def eF(v):
    return 0.0 if v < -1 else ((v + 1) / 2 if v < 0 else (0.5 + v - v * v / 2 if v < 1 else 1.0))


TX = [(-1, "-1"), (1, "1")]
Pf = w.Plot("pf", (-1.6, 1.6), (0, 1.15), w=760, h=250, xticks=TX, yticks=[(0.5, "1/2"), (1, "1")], yname="f(x)",
            pad=(60, 60, 40, 46))
Pf.seg("pf-f1", [(-1.55, 0), (-1, 0)], kind="ink", hidden=False)
Pf.seg("pf-f2", [(-1, 0.5), (0, 0.5)], kind="b", hidden=False)
Pf.seg("pf-f3", [(0, 1), (1, 0), (1.55, 0)], kind="a", hidden=False)
Pf.area("pf-s1", ef, -1, -0.5, kind="b")
Pf.area("pf-s2", ef, -1, 0.5, kind="d")
Pf.vline("pf-t1", -0.5, 0, 0.9)
Pf.vline("pf-t2", 0.5, 0, 0.9)
Pf.label("pf-lt1", -0.5, 0.95, "t", kind="ink")
Pf.label("pf-lt2", 0.5, 0.95, "t", kind="ink")

def plot_F(p, shown, h=330):
    """the F of the example; pieces hidden (built step by step) or shown; the wrong branch {p}-bad always hidden"""
    G = w.Plot(p, (-1.6, 1.6), (0, 1.15), w=760, h=h, xticks=TX, yticks=[(0.5, "1/2"), (1, "1")], xname="t",
               yname="F(t)", pad=(60, 60, 40, 46))
    hd = not shown
    G.seg(f"{p}-0", [(-1.55, 0), (-1, 0)], kind="ink", hidden=hd)
    G.seg(f"{p}-1", [(-1, 0), (0, 0.5)], kind="b", hidden=hd)
    G.curve(f"{p}-2", eF, 0, 1, kind="a", hidden=hd)
    G.seg(f"{p}-3", [(1, 1), (1.55, 1)], kind="ink", hidden=hd)
    G.curve(f"{p}-bad", lambda v: v - v * v / 2, 0, 1, kind="bad", dash=True)
    G.dot(f"{p}-j0", 0, 0.5, "(0, 1/2)", dx=-14, dy=-16, anchor="end", kind="b", hidden=hd)
    G.dot(f"{p}-j1", 1, 1, "(1, 1)", dx=-14, dy=-16, anchor="end", kind="a", hidden=hd)
    if not shown:
        G.dot(f"{p}-p1", -0.5, 0.25, None, kind="b")
        G.dot(f"{p}-p2", 0.5, 0.875, None, kind="d")
    return G.svg()


PF = plot_F("pF", False)

PX = w.Plot("px", (-1.4, 4.4), (0, 1.12), w=780, h=400, xticks=[(-1, "-1"), (1, "1"), (2, "2"), (3, "3"), (4, "4")],
            yticks=[(0.75, "3/4"), (1, "1")], xname="t", yname="F(t)")
PX.seg("px-0", [(-1.35, 0), (-1, 0)], kind="ink")
PX.curve("px-1", lambda v: 0.75 * (1 + v)**2, -1, 0, kind="b")
PX.curve("px-2", lambda v: 1 - math.exp(-v) / 4, 0, 4.3, kind="a")
PX.hline("px-one", 1, -1.35, 4.3)
PX.curve("px-bad", lambda v: (1 - math.exp(-v)) / 4, 0, 4.3, kind="bad", dash=True)
PX.dot("px-j", 0, 0.75, "(0, 3/4)", dx=-14, dy=-16, anchor="end", kind="b")
PX.label("px-l1", -0.85, 0.55, "¾(1+t)²", kind="b")
PX.label("px-l2", 2.3, 0.86, "1 − e⁻ᵗ/4", kind="a")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבנה את ההתפלגות המצטברת מתוך צפיפות, קטע אחר קטע."),
    P("נבדוק רציפות בנקודות החיבור, ונראה איך נראה הגרף הנכון."),
    P("ובסוף נפתור סעיף ממבחן.", hold=0.4),
], stage='<div class="kicker">F05 · משתנה רציף</div><h1>התפלגות מצטברת קטע אחר קטע</h1>'
         '<p>לבנות את ההתפלגות המצטברת מצפיפות מחולקת לקטעים, לבדוק רציפות בנקודות החיבור, ולזהות את הגרף הנכון.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("ההתפלגות המצטברת, $F$ של $t$, היא ההסתברות ש-$X$ קטן או שווה ל-$t$.", do=show("i-def"),
      say="ההתפלגות המצטברת, אֶף של טִי, היא ההסתברות שאִקְס קטן או שווה לטִי."),
    P("כלומר: **כל השטח שנצבר** מתחת לצפיפות, משמאל ל-$t$.", do=show("pf-s1", "pf-t1", "pf-lt1"),
      say="כלומר: כל השטח שנצבר מתחת לצפיפות, משמאל לטִי."),
    P("נבנה אותה לצפיפות הזאת: חצי ממינוס אחת עד אפס, ואז אחת פחות $x$ עד אחת.", do=show("i-f"),
      say="נבנה אותה לצפיפות הזאת: חצי ממינוס אחת עד אפס, ואז אחת פחות אִקְס עד אחת."),
    P("לפני מינוס אחת לא נצבר כלום: $F$ שווה אפס.", do=show("pF-0", "i-0"),
      say="לפני מינוס אחת לא נצבר כלום: אֶף שווה אפס."),
    P("בקטע הראשון נצבר מלבן: רוחב $t$ ועוד אחת, גובה חצי.", do=show("pF-1", "pF-p1", "i-1"),
      say="בקטע הראשון נצבר מלבן: רוחב טִי ועוד אחת, גובה חצי."),
    P("בסוף הקטע, באפס, כבר נצבר חצי. זו נקודת החיבור.", do=show("pF-j0")),
    P("בקטע השני **ממשיכים** מהחצי: חצי, ועוד האינטגרל מאפס עד $t$ של אחת פחות $x$.",
      do=show("pf-s2", "pf-t2", "pf-lt2", "i-2", "i-r"),
      say="בקטע השני ממשיכים מהחצי: חצי, ועוד האינטגרל מאפס עד טִי של אחת פחות אִקְס."),
    P("יוצא חצי, ועוד $t$, פחות $t^2$ חלקי שתיים.", do=show("pF-2", "pF-p2"),
      say="יוצא חצי, ועוד טִי, פחות טִי בריבוע חלקי שתיים."),
    P("באחת זה חצי ועוד אחת פחות חצי: בדיוק אחת. ומשם והלאה $F$ נשארת אחת.", do=show("pF-j1", "pF-3", "i-3"),
      say="באחת זה חצי ועוד אחת פחות חצי: בדיוק אחת. ומשם והלאה אֶף נשארת אחת."),
], stage=f'<div class="pd-col" style="gap:6px">{Pf.svg()}{PF}</div>',
   panel=st.card("i-def", "rule", "🔑 $F(t)=P(X\\le t)=\\displaystyle\\int_{-\\infty}^t f(x)\\,dx$")
         + w.chip("i-f", "$f=\\tfrac12$ על $[-1,0)$, $\\ f=1-x$ על $[0,1)$", "warn")
         + w.eqs("i", ["$t<-1:\\ \\ F=0$", "$-1\\le t<0:\\ \\ F=\\tfrac{t+1}{2}$",
                       "$0\\le t<1:\\ \\ F=\\tfrac12+t-\\tfrac{t^2}{2}$", "$t\\ge1:\\ \\ F=1$"], size=34, gap=6)
         + st.card("i-r", "rule", "🔑 $F(t)=F(t_0)+\\displaystyle\\int_{t_0}^t f$"))

check = Scene("check", "בדיקות ומלכודת", [
    P("שלוש בדיקות שחייבות לעבור: $F$ רציפה, לא יורדת, ועולה מאפס עד אחת.", do=show("c-1"),
      say="שלוש בדיקות שחייבות לעבור: אֶף רציפה, לא יורדת, ועולה מאפס עד אחת."),
    P("רציפה: בנקודת החיבור, שני הקטעים נותנים אותו ערך. כאן חצי משני הצדדים.", do=show("c-2")),
    P("ועוד בדיקה שימושית: השיפוע של $F$ הוא הצפיפות. בקטע הראשון השיפוע חצי, בדיוק כמו $f$ שם.", do=show("c-4"),
      say="ועוד בדיקה שימושית: השיפוע של אֶף הוא הצפיפות. בקטע הראשון השיפוע חצי, בדיוק כמו אֶף הקטנה שם."),
    P("ובקטע השני, הנגזרת של חצי ועוד $t$ פחות $t^2$ חלקי שתיים היא אחת פחות $t$. שוב הצפיפות.",
      say="ובקטע השני, הנגזרת של חצי ועוד טִי פחות טִי בריבוע חלקי שתיים, היא אחת פחות טִי. שוב הצפיפות."),
    P("ועכשיו המלכודת הנפוצה ביותר: לשכוח את מה שנצבר.", do=show("c-t")),
    P("מי שכותב בקטע השני רק $t$ פחות $t^2$ חלקי שתיים, מתחיל שוב מאפס.", do=show("pG-bad"),
      say="מי שכותב בקטע השני רק טִי פחות טִי בריבוע חלקי שתיים, מתחיל שוב מאפס."),
    P("הגרף שלו **קופץ למטה** באפס, ונגמר בחצי במקום באחת. שתי הבדיקות נכשלות.", do=show("c-3"), hold=0.4),
], stage=f'<div class="pd-col">{plot_F("pG", True, h=420)}</div>',
   panel=st.card("c-1", "rule", "🔑 רציפה, לא יורדת, מ-$0$ עד $1$")
         + st.card("c-2", "ex", "$F(0)=\\tfrac12$ משני הצדדים ✓")
         + st.card("c-4", "rule", "🔑 $F'(t)=f(t)$")
         + st.card("c-t", "trap", "⚠️ שוכחים את $F(0)=\\tfrac12$ שנצבר")
         + st.card("c-3", "ex", "$t-\\tfrac{t^2}{2}$: קופצת למטה, נגמרת ב-$\\tfrac12$ ✗"))

def mini(p, pts_list, curve=None):
    G = w.Plot(p, (-1.5, 1.5), (0, 1.15), w=330, h=270, xticks=[(-1, "-1"), (1, "1")], yticks=[(0.5, "½"), (1, "1")],
               xname="t", yname="", pad=(40, 40, 24, 44))
    for i, pts in enumerate(pts_list):
        G.seg(f"{p}-s{i}", pts, kind="a", hidden=False)
    if curve:
        G.curve(f"{p}-c", curve[0], curve[1], curve[2], kind="a", hidden=False)
    return G.svg()


GA = mini("ga", [[(-1.45, 0), (-1, 0), (0, 0.5)], [(1, 1), (1.45, 1)]], (eF, 0, 1))
GB = mini("gb", [[(-1.45, 0), (-1, 0), (-1, 0.5), (0, 0.5), (0, 1), (1, 0), (1.45, 0)]])
GC = mini("gc", [[(-1.45, 0), (-1, 0), (1, 1), (1.45, 1)]])

graphs = Scene("graphs", "איזה גרף?", [
    P("במבחן לפעמים מבקשים לבחור את הגרף של $F$. הנה שלושה מועמדים לדוגמה שלנו.",
      say="במבחן לפעמים מבקשים לבחור את הגרף של אֶף. הנה שלושה מועמדים לדוגמה שלנו."),
    P("המועמד הזה יורד בסוף, ונגמר באפס. זו בכלל הצפיפות, לא ההתפלגות המצטברת.", do=show("g-b", "g-bx")),
    P("והמועמד הזה עולה מאפס לאחת, רציף ולא יורד. נראה טוב, אבל השיפוע שלו חצי לכל אורכו.", do=show("g-c")),
    P("מימין לאפס הצפיפות היא אחת, ולכן שם השיפוע של $F$ חייב להיות אחת. הוא נפסל.", do=show("g-cx"),
      say="מימין לאפס הצפיפות היא אחת, ולכן שם השיפוע של אֶף חייב להיות אחת. הוא נפסל."),
    P("הנכון: ישר עד חצי באפס, ואז עקומה שמתכופפת, עד אחת באחת.", do=show("g-a", "g-ax"), hold=0.4),
], stage='<div class="pd-row" style="gap:20px;align-items:flex-start">'
         f'<div id="g-c" class="pd-col h" style="gap:8px">{GC}' + w.chip("g-cx", "✗ שיפוע לא נכון", "bad") + '</div>'
         f'<div id="g-b" class="pd-col h" style="gap:8px">{GB}' + w.chip("g-bx", "✗ יורדת: זו $f$", "bad") + '</div>'
         f'<div id="g-a" class="pd-col h" style="gap:8px">{GA}' + w.chip("g-ax", "✓ $F$", "ok") + '</div></div>',
   layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("סעיף ממבחן: מהסעיף הקודם, הצפיפות היא שלושה חצאים כפול אחת ועוד $x$, ממינוס אחת עד אפס.",
      say="סעיף ממבחן: מהסעיף הקודם, הצפיפות היא שלושה חצאים כפול, בסוגריים, אחת ועוד אִקְס, ממינוס אחת עד אפס."),
    P("ומאפס והלאה: רבע כפול $e$ בחזקת מינוס $x$. מבקשים את $F$ ושרטוט.",
      say="ומאפס והלאה: רבע כפול אִי בחזקת מינוס אִקְס. מבקשים את אֶף ושרטוט."),
    P("לפני מינוס אחת: אפס.", do=show("px-0", "x-0")),
    P("בקטע הראשון: האינטגרל של שלושה חצאים כפול אחת ועוד $x$, ממינוס אחת עד $t$.", do=show("x-1"),
      say="בקטע הראשון: האינטגרל של שלושה חצאים כפול, בסוגריים, אחת ועוד אִקְס, ממינוס אחת עד טִי."),
    P("הקדומה של אחת ועוד $x$ היא החצי של הריבוע שלו. יוצא שלושה רבעים כפול אחת ועוד $t$, בריבוע.", do=show("px-1", "px-l1", "x-2"),
      say="הקדומה של אחת ועוד אִקְס היא חצי מהריבוע שלו. יוצא שלושה רבעים, כפול אחת ועוד טִי, בריבוע."),
    P("באפס נצברו שלושה רבעים. זו נקודת החיבור.", do=show("px-j")),
    P("בקטע השני: שלושה רבעים, ועוד רבע כפול אחת פחות $e$ בחזקת מינוס $t$.", do=show("x-3"),
      say="בקטע השני: שלושה רבעים, ועוד רבע, כפול אחת פחות אִי בחזקת מינוס טִי."),
    P("מסדרים: אחת פחות $e$ בחזקת מינוס $t$, חלקי ארבע.", do=show("px-2", "px-l2", "px-one", "x-4"),
      say="מסדרים: אחת פחות אִי בחזקת מינוס טִי, חלקי ארבע."),
    P("בדיקות: באפס שני הקטעים נותנים שלושה רבעים, ובאינסוף $F$ שואפת לאחת.", do=show("x-ok"),
      say="בדיקות: באפס שני הקטעים נותנים שלושה רבעים, ובאינסוף אֶף שואפת לאחת."),
    P("המלכודת כאן: להתחיל את הקטע השני מאפס. אז $F$ נגמרת ברבע.", do=show("px-bad", "x-t"),
      say="המלכודת כאן: להתחיל את הקטע השני מאפס. אז אֶף נגמרת ברבע."),
    P("ומלכודת נוספת: לכתוב אחת פחות $e$ בחזקת מינוס $t$ חלקי ארבע גם לפני אפס. כל ענף שייך לקטע שלו.", hold=0.6,
      say="ומלכודת נוספת: לכתוב אחת פחות אִי בחזקת מינוס טִי חלקי ארבע, גם לפני אפס. כל ענף שייך לקטע שלו."),
], stage=f'<div class="pd-col">{PX.svg()}'
         + st.card("x-t", "trap", "⚠️ הקטע השני מתחיל מ-$F(0)=\\tfrac34$, לא מ-$0$") + "</div>",
   panel=w.stem(Q["id"], "$f=\\tfrac32(1+x)$ על $[-1,0)$, $\\ f=\\tfrac14e^{-x}$ ל-$x\\ge0$.<br>חשבו את $F_X(t)$ ושרטטו.")
         + w.eqs("x", ["$t<-1:\\ \\ F=0$", "$\\displaystyle\\int_{-1}^t \\tfrac32(1+x)\\,dx$", "$=\\tfrac34(1+t)^2$",
                       "$t\\ge0:\\ \\ \\tfrac34+\\tfrac14\\left(1-e^{-t}\\right)$", "$=1-\\tfrac14e^{-t}$"], size=32, gap=4)
         + w.chip("x-ok", "$F(0)=\\tfrac34$ משני הצדדים ✓"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: $F$ של $t$ היא כל השטח שנצבר משמאל ל-$t$.", do=show("r-1"),
      say="לסיכום: אֶף של טִי היא כל השטח שנצבר משמאל לטִי."),
    P("בכל קטע ממשיכים ממה שנצבר עד תחילתו, ומוסיפים את האינטגרל בתוך הקטע.", do=show("r-2")),
    P("ובודקים: רציפה בנקודות החיבור, לא יורדת, מאפס עד אחת.", do=show("r-3")),
    P("והגרף שקופץ למטה, או נגמר מתחת לאחת, שכח לצבור. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="pd-col"><div class="pd-big">$F(t)=F(t_0)+\\displaystyle\\int_{t_0}^{t} f(x)\\,dx$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $F(t)=P(X\\le t)$")
         + st.card("r-2", "rule", "🔑 כל קטע מוסיף למה שנצבר")
         + st.card("r-3", "ex", "רציפה, לא יורדת, מ-$0$ עד $1$")
         + st.card("r-4", "trap", "⚠️ קפיצה למטה = שכחו לצבור"))

VIDEO = Video("F05", "pdf", "התפלגות מצטברת קטע אחר קטע", w.fix_scenes([title, idea, check, graphs, exam, recap]),
              bank={"25A-C-Q3b": None})
