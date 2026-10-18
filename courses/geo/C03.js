/* geo, level 3 - bands (|X-Y|<c), two inequalities at once, triangles, complement of "or". */
COURSE_LEVEL("geo", {
  id: "C03", order: 3, icon: "🔺", title: "רצועות ומשולשים",
  goal: "אחרי השלב הזה אפשר לחשב הסתברות של רצועה סביב האלכסון ושל חיתוך של שני אי-שוויונות.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>הרבה שאלות שואלות אם שני מספרים <b>קרובים</b> זה לזה: "ההפרש קטן מ-$c$". זה אי-שוויון עם ערך מוחלט, והוא מתפרק לשני אי-שוויונות.</p>
    <div class="lesson-rule">🔑 $\lvert X-Y\rvert<c \iff -c<X-Y<c \iff Y>X-c$ <b>וגם</b> $Y<X+c$. זו <b>רצועה</b> סביב האלכסון, בין הקווים $y=x-c$ ו-$y=x+c$.</div>
    <p>את שטח הרצועה בריבוע היחידה מחשבים דרך המשלים: מהריבוע מורידים שני <b>משולשי פינה</b> זהים, כל אחד עם ניצבים $1-c$.</p>
    <div class="lesson-ex"><b>דוגמה.</b> $P(\lvert X-Y\rvert<\frac12)$ בריבוע היחידה: שני משולשי הפינה הם עם ניצבים $\frac12$, שטח כל אחד $\frac12\cdot\frac12\cdot\frac12=\frac18$. השטח הנשאר $1-2\cdot\frac18=\frac34$, ולכן $P=\frac34$.</div>
    <div class="region-fig" data-region='{"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": -1, "c": "1/2", "op": "<"}, {"a": 1, "b": -1, "c": "-1/2", "op": ">"}], "labels": {"x": "X", "y": "Y"}, "caption": "|X-Y|<1/2"}'></div>
    <h3>שני אי-שוויונות ביחד</h3>
    <p>"וגם" הוא <b>חיתוך</b>: האזור הוא החלק שמקיים את שני הצדדים. מציירים את שני הקווים ובודקים באיזה אזור הצדדים נפגשים; לרוב יוצא משולש.</p>
    <p>"או" הוא <b>איחוד</b>, והכי קל לחשב אותו דרך המשלים: "לא ($A$ או $B$)" זה "לא $A$ וגם לא $B$".</p>
    <div class="lesson-trap">⚠️ $\lvert X-Y\rvert>c$ הוא "או": $X-Y>c$ או $X-Y<-c$. אלה <b>שני משולשי הפינה</b>, בדיוק מה שהסרנו מהרצועה. לא לבלבל בין "קטן" ו"גדול".</div>` },
  questions: [
    { id: "geo-C03-Q1",
      step: { type: "numeric", answer: 0.5556, tol: 0.003,
              prompt: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי $P\\left(\\lvert X-Y\\rvert<\\frac13\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "הרצועה היא הריבוע פחות שני משולשי פינה עם ניצבים $1-\\frac13=\\frac23$. שטח כל אחד $\\frac12\\cdot\\frac23\\cdot\\frac23=\\frac29$. השטח הנשאר $1-\\frac49=\\frac59$, ו-$|\\Omega|=1$, ולכן $P=\\frac59\\approx0.556$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: -1, c: "1/3", op: "<" }, { a: 1, b: -1, c: "-1/3", op: ">" }], labels: { x: "X", y: "Y" }, caption: "|X-Y|<1/3" },
      sim: { kind: "area", estimate: "P(|X-Y|<1/3)", exact: 5 / 9, params: { space: { x: [0, 1], y: [0, 1] }, event: "abs(x-y)<1/3" } },
      recap: "רצועה: $1-(1-c)^2$ בריבוע היחידה." },
    { id: "geo-C03-Q2",
      question: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי $P\\left(\\lvert X-Y\\rvert>\\frac14\\right)$ ?",
      options: [{ id: "a", value: "$\\frac{9}{16}$" }, { id: "b", value: "$\\frac{7}{16}$" }, { id: "c", value: "$\\frac{3}{4}$" }, { id: "d", value: "$\\frac{9}{32}$" }],
      correctId: "a",
      region: { space: { x: [0, 1], y: [0, 1] }, event: { any: [[{ a: 1, b: -1, c: "1/4", op: ">" }], [{ a: 1, b: -1, c: "-1/4", op: "<" }]] }, labels: { x: "X", y: "Y" }, caption: "|X-Y|>1/4" },
      sim: { kind: "area", estimate: "P(|X-Y|>1/4)", exact: 9 / 16, params: { space: { x: [0, 1], y: [0, 1] }, event: "abs(x-y)>1/4" } },
      explanation: "האירוע הוא שני משולשי פינה, כל אחד עם ניצבים $1-\\frac14=\\frac34$ ושטח $\\frac12\\cdot\\frac34\\cdot\\frac34=\\frac9{32}$. שניהם יחד $\\frac9{16}$. התשובה $\\frac9{32}$ היא משולש אחד בלבד, ו-$\\frac7{16}$ היא הרצועה $\\lvert X-Y\\rvert<\\frac14$ (המשלים).",
      recap: "$|X-Y|>c$: שני משולשי פינה, ביחד $(1-c)^2$." },
    { id: "geo-C03-Q3",
      step: { type: "numeric", answer: 0.0625, tol: 0.002,
              prompt: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי ההסתברות שמתקיימים גם $X<Y$ וגם $X+Y<\\frac12$ ? (אפשר שבר או עשרוני)",
              explain: "שני הקווים $y=x$ ו-$y=\\frac12-x$ נפגשים ב-$(\\frac14,\\frac14)$. האזור הוא המשולש עם הקודקודים $(0,0)$, $(0,\\frac12)$ ו-$(\\frac14,\\frac14)$: בסיס $\\frac12$ על ציר $y$, גובה $\\frac14$. שטחו $\\frac12\\cdot\\frac12\\cdot\\frac14=\\frac1{16}$, ו-$|\\Omega|=1$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: -1, b: 1, c: 0, op: ">" }, { a: 1, b: 1, c: "1/2", op: "<" }], labels: { x: "X", y: "Y" }, caption: "X<Y וגם X+Y<1/2" },
      sim: { kind: "area", estimate: "P(X<Y, X+Y<1/2)", exact: 1 / 16, params: { space: { x: [0, 1], y: [0, 1] }, event: "x<y and x+y<1/2" } },
      recap: "שני קווים: מוצאים את נקודת המפגש ומחשבים שטח משולש." },
    { id: "geo-C03-Q4",
      question: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי $P\\left(\\frac12<X+Y<\\frac32\\right)$ ?",
      options: [{ id: "a", value: "$\\frac34$" }, { id: "b", value: "$\\frac12$" }, { id: "c", value: "$\\frac78$" }, { id: "d", value: "$\\frac14$" }],
      correctId: "a",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 1, c: "1/2", op: ">" }, { a: 1, b: 1, c: "3/2", op: "<" }], labels: { x: "X", y: "Y" }, caption: "1/2<X+Y<3/2" },
      sim: { kind: "area", estimate: "P(1/2<X+Y<3/2)", exact: 0.75, params: { space: { x: [0, 1], y: [0, 1] }, event: "x+y>1/2 and x+y<3/2" } },
      explanation: "מורידים מהריבוע שני משולשי פינה: $X+Y\\le\\frac12$ (בפינה $(0,0)$, ניצבים $\\frac12$, שטח $\\frac18$) ו-$X+Y\\ge\\frac32$ (בפינה $(1,1)$, ניצבים $\\frac12$, שטח $\\frac18$). נשאר $1-\\frac14=\\frac34$. התשובה $\\frac78$ מתקבלת אם מורידים רק משולש אחד.",
      recap: "רצועה בין שני קווים מקבילים: מחסירים את שני משולשי הפינה." },
    { id: "geo-C03-Q5",
      step: { type: "numeric", answer: 0.4375, tol: 0.005,
              prompt: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. מהי $P\\left(\\lvert X-Y\\rvert<\\frac12\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "$|\\Omega|=1\\cdot2=2$. עבור כל $x$ הערכים המתאימים הם $y$ בין $x-\\frac12$ ל-$x+\\frac12$ בתוך $(0,2)$. אם $x<\\frac12$ האורך הוא $x+\\frac12$, ואם $x>\\frac12$ האורך הוא $1$. השטח $\\int_0^{1/2}\\left(x+\\frac12\\right)dx+\\frac12\\cdot1=\\frac38+\\frac12=\\frac78$. לכן $P=\\frac{7/8}{2}=\\frac7{16}$." },
      region: { space: { x: [0, 1], y: [0, 2] }, event: [{ a: 1, b: -1, c: "1/2", op: "<" }, { a: 1, b: -1, c: "-1/2", op: ">" }], labels: { x: "X", y: "Y" }, caption: "|X-Y|<1/2 במלבן (0,1)x(0,2)" },
      sim: { kind: "area", estimate: "P(|X-Y|<1/2)", exact: 7 / 16, params: { space: { x: [0, 1], y: [0, 2] }, event: "abs(x-y)<1/2" } },
      recap: "במלבן הרצועה נחתכת בגבולות: מחשבים שטח בנפרד לכל קטע של $x$ ומחלקים ב-$|\\Omega|$." },
  ],
});
