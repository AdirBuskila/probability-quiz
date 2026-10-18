/* joint, level 8 - the Bernoulli-matrix family: det and trace as functions of two Bernoulli variables. */
COURSE_LEVEL("joint", {
  id: "C08", order: 8, icon: "🔢", title: "מטריצות ברנולי: דטרמיננטה ועקבה",
  goal: "אחרי השלב הזה אפשר, בהינתן מטריצה שאיבריה מבוססים על שני ביטים, למצוא את ההתפלגות המשותפת של $(D,T)$, לזהות מתי $D$ ברנולי, ולהכריע על תלות ומתאם.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>בשאלות הללו נותנים מטריצה $2\times2$ שאיבריה בנויים מ-$X\sim\mathrm{Ber}(p)$ ו-$Y\sim\mathrm{Ber}(q)$ בלתי תלויים, ומגדירים $D=\det$ ו-$T=\mathrm{tr}$. הדרך אחת תמיד.</p>
    <div class="lesson-rule">🔑 לדטרמיננטה ולעקבה: $\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc$ ו-$\mathrm{tr}=a+d$. ובביט $X\in\{0,1\}$ מתקיים $X^2=X$ (וכך גם $Y^2=Y$), מה שמפשט את הביטויים.</div>
    <h3>מתכון</h3>
    <ul>
      <li>מחשבים את $D$ ואת $T$ כביטויים ב-$X,Y$ ומפשטים בעזרת $X^2=X$.</li>
      <li>טבלה של ארבעת המצבים $(X,Y)$: הסתברותם $(1-p)(1-q)$, $(1-p)q$, $p(1-q)$, $pq$, ולכל מצב ערכי $D$ ו-$T$.</li>
      <li><b>מקבצים</b> מצבים שנותנים את אותו זוג $(D,T)$ ומחברים הסתברויות.</li>
      <li>משם: שוליים, תוחלות, $\mathrm{Cov}$, ושאלת התלות.</li>
    </ul>
    <div class="lesson-ex"><b>דוגמה.</b> $\boldsymbol A=\begin{pmatrix}X&1\\1&Y\end{pmatrix}$. אז $D=XY-1$ ו-$T=X+Y$.
    <table><thead><tr><th>$(X,Y)$</th><th>$(0,0)$</th><th>$(0,1)$</th><th>$(1,0)$</th><th>$(1,1)$</th></tr></thead>
    <tbody><tr><td>הסתברות</td><td>$(1-p)(1-q)$</td><td>$(1-p)q$</td><td>$p(1-q)$</td><td>$pq$</td></tr>
    <tr><td>$D$</td><td>$-1$</td><td>$-1$</td><td>$-1$</td><td>$0$</td></tr>
    <tr><td>$T$</td><td>$0$</td><td>$1$</td><td>$1$</td><td>$2$</td></tr></tbody></table>
    המצבים $(0,1)$ ו-$(1,0)$ נותנים אותו זוג $(D,T)=(-1,1)$, ולכן התא הזה הוא $(1-p)q+p(1-q)=p+q-2pq$. ההסתברות $P(D=0)=pq$, כלומר $D+1=XY$ הוא <b>ברנולי</b> עם פרמטר $pq$ (ואם $p=q$, פרמטר $p^2$). בנוסף $E[D]=pq-1$, $E[T]=p+q$, $E[DT]=2pq-p-q$, ולכן $\mathrm{Cov}(D,T)=pq(2-p-q)$.</div>
    <div class="lesson-rule">🔑 שאלת "האם $D$ ו-$T$ בלתי תלויים?" עונים כמו תמיד: או שמוצאים תא שבו הטבלה שונה ממכפלת השוליים (בדרך כלל $0$), או שמראים ש-$D$ תלוי רק ב-$X$ ו-$T$ תלוי רק ב-$Y$ (אז הם בלתי תלויים).</div>
    <div class="lesson-trap">⚠️ אל תשכחו לקבץ מצבים (שני מצבים באותו תא), ואל תשכחו ש-$X^2=X$ רק עבור ביטים. ואם הם מתואמים או לא: צריך $\mathrm{Cov}\ne0$, ולא רק "נראה תלוי".</div>` },
  questions: [
    { id: "joint-C08-Q1",
      step: { type: "numeric", answer: 0.25, tol: 0.001,
              prompt: String.raw`$X,Y\sim\mathrm{Ber}(\frac12)$ בלתי תלויים, ונתונה המטריצה $\boldsymbol C=\begin{pmatrix}X&0\\0&Y\end{pmatrix}$ עם $D=\det\boldsymbol C$. מהו $P(D=1)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$D=X\cdot Y-0\cdot0=XY$. הוא $1$ רק כש-$X=Y=1$, בהסתברות $\frac12\cdot\frac12=\frac14$. כלומר $D\sim\mathrm{Ber}(pq)$.` },
      sim: { kind: "bernoulli_matrix", estimate: "P(D=1)", exact: 0.25, params: { n: 2, p: [[0.5, 0], [0, 0.5]], event: "det == 1" } },
      recap: "$XY$ הוא ברנולי עם פרמטר $pq$." },
    { id: "joint-C08-Q2",
      step: { type: "numeric", answer: 0.6, tol: 0.001,
              prompt: String.raw`$X,Y\sim\mathrm{Ber}(p)$ בלתי תלויים (אותו $p$), ו-$D=\det\begin{pmatrix}X&0\\0&Y\end{pmatrix}=XY$. עבור איזה $p$ מתקיים $P(D=1)=0.36$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$D=XY\sim\mathrm{Ber}(p^2)$, ולכן $p^2=0.36$ ו-$p=0.6$ (הערך השלילי $-0.6$ אינו הסתברות).` },
      sim: { kind: "custom_discrete", estimate: "P(D=1) ב-p=0.6", exact: 0.36,
             params: { vars: { X: { values: [0, 1], probs: [0.4, 0.6] }, Y: { values: [0, 1], probs: [0.4, 0.6] } }, event: "X*Y == 1" } },
      recap: "$D=XY$ הוא $\\mathrm{Ber}(p^2)$." },
    { id: "joint-C08-Q3",
      question: String.raw`$X\sim\mathrm{Ber}(p)$ ו-$Y\sim\mathrm{Ber}(q)$ בלתי תלויים. עבור $\boldsymbol C=\begin{pmatrix}X&0\\0&Y\end{pmatrix}$ מגדירים $D=\det\boldsymbol C=XY$ ו-$T=\mathrm{tr}\,\boldsymbol C=X+Y$. מהו $P(D=0,\ T=1)$ ?`,
      options: [{ id: "a", value: "$p+q-2pq$" }, { id: "b", value: "$p+q-pq$" }, { id: "c", value: "$p+q$" }, { id: "d", value: "$2pq$" }],
      correctId: "a",
      explanation: String.raw`$T=1$ אומר שבדיוק אחד מהשניים הוא $1$, ואז $D=XY=0$ אוטומטית. ההסתברות היא $p(1-q)+(1-p)q=p+q-2pq$. הביטוי $p+q-pq$ הוא ההסתברות ש-$X=1$ או $Y=1$ (לפחות אחד) ומכליל גם את המצב $(1,1)$ שבו $T=2$. הביטוי $p+q$ מחבר בלי להפחית כפל, והביטוי $2pq$ מתאים למצב $(1,1)$ בלבד, כפול שניים.`,
      sim: { kind: "custom_discrete", estimate: "P(D=0, T=1) ב-p=0.3, q=0.6", exact: 0.54,
             params: { vars: { X: { values: [0, 1], probs: [0.7, 0.3] }, Y: { values: [0, 1], probs: [0.4, 0.6] } }, event: "X+Y == 1" } },
      recap: "מצבים שונים באותו תא: $(0,1)$ ו-$(1,0)$ נחברים." },
    { id: "joint-C08-Q4",
      step: { type: "numeric", answer: -0.09375, tol: 0.001,
              prompt: String.raw`$X\sim\mathrm{Ber}(\frac14)$ ו-$Y\sim\mathrm{Ber}(\frac12)$ בלתי תלויים, ונתונה $\boldsymbol G=\begin{pmatrix}X&Y\\1&Y\end{pmatrix}$ עם $D=\det\boldsymbol G=XY-Y$ ו-$T=\mathrm{tr}\,\boldsymbol G=X+Y$. מהי $\mathrm{Cov}(D,T)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$D=-1$ רק במצב $(X,Y)=(0,1)$ (אז $0-1=-1$), ובשאר המצבים $D=0$. לכן $E[D]=-P(0,1)=-\frac34\cdot\frac12=-\frac38$. $E[T]=\frac14+\frac12=\frac34$. $E[DT]=(-1)\cdot1\cdot\frac38=-\frac38$, כי ב-$(0,1)$ מתקיים $T=1$. $\mathrm{Cov}=-\frac38-(-\frac38)(\frac34)=-\frac38\cdot\frac14=-\frac3{32}=-0.09375$.` },
      sim: { kind: "custom_discrete", estimate: "Cov(D,T)", exact: -0.09375,
             params: { vars: { X: { values: [0, 1], probs: [0.75, 0.25] }, Y: { values: [0, 1], probs: [0.5, 0.5] } }, measure: "cov", expr: ["X*Y-Y", "X+Y"] } },
      recap: "בונים טבלה של ארבעת המצבים ומחשבים $E[D],E[T],E[DT]$." },
    { id: "joint-C08-Q5",
      question: String.raw`$X,Y$ ברנולי בלתי תלויים, ונתונה $\boldsymbol Q=\begin{pmatrix}Y&X\\1&0\end{pmatrix}$ עם $D=\det\boldsymbol Q$ ו-$T=\mathrm{tr}\,\boldsymbol Q$. האם $D$ ו-$T$ בלתי תלויים?`,
      options: [
        { id: "a", value: "כן, כי D תלוי רק ב-X ו-T תלוי רק ב-Y" },
        { id: "b", value: "לא, כי שניהם מוגדרים מאותה מטריצה" },
        { id: "c", value: "לא, כי יש תא אפס בטבלה" },
        { id: "d", value: "כן, אבל רק אם p = q" }],
      correctId: "a",
      explanation: String.raw`$D=Y\cdot0-X\cdot1=-X$ ו-$T=Y+0=Y$. פונקציה של $X$ ופונקציה של $Y$ הן בלתי תלויות כש-$X,Y$ בלתי תלויים, לכל $p,q$. מוצא משותף של המטריצה לא יוצר תלות. תא אפס לא מוכיח תלות אלא אם שוליו חיוביים, וכאן הטבלה היא מכפלה.`,
      sim: { kind: "custom_discrete", estimate: "Cov(D,T) ב-p=0.3, q=0.6", exact: 0,
             params: { vars: { X: { values: [0, 1], probs: [0.7, 0.3] }, Y: { values: [0, 1], probs: [0.4, 0.6] } }, measure: "cov", expr: ["-X", "Y"] } },
      recap: "פונקציות של משתנים בלתי תלויים נפרדים הן בלתי תלויות." },
    { id: "joint-C08-Q6",
      step: { type: "numeric", answer: 0.7071, tol: 0.002,
              prompt: String.raw`$X,Y\sim\mathrm{Ber}(\frac12)$ בלתי תלויים, ו-$\boldsymbol B=\begin{pmatrix}X&Y\\Y&X\end{pmatrix}$ עם $D=\det\boldsymbol B$ ו-$T=\mathrm{tr}\,\boldsymbol B$. מהו מקדם המתאם $\rho(D,T)$ ? (עשרוני, דיוק של שלוש ספרות)`,
              explain: String.raw`$D=X^2-Y^2=X-Y$ ו-$T=2X$. $\mathrm{Var}[D]=\frac14+\frac14=\frac12$, $\mathrm{Var}[T]=4\cdot\frac14=1$, $\mathrm{Cov}(D,T)=\mathrm{Cov}(X-Y,2X)=2\mathrm{Var}[X]=\frac12$. לכן $\rho=\frac{1/2}{\sqrt{\frac12\cdot1}}=\frac1{\sqrt2}\approx0.7071$.` },
      recap: "מפשטים עם $X^2=X$, ואז $\\mathrm{Cov}$ ושונויות." },
  ],
});
