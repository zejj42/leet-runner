"""The version: major.minor from pyproject.toml, then the number of commits, which grows by itself. 0.1.63"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .catalog import ROOT


def version(root: Path = ROOT, at: str = "HEAD") -> str:
    found = re.search(r'^version\s*=\s*"(\d+\.\d+)', (root / "pyproject.toml").read_text(), flags=re.M) \
        if (root / "pyproject.toml").exists() else None
    base = found.group(1) if found else "0.0"
    try:
        count = subprocess.check_output(["git", "-C", str(root), "rev-list", "--count", at], text=True,
                                        stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return base                                         # not a git clone
    return f"{base}.{count}"
