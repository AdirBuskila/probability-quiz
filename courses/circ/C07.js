/* Circuits course, level 7 - take a circuit apart and rebuild a new one from the same units */
const U = (id, p) => ({ type: "comp", id, p });
const SER = (...k) => ({ type: "series", children: k });
const PAR = (...k) => ({ type: "parallel", children: k });
const sim = (estimate, exact, params) => ({ kind: "circuit", estimate, exact, params });
COURSE_LEVEL("circ", {
  id: "C07", order: 7, icon: "🔧", title: "פירקו והרכיבו מעגל חדש",
  goal: "לחשב חיתוך, איחוד והסתברות מותנית בין שני מעגלים שנבנו מאותן יחידות.",
  source: "ai-verified",
  lesson: { figs: [{ src: "images/courses/circ/r_pair.svg", alt: "Q1: A בטור עם B. Q2: A במקביל ל-B", caption: "אותן שתי יחידות, בשני חיבורים: Q1 בטור ו-Q2 במקביל" }], html: String.raw`
    <p>בשאלות "פירקו והרכיבו" יש שני מעגלים, $Q_1$ ו-$Q_2$, שבנויים מ<b>אותן יחידות</b>. הם <b>תלויים</b>: אם $A$ תקולה היא תקולה בשניהם. לכן אסור לכתוב $P(Q_1\cap Q_2)=P(Q_1)P(Q_2)$.</p>
    <div class="lesson-rule">🔑 מהלך הפתרון: (1) כותבים כל מעגל כמאורע ביחידות, למשל $Q_1=A\cap(B\cup C)$. (2) את $P(Q_1\cap Q_2)$ מוצאים על ידי בדיקה באילו מצבי יחידות <b>שניהם</b> פועלים (בדרך כלל התניה על היחידות המשותפות). (3) מחשבים לפי הנוסחאות:</div>
    <div class="lesson-formula">$P(Q_1\mid Q_2)=\dfrac{P(Q_1\cap Q_2)}{P(Q_2)}$</div>
    <div class="lesson-formula">$P(Q_1\cup Q_2)=P(Q_1)+P(Q_2)-P(Q_1\cap Q_2)$</div>
    <p><b>מקרה מיוחד, מעגל מוכל במעגל:</b> אם בכל מצב שבו $Q_1$ פועל גם $Q_2$ פועל ($Q_1\subseteq Q_2$), אז $P(Q_1\cap Q_2)=P(Q_1)$, $P(Q_2\mid Q_1)=1$ ו-$P(Q_1\cup Q_2)=P(Q_2)$.</p>
    <div class="lesson-ex">דוגמה (באיור, $p=0.6$): $Q_1$ בטור מוכל ב-$Q_2$ שבמקביל. $P(Q_1)=0.36$ ו-$P(Q_2)=0.84$. לכן $P(Q_1\cap Q_2)=0.36$, ו-$P(Q_1\mid Q_2)=\dfrac{0.36}{0.84}=\dfrac37\approx 0.43$, אבל $P(Q_2\mid Q_1)=1$.</div>
    <div class="lesson-trap">⚠️ הכיוון משנה. $P(Q_1\mid Q_2)\ne P(Q_2\mid Q_1)$, והמכנה הוא תמיד המעגל שידוע שפועל.</div>
    <div class="lesson-trap">⚠️ מעגל לא תמיד מוכל באחר. בדקו עם מצב אחד: אם יש מצב שבו $Q_1$ פועל ו-$Q_2$ לא, אין הכלה.</div>` },
  questions: [
    { id: "C07-Q1", image: "images/courses/circ/r_pair2.svg",
      step: { type: "numeric",
        prompt: "שלוש יחידות $A,B,C$ בהסתברות $0.5$ כל אחת (בלתי תלויות). המעגל $Q_1$: $A$ בטור עם הזוג המקבילי $B,C$. המעגל $Q_2$: $B$ בטור עם הזוג המקבילי $A,C$ (ראו איור). מה ההסתברות ששני המעגלים פועלים יחד?",
        answer: 0.25, tol: 0.0005,
        explain: "$Q_1=A\\cap(B\\cup C)$ ו-$Q_2=B\\cap(A\\cup C)$. אם $A$ ו-$B$ שתיהן פועלות, שני המעגלים פועלים. אם $B$ תקולה, $Q_2$ לא פועל, ואם $A$ תקולה, $Q_1$ לא פועל. לכן $Q_1\\cap Q_2=A\\cap B$ ו-$P=0.5\\cdot 0.5=0.25$." },
      sim: sim("P(Q1 and Q2)", 0.25, { network: SER(U("A", 0.5), PAR(U("B", 0.5), U("C", 0.5))), event: "(A == 1 and (B == 1 or C == 1)) and (B == 1 and (A == 1 or C == 1))" }),
      recap: "חיתוך בין שני מעגלים: מוצאים באילו מצבי יחידות שניהם פועלים" },
    { id: "C07-Q2", image: "images/courses/circ/r_pair2.svg",
      step: { type: "numeric",
        prompt: "באותם שני מעגלים ($P=0.5$ לכל יחידה): אם ידוע ש-$Q_2$ פועל, מה ההסתברות ש-$Q_1$ פועל? ענו כמספר עשרוני.",
        answer: 0.6667, tol: 0.0005,
        explain: "$P(Q_2)=0.5\\cdot(1-0.25)=0.375$, ו-$P(Q_1\\cap Q_2)=0.25$ מהשאלה הקודמת. $P(Q_1\\mid Q_2)=\\dfrac{0.25}{0.375}=\\dfrac23\\approx 0.6667$." },
      sim: sim("P(Q1 | Q2)", 2 / 3, { network: SER(U("A", 0.5), PAR(U("B", 0.5), U("C", 0.5))), event: "A == 1 and (B == 1 or C == 1)", given: "B == 1 and (A == 1 or C == 1)" }),
      recap: "$P(Q_1\\mid Q_2)$: חיתוך חלקי $P(Q_2)$" },
    { id: "C07-Q3", image: "images/courses/circ/r_pair2.svg",
      step: { type: "numeric",
        prompt: "באותם שני מעגלים ($P=0.5$ לכל יחידה): מה ההסתברות שלפחות אחד משני המעגלים פועל? ענו כמספר עשרוני.",
        answer: 0.5, tol: 0.0005,
        explain: "$P(Q_1)=P(Q_2)=0.375$ ו-$P(Q_1\\cap Q_2)=0.25$. $P(Q_1\\cup Q_2)=0.375+0.375-0.25=0.5$. אי אפשר לחבר בלי להחסיר את החיתוך, אחרת מקבלים $0.75$." },
      sim: sim("P(Q1 or Q2)", 0.5, { network: SER(U("A", 0.5), PAR(U("B", 0.5), U("C", 0.5))), event: "(A == 1 and (B == 1 or C == 1)) or (B == 1 and (A == 1 or C == 1))" }),
      recap: "איחוד: סכום פחות חיתוך" },
    { id: "C07-Q4", image: "images/courses/circ/r_pair5.svg",
      question: "שתי יחידות $A,B$ בהסתברות $0.5$ כל אחת (בלתי תלויות). $Q_1$ הוא חיבור בטור ו-$Q_2$ חיבור במקביל (ראו איור). אם ידוע ש-$Q_2$ פועל, מה ההסתברות ש-$Q_1$ פועל?",
      options: [{ id: "a", value: "1/3" }, { id: "b", value: "1" }, { id: "c", value: "0.25" }, { id: "d", value: "0.75" }],
      correctId: "a",
      sim: sim("P(Q1 | Q2)", 1 / 3, { network: SER(U("A", 0.5), U("B", 0.5)), event: "A == 1 and B == 1", given: "A == 1 or B == 1" }),
      explanation: "$Q_1\\subseteq Q_2$, ולכן $P(Q_1\\cap Q_2)=P(Q_1)=0.25$ ו-$P(Q_2)=0.75$. $P(Q_1\\mid Q_2)=\\dfrac{0.25}{0.75}=\\dfrac13$. התשובה 1 היא הכיוון ההפוך, $P(Q_2\\mid Q_1)$. 0.25 היא $P(Q_1)$ בלי התנאי. 0.75 היא $P(Q_2)$.",
      recap: "מעגל מוכל: $P(Q_1\\mid Q_2)=P(Q_1)/P(Q_2)$" },
    { bankId: "25A-A-Q4c", recap: "$P(Q_1\\mid Q_2)=P(Q_1\\cap Q_2)/P(Q_2)$: מחשבים את החיתוך בהתניה על היחידות המשותפות" },
    { bankId: "24B-A-Q6b", recap: "מתנים על היחידות המשותפות ומשלבים את שני המעגלים באותו אירוע" },
  ],
});
