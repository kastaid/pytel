# pytel < https://t.me/kastaid >
# Copyright (C) 20253-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the mGNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from pyrogram.enums import (
    ChatMembersFilter,)
from pyrogram.errors import (
    UserAdminInvalid,
    ChatNotModified,)
from pyrogram.types import (
    ChatPermissions,
    ChatPrivileges,
    Chat,)
from . import (
    FloodWait,
    OWNER_ID,
    UserRestricted,
    UserNotParticipant,
    _try_purged,
    eor,
    extract_user,
    user_and_reason,
    plugins_helper,
    px,
    pytel,
    _supersu,
    random_prefixies,
    short_dict,
    LOCK_TYPES,
    suppress,)

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

data = {
    "messages": "can_send_messages",
    "media": "can_send_media_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "others": "can_send_other_messages",
    "links": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}

_PROMDEM_TEXT = """
<u><b>{}</u></b>
├ <b>Status:</b> {}
└ <b>Users:</b> {}
"""

_UMT_TEXT = """
<u><b>{}</u></b>
├ <b>Users:</b> {}
└ <b>Reason:</b> {}
"""


async def current_chat_permissions(
    client, chat_id
):
    perms = []
    perm = (
        await client.get_chat(
            chat_id
        )
    ).permissions
    if (
        perm.can_send_messages
    ):
        perms.append(
            "can_send_messages"
        )
    if (
        perm.can_send_media_messages
    ):
        perms.append(
            "can_send_media_messages"
        )
    if (
        perm.can_send_other_messages
    ):
        perms.append(
            "can_send_other_messages"
        )
    if (
        perm.can_add_web_page_previews
    ):
        perms.append(
            "can_add_web_page_previews"
        )
    if (
        perm.can_send_polls
    ):
        perms.append(
            "can_send_polls"
        )
    if (
        perm.can_change_info
    ):
        perms.append(
            "can_change_info"
        )
    if (
        perm.can_invite_users
    ):
        perms.append(
            "can_invite_users"
        )
    if (
        perm.can_pin_messages
    ):
        perms.append(
            "can_pin_messages"
        )
    return perms


async def tgroups_lock(
    client,
    message,
    parameter,
    permissions: list,
    perm: str,
    lock,
):
    if lock:
        if (
            perm
            not in permissions
        ):
            return
        permissions.remove(
            perm
        )
    else:
        if (
            perm
            in permissions
        ):
            return
        permissions.append(
            perm
        )
    permissions = {
        perm: True
        for perm in list(
            set(
                permissions
            )
        )
    }
    try:
        await client.set_chat_permissions(
            message.chat.id,
            ChatPermissions(
                **permissions
            ),
        )
    except (
        ChatNotModified
    ):
        return await message.edit_text(
            (
                f"🔒 **Locked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
                if lock
                else f"🔓 **Unlocked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
        )
    except (
        Exception
    ) as excp:
        client.send_log.exception(
            excp
        )
    await message.edit_text(
        (
            f"🔒 **Locked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            if lock
            else f"🔓 **Unlocked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
        )
    )


async def list_admins(
    client,
    chat_id: int,
    user_id: int,
) -> bool:
    adm = []
    async for m in client.get_chat_members(
        chat_id,
        filter=ChatMembersFilter.ADMINISTRATORS,
    ):
        adm.append(
            m.user.id
        )
    if user_id in adm:
        adm.clear()
        return True
    else:
        adm.clear()
        return False


@pytel.instruction(
    ["lock", "unlock"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
)
async def _locked_group(
    client, message
):
    if (
        len(
            message.command
        )
        != 2
    ):
        return
    chat_id = (
        message.chat.id
    )
    parameter = (
        message.text.strip()
        .split(None, 1)[
            1
        ]
        .lower()
    )
    state = (
        message.command[
            0
        ].lower()
    )
    if (
        parameter
        not in data
        and parameter
        != "all"
    ):
        return
    permissions = await current_chat_permissions(
        client, chat_id
    )
    if parameter in data:
        await tgroups_lock(
            client,
            message,
            parameter,
            permissions,
            data[
                parameter
            ],
            state
            == "lock",
        )
    elif (
        parameter
        == "all"
        and state
        == "lock"
    ):
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(),
            )
            await message.edit_text(
                f"🔒 **Locked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
        except ChatNotModified:
            return await message.edit_text(
                f"🔒 **Success Locked!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
    elif (
        parameter
        == "all"
        and state
        == "unlock"
    ):
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatNotModified:
            return await message.edit_text(
                f"🔓 **Unlocked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
        except (
            Exception
        ) as excp:
            client.send_log.exception(
                excp
            )
        await message.edit(
            f"🔓 **Unlocked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
        )

    elif (
        parameter
        == "all"
        and state
        == "unlock"
    ):
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatNotModified:
            return await message.edit_text(
                f"🔓 <b>Unlocked for `all`</b> <code>{message.chat.title}</code>",
            )
        await eor(
            message,
            f"🔓 <b>Unlocked for `all`</b> <code>{message.chat.title}</code>",
        )


@pytel.instruction(
    ["locktypes"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
)
async def _locktypes(
    client, message
):
    text = (
        "<u><b>Locktypes Available</u></b>\n\n"
        + "\n".join(
            [
                f"• <code>{x}</code> <b>:</b> <i>{y}</i>"
                for x, y in short_dict(
                    LOCK_TYPES
                ).items()
            ]
        )
    )
    text += "\n\n<b>Example:</b>\n"
    text += f"<code>{random_prefixies(px)}lock all</code> : To locked everything."
    await eor(
        message,
        text=text,
    )


@pytel.instruction(
    [
        "promote",
        "fullpromote",
        "fpromote",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_promote_members"
    ],
)
async def _promoted(
    client, message
):
    user_id = await extract_user(
        client, message
    )
    x = await eor(
        message,
        text="Checking...",
    )
    if not user_id:
        await eor(
            x,
            text="Unable to find user.",
        )
        return
    if (
        user_id
        == client.me.id
    ):
        await eor(
            x,
            text="Unable to promoting urself.",
        )
        return
    _info, status = (
        "Promoting Member",
        None,
    )
    chat_id = (
        message.chat.id
    )
    ladm = await list_admins(
        client,
        chat_id=chat_id,
        user_id=user_id,
    )
    mention = (
        await client.get_users(
            user_id
        )
    ).mention
    if ladm:
        await eor(
            x,
            text="User's already an Admins.",
        )
        return
    else:
        yy = await eor(
            x,
            text="Promoting...",
        )
        if (
            message.command[
                0
            ][
                0
            ]
            == "f"
        ):
            status = "Administrator"
            try:
                await client.promote_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    privileges=ChatPrivileges(
                        can_manage_chat=True,
                        can_delete_messages=True,
                        can_manage_video_chats=True,
                        can_restrict_members=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                        can_promote_members=True,
                    ),
                )
                await sleep(
                    1.5
                )
                await eor(
                    yy,
                    text=_PROMDEM_TEXT.format(
                        _info,
                        status,
                        mention,
                    ),
                )
                return
            except UserRestricted:
                text = "You are limited/restricted. You can't promoting this member."
                await eor(
                    yy,
                    text=text,
                )
                return
        else:
            status = (
                "Staff"
            )
            try:
                await client.promote_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    privileges=ChatPrivileges(
                        can_manage_chat=True,
                        can_delete_messages=True,
                        can_manage_video_chats=True,
                        can_restrict_members=True,
                        can_change_info=False,
                        can_invite_users=True,
                        can_pin_messages=True,
                        can_promote_members=False,
                    ),
                )
                await sleep(
                    1
                )
                await eor(
                    yy,
                    text=_PROMDEM_TEXT.format(
                        _info,
                        status,
                        mention,
                    ),
                )
                return
            except UserRestricted:
                text = "You are limited/restricted. You can't promoting this member."
                await eor(
                    yy,
                    text=text,
                )
                return


@pytel.instruction(
    [
        "demote",
        "demoted",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_promote_members"
    ],
)
async def _demoted(
    client, message
):
    user_id = await extract_user(
        client, message
    )
    x = await eor(
        message,
        text="Checking...",
    )
    if not user_id:
        await eor(
            x,
            text="Unable to find user.",
        )
        return
    if (
        user_id
        == client.me.id
    ):
        await eor(
            x,
            text="Unable to demoting urself.",
        )
        return
    yy = await eor(
        x,
        text="Demoting...",
    )
    _info, status = (
        "Demoting Admins",
        None,
    )
    chat_id = (
        message.chat.id
    )
    if message.command:
        pu = await client.get_chat_member(
            message.chat.id,
            user_id,
        )
        pumention = (
            await client.get_users(
                pu.promoted_by.id
            )
        ).mention
        mention = (
            await client.get_users(
                user_id
            )
        ).mention
        if (
            pu.promoted_by.id
            == client.me.id
        ):
            status = (
                "Member"
            )
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ),
            )
            await sleep(
                1.5
            )
            await eor(
                yy,
                text=_PROMDEM_TEXT.format(
                    _info,
                    status,
                    mention,
                ),
            )
            return

        else:
            text = """
You can't demoting {}
because he was promoted by {}.
"""
            await eor(
                yy,
                text=text.format(
                    mention,
                    pumention,
                ),
            )
            return


@pytel.instruction(
    [
        "mute",
        "muted",
        "dmute",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_restricted"
    ],
)
async def _muted(
    client, message
):
    (
        user_id,
        reason,
    ) = await user_and_reason(
        client,
        message,
        sender_chat=False,
    )
    x = await eor(
        message,
        text="Checking...",
    )
    if not user_id:
        await eor(
            x,
            text="Unable to find user.",
        )
        return
    chat_id = (
        message.chat.id
    )
    ladm = await list_admins(
        client,
        chat_id=chat_id,
        user_id=user_id,
    )
    if (
        user_id
        == client.me.id
    ):
        await eor(
            x,
            text="Unable to muting urself.",
        )
        return
    if user_id in list(
        _supersu
    ):
        await eor(
            x,
            text="I can't muting, coz he's My Developer..",
        )
        return
    if ladm:
        await eor(
            x,
            text="I can't mute an admin, You know the rules ?",
        )
        return
    yy = await eor(
        x,
        text="Muting...",
    )
    mention = (
        await client.get_users(
            user_id
        )
    ).mention
    rsn = (
        reason
        if reason
        else "N/A"
    )
    status = (
        "Muting User"
    )
    if (
        message.command[
            0
        ][0]
        == "d"
    ):
        await message.reply_to_message.delete()
    with suppress(
        BaseException,
        UserNotParticipant,
    ):
        await message.chat.restrict_member(
            user_id,
            permissions=ChatPermissions(),
        )
        await eor(
            yy,
            text=_UMT_TEXT.format(
                status,
                mention,
                rsn,
            ),
        )


@pytel.instruction(
    [
        "unmute",
        "unmuted",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_restricted"
    ],
)
async def _unmuted(
    client, message
):
    user_id = await extract_user(
        client, message
    )
    x = await eor(
        message,
        text="Checking...",
    )
    if not user_id:
        await eor(
            x,
            text="Unable to find user.",
        )
        return
    chat_id = (
        message.chat.id
    )
    ladm = await list_admins(
        client,
        chat_id=chat_id,
        user_id=user_id,
    )
    if (
        user_id
        == client.me.id
    ):
        await eor(
            x,
            text="Unable to un-muting urself.",
        )
        return
    if ladm:
        await eor(
            x,
            text="I can't unmute an admin, You know the rules ?",
        )
        return
    text = """
<b><u>Unmuting User</b></u>
└ <b>Users:</b> {}
"""
    yy = await eor(
        x,
        text="Unmuting...",
    )
    with suppress(
        BaseException,
        UserNotParticipant,
    ):
        await message.chat.restrict_member(
            user_id,
            permissions=unmute_permissions,
        )
        mention = (
            await client.get_users(
                user_id
            )
        ).mention
        await eor(
            yy,
            text=text.format(
                mention,
            ),
        )


@pytel.instruction(
    [
        "kick",
        "kicked",
        "dkick",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_restricted"
    ],
)
async def _kicked(
    client, message
):
    x = await eor(
        message,
        text="Restricting users...",
    )
    (
        user,
        reason,
    ) = await user_and_reason(
        client,
        message,
        sender_chat=False,
    )
    if not user:
        await eor(
            x,
            text="I can't find that user.",
        )
        return
    chat_id = (
        message.chat.id
    )
    ladm = await list_admins(
        client,
        chat_id=chat_id,
        user_id=user,
    )
    if (
        user
        == client.me.id
    ):
        await eor(
            x,
            text="I can't restricting myself.",
        )
        return
    if user == int(
        OWNER_ID
    ):
        await eor(
            x,
            text="I can't restricting my owner.",
        )
        return
    if ladm:
        await eor(
            x,
            text="I can't kick an admin, You know the rules ?",
        )
        return
    if user in list(
        _supersu
    ):
        await eor(
            x,
            text="I can't restricting, coz he's My Developer..",
        )
        return

    try:
        mention = (
            await client.get_users(
                user
            )
        ).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anonymous"
        )

    msg = f"<b>Kicked User:</b> {mention}\n"
    if (
        message.command[
            0
        ]
        == "dkick"
    ):
        await message.reply_to_message.delete()
    if reason:
        msg += f"<b>Reason:</b> {reason}"
    with suppress(
        Exception,
        UserNotParticipant,
    ):
        await client.ban_chat_member(
            message.chat.id,
            user,
        )
        await client.unban_chat_member(
            message.chat.id,
            user,
        )
    await eor(
        x, text=msg
    )


@pytel.instruction(
    [
        "ban",
        "banned",
        "dban",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_restricted"
    ],
)
async def _banned(
    client, message
):
    x = await eor(
        message,
        text="Restricting users...",
    )
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
            x,
            text="I can't find that user.",
        )
        return
    chat_id = (
        message.chat.id
    )
    ladm = await list_admins(
        client,
        chat_id=chat_id,
        user_id=user,
    )
    if (
        user
        == client.me.id
    ):
        await eor(
            x,
            text="I can't restricting myself.",
        )
        return
    if user == int(
        OWNER_ID
    ):
        await eor(
            x,
            text="I can't restricting my owner.",
        )
        return
    if ladm:
        await eor(
            x,
            text="I can't ban an admin, You know the rules ?",
        )
        return
    if user in list(
        _supersu
    ):
        await eor(
            x,
            text="I can't restricting, coz he's My Developer..",
        )
        return

    try:
        mention = (
            await client.get_users(
                user
            )
        ).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anonymous"
        )

    msg = f"<b>Banned User:</b> {mention}\n"
    if (
        message.command[
            0
        ][0]
        == "d"
    ):
        await message.reply_to_message.delete()
    if reason:
        msg += f"<b>Reason:</b> {reason}"
    with suppress(
        Exception,
        UserNotParticipant,
    ):
        await client.ban_chat_member(
            message.chat.id,
            user,
        )
    await eor(
        x, text=msg
    )


@pytel.instruction(
    [
        "unban",
        "unbanned",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_restricted"
    ],
)
async def _unbanned(
    client, message
):
    reply = (
        message.reply_to_message
    )
    x = await eor(
        message,
        text="Checking...",
    )
    if (
        reply
        and reply.sender_chat
        and reply.sender_chat
        != message.chat.id
    ):
        await eor(
            x,
            text="You cannot unban a channel",
        )
        return

    if (
        len(
            message.command
        )
        == 2
    ):
        user = message.text.split(
            None, 1
        )[
            1
        ]
    elif (
        len(
            message.command
        )
        == 1
        and reply
    ):
        user = (
            message.reply_to_message.from_user.id
        )
    else:
        await eor(
            x,
            text="Provide a username or reply to a user's message to unban.",
        )
        return
    chat_id = (
        message.chat.id
    )
    ladm = await list_admins(
        client,
        chat_id=chat_id,
        user_id=user,
    )
    if ladm:
        await eor(
            x,
            text="Why should I unban admin ?",
        )
        return
    yy = await eor(
        x,
        text="Unbanning...",
    )
    try:
        mention = (
            await client.get_users(
                user
            )
        ).mention
    except Exception:
        mention = user
    with suppress(
        Exception,
        UserNotParticipant,
    ):
        await client.unban_chat_member(
            message.chat.id,
            user,
        )
    await eor(
        yy,
        text=f"Unbanned! {mention}",
    )


@pytel.instruction(
    ["pin", "pin-s"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_pinned"
    ],
)
async def _pinned(
    client, message
):
    if (
        not message.reply_to_message
    ):
        await eor(
            message,
            text="reply to message.",
        )
        return

    mid = (
        message.reply_to_message.id
    )
    if (
        message.command[
            0
        ]
        == "pin-s"
    ):
        is_silent = True
    if (
        message.command[
            0
        ]
        == "pin"
    ):
        is_silent = False

    with suppress(
        Exception
    ):
        x = await client.pin_chat_message(
            chat_id=message.chat.id,
            message_id=mid,
            disable_notification=is_silent,
        )
        if is_silent:
            await client.delete_messages(
                message.chat.id,
                x.id,
            )

    await _try_purged(
        message, 1
    )
    return


@pytel.instruction(
    [
        "unpin",
        "unpinall",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_pinned"
    ],
)
async def _unpinned(
    client, message
):
    chat = (
        message.chat.id
    )
    if (
        message.command[
            0
        ]
        == "unpinall"
    ):
        await client.unpin_all_chat_messages(
            chat
        )
        await _try_purged(
            message, 1
        )
        return
    if (
        message.command[
            0
        ]
        == "unpin"
    ):
        if (
            not message.reply_to_message
        ):
            gc = await client.get_chat(
                chat
            )
            if not isinstance(
                gc, Chat
            ):
                raise ValueError(
                    "Invalid Chat"
                )
            if (
                not gc.pinned_message
            ):
                return await eor(
                    message,
                    "no-pinned-message",
                )
            pinned = (
                gc.pinned_message.id
            )
            await client.unpin_chat_message(
                gc.id,
                pinned,
            )
        else:
            mid = (
                message.reply_to_message.id
            )
            await client.unpin_chat_message(
                chat_id=message.chat.id,
                message_id=mid,
            )
        await _try_purged(
            message, 1
        )
        return


@pytel.instruction(
    [
        "zombies",
        "zombie",
    ],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=[
        "can_restricted"
    ],
)
async def _zombies(
    client, message
):
    zombie, chat = (
        [],
        message.chat,
    )
    x = await eor(
        message,
        text="finding zombie...",
    )
    ghost = client.get_chat_members(
        chat_id=chat.id,
    )
    async for member in ghost:
        try:
            if (
                member.user.first_name
                is None
            ):
                x = await eor(
                    x,
                    text=f"Removing {len(zombie)} zombie accounts...",
                )
                await client.ban_chat_member(
                    chat.id,
                    member.user.id,
                )
                zombie = (
                    zombie
                    + [
                        member.user.id
                    ]
                )
                await sleep(
                    1
                )

        except UserAdminInvalid:
            zombie = set(
                zombie
            ) - set(
                member.user.id
            )
        except (
            FloodWait
        ) as flood:
            await sleep(flood.value)  # type: ignore
            await client.ban_chat_member(
                chat.id,
                member.user.id,
            )
            zombie = (
                zombie
                + [
                    member.user.id
                ]
            )

    if len(zombie) == 0:
        await eor(
            x,
            text="no zombies, your group is clean.",
        )
        return

    await eor(
        x,
        text=f"has cleaned {len(zombie)} deleted (zombie) accounts.",
    )
    zombie.clear()


plugins_helper[
    "admins"
] = {
    f"{random_prefixies(px)}[f/full]promote [id/username/reply]": "To promoting member to be admins.",
    f"{random_prefixies(px)}demote [username/id/reply]": "To demoting admins to be member.",
    f"{random_prefixies(px)}lock [types]": "To locked permissions the group depending on the type.",
    f"{random_prefixies(px)}lock all": "To locked everything.",
    f"{random_prefixies(px)}unlock [types]": "To unlocked permissions the group depending on the type.",
    f"{random_prefixies(px)}unlock all": "To unlocked everything.",
    f"{random_prefixies(px)}locktypes": "To get the group key list type.",
    f"{random_prefixies(px)}[d]kick [username/id/reply]": "To kicked user on chats. dkick: d: for delete message from user.",
    f"{random_prefixies(px)}[d]ban [username/id/reply]": "To banned user on chats. dban: d: for delete message from user.",
    f"{random_prefixies(px)}unban [username/id/reply]": "To unban user on chats.",
    f"{random_prefixies(px)}pin / pin-s [reply message]": "To pinned message on chats/channel. pin-s : -s: for silent notification.",
    f"{random_prefixies(px)}unpin[all] / [reply message]": "To unpinned message on chats/channel.",
    f"{random_prefixies(px)}[d]mute [username/id/reply]": "To muting user. (d: delete message user)",
    f"{random_prefixies(px)}unmute [username/id/reply]": "To unmuting user",
    f"{random_prefixies(px)}zombies": "To Kick all deleted account in group/channel. ( max: 99 account )",
}
