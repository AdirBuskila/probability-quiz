# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-C.json -- probability (course 20021), semester B 2024, moed C (15.09.2024).
6 questions, 23 items (Q1 5, Q2 4, Q3 5 incl. a bonus, Q4 3, Q5 3, Q6 3), 25 points each (+5 bonus in Q3).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-C.py

Source: exam pp.1-3, handwritten official solutions pp.4-11 (grid paper).

Transcription notes
- Part keys are single letters. Q1 prints a-1, a-2, a-3, b-1, b-2, stored as a b c d e. Map: Q1 a=א-1, b=א-2,
  c=א-3, d=ב-1, e=ב-2; Q2 a=א, b=ב-1, c=ב-2, d=ג (the printed label is the first bold token of each question text).
- Q1 (ב): the printed text says "the shorter matchstick" but defines Z = max(X,Y). The official solution (which writes
  "max" over the line) uses the maximum: P(Z<L/3)=1/9. The question is transcribed as printed (word and formula); the key
  matches the formula.
- Q1 area items (c, d, e) have region data in tools/verify/24B-C/regions.json (no `region` field in RAW_SCHEMA).
- Q3 (סעיף בונוס) = Q3e: no solution page in the source; solved (solutionSource "solved", official:false):
  cov[D,T] = 2np^2(1-p), verified exactly and by Monte Carlo in tools/verify/24B-C/check.py.
- Q5: the official solution page says "here opens the solution of Q5 of 24B-A (16.07.24)" (identical question); the
  solution text is transcribed from the 24B-A solution of that same question.
- Q6 (א) and (ב) TYPO RULING (arbiter 2026-10-18, the printed question wins): the official expanded form of P(Q)
  is p^2(2+p-5p^2+2p^3), but its own first line p(2p-p^2)^2+(1-p)(2p^2-p^4) expands to p^2(2+2p-5p^2+2p^3);
  and P(Q|A) is printed with -4p^3 where the official formula expands to -3p^3. Both are final answers, so both
  ship with the expansions corrected, solutionSource "solved", official:false and the "הפתרון הרשמי עם תיקון"
  prefix: P(Q) = p^2(2+2p-5p^2+2p^3), P(A|Q) = (1+2p-3p^2+p^3)/(2+2p-5p^2+2p^3). Verified exactly and by
  Monte Carlo in tools/verify/24B-C/check.py.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-C.json"
CODE = "24B-C"
IMG = "images/exams/24B-C-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_LEAD = r"נתבונן בשני גפרורים שאורכם מהווים משתנים מקריים בלתי תלויים $X\sim U_c(0,L)$ ו-$Y\sim U_c(0,L)$."
Q1_B = r"יהי $Z$ אורך הגפרור הקצר בין השניים: $Z=\max(X,Y)$."

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א-1:** חשבו את ההסתברות $P(X<L/5)$.",
    r"""$$P(X<L/5)=\frac{L/5}{L}=\frac15.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**א-2:** חשבו את ההסתברות $P(Y>L/3)$.",
    r"""$$P(Y>L/3)=\frac{L-L/3}{L}=\frac23.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**א-3:** חשבו את ההסתברות $P(X+Y\le 3L/2)$.",
    r"""נשתמש בגישה הגאומטרית: $\Omega$ הוא ריבוע בצלע $L$, $|\Omega|=L^2$. האזור $\{Y\le\frac32L-X\}$ הוא כל הריבוע פרט למשולש הפינה הימנית-עליונה שניצביו $\frac L2$ ושטחו $\frac12\cdot\frac{L^2}{4}$. לכן
$$P(X+Y\le\tfrac32L)=\frac{L^2-\frac12\cdot\frac{L^2}{4}}{L^2}=\frac78.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ד", "minmax_transform",
    Q1_B + "\n" + r"**ב-1:** חשבו את ההסתברות $P(Z<L/3)$.",
    r"""נפצל לפי איזה גפרור ארוך יותר:
$$P(Z<\tfrac L3)=P(Z<\tfrac L3\cap X<Y)+P(Z<\tfrac L3\cap X\ge Y).$$
כאשר $X<Y$ מתקיים $Z=Y$, ולכן $|\{Z<\frac L3\cap X<Y\}|=|\{Y<\frac L3\cap Y>X\}|=\frac12\cdot\frac{L^2}{9}=\frac{L^2}{18}$, וההסתברות היא $\frac{1}{18}$ (חלוקה ב-$|\Omega|=L^2$).
כאשר $X\ge Y$ מתקיים $Z=X$, ובאופן סימטרי $|\{Z<\frac L3\cap X\ge Y\}|=|\{X<\frac L3\cap Y\le X\}|=\frac{L^2}{18}$, וההסתברות היא $\frac1{18}$.
לכן
$$P(Z<\tfrac L3)=\frac1{18}+\frac1{18}=\frac19.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ה", "minmax_transform",
    Q1_B + "\n" + r"**ב-2:** חשבו את ההסתברות המותנית $P(Z<L/2\ /\ X>L/4)$.",
    r"""לפי הגדרת ההסתברות המותנית:
$$P(Z<\tfrac L2\mid X>\tfrac L4)=\frac{P(Z<\frac L2\cap X>\frac L4)}{P(X>\frac L4)},\qquad P(X>\tfrac L4)=\frac{L-L/4}{L}=\frac34.$$
נפצל את המונה לפי $X<Y$ ו-$X\ge Y$ ונחשב שטחים (חלקי $|\Omega|=L^2$): האזורים $\{X<\frac L2,\ X>\frac L4,\ Y<\frac L2\}$ מרכיבים יחד אזור בגודל $\frac L4\cdot\frac L2$, ולכן
$$P(Z<\tfrac L2\cap X>\tfrac L4)=\frac1{L^2}\left(\frac L4\cdot\frac L2\right)=\frac18.$$
ומכאן
$$P(Z<\tfrac L2\mid X>\tfrac L4)=\frac{1/8}{3/4}=\frac16.$$""",
    5, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_LEAD = r"באוסף נמצאות 10 ספרות: $\{0,1,2,3,4,5,6,7,8,9\}$."

questions.append(Q(
    2, "א", "combinatorics",
    r"מוציאים מהאוסף ספרה אחת. מהי ההסתברות שהיא תתחלק ב-3 ללא שארית?",
    r"""נסמן ב-$A_1$ את המאורע שהספרה מתחלקת ב-3 ללא שארית: $A_1=\{0,3,6,9\}$. לכן
$$P(A_1)=\frac{|A_1|}{|\Omega|}=\frac4{10}=\frac25.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ב", "combinatorics",
    r"מוציאים מהאוסף שתי ספרות ללא החזרה." "\n" r"**ב-1:** מהי ההסתברות שהספרה השנייה תתחלק ב-3 ללא שארית?",
    r"""נסמן ב-$A_2$ את המאורע שהספרה השנייה שנבחרה (ללא החזרה) מתחלקת ב-3 ללא שארית. מרחב המדגם הוא כל הזוגות הסדורים של ספרות שונות, $|\Omega'|=10\cdot9=90$. לספרה השנייה 4 אפשרויות (0, 3, 6, 9) ולכל אחת 9 אפשרויות לספרה הראשונה:
$$P(A_2)=\frac{|A_2|}{|\Omega'|}=\frac{4\cdot9}{90}=\frac25.$$""",
    7, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"מוציאים מהאוסף שתי ספרות ללא החזרה." "\n" r"**ב-2:** אם ידוע כי הספרה הראשונה התחלקה ב-3 ללא שארית, מהי ההסתברות שהספרה השנייה תהיה זוגית?",
    r"""נסמן ב-$B_2$ את המאורע שהספרה השנייה זוגית. לפי הגדרת ההסתברות המותנית:
$$P(B_2\mid A_1)=\frac{P(A_1\cap B_2)}{P(A_1)}=\frac{1/5}{2/5}=\frac12.$$
כאשר $P(A_1\cap B_2)=\frac{|A_1\cap B_2|}{|\Omega'|}=\frac{18}{90}=\frac15$: אם הספרה הראשונה היא $0$ או $6$ נותרות 4 ספרות זוגיות לספרה השנייה, ואם היא $3$ או $9$ נותרות 5 ספרות זוגיות; $4+4+5+5=18$.""",
    6, contextId="c2"))

questions.append(Q(
    2, "ד", "combinatorics",
    r"מוציאים מהאוסף שלוש ספרות ללא החזרה. מהי ההסתברות שהספרה השלישית תתחלק ב-3 ללא שארית?",
    r"""נסמן ב-$A_3$ את המאורע שהספרה השלישית מתחלקת ב-3 ללא שארית. לספרה השלישית 4 אפשרויות (0, 3, 6, 9), ולשתי הספרות הראשונות $9\cdot8=72$ אפשרויות. מרחב המדגם הוא $|\Omega''|=10\cdot9\cdot8$. לכן
$$P(A_3)=\frac{|A_3|}{|\Omega''|}=\frac{4\cdot72}{10\cdot9\cdot8}=\frac25.$$""",
    7, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_LEAD = (r"נתבונן בסדרה של $n$ מטריצות ברנולי מהצורה"
           "\n" r"$$\boldsymbol{Q}_1=\begin{pmatrix}0&-X_1\\Y_1&X_1+Y_1\end{pmatrix},\ \ \boldsymbol{Q}_2=\begin{pmatrix}0&-X_2\\Y_2&X_2+Y_2\end{pmatrix},\ \ldots,\ \ \boldsymbol{Q}_n=\begin{pmatrix}0&-X_n\\Y_n&X_n+Y_n\end{pmatrix},$$"
           "\n" r"כאשר $X_j$ ו-$Y_j$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגויות ברנולי: $X_j\sim\mathrm{Ber}(p)$ ו-$Y_j\sim\mathrm{Ber}(p)$ עבור כל $j=1,\ldots,n$. "
           r"עבור כל מטריצה $\boldsymbol{Q}_j$ נגדיר שני משתנים מקריים חדשים: דטרמיננטה $D_j=\det\boldsymbol{Q}_j$ ועקבה $T_j=\operatorname{tr}\boldsymbol{Q}_j$.")

questions.append(Q(
    3, "א", "special_discrete",
    r"**א:** מצאו את פונקציית ההסתברות של משתנה מקרי $D_1$. מה שם ההתפלגות של $D_1$ ומהם הפרמטרים של ההתפלגות?",
    r"""$$D_j=X_jY_j,\qquad T_j=X_j+Y_j.$$
מאחר ש-$X_j\sim\mathrm{Ber}(p)$ ו-$Y_j\sim\mathrm{Ber}(p)$, כל אחד מהם מקבל רק את הערכים 0 ו-1, ולכן גם המכפלה $D_j=X_jY_j$ מקבלת רק את הערכים 0 ו-1; ו-$D_j=1$ אם ורק אם $X_j=Y_j=1$, ובגלל אי-התלות $P(D_j=1)=p\cdot p=p^2$. לכן
$$D_j=X_jY_j\sim\mathrm{Ber}(p^2),\qquad P(D_1=1)=p^2,\ P(D_1=0)=1-p^2.$$""",
    8, contextId="c3"))

questions.append(Q(
    3, "ב", "special_discrete",
    r"**ב:** מצאו את פונקציית ההסתברות של משתנה מקרי $T_1$. מה שם ההתפלגות של $T_1$ ומהם הפרמטרים של ההתפלגות?",
    r"""$T_j=X_j+Y_j$ הוא סכום של שני משתנים מקריים ברנולי בלתי תלויים בעלי אותו פרמטר $p$. לפי משפט הפירוק (סכום של ברנולי בלתי תלויים הוא בינומי):
$$T_1\sim\mathrm{Bin}(2,p),\qquad P(T_1=t)=\binom2tp^t(1-p)^{2-t},\ t=0,1,2.$$""",
    8, contextId="c3"))

questions.append(Q(
    3, "ג", "special_discrete",
    r"נגדיר משתנה חדש $D=\sum_{j=1}^nD_j$. איך משתנה $D$ מפולג? **נמקו היטב!**",
    r"""$D$ הוא סכום של $n$ משתנים מקריים $D_j\sim\mathrm{Ber}(p^2)$ (סעיף א). המשתנים $D_j$ בלתי תלויים זה בזה, כי כל אחד מהם נקבע רק על ידי הזוג $(X_j,Y_j)$ וזוגות שונים בלתי תלויים. לפי משפט הפירוק (סכום של $n$ ברנולי בלתי תלויים בעלי אותו פרמטר) מתקבל
$$D\sim\mathrm{Bin}(n,p^2).$$""",
    4, contextId="c3"))

questions.append(Q(
    3, "ד", "special_discrete",
    r"נגדיר משתנה חדש $T=\sum_{j=1}^nT_j$. איך משתנה $T$ מפולג? **נמקו היטב!**",
    r"""$T$ הוא סכום של $n$ משתנים מקריים בלתי תלויים $T_j\sim\mathrm{Bin}(2,p)$ (סעיף ב). לפי משפט הפירוק (סכום של בינומיים בלתי תלויים בעלי אותו $p$, כל אחד הוא סכום של 2 ברנולי) מתקבל
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
Q4_LEAD = r"לפניכם גרף עבור פונקציית צפיפות ההסתברות $f_Z(z)$ של משתנה מקרי $Z$. הצפיפות קבועה ושווה $\frac25$ על $(-a,a)$, יורדת ליניארית מ-$\frac25$ ל-$0$ על $(a,b)$ ושווה $0$ מחוץ ל-$(-a,b)$."

questions.append(Q(
    4, "א", "continuous_rv",
    r"**א:** בהנחה כי $\mathbb{E}[Z]=4/15$, מצאו את הפרמטרים $a$ ו-$b$.",
    r"""**נרמול.** מלבן ברוחב $2a$ וגובה $\frac25$, ומשולש ברוחב $b-a$ וגובה $\frac25$:
$$2a\cdot\frac25+(b-a)\cdot\frac25\cdot\frac12=1\ \Longrightarrow\ 3a+b=5.$$
**תוחלת.** על $(-a,a)$ הצפיפות קבועה, ולכן אינטגרל $zf_Z(z)$ שם הוא $0$. על $(a,b)$ הצפיפות היא $\frac25\cdot\frac{b-z}{b-a}$:
$$\mathbb{E}[Z]=\int_a^bz\cdot\frac25\cdot\frac{b-z}{b-a}\,dz=\frac{2}{5(b-a)}\left\{\frac{bz^2}{2}\Big|_a^b-\frac{z^3}{3}\Big|_a^b\right\}=\frac25\left\{\frac b2(b+a)-\frac{b^2+ab+a^2}{3}\right\}=\frac1{15}\left(b^2+ab-2a^2\right).$$
מ-$\mathbb{E}[Z]=\frac4{15}$ מתקבל $b^2+ab-2a^2=4$. נציב $b=5-3a$ ונקבל
$$4a^2-25a+21=0\ \Longrightarrow\ a=1\ \text{ or }\ a=\frac{21}4.$$
הפתרון $a=\frac{21}{4}$ נפסל, כי אז $b=-\frac{43}4<a$ (נדרש $b>a$). לכן
$$a=1,\qquad b=2.$$""",
    10, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"**ב:** בהינתן הפרמטרים מהסעיף הקודם, חשבו את פונקציית ההתפלגות המצטברת $F_Z(t)$ ושרטטו את התוצאה.",
    r"""עם $a=1$, $b=2$ הצפיפות היא $\frac25$ על $(-1,1)$ ו-$\frac25(2-z)$ על $(1,2)$. אינטגרציה לכל $t\in\mathbb{R}$ נותנת
$$F_Z(t)=P(Z\le t)=\begin{cases}0,&t<-1,\\ \frac25(t+1),&-1\le t<1,\\ 1-\dfrac{(2-t)^2}{5},&1\le t<2,\\ 1,&t\ge2.\end{cases}$$
![גרף פונקציית ההתפלגות המצטברת F_Z(t)](images/exams/24B-C-Q4-cdf.png)""",
    10, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"**ג:** מהי ההסתברות המותנית $P(Z>1/2\ /\ |Z|<3/2)$?",
    r"""$$P\left(Z>\tfrac12\ \Big|\ |Z|<\tfrac32\right)=\frac{P(\frac12<Z<\frac32)}{P(-\frac32<Z<\frac32)}=\frac{F_Z(\frac32)-F_Z(\frac12)}{F_Z(\frac32)-F_Z(-\frac32)}=\frac{\frac{19}{20}-\frac35}{\frac{19}{20}-0}=\frac7{19}.$$""",
    5, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_LEAD = (r"לפניך $N$ קופסאות ממוספרות. בקופסה הראשונה ישנם $n_1$ ברגים, בקופסה השנייה ישנם $n_2$ ברגים, $\ldots$, "
           r"בקופסה ה-$N$ ישנם $n_N$ ברגים. מתקיים: $n_1\ne n_2\ne\cdots\ne n_N$.")

questions.append(Q(
    5, "א", "discrete_rv",
    r"**א:** בוחרים **באקראי** באחת הקופסאות. כמה ברגים, בממוצע, יהיו בקופסה שנבחרה?",
    r"""כל קופסה נבחרת בהסתברות $\frac1N$. אם $X$ הוא מספר הברגים בקופסה שנבחרה, אז $P(X=n_i)=\frac1N$ ולכן
$$\mathbb{E}[X]=\frac{n_1+n_2+\cdots+n_N}{N}.$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ב", "discrete_rv",
    r"**ב:** מוציאים את כל הברגים מכל הקופסאות ומערבבים אותם היטב. מאוסף שנוצר בוחרים **באקראי** בורג אחד. כמה ברגים, בממוצע, היו בתוך הקופסה שאליה שייך הבורג הנבחר?",
    r"""נסמן $n=n_1+n_2+\cdots+n_N$ (סך הברגים). הבורג שנבחר שייך לקופסה $i$ בהסתברות $\frac{n_i}{n}$, ואז בקופסה היו $n_i$ ברגים. אם $Y$ הוא מספר הברגים בקופסה של הבורג הנבחר:
$$\mathbb{E}[Y]=\frac{n_1^2+n_2^2+\cdots+n_N^2}{n_1+n_2+\cdots+n_N}.$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ג", "discrete_rv",
    r"נסמן ב-$A$ את תשובתך בסעיף א' וב-$B$ את תשובתך בסעיף ב'. האם $B\ge A$? האם $B<A$? נמקו **היטב!**",
    r"""מהסעיפים הקודמים $A=\mathbb{E}[X]$, $B=\mathbb{E}[Y]$ ו-$\mathbb{E}[X^2]=\frac{n_1^2+\cdots+n_N^2}{N}$, ולכן
$$B=\frac{\mathbb{E}[X^2]}{\mathbb{E}[X]}=\frac{\operatorname{Var}[X]+(\mathbb{E}[X])^2}{\mathbb{E}[X]}.$$
נחלק ב-$\mathbb{E}[X]$:
$$\frac{B}{A}=1+\frac{\operatorname{Var}[X]}{(\mathbb{E}[X])^2}\ge1.$$
מכאן $B\ge A$ (התשובה הרשמית), והטענה $B<A$ אינה נכונה.""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_LEAD = (r"מעגל חשמלי מורכב מחמש יחידות הפועלות ללא תלות אחת בשנייה בהסתברות $p$. "
           r"המעגל הוא גשר: $A$ ו-$B$ בצד שמאל (מהצומת השמאלי לצומת העליון ולצומת התחתון), $C$ ו-$D$ בצד ימין (מהצומת העליון ומהתחתון לצומת הימני), "
           r"ו-$E$ מחבר בין הצומת העליון לתחתון.")
questions.append(Q(
    6, "א", "circuits",
    r"**א:** מהי ההסתברות שהמעגל כולו פועל? **עליך לתת חישוב מפורט!**",
    r"""**הפתרון הרשמי עם תיקון:** בפתרון הרשמי הפתיחה של הביטוי נכתבה $P(Q)=p^2(2+p-5p^2+2p^3)$, אבל הביטוי הרשמי עצמו נפתח ל-$p^2(2+2p-5p^2+2p^3)$ (המקדם של $p^3$ הוא $2$ ולא $1$). התיקון נבדק (חישוב מדויק וסימולציה).
נפצל לפי הרכיב $E$ (הגשר).
אם $E$ פועל (הסתברות $p$), המעגל פועל אם ($A$ או $B$ פועל) **וגם** ($C$ או $D$ פועל): הסתברות $(2p-p^2)^2$.
אם $E$ אינו פועל (הסתברות $1-p$), המעגל פועל אם ($A$ וגם $C$) או ($B$ וגם $D$): הסתברות $2p^2-p^4$.
$$P(Q)=p\,(2p-p^2)^2+(1-p)(2p^2-p^4)=(4p^3-4p^4+p^5)+(2p^2-2p^3-p^4+p^5)$$
$$P(Q)=2p^2+2p^3-5p^4+2p^5=p^2\,(2+2p-5p^2+2p^3).$$""",
    10, contextId="c6", solutionSource="solved", official=False))

questions.append(Q(
    6, "ב", "circuits",
    r"**ב:** אם ידוע כי המעגל כולו פועל, מהי ההסתברות שהיחידה $A$ פועלת?",
    r"""**הפתרון הרשמי עם תיקון:** בפתרון הרשמי נכתב $P(Q\mid A)=p+2p^2-4p^3+p^4$ והתשובה $\frac{1+2p-4p^2+p^3}{2+p-5p^2+2p^3}$. הביטוי הרשמי $p+p(2p-p^2)-p^2(2p-p^2)$ נפתח ל-$p+2p^2-3p^3+p^4$, והמכנה מתוקן לפי סעיף א, ולכן התשובה הסופית שונה מהתשובה הרשמית. התיקון נבדק (חישוב מדויק וסימולציה).
לפי נוסחת בייס:
$$P(A\mid Q)=\frac{P(Q\mid A)P(A)}{P(Q)}.$$
בהינתן ש-$A$ פועל, המעגל פועל אם $C$ פועל, או אם $D$ פועל וגם ($E$ או $B$ פועל):
$$P(Q\mid A)=p+p(2p-p^2)-p^2(2p-p^2)=p+2p^2-p^3-2p^3+p^4=p+2p^2-3p^3+p^4.$$
עם $P(A)=p$ ו-$P(Q)=p^2(2+2p-5p^2+2p^3)$ מסעיף א:
$$P(A\mid Q)=\frac{p\,(p+2p^2-3p^3+p^4)}{p^2(2+2p-5p^2+2p^3)}=\frac{1+2p-3p^2+p^3}{2+2p-5p^2+2p^3}.$$""",
    10, contextId="c6", solutionSource="solved", official=False))

questions.append(Q(
    6, "ג", "circuits",
    r"**ג:** אם ידוע כי **בדיוק יחידה אחת לא** פועלת (ולא ידוע איזו יחידה בדיוק!), מהי ההסתברות שהמעגל כולו כן פועל?",
    r"""אם בדיוק יחידה אחת אינה פועלת, ארבע היחידות האחרות פועלות. כדי שהמעגל יפסיק לפעול צריך להיכשל לפחות שני רכיבים מתאימים (חתך מינימלי של הגשר הוא בגודל 2), ולכן כשרק רכיב אחד נכשל המעגל תמיד פועל:
$$P(Q\mid\text{exactly one unit fails})=1.$$""",
    5, contextId="c6"))

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר ב׳ תשפ״ד, מועד ג (15.09.2024)",
    "year": 2024,
    "examDate": "15.09.2024",
    "sourceFile": "24B-C exam pp.1-3",
    "solutionFile": "24B-C official handwritten solutions pp.4-11",
    "contexts": {
        "c1": {"kind": "text", "title": "שאלה 1", "text": Q1_LEAD},
        "c2": {"kind": "text", "title": "שאלה 2", "text": Q2_LEAD},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_LEAD},
        "c4": {"kind": "image", "title": "שאלה 4: גרף הצפיפות", "image": IMG + "Q4-pdf.png", "caption": Q4_LEAD},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_LEAD},
        "c6": {"kind": "image", "title": "שאלה 6: מעגל גשר", "image": IMG + "Q6-bridge.png", "caption": Q6_LEAD},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
