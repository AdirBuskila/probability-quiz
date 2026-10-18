import json, sys
sys.stdout.reconfigure(encoding='utf-8')
code = sys.argv[1]
only = sys.argv[2:]
d = json.load(open(f'C:/Users/Adir/Desktop/Coding/Dev/probability-quiz/tools/raw/{code}.json', encoding='utf-8'))
for q in d['questions']:
    key = f"{q['num']}{q.get('part','')}"
    if only and key not in only: continue
    print('=' * 20, code, key, q.get('kind'), q.get('solutionSource'), q.get('rubricSource'), q.get('stepsSource'), 'hold=' + str(q.get('hold')))
    print('SOL:', q.get('solution'))
    for r in q.get('rubric', []): print('  RUB', r['points'], r['text'])
    for pf in q.get('pitfalls', []): print('  PIT', pf)
    for i, st in enumerate(q.get('steps', [])):
        s = {k: v for k, v in st.items()}
        print('  STEP', i, json.dumps(s, ensure_ascii=False))
    if 'region' in q: print('  REGION', json.dumps(q['region'], ensure_ascii=False))
    if 'sim' in q: print('  SIM', json.dumps(q['sim'], ensure_ascii=False)[:700])
