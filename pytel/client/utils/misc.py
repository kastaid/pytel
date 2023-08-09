# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from datetime import date
from html import escape
from random import choice
from re import sub
from subprocess import (
    SubprocessError,
    run,)
from typing import (
    List,
    Optional,
    Union,
    Any,)
from pytelibs import _i
from pytz import timezone
from pytel.config import TimeZone
from pytel.logger import (
    pylog as send_log,)

tz = timezone(TimeZone)
SIZE_UNITS = [
    "B",
    "KB",
    "MB",
    "GB",
    "TB",
    "PB",
    "EB",
]


def gg_restricted() -> None:
    RunningCommand(_i)


def random_prefixies(
    px: Union[str, List[str]]
) -> Optional[str]:
    if px:
        prefixies = choice(px)
    return str(prefixies)


def escape_markdown(
    text,
):
    escape_chars = r"\*_`\[}{"
    return sub(
        r"([%s])" % escape_chars,
        r"\\\1",
        text,
    )


def mention_html(user_id, name):
    return '<a href="tg://user?id={}">{}</a>'.format(
        user_id,
        escape(name),
    )


def mention_markdown(user_id, name):
    return (
        "[{}](tg://user?id={})".format(
            escape_markdown(name),
            user_id,
        )
    )


def short_dict(
    dct: Optional[dict],
    reverse: Optional[bool] = False,
) -> Optional[dict]:
    return dict(
        sorted(
            dct.items(), reverse=reverse
        )
    )


def humanboolean(
    x: Optional[bool] = False,
) -> Optional[str]:
    return "Yes" if x else "No"


def time_formatter(
    ms: Union[int, float]
) -> str:
    (
        minutes,
        seconds,
    ) = divmod(
        int(ms / 1000),
        60,
    )
    (
        hours,
        minutes,
    ) = divmod(minutes, 60)
    (
        days,
        hours,
    ) = divmod(hours, 24)
    (
        weeks,
        days,
    ) = divmod(days, 7)
    tmp = (
        (
            (str(weeks) + "w, ")
            if weeks
            else ""
        )
        + (
            (str(days) + "d, ")
            if days
            else ""
        )
        + (
            (str(hours) + "h, ")
            if hours
            else ""
        )
        + (
            (str(minutes) + "m, ")
            if minutes
            else ""
        )
        + (
            (str(seconds) + "s, ")
            if seconds
            else ""
        )
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
        (
            stdout,
            stderr,
        ) = (
            process.stdout,
            process.stderr,
        )
        return str(stdout), str(stderr)
    except SubprocessError as excp:
        send_log.error(excp)


def size_bytes(size_in_bytes):
    if size_in_bytes is None:
        return "0B"
    index = 0
    while (
        size_in_bytes >= 1024
        and index < len(SIZE_UNITS) - 1
    ):
        size_in_bytes /= 1024
        index += 1
    return (
        f"{size_in_bytes:.2f}{SIZE_UNITS[index]}"
        if index > 0
        else f"{size_in_bytes}B"
    )


def subs_like_view_format(
    num_count: Union[int, float],
    precision=2,
) -> Optional[str]:
    suffixes = [
        "",
        "K",
        "M",
        "B",
        "T",
        "Q",
    ]
    m = sum(
        [
            abs(num_count / 1000.0**x)
            >= 1
            for x in range(
                1, len(suffixes)
            )
        ]
    )
    return f"{num_count/1000.0**m:.{precision}f}{suffixes[m]}"


def int2date(
    argdate: Optional[int],
) -> Optional[Any]:
    year = int(argdate / 10000)
    month = int((argdate % 10000) / 100)
    day = int(argdate % 100)
    return date(
        year, month, day
    ).strftime("%d %B %Y")
