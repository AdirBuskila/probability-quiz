import json, sys
sys.stdout.reconfigure(encoding='utf-8')
for code in sys.argv[1:]:
    d = json.load(open(f'C:/Users/Adir/Desktop/Coding/Dev/probability-quiz/tools/raw/{code}.json', encoding='utf-8'))
    bad = 0
    for q in d['questions']:
        s = sum(r['points'] for r in q.get('rubric', []))
        if s != q.get('points'):
            bad += 1; print('MISMATCH', code, q['num'], q.get('part'), s, q.get('points'))
        for i, st in enumerate(q.get('steps', [])):
            if st['type'] == 'choice':
                ids = [o['id'] for o in st['options']]
                if st['correctId'] not in ids: print('BAD correctId', code, q['num'], q.get('part'), i)
            if st['type'] == 'numeric' and 'tol' in st and st['tol'] < 0: print('BAD tol', code, q['num'], q.get('part'), i)
    print(code, 'questions', len(d['questions']), 'rubric mismatches', bad)
