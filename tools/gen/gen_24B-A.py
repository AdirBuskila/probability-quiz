# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-A.json -- probability (course 20021), semester B 2024, moed A (16.07.2024).
6 questions, 24 items (Q1 5, Q2 4, Q3 6, Q4 3, Q5 3, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-A.py

Source: exam pp.1-3, handwritten official solutions pp.4-11 (grid paper).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, a-3, b-1, b-2; stored as a b c d e (the printed label is the
  first bold token of each question text). Map: Q1 a=א-1, b=א-2, c=א-3, d=ב-1, e=ב-2.
- Math never holds Hebrew.
- Q1 area items carry `region` (area figure) and, with the other numeric parts, `sim`: see EXTRAS near the end.
- Q3(ה) (independent?): the handwritten reason is only partly legible ("dependent"); the shipped reasoning uses the
  official joint table of the same solution (a zero cell), confidence med. Q3(ו) is the official cov != 0.
- Q5(ג): the official solution concludes E[Y] >= E[X] (via Var >= 0); it is transcribed as printed.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-A.json"
CODE = "24B-A"
IMG = "images/exams/24B-A-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_LEAD = r"נתבונן בשני גפרורים שאורכם מהווים משתנים מקריים בלתי תלויים $X\sim U_c(0,L)$ ו-$Y\sim U_c(0,L)$."
Q1_B = r"יהי $Z$ אורך הגפרור הקצר בין השניים: $Z=\min(X,Y)$."

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א-1:** חשבו את ההסתברות $P(X<L/3)$.",
    r"""$X\sim U_c(0,L)$, ולכן
$$P(X<L/3)=F_X(L/3)=\frac{L/3}{L}=\frac13.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**א-2:** חשבו את ההסתברות $P(Y>L/4)$.",
    r"""$Y\sim U_c(0,L)$, ולכן
$$P(Y>L/4)=1-F_Y(L/4)=1-\frac14=\frac34.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**א-3:** חשבו את ההסתברות $P(X+Y\le 4L/3)$.",
    r"""נשתמש בגישה הקלאסית (גאומטרית): מרחב המדגם הוא הריבוע $\Omega=\{0<x<L,\ 0<y<L\}$ ושטחו $|\Omega|=L^2$.
$$P(X+Y\le \tfrac43L)=\frac{|\{Y\le \frac43L-x\}|}{|\Omega|}.$$
הישר $y=\frac43L-x$ חותך את הריבוע, והאזור שמעליו (הפינה הימנית-עליונה) הוא משולש שניצביו באורך $\frac{2L}{3}$. לכן
$$|\{Y\le \tfrac43L-x\}|=L^2-\frac12\left(\frac{2L}{3}\right)^2=\left(1-\frac29\right)L^2=\frac79L^2.$$
ומכאן
$$P(X+Y\le \tfrac43L)=\frac79.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ד", "minmax_transform",
    Q1_B + "\n" + r"**ב-1:** חשבו את ההסתברות $P(Z<L/3)$.",
    r"""נפצל לפי איזה גפרור קצר יותר:
$$P(Z<\tfrac L3)=P(Z<\tfrac L3\cap X\le Y)+P(Z<\tfrac L3\cap X>Y)=P(X<\tfrac L3\cap Y\ge X)+P(Y<\tfrac L3\cap Y<X).$$
בגישה הגאומטרית ($|\Omega|=L^2$):
$$\frac{|\{X<\frac L3\cap Y\ge X\}|}{L^2}+\frac{|\{Y<\frac L3\cap Y<X\}|}{L^2}.$$
האזור הראשון הוא הרצועה $0<x<\frac L3$ מעל הישר $y=x$, ושטחו
$$L\cdot\frac L3-\frac12\left(\frac L3\right)^2=L^2\left(\frac13-\frac1{18}\right)=\frac5{18}L^2.$$
האזור השני סימטרי לו ולכן גם שטחו $\frac5{18}L^2$. סך הכול
$$P(Z<\tfrac L3)=\frac5{18}+\frac5{18}=\frac59.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ה", "minmax_transform",
    Q1_B + "\n" + r"**ב-2:** חשבו את ההסתברות המותנית $P(Z<L/2\ /\ X>L/4)$.",
    r"""לפי הגדרת ההסתברות המותנית:
$$P(Z<\tfrac L2\mid X>\tfrac L4)=\frac{P(Z<\frac L2\cap X>\frac L4)}{P(X>\frac L4)},\qquad P(X>\tfrac L4)=\frac34.$$
בגישה הגאומטרית המונה הוא שטח האזור $\{Z<\frac L2\}\cap\{X>\frac L4\}$ חלקי $|\Omega|=L^2$. האזור מורכב משני חלקים, ושטחו הכולל הוא
$$\frac{\frac{L^2}4+\frac{L^2}4}{L^2}=\frac12.$$
ולכן
$$P(Z<\tfrac L2\mid X>\tfrac L4)=\frac43\cdot\frac12=\frac23.$$""",
    5, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_LEAD = r"באוסף נמצאות 10 ספרות: $\{0,1,2,3,4,5,6,7,8,9\}$."
questions.append(Q(
    2, "א", "combinatorics",
    r"מוציאים מהאוסף ספרה אחת. מהי ההסתברות שהיא תהיה שווה ל-3?",
    r"""$$P(3_1)=\frac{|3_1|}{|\Omega|}=\frac1{10}.$$""",
    5, contextId="c2"))
questions.append(Q(
    2, "ב", "combinatorics",
    r"מוציאים מהאוסף שתי ספרות ללא החזרה. מהי ההסתברות שהספרה השנייה תהיה שווה ל-3?",
    r"""הספרה הראשונה אינה 3 (ההסתברות $\frac9{10}$), ואז הספרה השנייה היא 3 (ההסתברות $\frac19$ מבין 9 הספרות שנותרו):
$$P(3_2)=\frac9{10}\cdot\frac19=\frac1{10}.$$""",
    7, contextId="c2"))
questions.append(Q(
    2, "ג", "combinatorics",
    r"מוציאים מהאוסף שלוש ספרות ללא החזרה. מהי ההסתברות שהספרה השלישית תהיה שווה ל-3?",
    r"""שתי הספרות הראשונות אינן 3, ואז השלישית היא 3:
$$P(3_3)=\frac9{10}\cdot\frac89\cdot\frac18=\frac1{10}.$$""",
    7, contextId="c2"))
questions.append(Q(
    2, "ד", "combinatorics",
    r"מוציאים מהאוסף את כל הספרות ללא החזרה. מהי ההסתברות שהספרה העשירית תהיה שווה ל-3?",
    r"""תשע הספרות הראשונות אינן 3, והאחרונה היא 3:
$$P(3_{10})=\frac9{10}\cdot\frac89\cdot\frac78\cdot\frac67\cdot\frac56\cdot\frac45\cdot\frac34\cdot\frac23\cdot\frac12\cdot 1=\frac1{10}.$$""",
    6, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_LEAD = (r"נתבונן במטריצת ברנולי מהצורה $\boldsymbol{Q}=\begin{pmatrix}X&-X^2\\Y^2&X-Y\end{pmatrix}$, "
           r"כאשר $X$ ו-$Y$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגויות ברנולי: $X\sim\mathrm{Ber}(p)$ ו-$Y\sim\mathrm{Ber}(p)$. "
           r"נגדיר שני משתנים מקריים חדשים: דטרמיננטה $D=\det\boldsymbol{Q}$ ועקבה $T=\operatorname{tr}\boldsymbol{Q}$ של המטריצה $\boldsymbol{Q}$.")
Q3_PRE = r"""**פישוט.** מאחר ש-$X,Y\in\{0,1\}$ מתקיים $X^2=X$ ו-$Y^2=Y$, ולכן
$$D=X(X-Y)+X^2Y^2=X-XY+XY=X,\qquad T=X+(X-Y)=2X-Y.$$
"""

questions.append(Q(
    3, "א", "joint_discrete",
    r"**א:** חשבו את פונקציית ההסתברות המשותפת של משתנה מקרי דו ממדי $(D,T)$.",
    Q3_PRE + r"""נמנה את ארבע התוצאות האפשריות של $(X,Y)$:
$$\begin{array}{c|c|c|c|c} X & Y & D & T & \mathrm{P} \\ \hline 0 & 0 & 0 & 0 & (1-p)^2 \\ \hline 0 & 1 & 0 & -1 & p(1-p) \\ \hline 1 & 0 & 1 & 2 & p(1-p) \\ \hline 1 & 1 & 1 & 1 & p^2 \end{array}$$

ולכן הפונקציה המשותפת (עם השוליים):
$$\begin{array}{c|c|c|c|c|c} D\backslash T & -1 & 0 & 1 & 2 & P_D(d) \\ \hline 0 & p(1-p) & (1-p)^2 & 0 & 0 & 1-p \\ \hline 1 & 0 & 0 & p^2 & p(1-p) & p \\ \hline P_T(t) & p(1-p) & (1-p)^2 & p^2 & p(1-p) & 1 \end{array}$$
""",
    5, contextId="c3"))

questions.append(Q(
    3, "ב", "discrete_rv",
    r"**ב:** חשבו תוחלת $\mathbb{E}[D]$ ושונות $\operatorname{var}[D]$ של דטרמיננטה.",
    r"""מאחר ש-$D=X$ ו-$X\sim\mathrm{Ber}(p)$:
$$\mathbb{E}[D]=\mathbb{E}[X]=p,\qquad \operatorname{Var}[D]=\operatorname{Var}[X]=p(1-p).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ג", "discrete_rv",
    r"**ג:** חשבו תוחלת $\mathbb{E}[T]$ ושונות $\operatorname{var}[T]$ של עקבה.",
    r"""מאחר ש-$T=2X-Y$ ו-$X,Y$ בלתי תלויים:
$$\mathbb{E}[T]=2\mathbb{E}[X]-\mathbb{E}[Y]=2p-p=p,$$
$$\operatorname{Var}[T]=4\operatorname{Var}[X]+\operatorname{Var}[Y]=4p(1-p)+p(1-p)=5p(1-p).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ד", "joint_discrete",
    r"**ד:** חשבו את השונות המשותפת $\operatorname{cov}[D,T]$.",
    r"""$$\operatorname{Cov}[D,T]=\mathbb{E}[DT]-\mathbb{E}[D]\,\mathbb{E}[T].$$
$$\mathbb{E}[DT]=\mathbb{E}[X(2X-Y)]=2\mathbb{E}[X]-\mathbb{E}[XY]=2\mathbb{E}[X]-\mathbb{E}[X]\mathbb{E}[Y]=2p-p^2$$
(השתמשנו ב-$X^2=X$ ובאי-התלות של $X,Y$). לכן
$$\operatorname{Cov}[D,T]=2p-p^2-p\cdot p=2p(1-p).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ה", "independence",
    r"**ה:** האם המשתנים $D$ ו-$T$ בלתי תלויים? נמקו היטב!",
    r"""**לא, המשתנים תלויים.**
מהטבלה המשותפת: $P(D=0,T=1)=0$, אבל
$$P(D=0)\,P(T=1)=(1-p)\,p^2>0\qquad(0<p<1).$$
מכיוון ש-$P(D=0,T=1)\ne P(D=0)P(T=1)$, המשתנים אינם בלתי תלויים. (בהתאם, $\operatorname{Cov}[D,T]=2p(1-p)\ne0$ עבור $0<p<1$, ובלתי תלויים היו בהכרח בלתי מתואמים.)""",
    4, contextId="c3", confidence="med"))

questions.append(Q(
    3, "ו", "joint_discrete",
    r"**ו:** האם המשתנים $D$ ו-$T$ בלתי מתואמים? נמקו היטב!",
    r"""**לא, המשתנים מתואמים.**
$\operatorname{Cov}[D,T]=2p(1-p)\ne 0$ עבור $p\ne 0,1$, ולכן $D$ ו-$T$ אינם בלתי מתואמים.""",
    4, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_LEAD = r"לפניכם גרף עבור פונקציית צפיפות ההסתברות $f_Z(z)$ של משתנה מקרי $Z$."

questions.append(Q(
    4, "א", "continuous_rv",
    r"**א:** בהנחה כי $\mathbb{E}[Z]=3/8$, מצאו את הפרמטרים $a$ ו-$b$.",
    r"""**נרמול.** שטח הצפיפות הוא 1: שני משולשים בשטח $\frac a2$ כל אחד, ומלבן ברוחב $b-a$ וגובה 1:
$$\frac a2+\frac a2+(b-a)=1\ \Longrightarrow\ b=1.$$
**תוחלת.** על הקטעים $(-a,0)$ ו-$(0,a)$ הצפיפות היא $-\frac za$ ו-$\frac za$ בהתאמה:
$$\mathbb{E}[Z]=\int_{-a}^0z\left(-\frac za\right)dz+\int_0^az\cdot\frac za\,dz+\int_a^bz\cdot1\,dz.$$
שני האינטגרלים הראשונים מבטלים זה את זה (סכומם 0), והשלישי שווה $\frac{b^2-a^2}2$. לכן, עם $b=1$,
$$\frac{b^2-a^2}{2}=\frac38\ \Longrightarrow\ a^2=\frac14\ \Longrightarrow\ a=\frac12.$$
תשובה: $a=\frac12,\ b=1$.""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"**ב:** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_Z(t)$ ושרטטו את התוצאה.",
    r"""עם $a=\frac12$, $b=1$ הצפיפות היא $-2z$ על $(-\frac12,0)$, $2z$ על $(0,\frac12)$ ו-$1$ על $(\frac12,1)$. אינטגרציה לכל $t\in\mathbb{R}$ נותנת
$$F_Z(t)=P(Z\le t)=\begin{cases}0,&t<-\frac12,\\ \frac14-t^2,&-\frac12\le t<0,\\ \frac14+t^2,&0\le t<\frac12,\\ t,&\frac12\le t<1,\\ 1,&t\ge1.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת F_Z(t)](images/exams/24B-A-Q4-cdf.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"**ג:** מהי ההסתברות המותנית $P(Z>1/4\ /\ |Z|<1/2)$?",
    r"""$$P\left(Z>\tfrac14\ \Big|\ |Z|<\tfrac12\right)=\frac{P(\frac14<Z<\frac12)}{P(|Z|<\frac12)}=\frac{F_Z(\frac12)-F_Z(\frac14)}{F_Z(\frac12)-F_Z(-\frac12)}=\frac{\frac12-\frac5{16}}{\frac12-0}=\frac38.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_LEAD = (r"במפגש משתתפות $N$ משפחות. במשפחה הראשונה ישנם $n_1$ אנשים, במשפחה השנייה ישנם $n_2$ אנשים, $\ldots$, "
           r"במשפחה ה-$N$ ישנם $n_N$ אנשים. מתקיים: $n_1\ne n_2\ne\cdots\ne n_N$.")
Q5_HINT = ""

questions.append(Q(
    5, "א", "discrete_rv",
    r"**א:** בוחרים **באקראי** באחת המשפחות. יהי $X$ משתנה מקרי המתאר את גודל המשפחה שנבחרה. מהו הגודל הממוצע $\mathbb{E}[X]$ של משפחה שנבחרה?",
    r"""כל משפחה נבחרת בהסתברות $\frac1N$, ולכן:
$$\begin{array}{c|c|c|c|c} x & n_1 & n_2 & \cdots & n_N \\ \hline P_X(x) & \frac1N & \frac1N & \cdots & \frac1N \end{array}$$

$$\mathbb{E}[X]=\frac{n_1+n_2+\cdots+n_N}{N}.$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ב", "discrete_rv",
    r"**ב:** בוחרים **באקראי** באחד ממשתתפי המפגש. יהי $Y$ גודל של משפחתו. מהו הגודל הממוצע $\mathbb{E}[Y]$ של משפחתו של המשתתף?",
    r"""נסמן $n=n_1+n_2+\cdots+n_N$ (מספר המשתתפים). המשתתף שנבחר שייך למשפחה $i$ בהסתברות $\frac{n_i}{n}$, ואז $Y=n_i$:
$$\begin{array}{c|c|c|c|c} y & n_1 & n_2 & \cdots & n_N \\ \hline P_Y(y) & \frac{n_1}{n} & \frac{n_2}{n} & \cdots & \frac{n_N}{n} \end{array}$$

$$\mathbb{E}[Y]=\frac{n_1^2+n_2^2+\cdots+n_N^2}{n_1+n_2+\cdots+n_N}.$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ג", "discrete_rv",
    r"**ג:** האם $\mathbb{E}[Y]=\mathbb{E}[X]$? האם $\mathbb{E}[Y]\ge\mathbb{E}[X]$? האם $\mathbb{E}[Y]<\mathbb{E}[X]$? יש לנמק **היטב!**",
    r"""מהסעיפים הקודמים, $\mathbb{E}[X]=\frac{n}{N}$ ו-$\mathbb{E}[X^2]=\frac{n_1^2+\cdots+n_N^2}{N}$, ולכן
$$\mathbb{E}[Y]=\frac{\mathbb{E}[X^2]}{\mathbb{E}[X]}=\frac{\operatorname{Var}[X]+(\mathbb{E}[X])^2}{\mathbb{E}[X]}.$$
נחלק ב-$\mathbb{E}[X]$:
$$\frac{\mathbb{E}[Y]}{\mathbb{E}[X]}=1+\frac{\operatorname{Var}[X]}{(\mathbb{E}[X])^2}\ge1.$$
מכאן $\mathbb{E}[Y]\ge\mathbb{E}[X]$ (התשובה הרשמית). בהתאם, הטענה $\mathbb{E}[Y]<\mathbb{E}[X]$ אינה נכונה.""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_LEAD = (r"ארבעה רכיבים $A$, $B$, $C$ ו-$D$ פועלים בהסתברויות זהות וללא תלות אחד בשני: $P(A)=P(B)=P(C)=P(D)=p$. "
           r"מרכיבים אלה הורכב המעגל הראשון ($\boldsymbol{Q}_1$) ולאחר מכן המעגל השני ($\boldsymbol{Q}_2$) בו חלק היחידות נלקחו מהמעגל $\boldsymbol{Q}_1$; "
           r"היחידה $E$ הינה יחידה חדשה הפועלת בהסתברות $P(E)=q$ ללא תלות ביחידות אחרות.")

questions.append(Q(
    6, "א", "circuits",
    r"**א:** מהי ההסתברות $P(\boldsymbol{Q}_1)$ שהמעגל הראשון יפעל?",
    r"""המעגל הראשון: $D$ בטור עם המקבץ של ($A$ בטור $B$) במקביל ל-$C$:
$$Q_1=\bigl((A\cap B)\cup C\bigr)\cap D.$$
$$P(Q_1)=P(D)\bigl\{P(A\cap B)+P(C)-P(A\cap B\cap C)\bigr\}=p\,(p^2+p-p^3)=p^2(1+p-p^2).$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"**ב:** מהי ההסתברות שגם מעגל $\boldsymbol{Q}_2$ **וגם** מעגל $\boldsymbol{Q}_1$ יפעלו?",
    r"""נסמן $\tilde Q=Q_1\cap Q_2$ (שני המעגלים מחוברים בטור, כשכל רכיב משותף מופיע פעם אחת בחישוב). נשתמש בהסתברות שלמה לפי $A$:
$$P(\tilde Q)=P(\tilde Q\mid A)P(A)+P(\tilde Q\mid\bar A)P(\bar A).$$
**$A$ פועל.** $Q_2$ פועל מיד (הענף התחתון תקין), ו-$Q_1$ פועל אם $D$ פועל ו-$B$ או $C$ פועל:
$$\tilde Q\mid A=D\cap(B\cup C),\qquad P(\tilde Q\mid A)=p(2p-p^2)=p^2(2-p).$$
**$A$ אינו פועל.** $Q_1$ דורש $D\cap C$, ו-$Q_2$ דורש $D\cap E\cap B$:
$$\tilde Q\mid\bar A=D\cap C\cap E\cap B,\qquad P(\tilde Q\mid\bar A)=p^3q.$$
לכן
$$P(\tilde Q)=p^3(2-p)+p^3q(1-p)=p^3\bigl[2-p+q(1-p)\bigr]=p^3\bigl[1+(1-p)(1+q)\bigr].$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    r"**ג:** אם ידוע כי מעגל $\boldsymbol{Q}_1$ פעל, מהי ההסתברות שגם המעגל $\boldsymbol{Q}_2$ יפעל?",
    r"""$$P(Q_2\mid Q_1)=\frac{P(Q_1\cap Q_2)}{P(Q_1)}=\frac{p^3\bigl[1+(1-p)(1+q)\bigr]}{p^2(1+p-p^2)}=p\cdot\frac{1+(1-p)(1+q)}{1+(1-p)p}.$$""",
    7, contextId="c6"))

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר ב׳ תשפ״ד, מועד א (16.07.2024)",
    "year": 2024,
    "examDate": "16.07.2024",
    "sourceFile": "24B-A exam pp.1-3",
    "solutionFile": "24B-A official handwritten solutions pp.4-11",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1", "text": Q1_LEAD},
        "c2": {"kind": "text", "title": "שאלה 2", "text": Q2_LEAD},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_LEAD},
        "c4": {"kind": "image", "title": "שאלה 4: גרף הצפיפות", "image": IMG + "Q4-pdf.png", "caption": Q4_LEAD},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_LEAD},
        "c6": {"kind": "image", "title": "שאלה 6: שני מעגלים", "image": IMG + "Q6-circuits.png", "caption": Q6_LEAD},
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
    (1, "א"): {"region": REG([lin(1, 0, "1/3", "<")], 1 / 3, "האירוע X<L/3 (יחידות של L)"),
               "sim": AREA("P(X<L/3)", 1 / 3)},
    (1, "ב"): {"region": REG([lin(0, 1, "1/4", ">")], 3 / 4, "האירוע Y>L/4 (יחידות של L)"),
               "sim": AREA("P(Y>L/4)", 3 / 4)},
    (1, "ג"): {"region": REG([lin(1, 1, "4/3", "<=")], 7 / 9, "האירוע X+Y<=4L/3 (יחידות של L)"),
               "sim": AREA("P(X+Y<=4L/3)", 7 / 9)},
    (1, "ד"): {"region": REG({"any": [[lin(1, 0, "1/3", "<")], [lin(0, 1, "1/3", "<")]]}, 5 / 9, "האירוע min(X,Y)<L/3 (יחידות של L)"),
               "sim": AREA("P(Z<L/3)", 5 / 9)},
    (1, "ה"): {"region": REG({"any": [[lin(1, 0, "1/2", "<")], [lin(0, 1, "1/2", "<")]]}, 2 / 3, "האירוע min(X,Y)<L/2 בהינתן X>L/4 (יחידות של L)",
                             given=[lin(1, 0, "1/4", ">")]),
               "sim": AREA("P(Z<L/2 | X>L/4)", 2 / 3)},
    (2, "א"): {"sim": {"kind": "urn", "estimate": "P(1st digit = 3)", "exact": 1 / 10,
                       "params": {"values": list(range(10)), "draws": 1, "event": "v1 == 3"}}},
    (2, "ב"): {"sim": {"kind": "urn", "estimate": "P(2nd digit = 3)", "exact": 1 / 10,
                       "params": {"values": list(range(10)), "draws": 2, "event": "v2 == 3"}}},
    (2, "ג"): {"sim": {"kind": "urn", "estimate": "P(3rd digit = 3)", "exact": 1 / 10,
                       "params": {"values": list(range(10)), "draws": 3, "event": "v3 == 3"}}},
    (2, "ד"): {"sim": {"kind": "urn", "estimate": "P(10th digit = 3)", "exact": 1 / 10,
                       "params": {"values": list(range(10)), "draws": 10, "event": "v10 == 3"}}},
    (4, "ג"): {"sim": PDF("P(Z>1/4 | |Z|<1/2)", 3 / 8,
                          [("-1/2", 0, "-2*x"), (0, "1/2", "2*x"), ("1/2", 1, "1")], "x > 1/4", "abs(x) < 1/2")},
}
for _q in questions:
    _x = EXTRAS.get((_q["num"], _q.get("part")))
    if _x:
        _q.update(_x)


# ---- extra sims for items with symbolic answers, at sample parameter values (stated in `estimate`)
def _bern(p):
    return {"X": {"values": [0, 1], "probs": [1 - p, p]}, "Y": {"values": [0, 1], "probs": [1 - p, p]}}


_DET = "X*(X-Y)+X^2*Y^2"      # det Q straight from the matrix entries (no X^2=X shortcut)
_TR = "X+(X-Y)"
EXTRA_SIMS = {
    (3, "א"): {"kind": "custom_discrete", "estimate": "P(D=1, T=2) ב-p=0.3", "exact": 0.21,
               "params": {"vars": _bern(0.3), "event": _DET + " == 1 and " + _TR + " == 2"}},
    (3, "ב"): {"kind": "custom_discrete", "estimate": "Var[D] ב-p=0.3", "exact": 0.21,
               "params": {"vars": _bern(0.3), "measure": "var", "expr": _DET}},
    (3, "ג"): {"kind": "custom_discrete", "estimate": "Var[T] ב-p=0.3", "exact": 1.05,
               "params": {"vars": _bern(0.3), "measure": "var", "expr": _TR}},
    (3, "ד"): {"kind": "custom_discrete", "estimate": "cov[D,T] ב-p=0.3", "exact": 0.42,
               "params": {"vars": _bern(0.3), "measure": "cov", "expr": [_DET, _TR]}},
    (3, "ה"): {"kind": "custom_discrete", "estimate": "P(D=0, T=1) ב-p=0.3", "exact": 0,
               "params": {"vars": _bern(0.3), "event": _DET + " == 0 and " + _TR + " == 1"}},
    (3, "ו"): {"kind": "custom_discrete", "estimate": "cov[D,T] ב-p=0.3", "exact": 0.42,
               "params": {"vars": _bern(0.3), "measure": "cov", "expr": [_DET, _TR]}},
    (4, "א"): PDF("E[Z] ב-a=1/2, b=1", 3 / 8, [("-1/2", 0, "-2*x"), (0, "1/2", "2*x"), ("1/2", 1, "1")], "x").copy(),
    (5, "א"): {"kind": "urn", "estimate": "E[X] בשלוש משפחות בגדלים 2,3,7", "exact": 4,
               "params": {"values": [2, 3, 7], "draws": 1, "measure": "mean", "expr": "v1"}},
    (5, "ב"): {"kind": "urn", "estimate": "E[Y] בשלוש משפחות בגדלים 2,3,7", "exact": 31 / 6,
               "params": {"values": [2] * 2 + [3] * 3 + [7] * 7, "draws": 1, "measure": "mean", "expr": "v1"}},
    (5, "ג"): {"kind": "urn", "estimate": "Var[X] בשלוש משפחות בגדלים 2,3,7", "exact": 14 / 3,
               "params": {"values": [2, 3, 7], "draws": 1, "measure": "var", "expr": "v1"}},
    (6, "א"): {"kind": "circuit", "estimate": "P(Q1) ב-p=0.6", "exact": 0.4464,
               "params": {"event": "S", "network": {"type": "series", "children": [
                   {"type": "comp", "id": "D", "p": 0.6},
                   {"type": "parallel", "children": [
                       {"type": "series", "children": [{"type": "comp", "id": "A", "p": 0.6}, {"type": "comp", "id": "B", "p": 0.6}]},
                       {"type": "comp", "id": "C", "p": 0.6}]}]}}},
}
# Q4(א): the pdf sim is a "mean" measure, not a probability
EXTRA_SIMS[(4, "א")]["params"]["measure"] = "mean"
EXTRA_SIMS[(4, "א")]["params"]["expr"] = "x"
EXTRA_SIMS[(4, "א")]["params"].pop("event")
_CIRC5 = {"type": "series", "children": [{"type": "comp", "id": c, "p": 0.6} for c in "ABCD"] + [{"type": "comp", "id": "E", "p": 0.5}]}
_Q1E = "D and ((A and B) or C)"
_Q2E = "D and (A or (E and B))"
EXTRA_SIMS[(6, "ב")] = {"kind": "circuit", "estimate": "P(Q1 וגם Q2) ב-p=0.6, q=0.5", "exact": 0.3456,
                        "params": {"event": _Q1E + " and " + _Q2E, "network": _CIRC5}}
EXTRA_SIMS[(6, "ג")] = {"kind": "circuit", "estimate": "P(Q2 | Q1) ב-p=0.6, q=0.5", "exact": 0.3456 / 0.4464,
                        "params": {"event": _Q2E, "given": _Q1E, "network": _CIRC5}}
for _q in questions:
    _x = EXTRA_SIMS.get((_q["num"], _q.get("part")))
    if _x and "sim" not in _q:
        _q["sim"] = _x


# ---- rubric / pitfalls / steps (ai-draft). Every expected value is re-derived independently, by exact arithmetic and
# by Monte Carlo, in tools/verify/24B-A/steps_check.py (which reads the generated raw JSON).
from fractions import Fraction as Fr

FRAC = 0.0006   # tolerance when the answer is a non-terminating fraction entered as a 3-4 digit decimal


def O(*v):
    return [{"id": "abcdefgh"[i], "value": t} for i, t in enumerate(v)]


def CH(prompt, opts, ans, explain):
    return {"type": "choice", "prompt": prompt, "options": O(*opts), "correctId": "abcdefgh"[ans], "explain": explain}


def NU(prompt, val, explain):
    val = Fr(val)
    small = abs(val) < Fr(1, 10)           # small values need more digits: a 0.0006 tolerance would accept 0.02 for 0.0206
    a = round(float(val), 6 if small else 4)
    exact = (val * 10000).denominator == 1
    return {"type": "numeric", "prompt": prompt + ("" if exact else " (שבר או עשרוני)"), "answer": a,
            "tol": 0 if exact else (6e-5 if small else FRAC), "explain": explain}


def RB(*r):
    return [{"text": t, "points": p} for t, p in r]


S = {}


def ADD(num, part, rub, pit, steps):
    S[(num, part)] = (rub, pit, steps)


OMEGA = r"נקבע $L=1$ (היחס אינו תלוי ב-$L$). מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X,Y)$?"
OMEGA_X = r"הריבוע $(0,1)^2$ הוא מרחב המדגם של $(X,Y)$, ושטחו $1$. אלא אם $|\Omega|\ne1$, ההסתברות פשוט שווה לשטח; חשוב לבדוק זאת."

ADD(1, "א",
    RB((r"גישה גאומטרית: הסתברות = שטח האירוע חלקי $|\Omega|=L^2$ (או $F_X$ של אחידה)", 2),
       (r"האירוע $X<L/3$ הוא רצועה ברוחב $L/3$ לכל גובה הריבוע", 2), (r"התשובה $\frac13$", 1)),
    [r"לחשב שטח ולא לחלק ב-$|\Omega|$ (כאן זה מתחבא כי $L=1$)", r"להתייחס ל-$Y$ כאילו הוא מגביל את האירוע"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח האירוע $\{X<\frac13\}$ בתוך הריבוע?", Fr(1, 3), r"רצועה ברוחב $\frac13$ וגובה $1$: שטח $\frac13$, ולכן $P=\frac{1/3}{1}=\frac13$.")])

ADD(1, "ב",
    RB((r"גישה גאומטרית או $1-F_Y(L/4)$", 2), (r"האירוע $Y>L/4$ הוא רצועה ברוחב $\frac34L$ (או משלים של רצועה)", 2), (r"התשובה $\frac34$", 1)),
    [r"להפוך את האי-שוויון ולחשב $P(Y<L/4)=\frac14$", r"לשכוח את החילוק ב-$|\Omega|$"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח האירוע $\{Y>\frac14\}$ בתוך הריבוע?", Fr(3, 4), r"רצועה בגובה $1-\frac14=\frac34$ וברוחב $1$: שטח $\frac34$.")])

ADD(1, "ג",
    RB((r"הצגת $\Omega$ כריבוע ו-$|\Omega|=L^2$", 1), (r"זיהוי המשלים $X+Y>\frac43L$ כמשולש פינתי בקודקוד $(L,L)$", 2),
       (r"שטח המשולש $\frac12\left(\frac{2L}{3}\right)^2$ והחסרתו מ-$L^2$", 1), (r"התשובה $\frac79$", 1)),
    [r"לחשב את שטח המשולש כ-$\frac12\cdot\frac43\cdot\frac43$ (לא לחתוך אותו עם הריבוע)", r"לשכוח את החילוק ב-$|\Omega|$"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח המשלים $\{X+Y>\frac43\}$ בתוך הריבוע? (משולש בפינה $(1,1)$)", Fr(2, 9),
        r"הישר $x+y=\frac43$ חותך את הצלעות ב-$(1,\frac13)$ וב-$(\frac13,1)$: ניצבי המשולש $\frac23$, שטחו $\frac12\cdot\frac49=\frac29$."),
     NU(r"מהו שטח האירוע $\{X+Y\le\frac43\}$?", Fr(7, 9), r"$1-\frac29=\frac79$, ולכן $P=\frac79$.")])

ADD(1, "ד",
    RB((r"פירוק האירוע $Z<\frac L3$ לפי איזה גפרור קצר יותר (או איחוד $X<\frac L3$ או $Y<\frac L3$)", 2),
       (r"חישוב השטחים: $\frac5{18}L^2$ לכל חלק (או משלים בשטח $\frac49L^2$)", 2), (r"התשובה $\frac59$", 1)),
    [r"לחבר $\frac13+\frac13=\frac23$ ולשכוח שהחיתוך נספר פעמיים", r"לכתוב $\min(X,Y)<c$ כחיתוך (זה $\max$)"],
    [NU(OMEGA, 1, OMEGA_X),
     CH(r"$Z=\min(X,Y)$. איזה תיאור של האירוע $Z<\frac13$ נכון?",
        [r"$X<\frac13$ **או** $Y<\frac13$: איחוד של שתי רצועות", r"$X<\frac13$ **וגם** $Y<\frac13$: ריבוע פינתי",
         r"$X+Y<\frac13$: משולש פינתי"], 0,
        r"המינימום קטן מ-$\frac13$ כאשר לפחות אחד קטן מ-$\frac13$. החיתוך הוא האירוע $\max<\frac13$ (שטח $\frac19$), והמשולש שטחו $\frac1{18}$; שניהם אינם $\frac59$."),
     NU(r"מהו שטח המשלים $\{X\ge\frac13\ \text{and}\ Y\ge\frac13\}$?", Fr(4, 9), r"ריבוע בצלע $\frac23$: שטח $\frac49$."),
     NU(r"מהי $P(Z<\frac13)$?", Fr(5, 9), r"$1-\frac49=\frac59$.")])

ADD(1, "ה",
    RB((r"הגדרת הסתברות מותנית כמנה של שטחים: $\frac{P(Z<\frac L2\cap X>\frac L4)}{P(X>\frac L4)}$", 1),
       (r"המכנה $P(X>\frac L4)=\frac34$", 1), (r"שטח החיתוך $\frac12$ (שני חלקים בני $\frac14$)", 2), (r"התשובה $\frac23$", 1)),
    [r"לחלק ב-$|\Omega|=1$ במקום בשטח התנאי $\frac34$", r"להניח ש-$Z<\frac L2$ ו-$X>\frac L4$ בלתי תלויים ולכפול"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח אזור התנאי $\{X>\frac14\}$ (המכנה, לפני החילוק ב-$|\Omega|$)?", Fr(3, 4), r"רצועה ברוחב $\frac34$: שטח $\frac34$; זה $P(X>\frac14)$."),
     NU(r"מהו שטח החיתוך $\{\min(X,Y)<\frac12\}\cap\{X>\frac14\}$?", Fr(1, 2),
        r"באזור $X>\frac14$ (שטח $\frac34$) מסירים את הפינה $\{X\ge\frac12,Y\ge\frac12\}$ בשטח $\frac14$: נשאר $\frac12$."),
     NU(r"מהי ההסתברות המותנית?", Fr(2, 3), r"$\frac{1/2}{3/4}=\frac23$.")])

# ---- Q2
Q2M1 = [r"מרחב מדגם אחיד סופי: $P=\frac{|A|}{|\Omega|}$ (הגישה הקלאסית)", r"התפלגות גאומטרית: מחכים להופעה הראשונה של הספרה $3$",
        r"התפלגות בינומית $\mathrm{Bin}(10,\frac1{10})$"]
Q2M = [r"ללא החזרה: כל הוצאה מותנית בקודמותיה, ולכן כופלים הסתברויות מותנות (או סופרים סדרות)",
       r"הוצאות בלתי תלויות, כמו $\mathrm{Bin}(n,\frac1{10})$: בכל מקום ההסתברות היא $\frac1{10}$ כי זה ניסוי חוזר",
       r"התפלגות גאומטרית: מחכים להופעה הראשונה של הספרה $3$"]
Q2M_EX = (r"בלי החזרה ההוצאות תלויות: למשל $P(3_2\mid 3_1)=0\ne\frac1{10}$, ולכן הבינומית אינה מתאימה. הגאומטרית נותנת $(\frac9{10})^{k-1}\frac1{10}$ "
          r"(למשל $0.0387$ בהוצאה העשירית, לא $0.1$).")

ADD(2, "א",
    RB((r"מרחב המדגם: 10 ספרות שוות סיכוי, $|\Omega|=10$", 2), (r"מספר התוצאות הנוחות $|A|=1$", 1), (r"התשובה $\frac1{10}$", 2)),
    [r"לבלבל בין מספר הספרות להסתברות ולכתוב $\frac13$"],
    [CH(r"מוציאים ספרה אחת מתוך $10$. איזה מודל מתאים?", Q2M1, 0,
        r"הוצאה בודדת מתוך אוסף שוות-סיכוי היא מרחב אחיד. גאומטרית ובינומית מתארות סדרות של ניסויים חוזרים, ואין כאן סדרה."),
     NU(r"מהי ההסתברות שהספרה שהוצאה היא $3$?", Fr(1, 10), r"$\frac{|A|}{|\Omega|}=\frac1{10}$.")])

ADD(2, "ב",
    RB((r"זיהוי הוצאה ללא החזרה ובחירת כלל המכפלה (התניה בהוצאה הראשונה)", 2), (r"$P(3_1^c)=\frac9{10}$ ואז $P(3_2\mid3_1^c)=\frac19$", 3), (r"התשובה $\frac1{10}$", 2)),
    [r"להניח אי-תלות בין שתי ההוצאות ולכתוב $\frac1{10}\cdot\frac1{10}$ או $\frac9{10}\cdot\frac1{10}$", r"לשכוח שהספרה השנייה יכולה להיות $3$ רק אם הראשונה אינה $3$"],
    [CH(r"מוציאים שתי ספרות ללא החזרה. איזה מודל מתאים לשאלה על הספרה השנייה?", Q2M, 0, Q2M_EX),
     NU(r"מהי ההסתברות שהספרה הראשונה אינה $3$?", Fr(9, 10), r"$9$ ספרות מתוך $10$."),
     NU(r"בהינתן שהראשונה אינה $3$, מהי ההסתברות שהשנייה היא $3$?", Fr(1, 9), r"נותרו $9$ ספרות ו-$3$ ביניהן: $\frac19$."),
     NU(r"מהי $P(3_2)$?", Fr(1, 10), r"$\frac9{10}\cdot\frac19=\frac1{10}$.")])

ADD(2, "ג",
    RB((r"הספרה השלישית היא $3$ רק אם שתי הראשונות אינן $3$", 2), (r"$\frac9{10}\cdot\frac89$ ואז $\frac18$", 3), (r"התשובה $\frac1{10}$", 2)),
    [r"לכפול $\frac9{10}\cdot\frac9{10}\cdot\frac1{10}$ (כאילו עם החזרה)", r"לחשב את ההסתברות ש-$3$ יופיע באחת מהשלוש ולא במקום השלישי דווקא"],
    [CH(r"מוציאים שלוש ספרות ללא החזרה. איזה מודל מתאים?", Q2M, 0, Q2M_EX),
     NU(r"מהי ההסתברות ששתי הספרות הראשונות אינן $3$?", Fr(4, 5), r"$\frac9{10}\cdot\frac89=\frac8{10}$."),
     NU(r"בהינתן ששתיהן אינן $3$, מהי ההסתברות שהשלישית היא $3$?", Fr(1, 8), r"נותרו $8$ ספרות, ביניהן $3$: $\frac18$."),
     NU(r"מהי $P(3_3)$?", Fr(1, 10), r"$\frac45\cdot\frac18=\frac1{10}$.")])

ADD(2, "ד",
    RB((r"כלל המכפלה עם $10$ גורמים, או טיעון סימטריה/ספירה", 3), (r"צמצום המכפלה הטלסקופית $\frac9{10}\cdot\frac89\cdots\frac12\cdot1$", 2), (r"התשובה $\frac1{10}$", 1)),
    [r"לחשב $\left(\frac9{10}\right)^9\frac1{10}$ כאילו הוצאות בלתי תלויות", r"לכתוב $10!$ במקום $9!$ במונה"],
    [CH(r"מוציאים את כל $10$ הספרות ללא החזרה. איזה מודל מתאים?",
        [r"מרחב אחיד על תמורות של $10$ הספרות: סופרים תמורות שבהן $3$ במקום האחרון",
         r"התפלגות גאומטרית: $P=(\frac9{10})^9\cdot\frac1{10}$", r"בינומית $\mathrm{Bin}(10,\frac1{10})$: $P=\frac1{10}$"], 0,
        r"הוצאה ללא החזרה של כל הספרות היא תמורה אקראית. הגאומטרית מניחה אי-תלות, ולכן נותנת $0.0387$; הבינומית סופרת הצלחות ולא מתארת סדר."),
     NU(r"כמה תמורות של $10$ הספרות מסיימות ב-$3$?", 362880, r"שאר $9$ הספרות מסודרות בכל דרך: $9!=362880$."),
     NU(r"כמה תמורות יש בסך הכול?", 3628800, r"$10!=3628800$."),
     NU(r"מהי $P(3_{10})$?", Fr(1, 10), r"$\frac{9!}{10!}=\frac1{10}$.")])

# ---- Q3
Q3M = [r"למנות את ארבעת הצירופים של $(X,Y)$, לחשב $(D,T)$ לכל אחד, ולצרף הסתברות מכפלה (בלתי תלויים)",
       r"$(D,T)$ מתפלג בינומית, כי $T$ סכום של ניסויי ברנולי",
       r"ההסתברות המשותפת היא מכפלת השוליות $P_D(d)P_T(t)$, כי $D$ ו-$T$ נבנו מאותם משתנים בלתי תלויים"]
ADD(3, "א",
    RB((r"פישוט $D=X$ ו-$T=2X-Y$ בעזרת $X^2=X$, $Y^2=Y$", 2), (r"טבלת ארבע התוצאות של $(X,Y)$ עם ערכי $(D,T)$ והסתברויותיהן", 2), (r"הטבלה המשותפת המלאה עם השוליות", 1)),
    [r"להשאיר את $X^2$ בלי לפשט (לברנולי $X^2=X$)", r"לכתוב את המשותפת כמכפלת השוליות (שני המשתנים תלויים באותם $X,Y$)"],
    [CH(r"איך מחשבים את ההסתברות המשותפת של $(D,T)$?", Q3M, 0,
        r"$(D,T)$ היא פונקציה של $(X,Y)$ בלבד, ולכן ממנים את 4 התוצאות. $T=2X-Y$ מקבל גם $-1$ ולכן אינו בינומי; ובטבלה $P(D=0,T=1)=0$ בעוד מכפלת השוליות חיובית."),
     NU(r"מהו $T$ כאשר $X=0$ ו-$Y=1$?", -1, r"$T=2\cdot0-1=-1$ (בדקו גם דרך העקבה של המטריצה)."),
     NU(r"ב-$p=0.3$, מהי $P(D=1,T=2)$?", Fr(21, 100), r"$D=1,T=2$ רק עבור $(X,Y)=(1,0)$: $p(1-p)=0.21$."),
     NU(r"בטבלה המשותפת עם $D\in\{0,1\}$ ו-$T\in\{-1,0,1,2\}$, כמה מתוך $8$ התאים שווים ל-$0$?", 4, r"רק ארבעה תאים אפשריים; ארבעת האחרים $(0,1),(0,2),(1,-1),(1,0)$ הם $0$.")])

ADD(3, "ב",
    RB((r"זיהוי $D=X$", 2), (r"$\mathbb E[D]=p$", 1), (r"$\operatorname{Var}[D]=p(1-p)$", 1)),
    [r"לבלבל עם המקרה $D=XY$ ולכתוב $\mathrm{Ber}(p^2)$"],
    [CH(r"מהי ההתפלגות של $D$?", [r"$\mathrm{Ber}(p)$", r"$\mathrm{Ber}(p^2)$", r"$\mathrm{Bin}(2,p)$"], 0,
        r"$D=X(X-Y)+X^2Y^2=X$ לכל ערך של $Y$, ולכן $D\sim\mathrm{Ber}(p)$; $P(D=1)=p$ ולא $p^2$ (ב-$p=0.3$: $0.3$ מול $0.09$), וגם $D$ אינו מקבל $2$."),
     NU(r"ב-$p=0.3$, מהי $\operatorname{Var}[D]$?", Fr(21, 100), r"$p(1-p)=0.21$.")])

ADD(3, "ג",
    RB((r"$T=2X-Y$ וליניאריות התוחלת: $\mathbb E[T]=p$", 2), (r"אי-תלות: $\operatorname{Var}[T]=4\operatorname{Var}[X]+\operatorname{Var}[Y]$", 2)),
    [r"לכתוב $\operatorname{Var}[2X-Y]=2\operatorname{Var}[X]-\operatorname{Var}[Y]$ (השונות של $-Y$ היא חיובית)"],
    [CH(r"איזה ביטוי נכון עבור $\operatorname{Var}[2X-Y]$ כש-$X,Y$ בלתי תלויים?",
        [r"$4\operatorname{Var}[X]+\operatorname{Var}[Y]$", r"$2\operatorname{Var}[X]-\operatorname{Var}[Y]$", r"$(2-1)^2\operatorname{Var}[X]$"], 0,
        r"$\operatorname{Var}[aX+bY]=a^2\operatorname{Var}[X]+b^2\operatorname{Var}[Y]$. הביטוי השני הוא כמעט תמיד שגוי (ב-$p=0.3$: $0.21\ne1.05$), והשלישי מניח $Y=X$."),
     NU(r"ב-$p=0.3$, מהי $\mathbb E[T]$?", Fr(3, 10), r"$2p-p=p=0.3$."),
     NU(r"ב-$p=0.3$, מהי $\operatorname{Var}[T]$?", Fr(21, 20), r"$5p(1-p)=5\cdot0.21=1.05$.")])

ADD(3, "ד",
    RB((r"$\operatorname{Cov}=\mathbb E[DT]-\mathbb E[D]\mathbb E[T]$", 1), (r"$\mathbb E[DT]=\mathbb E[X(2X-Y)]=2p-p^2$ (שימוש ב-$X^2=X$ ובאי-התלות)", 2), (r"התשובה $2p(1-p)$", 1)),
    [r"לכתוב $\mathbb E[X^2]=p^2$ במקום $p$", r"להסיק $\operatorname{Cov}=0$ מאי-התלות של $X,Y$ (אבל $D,T$ תלויים)"],
    [NU(r"ב-$p=0.3$, מהי $\mathbb E[DT]$?", Fr(51, 100), r"$\mathbb E[X(2X-Y)]=2p-p^2=0.6-0.09=0.51$."),
     NU(r"ב-$p=0.3$, מהו המכפלה $\mathbb E[D]\,\mathbb E[T]$?", Fr(9, 100), r"$p\cdot p=0.09$."),
     NU(r"ב-$p=0.3$, מהי $\operatorname{cov}[D,T]$?", Fr(21, 50), r"$0.51-0.09=0.42=2p(1-p)$.")])

ADD(3, "ה",
    RB((r"זיהוי תא אפס בטבלה המשותפת: $P(D=0,T=1)=0$", 2), (r"השוואה למכפלת השוליות החיובית $(1-p)p^2$", 1), (r"מסקנה: תלויים", 1)),
    [r"לבדוק תא אחד שבו המכפלה במקרה שווה ולהסיק אי-תלות", r"להסיק אי-תלות מכך ש-$X,Y$ בלתי תלויים"],
    [NU(r"מהי $P(D=0,T=1)$? ($D=X$, ו-$T=1$ רק כש-$X=Y=1$.)", 0, r"אם $D=0$ אז $X=0$, ואז $T=-Y\le0$, ולכן $T=1$ בלתי אפשרי."),
     NU(r"ב-$p=0.3$, מהו המכפלה $P(D=0)\,P(T=1)$?", Fr(63, 1000), r"$0.7\cdot0.09=0.063>0$."),
     CH(r"האם $D$ ו-$T$ בלתי תלויים?", [r"לא: $P(D=0,T=1)=0\ne P(D=0)P(T=1)>0$", r"כן, כי $X$ ו-$Y$ בלתי תלויים"], 0,
        r"אי-תלות של $X,Y$ אינה גוררת אי-תלות של פונקציות שונות של שניהם יחד; מספיק תא אחד שבו המשותפת שונה ממכפלת השוליות.")])

ADD(3, "ו",
    RB((r"חישוב $\operatorname{Cov}[D,T]=2p(1-p)$ (מהסעיף הקודם)", 2), (r"$\operatorname{Cov}\ne0$ עבור $0<p<1$, ולכן מתואמים", 2)),
    [r"להניח שתלות גוררת מתאם ולהיפך"],
    [NU(r"ב-$p=0.3$, מהי $\operatorname{cov}[D,T]$?", Fr(21, 50), r"$2p(1-p)=0.42$."),
     CH(r"איזו טענה על תלות ומתאם נכונה תמיד?",
        [r"בלתי תלויים $\Rightarrow$ בלתי מתואמים", r"בלתי מתואמים $\Rightarrow$ בלתי תלויים", r"בלתי תלויים $\Leftrightarrow$ בלתי מתואמים"], 0,
        r"אי-תלות גוררת $\operatorname{Cov}=0$, אך לא להיפך (דוגמה: $X$ סימטרי ו-$X^2$). לכן $\operatorname{Cov}\ne0$ כאן מראה גם תלות.")])

# ---- Q4
ADD(4, "א",
    RB((r"נרמול: סכום שטחי שני המשולשים והמלבן שווה $1$, ולכן $b=1$", 3), (r"תוחלת: שני האינטגרלים הראשונים מתבטלים והשלישי $\frac{b^2-a^2}2$", 4), (r"פתרון $a=\frac12$, $b=1$", 3)),
    [r"לרשום את הצפיפות על $(-a,0)$ כ-$\frac za$ (היא $-\frac za$, אי-שלילית)", r"לשכוח שהשטח מתחת למשולש השמאלי נספר בנרמול"],
    [CH(r"אילו תנאים קובעים את שני הפרמטרים $a,b$?",
        [r"נרמול $\int f=1$ ביחד עם הנתון $\mathbb E[Z]=\frac38$", r"נרמול בלבד", r"הנתון $\mathbb E[Z]=\frac38$ בלבד"], 0,
        r"יש שני נעלמים ולכן שתי משוואות. נרמול לבדו נותן $b=1$ לכל $a$; התוחלת $\frac{1-a^2}2$ משתנה עם $a$ ולכן היא שקובעת אותו."),
     NU(r"מהו $b$? (שטח המשולשים $\frac a2+\frac a2$ בתוספת מלבן ברוחב $b-a$ וגובה $1$ שווה $1$.)", 1, r"$a+(b-a)=b=1$."),
     NU(r"עם $b=1$, התוחלת היא $\frac{1-a^2}2=\frac38$. מהו $a^2$?", Fr(1, 4), r"$1-a^2=\frac34$."),
     NU(r"מהו $a$?", Fr(1, 2), r"$a>0$ ולכן $a=\frac12$.")])

ADD(4, "ב",
    RB((r"אינטגרציה של הצפיפות על כל קטע: $-2z$, $2z$ ו-$1$", 4), (r"$F(t)$ על ארבעת הקטעים, כולל $\frac14$ בנקודה $0$", 4), (r"שרטוט הגרף (רציף, עולה, מ-$0$ ל-$1$)", 2)),
    [r"לשכוח את ההסתברות $\frac14$ שנצברה לפני $0$ ולרשום $F(t)=t^2$ ב-$(0,\frac12)$", r"לא לוודא ש-$F$ רציפה בנקודות החיבור"],
    [NU(r"מהי $F_Z(0)=P(Z\le0)$? (שטח המשולש השמאלי)", Fr(1, 4), r"$\int_{-1/2}^0(-2z)\,dz=\frac14$."),
     CH(r"איזו נוסחה נכונה ל-$F_Z(t)$ עבור $0\le t<\frac12$?", [r"$\frac14+t^2$", r"$t^2$", r"$\frac14-t^2$", r"$2t$"], 0,
        r"$F(t)=F(0)+\int_0^t2z\,dz=\frac14+t^2$. הנוסחה $t^2$ שוכחת את המסה שלפני $0$; $\frac14-t^2$ היא הנוסחה ל-$t<0$."),
     NU(r"מהי $F_Z(\frac14)$?", Fr(5, 16), r"$\frac14+\frac1{16}=\frac5{16}$."),
     NU(r"מהי $F_Z(\frac34)$? (על $[\frac12,1)$ מתקיים $F=t$.)", Fr(3, 4), r"$F(\frac12)=\frac12$, והצפיפות $1$ מוסיפה $\frac14$.")])

ADD(4, "ג",
    RB((r"הגדרת ההסתברות המותנית כמנה של הפרשי $F$", 1), (r"המכנה $P(|Z|<\frac12)=F(\frac12)-F(-\frac12)=\frac12$", 2), (r"המונה $F(\frac12)-F(\frac14)=\frac3{16}$", 1), (r"התשובה $\frac38$", 1)),
    [r"לחלק ב-$P(Z>\frac14)$ במקום ב-$P(|Z|<\frac12)$", r"לשכוח שהאירוע $\{Z>\frac14\}\cap\{|Z|<\frac12\}$ הוא $\{\frac14<Z<\frac12\}$"],
    [NU(r"מהי $P(|Z|<\frac12)=F(\frac12)-F(-\frac12)$? (המכנה)", Fr(1, 2), r"$\frac12-0=\frac12$."),
     NU(r"מהי $P(\frac14<Z<\frac12)=F(\frac12)-F(\frac14)$? (המונה)", Fr(3, 16), r"$\frac12-\frac5{16}=\frac3{16}$."),
     NU(r"מהי ההסתברות המותנית?", Fr(3, 8), r"$\frac{3/16}{1/2}=\frac38$.")])

# ---- Q5 (sizes 2, 3, 7 as the sample: N=3, n=12)
Q5SZ = r"נדגים עם $N=3$ משפחות בגדלים $2,3,7$ (סך הכול $n=12$ משתתפים)."
ADD(5, "א",
    RB((r"כל משפחה נבחרת בהסתברות $\frac1N$ (בחירה אחידה של משפחה)", 4), (r"טבלת ההתפלגות של $X$", 3), (r"$\mathbb E[X]=\frac{n_1+\cdots+n_N}N$", 3)),
    [r"לשקלל את המשפחות לפי גודלן (זו שאלה ב')"],
    [CH(r"בוחרים **משפחה** באקראי. מהי $P(X=n_i)$?", [r"$\frac1N$", r"$\frac{n_i}{n_1+\cdots+n_N}$", r"$\frac{n_i}{N}$"], 0,
        r"המדגם הוא משפחה, כולן שוות סיכוי: $\frac1N$. $\frac{n_i}{n}$ הוא הכלל למשתתף שנבחר (גודל ממושקל), ו-$\frac{n_i}N$ אינו אפילו התפלגות (סכומו אינו $1$)."),
     NU(Q5SZ + r" מהי $P(X=7)$?", Fr(1, 3), r"$\frac1N=\frac13$."),
     NU(r"באותו מדגם, מהי $\mathbb E[X]$?", 4, r"$\frac{2+3+7}3=4$.")])

ADD(5, "ב",
    RB((r"זיהוי שבחירת משתתף נותנת משפחה $i$ בהסתברות $\frac{n_i}{n}$", 4), (r"טבלת ההתפלגות של $Y$", 3), (r"$\mathbb E[Y]=\frac{\sum n_i^2}{\sum n_i}$", 3)),
    [r"להשתמש שוב ב-$\frac1N$ ולקבל $\mathbb E[Y]=\mathbb E[X]$", r"לחשב $\sum n_i\cdot\frac{n_i}{N}$ (מחלק שגוי)"],
    [CH(r"בוחרים **משתתף** באקראי ו-$Y$ הוא גודל משפחתו. מהי $P(Y=n_i)$?", [r"$\frac{n_i}{n_1+\cdots+n_N}$", r"$\frac1N$", r"$\frac{n_i^2}{n_1^2+\cdots+n_N^2}$"], 0,
        r"המשפחה $i$ מכילה $n_i$ משתתפים מתוך $n$ ולכן נבחרת בהסתברות $\frac{n_i}n$: משפחות גדולות מיוצגות יתר על המידה. $\frac1N$ הוא כלל המשפחה, והשלישי אינו מתאים לספירת משתתפים."),
     NU(Q5SZ + r" מהי $P(Y=7)$?", Fr(7, 12), r"$\frac7{12}$."),
     NU(r"באותו מדגם, מהי $\mathbb E[Y]$?", Fr(31, 6), r"$\frac{2^2+3^2+7^2}{12}=\frac{62}{12}=\frac{31}6$.")])

ADD(5, "ג",
    RB((r"$\mathbb E[Y]=\frac{\mathbb E[X^2]}{\mathbb E[X]}$", 2), (r"$\frac{\mathbb E[Y]}{\mathbb E[X]}=1+\frac{\operatorname{Var}[X]}{(\mathbb E[X])^2}$", 2), (r"מסקנה: $\mathbb E[Y]\ge\mathbb E[X]$ (ושוויון רק כש-$\operatorname{Var}=0$)", 1)),
    [r"להסיק שהממוצעים שווים כי 'שניהם גודל משפחה'", r"לשכוח ש-$\operatorname{Var}\ge0$ ולטעות בכיוון"],
    [NU(Q5SZ + r" מהי $\operatorname{Var}[X]$?", Fr(14, 3), r"$\mathbb E[X^2]=\frac{4+9+49}3=\frac{62}3$, ו-$\frac{62}3-16=\frac{14}3$."),
     NU(r"באותו מדגם, מהו היחס $\frac{\mathbb E[Y]}{\mathbb E[X]}$?", Fr(31, 24), r"$\frac{31/6}{4}=\frac{31}{24}=1+\frac{14/3}{16}$."),
     CH(r"מה נכון לגבי $\mathbb E[Y]$ ו-$\mathbb E[X]$?",
        [r"$\mathbb E[Y]\ge\mathbb E[X]$ תמיד, ושוויון רק כש-$\operatorname{Var}[X]=0$", r"$\mathbb E[Y]=\mathbb E[X]$ תמיד", r"$\mathbb E[Y]<\mathbb E[X]$ תמיד"], 0,
        r"$\frac{\mathbb E[Y]}{\mathbb E[X]}=1+\frac{\operatorname{Var}[X]}{(\mathbb E[X])^2}\ge1$. בדוגמה היחס $\frac{31}{24}>1$, ולכן שתי הטענות האחרות נכשלות.")])

# ---- Q6
Q6M1 = [r"טור של $D$ עם מקבץ: ענף ($A$ בטור $B$) מקביל ל-$C$", r"מקבץ מקבילי של $A,B,C$ בטור עם $D$",
        r"טור של $A,B,C,D$"]
ADD(6, "א",
    RB((r"קריאת המעגל: $Q_1=\bigl((A\cap B)\cup C\bigr)\cap D$", 3), (r"$P\bigl((A\cap B)\cup C\bigr)=p^2+p-p^3$ (הכלה והפרדה, בלתי תלויים)", 3), (r"הכפלה ב-$P(D)$: $p^2(1+p-p^2)$", 3)),
    [r"לחשב $P((A\cap B)\cup C)=p^2+p$ ולשכוח להחסיר את החיתוך", r"להחליף בין טור למקביל"],
    [CH(r"איזה ביטוי מתאר את $Q_1$ לפי האיור?", Q6M1, 0,
        r"האיור: $D$ בטור לפני מקבץ ששני ענפיו הם $A{-}B$ בטור ו-$C$ לבד. אפשרות ב' מניחה שלושה ענפים מקבילים, ואפשרות ג' מחייבת את כל הרכיבים."),
     NU(r"ב-$p=0.6$, מהי ההסתברות שהמקבץ $(A\cap B)\cup C$ פועל?", Fr(93, 125), r"$p^2+p-p^3=0.36+0.6-0.216=0.744$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_1)$?", Fr(279, 625), r"$0.6\cdot0.744=0.4464$.")])

Q6M2 = [r"ל-$Q_1$ ו-$Q_2$ יחידות משותפות, ולכן לא מכפילים: מתנים ביחידה משותפת ($A$) ומשתמשים בהסתברות שלמה",
        r"$P(Q_1\cap Q_2)=P(Q_1)\,P(Q_2)$, כי הם שני מעגלים נפרדים",
        r"$P(Q_1\cap Q_2)=P(Q_1)+P(Q_2)$"]
ADD(6, "ב",
    RB((r"זיהוי שהמעגלים תלויים (יחידות משותפות) והתניה ב-$A$", 2), (r"$A$ פועל: $\tilde Q=D\cap(B\cup C)$, ההסתברות $p^2(2-p)$", 3), (r"$A$ אינו פועל: $\tilde Q=D\cap C\cap E\cap B$, ההסתברות $p^3q$", 2), (r"הסתברות שלמה וצמצום: $p^3[1+(1-p)(1+q)]$", 2)),
    [r"להכפיל $P(Q_1)P(Q_2)$ למרות היחידות המשותפות", r"לשכוח את $D$ שנדרש בשני המעגלים"],
    [CH(r"איך מחשבים את $P(Q_1\cap Q_2)$?", Q6M2, 0,
        r"בשני המעגלים מופיעות $A,B,D$, ולכן אין אי-תלות. בנקודה $p=0.6,q=0.5$: המכפלה $0.4464\cdot0.432=0.1928$, אבל הערך הנכון $0.3456$; והסכום גדול מ-$0.8$ ואינו הסתברות של חיתוך."),
     NU(r"ב-$p=0.6$: בהינתן ש-$A$ פועל, מהי $P(Q_1\cap Q_2)$? ($Q_2$ פועל אם $D$ פועל, ו-$Q_1$ דורש $D\cap(B\cup C)$.)", Fr(63, 125), r"$p(2p-p^2)=0.6\cdot0.84=0.504$."),
     NU(r"ב-$p=0.6$, $q=0.5$: בהינתן ש-$A$ אינו פועל, מהי $P(Q_1\cap Q_2)$? (נדרש $D\cap C\cap E\cap B$)", Fr(27, 250), r"$p^3q=0.216\cdot0.5=0.108$."),
     NU(r"באותם ערכים, מהי $P(Q_1\cap Q_2)$?", Fr(216, 625), r"$0.6\cdot0.504+0.4\cdot0.108=0.3024+0.0432=0.3456$.")])

ADD(6, "ג",
    RB((r"הגדרת הסתברות מותנית: $\frac{P(Q_1\cap Q_2)}{P(Q_1)}$", 2), (r"שימוש בתוצאות הסעיפים הקודמים לחישוב המונה והמכנה", 3), (r"פישוט ל-$p\cdot\frac{1+(1-p)(1+q)}{1+(1-p)p}$", 2)),
    [r"לחלק ב-$P(Q_2)$ במקום ב-$P(Q_1)$ (התנאי הוא $Q_1$)", r"לטעות בהצבה ולקבל הסתברות גדולה מ-$1$"],
    [NU(r"ב-$p=0.6$, $q=0.5$: מהי $P(Q_1)$? (המכנה: אירוע התנאי)", Fr(279, 625), r"$0.4464$ מסעיף א."),
     NU(r"באותם ערכים, מהי $P(Q_1\cap Q_2)$? (המונה)", Fr(216, 625), r"$0.3456$ מסעיף ב."),
     NU(r"מהי $P(Q_2\mid Q_1)$?", Fr(216, 279), r"$\frac{0.3456}{0.4464}=\frac{24}{31}\approx0.7742$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = "ai-draft"
        _q["stepsSource"] = "ai-draft"


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
