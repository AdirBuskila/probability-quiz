# -*- coding: utf-8 -*-
"""Run every `sim` and every `region` in the raw files through the browser's own code (sim.js / region.js, in Node),
so the "simulate it" button and the area figure can never disagree with the key.

    PYTHONUTF8=1 py tools/check_sim_specs.py              # all raw exam files
    PYTHONUTF8=1 py tools/check_sim_specs.py tools/raw/26A-B.json ...

For each question `sim`: Sim.check (tools/sim_check.js) runs exactly the button's first run (same seed, same
trials) and requires |estimate - exact| <= 4 SE, plus the deterministic value (exact enumeration, exact polygon
area or quadrature) must equal `exact`; a pdf must integrate to 1. For each `region` with `exact` (question or
step): the polygon area (exact) or the fine grid area must match. Exit 1 on any failure. validate.py main
calls this script. Prints ASCII only.
"""
import json, pathlib, re, subprocess, sys

TOOLS = pathlib.Path(__file__).resolve().parent
RAW = TOOLS / "raw"
EXAM_RE = re.compile(r"^(\d{2}[A-Z]-[A-Z]|SAMP-\d+|DEMO-[A-Z])\.json$")
sys.path.insert(0, str(TOOLS))
from richtext import question_id  # noqa: E402


def collect(files):
    jobs = []
    for fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue   # validate.py reports parse errors
        code = data.get("examCode") or fp.stem
        for q in data.get("questions") or []:
            if not isinstance(q, dict) or q.get("hold"):
                continue
            qid = question_id(code, q)
            item = {"region": q["region"]} if "region" in q else {}
            if isinstance(q.get("sim"), dict):
                jobs.append({"where": f"{qid} sim", "type": "sim", "spec": q["sim"], "item": item})
            regs = q.get("region")
            for i, r in enumerate(regs if isinstance(regs, list) else ([regs] if regs else [])):
                jobs.append({"where": f"{qid} region{'' if not isinstance(regs, list) else f'[{i}]'}", "type": "region", "spec": r})
            for j, s in enumerate(q.get("steps") or []):
                if isinstance(s, dict) and s.get("region"):
                    rs = s["region"]
                    for i, r in enumerate(rs if isinstance(rs, list) else [rs]):
                        jobs.append({"where": f"{qid} step[{j}] region", "type": "region", "spec": r})
    return jobs


def main():
    args = sys.argv[1:]
    files = [pathlib.Path(a) for a in args] if args else [p for p in sorted(RAW.glob("*.json")) if EXAM_RE.match(p.name)]
    jobs = collect(files)
    if not jobs:
        print("sim-check: no sim/region specs in the raw files")
        return 0
    proc = subprocess.run(["node", str(TOOLS / "sim_check.js")], input=json.dumps(jobs), capture_output=True,
                          text=True, encoding="utf-8", cwd=str(TOOLS))
    if proc.returncode not in (0, 1) or not proc.stdout.strip():
        print("sim-check: node sim_check.js failed: " + proc.stderr.encode("ascii", "backslashreplace").decode()[:400])
        return 1
    results = json.loads(proc.stdout)
    bad = [r for r in results if not r["ok"]]
    n_sim = sum(1 for j in jobs if j["type"] == "sim")
    print(f"sim-check: {n_sim} sim(s), {len(jobs) - n_sim} region(s), {len(bad)} failing")
    for r in results:
        line = f"{'  ok  ' if r['ok'] else '  FAIL'} {r['where']}: {r['summary']}"
        if not r["ok"]:
            line += " -- " + "; ".join(r["problems"])
        print(line.encode("ascii", "backslashreplace").decode())
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
