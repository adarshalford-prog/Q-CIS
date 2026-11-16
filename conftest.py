"""Make ``src`` and the repository root importable when running pytest from the root."""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(ROOT, "src"), ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)
