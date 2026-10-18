# -*- coding: utf-8 -*-
"""Generator for tools/raw/26A-A.json -- probability (course 20021), semester A 2026, moed A (09.02.2026).
6 questions, 30 items (Q1 5, Q2 5, Q3 4, Q4 4, Q5 5, Q6 7). 25 points per question; Q2 part ה and Q5 part ה are
5-point bonus parts (graded only for a full solution, as printed).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_26A-A.py

Source: exam pp.1-4, handwritten official solutions on grid paper pp.5-20 (no text layer; rendered and read).

Transcription notes
- Part keys: the id scheme allows ONE letter per part. Q5 prints "א-1", "א-2", "א-3", "ב", "ג"(bonus); Q6 prints
  "א", "ב-1", "ב-2", "ג-1", "ג-2", "ג-3", "ד". They are stored as consecutive letters and the printed label is the
  first bold token of each question text. Map: Q5 a=א-1 b=א-2 c=א-3 d=ב e=ג(bonus);
  Q6 a=א b=ב-1 c=ב-2 d=ג-1 e=ג-2 f=ג-3 g=ד.
- The handwritten solutions are terse; they are transcribed step by step into Hebrew prose, no new results added.
- Math never holds Hebrew.
- Q1 region data and the sim specs live in the REGIONS / SIMS blocks above the exam dict.
- The page-1 cover (lecturer names) is not copied anywhere.
"""
import itertools, json, math, pathlib
from fractions import Fraction

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "26A-A.json"
CODE = "26A-A"
IMG = "images/exams/26A-A-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_CAP = (r"שתי נקודות $A$ ו-$B$ נבחרו באקראי על הקטע שארכו יחידה אחת. הן מחלקות את הקטע לשלושה קטעים: שמאלי, אמצעי וימני. "
          r"מיקום הנקודות מתואר על ידי שני משתנים מקריים בלתי תלויים בעלי התפלגות אחידה: $X_1\sim U_c\left(0,\frac12\right)$ ו-$X_2\sim U_c\left(0,\frac12\right)$. "
          r"כאן $X_1$ הוא אורך הקטע השמאלי ו-$X_2$ הוא אורך הקטע הימני, ולכן אורך הקטע האמצעי הוא $1-X_1-X_2$.")

Q1_OMEGA = r"""מרחב המדגם הוא הריבוע $\Omega=\left(0,\frac12\right)^2$ במישור $(x_1,x_2)$, ושטחו $|\Omega|=\frac14$. הסתברות היא שטח האזור חלקי $\frac14$ (גישה קלאסית)."""

questions.append(Q(
    1, "א", "uniform_geometric",
    r"מה ההסתברות שהקטע השמאלי הוא הכי קצר?",
    r"""**הקטע השמאלי הכי קצר.**
""" + Q1_OMEGA + r"""
הקטע השמאלי הכי קצר אם ורק אם הוא קצר מהימני ומהאמצעי:
$$P\bigl(X_1<X_2\ \cap\ X_1<1-X_1-X_2\bigr)=P\bigl(X_1<X_2<1-2X_1\bigr).$$
האזור הוא $\{x_1<x_2<1-2x_1\}$ בתוך הריבוע. הישר $x_2=x_1$ והישר $x_2=1-2x_1$ נחתכים ב-$x_1=\frac13$; הישר השני חותך את הצלע העליונה $x_2=\frac12$ ב-$x_1=\frac14$.
![האזור x1 < x2 < 1-2x1 בתוך הריבוע (0,1/2)^2](images/exams/26A-A-Q1a-region.png)
שטח האזור הוא שטח המשולש שבין הישר $x_2=x_1$ לצלע העליונה, פחות החלק שנחתך:
$$\left|\{x_1<x_2<1-2x_1\}\right|=\frac12\cdot\frac12\cdot\frac12-\frac12\cdot\frac14\cdot\frac16.$$
לכן
$$P=\frac{\frac12\cdot\frac12\cdot\frac12-\frac12\cdot\frac14\cdot\frac16}{1/4}=\frac{5}{12}.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"מה ההסתברות שהקטע הימני הוא הכי ארוך?",
    r"""**הקטע הימני הכי ארוך.**
""" + Q1_OMEGA + r"""
הקטע הימני ארוך מהשמאלי ומהאמצעי:
$$P\bigl(X_2>X_1\ \cap\ X_2>1-X_1-X_2\bigr)=P\left(X_2>X_1\ \cap\ X_2>\frac{1-X_1}{2}\right).$$
הישר $x_2=x_1$ והישר $x_2=\frac{1-x_1}2$ נחתכים ב-$x_1=\frac13$, והאזור המבוקש הוא המשולש שמעליהם בתוך הריבוע.
![האזור x2 > x1 וגם x2 > (1-x1)/2 בתוך הריבוע](images/exams/26A-A-Q1b-region.png)
שטח המשולש הוא $\frac12\cdot\frac12\cdot\frac16$, ולכן
$$P=\frac{\frac12\cdot\frac12\cdot\frac16}{1/4}=\frac16.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"מה ההסתברות שהקטע השמאלי הוא הקצר ביותר והקטע הימני הארוך ביותר?",
    r"""**שמאלי הכי קצר וימני הכי ארוך.**
לאחר שני הסעיפים הקודמים מדובר באזור
$$\left\{x_1<x_2<1-2x_1\ \cap\ x_2>\frac{1-x_1}{2}\right\},$$
כלומר בחיתוך שני האירועים.
![החיתוך: משולש קטן בפינה השמאלית העליונה של הריבוע](images/exams/26A-A-Q1c-region.png)
זהו משולש קטן, ושטחו
$$\left|\{\cdots\}\right|=\frac12\cdot\frac14\cdot\left(\frac12-\frac13\right)=\frac12\cdot\frac14\cdot\frac16.$$
מכאן
$$P=\frac{\frac12\cdot\frac14\cdot\frac16}{1/4}=\frac1{12}.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"מה ההסתברות שהקטע האמצעי הוא הארוך בין שלושה?",
    r"""**הקטע האמצעי הכי ארוך.**
האמצעי ארוך משני האחרים:
$$P\bigl(1-X_1-X_2>X_1\ \cap\ 1-X_1-X_2>X_2\bigr)=P\left(X_2<1-2X_1\ \cap\ X_2<\frac{1-X_1}{2}\right).$$
האזור הוא החלק של הריבוע שמתחת לשני הישרים, כלומר טרפז.
![האזור שמתחת לשני הישרים בתוך הריבוע](images/exams/26A-A-Q1d-region.png)
משלים האזור בריבוע הוא שני משולשים חופפים: האחד שבו $X_1$ הקטע הארוך ביותר, והשני שבו $X_2$ הארוך ביותר, ושטח כל אחד מהם $\frac1{24}$ (למשל הראשון הוא המשולש עם קודקודים $\left(\frac13,\frac13\right)$, $\left(\frac12,0\right)$, $\left(\frac12,\frac12\right)$). לכן השטח הוא שטח הריבוע פחות שני המשולשים:
$$\frac14-2\cdot\frac1{24}=\frac16=\frac14\cdot\frac23.$$
לכן
$$P=\frac{\frac14\cdot\frac23}{1/4}=\frac23.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ה", "uniform_geometric",
    r"מה ההסתברות שלכל הקטעים יש אותו אורך?",
    r"""**שלושת הקטעים שווים.**
$$P\bigl(X_1=X_2=1-X_1-X_2\bigr)=0,$$
כיוון שמדובר במשתנים רציפים: האירוע הוא נקודה בודדת במישור, ושטחה אפס.""",
    5, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_CAP = (r"כל אחד משני השחקנים, יוג׳ין ובוריס, מטיל מטבע מוטה עד קבלת התוצאה ״עץ״ בפעם הראשונה. "
          r"(המטבעות של שני השחקנים מוטים באותו אופן: הם בעלי הסתברות זהה לקבלת ״עץ״.) הראשון שמקבל ״עץ״ מנצח. "
          r"נתון כי ההסתברות לתיקו במשחק היא $Q$.")

questions.append(Q(
    2, "א", "special_discrete",
    r"מהי ההסתברות שיוג׳ין ינצח? מהי ההסתברות שבוריס ינצח?",
    r"""**ההסתברות לניצחון.**
מכיוון שהמטבעות של השחקנים מוטים באותה מידה, ההסתברות שיוג׳ין ינצח שווה להסתברות שבוריס ינצח:
$$P_E=P_B.$$
ובנוסף, האירועים (יוג׳ין ינצח, בוריס ינצח, תיקו) מהווים חלוקה:
$$P_E+P_B+Q=1.$$
מכאן
$$P_E=P_B=\frac{1-Q}{2}.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ב", "special_discrete",
    r"מהי ההסתברות לקבלת התוצאה ״עץ״ בהטלה בודדת של מטבע מוטה?",
    r"""**הסתברות העץ $p$ כפונקציה של $Q$.**
יהי $X_1$ מספר ההטלות של יוג׳ין עד קבלת ״עץ״ בפעם הראשונה, ו-$X_2$ מספר ההטלות של בוריס. אז $X_1,X_2$ בלתי תלויים והם גאומטריים:
$$X_1\sim G(p),\quad X_2\sim G(p),\qquad P(X_i=k)=p(1-p)^{k-1},\ k=1,2,\ldots$$
תיקו פירושו $X_1=X_2$, ולכן
$$\begin{aligned}Q&=P(X_1=X_2)=\sum_{k=1}^{\infty}P(X_1=k\cap X_2=k)=\sum_{k=1}^{\infty}P(X_1=k)P(X_2=k)\\&=p^2\sum_{k=1}^{\infty}\bigl[(1-p)^2\bigr]^{k-1}=p^2\cdot\frac1{1-(1-p)^2}=\frac{p}{2-p}.\end{aligned}$$
נחלץ את $p$ מהמשוואה $Q=\frac{p}{2-p}$:
$$p=\frac{2Q}{1+Q}.$$""",
    10, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"אם ידוע כי המשחק הסתיים בתיקו, מה ההסתברות ששני השחקנים הגיעו ל״עץ״ בפעם הראשונה בהטלה ה-$k$?",
    r"""**בהינתן תיקו, שניהם קיבלו עץ בהטלה $k$.**
$$\begin{aligned}P(X_1=k\cap X_2=k\mid X_1=X_2)&=\frac{P(X_1=k\cap X_2=k\cap X_1=X_2)}{P(X_1=X_2)}\\&=\frac{P(X_1=k)P(X_2=k)}{Q}=\frac{p^2(1-p)^{2(k-1)}}{Q}.\end{aligned}$$
נציב $p=\frac{2Q}{1+Q}$, ואז $1-p=\frac{1-Q}{1+Q}$:
$$P(X_1=k\cap X_2=k\mid X_1=X_2)=\frac{4Q}{(1+Q)^2}\left(\frac{1-Q}{1+Q}\right)^{2(k-1)}.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ד", "conditional_bayes",
    r"אם ידוע כי בוריס ניצח, מה ההסתברות שהוא קיבל ״עץ״ בפעם הראשונה בהטלה ה-$k$?",
    r"""**בהינתן שבוריס ניצח, הוא קיבל עץ בהטלה $k$.**
בוריס מנצח אם $X_2<X_1$, ו-$P_B=\frac{1-Q}{2}$ מסעיף א׳. לכן
$$P(X_2=k\mid X_2<X_1)=\frac{P(X_2=k\cap X_2<X_1)}{P_B}=\frac{P(X_2=k)\,P(X_1>k)}{P_B}.$$
כאן $P(X_2=k)=p(1-p)^{k-1}$, $P(X_1>k)=(1-p)^k$ ו-$P_B=\frac{1-Q}{2}$. הצבה ופישוט (עם $p=\frac{2Q}{1+Q}$) נותנים
$$P(X_2=k\mid X_2<X_1)=\frac{4Q}{(1+Q)^2}\left(\frac{1-Q}{1+Q}\right)^{2(k-1)}.$$
שימו לב: התשובה זהה לזו של הסעיף הקודם.""",
    5, contextId="c2"))

questions.append(Q(
    2, "ה", "special_discrete",
    r"**סעיף בונוס:** מהי תוחלת אורך המשחק בהינתן שהסתיים בתיקו? (5 נק׳, הניקוד יינתן עבור פתרון מלא בלבד.)",
    r"""**תוחלת אורך המשחק בהינתן תיקו.**
מסעיף ג׳ עולה כי אורך המשחק $T$ בהינתן תיקו מקיים
$$P(T=k)=\frac{4Q}{(1+Q)^2}\left(\frac{1-Q}{1+Q}\right)^{2(k-1)},$$
כלומר
$$T\sim G\!\left(p_0=\frac{4Q}{(1+Q)^2}\right).$$
לכן
$$\mathbb{E}[T]=\frac1{p_0}=\frac{(1+Q)^2}{4Q}.$$""",
    5, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_CAP = (r"בקו ייצור לרכיבים אלקטרוניים בטכנולוגיית הדפסת תלת-ממד, מדפיסים שני רכיבים $A$ ו-$B$ זה לצד זה. "
          r"בשל אופי התהליך הטכנולוגי, קיימת תלות הדדית בתקינות הרכיבים. ההסתברות שרכיב בודד ($A$) תקין (פועל) הינה $P(A)=p$. "
          r"עם זאת, תקינות של רכיב $B$ תלויה במצבו של רכיב $A$: אם רכיב $A$ תקין, הרכיב $B$ פועל בהסתברות $q$, אך אם רכיב $A$ לא תקין, הרכיב $B$ פועל בהסתברות $s$.")

Q3_NOTE = "\n" + r"**הערה:** אין להשתמש בטבלאות אמת. יש לתת חישוב מפורט בכל סעיף."

questions.append(Q(
    3, "א", "circuits",
    r"מחברים את שניהם בטור. מה ההסתברות $P(Q_1)$ שהמעגל שנוצר פועל?" + Q3_NOTE,
    r"""**חיבור בטור.**
נתון $P(B\mid\bar A)=s$, $P(B\mid A)=q$, $P(A)=p$. בטור המעגל פועל אם ורק אם שני הרכיבים פועלים, ולכן
$$P(Q_1)=P(A\cap B)=P(B\mid A)P(A)=pq.$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ב", "circuits",
    r"מחברים את שניהם במקביל. מה ההסתברות $P(Q_2)$ שהמעגל שנוצר פועל?" + Q3_NOTE,
    r"""**חיבור במקביל.**
במקביל המעגל פועל אם לפחות אחד הרכיבים פועל:
$$P(Q_2)=P(A\cup B)=P(A)+P(B)-P(A\cap B),\qquad P(A)=p,\ P(A\cap B)=pq.$$
כדי למצוא את $P(B)$ נשתמש ב-$P(B\mid\bar A)=s$:
$$s=\frac{P(\bar A\cap B)}{P(\bar A)},\quad P(\bar A)=1-p\quad\Longrightarrow\quad P(\bar A\cap B)=s(1-p).$$
לכן
$$P(B)=P(A\cap B)+P(\bar A\cap B)=pq+s(1-p).$$
ומכאן
$$P(Q_2)=p+pq+s(1-p)-pq=p+s(1-p).$$""",
    6, contextId="c3"))

questions.append(Q(
    3, "ג", "conditional_bayes",
    r"אם ידוע כי המעגל $Q_2$ פועל, מה ההסתברות שגם $Q_1$ יפעל?" + Q3_NOTE,
    r"""**$P(Q_1\mid Q_2)$.**
$$P(Q_1\mid Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}.$$
כאן $Q_1\cap Q_2=(A\cap B)\cap(A\cup B)=A\cap B=Q_1$. לכן
$$P(Q_1\mid Q_2)=\frac{P(Q_1)}{P(Q_2)}=\frac{pq}{p+s(1-p)}.$$""",
    7, contextId="c3"))

questions.append(Q(
    3, "ד", "circuits",
    r"מה ההסתברות שלפחות אחד המעגלים יפעל?" + Q3_NOTE,
    r"""**$P(Q_1\cup Q_2)$.**
מאחר ש-$Q_1\subseteq Q_2$,
$$P(Q_1\cup Q_2)=P(A\cup B)=P(Q_2)=p+s(1-p).$$""",
    7, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_FX = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות" "\n"
         r"$$f_X(x)=\begin{cases}a\,e^{x},&x<0\\b\,(1-x)^2,&0\le x<2\\c,&x\ge 2\end{cases}$$"
         "\n" r"כאן, הפרמטרים $a$, $b$ ו-$c$ אינם ידועים.")

questions.append(Q(
    4, "א", "continuous_rv",
    r"חשבו את הפרמטרים $a$, $b$ ו-$c$ בהנחה שהתוחלת $\mathbb{E}[X]=\mu$.",
    r"""**מציאת $a,b,c$.**
כדי שהנרמול יתקיים צריך $c=0$ (קבוע על קרן אינסופית אינו אינטגרבילי). אז הנרמול נותן
$$1=\int_{-\infty}^{\infty}f_X(x)\,dx=a\int_{-\infty}^0e^x\,dx+b\int_0^2(1-x)^2\,dx,$$
כאשר $\int_{-\infty}^0e^x\,dx=1$ ו-$\int_0^2(1-x)^2\,dx=\frac23$. לכן
$$a+\frac23b=1.\qquad(1)$$
עבור התוחלת:
$$\mu=\mathbb{E}[X]=a\int_{-\infty}^0xe^x\,dx+b\int_0^2x(1-x)^2\,dx,$$
כאשר $\int_{-\infty}^0xe^x\,dx=-1$ ו-$\int_0^2x(1-x)^2\,dx=\frac23$. לכן
$$-a+\frac23b=\mu.\qquad(2)$$
משתי המשוואות מקבלים
$$a=\frac{1-\mu}{2},\qquad b=\frac34(1+\mu),\qquad c=0.$$""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"מהו הערך הגדול והקטן ביותר של התוחלת $\mu$?",
    r"""**התחום של $\mu$.**
צפיפות חייבת לקיים $f_X(x)\ge0$, ולכן $a\ge0$ ו-$b\ge0$. מ-$a\ge0$ מקבלים $1-\mu\ge0$, ומ-$b\ge0$ מקבלים $1+\mu\ge0$. לכן
$$-1\le\mu\le1.$$
הערך הקטן ביותר הוא $-1$ והגדול ביותר הוא $1$.
![סקיצה של f_X: עקומה אקספוננציאלית משמאל ל-0 בגובה a ב-0, ועקומה ריבועית בקטע 0 עד 2 שמתחילה בגובה b](images/exams/26A-A-Q4-pdf.png)""",
    5, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"מצאו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו אותה.",
    r"""**פונקציית ההתפלגות המצטברת.**
$F_X(t)=\int_{-\infty}^tf_X(x)\,dx$ לכל $t\in\mathbb{R}$, ולכן
$$F_X(t)=\begin{cases}a\displaystyle\int_{-\infty}^te^x\,dx,&t<0\\a+b\displaystyle\int_0^t(1-x)^2\,dx,&0\le t<2\\1,&t\ge2\end{cases}$$
כאשר $\int_{-\infty}^te^x\,dx=e^t$ ו-$\int_0^t(1-x)^2\,dx=\frac13\left\{(t-1)^3+1\right\}$. הצבת $a,b$ נותנת
$$F_X(t)=\begin{cases}\dfrac{1-\mu}{2}e^t,&t<0\\[2mm]\dfrac{3-\mu}{4}+\dfrac{1+\mu}{4}(t-1)^3,&0\le t<2\\[2mm]1,&t\ge2\end{cases}$$
![גרף F_X(t): עלייה מ-0 ל-(1-μ)/2 ב-t=0, אחר כך עד (3-μ)/4 ב-t=1, ועד 1 ב-t=2](images/exams/26A-A-Q4-cdf.png)""",
    5, contextId="c4"))

questions.append(Q(
    4, "ד", "continuous_rv",
    r"חשבו את ההסתברות $P(0<X<|\mu|)$.",
    r"""**$P(0<X<|\mu|)$.**
$$P(0<X<|\mu|)=F_X(|\mu|)-F_X(0).$$
מכיוון ש-$|\mu|\le1<2$ (סעיף ב׳) אפשר להשתמש בענף האמצעי של $F_X(t)$:
$$P(0<X<|\mu|)=\frac{3-\mu}{4}+\frac{1+\mu}{4}(|\mu|-1)^3-\frac{1-\mu}{2}=\frac{1+\mu}{4}\Bigl\{1-(1-|\mu|)^3\Bigr\}.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_A = r"עופרי שובר מקל באורך $L$ לשני חלקים באופן אקראי."

questions.append(Q(
    5, "א", "minmax_transform",
    Q5_A + "\n" + r"**(א-1):** יהי $X_1$ משתנה מקרי המתאר את אורך החלק **הקצר מבין השניים** ויהיה $\eta_1$ משתנה מקרי המתאר את היחס בין אורך $X_1$ לבין אורך המקל: $\eta_1=X_1/L$. מצאו את פונקציית ההתפלגות המצטברת $F_{\eta_1}(t)$ של משתנה זה (נא להציג חישוב מפורט). האם התשובה תלויה באורך המקל $L$?",
    r"""**$F_{\eta_1}(t)$.**
נסמן ב-$x$ את נקודת השבירה, $x\sim U_c(0,L)$. אז
$$X_1=\min(x,L-x),\qquad \eta_1=\frac{X_1}{L}=\min\left(\frac xL,1-\frac xL\right).$$
מחפשים $F_{\eta_1}(t)=P(\eta_1\le t)$ לכל $t\in\mathbb{R}$.
• עבור $t<0$: $F_{\eta_1}(t)=0$, כי $\eta_1$ אי-שלילי.
• עבור $t\ge\frac12$: $P(\eta_1\le t)=1$, כי תמיד $\eta_1\le\frac12$.
• עבור $0\le t<\frac12$: $\eta_1=\frac xL$ ב-$0\le x<\frac L2$ ו-$\eta_1=1-\frac xL$ ב-$\frac L2\le x\le L$. לכן $\eta_1\le t$ אם ורק אם $0\le x\le tL$ או $(1-t)L\le x\le L$:
$$P(\eta_1\le t)=P\bigl(0\le x\le tL\ \cup\ (1-t)L\le x\le L\bigr)=\frac{tL}{L}+\frac{L-(1-t)L}{L}=2t.$$
לסיכום
$$F_{\eta_1}(t)=\begin{cases}0,&t<0\\2t,&0\le t<\frac12\\1,&t\ge\frac12\end{cases}$$
![גרף F של η1: ישר עולה מ-0 ל-1 על הקטע מ-0 עד 1/2](images/exams/26A-A-Q5-cdf.png)
התשובה אינה תלויה ב-$L$.""",
    12))

questions.append(Q(
    5, "ב", "minmax_transform",
    Q5_A + "\n" + r"**(א-2):** מצאו את פונקציית הצפיפות $f_{\eta_1}(t)$ ומה שם ההתפלגות ומה הפרמטרים של ההתפלגות המתקבלת?",
    r"""**$f_{\eta_1}(t)$.**
$$f_{\eta_1}(t)=\frac{d}{dt}F_{\eta_1}(t)=\begin{cases}0,&t<0\\2,&0\le t<\frac12\\0,&t\ge\frac12\end{cases}$$
זוהי צפיפות אחידה:
$$\eta_1\sim U_c\left(0,\frac12\right).$$""",
    3))

questions.append(Q(
    5, "ג", "minmax_transform",
    Q5_A + "\n" + r"**(א-3):** חשבו את התוחלת $\mathbb{E}[\eta_1]$ ואת השונות $\operatorname{var}[\eta_1]$ של היחס.",
    r"""**תוחלת ושונות.**
עבור התפלגות אחידה על $\left(0,\frac12\right)$:
$$\mathbb{E}[\eta_1]=\frac{0+\frac12}{2}=\frac14,\qquad \operatorname{Var}[\eta_1]=\frac{\left(\frac12-0\right)^2}{12}=\frac1{48}.$$""",
    4))

questions.append(Q(
    5, "ד", "minmax_transform",
    Q5_A + "\n" + r"**(ב):** לאחר ששבר את המקל בפעם הראשונה, לוקח עופרי את החלק הקצר מבין השניים ($X_1$ שאורכו) ושובר גם אותו לשני חלקים באופן אקראי. יהי $X_2$ אורך החלק **הקצר מבין השניים** לאחר השבירה השנייה. חשבו את התוחלת $\mathbb{E}[X_2]$ ואת השונות $\operatorname{var}[X_2]$.",
    r"""**תוחלת ושונות של $X_2$.**
מההגדרה, $X_1=\eta_1L$ (כאשר $\eta_1\sim U_c(0,\frac12)$), ולכן $X_2=\eta_2X_1=\eta_2\eta_1L$, כאשר $\eta_2\sim U_c\left(0,\frac12\right)$ בלתי תלוי ב-$\eta_1$ (אותו מצב, על מקל באורך $X_1$).
מאי-התלות:
$$\mathbb{E}[X_2]=\mathbb{E}[\eta_2\eta_1L]=L\,\mathbb{E}[\eta_1]\,\mathbb{E}[\eta_2]=L\cdot\frac14\cdot\frac14=\frac L{16}.$$
עבור השונות:
$$\operatorname{Var}[X_2]=\mathbb{E}[X_2^2]-\left(\frac L{16}\right)^2,\qquad \mathbb{E}[X_2^2]=L^2\,\mathbb{E}[\eta_1^2]\,\mathbb{E}[\eta_2^2]=\left(\frac L{12}\right)^2,$$
כי
$$\mathbb{E}[\eta_1^2]=\operatorname{Var}[\eta_1]+\mathbb{E}[\eta_1]^2=\frac1{48}+\frac1{16}=\frac1{12}.$$
לכן
$$\operatorname{Var}[X_2]=L^2\left(\left(\frac1{12}\right)^2-\left(\frac1{16}\right)^2\right)=\frac{7L^2}{48^2}=\frac{7L^2}{2304}.$$""",
    6))

questions.append(Q(
    5, "ה", "minmax_transform",
    Q5_A + "\n" + r"**סעיף בונוס (ג):** עופרי ממשיך בתהליך: בכל שלב הוא שובר את החלק הקצר שהתקבל בשבירה הקודמת באופן אקראי. חשבו את התוחלת $\mathbb{E}[X_n]$ ואת השונות $\operatorname{var}[X_n]$ של החלק הקצר המתקבל לאחר $n$ שבירות. (5 נק׳, הניקוד יינתן עבור פתרון מלא בלבד.)",
    r"""**$n$ שבירות.**
באותו אופן $X_n=\eta_n\cdots\eta_1L$ עם $\eta_i$ בלתי תלויים ושווי התפלגות $U_c\left(0,\frac12\right)$. לכן
$$\mathbb{E}[X_n]=L\bigl(\mathbb{E}[\eta_1]\bigr)^n=L\left(\frac14\right)^n.$$
עבור השונות:
$$\mathbb{E}[X_n^2]=L^2\bigl(\mathbb{E}[\eta_1^2]\bigr)^n=L^2\left(\frac1{12}\right)^n,$$
ולכן
$$\operatorname{Var}[X_n]=\mathbb{E}[X_n^2]-L^2\left(\frac1{16}\right)^n=L^2\left\{\left(\frac1{12}\right)^n-\left(\frac1{16}\right)^n\right\}.$$""",
    5))

# ------------------------------------------------------------------ Q6
Q6_DEF = (r"נגדיר סוגי ״שכנות״ בין שני סימני $\times$ בעזרת הדיאגרמות המצורפות. **סמיכות אופקית:** שני הסימנים נמצאים במשבצות צמודות באותה שורה. "
          r"**סמיכות אנכית:** שני הסימנים נמצאים במשבצות צמודות באותה עמודה. "
          r"**סמיכות אלכסונית:** שני הסימנים נמצאים במשבצות החולקות פינה ויוצרים קו אלכסוני יורד $\backslash$. "
          r"**סמיכות אנטי-אלכסונית:** שני הסימנים נמצאים במשבצות החולקות פינה ויוצרים קו אלכסוני עולה $/$.")
Q6_IMG = "images/exams/26A-A-Q6-adjacent.png"
Q6_B = r"ממקמים באקראי שני סימני $\times$ בטבלה $3\times3$."
Q6_G = r"נתונה כעת טבלה ריבועית $N\times N$ כאשר $N\ge2$. ממקמים בה באקראי שני סימני $\times$."

questions.append(Q(
    6, "א", "combinatorics",
    r"נתונה טבלה בגודל $3\times3$ (סה״כ $9$ משבצות). בכמה דרכים שונות ניתן למקם שני סימני $\times$ זהים בטבלה? (לא ניתן לסמן את אותה המשבצת פעמיים).",
    r"""**מספר ההצבות.**
יש $9$ משבצות, ומתוכן בוחרים $2$ לסימונים זהים:
$$P_9(2,7)=\frac{9!}{2!\,7!}=36.$$""",
    3, image="images/exams/26A-A-Q6-board1.png"))

questions.append(Q(
    6, "ב", "combinatorics",
    Q6_DEF + "\n" + Q6_B + "\n" + r"**(ב-1):** מה ההסתברות שהם יהיו סמוכים אופקית או אנכית?",
    r"""**סמיכות אופקית או אנכית.**
**אופקית:** בכל שורה יש $2$ אפשרויות, ויש $3$ שורות, ולכן $2\times3=6$ אפשרויות.
**אנכית:** גם כאן $6$ אפשרויות, מאותה סיבה.
סך הכול $12$ אפשרויות, והסתברות
$$\frac{12}{36}=\frac13.$$""",
    3, image=Q6_IMG))

questions.append(Q(
    6, "ג", "combinatorics",
    Q6_DEF + "\n" + Q6_B + "\n" + r"**(ב-2):** מה ההסתברות שהם יהיו סמוכים אלכסונית או אנטי-אלכסונית?",
    r"""**סמיכות אלכסונית או אנטי-אלכסונית.**
**אלכסונית:** המשבצת העליונה-שמאלית של הזוג יכולה להיות בכל אחת מ-$2$ השורות העליונות ובכל אחת מ-$2$ העמודות השמאליות, ולכן $2\times2=4$ אפשרויות.
**אנטי-אלכסונית:** גם $4$ אפשרויות.
סך הכול $8$ אפשרויות, והסתברות
$$\frac{8}{36}=\frac29.$$""",
    3, image=Q6_IMG))

questions.append(Q(
    6, "ד", "combinatorics",
    Q6_G + "\n" + r"**(ג-1):** בכמה דרכים שונות ניתן למקם את הסימנים בטבלה? (לא ניתן לסמן את אותה המשבצת פעמיים).",
    r"""**$N\times N$: מספר ההצבות.**
$$P_{N^2}(2,N^2-2)=\frac{(N^2)!}{2!\,(N^2-2)!}=\frac{N^2(N^2-1)}{2}.$$""",
    3))

questions.append(Q(
    6, "ה", "combinatorics",
    Q6_DEF + "\n" + Q6_G + "\n" + r"**(ג-2):** מה ההסתברות שהם יהיו סמוכים אופקית או אנכית?",
    r"""**אופקית או אנכית ב-$N\times N$.**
בכל שורה יש $N-1$ אפשרויות לסמיכות אופקית, ויש $N$ שורות: $N(N-1)$. אותו מספר עבור סמיכות אנכית. סך הכול $2N(N-1)$. ההסתברות:
$$\frac{2N(N-1)}{N^2(N^2-1)/2}=\frac{4}{N(N+1)}.$$
(בדיקה: עבור $N=3$ מתקבל $\frac13$, כמו בסעיף ב-1.)""",
    4, image=Q6_IMG))

questions.append(Q(
    6, "ו", "combinatorics",
    Q6_DEF + "\n" + Q6_G + "\n" + r"**(ג-3):** מה ההסתברות שהם יהיו סמוכים אלכסונית או אנטי-אלכסונית?",
    r"""**אלכסונית או אנטי-אלכסונית ב-$N\times N$.**
עבור סמיכות אלכסונית: לכל שורה (מלבד השורה האחרונה) קיימות $N-1$ אפשרויות, וסך הכול $(N-1)^2$. אותו מספר עבור אנטי-אלכסונית. לכן ההסתברות המבוקשת:
$$\frac{2(N-1)^2}{N^2(N^2-1)/2}=\frac{4(N-1)}{N^2(N+1)}.$$""",
    4, image=Q6_IMG))

questions.append(Q(
    6, "ז", "combinatorics",
    r"נתונה טבלה ריבועית $N\times N$ כאשר $N\ge2$. כעת ממקמים בה באקראי $k$ סימני $\times$ כאשר $2\le k\le N$. מה ההסתברות ש-$k$ סימני $\times$ יהיו סמוכים אופקית, אנכית, אלכסונית או אנטי-אלכסונית?",
    r"""**$k$ סימנים ברצף.**
מרחב המדגם:
$$|\Omega|=P_{N^2}(k,N^2-k)=\frac{(N^2)!}{k!\,(N^2-k)!}=\binom{N^2}{k}.$$
• **כמות הסמיכויות האופקיות:** $N\cdot(N-k+1)$ (בכל שורה $N-k+1$ מקומות לרצף).
• **כמות הסמיכויות האנכיות:** $N(N-k+1)$.
• **כמות הסמיכויות האלכסוניות:** $(N-k+1)\cdot(N-k+1)$.
• **כמות הסמיכויות האנטי-אלכסוניות:** גם כאן $(N-k+1)^2$.
סך הכול כמות הסמיכויות מכל הסוגים:
$$2N(N-k+1)+2(N-k+1)^2=2(N-k+1)(2N-k+1).$$
ההסתברות המבוקשת על פי היחס:
$$\frac{2(N-k+1)(2N-k+1)}{\binom{N^2}{k}}.$$""",
    5, image="images/exams/26A-A-Q6-lines.png"))

# ------------------------------------------------------------------ area regions + simulations (RAW_SCHEMA `region`, `sim`)
_SQ = {"x": [0, 0.5], "y": [0, 0.5]}
_LB = {"x": "X1", "y": "X2"}
_L = lambda a, b, c, op: {"a": a, "b": b, "c": c, "op": op}
REGIONS = {
    (1, "א"): {"space": _SQ, "labels": _LB, "event": [_L(1, -1, 0, "<"), _L(2, 1, 1, "<")], "exact": 5 / 12, "caption": "הקטע השמאלי הכי קצר"},
    (1, "ב"): {"space": _SQ, "labels": _LB, "event": [_L(-1, 1, 0, ">"), _L(1, 2, 1, ">")], "exact": 1 / 6, "caption": "הקטע הימני הכי ארוך"},
    (1, "ג"): {"space": _SQ, "labels": _LB, "event": [_L(1, -1, 0, "<"), _L(2, 1, 1, "<"), _L(1, 2, 1, ">")], "exact": 1 / 12, "caption": "שמאלי הכי קצר וימני הכי ארוך"},
    (1, "ד"): {"space": _SQ, "labels": _LB, "event": [_L(2, 1, 1, "<"), _L(1, 2, 1, "<")], "exact": 2 / 3, "caption": "הקטע האמצעי הכי ארוך"},
}


def _pairs_3x3():
    cells = [(r, c) for r in range(3) for c in range(3)]
    rows = []
    for i in range(9):
        for j in range(i + 1, 9):
            rows.append({"p": 1 / 36, "r1": cells[i][0], "c1": cells[i][1], "r2": cells[j][0], "c2": cells[j][1]})
    return rows


SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(left shortest)", "exact": 5 / 12},
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(right longest)", "exact": 1 / 6},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(left shortest and right longest)", "exact": 1 / 12},
    (1, "ד"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(middle longest)", "exact": 2 / 3},
    (6, "ב"): {"kind": "custom_discrete", "params": {"joint": _pairs_3x3(), "event": "abs(r1-r2)+abs(c1-c2) == 1"},
               "estimate": "P(horizontal or vertical)", "exact": 1 / 3},
    (6, "ג"): {"kind": "custom_discrete", "params": {"joint": _pairs_3x3(), "event": "abs(r1-r2) == 1 and abs(c1-c2) == 1"},
               "estimate": "P(diagonal or anti-diagonal)", "exact": 2 / 9},
}

# ---- step-author additions: sims at sample parameter values for the symbolic answers
def _geom(p, K=80):
    probs = [p * (1 - p) ** (k - 1) for k in range(1, K + 1)]
    probs[-1] += 1 - sum(probs)          # tail mass (~1e-13) goes to the last value
    return {"values": list(range(1, K + 1)), "probs": probs}


_P2 = 0.3                                # Q2: coin bias p=0.3, so the tie probability is Q = p/(2-p) = 3/17
_Q2 = Fraction(3, 17)
_G2 = {"vars": {"X1": _geom(_P2), "X2": _geom(_P2)}}
_AB = [{"p": 0.42, "A": 1, "B": 1}, {"p": 0.18, "A": 1, "B": 0}, {"p": 0.08, "A": 0, "B": 1}, {"p": 0.32, "A": 0, "B": 0}]  # Q3: p=0.6,q=0.7,s=0.2
_C3 = {"joint": _AB}


def _cells(n):
    return [(r, c) for r in range(n) for c in range(n)]


def _pairs(n):
    cs = _cells(n)
    return [{"p": 1 / math.comb(n * n, 2), "r1": a[0], "c1": a[1], "r2": b[0], "c2": b[1]}
            for i, a in enumerate(cs) for b in cs[i + 1:]]


def _lines3(n):
    """the actual random placement: every 3-subset of cells of an n x n board is equally likely, in sorted order
    (r1,c1)<(r2,c2)<(r3,c3). Three marks are 'in a line' when consecutive cells differ by the same step, one cell in
    a row, column or diagonal (see _LINE3_EVENT)."""
    return [{"p": 1 / math.comb(n * n, 3), "r1": a[0], "c1": a[1], "r2": b[0], "c2": b[1], "r3": c[0], "c3": c[1]}
            for a, b, c in itertools.combinations(sorted(_cells(n)), 3)]


_LINE3_EVENT = "r2 - r1 == r3 - r2 and c2 - c1 == c3 - c2 and abs(r2 - r1) <= 1 and abs(c2 - c1) <= 1"


SIMS.update({
    (2, "א"): dict(kind="custom_discrete", params=dict(_G2, event="X1 < X2"), estimate="P(Eugene wins), p=0.3", exact=float((1 - _Q2) / 2)),
    (2, "ב"): dict(kind="custom_discrete", params=dict(_G2, event="X1 == X2"), estimate="P(tie) = p/(2-p) at p=0.3", exact=float(_Q2)),
    (2, "ג"): dict(kind="custom_discrete", params=dict(_G2, event="X1 == 2 and X2 == 2", given="X1 == X2"),
                   estimate="P(both at toss 2 | tie), p=0.3", exact=0.3 ** 2 * 0.7 ** 2 / float(_Q2)),
    (2, "ד"): dict(kind="custom_discrete", params=dict(_G2, event="X2 == 2", given="X2 < X1"),
                   estimate="P(X2=2 | Boris wins), p=0.3", exact=0.3 ** 2 * 0.7 ** 2 / float(_Q2)),
    (2, "ה"): dict(kind="custom_discrete", params=dict(_G2, measure="mean", expr="X1", given="X1 == X2"),
                   estimate="E[T | tie], p=0.3", exact=float((1 + _Q2) ** 2 / (4 * _Q2))),
    (3, "א"): dict(kind="custom_discrete", params=dict(_C3, event="A == 1 and B == 1"), estimate="P(Q1), p=0.6 q=0.7 s=0.2", exact=0.42),
    (3, "ב"): dict(kind="custom_discrete", params=dict(_C3, event="A == 1 or B == 1"), estimate="P(Q2), p=0.6 q=0.7 s=0.2", exact=0.68),
    (3, "ג"): dict(kind="custom_discrete", params=dict(_C3, event="A == 1 and B == 1", given="A == 1 or B == 1"),
                   estimate="P(Q1 | Q2), p=0.6 q=0.7 s=0.2", exact=21 / 34),
    (3, "ד"): dict(kind="custom_discrete", params=dict(_C3, event="A == 1 or B == 1"), estimate="P(Q1 u Q2), p=0.6 q=0.7 s=0.2", exact=0.68),
    (4, "ד"): dict(kind="pdf", params={"pieces": [{"from": -40, "to": 0, "expr": "0.25*exp(x)"},
                                                   {"from": 0, "to": 2, "expr": "1.125*(1-x)^2"}],
                                      "event": "x > 0 and x < 0.5"},
                   estimate="P(0<X<|mu|), mu=0.5", exact=21 / 64),
    (6, "ה"): dict(kind="custom_discrete", params={"joint": _pairs(4), "event": "abs(r1-r2)+abs(c1-c2) == 1"},
                   estimate="P(horizontal or vertical), N=4", exact=4 / (4 * 5)),
    (6, "ו"): dict(kind="custom_discrete", params={"joint": _pairs(4), "event": "abs(r1-r2) == 1 and abs(c1-c2) == 1"},
                   estimate="P(diagonal or anti-diagonal), N=4", exact=4 * 3 / (16 * 5)),
    (6, "ז"): dict(kind="custom_discrete", params={"joint": _lines3(4), "event": _LINE3_EVENT},
                   estimate="P(3 marks in a line), N=4 k=3", exact=2 * 2 * 6 / math.comb(16, 3)),
})

for _q in questions:
    _k = (_q["num"], _q.get("part"))
    if _k in REGIONS:
        _q["region"] = REGIONS[_k]
    if _k in SIMS:
        _q["sim"] = SIMS[_k]

# ---- step-author: rubric, pitfalls, guided steps. Data in steps_26A_A.py; every value is re-derived in
# tools/verify/26A-A/steps_check.py (exact + Monte Carlo).
import probsteps
from steps_26A_A import DATA as _STEPS
probsteps.apply(questions, _STEPS, CODE)

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ו, מועד א (09.02.2026)",
    "year": 2026,
    "examDate": "09.02.2026",
    "sourceFile": "26A-A exam pp.1-4",
    "solutionFile": "26A-A handwritten official solutions pp.5-20",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: שלושה קטעים", "image": IMG + "c1-segment.png", "caption": Q1_CAP},
        "c2": {"kind": "text", "title": "שאלה 2: יוג׳ין ובוריס", "text": Q2_CAP},
        "c3": {"kind": "image", "title": "שאלה 3: מעגלים", "image": IMG + "Q3-circuits.png", "caption": Q3_CAP},
        "c4": {"kind": "text", "title": "שאלה 4", "text": Q4_FX},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
