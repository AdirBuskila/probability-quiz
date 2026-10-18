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
- Q1 region data: tools/verify/25S-A/regions.json (RAW_SCHEMA has no `region` field).
- The page-1 cover (lecturer names) is not copied anywhere.
"""
import json, pathlib

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
$$P(A/\bar B)=\frac{P(A\cap\bar B)}{P(\bar B)}=\frac{P(A\setminus B)}{1-P(B)}=\frac{p}{1-\frac qs}=\frac{ps}{s-q}.$$""",
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
$$P(\bar A/\bar B)=1-P(A/\bar B)=1-\frac{ps}{s-q}.$$""",
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
$$P_4=\frac{p^4}{P_2}=\frac{p^2}{1+2p-2p^2}.$$""",
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
