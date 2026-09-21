"""Makes `leetkit` importable from every problem folder, and adds the --stress switch."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def pytest_addoption(parser):
    parser.addoption("--stress", action="store_true", default=False, help="also run the large, slow cases")
