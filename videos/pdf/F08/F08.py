# -*- coding: utf-8 -*-
"""F08 · מגרף לנוסחה — video script (build: tools/video/vid.py F08).

Source: courses/pdf/C08.js (lesson + goal: read a sketched density, find the unknown height from the area, write a
formula per segment, compute a probability).
Exam anchor: 25A-B-Q3a (the original exam figure images/exams/25A-B-Q3-pdf.png, shown cropped and never redrawn:
a on [-1,0), a triangle with apex (1,b) on [0,2]; E[X] = mu: a + b = 1, -a/2 + b = mu, so a = 2(1-mu)/3,
b = (1+2mu)/3). No guided quiz uses it.
Not used on purpose: every C08 quiz item (the trapezoid 0 -> c on [0,1) then c to 3: c = 2/5, the formula 2x/5,
P(X>1); the tent with apex (1, h) on [0,3]: h = 2/3, (3-x)/3, P(X>2)) and the boss polygon 24A-B-Q4a. The worked
example is new: height h on [0,1), then a straight line down to 0 at x = 3 (h = 1/2, f = (3-x)/4, P(X>2) = 1/8).
Every area, line, constant and integral is computed with sympy and cross-checked numerically.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pdf as w
from w_pdf import x, t, R, Pdf, oo

hh, a, b, mu = sp.symbols("h a b mu", real=True)


def line(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    m = (y2 - y1) / (x2 - x1)
    return sp.expand(y1 + m * (x - x1))


# ---------------------------------------------------------------- example: h on [0,1), line (1,h) -> (3,0)
area = hh * 1 + R(1, 2) * 2 * hh
assert area == 2 * hh
H = sp.solve(area - 1, hh)[0]
assert H == R(1, 2)
L = line((1, H), (3, 0))
assert sp.simplify(L - (3 - x) / 4) == 0 and L.subs(x, 1) == H and L.subs(x, 3) == 0
assert sp.diff(L, x) == -R(1, 4)
E = Pdf([(0, 1, H), (1, 3, L)])
assert E.total() == 1 and E.nonneg()
assert L.subs(x, 2) == R(1, 4)
assert E.prob(2, 3) == R(1, 8) == R(1, 2) * 1 * R(1, 4)
assert E.prob(0, 1) == R(1, 2)

# ---------------------------------------------------------------- exam 25A-B-Q3a
Q = BANK["25A-B-Q3a"]
assert "\\mu" in Q["question"]
up, down = line((0, 0), (1, b)), line((1, b), (2, 0))
assert sp.simplify(up - b * x) == 0 and sp.simplify(down - b * (2 - x)) == 0
N = sp.integrate(a, (x, -1, 0)) + sp.integrate(up, (x, 0, 1)) + sp.integrate(down, (x, 1, 2))
assert sp.simplify(N - (a + b)) == 0
assert R(1, 2) * 2 * b == b                                       # triangle: half base times height
M = sp.integrate(x * a, (x, -1, 0)) + sp.integrate(x * up, (x, 0, 1)) + sp.integrate(x * down, (x, 1, 2))
assert sp.simplify(M - (-a / 2 + b)) == 0
assert sp.integrate(x * up, (x, 0, 1)) == b / 3 and sp.simplify(sp.integrate(x * down, (x, 1, 2)) - 2 * b / 3) == 0
S = sp.solve([N - 1, M - mu], [a, b])
assert sp.simplify(S[a] - R(2, 3) * (1 - mu)) == 0 and sp.simplify(S[b] - (1 + 2 * mu) / 3) == 0
for m in (R(-1, 2), 0, R(1, 2), 1):
    am, bm = S[a].subs(mu, m), S[b].subs(mu, m)
    p = Pdf([(-1, 0, am), (0, 1, bm * x), (1, 2, bm * (2 - x))])
    assert p.total() == 1 and p.mean() == m
assert sp.reduce_inequalities([S[a] >= 0, S[b] >= 0], mu).as_set() == sp.Interval(-R(1, 2), 1)
for m in (R(-1, 2), 0, R(1, 2), 1):                                   # 25A-B-Q3d: P(X<1 | X>0) = 1/2 for every mu
    bm = S[b].subs(mu, m)
    p = Pdf([(-1, 0, S[a].subs(mu, m)), (0, 1, bm * x), (1, 2, bm * (2 - x))])
    if bm != 0:
        assert p.prob(0, 1) / p.prob(0, 2) == R(1, 2)
assert S[b].subs(mu, -R(1, 2)) == 0 and S[a].subs(mu, 1) == 0
WRONG = sp.solve([a + 2 * b - 1, -a / 2 + b - mu], [a, b])       # triangle area taken as 2b
assert sp.simplify(WRONG[b] - S[b]) != 0

# ---------------------------------------------------------------- figures
PL = w.Plot("pl", (-0.3, 3.5), (0, 0.72), w=800, h=400, xticks=[(1, "1"), (2, "2"), (3, "3")],
            yticks=[(0.25, "1/4"), (0.5, "h")])
PL.seg("pl-f", [(-0.25, 0), (0, 0), (0, 0.5), (1, 0.5), (3, 0), (3.45, 0)], kind="a", hidden=False)
PL.dot("pl-d0", 0, 0.5, "(0, h)", dx=12, dy=-16)
PL.dot("pl-d1", 1, 0.5, "(1, h)", dx=12, dy=-16)
PL.dot("pl-d3", 3, 0, "(3, 0)", dx=0, dy=-20, anchor="middle")
PL.area("pl-rect", lambda v: 0.5, 0, 1, kind="b")
PL.area("pl-tri", lambda v: (3 - v) / 4, 1, 3, kind="d")
PL.area("pl-tail", lambda v: (3 - v) / 4, 2, 3, kind="c")
PL.dot("pl-d2", 2, 0.25, "(2, 1/4)", dx=12, dy=-16, kind="b")
PL.label("pl-lr", 0.5, 0.2, "h", kind="ink")
PL.label("pl-lt", 1.55, 0.12, "2h/2", kind="ink")
PL.label("pl-lf", 2.25, 0.42, "(3 − x)/4", kind="a", anchor="start")

FIG = w.raster_crop("fig", "images/exams/25A-B-Q3-pdf.png", (477, 282), 660, keep=0.83)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה הצפיפות לא ניתנת בנוסחה, אלא בשרטוט."),
    P("נקרא את הנקודות, נמצא את הגובה מהשטח, ונכתוב נוסחה לכל קטע."),
    P("ובסוף נפתור סעיף ממבחן עם השרטוט המקורי.", hold=0.4),
], stage='<div class="kicker">F08 · משתנה רציף</div><h1>מגרף לנוסחה</h1>'
         '<p>לקרוא שרטוט של צפיפות, למצוא את הגובה הלא ידוע משטח, לכתוב נוסחה לכל קטע ולחשב הסתברות.</p>',
   layout="title")

read = Scene("read", "קוראים את השרטוט", [
    P("הנה שרטוט: הצפיפות שטוחה בגובה $h$ מאפס עד אחת, ואז יורדת בקו ישר עד אפס, בשלוש.",
      say="הנה שרטוט: הצפיפות שטוחה בגובה אֵייץ' מאפס עד אחת, ואז יורדת בקו ישר עד אפס, בשלוש."),
    P("צעד ראשון: רושמים את הנקודות שבהן הקו נשבר. גם עם הסימן $h$.", do=show("pl-d0", "pl-d1", "pl-d3", "s-0"),
      say="צעד ראשון: רושמים את הנקודות שבהן הקו נשבר. גם עם הסימן אֵייץ'."),
    P("צעד שני: הנרמול הוא **שטח**, ואין צורך באינטגרל. מפרקים לצורות פשוטות.", do=show("s-r")),
    P("מלבן ברוחב אחת ובגובה $h$: השטח $h$.", do=show("pl-rect", "pl-lr", "s-1"),
      say="מלבן ברוחב אחת ובגובה אֵייץ': השטח אֵייץ'."),
    P("ומשולש בבסיס שתיים ובגובה $h$: חצי בסיס כפול גובה, כלומר שוב $h$.", do=show("pl-tri", "pl-lt", "s-2"),
      say="ומשולש בבסיס שתיים ובגובה אֵייץ': חצי בסיס כפול גובה, כלומר שוב אֵייץ'."),
    P("שתיים $h$ שווה אחת, ולכן $h$ הוא חצי.", do=show("s-3"),
      say="שתיים אֵייץ' שווה אחת, ולכן אֵייץ' הוא חצי."),
    P("צעד שלישי: נוסחה לכל קטע. בקטע הראשון היא פשוט חצי.", do=show("s-4")),
    P("בשני, ישר דרך $(1,\\tfrac12)$ ו-$(3,0)$. השיפוע: מינוס חצי חלקי שתיים, כלומר מינוס רבע.", do=show("s-5"),
      say="בשני, ישר דרך שתי נקודות: הנקודה שבה אִקְס אחת והגובה חצי, והנקודה שבה אִקְס שלוש והגובה אפס. השיפוע: מינוס חצי חלקי שתיים, כלומר מינוס רבע."),
    P("יוצא שלוש פחות $x$, חלקי ארבע. ובודקים בנקודה: באחת זה חצי, ובשלוש אפס.", do=show("s-6", "pl-lf"),
      say="יוצא שלוש פחות אִקְס, חלקי ארבע. ובודקים בנקודה: באחת זה חצי, ובשלוש אפס."),
    P("ועכשיו הסתברות: $X$ גדול משתיים. בשתיים הגובה הוא רבע.", do=show("pl-d2"),
      say="ועכשיו הסתברות: אִקְס גדול משתיים. בשתיים הגובה הוא רבע."),
    P("הזנב הוא משולש קטן: בסיס אחת, גובה רבע. השטח שמינית.", do=show("pl-tail", "s-ok"), hold=0.4),
], stage=f'<div class="pd-col">{PL.svg()}</div>',
   panel=w.eqs("s", ["$(0,h),\\ (1,h),\\ (3,0)$", "<span dir=\"rtl\">מלבן: $1\\cdot h=h$</span>",
                     "<span dir=\"rtl\">משולש: $\\tfrac{2\\cdot h}{2}=h$</span>", "$2h=1\\ \\Rightarrow\\ h=\\tfrac12$",
                     "$[0,1):\\ \\ f=\\tfrac12$", "$m=\\tfrac{0-1/2}{3-1}=-\\tfrac14$", "$[1,3):\\ \\ f=\\tfrac{3-x}{4}$"],
                 size=32, gap=4)
         + st.card("s-r", "rule", "🔑 נרמול = סכום שטחים $=1$")
         + w.chip("s-ok", "$P(X>2)=\\tfrac12\\cdot1\\cdot\\tfrac14=\\tfrac18$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("סעיף ממבחן, עם השרטוט המקורי. הצפיפות היא הקבוע $a$ ממינוס אחת עד אפס.",
      say="סעיף ממבחן, עם השרטוט המקורי. הצפיפות היא הקבוע אֵיי ממינוס אחת עד אפס."),
    P("ואחריו משולש מאפס עד שתיים, עם קודקוד בגובה $b$ באחת. התוחלת היא $\\mu$, ומבקשים את $a$ ו-$b$.",
      say="ואחריו משולש מאפס עד שתיים, עם קודקוד בגובה בִּי באחת. התוחלת היא מְיוּ, ומבקשים את אֵיי ובִּי."),
    P("הנרמול משטחים: מלבן בשטח $a$, ומשולש בבסיס שתיים ובגובה $b$, כלומר בשטח $b$.", do=show("x-0"),
      say="הנרמול משטחים: מלבן בשטח אֵיי, ומשולש בבסיס שתיים ובגובה בִּי, כלומר בשטח בִּי."),
    P("לכן $a$ ועוד $b$ שווה אחת. והמלכודת: לכתוב שטח משולש כבסיס כפול גובה, שתיים $b$.", do=show("x-1", "x-t"),
      say="לכן אֵיי ועוד בִּי שווה אחת. והמלכודת: לכתוב שטח משולש כבסיס כפול גובה, שתיים בִּי."),
    P("לתוחלת צריך נוסחאות. עולה דרך אפס-אפס ואחת-$b$: $b x$. ויורד דרך אחת-$b$ ושתיים-אפס: $b$ כפול שתיים פחות $x$.",
      do=show("x-2"),
      say="לתוחלת צריך נוסחאות. העולה עובר דרך הראשית ודרך אחת ובִּי: בִּי אִקְס. והיורד עובר דרך אחת ובִּי, ודרך שתיים ואפס: בִּי כפול, בסוגריים, שתיים פחות אִקְס."),
    P("התוחלת: מהמלבן מינוס $a$ חצאים, כי הוא בצד השלילי.", do=show("x-3"),
      say="התוחלת: מהמלבן מינוס אֵיי חצאים, כי הוא בצד השלילי."),
    P("ומהמשולש: $b$ שלישים ועוד שני שלישים $b$, כלומר $b$.", do=show("x-4"),
      say="ומהמשולש: בִּי שלישים, ועוד שני שלישים בִּי, כלומר בִּי."),
    P("וזה הגיוני: המשולש סימטרי סביב אחת, ולכן הוא תורם את השטח שלו כפול אחת.", do=show("x-r")),
    P("שתי משוואות: $a$ ועוד $b$ שווה אחת, ומינוס $a$ חצאים ועוד $b$ שווה $\\mu$.", do=show("x-5"),
      say="שתי משוואות: אֵיי ועוד בִּי שווה אחת, ומינוס אֵיי חצאים ועוד בִּי שווה מְיוּ."),
    P("מציבים $a$ שווה אחת פחות $b$: שלושה $b$ חצאים, פחות חצי, שווה $\\mu$.", do=show("x-6"),
      say="מציבים אֵיי שווה אחת פחות בִּי: שלושה בִּי חצאים, פחות חצי, שווה מְיוּ."),
    P("לכן $b$ הוא אחת ועוד שתיים $\\mu$, חלקי שלוש. ו-$a$ הוא שני שלישים כפול אחת פחות $\\mu$.", do=show("x-ok"),
      hold=0.6,
      say="לכן בִּי הוא אחת ועוד שתיים מְיוּ, חלקי שלוש. ואֵיי הוא שני שלישים, כפול אחת פחות מְיוּ."),
], stage=f'<div class="pd-col">{FIG}'
         + st.card("x-t", "trap", "⚠️ שטח משולש: $\\tfrac{2\\cdot b}{2}=b$, לא $2b$")
         + st.card("x-r", "ex", "משולש סימטרי סביב $1$: תורם $b\\cdot1$") + "</div>",
   panel=w.stem(Q["id"], "בשרטוט: $a$ על $[-1,0)$, משולש עם קודקוד $(1,b)$ על $[0,2]$. נתון $E[X]=\\mu$. מצאו $a,b$.")
         + w.eqs("x", ["$a\\cdot1+\\tfrac{2\\cdot b}{2}$", "$a+b=1$", "$b\\,x,\\quad b(2-x)$",
                       "$\\displaystyle\\int_{-1}^0 a\\,x\\,dx=-\\tfrac a2$", "$\\tfrac b3+\\tfrac{2b}{3}=b$",
                       "$-\\tfrac a2+b=\\mu$", "$\\tfrac{3b}{2}-\\tfrac12=\\mu$"], size=30, gap=2)
         + w.chip("x-ok", "$a=\\tfrac23(1-\\mu),\\ \\ b=\\tfrac{1+2\\mu}{3}$"))

FIG2 = w.raster_crop("fig2", "images/exams/25A-B-Q3-pdf.png", (477, 282), 660, keep=0.83)

more = Scene("more", "עוד מאותו שרטוט", [
    P("ומאותו שרטוט אפשר לקרוא עוד. איזה ערכים יכולה התוחלת לקבל?",
      say="ומאותו שרטוט אפשר לקרוא עוד. אילו ערכים יכולה התוחלת לקבל?"),
    P("שני הגבהים חייבים להיות אי-שליליים. $a$ אי-שלילי רק כש-$\\mu$ קטן או שווה לאחת.", do=show("y-0"),
      say="שני הגבהים חייבים להיות אִי שליליים. אֵיי אִי שלילי רק כשמְיוּ קטן או שווה לאחת."),
    P("ו-$b$ אי-שלילי רק כש-$\\mu$ גדול או שווה למינוס חצי.", do=show("y-1"),
      say="ובִּי אִי שלילי רק כשמְיוּ גדול או שווה למינוס חצי."),
    P("והקצוות הגיוניים: ב-$\\mu$ שווה אחת נשאר רק המשולש, וב-$\\mu$ מינוס חצי רק המלבן.", do=show("y-r"),
      say="והקצוות הגיוניים: במְיוּ שווה אחת נשאר רק המשולש, ובמְיוּ מינוס חצי נשאר רק המלבן."),
    P("ועוד שאלה: ההסתברות ש-$X$ קטן מאחת, בהינתן ש-$X$ חיובי.",
      say="ועוד שאלה: ההסתברות שאִקְס קטן מאחת, בהינתן שאִקְס חיובי."),
    P("התנאי הוא כל המשולש, בשטח $b$. והחיתוך הוא חצי המשולש השמאלי, בשטח $b$ חצאים.", do=show("y-2"),
      say="התנאי הוא כל המשולש, בשטח בִּי. והחיתוך הוא חצי המשולש השמאלי, בשטח בִּי חצאים."),
    P("היחס הוא חצי, בלי קשר ל-$\\mu$. השרטוט חסך את כל החישוב.", do=show("y-ok"), hold=0.6,
      say="היחס הוא חצי, בלי קשר למְיוּ. השרטוט חסך את כל החישוב."),
], stage=f'<div class="pd-col">{FIG2}' + st.card("y-r", "ex", "$\\mu=1$: רק משולש · $\\mu=-\\tfrac12$: רק מלבן") + "</div>",
   panel=w.eqs("y", ["$a=\\tfrac23(1-\\mu)\\ge0\\iff\\mu\\le1$", "$b=\\tfrac{1+2\\mu}{3}\\ge0\\iff\\mu\\ge-\\tfrac12$",
                     "$P(X<1\\mid X>0)=\\dfrac{b/2}{b}$"], size=34, gap=12)
         + w.chip("y-ok", "$-\\tfrac12\\le\\mu\\le1,\\ \\ \\ P=\\tfrac12$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: משרטוט, קודם רושמים את הנקודות שבהן הקו נשבר.", do=show("r-1")),
    P("הנרמול הוא סכום שטחים: מלבן הוא רוחב כפול גובה, ומשולש הוא חצי מזה.", do=show("r-2")),
    P("נוסחה לקטע: ישר דרך שתי נקודות, עם שיפוע של הפרש גבהים חלקי הפרש רוחב.", do=show("r-3")),
    P("ואחרי כל נוסחה בודקים אותה בנקודה מהשרטוט. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="pd-col"><div class="pd-big">$y=y_1+m\\,(x-x_1),\\quad m=\\dfrac{y_2-y_1}{x_2-x_1}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 נקודות השבירה $(x,y)$")
         + st.card("r-2", "rule", "🔑 מלבן $w\\cdot h$, משולש $\\tfrac{w\\cdot h}{2}$")
         + st.card("r-3", "ex", "ישר דרך שתי נקודות")
         + st.card("r-4", "trap", "⚠️ בודקים בנקודה מהשרטוט"))

VIDEO = Video("F08", "pdf", "מגרף לנוסחה", w.fix_scenes([title, read, exam, more, recap]),
              bank={"25A-B-Q3a": None, "25A-B-Q3b": None, "25A-B-Q3d": None})
