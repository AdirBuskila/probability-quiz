# Refuter: own Monte Carlo of every region spec in the four sittings (own reading of the spec, not region.js),
# compared with the spec's "exact" and with the probability implied by the printed event (hand-coded below).
import json, math, random
random.seed(5)
N = 300000
def const(v):
    if isinstance(v, (int, float)): return float(v)
    return float(eval(v, {"pi": math.pi, "sqrt": math.sqrt}))
def ok(q, x, y):
    if "expr" in q:
        val = eval(q["expr"].replace("^", "**"), {"x": x, "y": y})
        c = const(q["c"])
    else:
        val = const(q.get("a", 0)) * x + const(q.get("b", 0)) * y
        c = const(q["c"])
    return {"<": val < c, "<=": val <= c, ">": val > c, ">=": val >= c}[q["op"]]
def test(sp):
    x0, x1 = map(const, sp["space"]["x"]); y0, y1 = map(const, sp["space"]["y"])
    nE = nG = nEG = 0
    for _ in range(N):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1)
        e = all(ok(q, x, y) for q in sp["event"])
        g = all(ok(q, x, y) for q in sp.get("given", [])) if "given" in sp else True
        nG += g; nEG += e and g
    return nEG / nG
# printed events, independent of the spec (python lambdas of the underlying variables)
truth = {
    ("26A-B", 1): lambda x, y: x * y <= .3,
    ("26A-A", "1א"): lambda x, y: x < y and 2 * x + y < 1,
    ("26A-A", "1ב"): lambda x, y: y > x and y > 1 - x - y,
    ("26A-A", "1ג"): lambda x, y: x < y and x < 1 - x - y and y > 1 - x - y,
    ("26A-A", "1ד"): lambda x, y: 1 - x - y > x and 1 - x - y > y,
    ("25S-C", "1א"): lambda b, L: (L - b) / 2 < .25,
    ("25S-C", "1ב"): lambda b, L: (L - b) / 2 < 2 / 3,
}
for code in ['26A-B', '26A-A', '25S-C', '25S-B']:
    d = json.load(open(f'tools/raw/{code}.json', encoding='utf-8'))
    for q in d['questions']:
        specs = []
        if 'region' in q: specs.append(('Q', q['region']))
        for i, s in enumerate(q.get('steps', [])):
            if 'region' in s: specs.append((f'step{i}', s['region']))
        for where, r in specs:
            for sp in (r if isinstance(r, list) else [r]):
                p = test(sp)
                key = (code, q['num']) if code == '26A-B' else (code, f"{q['num']}{q.get('part','')}")
                x0, x1 = map(const, sp["space"]["x"]); y0, y1 = map(const, sp["space"]["y"])
                t = None
                if key in truth:
                    f = truth[key]; c = 0
                    for _ in range(N):
                        c += f(random.uniform(x0, x1), random.uniform(y0, y1))
                    t = c / N
                elif code == '25S-B':
                    pp = math.pi
                    def ev(a, b, k=q.get('part')):
                        if k == 'א': return b > 2 * a
                        if k == 'ב': return abs(a - b) < pp / 2
                        if k == 'ג': return abs(a - b) < pp / 2 and b > 2 * a
                    c = n = 0
                    for _ in range(N):
                        a, b = random.uniform(0, pp), random.uniform(0, pp)
                        if q.get('part') == 'ג':
                            if b > 2 * a:
                                n += 1; c += abs(a - b) < pp / 2
                        else:
                            n += 1; c += ev(a, b)
                    t = c / n
                print(code, q['num'], q.get('part'), where, 'spec MC', round(p, 4), 'spec exact', round(sp.get('exact', float('nan')), 4), 'printed-event MC', None if t is None else round(t, 4))
