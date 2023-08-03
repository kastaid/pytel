# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from random import randrange
from time import time
from pyrogram.enums import (
    ChatMemberStatus,)
from . import (
    _GBAN_LOCKED,
    _UNGBAN_LOCKED,
    _GCAST_LOCKED,
    _GUCAST_LOCKED,
    GCAST_BLACKLIST,
    GUCAST_BLACKLIST,
    OWNER_ID,
    ChatType,
    FloodWait,
    ParseMode,
    eor,
    developer,
    get_text,
    time_formatter,
    plugins_helper,
    px,
    pytel,
    get_blacklisted,
    random_prefixies,
    user_and_reason,
    _try_purged,)


@pytel.instruction(
    ["devgcast"],
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
        if message.reply_to_message:
            send = (
                message.reply_to_message
            )
        elif len(message.command) < 2:
            await eor(
                message,
                text="Give some text to Gcast or reply message.",
            )
            return
        else:
            send = get_text(message)
        aa = await eor(
            message,
            text="💬 Start a live broadcast message to groups..",
        )
        _GCAST_LOCKED.add(user_lock)
        async for gg in client.get_dialogs():
            if gg.chat.type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
            ]:
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
            "<u><b>Global Group Broadcast Successful</b></u>\n"
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


@pytel.instruction(
    ["devgucast"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["gucast"],
    outgoing=True,
)
async def _global_user_broadcast(
    client, message
):
    if client:
        user_lock = client.me.id
    if user_lock in _GUCAST_LOCKED:
        await eor(
            message,
            text="Please wait until previous **--gucast--** finished...",
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
        GU_BLACKLIST = await get_blacklisted(
            url="https://raw.githubusercontent.com/kastaid/resources/main/gucastblacklist.py",
            attempts=6,
            fallbacks=GUCAST_BLACKLIST,
        )
        gblack = {
            *GU_BLACKLIST,
            *developer,
        }
        if message.reply_to_message:
            send = (
                message.reply_to_message
            )
        elif len(message.command) < 2:
            await eor(
                message,
                text="Give some text to Gucast or reply message.",
            )
            return
        else:
            send = get_text(message)
        aa = await eor(
            message,
            text="💬 Start a live broadcast message to users..",
        )
        _GUCAST_LOCKED.add(user_lock)
        async for gg in client.get_dialogs():
            if gg.chat.type in [
                ChatType.PRIVATE,
            ]:
                usr_id = gg.chat.id
                if usr_id not in gblack:
                    try:
                        if (
                            message.reply_to_message
                        ):
                            await send.copy(
                                usr_id
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
                                    usr_id
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
        text_gubcast = (
            "<u><b>Global User Broadcast Successful</b></u>\n"
            + " ├ <b>Time taken:</b> <code>"
            + taken
            + "</code>\n"
            + " ├ <b>Sent:</b> <code>"
            + s1
            + "</code> users.\n"
            + " └ <b>Failed:</b> <code>"
            + s2
            + "</code> users.\n\n(c) @kastaid #pytel"
        )
        await client.send_message(
            int(message.chat.id),
            text=text_gubcast,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            disable_web_page_preview=True,
        )
        _GUCAST_LOCKED.discard(
            user_lock
        )
        return await _try_purged(
            aa, 1.5
        )


@pytel.instruction(
    ["devgban"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["gban", "gbanned"],
    outgoing=True,
)
async def _global_banned(
    client, message
):
    if client:
        user_lock = client.me.id
    if user_lock in _GBAN_LOCKED:
        await eor(
            message,
            text="Please wait until previous **--GBanned--** finished...",
        )
        return

    (
        user,
        reason,
    ) = await user_and_reason(
        client,
        message,
        sender_chat=True,
    )
    if not user:
        await eor(
            message,
            text="I can't find that user.",
        )
        return
    if (user in list(developer)) or (
        user == int(OWNER_ID)
    ):
        return
    x = await eor(
        message,
        text="</b>Restricting users . . .</b>",
    )
    _GBAN_LOCKED.add(user_lock)
    (
        total_success,
        total_failed,
        gp_success,
        gp_failed,
        sg_success,
        sg_failed,
        ch_success,
        ch_failed,
    ) = (0, 0, 0, 0, 0, 0, 0, 0)
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.GROUP
        ]:
            me = await client.get_chat_member(
                dialog.chat.id,
                (
                    await client.get_me()
                ).id,
            )
            if me.status in (
                ChatMemberStatus.OWNER,
                ChatMemberStatus.ADMINISTRATOR,
            ):
                chat_id = dialog.chat.id
                try:
                    await client.ban_chat_member(
                        chat_id, user
                    )
                    gp_success = (
                        gp_success + 1
                    )
                    await sleep(0.5)
                except (
                    FloodWait
                ) as flood:
                    await sleep(
                        flood.value
                    )
                    await client.ban_chat_member(
                        chat_id, user
                    )
                    gp_success = (
                        gp_success + 1
                    )
                    await sleep(0.5)
                except Exception:
                    gp_failed = (
                        gp_failed + 1
                    )

        elif dialog.chat.type in [
            ChatType.SUPERGROUP
        ]:
            me = await client.get_chat_member(
                dialog.chat.id,
                (
                    await client.get_me()
                ).id,
            )
            if me.status in (
                ChatMemberStatus.OWNER,
                ChatMemberStatus.ADMINISTRATOR,
            ):
                chat_id = dialog.chat.id
                try:
                    await client.ban_chat_member(
                        chat_id, user
                    )
                    sg_success = (
                        sg_success + 1
                    )
                    await sleep(0.5)
                except (
                    FloodWait
                ) as flood:
                    await sleep(
                        flood.value
                    )
                    await client.ban_chat_member(
                        chat_id, user
                    )
                    sg_success = (
                        sg_success + 1
                    )
                    await sleep(0.5)
                except Exception:
                    sg_failed = (
                        sg_failed + 1
                    )

        elif dialog.chat.type in [
            ChatType.CHANNEL
        ]:
            chat_id = dialog.chat.id
            try:
                await client.ban_chat_member(
                    chat_id, user
                )
                ch_success = (
                    ch_success + 1
                )
                await sleep(0.5)
            except FloodWait as flood:
                await sleep(flood.value)
                await client.ban_chat_member(
                    chat_id, user
                )
                ch_success = (
                    ch_success + 1
                )
                await sleep(0.5)
            except Exception:
                ch_failed = (
                    ch_failed + 1
                )

    fullname = (
        await client.user_fullname(user)
    )
    reason = reason if reason else "-"
    total_success = (
        total_success
        + ch_success
        + sg_success
        + gp_success
    )
    total_failed = (
        total_failed
        + ch_failed
        + sg_failed
        + gp_failed
    )
    if total_success >= 0:
        text = """
<u><b>Globally Banned</u> !!</b>
├ <b>Users:</b> </b> <a href=tg://user?id={}>{}</a>
└ <b>Reason:</b> {}

<u>STATUS</u> ( <i>Success</i> )
├ <b>Groups:</b> {}
├ <b>Supergroups:</b> {}
└ <b>Channel:</b> {}

<u>STATUS</u> ( <i>Failed</i> )
├ <b>Groups:</b> {}
├ <b>Supergroups:</b> {}
└ <b>Channel:</b> {}

<u>TOTAL</u>
├ <b>Success:</b> {}
└ <b>Failed:</b> {}

(c) @kastaid #pytel
"""
        await client.send_message(
            int(message.chat.id),
            text=text.format(
                user,
                fullname,
                reason,
                gp_success,
                sg_success,
                ch_success,
                gp_failed,
                sg_failed,
                ch_failed,
                total_success,
                total_failed,
            ),
            parse_mode=ParseMode.HTML,
            disable_notification=True,
        )
        _GBAN_LOCKED.discard(user_lock)
        return await _try_purged(x, 1.5)


@pytel.instruction(
    ["devungban"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["ungban", "ungbanned"],
    outgoing=True,
)
async def _unglobal_banned(
    client, message
):
    if client:
        user_lock = client.me.id
    if user_lock in _UNGBAN_LOCKED:
        await eor(
            message,
            text="Please wait until previous **--UnGBanned--** finished...",
        )
        return

    (
        user,
        reason,
    ) = await user_and_reason(
        client,
        message,
        sender_chat=True,
    )
    if not user:
        await eor(
            message,
            text="I can't find that user.",
        )
        return
    if (user in list(developer)) or (
        user == int(OWNER_ID)
    ):
        return
    x = await eor(
        message,
        text="</b>Un-Restricting users . . .</b>",
    )
    _UNGBAN_LOCKED.add(user_lock)
    (
        total_success,
        total_failed,
        gp_success,
        gp_failed,
        sg_success,
        sg_failed,
        ch_success,
        ch_failed,
    ) = (0, 0, 0, 0, 0, 0, 0, 0)
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.GROUP
        ]:
            me = await client.get_chat_member(
                dialog.chat.id,
                (
                    await client.get_me()
                ).id,
            )
            if me.status in (
                ChatMemberStatus.OWNER,
                ChatMemberStatus.ADMINISTRATOR,
            ):
                chat_id = dialog.chat.id
                try:
                    await client.unban_chat_member(
                        chat_id, user
                    )
                    gp_success = (
                        gp_success + 1
                    )
                    await sleep(0.5)
                except (
                    FloodWait
                ) as flood:
                    await sleep(
                        flood.value
                    )
                    await client.unban_chat_member(
                        chat_id, user
                    )
                    gp_success = (
                        gp_success + 1
                    )
                    await sleep(0.5)
                except Exception:
                    gp_failed = (
                        gp_failed + 1
                    )

        elif dialog.chat.type in [
            ChatType.SUPERGROUP
        ]:
            me = await client.get_chat_member(
                dialog.chat.id,
                (
                    await client.get_me()
                ).id,
            )
            if me.status in (
                ChatMemberStatus.OWNER,
                ChatMemberStatus.ADMINISTRATOR,
            ):
                chat_id = dialog.chat.id
                try:
                    await client.unban_chat_member(
                        chat_id, user
                    )
                    sg_success = (
                        sg_success + 1
                    )
                    await sleep(0.5)
                except (
                    FloodWait
                ) as flood:
                    await sleep(
                        flood.value
                    )
                    await client.unban_chat_member(
                        chat_id, user
                    )
                    sg_success = (
                        sg_success + 1
                    )
                    await sleep(0.5)
                except Exception:
                    sg_failed = (
                        sg_failed + 1
                    )

        elif dialog.chat.type in [
            ChatType.CHANNEL
        ]:
            chat_id = dialog.chat.id
            try:
                await client.unban_chat_member(
                    chat_id, user
                )
                ch_success = (
                    ch_success + 1
                )
                await sleep(0.5)
            except FloodWait as flood:
                await sleep(flood.value)
                await client.unban_chat_member(
                    chat_id, user
                )
                ch_success = (
                    ch_success + 1
                )
                await sleep(0.5)
            except Exception:
                ch_failed = (
                    ch_failed + 1
                )

    fullname = (
        await client.user_fullname(user)
    )
    reason = reason if reason else "-"
    total_success = (
        total_success
        + ch_success
        + sg_success
        + gp_success
    )
    total_failed = (
        total_failed
        + ch_failed
        + sg_failed
        + gp_failed
    )
    if total_success >= 0:
        text = """
<u><b>Un-Globally Banned</u> !!</b>
├ <b>Users:</b> </b> <a href=tg://user?id={}>{}</a>
└ <b>Reason:</b> {}

<u>STATUS</u> ( <i>Success</i> )
├ <b>Groups:</b> {}
├ <b>Supergroups:</b> {}
└ <b>Channel:</b> {}

<u>STATUS</u> ( <i>Failed</i> )
├ <b>Groups:</b> {}
├ <b>Supergroups:</b> {}
└ <b>Channel:</b> {}

<u>TOTAL</u>
├ <b>Success:</b> {}
└ <b>Failed:</b> {}

(c) @kastaid #pytel
"""
        await client.send_message(
            int(message.chat.id),
            text=text.format(
                user,
                fullname,
                reason,
                gp_success,
                sg_success,
                ch_success,
                gp_failed,
                sg_failed,
                ch_failed,
                total_success,
                total_failed,
            ),
            parse_mode=ParseMode.HTML,
            disable_notification=True,
        )
        _UNGBAN_LOCKED.discard(
            user_lock
        )
        return await _try_purged(x, 1.5)


plugins_helper["globals"] = {
    f"{random_prefixies(px)}gcast [text/reply message]": "To broadcast a message globally to all groups u've.",
    f"{random_prefixies(px)}gucast [text/reply message]": "To broadcast a message globally to all users.",
    f"{random_prefixies(px)}gban [username/id/reply user] [reason]": "To globally banned user.",
    f"{random_prefixies(px)}ungban [username/id/reply user] [reason]": "To un-globally banned user.",
}
