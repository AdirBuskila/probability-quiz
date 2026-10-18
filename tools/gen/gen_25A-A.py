# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-A.json -- probability (course 20021), semester A 2025, moed A (17.02.2025).
6 questions, 22 items (Q1 3, Q2 4, Q3 4, Q4 4, Q5 3, Q6 4), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-A.py

Source: exam pp.1-3, handwritten official solutions on grid paper pp.4-20. Student/lecturer names are not copied.

Transcription notes
- Part keys: single letters. Q6 prints "ג-1" and "ג-2" -> c and d. The printed label is the first bold token of the text.
- Q1 / Q5 / Q6 are shipped as printed. Q2: the official solution takes Omega = {100,...,999} (900 numbers, i.e. a
  three-digit number with a non-zero first digit; digits may repeat), as printed it just says "a number of 3 digits".
- Q1-type area items carry `region` data (REGIONS below; RAW_SCHEMA `region`).
- Math never holds Hebrew.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-A.json"
CODE = "25A-A"
IMG = "images/exams/25A-A-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"שתי נקודות $A$ ו-$B$ נבחרו באקראי על הקטע שארכו יחידה אחת. מיקום הנקודות מתואר על ידי שני משתנים מקריים בלתי תלויים בעלי התפלגות אחידה: "
          r"$X_1\sim U_c\left(0,\frac13\right)$ ו-$X_2\sim U_c\left(0,\frac23\right)$.")

SOL1_0 = r"""נשתמש בגישה הקלאסית. מרחב המדגם הוא המלבן $\Omega=\left(0,\frac13\right)\times\left(0,\frac23\right)$ ושטחו $|\Omega|=\frac13\cdot\frac23=\frac29$."""

questions.append(Q(
    1, "א", "uniform_geometric",
    r"חשבו את $P(X_1>X_2)$. (8 נק׳)",
    SOL1_0 + r"""
האזור $\{x_2<x_1\}$ בתוך המלבן הוא משולש ישר זווית בעל ניצבים $\frac13$ ו-$\frac13$ (האלכסון $x_2=x_1$ יוצא מהמלבן בפינה $\left(\frac13,\frac13\right)$), ושטחו $\frac12\cdot\frac13\cdot\frac13=\frac1{18}$. לכן
$$P(X_1>X_2)=\frac{|\{x_2<x_1\}|}{|\Omega|}=\frac{\frac12\cdot\frac13\cdot\frac13}{\frac13\cdot\frac23}=\frac14.$$""",
    8, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"מהי ההסתברות שניתן ליצור משולש על ידי קיפול הקטעים הצדדיים? (10 נק׳)",
    SOL1_0 + r"""
הקטעים הם $X_1$, $X_2$ והקטע האמצעי $1-X_1-X_2$. כדי שניתן יהיה ליצור משולש, כל צלע חייבת להיות לכל היותר סכום שתי האחרות:
$$\begin{cases}X_1+X_2\ge1-X_1-X_2\\X_1+(1-X_1-X_2)\ge X_2\\X_2+(1-X_1-X_2)\ge X_1\end{cases}\ \Longrightarrow\ \begin{cases}X_1+X_2\ge\frac12\\X_1\le\frac12\\X_2\le\frac12\end{cases}$$
בתוך המלבן $X_1<\frac13<\frac12$ תמיד, והאזור הוא המשולש שבין הישר $x_2=\frac12-x_1$ לישר $x_2=\frac12$, עבור $0<x_1<\frac13$. הוא משולש ישר זווית בעל ניצבים $\frac13$ ו-$\frac13$ ושטחו $\frac1{18}$. לכן
$$P(X_1+X_2\ge\tfrac12\cap X_1\le\tfrac12\cap X_2\le\tfrac12)=\frac{\frac12\cdot\frac13\cdot\frac13}{\frac23\cdot\frac13}=\frac14.$$""",
    10, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"מהי ההסתברות שניתן ליצור משולש על ידי קיפול הקטעים הצדדיים אם ידוע כי $X_1>X_2$? (7 נק׳)",
    SOL1_0 + r"""
$$P(\text{triangle}\mid X_1>X_2)=\frac{P(X_1+X_2\ge\frac12\cap X_1\le\frac12\cap X_2\le\frac12\cap X_1>X_2)}{P(X_1>X_2)},\qquad P(X_1>X_2)=\frac14.$$
האזור שבו מתקיימים גם $x_1+x_2\ge\frac12$ וגם $x_2<x_1$ הוא משולש קטן. הקווים $x_2=x_1$ ו-$x_2=\frac12-x_1$ נפגשים ב-$x_1=\frac14$, והמשולש משתרע עד $x_1=\frac13$. בסיסו (אורך הקטע האנכי ב-$x_1=\frac13$) הוא $\frac13-\frac16=\frac16$ וגובהו (לאורך ציר $x_1$) הוא $\frac13-\frac14=\frac1{12}$, ולכן שטחו $\frac12\cdot\frac1{12}\cdot\frac16=\frac1{144}$:
$$P(\text{triangle}\cap X_1>X_2)=\frac{\frac12\cdot\frac1{12}\cdot\frac16}{\frac13\cdot\frac23}=\frac1{32}.$$
לכן
$$P(\text{triangle}\mid X_1>X_2)=\frac{1/32}{1/4}=\frac18.$$""",
    7, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_TXT = (r"מרכיבים **מספר** בן $3$ ספרות מהספרות $\{9,8,7,6,5,4,3,2,1,0\}$. נגדיר שלושה מאורעות:" "\n"
          r"$A_2=\{$המספר שמורכב מתחלק ב-$2$ ללא שארית$\}$;" "\n"
          r"$A_4=\{$המספר שמורכב מתחלק ב-$4$ ללא שארית$\}$;" "\n"
          r"$A_8=\{$המספר שמורכב מתחלק ב-$8$ ללא שארית$\}$.")

questions.append(Q(
    2, "א", "basics_events",
    r"מצאו את ההסתברויות $P(A_2)$, $P(A_4)$ ו-$P(A_8)$. (10 נק׳)",
    r"""מרחב המדגם הוא כל המספרים התלת-ספרתיים: $\Omega=\{100,101,\ldots,999\}$ ו-$|\Omega|=900$.
$$A_2=\{100,102,\ldots,998\},\qquad|A_2|=\frac{998-100}{2}+1=450,$$
$$A_4=\{100,104,\ldots,996\},\qquad|A_4|=\frac{996-100}{4}+1=225,$$
$$A_8=\{104,112,\ldots,992\},\qquad|A_8|=\frac{992-104}{8}+1=112.$$
לכן
$$P(A_2)=\frac{450}{900}=\frac12,\qquad P(A_4)=\frac{225}{900}=\frac14,\qquad P(A_8)=\frac{112}{900}=\frac{28}{225}\ne\frac18.$$""",
    10, contextId="c2"))

questions.append(Q(
    2, "ב", "independence",
    r"האם המאורעות $A_2$ ו-$A_4$ הם מאורעות בלתי תלויים? (5 נק׳)",
    r"""$A_4\subseteq A_2$ (כל מספר המתחלק ב-$4$ מתחלק ב-$2$), ולכן $A_2\cap A_4=A_4$ ו-
$$P(A_2\cap A_4)=P(A_4).$$
אילו היו בלתי תלויים, היה מתקיים $P(A_2\cap A_4)=P(A_2)P(A_4)$, כלומר $P(A_4)=P(A_2)P(A_4)$, ולכן $P(A_2)=1$. אך $P(A_2)=\frac12\ne1$.
לכן **לא**: המאורעות תלויים.""",
    5, contextId="c2"))

questions.append(Q(
    2, "ג", "independence",
    r"האם המאורעות $A_4$ ו-$A_8$ הם מאורעות בלתי תלויים? (5 נק׳)",
    r"""$A_8\subseteq A_4$ (כל מספר המתחלק ב-$8$ מתחלק ב-$4$), ולכן $A_4\cap A_8=A_8$ ו-$P(A_4\cap A_8)=P(A_8)$.
אילו היו בלתי תלויים, היה מתקיים $P(A_8)=P(A_4)P(A_8)$ ולכן $P(A_4)=1$. אך $P(A_4)=\frac14\ne1$.
לכן **לא**: המאורעות תלויים.""",
    5, contextId="c2"))

questions.append(Q(
    2, "ד", "basics_events",
    r"האם הטענה $A_8=A_2\cap A_4$ נכונה? **הוכיחו את תשובתכם!** (5 נק׳)",
    r"""**הטענה אינה נכונה.** כפי שראינו, $A_2\cap A_4=A_4$ (כי $A_4\subseteq A_2$), ולכן הטענה שקולה ל-$A_8=A_4$.
אך $A_8\ne A_4$: למשל $100\in A_4$ כי $100=4\cdot25$, אך $100\notin A_8$ כי $100$ אינו מתחלק ב-$8$ (וגם $|A_4|=225\ne112=|A_8|$).
לכן $A_8\ne A_2\cap A_4$.""",
    5, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות" "\n"
          r"$$f_X(x)=\begin{cases}ae^{x},&x<0;\\bx,&0\le x<1;\\\dfrac cx,&x\ge1.\end{cases}$$"
          "\n" r"המקדמים $a$, $b$ ו-$c$ אינם ידועים.")

questions.append(Q(
    3, "א", "continuous_rv",
    r"בהנחה כי $\mathbb{E}[X]=\mu$, מצאו אותם ובטאו אותם באמצעות $\mu$. (10 נק׳)",
    r"""**נרמול:**
$$\int_{-\infty}^{\infty}f_X(x)\,dx=a\int_{-\infty}^0e^x\,dx+b\int_0^1x\,dx+c\int_1^\infty\frac{dx}x=a+\frac b2+c\int_1^\infty\frac{dx}x=1.$$
האינטגרל $\int_1^\infty\frac{dx}x$ מתבדר, ולכן חייב להיות $c=0$. ומכאן
$$a+\frac b2=1.\qquad(*)$$
**תוחלת:**
$$\mathbb{E}[X]=a\int_{-\infty}^0xe^x\,dx+b\int_0^1x^2\,dx=-a+\frac b3=\mu.\qquad(**)$$
פתרון $(*)$ ו-$(**)$:
$$a=\frac{2-3\mu}5,\qquad b=\frac65(\mu+1),\qquad c=0.$$""",
    10, contextId="c3"))

questions.append(Q(
    3, "ב", "continuous_rv",
    r"האם ייתכן כי $\mu=1$? נמקו! (3 נק׳)",
    r"""צפיפות חייבת להיות אי-שלילית, $f_X(x)\ge0$, ולכן $a=\frac{2-3\mu}5\ge0$. עבור $\mu=1$ מקבלים $a=-\frac15<0$, ולכן $\mu=1$ **אינו** אפשרי: $\mu\ne1$.""",
    3, contextId="c3"))

questions.append(Q(
    3, "ג", "continuous_rv",
    r"חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו אותה. (8 נק׳)",
    r"""$F_X(t)=\int_{-\infty}^tf_X(x)\,dx$ עם
$$f_X(x)=\begin{cases}\dfrac{2-3\mu}5e^x,&x<0,\\\dfrac65(\mu+1)x,&0\le x<1,\\0,&x\ge1.\end{cases}$$
- $t<0$: $F_X(t)=\dfrac{2-3\mu}5\int_{-\infty}^te^x\,dx=\dfrac{2-3\mu}5e^t$.
- $0\le t<1$: $F_X(t)=\dfrac{2-3\mu}5\cdot1+\dfrac65(\mu+1)\cdot\dfrac{t^2}2$.
- $t\ge1$: $F_X(t)=\dfrac{2-3\mu}5+\dfrac65(\mu+1)\cdot\dfrac12=1$.

כלומר
$$F_X(t)=\begin{cases}\dfrac{2-3\mu}5e^t,&t<0,\\\dfrac{2-3\mu}5+\dfrac35(\mu+1)t^2,&0\le t<1,\\1,&t\ge1.\end{cases}$$
הגרף: עלייה אקספוננציאלית עד הערך $\frac{2-3\mu}5$ ב-$t=0$, אחר כך פרבולה עולה עד $1$ ב-$t=1$, ואז קבוע $1$.""",
    8, contextId="c3"))

questions.append(Q(
    3, "ד", "continuous_rv",
    r"חשבו את ההסתברות $P(X<1\,/\,X>0)$. (4 נק׳)",
    r"""$$P(X<1\mid X>0)=\frac{P(0<X<1)}{P(X>0)}=\frac{F_X(1)-F_X(0)}{1-F_X(0)}=\frac{1-\frac{2-3\mu}5}{1-\frac{2-3\mu}5}=1.$$""",
    4, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"סטודנט של המכון הטכנולוגי חולון מרכיב מעגל חשמלי $\boldsymbol{Q_1}$ מחמש יחידות $A$, $B$, $C$, $D$ ו-$E$ הפועלות ללא תלות אחת בשנייה בהסתברויות הזהות $p$." "\n"
          r"לאחר מכן, הוא מפרק את המעגל ומרכיב מעגל חדש $\boldsymbol{Q_2}$ – מאותן היחידות.")

questions.append(Q(
    4, "א", "circuits",
    r"מהי ההסתברות שמעגל $Q_1$ פועל? (7 נק׳)",
    r"""נפעל לפי נוסחת ההסתברות השלמה על היחידה האמצעית $E$:
$$P(Q_1)=P(Q_1/E)P(E)+P(Q_1/\overline E)P(\overline E),\qquad P(E)=p.$$
(נדרש חישוב מפורט של שתי ההסתברויות המותנות.)
- $E$ פועלת: $P(Q_1/E)=(2p-p^2)^2$.
- $E$ לא פועלת: $P(Q_1/\overline E)=2p^2-p^4$.

לכן
$$P(Q_1)=p^3(2-p)^2+p^2(1-p)(2-p^2).$$""",
    7, contextId="c4"))

questions.append(Q(
    4, "ב", "circuits",
    r"מהי ההסתברות שמעגל $Q_2$ פועל? (7 נק׳)",
    r"""$Q_2$: היחידה $A$ בטור עם ($B\,\|\,C$) ובטור עם ($D\,\|\,E$). לכן
$$P(Q_2)=p\,(2p-p^2)^2=p^3(2-p)^2.$$""",
    7, contextId="c4"))

questions.append(Q(
    4, "ג", "circuits",
    r"**אם ידוע** כי מעגל $Q_2$ פועל, מהי ההסתברות שגם המעגל $Q_1$ פועל? (7 נק׳)",
    r"""$$P(Q_1/Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}.$$
נסמן $\widetilde Q=Q_1\cap Q_2$ ונפעל לפי נוסחת ההסתברות השלמה על $A\cap E$ וארבעת המקרים: $A\cap E$, $A\cap\overline E$, $\overline A\cap E$, $\overline A\cap\overline E$. כאשר $A$ לא פועלת $Q_2$ אינו פועל, ולכן שני המקרים האחרונים תורמים $0$.
- $A\cap E$: $Q_1$ הופך ל-$B\cup D$ ו-$Q_2$ ל-$B\cup C$ (כש-$E$ פועלת $D\cup E$ מתקיים). המאורע המשותף הוא $(B\cup D)\cap(B\cup C)=B\cup(C\cap D)$, ולכן $P(\widetilde Q/A\cap E)=p+p^2-p^3$.
- $A\cap\overline E$: $Q_1$ הופך ל-$B\cap D$ ו-$Q_2$ ל-$(B\cup C)\cap D$. המשותף: $(B\cup C)\cap D$, ולכן $P(\widetilde Q/A\cap\overline E)=(2p-p^2)p$.

מכאן
$$P(\widetilde Q)=p^2\cdot p(1+p-p^2)+p(1-p)\cdot p^2(2-p)=p^3(3-2p),$$
ולכן
$$P(Q_1/Q_2)=\frac{p^3(3-2p)}{p^3(2-p)^2}=\frac{3-2p}{(2-p)^2}.$$""",
    7, contextId="c4"))

questions.append(Q(
    4, "ד", "circuits",
    r"**אם ידוע** כי מעגל $Q_2$ פועל, מהי ההסתברות שהמעגל $Q_1$ **לא** פועל? (4 נק׳)",
    r"""$$P(\overline{Q_1}/Q_2)=1-P(Q_1/Q_2)=1-\frac{3-2p}{(2-p)^2}=\frac{(1-p)^2}{(2-p)^2}.$$""",
    4, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_TXT = (r"נתבונן בפונקציה $y(t)=\cos(\omega t)$ בעלת תדירות אקראית. יהי $N_T$ משתנה מקרי המתאר את מספר האפסים$^{(*)}$ של פונקציה $y(t)$ בקטע $(0,T)$. $\omega\sim\mathrm{Exp}(\lambda)$." "\n"
          r"$^{(*)}$ הערה: אפסים של פונקציה $y(t)$ הם שורשי המשוואה $y(t)=0$." "\n"
          r"**להזכירכם:** $\displaystyle\sum_{k=1}^{\infty}kq^k=\frac{q}{(1-q)^2}$ עבור $|q|<1$.")

SOL5_0 = r"""$\cos(\omega t)=0\iff\omega t=\frac\pi2+\pi j$, ולכן השורשים החיוביים הם
$$t_k=\frac\pi{2\omega}+\frac\pi\omega(k-1),\qquad k=1,2,\ldots$$"""

questions.append(Q(
    5, "א", "special_discrete",
    r"מצאו את פונקציית ההסתברות של משתנה מקרי $N_T$. (10 נק׳)",
    SOL5_0 + r"""
$N_T$ הוא משתנה מקרי בדיד המקבל את הערכים $j=0,1,2,\ldots$

**$N_T=0$:** אין שורש בקטע $(0,T)$, כלומר השורש הראשון נמצא מימין ל-$T$: $t_1=\frac\pi{2\omega}>T$.
$$P(N_T=0)=P\left(\frac\pi{2\omega}>T\right)=P\left(\omega<\frac\pi{2T}\right)=\lambda\int_0^{\pi/(2T)}e^{-\lambda x}\,dx=1-e^{-\lambda\pi/(2T)}.$$
**$N_T=k$, $k=1,2,\ldots$:** $t_k<T<t_{k+1}$:
$$P(N_T=k)=P\left(\frac\pi{2\omega}+\frac\pi\omega(k-1)<T<\frac\pi{2\omega}+\frac\pi\omega k\right)=P\left(-\frac\pi{2T}+\frac{\pi k}T<\omega<\frac\pi{2T}+\frac{\pi k}T\right).$$
$$=\lambda\int_{-\frac\pi{2T}+\frac{\pi k}T}^{\frac\pi{2T}+\frac{\pi k}T}e^{-\lambda x}\,dx=e^{-\lambda\left(-\frac\pi{2T}+\frac{\pi k}T\right)}-e^{-\lambda\left(\frac\pi{2T}+\frac{\pi k}T\right)}.$$
כלומר
$$P(N_T=k)=\begin{cases}1-e^{-\lambda\pi/(2T)},&k=0,\\e^{-\frac{\lambda\pi}T k}\left\{e^{\frac{\lambda\pi}{2T}}-e^{-\frac{\lambda\pi}{2T}}\right\},&k=1,2,\ldots\end{cases}$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    r"חשבו את התוחלת $\mathbb{E}[N_T]$. (10 נק׳)",
    r"""$$\mathbb{E}[N_T]=\sum_{k=0}^{\infty}k\,P(N_T=k)=\left\{e^{\frac{\lambda\pi}{2T}}-e^{-\frac{\lambda\pi}{2T}}\right\}\sum_{k=1}^{\infty}k\,q^k\Bigg|_{q=e^{-\lambda\pi/T}}.$$
לפי ההערה $\sum_{k=1}^\infty kq^k=\frac q{(1-q)^2}$, ו-$\frac q{(1-q)^2}=\frac1{\left(e^{\lambda\pi/(2T)}-e^{-\lambda\pi/(2T)}\right)^2}$ עבור $q=e^{-\lambda\pi/T}$. לכן
$$\mathbb{E}[N_T]=\frac1{e^{\frac{\lambda\pi}{2T}}-e^{-\frac{\lambda\pi}{2T}}}.$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ג", "conditional_bayes",
    r"יהיו $\{t_1,t_2,\ldots\}$ שורשים חיוביים של המשוואה $y(t)=0$ המסודרים בסדר עולה $0<t_1<t_2<\cdots$. עבור כל $k\ge1$ חשבו את ההסתברות המותנית $P(t_{k+1}>T\,/\,t_k<T)$. (5 נק׳)",
    r"""$$P(t_{k+1}>T\mid t_k<T)=\frac{P(t_k<T<t_{k+1})}{P(t_k<T)}=\frac{P(N_T=k)}{P(t_k<T)}.$$
$$P(t_k<T)=P\left(\omega>-\frac\pi{2T}+\frac{\pi k}T\right)=\lambda\int_{-\frac\pi{2T}+\frac{\pi k}T}^{\infty}e^{-\lambda x}\,dx=e^{\frac{\lambda\pi}{2T}}e^{-\frac{\lambda\pi}Tk}.$$
הצבה:
$$P(t_{k+1}>T\mid t_k<T)=\frac{e^{-\frac{\lambda\pi}Tk}\left\{e^{\frac{\lambda\pi}{2T}}-e^{-\frac{\lambda\pi}{2T}}\right\}}{e^{\frac{\lambda\pi}{2T}}e^{-\frac{\lambda\pi}Tk}}=1-e^{-\lambda\pi/T}.$$""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_TXT = (r"במחסן חלפים ישנן סוללות משני מפעלים $A$ ו-$B$. פרופורציית הסוללות ממפעל $A$ הינה $q$. מכינים משלוח של $n$ סוללות שנלקחות באקראי מהמחסן.")
Q6_HINT = r"""**הערה:** לידיעתך,
$$\sum_{j=m}^{N}C_j^mC_N^ja^j=C_N^ma^m(1+a)^{N-m}$$
(יכול להיות שאין צורך להשתמש בנוסחה זו)."""

questions.append(Q(
    6, "א", "special_discrete",
    r"נגדיר משתנה מקרי $X=\{$מספר הסוללות ממפעל $A$ במשלוח$\}$. מצאו את פונקציית ההסתברות של משתנה זה. **עליך לתת הסבר מפורט.** (6 נק׳)",
    r"""נבצע סדרה של $n$ ניסויי ברנולי בבדיקת תוכן המשלוח. עבור הפריט ה-$j$ ($j=1,\ldots,n$) נגדיר משתנה מקרי
$$X_j=\begin{cases}1,&\text{battery from }A,\ \text{probability }q,\\0,&\text{battery from }B,\ \text{probability }1-q,\end{cases}\qquad X_j\sim\mathrm{Ber}(q).$$
סך כל הסוללות במשלוח שמקורן במפעל $A$ הוא $X=\sum_{j=1}^nX_j$, סכום של $n$ משתנים ברנולי בלתי תלויים (וזהים), ולכן $X\sim\mathrm{Bin}(n,q)$:
$$P(X=k)=\binom nkq^k(1-q)^{n-k},\qquad k=0,1,\ldots,n.$$""",
    6, contextId="c6"))

questions.append(Q(
    6, "ב", "special_discrete",
    r"נתון כי פרופורציית הסוללות הפגומות הינה $p$ ללא קשר למפעל בו נוצרו. כתוצאה מכך, חלק מהסוללות במשלוח פגומות. נגדיר משתנה מקרי $Y=\{$מספר הסוללות הפגומות במשלוח שמקורן במפעל $A\}$. מצאו את פונקציית ההסתברות של משתנה זה. **עליך לתת הסבר מפורט.** (12 נק׳)" "\n" + Q6_HINT,
    r"""גם כאן נבצע סדרה של $n$ ניסויי ברנולי בבדיקת הפריטים: בכל פריט בודקים גם מבחינת השיוך למפעל וגם מבחינת תקינות הסוללה. עבור הפריט ה-$j$ נגדיר ($Y_j=1$ אם הסוללה שייכת ל-$A$ וגם פגומה, בהסתברות $q\cdot p$)
$$Y_j=\begin{cases}1,&\text{from }A\text{ and defective},\ \text{probability }q\cdot p,\\0,&\text{otherwise}.\end{cases}$$
ההסתברות להצלחה בכל ניסוי היא $pq$ (אי-תלות בין המפעל לבין הפגם), ולכן $Y=\sum_{j=1}^nY_j$ סכום של $n$ משתנים $\mathrm{Ber}(pq)$ בלתי תלויים:
$$Y\sim\mathrm{Bin}(n,pq),\qquad P(Y=k)=\binom nk(pq)^k(1-pq)^{n-k},\qquad k=0,1,\ldots,n.$$
**הערה:** אפשר לתאר כל $Y_k$ ככפל של שני משתני ברנולי בלתי תלויים: $Y_k=X_kZ_k$ כאשר $X_k\sim\mathrm{Ber}(q)$ (שייכות למפעל $A$) ו-$Z_k\sim\mathrm{Ber}(p)$ (תקינות הסוללה).""",
    12, contextId="c6"))

questions.append(Q(
    6, "ג", "joint_discrete",
    r"**ג-1:** חשבו את מקדם המתאם $\rho[X,Y]$. (5 נק׳)",
    r"""$$\rho[X,Y]=\frac{\operatorname{Cov}[X,Y]}{\sqrt{\operatorname{Var}X}\sqrt{\operatorname{Var}Y}},\qquad\operatorname{Var}X=nq(1-q),\quad\operatorname{Var}Y=npq(1-pq).$$
$$\operatorname{Cov}[X,Y]=\mathbb{E}[XY]-\mathbb{E}[X]\,\mathbb{E}[Y],\qquad\mathbb{E}[X]=nq,\ \mathbb{E}[Y]=npq.$$
$$\mathbb{E}[XY]=\mathbb{E}\Bigl[\sum_{j=1}^nX_j\cdot\sum_{k=1}^nX_kZ_k\Bigr]=\sum_{j=1}^n\mathbb{E}[X_j^2]\,\mathbb{E}[Z_j]+\sum_{j\ne k}\mathbb{E}[X_j]\,\mathbb{E}[X_k]\,\mathbb{E}[Z_k]=pq\,n+n(n-1)pq^2.$$
(כאן $\mathbb{E}[X_j^2]=q$.) לכן
$$\operatorname{Cov}[X,Y]=pqn+n(n-1)pq^2-n^2pq^2=npq(1-q).$$
הצבה:
$$\rho[X,Y]=\frac{npq(1-q)}{\sqrt{nq(1-q)}\sqrt{npq(1-pq)}}=\sqrt{\frac{p(1-q)}{1-pq}}.$$""",
    5, contextId="c6"))

questions.append(Q(
    6, "ד", "joint_discrete",
    r"**ג-2:** מה מביאה הנוסחה שקיבלתם בסעיף ג-1 עבור $p=1$? הסבירו. (2 נק׳)",
    r"""עבור $p=1$ מתקבל $\rho[X,Y]=\sqrt{\frac{1-q}{1-q}}=1$.
הסבר: כאשר $p=1$ כל הסוללות פגומות, ולכן $Y=X$ (מספר הסוללות הפגומות ממפעל $A$ שווה למספר הסוללות ממפעל $A$), ואז
$$\rho[X,X]=\frac{\operatorname{Var}X}{\sqrt{\operatorname{Var}X}\sqrt{\operatorname{Var}X}}=1.$$""",
    2, contextId="c6"))

# ------------------------------------------------------------------ area regions (RAW_SCHEMA `region`)
REGIONS = {
    (1, 'א'): {"space": {"x": [0, "1/3"], "y": [0, "2/3"]}, "event": [{"a": -1, "b": 1, "c": 0, "op": "<"}], "exact": 0.25, "labels": {"x": "X1", "y": "X2"}, "caption": "X1>X2"},
    (1, 'ב'): {"space": {"x": [0, "1/3"], "y": [0, "2/3"]}, "event": [{"a": 1, "b": 1, "c": 0.5, "op": ">="}, {"a": 1, "b": 0, "c": 0.5, "op": "<="}, {"a": 0, "b": 1, "c": 0.5, "op": "<="}], "exact": 0.25, "labels": {"x": "X1", "y": "X2"}, "caption": "תנאי המשולש"},
    (1, 'ג'): {"space": {"x": [0, "1/3"], "y": [0, "2/3"]}, "event": [{"a": 1, "b": 1, "c": 0.5, "op": ">="}, {"a": 1, "b": 0, "c": 0.5, "op": "<="}, {"a": 0, "b": 1, "c": 0.5, "op": "<="}], "given": [{"a": -1, "b": 1, "c": 0, "op": "<"}], "exact": 0.125, "labels": {"x": "X1", "y": "X2"}, "caption": "תנאי המשולש בהינתן X1>X2"},
}
for _q in questions:
    _r = REGIONS.get((_q["num"], _q.get("part")))
    if _r is not None:
        _q["region"] = _r

# ------------------------------------------------------------------ area regions + simulations (RAW_SCHEMA `region`, `sim`)
SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X1>X2)", "exact": 0.25},
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(triangle)", "exact": 0.25},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(triangle | X1>X2)", "exact": 0.125},
    (2, "א"): {"kind": "custom_discrete",
               "params": {"vars": {"N": {"values": list(range(100, 1000)), "probs": [1 / 900] * 900}}, "event": "N % 8 == 0"},
               "estimate": "P(A8)", "exact": 28 / 225},
}

for _q in questions:
    _k = (_q["num"], _q.get("part"))
    if _k in SIMS:
        _q["sim"] = SIMS[_k]

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ה, מועד א (17.02.2025)",
    "year": 2025,
    "examDate": "17.02.2025",
    "sourceFile": "25A-A exam pp.1-3",
    "solutionFile": "25A-A handwritten official solutions, pp.4-20",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1", "image": IMG + "Q1-segment.png", "caption": Q1_TXT},
        "c2": {"kind": "text", "title": "שאלה 2", "text": Q2_TXT},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_TXT},
        "c4": {"kind": "image", "title": "שאלה 4: מעגלים", "image": IMG + "Q4-circuits.png", "caption": Q4_TXT},
        "c5": {"kind": "image", "title": "שאלה 5", "image": IMG + "Q5-cos.png", "caption": Q5_TXT},
        "c6": {"kind": "text", "title": "שאלה 6", "text": Q6_TXT},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
