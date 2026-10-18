/* geo, level 1 - the sample space: a square or a rectangle, and |Omega|. */
COURSE_LEVEL("geo", {
  id: "C01", order: 1, icon: "🟦", title: "מרחב המדגם: ריבוע ומלבן",
  goal: "אחרי השלב הזה אפשר לזהות את מרחב המדגם של שני משתנים אחידים, לחשב את שטחו, ולמצוא הסתברות של אירוע מלבני.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>נניח ש-$X$ ו-$Y$ הם משתנים מקריים <b>בלתי תלויים</b> ו<b>אחידים</b>. אז הזוג $(X,Y)$ הוא נקודה אקראית שנבחרת <b>אחיד על מלבן</b>: כל אזור בעל אותו שטח הוא באותה מידה סביר.</p>
    <div class="lesson-rule">🔑 $X\sim U_c(0,a)$ ו-$Y\sim U_c(0,b)$ בלתי תלויים: מרחב המדגם הוא המלבן $\Omega=(0,a)\times(0,b)$, ושטחו $|\Omega|=a\cdot b$.</div>
    <div class="lesson-rule">🔑 לכל אירוע $A$ (אזור בתוך המלבן): $$P(A)=\frac{S(A)}{|\Omega|},$$ כאשר $S(A)$ הוא שטח האזור.</div>
    <p>כשהמשתנים אחידים על $(0,1)$ המלבן הוא <b>ריבוע היחידה</b>, שטחו $1$, וההסתברות היא פשוט השטח. אבל אם אחד המשתנים אחיד על $(0,2)$ אז $|\Omega|=2$, ואת השטח של האירוע חייבים לחלק ב-$2$.</p>
    <div class="lesson-ex"><b>דוגמה.</b> $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,1)$. מהי $P(X<\frac14)$? האירוע הוא רצועה אנכית בין $x=0$ ל-$x=\frac14$, ברוחב $\frac14$ ובגובה $1$. שטחה $\frac14$, ו-$|\Omega|=1$, ולכן ההסתברות $\frac14$.</div>
    <div class="region-fig" data-region='{"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": 0, "c": "1/4", "op": "<"}], "labels": {"x": "X", "y": "Y"}, "caption": "X<1/4"}'></div>
    <div class="lesson-ex"><b>דוגמה במלבן.</b> $X\sim U_c(0,2)$ ו-$Y\sim U_c(0,3)$. אז $|\Omega|=2\cdot3=6$. לאירוע $X<1$ יש שטח $1\cdot3=3$ (רוחב $1$, גובה $3$), ולכן $P(X<1)=\frac36=\frac12$. זה כמובן אותו ערך כמו $P(X<1)=\frac12$ של משתנה אחד: ה-$Y$ לא משנה כלום.</div>
    <div class="lesson-trap">⚠️ הטעות הנפוצה ביותר: לחלק ב-$1$ במקום ב-$|\Omega|$. תמיד רושמים קודם את $|\Omega|$.</div>
    <h3>סדר העבודה</h3>
    <ul>
      <li>רושמים את ההתפלגויות של $X$ ו-$Y$ ומחשבים $|\Omega|$.</li>
      <li>מציירים את האירוע בתוך המלבן ומחשבים את שטחו.</li>
      <li>מחלקים: $P=\dfrac{S(A)}{|\Omega|}$.</li>
    </ul>` },
  questions: [
    { id: "geo-C01-Q1",
      step: { type: "numeric", answer: 2, tol: 0,
              prompt: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים, והנקודה $(X,Y)$ נבחרת אחיד במלבן $\\Omega$. מהו $|\\Omega|$, שטח מרחב המדגם?",
              explain: "המלבן הוא $(0,1)\\times(0,2)$, ושטחו $1\\cdot2=2$. התשובה $1$ היא שטח ריבוע היחידה, וזה לא מרחב המדגם כאן." },
      recap: "$|\\Omega|$ הוא שטח המלבן $a\\cdot b$, לא תמיד $1$." },
    { id: "geo-C01-Q2",
      step: { type: "numeric", answer: 6, tol: 0,
              prompt: "$X\\sim U_c(0,3)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. מהו $|\\Omega|$?",
              explain: "$\\Omega=(0,3)\\times(0,2)$ ושטחו $3\\cdot2=6$." },
      recap: "$|\\Omega|=a\\cdot b$." },
    { id: "geo-C01-Q3",
      question: "$X\\sim U_c(0,3)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. מהי $P(X<1)$ ?",
      options: [{ id: "a", value: "$\\frac13$" }, { id: "b", value: "$\\frac12$" }, { id: "c", value: "$\\frac23$" }, { id: "d", value: "$2$" }],
      correctId: "a",
      region: { space: { x: [0, 3], y: [0, 2] }, event: [{ a: 1, b: 0, c: 1, op: "<" }], labels: { x: "X", y: "Y" }, caption: "X<1 במלבן (0,3)x(0,2)" },
      sim: { kind: "area", estimate: "P(X<1)", exact: 1 / 3, params: { space: { x: [0, 3], y: [0, 2] }, event: "x<1" } },
      explanation: "$|\\Omega|=3\\cdot2=6$. האירוע $X<1$ הוא רצועה ברוחב $1$ ובגובה $2$, שטחה $2$. ההסתברות $\\frac26=\\frac13$. התשובה $\\frac12$ מתקבלת אם מחלקים ב-$4$ במקום ב-$6$, ו-$\\frac23$ היא ההסתברות של המשלים.",
      recap: "שטח האירוע חלקי $|\\Omega|$." },
    { id: "geo-C01-Q4",
      step: { type: "numeric", answer: 0.125, tol: 0.005,
              prompt: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי ההסתברות $P\\left(X<\\frac14,\\ Y>\\frac12\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "האירוע הוא מלבן ברוחב $\\frac14$ ובגובה $\\frac12$ (מ-$y=\\frac12$ עד $y=1$). שטחו $\\frac14\\cdot\\frac12=\\frac18$, ו-$|\\Omega|=1$, ולכן ההסתברות $\\frac18=0.125$. זה גם $\\frac14\\cdot\\frac12$, כי המשתנים בלתי תלויים." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 0, c: "1/4", op: "<" }, { a: 0, b: 1, c: "1/2", op: ">" }], labels: { x: "X", y: "Y" }, caption: "X<1/4 וגם Y>1/2" },
      sim: { kind: "area", estimate: "P(X<1/4, Y>1/2)", exact: 0.125, params: { space: { x: [0, 1], y: [0, 1] }, event: "x<1/4 and y>1/2" } },
      recap: "אירוע מלבני: רוחב כפול גובה, חלקי $|\\Omega|$." },
    { id: "geo-C01-Q5",
      question: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. מהי $P(Y<\\frac12)$ ?",
      options: [{ id: "a", value: "$\\frac12$" }, { id: "b", value: "$\\frac14$" }, { id: "c", value: "$\\frac34$" }, { id: "d", value: "$1$" }],
      correctId: "b",
      region: { space: { x: [0, 1], y: [0, 2] }, event: [{ a: 0, b: 1, c: "1/2", op: "<" }], labels: { x: "X", y: "Y" }, caption: "Y<1/2 במלבן (0,1)x(0,2)" },
      sim: { kind: "area", estimate: "P(Y<1/2)", exact: 0.25, params: { space: { x: [0, 1], y: [0, 2] }, event: "y<1/2" } },
      explanation: "$|\\Omega|=1\\cdot2=2$. האירוע $Y<\\frac12$ הוא רצועה ברוחב $1$ ובגובה $\\frac12$, שטחה $\\frac12$. לכן $P=\\frac{1/2}{2}=\\frac14$. התשובה $\\frac12$ היא שטח האירוע בלי החלוקה ב-$|\\Omega|$ (זו הטעות הנפוצה). התשובה $\\frac12$ אינה נכונה גם כי $Y$ מקבל ערכים עד $2$ ורק רבע מהם קטנים מ-$\\frac12$.",
      recap: "מחלקים ב-$|\\Omega|=2$, לא ב-$1$." },
  ],
});
