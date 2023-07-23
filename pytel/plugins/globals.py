# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from random import randrange
from time import time
from . import (
    _GCAST_LOCKED,
    GCAST_BLACKLIST,
    ChatType,
    FloodWait,
    ParseMode,
    eor,
    time_formatter,
    plugins_helper,
    px,
    pytel,
    get_blacklisted,
    random_prefixies,
    _try_purged,)


@pytel.instruction(
    ["sgcast"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["gcast"],
    outgoing=True,
)
async def _global_broadcast(
    client, message
):
    if client:
        user_lock = client.me.id
    if user_lock in _GCAST_LOCKED:
        await eor(
            message,
            text="Please wait until previous **--gcast--** finished...",
        )
        return
    else:
        (
            start_time,
            success,
            failed,
        ) = (
            time(),
            0,
            0,
        )
        BLACKLIST = await get_blacklisted(
            url="https://raw.githubusercontent.com/kastaid/resources/main/gcastblacklist.py",
            attempts=6,
            fallbacks=GCAST_BLACKLIST,
        )
        gblack = {
            *BLACKLIST,
        }
        _GCAST_LOCKED.add(user_lock)
        async for gg in client.get_dialogs():
            if gg.chat.type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
            ]:
                if (
                    message.reply_to_message
                ):
                    send = (
                        message.reply_to_message
                    )
                elif (
                    len(message.command)
                    < 2
                ):
                    await eor(
                        message,
                        text="Give some text to Gcast or reply message.",
                    )
                    return
                else:
                    send = message.text.split(
                        None,
                        1,
                    )[
                        1
                    ]
                aa = await eor(
                    message,
                    text="💬 Start a live broadcast message..",
                )
                chat_id = gg.chat.id
                if (
                    chat_id
                    not in gblack
                ):
                    try:
                        if (
                            message.reply_to_message
                        ):
                            await send.copy(
                                chat_id
                            )
                            await sleep(
                                randrange(
                                    6,
                                    9,
                                )
                            )
                            success = (
                                success
                                + 1
                            )
                        else:
                            await client.send_message(
                                int(
                                    chat_id
                                ),
                                text=send,
                                disable_notification=True,
                                disable_web_page_preview=True,
                            )
                            await sleep(
                                randrange(
                                    6,
                                    9,
                                )
                            )
                            success = (
                                success
                                + 1
                            )
                    except (
                        FloodWait
                    ) as excp:
                        await sleep(
                            excp.value
                            + 5
                        )
                    except Exception:
                        failed = (
                            failed + 1
                        )

        taken = time_formatter(
            (time() - start_time) * 1000
        )
        s1 = f"{success}"
        s2 = f"{failed}"
        text_gbcast = (
            "<u><b>Global Broadcast Successful</b></u>\n"
            + " ├ <b>Time taken:</b> <code>"
            + taken
            + "</code>\n"
            + " ├ <b>Sent:</b> <code>"
            + s1
            + "</code> groups.\n"
            + " └ <b>Failed:</b> <code>"
            + s2
            + "</code> groups.\n\n(c) @kastaid #pytel"
        )
        await client.send_message(
            int(message.chat.id),
            text=text_gbcast,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
        )
        _GCAST_LOCKED.discard(user_lock)
        return await _try_purged(
            aa, 1.5
        )


plugins_helper["globals"] = {
    f"{random_prefixies(px)}gcast [text/reply message]": "To broadcast a message globally to all groups u've.",
}
