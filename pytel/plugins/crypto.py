# pytel < https://t.me/kastaid > Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    fetch_crypto,
    _try_purged,
    eor,
    get_text,
    suppress,
    plugins_helper,
    px,
    pytel,
    replied,
    random_prefixies,)


@pytel.instruction(
    [
        "crypto",
    ],
    outgoing=True,
)
async def _crypto_charts(
    client, message
):
    with suppress(BaseException):
        str_crypto = get_text(
            message, normal=True
        )
        if not str_crypto:
            await eor(
                message,
                text="Provide a valid Crypto Coins / BTC.",
            )
            return

        x = await eor(
            message,
            text=f"Fetching charts for **{str_crypto.upper()}**",
        )
        crypto_info = fetch_crypto(
            str_crypto
        )
        await client.send_message(
            message.chat.id,
            text=crypto_info,
            protect_content=True,
            reply_to_message_id=replied(
                message
            ),
            disable_web_page_preview=True,
        )
        return await _try_purged(x, 1.5)


plugins_helper["crypto"] = {
    f"{random_prefixies(px)}crypto [reply/text: btc/cryptocurrency]": "To fetching charts for bitcoin or cryptocurrency.",
}
