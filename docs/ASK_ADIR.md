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

### 26A-B Q3 a, b, d - official key uses different q2/q4 labels than the printed question
- Path: official PDF of sitting 26A-B (typed solutions), see sitting code only
- Page: exam p.2 (Q3 definitions of q1..q4); solution pp.8-9 (printed 5-6; same text in the Arabic/other-language copies)
- Question: the printed exam defines q2 = P(B | not-A and not-C) and q4 = P(B | not-A and C). The official solution defines q2 = P(B | not-A and C) and q4 = P(B | not-A and not-C) (q1 and q3 agree). The official answers to Q3a (P(B)), Q3b (independence condition and P(A|B), denominator) and Q3d (P(Q2) = 1-(1-q4)(1-p)^2) are correct only under the solution's labelling. Under the printed labelling they differ (check.py at p=0.3, q=(0.9,0.7,0.5,0.3): P(B) official 0.480 vs true 0.592; P(A|B) 0.3875 vs 0.3142; P(Q2) 0.657 vs 0.853; confirmed by exact enumeration and by Monte Carlo). Q3c (P(Q1)=q1 p^2) is unaffected and is shipped. Exact + MC checks of the official formulas under the solution's labelling all pass.
- Needed: which labelling is intended? (a) printed labelling is a typo and the solution's is right: ship the official answers as they are, with the question text changed to the solution's definitions; or (b) printed labelling stands: the official answers for a, b, d must be replaced (ship them with the corrected formulas, marked official:false).
- Status: hold (Q3a, Q3b, Q3d held, in the raw JSON with the official solution text transcribed; not in the bank)

## Resolved
