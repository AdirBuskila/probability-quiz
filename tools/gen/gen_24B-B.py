# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-B.json -- probability (course 20021), semester B 2024, moed B (06.08.2024).
6 questions, 22 items (Q1 5, Q2 4, Q3 4, Q4 3, Q5 3, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-B.py

Source: exam pp.1-3, handwritten official solutions pp.4-16 (grid paper).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, a-3, b-1, b-2, stored as a b c d e (the printed label is the
  first bold token of each question text). Map: Q1 a=א-1, b=א-2, c=א-3, d=ב-1, e=ב-2;
  Q6 a=א, b=ב-1, c=ב-2.
- Q1 area items (a, b, c) carry a `region` (moved from the old regions.json); every sim is checked by check_sim_specs; steps are verified in tools/verify/24B-B/steps_check.py.
- Q3(ד) TYPO RULING (arbiter 2026-10-18, the printed question wins): the official solution gives 20/36 = 5/9 for
  P(number even | digit sum odd). "Digit sum odd" has 40 ordered pairs (5 odd digits x 4 even, in both orders),
  20 of them with an even units digit, so the exact value is 1/2. Shipped 1/2 with the official method and the
  denominator corrected, solutionSource "solved", official:false, "הפתרון הרשמי עם תיקון" prefix; verified exactly
  and by Monte Carlo in tools/verify/24B-B/check.py.
- Q5: the official solution takes Q = 1/365 (probability that a student has a birthday on 1 September); the
  question text itself does not state it. Q5(ג) is stated in the official solution with p~ = (1-p)/(1-pQ).
"""
import json, pathlib
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from verified import src as _vsrc

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
    r"""נסמן ב-$Q=\frac1{365}$ את ההסתברות שתלמיד נולד ב-1 בספטמבר. זו הנחה שאינה כתובה בשאלה: כל תלמיד נולד באחד מ-$365$ ימי השנה בהסתברות שווה, וללא תלות בשאר. $Y$ יכול לקבל ערכים $k=0,1,\ldots,N$. לפי נוסחת ההסתברות השלמה לפי $X$ (בהינתן $X=j$ התלמידים שהגיעו הם $j$, וכל אחד נולד באותו תאריך בהסתברות $Q$):
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
כלומר, בהינתן $Y=k$, מספר התלמידים שלא הגיעו מבין $N-k$ התלמידים שנותרו הוא $\mathrm{Bin}(N-k,\tilde p)$.
כאן $Q=\frac1{365}$ לפי אותה הנחה כמו בסעיף ב: כל תלמיד נולד בכל אחד מ-$365$ ימי השנה בהסתברות שווה, וללא תלות בשאר.""",
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

# ---- regions (region.js), "simulate it" specs (sim.js) and rubric / pitfalls / guided steps (ai-draft) -----------------
# Regions were moved here from tools/verify/<CODE>/regions.json. Every sim `exact` is the shipped final answer (symbolic
# answers are simulated at a sample value stated in `estimate`). Every expected step value is re-derived independently,
# exactly and by Monte Carlo, in tools/verify/<CODE>/steps_check.py (which reads the generated raw JSON back).
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


# ---- 24B-B specifics: area figures, simulations, steps
S12 = {"x": [0, 1], "y": [0, 2]}
L12 = {"x": "X1/L", "y": "X2/L"}
_pm = 0.3                                   # sample p for the symbolic answers
_mix = [(0, 1, "0.65"), (1, 2, "0.35")]     # density of Y at p=0.3 (L=1): p*1 + (1-p)/2 on (0,1), (1-p)/2 on (1,2)
_urn = dict(counts={"red": 3, "black": 7})  # D=3, N=10
_pq = 0.6 / 365                             # p*Q at p=0.6, Q=1/365
_N5 = 5


def _pY(k):
    from math import comb
    return comb(5, k) * _pq ** k * (1 - _pq) ** (5 - k)


_pt = (1 - 0.6) / (1 - _pq)                 # p-tilde of part c at p=0.6
_ABs = BER(0.6, *["A%d" % i for i in range(1, 6)]) | BER(1 / 365, *["B%d" % i for i in range(1, 6)])
_SA = "+".join("A%d" % i for i in range(1, 6))
_SY = "+".join("A%d*B%d" % (i, i) for i in range(1, 6))
_c = 4 * _pt ** 3 * (1 - _pt)
_pAB = {"A": 0.6, "B": 0.6, "C": 0.6, "D": 0.6, "E": 0.6}
_Q1 = "(A and B) or (C and D) or (E and ((A and D) or (C and B)))"
_Q2 = "(A or B) and (C or D or E)"
_p6 = 0.6
_PQ1 = _p6 ** 2 * (2 + 2 * _p6 - 5 * _p6 ** 2 + 2 * _p6 ** 3)
_PQ2 = (2 * _p6 - _p6 ** 2) * (1 - (1 - _p6) ** 3)
_PI = 3 * _p6 ** 5 - 9 * _p6 ** 4 + 7 * _p6 ** 3

EXTRAS.update({
    (1, "א"): {"region": REG([lin(1, 0, "1/5", "<")], 1 / 5, "האירוע X1<L/5 (יחידות של L)", space=S12, labels=L12), "sim": AREA("P(X1<L/5)", 1 / 5)},
    (1, "ב"): {"region": REG([lin(1, 1, 1, ">")], 3 / 4, "האירוע X1+X2>L (יחידות של L)", space=S12, labels=L12), "sim": AREA("P(X1+X2>L)", 3 / 4)},
    (1, "ג"): {"region": REG([lin(1, -1, 0, ">")], 1 / 4, "האירוע X1>X2 (יחידות של L)", space=S12, labels=L12), "sim": AREA("P(X1>X2)", 1 / 4)},
    (1, "ד"): {"sim": PDF("P(Y<L) ב-p=0.3", 0.65, _mix, "x < 1")},
    (1, "ה"): {"sim": PDF("P(L/2<Y<3L/2) ב-p=0.3", 0.5, _mix, "x > 1/2 and x < 3/2")},
    (2, "א"): {"sim": URN("P(R1) ב-D=3, N=10", 0.3, 1, "red_1", **_urn)},
    (2, "ב"): {"sim": URN("P(R2) ב-D=3, N=10", 0.3, 2, "red_2", **_urn)},
    (2, "ג"): {"sim": URN("P(R3) ב-D=3, N=10", 0.3, 3, "red_3", **_urn)},
    (2, "ד"): {"sim": URN("P(R3 | R2) ב-D=3, N=10", 2 / 9, 3, "red_3", "red_2", **_urn)},
    (3, "א"): {"sim": URN("P(המספר זוגי)", 4 / 9, 2, "v2 % 2 == 0", values=list(range(1, 10)))},
    (3, "ב"): {"sim": URN("P(המספר מתחלק ב-3)", 1 / 3, 2, "(v1 + v2) % 3 == 0", values=list(range(1, 10)))},
    (3, "ג"): {"sim": URN("P(המספר מתחלק ב-5)", 1 / 9, 2, "v2 == 5", values=list(range(1, 10)))},
    (3, "ד"): {"sim": URN("P(המספר זוגי | סכום הספרות אי-זוגי)", 1 / 2, 2, "v2 % 2 == 0", "(v1 + v2) % 2 == 1", values=list(range(1, 10)))},
    (4, "א"): {"sim": PDF("E[Z] ב-a=1/3, b=1", 4 / 9, [("-1/3", 0, "1+3*x"), (0, "1/3", "1-3*x"), ("1/3", 1, "1")], measure="mean", expr="x")},
    (4, "ב"): {"sim": PDF("F_Z(1/6)=P(Z<=1/6)", 7 / 24, [("-1/3", 0, "1+3*x"), (0, "1/3", "1-3*x"), ("1/3", 1, "1")], "x <= 1/6")},
    (4, "ג"): {"sim": PDF("P(Z>1/4 | |Z|<3/4)", 41 / 72, [("-1/3", 0, "1+3*x"), (0, "1/3", "1-3*x"), ("1/3", 1, "1")], "x > 1/4", "abs(x) < 3/4")},
    (5, "א"): {"sim": CUST("P(X=3) ב-N=5, p=0.6", 0.3456, BER(0.6, *["A%d" % i for i in range(1, 6)]), event=_SA + " == 3")},
    (5, "ב"): {"sim": CUST("P(Y=1) ב-N=5, p=0.6, Q=1/365", _pY(1), _ABs, event=_SY + " == 1", trials=400000)},
    (5, "ג"): {"sim": CUST("P(X=2 | Y=1) ב-N=5, p=0.6, Q=1/365", _c, _ABs, event=_SA + " == 2", given=_SY + " == 1", trials=1000000)},
    (6, "א"): {"sim": CIRC("P(Q1) ב-p=0.6", _PQ1, _pAB, _Q1)},
    (6, "ב"): {"sim": CIRC("P(Q2) ב-p=0.6", _PQ2, _pAB, _Q2)},
    (6, "ג"): {"sim": CIRC("P(Q1 | Q2) ב-p=0.6", _PI / _PQ2, _pAB, _Q1, _Q2)},
})

OM = r"נקבע $L=1$ (היחס אינו תלוי ב-$L$). מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X_1,X_2)$, כלומר המלבן $(0,1)\times(0,2)$?"
OM_X = r"המלבן ברוחב $1$ ובגובה $2$ הוא מרחב המדגם, ושטחו $2$. ההסתברות היא שטח האירוע חלקי $2$, לא שטח האירוע בלבד."

ADD(1, "א",
    RB((r"גישה גאומטרית: הסתברות = שטח האירוע חלקי $|\Omega|=2L^2$ (או $F_{X_1}(L/5)$)", 2), (r"האירוע $X_1<\frac L5$ הוא רצועה ברוחב $\frac L5$ לכל גובה המלבן", 2), (r"התשובה $\frac15$", 1)),
    [r"לשכוח את החילוק ב-$|\Omega|=2$ ולכתוב $\frac25$", r"להניח ש-$X_2$ משפיע על האירוע"],
    [NU(OM, 2, OM_X),
     NU(r"מהו שטח האירוע $\{X_1<\frac15\}$ בתוך המלבן?", Fr(2, 5), r"רצועה ברוחב $\frac15$ ובגובה $2$: שטח $\frac25$."),
     NU(r"מהי ההסתברות $P(X_1<\frac L5)$?", Fr(1, 5), r"$\frac{2/5}{2}=\frac15$.")])

ADD(1, "ב",
    RB((r"הגדרת מרחב המדגם כמלבן $|\Omega|=2L^2$", 1), (r"זיהוי האזור שמתחת לישר $x_2=L-x_1$ כמשולש בשטח $\frac12L^2$", 2), (r"שטח האירוע $\frac32L^2$ וחלוקה ב-$|\Omega|$", 1), (r"התשובה $\frac34$", 1)),
    [r"לחשב את שטח המשולש במקום את שטח המשלים", r"לחלק ב-$L^2$ במקום ב-$2L^2$"],
    [NU(OM, 2, OM_X),
     NU(r"מהו שטח המשלים $\{X_1+X_2\le1\}$ בתוך המלבן? (משולש בפינה $(0,0)$)", Fr(1, 2), r"ניצבי המשולש הם $1$ ו-$1$ (הישר חותך את הצירים ב-$(1,0)$ וב-$(0,1)$, שניהם בתוך המלבן): שטח $\frac12$."),
     NU(r"מהו שטח האירוע $\{X_1+X_2>1\}$?", Fr(3, 2), r"$2-\frac12=\frac32$."),
     NU(r"מהי $P(X_1+X_2>L)$?", Fr(3, 4), r"$\frac{3/2}{2}=\frac34$.")])

ADD(1, "ג",
    RB((r"מרחב המדגם כמלבן, $|\Omega|=2L^2$", 1), (r"האירוע $X_2<X_1$ הוא המשולש שמתחת לאלכסון $x_2=x_1$ (לא מעליו, והמלבן גבוה יותר מרוחבו)", 2), (r"שטח המשולש $\frac{L^2}2$ והתשובה $\frac14$", 2)),
    [r"לקחת את חצי המלבן ולכתוב $\frac12$ (המלבן אינו ריבוע)", r"לחלק ב-$L^2$ במקום ב-$2L^2$"],
    [NU(OM, 2, OM_X),
     NU(r"מהו שטח האירוע $\{X_2<X_1\}$ בתוך המלבן? (המשולש מתחת לאלכסון)", Fr(1, 2), r"האלכסון $x_2=x_1$ מגיע עד $(1,1)$; מתחתיו משולש ישר זווית עם ניצבים $1$ ו-$1$: שטח $\frac12$."),
     NU(r"מהי $P(X_1>X_2)$?", Fr(1, 4), r"$\frac{1/2}{2}=\frac14$.")])

ADD(1, "ד",
    RB((r"פירוק לפי תוצאת המטבע ($Y=X_1$ בהסתברות $p$, $Y=X_2$ בהסתברות $1-p$)", 2), (r"$P(X_1<L)=1$ ו-$P(X_2<L)=\frac12$", 2), (r"התשובה $\frac{1+p}{2}$", 1)),
    [r"לחשב ממוצע פשוט של שתי ההסתברויות ולהתעלם מהטיית המטבע", r"לכפול $P(X_1<L)\cdot P(X_2<L)$ כאילו נבחרו שני הגפרורים"],
    [CH(r"איזה כלל מחשב את $P(Y<L)$? (בבדיקה ב-$p=0.3$)",
        [r"הסתברות שלמה לפי המטבע: $p\,P(X_1<L)+(1-p)\,P(X_2<L)$",
         r"ממוצע פשוט: $\frac12\bigl(P(X_1<L)+P(X_2<L)\bigr)$",
         r"מכפלה: $P(X_1<L)\cdot P(X_2<L)$"], 0,
        r"נבחר גפרור אחד, ובהסתברות $p$ הוא $X_1$. הממוצע הפשוט נותן $0.75$ (מתעלם מכך שהמטבע מוטה), והמכפלה נותנת $0.5$ (כאילו נבחרו שני הגפרורים). הכלל הנכון נותן $0.65$."),
     NU(r"מהי $P(X_1<L)$?", 1, r"$X_1\sim U(0,L)$ ולכן תמיד קטן מ-$L$ (בהסתברות $1$)."),
     NU(r"מהי $P(X_2<L)$?", Fr(1, 2), r"$X_2\sim U(0,2L)$: $\frac{L}{2L}=\frac12$."),
     NU(r"מהי $P(Y<L)$ כאשר $p=0.3$?", Fr(13, 20), r"$0.3\cdot1+0.7\cdot\frac12=0.65=\frac{1+p}{2}$.")])

ADD(1, "ה",
    RB((r"פירוק לפי תוצאת המטבע (הסתברות שלמה)", 2), (r"$P(\frac L2<X_1<\frac{3L}2)=\frac12$ (רק החלק $(\frac L2,L)$ נמצא בטווח של $X_1$)", 2), (r"$P(\frac L2<X_2<\frac{3L}2)=\frac12$ והתשובה $\frac12$", 1)),
    [r"לספור את כל הקטע $(\frac L2,\frac{3L}2)$ עבור $X_1$ ולקבל $1$", r"לשכוח את ההסתברות $p$ של המטבע"],
    [NU(r"מהי $P(\frac L2<X_1<\frac{3L}2)$? (זכרו ש-$X_1$ מקבל ערכים רק ב-$(0,L)$)", Fr(1, 2), r"הקטע החופף ל-$(0,L)$ הוא $(\frac L2,L)$, באורך $\frac L2$ מתוך $L$."),
     NU(r"מהי $P(\frac L2<X_2<\frac{3L}2)$?", Fr(1, 2), r"הקטע $(\frac L2,\frac{3L}2)$ באורך $L$ נמצא כולו ב-$(0,2L)$: $\frac{L}{2L}=\frac12$."),
     NU(r"מהי ההסתברות המבוקשת כאשר $p=0.3$?", Fr(1, 2), r"$0.3\cdot\frac12+0.7\cdot\frac12=\frac12$ (לכל $p$).")])

# ---- Q2: urn with D red and N-D black; numeric checks at D=3, N=10
Q2MODEL = [r"הוצאה ללא החזרה: הסתברויות מותנות על הרכב הכד שנותר (הסתברות שלמה לפי צבעי ההוצאות הקודמות)",
           r"מכפלה של שתי הסתברויות בלתי תלויות: $P(R_2)=\left(\frac DN\right)^2$",
           r"הניחו שהכדור הראשון אדום, והסתברות הכדור השני היא $\frac{D-1}{N-1}$"]
ADD(2, "א",
    RB((r"בחירת מודל: הוצאה בודדת, כל הכדורים שווי סיכוי (גישה קלאסית)", 2), (r"ספירה: $D$ כדורים אדומים מתוך $N$", 2), (r"התשובה $\frac DN$", 1)),
    [r"להתבלבל בין אדום לשחור ולכתוב $\frac{N-D}{N}$"],
    [CH(r"מוציאים כדור אחד מכד עם $D$ אדומים ו-$N-D$ שחורים. איזה מודל מתאים?",
        [r"מרחב אחיד על $N$ הכדורים, ו-$P=\frac{|A|}{|\Omega|}$ (גישה קלאסית)",
         r"התפלגות גאומטרית: ממתינים לכדור האדום הראשון",
         r"כלל המכפלה של הסתברויות מותנות בהוצאה קודמת"], 0,
        r"הוצאה בודדת מאוסף שווה סיכוי היא מרחב אחיד. הגאומטרית מתארת סדרת ניסויים עד הצלחה, וכאן יש ניסוי יחיד; ואין הוצאה קודמת שאפשר להתנות עליה."),
     NU(r"מהי $P(R_1)$ כאשר $D=3$ ו-$N=10$?", Fr(3, 10), r"$\frac DN=\frac3{10}$.")])

ADD(2, "ב",
    RB((r"הסתברות שלמה לפי צבע הכדור הראשון", 2), (r"הסתברויות מותנות ללא החזרה: $\frac{D-1}{N-1}$ ו-$\frac D{N-1}$", 3), (r"פישוט המונה ל-$D(N-1)$ והתשובה $\frac DN$", 2)),
    [r"להניח הוצאות בלתי תלויות ולכתוב $\frac{D^2}{N^2}$", r"להניח שהכדור הראשון אדום ולכתוב $\frac{D-1}{N-1}$"],
    [CH(r"מוציאים שני כדורים ללא החזרה ומחשבים את $P(R_2)$. איזו גישה נכונה?", Q2MODEL, 0,
        r"הצבע של הכדור הראשון אינו ידוע ולכן מפצלים לפיו. המכפלה $\left(\frac DN\right)^2$ היא ההסתברות ששני הכדורים אדומים ($0.09$ ב-$D=3,N=10$), לא של השני בלבד. הנחה שהראשון אדום נותנת $\frac29$ במקום $0.3$."),
     NU(r"מהי $P(R_1)$ כאשר $D=3$, $N=10$?", Fr(3, 10), r"$\frac{3}{10}$."),
     NU(r"בהינתן ש-$R_1$ התרחש, מהי $P(R_2\mid R_1)$?", Fr(2, 9), r"נותרו $9$ כדורים, $2$ מהם אדומים: $\frac29$."),
     NU(r"בהינתן ש-$B_1$ (הראשון שחור) התרחש, מהי $P(R_2\mid B_1)$?", Fr(1, 3), r"נותרו $9$ כדורים ו-$3$ מהם אדומים: $\frac39=\frac13$."),
     NU(r"מהי $P(R_2)$?", Fr(3, 10), r"$\frac3{10}\cdot\frac29+\frac7{10}\cdot\frac13=\frac{6+21}{90}=\frac3{10}$.")])

ADD(2, "ג",
    RB((r"פיצול לפי צבעי שני הכדורים הראשונים (ארבעה מקרים זרים)", 2), (r"סכום זוגות המקרים: $\frac{D(D-1)}{N(N-1)}$ ו-$\frac{D(N-D)}{N(N-1)}$", 3), (r"התשובה $\frac DN$", 2)),
    [r"לכתוב $\left(\frac DN\right)^3$ (הוצאה עם החזרה)", r"לספור רק את המקרה $R_1R_2R_3$ ולשכוח את שאר שלושת המקרים"],
    [CH(r"מוציאים שלושה כדורים ללא החזרה ומחשבים את $P(R_3)$. איזו גישה נכונה?",
        [r"הסתברות שלמה לפי צבעי שני הכדורים הראשונים (ארבעה מקרים זרים), כל מקרה במכפלת הסתברויות מותנות",
         r"מכפלה של שלוש הסתברויות בלתי תלויות: $P(R_3)=\left(\frac DN\right)^3$",
         r"המקרה $R_1R_2R_3$ בלבד: $P(R_3)=\frac DN\cdot\frac{D-1}{N-1}\cdot\frac{D-2}{N-2}$"], 0,
        r"הכדור השלישי יכול להיות אדום אחרי כל צירוף של שני צבעים. המכפלה $\left(\frac DN\right)^3$ היא ההסתברות ששלושת הכדורים אדומים ($0.027$ ב-$D=3,N=10$). המקרה היחיד $R_1R_2R_3$ נותן $\frac1{120}\approx0.0083$. שניהם רחוקים מ-$0.3$."),
     NU(r"מהי $P(R_1\cap R_2\cap R_3)$ כאשר $D=3$, $N=10$?", Fr(1, 120), r"$\frac3{10}\cdot\frac29\cdot\frac18=\frac{1}{120}$."),
     NU(r"מהי $P(B_1\cap B_2\cap R_3)$ באותם ערכים?", Fr(7, 40), r"$\frac7{10}\cdot\frac69\cdot\frac38=\frac{126}{720}=\frac7{40}$."),
     NU(r"מהי $P(R_3)$ באותם ערכים?", Fr(3, 10), r"ארבעת המקרים: $\frac1{120}+\frac7{120}+\frac7{120}+\frac{21}{120}=\frac{36}{120}=\frac3{10}$ (כל אחד משני המקרים המעורבים הוא $\frac7{120}$).")])

ADD(2, "ד",
    RB((r"הגדרת הסתברות מותנית $P(R_3\mid R_2)=\frac{P(R_2\cap R_3)}{P(R_2)}$", 2), (r"$P(R_2)=\frac DN$ מהסעיף הקודם", 1), (r"פיצול $P(R_2R_3)$ לפי הכדור הראשון: $\frac{D(D-1)}{N(N-1)}$", 2), (r"התשובה $\frac{D-1}{N-1}$", 1)),
    [r"לכתוב $\frac{D-2}{N-2}$ (להניח ששני הכדורים הקודמים אדומים)", r"להניח אי-תלות ולכתוב $\frac DN$"],
    [CH(r"נתון ש-$R_2$ התרחש (הכדור הראשון אינו ידוע). איזה חישוב נכון ל-$P(R_3\mid R_2)$?",
        [r"היחס $\frac{P(R_2\cap R_3)}{P(R_2)}$ של שתי הסתברויות בלתי מותנות",
         r"$P(R_3\mid R_2)=P(R_3)=\frac DN$, כי ההוצאות בלתי תלויות",
         r"$\frac{D-2}{N-2}$, בהנחה ששני הכדורים הקודמים אדומים"], 0,
        r"ההוצאות ללא החזרה תלויות. ב-$D=3,N=10$ התשובה הנכונה היא $\frac29\approx0.222$, ואילו אי-תלות נותנת $0.3$ וההנחה על שני אדומים נותנת $\frac18$."),
     NU(r"מהי $P(R_2)$ כאשר $D=3$, $N=10$? (המכנה: אירוע התנאי)", Fr(3, 10), r"$\frac DN=\frac3{10}$ (מסעיף ב)."),
     NU(r"מהי $P(R_2\cap R_3)$ באותם ערכים? (המונה)", Fr(1, 15), r"$\frac{D(D-1)}{N(N-1)}=\frac{6}{90}=\frac1{15}$."),
     NU(r"מהי $P(R_3\mid R_2)$?", Fr(2, 9), r"$\frac{1/15}{3/10}=\frac29=\frac{D-1}{N-1}$.")])

# ---- Q3: two distinct digits from 1..9, ordered
CNT = r"מרחב המדגם הוא הזוגות הסדורים של ספרות שונות מ-$\{1,\dots,9\}$."
ADD(3, "א",
    RB((r"מרחב המדגם: זוגות סדורים ללא חזרה, $|\Omega|=9\cdot8=72$", 2), (r"המספר זוגי אם ורק אם ספרת האחדות זוגית", 2), (r"ספירה: $4\cdot8=32$ והתשובה $\frac49$", 3)),
    [r"לספור זוגות לא סדורים ($36$) או עם חזרה ($81$)", r"לשכוח שספרת העשרות מוגבלת ל-$8$ אפשרויות (ללא חזרה)"],
    [CH(CNT + r" מהו גודל מרחב המדגם?",
        [r"$72$ זוגות סדורים ללא חזרה ($9\cdot8$)", r"$81$ זוגות סדורים עם חזרה ($9\cdot9$)", r"$36$ זוגות לא סדורים"], 0,
        r"הספרה הראשונה היא העשרות והשנייה האחדות, ולכן $12\ne21$ (הסדר חשוב, לא $36$). ההוצאה ללא החזרה, ולכן הספרות שונות (לא $81$)."),
     NU(r"כמה זוגות סדורים נותנים מספר זוגי? (ספרת האחדות זוגית)", 32, r"$4$ ערכים לאחדות ($2,4,6,8$) ו-$8$ ערכים לעשרות: $32$."),
     NU(r"מהי ההסתברות שהמספר זוגי?", Fr(4, 9), r"$\frac{32}{72}=\frac49$.")])

ADD(3, "ב",
    RB((r"קריטריון התחלקות ב-3: סכום הספרות מתחלק ב-3", 2), (r"מספר הספרות בכל שארית מודולו $3$ הוא $3$, ואיסוף הזוגות: $6+18=24$", 3), (r"התשובה $\frac13$", 2)),
    [r"להשתמש בספרת האחדות בלבד כקריטריון", r"לשכוח שהספרות חייבות להיות שונות (שארית 0: $3\cdot2$ ולא $3\cdot3$)"],
    [CH(r"איזה קריטריון קובע אם מספר דו-ספרתי מתחלק ב-3?",
        [r"סכום הספרות מתחלק ב-$3$", r"ספרת האחדות מתחלקת ב-$3$", r"ספרת העשרות מתחלקת ב-$3$"], 0,
        r"כך ב-$3$ בלבד. למשל $13$ מסתיים ב-$3$ ואינו מתחלק ב-$3$, ו-$12$ מתחלק ב-$3$ אף שהאחדות שלו $2$."),
     NU(r"כמה זוגות סדורים של ספרות שונות מ-$\{1,\dots,9\}$ סכומם מתחלק ב-$3$?", 24, r"שתיהן בשארית $0$: $3\cdot2=6$. שארית $1$ ושארית $2$ בשני הסדרים: $2\cdot3\cdot3=18$. סך הכול $24$."),
     NU(r"מהי ההסתברות שהמספר מתחלק ב-$3$?", Fr(1, 3), r"$\frac{24}{72}=\frac13$.")])

ADD(3, "ג",
    RB((r"קריטריון: ספרת האחדות היא $5$ (או $0$, שאינו באוסף)", 2), (r"ספירה: $8$ אפשרויות לספרת העשרות", 3), (r"התשובה $\frac19$", 2)),
    [r"לכלול גם את המקרה שספרת העשרות היא $5$", r"לספור $9$ אפשרויות לעשרות (בלי החזרה: $8$)"],
    [CH(r"איזה קריטריון קובע אם מספר דו-ספרתי מתחלק ב-5 (כאשר $0$ אינו באוסף)?",
        [r"ספרת האחדות היא $5$", r"ספרת העשרות היא $5$", r"סכום הספרות מתחלק ב-$5$"], 0,
        r"כך ב-$5$ בלבד. $52$ אינו מתחלק ב-$5$ אף שהעשרות $5$, ו-$14$ (סכום $5$) אינו מתחלק ב-$5$."),
     NU(r"כמה זוגות סדורים נותנים מספר המתחלק ב-$5$?", 8, r"האחדות $5$, והעשרות כל ספרה אחרת: $8$."),
     NU(r"מהי ההסתברות שהמספר מתחלק ב-$5$?", Fr(1, 9), r"$\frac8{72}=\frac19$.")])

ADD(3, "ד",
    RB((r"הגדרת הסתברות מותנית כיחס ספירות: $\frac{|\text{even}\cap\text{odd sum}|}{|\text{odd sum}|}$", 1), (r"מכנה: $2\cdot5\cdot4=40$ זוגות עם סכום אי-זוגי", 1), (r"מונה: $5\cdot4=20$ (עשרות אי-זוגית, אחדות זוגית)", 1), (r"התשובה $\frac12$", 1)),
    [r"להשתמש במכנה $36$ (חצי מ-$72$) ולקבל $\frac59$", r"לשכוח שהסדר חשוב ולספור רק $20$ זוגות סכום אי-זוגי"],
    [NU(r"כמה זוגות סדורים סכום ספרותיהם אי-זוגי? (אחת אי-זוגית, אחת זוגית, בשני הסדרים)", 40, r"$2\cdot5\cdot4=40$ (לא $36$)."),
     NU(r"מהי $P(\text{odd sum})$? (המכנה: אירוע התנאי)", Fr(5, 9), r"$\frac{40}{72}=\frac59$."),
     NU(r"מהי $P(\text{even number}\cap\text{odd sum})$? (המונה: עשרות אי-זוגית ואחדות זוגית)", Fr(5, 18), r"$\frac{5\cdot4}{72}=\frac5{18}$."),
     NU(r"מהי ההסתברות המותנית?", Fr(1, 2), r"$\frac{5/18}{5/9}=\frac12$.")])

# ---- Q4: pdf with a=1/3, b=1 (triangle on (-a,a) with peak 1, then constant 1 up to b)
ADD(4, "א",
    RB((r"נרמול: שטח המשולש $a$ ושטח המלבן $b-a$, ולכן $b=1$", 3), (r"סימטריה: אינטגרל $zf_Z(z)$ על $(-a,a)$ הוא $0$", 2), (r"תוחלת: $\frac{b^2-a^2}{2}=\frac49$", 3), (r"פתרון $a=\frac13$, $b=1$", 2)),
    [r"לכלול את המשולש בחישוב התוחלת ולקבל משוואה שגויה", r"לשכוח שהנרמול קובע את $b$ ללא תלות ב-$a$"],
    [NU(r"הצפיפות בגובה $1$. שטח המשולש על $(-a,a)$ הוא $a$ ושטח המלבן $(a,b)$ הוא $b-a$. מהו $b$ שנובע מהנרמול?", 1, r"$a+(b-a)=b=1$."),
     CH(r"מה תרומת הקטע $(-a,a)$ לתוחלת $\mathbb E[Z]$?",
        [r"$0$, כי $zf_Z(z)$ אי-זוגית והקטע סימטרי", r"חיובית ושווה ל-$\frac a2$", r"שלילית כי הקטע כולל ערכים שליליים"], 0,
        r"הצפיפות זוגית ולכן $zf_Z(z)$ אי-זוגית; האינטגרל על קטע סימטרי מתאפס. הערכים השליליים מתקזזים עם החיוביים, ולכן התרומה לא חיובית ולא שלילית."),
     NU(r"מהו $a$ אם $\mathbb E[Z]=\frac{1-a^2}{2}=\frac49$?", Fr(1, 3), r"$a^2=1-\frac89=\frac19$, ולכן $a=\frac13$.")])

ADD(4, "ב",
    RB((r"פירוק לקטעים: $(-\frac13,0)$, $(0,\frac13)$, $(\frac13,1)$", 2), (r"$F_Z$ על כל קטע: $\frac{(1+3t)^2}6$, $\frac13-\frac{(1-3t)^2}6$, $t$", 5), (r"רציפות ב-$0$ וב-$\frac13$ והערכים $0$ ו-$1$ בקצוות", 3)),
    [r"לשכוח את הקבוע $\frac13$ בקטע השני (להניח $F_Z(0)=0$)", r"לא לבדוק רציפות בין הקטעים"],
    [NU(r"מהו $F_Z(0)=P(Z\le0)$? (השטח של חצי המשולש השמאלי)", Fr(1, 6), r"משולש ישר זווית עם בסיס $\frac13$ וגובה $1$: שטח $\frac16$."),
     NU(r"מהו $F_Z(\frac16)$? (הקטע $0\le t<\frac13$)", Fr(7, 24), r"$\frac13-\frac{(1-\frac12)^2}6=\frac13-\frac1{24}=\frac7{24}$."),
     NU(r"מהו $F_Z(\frac12)$? (הקטע $\frac13\le t<1$)", Fr(1, 2), r"בקטע הזה $F_Z(t)=t$.")])

ADD(4, "ג",
    RB((r"הגדרת הסתברות מותנית כיחס של הפרשי $F_Z$", 2), (r"מכנה: $F_Z(\frac34)-F_Z(-\frac34)=\frac34$", 1), (r"מונה: $F_Z(\frac34)-F_Z(\frac14)=\frac{41}{96}$", 1), (r"התשובה $\frac{41}{72}$", 1)),
    [r"לחלק ב-$1$ ולא ב-$P(|Z|<\frac34)$", r"לטעות בערך של $F_Z(\frac14)$ (להשתמש בקטע הלא נכון)"],
    [NU(r"מהי $P(|Z|<\frac34)=F_Z(\frac34)-F_Z(-\frac34)$? (המכנה)", Fr(3, 4), r"$\frac34-0=\frac34$ (הצפיפות מתאפסת משמאל ל-$-\frac13$)."),
     NU(r"מהו $F_Z(\frac14)$?", Fr(31, 96), r"$\frac13-\frac{(1-\frac34)^2}6=\frac13-\frac1{96}=\frac{31}{96}$."),
     NU(r"מהי $P(\frac14<Z<\frac34)$? (המונה)", Fr(41, 96), r"$\frac34-\frac{31}{96}=\frac{72-31}{96}=\frac{41}{96}$."),
     NU(r"מהי ההסתברות המותנית?", Fr(41, 72), r"$\frac{41/96}{3/4}=\frac{41}{72}$.")])

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

# ---- Q6: bridge Q1 and series-of-parallels Q2; numeric checks at p=0.6
ADD(6, "א",
    RB((r"פיצול לפי הרכיב $E$ (הגשר)", 3), (r"$E$ פועל: $(2p-p^2)^2$; $E$ אינו פועל: $2p^2-p^4$", 4), (r"הצבה ופישוט ל-$p^2(2+2p-5p^2+2p^3)$", 2)),
    [r"להתייחס למעגל כטור-מקבילי ולהתעלם מ-$E$", r"לטעות בהתאמה בין הרכיבים בגשר (למשל $A\!-\!E\!-\!D$)"],
    [CH(r"איך מחשבים את $P(Q_1)$ במעגל הגשר?",
        [r"מפצלים לפי $E$: כש-$E$ פועל המעגל הוא $(A\cup C)\cap(B\cup D)$, וכשאינו פועל $(AB)\cup(CD)$", r"מניחים שהמעגל הוא $(AB)\cup(CD)$ ומתעלמים מ-$E$", r"כל חמשת הרכיבים בטור: $p^5$"], 0,
        r"ל-$E$ יש תפקיד. ב-$p=0.6$ ההתעלמות מ-$E$ נותנת $0.5904$ (קטן מהנכון $0.65952$) וטור נותן $0.07776$."),
     NU(r"מהי $P(Q_1\mid E\ \text{works})$ כאשר $p=0.6$?", (2 * _p6 - _p6 ** 2) ** 2, r"$(2p-p^2)^2=0.84^2=0.7056$."),
     NU(r"מהי $P(Q_1\mid E\ \text{fails})$ באותו $p$?", 2 * _p6 ** 2 - _p6 ** 4, r"$2p^2-p^4=0.72-0.1296=0.5904$."),
     NU(r"מהי $P(Q_1)$?", _PQ1, r"$0.6\cdot0.7056+0.4\cdot0.5904=0.65952$.")])

ADD(6, "ב",
    RB((r"$Q_2$ הוא טור של שני מקבצים בלתי תלויים: $(A\cup B)$ ו-$(C\cup D\cup E)$", 4), (r"$P(A\cup B)=2p-p^2$ ו-$P(C\cup D\cup E)=1-(1-p)^3$", 3), (r"המכפלה $6p^2-9p^3+5p^4-p^5$", 2)),
    [r"להתייחס ל-$Q_2$ כמקבילי של הכול", r"לטעות במשלים: $1-(1-p)^3$ ולא $1-(1-p)^2$"],
    [CH(r"איזה תיאור מתאים ל-$Q_2$ ($A$ ו-$B$ במקביל, בטור עם $C$, $D$ ו-$E$ במקביל)?",
        [r"טור של שני מקבצים בלתי תלויים, ולכן $P(Q_2)=P(A\cup B)\cdot P(C\cup D\cup E)$", r"חמישה רכיבים במקביל: $1-(1-p)^5$", r"חמישה רכיבים בטור: $p^5$"], 0,
        r"במעגל שני מקבצים (שני רכיבים ושלושה רכיבים) בטור. במקביל מלא היה נותן $0.98976$ ובטור מלא $0.07776$, לא הערך הנכון $0.78624$."),
     NU(r"מהי $P(A\cup B)$ כאשר $p=0.6$?", 2 * _p6 - _p6 ** 2, r"$1-0.4^2=0.84$."),
     NU(r"מהי $P(C\cup D\cup E)$ באותו $p$?", 1 - (1 - _p6) ** 3, r"$1-0.4^3=0.936$."),
     NU(r"מהי $P(Q_2)$?", _PQ2, r"$0.84\cdot0.936=0.78624$.")])

ADD(6, "ג",
    RB((r"הגדרת הסתברות מותנית $\frac{P(Q_1\cap Q_2)}{P(Q_2)}$", 2), (r"חישוב $P(Q_1\cap Q_2)$ בהסתברות שלמה לפי $A,B$ (ארבעה מקרים)", 3), (r"הצבה ופישוט ל-$\frac{p(7-9p+3p^2)}{6-9p+5p^2-p^3}$", 2)),
    [r"להניח ש-$Q_1$ ו-$Q_2$ בלתי תלויים ולכפול", r"להתנות על $Q_1$ במקום על $Q_2$"],
    [CH(r"איך מחשבים את $P(Q_1\cap Q_2)$?",
        [r"בהסתברות שלמה לפי $A,B$, כי שני המעגלים משתמשים באותם רכיבים", r"כמכפלה $P(Q_1)\cdot P(Q_2)$, כי הם בלתי תלויים", r"כסכום $P(Q_1)+P(Q_2)$"], 0,
        r"המעגלים תלויים כי הם חולקים רכיבים. ב-$p=0.6$ המכפלה נותנת $0.5185$ במקום $0.57888$, והסכום עולה על $1$."),
     NU(r"מהי $P(Q_2)$ כאשר $p=0.6$? (המכנה: אירוע התנאי)", _PQ2, r"$0.78624$ מסעיף ב."),
     NU(r"מהי $P(Q_1\cap Q_2)$ באותו $p$? (המונה)", _PI, r"$3p^5-9p^4+7p^3=0.23328-1.1664+1.512=0.57888$."),
     NU(r"מהי $P(Q_1\mid Q_2)$?", _PI / _PQ2, r"$\frac{0.57888}{0.78624}\approx0.7363$.")])

APPLY(questions)


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
