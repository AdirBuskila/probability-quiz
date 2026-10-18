# -*- coding: utf-8 -*-
"""Generator for tools/raw/24S-A.json -- probability (course 20021), semester C 2024, moed A (14.10.2024).
6 questions, 21 items (Q1 3, Q2 4, Q3 4, Q4 3, Q5 3, Q6 4), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24S-A.py

Source: exam pp.1-3, handwritten official solutions pp.4-13 (grid paper).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, b, stored as a b c. Map: Q1 a=א-1, b=א-2 (it asks two
  probabilities for 14 points, kept as ONE item), c=ב; Q2 a=א, b=ב, c=ג-1, d=ג-2.
- Q1 area items carry `region` (area figure) and, with the other numeric parts, `sim`: see EXTRAS near the end.
- Q5: the official solution takes Q = 1/365 (probability of a birthday on the exam date); the question text does not
  state it. The solution page also offers an alternative solution without the hint, transcribed below the main one.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24S-A.json"
CODE = "24S-A"
IMG = "images/exams/24S-A-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_LEAD = r"לפניך ריבוע בעל שטח $1$ (צלע באורך $1$)."

questions.append(Q(
    1, "א", "uniform_geometric",
    r"שתי נקודות $A$ ו-$B$ נבחרו **באקראי** על צלעות **סמוכות** כמשורטט באיור (העליון)." "\n" r"**א-1:** נאפיין את מיקומן של הנקודות $A$ ו-$B$ באמצעות משתנים מקריים רציפים $X$ ו-$Y$. איך משתנים אלה מפולגים?",
    r"""הנקודות $A$ ו-$B$ נבחרו באקראי על צלעות באורך $1$. לכן
$$X\sim U_c(0,1)\quad\text{and}\quad Y\sim U_c(0,1).$$""",
    4, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"שתי נקודות $A$ ו-$B$ נבחרו **באקראי** על צלעות **סמוכות** כמשורטט באיור (העליון)." "\n" r"**א-2:** יהי $L$ אורך הקטע $|AB|$. מצאו את ההסתברויות $P(L<1)$ ו-$P(1/2<L<1)$.",
    r"""לפי משפט פיתגורס
$$L=\sqrt{X^2+Y^2}.$$
נשתמש בגישה הגאומטרית: $\Omega=\{0<x<1,\ 0<y<1\}$ הוא ריבוע היחידה, $|\Omega|=1$.
$$P(L<1)=P(X^2+Y^2<1)=\frac{|\{x^2+y^2<1\}|}{|\Omega|}.$$
האזור $\{x^2+y^2<1\}$ בתוך הריבוע הוא רבע עיגול ברדיוס $1$, ושטחו $\frac\pi4$:
$$P(L<1)=\frac{\pi/4}{1}=\frac\pi4\approx0.79.$$
$$P(\tfrac12<L<1)=P(\tfrac14<X^2+Y^2<1)=\frac\pi4-\frac\pi4\cdot\frac14=\frac{3\pi}{16}\approx0.59.$$
(מרבע העיגול ברדיוס $1$ מורידים את רבע העיגול ברדיוס $\frac12$, ששטחו $\frac\pi4\cdot\frac14$.)""",
    14, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"הפעם שתי נקודות $A$ ו-$B$ נבחרו **באקראי** על צלעות **מקבילות** כמשורטט באיור (התחתון)." "\n" r"**ב:** יהי $L$ אורך הקטע $|AB|$. מצאו את ההסתברות $P(L<\sqrt{10}/3)$.",
    r"""לפי משפט פיתגורס, כאשר ההפרש בין שתי הנקודות לאורך הצלעות הוא $x-y$ והמרחק בין הצלעות הוא $1$:
$$L=\sqrt{1+(x-y)^2}.$$
$$P(L<\tfrac{\sqrt{10}}3)=P\left(1+(X-Y)^2<\tfrac{10}9\right)=P\left((X-Y)^2<\tfrac19\right)=P\left(|X-Y|<\tfrac13\right)=\frac{|\{|x-y|<\frac13\}|}{|\Omega|}.$$
האזור $\{|x-y|<\frac13\}$ הוא רצועה סביב האלכסון $y=x$ בתוך ריבוע היחידה. שטחו הוא שטח הריבוע פחות שני משולשי פינה שניצביהם $\frac23$:
$$|\{|x-y|<\tfrac13\}|=1-2\cdot\frac12\left(\frac23\right)^2=\frac59.$$
לכן
$$P(L<\tfrac{\sqrt{10}}3)=\frac59.$$""",
    7, contextId="c1"))

# ------------------------------------------------------------------ Q2
questions.append(Q(
    2, "א", "combinatorics",
    r"מטילים קובייה מאוזנת **פעם אחר פעם** ומסכמים את התוצאות. מהי ההסתברות שסכום התוצאות **אי פעם** יהיה שווה ל-5?",
    r"""נסמן $A=\{$סכום התוצאות אי פעם יהיה שווה ל-5$\}$. הסכום מגיע ל-5 בדיוק כאשר סדרת ההטלות הראשונות היא פירוק של 5 לסכום של מספרים מ-1 עד 6 (הסדר חשוב):
הטלה אחת: $\{5\}$ - הסתברות $\frac16$.
שתי הטלות: $14,41,23,32$ - הסתברות $4\left(\frac16\right)^2$.
שלוש הטלות: $113,131,311,122,212,221$ - הסתברות $6\left(\frac16\right)^3$.
ארבע הטלות: $1112,1121,1211,2111$ - הסתברות $4\left(\frac16\right)^4$.
חמש הטלות: $11111$ - הסתברות $\left(\frac16\right)^5$.
לכן
$$P(A)=\frac16+4\left(\frac16\right)^2+6\left(\frac16\right)^3+4\left(\frac16\right)^4+\left(\frac16\right)^5=\frac16\left(\frac76\right)^4=\frac{7^4}{6^5}\approx0.31.$$""",
    7))

questions.append(Q(
    2, "ב", "combinatorics",
    r"מטילים קובייה מאוזנת **פעמיים** ומסכמים את התוצאות. מהי ההסתברות שסכום התוצאות יהיה שווה ל-5?",
    r"""נסמן $B=\{$סכום שתי התוצאות שווה ל-5$\}=\{14,23,32,41\}$. לכן
$$P(B)=4\left(\frac16\right)^2=\frac4{36}=\frac19.$$""",
    6))

questions.append(Q(
    2, "ג", "combinatorics",
    r"מטילים קובייה מאוזנת **שלוש פעמים** ומסכמים את התוצאות." "\n" r"**ג-1:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-5?",
    r"""נסמן $C=\{$סכום שלוש התוצאות שווה ל-5$\}=\{113,131,311,122,212,221\}$. לכן
$$P(C)=6\left(\frac16\right)^3=\frac1{36}.$$""",
    6))

questions.append(Q(
    2, "ד", "conditional_bayes",
    r"מטילים קובייה מאוזנת **שלוש פעמים** ומסכמים את התוצאות." "\n" r"**ג-2:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-5 **אם ידוע** כי סכום של שתי התוצאות הראשונות היה שווה ל-3?",
    r"""נסמן $C=\{$סכום שלוש התוצאות שווה ל-5$\}$ ו-$D=\{$סכום שתי התוצאות הראשונות שווה ל-3$\}=\{12\ast,21\ast\}$ (התוצאה השלישית חופשית). אז $C\cap D=\{122,212\}$ ולכן
$$P(C\mid D)=\frac{P(C\cap D)}{P(D)}=\frac{P(\{122,212\})}{P(\{12\ast,21\ast\})}=\frac{2\left(\frac16\right)^3}{2\left(\frac16\right)^2}=\frac16.$$""",
    6))

# ------------------------------------------------------------------ Q3
Q3_LEAD = (r"מטילים מטבע מוטה **שלוש** פעמים; ההסתברות לתוצאת ״עץ״ הינה $P(H)=p$. נגדיר שני משתנים מקריים: "
           r"$X=\{$מספר תוצאות ״עץ״ בשתי ההטלות הראשונות$\}$ ו-$Y=\{$מספר תוצאות ״עץ״ בשתי ההטלות האחרונות$\}$.")

questions.append(Q(
    3, "א", "joint_discrete",
    r"מצאו את פונקציית ההסתברות המשותפת $P_{XY}(x,y)$ וודאו כי תכונת הנרמול מתקיימת.",
    r"""נגדיר $X_1,X_2,X_3\sim\mathrm{Ber}(p)$ בלתי תלויים (תוצאות שלוש ההטלות; $1$ = ״עץ״). אז $X=X_1+X_2$ ו-$Y=X_2+X_3$.
נמנה את שמונה התוצאות האפשריות:
$$\begin{array}{c|cccccccc}X_1&0&1&0&0&1&1&0&1\\ \hline X_2&0&0&1&0&1&0&1&1\\ \hline X_3&0&0&0&1&0&1&1&1\\ \hline X&0&1&1&0&2&1&1&2\\ \hline Y&0&0&1&1&1&1&2&2\end{array}$$
ההסתברות המשותפת:
$$\begin{array}{c|ccc|c}x\backslash y&0&1&2&P_X(x)\\ \hline 0&(1-p)^3&p(1-p)^2&0&(1-p)^2\\ 1&p(1-p)^2&p(1-p)&p^2(1-p)&2p(1-p)\\ 2&0&p^2(1-p)&p^3&p^2\\ \hline P_Y(y)&(1-p)^2&2p(1-p)&p^2&1\end{array}$$
(במשבצת $(1,1)$ מופיעים שני המקרים $(1,0,1)$ ו-$(0,1,0)$: $p^2(1-p)+p(1-p)^2=p(1-p)$.) סכום כל המשבצות הוא $1$, ולכן תכונת הנרמול מתקיימת.""",
    11, contextId="c3"))

questions.append(Q(
    3, "ב", "joint_discrete",
    r"מצאו את פונקציות ההתפלגות השוליות $P_X(x)$ ו-$P_Y(y)$.",
    r"""לפי משפט הפירוק, $X=X_1+X_2$ ו-$Y=X_2+X_3$ הם סכומים של שני ברנולי בלתי תלויים:
$$X\sim\mathrm{Bin}(2,p),\qquad Y\sim\mathrm{Bin}(2,p).$$
כלומר $P_X(x)=P_Y(x)=\binom2xp^x(1-p)^{2-x}$, $x=0,1,2$: $(1-p)^2,\ 2p(1-p),\ p^2$ (כפי שמופיע בשולי הטבלה).""",
    6, contextId="c3"))

questions.append(Q(
    3, "ג", "discrete_rv",
    r"חשבו את התוחלות $\mathbb{E}[X]$, $\mathbb{E}[Y]$ והשונויות $\operatorname{var}[X]$, $\operatorname{var}[Y]$.",
    r"""מאחר ש-$X,Y\sim\mathrm{Bin}(2,p)$:
$$\mathbb{E}[X]=\mathbb{E}[Y]=2p,\qquad \operatorname{Var}[X]=\operatorname{Var}[Y]=2p(1-p).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ד", "independence",
    r"האם $X$ ו-$Y$ הם משתנים מקריים בלתי תלויים? נמקו והסבירו!",
    r"""**לא, המשתנים תלויים.** אילו היו בלתי תלויים היה מתקיים $P_{XY}(x,y)=P_X(x)P_Y(y)$ לכל $(x,y)$. אבל ב-$(x,y)=(2,0)$ מתקיים $P_{XY}(2,0)=0$ (שתי ההטלות הראשונות ״עץ״ ושתי האחרונות לא, בלתי אפשרי כי ההטלה האמצעית משותפת), בעוד $P_X(2)P_Y(0)=p^2(1-p)^2>0$ עבור $0<p<1$.""",
    4, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_FX = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות מהצורה:" "\n"
         r"$$f_X(x)=\begin{cases}0,&x<-1\\a,&-1\le x<0\\b\,e^{-x},&x\ge0\end{cases}$$")

questions.append(Q(
    4, "א", "continuous_rv",
    r"**א:** בהנחה כי $\mathbb{E}[X]=0$, מצאו את הפרמטרים $a$ ו-$b$.",
    r"""**נרמול.**
$$a+\int_0^\infty be^{-x}\,dx=1\ \Longrightarrow\ a+b=1.$$
**תוחלת.**
$$\mathbb{E}[X]=a\int_{-1}^0x\,dx+b\int_0^\infty xe^{-x}\,dx=-\frac a2+b=0.$$
מ-$a+b=1$ ו-$b-\frac a2=0$ מתקבל
$$a=\frac23,\qquad b=\frac13.$$""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"**ב:** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את התוצאה.",
    r"""$$F_X(t)=\int_{-\infty}^tf_X(x)\,dx=\begin{cases}0,&t<-1,\\ \frac23(t+1),&-1\le t<0,\\ \frac23+\frac13\int_0^te^{-x}dx=1-\frac13e^{-t},&t\ge0.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת F_X(t)](images/exams/24S-A-Q4-cdf.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"**ג:** מהי ההסתברות המותנית $P(X>-1/2\ /\ X<1)$?",
    r"""$$P\left(X>-\tfrac12\ \Big|\ X<1\right)=\frac{P(-\frac12<X<1)}{P(X<1)}=\frac{F_X(1)-F_X(-\frac12)}{F_X(1)}=1-\frac{F_X(-\frac12)}{F_X(1)}.$$
$F_X(-\frac12)=\frac13$ ו-$F_X(1)=1-\frac1{3e}$, לכן
$$=1-\frac{1/3}{1-\frac1{3e}}=\frac{2e-1}{3e-1}\approx0.62.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_LEAD = (r"למבחן סוף הקורס ב״הסתברות״ אשר מתקיים **היום** נרשמו $N$ סטודנטים. בגלל סיבות שונות ומשונות, "
           r"כל אחד מהסטודנטים מחליט להגיע למבחן בהסתברות $p$.")
Q5_HINT = (r"**הערה:** לידיעתך,"
           "\n" r"$$\sum_{j=m}^{N}C_j^mC_N^ja^j=C_N^ma^m(1+a)^{N-m}$$"
           "\n" r"(יכול להיות שאין צורך להשתמש בנוסחה זו).")

questions.append(Q(
    5, "א", "special_discrete",
    r"**א:** יהי $X$ משתנה מקרי המתאר את מספר הסטודנטים אשר הגיעו למבחן. איך משתנה זה מפולג? **עליך לתת הסבר מפורט.**",
    r"""כל אחד מ-$N$ הסטודנטים מחליט באופן בלתי תלוי להגיע בהסתברות $p$, ולכן $X$ סופר הצלחות ב-$N$ ניסויי ברנולי בלתי תלויים בעלי אותה הסתברות הצלחה:
$$X\sim\mathrm{Bin}(N,p),\qquad P(X=j)=\binom Njp^j(1-p)^{N-j},\quad j=0,1,\ldots,N.$$""",
    5, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    r"**ב:** יהי $Y$ משתנה מקרי המתאר את מספר הסטודנטים – **מתוך אלה שהגיעו למבחן** – אשר נולדו **היום** (כלומר, בתאריך המבחן). מצאו את פונקציית ההסתברות של משתנה זה." "\n" + Q5_HINT,
    r"""**פתרון בעזרת ההערה.** נסמן ב-$Q=\frac1{365}$ את ההסתברות שסטודנט נולד בתאריך המבחן. בהינתן ש-$j$ סטודנטים הגיעו, ההסתברות שבדיוק $k$ מהם נולדו בתאריך המבחן היא $\binom jkQ^k(1-Q)^{j-k}$. לפי נוסחת ההסתברות השלמה:
$$P(Y=k)=\sum_{j=k}^{N}P(Y=k\mid X=j)P(X=j)=\sum_{j=k}^{N}\binom jkQ^k(1-Q)^{j-k}\binom Njp^j(1-p)^{N-j}$$
$$=\frac{Q^k}{(1-Q)^k}(1-p)^N\sum_{j=k}^{N}\binom jk\binom Nj\left(\frac{p}{1-p}(1-Q)\right)^j.\qquad(*)$$
הסכום הוא בדיוק הסכום שבהערה עם $m=k$ ו-$a=\frac p{1-p}(1-Q)$. אז $1+a=\frac{1-pQ}{1-p}$ ו
$$\sum_{j=k}^{N}\binom jk\binom Nja^j=\binom Nk\frac{(1-pQ)^{N-k}p^k(1-Q)^k}{(1-p)^N}.$$
הצבה חזרה ב-$(*)$ נותנת
$$P(Y=k)=\binom Nk(pQ)^k(1-pQ)^{N-k},\qquad k=0,1,\ldots,N.$$

**פתרון חלופי, ללא שימוש בהערה.** נאפיין כל אחד מ-$N$ הסטודנטים על ידי זוג משתני ברנולי בלתי תלויים: $X_j=1$ (בהסתברות $p$) אם הגיע למבחן, ו-$\tilde X_j=1$ (בהסתברות $Q$) אם נולד בתאריך המבחן. כדי לספור את מי שהגיע וגם נולד בתאריך הנדרש, נשתמש במשתנה ברנולי $Y_j=X_j\tilde X_j$:
$$Y_j=\begin{cases}1,&pQ\ (\text{arrived and born on the exam date})\\0,&\text{else}\end{cases}\sim\mathrm{Ber}(pQ).$$
ולכן, לפי משפט הפירוק,
$$Y=\sum_{j=1}^NY_j\sim\mathrm{Bin}(N,pQ).$$""",
    15, contextId="c5"))

questions.append(Q(
    5, "ג", "conditional_bayes",
    r"**ג:** אם ידוע כי בין כל הסטודנטים שהגיעו למבחן בדיוק $k$ נולדו בתאריך המבחן, מהי ההסתברות שבדיוק $n$ סטודנטים הגיעו למבחן?",
    r"""לפי נוסחת בייס:
$$P(X=n\mid Y=k)=\frac{P(Y=k\mid X=n)P(X=n)}{P(Y=k)}=\frac{\binom nkQ^k(1-Q)^{n-k}\cdot\binom Nnp^n(1-p)^{N-n}}{\binom Nk(pQ)^k(1-pQ)^{N-k}}.$$
לאחר הצבה ופישוט (באמצעות $\binom nk\binom Nn=\binom Nk\binom{N-k}{n-k}$) מתקבל
$$P(X=n\mid Y=k)=\binom{N-k}{N-n}\tilde p^{\,N-n}(1-\tilde p)^{(N-k)-(N-n)},\qquad\tilde p=\frac{1-p}{1-pQ}.$$""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_LEAD = (r"מעגל חשמלי מורכב משש יחידות כמתואר באיור. כל היחידות פועלות בהסתברויות זהות $P(A)=\cdots=P(F)=p$ וללא תלות זו בזו. "
           r"המעגל הוא גרף על ארבע צמתים: צומת שמאלי (כניסה) וצומת ימני (יציאה), צומת עליון וצומת מרכזי. "
           r"$A$ מחברת בין השמאלי לעליון, $C$ בין העליון לימני, $B$ בין העליון למרכזי, $D$ בין השמאלי למרכזי, $E$ בין המרכזי לימני, ו-$F$ בין השמאלי לימני.")
Q6_PQ = r"p\,(1+2p-7p^3+7p^4-2p^5)"

questions.append(Q(
    6, "א", "circuits",
    r"**א:** מהי ההסתברות שמעגל כולו פועל?",
    r"""נסמן $Q=\{$המעגל כולו פועל$\}$ ונפצל לפי היחידה $B$:
$$P(Q)=P(Q\mid B)P(B)+P(Q\mid\bar B)P(\bar B).$$
**$B$ פועלת** (הצומת העליון והמרכזי מחוברים): מתקבל ($A$ במקביל ל-$D$) בטור עם ($C$ במקביל ל-$E$), הכול במקביל ל-$F$:
$$P(Q\mid B)=p+(2p-p^2)^2-p(2p-p^2)^2=p+4p^2-8p^3+5p^4-p^5.$$
**$B$ אינה פועלת:** מתקבל ($A$ בטור $C$) במקביל ל-($D$ בטור $E$), הכול במקביל ל-$F$:
$$P(Q\mid\bar B)=p+(2p^2-p^4)-p(2p^2-p^4)=p+2p^2-2p^3-p^4+p^5.$$
לכן
$$P(Q)=p\,(1+2p-7p^3+7p^4-2p^5).$$""",
    10, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"**ב:** אם ידוע כי מעגל כולו פועל, מהי ההסתברות שיחידה $B$ **לא** פועלת?",
    r"""לפי נוסחת בייס:
$$P(\bar B\mid Q)=\frac{P(Q\mid\bar B)P(\bar B)}{P(Q)}=\frac{(1+2p-2p^2-p^3+p^4)(1-p)}{1+2p-7p^3+7p^4-2p^5}=\frac{1+p-4p^2+p^3+2p^4-p^5}{1+2p-7p^3+7p^4-2p^5}.$$""",
    5, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    r"**ג:** אם ידוע כי **בדיוק יחידה אחת לא** פועלת (ולא ידוע איזו יחידה בדיוק!), מהי ההסתברות שהמעגל כולו כן פועל?",
    r"""אם בדיוק יחידה אחת אינה פועלת, חמש היחידות האחרות פועלות. כדי שהמעגל יפסיק לפעול צריכים להיכשל לפחות שני רכיבים (כל חתך מינימלי של המעגל הוא בגודל לפחות 2), ולכן כשרק רכיב אחד נכשל המעגל תמיד פועל:
$$P(Q\mid\text{exactly one unit fails})=1.$$""",
    5, contextId="c6"))

questions.append(Q(
    6, "ד", "circuits",
    r"**ד:** אם ידוע כי מעגל כולו פועל, מהי ההסתברות שכל היחידות פועלות?",
    r"""$$P(A\cap B\cap C\cap D\cap E\cap F\mid Q)=\frac{P(Q\mid A\cap\cdots\cap F)\,P(A\cap\cdots\cap F)}{P(Q)}=\frac{1\cdot p^6}{p\,(1+2p-7p^3+7p^4-2p^5)}=\frac{p^5}{1+2p-7p^3+7p^4-2p^5}.$$""",
    5, contextId="c6"))

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר ג׳ תשפ״ד, מועד א (14.10.2024)",
    "year": 2024,
    "examDate": "14.10.2024",
    "sourceFile": "24S-A exam pp.1-3",
    "solutionFile": "24S-A official handwritten solutions pp.4-13",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: שתי נקודות על צלעות הריבוע", "image": IMG + "Q1-squares.png", "caption": Q1_LEAD},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_LEAD},
        "c4": {"kind": "text", "title": "שאלה 4", "text": Q4_FX},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_LEAD},
        "c6": {"kind": "image", "title": "שאלה 6: מעגל חשמלי", "image": IMG + "Q6-circuit.png", "caption": Q6_LEAD},
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
    (1, "ב"): {
        "region": [REG([{"expr": "x^2+y^2", "op": "<", "c": 1}], pi / 4, "האירוע L<1: רבע עיגול ברדיוס 1"),
                   REG([{"expr": "x^2+y^2", "op": ">", "c": "1/4"}, {"expr": "x^2+y^2", "op": "<", "c": 1}], 3 * pi / 16,
                       "האירוע 1/2<L<1: טבעת רבע עיגול")],
        "sim": AREA("P(1/2<L<1)", 3 * pi / 16, space=U, event="x^2+y^2 > 1/4 and x^2+y^2 < 1")},
    (1, "ג"): {
        "region": REG([lin(1, -1, "1/3", "<"), lin(1, -1, "-1/3", ">")], 5 / 9, "האירוע |X-Y|<1/3 (רצועה סביב האלכסון)"),
        "sim": AREA("P(L<sqrt(10)/3)", 5 / 9)},
    (2, "א"): {"sim": DICE("P(sum ever = 5)", 7 ** 4 / 6 ** 5, 5,
                           "d1 == 5 or d1+d2 == 5 or d1+d2+d3 == 5 or d1+d2+d3+d4 == 5 or d1+d2+d3+d4+d5 == 5")},
    (2, "ב"): {"sim": DICE("P(sum = 5)", 1 / 9, 2, "sum == 5")},
    (2, "ג"): {"sim": DICE("P(sum = 5)", 1 / 36, 3, "sum == 5")},
    (2, "ד"): {"sim": DICE("P(sum = 5 | d1+d2 = 3)", 1 / 6, 3, "sum == 5", "d1+d2 == 3")},
    (4, "ג"): {"sim": PDF("P(X>-1/2 | X<1)", (2 * _E - 1) / (3 * _E - 1),
                          [(-1, 0, "2/3"), (0, 30, "1/3*exp(-x)")], "x > -1/2", "x < 1")},
}
for _q in questions:
    _x = EXTRAS.get((_q["num"], _q.get("part")))
    if _x:
        _q.update(_x)


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
