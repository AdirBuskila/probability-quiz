/* events, level 10 - boss: real exam questions on events, conditional probability, Bayes and independence. */
COURSE_LEVEL("events", {
  id: "C10", order: 10, icon: "🏆", title: "בוס: שאלות מבחן אמיתיות",
  goal: "אחרי השלב הזה אפשר לפתור סעיפים אמיתיים ממבחנים בנושא מאורעות, הסתברות מותנית, בייס ואי-תלות.",
  boss: true,
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>ששת הסעיפים הבאים לקוחים ממבחנים אמיתיים. לפני כל אחד, רשימת בדיקה קצרה:</p>
    <ul>
      <li>מהו $\Omega$, ומהו המאורע המבוקש?</li>
      <li>בשאלת "אם ידוע ש...": מהו המכנה? זה מה שידוע, לא $|\Omega|$.</li>
      <li>נתונים $p,q,s$: בנו קודם את ארבעת התאים, ואחר כך ענו.</li>
      <li>בכדים בלי החזרה: איך משתנה הכד אחרי כל משיכה, ומה ידוע על המשיכות הקודמות?</li>
    </ul>
    <div class="lesson-rule">🔑 זרים: $P(A\cap B)=0$. בלתי תלויים: $P(A\cap B)=P(A)P(B)$. מותנה: חיתוך חלקי מה שידוע. בייס: הפיכת הכיוון עם הסתברות שלמה במכנה.</div>` },
  questions: [
    { bankId: "24A-B-Q2b", recap: String.raw`מותנה בקוביות: ספרו את התנאי, ואז את החיתוך.` },
    { bankId: "25A-A-Q2d", recap: String.raw`הכלה בין מאורעות של מכפלות: $A_4\subseteq A_2$.` },
    { bankId: "25A-B-Q2a", recap: String.raw`בייס עם $p,q,s$: $P(\overline{A}/B)=\frac{s(1-p)}{q}$.` },
    { bankId: "25A-B-Q2e", recap: String.raw`אי-תלות: $P(A\cap B)=pq$ נותן $q=s$.` },
    { bankId: "25B-A-Q2d", recap: String.raw`"האם ייתכן": מוצאים הסתברות שהייתה יוצאת שלילית.` },
    { bankId: "24B-B-Q2d", recap: String.raw`כדים: $P(R_3/R_2)=\frac{D-1}{N-1}$.` },
  ],
});
