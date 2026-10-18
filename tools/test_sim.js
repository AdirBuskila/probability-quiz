// Unit tests for sim.js + region.js (Node, no browser):  node tools/test_sim.js
// Every generator kind runs on hand-made specs with known exact answers; the simulation must land within
// 4 standard errors, the deterministic compute (enumeration / polygon / quadrature) must match, and polygonal
// region areas must equal the exact value. Seeds are fixed, so the run is deterministic. Prints ASCII only.
const path = require("path");
const Region = require(path.join(__dirname, "..", "region.js"));
const Sim = require(path.join(__dirname, "..", "sim.js"));

let fail = 0;
function assert(cond, msg) { console.log((cond ? "  ok  " : "FAIL  ") + msg); if (!cond) fail++; }
const close = (a, b, t) => Math.abs(a - b) <= t;

/* ---------- expression parser ---------- */
console.log("expr");
{
  const C = Region.Expr.compile;
  assert(C("2+3*4^2")({}) === 50, "precedence 2+3*4^2 = 50");
  assert(C("-x^2", new Set(["x"]))({ x: 3 }) === -9, "-x^2 = -(x^2)");
  assert(C("0<x<1", new Set(["x"]))({ x: 0.5 }) === 1 && C("0<x<1", new Set(["x"]))({ x: 2 }) === 0, "chained comparison");
  assert(C("sum % 3 == 0 and not d1 == d2", new Set(["sum", "d1", "d2"]))({ sum: 9, d1: 1, d2: 2 }) === 1, "mod / and / not");
  assert(C("max(x, y) <= 1/2 || abs(x-y) > 0.9", new Set(["x", "y"]))({ x: 0.1, y: 0.4 }) === 1, "functions and ||");
  assert(close(Region.Expr.constant("ln(2)/2 + 1/2"), 0.5 + Math.LN2 / 2, 1e-15), "constant expression");
  let threw = false; try { C("x + z", new Set(["x"])); } catch (e) { threw = /unknown name z/.test(e.message); }
  assert(threw, "unknown variable is a compile error");
  threw = false; try { C("alert(1)", new Set()); } catch (e) { threw = /unknown function/.test(e.message); }
  assert(threw, "unknown function is a compile error (no eval)");
  threw = false; try { C("x;y", new Set(["x", "y"])); } catch (e) { threw = true; }
  assert(threw, "stray characters rejected");
}

/* ---------- region geometry ---------- */
console.log("region");
const U2 = { x: [0, 1], y: [0, 1] };
const regionCases = [
  ["P(X+Y<1)", { space: U2, event: [{ a: 1, b: 1, c: 1, op: "<" }] }, 1 / 2, true],
  ["P(|X-Y|<1/4) = 7/16", { space: U2, event: [{ a: 1, b: -1, c: 0.25, op: "<" }, { a: 1, b: -1, c: -0.25, op: ">" }] }, 7 / 16, true],
  ["P(|X-Y|>1/4) union = 9/16", { space: U2, event: { any: [[{ a: 1, b: -1, c: 0.25, op: ">" }], [{ a: 1, b: -1, c: -0.25, op: "<" }]] } }, 9 / 16, true],
  ["P(X<1/2 | X+Y>1) = 1/4", { space: U2, event: [{ a: 1, c: 0.5, op: "<" }], given: [{ a: 1, b: 1, c: 1, op: ">" }] }, 1 / 4, true],
  ["U(0,1)xU(0,2): P(Y<X) = 1/4", { space: { x: [0, 1], y: [0, 2] }, event: [{ a: -1, b: 1, c: 0, op: "<" }] }, 1 / 4, true],
  ["overlapping union by inclusion-exclusion = 3/4", { space: U2, event: { any: [[{ a: 1, c: 0.5, op: "<" }], [{ b: 1, c: 0.5, op: "<" }]] } }, 3 / 4, true],
  ["P(XY<1/2) = 1/2 + ln2/2 (grid)", { space: U2, event: [{ expr: "x*y", op: "<", c: 0.5 }] }, 0.5 + Math.LN2 / 2, false],
  ["P(Y > X^2) = 2/3 (grid)", { space: U2, event: [{ expr: "y-x^2", op: ">", c: 0 }] }, 2 / 3, false],
];
for (const [name, spec, ex, poly] of regionCases) {
  const r = Region.compute(spec, { nx: 1600, ny: 400 });
  assert(r.exactGeom === poly && close(r.p, ex, poly ? 1e-12 : 1e-3), `${name}: ${poly ? "polygon" : "grid"} p=${r.p.toFixed(6)}`);
  assert(Region.check(Object.assign({ exact: ex }, spec)).length === 0, `${name}: Region.check passes with exact`);
  const html = Region.figure(spec);
  assert(/<svg class="rg-svg"/.test(html) && /class="rg-event/.test(html) && !/rg-error/.test(html), `${name}: figure renders an svg with the event`);
}
assert(Region.check({ space: U2, event: [{ a: 1, b: 1, c: 1, op: "<" }], exact: 0.4 }).length === 1, "a wrong region exact is reported");
assert(/rg-given/.test(Region.figure(regionCases[3][1])) && /rg-both/.test(Region.figure(regionCases[3][1])), "conditional figure has the hatched given and the intersection");
assert(/rg-error/.test(Region.figure({ space: U2, event: [{ a: 1, op: "~" }] })), "a bad region renders an error box, not a crash");

/* ---------- simulations, one or more per kind ---------- */
console.log("sim");
const simCases = [
  ["area P(X+Y<1)", { kind: "area", params: { space: U2, event: [{ a: 1, b: 1, c: 1, op: "<" }] }, exact: 1 / 2 }, "polygon"],
  ["area P(XY<1/2) string event", { kind: "area", params: { space: U2, event: "x*y < 1/2" }, exact: 0.5 + Math.LN2 / 2 }, "quadrature"],
  ["area P(X<1/2 | X+Y>1)", { kind: "area", params: { space: U2, event: [{ a: 1, c: 0.5, op: "<" }], given: [{ a: 1, b: 1, c: 1, op: ">" }] }, exact: 1 / 4 }, "polygon"],
  ["area E[XY] = 1/4", { kind: "area", params: { space: U2, measure: "mean", expr: "x*y" }, exact: 1 / 4 }, "quadrature"],
  ["area Var(XY) = 7/144", { kind: "area", params: { space: U2, measure: "var", expr: "x*y" }, exact: 7 / 144 }, "quadrature"],
  ["area E[max | X+Y<1] = 1/2", { kind: "area", params: { space: U2, measure: "mean", expr: "max(x,y)", given: "x+y<1" }, exact: 1 / 2 }, "quadrature"],
  ["pdf f=2x: P(X<1/2) = 1/4", { kind: "pdf", params: { pieces: [{ from: 0, to: 1, expr: "2*x" }], event: "x < 1/2" }, exact: 1 / 4 }, "quadrature"],
  ["pdf f=2x: E[X] = 2/3", { kind: "pdf", params: { pieces: [{ from: 0, to: 1, expr: "2*x" }], measure: "mean", expr: "x" }, exact: 2 / 3 }, "quadrature"],
  ["pdf piecewise: P(X>1 | X>1/2) = 3/7", { kind: "pdf", params: { pieces: [{ from: 0, to: 1, expr: "x/2" }, { from: 1, to: 2, expr: "3/4" }], event: "x > 1", given: "x > 1/2" }, exact: 0.75 / (0.75 + 0.1875) }, "quadrature"],
  ["pdf singular f=-ln x: P(X<1/4)", { kind: "pdf", params: { pieces: [{ from: 0, to: 1, expr: "-ln(x)" }], event: "x<1/4" }, exact: 0.25 - 0.25 * Math.log(0.25) }, "quadrature"],
  ["circuit 2-of-3 (p=0.9)", { kind: "circuit", params: { network: { type: "kofn", k: 2, children: [{ type: "comp", id: "A", p: 0.9 }, { type: "comp", id: "B", p: 0.9 }, { type: "comp", id: "C", p: 0.9 }] }, event: "S" }, exact: 3 * 0.81 - 2 * 0.729 }, "enumeration"],
  ["circuit series(A, parallel(B,C)) | B works", { kind: "circuit", params: { network: { type: "series", children: [{ type: "comp", id: "A", p: 0.8 }, { type: "parallel", children: [{ type: "comp", id: "B", p: 0.5 }, { type: "comp", id: "C", p: 0.6 }] }] }, event: "S", given: "B" }, exact: 0.8 }, "enumeration"],
  ["circuit bridge p=1/2 = 1/2", { kind: "circuit", params: { edges: [{ id: "Q1", from: "s", to: "a", p: 0.5 }, { id: "Q2", from: "s", to: "b", p: 0.5 }, { id: "Q3", from: "a", to: "b", p: 0.5 }, { id: "Q4", from: "a", to: "t", p: 0.5 }, { id: "Q5", from: "b", to: "t", p: 0.5 }], source: "s", sink: "t", event: "S" }, exact: 0.5 }, "enumeration"],
  ["circuit P(Q1 | S) (Bayes)", { kind: "circuit", params: { network: { type: "parallel", children: [{ type: "comp", id: "Q1", p: 0.5 }, { type: "comp", id: "Q2", p: 0.5 }] }, event: "Q1", given: "S" }, exact: 2 / 3 }, "enumeration"],
  ["dice two dice sum 7 = 1/6", { kind: "dice", params: { n: 2, event: "sum == 7" }, exact: 1 / 6 }, "enumeration"],
  ["dice sum divisible by 3 and d1<d2", { kind: "dice", params: { n: 2, event: "sum % 3 == 0 and d1 < d2" }, exact: 5 / 36 }, "enumeration"],
  ["dice biased die E[d1] = 4.5", { kind: "dice", params: { n: 1, weights: [1, 1, 1, 1, 1, 5], measure: "mean", expr: "d1" }, exact: (1 + 2 + 3 + 4 + 5 + 30) / 10 }, "enumeration"],
  ["urn without replacement: 2 red of 2 from 3R5B = 3/28", { kind: "urn", params: { counts: { red: 3, black: 5 }, draws: 2, replace: false, event: "red == 2" }, exact: 3 / 28 }, "enumeration"],
  ["urn with replacement: 2nd red | 1st red = 3/8", { kind: "urn", params: { counts: { red: 3, black: 5 }, draws: 2, replace: true, event: "red_2 == 1", given: "red_1 == 1" }, exact: 3 / 8 }, "enumeration"],
  ["urn without replacement: 2nd red | 1st red = 2/7", { kind: "urn", params: { counts: { red: 3, black: 5 }, draws: 2, event: "red_2", given: "red_1" }, exact: 2 / 7 }, "enumeration"],
  ["urn digits 1..9 no replacement, 2-digit number even = 4/9", { kind: "urn", params: { values: [1, 2, 3, 4, 5, 6, 7, 8, 9], draws: 2, event: "v2 % 2 == 0" }, exact: 4 / 9 }, "enumeration"],
  ["bernoulli 2x2 p=1/2: P(det=0) = 10/16", { kind: "bernoulli_matrix", params: { n: 2, p: 0.5, event: "det == 0" }, exact: 10 / 16 }, "enumeration"],
  ["bernoulli 2x2 p=1/2: E[det] = 0", { kind: "bernoulli_matrix", params: { n: 2, p: 0.5, measure: "mean", expr: "det" }, exact: 0 }, "enumeration"],
  ["bernoulli 2x2 p=1/2: Var(det) = 3/8", { kind: "bernoulli_matrix", params: { n: 2, p: 0.5, measure: "var", expr: "det" }, exact: 3 / 8 }, "enumeration"],
  ["bernoulli 2x2 p=1/2: cov(det, trace) = 1/4", { kind: "bernoulli_matrix", params: { n: 2, p: 0.5, measure: "cov", expr: ["det", "trace"] }, exact: 1 / 4 }, "enumeration"],
  ["bernoulli 2x2 joint pmf P(det=1, trace=2) = 3/16", { kind: "bernoulli_matrix", params: { n: 2, p: 0.5, event: "det == 1 and trace == 2" }, exact: 3 / 16 }, "enumeration"],
  ["custom_discrete cov(X, X+Y) = Var X", { kind: "custom_discrete", params: { vars: { X: { values: [0, 1], probs: [0.7, 0.3] }, Y: { values: [1, 2, 3], probs: [0.2, 0.5, 0.3] } }, measure: "cov", expr: ["X", "X+Y"] }, exact: 0.21 }, "enumeration"],
  ["custom_discrete joint table P(X=Y)", { kind: "custom_discrete", params: { joint: [{ p: 0.1, X: 0, Y: 0 }, { p: 0.4, X: 0, Y: 1 }, { p: 0.2, X: 1, Y: 0 }, { p: 0.3, X: 1, Y: 1 }], event: "X == Y" }, exact: 0.4 }, "enumeration"],
];
for (const [name, spec, method] of simCases) {
  const c = Sim.check(spec);
  const mc = c.mc || {}, cp = c.computed || {};
  assert(c.ok, `${name}: mc=${(+mc.est).toFixed(5)} se=${(+mc.se).toFixed(5)} computed=${cp.value != null ? (+cp.value).toFixed(7) : "-"} ${c.problems.join("; ")}`);
  assert(cp.method === method, `${name}: computed by ${method} (got ${cp.method})`);
}
/* the checker catches a wrong key, both ways */
{
  const bad = Sim.check({ kind: "dice", params: { n: 2, event: "sum == 7" }, exact: 0.2 });
  assert(!bad.ok && bad.problems.length >= 2, "a wrong exact fails both the enumeration and the 4-SE check");
  const badPdf = Sim.check({ kind: "pdf", params: { pieces: [{ from: 0, to: 1, expr: "3*x" }], event: "x<1/2" }, exact: 0.25 });
  assert(!badPdf.ok && badPdf.problems.some(p => /integrates/.test(p)), "an unnormalized pdf is reported");
  const badExpr = Sim.check({ kind: "dice", params: { n: 2, event: "summ == 7" }, exact: 1 / 6 });
  assert(!badExpr.ok && /unknown name summ/.test(badExpr.problems.join()), "a typo in a predicate is reported");
}
/* determinism + fromRegion */
{
  const s = { kind: "area", params: { space: U2, event: "x+y<1" }, exact: 0.5 };
  const a = Sim.run(s, { trials: 5000 }), b = Sim.run(s, { trials: 5000 });
  assert(a.est === b.est, "same seed -> same estimate (mulberry32)");
  const c = Sim.run(s, { trials: 5000, seed: 7 });
  assert(c.est !== a.est, "another seed -> another stream");
  const item = { region: { space: U2, event: [{ a: 1, b: 1, c: 1, op: "<" }], given: [{ a: 1, c: 0.5, op: ">" }] } };
  const fr = Sim.check({ kind: "area", params: { fromRegion: true }, exact: 1 / 4 }, { item });
  assert(fr.ok && fr.computed.method === "polygon", "area fromRegion reuses the item's region (P(X+Y<1 | X>1/2) = 1/4)");
  const R = Sim.create(s); R.run(1000); R.run(4000);
  assert(R.result().est === a.est, "chunked runs give the same stream as one run");
}

console.log(fail ? `\n${fail} FAILED` : "\ntest_sim: all ok");
process.exit(fail ? 1 : 0);
