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
    fetch_weather,
    get_text,
    plugins_helper,
    px,
    pytel,
    replied,
    random_prefixies,)


@pytel.instruction(
    [
        "weather",
        "cuaca",
    ],
    outgoing=True,
)
async def _weather(
    client, message
):
    region = get_text(
        message
    )
    if not region:
        await eor(
            message,
            text="Provide a valid Region or City.",
        )
        return
    x = await eor(
        message,
        text=f"Fetches weather data for the <u>{region.capitalize()}</u>",
    )
    get_info = await fetch_weather(
        region
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
    "weather"
] = {
    f"{random_prefixies(px)}weather / {random_prefixies(px)}cuaca [region/city]/[reply]": "To get weather information.",
}
