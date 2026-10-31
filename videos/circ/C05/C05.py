# -*- coding: utf-8 -*-
"""C05 · הגשר: מתנים על היחידה האמצעית — video script (build: tools/video/vid.py C05).

Source: courses/circ/C05.js (lesson + goal). Exam anchor: 24B-C-Q6c (a five-unit bridge, all p: given that exactly
one unit does not work, the probability that the circuit works) = 1. Open question (bank key None), used by no
guided quiz.
Avoided on purpose: the bridge formula P(S) = p^2(2+2p-5p^2+2p^3) for equal p — it is the answer of the quiz items
24A-C-Q6a (C05) and 25A-A-Q4a (C09 boss), so it never appears here, and neither do its bank twins (24A-A/B/D-Q6a,
24B-B-Q6a, 24B-C-Q6a, 25A-B-Q4a, 25S-C-Q5a); 24B-C-Q6b (its answer needs that formula as denominator); the C05
quiz cases (E works -> (A||C)(B||D) as an MCQ, the 0.8 bridge 0.9216/0.8704/0.91136, the 0.5 bridge) and the
lesson's 0.9 bridge.
Worked example: a bridge with five different units A=0.9, B=0.8, C=0.7, D=0.6, E=0.5: 0.8924 | 0.8376 -> 0.865.
Every number is exact (full truth table, w_circ).
"""
from fractions import Fraction as Fr
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

# ---------------------------------------------------------------- numbers (verified)
TB = w.BR("A", "B", "C", "D", "E")            # A top-left, B top-right, C bottom-left, D bottom-right, E middle
PR = {"A": Fr("0.9"), "B": Fr("0.8"), "C": Fr("0.7"), "D": Fr("0.6"), "E": Fr("0.5")}
works = lambda s: w.works(TB, s)
on = w.fprob(works, PR, given=lambda s: s["E"])
off = w.fprob(works, PR, given=lambda s: not s["E"])
tot = w.fprob(works, PR)
pa = lambda *k: 1 - eval("*".join(f"(1-PR['{x}'])" for x in k))
assert on == pa("A", "C") * pa("B", "D") == Fr("0.97") * Fr("0.92") == Fr("0.8924")
assert off == 1 - (1 - PR["A"] * PR["B"]) * (1 - PR["C"] * PR["D"]) == 1 - Fr("0.28") * Fr("0.58") == Fr("0.8376")
assert tot == PR["E"] * on + (1 - PR["E"]) * off == Fr("0.865")
assert off < tot < on                                                    # the weighted mean sits between the cases
# E as a wire: (A||C)(B||D); E cut: AB || CD -- checked state by state, not only in probability
for bits in range(16):
    s = {u: bool(bits >> i & 1) for i, u in enumerate("ABCD")}
    assert works({**s, "E": True}) == ((s["A"] or s["C"]) and (s["B"] or s["D"]))
    assert works({**s, "E": False}) == ((s["A"] and s["B"]) or (s["C"] and s["D"]))
assert not works({"A": True, "B": False, "C": False, "D": True, "E": False})    # A and D alone need E
assert works({"A": True, "B": False, "C": False, "D": True, "E": True})

# exam 24B-C-Q6c: A, B on the left (top/bottom), C, D on the right (top/bottom), E between top and bottom
Q = BANK["24B-C-Q6c"]
assert Q["contextId"] == "24B-C-c6" and "=1" in Q["solution"].replace(" ", "")
TX = w.BR("A", "C", "B", "D", "E")
p = w.p
one = lambda s: sum(not v for v in s.values()) == 1
assert w.sprob(lambda s: w.works(TX, s), w.same("ABCDE"), given=one) == 1
assert w.eq(w.sprob(one, w.same("ABCDE")), 5 * p ** 4 * (1 - p))          # what the trap would answer
for u in "ABCDE":                                                          # every single failure leaves a path
    assert w.works(TX, {x: x != u for x in "ABCDE"})
assert not w.works(TX, {"A": False, "B": False, "C": True, "D": True, "E": True})   # two can cut it (A, B)
PATH = {"A": ("B", "D"), "B": ("A", "C"), "C": ("B", "D"), "D": ("A", "C"), "E": ("A", "C")}
for u, (a, b) in PATH.items():
    s = {x: x in (a, b) for x in "ABCDE"}
    assert w.works(TX, s) and u not in (a, b)

# ---------------------------------------------------------------- figures
PL = {k: f"{float(v):g}" for k, v in PR.items()}
c0 = w.Circ("c0", TB, scale=1.0)
cb = w.Circ("cb", TB, probs=PL, scale=0.95)
cx = w.Circ("cx", TX, scale=0.9)

STEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>מעגל גשר מחמש יחידות בלתי תלויות, כל אחת פועלת '
        'בהסתברות $p$. ידוע שבדיוק יחידה אחת <b>לא</b> פועלת, ולא ידוע איזו. מה ההסתברות שהמעגל פועל?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את המעגל שמופיע כמעט בכל מבחן: הגשר."),
    P("נראה למה הצמצום של טור ומקביל נתקע בו, ואיך התניה על יחידה אחת פותרת הכול."),
    P("ובסוף נפתור סעיף אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">C05 · מעגלים חשמליים</div><h1>הגשר: מתנים על היחידה האמצעית</h1>'
         '<p>לחשב את ההסתברות שמעגל גשר פועל על ידי התניה על היחידה האמצעית (הסתברות שלמה).</p>', layout="title")

idea = Scene("idea", "למה זה נתקע", [
    P("זה הגשר: $A$ ו-$B$ בדרך העליונה, $C$ ו-$D$ בדרך התחתונה.", say="זה הגשר: אֵיי ובִּי בדרך העליונה, סִי ודִּי בדרך התחתונה."),
    P("ו-$E$ באמצע, מחברת בין שתי הדרכים.", do=show("c0-ok-E"), say="ואִי באמצע, מחברת בין שתי הדרכים."),
    P("נסו למצוא כאן בלוק. $A$ ו-$B$ לא בטור נקי, כי $E$ יוצאת מהנקודה שביניהן.", do=hide("c0-ok-E") + show("c0-ok-A", "c0-ok-B"),
      say="נסו למצוא כאן בלוק. אֵיי ובִּי לא בטור נקי, כי אִי יוצאת מהנקודה שביניהן."),
    P("וגם $A$ ו-$C$ לא במקביל נקי. אין אף בלוק, והצמצום נתקע.", do=hide("c0-ok-B") + show("c0-ok-C", "i-1"),
      say="וגם אֵיי וסִי לא במקביל נקי. אין אף בלוק, והצמצום נתקע."),
    P("למשל: $A$ ו-$D$ פועלות, $B$ ו-$C$ לא. האם יש זרם? רק אם $E$ פועלת.",
      do=hide("c0-ok-C") + show("c0-ok-A", "c0-ok-D", "c0-x-B", "c0-x-C"),
      say="למשל: אֵיי ודִּי פועלות, בִּי וסִי לא. האם יש זרם? רק אם אִי פועלת."),
    P("כלומר הכול תלוי ב-$E$. אז נקבע את המצב שלה, ונפריד לשני מקרים.", do=show("i-r1"),
      say="כלומר הכול תלוי באִי. אז נקבע את המצב שלה, ונפריד לשני מקרים."),
    P("זו נוסחת ההסתברות השלמה, כשהחלוקה היא: $E$ פועלת, או $E$ לא פועלת.", do=show("i-r2"),
      say="זו נוסחת ההסתברות השלמה, כשהחלוקה היא: אִי פועלת, או אִי לא פועלת.", hold=0.4),
], stage=f'<div class="circ-stack">{c0.svg()}</div>',
   panel=st.card("i-1", "plain", "אין בלוק נקי של טור או מקביל")
         + st.card("i-r1", "rule", "🔑 מתנים על היחידה האמצעית $E$")
         + st.card("i-r2", "rule", "🔑 $P(S)=P(E)P(S\\mid E)+P(\\overline E)P(S\\mid\\overline E)$"))

cases = Scene("cases", "שני המקרים", [
    P("נחשב גשר עם חמש יחידות שונות: $0.9$, $0.8$, $0.7$, $0.6$, ו-$E$ עם $0.5$.",
      say="נחשב גשר עם חמש יחידות שונות: 0.9, 0.8, 0.7, 0.6, ואִי עם 0.5."),
    P("מקרה ראשון: $E$ פועלת. היא כמו חוט, ושתי הנקודות האמצעיות הופכות לנקודה אחת.",
      do=hide("cb-u-E") + show("cb-w-E", "a-0"), say="מקרה ראשון: אִי פועלת. היא כמו חוט, ושתי הנקודות האמצעיות הופכות לנקודה אחת."),
    P("משמאל $A$ ו-$C$ מגיעות לאותה נקודה: הן במקביל. מימין גם $B$ ו-$D$ במקביל.", do=show("a-1"),
      say="משמאל אֵיי וסִי מגיעות לאותה נקודה: הן במקביל. מימין גם בִּי ודִּי במקביל."),
    P("$A$ ו-$C$: אחת פחות $0.1$ כפול $0.3$, כלומר $0.97$. $B$ ו-$D$: $0.92$.",
      say="אֵיי וסִי: אחת פחות 0.1 כפול 0.3, כלומר 0.97. בִּי ודִּי: 0.92."),
    P("והזוגות בטור: $0.97$ כפול $0.92$, כלומר $0.8924$.", do=show("a-2"), say="והזוגות בטור: 0.97 כפול 0.92, כלומר 0.8924.",
      hold=0.3),
    P("מקרה שני: $E$ לא פועלת. היא כמו חוט שנחתך, ונשארות שתי דרכים נפרדות.",
      do=hide("cb-w-E", "a-1") + show("cb-cut-E", "a-3"), say="מקרה שני: אִי לא פועלת. היא כמו חוט שנחתך, ונשארות שתי דרכים נפרדות."),
    P("$A$ ו-$B$ בטור: $0.72$. $C$ ו-$D$ בטור: $0.42$. ושתי הדרכים במקביל.", do=show("a-4"),
      say="אֵיי ובִּי בטור: 0.72. סִי ודִּי בטור: 0.42. ושתי הדרכים במקביל."),
    P("אחת פחות $0.28$ כפול $0.58$: יוצא $0.8376$, קצת פחות מהמקרה הראשון.", do=show("a-5"),
      say="אחת פחות 0.28 כפול 0.58: יוצא 0.8376, קצת פחות מהמקרה הראשון.", hold=0.3),
    P("ועכשיו משקללים: כל מקרה כפול ההסתברות שלו. כאן שניהם חצי.", do=hide("cb-cut-E", "a-4") + show("cb-u-E")),
    P("$0.5$ כפול $0.8924$, ועוד $0.5$ כפול $0.8376$. יוצא $0.865$.", do=show("cb-on", "a-7"),
      say="0.5 כפול 0.8924, ועוד 0.5 כפול 0.8376. יוצא 0.865.", hold=0.3),
    P("בדיקה: התוצאה חייבת להיות בין שני המקרים. ואכן.", do=show("a-8")),
    P("המלכודת: לחשב רק מקרה אחד, או לשכוח את המשקלים. אחד מהם לבד הוא רק חסם, לא התשובה.", do=show("a-t"),
      hold=0.4),
], stage=f'<div class="circ-stack">{cb.svg()}<div class="circ-swap" style="--swap-h:80px">'
         + r'<div id="a-1" class="h"><div class="circ-cap" style="font-size:36px;color:var(--ink)">$(A\parallel C)$ בטור עם $(B\parallel D)$</div></div>'
         + r'<div id="a-4" class="h"><div class="circ-mid">$(A\text{-}B)\parallel(C\text{-}D)$</div></div></div></div>',
   panel=st.card("a-0", "plain", "$E$ פועלת: חוט")
         + st.card("a-2", "ex", r"$P(S\mid E)=0.97\cdot0.92=0.8924$")
         + st.card("a-3", "plain", "$E$ לא פועלת: חוט חתוך")
         + st.card("a-5", "ex", r"$P(S\mid\overline E)=1-0.28\cdot0.58=0.8376$")
         + st.card("a-7", "ex", r"$0.5\cdot0.8924+0.5\cdot0.8376=0.865$")
         + st.card("a-8", "rule", "🔑 $P(S)=0.865$, בין שני המקרים ✓")
         + st.card("a-t", "trap", "⚠️ שני המקרים, כל אחד במשקל שלו"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: גשר מחמש יחידות, כל אחת פועלת בהסתברות $p$, בלי תלות.",
      say="שאלה ממבחן: גשר מחמש יחידות, כל אחת פועלת בהסתברות פִּי, בלי תלות."),
    P("שימו לב לשמות: כאן $A$ ו-$B$ בצד שמאל, $C$ ו-$D$ בצד ימין, ו-$E$ באמצע.",
      say="שימו לב לשמות: כאן אֵיי ובִּי בצד שמאל, סִי ודִּי בצד ימין, ואִי באמצע."),
    P("ידוע שבדיוק יחידה אחת לא פועלת, ולא ידוע איזו. מה ההסתברות שהמעגל פועל?", do=show("x-1")),
    P("לפני שכותבים נוסחה, נבדוק כל אחת מחמש האפשרויות."),
    P("$A$ נכשלת: הזרם עובר בתחתית, דרך $B$ ו-$D$.", do=show("cx-x-A", "cx-ok-B", "cx-ok-D"),
      say="אֵיי נכשלת: הזרם עובר בתחתית, דרך בִּי ודִּי."),
    P("$B$ נכשלת: הזרם עובר למעלה, דרך $A$ ו-$C$.", do=hide("cx-x-A", "cx-ok-B", "cx-ok-D") + show("cx-x-B", "cx-ok-A", "cx-ok-C"),
      say="בִּי נכשלת: הזרם עובר למעלה, דרך אֵיי וסִי."),
    P("$C$ נכשלת: שוב התחתית. ו-$D$ נכשלת: שוב הדרך העליונה.",
      do=hide("cx-x-B", "cx-ok-A", "cx-ok-C") + show("cx-x-C", "cx-ok-B", "cx-ok-D"),
      say="סִי נכשלת: שוב התחתית. ודִּי נכשלת: שוב הדרך העליונה."),
    P("ואם $E$ נכשלת, שתי הדרכים שלמות.", do=hide("cx-x-C", "cx-ok-B", "cx-ok-D") + show("cx-x-E", "cx-ok-A", "cx-ok-C"),
      say="ואם אִי נכשלת, שתי הדרכים שלמות."),
    P("כלומר בכל חמשת המקרים המעגל פועל. ולכן ההסתברות היא אחת.", do=hide("cx-x-E", "cx-ok-A", "cx-ok-C") + show("cx-on", "x-2"),
      hold=0.3),
    P("בנוסחה: החיתוך הוא כל המאורע שבו בדיוק יחידה אחת נכשלת, ולכן המונה שווה למכנה.", do=show("x-3")),
    P("והסיבה העמוקה: כדי לנתק גשר צריך לפחות שתי יחידות. למשל $A$ ו-$B$ ביחד.", do=show("x-4"),
      say="והסיבה העמוקה: כדי לנתק גשר צריך לפחות שתי יחידות. למשל אֵיי ובִּי ביחד."),
    P("המלכודת: לענות $5p^4(1-p)$. זו ההסתברות שבדיוק יחידה אחת נכשלת, וזה מה שידוע, לא מה ששואלים.",
      do=show("x-t"),
      say="המלכודת: לענות חמש פִּי בחזקת ארבע, כפול אחת פחות פִּי. זו ההסתברות שבדיוק יחידה אחת נכשלת, וזה מה שידוע, לא מה ששואלים.",
      hold=0.5),
], stage='<div class="circ-stack">'
         + '<div class="circ-row">' + st.raster("xr", "images/exams/24B-C-Q6-bridge.png", 300, (730, 526))
         + f'{cx.svg()}</div>'
         + st.card("x-3", "ex", "$P(S\\mid N_1)=\\dfrac{P(S\\cap N_1)}{P(N_1)}=\\dfrac{5p^4(1-p)}{5p^4(1-p)}=1$") + '</div>',
   panel=STEM
         + st.card("x-1", "plain", "$N_1$: בדיוק יחידה אחת לא פועלת")
         + st.card("x-2", "rule", "🔑 $P(S\\mid N_1)=1$")
         + st.card("x-4", "plain", "חתך של גשר: לפחות 2 יחידות")
         + st.card("x-t", "trap", "⚠️ $5p^4(1-p)$ הוא $P(N_1)$, הנתון"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בגשר אין בלוק נקי, כי היחידה האמצעית מחברת את שתי הדרכים.", do=show("r-1")),
    P("מתנים עליה. אם היא פועלת, היא חוט: שני זוגות מקביליים בטור.", do=show("r-2")),
    P("אם היא לא פועלת, היא נחתכת: שתי דרכים בטור, במקביל זו לזו.", do=show("r-3")),
    P("ובסוף משקללים את שני המקרים בהסתברות שלמה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="circ-stack"><div class="circ-mid">$P(S)=P(E)\\,P(S\\mid E)+P(\\overline E)\\,P(S\\mid\\overline E)$</div></div>',
   panel=st.card("r-1", "rule", "🔑 מתנים על $E$")
         + st.card("r-2", "rule", "🔑 $E$ פועלת: $(A\\parallel C)$ בטור עם $(B\\parallel D)$")
         + st.card("r-3", "rule", "🔑 $E$ לא: $(A\\text{-}B)\\parallel(C\\text{-}D)$")
         + st.card("r-4", "trap", "⚠️ שני המקרים, עם המשקלים"))

VIDEO = Video("C05", "circ", "הגשר: מתנים על היחידה האמצעית", [title, idea, cases, exam, recap],
              bank={"24B-C-Q6c": None})
