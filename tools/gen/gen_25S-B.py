# -*- coding: utf-8 -*-
"""Generator for tools/raw/25S-B.json -- probability (course 20021), summer 2025, moed B (10.11.2025). Choose 4 of 6
questions, 25 points each. 22 items (Q1 3, Q2 3, Q3 4, Q4 5, Q5 3, Q6 4).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25S-B.py

Source: exam pp.1-3 (pdf), official solutions pp.4-15 (blue-ink handwriting on plain/grid paper; Q6 typed).
No text layer; rendered and read.

Transcription notes
- Part keys: single letters. Q4 prints "א", "ב-1", "ב-2", "ב-3", "ג" -> a b c d e; Q2 prints "א", "ב-1", "ב-2" -> a b c;
  Q5 and Q6 are plain letters. The printed label is the first bold token of each question text.
- Q2: the printed text says "two numbers are chosen one after the other" without naming replacement; the official
  solution treats it as without replacement (it writes X1 != X2), and that reading is the one transcribed.
- Q3 printed hint (sum x^n/(n-k)!) is kept in parts that use it.
- Math never holds Hebrew; Hebrew event names inside the official solution are replaced by the symbols D1, D2 etc.
- Q1 region data and the sim specs live in the REGIONS / SIMS blocks above the exam dict.
- The page-1 cover (lecturer names) is not copied anywhere.
"""
import json, math, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25S-B.json"
CODE = "25S-B"
IMG = "images/exams/25S-B-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_CAP = (r"במערכת המחוגים הבאה, הזוויות $\alpha_1$ ו-$\alpha_2$ מהוות משתנים מקריים בלתי תלויים בעלי התפלגות אחידה רציפה: "
          r"$\alpha_1\sim U_c(0,\pi)$, $\alpha_2\sim U_c(0,\pi)$. הזווית $\alpha_1$ מאפיינת את המחוג מס׳ 1; הזווית $\alpha_2$ מאפיינת את המחוג מס׳ 2. "
          r"הזווית $\beta$ היא הזווית בין המחוגים; שימו לב כי $\beta=|\alpha_1-\alpha_2|$.")

Q1_OMEGA = r"מרחב המדגם הוא הריבוע $\Omega=(0,\pi)^2$ במישור $(\alpha_1,\alpha_2)$, ושטחו $|\Omega|=\pi^2$."

questions.append(Q(
    1, "א", "uniform_geometric",
    r"מה ההסתברות ש-$\alpha_2>2\alpha_1$?",
    r"""**$P(\alpha_2>2\alpha_1)$.**
""" + Q1_OMEGA + r"""
האזור $\{\alpha_2>2\alpha_1\}$ הוא המשולש שמעל הישר $\alpha_2=2\alpha_1$, שקודקודיו $(0,0)$, $(0,\pi)$ ו-$(\frac\pi2,\pi)$.
![האזור α2 > 2α1 בתוך הריבוע](images/exams/25S-B-Q1a-region.png)
$$P(\alpha_2>2\alpha_1)=\frac{\text{area}(ADE)}{|\Omega|}=\frac{\frac12\cdot\pi\cdot\frac\pi2}{\pi^2}=\frac14.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"מה ההסתברות שהזווית $\beta$ היא זווית חדה?",
    r"""**$P(\beta\text{ acute})=P\left(|\alpha_1-\alpha_2|<\frac\pi2\right)$.**
""" + Q1_OMEGA + r"""
$$|\alpha_1-\alpha_2|<\frac\pi2\iff-\frac\pi2<\alpha_2-\alpha_1<\frac\pi2\iff\alpha_1-\frac\pi2<\alpha_2<\alpha_1+\frac\pi2.$$
זהו רצועה סביב האלכסון $\alpha_2=\alpha_1$ בין הישרים $\alpha_2=\alpha_1+\frac\pi2$ ו-$\alpha_2=\alpha_1-\frac\pi2$. מחוץ לרצועה שני משולשים ישרי-זווית שכל ניצב שלהם $\frac\pi2$, ולכן שטח הרצועה בתוך הריבוע הוא שטח הריבוע פחות שני המשולשים.
![הרצועה בין הישרים α2 = α1 ± π/2 בתוך הריבוע](images/exams/25S-B-Q1b-region.png)
$$P\left(|\alpha_1-\alpha_2|<\frac\pi2\right)=\frac{\pi^2-2\cdot\frac12\left(\frac\pi2\right)^2}{\pi^2}=\frac{\pi^2-\frac{\pi^2}{4}}{\pi^2}=\frac34.$$""",
    10, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"מה ההסתברות שהזווית $\beta$ היא זווית חדה **אם ידוע** כי $\alpha_2>2\alpha_1$?",
    r"""**$P\left(|\alpha_1-\alpha_2|<\frac\pi2\ \Big/\ \alpha_2>2\alpha_1\right)$.**
$$P\left(|\alpha_1-\alpha_2|<\frac\pi2\ \Big/\ \alpha_2>2\alpha_1\right)=\frac{P\left(|\alpha_1-\alpha_2|<\frac\pi2\cap\alpha_2>2\alpha_1\right)}{P(\alpha_2>2\alpha_1)}.$$
החיתוך הוא האזור בתוך המשולש $\{\alpha_2>2\alpha_1\}$ שמתחת לישר $\alpha_2=\alpha_1+\frac\pi2$ (המשולש עם קודקודים $(0,0)$, $(0,\frac\pi2)$ ו-$(\frac\pi2,\pi)$), ושטחו $\frac{\pi^2}{8}$:
$$P\left(|\alpha_1-\alpha_2|<\frac\pi2\cap\alpha_2>2\alpha_1\right)=\frac{\text{area}}{|\Omega|}=\frac{\pi^2/8}{\pi^2}=\frac18.$$
לכן
$$P\left(\cdots\ \Big/\ \alpha_2>2\alpha_1\right)=\frac{1/8}{1/4}=\frac12.$$""",
    10, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_CAP = r"לפניך רשימה של מספרים עוקבים בין $1$ ל-$(2N+1)$."

questions.append(Q(
    2, "א", "basics_events",
    r"נבחר באקראי מספר אחד מהרשימה. מה ההסתברות שהוא מתחלק ב-$2$ ללא שארית?",
    r"""**מספר זוגי.**
$A=\{1,2,3,\ldots,2N+1\}$, $|\Omega|=2N+1$. המספרים הזוגיים הם $2k$ עבור $1\le k\le N$, ולכן $|B|=N$ ו-
$$P(B)=\frac{N}{2N+1}.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ב", "combinatorics",
    r"נבחרים באקראי שני מספרים, אחד אחרי השני. **ב-1:** מה ההסתברות שסכום שני המספרים יהווה מספר זוגי?",
    r"""**הערה:** בניסוח המילולי של השאלה לא נאמר שההוצאה היא ללא החזרה, אך הפתרון הרשמי מניח הוצאה ללא החזרה ($X_1\ne X_2$), ובהתאם לכך מחושבות התשובות כאן.

**סכום זוגי.**
שני המספרים שונים זה מזה ($X_1\ne X_2$, $X_1,X_2\in A$). נסמן $C=\{X_1+X_2\text{ even}\}$ ו-$D_1=\{X_1\text{ even}\}$, $D_2=\{X_2\text{ even}\}$. הסכום זוגי אם ורק אם שני המספרים זוגיים או ששניהם אי-זוגיים:
$$C=(D_1\cap D_2)\cup(\bar D_1\cap\bar D_2).$$
$$P(D_1\cap D_2)=P(D_2\mid D_1)P(D_1)=\frac{N-1}{2N}\cdot\frac N{2N+1}=\frac{N-1}{2(2N+1)},$$
$$P(\bar D_1\cap\bar D_2)=P(\bar D_2\mid\bar D_1)P(\bar D_1)=\frac N{2N}\left(1-\frac N{2N+1}\right)=\frac N{2N}\cdot\frac{N+1}{2N+1}=\frac{N+1}{2(2N+1)}.$$
לכן
$$P(C)=\frac{N-1}{2(2N+1)}+\frac{N+1}{2(2N+1)}=\frac N{2N+1}.$$""",
    12, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"נבחרים באקראי שני מספרים, אחד אחרי השני. **ב-2:** אם ידוע כי המספר הראשון היה זוגי, מה ההסתברות שסכום שני המספרים יהווה מספר זוגי?",
    r"""**הערה:** בניסוח המילולי של השאלה לא נאמר שההוצאה היא ללא החזרה, אך הפתרון הרשמי מניח הוצאה ללא החזרה ($X_1\ne X_2$), ובהתאם לכך מחושבות התשובות כאן.

**סכום זוגי בהינתן שהראשון זוגי.**
$$P(C\mid D_1)=\frac{P(C\cap D_1)}{P(D_1)}.$$
$$C\cap D_1=\bigl((D_1\cap D_2)\cup(\bar D_1\cap\bar D_2)\bigr)\cap D_1=D_1\cap D_2,$$
כי $\bar D_1\cap D_1=\emptyset$. לכן
$$P(C\mid D_1)=\frac{P(D_1\cap D_2)}{P(D_1)}=\frac{\frac{N-1}{2(2N+1)}}{\frac N{2N+1}}=\frac{N-1}{2N}.$$""",
    8, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_CAP = (r"מספר מקרי ($X$) של אנשים נכנסים למסעדה ריקה, כאשר כל אחד מהם יהנה מארוחתו בהסתברות $p$ ולא יהנה ממנה בהסתברות $1-p$ "
          r"(בלי תלות בסועדים האחרים). בהנחה כי מספר הסועדים במסעדה מהווה משתנה פואסון, $X\sim P(\lambda)$, ענו על השאלות הבאות. "
          r"נגדיר משתנה מקרי $Y=\{$מספר האנשים שיהנו מהארוחה$\}$.")

HINT3 = "\n" + r"**לידיעתך:** $$\sum_{n=k}^{\infty}\frac{x^n}{(n-k)!}=x^ke^x.$$"

questions.append(Q(
    3, "א", "special_discrete",
    r"מהם הערכים האפשריים של משתנה מקרי $Y$?",
    r"""**הערכים האפשריים של $Y$.**
$X$ אינו חסום, ולכן
$$Y\in\{0,1,2,\ldots,n,\ldots\}.$$""",
    2, contextId="c3"))

questions.append(Q(
    3, "ב", "special_discrete",
    r"מצאו את פונקציית ההסתברות של משתנה מקרי $Y$." + HINT3,
    r"""**פונקציית ההסתברות של $Y$ (דילול פואסון).**
נשתמש בנוסחת ההסתברות השלמה על $X$:
$$P(Y=k)=\sum_{n=0}^{\infty}P(Y=k\mid X=n)P(X=n)=\sum_{n=k}^{\infty}P(Y=k\mid X=n)P(X=n),$$
כי כדי ש-$k$ אנשים יהנו, צריכים להיכנס לפחות $k$ אנשים (עבור $n<k$ ההסתברות המותנית אפס).
$$P(X=n)=e^{-\lambda}\frac{\lambda^n}{n!},\qquad P(Y=k\mid X=n)=\binom nk p^k(1-p)^{n-k},$$
כי בהינתן $n$ נכנסים, כל אחד נהנה בלי תלות באחרים. לכן
$$\begin{aligned}P(Y=k)&=\sum_{n=k}^{\infty}\binom nkp^k(1-p)^{n-k}e^{-\lambda}\frac{\lambda^n}{n!}\\&=\sum_{n=k}^{\infty}\frac{n!}{k!(n-k)!}p^k(1-p)^{n-k}e^{-\lambda}\frac{\lambda^n}{n!}\\&=\frac{e^{-\lambda}p^k}{k!}\sum_{n=k}^{\infty}\frac{(1-p)^{n-k}\lambda^n}{(n-k)!}.\end{aligned}$$
נציב $m=n-k$ (כלומר $n=m+k$), והסכום מתחיל ב-$m=0$:
$$P(Y=k)=\frac{e^{-\lambda}p^k\lambda^k}{k!}\sum_{m=0}^{\infty}\frac{\lambda^m(1-p)^m}{m!}=\frac{e^{-\lambda}p^k\lambda^k}{k!}\sum_{m=0}^{\infty}\frac{\bigl(\lambda(1-p)\bigr)^m}{m!}=\frac{e^{-\lambda}p^k\lambda^k}{k!}\,e^{\lambda(1-p)}.$$
(הסכום הוא טור טיילור של $e^x$ עבור $x=\lambda(1-p)$.) לכן
$$P(Y=k)=\frac{(\lambda p)^ke^{-\lambda p}}{k!},\qquad k=0,1,2,\ldots,$$
כלומר
$$Y\sim P(\lambda p).$$""",
    12, contextId="c3"))

questions.append(Q(
    3, "ג", "special_discrete",
    r"אם ידוע כי בדיוק $n$ אנשים נכנסו למסעדה, מה ההסתברות ש-$k$ מהם נהנו מהמסעדה?",
    r"""**בהינתן $n$ נכנסים, $k$ נהנו.**
בהינתן $X=n$, כל אחד מ-$n$ הנכנסים נהנה בהסתברות $p$ ללא תלות באחרים, ולכן
$$P(Y=k\mid X=n)=\binom nkp^k(1-p)^{n-k},\qquad k=0,1,\ldots,n.$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ד", "conditional_bayes",
    r"אם ידוע כי בדיוק $k$ אנשים נהנו מהמסעדה, מהי ההסתברות שנכנסו למסעדה $n$ אנשים?" + HINT3,
    r"""**בהינתן $k$ נהנו, $n$ נכנסו (נוסחת בייס).**
$$P(X=n\mid Y=k)=\frac{P(Y=k\mid X=n)P(X=n)}{P(Y=k)}.$$
נציב את התוצאות מהסעיפים הקודמים:
$$P(X=n\mid Y=k)=\frac{\binom nkp^k(1-p)^{n-k}\,e^{-\lambda}\dfrac{\lambda^n}{n!}}{\dfrac{(\lambda p)^ke^{-\lambda p}}{k!}}=\frac{\dfrac{n!}{k!(n-k)!}p^k(1-p)^{n-k}e^{-\lambda}\dfrac{\lambda^n}{n!}\,k!}{\lambda^kp^ke^{-\lambda p}}=\frac{(1-p)^{n-k}e^{-\lambda}\lambda^{n-k}}{(n-k)!\,e^{-\lambda p}}.$$
לכן
$$P(X=n\mid Y=k)=e^{-\lambda(1-p)}\frac{\bigl(\lambda(1-p)\bigr)^{n-k}}{(n-k)!},\qquad n\ge k.$$
כלומר $X-k\sim P\bigl(\lambda(1-p)\bigr)$ בהינתן $Y=k$.""",
    6, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_FX = (r"משתנה מקרי $X$ מתואר על ידי פונקציית צפיפות ההסתברות" "\n"
         r"$$f_X(x)=\begin{cases}a+\dfrac{b}{x\sqrt x}+cx,&0<x\le1\\0,&\text{else}\end{cases}$$")

questions.append(Q(
    4, "א", "continuous_rv",
    r"מהן המגבלות הכלליות על הערכים של המקדמים $a$, $b$ ו-$c$? עליך לנמק היטב!",
    r"""**מגבלות על המקדמים.**
צפיפות צריכה להיות מנורמלת:
$$\int_0^1\left(a+\frac{b}{x\sqrt x}+cx\right)dx=1.$$
האינטגרל $\int_0^1\frac{b}{x\sqrt x}\,dx$ מתכנס ב-$0$ רק אם $b=0$, כי $\frac{1}{x\sqrt x}=x^{-3/2}$ ו-$\frac32\ge1$. לכן
$$b=0.$$
אז
$$\int_0^1(a+cx)\,dx=\left(ax+c\frac{x^2}2\right)\Big|_0^1=a+\frac c2=1\quad\Longrightarrow\quad c=2-2a.$$
כלומר $f_X(x)=a+(2-2a)x$ ב-$(0,1]$.
נדרוש $f_X\ge0$: מכיוון שהפונקציה ליניארית ב-$[0,1]$, היא אי-שלילית שם אם ורק אם שני קצותיה אי-שליליים:
$$f_X(0)=a\ge0,\qquad f_X(1)=a+2-2a=2-a\ge0\ \Longrightarrow\ 0\le a\le2.$$
ומכאן $-2\le c\le2$.""",
    6, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"מצאו את **כל** המקדמים אם נתון כי $\mathbb{E}[X]=\mu$.",
    r"""**המקדמים כפונקציה של $\mu$.**
$$\mathbb{E}[X]=\int_0^1x\bigl(a+(2-2a)x\bigr)dx=\left[\frac{ax^2}2+(2-2a)\frac{x^3}3\right]_0^1=\frac a2+\frac{2-2a}3=\mu.$$
$$3a+4-4a=6\mu\quad\Longrightarrow\quad a=4-6\mu.$$
ולכן
$$a=4-6\mu,\qquad b=0,\qquad c=2-2(4-6\mu)=12\mu-6.$$""",
    6, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"האם ייתכן ש-$\mu=0$? למה?",
    r"""**האם $\mu=0$ אפשרי?**
לא. עבור $\mu=0$ מקבלים $a=4$, אבל $a$ חייב לקיים $0\le a\le2$ (סעיף א׳). לכן $\mu=0$ אינו אפשרי.""",
    3, contextId="c4"))

questions.append(Q(
    4, "ד", "continuous_rv",
    r"מהו הערך הקטן והגדול ביותר המותר של $\mu$?",
    r"""**התחום של $\mu$.**
$$0\le a=4-6\mu\le2\ \Longrightarrow\ -2\le6\mu-4\le0\ \Longrightarrow\ \frac13\le\mu\le\frac23.$$
לכן
$$\mu_{\min}=\frac13,\qquad\mu_{\max}=\frac23.$$""",
    6, contextId="c4"))

questions.append(Q(
    4, "ה", "continuous_rv",
    r"חשבו את ההסתברות $P(X\le1/2)$.",
    r"""**$P(X\le\frac12)$.**
$$P\left(X\le\frac12\right)=\int_0^{1/2}f_X(x)\,dx=\int_0^{1/2}\bigl(a+2(1-a)x\bigr)dx=\left[ax+(1-a)x^2\right]_0^{1/2}=\frac a2+\frac{1-a}4.$$
הצבת $a=4-6\mu$:
$$P\left(X\le\frac12\right)=\frac{4-6\mu}2+\frac{-3+6\mu}4=\frac54-\frac{3\mu}2.$$""",
    4, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_CAP = (r"ארבע יחידות $A$, $B$, $C$, $D$ פועלות ללא תלות אחת בשנייה בהסתברויות זהות $P(A)=P(B)=P(C)=P(D)=p$. "
          r"מיחידות אלו מרכיבים את המעגל הראשון ולאחר מכן את המעגל השני, בהתאם לאיור. "
          r"במעגל הראשון $D$ בטור עם הצירוף של ענף ($A$ ו-$B$ בטור) במקביל ל-$C$; במעגל השני $B$ בטור עם הצירוף של $D$ במקביל לענף ($A$ ו-$C$ בטור).")
NOTE5 = "\n" + r"**הערה:** אסור להשתמש ב״טבלת אמת״ בפתרון השאלה!"

questions.append(Q(
    5, "א", "circuits",
    r"מהי ההסתברות שהמעגל הראשון פועל?" + NOTE5,
    r"""**$P(Q_1)$.**
המעגל הראשון פועל אם $D$ פועל וגם ($A$ ו-$B$ פועלים, או $C$ פועל):
$$Q_1=D\cap\bigl((A\cap B)\cup C\bigr).$$
$$P(Q_1)=P(D)\,P\bigl((A\cap B)\cup C\bigr)=P(D)\Bigl[P(A\cap B)+P(C)-P(A\cap B\cap C)\Bigr]=p\bigl[p^2+p-p^3\bigr]=p^3+p^2-p^4.$$""",
    5, contextId="c5"))

questions.append(Q(
    5, "ב", "circuits",
    r"מהי ההסתברות ששני המעגלים יפעלו?" + NOTE5,
    r"""**$P(Q_1\cap Q_2)$.**
המעגל השני: $Q_2=B\cap\bigl(D\cup(A\cap C)\bigr)$. נסמן $G=Q_1\cap Q_2$ ונחשב לפי ארבעת המצבים של $(A,B)$:
$$P(G)=P(G\mid A\cap B)P(A\cap B)+P(G\mid A\cap\bar B)P(A\cap\bar B)+P(G\mid\bar A\cap B)P(\bar A\cap B)+P(G\mid\bar A\cap\bar B)P(\bar A\cap\bar B).$$
• אם $B$ לא פועל, $Q_2$ לא פועל (הוא בטור עם $B$), ולכן $P(G\mid A\cap\bar B)=P(G\mid\bar A\cap\bar B)=0$.
• $A,B$ פועלים: $Q_1$ פועל בדיוק כש-$D$ פועל, ו-$Q_2$ פועל כש-$D$ או $C$ פועל; לכן $G$ פועל בדיוק כש-$D$ פועל, ו-$P(G\mid A\cap B)=p$.
• $\bar A$ ו-$B$ פועל: $Q_1$ פועל אם $D$ וגם $C$ פועלים, ו-$Q_2$ פועל אם $D$ פועל, ולכן $P(G\mid\bar A\cap B)=P(D\cap C)=p^2$.
$$P(G)=p\cdot p^2+p^2\cdot(1-p)\cdot p=p^3+p^3-p^4=2p^3-p^4.$$""",
    12, contextId="c5"))

questions.append(Q(
    5, "ג", "conditional_bayes",
    r"אם ידוע כי שני המעגלים פועלים, מה ההסתברות שכל היחידות תקינות (כלומר, פועלות)?" + NOTE5,
    r"""**$P(A\cap B\cap C\cap D\mid G)$.**
$$P(A\cap B\cap C\cap D\mid G)=\frac{P(G\mid A\cap B\cap C\cap D)\,P(A\cap B\cap C\cap D)}{P(G)}=\frac{1\cdot p^4}{2p^3-p^4}=\frac{p}{2-p}.$$""",
    8, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_CAP = (r"מטילים פעמיים קובייה הוגנת, בעלת $N$ פאות. נסמן ב-$X_1$ וב-$X_2$ את תוצאות ההטלות. "
          r"נגדיר משתנה מקרי דו ממדי $(X_{\min},X_{\max})$ כאשר $X_{\min}=\min(X_1,X_2)$ ו-$X_{\max}=\max(X_1,X_2)$.")

questions.append(Q(
    6, "א", "minmax_transform",
    r"מצאו את פונקציית ההסתברות המשותפת $P(X_{\min}=k,X_{\max}=\ell)$ תוך ציון של ערכים אפשריים של $k$ ו-$\ell$.",
    r"""**ההתפלגות המשותפת.**
$$P(X_{\min}=k,X_{\max}=\ell)=\begin{cases}0,&k>\ell\\P(X_1=X_2=i),&k=\ell=i,\ 1\le i\le N\\P(X_1=k,X_2=\ell)+P(X_1=\ell,X_2=k),&k<\ell\end{cases}$$
כלומר
$$P(X_{\min}=k,X_{\max}=\ell)=\begin{cases}0,&k>\ell\\\dfrac1{N^2},&k=\ell=i,\ 1\le i\le N\\\dfrac2{N^2},&k<\ell\end{cases}$$
(הערכים האפשריים: $k,\ell\in\{1,\ldots,N\}$ עם $k\le\ell$.)""",
    9, contextId="c6"))

questions.append(Q(
    6, "ב", "minmax_transform",
    r"מצאו את פונקציית ההסתברות השולית עבור משתנה מקרי $X_{\min}$.",
    r"""**ההתפלגות השולית של $X_{\min}$.**
$$P(X_{\min}=k)=P(X_{\min}=k,X_{\max}=k)+\sum_{\ell=k+1}^{N}P(X_{\min}=k,X_{\max}=\ell)=\frac1{N^2}+\frac2{N^2}(N-k)=\frac{1+2(N-k)}{N^2},\qquad k=1,2,\ldots,N.$$""",
    6, contextId="c6"))

questions.append(Q(
    6, "ג", "minmax_transform",
    r"מצאו את פונקציית ההסתברות השולית עבור משתנה מקרי $X_{\max}$.",
    r"""**ההתפלגות השולית של $X_{\max}$.**
$$P(X_{\max}=\ell)=P(X_{\min}=\ell,X_{\max}=\ell)+\sum_{k=1}^{\ell-1}P(X_{\min}=k,X_{\max}=\ell)=\frac1{N^2}+\frac2{N^2}(\ell-1)=\frac{1+2(\ell-1)}{N^2},\qquad \ell=1,2,\ldots,N.$$""",
    6, contextId="c6"))

questions.append(Q(
    6, "ד", "minmax_transform",
    r"האם $X_{\min}$ ו-$X_{\max}$ הם משתנים מקריים תלויים או בלתי תלויים? נמקו היטב!",
    r"""**אי-תלות.**
המשתנים תלויים:
$$P(X_{\min}=2,X_{\max}=1)=0\ne P(X_{\min}=2)\cdot P(X_{\max}=1)=\frac{1+2(N-2)}{N^2}\cdot\frac1{N^2}=\frac{1+2(N-2)}{N^4}.$$
(עבור $N\ge2$.)""",
    4, contextId="c6"))

# ------------------------------------------------------------------ area regions + simulations (RAW_SCHEMA `region`, `sim`)
_SQ = {"x": [0, "pi"], "y": [0, "pi"]}
_LB = {"x": "α1", "y": "α2"}
_UP = {"a": -2, "b": 1, "c": 0, "op": ">"}
_STRIP = [{"a": -1, "b": 1, "c": "pi/2", "op": "<"}, {"a": -1, "b": 1, "c": "-pi/2", "op": ">"}]
REGIONS = {
    (1, "א"): {"space": _SQ, "labels": _LB, "event": [_UP], "exact": 0.25, "caption": "האזור α2>2α1"},
    (1, "ב"): {"space": _SQ, "labels": _LB, "event": _STRIP, "exact": 0.75, "caption": "β חדה: |α1-α2|<π/2"},
    (1, "ג"): {"space": _SQ, "labels": _LB, "event": _STRIP, "given": [_UP], "exact": 0.5, "caption": "β חדה בהינתן α2>2α1"},
}
SIMS = {
    (1, "א"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(a2>2a1)", "exact": 0.25},
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(|a1-a2|<pi/2)", "exact": 0.75},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(|a1-a2|<pi/2 | a2>2a1)", "exact": 0.5},
}

# ---- step-author additions: sims at sample parameter values for the symbolic answers
def _thinning_rows(lam=2.0, p=0.3, K=40):
    """X ~ Poisson(lam) diners, each enjoys with probability p: joint (X, Y); tail beyond K is ~1e-38"""
    rows = []
    for x in range(K + 1):
        px = math.exp(-lam) * lam ** x / math.factorial(x)
        for y in range(x + 1):
            rows.append({"p": px * math.comb(x, y) * p ** y * (1 - p) ** (x - y), "X": x, "Y": y})
    tot = sum(r["p"] for r in rows)
    rows[-1]["p"] += 1 - tot
    return rows


def _comp(i, p):
    return {"type": "comp", "id": i, "p": p}


_PC = 0.6                                                    # Q5: every unit works with probability p = 0.6
_Q1NET = {"type": "series", "children": [_comp("D", _PC), {"type": "parallel", "children": [
    {"type": "series", "children": [_comp("A", _PC), _comp("B", _PC)]}, _comp("C", _PC)]}]}
_G = "S == 1 and B == 1 and (D == 1 or (A == 1 and C == 1))"   # Q1 works and Q2 = B and (D or (A and C)) works
_NUMS = {"values": list(range(1, 10)), "draws": 2, "replace": False}
SIMS.update({
    (2, "א"): dict(kind="urn", params={"values": list(range(1, 10)), "draws": 1, "event": "v1 % 2 == 0"}, estimate="P(even), N=4", exact=4 / 9),
    (2, "ב"): dict(kind="urn", params=dict(_NUMS, event="(v1+v2) % 2 == 0"), estimate="P(sum even), N=4", exact=4 / 9),
    (2, "ג"): dict(kind="urn", params=dict(_NUMS, event="(v1+v2) % 2 == 0", given="v1 % 2 == 0"),
                   estimate="P(sum even | first even), N=4", exact=3 / 8),
    (3, "ב"): dict(kind="custom_discrete", params={"joint": _thinning_rows(), "event": "Y == 1"},
                   estimate="P(Y=1), lambda=2 p=0.3", exact=0.6 * math.exp(-0.6)),
    (3, "ג"): dict(kind="custom_discrete", params={"vars": {"Z%d" % i: {"values": [0, 1], "probs": [0.7, 0.3]} for i in range(1, 6)},
                                                    "event": "Z1+Z2+Z3+Z4+Z5 == 2"},
                   estimate="P(Y=2 | X=5), p=0.3", exact=math.comb(5, 2) * 0.3 ** 2 * 0.7 ** 3),
    (3, "ד"): dict(kind="custom_discrete", params={"joint": _thinning_rows(), "event": "X == 3", "given": "Y == 1"},
                   estimate="P(X=3 | Y=1), lambda=2 p=0.3", exact=math.exp(-1.4) * 1.4 ** 2 / 2),
    (4, "ה"): dict(kind="pdf", params={"pieces": [{"from": 0, "to": 1, "expr": "1.6-1.2*x"}], "event": "x <= 0.5"},
                   estimate="P(X<=1/2), mu=0.4", exact=0.65),
    (5, "א"): dict(kind="circuit", params={"network": _Q1NET, "event": "S == 1"}, estimate="P(Q1), p=0.6", exact=_PC ** 3 + _PC ** 2 - _PC ** 4),
    (5, "ב"): dict(kind="circuit", params={"network": _Q1NET, "event": _G}, estimate="P(Q1 and Q2), p=0.6", exact=2 * _PC ** 3 - _PC ** 4),
    (5, "ג"): dict(kind="circuit", params={"network": _Q1NET, "event": "A+B+C+D == 4", "given": _G},
                   estimate="P(all work | both circuits work), p=0.6", exact=_PC / (2 - _PC)),
    (6, "א"): dict(kind="dice", params={"n": 2, "faces": 6, "event": "min == 2 and max == 5"}, estimate="P(min=2,max=5), N=6", exact=2 / 36),
    (6, "ב"): dict(kind="dice", params={"n": 2, "faces": 6, "event": "min == 2"}, estimate="P(min=2), N=6", exact=9 / 36),
    (6, "ג"): dict(kind="dice", params={"n": 2, "faces": 6, "event": "max == 4"}, estimate="P(max=4), N=6", exact=7 / 36),
})

for _q in questions:
    _k = (_q["num"], _q.get("part"))
    if _k in REGIONS:
        _q["region"] = REGIONS[_k]
    if _k in SIMS:
        _q["sim"] = SIMS[_k]

# ---- step-author: rubric, pitfalls, guided steps. Data in steps_25S_B.py; every value is re-derived in
# tools/verify/25S-B/steps_check.py (exact + Monte Carlo).
import probsteps
from steps_25S_B import DATA as _STEPS
probsteps.apply(questions, _STEPS, CODE)

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר קיץ תשפ״ה, מועד ב (10.11.2025)",
    "year": 2025,
    "examDate": "10.11.2025",
    "sourceFile": "25S-B exam pp.1-3",
    "solutionFile": "25S-B handwritten official solutions pp.4-15",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: מחוגים", "image": IMG + "Q1-clock.png", "caption": Q1_CAP},
        "c2": {"kind": "text", "title": "שאלה 2: רשימת מספרים", "text": Q2_CAP},
        "c3": {"kind": "text", "title": "שאלה 3: מסעדה", "text": Q3_CAP},
        "c4": {"kind": "text", "title": "שאלה 4", "text": Q4_FX},
        "c5": {"kind": "image", "title": "שאלה 5: מעגלים", "image": IMG + "Q5-circuits.png", "caption": Q5_CAP},
        "c6": {"kind": "text", "title": "שאלה 6: קובייה", "text": Q6_CAP},
    },
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
