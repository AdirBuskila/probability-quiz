# -*- coding: utf-8 -*-
"""Generator for tools/raw/25B-B.json -- probability (course 20021), semester B 2025, moed B (12.08.2025). Choose 4 of 6
questions, 25 points each (Q2 has a 5-point bonus part). 29 items (Q1 6, Q2 6, Q3 5, Q4 4, Q5 5, Q6 3).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25B-B.py

Source: exam pp.1-3 (pdf), handwritten official solutions on grid paper pp.4-17 (no text layer; rendered and read).
Q3 and Q6 are printed "question from practice sheet no. 1 / no. 5"; they are ordinary exam questions here.

Transcription notes
- Part keys: single letters. Q1 prints "א", "ב-1", "ב-2", "ב-3", "ג", "ד" -> a b c d e f; Q2 prints "א-1", "א-2",
  "א-3", "ב", "ג", "ד"(bonus) -> a b c d e f; Q3 prints "א-1", "א-2", "ב-1", "ב-2", "ב-3" -> a b c d e;
  Q5 prints "א", "ב-1".."ב-4" -> a b c d e; Q6 prints "א-1", "א-2", "ב" -> a b c. The printed label is the first bold
  token of each question text.
- Q2 part ו (bonus, disjoint events): HELD. The official answer is s = q, but exact analysis shows that disjointness
  with P(B) > 0 forces p = 1 (s = q would make P(B) = 0). Disagreement with the official key -> hold + ASK_ADIR entry;
  the official key is not changed.
- Q3: the head of the school guesses at random; as in the official solution the sample space is the N^2 equally likely
  (guess, number) pairs.
- Q6 part א-1/ב: the official solution is a formula that refers to the practice sheet; the one-line derivation (total
  probability over the number X of red balls moved) is added so that the item is self-contained.
- Q1 region data: tools/verify/25B-B/regions.json (RAW_SCHEMA has no `region` field).
- The page-1 cover (lecturer names) is not copied anywhere.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25B-B.json"
CODE = "25B-B"
IMG = "images/exams/25B-B-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_CAP = (r"על חליל צד באורך $1$ מ׳ נבחרו שתי נקודות, באקראי וללא תלות אחת בשנייה. נאפיין את מיקום הנקודות באמצעות משתנים מקריים $X_1$ ו-$X_2$ "
          r"אשר מודדים את המרחק בין הקצה השמאלי של החליל לבין הנקודה עצמה. **שימו לב** כי המרחק $X_1$ יכול להיות גם גדול מ-$X_2$!")

Q1_X = r"נסמן $X=|X_1-X_2|$ (המרחק בין שתי הנקודות שנבחרו על החליל). מרחב המדגם הוא ריבוע היחידה $\Omega=(0,1)^2$ במישור $(x_1,x_2)$, ושטחו $|\Omega|=1$."

questions.append(Q(
    1, "א", "uniform_geometric",
    r"איך משתנה מקרי $X_1$ מפולג? איך משתנה מקרי $X_2$ מפולג? עליך לנמק היטב!",
    r"""**התפלגות המיקומים.**
כל נקודה נבחרת באקראי על חליל שאורכו $1$ מ׳, כלומר באופן אחיד לאורכו, והמרחק שלה מהקצה השמאלי הוא משתנה אחיד על $(0,1)$. הבחירות בלתי תלויות. לכן
$$X_1\sim U_c(0,1),\qquad X_2\sim U_c(0,1),$$
ובלתי תלויים.""",
    4, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"יהיה $X=|X_1-X_2|$ מרחק בין שתי הנקודות שנבחרו על החליל. **ב-1:** מצאו את ההסתברות $P(X<1/2)$.",
    r"""**$P(|X_1-X_2|<\frac12)$.**
""" + Q1_X + r"""
$$P\left(|X_1-X_2|<\frac12\right)=P\left(X_1-\frac12<X_2<X_1+\frac12\right)=\frac{\left|\{X_1-\frac12<X_2<X_1+\frac12\}\right|}{|\Omega|},\qquad|\Omega|=1.$$
האזור הוא הרצועה שבין הישרים $x_2=x_1+\frac12$ ו-$x_2=x_1-\frac12$ בתוך הריבוע. מחוץ לרצועה שני משולשים שכל אחד מהם בעל ניצבים $\frac12$ ו-$\frac12$:
![הרצועה בין הישרים x2 = x1 ± 1/2 בתוך ריבוע היחידה](images/exams/25B-B-Q1b-region.png)
$$P=1-2\cdot\frac12\cdot\frac12\cdot\frac12=\frac34.$$""",
    4, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"יהיה $X=|X_1-X_2|$ מרחק בין שתי הנקודות שנבחרו על החליל. **ב-2:** מצאו את ההסתברות $P(X>3/2)$.",
    r"""**$P(|X_1-X_2|>\frac32)$.**
$$P\left(|X_1-X_2|>\frac32\right)=1-P\left(X_1-\frac32<X_2<X_1+\frac32\right)=1-\frac{\left|\{X_1-\frac32<X_2<X_1+\frac32\}\right|}{|\Omega|}=1-\frac11=0.$$
(הרצועה מכסה את כל הריבוע, שכן $|X_1-X_2|<1$ תמיד.)""",
    4, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"יהיה $X=|X_1-X_2|$ מרחק בין שתי הנקודות שנבחרו על החליל. **ב-3:** מצאו את פונקציית ההתפלגות המצטברת $F_X(t)$ של משתנה מקרי $X$ ושרטטו אותה.",
    r"""**$F_X(t)$.**
$$F_X(t)=P(|X_1-X_2|\le t),\qquad t\in\mathbb{R}.$$
עבור $t<0$: $F_X(t)=0$. עבור $t\ge0$: $F_X(t)=\left|\{|x_1-x_2|\le t\}\right|$.
• $0\le t<1$: האזור הוא רצועה בין הישרים $x_2=x_1\pm t$; הקצוות הם שני משולשים עם ניצבים $1-t$:
![הרצועה בין הישרים x2 = x1 ± t בתוך הריבוע](images/exams/25B-B-Q1c-region.png)
$$\left|\{|x_1-x_2|\le t\}\right|=1-2\cdot\frac12(1-t)^2=t(2-t)=2t-t^2.$$
• $t\ge1$: השטח הוא $1$.
לכן
$$F_X(t)=\begin{cases}0,&t<0\\2t-t^2,&0\le t<1\\1,&t\ge1\end{cases}$$
![גרף F_X(t): עלייה קעורה מ-0 ל-1 על הקטע 0 עד 1](images/exams/25B-B-Q1c-cdf.png)""",
    8, contextId="c1"))

questions.append(Q(
    1, "ה", "continuous_rv",
    r"מצא/י את פונקציית צפיפות ההסתברות $f_X(t)$ של משתנה מקרי $X$, שרטטו אותה וודאו כי תכונת הנרמול מתקיימת.",
    r"""**פונקציית הצפיפות.**
$$f_X(t)=\frac d{dt}F_X(t)=\begin{cases}0,&t<0\\2(1-t),&0\le t<1\\0,&t\ge1\end{cases}$$
![גרף f_X(t): ישר יורד מ-2 ב-t=0 ל-0 ב-t=1](images/exams/25B-B-Q1d-pdf.png)
נרמול: השטח שמתחת לצפיפות הוא שטח משולש:
$$\frac12\cdot2\cdot1=1.$$""",
    2, contextId="c1"))

questions.append(Q(
    1, "ו", "continuous_rv",
    r"חשבו את תוחלת $\mathbb{E}[X]$.",
    r"""**$\mathbb{E}[X]$.**
$$\mathbb{E}[X]=\int_0^1t\cdot2(1-t)\,dt=2\left\{\frac{t^2}2-\frac{t^3}3\right\}\Big|_0^1=\frac13.$$""",
    3, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_CAP = r"יהיו $A$ ו-$B$ מאורעות לא ריקים. נתון כי $P(\bar A/B)=p$, $P(A/\bar B)=q$ ו-$P(A\cup B)=s$."

questions.append(Q(
    2, "א", "conditional_bayes",
    r"חשבו את ההסתברויות הבאות: **(א-1):** $P(A)$. (5 נק׳ לכל תת סעיף)",
    r"""**$P(A)$.**
נפתח משתי המשוואות הנתונות.
① מ-$P(\bar A/B)=p$ מקבלים $P(A/B)=1-p$, ולכן
$$P(A/B)=\frac{P(A\cap B)}{P(B)}=\frac{P(A)+P(B)-P(A\cup B)}{P(B)}=1-p,$$
כלומר $P(A)+P(B)-s=(1-p)P(B)$, ומכאן המשוואה הראשונה:
$$P(A)+p\,P(B)=s.$$
② מ-$P(A/\bar B)=q$ מקבלים $P(\bar A/\bar B)=1-q$, ולכן
$$P(\bar A/\bar B)=\frac{P(\bar A\cap\bar B)}{P(\bar B)}=\frac{P(\overline{A\cup B})}{1-P(B)}=\frac{1-s}{1-P(B)}=1-q,$$
ומכאן המשוואה השנייה (ראו סעיף א-2):
$$P(B)=\frac{s-q}{1-q}.$$
הצבה במשוואה הראשונה נותנת
$$P(A)=s-p\cdot\frac{s-q}{1-q}.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ב", "conditional_bayes",
    r"חשבו את ההסתברויות הבאות: **(א-2):** $P(B)$. (5 נק׳ לכל תת סעיף)",
    r"""**$P(B)$.**
מהמשוואה השנייה בסעיף א-1,
$$P(B)=\frac{s-q}{1-q}.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"חשבו את ההסתברויות הבאות: **(א-3):** $P(A\cap B)$. (5 נק׳ לכל תת סעיף)",
    r"""**$P(A\cap B)$.**
$$P(A\cap B)=P(A)+P(B)-P(A\cup B),$$
והצבה של התוצאות הקודמות נותנת
$$P(A\cap B)=(1-p)\,\frac{s-q}{1-q}.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ד", "independence",
    r"**ב:** האם ייתכן כי $q>s$? נמקו היטב!",
    r"""**האם $q>s$ אפשרי?**
לא. אילו $q>s$ היינו מקבלים
$$P(B)=\frac{s-q}{1-q}<0\qquad\text{and}\qquad P(A\cap B)=(1-p)\frac{s-q}{1-q}<0,$$
וזה בלתי אפשרי (הסתברות אינה שלילית). לכן התשובה היא **לא**.""",
    5, contextId="c2"))

questions.append(Q(
    2, "ה", "independence",
    r"**ג:** עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו **בלתי תלויים**?",
    r"""**אי-תלות.**
$A$ ו-$B$ בלתי תלויים אם ורק אם $P(A/\bar B)=P(A)$ וגם $P(A/B)=P(A)$. כאן $P(A/\bar B)=q$ ו-$P(A/B)=1-p$, ולכן שני האגפים שווים ל-$P(A)$ אם
$$p=1-q.$$""",
    5, contextId="c2"))

questions.append({
    "num": 2, "part": "ו", "kind": "computation", "topic": "independence",
    "question": r"**סעיף בונוס:** עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו **זרים**? (5 נק׳ – הניקוד יינתן עבור פתרון מלא בלבד.)",
    "contextId": "c2", "points": 5,
    "hold": ("key-disagreement: the official key is s = q (from P(A and B) = (1-p)(s-q)/(1-q) = 0), but s = q makes P(B) = 0, "
             "and for P(B) > 0 disjointness forces p = P(not-A | B) = 1 with s, q free (tools/verify/25B-B/check.py, Q2f). See ASK_ADIR."),
})

# ------------------------------------------------------------------ Q3
Q3_A = r"יוגיין בוחר באקראי מספר בין $1$ ל-$N$ ורושם אותו על הדף. ראש בית הספר למדעי המתמטיקה מנחש מהו מספרו של יוגיין."
Q3_B = (r"יוגיין בוחר באקראי מספר בין $1$ ל-$N$ ואסתר מנחשת באקראי ובאופן בלתי תלוי מספר בין $1$ ל-$M$. "
        r"ראש בית הספר למדעי המתמטיקה מנחש מהו מספרו של יוגיין ומהו מספרה של אסתר.")
Q3_OMEGA = r"""מרחב המדגם הוא כל זוגות (ניחוש, מספר):
$$\Omega=\{(1,1),(1,2),\ldots,(1,N),(2,1),\ldots,(N,N)\},\qquad|\Omega|=N^2,$$
וכל זוג שווה הסתברות."""

questions.append(Q(
    3, "א", "combinatorics",
    Q3_A + "\n" + r"**א-1:** מהי ההסתברות שראש בית הספר ינחש נכון את מספרו של יוגיין?",
    r"""**ניחוש נכון.**
""" + Q3_OMEGA + r"""
הניחוש נכון בדיוק ב-$N$ זוגות (הזוגות $(i,i)$), ולכן
$$P(\text{correct})=\frac{|\{\cdots\}|}{|\Omega|}=\frac N{N^2}=\frac1N.$$""",
    5))

questions.append(Q(
    3, "ב", "combinatorics",
    Q3_A + "\n" + r"**א-2:** מהי ההסתברות שראש בית הספר ינחש **מספר שכן**?",
    r"""**ניחוש של מספר שכן.**
""" + Q3_OMEGA + r"""
הניחוש הוא מספר שכן אם ההפרש בין הניחוש למספר הוא $1$ בערך מוחלט. לכל מספר $i$ יש שני שכנים, $i-1$ ו-$i+1$, מלבד המספרים $1$ ו-$N$ שלכל אחד מהם שכן אחד בלבד. לכן יש $1+1+2(N-2)=2(N-1)$ זוגות מתאימים, ו-
$$P(\text{neighbour})=\frac{2(N-1)}{N^2}.$$""",
    5))

questions.append(Q(
    3, "ג", "combinatorics",
    Q3_B + "\n" + r"**ב-1:** מהי ההסתברות שראש בית הספר ינחש נכון את שני המספרים, של יוגיין ושל אסתר?",
    r"""**ניחוש נכון של שני המספרים.**
שני הניחושים בלתי תלויים (אין קשר בין בחירת יוגיין לבחירת אסתר), ולכן
$$P=\frac1N\cdot\frac1M.$$""",
    5))

questions.append(Q(
    3, "ד", "combinatorics",
    Q3_B + "\n" + r"**ב-2:** מהי ההסתברות שראש בית הספר ינחש נכון **לפחות אחד** המספרים?",
    r"""**לפחות ניחוש נכון אחד.**
נסמן $A_1=\{$ראש בית הספר מנחש נכון את מספרו של יוגיין$\}$ ו-$A_2=\{$ראש בית הספר מנחש נכון את מספרה של אסתר$\}$. אלה מאורעות בלתי תלויים, ולכן
$$P(A_1\cup A_2)=P(A_1)+P(A_2)-P(A_1)P(A_2)=\frac1N+\frac1M-\frac1{NM}.$$
באופן חלופי:
$$P(A_1\cup A_2)=1-P(\bar A_1\cap\bar A_2)=1-P(\bar A_1)P(\bar A_2)=1-\left(1-\frac1N\right)\left(1-\frac1M\right),$$
כמובן, אותה תשובה.""",
    5))

questions.append(Q(
    3, "ה", "combinatorics",
    Q3_B + "\n" + r"**ב-3:** מהי ההסתברות שראש בית הספר ינחש נכון את מספרו של יוגיין וכן **מספר שכן** של אסתר?",
    r"""**מספרו של יוגיין וגם מספר שכן של אסתר.**
שני הניחושים בלתי תלויים; ההסתברות לנחש מספר שכן של אסתר מחושבת כמו בסעיף א-2 עם $M$ במקום $N$:
$$P=\frac1N\cdot\frac{2(M-1)}{M^2}.$$""",
    5))

# ------------------------------------------------------------------ Q4
Q4_FX = (r"משתנה מקרי $X$, בעל תוחלת $\mu=\mathbb{E}[X]$, מתואר על ידי פונקציית צפיפות ההסתברות מהצורה" "\n"
         r"$$f_X(x)=\begin{cases}a,&x<-1;\\bx+c,&-1\le x<0;\\d,&0\le x<1;\\g/x+h,&x\ge1.\end{cases}$$"
         "\n" r"כמו כן, נתון כי $P(X<0)=P(X>0)$.")

questions.append(Q(
    4, "א", "continuous_rv",
    r"אנא מצאו את המקדמים $a$, $b$, $c$, $d$, $g$ ו-$h$. ייתכן ותשובותיך יכללו את $\mu$.",
    r"""**מציאת המקדמים.**
נתחיל מתכונת הנרמול:
$$1=\int_{-\infty}^{\infty}f_X(x)\,dx=\int_{-\infty}^{-1}a\,dx+\int_{-1}^0(bx+c)\,dx+\int_0^1d\,dx+\int_1^{\infty}\left(\frac gx+h\right)dx.$$
• האינטגרל $\int_{-\infty}^{-1}a\,dx$ מתכנס רק אם $a=0$.
• האינטגרל $\int_1^{\infty}\left(\frac gx+h\right)dx$ מתכנס רק אם $g=0$ ו-$h=0$.
לכן
$$1=\int_{-1}^0(bx+c)\,dx+d\ \Longrightarrow\ c-\frac b2+d=1.$$
מהנתון $P(X<0)=P(X>0)$, כאשר $P(X<0)=\int_{-1}^0(bx+c)\,dx=c-\frac b2$ ו-$P(X>0)=\int_0^1d\,dx=d$, מתקבל
$$c-\frac b2=d.$$
יחד עם המשוואה הקודמת:
$$\begin{cases}c-\frac b2=\frac12\\d=\frac12\end{cases}\qquad(*)$$
נשתמש גם בתוחלת:
$$\mu=\mathbb{E}[X]=\int_{-1}^0(bx+c)x\,dx+\int_0^1d\,x\,dx=\left(\frac b3-\frac c2\right)+\frac d2,$$
ולכן
$$\frac{2b}3+d-c=2\mu.\qquad(**)$$
מפתרון המשוואות מתקבל $b=12\mu$ ו-$c=6\mu+\frac12$. בסך הכול:
$$a=0,\quad g=0,\quad h=0,\quad d=\frac12,\quad b=12\mu,\quad c=6\mu+\frac12.$$""",
    8, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"שרטטו את פונקציית הצפיפות אשר מצאת בסעיף הקודם. מהו הערך הקטן והגדול ביותר של התוחלת $\mu$? נמקו!",
    r"""**התחום של $\mu$.**
בסעיף הקודם קיבלנו
$$f_X(x)=\begin{cases}0,&x<-1\\12\mu\,x+6\mu+\frac12,&-1\le x<0\\\frac12,&0\le x<1\\0,&x\ge1\end{cases}$$
![סקיצה של f_X: ישר בין x=-1 ל-x=0 מהגובה 1/2 פחות 6μ עד 6μ ועוד 1/2, ואחר כך קבוע 1/2 בין 0 ל-1](images/exams/25B-B-Q4-pdf.png)
צפיפות חייבת לקיים $f_X(x)\ge0$, ולכן (הצפיפות ליניארית ב-$[-1,0]$ ולכן מספיק לבדוק את קצותיה):
$$\begin{cases}\frac12-6\mu\ge0\\6\mu+\frac12\ge0\end{cases}\quad\Longrightarrow\quad-\frac1{12}\le\mu\le\frac1{12}.$$""",
    5, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"בהינתן הפרמטרים מסעיף א׳, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את התוצאה. לצורכי השרטוט עליך להניח כי $\mu>0$.",
    r"""**פונקציית ההתפלגות המצטברת.**
$$F_X(t)=\begin{cases}0,&t<-1\\\dfrac12(t+1)(12\mu t+1),&-1\le t<0\\\dfrac{t+1}2,&0\le t<1\\1,&t\ge1\end{cases}$$
(בענף $-1\le t<0$: $\int_{-1}^t\left(12\mu x+6\mu+\frac12\right)dx=\frac12(t+1)(12\mu t+1)$; בנקודה $t=0$ מתקבל $\frac12$.)
![גרף F_X(t) עבור μ חיובי: עולה קמורה עד 1/2 ב-t=0 ואז ישר עד 1 ב-t=1](images/exams/25B-B-Q4-cdf.png)
(השרטוט הוא עבור $\mu>0$.)""",
    8, contextId="c4"))

questions.append(Q(
    4, "ד", "conditional_bayes",
    r"מהי ההסתברות המותנית $P(X<0\,/\,X>-1/2)$?",
    r"""**$P(X<0\mid X>-\frac12)$.**
$$P\left(X<0\ \Big/\ X>-\frac12\right)=\frac{P\left(-\frac12<X<0\right)}{P\left(X>-\frac12\right)}=\frac{F_X(0)-F_X\left(-\frac12\right)}{1-F_X\left(-\frac12\right)}.$$
כאן $F_X\left(-\frac12\right)=\frac14(1-6\mu)$ ו-$F_X(0)=\frac12$, ולכן
$$P\left(X<0\ \Big/\ X>-\frac12\right)=\frac{1+6\mu}{3+6\mu}.$$""",
    4, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_CAP = (r"לפניך מעגל חשמלי ($Q_0$) המורכב מיחידות $A$, $B$ ו-$C$ הפועלות ללא תלות אחת בשנייה בהסתברויות הזהות $p$. "
          r"במעגל $Q_0$ היחידות $A$ ו-$B$ בטור זו עם זו, ובמקביל להן היחידה $C$.")
Q5_B = (r"מפרקים מעגל $Q_0$ ומרכיבים – מאותן היחידות $A$, $B$ ו-$C$ – מעגל חדש **עם מבנה (טופולוגיה) זהה**. בין היתר, יכול להתקבל אותו מעגל בדיוק ($Q_0$) "
        r"אך יכול להתקבל גם מעגל עם היחידות $A$, $B$ ו-$C$ שנמצאות במקומות אחרים, כגון:" "\n"
        r"![דוגמה לאחת האפשרויות למעגל החדש: A ו-C בטור זו עם זו, ובמקביל להן B](images/exams/25B-B-Q5-example.png)" "\n"
        r"(שימו לב, כי אין מידע על מיקום המצאות מדויק של כל יחידה ויחידה!)")

questions.append(Q(
    5, "א", "circuits",
    r"מהי ההסתברות שמעגל זה פועל?",
    r"""**$P(Q_0)$.**
$$P(Q_0)=P\bigl((A\cap B)\cup C\bigr)=p^2+p-p^3=p\,(1+p-p^2).$$""",
    3, contextId="c5"))

questions.append(Q(
    5, "ב", "circuits",
    Q5_B + "\n" + r"**ב-1:** מהי ההסתברות שמעגל חדש ספציפי (כגון המתואר בדוגמה מעלה) יפעל?",
    r"""**מעגל חדש ספציפי.**
הסתברות הפעולה של המעגל הכללי שבו שתי יחידות בטור ובמקביל להן יחידה שלישית אינה תלויה בזהות היחידות (כולן בעלות אותה הסתברות), ולכן עבור מעגל חדש ספציפי נקבל
$$p\,(1+p-p^2).$$""",
    3, contextId="c5"))

questions.append(Q(
    5, "ג", "circuits",
    Q5_B + "\n" + r"**ב-2:** מהי ההסתברות שגם המעגל המקורי וגם המעגל החדש (עם מיקום יחידות לא ידוע מראש) יפעלו?",
    r"""**$P(Q_0\cap Q')$.**
נסמן את מקומות המעגל: $R_1$ ו-$R_2$ הם שני המקומות בטור, ו-$L_1$ הוא המקום המקביל להם. שש האפשרויות לשיבוץ $A,B,C$ הן בעלות הסתברות שווה:
$$\begin{array}{c|ccc|c}\text{No.}&R_1&R_2&L_1&\text{circuit}\\\hline\mathrm{I}&A&B&C&Q_1=Q_0\\\mathrm{II}&B&A&C&Q_2=Q_0\\\mathrm{III}&A&C&B&Q_3\\\mathrm{IV}&C&A&B&Q_4=Q_3\\\mathrm{V}&B&C&A&Q_5\\\mathrm{VI}&C&B&A&Q_6=Q_5\end{array}$$
המעגל החדש הוא $Q'$, ולפי נוסחת ההסתברות השלמה על השיבוץ:
$$P(Q_0\cap Q')=P(Q_0\cap Q'/\mathrm{I})P(\mathrm{I})+P(Q_0\cap Q'/\mathrm{II})P(\mathrm{II})+\cdots+P(Q_0\cap Q'/\mathrm{VI})P(\mathrm{VI}),\qquad P(\mathrm{I})=\cdots=P(\mathrm{VI})=\frac16.\qquad(\dagger)$$
• $P(Q_0\cap Q'/\mathrm{I})=P(Q_0\cap Q_1)=P(Q_0)=p(1+p-p^2)$, וכך גם עבור II (כי $Q_1=Q_2=Q_0$).
• עבור III: $P(Q_0\cap Q_3)$, כאשר $Q_0=(A\cap B)\cup C$ ו-$Q_3=(A\cap C)\cup B$. נפעל לפי $B$:
$$P(Q_0\cap Q_3)=P(Q_0\cap Q_3/B)P(B)+P(Q_0\cap Q_3/\bar B)P(\bar B)=P(A\cup C)\,p+P(A\cap C)(1-p)=p(2p-p^2)+p^2(1-p)=3p^2-2p^3.$$
(בהינתן $B$: $Q_3$ מתקיים מאליו ו-$Q_0=A\cup C$; בהינתן $\bar B$: $Q_0=C$ ו-$Q_3=A\cap C$.)
• עבור IV: $Q_4=Q_3$, ולכן $3p^2-2p^3$. עבור V ו-VI ($Q_5=Q_6=(B\cap C)\cup A$): בהתניה על $A$ מקבלים $P(B\cup C)\,p+P(B\cap C)(1-p)$, ושוב $3p^2-2p^3$.
הצבה ב-$(\dagger)$:
$$P(Q_0\cap Q')=\frac16\Bigl\{2\bigl(p+p^2-p^3\bigr)+4\bigl(3p^2-2p^3\bigr)\Bigr\}=\frac p3\left(1+7p-5p^2\right).$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ד", "conditional_bayes",
    Q5_B + "\n" + r"**ב-3:** אם ידוע כי המעגל המקורי ($Q_0$) פעל, מה ההסתברות שגם המעגל החדש (עם מיקום יחידות לא ידוע מראש) יפעל?",
    r"""**$P(Q'/Q_0)$.**
$$P(Q'/Q_0)=\frac{P(Q_0\cap Q')}{P(Q_0)}=\frac{\frac p3(1+7p-5p^2)}{p(1+p-p^2)}=\frac{1+7p-5p^2}{3\,(1+p-p^2)}.$$""",
    5, contextId="c5"))

questions.append(Q(
    5, "ה", "conditional_bayes",
    Q5_B + "\n" + r"**ב-4:** אם ידוע כי המעגל המקורי ($Q_0$) **לא** פעל, מה ההסתברות שהמעגל החדש (עם מיקום יחידות לא ידוע מראש) כן יפעל?",
    r"""**$P(Q'/\bar Q_0)$.**
$$P(Q'/\bar Q_0)=\frac{P(Q'\cap\bar Q_0)}{P(\bar Q_0)}=\frac{P(Q')-P(Q'\cap Q_0)}{1-P(Q_0)}=\frac{2p}{3\,(1+p)}.$$
(כאן $P(Q')=P(Q_0)=p(1+p-p^2)$, כי לכל שיבוץ אותה הסתברות פעולה.)""",
    4, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_CAP = (r"נתונים שני כדים: הראשון מכיל $N_1$ כדורים ובניהם $D_1$ כדורים אדומים. השני מכיל $N_2$ כדורים ובניהם $D_2$ כדורים אדומים.")
Q6_A = r"מהכד הראשון, נלקחו באקראי $n$ כדורים והוספו לכד השני. לאחר מכן, כדור אחד נלקח מהכד השני."

questions.append(Q(
    6, "א", "special_discrete",
    Q6_A + "\n" + r"**א-1:** מהי ההסתברות שצבעו אדום? (נא להניח כי $n\le N_1$).",
    r"""**$P(\text{red})$.**
נסמן ב-$X$ את מספר הכדורים האדומים בין $n$ הכדורים שהועברו; $X$ מתפלג היפרגיאומטרית, ו-$\mathbb{E}[X]=n\frac{D_1}{N_1}$. בהינתן $X=k$ בכד השני יש $N_2+n$ כדורים, מהם $D_2+k$ אדומים. לפי ההסתברות השלמה:
$$P(\text{red})=\sum_kP(\text{red}/X=k)P(X=k)=\frac{D_2+\mathbb{E}[X]}{N_2+n}=\frac{D_2+n\dfrac{D_1}{N_1}}{N_2+n}.$$""",
    15, contextId="c6"))

questions.append(Q(
    6, "ב", "conditional_bayes",
    Q6_A + "\n" + r"**א-2:** אם ידוע כי צבעו של הכדור שנלקח מהכד השני היה אדום, מהי ההסתברות שכל הכדורים שהוצאו קודם לכן מהכד הראשון היו אדומים?",
    r"""**$P(X=n/\text{red})$.**
נסמן ב-$X$ את מספר הכדורים האדומים בין $n$ שנלקחו מהכד הראשון. לפי נוסחת בייס:
$$P(X=n/\text{red})=\frac{P(\text{red}/X=n)\,P(X=n)}{P(\text{red})}.$$
כאן $P(\text{red}/X=n)=\dfrac{D_2+n}{N_2+n}$ ו-$X\sim\mathrm{Hyp}(D_1,N_1,n)$, כלומר
$$P(X=k)=\frac{\binom{D_1}{k}\binom{N_1-D_1}{n-k}}{\binom{N_1}{n}},\qquad P(X=n)=\frac{\binom{D_1}{n}}{\binom{N_1}{n}}.$$
הצבה:
$$P(X=n/\text{red})=\frac{D_2+n}{D_2+n\dfrac{D_1}{N_1}}\cdot\frac{\binom{D_1}{n}}{\binom{N_1}{n}}.$$""",
    5, contextId="c6"))

questions.append(Q(
    6, "ג", "special_discrete",
    r"מהכד הראשון, נלקחו באקראי $n$ כדורים, **צבעיהם הוחלפו** (כל כדור אדום נצבע בשחור וכל כדור שחור נצבע באדום) ורק אז הוספו לכד השני. לאחר מכן, כדור אחד נלקח מהכד השני. מהי ההסתברות שצבעו אדום? (נא להניח כי $n\le N_1$).",
    r"""**כדורים שצבעיהם הוחלפו.**
כעת כל כדור שהועבר הוא אדום בדיוק כאשר הוא היה שחור בכד הראשון, ולכן מספר הכדורים האדומים שהועברו הוא $n-X$ (עם $\mathbb{E}[n-X]=n\left(1-\frac{D_1}{N_1}\right)$). בדומה לסעיף א-1:
$$P(\text{red})=\frac{D_2+n\left(1-\dfrac{D_1}{N_1}\right)}{N_2+n}.$$""",
    5, contextId="c6"))

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר ב׳ תשפ״ה, מועד ב (12.08.2025)",
    "year": 2025,
    "examDate": "12.08.2025",
    "sourceFile": "25B-B exam pp.1-3",
    "solutionFile": "25B-B handwritten official solutions pp.4-17",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: חליל", "image": IMG + "Q1-flute.png", "caption": Q1_CAP},
        "c2": {"kind": "text", "title": "שאלה 2: מאורעות", "text": Q2_CAP},
        "c4": {"kind": "text", "title": "שאלה 4", "text": Q4_FX},
        "c5": {"kind": "image", "title": "שאלה 5: מעגל", "image": IMG + "Q5-q0.png", "caption": Q5_CAP},
        "c6": {"kind": "image", "title": "שאלה 6: שני כדים", "image": IMG + "Q6-urns.png", "caption": Q6_CAP},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
