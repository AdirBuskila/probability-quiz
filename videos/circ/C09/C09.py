# -*- coding: utf-8 -*-
"""C09 · בוס: שאלות מבחן אמיתיות — video script (build: tools/video/vid.py C09). Boss walkthrough.

Source: courses/circ/C09.js (boss level: bridge, two circuits from the same units, Bayes, different probabilities).
Exam anchors (all open questions, bank key None, used by no guided quiz):
  24A-D-Q6b, 24A-D-Q6c  Q1 the bridge (A top-left, B top-right, C bottom-left, D bottom-right, E middle); Q2 from the
                        same units: A straight across, in parallel with E-B and with C-D. P(Q2) = p+(1-p)(2p^2-p^4)
                        by conditioning on A; P(Q2|Q1) = 1 because every path of Q1 contains a path of Q2 (Q1 ⊆ Q2),
                        so P(Q1) (the bridge formula, a quiz answer) is never needed.
  25S-A-Q5b, 25S-A-Q5c  the road map: both Eugene and Serge reach the institute, P2 = p^2(1+2p-2p^2); Eugene yes and
                        Serge no, P3 = P1 - P2 = p(1-p)(1-p^2).
Avoided on purpose: the six C09 boss items (25A-A-Q4a, 24S-A-Q6a/b, 24A-B-Q6c, 25B-A-Q5d, 24B-A-Q6c) and their twins:
the (A-B)||C block (25B-B-Q5a/b/c, whose arrangement argument is also the one of 25B-A-Q5d, and the block of 24B-A-Q6a/
24B-A-Q6c) is not used; the bridge formula is not shown; 25S-A-Q5a is solved in C04 and only quoted here as a given.
Note: C07 solves 24B-B-Q6c by the same conditioning template that the boss item 24A-B-Q6c needs (different Q2).
Every probability is the full truth table summed (w_circ.sprob); the inclusion Q1 ⊆ Q2 is checked state by state.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_circ as w

p = w.p

# ---------------------------------------------------------------- 24A-D-Q6b/c (verified)
QB, QC = BANK["24A-D-Q6b"], BANK["24A-D-Q6c"]
assert QB["contextId"] == QC["contextId"] == "24A-D-c6"
assert "p+(1-p)(2p^2-p^4)" in QB["solution"].replace(" ", "") and "P(Q_2/Q_1)=1" in QC["solution"].replace(" ", "")
U5 = w.same("ABCDE")
TB = w.BR("A", "B", "C", "D", "E")
TQ2 = w.Pa(w.S(w.C("E"), w.C("B")), w.C("A"), w.S(w.C("C"), w.C("D")))
b1 = lambda s: w.works(TB, s)
b2 = lambda s: w.works(TQ2, s)
PQ2 = w.sprob(b2, U5)
assert w.eq(PQ2, p + (1 - p) * (2 * p ** 2 - p ** 4))
assert w.sprob(b2, U5, given=lambda s: s["A"]) == 1
assert w.eq(w.sprob(b2, U5, given=lambda s: not s["A"]), 2 * p ** 2 - p ** 4)
assert w.eq(2 * p ** 2 - p ** 4, 1 - (1 - p ** 2) ** 2)
for bits in range(32):                                    # Q1 ⊆ Q2, state by state
    st_ = {u: bool(bits >> i & 1) for i, u in enumerate("ABCDE")}
    assert not b1(st_) or b2(st_)
PATHS = [("A", "B"), ("C", "D"), ("A", "E", "D"), ("C", "E", "B")]   # the minimal paths of the bridge
for pa in PATHS:
    assert b1({u: u in pa for u in "ABCDE"}) and b2({u: u in pa for u in "ABCDE"})
assert w.sprob(b2, U5, given=b1) == 1
assert not w.eq(w.sprob(b1, U5, given=b2), 1)                            # the other direction is not 1

# ---------------------------------------------------------------- 25S-A-Q5b/c (verified)
QS2, QS3 = BANK["25S-A-Q5b"], BANK["25S-A-Q5c"]
assert QS2["contextId"] == QS3["contextId"] == "25S-A-c5"
assert "p^2\\left(1+2p-2p^2\\right)" in QS2["solution"].replace(" ", "") and "p-p^2-p^3+p^4" in QS3["solution"].replace(" ", "")
U4 = w.same("ABCD")
QE = lambda s: s["A"] or (s["C"] and s["D"] and s["B"])   # Eugene: A, or C (pub) - D - B
QSe = lambda s: s["B"] or (s["D"] and s["C"] and s["A"])  # Serge: B, or D (pub) - C - A
P1 = w.sprob(QE, U4)
P2 = w.sprob(lambda s: QE(s) and QSe(s), U4)
P3 = w.sprob(lambda s: QE(s) and not QSe(s), U4)
assert w.eq(P1, p + p ** 3 - p ** 4)
assert w.eq(P2, p ** 2 * (1 + 2 * p - 2 * p ** 2))
assert w.eq(w.sprob(lambda s: QE(s) and QSe(s), U4, given=lambda s: s["A"]), p + p ** 2 - p ** 3)
assert w.eq(w.sprob(lambda s: QE(s) and QSe(s), U4, given=lambda s: not s["A"]), p ** 3)
assert w.eq(P3, P1 - P2) and w.eq(P3, p - p ** 2 - p ** 3 + p ** 4) and w.eq(P3, p * (1 - p) * (1 - p ** 2))
for bits in range(16):                                    # Eugene yes, Serge no  <=>  A open, B closed, not (C and D)
    s = {u: bool(bits >> i & 1) for i, u in enumerate("ABCD")}
    assert bool(QE(s) and not QSe(s)) == (s["A"] and not s["B"] and not (s["C"] and s["D"]))
assert not w.eq(P2, P1 ** 2)                                                # the trap: the two trips share roads

# ---------------------------------------------------------------- figures
cb = w.Circ("cb", TB, scale=0.72)
c2 = w.Circ("c2", TQ2, scale=0.8)
ce = w.Circ("ce", w.Pa(w.C("A"), w.S(w.C("C"), w.C("D"), w.C("B"))), scale=0.8)
cs = w.Circ("cs", w.Pa(w.C("B"), w.S(w.C("D"), w.C("C"), w.C("A"))), scale=0.8)

STEM1 = (f'<div class="qstem"><span class="qid">{QC["id"]}</span>$Q_1$ גשר מחמש יחידות, כל אחת $p$. מאותן יחידות '
         'מרכיבים את $Q_2$. (1) מה $P(Q_2)$? (2) אם ידוע ש-$Q_1$ פועל, מה ההסתברות שגם $Q_2$ פועל?</div>')
STEM2 = (f'<div class="qstem"><span class="qid">{QS2["id"]}</span>כל כביש פתוח בהסתברות $p$. '
         'מה ההסתברות שגם יוג׳ין וגם סרג׳ מגיעים למכון? ומה ההסתברות שיוג׳ין מגיע וסרג׳ לא?</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הבוס של מעגלים חשמליים: שתי שאלות מבחן אמיתיות, ארבעה סעיפים."),
    P("בראשונה בונים מעגל חדש מהיחידות של גשר. בשנייה, שני אנשים יוצאים לדרך על אותה מפת כבישים."),
    P("בשתיהן הכלים הם אותם כלים: צמצום, התניה, הכלה, וחיתוך של מאורעות תלויים.", hold=0.4),
], stage='<div class="kicker">C09 · מעגלים חשמליים</div><h1>בוס: שאלות מבחן אמיתיות</h1>'
         '<p>לפתור שאלות מעגלים מהמבחנים האמיתיים: גשר, מעגל שני מאותן יחידות, בייס ורכיבים עם הסתברויות שונות.</p>',
   layout="title")

q1 = Scene("q1", "שאלה 1: גשר ומעגל חדש", [
    P("שאלה ראשונה: $Q_1$ הוא גשר מחמש יחידות, כל אחת פועלת בהסתברות $p$.",
      say="שאלה ראשונה: קְיוּ אחת הוא גשר מחמש יחידות, כל אחת פועלת בהסתברות פִּי."),
    P("מפרקים אותו, ובונים מאותן יחידות את $Q_2$: $A$ עוברת ישר מהכניסה ליציאה.", do=hide("xr0") + show("xs"),
      say="מפרקים אותו, ובונים מאותן יחידות את המעגל השני: אֵיי עוברת ישר מהכניסה ליציאה."),
    P("ובמקביל אליה שתי דרכים: $E$ ו-$B$ בטור, ו-$C$ ו-$D$ בטור.",
      say="ובמקביל אליה שתי דרכים: אִי ובִּי בטור, וסִי ודִּי בטור."),
    P("סעיף ראשון: מה ההסתברות ש-$Q_2$ פועל? מתנים על $A$, כי היא מקצרת את כל המעגל.",
      do=show("c2-ok-A", "c2-on"), say="סעיף ראשון: מה ההסתברות שהמעגל השני פועל? מתנים על אֵיי, כי היא מקצרת את כל המעגל."),
    P("אם $A$ פועלת, המעגל פועל בוודאות. ואם לא, נשארו שתי דרכים של שתי יחידות, במקביל.",
      do=hide("c2-ok-A", "c2-on") + show("c2-x-A", "y-1"),
      say="אם אֵיי פועלת, המעגל פועל בוודאות. ואם לא, נשארו שתי דרכים של שתי יחידות, במקביל."),
    P("כל דרך נכשלת ב-$1-p^2$, ושתיהן ב-$(1-p^2)^2$. אז הן פועלות ב-$2p^2-p^4$.",
      say="כל דרך נכשלת באחת פחות, פִּי בריבוע. ושתיהן יחד בריבוע של המספר הזה. אז הן פועלות בשתיים פִּי בריבוע פחות פִּי בחזקת ארבע."),
    P("משקללים: $p$ כפול אחת, ועוד $1-p$ כפול $2p^2-p^4$.", do=hide("c2-x-A") + show("y-2"),
      say="משקללים: פִּי כפול אחת, ועוד אחת פחות פִּי, כפול שתיים פִּי בריבוע פחות פִּי בחזקת ארבע.", hold=0.4),
    P("סעיף שני: אם ידוע ש-$Q_1$ פועל, מה ההסתברות ש-$Q_2$ פועל?",
      say="סעיף שני: אם ידוע שהגשר פועל, מה ההסתברות שגם המעגל השני פועל?"),
    P("לפני נוסחאות, נבדוק את הדרכים של הגשר. יש לו ארבע דרכים מינימליות.", do=show("y-3")),
    P("$A$-$B$, ו-$A$-$E$-$D$, עוברות דרך $A$. ו-$A$ לבדה כבר מפעילה את $Q_2$.",
      do=show("cb-ok-A", "cb-ok-B", "cb-ok-E", "cb-ok-D"),
      say="אֵיי-בִּי, ואֵיי-אִי-דִּי, עוברות דרך אֵיי. ואֵיי לבדה כבר מפעילה את המעגל השני."),
    P("$C$-$D$ היא בדיוק אחת הדרכים של $Q_2$. ו-$C$-$E$-$B$ מכילה את $E$ וגם את $B$, עוד דרך של $Q_2$.",
      do=hide("cb-ok-A", "cb-ok-D") + show("cb-ok-C"),
      say="סִי-דִּי היא בדיוק אחת הדרכים של המעגל השני. וסִי-אִי-בִּי מכילה את אִי וגם את בִּי, עוד דרך של המעגל השני."),
    P("כלומר בכל מצב שבו הגשר פועל, גם $Q_2$ פועל. הגשר מוכל ב-$Q_2$.", do=hide("cb-ok-C", "cb-ok-E", "cb-ok-B") + show("y-4"),
      say="כלומר בכל מצב שבו הגשר פועל, גם המעגל השני פועל. הגשר מוכל בו."),
    P("ולכן החיתוך הוא פשוט הגשר, והמנה היא אחת. בלי לחשב את הגשר בכלל.", do=show("y-5"), hold=0.3),
    P("המלכודת: הכיוון. ההפך, אם ידוע ש-$Q_2$ פועל, כבר לא שווה אחת: $A$ לבדה מפעילה את $Q_2$, אבל לא את הגשר.",
      do=show("y-t"),
      say="המלכודת: הכיוון. ההפך, אם ידוע שהמעגל השני פועל, כבר לא שווה אחת: אֵיי לבדה מפעילה אותו, אבל לא את הגשר.", hold=0.4),
], stage='<div class="circ-stack"><div class="circ-swap" style="--swap-h:300px"><div id="xr0">'
         + st.raster("xr", "images/exams/24A-D-Q6-circuits.png", 600, (812, 402))
         + f'</div><div id="xs" class="h"><div class="circ-row" style="gap:20px">{cb.svg()}{c2.svg()}</div></div></div>'
         + st.card("y-2", "rule", r"🔑 $P(Q_2)=p+(1-p)(2p^2-p^4)$")
         + st.card("y-5", "rule", r"🔑 $Q_1\subseteq Q_2\ \Rightarrow\ P(Q_2\mid Q_1)=\dfrac{P(Q_1)}{P(Q_1)}=1$") + '</div>',
   panel=STEM1
         + st.card("y-1", "plain", r"$P(Q_2\mid\overline A)=1-(1-p^2)^2=2p^2-p^4$")
         + st.card("y-3", "plain", r"דרכי הגשר: $AB,\ CD,\ AED,\ CEB$")
         + st.card("y-4", "ex", r"כל דרך של $Q_1$ מכילה דרך של $Q_2$")
         + st.card("y-t", "trap", r"⚠️ $P(Q_1\mid Q_2)\ne1$"))

q2 = Scene("q2", "שאלה 2: מפת הכבישים", [
    P("שאלה שנייה: מפת הכבישים מהרמה של המשלים. כל כביש פתוח בהסתברות $p$.",
      say="שאלה שנייה: מפת הכבישים מהרמה של המשלים. כל כביש פתוח בהסתברות פִּי."),
    P("יוג׳ין מגיע דרך $A$, או בעקיפה $C$, $D$, $B$. כבר ראינו: $P_1$ הוא $p+p^3-p^4$.", do=show("w-0"),
      say="יוג׳ין מגיע דרך אֵיי, או בעקיפה סִי, דִּי, בִּי. כבר ראינו: פֵּא אחת היא פִּי ועוד פִּי בשלישית פחות פִּי בחזקת ארבע."),
    P("וסרג׳ בסימטריה: דרך $B$, או בעקיפה $D$, $C$, $A$.", say="וסרג׳ בסימטריה: דרך בִּי, או בעקיפה דִּי, סִי, אֵיי."),
    P("סעיף ראשון: מה ההסתברות ששניהם מגיעים? הם משתמשים באותם כבישים, ולכן מתנים על כביש $A$.",
      say="סעיף ראשון: מה ההסתברות ששניהם מגיעים? הם משתמשים באותם כבישים, ולכן מתנים על כביש אֵיי."),
    P("$A$ פתוח: יוג׳ין מגיע בוודאות. וסרג׳ צריך את $B$, או את $C$ וגם $D$.", do=show("ce-ok-A", "cs-ok-A"),
      say="אֵיי פתוח: יוג׳ין מגיע בוודאות. וסרג׳ צריך את בִּי, או את סִי וגם דִּי."),
    P("וזה $p+p^2-p^3$.", do=show("w-2"), say="וזה פִּי ועוד פִּי בריבוע פחות פִּי בשלישית."),
    P("$A$ סגור: יוג׳ין חייב את העקיפה, $C$, $D$ וגם $B$. ואז סרג׳ מגיע דרך $B$ בכל מקרה. זה $p^3$.",
      do=hide("ce-ok-A", "cs-ok-A") + show("ce-x-A", "cs-x-A", "w-3"),
      say="אֵיי סגור: יוג׳ין חייב את העקיפה, סִי, דִּי וגם בִּי. ואז סרג׳ מגיע דרך בִּי בכל מקרה. זה פִּי בשלישית."),
    P("משקללים: $P_2$ הוא $p^2$ כפול $1+2p-2p^2$.", do=hide("ce-x-A", "cs-x-A") + show("w-4"),
      say="משקללים: פֵּא שתיים היא פִּי בריבוע, כפול אחת ועוד שתיים פִּי פחות שתיים פִּי בריבוע.", hold=0.3),
    P("סעיף שני: יוג׳ין מגיע, וסרג׳ לא. זה החלק של $P_1$ שאינו בחיתוך: $P_1$ פחות $P_2$.", 
      say="סעיף שני: יוג׳ין מגיע, וסרג׳ לא. זה החלק של פֵּא אחת שאינו בחיתוך: פֵּא אחת פחות פֵּא שתיים."),
    P("ויוצא $p-p^2-p^3+p^4$.", do=show("w-6"), say="ויוצא פִּי פחות פִּי בריבוע פחות פִּי בשלישית ועוד פִּי בחזקת ארבע."),
    P("ובדיקה בדרך אחרת: כדי שסרג׳ לא יגיע, $B$ חייב להיות סגור. אז יוג׳ין צריך את $A$.",
      do=show("ce-ok-A", "ce-x-B", "cs-x-B"),
      say="ובדיקה בדרך אחרת: כדי שסרג׳ לא יגיע, בִּי חייב להיות סגור. אז יוג׳ין צריך את אֵיי."),
    P("ולסרג׳ חסרה העקיפה: לא גם $C$ וגם $D$. יוצא $p(1-p)(1-p^2)$, אותה תוצאה.", do=show("w-7"),
      say="ולסרג׳ חסרה העקיפה: לא גם סִי וגם דִּי. יוצא פִּי, כפול אחת פחות פִּי, כפול אחת פחות, פִּי בריבוע. אותה תוצאה."),
    P("המלכודת: $P_1$ בריבוע. שני הטיולים חולקים כבישים, ולכן הם תלויים.", do=show("w-t"),
      say="המלכודת: פֵּא אחת בריבוע. שני הטיולים חולקים כבישים, ולכן הם תלויים.", hold=0.5),
], stage=f'<div class="circ-stack">{st.raster("xr2", "images/exams/25S-A-Q5-map.png", 300, (556, 482))}'
         f'<div class="circ-row" style="gap:16px">{ce.svg()}{cs.svg()}</div>'
         '<div class="circ-cap">יוג׳ין (משמאל) &nbsp;·&nbsp; סרג׳ (מימין)</div>'
         '<div class="circ-row" style="gap:16px">' + st.card("w-2", "plain", "$A$: $p+p^2-p^3$")
         + st.card("w-3", "plain", "$\\overline A$: $p^3$") + '</div></div>',
   panel=STEM2
         + st.card("w-0", "plain", "$P_1=p+p^3-p^4$")
         + st.card("w-4", "rule", "🔑 $P_2=p^2(1+2p-2p^2)$")
         + st.card("w-6", "rule", "🔑 $P_3=P_1-P_2=p-p^2-p^3+p^4$")
         + st.card("w-7", "ex", "$=p(1-p)(1-p^2)$ ✓")
         + st.card("w-t", "trap", "⚠️ לא $P_1^2$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום הבוס: בכל השאלות האלה היו שני מאורעות שחולקים את אותן יחידות.", do=show("r-1")),
    P("ולכן אף פעם לא כופלים אותם. מתנים על מה שמשותף, או מחפשים הכלה בין המאורעות.", do=show("r-2")),
    P("בכל מקרה כותבים מה צריך כדי ששניהם יקרו, ומשקללים בהסתברות שלמה.", do=show("r-3")),
    P("ואחרי שיש חיתוך, הכול נגזר ממנו: מותנית, איחוד, או אחד בלי השני. בהצלחה במבחן.", do=show("r-4"), hold=0.6),
], stage='<div class="circ-stack"><div class="circ-mid">$P(X\\cap Y)=\\sum_k P(\\text{case}_k)\\,P(X\\cap Y\\mid\\text{case}_k)$</div>'
         '<div class="circ-mid">$P(X\\cap\\overline Y)=P(X)-P(X\\cap Y)$</div></div>',
   panel=st.card("r-1", "trap", "⚠️ יחידות משותפות: מאורעות תלויים")
         + st.card("r-2", "rule", "🔑 מתנים על המשותף")
         + st.card("r-3", "rule", "🔑 הסתברות שלמה על המקרים")
         + st.card("r-4", "rule", "🔑 מותנית, איחוד והפרש מתוך החיתוך"))

VIDEO = Video("C09", "circ", "בוס: שאלות מבחן אמיתיות", [title, q1, q2, recap],
              bank={"24A-D-Q6b": None, "24A-D-Q6c": None, "25S-A-Q5b": None, "25S-A-Q5c": None})
