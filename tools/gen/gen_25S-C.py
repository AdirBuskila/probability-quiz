# -*- coding: utf-8 -*-
"""Generator for tools/raw/25S-C.json -- probability (course 20021), summer 2025, moed C (11.12.2025; the file name of the
source says 11.12.2025 and the exam header agrees). Choose 4 of 6 questions, 25 points each. 22 items
(Q1 4, Q2 4, Q3 5, Q4 3, Q5 3, Q6 3).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25S-C.py

Source: exam pp.1-3 (pdf), handwritten official solutions on grid paper pp.4-14 (no text layer; rendered and read).

Transcription notes
- Part keys: single letters. Q1 prints "א-1", "א-2", "ב", "ג"; stored a b c d (the printed label is the first bold token of
  the question text). Q5 prints "א", "ב-1", "ב-2"; stored a b c, same convention.
- The handwritten solutions are terse; they are transcribed into Hebrew prose, no new results added. Circuit diagrams that
  the solution redraws for each conditioning case are described in words.
- Q6 part ג: the official solution concludes E[Y] >= E[X]; strictness follows from the printed condition that the
  n_i are all different (variance > 0), which is added as a remark.
- Q1 region data and the sim specs live in the REGIONS / SIMS blocks above the exam dict.
- The page-1 cover (lecturer names) is not copied anywhere.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25S-C.json"
CODE = "25S-C"
IMG = "images/exams/25S-C-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_CAP = (r"במשולש שווה שוקיים אורך הבסיס $b$ והיקף המשולש $L$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגות אחידה: "
          r"$b\sim U_c(0,1)$ ו-$L\sim U_c(1,2)$. נסמן ב-$a$ את אורך כל אחת משתי השוקיים.")

Q1_SETUP = r"""מכיוון ש-$L=2a+b$, מתקבל
$$a=\frac{L-b}{2}.$$
מרחב המדגם הוא הריבוע $\Omega=\{(b,L):0<b<1,\ 1<L<2\}$, ושטחו $|\Omega|=1$, כך שהסתברות שווה לשטח האזור."""

questions.append(Q(
    1, "א", "uniform_geometric",
    r"חשבו את ההסתברויות הבאות: **א-1:** $P(a<1/4)$.",
    r"""**$P(a<\frac14)$.**
""" + Q1_SETUP + r"""
$$P\left(a<\frac14\right)=P\left(\frac{L-b}{2}\le\frac14\right)=P\left(L\le b+\frac12\right)=\frac{\left|\{L\le b+\frac12\}\right|}{|\Omega|},\qquad |\Omega|=1.$$
הישר $L=b+\frac12$ חותך את הריבוע במשולש קטן בפינה הימנית התחתונה, שבו שני הניצבים שווים ל-$\frac12$ (הישר נכנס לריבוע ב-$L=1$ כאשר $b=\frac12$, ויוצא ב-$b=1$ בגובה $L=\frac32$).
![האזור L ≤ b + 1/2 בתוך הריבוע b בין 0 ל-1, L בין 1 ל-2](images/exams/25S-C-Q1a-region.png)
$$\left|\{L\le b+\tfrac12\}\right|=\frac12\cdot\frac12\cdot\frac12=\frac18,\qquad P\left(a<\frac14\right)=\frac18.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"חשבו את ההסתברויות הבאות: **א-2:** $P(a<2/3)$.",
    r"""**$P(a<\frac23)$.**
""" + Q1_SETUP + r"""
$$P\left(a<\frac23\right)=P\left(\frac{L-b}{2}\le\frac23\right)=P\left(L\le b+\frac43\right)=\frac{\left|\{L\le b+\frac43\}\right|}{|\Omega|},\qquad |\Omega|=1.$$
הישר $L=b+\frac43$ חותך את הצלע העליונה $L=2$ ב-$b=\frac23$, כך שהאזור שמעליו הוא משולש קטן בפינה השמאלית העליונה עם ניצבים $\frac23$.
![האזור L ≤ b + 4/3 בתוך הריבוע](images/exams/25S-C-Q1b-region.png)
$$\left|\{L\le b+\tfrac43\}\right|=1-\frac12\left(\frac23\right)^2=\frac79,\qquad P\left(a<\frac23\right)=\frac79.$$""",
    7, contextId="c1"))

questions.append(Q(
    1, "ג", "continuous_rv",
    r"**ב:** מצאו תוחלת $\mathbb{E}[a]$ ושונות $\operatorname{var}[a]$.",
    r"""**תוחלת ושונות של $a$.**
$$\mathbb{E}[a]=\mathbb{E}\left[\frac{L-b}{2}\right]=\frac12\Bigl(\mathbb{E}[L]-\mathbb{E}[b]\Bigr)=\frac12\left\{\frac32-\frac12\right\}=\frac12,$$
כאשר $\mathbb{E}[L]=\frac{1+2}{2}=\frac32$ ו-$\mathbb{E}[b]=\frac{0+1}{2}=\frac12$.
לשונות:
$$\operatorname{Var}[a]=\mathbb{E}[a^2]-\bigl(\mathbb{E}[a]\bigr)^2=\mathbb{E}[a^2]-\frac14.$$
$$\mathbb{E}[a^2]=\mathbb{E}\left[\left(\frac{L-b}{2}\right)^2\right]=\frac14\,\mathbb{E}\bigl[L^2-2Lb+b^2\bigr]=\frac14\Bigl\{\mathbb{E}[L^2]+\mathbb{E}[b^2]-2\,\mathbb{E}[b]\,\mathbb{E}[L]\Bigr\},$$
כאשר השתמשנו באי-תלות של $b,L$ בחישוב $\mathbb{E}[Lb]$. הרגעים השניים:
$$\mathbb{E}[L^2]=\operatorname{Var}[L]+\bigl(\mathbb{E}[L]\bigr)^2=\frac{(2-1)^2}{12}+\left(\frac32\right)^2=\frac1{12}+\frac94=\frac{28}{12}=\frac73,$$
$$\mathbb{E}[b^2]=\operatorname{Var}[b]+\bigl(\mathbb{E}[b]\bigr)^2=\frac{(1-0)^2}{12}+\left(\frac12\right)^2=\frac1{12}+\frac14=\frac13.$$
לכן
$$\mathbb{E}[a^2]=\frac14\left\{\frac73+\frac13-2\cdot\frac12\cdot\frac32\right\}=\frac7{24},$$
ולכן
$$\operatorname{Var}[a]=\frac7{24}-\frac14=\frac1{24}.$$""",
    8, contextId="c1"))

questions.append(Q(
    1, "ד", "continuous_rv",
    r"**ג:** חשבו שונות משותפת $\operatorname{cov}[a,b]=\mathbb{E}[ab]-\mathbb{E}[a]\,\mathbb{E}[b]$. האם המשתנים $a$ ו-$b$ מתואמים או בלתי מתואמים?",
    r"""**$\operatorname{cov}[a,b]$.**
$$\operatorname{Cov}[a,b]=\mathbb{E}[ab]-\mathbb{E}[a]\,\mathbb{E}[b]=\mathbb{E}[ab]-\frac12\cdot\frac12=\mathbb{E}[ab]-\frac14.$$
$$\mathbb{E}[ab]=\mathbb{E}\left[\frac{L-b}{2}\,b\right]=\frac12\Bigl\{\mathbb{E}[L]\,\mathbb{E}[b]-\mathbb{E}[b^2]\Bigr\}=\frac12\left\{\frac32\cdot\frac12-\frac13\right\}=\frac5{24}.$$
לכן
$$\operatorname{Cov}[a,b]=\frac5{24}-\frac14=-\frac1{24}\ne0.$$
המשתנים $a$ ו-$b$ מתואמים.""",
    3, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_CAP = (r"מרכיבים מספר דו ספרתי באופן הבא: מאוסף הספרות $\{1,2,3,4,5,6,7,8,9\}$ מוצאים באקראי **וללא החזרה** שתי ספרות. "
          r"הספרה הראשונה שנבחרה הינה ספרת העשרות של המספר; הספרה השנייה שנבחרה הינה ספרת האחדות.")

Q2_SETUP = r"נסמן ב-$X$ את ספרת העשרות וב-$Y$ את ספרת האחדות. מרחב המדגם הוא כל הזוגות הסדורים של ספרות שונות, ולכן $|\Omega|=9\cdot8=72$ (כל הזוגות שווי הסתברות)."

questions.append(Q(
    2, "א", "combinatorics",
    r"מהי ההסתברות שהמספר שהורכב הינו מספר אי זוגי?",
    r"""**המספר אי-זוגי.**
""" + Q2_SETUP + r"""
המספר אי-זוגי אם ספרת האחדות אי-זוגית: $5$ אפשרויות לספרת האחדות ($1,3,5,7,9$), ולספרת העשרות נותרו $8$ ספרות. לכן $|\{\cdots\}|=40$ ו-
$$P=\frac{40}{72}=\frac59.$$""",
    7, contextId="c2"))

questions.append(Q(
    2, "ב", "combinatorics",
    r"מהי ההסתברות שהמספר שהורכב מתחלק ב-3 ללא שארית?",
    r"""**המספר מתחלק ב-3.**
המספר מתחלק ב-$3$ אם ורק אם סכום ספרותיו מתחלק ב-$3$. נחלק את הספרות לפי שארית בחלוקה ב-$3$: שארית $0$: $\{3,6,9\}$; שארית $1$: $\{1,4,7\}$; שארית $2$: $\{2,5,8\}$. סכום מתחלק ב-$3$ כאשר שתי הספרות בשארית $0$ ($3\cdot2=6$ זוגות סדורים), או שאחת בשארית $1$ והשנייה בשארית $2$ ($3\cdot3\cdot2=18$ זוגות סדורים). סך הכול $24=2\cdot12$ זוגות, ו-$|\Omega|=72$:
$$P=\frac{24}{72}=\frac13.$$""",
    7, contextId="c2"))

questions.append(Q(
    2, "ג", "combinatorics",
    r"מהי ההסתברות שהמספר שהורכב מתחלק ב-5 ללא שארית?",
    r"""**המספר מתחלק ב-5.**
מספר מתחלק ב-$5$ אם ספרת האחדות היא $5$ (אין $0$ באוסף). ספרת האחדות $5$, ולספרת העשרות $8$ אפשרויות, ולכן
$$P=\frac8{72}=\frac19.$$""",
    7, contextId="c2"))

questions.append(Q(
    2, "ד", "conditional_bayes",
    r"אם ידוע כי סכום הספרות מהווה מספר זוגי, מהי ההסתברות שהמספר עצמו הוא כן אי זוגי?",
    r"""**בהינתן סכום ספרות זוגי, המספר אי-זוגי.**
$$P(\text{odd}\mid X+Y\text{ even})=\frac{P(\text{odd}\cap X+Y\text{ even})}{P(X+Y\text{ even})}=\frac{\left|\{\text{odd}\cap X+Y\text{ even}\}\right|}{\left|\{X+Y\text{ even}\}\right|}=\frac{20}{32}=\frac58.$$
הסבר הספירה: סכום זוגי פירושו ששתי הספרות באותה זוגיות: שתיהן אי-זוגיות ($5\cdot4=20$ זוגות) או שתיהן זוגיות ($4\cdot3=12$ זוגות), סך הכול $32$. המספר אי-זוגי בדיוק כשספרת האחדות אי-זוגית, כלומר בכל $20$ הזוגות שבהם שתיהן אי-זוגיות.""",
    4, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_CAP = (r"נתונה מטריצת ברנולי מהצורה" "\n"
          r"$$\boldsymbol{Q}=\begin{pmatrix}XY&-X\\Y&X+Y-XY\end{pmatrix},$$"
          "\n" r"כאשר $X$ ו-$Y$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגויות ברנולי: $X\sim\mathrm{Ber}(p)$ ו-$Y\sim\mathrm{Ber}(p)$. "
          r"נגדיר שני משתנים מקריים חדשים: דטרמיננטה $D=\det\boldsymbol{Q}$ ועקבה $T=\operatorname{tr}\boldsymbol{Q}$ של מטריצה $\boldsymbol{Q}$.")

Q3_REDUCE = r"""**פישוט $D$ ו-$T$.**
כאשר $X,Y\sim\mathrm{Ber}(p)$ מתקיים $X^2=X$ ו-$Y^2=Y$, ולכן
$$D=\det\boldsymbol{Q}=XY(X+Y-XY)+XY=X^2Y+XY^2-X^2Y^2+XY=2XY,\qquad T=\operatorname{tr}\boldsymbol{Q}=X+Y.$$"""

questions.append(Q(
    3, "א", "joint_discrete",
    r"חשבו את פונקציית ההסתברות המשותפת של משתנה מקרי דו ממדי $(D,T)$.",
    Q3_REDUCE + r"""
הערכים האפשריים של $(X,Y)$:
$$\begin{array}{c|cccc}X&0&0&1&1\\Y&0&1&0&1\\D&0&0&0&2\\T&0&1&1&2\end{array}$$
ומכאן הטבלה המשותפת:
$$\begin{array}{c|ccc|c}D\backslash T&0&1&2&P_D(d)\\\hline0&(1-p)^2&2p(1-p)&0&1-p^2\\2&0&0&p^2&p^2\\\hline P_T(t)&(1-p)^2&2p(1-p)&p^2&\end{array}$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ב", "special_discrete",
    r"חשבו את פונקציית ההסתברות השולית של משתנה מקרי $D$. מהו שם ההתפלגות של $D$ ומהם הפרמטרים של ההתפלגות?",
    r"""**ההתפלגות השולית של $D$.**
מהטבלה, $P(D=0)=1-p^2$ ו-$P(D=2)=p^2$. מאחר ש-$D=2XY$,
$$\frac D2=XY\sim\mathrm{Ber}(p^2).$$
כלומר $D$ מקבל את הערך $2$ בהסתברות $p^2$ ואת הערך $0$ בהסתברות $1-p^2$ (ברנולי בפרמטר $p^2$, מוכפל ב-$2$).""",
    5, contextId="c3"))

questions.append(Q(
    3, "ג", "special_discrete",
    r"חשבו את פונקציית ההסתברות השולית של משתנה מקרי $T$. מהו שם ההתפלגות של $T$ ומהם הפרמטרים של ההתפלגות?",
    r"""**ההתפלגות השולית של $T$.**
מהטבלה, $P(T=0)=(1-p)^2$, $P(T=1)=2p(1-p)$, $P(T=2)=p^2$. זהו סכום של שני משתני ברנולי בלתי תלויים:
$$T=X+Y\sim\mathrm{Bin}(2,p).$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ד", "independence",
    r"האם המשתנים $D$ ו-$T$ בלתי תלויים? נמקו היטב!",
    r"""**אי-תלות.**
המשתנים תלויים: $P_{DT}(d,t)\ne P_D(d)P_T(t)$ עבור זוג ערכים כלשהו. למשל עבור $T=0$ ו-$D=2$:
$$P(D=2,T=0)=0\ne p^2(1-p)^2=P(D=2)\,P(T=0)$$
(לכל $0<p<1$).""",
    5, contextId="c3"))

questions.append(Q(
    3, "ה", "joint_discrete",
    r"האם המשתנים $D$ ו-$T$ בלתי מתואמים? נמקו היטב!",
    r"""**מתאם.**
נחשב את השונות המשותפת:
$$\operatorname{Cov}(D,T)=\mathbb{E}[DT]-\mathbb{E}[D]\,\mathbb{E}[T],\qquad \mathbb{E}[D]=2p^2,\quad \mathbb{E}[T]=2p.$$
$$\mathbb{E}[DT]=\mathbb{E}\bigl[2XY(X+Y)\bigr]=2\,\mathbb{E}\bigl[X^2Y+XY^2\bigr]=2\,\mathbb{E}[XY+XY]=4\,\mathbb{E}[X]\,\mathbb{E}[Y]=4p^2,$$
(כי $X^2=X$, $Y^2=Y$ ואי-התלות של $X,Y$). לכן
$$\operatorname{Cov}(D,T)=4p^2-4p^3=4p^2(1-p)\ne0\qquad(0<p<1).$$
המשתנים $D$ ו-$T$ מתואמים (אינם בלתי מתואמים).""",
    5, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_CAP = (r"לפניך גרף עבור פונקציית צפיפות ההסתברות $f_X(x)$ של משתנה מקרי $X$ בעל תוחלת $\mathbb{E}[X]=\frac{23}{24}$. "
          r"הצפיפות עולה ליניארית מ-$0$ ב-$x=0$ עד הגובה $1$ ב-$x=a$, נשארת בגובה $1$ עד $x=b$, ושווה אפס בכל מקום אחר.")

questions.append(Q(
    4, "א", "continuous_rv",
    r"מצאו את הפרמטרים $a$ ו-$b$.",
    r"""**מציאת $a,b$.**
מהגרף
$$f_X(x)=\begin{cases}x/a,&0\le x<a\\1,&a\le x\le b\\0,&\text{else}\end{cases}$$
נרמול:
$$\frac a2+(b-a)=1\quad\Longrightarrow\quad b-\frac a2=1.$$
תוחלת:
$$\mathbb{E}[X]=\int_0^ax\cdot\frac xa\,dx+\int_a^bx\cdot1\,dx=\frac{a^2}3+\frac{b^2-a^2}2=\frac{b^2}2-\frac{a^2}6=\frac{23}{24}\quad\Longrightarrow\quad3b^2-a^2=\frac{23}4.$$
פתרון שתי המשוואות יחד: $a=2b-2$, ולכן
$$3b^2-(2b-2)^2=\frac{23}{4}\ \Longrightarrow\ 3b^2-4b^2-4+8b=\frac{23}4\ \Longrightarrow\ b^2-8b+\frac{39}4=0.$$
$$b=\frac32\quad\text{or}\quad b=\frac{13}2,\qquad a=2b-2=1\quad\text{or}\quad 11.$$
מכיוון ש-$a<b$ (כפי שמופיע בגרף), הפתרון הוא
$$a=1,\qquad b=\frac32.$$
![הצפיפות עם a=1 ו-b=3/2](images/exams/25S-C-Q4-solved.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו גרף של $F_X(t)$ אשר משקף את תוצאות החישוב.",
    r"""**פונקציית ההתפלגות המצטברת.**
$F_X(t)=\int_{-\infty}^tf_X(x)\,dx$, כאשר $f_X(x)=x$ ב-$[0,1)$ ו-$f_X(x)=1$ ב-$[1,\frac32]$:
$$F_X(t)=\begin{cases}0,&t<0\\\dfrac{t^2}2,&0\le t<1\\t-\dfrac12,&1\le t<\dfrac32\\1,&t\ge\dfrac32\end{cases}$$
![גרף F_X(t): פרבולה עד (1, 1/2), אחר כך ישר עד (3/2, 1)](images/exams/25S-C-Q4-cdf.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"מהי ההסתברות $P\left(X\le\frac54\,\Big/\,X>\frac12\right)$?",
    r"""**הסתברות מותנית.**
$$P\left(X\le\frac54\,\Big/\,X>\frac12\right)=\frac{P\left(\frac12<X\le\frac54\right)}{P\left(X>\frac12\right)}=\frac{F_X\left(\frac54\right)-F_X\left(\frac12\right)}{1-F_X\left(\frac12\right)}=\frac{\left(\frac54-\frac12\right)-\frac18}{1-\frac18}=\frac57.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_CAP = (r"סטודנט של המכון הטכנולוגי חולון הרכיב מעגל חשמלי $Q_1$ מחמש יחידות $A,B,C,D,E$ הפועלות ללא תלות אחת בשנייה בהסתברויות זהות $p$. "
          r"במעגל $Q_1$ ($A$ ו-$C$ בענף השמאלי, $B$ ו-$D$ בענף הימני, ו-$E$ מגשר ביניהם) ובמעגל $Q_2$ ($A$ ו-$B$ במקביל, בטור עם $C$, $D$ ו-$E$ במקביל) מופיעים הרכיבים כבאיור.")

questions.append(Q(
    5, "א", "circuits",
    r"מה ההסתברות שמעגל $Q_1$ פעיל?",
    r"""**$P(Q_1)$.**
נפעל לפי רכיב $E$ (הגשר), באמצעות הסתברות שלמה:
• אם $E$ פועל (הסתברות $p$): המעגל הוא $A\parallel C$ בטור עם $B\parallel D$, והסתברותו $(2p-p^2)^2$.
• אם $E$ לא פועל (הסתברות $1-p$): המעגל הוא $(A\text{-}B\text{ series})\parallel(C\text{-}D\text{ series})$, והסתברותו $2p^2-p^4$.
לכן
$$P(Q_1)=(2p-p^2)^2\,p+(2p^2-p^4)(1-p)=\bigl(2+2p-5p^2+2p^3\bigr)p^2.$$""",
    9, contextId="c5"))

questions.append(Q(
    5, "ב", "circuits",
    r"לאחר פירוק של מעגל $Q_1$, סטודנט הרכיב מעגל חדש $Q_2$, מאותן יחידות. **ב-1:** מה ההסתברות שמעגל $Q_2$ יפעל?",
    r"""**$P(Q_2)$.**
$Q_2$ הוא $(A\parallel B)$ בטור עם $(C\parallel D\parallel E)$. הקבוצות בלתי תלויות, ולכן
$$P(Q_2)=(2p-p^2)\cdot\bigl[1-(1-p)^3\bigr]=6p^2-9p^3+5p^4-p^5.$$""",
    9, contextId="c5"))

questions.append(Q(
    5, "ג", "conditional_bayes",
    r"לאחר פירוק של מעגל $Q_1$, סטודנט הרכיב מעגל חדש $Q_2$, מאותן יחידות. **ב-2:** אם ידוע ש-$Q_2$ פעל, מה ההסתברות שגם המעגל המקורי $Q_1$ פעל?",
    r"""**$P(Q_1\mid Q_2)$.**
$$P(Q_1\mid Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}.$$
נסמן $\tilde Q=Q_1\cap Q_2$ ונחשב $P(\tilde Q)$ לפי ארבעת מצבי $(A,B)$:
$$P(Q_1\cap Q_2)=P(\tilde Q\mid A\cap B)P(A\cap B)+P(\tilde Q\mid\bar A\cap\bar B)P(\bar A\cap\bar B)+P(\tilde Q\mid A\cap\bar B)P(A\cap\bar B)+P(\tilde Q\mid\bar A\cap B)P(\bar A\cap B),$$
עם ההסתברויות $p^2$, $(1-p)^2$, $p(1-p)$, $p(1-p)$ בהתאמה.
• **$A,B$ פועלים:** $Q_1$ פועל תמיד (המסלול $A$ ואחריו $B$ בחלק העליון), ולכן $\tilde Q=Q_2$, ו-$Q_2$ פועל אם אחד מ-$C,D,E$ פועל: $P(\tilde Q\mid A\cap B)=1-(1-p)^3$.
• **$\bar A\cap\bar B$:** $Q_2$ לא פועל, ולכן $0$.
• **$A$ פועל, $B$ לא:** $Q_1$ פועל אם ורק אם $D$ פועל וגם אחד מ-$E,C$ פועל; אז גם $Q_2$ פועל (כי $D$ פועל וגם $A$ פועל). לכן $P(\tilde Q\mid A\cap\bar B)=P(D)\,P(E\cup C)=p(2p-p^2)$.
• **$B$ פועל, $A$ לא:** באופן סימטרי $P(C)\cdot P(E\cup D)=p(2p-p^2)$.
לכן
$$P(Q_1\cap Q_2)=p^2\bigl[1-(1-p)^3\bigr]+2p(1-p)\cdot p(2p-p^2)=3p^5-9p^4+7p^3,$$
ומכאן
$$P(Q_1\mid Q_2)=\frac{p\,(7-9p+3p^2)}{6-9p+5p^2-p^3}.$$""",
    7, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_CAP = (r"במפגש משתתפות $N$ משפחות. במשפחה הראשונה ישנם $n_1$ אנשים, במשפחה השנייה ישנם $n_2$ אנשים, $\ldots$, במשפחה ה-$N$ ישנם $n_N$ אנשים. "
          r"מתקיים: $n_1\ne n_2\ne\cdots\ne n_N$.")

questions.append(Q(
    6, "א", "discrete_rv",
    r"בוחרים **באקראי** באחת המשפחות. יהי $X$ משתנה מקרי המתאר את גודל המשפחה שנבחרה. מהו הגודל הממוצע $\mathbb{E}[X]$ של משפחה שנבחרה?",
    r"""**גודל משפחה ממוצע.**
כל משפחה נבחרת בהסתברות $\frac1N$:
$$\begin{array}{c|cccc}X&n_1&n_2&\cdots&n_N\\\hline P_X(x)&\frac1N&\frac1N&\cdots&\frac1N\end{array}$$
לכן
$$\mathbb{E}[X]=\frac{n_1+n_2+\cdots+n_N}{N}.$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ב", "discrete_rv",
    r"בוחרים **באקראי** באחד ממשתתפי המפגש. יהי $Y$ גודל של משפחתו. מהו הגודל הממוצע $\mathbb{E}[Y]$ של משפחתו של המשתתף?",
    r"""**גודל משפחה של משתתף שנבחר.**
נסמן $n=n_1+n_2+\cdots+n_N$ (מספר המשתתפים הכולל). משפחה בגודל $n_i$ נבחרת (דרך אחד מחבריה) בהסתברות $\frac{n_i}{n}$:
$$\begin{array}{c|cccc}Y&n_1&n_2&\cdots&n_N\\\hline P_Y(y)&\frac{n_1}{n}&\frac{n_2}{n}&\cdots&\frac{n_N}{n}\end{array}$$
לכן
$$\mathbb{E}[Y]=\frac{n_1^2+n_2^2+\cdots+n_N^2}{n_1+n_2+\cdots+n_N}.$$""",
    10, contextId="c6"))

questions.append(Q(
    6, "ג", "discrete_rv",
    r"האם $\mathbb{E}[Y]=\mathbb{E}[X]$? האם $\mathbb{E}[Y]\ge\mathbb{E}[X]$? האם $\mathbb{E}[Y]<\mathbb{E}[X]$?",
    r"""**השוואה.**
מהסעיפים הקודמים אפשר לכתוב $\mathbb{E}[Y]=\dfrac{\mathbb{E}[X^2]}{\mathbb{E}[X]}$ (המונה והמכנה חולקים ב-$N$). לכן
$$\mathbb{E}[Y]=\frac{\mathbb{E}[X^2]}{\mathbb{E}[X]}=\frac{\operatorname{Var}[X]+\bigl(\mathbb{E}[X]\bigr)^2}{\mathbb{E}[X]},\qquad\frac{\mathbb{E}[Y]}{\mathbb{E}[X]}=1+\frac{\operatorname{Var}[X]}{\bigl(\mathbb{E}[X]\bigr)^2}\ge1.$$
מכאן $\mathbb{E}[Y]\ge\mathbb{E}[X]$ (הטענה השנייה נכונה), והטענה $\mathbb{E}[Y]<\mathbb{E}[X]$ לעולם אינה מתקיימת. (הערה: מאחר שהגדלים $n_i$ שונים זה מזה והשונות חיובית, אי-השוויון חזק, ולכן גם $\mathbb{E}[Y]=\mathbb{E}[X]$ אינה נכונה.)""",
    6, contextId="c6"))

# ------------------------------------------------------------------ area regions + simulations (RAW_SCHEMA `region`, `sim`)
_SP = {"x": [0, 1], "y": [1, 2]}
_LB = {"x": "b", "y": "L"}
REGIONS = {
    (1, "א"): {"space": _SP, "labels": _LB, "event": [{"a": -1, "b": 1, "c": 0.5, "op": "<="}], "exact": 1 / 8, "caption": "האזור L ≤ b + 1/2 (a<1/4)"},
    (1, "ב"): {"space": _SP, "labels": _LB, "event": [{"a": -1, "b": 1, "c": "4/3", "op": "<="}], "exact": 7 / 9, "caption": "האזור L ≤ b + 4/3 (a<2/3)"},
}
_URN = {"values": list(range(1, 10)), "draws": 2, "replace": False}
SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(a<1/4)", "exact": 1 / 8, "seed": 12345},
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(a<2/3)", "exact": 7 / 9},
    (1, "ג"): {"kind": "area", "params": {"space": _SP, "measure": "var", "expr": "(y-x)/2"}, "estimate": "Var[a]", "exact": 1 / 24},
    (1, "ד"): {"kind": "area", "params": {"space": _SP, "measure": "cov", "expr": ["(y-x)/2", "x"]}, "estimate": "Cov[a,b]", "exact": -1 / 24},
    (2, "א"): {"kind": "urn", "params": dict(_URN, event="v2 % 2 == 1"), "estimate": "P(odd)", "exact": 5 / 9},
    (2, "ב"): {"kind": "urn", "params": dict(_URN, event="(v1+v2) % 3 == 0"), "estimate": "P(divisible by 3)", "exact": 1 / 3},
    (2, "ג"): {"kind": "urn", "params": dict(_URN, event="v2 == 5"), "estimate": "P(divisible by 5)", "exact": 1 / 9},
    (2, "ד"): {"kind": "urn", "params": dict(_URN, event="v2 % 2 == 1", given="(v1+v2) % 2 == 0"), "estimate": "P(odd | digit sum even)", "exact": 5 / 8},
    (4, "ג"): {"kind": "pdf", "params": {"pieces": [{"from": 0, "to": 1, "expr": "x"}, {"from": 1, "to": 1.5, "expr": "1"}],
                                        "event": "x <= 5/4", "given": "x > 1/2"}, "estimate": "P(X<=5/4 | X>1/2)", "exact": 5 / 7},
}

for _q in questions:
    _k = (_q["num"], _q.get("part"))
    if _k in REGIONS:
        _q["region"] = REGIONS[_k]
    if _k in SIMS:
        _q["sim"] = SIMS[_k]

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר קיץ תשפ״ה, מועד ג (11.12.2025)",
    "year": 2025,
    "examDate": "11.12.2025",
    "sourceFile": "25S-C exam pp.1-3",
    "solutionFile": "25S-C handwritten official solutions pp.4-14",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: משולש שווה שוקיים", "image": IMG + "Q1-triangle.png", "caption": Q1_CAP},
        "c2": {"kind": "text", "title": "שאלה 2: מספר דו ספרתי", "text": Q2_CAP},
        "c3": {"kind": "text", "title": "שאלה 3: מטריצת ברנולי", "text": Q3_CAP},
        "c4": {"kind": "image", "title": "שאלה 4", "image": IMG + "Q4-pdf.png", "caption": Q4_CAP},
        "c5": {"kind": "image", "title": "שאלה 5: מעגלים", "image": IMG + "Q5-circuits.png", "caption": Q5_CAP},
        "c6": {"kind": "text", "title": "שאלה 6: משפחות", "text": Q6_CAP},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
