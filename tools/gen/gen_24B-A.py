# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-A.json -- probability (course 20021), semester B 2024, moed A (16.07.2024).
6 questions, 24 items (Q1 5, Q2 4, Q3 6, Q4 3, Q5 3, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-A.py

Source: exam pp.1-3, handwritten official solutions pp.4-11 (grid paper).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, a-3, b-1, b-2; stored as a b c d e (the printed label is the
  first bold token of each question text). Map: Q1 a=א-1, b=א-2, c=א-3, d=ב-1, e=ב-2.
- Math never holds Hebrew.
- Q1 area items (c, d, e) have region data in tools/verify/24B-A/regions.json (no `region` field in RAW_SCHEMA).
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

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
