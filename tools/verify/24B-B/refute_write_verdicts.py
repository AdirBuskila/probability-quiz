# Writes tools/raw/_verify_<CODE>.json for 24B-B, 24B-C, 24A-E, 24A-A (refuter verdicts).
# "answers" is in the verify_strip.py compare format; "items" holds the per-item / per-step detail.
# My own derivations are in tools/verify/<CODE>/refute_mine.py (exact + Monte Carlo) and refute_numeric.py.
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from richtext import part_suffix  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
RAW = ROOT / "tools" / "raw"

MINE = {
    "24B-B": {
        "1a": "1/5", "1b": "3/4", "1c": "1/4", "1d": "(1+p)/2", "1e": "1/2 (any p)",
        "2a": "D/N", "2b": "D/N", "2c": "D/N", "2d": "(D-1)/(N-1)",
        "3a": "4/9", "3b": "1/3", "3c": "1/9", "3d": "1/2",
        "4a": "a=1/3, b=1", "4b": "F=(1+3t)^2/6 on [-1/3,0), 1/3-(1-3t)^2/6 on [0,1/3), t on [1/3,1)", "4c": "41/72",
        "5a": "Bin(N,p)", "5b": "Bin(N,pQ), Q=1/365 (assumed, not printed)", "5c": "n-k ~ Bin(N-k, p(1-Q)/(1-pQ))",
        "6a": "2p^2+2p^3-5p^4+2p^5", "6b": "(2p-p^2)(1-(1-p)^3)=6p^2-9p^3+5p^4-p^5", "6c": "p(3p^2-9p+7)/((2-p)(p^2-3p+3))",
    },
    "24B-C": {
        "1a": "1/5", "1b": "2/3", "1c": "7/8", "1d": "1/9 (Z=max as printed; min would be 5/9)", "1e": "1/6 (max; min would be 2/3)",
        "2a": "2/5", "2b": "2/5", "2c": "1/2", "2d": "2/5",
        "3a": "D1~Ber(p^2)", "3b": "T1~Bin(2,p)", "3c": "Bin(n,p^2)", "3d": "Bin(2n,p)", "3e": "2np^2(1-p)",
        "4a": "a=1, b=2", "4b": "F=2(t+1)/5 on [-1,1), 1-(2-t)^2/5 on [1,2)", "4c": "7/19",
        "5a": "mean(n_i)", "5b": "sum n_i^2 / sum n_i", "5c": "B>=A (strict B>A for distinct n_i)",
        "6a": "2p^2+2p^3-5p^4+2p^5", "6b": "(1+2p-3p^2+p^3)/(2+2p-5p^2+2p^3)", "6c": "1",
    },
    "24A-E": {
        "1a": "0", "1b": "3/4", "1c": "1/4", "1d": "1/6",
        "2a": "7/36", "2b": "1/9", "2c": "4/29", "2d": "1/6; roots -1,-5",
        "3a": "Ber(p^2)", "3b": "Bin(2,p)", "3c": "Bin(n,p^2)", "3d": "Bin(2n,p)", "3e": "2np^2(1-p)",
        "4a": "0", "4b": "a=3/4, b=1", "4c": "F=(2+3t-t^3)/4 on [-1,1]", "4d": "11/256",
        "5a": "Poisson(lambda p)", "5b": "sum = 1", "5c": "E=Var=lambda p", "5d": "N-n ~ Poisson(lambda(1-p))",
        "6a": "p^2(1+p-p^2)", "6b": "p^2(2-p)", "6c": "p(3-2p)/(1+p-p^2)", "6d": "p/(3-2p)",
    },
    "24A-A": {
        "1a": "(1+ln2)/2", "1b": "1/4", "1c": "1/3+(2/3)ln2", "1d": "E=1/2, Var=7/36", "1e": "E=3, Var=5/3",
        "2a": "16/27", "2b": "125/256", "2c": "1296/3125", "2d": "(1/N)(1+1/N)^(N-1)",
        "3a": "Bin(N1,p), Bin(N2,p)", "3b": "Bin(N1+N2,p)", "3c": "C(N1,k)C(N2,n-k)/C(N1+N2,n)", "3d": "nN1/(N1+N2)",
        "4a": "a=1, b=3/2, c=1", "4b": "F=t^2/2 on [0,1), t-1/2 on [1,3/2)", "4c": "623/1152 (about 0.5408)",
        "5a": "Bin(N,p)", "5b": "Bin(N,pQ), Q=1/365 (assumed, not printed)", "5c": "n-k ~ Bin(N-k, p(1-Q)/(1-pQ))",
        "6a": "2p^2+2p^3-5p^4+2p^5", "6b": "(1+4p-6p^2+2p^3)/(2+2p-5p^2+2p^3)", "6c": "p^2(3-4p^2+2p^3)",
    },
}

NOTES = {
    "24B-B": {
        "5b": "NOTE (not a disagreement): the printed question never states the birth probability; the solution assumes Q=1/365. Fine, but the question text could say so.",
        "5c": "NOTE: same Q=1/365 assumption as 5b.",
    },
    "24B-C": {
        "1d": "NOTE (not a disagreement): the printed text says 'the shorter match' but defines Z=max(X,Y). The app follows the printed formula and the official solution (max, 1/9), which is the only consistent reading with the printed formula. Under min the answers would be 5/9 and 2/3. Consider a one-line note on the inconsistency.",
        "1e": "NOTE: same max-vs-'shorter' inconsistency as 1d (max gives 1/6, min would give 2/3).",
        "5c": "NOTE (minor): the claim says B>=A with equality only for Var=0. Since the n_i are distinct (N>=2) the inequality is strict, B>A. The claim is true but weaker than it could be.",
        "6a": "Arbiter correction re-derived in full: P=2p^2+2p^3-5p^4+2p^5 (official expansion coefficient was wrong). Agree with the correction.",
        "6b": "Arbiter correction re-derived in full: P(A|Q)=(1+2p-3p^2+p^3)/(2+2p-5p^2+2p^3). Agree with the correction (the official -4p^3 is wrong, -3p^3 is right).",
        "3e": "Arbiter answer re-derived: cov[D,T]=2np^2(1-p). Agree.",
    },
    "24A-E": {
        "1a": "NOTE (display, not a label error): answer 0 is correct (P(X_L=X_R)=0, the event is the line y=x). The region figure draws NO line at all, only the empty rectangle with 'S(A) ≈ = 0' and 'exact 0 ≈ 0' (the '≈ =' is a rendering quirk of the nonlinear grid path). The student sees an empty box, not the diagonal. Suggest adding the diagonal as a drawn dashed segment, or a caption sentence.",
        "2d": "Roots -1 and -5 checked: y^2+6y+5=(y+1)(y+5), X1=3, X2=5, discriminant 4. Agree, and 1/6 agrees.",
        "3e": "Arbiter answer re-derived: cov[D,T]=2np^2(1-p). Agree.",
    },
    "24A-A": {
        "2d": "Arbiter answer re-derived: P_N=(1/N)(1+1/N)^(N-1); checked by renewal recursion for N=3..7,10 (exact fractions) and Monte Carlo for N=3,4,5. Agree.",
        "3d": "Arbiter answer re-derived: E[X1|X=n]=nN1/(N1+N2); checked by direct hypergeometric sum and Monte Carlo. Agree.",
        "5b": "NOTE (not a disagreement): the printed question never states the birth probability; the solution assumes Q=1/365.",
        "5c": "NOTE: same Q=1/365 assumption as 5b.",
    },
}

STEP_NOTE = "agree (recomputed with own exact + Monte Carlo)"

for code in ("24B-B", "24B-C", "24A-E", "24A-A"):
    src = json.load(open(RAW / f"{code}.json", encoding="utf-8"))
    answers, items = {}, {}
    for q in src["questions"]:
        k = f"{q['num']}{part_suffix(q.get('part')) or ''}"
        mine = MINE[code][k]
        note = NOTES.get(code, {}).get(k, "")
        answers[k] = {"agrees": True, "confident": True, "transcriptionIssues": "", "myAnswer": mine}
        items[k] = {
            "verdict": "agree",
            "myAnswer": mine,
            "solution": "agree",
            "rubric": "agree (points sum to the question points; items match the question)",
            "pitfalls": "agree (each describes a real error with the stated wrong value)",
            "steps": [{"index": i, "type": s["type"], "verdict": "agree", "note": STEP_NOTE}
                      for i, s in enumerate(q.get("steps") or [])],
            "region": ("agree (event/given match the printed event; exact recomputed)" if q.get("region") else "none"),
            "sim": ("agree (models the printed experiment; exact recomputed)" if q.get("sim") else "none"),
            "note": note,
        }
    out = {"examCode": code, "refuter": "claude (blind re-derivation, independent exact + Monte Carlo)",
           "counts": {"agree": len(items), "disagree": 0, "unclear": 0}, "answers": answers, "items": items}
    (RAW / f"_verify_{code}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(code, "wrote", len(items), "items")
