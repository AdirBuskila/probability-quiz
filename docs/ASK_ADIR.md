# ASK_ADIR - probability

Open questions for Adir. One entry per item; the orchestrator moves it to Resolved when answered.

## Open

<!-- Entry format:
### <exam code> Q<number> - <short title>
- Path: <absolute file path>
- Page: <page number>
- Question: <what is unclear or missing>
- Needed: <what Adir must provide or decide>
- Status: hold
-->

### 24B-B Q3 d - official answer 5/9 disagrees with the exact value 1/2
- Path: official PDF of sitting 24B-B, see sitting code only
- Page: solution p.9 (printed Q3 d: P(number even | digit sum odd))
- Question: the official solution gives 20/36 = 5/9. Two distinct digits from 1..9 give 72 ordered pairs; "digit sum odd" has 40 of them (5 odd x 4 even, both orders), and the number is even exactly when the units digit is even: 20 of the 40. So the exact value is 20/40 = 1/2 (exact enumeration and 2*10^6-trial Monte Carlo 0.5002 in tools/verify/24B-B/check.py). The official denominator 36 does not match any reading of the printed condition.
- Needed: ship the corrected 1/2 (official:false, solved) or keep the printed 5/9?
- Status: hold (Q3d held, in the raw JSON with the official text; not in the bank)

### 24A-E Q3 bonus (ה) - no official solution for cov[D,T]
- Path: official PDF of sitting 24A-E (handwritten solutions)
- Page: exam p.2 (Q3 bonus, 5 pts, optional); solutions end after Q3 ד on p.8
- Question: the bonus part asks cov[D,T] for D = sum of D_j, T = sum of T_j; the official solution has no answer for it.
- Needed: route to the solver (no-key); not a key dispute.
- Status: hold (no-key; question text transcribed, not in the bank)

### 24B-C Q6 a, b - official expansions contain arithmetic slips
- Path: official PDF of sitting 24B-C, see sitting code only
- Page: solution pp.10-11 (printed Q6 a and b, bridge circuit)
- Question: (a) the official first line P(Q) = p(2p-p^2)^2 + (1-p)(2p^2-p^4) is right and expands to p^2(2+2p-5p^2+2p^3), but the printed expanded answer is p^2(2+p-5p^2+2p^3). (b) P(Q|A) is printed p+2p^2-4p^3+p^4 while its own formula p+p(2p-p^2)-p^2(2p-p^2) expands to p+2p^2-3p^3+p^4, so the printed final P(A|Q) = (1+2p-4p^2+p^3)/(2+p-5p^2+2p^3) is wrong; the exact value is (1+2p-3p^2+p^3)/(2+2p-5p^2+2p^3) (at p=0.5: 0.6875 exact vs 0.75 printed; exact enumeration and Monte Carlo in tools/verify/24B-C/check.py). Part c (answer 1) is fine.
- Needed: ship the corrected expansions (official:false, solved) or keep the printed ones?
- Status: hold (Q6a and Q6b held, in the raw JSON with the official text; not in the bank)

### 24B-C Q1 b - printed text says "shorter" but defines Z = max(X,Y)
- Path: official PDF of sitting 24B-C
- Page: exam p.1 (Q1 b)
- Question: the printed words "the shorter matchstick" contradict the printed formula Z = max(X,Y); the official solution uses max (P(Z<L/3) = 1/9, P(Z<L/2 | X>L/4) = 1/6). Transcribed as printed; the key matches the formula, so not held.
- Needed: confirm that max is intended (with min the answers would be 5/9 and 2/3, as in 24B-A).
- Status: note only (items shipped)

### 24A-A Q2 d and Q3 d - bonus parts with no official solution
- Path: official PDF of sitting 24A-A (handwritten solutions), see sitting code only
- Page: exam p.2 (Q2 d: P_N for an N-sided die, 3 pts; Q3 d: mean number of A's in the first string given n in total, 3 pts; both "אין חובה לפתור"); solutions p.6-9 stop after Q2 c and Q3 c
- Question: no official answer for either bonus part. Pattern for Q2 d is P_N = (1/N)(1+1/N)^(N-1) (exact for N=2..9 in tools/verify/24A-A/check.py); for Q3 d, E[X1 | X=n] = n N1/(N1+N2) from the hypergeometric of Q3 c.
- Needed: route to the solver (no-key); not a key dispute.
- Status: hold (no-key; question text transcribed, not in the bank)

### 25S-A Q3 e - bonus part, official solution explicitly withheld
- Path: official PDF of sitting 25S-A (handwritten solutions), see sitting code only
- Page: exam p.2 (Q3 e, bonus 5 pts: n balls drawn without replacement, probability that the last two are both red); solution p.9 ends Q3 d with the note that the bonus solution will not be published
- Question: no official answer. Solver value (pure symmetry): D(D-1)/(N(N-1)); confirmed by Monte Carlo (>= 10^6 trials) at four (N, D, n) in tools/verify/25S-A/check.py (printed as INFO, not compared with any key).
- Needed: route to the solver (no-key); not a key dispute.
- Status: hold (no-key; question text transcribed, not in the bank)

### 25A-C Q3 c - official 1-1/e disagrees with the exact value 1-(4/13)e^(-1/2)
- Path: official PDF of sitting 25A-C (handwritten solutions), see sitting code only
- Page: solution p.7 (Q3 c); exam p.2
- Question: with the official a=3/2, b=1/4 the cdf is F(t)=3/4 (1+t)^2 on [-1,0) and 1-(1/4)e^(-t) for t>=0. Then P(X<1/2 | X>-1/2) = (F(1/2)-F(-1/2))/(1-F(-1/2)) = (13/16 - e^(-1/2)/4)/(13/16) = 1-(4/13)e^(-1/2), about 0.813. The official answer is 1-1/e, about 0.63. Exact computation and Monte Carlo (2*10^6 trials) both give 0.813.
- Needed: confirm the official answer is a slip (then ship 1-(4/13)e^(-1/2), marked official:false) or tell us what was intended.
- Status: hold (Q3c held in the raw JSON with the official text transcribed; not in the bank)

### 25A-C Q4 b, c - printed H works with probability q, the official polynomial is the q=p case
- Path: official PDF of sitting 25A-C (handwritten solutions), see sitting code only
- Page: exam p.2 (Q4 text); solution pp.9-13 (Q4 b, c)
- Question: the exam says the added unit H works with probability q. The official solution uses P(H)=p and gets P(Q2)=p^3(2+4p-2p^2-13p^3+14p^4-4p^5) and the same polynomial for P(Q1 or Q2). Exact enumeration of the network shows these are correct only when q=p (at p=0.7, q=0.4 the official gives 0.703, the exact value is 0.624, Monte Carlo 0.623). The general answer is P(Q2)=q*P(Q2|H)+(1-q)*P(Q1); P(Q1 or Q2)=P(Q2) because Q1 implies Q2. Parts a and d (answer 1) do not depend on q and are shipped.
- Needed: either the printed q is a typo for p (ship the official answers unchanged), or q stands (ship the general-q formulas, marked official:false).
- Status: hold (Q4b, Q4c held, in the raw JSON with the official solution text transcribed; not in the bank)

### 25A-B Q6 e, f - bonus parts with no official solution
- Path: official PDF of sitting 25A-B (handwritten solutions), see sitting code only
- Page: exam p.3 (Q6 bonus 1 and 2); the solution file ends after Q6 d (p.23)
- Question: the variances var[X_L], var[X_R] (bonus 1) and the correlation rho[X_L,X_R] (bonus 2) have no worked solution.
- Needed: the solver route (no-key); nothing from Adir unless a key exists.
- Status: hold (no-key)

### 25B-B Q2 f - bonus (disjoint events): official key s = q is wrong or incomplete
- Path: official PDF of sitting 25B-B (handwritten solutions), see sitting code only
- Page: exam p.2 (Q2 d, printed as the bonus part "disjoint"); solution p.8 (last box)
- Question: given P(not-A | B) = p, P(A | not-B) = q, P(A or B) = s, the official answer for "A and B disjoint" is s = q (from P(A and B) = (1-p)(s-q)/(1-q) = 0). But s = q makes P(B) = (s-q)/(1-q) = 0 (B has probability zero). For a non-trivial B (P(B) > 0), disjoint events have P(not-A | B) = 1, so the true condition is p = 1, with s and q free (check.py Q2f: A,B disjoint with p=1, q=5/16, s=9/20, while s != q). The other factor (1-p) = 0 was missed.
- Needed: keep the official key (s = q) with the p = 1 caveat, or ship p = 1 (official:false, solved)? Not decided by the transcriber.
- Status: hold (key disagreement; question text transcribed, not in the bank)

## Resolved

### 26A-B Q3 a, b, d - official key uses different q2/q4 labels than the printed question
- Path: official PDF of sitting 26A-B (typed solutions), see sitting code only
- Page: exam p.2 (Q3 definitions of q1..q4); solution pp.8-9 (printed 5-6; same text in the Arabic/other-language copies)
- Question: the printed exam defines q2 = P(B | not-A and not-C) and q4 = P(B | not-A and C). The official solution defines q2 = P(B | not-A and C) and q4 = P(B | not-A and not-C) (q1 and q3 agree). The official answers to Q3a (P(B)), Q3b (independence condition and P(A|B), denominator) and Q3d (P(Q2) = 1-(1-q4)(1-p)^2) are correct only under the solution's labelling. Under the printed labelling they differ (check.py at p=0.3, q=(0.9,0.7,0.5,0.3): P(B) official 0.480 vs true 0.592; P(A|B) 0.3875 vs 0.3142; P(Q2) 0.657 vs 0.853; confirmed by exact enumeration and by Monte Carlo). Q3c (P(Q1)=q1 p^2) is unaffected and is shipped. Exact + MC checks of the official formulas under the solution's labelling all pass.
- Needed: which labelling is intended? (a) printed labelling is a typo and the solution's is right: ship the official answers as they are, with the question text changed to the solution's definitions; or (b) printed labelling stands: the official answers for a, b, d must be replaced (ship them with the corrected formulas, marked official:false).
- Status: resolved 2026-10-18 by the arbiter under the standing rulings (the printed question wins; final-answer error -> typo ruling). Re-read from the rendered pages: the swap is real and changes the final answers of a, b and d. Shipped option (b): official method with q2/q4 swapped back to the printed definitions, solutionSource solved, official:false, prefix "הפתרון הרשמי עם תיקון". Corrected: P(B) = q1p^2 + (q3+q4)p(1-p) + q2(1-p)^2; independence iff pq1+(1-p)q3 = pq4+(1-p)q2; P(A|B) = (q1p^2+q3p(1-p))/P(B); P(Q2) = 1-(1-q2)(1-p)^2 (at p=0.3: 0.592, 0.3142, 0.853). check.py asserts them exactly and by Monte Carlo at three parameter sets. Adir can override (choose option a).
