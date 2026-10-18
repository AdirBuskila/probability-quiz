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


# ---- extra sims for items with symbolic answers, at sample parameter values (stated in `estimate`)
def _bern(p):
    return {"X": {"values": [0, 1], "probs": [1 - p, p]}, "Y": {"values": [0, 1], "probs": [1 - p, p]}}


_DET = "X*Y*(X+Y-X*Y)+X*Y"     # det Q straight from the matrix entries (no X^2=X shortcut)
_TR = "X*Y+(X+Y-X*Y)"
_BR = {"edges": [{"id": "A", "from": "L", "to": "T", "p": 0.6}, {"id": "B", "from": "T", "to": "R", "p": 0.6},
                 {"id": "C", "from": "L", "to": "U", "p": 0.6}, {"id": "D", "from": "U", "to": "R", "p": 0.6},
                 {"id": "E", "from": "T", "to": "U", "p": 0.6}], "source": "L", "sink": "R"}
_Q1E = "(A and B) or (C and D) or (A and E and D) or (C and E and B)"
_Q2E = "(A or B) and (C or D)"
_NT = 30      # the number of tosses is truncated at 30 (tail mass 0.5^30 goes to the last value)


def _compound(Z_event, p, Q):
    probs = [p * (1 - p) ** (j - 1) for j in range(1, _NT + 1)]
    probs[-1] += 1 - sum(probs)
    vs = {"Y": {"values": list(range(1, _NT + 1)), "probs": probs}}
    for i in range(1, _NT + 1):
        vs["B%d" % i] = {"values": [0, 1], "probs": [1 - Q, Q]}
    z = "+".join("B%d*(Y>=%d)" % (i, i) for i in range(1, _NT + 1))
    return {"vars": vs, "event": "(" + z + ")" + Z_event}


EXTRA_SIMS = {
    (3, "א"): {"kind": "custom_discrete", "estimate": "P(D=0, T=1) ב-p=0.3", "exact": 0.42,
               "params": {"vars": _bern(0.3), "event": _DET + " == 0 and " + _TR + " == 1"}},
    (3, "ב"): {"kind": "custom_discrete", "estimate": "P(D=2) ב-p=0.3", "exact": 0.09,
               "params": {"vars": _bern(0.3), "event": _DET + " == 2"}},
    (3, "ג"): {"kind": "custom_discrete", "estimate": "P(T=0) ב-p=0.3", "exact": 0.49,
               "params": {"vars": _bern(0.3), "event": _TR + " == 0"}},
    (3, "ד"): {"kind": "custom_discrete", "estimate": "P(D=2, T=0) ב-p=0.3", "exact": 0,
               "params": {"vars": _bern(0.3), "event": _DET + " == 2 and " + _TR + " == 0"}},
    (3, "ה"): {"kind": "custom_discrete", "estimate": "cov[D,T] ב-p=0.3", "exact": 0.252,
               "params": {"vars": _bern(0.3), "measure": "cov", "expr": [_DET, _TR]}},
    (4, "א"): {"kind": "pdf", "estimate": "E[X] ב-a=3/4, b=13/12, c=8/9", "exact": 5 / 9,
               "params": {"pieces": [{"from": 0, "to": "3/4", "expr": "8/9"}, {"from": "3/4", "to": "13/12", "expr": "1"}],
                          "measure": "mean", "expr": "x"}},
    (4, "ב"): PDF("F(9/10)", 0.9 - 1 / 12, [(0, "3/4", "8/9"), ("3/4", "13/12", "1")], "x <= 9/10"),
    (5, "א"): {"kind": "urn", "estimate": "P(X=2) ב-D=2, N=5, n=4 (Q=0.4)", "exact": 0.3456,
               "params": {"counts": {"red": 2, "black": 3}, "draws": 4, "replace": True, "event": "red == 2"}},
    (5, "ב"): {"kind": "custom_discrete", "estimate": "P(Z=0) ב-p=0.5, Q=0.4 (קטוע ב-30 הטלות)", "exact": 3 / 7,
               "params": _compound(" == 0", 0.5, 0.4)},
    (5, "ג"): {"kind": "custom_discrete", "estimate": "P(Z=2) ב-p=0.5, Q=0.4 (קטוע ב-30 הטלות)", "exact": 40 / 343,
               "params": _compound(" == 2", 0.5, 0.4)},
    (6, "א"): {"kind": "circuit", "estimate": "P(Q1) ב-p=0.6", "exact": 0.65952, "params": dict(_BR, event="S")},
    (6, "ב"): {"kind": "circuit", "estimate": "P(Q2) ב-p=0.6", "exact": 0.7056,
               "params": {"event": "S", "network": {"type": "series", "children": [
                   {"type": "parallel", "children": [{"type": "comp", "id": "A", "p": 0.6}, {"type": "comp", "id": "B", "p": 0.6}]},
                   {"type": "parallel", "children": [{"type": "comp", "id": "C", "p": 0.6}, {"type": "comp", "id": "D", "p": 0.6}]}]}}},
    (6, "ג"): {"kind": "circuit", "estimate": "P(Q1 | Q2) ב-p=0.6", "exact": 0.54432 / 0.7056,
               "params": dict(_BR, event=_Q1E, given=_Q2E)},
}
for _q in questions:
    _x = EXTRA_SIMS.get((_q["num"], _q.get("part")))
    if _x and "sim" not in _q:
        _q["sim"] = _x


# ---- rubric / pitfalls / steps (ai-draft). Every expected value is re-derived independently, by exact arithmetic and
# by Monte Carlo, in tools/verify/24A-B/steps_check.py (which reads the generated raw JSON).
from fractions import Fraction as Fr

FRAC = 0.0006   # tolerance when the answer is a non-terminating fraction entered as a 3-4 digit decimal


def O(*v):
    return [{"id": "abcdefgh"[i], "value": t} for i, t in enumerate(v)]


def CH(prompt, opts, ans, explain):
    return {"type": "choice", "prompt": prompt, "options": O(*opts), "correctId": "abcdefgh"[ans], "explain": explain}


def NU(prompt, val, explain):
    val = Fr(val)
    a = round(float(val), 4)
    exact = (val * 10000).denominator == 1
    return {"type": "numeric", "prompt": prompt + ("" if exact else " (שבר או עשרוני)"), "answer": a,
            "tol": 0 if exact else FRAC, "explain": explain}


def RB(*r):
    return [{"text": t, "points": p} for t, p in r]


S = {}


def ADD(num, part, rub, pit, steps):
    S[(num, part)] = (rub, pit, steps)


OMEGA = r"נקודה אקראית בריבוע היחידה. מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X,Y)$?"
OMEGA_X = r"הריבוע $(0,1)^2$ שטחו $1$, ולכן כאן ההסתברות שווה לשטח. כשמרחב המדגם אינו ריבוע היחידה חייבים לחלק ב-$|\Omega|$."
S1S = r"$S_1=\frac X2,\ S_2=\frac Y2,\ S_3=\frac{1-X}2$. "

ADD(1, "א",
    RB((r"תרגום $S_1<\frac18$ לתנאי על $X$: $X<\frac14$", 3), (r"גישה גאומטרית או $F_X$ של התפלגות אחידה", 2), (r"התשובה $\frac14$", 2)),
    [r"לפתור $X<\frac18$ ולשכוח את הגורם $\frac12$ ב-$S_1=\frac X2$", r"לחלק ב-$\frac12$ במקום לכפול ב-$2$ באי-השוויון"],
    [NU(OMEGA, 1, OMEGA_X),
     CH(S1S + r"איזה תנאי שקול ל-$S_1<\frac18$?", [r"$X<\frac14$", r"$X<\frac18$", r"$X<\frac12$"], 0,
        r"$\frac X2<\frac18\iff X<\frac14$. הערכים $\frac18$ ו-$\frac12$ נותנים הסתברויות $\frac18$ ו-$\frac12$ ולא את ערך $S_1<\frac18$."),
     NU(r"מהו שטח האירוע $\{X<\frac14\}$?", Fr(1, 4), r"רצועה ברוחב $\frac14$ לכל הגובה: $\frac14$.")])

ADD(1, "ב",
    RB((r"$S_1+S_2=\frac{X+Y}2<\frac34\iff X+Y<\frac32$", 3), (r"המשלים: משולש פינתי בקודקוד $(1,1)$ בניצבים $\frac12$ ושטחו $\frac18$", 3), (r"התשובה $\frac78$", 1)),
    [r"לשכוח להכפיל ב-$2$ ולפתור $X+Y<\frac34$", r"לחשב את שטח המשולש הלא נכון (הפינה $(0,0)$ במקום $(1,1)$)"],
    [NU(OMEGA, 1, OMEGA_X),
     CH(S1S + r"איזה תנאי שקול ל-$S_1+S_2<\frac34$?", [r"$X+Y<\frac32$", r"$X+Y<\frac34$", r"$X+Y<3$"], 0,
        r"$\frac{X+Y}2<\frac34\iff X+Y<\frac32$. התנאי $X+Y<\frac34$ נותן $\frac9{32}$, והתנאי $X+Y<3$ תמיד מתקיים."),
     NU(r"מהו שטח המשלים $\{X+Y\ge\frac32\}$ (משולש בפינה $(1,1)$)?", Fr(1, 8), r"ניצבים $\frac12$: $\frac12\cdot\frac14=\frac18$."),
     NU(r"מהי $P(S_1+S_2<\frac34)$?", Fr(7, 8), r"$1-\frac18=\frac78$.")])

ADD(1, "ג",
    RB((r"$S_1<S_2\iff X<Y$", 3), (r"אזור $Y>X$ הוא חצי הריבוע, שטחו $\frac12$", 3), (r"התשובה $\frac12$", 1)),
    [r"להפוך את כיוון אי-השוויון", r"לפתור בלי גאומטריה ולכתוב $\frac13$"],
    [NU(OMEGA, 1, OMEGA_X),
     CH(S1S + r"איזה תנאי שקול ל-$S_1<S_2$?", [r"$Y>X$", r"$Y>2X$", r"$Y>\frac X2$"], 0,
        r"שני האגפים מכילים את אותו גורם $\frac12$: $\frac X2<\frac Y2\iff X<Y$. התנאים האחרים הם $\frac14$ ו-$\frac34$ מהשטח."),
     NU(r"מהו שטח האזור $\{Y>X\}$ בריבוע?", Fr(1, 2), r"משולש ישר-זווית בניצבים $1$: $\frac12$.")])

ADD(1, "ד",
    RB((r"תרגום ל-$X<Y<1-X$ (שני תנאים: $S_1<S_2$ ו-$S_2<S_3$)", 2), (r"זיהוי האזור כמשולש $(0,0),(0,1),(\frac12,\frac12)$", 1), (r"שטח $\frac14$", 1)),
    [r"לתרגם את $S_2<S_3$ ל-$Y<1-Y$ (שוכחים ש-$S_3$ תלוי ב-$X$)"],
    [NU(OMEGA, 1, OMEGA_X),
     CH(S1S + r"איזה תנאי שקול ל-$S_1<S_2<S_3$?", [r"$X<Y<1-X$", r"$X<Y<1-Y$", r"$Y<X<1-X$"], 0,
        r"$S_1<S_2\iff X<Y$ ו-$S_2<S_3\iff Y<1-X$. שני התנאים האחרים נותנים $\frac18$."),
     NU(r"מהו שטח המשולש עם הקודקודים $(0,0)$, $(0,1)$, $(\frac12,\frac12)$?", Fr(1, 4), r"בסיס $1$ על ציר $y$ וגובה $\frac12$: $\frac14$.")])

# ---- Q2
Q2M1 = [r"מרחב מדגם אחיד על $36$ הזוגות: $P=\frac{|A|}{36}$", r"הסכום מתפלג אחיד על $2,\dots,12$: $P=\frac1{11}$",
        r"התפלגות בינומית $\mathrm{Bin}(2,\frac16)$"]
ADD(2, "א",
    RB((r"מרחב המדגם: $36$ זוגות שווי סיכוי", 2), (r"האירוע $\{14,23,32,41\}$, $|A|=4$", 3), (r"התשובה $\frac19$", 2)),
    [r"להניח שהסכומים $2,\dots,12$ שווי סיכוי ולכתוב $\frac1{11}$", r"לספור רק $14,23$ ולשכוח את הסדר"],
    [CH(r"מטילים קובייה מאוזנת פעמיים. איזה מודל מתאים לחישוב $P(\text{sum}=5)$?", Q2M1, 0,
        r"הזוגות $(i,j)$ שווי סיכוי, הסכומים לא: סכום $7$ שכיח פי $6$ מסכום $2$, ולכן $\frac1{11}$ שגוי. הבינומית סופרת הצלחות בניסויים זהים ואינה נותנת סכום."),
     NU(r"כמה זוגות $(i,j)$ נותנים סכום $5$?", 4, r"$(1,4),(2,3),(3,2),(4,1)$."),
     NU(r"מהי $P(\text{sum}=5)$?", Fr(1, 9), r"$\frac4{36}=\frac19$.")])

ADD(2, "ב",
    RB((r"הגדרת המותנית $P(B/A)=\frac{|A\cap B|}{|A|}$", 2), (r"$A\cap B=\{41\}$ ו-$|A|=4$", 3), (r"התשובה $\frac14$", 2)),
    [r"להשתמש ב-$P(B)=\frac12$ כאילו $A,B$ בלתי תלויים", r"לחלק ב-$|\Omega|=36$ במקום ב-$|A|$"],
    [CH(r"נתון שהסכום הוא $5$. איך מחשבים את ההסתברות שהתוצאה הראשונה גדולה מ-$3$?",
        [r"מצמצמים את מרחב המדגם ל-$A$ וסופרים בתוכו: $\frac{|A\cap B|}{|A|}$", r"$P(B)=\frac12$, כי ההטלה הראשונה אינה תלויה בסכום",
         r"$P(A)\,P(B)$"], 0,
        r"הסכום תלוי בהטלה הראשונה: $P(B/A)=\frac14\ne P(B)=\frac12$, ולכן אי-תלות שגויה; והמכפלה $\frac1{18}$ אינה מותנית."),
     NU(r"מהי $P(A)$, ההסתברות לסכום $5$? (אירוע התנאי)", Fr(1, 9), r"$\frac4{36}$."),
     NU(r"מהי $P(A\cap B)$, כלומר סכום $5$ וגם תוצאה ראשונה גדולה מ-$3$?", Fr(1, 36), r"רק $(4,1)$: $\frac1{36}$."),
     NU(r"מהי $P(B/A)$?", Fr(1, 4), r"$\frac{1/36}{1/9}=\frac14$.")])

ADD(2, "ג",
    RB((r"מרחב אחיד על $36$ זוגות", 1), (r"ספירת המשלים: $8$ זוגות עם מכפלה גדולה מ-$18$ (או $28$ נוחים ישירות)", 4), (r"התשובה $\frac79$", 2)),
    [r"לספור רק חלק מהזוגות הסימטריים (למשל לשכוח $(3,6)$ ו-$(6,3)$)"],
    [NU(r"מהו $|\Omega|$ בהטלת קובייה פעמיים?", 36, r"$6\cdot6$ זוגות סדורים."),
     NU(r"כמה זוגות $(i,j)$ נותנים מכפלה גדולה מ-$18$?", 8, r"שמונה זוגות: $(4,5),(4,6),(5,4),(5,5),(5,6),(6,4),(6,5),(6,6)$. המשלים $36-8=28$."),
     NU(r"מהי $P(\text{product}\le18)$?", Fr(7, 9), r"$\frac{28}{36}=\frac79$.")])

ADD(2, "ד",
    RB((r"הגדרת המותנית $\frac{|C\cap D|}{|C|}$", 1), (r"$|C|=28$ ו-$|C\cap D|=8$", 2), (r"התשובה $\frac27$", 1)),
    [r"לחלק ב-$|\Omega|=36$", r"לספור זוגות אי-זוגיים בלי לסנן לפי $C$ (שם $9$ זוגות)"],
    [NU(r"מהי $P(C)$, ההסתברות שהמכפלה אינה עולה על $18$? (אירוע התנאי)", Fr(7, 9), r"$\frac{28}{36}$."),
     NU(r"מהי $P(C\cap D)$, מכפלה לכל היותר $18$ ושתי התוצאות אי-זוגיות?", Fr(2, 9),
        r"מתוך $9$ הזוגות האי-זוגיים רק $(5,5)$ נכשל (מכפלה $25$): $8$ זוגות, $\frac8{36}=\frac29$."),
     NU(r"מהי $P(D/C)$?", Fr(2, 7), r"$\frac{2/9}{7/9}=\frac27$.")])

# ---- Q3
Q3M = [r"למנות את ארבעת הצירופים של $(X,Y)$, לחשב $(D,T)$ לכל אחד, ולצרף הסתברות מכפלה (בלתי תלויים)",
       r"$(D,T)$ מתפלג בינומית דו-ממדית, כי $T=X+Y$ סכום ניסויי ברנולי",
       r"ההסתברות המשותפת היא מכפלת השוליות $P_D(d)P_T(t)$, כי $D$ ו-$T$ נבנו מאותם משתנים בלתי תלויים"]
ADD(3, "א",
    RB((r"פישוט $D=2XY$ ו-$T=X+Y$ ($X^2=X$)", 2), (r"טבלת ארבע התוצאות של $(X,Y)$ עם ערכי $(D,T)$", 2), (r"הטבלה המשותפת והשוליות", 1)),
    [r"להשאיר את $D$ בלי פישוט", r"לרשום את המשותפת כמכפלת השוליות"],
    [CH(r"איך מחשבים את ההסתברות המשותפת של $(D,T)$?", Q3M, 0,
        r"$(D,T)$ היא פונקציה של $(X,Y)$ בלבד: ממנים 4 תוצאות. $D=2XY$ לא מקבל $1$, ולכן אין כאן מכפלת שוליות (למשל $P(D=2,T=0)=0$)."),
     NU(r"מהו $D=\det\boldsymbol Q$ כאשר $X=Y=1$?", 2, r"$\boldsymbol Q=\begin{pmatrix}1&-1\\1&1\end{pmatrix}$, דטרמיננטה $1+1=2$."),
     NU(r"ב-$p=0.3$, מהי $P(D=0,T=1)$? ($(X,Y)=(0,1)$ או $(1,0)$)", Fr(21, 50), r"$2p(1-p)=0.42$."),
     NU(r"בטבלה עם $D\in\{0,2\}$ ו-$T\in\{0,1,2\}$, כמה מתוך $6$ התאים שווים ל-$0$?", 3, r"רק $(0,0),(0,1),(2,2)$ אפשריים; השלושה האחרים $(0,2),(2,0),(2,1)$ הם $0$.")])

ADD(3, "ב",
    RB((r"$P(D=2)=P(XY=1)=p^2$ ו-$P(D=0)=1-p^2$", 3), (r"$\frac D2=XY\sim\mathrm{Ber}(p^2)$ ולכן $D=2B$", 2)),
    [r"לכתוב $D\sim\mathrm{Ber}(p)$ בלי לשים לב שהערך הוא $2$ והסתברותו $p^2$"],
    [CH(r"ב-$p=0.3$, מהי $P(D=2)$?", [r"$p^2=0.09$", r"$p=0.3$", r"$2p(1-p)=0.42$"], 0,
        r"$D=2$ רק כש-$X=Y=1$ (הסתברות $p^2$). $p$ הוא $P(X=1)$, ו-$2p(1-p)$ הוא $P(X\ne Y)$."),
     NU(r"ב-$p=0.3$, מהי $P(D=2)$?", Fr(9, 100), r"$0.3^2=0.09$."),
     NU(r"ב-$p=0.3$, מהי $\mathbb E[D]$?", Fr(9, 50), r"$2\cdot p^2=0.18$.")])

ADD(3, "ג",
    RB((r"$T=X+Y$ סכום של שני ברנולי בלתי תלויים בעלי אותו $p$", 2), (r"משפט הפירוק: $T\sim\mathrm{Bin}(2,p)$", 2), (r"ההסתברויות $(1-p)^2,\,2p(1-p),\,p^2$", 1)),
    [r"לכתוב $\mathrm{Ber}(2p)$ (הערך $2$ אפשרי)"],
    [CH(r"מהי ההתפלגות של $T=X+Y$?", [r"$\mathrm{Bin}(2,p)$", r"$\mathrm{Ber}(2p)$", r"$\mathrm{Bin}(2,p^2)$"], 0,
        r"סכום של $2$ ברנולי בלתי תלויים באותו $p$ הוא $\mathrm{Bin}(2,p)$ (ב-$p=0.3$: $P(T=1)=0.42$). $\mathrm{Ber}(2p)$ אינו יכול לקבל $2$, ו-$\mathrm{Bin}(2,p^2)$ נותן $0.1638$."),
     NU(r"ב-$p=0.3$, מהי $P(T=0)$?", Fr(49, 100), r"$(1-p)^2=0.49$."),
     NU(r"ב-$p=0.3$, מהי $P(T=1)$?", Fr(21, 50), r"$2p(1-p)=0.42$.")])

ADD(3, "ד",
    RB((r"תא אפס בטבלה המשותפת: $P(D=2,T=0)=0$", 2), (r"מכפלת השוליות $p^2(1-p)^2>0$", 2), (r"מסקנה: תלויים", 1)),
    [r"להסיק אי-תלות מכך ש-$X,Y$ בלתי תלויים"],
    [NU(r"מהי $P(D=2,T=0)$? ($D=2$ דורש $X=Y=1$, ואז $T=2$.)", 0, r"האירועים זרים."),
     NU(r"ב-$p=0.3$, מהו המכפלה $P(D=2)\,P(T=0)$?", Fr(441, 10000), r"$0.09\cdot0.49=0.0441>0$."),
     CH(r"האם $D$ ו-$T$ בלתי תלויים?", [r"לא: $P(D=2,T=0)=0\ne P(D=2)P(T=0)$", r"כן, כי $X$ ו-$Y$ בלתי תלויים"], 0,
        r"מספיק תא אחד שבו המשותפת שונה ממכפלת השוליות.")])

ADD(3, "ה",
    RB((r"$\mathbb E[D]=2p^2$, $\mathbb E[T]=2p$", 1), (r"$\mathbb E[DT]=\mathbb E[2XY(X+Y)]=4p^2$ (שימוש ב-$X^2Y=XY$)", 2), (r"$\operatorname{Cov}=4p^2(1-p)\ne0$: מתואמים", 2)),
    [r"להניח $\mathbb E[DT]=\mathbb E[D]\mathbb E[T]$ (זה נכון רק לבלתי תלויים)"],
    [NU(r"ב-$p=0.3$, מהי $\mathbb E[DT]$?", Fr(9, 25), r"$4p^2=0.36$."),
     NU(r"ב-$p=0.3$, מהו המכפלה $\mathbb E[D]\,\mathbb E[T]$?", Fr(27, 250), r"$2p^2\cdot2p=0.18\cdot0.6=0.108$."),
     NU(r"ב-$p=0.3$, מהי $\operatorname{cov}[D,T]$?", Fr(63, 250), r"$0.36-0.108=0.252=4p^2(1-p)$.")])

# ---- Q4
ADD(4, "א",
    RB((r"נרמול ויחס: $ac=2(b-a)$ ו-$ac+(b-a)=1$, ולכן $b-a=\frac13$", 4), (r"תוחלת: $\frac{ca^2}2+\frac{b^2-a^2}2=\frac59$ ומכאן $b+3a=\frac{10}3$", 4), (r"$a=\frac34$, $b=\frac{13}{12}$, $c=\frac89$", 2)),
    [r"לשכוח את תנאי היחס ולנסות לפתור רק מהנרמול והתוחלת", r"לרשום $\int_0^ax\cdot c\,dx=ca$ במקום $\frac{ca^2}2$"],
    [CH(r"כמה משוואות דרושות ל-$a,b,c$, ומאיפה הן?",
        [r"שלוש: נרמול, $P(0\le X\le a)=2P(a\le X\le b)$ ו-$\mathbb E[X]=\frac59$", r"שתיים: נרמול ותוחלת, כי התנאי על ההסתברויות מיותר",
         r"אחת: נרמול בלבד"], 0,
        r"שלושה נעלמים דורשים שלוש משוואות. בלי תנאי היחס נשארת משפחה חד-פרמטרית של פתרונות."),
     NU(r"מהו $b-a$? (מהנרמול $ac+(b-a)=1$ ומ-$ac=2(b-a)$)", Fr(1, 3), r"$3(b-a)=1$."),
     NU(r"מהו $a$?", Fr(3, 4), r"מהתוחלת $b+3a=\frac{10}3$ ויחד עם $b-a=\frac13$: $4a=3$."),
     NU(r"מהו $c$?", Fr(8, 9), r"$ac=\frac23$ ולכן $c=\frac{2/3}{3/4}=\frac89$.")])

ADD(4, "ב",
    RB((r"אינטגרציה על $[0,\frac34)$: $F=\frac89t$", 3), (r"על $[\frac34,\frac{13}{12})$: $F=t-\frac1{12}$ (רציפות ב-$\frac34$)", 4), (r"שרטוט גרף: קו, קו בשיפוע $1$, ואז $1$", 3)),
    [r"לרשום $F(t)=t$ על הקטע השני בלי להוסיף את הקבוע (חסרה המסה $\frac23$ שנצברה)", r"להפסיק את $F$ במקום להגיע ל-$1$ ב-$b$"],
    [NU(r"מהי $F_X(\frac34)=P(X\le\frac34)$?", Fr(2, 3), r"$\frac89\cdot\frac34=\frac23$ ($=ac$)."),
     CH(r"איזו נוסחה נכונה ל-$F_X(t)$ עבור $\frac34\le t<\frac{13}{12}$? (נבדוק ב-$t=0.9$)", [r"$t-\frac1{12}$", r"$t$", r"$\frac89t$"], 0,
        r"$F(t)=\frac23+(t-\frac34)=t-\frac1{12}$ (ב-$0.9$: $0.8167$). $F=t$ נותנת $0.9$, והנוסחה $\frac89t$ שייכת לקטע הראשון ($0.8$)."),
     NU(r"מהי $F_X(1)$?", Fr(11, 12), r"$1-\frac1{12}=\frac{11}{12}$.")])

ADD(4, "ג",
    RB((r"$\mathbb E[X]=\frac59<a=\frac34$, ולכן יש להשתמש בקטע הראשון של $F$", 2), (r"$F_X(\frac59)=\frac89\cdot\frac59$", 2), (r"התשובה $\frac{40}{81}$", 1)),
    [r"להשתמש בנוסחה של הקטע השני למרות ש-$\frac59<\frac34$"],
    [NU(r"מהי הצפיפות על $[0,a]$ (הקבוע $c$)?", Fr(8, 9), r"מסעיף א."),
     CH(r"באיזה קטע נמצא $t=\mathbb E[X]=\frac59$ ומה נוסחת $F$ שם? (בערך $t=\frac59$)", [r"$\frac89t$, כי $\frac59<\frac34$", r"$t-\frac1{12}$, כי זו הנוסחה האחרונה", r"$t$"], 0,
        r"$\frac59\approx0.556<0.75$, ולכן $F=\frac89t=\frac{40}{81}\approx0.494$. הנוסחאות האחרות נותנות $0.472$ ו-$0.556$."),
     NU(r"מהי $P(X\le\mathbb E[X])$?", Fr(40, 81), r"$\frac89\cdot\frac59=\frac{40}{81}$.")])

# ---- Q5 (D=2, N=5, Q=D/N=0.4, p=0.5, n=4)
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

# ---- Q6 (bridge Q1; Q2=(A||B)-(C||D); p=0.6)
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
    RB((r"$Q_2=(A\cup B)\cap(C\cup D)$: שני מקבצים בטור", 3), (r"בלתי תלויים: $P(A\cup B)P(C\cup D)$", 3), (r"התשובה $(2p-p^2)^2$", 3)),
    [r"לבלבל בין טור ומקביל ולחשב $(p^2)^2$"],
    [CH(r"מהו המבנה של $Q_2$?", [r"שני מקבצים מקביליים ($A,B$) ו-($C,D$) בטור", r"ארבעה רכיבים בטור", r"ארבעה רכיבים במקביל"], 0,
        r"ב-$p=0.6$: המבנה הנכון נותן $0.7056$, ארבעה בטור נותנים $0.1296$, וארבעה במקביל נותנים $0.9744$."),
     NU(r"ב-$p=0.6$, מהי $P(A\cup B)$?", Fr("0.84"), r"$2p-p^2=0.84$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_2)$?", Fr("0.7056"), r"$0.84^2=0.7056$.")])

ADD(6, "ג",
    RB((r"$P(Q_1/Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}$", 1), (r"התניה על $E$: $P(\tilde Q/E)=2p^2-p^4$ ו-$P(\tilde Q/\bar E)=4p^3-3p^4$", 3), (r"$P(Q_1\cap Q_2)=p^3(6-7p+2p^2)$", 1), (r"התשובה $\frac{p(3-2p)}{2-p}$", 2)),
    [r"להכפיל $P(Q_1)P(Q_2)$ למרות שהמעגלים חולקים את אותם רכיבים", r"לחלק ב-$P(Q_1)$ במקום ב-$P(Q_2)$"],
    [CH(r"איך מחשבים את $P(Q_1\cap Q_2)$?",
        [r"בונים אירוע אחד $\tilde Q$ ומתנים ב-$E$ (שנמצא רק ב-$Q_1$)", r"$P(Q_1)P(Q_2)$ כי $Q_1,Q_2$ בלתי תלויים", r"$P(Q_1)+P(Q_2)-1$"], 0,
        r"שני המעגלים עושים שימוש באותם $A,B,C,D$ ולכן הם תלויים. ב-$p=0.6$: המכפלה $0.4654$, ו-$P(Q_1)+P(Q_2)-1=0.3651$, אבל הנכון $0.5443$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_2)$? (המכנה: אירוע התנאי)", Fr("0.7056"), r"מסעיף ב."),
     NU(r"באותו $p$: כש-$E$ פועלת, מהי $P(\tilde Q)$? ($(A\cap D)\cup(B\cap C)$)", Fr("0.5904"), r"$2p^2-p^4=0.5904$."),
     NU(r"כש-$E$ אינה פועלת, מהי $P(\tilde Q)$?", Fr("0.4752"), r"$4p^3-3p^4=0.864-0.3888=0.4752$."),
     NU(r"מהי $P(Q_1/Q_2)$?", Fr("0.54432") / Fr("0.7056"), r"$P(Q_1\cap Q_2)=0.6\cdot0.5904+0.4\cdot0.4752=0.54432$, ולכן $\frac{0.54432}{0.7056}=\frac{p(3-2p)}{2-p}=\frac{27}{35}\approx0.7714$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = "ai-draft"
        _q["stepsSource"] = "ai-draft"


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
