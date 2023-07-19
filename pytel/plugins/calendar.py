# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from calendar import month
from datetime import datetime
from typing import Optional
from pytanggalmerah import TanggalMerah
from . import (
    ParseMode,
    TimeZone,
    _try_purged,
    plugins_helper,
    px,
    tz,
    pytel,
    random_prefixies,)


def calendar_command() -> Optional[str]:
    u_1 = u_2 = u_3 = random_prefixies(
        px
    )
    calendar_cmd = """
<b>{} ›</b>

<i>{}.</i>

<code>{}calendar -now</code>
<code>{}calendar -m [{}]</code>

<b>{}:</b>
{} › <code>{}calendar -m jan/januari/january</code>

{}.
""".format(
        "Command Guide",
        "Calendar for this years",
        u_1,
        u_2,
        "month",
        "Example",
        "Execute",
        u_3,
        "Chouse a month",
    )
    return str(calendar_cmd)


m1 = [
    "jan",
    "januari",
    "january",
]
m2 = [
    "feb",
    "februari",
    "february",
]
m3 = [
    "mar",
    "maret",
    "march",
]
m4 = ["apr", "april"]
m5 = ["may", "mei"]
m6 = [
    "jun",
    "juni",
    "june",
]
m7 = [
    "jul",
    "juli",
    "july",
]
m8 = [
    "aug",
    "agustus",
    "august",
]
m9 = [
    "sep",
    "september",
]
m10 = [
    "oct",
    "oktober",
    "october",
]
m11 = [
    "nov",
    "november",
]
m12 = [
    "dec",
    "desember",
    "december",
]


@pytel.instruction(
    [
        "calendar -now",
        "calendar -m",
    ],
    outgoing=True,
    sensitive=False,
)
async def _calendar(client, message):
    point = message.text.split(None, 2)
    ye = datetime.now(tz).year
    da = datetime.now(tz).strftime(
        "<b>{}:</b> <u>%d/%m/%Y</u>\n<b>{}:</b> <u>%H:%M:%S</u>".format(
            "Date",
            "Time",
        ),
    )
    _ = TanggalMerah(
        cache_path=None,
        cache_time=600,
    )
    _.set_timezone(TimeZone)
    if _.is_holiday():
        dayoff = "".join(_.get_event())
    else:
        dayoff = "{}".format(
            "Now isn't a holiday."
        )
    try:
        if point[1] == "-now":
            mo = datetime.now(tz).month
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m1
        ):
            mo = 1
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m2
        ):
            mo = 2
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m3
        ):
            mo = 3
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m4
        ):
            mo = 4
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m5
        ):
            mo = 5
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m6
        ):
            mo = 6
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m7
        ):
            mo = 7
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m8
        ):
            mo = 8
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m9
        ):
            mo = 9
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m10
        ):
            mo = 10
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m11
        ):
            mo = 11
            ca = month(
                ye,
                mo,
                2,
                1,
            )

        elif (
            point[1] == "-m"
            and point[2] in m12
        ):
            mo = 12
            ca = month(
                ye,
                mo,
                2,
                1,
            )

    except BaseException:
        exam = calendar_command()
        await message.reply(
            "{}".format(str(exam)),
            parse_mode=ParseMode.HTML,
            disable_notification=True,
        )
        return await _try_purged(
            message,
            3.5,
        )

    date_and_time = """
<strong><i>{}:</i></strong>

<code>{}</code>
<u><b>{}</u></b>
{}
<b>{}:</b> <u>{}</u>
""".format(
        "The month you requested",
        ca,
        "Now",
        da,
        "Day off",
        dayoff,
    )
    await message.reply(
        date_and_time,
        parse_mode=ParseMode.HTML,
        disable_notification=True,
    )
    return await _try_purged(
        message, 3.5
    )


plugins_helper["calendar"] = {
    f"{random_prefixies(px)}calendar -now": "Get calendar for now.",
    f"{random_prefixies(px)}calendar -m [month]": "Get calendar month information.",
}
