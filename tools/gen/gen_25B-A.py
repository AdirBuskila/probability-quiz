# -*- coding: utf-8 -*-
"""Generator for tools/raw/25B-A.json -- probability (course 20021), semester B 2025, moed A (15.07.2025).
6 questions, 25 items (Q1 5, Q2 5, Q3 3, Q4 4, Q5 5, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25B-A.py

Source: exam pp.1-3, handwritten official solutions on grid paper pp.4-19 (all questions have a solution).
Student/lecturer names printed on the cover page are not copied.

Transcription notes
- Part keys: single letters. Q2 prints sub-parts "א-1", "א-2", "א-3" and Q5 prints "ב-1" ... "ב-4"; they are stored as
  consecutive letters and the printed label is the first bold token of each question text.
  Q2: a=א-1, b=א-2, c=א-3, d=ב, e=ג.  Q5: a=א, b=ב-1, c=ב-2, d=ב-3, e=ב-4.  Q6: a=א, b=ב-1, c=ב-2.
- Q4: the printed density has the term c/x^3+g on x>=1. The official solution shows that finite variance forces
  c=0 and g=0 (stated in the question text as "ושונות סופית"), so a and b are the only free coefficients.
- Q5: "the new circuit" is the same three units placed at random (6 equally likely arrangements); the official solution
  lists the six arrangements in a table (Q1..Q6, three of them equal to Q0 or each other).
- Q1-type area items carry `region` data (REGIONS below; RAW_SCHEMA `region`).
- Math never holds Hebrew.
"""
import json, math, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25B-A.json"
CODE = "25B-A"
IMG = "images/exams/25B-A-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"לפניך משולש ישר זווית ושווה שוקיים בעל שטח $1/2$. על שתי צלעותיו נבחרו **באקראי** שתי נקודות $A$ ו-$B$ כמתואר באיור. "
          r"יהיו $X$ ו-$Y$ שני משתנים מקריים רציפים המתארים את מיקומן של $A$ ו-$B$.")

questions.append(Q(
    1, "א", "uniform_geometric",
    r"איך המשתנים $X$ ו-$Y$ מפולגים? **נמקו!**",
    r"""המשולש ישר זווית ושווה שוקיים ושטחו $\frac12$, ולכן אורך כל אחת משתי הצלעות הניצבות הוא $1$.
כאשר הנקודות $A$ ו-$B$ נבחרות באקראי על הצלעות, מקבלים
$$X\sim U_c(0,1),\qquad Y\sim U_c(0,1),$$
כלומר שני משתנים אחידים רציפים על $(0,1)$ (ובחירת שתי הנקודות בלתי תלויה).""",
    4, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"יהי $L$ אורך הקטע $AB$. מצאו את ההסתברות $P(L<1)$.",
    r"""נשתמש בגישה הקלאסית. $L=\sqrt{X^2+Y^2}$, ולכן
$$P(L<1)=P(X^2+Y^2<1)=\frac{\left|\{x^2+y^2<1\}\right|}{|\Omega|},\qquad |\Omega|=1.$$
האזור $\{x^2+y^2<1\}$ בתוך ריבוע היחידה הוא רבע עיגול ברדיוס $1$, ושטחו $\frac{\pi}{4}$. לכן
$$P(L<1)=\frac{\pi}{4}\approx 0.79.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"יהי $S$ שטח המשולש $OAB$. מצאו את ההסתברות $P(S<1/4)$.",
    r"""שטח המשולש $OAB$ הוא $S=\frac12XY$. לכן
$$P(S<\tfrac14)=P(\tfrac12XY<\tfrac14)=P(XY<\tfrac12)=P\left(Y<\frac{1}{2X}\right)=\frac{\left|\{Y<\frac1{2X}\}\right|}{|\Omega|},\qquad|\Omega|=1.$$
ההיפרבולה $y=\frac1{2x}$ חותכת את ריבוע היחידה ב-$x=\frac12$. עבור $0<x<\frac12$ כל $0<y<1$ מתאים, ועבור $\frac12<x<1$ מתקבל $0<y<\frac1{2x}$. לכן
$$\left|\{Y<\tfrac1{2X}\}\right|=\frac12\cdot 1+\int_{1/2}^{1}\frac{dx}{2x}=\frac12+\frac12\ln x\Big|_{1/2}^{1}=\frac12(1+\ln 2).$$
ולכן
$$P(S<\tfrac14)=\frac12(1+\ln2)\approx0.85.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ד", "uniform_geometric",
    r"מצאו את ההסתברות המותנית $P(L<1\,/\,S<1/4)$.",
    r"""לפי ההגדרה
$$P(L<1\mid S<\tfrac14)=\frac{P(L<1\cap S<\frac14)}{P(S<\frac14)},\qquad P(S<\tfrac14)=\frac12(1+\ln2).$$
נמצא את החיתוך. הקימור $y=\frac1{2x}$ והמעגל $x^2+y^2=1$ נחתכים בנקודה שבה
$$x^2+\frac1{4x^2}=1\ \Longrightarrow\ x=y=\frac1{\sqrt2}.$$
רבע העיגול כולו נמצא מתחת להיפרבולה (בתחום $x^2+y^2<1$ מתקיים $xy<\frac12$), ולכן
$$P(L<1\cap S<\tfrac14)=P(X^2+Y^2<1)=P(L<1)=\frac{\pi}{4}.$$
מכאן
$$P(L<1\mid S<\tfrac14)=\frac{P(L<1)}{P(S<\frac14)}=\frac{\pi/4}{\frac12(1+\ln2)}=\frac{\pi}{2(1+\ln2)}\approx0.93.$$""",
    5, contextId="c1"))

questions.append(Q(
    1, "ה", "continuous_rv",
    r"חשבו תוחלת $\mathbb{E}[S]$ ושונות $\operatorname{var}[S]$ של שטח המשולש.",
    r"""$$\mathbb{E}[S]=\mathbb{E}\left[\tfrac12XY\right]=\frac12\,\mathbb{E}[X]\,\mathbb{E}[Y]=\frac12\cdot\frac12\cdot\frac12=\frac18.$$
עבור השונות,
$$\operatorname{Var}[S]=\operatorname{Var}\left[\tfrac12XY\right]=\frac14\operatorname{Var}[XY].$$
מאי-תלות, $\mathbb{E}[X^2]=\mathbb{E}[Y^2]=\frac13$ ו-$\mathbb{E}[X]=\mathbb{E}[Y]=\frac12$, ולכן
$$\operatorname{Var}[XY]=\mathbb{E}[X^2]\,\mathbb{E}[Y^2]-\bigl(\mathbb{E}[X]\,\mathbb{E}[Y]\bigr)^2=\frac19-\frac1{16}=\frac7{144}.$$
הצבה נותנת
$$\operatorname{Var}[S]=\frac14\cdot\frac7{144}=\frac7{576}\approx0.012.$$""",
    6, contextId="c1"))

# ------------------------------------------------------------------ Q2
Q2_TXT = r"יהיו $A$ ו-$B$ מאורעות לא ריקים. נתון כי $P(A/B)=p$, $P(\overline{A}/\overline{B})=q$ ו-$P(A\cup B)=s$."

SOL2_BASE = r"""נסמן את הנתונים: $P(A/B)=p$, $P(\overline A/\overline B)=q$, $P(A\cup B)=s$.
מהנתון הראשון
$$P(A/B)=\frac{P(A\cap B)}{P(B)}=\frac{P(A)+P(B)-P(A\cup B)}{P(B)}=p\ \Longrightarrow\ P(A)+(1-p)P(B)=s.\qquad(1)$$
מהנתון השני
$$P(\overline A/\overline B)=\frac{P(\overline{A\cup B})}{P(\overline B)}=\frac{1-s}{1-P(B)}=q\ \Longrightarrow\ P(B)=1-\frac{1-s}{q}.\qquad(2)$$"""

questions.append(Q(
    2, "א", "conditional_bayes",
    r"חשבו את ההסתברות $P(A)$." "\n" r"**(א-1):** $P(A)$ (5 נק׳).",
    SOL2_BASE + r"""
נציב את $(2)$ ב-$(1)$:
$$P(A)=s-(1-p)P(B)=s-(1-p)\left(1-\frac{1-s}{q}\right).$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ב", "conditional_bayes",
    r"חשבו את ההסתברות $P(B)$." "\n" r"**(א-2):** $P(B)$ (5 נק׳).",
    SOL2_BASE + r"""
לכן, לפי $(2)$,
$$P(B)=1-\frac{1-s}{q}.$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ג", "conditional_bayes",
    r"חשבו את ההסתברות $P(A\cap B)$." "\n" r"**(א-3):** $P(A\cap B)$ (5 נק׳).",
    SOL2_BASE + r"""
לפי $P(A\cap B)=P(A)+P(B)-P(A\cup B)$ ומהנתון הראשון $P(A\cap B)=p\,P(B)$:
$$P(A\cap B)=p\,P(B)=p\left(1-\frac{1-s}{q}\right).$$""",
    5, contextId="c2"))

questions.append(Q(
    2, "ד", "basics_events",
    r"האם ייתכן כי $q<1-s$? **נמקו היטב!** (5 נק׳)",
    r"""מ-$P(B)\ge0$ נקבל
$$1-\frac{1-s}{q}\ge0\ \Longleftrightarrow\ q\ge1-s.$$
לכן $q<1-s$ **אינו** יכול להתקיים: התשובה היא לא, כי אז $P(B)$ היה שלילי.""",
    5, contextId="c2"))

questions.append(Q(
    2, "ה", "independence",
    r"עבור אילו פרמטרים $p$, $q$ ו-$s$ המאורעות $A$ ו-$B$ יהיו מאורעות **בלתי תלויים**? (5 נק׳)",
    r"""אם $A$ ו-$B$ בלתי תלויים, אז
$$P(A/B)=P(A)=p,$$
וגם
$$P(\overline A/\overline B)=P(\overline A)=q.$$
מכאן $q=P(\overline A)=1-P(A)=1-p$, כלומר
$$p=1-q.$$
להפך, אם $p=1-q$ אז $P(A)=s-(1-p)P(B)=s-q\cdot\frac{q+s-1}q=1-q=p=P(A/B)$, ולכן $A$ ו-$B$ בלתי תלויים (לכל $s$).""",
    5, contextId="c2"))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"אסתר נמצאת בצד אחד של הנהר ועליה לעבור מגדה א׳ לגדה ב׳. ידוע כי בין שתי הגדות ישנם שלושה גשרים. "
          r"על הגשר הראשון ישנם $N_1$ שערים, ועל הגשר השני והשלישי $N_2$ ו-$N_3$ שערים בהתאמה. "
          r"בהנחה כי כל שער פתוח בהסתברות $p$ (ללא קשר ליתר השערים),")

SOL3_BASE = r"""נגדיר את המאורעות
$Q=\{$אסתר עוברת מגדה א׳ לגדה ב׳$\}$ ולכל $j=1,2,3$:
$A_j=\{$אסתר יכולה לעבור דרך גשר מס׳ $j\}$.
אסתר עוברת דרך גשר $j$ אם ורק אם כל $N_j$ השערים שעליו פתוחים, ולכן $P(A_j)=p^{N_j}$, והגשרים בלתי תלויים."""

questions.append(Q(
    3, "א", "circuits",
    r"מצאו את ההסתברות שאסתר תצליח לעבור מגדה אחת לשנייה. (15 נק׳)",
    SOL3_BASE + r"""
$Q=A_1\cup A_2\cup A_3$, ולכן
$$P(Q)=1-P(\overline Q)=1-P(\overline{A_1}\cap\overline{A_2}\cap\overline{A_3})=1-P(\overline{A_1})P(\overline{A_2})P(\overline{A_3})$$
לפי אי-התלות. מאחר ש-$P(\overline{A_j})=1-p^{N_j}$,
$$P(Q)=1-\left(1-p^{N_1}\right)\left(1-p^{N_2}\right)\left(1-p^{N_3}\right).$$""",
    15, contextId="c3"))

questions.append(Q(
    3, "ב", "conditional_bayes",
    r"**אם ידוע** כי אסתר הצליחה לעבור מגדה לגדה, מהי ההסתברות שהיא עשתה זאת באמצעות הגשר השני? (5 נק׳)",
    SOL3_BASE + r"""
לפי נוסחת בייס
$$P(A_2/Q)=\frac{P(Q/A_2)\,P(A_2)}{P(Q)},\qquad P(Q/A_2)=1.$$
לכן
$$P(A_2/Q)=\frac{p^{N_2}}{1-\left(1-p^{N_1}\right)\left(1-p^{N_2}\right)\left(1-p^{N_3}\right)}.$$""",
    5, contextId="c3"))

questions.append(Q(
    3, "ג", "conditional_bayes",
    r"**אם ידוע** כי אסתר הצליחה לעבור מגדה לגדה, מהי ההסתברות שהיא **לא** עשתה זאת באמצעות הגשר השני? (5 נק׳)",
    SOL3_BASE + r"""
לפי סעיף ב׳ ומשלים,
$$P(\overline{A_2}/Q)=1-P(A_2/Q)=1-\frac{p^{N_2}}{1-\left(1-p^{N_1}\right)\left(1-p^{N_2}\right)\left(1-p^{N_3}\right)}.$$""",
    5, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"משתנה מקרי $X$, בעל תוחלת $\mathbb{E}[X]=\mu$ **ושונות סופית**, מתואר על ידי פונקציית צפיפות ההסתברות מהצורה" "\n"
          r"$$f_X(x)=\begin{cases}0,&x<-1;\\a(x+1),&-1\le x<0;\\b,&0\le x<1;\\c/x^3+g,&x\ge1.\end{cases}$$")

questions.append(Q(
    4, "א", "continuous_rv",
    r"אנא מצאו את המקדמים $a$, $b$, $c$ ו-$g$. ייתכן ותשובתיך יכללו את $\mu$. (8 נק׳)",
    r"""**תחילה $g$ ו-$c$.** מאחר שהשונות סופית, $\mathbb{E}[X^2]$ סופי. התרומה של $x\ge1$ היא
$$\int_1^\infty x^2\left(\frac{c}{x^3}+g\right)dx=c\int_1^\infty\frac{dx}{x}+g\int_1^\infty x^2\,dx.$$
האינטגרלים $\int_1^\infty\frac{dx}{x}$ ו-$\int_1^\infty x^2dx$ מתבדרים, ולכן, כדי שהאינטגרל יתכנס, חייב להתקיים $g=0$ ו-$c=0$.
כעת הצפיפות היא $a(x+1)$ על $[-1,0)$, $b$ על $[0,1)$ ו-$0$ אחרת.

**נרמול:**
$$a\int_{-1}^0(x+1)\,dx+b\int_0^1dx=1\ \Longrightarrow\ \frac a2+b=1.$$
**תוחלת:**
$$\mu=a\int_{-1}^0x(x+1)\,dx+b\int_0^1x\,dx=a\cdot\left(-\frac16\right)+\frac b2\ \Longrightarrow\ b-\frac a3=2\mu.$$
פתרון שתי המשוואות נותן
$$a=\frac65(1-2\mu),\qquad b=\frac25(1+3\mu),\qquad c=0,\quad g=0.$$""",
    8, contextId="c4"))

questions.append(Q(
    4, "ב", "continuous_rv",
    r"מהו הערך הקטן והגדול ביותר של התוחלת $\mu$? **נמקו!** (5 נק׳)",
    r"""צפיפות חייבת להיות אי-שלילית, ולכן $a\ge0$ ו-$b\ge0$:
$$a\ge0\Rightarrow1-2\mu\ge0\Rightarrow\mu\le\frac12,\qquad b\ge0\Rightarrow1+3\mu\ge0\Rightarrow\mu\ge-\frac13.$$
לכן
$$-\frac13\le\mu\le\frac12.$$""",
    5, contextId="c4"))

questions.append(Q(
    4, "ג", "continuous_rv",
    r"בהינתן הפרמטרים מסעיף א׳, חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו את התוצאה. (8 נק׳)",
    r"""$F_X(t)=\int_{-\infty}^tf_X(x)\,dx$. נפרק לתחומים:

עבור $t<-1$: $F_X(t)=0$.
עבור $-1\le t<0$: $F_X(t)=\dfrac a2(t+1)^2$.
עבור $0\le t<1$: $F_X(t)=\dfrac a2+bt$.
עבור $t\ge1$: $F_X(t)=1$.

הצבת $a$ ו-$b$:
$$F_X(t)=\begin{cases}0,&t<-1,\\\dfrac35(1-2\mu)(t+1)^2,&-1\le t<0,\\\dfrac35(1-2\mu)+\dfrac25(1+3\mu)\,t,&0\le t<1,\\1,&t\ge1.\end{cases}$$
הגרף: אפס עד $-1$, עלייה פרבולית ל-$\frac35(1-2\mu)$ ב-$t=0$, אחר כך עלייה לינארית עד $1$ ב-$t=1$, ואז קבוע $1$.""",
    8, contextId="c4"))

questions.append(Q(
    4, "ד", "continuous_rv",
    r"מהי ההסתברות המותנית $P(X<1\,/\,X>-1/2)$? (4 נק׳)",
    r"""$$P(X<1\mid X>-\tfrac12)=\frac{P(-\frac12<X<1)}{P(X>-\frac12)}=\frac{F_X(1)-F_X(-\frac12)}{1-F_X(-\frac12)}=\frac{1-F_X(-\frac12)}{1-F_X(-\frac12)}=1,$$
כי $F_X(1)=1$ (הצפיפות מתאפסת מימין ל-$1$).""",
    4, contextId="c4"))

# ------------------------------------------------------------------ Q5
Q5_TXT = r"לפניך מעגל חשמלי ($\boldsymbol{Q_0}$) המורכב מיחידות $A$, $B$ ו-$C$ הפועלות ללא תלות אחת בשנייה בהסתברויות הזהות $p$."

Q5_B = (r"מפרקים מעגל $Q_0$ ומרכיבים – **מאותן היחידות** $A$, $B$ ו-$C$ – מעגל חדש **עם טופולוגיה זהה**. בין היתר, "
        r"יכול להתקבל אותו מעגל בדיוק ($Q_0$) אך יכול להתקבל גם מעגל עם היחידות $A$, $B$ ו-$C$ שנמצאות במקומות אחרים, כגון: "
        r"(ראו איור: דוגמה לאחת האפשרויות למעגל החדש). "
        r"(שימו לב, כי אין מידע על מיקום הימצאות מדויק של כל יחידה ויחידה!)")

Q5_SOL_B = r"""המעגל החדש $Q'$ מורכב מאותן שלוש יחידות באותה טופולוגיה ($L_1$ בטור עם המקבילה של $R_1$ ו-$R_2$), אך מקום היחידות נקבע באקראי. יש $3!=6$ סידורים אפשריים והם שווי הסתברות ($\frac16$ כל אחד):

- סידור I: ($R_2,R_1,L_1)=(C,B,A)$, המעגל $Q_1\equiv Q_0$;
- סידור II: $(B,C,A)$, המעגל $Q_2\equiv Q_0$;
- סידור III: $(C,A,B)$, המעגל $Q_3$;
- סידור IV: $(B,A,C)$, המעגל $Q_4$;
- סידור V: $(A,B,C)$, המעגל $Q_5\equiv Q_4$;
- סידור VI: $(A,C,B)$, המעגל $Q_6\equiv Q_3$."""

questions.append(Q(
    5, "א", "circuits",
    r"מהי ההסתברות שמעגל זה פועל? (3 נק׳)",
    r"""$Q_0=A\cap(B\cup C)$. לכן, מאי-תלות,
$$P(Q_0)=P(A)\,P(B\cup C)=p\,(2p-p^2)=p^2(2-p).$$""",
    3, contextId="c5"))

questions.append(Q(
    5, "ב", "circuits",
    Q5_B + "\n" + r"**ב-1:** מהי ההסתברות שהמעגל החדש (**עם מיקום לא ידוע של היחידות**) יפעל? (3 נק׳)",
    r"""מכיוון שהמעגל החדש בנוי מאותן שלוש יחידות באותה טופולוגיה, ולכל היחידות אותה הסתברות $p$, ההסתברות שהוא פועל היא כמו של $Q_0$:
$$P(Q')=p^2(2-p).$$""",
    3, contextId="c5", image=IMG + "Q5-example.png"))

questions.append(Q(
    5, "ג", "circuits",
    Q5_B + "\n" + r"**ב-2:** מהי ההסתברות שגם המעגל המקורי וגם המעגל החדש יפעלו? (10 נק׳)",
    Q5_SOL_B + r"""

לפי נוסחת ההסתברות השלמה על ששת הסידורים,
$$P(Q_0\cap Q')=\sum_{i=\mathrm{I}}^{\mathrm{VI}}P(Q_0\cap Q'\mid i)\,P(i),\qquad P(i)=\tfrac16.$$
- I ו-II: $Q'=Q_0$ ולכן $P(Q_0\cap Q'\mid i)=P(Q_0)=p^2(2-p)$.
- III ו-VI: $Q_3=B\cap(A\cup C)$. אז
$$Q_0\cap Q_3=A\cap(B\cup C)\cap B\cap(A\cup C)=\bigl[(A\cap B)\cup(A\cap C)\bigr]\cap\bigl[(A\cap B)\cup(B\cap C)\bigr]=(A\cap B)\cup(A\cap B\cap C)=A\cap B,$$
ולכן $P(Q_0\cap Q'\mid i)=P(A\cap B)=p^2$.
- IV ו-V: $Q_4=C\cap(A\cup B)$. אז $Q_0\cap Q_4=A\cap(B\cup C)\cap C\cap(A\cup B)=A\cap C$, ולכן $P(Q_0\cap Q'\mid i)=p^2$.

מכאן
$$P(Q_0\cap Q')=\frac16\Bigl\{2p^2(2-p)+4p^2\Bigr\}=\frac{p^2}{3}(4-p).$$""",
    10, contextId="c5", image=IMG + "Q5-example.png"))

questions.append(Q(
    5, "ד", "circuits",
    Q5_B + "\n" + r"**ב-3:** **אם ידוע** כי המעגל המקורי ($Q_0$) פעל, מהי ההסתברות שגם המעגל החדש יפעל? (5 נק׳)",
    r"""לפי ההגדרה ומסעיפים קודמים,
$$P(Q'/Q_0)=\frac{P(Q_0\cap Q')}{P(Q_0)}=\frac{\frac{p^2}{3}(4-p)}{p^2(2-p)}=\frac13\cdot\frac{4-p}{2-p}.$$""",
    5, contextId="c5", image=IMG + "Q5-example.png"))

questions.append(Q(
    5, "ה", "circuits",
    Q5_B + "\n" + r"**ב-4:** **אם ידוע** כי המעגל המקורי ($Q_0$) **לא** פעל, מהי ההסתברות שהמעגל החדש כן יפעל? (4 נק׳)",
    r"""$$P(Q'/\overline{Q_0})=\frac{P(Q'\cap\overline{Q_0})}{1-P(Q_0)}=\frac{P(Q')-P(Q'\cap Q_0)}{1-P(Q_0)}.$$
הצבה:
$$P(Q'/\overline{Q_0})=\frac{p^2(2-p)-\frac{p^2}{3}(4-p)}{1-p^2(2-p)}=\frac23\cdot\frac{p^2(1-p)}{1-p^2(2-p)}.$$""",
    4, contextId="c5", image=IMG + "Q5-example.png"))

# ------------------------------------------------------------------ Q6
Q6_TXT = r"בתאריך 1 במאי נפתחה ההרשמה מקוונת ללימודים במכון הטכנולוגי חולון דרך מילוי טופס הרשמה."
Q6_HINT = r"""**הערה:** לידיעתך,
$$\sum_{j=m}^{\infty}C_j^m\frac{a^j}{j!}=\frac{a^m}{m!}e^a$$
(יכול להיות שאין צורך להשתמש בנוסחה זו)."""

questions.append(Q(
    6, "א", "special_discrete",
    r"**אם ידוע** כי בדיוק $N$ מועמדים מילאו את טופס ההרשמה, מהי ההסתברות שמתוכם בדיוק $k$ נולדו ביום ההרשמה? (10 נק׳)",
    r"""נסמן ב-$W$ את מספר המועמדים, מבין $N$ שמילאו את הטופס, שנולדו ביום ההרשמה.
נניח, בקירוב הסטנדרטי (בהנחה שההסתברות להיוולד ביום מסוים היא $\frac1{365}$), שלכל מועמד ההסתברות להיוולד בתאריך נתון היא $\frac1{365}$, ללא תלות באחרים (הסבר: ניסוי ברנולי חוזר $N$ פעמים). אז
$$W\sim\mathrm{Bin}\left(N,\ p=\tfrac1{365}\right),$$
כלומר
$$P(W=k)=\binom Nk p^k(1-p)^{N-k},\qquad k=0,1,\ldots,N.$$""",
    10, contextId="c6"))

questions.append(Q(
    6, "ב", "special_discrete",
    r"נניח כי מספר המועמדים ($X$) שמילאו את טופס ההרשמה ביום ההרשמה מהווה משתנה מקרי בעל התפלגות פואסון $X\sim\mathrm{P}(\lambda)$." "\n"
    r"**ב-1:** מהי ההסתברות שמתוך כל אלה שמילאו את טופס ההרשמה, בדיוק $k$ נולדו ביום ההרשמה? שימו לב כי אין אנו יודעים כמה מועמדים נגשו לטופס ההרשמה! (10 נק׳)" "\n" + Q6_HINT,
    r"""נגדיר $Y$ = מספר המועמדים, מבין אלה שמילאו את הטופס, שנולדו ביום ההרשמה. ערכים אפשריים: $k=0,1,\ldots,\infty$ ($X$ יכול להיות גדול כרצוננו).
לפי נוסחת ההסתברות השלמה, כאשר נתון $X=j$ ההסתברות לכך שבדיוק $k$ מהם נולדו ביום ההרשמה היא בינומית, $\mathrm{Bin}(j,p)$, ולכן אפשרי רק $j\ge k$:
$$P(Y=k)=\sum_{j=k}^{\infty}P(Y=k\mid X=j)P(X=j)=\sum_{j=k}^{\infty}\binom jk p^k(1-p)^{j-k}\frac{\lambda^j}{j!}e^{-\lambda}.$$
נוציא גורמים קבועים ונשתמש בנוסחה הנתונה עם $a=\lambda(1-p)$:
$$P(Y=k)=e^{-\lambda}\frac{p^k}{(1-p)^k}\sum_{j=k}^{\infty}\binom jk\frac{[\lambda(1-p)]^j}{j!}=e^{-\lambda}\frac{p^k}{(1-p)^k}\cdot\frac{[\lambda(1-p)]^k}{k!}e^{\lambda(1-p)}.$$
ולכן
$$P(Y=k)=\frac{(\lambda p)^k}{k!}e^{-\lambda p},\qquad k=0,1,\ldots$$
כלומר $Y\sim\mathrm{P}(\lambda p)$.""",
    10, contextId="c6"))

questions.append(Q(
    6, "ג", "conditional_bayes",
    r"**ב-2:** **אם ידוע** כי בין ממלאי טופס ההרשמה בדיוק $k$ נולדו בתאריך ההרשמה, מהי ההסתברות שבדיוק $n$ מועמדים מילאו את הטופס? (5 נק׳)",
    r"""לפי נוסחת בייס
$$P(X=n/Y=k)=\frac{P(Y=k/X=n)\,P(X=n)}{P(Y=k)}.$$
הצבה:
$$=\frac{\binom nk p^k(1-p)^{n-k}\cdot\frac{\lambda^n}{n!}e^{-\lambda}}{\frac{(\lambda p)^k}{k!}e^{-\lambda p}}=\frac{[\lambda(1-p)]^{n-k}}{(n-k)!}e^{-\lambda(1-p)}.$$
ולכן
$$P(X=n/Y=k)=\frac{[\lambda(1-p)]^{n-k}}{(n-k)!}e^{-\lambda(1-p)},\qquad n=k,k+1,\ldots$$
(התפלגות פואסון עם פרמטר $\lambda(1-p)$, מוסטת ב-$k$). כאן $p$ היא ההסתברות שמועמד נולד ביום ההרשמה (בהנחה שההסתברות להיוולד ביום מסוים היא $\frac1{365}$, כלומר $p=\frac1{365}$).""",
    5, contextId="c6"))

# ------------------------------------------------------------------ area regions (RAW_SCHEMA `region`)
REGIONS = {
    (1, 'ב'): {"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"expr": "x^2+y^2", "op": "<", "c": 1}], "exact": 0.7853981633974483, "caption": "האזור x²+y²<1 (רבע עיגול)"},
    (1, 'ג'): {"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"expr": "x*y", "op": "<", "c": 0.5}], "exact": 0.8465735902799727, "caption": "האזור xy<1/2 (S<1/4)"},
    (1, 'ד'): {"space": {"x": [0, 1], "y": [0, 1]}, "event": [{"expr": "x^2+y^2", "op": "<", "c": 1}], "given": [{"expr": "x*y", "op": "<", "c": 0.5}], "exact": 0.9277376147981501, "caption": "L<1 בהינתן S<1/4"},
}
for _q in questions:
    _r = REGIONS.get((_q["num"], _q.get("part")))
    if _r is not None:
        _q["region"] = _r

# ------------------------------------------------------------------ area regions + simulations (RAW_SCHEMA `region`, `sim`)
_U2 = {"x": [0, 1], "y": [0, 1]}
SIMS = {
    (1, "ב"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(L<1)", "exact": math.pi / 4},
    (1, "ג"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(S<1/4)", "exact": 0.5 * (1 + math.log(2))},
    (1, "ד"): {"kind": "area", "params": {"fromRegion": True}, "estimate": "P(L<1 | S<1/4)", "exact": math.pi / (2 * (1 + math.log(2)))},
    (1, "ה"): {"kind": "area", "params": {"space": _U2, "measure": "var", "expr": "x*y/2"}, "estimate": "Var[S]", "exact": 7 / 576},
}

for _q in questions:
    _k = (_q["num"], _q.get("part"))
    if _k in SIMS:
        _q["sim"] = SIMS[_k]

# ------------------------------------------------------------------ exam
exam = {
    "examCode": CODE,
    "examLabel": "הסתברות, סמסטר ב׳ תשפ״ה, מועד א (15.07.2025)",
    "year": 2025,
    "examDate": "15.07.2025",
    "sourceFile": "25B-A exam pp.1-3",
    "solutionFile": "25B-A handwritten official solutions, pp.4-19",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1", "image": IMG + "Q1-triangle.png", "caption": Q1_TXT},
        "c2": {"kind": "text", "title": "שאלה 2", "text": Q2_TXT},
        "c3": {"kind": "image", "title": "שאלה 3: שלושה גשרים", "image": IMG + "Q3-bridges.png", "caption": Q3_TXT},
        "c4": {"kind": "text", "title": "שאלה 4", "text": Q4_TXT},
        "c5": {"kind": "image", "title": "שאלה 5: מעגל חשמלי", "image": IMG + "Q5-q0.png", "caption": Q5_TXT},
        "c6": {"kind": "text", "title": "שאלה 6", "text": Q6_TXT},
    },
    "questions": questions,
}

# ------------------------------------------------------------------ steps / rubric / pitfalls (ai-draft) + extra sims
# Every step value is re-derived independently (exact fractions / sympy / brute force, and Monte Carlo) in
# tools/verify/25B-A/steps_check.py, which reads the generated raw JSON back and compares.
import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import probsteps as PS
from fractions import Fraction as Fr
from math import e as _E, pi as _PI, log as _LN

num, choice, item = PS.num, PS.choice, PS.item
DATA = {}

_OM1 = num(r"שטח מרחב המדגם $|\Omega|$, ריבוע היחידה $(0,1)\times(0,1)$.", 1, r"$|\Omega|=1\cdot1=1$.")
_AREA_MODEL = choice(
    r"$X$ ו-$Y$ בלתי תלויים ואחידים על $(0,1)$. איזה כלי מתאים לחישוב הסתברות של אירוע שמוגדר על שניהם?",
    [r"שיטת השטח: $(X,Y)$ אחידה על ריבוע היחידה, וההסתברות היא שטח האירוע חלקי $|\Omega|$",
     r"התפלגות בינומית",
     r"נוסחת ההסתברות השלמה על ערכים בדידים",
     r"התפלגות פואסון"], 0,
    r"שני משתנים רציפים אחידים ובלתי תלויים נותנים התפלגות אחידה על ריבוע, ולכן הסתברות = שטח. הבינומית והפואסונית סופרות הצלחות, והשלמה על ערכים בדידים אינה רלוונטית לתחום רציף.")

# ---- Q1
DATA[(1, "א")] = item(
    [(r"אורך כל ניצב: שטח $\frac12\cdot\ell^2=\frac12$ ולכן $\ell=1$", 2),
     (r"נקודה אקראית על צלע באורך $1$ היא $U_c(0,1)$", 1),
     (r"אי-תלות בין בחירת שתי הנקודות", 1)],
    [r"לחשוב שהצלעות באורך $\frac12$ (שטח $\frac12$ הוא השטח כולו, לא אורך הצלע).",
     r"להתייחס לאורך היתר $\sqrt2$ כאילו הנקודה נבחרת עליו."],
    [num(r"אורך כל אחת משתי הצלעות הניצבות (משולש ישר זווית ושווה שוקיים בעל שטח $\frac12$).", 1, r"$\frac12\ell^2=\frac12\Rightarrow\ell=1$."),
     choice(r"איך מפולגים $X$ ו-$Y$?",
            [r"$U_c(0,1)$ ובלתי תלויים", r"$U_c\left(0,\frac12\right)$", r"$U_c(0,\sqrt2)$", r"$\mathrm{Exp}(1)$"], 0,
            r"נקודה אקראית על צלע באורך $1$ אחידה על $(0,1)$. $\sqrt2$ הוא אורך היתר, שעליו לא נבחרות הנקודות.")])

DATA[(1, "ב")] = item(
    [(r"$L=\sqrt{X^2+Y^2}$ והצגת $P(L<1)$ כיחס שטחים", 2),
     (r"$|\Omega|=1$", 1),
     (r"האזור הוא רבע עיגול ברדיוס $1$ בתוך הריבוע", 1),
     (r"שטח $\frac\pi4$ והתשובה", 1)],
    [r"להשתמש בשטח עיגול שלם $\pi$ ולשכוח שרק הרבע החיובי בתוך הריבוע.", r"לקחת רדיוס $\sqrt2$ במקום $1$."],
    [_AREA_MODEL, _OM1,
     choice(r"מהו האזור $\{x^2+y^2<1\}$ בתוך ריבוע היחידה?",
            [r"רבע עיגול ברדיוס $1$", r"חצי עיגול ברדיוס $1$", r"משולש $x+y<1$", r"רבע עיגול ברדיוס $\sqrt2$"], 0,
            r"$x,y>0$ ולכן רק הרבע הראשון של העיגול ברדיוס $1$. משולש הוא האזור $x+y<1$, ורדיוס $\sqrt2$ חורג מהריבוע."),
     num(r"מהי $P(L<1)$? (עד שלוש ספרות אחרי הנקודה)", _PI / 4, r"$\frac\pi4\approx0.785$.", tol=0.001)])

DATA[(1, "ג")] = item(
    [(r"$S=\frac12XY$ ולכן $S<\frac14\iff XY<\frac12$", 1),
     (r"גבול ההיפרבולה $y=\frac1{2x}$ חותך את $y=1$ ב-$x=\frac12$", 1),
     (r"שטח התחום $0<x<\frac12$ הוא $\frac12$", 1),
     (r"האינטגרל $\int_{1/2}^1\frac{dx}{2x}=\frac{\ln2}2$", 1),
     (r"סכום: $\frac12(1+\ln2)$", 1)],
    [r"לשכוח שעבור $x<\frac12$ כל $y\in(0,1)$ מתאים, ולבצע אינטגרל מ-$0$ (האינטגרל מתבדר).",
     r"לטעות במקדם: $S<\frac14$ שקול ל-$XY<\frac12$ ולא ל-$XY<\frac14$."],
    [_OM1,
     num(r"באיזה $x$ ההיפרבולה $y=\frac1{2x}$ חותכת את הישר $y=1$?", Fr(1, 2), r"$\frac1{2x}=1\Rightarrow x=\frac12$. משמאל לו כל $y\in(0,1)$ מתאים."),
     num(r"שטח האזור לימין של זה: $\int_{1/2}^1\frac{dx}{2x}$ (עד שלוש ספרות).", _LN(2) / 2, r"$\frac12\ln x\big|_{1/2}^1=\frac{\ln2}2\approx0.3466$.", tol=0.001),
     num(r"מהי $P(S<\frac14)$? (עד שלוש ספרות)", (1 + _LN(2)) / 2, r"$\frac12+\frac{\ln2}2\approx0.8466$.", tol=0.001)])

DATA[(1, "ד")] = item(
    [(r"הגדרת ההסתברות המותנית: $\frac{P(L<1\cap S<\frac14)}{P(S<\frac14)}$", 1),
     (r"$P(S<\frac14)=\frac12(1+\ln2)$ מהסעיף הקודם", 1),
     (r"רבע העיגול כולו מתחת להיפרבולה: $x^2+y^2<1\Rightarrow xy<\frac12$", 2),
     (r"לכן החיתוך הוא $\frac\pi4$ והתשובה $\frac{\pi}{2(1+\ln2)}$", 1)],
    [r"לחשב את החיתוך כשטח בין העיגול להיפרבולה: הרבע כולו כלול באזור $xy<\frac12$.",
     r"לחלק ב-$P(L<1)$ במקום ב-$P(S<\frac14)$."],
    [_OM1,
     num(r"הסתברות אירוע התנאי $P(S<\frac14)$ (סעיף ג). עד שלוש ספרות.", (1 + _LN(2)) / 2, r"$\frac12(1+\ln2)\approx0.8466$.", tol=0.001),
     choice(r"מהו האזור $\{L<1\}\cap\{S<\frac14\}$?",
            [r"כל רבע העיגול, כי $x^2+y^2<1$ גורר $xy\le\frac{x^2+y^2}2<\frac12$", r"שטח בין העיגול להיפרבולה", r"ריבוע היחידה כולו", r"קבוצה ריקה"], 0,
            r"אי-שוויון ממוצעים: $xy\le\frac{x^2+y^2}{2}$. בתוך הרבע הערך קטן מ-$\frac12$, ולכן החיתוך הוא כל הרבע ושטחו $\frac\pi4$."),
     num(r"מהי ההסתברות המותנית? (עד שלוש ספרות)", _PI / (2 * (1 + _LN(2))), r"$\frac{\pi/4}{\frac12(1+\ln2)}=\frac{\pi}{2(1+\ln2)}\approx0.928$.", tol=0.001)])

DATA[(1, "ה")] = item(
    [(r"$\mathbb{E}[S]=\frac12\mathbb{E}[X]\mathbb{E}[Y]=\frac18$ מאי-תלות", 2),
     (r"$\mathbb{E}[X^2]=\mathbb{E}[Y^2]=\frac13$", 1),
     (r"$\operatorname{Var}[XY]=\mathbb{E}[X^2]\mathbb{E}[Y^2]-(\mathbb{E}[X]\mathbb{E}[Y])^2=\frac7{144}$", 2),
     (r"$\operatorname{Var}[S]=\frac14\operatorname{Var}[XY]=\frac7{576}$", 1)],
    [r"לכתוב $\operatorname{Var}[XY]=\operatorname{Var}[X]\operatorname{Var}[Y]=\frac1{144}$: זו נוסחה שגויה.",
     r"לשכוח את המקדם $\frac14$ ב-$\operatorname{Var}[\frac12XY]$."],
    [choice(r"איזה כלל מאפשר לחשב את $\mathbb{E}[XY]$ ואת $\mathbb{E}[X^2Y^2]$ ישירות?",
            [r"אי-תלות: התוחלת של מכפלה היא מכפלת התוחלות", r"ליניאריות בלבד: $\mathbb{E}[XY]=\mathbb{E}[X]+\mathbb{E}[Y]$", r"נוסחת ההסתברות השלמה", r"שיטת השטח על אירוע"], 0,
            r"אי-תלות מאפשרת לפרק תוחלת של מכפלת פונקציות. ליניאריות נותנת סכום, לא מכפלה (ונותנת $1$ במקום $\frac14$)."),
     num(r"מהי $\mathbb{E}[S]$?", Fr(1, 8), r"$\frac12\cdot\frac12\cdot\frac12=\frac18$."),
     num(r"$\mathbb{E}[X^2]=\int_0^1x^2\,dx$.", Fr(1, 3), r"$\frac13$."),
     num(r"$\operatorname{Var}[XY]=\mathbb{E}[X^2]\mathbb{E}[Y^2]-\left(\mathbb{E}[X]\mathbb{E}[Y]\right)^2$.", Fr(7, 144), r"$\frac19-\frac1{16}=\frac7{144}$."),
     num(r"מהי $\operatorname{Var}[S]$? (עד חמש ספרות)", Fr(7, 576), r"$\frac14\cdot\frac7{144}=\frac7{576}\approx0.01215$.", tol=0.00002)])

# ---- Q2: p = 3/5, q = 7/10, s = 4/5
_p, _q, _s = Fr(3, 5), Fr(7, 10), Fr(4, 5)
_PB = 1 - (1 - _s) / _q
_PA = _s - (1 - _p) * _PB
_PAB = _p * _PB
_JOINT = [{"p": float(_PAB), "A": 1, "B": 1}, {"p": float(_PA - _PAB), "A": 1, "B": 0},
          {"p": float(_PB - _PAB), "A": 0, "B": 1}, {"p": float(1 - _s), "A": 0, "B": 0}]

DATA[(2, "א")] = item(
    [(r"הצגת $P(A/B)$ באמצעות $P(A\cap B)=P(A)+P(B)-s$", 2),
     (r"משוואה $(1)$: $P(A)+(1-p)P(B)=s$", 1),
     (r"מהנתון השני: $P(B)=1-\frac{1-s}q$", 1),
     (r"הצבה: $P(A)=s-(1-p)\left(1-\frac{1-s}q\right)$", 1)],
    [r"להניח ש-$A$ ו-$B$ בלתי תלויים ולכתוב $P(A\cap B)=P(A)P(B)$: אין זה נתון.",
     r"לטעות ב-$P(\overline{A\cup B})=1-s$ לעומת $P(\overline A)P(\overline B)$."],
    [choice(r"איך מתרגמים את שלושת הנתונים למשוואות ב-$P(A)$ וב-$P(B)$?",
            [r"$P(A\cap B)=pP(B)$ ו-$P(A\cup B)=P(A)+P(B)-P(A\cap B)$, ומשלים $P(\overline A\cap\overline B)=1-s$",
             r"$P(A\cap B)=P(A)P(B)$ (אי-תלות)", r"$P(A\cup B)=P(A)+P(B)$ (זרים)", r"נוסחת בייס בלבד"], 0,
            r"לא נתון שהמאורעות בלתי תלויים או זרים. מהגדרת המותנה ומהכלה-הפרדה מקבלים את שתי המשוואות."),
     num(r"ב-$p=0.6$, $q=0.7$, $s=0.8$: $P(B)=1-\frac{1-s}q$ (עד שש ספרות).", _PB, r"$1-\frac{0.2}{0.7}=\frac57\approx0.714286$."),
     num(r"באותם ערכים: $P(A)=s-(1-p)P(B)$.", _PA, r"$0.8-0.4\cdot\frac57=\frac{18}{35}\approx0.514286$.")])

DATA[(2, "ב")] = item(
    [(r"$P(\overline A\cap\overline B)=P(\overline{A\cup B})=1-s$", 2),
     (r"$P(\overline A/\overline B)=\frac{1-s}{1-P(B)}=q$", 2),
     (r"פתרון: $P(B)=1-\frac{1-s}q$", 1)],
    [r"להפעיל את משוואת המותנה על $P(A/B)$ במקום על $P(\overline A/\overline B)$, שהיא שנותנת את $P(B)$ ישירות."],
    [choice(r"מהו המונה ב-$P(\overline A/\overline B)$?",
            [r"$P(\overline A\cap\overline B)=1-P(A\cup B)=1-s$", r"$P(\overline A)$", r"$1-P(A)-P(B)$", r"$s$"], 0,
            r"לפי דה-מורגן $\overline A\cap\overline B=\overline{A\cup B}$. הביטוי $1-P(A)-P(B)$ שגוי כי $A$ ו-$B$ אינם זרים."),
     num(r"ב-$q=0.7$, $s=0.8$: $P(\overline B)=\frac{1-s}q$ (עד שש ספרות).", Fr(2, 7), r"$\frac{0.2}{0.7}=\frac27$."),
     num(r"מהו $P(B)$?", _PB, r"$1-\frac27=\frac57$.")])

DATA[(2, "ג")] = item(
    [(r"$P(A\cap B)=P(A/B)P(B)=pP(B)$", 2),
     (r"שימוש ב-$P(B)$ מסעיף ב", 1),
     (r"התשובה $p\left(1-\frac{1-s}q\right)$", 2)],
    [r"לחשב $P(A)P(B)$ כמו באי-תלות.", r"לשכוח שהמותנה הוא $P(A/B)$ ולא $P(B/A)$."],
    [choice(r"איך מחשבים את $P(A\cap B)$ מהנתונים?",
            [r"$P(A/B)\cdot P(B)=pP(B)$", r"$P(A)P(B)$", r"$P(A/B)\cdot P(A)$", r"$s-P(A)-P(B)$"], 0,
            r"כלל המכפלה: חיתוך = מותנה כפול התנאי. השאר דורשים אי-תלות, תנאי אחר, או נותנים סימן הפוך."),
     num(r"ב-$p=0.6$, $q=0.7$, $s=0.8$: $P(B)$ (סעיף ב).", _PB, r"$\frac57$."),
     num(r"מהו $P(A\cap B)$?", _PAB, r"$0.6\cdot\frac57=\frac37\approx0.428571$.")])

DATA[(2, "ד")] = item(
    [(r"דרישת $P(B)\ge0$", 2),
     (r"$1-\frac{1-s}q\ge0\iff q\ge1-s$", 2),
     (r"מסקנה: $q<1-s$ אינו אפשרי", 1)],
    [r"לבדוק רק ש-$P(B)\le1$ ולשכוח את אי-השליליות."],
    [num(r"ב-$q=0.1$, $s=0.8$: מהו $P(B)=1-\frac{1-s}q$?", -1, r"$1-\frac{0.2}{0.1}=-1$: הסתברות שלילית."),
     choice(r"האם ייתכן $q<1-s$?",
            [r"לא: אז $P(B)<0$", r"כן: אין הגבלה על $q$", r"כן, אם $p$ גדול מספיק", r"לא: אז $P(A)>1$"], 0,
            r"$P(B)\ge0$ שקול ל-$q\ge1-s$. אם $q<1-s$ מתקבל $P(B)<0$, בלתי אפשרי, וזה לא תלוי ב-$p$.")])

DATA[(2, "ה")] = item(
    [(r"אי-תלות נותנת $P(A/B)=P(A)=p$", 1),
     (r"אי-תלות נותנת גם $P(\overline A/\overline B)=P(\overline A)=q$", 2),
     (r"$q=1-P(A)=1-p$ ולכן $p=1-q$", 2)],
    [r"להסיק $p=q$ במקום $p=1-q$ (השוו $P(A)$ עם $P(\overline A)$).", r"לחפש תנאי על $s$: התנאי $p=1-q$ אינו תלוי ב-$s$ כאן."],
    [choice(r"מה גוררת אי-תלות של $A$ ו-$B$?",
            [r"$P(A/B)=P(A)$ וגם $P(\overline A/\overline B)=P(\overline A)$", r"$P(A\cap B)=0$", r"$P(A/B)=P(\overline A/\overline B)$", r"$P(A\cup B)=1$"], 0,
            r"אי-תלות פירושה שההתניה אינה משנה את ההסתברות, גם עבור המשלימים. $P(A\cap B)=0$ הוא זרות."),
     num(r"אם $q=0.3$ והמאורעות בלתי תלויים, כמה הוא $p$?", Fr(7, 10), r"$p=1-q=0.7$.")])

# ---- Q3: bridges, sample p = 0.8, gates (1, 2, 3)
_pp = Fr(4, 5)
_PAj = [_pp ** k for k in (1, 2, 3)]
_blocked = (1 - _PAj[0]) * (1 - _PAj[1]) * (1 - _PAj[2])
_PQ = 1 - _blocked
_PA2Q = _PAj[1] / _PQ
_SERIES = lambda ids: {"type": "series", "children": [{"type": "comp", "id": i, "p": 0.8} for i in ids]}
_NET3 = {"type": "parallel", "children": [{"type": "comp", "id": "g1", "p": 0.8}, _SERIES(["g2a", "g2b"]), _SERIES(["g3a", "g3b", "g3c"])]}

DATA[(3, "א")] = item(
    [(r"הגדרת $A_j$ ו-$P(A_j)=p^{N_j}$ (כל שערי הגשר פתוחים)", 4),
     (r"$Q=A_1\cup A_2\cup A_3$ ומעבר למשלים", 4),
     (r"אי-תלות בין הגשרים", 3),
     (r"התשובה $1-\prod_j\left(1-p^{N_j}\right)$", 4)],
    [r"לחבר את $P(A_j)$: האירועים אינם זרים.", r"להשתמש בבינומית על מספר השערים: חשוב אילו שערים פתוחים, ויש לפתוח את כל שערי אותו גשר."],
    [choice(r"אסתר עוברת אם לפחות גשר אחד פתוח לגמרי. איזו גישה מתאימה?",
            [r"משלים: $1-P(\text{all bridges blocked})$ ואי-תלות בין הגשרים", r"סכום $\sum p^{N_j}$ (כאילו הגשרים זרים)", r"מכפלה $\prod p^{N_j}$ (כל הגשרים פתוחים)", r"בינומית על מספר השערים הפתוחים"], 0,
            r"האירוע 'לפחות אחד' נחשב דרך המשלים. סכום הסתברויות דורש זרות, מכפלה היא 'כולם', ובינומית אינה מבחינה בין שערי גשרים שונים."),
     num(r"ב-$p=0.8$ ו-$(N_1,N_2,N_3)=(1,2,3)$: $P(A_2)$.", _PAj[1], r"$0.8^2=0.64$."),
     num(r"באותם ערכים: הסתברות שכל שלושת הגשרים חסומים, $\prod(1-p^{N_j})$ (עד שש ספרות).", _blocked, r"$0.2\cdot0.36\cdot0.488=0.035136$."),
     num(r"מהי ההסתברות שאסתר עוברת?", _PQ, r"$1-0.035136=0.964864$.")])

DATA[(3, "ב")] = item(
    [(r"נוסחת בייס: $P(A_2/Q)=\frac{P(Q/A_2)P(A_2)}{P(Q)}$", 2),
     (r"$P(Q/A_2)=1$ כי אם גשר $2$ פתוח היא עוברת", 1),
     (r"הצבת $P(A_2)=p^{N_2}$ ו-$P(Q)$ מסעיף א", 2)],
    [r"לחשב את $P(Q/A_2)$ כ-$P(A_2)$: אם הגשר השני פתוח, ההצלחה בטוחה."],
    [choice(r"מה $P(Q/A_2)$?", [r"$1$: גשר $2$ פתוח, ולכן עוברת", r"$p^{N_2}$", r"$P(Q)$", r"$0$"], 0,
            r"$A_2\subseteq Q$ ולכן $P(Q/A_2)=1$, וזה מצמצם את בייס ל-$P(A_2)/P(Q)$."),
     num(r"ב-$p=0.8$, $N=(1,2,3)$: $P(A_2)$.", _PAj[1], r"$0.64$."),
     num(r"מהי $P(A_2/Q)$? (עד שש ספרות)", _PA2Q, r"$\frac{0.64}{0.964864}\approx" + f"{float(_PA2Q):.6f}" + "$.")])

DATA[(3, "ג")] = item(
    [(r"משלים בתוך המותנה: $1-P(A_2/Q)$", 3),
     (r"הצבת התשובה מסעיף ב", 2)],
    [r"לחשב $1-P(A_2)$ במקום $1-P(A_2/Q)$."],
    [choice(r"איך מחשבים את $P(\overline{A_2}/Q)$?",
            [r"$1-P(A_2/Q)$", r"$1-P(A_2)$", r"$P(\overline{A_2})P(Q)$", r"$1-P(Q/A_2)$"], 0,
            r"המשלים נעשה בתוך אותו תנאי $Q$. השאר מחליפים או מתעלמים מהתנאי ($1-P(Q/A_2)=0$)."),
     num(r"ב-$p=0.8$, $N=(1,2,3)$: מהי $P(\overline{A_2}/Q)$?", 1 - _PA2Q, r"$1-" + f"{float(_PA2Q):.6f}={float(1 - _PA2Q):.6f}" + "$.")])

# ---- Q4: pdf with a(x+1), b; sample mu = 0 (a = 6/5, b = 2/5)
_a0, _b0 = Fr(6, 5), Fr(2, 5)
_F = lambda t: _a0 / 2 * (t + 1) ** 2 if t < 0 else _a0 / 2 + _b0 * t
DATA[(4, "א")] = item(
    [(r"שונות סופית גוררת $c=g=0$ (האינטגרלים של $x^2f$ מתבדרים)", 2),
     (r"נרמול: $\frac a2+b=1$", 2),
     (r"תוחלת: $-\frac a6+\frac b2=\mu$", 2),
     (r"פתרון: $a=\frac65(1-2\mu)$, $b=\frac25(1+3\mu)$", 2)],
    [r"לדרוש $c=0$ מהנרמול בלבד: $\int_1^\infty\frac{c}{x^3}dx=\frac c2$ מתכנס; רק התנאי על השונות פוסל את $c$.",
     r"לטעות באינטגרל $\int_{-1}^0x(x+1)\,dx=-\frac16$."],
    [choice(r"איזה כלי מתאים למציאת מקדמי הצפיפות?",
            [r"נרמול $\int f=1$ ותוחלת $\int xf=\mu$, ותנאי השונות הסופית", r"שיטת השטח", r"נוסחת בייס", r"התפלגות בינומית"], 0,
            r"הצפיפות נתונה עד כדי מקדמים; מה שנתון הוא התוחלת והשונות הסופית. שיטת השטח, בייס ובינומית אינם מתאימים."),
     choice(r"מדוע $c=0$ ו-$g=0$?",
            [r"אחרת $\mathbb{E}[X^2]$ מתבדר: $\int_1^\infty\frac{dx}x$ ו-$\int_1^\infty x^2dx$ מתבדרים",
             r"כי הנרמול מחייב $c=0$ ($\int_1^\infty\frac{c}{x^3}$ מתבדר)",
             r"כי התוחלת הסופית לבדה פוסלת את $c$",
             r"כי הצפיפות אינה יכולה להיות חיובית ב-$x\ge1$"], 0,
            r"$\int_1^\infty c/x^3\,dx=\frac c2$ מתכנס, ולכן הנרמול והתוחלת לא פוסלים את $c$; רק $\mathbb{E}[X^2]$ (עם $x^2\cdot\frac{c}{x^3}=\frac cx$) מתבדר."),
     num(r"עבור $\mu=0$: מהו $a$?", _a0, r"$a=\frac65(1-2\mu)=\frac65$."),
     num(r"עבור $\mu=0$: מהו $b$?", _b0, r"$b=\frac25(1+3\mu)=\frac25$. בדיקה: $\frac a2+b=\frac35+\frac25=1$ ו-$-\frac a6+\frac b2=-\frac15+\frac15=0$.")])

DATA[(4, "ב")] = item(
    [(r"צפיפות אי-שלילית: $a\ge0$ ו-$b\ge0$", 1),
     (r"$a\ge0\Rightarrow\mu\le\frac12$", 2),
     (r"$b\ge0\Rightarrow\mu\ge-\frac13$", 2)],
    [r"לבדוק רק את $a$ ולשכוח את $b$, או להפך."],
    [choice(r"מה התנאי על $a$ ו-$b$ כדי שהפונקציה תהיה צפיפות?",
            [r"שניהם אי-שליליים", r"שניהם קטנים מ-$1$", r"$a+b=1$", r"$a=b$"], 0,
            r"צפיפות חייבת להיות $\ge0$ (הנרמול כבר סופק על ידי הפתרון)."),
     num(r"הערך הגדול ביותר של $\mu$ ($a\ge0$).", Fr(1, 2), r"$1-2\mu\ge0\Rightarrow\mu\le\frac12$."),
     num(r"הערך הקטן ביותר של $\mu$ ($b\ge0$) (עד שלוש ספרות).", Fr(-1, 3), r"$1+3\mu\ge0\Rightarrow\mu\ge-\frac13$.", tol=0.001)])

DATA[(4, "ג")] = item(
    [(r"פיצול לתחומים: $t<-1$, $-1\le t<0$, $0\le t<1$, $t\ge1$", 2),
     (r"$-1\le t<0$: $\frac a2(t+1)^2$", 2),
     (r"$0\le t<1$: $\frac a2+bt$ (כולל המסה שנצברה)", 2),
     (r"הצבת $a,b$ והגרף: $F=1$ מ-$t=1$", 2)],
    [r"לשכוח להוסיף את המסה $\frac a2$ בתחום $0\le t<1$.", r"לצייר את הקטע הראשון כקו ישר במקום פרבולה."],
    [choice(r"מהי צורת $F_X(t)$ בקטע $-1\le t<0$?",
            [r"פרבולה עולה (אינטגרל של פונקציה ליניארית)", r"קו ישר", r"אקספוננט", r"קבוע"], 0,
            r"הצפיפות שם ליניארית $a(x+1)$, ואינטגרל שלה ריבועי."),
     num(r"עבור $\mu=0$: $F_X\left(-\frac12\right)$.", _F(Fr(-1, 2)), r"$\frac a2\left(\frac12\right)^2=\frac35\cdot\frac14=0.15$."),
     num(r"עבור $\mu=0$: $F_X(0)$.", _F(Fr(0)), r"$\frac a2=0.6$."),
     num(r"עבור $\mu=0$: $F_X\left(\frac12\right)$.", _F(Fr(1, 2)), r"$0.6+0.4\cdot0.5=0.8$.")])

DATA[(4, "ד")] = item(
    [(r"$P(X>-\frac12)=1-F_X(-\frac12)$ והצגה כיחס", 1),
     (r"$P(-\frac12<X<1)=F_X(1)-F_X(-\frac12)=1-F_X(-\frac12)$", 2),
     (r"היחס הוא $1$", 1)],
    [r"לחשב את $F_X(1)$ כ-$F_X(-\frac12)$ או להפך."],
    [num(r"עבור $\mu=0$: הסתברות אירוע התנאי $P(X>-\frac12)$.", 1 - _F(Fr(-1, 2)), r"$1-0.15=0.85$."),
     num(r"עבור $\mu=0$: $P\left(-\frac12<X<1\right)$.", 1 - _F(Fr(-1, 2)), r"$F_X(1)-F_X(-\frac12)=1-0.15=0.85$ כי $F_X(1)=1$."),
     num(r"מהי $P\left(X<1\mid X>-\frac12\right)$?", 1, r"$\frac{0.85}{0.85}=1$: כל המסה שמימין ל-$-\frac12$ נמצאת מתחת ל-$1$.")])

# ---- Q5: circuit, sample p = 0.6
_c = Fr(3, 5)
_P0 = _c ** 2 * (2 - _c)
_PJ = _c ** 2 * (4 - _c) / 3
_PR = Fr(2, 3) * _c ** 2 * (1 - _c) / (1 - _P0)
DATA[(5, "א")] = item(
    [(r"$Q_0=A\cap(B\cup C)$ (טור של $A$ עם הזוג המקביל)", 1),
     (r"$P(B\cup C)=2p-p^2$", 1),
     (r"$P(Q_0)=p^2(2-p)$ מאי-תלות", 1)],
    [r"להכפיל $p^3$ (להתעלם מכך ש-$B$ ו-$C$ מקבילות)."],
    [choice(r"איך בנוי $Q_0$ ואיך מחשבים?",
            [r"$A$ בטור עם הזוג המקביל $B,C$: מכפילים $p\cdot(2p-p^2)$", r"שלושתן במקביל", r"שלושתן בטור", r"בינומית $\mathrm{Bin}(3,p)$"], 0,
            r"טור דורש ששני החלקים יפעלו: $A$ והזוג. המקבילי מצליח אם לפחות אחת מ-$B,C$ פועלת."),
     num(r"ב-$p=0.6$: $P(B\cup C)$.", Fr(21, 25), r"$2p-p^2=1.2-0.36=0.84$."),
     num(r"ב-$p=0.6$: $P(Q_0)$.", _P0, r"$0.6\cdot0.84=0.504$.")])

DATA[(5, "ב")] = item(
    [(r"המעגל החדש הוא אותה טופולוגיה עם אותן יחידות במקומות אחרים", 1),
     (r"לכל היחידות אותה הסתברות $p$ ולכן אותה הנוסחה", 1),
     (r"$P(Q')=p^2(2-p)$", 1)],
    [r"לחשב את הסידורים השונים בנפרד: ההסתברות שהמעגל פועל זהה לכל סידור."],
    [choice(r"מדוע ההסתברות שהמעגל החדש פועל שווה לזו של $Q_0$?",
            [r"אותה טופולוגיה ובכל המקומות יחידה בהסתברות $p$, בלי קשר לזהות היחידה", r"כי הוא תמיד זהה ל-$Q_0$", r"כי $p=1$", r"כי כל סידור נותן בדיוק את אותו מעגל"], 0,
            r"ההסתברות תלויה רק במבנה ובהסתברויות, שלא משתנים. 'כל סידור נותן בדיוק את אותו מעגל' שגוי: חלק מהסידורים נותנים מעגל שונה (המבנה כן משתנה), אך ההסתברות זהה."),
     num(r"ב-$p=0.6$: $P(Q')$.", _P0, r"$p^2(2-p)=0.504$.")])

DATA[(5, "ג")] = item(
    [(r"ששת הסידורים שווי הסתברות $\frac16$, נוסחת ההסתברות השלמה", 2),
     (r"סידורים I ו-II: $Q'\equiv Q_0$ ולכן $p^2(2-p)$", 2),
     (r"סידורים III-VI: החיתוך הוא $A\cap B$ או $A\cap C$, והסתברותו $p^2$", 4),
     (r"סכום: $\frac{p^2}3(4-p)$", 2)],
    [r"להכפיל $P(Q_0)P(Q')$: המעגלים משתמשים באותן יחידות ולכן תלויים.",
     r"לספור פחות מ-$6$ סידורים, או לתת להם משקל לא שווה."],
    [choice(r"המעגל החדש הוא סידור אקראי של שלוש היחידות. מה הגישה?",
            [r"הסתברות שלמה על ששת הסידורים השווי-הסתברות", r"מכפלה $P(Q_0)P(Q')$", r"בייס", r"בינומית"], 0,
            r"החיתוך תלוי בסידור, ולכן מתנים על הסידור. מכפלה דורשת אי-תלות, וכאן הן אותן יחידות."),
     num(r"ב-$p=0.6$, בהינתן סידור I או II: מהי $P(Q_0\cap Q')$?", _P0, r"$Q'\equiv Q_0$ ולכן החיתוך הוא $Q_0$: $0.504$."),
     num(r"ב-$p=0.6$, בהינתן סידור III, IV, V או VI: מהי $P(Q_0\cap Q')$ (שווה ל-$P(A\cap B)$)?", _c ** 2, r"$p^2=0.36$."),
     num(r"מהו $P(Q_0\cap Q')$?", _PJ, r"$\frac16\{2\cdot0.504+4\cdot0.36\}=0.408=\frac{p^2}3(4-p)$.")])

DATA[(5, "ד")] = item(
    [(r"הגדרה: $\frac{P(Q_0\cap Q')}{P(Q_0)}$", 1),
     (r"הצבת סעיפים א ו-ג", 2),
     (r"פישוט: $\frac13\cdot\frac{4-p}{2-p}$", 2)],
    [r"לחלק ב-$P(Q')$ במקום ב-$P(Q_0)$; שניהם שווים כאן, אך ההגדרה היא ב-$P(Q_0)$ כאירוע התנאי."],
    [num(r"ב-$p=0.6$: הסתברות אירוע התנאי $P(Q_0)$.", _P0, r"$0.504$."),
     num(r"ב-$p=0.6$: $P(Q_0\cap Q')$ (סעיף ג).", _PJ, r"$0.408$."),
     num(r"מהי $P(Q'/Q_0)$? (עד שש ספרות)", _PJ / _P0, r"$\frac{0.408}{0.504}=\frac{4-p}{3(2-p)}\approx0.809524$.")])

DATA[(5, "ה")] = item(
    [(r"$P(Q'\cap\overline{Q_0})=P(Q')-P(Q'\cap Q_0)$", 2),
     (r"$P(\overline{Q_0})=1-p^2(2-p)$", 1),
     (r"הצבה ופישוט: $\frac23\cdot\frac{p^2(1-p)}{1-p^2(2-p)}$", 1)],
    [r"לחשב $1-P(Q'/Q_0)$: המשלים כאן הוא של אירוע התנאי, לא של אירוע המבוקש."],
    [choice(r"איך מחשבים את $P(Q'\cap\overline{Q_0})$?",
            [r"$P(Q')-P(Q'\cap Q_0)$", r"$P(Q')P(\overline{Q_0})$", r"$1-P(Q'\cap Q_0)$", r"$P(\overline{Q_0})-P(Q_0\cap Q')$"], 0,
            r"פיצול $Q'$ לפי $Q_0$ ו-$\overline{Q_0}$. מכפלה דורשת אי-תלות, והאחרים אינם נכונים."),
     num(r"ב-$p=0.6$: הסתברות אירוע התנאי $P(\overline{Q_0})$.", 1 - _P0, r"$1-0.504=0.496$."),
     num(r"ב-$p=0.6$: $P(Q'\cap\overline{Q_0})$.", _P0 - _PJ, r"$0.504-0.408=0.096$."),
     num(r"מהי $P(Q'/\overline{Q_0})$? (עד שש ספרות)", _PR, r"$\frac{0.096}{0.496}\approx0.193548$.")])

# ---- Q6: registration form
_e2 = _E ** -1
DATA[(6, "א")] = item(
    [(r"כל מועמד נולד ביום ההרשמה בהסתברות $p=\frac1{365}$, בלתי תלוי באחרים", 4),
     (r"$N$ ניסויי ברנולי ולכן $\mathrm{Bin}(N,p)$", 3),
     (r"פונקציית ההסתברות $\binom Nkp^k(1-p)^{N-k}$", 3)],
    [r"להשתמש בפואסון: $N$ נתון וסופי ולכן הבינומית מדויקת.", r"לטעות ולהשתמש ב-$\frac1{365}$ בהסתברות הכישלון."],
    [choice(r"ידוע ש-$N$ מועמדים מילאו טופס. איזה מודל מתאים למספר שנולדו ביום ההרשמה?",
            [r"בינומי $\mathrm{Bin}(N,p)$: $N$ ניסויים בלתי תלויים", r"היפרגאומטרי: אין אוכלוסייה סופית עם מספר ידוע של 'הצלחות'", r"גאומטרי: $N$ קבוע", r"פואסון: $N$ ידוע ולכן אין צורך בקירוב"], 0,
            r"$N$ ידוע והמועמדים בלתי תלויים: בינומי מדויק. פואסון יהיה קירוב בלבד."),
     num(r"ב-$N=5$, $p=0.2$: $P(W=2)$.", Fr(10) * Fr(1, 5) ** 2 * Fr(4, 5) ** 3, r"$\binom52\cdot0.2^2\cdot0.8^3=10\cdot0.04\cdot0.512=0.2048$.")])

DATA[(6, "ב")] = item(
    [(r"$Y\sim\mathrm{P}(\lambda p)$ (דילול פואסון) או חישוב ישיר", 2),
     (r"נוסחת ההסתברות השלמה: $\sum_{j\ge k}P(Y=k/X=j)P(X=j)$", 3),
     (r"שימוש ברמז עם $a=\lambda(1-p)$", 3),
     (r"התוצאה $\frac{(\lambda p)^k}{k!}e^{-\lambda p}$", 2)],
    [r"להשתמש בבינומית $\mathrm{Bin}(X,p)$ עם $X$ קבוע: מספר המועמדים אקראי.",
     r"לטעות ב-$a=\lambda p$ ברמז; הסכום הוא על האלה שאינם נספרים: $a=\lambda(1-p)$."],
    [choice(r"$X\sim\mathrm{P}(\lambda)$ ממלאים טופס, וכל אחד נולד ביום ההרשמה בהסתברות $p$ בלי תלות. מהו המודל ל-$Y$?",
            [r"דילול פואסון: $Y\sim\mathrm{P}(\lambda p)$", r"$\mathrm{Bin}(N,p)$ עם $N$ קבוע", r"$\mathrm{P}(\lambda)$ (הדילול לא משנה)", r"גאומטרי"], 0,
            r"מספר המועמדים אקראי (פואסון), ולכן בינומית עם $N$ קבוע אינה מתאימה. דילול של פואסון נשאר פואסון עם פרמטר מוקטן."),
     choice(r"איזה $a$ מציבים בסכום $\sum_{j\ge k}\binom jk\frac{a^j}{j!}$ מהרמז?",
            [r"$a=\lambda(1-p)$", r"$a=\lambda p$", r"$a=\lambda$", r"$a=1-p$"], 0,
            r"אחרי הוצאת $\frac{p^k}{(1-p)^k}$ נשאר $\frac{[\lambda(1-p)]^j}{j!}$."),
     num(r"ב-$\lambda=2$, $p=0.5$: $P(Y=0)$ (עד שש ספרות).", _E ** -1, r"$e^{-\lambda p}=e^{-1}\approx0.367879$."),
     num(r"באותם ערכים: $P(Y=2)$.", _E ** -1 / 2, r"$\frac{(\lambda p)^2}{2!}e^{-\lambda p}=\frac{e^{-1}}2\approx0.18394$.")])

DATA[(6, "ג")] = item(
    [(r"נוסחת בייס: $\frac{P(Y=k/X=n)P(X=n)}{P(Y=k)}$", 2),
     (r"הצבת בינומית, פואסון ו-$P(Y=k)$ מסעיף ב", 2),
     (r"פישוט: פואסון עם פרמטר $\lambda(1-p)$ מוסט ב-$k$", 1)],
    [r"לשכוח שהערכים האפשריים הם $n\ge k$ (מספר הממלאים לפחות $k$)."],
    [choice(r"איזו נוסחה מתאימה ל-$P(X=n/Y=k)$?",
            [r"בייס, עם $P(Y=k/X=n)$ בינומית", r"הסתברות שלמה על $Y$", r"$P(X=n)P(Y=k)$ (אי-תלות)", r"בינומית $\mathrm{Bin}(n,p)$ בלבד"], 0,
            r"מחשבים הסתברות לסיבה בהינתן התוצאה: בייס. $X$ ו-$Y$ תלויים (ל-$Y\le X$)."),
     num(r"ב-$\lambda=2$, $p=0.5$: $P(X=1/Y=1)$ (עד שש ספרות).", _E ** -1, r"$n=k$: $\frac{[\lambda(1-p)]^0}{0!}e^{-1}=e^{-1}\approx0.367879$."),
     num(r"באותם ערכים: $P(X=3/Y=1)$.", _E ** -1 / 2, r"$\frac{1^{2}}{2!}e^{-1}=\frac{e^{-1}}2\approx0.18394$.")])

# ---- extra sims (symbolic answers, at sample parameters stated in `estimate`)
def _pois_binom_joint(lam, p, K=20):
    from math import comb, exp, factorial
    rows = []
    for j in range(K + 1):
        pj = exp(-lam) * lam ** j / factorial(j)
        for k in range(j + 1):
            rows.append({"p": pj * comb(j, k) * p ** k * (1 - p) ** (j - k), "X": j, "Y": k})
    return rows


_Q0E = "(A == 1 and (B == 1 or C == 1))"
_QPE = ("((R <= 2 and A == 1 and (B == 1 or C == 1)) or ((R == 3 or R == 6) and B == 1 and (A == 1 or C == 1))"
        " or ((R == 4 or R == 5) and C == 1 and (A == 1 or B == 1)))")
_VARS5 = {"A": {"values": [0, 1], "probs": [0.4, 0.6]}, "B": {"values": [0, 1], "probs": [0.4, 0.6]},
          "C": {"values": [0, 1], "probs": [0.4, 0.6]}, "R": {"values": [1, 2, 3, 4, 5, 6], "probs": [1 / 6] * 6}}
_NET5 = {"type": "series", "children": [{"type": "comp", "id": "A", "p": 0.6},
                                        {"type": "parallel", "children": [{"type": "comp", "id": "B", "p": 0.6}, {"type": "comp", "id": "C", "p": 0.6}]}]}
EXTRA_SIMS = {
    (2, "א"): {"kind": "custom_discrete", "estimate": "P(A) ב-(p,q,s)=(0.6,0.7,0.8)", "exact": float(_PA),
               "params": {"joint": _JOINT, "event": "A == 1"}},
    (2, "ב"): {"kind": "custom_discrete", "estimate": "P(B) ב-(p,q,s)=(0.6,0.7,0.8)", "exact": float(_PB),
               "params": {"joint": _JOINT, "event": "B == 1"}},
    (2, "ג"): {"kind": "custom_discrete", "estimate": "P(A n B) ב-(p,q,s)=(0.6,0.7,0.8)", "exact": float(_PAB),
               "params": {"joint": _JOINT, "event": "A == 1 and B == 1"}},
    (3, "א"): {"kind": "circuit", "estimate": "P(Q) ב-p=0.8, N=(1,2,3)", "exact": float(_PQ), "params": {"event": "S", "network": _NET3}},
    (3, "ב"): {"kind": "circuit", "estimate": "P(A2 | Q) ב-p=0.8, N=(1,2,3)", "exact": float(_PA2Q),
               "params": {"event": "g2a == 1 and g2b == 1", "given": "S == 1", "network": _NET3}},
    (3, "ג"): {"kind": "circuit", "estimate": "P(not A2 | Q) ב-p=0.8, N=(1,2,3)", "exact": float(1 - _PA2Q),
               "params": {"event": "not (g2a == 1 and g2b == 1)", "given": "S == 1", "network": _NET3}},
    (4, "א"): {"kind": "pdf", "estimate": "E[X] ב-μ=0.1 (a=0.96, b=0.52)", "exact": 0.1,
               "params": {"pieces": [{"from": -1, "to": 0, "expr": "0.96*(x+1)"}, {"from": 0, "to": 1, "expr": "0.52"}], "measure": "mean", "expr": "x"}},
    (4, "ג"): {"kind": "pdf", "estimate": "F(-1/2) ב-μ=0 (a=6/5, b=2/5)", "exact": 0.15,
               "params": {"pieces": [{"from": -1, "to": 0, "expr": "1.2*(x+1)"}, {"from": 0, "to": 1, "expr": "0.4"}], "event": "x < -1/2"}},
    (5, "א"): {"kind": "circuit", "estimate": "P(Q0) ב-p=0.6", "exact": float(_P0), "params": {"event": "S", "network": _NET5}},
    (5, "ב"): {"kind": "circuit", "estimate": "P(Q') = P(Q0) ב-p=0.6", "exact": float(_P0), "params": {"event": "S", "network": _NET5}},
    (5, "ג"): {"kind": "custom_discrete", "estimate": "P(Q0 n Q') ב-p=0.6 (סידור אקראי R)", "exact": float(_PJ),
               "params": {"vars": _VARS5, "event": _Q0E + " and " + _QPE}},
    (5, "ד"): {"kind": "custom_discrete", "estimate": "P(Q' | Q0) ב-p=0.6", "exact": float(_PJ / _P0),
               "params": {"vars": _VARS5, "event": _QPE, "given": _Q0E}},
    (5, "ה"): {"kind": "custom_discrete", "estimate": "P(Q' | not Q0) ב-p=0.6", "exact": float(_PR),
               "params": {"vars": _VARS5, "event": _QPE, "given": "not " + _Q0E}},
    (6, "א"): {"kind": "urn", "estimate": "P(W=2) ב-N=5, p=0.2", "exact": 0.2048,
               "params": {"counts": {"hit": 1, "miss": 4}, "draws": 5, "replace": True, "event": "hit == 2"}},
    (6, "ב"): {"kind": "custom_discrete", "estimate": "P(Y=2) ב-λ=2, p=0.5", "exact": _E ** -1 / 2,
               "params": {"joint": _pois_binom_joint(2, 0.5), "event": "Y == 2"}},
    (6, "ג"): {"kind": "custom_discrete", "estimate": "P(X=3 | Y=1) ב-λ=2, p=0.5", "exact": _E ** -1 / 2,
               "params": {"joint": _pois_binom_joint(2, 0.5), "event": "X == 3", "given": "Y == 1"}},
}
for _q in questions:
    _s = EXTRA_SIMS.get((_q["num"], _q.get("part")))
    if _s is not None:
        assert "sim" not in _q, (_q["num"], _q.get("part"))
        _q["sim"] = _s

print("steps:", PS.apply(questions, DATA, CODE), "items")


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
