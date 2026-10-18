# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-D.json -- probability (course 20021-80), semester A 2024, moed A (03.04.2024).
Code 24A-D is fixed by GATE1 (the 20021-80 group; the 20021 group of 25.3.2024 is 24A-A).
6 questions, 21 items (Q1 3, Q2 5, Q3 3, Q4 4, Q5 3, Q6 3), 25 points each.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-D.py

Source: the source PDF opens with a video-meeting cover page (page 1); it is NOT transcribed and NOT shipped.
Exam pp.2-4, official handwritten solutions pp.5-21.
Transcription notes
- Part keys are single letters (printed label is the bold token at the start of the question text).
  Q2 prints א, ב-1, ב-2, ב-3, ב-4 -> keys א ב ג ד ה. Q4 prints א, ב, ג-1, ג-2 -> keys א ב ג ד.
  Q5 prints א, ב-1, ב-2 (and an intro) -> keys א ב ג. Q6 prints א, ב-1, ב-2 -> keys א ב ג.
- Q6(ג): the official answer is P(Q2/Q1)=1 (Q1 is contained in Q2); transcribed as printed.
- Q5: the registration-page screenshot in the exam is decoration and is not shipped.
- Q1 region data is in tools/verify/24A-D/regions.json (RAW_SCHEMA has no `region` field).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-D.json"
CODE = "24A-D"
IMG = "images/exams/24A-D-"


def Q(num, part, topic, question, solution, points, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "official-pdf", "official": True, "confidence": "high", "points": points}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ------------------------------------------------------------------ Q1
Q1_TXT = (r"חגב מבצע שתי קפיצות אקראיות באותו כיוון, אחת אחרי השנייה. אורכי הקפיצות מהווים משתנים מקריים בלתי תלויים בעלי התפלגות אחידה רציפה: "
          r"$X_1\sim U_c(0,1)$ ו-$X_2\sim U_c(0,1)$.")

questions.append(Q(
    1, "א", "uniform_geometric",
    r"**א.** מצאו את ההסתברות שהאורך הכולל $X_1+X_2$ של שתי קפיצות לא יעלה על $\frac23$.",
    r"""$X_1,X_2$ בלתי תלויים, $X_1\sim U_c(0,1)$, $X_2\sim U_c(0,1)$. מרחב המדגם: ריבוע היחידה, $|\Omega|=1$.
$$P\left(X_1+X_2\le\tfrac23\right)=P\left(X_2\le\tfrac23-X_1\right)=\frac{\left|\{x_2\le\frac23-x_1\}\right|}{|\Omega|}=\frac12\left(\frac23\right)^2=\frac29.$$""",
    9, contextId="c1"))

questions.append(Q(
    1, "ב", "uniform_geometric",
    r"**ב.** מהי ההסתברות שגם הקפיצה הראשונה וגם הקפיצה השנייה יהיו קצרות מ-$\frac23$?",
    r"""$X_1,X_2$ בלתי תלויים, ולכן
$$P\left(X_1<\tfrac23\cap X_2<\tfrac23\right)=P\left(X_1<\tfrac23\right)P\left(X_2<\tfrac23\right)=\frac23\cdot\frac23=\frac49.$$
כאשר $P\left(X_1<\frac23\right)=F_{X_1}\left(\frac23\right)=\frac23$: ל-$X\sim U_c(a,b)$ מתקיים $F_X(t)=\frac{t-a}{b-a}$ עבור $a\le t<b$, ובמקרה שלנו $a=0$, $b=1$.
באופן גאומטרי: $\dfrac{\left|\{x_1<\frac23\cap x_2<\frac23\}\right|}{|\Omega|}=\left(\frac23\right)^2=\frac49$.""",
    9, contextId="c1"))

questions.append(Q(
    1, "ג", "uniform_geometric",
    r"**ג.** **אם ידוע** כי אורך הקפיצה הראשונה לא עלה על $\frac23$, מהי ההסתברות שהאורך הכולל של שתי קפיצות לא יעלה על $1$?",
    r"""$$P\left(X_1+X_2\le1\,\Big/\,X_1\le\tfrac23\right)=\frac{P\left(X_1+X_2\le1\cap X_1\le\frac23\right)}{P\left(X_1\le\frac23\right)},\qquad P\left(X_1\le\tfrac23\right)=\frac23.$$
המונה: $\left|\{x_1+x_2\le1\cap x_1\le\frac23\}\right|$, כאשר $x_1+x_2\le1$ שקול ל-$x_2\le1-x_1$. מהתיאור הגאומטרי:
$$=\frac12-\frac12\left(\frac13\right)^2=\frac12-\frac1{18}=\frac8{18}=\frac49.$$
הצבה:
$$P\left(X_1+X_2\le1\,\Big/\,X_1\le\tfrac23\right)=\frac{4/9}{2/3}=\frac23.$$""",
    7, contextId="c1"))

# ------------------------------------------------------------------ Q2
questions.append(Q(
    2, "א", "combinatorics",
    r"**א.** מטילים קובייה **מאוזנת פעמיים** ומסכמים את התוצאות. מהי ההסתברות שסכום התוצאות יהיה שווה ל-6?",
    r"""גישה קלאסית (מרחב מדגם אחיד): $\Omega=\{11,\dots,16,\dots,61,\dots,66\}$, $|\Omega|=36$.
$A$ = ״הסכום שווה ל-6״ $=\{15,24,33,42,51\}$.
$$P(A)=\frac{|A|}{|\Omega|}=\frac5{36}.$$""",
    5))

Q2B = r"מטילים קובייה **מאוזנת שלוש פעמים** ומסכמים את התוצאות." "\n"

questions.append(Q(
    2, "ב", "combinatorics",
    Q2B + r"**ב-1:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-6?",
    r"""$|\Omega|=6^3$ ($\Omega$: שלשות תוצאות).
$B_1$ = ״הסכום שווה ל-6״ $=\{114,141,411,123,132,213,231,312,321,222\}$.
$$P(B_1)=\frac{|B_1|}{|\Omega|}=\frac{10}{6^3}=\frac5{108}.$$""",
    5))

questions.append(Q(
    2, "ג", "conditional_bayes",
    Q2B + r"**ב-2:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-6 **אם ידוע** כי סכום של שתי התוצאות הראשונות היה שווה ל-2?",
    r"""התוצאות $X_1,X_2,X_3$.
$$P(X_1+X_2+X_3=6/X_1+X_2=2)=\frac{P(X_1+X_2+X_3=6\cap X_1+X_2=2)}{P(X_1+X_2=2)}=\frac{P(X_3=4\cap X_1+X_2=2)}{P(X_1+X_2=2)}$$
(ההטלות בלתי תלויות)
$$=\frac{P(X_3=4)\,P(X_1+X_2=2)}{P(X_1+X_2=2)}=P(X_3=4)=\frac16.$$""",
    5))

questions.append(Q(
    2, "ד", "conditional_bayes",
    Q2B + r"**ב-3:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-6 **אם ידוע** כי התוצאה הראשונה הייתה קטנה מהתוצאה השנייה?",
    r"""$$P(X_1+X_2+X_3=6/X_1<X_2)=\frac{P(X_1+X_2+X_3=6\cap X_1<X_2)}{P(X_1<X_2)}.$$
$P(X_1<X_2)=\dfrac{|\{x_1<x_2\}|}{|\Omega_{(2)}|}=\dfrac{15}{36}=\dfrac5{12}$ (מבין 36 זוגות, 6 הם $x_1=x_2$ ו-15 הם $x_1<x_2$).
$\{X_1+X_2+X_3=6\}=\{114,141,411,123,132,213,231,312,321,222\}$, ולכן
$\{X_1+X_2+X_3=6\}\cap\{X_1<X_2\}=\{141,123,132,231\}$, כלומר $P(\cdot)=\dfrac4{6^3}$.
$$P(X_1+X_2+X_3=6/X_1<X_2)=\frac{4}{6^3}\cdot\frac{12}{5}=\frac{4}{5\cdot6\cdot3}=\frac2{45}.$$""",
    5))

questions.append(Q(
    2, "ה", "conditional_bayes",
    Q2B + r"**ב-4:** מהי ההסתברות שסכום התוצאות יהיה שווה ל-6 **אם ידוע** כי שתי התוצאות הראשונות היו זהות?",
    r"""$$P(X_1+X_2+X_3=6/X_1=X_2)=\frac{P(X_1+X_2+X_3=6\cap X_1=X_2)}{P(X_1=X_2)},\qquad P(X_1=X_2)=\frac16.$$
$P(X_1+X_2+X_3=6\cap X_1=X_2)=\dfrac{|\{114,222\}|}{|\Omega|}=\dfrac2{6^3}$. לכן
$$P(X_1+X_2+X_3=6/X_1=X_2)=\frac2{6^3}\cdot6=\frac2{36}=\frac1{18}.$$""",
    5))

# ------------------------------------------------------------------ Q3
Q3_TXT = (r"נתבונן במטריצת ברנולי מהצורה $\boldsymbol Q=\begin{pmatrix}0&X\\Y&X+Y\end{pmatrix}$ כאשר $X$ ו-$Y$ מהווים משתנים מקריים בלתי תלויים בעלי התפלגויות ברנולי: "
          r"$X\sim\mathrm{Ber}(p)$ ו-$Y\sim\mathrm{Ber}(q)$. נגדיר שני משתנים מקריים חדשים: דטרמיננטה $D=\det\boldsymbol Q$ ועקבה $T=\operatorname{tr}\boldsymbol Q$ של מטריצה $\boldsymbol Q$.")
Q3_HEAD = r"$D=\det\boldsymbol Q=-XY$, $\ T=\operatorname{tr}\boldsymbol Q=X+Y$; $X\sim\mathrm{Ber}(p)$, $Y\sim\mathrm{Ber}(q)$ בלתי תלויים." "\n"

questions.append(Q(
    3, "א", "discrete_rv",
    r"**א.** חשבו תוחלת $\mathbb E[D]$ ושונות $\operatorname{var}[D]$ של דטרמיננטה.",
    Q3_HEAD + r"""$$\mathbb E[D]=\mathbb E[-XY]=-\mathbb E[X]\,\mathbb E[Y]=-pq.$$
$\operatorname{Var}[D]=\mathbb E[D^2]-(\mathbb E[D])^2=\mathbb E[D^2]-(pq)^2$, כאשר $\mathbb E[D^2]=\mathbb E[X^2Y^2]=\mathbb E[XY]=\mathbb E[X]\,\mathbb E[Y]=pq$ (כי $X^2=X$, $Y^2=Y$). לכן
$$\operatorname{Var}[D]=pq-(pq)^2=pq(1-pq).$$""",
    8, contextId="c3"))

questions.append(Q(
    3, "ב", "discrete_rv",
    r"**ב.** חשבו תוחלת $\mathbb E[T]$ ושונות $\operatorname{var}[T]$ של עקבה.",
    r"""$$\mathbb E[T]=\mathbb E[X+Y]=\mathbb E[X]+\mathbb E[Y]=p+q.$$
$$\operatorname{Var}[T]=\operatorname{Var}[X+Y]=\operatorname{Var}[X]+\operatorname{Var}[Y]=p(1-p)+q(1-q).$$""",
    8, contextId="c3"))

questions.append(Q(
    3, "ג", "joint_discrete",
    r"**ג.** חשבו את השונות המשותפת $\operatorname{cov}[D,T]$.",
    r"""$\operatorname{Cov}[D,T]=\mathbb E[DT]-\mathbb E[D]\,\mathbb E[T]=\mathbb E[DT]+pq(p+q)$.
$$\mathbb E[DT]=\mathbb E\bigl[-XY(X+Y)\bigr]=-\mathbb E[X^2Y+XY^2]=-\mathbb E[2XY]=-2\,\mathbb E[X]\,\mathbb E[Y]=-2pq$$
(כי $X^2Y=XY$ ו-$XY^2=XY$). לכן
$$\operatorname{Cov}[D,T]=-2pq+pq(p+q)=pq\,(-2+p+q).$$""",
    9, contextId="c3"))

# ------------------------------------------------------------------ Q4
Q4_TXT = (r"נתבונן במשתנה מקרי $X$ בעל פונקציית צפיפות ההסתברות מהצורה" "\n"
          r"$$f(x)=\begin{cases}a(b-|x|),&-b\le x\le b\\ 0,&\text{else}\end{cases}$$" "\n"
          r"כאשר $a>0$ ו-$b>0$.")

questions.append(Q(
    4, "א", "continuous_rv",
    Q4_TXT + "\n" + r"**א.** מצאו את תוחלת המשתנה $\mathbb E[X]$. (אם יהיה בכך צורך, ניתן לבטא אותה דרך המקדמים $a$ ו-$b$).",
    r"""$$\mathbb E[X]=\int_{-\infty}^{+\infty}x\,f_X(x)\,dx=\int_{-b}^{b}x\,f_X(x)\,dx=0,$$
כי $f_X$ זוגית, ולכן $x\,f_X(x)$ אי-זוגית, והתחום סימטרי.""",
    6, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ב", "continuous_rv",
    Q4_TXT + "\n" + r"**ב.** חשבו את המקדמים $a$ ו-$b$ אם נתון כי השונות $\operatorname{var}[X]=\frac23$.",
    r"""נרמול: שטח המשולש שווה ל-1:
$$\frac12\cdot 2b\cdot ab=1\ \Rightarrow\ ab^2=1.$$
שונות: $\operatorname{Var}[X]=\mathbb E[X^2]-(\mathbb E[X])^2=\mathbb E[X^2]$ (כי $\mathbb E[X]=0$):
$$\frac23=\mathbb E[X^2]=\int_{-b}^{b}x^2f_X(x)\,dx=2\int_0^b x^2f_X(x)\,dx=2a\int_0^bx^2(b-x)\,dx=2a\left\{b\cdot\frac{b^3}{3}-\frac{b^4}{4}\right\}=2a\left\{\frac{b^4}{3}-\frac{b^4}{4}\right\}=\frac{ab^4}{6}.$$
לכן $ab^4=4$. יחד עם $ab^2=1$ מתקבל $b^2=4$ ולכן
$$a=\frac14,\qquad b=2.$$""",
    6, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ג", "continuous_rv",
    Q4_TXT + "\n" + r"בהינתן המקדמים $a$ ו-$b$ מהסעיף הקודם:" "\n" r"**ג-1:** חשבו את פונקציית ההתפלגות המצטברת $F_X(t)$ ושרטטו אותה.",
    r"""$f_X(x)=\dfrac14(2-|x|)$ עבור $-2\le x\le2$ (שיא $\frac12$ ב-$x=0$).
$$F_X(t)=\int_{-\infty}^tf_X(x)\,dx=\begin{cases}0,&t<-2,\\ \dfrac12(t+2)\cdot\dfrac{t+2}{4}=\dfrac18(t+2)^2,&-2\le t<0,\\ 1-\dfrac12(2-t)\cdot\dfrac{2-t}{4}=1-\dfrac18(2-t)^2,&0\le t<2,\\ 1,&t\ge2.\end{cases}$$
(לפי שטח המשולש משמאל ל-$t$, שגובהו $\frac{t+2}{4}$, או $1$ פחות שטח המשולש מימין ל-$t$, שגובהו $\frac{2-t}{4}$.)
![גרף פונקציית ההתפלגות המצטברת](images/exams/24A-D-Q4-cdf.png)""",
    7, image=IMG + "Q4-pdf.png"))

questions.append(Q(
    4, "ד", "continuous_rv",
    Q4_TXT + "\n" + r"בהינתן המקדמים $a$ ו-$b$ מהסעיף הקודם:" "\n" r"**ג-2:** מצאו את ההסתברות המותנית $P(X>a\,/\,|X|<1)$.",
    r"""$$P\left(X>\tfrac14\,\Big/\,|X|<1\right)=\frac{P\left(X>\frac14\cap|X|<1\right)}{P(|X|<1)}=\frac{P\left(\frac14<X<1\right)}{P(-1<X<1)}=\frac{F_X(1)-F_X\left(\frac14\right)}{F_X(1)-F_X(-1)}.$$
($P(a<X<b)=F_X(b)-F_X(a)$.) מהנוסחה של $F_X$: $F_X(1)=\frac78$, $F_X\left(\frac14\right)=1-\frac18\cdot\frac{49}{16}$, $F_X(-1)=\frac18$. לכן
$$P\left(X>\tfrac14\,\Big/\,|X|<1\right)=\frac{11}{32}.$$""",
    6, image=IMG + "Q4-pdf.png"))

# ------------------------------------------------------------------ Q5
Q5_TXT = r"**בתאריך 1 באפריל** נפתחה הרשמה מקוונת ללימודים במכון הטכנולוגי חולון דרך מילוי טופס הרשמה באתר המכון."
Q5_HINT = (r"**הערה:** לידיעתך," "\n"
           r"$$\sum_{j=m}^{\infty}C_j^m\frac{a^j}{j!}=\frac{a^m}{m!}e^a.$$" "\n"
           r"(יכול להיות שאין צורך להשתמש בנוסחה זו.)")

questions.append(Q(
    5, "א", "special_discrete",
    r"**א.** **אם ידוע** כי בדיוק $N$ מועמדים מילאו את טופס ההרשמה, מהי ההסתברות שמתוכם בדיוק $k$ נולדו ביום ההרשמה? **יש לתת הסבר מפורט.**",
    r"""נגדיר $W=$ מספר המועמדים מתוך $N$ אשר נולדו ב-01.04. אז $W\sim\mathrm{Bin}\left(N,p=\dfrac1{365}\right)$:
$$P(W=k)=\binom Nk p^k(1-p)^{N-k},\qquad k=0,1,\dots,N.$$
(יש לתת הסבר מפורט באמצעות משפט הפירוק: כל מועמד הוא ניסוי ברנולי בלתי תלוי.)""",
    10, contextId="c5"))

questions.append(Q(
    5, "ב", "special_discrete",
    r"**ב-1:** נניח כי מספר המועמדים ($X$) שמילאו את טופס ההרשמה ביום ההרשמה מהווה משתנה מקרי בעל התפלגות פואסון $X\sim P(\lambda)$. מהי ההסתברות שמתוך כל אלה שמילאו את טופס ההרשמה, בדיוק $k$ נולדו ביום ההרשמה? שימו לב כי אין אנו יודעים כמה מועמדים נגשו לטופס ההרשמה!" "\n" + Q5_HINT,
    r"""נתון כי מספר ממלאי הטופס הוא משתנה פואסוני: $X\sim P(\lambda)$, $\ P(X=j)=\dfrac{\lambda^j}{j!}e^{-\lambda}$, $j=0,1,2,\dots$
נגדיר $Y=$ מספר המועמדים מתוכם שנולדו ב-01.04 ($p=\frac1{365}$).
$$P(Y=k)=\sum_{j=k}^{\infty}P(Y=k/X=j)P(X=j)=\sum_{j=k}^{\infty}\binom jk p^k(1-p)^{j-k}\,\frac{\lambda^j}{j!}e^{-\lambda}=e^{-\lambda}\frac{p^k}{(1-p)^k}\sum_{j=k}^{\infty}\binom jk\frac{[\lambda(1-p)]^j}{j!}.$$
לפי הנוסחה שבהערה, עם $m=k$ ו-$a=\lambda(1-p)$, הסכום שווה ל-$\dfrac{\lambda^k(1-p)^k}{k!}e^{\lambda(1-p)}$. הצבה ופישוט:
$$P(Y=k)=e^{-\lambda p}\frac{(\lambda p)^k}{k!},\qquad k=0,1,2,\dots,\qquad Y\sim P(\lambda p).$$""",
    10, contextId="c5"))

questions.append(Q(
    5, "ג", "conditional_bayes",
    r"**ב-2:** **אם ידוע** כי בין ממלאי טופס ההרשמה בדיוק $k$ נולדו בתאריך ההרשמה, מהי ההסתברות שבדיוק $n$ מועמדים מילאו את הטופס?" "\n" + Q5_HINT,
    r"""לפי נוסחת בייס:
$$P(X=n/Y=k)=\frac{P(Y=k/X=n)\,P(X=n)}{P(Y=k)}=\frac{\binom nk p^k(1-p)^{n-k}\cdot\dfrac{\lambda^n}{n!}e^{-\lambda}}{e^{-\lambda p}\dfrac{(\lambda p)^k}{k!}}.$$
בצמצום:
$$P(X=n/Y=k)=\frac{[\lambda(1-p)]^{n-k}}{(n-k)!}\,e^{-\lambda(1-p)},\qquad n=k,k+1,\dots$$""",
    5, contextId="c5"))

# ------------------------------------------------------------------ Q6
Q6_TXT = (r"סטודנט של המכון הטכנולוגי חולון הרכיב מעגל חשמלי $Q_1$ מחמש יחידות $A,B,C,D$ ו-$E$ הפועלות ללא תלות אחת בשנייה בהסתברויות הזהות $p$.")

questions.append(Q(
    6, "א", "circuits",
    r"**א.** מהי ההסתברות שמעגל $Q_1$ פעיל?",
    r"""מותנים ב-$E$:
$$P(Q_1)=P(Q_1/E)P(E)+P(Q_1/\bar E)P(\bar E)=(2p-p^2)^2\,p+(2p^2-p^4)(1-p).$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ב", "circuits",
    r"הסטודנט פירק את המעגל $Q_1$ והרכיב מעגל חדש $Q_2$ – **מאותן היחידות**." "\n" r"**ב-1:** מהי ההסתברות שמעגל $Q_2$ יפעל?",
    r"""מותנים ב-$A$ (ביחידה $A$ ב-$Q_2$ יש מסלול ישיר בין שני קצות המעגל):
$$P(Q_2)=P(Q_2/A)P(A)+P(Q_2/\bar A)P(\bar A).$$
- $P(Q_2/A)=1$ ($A$ פעילה ומקצרת את המעגל);
- $P(Q_2/\bar A)=P\bigl((E\cap B)\cup(C\cap D)\bigr)=2p^2-p^4$.

$$P(Q_2)=p+(1-p)(2p^2-p^4).$$""",
    9, contextId="c6"))

questions.append(Q(
    6, "ג", "circuits",
    r"הסטודנט פירק את המעגל $Q_1$ והרכיב מעגל חדש $Q_2$ – **מאותן היחידות**." "\n" r"**ב-2:** **אם ידוע** כי מעגל $Q_1$ פעיל, מהי ההסתברות שגם המעגל $Q_2$ יפעל?",
    r"""$$P(Q_2/Q_1)=\frac{P(Q_1\cap Q_2)}{P(Q_1)},\qquad P(Q_1)=p(2p-p^2)^2+(1-p)(2p^2-p^4).$$
נסמן $\tilde Q=Q_1\cap Q_2$ ונחשב בהתניה על $A,E$:
$$P(\tilde Q)=P(\tilde Q/A\cap E)P(A\cap E)+P(\tilde Q/\bar A\cap\bar E)P(\bar A\cap\bar E)+P(\tilde Q/A\cap\bar E)P(A\cap\bar E)+P(\tilde Q/\bar A\cap E)P(\bar A\cap E).$$
- $\tilde Q/A\cap E$: $P(B\cup D)=2p-p^2$, וההסתברות לכך $p^2$;
- $\tilde Q/\bar A\cap\bar E$: $P(C\cap D)=p^2$, וההסתברות לכך $(1-p)^2$;
- $\tilde Q/A\cap\bar E$: $P\bigl(B\cup(C\cap D)\bigr)=p+p^2-p^3$, וההסתברות לכך $p(1-p)$;
- $\tilde Q/\bar A\cap E$: $P\bigl(C\cap(B\cup D)\bigr)=p(2p-p^2)$, וההסתברות לכך $p(1-p)$.

$$P(Q_1\cap Q_2)=(2p-p^2)p^2+p^2(1-p)^2+p(1-p)(p+p^2-p^3)+p^2(1-p)(2p-p^2).$$
הצבה סופית (הביטוי שווה ל-$P(Q_1)$):
$$P(Q_2/Q_1)=1.$$""",
    7, contextId="c6"))

exam = {
    "examCode": CODE,
    "examLabel": "הסתברות (20021-80), סמסטר א׳ תשפ״ד, מועד א (03.04.2024)",
    "year": 2024,
    "examDate": "03.04.2024",
    "sourceFile": "24A-D exam pp.2-4",
    "solutionFile": "24A-D official handwritten solutions pp.5-21",
    "contexts": {
        "c1": {"kind": "image", "title": "שאלה 1: החגב", "image": IMG + "Q1-grasshopper.png", "caption": Q1_TXT},
        "c3": {"kind": "text", "title": "שאלה 3", "text": Q3_TXT},
        "c5": {"kind": "text", "title": "שאלה 5", "text": Q5_TXT},
        "c6": {"kind": "image", "title": "שאלה 6: מעגלים", "image": IMG + "Q6-circuits.png", "caption": Q6_TXT},
    },
    "questions": questions,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
