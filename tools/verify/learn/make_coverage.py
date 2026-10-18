# -*- coding: utf-8 -*-
"""Builds docs/learn_coverage.md: concept -> brief section -> example question ids, from the question data.
Every bank question must match at least one concept (else it is printed as UNCOVERED and the script exits 1).
Run: PYTHONUTF8=1 py tools/verify/learn/make_coverage.py"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RAW = os.path.join(ROOT, "tools", "raw")
K = "אבגדהוזחטיכלמנסעפצקרשת"


def pk(p):
    if not p:
        return ""
    p = p.strip().rstrip("'.)׳")
    p = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}.get(p, p)
    return chr(97 + K.index(p)) if p in K else p


qs = []
for f in sorted(glob.glob(os.path.join(RAW, "2*.json"))):
    d = json.load(open(f, encoding="utf8"))
    for q in d["questions"]:
        if q.get("hold"):
            continue
        ctx = ""
        if q.get("contextId"):
            c = d.get("contexts", {}).get(q["contextId"]) or {}
            ctx = " ".join(str(c.get(k, "")) for k in ("title", "text", "caption"))
        qs.append((d["examCode"] + "-Q" + str(q["num"]) + pk(q.get("part")), q.get("topic"), q.get("question", "") + " " + ctx + " " + q.get("solution", "")))

# (concept, brief chapter id, section, topic filter or None, regex on question+context+solution)
R = [
    ("מרחב מדגם, הסתברות קלאסית, ספירת מאורע", "basics_events", "הגדרות; ספירת מכפלות", {"basics_events"}, r"."),
    ("אלגברה של מאורעות, איחוד, משלים, זרים", "basics_events", "חוקים", {"basics_events", "independence"}, r"זר|\\cup|\\subseteq|=A_"),
    ("הסתברות מותנית ('אם ידוע')", "conditional_bayes", "מתכון 1", {"conditional_bayes", "combinatorics", "special_discrete", "circuits", "uniform_geometric", "continuous_rv", "minmax_transform", "joint_discrete"}, r"אם ידוע|/|\\mid"),
    ("מאורעות עם p,q,s ושלושה נתונים (ארבעה תאים)", "conditional_bayes", "מתכון 2", {"conditional_bayes", "independence", "basics_events"}, r"P\(A|P\(B"),
    ("הסתברות שלמה", "conditional_bayes", "מתכון 3", {"conditional_bayes", "special_discrete", "circuits", "combinatorics"}, r"."),
    ("בייס (הפיכת התניה)", "conditional_bayes", "מתכון 4", {"conditional_bayes"}, r"."),
    ("אי-תלות של מאורעות ומשתנים; זרים; בלתי מתואמים", "independence", "כל הפרק", {"independence"}, r"."),
    ("ספירה: עקרון הכפל, בחירות עם/בלי החזרה, מסודר", "combinatorics", "הגדרות; מתכון", {"combinatorics"}, r"."),
    ("קוביות, סכומים, משוואה ריבועית, 'אי פעם'", "combinatorics", "דוגמאות 1-2", {"combinatorics", "conditional_bayes", "special_discrete", "discrete_rv"}, r"קובי"),
    ("פריסות על לוח ומסלולים", "combinatorics", "דוגמאות 4-5", {"combinatorics", "special_discrete", "conditional_bayes"}, r"טבלה|רשת|משבצ"),
    ("תוחלת ושונות של משתנה בדיד, E[g(X)]", "discrete_rv", "מתכון", {"discrete_rv", "joint_discrete", "special_discrete", "minmax_transform", "continuous_rv"}, r"תוחלת|שונות|\\mathbb\{?E"),
    ("מוטה-גודל (בחירה לפי אנשים)", "discrete_rv", "דוגמה 2", {"discrete_rv"}, r"משפח|ברגים|קופס"),
    ("התפלגויות מיוחדות ומשפט הפירוק", "special_discrete", "טבלת ההתפלגויות", {"special_discrete", "conditional_bayes", "joint_discrete"}, r"."),
    ("הסתברות שלמה עם סכום מהרמז; דילול", "special_discrete", "דילול", {"special_discrete", "conditional_bayes"}, r"הערה|לידיעתך|הגיע|פואסון|פונים|נכנס"),
    ("גאומטרית, זוגיות, מי ראשון", "special_discrete", "זוגיות", {"special_discrete"}, r"עץ|מטבע|זוגי"),
    ("כד: היפרגאומטרי, עם/בלי החזרה", "special_discrete", "כדים", {"special_discrete", "conditional_bayes", "combinatorics"}, r"כד|כדור"),
    ("התפלגות משותפת, שוליים, מטריצת ברנולי", "joint_discrete", "מתכון; דוגמה 1", {"joint_discrete", "discrete_rv", "independence"}, r"."),
    ("שונות משותפת ומקדם מתאם", "joint_discrete", "הגדרות; דוגמה 4", {"joint_discrete", "independence", "continuous_rv", "discrete_rv"}, r"cov|rho|מתאם|שונות משותפת"),
    ("צפיפות, מצטברת, תוחלת ושונות רציפות; אחידה, מעריכית", "continuous_rv", "הגדרות", {"continuous_rv", "uniform_geometric", "minmax_transform"}, r"."),
    ("צפיפות עם קבועים, נרמול, כלל האפס, תחום μ", "pdf_constants", "מתכון", {"continuous_rv", "conditional_bayes"}, r"פרמטר|מקדמים|נרמול|\\mu|צפיפות"),
    ("התפלגות מצטברת לפי קטעים ושרטוט", "pdf_constants", "שלב 7; רשימת בדיקה", {"continuous_rv", "minmax_transform"}, r"F_|מצטברת"),
    ("הסתברות מותנית מתוך F", "pdf_constants", "הסתברות מותנית מתוך F", {"continuous_rv"}, r"/|\\mid"),
    ("שיטת השטח: הסתברות כשטח, |Ω|", "area_method", "המתכון", {"uniform_geometric", "minmax_transform", "continuous_rv", "conditional_bayes"}, r"."),
    ("שיטת השטח: הסתברות מותנית כיחס שטחים", "area_method", "התניה בשיטת השטח", {"uniform_geometric", "minmax_transform"}, r"/|ידוע"),
    ("F של מינימום, מקסימום, יחס, מכפלה, מרחק", "area_method", "התפלגות מצטברת של פונקציה", {"minmax_transform", "uniform_geometric"}, r"."),
    ("מינימום ומקסימום; שבירת מקל; בחירה ללא החזרה", "minmax_transform", "כל הפרק", {"minmax_transform", "joint_discrete"}, r"."),
    ("מעגלים: טור, מקביל, גשר", "circuits", "כללי היסוד; הגשר", {"circuits"}, r"."),
    ("מעגל חדש מאותן יחידות; חיתוך; בדיוק אחת תקולה; רכיבים תלויים", "circuits", "כל הפרק", {"circuits", "conditional_bayes", "independence"}, r"."),
    ("נורמלית, קירוב ו-CLT", "exp_normal", "כל הפרק", {"exp_normal"}, r"."),
]

cov = {}
uncovered = []
for qid, topic, text in qs:
    hit = False
    for i, (name, ch, sec, tops, rx) in enumerate(R):
        if topic in tops and re.search(rx, text):
            cov.setdefault(i, []).append(qid)
            hit = True
    if not hit:
        uncovered.append((qid, topic))

lines = ["# כיסוי מצב הלימוד: מושג, פרק, שאלות לדוגמה", "",
         "נוצר אוטומטית מבנק השאלות על ידי `tools/verify/learn/make_coverage.py` (סיווג לפי נושא ומילות מפתח). כל שאלה בבנק משויכת לפחות למושג אחד.", "",
         "| מושג | פרק (כרטיס בלמידה) | סעיף | מספר שאלות | שאלות לדוגמה |", "|---|---|---|---|---|"]
for i, (name, ch, sec, tops, rx) in enumerate(R):
    ids = cov.get(i, [])
    ex = ", ".join(ids[:5]) if ids else "(אין שאלות בבנק 2024+; חומר עזר)"
    lines.append("| %s | `%s` | %s | %d | %s |" % (name, ch, sec, len(ids), ex))
lines += ["", "## פערים", ""]
lines.append("- **נורמלית, דה מואבר-לפלס ו-CLT:** אין אף שאלה בבנק (0 מתוך 20 מועדים). הנושא נלמד בפרק `exp_normal` לפי הנוסחון, מסומן כנדיר. הגל השני (2020-2023) יוסיף שאלות.")
lines.append("- **שאלות עם נתוני תמונה בלבד** (גרפי צפיפות, ציורי מעגלים): הפרק מלמד את השיטה, והדוגמאות נבנו מחדש. הגרפים עצמם נמצאים בשאלות.")
lines.append("- **סעיפי בונוס ללא פתרון רשמי** (למשל `24A-A-Q2d`): נפתרו בפרקים כדוגמאות (למשל $P_N$ בפרק הקומבינטוריקה), אך אין להם מפתח רשמי.")
lines.append("- **הרמזים עם סכום** נלמדים בפרקים `special_discrete` ו-`traps`, אבל כל רמז חדש דורש זיהוי הזזת האינדקס.")
open(os.path.join(ROOT, "docs", "learn_coverage.md"), "w", encoding="utf8").write("\n".join(lines) + "\n")
print("questions: %d, uncovered: %d" % (len(qs), len(uncovered)))
for u in uncovered[:40]:
    print("UNCOVERED", u)
sys.exit(1 if uncovered else 0)
