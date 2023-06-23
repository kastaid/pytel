# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from pathlib import Path
from shutil import rmtree
from time import time
from pyrogram import Client
from .client import PytelClient
from .config import (
    API_ID,
    API_HASH,
    SESSION1,
    SESSION2,
    SESSION3,
    SESSION4,
    SESSION5,
    TGB_TOKEN,
)
from .logger import pylog as send_log

__license__ = "GNU Affero General Public License v3.0"
__copyright__ = "PYTEL Copyright (C) 2023-present kastaid"

start_time = time()

Rooters: Path = Path(__file__).parent.parent


try:
    pytel_tgb = Client(
        name="pytel",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=TGB_TOKEN,
        in_memory=True,
    )
    pytel_1 = (
        PytelClient(
            name="pytel1",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION1,
        )
        if SESSION1
        else None
    )
    pytel_2 = (
        PytelClient(
            name="pytel2",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION2,
        )
        if SESSION2
        else None
    )
    pytel_3 = (
        PytelClient(
            name="pytel3",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION3,
        )
        if SESSION3
        else None
    )
    pytel_4 = (
        PytelClient(
            name="pytel4",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION4,
        )
        if SESSION4
        else None
    )
    pytel_5 = (
        PytelClient(
            name="pytel5",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION5,
        )
        if SESSION5
        else None
    )
    pytel = PytelClient(name="pytel")
except Exception as excp:
    send_log.error(excp)

pytelist = [_ for _ in [pytel_1, pytel_2, pytel_3, pytel_4, pytel_5] if _]

if pytel:
    for pytel_ in pytelist:
        pytel._client.append(pytel_)
else:
    pytel = None


dirs = "cache/"
for _ in dirs:
    if not (Rooters / _).exists():
        (Rooters / _).mkdir(parents=True, exist_ok=True)
    else:
        for f in (Rooters / _).rglob("*"):
            if f.is_dir():
                rmtree(f)
            else:
                f.unlink(missing_ok=True)
