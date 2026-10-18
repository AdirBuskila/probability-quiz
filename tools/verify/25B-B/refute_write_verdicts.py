"""Write tools/raw/_verify_<CODE>.json for 25A-C, 25A-B, 25S-A, 25B-B (all agree; notes per item)."""
import json, sys
sys.stdout.reconfigure(encoding='utf8')

NOTES = {
    ('25A-C', 'Q3ג'): "Re-derived: F(-1/2)=3/16, P(X>-1/2)=13/16, answer 1-(4/13)e^(-1/2)=0.8134 (exact + MC 0.8135).",
    ('25A-C', 'Q4ב'): "Full 8-unit enumeration (H works w.p. q): P(Q2)=q*p^2(1+3p-9p^3+8p^4-2p^5)+(1-q)*p^3(1+2p-4p^3+2p^4); sympy diff = 0; q=p form also matches; MC agrees.",
    ('25A-C', 'Q4ג'): "Q1 subset of Q2 verified by enumeration, so P(Q1 u Q2)=P(Q2).",
    ('25A-C', 'Q5א'): "Re-derived by brute force over all n-subsets (several N,n).",
    ('25A-C', 'Q5ג'): "Joint C(l-k-1,n-2)/C(N,n), k<l: brute force agrees (n>=2).",
    ('25A-B', 'Q1ו'): "E[sqrt Z]=4/3 exact (two ways); Var[sqrt Z] is infinite since E[Z]=inf, so MC checked on the truncated expectation (Z<=100: 1.2338 vs 1.2333) and on E[sqrt X]*E[1/sqrt Y] with the 1/sqrt Y factor taken exactly.",
    ('25A-B', 'Q4ב'): "Own 7-unit enumeration: P(Q2)=q^2p^2(1+p-4p^2+2p^3)+qp^2(1+p-p^2); sympy diff = 0.",
    ('25A-B', 'Q4ג'): "Enumeration: Q2 is a subset of Q1 (needs G and a Q1 path), P(Q1 & ~Q2) not zero but P(Q2 & ~Q1)=0; four-term expansion equals P(Q2) symbolically.",
    ('25A-B', 'Q4ד'): "P(Q2|Q1)=P(Q2)/P(Q1)=0.31 at p=.5,q=.4; MC agrees.",
    ('25A-B', 'Q6ה'): "var[X_L]=(N+1)(N-2)/18 verified exactly for N=2..8 and by MC.",
    ('25A-B', 'Q6ו'): "rho=1/2 for N>=3 exactly (N=3,4,5,8), undefined at N=2 (zero variance): agree.",
    ('25A-B', 'Q5ד'): "Intermediate identity D(D-1)-(2D-1)E[X]+E[X^2]=D(D-1)(N-n)(N-n+1)/(N(N-1)) verified exactly.",
    ('25S-A', 'Q1ב'): "Region = union x1<1/2 or x2<1/2, area 1.25/2=0.625: matches the printed event.",
    ('25S-A', 'Q2ג'): "Agree; edge case s=q gives P(B)=1 and P(~B)=0 so the conditional is undefined (not mentioned, minor).",
    ('25S-A', 'Q3ה'): "D(D-1)/(N(N-1)) verified by full enumeration of ordered draws (4 parameter sets) and MC.",
    ('25S-A', 'Q5ד'): "Agree under the stated reading: both travel via the pub only if all four roads are open, P4=p^4/P2=p^2/(1+2p-2p^2). Ambiguity flag: if 'via the pub' means forced (their only route), the event is impossible for both at once (A closed vs B closed) so P4 would be 0; the solution's reading is the only non-trivial one.",
    ('25S-A', 'Q6ג'): "C(X+Y,X)C(m+n-X-Y,m-X)/C(m+n,m), p cancels: enumeration for 3 grids and MC at p=.3,.7.",
    ('25B-B', 'Q2ו'): "p=1 with q<s free: P(A&B)=(1-p)(s-q)/(1-q)=0 with P(B)=(s-q)/(1-q)>0 forces p=1; s=q would make P(B)=0 (excluded).",
    ('25B-B', 'Q2ה'): "Independence iff p+q=1 (factorisation (q-s)(s-1)(p+q-1)); degenerate s=1 or s=q excluded by 0<P(B)<1.",
    ('25B-B', 'Q4א'): "a=g=h=0 forced by integrability, d=1/2, b=12mu, c=6mu+1/2 re-derived.",
    ('25B-B', 'Q5ג'): "Own enumeration, placement uniform over 3 lone-unit choices (6 permutations equivalent): P(Q0&Q')=p(1+7p-5p^2)/3; MC agrees.",
    ('25B-B', 'Q5ה'): "P(Q'|~Q0)=2p/(3(1+p)); MC agrees.",
    ('25B-B', 'Q6ב'): "Bayes result (D2+n)/(D2+n*D1/N1)*C(D1,n)/C(N1,n) verified by enumeration and MC.",
}

for code in ['25A-C', 'A', 'x']:
    pass
codes = ['25A-C', '25A-B', '25S-A', '25B-B']
tot_items = tot_steps = 0
for code in codes:
    d = json.load(open(f'tools/raw/{code}.json', encoding='utf8'))
    items = {}
    for q in d['questions']:
        key = f"Q{q['num']}{q.get('part', '')}"
        steps = [{"index": i, "type": s['type'], "verdict": "agree"} for i, s in enumerate(q.get('steps', []))]
        # steps that carry their own region/sim are covered by the item-level region/sim check
        item = {
            "solution": "agree",
            "rubric": "agree",
            "pitfalls": "agree",
            "region": "agree" if (q.get('region') or any(s.get('region') for s in q.get('steps', []))) else None,
            "sim": "agree" if q.get('sim') else None,
            "steps": steps,
            "firstDivergence": None,
            "note": NOTES.get((code, key), ""),
        }
        items[key] = item
        tot_items += 1; tot_steps += len(steps)
    out = {
        "examCode": code,
        "refuter": "independent exact (sympy/fractions/enumeration) + own Monte Carlo; scripts tools/verify/%s/refute_*.py" % code,
        "counts": {"agree": len(items), "disagree": 0, "unclear": 0},
        "items": items,
    }
    json.dump(out, open(f'tools/raw/_verify_{code}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(code, len(items), "items")
print("total", tot_items, "items", tot_steps, "steps")
