/* pdf course, level 4 - two unknown constants: normalization plus E[X] give a 2x2 linear system. Checked by tools/verify/needhelp/pdf/check.py */
COURSE_LEVEL("pdf", {
  id: "C04", order: 4, icon: "⚖️", title: "שני קבועים: נרמול ותוחלת",
  goal: "אחרי השלב הזה אפשר למצוא שני קבועים (גם כשהתוחלת נתונה כסימן μ) מהנרמול ומהמשוואה השנייה שנותנת את התוחלת.",
  source: "ai-verified",
  lesson: {
    html: String.raw`
<p>כשיש שני קבועים לא ידועים, משוואת הנרמול לבדה לא מספיקה. במבחן נותנים בדרך כלל גם את <b>התוחלת</b> $E[X]$, ואז מקבלים <b>משוואה שנייה</b>.</p>
<div class="lesson-formula">$$E[X]=\int_{-\infty}^{\infty}x\,f_X(x)\,dx$$</div>
<p>מחשבים אותה כמו הנרמול, אבל <b>מכפילים את הצפיפות ב-$x$ לפני שמאנטגרלים</b>, ושוב קטע אחר קטע.</p>
<div class="lesson-rule">🔑 <b>המתכון:</b> (1) משוואת נרמול: $\int f=1$. (2) משוואת תוחלת: $\int x f=E[X]$. (3) הן שתיהן ליניאריות בקבועים, ולכן פותרים מערכת $2\times2$ (הצבה). (4) אם התוחלת נתונה כסימן $\mu$, הקבועים יוצאים כביטויים ב-$\mu$.</div>
<div class="lesson-ex">דוגמה: $f=a$ על $[0,1)$ ו-$f=b$ על $[1,2)$, ו-$E[X]=\tfrac54$. הנרמול: $a+b=1$. התוחלת: $\int_0^1 x\,a\,dx+\int_1^2 x\,b\,dx=\tfrac a2+\tfrac{3b}{2}=\tfrac54$. מציבים $a=1-b$: $\tfrac{1-b}{2}+\tfrac{3b}{2}=\tfrac12+b=\tfrac54$, ולכן $b=\tfrac34$ ו-$a=\tfrac14$.</div>
<p>שני אינטגרלים שחוזרים עם אקספוננט (מופיעים בנוסחון כ-$\int_0^\infty t^ne^{-t}dt=n!$):</p>
<table>
<thead><tr><th>אינטגרל</th><th>ערך</th></tr></thead>
<tbody>
<tr><td>$\int_0^\infty x\,e^{-x}\,dx$</td><td>$1$</td></tr>
<tr><td>$\int_{-\infty}^0 x\,e^{x}\,dx$</td><td>$-1$</td></tr>
</tbody></table>
<div class="lesson-trap">⚠️ בטעות נפוצה בחישוב התוחלת משתמשים בצפיפות כמו שהיא ושוכחים את ה-$x$. אם בקטע השני כתבתם $\int_1^2 b\,dx$ במקום $\int_1^2 x\,b\,dx$, קיבלתם שוב את משוואת הנרמול ולא משוואה חדשה.</div>`
  },
  questions: [
    { id: "C04-Q1",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a$ בקטע $[0,1)$, $f(x)=b$ בקטע $[1,2)$, ו-0 מחוץ לשניהם, ונתון $E[X]=\\frac76$. מהו $b$? (שבר או עשרוני)",
              answer: 0.666667, tol: 0.001,
              explain: "נרמול: $a+b=1$. תוחלת: $\\frac a2+\\frac{3b}{2}=\\frac76$. מציבים $a=1-b$: $\\frac12+b=\\frac76$, ולכן $b=\\frac23$ (ו-$a=\\frac13$)." },
      sim: { kind: "pdf", estimate: "E[X]", exact: 1.166666666667, params: { pieces: [{ from: 0, to: 1, expr: "1/3" }, { from: 1, to: 2, expr: "2/3" }], measure: "mean", expr: "x" } },
      recap: "נרמול ועוד תוחלת: שתי משוואות ליניאריות." },
    { id: "C04-Q2",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a\\,x$ בקטע $[0,1)$, $f(x)=b$ בקטע $[1,2)$, ו-0 מחוץ לשניהם, ונתון $E[X]=\\frac76$. מהו $a$? (שבר או עשרוני)",
              answer: 0.8, tol: 0.001,
              explain: "נרמול: $\\frac a2+b=1$. תוחלת: $\\int_0^1 x\\cdot a x\\,dx+\\int_1^2 x\\,b\\,dx=\\frac a3+\\frac{3b}{2}=\\frac76$. מ-$b=1-\\frac a2$ מקבלים $\\frac a3+\\frac32-\\frac{3a}{4}=\\frac76$, כלומר $-\\frac{5a}{12}=-\\frac13$ ו-$a=\\frac45$ (ו-$b=\\frac35$)." },
      sim: { kind: "pdf", estimate: "E[X]", exact: 1.166666666667, params: { pieces: [{ from: 0, to: 1, expr: "4/5*x" }, { from: 1, to: 2, expr: "3/5" }], measure: "mean", expr: "x" } },
      recap: "הצפיפות הראשונה היא $ax$, ולכן באינטגרל התוחלת מופיע $a x^2$." },
    { id: "C04-Q3",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a$ בקטע $[-2,0)$ ו-$f(x)=b\\,e^{-x}$ ל-$x\\ge0$ (ו-0 לפני $-2$), ונתון $E[X]=0$. מהו $b$? (שבר או עשרוני)",
              answer: 0.5, tol: 0.001,
              explain: "נרמול: $2a+b\\int_0^\\infty e^{-x}dx=2a+b=1$. תוחלת: $\\int_{-2}^0 x\\,a\\,dx+b\\int_0^\\infty x\\,e^{-x}dx=-2a+b=0$. לכן $b=2a$ ו-$4a=1$: $a=\\frac14$, $b=\\frac12$." },
      recap: "$\\int_0^\\infty x\\,e^{-x}\\,dx=1$, ו-$\\int_{-2}^0 x\\,dx=-2$." },
    { id: "C04-Q4", question: "הצפיפות היא $f(x)=a$ בקטע $[0,1)$, $f(x)=b$ בקטע $[1,2)$, ו-0 מחוץ לשניהם, ונתון $E[X]=\\mu$. איזה ביטוי הוא $a$?",
      options: [
        { id: "a", value: "$\\mu-\\dfrac12$" },
        { id: "b", value: "$\\dfrac32-\\mu$" },
        { id: "c", value: "$\\dfrac12-\\mu$" },
        { id: "d", value: "$2\\mu-1$" }],
      correctId: "b",
      explanation: "נרמול: $a+b=1$. תוחלת: $\\frac a2+\\frac{3b}{2}=\\mu$. מציבים $b=1-a$: $\\frac32-a=\\mu$, ולכן $a=\\frac32-\\mu$. הביטוי $\\mu-\\frac12$ הוא $b$ ולא $a$.",
      recap: "מבטאים את הקבוע הראשון באמצעות $\\mu$ מההצבה." },
    { id: "C04-Q5",
      step: { type: "findbug",
              prompt: "הצפיפות היא $f(x)=a\\,x$ בקטע $[0,1)$ ו-$f(x)=b$ בקטע $[1,2)$. הפותר חישב את התוחלת כך, ויש בפתרון טעות. באיזו שורה היא נעשתה לראשונה?",
              lines: [
                "נרמול: $\\dfrac a2+b=1$",
                "$\\mu=\\displaystyle\\int_0^1 x\\cdot a x\\,dx+\\int_1^2 b\\,dx$",
                "$\\mu=\\dfrac a3+b$"],
              bugIndex: 1,
              explain: "בקטע השני חסר ה-$x$: צריך $\\int_1^2 x\\cdot b\\,dx=\\frac{3b}{2}$. ללא ה-$x$ מחשבים את $\\int_1^2 b\\,dx=b$, שזה חלק מהנרמול, ולכן התוחלת הנכונה היא $\\mu=\\frac a3+\\frac{3b}{2}$." },
      recap: "בתוחלת מכפילים את הצפיפות ב-$x$ בכל קטע." },
    { id: "C04-Q6",
      step: { type: "numeric",
              prompt: "הצפיפות היא $f(x)=a\\,e^{x}$ ל-$x<0$ ו-$f(x)=b$ בקטע $[0,1)$ (ו-0 אחרי 1), ונתון $E[X]=-\\frac13$. מהו $b$? (שבר או עשרוני)",
              answer: 0.444444, tol: 0.001,
              explain: "נרמול: $a+b=1$. תוחלת: $a\\int_{-\\infty}^0 x\\,e^{x}dx+b\\int_0^1 x\\,dx=-a+\\frac b2=-\\frac13$. מציבים $a=1-b$: $-1+b+\\frac b2=-\\frac13$, כלומר $\\frac{3b}{2}=\\frac23$ ו-$b=\\frac49$ (ו-$a=\\frac59$)." },
      recap: "$\\int_{-\\infty}^0 x\\,e^{x}\\,dx=-1$." },
  ],
});
