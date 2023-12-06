# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

import asyncio
import signal
from contextlib import (
    suppress,)
from os import (
    getpid,
    close,)
from signal import (
    signal as signal_name,
    SIGINT,
    SIGTERM,
    SIGABRT,)
from typing import (
    Any,
    Optional,)
import psutil
from .client import (
    Instagram,)
from .client.dbase.dbMessaging import (
    clear_all_schedule,
    clear_all_dspam,)
from .logger import pylog

signals = {
    k: v
    for v, k in signal.__dict__.items()
    if v.startswith(
        "SIG"
    )
    and not v.startswith(
        "SIG_"
    )
}


async def pytasks(
    confirm: Optional[
        bool
    ],
    client: Any,
):
    """
    TASKS :: Client
    """
    tasks = None

    def signal_handler(
        signum, __
    ):
        pylog.info(
            f"🛑 Stop signal received ({signals[signum]})."
        )
        pylog.info(
            "🚫 Tasks cancellation..."
        )
        for a in client:
            pylog.success(
                f"🏃 Exiting for User ID ( {a.me.id} )"
            )
            clear_all_dspam(
                a.me.id
            )
            clear_all_schedule(
                a.me.id
            )
            for (
                b
            ) in asyncio.all_tasks(
                a.loop
            ):
                b.cancel()
        pylog.info(
            "👋 See you next time !",
        )
        Instagram.loged_out(
            crash=True
        )
        tasks.cancel()
        with suppress(
            Exception
        ):
            proc = psutil.Process(
                getpid()
            )
            for _ in (
                proc.open_files()
                + proc.connections()
            ):
                close(
                    _.fd
                )

    for s in (
        SIGINT,
        SIGTERM,
        SIGABRT,
    ):
        signal_name(
            s,
            signal_handler,
        )
    while confirm:
        tasks = asyncio.create_task(
            asyncio.sleep(
                99999
            )
        )
        try:
            await tasks
        except (
            asyncio.CancelledError
        ):
            break
