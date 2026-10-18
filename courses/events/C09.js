/* events, level 9 - urns with and without replacement, conditional on a previous draw. */
COURSE_LEVEL("events", {
  id: "C09", order: 9, icon: "🏺", title: "כדים: עם החזרה, בלי החזרה ובהינתן משיכה קודמת",
  goal: "אחרי השלב הזה אפשר לחשב הסתברויות בכד עם ובלי החזרה, גם בהינתן משיכה קודמת, ולדעת מתי הכדור ה-$k$ אדום בהסתברות $\\frac DN$.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>בכד $D$ כדורים אדומים מתוך $N$. <b>עם החזרה</b> כל משיכה מתחילה מכד זהה, והמשיכות בלתי תלויות. <b>בלי החזרה</b> כל משיכה משנה את הכד.</p>
    <div class="lesson-rule">🔑 בלי החזרה, בהינתן שמשכו כבר אדום: $P(R_2/R_1)=\dfrac{D-1}{N-1}$. בהינתן ששחור: $P(R_2/B_1)=\dfrac{D}{N-1}$. עם החזרה: תמיד $\dfrac DN$.</div>
    <div class="lesson-ex"><b>דוגמה.</b> 3 אדומים ו-5 שחורים, שני כדורים אדומים. בלי החזרה: $\frac38\cdot\frac27=\frac3{28}$. עם החזרה: $\frac38\cdot\frac38=\frac9{64}$.</div>
    <h3>סימטריה: הכדור ה-$k$ בלי לדעת מה קדם</h3>
    <div class="lesson-rule">🔑 בלי החזרה, אם <b>לא ידוע</b> מה יצא לפני כן, אז $P(R_k)=\dfrac DN$ לכל $k$. כל כדור סביר באותה מידה להיות במקום ה-$k$.</div>
    <p>בדיקה למקרה $k=2$: $P(R_2)=\frac DN\cdot\frac{D-1}{N-1}+\frac{N-D}{N}\cdot\frac D{N-1}=\frac DN$.</p>
    <h3>התניה על כדור, והמשיכות שלא ידועות</h3>
    <p>בהינתן שהכדור השני אדום (והראשון לא ידוע): בין שאר $N-1$ הכדורים יש בדיוק $D-1$ אדומים, והכדור השלישי נמצא בכל אחד מהמקומות הנותרים באותה סבירות. לכן $$P(R_3/R_2)=\frac{D-1}{N-1}.$$ התנייה על כדור אחד משנה את הכד, אבל כדור שלא ידוע לא משנה כלום.</p>
    <div class="lesson-trap">⚠️ הסימטריה $P(R_2)=\frac DN$ נכונה רק כשלא יודעים מה יצא ראשון. בהינתן הכדור הראשון, החישוב משתנה. וההסתברות <b>המשותפת</b> של שני כדורים (כמו "שניהם אדומים") כן שונה בין עם ובלי החזרה.</div>` },
  questions: [
    { id: "events-C09-Q1",
      step: { type: "numeric", answer: 0.2857, tol: 0.002,
              prompt: String.raw`בכד 3 כדורים אדומים ו-5 שחורים. מוציאים שני כדורים בלי החזרה. ידוע שהכדור הראשון אדום. מהי ההסתברות שהשני אדום? (שבר או עשרוני)`,
              explain: String.raw`אחרי הוצאת אדום נשארו 7 כדורים, 2 מהם אדומים: $\frac27\approx0.286$. התשובה $\frac38$ היא ההסתברות עם החזרה.` },
      sim: { kind: "urn", estimate: "P(R2 | R1)", exact: 2 / 7, params: { counts: { red: 3, black: 5 }, draws: 2, replace: false, event: "red_2", given: "red_1" } },
      recap: String.raw`$P(R_2/R_1)=\frac{D-1}{N-1}$.` },
    { id: "events-C09-Q2",
      question: String.raw`בכד 3 כדורים אדומים ו-5 שחורים. מוציאים שני כדורים בלי החזרה. מהי ההסתברות ששניהם אדומים?`,
      options: [{ id: "a", value: String.raw`$\frac{3}{28}$` }, { id: "b", value: String.raw`$\frac{9}{64}$` }, { id: "c", value: String.raw`$\frac{3}{32}$` }, { id: "d", value: String.raw`$\frac{3}{8}$` }],
      correctId: "a",
      sim: { kind: "urn", estimate: "P(שניהם אדומים)", exact: 3 / 28, params: { counts: { red: 3, black: 5 }, draws: 2, replace: false, event: "red_1 and red_2" } },
      explanation: String.raw`$\frac38\cdot\frac27=\frac3{28}$. התשובה $\frac9{64}$ היא עם החזרה. $\frac3{32}$ מתקבלת מ-$\frac38\cdot\frac28$ (שוכחים שהכד קטן ב-1), ו-$\frac38$ היא הסתברות של כדור בודד.`,
      recap: String.raw`בלי החזרה: הכד קטן ב-1 והאדומים קטנים ב-1.` },
    { id: "events-C09-Q3",
      step: { type: "numeric", answer: 0.4, tol: 0.001,
              prompt: String.raw`בכד 4 כדורים אדומים ו-6 שחורים. מוציאים שלושה כדורים בלי החזרה. מהי ההסתברות שהכדור **השלישי** אדום (בלי לדעת מה יצא קודם)?`,
              explain: String.raw`בסימטריה, כל כדור סביר באותה מידה להיות שלישי: $\frac DN=\frac4{10}=0.4$. אפשר לאמת בפיצול לפי שני הכדורים הראשונים, והתוצאה זהה.` },
      sim: { kind: "urn", estimate: "P(R3)", exact: 0.4, params: { counts: { red: 4, black: 6 }, draws: 3, replace: false, event: "red_3" } },
      recap: String.raw`בלי לדעת מה קדם: $P(R_k)=\frac DN$.` },
    { id: "events-C09-Q4",
      step: { type: "numeric", answer: 0.3333, tol: 0.002,
              prompt: String.raw`בכד 4 כדורים אדומים ו-6 שחורים. מוציאים שלושה כדורים בלי החזרה. ידוע שהכדור **השני** אדום (הראשון לא ידוע). מהי ההסתברות שהשלישי אדום? (שבר או עשרוני)`,
              explain: String.raw`$P(R_3/R_2)=\frac{D-1}{N-1}=\frac39=\frac13$. בין 9 הכדורים האחרים יש 3 אדומים. אפשר לאמת: $P(R_2\cap R_3)=\frac4{10}\cdot\frac39=\frac2{15}$ ו-$P(R_2)=\frac25$, ולכן $\frac{2/15}{2/5}=\frac13$. התשובה $0.4$ מתעלמת מהמידע.` },
      sim: { kind: "urn", estimate: "P(R3 | R2)", exact: 1 / 3, params: { counts: { red: 4, black: 6 }, draws: 3, replace: false, event: "red_3", given: "red_2" } },
      recap: String.raw`$P(R_3/R_2)=\frac{D-1}{N-1}$.` },
    { id: "events-C09-Q5",
      step: { type: "findbug",
              prompt: String.raw`בכד 4 אדומים ו-6 שחורים מוציאים שלושה כדורים בלי החזרה. ידוע שהשני אדום. בפתרון הבא של "הכדור השלישי אדום" **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`הכדור השני כבר ידוע שהוא אדום, ולכן בין 9 הכדורים הנותרים יש בדיוק 3 אדומים.`,
                String.raw`הכדור השלישי נמצא באקראי באחד מ-9 המקומות הנותרים, ולכן $P(R_3/R_2)=\frac49$.`,
              ],
              bugIndex: 1,
              explain: String.raw`בין 9 הנותרים יש 3 אדומים (השורה הראשונה), ולכן $\frac39=\frac13$ ולא $\frac49$. הערך $\frac49$ שוכח שהאדום של המשיכה השנייה כבר יצא.` },
      recap: String.raw`אחרי שכדור אדום יצא, בכד נשארו $D-1$ אדומים.` },
    { bankId: "24B-B-Q2c", recap: String.raw`הכדור ה-$k$ אדום בהסתברות $\frac DN$.` },
  ],
});
