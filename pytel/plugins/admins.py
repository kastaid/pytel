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
    Chat,)
from . import (
    FloodWait,
    OWNER_ID,
    _try_purged,
    eor,
    user_and_reason,
    plugins_helper,
    px,
    pytel,
    developer,
    random_prefixies,
    short_dict,
    LOCK_TYPES,
    suppress,)

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


async def current_chat_permissions(
    client, chat_id
):
    perms = []
    perm = (
        await client.get_chat(chat_id)
    ).permissions
    if perm.can_send_messages:
        perms.append(
            "can_send_messages"
        )
    if perm.can_send_media_messages:
        perms.append(
            "can_send_media_messages"
        )
    if perm.can_send_other_messages:
        perms.append(
            "can_send_other_messages"
        )
    if perm.can_add_web_page_previews:
        perms.append(
            "can_add_web_page_previews"
        )
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")
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
        if perm not in permissions:
            return
        permissions.remove(perm)
    else:
        if perm in permissions:
            return
        permissions.append(perm)
    permissions = {
        perm: True
        for perm in list(
            set(permissions)
        )
    }
    try:
        await client.set_chat_permissions(
            message.chat.id,
            ChatPermissions(
                **permissions
            ),
        )
    except Exception as excp:
        client.send_log.exception(excp)
    await message.edit_text(
        (
            f"🔒 **Locked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            if lock
            else f"🔓 **Unlocked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
        )
    )


async def list_admins(
    client, chat_id: int
) -> list:
    admin = []
    async for u in client.get_chat_members(
        chat_id,
        filter=ChatMembersFilter.ADMINISTRATORS,
    ):
        if u.user.id:
            admin.append(u.user.id)
            return list(admin)


@pytel.instruction(
    ["lock", "unlock"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
)
async def _locked_group(
    client, message
):
    if len(message.command) != 2:
        return
    chat_id = message.chat.id
    parameter = (
        message.text.strip()
        .split(None, 1)[1]
        .lower()
    )
    state = message.command[0].lower()
    if (
        parameter not in data
        and parameter != "all"
    ):
        return
    permissions = (
        await current_chat_permissions(
            client, chat_id
        )
    )
    if parameter in data:
        await tgroups_lock(
            client,
            message,
            parameter,
            permissions,
            data[parameter],
            state == "lock",
        )
    elif (
        parameter == "all"
        and state == "lock"
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
        parameter == "all"
        and state == "unlock"
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
        except Exception as excp:
            client.send_log.exception(
                excp
            )
        await message.edit(
            f"🔓 **Unlocked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
        )

    elif (
        parameter == "all"
        and state == "unlock"
    ):
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
async def _locktypes(client, message):
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
    await eor(message, text=text)


@pytel.instruction(
    ["kick", "kicked", "dkick"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=["can_restricted"],
)
async def _kicked(client, message):
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
    if user == client.me.id:
        await eor(
            x,
            text="I can't restricting myself.",
        )
        return
    if user == int(OWNER_ID):
        await eor(
            x,
            text="I can't restricting my owner.",
        )
        return
    if user in (
        await list_admins(
            client, message.chat.id
        )
    ):
        await eor(
            x,
            "I can't kick an admin, You know the rules ?",
        )
        return
    if user in list(developer):
        await eor(
            x,
            text="I can't restricting, coz he's My Developer..",
        )
        return

    try:
        mention = (
            await client.get_users(user)
        ).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anonymous"
        )

    msg = (
        f"**Kicked User:** {mention}\n"
    )
    if message.command[0] == "dkick":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Reason:** {reason}"
    with suppress(Exception):
        await message.chat.ban_member(
            user
        )
        await message.chat.unban_member(
            user
        )
    await eor(x, text=msg)


@pytel.instruction(
    ["ban", "banned", "dban"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=["can_restricted"],
)
async def _banned(client, message):
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
    if user == client.me.id:
        await eor(
            x,
            text="I can't restricting myself.",
        )
        return
    if user == int(OWNER_ID):
        await eor(
            x,
            text="I can't restricting my owner.",
        )
        return
    if user in (
        await list_admins(
            client, message.chat.id
        )
    ):
        await eor(
            x,
            "I can't ban an admin, You know the rules ?",
        )
        return
    if user in list(developer):
        await eor(
            x,
            text="I can't restricting, coz he's My Developer..",
        )
        return

    try:
        mention = (
            await client.get_users(user)
        ).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anonymous"
        )

    msg = (
        f"**Banned User:** {mention}\n"
    )
    if message.command[0] == "dban":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Reason:** {reason}"
    with suppress(Exception):
        await message.chat.ban_member(
            user
        )
    await eor(x, text=msg)


@pytel.instruction(
    ["unban", "unbanned"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=["can_restricted"],
)
async def _unbanned(client, message):
    reply = message.reply_to_message

    if (
        reply
        and reply.sender_chat
        and reply.sender_chat
        != message.chat.id
    ):
        await eor(
            message,
            text="You cannot unban a channel",
        )
        return

    if len(message.command) == 2:
        user = message.text.split(
            None, 1
        )[1]
    elif (
        len(message.command) == 1
        and reply
    ):
        user = (
            message.reply_to_message.from_user.id
        )
    else:
        await eor(
            message,
            text="Provide a username or reply to a user's message to unban.",
        )
        return
    with suppress(Exception):
        await message.chat.unban_member(
            user
        )
    umention = (
        await client.get_users(user)
    ).mention
    await eor(
        message,
        text=f"Unbanned! {umention}",
    )


@pytel.instruction(
    ["pin", "pin-s"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=["can_pinned"],
)
async def _pinned(client, message):
    if not message.reply_to_message:
        await eor(
            message,
            text="reply to message.",
        )
        return

    mid = message.reply_to_message.id
    if message.command[0] == "pin-s":
        is_silent = True
    if message.command[0] == "pin":
        is_silent = False

    with suppress(Exception):
        x = await client.pin_chat_message(
            chat_id=message.chat.id,
            message_id=mid,
            disable_notification=is_silent,
        )
        if is_silent:
            await client.delete_messages(
                message.chat.id, x.id
            )

    await _try_purged(message, 1)
    return


@pytel.instruction(
    ["unpin", "unpinall"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=["can_pinned"],
)
async def _unpinned(client, message):
    chat = message.chat.id
    if message.command[0] == "unpinall":
        await client.unpin_all_chat_messages(
            chat
        )
        await _try_purged(message, 1)
        return
    if message.command[0] == "unpin":
        if not message.reply_to_message:
            gc = await client.get_chat(
                chat
            )
            if not isinstance(gc, Chat):
                raise ValueError(
                    "Invalid Chat"
                )
            if not gc.pinned_message:
                return await eor(
                    message,
                    "no-pinned-message",
                )
            pinned = (
                gc.pinned_message.id
            )
            await client.unpin_chat_message(
                gc.id, pinned
            )
        else:
            mid = (
                message.reply_to_message.id
            )
            await client.unpin_chat_message(
                chat_id=message.chat.id,
                message_id=mid,
            )
        await _try_purged(message, 1)
        return


@pytel.instruction(
    ["zombies"],
    outgoing=True,
    admin_only=True,
    supergroups=True,
    privileges=["can_restricted"],
)
async def _zombies(client, message):
    zombie, chat = 0, message.chat
    x = await eor(
        message,
        text="finding zombie...",
    )
    async for member in client.get_chat_members(chat.id):  # type: ignore
        if member.user.is_deleted:
            zombie = zombie + 1
            try:
                await client.ban_chat_member(
                    chat.id,
                    member.user.id,
                )
                await sleep(0.7)
            except UserAdminInvalid:
                zombie = zombie - 1
            except FloodWait as flood:
                await sleep(flood.value)  # type: ignore

    if zombie == 0:
        return await eor(
            x, text="zombie-clean"
        )

    return await eor(
        x,
        text=f"cleaning-zombie {zombie} account.",
    )


plugins_helper["admins"] = {
    f"{random_prefixies(px)}lock [types]": "To locked permissions the group depending on the type.",
    f"{random_prefixies(px)}lock all": "To locked everything.",
    f"{random_prefixies(px)}unlock [types]": "To unlocked permissions the group depending on the type.",
    f"{random_prefixies(px)}unlock all": "To unlocked everything.",
    f"{random_prefixies(px)}locktypes": "To get the group key list type.",
    f"{random_prefixies(px)}kick / dkick [username/id/reply message user]": "To kicked user on chats. dkick: d: for delete message from user.",
    f"{random_prefixies(px)}ban / dban [username/id/reply message user]": "To banned user on chats. dban: d: for delete message from user.",
    f"{random_prefixies(px)}unban [username/id/reply message user]": "To unban user on chats.",
    f"{random_prefixies(px)}pin / pin-s [reply message]": "To pinned message on chats/channel. pin-s : -s: for silent notification.",
    f"{random_prefixies(px)}unpin[all] / [reply message]": "To unpinned message on chats/channel.",
    f"{random_prefixies(px)}zombies": "To Kick all deleted account in group/channel.",
}
