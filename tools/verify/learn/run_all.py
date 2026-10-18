# -*- coding: utf-8 -*-
"""Run every learn-mode number check:  PYTHONUTF8=1 py tools/verify/learn/run_all.py
Exit code 1 if any check fails."""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common  # noqa: E402

MODULES = ["v1_basics", "v2_discrete", "v3_continuous", "v4_circuits_traps"]

for name in MODULES:
    if not os.path.exists(os.path.join(HERE, name + ".py")):
        print("skip (missing): " + name)
        continue
    importlib.import_module(name).run()

sys.exit(1 if common.report() else 0)
