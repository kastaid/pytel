# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in

from asyncio import sleep
from typing import Set
from . import (
    ParseMode,
    FloodWait,
    _try_purged,
    eor,
    get_text,
    plugins_helper,
    px,
    pytel,
    suppress,
    random_prefixies,)

_MENTION_LOCK: Set[int] = set()
mention_chats = []


@pytel.instruction(
    ["mentionall", "tagall"],
    outgoing=True,
    supergroups=True,
)
async def _mention_all(client, message):
    if client:
        user_id = client.me.id
    if user_id in _MENTION_LOCK:
        await eor(
            message,
            text="Please wait until previous **--mention--** finished...",
        )
        return

    chat_id = message.chat.id
    tx = get_text(message)
    if not tx:
        await eor(
            message,
            text="provide a **--text--** or message **--reply--** to the contents of a message when **--tagging--** a member.",
        )

    await _try_purged(message, 0.6)
    mention_chats.append(chat_id)
    _MENTION_LOCK.add(user_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(
        chat_id
    ):
        if (
            chat_id not in mention_chats
        ) and (
            user_id not in _MENTION_LOCK
        ):
            break
        elif (usr.user.is_bot) or (
            usr.user.is_deleted
        ):
            pass
        usrnum = usrnum + 1
        usrtxt += f"👤 <a href=tg://user?id={usr.user.id}>{await client.user_fullname(usr.user.id)}</a>\n"
        if usrnum == 5:
            try:
                txt = f"<b>{tx}</b>\n\n{usrtxt}\n"
                await client.send_message(
                    chat_id,
                    txt,
                    parse_mode=ParseMode.HTML,
                )
                await sleep(20)
                usrnum = 0
                usrtxt = ""
            except FloodWait as flood:
                await sleep(
                    flood.value + 3
                )
                with suppress(
                    Exception
                ):
                    await client.send_message(
                        chat_id,
                        txt,
                        parse_mode=ParseMode.HTML,
                    )
                    await sleep(20)
                    usrnum = 0
                    usrtxt = ""
    with suppress(Exception):
        _MENTION_LOCK.discard(user_id)
        mention_chats.remove(chat_id)


@pytel.instruction(
    ["cmention", "ctag"],
    outgoing=True,
    supergroups=True,
)
async def _cancel_mention(
    client, message
):
    if client:
        user_id = client.me.id
        chat_id = message.chat.id
    if (
        user_id not in _MENTION_LOCK
    ) and (
        chat_id not in mention_chats
    ):
        await eor(
            message,
            text="You do not currently mention members of this group.",
        )
        return
    x = await eor(
        message,
        text="Canceling mention members...",
    )
    mention_chats.remove(chat_id)
    _MENTION_LOCK.discard(user_id)
    await eor(
        x,
        text="Successfully stopped mentioning member.",
    )


plugins_helper["mention"] = {
    f"{random_prefixies(px)}mentionall / tagall [text/reply message]": "To mention members in the group. ( 20 seconds 1x send messages )",
    f"{random_prefixies(px)}cmention / ctag": "To cancel the current mention.",
}
