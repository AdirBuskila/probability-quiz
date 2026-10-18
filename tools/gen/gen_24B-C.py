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
- Q1 area items (a-e) carry a `region` (moved from the old regions.json); sims are checked by check_sim_specs; steps by tools/verify/24B-C/steps_check.py.
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
            q["rubricSource"] = "ai-draft"
            q["stepsSource"] = "ai-draft"
    assert set(S) <= {(q["num"], q.get("part")) for q in questions}, "steps for unknown items"


# ---- 24B-C specifics: area figures, simulations, steps
_P3 = 0.3                                    # sample p for the Bernoulli-matrix answers (n = 3 matrices)
_XY3 = ["X%d" % i for i in range(1, 4)] + ["Y%d" % i for i in range(1, 4)]
_DS = "X1*Y1+X2*Y2+X3*Y3"
_TS = "+".join(_XY3)
_pdf4 = [(-1, 1, "2/5"), (1, 2, "2/5*(2-x)")]
_p6 = 0.6
_QB = "(E and (A or B) and (C or D)) or (not E and ((A and C) or (B and D)))"
_PQ = _p6 ** 2 * (2 + 2 * _p6 - 5 * _p6 ** 2 + 2 * _p6 ** 3)
_PAQ = (1 + 2 * _p6 - 3 * _p6 ** 2 + _p6 ** 3) / (2 + 2 * _p6 - 5 * _p6 ** 2 + 2 * _p6 ** 3)
_pAB6 = {c: _p6 for c in "ABCDE"}
_DG = {"values": [2, 3, 7]}

EXTRAS.update({
    (1, "א"): {"region": REG([lin(1, 0, "1/5", "<")], 1 / 5, "האירוע X<L/5 (יחידות של L)"), "sim": AREA("P(X<L/5)", 1 / 5)},
    (1, "ב"): {"region": REG([lin(0, 1, "1/3", ">")], 2 / 3, "האירוע Y>L/3 (יחידות של L)"), "sim": AREA("P(Y>L/3)", 2 / 3)},
    (1, "ג"): {"region": REG([lin(1, 1, "3/2", "<=")], 7 / 8, "האירוע X+Y<=3L/2 (יחידות של L)"), "sim": AREA("P(X+Y<=3L/2)", 7 / 8)},
    (1, "ד"): {"region": REG([lin(1, 0, "1/3", "<"), lin(0, 1, "1/3", "<")], 1 / 9, "האירוע max(X,Y)<L/3 (יחידות של L)"), "sim": AREA("P(Z<L/3), Z=max(X,Y)", 1 / 9)},
    (1, "ה"): {"region": REG([lin(1, 0, "1/2", "<"), lin(0, 1, "1/2", "<")], 1 / 6, "האירוע max(X,Y)<L/2 בהינתן X>L/4 (יחידות של L)", given=[lin(1, 0, "1/4", ">")]),
               "sim": AREA("P(Z<L/2 | X>L/4)", 1 / 6)},
    (2, "א"): {"sim": URN("P(הספרה מתחלקת ב-3)", 2 / 5, 1, "v1 % 3 == 0", values=list(range(10)))},
    (2, "ב"): {"sim": URN("P(הספרה השנייה מתחלקת ב-3)", 2 / 5, 2, "v2 % 3 == 0", values=list(range(10)))},
    (2, "ג"): {"sim": URN("P(השנייה זוגית | הראשונה מתחלקת ב-3)", 1 / 2, 2, "v2 % 2 == 0", "v1 % 3 == 0", values=list(range(10)))},
    (2, "ד"): {"sim": URN("P(הספרה השלישית מתחלקת ב-3)", 2 / 5, 3, "v3 % 3 == 0", values=list(range(10)))},
    (3, "א"): {"sim": CUST("P(D1=1) ב-p=0.3", 0.09, BER(_P3, "X", "Y"), event="X*Y == 1")},
    (3, "ב"): {"sim": CUST("P(T1=1) ב-p=0.3", 0.42, BER(_P3, "X", "Y"), event="X+Y == 1")},
    (3, "ג"): {"sim": CUST("P(D=1) ב-n=3, p=0.3", 3 * 0.09 * 0.91 ** 2, BER(_P3, *_XY3), event=_DS + " == 1")},
    (3, "ד"): {"sim": CUST("P(T=2) ב-n=3, p=0.3", 15 * 0.09 * 0.7 ** 4, BER(_P3, *_XY3), event=_TS + " == 2")},
    (3, "ה"): {"sim": CUST("cov[D,T] ב-n=3, p=0.3", 2 * 3 * 0.09 * 0.7, BER(_P3, *_XY3), measure="cov", expr=[_DS, _TS])},
    (4, "א"): {"sim": PDF("E[Z] ב-a=1, b=2", 4 / 15, _pdf4, measure="mean", expr="x")},
    (4, "ב"): {"sim": PDF("F_Z(1/2)=P(Z<=1/2)", 3 / 5, _pdf4, "x <= 1/2")},
    (4, "ג"): {"sim": PDF("P(Z>1/2 | |Z|<3/2)", 7 / 19, _pdf4, "x > 1/2", "abs(x) < 3/2")},
    (5, "א"): {"sim": URN("E[X] בשלוש קופסאות בגדלים 2,3,7", 4, 1, values=[2, 3, 7], measure="mean", expr="v1")},
    (5, "ב"): {"sim": URN("E[Y] בשלוש קופסאות בגדלים 2,3,7", 31 / 6, 1, values=[2] * 2 + [3] * 3 + [7] * 7, measure="mean", expr="v1")},
    (6, "א"): {"sim": CIRC("P(Q) ב-p=0.6", _PQ, _pAB6, _QB)},
    (6, "ב"): {"sim": CIRC("P(A | Q) ב-p=0.6", _PAQ, _pAB6, "A", _QB)},
    (6, "ג"): {"sim": CIRC("P(Q | בדיוק יחידה אחת תקולה) ב-p=0.6", 1, _pAB6, _QB, "A + B + C + D + E == 4")},
})

OM1 = r"נקבע $L=1$. מהו שטח מרחב המדגם $|\Omega|$ של הזוג $(X,Y)$, כלומר ריבוע היחידה?"
OM1_X = r"ריבוע בצלע $1$ הוא מרחב המדגם, ושטחו $1$. כאן ההסתברות שווה לשטח האירוע (אך בכל זאת מחלקים ב-$|\Omega|$)."

ADD(1, "א",
    RB((r"גישה גאומטרית או $F_X(L/5)$ של אחידה", 2), (r"האירוע $X<\frac L5$ הוא רצועה ברוחב $\frac L5$", 2), (r"התשובה $\frac15$", 1)),
    [r"להתייחס ל-$Y$ כאילו הוא מגביל את האירוע"],
    [NU(OM1, 1, OM1_X),
     NU(r"מהי $P(X<\frac L5)$? (שטח הרצועה ברוחב $\frac15$ חלקי $|\Omega|$)", Fr(1, 5), r"$\frac{1/5}{1}=\frac15$.")])

ADD(1, "ב",
    RB((r"גישה גאומטרית: הסתברות = שטח האירוע חלקי $L^2$", 2), (r"האירוע $Y>\frac L3$ הוא רצועה בגובה $\frac23L$", 2), (r"התשובה $\frac23$", 1)),
    [r"לחשב $P(Y<\frac L3)=\frac13$ במקום המשלים"],
    [NU(OM1, 1, OM1_X),
     NU(r"מהי $P(Y>\frac L3)$? (שטח הרצועה בגובה $1-\frac13$ חלקי $|\Omega|$)", Fr(2, 3), r"$\frac{2/3}{1}=\frac23$.")])

ADD(1, "ג",
    RB((r"מרחב המדגם כריבוע, $|\Omega|=L^2$", 1), (r"המשלים $X+Y>\frac32L$ הוא משולש פינתי בקודקוד $(L,L)$ עם ניצבים $\frac L2$", 2), (r"שטח המשולש $\frac{L^2}8$ והחסרתו מ-$L^2$", 1), (r"התשובה $\frac78$", 1)),
    [r"לחשב את שטח המשולש כ-$\frac12\cdot\frac32\cdot\frac32$ (לא לחתוך אותו עם הריבוע)", r"לשכוח את החילוק ב-$|\Omega|$"],
    [NU(OM1, 1, OM1_X),
     NU(r"מהו שטח המשלים $\{X+Y>\frac32\}$ בתוך הריבוע? (משולש בפינה $(1,1)$)", Fr(1, 8), r"הישר $x+y=\frac32$ חותך את הצלעות ב-$(1,\frac12)$ וב-$(\frac12,1)$: ניצבים $\frac12$, שטח $\frac12\cdot\frac14=\frac18$."),
     NU(r"מהי $P(X+Y\le\frac32L)$?", Fr(7, 8), r"$1-\frac18=\frac78$.")])

ADD(1, "ד",
    RB((r"זיהוי שהאירוע $\max(X,Y)<\frac L3$ שקול ל-$X<\frac L3$ **וגם** $Y<\frac L3$", 2), (r"האירוע הוא ריבוע בצלע $\frac L3$ ושטחו $\frac{L^2}9$", 2), (r"התשובה $\frac19$", 1)),
    [r"לכתוב את האירוע כאיחוד (זה $\min$) ולקבל $\frac59$", r"לחבר $\frac1{18}+\frac1{18}$ בלי להבין שהפיצול מכסה את הריבוע כולו"],
    [NU(OM1, 1, OM1_X),
     CH(r"$Z=\max(X,Y)$ כפי שהוגדר. איזה תיאור של האירוע $Z<\frac13$ נכון?",
        [r"$X<\frac13$ **וגם** $Y<\frac13$: ריבוע פינתי", r"$X<\frac13$ **או** $Y<\frac13$: איחוד של שתי רצועות", r"$X+Y<\frac13$: משולש פינתי"], 0,
        r"המקסימום קטן מ-$\frac13$ אם ורק אם שניהם קטנים מ-$\frac13$. האיחוד הוא האירוע $\min(X,Y)<\frac13$ (שטח $\frac59$), והמשולש שטחו $\frac1{18}$; שניהם אינם $\frac19$."),
     NU(r"מהי $P(Z<\frac L3)$? (שטח הריבוע חלקי $|\Omega|$)", Fr(1, 9), r"$\left(\frac13\right)^2=\frac19$.")])

ADD(1, "ה",
    RB((r"הגדרת הסתברות מותנית כיחס שטחים: $\frac{P(Z<\frac L2\cap X>\frac L4)}{P(X>\frac L4)}$", 1), (r"המכנה $P(X>\frac L4)=\frac34$", 1), (r"שטח החיתוך $\frac14\cdot\frac12=\frac18$ (מלבן $\frac L4<X<\frac L2$, $Y<\frac L2$)", 2), (r"התשובה $\frac16$", 1)),
    [r"לחלק ב-$|\Omega|=1$ במקום בשטח התנאי $\frac34$", r"להניח שהאירועים בלתי תלויים ולכפול"],
    [NU(OM1, 1, OM1_X),
     NU(r"מהי $P(X>\frac14)$? (שטח אזור התנאי; המכנה)", Fr(3, 4), r"רצועה ברוחב $\frac34$: שטח $\frac34$."),
     NU(r"מהו שטח החיתוך $\{\max(X,Y)<\frac12\}\cap\{X>\frac14\}$?", Fr(1, 8), r"$X\in(\frac14,\frac12)$ ו-$Y<\frac12$: מלבן $\frac14\times\frac12$, שטח $\frac18$."),
     NU(r"מהי ההסתברות המותנית?", Fr(1, 6), r"$\frac{1/8}{3/4}=\frac16$.")])

# ---- Q2: digits 0..9
D2 = r"באוסף $10$ ספרות: $\{0,1,\dots,9\}$."
ADD(2, "א",
    RB((r"מרחב המדגם: $10$ ספרות שוות סיכוי", 2), (r"האירוע $A_1=\{0,3,6,9\}$ (כולל $0$)", 2), (r"התשובה $\frac25$", 1)),
    [r"לשכוח שגם $0$ מתחלק ב-$3$ ולכתוב $\frac3{10}$", r"לחלק ב-$9$ במקום ב-$10$"],
    [CH(D2 + r" מוציאים ספרה אחת. איזה תיאור של מרחב המדגם נכון?",
        [r"$10$ ספרות שוות סיכוי", r"$9$ ספרות (בלי $0$)", r"$4$ תוצאות: $0,3,6,9$"], 0,
        r"כל $10$ הספרות באוסף שוות סיכוי, כולל $0$. $9$ ספרות מוחקת את $0$, שהוא בעצמו מתחלק ב-$3$. הארבע ($0,3,6,9$) הן האירוע, לא מרחב המדגם."),
     NU(r"כמה ספרות באוסף מתחלקות ב-$3$ ללא שארית?", 4, r"$0,3,6,9$ (גם $0$ מתחלק ב-$3$)."),
     NU(r"מהי $P(A_1)$?", Fr(2, 5), r"$\frac4{10}=\frac25$.")])

ADD(2, "ב",
    RB((r"מרחב המדגם: זוגות סדורים ללא חזרה, $|\Omega'|=10\cdot9=90$", 2), (r"ספירה: $4$ אפשרויות לספרה השנייה ו-$9$ לראשונה: $36$", 3), (r"התשובה $\frac25$", 2)),
    [r"לספור $4\cdot10$ (להתעלם מכך שהראשונה שונה מהשנייה)", r"לחשוב שהסדר לא חשוב"],
    [CH(D2 + r" מוציאים שתי ספרות ללא החזרה. מהו מרחב המדגם?",
        [r"$90$ זוגות סדורים של ספרות שונות", r"$100$ זוגות סדורים (עם חזרה)", r"$45$ זוגות לא סדורים"], 0,
        r"השנייה נבחרת מהספרות שנותרו ולכן הספרות שונות ($90$, לא $100$). השאלה על הספרה **השנייה**, ולכן הסדר חשוב ($45$ מאבד אותו)."),
     NU(r"כמה זוגות סדורים מקיימים: הספרה השנייה מתחלקת ב-$3$?", 36, r"$4$ אפשרויות לשנייה, ולכל אחת $9$ ספרות אחרות לראשונה: $36$."),
     NU(r"מהי $P(A_2)$?", Fr(2, 5), r"$\frac{36}{90}=\frac25$.")])

ADD(2, "ג",
    RB((r"הגדרת הסתברות מותנית $\frac{P(A_1\cap B_2)}{P(A_1)}$", 2), (r"$P(A_1)=\frac25$", 1), (r"ספירת $A_1\cap B_2$ לפי הספרה הראשונה: $4+4+5+5=18$", 2), (r"התשובה $\frac12$", 1)),
    [r"לספור $5$ זוגיות לשנייה בלי להתחשב בספרה הראשונה שהוצאה", r"לחלק ב-$P(B_2)$ במקום ב-$P(A_1)$"],
    [CH(r"נתון שהראשונה התחלקה ב-$3$ ($A_1$) ומחפשים את ההסתברות שהשנייה זוגית ($B_2$). איזה ביטוי נכון?",
        [r"$\frac{P(A_1\cap B_2)}{P(A_1)}$", r"$\frac{P(A_1\cap B_2)}{P(B_2)}$", r"$P(A_1\cap B_2)$"], 0,
        r"ההסתברות המותנית מחלקת בהסתברות **התנאי** $A_1$. השני נותן $0.4$ (זו $P(A_1\mid B_2)$) והשלישי נותן $0.2$ (בלי חלוקה בכלל)."),
     NU(r"מהי $P(A_1)$? (המכנה: אירוע התנאי)", Fr(2, 5), r"$\frac25$ מסעיף א."),
     NU(r"כמה זוגות סדורים מקיימים: הראשונה מתחלקת ב-$3$ והשנייה זוגית?", 18, r"ראשונה $0$ או $6$: $4$ זוגיות שנותרו; ראשונה $3$ או $9$: $5$ זוגיות: $4+4+5+5=18$."),
     NU(r"מהי $P(A_1\cap B_2)$?", Fr(1, 5), r"$\frac{18}{90}=\frac15$."),
     NU(r"מהי ההסתברות המותנית?", Fr(1, 2), r"$\frac{1/5}{2/5}=\frac12$.")])

ADD(2, "ד",
    RB((r"מרחב המדגם: שלשות סדורות ללא חזרה, $|\Omega''|=10\cdot9\cdot8=720$", 2), (r"ספירה: $4$ אפשרויות לשלישית ו-$9\cdot8=72$ לשתיים הראשונות", 3), (r"התשובה $\frac25$", 2)),
    [r"לספור שלשות עם חזרה ($1000$ במכנה): התשובה זהה אך מרחב המדגם שגוי", r"לשכוח שהראשונות שונות מהשלישית"],
    [CH(D2 + r" מוציאים שלוש ספרות ללא החזרה. מהו מרחב המדגם?",
        [r"$720$ שלשות סדורות של ספרות שונות", r"$1000$ שלשות סדורות (עם חזרה)", r"$120$ שלשות לא סדורות"], 0,
        r"בלי החזרה הספרות שונות ($10\cdot9\cdot8=720$), והשלישית נבדלת מהראשונות, ולכן הסדר חשוב ($120$ מאבד אותו)."),
     NU(r"כמה שלשות סדורות מקיימות: הספרה השלישית מתחלקת ב-$3$?", 288, r"$4$ אפשרויות לשלישית ו-$9\cdot8=72$ לשתי הראשונות: $4\cdot72=288$."),
     NU(r"מהי $P(A_3)$?", Fr(2, 5), r"$\frac{288}{720}=\frac25$.")])

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

# ---- Q4: pdf, constant 2/5 on (-a,a), linear to 0 on (a,b); a=1, b=2
ADD(4, "א",
    RB((r"נרמול: $2a\cdot\frac25+\frac12(b-a)\frac25=1$, כלומר $3a+b=5$", 3), (r"סימטריה: אינטגרל $zf_Z(z)$ על $(-a,a)$ הוא $0$", 2), (r"תוחלת: $\frac{1}{15}(b^2+ab-2a^2)=\frac4{15}$", 3), (r"פתרון המשוואה הריבועית ופסילת $a=\frac{21}4$ ($b<a$)", 2)),
    [r"לא לפסול את הפתרון $a=\frac{21}4$", r"לכלול את הקטע $(-a,a)$ בחישוב התוחלת"],
    [CH(r"הצבת $b=5-3a$ ב-$b^2+ab-2a^2=4$ נותנת $4a^2-25a+21=0$, כלומר $a=1$ או $a=\frac{21}4$. איזה פתרון מתאים?",
        [r"$a=1$", r"$a=\frac{21}4$", r"שני הפתרונות"], 0,
        r"עבור $a=\frac{21}4$ מתקבל $b=5-\frac{63}4=-\frac{43}4<a$, בניגוד לדרישה $b>a>0$. לכן רק $a=1$ מתאים."),
     NU(r"מהו $b$ כאשר $a=1$ (ממשוואת הנרמול $3a+b=5$)?", 2, r"$b=5-3=2$."),
     NU(r"בדיקה: מהי $\mathbb E[Z]=\frac1{15}(b^2+ab-2a^2)$ עבור $a=1$, $b=2$?", Fr(4, 15), r"$\frac{4+2-2}{15}=\frac4{15}$, כנדרש.")])

ADD(4, "ב",
    RB((r"פירוק לקטעים: $(-1,1)$ קבועה, $(1,2)$ יורדת ליניארית", 2), (r"$F_Z(t)=\frac25(t+1)$ על $[-1,1)$ ו-$1-\frac{(2-t)^2}5$ על $[1,2)$", 6), (r"בדיקת רציפות: $F_Z(1)=\frac45$, $F_Z(2)=1$", 2)),
    [r"לשכוח את הקבוע $\frac45$ בקטע האחרון", r"לטעות בגבול התחתון $-1$ (להתחיל מ-$0$)"],
    [NU(r"מהו $F_Z(0)=P(Z\le0)$?", Fr(2, 5), r"חצי הקטע הקבוע: $\frac25\cdot1=\frac25$."),
     NU(r"מהו $F_Z(1)$? (סוף הקטע הקבוע)", Fr(4, 5), r"$\frac25\cdot2=\frac45$."),
     NU(r"מהו $F_Z(\frac32)$? (בקטע $1\le t<2$)", Fr(19, 20), r"$1-\frac{(2-\frac32)^2}{5}=1-\frac1{20}=\frac{19}{20}$.")])

ADD(4, "ג",
    RB((r"הגדרת הסתברות מותנית כיחס הפרשי $F_Z$", 2), (r"מכנה $F_Z(\frac32)-F_Z(-\frac32)=\frac{19}{20}$", 1), (r"מונה $F_Z(\frac32)-F_Z(\frac12)=\frac7{20}$", 1), (r"התשובה $\frac7{19}$", 1)),
    [r"לחלק ב-$1$ ולא ב-$P(|Z|<\frac32)$", r"להשתמש בקטע הלא נכון של $F_Z$ ב-$\frac32$"],
    [NU(r"מהו $F_Z(\frac12)$?", Fr(3, 5), r"$\frac25\left(\frac12+1\right)=\frac35$."),
     NU(r"מהי $P(|Z|<\frac32)=F_Z(\frac32)-F_Z(-\frac32)$? (המכנה)", Fr(19, 20), r"$\frac{19}{20}-0=\frac{19}{20}$ ($F_Z(-\frac32)=0$)."),
     NU(r"מהי $P(\frac12<Z<\frac32)$? (המונה)", Fr(7, 20), r"$\frac{19}{20}-\frac35=\frac{7}{20}$."),
     NU(r"מהי ההסתברות המותנית?", Fr(7, 19), r"$\frac{7/20}{19/20}=\frac7{19}$.")])

# ---- Q5: boxes of bolts; numeric checks with n_i = 2, 3, 7
Q5SZ = r"בשלוש קופסאות יש $2$, $3$ ו-$7$ ברגים."
ADD(5, "א",
    RB((r"כל קופסה נבחרת בהסתברות $\frac1N$ (בחירה אחידה של קופסה)", 4), (r"טבלת ההתפלגות של $X$", 3), (r"$\mathbb E[X]=\frac{n_1+\cdots+n_N}N$", 3)),
    [r"לשקלל את הקופסאות לפי גודלן (זו שאלה ב')"],
    [CH(r"בוחרים **קופסה** באקראי. מהי $P(X=n_i)$?", [r"$\frac1N$", r"$\frac{n_i}{n_1+\cdots+n_N}$", r"$\frac{n_i}{N}$"], 0,
        r"המדגם הוא קופסה, וכולן שוות סיכוי: $\frac1N$. $\frac{n_i}{n}$ הוא הכלל לבורג שנבחר, ו-$\frac{n_i}N$ אינו התפלגות (סכומו אינו $1$)."),
     NU(Q5SZ + r" מהי $P(X=7)$?", Fr(1, 3), r"$\frac1N=\frac13$."),
     NU(r"באותו מדגם, מהי $\mathbb E[X]$?", 4, r"$\frac{2+3+7}3=4$.")])

ADD(5, "ב",
    RB((r"זיהוי שבחירת בורג נותנת קופסה $i$ בהסתברות $\frac{n_i}{n}$", 4), (r"טבלת ההתפלגות של $Y$", 3), (r"$\mathbb E[Y]=\frac{\sum n_i^2}{\sum n_i}$", 3)),
    [r"להשתמש שוב ב-$\frac1N$ ולקבל $\mathbb E[Y]=\mathbb E[X]$", r"לחשב $\sum n_i\cdot\frac{n_i}{N}$ (מחלק שגוי)"],
    [CH(r"בוחרים **בורג** באקראי ו-$Y$ הוא מספר הברגים בקופסתו. מהי $P(Y=n_i)$?", [r"$\frac{n_i}{n_1+\cdots+n_N}$", r"$\frac1N$", r"$\frac{n_i^2}{n_1^2+\cdots+n_N^2}$"], 0,
        r"הקופסה $i$ מכילה $n_i$ ברגים מתוך $n$ ולכן נבחרת בהסתברות $\frac{n_i}n$: קופסאות גדולות מיוצגות יתר על המידה. $\frac1N$ הוא כלל הקופסה, והשלישי אינו מתאים לספירת ברגים."),
     NU(Q5SZ + r" מהי $P(Y=7)$?", Fr(7, 12), r"$\frac7{12}$."),
     NU(r"באותו מדגם, מהי $\mathbb E[Y]$?", Fr(31, 6), r"$\frac{2^2+3^2+7^2}{12}=\frac{62}{12}=\frac{31}6$.")])

ADD(5, "ג",
    RB((r"$\mathbb E[Y]=\frac{\mathbb E[X^2]}{\mathbb E[X]}$", 2), (r"$\frac{\mathbb E[Y]}{\mathbb E[X]}=1+\frac{\operatorname{Var}[X]}{(\mathbb E[X])^2}$", 2), (r"מסקנה: $B\ge A$ (שוויון רק כש-$\operatorname{Var}=0$)", 1)),
    [r"להסיק שהממוצעים שווים כי ״שניהם מספר ברגים״", r"לשכוח ש-$\operatorname{Var}\ge0$ ולטעות בכיוון"],
    [NU(Q5SZ + r" מהי $\operatorname{Var}[X]$?", Fr(14, 3), r"$\mathbb E[X^2]=\frac{4+9+49}3=\frac{62}3$, ו-$\frac{62}3-16=\frac{14}3$."),
     NU(r"באותו מדגם, מהו היחס $\frac{B}{A}=\frac{\mathbb E[Y]}{\mathbb E[X]}$?", Fr(31, 24), r"$\frac{31/6}{4}=\frac{31}{24}=1+\frac{14/3}{16}$."),
     CH(r"מה נכון לגבי $B=\mathbb E[Y]$ ו-$A=\mathbb E[X]$?",
        [r"$B\ge A$ תמיד, ושוויון רק כש-$\operatorname{Var}[X]=0$", r"$B=A$ תמיד", r"$B<A$ תמיד"], 0,
        r"$\frac BA=1+\frac{\operatorname{Var}[X]}{(\mathbb E[X])^2}\ge1$. בדוגמה היחס $\frac{31}{24}>1$, ולכן שתי הטענות האחרות נכשלות.")])

# ---- Q6: bridge circuit; numeric checks at p=0.6
ADD(6, "א",
    RB((r"פיצול לפי הרכיב $E$ (הגשר)", 3), (r"$E$ פועל: $(2p-p^2)^2$; $E$ אינו פועל: $2p^2-p^4$", 4), (r"הצבה ופישוט: $p^2(2+2p-5p^2+2p^3)$ (הפישוט הרשמי תוקן)", 3)),
    [r"להתעלם מ-$E$ ולחשב רק $(AC)\cup(BD)$", r"לטעות בפתיחת הסוגריים (מקדם $p^3$)"],
    [CH(r"איך מחשבים את $P(Q)$ במעגל הגשר?",
        [r"מפצלים לפי $E$: כש-$E$ פועל המעגל הוא $(A\cup B)\cap(C\cup D)$, וכשאינו פועל $(AC)\cup(BD)$", r"מניחים שהמעגל הוא $(AC)\cup(BD)$ ומתעלמים מ-$E$", r"כל חמשת הרכיבים בטור: $p^5$"], 0,
        r"ל-$E$ יש תפקיד. ב-$p=0.6$ התעלמות מ-$E$ נותנת $0.5904$ (קטן מהנכון $0.65952$) וטור נותן $0.07776$."),
     NU(r"מהי $P(Q\mid E\ \text{works})$ כאשר $p=0.6$?", (2 * _p6 - _p6 ** 2) ** 2, r"$(2p-p^2)^2=0.84^2=0.7056$."),
     NU(r"מהי $P(Q\mid E\ \text{fails})$ באותו $p$?", 2 * _p6 ** 2 - _p6 ** 4, r"$2p^2-p^4=0.72-0.1296=0.5904$."),
     NU(r"מהי $P(Q)$?", _PQ, r"$0.6\cdot0.7056+0.4\cdot0.5904=0.65952$.")])

ADD(6, "ב",
    RB((r"נוסחת בייס $P(A\mid Q)=\frac{P(Q\mid A)P(A)}{P(Q)}$", 3), (r"$P(Q\mid A)=p+p(2p-p^2)-p^2(2p-p^2)=p+2p^2-3p^3+p^4$ (הפישוט הרשמי תוקן)", 4), (r"התשובה $\frac{1+2p-3p^2+p^3}{2+2p-5p^2+2p^3}$", 3)),
    [r"להשתמש בפישוט הרשמי השגוי ($-4p^3$)", r"לחלק ב-$P(A)$ במקום ב-$P(Q)$"],
    [CH(r"נתון שהמעגל פועל ($Q$), ומחפשים את ההסתברות ש-$A$ פועלת. איזו נוסחה נכונה?",
        [r"בייס: $\frac{P(Q\mid A)\,P(A)}{P(Q)}$", r"$P(A\mid Q)=P(Q\mid A)$", r"$P(A\mid Q)=P(A)$, כי $A$ אחד מחמישה רכיבים בלתי תלויים"], 0,
        r"$A$ והמעגל תלויים (הצלחת המעגל מגדילה את הסיכוי ש-$A$ פועלת). ב-$p=0.6$: $P(Q\mid A)=0.8016$, $P(A)=0.6$, ולכן התשובה הנכונה $0.729$; שתי האפשרויות האחרות נותנות $0.8016$ ו-$0.6$."),
     NU(r"מהי $P(Q)$ כאשר $p=0.6$? (המכנה: אירוע התנאי)", _PQ, r"$0.65952$ מסעיף א."),
     NU(r"מהי $P(Q\mid A)=p+p(2p-p^2)-p^2(2p-p^2)$ באותו $p$?", 0.8016, r"$0.6+0.504-0.3024=0.8016$."),
     NU(r"מהי $P(A\mid Q)$?", _PAQ, r"$\frac{0.8016\cdot0.6}{0.65952}\approx0.72926$.")])

ADD(6, "ג",
    RB((r"אם בדיוק יחידה אחת תקולה, ארבע האחרות פועלות", 2), (r"כל חתך של הגשר (קבוצת יחידות שתקלתן מפילה את המעגל) כולל לפחות שתי יחידות, ולכן תקלה בודדת אינה מפילה אותו", 2), (r"מסקנה: הסתברות $1$", 1)),
    [r"לחשוב שזה תלוי באיזו יחידה תקולה", r"לבלבל עם $P(Q)$ הבלתי מותנית"],
    [CH(r"נתון שבדיוק יחידה אחת תקולה (לא ידוע איזו). מה ההסתברות שהמעגל פועל?",
        [r"$1$, כי המעגל פועל בכל אחד מחמשת המצבים האפשריים", r"תלוי באיזו יחידה, ולכן הסתברות פחותה מ-$1$", r"$p^4(1-p)$"], 0,
        r"בכל אחד מחמשת המצבים של תקלה יחידה קיים מסלול פעיל. $p^4(1-p)$ היא ההסתברות לאחד המצבים בלבד (לא מותנית)."),
     NU(r"בכמה מבין חמשת המצבים של ״בדיוק יחידה אחת תקולה״ המעגל פועל?", 5, r"בכולם: אין חתך של גודל $1$ בגשר."),
     NU(r"מהי ההסתברות המבוקשת?", 1, r"$\frac55=1$.")])

APPLY(questions)


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
