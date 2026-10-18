import json, sys
code, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = json.load(open(f'tools/raw/{code}.json', encoding='utf8'))
for i, q in enumerate(d['questions']):
    if not (lo <= i <= hi): continue
    print(f"=== [{i}] Q{q['num']}{q.get('part','')} conf={q.get('confidence')} rub={q.get('rubricSource')} st={q.get('stepsSource')}")
    print("SOL:", q.get('solution'))
    if 'region' in q: print("REGION:", json.dumps(q['region'], ensure_ascii=False))
    if 'sim' in q: print("SIM:", json.dumps(q['sim'], ensure_ascii=False))
    print("RUBRIC:", [(r['text'], r['points']) for r in q.get('rubric', [])], "sum", sum(r['points'] for r in q.get('rubric', [])), "pts", q.get('points'))
    print("PIT:", q.get('pitfalls'))
    for j, s in enumerate(q.get('steps', [])):
        s = dict(s)
        print(f"  STEP{j}:", json.dumps(s, ensure_ascii=False))
