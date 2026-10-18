/* Circuits course, level 6 - Bayes on circuits: P(unit works | the circuit works) */
const U = (id, p) => ({ type: "comp", id, p });
const SER = (...k) => ({ type: "series", children: k });
const PAR = (...k) => ({ type: "parallel", children: k });
const sim = (estimate, exact, params) => ({ kind: "circuit", estimate, exact, params });
COURSE_LEVEL("circ", {
  id: "C06", order: 6, icon: "🔍", title: "בייס במעגלים: אם ידוע שהמעגל פועל",
  goal: "לחשב את ההסתברות שיחידה פועלת (או כולן, או לא) בהינתן שהמעגל כולו פועל.",
  source: "ai-verified",
  lesson: { figs: [{ src: "images/courses/circ/b_sp.svg", alt: "A בטור עם הזוג המקבילי B ו-C", caption: "דוגמה לשאלת בייס: אם ידוע שהמעגל פועל, מה הסיכוי ש-B פועלת?" }], html: String.raw`
    <p>שאלה נפוצה: "אם <b>ידוע</b> שהמעגל פועל, מה ההסתברות שיחידה $X$ פועלת?" זו הסתברות מותנית, והמכנה הוא תמיד מה שידוע, כלומר $P(S)$:</p>
    <div class="lesson-formula">$P(X\mid S)=\dfrac{P(X\cap S)}{P(S)}=\dfrac{P(X)\,P(S\mid X)}{P(S)}$</div>
    <div class="lesson-rule">🔑 מהלך הפתרון: (1) מחשבים $P(S)$ בשיטות מהשלבים הקודמים. (2) מחשבים $P(X\cap S)$: מניחים ש-$X$ פועלת (היא הופכת לחוט במעגל), מחשבים את $P(S\mid X)$ וכופלים ב-$P(X)$. (3) מחלקים.</div>
    <p>שני מקרים קיצוניים שחוסכים חישוב:</p>
    <ul>
      <li><b>יחידה בטור:</b> אם המעגל פועל, היחידה חייבת לפעול, ולכן $P(X\mid S)=1$.</li>
      <li><b>יחידה במקביל:</b> כשהמעגל פועל, ייתכן שדווקא יחידה אחרת הצילה אותו, ולכן $P(X\mid S)<1$, אבל עדיין גדול מ-$P(X)$.</li>
    </ul>
    <div class="lesson-ex">דוגמה: שתי יחידות במקביל, כל אחת בהסתברות $0.5$. $P(S)=1-0.25=0.75$. אם $A$ פועלת המעגל פועל בוודאות, ולכן $P(A\cap S)=P(A)=0.5$. התוצאה: $P(A\mid S)=\dfrac{0.5}{0.75}=\dfrac23$, גדולה מ-$0.5$. כלל הנוסחה לשתי יחידות זהות: $P(A\mid S)=\dfrac{1}{2-p}$.</div>
    <div class="lesson-trap">⚠️ הכיוון משנה: $P(X\mid S)\ne P(S\mid X)$. בשאלה "אם ידוע שהמעגל פועל" המכנה הוא $P(S)$, לא $P(X)$.</div>
    <div class="lesson-trap">⚠️ "כל היחידות פועלות" ו"המעגל פועל" אינם אותו מאורע בטופולוגיה עם מקביל. כשרוצים את $P(\text{all}\mid S)$ מחשבים $P(\text{all})$, שהוא מכפלת כל $p_i$, ומחלקים ב-$P(S)$.</div>` },
  questions: [
    { id: "C06-Q1", image: "images/courses/circ/b_ser.svg",
      question: "שתי יחידות בטור, כל אחת פועלת בהסתברות $0.7$ (בלתי תלויות). אם ידוע שהמעגל פועל, מה ההסתברות ש-$A$ פועלת?",
      options: [{ id: "a", value: "1" }, { id: "b", value: "0.7" }, { id: "c", value: "0.49" }, { id: "d", value: "0.51" }],
      correctId: "a",
      sim: sim("P(A | S)", 1, { network: SER(U("A", 0.7), U("B", 0.7)), event: "A == 1", given: "S == 1" }),
      explanation: "בטור המעגל פועל רק אם $A$ פועלת, ולכן $A\\cap S=S$ ו-$P(A\\mid S)=\\dfrac{P(S)}{P(S)}=1$. התשובה 0.7 היא $P(A)$ ללא התנאי. 0.49 היא $P(S)$ עצמה. 0.51 הוא $1-P(S)$.",
      recap: "יחידה בטור, בהינתן שהמעגל פועל: ההסתברות 1" },
    { id: "C06-Q2", image: "images/courses/circ/b_par.svg",
      step: { type: "numeric",
        prompt: "שתי יחידות במקביל, כל אחת פועלת בהסתברות $0.6$ (בלתי תלויות). אם ידוע שהמעגל פועל, מה ההסתברות ש-$A$ פועלת? ענו כמספר עשרוני.",
        answer: 0.7143, tol: 0.0005,
        explain: "$P(S)=1-0.4^2=0.84$. אם $A$ פועלת המעגל פועל, ולכן $P(A\\cap S)=P(A)=0.6$. $P(A\\mid S)=\\dfrac{0.6}{0.84}=\\dfrac57\\approx 0.7143$. אפשר גם בנוסחה $\\dfrac{1}{2-p}=\\dfrac{1}{1.4}$." },
      sim: sim("P(A | S)", 5 / 7, { network: PAR(U("A", 0.6), U("B", 0.6)), event: "A == 1", given: "S == 1" }),
      recap: "$P(A\\cap S)=P(A)$ כשפעולת $A$ לבדה מספיקה" },
    { id: "C06-Q3", image: "images/courses/circ/b_sp2.svg",
      step: { type: "numeric",
        prompt: "$A$ בטור עם הזוג המקבילי $B,C$ (ראו איור), כאשר $P(A)=0.9$, $P(B)=0.5$ ו-$P(C)=0.8$ (בלתי תלויות). אם ידוע שהמעגל פועל, מה ההסתברות ש-$B$ פועלת? ענו כמספר עשרוני.",
        answer: 0.5556, tol: 0.0005,
        explain: "$P(S)=0.9\\cdot(1-0.5\\cdot 0.2)=0.9\\cdot 0.9=0.81$. אם $B$ פועלת, המעגל פועל כש-$A$ פועלת: $P(S\\mid B)=0.9$, ולכן $P(B\\cap S)=0.5\\cdot 0.9=0.45$. $P(B\\mid S)=\\dfrac{0.45}{0.81}=\\dfrac59\\approx 0.5556$." },
      sim: sim("P(B | S)", 5 / 9, { network: SER(U("A", 0.9), PAR(U("B", 0.5), U("C", 0.8))), event: "B == 1", given: "S == 1" }),
      recap: "מניחים שהיחידה פועלת, מחשבים את $P(S\\mid X)$ וכופלים ב-$P(X)$" },
    { id: "C06-Q4",
      step: { type: "findbug",
        prompt: "מחשבים את ההסתברות ש-$A$ פועלת בהינתן שהמעגל פועל, כששתי יחידות זהות ($P=0.6$) במקביל. בפתרון שורה אחת שגויה. סמנו אותה.",
        lines: [
          "$P(S)=1-(1-0.6)^2=0.84$",
          "$P(A\\cap S)=P(A)=0.6$, כי אם $A$ פועלת אז המעגל פועל",
          "$P(A\\mid S)=\\dfrac{P(A\\cap S)}{P(A)}$",
          "$=\\dfrac{0.6}{0.84}\\approx 0.714$"],
        bugIndex: 2,
        explain: "בהסתברות מותנית המכנה הוא ההסתברות של **מה שידוע**, כלומר $P(S)$, לא $P(A)$. עם $P(A)$ במכנה היה יוצא $\\dfrac{0.6}{0.6}=1$, ולא $0.714$ כמו בשורה האחרונה." },
      recap: "$P(X\\mid S)=\\dfrac{P(X\\cap S)}{P(S)}$: המכנה הוא מה שידוע" },
    { id: "C06-Q5", image: "images/courses/circ/b_sp.svg",
      step: { type: "numeric",
        prompt: "$A$ בטור עם הזוג המקבילי $B,C$ (ראו איור), וכל היחידות פועלות בהסתברות $0.6$ (בלתי תלויות). אם ידוע שהמעגל פועל, מה ההסתברות שכל שלוש היחידות פועלות? ענו כמספר עשרוני.",
        answer: 0.4286, tol: 0.0005,
        explain: "$P(S)=0.6\\cdot(1-0.4^2)=0.6\\cdot 0.84=0.504$. אם כל שלוש פועלות המעגל פועל, ולכן $P(\\text{all}\\cap S)=P(\\text{all})=0.6^3=0.216$. $P(\\text{all}\\mid S)=\\dfrac{0.216}{0.504}=\\dfrac37\\approx 0.4286$." },
      sim: sim("P(all | S)", 3 / 7, { network: SER(U("A", 0.6), PAR(U("B", 0.6), U("C", 0.6))), event: "A == 1 and B == 1 and C == 1", given: "S == 1" }),
      recap: "כולן פועלות גורר שהמעגל פועל: המונה הוא $\\prod p_i$" },
    { bankId: "24S-A-Q6d", recap: "$P(\\text{all}\\mid S)=\\dfrac{p^6}{P(S)}$: מכפלת כל היחידות חלקי הסתברות המעגל" },
  ],
});
