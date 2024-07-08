from __future__ import annotations

from os import getenv
import os

AXES_ENABLED = os.environ.get("AXES_ENABLED", default="true").lower() == "true"
AXES_FAILURE_LIMIT = int(os.environ.get("AXES_FAILURE_LIMIT", default="50"))


