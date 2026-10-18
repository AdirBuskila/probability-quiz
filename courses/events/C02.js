/* events, level 2 - the basic rules: complement, inclusion-exclusion, difference, exactly one, counting multiples. */
COURSE_LEVEL("events", {
  id: "C02", order: 2, icon: "➕", title: "משלים, הכלה והפרדה",
  goal: "אחרי השלב הזה אפשר לחשב הסתברות של איחוד, של משלים, של הפרש ושל \"בדיוק אחד\", וגם לספור מכפלות של מספר בטווח.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>לא תמיד ספירת תוצאות היא הדרך הקלה. את הסתברות של מאורע מורכב מחשבים מהסתברויות של חלקיו, בעזרת כמה כללים.</p>
    <div class="lesson-rule">🔑 <b>משלים:</b> $P(\overline{A})=1-P(A)$.<br><b>איחוד (הכלה והפרדה):</b> $P(A\cup B)=P(A)+P(B)-P(A\cap B)$.</div>
    <p>למה מחסירים את החיתוך? כי כשמחברים $P(A)+P(B)$ התוצאות של $A\cap B$ נספרות פעמיים, פעם בכל מאורע.</p>
    <h3>עוד שלושה כללים שמשתמשים בהם כל הזמן</h3>
    <ul>
      <li><b>הפרש:</b> $P(A\setminus B)=P(A)-P(A\cap B)$ (מורידים מ-$A$ את החלק שגם ב-$B$).</li>
      <li><b>אף אחד:</b> $P(\overline{A}\cap\overline{B})=1-P(A\cup B)$.</li>
      <li><b>בדיוק אחד:</b> $P(A)+P(B)-2P(A\cap B)$. כאן מחסירים את החיתוך <b>פעמיים</b>, כי החיתוך אינו חלק מ"בדיוק אחד" בכלל. (ל"לפחות אחד" מחסירים פעם אחת.)</li>
    </ul>
    <div class="lesson-ex"><b>דוגמה.</b> $P(A)=0.5$, $P(B)=0.3$, $P(A\cap B)=0.1$. אז $P(A\cup B)=0.5+0.3-0.1=0.7$, ההסתברות ש"אף אחד לא קרה" היא $1-0.7=0.3$, $P(A\setminus B)=0.5-0.1=0.4$, ו"בדיוק אחד" הוא $0.5+0.3-2\cdot0.1=0.6$.</div>
    <h3>שלושה מאורעות</h3>
    <p>$P(A\cup B\cup C)=P(A)+P(B)+P(C)-P(A\cap B)-P(A\cap C)-P(B\cap C)+P(A\cap B\cap C)$. מחברים, מחסירים זוגות, ומוסיפים בחזרה את השלישייה.</p>
    <h3>ספירת מכפלות של $k$ בטווח</h3>
    <p>כמה מספרים בין $a$ ל-$b$ (כולל) מתחלקים ב-$k$ ללא שארית? $\left\lfloor\frac{b}{k}\right\rfloor-\left\lfloor\frac{a-1}{k}\right\rfloor$. בוחרים באקראי מספר תלת-ספרתי: $\Omega=\{100,\dots,999\}$ ו-$|\Omega|=900$.</p>
    <div class="lesson-ex"><b>דוגמה.</b> $A_2$ = "מתחלק ב-2": $|A_2|=\lfloor 999/2\rfloor-\lfloor 99/2\rfloor=499-49=450$. $A_4$ = "מתחלק ב-4": $|A_4|=249-24=225$. כל מכפלה של 4 היא גם מכפלה של 2, ולכן $A_4\subseteq A_2$ ו-$A_2\cap A_4=A_4$.</div>
    <div class="lesson-trap">⚠️ $|A_8|=112$ ולא $\frac{900}{8}=112.5$. ההסתברות אינה $\frac18$, כי הטווח לא מתחיל ב-$0$. תמיד משתמשים בנוסחת הספירה.</div>` },
  questions: [
    { id: "events-C02-Q1",
      step: { type: "numeric", answer: 0.7, tol: 0.001,
              prompt: String.raw`$P(A)=0.5$, $P(B)=0.3$ ו-$P(A\cap B)=0.1$. מהי $P(A\cup B)$ ?`,
              explain: String.raw`$0.5+0.3-0.1=0.7$. התשובה $0.8$ היא סכום ההסתברויות בלי להוריד את החיתוך.` },
      sim: { kind: "custom_discrete", estimate: "P(A או B)", exact: 0.7, params: { joint: [{ p: 0.1, A: 1, B: 1 }, { p: 0.4, A: 1, B: 0 }, { p: 0.2, A: 0, B: 1 }, { p: 0.3, A: 0, B: 0 }], event: "A == 1 or B == 1" } },
      recap: String.raw`$P(A\cup B)=P(A)+P(B)-P(A\cap B)$.` },
    { id: "events-C02-Q2",
      step: { type: "numeric", answer: 0.4, tol: 0.001,
              prompt: String.raw`$P(A)=0.5$, $P(B)=0.3$ ו-$P(A\cap B)=0.1$. מהי ההסתברות של "$A$ אבל לא $B$", כלומר $P(A\setminus B)$ ?`,
              explain: String.raw`מ-$A$ מורידים את החלק שגם ב-$B$: $0.5-0.1=0.4$. התשובה $0.5$ היא $P(A)$ כולו, וכוללת גם את מה שב-$B$.` },
      recap: String.raw`$P(A\setminus B)=P(A)-P(A\cap B)$.` },
    { id: "events-C02-Q3",
      step: { type: "numeric", answer: 0.7, tol: 0.001,
              prompt: String.raw`$P(A)=0.5$ ו-$P(B)=0.4$ ו-$P(A\cap B)=0.1$. מהי ההסתברות שקרה **בדיוק אחד** משני המאורעות?`,
              explain: String.raw`בדיוק אחד: $0.5+0.4-2\cdot0.1=0.7$. התשובה $0.8$ היא "לפחות אחד" ($0.5+0.4-0.1$), והיא כוללת גם את מקרה "שניהם".` },
      sim: { kind: "custom_discrete", estimate: "P(בדיוק אחד)", exact: 0.7, params: { joint: [{ p: 0.1, A: 1, B: 1 }, { p: 0.4, A: 1, B: 0 }, { p: 0.3, A: 0, B: 1 }, { p: 0.2, A: 0, B: 0 }], event: "A + B == 1" } },
      recap: String.raw`בדיוק אחד: מורידים את החיתוך פעמיים.` },
    { id: "events-C02-Q4",
      step: { type: "numeric", answer: 128, tol: 0,
              prompt: String.raw`כמה מספרים תלת-ספריים (מ-100 עד 999) מתחלקים ב-7 ללא שארית?`,
              explain: String.raw`$\lfloor 999/7\rfloor-\lfloor 99/7\rfloor=142-14=128$. התשובה 129 מתקבלת אם מעגלים למעלה את $\frac{900}{7}\approx128.6$, וזה לא נכון: מה שקובע הוא איפה הטווח מתחיל ואיפה הוא נגמר.` },
      recap: String.raw`$\lfloor b/k\rfloor-\lfloor (a-1)/k\rfloor$.` },
    { id: "events-C02-Q5",
      question: String.raw`בוחרים באקראי מספר תלת-ספרתי (מ-100 עד 999). מהי ההסתברות שהוא מתחלק ב-2 **או** ב-5 ?`,
      options: [{ id: "a", value: String.raw`$\frac{3}{5}$` }, { id: "b", value: String.raw`$\frac{7}{10}$` }, { id: "c", value: String.raw`$\frac{1}{2}$` }, { id: "d", value: String.raw`$\frac{2}{5}$` }],
      correctId: "a",
      sim: { kind: "urn", estimate: "P(מתחלק ב-2 או ב-5)", exact: 3 / 5, params: { values: Array.from({ length: 900 }, (_, i) => 100 + i), draws: 1, replace: false, event: "v1 % 2 == 0 or v1 % 5 == 0" } },
      explanation: String.raw`$|A_2|=450$, $|A_5|=\lfloor 999/5\rfloor-\lfloor 99/5\rfloor=199-19=180$. מתחלק גם ב-2 וגם ב-5 אם ורק אם מתחלק ב-10: $|A_{10}|=99-9=90$. לכן $|A_2\cup A_5|=450+180-90=540$ ו-$P=\frac{540}{900}=\frac35$. התשובה $\frac7{10}$ היא $\frac{450+180}{900}$ בלי להוריד את החיתוך.`,
      recap: String.raw`מתחלק ב-2 וגם ב-5 = מתחלק ב-10. מחסירים את החיתוך.` },
    { id: "events-C02-Q6",
      step: { type: "findbug",
              prompt: String.raw`בכיתה 60% לומדים מתמטיקה ($M$), 50% לומדים פיזיקה ($F$), ו-30% לומדים את שניהם. הפתרון הבא של "איזה חלק מהכיתה לא לומד אף אחד מהם" כולל **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`$P(M)=0.6$, $P(F)=0.5$, $P(M\cap F)=0.3$.`,
                String.raw`"לפחות אחד" הוא האיחוד, ו"אף אחד" הוא המשלים שלו.`,
                String.raw`$P(M\cup F)=0.6+0.5-2\cdot0.3=0.5$.`,
                String.raw`לכן ההסתברות ש"אף אחד לא לומד" היא $1-P(M\cup F)=0.2$.`,
              ],
              bugIndex: 2,
              explain: String.raw`לאיחוד מחסירים את החיתוך פעם אחת: $0.6+0.5-0.3=0.8$. ההסרה הכפולה היא של "בדיוק אחד". עם $0.8$ מתקבל אכן $1-0.8=0.2$ בשורה האחרונה.` },
      recap: String.raw`איחוד: חיתוך פעם אחת. בדיוק אחד: פעמיים.` },
  ],
});
