"""Independent re-check of every `region` and `sim` in the given sittings (own evaluator, own MC, own enumeration).
Does not use region.js / sim.js / check_sim_specs.py."""
import ast, itertools, json, math, sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'C:/Users/Adir/Desktop/Coding/Dev/probability-quiz/tools/raw/'
rng = np.random.default_rng(31337)
NMC = 1_000_000

FUNCS = {'abs': np.abs, 'sqrt': np.sqrt, 'exp': np.exp, 'log': np.log, 'ln': np.log, 'floor': np.floor, 'ceil': np.ceil,
         'round': np.round, 'min': np.minimum, 'max': np.maximum, 'sin': np.sin, 'cos': np.cos}
CONST = {'pi': math.pi, 'e': math.e}


class T(ast.NodeTransformer):
    def visit_BoolOp(self, n):
        vals = [self.visit(v) for v in n.values]
        op = ast.BitAnd() if isinstance(n.op, ast.And) else ast.BitOr()
        out = vals[0]
        for v in vals[1:]:
            out = ast.BinOp(out, op, v)
        return out

    def visit_UnaryOp(self, n):
        if isinstance(n.op, ast.Not):
            return ast.UnaryOp(ast.Invert(), self.visit(n.operand))
        return self.generic_visit(n)

    def visit_Compare(self, n):
        parts = []
        left = self.visit(n.left)
        for op, c in zip(n.ops, n.comparators):
            c = self.visit(c)
            parts.append(ast.Compare(left, [op], [c]))
            left = c
        out = parts[0]
        for p in parts[1:]:
            out = ast.BinOp(out, ast.BitAnd(), p)
        return out


def comp(src):
    s = src.replace('&&', ' and ').replace('||', ' or ').replace('^', '**')
    tree = ast.parse(s, mode='eval')
    tree = ast.fix_missing_locations(T().visit(tree))
    return compile(tree, '<e>', 'eval')


def ev(src, env):
    e = dict(FUNCS); e.update(CONST); e.update(env)
    return eval(comp(src), {'__builtins__': {}}, e)


def num(v):
    if isinstance(v, (int, float)): return float(v)
    return float(eval(comp(v), {'__builtins__': {}}, dict(FUNCS, **CONST)))


def ineq_mask(q, x, y):
    c = num(q['c']) if 'c' in q else 0.0
    if 'expr' in q:
        v = ev(q['expr'], {'x': x, 'y': y})
    else:
        v = num(q.get('a', 0)) * x + num(q.get('b', 0)) * y
    op = q['op']
    return {'<': v < c, '<=': v <= c, '>': v > c, '>=': v >= c}[op]


def set_mask(s, x, y):
    if isinstance(s, str):
        return ev(s, {'x': x, 'y': y}).astype(bool) if hasattr(ev(s, {'x': x[:1], 'y': y[:1]}), 'astype') else bool(ev(s, {'x': x, 'y': y}))
    if isinstance(s, dict):
        assert list(s.keys()) == ['any'], s
        m = np.zeros_like(x, bool)
        for conj in s['any']:
            m |= set_mask(conj, x, y)
        return m
    m = np.ones_like(x, bool)
    for q in s:
        if isinstance(q, dict) and 'any' in q:
            m &= set_mask(q, x, y)
        elif isinstance(q, str):
            m &= set_mask(q, x, y)
        else:
            m &= ineq_mask(q, x, y)
    return m


def sample_space(sp, n):
    x0, x1 = num(sp['x'][0]), num(sp['x'][1]); y0, y1 = num(sp['y'][0]), num(sp['y'][1])
    return x0 + (x1 - x0) * rng.random(n), y0 + (y1 - y0) * rng.random(n)


def check_region(r, label, out):
    x, y = sample_space(r['space'], NMC)
    ev_m = set_mask(r['event'], x, y)
    if r.get('given'):
        g = set_mask(r['given'], x, y)
        p = (ev_m & g).sum() / g.sum(); se = math.sqrt(p * (1 - p) / g.sum())
    else:
        p = ev_m.mean(); se = math.sqrt(p * (1 - p) / NMC)
    ex = r.get('exact')
    ok = ex is not None and abs(p - ex) <= 4 * se + 1e-4
    out.append((label, 'region', ok, f'MC={p:.5f} exact={ex} (4se={4*se:.5f}) caption={r.get("caption")}'))


# ---------------- sims
def build_var_samples(kind, params, n, item):
    """return dict of numpy arrays of the kind's variables"""
    if kind == 'area':
        if params.get('fromRegion'):
            reg = item['region']; reg = reg[0] if isinstance(reg, list) else reg
            sp = reg['space']; params = dict(params, event=reg['event'], given=reg.get('given'))
        else:
            sp = params['space']
        x, y = sample_space(sp, n)
        return {'x': x, 'y': y}, params
    if kind == 'pdf':
        pieces = params['pieces']
        # numeric inverse cdf on fine table per piece
        grid = []; dens = []
        for pc in pieces:
            a, b = num(pc['from']), num(pc['to'])
            xs = np.linspace(a, b, 40001)
            ds = ev(pc['expr'], {'x': xs}) * np.ones_like(xs)
            grid.append(xs); dens.append(ds)
        xs_all = np.concatenate(grid); ds_all = np.concatenate(dens)
        # cumulative trapezoid inside pieces
        cum = [0.0]; X = [xs_all[0]]
        pos = 0
        xs_l = []; c_l = []
        tot = 0.0
        for xs, ds in zip(grid, dens):
            seg = np.concatenate([[0], np.cumsum((ds[1:] + ds[:-1]) / 2 * np.diff(xs))]) + tot
            xs_l.append(xs); c_l.append(seg); tot = seg[-1]
        xs_all = np.concatenate(xs_l); cdf = np.concatenate(c_l)
        params = dict(params); params['_mass'] = tot
        u = rng.random(n) * tot
        idx = np.searchsorted(cdf, u).clip(1, len(cdf) - 1)
        lo, hi = cdf[idx - 1], cdf[idx]
        t = np.where(hi > lo, (u - lo) / np.where(hi > lo, hi - lo, 1), 0)
        xs_s = xs_all[idx - 1] + t * (xs_all[idx] - xs_all[idx - 1])
        return {'x': xs_s}, params
    if kind == 'dice':
        nd = params['n']; faces = params.get('faces', 6); w = params.get('weights')
        ds = []
        for i in range(nd):
            if w is None: ds.append(rng.integers(1, faces + 1, n))
            else:
                ww = np.array(w[i] if isinstance(w[0], list) else w, float); ww /= ww.sum()
                ds.append(rng.choice(np.arange(1, faces + 1), n, p=ww))
        env = {f'd{i+1}': d for i, d in enumerate(ds)}
        st = np.stack(ds, 1)
        env.update(sum=st.sum(1), prod=st.prod(1), max=st.max(1), min=st.min(1), n=nd)
        return env, params
    if kind == 'urn':
        draws = params['draws']; rep = params.get('replace', False)
        if 'counts' in params:
            names = list(params['counts']); cnt = [params['counts'][k] for k in names]
            pool = np.repeat(np.arange(len(names)), cnt)
            tot = len(pool)
            if rep:
                d = pool[rng.integers(0, tot, (n, draws))]
            else:
                perm = np.argsort(rng.random((n, tot)), 1)[:, :draws]
                d = pool[perm]
            env = {}
            for k, nm in enumerate(names):
                env[nm] = (d == k).sum(1)
                for j in range(draws):
                    env[f'{nm}_{j+1}'] = (d[:, j] == k).astype(int)
            return env, params
        vals = np.array(params['values'], float); tot = len(vals)
        if rep:
            idx = rng.integers(0, tot, (n, draws))
        else:
            idx = np.argsort(rng.random((n, tot)), 1)[:, :draws]
        d = vals[idx]
        env = {f'v{j+1}': d[:, j] for j in range(draws)}
        env.update(sum=d.sum(1), max=d.max(1), min=d.min(1))
        return env, params
    if kind == 'custom_discrete':
        if 'vars' in params:
            env = {}
            for k, v in params['vars'].items():
                pr = np.array(v['probs'], float); pr /= pr.sum()
                env[k] = rng.choice(np.array(v['values'], float), n, p=pr)
            return env, params
        rows = params['joint']
        pr = np.array([r['p'] for r in rows], float); pr /= pr.sum()
        idx = rng.choice(len(rows), n, p=pr)
        keys = [k for k in rows[0] if k != 'p']
        env = {k: np.array([r[k] for r in rows], float)[idx] for k in keys}
        return env, params
    if kind == 'circuit':
        comps = []
        def walk(nd):
            if nd['type'] == 'comp': comps.append((nd['id'], nd['p']))
            else:
                for c in nd['children']: walk(c)
        if 'network' in params:
            walk(params['network'])
            ids = [c[0] for c in comps]; ps = [c[1] for c in comps]
        else:
            ids = [e['id'] for e in params['edges']]; ps = [e['p'] for e in params['edges']]
        k = len(ids)
        st = rng.random((n, k)) < np.array(ps)
        env = {i: st[:, j].astype(int) for j, i in enumerate(ids)}
        # structure function via enumeration table
        table = np.zeros(2 ** k, bool)
        def struct(state):
            s = dict(zip(ids, state))
            if 'network' in params:
                def f(nd):
                    t = nd['type']
                    if t == 'comp': return bool(s[nd['id']])
                    ch = [f(c) for c in nd['children']]
                    if t == 'series': return all(ch)
                    if t == 'parallel': return any(ch)
                    if t == 'kofn': return sum(ch) >= nd['k']
                return f(params['network'])
            adj = {}
            for e in params['edges']:
                if s[e['id']]:
                    adj.setdefault(e['from'], set()).add(e['to']); adj.setdefault(e['to'], set()).add(e['from'])
            seen = {params['source']}; stack = [params['source']]
            while stack:
                z = stack.pop()
                for w_ in adj.get(z, ()):
                    if w_ not in seen: seen.add(w_); stack.append(w_)
            return params['sink'] in seen
        for code in range(2 ** k):
            state = [(code >> j) & 1 for j in range(k)]
            table[code] = struct(state)
        code_arr = sum((st[:, j].astype(np.int64) << j) for j in range(k))
        env['S'] = table[code_arr].astype(int)
        # exact enumeration
        exact = {}
        params = dict(params); params['_table'] = (ids, ps, table)
        return env, params
    raise ValueError(kind)


def sim_exact_enum(kind, params, item):
    """exact value by enumeration for discrete kinds; None otherwise"""
    measure = params.get('measure', 'prob')
    if measure != 'prob': return None
    if kind == 'circuit':
        ids, ps, table = params['_table']
        k = len(ids)
        tot_ev = 0.0; tot_g = 0.0
        for code in range(2 ** k):
            w = 1.0
            env = {}
            for j in range(k):
                b = (code >> j) & 1
                w *= ps[j] if b else 1 - ps[j]
                env[ids[j]] = np.array([b])
            env['S'] = np.array([int(table[code])])
            g = bool(ev(params['given'], env)[0]) if params.get('given') else True
            if not g: continue
            tot_g += w
            if bool(np.array(ev(params['event'], env)).reshape(-1)[0]): tot_ev += w
        return tot_ev / tot_g
    if kind == 'dice':
        nd = params['n']; faces = params.get('faces', 6)
        if faces ** nd > 400000 or params.get('weights'): return None
        grid = np.array(list(itertools.product(range(1, faces + 1), repeat=nd)))
        env = {f'd{i+1}': grid[:, i] for i in range(nd)}
        env.update(sum=grid.sum(1), prod=grid.prod(1), max=grid.max(1), min=grid.min(1), n=nd)
        m = np.ones(len(grid), bool) if not params.get('given') else np.asarray(ev(params['given'], env), bool)
        e_ = np.asarray(ev(params['event'], env), bool)
        return (e_ & m).sum() / m.sum()
    if kind == 'custom_discrete':
        if 'joint' in params:
            rows = params['joint']
            pr = np.array([r['p'] for r in rows], float)
            keys = [k for k in rows[0] if k != 'p']
            env = {k: np.array([r[k] for r in rows], float) for k in keys}
            m = np.ones(len(rows), bool) if not params.get('given') else np.asarray(ev(params['given'], env), bool)
            e_ = np.asarray(ev(params['event'], env), bool)
            return (pr * (e_ & m)).sum() / (pr * m).sum()
        names = list(params['vars'])
        sizes = [len(params['vars'][k]['values']) for k in names]
        if np.prod(sizes) > 2_000_000: return None
        grids = np.meshgrid(*[np.array(params['vars'][k]['values'], float) for k in names], indexing='ij')
        pgrids = np.meshgrid(*[np.array(params['vars'][k]['probs'], float) / sum(params['vars'][k]['probs']) for k in names], indexing='ij')
        env = {k: g.reshape(-1) for k, g in zip(names, grids)}
        pr = np.prod(pgrids, axis=0).reshape(-1)
        m = np.ones(len(pr), bool) if not params.get('given') else np.asarray(ev(params['given'], env), bool)
        e_ = np.asarray(ev(params['event'], env), bool)
        return (pr * (e_ & m)).sum() / (pr * m).sum()
    if kind == 'urn':
        return None
    return None


def check_sim(sim, item, label, out):
    kind = sim['kind']; params = sim['params']
    env, params = build_var_samples(kind, params, NMC, item)
    measure = params.get('measure', 'prob')
    given = params.get('given')
    if kind == 'area':
        event = params.get('event')
        if not isinstance(event, str):
            xs, ys = env['x'], env['y']
        else:
            xs, ys = env['x'], env['y']
        m = np.ones(NMC, bool)
        if given: m = set_mask(given, env['x'], env['y']) if not isinstance(given, str) else np.asarray(ev(given, env), bool)
        if measure == 'prob':
            e_ = set_mask(event, env['x'], env['y']) if not isinstance(event, str) else np.asarray(ev(event, env), bool)
    else:
        m = np.ones(NMC, bool) if not given else np.asarray(ev(given, env), bool)
        if measure == 'prob':
            e_ = np.asarray(ev(params['event'], env), bool)
    if measure == 'prob':
        p = (e_ & m).sum() / m.sum(); se = math.sqrt(max(p * (1 - p), 1e-12) / m.sum())
    elif measure in ('mean', 'var'):
        v = np.asarray(ev(params['expr'], env), float)[m]
        p = v.mean() if measure == 'mean' else v.var(); se = v.std() / math.sqrt(len(v)) if measure == 'mean' else v.var() * math.sqrt(2.0 / len(v))
    elif measure == 'cov':
        a = np.asarray(ev(params['expr'][0], env), float)[m]; b = np.asarray(ev(params['expr'][1], env), float)[m]
        p = np.mean(a * b) - a.mean() * b.mean(); se = a.std() * b.std() / math.sqrt(len(a))
    ex = sim['exact']
    # pdf mass check
    note = ''
    if kind == 'pdf': note = f" mass={params['_mass']:.6f}"
    enum = sim_exact_enum(kind, params, item)
    ok = abs(p - ex) <= 4.5 * se + 1e-4
    if enum is not None:
        ok = ok and abs(enum - ex) < 1e-9 + 1e-6 * abs(ex)
        note += f' enum={enum:.9f}'
    out.append((label, f'sim/{kind}', ok, f'MC={p:.5f} exact={ex} (4.5se={4.5*se:.5f}){note} est="{sim.get("estimate")}"'))


def main():
    for code in sys.argv[1:]:
        d = json.load(open(ROOT + code + '.json', encoding='utf-8'))
        out = []
        for q in d['questions']:
            lab = f"{code}-Q{q['num']}{q.get('part','')}"
            regs = q.get('region')
            if regs:
                for i, r in enumerate(regs if isinstance(regs, list) else [regs]):
                    check_region(r, f'{lab} region{i}', out)
            for si, st in enumerate(q.get('steps', [])):
                if 'region' in st:
                    rr = st['region']
                    for i, r in enumerate(rr if isinstance(rr, list) else [rr]):
                        check_region(r, f'{lab} step{si} region{i}', out)
            if 'sim' in q:
                try:
                    check_sim(q['sim'], {'region': q.get('region')}, lab, out)
                except Exception as ex_:
                    out.append((lab, 'sim', False, f'ERROR {ex_!r}'))
        for lab, typ, ok, msg in out:
            print(('OK  ' if ok else 'FAIL'), lab, typ, msg)
        print(code, 'total', len(out), 'fail', sum(1 for o in out if not o[2]))


main()
