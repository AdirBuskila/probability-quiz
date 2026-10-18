# -*- coding: utf-8 -*-
"""Generator for tools/raw/DEMO-P.json -- the probability extras demo (area figures + "simulate it").
NEVER SHIPPED: build_questions.py skips DEMO-* unless run with --demo (for tools/verify_dom.js and screenshots).
Run: PYTHONUTF8=1 py tools/gen/gen_DEMO-P.py && PYTHONUTF8=1 py tools/build_questions.py --demo
     node tools/verify_dom.js && PYTHONUTF8=1 py tools/build_questions.py      (rebuild without the demo)
Each sim / region here is checked by tools/check_sim_specs.py like any real one."""
import json, math, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "DEMO-P.json"
U2 = {"x": [0, 1], "y": [0, 1]}
XY = {"x": "X", "y": "Y"}


def Q(num, part, topic, question, solution, **kw):
    q = {"num": num, "kind": "computation", "topic": topic, "question": question, "solution": solution,
         "solutionSource": "solved", "official": False, "confidence": "high", "points": 5}
    if part:
        q["part"] = part
    q.update(kw)
    return q


band = {"space": U2, "labels": XY, "exact": 0.75,
        "event": [{"a": 1, "b": -1, "c": 0.5, "op": "<"}, {"a": 1, "b": -1, "c": -0.5, "op": ">"}],
        "caption": "המאורע |X-Y|<1/2 בתוך ריבוע היחידה"}
cond = {"space": U2, "labels": XY, "exact": 0.25,
        "event": [{"a": 1, "c": 0.5, "op": "<"}], "given": [{"a": 1, "b": 1, "c": 1, "op": ">"}],
        "caption": "המאורע X<1/2 בהינתן X+Y>1"}
hyper = {"space": U2, "labels": XY, "exact": 0.5 + math.log(2) / 2,
         "event": [{"expr": "x*y", "op": "<", "c": 0.5}], "caption": "המאורע XY<1/2 (שפה עקומה)"}

questions = [
    Q(1, "א", "uniform_geometric",
      r"[דמו] $X,Y\sim U(0,1)$ בלתי תלויים. חשבו את $P(|X-Y|<\tfrac12)$.",
      r"ההסתברות שווה לשטח. המשלים הוא שני משולשים ששטח כל אחד $\tfrac18$, ולכן $P=1-\tfrac14=\tfrac34$.",
      region=band,
      sim={"kind": "area", "params": {"fromRegion": True}, "estimate": "P(|X-Y|<1/2)", "exact": 0.75},
      steps=[{"type": "numeric", "prompt": r"מה השטח של אחד משני המשולשים הלבנים באיור?", "answer": 0.125, "tol": 1e-9,
              "region": band, "explain": r"משולש ישר זווית עם ניצבים $\tfrac12$: שטחו $\tfrac18$."}],
      stepsSource="ai-verified"),
    Q(1, "ב", "uniform_geometric",
      r"[דמו] חשבו את $P(X<\tfrac12 \mid X+Y>1)$.",
      r"השטח של התנאי הוא $\tfrac12$ והשטח של החיתוך הוא $\tfrac18$, ולכן $P=\tfrac{1/8}{1/2}=\tfrac14$.",
      region=cond,
      sim={"kind": "area", "params": {"fromRegion": True}, "estimate": "P(X<1/2 | X+Y>1)", "exact": 0.25}),
    Q(1, "ג", "uniform_geometric",
      r"[דמו] חשבו את $P(XY<\tfrac12)$.",
      r"$P=\tfrac12+\int_{1/2}^1\frac{1}{2x}\,dx=\tfrac12+\tfrac12\ln 2$.",
      region=hyper,
      sim={"kind": "area", "params": {"space": U2, "event": "x*y < 1/2"}, "estimate": "P(XY<1/2)",
           "exact": 0.5 + math.log(2) / 2}),
    Q(2, None, "circuits",
      r"[דמו] רכיב $A$ (אמינות $0.9$) מחובר בטור למקבץ מקבילי של $B$ ($0.8$) ו-$C$ ($0.7$). מה ההסתברות שהמעגל עובד?",
      r"$P=0.9\cdot(1-0.2\cdot 0.3)=0.846$.",
      sim={"kind": "circuit", "estimate": "P(S)", "exact": 0.846,
           "params": {"event": "S", "network": {"type": "series", "children": [
               {"type": "comp", "id": "A", "p": 0.9},
               {"type": "parallel", "children": [{"type": "comp", "id": "B", "p": 0.8}, {"type": "comp", "id": "C", "p": 0.7}]}]}}}),
    Q(3, None, "continuous_rv",
      r"[דמו] ל-$X$ צפיפות $f(x)=3x^2$ על $(0,1)$. חשבו את $P(X>\tfrac12)$.",
      r"$P=\int_{1/2}^1 3x^2\,dx=1-\tfrac18=\tfrac78$.",
      sim={"kind": "pdf", "estimate": "P(X>1/2)", "exact": 0.875,
           "params": {"pieces": [{"from": 0, "to": 1, "expr": "3*x^2"}], "event": "x > 1/2"}}),
    Q(4, None, "conditional_bayes",
      r"[דמו] מטילים שתי קוביות הוגנות. מה ההסתברות שסכומן $7$, בהינתן שהקובייה הראשונה זוגית?",
      r"לכל ערך של הקובייה הראשונה יש בדיוק ערך אחד של השנייה שמשלים ל-$7$, ולכן $P=\tfrac16$.",
      sim={"kind": "dice", "estimate": "P(sum = 7 | d1 even)", "exact": 1 / 6,
           "params": {"n": 2, "event": "sum == 7", "given": "d1 % 2 == 0"}}),
]

exam = {"examCode": "DEMO-P", "examLabel": "[דמו] הדגמת שיטת השטח והסימולציה", "year": 2026, "questions": questions}
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
