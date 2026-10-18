# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-B.json -- probability (course 20021), semester A 2025, moed B (12.03.2025).
6 questions, 30 items (Q1 6, Q2 6, Q3 4, Q4 4, Q5 4, Q6 6), 25 points each (Q5 d, Q6 e, f are 5-point bonus parts).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-B.py

Source: exam pp.1-3, handwritten official solutions on grid paper pp.4-23. Student/lecturer names are not copied.

Transcription notes
- Part keys: single letters, printed label is the first bold token. Q1 prints "א-1..א-3, ב, ג, ד" -> a..f.
  Q2 prints "א-1..א-4, ב, ג" -> a..f. Q6: a..f = א, ב, ג, ד, ה (bonus 1), ו (bonus 2).
- Q6 e, f: the two bonus parts (variances / correlation coefficient) have no worked solution in the solution file
  (it ends after part ד). Solved (solutionSource "solved", official:false): var[XL] = var[XR] = (N+1)(N-2)/18,
  cov = (N+1)(N-2)/36, rho = 1/2 for N >= 3 (undefined for N = 2). Verified exactly and by MC in tools/verify/25A-B/check.py.
- Q6: the printed text names the two people who sit down by their first names (they are lecturers); the names are
  replaced by "שני אנשים", the photo is not cropped and the sentence about the figure is reworded.
- Q1 d: E[sqrt Z] has infinite-variance Monte Carlo (E[Z] is infinite), see check.py (truncated MC + exact).
- Q1 area items carry `region` data (REGIONS below; RAW_SCHEMA `region`).
- Math never holds Hebrew.
"""
import json, math, pathlib
from fractions import Fraction as Fr

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-B.json"
CODE = "25A-B"
IMG = "images/exams/25A-B-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question,
         "points": points}
    if solution:
        q.update({"solution": solution, "solutionSource": "official-pdf", "official": True, "confidence": "high"})
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"יהיו $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,1)$ משתנים מקריים בלתי תלויים בעלי התפלגות אחידה. נגדיר משתנה מקרי חדש כיחס בין השניים:" "\n"
          r"$$Z=\frac XY.$$")
Q1_A = r"חשבו את ההסתברויות (3 נק׳ לכל תת סעיף):"
SOL1_0 = r"""נשתמש בגישה הקלאסית: מרחב המדגם הוא ריבוע היחידה $\Omega=(0,1)^2$ ו-$|\Omega|=1$."""

questions.append(Q(
    1, "א", "minmax_transform",
    Q1_A + "\n" + r"**(א-1):** $P(Z<1/3)$.",
    SOL1_0 + r"""
$$P(Z<\tfrac13)=P\left(\frac XY<\frac13\right)=P(Y>3X)=\frac{|\{Y>3X\}|}{|\Omega|}.$$
האזור $\{y>3x\}$ בתוך הריבוע הוא משולש בעל בסיס $\frac13$ וגובה $1$, ושטחו $\frac12\cdot\frac13\cdot1=\frac16$. לכן
$$P(Z<\tfrac13)=\frac16.$$""",
    3, contextId="c1"))

questions.append(Q(
    1, "ב", "minmax_transform",
    Q1_A + "\n" + r"**(א-2):** $P(Z<3)$.",
    SOL1_0 + r"""
$$P(Z<3)=P\left(\frac XY<3\right)=P\left(Y>\frac X3\right)=\frac{|\{Y>\frac X3\}|}{|\Omega|}.$$
משלים: האזור $\{y<\frac x3\}$ הוא משולש בעל בסיס $1$ וגובה $\frac13$, ושטחו $\frac12\cdot1\cdot\frac13=\frac16$. לכן
$$P(Z<3)=1-\frac16=\frac56.$$""",
    3, contextId="c1"))

questions.append(Q(
    1, "ג", "minmax_transform",
    Q1_A + "\n" + r"**(א-3):** $P(Z<1)$.",
    SOL1_0 + r"""
$$P(Z<1)=P\left(\frac XY<1\right)=P(Y>X)=\frac12$$
(חצי מהריבוע נמצא מעל האלכסון $y=x$).""",
    3, contextId="c1"))

questions.append(Q(
    1, "ד", "minmax_transform",
    r"מצאו את פונקציית ההתפלגות המצטברת $F_Z(t)$ של משתנה מקרי $Z$ ושרטטו אותה. (10 נק׳)",
    SOL1_0 + r"""
$$F_Z(t)=P(Z\le t)=\begin{cases}0,&t\le0,\\P\left(\frac XY<t\right),&t>0.\end{cases}$$
עבור $t>0$: $P\left(\frac XY<t\right)=P\left(Y>\frac Xt\right)$, ועל כן $|\Omega|=1$ והתשובה היא שטח האזור $\{y>\frac xt\}$ בתוך הריבוע.
- **מקרה 1, $0<t\le1$:** הישר $y=\frac xt$ עולה בשיפוע $\ge1$ ויוצא מהריבוע ב-$x=t$ (גובה $1$). האזור הוא משולש בעל בסיס $t$ וגובה $1$, ושטחו $\frac t2$.
- **מקרה 2, $t>1$:** הישר $y=\frac xt$ יוצא מהריבוע בנקודה $\left(1,\frac1t\right)$. השטח מתחת לישר הוא $\frac12\cdot1\cdot\frac1t=\frac1{2t}$, ולכן השטח מעליו הוא $1-\frac1{2t}$.

לכן
$$F_Z(t)=\begin{cases}0,&t\le0,\\\dfrac t2,&0<t\le1,\\1-\dfrac1{2t},&t>1.\end{cases}$$
הגרף: אפס עד $0$, ישר עם שיפוע $\frac12$ עד $(1,\frac12)$, ואחר כך עלייה מתמתנת שואפת ל-$1$.""",
    10, contextId="c1"))

questions.append(Q(
    1, "ה", "minmax_transform",
    r"מצאו את פונקציית הצפיפות $f_Z(t)$. (2 נק׳)",
    r"""$f_Z(t)=\frac{d}{dt}F_Z(t)$:
$$f_Z(t)=\begin{cases}0,&t\le0,\\\dfrac12,&0<t\le1,\\\dfrac1{2t^2},&t>1.\end{cases}$$""",
    2, contextId="c1"))

questions.append(Q(
    1, "ו", "continuous_rv",
    r"חשבו את התוחלת $\mathbb{E}\left[\sqrt Z\right]$. (4 נק׳)",
    r"""**דרך א׳ (בלי הצפיפות של $Z$):** $\sqrt Z=\frac{\sqrt X}{\sqrt Y}$ ו-$X,Y$ בלתי תלויים:
$$\mathbb{E}\left[\sqrt Z\right]=\mathbb{E}\left[\sqrt X\right]\cdot\mathbb{E}\left[\frac1{\sqrt Y}\right].$$
$$\mathbb{E}\left[\sqrt X\right]=\int_0^1\sqrt x\,dx=\frac23,\qquad\mathbb{E}\left[\frac1{\sqrt Y}\right]=\int_0^1\frac{dy}{\sqrt y}=2\sqrt y\Big|_0^1=2.$$
לכן $\mathbb{E}[\sqrt Z]=\frac43$.

**דרך ב׳ (דרך הצפיפות):**
$$\mathbb{E}\left[\sqrt Z\right]=\int_{-\infty}^{\infty}\sqrt t\,f_Z(t)\,dt=\int_0^1\sqrt t\cdot\frac12\,dt+\int_1^\infty\sqrt t\cdot\frac1{2t^2}\,dt=\frac13+\frac12\int_1^\infty\frac{dt}{t\sqrt t}=\frac13+1=\frac43.$$""",
    4, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_TXT = r"יהיו $A$ ו-$B$ מאורעות כלשהם בעלי הסתברות $P(A)=p$ ו-$P(B)=q$. בהינתן הסתברות מותנית $P(B/\overline A)=s$,"
Q2_A = r"חשבו את ההסתברויות הבאות (4 נק׳ לכל תת סעיף):"

questions.append(Q(
    2, "א", "conditional_bayes",
    Q2_A + "\n" + r"**(א-1):** $P(\overline{A}/B)$.",
    r"""לפי בייס, $P(B/\overline A)=\frac{P(\overline A/B)\,P(B)}{P(\overline A)}$, כלומר $s=\frac{P(\overline A/B)\,q}{1-p}$. לכן
$$P(\overline A/B)=\frac{s(1-p)}{q}.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ב", "conditional_bayes",
    Q2_A + "\n" + r"**(א-2):** $P(A/B)$.",
    r"""$$P(A/B)=1-P(\overline A/B)=1-\frac{s(1-p)}{q}.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    Q2_A + "\n" + r"**(א-3):** $P(A\cap B)$.",
    r"""$P(A\cap B)=P(A/B)\,P(B)$ ומכאן, לאחר הצבה,
$$P(A\cap B)=q-s(1-p).$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ד", "conditional_bayes",
    Q2_A + "\n" + r"**(א-4):** $P(A\cup B)$.",
    r"""$$P(A\cup B)=P(A)+P(B)-P(A\cap B)=p+q-\bigl[q-s(1-p)\bigr]=p+s(1-p).$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ה", "independence",
    r"עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו מאורעות **בלתי תלויים**? (4 נק׳)",
    r"""בלתי תלויים אם ורק אם $P(A\cap B)=P(A)P(B)$, כלומר
$$q-s(1-p)=pq\ \Longleftrightarrow\ q(1-p)=s(1-p).$$
(בהנחה ש-$p\ne1$) מתקבל
$$q=s.$$""",
    4, contextId="c2"))

questions.append(Q(
    2, "ו", "basics_events",
    r"עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו מאורעות **זרים**? (5 נק׳)",
    r"""זרים אם ורק אם $P(A\cap B)=0$, כלומר $q-s(1-p)=0$:
$$q=s(1-p).$$""",
    5, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות המשורטטת כאן. המקדמים $a$ ו-$b$ אינם ידועים." "\n"
          r"(בגרף: הצפיפות שווה לקבוע $a$ על $[-1,0)$; על $[0,2]$ היא משולש שקודקודו העליון בנקודה $(1,b)$, עולה ליניארית מ-$0$ ב-$x=0$ ויורדת ליניארית ל-$0$ ב-$x=2$; אפס בשאר המקומות.)")

questions.append(Q(
    3, "א", "continuous_rv",
    r"בהנחה כי $\mathbb{E}[X]=\mu$, מצאו את המקדמים ובטאו אותם באמצעות $\mu$. (10 נק׳)",
    r"""**נרמול:** שטח המלבן $[-1,0)\times[0,a]$ הוא $a$ ושטח המשולש (בסיס $2$, גובה $b$) הוא $b$, לכן
$$a+b=1.\qquad(*)$$
**תוחלת:** על $[0,1)$ הצפיפות היא $bx$ ועל $[1,2]$ היא $b(2-x)$:
$$\mu=\int_{-1}^0x\,a\,dx+\int_0^1x\cdot bx\,dx+\int_1^2x\cdot b(2-x)\,dx=-\frac a2+\frac b3+b\left(x^2\Big|_1^2-\frac{x^3}3\Big|_1^2\right)=-\frac a2+b.\qquad(**)$$
פתרון $(*)$ ו-$(**)$:
$$a=\frac23(1-\mu),\qquad b=\frac{1+2\mu}{3}.$$""",
    10, contextId="c3"))

questions.append(Q(
    3, "ב", "continuous_rv",
    r"מהו הערך הקטן והגדול ביותר של התוחלת $\mu$? נמקו! (4 נק׳)",
    r"""צפיפות חייבת להיות אי-שלילית, $a\ge0$ ו-$b\ge0$:
$$1-\mu\ge0\ \Rightarrow\ \mu\le1,\qquad1+2\mu\ge0\ \Rightarrow\ \mu\ge-\frac12.$$
לכן
$$-\frac12\le\mu\le1.$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ג", "continuous_rv",
    r"חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו אותה. (7 נק׳)",
    r"""$F_X(t)=\int_{-\infty}^tf_X(x)\,dx$, לכל $t\in\mathbb R$. נפרק לתחומים:
- $t<-1$: $F_X(t)=0$.
- $-1\le t<0$: $F_X(t)=a(t+1)=\frac23(1-\mu)(t+1)$.
- $0\le t<1$: $F_X(t)=a+\frac12\cdot t\cdot bt=\frac23(1-\mu)+\frac{1+2\mu}{6}t^2$.
- $1\le t<2$: $F_X(t)=1-\frac12(2-t)\cdot b(2-t)=1-\frac{1+2\mu}{6}(2-t)^2$.
- $t\ge2$: $F_X(t)=1$.

כלומר
$$F_X(t)=\begin{cases}0,&t<-1,\\\dfrac23(1-\mu)(t+1),&-1\le t<0,\\\dfrac23(1-\mu)+\dfrac{1+2\mu}6\,t^2,&0\le t<1,\\1-\dfrac{1+2\mu}6(2-t)^2,&1\le t<2,\\1,&t\ge2.\end{cases}$$
בגרף $F_X(0)=\frac23(1-\mu)$ ו-$F_X(1)=\frac{5-2\mu}{6}$.""",
    7, contextId="c3"))

questions.append(Q(
    3, "ד", "continuous_rv",
    r"חשבו את ההסתברות $P(X<1\,/\,X>0)$. (4 נק׳)",
    r"""$$P(X<1\mid X>0)=\frac{P(0<X<1)}{P(X>0)}=\frac{F_X(1)-F_X(0)}{1-F_X(0)}=\frac{\frac b2}{b}=\frac12.$$""",
    4, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"סטודנט של המכון הטכנולוגי חולון הרכיב מעגל $\boldsymbol{Q_1}$ מיחידות $A$, $B$, $C$, $D$ ו-$E$ הפועלות ללא תלות אחת בשנייה בהסתברויות הזהות $p$." "\n"
          r"לאחר מכן, הוא שינה את המעגל $\boldsymbol{Q_1}$ על ידי ״הוספת״ שתי יחידות נוספות $F$ ו-$G$, אשר פועלות בהסתברויות הזהות $q$ וזאת ללא תלות אחת בשנייה וללא תלות בכל יחידה אחרת. המעגל שנוצר הינו $\boldsymbol{Q_2}$.")

questions.append(Q(
    4, "א", "circuits",
    r"מהי ההסתברות שמעגל $Q_1$ פועל? (8 נק׳)",
    r"""נפעל לפי נוסחת ההסתברות השלמה על היחידה האמצעית $E$:
$$P(Q_1)=P(Q_1/E)P(E)+P(Q_1/\overline E)P(\overline E),\qquad P(E)=p.$$
- $E$ פועלת: ($A\,\|\,B$) בטור עם ($C\,\|\,D$): $P(Q_1/E)=(2p-p^2)^2$.
- $E$ לא פועלת: $(A,C)\ \|\ (B,D)$: $P(Q_1/\overline E)=2p^2-p^4$.

לכן
$$P(Q_1)=p(2p-p^2)^2+(1-p)(2p^2-p^4).$$""",
    8, contextId="c4"))

questions.append(Q(
    4, "ב", "circuits",
    r"מהי ההסתברות שמעגל $Q_2$ פועל? (8 נק׳)",
    r"""נפעל לפי נוסחת ההסתברות השלמה על $F$:
$$P(Q_2)=P(Q_2/F)P(F)+P(Q_2/\overline F)P(\overline F),\qquad P(F)=q.$$
כאשר $F$ פועלת, $Q_2$ הוא המעגל $Q_1$ בטור עם $G$: $P(Q_2/F)=q\,P(Q_1)$.
כאשר $F$ לא פועלת, $D$ מנותקת והמעגל הוא $\bigl(A\cup(B\cap E)\bigr)\cap C\cap G$:
$$P(Q_2/\overline F)=P(C)P(G)P\bigl(A\cup(B\cap E)\bigr)=p\cdot q\cdot(p+p^2-p^3)=p^2q(1+p-p^2).$$
לכן
$$P(Q_2)=q^2P(Q_1)+p^2q(1-q)(1+p-p^2)=q^2p^2(1+p-4p^2+2p^3)+qp^2(1+p-p^2).$$""",
    8, contextId="c4"))

questions.append(Q(
    4, "ג", "circuits",
    r"מהי ההסתברות שגם מעגל $Q_1$ וגם מעגל $Q_2$ פעלו? (6 נק׳)",
    r"""נסמן $\widetilde Q=Q_1\cap Q_2$ ונפעל לפי נוסחת ההסתברות השלמה על ארבעת המקרים של $E$ ו-$F$:
$$P(\widetilde Q)=P(\widetilde Q/E\cap F)\,pq+P(\widetilde Q/\overline E\cap\overline F)\,(1-p)(1-q)+P(\widetilde Q/E\cap\overline F)\,p(1-q)+P(\widetilde Q/\overline E\cap F)\,q(1-p).$$
- $E\cap F$: $(A\cup B)\cap(C\cup D)\cap G$, ולכן $(2p-p^2)^2q$.
- $\overline E\cap\overline F$: $\bigl((A\cap C)\cup(B\cap D)\bigr)\cap A\cap C\cap G=A\cap C\cap G$, ולכן $p^2q$.
- $E\cap\overline F$: $(A\cup B)\cap(C\cup D)\cap C\cap G=(A\cup B)\cap C\cap G$, ולכן $pq(2p-p^2)$.
- $\overline E\cap F$: $\bigl((A\cap C)\cup(B\cap D)\bigr)\cap G$, ולכן $q(2p^2-p^4)$.

הצבה:
$$P(\widetilde Q)=pq(2p-p^2)^2q+(1-p)(1-q)p^2q+p(1-q)pq(2p-p^2)+q(1-p)q(2p^2-p^4).$$
לאחר פישוט
$$P(\widetilde Q)=qp^2(1+p-p^2)+q^2p^2(1+p-4p^2+2p^3)=P(Q_2).$$
(כלומר $Q_2$ פועל רק אם גם $Q_1$ פועל.)""",
    6, contextId="c4"))

questions.append(Q(
    4, "ד", "circuits",
    r"**אם ידוע** כי מעגל $Q_1$ פעל, מהי ההסתברות שהמעגל $Q_2$ פעל גם כן? (3 נק׳)",
    r"""$$P(Q_2/Q_1)=\frac{P(\widetilde Q)}{P(Q_1)}=\frac{P(Q_2)}{P(Q_1)}.$$
כלומר, לפי סעיפים א׳, ב׳ ו-ג׳,
$$P(Q_2/Q_1)=\frac{q^2p^2(1+p-4p^2+2p^3)+qp^2(1+p-p^2)}{p(2p-p^2)^2+(1-p)(2p^2-p^4)}.$$""",
    3, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_TXT = (r"בכד נמצאים $D$ כדורים אדומים ו-$(N-D)$ כדורים שחורים.")

questions.append(Q(
    5, "א", "special_discrete",
    r"מוציאים מהכד כדור אחד באקראי. מה ההסתברות $P(R_1)$ שצבעו אדום? (3 נק׳)",
    r"""לפי הגישה הקלאסית
$$P(R_1)=\frac DN.$$""",
    3, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    r"מוציאים מהכד שני כדורים **ללא החזרה**. מהי ההסתברות $P(R_2)$ שהכדור **השני** יהיה אדום? שימו לב כי אין מידע על צבעו של הכדור הראשון. (7 נק׳)",
    r"""לפי נוסחת ההסתברות השלמה על צבע הכדור הראשון ($R_1$ אדום, $B_1$ שחור):
$$P(R_2)=P(R_2/R_1)P(R_1)+P(R_2/B_1)P(B_1)=\frac{D-1}{N-1}\cdot\frac DN+\frac D{N-1}\cdot\frac{N-D}N.$$
$$=\frac{D(D-1)+D(N-D)}{N(N-1)}=\frac{D(N-1)}{N(N-1)}=\frac DN.$$""",
    7, contextId="c5"))

questions.append(Q(
    5, "ג", "special_discrete",
    r"מוציאים מהכד $n$ כדורים **ללא החזרה**. בהנחה כי $D\ge n\ge2$, מהי ההסתברות $P(R_n)$ **שהכדור ה-$n$** יהיה אדום? שימו לב כי אין מידע על צבעים של $(n-1)$ הכדורים הקודמים שהוצאו מהכד. (15 נק׳)",
    r"""נגדיר $X$ = מספר הכדורים האדומים ב-$(n-1)$ הכדורים הקודמים. כי הדגימה היא ללא החזרה, $X\sim\mathrm{Hyp}(N,D,n-1)$.
לפי נוסחת ההסתברות השלמה:
$$P(R_n)=\sum_{k=0}^{n-1}P(R_n/X=k)\,P(X=k).$$
כאשר $X=k$, נשארו בכד $N-(n-1)$ כדורים, מהם $D-k$ אדומים, ולכן $P(R_n/X=k)=\frac{D-k}{N-n+1}$:
$$P(R_n)=\sum_{k=0}^{n-1}\frac{D-k}{N-n+1}P(X=k)=\frac1{N-n+1}\Bigl\{D\sum_{k=0}^{n-1}P(X=k)-\sum_{k=0}^{n-1}k\,P(X=k)\Bigr\}.$$
הסכום הראשון שווה $1$ והשני הוא $\mathbb{E}[X]=(n-1)\frac DN$. לכן
$$P(R_n)=\frac{D-(n-1)\frac DN}{N-n+1}=\frac DN.$$""",
    15, contextId="c5"))

questions.append(Q(
    5, "ד", "special_discrete",
    r"**סעיף בונוס:** **אם ידוע** כי הכדור ה-$n$ שהוצא היה אדום, מהי ההסתברות שהכדור הבא שיוצא מהכד יהיה אדום גם הוא? עליך להניח כי $1\le n\le(D-1)$. (5 נק׳ - הניקוד יינתן רק עבור פתרון מלא.)",
    r"""$$P(R_{n+1}/R_n)=\frac{P(R_n\cap R_{n+1})}{P(R_n)},\qquad P(R_n)=\frac DN.$$
נשתמש שוב ב-$X$ (מספר האדומים ב-$(n-1)$ הקודמים) ובנוסחת ההסתברות השלמה:
$$P(R_n\cap R_{n+1})=\sum_{k=0}^{n-1}P(R_n\cap R_{n+1}/X=k)P(X=k),\qquad P(R_n\cap R_{n+1}/X=k)=\frac{D-k}{N-n+1}\cdot\frac{D-k-1}{N-n}.$$
לכן
$$P(R_n\cap R_{n+1})=\frac1{(N-n)(N-n+1)}\sum_{k=0}^{n-1}(D-k)(D-1-k)P(X=k)=\frac1{(N-n)(N-n+1)}\Bigl\{D(D-1)-(2D-1)\mathbb{E}[X]+\mathbb{E}[X^2]\Bigr\}.$$
כאשר $\mathbb{E}[X]=(n-1)\frac DN$ ו-$\mathbb{E}[X^2]=\operatorname{Var}[X]+\bigl(\mathbb{E}[X]\bigr)^2$ עם שונות היפרגיאומטרית $\operatorname{Var}[X]=(n-1)\frac DN\cdot\frac{N-D}N\cdot\frac{N-n+1}{N-1}$, מתקבל לאחר הצבה
$$D(D-1)-(2D-1)\mathbb{E}[X]+\mathbb{E}[X^2]=\frac{D(D-1)(N-n)(N-n+1)}{N(N-1)},$$
ולכן
$$P(R_n\cap R_{n+1})=\frac DN\cdot\frac{D-1}{N-1}.$$
לבסוף
$$P(R_{n+1}/R_n)=\frac{D-1}{N-1}.$$""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_TXT = (r"שני אנשים מתיישבים **באקראי** על שני כיסאות מתוך שורת כיסאות הממוספרים ברצף בין $1$ ל-$N$ (אין לראות בכך טענה שאחד מהם תמיד מתיישב שמאלה מהשני!).")
Q6_HINT = r"""**הערה:** לידיעתך,
$$\sum_{k=1}^{N}k=\frac{N(N+1)}2,\qquad\sum_{k=1}^{N}k^2=\frac{N(N+1)(2N+1)}6,\qquad\sum_{k=1}^{N}k^3=\frac{N^2(N+1)^2}4.$$
(הסכום $\sum k^3$ נועד לסעיפי הבונוס.)"""

questions.append(Q(
    6, "א", "special_discrete",
    r"יהיו $X$ ו-$Y$ משתנים מקריים אשר מתארים את מספרי הכיסאות שהשניים תפסו. איך $X$ מפולג? איך $Y$ מפולג? **נמקו היטב!** (3 נק׳)",
    r"""כל אחד משני האנשים מתיישב באקראי באחד מ-$N$ הכיסאות, ובאופן שוויוני לכל כיסא; לכן
$$X\sim U_d(1,N),\qquad Y\sim U_d(1,N).$$
ההתפלגות המשותפת של $(X,Y)$ היא $P(X=x,Y=y)=\frac1{N(N-1)}$ לכל $x\ne y$ ו-$0$ על האלכסון $x=y$ (שני אנשים אינם יכולים לתפוס אותו כיסא). המשתנים אחידים אך **אינם** בלתי תלויים.
ההסתברות השולית של כל מספר כיסא היא $\frac{N-1}{N(N-1)}=\frac1N$.""",
    3, contextId="c6"))

questions.append(Q(
    6, "ב", "joint_discrete",
    r"יהיו $X_R=\max(X,Y)$ ו-$X_L=\min(X,Y)$ משתנים מקריים אשר מתארים את מספר הכיסא התפוס השמאלי ביותר ($X_L$) ואת מספר הכיסא הימני ביותר ($X_R$) שנתפס. בהנחה כי $N\ge2$, חשבו את פונקציית ההסתברות המשותפת של משתנה מקרי דו ממדי $(X_L,X_R)$. (10 נק׳)",
    r"""מכיוון ש-$X_L<X_R$ תמיד, ההסתברות שווה אפס עבור $j\ge k$. עבור $j<k$ שני המאורעות $\{X=j,Y=k\}$ ו-$\{X=k,Y=j\}$ מרכיבים יחד את $\{X_L=j,X_R=k\}$:
$$P(X_L=j,X_R=k)=P(X=j,Y=k)+P(X=k,Y=j)=\frac1{N(N-1)}+\frac1{N(N-1)}=\frac2{N(N-1)}.$$
לכן
$$P(X_L=j,X_R=k)=\begin{cases}0,&j\ge k,\\\dfrac2{N(N-1)},&j<k,\end{cases}\qquad j,k=1,2,\ldots,N.$$
בדיקה: מספר הזוגות $j<k$ הוא $\frac{N(N-1)}2$, ולכן סכום ההסתברויות הוא $\frac{N(N-1)}2\cdot\frac2{N(N-1)}=1$.""",
    10, contextId="c6"))

questions.append(Q(
    6, "ג", "joint_discrete",
    r"חשבו את פונקציית ההסתברות השוליות עבור משתנה מקרי $X_L$ ועבור משתנה מקרי $X_R$. (6 נק׳)",
    r"""נסכום את ההסתברות המשותפת לפי השורה והעמודה בטבלה.
- **עבור $X_L$:** $X_L=k$ אפשרי עבור $k=1,2,\ldots,N-1$. בשורה $k$ יש $N-k$ תאים בעלי הסתברות חיובית, ולכן
$$P(X_L=k)=\frac{2(N-k)}{N(N-1)},\qquad k=1,\ldots,N-1.$$
- **עבור $X_R$:** $X_R=k$ אפשרי עבור $k=2,3,\ldots,N$. בעמודה $k$ יש $k-1$ תאים בעלי הסתברות חיובית, ולכן
$$P(X_R=k)=\frac{2(k-1)}{N(N-1)},\qquad k=2,\ldots,N.$$""",
    6, contextId="c6"))

questions.append(Q(
    6, "ד", "discrete_rv",
    r"חשבו את התוחלות $\mathbb{E}[X_L]$ ו-$\mathbb{E}[X_R]$. הציבו $N=2$ והסבירו את התוצאה! (6 נק׳)" "\n" + Q6_HINT,
    r"""$$\mathbb{E}[X_L]=\sum_{k=1}^{N-1}k\cdot\frac{2(N-k)}{N(N-1)}=\frac2{N(N-1)}\Bigl\{N\sum_{k=1}^{N-1}k-\sum_{k=1}^{N-1}k^2\Bigr\}.$$
עם $\sum_{k=1}^{N-1}k=\frac{N(N-1)}2$ ו-$\sum_{k=1}^{N-1}k^2=\frac{N(N-1)(2N-1)}6$:
$$\mathbb{E}[X_L]=N-\frac{2N-1}3=\frac{N+1}3.$$
$$\mathbb{E}[X_R]=\sum_{k=2}^{N}k\cdot\frac{2(k-1)}{N(N-1)}=\frac2{N(N-1)}\Bigl\{\sum_{k=1}^{N}k^2-\sum_{k=1}^{N}k\Bigr\}=\frac2{N(N-1)}\cdot\frac{N(N+1)}6\{2N+1-3\}=\frac{2(N+1)}3.$$
**הצבת $N=2$:** $\mathbb{E}[X_L]=1$ ו-$\mathbb{E}[X_R]=2$.
הסבר: כאשר $N=2$ יש רק שני כיסאות והאנשים תופסים את שניהם, ולכן תמיד $X_L=1$ ו-$X_R=2$ (משתנים דטרמיניסטיים).""",
    6, contextId="c6"))

SOLVED = {"solutionSource": "solved", "official": False, "confidence": "high"}

questions.append(Q(
    6, "ה", "discrete_rv",
    r"**סעיף בונוס 1:** חשבו את השונויות $\operatorname{var}[X_L]$ ו-$\operatorname{var}[X_R]$. הציבו $N=2$ והסבירו את התוצאה! (5 נק׳ - הניקוד יינתן רק עבור פתרון מלא.)" "\n" + Q6_HINT,
    r"""**פתרון (אין פתרון רשמי לסעיפי הבונוס).**
נשתמש בפונקציות ההסתברות השוליות מסעיף ג ובתוחלות מסעיף ד, ו-$\operatorname{var}[X]=\mathbb{E}[X^2]-(\mathbb{E}[X])^2$.
**עבור $X_L$:**
$$\mathbb{E}[X_L^2]=\sum_{k=1}^{N-1}k^2\cdot\frac{2(N-k)}{N(N-1)}=\frac2{N(N-1)}\Bigl\{N\sum_{k=1}^{N-1}k^2-\sum_{k=1}^{N-1}k^3\Bigr\}.$$
עם $\sum_{k=1}^{N-1}k^2=\frac{(N-1)N(2N-1)}6$ ו-$\sum_{k=1}^{N-1}k^3=\frac{(N-1)^2N^2}4$:
$$N\cdot\frac{(N-1)N(2N-1)}6-\frac{(N-1)^2N^2}4=N^2(N-1)\Bigl\{\frac{2N-1}6-\frac{N-1}4\Bigr\}=\frac{N^2(N-1)(N+1)}{12},$$
ולכן $\mathbb{E}[X_L^2]=\frac{N(N+1)}6$ ו-
$$\operatorname{var}[X_L]=\frac{N(N+1)}6-\frac{(N+1)^2}9=\frac{(N+1)(3N-2N-2)}{18}=\frac{(N+1)(N-2)}{18}.$$
**עבור $X_R$:**
$$\mathbb{E}[X_R^2]=\sum_{k=2}^{N}k^2\cdot\frac{2(k-1)}{N(N-1)}=\frac2{N(N-1)}\Bigl\{\sum_{k=1}^{N}k^3-\sum_{k=1}^{N}k^2\Bigr\}=\frac2{N(N-1)}\cdot\frac{N(N+1)\{3N(N+1)-2(2N+1)\}}{12}.$$
מאחר ש-$3N^2-N-2=(3N+2)(N-1)$, מתקבל $\mathbb{E}[X_R^2]=\frac{(N+1)(3N+2)}6$, ולכן
$$\operatorname{var}[X_R]=\frac{(N+1)(3N+2)}6-\frac{4(N+1)^2}9=\frac{(N+1)(9N+6-8N-8)}{18}=\frac{(N+1)(N-2)}{18}.$$
כלומר $\operatorname{var}[X_L]=\operatorname{var}[X_R]=\frac{(N+1)(N-2)}{18}$ (גם בגלל הסימטריה: $N+1-X_R$ מתפלג כמו $X_L$).
**הצבת $N=2$:** $\operatorname{var}[X_L]=\operatorname{var}[X_R]=0$. הסבר: כאשר $N=2$ תמיד $X_L=1$ ו-$X_R=2$ (סעיף ד), ולמשתנה דטרמיניסטי אין פיזור.""",
    5, contextId="c6", **SOLVED))

questions.append(Q(
    6, "ו", "joint_discrete",
    r"**סעיף בונוס 2:** חשבו את מקדם המתאם $\rho[X_L,X_R]$. האם הנוסחה שפיתחת נכונה גם עבור $N=2$? נמקו! (5 נק׳ - הניקוד יינתן רק עבור פתרון מלא.)" "\n" + Q6_HINT,
    r"""**פתרון (אין פתרון רשמי לסעיפי הבונוס).**
$$\rho[X_L,X_R]=\frac{\operatorname{cov}[X_L,X_R]}{\sqrt{\operatorname{var}[X_L]\operatorname{var}[X_R]}},\qquad\operatorname{cov}[X_L,X_R]=\mathbb{E}[X_LX_R]-\mathbb{E}[X_L]\,\mathbb{E}[X_R].$$
לפי ההתפלגות המשותפת מסעיף ב,
$$\mathbb{E}[X_LX_R]=\sum_{j<k}jk\cdot\frac2{N(N-1)}=\frac2{N(N-1)}\cdot\frac12\Bigl\{\Bigl(\sum_{k=1}^Nk\Bigr)^2-\sum_{k=1}^Nk^2\Bigr\}=\frac1{N(N-1)}\Bigl\{\frac{N^2(N+1)^2}4-\frac{N(N+1)(2N+1)}6\Bigr\}.$$
כמו בסעיף הקודם $3N(N+1)-2(2N+1)=(3N+2)(N-1)$, ולכן $\mathbb{E}[X_LX_R]=\frac{(N+1)(3N+2)}{12}$. עם התוחלות מסעיף ד:
$$\operatorname{cov}[X_L,X_R]=\frac{(N+1)(3N+2)}{12}-\frac{N+1}3\cdot\frac{2(N+1)}3=\frac{(N+1)(9N+6-8N-8)}{36}=\frac{(N+1)(N-2)}{36}.$$
עם השונויות מסעיף הבונוס הקודם, עבור $N\ge3$:
$$\rho[X_L,X_R]=\frac{\frac{(N+1)(N-2)}{36}}{\frac{(N+1)(N-2)}{18}}=\frac12.$$
מקדם המתאם אינו תלוי ב-$N$.
**עבור $N=2$ הנוסחה לא נכונה:** שתי השונויות ושונות משותפת שוות $0$, והביטוי $\frac00$ אינו מוגדר. $X_L$ ו-$X_R$ הם קבועים, ולכן מקדם המתאם שלהם לא מוגדר (הצמצום ב-$(N-2)$ מותר רק כאשר $N\ne2$).""",
    5, contextId="c6", **SOLVED))

# ------------------------------------------------------------------ area regions (RAW_SCHEMA `region`)
REGIONS = {
    (1, 'א'): {"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 3, "b": -1, "c": 0, "op": "<"}], "exact": 0.16666666666666666, "caption": "X/Y<1/3, כלומר y>3x"},
    (1, 'ב'): {"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": -3, "c": 0, "op": "<"}], "exact": 0.8333333333333334, "caption": "X/Y<3, כלומר y>x/3"},
    (1, 'ג'): {"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": -1, "c": 0, "op": "<"}], "exact": 0.5, "caption": "X/Y<1, כלומר y>x"},
    (1, 'ד'): [{"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": -0.4, "c": 0, "op": "<"}], "exact": 0.2, "caption": "t=0.4: שטח t/2"}, {"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"a": 1, "b": -2, "c": 0, "op": "<"}], "exact": 0.75, "caption": "t=2: שטח 1-1/(2t)"}],
}
for _q in questions:
    _r = REGIONS.get((_q["num"], _q.get("part")))
    if _r is not None:
        _q["region"] = _r

# ------------------------------------------------------------------ simulations (RAW_SCHEMA `sim`)
# Symbolic answers are simulated at a stated sample value (given in each `estimate`). Not simulated: part ו (E[sqrt Z]
# has infinite variance, so the button's Monte Carlo cannot meet its own 4 SE test) and part ב of Q3 (a range of mu).
def J(pAB, pAnB, pnAB, pnAnB):
    return [{"p": pAB, "A": 1, "B": 1}, {"p": pAnB, "A": 1, "B": 0}, {"p": pnAB, "A": 0, "B": 1}, {"p": pnAnB, "A": 0, "B": 0}]


U11 = {"x": [0, 1], "y": [0, 1]}
_Q1_WORKS = ("(E == 1 and (A == 1 or B == 1) and (C == 1 or D == 1)) or (E == 0 and ((A == 1 and C == 1) or (B == 1 and D == 1)))")
Q4_E2 = [("A", "s", "u1"), ("B", "s", "d1"), ("E", "u1", "d1"), ("C", "u1", "u2"), ("D", "d1", "d2"), ("F", "u2", "d2"), ("G", "u2", "t")]


def net2(p, q):
    return {"edges": [{"id": i, "from": a, "to": b, "p": (q if i in "FG" else p)} for i, a, b in Q4_E2], "source": "s", "sink": "t"}


_p, _q = 0.5, 0.4
_P1 = _p * (2 * _p - _p ** 2) ** 2 + (1 - _p) * (2 * _p ** 2 - _p ** 4)
_P2 = _q ** 2 * _P1 + _p ** 2 * _q * (1 - _q) * (1 + _p - _p ** 2)
# Q2: p=0.4, q=0.5, s=P(B|not A)=0.6  =>  P(B and not A)=0.36, P(A and B)=0.14
_J2 = J(0.14, 0.26, 0.36, 0.24)
_PDF3 = {"pieces": [{"from": -1, "to": 0, "expr": "0.5"}, {"from": 0, "to": 1, "expr": "0.5*x"}, {"from": 1, "to": 2, "expr": "0.5*(2-x)"}]}
_URN = {"counts": {"red": 5, "black": 7}}
_CH = {"values": list(range(1, 9)), "draws": 2}   # two people on chairs 1..8

SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X/Y<1/3)", "exact": 1 / 6},
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X/Y<3)", "exact": 5 / 6},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X/Y<1)", "exact": 0.5},
    (1, "ד"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "F_Z(0.4)=P(Z<=0.4)", "exact": 0.2},
    (1, "ה"): {"kind": "area", "params": {"space": U11, "event": "x > 0.5*y and x < 2*y"}, "estimate": "P(1/2<Z<2)=F_Z(2)-F_Z(1/2)", "exact": 0.5},
    (2, "א"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 0", "given": "B == 1"}, "estimate": "P(not A|B) ב-p=0.4,q=0.5,s=0.6", "exact": 0.72},
    (2, "ב"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 1", "given": "B == 1"}, "estimate": "P(A|B) ב-p=0.4,q=0.5,s=0.6", "exact": 0.28},
    (2, "ג"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 1 and B == 1"}, "estimate": "P(A and B) ב-p=0.4,q=0.5,s=0.6", "exact": 0.14},
    (2, "ד"): {"kind": "custom_discrete", "params": {"joint": _J2, "event": "A == 1 or B == 1"}, "estimate": "P(A or B) ב-p=0.4,q=0.5,s=0.6", "exact": 0.76},
    # independent: q = s = 0.5, p = 0.4 => P(A and B) = pq = 0.2
    (2, "ה"): {"kind": "custom_discrete", "params": {"joint": J(0.2, 0.2, 0.3, 0.3), "event": "A == 1 and B == 1"}, "estimate": "P(A and B)=pq ב-p=0.4,q=s=0.5", "exact": 0.2},
    # disjoint: p=0.4, s=0.5 => q = s(1-p) = 0.3, P(A or B) = p+q = 0.7
    (2, "ו"): {"kind": "custom_discrete", "params": {"joint": J(0.0, 0.4, 0.3, 0.3), "event": "A == 1 or B == 1"}, "estimate": "P(A or B)=p+q ב-p=0.4,s=0.5 (q=0.3)", "exact": 0.7},
    # Q3 at mu = 0.25: a = 1/2, b = 1/2
    (3, "א"): {"kind": "pdf", "params": dict(_PDF3, measure="mean", expr="x"), "estimate": "E[X]=mu ב-mu=0.25", "exact": 0.25},
    (3, "ג"): {"kind": "pdf", "params": dict(_PDF3, event="x <= 0.5"), "estimate": "F_X(0.5) ב-mu=0.25", "exact": 0.5625},
    (3, "ד"): {"kind": "pdf", "params": dict(_PDF3, event="x < 1", given="x > 0"), "estimate": "P(X<1 | X>0)", "exact": 0.5},
    # Q4 at p=0.5, q=0.4
    (4, "א"): {"kind": "circuit", "params": {"edges": [{"id": i, "from": a, "to": b, "p": _p} for i, a, b in
                                                        [("A", "s", "u1"), ("B", "s", "d1"), ("E", "u1", "d1"), ("C", "u1", "t"), ("D", "d1", "t")]],
                                             "source": "s", "sink": "t", "event": "S"}, "estimate": "P(Q1) ב-p=0.5", "exact": _P1},
    (4, "ב"): {"kind": "circuit", "params": dict(net2(_p, _q), event="S"), "estimate": "P(Q2) ב-p=0.5,q=0.4", "exact": _P2},
    (4, "ג"): {"kind": "circuit", "params": dict(net2(_p, _q), event="S == 1 and (" + _Q1_WORKS + ")"), "estimate": "P(Q1 and Q2) ב-p=0.5,q=0.4", "exact": _P2},
    (4, "ד"): {"kind": "circuit", "params": dict(net2(_p, _q), event="S", given=_Q1_WORKS), "estimate": "P(Q2|Q1) ב-p=0.5,q=0.4", "exact": _P2 / _P1},
    # Q5: D=5 red of N=12
    (5, "א"): {"kind": "urn", "params": dict(_URN, draws=1, event="red_1 == 1"), "estimate": "P(R1) ב-D=5,N=12", "exact": 5 / 12},
    (5, "ב"): {"kind": "urn", "params": dict(_URN, draws=2, event="red_2 == 1"), "estimate": "P(R2) ב-D=5,N=12", "exact": 5 / 12},
    (5, "ג"): {"kind": "urn", "params": dict(_URN, draws=4, event="red_4 == 1"), "estimate": "P(R4) ב-D=5,N=12", "exact": 5 / 12},
    (5, "ד"): {"kind": "urn", "params": dict(_URN, draws=4, event="red_4 == 1", given="red_3 == 1"), "estimate": "P(R4|R3) ב-D=5,N=12", "exact": 4 / 11},
    # Q6: N=8 chairs
    (6, "א"): {"kind": "urn", "params": dict(_CH, event="v1 <= 3"), "estimate": "P(X<=3) ב-N=8", "exact": 3 / 8},
    (6, "ב"): {"kind": "urn", "params": dict(_CH, event="min == 3 and max == 6"), "estimate": "P(XL=3,XR=6) ב-N=8", "exact": 2 / 56},
    (6, "ג"): {"kind": "urn", "params": dict(_CH, event="min == 3"), "estimate": "P(XL=3) ב-N=8", "exact": 10 / 56},
    (6, "ד"): {"kind": "urn", "params": dict(_CH, measure="mean", expr="min"), "estimate": "E[XL] ב-N=8", "exact": 3.0},
    (6, "ה"): {"kind": "urn", "params": dict(_CH, measure="var", expr="min"), "estimate": "var[XL] ב-N=8", "exact": 3.0},
    (6, "ו"): {"kind": "urn", "params": dict(_CH, measure="cov", expr=["min", "max"]), "estimate": "cov[XL,XR] ב-N=8 (rho=cov/var=1/2)", "exact": 1.5},
}
for _q in questions:
    _s = SIMS.get((_q["num"], _q.get("part")))
    if _s is not None:
        _q["sim"] = _s

# ------------------------------------------------------------------ rubric / pitfalls / steps (ai-draft)
# Every expected value is re-derived independently (exact fractions / enumeration / sympy, and Monte Carlo where a kind
# applies) in tools/verify/25A-B/steps_check.py, which reads the generated raw JSON back.
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


OMEGA = r"מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X,Y)$, כאשר $X,Y\sim U(0,1)$ בלתי תלויים?"
OMEGA_X = r"ריבוע היחידה $(0,1)^2$ הוא מרחב המדגם, ושטחו $1$, לכן ההסתברות שווה לשטח האירוע."

ADD(1, "א",
    RB((r"תרגום $\frac XY<\frac13$ ל-$y>3x$", 1), (r"האזור הוא משולש עם בסיס $\frac13$ וגובה $1$", 1), (r"שטח $\frac16$ והסתברות $\frac16$", 1)),
    [r"להפוך את האי-שוויון ולחשב את השטח של $y<3x$ (שהוא $\frac56$)", r"לשכוח שהישר $y=3x$ יוצא מהריבוע ב-$x=\frac13$"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"באיזה ערך של $x$ הישר $y=3x$ יוצא מהריבוע (מגיע ל-$y=1$)?", Fr(1, 3), r"$3x=1$, כלומר $x=\frac13$."),
     NU(r"מהו שטח המשולש $\{y>3x\}$ בתוך הריבוע, כלומר $P(Z<\frac13)$?", Fr(1, 6), r"$\frac12\cdot\frac13\cdot1=\frac16$.", region=REGIONS[(1, "א")])])

ADD(1, "ב",
    RB((r"תרגום $\frac XY<3$ ל-$y>\frac x3$", 1), (r"המשלים $\{y<\frac x3\}$ הוא משולש עם בסיס $1$ וגובה $\frac13$", 1), (r"התשובה $1-\frac16=\frac56$", 1)),
    [r"לחשב את שטח המשולש ולהשאיר אותו כתשובה ($\frac16$) במקום המשלים"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח המשולש המשלים $\{y<\frac x3\}$?", Fr(1, 6), r"בסיס $1$, גובה $\frac13$: $\frac12\cdot1\cdot\frac13=\frac16$."),
     NU(r"מהי $P(Z<3)$?", Fr(5, 6), r"$1-\frac16=\frac56$.", region=REGIONS[(1, "ב")])])

ADD(1, "ג",
    RB((r"תרגום $\frac XY<1$ ל-$y>x$", 1), (r"חצי הריבוע מעל האלכסון", 1), (r"התשובה $\frac12$", 1)),
    [r"לחשוב ש-$P(Z<1)$ גדולה מ-$\frac12$ כי הטווח של $Z$ אינסופי (אבל הסימטריה $X\leftrightarrow Y$ נותנת $\frac12$)"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח האזור $\{y>x\}$ בתוך הריבוע?", Fr(1, 2), r"המשולש שמעל האלכסון: חצי מהריבוע. לכן $P(Z<1)=\frac12$.", region=REGIONS[(1, "ג")])])

ADD(1, "ד",
    RB((r"$F_Z(t)=0$ עבור $t\le0$", 1), (r"מקרה $0<t\le1$: משולש בבסיס $t$ ובגובה $1$, שטח $\frac t2$", 3), (r"מקרה $t>1$: משלים של משולש, $1-\frac1{2t}$", 4), (r"הרכבה ובדיקת רציפות ב-$t=1$", 2)),
    [r"להשתמש בנוסחה $\frac t2$ גם עבור $t>1$ (אז מתקבלת הסתברות גדולה מ-$\frac12$ ללא סיבה)", r"לשכוח שעבור $t>1$ הישר יוצא מהריבוע דרך הצלע הימנית ולא דרך הצלע העליונה"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו $F_Z(0.4)$? (המקרה $0<t\le1$)", Fr(1, 5), r"משולש בבסיס $0.4$ ובגובה $1$: שטח $\frac{0.4}2=0.2$, כלומר $\frac t2$.", region=REGIONS[(1, "ד")][0]),
     NU(r"מהו $F_Z(2)$? (המקרה $t>1$)", Fr(3, 4), r"$1-\frac1{2t}=1-\frac14=0.75$.", region=REGIONS[(1, "ד")][1]),
     NU(r"מהו $F_Z(1)$ (נקודת המעבר בין שני המקרים)?", Fr(1, 2), r"$\frac12$ משני הצדדים: $\frac t2$ ו-$1-\frac1{2t}$ שווים ב-$t=1$.")])

ADD(1, "ה",
    RB((r"גזירת $F_Z$ בכל תחום", 1), (r"$f_Z(t)=\frac12$ עבור $0<t\le1$ ו-$\frac1{2t^2}$ עבור $t>1$", 1)),
    [r"לשכוח לאפס את הצפיפות עבור $t\le0$"],
    [NU(r"מהו $f_Z(0.5)$?", Fr(1, 2), r"$F_Z(t)=\frac t2$ שם, והנגזרת $\frac12$."),
     NU(r"מהו $f_Z(2)$?", Fr(1, 8), r"$F_Z(t)=1-\frac1{2t}$, הנגזרת $\frac1{2t^2}=\frac18$."),
     NU(r"מהו $\int_1^{\infty}f_Z(t)\,dt$ (בדיקת נרמול: הוא צריך להשלים את $\int_0^1f_Z=\frac12$ ל-$1$)?", Fr(1, 2), r"$\int_1^\infty\frac{dt}{2t^2}=\frac12$.")])

ADD(1, "ו",
    RB((r"אי-תלות: $\mathbb{E}[\sqrt X\cdot Y^{-1/2}]=\mathbb{E}[\sqrt X]\,\mathbb{E}[Y^{-1/2}]$", 1), (r"$\mathbb{E}[\sqrt X]=\frac23$", 1), (r"$\mathbb{E}[Y^{-1/2}]=2$", 1), (r"התוצאה $\frac43$", 1)),
    [r"לכתוב $\mathbb{E}[\sqrt Z]=\sqrt{\mathbb{E}[Z]}$ (ו-$\mathbb{E}[Z]=\infty$)", r"לכתוב $\mathbb{E}\!\left[\frac1{\sqrt Y}\right]=\frac1{\mathbb{E}[\sqrt Y]}$"],
    [CH(r"כיצד אפשר לחשב את $\mathbb{E}[\sqrt Z]$ בלי הצפיפות של $Z$?",
        [r"$\sqrt Z=\sqrt X\cdot Y^{-1/2}$ ו-$X,Y$ בלתי תלויים, ולכן התוחלת של המכפלה היא מכפלת התוחלות", r"$\mathbb{E}[\sqrt Z]=\sqrt{\mathbb{E}[Z]}$", r"$\mathbb{E}[\sqrt Z]=\dfrac{\mathbb{E}[\sqrt X]}{\mathbb{E}[\sqrt Y]}$"], 0,
        r"השנייה שגויה: $\mathbb{E}[Z]=\mathbb{E}[X]\,\mathbb{E}[1/Y]=\infty$, והשורש אינו מתחלף עם התוחלת. השלישית שגויה: תוחלת של מנה אינה מנת התוחלות ($\mathbb{E}[1/\sqrt Y]=2$ ולא $\frac32$)."),
     NU(r"מהו $\mathbb{E}[\sqrt X]$?", Fr(2, 3), r"$\int_0^1\sqrt x\,dx=\frac23$."),
     NU(r"מהו $\mathbb{E}\!\left[\frac1{\sqrt Y}\right]$?", 2, r"$\int_0^1y^{-1/2}\,dy=2$."),
     NU(r"מהו $\mathbb{E}[\sqrt Z]$?", Fr(4, 3), r"$\frac23\cdot2=\frac43$.")])

# Q2: sample p = 0.4, q = 0.5, s = P(B|not A) = 0.6
Q2S = r"נקבע $p=0.4$, $q=0.5$, $s=0.6$. "
ADD(2, "א",
    RB((r"הכלל של בייס עם התנאי המתאים", 1), (r"$P(B\cap\overline A)=s(1-p)$", 2), (r"הצבה והתשובה $\frac{s(1-p)}{q}$", 1)),
    [r"לבלבל בין $P(B\mid\overline A)=s$ לבין $P(\overline A\mid B)$", r"להפוך את בייס ולכתוב $\frac{sq}{1-p}$"],
    [CH(r"נתון $P(B\mid\overline A)=s$. איך מחשבים את $P(\overline A\mid B)$?",
        [r"בייס: $P(\overline A\mid B)=\dfrac{P(B\mid\overline A)\,P(\overline A)}{P(B)}$", r"$P(\overline A\mid B)=P(B\mid\overline A)=s$", r"$P(\overline A\mid B)=\dfrac{P(B\mid\overline A)\,P(B)}{P(\overline A)}$"], 0,
        r"השנייה מניחה שהתנאי וההסתברות מתחלפים (זה נכון רק כש-$P(\overline A)=P(B)$). בשלישית הגורמים $P(\overline A)$ ו-$P(B)$ הפוכים. בדוגמה: $0.6$ ו-$0.5$ במקום $0.72$."),
     NU(Q2S + r"מהי $P(B\cap\overline A)=s(1-p)$?", Fr(9, 25), r"$0.6\cdot0.6=0.36$."),
     NU(r"מהי הסתברות התנאי $P(B)$?", Fr(1, 2), r"נתון: $q=0.5$."),
     NU(r"מהי $P(\overline A\mid B)$?", Fr(18, 25), r"$\frac{0.36}{0.5}=0.72$, כלומר $\frac{s(1-p)}q$.")])

ADD(2, "ב",
    RB((r"המשלים בתוך ההתניה: $P(A\mid B)+P(\overline A\mid B)=1$", 2), (r"הצבת סעיף א", 1), (r"התשובה $1-\frac{s(1-p)}q$", 1)),
    [r"להחסיר מ-$1$ את $P(\overline A)$ הלא מותנית", r"לכתוב $1-s$"],
    [CH(r"איך מחשבים את $P(A\mid B)$ מתוך $P(\overline A\mid B)$?",
        [r"$P(A\mid B)=1-P(\overline A\mid B)$: מכלול הסתברויות מותנות באותו תנאי", r"$P(A\mid B)=1-P(\overline A)$", r"$P(A\mid B)=1-P(B\mid\overline A)=1-s$"], 0,
        r"השנייה מערבבת הסתברות לא מותנית ($1-P(\overline A)=0.4$) והשלישית מערבבת את כיוון ההתניה ($1-s=0.4$), שתיהן במקום $0.28$."),
     NU(Q2S + r"מהי $P(\overline A\mid B)$ (סעיף א)?", Fr(18, 25), r"$0.72$."),
     NU(r"מהי $P(A\mid B)$?", Fr(7, 25), r"$1-0.72=0.28$.")])

ADD(2, "ג",
    RB((r"פירוק $B$ ל-$A\cap B$ ו-$\overline A\cap B$", 2), (r"$P(B\cap\overline A)=s(1-p)$", 1), (r"התשובה $q-s(1-p)$", 1)),
    [r"להניח אי-תלות ולכתוב $pq$", r"לכתוב $P(A\cap B)=P(A\mid B)$ בלי להכפיל ב-$P(B)$"],
    [CH(r"כיצד מחשבים את $P(A\cap B)$ מהנתונים?",
        [r"$P(A\cap B)=P(B)-P(B\cap\overline A)=q-s(1-p)$", r"$P(A\cap B)=P(A)P(B)=pq$", r"$P(A\cap B)=s\cdot q$"], 0,
        r"השנייה מניחה אי-תלות שלא נתונה ($0.2$ במקום $0.14$). השלישית מכפילה הסתברות מותנית בהסתברות לא קשורה ($0.3$)."),
     NU(Q2S + r"מהי $P(B\cap\overline A)$?", Fr(9, 25), r"$s(1-p)=0.36$."),
     NU(r"מהי $P(A\cap B)$?", Fr(7, 50), r"$q-0.36=0.14$.")])

ADD(2, "ד",
    RB((r"פירוק האיחוד $A\cup B=A\ \dot\cup\ (B\cap\overline A)$", 2), (r"$P(B\cap\overline A)=s(1-p)$", 1), (r"התשובה $p+s(1-p)$", 1)),
    [r"לכתוב $p+q$ ולשכוח את החיתוך", r"להניח אי-תלות ולכתוב $p+q-pq$"],
    [CH(r"איזה ביטוי נכון עבור $P(A\cup B)$?",
        [r"$p+s(1-p)$: $A$ ועוד החלק של $B$ שמחוץ ל-$A$", r"$p+q$", r"$p+q-pq$"], 0,
        r"השני סופר את $A\cap B$ פעמיים ($0.9\ne0.76$). השלישי מניח אי-תלות שלא נתונה ($0.7\ne0.76$)."),
     NU(Q2S + r"מהי $P(B\cap\overline A)$?", Fr(9, 25), r"$0.36$."),
     NU(r"מהי $P(A\cup B)$?", Fr(19, 25), r"$0.4+0.36=0.76$.")])

ADD(2, "ה",
    RB((r"תנאי אי-תלות $P(A\cap B)=P(A)P(B)$", 1), (r"הצבת $P(A\cap B)=q-s(1-p)$", 1), (r"פישוט: $q(1-p)=s(1-p)$ ולכן $q=s$ (עבור $p\ne1$)", 2)),
    [r"לשכוח את ההנחה $p\ne1$ בצמצום", r"לבלבל בין אי-תלות לזרות"],
    [CH(r"איזו משוואה מבטאת אי-תלות של $A,B$ עם הנתונים כאן?",
        [r"$q-s(1-p)=pq$", r"$q-s(1-p)=0$", r"$s=p$"], 0,
        r"השנייה היא זרות. השלישית אינה קשורה: אי-תלות אומרת $P(B\mid\overline A)=P(B)$, כלומר $s=q$ ולא $s=p$."),
     NU(r"עבור $p=0.4$ ו-$q=0.5$: איזו $P(A\cap B)$ נדרשת לאי-תלות?", Fr(1, 5), r"$pq=0.2$."),
     NU(r"עבור אותם $p,q$: איזה $s$ מקיים $q-s(1-p)=pq$?", Fr(1, 2), r"$s=\frac{q-pq}{1-p}=\frac{0.3}{0.6}=0.5=q$.")])

ADD(2, "ו",
    RB((r"זרות: $P(A\cap B)=0$", 2), (r"$q-s(1-p)=0$", 2), (r"$q=s(1-p)$", 1)),
    [r"לכתוב $s=q$ (זה אי-תלות)", r"להתעלם מהשוויון $P(A\cap B)=q-s(1-p)$"],
    [CH(r"איזו משוואה מבטאת שהמאורעות $A,B$ זרים?",
        [r"$P(A\cap B)=0$, כלומר $q-s(1-p)=0$", r"$P(A\cap B)=pq$", r"$P(A\cup B)=1$"], 0,
        r"השנייה היא אי-תלות. השלישית אומרת ש-$A,B$ ממלאים את כל המרחב, לא שהם זרים."),
     NU(r"עבור $p=0.4$ ו-$s=0.5$ זרים: מהו $q$?", Fr(3, 10), r"$q=s(1-p)=0.5\cdot0.6=0.3$.")])

# Q3: sample mu = 0.25  =>  a = 1/2, b = 1/2
Q3S = r"נקבע $\mu=0.25$. "
ADD(3, "א",
    RB((r"נרמול: שטח המלבן $a$ ועוד שטח המשולש $b$ שווה $1$", 3), (r"תוחלת: $-\frac a2+b=\mu$", 4), (r"פתרון: $a=\frac23(1-\mu)$, $b=\frac{1+2\mu}3$", 3)),
    [r"לחשב את שטח המשולש כבסיס כפול גובה ($2b$)", r"לשכוח את הסימן של תרומת הצד השלילי לתוחלת"],
    [CH(r"מהי משוואת הנרמול של הצפיפות המשורטטת (מלבן בגובה $a$ על $[-1,0)$ ומשולש בבסיס $2$ וגובה $b$)?",
        [r"$a\cdot1+\frac12\cdot2\cdot b=1$, כלומר $a+b=1$", r"$a\cdot1+2\cdot b=1$", r"$a+b=\mu$"], 0,
        r"שטח משולש הוא חצי בסיס כפול גובה, ולכן $2b$ שגוי. $\mu$ הוא התוחלת ולא סכום השטחים."),
     NU(Q3S + r"מהו $a=\frac23(1-\mu)$?", Fr(1, 2), r"$\frac23\cdot0.75=0.5$."),
     NU(r"מהו $b=\frac{1+2\mu}3$?", Fr(1, 2), r"$\frac{1.5}3=0.5$; ואכן $a+b=1$ ו-$-\frac a2+b=0.25$.")])

ADD(3, "ב",
    RB((r"אי-שליליות: $a\ge0$ ו-$b\ge0$", 2), (r"$\mu\le1$ מ-$a\ge0$ ו-$\mu\ge-\frac12$ מ-$b\ge0$", 2)),
    [r"להפוך את הכיוונים של האי-שוויונות"],
    [NU(r"באיזה $\mu$ מתאפס $a=\frac23(1-\mu)$ (הערך הגדול ביותר)?", 1, r"$\mu=1$."),
     NU(r"באיזה $\mu$ מתאפס $b=\frac{1+2\mu}3$ (הערך הקטן ביותר)?", Fr(-1, 2), r"$\mu=-\frac12$.")])

ADD(3, "ג",
    RB((r"אינטגרציה לפי תחומים", 2), (r"$F_X(0)=a$ ו-$F_X(1)=\frac{5-2\mu}{6}$", 3), (r"הנוסחה בכל ענף", 2)),
    [r"לשכוח את השטח המצטבר $a$ בענף $0\le t<1$", r"לכתוב את הענף האחרון בלי למשוך מ-$1$"],
    [NU(Q3S + r"מהו $F_X(0)$?", Fr(1, 2), r"$a=0.5$ (שטח המלבן)."),
     NU(r"מהו $F_X(1)$?", Fr(3, 4), r"$\frac{5-2\mu}6=\frac{4.5}6=0.75$."),
     NU(r"מהו $F_X(0.5)=a+\frac{1+2\mu}6t^2$?", Fr(9, 16), r"$0.5+0.25\cdot0.25=0.5625$.")])

ADD(3, "ד",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$P(X>0)=b$", 1), (r"$P(0<X<1)=\frac b2$ (חצי המשולש)", 1), (r"התשובה $\frac12$", 1)),
    [r"לחלק ב-$1$ במקום ב-$P(X>0)$", r"לפרש את $\frac12$ כמקרה פרטי של $\mu$ ולא כסימטריה של המשולש"],
    [NU(Q3S + r"מהי הסתברות התנאי $P(X>0)$?", Fr(1, 2), r"שטח המשולש: $b=0.5$."),
     NU(r"מהי $P(0<X<1)$?", Fr(1, 4), r"המשולש סימטרי סביב $x=1$, ולכן חצי ממנו: $\frac b2=0.25$."),
     NU(r"מהי $P(X<1\mid X>0)$?", Fr(1, 2), r"$\frac{0.25}{0.5}=\frac12$, ללא תלות ב-$\mu$.")])

# Q4: p = 0.5, q = 0.4
ADD(4, "א",
    RB((r"נוסחת ההסתברות השלמה על $E$", 3), (r"$P(Q_1/E)=(2p-p^2)^2$ ו-$P(Q_1/\overline E)=2p^2-p^4$", 3), (r"הרכבה: $p(2p-p^2)^2+(1-p)(2p^2-p^4)$", 2)),
    [r"להתייחס ל-$E$ כרכיב בטור", r"לכתוב $P(Q_1/\overline E)=p^2\cdot p^2$"],
    [CH(r"במעגל $Q_1$ ($E$ מחברת בין שני הענפים), כיצד מחשבים את $P(Q_1)$?",
        [r"התניה על $E$: עם $E$ המעגל הוא $(A\|B)$ בטור עם $(C\|D)$, בלי $E$ הוא $(A,C)\|(B,D)$", r"$(A\|B)$ בטור עם $(C\|D)$ בלי להתחשב ב-$E$", r"$(A,C)\|(B,D)$ כאילו $E$ לא קיימת"], 0,
        r"השנייה מתעלמת ממקרה $E$ כבויה, השלישית ממקרה $E$ פועלת (הערכים $0.5625$ ו-$0.4375$ במקום $0.5$)."),
     NU(r"עבור $p=0.5$: מהו $P(Q_1/E)=(2p-p^2)^2$?", Fr(9, 16), r"$0.75^2=0.5625$."),
     NU(r"מהו $P(Q_1/\overline E)=2p^2-p^4$?", Fr(7, 16), r"$0.5-0.0625=0.4375$."),
     NU(r"מהי $P(Q_1)$?", Fr(1, 2), r"$0.5\cdot0.5625+0.5\cdot0.4375=0.5$.")])

ADD(4, "ב",
    RB((r"התניה על $F$", 2), (r"$P(Q_2/F)=q\,P(Q_1)$ (בטור עם $G$)", 2), (r"$P(Q_2/\overline F)=p^2q(1+p-p^2)$", 2), (r"הרכבה", 2)),
    [r"לשכוח שכש-$F$ כבויה גם $D$ מנותקת", r"לשכוח את הגורם $q$ של $G$ בענף בו $F$ פועלת"],
    [CH(r"במעגל $Q_2$ (נוספו $F$ ו-$G$), על מה כדאי להתנות?",
        [r"על $F$: כש-$F$ פועלת המעגל הוא $Q_1$ בטור עם $G$, וכשהיא כבויה $D$ מנותקת", r"על $G$ בלבד: $G$ בטור, לכן $P(Q_2)=q\,P(Q_1)$", r"על $A$: כשהיא פועלת מקבלים מעגל טורי פשוט"], 0,
        r"השנייה שוכחת שכש-$F$ כבויה המעגל שונה מ-$Q_1$ (הערך $0.2$ במקום $0.155$). בשלישית נשארים גשר ושתי יחידות נוספות, כלומר אין פישוט."),
     NU(r"עבור $p=0.5$, $q=0.4$: מהי $P(Q_2/F)=q\,P(Q_1)$?", Fr(1, 5), r"$0.4\cdot0.5=0.2$."),
     NU(r"מהי $P(Q_2/\overline F)=p^2q(1+p-p^2)$?", Fr(1, 8), r"$0.25\cdot0.4\cdot1.25=0.125$."),
     NU(r"מהי $P(Q_2)$?", Fr(31, 200), r"$0.4\cdot0.2+0.6\cdot0.125=0.155$.")])

ADD(4, "ג",
    RB((r"זיהוי $Q_2\subseteq Q_1$", 3), (r"$P(Q_1\cap Q_2)=P(Q_2)$", 2), (r"הצבת הביטוי מסעיף ב", 1)),
    [r"להניח ש-$Q_1,Q_2$ בלתי תלויים ולכפול", r"לכתוב $P(Q_1\cap Q_2)=P(Q_1)$ (הפוך)"],
    [CH(r"מה הקשר בין המאורעות $Q_1$ ו-$Q_2$?",
        [r"$Q_2\subseteq Q_1$: אם $Q_2$ פועל אז גם $Q_1$ פועל, ולכן $P(Q_1\cap Q_2)=P(Q_2)$", r"$Q_1\subseteq Q_2$, ולכן $P(Q_1\cap Q_2)=P(Q_1)$", r"בלתי תלויים: $P(Q_1\cap Q_2)=P(Q_1)P(Q_2)$"], 0,
        r"בדיקה של כל מצבי $A,\ldots,G$ מראה שבכל מצב ש-$Q_2$ פועל גם $Q_1$ פועל, אבל לא להפך (למשל כש-$G$ כבויה). בלתי תלויים הם אינם: הם חולקים את $A,\ldots,E$ ($0.078\ne0.155$)."),
     NU(r"עבור $p=0.5$, $q=0.4$: מהי $P(Q_2\cap\overline{Q_1})$?", 0, r"$Q_2\subseteq Q_1$, ולכן החיתוך ריק."),
     NU(r"מהי $P(Q_1\cap Q_2)$?", Fr(31, 200), r"שווה ל-$P(Q_2)=0.155$.")])

ADD(4, "ד",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$P(Q_1)$ בתור המכנה ו-$P(Q_1\cap Q_2)=P(Q_2)$ במונה", 1), (r"היחס", 1)),
    [r"לחלק ב-$P(Q_2)$ במקום ב-$P(Q_1)$"],
    [NU(r"עבור $p=0.5$, $q=0.4$: מהי הסתברות התנאי $P(Q_1)$?", Fr(1, 2), r"$0.5$ (סעיף א)."),
     NU(r"מהי $P(Q_1\cap Q_2)$?", Fr(31, 200), r"$P(Q_2)=0.155$."),
     NU(r"מהי $P(Q_2\mid Q_1)$?", Fr(31, 100), r"$\frac{0.155}{0.5}=0.31$.")])

# Q5: D = 5 red of N = 12
ADD(5, "א",
    RB((r"הגישה הקלאסית: מקרים רצויים חלקי כל המקרים", 3)),
    [r"לבלבל בין $\frac DN$ לבין $\frac D{N-D}$"],
    [NU(r"בכד $N=12$ כדורים, מהם $D=5$ אדומים. כמה תוצאות שוות-הסתברות יש להוצאת כדור אחד?", 12, r"$N=12$."),
     NU(r"מהי $P(R_1)=\frac DN$?", Fr(5, 12), r"$\frac5{12}\approx0.4167$.")])

ADD(5, "ב",
    RB((r"נוסחת ההסתברות השלמה על צבע הכדור הראשון", 3), (r"$P(R_2/R_1)=\frac{D-1}{N-1}$ ו-$P(R_2/B_1)=\frac D{N-1}$", 2), (r"פישוט ל-$\frac DN$", 2)),
    [r"להניח ש-$P(R_2)=\frac{D-1}{N-1}$ (כאילו הראשון אדום)", r"לשכוח שהצבע של הכדור הראשון אינו ידוע"],
    [CH(r"הכדור הראשון אינו נבדק. כיצד מחשבים את $P(R_2)$?",
        [r"נוסחת ההסתברות השלמה לפי צבע הכדור הראשון", r"$P(R_2)=\dfrac{D-1}{N-1}$, כאילו הכדור הראשון היה אדום", r"$P(R_2)=\dfrac{D}{N-1}$, כאילו הראשון היה שחור"], 0,
        r"השנייה והשלישית מניחות מידע שאין (הערכים $0.364$ ו-$0.455$ במקום $0.4167$)."),
     NU(r"עבור $D=5$, $N=12$: מהי $P(R_2/R_1)$?", Fr(4, 11), r"$\frac{D-1}{N-1}=\frac4{11}$."),
     NU(r"מהי $P(R_2/B_1)$?", Fr(5, 11), r"$\frac D{N-1}=\frac5{11}$."),
     NU(r"מהי $P(R_2)$?", Fr(5, 12), r"$\frac4{11}\cdot\frac5{12}+\frac5{11}\cdot\frac7{12}=\frac{55}{132}=\frac5{12}$.")])

ADD(5, "ג",
    RB((r"התניה על $X$, מספר האדומים בין $n-1$ הכדורים הראשונים ($X\sim\mathrm{Hyp}$)", 5), (r"$P(R_n/X=k)=\frac{D-k}{N-n+1}$", 4), (r"שימוש ב-$\mathbb{E}[X]=(n-1)\frac DN$ ופישוט ל-$\frac DN$", 6)),
    [r"להתעלם מכך שצבעי הכדורים הקודמים אינם ידועים", r"לכפול את $P(R_i)$ לכל $i\le n$ כאילו אלה מאורעות בלתי תלויים"],
    [CH(r"הכדורים $1,\ldots,n-1$ שהוצאו קודם אינם נראים. כיצד מחשבים את $P(R_n)$?",
        [r"מתנים על מספר האדומים $X$ בין $n-1$ הראשונים (התפלגות היפרגיאומטרית) ומשתמשים בנוסחת ההסתברות השלמה", r"מכפילים: $P(R_n)=\prod_{i=1}^{n}P(R_i)$", r"מתנים על הכדור הראשון בלבד ומתעלמים משאר הכדורים"], 0,
        r"המכפלה מייצגת מאורע שונה (כולם אדומים) ואינה מתאימה ($0.030$ במקום $0.417$). התניה על הראשון בלבד משאירה $n-2$ כדורים בלתי ידועים."),
     NU(r"עבור $D=5$, $N=12$, $n=4$: מהי $\mathbb{E}[X]=(n-1)\frac DN$?", Fr(5, 4), r"$3\cdot\frac5{12}=1.25$."),
     NU(r"בהינתן $X=1$: מהי $P(R_4\mid X=1)=\frac{D-k}{N-n+1}$?", Fr(4, 9), r"נשארו $9$ כדורים, מהם $4$ אדומים: $\frac49$."),
     NU(r"מהי $P(R_4)$?", Fr(5, 12), r"$\frac{D-\mathbb{E}[X]}{N-n+1}=\frac{3.75}{9}=\frac5{12}$.")])

ADD(5, "ד",
    RB((r"הגדרת ההסתברות המותנית", 1), (r"$P(R_n)=\frac DN$ מסעיף ג", 1), (r"$P(R_n\cap R_{n+1})=\frac{D(D-1)}{N(N-1)}$", 2), (r"התשובה $\frac{D-1}{N-1}$", 1)),
    [r"לכתוב $\frac{D-1}{N-1}$ בלי לבדוק שהתנאי $R_n$ אינו מגביל את שאר הכדורים", r"לחלק ב-$P(R_{n+1})$"],
    [CH(r"כיצד מחשבים את $P(R_{n+1}\mid R_n)$ כשאין מידע על $n-1$ הכדורים הראשונים?",
        [r"$\dfrac{P(R_n\cap R_{n+1})}{P(R_n)}$, ומתנים על $X$ לחישוב החיתוך", r"$\dfrac{D}{N}$, כי כל כדור שווה סיכוי", r"$\dfrac{D-n}{N-n}$, כאילו הוצאו $n$ אדומים"], 0,
        r"השנייה מתעלמת מהמידע ש-$R_n$ קרה ($0.417$ במקום $0.364$). השלישית מניחה שכל הכדורים הקודמים אדומים."),
     NU(r"עבור $D=5$, $N=12$: מהי הסתברות התנאי $P(R_n)$?", Fr(5, 12), r"$\frac DN=\frac5{12}$."),
     NU(r"מהי $P(R_n\cap R_{n+1})=\frac{D(D-1)}{N(N-1)}$?", Fr(5, 33), r"$\frac{20}{132}=\frac5{33}\approx0.1515$."),
     NU(r"מהי $P(R_{n+1}\mid R_n)$?", Fr(4, 11), r"$\frac{5/33}{5/12}=\frac4{11}\approx0.3636$.")])

# Q6: N = 8 chairs
ADD(6, "א",
    RB((r"כל אחד מהם נבחר אחיד: $X,Y\sim U_d(1,N)$", 1), (r"ההתפלגות המשותפת $\frac1{N(N-1)}$ על $x\ne y$", 1), (r"הם אינם בלתי תלויים", 1)),
    [r"לטעון ש-$X,Y$ בלתי תלויים כי כל אחד אחיד"],
    [CH(r"האם $X$ ו-$Y$ (מספרי הכיסאות) בלתי תלויים?",
        [r"לא: $P(X=3,Y=3)=0$ אבל $P(X=3)P(Y=3)=\frac1{64}>0$", r"כן: כל אחד מהם מתפלג אחיד", r"כן: האנשים נבחרים באקראי ולא מתייעצים"], 0,
        r"שני אנשים אינם יושבים על אותו כיסא, לכן ההסתברות המשותפת על האלכסון היא $0$, בעוד שמכפלת השוליים חיובית. אחידות כל אחד בנפרד לא מבטיחה אי-תלות."),
     NU(r"כמה זוגות סדורים $(x,y)$ עם $x\ne y$ יש עבור $N=8$?", 56, r"$N(N-1)=56$."),
     NU(r"מהי $P(X=3)=\sum_yP(X=3,Y=y)$?", Fr(1, 8), r"$7$ ערכים של $y$, כל אחד $\frac1{56}$: $\frac7{56}=\frac18$."),
     NU(r"מהי $P(X=3,Y=5)$?", Fr(1, 56), r"$\frac1{56}\approx0.0179$.")])

ADD(6, "ב",
    RB((r"$X_L<X_R$ תמיד, ולכן ההסתברות $0$ עבור $j\ge k$", 3), (r"שני המאורעות $\{X=j,Y=k\}$ ו-$\{X=k,Y=j\}$ יוצרים את $\{X_L=j,X_R=k\}$", 4), (r"$\frac2{N(N-1)}$ ובדיקת נרמול", 3)),
    [r"לספור רק את הזוג הסדור אחד, ולקבל $\frac1{N(N-1)}$", r"לשכוח את האפס עבור $j\ge k$"],
    [CH(r"אילו זוגות סדורים $(X,Y)$ נותנים $X_L=3$ ו-$X_R=6$?",
        [r"שניים: $(3,6)$ ו-$(6,3)$", r"אחד: $(3,6)$", r"שלושה: $(3,6)$, $(6,3)$ ו-$(3,3)$"], 0,
        r"$X_L,X_R$ הם המינימום והמקסימום ולכן הסדר לא משנה: שני זוגות. $(3,3)$ אינו אפשרי."),
     NU(r"כמה זוגות לא סדורים $\{j,k\}$ עם $j<k$ יש עבור $N=8$?", 28, r"$\binom82=28$."),
     NU(r"מהי $P(X_L=3,X_R=6)$?", Fr(1, 28), r"$\frac2{56}=\frac1{28}\approx0.0357$ (וסכום $28\cdot\frac1{28}=1$).")])

ADD(6, "ג",
    RB((r"סכימה על שורה או עמודה בטבלה המשותפת", 2), (r"$P(X_L=k)=\frac{2(N-k)}{N(N-1)}$", 2), (r"$P(X_R=k)=\frac{2(k-1)}{N(N-1)}$", 2)),
    [r"להחליף בין השורה לעמודה ולקבל $N-k$ עבור $X_R$"],
    [CH(r"כמה ערכים $X_R$ אפשריים כאשר $X_L=3$ ($N=8$)? (מספר התאים החיוביים בשורה)",
        [r"$N-k=5$", r"$k-1=2$", r"$N-1=7$"], 0,
        r"שורה $X_L=k$ כוללת את $X_R=k+1,\ldots,N$: $N-k$ תאים. $k-1$ הוא מספר התאים בעמודה $X_R=k$."),
     NU(r"מהי $P(X_L=3)$ עבור $N=8$?", Fr(5, 28), r"$\frac{2\cdot5}{56}=\frac5{28}\approx0.1786$."),
     NU(r"מהי $P(X_R=4)$ עבור $N=8$?", Fr(3, 28), r"$\frac{2\cdot3}{56}=\frac3{28}\approx0.1071$.")])

ADD(6, "ד",
    RB((r"$\mathbb{E}[X_L]=\sum k\,P(X_L=k)$", 2), (r"שימוש בסכומי חזקות", 2), (r"$\frac{N+1}3$ ו-$\frac{2(N+1)}3$, והצבת $N=2$", 2)),
    [r"לשכוח שסכום $X_L$ חסום ב-$N-1$"],
    [NU(r"מהו $\mathbb{E}[X_L]$ עבור $N=8$?", 3, r"$\frac{N+1}3=3$."),
     NU(r"מהו $\mathbb{E}[X_R]$ עבור $N=8$?", 6, r"$\frac{2(N+1)}3=6$; ואכן $\mathbb{E}[X_L]+\mathbb{E}[X_R]=9=N+1=\mathbb{E}[X]+\mathbb{E}[Y]$."),
     NU(r"מהו $\mathbb{E}[X_L]$ עבור $N=2$?", 1, r"$\frac{3}3=1$: שני הכיסאות תמיד תפוסים.")])

ADD(6, "ה",
    RB((r"$\mathbb{E}[X_L^2]=\frac{N(N+1)}6$", 2), (r"$\operatorname{var}[X_L]=\frac{(N+1)(N-2)}{18}$", 2), (r"סימטריה לגבי $X_R$ והצבת $N=2$", 1)),
    [r"לשכוח להחסיר את הריבוע של התוחלת"],
    [NU(r"מהי $\operatorname{var}[X_L]$ עבור $N=8$?", 3, r"$\frac{9\cdot6}{18}=3$."),
     NU(r"מהי $\operatorname{var}[X_R]$ עבור $N=8$ (סימטריה: $N+1-X_R\overset d=X_L$)?", 3, r"אותו ערך: $3$."),
     NU(r"מהי $\operatorname{var}[X_L]$ עבור $N=2$?", 0, r"$\frac{3\cdot0}{18}=0$: משתנה דטרמיניסטי.")])

ADD(6, "ו",
    RB((r"$\mathbb{E}[X_LX_R]=\frac{(N+1)(3N+2)}{12}$", 2), (r"$\operatorname{cov}=\frac{(N+1)(N-2)}{36}$", 2), (r"$\rho=\frac12$ עבור $N\ge3$, ולא מוגדר ל-$N=2$", 1)),
    [r"לצמצם $\frac00$ עבור $N=2$ ולקבל $\rho=\frac12$"],
    [NU(r"מהו $\mathbb{E}[X_LX_R]$ עבור $N=8$?", Fr(39, 2), r"$\frac{9\cdot26}{12}=19.5$."),
     NU(r"מהי $\operatorname{cov}[X_L,X_R]=\mathbb{E}[X_LX_R]-\mathbb{E}[X_L]\mathbb{E}[X_R]$?", Fr(3, 2), r"$19.5-3\cdot6=1.5$."),
     NU(r"מהו $\rho[X_L,X_R]$ עבור $N=8$?", Fr(1, 2), r"$\frac{1.5}{\sqrt{3\cdot3}}=\frac12$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = "ai-draft"
        _q["stepsSource"] = "ai-draft"

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ה, מועד ב (12.03.2025)",
    "year": 2025,
    "examDate": "12.03.2025",
    "sourceFile": "25A-B exam pp.1-3",
    "solutionFile": "25A-B handwritten official solutions, pp.4-23",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1", "text": Q1_TXT},
        "c2": {"kind": "text", "title": "שאלה 2", "text": Q2_TXT},
        "c3": {"kind": "image", "title": "שאלה 3", "image": IMG + "Q3-pdf.png", "caption": Q3_TXT},
        "c4": {"kind": "image", "title": "שאלה 4: מעגלים", "image": IMG + "Q4-circuits.png", "caption": Q4_TXT},
        "c5": {"kind": "image", "title": "שאלה 5: כד", "image": IMG + "Q5-urn.png", "caption": Q5_TXT},
        "c6": {"kind": "text", "title": "שאלה 6: כיסאות", "text": Q6_TXT},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
