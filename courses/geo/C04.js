/* geo, level 4 - conditional probability by area: S(A and B) / S(B). */
COURSE_LEVEL("geo", {
  id: "C04", order: 4, icon: "🎯", title: "הסתברות מותנית: שטח החיתוך חלקי שטח התנאי",
  goal: "אחרי השלב הזה אפשר לחשב $P(A\\mid B)$ בשיטת השטח: לצייר את התנאי, את החיתוך, ולחלק את שני השטחים.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>"בהינתן ש-$B$" מקטין את העולם: הנקודה כבר ידועה כנמצאת באזור $B$, ורק שם מחפשים את $A$. ההסתברות המותנית היא היחס בין שני שטחים.</p>
    <div class="lesson-rule">🔑 $$P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{S(A\cap B)}{S(B)}.$$ המכנה הוא <b>שטח אזור התנאי $B$</b>, <b>לא</b> $|\Omega|$. הגודל $|\Omega|$ מופיע במונה ובמכנה ומצטמצם.</div>
    <p>סדר העבודה: (1) מציירים את אזור התנאי $B$ ומחשבים את שטחו. (2) מציירים את החיתוך $A\cap B$ (החלק של $A$ שנמצא בתוך $B$) ומחשבים את שטחו. (3) מחלקים.</p>
    <div class="lesson-ex"><b>דוגמה.</b> בריבוע היחידה, $P\left(X+Y<1\mid X<\frac12\right)$. התנאי $X<\frac12$ הוא רצועה ברוחב $\frac12$ ובגובה $1$, שטחה $\frac12$. החיתוך: הנקודות עם $x<\frac12$ מתחת לקו $y=1-x$. שטחו $\int_0^{1/2}(1-x)\,dx=\frac12-\frac18=\frac38$. לכן $P=\dfrac{3/8}{1/2}=\dfrac34$.</div>
    <div class="region-fig" data-region='{"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": 1, "c": 1, "op": "<"}], "given": [{"a": 1, "b": 0, "c": "1/2", "op": "<"}], "labels": {"x": "X", "y": "Y"}, "caption": "X+Y<1 בהינתן X<1/2"}'></div>
    <p>באיור, האזור המקווקו הוא התנאי, והגוון החזק הוא החיתוך.</p>
    <div class="lesson-trap">⚠️ שתי טעויות נפוצות: לחלק ב-$|\Omega|$ במקום בשטח התנאי, או לחשב את שטח $A$ כולו ולא רק את החלק שבתוך $B$.</div>` },
  questions: [
    { id: "geo-C04-Q1",
      step: { type: "numeric", answer: 0.5, tol: 0,
              prompt: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מחשבים $P\\left(X<\\frac14\\mid X+Y<1\\right)$. מהו שטח אזור התנאי $\\{X+Y<1\\}$, כלומר המכנה? (אפשר שבר או עשרוני)",
              explain: "אזור התנאי הוא משולש בפינת הראשית עם ניצבים $1$ ו-$1$, ושטחו $\\frac12$." },
      recap: "המכנה הוא שטח אזור התנאי." },
    { id: "geo-C04-Q2",
      step: { type: "numeric", answer: 0.21875, tol: 0.002,
              prompt: "באותו ניסוי ($X,Y\\sim U_c(0,1)$ בלתי תלויים), מחשבים $P\\left(X<\\frac14\\mid X+Y<1\\right)$. מהו שטח החיתוך $\\{X<\\frac14\\}\\cap\\{X+Y<1\\}$, כלומר המונה? (אפשר שבר או עשרוני)",
              explain: "החיתוך הוא הנקודות עם $x<\\frac14$ מתחת לקו $y=1-x$: טרפז. שטחו $\\int_0^{1/4}(1-x)\\,dx=\\frac14-\\frac1{32}=\\frac7{32}\\approx0.219$." },
      recap: "המונה הוא שטח החיתוך, לא שטח $A$ כולו." },
    { id: "geo-C04-Q3",
      question: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P\\left(X<\\frac14\\mid X+Y<1\\right)$ ?",
      options: [{ id: "a", value: "$\\frac{7}{16}$" }, { id: "b", value: "$\\frac{7}{32}$" }, { id: "c", value: "$\\frac14$" }, { id: "d", value: "$\\frac{7}{8}$" }],
      correctId: "a",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 0, c: "1/4", op: "<" }], given: [{ a: 1, b: 1, c: 1, op: "<" }], labels: { x: "X", y: "Y" }, caption: "X<1/4 בהינתן X+Y<1" },
      sim: { kind: "area", estimate: "P(X<1/4 | X+Y<1)", exact: 7 / 16, params: { space: { x: [0, 1], y: [0, 1] }, event: "x<1/4", given: "x+y<1" } },
      explanation: "שטח החיתוך $\\frac7{32}$, שטח התנאי $\\frac12$, ולכן $P=\\frac{7/32}{1/2}=\\frac7{16}$. התשובה $\\frac7{32}$ היא שטח החיתוך בלבד (חלוקה ב-$|\\Omega|=1$ במקום בשטח התנאי). התשובה $\\frac14$ היא $P(X<\\frac14)$ בלי התנאי.",
      recap: "$\\frac{S(A\\cap B)}{S(B)}$ ולא $S(A\\cap B)$." },
    { id: "geo-C04-Q4",
      step: { type: "numeric", answer: 0.3333, tol: 0.004,
              prompt: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. חשבו את $P\\left(Y<1\\mid X+Y>1\\right)$. (אפשר שבר או עשרוני)",
              explain: "במלבן $(0,1)\\times(0,2)$ אזור התנאי $x+y>1$ הוא המלבן פחות משולש הפינה (ניצבים $1$): שטחו $2-\\frac12=\\frac32$. החיתוך עם $y<1$ הוא המשולש שבתוך ריבוע היחידה מעל הקו $x+y=1$, ושטחו $\\frac12$. לכן $P=\\frac{1/2}{3/2}=\\frac13$. אם מחלקים ב-$|\\Omega|=2$ מקבלים $\\frac14$, וזו טעות." },
      region: { space: { x: [0, 1], y: [0, 2] }, event: [{ a: 0, b: 1, c: 1, op: "<" }], given: [{ a: 1, b: 1, c: 1, op: ">" }], labels: { x: "X", y: "Y" }, caption: "Y<1 בהינתן X+Y>1" },
      sim: { kind: "area", estimate: "P(Y<1 | X+Y>1)", exact: 1 / 3, params: { space: { x: [0, 1], y: [0, 2] }, event: "y<1", given: "x+y>1" } },
      recap: "מחלקים בשטח התנאי ($\\frac32$), לא ב-$|\\Omega|=2$." },
    { id: "geo-C04-Q5",
      step: { type: "numeric", answer: 0.25, tol: 0.005,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. חשבו את $P\\left(X>\\frac12\\mid Y>X\\right)$. (אפשר שבר או עשרוני)",
              explain: "אזור התנאי $y>x$ הוא המשולש העליון, ושטחו $\\frac12$. החיתוך עם $x>\\frac12$ הוא משולש עם הקודקודים $(\\frac12,\\frac12)$, $(\\frac12,1)$, $(1,1)$ עם ניצבים $\\frac12$ ו-$\\frac12$, ושטחו $\\frac18$. לכן $P=\\frac{1/8}{1/2}=\\frac14$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 0, c: "1/2", op: ">" }], given: [{ a: -1, b: 1, c: 0, op: ">" }], labels: { x: "X", y: "Y" }, caption: "X>1/2 בהינתן Y>X" },
      sim: { kind: "area", estimate: "P(X>1/2 | Y>X)", exact: 0.25, params: { space: { x: [0, 1], y: [0, 1] }, event: "x>1/2", given: "y>x" } },
      recap: "מציירים את התנאי, ואז את החיתוך בתוכו." },
  ],
});
