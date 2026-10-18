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
- Q2 part ו (bonus, disjoint events) TYPO RULING (arbiter 2026-10-18, the printed question wins): the official answer
  is s = q, but s = q makes P(B) = 0, so P(not-A | B) = p would be undefined; with P(B) > 0 disjointness forces
  p = 1 (q < s free). Shipped p = 1 with the official method (P(A and B) = (1-p)(s-q)/(1-q) = 0, the factor 1-p),
  solutionSource "solved", official:false, "הפתרון הרשמי עם תיקון" prefix; verified in tools/verify/25B-B/check.py.
- Q3: the head of the school guesses at random; as in the official solution the sample space is the N^2 equally likely
  (guess, number) pairs.
- Q6 part א-1/ב: the official solution is a formula that refers to the practice sheet; the one-line derivation (total
  probability over the number X of red balls moved) is added so that the item is self-contained.
- Q1 parts b, c, d carry `region` data (REGIONS below; moved from tools/verify/25B-B/regions.json) and every simulable part a `sim`.
- The page-1 cover (lecturer names) is not copied anywhere.
"""
import json, math, pathlib
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from verified import src as _vsrc
from fractions import Fraction as Fr

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

questions.append(Q(
    2, "ו", "independence",
    r"**סעיף בונוס:** עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו **זרים**? (5 נק׳ – הניקוד יינתן עבור פתרון מלא בלבד.)",
    r"""**הפתרון הרשמי עם תיקון:** בפתרון הרשמי התשובה היא $s=q$. אבל עבור $s=q$ מתקבל $P(B)=\frac{s-q}{1-q}=0$, ואז $P(\bar A/B)=p$ אינה מוגדרת, בניגוד לנתון. הגורם שמתאפס חייב להיות $1-p$, ולכן התשובה הנכונה היא $p=1$. התיקון נבדק (חישוב מדויק וסימולציה).
**מאורעות זרים.**
$A$ ו-$B$ זרים אם ורק אם $P(A\cap B)=0$. מסעיף א-3,
$$P(A\cap B)=(1-p)\,\frac{s-q}{1-q}=(1-p)\,P(B).$$
מאחר שהנתון $P(\bar A/B)=p$ מוגדר, $P(B)>0$, כלומר $s>q$ (ראו גם סעיף ב). לכן המכפלה מתאפסת רק כאשר
$$p=1,$$
כלומר $P(\bar A/B)=1$: כאשר $B$ מתרחש, $A$ לא מתרחש. הפרמטרים $q$ ו-$s$ חופשיים (עם $q<s$); למשל $p=1$, $q=\frac5{16}$, $s=\frac9{20}$ מתאימים לזוג מאורעות זרים.""",
    5, contextId="c2", solutionSource="solved", official=False))

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

# ------------------------------------------------------------------ area regions (RAW_SCHEMA `region`; moved from tools/verify/25B-B/regions.json)
U11 = {"x": [0, 1], "y": [0, 1]}
XL = {"x": "X1", "y": "X2"}
REGIONS = {
    (1, "ב"): {"space": U11, "labels": XL, "event": [{"a": -1, "b": 1, "c": -0.5, "op": ">"}, {"a": -1, "b": 1, "c": 0.5, "op": "<"}], "exact": 0.75,
               "caption": "הרצועה |x1-x2|<1/2"},
    (1, "ג"): {"space": U11, "labels": XL, "event": {"any": [[{"a": 1, "b": -1, "c": 1.5, "op": ">"}], [{"a": -1, "b": 1, "c": 1.5, "op": ">"}]]}, "exact": 0.0,
               "caption": "האזור |x1-x2|>3/2 ריק"},
    (1, "ד"): {"space": U11, "labels": XL, "event": [{"a": 1, "b": -1, "c": 0.4, "op": "<="}, {"a": -1, "b": 1, "c": 0.4, "op": "<="}], "exact": 0.64,
               "caption": "הרצועה |x1-x2|<=t עבור t=0.4 (שטח 2t-t^2)"},
}
for _q in questions:
    _r = REGIONS.get((_q["num"], _q.get("part")))
    if _r is not None:
        _q["region"] = _r

# ------------------------------------------------------------------ simulations (RAW_SCHEMA `sim`)
# Symbolic answers are simulated at a stated sample value (given in each `estimate`). Not simulated: Q1 part א (a
# distribution statement), Q2 part ד (an impossibility argument), Q4 part ב (a range of mu).
def J(pAB, pAnB, pnAB, pnAnB):
    return [{"p": pAB, "A": 1, "B": 1}, {"p": pAnB, "A": 1, "B": 0}, {"p": pnAB, "A": 0, "B": 1}, {"p": pnAnB, "A": 0, "B": 0}]


def uni(lo, hi):
    n = hi - lo + 1
    return {"values": list(range(lo, hi + 1)), "probs": [1 / n] * n}


# Q2: p=P(not A|B)=0.4, q=P(A|not B)=0.2, s=P(A or B)=0.7  =>  P(B)=0.625, P(A and B)=0.375, P(A)=0.45
_J2 = J(0.375, 0.075, 0.25, 0.3)
_PDF1 = {"pieces": [{"from": 0, "to": 1, "expr": "2*(1-x)"}]}
# Q4: mu = 1/24  =>  b = 12 mu = 1/2, c = 6 mu + 1/2 = 3/4, d = 1/2
_PDF4 = {"pieces": [{"from": -1, "to": 0, "expr": "0.5*x+0.75"}, {"from": 0, "to": 1, "expr": "0.5"}]}
_GUESS = {"vars": {"gE": uni(1, 3), "nE": uni(1, 3), "gS": uni(1, 4), "nS": uni(1, 4)}}
_Q0 = "A*B + C > 0"
_QP = "((K <= 2 and A*B + C > 0) or ((K == 3 or K == 4) and A*C + B > 0) or (K >= 5 and B*C + A > 0))"
_Q5 = {"vars": {"A": {"values": [0, 1], "probs": [0.4, 0.6]}, "B": {"values": [0, 1], "probs": [0.4, 0.6]},
                "C": {"values": [0, 1], "probs": [0.4, 0.6]}, "K": uni(1, 6)}}
_P0 = 0.6 * (1 + 0.6 - 0.36)               # 0.744
_P0P = 0.6 / 3 * (1 + 7 * 0.6 - 5 * 0.36)   # 0.68
# Q6: N1=6 (D1=4 red), N2=4 (D2=1 red), n=3 balls moved
_HYP = {1: 4 / 20, 2: 12 / 20, 3: 4 / 20}   # P(X=k), X = red balls moved


def _joint6(xval, red_of):
    rows = []
    for k, w in _HYP.items():
        pr = red_of(k) / 7
        rows.append({"p": w * pr, "X": xval(k), "R": 1})
        rows.append({"p": w * (1 - pr), "X": xval(k), "R": 0})
    return rows


SIMS = {
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(|X1-X2|<1/2)", "exact": 0.75},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(|X1-X2|>3/2)", "exact": 0.0},
    (1, "ד"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "F_X(0.4)=P(|X1-X2|<=0.4)", "exact": 0.64},
    (1, "ה"): {"kind": "pdf", "params": dict(_PDF1, event="x > 0.2 and x < 0.6"), "estimate": "P(0.2<X<0.6)=F(0.6)-F(0.2)", "exact": 0.48},
    (1, "ו"): {"kind": "pdf", "params": dict(_PDF1, measure="mean", expr="x"), "estimate": "E[X]", "exact": 1 / 3},
    (2, "א"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 1"}, "estimate": "P(A) ב-p=0.4,q=0.2,s=0.7", "exact": 0.45},
    (2, "ב"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "B == 1"}, "estimate": "P(B) ב-p=0.4,q=0.2,s=0.7", "exact": 0.625},
    (2, "ג"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 1 and B == 1"}, "estimate": "P(A and B) ב-p=0.4,q=0.2,s=0.7", "exact": 0.375},
    # independent: p=1-q=0.8, q=0.2, s=0.6  =>  P(A)=0.2, P(B)=0.5, P(A and B)=0.1=P(A)P(B)
    (2, "ה"): {"kind": "custom_discrete", "params": {"joint": J(0.1, 0.1, 0.4, 0.4), "event": "A == 1 and B == 1"}, "estimate": "P(A and B)=P(A)P(B) ב-p=0.8,q=0.2,s=0.6", "exact": 0.1},
    # disjoint (corrected): p=1, q=5/16, s=9/20  =>  P(A or B)=P(A)+P(B)=s
    (2, "ו"): {"kind": "custom_discrete", "params": {"joint": J(0.0, 0.25, 0.2, 0.55), "event": "A == 1 or B == 1"}, "estimate": "P(A or B)=P(A)+P(B) ב-p=1,q=5/16,s=9/20", "exact": 0.45},
    # Q3: N=6 for a, b; N=3 (Eugene) and M=4 (Esther) for c-e
    (3, "א"): {"kind": "dice", "params": {"n": 2, "faces": 6, "event": "d1 == d2"}, "estimate": "P(correct guess) ב-N=6", "exact": 1 / 6},
    (3, "ב"): {"kind": "dice", "params": {"n": 2, "faces": 6, "event": "abs(d1 - d2) == 1"}, "estimate": "P(neighbour) ב-N=6", "exact": 10 / 36},
    (3, "ג"): {"kind": "custom_discrete", "params": dict(_GUESS, event="gE == nE and gS == nS"), "estimate": "P(both correct) ב-N=3,M=4", "exact": 1 / 12},
    (3, "ד"): {"kind": "custom_discrete", "params": dict(_GUESS, event="gE == nE or gS == nS"), "estimate": "P(at least one correct) ב-N=3,M=4", "exact": 1 / 3 + 1 / 4 - 1 / 12},
    (3, "ה"): {"kind": "custom_discrete", "params": dict(_GUESS, event="gE == nE and abs(gS - nS) == 1"), "estimate": "P(Eugene correct, Esther neighbour) ב-N=3,M=4", "exact": 1 / 3 * 6 / 16},
    # Q4 at mu = 1/24
    (4, "א"): {"kind": "pdf", "params": dict(_PDF4, measure="mean", expr="x"), "estimate": "E[X]=mu ב-mu=1/24", "exact": 1 / 24},
    (4, "ג"): {"kind": "pdf", "params": dict(_PDF4, event="x <= -0.5"), "estimate": "F_X(-1/2) ב-mu=1/24", "exact": 0.1875},
    (4, "ד"): {"kind": "pdf", "params": dict(_PDF4, event="x < 0", given="x > -0.5"), "estimate": "P(X<0 | X>-1/2) ב-mu=1/24", "exact": 5 / 13},
    # Q5 at p=0.6
    (5, "א"): {"kind": "circuit", "params": {"network": {"type": "parallel", "children": [
        {"type": "series", "children": [{"type": "comp", "id": "A", "p": 0.6}, {"type": "comp", "id": "B", "p": 0.6}]}, {"type": "comp", "id": "C", "p": 0.6}]}, "event": "S"},
        "estimate": "P(Q0) ב-p=0.6", "exact": _P0},
    (5, "ב"): {"kind": "circuit", "params": {"network": {"type": "parallel", "children": [
        {"type": "series", "children": [{"type": "comp", "id": "A", "p": 0.6}, {"type": "comp", "id": "C", "p": 0.6}]}, {"type": "comp", "id": "B", "p": 0.6}]}, "event": "S"},
        "estimate": "P(Q') למעגל החדש הספציפי ב-p=0.6", "exact": _P0},
    (5, "ג"): {"kind": "custom_discrete", "params": dict(_Q5, event=_Q0 + " and " + _QP), "estimate": "P(Q0 and Q') ב-p=0.6", "exact": _P0P},
    (5, "ד"): {"kind": "custom_discrete", "params": dict(_Q5, event=_QP, given=_Q0), "estimate": "P(Q'|Q0) ב-p=0.6", "exact": _P0P / _P0},
    (5, "ה"): {"kind": "custom_discrete", "params": dict(_Q5, event=_QP, given="A*B + C == 0"), "estimate": "P(Q'|not Q0) ב-p=0.6", "exact": 2 * 0.6 / (3 * 1.6)},
    # Q6: N1=6 (D1=4), N2=4 (D2=1), n=3
    (6, "א"): {"kind": "custom_discrete", "params": {"joint": _joint6(lambda k: k, lambda k: 1 + k), "event": "R == 1"}, "estimate": "P(red) ב-N1=6,D1=4,N2=4,D2=1,n=3", "exact": 3 / 7},
    (6, "ב"): {"kind": "custom_discrete", "params": {"joint": _joint6(lambda k: k, lambda k: 1 + k), "event": "X == 3", "given": "R == 1"}, "estimate": "P(X=n | red) ב-N1=6,D1=4,N2=4,D2=1,n=3", "exact": 4 / 15},
    (6, "ג"): {"kind": "custom_discrete", "params": {"joint": _joint6(lambda k: 3 - k, lambda k: 1 + 3 - k), "event": "R == 1"},
               "estimate": "P(red) אחרי החלפת צבעים ב-N1=6,D1=4,N2=4,D2=1,n=3", "exact": 2 / 7},
}
for _q in questions:
    _s = SIMS.get((_q["num"], _q.get("part")))
    if _s is not None:
        _q["sim"] = _s

# ------------------------------------------------------------------ rubric / pitfalls / steps (ai-draft)
# Every expected value is re-derived independently (exact fractions / enumeration / sympy, and Monte Carlo where a kind
# applies) in tools/verify/25B-B/steps_check.py, which reads the generated raw JSON back. The steps of Q2 part ו follow
# the CORRECTED solution (p = 1).
FRAC = 0.0006   # tolerance when the answer is a non-terminating value entered as a 3-4 digit decimal


def O(*v):
    return [{"id": "abcdefgh"[i], "value": t} for i, t in enumerate(v)]


def CH(prompt, opts, ans, explain):
    return {"type": "choice", "prompt": prompt, "options": O(*opts), "correctId": "abcdefgh"[ans], "explain": explain}


def NU(prompt, val, explain, region=None):
    a = round(float(val), 4)
    exact = abs(a - float(val)) < 1e-12
    s = {"type": "numeric", "prompt": prompt + ("" if exact else " (שבר או עשרוני)"), "answer": a,
         "tol": 0 if exact else FRAC, "explain": explain}
    if region is not None:
        s["region"] = region
    return s


def RB(*r):
    return [{"text": t, "points": p} for t, p in r]


S = {}


def ADD(num, part, rub, pit, steps):
    S[(num, part)] = (rub, pit, steps)


OMEGA = r"מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X_1,X_2)$, כאשר $X_1,X_2\sim U(0,1)$ בלתי תלויים?"
OMEGA_X = r"ריבוע היחידה $(0,1)^2$ הוא מרחב המדגם, ושטחו $1$, לכן ההסתברות שווה לשטח האירוע."

ADD(1, "א",
    RB((r"הנקודה נבחרת אחיד לאורך החליל: $X_i\sim U_c(0,1)$", 2), (r"הבחירות בלתי תלויות, ולכן $X_1,X_2$ בלתי תלויים", 1), (r"נימוק: אורך החליל $1$ מ'", 1)),
    [r"לתאר את ההתפלגות בלי לנמק מדוע היא אחידה", r"לשכוח לציין אי-תלות"],
    [NU(r"מהי צפיפות ההסתברות $f_{X_1}(0.3)$ של נקודה שנבחרת אחיד על חליל באורך $1$?", 1, r"$f(x)=1$ על $(0,1)$."),
     NU(r"מהי $P(X_1\le0.25)$?", Fr(1, 4), r"$F(t)=t$ על $(0,1)$, לכן $0.25$.")])

ADD(1, "ב",
    RB((r"גישה גאומטרית: מרחב המדגם ריבוע היחידה", 1), (r"האירוע הוא רצועה, והמשלים שני משולשים עם ניצבים $\frac12$", 2), (r"התשובה $\frac34$", 1)),
    [r"לחשב רק משולש אחד של המשלים ולקבל $\frac78$", r"לשכוח שהרצועה סימטרית סביב האלכסון"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח אחד משני המשולשים מחוץ לרצועה $|x_1-x_2|<\frac12$?", Fr(1, 8), r"ניצבים $\frac12$ ו-$\frac12$: $\frac12\cdot\frac14=\frac18$.", region=REGIONS[(1, "ב")]),
     NU(r"מהי $P(|X_1-X_2|<\frac12)$?", Fr(3, 4), r"$1-2\cdot\frac18=\frac34$.")])

ADD(1, "ג",
    RB((r"טווח $|X_1-X_2|$ הוא $[0,1)$", 2), (r"הרצועה $|x_1-x_2|\le\frac32$ מכסה את כל הריבוע", 1), (r"התשובה $0$", 1)),
    [r"לחשב שטח של משולש 'גדול' מחוץ לריבוע"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו הערך הגדול ביותר האפשרי של $|X_1-X_2|$ (בכל זוג נקודות על חליל באורך $1$)?", 1, r"שתי נקודות על קטע באורך $1$ נמצאות במרחק של לכל היותר $1$."),
     NU(r"מהי $P(|X_1-X_2|>\frac32)$?", 0, r"$\frac32>1$, לכן האירוע ריק ושטחו $0$.", region=REGIONS[(1, "ג")])])

ADD(1, "ד",
    RB((r"$F_X(t)=0$ עבור $t<0$ ו-$1$ עבור $t\ge1$", 2), (r"עבור $0\le t<1$: משלים של שני משולשים עם ניצבים $1-t$", 4), (r"$F_X(t)=2t-t^2$", 2)),
    [r"להשתמש בניצבים $t$ במקום $1-t$", r"לשכוח את הכפל ב-$2$ (שני משולשים)"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"עבור $t=0.4$: מהו שטח אחד משני המשולשים מחוץ לרצועה (ניצבים $1-t$)?", 0.18, r"$\frac12(0.6)^2=0.18$.", region=REGIONS[(1, "ד")]),
     NU(r"מהו $F_X(0.4)=1-2\cdot\frac{(1-t)^2}2$?", 0.64, r"$1-0.36=0.64=2t-t^2$."),
     NU(r"מהו $F_X(1)$?", 1, r"$2-1=1$: הנוסחה מתחברת ל-$1$ ב-$t=1$.")])

ADD(1, "ה",
    RB((r"גזירה: $f_X=F_X'$", 1), (r"$f_X(t)=2(1-t)$ על $[0,1)$", 1)),
    [r"לשכוח את האפס מחוץ ל-$[0,1)$"],
    [NU(r"מהו $f_X(0.4)$?", 1.2, r"$2(1-0.4)=1.2$."),
     NU(r"מהו $f_X(1)$?", 0, r"$2(1-1)=0$."),
     NU(r"בדיקת נרמול: מהו $\int_0^1f_X(t)\,dt$?", 1, r"שטח משולש עם בסיס $1$ וגובה $f_X(0)=2$: $1$.")])

ADD(1, "ו",
    RB((r"הצבה בהגדרה $\int tf_X(t)\,dt$", 1), (r"פירוק $2t-2t^2$", 1), (r"התוצאה $\frac13$", 1)),
    [r"לשכוח לכפול ב-$t$ בתוך האינטגרל"],
    [NU(r"מהו $\int_0^12t\,dt$?", 1, r"$t^2\big|_0^1=1$."),
     NU(r"מהו $\int_0^12t^2\,dt$?", Fr(2, 3), r"$\frac23t^3\big|_0^1=\frac23$."),
     NU(r"מהי $\mathbb{E}[X]=\int_0^1t\cdot2(1-t)\,dt$?", Fr(1, 3), r"$1-\frac23=\frac13$.")])

# Q2: sample p=0.4, q=0.2, s=0.7
Q2S = r"נקבע $p=0.4$, $q=0.2$, $s=0.7$. "
ADD(2, "א",
    RB((r"מציאת $P(B)$ מתוך $P(\overline A/\overline B)=1-q$ ו-$P(\overline A\cap\overline B)=1-s$", 2), (r"$P(A\cap B)=(1-p)P(B)$", 1), (r"$P(A)=s-pP(B)$", 2)),
    [r"להחליף בין $P(A/B)$ לבין $P(\overline A/B)$", r"לחשוב ש-$P(B)=s-q$"],
    [CH(r"כיצד מוצאים את $P(B)$ מתוך $q=P(A/\overline B)$ ו-$s=P(A\cup B)$?",
        [r"$P(\overline A\cap\overline B)=1-s$ ו-$P(\overline B)=\dfrac{1-s}{1-q}$, כלומר $P(B)=\dfrac{s-q}{1-q}$", r"$P(B)=p$", r"$P(B)=s-q$"], 0,
        r"השנייה מבלבלת בין הסתברות מותנית ללא מותנית ($0.4$ במקום $0.625$). השלישית מתעלמת מכך ש-$q$ הסתברות מותנית ב-$\overline B$ ($0.5$)."),
     NU(Q2S + r"מהי $P(B)$?", Fr(5, 8), r"$\frac{s-q}{1-q}=\frac{0.5}{0.8}=0.625$."),
     NU(r"מהי $P(A\cap B)=(1-p)P(B)$?", Fr(3, 8), r"$0.6\cdot0.625=0.375$."),
     NU(r"מהי $P(A)=P(A\cup B)-P(B)+P(A\cap B)$?", Fr(9, 20), r"$0.7-0.625+0.375=0.45$, כלומר $s-pP(B)$.")])

ADD(2, "ב",
    RB((r"$P(\overline A\cap\overline B)=1-s$ (דה-מורגן)", 2), (r"$P(\overline A/\overline B)=1-q$ ולכן $P(\overline B)=\frac{1-s}{1-q}$", 2), (r"$P(B)=\frac{s-q}{1-q}$", 1)),
    [r"לכתוב $P(\overline B)=\frac{s}{1-q}$ (בלי להחסיר מ-$1$)"],
    [CH(r"מהו $P(\overline A\mid\overline B)$ במונחי הנתונים?",
        [r"$1-q$, כי $q=P(A\mid\overline B)$", r"$q$", r"$1-p$"], 0,
        r"$q$ הוא $P(A\mid\overline B)$ ולא המשלים; $1-p$ הוא $P(A\mid B)$, התנאי השונה."),
     NU(Q2S + r"מהי $P(\overline A\cap\overline B)$?", Fr(3, 10), r"$1-s=0.3$."),
     NU(r"מהי $P(\overline B)=\frac{P(\overline A\cap\overline B)}{P(\overline A\mid\overline B)}$?", Fr(3, 8), r"$\frac{0.3}{0.8}=0.375$."),
     NU(r"מהי $P(B)$?", Fr(5, 8), r"$1-0.375=0.625$.")])

ADD(2, "ג",
    RB((r"$P(A\mid B)=1-p$", 1), (r"$P(B)=\frac{s-q}{1-q}$ מסעיף ב", 2), (r"$P(A\cap B)=(1-p)\frac{s-q}{1-q}$", 2)),
    [r"להשתמש ב-$p$ במקום $1-p$", r"לטעות בחישוב $P(B)$ מסעיף ב"],
    [NU(Q2S + r"מהי $P(B)$ (סעיף ב)?", Fr(5, 8), r"$0.625$."),
     NU(r"מהי $P(A\mid B)=1-P(\overline A\mid B)$?", Fr(3, 5), r"$1-p=0.6$."),
     NU(r"מהי $P(A\cap B)$?", Fr(3, 8), r"$0.6\cdot0.625=0.375$.")])

ADD(2, "ד",
    RB((r"$P(B)=\frac{s-q}{1-q}$ חייבת להיות $\ge0$", 3), (r"אם $q>s$ המונה שלילי והמכנה חיובי", 1), (r"מסקנה: לא ייתכן", 1)),
    [r"לענות 'כן' בלי לבדוק את סימן $P(B)$"],
    [CH(r"האם ייתכן $q>s$?",
        [r"לא: אז $P(B)=\frac{s-q}{1-q}<0$", r"כן: אין קשר בין $q$ ל-$s$", r"כן: $q>s$ נדרש כש-$A$ קשור ל-$B$"], 0,
        r"$P(\overline A\cap\overline B)=1-s=(1-q)P(\overline B)$, ולכן $P(\overline B)=\frac{1-s}{1-q}$; אם $q>s$ מתקבל $P(\overline B)>1$, וגם $P(B)<0$."),
     NU(r"עבור $q=0.5$ ו-$s=0.3$: מהו $P(B)=\frac{s-q}{1-q}$?", Fr(-2, 5), r"$\frac{-0.2}{0.5}=-0.4<0$: לא יתכן.")])

ADD(2, "ה",
    RB((r"אי-תלות: $P(A/B)=P(A/\overline B)=P(A)$", 2), (r"$P(A/B)=1-p$ ו-$P(A/\overline B)=q$", 1), (r"התנאי $p=1-q$", 2)),
    [r"לדרוש $p=q$", r"להסתפק בשוויון אחד בלבד"],
    [CH(r"איזה תנאי שקול לאי-תלות של $A$ ו-$B$ (כש-$0<P(B)<1$)?",
        [r"$P(A\mid B)=P(A\mid\overline B)$", r"$P(A\mid B)=P(B\mid A)$", r"$P(A\cap B)=0$"], 0,
        r"השני נכון רק כש-$P(A)=P(B)$. השלישי הוא זרות."),
     NU(r"עבור $q=0.2$: איזה $p$ מקיים $p=1-q$?", Fr(4, 5), r"$0.8$."),
     NU(r"באותם ערכים: מהו $P(A\mid B)-P(A\mid\overline B)=(1-p)-q$?", 0, r"$0.2-0.2=0$.")])

ADD(2, "ו",
    RB((r"זרות: $P(A\cap B)=0$", 1), (r"$P(A\cap B)=(1-p)P(B)$ ו-$P(B)>0$ כי $P(\overline A/B)$ מוגדרת", 2), (r"מסקנה (תיקון): $p=1$, ו-$s=q$ אינו מתאים", 2)),
    [r"לכתוב $s=q$ כמו בפתרון הרשמי (אז $P(B)=0$ ו-$P(\overline A\mid B)$ אינה מוגדרת)", r"לשכוח ש-$P(B)>0$ מהנתון"],
    [CH(r"מה מבטיח ש-$P(A\cap B)=(1-p)\,P(B)$ מתאפס, בהינתן ש-$P(\overline A/B)=p$ מוגדרת?",
        [r"$p=1$ (כי $P(B)>0$ מכיוון שההסתברות המותנית מוגדרת)", r"$s=q$ (כי אז $P(B)=0$)", r"$q=0$"], 0,
        r"עבור $s=q$ מתקבל $P(B)=0$, ואז $P(\overline A/B)$ אינה מוגדרת בניגוד לנתון. $q=0$ אינו מבטיח זרות."),
     NU(r"עבור $q=\frac5{16}$ ו-$s=\frac9{20}$: מהו $P(B)=\frac{s-q}{1-q}$?", Fr(1, 5), r"$\frac{11/80}{11/16}=\frac15$."),
     NU(r"עבור $p=1$: מהו $P(A)=s-pP(B)$?", Fr(1, 4), r"$\frac9{20}-\frac15=\frac14$; ואכן $P(A\cap B)=0$, $P(A)+P(B)=\frac9{20}=s$.")])

# Q3
ADD(3, "א",
    RB((r"מרחב המדגם: זוגות (ניחוש, מספר), כולם שווי הסתברות", 2), (r"$N$ זוגות מתאימים: $(i,i)$", 2), (r"התשובה $\frac1N$", 1)),
    [r"לספור רק $N$ אפשרויות ולחלק ב-$N$ בלי לזהות שהניחוש הוא אקראי"],
    [CH(r"מהו מרחב המדגם המתאים (המספר של יוגיין והניחוש של ראש בית הספר הם אקראיים)?",
        [r"כל זוגות (ניחוש, מספר), $N^2$ זוגות שווי הסתברות", r"רק המספרים $1,\ldots,N$ של יוגיין", r"כל התמורות של $1,\ldots,N$"], 0,
        r"גם הניחוש אקראי, ולכן שני הצדדים משתנים. הצד השני אינו מביא בחשבון את הניחוש; תמורות לא רלוונטיות."),
     NU(r"עבור $N=6$: מהו $|\Omega|$ (מספר הזוגות)?", 36, r"$N^2=36$."),
     NU(r"כמה זוגות מתאימים לניחוש נכון?", 6, r"הזוגות $(i,i)$: $N=6$."),
     NU(r"מהי ההסתברות לניחוש נכון?", Fr(1, 6), r"$\frac6{36}=\frac16$.")])

ADD(3, "ב",
    RB((r"הגדרת שכן: ההפרש בין הניחוש למספר הוא $1$ בערך מוחלט", 1), (r"ספירה: $2(N-1)$ זוגות", 3), (r"$\frac{2(N-1)}{N^2}$", 1)),
    [r"לספור $2N$ זוגות (שכחו שהקצוות יש להם שכן אחד)", r"לספור כל זוג פעמיים"],
    [NU(r"עבור $N=6$: מהו $|\Omega|$?", 36, r"$N^2=36$."),
     NU(r"כמה זוגות $(i,j)$ מקיימים $|i-j|=1$ עבור $N=6$?", 10, r"$2(N-1)=10$: חמישה זוגות עולים וחמישה יורדים."),
     NU(r"מהי ההסתברות לניחוש של מספר שכן?", Fr(5, 18), r"$\frac{10}{36}=\frac5{18}\approx0.2778$.")])

ADD(3, "ג",
    RB((r"בחירת יוגיין ובחירת אסתר בלתי תלויות", 2), (r"$P(A_1)=\frac1N$ ו-$P(A_2)=\frac1M$", 2), (r"מכפלה: $\frac1{NM}$", 1)),
    [r"לחבר את ההסתברויות במקום להכפיל"],
    [CH(r"איך משלבים את ההסתברויות לנחש נכון את שני המספרים?",
        [r"מכפלה, כי שני המשחקים בלתי תלויים", r"סכום $\frac1N+\frac1M$", r"המקסימום $\max(\frac1N,\frac1M)$"], 0,
        r"הסכום גדול מ-$\frac1N$ ואף יכול לעלות על $1$ (הערכים $0.583$); המקסימום מתעלם מהדרישה לשני הניחושים."),
     NU(r"עבור $N=3$, $M=4$: מהי $P(A_1)$?", Fr(1, 3), r"$\frac13$."),
     NU(r"מהי $P(A_2)$?", Fr(1, 4), r"$\frac14$."),
     NU(r"מהי $P(A_1\cap A_2)$?", Fr(1, 12), r"$\frac13\cdot\frac14=\frac1{12}\approx0.0833$.")])

ADD(3, "ד",
    RB((r"כלל החיבור: $P(A_1\cup A_2)=P(A_1)+P(A_2)-P(A_1\cap A_2)$", 2), (r"$P(A_1\cap A_2)=P(A_1)P(A_2)$", 2), (r"$\frac1N+\frac1M-\frac1{NM}$", 1)),
    [r"לחבר בלי לחסר את החיתוך", r"לחשב $1-\frac1{NM}$"],
    [CH(r"איך מחשבים את ההסתברות לנחש נכון לפחות אחד המספרים?",
        [r"$P(A_1)+P(A_2)-P(A_1\cap A_2)$", r"$P(A_1)+P(A_2)$", r"$1-P(A_1\cap A_2)$"], 0,
        r"הראשון בלבד מונע ספירה כפולה: השני נותן $0.583$, והשלישי $0.917$, במקום $0.5$."),
     NU(r"עבור $N=3$, $M=4$: מהי $P(A_1\cap A_2)$?", Fr(1, 12), r"$\frac1{12}$."),
     NU(r"מהי $P(A_1\cup A_2)$?", Fr(1, 2), r"$\frac13+\frac14-\frac1{12}=\frac12$.")])

ADD(3, "ה",
    RB((r"אי-תלות: מכפלת ההסתברויות", 2), (r"ההסתברות לנחש שכן של אסתר היא $\frac{2(M-1)}{M^2}$", 2), (r"$\frac1N\cdot\frac{2(M-1)}{M^2}$", 1)),
    [r"להשתמש ב-$N$ במקום $M$ בחישוב השכן", r"לחבר במקום להכפיל"],
    [CH(r"איך משלבים את ההסתברות לנחש נכון את מספרו של יוגיין ושכן של אסתר?",
        [r"מכפלה, כי שני המשחקים בלתי תלויים", r"סכום ההסתברויות", r"מנה של ההסתברויות"], 0,
        r"סכום או מנה אינם מתארים חיתוך של מאורעות בלתי תלויים."),
     NU(r"עבור $M=4$: מהי ההסתברות לנחש מספר שכן של אסתר, $\frac{2(M-1)}{M^2}$?", Fr(3, 8), r"$\frac{6}{16}=0.375$."),
     NU(r"עבור $N=3$: מהי $P(A_1)$?", Fr(1, 3), r"$\frac13$."),
     NU(r"מהי ההסתברות המבוקשת?", Fr(1, 8), r"$\frac13\cdot\frac38=\frac18=0.125$.")])

# Q4: mu = 1/24
Q4S = r"נקבע $\mu=\frac1{24}$. "
ADD(4, "א",
    RB((r"אינטגרביליות: $a=g=h=0$", 2), (r"נרמול ושוויון $P(X<0)=P(X>0)$: $d=\frac12$", 3), (r"תנאי התוחלת ופתרון: $b=12\mu$, $c=6\mu+\frac12$", 3)),
    [r"לא לאפס את $a$ ואת $g,h$ ולהמשיך עם אינטגרלים מתבדרים", r"לשכוח שהצפיפות מוגדרת פעמיים בנקודות הקצה"],
    [CH(r"מדוע $a=0$ וגם $g=h=0$?",
        [r"האינטגרל של קבוע חיובי על קרן אינסופית מתבדר, והצפיפות חייבת להיות אינטגרבילית", r"כי הצפיפות רציפה בכל נקודה", r"כי $\mu$ חייב להיות $0$"], 0,
        r"הצפיפות אינה נדרשת להיות רציפה, ו-$\mu$ אינו $0$ בדרך כלל ($b=12\mu$)."),
     NU(Q4S + r"מהו $d$? (מ-$P(X<0)=P(X>0)$ והנרמול)", Fr(1, 2), r"שני חצאי הסתברות: $d=\frac12$."),
     NU(r"מהו $b=12\mu$?", Fr(1, 2), r"$12\cdot\frac1{24}=\frac12$."),
     NU(r"מהו $c=6\mu+\frac12$?", Fr(3, 4), r"$\frac14+\frac12=\frac34$.")])

ADD(4, "ב",
    RB((r"הצפיפות ליניארית על $[-1,0]$, לכן מספיק לבדוק את הקצוות", 2), (r"$f(-1)=\frac12-6\mu\ge0$ ו-$f(0)=6\mu+\frac12\ge0$", 2), (r"$-\frac1{12}\le\mu\le\frac1{12}$", 1)),
    [r"לבדוק רק קצה אחד", r"להפוך את כיוון האי-שוויון"],
    [NU(r"באיזה $\mu$ מתאפס $f(-1)=\frac12-6\mu$ (הערך הגדול ביותר של $\mu$)?", Fr(1, 12), r"$\mu=\frac1{12}\approx0.0833$."),
     NU(r"באיזה $\mu$ מתאפס $f(0)=6\mu+\frac12$ (הערך הקטן ביותר)?", Fr(-1, 12), r"$\mu=-\frac1{12}\approx-0.0833$.")])

ADD(4, "ג",
    RB((r"$F_X(t)=0$ עבור $t<-1$", 1), (r"אינטגרציה של $12\mu x+6\mu+\frac12$ מ-$-1$", 3), (r"ענף $[0,1)$: $\frac{t+1}2$ ו-$F_X=1$ מ-$t=1$", 2), (r"בדיקת רציפות ב-$t=0$: $\frac12$", 2)),
    [r"לשכוח את הקבוע $F_X(-1)=0$", r"לשכוח שהענף האמצעי משתנה עם $\mu$"],
    [NU(Q4S + r"מהו $F_X(-\frac12)=\frac12(t+1)(12\mu t+1)$?", Fr(3, 16), r"$\frac12\cdot\frac12\cdot\frac34=\frac3{16}=0.1875$."),
     NU(r"מהו $F_X(0)$ (נקודת החיבור)?", Fr(1, 2), r"$\frac12(1)(1)=\frac12$."),
     NU(r"מהו $F_X(\frac12)=\frac{t+1}2$?", Fr(3, 4), r"$\frac{1.5}2=0.75$.")])

ADD(4, "ד",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$P(X>-\frac12)=1-F_X(-\frac12)$", 1), (r"$P(-\frac12<X<0)=F_X(0)-F_X(-\frac12)$", 1), (r"התשובה $\frac{1+6\mu}{3+6\mu}$", 1)),
    [r"לחלק ב-$P(X<0)=\frac12$ במקום ב-$P(X>-\frac12)$"],
    [NU(Q4S + r"מהי הסתברות התנאי $P(X>-\frac12)$?", Fr(13, 16), r"$1-\frac3{16}=\frac{13}{16}$."),
     NU(r"מהי $P(-\frac12<X<0)$?", Fr(5, 16), r"$\frac12-\frac3{16}=\frac5{16}$."),
     NU(r"מהי $P(X<0\mid X>-\frac12)$?", Fr(5, 13), r"$\frac{5/16}{13/16}=\frac5{13}\approx0.3846$, כלומר $\frac{1+6\mu}{3+6\mu}$.")])

# Q5: p = 0.6
ADD(5, "א",
    RB((r"תרגום המעגל: $(A\cap B)\cup C$", 1), (r"כלל החיבור-החיסור", 1), (r"$p+p^2-p^3$", 1)),
    [r"לכתוב $p^2+p$ (שכחו לחסר את החיתוך)"],
    [CH(r"איך משלבים את $P(A\cap B)$ ו-$P(C)$ כדי לקבל את $P((A\cap B)\cup C)$?",
        [r"$P(A\cap B)+P(C)-P(A\cap B\cap C)$", r"$P(A\cap B)+P(C)$", r"$P(A\cap B)\cdot P(C)$"], 0,
        r"השני סופר את החיתוך פעמיים ($0.96$), והשלישי הוא חיתוך ולא איחוד ($0.216$), במקום $0.744$."),
     NU(r"עבור $p=0.6$: מהי $P(A\cap B)$?", Fr(9, 25), r"$p^2=0.36$."),
     NU(r"מהי $P(Q_0)$?", Fr(93, 125), r"$0.36+0.6-0.216=0.744$.")])

ADD(5, "ב",
    RB((r"אותה טופולוגיה: אותה נוסחה", 1), (r"הסתברות פעולה אינה תלויה בזהות היחידות כשכולן שוות", 1), (r"$p(1+p-p^2)$", 1)),
    [r"לחשוב שהשינוי במיקום משנה את ההסתברות"],
    [CH(r"מדוע ל-$Q'$ הספציפי (למשל $(A\cap C)\cup B$) אותה הסתברות פעולה כמו ל-$Q_0$?",
        [r"יחידות זהות בהסתברות $p$ ובלתי תלויות, ולכן רק המבנה קובע את ההסתברות", r"כי $Q'=Q_0$ כמאורע", r"כי $p=1$"], 0,
        r"$Q'$ ו-$Q_0$ הם מאורעות שונים (למשל כש-$A=0$, $B=1$, $C=0$: $Q'$ פועל אבל $Q_0$ לא) עם אותה הסתברות."),
     NU(r"עבור $p=0.6$: מהי $P(A\cap C)$ ב-$Q'=(A\cap C)\cup B$?", Fr(9, 25), r"$0.36$."),
     NU(r"מהי $P(Q')$?", Fr(93, 125), r"$0.36+0.6-0.216=0.744$.")])

ADD(5, "ג",
    RB((r"שש האפשרויות לשיבוץ, בהסתברות שווה", 2), (r"התניה על השיבוץ (נוסחת ההסתברות השלמה)", 2), (r"$P(Q_0\cap Q_3)=3p^2-2p^3$", 3), (r"הרכבה: $\frac p3(1+7p-5p^2)$", 3)),
    [r"להכפיל $P(Q_0)P(Q')$ בטעות", r"לשכוח ששני שיבוצים נותנים את $Q_0$ עצמו ו-4 אחרים נותנים $3p^2-2p^3$"],
    [CH(r"כיצד מחשבים את ההסתברות ש-$Q_0$ וגם $Q'$ (שיבוץ אקראי) פועלים?",
        [r"נוסחת ההסתברות השלמה על שש האפשרויות לשיבוץ, כל אחת בהסתברות $\frac16$", r"$P(Q_0)\cdot P(Q')$", r"$P(Q_0)$ בלבד"], 0,
        r"המאורעות תלויים (אותן יחידות), ולכן המכפלה ($0.553$) שגויה. $P(Q_0)=0.744$ מתעלם מהצורך ש-$Q'$ יפעל."),
     NU(r"עבור $p=0.6$ ושיבוצים I ו-II ($Q'=Q_0$): מהי $P(Q_0\cap Q')$?", Fr(93, 125), r"$P(Q_0)=0.744$."),
     NU(r"בשיבוצים III-VI: מהי $P(Q_0\cap Q')=3p^2-2p^3$?", Fr(81, 125), r"$1.08-0.432=0.648$."),
     NU(r"מהי $P(Q_0\cap Q')$ הכוללת?", Fr(17, 25), r"$\frac16\{2\cdot0.744+4\cdot0.648\}=0.68$.")])

ADD(5, "ד",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"המכנה $P(Q_0)$", 2), (r"היחס $\frac{1+7p-5p^2}{3(1+p-p^2)}$", 2)),
    [r"לחלק ב-$P(Q')$ במקום ב-$P(Q_0)$ (אותו ערך כאן, אך התנאי הוא $Q_0$)"],
    [NU(r"עבור $p=0.6$: מהי הסתברות התנאי $P(Q_0)$?", Fr(93, 125), r"$0.744$."),
     NU(r"מהי $P(Q_0\cap Q')$ (סעיף ג)?", Fr(17, 25), r"$0.68$."),
     NU(r"מהי $P(Q'\mid Q_0)$?", 0.68 / 0.744, r"$\frac{0.68}{0.744}\approx0.9140$.")])

ADD(5, "ה",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$P(Q'\cap\overline{Q_0})=P(Q')-P(Q'\cap Q_0)$", 2), (r"המכנה $P(\overline{Q_0})=1-P(Q_0)$", 1)),
    [r"לחסר $P(Q_0)$ במקום $P(Q'\cap Q_0)$"],
    [NU(r"עבור $p=0.6$: מהי הסתברות התנאי $P(\overline{Q_0})$?", Fr(32, 125), r"$1-0.744=0.256$."),
     NU(r"מהי $P(Q'\cap\overline{Q_0})=P(Q')-P(Q'\cap Q_0)$?", Fr(8, 125), r"$0.744-0.68=0.064$."),
     NU(r"מהי $P(Q'\mid\overline{Q_0})$?", Fr(1, 4), r"$\frac{0.064}{0.256}=0.25=\frac{2p}{3(1+p)}$.")])

# Q6: N1=6 (D1=4 red), N2=4 (D2=1 red), n=3 balls moved
ADD(6, "א",
    RB((r"התניה על $X$, מספר האדומים שהועברו (היפרגיאומטרי)", 5), (r"$P(\text{red}/X=k)=\frac{D_2+k}{N_2+n}$", 5), (r"$\mathbb{E}[X]=n\frac{D_1}{N_1}$ והרכבה", 5)),
    [r"לשכוח שבכד השני יש עכשיו $N_2+n$ כדורים", r"להניח שכל הכדורים שהועברו אדומים"],
    [CH(r"כיצד מחשבים את ההסתברות שכדור הנלקח מהכד השני (אחרי ההעברה) יהיה אדום?",
        [r"נוסחת ההסתברות השלמה על $X$, מספר האדומים שהועברו", r"$\dfrac{D_2}{N_2}$, כאילו ההעברה לא השפיעה", r"$\dfrac{D_1}{N_1}$, כאילו הכדור נלקח מהכד הראשון"], 0,
        r"ההעברה משנה את הרכב הכד השני, ולכן $\frac{D_2}{N_2}$ (שהוא $0.25$) שגוי; $\frac{D_1}{N_1}=0.667$ מתייחס לכד אחר."),
     NU(r"עבור $N_1=6$, $D_1=4$, $N_2=4$, $D_2=1$, $n=3$: מהו $\mathbb{E}[X]=n\frac{D_1}{N_1}$?", 2, r"$3\cdot\frac46=2$."),
     NU(r"מהי $P(\text{red}/X=3)=\frac{D_2+3}{N_2+n}$?", Fr(4, 7), r"בכד $7$ כדורים, מהם $4$ אדומים."),
     NU(r"מהי $P(\text{red})=\frac{D_2+\mathbb{E}[X]}{N_2+n}$?", Fr(3, 7), r"$\frac{1+2}{7}=\frac37\approx0.4286$.")])

ADD(6, "ב",
    RB((r"בייס: $\frac{P(\text{red}/X=n)P(X=n)}{P(\text{red})}$", 2), (r"$P(X=n)=\frac{\binom{D_1}{n}}{\binom{N_1}{n}}$", 1), (r"$P(\text{red}/X=n)=\frac{D_2+n}{N_2+n}$ ו-$P(\text{red})$ מסעיף א", 2)),
    [r"להשתמש ב-$P(\text{red}/X=n)$ בלי לכפול ב-$P(X=n)$", r"לחלק ב-$P(X=n)$ במקום ב-$P(\text{red})$"],
    [CH(r"נתון שהכדור שנלקח מהכד השני אדום. כיצד מחשבים את ההסתברות שכל $n$ הכדורים שהועברו היו אדומים?",
        [r"כלל בייס: $\dfrac{P(\text{red}/X=n)\,P(X=n)}{P(\text{red})}$", r"$P(X=n)$ ללא התחשבות במידע", r"$P(\text{red}/X=n)$"], 0,
        r"השני מתעלם מהמידע החדש ($0.2$ במקום $0.267$). השלישי הוא ההסתברות ההפוכה ($0.571$)."),
     NU(r"עבור אותם ערכים: מהי $P(X=3)=\frac{\binom43}{\binom63}$?", Fr(1, 5), r"$\frac4{20}=0.2$."),
     NU(r"מהי $P(\text{red}/X=3)$?", Fr(4, 7), r"$\frac47$."),
     NU(r"מהי הסתברות התנאי $P(\text{red})$?", Fr(3, 7), r"סעיף א."),
     NU(r"מהי $P(X=3/\text{red})$?", Fr(4, 15), r"$\frac{(4/7)(1/5)}{3/7}=\frac4{15}\approx0.2667$.")])

ADD(6, "ג",
    RB((r"הצבעים הוחלפו: מספר האדומים שהועברו הוא $n-X$", 2), (r"$\mathbb{E}[n-X]=n(1-\frac{D_1}{N_1})$", 2), (r"$\frac{D_2+n(1-D_1/N_1)}{N_2+n}$", 1)),
    [r"להשתמש ב-$X$ במקום $n-X$", r"לשכוח שהחלפת הצבעים מוסיפה את השחורים כאדומים"],
    [CH(r"אחרי החלפת הצבעים, מהו מספר הכדורים האדומים שהועברו לכד השני?",
        [r"$n-X$, מספר הכדורים ששחורים בכד הראשון", r"$X$", r"$n$"], 0,
        r"כל כדור שהועבר הופך לצבע ההפוך: אדום נעשה שחור ושחור נעשה אדום. $X$ היה נכון לפני ההחלפה; $n$ נכון רק אם כולם היו שחורים."),
     NU(r"עבור אותם ערכים: מהו $\mathbb{E}[n-X]$?", 1, r"$3-2=1$."),
     NU(r"מהי $P(\text{red})=\frac{D_2+\mathbb{E}[n-X]}{N_2+n}$?", Fr(2, 7), r"$\frac{1+1}7=\frac27\approx0.2857$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = _vsrc(CODE)
        _q["stepsSource"] = _vsrc(CODE)

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
