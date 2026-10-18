# דף נוסחאות מרוכז

> 🔑 הדף עוקב אחרי סדר הנוסחון הרשמי (הרצאות 1 עד 8). **שורות המסומנות ב-$\star$ אינן בנוסחון**: אלה התוספות של מצב הלימוד, בעיקר שני המתכונים שהנוסחון חסר (שיטת השטח וצפיפות עם קבועים). אל תניחו שמותר להכניס את הדף הזה למבחן: מותר רק הנוסחון ו"ערכת המבחן".

## הרצאה 1: מאורעות

| מה | נוסחה |
|---|---|
| הסתברות קלאסית | $P(A)=\frac{\lvert A\rvert}{\lvert\Omega\rvert}$ (תוצאות שוות הסתברות) |
| משלים, איחוד | $P(\overline A)=1-P(A)$; $P(A\cup B)=P(A)+P(B)-P(A\cap B)$ |
| דה מורגן | $\overline{A\cap B}=\overline A\cup\overline B$; $\overline{A\cup B}=\overline A\cap\overline B$ |
| זרים | $A\cap B=\varnothing$; $P(\cup A_i)=\sum P(A_i)$ לזרים בזוגות |
| $\star$ הפרש, שלושה מאורעות | $P(A\setminus B)=P(A)-P(A\cap B)$; $P(A\cup B\cup C)=\sum P-\sum P(\cap_2)+P(A\cap B\cap C)$ |
| $\star$ ארבעה תאים | $A\cap B$, $A\cap\overline B$, $\overline A\cap B$, $\overline A\cap\overline B$ סכומם 1: שלושה נתונים קובעים הכול |
| $\star$ ספירת מכפלות של $k$ בין $a$ ל-$b$ | $\lfloor b/k\rfloor-\lfloor(a-1)/k\rfloor$ |

## הרצאה 2: מותנית ואי-תלות

| מה | נוסחה |
|---|---|
| מותנית | $P(A/B)=\frac{P(A\cap B)}{P(B)}$ |
| כלל הכפל והשרשרת | $P(A\cap B)=P(A)P(B/A)$; $P(\cap A_i)=P(A_1)P(A_2/A_1)\cdots$ |
| הסתברות שלמה | $P(B)=\sum_iP(B/A_i)P(A_i)$ |
| בייס | $P(A_i/B)=\frac{P(B/A_i)P(A_i)}{\sum_jP(B/A_j)P(A_j)}$ |
| אי-תלות | $P(A\cap B)=P(A)P(B)$ |
| $\star$ "אם ידוע" | המכנה הוא $P(B)$ של הנתון $B$, לא $\lvert\Omega\rvert$ |
| $\star$ בלתי תלויים / זרים | $P(A\cap B)=P(A)P(B)$ / $P(A\cap B)=0$ (שניים חיוביים: לא שניהם) |

## הרצאה 3: קומבינטוריקה

| | בלי החזרה | עם החזרה |
|---|---|---|
| **מסודרת** | $\frac{n!}{(n-k)!}$ | $n^k$ |
| **לא מסודרת** | $\binom nk$ | $\binom{n+k-1}k$ |

$n!=\Gamma(n+1)$; סידורים בשורה $n!$, במעגל $(n-1)!$; מולטינומי $\frac{n!}{n_1!\cdots n_k!}$; בינום $\sum\binom nja^jb^{n-j}=(a+b)^n$.
$\star$ **סכום קוביות הם לא שווי הסתברות; סופרים זוגות מסודרים. "אי פעם נגיע ל-$N$": $\frac1N\left(1+\frac1N\right)^{N-1}$.**

## הרצאה 4: משתנה בדיד

| מה | נוסחה |
|---|---|
| תוחלת | $E[X]=\sum xP(x)$; $E[g(X)]=\sum g(x)P(x)$ |
| שונות | $\mathrm{Var}=E[X^2]-(E[X])^2$; $\mathrm{Var}[aX+b]=a^2\mathrm{Var}[X]$ |
| סכום | $E[X+Y]=E[X]+E[Y]$ תמיד; $\mathrm{Var}[X+Y]=\mathrm{Var}+\mathrm{Var}$ לבלתי תלויים |
| מצטברת | $F(t)=\sum_{x\le t}P(x)$; $P(x_1<X\le x_2)=F(x_2)-F(x_1)$ |
| $\star$ מוטה-גודל | בחירה לפי אנשים: $E[Y]=\frac{E[X^2]}{E[X]}\ge E[X]$ |

## הרצאה 5: התפלגויות בדידות

| התפלגות | $P(X=k)$ | $E$ | $\mathrm{Var}$ |
|---|---|---|---|
| $U_d(a,b)$ | $\frac1{b-a+1}$ | $\frac{a+b}2$ | $\frac{(b-a+1)^2-1}{12}$ |
| $\mathrm{Ber}(p)$ | $p$ ל-1 | $p$ | $p(1-p)$ |
| $\mathrm{Bin}(n,p)$ | $\binom nkp^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| $G(p)$ | $p(1-p)^{k-1}$ | $\frac1p$ | $\frac{1-p}{p^2}$ |
| $\mathrm{NegBin}(m,p)$ | $\binom{k-1}{m-1}p^m(1-p)^{k-m}$ | $\frac mp$ | $\frac{m(1-p)}{p^2}$ |
| $\mathrm{Hyp}(N,D,n)$ | $\frac{\binom Dk\binom{N-D}{n-k}}{\binom Nn}$ | $n\frac DN$ | $n\frac DN\left(1-\frac DN\right)\frac{N-n}{N-1}$ |
| $P(\lambda)$ | $\frac{\lambda^k}{k!}e^{-\lambda}$ | $\lambda$ | $\lambda$ |

- משפט הפירוק: סכום $n$ ברנולי בלתי תלויים $=\mathrm{Bin}(n,p)$. חוסר זיכרון (גאומטרית): $P(X>k+n/X>k)=P(X>n)$.
- זוגיות: $P(X\ \mathrm{even})=\frac12E[1+(-1)^X]$.
- $\star$ **דילול:** $\mathrm{Bin}(N,p)$ ואז כל אחד מקיים בהסתברות $Q$ נותן $\mathrm{Bin}(N,pQ)$; $P(\lambda)$ מדולל ב-$p$ נותן $P(\lambda p)$. אחרי דילול פואסוני, ההפרש $X-Y$ הוא $P(\lambda(1-p))$.
- $\star$ **זוגיות לגאומטרית:** $P(X\ \mathrm{even})=\frac{1-p}{2-p}$.
- $\star$ **כד:** הסתברות שהכדור ה-$k$ אדום היא $\frac DN$ (בלי החזרה, בלי מידע).

## הרצאה 6: משתנה דו-ממדי

| מה | נוסחה |
|---|---|
| שוליים | $P_X(x)=\sum_yP_{XY}(x,y)$ |
| אי-תלות | $P_{XY}=P_XP_Y$ **בכל** תא |
| אי-מתאם | $E[XY]=E[X]E[Y]$; בלתי תלויים $\Rightarrow$ בלתי מתואמים (לא להפך) |
| שונות משותפת | $\mathrm{Cov}=E[XY]-E[X]E[Y]$ |
| מתאם | $\rho=\frac{\mathrm{Cov}}{\sqrt{\mathrm{Var}X\mathrm{Var}Y}}\in[-1,1]$; $Y=aX+b\Rightarrow\rho=\pm1$ |
| סכום | $\mathrm{Var}[X+Y]=\mathrm{Var}X+\mathrm{Var}Y+2\mathrm{Cov}$ |
| $\star$ תלות | תא אחד שבו הטבלה $\ne$ מכפלת השוליים (בדרך כלל אפס) |
| $\star$ מינימום ומקסימום | ללא החזרה: $\frac{\binom{\ell-k-1}{n-2}}{\binom Nn}$; שתי הטלות: $\frac2{N^2}$ ל-$k<\ell$ |

## הרצאה 7: משתנה רציף

| מה | נוסחה |
|---|---|
| הסתברות | $P(a<X<b)=\int_a^bf$; $\int f=1$, $f\ge0$ |
| מצטברת | $F(t)=\int_{-\infty}^tf$; $f=F'$ |
| תוחלת, שונות | $E=\int xf$; $\mathrm{Var}=\int x^2f-(E)^2$ |
| $U_c(a,b)$ | $f=\frac1{b-a}$; $E=\frac{a+b}2$; $\mathrm{Var}=\frac{(b-a)^2}{12}$ |
| $\mathrm{Exp}(\lambda)$ | $f=\lambda e^{-\lambda y}$; $F=1-e^{-\lambda t}$; $E=\frac1\lambda$; $\mathrm{Var}=\frac1{\lambda^2}$ |
| $\mathrm{Erlang}(m,\lambda)$ | $E=\frac m\lambda$; $\mathrm{Var}=\frac m{\lambda^2}$ |
| $N(\mu,\sigma^2)$ | $F(t)=\Phi\left(\frac{t-\mu}\sigma\right)$; $\Phi(d)=\frac12+NA(0,d)$ (נדיר בשנים האחרונות) |
| אינטגרלים | $\int_0^\infty t^ne^{-t}dt=n!$; $\int_0^1t^{-p}dt$ מתבדר ל-$p\ge1$ |

## הרצאה 8: דה מואבר-לפלס ומשפט הגבול המרכזי (נדיר)

$X_B\sim\mathrm{Bin}(n,p)\approx N(np,np(1-p))$ עם תיקון $\pm\frac12$. $\sum X_k\approx N(n\mu,n\sigma^2)$; $\overline X\approx N(\mu,\frac{\sigma^2}n)$.

## סכומים וטורים

$\sum_{j=1}^nj=\frac{n(n+1)}2$, $\sum j^2=\frac{n(n+1)(2n+1)}6$, $\sum j^3=\frac{n^2(n+1)^2}4$. הנדסי סופי $\sum_{j_1}^{j_2}q^j=\frac{q^{j_1}(1-q^{j_2-j_1+1})}{1-q}$; אינסופי $\sum_{j\ge j_1}q^j=\frac{q^{j_1}}{1-q}$ ($\lvert q\rvert<1$). $e^x=\sum\frac{x^k}{k!}$. $\star$ $\sum_{n\ge k}\frac{x^n}{(n-k)!}=x^ke^x$ (**שימו לב להזזה**).

---

## $\star$ מתכון 1: שיטת השטח (ראו [[area_method]])

1. $X\sim U(0,a)$, $Y\sim U(0,b)$ בלתי תלויים $\Rightarrow$ אחיד על מלבן, $\lvert\Omega\rvert=ab$.
2. מציירים, מתרגמים לאי-שוויון, בוחרים צד בנקודת מבחן.
3. $P=\frac{S(A)}{\lvert\Omega\rvert}$ ($S$ שטח); מותנה $\frac{S(A\cap B)}{S(B)}$.
4. סכום: קו יורד; $\lvert x-y\rvert<c$: רצועה; $xy<c$: היפרבולה ($\int\frac{dx}x=\ln x$); $\min<t$: משלים של "שניהם $\ge t$"; $\max<t$: ריבוע בפינה.
5. $F_Z(t)$: אזור כפונקציה של $t$; מקרים לפי מקום הגבול; בדיקת רציפות.

| ריבוע היחידה | $F(t)$ |
|---|---|
| $\max$ | $t^2$ |
| $\min$ | $2t-t^2$ |
| $\lvert X-Y\rvert$ | $2t-t^2$ |
| $X/Y$ | $\frac t2$ ($t\le1$), $1-\frac1{2t}$ ($t>1$) |
| $XY$ | $t-t\ln t$ |
| $\min/\max$ | $t$ ($U_c(0,1)$) |

## $\star$ מתכון 2: צפיפות עם קבועים (ראו [[pdf_constants]])

1. נרמול $\int f=1$. 2. אינטגרל מתבדר $\Rightarrow$ קבוע $=0$. 3. תוחלת נתונה $\Rightarrow$ משוואה שנייה. 4. פותרים. 5. $f\ge0$ (קצוות של קטעים ליניאריים) $\Rightarrow$ תחום הפרמטר. 6. $F$ לפי קטעים, כל קטע מוסיף למה שנצבר, רציפה. 7. $P(a<X<b)=F(b)-F(a)$; $P(X>a/X<b)=\frac{F(b)-F(a)}{F(b)}$.

## $\star$ מעגלים (ראו [[circuits]])

טור $\prod p_i$; מקביל $1-\prod(1-p_i)$; גשר: התניה על האמצעי: $p(2p-p^2)^2+(1-p)(2p^2-p^4)$. $P(Q_1/Q_2)=\frac{P(Q_1\cap Q_2)}{P(Q_2)}$ (המכנה הוא מה שידוע).

## $\star$ אחידים בקצרה

$U_c(0,L)$: $E=\frac L2$, $E[X^2]=\frac{L^2}3$, $\mathrm{Var}=\frac{L^2}{12}$. בלתי תלויים: $E[XY]=E[X]E[Y]$, $E[X^2Y^2]=E[X^2]E[Y^2]$. שבירת מקל: $\eta=\frac{\min}{L}\sim U_c(0,\frac12)$.

## $\star$ מלכודות בקצרה (ראו [[traps]])

$\lvert\Omega\rvert\ne1$ | מכנה מותנה | עם/בלי החזרה | מסודר/לא מסודר | זרים $\ne$ בלתי תלויים $\ne$ בלתי מתואמים | מוטה-גודל | הזזת אינדקס | $F$ צובר
