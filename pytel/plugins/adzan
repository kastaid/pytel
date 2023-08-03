# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    ParseMode,
    _try_purged,
    eor,
    fetch_adzan,
    get_text,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    suppress,)


@pytel.instruction(
    [
        "adzan",
        "adzhan",
        "azan",
    ],
    outgoing=True,
)
async def _adzan(client, message):
    with suppress(BaseException):
        str_city = get_text(message)
        if not str_city:
            await eor(
                message,
                text="Provide a valid Region or City.",
            )
            return

        x = await eor(
            message,
            text=f"Fetches to prayer data for the **{str_city.capitalize()}**",
        )
        get_info = await fetch_adzan(
            str_city
        )
        await x.reply(
            get_info,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
        )
        return await _try_purged(x, 1.5)


plugins_helper["adzan"] = {
    f"{random_prefixies(px)}adzan [region city]/[reply text]": "To get call to prayer information, according to the selected region.",
}
