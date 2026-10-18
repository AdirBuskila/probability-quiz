# STATUS - probability

Resume here: phase 7 - ship (QA passed 2026-10-18, awaiting Adir / the orchestrator)
Opus sessions: 0 of 2
Engine: open   Format: open multi-part computation   Cutoff: 2024 onward (20 sittings, 24A-A ... 26A-B)

Triage material (private, names students, never copied into this repo): C:\Users\Adir\Desktop\Coding\Dev\course-factory\courses\probabilityormat_triage.md

Gates 1, 2 and 7 always stop for Adir.

- [x] Phase 0 - intake
  - [x] registry entry exists
  - [x] source folder exists and is non-empty
- [x] Phase 1 - triage  (GATE 1: Adir approves format, cutoff, topics)
  - [x] triager run per subfolder
  - [x] format_triage.md merged (verdict, cutoff, topics, engine choice)
  - [x] Adir approved
  - [x] config.overlay.json written, app repo scaffolded (triage stays in the factory)
- [x] Phase 2 - flagship  (GATE 2: Adir tries it in the browser)
  - [x] topic taxonomy chosen
  - [x] flagship sitting transcribed + validated (26A-B: 23 items, 20 in the bank, Q3a/b/d held, see ASK_ADIR; verified by tools/verify/26A-B/check.py: exact + Monte Carlo, 185 checks)
  - [x] steps (if open questions) + refuter pass
  - [x] smoke / verify_dom green, running locally
  - [x] Adir tried it
- [x] Phase 3 - bank
  - [x] all in-scope sittings transcribed (batches of <=4)
  - [x] validate.py clean
  - [x] solver run for questions with no trustworthy solution
  - [x] refuter: non-official all; official 20% sample (whole exam on any disagreement)
  - [x] arbiter / ASK_ADIR for disagreements
  - [x] completeness check per exam
- [x] Phase 4 - steps
  - [x] step-author batches done for every open question
  - [x] rubricSource / stepsSource labeled
  - [x] refuter on every steps block
- [x] Phase 5 - learn
  - [x] learn-writer per topic
  - [x] coverage report: no gaps
- [x] Phase 5b - need help
  - [x] 2-5 course areas approved at gate 1, `needHelp` in course.config.json
  - [x] learn-writer lessons + coverage table complete, step-author questions (bankId pulls marked)
  - [x] course_lint.js --strict clean, refuter (course_dump.js) clean, levels set to ai-verified
  - [x] tools/redact.txt filled, validate.py clean
- [x] Phase 6 - QA
  - [x] validate, build_questions, build_learn, smoke, verify_dom green
  - [x] shoot.js screenshots taken
  - [x] render-checker sweep clean
- [ ] Phase 7 - ship  (GATE 3: Adir OKs going public)
  - [ ] deck redesign done (else stop and tell Adir)
  - [ ] .gitignore excludes raw PNGs, favicon, GoatCounter, .nojekyll
  - [ ] year range checked against data
  - [ ] Adir OK to go public
  - [ ] GitHub repo + Pages live
  - [ ] deck tile added
  - [ ] registry status = live

## Notes

- 2026-10-18 phase 6 QA: 478 questions (20 sittings), 16 learn chapters, 6 guided courses / 55 levels; all tests green; render_audit 0 findings at 390px and 1000px; privacy_scan 0 real names (only the common word for counting matches a redact entry as a substring); escape scan 0. Bidi engine from the factory template (5e76199) plus a local fix: math-run is dir=rtl so sentence-final punctuation sits left of the formula. Sim/region labels go through the same isolates (Region.label).
