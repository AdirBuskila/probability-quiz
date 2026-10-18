// Companion of check.py: runs the page's own sim.js / region.js (in Node) on the course's sims and regions.
// stdin: [{where, type:"sim"|"region", spec, expect}]  ->  stdout: [{where, type, ok, summary}]
const path = require("path");
const ROOT = path.resolve(__dirname, "..", "..", "..", "..");
const Region = require(path.join(ROOT, "region.js"));
const Sim = require(path.join(ROOT, "sim.js"));
let input = "";
process.stdin.on("data", d => { input += d; });
process.stdin.on("end", () => {
  const out = [];
  for (const j of JSON.parse(input)) {
    let ok = true, summary = "";
    try {
      if (j.type === "sim") {
        const c = Sim.check(j.spec, { item: {} });
        const mc = c.mc || {}, cp = c.computed || {};
        ok = c.ok && (j.expect == null || Math.abs(j.spec.exact - j.expect) < 1e-9);
        summary = `sim.js ok=${c.ok} mc=${(+mc.est).toFixed(5)} se=${(+mc.se).toFixed(5)} computed=${cp.value != null ? (+cp.value).toFixed(6) : "-"} exact=${j.spec.exact.toFixed(6)}` + (c.ok ? "" : " " + c.problems.join(";"));
      } else {
        const problems = Region.check(j.spec);
        const r = Region.compute(j.spec, { nx: 1600, ny: 400 });
        ok = problems.length === 0 && (j.expect == null || Math.abs(r.p - j.expect) < 2e-3);
        summary = `region.js p=${r.p.toFixed(6)} ${j.expect == null ? "" : "expect=" + j.expect.toFixed(6)} ${problems.join(";")}`;
      }
    } catch (e) { ok = false; summary = "error " + e.message; }
    out.push({ where: j.where, type: j.type, ok, summary });
  }
  process.stdout.write(JSON.stringify(out));
});
