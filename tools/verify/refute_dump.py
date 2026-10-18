import json, sys
code = sys.argv[1]
sel = sys.argv[2:]
d = json.load(open(f'tools/raw/{code}.json', encoding='utf-8'))
for q in d['questions']:
    k = f"{q['num']}{q.get('part','')}"
    if sel and k not in sel and str(q['num']) not in sel: continue
    print('=' * 10, k, q['kind'])
    print('SOL:', q.get('solution'))
    r = q.get('rubric')
    if r: print('RUBRIC', sum(x['points'] for x in r), 'pts=', q.get('points'), [(x['text'][:90], x['points']) for x in r])
    for p in q.get('pitfalls', []): print('PIT:', p)
    for i, s in enumerate(q.get('steps', [])):
        s2 = dict(s)
        pr = s2.pop('prompt', '')
        print(f'STEP{i}', s2.get('type'), 'PROMPT:', pr)
        s2.pop('type', None)
        print('   ', json.dumps(s2, ensure_ascii=False))
    if 'region' in q: print('REGION:', json.dumps(q['region'], ensure_ascii=False))
    if 'sim' in q: print('SIM:', json.dumps(q['sim'], ensure_ascii=False))
