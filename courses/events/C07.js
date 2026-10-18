/* events, level 7 - Bayes: reversing the conditioning, and "can it be". */
COURSE_LEVEL("events", {
  id: "C07", order: 7, icon: "🔄", title: "בייס: הפיכת ההתניה",
  goal: "אחרי השלב הזה אפשר להפוך התניה: מ-$P(B/A)$ ל-$P(A/B)$, ולהכריע אם נתונים עם הסתברות מותנית אפשריים.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>נתון מה קורה בכל מקרה ($P(B/A)$), ושואלים לאחור: אם <b>ידוע ש-$B$ קרה</b>, מה ההסתברות שהיה המקרה $A$? זו <b>נוסחת בייס</b>:</p>
    <div class="lesson-rule">🔑 $$P(A/B)=\frac{P(B/A)\,P(A)}{P(B)}$$ והמכנה $P(B)$ מחשבים בהסתברות שלמה: $P(B)=P(B/A)P(A)+P(B/\overline{A})P(\overline{A})$.</div>
    <p>המונה הוא המסלול "$A$ ואז $B$", והמכנה הוא כל המסלולים שמסתיימים ב-$B$. הנוסחה היא פשוט $\frac{P(A\cap B)}{P(B)}$, כשהחיתוך מחושב בכלל הכפל.</p>
    <div class="lesson-ex"><b>דוגמה.</b> מכונה 1 מייצרת $60\%$ מהפריטים ($2\%$ פגומים), מכונה 2 מייצרת $40\%$ ($5\%$ פגומים). פריט נמצא פגום. מה ההסתברות שמכונה 2 ייצרה אותו? $P(D)=0.032$, והמסלול "מכונה 2 ופגום" הוא $0.4\cdot0.05=0.02$. לכן $P(M_2/D)=\frac{0.02}{0.032}=0.625$.</div>
    <div class="lesson-trap">⚠️ $P(A/B)$ ו-$P(B/A)$ הן שתי הסתברויות שונות. רוב הנבדקים עם תוצאה חיובית במבחן מדויק של 95% אינם חולים, אם המחלה נדירה: מי שנבדק חיובי הוא ברובו בריא, כי הבריאים רבים מאוד.</div>
    <h3>עם p, q, s</h3>
    <p>אם $P(A)=p$, $P(B)=q$ ו-$P(B/\overline{A})=s$, אז $P(B\cap\overline{A})=s(1-p)$ ולכן $$P(\overline{A}/B)=\frac{s(1-p)}{q}.$$</p>
    <h3>האם הנתונים אפשריים עם התניה?</h3>
    <p>נתון $P(A/B)=p$, $P(\overline{A}/\overline{B})=q$ ו-$P(A\cup B)=s$. הסיכוי ש"אף אחד לא קרה" הוא $P(\overline{A}\cap\overline{B})=1-s$, ו-$q=P(\overline{A}/\overline{B})=\frac{1-s}{P(\overline{B})}$. מכיוון ש-$P(\overline{B})\le1$, חייב להתקיים $q\ge1-s$. אם נתון $q<1-s$, הנתונים סותרים.</p>` },
  questions: [
    { id: "events-C07-Q1",
      step: { type: "numeric", answer: 0.161, tol: 0.002,
              prompt: String.raw`$1\%$ מהאוכלוסייה חולים. הבדיקה חיובית אצל $95\%$ מהחולים ואצל $5\%$ מהבריאים. אדם נבדק וקיבל תוצאה חיובית. מה ההסתברות שהוא חולה? (עשרוני)`,
              explain: String.raw`מסלול חולה וחיובי: $0.01\cdot0.95=0.0095$. מסלול בריא וחיובי: $0.99\cdot0.05=0.0495$. הסכום (המכנה) $0.059$. $\frac{0.0095}{0.059}\approx0.161$. התשובה $0.95$ היא ההסתברות לבדיקה חיובית אצל חולה, הכיוון ההפוך.` },
      sim: { kind: "custom_discrete", estimate: "P(חולה | חיובי)", exact: 0.0095 / 0.059, params: { joint: [{ p: 0.0095, S: 1, T: 1 }, { p: 0.0005, S: 1, T: 0 }, { p: 0.0495, S: 0, T: 1 }, { p: 0.9405, S: 0, T: 0 }], event: "S == 1", given: "T == 1" } },
      recap: String.raw`בייס: מסלול רצוי חלקי כל המסלולים שנגמרים בנתון.` },
    { id: "events-C07-Q2",
      step: { type: "numeric", answer: 0.625, tol: 0.002,
              prompt: String.raw`מכונה 1 מייצרת $60\%$ מהפריטים ו-$2\%$ מהם פגומים. מכונה 2 מייצרת $40\%$ ו-$5\%$ מהם פגומים. נמצא פריט פגום. מה ההסתברות שהוא ממכונה 2 ?`,
              explain: String.raw`$P(D)=0.6\cdot0.02+0.4\cdot0.05=0.032$. $P(M_2/D)=\frac{0.4\cdot0.05}{0.032}=\frac{0.02}{0.032}=0.625$. התשובה $0.05$ היא שיעור הפגומים במכונה 2, כלומר הכיוון ההפוך.` },
      sim: { kind: "custom_discrete", estimate: "P(מכונה 2 | פגום)", exact: 0.625, params: { joint: [{ p: 0.012, M: 1, D: 1 }, { p: 0.588, M: 1, D: 0 }, { p: 0.02, M: 2, D: 1 }, { p: 0.38, M: 2, D: 0 }], event: "M == 2", given: "D == 1" } },
      recap: String.raw`מונה: $P(D/M_2)P(M_2)$. מכנה: $P(D)$.` },
    { id: "events-C07-Q3",
      step: { type: "findbug",
              prompt: String.raw`אותה שאלה: מה ההסתברות שפריט פגום הגיע ממכונה 2 ? בפתרון הבא **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`$P(D)=0.6\cdot0.02+0.4\cdot0.05=0.032$.`,
                String.raw`$P(M_2\cap D)=P(M_2)\,P(D/M_2)=0.4\cdot0.05=0.02$.`,
                String.raw`$P(M_2/D)=\dfrac{P(M_2\cap D)}{P(M_2)}=\dfrac{0.02}{0.4}=0.05$.`,
              ],
              bugIndex: 2,
              explain: String.raw`המכנה הוא מה שידוע: הפריט פגום, ולכן $P(D)=0.032$. החלוקה ב-$P(M_2)$ נותנת $P(D/M_2)$, הכיוון ההפוך. הנכון: $\frac{0.02}{0.032}=0.625$.` },
      recap: String.raw`מה שאחרי הקו האלכסוני הוא המכנה.` },
    { id: "events-C07-Q4",
      step: { type: "numeric", answer: 0.56, tol: 0.001,
              prompt: String.raw`$P(A)=0.3$, $P(B)=0.5$ ו-$P(B/\overline{A})=0.4$. מהי $P(\overline{A}/B)$ ?`,
              explain: String.raw`$P(B\cap\overline{A})=0.4\cdot0.7=0.28$ ולכן $P(\overline{A}/B)=\frac{0.28}{0.5}=0.56$. התשובה $0.4$ היא הנתון עצמו, בכיוון ההפוך.` },
      sim: { kind: "custom_discrete", estimate: "P(לא A | B)", exact: 0.56, params: { joint: [{ p: 0.22, A: 1, B: 1 }, { p: 0.08, A: 1, B: 0 }, { p: 0.28, A: 0, B: 1 }, { p: 0.42, A: 0, B: 0 }], event: "A == 0", given: "B == 1" } },
      recap: String.raw`$P(\overline{A}/B)=\dfrac{s(1-p)}{q}$.` },
    { id: "events-C07-Q5",
      question: String.raw`נתון $P(A/B)=p$, $P(\overline{A}/\overline{B})=q$ ו-$P(A\cup B)=0.9$. איזה ערך של $q$ **אינו** אפשרי?`,
      options: [{ id: "a", value: "$0.05$" }, { id: "b", value: "$0.2$" }, { id: "c", value: "$0.5$" }, { id: "d", value: "$0.9$" }],
      correctId: "a",
      explanation: String.raw`$P(\overline{A}\cap\overline{B})=1-0.9=0.1$ ו-$q=\frac{0.1}{P(\overline{B})}\ge0.1$ כי $P(\overline{B})\le1$. לכן $q=0.05$ בלתי אפשרי: היה נדרש $P(\overline{B})=2$. הערכים $0.2,0.5,0.9$ נותנים $P(\overline{B})=0.5,0.2,\frac19$, כולם תקינים.`,
      recap: String.raw`$q\ge1-s$, כי $P(\overline{B})\le1$.` },
    { bankId: "25A-C-Q2b", recap: String.raw`$P(B/\overline{A})=\dfrac{s-p}{1-p}$.` },
  ],
});
