/* events, level 3 - the family P(A)=p, P(B)=q, P(A or B)=s: intersection, cells, disjoint, independent, "can it be". */
COURSE_LEVEL("events", {
  id: "C03", order: 3, icon: "🧮", title: "הנתונים p, q, s: חיתוך, זרים ובלתי תלויים",
  goal: "אחרי השלב הזה אפשר, מתוך $P(A)$, $P(B)$ ו-$P(A\\cup B)$, לחשב את כל ארבעת התאים, ולהכריע מתי המאורעות זרים, מתי בלתי תלויים, ומתי הנתונים בכלל אפשריים.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>שאלה מאוד נפוצה במבחנים: נתונים $P(A)=p$, $P(B)=q$ ו-$P(A\cup B)=s$ (או שלושה נתונים דומים), ושואלים על חיתוך, על הפרש, על זרים ועל בלתי תלויים. הכול נובע מכלל האיחוד.</p>
    <div class="lesson-rule">🔑 $$P(A\cap B)=p+q-s$$ (זה כלל האיחוד $s=p+q-P(A\cap B)$, מסודר מחדש.)</div>
    <h3>ארבעה תאים</h3>
    <p>שני מאורעות מחלקים את $\Omega$ לארבעה תאים זרים שסכומם $1$:</p>
    <table><thead><tr><th></th><th>$B$</th><th>$\overline{B}$</th></tr></thead><tbody>
      <tr><td>$A$</td><td>$A\cap B=p+q-s$</td><td>$A\setminus B=s-q$</td></tr>
      <tr><td>$\overline{A}$</td><td>$B\setminus A=s-p$</td><td>$\overline{A}\cap\overline{B}=1-s$</td></tr>
    </tbody></table>
    <p>סכום השורה העליונה הוא $p$, סכום העמודה השמאלית הוא $q$. שלושה נתונים קובעים את כל הטבלה.</p>
    <h3>זרים ובלתי תלויים</h3>
    <ul>
      <li><b>זרים:</b> $A\cap B=\varnothing$, כלומר $P(A\cap B)=0$, כלומר $s=p+q$.</li>
      <li><b>בלתי תלויים:</b> $P(A\cap B)=P(A)\,P(B)$, כלומר $p+q-s=pq$.</li>
    </ul>
    <div class="lesson-ex"><b>דוגמה.</b> $p=0.5$, $q=0.4$, $s=0.7$. החיתוך $0.5+0.4-0.7=0.2$. הטבלה: $A\cap B=0.2$, $A\setminus B=0.3$, $B\setminus A=0.2$, אף אחד $0.3$ (סכום $1$). הם לא זרים ($0.2\ne0$). בלתי תלויים? $pq=0.2$ והחיתוך $0.2$, כן.</div>
    <h3>האם הנתונים אפשריים?</h3>
    <p>כל תא חייב להיות בין $0$ ל-$1$. מכאן: $s\ge\max(p,q)$ (האיחוד לא קטן ממאורע שבתוכו), $s\le1$ ו-$s\le p+q$ (החיתוך לא שלילי).</p>
    <div class="lesson-trap">⚠️ מצאתם חיתוך שלילי, או תא גדול מהשורה שלו? הנתונים סותרים, ואף מאורעות לא מקיימים אותם.</div>` },
  questions: [
    { id: "events-C03-Q1",
      step: { type: "numeric", answer: 0.2, tol: 0.001,
              prompt: String.raw`$P(A)=0.5$, $P(B)=0.4$ ו-$P(A\cup B)=0.7$. מהי $P(A\cap B)$ ?`,
              explain: String.raw`$0.5+0.4-0.7=0.2$. התשובה $0.9$ היא $p+q$, בלי להחסיר את $s$.` },
      sim: { kind: "custom_discrete", estimate: "P(A וגם B)", exact: 0.2, params: { joint: [{ p: 0.2, A: 1, B: 1 }, { p: 0.3, A: 1, B: 0 }, { p: 0.2, A: 0, B: 1 }, { p: 0.3, A: 0, B: 0 }], event: "A == 1 and B == 1" } },
      recap: String.raw`$P(A\cap B)=p+q-s$.` },
    { id: "events-C03-Q2",
      step: { type: "numeric", answer: 0.3, tol: 0.001,
              prompt: String.raw`אותם נתונים: $P(A)=0.5$, $P(B)=0.4$, $P(A\cup B)=0.7$. מהי $P(A\setminus B)$, ההסתברות ש-$A$ קרה ו-$B$ לא ?`,
              explain: String.raw`$P(A\setminus B)=s-q=0.7-0.4=0.3$ (או $p-P(A\cap B)=0.5-0.2$). התשובה $0.2$ היא החיתוך.` },
      recap: String.raw`$P(A\setminus B)=s-q$.` },
    { id: "events-C03-Q3",
      question: String.raw`$P(A)=0.3$, $P(B)=0.5$ ו-$P(A\cup B)=0.8$. איזה משפט נכון?`,
      options: [
        { id: "a", value: "המאורעות זרים ואינם בלתי תלויים" },
        { id: "b", value: "המאורעות בלתי תלויים ואינם זרים" },
        { id: "c", value: "המאורעות גם זרים וגם בלתי תלויים" },
        { id: "d", value: "המאורעות לא זרים ולא בלתי תלויים" }],
      correctId: "a",
      sim: { kind: "custom_discrete", estimate: "P(A או B)", exact: 0.8, params: { joint: [{ p: 0, A: 1, B: 1 }, { p: 0.3, A: 1, B: 0 }, { p: 0.5, A: 0, B: 1 }, { p: 0.2, A: 0, B: 0 }], event: "A == 1 or B == 1" } },
      explanation: String.raw`$P(A\cap B)=0.3+0.5-0.8=0$, ולכן הם זרים. בלתי תלויים היו אם החיתוך היה $pq=0.15$, אבל הוא $0\ne0.15$. מאורעות עם הסתברות חיובית שהם זרים אינם בלתי תלויים.`,
      recap: String.raw`זרים: $s=p+q$. בלתי תלויים: $p+q-s=pq$.` },
    { id: "events-C03-Q4",
      step: { type: "numeric", answer: 0.7, tol: 0.001,
              prompt: String.raw`$P(A)=0.4$ ו-$P(B)=0.5$, והמאורעות בלתי תלויים. מהי $P(A\cup B)$ ?`,
              explain: String.raw`בלתי תלויים: $P(A\cap B)=0.4\cdot0.5=0.2$. לכן $s=0.4+0.5-0.2=0.7$. התשובה $0.9$ היא $p+q$ בלי להחסיר את החיתוך.` },
      sim: { kind: "custom_discrete", estimate: "P(A או B)", exact: 0.7, params: { joint: [{ p: 0.2, A: 1, B: 1 }, { p: 0.2, A: 1, B: 0 }, { p: 0.3, A: 0, B: 1 }, { p: 0.3, A: 0, B: 0 }], event: "A == 1 or B == 1" } },
      recap: String.raw`בלתי תלויים: $s=p+q-pq$.` },
    { id: "events-C03-Q5",
      question: String.raw`נתון $P(A)=0.6$ ו-$P(B)=0.7$. איזה ערך של $P(A\cup B)$ **אינו** אפשרי?`,
      options: [{ id: "a", value: "$0.65$" }, { id: "b", value: "$0.7$" }, { id: "c", value: "$0.9$" }, { id: "d", value: "$1$" }],
      correctId: "a",
      explanation: String.raw`האיחוד חייב להכיל את $B$, ולכן $s\ge0.7$. הערך $0.65$ קטן מ-$P(B)$: החיתוך היה $0.6+0.7-0.65=0.65>0.6=P(A)$, בלתי אפשרי. הערך $0.7$ אפשרי ($A\subseteq B$, חיתוך $0.6$), $0.9$ נותן חיתוך $0.4$, ו-$1$ נותן חיתוך $0.3$, שניהם תקינים.`,
      recap: String.raw`$\max(p,q)\le s\le\min(1,p+q)$.` },
    { id: "events-C03-Q6",
      step: { type: "numeric", answer: 0.6, tol: 0.001,
              prompt: String.raw`$P(A)=0.3$, $P(B)=0.5$ ו-$P(A\cup B)=0.7$. מהי ההסתברות שקרה בדיוק אחד משני המאורעות?`,
              explain: String.raw`החיתוך $0.3+0.5-0.7=0.1$. בדיוק אחד: $A\setminus B$ ועוד $B\setminus A$, כלומר $(0.3-0.1)+(0.5-0.1)=0.6$ (או $s-P(A\cap B)=0.7-0.1$). התשובה $0.7$ היא "לפחות אחד".` },
      sim: { kind: "custom_discrete", estimate: "P(בדיוק אחד)", exact: 0.6, params: { joint: [{ p: 0.1, A: 1, B: 1 }, { p: 0.2, A: 1, B: 0 }, { p: 0.4, A: 0, B: 1 }, { p: 0.3, A: 0, B: 0 }], event: "A + B == 1" } },
      recap: String.raw`בדיוק אחד $=s-P(A\cap B)$.` },
  ],
});
