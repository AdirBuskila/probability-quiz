// Node driver for tools/check_sim_specs.py: reads [{where, type:"sim"|"region", spec, item?}] as JSON on stdin,
// writes [{where, ok, problems, summary}] as JSON on stdout. Uses the very files the page loads (sim.js, region.js).
const path = require("path");
const Region = require(path.join(__dirname, "..", "region.js"));
const Sim = require(path.join(__dirname, "..", "sim.js"));

let input = "";
process.stdin.on("data", d => { input += d; });
process.stdin.on("end", () => {
  const jobs = JSON.parse(input), out = [];
  for (const j of jobs) {
    if (j.type === "region") {
      const problems = Region.check(j.spec);
      let summary = "";
      try { const r = Region.compute(j.spec, { nx: 1600, ny: 400 }); summary = `${r.exactGeom ? "polygon" : "grid"} p=${r.p.toFixed(6)}` + (typeof j.spec.exact === "number" ? ` exact=${j.spec.exact}` : " (no exact)"); } catch (e) { summary = "error"; }
      out.push({ where: j.where, ok: problems.length === 0, problems, summary });
    } else {
      const c = Sim.check(j.spec, { item: j.item });
      const mc = c.mc || {}, cp = c.computed || {};
      out.push({ where: j.where, ok: c.ok, problems: c.problems,
        summary: `${j.spec.kind} mc=${isFinite(mc.est) ? mc.est.toFixed(5) : "-"} se=${isFinite(mc.se) ? mc.se.toFixed(5) : "-"} n=${mc.n || 0}` +
          ` ${cp.method || "-"}=${cp.value != null ? (+cp.value).toFixed(7) : "-"} exact=${j.spec.exact}` });
    }
  }
  process.stdout.write(JSON.stringify(out));
  process.exit(out.every(r => r.ok) ? 0 : 1);
});
