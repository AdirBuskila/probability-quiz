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
import json, pathlib

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
$$p=1-q.$$""",
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
נניח, בקירוב הסטנדרטי, שלכל מועמד ההסתברות להיוולד בתאריך נתון היא $\frac1{365}$, ללא תלות באחרים (הסבר: ניסוי ברנולי חוזר $N$ פעמים). אז
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
(התפלגות פואסון עם פרמטר $\lambda(1-p)$, מוסטת ב-$k$).""",
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

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
