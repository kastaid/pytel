"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from .checker import check_pypi_version
from .logger import pylog as send_log

check_pypi_version()

try:
    from asyncio import (
        get_event_loop,
        set_event_loop_policy,
        DefaultEventLoopPolicy,
        SelectorEventLoop,)
    from selectors import SelectSelector
    from requests.exceptions import (
        ChunkedEncodingError,)
    from urllib3.exceptions import (
        IncompleteRead, ProtocolError,)

    #    from uvloop import EventLoopPolicy
    from version import (
        __version__ as pyver,)
except KeyboardInterrupt:
    send_log.warning(
        "Received interrupt while import"
    )
except Exception as excp:
    send_log.exception(excp)


class MyPolicy(DefaultEventLoopPolicy):
    def new_event_loop(self):
        selector = SelectSelector()
        return SelectorEventLoop(
            selector
        )


set_event_loop_policy(MyPolicy())
loopers = get_event_loop()

try:
    from os import cpu_count
    from pathlib import Path
    from platform import (
        uname, system, machine,)
    from shutil import rmtree
    from sys import (
        platform, maxsize, version_info,
        exit,)
    from time import time
    from pyrogram.errors.exceptions.unauthorized_401 import (
        Unauthorized,)
    from .client import PytelClient
    from .config import (
        API_HASH, API_ID, SESSION1,
        SESSION2, SESSION3, SESSION4,
        SESSION5, SESSION6, SESSION7,
        SESSION8, SESSION9, SESSION10,
        BOT_SESSION, TGB_TOKEN, API_ID1,
        API_HASH1, API_ID2, API_HASH2,
        API_ID3, API_HASH3, API_ID4,
        API_HASH4, API_ID5, API_HASH5,
        API_ID6, API_HASH6, API_ID7,
        API_HASH7, API_ID8, API_HASH8,
        API_ID9, API_HASH9, API_ID10,
        API_HASH10,)
except KeyboardInterrupt:
    send_log.warning(
        "Received interrupt while import"
    )
except IncompleteRead as i:
    send_log.exception(
        f"HTTP Response, ERROR: {i}"
    )
except ProtocolError as p:
    send_log.exception(
        f"Connection Broken, ERROR: {p}"
    )
except ChunkedEncodingError as c:
    send_log.exception(
        f"Connection Error, ERROR: {c}"
    )
except Exception as excp:
    send_log.exception(excp)

__license__ = "GNU Affero General Public License v3.0"
__copyright__ = "PYTEL Copyright (C) 2023-present kastaid"

start_time = time()


if (
    platform.startswith("linux")
    and maxsize == 2**63 - 1
):
    platform = system()
    machine = machine()
    if machine.startswith("aarch64"):
        mch = "📱"
    else:
        mch = "💻"
    send_log.info(
        "{} Starting-up on the system {} {}".format(
            mch,
            str(platform),
            str(machine),
        )
    )
else:
    platform = system()
    architecture = "64-bit"
    send_log.warning(
        "You've to use {} {} system first!".format(
            str(platform), architecture
        )
    )
    exit(1)


if (
    version_info.major == 3
    and version_info.minor >= 8
    and version_info.micro >= 0
):
    major = version_info.major
    minor = version_info.minor
    micro = version_info.micro
    send_log.info(
        "And running PYTEL on the Python {}.{}.{}".format(
            str(round(major)),
            str(round(minor)),
            str(round(micro)),
        )
    )
else:
    major = 3
    minor = 9
    send_log.warning(
        "You've to use python version of at least >= {}.{}.x ! quitting...".format(
            str(round(major)),
            str(round(minor)),
        )
    )
    exit(1)

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
    64, (cpu_count() or 1) + 1
)
SYSTEM_VERSION = f"{uname().system}"
DEVICE_MODEL = f"{uname().machine}"

try:
    import pyroaddon
    from pyrogram import Client

    pytel_tgb = Client(
        name="pytel_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=TGB_TOKEN,
        session_string=BOT_SESSION,
        in_memory=True,
        no_updates=False,
        ipv6=False,
    )
except KeyboardInterrupt:
    send_log.warning(
        "Received interrupt while import"
    )
except Unauthorized as excp:
    send_log.warning(
        f"SESSION Unauthorized coz: {excp}"
    )
    exit(1)
except Exception as excp:
    send_log.exception(excp)
    exit(1)

try:
    pytel_1 = (
        PytelClient(
            name="pytel1",
            api_id=API_ID1,
            api_hash=API_HASH1,
            session_string=SESSION1,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION1
        and API_ID1
        and API_HASH1
        else None
    )
    pytel_2 = (
        PytelClient(
            name="pytel2",
            api_id=API_ID2,
            api_hash=API_HASH2,
            session_string=SESSION2,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION2
        and API_ID2
        and API_HASH2
        else None
    )
    pytel_3 = (
        PytelClient(
            name="pytel3",
            api_id=API_ID3,
            api_hash=API_HASH3,
            session_string=SESSION3,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION3
        and API_ID3
        and API_HASH3
        else None
    )
    pytel_4 = (
        PytelClient(
            name="pytel4",
            api_id=API_ID4,
            api_hash=API_HASH4,
            session_string=SESSION4,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION4
        and API_ID4
        and API_HASH4
        else None
    )
    pytel_5 = (
        PytelClient(
            name="pytel5",
            api_id=API_ID5,
            api_hash=API_HASH5,
            session_string=SESSION5,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION5
        and API_ID5
        and API_HASH5
        else None
    )
    pytel_6 = (
        PytelClient(
            name="pytel6",
            api_id=API_ID6,
            api_hash=API_HASH6,
            session_string=SESSION6,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION6
        and API_ID6
        and API_HASH6
        else None
    )
    pytel_7 = (
        PytelClient(
            name="pytel7",
            api_id=API_ID7,
            api_hash=API_HASH7,
            session_string=SESSION7,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION7
        and API_ID7
        and API_HASH7
        else None
    )
    pytel_8 = (
        PytelClient(
            name="pytel8",
            api_id=API_ID8,
            api_hash=API_HASH8,
            session_string=SESSION8,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION8
        and API_ID8
        and API_HASH8
        else None
    )
    pytel_9 = (
        PytelClient(
            name="pytel9",
            api_id=API_ID9,
            api_hash=API_HASH9,
            session_string=SESSION9,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION9
        and API_ID9
        and API_HASH9
        else None
    )
    pytel_10 = (
        PytelClient(
            name="pytel10",
            api_id=API_ID10,
            api_hash=API_HASH10,
            session_string=SESSION10,
            in_memory=True,
            lang_code="en",
            ipv6=False,
            no_updates=False,
            sleep_threshold=60,
            app_version=APP_VERSION,
            system_version=SYSTEM_VERSION,
            device_model=DEVICE_MODEL,
            workers=WORKERS,
        )
        if SESSION10
        and API_ID10
        and API_HASH10
        else None
    )
    pytel = PytelClient(
        name="pytel", lang_code="en"
    )
except KeyboardInterrupt:
    send_log.warning(
        "Received interrupt while import"
    )
except Unauthorized as excp:
    send_log.warning(
        f"SESSION Unauthorized coz: {excp}"
    )
    exit(1)
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
        try:  # noqa
            if (
                pytel_
                not in pytel._client
            ):
                pytel._client.append(
                    pytel_
                )
            else:
                pass
        except Exception:
            pass
else:
    pytl = None
