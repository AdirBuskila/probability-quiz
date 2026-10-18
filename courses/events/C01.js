/* events, level 1 - event algebra: union, intersection, complement, difference, De Morgan. */
COURSE_LEVEL("events", {
  id: "C01", order: 1, icon: "🧩", title: "אלגברה של מאורעות",
  goal: "אחרי השלב הזה אפשר לתרגם משפט כמו \"לפחות אחד\", \"אף אחד\" או \"בדיוק אחד\" למאורע, לחשב את גודלו, ולהשתמש בחוקי דה מורגן.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p><b>מרחב המדגם</b> $\Omega$ הוא אוסף כל התוצאות האפשריות של הניסוי. <b>מאורע</b> הוא תת-קבוצה של $\Omega$. כשכל התוצאות סבירות באותה מידה (קובייה הוגנת, מטבע הוגן), ההסתברות היא ספירה:</p>
    <div class="lesson-rule">🔑 $$P(A)=\frac{|A|}{|\Omega|}$$</div>
    <h3>הפעולות</h3>
    <table><thead><tr><th>במילים</th><th>סימון</th><th>מה זה</th></tr></thead><tbody>
      <tr><td>"$A$ או $B$" (לפחות אחד מהם)</td><td>$A\cup B$</td><td>איחוד: כל תוצאה שבאחד מהם לפחות</td></tr>
      <tr><td>"$A$ וגם $B$" (שניהם)</td><td>$A\cap B$</td><td>חיתוך: תוצאות שבשניהם</td></tr>
      <tr><td>"לא $A$"</td><td>$\overline{A}$</td><td>משלים: כל מה שב-$\Omega$ ואינו ב-$A$</td></tr>
      <tr><td>"$A$ אבל לא $B$"</td><td>$A\setminus B=A\cap\overline{B}$</td><td>הפרש</td></tr>
    </tbody></table>
    <p>מאורעות <b>זרים</b> הם מאורעות שאין להם תוצאה משותפת: $A\cap B=\varnothing$.</p>
    <h3>חוקי דה מורגן</h3>
    <div class="lesson-rule">🔑 $$\overline{A\cup B}=\overline{A}\cap\overline{B}\qquad\qquad \overline{A\cap B}=\overline{A}\cup\overline{B}$$ המשלים הופך "או" ל"וגם" ו"וגם" ל"או". במילים: "לא קרה אף אחד משניהם" הוא "גם $A$ לא קרה וגם $B$ לא קרה".</div>
    <h3>משפטים נפוצים</h3>
    <ul>
      <li>לפחות אחד: $A\cup B$.</li>
      <li>אף אחד: $\overline{A\cup B}=\overline{A}\cap\overline{B}$.</li>
      <li>בדיוק אחד: $(A\setminus B)\cup(B\setminus A)$.</li>
      <li>שניהם: $A\cap B$.</li>
    </ul>
    <div class="lesson-ex"><b>דוגמה.</b> מטילים קובייה הוגנת, $\Omega=\{1,2,3,4,5,6\}$. $A$ = "התוצאה זוגית" $=\{2,4,6\}$ ו-$B$ = "התוצאה גדולה מ-3" $=\{4,5,6\}$.
    <br>$A\cap B=\{4,6\}$, $A\cup B=\{2,4,5,6\}$, $A\setminus B=\{2\}$, $B\setminus A=\{5\}$, $\overline{A\cup B}=\{1,3\}$.
    <br>שלוש קבוצות בנות שתי תוצאות כל אחת: שניהם $\{4,6\}$, בדיוק אחד $\{2,5\}$, אף אחד $\{1,3\}$. יחד הן מכסות את כל שש התוצאות. לכן $P(A\cup B)=\frac46=\frac23$.</div>
    <div class="lesson-trap">⚠️ $|A\cup B|$ אינו $|A|+|B|$. כאן $3+3=6$, אבל באיחוד יש רק 4 תוצאות, כי $4$ ו-$6$ נספרו פעמיים. על כך בשלב הבא.</div>` },
  questions: [
    { id: "events-C01-Q1",
      step: { type: "numeric", answer: 2, tol: 0,
              prompt: String.raw`מטילים קובייה הוגנת. $A$ = "התוצאה זוגית", $B$ = "התוצאה גדולה מ-3". כמה תוצאות יש במאורע $A\cap B$ ?`,
              explain: String.raw`$A=\{2,4,6\}$ ו-$B=\{4,5,6\}$. החיתוך הוא התוצאות שבשניהם: $\{4,6\}$, כלומר 2 תוצאות. התשובה 4 היא גודל האיחוד, ו-3 הוא גודל של כל אחד מהמאורעות לבדו.` },
      recap: String.raw`חיתוך = התוצאות שבשני המאורעות יחד.` },
    { id: "events-C01-Q2",
      question: String.raw`מטילים קובייה הוגנת. $A$ = "התוצאה זוגית", $B$ = "התוצאה גדולה מ-3". מהי $P(A\cup B)$ ?`,
      options: [{ id: "a", value: String.raw`$\frac{1}{2}$` }, { id: "b", value: String.raw`$\frac{2}{3}$` }, { id: "c", value: "$1$" }, { id: "d", value: String.raw`$\frac{1}{3}$` }],
      correctId: "b",
      sim: { kind: "dice", estimate: "P(זוגי או גדול מ-3)", exact: 2 / 3, params: { n: 1, event: "d1 % 2 == 0 or d1 > 3" } },
      explanation: String.raw`$A\cup B=\{2,4,5,6\}$ ולכן $P=\frac46=\frac23$. התשובה $1$ מתקבלת מחיבור $|A|+|B|=6$ בלי להוריד את החיתוך $\{4,6\}$ שנספר פעמיים. $\frac12$ היא $P(A)$ בלבד, ו-$\frac13$ היא $P(A\cap B)$.`,
      recap: String.raw`איחוד: סופרים כל תוצאה פעם אחת.` },
    { id: "events-C01-Q3",
      question: String.raw`מהו המאורע "לא קרה אף אחד משני המאורעות $A$ ו-$B$" ?`,
      options: [{ id: "a", value: String.raw`$\overline{A}\cup\overline{B}$` }, { id: "b", value: String.raw`$\overline{A}\cap\overline{B}$` }, { id: "c", value: String.raw`$A\cap B$` }, { id: "d", value: String.raw`$\overline{A\cap B}$` }],
      correctId: "b",
      explanation: String.raw`"אף אחד" הוא המשלים של "לפחות אחד": $\overline{A\cup B}$, ולפי דה מורגן זה $\overline{A}\cap\overline{B}$, כלומר גם $A$ לא קרה וגם $B$ לא קרה. התשובות $\overline{A}\cup\overline{B}$ ו-$\overline{A\cap B}$ שוות זו לזו והן אומרות "לא קרו שניהם יחד" (לפחות אחד לא קרה), וזה מאורע גדול יותר. $A\cap B$ הוא "קרו שניהם".`,
      recap: String.raw`אף אחד: $\overline{A}\cap\overline{B}$. לא שניהם: $\overline{A}\cup\overline{B}$.` },
    { id: "events-C01-Q4",
      step: { type: "numeric", answer: 0.3333, tol: 0.002,
              prompt: String.raw`מטילים קובייה הוגנת. $A$ = "זוגית", $B$ = "גדולה מ-3". מהי ההסתברות שלא קרה אף אחד משני המאורעות? (שבר או עשרוני)`,
              explain: String.raw`"אף אחד" הוא תוצאה שאינה זוגית וגם אינה גדולה מ-3: $\overline{A}\cap\overline{B}=\{1,3,5\}\cap\{1,2,3\}=\{1,3\}$. ההסתברות $\frac26=\frac13$.` },
      sim: { kind: "dice", estimate: "P(לא זוגי וגם לא גדול מ-3)", exact: 1 / 3, params: { n: 1, event: "d1 % 2 == 1 and d1 <= 3" } },
      recap: String.raw`אף אחד = חיתוך המשלימים.` },
    { id: "events-C01-Q5",
      question: String.raw`מטילים קובייה הוגנת. $A$ = "זוגית", $B$ = "גדולה מ-3". מהי ההסתברות שקרה **בדיוק אחד** משני המאורעות?`,
      options: [{ id: "a", value: String.raw`$\frac{1}{6}$` }, { id: "b", value: String.raw`$\frac{1}{3}$` }, { id: "c", value: String.raw`$\frac{1}{2}$` }, { id: "d", value: String.raw`$\frac{2}{3}$` }],
      correctId: "b",
      sim: { kind: "dice", estimate: "P(בדיוק אחד)", exact: 1 / 3, params: { n: 1, event: "(d1 % 2 == 0 and d1 <= 3) or (d1 % 2 == 1 and d1 > 3)" } },
      explanation: String.raw`בדיוק אחד: $(A\setminus B)\cup(B\setminus A)=\{2\}\cup\{5\}=\{2,5\}$, ולכן $\frac26=\frac13$. התשובה $\frac23$ היא "לפחות אחד" (כוללת גם את $\{4,6\}$ שבהם קרו שניהם), ו-$\frac16$ היא תוצאה אחת בלבד.`,
      recap: String.raw`בדיוק אחד = $(A\setminus B)\cup(B\setminus A)$, בלי החיתוך.` },
    { id: "events-C01-Q6",
      step: { type: "findbug",
              prompt: String.raw`מטילים קובייה הוגנת, $A$ = "זוגית", $B$ = "גדולה מ-3". בפתרון הבא של "מה ההסתברות שלא קרה אף אחד מהם" **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`$\overline{A}=\{1,3,5\}$ ו-$\overline{B}=\{1,2,3\}$.`,
                String.raw`המאורע "אף אחד משניהם לא קרה" הוא $\overline{A\cup B}$.`,
                String.raw`לפי דה מורגן, $\overline{A\cup B}=\overline{A}\cup\overline{B}$.`,
                String.raw`החיתוך $\overline{A}\cap\overline{B}=\{1,3\}$, ולכן ההסתברות היא $\frac26=\frac13$.`,
              ],
              bugIndex: 2,
              explain: String.raw`דה מורגן הופך איחוד לחיתוך: $\overline{A\cup B}=\overline{A}\cap\overline{B}$. השורה האחרונה כבר משתמשת בחיתוך, וזה אכן נותן את התשובה הנכונה $\frac13$. האיחוד $\{1,2,3,5\}$ היה נותן $\frac23$, וזה "לא שניהם".` },
      recap: String.raw`דה מורגן: המשלים של איחוד הוא חיתוך המשלימים.` },
  ],
});
