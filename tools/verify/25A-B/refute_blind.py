import json, sys
sys.stdout.reconfigure(encoding='utf8')
d = json.load(open(f'tools/raw/_blind_{sys.argv[1]}.json', encoding='utf8'))
for k, v in (d['contexts'].items() if isinstance(d['contexts'], dict) else enumerate(d['contexts'])):
    print('CTX', k, json.dumps(v, ensure_ascii=False))
for q in d['questions']:
    extra = {k: q[k] for k in q if k not in ('num', 'part', 'kind', 'topic', 'points', 'question', 'contextId', 'image')}
    print(f"\n{q['num']}{q['part']} {q['kind']} pts={q['points']} ctx={q.get('contextId')} img={q.get('image')} {extra if extra else ''}\n  {q['question']}")
