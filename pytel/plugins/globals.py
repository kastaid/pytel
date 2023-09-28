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
from ..client.dbase.dbGBlacklist import (
    check_blacklisted,
    add_blacklisted,
    rem_blacklisted,
    rem_all_blacklisted,
    list_blacklisted,)
from . import (
    _GBAN_LOCKED,
    _UNGBAN_LOCKED,
    _GCAST_LOCKED,
    _GUCAST_LOCKED,
    GCAST_BLACKLIST,
    GUCAST_BLACKLIST,
    OWNER_ID,
    ChatType,
    ChannelPrivate,
    UserNotParticipant,
    FloodWait,
    ParseMode,
    eor,
    _supersu,
    suppress,
    get_text,
    time_formatter,
    plugins_helper,
    px,
    pytel,
    get_blacklisted,
    random_prefixies,
    user_and_reason,
    get_chat_ids,
    _try_purged,)

_GB_TEXT = """
<u><b>{}</u> !!</b>
├ <b>Users:</b> </b> <a href=tg://user?id={}>{}</a>
└ <b>Reason:</b> {}

<u>STATUS</u> ( ✅ <i>Success</i> )
├ <b>Groups:</b> {}
├ <b>Supergroups:</b> {}
└ <b>Channel:</b> {}

<u>STATUS</u> ( 🚫 <i>Failed</i> )
├ <b>Groups:</b> {}
├ <b>Supergroups:</b> {}
└ <b>Channel:</b> {}

<u>TOTAL</u>
├ <b>Success:</b> {}
└ <b>Failed:</b> {}

(c) @kastaid #pytel
"""


@pytel.instruction(
    ["addbl"],
    outgoing=True,
)
async def _added_blacklisted(
    client, message
):
    get_chat_group = (
        message.command[1]
        if len(message.command) > 1
        else message.chat.id
    )
    gc = get_chat_ids(
        str(get_chat_group)
    )
    if not gc:
        await eor(
            message,
            text="Please provide id/username/link messages of group.",
        )
        return

    x = await eor(
        message,
        text="Checking...",
    )
    try:
        chat = await client.get_chat(gc)
    except Exception as excp:
        client.send_log.exception(excp)
        await eor(
            x, text=f"Exception: {excp}"
        )
        return

    user_id = client.me.id
    chat_name = str(chat.title)
    chat_id = int(chat.id)

    check = check_blacklisted(
        user_id, chat_id
    )
    if check:
        await eor(
            x,
            text="This chats already in blacklisted.",
        )
        return

    add_blacklisted(user_id, chat_id)
    text = f"""
<b><u>ADDED BLACKLISTED</u></b>
├ <b>Group Name:</b> {chat_name}
└ <b>Group ID:</b> <code>{chat_id}</code>
"""
    await eor(
        x,
        text=text,
    )


@pytel.instruction(
    ["rembl"],
    outgoing=True,
)
async def _rem_blacklisted(
    client, message
):
    get_chat_group = (
        message.command[1]
        if len(message.command) > 1
        else message.chat.id
    )
    gc = get_chat_ids(
        str(get_chat_group)
    )
    if not gc:
        await eor(
            message,
            text="Please provide id/username/link messages of group.",
        )
        return

    x = await eor(
        message,
        text="Checking...",
    )
    try:
        chat = await client.get_chat(gc)
    except Exception as excp:
        client.send_log.exception(excp)
        await eor(
            x, text=f"Exception: {excp}"
        )
        return

    user_id = client.me.id
    chat_name = str(chat.title)
    chat_id = int(chat.id)

    check = check_blacklisted(
        user_id, chat_id
    )
    if not check:
        await eor(
            x,
            text="This chats not already in blacklisted.",
        )
        return

    rem_blacklisted(user_id, chat_id)
    text = f"""
<b><u>REMOVE BLACKLISTED</u></b>
├ <b>Group Name:</b> {chat_name}
└ <b>Group ID:</b> <code>{chat_id}</code>
"""
    await eor(
        x,
        text=text,
    )


@pytel.instruction(
    ["remallbl"],
    outgoing=True,
)
async def _rem_all_blacklisted(
    client, message
):
    if client:
        user_id = client.me.id
        rem_all_blacklisted(user_id)
        text = f"""
<b><u>REMOVING ALL BLACKLISTED CHATS</u></b>
└ <b>Status:</b> <i>Success</i>
"""
        await eor(
            message,
            text=text,
        )


@pytel.instruction(
    ["listbl"],
    outgoing=True,
)
async def _lists_blacklisted(
    client, message
):
    x = await eor(
        message,
        text="Checking...",
    )
    user = client.me.id
    groups = await list_blacklisted(
        user
    )
    if not groups:
        await eor(
            x,
            text="You don't have a blacklisted.",
        )
        return
    text = f"<u><b>BLACKLISTED CHAT</u></b> ( {len(groups)} )"
    for c in groups:
        try:
            chat = (
                await client.get_chat(
                    int(c)
                )
            )
            text += f"\n├ <code>{chat.id}</code> - {chat.title}"
            await sleep(1.3)
        except FloodWait as flood:
            await sleep(flood.value + 3)
        except KeyError:  # removing
            rem_blacklisted(
                user, chat.id
            )
        except BaseException:
            pass

    if text:
        await eor(
            x,
            text=text,
        )


@pytel.instruction(
    ["devgcast", "dgcast", "cgcast"],
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
        dbl = await list_blacklisted(
            user_lock
        )
        lsted = []
        if dbl:
            lsted += [
                int(_) for _ in dbl
            ]
        else:
            pass
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
        _GCAST_LOCKED.add(user_lock)
        gpc = client.get_dialogs()
        aa = await eor(
            message,
            text="💬 Start a live broadcast message to groups..",
        )
        async for gg in gpc:
            if gg.chat.type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
            ]:
                chat_id = gg.chat.id
                if (
                    chat_id
                    not in gblack
                    and (
                        chat_id
                        not in list(
                            lsted
                        )
                    )
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
            + "</code> groups.\n\n(c) kastaid #pytel"
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
            *_supersu,
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
        _GUCAST_LOCKED.add(user_lock)
        gpc = client.get_dialogs()
        aa = await eor(
            message,
            text="💬 Start a live broadcast message to users..",
        )
        async for gg in gpc:
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
            + "</code> users.\n\n(c) kastaid #pytel"
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
    ["devgban", "dgban"],
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
    if (user in list(_supersu)) or (
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
            with suppress(
                ChannelPrivate,
                UserNotParticipant,
            ):
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
                    chat_id = (
                        dialog.chat.id
                    )
                    try:
                        await client.ban_chat_member(
                            chat_id,
                            user,
                        )
                        gp_success = (
                            gp_success
                            + 1
                        )
                        await sleep(0.5)
                    except (
                        FloodWait
                    ) as flood:
                        await sleep(
                            flood.value
                        )
                        await client.ban_chat_member(
                            chat_id,
                            user,
                        )
                        gp_success = (
                            gp_success
                            + 1
                        )
                        await sleep(0.5)
                    except (
                        BaseException
                    ):
                        gp_failed = (
                            gp_failed
                            + 1
                        )

        elif dialog.chat.type in [
            ChatType.SUPERGROUP
        ]:
            with suppress(
                ChannelPrivate,
                UserNotParticipant,
            ):
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
                    chat_id = (
                        dialog.chat.id
                    )
                    try:
                        await client.ban_chat_member(
                            chat_id,
                            user,
                        )
                        sg_success = (
                            sg_success
                            + 1
                        )
                        await sleep(0.5)
                    except (
                        FloodWait
                    ) as flood:
                        await sleep(
                            flood.value
                        )
                        await client.ban_chat_member(
                            chat_id,
                            user,
                        )
                        sg_success = (
                            sg_success
                            + 1
                        )
                        await sleep(0.5)
                    except (
                        BaseException
                    ):
                        sg_failed = (
                            sg_failed
                            + 1
                        )

        elif dialog.chat.type in [
            ChatType.CHANNEL
        ]:
            with suppress(
                ChannelPrivate,
                UserNotParticipant,
            ):
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
                    chat_id = (
                        dialog.chat.id
                    )
                    try:
                        await client.ban_chat_member(
                            chat_id,
                            user,
                        )
                        ch_success = (
                            ch_success
                            + 1
                        )
                        await sleep(0.5)
                    except (
                        FloodWait
                    ) as flood:
                        await sleep(
                            flood.value
                        )
                        await client.ban_chat_member(
                            chat_id,
                            user,
                        )
                        ch_success = (
                            ch_success
                            + 1
                        )
                        await sleep(0.5)
                    except (
                        BaseException
                    ):
                        ch_failed = (
                            ch_failed
                            + 1
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
        await client.send_message(
            int(message.chat.id),
            text=_GB_TEXT.format(
                "Globally Banned",
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
    ["devungban", "dungban"],
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
    if (user in list(_supersu)) or (
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
        await client.send_message(
            int(message.chat.id),
            text=_GB_TEXT.format(
                "Un-Globally Banned",
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
    f"{random_prefixies(px)}addbl [id/username/link message or not]": "To added blacklisted ( gcast chats ).",
    f"{random_prefixies(px)}rembl [id/username/link message or not]": "To remove blacklisted ( gcast chats ).",
    f"{random_prefixies(px)}remallbl": "To removing all blacklisted ( gcast chats ).",
    f"{random_prefixies(px)}listbl": "To get blacklisted ( gcast chats ).",
    f"{random_prefixies(px)}gcast [text/reply message]": "To broadcast a message globally to all groups u've.",
    f"{random_prefixies(px)}gucast [text/reply message]": "To broadcast a message globally to all users.",
    f"{random_prefixies(px)}gban [username/id/reply user] [reason]": "To globally banned user.",
    f"{random_prefixies(px)}ungban [username/id/reply user] [reason]": "To un-globally banned user.",
}
