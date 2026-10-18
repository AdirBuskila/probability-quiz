# -*- coding: utf-8 -*-
"""Generator for tools/raw/24S-B.json -- probability (course 20021), semester C 2024, moed B (07.11.2024).
6 questions, 19 items (Q1 4, Q2 4, Q3 4, Q4 3, Q5 2, Q6 2), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24S-B.py

Source: exam pp.1-3, handwritten official solutions pp.4-13 (grid paper). Q5 is solved in English on p.10 (page of
a different hand, no name on it).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, a-3, b, stored as a b c d. Map: Q1 a=א-1, b=א-2, c=א-3, d=ב.
- Q1 area items carry `region` (area figure) and, with the other numeric parts, `sim`: see EXTRAS near the end.
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
$$=\frac{4e^2-e-1}{4e^2-1}\approx0.905.$$""",
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

# ---- area figures (region.js) and "simulate it" specs (sim.js), keyed by (num, part).
# Regions were moved here from the old verify regions file; every sim exact is the shipped final answer.
from math import pi, log, e as _E
U = {"x": [0, 1], "y": [0, 1]}
XY = {"x": "X", "y": "Y"}


def lin(a, b, c, op):
    return {"a": a, "b": b, "c": c, "op": op}


def REG(event, exact, caption, given=None, space=U):
    r = {"space": space, "labels": XY, "event": event, "exact": exact, "caption": caption}
    if given:
        r["given"] = given
    return r


def AREA(label, exact, **kw):
    return {"kind": "area", "estimate": label, "exact": exact, "params": dict(kw) if kw else {"fromRegion": True}}


def DICE(label, exact, n, event, given=None, weights=None):
    p = {"n": n, "event": event}
    if given:
        p["given"] = given
    if weights:
        p["weights"] = weights
    return {"kind": "dice", "estimate": label, "exact": exact, "params": p}


def PDF(label, exact, pieces, event, given=None):
    p = {"pieces": [{"from": a, "to": b, "expr": x} for a, b, x in pieces], "event": event}
    if given:
        p["given"] = given
    return {"kind": "pdf", "estimate": label, "exact": exact, "params": p}


EXTRAS = {
    (1, "א"): {"region": REG([{"expr": "x*y", "op": "<", "c": "1/2"}], 0.5 + log(2) / 2, "האירוע S=XY<1/2"),
               "sim": AREA("P(S<1/2)", 0.5 + log(2) / 2)},
    (1, "ב"): {"region": REG([{"expr": "x^2+y^2", "op": "<", "c": "1/4"}], pi / 16, "האירוע L<1/2: רבע עיגול ברדיוס 1/2"),
               "sim": AREA("P(L<1/2)", pi / 16)},
    (1, "ג"): {"region": REG([{"expr": "x*y", "op": "<", "c": "1/5"}], 2 * log(2) / 5, "האירוע S<1/5 בהינתן X>1/2",
                             given=[lin(1, 0, "1/2", ">")]),
               "sim": AREA("P(S<1/5 | X>1/2)", 2 * log(2) / 5)},
    (1, "ד"): {"sim": AREA("Var[S]", 7 / 144, space=U, measure="var", expr="x*y")},
    (2, "א"): {"sim": DICE("P(X1=X2)", 1 / 6, 2, "d1 == d2")},
    (2, "ג"): {"sim": DICE("P(X1X2 odd | X1!=X2)", 1 / 5, 2, "d1*d2 % 2 == 1", "d1 != d2")},
    (2, "ד"): {"sim": DICE("P(X1-X2 even | X1!=X2)", 2 / 5, 2, "abs(d1-d2) % 2 == 0", "d1 != d2")},
    (4, "ג"): {"sim": PDF("P(X>-2 | X<3)", (4 * _E ** 2 - _E - 1) / (4 * _E ** 2 - 1),
                          [(-30, -1, "e/4*exp(x)"), (-1, 1, "1/4"), (1, 30, "e/4*exp(-x)")], "x > -2", "x < 3")},
}
for _q in questions:
    _x = EXTRAS.get((_q["num"], _q.get("part")))
    if _x:
        _q.update(_x)


# ------------------------------------------------------------------ steps / rubric / pitfalls (ai-draft) + extra sims
# Every step value is re-derived independently (exact fractions / sympy / brute force, and Monte Carlo) in
# tools/verify/24S-B/steps_check.py, which reads the generated raw JSON back and compares.
import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import probsteps as PS
from fractions import Fraction as Fr
from math import e as _EE, pi as _PI, log as _LN

num, choice, item = PS.num, PS.choice, PS.item
DATA = {}

_OM1 = num(r"שטח מרחב המדגם $|\Omega|$, ריבוע היחידה $(0,1)\times(0,1)$.", 1, r"$|\Omega|=1$.")

# ---- Q1: rectangle with sides X, Y ~ U(0,1)
DATA[(1, "א")] = item(
    [(r"$S=XY$ ו-$|\Omega|=1$ (שיטת השטח על ריבוע היחידה)", 1),
     (r"$S<\frac12\iff y<\frac1{2x}$; עבור $x<\frac12$ כל $y\in(0,1)$ מתאים", 2),
     (r"האינטגרל $\int_{1/2}^1\frac{dx}{2x}=\frac{\ln2}2$", 2),
     (r"סכום: $\frac12+\frac12\ln2$", 2)],
    [r"לבצע אינטגרל של $\frac1{2x}$ מ-$0$ (מתבדר): עבור $x<\frac12$ ההיפרבולה מעל $y=1$.",
     r"לשכוח את חצי השטח $\frac12$ של התחום $0<x<\frac12$."],
    [_OM1,
     num(r"באיזה $x$ ההיפרבולה $y=\frac1{2x}$ חותכת את $y=1$?", Fr(1, 2), r"$\frac1{2x}=1\Rightarrow x=\frac12$. משמאל כל $y\in(0,1)$ מתאים."),
     num(r"האינטגרל $\int_{1/2}^1\frac{dx}{2x}$ (עד שלוש ספרות).", _LN(2) / 2, r"$\frac12\ln x\Big|_{1/2}^1=\frac{\ln2}2\approx0.3466$.", tol=0.001),
     num(r"מהי $P(S<\frac12)$? (עד שלוש ספרות)", (1 + _LN(2)) / 2, r"$\frac12+\frac{\ln2}2\approx0.8466$.", tol=0.001)])

DATA[(1, "ב")] = item(
    [(r"$L=\sqrt{X^2+Y^2}$, ולכן $L<\frac12\iff x^2+y^2<\frac14$", 2),
     (r"האזור הוא רבע עיגול ברדיוס $\frac12$, כולו בתוך הריבוע", 3),
     (r"שטח $\frac14\pi\left(\frac12\right)^2=\frac\pi{16}$ ו-$|\Omega|=1$", 2)],
    [r"לשכוח שהתנאי הוא $x^2+y^2<\frac14$ ולא $<\frac12$ (ריבוע הרדיוס).", r"להשתמש בשטח עיגול שלם."],
    [_OM1,
     choice(r"מהו האזור $\{x^2+y^2<\frac14\}$ בתוך ריבוע היחידה?",
            [r"רבע עיגול ברדיוס $\frac12$", r"רבע עיגול ברדיוס $\frac14$", r"עיגול שלם ברדיוס $\frac12$", r"רבע עיגול ברדיוס $1$"], 0,
            r"$x^2+y^2<\left(\frac12\right)^2$ הוא עיגול ברדיוס $\frac12$, ורק הרבע החיובי בתוך הריבוע."),
     num(r"מהי $P(L<\frac12)$? (עד חמש ספרות)", _PI / 16, r"$\frac\pi{16}\approx0.19635$.", tol=0.0002)])

DATA[(1, "ג")] = item(
    [(r"הגדרת המותנה: $\frac{P(S<\frac15\cap X>\frac12)}{P(X>\frac12)}$ ו-$P(X>\frac12)=\frac12$", 2),
     (r"עבור $x>\frac12$: $\frac1{5x}<\frac25<1$, ולכן ההיפרבולה מתחת ל-$y=1$", 1),
     (r"שטח $\int_{1/2}^1\frac{dx}{5x}=\frac{\ln2}5$", 1),
     (r"היחס: $\frac25\ln2$", 1)],
    [r"לחלק ב-$|\Omega|=1$ במקום ב-$P(X>\frac12)=\frac12$.", r"להוסיף שטח למחצית $x<\frac12$: הנתון $X>\frac12$ פוסל אותה."],
    [_OM1,
     num(r"הסתברות אירוע התנאי $P(X>\frac12)$.", Fr(1, 2), r"$X\sim U_c(0,1)$."),
     num(r"שטח האזור $\{xy<\frac15\}\cap\{x>\frac12\}$ (עד חמש ספרות).", _LN(2) / 5, r"$\int_{1/2}^1\frac{dx}{5x}=\frac{\ln2}5\approx0.13863$.", tol=0.0002),
     num(r"מהי ההסתברות המותנית? (עד חמש ספרות)", 2 * _LN(2) / 5, r"$\frac{\ln2/5}{1/2}=\frac25\ln2\approx0.27726$.", tol=0.0002)])

DATA[(1, "ד")] = item(
    [(r"$\mathbb{E}[S]=\mathbb{E}[X]\mathbb{E}[Y]=\frac14$ מאי-תלות", 2),
     (r"$\mathbb{E}[X^2]=\frac13$", 1),
     (r"$\operatorname{Var}[S]=\mathbb{E}[X^2]\mathbb{E}[Y^2]-\left(\mathbb{E}[S]\right)^2$", 2),
     (r"התשובה $\frac19-\frac1{16}=\frac7{144}$", 1)],
    [r"לכתוב $\operatorname{Var}[XY]=\operatorname{Var}[X]\operatorname{Var}[Y]=\frac1{144}$: נוסחה שגויה.",
     r"לשכוח את הריבוע של התוחלת בנוסחת השונות."],
    [choice(r"איזה כלל מאפשר לחשב את $\mathbb{E}[XY]$ ואת $\mathbb{E}[X^2Y^2]$ ישירות?",
            [r"אי-תלות: תוחלת מכפלה היא מכפלת תוחלות", r"ליניאריות: $\mathbb{E}[XY]=\mathbb{E}[X]+\mathbb{E}[Y]$", r"שיטת השטח", r"נוסחת ההסתברות השלמה"], 0,
            r"אי-תלות מפרקת תוחלת של מכפלה. ליניאריות נותנת סכום ($1$ במקום $\frac14$), ושיטת השטח מחשבת הסתברות לא תוחלת."),
     num(r"$\mathbb{E}[S]$.", Fr(1, 4), r"$\frac12\cdot\frac12=\frac14$."),
     num(r"$\mathbb{E}[X^2]=\int_0^1x^2\,dx$.", Fr(1, 3), r"$\frac13$."),
     num(r"$\operatorname{Var}[S]$ (עד חמש ספרות).", Fr(7, 144), r"$\frac19-\frac1{16}=\frac7{144}\approx0.04861$.", tol=0.00005)])

# ---- Q2: quadratic with dice coefficients
DATA[(2, "א")] = item(
    [(r"נוסחת השורשים: $y_{1,2}=\frac{X_1+X_2\pm|X_1-X_2|}2$", 2),
     (r"שורשים זהים אם ורק אם $X_1=X_2$", 1),
     (r"$P=\frac66\cdot\frac16=\frac16$", 2)],
    [r"לחשב את ההסתברות ל-$X_1=X_2=k$ עבור $k$ מסוים בלבד ולא לסכם על כל $k$."],
    [choice(r"מתי למשוואה $y^2-(X_1+X_2)y+X_1X_2=0$ שורשים זהים?",
            [r"כאשר $X_1=X_2$ (הדיסקרימיננטה היא $(X_1-X_2)^2=0$)", r"כאשר $X_1+X_2=0$", r"כאשר $X_1X_2=0$", r"כאשר $X_1=2X_2$"], 0,
            r"הדיסקרימיננטה $(X_1+X_2)^2-4X_1X_2=(X_1-X_2)^2$ מתאפסת בדיוק כש-$X_1=X_2$. הערכים בקוביה חיוביים, ולכן שני התנאים האחרים אינם אפשריים או אינם נכונים."),
     num(r"כמה זוגות סדורים $(X_1,X_2)$ מקיימים $X_1=X_2$?", 6, r"$(1,1),\ldots,(6,6)$."),
     num(r"מהי ההסתברות לשני שורשים זהים? (עד חמש ספרות)", Fr(1, 6), r"$\frac6{36}=\frac16\approx0.16667$.", tol=0.0002)])

DATA[(2, "ב")] = item(
    [(r"הדיסקרימיננטה $(X_1-X_2)^2$ ולכן השורשים $X_1$ ו-$X_2$", 3),
     (r"$X_1,X_2$ שלמים", 1),
     (r"ההסתברות $1$", 2)],
    [r"לבדוק את הדיסקרימיננטה כריבוע שלם ולהסיק שיש תנאי: היא תמיד ריבוע שלם."],
    [choice(r"מהם שורשי $y^2-(X_1+X_2)y+X_1X_2=0$?",
            [r"$X_1$ ו-$X_2$ (לפי סכום ומכפלה)", r"$X_1+X_2$ ו-$X_1X_2$", r"$\frac{X_1+X_2}2$ בלבד", r"$\pm\sqrt{X_1X_2}$"], 0,
            r"סכום השורשים $X_1+X_2$ ומכפלתם $X_1X_2$ מתקיימים בדיוק עבור $X_1$ ו-$X_2$. שאר האפשרויות אינן מקיימות את שתי המשוואות."),
     num(r"עבור $(X_1,X_2)=(2,5)$: הדיסקרימיננטה $(X_1+X_2)^2-4X_1X_2$.", 9, r"$49-40=9=(2-5)^2$."),
     num(r"מהי ההסתברות ששורשי המשוואה שלמים?", 1, r"השורשים הם $X_1$ ו-$X_2$, תמיד שלמים.")])

DATA[(2, "ג")] = item(
    [(r"הגדרת המותנה, אירוע התנאי $P(X_1\ne X_2)=\frac56$", 2),
     (r"המכפלה אי-זוגית אם ורק אם שניהם אי-זוגיים", 1),
     (r"ספירה: $3\cdot2=6$ זוגות סדורים שונים", 2),
     (r"$\frac{6/36}{5/6}=\frac15$", 2)],
    [r"לכלול את הזוגות השווים $(1,1),(3,3),(5,5)$ בסופרים (התנאי הוא שורשים שונים).",
     r"לחלק ב-$\frac16$ או ב-$1$ במקום ב-$\frac56$."],
    [choice(r"מתי המכפלה $X_1X_2$ אי-זוגית?",
            [r"כששני המספרים אי-זוגיים", r"כשאחד מהם אי-זוגי", r"כשהסכום אי-זוגי", r"כשהם שונים"], 0,
            r"מכפלה אי-זוגית רק אם אין גורם $2$, כלומר שני המספרים אי-זוגיים."),
     num(r"הסתברות אירוע התנאי $P(X_1\ne X_2)$ (עד חמש ספרות).", Fr(5, 6), r"$1-\frac16=\frac56\approx0.83333$.", tol=0.0002),
     num(r"כמה זוגות סדורים שונים, שניהם אי-זוגיים?", 6, r"$3$ ערכים לראשון ו-$2$ לשני שונה ממנו."),
     num(r"מהי ההסתברות המותנית? (עד חמש ספרות)", Fr(1, 5), r"$\frac{6/36}{5/6}=\frac15=0.2$.", tol=0.0002)])

DATA[(2, "ד")] = item(
    [(r"ההפרש זוגי אם ורק אם לשני המספרים אותה זוגיות", 1),
     (r"אירוע התנאי $\frac56$", 1),
     (r"ספירה: $3\cdot2+3\cdot2=12$ זוגות שונים באותה זוגיות", 3),
     (r"$\frac{12/36}{5/6}=\frac25$", 2)],
    [r"לספור $18$ זוגות (כולל השווים) ולקבל $\frac{18/36}{5/6}=\frac35$.", r"לחשוב שהפרש זוגי רק כששני המספרים זוגיים."],
    [choice(r"מתי ההפרש $X_1-X_2$ זוגי?",
            [r"כשלשני המספרים אותה זוגיות", r"כששניהם זוגיים בלבד", r"כשהסכום אי-זוגי", r"כשהם שונים"], 0,
            r"הפרש זוגי אם ורק אם הזוגיות זהה (שניהם זוגיים או שניהם אי-זוגיים)."),
     num(r"הסתברות אירוע התנאי $P(X_1\ne X_2)$ (עד חמש ספרות).", Fr(5, 6), r"$\frac56$.", tol=0.0002),
     num(r"כמה זוגות סדורים שונים באותה זוגיות?", 12, r"$3\cdot2$ אי-זוגיים ועוד $3\cdot2$ זוגיים."),
     num(r"מהי ההסתברות המותנית? (עד חמש ספרות)", Fr(2, 5), r"$\frac{12/36}{5/6}=\frac25=0.4$.", tol=0.0002)])

# ---- Q3: p = 0.3, X = X1+X2, Y = X1+X2+X3
DATA[(3, "א")] = item(
    [(r"הגדרת $X_1,X_2,X_3\sim\mathrm{Ber}(p)$ בלתי תלויים, $X=X_1+X_2$, $Y=X+X_3$", 2),
     (r"טבלת שמונה התוצאות והערכים של $(X,Y)$", 3),
     (r"מילוי $P_{XY}$ (למשל $P_{XY}(1,2)=2p^2(1-p)$)", 4),
     (r"שוליים ובדיקת נרמול", 2)],
    [r"להכפיל $P_X(x)P_Y(y)$: $Y$ כולל את $X$ ולכן תלויים.", r"לטעות במקרה $(1,1)$: $X=1$ ו-$X_3=0$ נותן $2p(1-p)^2$."],
    [choice(r"$Y=X+X_3$ עם $X_3$ בלתי תלוי ב-$X$. איך בונים את $P_{XY}$?",
            [r"$P_{XY}(x,y)=P_X(x)\cdot P(X_3=y-x)$, או ספירת שמונה התוצאות", r"$P_X(x)P_Y(y)$", r"בינומית $\mathrm{Bin}(3,p)$", r"שיטת השטח"], 0,
            r"$X$ ו-$Y$ תלויים. כיוון ש-$X_3$ בלתי תלוי ב-$X$ אפשר לכפול $P_X(x)$ ב-$P(X_3=y-x)$."),
     num(r"ב-$p=0.3$: $P_{XY}(1,2)$.", 2 * Fr(3, 10) * Fr(7, 10) * Fr(3, 10), r"$X=1$ בהסתברות $2p(1-p)$ ו-$X_3=1$: $2\cdot0.3\cdot0.7\cdot0.3=0.126$."),
     num(r"ב-$p=0.3$: $P_{XY}(0,1)$.", Fr(7, 10) ** 2 * Fr(3, 10), r"$X=0$ ו-$X_3=1$: $(1-p)^2p=0.147$."),
     num(r"ב-$p=0.3$: $P_{XY}(2,2)$.", Fr(3, 10) ** 2 * Fr(7, 10), r"$X=2$ ו-$X_3=0$: $p^2(1-p)=0.063$.")])

DATA[(3, "ב")] = item(
    [(r"$X=X_1+X_2\sim\mathrm{Bin}(2,p)$", 2), (r"$Y=X_1+X_2+X_3\sim\mathrm{Bin}(3,p)$", 2), (r"פונקציות ההסתברות", 2)],
    [r"להתבלבל בין $n=2$ ל-$n=3$ בשני המשתנים."],
    [choice(r"מה ההתפלגות של $Y$ (מספר ה״עץ״ בשלוש ההטלות)?",
            [r"$\mathrm{Bin}(3,p)$", r"$\mathrm{Bin}(2,p)$", r"$\mathrm{Geo}(p)$", r"$\mathrm{P}(3p)$"], 0,
            r"שלוש הטלות בלתי תלויות עם אותה הסתברות: $\mathrm{Bin}(3,p)$."),
     num(r"ב-$p=0.3$: $P_X(2)$.", Fr(9, 100), r"$p^2=0.09$."),
     num(r"ב-$p=0.3$: $P_Y(1)$.", 3 * Fr(3, 10) * Fr(7, 10) ** 2, r"$3\cdot0.3\cdot0.49=0.441$.")])

DATA[(3, "ג")] = item(
    [(r"$\mathbb{E}[X]=2p$, $\mathbb{E}[Y]=3p$", 2), (r"$\operatorname{Var}[X]=2p(1-p)$, $\operatorname{Var}[Y]=3p(1-p)$", 2)],
    [r"להחליף בין הפרמטרים $n=2$ ו-$n=3$."],
    [choice(r"מהן התוחלת והשונות של $\mathrm{Bin}(n,p)$?",
            [r"$np$ ו-$np(1-p)$", r"$np$ ו-$np^2$", r"$p$ ו-$np(1-p)$", r"$n(1-p)$ ו-$np$"], 0, r"נוסחאות הבינומית."),
     num(r"ב-$p=0.3$: $\mathbb{E}[Y]$.", Fr(9, 10), r"$3\cdot0.3=0.9$."),
     num(r"ב-$p=0.3$: $\operatorname{Var}[Y]$.", Fr(63, 100), r"$3\cdot0.3\cdot0.7=0.63$.")])

DATA[(3, "ד")] = item(
    [(r"בלתי תלויים פירושו $P_{XY}=P_XP_Y$ לכל זוג", 1),
     (r"הנקודה $(2,0)$: $P_{XY}(2,0)=0$", 1),
     (r"$P_X(2)P_Y(0)=p^2(1-p)^3>0$", 1),
     (r"מסקנה: תלויים", 1)],
    [r"להסיק אי-תלות מכך ש-$Y$ מוגדר מתוך הטלות נוספות: $Y$ כולל את $X$."],
    [num(r"$P_{XY}(2,0)$.", 0, r"אם שתי ההטלות הראשונות ״עץ״ אי אפשר ש-$Y=0$."),
     num(r"ב-$p=0.3$: $P_X(2)P_Y(0)$ (עד חמש ספרות).", Fr(9, 100) * Fr(343, 1000), r"$0.09\cdot0.343=0.03087$.", tol=0.0001),
     choice(r"מה המסקנה?", [r"תלויים: $0\ne0.03087$", r"בלתי תלויים: $0<0.03087$", r"בלתי תלויים: יש להם אותה תוחלת", r"לא ניתן לקבוע"], 0,
            r"זוג אחד שבו המכפלה שונה מההסתברות המשותפת מספיק להוכחת תלות.")])

# ---- Q4: f = a e^x (x<-1), 1/4 on [-1,1), b e^-x (x>=1)
_a = _EE / 4
DATA[(4, "א")] = item(
    [(r"נרמול: $\frac ae+\frac12+\frac be=1$, כלומר $a+b=\frac e2$", 3),
     (r"תוחלת: הקטע האמצעי סימטרי ותורם $0$", 2),
     (r"שני הזנבות: $-\frac{2a}e+\frac{2b}e=0$ ולכן $a=b$", 3),
     (r"$a=b=\frac e4$", 2)],
    [r"לשכוח שהצפיפות על הקטע האמצעי תורמת מסה $\frac12$ לנרמול.", r"לטעות בחישוב $\int_{-\infty}^{-1}xe^x\,dx=-\frac2e$."],
    [choice(r"איזו משוואה מתקבלת מ-$\mathbb{E}[X]=0$?",
            [r"$-\frac{2a}e+\frac{2b}e=0$, כלומר $a=b$", r"$a+b=0$", r"$a=2b$", r"$\frac ae+\frac be=0$"], 0,
            r"הקטע האמצעי סימטרי ולכן תורם $0$. הזנב השמאלי נותן $-\frac{2a}e$ והימני $+\frac{2b}e$."),
     num(r"המסה על הקטע האמצעי $\int_{-1}^1\frac14\,dx$.", Fr(1, 2), r"$\frac14\cdot2=\frac12$."),
     num(r"$a+b$ (מהנרמול; עד שש ספרות).", _EE / 2, r"$\frac{a+b}{e}=\frac12\Rightarrow a+b=\frac e2\approx1.359141$.", tol=0.00001),
     num(r"מהו $a$ (שווה ל-$b$)? (עד שש ספרות)", _a, r"$a=b=\frac e4\approx0.679570$.", tol=0.00001)])

DATA[(4, "ב")] = item(
    [(r"פיצול לתחומים $t<-1$, $-1\le t<1$, $t\ge1$", 2),
     (r"$t<-1$: $\frac e4e^t$", 2),
     (r"$-1\le t<1$: $\frac12+\frac t4$ (עם המסה שנצברה $\frac14$ בנקודה $-1$)", 3),
     (r"$t\ge1$: $1-\frac e4e^{-t}$, ושרטוט", 3)],
    [r"לשכוח את המסה $\frac14$ שנצברה בזנב השמאלי בתחום האמצעי.", r"לשרטט את הזנב הימני עולה מ-$\frac12$ בלי להעביר את המסה $\frac14$ שבקטע האמצעי."],
    [num(r"$F_X(-1)$ (עד חמש ספרות).", Fr(1, 4), r"$\frac e4e^{-1}=\frac14$."),
     num(r"$F_X(0)$ (סימטריה).", Fr(1, 2), r"$\frac14+\frac14\cdot1=\frac12$."),
     num(r"$F_X(2)$ (עד שלוש ספרות).", 1 - _EE ** -1 / 4, r"$1-\frac e4e^{-2}=1-\frac1{4e}\approx0.908$.", tol=0.001),
     choice(r"מהי צורת $F_X(t)$ בקטע $-1\le t<1$?",
            [r"קו ישר (הצפיפות קבועה)", r"פרבולה", r"אקספוננט", r"קבוע"], 0, r"הצפיפות קבועה $\frac14$ על הקטע, ולכן $F_X$ ליניארית.")])

DATA[(4, "ג")] = item(
    [(r"הצגה כיחס $\frac{F_X(3)-F_X(-2)}{F_X(3)}$", 1),
     (r"$F_X(3)=1-\frac1{4e^2}$ ו-$F_X(-2)=\frac1{4e}$", 2),
     (r"הצבה: $\frac{4e^2-e-1}{4e^2-1}$", 2)],
    [r"לחלק ב-$1$ במקום ב-$F_X(3)$."],
    [num(r"הסתברות אירוע התנאי $P(X<3)=F_X(3)$ (עד חמש ספרות).", 1 - _EE ** -2 / 4, r"$1-\frac1{4e^2}\approx0.96617$.", tol=0.0001),
     num(r"$P(-2<X<3)=F_X(3)-F_X(-2)$ (עד חמש ספרות).", 1 - _EE ** -2 / 4 - _EE ** -1 / 4, r"$0.96617-0.09197=0.87420$.", tol=0.0001),
     num(r"מהי ההסתברות המותנית? (עד חמש ספרות)", (1 - _EE ** -2 / 4 - _EE ** -1 / 4) / (1 - _EE ** -2 / 4), r"$\frac{0.87420}{0.96617}=\frac{4e^2-e-1}{4e^2-1}\approx0.90481$.", tol=0.0001)])

# ---- Q5: urn with coin-dependent additions; sample D=3, N=10, M=4, p=0.5
_D, _Nn, _M, _pp = 3, 10, 4, Fr(1, 2)
_Pred = (_D + 2 * _pp * _M) / (_Nn + 2 * _M)
_PX1 = Fr(4, 16)
_Pr1 = Fr(_D + 2, _Nn + 2 * _M)
DATA[(5, "א")] = item(
    [(r"$X\sim\mathrm{Bin}(M,p)$ מספר ה״עץ״", 3),
     (r"בהינתן $X=k$: $P(\text{red}/X=k)=\frac{D+2k}{N+2M}$", 4),
     (r"נוסחת ההסתברות השלמה על $k$", 4),
     (r"ליניאריות התוחלת: $\mathbb{E}[X]=pM$", 2),
     (r"התשובה $\frac{D+2pM}{N+2M}$", 2)],
    [r"לחשב עם הרכב הכד המקורי בלבד ($\frac DN$) ולשכוח את הכדורים שנוספו.",
     r"להציב $2k$ שחורים מחוץ למכנה: המכנה הוא $N+2M$ בכל מקרה."],
    [choice(r"הרכב הכד תלוי במספר ה״עץ״ $X$. איזו גישה מתאימה לסיכוי לכדור אדום?",
            [r"הסתברות שלמה על $X=k$ ($\mathrm{Bin}(M,p)$)", r"היפרגאומטרית על הכד המקורי", r"בייס", r"גאומטרית"], 0,
            r"ההרכב אקראי ותלוי ב-$X$, ולכן מתנים עליו. בייס הוא להיפוך התנאי, והיפרגאומטרית מתעלמת מהכדורים שנוספו."),
     num(r"ב-$D=3$, $N=10$, $M=4$: $P(\text{red}/X=3)$.", Fr(9, 18), r"$\frac{D+2k}{N+2M}=\frac9{18}=0.5$."),
     num(r"ב-$p=0.5$: $\mathbb{E}[X]=pM$.", 2, r"$0.5\cdot4=2$."),
     num(r"מהי $P(\text{red})$? (עד שש ספרות)", _Pred, r"$\frac{3+4}{18}=\frac7{18}\approx0.388889$.", tol=0.00001)])

DATA[(5, "ב")] = item(
    [(r"כדורים אדומים נוספים בזוגות: $n$ אי-זוגי נותן $0$", 3),
     (r"בייס: $P(X=\frac n2/\text{red})=\frac{P(\text{red}/X=\frac n2)P(X=\frac n2)}{P(\text{red})}$", 3),
     (r"הצבה: $\frac{D+n}{2M+N}\binom M{n/2}p^{n/2}(1-p)^{M-n/2}$", 2),
     (r"פישוט: $\frac{D+n}{D+2pM}\binom{M}{n/2}p^{n/2}(1-p)^{M-n/2}$", 2)],
    [r"להתעלם מהזוגיות של $n$ ולתת הסתברות חיובית גם ל-$n$ אי-זוגי.",
     r"להציב $P(\text{red}/X=n)$ במקום $P(\text{red}/X=\frac n2)$: $n$ כדורים אדומים נוספו כש-$\frac n2$ פעמים יצא ״עץ״."],
    [choice(r"האם התשובה תלויה בזוגיות של $n$?",
            [r"כן: $n$ אי-זוגי אי אפשרי כי נוספים שני כדורים בכל ״עץ״", r"לא: אותה נוסחה לכל $n$", r"כן, אבל רק כש-$M$ זוגי", r"לא: התוצאה תמיד $0$"], 0,
            r"כל ״עץ״ מוסיף שני אדומים, ולכן מספר האדומים שנוספו הוא תמיד זוגי."),
     num(r"ב-$M=4$, $p=0.5$: $P(X=1)$ (מקרה $n=2$).", _PX1, r"$\binom41\left(\frac12\right)^4=\frac14$."),
     num(r"ב-$D=3$, $N=10$: $P(\text{red}/X=1)$ (עד חמש ספרות).", _Pr1, r"$\frac{D+2}{N+2M}=\frac5{18}\approx0.27778$.", tol=0.0001),
     num(r"מהי ההסתברות שנוספו בדיוק $2$ כדורים אדומים, בהינתן שהכדור שהוצא אדום? (עד חמש ספרות)", _PX1 * _Pr1 / _Pred, r"$\frac{\frac14\cdot\frac5{18}}{\frac7{18}}=\frac5{28}\approx0.17857$.", tol=0.0001)])

# ---- Q6: nine-unit circuit, p = 0.6
_c = Fr(3, 5)
_blk = 2 * _c - _c ** 2
_PE = _c * _blk ** 2 + (1 - _c) * (2 * _c ** 2 - _c ** 4)
_QN = 2 * _c ** 2 - _c ** 4
_P0 = _QN + (1 - _QN) * _PE
_PEA = _c * (_c + _c ** 2 - _c ** 3)
_PQA = _QN + (1 - _QN) * _PEA
_P1 = (1 - _c) * _PQA / _P0
DATA[(6, "א")] = item(
    [(r"המעגל הוא הטבעת החיצונית במקביל לגשר הפנימי $E$ (כיחידה אחת)", 3),
     (r"נוסחת ההסתברות השלמה על $E$: $P(Q/E)=1$", 4),
     (r"$P(Q/\overline E)=2p^2-p^4$ (שני ענפי הטבעת החיצונית)", 4),
     (r"$P(Q)=p^2(2-p^2)+(1-p^2)^2P(E)$", 3),
     (r"חישוב $P(E)$ בהתניה על היחידה המרכזית: $p^3(2-p)^2+p^2(2-p^2)(1-p)$", 6)],
    [r"לשכוח שהגשר הפנימי $E$ אינו טורי-מקבילי ולנסות לצמצם אותו ישירות.",
     r"לטעות ב-$P(Q/\overline E)$: הטבעת החיצונית היא שני ענפים בני שתי יחידות, $2p^2-p^4$."],
    [choice(r"המעגל מכיל גשר פנימי. איזו גישה מתאימה לחישוב $P(Q)$?",
            [r"לראות את הגשר כיחידה $E$ ולהתנות עליו, ואז להתנות על היחידה המרכזית בתוכו", r"צמצום טורי-מקבילי ישיר של כל המעגל", r"בינומית על מספר היחידות הפועלות", r"בייס"], 0,
            r"הגשר הפנימי אינו ניתן לצמצום, ולכן מתנים על היחידה המרכזית שלו. בינומית מתעלמת מהמבנה."),
     num(r"ב-$p=0.6$: $P(E)$, הגשר הפנימי (עד חמש ספרות).", _PE, r"$p^3(2-p)^2+p^2(2-p^2)(1-p)=0.42336+0.23616=0.65952$.", tol=0.0001),
     num(r"ב-$p=0.6$: $P(Q/\overline E)=2p^2-p^4$ (עד חמש ספרות).", _QN, r"$0.72-0.1296=0.5904$.", tol=0.0001),
     num(r"מהי $P_0=P(Q)$? (עד חמש ספרות)", _P0, r"$P(E)+0.5904\,(1-P(E))=0.65952+0.20102=0.86054$.", tol=0.0001)])

DATA[(6, "ב")] = item(
    [(r"בייס: $P(\overline A/Q)=\frac{P(Q/\overline A)(1-p)}{P_0}$", 2),
     (r"כש-$A$ כבויה: $P(E/\overline A)=p^2(1+p-p^2)$", 2),
     (r"הצבה ב-$P(Q/\overline A)$ והתשובה $P_1$", 1)],
    [r"להציב $P(Q)$ במקום $P(Q/\overline A)$ במונה, או לשכוח את הגורם $1-p$."],
    [choice(r"איזו נוסחה מתאימה ל-$P(\overline A/Q)$?",
            [r"בייס: $\frac{P(Q/\overline A)(1-p)}{P(Q)}$", r"$1-p$", r"$P(Q/\overline A)$", r"$1-P(Q)$"], 0,
            r"מחשבים הסתברות לסיבה בהינתן התוצאה: בייס."),
     num(r"ב-$p=0.6$: $P(E/\overline A)=p^2(1+p-p^2)$ (עד חמש ספרות).", _PEA, r"$0.36\cdot1.24=0.4464$.", tol=0.0001),
     num(r"ב-$p=0.6$: $P(Q/\overline A)$ (עד חמש ספרות).", _PQA, r"$0.5904+0.4096\cdot0.4464\approx0.77325$.", tol=0.0001),
     num(r"מהי $P_1=P(\overline A/Q)$? (עד חמש ספרות)", _P1, r"$\frac{0.77325\cdot0.4}{0.86054}\approx0.35942$.", tol=0.0001)])

# ---- extra sims (symbolic answers, at sample parameters stated in `estimate`)
_BER3 = {"X1": {"values": [0, 1], "probs": [0.7, 0.3]}, "X2": {"values": [0, 1], "probs": [0.7, 0.3]}, "X3": {"values": [0, 1], "probs": [0.7, 0.3]}}
_joint5 = []
for _k in range(_M + 1):
    from math import comb as _comb
    _pk = _comb(_M, _k) * 0.5 ** _M
    _pr = (_D + 2 * _k) / (_Nn + 2 * _M)
    _joint5.append({"p": _pk * _pr, "X": _k, "R": 1})
    _joint5.append({"p": _pk * (1 - _pr), "X": _k, "R": 0})
_G6 = {"event": "S", "source": "T", "sink": "Bt", "edges": [
    {"id": "u1", "from": "T", "to": "m1", "p": 0.6}, {"id": "u2", "from": "m1", "to": "Bt", "p": 0.6},
    {"id": "u3", "from": "T", "to": "m2", "p": 0.6}, {"id": "u4", "from": "m2", "to": "Bt", "p": 0.6},
    {"id": "A", "from": "T", "to": "l", "p": 0.6}, {"id": "G", "from": "T", "to": "r", "p": 0.6},
    {"id": "H", "from": "l", "to": "Bt", "p": 0.6}, {"id": "K", "from": "r", "to": "Bt", "p": 0.6},
    {"id": "Cc", "from": "l", "to": "r", "p": 0.6}]}
EXTRA_SIMS = {
    (3, "א"): {"kind": "custom_discrete", "estimate": "P(X=1, Y=2) ב-p=0.3", "exact": float(2 * Fr(3, 10) ** 2 * Fr(7, 10)),
               "params": {"vars": _BER3, "event": "X1 + X2 == 1 and X1 + X2 + X3 == 2"}},
    (3, "ב"): {"kind": "custom_discrete", "estimate": "P(Y=1) ב-p=0.3", "exact": 0.441,
               "params": {"vars": _BER3, "event": "X1 + X2 + X3 == 1"}},
    (3, "ג"): {"kind": "custom_discrete", "estimate": "Var[Y] ב-p=0.3", "exact": 0.63,
               "params": {"vars": _BER3, "measure": "var", "expr": "X1 + X2 + X3"}},
    (5, "א"): {"kind": "custom_discrete", "estimate": "P(red) ב-D=3, N=10, M=4, p=0.5", "exact": float(_Pred),
               "params": {"joint": _joint5, "event": "R == 1"}},
    (5, "ב"): {"kind": "custom_discrete", "estimate": "P(X=1 | red) ב-D=3, N=10, M=4, p=0.5 (n=2)", "exact": float(_PX1 * _Pr1 / _Pred),
               "params": {"joint": _joint5, "event": "X == 1", "given": "R == 1"}},
    (6, "א"): {"kind": "circuit", "estimate": "P(Q) ב-p=0.6", "exact": float(_P0), "params": _G6},
    (6, "ב"): {"kind": "circuit", "estimate": "P(A לא פועלת | Q) ב-p=0.6", "exact": float(_P1), "params": dict(_G6, event="A == 0", given="S == 1")},
}
for _q in questions:
    _s = EXTRA_SIMS.get((_q["num"], _q.get("part")))
    if _s is not None:
        assert "sim" not in _q, (_q["num"], _q.get("part"))
        _q["sim"] = _s

print("steps:", PS.apply(questions, DATA, CODE), "items")


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
