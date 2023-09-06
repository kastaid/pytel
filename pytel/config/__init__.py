"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from pathlib import Path
from sys import exit
from pytel.logger import (
    pylog as send_log,)

Checker: Path = Path(
    __file__
).parent.parent

directory = ["config.env"]
for b in directory:
    for a in (Checker / b).rglob("*.*"):
        if not a.exists():
            send_log.warning(
                "File config.env not found !!"
            )
            exit(1)

try:
    from .configuration import *

    if not TGB_TOKEN:
        send_log.warning(
            "Please make a Bot from @BotFather and add it's token in TGB_TOKEN."
        )
        exit(1)
    if (
        not IG_USN
        or not IG_PASS
        or not IG_SECRET
    ):
        send_log.warning(
            "Please fill in the Instagram variables correctly."
        )
        exit(1)
except ImportError as excp:
    send_log.exception(excp)
    exit(1)
