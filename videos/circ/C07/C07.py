# -*- coding: utf-8 -*-
"""C07 · פירקו והרכיבו מעגל חדש — video script (build: tools/video/vid.py C07).

Source: courses/circ/C07.js (lesson + goal). Exam anchors: 24B-B-Q6b (Q2 = (A||B) in series with (C||D||E), all p:
P(Q2) = (2p-p^2)(1-(1-p)^3)) and 24B-B-Q6c (Q1 the bridge of the same units: P(Q1|Q2) = P(Q1∩Q2)/P(Q2) with
P(Q1∩Q2) = 7p^3-9p^4+3p^5, by conditioning on A and B). Open questions (bank key None), used by no guided quiz.
Avoided on purpose: P(Q1) of the bridge (the quiz formula of 24A-C-Q6a / 25A-A-Q4a: never needed here, since the
intersection is computed directly); the quiz items 24A-B-Q6c (C09 boss, Q2 = (A||B)(C||D)), 25A-A-Q4c and
24B-A-Q6b; every C07 quiz case (Q1 = A(B||C), Q2 = B(A||C) at 0.5 -> 0.25, 2/3, 0.5; series vs
parallel at 0.5 -> 1/3) and the lesson's series vs parallel at 0.6 -> 3/7.
Worked example: Q1 = A-B, Q2 = (A||B)-C at p = 0.8: P(Q1∩Q2) = 0.512 = P(ABC), P(Q1|Q2) = 2/3, P(Q2|Q1) = 0.8,
P(Q1∪Q2) = 0.896.
Note: the exam part uses the same conditioning template (on the shared units A, B) that the C09 boss item
24A-B-Q6c needs; its Q2 = (A||B)(C||D) and its numbers are never shown here.
Every number is exact (full truth table, w_circ).
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

# ---------------------------------------------------------------- numbers (verified)
T1 = w.S(w.C("A"), w.C("B"))
T2 = w.S(w.Pa(w.C("A"), w.C("B")), w.C("C"))
PR = w.same("ABC", Fr("0.8"))
q1 = lambda s: w.works(T1, s)
q2 = lambda s: w.works(T2, s)
P1, P2 = w.fprob(q1, PR), w.fprob(q2, PR)
PI = w.fprob(lambda s: q1(s) and q2(s), PR)
assert (P1, P2, PI) == (Fr("0.64"), Fr("0.768"), Fr("0.512"))
assert PI == w.fprob(lambda s: s["A"] and s["B"] and s["C"], PR)        # Q1 ∩ Q2 = A ∩ B ∩ C
assert PI / P2 == Fr(2, 3) and PI / P1 == Fr("0.8") == PR["C"]
assert P1 + P2 - PI == Fr("0.896") == w.fprob(lambda s: q1(s) or q2(s), PR)
assert P1 * P2 != PI and P1 * P2 == Fr("0.49152")                        # the trap: they share A and B
assert w.fprob(q2, PR, given=q1) == Fr("0.8")

# exam 24B-B-Q6b / Q6c
QB, QC = BANK["24B-B-Q6b"], BANK["24B-B-Q6c"]
assert QB["contextId"] == QC["contextId"] == "24B-B-c6"
assert "6p^2-9p^3+5p^4-p^5" in QB["solution"].replace(" ", "") and "3p^5-9p^4+7p^3" in QC["solution"].replace(" ", "")
p = w.p
TB = w.BR("A", "B", "C", "D", "E")                  # A top-left, B top-right, C bottom-left, D bottom-right, E middle
TQ2 = w.S(w.N(w.Pa(w.C("A"), w.C("B")), "ab"), w.N(w.Pa(w.C("C"), w.C("D"), w.C("E")), "cde"))
b1 = lambda s: w.works(TB, s)
b2 = lambda s: w.works(TQ2, s)
U = w.same("ABCDE")
PQ2 = w.sprob(b2, U)
assert w.eq(PQ2, (2 * p - p ** 2) * (1 - (1 - p) ** 3)) and w.eq(PQ2, 6 * p ** 2 - 9 * p ** 3 + 5 * p ** 4 - p ** 5)
both = lambda s: b1(s) and b2(s)
CASES = [((1, 1), p ** 2, 1 - (1 - p) ** 3), ((0, 0), (1 - p) ** 2, 0),
         ((1, 0), p * (1 - p), p * (2 * p - p ** 2)), ((0, 1), p * (1 - p), p * (2 * p - p ** 2))]
for (a, b), pc, cond in CASES:
    assert w.eq(w.sprob(both, U, given=lambda s, a=a, b=b: s["A"] == bool(a) and s["B"] == bool(b)), cond)
for bits in range(8):                                  # the case statements, state by state
    s = {u: bool(bits >> i & 1) for i, u in enumerate("CDE")}
    assert b1({"A": True, "B": True, **s}) and b2({"A": True, "B": True, **s}) == (s["C"] or s["D"] or s["E"])
    assert not b2({"A": False, "B": False, **s})
    assert b1({"A": True, "B": False, **s}) == (s["D"] and (s["C"] or s["E"]))
    assert b1({"A": False, "B": True, **s}) == (s["C"] and (s["D"] or s["E"]))
PI2 = w.sprob(both, U)
assert w.eq(PI2, sum(pc * c for _, pc, c in CASES)) and w.eq(PI2, 7 * p ** 3 - 9 * p ** 4 + 3 * p ** 5)
ANS = w.sprob(b1, U, given=b2)
assert w.eq(ANS, p * (7 - 9 * p + 3 * p ** 2) / (6 - 9 * p + 5 * p ** 2 - p ** 3))
assert w.eq(ANS.subs(p, 1), 1)

# ---------------------------------------------------------------- figures
e1 = w.Circ("e1", T1, scale=1.0)
e2 = w.Circ("e2", T2, scale=1.0)
xb = w.Circ("xb", TB, scale=0.78)
x2 = w.Circ("x2", TQ2, tags={"ab": "2p − p²", "cde": "1 − (1 − p)³"}, scale=0.78)
TAB = w.table("tc", ["", "$P(\\text{case})$", "$P(Q_1\\cap Q_2\\mid\\text{case})$"], [
    ("$A,B$", "$p^2$", "$1-(1-p)^3$"),
    ("$\\overline A,\\overline B$", "$(1-p)^2$", "$0$"),
    ("$A,\\overline B$", "$p(1-p)$", "$p\\,(2p-p^2)$"),
    ("$\\overline A,B$", "$p(1-p)$", "$p\\,(2p-p^2)$")])

STEM = (f'<div class="qstem"><span class="qid">{QC["id"]}</span>$Q_1$ גשר מחמש יחידות, כל אחת $p$. '
        'מפרקים ומרכיבים מאותן יחידות את $Q_2$. אם ידוע ש-$Q_2$ פועל, מה ההסתברות ש-$Q_1$ פועל?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה יש שני מעגלים, שבנויים מאותן יחידות בדיוק."),
    P("נראה למה הם תלויים זה בזה, ואיך מחשבים חיתוך, איחוד והסתברות מותנית ביניהם."),
    P("ובסוף נפתור שני סעיפים אמיתיים ממבחן.", hold=0.4),
], stage='<div class="kicker">C07 · מעגלים חשמליים</div><h1>פירקו והרכיבו מעגל חדש</h1>'
         '<p>לחשב חיתוך, איחוד והסתברות מותנית בין שני מעגלים שנבנו מאותן יחידות.</p>', layout="title")

ex1 = Scene("ex1", "שני מעגלים, אותן יחידות", [
    P("שלוש יחידות, כל אחת פועלת בהסתברות $0.8$. $Q_1$: $A$ ו-$B$ בטור.", do=show("a-0"),
      say="שלוש יחידות, כל אחת פועלת בהסתברות 0.8. קְיוּ אחת: אֵיי ובִּי בטור."),
    P("$Q_2$: $A$ ו-$B$ במקביל, והזוג בטור עם $C$.", say="קְיוּ שתיים: אֵיי ובִּי במקביל, והזוג בטור עם סִי."),
    P("$P(Q_1)$ הוא $0.64$. ו-$P(Q_2)$ הוא $0.96$ כפול $0.8$, כלומר $0.768$.", do=show("a-1"),
      say="ההסתברות של קְיוּ אחת היא 0.64. ושל קְיוּ שתיים: 0.96 כפול 0.8, כלומר 0.768."),
    P("הם **לא** בלתי תלויים: אם $A$ תקולה, היא תקולה בשני המעגלים.", do=show("e1-x-A", "e2-x-A", "a-t"),
      say="הם לא בלתי תלויים: אם אֵיי תקולה, היא תקולה בשני המעגלים."),
    P("לכן את החיתוך לא מכפילים. שואלים: באילו מצבים של היחידות שניהם פועלים?", do=hide("e1-x-A", "e2-x-A")),
    P("$Q_1$ דורש את $A$ ואת $B$. ואז הזוג המקבילי ב-$Q_2$ כבר פועל, ונשאר רק $C$.",
      do=show("e1-ok-A", "e1-ok-B", "e2-ok-A", "e2-ok-B"),
      say="קְיוּ אחת דורש את אֵיי ואת בִּי. ואז הזוג המקבילי בקְיוּ שתיים כבר פועל, ונשאר רק סִי."),
    P("אז שניהם פועלים בדיוק כששלוש היחידות פועלות: $0.8$ בשלישית, כלומר $0.512$.", do=show("e2-ok-C", "e1-on", "e2-on", "a-2"),
      say="אז שניהם פועלים בדיוק כששלוש היחידות פועלות: 0.8 בשלישית, כלומר 0.512."),
    P("מכפלה הייתה נותנת $0.49$ בקירוב. זה לא אותו דבר.", say="מכפלה הייתה נותנת 0.49 בקירוב. זה לא אותו דבר.", hold=0.3),
    P("ועכשיו הכיוון. אם ידוע ש-$Q_2$ פועל: $0.512$ חלקי $0.768$, כלומר שני שלישים.", do=show("a-3"),
      say="ועכשיו הכיוון. אם ידוע שקְיוּ שתיים פועל: 0.512 חלקי 0.768, כלומר שני שלישים."),
    P("ואם ידוע ש-$Q_1$ פועל: $0.512$ חלקי $0.64$, כלומר $0.8$. בדיוק הסיכוי של $C$.", do=show("a-4"),
      say="ואם ידוע שקְיוּ אחת פועל: 0.512 חלקי 0.64, כלומר 0.8. בדיוק הסיכוי של סִי."),
    P("ולפחות אחד מהם פועל: סכום פחות חיתוך, $0.896$.", do=show("a-5"), say="ולפחות אחד מהם פועל: סכום פחות חיתוך, 0.896.",
      hold=0.4),
], stage=f'<div class="circ-stack">{e1.svg()}{e2.svg()}</div>',
   panel=st.card("a-0", "plain", "$p=0.8$ לכל יחידה")
         + st.card("a-1", "plain", "$P(Q_1)=0.64,\\ P(Q_2)=0.768$")
         + st.card("a-t", "trap", "⚠️ יחידות משותפות: $P(Q_1\\cap Q_2)\\ne P(Q_1)P(Q_2)$")
         + st.card("a-2", "ex", "$Q_1\\cap Q_2=A\\cap B\\cap C$: $0.512$")
         + st.card("a-3", "plain", "$P(Q_1\\mid Q_2)=\\frac{0.512}{0.768}=\\frac23$")
         + st.card("a-4", "plain", "$P(Q_2\\mid Q_1)=\\frac{0.512}{0.64}=0.8$")
         + st.card("a-5", "plain", "$P(Q_1\\cup Q_2)=0.64+0.768-0.512=0.896$"))

rule = Scene("rule", "שיטה", [
    P("השיטה הכללית: את החיתוך מחשבים בהתניה על היחידות שמשנות הכי הרבה.", do=show("r-1")),
    P("בכל מקרה כותבים מה צריך כדי ששני המעגלים יפעלו, ומשקללים בהסתברות שלמה.", do=show("r-2")),
    P("ואחר כך הנוסחאות: מותנית היא חיתוך חלקי מה שידוע, ואיחוד הוא סכום פחות חיתוך.", do=show("r-3")),
    P("והכיוון חשוב: המכנה הוא תמיד המעגל שידוע שפועל.", do=show("r-4"), hold=0.4),
], stage='<div class="circ-stack"><div class="circ-big">$P(Q_1\\mid Q_2)=\\dfrac{P(Q_1\\cap Q_2)}{P(Q_2)}$</div>'
         '<div class="circ-mid">$P(Q_1\\cup Q_2)=P(Q_1)+P(Q_2)-P(Q_1\\cap Q_2)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 מתנים על היחידות המשותפות")
         + st.card("r-2", "rule", "🔑 הסתברות שלמה על המקרים")
         + st.card("r-3", "rule", "🔑 מותנית ואיחוד מהחיתוך")
         + st.card("r-4", "trap", "⚠️ $P(Q_1\\mid Q_2)\\ne P(Q_2\\mid Q_1)$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: $Q_1$ הוא גשר מחמש יחידות, כל אחת פועלת בהסתברות $p$.",
      say="שאלה ממבחן: קְיוּ אחת הוא גשר מחמש יחידות, כל אחת פועלת בהסתברות פִּי."),
    P("מפרקים אותו, ומאותן יחידות בונים את $Q_2$: $A$ במקביל ל-$B$, בטור עם שלוש במקביל.",
      say="מפרקים אותו, ומאותן יחידות בונים את קְיוּ שתיים: אֵיי במקביל לבִּי, בטור עם שלוש במקביל."),
    P("סעיף ראשון: $P(Q_2)$. שני בלוקים בטור: הזוג פועל ב-$2p-p^2$.", do=hide("xr0") + show("xs", "x2-blk-ab", "x2-bt-ab"),
      say="סעיף ראשון: ההסתברות של קְיוּ שתיים. שני בלוקים בטור: הזוג פועל בשתיים פִּי פחות פִּי בריבוע."),
    P("והשלישייה נכשלת רק כשכולן נכשלות, ולכן היא פועלת ב-$1-(1-p)^3$.", do=show("x2-blk-cde", "x2-bt-cde", "x-1"),
      say="והשלישייה נכשלת רק כשכולן נכשלות, ולכן היא פועלת באחת פחות, בסוגריים אחת פחות פִּי, בשלישית."),
    P("סעיף שני: אם $Q_2$ פועל, מה הסיכוי ש-$Q_1$ פועל? המכנה הוא $P(Q_2)$, והמונה הוא החיתוך.",
      say="סעיף שני: אם קְיוּ שתיים פועל, מה הסיכוי שקְיוּ אחת פועל? המכנה הוא ההסתברות של קְיוּ שתיים, והמונה הוא החיתוך."),
    P("את החיתוך מחשבים בהתניה על $A$ ו-$B$, כי הן קובעות את הזוג של $Q_2$ וגם את הדרך העליונה בגשר.",
      say="את החיתוך מחשבים בהתניה על אֵיי ובִּי, כי הן קובעות את הזוג של קְיוּ שתיים וגם את הדרך העליונה בגשר."),
    P("שתיהן פועלות: הגשר פועל דרך הדרך העליונה, ו-$Q_2$ צריך רק אחת משלוש.",
      do=show("tc-r-0", "xb-ok-A", "xb-ok-B"), say="שתיהן פועלות: הגשר פועל דרך הדרך העליונה, וקְיוּ שתיים צריך רק אחת משלוש."),
    P("שתיהן תקולות: הזוג של $Q_2$ נופל, והחיתוך הוא אפס.", do=hide("xb-ok-A", "xb-ok-B") + show("tc-r-1", "xb-x-A", "xb-x-B"),
      say="שתיהן תקולות: הזוג של קְיוּ שתיים נופל, והחיתוך הוא אפס."),
    P("רק $A$ פועלת: בגשר צריך את $D$, וגם $C$ או $E$. וזה כבר מבטיח את השלישייה של $Q_2$.",
      do=hide("xb-x-A") + show("tc-r-2", "xb-ok-A", "xb-ok-D"),
      say="רק אֵיי פועלת: בגשר צריך את דִּי, וגם סִי או אִי. וזה כבר מבטיח את השלישייה של קְיוּ שתיים."),
    P("ורק $B$ פועלת: בסימטריה, $C$, וגם $D$ או $E$.", do=hide("xb-ok-A", "xb-ok-D", "xb-x-B") + show("tc-r-3", "xb-x-A", "xb-ok-B", "xb-ok-C"),
      say="ורק בִּי פועלת: בסימטריה, סִי, וגם דִּי או אִי."),
    P("משקללים את ארבעת המקרים, ומקבלים $7p^3-9p^4+3p^5$.", do=hide("xb-x-A", "xb-ok-B", "xb-ok-C") + show("x-3"),
      say="משקללים את ארבעת המקרים, ומקבלים שבע פִּי בשלישית, פחות תשע פִּי בחזקת ארבע, ועוד שלוש פִּי בחזקת חמש."),
    P("מחלקים ב-$P(Q_2)$, ומצמצמים $p^2$. זו התשובה.", do=show("x-4"),
      say="מחלקים בהסתברות של קְיוּ שתיים, ומצמצמים פִּי בריבוע. זו התשובה.", hold=0.3),
    P("שימו לב: לא חישבנו בכלל את $P(Q_1)$. החיתוך והמכנה הספיקו.", say="שימו לב: לא חישבנו בכלל את ההסתברות של קְיוּ אחת. החיתוך והמכנה הספיקו."),
    P("המלכודת: לכתוב שהחיתוך הוא $P(Q_1)$ כפול $P(Q_2)$. אבל אלה אותן יחידות בדיוק.", do=show("x-t"),
      say="המלכודת: לכתוב שהחיתוך הוא ההסתברות של קְיוּ אחת כפול זו של קְיוּ שתיים. אבל אלה אותן יחידות בדיוק.", hold=0.5),
], stage='<div class="circ-stack">'
         + '<div class="circ-swap" style="--swap-h:330px"><div id="xr0">'
         + st.raster("xr", "images/exams/24B-B-Q6-circuits.png", 640, (1076, 526))
         + f'</div><div id="xs" class="h"><div class="circ-row" style="gap:20px">{xb.svg()}{x2.svg()}</div></div></div>'
         + f'{TAB}</div>',
   panel=STEM
         + st.card("x-1", "plain", "$P(Q_2)=(2p-p^2)\\,[1-(1-p)^3]$")
         + st.card("x-3", "ex", "$P(Q_1\\cap Q_2)=7p^3-9p^4+3p^5$")
         + st.card("x-4", "rule", "🔑 $\\dfrac{p\\,(7-9p+3p^2)}{6-9p+5p^2-p^3}$")
         + st.card("x-t", "trap", "⚠️ לא $P(Q_1)P(Q_2)$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: שני מעגלים מאותן יחידות הם תלויים, ולכן את החיתוך לא מכפילים.", do=show("r-a")),
    P("מתנים על היחידות המשותפות, ובכל מקרה בודקים מה צריך כדי ששניהם יפעלו.", do=show("r-b")),
    P("מותנית: חיתוך חלקי המעגל שידוע שפועל. איחוד: סכום פחות חיתוך.", do=show("r-c")),
    P("ואם מעגל אחד מוכל בשני, החיתוך הוא פשוט הקטן מביניהם. נתראה ברמה הבאה.", do=show("r-d"), hold=0.6),
], stage='<div class="circ-stack"><div class="circ-big">$P(Q_1\\cap Q_2)=\\sum_k P(\\text{case}_k)\\,P(Q_1\\cap Q_2\\mid\\text{case}_k)$</div></div>',
   panel=st.card("r-a", "trap", "⚠️ $P(Q_1\\cap Q_2)\\ne P(Q_1)P(Q_2)$")
         + st.card("r-b", "rule", "🔑 התניה על היחידות המשותפות")
         + st.card("r-c", "rule", "🔑 מותנית ואיחוד מתוך החיתוך")
         + st.card("r-d", "rule", "🔑 $Q_1\\subseteq Q_2\\ \\Rightarrow\\ P(Q_1\\cap Q_2)=P(Q_1)$"))

VIDEO = Video("C07", "circ", "פירקו והרכיבו מעגל חדש", [title, ex1, rule, exam, recap],
              bank={"24B-B-Q6b": None, "24B-B-Q6c": None})
