# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-B.json -- probability (course 20021), semester A 2025, moed B (12.03.2025).
6 questions, 30 items (Q1 6, Q2 6, Q3 4, Q4 4, Q5 4, Q6 6), 25 points each (Q5 d, Q6 e, f are 5-point bonus parts).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-B.py

Source: exam pp.1-3, handwritten official solutions on grid paper pp.4-23. Student/lecturer names are not copied.

Transcription notes
- Part keys: single letters, printed label is the first bold token. Q1 prints "א-1..א-3, ב, ג, ד" -> a..f.
  Q2 prints "א-1..א-4, ב, ג" -> a..f. Q6: a..f = א, ב, ג, ד, ה (bonus 1), ו (bonus 2).
- Q6 HOLD e, f: the two bonus parts (variances / correlation coefficient) have no worked solution in the solution file
  (it ends after part ד). Held as no-key; the orchestrator routes them to the solver.
- Q6: the printed text names the two people who sit down by their first names (they are lecturers); the names are
  replaced by "שני אנשים", the photo is not cropped and the sentence about the figure is reworded.
- Q1 d: E[sqrt Z] has infinite-variance Monte Carlo (E[Z] is infinite), see check.py (truncated MC + exact).
- Q1 area items carry `region` data (REGIONS below; RAW_SCHEMA `region`).
- Math never holds Hebrew.
"""
import json, pathlib

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

HOLD_Q6 = "no-key: the official solution file (pp.4-23) ends after part Q6-ד; the bonus parts ה and ו have no worked solution."

questions.append(Q(
    6, "ה", "discrete_rv",
    r"**סעיף בונוס 1:** חשבו את השונויות $\operatorname{var}[X_L]$ ו-$\operatorname{var}[X_R]$. הציבו $N=2$ והסבירו את התוצאה! (5 נק׳ - הניקוד יינתן רק עבור פתרון מלא.)" "\n" + Q6_HINT,
    "", 5, contextId="c6", hold=HOLD_Q6))

questions.append(Q(
    6, "ו", "joint_discrete",
    r"**סעיף בונוס 2:** חשבו את מקדם המתאם $\rho[X_L,X_R]$. האם הנוסחה שפיתחת נכונה גם עבור $N=2$? נמקו! (5 נק׳ - הניקוד יינתן רק עבור פתרון מלא.)" "\n" + Q6_HINT,
    "", 5, contextId="c6", hold=HOLD_Q6))

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
