# -*- coding: utf-8 -*-
"""Generator for tools/raw/24S-B.json -- probability (course 20021), semester C 2024, moed B (07.11.2024).
6 questions, 19 items (Q1 4, Q2 4, Q3 4, Q4 3, Q5 2, Q6 2), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24S-B.py

Source: exam pp.1-3, handwritten official solutions pp.4-13 (grid paper). Q5 is solved in English on p.10 (page of
a different hand, no name on it).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, a-3, b, stored as a b c d. Map: Q1 a=א-1, b=א-2, c=א-3, d=ב.
- Q1 area items (a, b, c) have region data in tools/verify/24S-B/regions.json (no `region` field in RAW_SCHEMA).
- Q3 here defines Y as the number of heads in all THREE tosses (different from 24S-A Q3).
- Q4(א): the official line "E[X]=0 => a=b" is justified in the text by integrating x f(x) on both tails (the
  official note is only partly legible; the calculation is exact).
- Q5(ב): the official answer is stated for even n only (n red balls are added in pairs); for odd n the probability is 0.
- Q6 (the 9-unit circuit) is a recursive structure: an outer 5-element part with the inner 5-unit bridge E as one element.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24S-B.json"
CODE = "24S-B"
IMG = "images/exams/24S-B-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_LEAD = (r"לפניך מלבן בעל צלעות אשר אורכן $X$ ו-$Y$ מהווים משתנים מקריים בלתי תלויים: $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,1)$. "
           r"יהי $S$ שטח המלבן ויהי $L$ אורך האלכסון.")

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א-1:** מצאו את ההסתברות $P(S<1/2)$.",
    r"""$S=XY$. נשתמש בגישה הגאומטרית: $\Omega$ הוא ריבוע היחידה, $|\Omega|=1$.
$$P(S<\tfrac12)=P(XY<\tfrac12)=P\left(Y<\tfrac1{2X}\right)=\frac{|\{y<\frac1{2x}\}|}{|\Omega|}.$$
עבור $0<x<\frac12$ מתקיים $\frac1{2x}>1$, ולכן כל $y\in(0,1)$ מתאים (שטח $\frac12$); עבור $\frac12<x<1$ השטח מתחת להיפרבולה $y=\frac1{2x}$ הוא האינטגרל. לכן
$$|\{y<\tfrac1{2x}\}|=\frac12+\int_{1/2}^1\frac{dx}{2x}=\frac12+\frac12\ln x\Big|_{1/2}^1=\frac12+\frac12\ln2.$$
$$P(S<\tfrac12)=\frac12+\frac12\ln2\approx0.85.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**א-2:** מצאו את ההסתברות $P(L<1/2)$.",
    r"""$L=\sqrt{X^2+Y^2}$, ולכן
$$P(L<\tfrac12)=P(X^2+Y^2<\tfrac14)=|\{x^2+y^2<\tfrac14\}|.$$
האזור הוא רבע עיגול ברדיוס $\frac12$ (בתוך ריבוע היחידה), ושטחו
$$\frac14\pi R^2\Big|_{R=1/2}=\frac\pi{16}.$$
$$P(L<\tfrac12)=\frac\pi{16}\approx0.20.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**א-3:** מצאו את ההסתברות המותנית $P(S<1/5\ /\ X>1/2)$.",
    r"""לפי הגדרת ההסתברות המותנית:
$$P(S<\tfrac15\mid X>\tfrac12)=\frac{P(Y<\frac1{5X}\cap X>\frac12)}{P(X>\frac12)},\qquad P(X>\tfrac12)=\frac12.$$
באזור $\frac12<x<1$ מתקיים $\frac1{5x}<\frac25<1$, ולכן השטח מתחת להיפרבולה $y=\frac1{5x}$ הוא האינטגרל, ו-$|\Omega|=1$:
$$P(S<\tfrac15\mid X>\tfrac12)=2\cdot|\{y<\tfrac1{5x}\cap x>\tfrac12\}|=2\int_{1/2}^1\frac{dx}{5x}=\frac25\ln2\approx0.28.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"**ב:** חשבו תוחלת $\mathbb{E}[S]$ ושונות $\operatorname{var}[S]$ של שטח המלבן.",
    r"""מאחר ש-$X,Y$ בלתי תלויים ו-$S=XY$:
$$\mathbb{E}[S]=\mathbb{E}[X]\,\mathbb{E}[Y]=\frac12\cdot\frac12=\frac14.$$
$$\operatorname{Var}[S]=\mathbb{E}[X^2Y^2]-\left(\mathbb{E}[S]\right)^2=\mathbb{E}[X^2]\,\mathbb{E}[Y^2]-\frac1{16}=\frac19-\frac1{16}=\frac7{144},$$
כאשר $\mathbb{E}[X^2]=\int_0^1x^2dx=\frac13$.""",
    6, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_LEAD = (r"מטילים קובייה מאוזנת **פעמיים** על מנת לקבוע את המקדמים $X_1$ ו-$X_2$ במשוואה הריבועית"
           "\n" r"$$y^2-(X_1+X_2)y+X_1X_2=0.$$"
           "\n" r"כאן $X_1$ ו-$X_2$ הם משתנים מקריים המסמנים את תוצאות ההטלה הראשונה והשנייה בהתאמה.")

questions.append(Q(
    2, "א", "combinatorics",
    r"מהי ההסתברות שיש למשוואה שני שורשים זהים?",
    r"""$X_1,X_2\sim U_d(1,6)$. שורשי המשוואה הם
$$y_{1,2}=\frac{X_1+X_2\pm\sqrt{(X_1+X_2)^2-4X_1X_2}}{2}=\frac{X_1+X_2\pm|X_1-X_2|}{2}.$$
אם $X_1=X_2$ השורשים זהים ($y_{1,2}=X_1$); אם $X_1\ne X_2$ השורשים הם $y_1=X_1$, $y_2=X_2$. לכן
$$P(X_1=X_2)=\sum_{k=1}^6P(X_1=k\cap X_2=k)=\frac16\cdot\frac16\cdot6=\frac16.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ב", "combinatorics",
    r"מהי ההסתברות ששורשי המשוואה יהוו **מספרים שלמים**?",
    r"""מאחר ש-$X_1$ ו-$X_2$ מקבלים ערכים שלמים (השורשים הם $X_1$ ו-$X_2$ עצמם):
$$P(y_{1,2}\ \text{integers})=1.$$""",
    6, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"**אם ידוע** כי יש למשוואה שני שורשים שונים, מהי ההסתברות שהכפל ביניהם יהווה מספר אי זוגי?",
    r"""$$P(y_1y_2\ \text{odd}\mid y_1\ne y_2)=P(X_1X_2\ \text{odd}\mid X_1\ne X_2)=\frac{P(X_1X_2\ \text{odd}\cap X_1\ne X_2)}{P(X_1\ne X_2)}.$$
המכפלה אי-זוגית אם ורק אם שני המספרים אי-זוגיים (3 ערכים אפשריים לכל אחד), ושונים: $3\cdot2=6$ זוגות מתוך 36, כלומר $\frac6{36}$. ו-$P(X_1\ne X_2)=1-\frac16=\frac56$. לכן
$$=\frac{6/36}{5/6}=\frac15.$$""",
    7, contextId="c2"))

questions.append(Q(
    2, "ד", "conditional_bayes",
    r"**אם ידוע** כי יש למשוואה שני שורשים שונים, מהי ההסתברות שההפרש ביניהם יהווה מספר זוגי?",
    r"""$$P(y_1-y_2\ \text{even}\mid y_1\ne y_2)=P(X_1-X_2\ \text{even}\mid X_1\ne X_2)=\frac{P(X_1-X_2\ \text{even}\cap X_1\ne X_2)}{P(X_1\ne X_2)}.$$
ההפרש זוגי אם ורק אם שני המספרים באותה זוגיות; ושונים: $3\cdot2+3\cdot2=12$ זוגות מתוך 36. לכן
$$=\frac{12/36}{5/6}=\frac25.$$""",
    7, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_LEAD = (r"מטילים מטבע מוטה **שלוש** פעמים; ההסתברות לתוצאות ״עץ״ הינה $P(H)=p$. נגדיר שני משתנים מקריים: "
           r"$X=\{$מספר תוצאות ״עץ״ בשתי ההטלות הראשונות$\}$ ו-$Y=\{$מספר תוצאות ״עץ״ בסדרה של שלוש ההטלות$\}$.")

questions.append(Q(
    3, "א", "joint_discrete",
    r"מצאו את פונקציית ההסתברות המשותפת $P_{XY}(x,y)$ וודאו כי תכונת הנרמול מתקיימת.",
    r"""נגדיר $X_1,X_2,X_3\sim\mathrm{Ber}(p)$ בלתי תלויים (תוצאות שלוש ההטלות; $1$ = ״עץ״). אז $X=X_1+X_2$ ו-$Y=X_1+X_2+X_3$.
נמנה את שמונה התוצאות האפשריות:
$$\begin{array}{c|cccccccc}X_1&0&1&0&0&1&1&0&1\\ \hline X_2&0&0&1&0&1&0&1&1\\ \hline X_3&0&0&0&1&0&1&1&1\\ \hline X&0&1&1&0&2&1&1&2\\ \hline Y&0&1&1&1&2&2&2&3\end{array}$$
ההסתברות המשותפת:
$$\begin{array}{c|cccc|c}x\backslash y&0&1&2&3&P_X(x)\\ \hline 0&(1-p)^3&p(1-p)^2&0&0&(1-p)^2\\ 1&0&2p(1-p)^2&2p^2(1-p)&0&2p(1-p)\\ 2&0&0&p^2(1-p)&p^3&p^2\\ \hline P_Y(y)&(1-p)^3&3p(1-p)^2&3p^2(1-p)&p^3&1\end{array}$$
סכום כל המשבצות הוא $1$, ולכן תכונת הנרמול מתקיימת.""",
    11, contextId="c3"))

questions.append(Q(
    3, "ב", "joint_discrete",
    r"מצאו את פונקציות ההתפלגות השוליות $P_X(x)$ ו-$P_Y(y)$.",
    r"""לפי משפט הפירוק, $X=X_1+X_2$ ו-$Y=X_1+X_2+X_3$ הם סכומים של ברנולי בלתי תלויים:
$$X\sim\mathrm{Bin}(2,p),\qquad Y\sim\mathrm{Bin}(3,p).$$
כלומר $P_X(x)=\binom2xp^x(1-p)^{2-x}$, $x=0,1,2$, ו-$P_Y(y)=\binom3yp^y(1-p)^{3-y}$, $y=0,1,2,3$ (כפי שמופיע בשולי הטבלה).""",
    6, contextId="c3"))

questions.append(Q(
    3, "ג", "discrete_rv",
    r"חשבו את התוחלות $\mathbb{E}[X]$, $\mathbb{E}[Y]$ והשונויות $\operatorname{var}[X]$, $\operatorname{var}[Y]$.",
    r"""מאחר ש-$X\sim\mathrm{Bin}(2,p)$ ו-$Y\sim\mathrm{Bin}(3,p)$:
$$\mathbb{E}[X]=2p,\quad\mathbb{E}[Y]=3p,\qquad\operatorname{Var}[X]=2p(1-p),\quad\operatorname{Var}[Y]=3p(1-p).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ד", "independence",
    r"האם $X$ ו-$Y$ הם משתנים מקריים בלתי תלויים? נמקו והסבירו!",
    r"""**לא, המשתנים תלויים.** אילו היו בלתי תלויים היה מתקיים $P_{XY}(x,y)=P_X(x)P_Y(y)$ לכל $(x,y)$. אבל ב-$(x,y)=(2,0)$ מתקיים $P_{XY}(2,0)=0$ (אם שתי ההטלות הראשונות ״עץ״ אי אפשר שבסך הכול אפס ״עץ״), בעוד $P_X(2)P_Y(0)=p^2(1-p)^3>0$ עבור $0<p<1$.""",
    4, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_FX = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות מהצורה:" "\n"
         r"$$f_X(x)=\begin{cases}a\,e^{x},&x<-1\\1/4,&-1\le x<1\\b\,e^{-x},&x\ge1\end{cases}$$")

questions.append(Q(
    4, "א", "continuous_rv",
    r"**א:** בהנחה כי $\mathbb{E}[X]=0$, מצאו את הפרמטרים $a$ ו-$b$.",
    r"""**נרמול.**
$$a\int_{-\infty}^{-1}e^xdx+\frac14\cdot2+b\int_1^\infty e^{-x}dx=1\ \Longrightarrow\ \frac ae+\frac12+\frac be=1\ \Longrightarrow\ a+b=\frac e2.$$
**תוחלת.** $\mathbb{E}[X]=0$. הצפיפות על $(-1,1)$ סימטרית ותורמת $0$, ולכן
$$\mathbb{E}[X]=a\int_{-\infty}^{-1}xe^xdx+b\int_1^\infty xe^{-x}dx=-\frac{2a}{e}+\frac{2b}{e}=0\ \Longrightarrow\ a=b.$$
מכאן
$$a=b=\frac e4.$$""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"**ב:** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את התוצאה.",
    r"""$$F_X(t)=P(X\le t)=\int_{-\infty}^tf_X(x)\,dx=\begin{cases}\dfrac e4e^{t},&t<-1,\\[2mm] \dfrac12+\dfrac t4,&-1\le t<1,\\[2mm] 1-\dfrac e4e^{-t},&t\ge1.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת F_X(t)](images/exams/24S-B-Q4-cdf.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"**ג:** מהי ההסתברות המותנית $P(X>-2\ /\ X<3)$?",
    r"""$$P\left(X>-2\ \Big|\ X<3\right)=\frac{P(-2<X<3)}{P(X<3)}=\frac{F_X(3)-F_X(-2)}{F_X(3)}.$$
$F_X(3)=1-\frac1{4e^2}$ ו-$F_X(-2)=\frac1{4e}$, לכן
$$=\frac{4e^2-e-1}{4e^2-1}\approx0.99.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_LEAD = (r"בכד נמצאים $D$ כדורים אדומים ו-$(N-D)$ כדורים שחורים. מוסיפים כדורים לכד באופן הבא: מטילים מטבע מוטה "
           r"(הסתברות לקבלת ״עץ״ הינה $p$) $M$ פעמים. אם יתקבל ״עץ״, מוסיפים לכד שני כדורים אדומים; אם יתקבל ״פלי״ – מוסיפים שני כדורים שחורים. "
           r"בתום $M$ ההטלות, מערבבים היטב את הכדורים בכד ומוציאים כדור אחד.")

questions.append(Q(
    5, "א", "special_discrete",
    r"מה ההסתברות שהוא בצבע אדום?",
    r"""נסמן ב-$X$ את מספר ה״עץ״ ב-$M$ ההטלות: $X\sim\mathrm{Bin}(M,p)$, $P(X=k)=\binom Mkp^k(1-p)^{M-k}$, $k=0,1,\ldots,M$.
בהינתן $X=k$ מוסיפים $2k$ כדורים אדומים ו-$2(M-k)$ שחורים, ובכד $N+2M$ כדורים מתוכם $D+2k$ אדומים. לפי נוסחת ההסתברות השלמה:
$$P(\text{red})=\sum_{k=0}^MP(\text{red}\mid X=k)P(X=k)=\sum_{k=0}^M\frac{D+2k}{N+2M}P(X=k)=\frac1{N+2M}\bigl\{D+2\mathbb{E}[X]\bigr\},\qquad\mathbb{E}[X]=pM.$$
לכן
$$P(\text{red})=\frac{D+2pM}{N+2M}.$$""",
    15, contextId="c5"))

questions.append(Q(
    5, "ב", "conditional_bayes",
    r"אם ידוע כי הכדור שהוצא הינו בצבע אדום, מה ההסתברות שהוספו לכד בדיוק $n$ כדורים אדומים במהלך ההטלות? האם התשובה תלויה בזוגיות של $n$?",
    r"""כדורים אדומים מתווספים בזוגות, ולכן $n$ כדורים אדומים נוספו אם ורק אם התקבלו $\frac n2$ פעמים ״עץ״ – ורק עבור $n$ **זוגי**. כלומר התשובה תלויה בזוגיות של $n$: עבור $n$ אי-זוגי ההסתברות היא $0$.
עבור $n$ זוגי, לפי נוסחת בייס:
$$P\left(X=\tfrac n2\mid\text{red}\right)=\frac{P(\text{red}\mid X=\frac n2)P(X=\frac n2)}{P(\text{red})}=\frac{D+n}{2M+N}\cdot\binom M{n/2}p^{n/2}(1-p)^{M-n/2}\cdot\frac{N+2M}{D+2pM}.$$
$$=\frac{D+n}{D+2pM}\binom M{n/2}p^{n/2}(1-p)^{M-n/2}\qquad(n\ \text{even only}).$$""",
    10, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_LEAD = (r"מעגל חשמלי מורכב מתשע יחידות הפועלות ללא תלות אחת בשנייה בהסתברות $p$ (ראו ציור). "
           r"המעגל כולל טבעת חיצונית עם ארבע יחידות (שתיים בכל חצי טבעת, בין הצומת העליון לתחתון) וטבעת פנימית עם חמש יחידות: "
           r"ארבע יחידות על הטבעת הפנימית (אחת מהן $A$) ויחידה אחת במרכז המחוברת בין הצומת השמאלי לימני של הטבעת הפנימית. "
           r"הטבעת הפנימית מחוברת בקווים אנכיים לצומת העליון והתחתון של הטבעת החיצונית.")

questions.append(Q(
    6, "א", "circuits",
    r"מצאו את ההסתברות $P_0$ שמעגל כולו פועל.",
    r"""נתייחס למעגל הנתון כמעגל שבו החלק הפנימי (הטבעת הפנימית עם חמש היחידות) מסומן כיחידה עצמאית $E$. אז המעגל $Q$ הוא $E$ במקביל לשני ענפים בני שתי יחידות בטור כל אחד (הטבעת החיצונית).
באמצעות נוסחת ההסתברות השלמה:
$$P(Q)=P(Q\mid E)P(E)+P(Q\mid\bar E)P(\bar E),\qquad P(Q\mid E)=1,\qquad P(Q\mid\bar E)=2p^2-p^4.$$
לכן
$$P(Q)=P(E)+(2p^2-p^4)(1-P(E))\quad\Longrightarrow\quad P(Q)=p^2(2-p^2)+(1-p^2)^2P(E).$$
**חישוב $P(E)$.** הטבעת הפנימית היא גשר: היחידה המרכזית $B$ והארבע האחרות. נפצל לפי $B$:
$$P(E)=P(E\mid B)P(B)+P(E\mid\bar B)P(\bar B)=(2p-p^2)^2\,p+(2p^2-p^4)(1-p)=p^3(2-p)^2+p^2(2-p^2)(1-p).$$
ולכן
$$P_0=P(Q)=p^2(2-p^2)+(1-p^2)^2P(E),\qquad P(E)=p^3(2-p)^2+p^2(2-p^2)(1-p).$$""",
    20, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"אם ידוע כי מעגל כולו פועל, מהי ההסתברות $P_1$ שיחידה $A$ **לא** פועלת?",
    r"""לפי נוסחת בייס:
$$P(\bar A\mid Q)=\frac{P(Q\mid\bar A)P(\bar A)}{P(Q)},\qquad P(\bar A)=1-p,\quad P(Q)=P_0.$$
יש לחשב את $P(Q\mid\bar A)$: כאשר $A$ אינה פועלת, הטבעת הפנימית $E$ היא יחידה אחת בטור עם מקבץ, ו
$$P(E\mid\bar A)=p\,(p+p^2-p^3)=p^2(1+p-p^2).$$
(כאשר $A$ כבויה, הגשר הפנימי הוא יחידה אחת בטור עם מקבץ של היחידה התחתונה השמאלית במקביל לשתי יחידות בטור: $p\cdot\bigl(p+p^2-p^3\bigr)$.)
לכן
$$P(Q\mid\bar A)=p^2(2-p^2)+(1-p^2)^2\,p^2(1+p-p^2),$$
ובהצבה
$$P_1=\frac{p^2(2-p^2)+(1-p^2)^2\cdot p^2(1+p-p^2)}{P_0}\cdot(1-p).$$""",
    5, contextId="c6"))

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר ג׳ תשפ״ד, מועד ב (07.11.2024)",
    "year": 2024,
    "examDate": "07.11.2024",
    "sourceFile": "24S-B exam pp.1-3",
    "solutionFile": "24S-B official handwritten solutions pp.4-13",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: מלבן", "image": IMG + "Q1-rect.png", "caption": Q1_LEAD},
        "c2": {"kind": "text", "title": "שאלה 2", "text": Q2_LEAD},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_LEAD},
        "c4": {"kind": "text", "title": "שאלה 4", "text": Q4_FX},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_LEAD},
        "c6": {"kind": "image", "title": "שאלה 6: מעגל חשמלי", "image": IMG + "Q6-circuit.png", "caption": Q6_LEAD},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
