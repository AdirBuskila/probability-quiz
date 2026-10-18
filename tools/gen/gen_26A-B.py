# -*- coding: utf-8 -*-
"""Generator for tools/raw/26A-B.json -- probability (course 20021), semester A 2026, moed B (30.04.2026),
flagship sitting. 6 questions, 23 items (Q1 3, Q2 3, Q3 4, Q4 4, Q5 5, Q6 4), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_26A-B.py

Source: exam pp.1-3 (pdf), typed official solutions in Hebrew pp.4-15 (printed 1-12). Pages 16+ are the
same solutions in other languages and are not used.

Transcription notes
- Part keys: the id scheme allows ONE letter per part, but Q5 and Q6 print sub-parts "א-1", "א-2", "א-3",
  "ב-1", "ב-2". They are stored as consecutive letters (Q5: א ב ג ד ה; Q6: א ב ג ד) and the printed label is
  the first bold token of each question text. Map: Q5 a=א-1, b=א-2, c=א-3, d=ב-1, e=ב-2;
  Q6 a=א-1, b=א-2, c=ב-1, d=ב-2.
- Math never holds Hebrew. Where the print has a Hebrew word inside a formula (P(X זוגי), "אחרת") the word is
  moved out of the math or replaced by an English word inside it (even / odd / else); the meaning is unchanged.
- Q3 q2/q4 SWAP (arbiter ruling 2026-10-18, standing "official typo" ruling: the printed question wins):
  the printed exam defines q2 = P(B | not-A and not-C) and q4 = P(B | not-A and C); the official solution
  (and its translations) uses q2 = P(B | not-A and C) and q4 = P(B | not-A and not-C). The official final
  answers of parts a, b and d are therefore wrong for the printed question (p=0.3, q=(.9,.7,.5,.3):
  P(B) 0.480 official vs 0.592 true). Shipped with the official method, q2/q4 swapped back to the printed
  definitions, solutionSource "solved", official:false and the "הפתרון הרשמי עם תיקון" prefix. Verified exactly
  and by Monte Carlo in tools/verify/26A-B/check.py. Part c is unaffected (official).
- Q1(a) carries a `region` (the area figure, t = 0.3) and a `sim`; Q1(c) a `sim` (Var[D]).
- The official solution header notes it is written for second-year level and that Q1 is solved with the
  classical-geometric approach as the question asked; that note is not part of any solution text.
"""
import itertools, json, math, pathlib
from fractions import Fraction

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "26A-B.json"
CODE = "26A-B"
IMG = "images/exams/26A-B-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_LEAD = r"נתבונן במטריצה האקראית $\boldsymbol{Q}=\begin{pmatrix}X&1\\0&Y\end{pmatrix}$, בהנחה ש-$X\sim U_c(0,1)$ ו-$Y\sim U_c(0,1)$ מהווים משתנים מקריים רציפים בלתי תלויים."

questions.append(Q(
    1, "א", "uniform_geometric",
    r"יהי $D=\det\boldsymbol{Q}$ הדטרמיננטה של המטריצה $\boldsymbol{Q}$. חשבו את פונקציית ההתפלגות המצטברת $F_D(t)$ של משתנה מקרי $D$ ושרטטו אותה.",
    r"""נשתמש בגישה הקלאסית להסתברות. מרחב המדגם הוא
$$\Omega=\{(x,y):0<x<1,\ 0<y<1\},$$
כלומר ריבוע היחידה במישור $(x,y)$. מאחר ש-$(X,Y)$ אחיד על הריבוע, הסתברויות שוות לשטחים בתוך הריבוע, ושטח הריבוע כולו הוא $1$.
עבור $0<t<1$ האירוע שאת שטחו מחשבים הוא
$$\{D\le t\}=\{XY\le t\}=\{(x,y)\in(0,1)^2:xy\le t\}.$$
השפה של האירוע בתוך הריבוע היא ההיפרבולה $xy=t$, כלומר $y=t/x$. האזור המוצל באיור הוא בדיוק האירוע $\{XY\le t\}$, עבור ערך מייצג של $t$.
![האזור xy ≤ t בתוך ריבוע היחידה: שטח t משמאל ל-x=t ושטח האינטגרל מתחת להיפרבולה מימין](images/exams/26A-B-Q1-region.png)
לכן, עבור $0<t<1$, השטח מתפצל באופן טבעי לשני חלקים:
• עבור $0<x<t$, האי-שוויון $xy\le t$ מתקיים לכל $0<y<1$, ולכן תרומת השטח היא $t$;
• עבור $t<x<1$, האי-שוויון שקול ל-$0<y\le t/x$, ולכן תרומת השטח היא $\int_t^1\frac{t}{x}\,dx$.
מכאן
$$\begin{aligned}F_D(t)&=P(D\le t)\\&=\operatorname{area}\{(x,y)\in(0,1)^2:xy\le t\}\\&=t+\int_t^1\frac{t}{x}\,dx\\&=t+t\,[\ln x]_t^1\\&=t-t\ln t.\end{aligned}$$
יחד עם מקרי הקצה מתקבל
$$F_D(t)=\begin{cases}0,&t<0,\\t-t\ln t,&0\le t<1,\\1,&t\ge 1.\end{cases}$$
ב-$t=0$ הביטוי $t-t\ln t$ מפורש לפי הגבול $0$ כאשר $t\downarrow 0$.
![גרף פונקציית ההתפלגות המצטברת של D=XY](images/exams/26A-B-Q1-cdf.png)""",
    12, contextId="c1",
    # area figure (region.js), from tools/verify/26A-B/regions.json, drawn at the representative t = 0.3:
    # P(XY <= 0.3) = t - t ln t at t = 0.3
    region={"space": {"x": [0, 1], "y": [0, 1]}, "labels": {"x": "X", "y": "Y"},
            "event": [{"expr": "x*y", "op": "<=", "c": 0.3}],
            "exact": 0.3 - 0.3 * math.log(0.3),
            "caption": "האזור XY ≤ t בריבוע היחידה, עבור t = 0.3 לדוגמה"}))

questions.append(Q(
    1, "ב", "continuous_rv",
    r"מצאו את פונקציית צפיפות ההסתברות $f_D(t)$ ושרטטו אותה.",
    r"""עבור $0<t<1$,
$$f_D(t)=F_D'(t)=\frac{d}{dt}(t-t\ln t)=1-(\ln t+1)=-\ln t.$$
לכן
$$f_D(t)=\begin{cases}-\ln t,&0<t<1,\\0,&\text{else}.\end{cases}$$
הצפיפות שואפת ל-$+\infty$ כאשר $t\downarrow 0$, ושווה ל-$0$ ב-$t=1$.
![גרף פונקציית הצפיפות של D=XY](images/exams/26A-B-Q1-pdf.png)""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "continuous_rv",
    r"חשבו את התוחלת $\mathbb{E}[D]$ ואת השונות $\operatorname{var}[D]$.",
    r"""כאן לא נשתמש בצפיפות של $D$. במקום זאת נשתמש באי-התלות של $X,Y$ וברגעים הסטנדרטיים של משתנה אחיד על $(0,1)$:
$$\mathbb{E}[X]=\mathbb{E}[Y]=\frac12,\qquad \mathbb{E}[X^2]=\mathbb{E}[Y^2]=\frac13.$$
מאחר ש-$X,Y$ בלתי תלויים ו-$D=XY$,
$$\mathbb{E}[D]=\mathbb{E}[XY]=\mathbb{E}[X]\,\mathbb{E}[Y]=\frac12\cdot\frac12=\frac14.$$
עבור השונות נחשב תחילה את הרגע השני, שוב באמצעות אי-תלות:
$$\mathbb{E}[D^2]=\mathbb{E}[X^2Y^2]=\mathbb{E}[X^2]\,\mathbb{E}[Y^2]=\frac13\cdot\frac13=\frac19.$$
לכן
$$\operatorname{Var}(D)=\mathbb{E}[D^2]-\mathbb{E}[D]^2=\frac19-\left(\frac14\right)^2=\frac19-\frac1{16}=\frac7{144}.$$
ולסיכום,
$$\mathbb{E}[D]=\frac14,\qquad \operatorname{Var}(D)=\frac7{144}.$$""",
    8, contextId="c1"))

# ------------------------------------------------------------------ Q2
HINT2 = r"""**הערה:** במידת הצורך ניתן להיעזר בזהות
$$\sum_{k=m}^{\infty}C_{k-1}^{m-1}a^k=\left(\frac{a}{1-a}\right)^m.$$"""

questions.append(Q(
    2, "א", "special_discrete",
    r"מטבע מוטה, בעל הסתברות $p$ לתוצאת ה״עץ״, מוטל $n$ פעמים ($n\ge 2$). מהי ההסתברות שתוצאת ה״פלי״ תופיע **בפעם הראשונה** רק **אחרי** ״עץ״?",
    r"""**הפלי הראשון מופיע רק לאחר עץ.**
נפרש את האירוע כך: במהלך $n$ ההטלות מופיע פלי ראשון, והוא מופיע לאחר לפחות עץ אחד. שקול לכך שהפלי הראשון מופיע בהטלה $k$, כאשר $2\le k\le n$.
אם הפלי הראשון מתקבל בהטלה $k$, אז $k-1$ ההטלות הראשונות הן עץ וההטלה ה-$k$ היא פלי. לכן
$$P(\text{first tail at toss }k)=p^{k-1}(1-p).$$
מכאן
$$\begin{aligned}P&=\sum_{k=2}^{n}p^{k-1}(1-p)\\&=(1-p)\left(p+p^2+\cdots+p^{n-1}\right)\\&=p\left(1-p^{n-1}\right).\end{aligned}$$
ולכן
$$P=p\left(1-p^{n-1}\right).$$""",
    10))

questions.append(Q(
    2, "ב", "special_discrete",
    r"הסעיפים הבאים אינם קשורים לסעיף א׳." "\n"
    r"מטילים מטבע מוטה, בעל הסתברות $p$ לתוצאת ה״עץ״, עד קבלת ה״עץ״ בפעם הראשונה. מהי ההסתברות שה״עץ״ הראשון יתקבל בהטלה שמספרה **זוגי**?",
    r"""**העץ הראשון מתקבל בהטלה שמספרה זוגי.**
נסמן ב-$X$ את מספר ההטלה שבה מתקבל העץ הראשון. אז
$$P(X=k)=(1-p)^{k-1}p,\qquad k=1,2,\ldots$$
נשתמש ישירות בנוסחת הזוגיות
$$P(X\ \mathrm{even})=\mathbb{E}\left[\frac{1+(-1)^X}{2}\right]=\frac{1+\mathbb{E}[(-1)^X]}{2}.$$
נותר לחשב את $\mathbb{E}[(-1)^X]$ מתוך ההתפלגות של $X$:
$$\begin{aligned}\mathbb{E}[(-1)^X]&=\sum_{k=1}^{\infty}(-1)^kP(X=k)\\&=\sum_{k=1}^{\infty}(-1)^k(1-p)^{k-1}p\\&=-p\sum_{r=0}^{\infty}\bigl(-(1-p)\bigr)^r\\&=-\frac{p}{1+(1-p)}\\&=-\frac{p}{2-p}.\end{aligned}$$
לפיכך
$$P(X\ \mathrm{even})=\frac12\left(1-\frac{p}{2-p}\right)=\frac{1-p}{2-p}.$$
ולכן
$$P(X\ \mathrm{even})=\frac{1-p}{2-p}.$$""",
    10))

questions.append(Q(
    2, "ג", "special_discrete",
    r"מטילים מטבע מוטה, בעל הסתברות $p$ לתוצאת ה״עץ״, עד קבלת ה-״עץ״ בפעם ה-$m$. מהי ההסתברות שזה יקרה בהטלה שמספרה **אי-זוגי**?" "\n" + HINT2,
    r"""**העץ ה-$m$ מתקבל בהטלה שמספרה אי-זוגי.**
נסמן ב-$Y$ את מספר ההטלה שבה מופיע העץ ה-$m$. אז ל-$Y$ יש צורה בינומית שלילית:
$$P(Y=k)=\binom{k-1}{m-1}p^m(1-p)^{k-m},\qquad k=m,m+1,\ldots$$
לפי נוסחת הזוגיות עבור ערכים אי-זוגיים,
$$P(Y\ \mathrm{odd})=\mathbb{E}\left[\frac{1-(-1)^Y}{2}\right]=\frac{1-\mathbb{E}[(-1)^Y]}{2}.$$
נחשב ישירות את $\mathbb{E}[(-1)^Y]$, בעזרת פונקציית ההסתברות של $Y$,
$$\begin{aligned}\mathbb{E}[(-1)^Y]&=\sum_{k=m}^{\infty}(-1)^k\binom{k-1}{m-1}p^m(1-p)^{k-m}\\&=\left(\frac{p}{1-p}\right)^m\sum_{k=m}^{\infty}\binom{k-1}{m-1}\bigl(-(1-p)\bigr)^k.\end{aligned}$$
נשתמש בזהות הנתונה במבחן,
$$\sum_{k=m}^{\infty}\binom{k-1}{m-1}a^k=\left(\frac{a}{1-a}\right)^m,\qquad |a|<1,$$
עם $a=-(1-p)$, ונקבל
$$\sum_{k=m}^{\infty}\binom{k-1}{m-1}\bigl(-(1-p)\bigr)^k=\left(\frac{-(1-p)}{1+(1-p)}\right)^m.$$
לכן
$$\begin{aligned}\mathbb{E}[(-1)^Y]&=\left(\frac{p}{1-p}\right)^m\left(\frac{-(1-p)}{1+(1-p)}\right)^m\\&=(-1)^m\left(\frac{p}{2-p}\right)^m.\end{aligned}$$
הצבה בנוסחת הזוגיות נותנת
$$P(Y\ \mathrm{odd})=\frac{1-(-1)^m\left(\frac{p}{2-p}\right)^m}{2}.$$
עבור $p=1$ אותה נוסחה מפורשת במובן הדטרמיניסטי: $Y=m$.""",
    5))

# ------------------------------------------------------------------ Q3  (a, b, d: q2/q4 swap corrected, official:false)
Q3_NOTE = (r"בקו ייצור לרכיבים אלקטרוניים בטכנולוגיית הדפסת תלת-ממד, מדפיסים שלושה רכיבים $A$, $B$ ו-$C$ זה לצד זה. "
           r"תקינות הרכיבים הצדדיים ($A$ ו-$C$) לא תלויה זו בזו, וההסתברות של כל אחד מהם להיות תקין היא $P(A)=P(C)=p$. "
           r"בשל אופי התהליך הטכנולוגי, קיימת תלות בין תקינות הרכיב האמצעי $B$ לבין תקינות הרכיבים הצדדיים:"
           "\n"
           r"$$P(B/A\cap C)=q_1,\quad P(B/\overline{A}\cap\overline{C})=q_2,\quad P(B/A\cap\overline{C})=q_3,\quad P(B/\overline{A}\cap C)=q_4.$$")

# Typo-ruling prefix for Q3 a, b, d (the official solution swaps q2 and q4 relative to the printed question).
FIX = (r"**הפתרון הרשמי עם תיקון:** בפתרון הרשמי הוגדרו $q_2=P(B\mid\bar A\cap C)$ ו-$q_4=P(B\mid\bar A\cap\bar C)$, "
       r"הפוך מהשאלה כפי שהודפסה, שבה $q_2=P(B\mid\bar A\cap\bar C)$ ו-$q_4=P(B\mid\bar A\cap C)$. "
       r"הפתרון שלהלן הוא הפתרון הרשמי, עם $q_2$ ו-$q_4$ לפי ההגדרות המודפסות, ולכן ")

questions.append(Q(
    3, "א", "conditional_bayes",
    r"מצאו את ההסתברות שהרכיב $B$ תקין (פועל).",
    FIX + r"""התשובה הסופית שונה מהתשובה הרשמית $q_1p^2+(q_2+q_3)p(1-p)+q_4(1-p)^2$. התיקון נבדק (חישוב מדויק וסימולציה).
**ההסתברות שהרכיב $B$ פועל.**
לפי נוסחת ההסתברות השלמה על ארבעת המקרים הזרים הנקבעים על ידי $A$ ו-$C$,
$$\begin{aligned}P(B)&=P(B\mid A\cap C)P(A\cap C)+P(B\mid\bar A\cap C)P(\bar A\cap C)\\&\quad+P(B\mid A\cap\bar C)P(A\cap\bar C)+P(B\mid\bar A\cap\bar C)P(\bar A\cap\bar C).\end{aligned}$$
מאחר ש-$A$ ו-$C$ בלתי תלויים,
$$P(A\cap C)=p^2,\quad P(\bar A\cap C)=(1-p)p,\quad P(A\cap\bar C)=p(1-p),\quad P(\bar A\cap\bar C)=(1-p)^2.$$
לכן
$$P(B)=q_1p^2+q_4p(1-p)+q_3p(1-p)+q_2(1-p)^2.$$
באופן שקול,
$$P(B)=q_1p^2+(q_3+q_4)p(1-p)+q_2(1-p)^2.$$""",
    5, contextId="c3", solutionSource="solved", official=False))

questions.append(Q(
    3, "ב", "independence",
    r"האם תקינות הרכיב $A$ תלויה בתקינות הרכיב $B$? אם כן, חשבו $P(A/B)$. אם לא, הסבירו מדוע.",
    FIX + r"""תנאי אי-התלות והמכנה של $P(A\mid B)$ שונים מהתשובה הרשמית (שם: $pq_1+(1-p)q_3=pq_2+(1-p)q_4$, והמכנה $q_1p^2+(q_2+q_3)p(1-p)+q_4(1-p)^2$). התיקון נבדק (חישוב מדויק וסימולציה).
**האם $A$ תלוי ב-$B$? מצאו $P(A\mid B)$.**
מתקיים $P(B\mid A)=pq_1+(1-p)q_3$ ו-$P(B\mid\bar A)=pq_4+(1-p)q_2$. המאורעות $A$ ו-$B$ בלתי תלויים רק תחת התנאי
$$pq_1+(1-p)q_3=pq_4+(1-p)q_2.$$
אחרת, הם תלויים זה בזה. בהנחה ש-$P(B)>0$,
$$P(A\mid B)=\frac{P(A\cap B)}{P(B)}.$$
כעת
$$\begin{aligned}P(A\cap B)&=P(A\cap B\cap C)+P(A\cap B\cap\bar C)\\&=P(B\mid A\cap C)P(A\cap C)+P(B\mid A\cap\bar C)P(A\cap\bar C)\\&=q_1p^2+q_3p(1-p).\end{aligned}$$
ולכן
$$P(A\mid B)=\frac{q_1p^2+q_3p(1-p)}{q_1p^2+(q_3+q_4)p(1-p)+q_2(1-p)^2}.$$""",
    4, contextId="c3", solutionSource="solved", official=False))

questions.append(Q(
    3, "ג", "circuits",
    r"מחברים את שלושת הרכיבים בטור (כמתואר במעגל $Q_1$). מהי ההסתברות $P(Q_1)$ שהמעגל פועל?" "\n"
    r"**הערה:** אין להשתמש בטבלאות אמת. יש לספק חישוב מפורט ומנומק לכל סעיף.",
    r"""**חיבור בטור.**
בחיבור בטור המעגל פועל אם ורק אם שלושת הרכיבים פועלים:
$$Q_1=A\cap B\cap C.$$
לכן
$$P(Q_1)=P(A\cap B\cap C)=q_1p^2.$$""",
    8, contextId="c3"))

questions.append(Q(
    3, "ד", "circuits",
    r"מחברים את שלושת הרכיבים במקביל (כמתואר במעגל $Q_2$). מהי ההסתברות $P(Q_2)$ שהמעגל פועל?" "\n"
    r"**הערה:** אין להשתמש בטבלאות אמת. יש לספק חישוב מפורט ומנומק לכל סעיף.",
    FIX + r"""התשובה הסופית שונה מהתשובה הרשמית $1-(1-q_4)(1-p)^2$. התיקון נבדק (חישוב מדויק וסימולציה).
**חיבור במקביל.**
בחיבור במקביל המעגל נכשל אם ורק אם שלושת הרכיבים נכשלים. לכן
$$P(Q_2)=1-P(\bar A\cap\bar B\cap\bar C).$$
כעת
$$P(\bar A\cap\bar B\cap\bar C)=P(\bar B\mid\bar A\cap\bar C)P(\bar A\cap\bar C)=(1-q_2)(1-p)^2.$$
ומכאן
$$P(Q_2)=1-(1-q_2)(1-p)^2.$$""",
    8, contextId="c3", solutionSource="solved", official=False))

# ------------------------------------------------------------------ Q4
Q4_FX = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות הבאה:" "\n"
         r"$$f_X(x)=\begin{cases}a,&x<0\\b\,x^2,&0\le x<1\\c\,e^{-(x-1)},&x\ge 1\end{cases}$$"
         "\n" r"כאן, המקדמים $a$, $b$ ו-$c$ אינם ידועים.")

questions.append(Q(
    4, "א", "continuous_rv",
    r"בהנחה שהתוחלת $\mathbb{E}[X]=\mu$, חשבו את המקדמים $a$, $b$ ו-$c$.",
    r"""**מציאת $a,b,c$.**
צפיפות חייבת להיות אינטגרבילית ושווה בסך הכול ל-$1$. קבוע על הקטע האינסופי $(-\infty,0)$ יכול להיות אינטגרבילי רק אם
$$a=0.$$
ננרמל את הצפיפות:
$$\int_0^1bx^2\,dx+\int_1^\infty ce^{-(x-1)}\,dx=1.$$
לכן
$$\frac b3+c=1.\qquad(1)$$
נשתמש כעת בתנאי התוחלת:
$$\mu=\mathbb{E}[X]=\int_0^1x\,bx^2\,dx+\int_1^\infty x\,ce^{-(x-1)}\,dx.$$
האינטגרל הראשון הוא $b/4$. באינטגרל השני נסמן $u=x-1$, ואז $x=u+1$, ולכן
$$\int_1^\infty xce^{-(x-1)}\,dx=c\int_0^\infty(u+1)e^{-u}\,du=c(1+1)=2c.$$
לכן
$$\frac b4+2c=\mu.\qquad(2)$$
פתרון $(1)$--$(2)$ נותן
$$a=0,\qquad b=\frac{12(2-\mu)}{5},\qquad c=\frac{4\mu-3}{5}.$$""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"מהו הערך הגדול והקטן ביותר של התוחלת $\mu$?",
    r"""**הערך המקסימלי והמינימלי של $\mu$.**
צפיפות חייבת להיות אי-שלילית. לכן $b\ge 0$ ו-$c\ge 0$, ומתקבל
$$\frac{12(2-\mu)}{5}\ge 0\quad\Longrightarrow\quad\mu\le 2,$$
וכן
$$\frac{4\mu-3}{5}\ge 0\quad\Longrightarrow\quad\mu\ge\frac34.$$
לכן
$$\frac34\le\mu\le 2.$$
הערך המינימלי הוא $3/4$, והערך המקסימלי הוא $2$.""",
    5, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"מצאו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את הגרף שלה.",
    r"""**פונקציית ההתפלגות.**
עבור $t<0$,
$$F_X(t)=0.$$
עבור $0\le t<1$,
$$F_X(t)=\int_0^tbx^2\,dx=\frac b3t^3=\frac{4(2-\mu)}{5}t^3.$$
עבור $t\ge 1$,
$$\begin{aligned}F_X(t)&=\int_0^1bx^2\,dx+\int_1^tce^{-(x-1)}\,dx\\&=\frac b3+c\left(1-e^{-(t-1)}\right)\\&=1-ce^{-(t-1)}\\&=1-\frac{4\mu-3}{5}e^{-(t-1)}.\end{aligned}$$
לכן
$$F_X(t)=\begin{cases}0,&t<0,\\\dfrac{4(2-\mu)}{5}t^3,&0\le t<1,\\1-\dfrac{4\mu-3}{5}e^{-(t-1)},&t\ge 1.\end{cases}$$
שני החלקים הלא-קבועים מתחברים בנקודה
$$(1,F_X(1))=\left(1,\frac{4(2-\mu)}{5}\right).$$
השרטוט הבא מציג את צורת פונקציית ההתפלגות עבור ערך טיפוסי של $\mu$ בתחום הפנימי $3/4<\mu<2$. אם $\mu=3/4$, נקודת החיבור היא $(1,1)$; ואם $\mu=2$, נקודת החיבור היא $(1,0)$.
![גרף F_X(t) עבור μ טיפוסי: 0 עבור t<0, עלייה קובייתית על [0,1), נקודת חיבור ב-t=1 ואחר כך התקרבות אקספוננציאלית ל-1](images/exams/26A-B-Q4-cdf.png)
הגרף קבוע ושווה $0$ עבור $t<0$, עולה באופן קובייתי על $[0,1)$, עובר דרך נקודת החיבור ב-$t=1$, ולאחר מכן מתקרב ל-$1$ מלמטה באופן אקספוננציאלי עבור $t\ge 1$.""",
    5, contextId="c4"))

questions.append(Q(
    4, "ד", "continuous_rv",
    r"חשבו את ההסתברות $P(0<X<\mu/2)$.",
    r"""**חישוב $P(0<X<\mu/2)$.**
מסעיף (ב), $3/4\le\mu\le 2$, ולכן
$$0<\frac\mu2\le 1.$$
לכן ניתן לחשב את ההסתברות ישירות באמצעות פונקציית ההתפלגות:
$$\begin{aligned}P(0<X<\mu/2)&=F_X\left(\frac\mu2\right)-F_X(0)\\&=\frac{4(2-\mu)}{5}\left(\frac\mu2\right)^3-0\\&=\frac{\mu^3(2-\mu)}{10}.\end{aligned}$$
ולכן
$$P(0<X<\mu/2)=\frac{\mu^3(2-\mu)}{10}.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_A = (r"יהיו $X$ ו-$\widetilde X$ משתנים מקריים המתארים את מספר הכדורים **האדומים** ואת מספר הכדורים **השחורים** בין $n$ שנלקחו **מהכד הראשון**, בהתאמה.")
Q5_B = (r"יהי $Y$ משתנה מקרי המתאר את מספר הכדורים **האדומים** מבין $m$ שנלקחו **מהכד השני** (לאחר שהוספו אליו $n$ הכדורים מהכד הראשון).")

questions.append(Q(
    5, "א", "special_discrete",
    Q5_A + "\n" + r"**א-1:** מהי פונקציית ההסתברות של משתנה $X$? נמקו את תשובתכם היטב!",
    r"""**פונקציית ההסתברות של $X$.**
נסמן ב-$X$ את מספר הכדורים האדומים בין $n$ הכדורים שנלקחו מהכד הראשון. מאחר שהדגימה היא ללא החזרה, $X$ מתפלג היפרגיאומטרית:
$$P(X=k)=\frac{\binom{D_1}{k}\binom{N_1-D_1}{n-k}}{\binom{N_1}{n}}.$$
הערכים האפשריים הם
$$\max\{0,\,n-(N_1-D_1)\}\le k\le\min\{n,\,D_1\}.$$
באופן שקול, הנוסחה תקפה אם מפרשים מקדמים בינומיים לא חוקיים כאפס.""",
    5, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    Q5_A + "\n" + r"**א-2:** מהי פונקציית ההסתברות של משתנה $\widetilde X$? נמקו את תשובתכם היטב!",
    r"""**פונקציית ההסתברות של $\widetilde X$.**
נסמן ב-$\widetilde X$ את מספר הכדורים השחורים בין אותם $n$ כדורים שנלקחו מהכד הראשון. מאחר שכל כדור שנלקח הוא אדום או שחור,
$$\widetilde X=n-X.$$
לכן גם $\widetilde X$ מתפלג היפרגיאומטרית:
$$P(\widetilde X=r)=\frac{\binom{N_1-D_1}{r}\binom{D_1}{n-r}}{\binom{N_1}{n}}.$$
הערכים האפשריים הם
$$\max\{0,\,n-D_1\}\le r\le\min\{n,\,N_1-D_1\}.$$""",
    5, contextId="c5"))

questions.append(Q(
    5, "ג", "joint_discrete",
    Q5_A + "\n" + r"**א-3:** מהו מקדם המתאם $\rho[X,\widetilde X]$? ספקו הסבר מפורט לתוצאה.",
    r"""**מקדם המתאם $\rho[X,\widetilde X]$.**
בגלל הקשר הליניארי
$$\widetilde X=n-X,$$
בין $X$ לבין $\widetilde X$, מקבלים מיד
$$\rho[X,\widetilde X]=-1.$$""",
    5, contextId="c5"))

questions.append(Q(
    5, "ד", "conditional_bayes",
    Q5_B + "\n" + r"**ב-1:** חשבו את ההסתברות המותנית $P(Y=\ell\,/\,X=k)$.",
    r"""**ההתפלגות המותנית של $Y$ בהינתן $X=k$.**
נסמן ב-$Y$ את מספר הכדורים האדומים בין $m$ הכדורים שנלקחו מהכד השני לאחר ההעברה. בהינתן $X=k$, הועברו לכד השני בדיוק $k$ כדורים אדומים ו-$n-k$ כדורים שחורים. לכן לאחר ההעברה יש בכד השני
$$N_2+n$$
כדורים בסך הכול, ומתוכם
$$D_2+k$$
אדומים. לכן, בהינתן $X=k$, המשתנה $Y$ מתפלג היפרגיאומטרית:
$$P(Y=\ell\mid X=k)=\frac{\binom{D_2+k}{\ell}\binom{N_2+n-D_2-k}{m-\ell}}{\binom{N_2+n}{m}}.$$
גם כאן מקדמים בינומיים מחוץ לטווח החוקי מפורשים כאפס.""",
    5, contextId="c5"))

questions.append(Q(
    5, "ה", "joint_discrete",
    Q5_B + "\n" + r"**ב-2:** מצאו את פונקציית ההסתברות המשותפת $P(X=k,Y=\ell)$ של המשתנה המקרי הדו-ממדי $(X,Y)$.",
    r"""**פונקציית ההסתברות המשותפת של $(X,Y)$.**
לפי כלל הכפל,
$$P(X=k,Y=\ell)=P(X=k)\,P(Y=\ell\mid X=k).$$
לכן
$$P(X=k,Y=\ell)=\frac{\binom{D_1}{k}\binom{N_1-D_1}{n-k}}{\binom{N_1}{n}}\cdot\frac{\binom{D_2+k}{\ell}\binom{N_2+n-D_2-k}{m-\ell}}{\binom{N_2+n}{m}}.$$
הנוסחה תקפה לכל $k,\ell$ שלמים אם מקדמים בינומיים בלתי אפשריים נחשבים לאפס.""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_A = r"נתונה טבלה בגודל $4\times 3$ (סה״כ $12$ משבצות)."
Q6_B = r"נתונה כעת טבלה מלבנית בגודל $N\times M$ כאשר $N\ge 3$, $M\ge 3$."

questions.append(Q(
    6, "א", "combinatorics",
    Q6_A + "\n" + r"**(א-1):** בכמה דרכים שונות ניתן למקם **שלושה** סימני $\times$ זהים בטבלה? (אין למקם יותר מסימן אחד במשבצת!) נמקו את תשובתכם!",
    r"""**$4\times 3$: מספר הדרכים בטבלה בגודל.**
יש $12$ תאים. מאחר שהסימנים זהים ואין לשים יותר מסימן אחד בתא, מספר ההצבות הוא
$$\binom{12}{3}=220.$$""",
    5, image="images/exams/26A-B-Q6-board1.png"))

questions.append(Q(
    6, "ב", "combinatorics",
    Q6_A + "\n" + r"**(א-2):** מהי ההסתברות ששלושת הסימנים ירכיבו ״צורות-V״ המתוארות מטה?",
    r"""**$4\times 3$: ההסתברות לקבל צורת V בטבלה בגודל.**
עבור טבלה $4\times 3$, שהיא אותו מלבן כמו $3\times 4$ עד כדי סיבוב, נספור את כל צורות ה-V האפשריות.
בכל בלוק בגודל $2\times 3$ יש שתי צורות V אופקיות. מספר הבלוקים בגודל $2\times 3$ הוא
$$(3-1)(4-2)=2\cdot 2=4.$$
לכן הם תורמים
$$2\cdot 4=8$$
צורות V.
בכל בלוק בגודל $3\times 2$ יש שתי צורות V אנכיות. מספר הבלוקים בגודל $3\times 2$ הוא
$$(3-2)(4-1)=1\cdot 3=3.$$
לכן הם תורמים
$$2\cdot 3=6$$
צורות V.
לפיכך מספר ההצבות הרצויות הוא
$$8+6=14.$$
ומכאן
$$P(\mathsf V)=\frac{14}{\binom{12}{3}}=\frac{14}{220}=\frac{7}{110}.$$""",
    10, image="images/exams/26A-B-Q6-vshapes.png"))

questions.append(Q(
    6, "ג", "combinatorics",
    Q6_B + "\n" + r"**(ב-1):** בכמה דרכים שונות ניתן למקם **שלושה** סימני $\times$ זהים בטבלה? (אין למקם יותר מסימן אחד במשבצת!) נמקו את תשובתכם!",
    r"""**$M\times N$: מספר הדרכים בטבלה בגודל.**
יש $MN$ תאים. לכן מספר הדרכים הכולל למקם שלושה סימנים זהים הוא
$$\binom{MN}{3}.$$""",
    3))

questions.append(Q(
    6, "ד", "combinatorics",
    Q6_B + "\n" + r"**(ב-2):** מהי ההסתברות שהם ירכיבו ״צורות-V״ (כפי שהוגדר מעלה, בסעיף א-2)?",
    r"""**$M\times N$: ההסתברות לקבל צורת V בטבלה בגודל.**
נניח $N\ge 3$ ו-$M\ge 3$.
בכל בלוק $2\times 3$ יש שתי צורות V. מספר הבלוקים הללו הוא
$$(M-1)(N-2).$$
לכן מספר צורות ה-V האופקיות הוא
$$2(M-1)(N-2).$$
בכל בלוק $3\times 2$ יש שתי צורות V. מספר הבלוקים הללו הוא
$$(M-2)(N-1).$$
לכן מספר צורות ה-V האנכיות הוא
$$2(M-2)(N-1).$$
לכן מספר צורות ה-V הכולל הוא
$$2(M-1)(N-2)+2(M-2)(N-1).$$
ההסתברות המבוקשת היא
$$P(\mathsf V)=\frac{2(M-1)(N-2)+2(M-2)(N-1)}{\binom{MN}{3}}.$$
באופן שקול,
$$P(\mathsf V)=\frac{4MN-6M-6N+8}{\binom{MN}{3}}.$$""",
    7, image="images/exams/26A-B-Q6-vshapes.png"))

# ------------------------------------------------------------------ area regions + simulations (RAW_SCHEMA `region`, `sim`)
SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "F_D(0.3)=P(XY<=0.3)", "exact": 0.3 - 0.3 * math.log(0.3)},
    (1, "ג"): {"kind": "area", "params": {"space": {"x": [0, 1], "y": [0, 1]}, "measure": "var", "expr": "x*y"},
               "estimate": "Var[D]", "exact": 7 / 144},
}

# ---- step-author additions: sims at sample parameter values for the symbolic answers
def _geom(p, K=80):
    probs = [p * (1 - p) ** (k - 1) for k in range(1, K + 1)]
    probs[-1] += 1 - sum(probs)          # tail mass (~1e-13) goes to the last value
    return {"values": list(range(1, K + 1)), "probs": probs}


def _negbin(m, p, K=140):
    """Y = toss number of the m-th head; truncated at K (tail mass ~1e-30 for m=2, p=0.5)"""
    ks = list(range(m, K + 1))
    probs = [math.comb(k - 1, m - 1) * p ** m * (1 - p) ** (k - m) for k in ks]
    probs[-1] += 1 - sum(probs)
    return {"values": ks, "probs": probs}


def _q3_rows(p=0.3, qs=None):
    """A, C independent with P=p; B | (A,C) with the PRINTED definitions: q1=(A,C), q2=(not A,not C), q3=(A,not C), q4=(not A,C)"""
    qs = qs or {(1, 1): 0.9, (0, 0): 0.7, (1, 0): 0.5, (0, 1): 0.3}
    rows = []
    for a in (0, 1):
        for c in (0, 1):
            w = (p if a else 1 - p) * (p if c else 1 - p)
            rows.append({"p": w * qs[(a, c)], "A": a, "B": 1, "C": c})
            rows.append({"p": w * (1 - qs[(a, c)]), "A": a, "B": 0, "C": c})
    return rows


def _vshapes(R, C):
    sh = set()
    for r in range(R - 1):
        for c in range(C - 2):
            sh.add(frozenset({(r, c), (r, c + 2), (r + 1, c + 1)}))
            sh.add(frozenset({(r + 1, c), (r + 1, c + 2), (r, c + 1)}))
    for r in range(R - 2):
        for c in range(C - 1):
            sh.add(frozenset({(r, c), (r + 2, c), (r + 1, c + 1)}))
            sh.add(frozenset({(r, c + 1), (r + 2, c + 1), (r + 1, c)}))
    return sh


def _board_rows(R, C):
    """the actual random placement: every 3-subset of cells is equally likely, listed in sorted order (r1,c1)<(r2,c2)<(r3,c3).
    Whether it is a V shape is decided by the event expression over the cell coordinates (see _VEVENT)."""
    cells = [(r, c) for r in range(R) for c in range(C)]
    tot = math.comb(R * C, 3)
    rows = [{"p": 1 / tot, "r1": a[0], "c1": a[1], "r2": b[0], "c2": b[1], "r3": c[0], "c3": c[1]}
            for a, b, c in itertools.combinations(cells, 3)]
    return rows, len(_vshapes(R, C)) / tot


# V shapes in sorted-cell order: a flat arm of two cells two apart plus the middle cell of the adjacent line (rows), or a column version
_VEVENT = ("(r1 == r2 and r3 == r1 + 1 and c2 == c1 + 2 and c3 == c1 + 1) or "
           "(r2 == r3 and r2 == r1 + 1 and c2 == c1 - 1 and c3 == c1 + 1) or "
           "(c1 == c3 and abs(c2 - c1) == 1 and r2 == r1 + 1 and r3 == r1 + 2)")


def _two_urns():
    """N1=10, D1=4, n=3 into urn 2 (N2=8, D2=3), then m=2 drawn: joint (X, Y) from the two hypergeometric stages"""
    rows = []
    for k in range(0, 4):
        px = Fraction(math.comb(4, k) * math.comb(6, 3 - k), math.comb(10, 3))
        for l in range(0, 3):
            py = Fraction(math.comb(3 + k, l) * math.comb(8 - k, 2 - l), math.comb(11, 2))
            if px * py:
                rows.append({"p": float(px * py), "X": k, "Y": l})
    return rows


_BOARD34, _PV34 = _board_rows(3, 4)
_BOARD45, _PV45 = _board_rows(4, 5)
_BC = {"joint": _q3_rows()}
_IS = lambda **kw: dict(kind="custom_discrete", **kw)
SIMS.update({
    (2, "א"): _IS(params={"vars": {"T%d" % i: {"values": [0, 1], "probs": [0.7, 0.3]} for i in range(1, 6)},
                         "event": "T1 == 1 and T1+T2+T3+T4+T5 < 5"},
                  estimate="P(first tail after a head), n=5 p=0.3 (1=head)", exact=0.3 * (1 - 0.3 ** 4)),
    (2, "ב"): _IS(params={"vars": {"X": _geom(0.3)}, "event": "X % 2 == 0"}, estimate="P(X even), p=0.3", exact=0.7 / 1.7),
    (2, "ג"): _IS(params={"vars": {"Y": _negbin(2, 0.5)}, "event": "Y % 2 == 1"}, estimate="P(Y odd), m=2 p=0.5", exact=4 / 9),
    (3, "א"): _IS(params=dict(_BC, event="B == 1"), estimate="P(B), p=0.3 q=(0.9,0.7,0.5,0.3)", exact=0.592),
    (3, "ב"): _IS(params=dict(_BC, event="A == 1", given="B == 1"), estimate="P(A | B), p=0.3 q=(0.9,0.7,0.5,0.3)", exact=0.186 / 0.592),
    (3, "ג"): _IS(params=dict(_BC, event="A == 1 and B == 1 and C == 1"), estimate="P(Q1) series, p=0.3 q1=0.9", exact=0.081),
    (3, "ד"): _IS(params=dict(_BC, event="A == 1 or B == 1 or C == 1"), estimate="P(Q2) parallel, p=0.3 q2=0.7", exact=0.853),
    (4, "ד"): dict(kind="pdf", params={"pieces": [{"from": 0, "to": 1, "expr": "2.4*x^2"},
                                                   {"from": 1, "to": 40, "expr": "0.2*exp(-(x-1))"}],
                                      "event": "x > 0 and x < 0.5"},
                   estimate="P(0<X<mu/2), mu=1", exact=0.1),
    (5, "א"): dict(kind="urn", params={"counts": {"red": 4, "black": 6}, "draws": 3, "event": "red == 1"},
                   estimate="P(X=1), N1=10 D1=4 n=3", exact=0.5),
    (5, "ב"): dict(kind="urn", params={"counts": {"red": 4, "black": 6}, "draws": 3, "event": "black == 2"},
                   estimate="P(X~=2), N1=10 D1=4 n=3", exact=0.5),
    (5, "ד"): dict(kind="urn", params={"counts": {"red": 4, "black": 7}, "draws": 2, "event": "red == 1"},
                   estimate="P(Y=1 | X=1), N2=8 D2=3 n=3 m=2", exact=28 / 55),
    (5, "ה"): _IS(params={"joint": _two_urns(), "event": "X == 2 and Y == 1"},
                  estimate="P(X=2,Y=1), N1=10 D1=4 n=3 N2=8 D2=3 m=2", exact=9 / 55),
    (6, "ב"): _IS(params={"joint": _BOARD34, "event": _VEVENT}, estimate="P(V shape), 3-by-4 board", exact=_PV34),
    (6, "ד"): _IS(params={"joint": _BOARD45, "event": _VEVENT}, estimate="P(V shape), 4-by-5 board", exact=_PV45),
})

for _q in questions:
    _k = (_q["num"], _q.get("part"))
    if _k in SIMS:
        _q["sim"] = SIMS[_k]

# ---- step-author: rubric, pitfalls, guided steps. Data in steps_26A_B.py; every value is re-derived in
# tools/verify/26A-B/steps_check.py (exact + Monte Carlo).
import probsteps
from steps_26A_B import DATA as _STEPS
probsteps.apply(questions, _STEPS, CODE)

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר א׳ תשפ״ו, מועד ב (30.04.2026)",
    "year": 2026,
    "examDate": "30.04.2026",
    "sourceFile": "26A-B exam pp.1-3",
    "solutionFile": "26A-B typed official solutions (Hebrew), pp.4-15",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1", "text": Q1_LEAD},
        "c3": {"kind": "image", "title": "שאלה 3: מעגלים", "image": IMG + "Q3-circuits.png", "caption": Q3_NOTE},
        "c4": {"kind": "text", "title": "שאלה 4", "text": Q4_FX},
        "c5": {"kind": "image", "title": "שאלה 5: שני כדים", "image": IMG + "Q5-urns.png",
               "caption": (r"נתונים שני כדים: הראשון מכיל $N_1$ כדורים, מתוכם $D_1$ כדורים אדומים והיתר שחורים. "
                           r"השני מכיל $N_2$ כדורים, מתוכם $D_2$ כדורים אדומים והיתר שחורים. "
                           r"מהכד הראשון, נלקחו באקראי וללא החזרה $n$ כדורים והוספו לכד השני. "
                           r"לאחר מכן, מהכד השני נלקחו באקראי וללא החזרה $m$ כדורים.")},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
