/* pdf course, level 6 - probabilities of intervals from F. Checked by tools/verify/needhelp/pdf/check.py */
COURSE_LEVEL("pdf", {
  id: "C06", order: 6, icon: "🧮", title: "הסתברות של קטע מתוך F",
  goal: "אחרי השלב הזה אפשר לחשב הסתברות של קטע, של זנב ושל שני זנבות ישירות מההתפלגות המצטברת, כולל ההסתברות להיות מתחת לתוחלת.",
  source: "ai-verified",
  lesson: {
    html: String.raw`
<p>ברגע שיש לכם את $F_X$ (פעם אחת), כל הסתברות היא חיסור או משלים. אין צורך לאנטגרל שוב.</p>
<table>
<thead><tr><th>השאלה</th><th>החישוב</th></tr></thead>
<tbody>
<tr><td>$P(a<X<b)$</td><td>$F(b)-F(a)$</td></tr>
<tr><td>$P(X\le b)$ (וגם $P(X<b)$)</td><td>$F(b)$</td></tr>
<tr><td>$P(X>a)$</td><td>$1-F(a)$</td></tr>
<tr><td>שני זנבות: $X<a$ או $X>b$</td><td>$F(a)+\bigl(1-F(b)\bigr)$</td></tr>
</tbody></table>
<p>בכל נוסחה מציבים בענף הנכון של $F$: את $a$ ו-$b$ מציבים בקטע שבו הם נמצאים.</p>
<div class="lesson-ex">דוגמה: $F(t)=\tfrac{t^2}{2}$ ל-$0\le t<1$, ו-$F(t)=\tfrac t2$ ל-$1\le t<2$. אז $P(\tfrac12<X<\tfrac32)=F(\tfrac32)-F(\tfrac12)=\tfrac34-\tfrac18=\tfrac58$. שימו לב: $\tfrac32$ בקטע השני ($\tfrac{t}{2}$) ו-$\tfrac12$ בקטע הראשון ($\tfrac{t^2}{2}$).</div>
<div class="lesson-rule">🔑 <b>שאלה קלאסית:</b> "מהי $P(X\le E[X])$?" פשוט מחשבים את התוחלת $\mu$ (או שהיא נתונה) ומחזירים $F(\mu)$. אין כאן שום קסם: $E[X]$ היא מספר, ומציבים אותו ב-$F$.</div>
<div class="lesson-trap">⚠️ $P(X>a)$ הוא $1-F(a)$ ולא $F(a)$. וב-$P(a<X<b)$ החיסור הוא בסדר הנכון: ה-$F$ של הקצה הגדול פחות ה-$F$ של הקצה הקטן.</div>`
  },
  questions: [
    { id: "C06-Q1",
      step: { type: "numeric",
              prompt: "ההתפלגות המצטברת היא $F(t)=\\frac{t^2}{2}$ ל-$0\\le t<1$, $F(t)=\\frac t2$ ל-$1\\le t<2$, $F(t)=0$ לפני 0 ו-$F(t)=1$ מ-2 והלאה. מהי $P(\\frac12<X<\\frac32)$? (שבר או עשרוני)",
              answer: 0.625, tol: 0.001,
              explain: "$F(\\frac32)-F(\\frac12)=\\frac{3/2}{2}-\\frac{(1/2)^2}{2}=\\frac34-\\frac18=\\frac58$." },
      sim: { kind: "pdf", estimate: "P(1/2<X<3/2)", exact: 0.625, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x > 1/2 and x < 3/2" } },
      recap: "$P(a<X<b)=F(b)-F(a)$, כל קצה בענף שלו." },
    { id: "C06-Q2",
      step: { type: "numeric",
              prompt: "באותה התפלגות מצטברת ($\\frac{t^2}{2}$ על $[0,1)$ ו-$\\frac t2$ על $[1,2)$), מהי $P(X>\\frac32)$? (שבר או עשרוני)",
              answer: 0.25, tol: 0.001,
              explain: "$P(X>\\frac32)=1-F(\\frac32)=1-\\frac34=\\frac14$." },
      sim: { kind: "pdf", estimate: "P(X>3/2)", exact: 0.25, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x > 3/2" } },
      recap: "$P(X>a)=1-F(a)$." },
    { id: "C06-Q3",
      step: { type: "numeric",
              prompt: "באותה התפלגות (שתוחלתה $E[X]=\\frac{13}{12}$), מהי $P(X\\le E[X])$? (שבר או עשרוני)",
              answer: 0.541667, tol: 0.001,
              explain: "$\\frac{13}{12}\\in[1,2)$, ולכן $F(\\frac{13}{12})=\\frac{13/12}{2}=\\frac{13}{24}\\approx0.5417$." },
      sim: { kind: "pdf", estimate: "P(X<=E[X])", exact: 0.541666666667, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x <= 13/12" } },
      recap: "$P(X\\le E[X])=F(E[X])$, בענף שבו נמצאת התוחלת." },
    { id: "C06-Q4",
      step: { type: "numeric",
              prompt: "באותה התפלגות מצטברת, מהי ההסתברות ש-$X<\\frac12$ או $X>\\frac32$? (שבר או עשרוני)",
              answer: 0.375, tol: 0.001,
              explain: "שני זנבות זרים: $F(\\frac12)+\\bigl(1-F(\\frac32)\\bigr)=\\frac18+\\frac14=\\frac38$." },
      sim: { kind: "pdf", estimate: "P(X<1/2 or X>3/2)", exact: 0.375, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x < 1/2 or x > 3/2" } },
      recap: "שני זנבות: $F(a)+1-F(b)$." },
    { id: "C06-Q5",
      step: { type: "numeric",
              prompt: "ההתפלגות המצטברת היא $F(t)=\\frac{2t}{3}$ ל-$0\\le t<1$ ו-$F(t)=\\frac{t+1}{3}$ ל-$1\\le t<2$ (0 לפני 0, 1 מ-2). מהי $P(\\frac13<X<\\frac43)$? (שבר או עשרוני)",
              answer: 0.555556, tol: 0.001,
              explain: "$F(\\frac43)=\\frac{4/3+1}{3}=\\frac79$ (בענף השני) ו-$F(\\frac13)=\\frac{2/3}{3}=\\frac29$ (בענף הראשון). ההפרש: $\\frac59$." },
      sim: { kind: "pdf", estimate: "P(1/3<X<4/3)", exact: 0.555555555556, params: { pieces: [{ from: 0, to: 1, expr: "2/3" }, { from: 1, to: 2, expr: "1/3" }], event: "x > 1/3 and x < 4/3" } },
      recap: "מציבים כל קצה בענף שבו הוא נמצא." },
    { id: "C06-Q6",
      step: { type: "numeric",
              prompt: "ההתפלגות המצטברת היא $F(t)=1-e^{-2t}$ ל-$t\\ge0$ (ו-0 ל-$t<0$). מהי $P(1<X<2)$? (עשרוני, ארבע ספרות אחרי הנקודה)",
              answer: 0.117, tol: 0.0006,
              explain: "$F(2)-F(1)=\\left(1-e^{-4}\\right)-\\left(1-e^{-2}\\right)=e^{-2}-e^{-4}\\approx0.1353-0.0183=0.1170$." },
      recap: "ה-1 מתבטל: $e^{-2}-e^{-4}$." },
  ],
});
