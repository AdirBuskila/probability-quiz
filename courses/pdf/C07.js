/* pdf course, level 7 - conditional probability P(A|B) from F. Checked by tools/verify/needhelp/pdf/check.py */
COURSE_LEVEL("pdf", {
  id: "C07", order: 7, icon: "🔀", title: "הסתברות מותנית מתוך F",
  goal: "אחרי השלב הזה אפשר לחשב הסתברות מותנית של קטעים, כולל תנאי עם ערך מוחלט, כיחס של הפרשי F.",
  source: "ai-verified",
  lesson: {
    html: String.raw`
<p>במבחן שואלים בצורה "$P(X>a\,/\,X<b)$": ההסתברות ש-$X>a$ <b>בהינתן</b> ש-$X<b$. ההגדרה היא כמו תמיד:</p>
<div class="lesson-formula">$$P(A\mid B)=\frac{P(A\cap B)}{P(B)}$$</div>
<p>עם צפיפות אפשר לעבוד בשלושה צעדים: (1) <b>המכנה</b> הוא ההסתברות של התנאי $B$, מ-$F$. (2) <b>המונה</b> הוא ההסתברות של החיתוך $A\cap B$: חותכים את שני הקטעים לקטע משותף אחד. (3) מחלקים.</p>
<table>
<thead><tr><th>השאלה</th><th>הנוסחה</th></tr></thead>
<tbody>
<tr><td>$P(X>a\mid X<b)$ כש-$a<b$</td><td>$\dfrac{F(b)-F(a)}{F(b)}$</td></tr>
<tr><td>$P(X<c\mid X>d)$ כש-$d<c$</td><td>$\dfrac{F(c)-F(d)}{1-F(d)}$</td></tr>
<tr><td>$P(X>a\mid |X|<b)$ כש-$0<a<b$</td><td>$\dfrac{F(b)-F(a)}{F(b)-F(-b)}$</td></tr>
</tbody></table>
<div class="lesson-ex">דוגמה (עם $F(t)=\tfrac{t^2}{2}$ ל-$0\le t<1$ ו-$F(t)=\tfrac t2$ ל-$1\le t<2$): $P(X>\tfrac12\mid X<\tfrac32)=\dfrac{F(\frac32)-F(\frac12)}{F(\frac32)}=\dfrac{\frac34-\frac18}{\frac34}=\dfrac56$.</div>
<div class="lesson-rule">🔑 <b>שני מקרים קיצוניים שחוסכים חישוב.</b> אם האירוע <b>מוכל בתנאי</b> (למשל $P(X<\tfrac12\mid X<1)$), החיתוך הוא האירוע עצמו: $\frac{F(1/2)}{F(1)}$. אם התנאי <b>מוכל באירוע</b> (למשל $P(X<2\mid \tfrac12<X<\tfrac32)$ כש-$X<2$ בטוח), התשובה היא 1.</div>
<div class="lesson-trap">⚠️ המכנה הוא תמיד ההסתברות של <b>התנאי</b>, ולא של האירוע. מי שמחלק ב-$P(A)$ או ב-1 מקבל לעיתים מספר גדול מ-1, וזה סימן שיש טעות.</div>`
  },
  questions: [
    { id: "C07-Q1",
      step: { type: "numeric",
              prompt: "ההתפלגות המצטברת היא $F(t)=\\frac{t^2}{2}$ ל-$0\\le t<1$ ו-$F(t)=\\frac t2$ ל-$1\\le t<2$ (0 לפני 0, 1 מ-2). מהי $P(X>\\frac12\\,/\\,X<\\frac32)$? (שבר או עשרוני)",
              answer: 0.833333, tol: 0.001,
              explain: "המונה: $P(\\frac12<X<\\frac32)=\\frac34-\\frac18=\\frac58$. המכנה: $P(X<\\frac32)=\\frac34$. היחס: $\\frac{5/8}{3/4}=\\frac56$." },
      sim: { kind: "pdf", estimate: "P(X>1/2 | X<3/2)", exact: 0.833333333333, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x > 1/2", given: "x < 3/2" } },
      recap: "המכנה הוא ההסתברות של התנאי: $F(\\frac32)$." },
    { id: "C07-Q2",
      step: { type: "numeric",
              prompt: "באותה התפלגות מצטברת, מהי $P(X<1\\,/\\,X>\\frac12)$? (שבר או עשרוני)",
              answer: 0.428571, tol: 0.001,
              explain: "המונה: $P(\\frac12<X<1)=F(1)-F(\\frac12)=\\frac12-\\frac18=\\frac38$. המכנה (התנאי): $P(X>\\frac12)=1-\\frac18=\\frac78$. היחס: $\\frac{3/8}{7/8}=\\frac37$." },
      sim: { kind: "pdf", estimate: "P(X<1 | X>1/2)", exact: 0.428571428571, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x < 1", given: "x > 1/2" } },
      recap: "המכנה: $1-F(\\frac12)$, כי התנאי הוא $X>\\frac12$." },
    { id: "C07-Q3",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=1+x$ בקטע $[-1,0)$ ו-$f(x)=1-x$ בקטע $[0,1)$ (0 מחוץ לשניהם). ההתפלגות המצטברת שלה היא $F(t)=\\frac{(t+1)^2}{2}$ ל-$-1\\le t<0$ ו-$F(t)=1-\\frac{(1-t)^2}{2}$ ל-$0\\le t<1$. מהי $P(X>\\frac14\\,/\\,|X|<\\frac12)$? (שבר או עשרוני)",
              answer: 0.208333, tol: 0.001,
              explain: "התנאי $|X|<\\frac12$ הוא $-\\frac12<X<\\frac12$, ולכן המכנה $F(\\frac12)-F(-\\frac12)=\\frac78-\\frac18=\\frac34$. המונה (החיתוך $\\frac14<X<\\frac12$): $F(\\frac12)-F(\\frac14)=\\frac78-\\frac{23}{32}=\\frac{5}{32}$. היחס: $\\frac{5/32}{3/4}=\\frac5{24}$." },
      sim: { kind: "pdf", estimate: "P(X>1/4 | |X|<1/2)", exact: 0.208333333333, params: { pieces: [{ from: -1, to: 0, expr: "1+x" }, { from: 0, to: 1, expr: "1-x" }], event: "x > 1/4", given: "abs(x) < 1/2" } },
      recap: "$|X|<b$ פירושו $-b<X<b$." },
    { id: "C07-Q4", question: "באותה צפיפות של השאלה הראשונה (ההתפלגות המצטברת $F(t)=\\frac{t^2}{2}$ על $[0,1)$ ו-$\\frac t2$ על $[1,2)$), מהי $P(X<\\frac12\\,/\\,X<1)$?",
      options: [
        { id: "a", value: "$\\dfrac18$" },
        { id: "b", value: "$\\dfrac12$" },
        { id: "c", value: "$\\dfrac14$" },
        { id: "d", value: "$\\dfrac38$" }],
      correctId: "c",
      explanation: "האירוע $X<\\frac12$ מוכל בתנאי $X<1$, ולכן החיתוך הוא האירוע עצמו: $\\frac{F(1/2)}{F(1)}=\\frac{1/8}{1/2}=\\frac14$. התשובה $\\frac18$ שוכחת לחלק בהסתברות של התנאי.",
      sim: { kind: "pdf", estimate: "P(X<1/2 | X<1)", exact: 0.25, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x < 1/2", given: "x < 1" } },
      recap: "אירוע מוכל בתנאי: מחלקים את ההסתברות של האירוע בזו של התנאי." },
    { id: "C07-Q5", question: "באותה צפיפות (ההתפלגות המצטברת $F(t)=\\frac{t^2}{2}$ על $[0,1)$ ו-$\\frac t2$ על $[1,2)$), מהי $P(X<2\\,/\\,\\frac12<X<\\frac32)$?",
      options: [
        { id: "a", value: "$\\dfrac34$" },
        { id: "b", value: "$\\dfrac58$" },
        { id: "c", value: "$1$" },
        { id: "d", value: "$\\dfrac56$" }],
      correctId: "c",
      explanation: "הצפיפות מתאפסת מ-$x=2$, ולכן $X<2$ בטוח. התנאי ($\\frac12<X<\\frac32$) מוכל באירוע ($X<2$), והחיתוך הוא התנאי עצמו, כלומר ההסתברות של התנאי מחולקת בעצמה והתוצאה 1.",
      sim: { kind: "pdf", estimate: "P(X<2 | 1/2<X<3/2)", exact: 1, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x < 2", given: "x > 1/2 and x < 3/2" } },
      recap: "תנאי מוכל באירוע: התשובה 1." },
    { id: "C07-Q6",
      step: { type: "findbug",
              prompt: "ההתפלגות המצטברת היא $F(t)=\\frac{t^2}{2}$ ל-$0\\le t<1$ ו-$F(t)=\\frac t2$ ל-$1\\le t<2$. בפתרון הבא של $P(X>\\frac12\\,/\\,X<\\frac32)$ נפלה טעות. באיזו שורה היא נעשתה לראשונה?",
              lines: [
                "$P=\\dfrac{P(\\frac12<X<\\frac32)}{P(X<\\frac32)}$",
                "$P(\\tfrac12<X<\\tfrac32)=F(\\tfrac32)-F(\\tfrac12)=\\tfrac34-\\tfrac18=\\tfrac58$",
                "$P(X<\\tfrac32)=F(\\tfrac12)=\\tfrac18$",
                "$P=\\dfrac{5/8}{1/8}=5$"],
              bugIndex: 2,
              explain: "ההסתברות של התנאי היא $P(X<\\frac32)=F(\\frac32)=\\frac34$ ולא $F(\\frac12)$. הערך 5 (הגדול מ-1) הוא הסימן שמשהו שבור. התשובה הנכונה היא $\\frac{5/8}{3/4}=\\frac56$." },
      recap: "הסתברות לא עולה על 1; אם יצא יותר, המכנה שגוי." },
  ],
});
