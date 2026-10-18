# -*- coding: utf-8 -*-
"""Generator for tools/raw/25S-A.json -- probability (course 20021), summer 2025, moed A (20.10.2025). Choose 4 of 6
questions, 25 points each. 26 items (Q1 4, Q2 7, Q3 5 (bonus part ה solved), Q4 3, Q5 4, Q6 3).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25S-A.py

Source: exam pp.1-3 (pdf), handwritten official solutions on grid paper pp.4-15 (no text layer; rendered and read).

Transcription notes
- Part keys: single letters. Q2 prints "א-1" ... "א-5", "ב", "ג" -> a b c d e (א-1..א-5), f (ב), g (ג); Q3 prints
  "א".."ה" -> a..e. The printed label (e.g. "א-3") is the first bold token of each question text.
- Q3 part ה is the BONUS part. The official solution states explicitly that the bonus solution will not be published,
  so there is no answer source: solved (solutionSource "solved", official:false) by the method of part ד,
  answer D(D-1)/(N(N-1)); verified exactly and by Monte Carlo in tools/verify/25S-A/check.py.
- Q5 part ד: the official solution defines the event "both travelled through the pub" as the intersection of the two
  pub routes; that definition is transcribed as printed.
- Math never holds Hebrew.
- Q1 parts a-d carry `region` data (REGIONS below; moved from tools/verify/25S-A/regions.json) and every simulable part a `sim`.
- The page-1 cover (lecturer names) is not copied anywhere.
"""
import json, math, pathlib
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from verified import src as _vsrc
from fractions import Fraction as Fr

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25S-A.json"
CODE = "25S-A"
IMG = "images/exams/25S-A-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_CAP = (r"חגב מבצע שתי קפיצות אקראיות באותו כיוון, אחת אחרי השנייה. אורכי הקפיצות מהווים משתנים מקריים בלתי תלויים בעלי התפלגות אחידה רציפה: "
          r"$X_1\sim U_c(0,1)$ ו-$X_2\sim U_c(0,2)$.")

Q1_OMEGA = r"מרחב המדגם הוא המלבן $\Omega=(0,1)\times(0,2)$ במישור $(x_1,x_2)$, ושטחו $|\Omega|=2$. הסתברות היא שטח האזור חלקי $2$ (גישה קלאסית)."

questions.append(Q(
    1, "א", "uniform_geometric",
    r"מהי ההסתברות שאורך הקפיצה הראשונה גדול מאורך הקפיצה השנייה?",
    r"""**$P(X_1>X_2)$.**
""" + Q1_OMEGA + r"""
$$P(X_1>X_2)=\frac{\left|\{x_1>x_2\}\right|}{|\Omega|}=\frac{1\cdot1\cdot\frac12}{2}=\frac14.$$
האזור $\{x_2<x_1\}$ הוא המשולש שמתחת לישר $x_2=x_1$ בתוך המלבן (ניצבים $1$ ו-$1$).
![האזור x2 < x1 בתוך המלבן](images/exams/25S-A-Q1a-region.png)""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"מהי ההסתברות שלפחות אחת משתי הקפיצות הייתה קצרה מ-$\frac12$?",
    r"""**$P(X_1<\frac12\ \cup\ X_2<\frac12)$.**
מכלל החיבור ומאי-התלות:
$$P\left(X_1<\tfrac12\cup X_2<\tfrac12\right)=P\left(X_1<\tfrac12\right)+P\left(X_2<\tfrac12\right)-P\left(X_1<\tfrac12\right)P\left(X_2<\tfrac12\right).$$
$P(X_1<\frac12)=\frac12$ כי $X_1\sim U_c(0,1)$, ו-$P(X_2<\frac12)=\frac{1/2}{2}=\frac14$ כי $X_2\sim U_c(0,2)$. הצבה:
$$P=\frac12+\frac14-\frac12\cdot\frac14=\frac58.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"מהי ההסתברות שהאורך הכולל $X_1+X_2$ של שתי קפיצות לא יעלה על $1$.",
    r"""**$P(X_1+X_2\le1)$.**
""" + Q1_OMEGA + r"""
$$P(X_1+X_2\le1)=\frac{\left|\{x_2\le1-x_1\}\right|}{|\Omega|}=\frac{\frac12\cdot1\cdot1}{2}=\frac14.$$
האזור $\{x_2\le1-x_1\}$ הוא המשולש שמתחת לישר $x_2=1-x_1$ בתוך המלבן.
![האזור x2 ≤ 1 - x1 בתוך המלבן](images/exams/25S-A-Q1c-region.png)""",
    8, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"אם ידוע כי האורך הכולל של שתי קפיצות גדול מ-$2$, מהי ההסתברות שאורך הקפיצה הראשונה גדול מ-$\frac12$?",
    r"""**$P(X_1>\frac12\mid X_1+X_2>2)$.**
לפי הגדרת הסתברות מותנית:
$$P\left(X_1>\tfrac12\ \Big/\ X_1+X_2>2\right)=\frac{P\left(X_1>\frac12\cap X_2>2-X_1\right)}{P(X_2>2-X_1)}.$$
שני האירועים הם אזורים בתוך המלבן, ומכיוון שהמכנה $|\Omega|=2$ משותף לשניהם, אפשר לחלק שטחים:
$$=\frac{\left|\{x_1>\frac12\cap x_2>2-x_1\}\right|}{\left|\{x_2>2-x_1\}\right|}=\frac{\frac12\cdot\frac{1+\frac12}{2}}{\frac12\cdot1\cdot1}=\frac{3/8}{1/2}=\frac34.$$
(השטח במונה הוא טרפז; השטח במכנה הוא המשולש מעל הישר $x_2=2-x_1$ בפינה העליונה של המלבן.)
![האזור x2 > 2 - x1 והחלק שלו מימין ל-x1=1/2](images/exams/25S-A-Q1d-region.png)""",
    7, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_CAP = (r"יהיו $A$ ו-$B$ מאורעות לא ריקים. נתון כי $P(A\setminus B)=p$, $P(A\cap B)=q$ ו-$P(A/B)=s$. "
          r"(כאן $A\setminus B$ הוא המאורע $A$ פחות $B$.)")

questions.append(Q(
    2, "א", "basics_events",
    r"חשבו את ההסתברויות הבאות (עליך לפשט את כל הביטויים!): **(א-1):** $P(A)$. (3 נק׳ לכל תת סעיף)",
    r"""**$P(A)$.**
$A$ מתפצל לחלק שמחוץ ל-$B$ ולחלק שבתוך $B$:
$$P(A)=P(A\setminus B)+P(A\cap B)=p+q.$$
![דיאגרמת ון של A ו-B](images/exams/25S-A-Q2-venn.png)""",
    3, contextId="c2"))

questions.append(Q(
    2, "ב", "conditional_bayes",
    r"חשבו את ההסתברויות הבאות (עליך לפשט את כל הביטויים!): **(א-2):** $P(B)$. (3 נק׳ לכל תת סעיף)",
    r"""**$P(B)$.**
$$P(A/B)=\frac{P(A\cap B)}{P(B)}\ \Longrightarrow\ s=\frac{q}{P(B)}\ \Longrightarrow\ P(B)=\frac qs.$$""",
    3, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"חשבו את ההסתברויות הבאות (עליך לפשט את כל הביטויים!): **(א-3):** $P(A/\bar B)$. (3 נק׳ לכל תת סעיף)",
    r"""**$P(A/\bar B)$.**
$$P(A/\bar B)=\frac{P(A\cap\bar B)}{P(\bar B)}=\frac{P(A\setminus B)}{1-P(B)}=\frac{p}{1-\frac qs}=\frac{ps}{s-q}.$$

**הערה:** כאשר $s=q$ מתקבל $P(\bar B)=0$, ולכן ההסתברות המותנית אינה מוגדרת; הנוסחה תקפה עבור $s>q$.""",
    3, contextId="c2"))

questions.append(Q(
    2, "ד", "conditional_bayes",
    r"חשבו את ההסתברויות הבאות (עליך לפשט את כל הביטויים!): **(א-4):** $P(\bar A/B)$. (3 נק׳ לכל תת סעיף)",
    r"""**$P(\bar A/B)$.**
$$P(\bar A/B)=1-P(A/B)=1-s.$$""",
    3, contextId="c2"))

questions.append(Q(
    2, "ה", "conditional_bayes",
    r"חשבו את ההסתברויות הבאות (עליך לפשט את כל הביטויים!): **(א-5):** $P(\bar A/\bar B)$. (3 נק׳ לכל תת סעיף)",
    r"""**$P(\bar A/\bar B)$.**
$$P(\bar A/\bar B)=1-P(A/\bar B)=1-\frac{ps}{s-q}.$$

**הערה:** כאשר $s=q$ מתקבל $P(\bar B)=0$, ולכן ההסתברות המותנית אינה מוגדרת; הנוסחה תקפה עבור $s>q$.""",
    3, contextId="c2"))

questions.append(Q(
    2, "ו", "independence",
    r"**ב:** האם ייתכן כי $s<q$? נמקו היטב!",
    r"""**האם $s<q$ אפשרי?**
לא. מסעיף א-2, $P(B)=\frac qs$, ומכיוון ש-$P(B)\le1$ מקבלים
$$\frac qs\le1\ \Longleftrightarrow\ q\le s.$$
לכן לא ייתכן ש-$s<q$.""",
    5, contextId="c2"))

questions.append(Q(
    2, "ז", "independence",
    r"**ג:** עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו מאורעות **בלתי תלויים**?",
    r"""**אי-תלות.**
$A$ ו-$B$ בלתי תלויים אם ורק אם $P(A/B)=P(A)$. לפי הסעיפים הקודמים, $P(A/B)=s$ ו-$P(A)=p+q$, ולכן התנאי הוא
$$p+q=s.$$""",
    5, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_CAP = r"בכד נמצאים $N$ כדורים וביניהם $D$ כדורים אדומים."

questions.append(Q(
    3, "א", "combinatorics",
    r"מוציאים מהכד **כדור אחד**. מהי ההסתברות שצבאו אדום?",
    r"""**כדור אחד.**
לפי הגישה הקלאסית,
$$P(R_1)=\frac DN.$$""",
    3, contextId="c3"))

questions.append(Q(
    3, "ב", "combinatorics",
    r"מוציאים מהכד **שני כדורים**, אחד אחרי השני. מהי ההסתברות שהכדור **השני** יהיה אדום? עליך לתת חישוב מפורט.",
    r"""**הכדור השני.**
לפי נוסחת ההסתברות השלמה על תוצאת הכדור הראשון:
$$P(R_2)=P(R_2/R_1)P(R_1)+P(R_2/\bar R_1)P(\bar R_1)=\frac{D-1}{N-1}\cdot\frac DN+\frac D{N-1}\cdot\left(1-\frac DN\right).$$
$$=\frac{D(D-1)}{N(N-1)}+\frac{D(N-D)}{N(N-1)}=\frac{D\,[D-1+N-D]}{N(N-1)}=\frac{D(N-1)}{N(N-1)}=\frac DN.$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ג", "combinatorics",
    r"מוציאים מהכד **שלושה כדורים** ללא החזרה. מהי ההסתברות שהכדור **השלישי** יהיה אדום? עליך לתת חישוב מפורט.",
    r"""**הכדור השלישי.**
לפי נוסחת ההסתברות השלמה על תוצאות שני הכדורים הראשונים:
$$P(R_3)=P(R_3/R_1\cap R_2)P(R_1\cap R_2)+P(R_3/\bar R_1\cap R_2)P(\bar R_1\cap R_2)+P(R_3/R_1\cap\bar R_2)P(R_1\cap\bar R_2)+P(R_3/\bar R_1\cap\bar R_2)P(\bar R_1\cap\bar R_2).$$
ההסתברויות לשני הכדורים הראשונים:
$$P(R_1\cap R_2)=\frac DN\cdot\frac{D-1}{N-1},\quad P(\bar R_1\cap R_2)=\frac{N-D}N\cdot\frac D{N-1},\quad P(R_1\cap\bar R_2)=\frac DN\cdot\frac{N-D}{N-1},\quad P(\bar R_1\cap\bar R_2)=\frac{N-D}N\cdot\frac{N-D-1}{N-1}.$$
ההסתברויות המותנות:
$$P(R_3/R_1\cap R_2)=\frac{D-2}{N-2},\quad P(R_3/\bar R_1\cap R_2)=\frac{D-1}{N-2},\quad P(R_3/R_1\cap\bar R_2)=\frac{D-1}{N-2},\quad P(R_3/\bar R_1\cap\bar R_2)=\frac D{N-2}.$$
הצבה, ואיחוד הזוגות של האיברים לפי הגורם המשותף:
$$P(R_3)=\frac{D(D-1)}{N(N-1)(N-2)}\bigl[(D-2)+(N-D)\bigr]+\frac{D(N-D)}{N(N-1)(N-2)}\bigl[(D-1)+(N-D-1)\bigr]=\frac{D(D-1)}{N(N-1)}+\frac{D(N-D)}{N(N-1)}=\frac{D}{N}.$$""",
    6, contextId="c3"))

questions.append(Q(
    3, "ד", "special_discrete",
    r"מוציאים מהכד $n$ כדורים ללא החזרה. מהי ההסתברות שהכדור ה-$n$ יהיה אדום? עליך לתת חישוב מפורט אשר לא מסתמך על הנחות מכול סוג שהוא.",
    r"""**הכדור ה-$n$.**
נסמן ב-$X$ את מספר הכדורים האדומים בין $n-1$ הכדורים שהוצאו קודם. אז $X\sim\mathrm{Hyp}(D,N,n-1)$. לפי נוסחת ההסתברות השלמה:
$$P(R_n)=\sum_{k=0}^{n-1}P(R_n/X=k)\,P(X=k).$$
בהינתן $X=k$ נשארו בכד $N-(n-1)$ כדורים, ומתוכם $D-k$ אדומים, ולכן
$$P(R_n/X=k)=\frac{D-k}{N-(n-1)}.$$
הצבה:
$$P(R_n)=\sum_{k=0}^{n-1}\frac{D-k}{N-(n-1)}P(X=k)=\frac1{N-n+1}\left\{D\sum_{k=0}^{n-1}P(X=k)-\sum_{k=0}^{n-1}k\,P(X=k)\right\}.$$
הסכום הראשון שווה $1$, והשני הוא $\mathbb{E}[X]=\frac DN(n-1)$ (תוחלת של היפרגאומטרי). לכן
$$P(R_n)=\frac1{N-n+1}\left\{D-D\frac{n-1}N\right\}=\frac{D}{N-n+1}\cdot\frac{N-n+1}{N}=\frac DN.$$""",
    11, contextId="c3"))

questions.append(Q(
    3, "ה", "combinatorics",
    r"**סעיף בונוס:** מוציאים מהכד $n$ כדורים ללא החזרה. מהי ההסתברות ששני הכדורים האחרונים יהיו אדומים? (5 נק׳, הניקוד יינתן עבור פתרון מפורט בלבד.)",
    r"""**פתרון (הפתרון הרשמי לסעיף הבונוס לא פורסם).**
נפעל כמו בסעיף ד ($2\le n\le N$). נסמן ב-$X$ את מספר הכדורים האדומים בין $m=n-2$ הכדורים שהוצאו לפני שני האחרונים. אז $X\sim\mathrm{Hyp}(D,N,m)$, ולפי נוסחת ההסתברות השלמה:
$$P(R_{n-1}\cap R_n)=\sum_kP(R_{n-1}\cap R_n/X=k)\,P(X=k).$$
בהינתן $X=k$ נשארו בכד $M=N-m=N-n+2$ כדורים, ומתוכם $D-k$ אדומים, ולכן
$$P(R_{n-1}\cap R_n/X=k)=\frac{D-k}{M}\cdot\frac{D-k-1}{M-1}.$$
הצבה:
$$P(R_{n-1}\cap R_n)=\frac{\mathbb{E}\big[(D-X)(D-X-1)\big]}{M(M-1)}.$$
נפתח: $(D-X)(D-X-1)=D(D-1)-2(D-1)X+X(X-1)$. תוחלת ההיפרגאומטרי היא $\mathbb{E}[X]=\frac{mD}N$, ובעזרת $k(k-1)\binom Dk=D(D-1)\binom{D-2}{k-2}$ וזהות ונדרמונד,
$$\mathbb{E}[X(X-1)]=\sum_kk(k-1)\frac{\binom Dk\binom{N-D}{m-k}}{\binom Nm}=D(D-1)\frac{\binom{N-2}{m-2}}{\binom Nm}=\frac{m(m-1)D(D-1)}{N(N-1)}.$$
לכן
$$\mathbb{E}\big[(D-X)(D-X-1)\big]=D(D-1)\cdot\frac{N(N-1)-2m(N-1)+m(m-1)}{N(N-1)}=D(D-1)\cdot\frac{(N-m)(N-m-1)}{N(N-1)}=\frac{D(D-1)\,M(M-1)}{N(N-1)}.$$
ומכאן
$$P(R_{n-1}\cap R_n)=\frac{D(D-1)}{N(N-1)}.$$
כמו בסעיף ד, התשובה לא תלויה ב-$n$: היא שווה להסתברות ששני הכדורים הראשונים אדומים.""",
    5, contextId="c3", solutionSource="solved", official=False))

# ------------------------------------------------------------------ Q4
Q4_CAP = (r"לפניך גרף עבור פונקציית צפיפות ההסתברות $f_X(x)$ של משתנה מקרי $X$: הצפיפות עולה ליניארית מ-$0$ ב-$x=0$ עד הגובה $\frac c2$ ב-$x=a$, "
          r"קופצת לגובה $c$ וקבועה עד $x=b$, ושווה אפס בכל מקום אחר. $X$ מתקיים:" "\n"
          r"$$\begin{cases}P(0\le X\le a)=P(a\le X\le b)\\\mathbb{E}[X]=\dfrac{43}{48}\end{cases}$$")

questions.append(Q(
    4, "א", "continuous_rv",
    r"מצאו את הפרמטרים $a$, $b$ ו-$c$.",
    r"""**מציאת $a,b,c$.**
מהגרף $f_X(x)=\dfrac{c\,x}{2a}$ ב-$[0,a)$ ו-$f_X(x)=c$ ב-$[a,b]$.
• נרמול: $\displaystyle\int_{-\infty}^{\infty}f_X(x)\,dx=1$:
$$\frac{ac}4+c(b-a)=1.$$
• מהתנאי $P(0\le X\le a)=P(a\le X\le b)$ כל אחד מהשטחים שווה ל-$\frac12$:
$$\frac{ac}4=c(b-a)=\frac12.\qquad(1)$$
• תוחלת:
$$\mathbb{E}[X]=\int_0^ax\cdot\frac{c\,x}{2a}\,dx+\int_a^bx\cdot c\,dx=\frac{c\,a^2}6+c\,\frac{b^2-a^2}2=\frac{43}{48}.\qquad(2)$$
ממשוואה (1): $c=\frac2a$ ו-$\frac a4=b-a$, כלומר $b=\frac54a$. הצבה ב-(2) נותנת $\frac{43}{48}a=\frac{43}{48}$, ולכן
$$a=1,\qquad b=\frac54,\qquad c=2.$$""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את התוצאה.",
    r"""**פונקציית ההתפלגות המצטברת.**
$F_X(t)=\int_{-\infty}^tf_X(x)\,dx$ לכל $t\in\mathbb{R}$, כאשר $f_X(x)=x$ ב-$[0,1)$ ו-$f_X(x)=2$ ב-$[1,\frac54]$:
$$F_X(t)=\begin{cases}0,&t<0\\\dfrac{t^2}2,&0\le t<1\\\dfrac12+2(t-1),&1\le t<\dfrac54\\1,&t\ge\dfrac54\end{cases}$$
(בענף האמצעי: $\frac12+2(t-1)=2t-\frac32$.)
![גרף F_X(t): פרבולה עד (1, 1/2), אחר כך ישר עד (5/4, 1)](images/exams/25S-A-Q4-cdf.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"חשבו את ההסתברות $P(X>1)$.",
    r"""**$P(X>1)$.**
$$P(X>1)=1-F_X(1)=1-\frac12=\frac12,$$
(הצפיפות מימין ל-$x=1$ מכילה בדיוק את המחצית השנייה, כפי שנדרש מהתנאי $P(0\le X\le a)=P(a\le X\le b)$ עם $a=1$.)""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_CAP = (r"לפניך מפת הכבישים בין ביתו של יוג׳ין, ביתו של סרג׳, קמפוס H.I.T. ופאב ״האקדמיה״. בגלל אי ודאות בתכנון עבודות בכבישים, כל אחד מהכבישים $A$, $B$, $C$ ו-$D$ "
          r"יכול להיסגר לתנועה בהסתברות $1-p$. כבישים אלה נסגרים לתנועה באופן בלתי תלוי זה בזה. ענו על השאלות הבאות.")

questions.append(Q(
    5, "א", "circuits",
    r"מהי ההסתברות $P_1$ שיוג׳ין יצליח להגיע מביתו למכון?",
    r"""**$P_1$.**
$P(A)=P(B)=P(C)=P(D)=p$. יוג׳ין מגיע למכון ישירות דרך $A$, או דרך $C$, $D$ ו-$B$ (דרך הפאב וביתו של סרג׳):
$$Q_E=A\cup(B\cap C\cap D).$$
$$P_1=P(Q_E)=P(A)+P(B\cap C\cap D)-P(A\cap B\cap C\cap D)=p+p^3-p^4.$$""",
    6, contextId="c5"))

questions.append(Q(
    5, "ב", "circuits",
    r"מהי ההסתברות $P_2$ שגם יוג׳ין וגם סרג׳ יצליחו להגיע למכון?",
    r"""**$P_2$.**
באופן סימטרי סרג׳ מגיע למכון דרך $B$, או דרך $D$, $C$ ו-$A$:
$$Q_S=B\cup(A\cap C\cap D).$$
עלינו לחשב $P(Q_E\cap Q_S)$. אפשר לעשות זאת באמצעות חוקי האלגברה הבוליאנית, אך נעדיף לתרגם את $Q_E\cap Q_S$ לשפת המעגלים: ענף $A$ במקביל ל-($B,C,D$ בטור), בטור עם ענף $B$ במקביל ל-($A,C,D$ בטור). נסמן $\tilde Q=Q_E\cap Q_S$ ונפעל לפי $A$:
$$P(\tilde Q)=P(\tilde Q/A)P(A)+P(\tilde Q/\bar A)P(\bar A).$$
• בהינתן $A$ פועל, $Q_E$ מתקיים, והתנאי $Q_S$ הופך ל-$B\cup(C\cap D)$:
$$P(\tilde Q/A)=P\bigl(B\cup(C\cap D)\bigr)=P(B)+P(C\cap D)-P(B\cap C\cap D)=p+p^2-p^3.$$
• בהינתן $A$ לא פועל, $Q_E$ דורש $B\cap C\cap D$, ו-$Q_S$ מתקיים אז מאליו (דרך $B$):
$$P(\tilde Q/\bar A)=P(B\cap C\cap D)=p^3.$$
הצבה:
$$P_2=P(Q_E\cap Q_S)=p\,(p+p^2-p^3)+p^3(1-p)=p^2\left(1+2p-2p^2\right).$$""",
    6, contextId="c5"))

questions.append(Q(
    5, "ג", "circuits",
    r"מהי ההסתברות $P_3$ שיוג׳ין **כן** יצליח להגיע מביתו למכון אך סרג׳ **לא** יצליח?",
    r"""**$P_3$.**
$$P_3=P(Q_E\cap\bar Q_S)=P(Q_E)-P(Q_E\cap Q_S)=P_1-P_2=p+p^3-p^4-p^2-2p^3+2p^4,$$
ולכן
$$P_3=p-p^2-p^3+p^4.$$""",
    6, contextId="c5"))

questions.append(Q(
    5, "ד", "conditional_bayes",
    r"אם ידוע כי שניהם הגיעו למכון, מהי ההסתברות $P_4$ ששניהם נסעו דרך הפאב?",
    r"""**$P_4=P(Q_{PUB}\mid Q_E\cap Q_S)$.**
$$P_4=\frac{P(Q_{PUB}\cap Q_E\cap Q_S)}{P(Q_E\cap Q_S)}.$$
כאן המאורע $Q_{PUB}$ הוא ששניהם עוברים דרך הפאב:
$$Q_{PUB}\cap Q_E\cap Q_S=(B\cap C\cap D)\cap(A\cap C\cap D)=A\cap B\cap C\cap D,$$
ולכן $P(Q_{PUB}\cap Q_E\cap Q_S)=p^4$. מכאן
$$P_4=\frac{p^4}{P_2}=\frac{p^2}{1+2p-2p^2}.$$

**הערה:** הביטוי ״שניהם נסעו דרך הפאב״ נקרא כאן כך שכל ארבעת הכבישים פתוחים ($A\cap B\cap C\cap D$); בקריאה מחמירה יותר, שבה שני המסלולים חייבים להיות זרים זה לזה, המאורע היה בלתי אפשרי.""",
    7, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_CAP = (r"נתונה רשת של $m\times n$ תאים כמתואר באיור. החלקיק שנמצא בפינה השמאלית התחתונה מתחיל לקפוץ. בכל קפיצה הוא יכול לקפוץ יחידה אחת ימינה בהסתברות $p$ "
          r"או יחידה אחת למעלה בהסתברות $1-p$.")

questions.append(Q(
    6, "א", "combinatorics",
    r"כמה קפיצות יידרשו לחלקיק כדי להגיע לפינה הימנית העליונה?",
    r"""**מספר הקפיצות.**
כדי להגיע מ-$A$ ל-$B$ צריך לבצע בסך הכול $m$ קפיצות ימינה ו-$n$ קפיצות למעלה, בסדר כלשהו. סך הכול יידרשו
$$T=n+m$$
קפיצות.""",
    5, contextId="c6"))

questions.append(Q(
    6, "ב", "special_discrete",
    r"מהי ההסתברות שחלקיק יגיע לפינה הימנית העליונה?",
    r"""**הסתברות להגיע לפינה.**
נגדיר משתנה מקרי $X=\{$מספר הקפיצות ימינה מתוך $n+m$ קפיצות$\}$. הניסוי (כל קפיצה בלתי תלויה, ימינה בהסתברות $p$) מביא לכך ש-
$$X\sim\mathrm{Bin}(n+m,p).$$
ההסתברות הנדרשת היא $P(X=m)$:
$$P(X=m)=\binom{n+m}{m}p^m(1-p)^{n+m-m},$$
כלומר
$$P(Q_{A\to B})=\binom{n+m}{m}p^m(1-p)^n.$$""",
    10, contextId="c6"))

questions.append(Q(
    6, "ג", "conditional_bayes",
    r"**אם ידוע** כי החלקיק הגיע לפינה הימנית העליונה, מהי ההסתברות שמסלול החלקיק עבר דרך הנקודה $(X,Y)$ בתוך הרשת? האם תשובתך תלויה ב-$p$?",
    r"""**בהינתן שהגיע ל-$B$, עבר דרך $(X,Y)$.**
נסמן ב-$R$ את הנקודה $(X,Y)$ ו-$Q_{A\to B}$ את האירוע שהחלקיק מגיע מ-$A$ ל-$B$.
$$P\bigl(R\in A\to B\mid Q_{A\to B}\bigr)=\frac{P(Q_{A\to R\to B})}{P(Q_{A\to B})}=\frac{P(Q_{A\to R})\,P(Q_{R\to B})}{P(Q_{A\to B})}.$$
(מעבר $A\to R$ ואחר כך $R\to B$ הם מאורעות בלתי תלויים: קפיצות נפרדות.)
כאן
$$P(Q_{A\to R})=\binom{X+Y}{X}p^X(1-p)^Y,\qquad P(Q_{R\to B})=\binom{m+n-X-Y}{m-X}p^{m-X}(1-p)^{n-Y}.$$
הצבה:
$$P\bigl(R\in A\to B\mid Q_{A\to B}\bigr)=\frac{\binom{X+Y}{X}p^X(1-p)^Y\binom{m+n-X-Y}{m-X}p^{m-X}(1-p)^{n-Y}}{\binom{n+m}{m}p^m(1-p)^n}=\frac{\binom{X+Y}{X}\binom{m+n-X-Y}{m-X}}{\binom{n+m}{m}}.$$
(החזקות של $p$ ו-$1-p$ מצטמצמות.) אפשר לראות שזו ההתפלגות ההיפרגאומטרית $\mathrm{Hyp}(X+Y,\,n+m,\,m)$. התשובה אינה תלויה ב-$p$!""",
    10, contextId="c6"))

# ------------------------------------------------------------------ area regions (RAW_SCHEMA `region`; moved from tools/verify/25S-A/regions.json)
R12 = {"x": [0, 1], "y": [0, 2]}
XL = {"x": "X1", "y": "X2"}
REGIONS = {
    (1, "א"): {"space": R12, "labels": XL, "event": [{"a": 1, "b": -1, "c": 0, "op": ">"}], "exact": 0.25, "caption": "האזור x1>x2"},
    (1, "ב"): {"space": R12, "labels": XL, "event": {"any": [[{"a": 1, "c": 0.5, "op": "<"}], [{"b": 1, "c": 0.5, "op": "<"}]]}, "exact": 0.625,
               "caption": "האזור x1<1/2 או x2<1/2"},
    (1, "ג"): {"space": R12, "labels": XL, "event": [{"a": 1, "b": 1, "c": 1, "op": "<="}], "exact": 0.25, "caption": "האזור x1+x2<=1"},
    (1, "ד"): {"space": R12, "labels": XL, "event": [{"a": 1, "c": 0.5, "op": ">"}], "given": [{"a": 1, "b": 1, "c": 2, "op": ">"}], "exact": 0.75,
               "caption": "x1>1/2 בהינתן x1+x2>2"},
}
for _q in questions:
    _r = REGIONS.get((_q["num"], _q.get("part")))
    if _r is not None:
        _q["region"] = _r

# ------------------------------------------------------------------ simulations (RAW_SCHEMA `sim`)
# Symbolic answers are simulated at a stated sample value (given in each `estimate`). Not simulated: Q2 part ו
# (an impossibility argument), Q6 part א (a deterministic count).
def J(pAB, pAnB, pnAB, pnAnB):
    return [{"p": pAB, "A": 1, "B": 1}, {"p": pAnB, "A": 1, "B": 0}, {"p": pnAB, "A": 0, "B": 1}, {"p": pnAnB, "A": 0, "B": 0}]


# Q2: p=P(A\B)=0.2, q=P(A and B)=0.3, s=P(A|B)=0.6  =>  P(B)=0.5
_J2 = J(0.3, 0.2, 0.2, 0.3)
_URN = {"counts": {"red": 5, "black": 7}}
_PDF4 = {"pieces": [{"from": 0, "to": 1, "expr": "x"}, {"from": 1, "to": 1.25, "expr": "2"}]}
_ROADS = {"network": {"type": "parallel", "children": [{"type": "comp", "id": c, "p": 0.6} for c in "ABCD"]}}
_QE = "(A == 1 or (B == 1 and C == 1 and D == 1))"
_QS = "(B == 1 or (A == 1 and C == 1 and D == 1))"
_STEPS = {"vars": {("S%d" % i): {"values": [0, 1], "probs": [0.4, 0.6]} for i in range(1, 6)}}
_SUM5 = "S1 + S2 + S3 + S4 + S5 == 3"

SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X1>X2)", "exact": 0.25},
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X1<1/2 or X2<1/2)", "exact": 0.625},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X1+X2<=1)", "exact": 0.25},
    (1, "ד"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X1>1/2 | X1+X2>2)", "exact": 0.75},
    (2, "א"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 1"}, "estimate": "P(A)=p+q ב-p=0.2,q=0.3,s=0.6", "exact": 0.5},
    (2, "ב"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "B == 1"}, "estimate": "P(B)=q/s ב-p=0.2,q=0.3,s=0.6", "exact": 0.5},
    (2, "ג"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 1", "given": "B == 0"}, "estimate": "P(A|not B)=ps/(s-q) ב-p=0.2,q=0.3,s=0.6", "exact": 0.4},
    (2, "ד"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 0", "given": "B == 1"}, "estimate": "P(not A|B)=1-s ב-s=0.6", "exact": 0.4},
    (2, "ה"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 0", "given": "B == 0"}, "estimate": "P(not A|not B) ב-p=0.2,q=0.3,s=0.6", "exact": 0.6},
    # independent: p=0.2, q=0.3, s=p+q=0.5  =>  P(B)=0.6, P(A and B)=0.3=P(A)P(B)
    (2, "ז"): {"kind": "custom_discrete", "params": {"joint": J(0.3, 0.2, 0.3, 0.2), "event": "A == 1 and B == 1"}, "estimate": "P(A and B)=P(A)P(B) ב-p=0.2,q=0.3,s=0.5", "exact": 0.3},
    # Q3: D=5 red of N=12
    (3, "א"): {"kind": "urn", "params": dict(_URN, draws=1, event="red_1 == 1"), "estimate": "P(R1) ב-D=5,N=12", "exact": 5 / 12},
    (3, "ב"): {"kind": "urn", "params": dict(_URN, draws=2, event="red_2 == 1"), "estimate": "P(R2) ב-D=5,N=12", "exact": 5 / 12},
    (3, "ג"): {"kind": "urn", "params": dict(_URN, draws=3, event="red_3 == 1"), "estimate": "P(R3) ב-D=5,N=12", "exact": 5 / 12},
    (3, "ד"): {"kind": "urn", "params": dict(_URN, draws=5, event="red_5 == 1"), "estimate": "P(R5) ב-D=5,N=12,n=5", "exact": 5 / 12},
    (3, "ה"): {"kind": "urn", "params": dict(_URN, draws=5, event="red_4 == 1 and red_5 == 1"), "estimate": "P(R4 and R5) ב-D=5,N=12,n=5", "exact": 5 / 33},
    # Q4: a=1, b=5/4, c=2
    (4, "א"): {"kind": "pdf", "params": dict(_PDF4, measure="mean", expr="x"), "estimate": "E[X]=43/48", "exact": 43 / 48},
    (4, "ב"): {"kind": "pdf", "params": dict(_PDF4, event="x <= 1.1"), "estimate": "F_X(1.1)", "exact": 0.7},
    (4, "ג"): {"kind": "pdf", "params": dict(_PDF4, event="x > 1"), "estimate": "P(X>1)", "exact": 0.5},
    # Q5 at p=0.6
    (5, "א"): {"kind": "circuit", "params": dict(_ROADS, event=_QE), "estimate": "P1 ב-p=0.6", "exact": 0.6 + 0.6 ** 3 - 0.6 ** 4},
    (5, "ב"): {"kind": "circuit", "params": dict(_ROADS, event=_QE + " and " + _QS), "estimate": "P2 ב-p=0.6", "exact": 0.36 * (1 + 1.2 - 0.72)},
    (5, "ג"): {"kind": "circuit", "params": dict(_ROADS, event=_QE + " and not " + _QS), "estimate": "P3 ב-p=0.6", "exact": 0.6 - 0.36 - 0.216 + 0.1296},
    (5, "ד"): {"kind": "circuit", "params": dict(_ROADS, event="A == 1 and B == 1 and C == 1 and D == 1", given=_QE + " and " + _QS),
               "estimate": "P4=P(all four open | both arrive) ב-p=0.6", "exact": 0.36 / (1 + 1.2 - 0.72)},
    # Q6: m=3 steps right, n=2 up, p=0.6
    (6, "ב"): {"kind": "custom_discrete", "params": dict(_STEPS, event=_SUM5), "estimate": "P(reach the corner) ב-m=3,n=2,p=0.6", "exact": 10 * 0.6 ** 3 * 0.4 ** 2},
    (6, "ג"): {"kind": "custom_discrete", "params": dict(_STEPS, event="S1 + S2 == 1", given=_SUM5), "estimate": "P(through (1,1) | reached corner) ב-m=3,n=2 (בלי תלות ב-p)", "exact": 0.6},
}
for _q in questions:
    _s = SIMS.get((_q["num"], _q.get("part")))
    if _s is not None:
        _q["sim"] = _s

# ------------------------------------------------------------------ rubric / pitfalls / steps (ai-draft)
# Every expected value is re-derived independently (exact fractions / enumeration / sympy, and Monte Carlo where a kind
# applies) in tools/verify/25S-A/steps_check.py, which reads the generated raw JSON back.
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


OMEGA = r"מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X_1,X_2)$, כאשר $X_1\sim U(0,1)$ ו-$X_2\sim U(0,2)$?"
OMEGA_X = r"המלבן $(0,1)\times(0,2)$ הוא מרחב המדגם, ושטחו $2$. ההסתברות היא שטח האירוע חלקי $2$."

ADD(1, "א",
    RB((r"גישה גאומטרית: שטח חלקי $|\Omega|=2$", 1), (r"האזור $x_2<x_1$ הוא משולש עם ניצבים $1$ ו-$1$ (הישר $x_2=x_1$ יוצא מהמלבן ב-$x_1=1$)", 3), (r"התשובה $\frac14$", 1)),
    [r"לחלק ב-$1$ ולקבל $\frac12$", r"לחשוב שהמשולש מגיע עד $x_2=2$"],
    [NU(OMEGA, 2, OMEGA_X),
     NU(r"מהו שטח האזור $\{x_2<x_1\}$ בתוך המלבן?", Fr(1, 2), r"משולש ישר-זווית עם ניצבים $1$ ו-$1$: שטח $\frac12$.", region=REGIONS[(1, "א")]),
     NU(r"מהי $P(X_1>X_2)$?", Fr(1, 4), r"$\frac{1/2}{2}=\frac14$.")])

ADD(1, "ב",
    RB((r"כלל החיבור והמשלים", 1), (r"$P(X_1<\frac12)=\frac12$ ו-$P(X_2<\frac12)=\frac14$", 2), (r"התשובה $\frac58$", 2)),
    [r"לחבר $\frac12+\frac14$ בלי לחסר את החיתוך", r"לחשב $P(X_2<\frac12)=\frac12$ במקום $\frac14$ (הטווח של $X_2$ הוא $2$)"],
    [NU(OMEGA, 2, OMEGA_X),
     NU(r"מהו שטח המלבן המשלים $\{x_1\ge\frac12\}\cap\{x_2\ge\frac12\}$?", Fr(3, 4), r"$\frac12\cdot\frac32=\frac34$.", region=REGIONS[(1, "ב")]),
     NU(r"מהי ההסתברות ש-$X_1<\frac12$ או $X_2<\frac12$?", Fr(5, 8), r"$1-\frac{3/4}{2}=\frac58$.")])

ADD(1, "ג",
    RB((r"הצגת האירוע כמשולש מתחת לישר $x_2=1-x_1$", 3), (r"שטח $\frac12$", 2), (r"חלוקה ב-$|\Omega|=2$: $\frac14$", 3)),
    [r"לחלק ב-$1$ ולקבל $\frac12$", r"לבלבל בין $x_1+x_2\le1$ ל-$x_1+x_2\le2$"],
    [NU(OMEGA, 2, OMEGA_X),
     NU(r"מהו שטח האזור $\{x_1+x_2\le1\}$ בתוך המלבן?", Fr(1, 2), r"משולש ישר-זווית עם ניצבים $1$ ו-$1$ (מוכל כולו במלבן).", region=REGIONS[(1, "ג")]),
     NU(r"מהי $P(X_1+X_2\le1)$?", Fr(1, 4), r"$\frac{1/2}{2}=\frac14$.")])

ADD(1, "ד",
    RB((r"הגדרת ההסתברות המותנית כיחס שטחים (המכנה $|\Omega|$ משותף)", 2), (r"שטח התנאי $\{x_2>2-x_1\}$: $\frac12$", 2), (r"שטח החיתוך (טרפז): $\frac38$", 2), (r"היחס $\frac34$", 1)),
    [r"לחלק את שטח החיתוך ב-$|\Omega|=2$ אבל לא את שטח התנאי, או להפך", r"לחשב את שטח החיתוך כמשולש במקום טרפז"],
    [NU(OMEGA, 2, OMEGA_X),
     NU(r"מהו שטח התנאי $\{x_1+x_2>2\}$ בתוך המלבן?", Fr(1, 2), r"משולש עם קודקודים $(0,2)$, $(1,1)$, $(1,2)$: שטח $\frac12$."),
     NU(r"מהו שטח החיתוך $\{x_1>\frac12\}\cap\{x_1+x_2>2\}$?", Fr(3, 8), r"$\int_{1/2}^{1}x_1\,dx_1=\frac38$ (טרפז).", region=REGIONS[(1, "ד")]),
     NU(r"מהי $P(X_1>\frac12\mid X_1+X_2>2)$?", Fr(3, 4), r"$\frac{3/8}{1/2}=\frac34$.")])

# Q2: sample p = 0.2, q = 0.3, s = 0.6
Q2S = r"נקבע $p=0.2$, $q=0.3$, $s=0.6$. "
ADD(2, "א",
    RB((r"פירוק $A$ לחלק שמחוץ ל-$B$ ולחלק שבתוכו", 1), (r"שני החלקים זרים, ולכן מחברים", 1), (r"$P(A)=p+q$", 1)),
    [r"להחסיר את החיתוך ($p+q-q$)"],
    [CH(r"כיצד מחשבים את $P(A)$ מ-$P(A\setminus B)$ ו-$P(A\cap B)$?",
        [r"$P(A)=P(A\setminus B)+P(A\cap B)$: שני חלקים זרים של $A$", r"$P(A)=P(A\setminus B)\cdot P(A\cap B)$", r"$P(A)=P(A\setminus B)+P(A\cap B)-P(A\setminus B)P(A\cap B)$"], 0,
        r"שני החלקים זרים, ולכן אין מה לחסר (השלישית) ואין להכפיל (השנייה: $0.06$ במקום $0.5$)."),
     NU(Q2S + r"מהי $P(A)$?", Fr(1, 2), r"$0.2+0.3=0.5$.")])

ADD(2, "ב",
    RB((r"הגדרת ההסתברות המותנית: $s=\frac{P(A\cap B)}{P(B)}$", 1), (r"חילוץ $P(B)$ מהמשוואה", 1), (r"$P(B)=\frac qs$", 1)),
    [r"להפוך את היחס ולכתוב $\frac sq$ (יוצא גדול מ-$1$)"],
    [CH(r"נתון $P(A\mid B)=s$ ו-$P(A\cap B)=q$. כיצד מחלצים את $P(B)$?",
        [r"$P(B)=\dfrac{P(A\cap B)}{P(A\mid B)}=\dfrac qs$", r"$P(B)=\dfrac sq$", r"$P(B)=q\cdot s$"], 0,
        r"השנייה נותנת $2>1$ בדוגמה, והשלישית נותנת $0.18$ שאינו מקיים $P(A\mid B)=\frac{0.3}{0.18}\ne0.6$."),
     NU(Q2S + r"מהי $P(B)$?", Fr(1, 2), r"$\frac{0.3}{0.6}=0.5$.")])

ADD(2, "ג",
    RB((r"הגדרת ההסתברות המותנית עם התנאי $\overline B$", 1), (r"$P(A\cap\overline B)=P(A\setminus B)=p$", 1), (r"$P(\overline B)=1-\frac qs$ והתשובה $\frac{ps}{s-q}$", 1)),
    [r"לחלק ב-$P(B)$ במקום ב-$P(\overline B)$", r"לכתוב $P(A\cap\overline B)=q$"],
    [CH(r"איזה מאורע הוא $A\cap\overline B$?",
        [r"$A\setminus B$, בהסתברות $p$", r"$A\cap B$, בהסתברות $q$", r"$\overline A\cap B$, בהסתברות $P(B)-q$"], 0,
        r"השנייה היא החלק של $A$ שבתוך $B$, והשלישית אינה חלק מ-$A$ כלל."),
     NU(Q2S + r"מהי הסתברות התנאי $P(\overline B)=1-\frac qs$?", Fr(1, 2), r"$1-0.5=0.5$."),
     NU(r"מהי $P(A\cap\overline B)$?", Fr(1, 5), r"$p=0.2$."),
     NU(r"מהי $P(A\mid\overline B)$?", Fr(2, 5), r"$\frac{0.2}{0.5}=0.4$, כלומר $\frac{ps}{s-q}$.")])

ADD(2, "ד",
    RB((r"משלים בתוך ההתניה: $P(\overline A\mid B)=1-P(A\mid B)$", 1), (r"הצבת הנתון $P(A\mid B)=s$", 1), (r"$P(\overline A\mid B)=1-s$", 1)),
    [r"להחסיר מ-$1$ את $P(A)$ במקום את $P(A\mid B)$"],
    [CH(r"איך מחשבים את $P(\overline A\mid B)$?",
        [r"$1-P(A\mid B)=1-s$", r"$1-P(A)=1-p-q$", r"$1-P(B)$"], 0,
        r"השנייה והשלישית אינן מותנות ב-$B$ (שתיהן נותנות $0.5$ במקום $0.4$)."),
     NU(Q2S + r"מהי $P(\overline A\mid B)$?", Fr(2, 5), r"$1-0.6=0.4$.")])

ADD(2, "ה",
    RB((r"משלים בתוך ההתניה על $\overline B$", 1), (r"שימוש בסעיף ג", 1), (r"$1-\frac{ps}{s-q}$", 1)),
    [r"לחסר מ-$1$ את $P(A\mid B)$ (התנאי הוא $\overline B$)"],
    [CH(r"איך מחשבים את $P(\overline A\mid\overline B)$?",
        [r"$1-P(A\mid\overline B)$", r"$1-P(A\mid B)=1-s$", r"$P(\overline A)=1-p-q$"], 0,
        r"השנייה מותנית באירוע אחר ($0.4$), והשלישית אינה מותנית ($0.5$), בעוד שהנכון הוא $0.6$."),
     NU(Q2S + r"מהי $P(A\mid\overline B)$ (סעיף ג)?", Fr(2, 5), r"$0.4$."),
     NU(r"מהי $P(\overline A\mid\overline B)$?", Fr(3, 5), r"$1-0.4=0.6$.")])

ADD(2, "ו",
    RB((r"$P(B)=\frac qs$ מסעיף א-2", 1), (r"$P(B)\le1$ מחייב $q\le s$", 2), (r"מסקנה: $s<q$ בלתי אפשרי", 2)),
    [r"לענות 'כן' בלי לבדוק ש-$P(B)\le1$"],
    [CH(r"האם ייתכן $s<q$?",
        [r"לא: $P(B)=\frac qs\le1$ מחייב $q\le s$", r"כן: אין קשר בין $s$ ל-$q$", r"כן: כאשר $P(A\cap B)<P(A)$"], 0,
        r"$s=\frac{q}{P(B)}\ge q$ תמיד, כי מחלקים ב-$P(B)\le1$; לכן $s<q$ מובילה לסתירה."),
     NU(r"עבור $q=0.5$ ו-$s=0.4$: מהו $P(B)=\frac qs$?", Fr(5, 4), r"$1.25>1$: לא יתכן.")])

ADD(2, "ז",
    RB((r"אי-תלות: $P(A\mid B)=P(A)$", 2), (r"$P(A)=p+q$", 1), (r"התנאי $s=p+q$", 2)),
    [r"לדרוש $s=p$ או $s=q$", r"לבלבל בין אי-תלות לזרות"],
    [CH(r"איזה תנאי שקול לאי-תלות של $A$ ו-$B$ (כש-$P(B)>0$)?",
        [r"$P(A\mid B)=P(A)$", r"$P(A\cap B)=0$", r"$P(A\mid B)=P(B\mid A)$"], 0,
        r"השני הוא זרות. השלישי נכון רק כש-$P(A)=P(B)$, ואינו שקול לאי-תלות."),
     NU(r"עבור $p=0.2$ ו-$q=0.3$: מהי $P(A)$?", Fr(1, 2), r"$p+q=0.5$."),
     NU(r"איזה $s=P(A\mid B)$ נדרש לאי-תלות?", Fr(1, 2), r"$s=P(A)=0.5=p+q$.")])

# Q3: D = 5 red of N = 12
ADD(3, "א",
    RB((r"הגישה הקלאסית: מקרים רצויים חלקי כל המקרים", 1), (r"$D$ מקרים רצויים מתוך $N$", 1), (r"התשובה $\frac DN$", 1)),
    [r"לחלק ב-$N-D$ במקום ב-$N$"],
    [NU(r"בכד $N=12$ כדורים, מהם $D=5$ אדומים. כמה תוצאות שוות-הסתברות יש להוצאת כדור אחד?", 12, r"$N=12$."),
     NU(r"מהי $P(R_1)$?", Fr(5, 12), r"$\frac DN=\frac5{12}$.")])

ADD(3, "ב",
    RB((r"נוסחת ההסתברות השלמה על הכדור הראשון", 2), (r"$P(R_2/R_1)=\frac{D-1}{N-1}$ ו-$P(R_2/\overline{R_1})=\frac D{N-1}$", 2), (r"פישוט ל-$\frac DN$", 1)),
    [r"להניח שהכדור הראשון אדום", r"לשכוח את הגורם $P(\overline{R_1})$"],
    [CH(r"הכדור הראשון אינו נבדק. כיצד מחשבים את $P(R_2)$?",
        [r"נוסחת ההסתברות השלמה לפי צבע הכדור הראשון", r"$\dfrac{D-1}{N-1}$, כאילו הכדור הראשון היה אדום", r"$\left(\dfrac DN\right)^2$, כאילו ההוצאות בלתי תלויות"], 0,
        r"השנייה מניחה מידע שאין ($0.364$). השלישית מתעלמת מהעובדה שההוצאה ללא החזרה ($0.174$ במקום $0.4167$)."),
     NU(r"עבור $D=5$, $N=12$: מהי $P(R_2/R_1)$?", Fr(4, 11), r"$\frac4{11}$."),
     NU(r"מהי $P(R_2/\overline{R_1})$?", Fr(5, 11), r"$\frac5{11}$."),
     NU(r"מהי $P(R_2)$?", Fr(5, 12), r"$\frac4{11}\cdot\frac5{12}+\frac5{11}\cdot\frac7{12}=\frac5{12}$.")])

ADD(3, "ג",
    RB((r"התניה על תוצאות שני הכדורים הראשונים (4 מקרים)", 2), (r"ההסתברויות $P(R_1\cap R_2)$ וכו' והמותנות $\frac{D-2}{N-2}$ וכו'", 2), (r"פישוט ל-$\frac DN$", 2)),
    [r"לשכוח אחד מארבעת המקרים", r"להשתמש במכנה $N-1$ במקום $N-2$ עבור ההוצאה השלישית"],
    [CH(r"כיצד מחשבים את $P(R_3)$ כאשר שני הכדורים הראשונים אינם נראים?",
        [r"נוסחת ההסתברות השלמה על תוצאות שני הכדורים הראשונים (ארבעה מקרים)", r"$P(R_3)=\dfrac{D-2}{N-2}$, כאילו שני הראשונים אדומים", r"$P(R_3)=P(R_1)P(R_2)P(R_3/R_1\cap R_2)$"], 0,
        r"השנייה מניחה מידע שאין ($0.3$). השלישית היא $P(R_1\cap R_2\cap R_3)$, מאורע אחר ($0.0455$)."),
     NU(r"עבור $D=5$, $N=12$: מהי $P(R_1\cap R_2)$?", Fr(5, 33), r"$\frac5{12}\cdot\frac4{11}=\frac5{33}$."),
     NU(r"מהי $P(R_3/R_1\cap R_2)$?", Fr(3, 10), r"$\frac{D-2}{N-2}=\frac3{10}$."),
     NU(r"מהי $P(R_3)$?", Fr(5, 12), r"סכום ארבעת המחוברים שווה $\frac DN=\frac5{12}$.")])

ADD(3, "ד",
    RB((r"התניה על $X$, מספר האדומים בין $n-1$ הכדורים הראשונים", 4), (r"$P(R_n/X=k)=\frac{D-k}{N-n+1}$", 3), (r"שימוש ב-$\mathbb{E}[X]=(n-1)\frac DN$", 2), (r"פישוט ל-$\frac DN$", 2)),
    [r"להתעלם מכך שהצבעים הקודמים אינם ידועים", r"להניח אי-תלות בין ההוצאות"],
    [CH(r"עבור $n$ כללי, על מה מתנים כדי לחשב את $P(R_n)$?",
        [r"על מספר האדומים $X$ בין $n-1$ הכדורים הראשונים (היפרגיאומטרי)", r"על צבע הכדור הראשון בלבד", r"על כך שכל $n-1$ הכדורים הראשונים אדומים"], 0,
        r"התניה על הראשון בלבד משאירה $n-2$ כדורים בלתי ידועים. התניה על 'כולם אדומים' היא מאורע שונה."),
     NU(r"עבור $D=5$, $N=12$, $n=5$: מהי $\mathbb{E}[X]=(n-1)\frac DN$?", Fr(5, 3), r"$4\cdot\frac5{12}=\frac53$."),
     NU(r"בהינתן $X=2$: מהי $P(R_5\mid X=2)=\frac{D-k}{N-n+1}$?", Fr(3, 8), r"נשארו $8$ כדורים, מהם $3$ אדומים."),
     NU(r"מהי $P(R_5)$?", Fr(5, 12), r"$\frac{D-\mathbb{E}[X]}{N-n+1}=\frac{10/3}{8}=\frac5{12}$.")])

ADD(3, "ה",
    RB((r"התניה על $X$ מבין $m=n-2$ הכדורים הראשונים", 2), (r"$P(R_{n-1}\cap R_n/X=k)=\frac{(D-k)(D-k-1)}{M(M-1)}$", 1), (r"חישוב $\mathbb{E}[(D-X)(D-X-1)]$ והתשובה $\frac{D(D-1)}{N(N-1)}$", 2)),
    [r"לכתוב $\left(\frac DN\right)^2$ (אי-תלות)", r"לחשוב שהתשובה תלויה ב-$n$"],
    [CH(r"איזו תשובה סבירה להסתברות ששני הכדורים האחרונים אדומים?",
        [r"$\dfrac{D(D-1)}{N(N-1)}$: כמו שני הכדורים הראשונים", r"$\left(\dfrac DN\right)^2$", r"$\dfrac{D(D-1)}{(N-n+2)(N-n+1)}$"], 0,
        r"השנייה מניחה אי-תלות ($0.174$ במקום $0.1515$); השלישית תקפה רק אם כל $n-2$ הכדורים הקודמים אדומים."),
     NU(r"עבור $D=5$, $N=12$, $n=5$ ($m=3$): מהי $\mathbb{E}[X]=\frac{mD}N$?", Fr(5, 4), r"$3\cdot\frac5{12}=1.25$."),
     NU(r"בהינתן $X=1$ ($M=9$): מהי $P(R_4\cap R_5\mid X=1)=\frac{(D-k)(D-k-1)}{M(M-1)}$?", Fr(1, 6), r"$\frac{4\cdot3}{9\cdot8}=\frac16$."),
     NU(r"מהי $P(R_4\cap R_5)$?", Fr(5, 33), r"$\frac{D(D-1)}{N(N-1)}=\frac{20}{132}=\frac5{33}\approx0.1515$.")])

# Q4: a = 1, b = 5/4, c = 2
ADD(4, "א",
    RB((r"נרמול $\frac{ac}4+c(b-a)=1$ ושוויון השטחים: כל אחד $\frac12$", 4), (r"תנאי התוחלת $\frac{ca^2}6+c\frac{b^2-a^2}2=\frac{43}{48}$", 3), (r"פתרון: $a=1$, $b=\frac54$, $c=2$", 3)),
    [r"לדרוש רציפות ב-$x=a$ (הצפיפות קופצת מ-$\frac c2$ ל-$c$)", r"לחשב את התוחלת של החלק הראשון עם $x\cdot\frac{c}{2a}$ במקום $x\cdot\frac{cx}{2a}$"],
    [CH(r"אילו תנאים קובעים את $a,b,c$?",
        [r"נרמול, שוויון שני השטחים ($\frac12$ כל אחד), ותנאי התוחלת: שלוש משוואות", r"נרמול ורציפות הצפיפות ב-$x=a$", r"נרמול בלבד"], 0,
        r"הצפיפות קופצת ב-$x=a$ (מ-$\frac c2$ ל-$c$), ולכן רציפות אינה תנאי. נרמול לבדו הוא משוואה אחת לשלושה נעלמים."),
     NU(r"מהו $a$? (מ-$\frac{ac}4=\frac12$ ו-$c(b-a)=\frac12$ ותוחלת)", 1, r"מתקבל $c=\frac2a$, $b=\frac54a$ והתוחלת $\frac{43}{48}a=\frac{43}{48}$, כלומר $a=1$."),
     NU(r"מהו $b$?", Fr(5, 4), r"$b=\frac54a=\frac54$."),
     NU(r"מהו $c$?", 2, r"$c=\frac2a=2$.")])

ADD(4, "ב",
    RB((r"$F_X(t)=\frac{t^2}2$ עבור $0\le t<1$", 3), (r"$F_X(t)=\frac12+2(t-1)$ עבור $1\le t<\frac54$", 4), (r"$F_X=0$ משמאל ו-$1$ מימין, ובדיקת רציפות", 3)),
    [r"לשכוח את הקבוע $\frac12$ בענף האמצעי"],
    [NU(r"מהו $F_X(1)$ (נקודת החיבור)?", Fr(1, 2), r"$\frac{1^2}2=\frac12$."),
     NU(r"מהו $F_X(1.1)$?", Fr(7, 10), r"$\frac12+2(0.1)=0.7$."),
     NU(r"מהו $F_X(\frac54)$?", 1, r"$\frac12+2\cdot\frac14=1$.")])

ADD(4, "ג",
    RB((r"$P(X>1)=1-F_X(1)$", 2), (r"הצבת $F_X(1)=\frac12$", 2), (r"התשובה $\frac12$", 1)),
    [r"לחשב $F_X(1)$ במקום המשלים"],
    [NU(r"מהי $P(0\le X\le1)=F_X(1)$?", Fr(1, 2), r"שטח המשולש $\frac{ac}4=\frac12$."),
     NU(r"מהי $P(X>1)$?", Fr(1, 2), r"$1-\frac12=\frac12$ (שטח המלבן $2\cdot\frac14$).")])

# Q5: p = 0.6
ADD(5, "א",
    RB((r"זיהוי הדרכים: ישירות דרך $A$, או דרך $C,D,B$ יחד", 2), (r"$Q_E=A\cup(B\cap C\cap D)$", 2), (r"חיבור-חיסור: $p+p^3-p^4$", 2)),
    [r"לכתוב $A\cup B\cup C\cup D$ (אף כביש בודד מלבד $A$ אינו מספיק)", r"לשכוח את חיסור החיתוך $A\cap B\cap C\cap D$"],
    [CH(r"איזה ביטוי מתאר את הצלחתו של יוג'ין להגיע למכון?",
        [r"$A\cup(B\cap C\cap D)$", r"$A\cap B\cap C\cap D$", r"$A\cup B\cup C\cup D$"], 0,
        r"השנייה דורשת שכל הכבישים יהיו פתוחים (גם כשרק $A$ פתוח הוא מגיע), והשלישית מניחה שכל כביש בודד מספיק (אבל $B$ לבדו לא מביא אותו למכון)."),
     NU(r"עבור $p=0.6$: מהי $P(B\cap C\cap D)$?", Fr(27, 125), r"$p^3=0.216$."),
     NU(r"מהי $P_1=p+p^3-p^4$?", Fr(1716, 2500), r"$0.6+0.216-0.1296=0.6864$.")])

ADD(5, "ב",
    RB((r"התניה על $A$", 2), (r"$P(\tilde Q/A)=P(B\cup(C\cap D))$", 2), (r"$P(\tilde Q/\overline A)=p^3$ והרכבה", 2)),
    [r"להניח ש-$Q_E,Q_S$ בלתי תלויים ולכפול", r"לשכוח שכש-$A$ כבוי, $Q_S$ מתקיים אוטומטית בתוך $Q_E$"],
    [CH(r"כיצד מחשבים את $P(Q_E\cap Q_S)$ בצורה הנוחה ביותר?",
        [r"נוסחת ההסתברות השלמה על $A$ (כש-$A$ פועל $Q_E$ מתקיים; כשהוא כבוי $Q_E$ דורש את $B\cap C\cap D$)", r"$P(Q_E)\cdot P(Q_S)$, כי שני האנשים בלתי תלויים", r"$P(Q_E)+P(Q_S)$"], 0,
        r"האירועים תלויים (אותם כבישים): המכפלה נותנת $0.471$ במקום $0.533$. הסכום עולה על $1$."),
     NU(r"עבור $p=0.6$: מהי $P(\tilde Q/A)=p+p^2-p^3$?", 0.744, r"$0.6+0.36-0.216=0.744$."),
     NU(r"מהי $P(\tilde Q/\overline A)=p^3$?", 0.216, r"$B,C,D$ כולם פתוחים."),
     NU(r"מהי $P_2$?", 0.5328, r"$0.6\cdot0.744+0.4\cdot0.216=0.5328$.")])

ADD(5, "ג",
    RB((r"$Q_E\cap\overline{Q_S}=Q_E\setminus(Q_E\cap Q_S)$", 3), (r"$P_3=P_1-P_2$", 2), (r"פישוט", 1)),
    [r"לכתוב $P_1(1-P_1')$ בשל תלות"],
    [CH(r"איך מחשבים את $P(Q_E\cap\overline{Q_S})$?",
        [r"$P(Q_E)-P(Q_E\cap Q_S)$", r"$P(Q_E)\,(1-P(Q_S))$", r"$1-P(Q_E\cap Q_S)$"], 0,
        r"השנייה מניחה אי-תלות ($0.2153$ במקום $0.1536$). השלישית כוללת מצבים בהם $Q_E$ לא קורה."),
     NU(r"עבור $p=0.6$: מהי $P_1$?", 0.6864, r"סעיף א."),
     NU(r"מהי $P_3=P_1-P_2$?", 0.1536, r"$0.6864-0.5328=0.1536$.")])

ADD(5, "ד",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$Q_{PUB}\cap Q_E\cap Q_S=A\cap B\cap C\cap D$", 2), (r"$P(\ldots)=p^4$", 2), (r"היחס $\frac{p^2}{1+2p-2p^2}$", 2)),
    [r"לחלק ב-$P_1$ או ב-$P_3$ במקום ב-$P_2$", r"לשכוח ש-$P_2$ הוא המכנה (התנאי: שניהם הגיעו)"],
    [CH(r"איזו קבוצת כבישים חייבת להיות פתוחה כדי ששניהם יגיעו ושניהם יעברו בפאב?",
        [r"כל ארבעת הכבישים $A,B,C,D$", r"$A$ ו-$B$ בלבד", r"$C$ ו-$D$ בלבד"], 0,
        r"דרך הפאב היא $C,D$ ועוד $B$ (יוג'ין) או $A$ (סרג'), ולשניהם יחד נדרשים כל ארבעת הכבישים. $C,D$ בלבד אינם מספיקים להגיע."),
     NU(r"עבור $p=0.6$: מהי הסתברות התנאי $P_2=P(Q_E\cap Q_S)$?", 0.5328, r"סעיף ב."),
     NU(r"מהי $P(A\cap B\cap C\cap D)=p^4$?", 0.1296, r"$0.6^4=0.1296$."),
     NU(r"מהי $P_4$?", 0.1296 / 0.5328, r"$\frac{0.1296}{0.5328}=\frac{p^2}{1+2p-2p^2}\approx0.2432$.")])

# Q6: m = 3 right, n = 2 up, p = 0.6
ADD(6, "א",
    RB((r"נדרשות $m$ קפיצות ימינה", 2), (r"ו-$n$ קפיצות למעלה", 2), (r"סך הכול $n+m$", 1)),
    [r"לספור $nm$ או $\max(n,m)$"],
    [NU(r"עבור $m=3$ ו-$n=2$: כמה קפיצות נדרשות?", 5, r"$m+n=5$."),
     NU(r"בכמה סדרים שונים אפשר לסדר $3$ קפיצות ימינה ו-$2$ קפיצות למעלה?", 10, r"$\binom53=10$.")])

ADD(6, "ב",
    RB((r"מספר הקפיצות ימינה מתוך $n+m$ הוא בינומי", 4), (r"ההסתברות היא $P(X=m)$", 3), (r"$\binom{n+m}mp^m(1-p)^n$", 3)),
    [r"לשכוח את $\binom{n+m}m$ (מספר הסדרים)", r"להחליף את התפקידים של $p$ ו-$1-p$"],
    [CH(r"כיצד מחשבים את ההסתברות להגיע לפינה הימנית העליונה?",
        [r"$X\sim\mathrm{Bin}(n+m,p)$ ו-$P(X=m)$: כל סדר של $m$ ימינה ו-$n$ למעלה מתאים", r"$p^m(1-p)^n$: מסלול אחד בלבד", r"$P(X\ge m)$"], 0,
        r"הראשון בלבד סופר את כל המסלולים. השני מתאים למסלול אחד ספציפי ($0.0346$ במקום $0.3456$). השלישי מכליל גם מקרים של יותר מ-$m$ קפיצות ימינה (שמחטיאים את הפינה)."),
     NU(r"עבור $m=3$, $n=2$: כמה מסלולים אפשריים?", 10, r"$\binom53=10$."),
     NU(r"מהי ההסתברות של מסלול ספציפי אחד, $p^3(1-p)^2$, עבור $p=0.6$?", 0.03456, r"$0.216\cdot0.16=0.03456$.", ),
     NU(r"מהי ההסתברות להגיע לפינה?", 0.3456, r"$10\cdot0.03456=0.3456$.")])

ADD(6, "ג",
    RB((r"הגדרת ההסתברות המותנית ופירוק המסלול דרך הנקודה", 3), (r"אי-תלות בין שני החלקים", 2), (r"הצמצום של $p$ והתוצאה ההיפרגיאומטרית", 5)),
    [r"לחשוב שהתשובה תלויה ב-$p$", r"לשכוח את המקדם הבינומי של אחד החלקים"],
    [CH(r"בהינתן שהחלקיק הגיע לפינה, מדוע ההסתברות לעבור דרך נקודה נתונה אינה תלויה ב-$p$?",
        [r"כל מסלול מוצלח כולל אותה כמות קפיצות ימינה ולמעלה, ולכן לכל המסלולים הסתברות זהה ו-$p$ מצטמצם", r"כי $p=\frac12$", r"כי העבר אינו משפיע על העתיד"], 0,
        r"השנייה אינה נתונה. השלישית נכונה לגבי אי-התלות בין הצעדים, אך אינה מסבירה את הצמצום: צריך שלכל המסלולים המוצלחים אותה הסתברות."),
     NU(r"עבור $m=3$, $n=2$, $p=0.6$, והנקודה $(1,1)$: מהי $P(A\to R)=\binom21p(1-p)$?", 0.48, r"$2\cdot0.6\cdot0.4=0.48$."),
     NU(r"מהי $P(R\to B)=\binom32p^2(1-p)$?", 0.432, r"$3\cdot0.36\cdot0.4=0.432$."),
     NU(r"מהי $P(Q_{A\to B})$?", 0.3456, r"סעיף ב."),
     NU(r"מהי ההסתברות המותנית?", Fr(3, 5), r"$\frac{0.48\cdot0.432}{0.3456}=0.6=\frac{\binom21\binom32}{\binom53}$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = _vsrc(CODE)
        _q["stepsSource"] = _vsrc(CODE)

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר קיץ תשפ״ה, מועד א (20.10.2025)",
    "year": 2025,
    "examDate": "20.10.2025",
    "sourceFile": "25S-A exam pp.1-3",
    "solutionFile": "25S-A handwritten official solutions pp.4-15",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: החגב", "image": IMG + "Q1-grasshopper.png", "caption": Q1_CAP},
        "c2": {"kind": "text", "title": "שאלה 2: מאורעות", "text": Q2_CAP},
        "c3": {"kind": "image", "title": "שאלה 3: כד", "image": IMG + "Q3-urn.png", "caption": Q3_CAP},
        "c4": {"kind": "image", "title": "שאלה 4", "image": IMG + "Q4-pdf.png", "caption": Q4_CAP},
        "c5": {"kind": "image", "title": "שאלה 5: מפת כבישים", "image": IMG + "Q5-map.png", "caption": Q5_CAP},
        "c6": {"kind": "image", "title": "שאלה 6: רשת", "image": IMG + "Q6-grid.png", "caption": Q6_CAP},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
