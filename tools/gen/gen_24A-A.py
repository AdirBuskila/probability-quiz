# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-A.json -- probability (course 20021), semester A 2024, moed A (25.03.2024).
This is the 20021 group; the 20021-80 group of 3.4.2024 is 24A-D. 6 questions, 22 items
(Q1 5, Q2 4, Q3 4, Q4 3, Q5 3, Q6 3), 25 points each. The two bonus parts (Q2 ד, Q3 ד) are held (no-key).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-A.py

Source: exam pp.1-3, official handwritten solutions pp.4-19.
Transcription notes
- Part keys are single letters. Q1 prints א-1, א-2, א-3, ב, ג -> keys א ב ג ד ה (a=א-1, b=א-2, c=א-3, d=ב, e=ג).
  The printed label is the bold token at the start of each question text.
- Q2 asks for the probability that the running sum of a fair N-sided die ever equals N ("שאי פעם נגיע לסכום").
- Q2(ד) and Q3(ד) are bonus parts ("אין חובה לפתור"); the official solution has no answer for either -> hold no-key.
  (Q2 gives the pattern P_N = p(1+p)^(N-1) only through P_3, P_4, P_5.)
- Q5(ב) has the main solution and the official short alternative (sum of Bernoulli).
- Q6(ב): the official solution has two methods (conditioning on A,E and on A alone); both are given.
- The thumbnail of the exam cover in Q5 is decoration and is not shipped.
- Q1 region data is in tools/verify/24A-A/regions.json (RAW_SCHEMA has no `region` field).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-A.json"
CODE = "24A-A"
IMG = "images/exams/24A-A-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"נתבונן במלבן בעל צלעות שאורכם מהווים משתנים מקריים בלתי תלויים $X\sim U_c(0,1)$ ו-$Y\sim U_c(0,2)$. "
          r"יהי $S$ שטח המלבן ו-$L$ היקף המלבן.")
Q1_SOL = r"שטח המלבן $S=X\cdot Y$, היקף המלבן $L=2(X+Y)$. מרחב המדגם: המלבן $\Omega=(0,1)\times(0,2)$, $|\Omega|=2$." "\n"

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א-1:** חשבו את ההסתברות $P(S<1)$.",
    Q1_SOL + r"""$$P(S<1)=P(XY<1)=P\left(Y<\tfrac1X\right).$$
אחדות של משתנים מקריים $X$ ו-$Y$ מאפשרת שימוש בגישה הקלאסית להסתברות:
$$P(S<1)=\frac{|\{y<\frac1x\}|}{|\Omega|},\qquad |\Omega|=2.$$
$$\left|\left\{y<\tfrac1x\right\}\right|=2\cdot\frac12+\int_{1/2}^{1}\frac{dx}{x}=1+\ln x\Big|_{1/2}^{1}=1+\ln 2.$$
לכן
$$P(S<1)=\frac12\,(1+\ln 2)\approx 0.847.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**א-2:** חשבו את ההסתברות $P(L<2)$.",
    Q1_SOL + r"""$$P(L<2)=P(X+Y<1)=\frac{|\{y<1-x\}|}{|\Omega|}=\frac{1/2}{2}=\frac14.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**א-3:** חשבו את ההסתברות המותנית $P(S<1\,/\,L>2)$.",
    Q1_SOL + r"""$$P(S<1/L>2)=\frac{P(S<1\cap L>2)}{P(L>2)},\qquad P(L>2)=1-\frac14=\frac34.$$
$$P(S<1\cap L>2)=P\left(Y<\tfrac1X\cap Y>1-X\right)=\frac{\left|\{y<\frac1x\cap y>1-x\}\right|}{|\Omega|}.$$
$$\left|\left\{y<\tfrac1x\cap y>1-x\right\}\right|=1+\ln 2-\frac12=\frac12+\ln 2,\qquad P(S<1\cap L>2)=\frac14+\frac12\ln 2.$$
לכן
$$P(S<1/L>2)=\frac13+\frac23\ln 2\approx 0.795.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ד", "continuous_rv",
    r"**ב.** חשבו תוחלת $\mathbb E[S]$ ושונות $\operatorname{var}[S]$ של שטח המלבן.",
    r"""$X,Y$ בלתי תלויים, ולכן
$$\mathbb E[S]=\mathbb E[XY]=\mathbb E[X]\,\mathbb E[Y]=\frac12\cdot 1=\frac12.$$
$\operatorname{Var}[S]=\mathbb E[S^2]-(\mathbb E[S])^2$, כאשר
$$\mathbb E[S^2]=\mathbb E[X^2Y^2]=\mathbb E[X^2]\,\mathbb E[Y^2]=\frac13\cdot\frac43=\frac49,$$
($\int_0^1x^2dx=\frac13$, $\ \int_0^2y^2\cdot\frac12\,dy=\frac43$). לכן
$$\operatorname{Var}[S]=\frac49-\frac14=\frac7{36}.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ה", "continuous_rv",
    r"**ג.** חשבו תוחלת $\mathbb E[L]$ ושונות $\operatorname{var}[L]$ של היקף המלבן.",
    r"""$$\mathbb E[L]=\mathbb E[2(X+Y)]=2\bigl(\mathbb E[X]+\mathbb E[Y]\bigr)=2\left(\frac12+1\right)=3.$$
$$\operatorname{Var}[L]=\operatorname{Var}[2(X+Y)]=4\bigl(\operatorname{Var}[X]+\operatorname{Var}[Y]\bigr)=4\left(\frac1{12}+\frac4{12}\right)=\frac53.$$""",
    5, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_COMMON = r"מטילים קובייה **מאוזנת** בעלת %s פאות ומסכמים את התוצאות."

questions.append(Q(
    2, "א", "special_discrete",
    Q2_COMMON % "3" + "\n" + r"**א.** מהי ההסתברות $P_3$ שאי פעם נגיע לסכום התוצאות השווה לשלוש?",
    r"""ההסתברות לקבל תוצאה ספציפית בהטלה היא $p=\dfrac13$.
ניתן להגיע לסכום השווה ל-3:
- בהטלה אחת: $\{3\}$: הסתברות $p$;
- בשתי הטלות: $\{2,1\}$ ו-$\{1,2\}$: הסתברות $2p^2$;
- בשלוש הטלות: $\{1,1,1\}$: הסתברות $p^3$.

$$P_3=p+2p^2+p^3=p(1+p)^2=\frac13\left(\frac43\right)^2.$$""",
    7))

questions.append(Q(
    2, "ב", "special_discrete",
    Q2_COMMON % "4" + "\n" + r"**ב.** מהי ההסתברות $P_4$ שאי פעם נגיע לסכום התוצאות השווה לארבע?",
    r"""ההסתברות לקבל תוצאה ספציפית בהטלה היא $p=\dfrac14$.
ניתן להגיע לסכום השווה ל-4:
- בהטלה אחת: $\{4\}$: הסתברות $p$;
- בשתי הטלות: $\{2,2\},\{3,1\},\{1,3\}$: הסתברות $3p^2$;
- בשלוש הטלות: $\{1,1,2\},\{1,2,1\},\{2,1,1\}$: הסתברות $3p^3$;
- בארבע הטלות: $\{1,1,1,1\}$: הסתברות $p^4$.

$$P_4=p+3p^2+3p^3+p^4=p(1+p)^3=\frac14\left(\frac54\right)^3.$$""",
    8))

questions.append(Q(
    2, "ג", "special_discrete",
    Q2_COMMON % "5" + "\n" + r"**ג.** מהי ההסתברות $P_5$ שאי פעם נגיע לסכום התוצאות השווה לחמש?",
    r"""ההסתברות לקבל תוצאה ספציפית בהטלה היא $p=\dfrac15$.
ניתן להגיע לסכום השווה ל-5:
- בהטלה אחת: $\{5\}$: הסתברות $p$;
- בשתי הטלות: $\{3,2\},\{2,3\},\{4,1\},\{1,4\}$: הסתברות $4p^2$;
- בשלוש הטלות: $\{1,1,3\},\{1,3,1\},\{3,1,1\},\{2,2,1\},\{2,1,2\},\{1,2,2\}$: הסתברות $6p^3$;
- בארבע הטלות: $\{1,2,1,1\},\{1,1,2,1\},\{1,1,1,2\},\{2,1,1,1\}$: הסתברות $4p^4$;
- בחמש הטלות: $\{1,1,1,1,1\}$: הסתברות $p^5$.

$$P_5=p\left(1+4p+6p^2+4p^3+p^4\right)=p(1+p)^4=\frac15\left(\frac65\right)^4.$$""",
    10))

questions.append({
    "num": 2, "part": "ד", "kind": "computation", "topic": "special_discrete", "points": 3,
    "question": r"**סעיף בונוס** – אין חובה לפתור: מטילים קובייה מאוזנת בעלת $N$ פאות ומסכמים את התוצאות. מהי ההסתברות $P_N$ שאי פעם נגיע לסכום התוצאות השווה ל-$N$? **אליך לתת חישוב מפורט.**",
    "hold": "no-key",
})

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"מחשב מייצר שתי סדרות אקראיות מאותיות $A$ ו-$B$. בסדרה הראשונה $N_1$ אותיות ובסדרה השנייה $N_2$ אותיות. "
          r"יהיו $X_1$ ו-$X_2$ משתנים מקריים המתארים את מספר האותיות $A$ בסדרה הראשונה והשנייה בהתאמה. "
          r"בהנחה ששכיחות האות $A$ בכל אחת מהסדרות היא $p$, ענו על השאלות הבאות:")

questions.append(Q(
    3, "א", "special_discrete",
    r"**א.** איך משתנים $X_1$ ו-$X_2$ מפולגים? **עליך לתת הסבר מפורט.**",
    r"""$$P(X_1=k)=\binom{N_1}{k}p^k(1-p)^{N_1-k},\qquad X_1\sim\mathrm{Bin}(N_1,p),$$
$$P(X_2=\ell)=\binom{N_2}{\ell}p^\ell(1-p)^{N_2-\ell},\qquad X_2\sim\mathrm{Bin}(N_2,p),$$
$k=0,1,\dots,N_1$ ; $\ell=0,1,\dots,N_2$.""",
    9, contextId="c3"))

questions.append(Q(
    3, "ב", "special_discrete",
    r"**ב.** נגדיר משתנה מקרי $X=X_1+X_2$ המתאר את מספר האותיות $A$ בשתי הסדרות ביחד. איך משתנה $X$ מפולג? **עליך להוכיח את טענתך.**",
    r"""לפי משפט הפירוק ניתן לייצג את $X_1$ כסכום של $N_1$ משתני ברנולי בלתי תלויים בעלי פרמטר $p$, ואת $X_2$ כסכום של $N_2$ משתני ברנולי כאלה:
$$X_1=\sum_{j=1}^{N_1}Z_j,\quad Z_j\sim\mathrm{Ber}(p),\qquad X_2=\sum_{k=1}^{N_2}W_k,\quad W_k\sim\mathrm{Ber}(p).$$
לכן $X=X_1+X_2$ מהווה סכום של $(N_1+N_2)$ משתני ברנולי בלתי תלויים בעלי פרמטר $p$. לפי משפט הפירוק
$$X\sim\mathrm{Bin}(N_1+N_2,p),$$
כלומר
$$P(X=j)=\binom{N_1+N_2}{j}p^j(1-p)^{N_1+N_2-j},\qquad j=0,1,\dots,N_1+N_2.$$""",
    9, contextId="c3"))

questions.append(Q(
    3, "ג", "conditional_bayes",
    r"**ג.** **אם ידוע** כי בשתי הסדרות ביחד האות $A$ מופיעה $n$ פעמים, מהי ההסתברות שבסדרה הראשונה האות $A$ מופיעה בדיוק $k$ פעמים?",
    r"""צריך למצוא את ההסתברות המותנית:
$$P(X_1=k/X=n)=\frac{P(X_1=k\cap X_1+X_2=n)}{P(X=n)}=\frac{P(X_1=k\cap X_2=n-k)}{P(X=n)}=\frac{P(X_1=k)\,P(X_2=n-k)}{P(X=n)}.$$
$$=\frac{\binom{N_1}{k}p^k(1-p)^{N_1-k}\cdot\binom{N_2}{n-k}p^{n-k}(1-p)^{N_2-n+k}}{\binom{N_1+N_2}{n}p^n(1-p)^{N_1+N_2-n}}$$
ולאחר צמצום:
$$P(X_1=k/X=n)=\frac{\binom{N_1}{k}\binom{N_2}{n-k}}{\binom{N_1+N_2}{n}}.$$""",
    7, contextId="c3"))

questions.append({
    "num": 3, "part": "ד", "kind": "computation", "topic": "special_discrete", "points": 3,
    "question": r"**סעיף בונוס** – אין חובה לפתור: אם ידוע כי בשתי הסדרות ביחד האות $A$ מופיעה $n$ פעמים, כמה אותיות $A$ מופיעות בסדרה הראשונה **בממוצע**?",
    "contextId": "c3",
    "hold": "no-key",
})

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"לפניך גרף עבור פונקציית צפיפות ההסתברות $f_X(x)$ של משתנה מקרי $X$. מתקיים:" "\n"
          r"$$\begin{cases}P(0\le X\le a)=P(a\le X\le b)\\ \mathbb E[X]=\frac{23}{24}\end{cases}$$")

questions.append(Q(
    4, "א", "continuous_rv",
    Q4_TXT + "\n" + r"**א.** מצאו את הפרמטרים $a$, $b$ ו-$c$.",
    r"""מהגרף עולה כי פונקציית הצפיפות נתונה על ידי הנוסחה
$$f_X(x)=\begin{cases}c\dfrac xa,&0<x<a\\ c,&a\le x<b\\ 0,&\text{else}\end{cases}$$
- תנאי הנרמול מתבטא כך: $\dfrac{ac}2+c(b-a)=1$.
- $P(0\le X\le a)=\dfrac{ac}2$ ; $P(a\le X\le b)=c(b-a)$. נתון כי שתי ההסתברויות שוות: $\dfrac{ac}2=c(b-a)$.

משני התנאים הנ״ל: $\dfrac{ac}{2}=\dfrac12\Rightarrow ac=1$ ; $\ c(b-a)=\dfrac12\Rightarrow bc=\dfrac32$, ולכן $b=\dfrac32a$.
בנוסף, לפי התוחלת:
$$\mathbb E[X]=\int_0^a x\cdot c\frac xa\,dx+\int_a^b x\cdot c\,dx=\frac ca\cdot\frac{a^3}{3}+\frac c2(b^2-a^2)=\frac{ca^2}{3}+\frac{cb^2}{2}-\frac{ca^2}{2}=\frac{cb^2}{2}-\frac{ca^2}{6}$$
$$=(bc)\frac b2-(ac)\frac a6=\frac{3b}{4}-\frac a6=\frac34\cdot\frac32a-\frac a6=\frac{23}{24}a=\frac{23}{24}.$$
לכן
$$a=1,\qquad b=\frac32,\qquad c=1.$$""",
    10, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ב", "continuous_rv",
    Q4_TXT + "\n" + r"**ב.** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את התוצאה.",
    r"""$$F_X(t)=\begin{cases}0,&t<0,\\ \dfrac{t^2}{2},&0\le t<1,\\ t-\dfrac12,&1\le t<\dfrac32,\\ 1,&t\ge\dfrac32.\end{cases}$$
(הגרף: פרבולה מ-$(0,0)$ ל-$\left(1,\frac12\right)$, אחר כך קו ישר עד $\left(\frac32,1\right)$, ואחר כך $1$.)""",
    10, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ג", "continuous_rv",
    Q4_TXT + "\n" + r"**ג.** מהי ההסתברות $P(X>\mathbb E[X])$?",
    r"""$$P(X>\mathbb E[X])=P\left(X>\tfrac{23}{24}\right)=1-F_X\left(t=\tfrac{23}{24}\right)=1-\frac12\left(\frac{23}{24}\right)^2\approx 0.541.$$""",
    5, image=IMG + "Q4-pdf.png"))

# ------------------------------------------------------------------ Q5
Q5_TXT = (r"למבחן סוף הקורס ב״הסתברות״ אשר מתקיים **היום** נרשמו $N$ סטודנטים. בגלל סיבות שונות ומשונות, כל אחד מהסטודנטים מחליט להגיע למבחן בהסתברות $p$.")
Q5_HINT = (r"**הערה:** לידיעתך," "\n"
           r"$$\sum_{j=m}^{N}C_j^mC_N^ja^j=C_N^m\,a^m(1+a)^{N-m}.$$" "\n"
           r"(יכול להיות שאין צורך להשתמש בנוסחה זו.)")

questions.append(Q(
    5, "א", "special_discrete",
    r"**א.** יהי $X$ משתנה מקרי המתאר את מספר הסטודנטים אשר הגיעו למבחן. איך משתנה זה מפולג? **עליך לתת הסבר מפורט.**",
    r"""$$P(X=j)=\binom Nj p^j(1-p)^{N-j},\qquad X\sim\mathrm{Bin}(N,p),\qquad j=0,1,\dots,N.$$
(כל סטודנט הוא ניסוי ברנולי בלתי תלוי: מגיע בהסתברות $p$.)""",
    3, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    r"**ב.** יהי $Y$ משתנה מקרי המתאר את מספר הסטודנטים – **מתוך אלה שהגיעו למבחן** – אשר נולדו **היום** (כלומר, בתאריך המבחן). מצאו את פונקציית ההסתברות של משתנה זה." "\n" + Q5_HINT,
    r"""לפי נוסחת ההסתברות השלמה:
$$P(Y=k)=\sum_{j=k}^{N}P(Y=k/X=j)\,P(X=j).$$
ידוע כי בהינתן $X=j$, ההסתברות שבדיוק $k$ מהם נולדו בתאריך המבחן היא $\binom jk Q^k(1-Q)^{j-k}$ עם $Q=\dfrac1{365}$. לכן
$$P(Y=k)=\sum_{j=k}^{N}\binom jk Q^k(1-Q)^{j-k}\binom Nj p^j(1-p)^{N-j}=\frac{Q^k}{(1-Q)^k}(1-p)^N\sum_{j=k}^{N}\binom jk\binom Nj\left(\frac{p}{1-p}(1-Q)\right)^j.\qquad(*)$$
הסכום כפי שהוא שווה בדיוק לסכום המופיע ברמז, עם $m=k$ ו-$a=\dfrac p{1-p}(1-Q)$:
$$\sum_{j=k}^N\binom jk\binom Nj\left(\frac p{1-p}(1-Q)\right)^j=\binom Nk\frac{(1-pQ)^{N-k}p^k(1-Q)^k}{(1-p)^N}.$$
הצבה חזרה ל-$(*)$ ופישוט נותנים:
$$P(Y=k)=\binom Nk(pQ)^k(1-pQ)^{N-k},\qquad k=0,1,\dots,N.$$
**קיים פתרון חלופי קצר ללא שימוש ברמז:** נסתכל על כל אחד מ-$N$ הסטודנטים על ידי זוג משתני ברנולי: $X_j=1$ אם הגיע למבחן (הסתברות $p$), $\tilde X_j=1$ אם נולד בתאריך המבחן (הסתברות $Q$). אם רוצים לספור את אלה שגם הגיעו למבחן וגם נולדו בתאריך המבחן, ניתן לעשות זאת בעזרת משתנה ברנולי $Y_j=X_j\cdot\tilde X_j\sim\mathrm{Ber}(pQ)$ (גם הגיע וגם נולד בתאריך המבחן). לכן $Y=\sum_{j=1}^NY_j\sim\mathrm{Bin}(N,pQ)$ (לפי משפט הפירוק).""",
    16, contextId="c5"))

questions.append(Q(
    5, "ג", "conditional_bayes",
    r"**ג.** **אם ידוע** כי בין כל הסטודנטים שהגיעו למבחן בדיוק $k$ נולדו בתאריך המבחן, מהי ההסתברות שבדיוק $n$ סטודנטים הגיעו למבחן?",
    r"""הסתברות מותנית (נוסחת בייס):
$$P(X=n/Y=k)=\frac{P(Y=k/X=n)\,P(X=n)}{P(Y=k)}=\frac{\binom nk Q^k(1-Q)^{n-k}\cdot\binom Nn p^n(1-p)^{N-n}}{\binom Nk(pQ)^k(1-pQ)^{N-k}}.$$
לאחר הצמצום ופישוט מתקבל
$$P(X=n/Y=k)=\binom{N-k}{N-n}\,(\tilde p)^{N-n}(1-\tilde p)^{N-k-(N-n)},\qquad \tilde p=\frac{1-p}{1-pQ}.$$""",
    6, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_TXT = (r"סטודנט של המכון הטכנולוגי חולון הרכיב מעגל חשמלי $Q_1$ מחמש יחידות $A,B,C,D$ ו-$E$ הפועלות ללא תלות אחת בשנייה בהסתברויות זהות $p$. "
          r"לאחר מכן, הוא פירק את המעגל והרכיב מעגל חדש $Q_2$ – מאותן היחידות.")

questions.append(Q(
    6, "א", "circuits",
    r"**א.** מהי ההסתברות שמעגל $Q_1$ פעיל?",
    r"""$$P(Q_1)=P(Q_2)=p\,(2p-p^2)^2+(1-p)(2p^2-p^4)=p^2\bigl(2+2p-5p^2+2p^3\bigr).$$
(מותנים ביחידה האמצעית: אם היא פעילה, שני זוגות מקבילים בטור, $(2p-p^2)^2$; אם לא, שני מסלולים בני שני רכיבים, $2p^2-p^4$. ב-$Q_2$ היחידה האמצעית היא $A$ במקום $E$, ולכן ההסתברות זהה.)""",
    3, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"**ב.** **אם ידוע** כי מעגל $Q_1$ פעיל, מהי ההסתברות שגם המעגל $Q_2$ יפעל?",
    r"""$$P(Q_2/Q_1)=\frac{P(Q_1\cap Q_2)}{P(Q_1)}.$$
נחשב את $P(Q_1\cap Q_2)$ בהתניה על $A$ ו-$E$; נסמן ב-$\tilde Q=Q_1\cap Q_2$ את המעגל שהמתקבל על ידי חיבור $Q_1$ ו-$Q_2$ בטור:
$$P(\tilde Q)=P(\tilde Q/A\cap E)P(A\cap E)+P(\tilde Q/\bar A\cap\bar E)P(\bar A\cap\bar E)+P(\tilde Q/A\cap\bar E)P(A\cap\bar E)+P(\tilde Q/\bar A\cap E)P(\bar A\cap E).$$
- $\tilde Q/A\cap E$: שני הגשרים מצטמצמים ל-$B\cup D$ (אחרי ש-$A$ ו-$E$ פעילים), כלומר $P=P(B\cup D)=2p-p^2$, וההסתברות לכך $p^2$ (נפרש גם כי שתי הצורות זהות: ברכיב $(2p-p^2)$ שמופיע כאן הוא $P(B\cup D)$ לכל גשר, והנתיב הכולל הוא אותו רכיב, ולכן $P(\tilde Q/A\cap E)=2p-p^2$);
- $\tilde Q/\bar A\cap\bar E$: $P(C\cap D)=p^2$, וההסתברות לכך $(1-p)^2$;
- $\tilde Q/A\cap\bar E$: $P=P\bigl(C\cap(B\cup D)\bigr)=p(2p-p^2)$, וההסתברות לכך $p(1-p)$;
- $\tilde Q/\bar A\cap E$: $P=p(2p-p^2)$ (באופן סימטרי), וההסתברות לכך $p(1-p)$.

לאחר הצבה:
$$P(Q_1\cap Q_2)=(2p-p^2)\,p^2+p^2(1-p)^2+2p(1-p)\,p(2p-p^2)=p^2\bigl(1+4p-6p^2+2p^3\bigr).$$
ולכן
$$P(Q_2/Q_1)=\frac{1+4p-6p^2+2p^3}{2+2p-5p^2+2p^3}.$$
**פתרון חלופי (התניה על $A$ ו-$\bar A$ בלבד):**
- $P(\tilde Q/A)=(2p-p^2)^2$ (כש-$A$ פעיל: $(E\cup C)\cap(B\cup D)$ פועלים בטור);
- $P(\tilde Q/\bar A)=P\bigl(C\cap((E\cap B)\cup D)\bigr)=p\,(p^2+p-p^3)=p^2(1+p-p^2)$.

$$P(\tilde Q)=P(\tilde Q/A)P(A)+P(\tilde Q/\bar A)P(\bar A)=p(2p-p^2)^2+(1-p)\,p^2(1+p-p^2)=p^2\bigl(1+4p-6p^2+2p^3\bigr).$$""",
    16, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    r"**ג.** מהי ההסתברות שלפחות מעגל אחד פעיל?",
    r"""$$P(Q_1\cup Q_2)=P(Q_1)+P(Q_2)-P(Q_1\cap Q_2).$$
לאחר הצבה ופישוט מתקבל
$$P(Q_1\cup Q_2)=p^2\bigl(3-4p^2+2p^3\bigr).$$""",
    6, contextId="c6"))

exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ד, מועד א (25.03.2024)",
    "year": 2024,
    "examDate": "25.03.2024",
    "sourceFile": "24A-A exam pp.1-3",
    "solutionFile": "24A-A official handwritten solutions pp.4-19",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: מלבן", "image": IMG + "Q1-rect.png", "caption": Q1_TXT},
        "c3": {"kind": "image", "title": "שאלה 3: סדרות אותיות", "image": IMG + "Q3-strings.png", "caption": Q3_TXT},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_TXT},
        "c6": {"kind": "image", "title": "שאלה 6: מעגלים", "image": IMG + "Q6-circuits.png", "caption": Q6_TXT},
    },
    "questions": questions,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
