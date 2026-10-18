// Plain-node unit tests for the render-time bidi fixes (window.Bidi in normalize.js):  node tools/test_bidi.js
const assert = require("assert");
const path = require("path");
global.window = {};
require(path.join(__dirname, "..", "normalize.js"));
const B = global.window.Bidi;
assert.ok(B && typeof B.render === "function", "Bidi API");

const label = l => `<bdi class="ltr nw opt-label" dir="ltr">${l}</bdi>`;
const ltr = t => `<bdi class="ltr nw" dir="ltr">${t}</bdi>`;

// option-label lines: the label (period included) is one LTR isolate at the line start
assert.strictEqual(B.render("a. סכום x ו-y"), `${label("a.")} סכום ${ltr("x")} ו-${ltr("y")}`);
assert.strictEqual(B.render("שאלה:<br>c. x עם סימן הפוך"), `שאלה:<br>${label("c.")} ${ltr("x")} עם סימן הפוך`);
assert.strictEqual(B.render("e. אף אחת מהתשובות לעיל לא נכונה"), `${label("e.")} אף אחת מהתשובות לעיל לא נכונה`);
assert.strictEqual(B.render("x<br>(b) שלום"), `${ltr("x")}<br>${label("(b)")} שלום`);
const many = B.render("שאלה<br>a. סכום x ו-y<br>b. מכפלת x ו-y<br>c. x עם סימן הפוך<br>e. אף אחת מהתשובות לעיל לא נכונה");
assert.strictEqual((many.match(/opt-label/g) || []).length, 4, "four labels");
assert.ok(!/(^|<br>)[a-e]\./.test(many), "no bare label left at a line start");

// idempotent
assert.strictEqual(B.render(B.render("a. סכום x ו-y")), B.render("a. סכום x ו-y"));

// a sentence ending with a formula keeps its period inside the formula's LTR isolate
const f = '<span class="math-inline"><math><mi>x</mi></math></span>';
assert.strictEqual(B.render(`הערך הוא ${f}.`), `הערך הוא <span class="math-run" dir="ltr">${f}.</span>`);
assert.strictEqual(B.render(`הערך הוא ${f}.<br>שורה`), `הערך הוא <span class="math-run" dir="ltr">${f}.</span><br>שורה`);
// formulas chained by punctuation form one run
assert.ok(B.render(`${f}, ${f}`).startsWith('<span class="math-run" dir="ltr">'));
// a period mid-sentence is left alone
assert.strictEqual(B.render(`${f}. אחר כך`), `${f}. אחר כך`);

// code blocks, inline code and math are untouched
const pre = '<pre class="code-block" dir="ltr"><code>a. x\nb. y</code></pre>';
assert.strictEqual(B.render(pre), pre);
assert.strictEqual(B.render(`שלום<br>${pre}`), `שלום<br>${pre}`);
const code = '<code class="tok" dir="ltr">a. x</code>';
assert.strictEqual(B.render(`<br>${code} ו`), `<br>${code} ו`);
const math = '<span class="math-block"><math><mi>a</mi><mo>.</mo></math></span>';
assert.strictEqual(B.render(math), math);

// plain Hebrew and a Latin-free line are unchanged
assert.strictEqual(B.render("שלום עולם."), "שלום עולם.");
assert.ok(!B.render("e.g. משהו").includes("opt-label"), "e.g. is not an option label");

// plain-text factorial: the "!" stays inside the LTR isolate (it used to render "!4")
assert.strictEqual(B.render("יש 4! אפשרויות"), `יש ${ltr("4!")} אפשרויות`);
assert.strictEqual(B.render("לחשב 2·5! במקום 2·4!, כי"), `לחשב ${ltr("2·5!")} במקום ${ltr("2·4!")}, כי`);
assert.strictEqual(B.render("יש n! אפשרויות"), `יש ${ltr("n!")} אפשרויות`);
// product / arithmetic chains are one isolate, leading and trailing operators included; a sentence-final period stays outside
assert.strictEqual(B.render("שווה …=120.·6·5·4 ועוד"), `שווה ${ltr("…=120.·6·5·4")} ועוד`);
assert.strictEqual(B.render("סה\"כ x + y = z יוצא"), `סה"כ ${ltr("x + y = z")} יוצא`);
assert.strictEqual(B.render("התוצאה היא 5."), `התוצאה היא ${ltr("5")}.`);
assert.strictEqual(B.render("יש 6·5·4."), `יש ${ltr("6·5·4")}.`);
// a ? or : after a digit stays outside, at the RTL end
assert.strictEqual(B.render("מתחילות ב: 1 או ב: 2?"), `מתחילות ב: ${ltr("1")} או ב: ${ltr("2")}?`);
assert.strictEqual(B.render("הערך 3:"), `הערך ${ltr("3")}:`);
// brackets: an all-LTR pair travels with its content; a pair that spans Hebrew stays outside so it mirrors as a pair
assert.strictEqual(B.render("הערך (n+1) הוא"), `הערך ${ltr("(n+1)")} הוא`);
assert.strictEqual(B.render("מתקיים [1,2,3] כך"), `מתקיים ${ltr("[1,2,3]")} כך`);
assert.strictEqual(B.render("כל תמורה: [אות ראשונה: 1 או 2] ואחריה"), `כל תמורה: [אות ראשונה: ${ltr("1")} או ${ltr("2")}] ואחריה`);
assert.strictEqual(B.render("P(n,m) (0 אם m>n)"), `${ltr("P(n,m)")} (${ltr("0")} אם ${ltr("m>n")})`);
// a Hebrew prefix letter before inline math stays outside the formula (RTL start)
assert.strictEqual(B.render(`אז ${f} ו-${f} הם`), `אז ${f} ו-${f} הם`);
assert.strictEqual(B.render("אז ו-x הם"), `אז ו-${ltr("x")} הם`);
assert.strictEqual(B.render("אז ב-3 ול-n"), `אז ב-${ltr("3")} ול-${ltr("n")}`);
// question-id chips (isolated LTR buttons) inside parentheses are left alone
const chip = id => `<button type="button" class="qref" data-q="${id}">${id}</button>`;
assert.strictEqual(B.render(`ראו (${chip("19A-A-Q1a")}), ועוד`), `ראו (${chip("19A-A-Q1a")}), ועוד`);
assert.strictEqual(B.render(`דומה (${chip("22A-A-Q2c")}, ${chip("22A-B-Q1b")}).`), `דומה (${chip("22A-A-Q2c")}, ${chip("22A-B-Q1b")}).`);
// idempotent on the new cases
for (const s of ["יש 4! אפשרויות", "שווה …=120.·6·5·4 ועוד", "P(n,m) (0 אם m>n)", "[אות ראשונה: 1 או 2] ואחריה"]) assert.strictEqual(B.render(B.render(s)), B.render(s));

// a lone ? or ! after a formula at a line end is glued to it (word joiner inside the run): it cannot wrap onto its own line
assert.strictEqual(B.render(`האם ${f}?`), `האם <span class="math-run" dir="ltr">${f}\u2060?</span>`);
assert.strictEqual(B.render(`מהו ${f}?<br>עוד`), `מהו <span class="math-run" dir="ltr">${f}\u2060?</span><br>עוד`);
assert.strictEqual(B.render(`${f}? אחר`), `${f}? אחר`);
// prefix letter + a plain-text formula: the prefix stays outside, at the RTL start
assert.strictEqual(B.render("ב-x = 3 כי"), `ב-${ltr("x = 3")} כי`);
assert.strictEqual(B.render("x = 3 ב-"), `${ltr("x = 3")} ב-`);
// plain Unicode math inside Hebrew is one LTR run, primes included (ASCII ' and U+2032)
assert.strictEqual(B.render("נגזרת 1/(ax+b) וגם"), `נגזרת ${ltr("1/(ax+b)")} וגם`);
assert.strictEqual(B.render("אז f' = 0 ו-f\u2032 = 0 כאן"), `אז ${ltr("f' = 0")} ו-${ltr("f\u2032 = 0")} כאן`);
assert.strictEqual(B.render("התוצאה: y = x² + 1"), `התוצאה: ${ltr("y = x² + 1")}`);
// a Hebrew sentence ending in a plain formula: the formula is one run and the final punctuation stays at the RTL end
assert.strictEqual(B.render("הנגזרת היא f'(x) = 2x."), `הנגזרת היא ${ltr("f'(x) = 2x")}.`);
assert.strictEqual(B.render("מהי f'(x) = 2x?"), `מהי ${ltr("f'(x) = 2x")}?`);

// Hebrew prefix + maqaf before a Latin word stays outside (RTL start); inline code keeps its trailing punctuation outside, at the RTL end
assert.strictEqual(B.render("ש-typedef וגם ו-NULL"), `ש-${ltr("typedef")} וגם ו-${ltr("NULL")}`);
const tok = '<code class="tok" dir="ltr">fileName</code>';
assert.strictEqual(B.render(`שם הקובץ ${tok}.`), `שם הקובץ ${tok}.`);
// pointer stars stay inside the run: "Item**." keeps both stars and the period stays outside
assert.strictEqual(B.render("הטיפוס Item**."), `הטיפוס ${ltr("Item**")}.`);
assert.strictEqual(B.render("ב-*ptr ו-**pp כאן"), `ב-${ltr("*ptr")} ו-${ltr("**pp")} כאן`);
assert.strictEqual(B.render("הטיפוס int* ו-char** כאן"), `הטיפוס ${ltr("int*")} ו-${ltr("char**")} כאן`);
// counters, times and percentages are LTR runs; comma lists of Latin words with a Hebrew conjunction
assert.strictEqual(B.render("שאלה 1/8"), `שאלה ${ltr("1/8")}`);
assert.strictEqual(B.render("⏱ 3:59:59"), `⏱ ${ltr("3:59:59")}`);
assert.strictEqual(B.render("ציון 80%."), `ציון ${ltr("80%")}.`);
assert.strictEqual(B.render("static, const ו-scope"), `${ltr("static, const")} ו-${ltr("scope")}`);

console.log("test_bidi: ok");
