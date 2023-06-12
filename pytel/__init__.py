# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from pathlib import Path
from time import time
from .client import pytel

start_time = time()

Rooters: Path = Path(__file__).parent.parent

dirs = ["cache", "logs"]
for _ in dirs:
    if not (Rooters / _).exists():
        (Rooters / _).mkdir(parents=True, exist_ok=True)
    else:
        for f in (Rooters / _).rglob("*.*"):
            if f.exists():
                f.unlink(missing_ok=True)
