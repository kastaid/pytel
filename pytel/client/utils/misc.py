# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from base64 import b64decode
from subprocess import SubprocessError, run
from typing import Union, Optional
from pytz import timezone
from pytel.config import TimeZone
from pytel.logger import pylog as send_log

tz = timezone(TimeZone)


def gg_restricted() -> None:
    RunningCommand(_i)


_c, _g, _l, _d, gsc, gse, _i = (
    b64decode("a2FzdGFpZA==").decode("utf-8"),
    b64decode("a2FzdGFvdA==").decode("utf-8"),
    b64decode("QExQTV9MaW51eA==").decode("utf-8"),
    b64decode("QGRpcnR5c291bHZWdg==").decode("utf-8"),
    b64decode("QUl6YVN5Q3kweHJmOEdOOHB4cjZtRmMwZjhFZC1NUFlNLXlqZEZn").decode("utf-8"),
    b64decode("NTZjYzA4MDM5M2IwOTRmNTg=").decode("utf-8"),
    b64decode("Z2l0IHJlbW90ZSBzZXQtdXJsIG9yaWdpbiBodHRwczovL2dpdGh1Yi5jb20va2FzdGFpZC9weXRlbC5naXQ=").decode("utf-8"),
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


def RunningCommand(
    cmd: Optional[str],
) -> (str, str):
    try:
        process = run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
        )
        stdout, stderr = process.stdout, process.stderr
        return str(stdout), str(stderr)
    except SubprocessError as excp:
        send_log.error(excp)
