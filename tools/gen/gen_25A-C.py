# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-C.json -- probability (course 20021), semester A 2025, moed C.
Date: the exam header (and this file) say 11.05.2025; the source file name says 11.12, which is wrong.
6 questions, 26 items (Q1 5, Q2 6, Q3 3, Q4 4, Q5 5, Q6 3), 25 points each (Q5 d, e are 5-point bonus parts).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-C.py

Source: exam pp.1-3, handwritten official solutions on grid paper pp.4-17. Student/lecturer names are not copied.

Transcription notes
- Part keys: single letters. Q1 prints "א-1..א-3, ב-1, ב-2" -> a, b, c, d, e. Q2 prints "א-1..א-4, ב, ג" -> a..d, e, f.
  The printed label is the first bold token of each question text.
- Q3 c HOLD: the official key is 1-1/e (about 0.63) but the exact value of the conditional probability with the
  official a=3/2, b=1/4 is 1-(4/13)e^{-1/2} (about 0.81). See docs/ASK_ADIR.md, tools/verify/25A-C/check.py.
- Q4 b, c HOLD: the printed unit H works with probability q, but the official polynomials are the q=p case
  (the solution writes P(H)=p). They are correct only for q=p. Parts a and d do not depend on q and are shipped.
- Q5: the official solution gives only the final formulas (no derivation); they are transcribed as printed.
- Q1 / Q6 area items carry `region` data (REGIONS below; RAW_SCHEMA `region`).
- Math never holds Hebrew.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-C.json"
CODE = "25A-C"
IMG = "images/exams/25A-C-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"לפניך מלבן בעל צלעות אשר אורכן $X$ ו-$Y$ מהווים משתנים מקריים בלתי תלויים: $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,\mathbf{2})$. "
          r"יהי $S$ שטח המלבן ויהי $L$ היקף המלבן.")

Q1_SOL0 = r"""$S=XY$ ו-$L=2(X+Y)$. לפי הנתון $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,2)$ בלתי תלויים, ולכן נשתמש בגישה הקלאסית: מרחב המדגם הוא המלבן $\Omega=(0,1)\times(0,2)$ ושטחו $|\Omega|=2$."""

questions.append(Q(
    1, "א", "uniform_geometric",
    r"מצאו את ההסתברויות הבאות:" "\n" r"**א-1:** $P(S<2/3)$ (5 נק׳).",
    Q1_SOL0 + r"""
$$P(S<\tfrac23)=P\left(Y<\frac{2}{3X}\right)=\frac{\left|\{Y<\frac2{3X}\}\right|}{|\Omega|},\qquad|\Omega|=2.$$
ההיפרבולה $y=\frac2{3x}$ חותכת את הישר $y=2$ ב-$x=\frac13$. עבור $0<x<\frac13$ כל $0<y<2$ מתאים, ועבור $\frac13<x<1$ מתקבל $0<y<\frac2{3x}$:
$$\left|\{Y<\tfrac2{3X}\}\right|=2\cdot\frac13+\int_{1/3}^{1}\frac{2}{3x}\,dx.$$
לכן
$$P(S<\tfrac23)=\frac12\left\{\frac23+\frac23\ln3\right\}=\frac{1+\ln3}{3}\approx0.70.$$""",
    5, contextId="c1", image=IMG + "Q1-rect.png"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"מצאו את ההסתברויות הבאות:" "\n" r"**א-2:** $P(L<2)$ (5 נק׳).",
    Q1_SOL0 + r"""
$$P(L<2)=P(X+Y<1)=P(Y<1-X)=\frac{\left|\{Y<1-X\}\right|}{|\Omega|}=\frac{\frac12\cdot1\cdot1}{2}=\frac14.$$""",
    5, contextId="c1", image=IMG + "Q1-rect.png"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"מצאו את ההסתברויות הבאות:" "\n" r"**א-3:** $P(S<2/3\ /\ L>2)$ (5 נק׳).",
    Q1_SOL0 + r"""
$$P(S<\tfrac23\mid L>2)=\frac{P(S<\frac23\cap L>2)}{P(L>2)}.$$
המשולש $\{X+Y<1\}$ נמצא כולו בתוך $\{S<\frac23\}$ (שם $XY\le\frac14$), ולכן
$$P(S<\tfrac23\cap L>2)=P(S<\tfrac23)-P(L<2)=\frac{1+\ln3}{3}-\frac14,\qquad P(L>2)=1-\frac14=\frac34.$$
מכאן
$$P(S<\tfrac23\mid L>2)=\frac{\frac{1+\ln3}{3}-\frac14}{\frac34}=\frac{1+4\ln3}{9}\approx0.60.$$""",
    5, contextId="c1", image=IMG + "Q1-rect.png"))

questions.append(Q(
    1, "ד", "continuous_rv",
    r"חשבו תוחלות ושונויות:" "\n" r"**ב-1:** תוחלת $\mathbb{E}[L]$ ושונות $\operatorname{var}[L]$ (5 נק׳).",
    r"""$L=2(X+Y)$, והמשתנים בלתי תלויים:
$$\mathbb{E}[L]=2\bigl(\mathbb{E}[X]+\mathbb{E}[Y]\bigr)=2\left(\frac12+1\right)=3.$$
$$\operatorname{Var}[L]=4\bigl(\operatorname{Var}[X]+\operatorname{Var}[Y]\bigr)=4\left(\frac1{12}+\frac4{12}\right)=\frac53\approx1.67.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ה", "continuous_rv",
    r"חשבו תוחלות ושונויות:" "\n" r"**ב-2:** תוחלת $\mathbb{E}[S]$ ושונות $\operatorname{var}[S]$ (5 נק׳).",
    r"""$S=XY$ ו-$X,Y$ בלתי תלויים:
$$\mathbb{E}[S]=\mathbb{E}[X]\,\mathbb{E}[Y]=\frac12\cdot1=\frac12.$$
$$\operatorname{Var}[S]=\mathbb{E}[X^2Y^2]-\bigl(\mathbb{E}[S]\bigr)^2=\mathbb{E}[X^2]\,\mathbb{E}[Y^2]-\frac14=\frac13\cdot\frac43-\frac14=\frac49-\frac14=\frac7{36}\approx0.19.$$""",
    5, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_TXT = r"יהיו $A$ ו-$B$ מאורעות כלשהם בעלי הסתברות $P(A)=p$ ו-$P(B)=q$. כמו כן, נתון כי $P(A\cup B)=s$."
Q2_A = r"חשבו את ההסתברויות הבאות (4 נק׳ לכל תת סעיף):"

questions.append(Q(
    2, "א", "conditional_bayes",
    Q2_A + "\n" + r"**(א-1):** $P(A/B)$.",
    r"""$$P(A/B)=\frac{P(A\cap B)}{P(B)}=\frac{P(A)+P(B)-P(A\cup B)}{P(B)}=\frac{p+q-s}{q}.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ב", "conditional_bayes",
    Q2_A + "\n" + r"**(א-2):** $P(B/\overline{A})$.",
    r"""$$P(B/\overline A)=\frac{P(\overline A/B)\,P(B)}{P(\overline A)}=\frac{\bigl[1-P(A/B)\bigr]P(B)}{1-P(A)}=\frac{\left[1-\left(1-\frac{s-p}{q}\right)\right]q}{1-p}=\frac{s-p}{1-p}.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    Q2_A + "\n" + r"**(א-3):** $P(A/\overline{B})$.",
    r"""$$P(A/\overline B)=\frac{P(\overline B/A)\,P(A)}{P(\overline B)}=\frac{P(A)\bigl[1-P(B/A)\bigr]}{1-P(B)}=\frac{p}{1-q}\left[1-\frac{P(A/B)P(B)}{P(A)}\right]=\frac p{1-q}\left[1-\frac{p+q-s}{q}\cdot\frac qp\right]=\frac{s-q}{1-q}.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ד", "conditional_bayes",
    Q2_A + "\n" + r"**(א-4):** $P(\overline{A}/\overline{B})$.",
    r"""$$P(\overline A/\overline B)=1-P(A/\overline B)=1-\frac{s-q}{1-q}=\frac{1-s}{1-q}.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ה", "independence",
    r"עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו מאורעות **בלתי תלויים**? (4 נק׳)",
    r"""$A$ ו-$B$ בלתי תלויים אם ורק אם $P(A\cap B)=P(A)P(B)$. מכיוון ש-$P(A\cap B)=p+q-s$,
$$p+q-s=pq\ \Longleftrightarrow\ s=p+q-pq.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ו", "basics_events",
    r"עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו מאורעות **זרים**? (5 נק׳)",
    r"""$A$ ו-$B$ זרים אם ורק אם $P(A\cap B)=0$, כלומר $p+q-s=0$:
$$s=p+q.$$""",
    5, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות מהצורה" "\n"
          r"$$f_X(x)=\begin{cases}0,&x<-1;\\a(1+x),&-1\le x<0;\\b\,e^{-x},&x\ge0.\end{cases}$$")

questions.append(Q(
    3, "א", "continuous_rv",
    r"בהנחה כי $\mathbb{E}[X]=0$, מצאו את הפרמטרים $a$ ו-$b$. (10 נק׳)",
    r"""**נרמול:**
$$\int_{-\infty}^{\infty}f_X(x)\,dx=a\int_{-1}^0(1+x)\,dx+b\int_0^\infty e^{-x}\,dx=\frac a2+b=1.$$
**תוחלת:**
$$\mathbb{E}[X]=a\int_{-1}^0x(1+x)\,dx+b\int_0^\infty xe^{-x}\,dx=-\frac a6+b\,\Gamma(2)=-\frac a6+b=0\ \Longrightarrow\ b=\frac a6.$$
פתרון שתי המשוואות:
$$a=\frac32,\qquad b=\frac14.$$""",
    10, contextId="c3"))

questions.append(Q(
    3, "ב", "continuous_rv",
    r"בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את התוצאה. (10 נק׳)",
    r"""הצפיפות היא $f_X(x)=\frac32(1+x)$ על $[-1,0)$ ו-$\frac14e^{-x}$ על $x\ge0$. $F_X(t)=\int_{-\infty}^tf_X(x)\,dx$:
$$F_X(t)=\begin{cases}0,&t<-1,\\\dfrac34(1+t)^2,&-1\le t<0,\\1-\dfrac14e^{-t},&t\ge0.\end{cases}$$
הגרף: אפס עד $-1$, עלייה פרבולית עד הערך $\frac34$ ב-$t=0$, אחר כך עלייה אקספוננציאלית שואפת ל-$1$.""",
    10, contextId="c3"))

HOLD_Q3C = ("The official key is 1-1/e (about 0.63) but (F(1/2)-F(-1/2))/(1-F(-1/2)) with the official F "
            "equals 1-(4/13)e^{-1/2} (about 0.81); confirmed by exact computation and Monte Carlo. See ASK_ADIR.")

questions.append(Q(
    3, "ג", "continuous_rv",
    r"מהי ההסתברות המותנית $P(X<1/2\ /\ X>-1/2)$? (5 נק׳)",
    r"""$$P(X<\tfrac12\mid X>-\tfrac12)=\frac{P(-\frac12<X<\frac12)}{P(X>-\frac12)}=\frac{F_X(\frac12)-F_X(-\frac12)}{1-F_X(-\frac12)}=1-\frac1e\approx0.63.$$""",
    5, contextId="c3", hold=HOLD_Q3C))

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"סטודנט של המכון הטכנולוגי חולון הרכיב מעגל $\boldsymbol{Q_1}$ מיחידות $A$, $B$, $C$, $D$, $E$, $F$ ו-$G$ הפועלות ללא תלות אחת בשנייה בהסתברויות הזהות $p$." "\n"
          r"לאחר מכן, הוא שינה את המעגל $\boldsymbol{Q_1}$ על ידי ״הוספת״ היחידה $H$ אשר פועלת בהסתברות $q$ וזאת ללא תלות בכל יחידה אחרת. המעגל שנוצר הינו $\boldsymbol{Q_2}$.")

questions.append(Q(
    4, "א", "circuits",
    r"מהי ההסתברות שמעגל $Q_1$ פועל? (8 נק׳)",
    r"""נפעל לפי נוסחת ההסתברות השלמה על היחידה $E$ (הגשר):
$$P(Q_1)=P(Q_1/E)\,P(E)+P(Q_1/\overline E)\,P(\overline E),\qquad P(E)=p,\ P(\overline E)=1-p.$$
- **$E$ פועלת:** $E$ מחברת את הצמתים, והמעגל הופך ל-($A\,\|\,B$) בטור עם ($C\,\|\,(D$ בטור $F)$) בטור עם $G$:
$$P(Q_1/E)=(2p-p^2)\,(p+p^2-p^3)\cdot p=p^3(2-p)(1+p-p^2).$$
- **$E$ לא פועלת:** $(A,C)\ \|\ (B,D,F)$ בטור עם $G$:
$$P(Q_1/\overline E)=(p^2+p^3-p^5)\cdot p=p^3(1+p-p^3).$$

מכאן
$$P(Q_1)=p^4(2-p)(1+p-p^2)+(1-p)p^3(1+p-p^3)=p^3\left\{1+2p-4p^3+2p^4\right\}.$$""",
    8, contextId="c4"))

HOLD_Q4 = ("The printed unit H works with probability q, but the official solution computes with P(H)=p, so its "
           "polynomial p^3(2+4p-2p^2-13p^3+14p^4-4p^5) is the q=p case only (verified by exact enumeration and Monte Carlo). See ASK_ADIR.")

questions.append(Q(
    4, "ב", "circuits",
    r"מהי ההסתברות שמעגל $Q_2$ פועל? (8 נק׳)",
    r"""נפעל לפי נוסחת ההסתברות השלמה על $H$ (בפתרון הרשמי מציבים $P(H)=p$):
$$P(Q_2)=P(Q_2/H)\,P(H)+P(Q_2/\overline H)\,P(\overline H),\qquad P(Q_2/\overline H)=P(Q_1).$$
כאשר $H$ פועלת, נקבל את המעגל $\widetilde Q_2$: היחידות $G,F$ במקביל, כך שהן מתנהגות כיחידה אחת $J$ עם $P(J)=p(2-p)$ בטור עם $C$:
$$P(Q_2/H)=p^2(1+3p-9p^3+8p^4-2p^5).$$
הצבה בנוסחת ההסתברות השלמה נותנת
$$P(Q_2)=p^3\left(2+4p-2p^2-13p^3+14p^4-4p^5\right).$$""",
    8, contextId="c4", hold=HOLD_Q4))

questions.append(Q(
    4, "ג", "circuits",
    r"מהי ההסתברות שלפחות אחד המעגלים פעל? (6 נק׳)",
    r"""נסמן $Q=Q_1\cup Q_2$ ונפעל לפי נוסחת ההסתברות השלמה על ארבעת המקרים של $G$ ו-$H$ (פועלת או לא):
$$P(Q)=P(Q/G\cap H)P(G\cap H)+P(Q/G\cap\overline H)P(G\cap\overline H)+P(Q/\overline G\cap H)P(\overline G\cap H)+P(Q/\overline G\cap\overline H)P(\overline G\cap\overline H),$$
כאשר המחובר האחרון הוא $0$ (שני המעגלים דורשים אחת מהיחידות $G,H$). אחרי הצבה ופישוט מתקבל אותו ביטוי כמו $P(Q_2)$:
$$P(Q_1\cup Q_2)=p^3\left\{2+4p-2p^2-13p^3+14p^4-4p^5\right\}.$$""",
    6, contextId="c4", hold=HOLD_Q4))

questions.append(Q(
    4, "ד", "circuits",
    r"**אם ידוע** כי מעגל $Q_1$ פעל, מהי ההסתברות שהמעגל $Q_2$ פעל גם כן? (3 נק׳)",
    r"""$$P(Q_2/Q_1)=\frac{P(Q_1\cap Q_2)}{P(Q_1)}=\frac{P(Q_1)+P(Q_2)-P(Q_1\cup Q_2)}{P(Q_1)}=\frac{p^3(1+2p-4p^3+2p^4)}{p^3\{1+2p-4p^3+2p^4\}}=1.$$
הסבר: ההוספה של $H$ מוסיפה רק מסלולים אפשריים, ולכן אם $Q_1$ פועל אז בהכרח גם $Q_2$ פועל.""",
    3, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_TXT = (r"$n$ מספרים $\{X_1,X_2,\ldots,X_n\}$ נבחרו באקראי **וללא החזרה** מאוסף המספרים $\{1,2,3,\ldots,N-1,N\}$. יהי" "\n"
          r"$$X_{\min}=\min\{X_1,X_2,\ldots,X_n\}$$"
          "\n" r"המספר הקטן ביותר ו—" "\n"
          r"$$X_{\max}=\max\{X_1,X_2,\ldots,X_n\}$$"
          "\n" r"המספר הגדול ביותר בין $n$ המספרים שנבחרו.")

questions.append(Q(
    5, "א", "minmax_transform",
    r"חשבו את פונקציית ההסתברות $P(X_{\min}=k)$ וציינו את הערכים האפשריים של $X_{\min}$. (8 נק׳)",
    r"""$$P(X_{\min}=k)=\frac{\binom{N-k}{n-1}}{\binom Nn},\qquad k=1,2,\ldots,N-n+1.$$""",
    8, contextId="c5"))

questions.append(Q(
    5, "ב", "minmax_transform",
    r"חשבו את פונקציית ההסתברות $P(X_{\max}=\ell)$ וציינו את הערכים האפשריים של $X_{\max}$. (8 נק׳)",
    r"""$$P(X_{\max}=\ell)=\frac{\binom{\ell-1}{n-1}}{\binom Nn},\qquad \ell=n,n+1,\ldots,N.$$""",
    8, contextId="c5"))

questions.append(Q(
    5, "ג", "joint_discrete",
    r"חשבו את פונקציית ההסתברות המשותפת $P(X_{\min}=k,\ X_{\max}=\ell)$ וציינו את הערכים האפשריים של משתנה דו ממדי $(X_{\min},X_{\max})$. (9 נק׳)",
    r"""$$P(X_{\min}=k,\ X_{\max}=\ell)=\frac{\binom{\ell-k-1}{n-2}}{\binom Nn},\qquad 1\le k<\ell\le N.$$""",
    9, contextId="c5"))

questions.append(Q(
    5, "ד", "minmax_transform",
    r"**סעיף בונוס 1:** חשבו את התוחלת $\mathbb{E}[X_{\min}]$. (5 נק׳ - הניקוד יינתן רק עבור פתרון מלא.)",
    r"""$$\mathbb{E}[X_{\min}]=\frac{N+1}{n+1}.$$""",
    5, contextId="c5"))

questions.append(Q(
    5, "ה", "minmax_transform",
    r"**סעיף בונוס 2:** חשבו את התוחלת $\mathbb{E}[X_{\max}]$. (5 נק׳ - הניקוד יינתן רק עבור פתרון מלא.)",
    r"""$$\mathbb{E}[X_{\max}]=n\,\frac{N+1}{n+1}.$$""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_TXT = (r"יהיו $X\sim U_c(0,L)$ ו-$Y\sim U_c(0,L)$ שני משתנים מקריים בלתי תלויים בעלי התפלגות אחידה. נסמן ב-$\min(X,Y)$ את הערך הקטן בין השניים וב-$\max(X,Y)$ את הערך הגדול בין השניים. $L>0$ כאשר. כמו כן, נגדיר משתנה מקרי חדש" "\n"
          r"$$Z=\frac{\min(X,Y)}{\max(X,Y)}.$$")

questions.append(Q(
    6, "א", "minmax_transform",
    r"חשבו ושרטטו את פונקציית ההתפלגות המצטברת $F_Z(t)$ של משתנה מקרי $Z$. (15 נק׳)",
    r"""$F_Z(t)=P(Z\le t)$ לכל $t\in\mathbb R$. מאחר ש-$\frac{\min(X,Y)}{\max(X,Y)}\ge0$, מתקבל $F_Z(t)=0$ עבור $t<0$.
מחלקים את המאורע לפי מי מהשניים גדול: $F_Z(t)=P(Z\le t\cap X>Y)+P(Z\le t\cap X\le Y)$.
כאשר $X>Y$ מתקיים $Z=\frac YX$, ולכן $P(Z\le t\cap X>Y)=P(Y\le tX\cap Y<X)=\frac{|\{Y\le tX,\ Y<X\}|}{|\Omega|}$ עם $|\Omega|=L^2$.
- **מקרה 1, $0\le t<1$:** האזור הוא משולש מתחת לישר $y=tx$ ושטחו $\frac{tL^2}{2}$.
- **מקרה 2, $t\ge1$:** האזור הוא כל המשולש מתחת ל-$y=x$ ושטחו $\frac12L^2$.

לכן
$$P(Z\le t\cap X>Y)=\begin{cases}0,&t<0,\\t/2,&0\le t<1,\\1/2,&t\ge1.\end{cases}$$
בגלל הסימטריה בין $X$ ל-$Y$ (החלפת התפקידים) מתקבל אותו ביטוי עבור $X\le Y$. לכן
$$F_Z(t)=\begin{cases}0,&t<0,\\t,&0\le t<1,\\1,&t\ge1.\end{cases}$$
הגרף: אפס עד $0$, ישר באלכסון עד $(1,1)$ ואז קבוע $1$.""",
    15, contextId="c6"))

questions.append(Q(
    6, "ב", "minmax_transform",
    r"חשבו ושרטטו את פונקציית צפיפות ההסתברות $f_Z(t)$ של משתנה מקרי $Z$. (5 נק׳)",
    r"""$$f_Z(t)=F_Z'(t)=\begin{cases}1,&0\le t\le1,\\0,&\text{else},\end{cases}\qquad\Longrightarrow\qquad Z\sim U_c(0,1).$$""",
    5, contextId="c6"))

questions.append(Q(
    6, "ג", "continuous_rv",
    r"חשבו את התוחלת $\mathbb{E}[Z]$ ואת השונות $\operatorname{var}[Z]$. (5 נק׳)",
    r"""$$\mathbb{E}[Z]=\int_0^1z\,dz=\frac12.$$
$$\operatorname{Var}[Z]=\mathbb{E}[Z^2]-\bigl(\mathbb{E}[Z]\bigr)^2=\frac13-\frac14=\frac1{12}.$$""",
    5, contextId="c6"))

# ------------------------------------------------------------------ area regions (RAW_SCHEMA `region`)
REGIONS = {
    (1, 'א'): {"space": {"x": [0, 1], "y": [0, 2]}, "event": [{"expr": "x*y", "op": "<", "c": "2/3"}], "exact": 0.6995374295560367, "labels": {"x": "X", "y": "Y"}, "caption": "האזור xy<2/3"},
    (1, 'ב'): {"space": {"x": [0, 1], "y": [0, 2]}, "event": [{"a": 1, "b": 1, "c": 1, "op": "<"}], "exact": 0.25, "labels": {"x": "X", "y": "Y"}, "caption": "האזור x+y<1 (L<2)"},
    (1, 'ג'): {"space": {"x": [0, 1], "y": [0, 2]}, "event": [{"expr": "x*y", "op": "<", "c": "2/3"}], "given": [{"a": 1, "b": 1, "c": 1, "op": ">"}], "exact": 0.5993832394080488, "labels": {"x": "X", "y": "Y"}, "caption": "S<2/3 בהינתן L>2"},
    (6, 'א'): {"space": {"x": [0, 1], "y": [0, 1]}, "event": ["min(x,y) <= 0.4*max(x,y)"], "exact": 0.4, "labels": {"x": "X/L", "y": "Y/L"}, "caption": "האזור min/max ≤ t עבור t=0.4 (אחרי חלוקה ב-L)"},
}
for _q in questions:
    _r = REGIONS.get((_q["num"], _q.get("part")))
    if _r is not None:
        _q["region"] = _r

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ה, מועד ג (11.05.2025)",
    "year": 2025,
    "examDate": "11.05.2025",
    "sourceFile": "25A-C exam pp.1-3",
    "solutionFile": "25A-C handwritten official solutions, pp.4-17",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1", "text": Q1_TXT},
        "c2": {"kind": "text", "title": "שאלה 2", "text": Q2_TXT},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_TXT},
        "c4": {"kind": "image", "title": "שאלה 4: מעגלים", "image": IMG + "Q4-circuits.png", "caption": Q4_TXT},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_TXT},
        "c6": {"kind": "text", "title": "שאלה 6", "text": Q6_TXT},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
