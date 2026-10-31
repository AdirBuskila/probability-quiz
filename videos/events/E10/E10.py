# -*- coding: utf-8 -*-
"""E10 · בוס: שאלות מבחן אמיתיות — video script (build: tools/video/vid.py E10).

Source: courses/events/C10.js (boss level: real exam parts on events, conditional probability, Bayes, independence).
A walkthrough of three fresh exam parts (open questions, bank key None), none of them used by any guided quiz:
  24A-D-Q2d  three fair dice; P(sum = 6 / X1 < X2) = 2/45
  25S-A-Q2b + 25S-A-Q2c  P(A∖B)=p, P(A∩B)=q, P(A/B)=s: P(B) = q/s, then P(A/B̄) = ps/(s−q)
  25S-A-Q2g  the same data: independent  <=>  s = p + q
Avoided on purpose: the six C10 boss items (24A-B-Q2b, 25A-A-Q2d, 25A-B-Q2a, 25A-B-Q2e, 25B-A-Q2d, 24B-B-Q2d) and
their content twins; 25S-A-Q2f ("can s < q?", a sibling of the boss item 25B-A-Q2d) is not solved.
The dice part is checked on the checker's dice(3) space with Monte Carlo; the p, q, s parts with sympy and on explicit
four-cell spaces for several numeric (p, q, s).
"""
from fractions import Fraction as Fr
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_events as w

# ---------------------------------------------------------------- part 1: 24A-D-Q2d
Q1 = BANK["24A-D-Q2d"]
assert "\\frac2{45}" in Q1["solution"].replace(" ", "")
D3 = w.Space.dice(3)
S6 = lambda o: o["sum"] == 6
LT = lambda o: o["d1"] < o["d2"]
trip = sorted(f'{o["d1"]}{o["d2"]}{o["d3"]}' for o, _ in D3.out if S6(o))
assert trip == ["114", "123", "132", "141", "213", "222", "231", "312", "321", "411"]
hit = [t for t in trip if t[0] < t[1]]
assert hit == ["123", "132", "141", "231"]
assert D3.P(LT) == Fr(15, 36) == Fr(5, 12) and D3.P(lambda o: S6(o) and LT(o)) == Fr(4, 216)
ANS1 = D3.both(S6, given=LT)
assert ANS1 == Fr(4, 216) / Fr(15, 36) == Fr(2, 45)
assert D3.P(S6) == Fr(10, 216) and Fr(4, 10) != ANS1                       # trap: 4 of the 10 triples

# ---------------------------------------------------------------- parts 2, 3: 25S-A-Q2b / Q2c / Q2g
Q2b, Q2c, Q3 = BANK["25S-A-Q2b"], BANK["25S-A-Q2c"], BANK["25S-A-Q2g"]
assert "P(B)=\\fracqs" in Q2b["solution"].replace(" ", "").replace("\\Longrightarrow", "")
assert "\\frac{ps}{s-q}" in Q2c["solution"].replace(" ", "") and "p+q=s" in Q3["solution"].replace(" ", "")
p, q, s = sp.symbols("p q s", positive=True)
PB = q / s
PAnB = sp.simplify(p / (1 - PB))
assert sp.simplify(PAnB - p * s / (s - q)) == 0
assert sp.solve(sp.Eq(s, p + q), s) == [p + q]                               # P(A/B) = P(A)
for ab, an, nb in [(Fr(1, 5), Fr(1, 10), Fr(3, 10)), (Fr(1, 4), Fr(1, 8), Fr(1, 2)), (Fr(3, 20), Fr(3, 20), Fr(7, 20))]:
    S = w.Space([({"A": 1, "B": 1}, ab), ({"A": 1, "B": 0}, an), ({"A": 0, "B": 1}, nb),
                 ({"A": 0, "B": 0}, 1 - ab - an - nb)])
    pv, qv = an, ab
    sv = S.P(lambda o: o["A"], given=lambda o: o["B"])
    assert S.P(lambda o: o["B"]) == qv / sv
    assert S.both(lambda o: o["A"], given=lambda o: not o["B"]) == pv * sv / (sv - qv)
    indep = S.P(lambda o: o["A"] and o["B"]) == S.P(lambda o: o["A"]) * S.P(lambda o: o["B"])
    assert indep == (sv == pv + qv)
assert (Fr(3, 20) + Fr(3, 20)) == Fr(3, 20) / Fr(1, 2)                         # the third table is the independent one

T2 = w.cells_table("t2", {"ab": "q", "an": "p", "mA": "p+q", "mB": "q/s", "mnB": "1-q/s", "tot": "1"},
                   shown=("ab", "an"))
STEM1 = (f'<div class="qstem"><span class="qid">{Q1["id"]}</span>מטילים קובייה מאוזנת שלוש פעמים ומסכמים. '
         'מה ההסתברות שהסכום 6, <b>אם ידוע</b> שהתוצאה הראשונה קטנה מהשנייה?</div>')
STEM2 = (f'<div class="qstem"><span class="qid">{Q2b["id"]} · {Q2c["id"]} · {Q3["id"]}</span>$A,B$ לא ריקים, '
         '<span class="nobr">$P(A\\setminus B)=p$</span>, <span class="nobr">$P(A\\cap B)=q$</span>, '
         '<span class="nobr">$P(A/B)=s$</span>. חשבו $P(B)$, $P(A/\\overline{B})$, ומתי $A,B$ בלתי תלויים?</div>')

TRIP = '<div class="ev-mid" style="font-size:40px;letter-spacing:2px">' + "&ensp;".join(
    f'<span id="d-{t}">{t}</span>' if t not in hit else f'<b id="d-{t}" style="color:var(--brand)">{t}</b>' for t in trip) + "</div>"
TRIP0 = '<div class="ev-mid" style="font-size:40px;letter-spacing:2px">' + "&ensp;".join(trip) + "</div>"

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הבוס של הקורס: שלושה סעיפים אמיתיים ממבחנים, פתורים מההתחלה ועד הסוף."),
    P("לפני כל סעיף: מהו מרחב המדגם, מה ידוע, ומה המכנה."),
    P("נתחיל.", hold=0.4),
], stage='<div class="kicker">E10 · בוס</div><h1>בוס: שאלות מבחן אמיתיות</h1>'
         '<p>מותנה בשלוש קוביות, ונתוני $p,q,s$: הסתברות מותנית, משלים ואי-תלות.</p>',
   layout="title")

part1 = Scene("p1", "סעיף 1: שלוש קוביות", [
    P("סעיף ראשון. מטילים קובייה מאוזנת שלוש פעמים, ומסכמים.", do=show("x-stem1")),
    P("אם ידוע שהתוצאה הראשונה קטנה מהשנייה, מה ההסתברות שהסכום שש?", hold=0.1),
    P("ההגדרה: החיתוך חלקי מה שידוע. נתחיל במכנה, מה שידוע: הראשונה קטנה מהשנייה.", do=show("y-1")),
    P("התוצאה השלישית לא משנה כאן, אז מספיק לספור זוגות. מתוך שלושים ושישה, בשישה הן שוות.",
      do=show("y-2")),
    P("בשלושים הנותרים, בחצי הראשונה קטנה, ובחצי גדולה. חמישה עשר מתוך שלושים ושישה, כלומר חמש חלקי שתים עשרה.",
      say="בשלושים הנותרים, בחצי הראשונה קטנה, ובחצי גדולה. חמישה עשר מתוך שלושים ושישה, כלומר חמש חלקי שתים עשרה.",
      hold=0.3),
    P("עכשיו המונה. כל השלשות שסכומן שש: יש עשר כאלה.", do=show("y-3")),
    P("מתוכן, הראשונה קטנה מהשנייה רק בארבע: אחת שתיים שלוש, אחת שלוש שתיים, אחת ארבע אחת, ושתיים שלוש אחת.",
      do=hide("y-3") + show("y-4")),
    P("כל שלשה בהסתברות אחת חלקי מאתיים שש עשרה. אז החיתוך: ארבע חלקי מאתיים שש עשרה.", do=show("y-5")),
    P("מחלקים: ארבע חלקי מאתיים שש עשרה, חלקי חמש חלקי שתים עשרה. יוצא שתיים חלקי ארבעים וחמש.",
      say="מחלקים: ארבע חלקי מאתיים שש עשרה, חלקי חמש חלקי שתים עשרה. יוצא שתיים חלקי ארבעים וחמש.",
      do=show("y-6"), hold=0.3),
    P("המלכודת: לענות ארבע עשיריות, ארבע מתוך עשר השלשות. זה התנה על הסכום, הכיוון ההפוך.", do=show("y-t"), hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="y-1" class="h">$P(S=6\,/\,X_1&lt;X_2)=\dfrac{P(S=6\cap X_1&lt;X_2)}{P(X_1&lt;X_2)}$</div>'
         r'<div id="y-2" class="h">$P(X_1&lt;X_2)=\frac{(36-6)/2}{36}=\frac{15}{36}=\frac{5}{12}$</div></div>'
         f'<div class="ev-swap" style="--swap-h:70px"><div id="y-3" class="h">{TRIP0}</div><div id="y-4" class="h">{TRIP}</div></div>'
         '<div class="ev-eqs lg">'
         r'<div id="y-5" class="h">$P(S=6\cap X_1&lt;X_2)=\frac{4}{216}$</div>'
         r'<div id="y-6" class="h">$\dfrac{4/216}{5/12}=\dfrac{2}{45}$</div></div></div>',
   panel=f'<div id="x-stem1" class="h">{STEM1}</div>'
         + st.card("y-t", "trap", "⚠️ $\\frac{4}{10}$ הוא $P(X_1&lt;X_2\\,/\\,S=6)$"))

part2 = Scene("p2", "סעיף 2: p, q, s", [
    P("סעיף שני. $A$ ו-$B$ מאורעות לא ריקים. נתונים: $A$ פחות $B$ בהסתברות $p$, והחיתוך בהסתברות $q$.",
      say="סעיף שני. אֵיי ובִּי מאורעות לא ריקים. נתונים: אֵיי פחות בִּי בהסתברות פִּי, והחיתוך בהסתברות קְיוּ.",
      do=show("x-stem2")),
    P("והנתון השלישי: ההסתברות של $A$ בהינתן $B$ היא $s$.",
      say="והנתון השלישי: ההסתברות של אֵיי בהינתן בִּי היא אֶס.", hold=0.1),
    P("נמלא את הטבלה. החיתוך $q$, ו-$A$ בלי $B$ הוא $p$. לכן $P(A)$ הוא $p$ ועוד $q$, כמו שראינו בסרטון הראשון.",
      say="נמלא את הטבלה. החיתוך קְיוּ, ואֵיי בלי בִּי הוא פִּי. לכן פֵּה של אֵיי הוא פִּי ועוד קְיוּ, כמו שראינו בסרטון הראשון.",
      do=show("t2-mA")),
    P("עכשיו $P(B)$. ההגדרה: $s$ שווה החיתוך חלקי $P(B)$, כלומר $q$ חלקי $P(B)$.",
      say="עכשיו פֵּה של בִּי. ההגדרה: אֶס שווה החיתוך חלקי פֵּה של בִּי, כלומר קְיוּ חלקי פֵּה של בִּי.", do=show("z-1")),
    P("מעבירים אגפים: $P(B)$ שווה $q$ חלקי $s$.", say="מעבירים אגפים: פֵּה של בִּי שווה קְיוּ חלקי אֶס.",
      do=show("t2-mB", "t2-mnB", "z-2"), hold=0.3),
    P("ועכשיו ההסתברות של $A$ בהינתן המשלים של $B$. המונה: $A$ בלי $B$, כלומר $p$.",
      say="ועכשיו ההסתברות של אֵיי בהינתן המשלים של בִּי. המונה: אֵיי בלי בִּי, כלומר פִּי.", do=show("t2-h-an", "z-3")),
    P("המכנה: מה שידוע, המשלים של $B$. אחת פחות $q$ חלקי $s$.",
      say="המכנה: מה שידוע, המשלים של בִּי. אחת פחות קְיוּ חלקי אֶס.", do=show("t2-h-mnB")),
    P("מכפילים מונה ומכנה ב-$s$: $p$ כפול $s$, חלקי $s$ פחות $q$.",
      say="מכפילים מונה ומכנה באֶס: פִּי כפול אֶס, חלקי, בסוגריים, אֶס פחות קְיוּ.", do=show("z-4"), hold=0.3),
    P("המלכודת: לחלק ב-$P(B)$ ולא במשלים שלו. אחרי הקו האלכסוני כתוב המשלים, והוא המכנה.",
      say="המלכודת: לחלק בפֵּה של בִּי ולא במשלים שלו. אחרי הקו האלכסוני כתוב המשלים, והוא המכנה.", do=show("z-t"), hold=0.4),
], stage=f'<div class="ev-stack">{T2}<div class="ev-eqs lg">'
         r'<div id="z-1" class="h">$s=\dfrac{P(A\cap B)}{P(B)}=\dfrac{q}{P(B)}$</div>'
         r'<div id="z-2" class="h">$P(B)=\dfrac{q}{s}$</div>'
         r'<div id="z-3" class="h">$P(A/\overline{B})=\dfrac{P(A\setminus B)}{P(\overline{B})}=\dfrac{p}{1-q/s}$</div></div></div>',
   panel=f'<div id="x-stem2" class="h">{STEM2}</div>'
         + st.card("z-4", "rule", "🔑 $P(A/\\overline{B})=\\dfrac{ps}{s-q}$")
         + st.card("z-t", "trap", "⚠️ המכנה הוא $P(\\overline{B})$, לא $P(B)$"))

part3 = Scene("p3", "סעיף 3: אי-תלות", [
    P("סעיף שלישי, על אותם נתונים: עבור אילו פרמטרים $A$ ו-$B$ בלתי תלויים?",
      say="סעיף שלישי, על אותם נתונים: עבור אילו פרמטרים אֵיי ובִּי בלתי תלויים?"),
    P("ההגדרה: החיתוך שווה למכפלה. את החיתוך כבר יש לנו: $q$.",
      say="ההגדרה: החיתוך שווה למכפלה. את החיתוך כבר יש לנו: קְיוּ.", do=show("w-1")),
    P("והמכפלה: $P(A)$ הוא $p$ ועוד $q$, ו-$P(B)$ הוא $q$ חלקי $s$.",
      say="והמכפלה: פֵּה של אֵיי הוא פִּי ועוד קְיוּ, ופֵּה של בִּי הוא קְיוּ חלקי אֶס.", do=show("w-2")),
    P("משווים: $q$ שווה $(p+q)$ כפול $q$ חלקי $s$.",
      say="משווים: קְיוּ שווה, בסוגריים פִּי ועוד קְיוּ, כפול קְיוּ חלקי אֶס.", do=show("w-3")),
    P("$q$ חיובי, כי $P(B)$ שווה $q$ חלקי $s$, וההסתברות המותנית מוגדרת רק כש-$P(B)$ חיובי. אז מותר לחלק ב-$q$.",
      say="קְיוּ חיובי, כי פֵּה של בִּי שווה קְיוּ חלקי אֶס, וההסתברות המותנית מוגדרת רק כשפֵּה של בִּי חיובי. אז מותר לחלק בקְיוּ."),
    P("נשאר: $p$ ועוד $q$, חלקי $s$, שווה אחת. כלומר $s$ שווה $p$ ועוד $q$.",
      say="נשאר: פִּי ועוד קְיוּ, חלקי אֶס, שווה אחת. כלומר אֶס שווה פִּי ועוד קְיוּ.", do=show("w-4", "w-5"), hold=0.3),
    P("המלכודת: לבדוק אם הם זרים. זרים היה אומר שהחיתוך, $q$, הוא אפס. אבל השאלה על אי-תלות.",
      say="המלכודת: לבדוק אם הם זרים. זרים היה אומר שהחיתוך, קְיוּ, הוא אפס. אבל השאלה על אי תלות.",
      do=show("w-t"), hold=0.4),
], stage='<div class="ev-stack"><div class="ev-eqs lg">'
         r'<div id="w-1" class="h">$P(A\cap B)=q$</div>'
         r'<div id="w-2" class="h">$P(A)P(B)=(p+q)\cdot\dfrac{q}{s}$</div>'
         r'<div id="w-3" class="h">$q=(p+q)\cdot\dfrac{q}{s}$</div>'
         r'<div id="w-4" class="h">$\dfrac{p+q}{s}=1$</div></div></div>',
   panel=st.card("w-5", "rule", "🔑 בלתי תלויים אם ורק אם $s=p+q$")
         + st.card("w-t", "trap", "⚠️ אי-תלות $\\ne$ זרים"))

recap = Scene("recap", "סיכום הקורס", [
    P("לסיכום הקורס: מתרגמים את המשפט למאורע, ומפרקים אותו לחלקים זרים.", do=show("r-1")),
    P("בשאלת אם ידוע: המונה הוא החיתוך, והמכנה הוא מה שידוע.", do=show("r-2")),
    P("כשמשהו תלוי במקרה: הסתברות שלמה. וכשהופכים את הכיוון: בייס.", do=show("r-3")),
    P("ואי-תלות בודקים במספרים, לא בתחושה. בהצלחה במבחן!", do=show("r-4"), hold=0.6),
], stage='<div class="ev-stack"><div class="ev-big">$P(A/B)=\\dfrac{P(A\\cap B)}{P(B)}$</div></div>',
   panel=st.card("r-1", "rule", "🔑 חלקים זרים מתחברים")
         + st.card("r-2", "rule", "🔑 מכנה: מה שידוע")
         + st.card("r-3", "rule", "🔑 שלמה ובייס: עץ")
         + st.card("r-4", "trap", "⚠️ אי-תלות: $P(A\\cap B)=P(A)P(B)$"))

VIDEO = Video("E10", "events", "בוס: שאלות מבחן אמיתיות", [title, part1, part2, part3, recap],
              bank={"24A-D-Q2d": None, "25S-A-Q2b": None, "25S-A-Q2c": None, "25S-A-Q2g": None})
