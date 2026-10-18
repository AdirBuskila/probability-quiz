import json, sys
sys.stdout.reconfigure(encoding='utf-8')
RAW = 'C:/Users/Adir/Desktop/Coding/Dev/probability-quiz/tools/raw/'

DERIVATION = {
    '25B-A': "Own derivations (written before opening the claims, scripts tools/verify/25B-A/refute_derive.py): Q1 X,Y iid U(0,1): P(L<1)=pi/4, P(S<1/4)=(1+ln2)/2, cond=pi/(2(1+ln2)) (quarter disc lies inside xy<1/2), E[S]=1/8, var[S]=7/576. Q2 P(B)=(q+s-1)/q, P(AB)=p(q+s-1)/q, P(A)=s-(1-p)P(B); q<1-s impossible; independent iff p+q=1 (s free). Q3 1-prod(1-p^Ni), cond p^N2/P. Q4 c=g=0 (finite variance), a=6(1-2mu)/5, b=(2+6mu)/5, mu in [-1/3,1/2], cond prob =1. Q5 P(Q0)=2p^2-p^3, both=(4p^2-p^3)/3, cond (4-p)/(3(2-p)), 2p^2/(3(1+p-p^2)). Q6 Bin(N,1/365), Poisson(lam/365), n-k~Poisson(lam*364/365). Each cross-checked by 4e6-sample Monte Carlo.",
    '25A-A': "Own derivations (tools/verify/25A-A/refute_derive.py): Q1 1/4, 1/4, 1/8 (sympy + MC). Q2 on 100..999: 1/2,1/4,28/225, all dependent, A8!=A2&A4. Q3 c=0, a=(2-3mu)/5, b=6(mu+1)/5, mu=1 impossible (a<0), F(t), cond=1. Q4 bridge p^2(2+2p-5p^2+2p^3), Q2 p^3(2-p)^2, P(Q1|Q2)=(3-2p)/(2-p)^2, complement (1-p)^2/(2-p)^2. Q5 P(N=k)=q^(k-1/2)(1-q), q=e^(-lam*pi/T), E=1/(e^x-e^-x), cond 1-q. Q6 Bin(n,q), Bin(n,pq), rho=sqrt(p(1-q)/(1-pq)), rho=1 at p=1.",
    '24S-A': "Own derivations (tools/verify/24S-A/refute_derive.py): Q1 pi/4, 3pi/16, 5/9. Q2 7^4/6^5, 1/9, 1/36, 1/6. Q3 joint by enumeration, marginals Bin(2,p), dependent. Q4 a=2/3,b=1/3, F, cond=(2e-1)/(3e-1)=0.6201. Q5 Bin(N,p), Bin(N,p/365), X-k|Y=k ~ Bin(N-k, p(1-r)/(1-pr)). Q6 enumeration over 2^6 states: p(1+2p-7p^3+7p^4-2p^5), P(B fails|works), 1, p^5/(...).",
    '24S-B': "Own derivations (tools/verify/24S-B/refute_derive.py): Q1 (1+ln2)/2, pi/16, (2/5)ln2, 1/4 and 7/144. Q2 1/6, 1, 1/5, 2/5. Q3 joint by enumeration, X~Bin(2,p), Y~Bin(3,p), dependent. Q4 a=b=e/4, F, P(X>-2|X<3)=(4e^2-e-1)/(4e^2-1)=0.9048 (sympy and MC 0.9046). Q5 (D+2pM)/(N+2M); posterior nonzero only for even n. Q6 parallel(series2,series2,bridge5) by enumeration, P0 and P1 at p=.6: 0.860539, 0.359424.",
}

# flags: (item key or None, kind, text)  -- verdict overrides: {(key,'solution'|'step i'): ('disagree', text)}
FLAGS = {
    '25B-A': [
        ('3ב', 'explain-typo', "step 2 explain says 0.64/0.964864 ~ 0.663317; correct is 0.663306 (the stored answer 0.66330592 is right)."),
        ('3ג', 'explain-typo', "step 1 explain says 1-0.663317=0.336683; correct is 0.336694 (stored answer right)."),
        ('2ה', 'gap', "solution proves only necessity (independent => p+q=1); sufficiency (p+q=1 => independent, s free) is not shown. Final answer p+q=1 is right (identity P(AB)-P(A)P(B) = -(s-1)(p+q-1)(q+s-1)/q^2)."),
        ('2ד', 'minor', "step 1 option d ('no: then P(A)>1') answers the question correctly but with a reason that is false in general; the intended key (a) is still the only option with a correct reason."),
        ('6א', 'assumption', "question text never states the 1/365 birthday probability; solution states it as an assumption (leap years ignored). 6ב/6ג solution reuse the symbol p for 1/365 without restating it."),
    ],
    '25A-A': [
        ('2א', 'ruling', "Omega = 100..999 (900 numbers) is the natural reading of 'a number of 3 digits' (a leading 0 does not make a 3-digit number); the digit list including 0 only gives the digit alphabet. Under the alternative reading (000..999, 1000 strings) P(A2),P(A4),P(A8)=1/2,1/4,1/8; the dependence answers (2ב,2ג,2ד) are identical in both readings. Solution states its Omega explicitly, so it is defensible; pitfall 'take |Omega|=1000' is therefore a reading-dependent pitfall, not a plain error."),
        ('5ב', 'explain-typo', "step 2 explain prints 0.181019, stored answer 0.18101541 (right); harmless."),
    ],
    '24S-A': [
        ('5ב', 'assumption', "1/365 birthday probability is not in the question text; solution introduces Q=1/365 explicitly."),
    ],
    '24S-B': [],
}

OVERRIDES = {
    '25B-A': {
        ('5ב', 'step 0'): "disagree: options a ('same topology, every place holds a unit with prob p regardless of identity') and d ('the arrangement does not change the structure') are both correct statements for why P(Q')=P(Q0); only 'a' is keyed. Fix: reword d to something false (e.g. 'because every arrangement gives the identical circuit').",
    },
    '25A-A': {
        ('4ג', 'solution'): "disagree (intermediate line only, final answer agrees): in the A and not-E case the solution says 'Q1 becomes B and D'. Correct: Q1 | A,not-E = B or (C and D). The next line (joint event = (B or C) and D, probability (2p-p^2)p) and the total p^3(3-2p), ratio (3-2p)/(2-p)^2 are right. Fix the text to 'Q1 becomes B u (C n D)'.",
    },
    '24S-B': {
        ('4ג', 'solution'): "disagree (numeric tail only): solution ends '= (4e^2-e-1)/(4e^2-1) ~ 0.99'. The exact expression is right and equals 0.90481 (own sympy + MC 0.9046); 0.99 is wrong. Official page 9 of the scan prints F(3)=1-1/(4e^2), F(-2)=1/(4e) and the same fraction (4e^2-e-1)/(4e^2-1) followed by a bare '~' with no number, so '0.99' is not official: it is an authoring slip, a typo in an intermediate decimal, not a final-answer error (the final answer is the closed form). Steps already carry 0.9048 (step 2 explain says ~0.90481), so the solution text contradicts its own steps. Fix: '~0.90'.",
    },
}


def main():
    total = {}
    for code in ['25B-A', '25A-A', '24S-A', '24S-B']:
        d = json.load(open(RAW + code + '.json', encoding='utf-8'))
        items = {}
        n_agree = n_dis = 0
        for q in d['questions']:
            key = f"{q['num']}{q.get('part','')}"
            it = {'solution': 'agree', 'rubric': 'agree (points sum to the item points; every point matches a step of the derivation)', 'pitfalls': 'agree', 'steps': {}}
            if 'region' in q:
                it['region'] = 'agree (inequalities match the printed event/sample space; own MC matches `exact`; rendered through region.js for a sample)'
            if 'sim' in q:
                it['sim'] = f"agree (own MC {1_000_000} samples + own enumeration where discrete matches `exact`; spec models the question's experiment; `estimate` label and sample values correct)"
            for i, st in enumerate(q.get('steps', [])):
                it['steps'][str(i)] = f"agree ({st['type']})"
            ov_sol = OVERRIDES.get(code, {}).get((key, 'solution'))
            if ov_sol:
                it['solution'] = ov_sol
            for (k, w), txt in OVERRIDES.get(code, {}).items():
                if k == key and w.startswith('step '):
                    it['steps'][w.split()[1]] = txt
            flags = [f"[{kind}] {txt}" for k2, kind, txt in FLAGS[code] if k2 == key]
            if flags:
                it['flags'] = flags
            dis = [v for v in [it['solution']] + list(it['steps'].values()) if str(v).startswith('disagree')]
            n_dis += len(dis)
            n_agree += (1 + len(it['steps'])) - len(dis)
            items[key] = it
        out = {'examCode': code, 'refuter': 'refuter (blind, own derivation first)', 'derivation': DERIVATION[code],
               'counts': {'items': len(items), 'agree_claims': n_agree, 'disagree_claims': n_dis},
               'items': items}
        json.dump(out, open(RAW + f'_verify_{code}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        total[code] = (len(items), n_agree, n_dis)
    print(total)


main()
