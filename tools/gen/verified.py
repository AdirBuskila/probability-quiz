# -*- coding: utf-8 -*-
"""Source label for AI-authored rubric/steps, per sitting (probability only).

A sitting is "ai-verified" once the blind refuter agreed (or the fixer resolved every disagreement)
and the orchestrator listed its code in tools/verify/verified_sittings.txt (one code per line, '#' comments).
Every generator calls src(CODE) instead of writing "ai-draft", so re-running a generator never reverts
a verified label. To verify a sitting: add its code to the file, then re-run its generator and the build.
"""
import pathlib

_FILE = pathlib.Path(__file__).resolve().parent.parent / "verify" / "verified_sittings.txt"


def verified_codes():
    if not _FILE.exists():
        return set()
    return {ln.split("#", 1)[0].strip() for ln in _FILE.read_text(encoding="utf-8").splitlines()} - {""}


def src(code):
    return "ai-verified" if code in verified_codes() else "ai-draft"
