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


# ---- extra sims for items with symbolic answers, at sample parameter values (stated in `estimate`)
def _bern2(p, q):
    return {"X": {"values": [0, 1], "probs": [1 - p, p]}, "Y": {"values": [0, 1], "probs": [1 - q, q]}}


_DET = "-X-Y+X^2*Y^2"      # det Q straight from the matrix entries
_TR = "-1+X+Y"
_BR = {"edges": [{"id": "A", "from": "L", "to": "T", "p": 0.6}, {"id": "B", "from": "T", "to": "R", "p": 0.6},
                 {"id": "C", "from": "L", "to": "U", "p": 0.6}, {"id": "D", "from": "U", "to": "R", "p": 0.6},
                 {"id": "E", "from": "T", "to": "U", "p": 0.6}], "source": "L", "sink": "R"}
_Q1E = "(A and B) or (C and D) or (A and E and D) or (C and E and B)"
_Q2E = "(A or B) and (C or D or E)"
_NT = 30      # the number of tosses is truncated at 30 (tail mass 0.5^30 goes to the last value)


def _compound(Z_event, p, Q):
    probs = [p * (1 - p) ** (j - 1) for j in range(1, _NT + 1)]
    probs[-1] += 1 - sum(probs)
    vs = {"Y": {"values": list(range(1, _NT + 1)), "probs": probs}}
    for i in range(1, _NT + 1):
        vs["B%d" % i] = {"values": [0, 1], "probs": [1 - Q, Q]}
    z = "+".join("B%d*(Y>=%d)" % (i, i) for i in range(1, _NT + 1))
    return {"vars": vs, "event": "(" + z + ")" + Z_event}


_V = _bern2(0.3, 0.6)
EXTRA_SIMS = {
    (3, "א"): {"kind": "custom_discrete", "estimate": "P(D=-1, T=0) ב-p=0.3, q=0.6", "exact": 0.54,
               "params": {"vars": _V, "event": _DET + " == -1 and " + _TR + " == 0"}},
    (3, "ב"): {"kind": "custom_discrete", "estimate": "Var[D] ב-p=0.3, q=0.6", "exact": 0.2016,
               "params": {"vars": _V, "measure": "var", "expr": _DET}},
    (3, "ג"): {"kind": "custom_discrete", "estimate": "Var[T] ב-p=0.3, q=0.6", "exact": 0.45,
               "params": {"vars": _V, "measure": "var", "expr": _TR}},
    (3, "ד"): {"kind": "custom_discrete", "estimate": "cov[D,T] ב-p=0.3, q=0.6", "exact": -0.252,
               "params": {"vars": _V, "measure": "cov", "expr": [_DET, _TR]}},
    (3, "ה"): {"kind": "custom_discrete", "estimate": "P(D=0, T=0) ב-p=0.3, q=0.6", "exact": 0,
               "params": {"vars": _V, "event": _DET + " == 0 and " + _TR + " == 0"}},
    (3, "ו"): {"kind": "custom_discrete", "estimate": "cov[D,T] ב-p=0.3, q=0.6", "exact": -0.252,
               "params": {"vars": _V, "measure": "cov", "expr": [_DET, _TR]}},
    (4, "א"): {"kind": "pdf", "estimate": "E[X] ב-a=1, b=3/2", "exact": 23 / 24,
               "params": {"pieces": [{"from": 0, "to": 1, "expr": "x"}, {"from": 1, "to": "3/2", "expr": "1"}],
                          "measure": "mean", "expr": "x"}},
    (4, "ב"): PDF("F(6/5)", 0.7, [(0, 1, "x"), (1, "3/2", "1")], "x <= 6/5"),
    (5, "א"): {"kind": "urn", "estimate": "P(X=2) ב-D=2, N=5, n=4 (Q=0.4)", "exact": 0.3456,
               "params": {"counts": {"red": 2, "black": 3}, "draws": 4, "replace": True, "event": "red == 2"}},
    (5, "ב"): {"kind": "custom_discrete", "estimate": "P(Z=0) ב-p=0.5, Q=0.4 (קטוע ב-30 הטלות)", "exact": 3 / 7,
               "params": _compound(" == 0", 0.5, 0.4)},
    (5, "ג"): {"kind": "custom_discrete", "estimate": "P(Z=2) ב-p=0.5, Q=0.4 (קטוע ב-30 הטלות)", "exact": 40 / 343,
               "params": _compound(" == 2", 0.5, 0.4)},
    (6, "א"): {"kind": "circuit", "estimate": "P(Q1) ב-p=0.6", "exact": 0.65952, "params": dict(_BR, event="S")},
    (6, "ב"): {"kind": "circuit", "estimate": "P(Q2) ב-p=0.6", "exact": 0.78624,
               "params": {"event": "S", "network": {"type": "series", "children": [
                   {"type": "parallel", "children": [{"type": "comp", "id": "A", "p": 0.6}, {"type": "comp", "id": "B", "p": 0.6}]},
                   {"type": "parallel", "children": [{"type": "comp", "id": "C", "p": 0.6}, {"type": "comp", "id": "D", "p": 0.6},
                                                     {"type": "comp", "id": "E", "p": 0.6}]}]}}},
    (6, "ג"): {"kind": "circuit", "estimate": "P(Q1 | Q2) ב-p=0.6", "exact": 0.57888 / 0.78624,
               "params": dict(_BR, event=_Q1E, given=_Q2E)},
}
for _q in questions:
    _x = EXTRA_SIMS.get((_q["num"], _q.get("part")))
    if _x and "sim" not in _q:
        _q["sim"] = _x


# ---- rubric / pitfalls / steps (ai-draft). Every expected value is re-derived independently, by exact arithmetic and
# by Monte Carlo, in tools/verify/24A-C/steps_check.py (which reads the generated raw JSON).
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


OMEGA = r"נקודה אקראית $(X,Y)$ בריבוע היחידה. מהו שטח מרחב המדגם $|\Omega|$ (הריבוע, לא המשולש)?"
OMEGA_X = r"מרחב המדגם הוא הריבוע $(0,1)^2$ ושטחו $1$ (המשולש ה״גדול״ הוא רק אירוע בתוכו, ושטחו $\frac12$)."
S3S = r"$S_1=\frac X2,\ S_2=\frac Y2,\ S_3=\frac{1-X-Y}2$. "
PDELTA = r"מהי $P(O\in\Delta)$, כלומר שטח המשולש הגדול $\{Y\le1-X\}$? (אירוע התנאי, המכנה)"
PDELTA_X = r"חצי מהריבוע: $\frac12$. זהו המכנה בכל סעיף מותנה."

ADD(1, "א",
    RB((r"גישה גאומטרית: ההסתברות היא שטח המשולש חלקי $|\Omega|$, כאשר $\Omega$ הוא ריבוע היחידה", 3), (r"האירוע $Y\le1-X$ הוא חצי הריבוע, שטחו $\frac12$", 3), (r"התשובה $\frac12$", 1)),
    [r"לחשב את שטח המשולש כ-$1$ (ולא $\frac12$) או לחלק ב-$\frac12$ בטעות"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהו שטח המשולש $\{Y\le1-X\}$ בתוך הריבוע?", Fr(1, 2), r"משולש ישר-זווית בניצבים $1$: $\frac12$, ולכן $P=\frac{1/2}{1}=\frac12$.")])

ADD(1, "ב",
    RB((r"תרגום $S_1<\frac13\iff X<\frac23$", 1), (r"הסתברות מותנית כמנה של שטחים; המכנה $P(O\in\Delta)=\frac12$", 2), (r"שטח החיתוך $\frac12-\frac12\cdot\frac19=\frac49$", 3), (r"התשובה $\frac89$", 1)),
    [r"לחלק את שטח החיתוך ב-$|\Omega|=1$ ולא ב-$\frac12$", r"לחשב את שטח המשולש הקטן כ-$\frac12\cdot\frac23\cdot\frac23$ (הניצבים הם $\frac13$)"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(PDELTA, Fr(1, 2), PDELTA_X),
     CH(S3S + r"איזה תנאי שקול ל-$S_1<\frac13$?", [r"$X<\frac23$", r"$X<\frac16$", r"$X<\frac13$"], 0,
        r"$\frac X2<\frac13\iff X<\frac23$. התנאים האחרים נותנים הסתברויות מותנות $\frac{11}{36}$ ו-$\frac59$, לא $\frac89$."),
     NU(r"מהו שטח החיתוך $\{X<\frac23\}\cap\Delta$?", Fr(4, 9), r"$\frac12$ פחות המשולש הקטן $\{x\ge\frac23,\ y\le1-x\}$ בניצבים $\frac13$ ושטחו $\frac1{18}$: $\frac49$."),
     NU(r"מהי ההסתברות המותנית $P(S_1<\frac13\mid O\in\Delta)$?", Fr(8, 9), r"$\frac{4/9}{1/2}=\frac89$.")])

ADD(1, "ג",
    RB((r"תרגום $S_1+S_2>\frac13\iff X+Y>\frac23$", 1), (r"המכנה $\frac12$", 1), (r"שטח החיתוך $\frac12-\frac12\left(\frac23\right)^2=\frac5{18}$", 3), (r"התשובה $\frac59$", 2)),
    [r"לשכוח את הגורם $2$ במעבר מ-$\frac{X+Y}2>\frac13$ ל-$X+Y>\frac23$", r"לחלק ב-$|\Omega|=1$ במקום ב-$\frac12$"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(PDELTA, Fr(1, 2), PDELTA_X),
     CH(S3S + r"איזה תנאי שקול ל-$S_1+S_2>\frac13$?", [r"$X+Y>\frac23$", r"$X+Y>\frac16$", r"$X+Y>\frac13$"], 0,
        r"$\frac{X+Y}2>\frac13\iff X+Y>\frac23$. התנאים האחרים נותנים הסתברויות מותנות $\frac{35}{36}$ ו-$\frac89$, לא $\frac59$."),
     NU(r"מהו שטח החיתוך $\{X+Y>\frac23\}\cap\Delta$?", Fr(5, 18), r"$\frac12$ פחות המשולש $\{X+Y\le\frac23\}$ בניצבים $\frac23$ ושטחו $\frac29$: $\frac5{18}$."),
     NU(r"מהי ההסתברות המותנית?", Fr(5, 9), r"$\frac{5/18}{1/2}=\frac59$.")])

ADD(1, "ד",
    RB((r"$S_3=\frac{1-X-Y}2$ ו-$S_3>S_1\iff Y<1-2X$", 2), (r"המכנה $\frac12$ ושטח האזור $\{y<1-2x\}$ הוא $\frac14$", 2)),
    [r"לתרגם את $S_3>S_1$ ל-$Y<1-X$ (זה תנאי המשולש עצמו)"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(PDELTA, Fr(1, 2), PDELTA_X),
     CH(S3S + r"איזה תנאי שקול ל-$S_3>S_1$?", [r"$Y<1-2X$", r"$Y<1-X$", r"$Y<2-X$"], 0,
        r"$\frac{1-X-Y}2>\frac X2\iff Y<1-2X$. התנאים $Y<1-X$ ו-$Y<2-X$ מתקיימים בכל המשולש (הסתברות מותנית $1$)."),
     NU(r"מהו שטח $\{Y<1-2X\}$? (אינו חורג מהמשולש הגדול)", Fr(1, 4), r"משולש $(0,0),(\frac12,0),(0,1)$: $\frac12\cdot\frac12\cdot1=\frac14$."),
     NU(r"מהי ההסתברות המותנית $P(S_3>S_1\mid O\in\Delta)$?", Fr(1, 2), r"$\frac{1/4}{1/2}=\frac12$.")])

# ---- Q2 (biased die: P(1)=P(3)=P(5)=q, P(2)=P(4)=P(6)=2q, q=1/9)
Q2M = [r"קובייה לא מאוזנת: ההטלות בלתי תלויות, ולכן כופלים הסתברויות של כל תוצאה (לא מרחב אחיד)",
       r"מרחב אחיד על $6^k$ תוצאות: $P=\frac{|A|}{6^k}$", r"התפלגות בינומית"]
Q2M_EX = r"הקובייה אינה מאוזנת, ולכן התוצאות אינן שוות סיכוי ואין לספור ולחלק (למשל $P(\text{sum}=5)=\frac{8}{81}\ne\frac4{36}$). הבינומית סופרת הצלחות ואינה נותנת סכום."
ADD(2, "א",
    RB((r"הסכום $3q+3\cdot2q=9q$ חייב להיות $1$", 3), (r"$q=\frac19$", 2)),
    [r"להניח $q=\frac16$ כמו בקובייה מאוזנת"],
    [CH(r"איזה תנאי קובע את $q$?", [r"סכום ההסתברויות של כל הפאות שווה $1$", r"$P(1)=\frac16$, כי יש שש פאות", r"התוחלת היא $3.5$"], 0,
        r"ההסתברויות של פונקציית הסתברות מסתכמות ל-$1$ בלבד. $P(1)=\frac16$ נכון רק לקובייה מאוזנת, ו-$3.5$ אינה נתונה."),
     NU(r"בכמה $q$ מסתכם $P(1)+\dots+P(6)$? ($3\cdot q+3\cdot 2q$)", 9, r"$9q=1$."),
     NU(r"מהו $q$?", Fr(1, 9), r"$q=\frac19$.")])

ADD(2, "ב",
    RB((r"הסתברות כל זוג סדור היא מכפלה (בלתי תלויות), לא $\frac1{36}$", 2), (r"האירוע $\{14,23,32,41\}$: כל זוג בהסתברות $2q^2$", 2), (r"$8q^2=\frac8{81}$", 1)),
    [r"לספור $\frac4{36}$ כמו בקובייה מאוזנת", r"לשכוח שאי-זוגי נותן $q$ וזוגי נותן $2q$"],
    [CH(r"איזה מודל מתאים לסכום שתי הטלות של הקובייה הלא-מאוזנת?", Q2M, 0, Q2M_EX),
     NU(r"מהי $P(\text{first}=1,\ \text{second}=4)$?", Fr(2, 81), r"$q\cdot2q=2q^2=\frac2{81}$."),
     NU(r"מהי $P(\text{sum}=5)$?", Fr(8, 81), r"ארבעה זוגות בני $2q^2$ כל אחד: $8q^2=\frac8{81}$.")])

ADD(2, "ג",
    RB((r"מונים את הסדרות הסדורות: $113,131,311,122,212,221$", 2), (r"$P(113)=q^3$ ו-$P(122)=q(2q)^2=4q^3$", 2), (r"$3q^3+3\cdot4q^3=15q^3=\frac5{243}$", 1)),
    [r"לשכוח את התמורות (פי $3$) של כל צירוף", r"להשתמש ב-$\frac{|B|}{6^3}$"],
    [CH(r"איזה מודל מתאים לסכום שלוש הטלות של הקובייה הלא-מאוזנת?", Q2M, 0, Q2M_EX),
     NU(r"כמה סדרות סדורות של שלוש הטלות נותנות סכום $5$?", 6, r"$\{1,1,3\}$ ב-$3$ סדרים ו-$\{1,2,2\}$ ב-$3$ סדרים."),
     NU(r"מהי ההסתברות של הסדרה $(1,2,2)$ (ב-$q=\frac19$)?", Fr(4, 729), r"$q\cdot2q\cdot2q=4q^3=\frac4{729}$."),
     NU(r"מהי $P(\text{sum}=5)$?", Fr(5, 243), r"$3\cdot\frac1{729}+3\cdot\frac4{729}=\frac{15}{729}=\frac5{243}$.")])

ADD(2, "ד",
    RB((r"אירוע התנאי $C=\{X_1=X_2=1\}$ והחיתוך $B\cap C=\{113\}$", 2), (r"$P(B/C)=\frac{P(1)P(1)P(3)}{P(1)P(1)}=P(3)$ (אי-תלות)", 2), (r"התשובה $q=\frac19$", 1)),
    [r"לחלק ב-$P(B)$ במקום ב-$P(C)$", r"להשתמש ב-$\frac16$ כאילו הקובייה מאוזנת"],
    [CH(r"נתון ששתי ההטלות הראשונות נתנו סכום $2$. מהי ההסתברות לסכום $5$ בשלוש ההטלות?",
        [r"$P(X_3=3)=q$: ההטלה השלישית בלתי תלויה בראשונות", r"$P(B)=\frac5{243}$, כי הנתון אינו משנה", r"$\frac16$, הקובייה הוגנת"], 0,
        r"סכום $2$ בשתי הטלות מחייב $(1,1)$ ואז נדרש $X_3=3$. $P(B)\approx0.0206$ אינו התשובה (הנתון משנה), ו-$\frac16$ שגוי כי הקובייה אינה הוגנת."),
     NU(r"מהי $P(C)$, ההסתברות לסכום $2$ בשתי ההטלות? (התנאי)", Fr(1, 81), r"רק $(1,1)$: $q^2=\frac1{81}$."),
     NU(r"מהי $P(B\cap C)$, כלומר $(1,1,3)$?", Fr(1, 729), r"$q^3=\frac1{729}$."),
     NU(r"מהי $P(B/C)$?", Fr(1, 9), r"$\frac{1/729}{1/81}=\frac19=q$.")])

ADD(2, "ה",
    RB((r"אירוע התנאי $D=\{X_1<X_2\}$ ו-$P(D)=33q^2$ (חישוב על זוגות)", 2), (r"$P(B\cap D)=5q^3$ מהסדרות $131,122$", 2), (r"התשובה $\frac5{33}q=\frac5{297}$", 1)),
    [r"להניח ש-$B$ ו-$D$ בלתי תלויים", r"לספור את $D$ כ-$\frac{15}{36}$ (הקובייה אינה מאוזנת)"],
    [CH(r"נתון שהתוצאה הראשונה קטנה מהשנייה. מהי ההסתברות לסכום $5$ בשלוש ההטלות?",
        [r"מנה של שני חישובים: $\frac{P(B\cap D)}{P(D)}$", r"$P(B)=\frac5{243}$, כי $D$ והסכום בלתי תלויים", r"$\frac19$, הערך מהסעיף הקודם"], 0,
        r"$D$ ו-$B$ תלויים (למשל $D$ פוסל את $221$ ו-$311$), ולכן $\frac5{297}\approx0.0168\ne P(B)\approx0.0206$. הערך $\frac19$ שייך לתנאי אחר."),
     NU(r"מהי $P(D)=P(X_1<X_2)$ ב-$q=\frac19$? (סכום מכפלות על $15$ הזוגות)", Fr(33, 81), r"$33q^2=\frac{33}{81}=\frac{11}{27}$."),
     NU(r"מהי $P(B\cap D)$, סכום $5$ וגם $X_1<X_2$ (הסדרות $131,122$)?", Fr(5, 729), r"$q^3+4q^3=5q^3=\frac5{729}$."),
     NU(r"מהי $P(B/D)$?", Fr(5, 297), r"$\frac{5q^3}{33q^2}=\frac{5q}{33}=\frac5{297}$.")])

# ---- Q3 (matrix; X~Ber(p), Y~Ber(q); samples p=0.3, q=0.6)
Q3M = [r"למנות את ארבעת הצירופים של $(X,Y)$, לחשב $(D,T)$ לכל אחד, ולצרף הסתברות מכפלה (בלתי תלויים)",
       r"$(D,T)$ מתפלג בינומית דו-ממדית, כי $T$ סכום ניסויי ברנולי",
       r"ההסתברות המשותפת היא מכפלת השוליות $P_D(d)P_T(t)$, כי $D$ ו-$T$ נבנו מאותם משתנים בלתי תלויים"]
ADD(3, "א",
    RB((r"פישוט $D=XY-X-Y$ ו-$T=X+Y-1$ ($X^2=X$)", 2), (r"טבלת ארבע התוצאות של $(X,Y)$ עם $(D,T)$ והסתברויות מכפלה", 2), (r"הטבלה המשותפת המלאה והשוליות", 1)),
    [r"לא לפשט את $X^2Y^2$", r"להחליף בין $p$ ל-$q$ בהסתברויות התוצאות"],
    [CH(r"איך מחשבים את ההסתברות המשותפת של $(D,T)$?", Q3M, 0,
        r"$(D,T)$ היא פונקציה של $(X,Y)$ בלבד: ממנים 4 תוצאות. $T$ מקבל את הערך $-1$, ולכן אינו בינומי; ובטבלה $P(D=0,T=0)=0$ אך מכפלת השוליות חיובית."),
     NU(r"מהו $D=\det\boldsymbol Q$ כאשר $X=Y=1$?", -1, r"$\boldsymbol Q=\begin{pmatrix}-1&-1\\1&2\end{pmatrix}$, דטרמיננטה $-2+1=-1$."),
     NU(r"ב-$p=0.3$, $q=0.6$: מהי $P(D=-1,T=0)$? ($(X,Y)=(0,1)$ או $(1,0)$)", Fr(27, 50), r"$(1-p)q+p(1-q)=0.42+0.12=0.54$."),
     NU(r"בטבלה עם $D\in\{-1,0\}$ ו-$T\in\{-1,0,1\}$, כמה מתוך $6$ התאים שווים ל-$0$?", 3, r"אפשריים רק $(0,-1),(-1,0),(-1,1)$; האחרים $(0,0),(0,1),(-1,-1)$ הם $0$.")])

ADD(3, "ב",
    RB((r"$D=-1$ בכל מקרה מלבד $X=Y=0$, ולכן $P(D=-1)=p+q-pq$", 2), (r"$\mathbb E[D]=pq-p-q$", 1), (r"$\operatorname{Var}[D]=(p+q-pq)-(p+q-pq)^2$", 1)),
    [r"לכתוב $\mathbb E[D^2]=(\mathbb E[D])^2$", r"להחסיר את $\mathbb E[D]$ בלי לרבע"],
    [NU(r"ב-$p=0.3$, $q=0.6$: מהי $P(D=-1)$? ($D=0$ רק כש-$X=Y=0$)", Fr(18, 25), r"$1-(1-p)(1-q)=1-0.28=0.72$."),
     NU(r"מהי $\mathbb E[D]$ באותם ערכים?", Fr(-18, 25), r"$-1\cdot0.72=-0.72$."),
     NU(r"מהי $\operatorname{Var}[D]$ באותם ערכים?", Fr("0.2016"), r"$\mathbb E[D^2]=0.72$, ולכן $0.72-0.72^2=0.2016$.")])

ADD(3, "ג",
    RB((r"$\mathbb E[T]=p+q-1$", 1), (r"$T=X+Y-1$ ואי-תלות: $\operatorname{Var}[T]=\operatorname{Var}[X]+\operatorname{Var}[Y]$", 2), (r"התשובה $p(1-p)+q(1-q)$", 1)),
    [r"להחסיר את $1$ גם מהשונות", r"להניח $\operatorname{Var}[X]=\operatorname{Var}[Y]$"],
    [CH(r"איזה ביטוי נכון עבור $\operatorname{Var}[X+Y-1]$ כש-$X,Y$ בלתי תלויים?",
        [r"$\operatorname{Var}[X]+\operatorname{Var}[Y]$", r"$\operatorname{Var}[X]+\operatorname{Var}[Y]-1$", r"$\operatorname{Var}[X]\cdot\operatorname{Var}[Y]$"], 0,
        r"קבוע אינו משפיע על שונות, והשונויות מתחברות לבלתי תלויים. ב-$p=0.3,q=0.6$: $0.45$; האפשרות השנייה נותנת $-0.55$ (שונות שלילית), והשלישית $0.0504$."),
     NU(r"ב-$p=0.3$, $q=0.6$: מהי $\mathbb E[T]$?", Fr(-1, 10), r"$0.3+0.6-1=-0.1$."),
     NU(r"באותם ערכים, מהי $\operatorname{Var}[T]$?", Fr(9, 20), r"$0.3\cdot0.7+0.6\cdot0.4=0.21+0.24=0.45$.")])

ADD(3, "ד",
    RB((r"$\operatorname{Cov}=\mathbb E[DT]-\mathbb E[D]\mathbb E[T]$", 1), (r"$\mathbb E[DT]=-pq$ (רק התוצאה $X=Y=1$ נותנת מכפלה שונה מאפס)", 2), (r"הצבה וצמצום: $-(p+q)(1-p)(1-q)$", 1)),
    [r"לשכוח את הסימן השלילי של $D$", r"לחשב $\mathbb E[DT]$ על כל ארבע התוצאות ולטעות באחת"],
    [NU(r"ב-$p=0.3$, $q=0.6$: מהי $\mathbb E[DT]$? ($DT\ne0$ רק ב-$X=Y=1$, שם $D=-1$, $T=1$)", Fr(-9, 50), r"$-pq=-0.18$."),
     NU(r"באותם ערכים, מהו המכפלה $\mathbb E[D]\,\mathbb E[T]$?", Fr(9, 125), r"$(-0.72)(-0.1)=0.072$."),
     NU(r"מהי $\operatorname{cov}[D,T]$?", Fr(-63, 250), r"$-0.18-0.072=-0.252=-(p+q)(1-p)(1-q)$.")])

ADD(3, "ה",
    RB((r"תא אפס: $P(D=0,T=0)=0$", 2), (r"מכפלת השוליות $P(D=0)P(T=0)=(1-p)(1-q)(p+q-2pq)>0$", 1), (r"מסקנה: תלויים", 1)),
    [r"להסיק אי-תלות מכך ש-$X,Y$ בלתי תלויים"],
    [NU(r"מהי $P(D=0,T=0)$? ($D=0$ רק ב-$X=Y=0$, ושם $T=-1$)", 0, r"האירועים זרים."),
     NU(r"ב-$p=0.3$, $q=0.6$: מהו המכפלה $P(D=0)\,P(T=0)$?", Fr(1512, 10000), r"$0.28\cdot0.54=0.1512>0$."),
     CH(r"האם $D$ ו-$T$ בלתי תלויים?", [r"לא: $P(D=0,T=0)=0\ne P(D=0)P(T=0)$", r"כן, כי $X$ ו-$Y$ בלתי תלויים"], 0,
        r"מספיק תא אחד שבו המשותפת שונה ממכפלת השוליות.")])

ADD(3, "ו",
    RB((r"$\operatorname{Cov}[D,T]=-(p+q)(1-p)(1-q)$", 2), (r"שונה מאפס עבור $0<p,q<1$: מתואמים", 2)),
    [r"להניח שתלות גוררת מתאם ולהיפך"],
    [NU(r"ב-$p=0.3$, $q=0.6$: מהי $\operatorname{cov}[D,T]$?", Fr(-63, 250), r"$-(0.9)(0.7)(0.4)=-0.252$."),
     CH(r"איזו טענה על תלות ומתאם נכונה תמיד?",
        [r"בלתי תלויים $\Rightarrow$ בלתי מתואמים", r"בלתי מתואמים $\Rightarrow$ בלתי תלויים", r"בלתי תלויים $\Leftrightarrow$ בלתי מתואמים"], 0,
        r"אי-תלות גוררת $\operatorname{Cov}=0$ אך לא להיפך. כאן $\operatorname{Cov}\ne0$, ולכן $D,T$ מתואמים ובפרט תלויים.")])

# ---- Q4 (pdf: x/a on [0,a], 1 on [a,b]; E[X]=23/24)
ADD(4, "א",
    RB((r"נרמול: $\frac a2+(b-a)=1\Rightarrow a=2b-2$", 3), (r"תוחלת: $\frac{b^2}2-\frac{a^2}6=\frac{23}{24}$", 3), (r"פתרון המשוואה הריבועית $b^2-8b+\frac{39}4=0$", 2), (r"דחיית $b=\frac{13}2$ ($a=11>b$): $a=1$, $b=\frac32$", 2)),
    [r"לרשום את התוחלת של הקטע הראשון כ-$\int_0^ax\cdot\frac1a\,dx$", r"לשכוח לדחות את השורש שנותן $a>b$"],
    [CH(r"אילו תנאים קובעים את $a,b$?", [r"נרמול $\int f=1$ ביחד עם הנתון $\mathbb E[X]=\frac{23}{24}$", r"נרמול בלבד", r"התוחלת בלבד"], 0,
        r"שני נעלמים דורשים שתי משוואות: הנרמול נותן את $a=2b-2$, והתוחלת קובעת את $b$."),
     NU(r"הצבת $a=2b-2$ במשוואת התוחלת נותנת $b^2-8b+\frac{39}4=0$. מהו השורש הקטן יותר?", Fr(3, 2), r"השורשים $\frac32$ ו-$\frac{13}2$."),
     NU(r"מהו $a=2b-2$ עבור השורש שנבחר?", 1, r"$a=2\cdot\frac32-2=1$ (השורש $\frac{13}2$ נותן $a=11>b$, בלתי אפשרי)."),
     NU(r"בדיקה: מהי $\mathbb E[X]=\frac{b^2}2-\frac{a^2}6$ עבור $a=1$, $b=\frac32$?", Fr(23, 24), r"$\frac98-\frac16=\frac{23}{24}$.")])

ADD(4, "ב",
    RB((r"$F=\frac{t^2}2$ על $[0,1)$", 3), (r"$F=t-\frac12$ על $[1,\frac32)$ (רציפות ב-$1$)", 4), (r"שרטוט הגרף", 3)),
    [r"לרשום $F(t)=t$ בקטע השני בלי הקבוע", r"לא לוודא ש-$F(\frac32)=1$"],
    [NU(r"מהי $F_X(1)=P(X\le1)$?", Fr(1, 2), r"$\int_0^1x\,dx=\frac12$."),
     CH(r"איזו נוסחה נכונה ל-$F_X(t)$ עבור $1\le t<\frac32$? (נבדוק ב-$t=1.25$)", [r"$t-\frac12$", r"$t$", r"$\frac{t^2}2$"], 0,
        r"$F(t)=\frac12+(t-1)=t-\frac12$ (ב-$1.25$: $0.75$). $F=t$ נותנת $1.25>1$, והנוסחה $\frac{t^2}2$ שייכת לקטע הראשון ($0.78$)."),
     NU(r"מהי $F_X(1.2)$?", Fr(7, 10), r"$1.2-0.5=0.7$.")])

ADD(4, "ג",
    RB((r"הסתברות מותנית כמנה של הפרשי $F$", 1), (r"המכנה $P(X>\frac12)=1-F(\frac12)=\frac78$", 2), (r"המונה $F(\frac54)-F(\frac12)=\frac58$", 1), (r"התשובה $\frac57$", 1)),
    [r"לחלק ב-$P(X\le\frac54)$ במקום ב-$P(X>\frac12)$", r"להשתמש ב-$F=\frac{t^2}2$ גם ב-$t=\frac54$"],
    [NU(r"מהי $P(X>\frac12)=1-F(\frac12)$? (אירוע התנאי, המכנה)", Fr(7, 8), r"$F(\frac12)=\frac18$, ולכן $\frac78$."),
     NU(r"מהי $P(\frac12<X\le\frac54)=F(\frac54)-F(\frac12)$? (המונה)", Fr(5, 8), r"$F(\frac54)=\frac54-\frac12=\frac34$ ו-$\frac34-\frac18=\frac58$."),
     NU(r"מהי ההסתברות המותנית?", Fr(5, 7), r"$\frac{5/8}{7/8}=\frac57$.")])

# ---- Q5 (same experiments as 24A-B Q5; samples D=2, N=5, Q=0.4, p=0.5, n=4)
Q5M = [r"בינומית $\mathrm{Bin}(n,\frac DN)$: ניסויי ברנולי בלתי תלויים (עם החזרה)", r"היפר-גאומטרית: הוצאה בלי החזרה", r"פואסון: מספר מאורעות בזמן"]
ADD(5, "א",
    RB((r"כל הוצאה עם החזרה היא ניסוי ברנולי בלתי תלוי", 5), (r"הסתברות ההצלחה $Q=\frac DN$", 3), (r"$X\sim\mathrm{Bin}(n,Q)$ ופונקציית ההסתברות לכל $k=0,\dots,n$", 5), (r"טווח $k$", 2)),
    [r"להשתמש בהיפר-גאומטרית (מתאימה לבלי החזרה בלבד)", r"לכתוב $Q=\frac{N}{D}$"],
    [CH(r"מוציאים $n$ כדורים **עם החזרה**. איזה מודל מתאר את מספר האדומים?", Q5M, 0,
        r"עם החזרה ההוצאות בלתי תלויות והסתברות האדום קבועה, כלומר בינומית. ההיפר-גאומטרית דורשת הוצאה בלי החזרה."),
     NU(r"ב-$D=2$, $N=5$: מהי הסתברות ההצלחה $Q$ בהוצאה בודדת?", Fr(2, 5), r"$\frac DN=0.4$."),
     NU(r"ב-$n=4$ הוצאות, מהי $P(X=2)$?", Fr(432, 1250), r"$\binom42(0.4)^2(0.6)^2=6\cdot0.16\cdot0.36=0.3456$.")])

ADD(5, "ב",
    RB((r"$Y\sim G(p)$ הוא מספר ההטלות, ו-$Z\mid Y=j\sim\mathrm{Bin}(j,Q)$", 2), (r"הסתברות שלמה: $\sum_j(1-Q)^jp(1-p)^{j-1}$", 1), (r"סכום סדרה גאומטרית ביחס $(1-Q)(1-p)$ והתשובה $\frac{p(1-Q)}{p(1-Q)+Q}$", 2)),
    [r"להתייחס ל-$n$ כקבוע ולכתוב $(1-Q)^n$", r"לשכוח את החזקה $j-1$ ב-$(1-p)$ ולהפיק סכום שגוי"],
    [CH(r"איך מחשבים את $P(Z=0)$?",
        [r"הסתברות שלמה לפי מספר ההטלות $Y\sim G(p)$, כאשר $Z\mid Y=j\sim\mathrm{Bin}(j,Q)$", r"$Z\sim\mathrm{Bin}(n,Q)$ עם $n$ קבוע, ולכן $P(Z=0)=(1-Q)^n$",
         r"$Z$ מפולג פואסון"], 0,
        r"מספר הכדורים שנלקחו הוא $Y$ (אקראי) ולא $n$ קבוע; לכן ממצעים על $Y$. הפואסון אינו מופיע בשום שלב של הניסוי."),
     NU(r"ב-$p=0.5$, $Q=0.4$: מהי $P(Z=0\mid Y=2)$?", Fr(9, 25), r"$(1-Q)^2=0.36$."),
     NU(r"באותם ערכים, מהו היחס של הסדרה הגאומטרית $(1-Q)(1-p)$?", Fr(3, 10), r"$0.6\cdot0.5=0.3$."),
     NU(r"באותם ערכים, מהי $P(Z=0)$?", Fr(3, 7), r"$\frac{p(1-Q)}{1-(1-Q)(1-p)}=\frac{0.3}{0.7}=\frac37$.")])

ADD(5, "ג",
    RB((r"הסתברות שלמה: $\sum_{j\ge k}\binom jkQ^k(1-Q)^{j-k}p(1-p)^{j-1}$", 2), (r"שימוש בנוסחת ההערה עם $a=(1-Q)(1-p)$", 2), (r"פישוט: סדרה גאומטרית ב-$k$", 1)),
    [r"להתחיל את הסכום מ-$j=1$ ולא מ-$j=k$", r"לשכוח את הגורם $\frac p{1-p}$"],
    [CH(r"מהי צורת $P(Z=k)$ כפונקציה של $k\ge1$?",
        [r"סדרה גאומטרית ב-$k$ (יחס קבוע בין איברים סמוכים)", r"בינומית ב-$k$", r"פואסון ב-$k$"], 0,
        r"אחרי הצבת הנוסחה מתקבל $C\cdot r^k$ עם $r=\frac{Q(1-p)}{p(1-Q)+Q}$, כלומר גאומטרית; בינומית דורשת מספר קבוע של ניסויים, ופואסון דורש $\frac1{k!}$."),
     NU(r"ב-$p=0.5$, $Q=0.4$, $k=2$: מהו הסכום $\sum_{j\ge2}\binom j2a^j$ עם $a=0.3$?", Fr(900, 3430), r"$\frac{a^2}{(1-a)^3}=\frac{0.09}{0.343}\approx0.2624$."),
     NU(r"באותם ערכים, מהי $P(Z=2)$?", Fr(40, 343), r"$\frac{40}{343}\approx0.1166$.")])

# ---- Q6 (bridge Q1; Q2=(A||B) series (C||D||E); p=0.6)
Q6M = [r"מתנים ב-$E$ (היחידה האמצעית): אם היא פועלת מקבלים מקבילי-טורי, ואם לא מקבלים שני ענפים נפרדים",
       r"טור-מקביל פשוט, בלי התניה, כי כל הרכיבים בלתי תלויים", r"מתעלמים מ-$E$ כי היא בלתי תלויה"]
ADD(6, "א",
    RB((r"זיהוי הגשר: $E$ אינה בטור ואינה במקביל, ולכן מתנים ב-$E$", 3), (r"$E$ פועלת: $P=(2p-p^2)^2$; $E$ אינה פועלת: $P=2p^2-p^4$", 4), (r"הסתברות שלמה: $p^2(2+2p-5p^2+2p^3)$", 2)),
    [r"להתייחס ל-$E$ כאילו אינה משפיעה", r"לשכוח את הגורם $p$ של $E$ בהסתברות השלמה"],
    [CH(r"איך מחשבים את $P(Q_1)$ במעגל הגשר?", Q6M, 0,
        r"ב-$p=0.6$ ההתניה נותנת $0.6595$; בלי $E$ אין מבנה טורי-מקבילי כי ענפי $A{-}B$ ו-$C{-}D$ מחוברים דרך $E$."),
     NU(r"ב-$p=0.6$: אם $E$ פועלת, מהי ההסתברות שהמעגל פועל?", Fr("0.7056"), r"$E$ פועלת ממזגת את שני הצמתים האמצעיים: $(A\cup C)\cap(B\cup D)$, ולכן $(2p-p^2)^2=0.84^2=0.7056$."),
     NU(r"ב-$p=0.6$: אם $E$ אינה פועלת, מהי ההסתברות שהמעגל פועל? ($(A\cap B)\cup(C\cap D)$)", Fr("0.5904"), r"$2p^2-p^4=0.72-0.1296=0.5904$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_1)$?", Fr("0.65952"), r"$0.6\cdot0.7056+0.4\cdot0.5904=0.65952$.")])

ADD(6, "ב",
    RB((r"$Q_2=(A\cup B)\cap(C\cup D\cup E)$: שני מקבצים בטור", 3), (r"בלתי תלויים: $P(A\cup B)\cdot P(C\cup D\cup E)$", 3), (r"התשובה $(2p-p^2)\bigl[1-(1-p)^3\bigr]$", 3)),
    [r"לשכוח שהמקבץ השני כולל שלושה רכיבים ולכתוב $(2p-p^2)^2$"],
    [CH(r"מהו המבנה של $Q_2$?", [r"מקבץ מקבילי של $A,B$ בטור עם מקבץ מקבילי של $C,D,E$", r"מקבץ מקבילי של $A,B$ בטור עם מקבץ של $C,D$ בלבד", r"חמישה רכיבים במקביל"], 0,
        r"ב-$p=0.6$: המבנה הנכון נותן $0.7862$; בלי $E$ מקבלים $0.7056$, וחמישה במקביל נותנים $0.9898$."),
     NU(r"ב-$p=0.6$, מהי $P(C\cup D\cup E)$?", Fr("0.936"), r"$1-(1-p)^3=1-0.064=0.936$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_2)$?", Fr("0.78624"), r"$0.84\cdot0.936=0.78624$.")])

ADD(6, "ג",
    RB((r"$P(Q_1/Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}$", 1), (r"התניה על $A,B$: ארבעה מקרים, למשל $A,B$ פועלים: $1-(1-p)^3$; $A$ בלבד: $p(2p-p^2)$", 3), (r"$P(Q_1\cap Q_2)=3p^5-9p^4+7p^3$", 1), (r"התשובה $\frac{p(7-9p+3p^2)}{6-9p+5p^2-p^3}$", 2)),
    [r"להכפיל $P(Q_1)P(Q_2)$ למרות שהמעגלים חולקים רכיבים", r"לחלק ב-$P(Q_1)$ במקום ב-$P(Q_2)$"],
    [CH(r"איך מחשבים את $P(Q_1\cap Q_2)$?",
        [r"בונים אירוע אחד $\tilde Q$ ומתנים בזוג $A,B$ (חולקים אותם בשני המעגלים)", r"$P(Q_1)P(Q_2)$ כי $Q_1,Q_2$ בלתי תלויים", r"$P(Q_1)+P(Q_2)-1$"], 0,
        r"שני המעגלים עושים שימוש באותם $A,B,C,D$ ולכן הם תלויים. ב-$p=0.6$: המכפלה $0.5185$, ו-$P(Q_1)+P(Q_2)-1=0.4458$, אבל הנכון $0.5789$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_2)$? (המכנה: אירוע התנאי)", Fr("0.78624"), r"מסעיף ב."),
     NU(r"באותו $p$: כש-$A,B$ שניהם פועלים, מהי $P(\tilde Q)$? ($Q_1$ פועל, ו-$Q_2$ דורש $C\cup D\cup E$)", Fr("0.936"), r"$1-(1-p)^3=0.936$."),
     NU(r"כש-$A$ פועל ו-$B$ לא, מהי $P(\tilde Q)$? ($Q_1$ דורש $D$, ואז $E\cup C$)", Fr("0.504"), r"$p(2p-p^2)=0.6\cdot0.84=0.504$."),
     NU(r"מהי $P(Q_1/Q_2)$?", Fr("0.57888") / Fr("0.78624"), r"$P(Q_1\cap Q_2)=0.36\cdot0.936+2\cdot0.24\cdot0.504=0.57888$, ולכן $\frac{0.57888}{0.78624}\approx0.7363$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = "ai-draft"
        _q["stepsSource"] = "ai-draft"


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
