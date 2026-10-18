/* joint, level 3 - expectation of a function of (X,Y). */
COURSE_LEVEL("joint", {
  id: "C03", order: 3, icon: "🎯", title: "תוחלת של פונקציה של (X,Y)",
  goal: "אחרי השלב הזה אפשר לחשב $E[g(X,Y)]$ ישירות מהטבלה המשותפת, ובפרט $E[X]$, $E[X+Y]$ ו-$E[XY]$.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>כדי לחשב תוחלת של ביטוי שתלוי בשני המשתנים אין צורך להבין מה ההתפלגות שלו: לוקחים כל תא בטבלה, מחשבים את ערך הביטוי בו, וכופלים בהסתברות התא.</p>
    <div class="lesson-rule">🔑 $$E[g(X,Y)]=\sum_x\sum_y g(x,y)\,P_{XY}(x,y).$$ מקרים חשובים: $E[X]=\sum x\,P_{XY}(x,y)$ (או מהשוליים), $E[X+Y]=E[X]+E[Y]$, ו-$$E[XY]=\sum_x\sum_y xy\,P_{XY}(x,y).$$</div>
    <div class="lesson-ex"><b>דוגמה.</b> בטבלה $\begin{array}{c|cc}x\backslash y&0&1\\ \hline 0&0.1&0.3\\ 1&0.2&0.4\end{array}$ רק התא $(1,1)$ נותן $xy\ne0$, ולכן $E[XY]=1\cdot1\cdot0.4=0.4$. עבור $g=|x-y|$ התאים $(0,1)$ ו-$(1,0)$ נותנים $1$, ולכן $E|X-Y|=0.3+0.2=0.5$.</div>
    <div class="lesson-trap">⚠️ אין מצב ש-$E[XY]=E[X]E[Y]$ "תמיד". השוויון הזה נכון בבלתי תלויים ולא נכון בכלל. לכן מחשבים את $E[XY]$ מהטבלה, תא אחר תא. את הקשר ביניהם נחקור בשלבים הבאים.</div>
    <p>בשלב הזה כל החישובים על אותה טבלה: מטבע הוגן מוטל שלוש פעמים, $X$ הוא מספר העצים בשתי ההטלות הראשונות ו-$Y$ בשתי האחרונות.
    $$\begin{array}{c|ccc}x\backslash y&0&1&2\\ \hline 0&\frac18&\frac18&0\\ 1&\frac18&\frac14&\frac18\\ 2&0&\frac18&\frac18\end{array}$$</p>` },
  questions: [
    { id: "joint-C03-Q1",
      step: { type: "numeric", answer: 1, tol: 0.001,
              prompt: String.raw`בטבלה של שלוש הטלות הוגנות (מופיעה בשיעור), מהו $E[X]$ ?`,
              explain: String.raw`שוליים: $P_X=(\frac14,\frac12,\frac14)$ ולכן $E[X]=0\cdot\frac14+1\cdot\frac12+2\cdot\frac14=1$. אפשר גם לסכום $x\cdot P_{XY}$ על כל התאים, ומקבלים אותו ערך.` },
      sim: { kind: "custom_discrete", estimate: "E[X]", exact: 1,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "mean", expr: "X1 + X2" } },
      recap: "$E[X]=\\sum x\\,P_X(x)$." },
    { id: "joint-C03-Q2",
      step: { type: "numeric", answer: 1.25, tol: 0.001,
              prompt: String.raw`באותה טבלה (שלוש הטלות הוגנות, $X$ בשתי הראשונות ו-$Y$ בשתי האחרונות):
$$\begin{array}{c|ccc}x\backslash y&0&1&2\\ \hline 0&\frac18&\frac18&0\\ 1&\frac18&\frac14&\frac18\\ 2&0&\frac18&\frac18\end{array}$$
מהו $E[XY]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`התאים עם $xy\ne0$: $(1,1)$ נותן $1\cdot\frac14$. $(1,2)$ נותן $2\cdot\frac18$. $(2,1)$ נותן $2\cdot\frac18$. $(2,2)$ נותן $4\cdot\frac18$. הסכום $\frac14+\frac14+\frac14+\frac12=\frac54$.` },
      sim: { kind: "custom_discrete", estimate: "E[XY]", exact: 1.25,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "mean", expr: "(X1 + X2) * (X2 + X3)" } },
      recap: "$E[XY]$ הוא סכום של $xy\\cdot P_{XY}$ על כל התאים." },
    { id: "joint-C03-Q3",
      step: { type: "numeric", answer: 2, tol: 0.001,
              prompt: String.raw`באותו ניסוי (שלוש הטלות הוגנות, $X$ בשתי הראשונות ו-$Y$ בשתי האחרונות), מהו $E[X+Y]$ ? (רמז: $E[X]=E[Y]=1$)`,
              explain: String.raw`תוחלת היא ליניארית תמיד: $E[X+Y]=E[X]+E[Y]=1+1=2$, בלי קשר לתלות. אפשר גם לוודא מהטבלה: $\sum(x+y)P_{XY}=2$.` },
      sim: { kind: "custom_discrete", estimate: "E[X+Y]", exact: 2,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "mean", expr: "X1 + 2*X2 + X3" } },
      recap: "$E[X+Y]=E[X]+E[Y]$, גם כשהמשתנים תלויים." },
    { id: "joint-C03-Q4",
      step: { type: "numeric", answer: 0.5, tol: 0.001,
              prompt: String.raw`באותה טבלה (שלוש הטלות הוגנות, $X$ בשתי הראשונות ו-$Y$ בשתי האחרונות), מהו $E\left[\,|X-Y|\,\right]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$|x-y|$ שווה $1$ בארבעה תאים: $(0,1),(1,0),(1,2),(2,1)$, וכל אחד מהם $\frac18$. בשאר התאים הוא $0$ ($|x-y|=2$ מופיע רק בתאים $(0,2)$ ו-$(2,0)$ שהסתברותם $0$). לכן $E=4\cdot\frac18=\frac12$.` },
      sim: { kind: "custom_discrete", estimate: "E|X-Y|", exact: 0.5,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "mean", expr: "abs(X1 - X3)" } },
      recap: "מציבים את הפונקציה בכל תא וכופלים בהסתברות התא." },
    { id: "joint-C03-Q5",
      step: { type: "numeric", answer: 1.25, tol: 0.001,
              prompt: String.raw`באותה טבלה (שלוש הטלות הוגנות, $X$ בשתי הראשונות ו-$Y$ בשתי האחרונות), מהו $E\left[\max(X,Y)\right]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`המקסימום בכל תא: $(0,1)\to1$, $(1,0)\to1$, $(1,1)\to1$, $(1,2)\to2$, $(2,1)\to2$, $(2,2)\to2$, ו-$(0,0)\to0$. הסכום $1\cdot\frac18+1\cdot\frac18+1\cdot\frac14+2\cdot\frac18+2\cdot\frac18+2\cdot\frac18=\frac54$.` },
      sim: { kind: "custom_discrete", estimate: "E[max(X,Y)]", exact: 1.25,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "mean", expr: "max(X1 + X2, X2 + X3)" } },
      recap: "תוחלת של פונקציה: סכום על כל התאים של ערך הפונקציה כפול ההסתברות." },
  ],
});
