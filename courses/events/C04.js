/* events, level 4 - conditional probability and the right denominator. */
COURSE_LEVEL("events", {
  id: "C04", order: 4, icon: "🎯", title: "הסתברות מותנית: המכנה הנכון",
  goal: "אחרי השלב הזה אפשר לחשב $P(A/B)$ נכון: המונה הוא החיתוך, והמכנה הוא מה שידוע.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>"<b>אם ידוע ש-$B$</b>, מה ההסתברות ל-$A$?" פירושו: מצמצמים את העולם לתוצאות של $B$ בלבד, ושואלים איזה חלק מהן מקיים גם את $A$.</p>
    <div class="lesson-rule">🔑 $$P(A/B)=\frac{P(A\cap B)}{P(B)}$$ <b>מונה:</b> שני התנאים יחד. <b>מכנה:</b> מה שידוע. בתוצאות שוות הסתברות: $\dfrac{|A\cap B|}{|B|}$.</div>
    <div class="lesson-ex"><b>דוגמה.</b> מטילים שתי קוביות הוגנות. ידוע שהסכום הוא $5$. מה ההסתברות שהקובייה הראשונה גדולה מ-$3$? הזוגות עם סכום $5$: $(1,4),(2,3),(3,2),(4,1)$, כלומר $|B|=4$. מהם רק $(4,1)$ מקיים "ראשונה גדולה מ-3". לכן $P=\frac14$.</div>
    <div class="lesson-trap">⚠️ הטעות הנפוצה ביותר: לחלק ב-$|\Omega|=36$ במקום ב-$|B|$. "אם ידוע" מחליף את מרחב המדגם ב-$B$. כאן $\frac1{36}$ היה שגוי, והנכון $\frac{1/36}{4/36}=\frac14$.</div>
    <div class="lesson-trap">⚠️ הכיוון חשוב: $P(A/B)$ מחלק ב-$P(B)$, אבל $P(B/A)$ מחלק ב-$P(A)$. הגורם שאחרי הקו האלכסוני הוא תמיד המכנה.</div>
    <h3>עם הנתונים p, q, s</h3>
    <p>אם $P(A)=p$, $P(B)=q$, $P(A\cup B)=s$, אז $P(A\cap B)=p+q-s$ ולכן $P(A/B)=\dfrac{p+q-s}{q}$ ו-$P(B/A)=\dfrac{p+q-s}{p}$.</p>
    <p>אפשר גם להתנות במשלים: $P(A/\overline{B})=\dfrac{P(A\setminus B)}{P(\overline{B})}=\dfrac{s-q}{1-q}$.</p>` },
  questions: [
    { id: "events-C04-Q1",
      step: { type: "numeric", answer: 0.6, tol: 0.001,
              prompt: String.raw`מטילים שתי קוביות הוגנות. ידוע שהסכום הוא $8$. מהי ההסתברות שהקובייה הראשונה זוגית? (שבר או עשרוני)`,
              explain: String.raw`הזוגות עם סכום $8$: $(2,6),(3,5),(4,4),(5,3),(6,2)$, כלומר 5 תוצאות. בשלושה מהם הראשונה זוגית: $(2,6),(4,4),(6,2)$. לכן $\frac35=0.6$. התשובה $\frac{3}{36}$ מחלקת ב-$|\Omega|$.` },
      sim: { kind: "dice", estimate: "P(d1 זוגי | סכום 8)", exact: 3 / 5, params: { n: 2, event: "d1 % 2 == 0", given: "sum == 8" } },
      recap: String.raw`מכנה: מספר התוצאות שמקיימות את מה שידוע.` },
    { id: "events-C04-Q2",
      question: String.raw`מטילים שתי קוביות הוגנות. ידוע שלפחות בקובייה אחת יצא $6$. מהי ההסתברות שהסכום לפחות $10$?`,
      options: [{ id: "a", value: String.raw`$\frac{5}{11}$` }, { id: "b", value: String.raw`$\frac{5}{36}$` }, { id: "c", value: String.raw`$\frac{1}{6}$` }, { id: "d", value: String.raw`$\frac{5}{6}$` }],
      correctId: "a",
      sim: { kind: "dice", estimate: "P(סכום ≥ 10 | יש 6)", exact: 5 / 11, params: { n: 2, event: "sum >= 10", given: "max == 6" } },
      explanation: String.raw`המכנה: הזוגות שבהם לפחות קובייה אחת היא $6$: $11$ זוגות. מהם עם סכום $\ge10$: $(4,6),(6,4),(5,6),(6,5),(6,6)$, חמישה. לכן $\frac5{11}$. התשובה $\frac5{36}$ היא החיתוך חלקי $|\Omega|$ (שוכחים לחלק במה שידוע).`,
      recap: String.raw`לפני שמחלקים: ספרו את התוצאות של התנאי.` },
    { id: "events-C04-Q3",
      step: { type: "findbug",
              prompt: String.raw`מטילים שתי קוביות הוגנות. ידוע שהסכום הוא $6$. מה ההסתברות ששתי התוצאות שונות? בפתרון הבא **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`$B$ = הסכום $6$: $(1,5),(2,4),(3,3),(4,2),(5,1)$, כלומר $|B|=5$.`,
                String.raw`$A\cap B$ = סכום $6$ והתוצאות שונות: הכול חוץ מ-$(3,3)$, כלומר $|A\cap B|=4$.`,
                String.raw`$P(A/B)=\dfrac{|A\cap B|}{|\Omega|}=\dfrac{4}{36}=\dfrac19$.`,
              ],
              bugIndex: 2,
              explain: String.raw`המכנה הוא $|B|=5$, מה שידוע, ולא $|\Omega|=36$. התשובה הנכונה $\frac45$. שימו לב שבהינתן $B$ יש רק 5 תוצאות אפשריות, ולכן $\frac19$ קטנה מדי.` },
      recap: String.raw`המכנה הוא $|B|$, לא $|\Omega|$.` },
    { id: "events-C04-Q4",
      step: { type: "numeric", answer: 0.4, tol: 0.001,
              prompt: String.raw`$P(A)=0.5$, $P(B)=0.4$ ו-$P(A\cup B)=0.7$. מהי $P(B/A)$ ?`,
              explain: String.raw`החיתוך $0.5+0.4-0.7=0.2$. המכנה הוא מה שידוע, כלומר $P(A)=0.5$: $\frac{0.2}{0.5}=0.4$. התשובה $0.5$ מתקבלת מחלוקה ב-$P(B)$, וזה $P(A/B)$.` },
      sim: { kind: "custom_discrete", estimate: "P(B | A)", exact: 0.4, params: { joint: [{ p: 0.2, A: 1, B: 1 }, { p: 0.3, A: 1, B: 0 }, { p: 0.2, A: 0, B: 1 }, { p: 0.3, A: 0, B: 0 }], event: "B == 1", given: "A == 1" } },
      recap: String.raw`$P(B/A)$: מחלקים ב-$P(A)$.` },
    { id: "events-C04-Q5",
      question: String.raw`בכיתה, $M$ = "עבר מתמטיקה" ו-$F$ = "עבר פיזיקה". איזה ביטוי הוא ההסתברות ש"מבין אלה שעברו מתמטיקה, מי שלא עבר פיזיקה"?`,
      options: [{ id: "a", value: String.raw`$P(\overline{F}/M)$` }, { id: "b", value: String.raw`$P(M/\overline{F})$` }, { id: "c", value: String.raw`$P(\overline{F}\cap M)$` }, { id: "d", value: String.raw`$P(\overline{M}/F)$` }],
      correctId: "a",
      explanation: String.raw`"מבין אלה שעברו מתמטיקה" הוא התנאי, אחרי הקו האלכסוני: $M$. המבוקש הוא "לא עבר פיזיקה": $\overline{F}$. לכן $P(\overline{F}/M)$. $P(\overline{F}\cap M)$ היא ההסתברות המשותפת בלי חלוקה, ו-$P(M/\overline{F})$ הפוכה.`,
      recap: String.raw`"מבין ..." או "אם ידוע ..." הוא מה שאחרי הקו האלכסוני.` },
    { bankId: "25A-C-Q2a", recap: String.raw`$P(A/B)=\dfrac{p+q-s}{q}$.` },
  ],
});
