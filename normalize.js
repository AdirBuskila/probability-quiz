"use strict";
/* Answer normalisers for the step widgets (window.Normalize). Pure functions, no DOM, no state.
   text(s)       free text: trim, collapse whitespace, case-fold, drop a trailing period.
   complexity(s) asymptotic notation: spaces stripped, log/lg/log_2/log2 -> log, n² / n^{2} -> n^2,
                 Θ and O both accepted as written (Θ is folded onto O so either grades the same), case-insensitive.
   number(s)     decimal comma allowed, unicode minus, simple fractions "a/b"; NaN when it is not a number. */
(function (root) {
  const SUP = { "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9" };

  function text(s) {
    return String(s == null ? "" : s).normalize("NFKC").toLowerCase().replace(/\s+/g, " ").trim().replace(/[.。]+$/, "").trim();
  }

  function complexity(s) {
    let t = String(s == null ? "" : s).normalize("NFC");
    t = t.replace(/[Θθ]/g, "O").replace(/\\(?:Theta|theta|Omicron)/g, "O");
    t = t.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, m => "^" + [...m].map(c => SUP[c]).join(""));
    t = t.toLowerCase().replace(/\s+/g, "").replace(/\\/g, "");
    t = t.replace(/[·⋅*×]/g, "");                     // "n·log n" -> "nlog n"
    t = t.replace(/\^\{([^{}]*)\}/g, "^$1").replace(/_\{([^{}]*)\}/g, "_$1");
    t = t.replace(/log(?:_?2|₂)?(?![a-z])/g, "log");   // log, log2, log_2, log₂ -> log
    t = t.replace(/lg/g, "log");
    t = t.replace(/log(?:_?2|₂)/g, "log");
    return t;
  }

  function number(s) {
    let t = String(s == null ? "" : s).replace(/[−–—]/g, "-").replace(/\s+/g, "");
    if (!t) return NaN;
    const frac = /^(-?[0-9]+(?:[.,][0-9]+)?)\/([0-9]+(?:[.,][0-9]+)?)$/.exec(t);
    const val = x => Number(x.replace(",", "."));
    if (frac) { const d = val(frac[2]); return d === 0 ? NaN : val(frac[1]) / d; }
    if (!/^[+-]?(?:[0-9]+(?:[.,][0-9]*)?|[.,][0-9]+)$/.test(t)) return NaN;
    return val(t);
  }

  /* ---------- Bidi (window.Bidi): render-time fixes for Latin inside Hebrew (RTL) HTML ----------
     Ported from computer-systems-quiz 775f65b. render(html) = labelLines -> mathRuns -> isolate.
     labelLines: a line that starts with a Latin option label ("a." / "(b)" / "1)") gets the label, punctuation
                 included, in its own LTR isolate, so it sits at the start (right edge) with the period right after the letter.
     mathRuns:   inline formulas chained by punctuation become one LTR isolate; line-final punctuation stays with its formula.
     isolate:    every other non-Hebrew run holding a digit or Latin letter becomes an LTR <bdi>: "4!" keeps its "!", a product/arithmetic
                 chain (· × + − = /) is one run, a bracket whose partner is outside the run stays outside (so it mirrors as a pair in RTL),
                 sentence-final . , ? : stay outside at the RTL end.
     <pre>, <code>, MathML, formulas and existing LTR isolates are never touched. Idempotent. */
  const B_INLINE = /^<\/?(b|strong|i|em|u|sub|sup|code)\b[^>]*>$/i;
  const B_SKIP = /^<(code|bdi|pre|math)\b|class="[^"]*\b(lesson-formula|qref|math-inline|math-block|math-run|opt-ltr)\b|\bdir="ltr"/i;
  const B_START = /[A-Za-z0-9$"(\[|\u221a\u2016\u03a3\u2211\u2212\u0177\u0233\u03b1-\u03c9\u0394\u03b8]/;
  const B_END = /[A-Za-z0-9)\]|\u00b2\u00b3\u2016%\u221e'\u2032\u2033\u2019"\u2080-\u2089\u1d62\u2c7c\u2099\u2096\u0177\u0233\u0304\u03b1-\u03c9]/;
  const B_OP = /^[·×+−=\/*…]$/;      // · × + − = / * …  (the ASCII hyphen is not one: "ו-y")
  const bIsTag =p => p[0] === "<", bChr = p => (bIsTag(p) || p[0] === "&" && p.length > 1) ? "" : p;
  function isolate(html) {
    const toks = String(html).match(/<[^>]+>|[^<]+/g) || [];
    let out = "", run = [], skip = 0;
    const emit = parts => {
      if (!parts.length) return "";
      const s = parts.join("");
      { const st = [];                                                 // a bracket whose partner is outside this run stays outside, so it pairs with it in RTL
        for (let i = 0; i < parts.length; i++) { const c = bChr(parts[i]);
          if (c === "(" || c === "[") st.push([i, c]);
          else if (c === ")" || c === "]") { const top = st[st.length - 1];
            if (top && top[1] === (c === ")" ? "(" : "[")) st.pop(); else return emit(parts.slice(0, i)) + parts[i] + emit(parts.slice(i + 1)); } }
        if (st.length) { const i = st[st.length - 1][0]; return emit(parts.slice(0, i)) + parts[i] + emit(parts.slice(i + 1)); } }
      let a = 0, b = parts.length - 1;
      while (a <= b && !B_START.test(bChr(parts[a]))) a++;
      while (b >= a && !B_END.test(bChr(parts[b]))) b--;

      if (a <= b) {
        while (b + 1 < parts.length && bChr(parts[b + 1]) === "!" && /[A-Za-z0-9)\]]/.test(bChr(parts[b]))) b++;   // factorial: "4!" stays one run
        while (b + 1 < parts.length && bChr(parts[b + 1]) === "*" && /[A-Za-z0-9)\]*]/.test(bChr(parts[b]))) b++;   // pointer stars: "Item**" keeps its stars
        while (a > 0 && bChr(parts[a - 1]) === "*" && /[A-Za-z(]/.test(bChr(parts[a]))) a--;                          // ... and "*ptr" its star
        for (let j = a; j > 0;) { let k = j - 1; while (k >= 0 && /^\s$/.test(parts[k])) k--;                       // arithmetic chain: leading operators join the run
          if (k >= 0 && B_OP.test(bChr(parts[k]))) { a = k; j = k; } else break; }
        for (let j = b; j < parts.length - 1;) { let k = j + 1; while (k < parts.length && /^\s$/.test(parts[k])) k++;  // ... and so do trailing ones
          if (k < parts.length && B_OP.test(bChr(parts[k]))) { b = k; j = k; } else break; }
      }
      { const tail = parts.slice(b + 1).join(""); if (b >= a && /^[,;]?\s*(\.\.\.|…)$/.test(tail)) b = parts.length - 1; }   // a trailing ellipsis stays with its list
      while (a > 0 && bIsTag(parts[a - 1]) && !/^<\//.test(parts[a - 1])) a--;     // pull in tags hugging the core: <b>3</b>
      while (b < parts.length - 1 && /^<\//.test(parts[b + 1])) b++;
      const core = parts.slice(a, b + 1), st = [];
      let ok = a <= b && /[A-Za-z0-9]/.test(core.join(""));
      for (const t of core) { if (!bIsTag(t) || !ok) continue;
        const m = t.match(/^<(\/?)(\w+)/); if (m[1]) { if (st.pop() !== m[2].toLowerCase()) ok = false; } else st.push(m[2].toLowerCase()); }
      if (ok && st.length) ok = false;
      return ok ? parts.slice(0, a).join("") + `<bdi class="ltr${core.join("").replace(/<[^>]+>/g, "").length <= 22 ? " nw" : ""}" dir="ltr">${core.join("")}</bdi>` + parts.slice(b + 1).join("") : s;
    };
    const flush = () => { if (run.length) out += emit(run.join("").match(/<[^>]+>|&[#\w]+;|[^<]/g)); run = []; };
    for (const t of toks) {
      if (t[0] === "<") {
        if (skip) { out += t; if (/^<\//.test(t)) skip--; else if (!/\/>$|^<(br|img|hr|wbr)\b/i.test(t)) skip++; continue; }
        if (B_SKIP.test(t)) { flush(); out += t; if (!/^<(br|img)\b/i.test(t)) skip = 1; continue; }
        if (B_INLINE.test(t)) { run.push(t); continue; }
        flush(); out += t; continue;
      }
      if (skip) { out += t; continue; }
      for (const piece of t.match(/[֐-׿]+|[^֐-׿]+/g)) {          // Hebrew text ends a run
        if (/[֐-׿]/.test(piece)) { flush(); out += piece; } else run.push(piece);
      }
    }
    flush();
    return out;
  }

  /* apply fn to the parts of html outside <pre>/<code>/<math>; first = true only for the very start of the string */
  function outsideCode(html, fn) {
    return String(html).split(/(<pre\b[\s\S]*?<\/pre>|<code\b[\s\S]*?<\/code>|<math\b[\s\S]*?<\/math>)/i)
      .map((seg, i) => i % 2 ? seg : fn(seg, i === 0)).join("");
  }
  const LBL = String.raw`(\(?[A-Za-z]{1,2}\d?[.)]|\([A-Za-z0-9]{1,3}\)|\d{1,2}[.)])(?=\s|&nbsp;)`;
  const lbl = label => `<bdi class="ltr nw opt-label" dir="ltr">${label}</bdi>`;
  function labelLines(html) {
    return outsideCode(html, (seg, first) => {
      let out = seg.replace(new RegExp(String.raw`(<br\s*\/?>|<(?:li|p|div)\b[^>]*>)(\s*)` + LBL, "gi"), (m, lead, sp, label) => lead + sp + lbl(label));
      if (first) out = out.replace(new RegExp("^(\\s*)" + LBL), (m, sp, label) => sp + lbl(label));
      return out;
    });
  }

  const M_INL = '<span class="math-inline">(?:(?!</span>)[\\s\\S])*</span>';
  const M_RUN = '<span class="math-run" dir="ltr">(?:(?!</span></span>)[\\s\\S])*</span></span>';
  function mathRuns(html) {
    const h = String(html).replace(new RegExp(`${M_INL}(?:(?:[ ,;.:]|&nbsp;)+${M_INL})+`, "g"),
      m => `<span class="math-run" dir="ltr">${m}</span>`);
    return h.replace(new RegExp(`(${M_RUN}|${M_INL})([.,;:?!]+)(?=<br>|</[a-z]+>|$)`, "g"), (m, unit, punct0) => { const punct = punct0.replace(/^[?!]/, "\u2060$&");   // a lone ? or ! is glued to the formula (word joiner): it must not wrap onto its own line
      return       unit.startsWith('<span class="math-run"') ? unit.slice(0, -"</span>".length) + punct + "</span>"
        : `<span class="math-run" dir="ltr">${unit}${punct}</span>`; });
  }
  const render = html => isolate(mathRuns(labelLines(html)));
  const bidi = { render, isolate, labelLines, mathRuns };
  root.Bidi = bidi;
  root.crsIsolate = render;

  const api = { text, complexity, number, Bidi: bidi };
  root.Normalize = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
