# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from pyrogram import (
    enums,)
from pyrogram.raw.functions.messages import (
    DeleteHistory,)
from . import (
    eor,
    plugins_helper,
    px,
    pytel,
    random_prefixies,)


@pytel.instruction(
    ["purpmbot"],
    outgoing=True,
)
async def _clear_all_pm_bot(
    client, message
):
    success, failed = (
        0,
        0,
    )
    x = await eor(
        message,
        text="Processing...\nClear all private messages for category **--BOT--**",
    )
    async for dialog in client.get_dialogs():
        if (
            dialog.chat.type
            == enums.ChatType.BOT
        ):
            chat_id = (
                dialog.chat.id
            )
            history = await client.resolve_peer(
                chat_id
            )
            try:
                await client.invoke(
                    DeleteHistory(
                        peer=history,
                        max_id=0,
                        revoke=True,
                    )
                )
                success = (
                    success
                    + 1
                )
                await sleep(
                    2
                )
            except BaseException as excp:
                client.send_log.exception(
                    excp
                )
                failed = (
                    failed
                    + 1
                )

    if success >= 0:
        text = f"""
<b><u>Purged Private Messages</b></u>
├ <b>Type:</b> <i><u>BOT</i></u>
├ <b>Success:</b> {success} chats.
└ <b>Failed:</b> {failed} chats.
"""
        await eor(
            x, text=text
        )
        return
    else:
        await eor(
            x,
            text="history is clean",
        )
        return


@pytel.instruction(
    ["purpmuser"],
    outgoing=True,
)
async def _clear_all_pm_user(
    client, message
):
    success, failed = (
        0,
        0,
    )
    x = await eor(
        message,
        text="Processing...\nClear all private messages for category **--USER--**",
    )
    async for dialog in client.get_dialogs():
        if (
            dialog.chat.type
            == enums.ChatType.PRIVATE
        ):
            chat_id = (
                dialog.chat.id
            )
            history = await client.resolve_peer(
                chat_id
            )
            try:
                await client.invoke(
                    DeleteHistory(
                        peer=history,
                        max_id=0,
                        revoke=True,
                    )
                )
                success = (
                    success
                    + 1
                )
                await sleep(
                    2
                )
            except BaseException as excp:
                client.send_log.exception(
                    excp
                )
                failed = (
                    failed
                    + 1
                )

    if success >= 0:
        text = f"""
<b><u>Purged Private Messages</b></u>
├ <b>Type:</b> <i><u>USER</i></u>
├ <b>Success:</b> {success} chats.
└ <b>Failed:</b> {failed} chats.
"""
        await eor(
            x, text=text
        )
        return
    else:
        await eor(
            x,
            text="history is clean",
        )
        return


plugins_helper[
    "purgepm"
] = {
    f"{random_prefixies(px)}purpmbot": "To purged private messages for category bot.",
    f"{random_prefixies(px)}purpmuser": "To purged private messages for category user.",
}
