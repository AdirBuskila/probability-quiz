# -*- coding: utf-8 -*-
"""C06 · בייס במעגלים: אם ידוע שהמעגל פועל — video script (build: tools/video/vid.py C06).

Source: courses/circ/C06.js (lesson + goal). Exam anchor: 24A-E-Q6d (Q1 = D in series with (A-B || C), Q2 = D in
series with (C-B || A), all p; given that both circuits work, the probability that all four units work)
= p^4 / P(Q1 ∩ Q2) = p/(3-2p). Open question (bank key None), used by no guided quiz.
Avoided on purpose: P(Q1) of that question (24A-E-Q6a = p^2(1+p-p^2) is the twin of the C03 quiz item 24B-A-Q6a),
so the denominator is computed directly as "D and at least two of A, B, C", never through P(Q1); every C06 quiz case
(series 0.7 -> 1, parallel 0.6 -> 5/7, A(B||C) 0.9/0.5/0.8 -> 5/9, the findbug, all|S for A(B||C) at 0.6 -> 3/7,
24S-A-Q6d) and the lesson's parallel 0.5 -> 2/3 and 1/(2-p).
Worked example: A || (B-C) with P(A)=0.5, P(B)=P(C)=0.8: P(S)=0.82, P(A|S)=25/41, P(B|S)=36/41.
Every number is exact (full truth table, w_circ).
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

# ---------------------------------------------------------------- numbers (verified)
TE = w.Pa(w.C("A"), w.S(w.C("B"), w.C("C")))
PR = {"A": Fr("0.5"), "B": Fr("0.8"), "C": Fr("0.8")}
ok = lambda s: w.works(TE, s)
PS = w.fprob(ok, PR)
assert PS == 1 - Fr("0.5") * (1 - Fr("0.64")) == Fr("0.82")
assert w.fprob(lambda s: s["A"] and ok(s), PR) == PR["A"]                 # A alone makes the circuit work
PA = w.fprob(lambda s: s["A"], PR, given=ok)
assert PA == Fr("0.5") / Fr("0.82") == Fr(25, 41) and PA > PR["A"]
assert w.fprob(ok, PR, given=lambda s: s["B"]) == Fr("0.9")              # B works: A || C
PB = w.fprob(lambda s: s["B"], PR, given=ok)
assert PB == Fr("0.72") / Fr("0.82") == Fr(36, 41) and PB > PR["B"]
assert w.fprob(lambda s: s["A"], PR, given=lambda s: s["A"]) == 1         # the reversed P(S|A) = 1 is a different thing
assert w.fprob(ok, PR, given=lambda s: s["A"]) == 1

# exam 24A-E-Q6d
Q = BANK["24A-E-Q6d"]
assert Q["contextId"] == "24A-E-c6" and "\\frac{p}{3-2p}" in Q["solution"].replace(" ", "")
p = w.p
T1 = w.S(w.C("D"), w.Pa(w.S(w.C("A"), w.C("B")), w.C("C")))
T2 = w.S(w.C("D"), w.Pa(w.S(w.C("C"), w.C("B")), w.C("A")))
both = lambda s: w.works(T1, s) and w.works(T2, s)
two = lambda s: s["D"] and (s["A"] + s["B"] + s["C"]) >= 2
for bits in range(16):                                                     # both circuits = D and at least two of A,B,C
    s = {u: bool(bits >> i & 1) for i, u in enumerate("ABCD")}
    assert bool(both(s)) == bool(two(s))
PBOTH = w.sprob(both, w.same("ABCD"))
assert w.eq(PBOTH, p * (3 * p ** 2 - 2 * p ** 3)) and w.eq(PBOTH, p ** 3 * (3 - 2 * p))
assert w.eq(w.sprob(lambda s: all(s.values()), w.same("ABCD"), given=both), p / (3 - 2 * p))
P1 = w.sprob(lambda s: w.works(T1, s), w.same("ABCD"))
P2 = w.sprob(lambda s: w.works(T2, s), w.same("ABCD"))
assert not w.eq(PBOTH, P1 * P2)                                            # the trap: the circuits share units
assert w.eq((p / (3 - 2 * p)).subs(p, 1), 1) and (p / (3 - 2 * p)).subs(p, Fr(1, 2)) == Fr(1, 4)

# ---------------------------------------------------------------- figures
ce = w.Circ("ce", TE, probs={k: f"{float(v):g}" for k, v in PR.items()}, scale=1.15)
q1 = w.Circ("q1", T1, scale=0.8)
q2 = w.Circ("q2", T2, scale=0.8)

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>ארבע יחידות $A,B,C,D$, כל אחת פועלת בהסתברות $p$ '
        'בלי תלות. מהן הורכבו שני המעגלים שבאיור. אם ידוע ששני המעגלים פועלים, מה ההסתברות שכל הרכיבים תקינים?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נהפוך את הכיוון: ידוע שהמעגל פועל, ושואלים מה זה אומר על היחידות."),
    P("נראה איך משתמשים בהסתברות מותנית ובבייס, ואיזה מכנה הכי קל לפספס."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">C06 · מעגלים חשמליים</div><h1>בייס במעגלים: אם ידוע שהמעגל פועל</h1>'
         '<p>לחשב את ההסתברות שיחידה פועלת (או כולן, או לא) בהינתן שהמעגל כולו פועל.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("השאלה: אם ידוע שהמעגל פועל, מה ההסתברות שיחידה $X$ פועלת?", say="השאלה: אם ידוע שהמעגל פועל, מה ההסתברות שיחידה אִקְס פועלת?"),
    P("זו הסתברות מותנית. והמכנה הוא תמיד מה שידוע: $P(S)$.", do=show("i-1"), say="זו הסתברות מותנית. והמכנה הוא תמיד מה שידוע: פִּי של אֶס."),
    P("במונה: החיתוך, ש-$X$ פועלת וגם המעגל פועל.", say="במונה: החיתוך, שאִקְס פועלת וגם המעגל פועל."),
    P("ואת החיתוך מחשבים כך: מניחים ש-$X$ פועלת, מחשבים את המעגל שנשאר, וכופלים ב-$P(X)$.", do=show("i-2"),
      say="ואת החיתוך מחשבים כך: מניחים שאִקְס פועלת, מחשבים את המעגל שנשאר, וכופלים בהסתברות של אִקְס."),
    P("שלושה צעדים: המכנה, המונה, וחילוק.", do=show("i-r"), hold=0.4),
], stage='<div class="circ-stack"><div class="circ-big">$P(X\\mid S)=\\dfrac{P(X\\cap S)}{P(S)}$</div></div>',
   panel=st.card("i-1", "rule", "🔑 המכנה: מה שידוע, $P(S)$")
         + st.card("i-2", "rule", "🔑 $P(X\\cap S)=P(X)\\cdot P(S\\mid X)$")
         + st.card("i-r", "ex", "(1) $P(S)$ &nbsp; (2) $P(X\\cap S)$ &nbsp; (3) מחלקים"))

ex1 = Scene("ex1", "דוגמה", [
    P("המעגל: $A$ במקביל לטור של $B$ ו-$C$. $A$ עם $0.5$, ו-$B$, $C$ עם $0.8$.",
      say="המעגל: אֵיי במקביל לטור של בִּי וסִי. אֵיי עם 0.5, ובִּי, סִי עם 0.8."),
    P("צעד ראשון, המכנה. הטור פועל בהסתברות $0.64$, ולכן הוא נכשל ב-$0.36$.",
      say="צעד ראשון, המכנה. הטור פועל בהסתברות 0.64, ולכן הוא נכשל ב0.36."),
    P("המעגל נכשל כש-$A$ נכשלת וגם הטור: $0.5$ כפול $0.36$, כלומר $0.18$. ולכן $P(S)$ הוא $0.82$.", do=show("a-1"),
      say="המעגל נכשל כשאֵיי נכשלת וגם הטור: 0.5 כפול 0.36, כלומר 0.18. ולכן פִּי של אֶס היא 0.82."),
    P("שאלה ראשונה: מה ההסתברות ש-$A$ פועלת, אם ידוע שהמעגל פועל?", do=show("ce-ok-A"),
      say="שאלה ראשונה: מה ההסתברות שאֵיי פועלת, אם ידוע שהמעגל פועל?"),
    P("אם $A$ פועלת, המעגל פועל בוודאות. לכן החיתוך הוא פשוט $P(A)$, כלומר $0.5$.", do=show("ce-on", "a-2"),
      say="אם אֵיי פועלת, המעגל פועל בוודאות. לכן החיתוך הוא פשוט ההסתברות של אֵיי, כלומר 0.5."),
    P("מחלקים: $0.5$ חלקי $0.82$, כלומר $25$ חלקי $41$, בערך $0.61$.", do=show("a-3"),
      say="מחלקים: 0.5 חלקי 0.82, כלומר עשרים וחמש חלקי ארבעים ואחת, בערך 0.61.", hold=0.3),
    P("שאלה שנייה: ומה עם $B$? מניחים ש-$B$ פועלת.", do=hide("ce-ok-A", "ce-on") + show("ce-ok-B"),
      say="שאלה שנייה: ומה עם בִּי? מניחים שבִּי פועלת."),
    P("אז נשאר $A$ במקביל ל-$C$: אחת פחות $0.5$ כפול $0.2$, כלומר $0.9$.", do=show("a-4"),
      say="אז נשאר אֵיי במקביל לסִי: אחת פחות 0.5 כפול 0.2, כלומר 0.9."),
    P("החיתוך: $0.8$ כפול $0.9$, כלומר $0.72$. וחלקי $0.82$: $36$ חלקי $41$, בערך $0.88$.", do=show("a-5"),
      say="החיתוך: 0.8 כפול 0.9, כלומר 0.72. וחלקי 0.82: שלושים ושש חלקי ארבעים ואחת, בערך 0.88.", hold=0.3),
    P("שימו לב: שתי התוצאות גדולות מההסתברות המקורית. כשהיחידות בלתי תלויות, הידיעה שהמעגל פועל היא חדשות טובות על כל יחידה.",
      do=show("a-6")),
    P("ומקרה קיצון: יחידה שבטור עם כל המעגל. אם המעגל פועל, היא חייבת לפעול, וההסתברות היא אחת.", do=show("a-7"),
      hold=0.4),
], stage=f'<div class="circ-stack">{ce.svg()}</div>',
   panel=st.card("a-1", "plain", "$P(S)=1-0.5\\cdot0.36=0.82$")
         + st.card("a-2", "plain", "$P(A\\cap S)=P(A)=0.5$")
         + st.card("a-3", "ex", "$P(A\\mid S)=\\frac{0.5}{0.82}=\\frac{25}{41}\\approx0.61$")
         + st.card("a-4", "plain", "$P(S\\mid B)=1-0.5\\cdot0.2=0.9$")
         + st.card("a-5", "ex", "$P(B\\mid S)=\\frac{0.8\\cdot0.9}{0.82}=\\frac{36}{41}\\approx0.88$")
         + st.card("a-6", "rule", "🔑 $P(X\\mid S)\\ge P(X)$ (ליחידות בלתי תלויות)")
         + st.card("a-7", "rule", "🔑 יחידה בטור עם הכול: $P(X\\mid S)=1$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: ארבע יחידות, כל אחת פועלת בהסתברות $p$. מהן הרכיבו שני מעגלים.",
      say="שאלה ממבחן: ארבע יחידות, כל אחת פועלת בהסתברות פִּי. מהן הרכיבו שני מעגלים."),
    P("בראשון $A$ ו-$B$ בטור, ובמקביל להן $C$; והבלוק הזה בטור עם $D$.",
      say="בראשון אֵיי ובִּי בטור, ובמקביל להן סִי; והבלוק הזה בטור עם דִּי."),
    P("בשני מחליפים את התפקידים של $A$ ו-$C$.", say="בשני מחליפים את התפקידים של אֵיי וסִי."),
    P("ידוע ששני המעגלים פועלים. מה ההסתברות שכל ארבע היחידות תקינות?"),
    P("המאורע הידוע הוא ששניהם פועלים. הוא המכנה.", do=show("x-1")),
    P("המונה קל: אם כל ארבע תקינות, שני המעגלים בוודאי פועלים. ולכן החיתוך הוא $p^4$.",
      do=show("q1-ok-A", "q1-ok-B", "q1-ok-C", "q1-ok-D", "q2-ok-A", "q2-ok-B", "q2-ok-C", "q2-ok-D", "x-2"),
      say="המונה קל: אם כל ארבע תקינות, שני המעגלים בוודאי פועלים. ולכן החיתוך הוא פִּי בחזקת ארבע."),
    P("עכשיו המכנה. $D$ בטור בשני המעגלים, ולכן היא חייבת לפעול.",
      do=hide("q1-ok-A", "q1-ok-B", "q1-ok-C", "q2-ok-A", "q2-ok-B", "q2-ok-C"),
      say="עכשיו המכנה. דִּי בטור בשני המעגלים, ולכן היא חייבת לפעול."),
    P("ומ-$A$, $B$, $C$: הטענה היא ששני המעגלים פועלים בדיוק כשלפחות שתיים מהן פועלות.",
      say="ומאֵיי, בִּי, סִי: הטענה היא ששני המעגלים פועלים בדיוק כשלפחות שתיים מהן פועלות."),
    P("אם רק $A$ פועלת, המעגל הראשון נופל. אם רק $C$, השני נופל. ואם רק $B$, שניהם.",
      do=show("q1-ok-A", "q1-x-B", "q1-x-C", "q1-off"),
      say="אם רק אֵיי פועלת, המעגל הראשון נופל. אם רק סִי, השני נופל. ואם רק בִּי, שניהם."),
    P("ואם שתיים פועלות, כל זוג מספיק לשניהם. למשל $B$ ו-$C$: בראשון דרך $C$, ובשני דרך $C$ ו-$B$.",
      do=hide("q1-ok-A", "q1-x-B", "q1-x-C", "q1-off") + show("q1-ok-B", "q1-ok-C", "q2-ok-B", "q2-ok-C", "q1-x-A", "q2-x-A"),
      say="ואם שתיים פועלות, כל זוג מספיק לשניהם. למשל בִּי וסִי: בראשון דרך סִי, ובשני דרך סִי ובִּי."),
    P("לפחות שתיים מתוך שלוש: $3p^2(1-p)$ ועוד $p^3$, כלומר $3p^2-2p^3$.", do=show("x-3"),
      say="לפחות שתיים מתוך שלוש: שלוש פִּי בריבוע כפול אחת פחות פִּי, ועוד פִּי בשלישית. כלומר שלוש פִּי בריבוע פחות שתיים פִּי בשלישית."),
    P("וכפול $p$ בשביל $D$: המכנה הוא $p^3$ כפול $3-2p$.", do=show("x-4"),
      say="וכפול פִּי בשביל דִּי: המכנה הוא פִּי בשלישית, כפול שלוש פחות שתיים פִּי."),
    P("מחלקים: $p^4$ חלקי $p^3(3-2p)$, וזה $p$ חלקי $3-2p$.", do=show("x-5"),
      say="מחלקים: פִּי בחזקת ארבע חלקי פִּי בשלישית כפול שלוש פחות שתיים פִּי, וזה פִּי חלקי שלוש פחות שתיים פִּי.", hold=0.3),
    P("בדיקה: אם $p$ שווה אחת, יוצא אחת, כמו שצריך.", say="בדיקה: אם פִּי שווה אחת, יוצא אחת, כמו שצריך."),
    P("המלכודת: לכתוב במכנה $P(Q_1)$ כפול $P(Q_2)$. המעגלים בנויים מאותן יחידות, ולכן הם תלויים.", do=show("x-t"),
      say="המלכודת: לכתוב במכנה את ההסתברות של קְיוּ אחת כפול ההסתברות של קְיוּ שתיים. המעגלים בנויים מאותן יחידות, ולכן הם תלויים.",
      hold=0.5),
], stage='<div class="circ-stack">'
         + '<div class="circ-row">' + st.raster("xr", "images/exams/24A-E-Q6-circuits.png", 190, (432, 702))
         + f'<div class="circ-stack" style="width:auto;gap:4px">{q1.svg()}{q2.svg()}</div></div>'
         + st.card("x-4", "ex", "$P(Q_1\\cap Q_2)=p\\,(3p^2-2p^3)=p^3(3-2p)$")
         + st.card("x-5", "rule", "🔑 $\\dfrac{p^4}{p^3(3-2p)}=\\dfrac{p}{3-2p}$") + '</div>',
   panel=STEM
         + st.card("x-1", "plain", "מכנה: $P(Q_1\\cap Q_2)$")
         + st.card("x-2", "plain", "מונה: $P(\\text{all})=p^4$")
         + st.card("x-3", "plain", "$D$, ולפחות 2 מ-$A,B,C$")
         + st.card("x-t", "trap", "⚠️ לא $P(Q_1)P(Q_2)$: יחידות משותפות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: אם ידוע שהמעגל פועל, המכנה הוא תמיד ההסתברות של מה שידוע.", do=show("r-1")),
    P("את המונה מחשבים בהנחה שהיחידה פועלת: מצמצמים את המעגל שנשאר, וכופלים בהסתברות שלה.", do=show("r-2")),
    P("וכשהמאורע במונה גורר את מה שידוע, כמו כל היחידות פועלות, המונה הוא פשוט ההסתברות שלו.", do=show("r-3")),
    P("ואל תכפילו מעגלים שחולקים יחידות: הם תלויים. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="circ-stack"><div class="circ-big">$P(X\\mid S)=\\dfrac{P(X)\\,P(S\\mid X)}{P(S)}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 המכנה: $P(S)$")
         + st.card("r-2", "rule", "🔑 המונה: $P(X)\\cdot P(S\\mid X)$")
         + st.card("r-3", "rule", "🔑 $A\\subseteq S\\ \\Rightarrow\\ P(A\\cap S)=P(A)$")
         + st.card("r-4", "trap", "⚠️ מעגלים עם יחידות משותפות תלויים"))

VIDEO = Video("C06", "circ", "בייס במעגלים: אם ידוע שהמעגל פועל", [title, idea, ex1, exam, recap],
              bank={"24A-E-Q6d": None})
