# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pyrogram.errors.exceptions.forbidden_403 import (
    ChatSendMediaForbidden,
)
from . import (
    ParseMode,
    _try_purged,
    eor,
    get_text,
    is_url,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    screenshots,
)


@pytel.instruction("webss", outgoing=True)
async def _screenshots(client, message):
    url = get_text(message)
    if not url or not (is_url(url) is True):
        await eor(
            message,
            text="Provide a valid link!",
        )
        return

    x = await eor(
        message, text="Take a screenshot..."
    )
    try:
        file = await screenshots(
            url=url, download=False
        )
    except BaseException as excp:
        await eor(x, text=f"{excp}")
        return

    if file:
        try:
            z = await eor(
                x, text="Uploading..."
            )
            await client.send_photo(
                z.chat.id,
                photo=file,
                caption=(
                    "{} [PYTEL](https://github.com/kastaid/pytel)".format(
                        "Made using",
                    )
                    + "\n{} [KASTA ID 🇮🇩](t.me/kastaid)".format(
                        "a Project by",
                    )
                ),
                parse_mode=ParseMode.MARKDOWN,
                disable_notification=True,
            )
            await _try_purged(z, 2.5)
            return
        except ChatSendMediaForbidden:
            await eor(
                z,
                text="Sorry, <u>Chat Send Media Forbidden</u> in this Group.",
            )
            return
    else:
        await eor(
            x,
            text="Sorry, couldn't capture the screen.",
        )
        return


plugins_helper["webtools"] = {
    f"{random_prefixies(px)}webss [url]/[reply link]": "To capture the screen on the link.",
}
