/* pdf course, level 2 - normalizing one unknown constant. Checked by tools/verify/needhelp/pdf/check.py */
COURSE_LEVEL("pdf", {
  id: "C02", order: 2, icon: "🎯", title: "נרמול: מציאת קבוע אחד",
  goal: "אחרי השלב הזה אפשר למצוא קבוע לא ידוע בצפיפות מהתנאי שהשטח הכולל הוא 1.",
  source: "ai-verified",
  lesson: {
    html: String.raw`
<p>במבחן נותנים צפיפות עם קבוע לא ידוע, למשל $f(x)=c\,x$, ושואלים מהו $c$. הקבוע נקבע מהתנאי היחיד שלא ויתרנו עליו: <b>השטח הכולל הוא 1</b>.</p>
<div class="lesson-rule">🔑 <b>המתכון:</b> (1) כותבים $\int f(x)\,dx=1$ על התחום. (2) מחשבים את האינטגרל, והתוצאה היא ביטוי ב-$c$ (הקבוע יוצא מהאינטגרל). (3) פותרים משוואה ליניארית אחת ב-$c$.</div>
<div class="lesson-ex">דוגמה: $f(x)=c\,x^2$ בקטע $[0,1]$. הנרמול: $\int_0^1 c\,x^2\,dx=c\cdot\dfrac13=1$, ולכן $c=3$.</div>
<p>אינטגרלים שנשתמש בהם:</p>
<table>
<thead><tr><th>אינטגרל</th><th>ערך</th></tr></thead>
<tbody>
<tr><td>$\int_a^b x^n\,dx$</td><td>$\dfrac{b^{n+1}-a^{n+1}}{n+1}$</td></tr>
<tr><td>$\int_0^\infty e^{-kx}\,dx$ (עבור $k>0$)</td><td>$\dfrac1k$</td></tr>
</tbody></table>
<div class="lesson-trap">⚠️ טעות נפוצה: לשכוח את הגבול התחתון, או לחשב $\left[\frac{x^2}{2}\right]_0^{3}$ כ-$\frac32$ במקום $\frac92$. מציבים את הגבול בריבוע.</div>
<p>בדיקה מהירה אחרי שמצאתם $c$: הוא צריך לגרום ל-$f\ge0$ בכל התחום (כאן $c>0$), והשטח הוא 1 מעצם הפתרון.</p>`
  },
  questions: [
    { id: "C02-Q1",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=c\\,x$ בקטע $[0,2]$ (ו-0 מחוץ לו). מהו $c$? (שבר או עשרוני)",
              answer: 0.5, tol: 0.001,
              explain: "$\\int_0^2 c\\,x\\,dx=c\\cdot\\frac{2^2}{2}=2c=1$, ולכן $c=\\frac12$." },
      sim: { kind: "pdf", estimate: "P(X<1)", exact: 0.25, params: { pieces: [{ from: 0, to: 2, expr: "x/2" }], event: "x < 1" } },
      recap: "מציבים את הגבול בריבוע ומחלקים ב-2." },
    { id: "C02-Q2",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=c\\,x^2$ בקטע $[0,3]$. מהו $c$? (שבר או עשרוני, אפשר להקליד 1/9)",
              answer: 0.111111, tol: 0.0005,
              explain: "$\\int_0^3 c\\,x^2\\,dx=c\\cdot\\frac{3^3}{3}=9c=1$, ולכן $c=\\frac19\\approx0.1111$." },
      sim: { kind: "pdf", estimate: "P(X<1)", exact: 0.037037037037, params: { pieces: [{ from: 0, to: 3, expr: "x^2/9" }], event: "x < 1" } },
      recap: "$\\int_0^b x^2 = b^3/3$." },
    { id: "C02-Q3",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=c\\,(1-x^2)$ בקטע $[-1,1]$. מהו $c$? (שבר או עשרוני)",
              answer: 0.75, tol: 0.001,
              explain: "$\\int_{-1}^{1}c(1-x^2)\\,dx=c\\left[x-\\frac{x^3}{3}\\right]_{-1}^{1}=c\\left(\\frac23+\\frac23\\right)=\\frac{4c}{3}=1$, ולכן $c=\\frac34$." },
      sim: { kind: "pdf", estimate: "P(X>0)", exact: 0.5, params: { pieces: [{ from: -1, to: 1, expr: "3/4*(1-x^2)" }], event: "x > 0" } },
      recap: "גבולות שליליים: מציבים את שני הקצוות." },
    { id: "C02-Q4",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=c\\,e^{-2x}$ לכל $x\\ge0$ (ו-0 לפני כן). מהו $c$?",
              answer: 2, tol: 0,
              explain: "$\\int_0^\\infty c\\,e^{-2x}\\,dx=c\\cdot\\frac12=1$, ולכן $c=2$." },
      recap: "$\\int_0^\\infty e^{-kx}\\,dx=\\frac1k$." },
    { id: "C02-Q5",
      step: { type: "findbug",
              prompt: "הצפיפות היא $f(x)=c\\,x$ בקטע $[0,3]$. בפתרון הנרמול הבא נפלה טעות. באיזו שורה היא נעשתה לראשונה?",
              lines: [
                "$\\int_0^3 c\\,x\\,dx=1$",
                "$c\\left[\\dfrac{x^2}{2}\\right]_0^3=1$",
                "$c\\cdot\\dfrac{3}{2}=1$",
                "$c=\\dfrac23$"],
              bugIndex: 2,
              explain: "הציבו $3$ במקום $3^2=9$: $\\left[\\frac{x^2}{2}\\right]_0^3=\\frac92$. המשוואה הנכונה היא $c\\cdot\\frac92=1$, ולכן $c=\\frac29$. השורה האחרונה רק ממשיכה את הטעות." },
      recap: "ב-$\\frac{x^2}{2}$ מציבים את הגבול בריבוע." },
  ],
});
