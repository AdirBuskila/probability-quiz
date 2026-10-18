# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-B.json -- probability (course 20021), semester B 2024, moed B (06.08.2024).
6 questions, 22 items (Q1 5, Q2 4, Q3 4, Q4 3, Q5 3, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-B.py

Source: exam pp.1-3, handwritten official solutions pp.4-16 (grid paper).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, a-3, b-1, b-2, stored as a b c d e (the printed label is the
  first bold token of each question text). Map: Q1 a=א-1, b=א-2, c=א-3, d=ב-1, e=ב-2;
  Q6 a=א, b=ב-1, c=ב-2.
- Q1 area items (b, c) have region data in tools/verify/24B-B/regions.json (no `region` field in RAW_SCHEMA).
- Q3(ד) TYPO RULING (arbiter 2026-10-18, the printed question wins): the official solution gives 20/36 = 5/9 for
  P(number even | digit sum odd). "Digit sum odd" has 40 ordered pairs (5 odd digits x 4 even, in both orders),
  20 of them with an even units digit, so the exact value is 1/2. Shipped 1/2 with the official method and the
  denominator corrected, solutionSource "solved", official:false, "הפתרון הרשמי עם תיקון" prefix; verified exactly
  and by Monte Carlo in tools/verify/24B-B/check.py.
- Q5: the official solution takes Q = 1/365 (probability that a student has a birthday on 1 September); the
  question text itself does not state it. Q5(ג) is stated in the official solution with p~ = (1-p)/(1-pQ).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-B.json"
CODE = "24B-B"
IMG = "images/exams/24B-B-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_LEAD = r"נתבונן בשני גפרורים שאורכם מהווים משתנים מקריים בלתי תלויים $X_1\sim U_c(0,L)$ ו-$X_2\sim U_c(0,2L)$."
Q1_B = (r"בוחרים בגפרור באופן הבא: מטילים מטבע מוטה (בעל סיכוי $p$ לקבלת תוצאת ״עץ״). אם התקבל ״עץ״, בוחרים בגפרור שאורכו $X_1$; "
        r"אחרת בוחרים בגפרור שאורכו $X_2$. יהי $Y$ אורך של הגפרור שנבחר.")

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א-1:** חשבו את ההסתברות $P(X_1<L/5)$.",
    r"""$X_1\sim U_c(0,L)$, ולכן
$$P(X_1<L/5)=\frac{L/5}{L}=\frac15.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**א-2:** חשבו את ההסתברות $P(X_1+X_2>L)$.",
    r"""נשתמש בגישה הקלאסית. מרחב המדגם הוא המלבן $\Omega=\{0<x_1<L,\ 0<x_2<2L\}$, ושטחו $|\Omega|=2L^2$.
האירוע $\{X_2>L-X_1\}$ הוא החלק של המלבן שמעל הישר $x_2=L-x_1$. השטח שמתחת לישר (משולש שניצביו $L$) הוא $\frac12L^2$, ולכן
$$|\{X_2>L-X_1\}|=2L^2-\frac12L^2=\frac32L^2.$$
מכאן
$$P(X_1+X_2>L)=\frac{\frac32L^2}{2L^2}=\frac34.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**א-3:** חשבו את ההסתברות $P(X_1>X_2)$.",
    r"""נשתמש בגישה הקלאסית, עם $|\Omega|=2L^2$. האירוע $\{X_2<X_1\}$ הוא המשולש שמתחת לאלכסון $x_2=x_1$ בתוך המלבן, ושטחו $\frac{L^2}{2}$. לכן
$$P(X_1>X_2)=\frac{L^2/2}{2L^2}=\frac14.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ד", "conditional_bayes",
    Q1_B + "\n" + r"**ב-1:** חשבו את ההסתברות $P(Y<L)$.",
    r"""אורך הגפרור שנבחר הוא
$$Y=\begin{cases}X_1,&\text{with probability }p,\\X_2,&\text{with probability }1-p.\end{cases}$$
נסמן ב-$H$ את ״עץ״ וב-$T$ את ״פלי״. לפי נוסחת ההסתברות השלמה:
$$P(Y<L)=P(Y<L\mid H)P(H)+P(Y<L\mid T)P(T)=P(X_1<L)\,p+P(X_2<L)(1-p).$$
כאן $P(X_1<L)=1$ ו-$P(X_2<L)=\frac12$, ולכן
$$P(Y<L)=p+\frac12(1-p)=\frac{1+p}{2}.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ה", "conditional_bayes",
    Q1_B + "\n" + r"**ב-2:** חשבו את ההסתברות $P(L/2<Y<3L/2)$.",
    r"""שוב לפי נוסחת ההסתברות השלמה:
$$P(\tfrac L2<Y<\tfrac{3L}2)=P(\tfrac L2<Y<\tfrac{3L}2\mid H)\,p+P(\tfrac L2<Y<\tfrac{3L}2\mid T)(1-p).$$
בהינתן $H$: $Y=X_1$, ו-$P(\frac L2<X_1<\frac{3L}2)=\frac{L/2}{L}=\frac12$ (הקטע החופף ל-$(0,L)$ הוא $(\frac L2,L)$).
בהינתן $T$: $Y=X_2$, ו-$P(\frac L2<X_2<\frac{3L}2)=\frac{L}{2L}=\frac12$.
לכן
$$P(\tfrac L2<Y<\tfrac{3L}2)=\frac12p+\frac12(1-p)=\frac12.$$""",
    5, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_LEAD = r"בכד נמצאים $D$ כדורים אדומים ו-$(N-D)$ כדורים שחורים."
Q2_NOTE = "\n" r"עליך לפשט את התשובה עד כמה שניתן."

questions.append(Q(
    2, "א", "combinatorics",
    r"מוציאים מהכד כדור אחד. מהי ההסתברות שצבעו אדום?",
    r"""$$P(R_1)=\frac DN.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ב", "conditional_bayes",
    r"מוציאים מהכד שני כדורים ללא החזרה. מהי ההסתברות שהכדור השני הוא כדור אדום? עליך לפשט את התשובה עד כמה שניתן.",
    r"""נסמן ב-$R_i$ ($B_i$) את המאורע שהכדור ה-$i$ אדום (שחור). לפי הצבע של הכדור הראשון:
$$P(R_2)=P(R_1\cap R_2)+P(B_1\cap R_2)=\frac DN\cdot\frac{D-1}{N-1}+\frac{N-D}{N}\cdot\frac{D}{N-1}.$$
$$=\frac{D}{N(N-1)}\bigl\{D-1+N-D\bigr\}=\frac DN.$$""",
    7, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"מוציאים מהכד שלושה כדורים ללא החזרה. מהי ההסתברות שהכדור השלישי הוא כדור אדום? עליך לפשט את התשובה עד כמה שניתן.",
    r"""נפצל לפי הצבעים של שני הכדורים הראשונים (ארבעה מקרים זרים):
$$P(R_3)=P(R_1R_2R_3)+P(R_1B_2R_3)+P(B_1R_2R_3)+P(B_1B_2R_3).$$
$$P(R_1R_2R_3)=\frac DN\cdot\frac{D-1}{N-1}\cdot\frac{D-2}{N-2},\qquad P(R_1B_2R_3)=\frac DN\cdot\frac{N-D}{N-1}\cdot\frac{D-1}{N-2}.$$
סכומם:
$$\frac{D(D-1)}{N(N-1)(N-2)}\bigl\{D-2+N-D\bigr\}=\frac{D(D-1)}{N(N-1)}.$$
$$P(B_1R_2R_3)=\frac{N-D}{N}\cdot\frac{D}{N-1}\cdot\frac{D-1}{N-2},\qquad P(B_1B_2R_3)=\frac{N-D}{N}\cdot\frac{N-D-1}{N-1}\cdot\frac{D}{N-2}.$$
סכומם:
$$\frac{D(N-D)}{N(N-1)(N-2)}\bigl\{D-1+N-D-1\bigr\}=\frac{D(N-D)}{N(N-1)}.$$
בסך הכול
$$P(R_3)=\frac{D(D-1)}{N(N-1)}+\frac{D(N-D)}{N(N-1)}=\frac{D}{N(N-1)}\bigl\{D-1+N-D\bigr\}=\frac DN.$$""",
    7, contextId="c2"))

questions.append(Q(
    2, "ד", "conditional_bayes",
    r"מוציאים מהכד שלושה כדורים ללא החזרה. אם ידוע כי הכדור השני הוא אדום, מהי ההסתברות שהכדור השלישי אדום גם כן? עליך לפשט את התשובה עד כמה שניתן.",
    r"""$$P(R_3\mid R_2)=\frac{P(R_2\cap R_3)}{P(R_2)},\qquad P(R_2)=\frac DN.$$
(הערך $P(R_2)=\frac DN$ חושב בסעיף ב.)
נפצל את $R_2\cap R_3$ לפי הכדור הראשון:
$$P(R_2R_3)=P(R_1R_2R_3)+P(B_1R_2R_3)=\frac DN\cdot\frac{D-1}{N-1}\cdot\frac{D-2}{N-2}+\frac{N-D}{N}\cdot\frac{D}{N-1}\cdot\frac{D-1}{N-2}$$
$$=\frac{D(D-1)}{N(N-1)(N-2)}\bigl\{D-2+N-D\bigr\}=\frac{D(D-1)}{N(N-1)}.$$
לכן
$$P(R_3\mid R_2)=\frac{\frac{D(D-1)}{N(N-1)}}{\frac DN}=\frac{D-1}{N-1}.$$""",
    6, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_LEAD = (r"מרכיבים מספר דו ספרתי באופן הבא: מאוסף הספרות $\{1,2,3,4,5,6,7,8,9\}$ מוציאים באקראי **וללא החזרה** שתי ספרות. "
           r"הספרה הראשונה שנבחרה הינה ספרת העשרות של המספר; הספרה השנייה שנבחרה הינה ספרת האחדות.")
Q3_X = r"נסמן ב-$X$ את ספרת העשרות וב-$Y$ את ספרת האחדות. מרחב המדגם: $|\Omega|=9\cdot8=72$ זוגות סדורים." + "\n"

questions.append(Q(
    3, "א", "combinatorics",
    r"מהי ההסתברות שמספר שהורכב הינו מספר זוגי?",
    Q3_X + r"""המספר זוגי אם ורק אם ספרת האחדות $Y$ זוגית: ארבע אפשרויות ל-$Y$ ($2,4,6,8$) ולכל אחת שמונה אפשרויות ל-$X$ (ללא החזרה). לכן
$$P(\text{even})=\frac{|\{\cdots\}|}{|\Omega|}=\frac{32}{72}=\frac49.$$""",
    7, contextId="c3"))

questions.append(Q(
    3, "ב", "combinatorics",
    r"מהי ההסתברות שמספר שהורכב מתחלק ב-3 ללא שארית?",
    Q3_X + r"""מספר מתחלק ב-3 אם ורק אם סכום ספרותיו מתחלק ב-3, כלומר $X+Y\equiv0\pmod 3$. בין הספרות $1,\ldots,9$ יש שלוש ספרות מכל שארית (0, 1, 2) מודולו 3. מספר הזוגות הסדורים:
- שתיהן בשארית 0: $3\cdot2=6$;
- שארית 1 ושארית 2, או להפך: $2\cdot(3\cdot3)=18$.

סך הכול $24=2\cdot12$, ולכן
$$P(\div3)=\frac{24}{72}=\frac13.$$""",
    7, contextId="c3"))

questions.append(Q(
    3, "ג", "combinatorics",
    r"מהי ההסתברות שמספר שהורכב מתחלק ב-5 ללא שארית?",
    Q3_X + r"""המספר מתחלק ב-5 אם ורק אם ספרת האחדות היא $5$ (ספרת האחדות לא יכולה להיות $0$ באוסף). אז לספרת העשרות יש $8$ אפשרויות:
$$P(\div5)=\frac{8}{72}=\frac19.$$""",
    7, contextId="c3"))

questions.append(Q(
    3, "ד", "conditional_bayes",
    r"אם ידוע כי סכום הספרות מהווה מספר אי זוגי, מהי ההסתברות שמספר עצמו הוא כן זוגי?",
    r"""**הפתרון הרשמי עם תיקון:** בפתרון הרשמי המכנה הוא $36$ והתשובה $\frac{20}{36}=\frac59$. אבל יש $40$ זוגות סדורים שסכום ספרותיהם אי-זוגי, ולכן המכנה הנכון הוא $40$ והתשובה $\frac12$. התיקון נבדק (ספירה מדויקת וסימולציה).
""" + Q3_X + r"""לפי הגדרת ההסתברות המותנית:
$$P(\text{number even}\mid X+Y\text{ odd})=\frac{P(\text{number even}\cap X+Y\text{ odd})}{P(X+Y\text{ odd})}=\frac{|\{\text{number even}\cap X+Y\text{ odd}\}|}{|\{X+Y\text{ odd}\}|}.$$
סכום הספרות אי-זוגי אם ורק אם ספרה אחת אי-זוגית (5 אפשרויות) והאחרת זוגית (4 אפשרויות), בשני הסדרים: $|\{X+Y\text{ odd}\}|=2\cdot5\cdot4=40$.
המספר זוגי כאשר בנוסף ספרת האחדות $Y$ זוגית, כלומר $X$ אי-זוגית ו-$Y$ זוגית: $5\cdot4=20$ זוגות. לכן
$$P(\text{number even}\mid X+Y\text{ odd})=\frac{20}{40}=\frac12.$$""",
    4, contextId="c3", solutionSource="solved", official=False))

# ------------------------------------------------------------------ Q4
Q4_LEAD = r"לפניכם גרף עבור פונקציית צפיפות ההסתברות $f_Z(z)$ של משתנה מקרי $Z$."

questions.append(Q(
    4, "א", "continuous_rv",
    r"**א:** בהנחה כי $\mathbb{E}[Z]=4/9$, מצאו את הפרמטרים $a$ ו-$b$.",
    r"""**נרמול.** שטח הצפיפות הוא 1: משולש בשטח $a\cdot1=a$ ומלבן ברוחב $b-a$ וגובה 1:
$$a+(b-a)=1\ \Longrightarrow\ b=1.$$
**תוחלת.** הצפיפות על $(-a,a)$ זוגית, ולכן האינטגרל של $z f_Z(z)$ על $(-a,a)$ הוא $0$ (פונקציה אי-זוגית על קטע סימטרי). נשאר
$$\mathbb{E}[Z]=\int_a^bz\cdot1\,dz=\frac{b^2-a^2}{2}=\frac{1-a^2}{2}=\frac49\ \Longrightarrow\ a^2=\frac19\ \Longrightarrow\ a=\frac13.$$
תשובה: $a=\frac13,\ b=1$.""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"**ב:** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_Z(t)$ ושרטטו את התוצאה.",
    r"""עם $a=\frac13$, $b=1$ הצפיפות היא $3z+1$ על $(-\frac13,0)$, $1-3z$ על $(0,\frac13)$ ו-$1$ על $(\frac13,1)$. אינטגרציה לכל $t$ נותנת
$$F_Z(t)=P(Z\le t)=\begin{cases}0,&t<-\frac13,\\ \dfrac{(1+3t)^2}{6},&-\frac13\le t<0,\\ \dfrac13-\dfrac{(1-3t)^2}{6},&0\le t<\frac13,\\ t,&\frac13\le t<1,\\ 1,&t\ge1.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת F_Z(t)](images/exams/24B-B-Q4-cdf.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"**ג:** מהי ההסתברות המותנית $P(Z>1/4\ /\ |Z|<3/4)$?",
    r"""$$P\left(Z>\tfrac14\ \Big|\ |Z|<\tfrac34\right)=\frac{P(\frac14<Z<\frac34)}{P(-\frac34<Z<\frac34)}=\frac{F_Z(\frac34)-F_Z(\frac14)}{F_Z(\frac34)-F_Z(-\frac34)}.$$
$F_Z(\frac34)=\frac34$, $F_Z(-\frac34)=0$ ו-$F_Z(\frac14)=\frac13-\frac16\left(1-\frac34\right)^2=\frac{31}{96}$. לכן
$$=1-\frac43\cdot\frac{31}{96}=\frac{41}{72}.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_LEAD = (r"בכיתת ״מופת״ רשומים $N$ תלמידים. ביום פתיחת שנת הלימודים, 1 בספטמבר, בגלל סיבות שונות ומשונות, כל אחד מהתלמידים "
           r"מחליט להגיע ללימודים בהסתברות $p$.")
Q5_HINT = (r"**הערה:** לידיעתך,"
           "\n" r"$$\sum_{j=m}^{N}C_j^mC_N^ja^j=C_N^ma^m(1+a)^{N-m}$$"
           "\n" r"(ייתכן ואין צורך להשתמש בנוסחה זו).")

questions.append(Q(
    5, "א", "special_discrete",
    r"**א:** יהי $X$ משתנה מקרי המתאר את מספר התלמידים אשר כן הגיעו לכיתה. איך משתנה זה מפולג? **עליך לתת הסבר מפורט.**",
    r"""כל אחד מ-$N$ התלמידים מחליט באופן בלתי תלוי להגיע בהסתברות $p$, ולכן $X$ סופר את מספר ההצלחות ב-$N$ ניסויי ברנולי בלתי תלויים ובעלי אותה הסתברות הצלחה. לכן
$$X\sim\mathrm{Bin}(N,p),\qquad P(X=k)=\binom Nkp^k(1-p)^{N-k},\quad k=0,1,\ldots,N.$$""",
    3, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    r"**ב:** יהי $Y$ משתנה מקרי המתאר את מספר התלמידים **מתוך אלה שהגיעו לכיתה** – אשר נולדו **ב-1 בספטמבר**. מצאו את פונקציית ההסתברות של משתנה זה." "\n" + Q5_HINT,
    r"""נסמן ב-$Q=\frac1{365}$ את ההסתברות שתלמיד נולד ב-1 בספטמבר. $Y$ יכול לקבל ערכים $k=0,1,\ldots,N$. לפי נוסחת ההסתברות השלמה לפי $X$ (בהינתן $X=j$ התלמידים שהגיעו הם $j$, וכל אחד נולד באותו תאריך בהסתברות $Q$):
$$P(Y=k)=\sum_{j=k}^{N}P(Y=k\mid X=j)P(X=j)=\sum_{j=k}^{N}\binom jkQ^k(1-Q)^{j-k}\binom Njp^j(1-p)^{N-j}$$
$$=\frac{Q^k}{(1-Q)^k}(1-p)^N\sum_{j=k}^{N}\binom jk\binom Nj\left\{\frac{p(1-Q)}{1-p}\right\}^j.$$
נשתמש בנוסחה שבהערה עם $m=k$ ו-$a=\frac{p(1-Q)}{1-p}$. אז $1+a=\frac{1-pQ}{1-p}$ ומתקבל
$$\sum_{j=k}^{N}\binom jk\binom Nj a^j=\binom Nka^k(1+a)^{N-k}=\binom Nk\frac{p^k(1-Q)^k}{(1-p)^k}\cdot\frac{(1-pQ)^{N-k}}{(1-p)^{N-k}}=\binom Nk\frac{p^k(1-Q)^k}{(1-p)^N}(1-pQ)^{N-k}.$$
הצבה חזרה:
$$P(Y=k)=\binom Nk(pQ)^k(1-pQ)^{N-k},\qquad k=0,1,\ldots,N.$$
במילים אחרות, $Y\sim\mathrm{Bin}(N,pQ)$: כל תלמיד מגיע **וגם** נולד ב-1 בספטמבר בהסתברות $pQ$.""",
    16, contextId="c5"))

questions.append(Q(
    5, "ג", "conditional_bayes",
    r"**ג:** אם ידוע כי בין כל התלמידים אשר הגיעו לכיתה בדיוק $k$ נולדו ב-1 בספטמבר, מהי ההסתברות שבדיוק $n$ תלמידים הגיעו לכיתה?",
    r"""לפי נוסחת בייס:
$$P(X=n\mid Y=k)=\frac{P(Y=k\mid X=n)P(X=n)}{P(Y=k)}=\frac{\binom nkQ^k(1-Q)^{n-k}\cdot\binom Nnp^n(1-p)^{N-n}}{\binom Nk(pQ)^k(1-pQ)^{N-k}}.$$
מהזהות $\binom nk\binom Nn=\binom Nk\binom{N-k}{n-k}$ ומצמצום מתקבל
$$P(X=n\mid Y=k)=\binom{N-k}{N-n}\tilde p^{\,N-n}(1-\tilde p)^{(N-k)-(N-n)},\qquad \tilde p=\frac{1-p}{1-pQ}.$$
כלומר, בהינתן $Y=k$, מספר התלמידים שלא הגיעו מבין $N-k$ התלמידים שנותרו הוא $\mathrm{Bin}(N-k,\tilde p)$.""",
    6, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_LEAD = (r"סטודנט של המכון הטכנולוגי חולון הרכיב מעגל חשמלי $\boldsymbol{Q}_1$ מחמש יחידות $A$, $B$, $C$, $D$ ו-$E$ "
           r"הפועלות ללא תלות אחת בשנייה בהסתברויות זהות $p$. "
           r"**המעגל $\boldsymbol{Q}_1$ (גשר):** $A$ ו-$B$ בענף העליון בטור, $C$ ו-$D$ בענף התחתון בטור, ו-$E$ מחבר את הצומת שבין $A$ ל-$B$ לצומת שבין $C$ ל-$D$. "
           r"לאחר פירוק של מעגל $\boldsymbol{Q}_1$, הסטודנט הרכיב מעגל חדש $\boldsymbol{Q}_2$ **מאותן יחידות**: "
           r"$A$ ו-$B$ במקביל, בטור עם $C$, $D$ ו-$E$ במקביל.")

questions.append(Q(
    6, "א", "circuits",
    r"**א:** מהי ההסתברות שמעגל $\boldsymbol{Q}_1$ פעל?",
    r"""נפצל לפי הרכיב $E$ (הגשר). אם $E$ פועל, המעגל פועל אם ($A$ או $C$ פועל) **וגם** ($B$ או $D$ פועל): הסתברות $(2p-p^2)^2$. אם $E$ אינו פועל, המעגל הוא ($A$ בטור $B$) במקביל ל-($C$ בטור $D$): הסתברות $2p^2-p^4$. לכן
$$P(Q_1)=(2p-p^2)^2\,p+(2p^2-p^4)(1-p)=p^2\,(2+2p-5p^2+2p^3).$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"**ב-1:** מהי ההסתברות שמעגל $\boldsymbol{Q}_2$ יפעל?",
    r"""$Q_2$ הוא טור של שני מקבצים בלתי תלויים: $(A\cup B)$ ו-$(C\cup D\cup E)$. לכן
$$P(Q_2)=(2p-p^2)\bigl[1-(1-p)^3\bigr]=6p^2-9p^3+5p^4-p^5.$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    r"**ב-2:** אם ידוע שמעגל $\boldsymbol{Q}_2$ פעל, מהי ההסתברות שגם המעגל המקורי $\boldsymbol{Q}_1$ פעל?",
    r"""$$P(Q_1\mid Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}.$$
המעגל $\tilde Q=Q_1\cap Q_2$ משתמש באותן יחידות. נחשב את $P(Q_1\cap Q_2)$ בהסתברות שלמה לפי $A,B$:
- $A\cap B$ (הסתברות $p^2$): $Q_1$ פועל בוודאי (הענף העליון שלם) ו-$Q_2$ פועל אם $C\cup D\cup E$ פועל: $1-(1-p)^3$.
- $\bar A\cap\bar B$ (הסתברות $(1-p)^2$): $Q_2$ נכשל, ההסתברות $0$.
- $A\cap\bar B$ (הסתברות $p(1-p)$): $Q_1$ פועל אם $D$ פועל וגם $C$ או $E$ פועל; זה גם מבטיח ש-$C\cup D\cup E$ פועל, ולכן $P=p(2p-p^2)$.
- $\bar A\cap B$ (הסתברות $p(1-p)$): באופן דומה $Q_1$ פועל אם $C$ פועל וגם $D$ או $E$ פועל, ולכן $P=p(2p-p^2)$.

לכן
$$P(Q_1\cap Q_2)=p^2\bigl[1-(1-p)^3\bigr]+2p(1-p)\cdot p(2p-p^2)=3p^5-9p^4+7p^3.$$
ומכאן
$$P(Q_1\mid Q_2)=\frac{p\,(7-9p+3p^2)}{6-9p+5p^2-p^3}.$$""",
    7, contextId="c6"))

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר ב׳ תשפ״ד, מועד ב (06.08.2024)",
    "year": 2024,
    "examDate": "06.08.2024",
    "sourceFile": "24B-B exam pp.1-3",
    "solutionFile": "24B-B official handwritten solutions pp.4-16",
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
