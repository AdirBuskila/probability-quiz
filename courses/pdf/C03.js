/* pdf course, level 3 - a piecewise density and the "zero rule". Checked by tools/verify/needhelp/pdf/check.py */
COURSE_LEVEL("pdf", {
  id: "C03", order: 3, icon: "🧩", title: "צפיפות מחולקת לקטעים",
  goal: "אחרי השלב הזה אפשר לנרמל צפיפות שנוסחתה משתנה בין קטעים, ולזהות מתי אינטגרל מתבדר ולכן קבוע חייב להיות 0.",
  source: "ai-verified",
  lesson: {
    html: String.raw`
<p>במבחן הצפיפות כמעט תמיד כתובה בכמה קטעים, למשל $f(x)=a$ על $[0,1)$ ו-$f(x)=b$ על $[1,2)$. אין בזה שום דבר חדש: <b>מפצלים את האינטגרל לפי הקטעים ומחברים</b>.</p>
<div class="lesson-formula">$$\int_{-\infty}^{\infty}f=\int_{I_1}f+\int_{I_2}f+\cdots=1$$</div>
<p>כאן $I_1,I_2,\dots$ הם הקטעים של הצפיפות.</p>
<div class="lesson-ex">דוגמה: $f=a$ על $[0,1)$, $f=3a$ על $[1,2)$. $\;a\cdot1+3a\cdot1=4a=1$, ולכן $a=\tfrac14$.</div>
<p>כל קטע תורם לאינטגרל רק את החלק שלו. הקטעים ללא נוסחה (מחוץ לתחום) תורמים 0.</p>
<h3>כלל האפס: אינטגרל מתבדר</h3>
<p>כשתחום הוא אינסופי, או כשהצפיפות "מתפוצצת" ליד נקודה, האינטגרל עלול להיות אינסופי. אז <b>הקבוע שלפני הביטוי חייב להיות 0</b>, אחרת השטח הכולל לא יכול להיות 1.</p>
<table>
<thead><tr><th>הקטע</th><th>הביטוי</th><th>האינטגרל</th></tr></thead>
<tbody>
<tr><td>$[1,\infty)$</td><td>$\dfrac{c}{x^{p}}$</td><td>מתכנס רק אם $p>1$, ואז שווה $\dfrac{c}{p-1}$</td></tr>
<tr><td>$(0,1]$</td><td>$\dfrac{c}{x^{p}}$</td><td>מתכנס רק אם $p<1$, ואז שווה $\dfrac{c}{1-p}$</td></tr>
<tr><td>$(-\infty,0]$</td><td>$c\,e^{x}$</td><td>מתכנס, ושווה $c$</td></tr>
<tr><td>$[0,\infty)$</td><td>$c\,e^{-x}$</td><td>מתכנס, ושווה $c$</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 לדוגמה, $\int_1^\infty\frac{dx}{x}$ מתבדר ($p=1$), ולכן בצפיפות שבה מופיע $\frac cx$ בקטע $[1,\infty)$ מקבלים מיד $c=0$. לעומת זאת $\int_1^\infty\frac{dx}{x^2}=1$ מתכנס, ולכן $\frac{c}{x^2}$ מקבל חלק מהשטח.</div>
<div class="lesson-trap">⚠️ אל תשכחו את הקטע האינסופי. מי שמחשב רק את הקטעים הסופיים ומתעלם מ-$\frac cx$ מפספס את המשוואה $c=0$ ומקבל קבועים שגויים בהמשך.</div>`
  },
  questions: [
    { id: "C03-Q1",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a$ בקטע $[0,1)$, $f(x)=2a$ בקטע $[1,2)$, ו-0 מחוץ לשניהם. מהו $a$? (שבר או עשרוני)",
              answer: 0.333333, tol: 0.001,
              explain: "$\\int_0^1 a\\,dx+\\int_1^2 2a\\,dx=a+2a=3a=1$, ולכן $a=\\frac13$." },
      sim: { kind: "pdf", estimate: "P(X>1)", exact: 0.666666666667, params: { pieces: [{ from: 0, to: 1, expr: "1/3" }, { from: 1, to: 2, expr: "2/3" }], event: "x > 1" } },
      recap: "מפצלים את האינטגרל לפי הקטעים ומחברים." },
    { id: "C03-Q2",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a\\,x$ בקטע $[0,1)$, $f(x)=a$ בקטע $[1,2)$, ו-0 מחוץ לשניהם. מהו $a$? (שבר או עשרוני)",
              answer: 0.666667, tol: 0.001,
              explain: "$\\int_0^1 a\\,x\\,dx+\\int_1^2 a\\,dx=\\frac a2+a=\\frac{3a}{2}=1$, ולכן $a=\\frac23$." },
      sim: { kind: "pdf", estimate: "P(X<1)", exact: 0.333333333333, params: { pieces: [{ from: 0, to: 1, expr: "2/3*x" }, { from: 1, to: 2, expr: "2/3" }], event: "x < 1" } },
      recap: "כל קטע תורם את האינטגרל שלו: $\\frac a2$ ועוד $a$." },
    { id: "C03-Q3",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a\\,e^{x}$ ל-$x<0$ ו-$f(x)=\\frac12 e^{-x}$ ל-$x\\ge0$. מהו $a$? (שבר או עשרוני)",
              answer: 0.5, tol: 0.001,
              explain: "$\\int_{-\\infty}^0 a\\,e^{x}\\,dx=a$ ו-$\\int_0^\\infty\\frac12 e^{-x}\\,dx=\\frac12$. לכן $a+\\frac12=1$ ו-$a=\\frac12$." },
      recap: "$\\int_{-\\infty}^0 e^{x}\\,dx=1$ ו-$\\int_0^\\infty e^{-x}\\,dx=1$." },
    { id: "C03-Q4",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a$ בקטע $[0,1)$ ו-$f(x)=\\dfrac{a}{x^2}$ ל-$x\\ge1$ (ו-0 לפני 0). מהו $a$? (שבר או עשרוני)",
              answer: 0.5, tol: 0.001,
              explain: "$\\int_0^1 a\\,dx=a$ ו-$\\int_1^\\infty\\frac{a}{x^2}\\,dx=a\\cdot\\frac{1}{2-1}=a$. לכן $2a=1$ ו-$a=\\frac12$." },
      recap: "$\\int_1^\\infty x^{-2}\\,dx=1$ מתכנס, ולכן הקטע האינסופי תורם." },
    { id: "C03-Q5", question: "בצפיפות מסוימת מופיע בקטע אחד אחד מהביטויים הבאים, עם קבוע $c$. באיזה מהמקרים האינטגרל של הביטוי מתבדר, ולכן $c$ חייב להיות 0?",
      options: [
        { id: "a", value: "$\\dfrac{c}{x^2}$ בקטע $[1,\\infty)$" },
        { id: "b", value: "$c\\,e^{-x}$ בקטע $[0,\\infty)$" },
        { id: "c", value: "$\\dfrac{c}{\\sqrt{x}}$ בקטע $(0,1]$" },
        { id: "d", value: "$\\dfrac{c}{x}$ בקטע $[1,\\infty)$" }],
      correctId: "d",
      explanation: "$\\int_1^\\infty\\frac{dx}{x}$ מתבדר ($p=1$, ולכן $\\ln x\\to\\infty$), ולכן $c=0$. השאר מתכנסים: $\\int_1^\\infty x^{-2}=1$; $\\int_0^\\infty e^{-x}=1$; $\\int_0^1 x^{-1/2}=2$ (כאן $p=\\frac12<1$).",
      recap: "$\\frac cx$ על $[1,\\infty)$ מתבדר, ולכן $c=0$." },
  ],
});
