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

## Resolved

### 26A-B Q3 a, b, d - official key uses different q2/q4 labels than the printed question
- Path: official PDF of sitting 26A-B (typed solutions), see sitting code only
- Page: exam p.2 (Q3 definitions of q1..q4); solution pp.8-9 (printed 5-6; same text in the Arabic/other-language copies)
- Question: the printed exam defines q2 = P(B | not-A and not-C) and q4 = P(B | not-A and C). The official solution defines q2 = P(B | not-A and C) and q4 = P(B | not-A and not-C) (q1 and q3 agree). The official answers to Q3a (P(B)), Q3b (independence condition and P(A|B), denominator) and Q3d (P(Q2) = 1-(1-q4)(1-p)^2) are correct only under the solution's labelling. Under the printed labelling they differ (check.py at p=0.3, q=(0.9,0.7,0.5,0.3): P(B) official 0.480 vs true 0.592; P(A|B) 0.3875 vs 0.3142; P(Q2) 0.657 vs 0.853; confirmed by exact enumeration and by Monte Carlo). Q3c (P(Q1)=q1 p^2) is unaffected and is shipped. Exact + MC checks of the official formulas under the solution's labelling all pass.
- Needed: which labelling is intended? (a) printed labelling is a typo and the solution's is right: ship the official answers as they are, with the question text changed to the solution's definitions; or (b) printed labelling stands: the official answers for a, b, d must be replaced (ship them with the corrected formulas, marked official:false).
- Status: resolved 2026-10-18 by the arbiter under the standing rulings (the printed question wins; final-answer error -> typo ruling). Re-read from the rendered pages: the swap is real and changes the final answers of a, b and d. Shipped option (b): official method with q2/q4 swapped back to the printed definitions, solutionSource solved, official:false, prefix "הפתרון הרשמי עם תיקון". Corrected: P(B) = q1p^2 + (q3+q4)p(1-p) + q2(1-p)^2; independence iff pq1+(1-p)q3 = pq4+(1-p)q2; P(A|B) = (q1p^2+q3p(1-p))/P(B); P(Q2) = 1-(1-q2)(1-p)^2 (at p=0.3: 0.592, 0.3142, 0.853). check.py asserts them exactly and by Monte Carlo at three parameter sets. Adir can override (choose option a).
