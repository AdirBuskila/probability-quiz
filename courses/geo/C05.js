/* geo, level 5 - curved boundaries: xy<c (hyperbola), y<x^2 (parabola), x^2+y^2<r^2 (circle). Area by integral. */
COURSE_LEVEL("geo", {
  id: "C05", order: 5, icon: "〰️", title: "קימורים: היפרבולה, פרבולה ומעגל",
  goal: "אחרי השלב הזה אפשר לחשב שטח מתחת להיפרבולה, מתחת לפרבולה וברבע עיגול, ולהפוך אותו להסתברות.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>לפעמים הגבול של האירוע הוא לא קו ישר אלא <b>עקום</b>. הדרך לא משתנה: מציירים את הגבול, בוחרים צד, ומחשבים שטח. רק שהשטח כבר לא משולש, אלא <b>אינטגרל</b>.</p>
    <div class="lesson-rule">🔑 השטח מתחת לעקום $y=f(x)$ מ-$x=a$ עד $x=b$ הוא $\int_a^b f(x)\,dx$. כשהעקום חורג מגבולות הריבוע, חותכים את התחום ל<b>קטעים</b>: בכל קטע הגובה הוא אחד מהשניים, העקום או הצלע של הריבוע.</div>
    <h3>המכפלה $XY<c$</h3>
    <p>האי-שוויון שקול ל-$y<\dfrac cx$, היפרבולה. בריבוע היחידה עם $c<1$: לכל $x<c$ העקום גבוה מ-$1$, ולכן כל $y\in(0,1)$ מתאים (שטח $c$ בסך הכול). לכל $x>c$ השטח הוא האינטגרל $\int_c^1\dfrac cx\,dx=c\ln\dfrac1c$.</p>
    <div class="lesson-ex"><b>דוגמה.</b> $P(XY<\frac14)$: שטח $\frac14$ עבור $x<\frac14$, ועוד $\int_{1/4}^{1}\frac{1}{4x}dx=\frac14\ln4$. בסך הכול $\frac14+\frac14\ln4=\frac14+\frac12\ln2\approx0.597$.</div>
    <div class="region-fig" data-region='{"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"expr": "x*y", "op": "<", "c": "1/4"}], "labels": {"x": "X", "y": "Y"}, "caption": "XY<1/4"}'></div>
    <h3>הפרבולה $Y<X^2$ והמעגל</h3>
    <p>האזור $y<x^2$ בריבוע היחידה הוא מתחת לפרבולה, ושטחו $\int_0^1x^2\,dx=\frac13$. ההסתברות $P(Y>X^2)$ היא המשלים, $\frac23$.</p>
    <p>האי-שוויון $x^2+y^2<r^2$ (המרחק מהראשית קטן מ-$r$) הוא <b>רבע עיגול</b> ברדיוס $r$ כש-$r\le1$, ושטחו $\dfrac{\pi r^2}{4}$.</p>
    <div class="lesson-trap">⚠️ ב-$\int\frac1x\,dx=\ln x$ מציבים את הגבולות כ-$\ln b-\ln a$. לא לשכוח את הקטע $x<c$ שבו העקום מעל הריבוע: אם מדלגים עליו, השטח קטן מדי.</div>` },
  questions: [
    { id: "geo-C05-Q1",
      question: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P(Y<X^2)$ ?",
      options: [{ id: "a", value: "$\\frac13$" }, { id: "b", value: "$\\frac23$" }, { id: "c", value: "$\\frac12$" }, { id: "d", value: "$\\frac14$" }],
      correctId: "a",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ expr: "y-x^2", op: "<", c: 0 }], labels: { x: "X", y: "Y" }, caption: "Y<X^2" },
      sim: { kind: "area", estimate: "P(Y<X^2)", exact: 1 / 3, params: { space: { x: [0, 1], y: [0, 1] }, event: "y<x^2" } },
      explanation: "השטח מתחת לפרבולה הוא $\\int_0^1x^2\\,dx=\\frac13$, ו-$|\\Omega|=1$. התשובה $\\frac23$ היא $P(Y>X^2)$, האזור שמעל הפרבולה. התשובה $\\frac12$ מתאימה לאלכסון, לא לפרבולה.",
      recap: "שטח מתחת לעקום: אינטגרל." },
    { id: "geo-C05-Q2",
      step: { type: "numeric", answer: 0.5219, tol: 0.003,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. חשבו את $P\\left(XY<\\frac15\\right)$. (עשרוני, אפשר לעגל לשלוש ספרות)",
              explain: "$XY<\\frac15\\iff y<\\frac1{5x}$. לכל $x<\\frac15$ כל $y$ מתאים: שטח $\\frac15$. עבור $\\frac15<x<1$ השטח הוא $\\int_{1/5}^1\\frac{dx}{5x}=\\frac15\\ln5$. בסך הכול $\\frac{1+\\ln5}{5}\\approx0.522$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ expr: "x*y", op: "<", c: "1/5" }], labels: { x: "X", y: "Y" }, caption: "XY<1/5" },
      sim: { kind: "area", estimate: "P(XY<1/5)", exact: (1 + Math.log(5)) / 5, params: { space: { x: [0, 1], y: [0, 1] }, event: "x*y<1/5" } },
      recap: "היפרבולה: $c+c\\ln\\frac1c$ בריבוע היחידה." },
    { id: "geo-C05-Q3",
      question: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P\\left(XY<\\frac13\\right)$ ?",
      options: [{ id: "a", value: "$\\frac{1+\\ln3}{3}$" }, { id: "b", value: "$\\frac{\\ln3}{3}$" }, { id: "c", value: "$\\frac13+\\ln3$" }, { id: "d", value: "$1-\\frac{\\ln3}{3}$" }],
      correctId: "a",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ expr: "x*y", op: "<", c: "1/3" }], labels: { x: "X", y: "Y" }, caption: "XY<1/3" },
      sim: { kind: "area", estimate: "P(XY<1/3)", exact: (1 + Math.log(3)) / 3, params: { space: { x: [0, 1], y: [0, 1] }, event: "x*y<1/3" } },
      explanation: "עבור $x<\\frac13$: שטח $\\frac13$. עבור $\\frac13<x<1$: $\\int_{1/3}^1\\frac{dx}{3x}=\\frac13\\ln3$. הסכום $\\frac{1+\\ln3}3\\approx0.70$. התשובה $\\frac{\\ln3}3$ מפספסת את הקטע $x<\\frac13$. התשובה $\\frac13+\\ln3$ גדולה מ-$1$ ולכן אינה הסתברות. התשובה $1-\\frac{\\ln3}3$ היא לא המשלים הנכון.",
      recap: "שני קטעים: $x<c$ (הכול) ו-$x>c$ (אינטגרל)." },
    { id: "geo-C05-Q4",
      step: { type: "numeric", answer: 0.0873, tol: 0.001,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. חשבו את ההסתברות שהמרחק של הנקודה $(X,Y)$ מהראשית קטן מ-$\\frac13$. (עשרוני, ארבע ספרות אחרי הנקודה)",
              explain: "$\\sqrt{x^2+y^2}<\\frac13$ הוא רבע עיגול ברדיוס $\\frac13$ בתוך הריבוע. שטחו $\\frac{\\pi}{4}\\cdot\\frac19=\\frac{\\pi}{36}\\approx0.0873$, ו-$|\\Omega|=1$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ expr: "x^2+y^2", op: "<", c: "1/9" }], labels: { x: "X", y: "Y" }, caption: "המרחק מהראשית קטן מ-1/3" },
      sim: { kind: "area", estimate: "P(sqrt(X^2+Y^2)<1/3)", exact: Math.PI / 36, params: { space: { x: [0, 1], y: [0, 1] }, event: "x^2+y^2<1/9" } },
      recap: "רבע עיגול ברדיוס $r$: $\\frac{\\pi r^2}4$." },
    { id: "geo-C05-Q5",
      step: { type: "numeric", answer: 0.8333, tol: 0.004,
              prompt: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. חשבו את $P\\left(Y>X^2\\right)$. (אפשר שבר או עשרוני)",
              explain: "$|\\Omega|=1\\cdot2=2$. השטח מתחת לפרבולה בתוך המלבן הוא $\\int_0^1x^2\\,dx=\\frac13$ (הפרבולה לא עוברת את גובה $1$). השטח מעליה הוא $2-\\frac13=\\frac53$, ולכן $P=\\frac{5/3}{2}=\\frac56$." },
      region: { space: { x: [0, 1], y: [0, 2] }, event: [{ expr: "y-x^2", op: ">", c: 0 }], labels: { x: "X", y: "Y" }, caption: "Y>X^2 במלבן (0,1)x(0,2)" },
      sim: { kind: "area", estimate: "P(Y>X^2)", exact: 5 / 6, params: { space: { x: [0, 1], y: [0, 2] }, event: "y>x^2" } },
      recap: "במלבן $(0,1)\\times(0,2)$: מחלקים ב-$2$." },
  ],
});
