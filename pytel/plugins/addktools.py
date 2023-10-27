# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep, Lock
from contextlib import suppress
from datetime import datetime, timedelta
from random import randrange
from threading import RLock
from pyrogram.enums import (
    UserStatus,
    ChatType,
    ChatMemberStatus,)
from pyrogram.errors import (
    UserAdminInvalid,)
from . import (
    FloodWait,
    UserNotMutualContact,
    UserPrivacyRestricted,
    UsersTooMuch,
    BotsTooMuch,
    _INVITED_LOCKED,
    _KICKED_LOCKED,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    eor,
    tz,
    _try_purged,
    get_chat_ids,)

_WORKER_INVITED = []
_WORKER_KICKED = []

_LIMITED_FLOOD_TEXT = """
<b>Your account is <u>Limited</u></b>

<b><u>Wait</u></b> until it's time:
└ ⏰ <code>{}</code>
"""

_KICKING_TEXT = """
<b><u>KICKING USERS</b></u>
├ <b>Status:</b> {}
└ <b>Kicked:</b> ➖ <code>{}</code> users.

<b>Failed:</b> <code>{}</code> users.
"""

_ADDING_TEXT = """
<b><u>INVITING USERS</b></u>
├ <b>Status:</b> {}
└ <b>Adding:</b> ➕ <code>{}</code> users.

<b>Failed:</b> <code>{}</code> users.
"""


@pytel.instruction(
    ["add"],
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
    ["daddall"],
    supersu=["PYTEL"],
    supergroups=True,
    privileges=["can_invite_users"],
)
@pytel.instruction(
    ["addall"],
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
        except KeyError as excp:
            await eor(
                msg,
                text=f"Exception: {excp}",
            )
            return
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
                (
                    success,
                    failed,
                    run_status,
                ) = (0, 0, False)
                _WORKER_INVITED.append(
                    chat_id
                )
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
                        and (
                            not member.user.is_deleted
                        )
                    ):
                        try:
                            if (
                                chat_id
                                not in _WORKER_INVITED
                                and (
                                    user_lock
                                    not in _INVITED_LOCKED
                                )
                            ):
                                break

                            running = "🔄 <i>Running</i>"
                            await xy.edit(
                                _ADDING_TEXT.format(
                                    running,
                                    success,
                                    failed,
                                )
                            )
                            await sleep(
                                1
                            )

                            await client.add_chat_members(
                                message.chat.id,
                                member.user.id,
                            )
                            run_status = (
                                False
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
                            finished = "✅ <i>Finished</i>"
                            await xy.edit(
                                _ADDING_TEXT.format(
                                    finished,
                                    success,
                                    failed,
                                )
                            )
                            await xy.reply(
                                "<b>Unable to add user!\nReason:</b> Too many users, the group has reached its limit.",
                            )
                            run_status = (
                                True
                            )
                            _WORKER_INVITED.remove(
                                chat_id
                            )
                            _INVITED_LOCKED.discard(
                                user_lock
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
                            finished = "✅ <i>Finished</i>"
                            await xy.edit(
                                _ADDING_TEXT.format(
                                    finished,
                                    success,
                                    failed,
                                )
                            )
                            await xy.reply(
                                _LIMITED_FLOOD_TEXT.format(
                                    wait_for,
                                )
                            )
                            run_status = (
                                True
                            )
                            _WORKER_INVITED.remove(
                                chat_id
                            )
                            _INVITED_LOCKED.discard(
                                user_lock
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
                        else:
                            success = (
                                success
                                + 1
                            )

                if (
                    chat_id
                    in _WORKER_INVITED
                ):
                    run_status = True
                    _WORKER_INVITED.remove(
                        chat_id
                    )
                    _INVITED_LOCKED.discard(
                        user_lock
                    )
                    if run_status:
                        finished = "✅ <i>Finished</i>"
                        await xy.edit(
                            _ADDING_TEXT.format(
                                finished,
                                success,
                                failed,
                            )
                        )
                        return


@pytel.instruction(
    ["dkickall", "sdkickall"],
    supersu=["PYTEL"],
    supergroups=True,
    privileges=["can_restricted"],
)
@pytel.instruction(
    ["kickall", "skickall"],
    outgoing=True,
    supergroups=True,
    privileges=["can_restricted"],
)
async def _kicked_all(client, message):
    if client:
        user_lock = client.me.id
    if user_lock in _KICKED_LOCKED:
        await eor(
            message,
            text="Please wait until previous **--kicked users--** finished...",
        )
        return

    await eor(
        message, text="Checking..."
    )
    _RLOCKED = RLock()
    with _RLOCKED:
        chat_id = message.chat.id
        _ASYNC_KICKED = Lock()
        async with _ASYNC_KICKED:
            (
                success,
                failed,
                run_status,
            ) = (0, 0, False)
            _WORKER_KICKED.append(
                chat_id
            )
            _KICKED_LOCKED.add(
                user_lock
            )
            await _try_purged(message)
            yy = await client.send_message(
                message.chat.id,
                "Kicked all users...",
            )
            async for member in client.get_chat_members(
                chat_id,
            ):
                user = member.user.id
                try:
                    ms = await message.chat.ban_member(
                        user,
                    )
                    success = (
                        success + 1
                    )
                    if (
                        message.command[
                            0
                        ][0]
                        == "s"
                    ):
                        with suppress(
                            Exception
                        ):
                            await _try_purged(
                                yy
                            )
                        await client.delete_messages(
                            chat_id,
                            ms.id,
                            revoke=True,
                        )
                    else:
                        running = "🔄 <i>Running</i>"
                        await yy.edit(
                            _KICKING_TEXT.format(
                                running,
                                success,
                                failed,
                            )
                        )
                    run_status = False
                    await sleep(
                        randrange(
                            10, 15
                        )
                    )
                except (
                    FloodWait
                ) as flood:
                    wait_for = (
                        datetime.now(tz)
                        + timedelta(
                            seconds=flood.value
                        )
                    ).strftime(
                        "%A, %H:%M:%S"
                    )
                    finished = "✅ <i>Finished</i>"
                    await yy.edit(
                        _KICKING_TEXT.format(
                            finished,
                            success,
                            failed,
                        )
                    )
                    await yy.reply(
                        _LIMITED_FLOOD_TEXT.format(
                            wait_for,
                        )
                    )
                    run_status = True
                    _WORKER_KICKED.remove(
                        chat_id
                    )
                    _KICKED_LOCKED.discard(
                        user_lock
                    )
                    return
                except UserAdminInvalid:
                    failed = failed + 1
                except Exception:
                    failed = failed + 1

            if (
                chat_id
                in _WORKER_KICKED
            ):
                run_status = True
                _WORKER_KICKED.remove(
                    chat_id
                )
                _KICKED_LOCKED.discard(
                    user_lock
                )
                if run_status and (
                    message.command[0][
                        0
                    ]
                    != "s"
                ):
                    finished = "✅ <i>Finished</i>"
                    await yy.edit(
                        _KICKING_TEXT.format(
                            finished,
                            success,
                            failed,
                        )
                    )
                    return


plugins_helper["addktools"] = {
    f"{random_prefixies(px)}add [id/username: list/not (limit 25 username/id)]": "To adding user/bot.",
    f"{random_prefixies(px)}addall [target: id/username/link messages]": "To adding user from target.",
    f"{random_prefixies(px)}[s]kickall (s: silent)": "To kicked all users in channel/groups.",
}
