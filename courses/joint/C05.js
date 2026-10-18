/* joint, level 5 - independent vs uncorrelated, with the classic counterexample. */
COURSE_LEVEL("joint", {
  id: "C05", order: 5, icon: "⚖️", title: "בלתי תלויים לעומת בלתי מתואמים",
  goal: "אחרי השלב הזה אפשר להכריע מטבלה אם שני משתנים בלתי תלויים ואם הם בלתי מתואמים, ולהסביר למה אלה שני דברים שונים.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>יש שתי הגדרות שנוטים לבלבל ביניהן.</p>
    <div class="lesson-rule">🔑 <b>בלתי תלויים:</b> $P_{XY}(x,y)=P_X(x)\,P_Y(y)$ <b>בכל</b> תא של הטבלה.<br><b>בלתי מתואמים:</b> $\mathrm{Cov}(X,Y)=0$, כלומר $E[XY]=E[X]\,E[Y]$.</div>
    <div class="lesson-rule">🔑 אי-תלות <b>גוררת</b> אי-מתאם, אבל לא להפך: משתנים יכולים להיות בלתי מתואמים ועדיין תלויים.</div>
    <h3>איך בודקים אי-תלות</h3>
    <ul>
      <li>כדי להוכיח <b>תלות</b> מספיק תא אחד שבו $P_{XY}\ne P_XP_Y$. הכי מהיר: למצוא <b>אפס</b> בטבלה בתא ששני השוליים שלו חיוביים.</li>
      <li>כדי להוכיח <b>אי-תלות</b> חייבים לבדוק את כל התאים.</li>
    </ul>
    <div class="lesson-ex"><b>הדוגמה הקלאסית.</b> $X$ אחיד על $\{-1,0,1\}$ ו-$Y=X^2$. הזוגות האפשריים: $(-1,1)$, $(0,0)$, $(1,1)$, כל אחד בהסתברות $\frac13$.
    <table><thead><tr><th>$x\backslash y$</th><th>$0$</th><th>$1$</th><th>$P_X$</th></tr></thead>
    <tbody><tr><td>$-1$</td><td>$0$</td><td>$\frac13$</td><td>$\frac13$</td></tr>
    <tr><td>$0$</td><td>$\frac13$</td><td>$0$</td><td>$\frac13$</td></tr>
    <tr><td>$1$</td><td>$0$</td><td>$\frac13$</td><td>$\frac13$</td></tr>
    <tr><td>$P_Y$</td><td>$\frac13$</td><td>$\frac23$</td><td>$1$</td></tr></tbody></table>
    $E[X]=0$ ו-$E[XY]=E[X^3]=\frac13(-1)+0+\frac13(1)=0$, ולכן $\mathrm{Cov}=0-0\cdot E[Y]=0$: <b>בלתי מתואמים</b>. אבל $P(X=0,Y=1)=0$ בעוד $P_X(0)P_Y(1)=\frac13\cdot\frac23\ne0$: <b>תלויים</b>. הערך של $Y$ נקבע לגמרי מ-$X$, אבל הקשר אינו ליניארי ולכן $\mathrm{Cov}$ לא רואה אותו.</div>
    <div class="lesson-trap">⚠️ "$\mathrm{Cov}=0$ אז בלתי תלויים" היא טעות. הכיוון הנכון הוא רק: בלתי תלויים, אז $\mathrm{Cov}=0$.</div>` },
  questions: [
    { id: "joint-C05-Q1",
      question: String.raw`נתונה טבלה משותפת:
$$\begin{array}{c|cc}x\backslash y&0&1\\ \hline 0&0.06&0.14\\ 1&0.24&0.56\end{array}$$
האם $X$ ו-$Y$ בלתי תלויים?`,
      options: [
        { id: "a", value: "כן, כל תא שווה למכפלת השוליים שלו" },
        { id: "b", value: "לא, התאים אינם שווים זה לזה" },
        { id: "c", value: "לא, כי הסכום 1" },
        { id: "d", value: "אי אפשר לדעת בלי לחשב שונות משותפת" }],
      correctId: "a",
      explanation: String.raw`השוליים: $P_X=(0.2,0.8)$ ו-$P_Y=(0.3,0.7)$. המכפלות: $0.2\cdot0.3=0.06$, $0.2\cdot0.7=0.14$, $0.8\cdot0.3=0.24$, $0.8\cdot0.7=0.56$. כל התאים שווים למכפלה, ולכן יש אי-תלות. תאים שונים זה מזה אינם סימן לתלות, והסכום $1$ הוא תנאי לכל טבלה תקינה. $\mathrm{Cov}=0$ לבדו לא מספיק כדי להוכיח אי-תלות.`,
      recap: "אי-תלות: כל תא שווה למכפלת השוליים." },
    { id: "joint-C05-Q2",
      question: String.raw`מטילים מטבע הוגן שלוש פעמים. $X$ הוא מספר העצים בשתי הראשונות ו-$Y$ בשתי האחרונות, והטבלה:
$$\begin{array}{c|ccc}x\backslash y&0&1&2\\ \hline 0&\frac18&\frac18&0\\ 1&\frac18&\frac14&\frac18\\ 2&0&\frac18&\frac18\end{array}$$
האם $X$ ו-$Y$ בלתי תלויים?`,
      options: [
        { id: "a", value: String.raw`לא, כי $P(X=0,Y=2)=0$ בעוד $P_X(0)P_Y(2)=\frac1{16}$` },
        { id: "b", value: "כן, כי ההטלות בלתי תלויות" },
        { id: "c", value: String.raw`כן, כי $P_X=P_Y$` },
        { id: "d", value: "לא, כי יש בטבלה שני תאים השווים $\\frac14$" }],
      correctId: "a",
      explanation: String.raw`בתא $(0,2)$ ההסתברות $0$, אבל $P_X(0)=\frac14$ ו-$P_Y(2)=\frac14$, ומכפלתם $\frac1{16}\ne0$. תא אחד כזה מספיק להוכחת תלות. ההטלות בלתי תלויות, אבל $X$ ו-$Y$ חולקים את ההטלה האמצעית ולכן הם תלויים. שוויון בין השוליים לא קשור לאי-תלות.`,
      recap: "אפס בתא ששוליו חיוביים מוכיח תלות." },
    { id: "joint-C05-Q3",
      step: { type: "numeric", answer: 0, tol: 0.0005,
              prompt: String.raw`$X$ אחיד על $\{-1,0,1\}$ ו-$Y=X^2$. מהי השונות המשותפת $\mathrm{Cov}(X,Y)$ ?`,
              explain: String.raw`$E[X]=0$, ולכן $\mathrm{Cov}=E[XY]-0=E[X^3]$. $X^3=X$ לערכים $-1,0,1$, ולכן $E[X^3]=E[X]=0$. הכל שווה $0$.` },
      sim: { kind: "custom_discrete", estimate: "Cov(X,Y)", exact: 0,
             params: { joint: [{ p: 1 / 3, X: -1, Y: 1 }, { p: 1 / 3, X: 0, Y: 0 }, { p: 1 / 3, X: 1, Y: 1 }], measure: "cov", expr: ["X", "Y"] } },
      recap: "ב-$Y=X^2$ עם $X$ סימטרי, $\\mathrm{Cov}=0$." },
    { id: "joint-C05-Q4",
      question: String.raw`באותו זוג ($X$ אחיד על $\{-1,0,1\}$ ו-$Y=X^2$, שבו $\mathrm{Cov}=0$): האם $X$ ו-$Y$ בלתי תלויים?`,
      options: [
        { id: "a", value: "לא, הם תלויים אף שהם בלתי מתואמים" },
        { id: "b", value: "כן, כי Cov = 0" },
        { id: "c", value: "כן, כי Y ו-X מקבלים ערכים שונים" },
        { id: "d", value: "לא, כי הם מתואמים" }],
      correctId: "a",
      explanation: String.raw`$P(X=0,Y=1)=0$ אבל $P_X(0)P_Y(1)=\frac13\cdot\frac23=\frac29$. התא לא שווה למכפלה, ולכן יש תלות. $\mathrm{Cov}=0$ מראה אי-מתאם בלבד. התשובה "הם מתואמים" שגויה, כי $\mathrm{Cov}=0$.`,
      recap: "בלתי מתואמים, אבל תלויים: הדוגמה הקלאסית." },
    { id: "joint-C05-Q5",
      question: String.raw`ידוע ש-$\mathrm{Cov}(X,Y)=0$. מה בהכרח נכון?`,
      options: [
        { id: "a", value: String.raw`$E[XY]=E[X]E[Y]$, אבל אין הכרח שהם בלתי תלויים` },
        { id: "b", value: "X ו-Y בלתי תלויים" },
        { id: "c", value: String.raw`$X$ ו-$Y$ זרים` },
        { id: "d", value: String.raw`$X=0$ או $Y=0$` }],
      correctId: "a",
      explanation: String.raw`$\mathrm{Cov}=0$ שקול ל-$E[XY]=E[X]E[Y]$, וזה כל מה שנובע. אי-תלות דורשת שוויון בכל התאים, ו"זרים" הוא מושג על מאורעות ולא קשור כאן. $X$ ו-$Y$ יכולים להיות שניהם שונים מאפס עם $\mathrm{Cov}=0$.`,
      recap: "$\\mathrm{Cov}=0$ אומר אי-מתאם בלבד." },
    { id: "joint-C05-Q6",
      question: String.raw`$X$ הוא ביט הוגן ו-$Y=1-X$. האם $X$ ו-$Y$ בלתי מתואמים?`,
      options: [
        { id: "a", value: String.raw`לא, $\mathrm{Cov}(X,Y)=-\frac14\ne0$` },
        { id: "b", value: "כן, כי הם מקבלים ערכים שונים" },
        { id: "c", value: "כן, כי הם בלתי תלויים" },
        { id: "d", value: String.raw`לא, כי $\mathrm{Cov}(X,Y)=\frac14$` }],
      correctId: "a",
      explanation: String.raw`$E[X]=E[Y]=\frac12$ ו-$XY=X(1-X)=0$ תמיד, ולכן $E[XY]=0$ ו-$\mathrm{Cov}=0-\frac14=-\frac14\ne0$. הם מתואמים (אפילו $\rho=-1$), וגם תלויים: אם $X=1$ אז $Y=0$ בוודאות. הסימן של $\mathrm{Cov}$ שלילי, לא חיובי.`,
      sim: { kind: "custom_discrete", estimate: "Cov(X,Y)", exact: -0.25,
             params: { joint: [{ p: 0.5, X: 0, Y: 1 }, { p: 0.5, X: 1, Y: 0 }], measure: "cov", expr: ["X", "Y"] } },
      recap: "קשר ליניארי חד-משמעי נותן מתאם, לא אי-מתאם." },
  ],
});
