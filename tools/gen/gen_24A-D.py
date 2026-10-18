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
- Q1 area items carry `region` (area figure) and, with the other numeric parts, `sim`: see EXTRAS near the end.
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
    (1, "א"): {"region": REG([lin(1, 1, "2/3", "<=")], 2 / 9, "האירוע X1+X2<=2/3"),
               "sim": AREA("P(X1+X2<=2/3)", 2 / 9)},
    (1, "ב"): {"region": REG([lin(1, 0, "2/3", "<"), lin(0, 1, "2/3", "<")], 4 / 9, "האירוע X1<2/3 וגם X2<2/3"),
               "sim": AREA("P(X1<2/3, X2<2/3)", 4 / 9)},
    (1, "ג"): {"region": REG([lin(1, 1, 1, "<=")], 2 / 3, "האירוע X1+X2<=1 בהינתן X1<=2/3", given=[lin(1, 0, "2/3", "<=")]),
               "sim": AREA("P(X1+X2<=1 | X1<=2/3)", 2 / 3)},
    (2, "א"): {"sim": DICE("P(sum = 6)", 5 / 36, 2, "sum == 6")},
    (2, "ב"): {"sim": DICE("P(sum = 6)", 5 / 108, 3, "sum == 6")},
    (2, "ג"): {"sim": DICE("P(sum = 6 | d1+d2 = 2)", 1 / 6, 3, "sum == 6", "d1+d2 == 2")},
    (2, "ד"): {"sim": DICE("P(sum = 6 | d1<d2)", 2 / 45, 3, "sum == 6", "d1 < d2")},
    (2, "ה"): {"sim": DICE("P(sum = 6 | d1=d2)", 1 / 18, 3, "sum == 6", "d1 == d2")},
    (4, "ד"): {"sim": PDF("P(X>1/4 | |X|<1)", 11 / 32, [(-2, 0, "(2+x)/4"), (0, 2, "(2-x)/4")], "x > 1/4", "abs(x) < 1")},
}
for _q in questions:
    _x = EXTRAS.get((_q["num"], _q.get("part")))
    if _x:
        _q.update(_x)


# ---- extra sims for items with symbolic answers, at sample parameter values (stated in `estimate`)
import math as _m


def _bern2(p, q):
    return {"X": {"values": [0, 1], "probs": [1 - p, p]}, "Y": {"values": [0, 1], "probs": [1 - q, q]}}


_DET = "0*(X+Y)-X*Y"      # det Q straight from the matrix entries
_TR = "0+(X+Y)"
_BR = {"edges": [{"id": "A", "from": "L", "to": "T", "p": 0.6}, {"id": "B", "from": "T", "to": "R", "p": 0.6},
                 {"id": "C", "from": "L", "to": "U", "p": 0.6}, {"id": "D", "from": "U", "to": "R", "p": 0.6},
                 {"id": "E", "from": "T", "to": "U", "p": 0.6}], "source": "L", "sink": "R"}
_Q1E = "(A and B) or (C and D) or (A and E and D) or (C and E and B)"
_Q2E = "A or (E and B) or (C and D)"
_Q2G = {"edges": [{"id": "A", "from": "L", "to": "R", "p": 0.6}, {"id": "E", "from": "L", "to": "T", "p": 0.6},
                  {"id": "B", "from": "T", "to": "R", "p": 0.6}, {"id": "C", "from": "L", "to": "U", "p": 0.6},
                  {"id": "D", "from": "U", "to": "R", "p": 0.6}], "source": "L", "sink": "R"}
_NX = 25      # the number of candidates X ~ Poisson(4) is truncated at 25 (tail mass ~1e-11 goes to the last value)


def _thinned(event, given=None, lam=4.0, p=0.25):
    pk = [_m.exp(-lam) * lam ** k / _m.factorial(k) for k in range(_NX + 1)]
    pk[-1] += 1 - sum(pk)
    vs = {"X": {"values": list(range(_NX + 1)), "probs": pk}}
    for i in range(1, _NX + 1):
        vs["B%d" % i] = {"values": [0, 1], "probs": [1 - p, p]}
    y = "(" + "+".join("B%d*(X>=%d)" % (i, i) for i in range(1, _NX + 1)) + ")"
    out = {"vars": vs, "event": event.replace("Y", y)}
    if given:
        out["given"] = given.replace("Y", y)
    return out


_V = _bern2(0.3, 0.6)
_TRI = [{"from": -2, "to": 0, "expr": "(2+x)/4"}, {"from": 0, "to": 2, "expr": "(2-x)/4"}]
EXTRA_SIMS = {
    (3, "א"): {"kind": "custom_discrete", "estimate": "Var[D] ב-p=0.3, q=0.6", "exact": 0.1476,
               "params": {"vars": _V, "measure": "var", "expr": _DET}},
    (3, "ב"): {"kind": "custom_discrete", "estimate": "Var[T] ב-p=0.3, q=0.6", "exact": 0.45,
               "params": {"vars": _V, "measure": "var", "expr": _TR}},
    (3, "ג"): {"kind": "custom_discrete", "estimate": "cov[D,T] ב-p=0.3, q=0.6", "exact": -0.198,
               "params": {"vars": _V, "measure": "cov", "expr": [_DET, _TR]}},
    (4, "א"): {"kind": "pdf", "estimate": "E[X] ב-a=1/4, b=2", "exact": 0,
               "params": {"pieces": _TRI, "measure": "mean", "expr": "x"}},
    (4, "ב"): {"kind": "pdf", "estimate": "Var[X] ב-a=1/4, b=2", "exact": 2 / 3,
               "params": {"pieces": _TRI, "measure": "var", "expr": "x"}},
    (4, "ג"): PDF("F(-1)", 1 / 8, [(-2, 0, "(2+x)/4"), (0, 2, "(2-x)/4")], "x <= -1"),
    (5, "א"): {"kind": "urn", "estimate": "P(W=2) ב-N=6, p=0.25 (במקום 1/365)", "exact": 1215 / 4096,
                "params": {"counts": {"hit": 1, "miss": 3}, "draws": 6, "replace": True, "event": "hit == 2"}},
    (5, "ב"): {"kind": "custom_discrete", "estimate": "P(Y=2) ב-λ=4, p=0.25 (X קטוע ב-25)", "exact": _m.exp(-1) / 2,
               "params": _thinned("Y == 2")},
    (5, "ג"): {"kind": "custom_discrete", "estimate": "P(X=4 | Y=2) ב-λ=4, p=0.25 (X קטוע ב-25)", "exact": 9 * _m.exp(-3) / 2,
               "params": _thinned("X == 4", given="Y == 2")},
    (6, "א"): {"kind": "circuit", "estimate": "P(Q1) ב-p=0.6", "exact": 0.65952, "params": dict(_BR, event="S")},
    (6, "ב"): {"kind": "circuit", "estimate": "P(Q2) ב-p=0.6", "exact": 0.83616, "params": dict(_Q2G, event="S")},
    (6, "ג"): {"kind": "circuit", "estimate": "P(Q2 | Q1) ב-p=0.6", "exact": 1,
               "params": dict(_BR, event=_Q2E, given=_Q1E)},
}
for _q in questions:
    _x = EXTRA_SIMS.get((_q["num"], _q.get("part")))
    if _x and "sim" not in _q:
        _q["sim"] = _x


# ---- rubric / pitfalls / steps (ai-draft). Every expected value is re-derived independently, by exact arithmetic and
# by Monte Carlo, in tools/verify/24A-D/steps_check.py (which reads the generated raw JSON).
from fractions import Fraction as Fr

FRAC = 0.0006   # tolerance when the answer is a non-terminating fraction entered as a 3-4 digit decimal


def O(*v):
    return [{"id": "abcdefgh"[i], "value": t} for i, t in enumerate(v)]


def CH(prompt, opts, ans, explain):
    return {"type": "choice", "prompt": prompt, "options": O(*opts), "correctId": "abcdefgh"[ans], "explain": explain}


def NU(prompt, val, explain):
    val = Fr(val)
    small = abs(val) < Fr(1, 10)           # small values need more digits: a 0.0006 tolerance would accept 0.02 for 0.0206
    a = round(float(val), 6)
    exact = (val * 10000).denominator == 1
    return {"type": "numeric", "prompt": prompt + ("" if exact else " (שבר או עשרוני)"), "answer": a,
            "tol": 0 if exact else (6e-5 if small else FRAC), "explain": explain}


def RB(*r):
    return [{"text": t, "points": p} for t, p in r]


S = {}


def ADD(num, part, rub, pit, steps):
    S[(num, part)] = (rub, pit, steps)


OMEGA = r"אורכי שתי הקפיצות $(X_1,X_2)$ אחידים וב״ת ב-$(0,1)$. מהו שטח מרחב המדגם $|\Omega|$?"
OMEGA_X = r"הריבוע $(0,1)^2$ שטחו $1$, ולכן כאן ההסתברות שווה לשטח. כשמרחב המדגם אינו ריבוע היחידה חייבים לחלק ב-$|\Omega|$."

ADD(1, "א",
    RB((r"גישה גאומטרית: ההסתברות היא שטח האזור חלקי $|\Omega|=1$", 3), (r"האירוע $X_2\le\frac23-X_1$ הוא משולש בפינה $(0,0)$ בניצבים $\frac23$", 3), (r"שטח $\frac12\left(\frac23\right)^2=\frac29$", 3)),
    [r"להשתמש בריבוע בצלע $\frac23$ במקום משולש ולקבל $\frac49$", r"לחשב את שטח המשולש ללא הגורם $\frac12$"],
    [NU(OMEGA, 1, OMEGA_X),
     CH(r"איזה אזור מתאים לאירוע $X_1+X_2\le\frac23$?",
        [r"משולש בפינה $(0,0)$ בניצבים $\frac23$", r"ריבוע בפינה $(0,0)$ בצלע $\frac23$", r"משולש בפינה $(0,0)$ בניצבים $\frac13$"], 0,
        r"הישר $x_1+x_2=\frac23$ חותך את הצירים ב-$\frac23$. הריבוע הוא האירוע $\max<\frac23$ (שטח $\frac49$), והמשולש בניצבים $\frac13$ הוא $\frac1{18}$."),
     NU(r"מהו שטח האזור $\{X_1+X_2\le\frac23\}$?", Fr(2, 9), r"$\frac12\cdot\frac23\cdot\frac23=\frac29$.")])

ADD(1, "ב",
    RB((r"אי-תלות: $P(X_1<\frac23\cap X_2<\frac23)=P(X_1<\frac23)P(X_2<\frac23)$", 3), (r"$F(\frac23)=\frac23$ לכל אחד", 3), (r"התשובה $\frac49$ (או שטח הריבוע בצלע $\frac23$)", 3)),
    [r"להוסיף במקום לכפול: $\frac23+\frac23$", r"להתבלבל עם המשולש $X_1+X_2<\frac23$"],
    [NU(OMEGA, 1, OMEGA_X),
     CH(r"איזה אירוע הוא $\{X_1<\frac23\}\cap\{X_2<\frac23\}$?", [r"ריבוע בפינה $(0,0)$ בצלע $\frac23$", r"רצועה אנכית ברוחב $\frac23$", r"משולש בפינה $(0,0)$ בניצבים $\frac23$"], 0,
        r"שני תנאים בלתי תלויים על כל קואורדינטה: חיתוך שתי רצועות הוא ריבוע (שטח $\frac49$). רצועה אחת נותנת $\frac23$, והמשולש הוא $X_1+X_2<\frac23$ ($\frac29$)."),
     NU(r"מהי $P(X_1<\frac23)$?", Fr(2, 3), r"$F_{X_1}(\frac23)=\frac23$."),
     NU(r"מהו שטח הריבוע, כלומר $P(X_1<\frac23\cap X_2<\frac23)$?", Fr(4, 9), r"$\frac23\cdot\frac23=\frac49$.")])

ADD(1, "ג",
    RB((r"הגדרת המותנית $\frac{P(X_1+X_2\le1\cap X_1\le\frac23)}{P(X_1\le\frac23)}$ והמכנה $\frac23$", 2), (r"שטח החיתוך: $\frac12-\frac12\cdot\frac19=\frac49$", 3), (r"התשובה $\frac23$", 2)),
    [r"לחלק ב-$|\Omega|=1$ במקום ב-$\frac23$", r"לחשב את המשולש שנחתך כ-$\frac12\left(\frac23\right)^2$ (ניצביו $\frac13$)"],
    [NU(OMEGA, 1, OMEGA_X),
     NU(r"מהי $P(X_1\le\frac23)$? (אירוע התנאי, המכנה)", Fr(2, 3), r"רצועה ברוחב $\frac23$: שטח $\frac23$."),
     NU(r"מהו שטח החיתוך $\{X_1+X_2\le1\}\cap\{X_1\le\frac23\}$?", Fr(4, 9), r"המשולש $X_1+X_2\le1$ בשטח $\frac12$ פחות הפינה $\{x_1>\frac23\}$ בניצבים $\frac13$ ושטחה $\frac1{18}$: $\frac49$."),
     NU(r"מהי ההסתברות המותנית?", Fr(2, 3), r"$\frac{4/9}{2/3}=\frac23$.")])

# ---- Q2 (fair dice)
Q2M = [r"מרחב מדגם אחיד על $6^n$ סדרות סדורות של תוצאות: $P=\frac{|A|}{6^n}$", r"הסכום מתפלג אחיד על ערכיו האפשריים", r"התפלגות בינומית"]
Q2M_EX = r"לכל סדרה סדורה אותה הסתברות, אבל לסכומים לא (סכום $7$ שכיח פי $6$ מסכום $2$), ולכן יש לספור סדרות. הבינומית סופרת הצלחות ולא סכומים."
ADD(2, "א",
    RB((r"מרחב מדגם אחיד: $|\Omega|=36$", 2), (r"האירוע $\{15,24,33,42,51\}$, $|A|=5$", 2), (r"התשובה $\frac5{36}$", 1)),
    [r"לספור את $(3,3)$ פעמיים או לשכוח זוגות סדורים"],
    [CH(r"מטילים קובייה מאוזנת פעמיים. איזה מודל מתאים לחישוב $P(\text{sum}=6)$?", Q2M, 0, Q2M_EX),
     NU(r"כמה זוגות סדורים $(i,j)$ נותנים סכום $6$?", 5, r"$(1,5),(2,4),(3,3),(4,2),(5,1)$."),
     NU(r"מהי $P(\text{sum}=6)$?", Fr(5, 36), r"$\frac5{36}$.")])

ADD(2, "ב",
    RB((r"$|\Omega|=6^3$ שלשות סדורות", 1), (r"ספירת השלשות עם סכום $6$: $10$ שלשות", 3), (r"התשובה $\frac{10}{216}=\frac5{108}$", 1)),
    [r"לספור רק צירופים ולא שלשות סדורות (למשל לספור $123$ פעם אחת)"],
    [CH(r"מטילים קובייה מאוזנת שלוש פעמים. איזה מודל מתאים לחישוב $P(\text{sum}=6)$?", Q2M, 0, Q2M_EX),
     NU(r"מהו $|\Omega|$ בשלוש הטלות?", 216, r"$6^3=216$."),
     NU(r"כמה שלשות סדורות נותנות סכום $6$? (הצירופים: $\{1,1,4\},\{1,2,3\},\{2,2,2\}$ בסדרים שונים)", 10, r"$3+6+1=10$."),
     NU(r"מהי $P(\text{sum}=6)$?", Fr(5, 108), r"$\frac{10}{216}=\frac5{108}$.")])

ADD(2, "ג",
    RB((r"הסתברות מותנית: $\frac{P(B\cap C)}{P(C)}$ עם $C=\{X_1+X_2=2\}$", 2), (r"אי-תלות: $B\cap C=\{X_3=4\}\cap C$", 2), (r"התשובה $P(X_3=4)=\frac16$", 1)),
    [r"להשתמש ב-$P(B)=\frac5{108}$ ולהתעלם מהנתון", r"לחלק ב-$|\Omega|=216$"],
    [CH(r"נתון שסכום שתי ההטלות הראשונות הוא $2$. מהי ההסתברות שסכום שלוש ההטלות $6$?",
        [r"$P(X_3=4)=\frac16$: ההטלה השלישית בלתי תלויה בראשונות", r"$P(B)=\frac5{108}$, כי הנתון אינו משנה", r"$\frac1{36}$"], 0,
        r"סכום $2$ בשתי הראשונות מחייב $(1,1)$ ואז נדרש $X_3=4$. $P(B)\approx0.0463$ אינו התשובה כי הנתון משנה."),
     NU(r"מהי $P(C)$, ההסתברות ש-$X_1+X_2=2$? (התנאי)", Fr(1, 36), r"רק $(1,1)$: $\frac1{36}$."),
     NU(r"מהי $P(B\cap C)$, כלומר $(1,1,4)$?", Fr(1, 216), r"$\frac1{216}$."),
     NU(r"מהי $P(B/C)$?", Fr(1, 6), r"$\frac{1/216}{1/36}=\frac16$.")])

ADD(2, "ד",
    RB((r"$P(X_1<X_2)=\frac{15}{36}=\frac5{12}$ (חצי מהזוגות השונים)", 2), (r"$B\cap D=\{141,123,132,231\}$, $P=\frac4{216}$", 2), (r"התשובה $\frac2{45}$", 1)),
    [r"לספור $P(X_1<X_2)=\frac{15}{36}$ כ-$\frac12$ (שוכחים את הזוגות השווים)", r"להניח אי-תלות בין הסכום לבין התנאי"],
    [CH(r"נתון ש-$X_1<X_2$. מהי ההסתברות שסכום שלוש ההטלות $6$?",
        [r"מנה $\frac{P(B\cap D)}{P(D)}$, כי הסכום תלוי בתנאי", r"$P(B)=\frac5{108}$, כי $X_1<X_2$ אינו משפיע על הסכום", r"$\frac16$"], 0,
        r"$X_1<X_2$ פוסל שלשות רבות ולכן $\frac2{45}\approx0.0444\ne P(B)\approx0.0463$."),
     NU(r"מהי $P(D)=P(X_1<X_2)$? (אירוע התנאי)", Fr(5, 12), r"$\frac{15}{36}=\frac5{12}$."),
     NU(r"מהי $P(B\cap D)$, סכום $6$ וגם $X_1<X_2$? (השלשות $141,123,132,231$)", Fr(1, 54), r"$\frac4{216}=\frac1{54}$."),
     NU(r"מהי $P(B/D)$?", Fr(2, 45), r"$\frac{1/54}{5/12}=\frac{12}{270}=\frac2{45}$.")])

ADD(2, "ה",
    RB((r"$P(X_1=X_2)=\frac16$", 1), (r"$B\cap E=\{114,222\}$, $P=\frac2{216}$", 2), (r"התשובה $\frac1{18}$", 2)),
    [r"לספור את $P(X_1=X_2)$ כ-$\frac1{36}$", r"לשכוח את $(2,2,2)$ או $(1,1,4)$"],
    [CH(r"נתון ששתי ההטלות הראשונות זהות. מהי ההסתברות שסכום שלוש ההטלות $6$?",
        [r"מנה $\frac{P(B\cap E)}{P(E)}$, כי הסכום תלוי בתנאי", r"$P(B)=\frac5{108}$, כי הנתון אינו משנה", r"$\frac16$"], 0,
        r"$X_1=X_2$ מותיר רק $114$ ו-$222$ מבין עשרת הצירופים, ולכן $\frac1{18}\approx0.0556\ne P(B)\approx0.0463$."),
     NU(r"מהי $P(E)=P(X_1=X_2)$? (אירוע התנאי)", Fr(1, 6), r"$6$ זוגות מתוך $36$."),
     NU(r"מהי $P(B\cap E)$, סכום $6$ ושתי הראשונות זהות? (השלשות $114,222$)", Fr(1, 108), r"$\frac2{216}=\frac1{108}$."),
     NU(r"מהי $P(B/E)$?", Fr(1, 18), r"$\frac{1/108}{1/6}=\frac1{18}$.")])

# ---- Q3 (matrix [[0,X],[Y,X+Y]]; X~Ber(p), Y~Ber(q); samples p=0.3, q=0.6)
ADD(3, "א",
    RB((r"פישוט $D=-XY$", 2), (r"$\mathbb E[D]=-\mathbb E[X]\mathbb E[Y]=-pq$ (אי-תלות)", 2), (r"$\mathbb E[D^2]=pq$ ולכן $\operatorname{Var}[D]=pq(1-pq)$", 4)),
    [r"לשכוח את הסימן ולכתוב $\mathbb E[D]=pq$", r"לכתוב $\operatorname{Var}[D]=pq-pq=0$ (מבלבלים $\mathbb E[D^2]$ עם $(\mathbb E[D])^2$)"],
    [CH(r"ב-$p=0.3$, $q=0.6$: מהי $P(D=-1)$? ($D=0\cdot(X+Y)-XY$)", [r"$pq=0.18$", r"$p+q-pq=0.72$", r"$p+q=0.9$"], 0,
        r"$D=-1$ בדיוק כאשר $X=Y=1$ (הסתברות $pq$). $p+q-pq$ היא $P(X=1\text{ or }Y=1)$, ו-$p+q$ אינה הסתברות של אירוע זה."),
     NU(r"באותם ערכים, מהי $\mathbb E[D]$?", Fr(-9, 50), r"$-pq=-0.18$."),
     NU(r"באותם ערכים, מהי $\operatorname{Var}[D]$?", Fr("0.1476"), r"$\mathbb E[D^2]=0.18$, ו-$0.18-0.18^2=0.1476$.")])

ADD(3, "ב",
    RB((r"$T=X+Y$ וליניאריות התוחלת: $\mathbb E[T]=p+q$", 3), (r"אי-תלות: $\operatorname{Var}[T]=p(1-p)+q(1-q)$", 5)),
    [r"להוסיף $2\operatorname{Cov}$ בטעות כשהמשתנים בלתי תלויים"],
    [CH(r"איזה ביטוי נכון עבור $\operatorname{Var}[X+Y]$ כש-$X,Y$ בלתי תלויים?",
        [r"$\operatorname{Var}[X]+\operatorname{Var}[Y]$", r"$\operatorname{Var}[X]+\operatorname{Var}[Y]+2pq$", r"$\operatorname{Var}[X]\cdot\operatorname{Var}[Y]$"], 0,
        r"לבלתי תלויים $\operatorname{Cov}=0$ ולכן השונויות מתחברות. ב-$p=0.3,q=0.6$: $0.45$; הביטוי השני נותן $0.81$, והשלישי $0.0504$."),
     NU(r"ב-$p=0.3$, $q=0.6$: מהי $\mathbb E[T]$?", Fr(9, 10), r"$p+q=0.9$."),
     NU(r"באותם ערכים, מהי $\operatorname{Var}[T]$?", Fr(9, 20), r"$0.21+0.24=0.45$.")])

ADD(3, "ג",
    RB((r"$\operatorname{Cov}=\mathbb E[DT]-\mathbb E[D]\mathbb E[T]$", 2), (r"$\mathbb E[DT]=\mathbb E[-XY(X+Y)]=-2pq$ (שימוש ב-$X^2Y=XY$)", 4), (r"התשובה $pq(p+q-2)$", 3)),
    [r"לכתוב $\mathbb E[X^2Y]=p^2q$ במקום $pq$", r"לשכוח את הסימן השלילי של $D$"],
    [NU(r"ב-$p=0.3$, $q=0.6$: מהי $\mathbb E[DT]$? ($DT=-XY(X+Y)$ שווה $-2$ רק ב-$X=Y=1$)", Fr(-9, 25), r"$-2pq=-0.36$."),
     NU(r"באותם ערכים, מהו המכפלה $\mathbb E[D]\,\mathbb E[T]$?", Fr(-81, 500), r"$(-0.18)(0.9)=-0.162$."),
     NU(r"מהי $\operatorname{cov}[D,T]$?", Fr(-99, 500), r"$-0.36+0.162=-0.198=pq(p+q-2)$.")])

# ---- Q4 (pdf a(b-|x|) on [-b,b])
ADD(4, "א",
    RB((r"הצפיפות זוגית ולכן $x\,f(x)$ אי-זוגית", 3), (r"התחום סימטרי ולכן האינטגרל $0$", 3)),
    [r"לחשב $\mathbb E[X]=\frac b3$ (זו התוחלת של $|X|$, לא של $X$)"],
    [CH(r"מהי $\mathbb E[X]$? (במקרה $a=\frac14$, $b=2$)", [r"$0$: הצפיפות זוגית והתחום סימטרי", r"$\frac b2=1$", r"$\frac b3=\frac23$"], 0,
        r"$\int_{-b}^b x f(x)\,dx=0$ כי $xf(x)$ אי-זוגית. $\frac b3=E|X|$ ו-$\frac b2$ אינו אף אחד מהם."),
     NU(r"מהי $\mathbb E[X]$ ב-$a=\frac14$, $b=2$?", 0, r"$0$.")])

ADD(4, "ב",
    RB((r"נרמול: שטח המשולש $\frac12\cdot2b\cdot ab=1$, כלומר $ab^2=1$", 2), (r"שונות: $\mathbb E[X^2]=\frac{ab^4}6=\frac23$, כלומר $ab^4=4$", 2), (r"פתרון: $b^2=4$ ולכן $a=\frac14$, $b=2$", 2)),
    [r"לחשב את שונות הצפיפות בלי הגורם $2$ מהסימטריה", r"להשתמש ב-$\mathbb E[X]$ כמשוואה (הוא $0$ תמיד ואינו מוסיף מידע)"],
    [CH(r"אילו תנאים קובעים את $a$ ו-$b$?", [r"נרמול ושונות: שתי משוואות לשני נעלמים", r"נרמול ותוחלת: $\mathbb E[X]=0$ מספיק", r"שונות בלבד"], 0,
        r"התוחלת היא $0$ לכל $a,b$ ולכן אינה נותנת משוואה. נרמול נותן $ab^2=1$ והשונות נותנת $ab^4=4$."),
     NU(r"מהו $ab^4$? (מ-$\operatorname{Var}[X]=\frac{ab^4}6=\frac23$)", 4, r"$ab^4=6\cdot\frac23=4$."),
     NU(r"מחלקים את $ab^4=4$ ב-$ab^2=1$ ומקבלים $b^2=4$. מהו $b$?", 2, r"$b>0$."),
     NU(r"מהו $a=\frac1{b^2}$?", Fr(1, 4), r"$a=\frac14$.")])

ADD(4, "ג",
    RB((r"אינטגרציה של $\frac14(2-|x|)$ על כל קטע", 3), (r"$F(t)=\frac{(t+2)^2}8$ ל-$-2\le t<0$ ו-$1-\frac{(2-t)^2}8$ ל-$0\le t<2$", 3), (r"שרטוט הגרף", 1)),
    [r"לשכוח את המסה $\frac12$ שנצברה עד $0$ בקטע הימני", r"לרשום $\frac{(t+2)^2}{4}$ (בלי החילוק ב-$2$ משטח המשולש)"],
    [NU(r"מהי $F_X(0)$?", Fr(1, 2), r"הצפיפות סימטרית סביב $0$."),
     CH(r"איזו נוסחה נכונה ל-$F_X(t)$ עבור $-2\le t<0$? (נבדוק ב-$t=-1$)", [r"$\frac{(t+2)^2}8$", r"$\frac{(t+2)^2}4$", r"$\frac{(2-t)^2}8$"], 0,
        r"שטח המשולש משמאל ל-$t$: בסיס $t+2$ וגובה $\frac{t+2}4$, כלומר $\frac{(t+2)^2}8$ (ב-$-1$: $\frac18$). האחרות נותנות $\frac14$ ו-$\frac98>1$."),
     NU(r"מהי $F_X(1)$?", Fr(7, 8), r"$1-\frac{(2-1)^2}8=\frac78$.")])

ADD(4, "ד",
    RB((r"הגדרת מותנית: מנה של הפרשי $F$", 1), (r"המכנה $F(1)-F(-1)=\frac78-\frac18=\frac34$", 2), (r"המונה $F(1)-F(\frac14)=\frac7{8}-\frac{79}{128}=\frac{33}{128}$", 2), (r"התשובה $\frac{11}{32}$", 1)),
    [r"לחלק ב-$P(X<1)$ במקום ב-$P(|X|<1)$", r"להשתמש בנוסחת $F$ של הצד השמאלי ב-$t=\frac14$"],
    [NU(r"מהי $P(|X|<1)=F(1)-F(-1)$? (המכנה)", Fr(3, 4), r"$\frac78-\frac18=\frac34$."),
     NU(r"מהי $P(\frac14<X<1)=F(1)-F(\frac14)$? (המונה)", Fr(33, 128), r"$F(\frac14)=1-\frac{(7/4)^2}8=\frac{79}{128}$, ו-$\frac78-\frac{79}{128}=\frac{33}{128}$."),
     NU(r"מהי ההסתברות המותנית?", Fr(11, 32), r"$\frac{33/128}{3/4}=\frac{11}{32}$.")])

# ---- Q5 (thinning of a Poisson number of candidates)
Q5M = [r"בינומית $\mathrm{Bin}(N,p)$ עם $p=\frac1{365}$: כל מועמד הוא ניסוי ברנולי בלתי תלוי", r"היפר-גאומטרית: הוצאה בלי החזרה", r"פואסון: מספר מאורעות בזמן"]
ADD(5, "א",
    RB((r"כל מועמד נולד ב-01.04 בהסתברות $p=\frac1{365}$, בלתי תלוי באחרים", 4), (r"משפט הפירוק: $W\sim\mathrm{Bin}(N,p)$", 3), (r"$P(W=k)=\binom Nkp^k(1-p)^{N-k}$", 3)),
    [r"להשתמש בהיפר-גאומטרית או בפואסון כשמספר המועמדים ידוע", r"לכתוב $p=365$"],
    [CH(r"נתון ש-$N$ מועמדים בדיוק מילאו טופס. איזה מודל מתאר את מספר הנולדים ב-01.04?", Q5M, 0,
        r"מספר המועמדים קבוע וידוע וכל אחד ב״ת בהסתברות $\frac1{365}$: בינומית. פואסון מתאר מספר מקרים בלי $N$ קבוע, וההיפר-גאומטרית דורשת הוצאה בלי החזרה."),
     NU(r"מהי הסתברות ההצלחה $p$ של מועמד בודד?", Fr(1, 365), r"$\frac1{365}\approx0.00274$."),
     NU(r"בדוגמה $N=6$, $p=\frac14$ (במקום $\frac1{365}$): מהי $P(W=2)$?", Fr(1215, 4096), r"$\binom62\cdot\frac1{16}\cdot\left(\frac34\right)^4=15\cdot\frac{81}{4096}=\frac{1215}{4096}\approx0.2966$.")])

ADD(5, "ב",
    RB((r"הסתברות שלמה לפי $X\sim P(\lambda)$, כאשר $Y\mid X=j\sim\mathrm{Bin}(j,p)$", 3), (r"שימוש בנוסחת ההערה עם $a=\lambda(1-p)$", 4), (r"פישוט: $Y\sim P(\lambda p)$", 3)),
    [r"להתייחס ל-$N$ כקבוע ולכתוב בינומית", r"לכתוב $Y\sim P(\lambda)$ ולשכוח את הדילול ב-$p$"],
    [CH(r"ב-$\lambda=4$, $p=\frac14$: מהי $P(Y=2)$ בין המועמדים שמילאו טופס?",
        [r"$Y\sim P(\lambda p)$ (דילול של פואסון): $\frac{e^{-1}}{2}\approx0.1839$", r"$Y\sim\mathrm{Bin}(4,\frac14)$: $\approx0.2109$", r"$Y\sim P(\lambda)$: $\approx0.1465$"], 0,
        r"מספר המועמדים אקראי (פואסון), ולכן ממצעים על $X$ והתוצאה היא פואסון עם ממוצע $\lambda p$. הבינומית מניחה $N$ קבוע, ופואסון עם $\lambda$ מתעלם מהדילול."),
     NU(r"מהו הפרמטר $\lambda p$ ב-$\lambda=4$, $p=\frac14$?", 1, r"$4\cdot\frac14=1$."),
     NU(r"מהי $P(Y=2)$ ב-$P(1)$? ($\frac{e^{-1}1^2}{2!}$)", Fr(_m.exp(-1) / 2), r"$\frac{e^{-1}}2\approx0.18394$.")])

ADD(5, "ג",
    RB((r"נוסחת בייס: $\frac{P(Y=k\mid X=n)P(X=n)}{P(Y=k)}$", 2), (r"הצבת הבינומית והפואסונים וצמצום", 2), (r"התוצאה: $n-k\sim P(\lambda(1-p))$", 1)),
    [r"לבלבל בין $P(Y=k/X=n)$ לבין $P(X=n/Y=k)$", r"לשכוח את ההיסט $n-k$"],
    [CH(r"ב-$\lambda=4$, $p=\frac14$, $k=2$: מהי $P(X=4\mid Y=2)$?",
        [r"$n-k\sim P(\lambda(1-p))=P(3)$ ולכן $\frac{e^{-3}3^2}{2!}\approx0.2240$", r"$X\sim P(4)$ ללא תנאי: $\approx0.1954$", r"$\mathrm{Bin}(4,\frac34)$ בנקודה $2$: $\approx0.2109$"], 0,
        r"אחרי תנאי על $Y=k$ ה-$k$ הנולדים כבר נספרו, והנותרים (שלא נולדו) הם פואסון עם ממוצע $\lambda(1-p)$. התנאי משנה את ההתפלגות ולכן $0.1954$ שגוי."),
     NU(r"מהו הממוצע $\lambda(1-p)$ ב-$\lambda=4$, $p=\frac14$?", 3, r"$4\cdot\frac34=3$."),
     NU(r"מהי $P(X=4\mid Y=2)$? (כלומר $P(n-k=2)$ עבור $P(3)$)", Fr(9 * _m.exp(-3) / 2), r"$\frac{e^{-3}\cdot9}{2}\approx0.22404$.")])

# ---- Q6 (bridge Q1; Q2 = A || (E-B) || (C-D); p=0.6)
Q6M = [r"מתנים ב-$E$ (היחידה האמצעית): אם היא פועלת מקבלים מקבילי-טורי, ואם לא מקבלים שני ענפים נפרדים",
       r"טור-מקביל פשוט, בלי התניה, כי כל הרכיבים בלתי תלויים", r"מתעלמים מ-$E$ כי היא בלתי תלויה"]
ADD(6, "א",
    RB((r"זיהוי הגשר: $E$ אינה בטור ואינה במקביל, ולכן מתנים ב-$E$", 3), (r"$E$ פועלת: $P=(2p-p^2)^2$; $E$ אינה פועלת: $P=2p^2-p^4$", 4), (r"הסתברות שלמה: $p(2p-p^2)^2+(1-p)(2p^2-p^4)$", 2)),
    [r"להתייחס ל-$E$ כאילו אינה משפיעה", r"לשכוח את הגורם $p$ של $E$ בהסתברות השלמה"],
    [CH(r"איך מחשבים את $P(Q_1)$ במעגל הגשר?", Q6M, 0,
        r"ב-$p=0.6$ ההתניה נותנת $0.6595$; בלי $E$ אין מבנה טורי-מקבילי כי הענפים מחוברים דרך $E$."),
     NU(r"ב-$p=0.6$: אם $E$ פועלת, מהי ההסתברות שהמעגל פועל?", Fr("0.7056"), r"$E$ פועלת ממזגת את שני הצמתים האמצעיים: $(A\cup C)\cap(B\cup D)$, ולכן $(2p-p^2)^2=0.84^2=0.7056$."),
     NU(r"ב-$p=0.6$: אם $E$ אינה פועלת, מהי ההסתברות שהמעגל פועל? ($(A\cap B)\cup(C\cap D)$)", Fr("0.5904"), r"$2p^2-p^4=0.72-0.1296=0.5904$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_1)$?", Fr("0.65952"), r"$0.6\cdot0.7056+0.4\cdot0.5904=0.65952$.")])

ADD(6, "ב",
    RB((r"זיהוי מבנה $Q_2$: $A$ במקביל לשני ענפים, $(E\cap B)$ ו-$(C\cap D)$", 3), (r"התניה ב-$A$: אם $A$ פועל המעגל פועל ($P=1$)", 2), (r"אם $A$ אינו פועל: $P\bigl((E\cap B)\cup(C\cap D)\bigr)=2p^2-p^4$", 2), (r"הסתברות שלמה: $p+(1-p)(2p^2-p^4)$", 2)),
    [r"לחבר בטור את $A$ עם שני הענפים במקום לחבר במקביל", r"לשכוח את החיתוך $p^4$ בהסתברות האיחוד"],
    [CH(r"איזה תיאור של $Q_2$ מתאים לאיור?",
        [r"$A$ במקביל לשני ענפים: ($E$ בטור $B$) ו-($C$ בטור $D$)", r"$A$ בטור עם שני הענפים ($E$ בטור $B$) ו-($C$ בטור $D$)", r"גשר כמו $Q_1$"], 0,
        r"$A$ מקצר ישירות בין שני הקצוות. ב-$p=0.6$: התיאור הנכון נותן $0.8362$; $A$ בטור נותן $0.3542$, וגשר $0.6595$."),
     NU(r"ב-$p=0.6$: אם $A$ אינו פועל, מהי ההסתברות ש-$Q_2$ פועל? ($(E\cap B)\cup(C\cap D)$)", Fr("0.5904"), r"$2p^2-p^4=0.5904$."),
     NU(r"ב-$p=0.6$, מהי $P(Q_2)$?", Fr("0.83616"), r"$0.6+0.4\cdot0.5904=0.83616$.")])

ADD(6, "ג",
    RB((r"הגדרת מותנית: $\frac{P(Q_1\cap Q_2)}{P(Q_1)}$", 2), (r"הוכחה ש-$Q_1\subseteq Q_2$: כל מסלול של $Q_1$ מכיל מסלול של $Q_2$", 3), (r"מכאן $P(Q_1\cap Q_2)=P(Q_1)$ והתשובה $1$", 2)),
    [r"להתעלם מהיחידות המשותפות ולכתוב $P(Q_2)$ כתשובה", r"לחשב $P(Q_1\cap Q_2)$ כמכפלה"],
    [CH(r"מהי $P(Q_2/Q_1)$?",
        [r"$1$: כל מסלול של $Q_1$ ($AB$, $CD$, $AED$, $CEB$) מכיל מסלול של $Q_2$, ולכן $Q_1\subseteq Q_2$", r"$P(Q_2)$, כי המעגלים בלתי תלויים", r"$P(Q_1)$"], 0,
        r"המסלולים של $Q_1$ הם $AB,CD,AED,CEB$ ולכל אחד מהם יש תת-מסלול ב-$Q_2$: $A$, $CD$, $A$, $EB$. ב-$p=0.6$ האפשרויות האחרות נותנות $0.8362$ ו-$0.6595$."),
     NU(r"ב-$p=0.6$: מהי $P(Q_1)$? (התנאי)", Fr("0.65952"), r"מסעיף א."),
     NU(r"באותו $p$: מהי $P(Q_1\cap Q_2)$? ($Q_1\subseteq Q_2$)", Fr("0.65952"), r"החיתוך שווה ל-$Q_1$."),
     NU(r"מהי $P(Q_2/Q_1)$?", 1, r"$\frac{P(Q_1)}{P(Q_1)}=1$.")])

for _q in questions:
    _s = S.get((_q["num"], _q.get("part")))
    if _s and not _q.get("hold"):
        _q["rubric"], _q["pitfalls"], _q["steps"] = _s
        _q["rubricSource"] = "ai-draft"
        _q["stepsSource"] = "ai-draft"


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} items")
