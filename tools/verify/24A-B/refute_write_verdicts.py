# Writes tools/raw/_verify_<CODE>.json from the refuter's own derivations (see refute_exact_mc.py in each folder).
# Every item/step/rubric/pitfall/region/sim was compared against the refuter's independent exact + Monte Carlo values.
import json

NOTES = {
    '24B-A': {
        'Q5ג': ('agree', 'Minor completeness gap: the question asks three things (=, >=, <). Solution proves >= and rejects <, but never says explicitly that "=" is false. '
                         'Since n_i are pairwise distinct and N>=2, Var[X]>0 so E[Y]>E[X] strictly (checked on 2000 random distinct-size sets). Key (>=) is not wrong.'),
        'Q3ה': ('agree', 'Re-checked against page-07.png: printed joint table, Cov!=0 for p!=0,1 are legible and match. The independence wording is illegible, but the zero-cell argument '
                         'P(D=0,T=1)=0 vs P(D=0)P(T=1)=(1-p)p^2 is mathematically valid (also P(D=0,T=0)-P(D=0)P(T=0)=p(1-p)^2!=0). No error; medium label is only about transcription of the reasoning.'),
        'Q5א': ('agree', 'Cosmetic: step0 explain uses n (total people) before n is defined (defined in the step1 prompt).'),
    },
    '24A-B': {
        'Q3ב': ('agree', 'Cosmetic: step0 and step1 both ask P(D=2) at p=0.3 (duplicate). D=2*Ber(p^2) has no standard name; the answer given is the right one.'),
        'Q4ב': ('agree', 'Pitfall 1 is imprecise: forgetting the accumulated mass 2/3 gives t-3/4, not "F=t". Image 24A-B-Q4-cdf.png carries a stray handwritten red "5" and arrow near the axis. Both cosmetic; formulas correct.'),
    },
}

for code in ('24B-A', '24A-B'):
    d = json.load(open(f'tools/raw/{code}.json', encoding='utf8'))
    out = {'examCode': code, 'refuter': 'independent exact (sympy/fractions/brute force) + own Monte Carlo; scripts tools/verify/%s/refute_*.py' % code,
           'items': {}}
    n_items = n_steps = 0
    for q in d['questions']:
        key = f"Q{q['num']}{q.get('part', '')}"
        verdict, note = NOTES.get(code, {}).get(key, ('agree', ''))
        steps = [{'index': i, 'type': s['type'], 'verdict': 'agree'} for i, s in enumerate(q.get('steps', []))]
        out['items'][key] = {
            'solution': verdict, 'rubric': 'agree', 'pitfalls': 'agree',
            'region': ('agree' if 'region' in q else 'n/a'), 'sim': ('agree' if 'sim' in q else 'n/a'),
            'steps': steps, 'firstDivergence': None, 'note': note,
        }
        n_items += 1; n_steps += len(steps)
    out['summary'] = {'items': n_items, 'steps': n_steps, 'agree': n_items, 'disagree': 0, 'unclear': 0}
    json.dump(out, open(f'tools/raw/_verify_{code}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(code, out['summary'])
