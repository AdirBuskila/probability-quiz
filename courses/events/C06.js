/* events, level 6 - total probability. */
COURSE_LEVEL("events", {
  id: "C06", order: 6, icon: "🧱", title: "הסתברות שלמה",
  goal: "אחרי השלב הזה אפשר לפצל מאורע לפי מקרים, לחשב בכל מקרה, ולחבר: $P(B)=\\sum P(B/A_i)P(A_i)$.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>לפעמים $P(B)$ לא נתון, אבל ידוע מה קורה בכל "מקרה" אפשרי. <b>חלוקה</b> של $\Omega$ היא אוסף מאורעות $A_1,\dots,A_n$ ש<b>זרים בזוגות</b> ו<b>איחודם הוא $\Omega$</b> (כל תוצאה שייכת לבדיוק אחד מהם). למשל $A$ ו-$\overline{A}$ תמיד חלוקה.</p>
    <div class="lesson-rule">🔑 <b>הסתברות שלמה:</b> $$P(B)=\sum_i P(B/A_i)\,P(A_i)$$ ובשני מקרים: $P(B)=P(B/A)P(A)+P(B/\overline{A})P(\overline{A})$. זה ממוצע <b>משוקלל</b>: כל הסתברות מותנית מוכפלת בהסתברות של המקרה שלה.</div>
    <div class="lesson-ex"><b>דוגמה.</b> מכונה 1 מייצרת $60\%$ מהפריטים וב-$2\%$ מהם יש פגם. מכונה 2 מייצרת $40\%$ וב-$5\%$ מהם יש פגם. פריט אקראי פגום בהסתברות $$0.6\cdot0.02+0.4\cdot0.05=0.012+0.02=0.032.$$</div>
    <div class="lesson-trap">⚠️ המשקלים הם הסתברויות של <b>המקרים</b> ($P(A_i)$), לא של התוצאה. ואסור להחליף ביניהם: $P(B/A)P(\overline{A})$ הוא שגוי.</div>
    <h3>כדור שני בלי החזרה</h3>
    <p>בכד 3 אדומים ו-7 שחורים, מוציאים שניים בלי החזרה. מפצלים לפי הכדור הראשון: $$P(R_2)=\frac3{10}\cdot\frac29+\frac7{10}\cdot\frac39=\frac{27}{90}=\frac3{10}.$$ זו אותה הסתברות כמו של הכדור הראשון, וזה לא מקרה (עוד על כך בשלב על כדים).</p>` },
  questions: [
    { id: "events-C06-Q1",
      step: { type: "numeric", answer: 0.032, tol: 0.0005,
              prompt: String.raw`מכונה 1 מייצרת $60\%$ מהפריטים, ו-$2\%$ מהם פגומים. מכונה 2 מייצרת $40\%$, ו-$5\%$ מהם פגומים. מהי ההסתברות שפריט אקראי פגום?`,
              explain: String.raw`$0.6\cdot0.02+0.4\cdot0.05=0.032$. התשובה $0.035$ היא ממוצע פשוט של $2\%$ ו-$5\%$, בלי משקלים.` },
      sim: { kind: "custom_discrete", estimate: "P(פגום)", exact: 0.032, params: { joint: [{ p: 0.012, M: 1, D: 1 }, { p: 0.588, M: 1, D: 0 }, { p: 0.02, M: 2, D: 1 }, { p: 0.38, M: 2, D: 0 }], event: "D == 1" } },
      recap: String.raw`ממוצע משוקלל של ההסתברויות המותנות.` },
    { id: "events-C06-Q2",
      step: { type: "numeric", answer: 0.19, tol: 0.001,
              prompt: String.raw`בוחרים קופסה באקראי: קופסה 1 בהסתברות $0.5$, קופסה 2 בהסתברות $0.3$, קופסה 3 בהסתברות $0.2$. ההסתברות לשלוף כדור אדום היא $0.1$ בקופסה 1, $0.2$ בקופסה 2 ו-$0.4$ בקופסה 3. מהי ההסתברות לשלוף כדור אדום?`,
              explain: String.raw`$0.5\cdot0.1+0.3\cdot0.2+0.2\cdot0.4=0.05+0.06+0.08=0.19$. שלוש קופסאות הן חלוקה: המשקלים מסתכמים ל-$1$.` },
      sim: { kind: "custom_discrete", estimate: "P(אדום)", exact: 0.19, params: { joint: [{ p: 0.05, K: 1, R: 1 }, { p: 0.45, K: 1, R: 0 }, { p: 0.06, K: 2, R: 1 }, { p: 0.24, K: 2, R: 0 }, { p: 0.08, K: 3, R: 1 }, { p: 0.12, K: 3, R: 0 }], event: "R == 1" } },
      recap: String.raw`סכום על כל המקרים של החלוקה.` },
    { id: "events-C06-Q3",
      step: { type: "numeric", answer: 0.3, tol: 0.001,
              prompt: String.raw`בכד 3 כדורים אדומים ו-7 שחורים. מוציאים שני כדורים בלי החזרה. מהי ההסתברות שהכדור **השני** אדום? (פצלו לפי הכדור הראשון)`,
              explain: String.raw`אם הראשון אדום ($\frac3{10}$): השני אדום בהסתברות $\frac29$. אם הראשון שחור ($\frac7{10}$): $\frac39$. הסכום $\frac{6}{90}+\frac{21}{90}=\frac{27}{90}=0.3$. התשובה $\frac29\approx0.22$ היא המקרה הראשון בלבד.` },
      sim: { kind: "urn", estimate: "P(השני אדום)", exact: 0.3, params: { counts: { red: 3, black: 7 }, draws: 2, replace: false, event: "red_2" } },
      recap: String.raw`מפצלים לפי מה שקרה בשלב הראשון.` },
    { id: "events-C06-Q4",
      step: { type: "numeric", answer: 0.32, tol: 0.001,
              prompt: String.raw`$P(A)=0.4$, $P(B/A)=0.5$ ו-$P(B/\overline{A})=0.2$. מהי $P(B)$ ?`,
              explain: String.raw`$P(B)=0.5\cdot0.4+0.2\cdot0.6=0.2+0.12=0.32$. שימו לב ש-$P(\overline{A})=0.6$ ולא $0.4$.` },
      sim: { kind: "custom_discrete", estimate: "P(B)", exact: 0.32, params: { joint: [{ p: 0.2, A: 1, B: 1 }, { p: 0.2, A: 1, B: 0 }, { p: 0.12, A: 0, B: 1 }, { p: 0.48, A: 0, B: 0 }], event: "B == 1" } },
      recap: String.raw`$P(B)=P(B/A)P(A)+P(B/\overline{A})P(\overline{A})$.` },
    { id: "events-C06-Q5",
      step: { type: "findbug",
              prompt: String.raw`נתון $P(A)=0.3$, $P(B/A)=0.9$ ו-$P(B/\overline{A})=0.2$. בפתרון הבא של $P(B)$ **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`$P(\overline{A})=1-0.3=0.7$.`,
                String.raw`נפצל לפי $A$ ו-$\overline{A}$, שהם חלוקה של $\Omega$.`,
                String.raw`$P(B)=P(B/A)P(\overline{A})+P(B/\overline{A})P(A)=0.9\cdot0.7+0.2\cdot0.3=0.69$.`,
              ],
              bugIndex: 2,
              explain: String.raw`כל הסתברות מותנית מוכפלת בהסתברות של המקרה שלה: $P(B/A)$ עם $P(A)$ ו-$P(B/\overline{A})$ עם $P(\overline{A})$. הנכון: $0.9\cdot0.3+0.2\cdot0.7=0.27+0.14=0.41$.` },
      recap: String.raw`המשקל של $P(B/A)$ הוא $P(A)$.` },
    { id: "events-C06-Q6",
      question: String.raw`מטילים קובייה הוגנת. איזה זוג מאורעות הוא **חלוקה** של $\Omega$?`,
      options: [
        { id: "a", value: "\"התוצאה זוגית\" ו\"התוצאה גדולה מ-3\"" },
        { id: "b", value: "\"התוצאה קטנה מ-3\" ו\"התוצאה גדולה מ-4\"" },
        { id: "c", value: "\"התוצאה זוגית\" ו\"התוצאה אי-זוגית\"" },
        { id: "d", value: "\"התוצאה לכל היותר 3\" ו\"התוצאה גדולה מ-3 וקטנה מ-6\"" }],
      correctId: "c",
      explanation: "חלוקה דורשת שני תנאים: זרים, ואיחודם כל המרחב. \"זוגית\" ו\"אי-זוגית\" מקיימים את שניהם. הזוג הראשון לא זר (4 ו-6 בשניהם). בזוג השני התוצאות 3 ו-4 לא שייכות לאף אחד מהם. בזוג האחרון התוצאה 6 חסרה.",
      recap: "חלוקה: זרים ומכסים את כל $\\Omega$." },
  ],
});
