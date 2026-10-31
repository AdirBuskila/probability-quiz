# -*- coding: utf-8 -*-
"""E03 · הנתונים p, q, s: חיתוך, זרים ובלתי תלויים — video script (build: tools/video/vid.py E03).

Source: courses/events/C03.js (lesson + goal: from P(A)=p, P(B)=q, P(A∪B)=s get the four cells, decide disjoint /
independent / feasible). Exam anchors: 25A-C-Q2f (for which p, q, s are A, B disjoint?) and 25A-C-Q2e (for which
are they independent?), open questions (bank key None) that no guided quiz uses.
Avoided on purpose: the C03 quiz data (0.5/0.4/0.7, 0.3/0.5/0.8, 0.4/0.5 independent, P(A)=0.6 & P(B)=0.7 with
s=0.65, 0.3/0.5/0.7), 25A-C-Q2a / 25A-C-Q2b (C04 / C07 quiz: P(A/B), P(B/Ā) of this same context, never computed
here) and 25A-B-Q2e (C10 boss: independence with another set of givens).
Worked examples: p=0.6, q=0.5, s=0.8 (independent, not disjoint); p=0.3, q=0.45 with s = 0.4 or 0.8 (impossible).
Every cell is computed from the union rule and re-verified on an explicit four-cell space (w_events.Space).
"""
from fractions import Fraction as Fr
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w


def cells(p, q, s):
    """the four cells from p, q, s by the union rule; verified back on an explicit space"""
    ab, an, nb, nn = p + q - s, s - q, s - p, 1 - s
    if min(ab, an, nb, nn) < 0:
        return None
    S = w.Space([({"A": 1, "B": 1}, ab), ({"A": 1, "B": 0}, an), ({"A": 0, "B": 1}, nb), ({"A": 0, "B": 0}, nn)])
    assert S.P(lambda o: o["A"]) == p and S.P(lambda o: o["B"]) == q and S.P(lambda o: o["A"] or o["B"]) == s
    return S, (ab, an, nb, nn)


# ---------------------------------------------------------------- example 1: p=0.6, q=0.5, s=0.8
p1, q1, s1 = Fr("0.6"), Fr("0.5"), Fr("0.8")
S1, (ab1, an1, nb1, nn1) = cells(p1, q1, s1)
assert (ab1, an1, nb1, nn1) == (Fr("0.3"), Fr("0.3"), Fr("0.2"), Fr("0.2")) and sum((ab1, an1, nb1, nn1)) == 1
assert S1.both(lambda o: o["A"] and o["B"]) == ab1 == p1 * q1                 # independent
assert ab1 != 0                                                               # not disjoint
assert S1.P(lambda o: o["A"], given=lambda o: o["B"]) == p1                   # knowing B does not change P(A)

# ---------------------------------------------------------------- example 2: p=0.3, q=0.45, which s are possible
p2, q2 = Fr("0.3"), Fr("0.45")
lo, hi = max(p2, q2), min(1, p2 + q2)
assert (lo, hi) == (Fr("0.45"), Fr("0.75"))
assert cells(p2, q2, Fr("0.4")) is None and p2 + q2 - Fr("0.4") == Fr("0.35") > p2 and Fr("0.4") - q2 < 0
assert cells(p2, q2, Fr("0.8")) is None and p2 + q2 - Fr("0.8") == Fr("-0.05")
for k in range(0, 31):                                                        # every s on a grid: feasible <=> in range
    s = Fr(k, 30)
    assert (cells(p2, q2, s) is not None) == (lo <= s <= hi)

# ---------------------------------------------------------------- exam 25A-C-Q2f / Q2e (symbolic, then spot checks)
QF, QE = BANK["25A-C-Q2f"], BANK["25A-C-Q2e"]
assert QF["contextId"] == QE["contextId"] == "25A-C-c2"
assert "s=p+q" in QF["solution"].replace(" ", "") and "s=p+q-pq" in QE["solution"].replace(" ", "")
p, q, s = sp.symbols("p q s")
inter = p + q - s
assert sp.solve(sp.Eq(inter, 0), s) == [p + q]                                # disjoint
assert sp.solve(sp.Eq(inter, p * q), s) == [p + q - p * q]                    # independent
for pp, qq in [(Fr(1, 5), Fr(1, 2)), (Fr(2, 5), Fr(1, 3)), (Fr(1, 4), Fr(3, 4))]:
    Sd, c = cells(pp, qq, pp + qq)                                            # s = p + q: the intersection is empty
    assert Sd.P(lambda o: o["A"] and o["B"]) == 0
    Si, c = cells(pp, qq, pp + qq - pp * qq)                                  # s = p + q - pq: independent
    assert Si.both(lambda o: o["A"] and o["B"]) == pp * qq
    assert Si.P(lambda o: o["A"], given=lambda o: o["B"]) == pp
assert sp.expand(1 - (1 - p) * (1 - q) - (p + q - p * q)) == 0                # s = 1 - P(none) = 1 - (1-p)(1-q)

# ---------------------------------------------------------------- figures
T1 = w.cells_table("t1", {"ab": "0.3", "an": "0.3", "nb": "0.2", "nn": "0.2", "mA": "0.6", "mnA": "0.4",
                          "mB": "0.5", "mnB": "0.5", "tot": "1"}, shown=("mA", "mB"))
T0 = w.cells_table("t0", {"ab": "p+q-s", "an": "s-q", "nb": "s-p", "nn": "1-s", "mA": "p", "mnA": "1-p",
                          "mB": "q", "mnB": "1-q", "tot": "1"}, shown=("mA", "mB", "tot"))
T2 = w.cells_table("t2", {"ab": "0.35", "an": "-0.05", "nb": "0.1", "nn": "0.6", "mA": "0.3", "mnA": "0.7",
                          "mB": "0.45", "mnB": "0.55", "tot": "1"}, shown=("mA", "mB"))
assert (p2 + q2 - Fr("0.4"), p2 - (p2 + q2 - Fr("0.4")), q2 - (p2 + q2 - Fr("0.4")), 1 - Fr("0.4")) == \
       (Fr("0.35"), Fr("-0.05"), Fr("0.1"), Fr("0.6"))
TX = w.cells_table("tx", {"ab": "p+q-s", "an": "s-q", "nb": "s-p", "nn": "1-s", "mA": "p", "mnA": "1-p",
                          "mB": "q", "mnB": "1-q", "tot": "1"}, shown=("mA", "mB", "tot", "ab", "an", "nb", "nn"))

STEM = (f'<div class="qstem"><span class="qid">{QF["id"]} · {QE["id"]}</span>$P(A)=p$, $P(B)=q$ ו-$P(A\\cup B)=s$. '
        'עבור אילו $p,q,s$ המאורעות <b>זרים</b>? ועבור אילו הם <b>בלתי תלויים</b>?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את אחת השאלות הנפוצות במבחנים: נתונים שלושה מספרים, $p$, $q$ ו-$s$.",
      say="בסרטון הזה נכיר את אחת השאלות הנפוצות במבחנים: נתונים שלושה מספרים, פִּי, קְיוּ ואֶס."),
    P("נבנה מהם את כל התמונה, ונכריע מתי המאורעות זרים, מתי בלתי תלויים, ומתי הנתונים בכלל אפשריים."),
    P("ובסוף נפתור שני סעיפים אמיתיים ממבחן.", hold=0.4),
], stage='<div class="kicker">E03 · מאורעות</div><h1>הנתונים p, q, s</h1>'
         '<p>מתוך $P(A)$, $P(B)$ ו-$P(A\\cup B)$: ארבעת התאים, זרים, בלתי תלויים, והאם הנתונים אפשריים.</p>',
   layout="title")

idea = Scene("idea", "ארבעה תאים", [
    P("נתונים $P(A)=p$, $P(B)=q$, וההסתברות של האיחוד, $s$.",
      say="נתונים פֵּה של אֵיי שווה פִּי, פֵּה של בִּי שווה קְיוּ, וההסתברות של האיחוד, אֶס.", do=show("i-1")),
    P("הצעד הראשון תמיד אותו צעד: כלל האיחוד, מסודר מחדש. החיתוך שווה $p$ ועוד $q$ פחות $s$.",
      say="הצעד הראשון תמיד אותו צעד: כלל האיחוד, מסודר מחדש. החיתוך שווה פִּי ועוד קְיוּ פחות אֶס.",
      do=show("i-2", "t0-ab")),
    P("שני מאורעות מחלקים את אומגה לארבעה תאים זרים. נכתוב אותם בטבלה: שורה לכל מצב של $A$, ועמודה לכל מצב של $B$.",
      say="שני מאורעות מחלקים את אומגה לארבעה תאים זרים. נכתוב אותם בטבלה: שורה לכל מצב של אֵיי, ועמודה לכל מצב של בִּי."),
    P("$A$ בלי $B$: כל האיחוד, פחות $B$. כלומר $s$ פחות $q$.",
      say="אֵיי בלי בִּי: כל האיחוד, פחות בִּי. כלומר אֶס פחות קְיוּ.", do=show("t0-an")),
    P("$B$ בלי $A$: באותו אופן, $s$ פחות $p$.", say="בִּי בלי אֵיי: באותו אופן, אֶס פחות פִּי.", do=show("t0-nb")),
    P("ואף אחד: המשלים של האיחוד, אחת פחות $s$.", say="ואף אחד: המשלים של האיחוד, אחת פחות אֶס.", do=show("t0-nn")),
    P("שורה מסתכמת להסתברות שבשוליים שלה, וכל ארבעת התאים יחד מסתכמים לאחת. זו הבדיקה שלכם.",
      do=show("t0-mnA", "t0-mnB"), hold=0.3),
    P("ועכשיו שתי ההגדרות. **זרים**: החיתוך הוא אפס.", do=show("i-3")),
    P("**בלתי תלויים**: החיתוך שווה למכפלה של שתי ההסתברויות.", do=show("i-4"), hold=0.4),
], stage=f'<div class="ev-stack">{T0}</div>',
   panel=st.card("i-1", "plain", "$P(A)=p,\\ P(B)=q,\\ P(A\\cup B)=s$")
         + st.card("i-2", "rule", "🔑 $P(A\\cap B)=p+q-s$")
         + st.card("i-3", "ex", "זרים: $P(A\\cap B)=0$")
         + st.card("i-4", "ex", "בלתי תלויים: $P(A\\cap B)=P(A)\\,P(B)$"))

ex1 = Scene("ex1", "דוגמה", [
    P("דוגמה: $p$ שווה אפס נקודה שש, $q$ אפס נקודה חמש, ו-$s$ אפס נקודה שמונה.",
      say="דוגמה: פִּי שווה אפס נקודה שש, קְיוּ אפס נקודה חמש, ואֶס אפס נקודה שמונה.", do=show("a-1")),
    P("החיתוך: אפס נקודה שש ועוד אפס נקודה חמש פחות אפס נקודה שמונה. יוצא אפס נקודה שלוש.",
      do=show("t1-ab", "a-2")),
    P("$A$ בלי $B$: אפס נקודה שמונה פחות אפס נקודה חמש, כלומר אפס נקודה שלוש.",
      say="אֵיי בלי בִּי: אפס נקודה שמונה פחות אפס נקודה חמש, כלומר אפס נקודה שלוש.", do=show("t1-an")),
    P("$B$ בלי $A$: אפס נקודה שמונה פחות אפס נקודה שש, כלומר אפס נקודה שתיים. ואף אחד: אפס נקודה שתיים.",
      say="בִּי בלי אֵיי: אפס נקודה שמונה פחות אפס נקודה שש, כלומר אפס נקודה שתיים. ואף אחד: אפס נקודה שתיים.",
      do=show("t1-nb", "t1-nn")),
    P("בדיקה: שלוש ועוד שלוש ועוד שתיים ועוד שתיים עשיריות, זה אחת. הטבלה תקינה.",
      do=show("t1-mnA", "t1-mnB", "t1-tot"), hold=0.3),
    P("זרים? לא. החיתוך הוא אפס נקודה שלוש, ולא אפס.", do=show("a-3")),
    P("בלתי תלויים? המכפלה: אפס נקודה שש כפול אפס נקודה חמש, כלומר אפס נקודה שלוש.", do=show("t1-h-ab")),
    P("והחיתוך גם הוא אפס נקודה שלוש. הם שווים, ולכן המאורעות **בלתי תלויים**.", do=show("a-4"), hold=0.3),
    P("שימו לב: ההחלטה מגיעה רק אחרי שמחשבים את החיתוך. אי אפשר לנחש אותה מהנתונים לבד.", hold=0.4),
], stage=f'<div class="ev-stack">{T1}</div>',
   panel=st.card("a-1", "plain", "$p=0.6,\\ q=0.5,\\ s=0.8$")
         + st.card("a-2", "ex", "$P(A\\cap B)=0.6+0.5-0.8=0.3$")
         + st.card("a-3", "ex", "זרים? $0.3\\ne0$, לא")
         + st.card("a-4", "rule", "🔑 $pq=0.6\\cdot0.5=0.3=P(A\\cap B)$: בלתי תלויים"))

feas = Scene("feas", "האם הנתונים אפשריים?", [
    P("ועכשיו שאלה אחרת: האם כל שלושה מספרים בין אפס לאחת יכולים להיות $p$, $q$ ו-$s$?",
      say="ועכשיו שאלה אחרת: האם כל שלושה מספרים בין אפס לאחת יכולים להיות פִּי, קְיוּ ואֶס?"),
    P("לא. כל אחד מארבעת התאים חייב להיות בין אפס לאחת.", do=show("f-1")),
    P("ניקח $p$ אפס נקודה שלוש, $q$ אפס נקודה ארבעים וחמש, ונבדוק $s$ אפס נקודה ארבע.",
      say="ניקח פִּי שווה אפס נקודה שלוש, קְיוּ שווה אפס נקודה ארבעים וחמש, ונבדוק אֶס שווה אפס נקודה ארבע.", do=show("f-2")),
    P("החיתוך יוצא אפס נקודה שלושים וחמש, גדול מכל $A$. ולכן התא $A$ בלי $B$ יוצא שלילי.",
      say="החיתוך יוצא אפס נקודה שלושים וחמש, גדול מכל אֵיי. ולכן התא אֵיי בלי בִּי יוצא שלילי.",
      do=show("t2-ab", "t2-an", "t2-h-an")),
    P("הסתברות שלילית? אין דבר כזה. כלומר אין מאורעות שמקיימים את הנתונים האלה.", do=show("f-t"), hold=0.3),
    P("הסיבה: האיחוד מכיל את $B$, ולכן $s$ חייב להיות לפחות $q$, ולפחות $p$.",
      say="הסיבה: האיחוד מכיל את בִּי, ולכן אֶס חייב להיות לפחות קְיוּ, ולפחות פִּי.", do=show("f-3")),
    P("ומהצד השני, החיתוך לא שלילי: $s$ לכל היותר $p$ ועוד $q$, וגם לכל היותר אחת.",
      say="ומהצד השני, החיתוך לא שלילי: אֶס לכל היותר פִּי ועוד קְיוּ, וגם לכל היותר אחת."),
    P("כאן הטווח הוא מאפס נקודה ארבעים וחמש ועד אפס נקודה שבעים וחמש. אפס נקודה ארבע מחוץ לו, וגם אפס נקודה שמונה.",
      do=show("f-4"), hold=0.4),
], stage=f'<div class="ev-stack">{T2}</div>',
   panel=st.card("f-1", "rule", "🔑 כל תא בין $0$ ל-$1$")
         + st.card("f-2", "plain", "האם $p=0.3,\\ q=0.45,\\ s=0.4$ אפשרי?")
         + st.card("f-t", "trap", "⚠️ תא שלילי: הנתונים סותרים")
         + st.card("f-3", "rule", "🔑 $\\max(p,q)\\le s\\le\\min(1,\\,p+q)$")
         + st.card("f-4", "ex", "כאן: $0.45\\le s\\le0.75$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שני סעיפים ממבחן, באותיות. נתונים $p$, $q$ ו-$s$ כמו קודם.",
      say="ועכשיו שני סעיפים ממבחן, באותיות. נתונים פִּי, קְיוּ ואֶס כמו קודם.", do=show("x-stem")),
    P("סעיף ראשון: עבור אילו פרמטרים המאורעות **זרים**?"),
    P("זרים פירושו שהחיתוך אפס. והחיתוך, כבר ראינו, הוא $p$ ועוד $q$ פחות $s$.",
      say="זרים פירושו שהחיתוך אפס. והחיתוך, כבר ראינו, הוא פִּי ועוד קְיוּ פחות אֶס.", do=show("tx-h-ab", "x-1")),
    P("לכן זרים בדיוק כאשר $s$ שווה $p$ ועוד $q$: האיחוד הוא סכום פשוט, כי אין מה להחסיר.",
      say="לכן זרים בדיוק כאשר אֶס שווה פִּי ועוד קְיוּ: האיחוד הוא סכום פשוט, כי אין מה להחסיר.", do=show("x-2"), hold=0.3),
    P("סעיף שני: עבור אילו פרמטרים הם **בלתי תלויים**?"),
    P("בלתי תלויים: החיתוך שווה למכפלה. כלומר $p$ ועוד $q$ פחות $s$ שווה $p$ כפול $q$.",
      say="בלתי תלויים: החיתוך שווה למכפלה. כלומר פִּי ועוד קְיוּ פחות אֶס שווה פִּי כפול קְיוּ.", do=show("x-3")),
    P("מעבירים אגפים: $s$ שווה $p$ ועוד $q$ פחות $p$ כפול $q$.",
      say="מעבירים אגפים: אֶס שווה פִּי ועוד קְיוּ פחות פִּי כפול קְיוּ.", do=show("x-4"), hold=0.3),
    P("בדיקת שפיות: אז אף אחד מהם לא קרה בהסתברות $1-s$, שזה $(1-p)(1-q)$.",
      say="בדיקת שפיות: אז אף אחד מהם לא קרה בהסתברות אחת פחות אֶס, שזה, בסוגריים אחת פחות פִּי, כפול, בסוגריים אחת פחות קְיוּ.",
      do=show("tx-h-nn", "x-5")),
    P("בדיוק מה שמצפים ממאורעות בלתי תלויים: גם המשלימים שלהם בלתי תלויים.", hold=0.3),
    P("המלכודת: לכתוב $s$ שווה $p$ כפול $q$. המכפלה היא החיתוך, לא האיחוד.",
      say="המלכודת: לכתוב אֶס שווה פִּי כפול קְיוּ. המכפלה היא החיתוך, לא האיחוד.", do=show("x-t"), hold=0.5),
], stage=f'<div class="ev-stack">{TX}<div class="ev-eqs"><div id="x-1" class="h">$p+q-s=0$</div>'
         '<div id="x-3" class="h">$p+q-s=pq$</div><div id="x-5" class="h">$1-s=(1-p)(1-q)$</div></div></div>',
   panel=f'<div id="x-stem" class="h">{STEM}</div>'
         + st.card("x-2", "rule", "🔑 זרים $\\iff s=p+q$")
         + st.card("x-4", "rule", "🔑 בלתי תלויים $\\iff s=p+q-pq$")
         + st.card("x-t", "trap", "⚠️ $s=pq$ שגוי: $pq$ הוא החיתוך"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מ-$p$, $q$ ו-$s$, הצעד הראשון הוא החיתוך: $p$ ועוד $q$ פחות $s$.",
      say="לסיכום: מפִּי, קְיוּ ואֶס, הצעד הראשון הוא החיתוך: פִּי ועוד קְיוּ פחות אֶס.", do=show("s-1")),
    P("ממנו בונים את ארבעת התאים, ובודקים שהם מסתכמים לאחת.", do=show("s-2")),
    P("זרים: החיתוך אפס. בלתי תלויים: החיתוך שווה למכפלה.", do=show("s-3")),
    P("ותא שלילי אומר שהנתונים בלתי אפשריים. נתראה ברמה הבאה.", do=show("s-4"), hold=0.6),
], stage=f'<div class="ev-stack">{w.cells_table("tr", {"ab": "p+q-s", "an": "s-q", "nb": "s-p", "nn": "1-s", "mA": "p", "mnA": "1-p", "mB": "q", "mnB": "1-q", "tot": "1"}, shown=("ab", "an", "nb", "nn", "mA", "mnA", "mB", "mnB", "tot"))}</div>',
   panel=st.card("s-1", "rule", "🔑 $P(A\\cap B)=p+q-s$")
         + st.card("s-2", "rule", "🔑 ארבעה תאים, סכום $1$")
         + st.card("s-3", "rule", "🔑 זרים: $s=p+q$. בלתי תלויים: $s=p+q-pq$")
         + st.card("s-4", "trap", "⚠️ תא שלילי = נתונים סותרים"))

VIDEO = Video("E03", "events", "הנתונים p, q, s: חיתוך, זרים ובלתי תלויים", [title, idea, ex1, feas, exam, recap],
              bank={"25A-C-Q2f": None, "25A-C-Q2e": None})
