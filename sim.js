"use strict";
/* "Simulate it" (window.Sim) -- probability-only, app-local. A question may carry
     sim: { kind, params, estimate, exact, trials?, seed? }        (tools/RAW_SCHEMA.md, "Simulations")
   kind: area | pdf | circuit | dice | urn | bernoulli_matrix | custom_discrete.
   Common params: measure "prob" (default) | "mean" | "var" | "cov";
     event  (prob)      a predicate over the kind's variables (string; for area also the region forms);
     expr   (mean/var)  an expression; for cov a pair [expr1, expr2];
     given  (optional)  a predicate: everything is conditional on it (P(A|B), E[X|B] ...).
   Expressions use the tiny, eval-free language of region.js (Region.Expr).
   Each kind is a generator (one random outcome per trial, mulberry32 seeded) plus a deterministic "compute"
   (exact enumeration, exact polygon area, or quadrature) used by tools/check_sim_specs.py so the button and the
   key can never disagree:  Sim.check(spec) runs exactly the UI's first run (same seed, same trials).
   API: Sim.run(spec,{trials,seed,item}) -> {est,se,n,nGiven}   Sim.compute(spec,{item}) -> {value,method,tol}
        Sim.check(spec,{item}) -> {ok, problems, mc, computed}   Sim.mount(el, spec, {item}) -> the UI box */
(function (root) {
  const Region = root.Region || (typeof require === "function" ? require("./region.js") : null);
  const { compile, constant } = Region.Expr;
  const DEFAULT_TRIALS = 100000, DEFAULT_SEED = 20240325, ENUM_CAP = 2000000;

  function mulberry32(a) {
    a = a >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  /* Gauss-Legendre nodes/weights on [-1,1] */
  const GL5 = { x: [-0.9061798459386640, -0.5384693101056831, 0, 0.5384693101056831, 0.9061798459386640],
    w: [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891] };
  const pickCdf = (cum, u) => { let lo = 0, hi = cum.length - 1; while (lo < hi) { const m = (lo + hi) >> 1; if (cum[m] < u) lo = m + 1; else hi = m; } return lo; };
  const isIdent = s => typeof s === "string" && /^[A-Za-z_][A-Za-z0-9_]*$/.test(s);
  const num = (v, what) => { const x = constant(v); if (!isFinite(x)) throw new Error(`${what} is not a finite number`); return x; };

  /* ============================ generators ============================
     Each returns { vars:Set, sample(rng, env), enumerate?(cb(w, env)) -> method, preds?(compiled) }.
     enumerate calls cb(weight, env) over every outcome (weights sum to 1) and returns its method name. */
  const KINDS = {};

  /* ---- area: (x, y) uniform on the space rectangle; event/given may be region inequality forms ---- */
  KINDS.area = function (p, ctx) {
    const sp = Region._.normSpace(p.space);
    const vars = new Set(["x", "y"]);
    const rx = sp.x1 - sp.x0, ry = sp.y1 - sp.y0;
    return {
      vars,
      sample(rng, env) { env.x = sp.x0 + rng() * rx; env.y = sp.y0 + rng() * ry; },
      regionPred(form) { const set = Region._.normSet(form); const f = Region._.setPred(set); return { set, fn: env => f(env.x, env.y) ? 1 : 0 }; },
      exactProb(Eset, Gset) {   // all-linear sets: exact polygon areas
        const L = Region._.isLinearSet;
        if (!L(Eset) || (Gset && !L(Gset))) return null;
        const EG = Gset ? Region._.andSets(Eset, Gset) : Eset;
        const a = Region._.linearArea(EG, sp), b = Gset ? Region._.linearArea(Gset, sp) : rx * ry;
        return a == null || b == null ? null : a / b;
      },
      quadrature(preds, cb) {
        // columns: 300 cells x 5 Gauss nodes in x; per column, split y at every predicate's sign change, 5 Gauss nodes per piece
        const NXC = 300, NY = 200, hx = rx / NXC, env = {};
        for (let i = 0; i < NXC; i++) for (let a = 0; a < 5; a++) {
          const x = sp.x0 + hx * (i + 0.5 + 0.5 * GL5.x[a]), wx = hx * 0.5 * GL5.w[a];
          const cuts = [sp.y0, sp.y1];
          for (const pr of preds) {
            const f = y => { env.x = x; env.y = y; return !!pr(env); };
            for (const [lo, hi] of Region._.columnIntervals((xx, y) => f(y), x, sp.y0, sp.y1, NY)) cuts.push(lo, hi);
          }
          cuts.sort((u, v) => u - v);
          for (let k = 0; k + 1 < cuts.length; k++) {
            const y0 = cuts[k], y1 = cuts[k + 1], hy = y1 - y0;
            if (hy <= 1e-15) continue;
            for (let b = 0; b < 5; b++) {
              env.x = x; env.y = y0 + hy * 0.5 * (1 + GL5.x[b]);
              cb(wx * hy * 0.5 * GL5.w[b] / (rx * ry), env);
            }
          }
        }
        return "quadrature";
      },
    };
  };

  /* ---- pdf: a piecewise density of x, pieces [{from,to,expr}] (finite bounds); numeric inverse CDF ---- */
  KINDS.pdf = function (p) {
    const vars = new Set(["x"]);
    if (!Array.isArray(p.pieces) || !p.pieces.length) throw new Error("pdf needs pieces [{from,to,expr}]");
    const pieces = p.pieces.map((q, i) => {
      const a = num(q.from, `piece ${i} from`), b = num(q.to, `piece ${i} to`);
      if (!(b > a)) throw new Error(`piece ${i}: to must be > from`);
      return { a, b, f: compile(q.expr, vars) };
    }).sort((u, v) => u.a - v.a);
    // sampling table: K cells per piece, mass by 5-point Gauss (no endpoint evaluation: integrable singularities are fine)
    const K = 20000, lefts = [], widths = [], cum = [], env = {};
    let tot = 0, negative = false;
    for (const pc of pieces) {
      const h = (pc.b - pc.a) / K;
      for (let j = 0; j < K; j++) {
        const l = pc.a + h * j; let m = 0;
        for (let k = 0; k < 5; k++) { env.x = l + h * 0.5 * (1 + GL5.x[k]); const v = pc.f(env); if (v < -1e-12) negative = true; m += h * 0.5 * GL5.w[k] * v; }
        tot += Math.max(m, 0); lefts.push(l); widths.push(h); cum.push(tot);
      }
    }
    if (!(tot > 0)) throw new Error("pdf integrates to 0");
    return {
      vars, norm: tot, negative,
      sample(rng, e) {
        const u = rng() * tot, j = pickCdf(cum, u), prev = j ? cum[j - 1] : 0, m = cum[j] - prev;
        e.x = lefts[j] + (m > 0 ? (u - prev) / m : rng()) * widths[j];
      },
      quadrature(preds, cb) {
        const e = {};
        for (const pc of pieces) {
          const NB = 400, NS = 25, h = (pc.b - pc.a) / NB;
          for (let j = 0; j < NB; j++) {
            const l = pc.a + h * j, cuts = [l, l + h];
            for (const pr of preds) {   // sign changes inside the cell
              const at = x => { e.x = x; return !!pr(e); };
              let prev = at(l + h / (2 * NS));
              for (let s = 1; s < NS; s++) {
                const x = l + h * (s + 0.5) / NS, on = at(x);
                if (on !== prev) { let lo = x - h / NS, hi = x; for (let t = 0; t < 40; t++) { const m = (lo + hi) / 2; if (at(m) === prev) lo = m; else hi = m; } cuts.push((lo + hi) / 2); prev = on; }
              }
            }
            cuts.sort((u, v) => u - v);
            for (let k = 0; k + 1 < cuts.length; k++) {
              const a = cuts[k], b = cuts[k + 1], w = b - a;
              if (w <= 1e-15) continue;
              for (let g = 0; g < 5; g++) { e.x = a + w * 0.5 * (1 + GL5.x[g]); const fx = pc.f(e); e.x = a + w * 0.5 * (1 + GL5.x[g]); cb(w * 0.5 * GL5.w[g] * fx / tot, e); }
            }
          }
        }
        return "quadrature";
      },
    };
  };

  /* ---- circuit: series/parallel/k-of-n tree, or an edge list (bridge); variables: each component id, S ---- */
  KINDS.circuit = function (p) {
    const comps = [], ids = new Set();
    const addComp = (id, pr) => {
      if (!isIdent(id) || id === "S") throw new Error(`component id ${JSON.stringify(id)} must be an identifier other than S`);
      if (ids.has(id)) throw new Error(`duplicate component id ${id}`);
      const pv = num(pr, `component ${id} p`);
      if (!(pv >= 0 && pv <= 1)) throw new Error(`component ${id}: p must be in [0,1]`);
      ids.add(id); comps.push({ id, p: pv });
    };
    let works;
    if (p.network) {
      const build = node => {
        if (!node || typeof node !== "object") throw new Error("network node must be an object");
        if (node.type === "comp") { addComp(node.id, node.p); const id = node.id; return e => e[id]; }
        const kids = (node.children || []).map(build);
        if (!kids.length) throw new Error(`${node.type} needs children`);
        if (node.type === "series") return e => { for (const k of kids) if (!k(e)) return 0; return 1; };
        if (node.type === "parallel") return e => { for (const k of kids) if (k(e)) return 1; return 0; };
        if (node.type === "kofn") { const K = node.k; if (!Number.isInteger(K) || K < 1 || K > kids.length) throw new Error("kofn needs 1 <= k <= children"); return e => { let c = 0; for (const k of kids) if (k(e)) c++; return c >= K ? 1 : 0; }; }
        throw new Error(`network node type ${JSON.stringify(node.type)} must be series|parallel|kofn|comp`);
      };
      works = build(p.network);
    } else if (Array.isArray(p.edges)) {
      const edges = p.edges.map(ed => { addComp(ed.id, ed.p); return [String(ed.from), String(ed.to), ed.id]; });
      const src = String(p.source), dst = String(p.sink);
      if (p.source == null || p.sink == null) throw new Error("edge-list circuit needs source and sink");
      works = e => {   // undirected reachability over working components
        const seen = new Set([src]), stack = [src];
        while (stack.length) {
          const u = stack.pop();
          if (u === dst) return 1;
          for (const [a, b, id] of edges) if (e[id]) {
            const v = a === u ? b : b === u ? a : null;
            if (v != null && !seen.has(v)) { seen.add(v); stack.push(v); }
          }
        }
        return 0;
      };
    } else throw new Error("circuit needs network (tree) or edges + source + sink");
    const vars = new Set([...ids, "S"]);
    return {
      vars,
      sample(rng, e) { for (const c of comps) e[c.id] = rng() < c.p ? 1 : 0; e.S = works(e); },
      enumerate(cb) {
        const n = comps.length;
        if (n > 21) return null;
        const e = {};
        for (let m = 0; m < (1 << n); m++) {
          let w = 1;
          for (let i = 0; i < n; i++) { const on = (m >> i) & 1; e[comps[i].id] = on; w *= on ? comps[i].p : 1 - comps[i].p; }
          e.S = works(e);
          if (w > 0) cb(w, e);
        }
        return "enumeration";
      },
    };
  };

  /* ---- dice: n dice, faces (default 6), optional weights (one list for all dice, or one per die) ---- */
  KINDS.dice = function (p) {
    const n = p.n, F = p.faces == null ? 6 : p.faces;
    if (!Number.isInteger(n) || n < 1 || n > 12) throw new Error("dice: n must be an integer 1..12");
    if (!Number.isInteger(F) || F < 2) throw new Error("dice: faces must be an integer >= 2");
    let W = p.weights;
    const perDie = [];
    for (let d = 0; d < n; d++) {
      const w = W == null ? Array(F).fill(1) : (Array.isArray(W[0]) ? W[d] : W);
      if (!Array.isArray(w) || w.length !== F || w.some(v => !(num(v, "weight") >= 0))) throw new Error(`dice: weights for die ${d + 1} must be ${F} numbers >= 0`);
      const ws = w.map(v => num(v, "weight")), t = ws.reduce((a, b) => a + b, 0);
      let c = 0; perDie.push({ pr: ws.map(v => v / t), cum: ws.map(v => (c += v / t)) });
    }
    const vars = new Set(["sum", "prod", "max", "min", "n"]);
    for (let d = 1; d <= n; d++) vars.add("d" + d);
    const fill = (e, faces) => {
      let s = 0, pr = 1, mx = -Infinity, mn = Infinity;
      for (let d = 0; d < n; d++) { const v = faces[d]; e["d" + (d + 1)] = v; s += v; pr *= v; if (v > mx) mx = v; if (v < mn) mn = v; }
      e.sum = s; e.prod = pr; e.max = mx; e.min = mn; e.n = n;
    };
    const faces = new Array(n);
    return {
      vars,
      sample(rng, e) { for (let d = 0; d < n; d++) faces[d] = pickCdf(perDie[d].cum, rng() * perDie[d].cum[F - 1]) + 1; fill(e, faces); },
      enumerate(cb) {
        if (Math.pow(F, n) > ENUM_CAP) return null;
        const e = {};
        const rec = (d, w) => {
          if (d === n) { fill(e, faces); cb(w, e); return; }
          for (let f = 0; f < F; f++) { const q = perDie[d].pr[f]; if (q > 0) { faces[d] = f + 1; rec(d + 1, w * q); } }
        };
        rec(0, 1);
        return "enumeration";
      },
    };
  };

  /* ---- urn: counts by color ({"red":3,"black":5}) or numbered balls (values:[...]); k draws ---- */
  KINDS.urn = function (p) {
    const k = p.draws, rep = p.replace === true;
    let balls, colors = null;
    if (p.counts) {
      colors = Object.keys(p.counts);
      for (const c of colors) if (!isIdent(c)) throw new Error(`urn color ${JSON.stringify(c)} must be an identifier`);
      balls = [];
      colors.forEach((c, ci) => { const m = p.counts[c]; if (!Number.isInteger(m) || m < 0) throw new Error(`urn count of ${c} must be an integer >= 0`); for (let j = 0; j < m; j++) balls.push(ci); });
    } else if (Array.isArray(p.values)) balls = p.values.map(v => num(v, "urn value"));
    else throw new Error("urn needs counts {color:n} or values [...]");
    const N = balls.length;
    if (!Number.isInteger(k) || k < 1 || (!rep && k > N)) throw new Error("urn: draws must be 1..(number of balls) without replacement");
    const vars = new Set();
    if (colors) for (const c of colors) { vars.add(c); for (let i = 1; i <= k; i++) vars.add(c + "_" + i); }
    else { ["sum", "max", "min"].forEach(v => vars.add(v)); for (let i = 1; i <= k; i++) vars.add("v" + i); }
    const seq = new Array(k);
    const fill = e => {
      if (colors) {
        for (let ci = 0; ci < colors.length; ci++) { let c = 0; for (let i = 0; i < k; i++) { const on = seq[i] === ci ? 1 : 0; e[colors[ci] + "_" + (i + 1)] = on; c += on; } e[colors[ci]] = c; }
      } else {
        let s = 0, mx = -Infinity, mn = Infinity;
        for (let i = 0; i < k; i++) { const v = seq[i]; e["v" + (i + 1)] = v; s += v; if (v > mx) mx = v; if (v < mn) mn = v; }
        e.sum = s; e.max = mx; e.min = mn;
      }
    };
    const work = balls.slice();
    return {
      vars,
      sample(rng, e) {
        if (rep) for (let i = 0; i < k; i++) seq[i] = balls[Math.floor(rng() * N)];
        else for (let i = 0; i < k; i++) { const j = i + Math.floor(rng() * (N - i)); const t = work[i]; work[i] = work[j]; work[j] = t; seq[i] = work[i]; }
        fill(e);
      },
      enumerate(cb) {
        const e = {};
        if (colors) {   // sequences of colors, weighted by the remaining counts
          if (Math.pow(colors.length, k) > ENUM_CAP) return null;
          const left = colors.map(c => p.counts[c]);
          const rec = (i, w, tot) => {
            if (i === k) { fill(e); cb(w, e); return; }
            for (let ci = 0; ci < colors.length; ci++) {
              if (!left[ci]) continue;
              seq[i] = ci;
              const q = left[ci] / tot;
              if (rep) rec(i + 1, w * q, tot); else { left[ci]--; rec(i + 1, w * q, tot - 1); left[ci]++; }
            }
          };
          rec(0, 1, N);
        } else {
          let leaves = 1; for (let i = 0; i < k; i++) leaves *= rep ? N : N - i;
          if (leaves > ENUM_CAP) return null;
          const used = new Array(N).fill(false);
          const rec = (i, w) => {
            if (i === k) { fill(e); cb(w, e); return; }
            for (let j = 0; j < N; j++) {
              if (!rep && used[j]) continue;
              seq[i] = balls[j];
              if (rep) rec(i + 1, w / N); else { used[j] = true; rec(i + 1, w / (N - i)); used[j] = false; }
            }
          };
          rec(0, 1);
        }
        return "enumeration";
      },
    };
  };

  /* ---- bernoulli_matrix: n x n entries, entry = vals[1] w.p. p else vals[0]; variables aij, det, trace ---- */
  function det(M) {
    const n = M.length;
    if (n === 1) return M[0][0];
    if (n === 2) return M[0][0] * M[1][1] - M[0][1] * M[1][0];
    let s = 0;
    for (let j = 0; j < n; j++) {
      if (!M[0][j]) continue;
      const minor = M.slice(1).map(r => r.filter((_, c) => c !== j));
      s += (j % 2 ? -1 : 1) * M[0][j] * det(minor);
    }
    return s;
  }
  KINDS.bernoulli_matrix = function (p) {
    const n = p.n;
    if (!Number.isInteger(n) || n < 1 || n > 4) throw new Error("bernoulli_matrix: n must be 1..4");
    const P = [];
    for (let i = 0; i < n; i++) { P.push([]); for (let j = 0; j < n; j++) { const v = num(Array.isArray(p.p) ? p.p[i][j] : p.p, "p"); if (!(v >= 0 && v <= 1)) throw new Error("bernoulli_matrix: p must be in [0,1]"); P[i].push(v); } }
    const vals = p.vals ? p.vals.map(v => num(v, "vals")) : [0, 1];
    const vars = new Set(["det", "trace"]);
    for (let i = 1; i <= n; i++) for (let j = 1; j <= n; j++) vars.add(`a${i}${j}`);
    const M = P.map(r => r.map(() => 0));
    const fill = e => { let t = 0; for (let i = 0; i < n; i++) { t += M[i][i]; for (let j = 0; j < n; j++) e[`a${i + 1}${j + 1}`] = M[i][j]; } e.trace = t; e.det = det(M); };
    return {
      vars,
      sample(rng, e) { for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) M[i][j] = rng() < P[i][j] ? vals[1] : vals[0]; fill(e); },
      enumerate(cb) {
        const N = n * n, e = {};
        for (let m = 0; m < (1 << N); m++) {
          let w = 1;
          for (let t = 0; t < N; t++) { const i = (t / n) | 0, j = t % n, on = (m >> t) & 1; M[i][j] = vals[on]; w *= on ? P[i][j] : 1 - P[i][j]; }
          if (w > 0) { fill(e); cb(w, e); }
        }
        return "enumeration";
      },
    };
  };

  /* ---- custom_discrete: independent named variables {X:{values,probs}} or a joint table [{p, X, Y}] ---- */
  KINDS.custom_discrete = function (p) {
    if (p.vars && typeof p.vars === "object") {
      const names = Object.keys(p.vars);
      const dists = names.map(nm => {
        if (!isIdent(nm)) throw new Error(`variable name ${JSON.stringify(nm)} must be an identifier`);
        const d = p.vars[nm], vs = (d.values || []).map(v => num(v, nm + " value")), ps = (d.probs || []).map(v => num(v, nm + " prob"));
        if (!vs.length || vs.length !== ps.length) throw new Error(`${nm}: values and probs must have the same non-zero length`);
        const t = ps.reduce((a, b) => a + b, 0);
        if (Math.abs(t - 1) > 1e-9) throw new Error(`${nm}: probs sum to ${t}, not 1`);
        let c = 0; return { nm, vs, ps, cum: ps.map(v => (c += v)) };
      });
      return {
        vars: new Set(names),
        sample(rng, e) { for (const d of dists) e[d.nm] = d.vs[pickCdf(d.cum, rng() * d.cum[d.cum.length - 1])]; },
        enumerate(cb) {
          if (dists.reduce((a, d) => a * d.vs.length, 1) > ENUM_CAP) return null;
          const e = {};
          const rec = (i, w) => { if (i === dists.length) { cb(w, e); return; } const d = dists[i]; for (let j = 0; j < d.vs.length; j++) if (d.ps[j] > 0) { e[d.nm] = d.vs[j]; rec(i + 1, w * d.ps[j]); } };
          rec(0, 1);
          return "enumeration";
        },
      };
    }
    if (Array.isArray(p.joint) && p.joint.length) {
      const names = Object.keys(p.joint[0]).filter(k => k !== "p");
      for (const nm of names) if (!isIdent(nm)) throw new Error(`variable name ${JSON.stringify(nm)} must be an identifier`);
      const rows = p.joint.map(r => ({ p: num(r.p, "joint p"), v: names.map(nm => num(r[nm], nm)) }));
      const t = rows.reduce((a, r) => a + r.p, 0);
      if (Math.abs(t - 1) > 1e-9) throw new Error(`joint probabilities sum to ${t}, not 1`);
      let c = 0; const cum = rows.map(r => (c += r.p));
      const put = (e, r) => names.forEach((nm, i) => { e[nm] = r.v[i]; });
      return {
        vars: new Set(names),
        sample(rng, e) { put(e, rows[pickCdf(cum, rng() * c)]); },
        enumerate(cb) { const e = {}; for (const r of rows) if (r.p > 0) { put(e, r); cb(r.p, e); } return "enumeration"; },
      };
    }
    throw new Error("custom_discrete needs vars {X:{values,probs}} or joint [{p, X, ...}]");
  };

  /* ============================ measures ============================ */
  const MEASURES = new Set(["prob", "mean", "var", "cov"]);
  function prepare(spec, item) {
    if (!spec || typeof spec !== "object") throw new Error("sim must be an object");
    const make = KINDS[spec.kind];
    if (!make) throw new Error(`sim kind ${JSON.stringify(spec.kind)} unknown (${Object.keys(KINDS).join("|")})`);
    let params = spec.params || {};
    if (spec.kind === "area" && params.fromRegion) {
      const r = item && item.region ? (Array.isArray(item.region) ? item.region[params.fromRegion === true ? 0 : params.fromRegion] : item.region) : null;
      if (!r) throw new Error("area fromRegion: the item has no region");
      params = Object.assign({ space: r.space, event: r.event, given: r.given }, params);
    }
    const gen = make(params);
    const measure = params.measure || "prob";
    if (!MEASURES.has(measure)) throw new Error(`measure ${JSON.stringify(measure)} must be prob|mean|var|cov`);
    const pred = form => {
      if (form == null) return null;
      if (typeof form === "string") return { fn: compile(form, gen.vars), set: null };
      if (spec.kind === "area") return gen.regionPred(form);
      throw new Error("event/given must be an expression string");
    };
    const ev = measure === "prob" ? pred(params.event) : null;
    if (measure === "prob" && !ev) throw new Error("measure prob needs an event");
    const gv = pred(params.given);
    let f = null, g = null;
    if (measure === "mean" || measure === "var") { if (typeof params.expr !== "string") throw new Error(`measure ${measure} needs expr (string)`); f = compile(params.expr, gen.vars); }
    if (measure === "cov") { if (!Array.isArray(params.expr) || params.expr.length !== 2) throw new Error("measure cov needs expr [expr1, expr2]"); f = compile(params.expr[0], gen.vars); g = compile(params.expr[1], gen.vars); }
    return { gen, measure, ev, gv, f, g, params };
  }
  function makeAcc(P) {
    const s = { W: 0, H: 0, s1: 0, s2: 0, s3: 0, s4: 0, x: 0, y: 0, xy: 0, xx: 0, yy: 0, xxy: 0, xyy: 0, xxyy: 0 };
    const ev = P.ev && P.ev.fn, gv = P.gv && P.gv.fn, f = P.f, g = P.g, m = P.measure;
    function add(w, e) {
      if (gv && !gv(e)) return;
      s.W += w;
      if (m === "prob") { if (ev(e)) s.H += w; return; }
      if (m === "cov") {
        const a = f(e), b = g(e);
        s.x += w * a; s.y += w * b; s.xy += w * a * b; s.xx += w * a * a; s.yy += w * b * b;
        s.xxy += w * a * a * b; s.xyy += w * a * b * b; s.xxyy += w * a * a * b * b; return;
      }
      const v = f(e), v2 = v * v;
      s.s1 += w * v; s.s2 += w * v2; s.s3 += w * v2 * v; s.s4 += w * v2 * v2;
    }
    function result() {
      const W = s.W;
      if (!(W > 0)) return { est: NaN, se: NaN, nGiven: W };
      if (m === "prob") { const p = s.H / W; return { est: p, se: Math.sqrt(Math.max(p * (1 - p), 0) / W), nGiven: W }; }
      if (m === "cov") {
        const a = s.x / W, b = s.y / W, cov = s.xy / W - a * b;
        const e4 = s.xxyy / W - 2 * b * s.xxy / W - 2 * a * s.xyy / W + b * b * s.xx / W + a * a * s.yy / W + 4 * a * b * s.xy / W - 3 * a * a * b * b;
        return { est: cov, se: Math.sqrt(Math.max(e4 - cov * cov, 0) / W), nGiven: W };
      }
      const m1 = s.s1 / W, m2 = s.s2 / W, m3 = s.s3 / W, m4 = s.s4 / W, v = Math.max(m2 - m1 * m1, 0);
      if (m === "mean") return { est: m1, se: Math.sqrt(v / W), nGiven: W };
      const c4 = m4 - 4 * m1 * m3 + 6 * m1 * m1 * m2 - 3 * Math.pow(m1, 4);
      return { est: v, se: Math.sqrt(Math.max(c4 - v * v, 0) / W), nGiven: W };
    }
    return { add, result };
  }

  /* a stepping runner: run(k) advances k trials; result() any time */
  function create(spec, o) {
    o = o || {};
    const P = prepare(spec, o.item), rng = mulberry32(o.seed != null ? o.seed : (spec.seed != null ? spec.seed : DEFAULT_SEED));
    const acc = makeAcc(P), env = {};
    let n = 0;
    return {
      run(k) { for (let i = 0; i < k; i++) { P.gen.sample(rng, env); acc.add(1, env); } n += k; },
      result() { return Object.assign({ n }, acc.result()); },
      get n() { return n; },
    };
  }
  function run(spec, o) {
    o = o || {};
    const R = create(spec, o), N = o.trials || spec.trials || DEFAULT_TRIALS;
    R.run(N);
    return R.result();
  }
  /* the deterministic value: enumeration, exact polygon area, or quadrature */
  function compute(spec, o) {
    o = o || {};
    const P = prepare(spec, o.item);
    if (spec.kind === "area" && P.measure === "prob" && P.ev.set && (!P.gv || P.gv.set)) {
      const v = P.gen.exactProb(P.ev.set, P.gv && P.gv.set);
      if (v != null) return { value: v, method: "polygon", tol: 1e-9 };
    }
    const acc = makeAcc(P);
    let method;
    if (P.gen.enumerate) method = P.gen.enumerate((w, e) => acc.add(w, e));
    else if (P.gen.quadrature) method = P.gen.quadrature([P.ev, P.gv].filter(Boolean).map(x => x.fn), (w, e) => acc.add(w, e));
    if (!method) return { value: null, method: "none", tol: null };
    const out = { value: acc.result().est, method, tol: method === "enumeration" ? 1e-9 : 2e-4 };
    if (P.gen.norm != null) { out.norm = P.gen.norm; out.negative = P.gen.negative; }
    return out;
  }
  /* what tools/check_sim_specs.py asserts for every sim in the raw files */
  function check(spec, o) {
    o = o || {};
    const problems = [];
    let mc = null, computed = null;
    try {
      if (typeof spec.exact !== "number" || !isFinite(spec.exact)) problems.push("exact must be a finite number");
      computed = compute(spec, o);
      if (computed.norm != null && Math.abs(computed.norm - 1) > 1e-4) problems.push(`the pdf integrates to ${computed.norm}, not 1`);
      if (computed.negative) problems.push("the pdf is negative somewhere");
      if (computed.value != null && typeof spec.exact === "number") {
        const tol = computed.tol * Math.max(1, Math.abs(spec.exact));
        if (!(Math.abs(computed.value - spec.exact) <= tol)) problems.push(`${computed.method} gives ${computed.value}, exact says ${spec.exact}`);
      }
      mc = run(spec, o);   // exactly the button's first run
      if (typeof spec.exact === "number") {
        const band = 4 * Math.max(mc.se, 1 / Math.max(mc.nGiven, 1));
        if (!(Math.abs(mc.est - spec.exact) <= band)) problems.push(`simulation ${mc.est} +- ${mc.se} (n=${mc.n}) is more than 4 SE from exact ${spec.exact}`);
      }
      if (mc.nGiven < 1000) problems.push(`only ${mc.nGiven} trials met the condition (raise trials)`);
    } catch (e) { problems.push(e.message); }
    return { ok: problems.length === 0, problems, mc, computed };
  }

  /* ============================ UI ============================ */
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]));
  const grp = n => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  function digitsFor(se) { return Math.min(6, Math.max(3, Math.ceil(-Math.log10(Math.max(se, 1e-12))) + 1)); }
  const fmt = (v, d) => (isFinite(v) ? v.toFixed(d) : "—");
  const kfmt = n => n >= 1e6 ? (n / 1e6) + "M" : n >= 1e3 ? (n / 1e3) + "k" : String(n);

  function chartSvg(pts, exact, N, done) {
    const W = 320, H = 150, ML = 48, MR = 10, MT = 10, MB = 24, PW = W - ML - MR, PH = H - MT - MB;
    if (!pts.length) return "";
    const n0 = pts[0].n, lx0 = Math.log10(n0), lx1 = Math.log10(Math.max(N, n0 * 10));
    let lo = Infinity, hi = -Infinity;
    for (const p of pts) { if (isFinite(p.est)) { lo = Math.min(lo, p.est); hi = Math.max(hi, p.est); } }
    if (isFinite(exact)) { const se0 = pts[Math.min(2, pts.length - 1)].se || 0; lo = Math.min(lo, exact - 2.5 * se0); hi = Math.max(hi, exact + 2.5 * se0); }
    if (!(hi > lo)) { hi = lo + 1e-3; lo -= 1e-3; }
    const pad = (hi - lo) * 0.08; lo -= pad; hi += pad;
    const X = n => ML + (Math.log10(n) - lx0) / (lx1 - lx0) * PW, Y = v => MT + (hi - v) / (hi - lo) * PH;
    const f1 = v => Math.round(v * 10) / 10;
    let band = "";
    if (isFinite(exact)) {
      const up = pts.map(p => `${f1(X(p.n))} ${f1(Y(exact + 2 * (p.se || 0)))}`), dn = pts.slice().reverse().map(p => `${f1(X(p.n))} ${f1(Y(exact - 2 * (p.se || 0)))}`);
      band = `<path class="mc-band" d="M${up.join("L")}L${dn.join("L")}Z"/>`;
    }
    const line = `<polyline class="mc-line" points="${pts.filter(p => isFinite(p.est)).map(p => `${f1(X(p.n))},${f1(Y(p.est))}`).join(" ")}"/>`;
    const last = pts[pts.length - 1];
    let ax = "";
    for (let e = Math.ceil(lx0); e <= Math.floor(lx1); e++) { const x = f1(X(Math.pow(10, e))); ax += `<line class="mc-grid" x1="${x}" y1="${MT}" x2="${x}" y2="${MT + PH}"/><text class="mc-tl" x="${x}" y="${H - 8}" text-anchor="middle">${kfmt(Math.pow(10, e))}</text>`; }
    const d = Math.max(2, Math.min(5, Math.ceil(-Math.log10(hi - lo)) + 1));
    for (const v of [lo + pad, hi - pad]) ax += `<text class="mc-tl" x="${ML - 4}" y="${f1(Y(v) + 3)}" text-anchor="end">${v.toFixed(d)}</text>`;
    const ex = isFinite(exact) ? `<line class="mc-exact" x1="${ML}" y1="${f1(Y(exact))}" x2="${ML + PW}" y2="${f1(Y(exact))}"/><text class="mc-tl mc-tl-exact" x="${ML - 4}" y="${f1(Y(exact) + 3)}" text-anchor="end">${exact.toFixed(d)}</text>` : "";
    return `<svg class="mc-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" direction="ltr" role="img" aria-label="convergence">` +
      `<rect class="mc-bg" x="${ML}" y="${MT}" width="${PW}" height="${PH}"/>` + ax + band + ex + line +
      (isFinite(last.est) ? `<circle class="mc-dot${done ? " done" : ""}" cx="${f1(X(last.n))}" cy="${f1(Y(last.est))}" r="3"/>` : "") +
      `<text class="mc-tl" x="${ML + PW}" y="${H - 8}" text-anchor="end"></text></svg>`;
  }

  function mount(el, spec, o) {
    if (!el) return null;
    o = o || {};
    const doc = el.ownerDocument, win = doc.defaultView || root;
    const N = spec.trials || DEFAULT_TRIALS;
    const exact = typeof spec.exact === "number" ? spec.exact : NaN;
    el.innerHTML = `<div class="mc-box">` +
      `<div class="mc-head"><span class="mc-title">🎲 סימולציה</span>${spec.estimate ? `<bdi dir="ltr" class="mc-what">${esc(spec.estimate)}</bdi>` : ""}</div>` +
      `<p class="mc-desc">המחשב מגריל את הניסוי <bdi dir="ltr">${grp(N)}</bdi> פעמים. הקו הוא ההערכה המצטברת, והקו המקווקו הוא הערך המדויק.</p>` +
      `<button type="button" class="btn primary mc-run">🎲 הריצו סימולציה</button>` +
      `<div class="mc-chart" dir="ltr"></div><div class="mc-result" aria-live="polite"></div></div>`;
    const btn = el.querySelector(".mc-run"), chart = el.querySelector(".mc-chart"), out = el.querySelector(".mc-result");
    let runs = 0, busy = false;
    const raf = win.requestAnimationFrame ? cb => win.requestAnimationFrame(cb) : cb => win.setTimeout(cb, 16);
    const now = () => (win.performance && win.performance.now ? win.performance.now() : Date.now());
    btn.onclick = () => {
      if (busy) return;
      let R;
      try { R = create(spec, { item: o.item, seed: (spec.seed != null ? spec.seed : DEFAULT_SEED) + runs }); }
      catch (e) { out.innerHTML = `<div class="mc-err">הסימולציה לא הוגדרה כראוי (${esc(e.message)})</div>`; return; }
      busy = true; runs++; btn.disabled = true; btn.textContent = "⏳ מגריל…";
      const pts = [], cps = [];
      const n0 = Math.min(200, N);
      for (let i = 0; i <= 60; i++) cps.push(Math.round(n0 * Math.pow(N / n0, i / 60)));
      let ci = 0;
      const frame = () => {
        const t0 = now();
        while (R.n < N && now() - t0 < 10) {
          const target = Math.min(N, cps[ci] || N);
          R.run(Math.min(target - R.n, 5000));
          if (R.n >= target) { const r = R.result(); pts.push({ n: R.n, est: r.est, se: r.se }); while (ci < cps.length && cps[ci] <= R.n) ci++; }
        }
        const done = R.n >= N;
        chart.innerHTML = chartSvg(pts, exact, N, done);
        const r = R.result(), d = digitsFor(r.se);
        const near = isFinite(exact) && Math.abs(r.est - exact) <= 4 * Math.max(r.se, 1e-12);
        out.innerHTML =
          `<div class="mc-line1">הערכה: <bdi dir="ltr" class="mc-est">${fmt(r.est, d)} ± ${fmt(2 * r.se, d)}</bdi> <span class="mc-n">(<bdi dir="ltr">N = ${grp(R.n)}</bdi>)</span></div>` +
          (isFinite(exact) ? `<div class="mc-line2">ערך מדויק: <bdi dir="ltr">${esc(Region.nice(exact))}${Region.frac(exact) ? ` ≈ ${exact.toFixed(d)}` : ""}</bdi></div>` : "") +
          (spec.params && spec.params.given != null ? `<div class="mc-line3">התנאי התקיים ב-<bdi dir="ltr">${grp(r.nGiven)}</bdi> ניסויים, וההערכה מחושבת רק מהם.</div>` : "") +
          (done && isFinite(exact) ? `<div class="mc-verdict ${near ? "good" : "bad"}">${near ? "✓ הסימולציה מתיישבת עם הערך המדויק" : "⚠ סטייה גדולה מהצפוי"}</div>` : "") +
          (done ? `<div class="mc-note">הסימן <bdi dir="ltr">±</bdi> מציין פעמיים את שגיאת התקן (בערך <bdi dir="ltr">95%</bdi> ביטחון).</div>` : "");
        if (!done) { raf(frame); return; }
        busy = false; btn.disabled = false; btn.textContent = "🎲 הרצה נוספת (גרעין אחר)";
        el.dataset.done = String(runs);
      };
      raf(frame);
    };
    return { el };
  }

  const Sim = { run, create, compute, check, mount, mulberry32, KINDS: Object.keys(KINDS), DEFAULT_TRIALS, DEFAULT_SEED };
  root.Sim = Sim;
  if (typeof module !== "undefined" && module.exports) module.exports = Sim;
})(typeof window !== "undefined" ? window : globalThis);
