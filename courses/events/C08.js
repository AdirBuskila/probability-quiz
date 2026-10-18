/* events, level 8 - independent vs disjoint. */
COURSE_LEVEL("events", {
  id: "C08", order: 8, icon: "⚖️", title: "בלתי תלויים מול זרים",
  goal: "אחרי השלב הזה אפשר להכריע אם שני מאורעות בלתי תלויים, זרים, או שניהם, ולא לבלבל בין שני המושגים.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>שני מושגים שנשמעים דומים ואומרים דברים הפוכים כמעט:</p>
    <table><thead><tr><th></th><th>התנאי</th><th>המשמעות</th></tr></thead><tbody>
      <tr><td><b>זרים</b></td><td>$P(A\cap B)=0$</td><td>אם $A$ קרה אז $B$ בוודאות לא קרה. הם <b>תלויים</b> מאוד.</td></tr>
      <tr><td><b>בלתי תלויים</b></td><td>$P(A\cap B)=P(A)\,P(B)$</td><td>לדעת ש-$B$ קרה לא משנה את $P(A)$: $P(A/B)=P(A)$.</td></tr>
    </tbody></table>
    <div class="lesson-rule">🔑 אם $P(A)>0$ ו-$P(B)>0$, אז מאורעות <b>זרים</b> הם תמיד <b>תלויים</b> ($0\ne P(A)P(B)$), ומאורעות <b>בלתי תלויים</b> הם תמיד <b>לא זרים</b> ($P(A\cap B)=P(A)P(B)>0$).</div>
    <h3>איך בודקים</h3>
    <p>מחשבים את $P(A\cap B)$ ואת $P(A)P(B)$ ומשווים. מאורעות בלתי תלויים נשארים בלתי תלויים גם עם המשלים: אם $A,B$ בלתי תלויים אז גם $A,\overline{B}$.</p>
    <div class="lesson-ex"><b>דוגמה.</b> קובייה אחת. $A$ = "זוגית", $B$ = "גדולה מ-3". $P(A\cap B)=\frac26=\frac13$ ואילו $P(A)P(B)=\frac12\cdot\frac12=\frac14$. הם תלויים (ולא זרים). לעומת זאת, "הקובייה הראשונה זוגית" ו"הקובייה השנייה גדולה מ-3" בשתי הטלות נפרדות הם בלתי תלויים: $P=\frac12\cdot\frac12=\frac14$.</div>
    <div class="lesson-trap">⚠️ "הם זרים, ולכן בלתי תלויים" הוא שגוי. זרים אומר בדיוק ההפך: אחד מונע את השני.</div>
    <h3>עם p, q, s</h3>
    <p>עם $P(A)=p$, $P(B)=q$ ו-$P(A\cup B)=s$: בלתי תלויים כש-$p+q-s=pq$, כלומר $q=\dfrac{s-p}{1-p}$ (כש-$p\ne1$). זרים כש-$s=p+q$.</p>` },
  questions: [
    { id: "events-C08-Q1",
      question: String.raw`$P(A)=0.3$ ו-$P(B)=0.4$, והמאורעות זרים. איזה משפט נכון?`,
      options: [
        { id: "a", value: "הם תלויים, כי $P(A\\cap B)=0$ שונה מ-$0.12$" },
        { id: "b", value: "הם בלתי תלויים, כי זרים גורר בלתי תלויים" },
        { id: "c", value: "הם בלתי תלויים, כי $P(A\\cap B)=0$" },
        { id: "d", value: "אי אפשר לדעת" }],
      correctId: "a",
      explanation: String.raw`בלתי תלויים דורש $P(A\cap B)=0.3\cdot0.4=0.12$, אבל לזרים החיתוך הוא $0$. לכן הם תלויים. ידיעה ש-$A$ קרה מבטיחה ש-$B$ לא קרה.`,
      recap: String.raw`זרים עם הסתברות חיובית = תלויים.` },
    { id: "events-C08-Q2",
      step: { type: "numeric", answer: 0.58, tol: 0.001,
              prompt: String.raw`$A$ ו-$B$ בלתי תלויים, $P(A)=0.3$ ו-$P(B)=0.4$. מהי $P(A\cup B)$ ?`,
              explain: String.raw`$P(A\cap B)=0.12$, ולכן $0.3+0.4-0.12=0.58$. התשובה $0.7$ מתאימה למאורעות זרים.` },
      sim: { kind: "custom_discrete", estimate: "P(A או B)", exact: 0.58, params: { joint: [{ p: 0.12, A: 1, B: 1 }, { p: 0.18, A: 1, B: 0 }, { p: 0.28, A: 0, B: 1 }, { p: 0.42, A: 0, B: 0 }], event: "A == 1 or B == 1" } },
      recap: String.raw`בלתי תלויים: $P(A\cup B)=p+q-pq$.` },
    { id: "events-C08-Q3",
      question: String.raw`מטילים קובייה הוגנת אחת. $A$ = "זוגית", $B$ = "גדולה מ-3". איזה משפט נכון?`,
      options: [
        { id: "a", value: "הם תלויים, כי $P(A\\cap B)=\\frac13\\ne\\frac14=P(A)P(B)$" },
        { id: "b", value: "הם בלתי תלויים, כי $P(A\\cap B)=\\frac13$ ו-$P(A)P(B)=\\frac13$" },
        { id: "c", value: "הם זרים, כי יש בהם תוצאות שונות" },
        { id: "d", value: "הם בלתי תלויים, כי $A\\cap B\\ne\\varnothing$" }],
      correctId: "a",
      sim: { kind: "dice", estimate: "P(זוגי וגם גדול מ-3)", exact: 1 / 3, params: { n: 1, event: "d1 % 2 == 0 and d1 > 3" } },
      explanation: String.raw`$A\cap B=\{4,6\}$ ולכן $P(A\cap B)=\frac13$, אבל $P(A)P(B)=\frac12\cdot\frac12=\frac14$. הם לא זרים (4 ו-6 בשניהם) והם גם לא בלתי תלויים: החיתוך אינו שווה למכפלה. חיתוך לא ריק לבדו אינו מוכיח אי-תלות.`,
      recap: String.raw`בודקים $P(A\cap B)$ מול $P(A)P(B)$.` },
    { id: "events-C08-Q4",
      question: String.raw`מטילים קובייה הוגנת פעמיים. $A$ = "ההטלה הראשונה זוגית", $B$ = "ההטלה השנייה גדולה מ-3". מהי $P(A\cap B)$, ומה היחס בין המאורעות?`,
      options: [
        { id: "a", value: "$\\frac14$, והם בלתי תלויים" },
        { id: "b", value: "$\\frac14$, והם תלויים" },
        { id: "c", value: "$0$, והם זרים" },
        { id: "d", value: "$\\frac13$, והם בלתי תלויים" }],
      correctId: "a",
      sim: { kind: "dice", estimate: "P(ראשונה זוגית וגם שנייה > 3)", exact: 1 / 4, params: { n: 2, event: "d1 % 2 == 0 and d2 > 3" } },
      explanation: String.raw`ההטלות נפרדות, ולכן $P(A\cap B)=\frac12\cdot\frac12=\frac14=P(A)P(B)$: בלתי תלויים. הם לא זרים, כי שני המאורעות יכולים לקרות יחד (ראשונה $2$, שנייה $4$).`,
      recap: String.raw`הטלות נפרדות = בלתי תלויים.` },
    { id: "events-C08-Q5",
      step: { type: "findbug",
              prompt: String.raw`$P(A)=\frac12$, $P(B)=\frac13$, והמאורעות זרים. בנימוק הבא על אי-תלות **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`זרים פירושו $A\cap B=\varnothing$, ולכן $P(A\cap B)=0$.`,
                String.raw`אי-תלות פירושה $P(A\cap B)=P(A)P(B)=\frac16$.`,
                String.raw`מכיוון שהמאורעות זרים, הם בלתי תלויים.`,
              ],
              bugIndex: 2,
              explain: String.raw`$0\ne\frac16$, ולכן הם תלויים. זרים עם הסתברויות חיוביות אינם בלתי תלויים לעולם.` },
      recap: String.raw`זרים אינו בלתי תלויים.` },
    { id: "events-C08-Q6",
      step: { type: "numeric", answer: 0.5, tol: 0.001,
              prompt: String.raw`$P(A)=0.4$ ו-$P(A\cup B)=0.7$, והמאורעות בלתי תלויים. מהי $P(B)$ ?`,
              explain: String.raw`$0.4+q-0.4q=0.7$ ולכן $0.6q=0.3$ ו-$q=0.5$. בדיקה: $P(A\cap B)=0.2=0.4\cdot0.5$. התשובה $0.3$ מתקבלת אם מניחים זרים ($0.4+q=0.7$).` },
      sim: { kind: "custom_discrete", estimate: "P(B)", exact: 0.5, params: { joint: [{ p: 0.2, A: 1, B: 1 }, { p: 0.2, A: 1, B: 0 }, { p: 0.3, A: 0, B: 1 }, { p: 0.3, A: 0, B: 0 }], event: "B == 1" } },
      recap: String.raw`בלתי תלויים: $q=\dfrac{s-p}{1-p}$.` },
  ],
});
