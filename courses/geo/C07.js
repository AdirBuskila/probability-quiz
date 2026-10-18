/* geo, level 7 - CDF of a ratio X/Y and a product XY. */
COURSE_LEVEL("geo", {
  id: "C07", order: 7, icon: "✖️", title: "יחס ומכפלה",
  goal: "אחרי השלב הזה אפשר לחשב את ההתפלגות המצטברת של היחס $X/Y$ ושל המכפלה $XY$, ולהשתמש בה לחישוב הסתברויות.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <h3>היחס $Z=X/Y$</h3>
    <p>$\dfrac XY<t$ שקול ל-$Y>\dfrac Xt$, זו חצי-מישור מעל <b>קו דרך הראשית</b> $y=\dfrac xt$. בריבוע היחידה יש שני מקרים, לפי המקום שבו הקו יוצא מהריבוע.</p>
    <ul>
      <li>$0<t\le1$: הקו $y=\frac xt$ תלול ופוגש את הצלע העליונה $y=1$ ב-$x=t$. האזור הוא משולש עם קודקודים $(0,0),(0,1),(t,1)$ ושטחו $\frac t2$. כלומר $F(t)=\dfrac t2$.</li>
      <li>$t>1$: הקו מתון ופוגש את הצלע הימנית $x=1$ ב-$y=\frac1t$. המשלים הוא משולש עם קודקודים $(0,0),(1,0),(1,\frac1t)$ ושטחו $\frac1{2t}$. כלומר $F(t)=1-\dfrac1{2t}$.</li>
    </ul>
    <div class="region-fig" data-region='{"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": -2, "c": 0, "op": "<"}], "labels": {"x": "X", "y": "Y"}, "caption": "X/Y<2, כלומר Y>X/2"}'></div>
    <h3>המכפלה $Z=XY$</h3>
    <div class="lesson-rule">🔑 בריבוע היחידה, עבור $0<t<1$: $$F_{XY}(t)=P(XY\le t)=t-t\ln t.$$ (השטח $t$ עבור $x<t$, ועוד $\int_t^1\frac tx\,dx=-t\ln t$.)</div>
    <div class="lesson-ex"><b>דוגמה.</b> $P(\frac XY<\frac12)=F(\frac12)=\frac14$, ו-$P(\frac XY<2)=1-\frac14=\frac34$.</div>
    <p><b>כשהמשתנים לא באותו טווח</b> (למשל $Y\sim U_c(0,2)$) לא משתמשים בטבלה אלא מציירים את הקו בתוך המלבן המתאים ומחשבים שטח, ואז מחלקים ב-$|\Omega|$.</p>
    <div class="lesson-trap">⚠️ שתי הנוסחאות של היחס מחליפות מקום ב-$t=1$: לפני $t=1$ זה משולש שהוא האירוע עצמו, ואחרי $t=1$ זה משלים של משולש. ב-$t=1$ שתיהן נותנות $\frac12$.</div>` },
  questions: [
    { id: "geo-C07-Q1",
      step: { type: "numeric", answer: 0.1667, tol: 0.004,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P\\left(\\frac XY<\\frac13\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "$\\frac XY<\\frac13\\iff y>3x$. הקו $y=3x$ פוגש את $y=1$ ב-$x=\\frac13$. האזור הוא משולש עם קודקודים $(0,0),(0,1),(\\frac13,1)$, בסיס $\\frac13$ וגובה $1$, ושטחו $\\frac16$. זה גם $F(t)=\\frac t2$ ב-$t=\\frac13$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 3, b: -1, c: 0, op: "<" }], labels: { x: "X", y: "Y" }, caption: "X/Y<1/3, כלומר Y>3X" },
      sim: { kind: "area", estimate: "P(X/Y<1/3)", exact: 1 / 6, params: { space: { x: [0, 1], y: [0, 1] }, event: "x/y<1/3" } },
      recap: "$F(t)=\\frac t2$ עבור $t\\le1$." },
    { id: "geo-C07-Q2",
      step: { type: "numeric", answer: 0.25, tol: 0.005,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P\\left(\\frac XY>2\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "$\\frac XY>2\\iff y<\\frac x2$. הקו $y=\\frac x2$ פוגש את $x=1$ ב-$y=\\frac12$. האזור הוא משולש עם קודקודים $(0,0),(1,0),(1,\\frac12)$ ושטחו $\\frac12\\cdot1\\cdot\\frac12=\\frac14$. (בנוסחה: $1-F(2)=1-\\left(1-\\frac14\\right)=\\frac14$.)" },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: -2, c: 0, op: ">" }], labels: { x: "X", y: "Y" }, caption: "X/Y>2, כלומר Y<X/2" },
      sim: { kind: "area", estimate: "P(X/Y>2)", exact: 0.25, params: { space: { x: [0, 1], y: [0, 1] }, event: "x/y>2" } },
      recap: "$t>1$: המשלים הוא משולש בשטח $\\frac1{2t}$." },
    { id: "geo-C07-Q3",
      question: "$X,Y\\sim U_c(0,1)$ בלתי תלויים ו-$Z=\\frac XY$. מהי $F_Z(t)$ עבור $t>1$ ?",
      options: [{ id: "a", value: "$1-\\frac{1}{2t}$" }, { id: "b", value: "$\\frac t2$" }, { id: "c", value: "$\\frac{1}{2t}$" }, { id: "d", value: "$1-\\frac t2$" }],
      correctId: "a",
      explanation: "עבור $t>1$ המשלים $\\{Z>t\\}$ הוא משולש בשטח $\\frac1{2t}$, ולכן $F(t)=1-\\frac1{2t}$. התשובה $\\frac t2$ היא הנוסחה של $t\\le1$ וחורגת מ-$1$ כש-$t>2$. התשובה $\\frac1{2t}$ היא $P(Z>t)$, והתשובה $1-\\frac t2$ יורדת כש-$t$ גדל, ולכן אינה יכולה להיות התפלגות מצטברת. בדיקה: ב-$t=1$ צריך לקבל $\\frac12$ וגם $F\\to1$ כש-$t\\to\\infty$.",
      recap: "$F(t)=1-\\frac1{2t}$ עבור $t>1$." },
    { id: "geo-C07-Q4",
      step: { type: "numeric", answer: 0.3303, tol: 0.002,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. חשבו את $P\\left(XY<\\frac1{10}\\right)$. (עשרוני, ארבע ספרות)",
              explain: "לפי $F_{XY}(t)=t-t\\ln t$ ב-$t=\\frac1{10}$: $\\frac1{10}+\\frac1{10}\\ln10\\approx0.1+0.2303=0.3303$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ expr: "x*y", op: "<", c: "1/10" }], labels: { x: "X", y: "Y" }, caption: "XY<1/10" },
      sim: { kind: "area", estimate: "P(XY<1/10)", exact: 0.1 + 0.1 * Math.log(10), params: { space: { x: [0, 1], y: [0, 1] }, event: "x*y<1/10" } },
      recap: "$F_{XY}(t)=t-t\\ln t$." },
    { id: "geo-C07-Q5",
      step: { type: "numeric", answer: 0.1534, tol: 0.002,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. חשבו את $P\\left(XY>\\frac12\\right)$. (עשרוני, ארבע ספרות)",
              explain: "$P(XY\\le\\frac12)=\\frac12-\\frac12\\ln\\frac12=\\frac12+\\frac12\\ln2\\approx0.8466$. המשלים $\\frac12-\\frac12\\ln2\\approx0.1534$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ expr: "x*y", op: ">", c: "1/2" }], labels: { x: "X", y: "Y" }, caption: "XY>1/2" },
      sim: { kind: "area", estimate: "P(XY>1/2)", exact: 0.5 - 0.5 * Math.log(2), params: { space: { x: [0, 1], y: [0, 1] }, event: "x*y>1/2" } },
      recap: "\"גדול מ-$t$\" הוא $1-F(t)$." },
    { id: "geo-C07-Q6",
      step: { type: "numeric", answer: 0.25, tol: 0.005,
              prompt: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. מהי $P\\left(\\frac YX<1\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "$\\frac YX<1\\iff y<x$ (כי $x>0$). $|\\Omega|=1\\cdot2=2$. האזור $y<x$ בתוך המלבן $(0,1)\\times(0,2)$ הוא משולש עם ניצבים $1$ ו-$1$, ושטחו $\\frac12$. לכן $P=\\frac{1/2}{2}=\\frac14$ (ולא $\\frac12$ כמו בריבוע היחידה)." },
      region: { space: { x: [0, 1], y: [0, 2] }, event: [{ a: -1, b: 1, c: 0, op: "<" }], labels: { x: "X", y: "Y" }, caption: "Y/X<1 במלבן (0,1)x(0,2)" },
      sim: { kind: "area", estimate: "P(Y/X<1)", exact: 0.25, params: { space: { x: [0, 1], y: [0, 2] }, event: "y/x<1" } },
      recap: "מחלקים ב-$|\\Omega|$ כשהמלבן לא ריבוע." },
  ],
});
