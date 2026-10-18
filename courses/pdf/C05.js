/* pdf course, level 5 - the cumulative distribution function piece by piece. Checked by tools/verify/needhelp/pdf/check.py */
COURSE_LEVEL("pdf", {
  id: "C05", order: 5, icon: "📊", title: "התפלגות מצטברת קטע אחר קטע",
  goal: "אחרי השלב הזה אפשר לבנות את ההתפלגות המצטברת מצפיפות מחולקת לקטעים, לבדוק רציפות בנקודות החיבור, ולזהות את הגרף הנכון.",
  source: "ai-verified",
  lesson: {
    html: String.raw`
<p>ההתפלגות המצטברת היא השטח שנצבר משמאל עד הנקודה $t$:</p>
<div class="lesson-formula">$$F_X(t)=P(X\le t)=\int_{-\infty}^{t}f_X(x)\,dx$$</div>
<p>הקשר ההפוך: $f_X(x)=F_X'(x)$, כלומר הצפיפות היא השיפוע של $F$.</p>
<div class="lesson-rule">🔑 <b>המתכון קטע אחר קטע:</b> אם קטע מתחיל ב-$t_0$, אז לכל $t$ בקטע
$$F(t)=F(t_0)+\int_{t_0}^{t}f(x)\,dx.$$
<b>כל קטע מוסיף למה שכבר נצבר.</b> לפני הקטע הראשון $F=0$, ואחרי הקטע האחרון $F=1$.</div>
<div class="lesson-ex">הצפיפות $f(x)=x$ ל-$0\le x<1$, ו-$f(x)=\tfrac12$ ל-$1\le x<2$. הקטע הראשון: $F(t)=\int_0^t x\,dx=\tfrac{t^2}{2}$, ולכן $F(1)=\tfrac12$. הקטע השני מתחיל מ-$\tfrac12$ ולא מ-0: $F(t)=\tfrac12+\int_1^t\tfrac12\,dx=\tfrac12+\tfrac{t-1}{2}=\tfrac t2$. בסוף $F(2)=1$.</div>
<p>בדיקות שחייבות להצליח: $F$ רציפה (בנקודות החיבור שני הקטעים נותנים אותו ערך: כאן $\tfrac{1}{2}$ בשניהם ב-$t=1$), לא יורדת, מתחילה ב-0 ומסתיימת ב-1.</p>
<div class="lesson-trap">⚠️ אם הקטע השני כתוב $\tfrac{t-1}{2}$ בלי ה-$\tfrac12$ שנצבר, הגרף "קופץ למטה" ב-$t=1$ ונגמר ב-$\tfrac12$ במקום ב-1. זו הטעות הנפוצה ביותר בשאלות $F$.</div>`,
    figs: [{ src: "images/exams/crs-pdf-l5-pdf-cdf.png", alt: "משמאל הצפיפות f, מימין ההתפלגות המצטברת F שעולה ברציפות מ-0 עד 1", caption: "הצפיפות (משמאל) וההתפלגות המצטברת שלה (מימין)." }]
  },
  questions: [
    { id: "C05-Q1",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=x$ בקטע $[0,1)$, $f(x)=\\frac12$ בקטע $[1,2)$, ו-0 מחוץ לשניהם. מהו $F_X(1)$? (שבר או עשרוני)",
              answer: 0.5, tol: 0.001,
              explain: "$F(1)=\\int_0^1 x\\,dx=\\frac12$." },
      recap: "$F(t_0)$ בסוף קטע הוא כל מה שנצבר עד אליו." },
    { id: "C05-Q2",
      step: { type: "numeric",
              prompt: "בצפיפות של השאלה הקודמת ($x$ על $[0,1)$ ו-$\\frac12$ על $[1,2)$), מהו $F_X(\\frac32)$? (שבר או עשרוני)",
              answer: 0.75, tol: 0.001,
              explain: "$F(\\frac32)=F(1)+\\int_1^{3/2}\\frac12\\,dx=\\frac12+\\frac14=\\frac34$. (מהנוסחה $F(t)=\\frac t2$ מקבלים אותו ערך.)" },
      sim: { kind: "pdf", estimate: "F(3/2)", exact: 0.75, params: { pieces: [{ from: 0, to: 1, expr: "x" }, { from: 1, to: 2, expr: "1/2" }], event: "x <= 3/2" } },
      recap: "בקטע השני מוסיפים למה שנצבר: $F(1)$ ועוד שטח." },
    { id: "C05-Q3", question: "הצפיפות היא $f(x)=x$ בקטע $[0,1)$, $f(x)=\\frac12$ בקטע $[1,2)$, ו-0 מחוץ לשניהם. איזה ביטוי הוא $F_X(t)$ עבור $1\\le t<2$?",
      options: [
        { id: "a", value: "$\\dfrac{t-1}{2}$" },
        { id: "b", value: "$\\dfrac{t}{2}$" },
        { id: "c", value: "$\\dfrac{t^2}{2}$" },
        { id: "d", value: "$\\dfrac12+\\dfrac{t^2}{4}$" }],
      correctId: "b",
      explanation: "$F(t)=F(1)+\\int_1^t\\frac12\\,dx=\\frac12+\\frac{t-1}{2}=\\frac t2$. הביטוי $\\frac{t-1}{2}$ שוכח את $F(1)=\\frac12$ שנצבר (ולכן לא רציף ב-$t=1$). $\\frac{t^2}{2}$ ממשיך את הקטע הראשון, ו-$\\frac12+\\frac{t^2}{4}$ הוא אינטגרל של $x$ במקום הקבוע $\\frac12$.",
      recap: "$F(t)=F(t_0)+\\int_{t_0}^t f$." },
    { id: "C05-Q4", question: "הצפיפות היא $f(x)=x$ בקטע $[0,1)$, $f(x)=\\frac12$ בקטע $[1,2)$, ו-0 מחוץ לשניהם. איזה גרף הוא ההתפלגות המצטברת $F_X(t)$?",
      options: [
        { id: "a", type: "image", value: "images/exams/crs-pdf-l5-optB.png" },
        { id: "b", type: "image", value: "images/exams/crs-pdf-l5-optD.png" },
        { id: "c", type: "image", value: "images/exams/crs-pdf-l5-optA.png" },
        { id: "d", type: "image", value: "images/exams/crs-pdf-l5-optC.png" }],
      correctId: "c",
      explanation: "ההתפלגות המצטברת רציפה, לא יורדת, מתחילה ב-0 ומסתיימת ב-1. הגרף שקופץ למטה ב-$t=1$ שכח לצבור. הגרף שנראה כמו הצפיפות (עולה לינארית ואז שטוח) הוא הצפיפות עצמה. והגרף שעובר את 1 המשיך את $\\frac{t^2}{2}$ גם בקטע השני.",
      recap: "$F$ רציפה, עולה, מ-0 עד 1." },
    { id: "C05-Q5",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=\\frac23$ בקטע $[0,1)$, $f(x)=\\frac13$ בקטע $[1,2)$, ו-0 מחוץ לשניהם. מהו $F_X(\\frac32)$? (שבר או עשרוני)",
              answer: 0.833333, tol: 0.001,
              explain: "$F(1)=\\frac23$. אחר כך $F(\\frac32)=\\frac23+\\frac13\\cdot\\frac12=\\frac23+\\frac16=\\frac56$." },
      sim: { kind: "pdf", estimate: "F(3/2)", exact: 0.833333333333, params: { pieces: [{ from: 0, to: 1, expr: "2/3" }, { from: 1, to: 2, expr: "1/3" }], event: "x <= 3/2" } },
      recap: "מצטברים: שטח הקטע הראשון, ועוד חלק מהשני." },
    { id: "C05-Q6",
      step: { type: "numeric",
              prompt: "ההתפלגות המצטברת של $X$ היא $F_X(t)=t^3$ ל-$0\\le t\\le1$ (0 לפני כן, 1 אחרי כן). מהי הצפיפות $f_X(\\frac12)$? (שבר או עשרוני)",
              answer: 0.75, tol: 0.001,
              explain: "הצפיפות היא הנגזרת של $F$: $f(t)=3t^2$, ולכן $f(\\frac12)=3\\cdot\\frac14=\\frac34$." },
      recap: "$f=F'$." },
  ],
});
