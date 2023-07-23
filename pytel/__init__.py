"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from asyncio import (
    get_event_loop,
    set_event_loop_policy,)
from uvloop import EventLoopPolicy
from version import __version__ as pyver
from .logger import pylog as send_log

set_event_loop_policy(EventLoopPolicy())

loopers = get_event_loop()

try:
    from os import cpu_count
    from pathlib import Path
    from platform import uname
    from shutil import rmtree
    from sys import exit
    from time import time
    from .client import PytelClient
    from .config import (
        API_HASH, API_ID, SESSION1,
        SESSION2, SESSION3, SESSION4,
        SESSION5, SESSION6, SESSION7,
        SESSION8, SESSION9, SESSION10,
        TGB_TOKEN,)
except Exception as excp:
    send_log.exception(excp)

__license__ = "GNU Affero General Public License v3.0"
__copyright__ = "PYTEL Copyright (C) 2023-present kastaid"

start_time = time()

Rooters: Path = Path(
    __file__
).parent.parent

dirs = "cache/"
if not (Rooters / dirs).exists():
    (Rooters / dirs).mkdir(
        parents=True,
        exist_ok=True,
    )
else:
    for f in (Rooters / dirs).rglob(
        "*"
    ):
        if f.is_dir():
            rmtree(f)
        else:
            f.unlink(missing_ok=True)

APP_VERSION = f"PYTEL-Premium v.{pyver}"
WORKERS = min(
    64, (cpu_count() or 0) + 8
)
SYSTEM_VERSION = f"{uname().system}"
DEVICE_MODEL = f"{uname().machine}"

try:
    from pyrogram import Client

    pytel_tgb = Client(
        name="pytel",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=TGB_TOKEN,
        in_memory=True,
        ipv6=False,
    )
    pytel_1 = (
        PytelClient(
            name="pytel1",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION1,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
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
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
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
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
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
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
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
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION5
        else None
    )
    pytel_6 = (
        PytelClient(
            name="pytel6",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION6,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION6
        else None
    )
    pytel_7 = (
        PytelClient(
            name="pytel7",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION7,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION7
        else None
    )
    pytel_8 = (
        PytelClient(
            name="pytel8",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION8,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION8
        else None
    )
    pytel_9 = (
        PytelClient(
            name="pytel9",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION9,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION9
        else None
    )
    pytel_10 = (
        PytelClient(
            name="pytel10",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION10,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION10
        else None
    )
    pytel = PytelClient(
        name="pytel", lang_code="en"
    )
except Exception as excp:
    send_log.exception(excp)
    exit(1)

pytl = [
    _
    for _ in [
        pytel_1,
        pytel_2,
        pytel_3,
        pytel_4,
        pytel_5,
        pytel_6,
        pytel_7,
        pytel_8,
        pytel_9,
        pytel_10,
    ]
    if _
]

if pytel:
    for pytel_ in pytl:
        pytel._client.append(pytel_)
else:
    pytel = None
