# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-E.json -- probability (course 20021-80), semester A 2024, moed B (reserve-duty
moed, 09.05.2024). Code 24A-E is fixed by GATE1. 6 questions, 25 items (Q1 4, Q2 4, Q3 5, Q4 4, Q5 4, Q6 4).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-E.py

Source: exam pp.1-3, official handwritten solutions pp.4-15.
Transcription notes
- Part keys are single letters (printed label is the bold token at the start of the question text).
  Q4 prints ג-1, ג-2 -> keys ג ד. Q5 prints א-1, א-2, א-3, ב -> keys א ב ג ד.
- Q3 bonus (key ה, printed "סעיף בונוס", cov[D,T]) has NO official solution in the source -> solved
  (solutionSource "solved", official:false): cov[D,T] = 2np^2(1-p), verified exactly and by Monte Carlo in
  tools/verify/24A-E/check.py (same question and answer as 24B-C Q3e).
- Q2(ד) asks to find the roots; the official solution only gives the probability (1/6). The roots (-1 and -5) are
  added as a one-line completion computed from the official event B∩C={35}, and marked as such.
- The portrait and money-bag pictures in the Q5 header are decoration and are not shipped.
- Q1 items carry a `region` (moved from the old regions.json); sims are checked by check_sim_specs; steps by tools/verify/24A-E/steps_check.py.
"""
import json, pathlib
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from verified import src as _vsrc

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-E.json"
CODE = "24A-E"
IMG = "images/exams/24A-E-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"חגב אשר נמצא בנקודה $O$ מבצע שתי קפיצות אקראיות: קפיצה ראשונה – שמאלה וקפיצה שנייה – ימינה. "
          r"בהנחה שאורכי הקפיצות שמאלה ($X_L$) וימינה ($X_R$) מהווים משתנים מקריים בלתי תלויים בעלי התפלגות אחידה רציפה "
          r"$X_L\sim U_c(0,1)$ ו-$X_R\sim U_c(0,2)$, ענו על השאלות הבאות:")
Q1_SOL = r"$X_L\sim U_c(0,1)$, $X_R\sim U_c(0,2)$. מרחב המדגם: המלבן $\Omega=(0,1)\times(0,2)$, ושטחו $|\Omega|=2$." "\n"

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א.** מהי ההסתברות שבתום הקפיצה השנייה החגב יחזור לנקודה $O$?",
    r"""מכיוון ש-$X_L$ ו-$X_R$ הם משתנים מקריים רציפים, מתקיים
$$P(X_L=X_R)=0.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**ב.** מהי ההסתברות שבתום הקפיצה השנייה החגב ימצא את עצמו **ימינה** מנקודה $O$?",
    Q1_SOL + r"""$$P(X_R>X_L)=\frac{|\{x_R>x_L\}|}{|\Omega|}=\frac{2-\frac12}{2}=\frac34.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**ג.** מהי ההסתברות שבתום הקפיצה השנייה החגב ימצא את עצמו **שמאלה** מנקודה $O$?",
    r"""$$P(X_R<X_L)=1-\frac34=\frac14.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"**ד.** מהי ההסתברות שבתום הקפיצה השנייה החגב ימצא את עצמו **ימינה** מנקודה $O$ במרחק ממנה אשר לא עולה על $\frac13$?",
    Q1_SOL + r"""$$P\left(0<X_R-X_L<\tfrac13\right)=P\left(X_R>X_L\cap X_R<X_L+\tfrac13\right)=\frac{\left|\{x_R>x_L\}\cap\{x_R<x_L+\frac13\}\right|}{|\Omega|}$$
השטח הרצוי הוא שטח הטרפז (בין הישרים $x_R=x_L$ ו-$x_R=x_L+\frac13$, מעל $x_L\in(0,1)$) פחות המשולש הקטן החסר:
$$=\frac{1\cdot\frac{\frac13+\frac43}{2}-\frac12}{2}=\frac{\frac56-\frac12}{2}=\frac16.$$""",
    6, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_TXT = (r"מטילים קובייה **מאוזנת פעמיים** על מנת לקבוע את המקדמים $X_1$ ו-$X_2$ במשוואה הריבועית $y^2+2X_1y+X_2=0$. "
          r"כאן $X_1$ ו-$X_2$ הם משתנים מקריים המסמנים את תוצאות ההטלה הראשונה והשנייה בהתאמה.")
Q2_SOL = (r"שורשי המשוואה: $y_1=-X_1-\sqrt{X_1^2-X_2}$, $\ y_2=-X_1+\sqrt{X_1^2-X_2}$. $\ \Omega=\{11,\dots,16,21,\dots,26,\dots,61,\dots,66\}$, $|\Omega|=36$." "\n")

questions.append(Q(
    2, "א", "combinatorics",
    Q2_TXT + "\n" + r"**א.** מצאו את ההסתברות ששורשי המשוואה יהיו מרוכבים.",
    Q2_SOL + r"""השורשים מרוכבים אם ורק אם $X_1^2<X_2$, כלומר $A=\{12,\dots,16;\,25,26\}$.
$$P(X_1^2<X_2)=\frac{|A|}{|\Omega|}=\frac7{36}.$$""",
    8))

questions.append(Q(
    2, "ב", "combinatorics",
    Q2_TXT + "\n" + r"**ב.** מהי ההסתברות ששורשי המשוואה יהיו **מספרים שלמים**?",
    Q2_SOL + r"""השורשים שלמים אם ורק אם $X_1^2-X_2$ הוא ריבוע של מספר שלם. מתקבל
$B=\{11,23,24,35\}$ ($X_1^2-X_2=0,1,0,4$ בהתאמה), ולכן
$$P(B)=\frac{|B|}{|\Omega|}=\frac4{36}=\frac19.$$""",
    8))

questions.append(Q(
    2, "ג", "conditional_bayes",
    Q2_TXT + "\n" + r"**ג.** **אם ידוע** כי שורשי המשוואה ממשיים, מהי ההסתברות שהם מהווים מספרים שלמים?",
    r"""שורשים ממשיים: $\bar A$ (המשלים של $A$ מהסעיף הראשון), $|\bar A|=|\Omega|-|A|=36-7=29$. $B\cap\bar A=\{11,23,24,35\}$, $|B\cap\bar A|=4$.
$$P(B/\bar A)=\frac{P(B\cap\bar A)}{P(\bar A)}=\frac{|B\cap\bar A|}{|\Omega|-|A|}=\frac4{29}.$$""",
    4))

questions.append(Q(
    2, "ד", "conditional_bayes",
    Q2_TXT + "\n" + r"**ד.** **אם ידוע** כי בהטלה הראשונה התקבלה תוצאה ״3״, מהי ההסתברות ששורשי המשוואה הם מספרים שלמים? מצאו את השורשים במקרה זה.",
    r"""$C$ = ״בהטלה הראשונה התקבלה 3״ $=\{31,\dots,36\}$, $B\cap C=\{35\}$.
$$P(B/C)=\frac{|B\cap C|}{|C|}=\frac16.$$
(השלמה, לפי $B\cap C=\{35\}$, כלומר $X_1=3,\ X_2=5$: המשוואה $y^2+6y+5=0$ והשורשים $y=-3\pm\sqrt{9-5}=-1,\,-5$.)""",
    5))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"נתבונן בסדרה של $n$ מטריצות ברנולי מהצורה" "\n"
          r"$$\boldsymbol Q_1=\begin{pmatrix}0&-X_1\\Y_1&X_1+Y_1\end{pmatrix},\ \boldsymbol Q_2=\begin{pmatrix}0&-X_2\\Y_2&X_2+Y_2\end{pmatrix},\ \dots,\ \boldsymbol Q_n=\begin{pmatrix}0&-X_n\\Y_n&X_n+Y_n\end{pmatrix},$$" "\n"
          r"כאשר $X_j$ ו-$Y_j$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגות ברנולי: $X_j\sim\mathrm{Ber}(p)$ ו-$Y_j\sim\mathrm{Ber}(p)$ עבור כל $j=1,\dots,n$. "
          r"נגדיר שני משתנים מקריים חדשים עבור כל מטריצה $\boldsymbol Q_j$: דטרמיננטה $D_j=\det\boldsymbol Q_j$ ועקבה $T_j=\operatorname{tr}\boldsymbol Q_j$.")

questions.append(Q(
    3, "א", "special_discrete",
    r"**א.** מצאו את פונקציית ההסתברות של משתנה מקרי $D_1$. מה שם ההתפלגות של $D_1$ ומהם הפרמטרים של ההתפלגות?",
    r"""$D_j=X_jY_j$, $\ T_j=X_j+Y_j$.
מכיוון ש-$X_j\sim\mathrm{Ber}(p)$ ו-$Y_j\sim\mathrm{Ber}(p)$, כל אחד מהם מקבל את הערכים $0$ ו-$1$. לכן $X_jY_j$ מקבל את הערך $1$ אם ורק אם שניהם מקבלים $1$ (ואחרת $0$). לכן
$$D_j=X_jY_j\sim\mathrm{Ber}(p^2),$$
כלומר $P(D_1=1)=p^2$ ו-$P(D_1=0)=1-p^2$.""",
    8, contextId="c3"))

questions.append(Q(
    3, "ב", "special_discrete",
    r"**ב.** מצאו את פונקציית ההסתברות של משתנה מקרי $T_1$. מה שם ההתפלגות של $T_1$ ומהם הפרמטרים של ההתפלגות?",
    r"""$T_j=X_j+Y_j$ הוא סכום של שני משתני ברנולי בלתי תלויים בעלי אותו פרמטר $p$. לפי משפט הפירוק
$$T_j\sim\mathrm{Bin}(2,p).$$""",
    8, contextId="c3"))

questions.append(Q(
    3, "ג", "special_discrete",
    r"**ג.** נגדיר משתנה חדש $D=\sum_{j=1}^nD_j$. איך משתנה $D$ מפולג? **נמקו היטב!**",
    r"""$D=\sum_{j=1}^nD_j$ הוא סכום של $n$ משתנים בלתי תלויים, כל אחד $D_j\sim\mathrm{Ber}(p^2)$. באמצעות משפט הפירוק ניתן להוכיח (הוכיחו!) כי
$$D\sim\mathrm{Bin}(n,p^2).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ד", "special_discrete",
    r"**ד.** נגדיר משתנה חדש $T=\sum_{j=1}^nT_j$. איך משתנה $T$ מפולג? **נמקו היטב!**",
    r"""$T=\sum_{j=1}^nT_j$ הוא סכום של $n$ משתנים בלתי תלויים, כל אחד $T_j\sim\mathrm{Bin}(2,p)$. באמצעות משפט הפירוק ניתן להוכיח (הוכיחו!) כי
$$T\sim\mathrm{Bin}(2n,p).$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ה", "joint_discrete",
    r"**סעיף בונוס** (אין חובה לפתור!): חשבו את השונות המשותפת $\operatorname{cov}[D,T]$ של משתנים חדשים $D$ ו-$T$.",
    r"""**פתרון (אין פתרון רשמי לסעיף הבונוס).**
לפי הבילינאריות של השונות המשותפת,
$$\operatorname{cov}[D,T]=\operatorname{cov}\Big[\sum_{j=1}^nD_j,\ \sum_{k=1}^nT_k\Big]=\sum_{j=1}^n\sum_{k=1}^n\operatorname{cov}[D_j,T_k].$$
עבור $j\ne k$ המשתנה $D_j$ תלוי רק בזוג $(X_j,Y_j)$ ו-$T_k$ רק בזוג $(X_k,Y_k)$, והזוגות בלתי תלויים, ולכן $\operatorname{cov}[D_j,T_k]=0$. נשארים רק האיברים $j=k$:
$$\operatorname{cov}[D,T]=n\operatorname{cov}[D_1,T_1]=n\big(\operatorname{cov}[X_1Y_1,X_1]+\operatorname{cov}[X_1Y_1,Y_1]\big).$$
מאחר ש-$X_1^2=X_1$ (ברנולי) ו-$X_1,Y_1$ בלתי תלויים,
$$\operatorname{cov}[X_1Y_1,X_1]=\mathbb{E}[X_1^2Y_1]-\mathbb{E}[X_1Y_1]\,\mathbb{E}[X_1]=p\cdot p-p^2\cdot p=p^2(1-p),$$
ומאותה סימטריה גם $\operatorname{cov}[X_1Y_1,Y_1]=p^2(1-p)$. לכן
$$\operatorname{cov}[D,T]=2np^2(1-p).$$""",
    5, contextId="c3", solutionSource="solved", official=False))

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"נתבונן במשתנה מקרי $X$ בעל פונקציית הצפיפות מהצורה" "\n"
          r"$$f(x)=\begin{cases}a(b^2-x^2),&-b\le x\le b\\ 0,&\text{else}\end{cases}$$" "\n"
          r"כאשר $a>0$ ו-$b>0$.")

questions.append(Q(
    4, "א", "continuous_rv",
    Q4_TXT + "\n" + r"**א.** מצאו את תוחלת המשתנה $\mathbb E[X]$. (אם יהיה בכך צורך, ניתן לבטא אותה דרך המקדמים $a$ ו-$b$).",
    r"""$$\mathbb E[X]=\int_{-b}^{+b}x\,f_X(x)\,dx=0,$$
כי האינטגרנד $x\,f_X(x)$ אי-זוגי והתחום סימטרי.""",
    6))

questions.append(Q(
    4, "ב", "continuous_rv",
    Q4_TXT + "\n" + r"**ב.** חשבו את המקדמים $a$ ו-$b$ אם נתון כי השונות $\operatorname{var}[X]=\frac{3}{15}$.",
    r"""נרמול:
$$1=2\int_0^b f_X(x)\,dx=2a\int_0^b(b^2-x^2)\,dx=2a\left(b^3-\frac{b^3}{3}\right)=\frac{4ab^3}{3}\ \Rightarrow\ 4ab^3=3.$$
שונות (כי $\mathbb E[X]=0$):
$$\operatorname{Var}[X]=\mathbb E[X^2]=2a\int_0^b x^2(b^2-x^2)\,dx=2a\left(\frac{b^5}{3}-\frac{b^5}{5}\right)=\frac{4a}{15}b^5=\frac3{15}\ \Rightarrow\ 4ab^5=3.$$
מחלקים את שתי המשוואות: $b^2=1$, כלומר
$$a=\frac34,\qquad b=1.$$""",
    6))

questions.append(Q(
    4, "ג", "continuous_rv",
    Q4_TXT + "\n" + r"בהינתן המקדמים $a$ ו-$b$ מהסעיף הקודם:" "\n" r"**ג-1:** חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו אותה.",
    r"""$$f_X(x)=\begin{cases}\dfrac34(1-x^2),&-1<x<1\\0,&\text{else}\end{cases}$$
(הצפיפות היא פרבולה).
$$F_X(t)=\int_{-\infty}^t f_X(x)\,dx=\begin{cases}0,&t<-1,\\ \dfrac34\displaystyle\int_{-1}^t(1-x^2)\,dx,&-1\le t<1,\\ 1,&t\ge1.\end{cases}$$
$\displaystyle\int_{-1}^t(1-x^2)\,dx=\left(x-\frac{x^3}{3}\right)\Big|_{-1}^t=\frac23+t-\frac{t^3}{3}$. לכן
$$F_X(t)=\begin{cases}0,&t<-1,\\ \dfrac14\left(2+3t-t^3\right),&-1\le t<1,\\ 1,&t\ge1.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת](images/exams/24A-E-Q4-cdf.png)""",
    7))

questions.append(Q(
    4, "ד", "continuous_rv",
    Q4_TXT + "\n" + r"בהינתן המקדמים $a$ ו-$b$ מהסעיף הקודם:" "\n" r"**ג-2:** מצאו את ההסתברות המותנית $P(X>a\,/\,|X|<b)$.",
    r"""$$P(X>a/|X|<b)=P\left(X>\tfrac34\,\Big/\,|X|<1\right)=\frac{P\left(\frac34<X<1\right)}{P(-1<X<1)}=\frac{F_X(1)-F_X\left(\frac34\right)}{F_X(1)-F_X(-1)}=\frac{11}{256}.$$
(כאן $F_X(1)=1$ ו-$F_X(-1)=0$.)""",
    6))

# ------------------------------------------------------------------ Q5
Q5_TXT = (r"ב-21 ביוני – יום הולדת של סימאון פואסון – החליט מפעל הפיס לחלק פרסים כספיים לאנשים אשר יתקשרו למוקד החברה. "
          r"כאשר מגיעה שיחה למוקד, איש צוות מטיל מטבע מוטה (בעל הסתברות $p$ לקבלת תוצאת ״עץ״). אם מתקבלת תוצאת ״עץ״ בהטלה, "
          r"מפעל הפיס מעניק 1,000 דולר לפונה. במקרה של ״פלי״ הפרס לא יוענק.")
Q5_A = (r"יהי $X$ משתנה מקרי המתאר את **מספר הזוכים בפרס** כספי במהלך המשמרת. בהנחה כי מספר הפונים למוקד מפעל הפיס במהלך המשמרת "
        r"מהווה משתנה פואסון בעל פרמטר $\lambda>0$,")
Q5_HINT = (r"**הערה:** לידיעתך," "\n"
           r"$$\sum_{j=k}^{\infty}C_j^k\frac{a^j}{j!}=\frac{a^k}{k!}e^a.$$" "\n"
           r"(יכול להיות שאין צורך להשתמש בנוסחה זו.)")

questions.append(Q(
    5, "א", "special_discrete",
    Q5_A + "\n" + r"**א-1:** מצאו את פונקציית ההסתברות של משתנה מקרי $X$.",
    r"""נגדיר $X=$ מספר הזוכים בפרס (בדולר $1000$) בין מי שפנה למוקד, ו-$Y=$ מספר האנשים אשר פנו למוקד במהלך המשמרת.
$Y\sim P(\lambda)\ \Rightarrow\ P(Y=j)=\dfrac{\lambda^j}{j!}e^{-\lambda}$, $\ j=0,1,\dots$

הערכים האפשריים של $X$ הם $k=0,1,2,\dots$
$$P(X=k)=\sum_{j=k}^{\infty}P(X=k/Y=j)\,P(Y=j)=\sum_{j=k}^{\infty}\binom jk p^k(1-p)^{j-k}\,\frac{\lambda^j}{j!}e^{-\lambda}$$
$$=\frac{p^k}{(1-p)^k}\,e^{-\lambda}\sum_{j=k}^{\infty}\binom jk\frac{[\lambda(1-p)]^j}{j!}.$$
לפי הנוסחה שבהערה, הסכום שווה ל-$\dfrac{\lambda^k(1-p)^k}{k!}e^{\lambda-\lambda p}$, ולכן
$$P(X=k)=\frac{(\lambda p)^k}{k!}e^{-\lambda p},\qquad X\sim P(p\lambda).$$""",
    8, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    Q5_A + "\n" + r"**א-2:** ודאו כי תכונת הנורמול עבור תשובתכם בסעיף א-1 מתקיימת.",
    r"""$$\sum_{k=0}^{\infty}P(X=k)=e^{-\lambda p}\sum_{k=0}^{\infty}\frac{(\lambda p)^k}{k!}=e^{-\lambda p}\,e^{\lambda p}=1.$$""",
    6, contextId="c5"))

questions.append(Q(
    5, "ג", "special_discrete",
    Q5_A + "\n" + r"**א-3:** חשבו תוחלת $\mathbb E[X]$ ושונות $\operatorname{var}[X]$ של מספר הזוכים בפרס.",
    r"""מכיוון ש-$X\sim P(p\lambda)$, מתקיים (מההתפלגות הפואסונית הישירות)
$$\mathbb E[X]=p\lambda,\qquad \operatorname{Var}[X]=p\lambda.$$""",
    6, contextId="c5"))

questions.append(Q(
    5, "ד", "conditional_bayes",
    Q5_A + "\n" + r"**ב.** אם ידוע כי זכו בפרס $n$ פונים, מהי ההסתברות שבמהלך המשמרת הגיעו למוקד בדיוק $N$ פניות?" "\n" + Q5_HINT,
    r"""לפי נוסחת בייס:
$$P(Y=N/X=n)=\frac{P(X=n/Y=N)\,P(Y=N)}{P(X=n)}=\frac{\binom Nn p^n(1-p)^{N-n}\cdot\dfrac{\lambda^N}{N!}e^{-\lambda}}{\dfrac{(p\lambda)^n}{n!}e^{-p\lambda}}.$$
בצמצום מתקבל
$$P(Y=N/X=n)=\frac{[\lambda(1-p)]^{N-n}}{(N-n)!}\,e^{-\lambda(1-p)},\qquad N\ge n.$$""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_TXT = (r"ארבעה רכיבים $A,B,C$ ו-$D$ פועלים בהסתברויות זהות $P(A)=P(B)=P(C)=P(D)=p$ וללא תלות אחד בשני. "
          r"מרכיבים אלה הורכב המעגל הראשון ($Q_1$) ולאחר מכן – המעגל השני ($Q_2$), בהתאם לאיור.")

questions.append(Q(
    6, "א", "circuits",
    r"**א.** מהי ההסתברות $P(Q_1)$ שהמעגל הראשון יפעל?",
    r"""$Q_1=D\cap\bigl((A\cap B)\cup C\bigr)$, והרכיב $D$ בלתי תלוי ביתר:
$$P(Q_1)=P(D)\,P\bigl((A\cap B)\cup C\bigr)=p\,(p+p^2-p^3)=p^2\,(1+p-p^2).$$""",
    7, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"**ב.** מהי ההסתברות שלפחות מעגל אחד משני המעגלים $Q_1$ ו-$Q_2$ יפעל?",
    r"""נסמן $\tilde Q=Q_1\cup Q_2$ ונחשב בהתניה על $B$:
$$P(\tilde Q)=P(\tilde Q/B)\,P(B)+P(\tilde Q/\bar B)\,P(\bar B).$$
- $\tilde Q/B$: שני המסלולים מצטמצמים ל-$D\cap(A\cup C)$, כלומר $P(\tilde Q/B)=P\bigl(D\cap(A\cup C)\bigr)=p(2p-p^2)=p^2(2-p)$;
- $\tilde Q/\bar B$: $(D\cap C)\cup(D\cap A)=D\cap(A\cup C)$, כלומר $P(\tilde Q/\bar B)=p^2(2-p)$.

בסך הכול
$$P(\tilde Q)=P(Q_1\cup Q_2)=p^2(2-p).$$""",
    7, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    r"**ג.** **אם ידוע** כי מעגל $Q_1$ פעיל, מהי ההסתברות שגם המעגל $Q_2$ יפעל?",
    r"""$$P(Q_2/Q_1)=\frac{P(Q_1\cap Q_2)}{P(Q_1)},\qquad P(Q_1)=p^2(1+p-p^2).$$
$P(Q_1\cup Q_2)=P(Q_1)+P(Q_2)-P(Q_1\cap Q_2)$, ו-$P(Q_1)=P(Q_2)$ (סימטריה בין $A$ ל-$C$), ולכן
$$P(Q_1\cap Q_2)=2P(Q_1)-P(\tilde Q)=2p^2(1+p-p^2)-p^2(2-p)=p^3(3-2p).$$
לכן
$$P(Q_2/Q_1)=\frac{p(3-2p)}{1+p-p^2}.$$""",
    7, contextId="c6"))

questions.append(Q(
    6, "ד", "circuits",
    r"**ד.** **אם ידוע** כי שני המעגלים פועלים, מהי ההסתברות שכל הרכיבים תקינים (כלומר, פועלים)?",
    r"""$$P\bigl(A\cap B\cap C\cap D\,/\,Q_1\cap Q_2\bigr)=\frac{P(Q_1\cap Q_2/A\cap B\cap C\cap D)\,P(A\cap B\cap C\cap D)}{P(Q_1\cap Q_2)}=\frac{1\cdot p^4}{p^3(3-2p)}=\frac{p}{3-2p}.$$""",
    4, contextId="c6"))

# ---- regions (region.js), "simulate it" specs (sim.js) and rubric / pitfalls / guided steps (ai-draft) -----------------
# Regions were moved here from tools/verify/<CODE>/regions.json. Every sim `exact` is the shipped final answer (symbolic
# answers are simulated at a sample value stated in `estimate`). Every expected step value is re-derived independently,
# exactly and by Monte Carlo, in tools/verify/<CODE>/steps_check.py (which reads the generated raw JSON back).
import math
from fractions import Fraction as Fr

U01 = {"x": [0, 1], "y": [0, 1]}
XY = {"x": "X", "y": "Y"}


def lin(a, b, c, op):
    return {"a": a, "b": b, "c": c, "op": op}


def REG(event, exact, caption, given=None, space=U01, labels=XY):
    r = {"space": space, "labels": labels, "event": event, "exact": exact, "caption": caption}
    if given:
        r["given"] = given
    return r


def AREA(label, exact, **kw):
    return {"kind": "area", "estimate": label, "exact": exact, "params": dict(kw) if kw else {"fromRegion": True}}


def PDF(label, exact, pieces, event=None, given=None, measure=None, expr=None):
    p = {"pieces": [{"from": a, "to": b, "expr": x} for a, b, x in pieces]}
    if event:
        p["event"] = event
    if given:
        p["given"] = given
    if measure:
        p["measure"] = measure
        p["expr"] = expr
    return {"kind": "pdf", "estimate": label, "exact": exact, "params": p}


def URN(label, exact, draws, event=None, given=None, values=None, counts=None, measure=None, expr=None):
    p = {"draws": draws}
    if values is not None:
        p["values"] = values
    else:
        p["counts"] = counts
    if event:
        p["event"] = event
    if given:
        p["given"] = given
    if measure:
        p["measure"] = measure
        p["expr"] = expr
    return {"kind": "urn", "estimate": label, "exact": exact, "params": p}


def DICE(label, exact, n, event, given=None, faces=None):
    p = {"n": n, "event": event}
    if faces:
        p["faces"] = faces
    if given:
        p["given"] = given
    return {"kind": "dice", "estimate": label, "exact": exact, "params": p}


def CUST(label, exact, vs, event=None, given=None, measure=None, expr=None, trials=None):
    """vs: {name: (values, probs)}."""
    p = {"vars": {k: {"values": v, "probs": pr} for k, (v, pr) in vs.items()}}
    if event:
        p["event"] = event
    if given:
        p["given"] = given
    if measure:
        p["measure"] = measure
        p["expr"] = expr
    s = {"kind": "custom_discrete", "estimate": label, "exact": exact, "params": p}
    if trials:
        s["trials"] = trials
    return s


def CIRC(label, exact, probs, event, given=None):
    """probs: {component id: p}; the network only declares the components, the event is the structure function."""
    p = {"event": event, "network": {"type": "series", "children": [{"type": "comp", "id": c, "p": v} for c, v in probs.items()]}}
    if given:
        p["given"] = given
    return {"kind": "circuit", "estimate": label, "exact": exact, "params": p}


def BER(p, *names):
    return {n: ([0, 1], [1 - p, p]) for n in names}


def BIN(n, p):
    from math import comb
    return (list(range(n + 1)), [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)])


EXTRAS = {}


def O(*v):
    return [{"id": "abcdefgh"[i], "value": t} for i, t in enumerate(v)]


def CH(prompt, opts, ans, explain):
    return {"type": "choice", "prompt": prompt, "options": O(*opts), "correctId": "abcdefgh"[ans], "explain": explain}


def NU(prompt, val, explain, tol=None):
    """numeric step: exact (tol 0) when the value has <= 4 decimals, else 6 significant digits with a small tolerance."""
    v = float(val)
    r = round(v, 4)
    if abs(v - r) < 1e-12:
        return {"type": "numeric", "prompt": prompt, "answer": r, "tol": 0, "explain": explain}
    a = float("%.6g" % v)
    t = tol if tol is not None else min(0.0006, abs(a) * 0.005)
    return {"type": "numeric", "prompt": prompt + " (שבר או עשרוני)", "answer": a, "tol": t, "explain": explain}


def RB(*r):
    return [{"text": t, "points": p} for t, p in r]


S = {}


def ADD(num, part, rub, pit, steps):
    S[(num, part)] = (rub, pit, steps)


def APPLY(questions):
    for q in questions:
        k = (q["num"], q.get("part"))
        x = EXTRAS.get(k)
        if x:
            q.update(x)
        s = S.get(k)
        if s and not q.get("hold"):
            tot = sum(r["points"] for r in s[0])
            assert tot == q["points"], (k, tot, q["points"])
            assert 2 <= len(s[2]) <= 5, (k, len(s[2]))
            q["rubric"], q["pitfalls"], q["steps"] = s[0], s[1], s[2]
            q["rubricSource"] = _vsrc(CODE)
            q["stepsSource"] = _vsrc(CODE)
    assert set(S) <= {(q["num"], q.get("part")) for q in questions}, "steps for unknown items"


# ---- 24A-E specifics: area figures, simulations, steps
S12 = {"x": [0, 1], "y": [0, 2]}
LLR = {"x": "X_L", "y": "X_R"}
_P3 = 0.3                                    # sample p for the Bernoulli-matrix answers (n = 3 matrices)
_XY3 = ["X%d" % i for i in range(1, 4)] + ["Y%d" % i for i in range(1, 4)]
_DS = "X1*Y1+X2*Y2+X3*Y3"
_TS = "+".join(_XY3)
_INT = " or ".join("d1^2 - d2 == %d" % k for k in (0, 1, 4, 9, 16, 25))   # integer roots: the discriminant is a perfect square
_pdf4 = [(-1, 1, "3/4*(1-x^2)")]
_p6 = 0.6
_Q1E = "D and ((A and B) or C)"
_Q2E = "D and ((C and B) or A)"
_pAB4 = {c: _p6 for c in "ABCD"}
_PQ1 = _p6 ** 2 * (1 + _p6 - _p6 ** 2)
_PU = _p6 ** 2 * (2 - _p6)
_PI = _p6 ** 3 * (3 - 2 * _p6)

EXTRAS.update({
    (1, "א"): {"region": REG(["y == x"], 0, "האירוע X_R=X_L: קו, ושטחו 0 (יחידות של האורך)", space=S12, labels=LLR),
               "sim": AREA("P(X_R=X_L)", 0, space=S12, event="y == x")},
    (1, "ב"): {"region": REG([lin(-1, 1, 0, ">")], 3 / 4, "האירוע X_R>X_L", space=S12, labels=LLR), "sim": AREA("P(X_R>X_L)", 3 / 4)},
    (1, "ג"): {"region": REG([lin(-1, 1, 0, "<")], 1 / 4, "האירוע X_R<X_L", space=S12, labels=LLR), "sim": AREA("P(X_R<X_L)", 1 / 4)},
    (1, "ד"): {"region": REG([lin(-1, 1, 0, ">"), lin(-1, 1, "1/3", "<")], 1 / 6, "האירוע 0<X_R-X_L<1/3", space=S12, labels=LLR), "sim": AREA("P(0<X_R-X_L<1/3)", 1 / 6)},
    (2, "א"): {"sim": DICE("P(שורשים מרוכבים)", 7 / 36, 2, "d1^2 < d2")},
    (2, "ב"): {"sim": DICE("P(שורשים שלמים)", 1 / 9, 2, _INT)},
    (2, "ג"): {"sim": DICE("P(שלמים | ממשיים)", 4 / 29, 2, _INT, "d1^2 >= d2")},
    (2, "ד"): {"sim": DICE("P(שלמים | X1=3)", 1 / 6, 2, _INT, "d1 == 3")},
    (3, "א"): {"sim": CUST("P(D1=1) ב-p=0.3", 0.09, BER(_P3, "X", "Y"), event="X*Y == 1")},
    (3, "ב"): {"sim": CUST("P(T1=1) ב-p=0.3", 0.42, BER(_P3, "X", "Y"), event="X+Y == 1")},
    (3, "ג"): {"sim": CUST("P(D=1) ב-n=3, p=0.3", 3 * 0.09 * 0.91 ** 2, BER(_P3, *_XY3), event=_DS + " == 1")},
    (3, "ד"): {"sim": CUST("P(T=2) ב-n=3, p=0.3", 15 * 0.09 * 0.7 ** 4, BER(_P3, *_XY3), event=_TS + " == 2")},
    (3, "ה"): {"sim": CUST("cov[D,T] ב-n=3, p=0.3", 2 * 3 * 0.09 * 0.7, BER(_P3, *_XY3), measure="cov", expr=[_DS, _TS])},
    (4, "א"): {"sim": PDF("E[X] ב-a=3/4, b=1", 0, _pdf4, measure="mean", expr="x")},
    (4, "ב"): {"sim": PDF("Var[X] ב-a=3/4, b=1", 1 / 5, _pdf4, measure="var", expr="x")},
    (4, "ג"): {"sim": PDF("F_X(1/2)=P(X<=1/2)", 27 / 32, _pdf4, "x <= 1/2")},
    (4, "ד"): {"sim": PDF("P(X>3/4 | |X|<1)", 11 / 256, _pdf4, "x > 3/4", "abs(x) < 1")},
    (6, "א"): {"sim": CIRC("P(Q1) ב-p=0.6", _PQ1, _pAB4, _Q1E)},
    (6, "ב"): {"sim": CIRC("P(Q1 או Q2) ב-p=0.6", _PU, _pAB4, "(" + _Q1E + ") or (" + _Q2E + ")")},
    (6, "ג"): {"sim": CIRC("P(Q2 | Q1) ב-p=0.6", _PI / _PQ1, _pAB4, _Q2E, _Q1E)},
    (6, "ד"): {"sim": CIRC("P(כל הרכיבים פועלים | Q1 וגם Q2) ב-p=0.6", _p6 / (3 - 2 * _p6), _pAB4, "A and B and C and D", "(" + _Q1E + ") and (" + _Q2E + ")")},
})

OMR = r"מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X_L,X_R)$, כלומר המלבן $(0,1)\times(0,2)$?"
OMR_X = r"המלבן ברוחב $1$ ובגובה $2$ הוא מרחב המדגם, ושטחו $2$. ההסתברות היא שטח האירוע חלקי $2$."

ADD(1, "א",
    RB((r"אי-השוויון מתאר קו במישור $(x_L,x_R)$, ושטחו $0$", 3), (r"$P=\frac{0}{|\Omega|}=0$ (משתנים רציפים)", 2)),
    [r"לכתוב $\frac12$ או $\frac1{2}$ בטענה שהקפיצות ״סימטריות״", r"לחשוב שאירוע בעל הסתברות $0$ הוא בלתי אפשרי"],
    [NU(OMR, 2, OMR_X),
     CH(r"מדוע $P(X_L=X_R)=0$?",
        [r"האירוע הוא קו במלבן, ושטח קו הוא $0$ (משתנים רציפים)", r"כי $X_L\ne X_R$ בכל תוצאה אפשרית", r"כי לשני המשתנים התפלגויות שונות, ולכן הם לא שווים לעולם"], 0,
        r"שוויון אפשרי כנקודה על האלכסון, אך לאלכסון אין שטח. לכן ההסתברות $0$ אינה אומרת ״בלתי אפשרי״, והשוני בטווחים אינו מונע שוויון (למשל $0.5$)."),
     NU(r"מהו שטח הקו $\{x_R=x_L\}$ בתוך המלבן?", 0, r"לקו אין עובי ולכן אין שטח; $P=\frac02=0$.")])

ADD(1, "ב",
    RB((r"מרחב המדגם: $|\Omega|=2$", 1), (r"האירוע $X_R>X_L$ הוא המלבן פחות המשולש שמתחת לאלכסון", 3), (r"שטח $\frac32$ והתשובה $\frac34$", 3)),
    [r"לחשוב שהסתברות היא $\frac12$ בגלל סימטריה (הטווחים שונים)", r"לחלק ב-$1$ במקום ב-$2$"],
    [NU(OMR, 2, OMR_X),
     NU(r"מהו שטח המשלים $\{x_R\le x_L\}$ בתוך המלבן? (משולש מתחת לאלכסון)", Fr(1, 2), r"האלכסון מגיע עד $(1,1)$ בתוך המלבן; המשולש שמתחתיו בעל ניצבים $1$ ו-$1$: שטח $\frac12$."),
     NU(r"מהו שטח האירוע $\{x_R>x_L\}$?", Fr(3, 2), r"$2-\frac12=\frac32$."),
     NU(r"מהי $P(X_R>X_L)$?", Fr(3, 4), r"$\frac{3/2}{2}=\frac34$.")])

ADD(1, "ג",
    RB((r"הסתברות המשלים: $1-P(X_R>X_L)$ (מכיוון ש-$P(X_R=X_L)=0$)", 3), (r"או חישוב שטח המשולש $\frac12$ וחלוקה ב-$2$", 3), (r"התשובה $\frac14$", 1)),
    [r"להניח $\frac12$ מסימטריה", r"לשכוח שמשתנים רציפים ולכן אין שוויון"],
    [NU(OMR, 2, OMR_X),
     NU(r"מהו שטח האירוע $\{x_R<x_L\}$ בתוך המלבן? (המשולש מתחת לאלכסון)", Fr(1, 2), r"ניצבים $1$ ו-$1$: שטח $\frac12$."),
     NU(r"מהי $P(X_R<X_L)$?", Fr(1, 4), r"$\frac{1/2}{2}=\frac14$ (וגם $1-\frac34$).")])

ADD(1, "ד",
    RB((r"תיאור האירוע כרצועה בין $x_R=x_L$ ל-$x_R=x_L+\frac13$", 2), (r"שטח הרצועה: $\frac13$ (רוחב אנכי $\frac13$ לאורך $x_L\in(0,1)$; הרצועה כולה בתוך המלבן)", 3), (r"התשובה $\frac16$", 1)),
    [r"לחשב את הרצועה כטרפז ולהחסיר משולש לא נכון", r"לשכוח את החילוק ב-$|\Omega|=2$"],
    [NU(OMR, 2, OMR_X),
     NU(r"מהו שטח הרצועה $\{x_L<x_R<x_L+\frac13\}$ בתוך המלבן?", Fr(1, 3), r"לכל $x_L\in(0,1)$ ערכי $x_R$ הם בקטע באורך $\frac13$ (ו-$x_L+\frac13<2$), ולכן שטח $1\cdot\frac13=\frac13$."),
     NU(r"מהי $P(0<X_R-X_L<\frac13)$?", Fr(1, 6), r"$\frac{1/3}{2}=\frac16$.")])

# ---- Q2: quadratic y^2 + 2 X1 y + X2 = 0 with two fair dice
ADD(2, "א",
    RB((r"מרחב המדגם: $36$ זוגות סדורים שוות סיכוי", 2), (r"שורשים מרוכבים אם ורק אם המבחין שלילי: $X_1^2<X_2$", 3), (r"ספירה $|A|=7$ והתשובה $\frac7{36}$", 3)),
    [r"לבלבל בין מרוכבים לממשיים ולכתוב $\frac{29}{36}$", r"לספור זוגות עם $X_1<X_2$ (15) במקום $X_1^2<X_2$"],
    [CH(r"במשוואה $y^2+2X_1y+X_2=0$, מתי השורשים מרוכבים (אינם ממשיים)?",
        [r"כאשר $X_1^2<X_2$", r"כאשר $X_1^2>X_2$", r"כאשר $X_1<X_2$"], 0,
        r"המבחין הוא $4X_1^2-4X_2$ ושורשים לא ממשיים כאשר הוא שלילי. $X_1^2>X_2$ נותן שורשים ממשיים שונים, ו-$X_1<X_2$ אינו התנאי על המבחין (למשל $X_1=2,X_2=3$ נותן שורשים ממשיים)."),
     NU(r"כמה זוגות $(X_1,X_2)$ מקיימים $X_1^2<X_2$?", 7, r"$X_1=1$: $X_2=2,\dots,6$ (חמישה); $X_1=2$: $X_2=5,6$ (שניים); $X_1\ge3$: אף אחד. סך הכול $7$."),
     NU(r"מהי ההסתברות ששורשי המשוואה מרוכבים?", Fr(7, 36), r"$\frac7{36}$.")])

ADD(2, "ב",
    RB((r"שורשים שלמים אם ורק אם המבחין (חלקי 4) $X_1^2-X_2$ הוא ריבוע של שלם אי-שלילי", 3), (r"המאורע $B=\{11,23,24,35\}$", 3), (r"התשובה $\frac19$", 2)),
    [r"להסתפק בכך שהמבחין חיובי", r"לשכוח את המקרה של שורש כפול ($X_1^2=X_2$)"],
    [CH(r"במשוואה $y^2+2X_1y+X_2=0$, מתי השורשים מספרים שלמים?",
        [r"כאשר $X_1^2-X_2$ הוא ריבוע של מספר שלם אי-שלילי", r"כאשר $X_1^2-X_2>0$", r"כאשר $X_1$ ו-$X_2$ זוגיים"], 0,
        r"השורשים $-X_1\pm\sqrt{X_1^2-X_2}$ שלמים כאשר השורש הריבועי שלם. המבחין החיובי לבדו אינו מספיק (למשל $X_1=2,X_2=1$ נותן $\sqrt3$), וזוגיות אינה הקריטריון: $(2,2)$ זוגיים אך $4-2=2$ אינו ריבוע, ו-$(1,1)$ אי-זוגיים ובכל זאת השורשים שלמים."),
     NU(r"כמה זוגות $(X_1,X_2)$ נותנים שורשים שלמים?", 4, r"$11,23,24,35$ (ערכי $X_1^2-X_2$: $0,1,0,4$)."),
     NU(r"מהי ההסתברות ששורשי המשוואה שלמים?", Fr(1, 9), r"$\frac4{36}=\frac19$.")])

ADD(2, "ג",
    RB((r"הגדרת הסתברות מותנית $\frac{P(B\cap\bar A)}{P(\bar A)}$", 1), (r"$|\bar A|=29$ ו-$B\subseteq\bar A$ (שורשים שלמים הם ממשיים)", 2), (r"התשובה $\frac4{29}$", 1)),
    [r"לחלק ב-$36$ במקום ב-$29$", r"להניח ש-$B$ ו-$\bar A$ בלתי תלויים"],
    [CH(r"מהי $P(B\cap\bar A)$, כאשר $B$ = ״שורשים שלמים״ ו-$\bar A$ = ״שורשים ממשיים״?",
        [r"$P(B)$, כי כל זוג עם שורשים שלמים הוא גם בעל שורשים ממשיים", r"$0$, כי המאורעות זרים", r"$P(B)\cdot P(\bar A)$, כי המאורעות בלתי תלויים"], 0,
        r"שורשים שלמים הם ממשיים, ולכן $B\subseteq\bar A$ ו-$P(B\cap\bar A)=\frac19$. מכפלה הייתה נותנת $\frac19\cdot\frac{29}{36}\ne\frac19$, ואפס אינו נכון כי $B$ אינו ריק."),
     NU(r"מהי $P(\bar A)$ (שורשים ממשיים)? (המכנה: אירוע התנאי)", Fr(29, 36), r"$1-\frac7{36}=\frac{29}{36}$."),
     NU(r"מהי $P(B\cap\bar A)$? (המונה)", Fr(1, 9), r"$P(B)=\frac4{36}$."),
     NU(r"מהי ההסתברות המותנית $P(B\mid\bar A)$?", Fr(4, 29), r"$\frac{4/36}{29/36}=\frac4{29}$.")])

ADD(2, "ד",
    RB((r"הגדרת הסתברות מותנית: $C=\{31,\dots,36\}$ ו-$B\cap C=\{35\}$", 2), (r"התשובה $\frac16$", 1), (r"השורשים: $y^2+6y+5=0$ ולכן $-1$ ו-$-5$", 2)),
    [r"לחלק ב-$36$ במקום ב-$|C|=6$", r"לשכוח את השורש השני"],
    [CH(r"נתון $X_1=3$. עבור איזה $X_2\in\{1,\dots,6\}$ השורשים שלמים?",
        [r"$X_2=5$ בלבד ($9-5=4$ ריבוע שלם)", r"כל ערך של $X_2$", r"$X_2=9$ (מבחין אפס)"], 0,
        r"דרוש ש-$9-X_2$ יהיה ריבוע שלם אי-שלילי: $9-X_2\in\{8,\dots,3\}$ ורק $4$ הוא ריבוע, כלומר $X_2=5$. $X_2=9$ אינו תוצאה של קובייה."),
     NU(r"מהי $P(C)$ כאשר $C$ = ״התוצאה הראשונה $3$״? (המכנה: אירוע התנאי)", Fr(1, 6), r"$\frac6{36}$."),
     NU(r"מהי $P(B\cap C)$? (המונה)", Fr(1, 36), r"רק הזוג $(3,5)$."),
     NU(r"מהי $P(B\mid C)$?", Fr(1, 6), r"$\frac{1/36}{1/6}=\frac16$."),
     NU(r"מהו השורש הגדול משני השורשים כאשר $X_1=3$, $X_2=5$?", -1, r"$y=-3\pm\sqrt{9-5}$: השורשים $-1$ ו-$-5$.")])

# ---- Q3: Bernoulli matrices; numeric checks at p=0.3
ADD(3, "א",
    RB((r"$D_j=XY$ בעל ערכים $0,1$", 3), (r"$P(D_j=1)=P(X_j=1)P(Y_j=1)=p^2$ (אי-תלות)", 3), (r"$D_1\sim\mathrm{Ber}(p^2)$ ופונקציית ההסתברות", 2)),
    [r"לכתוב $D_1\sim\mathrm{Ber}(p)$ כי $X$ ו-$Y$ ברנולי", r"לחשב את הדטרמיננטה הלא נכון (לא $X+Y$)"],
    [CH(r"$D_1=\det\boldsymbol Q_1=X_1Y_1$ עם $X_1,Y_1\sim\mathrm{Ber}(p)$ בלתי תלויים. איך מפולג $D_1$?",
        [r"$\mathrm{Ber}(p^2)$", r"$\mathrm{Ber}(p)$", r"$\mathrm{Bin}(2,p)$"], 0,
        r"המכפלה היא $1$ רק כששניהם $1$, בהסתברות $p\cdot p=p^2$ (ב-$p=0.3$: $0.09$). $\mathrm{Bin}(2,p)$ היא התפלגות הסכום $T_1$ ומקבלת גם את הערך $2$, ו-$\mathrm{Ber}(p)$ נותן $0.3$."),
     NU(r"מהי $P(D_1=1)$ כאשר $p=0.3$?", Fr(9, 100), r"$p^2=0.09$."),
     NU(r"מהי $P(D_1=0)$ באותו $p$?", Fr(91, 100), r"$1-p^2=0.91$.")])

ADD(3, "ב",
    RB((r"$T_1=X_1+Y_1$ סכום של שני ברנולי בלתי תלויים עם אותו $p$", 3), (r"משפט הפירוק: $T_1\sim\mathrm{Bin}(2,p)$", 3), (r"פונקציית ההסתברות $\binom2tp^t(1-p)^{2-t}$", 2)),
    [r"לכתוב $\mathrm{Ber}(2p)$ (אינו חוקי כש-$p>\frac12$ ואינו מקבל את הערך $2$)", r"לשכוח את המקדם $2$ ב-$P(T_1=1)=2p(1-p)$"],
    [CH(r"$T_1=X_1+Y_1$ עם $X_1,Y_1\sim\mathrm{Ber}(p)$ בלתי תלויים. איך מפולג $T_1$?",
        [r"$\mathrm{Bin}(2,p)$: סכום של שני ברנולי בלתי תלויים", r"$\mathrm{Ber}(2p)$", r"$\mathrm{Ber}(p^2)$"], 0,
        r"סכום של $2$ ברנולי בלתי תלויים הוא בינומי. $T_1$ מקבל גם את הערך $2$, ולכן אינו ברנולי; ו-$\mathrm{Ber}(2p)$ אינו חוקי עבור $p>\frac12$."),
     NU(r"מהי $P(T_1=1)$ כאשר $p=0.3$?", Fr(42, 100), r"$2p(1-p)=2\cdot0.3\cdot0.7=0.42$."),
     NU(r"מהי $P(T_1=2)$ באותו $p$?", Fr(9, 100), r"$p^2=0.09$.")])

ADD(3, "ג",
    RB((r"$D=\sum D_j$ עם $D_j\sim\mathrm{Ber}(p^2)$", 1), (r"אי-תלות של ה-$D_j$ (כל אחד תלוי בזוג נפרד)", 2), (r"משפט הפירוק: $D\sim\mathrm{Bin}(n,p^2)$", 1)),
    [r"לכתוב $\mathrm{Bin}(n,p)$ או $\mathrm{Bin}(2n,p^2)$", r"לא לנמק את אי-התלות"],
    [CH(r"$D=\sum_{j=1}^nD_j$ עם $D_j\sim\mathrm{Ber}(p^2)$, ה-$D_j$ בלתי תלויים (כל אחד מהם נקבע מזוג $(X_j,Y_j)$ נפרד). איך מפולג $D$?",
        [r"$\mathrm{Bin}(n,p^2)$", r"$\mathrm{Bin}(n,p)$", r"$\mathrm{Bin}(2n,p^2)$"], 0,
        r"$n$ ניסויי ברנולי בלתי תלויים בהסתברות $p^2$. הפרמטר $p$ הוא של $X_j,Y_j$, ו-$2n$ ניסויים הם של $T$ (שני לכל מטריצה)."),
     NU(r"מהי $P(D=1)$ כאשר $n=3$ ו-$p=0.3$?", 3 * 0.09 * 0.91 ** 2, r"$\binom31(0.09)(0.91)^2\approx0.22359$.")])

ADD(3, "ד",
    RB((r"$T=\sum T_j$ עם $T_j\sim\mathrm{Bin}(2,p)$ בלתי תלויים", 2), (r"כל $T_j$ הוא סכום של $2$ ברנולי, ולכן $T$ סכום של $2n$ ברנולי בלתי תלויים", 2), (r"$T\sim\mathrm{Bin}(2n,p)$", 1)),
    [r"לכתוב $\mathrm{Bin}(n,p)$ ולשכוח שבכל מטריצה שני ברנולי", r"לכתוב $\mathrm{Bin}(n,2p)$"],
    [CH(r"$T=\sum_{j=1}^nT_j$ עם $T_j\sim\mathrm{Bin}(2,p)$ בלתי תלויים. איך מפולג $T$?",
        [r"$\mathrm{Bin}(2n,p)$", r"$\mathrm{Bin}(n,2p)$", r"$\mathrm{Bin}(n,p)$"], 0,
        r"כל $T_j=X_j+Y_j$ הוא סכום של $2$ ברנולי, ולכן $T$ הוא סכום של $2n$ ברנולי בלתי תלויים עם אותו $p$. $\mathrm{Bin}(n,2p)$ אינו חוקי כש-$p>\frac12$, ו-$\mathrm{Bin}(n,p)$ נותן תוחלת $np$ במקום $2np$."),
     NU(r"כמה ניסויי ברנולי בלתי תלויים מרכיבים את $T$ כאשר $n=3$?", 6, r"$2n=6$."),
     NU(r"מהי $P(T=2)$ כאשר $n=3$ ו-$p=0.3$?", 15 * 0.09 * 0.7 ** 4, r"$\binom62(0.3)^2(0.7)^4=15\cdot0.09\cdot0.2401\approx0.32414$.")])

ADD(3, "ה",
    RB((r"בילינאריות השונות המשותפת", 1), (r"אי-תלות בין זוגות שונים: $\operatorname{cov}[D_j,T_k]=0$ עבור $j\ne k$", 2), (r"חישוב $\operatorname{cov}[D_1,T_1]=2p^2(1-p)$", 1), (r"התשובה $2np^2(1-p)$", 1)),
    [r"להשאיר את האיברים $j\ne k$ ולקבל $n^2$", r"לשכוח ש-$X_1^2=X_1$ בברנולי"],
    [CH(r"בחישוב $\operatorname{cov}[D,T]=\sum_{j,k}\operatorname{cov}[D_j,T_k]$, מה קורה לאיברים עם $j\ne k$?",
        [r"הם מתאפסים, כי $D_j$ ו-$T_k$ תלויים בזוגות שונים ובלתי תלויים", r"הם חיוביים כי שניהם תלויים ב-$p$", r"הם שווים לאיברי האלכסון"], 0,
        r"שונות משותפת של משתנים בלתי תלויים היא $0$. לכן נשארים רק $n$ האיברים עם $j=k$ (ולא $n^2$)."),
     NU(r"מהי $\operatorname{cov}[D_1,T_1]$ כאשר $p=0.3$?", 2 * 0.09 * 0.7, r"$2p^2(1-p)=2\cdot0.09\cdot0.7=0.126$."),
     NU(r"מהי $\operatorname{cov}[D,T]$ כאשר $n=3$ ו-$p=0.3$?", 2 * 3 * 0.09 * 0.7, r"$n\cdot0.126=0.378$.")])

# ---- Q4: f(x) = a(b^2 - x^2) on [-b, b]; a = 3/4, b = 1
ADD(4, "א",
    RB((r"הצפיפות $f(x)$ זוגית, ולכן $xf(x)$ אי-זוגית", 3), (r"אינטגרל של פונקציה אי-זוגית על קטע סימטרי $(-b,b)$ מתאפס", 2), (r"התשובה $\mathbb E[X]=0$ (לכל $a,b$)", 1)),
    [r"לחשב $\mathbb E[X]=\frac b2$ מהחצי החיובי בלבד", r"לחשוב שהתוחלת תלויה ב-$a$ וב-$b$"],
    [CH(r"מה ערך האינטגרל $\int_{-b}^{b}x\,a(b^2-x^2)\,dx$?",
        [r"$0$: האינטגרנד אי-זוגי והקטע סימטרי", r"חיובי, כי $f(x)>0$", r"$ab^4/4$, האינטגרל על $(0,b)$"], 0,
        r"החצי השלילי מבטל את החיובי. האינטגרל על החצי החיובי לבדו הוא $\frac{ab^4}4$, אך התוחלת דורשת את שני החצאים."),
     NU(r"עבור $a=\frac34$, $b=1$: מהו $\int_0^1x\,f(x)\,dx$ (החצי החיובי)?", Fr(3, 16), r"$\frac34\left(\frac12-\frac14\right)=\frac3{16}$."),
     NU(r"מהי $\mathbb E[X]$ באותם ערכים?", 0, r"$\frac3{16}-\frac3{16}=0$.")])

ADD(4, "ב",
    RB((r"נרמול: $\frac{4ab^3}3=1$", 2), (r"שונות (כי $\mathbb E[X]=0$): $\frac{4ab^5}{15}=\frac3{15}$", 2), (r"חילוק המשוואות: $b^2=1$", 1), (r"$a=\frac34$, $b=1$", 1)),
    [r"להציב $\operatorname{Var}=\mathbb E[X^2]-\mathbb E[X]^2$ ולהתעלם מכך ש-$\mathbb E[X]=0$", r"לטעות באינטגרל $\int_0^bx^2(b^2-x^2)dx$"],
    [CH(r"יש שני נעלמים $a,b$. איך מתקבלות שתי משוואות מהנתונים?",
        [r"נרמול ושונות: חילוק שתי המשוואות מבטל את $a$ ונותן $b^2$", r"נרמול בלבד, כי הצפיפות קובעת את שני הפרמטרים", r"תוחלת ושונות, כי שתיהן תלויות ב-$a$"], 0,
        r"הנרמול נותן משוואה אחת בשני נעלמים. התוחלת $0$ לכל $a,b$ ולכן אינה נותנת משוואה."),
     NU(r"מה $b$ שמתקבל מחילוק $\frac{4ab^5}{4ab^3}=\frac{3}{3}$?", 1, r"$b^2=1$ ומכיוון ש-$b>0$, $b=1$."),
     NU(r"מהו $a$ מתוך הנרמול $4ab^3=3$ עבור $b=1$?", Fr(3, 4), r"$a=\frac34$.")])

ADD(4, "ג",
    RB((r"הצבת $a=\frac34$, $b=1$: $f(x)=\frac34(1-x^2)$", 1), (r"אינטגרציה: $\frac34\left(\frac23+t-\frac{t^3}{3}\right)=\frac14(2+3t-t^3)$", 3), (r"ערכי הקצה $0$ ו-$1$ ורציפות", 2), (r"שרטוט הגרף", 1)),
    [r"לשכוח את הקבוע $\frac23$ (גבול תחתון $-1$)", r"לא לציין $F=0$ ו-$F=1$ מחוץ ל-$(-1,1)$"],
    [NU(r"מהו $F_X(0)=P(X\le0)$?", Fr(1, 2), r"הצפיפות זוגית: חצי מהשטח משמאל ל-$0$."),
     NU(r"מהו $F_X(\frac12)=\frac14\left(2+3t-t^3\right)$ ב-$t=\frac12$?", Fr(27, 32), r"$\frac14\left(2+\frac32-\frac18\right)=\frac14\cdot\frac{27}8=\frac{27}{32}$."),
     NU(r"מהו $F_X(-\frac12)$?", Fr(5, 32), r"$\frac14\left(2-\frac32+\frac18\right)=\frac5{32}$ (וגם $1-\frac{27}{32}$ בסימטריה).")])

ADD(4, "ד",
    RB((r"הצבת $a=\frac34$, $b=1$ והגדרת הסתברות מותנית", 1), (r"מכנה $P(|X|<1)=1$", 1), (r"מונה $1-F_X(\frac34)=\frac{11}{256}$", 3), (r"התשובה $\frac{11}{256}$", 1)),
    [r"להשתמש ב-$F_X(\frac34)$ במקום המשלים", r"לטעות בחישוב $\frac34^3$ ב-$F_X(\frac34)$"],
    [NU(r"מהי $P(|X|<b)=P(|X|<1)$? (המכנה: אירוע התנאי)", 1, r"כל הצפיפות על $(-1,1)$."),
     NU(r"מהו $F_X(\frac34)$?", Fr(245, 256), r"$\frac14\left(2+\frac94-\frac{27}{64}\right)=\frac14\cdot\frac{245}{64}=\frac{245}{256}$."),
     NU(r"מהי $P(X>\frac34\mid|X|<1)$?", Fr(11, 256), r"$\frac{1-245/256}{1}=\frac{11}{256}$.")])

# ---- Q5: Poisson thinning; numeric checks at lambda = 3, p = 0.4 (no sim: a Poisson count has no finite sim kind)
ADD(5, "א",
    RB((r"הגדרת $Y\sim\mathrm{Poisson}(\lambda)$ ו-$X\mid Y=j\sim\mathrm{Bin}(j,p)$", 2), (r"הסתברות שלמה: סכום על $j\ge k$", 2), (r"שימוש בנוסחה ברמז ופישוט ל-$X\sim\mathrm{Poisson}(p\lambda)$", 4)),
    [r"להניח ש-$X\sim\mathrm{Poisson}(\lambda)$ בלי להתחשב בהטלת המטבע", r"לשכוח את הגבול התחתון $j\ge k$ של הסכום"],
    [CH(r"בהינתן שהגיעו $j$ פניות, כל אחת מניבה פרס בהסתברות $p$ ללא תלות באחרות. מה ההתפלגות של $X$ בהינתן $Y=j$?",
        [r"$\mathrm{Bin}(j,p)$", r"$\mathrm{Poisson}(\lambda p)$", r"גאומטרית עם פרמטר $p$"], 0,
        r"מספר קבוע $j$ של ניסויים בלתי תלויים נותן בינומית; ההתפלגות הפואסונית היא התוצאה הסופית (אחרי סכימה על $Y$), לא ההתפלגות בהינתן $Y$. גאומטרית סופרת ניסויים עד הצלחה."),
     NU(r"בהינתן $Y=3$ ו-$p=0.4$, מהי $P(X=0\mid Y=3)$?", Fr(216, 1000), r"$(1-p)^3=0.6^3=0.216$."),
     NU(r"מהי $P(X=0)$ כאשר $\lambda=3$ ו-$p=0.4$ (ידוע ש-$X\sim\mathrm{Poisson}(p\lambda)$)?", math.exp(-1.2), r"$e^{-p\lambda}=e^{-1.2}\approx0.30119$.")])

ADD(5, "ב",
    RB((r"סכום ההסתברויות של פואסון: $e^{-\lambda p}\sum_{k}\frac{(\lambda p)^k}{k!}$", 3), (r"טור טיילור של $e^{x}$", 2), (r"$e^{-\lambda p}e^{\lambda p}=1$", 1)),
    [r"להשתמש בטור גאומטרי במקום בטור של האקספוננט"],
    [CH(r"איזה טור מזהים ב-$\sum_{k=0}^\infty\frac{(\lambda p)^k}{k!}$?",
        [r"טור טיילור של $e^{x}$ ב-$x=\lambda p$", r"טור גאומטרי $\sum x^k$", r"משפט הבינום $(1+x)^n$"], 0,
        r"הגורם $\frac1{k!}$ מאפיין את טור האקספוננט. טור גאומטרי אין בו עצרת, ובינום הוא סכום סופי."),
     NU(r"מה ערך הטור $\sum_{k=0}^\infty\frac{x^k}{k!}$ ב-$x=\lambda p=1.2$?", math.exp(1.2), r"$e^{1.2}\approx3.3201$."),
     NU(r"מהו הסכום הכולל $e^{-1.2}\cdot e^{1.2}$?", 1, r"$1$, כנדרש.")])

ADD(5, "ג",
    RB((r"זיהוי $X\sim\mathrm{Poisson}(p\lambda)$ מסעיף א", 2), (r"תוחלת ושונות של פואסון שוות לפרמטר", 3), (r"$\mathbb E[X]=\operatorname{Var}[X]=p\lambda$", 1)),
    [r"לכתוב $\operatorname{Var}=\lambda p(1-p)$ (נוסחת הבינומית)", r"להשתמש ב-$\lambda$ במקום ב-$p\lambda$"],
    [CH(r"$X\sim\mathrm{Poisson}(p\lambda)$. מה התוחלת והשונות?",
        [r"שתיהן שוות ל-$p\lambda$", r"תוחלת $p\lambda$ ושונות $p\lambda(1-p)$", r"תוחלת $p\lambda$ ושונות $p^2\lambda$"], 0,
        r"בפואסון התוחלת והשונות שוות לפרמטר. $p\lambda(1-p)$ הוא נוסחת הבינומית, ו-$p^2\lambda$ חסר מקור."),
     NU(r"מהי $\mathbb E[X]$ כאשר $\lambda=3$ ו-$p=0.4$?", Fr(6, 5), r"$p\lambda=1.2$."),
     NU(r"מהי $\operatorname{Var}[X]$ באותם ערכים?", Fr(6, 5), r"$p\lambda=1.2$.")])

ADD(5, "ד",
    RB((r"נוסחת בייס $\frac{P(X=n\mid Y=N)P(Y=N)}{P(X=n)}$", 2), (r"הצבת הבינומית והפואסונית וצמצום", 2), (r"התשובה $\frac{[\lambda(1-p)]^{N-n}}{(N-n)!}e^{-\lambda(1-p)}$", 1)),
    [r"לחלק ב-$P(Y=N)$ במקום ב-$P(X=n)$", r"לשכוח שהתוצאה מוסטת: $N\ge n$"],
    [CH(r"נתון שזכו $n$ פונים ומחפשים את התפלגות מספר הפניות $Y$. איזו נוסחה נכונה?",
        [r"בייס: $P(Y=N\mid X=n)=\frac{P(X=n\mid Y=N)\,P(Y=N)}{P(X=n)}$", r"$P(Y=N\mid X=n)=P(X=n\mid Y=N)$", r"$P(Y=N\mid X=n)=P(Y=N)$, כי $Y$ קובע מראש את מספר הפניות"], 0,
        r"מספר הפניות והזוכים תלויים. ב-$\lambda=3$, $p=0.4$, $n=2$, $N=4$ האפשרות השנייה נותנת $0.3456$, השלישית $0.168$, והנכון $0.2678$."),
     NU(r"מהי $P(X=2)$ כאשר $\lambda=3$ ו-$p=0.4$? (המכנה: אירוע התנאי)", math.exp(-1.2) * 1.2 ** 2 / 2, r"$X\sim\mathrm{Poisson}(1.2)$: $e^{-1.2}\cdot\frac{1.44}{2}\approx0.21686$."),
     NU(r"מהי $P(X=2\cap Y=4)=P(X=2\mid Y=4)P(Y=4)$ באותם ערכים? (המונה)", 0.3456 * math.exp(-3) * 81 / 24, r"$\binom42(0.4)^2(0.6)^2\cdot\frac{3^4}{4!}e^{-3}=0.3456\cdot0.16803\approx0.058069$."),
     NU(r"מהי $P(Y=4\mid X=2)$?", math.exp(-1.8) * 1.8 ** 2 / 2, r"$\frac{0.058069}{0.21686}\approx0.26778=\frac{1.8^2}{2!}e^{-1.8}$.")])

# ---- Q6: circuits Q1 = D (AB u C), Q2 = D (CB u A); numeric checks at p = 0.6
ADD(6, "א",
    RB((r"קריאת המעגל: $Q_1=D\cap\bigl((A\cap B)\cup C\bigr)$", 2), (r"$P\bigl((A\cap B)\cup C\bigr)=p^2+p-p^3$", 3), (r"הכפלה ב-$P(D)$: $p^2(1+p-p^2)$", 2)),
    [r"לשכוח להחסיר את החיתוך ולכתוב $p^2+p$", r"להחליף בין טור למקביל"],
    [CH(r"איזה ביטוי מתאר את $Q_1$ לפי האיור ($D$ בטור עם מקבץ של ענף $A\!-\!B$ בטור ו-$C$)?",
        [r"$D\cap\bigl((A\cap B)\cup C\bigr)$", r"$D\cap(A\cup B\cup C)$", r"$A\cap B\cap C\cap D$"], 0,
        r"ב-$p=0.6$ האפשרות השנייה נותנת $0.6\cdot0.936=0.5616$ והשלישית $0.1296$, בעוד $Q_1$ נותן $0.4464$."),
     NU(r"מהי ההסתברות שהמקבץ $(A\cap B)\cup C$ פועל כאשר $p=0.6$?", Fr(93, 125), r"$p^2+p-p^3=0.36+0.6-0.216=0.744$."),
     NU(r"מהי $P(Q_1)$ באותו $p$?", _PQ1, r"$0.6\cdot0.744=0.4464$.")])

ADD(6, "ב",
    RB((r"התניה על $B$: בשני המקרים $Q_1\cup Q_2=D\cap(A\cup C)$", 3), (r"$P(A\cup C)=2p-p^2$ ובלתי תלוי ב-$D$", 2), (r"התשובה $p^2(2-p)$", 2)),
    [r"לחבר $P(Q_1)+P(Q_2)$ בלי להחסיר את החיתוך", r"להניח ש-$Q_1,Q_2$ זרים"],
    [CH(r"מהו האיחוד $Q_1\cup Q_2$ (עם $Q_1=D(AB\cup C)$ ו-$Q_2=D(CB\cup A)$)?",
        [r"$D\cap(A\cup C)$, ללא תלות ב-$B$", r"$D\cap(A\cup B\cup C)$", r"$D\cap A\cap C$"], 0,
        r"אם $B$ פועל: שני המעגלים שווים ל-$D(A\cup C)$. אם $B$ אינו פועל: $DC\cup DA=D(A\cup C)$. ב-$p=0.6$ האפשרות השנייה נותנת $0.5616$ והשלישית $0.216$, לעומת $0.504$."),
     NU(r"מהי $P(A\cup C)$ כאשר $p=0.6$?", 2 * _p6 - _p6 ** 2, r"$1-0.4^2=0.84$."),
     NU(r"מהי $P(Q_1\cup Q_2)$ באותו $p$?", _PU, r"$0.6\cdot0.84=0.504=p^2(2-p)$.")])

ADD(6, "ג",
    RB((r"הגדרת הסתברות מותנית $\frac{P(Q_1\cap Q_2)}{P(Q_1)}$", 2), (r"$P(Q_1\cap Q_2)=2P(Q_1)-P(Q_1\cup Q_2)=p^3(3-2p)$ (הכלה והפרדה וסימטריה)", 3), (r"התשובה $\frac{p(3-2p)}{1+p-p^2}$", 2)),
    [r"להכפיל $P(Q_1)P(Q_2)$ (המעגלים תלויים)", r"לשכוח ש-$P(Q_1)=P(Q_2)$ בסימטריה"],
    [CH(r"איך מחשבים את $P(Q_1\cap Q_2)$?",
        [r"$P(Q_1)+P(Q_2)-P(Q_1\cup Q_2)$", r"$P(Q_1)\cdot P(Q_2)$, כי הם בלתי תלויים", r"$P(Q_1\cup Q_2)-P(Q_1)$"], 0,
        r"המעגלים חולקים רכיבים ולכן תלויים: ב-$p=0.6$ המכפלה נותנת $0.1993$ והנכון $0.3888$. האפשרות השלישית נותנת $0.0576$."),
     NU(r"מהי $P(Q_1)$ כאשר $p=0.6$? (המכנה: אירוע התנאי)", _PQ1, r"$0.4464$ מסעיף א."),
     NU(r"מהי $P(Q_1\cap Q_2)=2P(Q_1)-P(Q_1\cup Q_2)$ באותו $p$? (המונה)", _PI, r"$2\cdot0.4464-0.504=0.3888=p^3(3-2p)$."),
     NU(r"מהי $P(Q_2\mid Q_1)$?", _PI / _PQ1, r"$\frac{0.3888}{0.4464}\approx0.87097$.")])

ADD(6, "ד",
    RB((r"נוסחת בייס: $\frac{P(Q_1\cap Q_2\mid ABCD)\,P(ABCD)}{P(Q_1\cap Q_2)}$", 2), (r"$P(Q_1\cap Q_2\mid ABCD)=1$ ו-$P(ABCD)=p^4$", 1), (r"התשובה $\frac{p}{3-2p}$", 1)),
    [r"לחלק ב-$P(Q_1)$ במקום ב-$P(Q_1\cap Q_2)$", r"לשכוח שאם כל הרכיבים פועלים שני המעגלים פועלים"],
    [CH(r"מהי $P(Q_1\cap Q_2\mid A\cap B\cap C\cap D)$?",
        [r"$1$: כשכל הרכיבים פועלים שני המעגלים פועלים", r"$p^4$", r"$P(Q_1\cap Q_2)$"], 0,
        r"אם כל הרכיבים פועלים, ל-$Q_1$ ול-$Q_2$ יש מסלול פעיל, ולכן ההסתברות $1$. שתי האפשרויות האחרות הן הסתברויות בלתי מותנות ($0.1296$ ו-$0.3888$)."),
     NU(r"מהי $P(A\cap B\cap C\cap D)$ כאשר $p=0.6$?", _p6 ** 4, r"$0.6^4=0.1296$."),
     NU(r"מהי $P(Q_1\cap Q_2)$ באותו $p$? (המכנה: אירוע התנאי)", _PI, r"$0.3888$ מסעיף ג."),
     NU(r"מהי ההסתברות שכל הרכיבים פועלים, בהינתן ששני המעגלים פועלים?", Fr(1, 3), r"$\frac{0.1296}{0.3888}=\frac13=\frac{p}{3-2p}$.")])

APPLY(questions)


exam = {
    "examCode": CODE,
    "examLabel": "הסתברות (20021-80), סמסטר א׳ תשפ״ד, מועד ב׳ – מילואים (09.05.2024)",
    "year": 2024,
    "examDate": "09.05.2024",
    "sourceFile": "24A-E exam pp.1-3",
    "solutionFile": "24A-E official handwritten solutions pp.4-15",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: החגב", "image": IMG + "Q1-grasshopper.png", "caption": Q1_TXT},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_TXT},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_TXT},
        "c6": {"kind": "image", "title": "שאלה 6: מעגלים", "image": IMG + "Q6-circuits.png", "caption": Q6_TXT},
    },
    "questions": questions,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
