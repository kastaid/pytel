# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    ParseMode,
    eor,
    fetch_adzan,
    get_text,
    plugins_helper,
    px,
    pytel,
    replied,
    _try_purged,
    random_prefixies,)


@pytel.instruction(
    [
        "dadzan",
        "dadzhan",
        "dazan",
    ],
    supersu=["PYTEL"],
)
@pytel.instruction(
    [
        "adzan",
        "adzhan",
        "azan",
    ],
    outgoing=True,
)
async def _adzhan(
    client, message
):
    str_city = get_text(
        message
    )
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
    await client.send_message(
        message.chat.id,
        text=get_info,
        disable_notification=True,
        parse_mode=ParseMode.HTML,
        reply_to_message_id=replied(
            message
        ),
    )
    return await _try_purged(
        x
    )


plugins_helper[
    "adzan"
] = {
    f"{random_prefixies(px)}adzan / azan [region city]/[reply text (region)]": "To get call to prayer information, according to the selected region.",
}
