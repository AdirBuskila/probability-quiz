/* joint, level 2 - marginal distributions: row sums and column sums. */
COURSE_LEVEL("joint", {
  id: "C02", order: 2, icon: "➕", title: "התפלגויות שוליות: סכום שורות וסכום עמודות",
  goal: "אחרי השלב הזה אפשר לקבל את ההתפלגות של $X$ לבדה ושל $Y$ לבדה מתוך הטבלה המשותפת, ולהבין למה השוליים לא קובעים את הטבלה.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>מהטבלה המשותפת אפשר לשחזר את ההתפלגות של כל משתנה בנפרד. התפלגות כזו נקראת <b>שולית</b>, כי היא נרשמת בשוליים של הטבלה.</p>
    <div class="lesson-rule">🔑 $$P_X(x)=\sum_y P_{XY}(x,y),\qquad P_Y(y)=\sum_x P_{XY}(x,y).$$ כלומר $P_X(x)$ הוא סכום <b>השורה</b> של $x$, ו-$P_Y(y)$ הוא סכום <b>העמודה</b> של $y$. הסכום של כל ערכי $P_X$ הוא $1$, וכך גם של $P_Y$.</div>
    <div class="lesson-ex"><b>דוגמה.</b> הטבלה, עם השוליים בשורה האחרונה ובעמודה האחרונה:
    <table><thead><tr><th>$x\backslash y$</th><th>$0$</th><th>$1$</th><th>$P_X(x)$</th></tr></thead>
    <tbody><tr><td>$0$</td><td>$0.1$</td><td>$0.3$</td><td>$0.4$</td></tr>
    <tr><td>$1$</td><td>$0.2$</td><td>$0.4$</td><td>$0.6$</td></tr>
    <tr><td>$P_Y(y)$</td><td>$0.3$</td><td>$0.7$</td><td>$1$</td></tr></tbody></table>
    $P_X(0)=0.1+0.3=0.4$ ו-$P_Y(1)=0.3+0.4=0.7$.</div>
    <h3>מה הם השוליים?</h3>
    <p>בטבלת שלוש ההטלות מהשלב הקודם, $X=X_1+X_2$ הוא מספר העצים בשתי הטלות בלתי תלויות, ולכן $X\sim\mathrm{Bin}(2,p)$. כך גם $Y=X_2+X_3\sim\mathrm{Bin}(2,p)$. אפשר לאמת זאת מסכומי השורות: עבור $p=\frac12$ מתקבל $\frac14,\frac12,\frac14$, בדיוק ההתפלגות הבינומית $\mathrm{Bin}(2,\frac12)$.</p>
    <div class="lesson-trap">⚠️ השוליים <b>לא</b> קובעים את הטבלה המשותפת. שתי טבלאות שונות לגמרי יכולות לחלוק אותם שוליים. למשל, שני מטבעות הוגנים: אם הם בלתי תלויים, כל תא הוא $\frac14$. אם הם צמודים ($Y=X$), התאים האלכסוניים הם $\frac12$ והשאר $0$. בשני המקרים השוליים הם $\frac12,\frac12$.</div>` },
  questions: [
    { id: "joint-C02-Q1",
      step: { type: "numeric", answer: 0.5, tol: 0.001,
              prompt: String.raw`מטילים מטבע הוגן שלוש פעמים. $X$ הוא מספר העצים בשתי ההטלות הראשונות ו-$Y$ בשתי האחרונות. הטבלה המשותפת:
$$\begin{array}{c|ccc}x\backslash y&0&1&2\\ \hline 0&\frac18&\frac18&0\\ 1&\frac18&\frac14&\frac18\\ 2&0&\frac18&\frac18\end{array}$$
מהו $P_X(1)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`סוכמים את השורה $x=1$: $\frac18+\frac14+\frac18=\frac12$. אם סוכמים עמודה במקום שורה מקבלים את $P_Y$ ולא את $P_X$.` },
      sim: { kind: "custom_discrete", estimate: "P(X=1)", exact: 0.5,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       event: "X1 + X2 == 1" } },
      recap: "$P_X(x)$ הוא סכום השורה של $x$." },
    { id: "joint-C02-Q2",
      step: { type: "numeric", answer: 0.25, tol: 0.001,
              prompt: String.raw`מטילים מטבע הוגן שלוש פעמים. $X$ הוא מספר העצים בשתי ההטלות הראשונות ו-$Y$ בשתי האחרונות, והטבלה המשותפת:
$$\begin{array}{c|ccc}x\backslash y&0&1&2\\ \hline 0&\frac18&\frac18&0\\ 1&\frac18&\frac14&\frac18\\ 2&0&\frac18&\frac18\end{array}$$
מהו $P_Y(2)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`סוכמים את העמודה $y=2$: $0+\frac18+\frac18=\frac14$.` },
      sim: { kind: "custom_discrete", estimate: "P(Y=2)", exact: 0.25,
             params: { vars: { X1: { values: [0, 1], probs: [0.5, 0.5] }, X2: { values: [0, 1], probs: [0.5, 0.5] }, X3: { values: [0, 1], probs: [0.5, 0.5] } },
                       event: "X2 + X3 == 2" } },
      recap: "$P_Y(y)$ הוא סכום העמודה של $y$." },
    { id: "joint-C02-Q3",
      question: String.raw`$X$ הוא מספר העצים בשתי ההטלות הראשונות מבין שלוש הטלות של מטבע הוגן, והשוליים שלו הם $P_X(0)=\frac14$, $P_X(1)=\frac12$, $P_X(2)=\frac14$. מהי ההתפלגות של $X$ ?`,
      options: [{ id: "a", value: String.raw`$\mathrm{Bin}(2,\frac12)$` }, { id: "b", value: String.raw`$\mathrm{Bin}(3,\frac12)$` }, { id: "c", value: String.raw`$\mathrm{Ber}(\frac12)$` }, { id: "d", value: String.raw`$\mathrm{Geo}(\frac12)$` }],
      correctId: "a",
      explanation: String.raw`$\mathrm{Bin}(2,\frac12)$ נותנת $\binom20\frac14,\ \binom21\frac14,\ \binom22\frac14=\frac14,\frac12,\frac14$, בדיוק השוליים. זה גם הגיוני, כי $X$ סופר עצים בשתי הטלות. $\mathrm{Bin}(3,\frac12)$ מקבלת ארבעה ערכים. $\mathrm{Ber}(\frac12)$ מקבלת רק $0$ ו-$1$, ו-$\mathrm{Geo}(\frac12)$ מקבלת ערכים ללא חסם.`,
      recap: "שוליים של סכום ניסויי ברנולי בלתי תלויים הם בינומיים." },
    { id: "joint-C02-Q4",
      step: { type: "numeric", answer: 0.75, tol: 0.001,
              prompt: String.raw`$X$ ו-$Y$ הם שני ביטים הוגנים בלתי תלויים. נגדיר $D=XY$ ו-$T=X+Y$. הטבלה המשותפת של $(D,T)$:
$$\begin{array}{c|ccc}d\backslash t&0&1&2\\ \hline 0&\frac14&\frac12&0\\ 1&0&0&\frac14\end{array}$$
מהו $P_D(0)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`סוכמים את השורה $d=0$: $\frac14+\frac12+0=\frac34$. בדיקה: $P_D(1)=\frac14$, והסכום $1$.` },
      sim: { kind: "custom_discrete", estimate: "P(D=0)", exact: 0.75,
             params: { vars: { X: { values: [0, 1], probs: [0.5, 0.5] }, Y: { values: [0, 1], probs: [0.5, 0.5] } }, event: "X*Y == 0" } },
      recap: "מחברים את כל התאים בשורה, כולל אפסים." },
    { id: "joint-C02-Q5",
      question: String.raw`שני מטבעות הוגנים. ידוע ש-$P_X(0)=P_X(1)=\frac12$ ו-$P_Y(0)=P_Y(1)=\frac12$. מה אפשר להסיק על הטבלה המשותפת $P_{XY}$ ?`,
      options: [
        { id: "a", value: "אי אפשר לקבוע אותה, כי שוליים זהים מתאימים לכמה טבלאות שונות" },
        { id: "b", value: String.raw`היא חייבת להיות $\frac14$ בכל תא` },
        { id: "c", value: String.raw`היא חייבת להיות $\frac12$ על האלכסון ו-$0$ מחוץ לו` },
        { id: "d", value: "היא נקבעת באופן יחיד כמכפלת השוליים" }],
      correctId: "a",
      explanation: String.raw`אם $X,Y$ בלתי תלויים, כל תא הוא $\frac14$. אם $Y=X$, האלכסון הוא $\frac12$ והשאר $0$. בשני המקרים השוליים הם $\frac12,\frac12$, ולכן השוליים לבדם לא קובעים את הטבלה. שתי התשובות הספציפיות נכונות רק לאחד המקרים, והמכפלה נכונה רק כשיש אי-תלות.`,
      recap: "השוליים הם סכומי שורות ועמודות, והטבלה נשארת חופשית." },
  ],
});
