# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-A.json -- probability (course 20021), semester A 2024, moed A (25.03.2024).
This is the 20021 group; the 20021-80 group of 3.4.2024 is 24A-D. 6 questions, 22 items
(Q1 5, Q2 4, Q3 4, Q4 3, Q5 3, Q6 3), 25 points each. The two bonus parts (Q2 ד, Q3 ד) have no key and are solved.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-A.py

Source: exam pp.1-3, official handwritten solutions pp.4-19.
Transcription notes
- Part keys are single letters. Q1 prints א-1, א-2, א-3, ב, ג -> keys א ב ג ד ה (a=א-1, b=א-2, c=א-3, d=ב, e=ג).
  The printed label is the bold token at the start of each question text.
- Q2 asks for the probability that the running sum of a fair N-sided die ever equals N ("שאי פעם נגיע לסכום").
- Q2(ד) and Q3(ד) are bonus parts ("אין חובה לפתור"); the official solution has no answer for either -> solved
  (solutionSource "solved", official:false): P_N = (1/N)(1+1/N)^(N-1) (compositions of N) and
  E[X1 | X=n] = n N1/(N1+N2) (hypergeometric mean). Verified exactly and by Monte Carlo in tools/verify/24A-A/check.py.
- Q5(ב) has the main solution and the official short alternative (sum of Bernoulli).
- Q6(ב): the official solution has two methods (conditioning on A,E and on A alone); both are given.
- The thumbnail of the exam cover in Q5 is decoration and is not shipped.
- Q1 area items (a-c) carry a `region` (moved from the old regions.json); sims are checked by check_sim_specs; steps by tools/verify/24A-A/steps_check.py.
"""
import json, pathlib
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from verified import src as _vsrc

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

questions.append(Q(
    2, "ד", "special_discrete",
    r"**סעיף בונוס** – אין חובה לפתור: מטילים קובייה מאוזנת בעלת $N$ פאות ומסכמים את התוצאות. מהי ההסתברות $P_N$ שאי פעם נגיע לסכום התוצאות השווה ל-$N$? **אליך לתת חישוב מפורט.**",
    r"""**פתרון (אין פתרון רשמי לסעיף הבונוס).**
ההסתברות לקבל תוצאה ספציפית בהטלה היא $p=\dfrac1N$. כמו בסעיפים א-ג, נפריד לפי מספר ההטלות $k$ שבהן מגיעים לסכום $N$ בפעם הראשונה ($k=1,\dots,N$).
מגיעים לסכום $N$ בדיוק אחרי $k$ הטלות אם ורק אם $k$ התוצאות הראשונות הן מספרים שלמים חיוביים שסכומם $N$ (כל תוצאה כזו קטנה או שווה ל-$N$, ולכן היא אפשרית בקובייה). מספר הסדרות הסדורות של $k$ מספרים שלמים חיוביים שסכומם $N$ הוא $\binom{N-1}{k-1}$ (בוחרים $k-1$ נקודות חיתוך מבין $N-1$ הרווחים), וכל סדרה כזו מתקבלת בהסתברות $p^k$.
המאורעות עבור ערכי $k$ שונים זרים (הסכום הרץ עולה ממש, ולכן עובר את $N$ לכל היותר פעם אחת). לכן
$$P_N=\sum_{k=1}^{N}\binom{N-1}{k-1}p^k=p\sum_{j=0}^{N-1}\binom{N-1}{j}p^j=p(1+p)^{N-1}.$$
כלומר
$$P_N=\frac1N\left(1+\frac1N\right)^{N-1},$$
בהתאם לתבנית של $P_3$, $P_4$ ו-$P_5$ בסעיפים א-ג.""",
    3, solutionSource="solved", official=False))

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

questions.append(Q(
    3, "ד", "special_discrete",
    r"**סעיף בונוס** – אין חובה לפתור: אם ידוע כי בשתי הסדרות ביחד האות $A$ מופיעה $n$ פעמים, כמה אותיות $A$ מופיעות בסדרה הראשונה **בממוצע**?",
    r"""**פתרון (אין פתרון רשמי לסעיף הבונוס).**
צריך את התוחלת המותנית $\mathbb E[X_1/X=n]$. לפי סעיף ג, בהינתן $X=n$ ההתפלגות של $X_1$ היא היפרגאומטרית:
$$P(X_1=k/X=n)=\frac{\binom{N_1}{k}\binom{N_2}{n-k}}{\binom{N_1+N_2}{n}}.$$
לכן
$$\mathbb E[X_1/X=n]=\sum_k k\,\frac{\binom{N_1}{k}\binom{N_2}{n-k}}{\binom{N_1+N_2}{n}}.$$
נשתמש בזהות $k\binom{N_1}{k}=N_1\binom{N_1-1}{k-1}$ ובזהות ונדרמונד $\sum_k\binom{N_1-1}{k-1}\binom{N_2}{n-k}=\binom{N_1+N_2-1}{n-1}$:
$$\mathbb E[X_1/X=n]=\frac{N_1\binom{N_1+N_2-1}{n-1}}{\binom{N_1+N_2}{n}}=N_1\cdot\frac{n}{N_1+N_2}.$$
כלומר
$$\mathbb E[X_1/X=n]=\frac{nN_1}{N_1+N_2},$$
התוצאה לא תלויה ב-$p$: בהינתן $n$ אותיות $A$ בסך הכול, כל אחד מ-$N_1+N_2$ המקומות נושא $A$ באותה הסתברות $\frac{n}{N_1+N_2}$, ובסדרה הראשונה יש $N_1$ מקומות.""",
    3, contextId="c3", solutionSource="solved", official=False))

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


# ---- 24A-A specifics: area figures, simulations, steps
S12 = {"x": [0, 1], "y": [0, 2]}
_pq = 0.6 / 365                             # p*Q at p=0.6, Q=1/365 (Q5)


def _pY(k):
    from math import comb
    return comb(5, k) * _pq ** k * (1 - _pq) ** (5 - k)


_pt = (1 - 0.6) / (1 - _pq)                 # p-tilde of part c at p=0.6
_ABs = BER(0.6, *["A%d" % i for i in range(1, 6)]) | BER(1 / 365, *["B%d" % i for i in range(1, 6)])
_SA = "+".join("A%d" % i for i in range(1, 6))
_SY = "+".join("A%d*B%d" % (i, i) for i in range(1, 6))
_c = 4 * _pt ** 3 * (1 - _pt)
_L2 = math.log(2)


def _runs(N):
    """event 'the running sum of an N-faced die ever equals N' as an expression over d1..dN"""
    return " or ".join("+".join("d%d" % j for j in range(1, k + 1)) + " == %d" % N for k in range(1, N + 1))


def _P(N):
    return (1 / N) * (1 + 1 / N) ** (N - 1)


_B1 = "(A and B) or (C and D) or (A and E and D) or (C and E and B)"
_B2 = "(E and B) or (C and D) or (E and A and D) or (C and A and B)"
_p6 = 0.6
_PQ1 = _p6 ** 2 * (2 + 2 * _p6 - 5 * _p6 ** 2 + 2 * _p6 ** 3)
_PI = _p6 ** 2 * (1 + 4 * _p6 - 6 * _p6 ** 2 + 2 * _p6 ** 3)
_PU = _p6 ** 2 * (3 - 4 * _p6 ** 2 + 2 * _p6 ** 3)
_pAB = {c: _p6 for c in "ABCDE"}
_pdf4 = [(0, 1, "x"), (1, "3/2", "1")]
_X1, _X2 = BIN(3, 0.3), BIN(2, 0.3)
_XX = {"X1": _X1, "X2": _X2}

EXTRAS.update({
    (1, "א"): {"region": REG([{"expr": "x*y", "op": "<", "c": 1}], (1 + _L2) / 2, "האירוע S=XY<1 (עקום y=1/x)", space=S12), "sim": AREA("P(S<1)", (1 + _L2) / 2)},
    (1, "ב"): {"region": REG([lin(1, 1, 1, "<")], 1 / 4, "האירוע L<2, כלומר X+Y<1", space=S12), "sim": AREA("P(L<2)", 1 / 4)},
    (1, "ג"): {"region": REG([{"expr": "x*y", "op": "<", "c": 1}], 1 / 3 + 2 * _L2 / 3, "האירוע S<1 בהינתן L>2 (X+Y>1)", given=[lin(1, 1, 1, ">")], space=S12),
               "sim": AREA("P(S<1 | L>2)", 1 / 3 + 2 * _L2 / 3)},
    (1, "ד"): {"sim": AREA("Var[S]", 7 / 36, space=S12, measure="var", expr="x*y")},
    (1, "ה"): {"sim": AREA("Var[L]", 5 / 3, space=S12, measure="var", expr="2*(x+y)")},
    (2, "א"): {"sim": DICE("P_3 (קובייה בעלת 3 פאות)", _P(3), 3, _runs(3), faces=3)},
    (2, "ב"): {"sim": DICE("P_4 (קובייה בעלת 4 פאות)", _P(4), 4, _runs(4), faces=4)},
    (2, "ג"): {"sim": DICE("P_5 (קובייה בעלת 5 פאות)", _P(5), 5, _runs(5), faces=5)},
    (2, "ד"): {"sim": DICE("P_N ב-N=6", _P(6), 6, _runs(6), faces=6)},
    (3, "א"): {"sim": CUST("P(X1=2) ב-N1=3, p=0.3", 0.189, _XX, event="X1 == 2")},
    (3, "ב"): {"sim": CUST("P(X=2) ב-N1=3, N2=2, p=0.3", 0.3087, _XX, event="X1 + X2 == 2")},
    (3, "ג"): {"sim": CUST("P(X1=1 | X=2) ב-N1=3, N2=2, p=0.3", 0.6, _XX, event="X1 == 1", given="X1 + X2 == 2")},
    (3, "ד"): {"sim": CUST("E[X1 | X=2] ב-N1=3, N2=2, p=0.3", 1.2, _XX, given="X1 + X2 == 2", measure="mean", expr="X1")},
    (4, "א"): {"sim": PDF("E[X] ב-a=1, b=3/2, c=1", 23 / 24, _pdf4, measure="mean", expr="x")},
    (4, "ב"): {"sim": PDF("F_X(5/4)=P(X<=5/4)", 3 / 4, _pdf4, "x <= 5/4")},
    (4, "ג"): {"sim": PDF("P(X>E[X])", 1 - 0.5 * (23 / 24) ** 2, _pdf4, "x > 23/24")},
    (5, "א"): {"sim": CUST("P(X=3) ב-N=5, p=0.6", 0.3456, BER(0.6, *["A%d" % i for i in range(1, 6)]), event=_SA + " == 3")},
    (5, "ב"): {"sim": CUST("P(Y=1) ב-N=5, p=0.6, Q=1/365", _pY(1), _ABs, event=_SY + " == 1", trials=400000)},
    (5, "ג"): {"sim": CUST("P(X=2 | Y=1) ב-N=5, p=0.6, Q=1/365", _c, _ABs, event=_SA + " == 2", given=_SY + " == 1", trials=1000000)},
    (6, "א"): {"sim": CIRC("P(Q1) ב-p=0.6", _PQ1, _pAB, _B1)},
    (6, "ב"): {"sim": CIRC("P(Q2 | Q1) ב-p=0.6", _PI / _PQ1, _pAB, _B2, _B1)},
    (6, "ג"): {"sim": CIRC("P(Q1 או Q2) ב-p=0.6", _PU, _pAB, "(" + _B1 + ") or (" + _B2 + ")")},
})

OMR = r"מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X,Y)$, כלומר המלבן $(0,1)\times(0,2)$?"
OMR_X = r"המלבן ברוחב $1$ ובגובה $2$ הוא מרחב המדגם, ושטחו $2$. ההסתברות היא שטח האירוע חלקי $2$."

ADD(1, "א",
    RB((r"גישה גאומטרית: $|\Omega|=2$", 1), (r"גבול האירוע $y=\frac1x$ חותך את $y=2$ ב-$x=\frac12$", 1), (r"שטח $=2\cdot\frac12+\int_{1/2}^1\frac{dx}{x}=1+\ln2$", 2), (r"התשובה $\frac12(1+\ln2)$", 1)),
    [r"לשכוח שהעקום חותך את $y=2$ (שטח הקטע הראשון הוא $2\cdot\frac12$)", r"לחלק ב-$1$ ולא ב-$2$"],
    [NU(OMR, 2, OMR_X),
     NU(r"באיזה $x$ העקום $y=\frac1x$ חותך את הקו $y=2$ (קצה המלבן העליון)?", Fr(1, 2), r"$\frac1x=2\Rightarrow x=\frac12$. עבור $x<\frac12$ כל גובה המלבן בתוך האירוע."),
     NU(r"מהו שטח האירוע $\{xy<1\}$ בתוך המלבן?", 1 + math.log(2), r"$2\cdot\frac12+\int_{1/2}^1\frac{dx}{x}=1+\ln2\approx1.6931$."),
     NU(r"מהי $P(S<1)$?", (1 + math.log(2)) / 2, r"$\frac{1+\ln2}{2}\approx0.8466$.")])

ADD(1, "ב",
    RB((r"הגדרת $L=2(X+Y)<2$ כ-$X+Y<1$", 1), (r"האירוע הוא משולש בפינה $(0,0)$ בשטח $\frac12$ (בתוך המלבן)", 3), (r"התשובה $\frac14$", 1)),
    [r"לשכוח שהיקף הוא $2(X+Y)$ ולכתוב $X+Y<2$", r"לחלק ב-$\frac12$ או ב-$1$ במקום ב-$2$"],
    [NU(OMR, 2, OMR_X),
     NU(r"מהו שטח האירוע $\{x+y<1\}$ בתוך המלבן? (משולש בפינה $(0,0)$)", Fr(1, 2), r"הישר חותך את הצירים ב-$(1,0)$ וב-$(0,1)$, שניהם בתוך המלבן: ניצבים $1$ ו-$1$, שטח $\frac12$."),
     NU(r"מהי $P(L<2)$?", Fr(1, 4), r"$\frac{1/2}{2}=\frac14$.")])

ADD(1, "ג",
    RB((r"הגדרת הסתברות מותנית $\frac{P(S<1\cap L>2)}{P(L>2)}$", 1), (r"$P(L>2)=1-\frac14=\frac34$", 1), (r"שטח החיתוך $\frac12+\ln2$", 2), (r"התשובה $\frac13+\frac23\ln2$", 1)),
    [r"לחלק ב-$P(S<1)$ במקום ב-$P(L>2)$", r"לשכוח להחסיר את שטח המשולש מהאזור מתחת לעקום"],
    [NU(OMR, 2, OMR_X),
     NU(r"מהי $P(L>2)$? (אירוע התנאי; המכנה)", Fr(3, 4), r"$1-\frac14=\frac34$, כלומר שטח $\frac32$."),
     NU(r"מהו שטח החיתוך $\{xy<1\}\cap\{x+y>1\}$ בתוך המלבן?", 0.5 + math.log(2), r"$(1+\ln2)-\frac12=\frac12+\ln2\approx1.1931$."),
     NU(r"מהי $P(S<1\mid L>2)$?", 1 / 3 + 2 * math.log(2) / 3, r"$\frac{(1/2+\ln2)/2}{3/4}=\frac13+\frac23\ln2\approx0.7954$.")])

ADD(1, "ד",
    RB((r"אי-תלות: $\mathbb E[XY]=\mathbb E[X]\mathbb E[Y]$", 1), (r"$\mathbb E[S]=\frac12$", 1), (r"$\mathbb E[S^2]=\mathbb E[X^2]\mathbb E[Y^2]=\frac49$", 2), (r"$\operatorname{Var}[S]=\frac7{36}$", 1)),
    [r"לחשב $\operatorname{Var}[S]=\operatorname{Var}[X]\operatorname{Var}[Y]$ (אינו נכון)", r"לטעות ב-$\mathbb E[Y^2]=\frac43$"],
    [CH(r"מדוע $\mathbb E[S]=\mathbb E[X]\,\mathbb E[Y]$?",
        [r"כי $X$ ו-$Y$ בלתי תלויים", r"כי התוחלת ליניארית ולכן $\mathbb E[XY]=\mathbb E[X]+\mathbb E[Y]$", r"כי זה נכון תמיד, גם בלי אי-תלות"], 0,
        r"התוחלת ליניארית לסכומים בלבד; למכפלה נדרשת אי-תלות (או חוסר מתאם). ב-$X,Y$ הנתונים הסכום היה נותן $\frac32$ ולא $\frac12$."),
     NU(r"מהי $\mathbb E[S]$?", Fr(1, 2), r"$\frac12\cdot1=\frac12$."),
     NU(r"מהי $\mathbb E[S^2]=\mathbb E[X^2]\,\mathbb E[Y^2]$?", Fr(4, 9), r"$\frac13\cdot\frac43=\frac49$."),
     NU(r"מהי $\operatorname{Var}[S]$?", Fr(7, 36), r"$\frac49-\frac14=\frac7{36}$.")])

ADD(1, "ה",
    RB((r"ליניאריות התוחלת: $\mathbb E[L]=2(\mathbb E[X]+\mathbb E[Y])=3$", 2), (r"שונות סכום בלתי תלויים: $\operatorname{Var}[X+Y]=\operatorname{Var}[X]+\operatorname{Var}[Y]$ ומקדם $4$ מהכפלה ב-$2$", 2), (r"$\operatorname{Var}[L]=\frac53$", 1)),
    [r"לכתוב $\operatorname{Var}[2(X+Y)]=2(\operatorname{Var}[X]+\operatorname{Var}[Y])$ (מקדם $2$ במקום $4$)", r"לטעות בשונות של $U(0,2)$: $\frac13$ ולא $\frac1{12}$"],
    [CH(r"איך מחשבים את $\operatorname{Var}[2(X+Y)]$?",
        [r"$4\bigl(\operatorname{Var}[X]+\operatorname{Var}[Y]\bigr)$", r"$2\bigl(\operatorname{Var}[X]+\operatorname{Var}[Y]\bigr)$", r"$4\operatorname{Var}[X]\operatorname{Var}[Y]$"], 0,
        r"קבוע מוצא מהשונות בריבוע ($2^2=4$), ושונות סכום של בלתי תלויים היא סכום השונויות. הנוסחה השנייה נותנת $\frac56$ והשלישית $\frac1{9}$, בעוד הנכון $\frac53$."),
     NU(r"מהי $\operatorname{Var}[X]$ של $X\sim U(0,1)$?", Fr(1, 12), r"$\frac{1^2}{12}$."),
     NU(r"מהי $\operatorname{Var}[Y]$ של $Y\sim U(0,2)$?", Fr(1, 3), r"$\frac{2^2}{12}=\frac13$."),
     NU(r"מהי $\operatorname{Var}[L]$?", Fr(5, 3), r"$4\left(\frac1{12}+\frac13\right)=\frac53$.")])

# ---- Q2: running sum of a fair N-faced die ever hits N: P_N = p(1+p)^(N-1), p = 1/N
ADD(2, "א",
    RB((r"פיצול לפי מספר ההטלות: $\{3\}$, $\{2,1\},\{1,2\}$, $\{1,1,1\}$", 3), (r"הסתברות $p^k$ לכל מסלול באורך $k$ ($p=\frac13$)", 2), (r"סכום: $p(1+p)^2=\frac{16}{27}$", 2)),
    [r"לכתוב $P_3=\frac13$ (רק הטלה אחת)", r"להסיק ש-$P_3=1$ כי הסכום ״בסוף מגיע״ (אפשר לדלג על $3$)"],
    [CH(r"קובייה בעלת $3$ פאות. איך מחשבים את ההסתברות שהסכום הרץ ייעצר בדיוק על $3$ בשלב כלשהו?",
        [r"מפצלים לפי מספר ההטלות $k$: כל סדרה של $k$ תוצאות חיוביות שסכומן $3$ מתקבלת בהסתברות $p^k$, והמקרים זרים",
         r"$p=\frac13$, כי צריך לקבל $3$ בהטלה אחת", r"$1$, כי הסכום עולה ובסוף מגיע ל-$3$"], 0,
        r"גם סדרות כמו $(1,2)$ ו-$(1,1,1)$ מגיעות ל-$3$, ולכן $\frac13$ נמוך מדי ($P_3=\frac{16}{27}$). הסכום יכול לדלג מעל $3$ (למשל $2$ ואז $2$), ולכן ההסתברות קטנה מ-$1$."),
     NU(r"כמה סדרות של שתי הטלות נותנות סכום $3$?", 2, r"$(1,2)$ ו-$(2,1)$."),
     NU(r"כמה סדרות של שלוש הטלות נותנות סכום $3$?", 1, r"$(1,1,1)$."),
     NU(r"מהי $P_3$?", Fr(16, 27), r"$p+2p^2+p^3=\frac13+\frac29+\frac1{27}=\frac{16}{27}$.")])

ADD(2, "ב",
    RB((r"פיצול לפי מספר ההטלות: מספר הסדרות לכל $k$ הוא $\binom{3}{k-1}$", 3), (r"הסתברות $p^k$ לכל מסלול ($p=\frac14$)", 3), (r"סכום: $p(1+p)^3=\frac{125}{256}$", 2)),
    [r"לספור סדרות כקבוצות ללא סדר ($\{3,1\}$ ו-$\{1,3\}$ כאחת)", r"לשכוח את מסלול הארבע הטלות"],
    [CH(r"קובייה בעלת $4$ פאות. איך סופרים את המסלולים שמגיעים ל-$4$?",
        [r"סדרות סדורות של $k$ מספרים חיוביים שסכומם $4$ (הסדר חשוב), בהסתברות $p^k$ כל אחת", r"קבוצות ללא סדר: $\{3,1\}$ ו-$\{1,3\}$ נספרות כאחת", r"כל $4^k$ הסדרות באורך $k$"], 0,
        r"$(3,1)$ ו-$(1,3)$ הן תוצאות שונות, כל אחת בהסתברות $p^2$. ספירה ללא סדר נותנת $0.3945$ (נמוך מהנכון $0.4883$), ו-$4^k$ סופר גם סדרות שסכומן אינו $4$."),
     NU(r"כמה סדרות של שתי הטלות נותנות סכום $4$?", 3, r"$(2,2),(3,1),(1,3)$."),
     NU(r"כמה סדרות של שלוש הטלות נותנות סכום $4$?", 3, r"$(1,1,2),(1,2,1),(2,1,1)$."),
     NU(r"מהי $P_4$?", Fr(125, 256), r"$p+3p^2+3p^3+p^4=\frac14\left(\frac54\right)^3=\frac{125}{256}$.")])

ADD(2, "ג",
    RB((r"פיצול לפי מספר ההטלות $k=1,\dots,5$ עם $\binom4{k-1}$ סדרות", 4), (r"הסתברות $p^k$ לכל מסלול ($p=\frac15$)", 4), (r"סכום: $p(1+p)^4=\frac{1296}{3125}$", 2)),
    [r"לשכוח סדרות מעורבות כמו $(1,2,2)$", r"לחשב $p^5$ בלבד"],
    [CH(r"קובייה בעלת $5$ פאות. איך מחשבים את ההסתברות להגיע לסכום $5$?",
        [r"סוכמים על $k=1,\dots,5$ את מספר הסדרות הסדורות עם סכום $5$ כפול $p^k$", r"רק המסלול של חמש יחידות: $p^5$", r"רק המסלול של הטלה אחת: $p$"], 0,
        r"יש מסלולים מכל אורך $1$ עד $5$. $p^5=0.00032$ ו-$p=0.2$ רחוקים מהנכון $0.41472$."),
     NU(r"כמה סדרות של שתי הטלות נותנות סכום $5$?", 4, r"$(1,4),(4,1),(2,3),(3,2)$."),
     NU(r"כמה סדרות של שלוש הטלות נותנות סכום $5$?", 6, r"$\binom42=6$: שלוש תמורות של $(1,1,3)$ ושלוש של $(1,2,2)$."),
     NU(r"כמה סדרות של ארבע הטלות נותנות סכום $5$?", 4, r"אחת מהן $2$ והיתר $1$: $4$ מקומות."),
     NU(r"מהי $P_5$?", Fr(1296, 3125), r"$p(1+p)^4=\frac15\left(\frac65\right)^4=\frac{1296}{3125}\approx0.41472$.")])

ADD(2, "ד",
    RB((r"מספר הסדרות הסדורות של $k$ מספרים חיוביים שסכומם $N$ הוא $\binom{N-1}{k-1}$", 1), (r"סכום $\sum_k\binom{N-1}{k-1}p^k$ ומשפט הבינום", 1), (r"$P_N=\frac1N\left(1+\frac1N\right)^{N-1}$", 1)),
    [r"לכתוב טור גאומטרי במקום משפט הבינום"],
    [CH(r"איך מסכמים את $\sum_{k=1}^N\binom{N-1}{k-1}p^k$?",
        [r"בעזרת משפט הבינום: $p(1+p)^{N-1}$", r"בעזרת טור גאומטרי: $p\frac{1-p^N}{1-p}$", r"$Np$"], 0,
        r"המקדמים בינומיים ולכן משפט הבינום מתאים. ב-$N=6$ הטור הגאומטרי נותן $0.2$ ו-$Np=1$, לעומת הנכון $0.3602$."),
     NU(r"כמה סדרות של שלוש הטלות נותנות סכום $6$? ($\binom{5}{2}$)", 10, r"$\binom{N-1}{k-1}=\binom52=10$."),
     NU(r"מהי $P_6$?", 16807 / 46656, r"$\frac16\left(\frac76\right)^5=\frac{16807}{46656}\approx0.36023$.")])

# ---- Q3: two strings; numeric checks at N1=3, N2=2, p=0.3
ADD(3, "א",
    RB((r"כל אות בסדרה היא ניסוי ברנולי בלתי תלוי עם הסתברות $p$ ל-$A$", 3), (r"$X_1\sim\mathrm{Bin}(N_1,p)$ ופונקציית ההסתברות", 3), (r"אותו דבר ל-$X_2\sim\mathrm{Bin}(N_2,p)$", 3)),
    [r"לא לנמק את אי-התלות בין האותיות", r"להחליף בין $N_1$ ל-$N_2$ בפונקציית ההסתברות"],
    [CH(r"סדרה בת $N_1$ אותיות, כל אחת $A$ בהסתברות $p$ באופן בלתי תלוי. איך מפולג $X_1$ (מספר ה-$A$)?",
        [r"$\mathrm{Bin}(N_1,p)$", r"פואסון עם פרמטר $N_1p$", r"גאומטרית עם פרמטר $p$"], 0,
        r"מספר קבוע של ניסויים בלתי תלויים נותן בינומית. פואסון אינו חסום ($X_1\le N_1$), וגאומטרית סופרת ניסויים עד ההצלחה הראשונה."),
     NU(r"מהי $P(X_1=0)$ כאשר $N_1=3$ ו-$p=0.3$?", Fr(343, 1000), r"$(1-p)^3=0.343$."),
     NU(r"מהי $P(X_1=2)$ באותם ערכים?", Fr(189, 1000), r"$\binom32(0.3)^2(0.7)=0.189$.")])

ADD(3, "ב",
    RB((r"הצגת $X_1$ ו-$X_2$ כסכומי ברנולי בלתי תלויים", 3), (r"$X$ הוא סכום של $N_1+N_2$ ברנולי בלתי תלויים עם אותו $p$", 3), (r"$X\sim\mathrm{Bin}(N_1+N_2,p)$ ופונקציית ההסתברות", 3)),
    [r"לכתוב $\mathrm{Bin}(N_1N_2,p)$", r"להוכיח בלי להסביר מדוע ההסתברויות זהות ($p$ זהה בשתי הסדרות)"],
    [CH(r"$X=X_1+X_2$ עם $X_1\sim\mathrm{Bin}(N_1,p)$ ו-$X_2\sim\mathrm{Bin}(N_2,p)$ בלתי תלויים. איך מפולג $X$?",
        [r"$\mathrm{Bin}(N_1+N_2,p)$", r"$\mathrm{Bin}(N_1N_2,p)$", r"$\mathrm{Bin}(N_1+N_2,2p)$"], 0,
        r"סכום של $N_1+N_2$ ברנולי בלתי תלויים עם אותו $p$. הכפלה $N_1N_2$ נותנת מספר ניסויים שגוי, ו-$2p$ אינו הסתברות חוקית כש-$p>\frac12$."),
     NU(r"כמה ניסויי ברנולי בלתי תלויים מרכיבים את $X$ כאשר $N_1=3$, $N_2=2$?", 5, r"$N_1+N_2=5$."),
     NU(r"מהי $P(X=2)$ כאשר $p=0.3$?", Fr(3087, 10000), r"$\binom52(0.3)^2(0.7)^3=10\cdot0.09\cdot0.343=0.3087$.")])

ADD(3, "ג",
    RB((r"הגדרת הסתברות מותנית: $\frac{P(X_1=k\cap X_2=n-k)}{P(X=n)}$", 2), (r"אי-תלות של הסדרות: המונה הוא מכפלה", 2), (r"צמצום ל-$\frac{\binom{N_1}k\binom{N_2}{n-k}}{\binom{N_1+N_2}n}$", 3)),
    [r"לכתוב את המונה כ-$P(X_1=k)P(X=n)$", r"לשכוח שהתנאי $X_2=n-k$ נובע מ-$X_1+X_2=n$"],
    [CH(r"איך מחשבים את $P(X_1=k\cap X=n)$?",
        [r"$P(X_1=k)\cdot P(X_2=n-k)$, כי $X_1,X_2$ בלתי תלויים", r"$P(X_1=k)\cdot P(X=n)$", r"$P(X_1=k)+P(X_2=n-k)$"], 0,
        r"האירוע $\{X_1=k,\,X=n\}$ שווה ל-$\{X_1=k,\,X_2=n-k\}$ והמשתנים בלתי תלויים. $X_1$ ו-$X$ תלויים (ב-$N_1=3,N_2=2,p=0.3$ המכפלה השנייה נותנת $0.1361$ במקום $0.18522$)."),
     NU(r"מהי $P(X=2)$ כאשר $N_1=3$, $N_2=2$, $p=0.3$? (המכנה: אירוע התנאי)", Fr(3087, 10000), r"$0.3087$ מסעיף ב."),
     NU(r"מהי $P(X_1=1\cap X_2=1)$ באותם ערכים? (המונה)", Fr(18522, 100000), r"$3(0.3)(0.7)^2\cdot2(0.3)(0.7)=0.441\cdot0.42=0.18522$."),
     NU(r"מהי $P(X_1=1\mid X=2)$?", Fr(3, 5), r"$\frac{0.18522}{0.3087}=0.6=\frac{\binom31\binom21}{\binom52}$.")])

ADD(3, "ד",
    RB((r"בהינתן $X=n$ ההתפלגות היפרגאומטרית (סעיף ג)", 1), (r"זהות $k\binom{N_1}k=N_1\binom{N_1-1}{k-1}$ וזהות ונדרמונד", 1), (r"$\mathbb E[X_1\mid X=n]=\frac{nN_1}{N_1+N_2}$", 1)),
    [r"לחשוב שהתוצאה תלויה ב-$p$"],
    [CH(r"נתון $X=n$. איך מפולג $X_1$ ומהי תלותו ב-$p$?",
        [r"היפרגאומטרית, ואינה תלויה ב-$p$", r"$\mathrm{Bin}(N_1,p)$, כמו ללא התנאי", r"$\mathrm{Bin}(n,\frac12)$"], 0,
        r"בהינתן $n$ אותיות $A$ מבין $N_1+N_2$ מקומות, כל קבוצה של $n$ מקומות שווה סיכוי, ולכן התוצאה היפרגאומטרית ובלתי תלויה ב-$p$. ב-$N_1=3,N_2=2,n=2$: $\mathbb E=1.2$ (לא $0.9=N_1p$, ולא $1$)."),
     NU(r"מהי $P(X_1=0\mid X=2)$ כאשר $N_1=3$, $N_2=2$?", Fr(1, 10), r"$\frac{\binom30\binom22}{\binom52}=\frac1{10}$."),
     NU(r"מהי $\mathbb E[X_1\mid X=2]$ באותם ערכים?", Fr(6, 5), r"$\frac{nN_1}{N_1+N_2}=\frac{2\cdot3}{5}=1.2$.")])

# ---- Q4: f = c x/a on (0,a), c on (a,b); a=1, b=3/2, c=1
ADD(4, "א",
    RB((r"נרמול: $\frac{ac}2+c(b-a)=1$", 2), (r"שוויון ההסתברויות: $\frac{ac}2=c(b-a)=\frac12$", 2), (r"$ac=1$, $bc=\frac32$ ולכן $b=\frac32a$", 2), (r"תוחלת: $\frac{23}{24}a=\frac{23}{24}$", 3), (r"$a=1$, $b=\frac32$, $c=1$", 1)),
    [r"לשכוח שהנרמול והשוויון הם שתי משוואות נפרדות", r"לטעות באינטגרל של התוחלת על הקטע $(a,b)$"],
    [NU(r"אם $P(0\le X\le a)=P(a\le X\le b)$, מהי $P(0\le X\le a)$?", Fr(1, 2), r"שתי ההסתברויות שוות וסכומן $1$: כל אחת $\frac12$."),
     NU(r"שטח המשולש הוא $\frac{ac}{2}=\frac12$. מהו המכפלה $ac$?", 1, r"$ac=1$."),
     NU(r"מה היחס $\frac ba$ אם גם $c(b-a)=\frac12$?", Fr(3, 2), r"$bc=\frac32$ ו-$ac=1$, לכן $\frac ba=\frac32$."),
     NU(r"בהצבת $b=\frac32a$, התוחלת היא $\frac{23}{24}a$. מהו $a$ כאשר $\mathbb E[X]=\frac{23}{24}$?", 1, r"$a=1$ (ואז $b=\frac32$, $c=1$).")])

ADD(4, "ב",
    RB((r"הצבת הפרמטרים: $f(x)=x$ על $(0,1)$, $1$ על $(1,\frac32)$", 2), (r"$F(t)=\frac{t^2}{2}$ על $[0,1)$ ו-$t-\frac12$ על $[1,\frac32)$", 6), (r"ערכי הקצה והרציפות ב-$t=1$ ושרטוט", 2)),
    [r"לשכוח את הקבוע $-\frac12$ בקטע השני", r"לא לציין $F=0$ ו-$F=1$ בקצוות"],
    [NU(r"מהו $F_X(1)$? (סוף הקטע הפרבולי)", Fr(1, 2), r"$\frac{1^2}{2}=\frac12$."),
     NU(r"מהו $F_X(\frac12)$?", Fr(1, 8), r"$\frac{(1/2)^2}{2}=\frac18$."),
     NU(r"מהו $F_X(\frac54)$? (הקטע $1\le t<\frac32$)", Fr(3, 4), r"$t-\frac12=\frac34$.")])

ADD(4, "ג",
    RB((r"$\mathbb E[X]=\frac{23}{24}$ מסעיף א", 1), (r"בחירת הענף של $F_X$: $\frac{23}{24}<1$ ולכן $\frac{t^2}{2}$", 2), (r"$P(X>\mathbb E[X])=1-F_X\left(\frac{23}{24}\right)\approx0.541$", 2)),
    [r"להציב בענף $t-\frac12$ (שמתאים ל-$t\ge1$)", r"לשכוח להחסיר מ-$1$"],
    [CH(r"באיזה ענף של $F_X$ נמצא $t=\frac{23}{24}$?",
        [r"$\frac{t^2}{2}$, כי $0\le t<1$", r"$t-\frac12$, כי $t<\frac32$", r"$1$, כי $t$ קרוב ל-$1$"], 0,
        r"הענף $t-\frac12$ מתחיל רק ב-$t=1$. הצבה שגויה ב-$t-\frac12$ נותנת $0.4583$ במקום $0.4592$; ו-$F=1$ מתחיל ב-$t=\frac32$."),
     NU(r"מהו $F_X\left(\frac{23}{24}\right)$?", 0.5 * (23 / 24) ** 2, r"$\frac12\left(\frac{23}{24}\right)^2\approx0.4592$."),
     NU(r"מהי $P(X>\mathbb E[X])$?", 1 - 0.5 * (23 / 24) ** 2, r"$1-0.4592\approx0.5408$.")])

# ---- Q5: attendance and birthday (symbolic in N, p, Q): numeric checks at N=5, p=0.6, Q=1/365
ADD(5, "א",
    RB((r"זיהוי $N$ ניסויי ברנולי בלתי תלויים עם אותה הצלחה $p$", 2), (r"$X\sim\mathrm{Bin}(N,p)$ ופונקציית ההסתברות", 1)),
    [r"להגיד פואסון או גאומטרית בלי נימוק", r"לשכוח את תנאי אי-התלות"],
    [CH(r"כל אחד מ-$N$ התלמידים מגיע בהסתברות $p$, ללא תלות באחרים. איך מפולג מספר המגיעים $X$?",
        [r"$\mathrm{Bin}(N,p)$: $N$ ניסויים בלתי תלויים עם אותה הסתברות הצלחה", r"גאומטרית: ממתינים להגעה הראשונה", r"פואסון: מספר מקרים בלי חסם עליון"], 0,
        r"מספר קבוע של ניסויים בלתי תלויים נותן בינומית. גאומטרית סופרת ניסויים עד הצלחה ראשונה, ופואסון אינו חסום, בעוד ש-$X\le N$."),
     NU(r"מהי $P(X=3)$ כאשר $N=5$ ו-$p=0.6$?", Fr(432, 1250), r"$\binom53(0.6)^3(0.4)^2=10\cdot0.216\cdot0.16=0.3456$.")])

ADD(5, "ב",
    RB((r"בחירת שיטה: הסתברות שלמה לפי $X$ או ספירה ישירה של ״הגיע וגם נולד״", 3), (r"הסתברות ההצלחה לתלמיד: $pQ$ (לא $Q$)", 4), (r"שימוש בנוסחה ברמז / הצגה כסכום ברנולי בלתי תלויים", 5), (r"התשובה $Y\sim\mathrm{Bin}(N,pQ)$", 4)),
    [r"לכתוב $Y\sim\mathrm{Bin}(N,Q)$ ולשכוח שהסופרים רק את מי שהגיע", r"לשכוח שהנוסחה ברמז דורשת $a=\frac{p(1-Q)}{1-p}$"],
    [CH(r"$Y$ סופר את התלמידים שהגיעו **וגם** נולדו ב-1 בספטמבר. איך מפולג $Y$?",
        [r"$\mathrm{Bin}(N,pQ)$: כל תלמיד ״הגיע וגם נולד״ בהסתברות $pQ$, בלתי תלוי באחרים", r"$\mathrm{Bin}(N,Q)$: כל תלמיד נולד בהסתברות $Q$", r"$\mathrm{Bin}(N,p+Q)$: חיבור ההסתברויות"], 0,
        r"תלמיד נספר רק אם מתקיימים שני תנאים בלתי תלויים, ולכן המכפלה $pQ$. אם היה $\mathrm{Bin}(N,Q)$ אז $P(Y=N)=Q^N$ במקום $(pQ)^N$, ו-$p+Q$ אינו מתאים (יכול לעבור $1$)."),
     NU(r"מהי ההסתברות $pQ$ שתלמיד מסוים גם הגיע וגם נולד בתאריך, כאשר $p=0.6$ ו-$Q=\frac1{365}$?", _pq, r"$pQ=\frac{0.6}{365}\approx0.0016438$."),
     NU(r"מהי $P(Y=0)$ כאשר $N=5$, $p=0.6$, $Q=\frac1{365}$?", (1 - _pq) ** 5, r"$(1-pQ)^5=\left(1-\frac{0.6}{365}\right)^5\approx0.99181$."),
     NU(r"מהי $P(Y=1)$ באותם ערכים?", _pY(1), r"$5\,pQ\,(1-pQ)^4\approx0.0081653$.")])

ADD(5, "ג",
    RB((r"נוסחת בייס: $\frac{P(Y=k\mid X=n)P(X=n)}{P(Y=k)}$", 2), (r"שימוש ב-$P(Y=k)$ מסעיף ב ובבינומית ב-$P(Y=k\mid X=n)$", 2), (r"התשובה $\binom{N-k}{N-n}\tilde p^{N-n}(1-\tilde p)^{n-k}$ עם $\tilde p=\frac{1-p}{1-pQ}$", 2)),
    [r"לחלק ב-$P(X=n)$ במקום ב-$P(Y=k)$", r"לא לצמצם נכון את המקדמים הבינומיים"],
    [CH(r"נתון $Y=k$ ומחפשים את התפלגות $X$. איזו נוסחה נכונה?",
        [r"נוסחת בייס: $P(X=n\mid Y=k)=\frac{P(Y=k\mid X=n)\,P(X=n)}{P(Y=k)}$", r"$P(X=n\mid Y=k)=P(Y=k\mid X=n)$", r"$P(X=n\mid Y=k)=P(X=n)$, כי $X$ ו-$Y$ בלתי תלויים"], 0,
        r"$Y$ סופר חלק מהמגיעים ולכן תלוי ב-$X$. עבור $N=5$, $n=2$, $k=1$ האפשרות השנייה נותנת $0.0055$ (זו $P(Y=1\mid X=2)$, התנאי ההפוך) והשלישית נותנת $0.2304$, בעוד שהנכון הוא $0.1542$."),
     NU(r"מהי $P(Y=1)$ כאשר $N=5$, $p=0.6$, $Q=\frac1{365}$? (המכנה)", _pY(1), r"$5\,pQ\,(1-pQ)^4\approx0.0081653$."),
     NU(r"מהי $P(X=2\cap Y=1)=P(Y=1\mid X=2)\,P(X=2)$ באותם ערכים?", 2 / 365 * (364 / 365) * 0.2304, r"$2Q(1-Q)\cdot0.2304\approx0.0012590$."),
     NU(r"מהי $P(X=2\mid Y=1)$?", _c, r"היחס $\frac{0.0012590}{0.0081653}\approx0.1542=\binom43\tilde p^3(1-\tilde p)$ עם $\tilde p=\frac{0.4}{1-pQ}$.")])

# ---- Q6: bridge circuits Q1 (middle unit E) and Q2 (middle unit A); numeric checks at p=0.6
ADD(6, "א",
    RB((r"פיצול לפי היחידה האמצעית $E$", 1), (r"$E$ פועל: $(2p-p^2)^2$; $E$ אינו פועל: $2p^2-p^4$", 1), (r"הצבה ופישוט", 1)),
    [r"להתעלם מהיחידה האמצעית"],
    [CH(r"איך מחשבים את $P(Q_1)$ במעגל הגשר?",
        [r"מפצלים לפי $E$: כש-$E$ פועל המעגל הוא $(A\cup C)\cap(B\cup D)$, וכשאינו פועל $(AB)\cup(CD)$", r"מניחים שהמעגל הוא $(AB)\cup(CD)$ ומתעלמים מ-$E$", r"כל חמשת הרכיבים בטור: $p^5$"], 0,
        r"ל-$E$ יש תפקיד. ב-$p=0.6$ התעלמות מ-$E$ נותנת $0.5904$ (קטן מהנכון $0.65952$) וטור נותן $0.07776$."),
     NU(r"מהי $P(Q_1\mid E\ \text{works})$ כאשר $p=0.6$?", (2 * _p6 - _p6 ** 2) ** 2, r"$(2p-p^2)^2=0.84^2=0.7056$."),
     NU(r"מהי $P(Q_1\mid E\ \text{fails})$ באותו $p$?", 2 * _p6 ** 2 - _p6 ** 4, r"$2p^2-p^4=0.5904$."),
     NU(r"מהי $P(Q_1)$?", _PQ1, r"$0.6\cdot0.7056+0.4\cdot0.5904=0.65952$.")])

ADD(6, "ב",
    RB((r"הגדרת הסתברות מותנית $\frac{P(Q_1\cap Q_2)}{P(Q_1)}$", 4), (r"חישוב $P(Q_1\cap Q_2)$ בהתניה על $A,E$ (ארבעה מקרים), או על $A$ בלבד", 8), (r"הצבה ופישוט ל-$\frac{1+4p-6p^2+2p^3}{2+2p-5p^2+2p^3}$", 4)),
    [r"להניח ש-$Q_1,Q_2$ בלתי תלויים ולכפול", r"לטעות בצמצום המעגל המשותף כש-$A$ ו-$E$ פועלים"],
    [CH(r"איך מחשבים את $P(Q_1\cap Q_2)$?",
        [r"בהסתברות שלמה לפי $A,E$, כי שני המעגלים משתמשים באותם רכיבים", r"כמכפלה $P(Q_1)\cdot P(Q_2)$", r"כסכום $P(Q_1)+P(Q_2)$"], 0,
        r"המעגלים תלויים כי הם חולקים רכיבים. ב-$p=0.6$ המכפלה נותנת $0.4350$ במקום $0.60192$, והסכום עולה על $1$."),
     NU(r"מהי $P(Q_1)$ כאשר $p=0.6$? (המכנה: אירוע התנאי)", _PQ1, r"$0.65952$ מסעיף א."),
     NU(r"כש-$A$ ו-$E$ פועלים, שני המעגלים פועלים אם $B\cup D$ פועל. מהי ההסתברות לכך כש-$p=0.6$?", 2 * _p6 - _p6 ** 2, r"$1-0.4^2=0.84$."),
     NU(r"מהי $P(Q_1\cap Q_2)$ באותו $p$? (המונה)", _PI, r"$p^2(1+4p-6p^2+2p^3)=0.36\cdot1.672=0.60192$."),
     NU(r"מהי $P(Q_2\mid Q_1)$?", _PI / _PQ1, r"$\frac{0.60192}{0.65952}\approx0.91266$.")])

ADD(6, "ג",
    RB((r"הכלה והפרדה: $P(Q_1\cup Q_2)=P(Q_1)+P(Q_2)-P(Q_1\cap Q_2)$", 3), (r"$P(Q_1)=P(Q_2)$ (סימטריה) ו-$P(Q_1\cap Q_2)$ מסעיף ב", 2), (r"התשובה $p^2(3-4p^2+2p^3)$", 1)),
    [r"לחבר $P(Q_1)+P(Q_2)$ בלי להחסיר את החיתוך"],
    [CH(r"איך מחשבים את $P(Q_1\cup Q_2)$?",
        [r"$P(Q_1)+P(Q_2)-P(Q_1\cap Q_2)$", r"$P(Q_1)+P(Q_2)$", r"$P(Q_1)\cdot P(Q_2)$"], 0,
        r"המעגלים אינם זרים ולא בלתי תלויים. הסכום נותן $1.319>1$ והמכפלה נותנת $0.435$ (זו ההסתברות לחיתוך אם היו תלויים באופן מלאכותי), בעוד האיחוד $0.71712$."),
     NU(r"מהי $P(Q_1)+P(Q_2)$ כאשר $p=0.6$?", 2 * _PQ1, r"$2\cdot0.65952=1.31904$."),
     NU(r"מהי $P(Q_1\cap Q_2)$ באותו $p$?", _PI, r"$0.60192$ מסעיף ב."),
     NU(r"מהי $P(Q_1\cup Q_2)$?", _PU, r"$1.31904-0.60192=0.71712$.")])

APPLY(questions)


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
