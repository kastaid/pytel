# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep, Lock
from datetime import datetime, timedelta
from random import randrange
from threading import RLock
from pyrogram.enums import (
    UserStatus,
    ChatType,
    ChatMemberStatus,)
from . import (
    FloodWait,
    UserNotMutualContact,
    UserPrivacyRestricted,
    UsersTooMuch,
    BotsTooMuch,
    _INVITED_LOCKED,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    eor,
    tz,
    _try_purged,
    get_chat_ids,)

_WORKER = []

_LIMITED_FLOOD_TEXT = """
<b>Your account is <u>Limited</u></b>
Wait until it's time:
<code>{}</code>
"""

_ADDING_TEXT = """
<b><u>INVITING USERS</b></u>
├ <b>Status:</b> 🔄 <i>Running</i>
└ <b>Adding:</b> ➕ <code>{}</code> users.

<b>Failed:</b> <code>{}</code> users.
"""


@pytel.instruction(
    ["invite"],
    outgoing=True,
    supergroups=True,
    privileges=["can_invite_users"],
)
async def _invited(client, message):
    msg = await eor(
        message,
        text="<code>Checking ...</code>",
    )
    get_usr = message.text.split(
        " ", 1
    )[1]
    if not get_usr:
        await msg.edit(
            "Please provide id/username."
        )
        return
    x = await eor(
        msg,
        text="<b>Adding users...</b>",
    )
    user_list = get_usr.split(" ")
    try:
        await client.add_chat_members(
            message.chat.id,
            user_list,
            forward_limit=25,
        )
    except UserNotMutualContact:
        return await x.edit(
            "<b>Unable to add user!\nReason:</b> User Not Mutual Contact.",
        )
    except UsersTooMuch:
        return await x.edit(
            "<b>Unable to add user!\nReason:</b> Too many users, the group has reached its limit.",
        )
    except BotsTooMuch:
        return await x.edit(
            "<b>Unable to add bot!\nReason:</b> There are too many bots in the group..",
        )
    except FloodWait as flood:
        wait_for = (
            datetime.now(tz)
            + timedelta(
                seconds=flood.value
            )
        ).strftime("%A, %H:%M:%S")
        return await x.edit(
            _LIMITED_FLOOD_TEXT.format(
                wait_for,
            )
        )
    except BaseException as excp:
        await x.edit(
            f"<b>Unable to add user/bot!\nTraceback:</b> <code>{excp}</code>",
        )
        return
    await x.edit(
        f"<b>User added successfully.</b>\nCount: {len(user_list)}"
    )


@pytel.instruction(
    ["dinviteall"],
    supersu=["PYTEL"],
    supergroups=True,
    privileges=["can_invite_users"],
)
@pytel.instruction(
    ["inviteall"],
    outgoing=True,
    supergroups=True,
    privileges=["can_invite_users"],
)
async def _invited_all(client, message):
    if client:
        user_lock = client.me.id
    if user_lock in _INVITED_LOCKED:
        await eor(
            message,
            text="Please wait until previous **--invite users--** finished...",
        )
        return

    _RLOCKED = RLock()
    with _RLOCKED:
        gets = (
            message.command[1]
            if len(message.command) > 1
            else message.chat.id
        )
        grp = get_chat_ids(str(gets))
        if not grp:
            await eor(
                message,
                text="Please provide id/username/link messages of groups.",
            )
            return

        msg = await eor(
            message,
            text="<code>Checking ...</code>",
        )
        try:
            chat = (
                await client.get_chat(
                    grp
                )
            )
        except Exception as excp:
            client.send_log.exception(
                excp
            )
            await eor(
                msg,
                text=f"Exception: {excp}",
            )
            return

        _CH = [ChatType.CHANNEL]
        _GP = [
            ChatType.SUPERGROUP,
            ChatType.GROUP,
        ]
        if chat.type in _CH:
            await eor(
                msg,
                text="Can't fetching user from channels.",
            )
            return

        elif chat.type in _GP:
            _ASYNC_INV = Lock()
            chat_id = message.chat.id
            async with _ASYNC_INV:
                success, failed = 0, 0
                _WORKER.append(chat_id)
                _INVITED_LOCKED.add(
                    user_lock
                )
                await _try_purged(msg)
                xy = await client.send_message(
                    message.chat.id,
                    "Adding User...",
                )
                async for member in client.get_chat_members(
                    chat.id
                ):
                    _STATUS = [
                        UserStatus.ONLINE,
                        UserStatus.OFFLINE,
                        UserStatus.RECENTLY,
                        UserStatus.LAST_WEEK,
                    ]
                    _ADM = [
                        ChatMemberStatus.ADMINISTRATOR,
                        ChatMemberStatus.OWNER,
                    ]
                    if (
                        member.user.status
                        in _STATUS
                        and (
                            member.status
                            not in _ADM
                        )
                        and (
                            not member.user.is_bot
                        )
                        and (
                            not member.user.is_scam
                        )
                        and (
                            not member.user.is_fake
                        )
                        and (
                            not member.user.is_restricted
                        )
                    ):
                        try:
                            if (
                                chat_id
                                not in _WORKER
                                and (
                                    user_lock
                                    not in _INVITED_LOCKED
                                )
                            ):
                                break

                            await xy.edit(
                                _ADDING_TEXT.format(
                                    success,
                                    failed,
                                )
                            )

                            await client.add_chat_members(
                                message.chat.id,
                                member.user.id,
                            )
                            success = (
                                success
                                + 1
                            )
                            await sleep(
                                randrange(
                                    20,
                                    30,
                                )
                            )
                        except (
                            UsersTooMuch
                        ):
                            await xy.reply(
                                "<b>Unable to add user!\nReason:</b> Too many users, the group has reached its limit.",
                            )
                            _INVITED_LOCKED.discard(
                                user_lock
                            )
                            _WORKER.remove(
                                chat_id
                            )
                            return
                        except (
                            FloodWait
                        ) as flood:
                            wait_for = (
                                datetime.now(
                                    tz
                                )
                                + timedelta(
                                    seconds=flood.value
                                )
                            ).strftime(
                                "%A, %H:%M:%S"
                            )
                            await xy.reply(
                                _LIMITED_FLOOD_TEXT.format(
                                    wait_for,
                                )
                            )
                            _INVITED_LOCKED.discard(
                                user_lock
                            )
                            _WORKER.remove(
                                chat_id
                            )
                            return
                        except UserNotMutualContact:
                            failed = (
                                failed
                                + 1
                            )
                        except UserPrivacyRestricted:
                            failed = (
                                failed
                                + 1
                            )
                        except BaseException:
                            failed = (
                                failed
                                + 1
                            )

            _WORKER.remove(chat_id)
            _INVITED_LOCKED.discard(
                user_lock
            )


plugins_helper["invtools"] = {
    f"{random_prefixies(px)}invite [id/username: list/not (limit 25)]": "To invite user/bot.",
    f"{random_prefixies(px)}inviteall [id/username/link messages group]": "To invite user to target.",
}
