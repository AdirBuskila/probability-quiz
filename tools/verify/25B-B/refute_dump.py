"""Compact dump of a raw exam's claims. usage: refute_dump.py CODE [sol_chars]"""
import json, sys
sys.stdout.reconfigure(encoding='utf8')
code = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 400
d = json.load(open(f'tools/raw/{code}.json', encoding='utf8'))
for i, q in enumerate(d['questions']):
    print(f"\n#### idx{i} Q{q.get('num')}{q.get('part','')} kind={q.get('kind')} pts={q.get('points')}")
    if q.get('kind') != 'computation':
        print(' options/key:', json.dumps({k: q.get(k) for k in ('options', 'answer', 'correct', 'correctId', 'key') if k in q}, ensure_ascii=False)[:600])
    print(' SOL-tail:', (q.get('solution') or '')[-n:].replace('\n', ' '))
    if q.get('region'):
        r = q['region']; print(' REGION:', json.dumps(({k: r[k] for k in r if k != 'labels'} if isinstance(r, dict) else r), ensure_ascii=False))
    if q.get('sim'): print(' SIM:', json.dumps(q['sim'], ensure_ascii=False))
    print(' RUBRIC:', [(x['points'], x['text'][:90]) for x in q.get('rubric', [])], 'sum', sum(x['points'] for x in q.get('rubric', [])))
    for p in q.get('pitfalls', []): print(' PIT:', p[:200])
    for j, s in enumerate(q.get('steps', [])):
        ex = {k: s[k] for k in s if k not in ('explain', 'prompt', 'region', 'sim', 'type')}
        print(f"  S{j} [{s['type']}] {s.get('prompt','')[:260]!r}\n      -> {json.dumps(ex, ensure_ascii=False)[:700]}")
        if s.get('region'): print('      region:', json.dumps(s['region'], ensure_ascii=False))
        if s.get('sim'): print('      sim:', json.dumps(s['sim'], ensure_ascii=False))
