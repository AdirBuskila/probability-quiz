# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-E.json -- probability (course 20021-80), semester A 2024, moed B (reserve-duty
moed, 09.05.2024). Code 24A-E is fixed by GATE1. 6 questions, 25 items (Q1 4, Q2 4, Q3 5, Q4 4, Q5 4, Q6 4).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-E.py

Source: exam pp.1-3, official handwritten solutions pp.4-15.
Transcription notes
- Part keys are single letters (printed label is the bold token at the start of the question text).
  Q4 prints ג-1, ג-2 -> keys ג ד. Q5 prints א-1, א-2, א-3, ב -> keys א ב ג ד.
- Q3 bonus (key ה, printed "סעיף בונוס", cov[D,T]) has NO official solution in the source -> hold "no-key".
- Q2(ד) asks to find the roots; the official solution only gives the probability (1/6). The roots (-1 and -5) are
  added as a one-line completion computed from the official event B∩C={35}, and marked as such.
- The portrait and money-bag pictures in the Q5 header are decoration and are not shipped.
- Q1 region data is in tools/verify/24A-E/regions.json (RAW_SCHEMA has no `region` field).
"""
import json, pathlib

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

questions.append({
    "num": 3, "part": "ה", "kind": "computation", "topic": "joint_discrete", "points": 5,
    "question": r"**סעיף בונוס** (אין חובה לפתור!): חשבו את השונות המשותפת $\operatorname{cov}[D,T]$ של משתנים חדשים $D$ ו-$T$.",
    "contextId": "c3",
    "hold": "no-key",
})

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
