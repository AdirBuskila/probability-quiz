"use strict";
/* Area-method visualizer (window.Region) -- probability-only, app-local (not part of the factory template).
   A region spec (tools/RAW_SCHEMA.md, "Area regions"):
     { "space": {"x":[a,b], "y":[c,d]},          the sample-space rectangle (X,Y uniform on it)
       "event": [ineq, ...] | {"any":[[ineq..],[ineq..]]} | "expression",
       "given": same forms (optional; conditional probability P(event | given)),
       "labels": {"x":"X","y":"Y"}, "exact": 0.5, "caption": "text", "ticks": {"x":[..],"y":[..]} }
   ineq:  {"a":1,"b":1,"c":1,"op":"<"}            linear  a*x + b*y op c   (a, b default 0)
          {"expr":"x*y","op":"<","c":0.5}          nonlinear  expr op c  (tiny parser below, never eval)
   A list is an AND; {"any":[...]} is an OR of ANDs; a string is a boolean expression of x and y.
   Polygonal sets (every ineq linear) are clipped exactly from the rectangle (Sutherland-Hodgman), and a union
   is measured by inclusion-exclusion, so the shown area is exact. Anything nonlinear is drawn from a fine
   column grid (boundaries refined by bisection) and its area is shown with "≈".
   API: Region.figure(spec|[spec..]) -> HTML string (<div class="region-fig">..svg..</div>)
        Region.hydrate(rootEl)            renders every .region-fig[data-region='json'] inside rootEl
        Region.compute(spec, {nx,ny})     -> {omega, pE, pG, pEG, p, exactGeom}
        Region.check(spec)                -> list of problems (strings)
        Region.Expr.compile(src, allowedVars) -> env => number ; Region.Expr.constant("1/3") -> number
   Loadable in Node (module.exports) for tools/test_sim.js and tools/check_sim_specs.py. */
(function (root) {
  /* =============================== tiny expression language ===============================
     numbers, identifiers, + - * / % ^, unary -, ( ), f(args); comparisons < <= > >= == != (chains such as
     0<x<1 mean 0<x and x<1); and/or/not (also && || !). Comparisons and logic give 1 or 0.
     Functions: abs sqrt exp log ln floor ceil round min max sin cos. Constants: pi, e. No implicit product. */
  const FUNCS = { abs: Math.abs, sqrt: Math.sqrt, exp: Math.exp, log: Math.log, ln: Math.log, floor: Math.floor,
    ceil: Math.ceil, round: Math.round, min: Math.min, max: Math.max, sin: Math.sin, cos: Math.cos };
  const CONSTS = { pi: Math.PI, e: Math.E };
  const WORD_OPS = { and: "&&", or: "||", not: "!" };
  const CMP = new Set(["<", "<=", ">", ">=", "==", "!="]);

  function tokenize(src) {
    const out = []; let i = 0;
    const re = /\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(<=|>=|==|!=|&&|\|\||[-+*/%^(),<>!]))/y;
    while (i < src.length) {
      if (/^\s*$/.test(src.slice(i))) break;
      re.lastIndex = i;
      const m = re.exec(src);
      if (!m) throw new Error(`expression "${src}": unexpected character at ${i}: "${src.slice(i).trim()[0]}"`);
      i = re.lastIndex;
      if (m[1] != null) out.push({ t: "num", v: parseFloat(m[1]) });
      else if (m[2] != null) out.push(WORD_OPS[m[2]] ? { t: "op", v: WORD_OPS[m[2]] } : { t: "id", v: m[2] });
      else out.push({ t: "op", v: m[3] });
    }
    return out;
  }

  /* allowed: Set of variable names (null = any name, looked up at run time). Returns env => number. */
  function compile(src, allowed) {
    src = String(src);
    const toks = tokenize(src); let i = 0;
    const err = msg => new Error(`expression "${src}": ${msg}`);
    const peek = () => toks[i];
    const isOp = v => toks[i] && toks[i].t === "op" && toks[i].v === v;
    const expect = v => { if (!isOp(v)) throw err(`expected "${v}"`); i++; };
    function pOr() { let a = pAnd(); while (isOp("||")) { i++; const x = a, b = pAnd(); a = e => (x(e) || b(e)) ? 1 : 0; } return a; }
    function pAnd() { let a = pNot(); while (isOp("&&")) { i++; const x = a, b = pNot(); a = e => (x(e) && b(e)) ? 1 : 0; } return a; }
    function pNot() { if (isOp("!")) { i++; const a = pNot(); return e => a(e) ? 0 : 1; } return pCmp(); }
    function pCmp() {
      const first = pAdd(), parts = [];
      let left = first;
      while (peek() && peek().t === "op" && CMP.has(peek().v)) {
        const op = toks[i++].v, right = pAdd();
        parts.push(cmpFn(op, left, right)); left = right;
      }
      if (!parts.length) return first;
      if (parts.length === 1) return parts[0];
      return e => { for (const p of parts) if (!p(e)) return 0; return 1; };
    }
    function cmpFn(op, a, b) {
      switch (op) {
        case "<": return e => a(e) < b(e) ? 1 : 0;
        case "<=": return e => a(e) <= b(e) ? 1 : 0;
        case ">": return e => a(e) > b(e) ? 1 : 0;
        case ">=": return e => a(e) >= b(e) ? 1 : 0;
        case "==": return e => Math.abs(a(e) - b(e)) < 1e-9 ? 1 : 0;
        default: return e => Math.abs(a(e) - b(e)) < 1e-9 ? 0 : 1;
      }
    }
    function pAdd() {
      let a = pMul();
      while (isOp("+") || isOp("-")) { const op = toks[i++].v, x = a, b = pMul(); a = op === "+" ? e => x(e) + b(e) : e => x(e) - b(e); }
      return a;
    }
    function pMul() {
      let a = pUnary();
      while (isOp("*") || isOp("/") || isOp("%")) {
        const op = toks[i++].v, x = a, b = pUnary();
        a = op === "*" ? e => x(e) * b(e) : op === "/" ? e => x(e) / b(e) : e => x(e) % b(e);
      }
      return a;
    }
    function pUnary() {
      if (isOp("-")) { i++; const a = pUnary(); return e => -a(e); }
      if (isOp("+")) { i++; return pUnary(); }
      return pPow();
    }
    function pPow() {
      const a = pAtom();
      if (isOp("^")) { i++; const b = pUnary(); return e => Math.pow(a(e), b(e)); }
      return a;
    }
    function pAtom() {
      const t = toks[i++];
      if (!t) throw err("unexpected end");
      if (t.t === "num") { const v = t.v; return () => v; }
      if (t.t === "id") {
        if (isOp("(")) {
          const f = FUNCS[t.v];
          if (!f) throw err(`unknown function ${t.v}()`);
          i++;
          const args = [];
          if (!isOp(")")) { args.push(pOr()); while (isOp(",")) { i++; args.push(pOr()); } }
          expect(")");
          if (args.length === 1) { const a0 = args[0]; return e => f(a0(e)); }
          if (args.length === 2) { const a0 = args[0], a1 = args[1]; return e => f(a0(e), a1(e)); }
          return e => f.apply(null, args.map(a => a(e)));
        }
        const name = t.v;
        if (allowed ? allowed.has(name) : !(name in CONSTS)) return e => { const v = e[name]; if (v === undefined) throw err(`no value for ${name}`); return +v; };
        if (name in CONSTS) { const v = CONSTS[name]; return () => v; }
        throw err(`unknown name ${name} (allowed: ${[...allowed].join(", ") || "none"})`);
      }
      if (t.v === "(") { const a = pOr(); expect(")"); return a; }
      throw err(`unexpected "${t.v}"`);
    }
    const fn = pOr();
    if (i < toks.length) throw err(`unexpected "${toks[i].v}" after the end`);
    return fn;
  }
  const NOVARS = new Set();
  function constant(v) {
    if (typeof v === "number") return v;
    if (typeof v === "string") return compile(v, NOVARS)({});
    throw new Error("a constant must be a number or a constant expression string");
  }
  const Expr = { compile, constant, tokenize };

  /* =============================== sets of the plane =============================== */
  const XY = new Set(["x", "y"]);
  const LE_OPS = new Set(["<", "<="]), GE_OPS = new Set([">", ">="]);

  /* one inequality -> {lin, a, b, c} (meaning a*x + b*y <= c) or {lin:false, f(x,y)->bool} */
  function normIneq(q) {
    if (typeof q === "string") { const f = compile(q, XY); return { lin: false, f: (x, y) => !!f({ x, y }) }; }
    if (!q || typeof q !== "object") throw new Error("an inequality must be an object or an expression string");
    const op = q.op;
    if (!LE_OPS.has(op) && !GE_OPS.has(op)) throw new Error(`inequality op ${JSON.stringify(op)} must be < <= > >=`);
    const c = constant(q.c == null ? 0 : q.c);
    if (q.expr != null) {
      const g = compile(q.expr, XY), env = { x: 0, y: 0 };
      const f = LE_OPS.has(op) ? (x, y) => { env.x = x; env.y = y; return g(env) <= c; } : (x, y) => { env.x = x; env.y = y; return g(env) >= c; };
      return { lin: false, f };
    }
    let a = constant(q.a == null ? 0 : q.a), b = constant(q.b == null ? 0 : q.b), cc = c;
    if (!a && !b) throw new Error("linear inequality with a = b = 0");
    if (GE_OPS.has(op)) { a = -a; b = -b; cc = -cc; }
    return { lin: true, a, b, c: cc, f: (x, y) => a * x + b * y <= cc + 1e-12 };
  }
  /* event/given -> list of conjuncts (each a list of normalized inequalities) */
  function normSet(s) {
    if (s == null) return null;
    if (typeof s === "string") return [[normIneq(s)]];
    if (Array.isArray(s)) return [s.map(normIneq)];
    if (typeof s === "object" && Array.isArray(s.any)) return s.any.map(c => (Array.isArray(c) ? c : [c]).map(normIneq));
    throw new Error("event/given must be a list of inequalities, {any:[...]} or an expression string");
  }
  const conjPred = conj => (x, y) => { for (const q of conj) if (!q.f(x, y)) return false; return true; };
  function setPred(set) {
    if (!set) return () => true;
    const ps = set.map(conjPred);
    return (x, y) => { for (const p of ps) if (p(x, y)) return true; return false; };
  }
  const isLinearSet = set => !!set && set.every(c => c.every(q => q.lin));
  function normSpace(sp) {
    if (!sp || !Array.isArray(sp.x) || !Array.isArray(sp.y) || sp.x.length !== 2 || sp.y.length !== 2) throw new Error("space must be {x:[a,b], y:[c,d]}");
    const s = { x0: constant(sp.x[0]), x1: constant(sp.x[1]), y0: constant(sp.y[0]), y1: constant(sp.y[1]) };
    if (!(s.x1 > s.x0) || !(s.y1 > s.y0)) throw new Error("space ranges must be increasing");
    return s;
  }

  /* ---- exact polygons ---- */
  const rectPoly = s => [[s.x0, s.y0], [s.x1, s.y0], [s.x1, s.y1], [s.x0, s.y1]];   // counter-clockwise
  function clip(poly, q) {   // keep a*x + b*y <= c
    const out = [], n = poly.length, val = p => q.a * p[0] + q.b * p[1] - q.c;
    for (let i = 0; i < n; i++) {
      const P = poly[i], Q = poly[(i + 1) % n], vp = val(P), vq = val(Q);
      if (vp <= 0) out.push(P);
      if ((vp < 0 && vq > 0) || (vp > 0 && vq < 0)) { const t = vp / (vp - vq); out.push([P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])]); }
    }
    return out;
  }
  function polyArea(p) { let a = 0; for (let i = 0; i < p.length; i++) { const P = p[i], Q = p[(i + 1) % p.length]; a += P[0] * Q[1] - Q[0] * P[1]; } return Math.abs(a) / 2; }
  function conjPoly(conj, s) { let p = rectPoly(s); for (const q of conj) { p = clip(p, q); if (p.length < 3) return []; } return p; }
  /* area of a union of convex polygons (each conjunct) by inclusion-exclusion */
  function linearArea(set, s) {
    const n = set.length;
    if (n > 12) return null;
    let total = 0;
    for (let mask = 1; mask < (1 << n); mask++) {
      const conj = []; let k = 0;
      for (let i = 0; i < n; i++) if (mask & (1 << i)) { conj.push(...set[i]); k++; }
      const p = conjPoly(conj, s);
      if (p.length >= 3) total += (k % 2 ? 1 : -1) * polyArea(p);
    }
    return total;
  }
  /* intersection of two sets: OR over every pair of conjuncts */
  function andSets(A, B) { if (!A) return B; if (!B) return A; const out = []; for (const a of A) for (const b of B) out.push(a.concat(b)); return out; }

  /* ---- grid for nonlinear sets: per column, the y-intervals where pred holds (bisection-refined) ---- */
  function columnIntervals(pred, x, y0, y1, ny) {
    const out = [], h = (y1 - y0) / ny;
    let prevIn = pred(x, y0 + h * 0.5), start = prevIn ? y0 : null;
    for (let j = 1; j < ny; j++) {
      const y = y0 + h * (j + 0.5), on = pred(x, y);
      if (on !== prevIn) {
        let lo = y - h, hi = y;       // boundary in (lo, hi)
        for (let k = 0; k < 30; k++) { const m = (lo + hi) / 2; if (pred(x, m) === prevIn) lo = m; else hi = m; }
        const b = (lo + hi) / 2;
        if (on) start = b; else { out.push([start, b]); start = null; }
        prevIn = on;
      }
    }
    if (prevIn) out.push([start, y1]);
    return out;
  }
  function gridArea(pred, s, nx, ny) {
    const w = (s.x1 - s.x0) / nx; let a = 0;
    for (let i = 0; i < nx; i++) for (const [p, q] of columnIntervals(pred, s.x0 + w * (i + 0.5), s.y0, s.y1, ny)) a += (q - p) * w;
    return a;
  }
  function setArea(set, s, o) {
    if (isLinearSet(set)) { const a = linearArea(set, s); if (a != null) return { area: a, exact: true }; }
    return { area: gridArea(setPred(set), s, o.nx || 400, o.ny || 200), exact: false };
  }

  function prepare(spec) {
    if (!spec || typeof spec !== "object") throw new Error("region must be an object");
    const s = normSpace(spec.space);
    if (spec.event == null) throw new Error("region needs an event");
    return { s, E: normSet(spec.event), G: normSet(spec.given) };
  }
  function compute(spec, o) {
    o = o || {};
    const { s, E, G } = prepare(spec);
    const omega = (s.x1 - s.x0) * (s.y1 - s.y0);
    const e = setArea(E, s, o);
    const r = { omega, pE: e.area, exactGeom: e.exact };
    // a zero-area event (a line such as y = x): spec.lines declares it, so its area is exactly 0
    if (Array.isArray(spec.lines) && spec.lines.length && !G && e.area < 1e-9) { r.pE = 0; r.exactGeom = true; }
    if (G) {
      const g = setArea(G, s, o), eg = setArea(andSets(E, G), s, o);
      Object.assign(r, { pG: g.area, pEG: eg.area, p: g.area > 0 ? eg.area / g.area : NaN, exactGeom: e.exact && g.exact && eg.exact });
    } else r.p = e.area / omega;
    return r;
  }
  const KEYS = new Set(["space", "event", "given", "labels", "exact", "caption", "ticks", "lines"]);
  function check(spec) {
    const out = [];
    if (!spec || typeof spec !== "object" || Array.isArray(spec)) return ["region must be an object"];
    for (const k of Object.keys(spec)) if (!KEYS.has(k)) out.push(`region: unknown key ${k}`);
    try {
      const r = compute(spec, { nx: 1600, ny: 400 });
      if (spec.exact != null) {
        if (typeof spec.exact !== "number") out.push("region: exact must be a number");
        else {
          const tol = r.exactGeom ? 1e-9 : 2e-3;
          if (!(Math.abs(r.p - spec.exact) <= tol)) out.push(`region: computed ${r.exactGeom ? "polygon" : "grid"} probability ${r.p} != exact ${spec.exact}`);
        }
      }
    } catch (e) { out.push("region: " + e.message); }
    return out;
  }

  /* =============================== formatting =============================== */
  function frac(v, maxDen) {
    maxDen = maxDen || 10000;
    if (!isFinite(v)) return null;
    if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
    for (let d = 2; d <= maxDen; d++) { const n = Math.round(v * d); if (Math.abs(v - n / d) < 1e-12 * Math.max(1, Math.abs(v))) return `${n}/${d}`; }
    return null;
  }
  const dec = (v, k) => (Math.round(v * Math.pow(10, k)) / Math.pow(10, k)).toString();
  function nice(v, maxDen) { const f = frac(v, maxDen); return f || dec(v, 4); }
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));

  function ticksFor(a, b) {
    const r = b - a, steps = [0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 2.5, 5, 10, 25, 50, 100];
    let st = steps.find(t => r / t <= 5) || r / 4;
    const out = [];
    for (let v = Math.ceil(a / st - 1e-9) * st; v <= b + 1e-9; v += st) out.push(Math.round(v * 1e9) / 1e9);
    return out;
  }

  /* =============================== SVG =============================== */
  let UID = 0;
  function svgOf(spec) {
    const { s, E, G } = prepare(spec);
    const id = "rg" + (++UID);
    const rx = s.x1 - s.x0, ry = s.y1 - s.y0;
    let aspect = ry / rx; const clamp = Math.min(2.2, Math.max(1 / 2.2, aspect)); const squashed = clamp !== aspect; aspect = clamp;
    const PW = aspect <= 1 ? 260 : 260 / aspect, PH = PW * aspect;
    const ML = 40, MR = 18, MT = 14, MB = 34, W = ML + PW + MR, H = MT + PH + MB;
    const X = x => ML + (x - s.x0) / rx * PW, Y = y => MT + (s.y1 - y) / ry * PH;
    const f1 = v => Math.round(v * 100) / 100;
    const polyD = p => p.length < 3 ? "" : "M" + p.map(q => `${f1(X(q[0]))} ${f1(Y(q[1]))}`).join("L") + "Z";
    const NX = 180, NY = 160, cw = rx / NX;
    function setD(set) {
      if (!set) return "";
      let d = "";
      for (const conj of set) {
        if (conj.every(q => q.lin)) { d += polyD(conjPoly(conj, s)); continue; }
        const pr = conjPred(conj);
        for (let i = 0; i < NX; i++) {
          const xa = s.x0 + cw * i, xc = xa + cw / 2;
          const xl = f1(X(xa)), xr = f1(X(xa + cw) + 0.6);
          for (const [p, q] of columnIntervals(pr, xc, s.y0, s.y1, NY)) d += `M${xl} ${f1(Y(p))}H${xr}V${f1(Y(q))}H${xl}Z`;
        }
      }
      return d;
    }
    const lab = spec.labels || {};
    const tk = spec.ticks || {};
    const tx = (tk.x ? tk.x.map(constant) : ticksFor(s.x0, s.x1)), ty = (tk.y ? tk.y.map(constant) : ticksFor(s.y0, s.y1));
    const tl = v => frac(v, 12) || dec(v, 2);
    let g = "";
    // grid + ticks
    for (const v of tx) g += `<line class="rg-grid" x1="${f1(X(v))}" y1="${MT}" x2="${f1(X(v))}" y2="${f1(MT + PH)}"/><line class="rg-tick" x1="${f1(X(v))}" y1="${f1(MT + PH)}" x2="${f1(X(v))}" y2="${f1(MT + PH + 4)}"/><text class="rg-tl" x="${f1(X(v))}" y="${f1(MT + PH + 15)}" text-anchor="middle">${esc(tl(v))}</text>`;
    for (const v of ty) g += `<line class="rg-grid" x1="${ML}" y1="${f1(Y(v))}" x2="${f1(ML + PW)}" y2="${f1(Y(v))}"/><line class="rg-tick" x1="${ML - 4}" y1="${f1(Y(v))}" x2="${ML}" y2="${f1(Y(v))}"/><text class="rg-tl" x="${ML - 6}" y="${f1(Y(v) + 3.5)}" text-anchor="end">${esc(tl(v))}</text>`;
    // boundary lines of the linear inequalities (dashed, clipped to the plot)
    let lines = "";
    const seen = new Set();
    for (const set of [E, G]) if (set) for (const conj of set) for (const q of conj) if (q.lin) {
      const key = [q.a, q.b, q.c].map(v => v.toFixed(9)).join();
      if (seen.has(key)) continue; seen.add(key);
      const pts = [];
      if (Math.abs(q.b) > 1e-12) for (const x of [s.x0, s.x1]) pts.push([x, (q.c - q.a * x) / q.b]);
      if (Math.abs(q.a) > 1e-12) for (const y of [s.y0, s.y1]) pts.push([(q.c - q.b * y) / q.a, y]);
      const inside = pts.filter(p => p[0] >= s.x0 - 1e-9 && p[0] <= s.x1 + 1e-9 && p[1] >= s.y0 - 1e-9 && p[1] <= s.y1 + 1e-9);
      if (inside.length >= 2) {
        inside.sort((u, v) => u[0] - v[0] || u[1] - v[1]);
        const A = inside[0], B = inside[inside.length - 1];
        if (Math.hypot(A[0] - B[0], A[1] - B[1]) > 1e-9) lines += `<line class="rg-bound" x1="${f1(X(A[0]))}" y1="${f1(Y(A[1]))}" x2="${f1(X(B[0]))}" y2="${f1(Y(B[1]))}"/>`;
      }
    }
    // zero-area event: solid line(s) a*x + b*y = c, clipped to the plot
    let evLines = "";
    for (const q of (Array.isArray(spec.lines) ? spec.lines : [])) {
      const a = constant(q.a == null ? 0 : q.a), b = constant(q.b == null ? 0 : q.b), c = constant(q.c == null ? 0 : q.c), pts = [];
      if (Math.abs(b) > 1e-12) for (const x of [s.x0, s.x1]) pts.push([x, (c - a * x) / b]);
      if (Math.abs(a) > 1e-12) for (const y of [s.y0, s.y1]) pts.push([(c - b * y) / a, y]);
      const ins = pts.filter(p => p[0] >= s.x0 - 1e-9 && p[0] <= s.x1 + 1e-9 && p[1] >= s.y0 - 1e-9 && p[1] <= s.y1 + 1e-9).sort((u, v) => u[0] - v[0] || u[1] - v[1]);
      if (ins.length >= 2) { const A = ins[0], B = ins[ins.length - 1]; evLines += `<line class="rg-evline" x1="${f1(X(A[0]))}" y1="${f1(Y(A[1]))}" x2="${f1(X(B[0]))}" y2="${f1(Y(B[1]))}"/>`; }
    }
    const dE = setD(E), dG = G ? setD(G) : "", dEG = G ? setD(andSets(E, G)) : "";
    const svg =
      `<svg class="rg-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${f1(W)} ${f1(H)}" width="${f1(W)}" height="${f1(H)}" direction="ltr" role="img" aria-label="${esc(spec.caption || "region")}">` +
      `<defs><pattern id="${id}h" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate(45)"><line class="rg-hatch" x1="0" y1="0" x2="0" y2="7"/></pattern>` +
      `<clipPath id="${id}c"><rect x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/></clipPath></defs>` +
      `<rect class="rg-space" x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/>` + g +
      `<g clip-path="url(#${id}c)">` +
      (dE ? `<path class="rg-event${G ? " rg-event-soft" : ""}" d="${dE}"/>` : "") +
      (dG ? `<path class="rg-given" d="${dG}" fill="url(#${id}h)"/>` : "") +
      (dEG ? `<path class="rg-both" d="${dEG}"/>` : "") +
      (dG ? `<path class="rg-given-line" d="${dG}"/>` : "") + lines + evLines + `</g>` +
      `<rect class="rg-frame" x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/>` +
      `<text class="rg-ax" x="${f1(ML + PW + 4)}" y="${f1(MT + PH + 28)}" text-anchor="end">${esc(lab.x || "x")}</text>` +
      `<text class="rg-ax" x="${ML - 30}" y="${MT + 4}" text-anchor="start">${esc(lab.y || "y")}</text>` +
      `</svg>`;
    return { svg, squashed };
  }

  function figureOne(spec) {
    let out;
    try {
      const { svg, squashed } = svgOf(spec);
      const r = compute(spec);
      const ap = r.exactGeom ? "" : "≈ ";
      const sh = v => r.exactGeom ? nice(v) : dec(v, 4);
      const om = nice(r.omega, 100);
      let nums;
      if (r.pG != null) {
        nums = `<span>|Ω| = ${esc(om)}</span><span>S(A∩B) ${ap}= ${esc(sh(r.pEG))}</span><span>S(B) ${ap}= ${esc(sh(r.pG))}</span>` +
          `<span class="rg-p">P(A | B) = S(A∩B) / S(B) ${ap}= ${esc(sh(r.p))}</span>`;
      } else {
        nums = `<span>|Ω| = ${esc(om)}</span><span>S(A) ${ap}= ${esc(sh(r.pE))}</span><span class="rg-p">P(A) = S(A) / |Ω| ${ap}= ${esc(sh(r.p))}</span>`;
      }
      const exact = typeof spec.exact === "number"
        ? `<div class="rg-exact">התשובה המדויקת: <bdi dir="ltr">${esc(nice(spec.exact))}${(frac(spec.exact) && !Number.isInteger(spec.exact)) ? ` ≈ ${esc(dec(spec.exact, 4))}` : ""}</bdi></div>` : "";
      const legend = `<div class="rg-legend">` +
        `<span class="rg-key"><i class="rg-sw rg-sw-e${r.pG != null ? " soft" : ""}"></i>המאורע A</span>` +
        (r.pG != null ? `<span class="rg-key"><i class="rg-sw rg-sw-g"></i>התנאי B</span><span class="rg-key"><i class="rg-sw rg-sw-eg"></i>A∩B</span>` : "") +
        `</div>`;
      out = (spec.caption ? `<div class="rg-caption">${esc(spec.caption)}</div>` : "") +
        `<div class="rg-plot" dir="ltr">${svg}</div>` + legend +
        `<div class="rg-nums" dir="ltr">${nums}</div>` + exact +
        (squashed ? `<div class="rg-note">הציור אינו בקנה מידה אחיד בשני הצירים.</div>` : "");
    } catch (e) {
      out = `<div class="rg-error">לא ניתן לצייר את האזור (${esc(e.message)})</div>`;
    }
    return out;
  }
  /* full figure markup; a list of specs gives one figure per spec */
  function figure(spec) {
    const list = Array.isArray(spec) ? spec : [spec];
    return list.map(sp => `<div class="region-fig" data-rg="1">${figureOne(sp)}</div>`).join("");
  }
  function hydrate(el) {
    if (!el || !el.querySelectorAll) return 0;
    const hosts = [...el.querySelectorAll(".region-fig[data-region]:not([data-rg])")];
    if (el.matches && el.matches(".region-fig[data-region]:not([data-rg])")) hosts.unshift(el);
    for (const h of hosts) {
      h.setAttribute("data-rg", "1");
      let spec;
      try { spec = JSON.parse(h.getAttribute("data-region")); } catch (e) { h.innerHTML = `<div class="rg-error">לא ניתן לקרוא את האזור</div>`; continue; }
      const list = Array.isArray(spec) ? spec : [spec];
      h.innerHTML = list.map(figureOne).join("");
    }
    return hosts.length;
  }
  /* learn mode / course lessons write <div class="region-fig" data-region='{...}'></div>; render them as they appear */
  if (typeof document !== "undefined" && typeof MutationObserver !== "undefined") {
    const start = () => {
      hydrate(document.body);
      new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (n.nodeType === 1) hydrate(n); })
        .observe(document.body, { childList: true, subtree: true });
    };
    if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
  }

  const Region = { figure, hydrate, compute, check, Expr, frac, nice,
    _: { normSet, normSpace, setPred, isLinearSet, linearArea, andSets, columnIntervals, conjPoly, polyArea } };
  root.Region = Region;
  if (typeof module !== "undefined" && module.exports) module.exports = Region;
})(typeof window !== "undefined" ? window : globalThis);
