/* geo, level 6 - CDF of max and min of two uniforms, with its density and mean. */
COURSE_LEVEL("geo", {
  id: "C06", order: 6, icon: "📈", title: "מקסימום ומינימום: התפלגות מצטברת",
  goal: "אחרי השלב הזה אפשר לחשב את ההתפלגות המצטברת של $\\max(X,Y)$ ושל $\\min(X,Y)$, ואת הצפיפות והתוחלת שלהן.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>עד עכשיו חישבנו הסתברות של אירוע אחד. אבל אפשר לשאול על משתנה חדש $Z$ שמוגדר מ-$X$ ו-$Y$, ולבקש את <b>ההתפלגות המצטברת</b> שלו, $F_Z(t)=P(Z\le t)$, לכל $t$. מקבעים $t$, מציירים את האזור $\{Z\le t\}$ ומחשבים את שטחו כפונקציה של $t$.</p>
    <h3>המקסימום</h3>
    <div class="lesson-rule">🔑 $\max(X,Y)\le t$ אם ורק אם <b>שניהם</b> $\le t$: $X\le t$ וגם $Y\le t$. זה ריבוע בצלע $t$ בפינת הראשית, ולכן $F_{\max}(t)=t^2$ עבור $0\le t\le1$.</div>
    <h3>המינימום</h3>
    <div class="lesson-rule">🔑 $\min(X,Y)>t$ אם ורק אם <b>שניהם</b> $>t$. זה ריבוע בצלע $1-t$ בפינה $(1,1)$, ולכן $F_{\min}(t)=1-(1-t)^2=2t-t^2$ עבור $0\le t\le1$. ("המינימום קטן מ-$t$" הוא "$X<t$ או $Y<t$", איחוד, ולכן עוברים למשלים.)</div>
    <div class="lesson-ex"><b>דוגמה.</b> בריבוע היחידה, $P(\min(X,Y)<\frac13)=1-\left(\frac23\right)^2=\frac59$: המשלים הוא ריבוע בצלע $\frac23$ שטחו $\frac49$.</div>
    <div class="region-fig" data-region='{"space": {"x": [0, 1], "y": [0, 1]}, "event": {"any": [[{"a": 1, "b": 0, "c": "1/3", "op": "<"}], [{"a": 0, "b": 1, "c": "1/3", "op": "<"}]]}, "labels": {"x": "X", "y": "Y"}, "caption": "min(X,Y)<1/3"}'></div>
    <h3>צפיפות ותוחלת</h3>
    <p>הצפיפות היא הנגזרת של ההתפלגות המצטברת: $f=F'$. למקסימום $f(t)=2t$ על $(0,1)$, והתוחלת היא $E[Z]=\int t\,f(t)\,dt$, כלומר $\int_0^1 2t^2\,dt=\frac23$.</p>
    <div class="lesson-trap">⚠️ אם אחד המשתנים אחיד על טווח אחר, כמו $(0,2)$, זה כבר לא ריבוע יחידה: מחשבים את השטח ומחלקים ב-$|\Omega|$.</div>` },
  questions: [
    { id: "geo-C06-Q1",
      step: { type: "numeric", answer: 0.4444, tol: 0.004,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P\\left(\\max(X,Y)<\\frac23\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "המקסימום קטן מ-$\\frac23$ כששניהם קטנים מ-$\\frac23$: ריבוע בצלע $\\frac23$ ושטחו $\\frac49$. לכן $P=\\frac49\\approx0.444$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 0, c: "2/3", op: "<" }, { a: 0, b: 1, c: "2/3", op: "<" }], labels: { x: "X", y: "Y" }, caption: "max(X,Y)<2/3" },
      sim: { kind: "area", estimate: "P(max(X,Y)<2/3)", exact: 4 / 9, params: { space: { x: [0, 1], y: [0, 1] }, event: "max(x,y)<2/3" } },
      recap: "מקסימום קטן מ-$t$: שניהם קטנים מ-$t$, ריבוע $t^2$." },
    { id: "geo-C06-Q2",
      question: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P\\left(\\min(X,Y)>\\frac14\\right)$ ?",
      options: [{ id: "a", value: "$\\frac{9}{16}$" }, { id: "b", value: "$\\frac{7}{16}$" }, { id: "c", value: "$\\frac34$" }, { id: "d", value: "$\\frac1{16}$" }],
      correctId: "a",
      region: { space: { x: [0, 1], y: [0, 1] }, event: [{ a: 1, b: 0, c: "1/4", op: ">" }, { a: 0, b: 1, c: "1/4", op: ">" }], labels: { x: "X", y: "Y" }, caption: "min(X,Y)>1/4" },
      sim: { kind: "area", estimate: "P(min(X,Y)>1/4)", exact: 9 / 16, params: { space: { x: [0, 1], y: [0, 1] }, event: "min(x,y)>1/4" } },
      explanation: "המינימום גדול מ-$\\frac14$ כששניהם גדולים מ-$\\frac14$: ריבוע בצלע $\\frac34$, שטחו $\\frac9{16}$. התשובה $\\frac7{16}$ היא $P(\\min<\\frac14)$, המשלים. התשובה $\\frac34$ היא $P(X>\\frac14)$ של משתנה אחד בלבד, בלי הדרישה שגם $Y$ גדול מ-$\\frac14$.",
      recap: "מינימום גדול מ-$t$: שניהם גדולים, ריבוע $(1-t)^2$." },
    { id: "geo-C06-Q3",
      step: { type: "numeric", answer: 0.4375, tol: 0.005,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים. מהי $P\\left(\\min(X,Y)<\\frac14\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "\"המינימום קטן מ-$\\frac14$\" הוא איחוד ($X<\\frac14$ או $Y<\\frac14$), ולכן מחשבים משלים: ריבוע בצלע $\\frac34$ בפינה $(1,1)$, שטח $\\frac9{16}$. התשובה $1-\\frac9{16}=\\frac7{16}=0.4375$." },
      region: { space: { x: [0, 1], y: [0, 1] }, event: { any: [[{ a: 1, b: 0, c: "1/4", op: "<" }], [{ a: 0, b: 1, c: "1/4", op: "<" }]] }, labels: { x: "X", y: "Y" }, caption: "min(X,Y)<1/4" },
      sim: { kind: "area", estimate: "P(min(X,Y)<1/4)", exact: 7 / 16, params: { space: { x: [0, 1], y: [0, 1] }, event: "min(x,y)<1/4" } },
      recap: "איחוד: חישוב דרך המשלים." },
    { id: "geo-C06-Q4",
      question: "$X,Y\\sim U_c(0,1)$ בלתי תלויים ו-$Z=\\min(X,Y)$. מהי ההתפלגות המצטברת $F_Z(t)$ עבור $0\\le t\\le1$ ?",
      options: [{ id: "a", value: "$t^2$" }, { id: "b", value: "$2t-t^2$" }, { id: "c", value: "$1-t^2$" }, { id: "d", value: "$t$" }],
      correctId: "b",
      explanation: "$P(Z>t)=(1-t)^2$, ולכן $F_Z(t)=1-(1-t)^2=2t-t^2$. הביטוי $t^2$ הוא ההתפלגות של המקסימום. הביטוי $1-t^2$ הוא משלים של המקסימום, והביטוי $t$ היה התפלגות של משתנה בודד. בדיקה: ב-$t=1$ התשובה הנכונה נותנת $1$, וב-$t=0$ היא נותנת $0$.",
      recap: "$F_{\\min}(t)=1-(1-t)^2$ ו-$F_{\\max}(t)=t^2$." },
    { id: "geo-C06-Q5",
      step: { type: "numeric", answer: 0.125, tol: 0.003,
              prompt: "$X\\sim U_c(0,1)$ ו-$Y\\sim U_c(0,2)$ בלתי תלויים. מהי $P\\left(\\max(X,Y)<\\frac12\\right)$ ? (אפשר שבר או עשרוני)",
              explain: "$|\\Omega|=1\\cdot2=2$. המקסימום קטן מ-$\\frac12$ כש-$X<\\frac12$ וגם $Y<\\frac12$: מלבן $\\frac12\\times\\frac12$, שטחו $\\frac14$. לכן $P=\\frac{1/4}{2}=\\frac18$." },
      region: { space: { x: [0, 1], y: [0, 2] }, event: [{ a: 1, b: 0, c: "1/2", op: "<" }, { a: 0, b: 1, c: "1/2", op: "<" }], labels: { x: "X", y: "Y" }, caption: "max(X,Y)<1/2 במלבן (0,1)×(0,2)" },
      sim: { kind: "area", estimate: "P(max(X,Y)<1/2)", exact: 1 / 8, params: { space: { x: [0, 1], y: [0, 2] }, event: "max(x,y)<1/2" } },
      recap: "במלבן מחלקים ב-$|\\Omega|=2$." },
    { id: "geo-C06-Q6",
      step: { type: "numeric", answer: 0.6667, tol: 0.004,
              prompt: "$X,Y\\sim U_c(0,1)$ בלתי תלויים ו-$Z=\\max(X,Y)$. מהי התוחלת $E[Z]$ ? (אפשר שבר או עשרוני)",
              explain: "$F_Z(t)=t^2$ ולכן הצפיפות $f_Z(t)=2t$ על $(0,1)$. התוחלת $\\int_0^1t\\cdot2t\\,dt=\\frac23$." },
      sim: { kind: "area", estimate: "E[max(X,Y)]", exact: 2 / 3, params: { space: { x: [0, 1], y: [0, 1] }, measure: "mean", expr: "max(x,y)" } },
      recap: "מהמצטברת גוזרים צפיפות, ואז $E[Z]=\\int tf(t)\\,dt$." },
  ],
});
