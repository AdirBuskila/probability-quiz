# -*- coding: utf-8 -*-
"""Lint tools/raw/*.json against tools/RAW_SCHEMA.md. Run before build_questions.py
(the build runs the same checks and aborts on any problem).

    PYTHONUTF8=1 py tools/validate.py            # all raw files (skips names starting "_")
    PYTHONUTF8=1 py tools/validate.py DEMO-A     # just one exam code (or a path)

Every message starts with the question id (<CODE>-Q<num><part>, e.g. DEMO-A-Q3b).
Exit code 1 if any PROBLEM is found. Prints ASCII only.
"""
import json, pathlib, re, sys, collections, unicodedata

TOOLS = pathlib.Path(__file__).resolve().parent
EXAM_RE = re.compile(r"^(\d{2}[A-Z]-[A-Z]|SAMP-\d+|DEMO-[A-Z])\.json$")  # only real exam files; tmp_*/_verify_*/_blind_* are ignored
RAW = TOOLS / "raw"
ROOT = TOOLS.parent

sys.path.insert(0, str(TOOLS))
from course_config import load as _load_cfg  # noqa: E402
from richtext import part_suffix, question_id  # noqa: E402

TOPICS = {k for k, _ in _load_cfg()["topics"]}   # closed list, single source
KINDS = ("computation", "proof", "algorithm", "code", "mcq", "truefalse")
STEP_TYPES = ("choice", "numeric", "text", "order", "findbug", "fillblank")
OPT_TYPES = {"text", "math", "image"}
OPT_IDS = ("a", "b", "c", "d", "e", "f", "g", "h")
CONFIDENCE = {"high", "med", "low"}
RUBRIC_SOURCES = {"official", "ai-draft", "ai-verified"}
STEPS_SOURCES = {"official", "ai-draft", "ai-verified"}
SOLUTION_SOURCES = {"official-pdf", "lecturer-solution", "student-solution", "solved"}
CONTEXT_KINDS = {"image", "text", "code"}
NORMALIZE = {"none", "complexity", "lower"}
DERIVED = {"id", "examCode", "examLabel", "year", "source", "topicLabel", "dedupKey", "pointsTotal"}
EXAM_KEYS = {"examCode", "examLabel", "year", "examDate", "sourceFile", "solutionFile", "contexts", "questions"}
CONTEXT_KEYS = {"kind", "title", "text", "image", "caption", "code"}
QUESTION_KEYS = {"num", "part", "kind", "topic", "points", "question", "contextId", "image", "solution",
                 "solutionSource", "official", "confidence", "hold", "rubric", "rubricSource", "pitfalls",
                 "steps", "stepsSource", "options", "correctId", "acceptedIds", "lockOrder", "explanation",
                 "verdict", "region", "sim"}
STEP_KEYS = {"type", "prompt", "explain", "code", "options", "correctId", "answer", "tol", "accept",
             "normalize", "lines", "bugIndex", "blankIndex", "region"}
RUBRIC_KEYS = {"text", "points"}
OPTION_KEYS = {"id", "type", "value"}
CODE_RE = re.compile(r"^(\d{2}[ABS]-[A-H]|SAMP-\d+|DEMO-[A-Z])$")
HEB = re.compile(r"[֐-׿]")
TOKEN = re.compile(r"(\$\$.+?\$\$|\$[^$]+?\$|`[^`]+`)", re.S)


# ---------------------------------------------------------------- anonymization (tools/redact.txt)
def load_redact():
    """Author names that must never ship (student solutions are anonymized). Optional file
    tools/redact.txt: one FULL name per line, '#' starts a comment. Matching is a case-insensitive
    whole-word match on NFC-normalized text (a name is not matched inside a longer word, so list
    prefixed or inflected forms as their own lines); Hebrew names (no case) match exactly."""
    fp = TOOLS / "redact.txt"
    if not fp.is_file():
        return []
    out = []
    for ln in fp.read_text(encoding="utf-8-sig").splitlines():
        ln = ln.split("#", 1)[0].strip()
        if ln:
            out.append(ln)
    return out


def _fold(s):
    return unicodedata.normalize("NFC", str(s)).casefold()


def _wordchar(c):
    return c == "_" or unicodedata.category(c)[0] in "LNM"


def contains_word(text, name):
    """name occurs in text with no letter/digit/mark/underscore directly before or after it
    (both arguments already folded). Hebrew-aware: a name inside a longer word does not match."""
    start = text.find(name)
    while start != -1:
        end = start + len(name)
        if (start == 0 or not _wordchar(text[start - 1])) and (end == len(text) or not _wordchar(text[end])):
            return True
        start = text.find(name, start + 1)
    return False


def _strings(x, path):
    """Yield (path, text) for every string value inside x."""
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _strings(v, f"{path}[{i}]")
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from _strings(v, f"{path}.{k}" if path else str(k))


def redact_problems(data, code, qid_of, names):
    """A listed name in ANY shipped text field (questions, options, solutions/explanations, rubric,
    pitfalls, steps, contexts, sourceFile/solutionFile/examLabel ...) is a problem; the message
    starts with the item id. The name itself is not echoed (logs would leak it)."""
    if not names:
        return []
    folded = [_fold(n) for n in names]
    out = []

    def scan(where, obj, base):
        seen = set()
        for path, text in _strings(obj, base):
            t = _fold(text)
            for i, n in enumerate(folded):
                if contains_word(t, n) and (path, i) not in seen:
                    seen.add((path, i))
                    out.append(f"{where}: redact.txt entry #{i + 1} found in {path} (author names must not ship)")

    scan(code, {k: v for k, v in data.items() if k not in ("questions", "contexts")}, "")
    for cid, c in (data.get("contexts") or {}).items():
        scan(f"{code} ctx {cid}", c, "")
    for q in data.get("questions") or []:
        if isinstance(q, dict):
            scan(qid_of(q), q, "")
    return out


IMG_LINE = re.compile(r"^!\[([^\]\n]*)\]\((images/exams/[A-Za-z0-9._-]+\.png)\)[ \t]*$")
FENCE_OPEN = re.compile(r"^```([A-Za-z0-9+#_-]{0,12})[ \t]*$")
FENCE_CLOSE = re.compile(r"^```[ \t]*$")


def split_fences(s):
    """Yield (kind, payload): ('text', str) | ('fence', (lang, body)) | ('unclosed', str).
    A fence opens on a line that is exactly ``` or ```lang and closes on a line that is exactly ```."""
    s = str(s)
    if "```" not in s:
        yield "text", s
        return
    lines, buf, i = s.replace("\r\n", "\n").split("\n"), [], 0
    while i < len(lines):
        m = FENCE_OPEN.match(lines[i])
        if not m:
            buf.append(lines[i])
            i += 1
            continue
        j = i + 1
        while j < len(lines) and not FENCE_CLOSE.match(lines[j]):
            j += 1
        if buf:
            yield "text", "\n".join(buf)
            buf = []
        if j >= len(lines):
            yield "unclosed", "\n".join(lines[i:])
            return
        yield "fence", (m.group(1), "\n".join(lines[i + 1:j]))
        i = j + 1
    if buf:
        yield "text", "\n".join(buf)


def rich_problems(s, where):
    """Balanced $, no Hebrew inside math. Returns a list of problem strings."""
    out = []
    if "```" in str(s):
        keep = []
        for fk, fp in split_fences(s):
            if fk == "unclosed":
                out.append(f"{where}: unclosed ``` code fence (close it with a line that is exactly ```)")
            elif fk == "text":
                keep.append(fp)
        s = "\n".join(keep)
    if "![" in str(s):
        keep = []
        for ln in str(s).replace("\r\n", "\n").split("\n"):
            m = IMG_LINE.match(ln)
            if m:
                if not (ROOT / m.group(2)).is_file():
                    out.append(f"{where}: image file missing {m.group(2)}")
            elif ln.lstrip().startswith("!["):
                out.append(f"{where}: an inline figure must be a line of exactly ![alt](images/exams/<file>.png)")
            else:
                keep.append(ln)
        s = "\n".join(keep)
    s = str(s).replace("\\$", "")
    for part in TOKEN.split(s):
        if part.startswith("$$") and part.endswith("$$") and len(part) > 4:
            tex = part[2:-2]
        elif part.startswith("$") and part.endswith("$") and len(part) > 2:
            tex = part[1:-1]
        elif part.startswith("`"):
            continue
        else:
            if "$" in part:
                out.append(f"{where}: unbalanced $ (use \\$ for a literal dollar)")
            continue
        if HEB.search(tex):
            out.append(f"{where}: Hebrew inside math ${tex}$")
        if not tex.strip():
            out.append(f"{where}: empty math span")
    return out


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def nonblank(x):
    return isinstance(x, str) and bool(x.strip())


def unknown_keys(w, obj, allowed, P):
    """Unknown keys are errors (a misspelt stepsSource would otherwise silently skip the draft gate).
    Derived keys (*Html, html, DERIVED) get their own message elsewhere."""
    for k in sorted(k for k in obj if k not in allowed and k not in DERIVED
                    and not k.endswith("Html") and k != "html"):
        P(f"{w}: unknown key {k!r}")


def check_options(w, opts, P, root, rich=True):
    """Shared by mcq questions and choice/fillblank steps. Returns the option ids."""
    if not isinstance(opts, list) or len(opts) < 2:
        P(f"{w}: needs at least 2 options")
        return []
    ids = [o.get("id") for o in opts]
    if len(set(ids)) != len(ids):
        P(f"{w}: duplicate option ids {ids}")
    for o in opts:
        ow = f"{w} opt {o.get('id')}"
        unknown_keys(ow, o, OPTION_KEYS, P)
        if o.get("id") not in OPT_IDS:
            P(f"{ow}: option id must be one of a..h")
        t = o.get("type", "text")
        if t not in OPT_TYPES:
            P(f"{ow}: bad type {t}")
        v = str(o.get("value", ""))
        if not v.strip():
            P(f"{ow}: blank value")
        if "html" in o:
            P(f"{ow}: derived field html must not be in raw")
        if t == "math":
            if HEB.search(v):
                P(f"{ow}: Hebrew inside math option")
            if v.strip().startswith("$"):
                P(f"{ow}: math option value must be TeX without $")
        elif t == "image":
            if not (root / v).is_file():
                P(f"{ow}: image file missing {v}")
        elif rich:
            for x in rich_problems(v, ow):
                P(x)
    return ids


def check_step(w, s, P, root):
    if not isinstance(s, dict):
        P(f"{w}: step must be an object")
        return
    t = s.get("type")
    if t not in STEP_TYPES:
        P(f"{w}: step type {t!r} not in {list(STEP_TYPES)}")
        return
    unknown_keys(w, s, STEP_KEYS, P)
    for k in s:
        if k.endswith("Html"):
            P(f"{w}: derived field {k} must not be in raw")
    if not nonblank(s.get("prompt")):
        P(f"{w}: empty prompt")
    else:
        for x in rich_problems(s["prompt"], w + " prompt"):
            P(x)
    if s.get("explain"):
        for x in rich_problems(s["explain"], w + " explain"):
            P(x)
    if "region" in s:
        check_region(w, s["region"], P)
    if "code" in s and not isinstance(s["code"], bool):
        P(f"{w}: code must be true/false")
    code = s.get("code") is True

    def lines_ok():
        ln = s.get("lines")
        if not isinstance(ln, list) or len(ln) < 2 or not all(isinstance(x, str) and x.strip() for x in ln):
            P(f"{w}: lines must be a list of >= 2 non-blank strings")
            return None
        if not code:
            for i, x in enumerate(ln):
                for y in rich_problems(x, f"{w} line {i}"):
                    P(y)
        return ln

    if t == "choice":
        ids = check_options(w, s.get("options"), P, root)
        if s.get("correctId") not in ids:
            P(f"{w}: correctId {s.get('correctId')} not among option ids")
    elif t == "numeric":
        if not is_num(s.get("answer")):
            P(f"{w}: numeric answer must be a number")
        if "tol" in s and (not is_num(s["tol"]) or s["tol"] < 0):
            P(f"{w}: tol must be a number >= 0")
    elif t == "text":
        acc = s.get("accept")
        if not isinstance(acc, list) or not acc or not all(nonblank(a) for a in acc):
            P(f"{w}: accept must be a non-empty list of strings")
        if s.get("normalize", "none") not in NORMALIZE:
            P(f"{w}: normalize {s.get('normalize')!r} not in {sorted(NORMALIZE)}")
    elif t == "order":
        lines_ok()
    elif t == "findbug":
        ln = lines_ok()
        bi = s.get("bugIndex")
        if not is_int(bi):
            P(f"{w}: bugIndex must be an int")
        elif ln is not None and not (0 <= bi < len(ln)):
            P(f"{w}: bugIndex {bi} out of range 0..{len(ln) - 1}")
    elif t == "fillblank":
        ln = lines_ok()
        bi = s.get("blankIndex")
        if not is_int(bi):
            P(f"{w}: blankIndex must be an int")
        elif ln is not None:
            if not (0 <= bi < len(ln)):
                P(f"{w}: blankIndex {bi} out of range 0..{len(ln) - 1}")
            elif "___" not in ln[bi]:
                P(f"{w}: line blankIndex {bi} must contain the ___ placeholder")
        ids = check_options(w, s.get("options"), P, root, rich=not code)
        if s.get("correctId") not in ids:
            P(f"{w}: correctId {s.get('correctId')} not among option ids")


# ---------------------------------------------------------------- region / sim (probability extras)
REGION_KEYS = {"space", "event", "given", "labels", "exact", "caption", "ticks"}
INEQ_OPS = {"<", "<=", ">", ">="}
SIM_KINDS = {"area", "pdf", "circuit", "dice", "urn", "bernoulli_matrix", "custom_discrete"}
SIM_KEYS = {"kind", "params", "estimate", "exact", "trials", "seed"}
SIM_MEASURES = {"prob", "mean", "var", "cov"}
SIM_REQUIRED = {"area": (), "pdf": ("pieces",), "circuit": (), "dice": ("n",), "urn": ("draws",),
                "bernoulli_matrix": ("n", "p"), "custom_discrete": ()}


def _const_ok(v):
    return is_num(v) or nonblank(v)


def _check_set(w, s, P):
    """event/given: list of inequalities (AND), {"any": [list, ...]} (OR of ANDs) or an expression string."""
    if isinstance(s, str):
        if not s.strip():
            P(f"{w}: empty expression")
        return
    if isinstance(s, dict) and set(s) == {"any"} and isinstance(s["any"], list) and s["any"]:
        for i, c in enumerate(s["any"]):
            _check_set(f"{w}.any[{i}]", c if isinstance(c, list) else [c], P)
        return
    if not isinstance(s, list) or not s:
        P(f"{w}: must be a non-empty list of inequalities, {{any:[...]}} or an expression string")
        return
    for i, q in enumerate(s):
        qw = f"{w}[{i}]"
        if isinstance(q, str):
            if not q.strip():
                P(f"{qw}: empty expression")
            continue
        if not isinstance(q, dict):
            P(f"{qw}: inequality must be an object or a string")
            continue
        extra = set(q) - ({"expr", "op", "c"} if "expr" in q else {"a", "b", "c", "op"})
        if extra:
            P(f"{qw}: unknown inequality key(s) {sorted(extra)}")
        if q.get("op") not in INEQ_OPS:
            P(f"{qw}: op must be one of < <= > >=")
        for k in ("a", "b", "c"):
            if k in q and not _const_ok(q[k]):
                P(f"{qw}: {k} must be a number or a constant expression string")
        if "expr" in q and not nonblank(q["expr"]):
            P(f"{qw}: expr must be a non-blank string")
        if "expr" not in q and not any(k in q for k in ("a", "b")):
            P(f"{qw}: a linear inequality needs a and/or b")


def _check_space(w, sp, P):
    if not isinstance(sp, dict) or set(sp) != {"x", "y"} or not all(
            isinstance(sp[k], list) and len(sp[k]) == 2 and all(_const_ok(v) for v in sp[k]) for k in ("x", "y")):
        P(f'{w}: space must be {{"x":[a,b], "y":[c,d]}}')


def check_region(w, r, P):
    """Shape of a `region` (an object or a non-empty list of them). Geometry and `exact` are checked by
    tools/check_sim_specs.py (Node, region.js), which validate.py main runs."""
    if isinstance(r, list):
        if not r:
            P(f"{w}: region list is empty")
        for i, x in enumerate(r):
            check_region(f"{w}[{i}]", x, P)
        return
    if not isinstance(r, dict):
        P(f"{w}: region must be an object (or a list of them)")
        return
    unknown_keys(w + " region", r, REGION_KEYS, P)
    _check_space(w + " region", r.get("space"), P)
    if "event" not in r:
        P(f"{w} region: needs event")
    else:
        _check_set(w + " region.event", r["event"], P)
    if "given" in r:
        _check_set(w + " region.given", r["given"], P)
    if "exact" in r and not (is_num(r["exact"]) and 0 <= r["exact"] <= 1):
        P(f"{w} region: exact must be a probability (number in [0,1])")
    if "labels" in r and not (isinstance(r["labels"], dict) and set(r["labels"]) <= {"x", "y"}
                              and all(isinstance(v, str) for v in r["labels"].values())):
        P(f'{w} region: labels must be {{"x": str, "y": str}}')
    if "caption" in r and not isinstance(r["caption"], str):
        P(f"{w} region: caption must be a string")
    if "ticks" in r and not (isinstance(r["ticks"], dict) and set(r["ticks"]) <= {"x", "y"}
                             and all(isinstance(v, list) and all(_const_ok(t) for t in v) for v in r["ticks"].values())):
        P(f'{w} region: ticks must be {{"x":[..], "y":[..]}} of numbers')


def check_sim(w, s, P, has_region=False):
    """Shape of a `sim`. Every sim is also RUN by tools/check_sim_specs.py (validate.py main calls it)."""
    if not isinstance(s, dict):
        P(f"{w}: sim must be an object")
        return
    unknown_keys(w + " sim", s, SIM_KEYS, P)
    kind = s.get("kind")
    if kind not in SIM_KINDS:
        P(f"{w} sim: kind {kind!r} not in {sorted(SIM_KINDS)}")
        return
    if not is_num(s.get("exact")):
        P(f"{w} sim: exact must be a number (the key the simulation is checked against)")
    if "estimate" in s and not nonblank(s["estimate"]):
        P(f"{w} sim: estimate must be a non-blank label")
    if "trials" in s and not (is_int(s["trials"]) and 1000 <= s["trials"] <= 2000000):
        P(f"{w} sim: trials must be an int in 1000..2000000")
    if "seed" in s and not is_int(s["seed"]):
        P(f"{w} sim: seed must be an int")
    pr = s.get("params")
    if not isinstance(pr, dict):
        P(f"{w} sim: params must be an object")
        return
    for k in SIM_REQUIRED[kind]:
        if k not in pr:
            P(f"{w} sim: kind {kind} needs params.{k}")
    m = pr.get("measure", "prob")
    if m not in SIM_MEASURES:
        P(f"{w} sim: measure {m!r} not in {sorted(SIM_MEASURES)}")
    from_region = kind == "area" and bool(pr.get("fromRegion"))
    if kind == "area":
        if from_region:
            if not has_region:
                P(f"{w} sim: fromRegion but the item has no region")
        else:
            _check_space(w + " sim.params", pr.get("space"), P)
    if m == "prob" and "event" not in pr and not from_region:
        P(f"{w} sim: measure prob needs params.event")
    for k in ("event", "given"):
        if k in pr:
            if kind == "area":
                _check_set(f"{w} sim.params.{k}", pr[k], P)
            elif not nonblank(pr[k]):
                P(f"{w} sim: params.{k} must be an expression string")
    if m in ("mean", "var") and not nonblank(pr.get("expr")):
        P(f"{w} sim: measure {m} needs params.expr (string)")
    if m == "cov" and not (isinstance(pr.get("expr"), list) and len(pr["expr"]) == 2 and all(nonblank(x) for x in pr["expr"])):
        P(f"{w} sim: measure cov needs params.expr [expr1, expr2]")


def check_question(code, q, ctxs, P, W, root):
    qid = question_id(code, q)
    kind = q.get("kind")
    unknown_keys(qid, q, QUESTION_KEYS, P)
    if not is_int(q.get("num")):
        P(f"{qid}: num must be an int")
    if q.get("part") not in (None, "") and part_suffix(q.get("part")) is None:
        P(f"{qid}: part {q.get('part')!r} is not a single letter (Hebrew or a-z)")
    if kind not in KINDS:
        P(f"{qid}: kind {kind!r} not in {list(KINDS)}")
    hold = q.get("hold")
    # a held question is left out of the bank: it needs no key/verdict/solution/source, only what identifies it
    for k in (() if hold else ("topic", "question", "official", "confidence")):
        if k not in q:
            P(f"{qid}: missing {k}")
    if q.get("topic") not in TOPICS and not (hold and "topic" not in q):
        P(f"{qid}: topic {q.get('topic')} not in closed list")
    if not nonblank(q.get("question")) and not hold:
        P(f"{qid}: empty question")
    if "official" in q and not isinstance(q["official"], bool):
        P(f"{qid}: official must be true/false")
    if "confidence" in q and q["confidence"] not in CONFIDENCE:
        P(f"{qid}: confidence must be high|med|low")
    for k in sorted(k for k in q if k in DERIVED or k.endswith("Html")):
        P(f"{qid}: derived field {k} must not be in raw")
    if "points" in q and (not is_num(q["points"]) or q["points"] < 0):
        P(f"{qid}: points must be a number >= 0")
    if q.get("contextId") and q["contextId"] not in ctxs:
        P(f"{qid}: contextId {q['contextId']} not defined in this file")
    if q.get("image") and not (root / q["image"]).is_file():
        P(f"{qid}: image file missing {q['image']}")
    if "hold" in q and not nonblank(hold):
        P(f"{qid}: hold must be a non-empty reason string")
    for k in ("question", "solution", "explanation"):
        if q.get(k):
            for x in rich_problems(q[k], f"{qid} {k}"):
                P(x)

    # ---- solution (mcq carries its key + explanation instead)
    has_sol = nonblank(q.get("solution"))
    if has_sol:
        if q.get("solutionSource") not in SOLUTION_SOURCES:
            P(f"{qid}: solutionSource {q.get('solutionSource')!r} not in {sorted(SOLUTION_SOURCES)}")
    elif not hold and kind != "mcq":
        P(f"{qid}: missing solution (a question without one must carry a hold reason)")
    if not has_sol and kind != "mcq":
        if q.get("steps"):
            P(f"{qid}: steps without a solution")
        if q.get("rubric"):
            P(f"{qid}: rubric without a solution")

    # ---- mcq options / key; forbidden elsewhere
    if kind == "mcq":
        held_bare = bool(hold) and not q.get("options")
        ids = [] if held_bare else check_options(qid, q.get("options"), P, root)
        if q.get("correctId") not in ids and not (hold and "correctId" not in q):
            P(f"{qid}: correctId {q.get('correctId')} not among option ids")
        acc = q.get("acceptedIds")
        if acc is not None:
            if not isinstance(acc, list) or len(acc) < 2:
                P(f"{qid}: acceptedIds only when >1 accepted (non-empty list of >=2)")
            else:
                if any(a not in ids for a in acc):
                    P(f"{qid}: acceptedIds {acc} contains an unknown option id")
                if acc[0] != q.get("correctId") and not (hold and "correctId" not in q):
                    P(f"{qid}: acceptedIds must start with correctId")
                if len(set(acc)) != len(acc):
                    P(f"{qid}: duplicate acceptedIds")
        if "lockOrder" in q and not isinstance(q["lockOrder"], bool):
            P(f"{qid}: lockOrder must be a boolean")
    else:
        for k in ("options", "correctId", "acceptedIds", "lockOrder"):
            if k in q:
                P(f"{qid}: {k} is only for kind mcq")
    if kind == "truefalse":
        if not isinstance(q.get("verdict"), bool) and not (hold and "verdict" not in q):
            P(f"{qid}: truefalse needs verdict true/false")
    elif "verdict" in q:
        P(f"{qid}: verdict is only for kind truefalse")

    # ---- rubric
    rub = q.get("rubric")
    if rub is not None:
        if not isinstance(rub, list) or not rub:
            P(f"{qid}: rubric must be a non-empty list")
        else:
            tot = 0
            for i, r in enumerate(rub):
                rw = f"{qid} rubric[{i}]"
                if not isinstance(r, dict) or not nonblank(r.get("text")):
                    P(f"{rw}: needs text")
                    continue
                if not is_num(r.get("points")) or r["points"] <= 0:
                    P(f"{rw}: points must be a number > 0")
                else:
                    tot += r["points"]
                unknown_keys(rw, r, RUBRIC_KEYS, P)
                if "html" in r:
                    P(f"{rw}: derived field html must not be in raw")
                for x in rich_problems(r["text"], rw):
                    P(x)
            if is_num(q.get("points")) and tot != q["points"]:
                W(f"{qid}: rubric points sum {tot} != points {q['points']}")
        if q.get("rubricSource") not in RUBRIC_SOURCES:
            P(f"{qid}: rubricSource {q.get('rubricSource')!r} not in {sorted(RUBRIC_SOURCES)}")
    elif kind != "mcq" and not hold:
        W(f"{qid}: no rubric yet")
    # ---- pitfalls
    pf = q.get("pitfalls")
    if pf is not None:
        if not isinstance(pf, list) or not all(nonblank(x) for x in pf):
            P(f"{qid}: pitfalls must be a list of non-blank strings")
        else:
            for i, x in enumerate(pf):
                for y in rich_problems(x, f"{qid} pitfalls[{i}]"):
                    P(y)
    # ---- steps
    steps = q.get("steps")
    if steps is not None:
        if not isinstance(steps, list) or not steps:
            P(f"{qid}: steps must be a non-empty list")
        else:
            for i, s in enumerate(steps):
                check_step(f"{qid} step[{i}]", s, P, root)
        if q.get("stepsSource") not in STEPS_SOURCES:
            P(f"{qid}: stepsSource {q.get('stepsSource')!r} not in {sorted(STEPS_SOURCES)}")
    elif kind != "mcq" and not hold:
        W(f"{qid}: no steps yet")
    if "region" in q:
        check_region(qid, q["region"], P)
    if "sim" in q:
        check_sim(qid, q["sim"], P, has_region="region" in q)
    if q.get("confidence") == "low":
        W(f"{qid}: confidence low")


BIDI_FACT = re.compile(r"(?<![A-Za-z0-9_])(?:[0-9]+|[A-Za-z])!(?!=)")
BIDI_CHAIN = re.compile(r"(?<![A-Za-z0-9_])[0-9A-Za-z()]+(?:\s*[·×]\s*[0-9A-Za-z()]+!?)+")


def bidi_lint(data, code):
    """Warnings (never problems) for digit+"!" (a factorial) or a product chain (a middle dot or x between digits)
    written OUTSIDE $...$ in raw text. The open renderer (Bidi in normalize.js) isolates both correctly, but math mode
    ($4!$ or a LaTeX cdot product) is the intended form and always renders right. Message prefix: "bidi:"."""
    out = []
    for path, text in _strings(data, ""):
        if not isinstance(text, str) or not (re.search(r"[0-9A-Za-z]!", text) or re.search(r"[·×]", text)):
            continue
        for fk, fp in split_fences(text):
            if fk != "text":
                continue
            for part in TOKEN.split(fp):
                if part.startswith("$") or part.startswith("`"):
                    continue
                part = "\n".join(ln for ln in part.split("\n") if not IMG_LINE.match(ln))
                hits = [m.group(0).strip() for m in BIDI_FACT.finditer(part)] + [m.group(0).strip() for m in BIDI_CHAIN.finditer(part)]
                for h in hits[:3]:
                    out.append(f"bidi: {code} {path}: '{h}' outside $...$ (wrap it in math mode)")
    return out


def check_file(fp):
    """Returns (problems, warnings, n_questions, by_topic Counter)."""
    problems, warns = [], []
    P, W = problems.append, warns.append
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{fp.name}: JSON parse error: {str(e).encode('ascii', 'backslashreplace').decode()}"], [], 0, collections.Counter()
    unknown_keys(fp.name, data, EXAM_KEYS, P)
    code = data.get("examCode")
    if not code:
        P(f"{fp.name}: missing examCode")
        code = fp.stem
    elif not CODE_RE.match(code):
        W(f"{fp.name}: examCode {code} not YY[A|B|S]-[A..H] or SAMP-N")
    if code != fp.stem:
        P(f"{fp.name}: examCode {code} != file name")
    for k in ("examLabel", "year"):
        if data.get(k) in (None, ""):
            P(f"{code}: missing {k}")
    ctxs = data.get("contexts") or {}
    for cid, c in ctxs.items():
        w = f"{code} ctx {cid}"
        unknown_keys(w, c, CONTEXT_KEYS, P)
        if c.get("kind") not in CONTEXT_KINDS:
            P(f"{w}: kind must be image|text|code")
        if c.get("kind") == "image":
            if not c.get("image"):
                P(f"{w}: image context without image")
            elif not (ROOT / c["image"]).is_file():
                P(f"{w}: image file missing {c['image']}")
        if c.get("kind") == "text" and not nonblank(c.get("text")):
            P(f"{w}: text context without text")
        if c.get("kind") == "code" and not nonblank(c.get("code")):
            P(f"{w}: code context without code")
        for k in ("text", "caption", "title"):
            if c.get(k):
                for x in rich_problems(c[k], f"{w} {k}"):
                    P(x)
    problems += redact_problems(data, code, lambda q: question_id(code, q), load_redact())
    warns += bidi_lint(data, code)
    qs = data.get("questions")
    if not isinstance(qs, list) or not qs:
        P(f"{code}: no questions")
        qs = []
    seen, by_topic = set(), collections.Counter()
    for q in qs:
        qid = question_id(code, q)
        if qid in seen:
            P(f"{qid}: duplicate question id (num + part)")
        seen.add(qid)
        check_question(code, q, ctxs, P, W, ROOT)
        if q.get("topic") in TOPICS:
            by_topic[q["topic"]] += 1
    return problems, warns, len(qs), by_topic


def main():
    args = sys.argv[1:]
    if args:
        files = []
        for a in args:
            p = pathlib.Path(a)
            files.append(p if p.suffix == ".json" else RAW / f"{a}.json")
    else:
        files = [p for p in sorted(RAW.glob("*.json")) if EXAM_RE.match(p.name)]
    total, all_p, all_w, topics = 0, [], [], collections.Counter()
    for fp in files:
        if not fp.is_file():
            all_p.append(f"{fp}: not found")
            continue
        p, w, n, bt = check_file(fp)
        total += n
        topics.update(bt)
        all_p += p
        all_w += w
        print(f"{fp.stem}: {n} questions, {len(p)} problems")
    print(f"\nTOTAL: {total} questions across {len(files)} files")
    print("by topic:", dict(topics))
    print("bidi lint hits (factorial / product chain outside $..$):", sum(1 for x in all_w if x.startswith("bidi:")))
    if all_w:
        print(f"\nWARNINGS ({len(all_w)}):")
        for x in all_w:
            print("  -", x.encode("ascii", "backslashreplace").decode())
    # string-escape corruption (e.g. "\notin" in a non-raw generator string -> newline + "otin")
    import subprocess
    lint = subprocess.run([sys.executable, str(TOOLS / "gen" / "lint_escapes.py")],
                          capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT))
    if lint.returncode:
        all_p += ["escape-lint: " + l for l in lint.stdout.splitlines() if not l.startswith("escape problems")]
    # every sim / region in the raw files is run in Node (sim.js, region.js) and must agree with its exact
    sims = subprocess.run([sys.executable, str(TOOLS / "check_sim_specs.py")] + [str(f) for f in files if f.is_file()],
                          capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT))
    print(sims.stdout.rstrip())
    if sims.returncode:
        all_p += (["sim-check: " + l.strip() for l in sims.stdout.splitlines() if l.startswith("  FAIL")]
                  or ["sim-check: " + (sims.stderr.strip() or "check_sim_specs.py failed")])
    print(f"\nPROBLEMS ({len(all_p)}):")
    for x in all_p:
        print("  -", x.encode("ascii", "backslashreplace").decode())
    sys.exit(1 if all_p else 0)


if __name__ == "__main__":
    main()
