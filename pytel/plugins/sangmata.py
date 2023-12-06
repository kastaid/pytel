# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from html import escape
from pyrogram.raw.functions.messages import (
    DeleteHistory,)
from . import (
    ParseMode,
    eor,
    plugins_helper,
    px,
    extract_user,
    pytel,
    _try_purged,
    replied,
    random_prefixies,)


@pytel.instruction(
    ["dsang", "dsg"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    [
        "sang",
        "sg",
    ],
    outgoing=True,
)
async def _sangmata(
    client, message
):
    user_id = await extract_user(
        client, message
    )
    if not user_id:
        await eor(
            message,
            text="Unable to find user.",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    sang = (
        "@sangmata_bot"
    )
    await client.unblock_user(
        sang
    )
    await client.send_message(
        sang, user_id
    )
    await sleep(3)
    info = await client.resolve_peer(
        sang
    )
    texts = []
    async for s in client.get_chat_history(
        sang
    ):
        if (
            not s.outgoing
        ):
            res = s.text
            if res.lower().startswith(
                "no data"
            ):
                await x.edit(
                    "Got no records."
                )
                await client.read_chat_history(
                    s.chat.id
                )
                return await client.invoke(
                    DeleteHistory(
                        peer=info,
                        max_id=0,
                        revoke=True,
                    )
                )
            if (
                "your quota"
                in res.lower()
            ):
                await x.edit(
                    "Your quota is limited. Try again Tomorrow!"
                )
                await client.read_chat_history(
                    s.chat.id
                )
                return await client.invoke(
                    DeleteHistory(
                        peer=info,
                        max_id=0,
                        revoke=True,
                    )
                )
            texts.append(
                escape(
                    res
                )
            )
            if (
                "history"
                in res.lower()
            ):
                await client.read_chat_history(
                    s.chat.id
                )
                break
    if not texts:
        await x.edit(
            "Cannot get any records.`"
        )
        return
    for txt in texts:
        await client.send_message(
            message.chat.id,
            f"<pre>{txt}</pre>",
            reply_to_message_id=replied(
                message
            ),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        await sleep(1)

    await _try_purged(
        x, 1.5
    )

    return await client.invoke(
        DeleteHistory(
            peer=info,
            max_id=0,
            revoke=True,
        )
    )


plugins_helper[
    "sangmata"
] = {
    f"{random_prefixies(px)}sg / sang [id/username/reply]": "To check the previous username. ( If there are )",
}
