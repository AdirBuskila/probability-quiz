# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-C.json -- probability (course 20021), semester A 2025, moed C.
Date: the exam header (and this file) say 11.05.2025; the source file name says 11.12, which is wrong.
6 questions, 26 items (Q1 5, Q2 6, Q3 3, Q4 4, Q5 5, Q6 3), 25 points each (Q5 d, e are 5-point bonus parts).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-C.py

Source: exam pp.1-3, handwritten official solutions on grid paper pp.4-17. Student/lecturer names are not copied.

Transcription notes
- Part keys: single letters. Q1 prints "א-1..א-3, ב-1, ב-2" -> a, b, c, d, e. Q2 prints "א-1..א-4, ב, ג" -> a..d, e, f.
  The printed label is the first bold token of each question text.
- Q3 c TYPO RULING (arbiter 2026-10-18, the printed question wins): the official key is 1-1/e (about 0.63) but the
  official formula with the official a=3/2, b=1/4 gives 1-(4/13)e^{-1/2} (about 0.81). Shipped the corrected value,
  solutionSource "solved", official:false, "הפתרון הרשמי עם תיקון" prefix.
- Q4 b, c TYPO RULING: the printed unit H works with probability q, but the official polynomials are the q=p case
  (the solution writes P(H)=p). Shipped the official method with P(H)=q:
  P(Q2) = P(Q1 u Q2) = q p^2(1+3p-9p^3+8p^4-2p^5) + (1-q) p^3(1+2p-4p^3+2p^4), solved, official:false, prefix.
  Parts a and d do not depend on q and stay official. All verified exactly and by Monte Carlo in tools/verify/25A-C/check.py.
- Q5: the official solution gives only the final formulas (no derivation); they are transcribed as printed.
- Q1 / Q6 area items carry `region` data (REGIONS below; RAW_SCHEMA `region`).
- Math never holds Hebrew.
"""
import json, math, pathlib
from fractions import Fraction as Fr

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

questions.append(Q(
    3, "ג", "continuous_rv",
    r"מהי ההסתברות המותנית $P(X<1/2\ /\ X>-1/2)$? (5 נק׳)",
    r"""**הפתרון הרשמי עם תיקון:** בפתרון הרשמי התשובה הסופית היא $1-\frac1e\approx0.63$, אבל הצבת $F_X$ מסעיף ב בנוסחה הרשמית נותנת $1-\frac4{13}e^{-1/2}\approx0.81$. התיקון נבדק (חישוב מדויק וסימולציה).
$$P(X<\tfrac12\mid X>-\tfrac12)=\frac{P(-\frac12<X<\frac12)}{P(X>-\frac12)}=\frac{F_X(\frac12)-F_X(-\frac12)}{1-F_X(-\frac12)}.$$
מסעיף ב: $F_X(\frac12)=1-\frac14e^{-1/2}$ ו-$F_X(-\frac12)=\frac34\cdot\frac14=\frac3{16}$. לכן
$$P(X<\tfrac12\mid X>-\tfrac12)=\frac{1-\frac14e^{-1/2}-\frac3{16}}{1-\frac3{16}}=\frac{\frac{13}{16}-\frac14e^{-1/2}}{\frac{13}{16}}=1-\frac4{13}e^{-1/2}\approx0.81.$$""",
    5, contextId="c3", solutionSource="solved", official=False))

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

FIX_Q4 = (r"**הפתרון הרשמי עם תיקון:** בשאלה כפי שהודפסה היחידה $H$ פועלת בהסתברות $q$, אבל בפתרון הרשמי הוצב $P(H)=p$, "
          r"ולכן הפולינום הרשמי $p^3\left(2+4p-2p^2-13p^3+14p^4-4p^5\right)$ נכון רק במקרה $q=p$. "
          r"הפתרון שלהלן הוא הפתרון הרשמי עם $P(H)=q$, ולכן התשובה הסופית שונה מהתשובה הרשמית (ומתלכדת איתה כאשר $q=p$). התיקון נבדק (חישוב מדויק וסימולציה)." "\n")

questions.append(Q(
    4, "ב", "circuits",
    r"מהי ההסתברות שמעגל $Q_2$ פועל? (8 נק׳)",
    FIX_Q4 + r"""נפעל לפי נוסחת ההסתברות השלמה על $H$:
$$P(Q_2)=P(Q_2/H)\,P(H)+P(Q_2/\overline H)\,P(\overline H),\qquad P(H)=q,\ P(Q_2/\overline H)=P(Q_1).$$
כאשר $H$ פועלת, נקבל את המעגל $\widetilde Q_2$: היחידות $G,F$ במקביל, כך שהן מתנהגות כיחידה אחת $J$ עם $P(J)=p(2-p)$ בטור עם $C$:
$$P(Q_2/H)=p^2(1+3p-9p^3+8p^4-2p^5).$$
הצבה בנוסחת ההסתברות השלמה, עם $P(Q_1)$ מסעיף א, נותנת
$$P(Q_2)=q\,p^2\left(1+3p-9p^3+8p^4-2p^5\right)+(1-q)\,p^3\left(1+2p-4p^3+2p^4\right).$$
(עבור $q=p$ מתקבל $p^3\left(2+4p-2p^2-13p^3+14p^4-4p^5\right)$.)""",
    8, contextId="c4", solutionSource="solved", official=False))

questions.append(Q(
    4, "ג", "circuits",
    r"מהי ההסתברות שלפחות אחד המעגלים פעל? (6 נק׳)",
    FIX_Q4 + r"""נסמן $Q=Q_1\cup Q_2$ ונפעל לפי נוסחת ההסתברות השלמה על ארבעת המקרים של $G$ ו-$H$ (פועלת או לא):
$$P(Q)=P(Q/G\cap H)P(G\cap H)+P(Q/G\cap\overline H)P(G\cap\overline H)+P(Q/\overline G\cap H)P(\overline G\cap H)+P(Q/\overline G\cap\overline H)P(\overline G\cap\overline H),$$
כאשר $P(G\cap H)=pq$, $P(G\cap\overline H)=p(1-q)$, $P(\overline G\cap H)=(1-p)q$, והמחובר האחרון הוא $0$ (שני המעגלים דורשים אחת מהיחידות $G,H$). אחרי הצבה ופישוט מתקבל אותו ביטוי כמו $P(Q_2)$ (כל מסלול של $Q_1$ הוא גם מסלול של $Q_2$, ולכן $Q_1\subseteq Q_2$):
$$P(Q_1\cup Q_2)=q\,p^2\left(1+3p-9p^3+8p^4-2p^5\right)+(1-q)\,p^3\left(1+2p-4p^3+2p^4\right).$$""",
    6, contextId="c4", solutionSource="solved", official=False))

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

# ------------------------------------------------------------------ simulations (RAW_SCHEMA `sim`)
# Symbolic answers are simulated at a stated sample value (given in each `estimate`). check_sim_specs.py verifies
# exact == the deterministic value and the button's own first run against it.
def J(pAB, pAnB, pnAB, pnAnB):
    return [{"p": pAB, "A": 1, "B": 1}, {"p": pAnB, "A": 1, "B": 0}, {"p": pnAB, "A": 0, "B": 1}, {"p": pnAnB, "A": 0, "B": 0}]


def CD(joint, event, given=None):
    d = {"joint": joint, "event": event}
    if given:
        d["given"] = given
    return d


U02 = {"x": [0, 1], "y": [0, 2]}
U11 = {"x": [0, 1], "y": [0, 1]}
Q4_E1 = [("A", "s", "u1"), ("B", "s", "d1"), ("E", "u1", "d1"), ("C", "u1", "u2"), ("D", "d1", "d2"), ("F", "u2", "d2"), ("G", "u2", "t")]


def bridge(p, q=None):
    ed = [{"id": i, "from": a, "to": b, "p": p} for i, a, b in Q4_E1]
    if q is not None:
        ed.append({"id": "H", "from": "d2", "to": "t", "p": q})
    return {"edges": ed, "source": "s", "sink": "t"}


_Q1_WORKS = ("G == 1 and ((E == 1 and (A == 1 or B == 1) and (C == 1 or (D == 1 and F == 1))) "
             "or (E == 0 and ((A == 1 and C == 1) or (B == 1 and D == 1 and F == 1))))")
_p, _q = 0.5, 0.4
_P1 = _p ** 3 * (1 + 2 * _p - 4 * _p ** 3 + 2 * _p ** 4)
_P2 = _q * _p ** 2 * (1 + 3 * _p - 9 * _p ** 3 + 8 * _p ** 4 - 2 * _p ** 5) + (1 - _q) * _P1
_N = 10
_NN = 120   # C(10,3)

SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(S<2/3)", "exact": (1 + math.log(3)) / 3},
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(L<2)", "exact": 0.25},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(S<2/3 | L>2)", "exact": (1 + 4 * math.log(3)) / 9},
    (1, "ד"): {"kind": "area", "params": {"space": U02, "measure": "var", "expr": "2*(x+y)"}, "estimate": "Var[L]", "exact": 5 / 3},
    (1, "ה"): {"kind": "area", "params": {"space": U02, "measure": "var", "expr": "x*y"}, "estimate": "Var[S]", "exact": 7 / 36},
    # Q2: p=0.4, q=0.5, s=0.6  =>  P(A and B)=0.3
    (2, "א"): {"kind": "custom_discrete", "params": CD(J(0.3, 0.1, 0.2, 0.4), "A == 1", "B == 1"), "estimate": "P(A|B) ב-p=0.4,q=0.5,s=0.6", "exact": 0.6},
    (2, "ב"): {"kind": "custom_discrete", "params": CD(J(0.3, 0.1, 0.2, 0.4), "B == 1", "A == 0"), "estimate": "P(B|not A) ב-p=0.4,q=0.5,s=0.6", "exact": 1 / 3},
    (2, "ג"): {"kind": "custom_discrete", "params": CD(J(0.3, 0.1, 0.2, 0.4), "A == 1", "B == 0"), "estimate": "P(A|not B) ב-p=0.4,q=0.5,s=0.6", "exact": 0.2},
    (2, "ד"): {"kind": "custom_discrete", "params": CD(J(0.3, 0.1, 0.2, 0.4), "A == 0", "B == 0"), "estimate": "P(not A|not B) ב-p=0.4,q=0.5,s=0.6", "exact": 0.8},
    # independent: p=0.4, q=0.5, s=p+q-pq=0.7
    (2, "ה"): {"kind": "custom_discrete", "params": CD(J(0.2, 0.2, 0.3, 0.3), "A == 1 and B == 1"), "estimate": "P(A and B)=pq ב-p=0.4,q=0.5,s=0.7", "exact": 0.2},
    # disjoint: p=0.3, q=0.4, s=p+q=0.7
    (2, "ו"): {"kind": "custom_discrete", "params": CD(J(0.0, 0.3, 0.4, 0.3), "A == 1 or B == 1"), "estimate": "P(A or B)=s ב-p=0.3,q=0.4", "exact": 0.7},
    # Q3: a=3/2, b=1/4 (the exponential tail is cut at x=40, mass e^-40)
    (3, "א"): {"kind": "pdf", "params": {"pieces": [{"from": -1, "to": 0, "expr": "1.5*(1+x)"}, {"from": 0, "to": 40, "expr": "0.25*exp(-x)"}],
                                         "measure": "mean", "expr": "x"}, "estimate": "E[X]", "exact": 0.0},
    (3, "ב"): {"kind": "pdf", "params": {"pieces": [{"from": -1, "to": 0, "expr": "1.5*(1+x)"}, {"from": 0, "to": 40, "expr": "0.25*exp(-x)"}],
                                         "event": "x <= -0.5"}, "estimate": "F_X(-1/2)", "exact": 3 / 16},
    (3, "ג"): {"kind": "pdf", "params": {"pieces": [{"from": -1, "to": 0, "expr": "1.5*(1+x)"}, {"from": 0, "to": 40, "expr": "0.25*exp(-x)"}],
                                         "event": "x < 0.5", "given": "x > -0.5"}, "estimate": "P(X<1/2 | X>-1/2)", "exact": 1 - 4 / 13 * math.exp(-0.5)},
    # Q4 at p=0.5, q=0.4
    (4, "א"): {"kind": "circuit", "params": dict(bridge(_p), event="S"), "estimate": "P(Q1) ב-p=0.5", "exact": _P1},
    (4, "ב"): {"kind": "circuit", "params": dict(bridge(_p, _q), event="S"), "estimate": "P(Q2) ב-p=0.5,q=0.4", "exact": _P2},
    (4, "ג"): {"kind": "circuit", "params": dict(bridge(_p, _q), event="S"), "estimate": "P(Q1 u Q2)=P(Q2) ב-p=0.5,q=0.4", "exact": _P2},
    (4, "ד"): {"kind": "circuit", "params": dict(bridge(_p, _q), event="S", given=_Q1_WORKS), "estimate": "P(Q2|Q1) ב-p=0.5,q=0.4", "exact": 1.0},
    # Q5: n=3 numbers from {1..10}, without replacement
    (5, "א"): {"kind": "urn", "params": {"values": list(range(1, 11)), "draws": 3, "event": "min == 2"}, "estimate": "P(Xmin=2) ב-N=10,n=3", "exact": 28 / _NN},
    (5, "ב"): {"kind": "urn", "params": {"values": list(range(1, 11)), "draws": 3, "event": "max == 7"}, "estimate": "P(Xmax=7) ב-N=10,n=3", "exact": 15 / _NN},
    (5, "ג"): {"kind": "urn", "params": {"values": list(range(1, 11)), "draws": 3, "event": "min == 2 and max == 7"}, "estimate": "P(Xmin=2,Xmax=7) ב-N=10,n=3", "exact": 4 / _NN},
    (5, "ד"): {"kind": "urn", "params": {"values": list(range(1, 11)), "draws": 3, "measure": "mean", "expr": "min"}, "estimate": "E[Xmin] ב-N=10,n=3", "exact": 11 / 4},
    (5, "ה"): {"kind": "urn", "params": {"values": list(range(1, 11)), "draws": 3, "measure": "mean", "expr": "max"}, "estimate": "E[Xmax] ב-N=10,n=3", "exact": 33 / 4},
    # Q6 (L = 1)
    (6, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "F_Z(0.4)=P(Z<=0.4)", "exact": 0.4},
    (6, "ב"): {"kind": "area", "params": {"space": U11, "event": "min(x,y) > 0.2*max(x,y) and min(x,y) <= 0.5*max(x,y)"},
               "estimate": "P(0.2<Z<=0.5)", "exact": 0.3},
    (6, "ג"): {"kind": "area", "params": {"space": U11, "measure": "var", "expr": "y/x", "given": "y < x"}, "estimate": "Var[Z] = Var[Y/X | Y<X] (סימטריה)", "exact": 1 / 12},
}
for _q in questions:
    _s = SIMS.get((_q["num"], _q.get("part")))
    if _s is not None:
        _q["sim"] = _s

# ------------------------------------------------------------------ rubric / pitfalls / steps (ai-draft)
# Every expected value is re-derived independently (exact fractions / enumeration / sympy, and Monte Carlo where a kind
# applies) in tools/verify/25A-C/steps_check.py, which reads the generated raw JSON back.
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


OMEGA = r"מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X,Y)$, כאשר $X\sim U(0,1)$ ו-$Y\sim U(0,2)$?"
OMEGA_X = r"המלבן $(0,1)\times(0,2)$ הוא מרחב המדגם, ושטחו $1\cdot2=2$. ההסתברות היא שטח האירוע חלקי $2$, לא שטח האירוע לבדו."
_l3 = math.log(3)

ADD(1, "א",
    RB((r"גישה גאומטרית: הסתברות = שטח האירוע חלקי $|\Omega|=2$", 1), (r"נקודת החיתוך $x=\frac13$ של ההיפרבולה $y=\frac2{3x}$ עם $y=2$ ופיצול התחום", 1),
       (r"שטח האירוע $\frac23+\frac23\ln3$ (מלבן ועוד אינטגרל)", 2), (r"חלוקה ב-$2$: $\frac{1+\ln3}{3}$", 1)),
    [r"לשכוח לחלק ב-$|\Omega|=2$ ולדווח על השטח $\frac23(1+\ln3)\approx1.40$ כהסתברות (גדולה מ-$1$)", r"להתעלם מהחלק $0<x<\frac13$ שבו כל $0<y<2$ מתאים ולאנטגרל על כל $(0,1)$ בלבד"],
    [NU(OMEGA, 2, OMEGA_X),
     NU(r"מהו שטח האירוע $\{xy<\frac23\}$ בתוך המלבן? ($\ln3\approx1.0986$)", 2 / 3 * (1 + _l3),
        r"עבור $0<x<\frac13$ כל $0<y<2$ מתאים (שטח $\frac23$), ועבור $\frac13<x<1$ מתקבל $y<\frac2{3x}$ (שטח $\frac23\ln3$). סך הכול $\frac23(1+\ln3)\approx1.399$.", region=REGIONS[(1, "א")]),
     NU(r"מהי $P(S<\frac23)$?", (1 + _l3) / 3, r"$\frac{1.399}{2}=\frac{1+\ln3}{3}\approx0.6995$.")])

ADD(1, "ב",
    RB((r"תרגום $L<2$ ל-$X+Y<1$", 1), (r"האירוע הוא משולש ישר-זווית עם ניצבים $1$ ו-$1$ בתוך המלבן (כי $Y<1-X\le 1<2$)", 2), (r"שטח $\frac12$, חלוקה ב-$|\Omega|=2$ ותשובה $\frac14$", 2)),
    [r"לחלק ב-$1$ (שטח הריבוע) במקום ב-$2$ ולקבל $\frac12$", r"לחשוב שהמשולש מגיע עד $y=2$, אף שהישר $y=1-x$ יוצא מהמלבן ב-$y=1$"],
    [NU(OMEGA, 2, OMEGA_X),
     NU(r"מהו שטח האירוע $\{x+y<1\}$ בתוך המלבן?", Fr(1, 2), r"משולש ישר-זווית עם ניצבים $1$ ו-$1$: שטח $\frac12$. הוא מוכל כולו במלבן."),
     NU(r"מהי $P(L<2)$?", Fr(1, 4), r"$\frac{1/2}{2}=\frac14$.")])

ADD(1, "ג",
    RB((r"הגדרת ההסתברות המותנית $P(A\cap B)/P(B)$", 1), (r"$P(L>2)=1-\frac14=\frac34$", 1), (r"$P(S<\frac23\cap L>2)=P(S<\frac23)-\frac14$ כי המשולש $x+y<1$ מוכל ב-$\{S<\frac23\}$", 2), (r"היחס $\frac{1+4\ln3}{9}$", 1)),
    [r"לחשב $P(S<\frac23)/P(L>2)$ בלי לחתוך עם התנאי", r"לטעות בכיוון התנאי ולחשב $P(L>2\mid S<\frac23)$"],
    [NU(OMEGA, 2, OMEGA_X),
     NU(r"מהי הסתברות התנאי $P(L>2)$?", Fr(3, 4), r"המשלים $\{x+y<1\}$ הוא משולש ששטחו $\frac12$, כלומר הסתברות $\frac14$; לכן $P(L>2)=\frac34$."),
     NU(r"מהי $P(S<\frac23\cap L>2)$?", (1 + _l3) / 3 - 0.25,
        r"המשולש $x+y<1$ מוכל ב-$\{xy<\frac23\}$ (שם $xy\le\frac14$), לכן מחסרים: $\frac{1+\ln3}{3}-\frac14\approx0.4495$.", region=REGIONS[(1, "ג")]),
     NU(r"מהי $P(S<\frac23\mid L>2)$?", (1 + 4 * _l3) / 9, r"$\frac{0.4495}{0.75}=\frac{1+4\ln3}{9}\approx0.5994$.")])

ADD(1, "ד",
    RB((r"אי-תלות: שונות של סכום = סכום שונויות", 1), (r"$\mathbb{E}[L]=2(\frac12+1)=3$", 1), (r"$\operatorname{Var}[X]=\frac1{12}$, $\operatorname{Var}[Y]=\frac4{12}$", 1), (r"הוצאת הקבוע בריבוע: $\operatorname{Var}[L]=4\cdot\frac5{12}=\frac53$", 2)),
    [r"לכתוב $\operatorname{Var}[2(X+Y)]=2\operatorname{Var}[X+Y]$ (הקבוע עולה בריבוע)", r"להשתמש ב-$\operatorname{Var}[Y]=\frac1{12}$ במקום $\frac{2^2}{12}$"],
    [CH(r"איזה נימוק מצדיק לחשב את $\operatorname{Var}[L]$ מתוך $\operatorname{Var}[X]$ ו-$\operatorname{Var}[Y]$?",
        [r"$X,Y$ בלתי תלויים, ולכן $\operatorname{Var}[X+Y]=\operatorname{Var}[X]+\operatorname{Var}[Y]$, והקבוע $2$ מוצא בריבוע",
         r"תמיד $\operatorname{Var}[X+Y]=\operatorname{Var}[X]+\operatorname{Var}[Y]$, גם בלי אי-תלות",
         r"$\operatorname{Var}[2(X+Y)]=2\operatorname{Var}[X+Y]$, כי קבוע מוצא מהשונות בלי שינוי"], 0,
        r"האפשרות השנייה שגויה: בלי אי-תלות מתווסף $2\operatorname{Cov}[X,Y]$. השלישית שגויה: $\operatorname{Var}[cW]=c^2\operatorname{Var}[W]$, כלומר הקבוע מוצא בריבוע."),
     NU(r"מהי $\mathbb{E}[L]$?", 3, r"$2(\mathbb{E}[X]+\mathbb{E}[Y])=2(\frac12+1)=3$."),
     NU(r"מהי $\operatorname{Var}[L]$?", Fr(5, 3), r"$4(\frac1{12}+\frac{4}{12})=4\cdot\frac5{12}=\frac53$.")])

ADD(1, "ה",
    RB((r"אי-תלות: $\mathbb{E}[XY]=\mathbb{E}[X]\mathbb{E}[Y]$", 1), (r"$\mathbb{E}[S]=\frac12\cdot1=\frac12$", 1), (r"$\mathbb{E}[S^2]=\mathbb{E}[X^2]\mathbb{E}[Y^2]=\frac13\cdot\frac43$", 2), (r"$\operatorname{Var}[S]=\frac49-\frac14=\frac7{36}$", 1)),
    [r"לכתוב $\operatorname{Var}[XY]=\operatorname{Var}[X]\operatorname{Var}[Y]$ (נכון רק לשונות של סכום)", r"לחשב $\mathbb{E}[Y^2]=\frac13$ במקום $\frac{2^2}{3}=\frac43$"],
    [NU(r"מהי $\mathbb{E}[S]=\mathbb{E}[XY]$?", Fr(1, 2), r"אי-תלות: $\frac12\cdot1=\frac12$."),
     NU(r"מהו הרגע השני $\mathbb{E}[S^2]=\mathbb{E}[X^2]\,\mathbb{E}[Y^2]$? (זכרו ש-$Y\sim U(0,2)$)", Fr(4, 9), r"$\mathbb{E}[X^2]=\frac13$, $\mathbb{E}[Y^2]=\frac43$, המכפלה $\frac49$."),
     NU(r"מהי $\operatorname{Var}[S]$?", Fr(7, 36), r"$\frac49-\frac14=\frac{16-9}{36}=\frac7{36}$.")])

# Q2 (sample p = 0.4, q = 0.5, s = 0.6)
Q2S = r"נקבע לשם החישוב $p=0.4$, $q=0.5$, $s=0.6$. "
ADD(2, "א",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$P(A\cap B)=p+q-s$ מכלל החיבור", 2), (r"התשובה $\frac{p+q-s}{q}$", 1)),
    [r"לחלק ב-$P(A)$ במקום ב-$P(B)$ (המכנה הוא אירוע התנאי)", r"להניח $P(A\cap B)=pq$ בלי שנתון שהאירועים בלתי תלויים"],
    [CH(r"כיצד מחשבים את $P(A\mid B)$ מהנתונים $P(A),P(B),P(A\cup B)$?",
        [r"$\dfrac{P(A\cap B)}{P(B)}$ עם $P(A\cap B)=P(A)+P(B)-P(A\cup B)$",
         r"$\dfrac{P(A\cap B)}{P(A)}$ עם $P(A\cap B)=P(A)+P(B)-P(A\cup B)$",
         r"$\dfrac{P(A)P(B)}{P(B)}=P(A)$, כי האירועים בלתי תלויים"], 0,
        r"השנייה מחלקת באירוע הלא נכון (זה $P(B\mid A)$, ושווה $0.75\ne0.6$ כאן). השלישית מניחה אי-תלות שלא נתונה (ואז $s$ היה חייב להיות $0.7$, לא $0.6$)."),
     NU(Q2S + r"מהי $P(A\cap B)$?", Fr(3, 10), r"$p+q-s=0.4+0.5-0.6=0.3$."),
     NU(r"מהי הסתברות התנאי $P(B)$ (המכנה)?", Fr(1, 2), r"נתון: $P(B)=q=0.5$."),
     NU(r"מהי $P(A\mid B)$?", Fr(3, 5), r"$\frac{0.3}{0.5}=0.6$, כלומר $\frac{p+q-s}{q}$.")])

ADD(2, "ב",
    RB((r"הגדרת ההסתברות המותנית עם התנאי $\overline A$", 1), (r"$P(B\cap\overline A)=P(A\cup B)-P(A)=s-p$", 2), (r"$P(\overline A)=1-p$ והתשובה $\frac{s-p}{1-p}$", 1)),
    [r"לחשב $P(B)/P(\overline A)$ ולכלול את $A\cap B$ במונה", r"לחלק ב-$P(A)$ במקום ב-$P(\overline A)$"],
    [CH(r"איך מבטאים את $P(B\cap\overline A)$ באמצעות $p,q,s$?",
        [r"$P(A\cup B)-P(A)=s-p$: האיחוד פחות החלק של $A$", r"$P(B)-P(A)=q-p$", r"$P(B)\,P(\overline A)=q(1-p)$, כי $A,B$ בלתי תלויים"], 0,
        r"השנייה כוללת חיסור שאינו מתאים לשום מאורע (ובדוגמה: $q-p=0.1\ne0.2$). השלישית מניחה אי-תלות שלא נתונה."),
     NU(Q2S + r"מהי הסתברות התנאי $P(\overline A)$?", Fr(3, 5), r"$1-p=0.6$."),
     NU(r"מהי $P(B\cap\overline A)$?", Fr(1, 5), r"$s-p=0.2$."),
     NU(r"מהי $P(B\mid\overline A)$?", Fr(1, 3), r"$\frac{0.2}{0.6}=\frac13$, כלומר $\frac{s-p}{1-p}$.")])

ADD(2, "ג",
    RB((r"הגדרת ההסתברות המותנית עם התנאי $\overline B$", 1), (r"$P(A\cap\overline B)=s-q$", 2), (r"$P(\overline B)=1-q$ והתשובה $\frac{s-q}{1-q}$", 1)),
    [r"להשתמש ב-$P(A)-P(A\cap B)$ בלי לפשט, ולטעות באחד המחוברים", r"לחלק ב-$q$ במקום ב-$1-q$"],
    [CH(r"איזו הצגה של $P(A\cap\overline B)$ נכונה?",
        [r"$P(A\cup B)-P(B)=s-q$", r"$P(A)-P(B)=p-q$", r"$P(A)\,P(\overline B)=p(1-q)$ (אי-תלות)"], 0,
        r"השנייה אינה הסתברות של מאורע בדוגמה ($p-q=-0.1<0$). השלישית מניחה אי-תלות שלא נתונה."),
     NU(Q2S + r"מהי הסתברות התנאי $P(\overline B)$?", Fr(1, 2), r"$1-q=0.5$."),
     NU(r"מהי $P(A\cap\overline B)$?", Fr(1, 10), r"$s-q=0.1$."),
     NU(r"מהי $P(A\mid\overline B)$?", Fr(1, 5), r"$\frac{0.1}{0.5}=0.2$, כלומר $\frac{s-q}{1-q}$.")])

ADD(2, "ד",
    RB((r"$P(\overline A\cap\overline B)=1-P(A\cup B)$ (דה-מורגן)", 2), (r"$P(\overline B)=1-q$", 1), (r"התשובה $\frac{1-s}{1-q}$", 1)),
    [r"לכתוב $P(\overline A\cap\overline B)=1-p-q$ (שוכחים ש-$A,B$ יכולים לחפוף)", r"לחלק ב-$1-p$ (התנאי הוא $\overline B$)"],
    [CH(r"איזה ביטוי נכון עבור $P(\overline A\cap\overline B)$?",
        [r"$1-P(A\cup B)=1-s$, לפי דה-מורגן", r"$1-p-q$", r"$(1-p)(1-q)$ (אי-תלות)"], 0,
        r"השני נכון רק אם $A,B$ זרים ($0.1\ne0.4$ בדוגמה). השלישי מניח אי-תלות שלא נתונה."),
     NU(Q2S + r"מהי $P(\overline A\cap\overline B)$?", Fr(2, 5), r"$1-s=0.4$."),
     NU(r"מהי הסתברות התנאי $P(\overline B)$?", Fr(1, 2), r"$1-q=0.5$."),
     NU(r"מהי $P(\overline A\mid\overline B)$?", Fr(4, 5), r"$\frac{0.4}{0.5}=0.8$, כלומר $\frac{1-s}{1-q}$.")])

ADD(2, "ה",
    RB((r"תנאי אי-תלות $P(A\cap B)=P(A)P(B)$", 2), (r"$P(A\cap B)=p+q-s$", 1), (r"פתרון ל-$s=p+q-pq$", 1)),
    [r"לבלבל בין אי-תלות ($P(A\cap B)=pq$) לבין זרות ($P(A\cap B)=0$)"],
    [CH(r"איזה תנאי מבטא אי-תלות של $A$ ו-$B$?",
        [r"$P(A\cap B)=P(A)\,P(B)$", r"$P(A\cap B)=0$", r"$P(A\cup B)=P(A)+P(B)$"], 0,
        r"שני התנאים האחרים מתארים זרות ($P(A\cap B)=0$): כשההסתברויות חיוביות, $0\ne P(A)P(B)$, ולכן זרות סותרת אי-תלות."),
     NU(r"עבור $p=0.4$ ו-$q=0.5$: מהי $P(A\cap B)$ הנדרשת לאי-תלות?", Fr(1, 5), r"$pq=0.2$."),
     NU(r"עבור אותם $p,q$: איזה $s$ נותן אי-תלות? ($s=p+q-P(A\cap B)$)", Fr(7, 10), r"$0.4+0.5-0.2=0.7$, כלומר $s=p+q-pq$.")])

ADD(2, "ו",
    RB((r"זרות: $P(A\cap B)=0$", 2), (r"$P(A\cap B)=p+q-s$", 2), (r"$s=p+q$", 1)),
    [r"לכתוב $s=p+q-pq$ (זה אי-תלות)", r"לשכוח ש-$P(A\cap B)=p+q-s$"],
    [CH(r"מהו המאפיין של שני מאורעות זרים?",
        [r"$P(A\cap B)=0$", r"$P(A\cap B)=P(A)P(B)$", r"$P(A)+P(B)=1$"], 0,
        r"השני הוא אי-תלות; השלישי הוא משלימות ולא זרות (זרים אינם חייבים להשלים זה את זה)."),
     NU(r"עבור $p=0.3$ ו-$q=0.4$ זרים: מהו $s=P(A\cup B)$?", Fr(7, 10), r"$P(A\cap B)=0$, ולכן $s=p+q=0.7$.")])

# Q3 (a=3/2, b=1/4)
ADD(3, "א",
    RB((r"נרמול: $\frac a2+b=1$", 3), (r"תנאי התוחלת: $-\frac a6+b=0$", 3), (r"פתרון המערכת: $a=\frac32$, $b=\frac14$", 4)),
    [r"לדרוש רציפות ב-$x=0$ ($a=b$), אף שהצפיפות אינה חייבת להיות רציפה", r"לחשב $\int_{-1}^0x(1+x)\,dx$ בסימן שגוי"],
    [CH(r"אילו תנאים קובעים את שני הנעלמים $a,b$?",
        [r"נרמול $\int f=1$ ותנאי התוחלת $\mathbb{E}[X]=0$: שתי משוואות", r"נרמול בלבד: משוואה אחת מספיקה", r"רציפות הצפיפות ב-$x=0$ ($a=b$) ונרמול"], 0,
        r"נרמול בלבד נותן משוואה אחת לשני נעלמים. רציפות לא נתונה, ואם $a=b$ אז $a=b=\frac23$ והתוחלת $-\frac19+\frac23\ne0$."),
     NU(r"מהו $a$?", Fr(3, 2), r"מ-$b=\frac a6$ ו-$\frac a2+b=1$: $\frac{2a}3=1$, כלומר $a=\frac32$."),
     NU(r"מהו $b$?", Fr(1, 4), r"$b=\frac a6=\frac14$.")])

ADD(3, "ב",
    RB((r"פיצול לשני תחומים ואינטגרציה של $\frac32(1+x)$ ושל $\frac14e^{-x}$", 4), (r"הענף $\frac34(1+t)^2$ עד $F(0)=\frac34$", 3), (r"הענף $1-\frac14e^{-t}$ והמשכיות", 3)),
    [r"לשכוח את קבוע האינטגרציה בענף השני ולהתחיל מ-$0$ ב-$t=0$", r"לכתוב $1-\frac14e^{-t}$ כבר עבור $t<0$"],
    [NU(r"מהו $F_X(-\frac12)$?", Fr(3, 16), r"$\frac34(1+t)^2=\frac34\cdot\frac14=\frac3{16}$."),
     NU(r"מהו $F_X(0)$ (ערך החיבור בין שני הענפים)?", Fr(3, 4), r"$\frac34(1+0)^2=\frac34$; מצד שני $1-\frac14e^0=\frac34$."),
     NU(r"מהו $F_X(1)$?", 1 - math.exp(-1) / 4, r"$1-\frac14e^{-1}\approx0.9080$.")])

ADD(3, "ג",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$P(X>-\frac12)=1-F(-\frac12)=\frac{13}{16}$", 1), (r"$P(-\frac12<X<\frac12)=F(\frac12)-F(-\frac12)$", 2), (r"התשובה המתוקנת $1-\frac4{13}e^{-1/2}\approx0.81$", 1)),
    [r"להתייחס לתנאי כאילו הוא רק $X>0$", r"להסתמך על הערך הרשמי $1-\frac1e$ שאינו מתאים לנוסחה"],
    [NU(r"מהי הסתברות התנאי $P(X>-\frac12)$?", Fr(13, 16), r"$1-F_X(-\frac12)=1-\frac3{16}=\frac{13}{16}$."),
     NU(r"מהי $P(-\frac12<X<\frac12)$?", 13 / 16 - math.exp(-0.5) / 4, r"$F(\frac12)-F(-\frac12)=\left(1-\frac14e^{-1/2}\right)-\frac3{16}\approx0.6609$."),
     NU(r"מהי $P(X<\frac12\mid X>-\frac12)$?", 1 - 4 / 13 * math.exp(-0.5), r"$\frac{0.6609}{13/16}=1-\frac4{13}e^{-1/2}\approx0.8134$.")])

# Q4 circuits, p = 0.5 (and q = 0.4)
ADD(4, "א",
    RB((r"זיהוי הגשר $E$ ושימוש בנוסחת ההסתברות השלמה עליו", 3), (r"$P(Q_1/E)$ ו-$P(Q_1/\overline E)$ מהפישוטים הטוריים-מקביליים", 3), (r"הרכבה ופישוט ל-$p^3(1+2p-4p^3+2p^4)$", 2)),
    [r"לנסות לצמצם את המעגל לטור-מקביל בלי להתנות על $E$", r"להתייחס ל-$E$ כאל מקביל בין $A$ ל-$B$"],
    [CH(r"באיזו שיטה חוסכים חישוב במעגל $Q_1$ (עם יחידה $E$ המחברת בין שני הענפים)?",
        [r"נוסחת ההסתברות השלמה על $E$: עם $E$ ובלעדיה המעגל הופך לטורי-מקבילי", r"כפל כל ההסתברויות: $p^7$", r"$1-(1-p)^7$, כאילו כל היחידות במקביל"], 0,
        r"אין אפשרות לצמצם ישירות בגלל $E$. $p^7=0.0078$ ו-$1-(1-p)^7=0.992$ רחוקים משני הצדדים מהערך הנכון $0.203$."),
     NU(r"עבור $p=0.5$: מהו $P(Q_1/E)=(2p-p^2)(p+p^2-p^3)\,p$?", Fr(15, 64), r"$0.75\cdot0.625\cdot0.5=0.234375$."),
     NU(r"מהו $P(Q_1/\overline E)=(p^2+p^3-p^5)\,p$?", Fr(11, 64), r"$(0.25+0.125-0.03125)\cdot0.5=0.171875$."),
     NU(r"מהי $P(Q_1)$?", Fr(13, 64), r"$0.5\cdot0.234375+0.5\cdot0.171875=0.203125$.")])

ADD(4, "ב",
    RB((r"התניה על $H$", 2), (r"$P(Q_2/H)=p^2(1+3p-9p^3+8p^4-2p^5)$", 3), (r"$P(Q_2/\overline H)=P(Q_1)$", 1), (r"הרכבה עם $P(H)=q$ (התיקון)", 2)),
    [r"להציב $P(H)=p$ כמו בפתרון הרשמי כשהשאלה מגדירה $q$", r"לכתוב $P(Q_2)=q\,P(Q_1)$ (בטור)"],
    [CH(r"כיצד מחשבים את $P(Q_2)$ מתוך $P(Q_1)$ כאשר מוסיפים את היחידה $H$?",
        [r"התניה על $H$: $P(Q_2)=q\,P(Q_2/H)+(1-q)\,P(Q_1)$", r"$P(Q_2)=1-(1-P(Q_1))(1-q)$, כאילו $H$ במקביל לכל המעגל", r"$P(Q_2)=q\,P(Q_1)$, כאילו $H$ בטור"], 0,
        r"$H$ מחברת רק נקודות פנימיות ולא את כל המעגל, ולכן אינה במקביל או בטור למעגל כולו (הערכים המתקבלים, $0.522$ ו-$0.081$, שונים מהנכון $0.303$)."),
     NU(r"עבור $p=0.5$: מהי $P(Q_2/H)=p^2(1+3p-9p^3+8p^4-2p^5)$?", Fr(29, 64), r"$0.25\cdot1.8125=0.453125$."),
     NU(r"עבור $p=0.5$, $q=0.4$: מהי $P(Q_2)$?", 0.4 * 29 / 64 + 0.6 * 13 / 64, r"$0.4\cdot0.453125+0.6\cdot0.203125=0.303125$.")])

ADD(4, "ג",
    RB((r"זיהוי $Q_1\subseteq Q_2$ (הוספת $H$ רק מוסיפה מסלולים)", 3), (r"$P(Q_1\cup Q_2)=P(Q_2)$", 1), (r"הצבת הביטוי של $P(Q_2)$ מסעיף ב", 2)),
    [r"לחבר $P(Q_1)+P(Q_2)$ ולחרוג מהסתברות הקרובה ל-$1$", r"להניח ש-$Q_1,Q_2$ בלתי תלויים"],
    [CH(r"מה הקשר בין המאורעות $Q_1$ ו-$Q_2$, ומהו $P(Q_1\cup Q_2)$?",
        [r"$Q_1\subseteq Q_2$ (הוספת $H$ מוסיפה מסלולים בלבד), ולכן $P(Q_1\cup Q_2)=P(Q_2)$", r"בלתי תלויים: $P(Q_1\cup Q_2)=P(Q_1)+P(Q_2)-P(Q_1)P(Q_2)$", r"זרים: $P(Q_1\cup Q_2)=P(Q_1)+P(Q_2)$"], 0,
        r"הם תלויים ביותר (אותן יחידות), ואינם זרים (ביניהם חיתוך שלם, $Q_1$)."),
     NU(r"עבור $p=0.5$: מהי $P(Q_1\cap Q_2)$?", Fr(13, 64), r"$Q_1\subseteq Q_2$, ולכן החיתוך הוא $Q_1$: $0.203125$."),
     NU(r"עבור $p=0.5$, $q=0.4$: מהי $P(Q_1\cup Q_2)=P(Q_1)+P(Q_2)-P(Q_1\cap Q_2)$?", 0.4 * 29 / 64 + 0.6 * 13 / 64, r"$0.203125+0.303125-0.203125=0.303125$.")])

ADD(4, "ד",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$Q_1\subseteq Q_2$ ולכן החיתוך הוא $Q_1$", 1), (r"היחס $1$ ונימוק", 1)),
    [r"לענות $P(Q_2)$ או $q$ בלי לשים לב שהחיתוך הוא $Q_1$"],
    [NU(r"עבור $p=0.5$: מהי הסתברות התנאי $P(Q_1)$?", Fr(13, 64), r"$0.203125$ (סעיף א)."),
     NU(r"מהי $P(Q_1\cap Q_2)$?", Fr(13, 64), r"$Q_1\subseteq Q_2$, ולכן $P(Q_1\cap Q_2)=P(Q_1)$."),
     NU(r"מהי $P(Q_2\mid Q_1)$?", 1, r"היחס $\frac{P(Q_1)}{P(Q_1)}=1$: אם $Q_1$ פועל אז גם $Q_2$.")])

# Q5: n numbers from {1..N} without replacement; sample N = 10, n = 3
OM5 = r"עבור $N=10$ ו-$n=3$: כמה בחירות (תת-קבוצות) של $3$ מספרים אפשריות מתוך $\{1,\ldots,10\}$?"
ADD(5, "א",
    RB((r"מרחב המדגם: $\binom Nn$ תת-קבוצות שוות הסתברות", 2), (r"$X_{\min}=k$: $k$ נבחר והשאר $n-1$ מהמספרים הגדולים מ-$k$, כלומר $\binom{N-k}{n-1}$", 4), (r"תחום הערכים $1\le k\le N-n+1$", 2)),
    [r"לספור $\binom{N-k}{n}$ (מבלי לכלול את $k$ עצמו)", r"לטעות בתחום: $k$ עד $N$ (אבל צריכים עוד $n-1$ מספרים גדולים יותר)"],
    [CH(r"כיצד סופרים את התת-קבוצות שבהן המינימום הוא בדיוק $k$?",
        [r"בוחרים את $k$, ואת $n-1$ האחרים מבין $N-k$ המספרים הגדולים מ-$k$: $\binom{N-k}{n-1}$", r"בוחרים $n$ מספרים מבין $N-k$ הגדולים מ-$k$: $\binom{N-k}{n}$", r"בוחרים $n-1$ מבין $N-1$ המספרים השונים מ-$k$: $\binom{N-1}{n-1}$"], 0,
        r"השנייה אינה כוללת את $k$ (בדוגמה $\binom83=56\ne28$). השלישית מרשה מספרים קטנים מ-$k$, ואז $k$ אינו המינימום."),
     NU(OM5, 120, r"$\binom{10}{3}=120$."),
     NU(r"כמה בחירות נותנות $X_{\min}=2$?", 28, r"$\binom{10-2}{3-1}=\binom82=28$."),
     NU(r"מהי $P(X_{\min}=2)$?", Fr(7, 30), r"$\frac{28}{120}=\frac7{30}$.")])

ADD(5, "ב",
    RB((r"מרחב המדגם $\binom Nn$", 2), (r"$X_{\max}=\ell$: $\ell$ נבחר והשאר $n-1$ מבין $\ell-1$ הקטנים ממנו: $\binom{\ell-1}{n-1}$", 4), (r"תחום הערכים $n\le\ell\le N$", 2)),
    [r"לספור $\binom{\ell}{n-1}$ (כולל את $\ell$ בין הקטנים)", r"לשכוח שחייבים לפחות $n$ מספרים, לכן $\ell\ge n$"],
    [CH(r"כיצד סופרים את התת-קבוצות שבהן המקסימום הוא בדיוק $\ell$?",
        [r"בוחרים את $\ell$, ואת $n-1$ האחרים מבין $\ell-1$ הקטנים ממנו: $\binom{\ell-1}{n-1}$", r"בוחרים $n-1$ מבין $\ell$ המספרים $1,\ldots,\ell$: $\binom{\ell}{n-1}$", r"בוחרים $n$ מבין $\ell-1$ הקטנים מ-$\ell$: $\binom{\ell-1}{n}$"], 0,
        r"השנייה מרשה לבחור שוב את $\ell$ (ב-$\ell=7$: $\binom72=21\ne15$). השלישית אינה כוללת את $\ell$ בתת-הקבוצה."),
     NU(r"כמה בחירות נותנות $X_{\max}=7$ (עבור $N=10$, $n=3$)?", 15, r"$\binom{6}{2}=15$."),
     NU(r"מהי $P(X_{\max}=7)$?", Fr(1, 8), r"$\frac{15}{120}=\frac18$.")])

ADD(5, "ג",
    RB((r"בחירת המינימום והמקסימום (שני מספרים קבועים)", 3), (r"$n-2$ המספרים האחרים נבחרים מהמספרים שבין $k$ ל-$\ell$: $\binom{\ell-k-1}{n-2}$", 4), (r"חלוקה ב-$\binom Nn$ ותחום $k<\ell$", 2)),
    [r"לספור $\binom{\ell-k}{n-2}$ (כולל את הקצוות)", r"לשכוח את התנאי $k<\ell$"],
    [CH(r"כמה מספרים אפשר לבחור לשאר הקבוצה, כאשר המינימום הוא $k$ והמקסימום $\ell$?",
        [r"$\ell-k-1$ מספרים (המספרים שבין $k$ ל-$\ell$, לא כולל הקצוות)", r"$\ell-k$ מספרים", r"$N-2$ מספרים"], 0,
        r"השני סופר גם אחד הקצוות. השלישי מרשה מספרים מחוץ ל-$[k,\ell]$, ואז $k$ או $\ell$ אינו הקיצון."),
     NU(r"עבור $k=2$, $\ell=7$: כמה מספרים נמצאים בין $k$ ל-$\ell$?", 4, r"$7-2-1=4$ (המספרים $3,4,5,6$)."),
     NU(r"כמה בחירות נותנות $X_{\min}=2$ ו-$X_{\max}=7$ (עם $n=3$)?", 4, r"בוחרים $n-2=1$ מתוך $4$: $\binom41=4$."),
     NU(r"מהי $P(X_{\min}=2,\,X_{\max}=7)$?", Fr(1, 30), r"$\frac4{120}=\frac1{30}$.")])

ADD(5, "ד",
    RB((r"שימוש בהתפלגות $\binom{N-k}{n-1}/\binom Nn$ או בסימטריה", 2), (r"סכום ישיר או זהות הוקי-סטיק", 2), (r"התשובה $\frac{N+1}{n+1}$", 1)),
    [r"להניח $\mathbb{E}[X_{\min}]=\frac N2$ כמו ביחיד", r"לטעות בזהות הסיכום"],
    [CH(r"איזו תוצאה סבירה עבור $\mathbb{E}[X_{\min}]$ כשבוחרים $n=3$ מספרים מתוך $1,\ldots,10$?",
        [r"$\dfrac{N+1}{n+1}=2.75$: ככל שיותר מספרים נבחרים, המינימום קרוב יותר ל-$1$", r"$\dfrac N2=5$, כמו התוחלת של מספר בודד", r"$\dfrac{N}{n}=3.33$"], 0,
        r"המינימום של $3$ מספרים קטן בהכרח מהתוחלת של מספר בודד, לכן $5$ אינו יתכן. הערך $\frac Nn$ אינו מקיים את המקרה $n=1$ ($\mathbb{E}=\frac{N+1}2$), בעוד ש-$\frac{N+1}{n+1}$ כן."),
     NU(r"מהו $\mathbb{E}[X_{\min}]$ עבור $N=10$, $n=3$ (חישוב ישיר $\sum k\,P(X_{\min}=k)$)?", Fr(11, 4), r"$\frac{N+1}{n+1}=\frac{11}4=2.75$.")])

ADD(5, "ה",
    RB((r"סימטריה: $X_{\max}\overset d=N+1-X_{\min}$", 2), (r"$\mathbb{E}[X_{\max}]=N+1-\mathbb{E}[X_{\min}]$", 2), (r"התשובה $n\frac{N+1}{n+1}$", 1)),
    [r"לכתוב $\mathbb{E}[X_{\max}]=N-\mathbb{E}[X_{\min}]$ (חסר $1$)"],
    [CH(r"איזה קשר מצדיק לחשב את $\mathbb{E}[X_{\max}]$ מתוך $\mathbb{E}[X_{\min}]$?",
        [r"הפיכת המספרים $i\mapsto N+1-i$: $X_{\max}$ מתפלג כמו $N+1-X_{\min}$", r"$X_{\max}$ ו-$X_{\min}$ בלתי תלויים", r"$X_{\max}=X_{\min}+n$"], 0,
        r"הם תלויים (המקסימום תמיד גדול מהמינימום), והקשר $X_{\max}=X_{\min}+n$ שגוי (תלוי במספרים שנבחרו)."),
     NU(r"מהו $\mathbb{E}[X_{\max}]$ עבור $N=10$, $n=3$?", Fr(33, 4), r"$11-\frac{11}4=\frac{33}4=8.25$, כלומר $n\frac{N+1}{n+1}$.")])

# Q6 (L = 1)
ADD(6, "א",
    RB((r"מרחב המדגם והסימטריה בין $X$ ל-$Y$", 3), (r"פיצול לפי מי גדול ושטח המשולש $\frac t2$", 7), (r"הרכבה $F_Z(t)=t$ והמקרים $t<0$, $t\ge1$", 5)),
    [r"לשכוח לכפול ב-$2$ בגלל הסימטריה (ולקבל $\frac t2$)", r"לחשב את השטח של $\{Y\le tX\}$ בלי להגביל ל-$Y<X$"],
    [NU(r"נקבע $L=1$ (היחס אינו תלוי ב-$L$). מהו שטח מרחב המדגם $|\Omega|$?", 1, r"הריבוע $(0,1)^2$, שטחו $1$."),
     NU(r"מהו שטח האירוע $\{\min(x,y)\le0.4\max(x,y)\}$ (שני משולשים)?", Fr(2, 5), r"בכל חצי של הריבוע משולש ששטחו $\frac{0.4}2=0.2$, יחד $0.4$.", region=REGIONS[(6, "א")]),
     NU(r"מהי $F_Z(0.4)=P(Z\le0.4)$?", Fr(2, 5), r"$\frac{0.4}{1}=0.4=t$.")])

ADD(6, "ב",
    RB((r"גזירה: $f_Z=F_Z'$", 3), (r"$f_Z(t)=1$ על $[0,1]$ ו-$0$ אחרת", 2)),
    [r"לשכוח לאפס את הצפיפות מחוץ ל-$[0,1]$"],
    [NU(r"מהו $f_Z(0.5)$?", 1, r"$F_Z(t)=t$ על $[0,1]$, לכן הנגזרת היא $1$."),
     NU(r"מהי $P(0.2<Z\le0.5)=\int_{0.2}^{0.5}f_Z$?", Fr(3, 10), r"$0.5-0.2=0.3$ (התפלגות אחידה).")])

ADD(6, "ג",
    RB((r"$Z\sim U(0,1)$ ולכן $\mathbb{E}[Z]=\frac12$", 2), (r"$\mathbb{E}[Z^2]=\frac13$", 2), (r"$\operatorname{Var}[Z]=\frac13-\frac14=\frac1{12}$", 1)),
    [r"לשכוח להעלות את התוחלת בריבוע"],
    [NU(r"מהו $\mathbb{E}[Z^2]=\int_0^1z^2\,dz$?", Fr(1, 3), r"$\frac13$."),
     NU(r"מהי $\operatorname{Var}[Z]$?", Fr(1, 12), r"$\frac13-\left(\frac12\right)^2=\frac1{12}$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = "ai-draft"
        _q["stepsSource"] = "ai-draft"

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
