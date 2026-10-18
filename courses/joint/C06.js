/* joint, level 6 - conditional pmf and conditional expectation from a table. */
COURSE_LEVEL("joint", {
  id: "C06", order: 6, icon: "🔍", title: "התפלגות מותנית ותוחלת מותנית מטבלה",
  goal: "אחרי השלב הזה אפשר לחשב מטבלה משותפת $P(X=x\\mid Y=y)$ ו-$E[X\\mid Y=y]$, ולהשתמש בהן לחישוב $E[X]$.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>"בהינתן $Y=y$" אומר שמסתכלים רק על <b>עמודה אחת</b> של הטבלה, העמודה של $y$. את הערכים בה צריך לנרמל, כדי שיסתכמו ל-$1$.</p>
    <div class="lesson-rule">🔑 $$P(X=x\mid Y=y)=\frac{P_{XY}(x,y)}{P_Y(y)},\qquad E[X\mid Y=y]=\sum_x x\,P(X=x\mid Y=y).$$ המכנה הוא סכום <b>העמודה</b> של $y$, כלומר $P_Y(y)$, לא $1$ ולא סכום השורה.</div>
    <div class="lesson-rule">🔑 תוחלת שלמה: $$E[X]=\sum_y P_Y(y)\,E[X\mid Y=y].$$ כלומר התוחלת הכללית היא ממוצע משוקלל של התוחלות המותנות.</div>
    <div class="lesson-ex"><b>דוגמה.</b> בטבלה $\begin{array}{c|cc}x\backslash y&0&1\\ \hline 0&0.1&0.3\\ 1&0.2&0.4\end{array}$ העמודה $y=1$ היא $0.3,\,0.4$ וסכומה $P_Y(1)=0.7$. לכן $P(X=0\mid Y=1)=\frac{0.3}{0.7}=\frac37$, $P(X=1\mid Y=1)=\frac47$, ו-$E[X\mid Y=1]=0\cdot\frac37+1\cdot\frac47=\frac47$.</div>
    <div class="lesson-trap">⚠️ לא מחלקים בסכום הלא נכון: $P(Y=y\mid X=x)$ מחלקים בסכום <b>השורה</b> של $x$, ו-$P(X=x\mid Y=y)$ בסכום <b>העמודה</b> של $y$. שתי ההסתברויות האלה בדרך כלל שונות.</div>
    <p>שלוש הטלות של מטבע הוגן, $X$ בשתי הראשונות ו-$Y$ בשתי האחרונות:
    $$\begin{array}{c|ccc}x\backslash y&0&1&2\\ \hline 0&\frac18&\frac18&0\\ 1&\frac18&\frac14&\frac18\\ 2&0&\frac18&\frac18\end{array}$$
    עמודה $y=0$: $\frac18,\frac18,0$ (סכום $\frac14$). עמודה $y=1$: $\frac18,\frac14,\frac18$ (סכום $\frac12$). עמודה $y=2$: $0,\frac18,\frac18$ (סכום $\frac14$).</p>` },
  questions: [
    { id: "joint-C06-Q1",
      step: { type: "numeric", answer: 0.5, tol: 0.001,
              prompt: String.raw`בטבלה של שלוש ההטלות (בשיעור): מהו $P(X=0\mid Y=0)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`עמודה $y=0$: התא $(0,0)$ הוא $\frac18$, וסכום העמודה $P_Y(0)=\frac14$. לכן $\frac{1/8}{1/4}=\frac12$.` },
      sim: { kind: "custom_discrete", estimate: "P(X=0 | Y=0)", exact: 0.5,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       event: "X1 + X2 == 0", given: "X2 + X3 == 0" } },
      recap: "מחלקים את התא בסכום העמודה." },
    { id: "joint-C06-Q2",
      step: { type: "numeric", answer: 0.5, tol: 0.001,
              prompt: String.raw`באותה טבלה (שלוש הטלות הוגנות): מהי $E[X\mid Y=0]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`ההתפלגות המותנית בעמודה $y=0$: $P(X=0\mid Y=0)=\frac12$, $P(X=1\mid Y=0)=\frac12$, $P(X=2\mid Y=0)=0$. התוחלת $0\cdot\frac12+1\cdot\frac12+2\cdot0=\frac12$.` },
      sim: { kind: "custom_discrete", estimate: "E[X | Y=0]", exact: 0.5,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "mean", expr: "X1 + X2", given: "X2 + X3 == 0" } },
      recap: "$E[X\\mid Y=y]$: תוחלת לפי ההתפלגות המותנית." },
    { id: "joint-C06-Q3",
      step: { type: "numeric", answer: 1.5, tol: 0.001,
              prompt: String.raw`באותה טבלה (שלוש הטלות הוגנות): מהי $E[X\mid Y=2]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`עמודה $y=2$: $0,\frac18,\frac18$ וסכומה $\frac14$. ההסתברויות המותנות: $0,\frac12,\frac12$. התוחלת $1\cdot\frac12+2\cdot\frac12=\frac32$.` },
      sim: { kind: "custom_discrete", estimate: "E[X | Y=2]", exact: 1.5,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       measure: "mean", expr: "X1 + X2", given: "X2 + X3 == 2" } },
      recap: "מנרמלים את העמודה לפני שמחשבים תוחלת." },
    { id: "joint-C06-Q4",
      question: String.raw`באותה טבלה (שלוש הטלות הוגנות, $X$ בשתי הראשונות ו-$Y$ בשתי האחרונות): מהו $P(Y=0\mid X=1)$ ?`,
      options: [{ id: "a", value: String.raw`$\frac14$` }, { id: "b", value: String.raw`$\frac12$` }, { id: "c", value: String.raw`$\frac18$` }, { id: "d", value: String.raw`$\frac13$` }],
      correctId: "a",
      explanation: String.raw`ההתניה היא ב-$X=1$, ולכן מסתכלים על **השורה** $x=1$: $\frac18,\frac14,\frac18$ וסכומה $P_X(1)=\frac12$. התא $(1,0)$ הוא $\frac18$, לכן $\frac{1/8}{1/2}=\frac14$. הערך $\frac12$ הוא $P(X=1\mid Y=0)$, שמחלקים בסכום העמודה, וזו הטעות הנפוצה. הערך $\frac18$ הוא התא עצמו בלי חלוקה.`,
      sim: { kind: "custom_discrete", estimate: "P(Y=0 | X=1)", exact: 0.25,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       event: "X2 + X3 == 0", given: "X1 + X2 == 1" } },
      recap: "בהינתן $X=x$ מחלקים בסכום השורה של $x$." },
    { id: "joint-C06-Q5",
      step: { type: "numeric", answer: 0.666667, tol: 0.002,
              prompt: String.raw`$X$ ו-$Y$ הם שני ביטים הוגנים בלתי תלויים, $D=XY$ ו-$T=X+Y$, והטבלה של $(D,T)$:
$$\begin{array}{c|ccc}d\backslash t&0&1&2\\ \hline 0&\frac14&\frac12&0\\ 1&0&0&\frac14\end{array}$$
מהו $P(T=1\mid D=0)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`ההתניה ב-$D=0$ היא על השורה $d=0$: $\frac14,\frac12,0$ וסכומה $\frac34$. לכן $P(T=1\mid D=0)=\frac{1/2}{3/4}=\frac23$.` },
      sim: { kind: "custom_discrete", estimate: "P(T=1 | D=0)", exact: 2 / 3,
             params: { vars: { X: { values: [0, 1], probs: [0.5, 0.5] }, Y: { values: [0, 1], probs: [0.5, 0.5] } }, event: "X+Y == 1", given: "X*Y == 0" } },
      recap: "מחלקים את התא בסכום השורה של התנאי." },
    { id: "joint-C06-Q6",
      step: { type: "numeric", answer: 1, tol: 0.001,
              prompt: String.raw`בטבלה של שלוש ההטלות ידוע ש-$P_Y=(\frac14,\frac12,\frac14)$, ושהתוחלות המותנות הן $E[X\mid Y=0]=\frac12$, $E[X\mid Y=1]=1$, $E[X\mid Y=2]=\frac32$. בעזרת נוסחת התוחלת השלמה, מהי $E[X]$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$E[X]=\sum_yP_Y(y)E[X\mid Y=y]=\frac14\cdot\frac12+\frac12\cdot1+\frac14\cdot\frac32=\frac18+\frac12+\frac38=1$. זה אותו ערך כמו $E[X]=1$ שחישבנו מהשוליים.` },
      recap: "$E[X]=\\sum_yP_Y(y)E[X\\mid Y=y]$." },
  ],
});
