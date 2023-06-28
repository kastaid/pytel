# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

import asyncio
from base64 import b64decode
from subprocess import SubprocessError
from typing import Union, Optional
from pytel.logger import pylog as send_log

_c, _g, _l, _d = (
    b64decode("a2FzdGFpZA==").decode("utf-8"),
    b64decode("a2FzdGFvdA==").decode("utf-8"),
    b64decode("QExQTV9MaW51eA==").decode("utf-8"),
    b64decode("QGRpcnR5c291bHZWdg==").decode("utf-8"),
)


def time_formatter(ms: Union[int, float]) -> str:
    minutes, seconds = divmod(int(ms / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w, ") if weeks else "")
        + ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
    )
    return tmp and tmp[:-2] or "0s"


async def RunningCommand(
    cmd: Optional[str],
) -> (bytes, bytes):
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        err = stderr.decode().strip()
        out = stdout.decode().strip()
        return out, err
    except SubprocessError as excp:
        send_log.error(excp)
