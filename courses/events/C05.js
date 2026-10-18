/* events, level 5 - the multiplication rule, the chain rule and trees. */
COURSE_LEVEL("events", {
  id: "C05", order: 5, icon: "🌳", title: "כלל הכפל ועצי הסתברות",
  goal: "אחרי השלב הזה אפשר לחשב הסתברות של \"קרה זה ואחר כך זה\" בעזרת כלל הכפל, כלל השרשרת ועץ.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>מהגדרת ההסתברות המותנית $P(A/B)=\frac{P(A\cap B)}{P(B)}$ מקבלים בהעברת אגפים את <b>כלל הכפל</b>:</p>
    <div class="lesson-rule">🔑 $$P(A\cap B)=P(B)\cdot P(A/B)=P(A)\cdot P(B/A)$$ ל-$n$ שלבים (<b>כלל השרשרת</b>): $$P(A_1\cap A_2\cap A_3)=P(A_1)\,P(A_2/A_1)\,P(A_3/A_1\cap A_2)$$</div>
    <p><b>עץ הסתברות</b> מציג את זה בציור: כל ענף הוא שלב, על כל ענף כותבים את ההסתברות המותנית שלו, <b>כופלים לאורך המסלול</b>, ו<b>מחברים</b> מסלולים שונים של אותו מאורע.</p>
    <div class="lesson-ex"><b>דוגמה.</b> בכד 3 כדורים אדומים ו-5 שחורים. מוציאים שני כדורים בזה אחר זה, <b>בלי החזרה</b>. ההסתברות ששניהם אדומים: הראשון אדום בהסתברות $\frac38$. אחרי שהוצאנו אדום נשארו 7 כדורים, 2 מהם אדומים, ולכן $P(R_2/R_1)=\frac27$. $$P(R_1\cap R_2)=\frac38\cdot\frac27=\frac{3}{28}.$$</div>
    <div class="lesson-trap">⚠️ <b>בלי החזרה</b> הכדור השני תלוי בראשון: מכפילים ב-$P(R_2/R_1)=\frac27$ ולא ב-$P(R_2)=\frac38$. רק <b>עם החזרה</b> (הכד חוזר לקדמותו) ההסתברויות לא משתנות, ואז התשובה $\frac38\cdot\frac38=\frac9{64}$.</div>
    <p>כשהמסלול מורכב משני שלבים שונים, העץ מראה גם מה לא קרה: ענף "שחור" ואז ענף "אדום" הוא מסלול נפרד עם הכפל שלו.</p>` },
  questions: [
    { id: "events-C05-Q1",
      step: { type: "numeric", answer: 0.15, tol: 0.001,
              prompt: String.raw`$P(A)=0.6$ ו-$P(B/A)=0.25$. מהי $P(A\cap B)$ ?`,
              explain: String.raw`כלל הכפל: $P(A\cap B)=P(A)P(B/A)=0.6\cdot0.25=0.15$. התשובה $0.25$ היא ההסתברות המותנית בלבד.` },
      recap: String.raw`$P(A\cap B)=P(A)\,P(B/A)$.` },
    { id: "events-C05-Q2",
      step: { type: "numeric", answer: 0.1333, tol: 0.002,
              prompt: String.raw`בכד 4 כדורים אדומים ו-6 שחורים. מוציאים שני כדורים בזה אחר זה בלי החזרה. מהי ההסתברות ששניהם אדומים? (שבר או עשרוני)`,
              explain: String.raw`$\frac4{10}\cdot\frac39=\frac{12}{90}=\frac2{15}\approx0.133$. אחרי הוצאת אדום נשארו 9 כדורים, 3 מהם אדומים.` },
      sim: { kind: "urn", estimate: "P(שני האדומים)", exact: 2 / 15, params: { counts: { red: 4, black: 6 }, draws: 2, replace: false, event: "red_1 and red_2" } },
      recap: String.raw`בלי החזרה: המכנה והמונה של השלב השני יורדים באחד.` },
    { id: "events-C05-Q3",
      step: { type: "numeric", answer: 0.08333, tol: 0.002,
              prompt: String.raw`בכד 5 כדורים אדומים ו-5 שחורים. מוציאים שלושה כדורים בלי החזרה. מהי ההסתברות ששלושתם אדומים? (שבר או עשרוני)`,
              explain: String.raw`כלל השרשרת: $\frac5{10}\cdot\frac49\cdot\frac38=\frac{60}{720}=\frac1{12}\approx0.0833$.` },
      sim: { kind: "urn", estimate: "P(שלושה אדומים)", exact: 1 / 12, params: { counts: { red: 5, black: 5 }, draws: 3, replace: false, event: "red_1 and red_2 and red_3" } },
      recap: String.raw`שרשרת: מכפילים את ההסתברות המותנית של כל שלב.` },
    { id: "events-C05-Q4",
      question: String.raw`מכונה עובדת ביום הראשון בהסתברות $0.9$. אם עבדה ביום הראשון, היא עובדת ביום השני בהסתברות $0.8$. אם התקלקלה ביום הראשון, היא עובדת ביום השני בהסתברות $0.3$. מהי ההסתברות שעבדה ביום הראשון **ותקולה** ביום השני?`,
      options: [{ id: "a", value: "$0.18$" }, { id: "b", value: "$0.02$" }, { id: "c", value: "$0.2$" }, { id: "d", value: "$0.07$" }],
      correctId: "a",
      sim: { kind: "custom_discrete", estimate: "P(עבדה ואז תקולה)", exact: 0.18, params: { joint: [{ p: 0.72, D1: 1, D2: 1 }, { p: 0.18, D1: 1, D2: 0 }, { p: 0.03, D1: 0, D2: 1 }, { p: 0.07, D1: 0, D2: 0 }], event: "D1 == 1 and D2 == 0" } },
      explanation: String.raw`המסלול: עבדה ($0.9$) ואז תקולה, שהיא המשלים של "עבדה" בהינתן שעבדה: $1-0.8=0.2$. $0.9\cdot0.2=0.18$. התשובה $0.02$ מתקבלת מ-$0.1\cdot0.2$ (טעות בענף הראשון), ו-$0.07$ היא מסלול אחר: התקלקלה ואז תקולה, $0.1\cdot0.7$.`,
      recap: String.raw`על כל ענף ההסתברות המותנית שלו. ענפים של אותו צומת מסתכמים ל-1.` },
    { id: "events-C05-Q5",
      step: { type: "findbug",
              prompt: String.raw`בכד 4 כדורים אדומים ו-6 שחורים. מוציאים שני כדורים בלי החזרה. בפתרון הבא של "שניהם אדומים" **שורה אחת** שגויה. מצאו אותה.`,
              lines: [
                String.raw`$R_i$ = הכדור ה-$i$ אדום. $P(R_1)=\frac{4}{10}$.`,
                String.raw`אחרי שהוצא כדור אדום נשארו 9 כדורים, 3 מהם אדומים: $P(R_2/R_1)=\frac39$.`,
                String.raw`$P(R_1\cap R_2)=P(R_1)\cdot P(R_2)=\frac4{10}\cdot\frac4{10}=\frac4{25}$.`,
              ],
              bugIndex: 2,
              explain: String.raw`כלל הכפל משתמש בהסתברות המותנית: $P(R_1\cap R_2)=P(R_1)\,P(R_2/R_1)=\frac4{10}\cdot\frac39=\frac2{15}$. הכפלה ב-$P(R_2)$ היא הנחה של אי-תלות, שנכונה רק עם החזרה.` },
      recap: String.raw`בלי החזרה: מכפילים ב-$P(R_2/R_1)$, לא ב-$P(R_2)$.` },
    { id: "events-C05-Q6",
      step: { type: "numeric", answer: 0.12, tol: 0.001,
              prompt: String.raw`$P(A)=0.5$, $P(B/A)=0.6$ ו-$P(C/A\cap B)=0.4$. מהי $P(A\cap B\cap C)$ ?`,
              explain: String.raw`$0.5\cdot0.6\cdot0.4=0.12$. כל גורם מותנה בכל מה שקרה לפניו.` },
      recap: String.raw`$P(A\cap B\cap C)=P(A)\,P(B/A)\,P(C/A\cap B)$.` },
  ],
});
