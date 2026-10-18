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

# ------------------------------------------------------------------ steps / rubric / pitfalls (ai-draft) + extra sims
# Every step value is re-derived independently (exact fractions / sympy / brute force, and Monte Carlo) in
# tools/verify/25A-A/steps_check.py, which reads the generated raw JSON back and compares.
import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import probsteps as PS
from fractions import Fraction as Fr
from math import e as _E, exp as _exp, pi as _PI

num, choice, item = PS.num, PS.choice, PS.item


def _br(p, ids="ABCDE"):
    """Q1 of this exam: the five-unit bridge (E in the middle)."""
    a, b, c, d, e = ids
    return {"event": "S", "edges": [
        {"id": a, "from": "s", "to": "u", "p": p}, {"id": c, "from": "s", "to": "v", "p": p},
        {"id": b, "from": "u", "to": "t", "p": p}, {"id": d, "from": "v", "to": "t", "p": p},
        {"id": e, "from": "u", "to": "v", "p": p}], "source": "s", "sink": "t"}


_Q2_UP = "A == 1 and (B == 1 or C == 1) and (D == 1 or E == 1)"
_P6 = Fr(3, 5)
_pq = Fr(3, 5)

_pdf_exp = lambda lam: [(0, 30, f"{lam}*exp(-{lam}*x)")]   # omega ~ Exp(lam), truncated at 30 (mass e^-60 lost)

DATA = {}

# ---- Q1: the area method, X1~U(0,1/3), X2~U(0,2/3)
_MODEL1 = choice(
    r"$X_1$ ו-$X_2$ בלתי תלויים ואחידים על קטעים. איזה כלי מתאים לחישוב $P(X_1>X_2)$?",
    [r"שיטת השטח: $(X_1,X_2)$ אחידה על המלבן, וההסתברות היא יחס שטחים",
     r"התפלגות בינומית",
     r"התפלגות היפרגאומטרית",
     r"התפלגות פואסון"], 0,
    r"המשתנים רציפים ואחידים, ולכן הזוג אחיד על מלבן והסתברות = שטח האירוע חלקי שטח המלבן. הבינומית והפואסונית סופרות הצלחות בניסויים חוזרים, וההיפרגאומטרית דורשת דגימה בלי החזרה מאוכלוסייה סופית; אין כאן אף אחד מאלה.")
_OMEGA1 = num(r"שטח מרחב המדגם $|\Omega|$, מלבן $\left(0,\frac13\right)\times\left(0,\frac23\right)$ (כמספר עשרוני או שבר).", Fr(2, 9),
              r"$|\Omega|=\frac13\cdot\frac23=\frac29$. הטעות הנפוצה: להניח $|\Omega|=1$.")

DATA[(1, "א")] = item(
    [(r"מרחב המדגם: המלבן $\left(0,\frac13\right)\times\left(0,\frac23\right)$ ו-$|\Omega|=\frac29$", 2),
     (r"זיהוי האזור $x_2<x_1$ כמשולש ישר זווית בעל ניצבים $\frac13$ (האלכסון יוצא מהפינה)", 3),
     (r"שטח האזור $\frac12\cdot\frac13\cdot\frac13=\frac1{18}$", 1),
     (r"יחס השטחים והתשובה $\frac14$", 2)],
    [r"לחשב יחס שטחים בלי לחלק ב-$|\Omega|$, או להניח $|\Omega|=1$.",
     r"לצייר את האלכסון $x_2=x_1$ כחוצה את כל המלבן (המלבן אינו ריבוע, והאלכסון יוצא בפינה $\left(\frac13,\frac13\right)$)."],
    [_MODEL1, _OMEGA1,
     num(r"שטח האזור $\{x_2<x_1\}$ בתוך המלבן.", Fr(1, 18),
         r"משולש ישר זווית עם ניצבים $\frac13$ ו-$\frac13$: $\frac12\cdot\frac13\cdot\frac13=\frac1{18}$."),
     num(r"מהי $P(X_1>X_2)$?", Fr(1, 4), r"$\frac{1/18}{2/9}=\frac14$.")])

DATA[(1, "ב")] = item(
    [(r"כתיבת שלושת התנאים לפי אורכי הקטעים $X_1$, $X_2$, $1-X_1-X_2$", 3),
     (r"זיהוי התנאים שחותכים את המלבן (התנאי $X_1\le\frac12$ תמיד מתקיים)", 2),
     (r"שטח המשולש $\frac1{18}$", 3),
     (r"חלוקה ב-$|\Omega|=\frac29$ והתשובה $\frac14$", 2)],
    [r"לשכוח שהתנאי $X_2\le\frac12$ אכן חותך את המלבן, כי $X_2$ מגיע עד $\frac23$.",
     r"להשתמש ב-$|\Omega|=1$."],
    [_OMEGA1,
     choice(r"אילו מבין שלושת התנאים $X_1\le\frac12$, $X_2\le\frac12$, $X_1+X_2\ge\frac12$ אינם מתקיימים בכל המלבן?",
            [r"$X_2\le\frac12$ ו-$X_1+X_2\ge\frac12$ בלבד ($X_1<\frac13$ ולכן $X_1\le\frac12$ תמיד)",
             r"שלושתם",
             r"$X_1+X_2\ge\frac12$ בלבד",
             r"אף אחד מהם"], 0,
            r"$X_1<\frac13<\frac12$ תמיד. אבל $X_2$ מגיע עד $\frac23>\frac12$, ולכן $X_2\le\frac12$ חותך; וגם $X_1+X_2\ge\frac12$ חותך (הנקודה ליד הראשית אינה מקיימת אותו)."),
     num(r"שטח האזור המקיים את שלושת התנאים.", Fr(1, 18),
         r"משולש בין הישרים $x_2=\frac12-x_1$ ו-$x_2=\frac12$ עבור $0<x_1<\frac13$: ניצבים $\frac13$ ו-$\frac13$, שטח $\frac1{18}$."),
     num(r"מהי ההסתברות שניתן ליצור משולש?", Fr(1, 4), r"$\frac{1/18}{2/9}=\frac14$.")])

DATA[(1, "ג")] = item(
    [(r"הצגת $P(\text{triangle}\mid X_1>X_2)$ כיחס $\frac{P(\text{triangle}\cap X_1>X_2)}{P(X_1>X_2)}$", 2),
     (r"$P(X_1>X_2)=\frac14$ (סעיף א)", 1),
     (r"האזור המשותף הוא משולש קטן; חישוב שטחו $\frac1{144}$", 2),
     (r"הצבה והתשובה $\frac18$", 2)],
    [r"לחלק ב-$P(\text{triangle})$ במקום ב-$P(X_1>X_2)$: הנתון מצמצם את מרחב המדגם לתנאי $X_1>X_2$.",
     r"לחשב את שטח החיתוך לפי משולש גדול מדי (להתעלם מהישר $x_2=\frac12-x_1$)."],
    [_OMEGA1,
     num(r"ההסתברות של אירוע התנאי, $P(X_1>X_2)$ (סעיף א).", Fr(1, 4), r"שטח $\frac1{18}$ חלקי $\frac29$ הוא $\frac14$."),
     num(r"שטח החיתוך: האזור שבו גם $x_1+x_2\ge\frac12$, גם $x_2\le\frac12$ וגם $x_2<x_1$.", Fr(1, 144),
         r"משולש עם קדקודים $\left(\frac14,\frac14\right)$, $\left(\frac13,\frac16\right)$, $\left(\frac13,\frac13\right)$: בסיס אנכי $\frac16$ וגובה $\frac1{12}$, שטח $\frac12\cdot\frac16\cdot\frac1{12}=\frac1{144}$."),
     num(r"מהי ההסתברות המותנית?", Fr(1, 8), r"$P(\text{triangle}\cap X_1>X_2)=\frac{1/144}{2/9}=\frac1{32}$, ואז $\frac{1/32}{1/4}=\frac18$.")])

# ---- Q2: divisibility of a three-digit number
DATA[(2, "א")] = item(
    [(r"$\Omega=\{100,\ldots,999\}$ ו-$|\Omega|=900$", 2),
     (r"$|A_2|=450$ ולכן $P(A_2)=\frac12$", 2),
     (r"$|A_4|=225$ ולכן $P(A_4)=\frac14$", 2),
     (r"$|A_8|=112$: האיבר הראשון $104$ והאחרון $992$", 2),
     (r"$P(A_8)=\frac{112}{900}=\frac{28}{225}\ne\frac18$", 2)],
    [r"לקחת $|\Omega|=1000$ (לספור גם מספרים שמתחילים ב-$0$).",
     r"להסיק $P(A_8)=\frac18$ מכך ש-$8$ מחלק כל שמיני מספר. $900$ אינו מתחלק ב-$8$, ולכן מקבלים $112$ ולא $112.5$."],
    [choice(r"בוחרים מספר תלת-ספרתי באקראי. איזה מודל מתאים לחישוב $P(A_8)$?",
            [r"הסתברות קלאסית: מספר המספרים המתחלקים ב-$8$ חלקי מספר כל המספרים התלת-ספריים",
             r"התפלגות בינומית",
             r"התפלגות גאומטרית",
             r"שיטת השטח"], 0,
            r"כל המספרים התלת-ספריים שווי הסתברות ולכן סופרים. אין כאן ניסויי ברנולי חוזרים או המתנה להצלחה, ואין משתנה רציף לשטח."),
     num(r"$|\Omega|$: כמה מספרים תלת-ספריים יש (מ-$100$ עד $999$)?", 900, r"$999-100+1=900$. המספר $000$-$099$ אינם תלת-ספריים."),
     num(r"$|A_8|$: כמה מהם מתחלקים ב-$8$?", 112, r"הראשון $104=8\cdot13$ והאחרון $992=8\cdot124$: $124-13+1=112$."),
     num(r"מהי $P(A_8)$?", Fr(28, 225), r"$\frac{112}{900}=\frac{28}{225}\approx0.1244$, שונה מ-$\frac18=0.125$.")])

_IND = choice(r"איזה תנאי שקול לכך ש-$A$ ו-$B$ בלתי תלויים?",
              [r"$P(A\cap B)=P(A)P(B)$",
               r"$P(A\cap B)=0$ (זה תנאי של מאורעות זרים)",
               r"$P(A\cup B)=P(A)+P(B)$ (גם זה תנאי של מאורעות זרים)",
               r"$P(A/B)=P(B/A)$ (מתקיים גם כש-$P(A)=P(B)$ והמאורעות תלויים)"], 0,
              r"אי-תלות פירושה שהסתברות החיתוך היא מכפלת ההסתברויות. שני התנאים הבאים הם זרות, והאחרון אינו שקול.")

DATA[(2, "ב")] = item(
    [(r"$A_4\subseteq A_2$ ולכן $A_2\cap A_4=A_4$", 2),
     (r"השוואה: $P(A_2\cap A_4)=\frac14$ לעומת $P(A_2)P(A_4)=\frac18$", 2),
     (r"מסקנה: תלויים", 1)],
    [r"לחשוב שאם אחד מכיל את השני אז הם בלתי תלויים, או שהם זרים. הכלה מחייבת תלות כשההסתברויות בין $0$ ל-$1$."],
    [_IND,
     num(r"$P(A_2\cap A_4)$.", Fr(1, 4), r"$A_4\subseteq A_2$, ולכן החיתוך הוא $A_4$ והסתברותו $\frac14$."),
     num(r"המכפלה $P(A_2)P(A_4)$.", Fr(1, 8), r"$\frac12\cdot\frac14=\frac18$."),
     choice(r"מה המסקנה?", [r"תלויים, כי $\frac14\ne\frac18$", r"בלתי תלויים, כי $A_4\subseteq A_2$", r"בלתי תלויים, כי שניהם קטנים מ-$1$", r"זרים, ולכן בלתי תלויים"], 0,
            r"אי-שוויון בין החיתוך למכפלה פירושו תלות.")])

DATA[(2, "ג")] = item(
    [(r"$A_8\subseteq A_4$ ולכן $A_4\cap A_8=A_8$", 2),
     (r"השוואה: $P(A_4\cap A_8)=\frac{28}{225}$ לעומת $P(A_4)P(A_8)=\frac{7}{225}$", 2),
     (r"מסקנה: תלויים", 1)],
    [r"להניח ש-$A_8$ ו-$A_4$ בלתי תלויים כי $8=2\cdot4$.",
     r"להציב $P(A_8)=\frac18$ במקום $\frac{28}{225}$."],
    [num(r"$P(A_4\cap A_8)$.", Fr(28, 225), r"$A_8\subseteq A_4$, ולכן החיתוך הוא $A_8$ והסתברותו $\frac{28}{225}\approx0.1244$."),
     num(r"המכפלה $P(A_4)P(A_8)$.", Fr(7, 225), r"$\frac14\cdot\frac{28}{225}=\frac7{225}\approx0.0311$."),
     choice(r"מה המסקנה?", [r"תלויים, כי $\frac{28}{225}\ne\frac7{225}$", r"בלתי תלויים, כי $A_8\subseteq A_4$", r"בלתי תלויים, כי $P(A_8)<P(A_4)$", r"זרים"], 0,
            r"החיתוך גדול פי $4$ מהמכפלה, ולכן אין אי-תלות.")])

DATA[(2, "ד")] = item(
    [(r"$A_4\subseteq A_2$ ולכן $A_2\cap A_4=A_4$", 2),
     (r"הטענה שקולה ל-$A_8=A_4$", 1),
     (r"דוגמה נגדית (או $|A_4|\ne|A_8|$) ומסקנה שהטענה שגויה", 2)],
    [r"לחשוב ש-$A_8=A_2\cap A_4$ כי $\mathrm{lcm}(2,4)=4$ (המכנה המשותף הוא $4$ ולא $8$)."],
    [num(r"$|A_2\cap A_4|$ (כמה מספרים תלת-ספריים מתחלקים גם ב-$2$ וגם ב-$4$?).", 225, r"מתחלק ב-$4$ גורר מתחלק ב-$2$, ולכן החיתוך הוא $A_4$ ו-$|A_4|=225$."),
     num(r"$|A_8|$.", 112, r"$|A_8|=112\ne225$, ולכן הקבוצות שונות."),
     choice(r"איזה מספר מראה ש-$A_8\ne A_2\cap A_4$?",
            [r"$100$ (מתחלק ב-$4$ ואינו מתחלק ב-$8$)", r"$104$ (מתחלק ב-$8$, ולכן שייך לשתי הקבוצות)",
             r"$102$ (אינו מתחלק ב-$4$, ולכן אינו בשתיהן)", r"$101$ (אינו מתחלק ב-$2$, ולכן אינו בשתיהן)"], 0,
            r"דוגמה נגדית חייבת להיות בקבוצה אחת ולא בשנייה. $100\in A_4=A_2\cap A_4$ אבל $100\notin A_8$. ב-$102$ ו-$101$ וב-$104$ שתי הקבוצות מסכימות.")])

# ---- Q3: pdf with e^x, bx, c/x
_MU = Fr(1, 5)
_A = (2 - 3 * _MU) / 5
_B = Fr(6, 5) * (_MU + 1)
DATA[(3, "א")] = item(
    [(r"נרמול: $a+\frac b2+c\int_1^\infty\frac{dx}x=1$", 3),
     (r"$\int_1^\infty\frac{dx}x$ מתבדר ולכן $c=0$", 2),
     (r"תוחלת: $\mathbb{E}[X]=-a+\frac b3=\mu$", 3),
     (r"פתרון המערכת: $a=\frac{2-3\mu}5$, $b=\frac65(\mu+1)$", 2)],
    [r"לדלג על $c$ ולהשאיר שלושה נעלמים בשתי משוואות: האינטגרל $\int_1^\infty\frac{dx}x$ מתבדר ולכן $c=0$.",
     r"לטעות בסימן של $\int_{-\infty}^0xe^x\,dx=-1$."],
    [choice(r"מצאו מקדמים לצפיפות כאשר נתונה התוחלת. איזה כלי מתאים?",
            [r"נרמול $\int f=1$ ותוחלת $\int xf$, שתי משוואות על המקדמים",
             r"נוסחת בייס",
             r"שיטת השטח (התפלגות אחידה על מלבן)",
             r"התפלגות בינומית"], 0,
            r"הצפיפות נתונה עד כדי מקדמים, והנתונים הם תנאי נרמול והתוחלת. בייס, שטחים ובינומית אינם רלוונטיים כאן."),
     num(r"מהו $c$? (האם $\int_1^\infty\frac{dx}x$ סופי?)", 0, r"האינטגרל מתבדר, ולכן אין ברירה אלא $c=0$ כדי שהנרמול יתקיים."),
     num(r"עבור $\mu=0$: מהו $a$? (פתרו את $a+\frac b2=1$ ו-$-a+\frac b3=\mu$).", Fr(2, 5), r"$a=\frac{2-3\mu}5=\frac25$."),
     num(r"עבור $\mu=0$: מהו $b$?", Fr(6, 5), r"$b=\frac65(\mu+1)=\frac65$. בדיקה: $\frac25+\frac35=1$ ו-$-\frac25+\frac25=0$.")])

DATA[(3, "ב")] = item(
    [(r"צפיפות חייבת להיות אי-שלילית: $a\ge0$", 1),
     (r"עבור $\mu=1$: $a=-\frac15<0$", 1),
     (r"מסקנה: לא ייתכן", 1)],
    [r"לבדוק רק את $b$ ולשכוח את $a$: דווקא $a$ נעשה שלילי."],
    [num(r"הציבו $\mu=1$: מהו $a=\frac{2-3\mu}5$?", Fr(-1, 5), r"$\frac{2-3}5=-\frac15$."),
     choice(r"האם ייתכן $\mu=1$?",
            [r"לא: $a<0$ והצפיפות חייבת להיות אי-שלילית", r"כן: המשוואות פתירות", r"כן: $b>0$ מספיק", r"לא: $b$ שלילי"], 0,
            r"פתירות המשוואות אינה מספיקה; הצפיפות חייבת להיות $\ge0$. כאן $a=-\frac15$ ו-$b=\frac{12}5>0$.")])

DATA[(3, "ג")] = item(
    [(r"הגדרה $F_X(t)=\int_{-\infty}^tf_X$ ופיצול לתחומים", 2),
     (r"$t<0$: $F_X(t)=\frac{2-3\mu}5e^t$", 2),
     (r"$0\le t<1$: $\frac{2-3\mu}5+\frac35(\mu+1)t^2$", 2),
     (r"$t\ge1$: $F_X(t)=1$, ושרטוט", 2)],
    [r"לשכוח להוסיף בתחום השני את המסה שנצברה מהתחום הראשון, $\frac{2-3\mu}5$.",
     r"להמשיך את הפרבולה אחרי $t=1$ במקום להציב $F_X(t)=1$."],
    [num(r"עבור $\mu=0$: $F_X(0)$ (המסה שנצברה מתחת ל-$0$).", Fr(2, 5), r"$\int_{-\infty}^0\frac25e^x\,dx=\frac25$."),
     num(r"עבור $\mu=0$: $F_X\left(\frac12\right)$.", Fr(11, 20), r"$\frac25+\frac35\cdot\left(\frac12\right)^2=\frac25+\frac3{20}=\frac{11}{20}$."),
     num(r"עבור $\mu=0$: $F_X(-1)$ (עד שלוש ספרות אחרי הנקודה).", Fr(2, 5) / _E, r"$\frac25e^{-1}\approx0.1472$.", tol=0.001),
     choice(r"כמה הוא $F_X(t)$ עבור $t\ge1$?", [r"$1$ (אין מסה מימין ל-$1$ כי $c=0$)", r"$\frac{2-3\mu}5$", r"$0$", r"תלוי ב-$\mu$"], 0,
            r"הצפיפות מתאפסת מימין ל-$1$, ולכן $F_X$ נשארת $1$.")])

DATA[(3, "ד")] = item(
    [(r"הצגה כיחס: $\frac{P(0<X<1)}{P(X>0)}$", 1),
     (r"$P(X>0)=1-F_X(0)$ ו-$P(0<X<1)=F_X(1)-F_X(0)$", 2),
     (r"$F_X(1)=1$ ולכן היחס הוא $1$", 1)],
    [r"לחשב $P(X<1)$ במקום $P(X<1\mid X>0)$: כאן הנתון מסיר את המסה השלילית, והתשובה $1$."],
    [num(r"עבור $\mu=0$: ההסתברות של אירוע התנאי $P(X>0)$.", Fr(3, 5), r"$1-F_X(0)=1-\frac25=\frac35$."),
     num(r"עבור $\mu=0$: $P(0<X<1)$.", Fr(3, 5), r"$F_X(1)-F_X(0)=1-\frac25=\frac35$."),
     num(r"מהי $P(X<1\mid X>0)$?", 1, r"$\frac{3/5}{3/5}=1$: כל המסה של $X>0$ נמצאת ב-$(0,1)$.")])

# ---- Q4: circuits, sample p = 0.6
_p = Fr(3, 5)
_blk = 2 * _p - _p ** 2                       # B||C
_Q1E, _Q1N = _blk ** 2, 2 * _p ** 2 - _p ** 4
_PQ1 = _p * _Q1E + (1 - _p) * _Q1N
_PQ2 = _p * _blk ** 2
_PJ = _p ** 3 * (3 - 2 * _p)
_PC = _PJ / _PQ2

DATA[(4, "א")] = item(
    [(r"נוסחת ההסתברות השלמה על היחידה האמצעית $E$", 2),
     (r"$P(Q_1/E)=(2p-p^2)^2$", 2),
     (r"$P(Q_1/\overline E)=2p^2-p^4$", 2),
     (r"הצבה: $P(Q_1)=p^3(2-p)^2+p^2(1-p)(2-p^2)$", 1)],
    [r"לנסות לצמצם את גשר $Q_1$ כמעגל טורי-מקבילי: אי אפשר, כי $E$ מחברת את שני המסלולים.",
     r"לשכוח שכש-$E$ פועלת שני הזוגות המקבילים מחוברים בטור, וכשהיא לא פועלת יש שני מסלולים בני שתי יחידות."],
    [choice(r"$Q_1$ הוא גשר בן חמש יחידות. איזו גישה מתאימה?",
            [r"נוסחת ההסתברות השלמה על היחידה האמצעית $E$ (פועלת או לא)",
             r"צמצום מיידי של טור ומקביל, בלי תנאי",
             r"התפלגות בינומית על מספר היחידות הפועלות",
             r"נוסחת בייס"], 0,
            r"בגשר היחידה האמצעית מקשרת שני מסלולים ולכן אי אפשר לצמצם. אחרי התניה ב-$E$ שני המקרים הם טורי-מקבילי פשוטים. הבינומית לא עוזרת כי חשוב אילו יחידות פועלות."),
     num(r"ב-$p=0.6$: $P(Q_1/E)$.", _Q1E, r"$(2p-p^2)^2=0.84^2=0.7056$."),
     num(r"ב-$p=0.6$: $P(Q_1/\overline E)$.", _Q1N, r"$2p^2-p^4=0.72-0.1296=0.5904$."),
     num(r"ב-$p=0.6$: $P(Q_1)$.", _PQ1, r"$0.6\cdot0.7056+0.4\cdot0.5904=0.65952$.")])

DATA[(4, "ב")] = item(
    [(r"$Q_2$ הוא טור של $A$, הזוג $B\|C$ והזוג $D\|E$", 3),
     (r"הסתברות זוג מקביל: $2p-p^2$", 2),
     (r"$P(Q_2)=p(2p-p^2)^2=p^3(2-p)^2$", 2)],
    [r"להכפיל $p^5$ (לשכוח שהזוגות מקבילים).", r"לחשב זוג מקביל כ-$2p$ ללא החיתוך $p^2$."],
    [choice(r"איך בנוי $Q_2$ ואיך מחשבים אותו?",
            [r"טור של שלושה חלקים בלתי תלויים, ומכפילים את הסתברויותיהם", r"סכום הסתברויות החלקים", r"תנאי על $E$ בלבד", r"בינומית $\mathrm{Bin}(5,p)$"], 0,
            r"טור פועל כשכל חלקיו פועלים, ולחלקים יחידות שונות ולכן בלתי תלויים: מכפלה. סכום ובינומית אינם מתאימים."),
     num(r"ב-$p=0.6$: $P(B\cup C)$ (זוג מקביל).", _blk, r"$2p-p^2=1.2-0.36=0.84$."),
     num(r"ב-$p=0.6$: $P(Q_2)$.", _PQ2, r"$0.6\cdot0.84^2=0.42336$.")])

DATA[(4, "ג")] = item(
    [(r"הגדרת ההסתברות המותנית: $\frac{P(Q_1\cap Q_2)}{P(Q_2)}$", 1),
     (r"פיצול לפי $A$ ו-$E$: אם $A$ לא פועלת אז $Q_2$ לא פועל", 2),
     (r"חישוב $P(\widetilde Q)=p^3(3-2p)$ מארבעת המקרים", 3),
     (r"חלוקה: $\frac{3-2p}{(2-p)^2}$", 1)],
    [r"להניח ש-$Q_1$ ו-$Q_2$ בלתי תלויים ולכתוב $P(Q_1\cap Q_2)=P(Q_1)P(Q_2)$: שניהם בנויים מאותן יחידות.",
     r"לחשב את $P(Q_2/Q_1)$ במקום $P(Q_1/Q_2)$."],
    [choice(r"מה המונה של $P(Q_1/Q_2)$?",
            [r"$P(Q_1\cap Q_2)$, כשהמעגלים תלויים כי יש להם אותן יחידות", r"$P(Q_1)P(Q_2)$", r"$P(Q_1)$", r"$P(Q_2/Q_1)$"], 0,
            r"לפי ההגדרה המונה הוא ההסתברות המשותפת. מכפלה מתאימה רק לאי-תלות, וכאן $0.65952\cdot0.42336\approx0.279$ שונה מההסתברות המשותפת $0.3888$."),
     num(r"ב-$p=0.6$: הסתברות אירוע התנאי $P(Q_2)$.", _PQ2, r"$p^3(2-p)^2=0.216\cdot1.96=0.42336$."),
     num(r"ב-$p=0.6$: $P(Q_1\cap Q_2)=p^3(3-2p)$.", _PJ, r"$0.216\cdot1.8=0.3888$ (דורש $A$ פועלת; אחר כך מקרים לפי $E$)."),
     num(r"ב-$p=0.6$: $P(Q_1/Q_2)$.", _PC, r"$\frac{0.3888}{0.42336}=\frac{3-2p}{(2-p)^2}=\frac{1.8}{1.96}\approx0.9184$.")])

DATA[(4, "ד")] = item(
    [(r"התניה באותו אירוע: $P(\overline{Q_1}/Q_2)=1-P(Q_1/Q_2)$", 2),
     (r"הצבת התשובה לסעיף ג", 1),
     (r"פישוט: $\frac{(1-p)^2}{(2-p)^2}$", 1)],
    [r"לחשב $1-P(Q_1)$ במקום $1-P(Q_1/Q_2)$: המשלים נעשה בתוך אותו עולם מותנה."],
    [choice(r"איך מחשבים את $P(\overline{Q_1}/Q_2)$?",
            [r"$1-P(Q_1/Q_2)$", r"$1-P(Q_1)$", r"$P(\overline{Q_1})P(Q_2)$", r"$1-P(Q_2/Q_1)$"], 0,
            r"המשלים נעשה בתוך המותנה (אותו אירוע תנאי). שאר הביטויים משנים את אירוע התנאי או מניחים אי-תלות."),
     num(r"ב-$p=0.6$: $P(Q_1/Q_2)$ (סעיף ג).", _PC, r"$\frac{1.8}{1.96}\approx0.9184$."),
     num(r"ב-$p=0.6$: $P(\overline{Q_1}/Q_2)$.", 1 - _PC, r"$1-0.9184=\frac{(1-p)^2}{(2-p)^2}=\frac{0.16}{1.96}\approx0.0816$.")])

# ---- Q5: random frequency omega ~ Exp(lambda); samples lambda=2, T=pi
_lam = 2
_q5 = _E ** -2                    # q = exp(-lambda*pi/T)
_S5 = _q5 / (1 - _q5) ** 2
_pref = _E - 1 / _E
DATA[(5, "א")] = item(
    [(r"שורשי $\cos(\omega t)$: $t_k=\frac{\pi}{2\omega}+\frac\pi\omega(k-1)$", 2),
     (r"$N_T=0$ שקול ל-$\omega<\frac\pi{2T}$ ולכן $P(N_T=0)=1-e^{-\lambda\pi/(2T)}$", 3),
     (r"$N_T=k$ שקול לכך ש-$\omega$ בקטע $\left(\frac{\pi(k-1/2)}T,\frac{\pi(k+1/2)}T\right)$", 3),
     (r"אינטגרל הצפיפות המעריכית והתשובה לכל $k\ge1$", 2)],
    [r"לטפל ב-$N_T$ כפואסוני: האפסים אינם תהליך פואסון, כולם נקבעים לפי $\omega$ יחיד.",
     r"לשכוח שהאפס הראשון הוא ב-$\frac{\pi}{2\omega}$ ולא ב-$\frac\pi\omega$ ולכן קצה הקטע הוא $\frac{\pi(k-1/2)}T$."],
    [choice(r"$N_T$ סופר את אפסי $\cos(\omega t)$ ב-$(0,T)$, כשהאקראיות היחידה היא $\omega$. איזה כלי מתאים?",
            [r"לתרגם את $\{N_T=k\}$ לאירוע על $\omega$ ולהשתמש בצפיפות המעריכית",
             r"התפלגות פואסון: האפסים מופיעים בקצב קבוע",
             r"התפלגות בינומית עם $T$ ניסויים",
             r"התפלגות גאומטרית: ממתינים לאפס הראשון"], 0,
            r"בהינתן $\omega$ האפסים נקבעים לגמרי במרווחים קבועים ואין אי-תלות בין מקטעים, ולכן אין תהליך פואסון. לכן מתרגמים את האירוע לאי-שוויון על $\omega$."),
     choice(r"לאיזה קטע של $\omega$ מתאים $\{N_T=k\}$ ($k\ge1$)?",
            [r"$\left(\frac{\pi(k-1/2)}T,\ \frac{\pi(k+1/2)}T\right)$", r"$\left(\frac{\pi k}T,\ \frac{\pi(k+1)}T\right)$",
             r"$\left(\frac{\pi(k-1)}T,\ \frac{\pi k}T\right)$", r"$\left(\frac{\pi(k-1/2)}T,\ \frac{\pi k}T\right)$"], 0,
            r"$N_T=k$ כאשר $t_k<T<t_{k+1}$, כלומר $\frac{\pi(k-1/2)}\omega<T<\frac{\pi(k+1/2)}\omega$. בהיפוך מקבלים את הקטע הראשון."),
     num(r"ב-$\lambda=2$, $T=\pi$: $P(N_T=0)$.", 1 - _E ** -1, r"$1-e^{-\lambda\pi/(2T)}=1-e^{-1}\approx0.6321$."),
     num(r"ב-$\lambda=2$, $T=\pi$: $P(N_T=1)$.", _E ** -1 - _E ** -3, r"$\omega\in\left(\frac12,\frac32\right)$: $e^{-1}-e^{-3}\approx0.3181$.")])

DATA[(5, "ב")] = item(
    [(r"$\mathbb{E}[N_T]=\sum kP(N_T=k)$, והוצאת הגורם הקבוע", 3),
     (r"זיהוי $q=e^{-\lambda\pi/T}$ והסכום $\sum kq^k=\frac q{(1-q)^2}$", 3),
     (r"הצבה ושימוש ב-$\frac q{(1-q)^2}=\frac1{\left(e^{x}-e^{-x}\right)^2}$", 2),
     (r"התשובה $\frac1{e^{\lambda\pi/(2T)}-e^{-\lambda\pi/(2T)}}$", 2)],
    [r"להציב את תוחלת פואסון $\lambda T$ במקום לסכם.", r"לשכוח את התחלת הסכום מ-$k=1$ כשמשתמשים ברמז."],
    [choice(r"איך מחשבים את $\mathbb{E}[N_T]$?",
            [r"$\sum kP(N_T=k)$ עם הסכום ההנדסי מהרמז", r"$\mathbb{E}[N_T]=\lambda T$ (תוחלת פואסון)", r"$\frac{T}{\pi}\mathbb{E}[\omega]$, בלי חלק שלם", r"$P(N_T=1)$"], 0,
            r"$N_T$ אינו פואסוני. הביטוי $\frac T\pi\mathbb{E}[\omega]$ מתעלם מכך ש-$N_T$ שלם (במדגם $\lambda=2,T=\pi$ הוא נותן $0.5$ במקום $0.4254$)."),
     num(r"ב-$\lambda=2$, $T=\pi$: $q=e^{-\lambda\pi/T}$ (עד שש ספרות).", _q5, r"$q=e^{-2}\approx0.135335$."),
     num(r"$\sum_{k\ge1}kq^k=\frac{q}{(1-q)^2}$ עבור אותו $q$.", _S5, r"$\frac{0.135335}{(0.864665)^2}\approx0.181019$."),
     num(r"מהי $\mathbb{E}[N_T]$ (המקדם $e-e^{-1}$ כפול הסכום)?", _pref * _S5, r"$\frac1{e-e^{-1}}\approx0.4254$.")])

_t2 = _E ** -3
_n2 = _E ** -4 * _pref
DATA[(5, "ג")] = item(
    [(r"המונה: $\{t_{k+1}>T\}\cap\{t_k<T\}=\{N_T=k\}$", 1),
     (r"$P(t_k<T)=P\left(\omega>\frac{\pi(k-1/2)}T\right)=e^{\frac{\lambda\pi}{2T}}e^{-\frac{\lambda\pi}Tk}$", 2),
     (r"הצבת $P(N_T=k)$ מסעיף א", 1),
     (r"פישוט: $1-e^{-\lambda\pi/T}$, בלתי תלוי ב-$k$", 1)],
    [r"לחלק ב-$P(t_{k+1}>T)$ או ב-$P(T)$ במקום ב-$P(t_k<T)$."],
    [choice(r"מהו המונה של $P(t_{k+1}>T\,/\,t_k<T)$?",
            [r"$P(N_T=k)$ (שני האירועים יחד אומרים שבדיוק $k$ שורשים לפני $T$)", r"$P(N_T\ge k)$", r"$P(t_{k+1}>T)$", r"$P(N_T\le k)$"], 0,
            r"$t_k<T$ אומר שיש לפחות $k$ שורשים לפני $T$, ו-$t_{k+1}>T$ אומר שיש לכל היותר $k$. יחד: בדיוק $k$."),
     num(r"ב-$\lambda=2$, $T=\pi$, $k=2$: הסתברות אירוע התנאי $P(t_2<T)$.", _t2, r"$P\left(\omega>\frac32\right)=e^{-3}\approx0.0498$."),
     num(r"באותם פרמטרים: $P(N_T=2)$.", _n2, r"$\omega\in\left(\frac32,\frac52\right)$: $e^{-3}-e^{-5}\approx0.0431$."),
     num(r"מהי ההסתברות המותנית?", 1 - _E ** -2, r"$\frac{0.0431}{0.0498}=1-e^{-2}\approx0.8647$ (תכונת חוסר הזיכרון של המעריכי).")])

# ---- Q6: batteries
DATA[(6, "א")] = item(
    [(r"זיהוי $n$ ניסויי ברנולי בלתי תלויים עם הצלחה $q$ (המפעל $A$)", 3),
     (r"$X=\sum X_j$ ולכן $X\sim\mathrm{Bin}(n,q)$", 2),
     (r"פונקציית ההסתברות $\binom nkq^k(1-q)^{n-k}$", 1)],
    [r"להשתמש בהיפרגאומטרית: הנתון הוא פרופורציה, לא אוכלוסייה סופית של גודל נתון.", r"לשכוח לציין את אי-התלות בין הסוללות."],
    [choice(r"בוחרים $n$ סוללות באקראי; פרופורציית $A$ במחסן היא $q$. איזה מודל מתאים ל-$X$?",
            [r"בינומי $\mathrm{Bin}(n,q)$: $n$ ניסויים בלתי תלויים עם הסתברות הצלחה $q$",
             r"היפרגאומטרי: חסר גודל המחסן ומספר הסוללות מ-$A$, ואלה אינם נתונים",
             r"גאומטרי: $n$ קבוע ואין המתנה להצלחה",
             r"פואסוני: $X$ חסום על ידי $n$"], 0,
            r"הפרופורציה $q$ נותנת הסתברות קבועה לכל סוללה. ההיפרגאומטרי דורש כמות סופית ידועה, הגאומטרי סופר ניסויים עד הצלחה, והפואסוני אינו חסום."),
     num(r"ב-$n=5$, $q=0.3$: $P(X=2)$.", Fr(5 * 4, 2) * Fr(3, 10) ** 2 * Fr(7, 10) ** 3, r"$\binom52\cdot0.3^2\cdot0.7^3=10\cdot0.09\cdot0.343=0.3087$.")])

DATA[(6, "ב")] = item(
    [(r"הגדרת $Y_j=1$ כשהסוללה מ-$A$ וגם פגומה", 3),
     (r"הסתברות ההצלחה $pq$ (אי-תלות בין המפעל לפגם)", 3),
     (r"$Y=\sum Y_j\sim\mathrm{Bin}(n,pq)$", 3),
     (r"פונקציית ההסתברות $\binom nk(pq)^k(1-pq)^{n-k}$", 3)],
    [r"לכתוב $\mathrm{Bin}(n,q)$ ולשכוח את הפגם, או $\mathrm{Bin}(n,p+q)$ (הסתברות שיכולה לעלות על $1$).",
     r"להשתמש ברמז עם סכום כפול כשהפתרון קצר יותר: סכום של $n$ משתני ברנולי."],
    [choice(r"$Y$ סופר סוללות ממפעל $A$ וגם פגומות. מה ההתפלגות?",
            [r"$\mathrm{Bin}(n,pq)$: כל סוללה היא הצלחה בהסתברות $pq$ ללא תלות", r"$\mathrm{Bin}(n,q)$", r"$\mathrm{Bin}(n,p+q)$", r"$\mathrm{Bin}(n,p)$"], 0,
            r"סוללה נספרת רק אם שני התנאים מתקיימים, והם בלתי תלויים: $pq$. $p+q$ עלול לעלות על $1$, ושני האחרים מתעלמים מתנאי."),
     num(r"ב-$p=0.2$, $q=0.5$: הסתברות ההצלחה לכל סוללה $pq$.", Fr(1, 10), r"$0.2\cdot0.5=0.1$."),
     num(r"ב-$n=4$: $P(Y=0)$.", Fr(9, 10) ** 4, r"$0.9^4=0.6561$."),
     num(r"ב-$n=4$: $P(Y=1)$.", 4 * Fr(1, 10) * Fr(9, 10) ** 3, r"$4\cdot0.1\cdot0.9^3=0.2916$.")])

_n, _pp, _qq = 4, Fr(1, 5), Fr(1, 2)
_varX, _varY = _n * _qq * (1 - _qq), _n * _pp * _qq * (1 - _pp * _qq)
_cov = _n * _pp * _qq * (1 - _qq)
DATA[(6, "ג")] = item(
    [(r"נוסחת המתאם $\frac{\operatorname{Cov}}{\sqrt{\operatorname{Var}X\operatorname{Var}Y}}$ והשונויות", 1),
     (r"$\mathbb{E}[XY]$ מפירוק לאינדיקטורים: $pqn+n(n-1)pq^2$", 2),
     (r"$\operatorname{Cov}[X,Y]=npq(1-q)$", 1),
     (r"$\rho=\sqrt{\frac{p(1-q)}{1-pq}}$", 1)],
    [r"להניח ש-$X$ ו-$Y$ בלתי תלויים ולקבל $\operatorname{Cov}=0$: $Y$ נספר מתוך $X$.",
     r"לשכוח את האיברים $j=k$ ב-$\mathbb{E}[XY]$ ($\mathbb{E}[X_j^2]=q$)."],
    [choice(r"איך מחשבים את $\mathbb{E}[XY]$?",
            [r"מפרקים $X=\sum X_j$ ו-$Y=\sum X_kZ_k$, ומפרידים אינדקסים שווים ושונים", r"$\mathbb{E}[X]\mathbb{E}[Y]$ כי המשתנים בלתי תלויים", r"$\mathbb{E}[X]+\mathbb{E}[Y]$", r"$\mathbb{E}[X^2]$"], 0,
            r"$Y$ סופר חלק מהסוללות ש-$X$ סופר, ולכן תלויים. בפירוק האינדקסים השווים נותנים $\mathbb{E}[X_j^2]\mathbb{E}[Z_j]=pq$ והשונים נותנים $pq^2$."),
     num(r"ב-$n=4$, $p=0.2$, $q=0.5$: $\operatorname{Cov}[X,Y]=npq(1-q)$.", _cov, r"$4\cdot0.2\cdot0.5\cdot0.5=0.2$."),
     num(r"באותם פרמטרים: $\operatorname{Var}X=nq(1-q)$.", _varX, r"$4\cdot0.5\cdot0.5=1$."),
     num(r"באותם פרמטרים: $\operatorname{Var}Y=npq(1-pq)$.", _varY, r"$4\cdot0.1\cdot0.9=0.36$."),
     num(r"מהו $\rho[X,Y]$?", Fr(1, 3), r"$\frac{0.2}{1\cdot0.6}=\frac13$, וגם $\sqrt{\frac{p(1-q)}{1-pq}}=\sqrt{\frac19}$.")])

DATA[(6, "ד")] = item(
    [(r"הצבה $p=1$: $\rho=1$", 1), (r"הסבר: $Y=X$ כשכל הסוללות פגומות", 1)],
    [r"לפרש $\rho=1$ כאי-תלות: מתאם $1$ הוא תלות לינארית מלאה."],
    [num(r"ב-$q=0.5$, $p=1$: $\rho=\sqrt{\frac{p(1-q)}{1-pq}}$.", 1, r"$\sqrt{\frac{0.5}{0.5}}=1$."),
     choice(r"מדוע?", [r"כש-$p=1$ כל הסוללות פגומות ולכן $Y=X$", r"כי $X$ ו-$Y$ בלתי תלויים", r"כי $Y=0$", r"כי $q=1$"], 0,
            r"$Y=X$ ולכן המתאם $\rho[X,X]=1$. אי-תלות היתה נותנת $0$, ו-$Y=0$ היה נותן שונות $0$.")])

# ---- extra sims (symbolic answers, at sample parameters stated in `estimate`)
_pc = float(_p)
EXTRA_SIMS = {
    (3, "א"): {"kind": "pdf", "estimate": "E[X] ב-μ=0.2 (a=0.28, b=1.44)", "exact": 0.2,
               "params": {"pieces": [{"from": -30, "to": 0, "expr": "0.28*exp(x)"}, {"from": 0, "to": 1, "expr": "1.44*x"}],
                          "measure": "mean", "expr": "x"}},
    (4, "א"): {"kind": "circuit", "estimate": "P(Q1) ב-p=0.6", "exact": float(_PQ1), "params": _br(_pc)},
    (4, "ב"): {"kind": "circuit", "estimate": "P(Q2) ב-p=0.6", "exact": float(_PQ2),
               "params": {"event": "S", "network": {"type": "series", "children": [
                   {"type": "comp", "id": "A", "p": _pc},
                   {"type": "parallel", "children": [{"type": "comp", "id": "B", "p": _pc}, {"type": "comp", "id": "C", "p": _pc}]},
                   {"type": "parallel", "children": [{"type": "comp", "id": "D", "p": _pc}, {"type": "comp", "id": "E", "p": _pc}]}]}}},
    (4, "ג"): {"kind": "circuit", "estimate": "P(Q1 | Q2) ב-p=0.6", "exact": float(_PC),
               "params": dict(_br(_pc), event="S", given=_Q2_UP)},
    (4, "ד"): {"kind": "circuit", "estimate": "P(not Q1 | Q2) ב-p=0.6", "exact": float(1 - _PC),
               "params": dict(_br(_pc), event="S == 0", given=_Q2_UP)},
    (5, "א"): {"kind": "pdf", "estimate": "P(N_T=1) ב-λ=2, T=π", "exact": _E ** -1 - _E ** -3,
               "params": {"pieces": [{"from": 0, "to": 30, "expr": "2*exp(-2*x)"}], "event": "x > 1/2 and x < 3/2"}},
    (5, "ב"): {"kind": "pdf", "estimate": "E[N_T] ב-λ=2, T=π", "exact": 1 / _pref,
               "params": {"pieces": [{"from": a, "to": b, "expr": "2*exp(-2*x)"} for a, b in zip([0] + [k + 0.5 for k in range(30)], [k + 0.5 for k in range(30)] + [30.5])],
                          "measure": "mean", "expr": "floor(x + 1/2)"}},
    (5, "ג"): {"kind": "pdf", "estimate": "P(t3>T | t2<T) ב-λ=2, T=π", "exact": 1 - _E ** -2,
               "params": {"pieces": [{"from": 0, "to": 30, "expr": "2*exp(-2*x)"}], "event": "x < 5/2", "given": "x > 3/2"}},
    (6, "א"): {"kind": "urn", "estimate": "P(X=2) ב-n=5, q=0.3", "exact": 0.3087,
               "params": {"counts": {"fromA": 3, "fromB": 7}, "draws": 5, "replace": True, "event": "fromA == 2"}},
    (6, "ב"): {"kind": "urn", "estimate": "P(Y=1) ב-n=4, pq=0.1 (p=0.2, q=0.5)", "exact": 0.2916,
               "params": {"counts": {"hit": 1, "miss": 9}, "draws": 4, "replace": True, "event": "hit == 1"}},
    (6, "ג"): {"kind": "custom_discrete", "estimate": "Cov[X,Y] ב-n=1, p=0.2, q=0.5", "exact": 0.05,
               "params": {"joint": [{"p": 0.5, "X": 0, "Y": 0}, {"p": 0.4, "X": 1, "Y": 0}, {"p": 0.1, "X": 1, "Y": 1}],
                          "measure": "cov", "expr": ["X", "Y"]}},
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
