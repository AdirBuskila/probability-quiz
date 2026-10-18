/* geo, level 2 - half-planes: x<c, y>x, x+y<c; triangles and the complement trick. */
COURSE_LEVEL("geo", {
  id: "C02", order: 2, icon: "📐", title: "חצאי מישור: קו אחד וצד אחד",
  goal: "אחרי השלב הזה אפשר לתרגם אי-שוויון בין $X$ ל-$Y$ לצד של קו, לבחור את הצד הנכון, ולחשב את שטח המשולש או המשלים.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>אירוע כמו $X+Y<\frac32$ או $Y>X$ הוא אי-שוויון בין $x$ ו-$y$. כל אי-שוויון כזה מחלק את המישור ל<b>שני צדדים</b> של קו, והאירוע הוא אחד מהצדדים.</p>
    <div class="lesson-rule">🔑 ארבעה צעדים: (1) מחליפים את האי-שוויון בשוויון ומציירים את <b>הקו</b> (שתי נקודות מספיקות). (2) מציבים <b>נקודת מבחן</b> כמו $(0.9,0.9)$ כדי לראות איזה צד מקיים את האי-שוויון. (3) מחשבים את שטח הצד הנכון בתוך המלבן. (4) מחלקים ב-$|\Omega|$.</div>
    <table><thead><tr><th>האירוע</th><th>הקו</th><th>מה האזור</th></tr></thead><tbody>
      <tr><td>$X<c$</td><td>$x=c$ אנכי</td><td>רצועה משמאל לקו</td></tr>
      <tr><td>$Y>X$</td><td>$y=x$ האלכסון</td><td>המשולש מעל האלכסון</td></tr>
      <tr><td>$X+Y<c$</td><td>$y=c-x$ יורד</td><td>משולש בפינה $(0,0)$ כש-$c\le1$</td></tr>
    </tbody></table>
    <div class="lesson-ex"><b>דוגמה.</b> בריבוע היחידה, $P(X+Y<\frac32)$. הקו $y=\frac32-x$ חותך את הריבוע בנקודות $(\frac12,1)$ ו-$(1,\frac12)$. ה<b>משלים</b> $X+Y>\frac32$ הוא משולש קטן בפינה $(1,1)$ עם ניצבים $\frac12$, ושטחו $\frac12\cdot\frac12\cdot\frac12=\frac18$. לכן $P=1-\frac18=\frac78$.</div>
    <div class="region-fig" data-region='{"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": 1, "c": "3/2", "op": "<"}], "labels": {"x": "X", "y": "Y"}, "caption": "X+Y<3/2"}'></div>
    <div class="lesson-rule">🔑 שטח משולש ישר-זווית: $\frac12\cdot$ ניצב $\cdot$ ניצב. כשהאזור גדול מחצי, עדיף לחשב את <b>המשלים</b> ולהחסיר מ-$1$ (או מ-$|\Omega|$ במלבן).</div>
    <div class="lesson-trap">⚠️ האלכסון $y=x$ יוצא מהפינה רק בריבוע. במלבן $(0,1)\times(0,2)$ האלכסון $y=x$ מגיע לנקודה $(1,1)$ ולא לפינה $(1,2)$: האזור $Y>x$ הוא טרפז, לא משולש.</div>` },
  questions: [
    { id: "geo-C02-Q1",
      question: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי $P(Y>X)$ ?",
      options: [{ id: "a", value: "$\\frac14$" }, { id: "b", value: "$\\frac12$" }, { id: "c", value: "$\\frac13$" }, { id: "d", value: "$\\frac34$" }],
      correctId: "b",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: -1, b: 1, c: 0, op: ">" }], labels: { x: "X", y: "Y" }, caption: "Y>X" },
      sim: { kind: "area", estimate: "P(Y>X)", exact: 0.5, params: { space: { x: [0, 1], y: [0, 1] }, event: "y>x" } },
      explanation: "האלכסון $y=x$ חותך את הריבוע לשני משולשים שווים, ואזור $Y>X$ הוא המשולש העליון: שטחו $\\frac12$ ו-$|\\Omega|=1$. התשובות $\\frac14$ ו-$\\frac13$ אינן שטח של שום חלק של הריבוע שנוצר מהאלכסון.",
      recap: "האלכסון מחלק את ריבוע היחידה לשני חצאים שווים." },
    { id: "geo-C02-Q2",
      step: { type: "numeric", answer: 0.2222, tol: 0.003,
              prompt: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. חשבו את $P\\left(X+Y<\\frac23\\right)$ (אפשר שבר או עשרוני).",
              explain: "הקו $y=\\frac23-x$ חותך את הצירים ב-$\\frac23$. האזור $X+Y<\\frac23$ הוא משולש בפינת הראשית עם ניצבים $\\frac23$ ו-$\\frac23$, ושטחו $\\frac12\\cdot\\frac23\\cdot\\frac23=\\frac29$. $|\\Omega|=1$ ולכן $P=\\frac29\\approx0.222$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 1, c: "2/3", op: "<" }], labels: { x: "X", y: "Y" }, caption: "X+Y<2/3" },
      sim: { kind: "area", estimate: "P(X+Y<2/3)", exact: 2 / 9, params: { space: { x: [0, 1], y: [0, 1] }, event: "x+y<2/3" } },
      recap: "משולש הפינה: $\\frac12 c^2$ כש-$c\\le1$." },
    { id: "geo-C02-Q3",
      question: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי $P\\left(X+Y<\\frac54\\right)$ ?",
      options: [{ id: "a", value: "$\\frac{23}{32}$" }, { id: "b", value: "$\\frac{9}{32}$" }, { id: "c", value: "$\\frac{25}{32}$" }, { id: "d", value: "$\\frac{15}{16}$" }],
      correctId: "a",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 1, c: "5/4", op: "<" }], labels: { x: "X", y: "Y" }, caption: "X+Y<5/4" },
      sim: { kind: "area", estimate: "P(X+Y<5/4)", exact: 23 / 32, params: { space: { x: [0, 1], y: [0, 1] }, event: "x+y<5/4" } },
      explanation: "המשלים $X+Y>\\frac54$ הוא משולש בפינה $(1,1)$ עם ניצבים $2-\\frac54=\\frac34$. שטחו $\\frac12\\cdot\\frac34\\cdot\\frac34=\\frac9{32}$, ולכן $P=1-\\frac9{32}=\\frac{23}{32}$. התשובה $\\frac9{32}$ היא שטח המשלים עצמו, בלי להחסיר מ-$1$.",
      recap: "כשהקו עובר מעל המרכז, מחשבים את משלים המשולש בפינה $(1,1)$." },
    { id: "geo-C02-Q4",
      step: { type: "numeric", answer: 0.75, tol: 0.005,
              prompt: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. מהי $P(Y>X)$ ? (אפשר שבר או עשרוני)",
              explain: "$|\\Omega|=1\\cdot2=2$. האלכסון $y=x$ מגיע ל-$(1,1)$. המשלים $Y<X$ הוא המשולש מתחת לאלכסון עם ניצבים $1$ ו-$1$, ושטחו $\\frac12$. לכן שטח $Y>X$ הוא $2-\\frac12=\\frac32$ ו-$P=\\frac{3/2}{2}=\\frac34$." },
      region: { space: { x: [0, 1], y: [0, 2] }, event: [{ a: -1, b: 1, c: 0, op: ">" }], labels: { x: "X", y: "Y" }, caption: "Y>X במלבן (0,1)x(0,2)" },
      sim: { kind: "area", estimate: "P(Y>X)", exact: 0.75, params: { space: { x: [0, 1], y: [0, 2] }, event: "y>x" } },
      recap: "במלבן האלכסון לא יוצא מהפינה: מחשבים משלים ומחלקים ב-$|\\Omega|$." },
    { id: "geo-C02-Q5",
      question: "$X$ ו-$Y$ בלתי תלויים, שניהם $U_c(0,1)$. מהי $P(Y>2X)$ ?",
      options: [{ id: "a", value: "$\\frac12$" }, { id: "b", value: "$\\frac14$" }, { id: "c", value: "$\\frac18$" }, { id: "d", value: "$\\frac13$" }],
      correctId: "b",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: -2, b: 1, c: 0, op: ">" }], labels: { x: "X", y: "Y" }, caption: "Y>2X" },
      sim: { kind: "area", estimate: "P(Y>2X)", exact: 0.25, params: { space: { x: [0, 1], y: [0, 1] }, event: "y>2*x" } },
      explanation: "הקו $y=2x$ יוצא מהראשית ופוגש את הצלע העליונה $y=1$ ב-$x=\\frac12$. האזור מעליו הוא משולש עם קודקודים $(0,0)$, $(0,1)$, $(\\frac12,1)$: בסיס $\\frac12$ (על הצלע העליונה) וגובה $1$, ושטחו $\\frac12\\cdot\\frac12\\cdot1=\\frac14$. התשובה $\\frac12$ מתאימה ל-$Y>X$ ולא ל-$Y>2X$.",
      recap: "קו דרך הראשית: מוצאים איפה הוא פוגש את צלע הריבוע." },
  ],
});
