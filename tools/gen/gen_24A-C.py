# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-C.json -- probability (course 20021), semester A 2024, moed C (27.05.2024).
6 questions, 20 items (Q1 4, Q2 5, Q3 6, Q4 3, Q5 3, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-C.py

Source: exam pp.1-3, official handwritten solutions pp.4-14.
Transcription notes
- Part keys are single letters. Q2 prints ג-1, ג-2, ג-3 -> keys ג ד ה (a=א, b=ב, c=ג-1, d=ג-2, e=ג-3).
  Q5 prints ב-1 twice (the second is a misprint for ב-2) -> keys א ב ג; the printed label is the bold token that
  starts each question text (ב-2 for the second).
- Q3(ה,ו): the official solution is only the word "כן"; the one-line reason added is read off the official joint
  table / official Cov formula.
- Q1 area items carry `region` (area figure) and, with the other numeric parts, `sim`: see EXTRAS near the end.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-C.json"
CODE = "24A-C"
IMG = "images/exams/24A-C-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"נתבונן במשולש ה״הגדול״ הבנוי על קודקודים $(0,0)$, $(0,1)$ ו-$(1,0)$. תהי $O$ נקודה אקראית בעלת שיעורים $X$ ו-$Y$ "
          r"אשר מהווים משתנים מקריים בלתי תלויים בעלי התפלגות אחידה $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,1)$." "\n"
          r"כאשר נקודה $O$ נמצאת בתוך המשולש ה״הגדול״, נוצרים שלושה משולשים קטנים משורטטים באיור. נסמן באמצעות "
          r"$S_1,S_2,S_3$ את שטחי המשולשים הללו.")

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א.** מהי ההסתברות שנקודה $O$ נמצאת בתוך המשולש ה״הגדול״?",
    r"""$$P(O\in\Delta)=P(Y\le 1-X)=\frac{|\{Y\le 1-x\}|}{|\Omega|}=\frac{1/2}{1}=\frac12.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**ב.** אם ידוע כי נקודה $O$ נמצאת בתוך המשולש ה״הגדול״, מהי ההסתברות ש-$S_1<\frac13$?",
    r"""$S_1=\dfrac X2$.
$$P\left(S_1<\tfrac13\,\Big/\,O\in\Delta\right)=P\left(\tfrac X2<\tfrac13\,\Big/\,Y\le 1-X\right)=\frac{P\left(X<\frac23\cap Y\le 1-X\right)}{P(Y\le 1-X)}=\frac{\left|\{x<\frac23\cap y\le 1-x\}\right|}{1/2}$$
$$=2\left(\frac12-\frac12\cdot\frac13\cdot\frac13\right)=\frac89.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**ג.** אם ידוע כי נקודה $O$ נמצאת בתוך המשולש ה״הגדול״, מהי ההסתברות ש-$S_1+S_2>\frac13$?",
    r"""$S_1=\dfrac X2,\ S_2=\dfrac Y2$.
$$P\left(S_1+S_2>\tfrac13\,\Big/\,O\in\Delta\right)=\frac{P\left(\frac{X+Y}{2}>\frac13\cap Y\le 1-X\right)}{P(Y\le 1-X)}=\frac{\left|\{y>\frac23-x\cap y\le 1-x\}\right|}{1/2}$$
$$=2\left(\frac12-\frac12\cdot\frac23\cdot\frac23\right)=1-\frac49=\frac59.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"**ד.** אם ידוע כי נקודה $O$ נמצאת בתוך המשולש ה״הגדול״, מהי ההסתברות ש-$S_3>S_1$?",
    r"""$S_3=\dfrac12-S_1-S_2=\dfrac12-\dfrac{X+Y}{2}=\dfrac{1-X-Y}{2}$.
$$P\left(S_3>S_1\,/\,O\in\Delta\right)=\frac{P\left(\frac{1-X-Y}{2}>\frac X2\cap Y\le 1-X\right)}{P(Y\le 1-X)}=2\left|\{y<1-2x\cap y\le 1-x\}\right|$$
$$=2\cdot\frac12\cdot 1\cdot\frac12=\frac12.$$""",
    4, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_TXT = r"בקובייה **לא מאוזנת**, $P(1)=P(3)=P(5)=q$ וגם $P(2)=P(4)=P(6)=2q$."

questions.append(Q(
    2, "א", "discrete_rv",
    Q2_TXT + "\n" + r"**א.** מצאו את $q$.",
    r"""$3q+3\cdot 2q=1\ \Rightarrow\ q=\dfrac19.$""",
    5))

questions.append(Q(
    2, "ב", "combinatorics",
    Q2_TXT + "\n" + r"**ב.** מטילים קובייה **לא מאוזנת זו פעמיים** ומסכמים את התוצאות. מהי ההסתברות שסכום התוצאות יהיה שווה ל-5?",
    r"""$A$ = ״סכום שתי ההטלות שווה ל-5״ $=\{14,23,32,41\}$.
$$P(A)=P(1)P(4)+P(2)P(3)+P(3)P(2)+P(4)P(1)=q\cdot 2q+2q\cdot q+q\cdot 2q+2q\cdot q=8q^2=\frac{8}{81}.$$""",
    5))

Q2C = Q2_TXT + "\n" + r"מטילים קובייה **לא מאוזנת זו שלוש פעמים** ומסכמים את התוצאות."

questions.append(Q(
    2, "ג", "combinatorics",
    Q2C + "\n" + r"**ג-1:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-5?",
    r"""$B$ = ״סכום שלוש ההטלות שווה ל-5״ $=\{113,131,311,122,212,221\}$.
$$P(B)=3\,P(1)P(1)P(3)+3\,P(1)P(2)P(2)=3q^3+3q(2q)^2=15q^3=\frac{15}{9^3}=\frac{5}{243}.$$""",
    5))

questions.append(Q(
    2, "ד", "conditional_bayes",
    Q2C + "\n" + r"**ג-2:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-5 **אם ידוע** כי סכום של שתי התוצאות הראשונות היה שווה ל-2?",
    r"""$C$ = ״סכום שתי התוצאות הראשונות שווה ל-2״ $=\{11\_\}$, $B\cap C=\{113\}$.
$$P(B/C)=\frac{P(B\cap C)}{P(C)}=\frac{P(1)P(1)P(3)}{P(1)P(1)}=P(3)=q=\frac19.$$""",
    5))

questions.append(Q(
    2, "ה", "conditional_bayes",
    Q2C + "\n" + r"**ג-3:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-5 **אם ידוע** כי התוצאה הראשונה הייתה קטנה מהתוצאה השנייה?",
    r"""$D$ = ״התוצאה הראשונה קטנה מהשנייה״ $=\{12\_,13\_,14\_,15\_,16\_,23\_,24\_,25\_,26\_,34\_,35\_,36\_,45\_,46\_,56\_\}$.
$B\cap D=\{131,122\}\ \Rightarrow\ P(B\cap D)=P(1)P(3)P(1)+P(1)P(2)P(2)=q^3+q(2q)^2=5q^3$.
$P(D)=2q^2\cdot 9+q^2\cdot 3+(2q)^2\cdot 3=33q^2$.
$$P(B/D)=\frac{P(B\cap D)}{P(D)}=\frac{5q^3}{33q^2}=\frac{5}{33}q=\frac{5}{297}.$$""",
    5))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"נתבונן במטריצת ברנולי מהצורה $\boldsymbol{Q}=\begin{pmatrix}-1&-X^2\\Y^2&X+Y\end{pmatrix}$ כאשר $X$ ו-$Y$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגויות ברנולי: "
          r"$X\sim\mathrm{Ber}(p)$ ו-$Y\sim\mathrm{Ber}(q)$. נגדיר שני משתנים מקריים חדשים: דטרמיננטה $D=\det\boldsymbol Q$ ועקבה $T=\operatorname{tr}\boldsymbol Q$ של מטריצה $\boldsymbol Q$.")

questions.append(Q(
    3, "א", "joint_discrete",
    r"**א.** חשבו את פונקציית ההסתברות המשותפת של משתנה מקרי דו ממדי $(D,T)$.",
    r"""$D=\det\boldsymbol Q=-X-Y+X^2Y^2=XY-X-Y$, $\ T=\operatorname{tr}\boldsymbol Q=X+Y-1$.
| $(X,Y)$ | $(0,0)$ | $(0,1)$ | $(1,0)$ | $(1,1)$ |
|---|---|---|---|---|
| $D$ | $0$ | $-1$ | $-1$ | $-1$ |
| $T$ | $-1$ | $0$ | $0$ | $1$ |

הערכים האפשריים: $D=-1,0$ ו-$T=-1,0,1$.

| $D\backslash T$ | $-1$ | $0$ | $1$ | $p_D(d)$ |
|---|---|---|---|---|
| $-1$ | $0$ | $p+q-2pq$ | $pq$ | $p+q-pq$ |
| $0$ | $(1-p)(1-q)$ | $0$ | $0$ | $1-p-q+pq$ |
| $p_T(t)$ | $1-p-q+pq$ | $p+q-2pq$ | $pq$ | $1$ |""",
    5, contextId="c3"))

questions.append(Q(
    3, "ב", "joint_discrete",
    r"**ב.** חשבו תוחלת $\mathbb E[D]$ ושונות $\operatorname{var}[D]$ של דטרמיננטה.",
    r"""$$\mathbb E[D]=(-1)(p+q-pq)=pq-p-q.$$
$\mathbb E[D^2]=1\cdot(p+q-pq)$, ולכן
$$\operatorname{Var}(D)=p+q-pq-(p+q-pq)^2.$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ג", "joint_discrete",
    r"**ג.** חשבו תוחלת $\mathbb E[T]$ ושונות $\operatorname{var}[T]$ של עקבה.",
    r"""$$\mathbb E[T]=(-1)(1-p-q+pq)+1\cdot pq=p+q-1.$$
$\mathbb E[T^2]=(-1)^2(1-p-q+pq)+pq=1-p-q+2pq$, ולכן
$$\operatorname{Var}(T)=1-p-q+2pq-(1-p-q)^2=p(1-p)+q(1-q).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ד", "joint_discrete",
    r"**ד.** חשבו את השונות המשותפת $\operatorname{cov}[D,T]$.",
    r"""$\operatorname{Cov}[D,T]=\mathbb E[DT]-\mathbb E[D]\,\mathbb E[T]$.
$\mathbb E[DT]=(-1)\cdot 1\cdot pq=-pq$, ולכן
$$\operatorname{Cov}[D,T]=-pq-(pq-p-q)(p+q-1).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ה", "independence",
    r"**ה.** האם המשתנים $D$ ו-$T$ בלתי תלויים? **נמקו היטב!**",
    r"""**לא, הם תלויים.** לפי הטבלה המשותפת $P(D=0,T=0)=0$, בעוד ש-$P(D=0)\,P(T=0)=(1-p)(1-q)(p+q-2pq)>0$ (עבור $0<p,q<1$).""",
    4, contextId="c3"))

questions.append(Q(
    3, "ו", "independence",
    r"**ו.** האם המשתנים $D$ ו-$T$ בלתי מתואמים? **נמקו היטב!**",
    r"""**לא, הם מתואמים:** $\operatorname{Cov}[D,T]=-pq-(pq-p-q)(p+q-1)=-(p+q)(1-p)(1-q)\ne 0$ (עבור $0<p,q<1$).""",
    4, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_TXT = r"לפניך גרף עבור פונקציית צפיפות ההסתברות $f_X(x)$ של משתנה מקרי $X$ בעל תוחלת $\mathbb E[X]=\frac{23}{24}$."

questions.append(Q(
    4, "א", "continuous_rv",
    Q4_TXT + "\n" + r"**א.** מצאו את הפרמטרים $a$ ו-$b$.",
    r"""נרמול: $\dfrac a2+(b-a)=1\ \Rightarrow\ b-\dfrac a2=1$.
תוחלת:
$$\mathbb E[X]=\int_0^a x\cdot\frac xa\,dx+\int_a^b x\cdot 1\,dx=\frac{a^2}{3}+\frac{b^2-a^2}{2}=\frac{b^2}{2}-\frac{a^2}{6}=\frac{23}{24}\ \Rightarrow\ 3b^2-a^2=\frac{23}{4}.$$
פותרים את שתי המשוואות יחד: $a=2b-2$, ולכן
$$3b^2-(2b-2)^2=\frac{23}{4}\ \Rightarrow\ b^2-8b+\frac{39}{4}=0\ \Rightarrow\ b=\frac32\ \ \mathrm{or}\ \ b=\frac{13}{2},$$
כלומר $a=1$ או $a=11$. מכיוון ש-$a<b$ מתקבל
$$a=1,\qquad b=\frac32.$$""",
    10, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ב", "continuous_rv",
    Q4_TXT + "\n" + r"**ב.** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו גרף של $F_X(t)$ אשר משקף את התוצאות החישוב.",
    r"""$$F_X(t)=\int_{-\infty}^t f_X(x)\,dx=\begin{cases}0,&t<0,\\ \dfrac{t^2}{2},&0\le t<1,\\ t-\dfrac12,&1\le t<\dfrac32,\\ 1,&t\ge\dfrac32.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת](images/exams/24A-C-Q4-cdf.png)""",
    10, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ג", "continuous_rv",
    Q4_TXT + "\n" + r"**ג.** מהי ההסתברות $P\left(X\le\frac54\,\big/\,X>\frac12\right)$?",
    r"""$$P\left(X\le\tfrac54\,\Big/\,X>\tfrac12\right)=\frac{P\left(\frac12<X\le\frac54\right)}{P\left(X>\frac12\right)}=\frac{F_X\left(\frac54\right)-F_X\left(\frac12\right)}{1-F_X\left(\frac12\right)}=\frac{\left(\frac54-\frac12\right)-\frac18}{1-\frac18}=\frac57.$$""",
    5, image=IMG + "Q4-pdf.png"))

# ------------------------------------------------------------------ Q5
Q5_TXT = (r"לפניך אוסף של $N$ כדורים, בינהם $D$ כדורים אדומים ו-$(N-D)$ כדורים שחורים. נתבונן בשני ניסויים נפרדים:" "\n"
          r"**ניסוי א׳:** מהאוסף מוצאים באקראי **ועם החזרה** $n$ כדורים. נגדיר משתנה מקרי $X$ המתאר את מספר הכדורים האדומים בין שנלקחו מהאוסף." "\n"
          r"**ניסוי ב׳:** מטילים **מטבע מוטה** עד קבלת תוצאת ״עץ״ **בפעם הראשונה**: אם תוצאת ״עץ״ התקבלה בהטלה הראשונה – מוצאים מהאוסף כדור אחד; "
          r"אם תוצאת ״עץ״ התקבלה בהטלה השנייה – מוצאים מהאוסף שני כדורים **(עם החזרה)**; אם תוצאת ״עץ״ התקבלה בהטלה השלישית – מוצאים מהאוסף שלושה כדורים **(עם החזרה)** וכן הלאה." "\n"
          r"יהי $Z$ משתנה מקרי המתאר את מספר הכדורים האדומים בין כל אלה שהוצאו עם החזרה מהאוסף, בהנחה שההסתברות ל״עץ״ בהטלה בודדת שווה ל-$p$.")
Q5_HINT = (r"**הערה:** לידיעתך, עבור $0\le a<1$ מתקיים:" "\n"
           r"$$\sum_{j=m}^{\infty}C_j^m a^j=\frac{a^m}{(1-a)^{m+1}}.$$")

questions.append(Q(
    5, "א", "special_discrete",
    r"**ניסוי א׳:** איך משתנה מקרי $X$ מפולג? **נמקו היטב!**",
    r"""$X\sim\mathrm{Bin}\left(n,\,Q=\dfrac DN\right)$ (כל הוצאה עם החזרה היא ניסוי ברנולי בלתי תלוי, שהסתברות ההצלחה בו, כלומר כדור אדום, היא $Q=D/N$).
$$P(X=k)=\binom nk Q^k(1-Q)^{n-k},\qquad k=0,1,\dots,n.$$""",
    15, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    r"**ב-1:** חשבו את ההסתברות $P(Z=0)$ שבין הכדורים שהוצאו אין אף כדור אדום.",
    r"""נגדיר משתנה מקרי $Y=\{$מספר הכדורים שהוצאו מהאוסף עם החזרה$\}$, כלומר מספר ההטלות עד העץ הראשון. אז $Y\sim G(p)$:
$$P(Y=j)=p(1-p)^{j-1},\qquad j=1,2,\dots$$
בהינתן $Y=j$ מתקיים $Z\sim\mathrm{Bin}(j,Q)$ עם $Q=D/N$.
$$P(Z=0)=\sum_{j=1}^{\infty}P(Z=0/Y=j)P(Y=j)=\sum_{j=1}^{\infty}(1-Q)^j\,p(1-p)^{j-1}=p(1-Q)\sum_{j=1}^{\infty}\bigl[(1-Q)(1-p)\bigr]^{j-1}=\frac{p(1-Q)}{1-(1-Q)(1-p)}.$$
כלומר
$$P(Z=0)=\frac{p(1-Q)}{p(1-Q)+Q}\Bigg|_{Q=D/N}.$$""",
    5, contextId="c5"))

questions.append(Q(
    5, "ג", "special_discrete",
    r"**ב-2:** חשבו את ההסתברות $P(Z=k)$ שבין הכדורים שהוצאו ישנם בדיוק $k$ כדורים אדומים ($k\ge 1$)." "\n" + Q5_HINT,
    r"""$$P(Z=k)=\sum_{j=k}^{\infty}P(Z=k/Y=j)P(Y=j)=\sum_{j=k}^{\infty}\binom jk Q^k(1-Q)^{j-k}\,p(1-p)^{j-1}=\frac{Q^k}{(1-Q)^k}\cdot\frac{p}{1-p}\sum_{j=k}^{\infty}\binom jk\bigl[(1-Q)(1-p)\bigr]^j.$$
לפי הנוסחה שבהערה, עם $m=k$ ו-$a=(1-Q)(1-p)$, הסכום שווה ל-$\dfrac{(1-Q)^k(1-p)^k}{[p(1-Q)+Q]^{k+1}}$. לכן
$$P(Z=k)=\frac{Q^k}{(1-Q)^k}\cdot\frac p{1-p}\cdot\frac{(1-Q)^k(1-p)^k}{[p(1-Q)+Q]^{k+1}},$$
$$P(Z=k)=\frac{p}{1-p}\cdot\frac{1}{p(1-Q)+Q}\cdot\left(\frac{Q(1-p)}{p(1-Q)+Q}\right)^k,\qquad k=1,2,\dots$$
(סדרה גאומטרית). בדיקה שסכום ההסתברויות שווה ל-1:
$$\sum_{k=0}^{\infty}P(Z=k)=P(Z=0)+\frac{p}{1-p}\cdot\frac1{p(1-Q)+Q}\sum_{k=1}^\infty\left(\frac{Q(1-p)}{p(1-Q)+Q}\right)^k=\frac{p(1-Q)}{p(1-Q)+Q}+\frac{Q}{p(1-Q)+Q}=1.$$""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_TXT = r"סטודנט של המכון הטכנולוגי חולון הרכיב מעגל $Q_1$ חשמלי מחמש יחידות $A,B,C,D$ ו-$E$ הפועלות ללא תלות אחת בשנייה בהסתברויות זהות $p$."

questions.append(Q(
    6, "א", "circuits",
    r"**א.** מהי ההסתברות שמעגל $Q_1$ פעיל?",
    r"""מתנים ב-$E$ (פעיל או לא פעיל):
$$P(Q_1)=(2p-p^2)^2\,p+(2p^2-p^4)(1-p)=\bigl(2+2p-5p^2+2p^3\bigr)p^2.$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"**ב-1:** לאחר פירוק של מעגל $Q_1$, סטודנט הרכיב מעגל חדש $Q_2$ מאותן יחידות. מהי ההסתברות שמעגל $Q_2$ יפעל?",
    r"""$$P(Q_2)=(2p-p^2)\bigl[1-(1-p)^3\bigr]=6p^2-9p^3+5p^4-p^5.$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    r"**ב-2:** אם ידוע שמעגל $Q_2$ פעיל, מהי ההסתברות שגם המעגל המקורי $Q_1$ פעיל?",
    r"""$$P(Q_1/Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}.$$
נסמן $\tilde Q=Q_1\cap Q_2$ (המעגל $Q_1$ בטור עם $Q_2$, מאותן יחידות) ונחשב בהתניה על הזוג $A,B$:
$$P(Q_1\cap Q_2)=P(\tilde Q/A\cap B)P(A\cap B)+P(\tilde Q/\bar A\cap\bar B)P(\bar A\cap\bar B)+P(\tilde Q/A\cap\bar B)P(A\cap\bar B)+P(\tilde Q/\bar A\cap B)P(\bar A\cap B).$$
- $P(\tilde Q/A\cap B)=1-(1-p)^3$ (כש-$A,B$ פעילים, $Q_1$ פעיל, ו-$Q_2$ פעיל אם לפחות אחד מ-$C,D,E$ פעיל), וההסתברות לכך $p^2$;
- $P(\tilde Q/\bar A\cap\bar B)=0$, וההסתברות לכך $(1-p)^2$;
- $P(\tilde Q/A\cap\bar B)=p(2p-p^2)$ (חייב $D$ פעיל, ואז $E\cup C$ פעיל), וההסתברות לכך $p(1-p)$;
- $P(\tilde Q/\bar A\cap B)=p(2p-p^2)$ (חייב $C$ פעיל, ואז $E\cup D$ פעיל), וההסתברות לכך $p(1-p)$.

לכן
$$P(Q_1\cap Q_2)=p^2\bigl[1-(1-p)^3\bigr]+2p(1-p)\cdot p(2p-p^2)=3p^5-9p^4+7p^3.$$
ולכן
$$P(Q_1/Q_2)=\frac{p^3(7-9p+3p^2)}{p^2(6-9p+5p^2-p^3)}=\frac{p\,(7-9p+3p^2)}{6-9p+5p^2-p^3}.$$""",
    7, contextId="c6"))

exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ד, מועד ג (27.05.2024)",
    "year": 2024,
    "examDate": "27.05.2024",
    "sourceFile": "24A-C exam pp.1-3",
    "solutionFile": "24A-C official handwritten solutions pp.4-14",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: משולש ונקודה אקראית", "image": IMG + "Q1-triangle.png", "caption": Q1_TXT},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_TXT},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_TXT},
        "c6": {"kind": "image", "title": "שאלה 6: מעגלים", "image": IMG + "Q6-circuits.png", "caption": Q6_TXT},
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
    (1, "א"): {"region": REG([lin(1, 1, 1, "<=")], 1 / 2, "המשולש ה״גדול״: Y<=1-X"),
               "sim": AREA("P(O in big triangle)", 1 / 2)},
    (1, "ב"): {"region": REG([lin(1, 0, "2/3", "<")], 8 / 9, "האירוע S1<1/3, כלומר X<2/3, בהינתן המשולש הגדול",
                             given=[lin(1, 1, 1, "<=")]),
               "sim": AREA("P(S1<1/3 | O in triangle)", 8 / 9)},
    (1, "ג"): {"region": REG([lin(1, 1, "2/3", ">")], 5 / 9, "האירוע S1+S2>1/3, כלומר X+Y>2/3, בהינתן המשולש הגדול",
                             given=[lin(1, 1, 1, "<=")]),
               "sim": AREA("P(S1+S2>1/3 | O in triangle)", 5 / 9)},
    (1, "ד"): {"region": REG([lin(2, 1, 1, "<")], 1 / 2, "האירוע S3>S1, כלומר Y<1-2X, בהינתן המשולש הגדול",
                             given=[lin(1, 1, 1, "<=")]),
               "sim": AREA("P(S3>S1 | O in triangle)", 1 / 2)},
    (2, "ב"): {"sim": DICE("P(sum = 5), biased die", 8 / 81, 2, "sum == 5", weights=[1, 2, 1, 2, 1, 2])},
    (2, "ג"): {"sim": DICE("P(sum = 5), biased die", 5 / 243, 3, "sum == 5", weights=[1, 2, 1, 2, 1, 2])},
    (2, "ד"): {"sim": DICE("P(sum = 5 | d1+d2 = 2)", 1 / 9, 3, "sum == 5", "d1+d2 == 2", weights=[1, 2, 1, 2, 1, 2])},
    (2, "ה"): {"sim": DICE("P(sum = 5 | d1<d2)", 5 / 297, 3, "sum == 5", "d1 < d2", weights=[1, 2, 1, 2, 1, 2])},
    (4, "ג"): {"sim": PDF("P(X<=5/4 | X>1/2)", 5 / 7, [(0, 1, "x"), (1, "3/2", "1")], "x <= 5/4", "x > 1/2")},
}
for _q in questions:
    _x = EXTRAS.get((_q["num"], _q.get("part")))
    if _x:
        _q.update(_x)


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
