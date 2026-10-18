/* joint, level 7 - the joint pmf of (min, max) of discrete picks. */
COURSE_LEVEL("joint", {
  id: "C07", order: 7, icon: "↔️", title: "מינימום ומקסימום של בחירות בדידות",
  goal: "אחרי השלב הזה אפשר למצוא את ההסתברות המשותפת של $(\\min,\\max)$ כשבוחרים שני מספרים או יותר, עם החזרה וללא החזרה.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>בוחרים מספרים באקראי, ומסמנים $M_1=\min$ ו-$M_2=\max$ של הבחירות. הזוג $(M_1,M_2)$ הוא משתנה דו-ממדי, ותמיד $M_1\le M_2$. לכן כל תא "מתחת לאלכסון" ($m_1>m_2$) הוא $0$.</p>
    <h3>שני מספרים</h3>
    <div class="lesson-rule">🔑 כשיש $N^2$ זוגות מסודרים שווי הסתברות (בחירה <b>עם החזרה</b>):
    $$P(\min=j,\ \max=k)=\begin{cases}\dfrac{2}{N^2},&j<k,\\[2mm] \dfrac1{N^2},&j=k,\\[1mm] 0,&j>k.\end{cases}$$
    הגורם $2$ מופיע כי הזוג הלא סדור $\{j,k\}$ מתקבל בשני סדרים: $(j,k)$ ו-$(k,j)$. כשהם שווים יש סדר אחד בלבד.</div>
    <div class="lesson-rule">🔑 <b>ללא החזרה</b> אי אפשר לקבל את אותו מספר פעמיים, ולכן $j=k$ בלתי אפשרי, ויש $N(N-1)$ זוגות מסודרים: $$P(\min=j,\ \max=k)=\frac{2}{N(N-1)},\qquad j<k.$$ יש $\binom N2$ תאים חיוביים, וסכומם $\binom N2\cdot\frac2{N(N-1)}=1$.</div>
    <div class="lesson-ex"><b>דוגמה.</b> קובייה הוגנת מוטלת פעמיים, $N=6$ עם החזרה. $P(\min=2,\max=5)$: הזוגות המסודרים $(2,5)$ ו-$(5,2)$, כלומר $\frac2{36}=\frac1{18}$.</div>
    <h3>יותר משני מספרים</h3>
    <div class="lesson-rule">🔑 בוחרים $n$ מספרים <b>שונים</b> מתוך $\{1,\dots,N\}$, ללא החזרה ובלי חשיבות לסדר (כל קבוצה בגודל $n$ שווה הסתברות). אז $$P(\min=k,\ \max=\ell)=\frac{\binom{\ell-k-1}{n-2}}{\binom Nn},\qquad k<\ell.$$ במונה סופרים את הקבוצות שבהן $k$ ו-$\ell$ נבחרו ואת שאר $n-2$ המספרים נבחרו <b>ממש בין</b> $k$ ל-$\ell$, ויש $\ell-k-1$ מספרים כאלה.</div>
    <div class="lesson-ex"><b>דוגמה.</b> $N=5$ ללא החזרה, $n=2$: כל תא עם $j<k$ שווה $\frac2{20}=\frac1{10}$, ויש $10$ תאים. בדיקה: הסכום $1$.</div>
    <div class="lesson-trap">⚠️ שתי טעויות: לשכוח את הגורם $2$ של שני הסדרים, ולתת הסתברות חיובית לתא עם $\min>\max$ או (ללא החזרה) לתא על האלכסון.</div>` },
  questions: [
    { id: "joint-C07-Q1",
      step: { type: "numeric", answer: 0.055556, tol: 0.001,
              prompt: String.raw`מטילים קובייה הוגנת פעמיים. $M_1$ הוא המינימום ו-$M_2$ המקסימום של שתי התוצאות. מהו $P(M_1=2,\ M_2=5)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`שני הסדרים $(2,5)$ ו-$(5,2)$ מתוך $36$ תוצאות, לכן $\frac2{36}=\frac1{18}\approx0.0556$. הערך $\frac1{36}$ הוא התעלמות מהגורם $2$.` },
      sim: { kind: "dice", estimate: "P(min=2, max=5)", exact: 1 / 18, params: { n: 2, event: "min == 2 and max == 5" } },
      recap: "כש-$j<k$ יש שני סדרים, ולכן $\\frac2{N^2}$." },
    { id: "joint-C07-Q2",
      step: { type: "numeric", answer: 0.027778, tol: 0.001,
              prompt: String.raw`מטילים קובייה הוגנת פעמיים. מהו $P(M_1=3,\ M_2=3)$, כלומר ששתי התוצאות שוות $3$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`רק התוצאה $(3,3)$, לכן $\frac1{36}\approx0.0278$. כשהמינימום והמקסימום שווים יש סדר אחד בלבד, ולכן אין גורם $2$.` },
      sim: { kind: "dice", estimate: "P(min=max=3)", exact: 1 / 36, params: { n: 2, event: "min == 3 and max == 3" } },
      recap: "על האלכסון $j=k$ יש סדר אחד: $\\frac1{N^2}$." },
    { id: "joint-C07-Q3",
      step: { type: "numeric", answer: 0.066667, tol: 0.001,
              prompt: String.raw`בוחרים שני מספרים שונים באקראי, ללא החזרה, מתוך $\{1,2,3,4,5,6\}$. מהו $P(M_1=2,\ M_2=5)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`ללא החזרה יש $6\cdot5=30$ זוגות מסודרים. שני מהם מתאימים: $(2,5)$ ו-$(5,2)$. לכן $\frac2{30}=\frac1{15}\approx0.0667$.` },
      sim: { kind: "urn", estimate: "P(min=2, max=5)", exact: 1 / 15, params: { values: [1, 2, 3, 4, 5, 6], draws: 2, event: "min == 2 and max == 5" } },
      recap: "ללא החזרה: $\\frac2{N(N-1)}$ לכל $j<k$." },
    { id: "joint-C07-Q4",
      step: { type: "numeric", answer: 15, tol: 0,
              prompt: String.raw`בוחרים שני מספרים שונים, ללא החזרה, מתוך $\{1,\dots,6\}$. בכמה תאים $(j,k)$ של טבלת $(M_1,M_2)$ ההסתברות חיובית?`,
              explain: String.raw`רק תאים עם $j<k$, כלומר בחירת שני מספרים שונים מתוך $6$ בלי סדר: $\binom62=15$. ואכן $15\cdot\frac1{15}=1$.` },
      recap: "התאים החיוביים הם אלה עם $j<k$: יש $\\binom N2$ כאלה." },
    { id: "joint-C07-Q5",
      step: { type: "numeric", answer: 0.033333, tol: 0.001,
              prompt: String.raw`בוחרים שלושה מספרים שונים באקראי, ללא החזרה, מתוך $\{1,\dots,10\}$. מהו $P(M_1=2,\ M_2=7)$ ? (אפשר שבר או עשרוני)`,
              explain: String.raw`$n=3$, $N=10$, $k=2$, $\ell=7$. המספר השלישי חייב להיות ממש בין $2$ ל-$7$: ארבע אפשרויות ($3,4,5,6$), כלומר $\binom{4}{1}=4$. הסך הכול $\binom{10}{3}=120$. לכן $\frac4{120}=\frac1{30}\approx0.0333$.` },
      sim: { kind: "urn", estimate: "P(min=2, max=7)", exact: 1 / 30, params: { values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], draws: 3, event: "min == 2 and max == 7" } },
      recap: "$\\frac{\\binom{\\ell-k-1}{n-2}}{\\binom Nn}$: שאר המספרים ממש בין המינימום למקסימום." },
    { id: "joint-C07-Q6",
      step: { type: "numeric", answer: 0.277778, tol: 0.001,
              prompt: String.raw`מטילים קובייה הוגנת פעמיים. מהי ההסתברות ש-$M_2-M_1=1$, כלומר שהתוצאות עוקבות? (אפשר שבר או עשרוני)`,
              explain: String.raw`התאים $(j,j+1)$ לכל $j=1,\dots,5$: חמישה תאים, וכל אחד $\frac2{36}$. הסכום $\frac{10}{36}=\frac5{18}\approx0.2778$.` },
      sim: { kind: "dice", estimate: "P(max - min = 1)", exact: 5 / 18, params: { n: 2, event: "max - min == 1" } },
      recap: "מסכמים את התאים שמקיימים את התנאי." },
  ],
});
