# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-B.json -- probability (course 20021), semester A 2024, moed B (17.04.2024).
6 questions, 22 items (Q1 4, Q2 4, Q3 5, Q4 3, Q5 3, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-B.py

Source: exam pp.1-3, official handwritten solutions pp.4-14.
Transcription notes
- Part keys are single letters. Q2 prints א-1, א-2, ב-1, ב-2 -> keys א ב ג ד. Q5 prints ב-1 twice (the second is a
  misprint for ב-2) -> keys א ב ג. Q6 prints א, ב-1, ב-2 -> keys א ב ג. The printed label is the bold token at the
  start of each question text.
- Q6(ג) has a main solution (conditioning on E) and an official alternative solution (conditioning on A,B); both
  are given.
- Q1 area items carry `region` (area figure) and, with the other numeric parts, `sim`: see EXTRAS near the end.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-B.json"
CODE = "24A-B"
IMG = "images/exams/24A-B-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"נקודה $O$ נבחרה באקראי בתוך הריבוע ששטחו הוא יחידה אחת. נסמן באמצעות $S_1,S_2,S_3,S_4$ את שטחי המשולשים שנוצרו (ראו איור). "
          r"בהנחה כי שיעורים $X$ ו-$Y$ של נקודה $O$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגות אחידה $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,1)$, ענו על השאלות הבאות:")
Q1_SOL = r"$S_1=\tfrac12 X,\ S_2=\tfrac12 Y,\ S_3=\tfrac12(1-X)$." "\n"

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א.** מהי ההסתברות $P\left(S_1<\frac18\right)$?",
    Q1_SOL + r"""$$P\left(S_1<\tfrac18\right)=P\left(\tfrac X2<\tfrac18\right)=P\left(X<\tfrac14\right)=\frac14,\qquad X\sim U_c(0,1).$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**ב.** מהי ההסתברות $P\left(S_1+S_2<\frac34\right)$?",
    Q1_SOL + r"""$$P\left(S_1+S_2<\tfrac34\right)=P\left(\tfrac{X+Y}{2}<\tfrac34\right)=P\left(X+Y<\tfrac32\right)=1-\frac12\left(\frac12\right)^2=\frac78.$$
(השטח המשלים הוא משולש ישר-זווית בפינה $(1,1)$ שניצביו $\frac12$, בתוך ריבוע ששטחו $1$; גישה גאומטרית.)""",
    7, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**ג.** מהי ההסתברות $P(S_1<S_2)$?",
    Q1_SOL + r"""$$P(S_1<S_2)=P\left(\tfrac X2<\tfrac Y2\right)=P(Y>X)=\frac{|\{y>x\}|}{|\Omega|}=\frac{1/2}{1}=\frac12.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"**ד.** מהי ההסתברות $P(S_1<S_2<S_3)$?",
    Q1_SOL + r"""$$P(S_1<S_2<S_3)=P(X<Y<1-X)=\bigl|\{x<y<1-x\}\bigr|=\frac14.$$
(גישה גאומטרית: המשולש שקודקודיו $(0,0)$, $(0,1)$, $\left(\frac12,\frac12\right)$.)""",
    4, contextId="c1"))

# ------------------------------------------------------------------ Q2
questions.append(Q(
    2, "א", "combinatorics",
    r"מטילים קובייה **מאוזנת פעמיים** ומסכמים את התוצאות." "\n" r"**א-1:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-5?",
    r"""$\Omega=\{11,\dots,16,\dots,61,\dots,66\}$, $|\Omega|=36$.
$A$ = ״סכום התוצאות שווה ל-5״ $=\{14,23,32,41\}$, $|A|=4$, ולכן
$$P(A)=\frac{|A|}{|\Omega|}=\frac4{36}=\frac19.$$""",
    7))

questions.append(Q(
    2, "ב", "conditional_bayes",
    r"מטילים קובייה **מאוזנת פעמיים** ומסכמים את התוצאות." "\n" r"**א-2:** **אם ידוע** כי סכום התוצאות שווה ל-5, מהי ההסתברות שהתוצאה הראשונה הייתה גדולה מ-3?",
    r"""$B$ = ״התוצאה הראשונה גדולה מ-3״ $=\{41,\dots,46;\,51,\dots,56;\,61,\dots,66\}$, $|B|=18$. $A\cap B=\{41\}$, $|A\cap B|=1$.
$$P(B/A)=\frac{P(B\cap A)}{P(A)}=\frac{|A\cap B|}{|A|}=\frac14.$$""",
    7))

questions.append(Q(
    2, "ג", "combinatorics",
    r"מטילים קובייה **מאוזנת פעמיים** ומכפילים את התוצאות." "\n" r"**ב-1:** מהי ההסתברות שכפל התוצאות לא יעלה על 18?",
    r"""$C$ = ״כפל התוצאות לא עולה על 18״ $=\{11\dots16;\,21\dots26;\,31\dots36;\,41\dots44;\,51,52,53;\,61,62,63\}$, $|C|=28$.
$$P(C)=\frac{|C|}{|\Omega|}=\frac{28}{36}=\frac79.$$""",
    7))

questions.append(Q(
    2, "ד", "conditional_bayes",
    r"מטילים קובייה **מאוזנת פעמיים** ומכפילים את התוצאות." "\n" r"**ב-2:** **אם ידוע** כי כפל התוצאות לא עולה על 18, מהי ההסתברות ששתי התוצאות היו אי זוגיות?",
    r"""$D$ = ״שתי התוצאות אי זוגיות״ $=\{11,13,15;\,31,33,35;\,51,53,55\}$.
$C\cap D=\{11,13,15;\,31,33,35;\,51,53\}$, $|C\cap D|=8$.
$$P(D/C)=\frac{P(C\cap D)}{P(C)}=\frac{|C\cap D|}{|C|}=\frac{8}{28}=\frac27.$$""",
    4))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"נתבונן במטריצת ברנולי מהצורה $\boldsymbol{Q}=\begin{pmatrix}XY&-X\\Y&X+Y-XY\end{pmatrix}$ כאשר $X$ ו-$Y$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגויות ברנולי: "
          r"$X\sim\mathrm{Ber}(p)$ ו-$Y\sim\mathrm{Ber}(p)$. נגדיר שני משתנים מקריים חדשים: דטרמיננטה $D=\det\boldsymbol Q$ ועקבה $T=\operatorname{tr}\boldsymbol Q$ של מטריצה $\boldsymbol Q$.")
Q3_HEAD = (r"$X\sim\mathrm{Ber}(p)$, $Y\sim\mathrm{Ber}(p)$ (בלתי תלויים)." "\n"
           r"$D=\det\boldsymbol Q=XY(X+Y-XY)+XY=X^2Y+XY^2-X^2Y^2+XY=2XY$ (כי $X^2=X$ ו-$Y^2=Y$, משתני ברנולי), $\ T=\operatorname{tr}\boldsymbol Q=X+Y$." "\n")

questions.append(Q(
    3, "א", "joint_discrete",
    r"**א.** חשבו את פונקציית ההסתברות המשותפת של משתנה מקרי דו ממדי $(D,T)$.",
    Q3_HEAD + r"""| $X$ | $0$ | $0$ | $1$ | $1$ |
|---|---|---|---|---|
| $Y$ | $0$ | $1$ | $0$ | $1$ |
| $D$ | $0$ | $0$ | $0$ | $2$ |
| $T$ | $0$ | $1$ | $1$ | $2$ |

| $D\backslash T$ | $0$ | $1$ | $2$ | $p_D(d)$ |
|---|---|---|---|---|
| $0$ | $(1-p)^2$ | $2p(1-p)$ | $0$ | $1-p^2$ |
| $2$ | $0$ | $0$ | $p^2$ | $p^2$ |
| $p_T(t)$ | $(1-p)^2$ | $2p(1-p)$ | $p^2$ | |""",
    5, contextId="c3"))

questions.append(Q(
    3, "ב", "joint_discrete",
    r"**ב.** חשבו את פונקציית ההסתברות השולית של משתנה מקרי $D$. מהו שם ההתפלגות של $D$ ומהם הפרמטרים של ההתפלגות?",
    r"""מהטבלה: $P(D=0)=1-p^2$, $\ P(D=2)=p^2$.
$$\frac D2=XY\sim\mathrm{Ber}(p^2).$$
כלומר $D=2B$ כאשר $B\sim\mathrm{Ber}(p^2)$: $D$ מקבל את הערך $2$ בהסתברות $p^2$ ואת הערך $0$ בהסתברות $1-p^2$.""",
    5, contextId="c3"))

questions.append(Q(
    3, "ג", "special_discrete",
    r"**ג.** חשבו את פונקציית ההסתברות השולית של משתנה מקרי $T$. מהו שם ההתפלגות של $T$ ומהם הפרמטרים של ההתפלגות?",
    r"""מהטבלה: $P(T=0)=(1-p)^2$, $\ P(T=1)=2p(1-p)$, $\ P(T=2)=p^2$.
(נימוק: $T=X+Y$ סכום של שני ברנולי בלתי תלויים, ולכן משפט הפירוק)
$$T=X+Y\sim\mathrm{Bin}(2,p).$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ד", "independence",
    r"**ד.** האם המשתנים $D$ ו-$T$ בלתי תלויים? **נמקו היטב!**",
    r"""**לא, הם תלויים,** כי $p_{DT}(d,t)\ne p_D(d)\,p_T(t)$: עבור $D=2$ ו-$T=0$ מתקבל $p_{DT}(2,0)=0$ בעוד ש-$p_D(2)\,p_T(0)=p^2(1-p)^2>0$ (עבור $0<p<1$).""",
    5, contextId="c3"))

questions.append(Q(
    3, "ה", "independence",
    r"**ה.** האם המשתנים $D$ ו-$T$ בלתי מתואמים? **נמקו היטב!**",
    r"""בודקים האם $\operatorname{Cov}(D,T)=0$:
$$\operatorname{Cov}(D,T)=\mathbb E[DT]-\mathbb E[D]\,\mathbb E[T],\qquad \mathbb E[D]=2p^2,\ \ \mathbb E[T]=2p.$$
$$\mathbb E[DT]=\mathbb E[2XY(X+Y)]=2\,\mathbb E[X^2Y+XY^2]=4\,\mathbb E[X]\,\mathbb E[Y]=4p^2$$
(כי $X^2Y=XY$ ו-$XY^2=XY$). לכן
$$\operatorname{Cov}[D,T]=4p^2-4p^3=4p^2(1-p)\ne 0,$$
ולכן **$D$ ו-$T$ מתואמים** (אינם בלתי מתואמים), עבור $0<p<1$.""",
    5, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"לפניך גרף עבור פונקציית צפיפות ההסתברות $f_X(x)$ של משתנה מקרי $X$. מתקיים:" "\n"
          r"$$\begin{cases}P(0\le X\le a)=2\cdot P(a\le X\le b)\\ \mathbb E[X]=\frac59\end{cases}$$")

questions.append(Q(
    4, "א", "continuous_rv",
    Q4_TXT + "\n" + r"**א.** מצאו את הפרמטרים $a$, $b$ ו-$c$.",
    r"""נרמול ותנאי ההסתברות:
$$ac=2(b-a),\qquad ac+(b-a)=1\ \Rightarrow\ b-a=\frac13,\quad ac=\frac23.$$
תוחלת:
$$\mathbb E[X]=\int_0^a x\cdot c\,dx+\int_a^b x\cdot 1\,dx=\frac{ca^2}{2}+\frac{b^2-a^2}{2}=\frac59.$$
כלומר $ca\cdot a+(b-a)(b+a)=\frac{10}{9}$, ולכן $\frac23 a+\frac13(b+a)=\frac{10}9$, כלומר $b+3a=\frac{10}3$. יחד עם $b-a=\frac13$ מתקבל $4a=3$:
$$a=\frac34,\qquad b=\frac{13}{12},\qquad c=\frac89.$$""",
    10, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ב", "continuous_rv",
    Q4_TXT + "\n" + r"**ב.** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו גרף של $F_X(t)$ אשר משקף את תוצאות החישוב.",
    r"""$$F_X(t)=\int_{-\infty}^t f_X(x)\,dx=\begin{cases}0,&t<0,\\ \dfrac89\,t,&0\le t<\dfrac34,\\ t-\dfrac1{12},&\dfrac34\le t<\dfrac{13}{12},\\ 1,&t\ge\dfrac{13}{12}.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת](images/exams/24A-B-Q4-cdf.png)""",
    10, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ג", "continuous_rv",
    Q4_TXT + "\n" + r"**ג.** מהי ההסתברות $P(X\le\mathbb E[X])$?",
    r"""$$P(X\le\mathbb E[X])=P\left(X\le\tfrac59\right)=F_X\left(\tfrac59\right)=\frac89\cdot\frac59=\frac{40}{81}.$$""",
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
Q6_B = r"לאחר פירוק של מעגל $Q_1$, סטודנט הרכיב מעגל חדש $Q_2$ **מאותן יחידות** (אך ללא יחידה $E$)."

questions.append(Q(
    6, "א", "circuits",
    r"**א.** מהי ההסתברות שמעגל $Q_1$ פעיל?",
    r"""מתנים ב-$E$ (פעיל או לא פעיל):
$$P(Q_1)=P(Q_1/E)P(E)+P(Q_1/\bar E)P(\bar E)=(2p-p^2)^2\,p+(2p^2-p^4)(1-p)$$
$$=p(2p-p^2)^2+(1-p)(2p^2-p^4)=p^2\bigl(2+2p-5p^2+2p^3\bigr).$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    Q6_B + "\n" + r"**ב-1:** מהי ההסתברות שמעגל $Q_2$ יפעל?",
    r"""$$P(Q_2)=P\bigl((A\cup B)\cap(C\cup D)\bigr)=P(A\cup B)\,P(C\cup D)=(2p-p^2)^2.$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    Q6_B + "\n" + r"**ב-2:** **אם ידוע** שמעגל $Q_2$ פעיל, מהי ההסתברות שגם המעגל המקורי $Q_1$ פעיל?",
    r"""$$P(Q_1/Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}.$$
נסמן $\tilde Q=Q_1\cap Q_2$ (שני המעגלים מחוברים בטור) ונחשב בהתניה על $E$:
$$P(\tilde Q)=P(\tilde Q/E)P(E)+P(\tilde Q/\bar E)P(\bar E).$$
**$E$ פעיל:** $\tilde Q$ פעיל אם ורק אם $(A\cup B)\cap(C\cup D)\cap(A\cup C)\cap(B\cup D)$. מתקיים $(A\cup B)\cap(A\cup C)=A\cup(B\cap C)$ ו-$(C\cup D)\cap(B\cup D)=D\cup(B\cap C)$, ולכן
$$P(\tilde Q/E)=P\bigl((A\cap D)\cup(B\cap C)\bigr)=P(A\cap D)+P(B\cap C)-P(A\cap B\cap C\cap D)=2p^2-p^4.$$
**$E$ לא פעיל:** נסמן $\tilde{\tilde Q}=\tilde Q/\bar E$ ונחשב בהתניה על $A,C$:
- $A\cap C$ פעילים (הסתברות $p^2$): נדרש $B\cup D$, כלומר $P=2p-p^2$;
- $\bar A\cap\bar C$ (הסתברות $(1-p)^2$): $P=0$;
- $A\cap\bar C$ (הסתברות $p(1-p)$): נדרשים $B$ ו-$D$, כלומר $P=p^2$;
- $\bar A\cap C$ (הסתברות $p(1-p)$): נדרשים $B$ ו-$D$, כלומר $P=p^2$.

$$P(\tilde Q/\bar E)=p^2(2p-p^2)+2p^3(1-p)=4p^3-3p^4.$$
לכן
$$P(Q_1\cap Q_2)=p\,(2p^2-p^4)+(1-p)(4p^3-3p^4)=p^3(6-7p+2p^2),$$
ולכן
$$P(Q_1/Q_2)=\frac{p^3(6-7p+2p^2)}{p^2(2-p)^2}=\frac{p(3-2p)}{2-p}.$$
**פתרון חלופי (התניה על $A,B$):**
- $A\cap B$ פעילים (הסתברות $p^2$): $\tilde Q$ פעיל אם $C\cup D$, כלומר $P=2p-p^2$;
- $\bar A\cap\bar B$ (הסתברות $(1-p)^2$): $P=0$;
- $A\cap\bar B$ (הסתברות $p(1-p)$): $P=P\bigl((C\cup D)\cap(E\cup C)\cap D\bigr)=P\bigl(D\cap(E\cup C)\bigr)=p(2p-p^2)$;
- $\bar A\cap B$ (הסתברות $p(1-p)$): $P=P\bigl((C\cup D)\cap C\cap(E\cup D)\bigr)=P\bigl(C\cap(E\cup D)\bigr)=p(2p-p^2)$.

$$P(Q_1\cap Q_2)=p^2(2p-p^2)+2p(1-p)\,p(2p-p^2)=p^2(2p-p^2)(3-2p),\qquad P(Q_1/Q_2)=\frac{p(3-2p)}{2-p}.$$""",
    7, contextId="c6"))

exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ד, מועד ב (17.04.2024)",
    "year": 2024,
    "examDate": "17.04.2024",
    "sourceFile": "24A-B exam pp.1-3",
    "solutionFile": "24A-B official handwritten solutions pp.4-14",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: ריבוע ונקודה אקראית", "image": IMG + "Q1-square.png", "caption": Q1_TXT},
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
    (1, "א"): {"region": REG([lin(1, 0, "1/4", "<")], 1 / 4, "האירוע S1<1/8, כלומר X<1/4"),
               "sim": AREA("P(S1<1/8)", 1 / 4)},
    (1, "ב"): {"region": REG([lin(1, 1, "3/2", "<")], 7 / 8, "האירוע S1+S2<3/4, כלומר X+Y<3/2"),
               "sim": AREA("P(S1+S2<3/4)", 7 / 8)},
    (1, "ג"): {"region": REG([lin(-1, 1, 0, ">")], 1 / 2, "האירוע S1<S2, כלומר Y>X"),
               "sim": AREA("P(S1<S2)", 1 / 2)},
    (1, "ד"): {"region": REG([lin(-1, 1, 0, ">"), lin(1, 1, 1, "<")], 1 / 4, "האירוע S1<S2<S3, כלומר X<Y<1-X"),
               "sim": AREA("P(S1<S2<S3)", 1 / 4)},
    (2, "א"): {"sim": DICE("P(sum = 5)", 1 / 9, 2, "sum == 5")},
    (2, "ב"): {"sim": DICE("P(d1>3 | sum = 5)", 1 / 4, 2, "d1 > 3", "sum == 5")},
    (2, "ג"): {"sim": DICE("P(product <= 18)", 7 / 9, 2, "prod <= 18")},
    (2, "ד"): {"sim": DICE("P(both odd | product <= 18)", 2 / 7, 2, "d1 % 2 == 1 and d2 % 2 == 1", "prod <= 18")},
    (4, "ג"): {"sim": PDF("P(X<=E[X])", 40 / 81, [(0, "3/4", "8/9"), ("3/4", "13/12", "1")], "x <= 5/9")},
}
for _q in questions:
    _x = EXTRAS.get((_q["num"], _q.get("part")))
    if _x:
        _q.update(_x)


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
