/* joint, level 4 - covariance and the correlation coefficient. */
COURSE_LEVEL("joint", {
  id: "C04", order: 4, icon: "📈", title: "שונות משותפת ומקדם מתאם",
  goal: "אחרי השלב הזה אפשר לחשב $\\mathrm{Cov}$, שונות ומקדם מתאם $\\rho$ מתוך טבלה משותפת, ושונות של סכום.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>השונות המשותפת מודדת אם שני משתנים נוטים לגדול יחד (חיובית), להפוך כיוון (שלילית), או שאין קשר ליניארי ביניהם (אפס).</p>
    <div class="lesson-rule">🔑 $$\mathrm{Cov}(X,Y)=E[XY]-E[X]\,E[Y],\qquad \rho(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}[X]\,\mathrm{Var}[Y]}}.$$ השונות של משתנה אחד היא $\mathrm{Var}[X]=E[X^2]-E[X]^2$ (זה בעצם $\mathrm{Cov}(X,X)$).</div>
    <div class="lesson-rule">🔑 תכונות: $-1\le\rho\le1$. אם $Y=aX+b$ אז $\rho=1$ כאשר $a>0$ ו-$\rho=-1$ כאשר $a<0$. ושונות של סכום: $$\mathrm{Var}[X+Y]=\mathrm{Var}[X]+\mathrm{Var}[Y]+2\,\mathrm{Cov}(X,Y).$$</div>
    <div class="lesson-ex"><b>דוגמה.</b> בטבלה $\begin{array}{c|cc}x\backslash y&0&1\\ \hline 0&0.1&0.3\\ 1&0.2&0.4\end{array}$ מקבלים $E[X]=0.6$, $E[Y]=0.7$, $E[XY]=0.4$, ולכן $\mathrm{Cov}=0.4-0.6\cdot0.7=-0.02$. שימו לב שזה מספר קטן וסימנו שלילי.</div>
    <h3>סדר העבודה</h3>
    <ul>
      <li>מחשבים $E[X]$, $E[Y]$ (מהשוליים) ו-$E[XY]$ (מהטבלה).</li>
      <li>$\mathrm{Cov}=E[XY]-E[X]E[Y]$.</li>
      <li>לצורך $\rho$: מחשבים גם $\mathrm{Var}[X]$ ו-$\mathrm{Var}[Y]$ ומחלקים בשורש מכפלתן.</li>
    </ul>
    <div class="lesson-trap">⚠️ שונות משותפת יכולה להיות שלילית, אבל שונות של משתנה אחד לא. אם יצא $\mathrm{Var}<0$ או $|\rho|>1$, יש טעות חישוב.</div>
    <p>בשלב הזה, ברוב השאלות: $X$ ו-$Y$ הם שני ביטים הוגנים בלתי תלויים, $D=XY$ ו-$T=X+Y$. הטבלה המשותפת של $(D,T)$:
    $$\begin{array}{c|ccc}d\backslash t&0&1&2\\ \hline 0&\frac14&\frac12&0\\ 1&0&0&\frac14\end{array}$$</p>` },
  questions: [
    { id: "joint-C04-Q1",
      step: { type: "numeric", answer: 0.25, tol: 0.001,
              prompt: String.raw`בטבלה של $(D,T)$ שבשיעור: $E[D]=\frac14$, $E[T]=1$. מהי השונות המשותפת $\mathrm{Cov}(D,T)$ ? (רמז: חשבו קודם $E[DT]$ מהטבלה. אפשר שבר או עשרוני)`,
              explain: String.raw`רק התא $(1,2)$ נותן $dt\ne0$: $E[DT]=1\cdot2\cdot\frac14=\frac12$. אז $\mathrm{Cov}=\frac12-\frac14\cdot1=\frac14$.` },
      sim: { kind: "custom_discrete", estimate: "Cov(D,T)", exact: 0.25,
             params: { vars: { X: { values: [0, 1], probs: [0.5, 0.5] }, Y: { values: [0, 1], probs: [0.5, 0.5] } }, measure: "cov", expr: ["X*Y", "X+Y"] } },
      recap: "$\\mathrm{Cov}=E[XY]-E[X]E[Y]$." },
    { id: "joint-C04-Q2",
      step: { type: "numeric", answer: 0.1875, tol: 0.001,
              prompt: String.raw`באותה טבלה של $(D,T)$ ($D=XY$, $T=X+Y$ לשני ביטים הוגנים): מהי $\mathrm{Var}[D]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$D$ מקבל $1$ בהסתברות $\frac14$ ו-$0$ אחרת, ולכן $E[D]=\frac14$ ו-$E[D^2]=\frac14$ (כי $D^2=D$). $\mathrm{Var}[D]=\frac14-\frac1{16}=\frac3{16}=0.1875$.` },
      sim: { kind: "custom_discrete", estimate: "Var[D]", exact: 0.1875,
             params: { vars: { X: { values: [0, 1], probs: [0.5, 0.5] }, Y: { values: [0, 1], probs: [0.5, 0.5] } }, measure: "var", expr: "X*Y" } },
      recap: "$\\mathrm{Var}=E[D^2]-E[D]^2$." },
    { id: "joint-C04-Q3",
      step: { type: "numeric", answer: 0.5, tol: 0.001,
              prompt: String.raw`באותה טבלה של $(D,T)$: מהי $\mathrm{Var}[T]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$T$ מקבל $0,1,2$ בהסתברויות $\frac14,\frac12,\frac14$. $E[T]=1$, $E[T^2]=\frac12+\frac44=\frac32$. $\mathrm{Var}[T]=\frac32-1=\frac12$.` },
      sim: { kind: "custom_discrete", estimate: "Var[T]", exact: 0.5,
             params: { vars: { X: { values: [0, 1], probs: [0.5, 0.5] }, Y: { values: [0, 1], probs: [0.5, 0.5] } }, measure: "var", expr: "X+Y" } },
      recap: "מחשבים $E[T^2]$ מהשוליים ומפחיתים $E[T]^2$." },
    { id: "joint-C04-Q4",
      step: { type: "numeric", answer: 0.8165, tol: 0.002,
              prompt: String.raw`באותה טבלה של $(D,T)$ ידוע ש-$\mathrm{Cov}(D,T)=\frac14$, $\mathrm{Var}[D]=\frac3{16}$ ו-$\mathrm{Var}[T]=\frac12$. מהו מקדם המתאם $\rho(D,T)$ ? (עשרוני, דיוק של שלוש ספרות)`,
              explain: String.raw`$\rho=\dfrac{1/4}{\sqrt{\frac3{16}\cdot\frac12}}=\dfrac{1/4}{\sqrt{3/32}}=\sqrt{\tfrac23}\approx0.8165$. הערך בין $-1$ ל-$1$, כנדרש. אם שוכחים את השורש מקבלים מספר שגוי שאינו אפילו קרוב.` },
      recap: "$\\rho$ הוא $\\mathrm{Cov}$ חלקי שורש מכפלת השונויות." },
    { id: "joint-C04-Q5",
      step: { type: "numeric", answer: 1.5, tol: 0.001,
              prompt: String.raw`מטילים מטבע הוגן שלוש פעמים. $X$ הוא מספר העצים בשתי הראשונות ו-$Y$ בשתי האחרונות. ידוע ש-$\mathrm{Var}[X]=\mathrm{Var}[Y]=\frac12$ ו-$\mathrm{Cov}(X,Y)=\frac14$. מהי $\mathrm{Var}[X+Y]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$\mathrm{Var}[X+Y]=\frac12+\frac12+2\cdot\frac14=\frac32$. אם מתעלמים מהשונות המשותפת מקבלים $1$, וזה נכון רק לבלתי תלויים.` },
      sim: { kind: "custom_discrete", estimate: "Var[X+Y]", exact: 1.5,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "var", expr: "X1 + 2*X2 + X3" } },
      recap: "$\\mathrm{Var}[X+Y]$ כולל את האיבר $2\\,\\mathrm{Cov}$." },
    { id: "joint-C04-Q6",
      question: String.raw`$X$ הוא משתנה מקרי עם שונות חיובית, ו-$Y=3-2X$. מהו $\rho(X,Y)$ ?`,
      options: [{ id: "a", value: "$-1$" }, { id: "b", value: "$-2$" }, { id: "c", value: "$1$" }, { id: "d", value: "$0$" }],
      correctId: "a",
      explanation: String.raw`$Y$ קשור ל-$X$ ביחס ליניארי $Y=aX+b$ עם $a=-2<0$, ולכן $\rho=-1$. התשובה $-2$ אינה אפשרית, כי $\rho$ תמיד בין $-1$ ל-$1$. התשובה $1$ נכונה רק כש-$a>0$. התשובה $0$ מתאימה לחוסר קשר ליניארי, וכאן הקשר ליניארי מלא.`,
      recap: "קשר ליניארי נותן $\\rho=\\pm1$ לפי סימן השיפוע." },
  ],
});
