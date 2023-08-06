# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from pyrogram.raw.functions.messages import (
    DeleteHistory,)
from . import (
    ChatSendMediaForbidden,
    _try_purged,
    eor,
    get_text,
    is_url,
    plugins_helper,
    px,
    pytel,
    random_prefixies,)


@pytel.instruction(
    ["socmed"],
    outgoing=True,
)
async def _socmed(client, message):
    str_link = get_text(
        message,
        save_link=True,
    )
    if not str_link or not (
        is_url(str_link) is True
    ):
        await eor(
            message,
            text="Provide a valid link!",
        )
        return

    smd = "@SaveAsBot"
    x = await eor(
        message,
        text="Getting social media...",
    )

    await client.unblock_user(smd)
    _ = await client.send_message(
        smd, str_link
    )
    await sleep(9)
    async for social_media in client.search_messages(
        smd,
    ):
        try:
            if social_media.video:
                await social_media.copy(
                    message.chat.id,
                    caption="(c) @kastaid #pytel",
                    reply_to_message_id=message.id,
                )
                await _try_purged(x)
        except ChatSendMediaForbidden:
            await eor(
                x,
                text="Sorry, <u>Chat Send Media Forbidden</u> in this Group.",
            )
            return

    await sleep(5)
    del_his = await client.resolve_peer(
        smd
    )
    return await client.invoke(
        DeleteHistory(
            peer=del_his,
            max_id=0,
            revoke=True,
        )
    )


plugins_helper["social"] = {
    f"{random_prefixies(px)}socmed [url]/[reply link]": "To get tiktok/instagram. ( Tiktok No Watermark)",
}
