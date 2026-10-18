// Render a few regions through the page's region.js and print the computed probability + a text dump of the figure.
const fs = require("fs");
const path = require("path");
const Region = require(path.join(__dirname, "..", "..", "region.js"));
const picks = [["25A-A", "1", "ג"], ["24S-B", "1", "ג"], ["25B-A", "1", "ד"], ["24S-A", "1", "ב"]];
for (const [code, num, part] of picks) {
  const d = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "raw", code + ".json"), "utf8"));
  const q = d.questions.find(x => String(x.num) === num && x.part === part);
  const regs = Array.isArray(q.region) ? q.region : [q.region];
  regs.forEach((r, i) => {
    const c = Region.compute(r, { nx: 1600, ny: 400 });
    const html = Region.figure(r);
    const txt = String(html).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
    console.log(code, num + part, "region" + i, c.exactGeom ? "polygon" : "grid", "p=" + c.p.toFixed(6), "exact=" + r.exact);
    console.log("   figure text:", txt.slice(0, 260));
  });
}
