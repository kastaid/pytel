# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import gather
from os import remove
from pyrogram.enums import ChatType
from . import (
    ParseMode,
    plugins_helper,
    px,
    pytel,
    humanboolean,
    random_prefixies,
    eor,
    attr_file,
    mentioned,
    _try_purged,
    get_spamwatch_banned,
    get_cas_banned,
    extract_user,)


@pytel.instruction(
    ["id"],
    outgoing=True,
)
async def _ids(client, message):
    chat_type = message.chat.type

    if chat_type == ChatType.PRIVATE:
        user_id = message.chat.id
        get_u = await mentioned(
            client,
            user_id,
            use_html=True,
        )
        try:
            dc_id = (
                "N/A"
                if not get_u.dc_id
                else get_u.dc_id
            )
        except BaseException:
            dc_id = "N/A"

        try:
            check_u = (
                "BOT"
                if get_u.is_bot
                else "USER"
            )
        except BaseException:
            check_u = "PRIVATE"

        text = """
<b><u>{}</b></u>
 ├ <b>Profile</b>: {}
 ├ <b>ID</b>: <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
            check_u,
            get_u,
            user_id,
            dc_id,
        )
        await eor(
            message,
            text=text,
        )
        return

    elif chat_type == ChatType.CHANNEL:
        try:
            dc_id = (
                message.sender_chat.dc_id
                if message.sender_chat.dc_id
                else "N/A"
            )
        except BaseException:
            dc_id = "N/A"

        channel_id = (
            message.sender_chat.id
        )
        text = """
<b><u>CHANNEL</b></u>
 ├ <b>Profile</b>: {}
 ├ <b>ID</b>: <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
            await mentioned(
                client,
                message.sender_chat.id,
                use_html=True,
            ),
            channel_id,
            dc_id,
        )
        await eor(
            message,
            text=text,
        )
        return

    elif chat_type in [
        ChatType.GROUP,
        ChatType.SUPERGROUP,
    ]:
        try:
            dc_id = (
                message.chat.dc_id
                if message.chat.dc_id
                else "N/A"
            )
        except BaseException:
            dc_id = "N/A"

        text = ""
        text += """
<b><u>GROUP</u></b>
 ├ <b>Profile</b>: {}
 ├ <b>ID</b>: <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
            await mentioned(
                client,
                message.chat.id,
                use_html=True,
            ),
            message.chat.id,
            dc_id,
        )
        if message.reply_to_message:
            try:
                dc_id = (
                    message.reply_to_message.from_user.dc_id
                    if message.reply_to_message.from_user.dc_id
                    else "N/A"
                )
            except BaseException:
                dc_id = "N/A"

            check_u = (
                "BOT"
                if message.reply_to_message.from_user.is_bot
                else "USER"
            )
            text += """
<b><u>{}</u></b>
 ├ <b>Reply From</b>: {}
 ├ <b>ID:</b> <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
                check_u,
                await mentioned(
                    client,
                    message.reply_to_message.from_user.id,
                    use_html=True,
                ),
                message.reply_to_message.from_user.id,
                dc_id,
            )
            if get_file := attr_file(
                message.reply_to_message
            ):
                text += """
<b><u>FILE</u></b>
 ├ <b>TypeFile</b>: {}
 └ <b>File ID</b>: <code>{}</code>
""".format(
                    get_file.message_type,
                    get_file.file_id,
                )
        else:
            try:
                dc_id = (
                    message.from_user.dc_id
                    if message.from_user.id
                    else "N/A"
                )
            except BaseException:
                dc_id = "N/A"

            check_u = (
                "BOT"
                if message.from_user.is_bot
                else "USER"
            )
            text += """
<b><u>{}</u></b>
 ├ <b>From</b>: {}
 ├ <b>ID</b>: <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
                check_u,
                await mentioned(
                    client,
                    message.from_user.id,
                    use_html=True,
                ),
                message.from_user.id,
                dc_id,
            )
            if get_file := attr_file(
                message
            ):
                text += """
<b><u>FILE</u></b>
 ├ <b>TypeFile</b>: {}
 └ <b>File ID</b>: <code>{}</code>
""".format(
                    get_file.message_type,
                    get_file.file_id,
                )
        await eor(
            message,
            text=text,
        )


@pytel.instruction(
    ["ubinfo"],
    outgoing=True,
    supergroups=True,
)
async def _user_info(client, message):
    user_id = await extract_user(
        client, message
    )
    if not user_id:
        await eor(
            message,
            text="Please reply to user or gimme id/username.",
        )
        return
    x = await eor(
        message,
        text="</b>Processing . . .</b>",
    )
    try:
        user = await client.get_users(
            user_id
        )
        username = (
            f"@{user.username}"
            if user.username
            else "-"
        )
        first_name = (
            f"{user.first_name}"
            if user.first_name
            else "-"
        )
        last_name = (
            f"{user.last_name}"
            if user.last_name
            else "-"
        )
        fullname = (
            f"{user.first_name} {user.last_name}"
            if user.last_name
            else user.first_name
        )
        user_details = (
            await client.get_chat(
                user.id
            )
        ).bio
        bio = (
            f"{user_details}"
            if user_details
            else "-"
        )
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace(
                "UserStatus.", ""
            )
            status = y.capitalize()
        else:
            status = "-"
        dc_id = (
            f"{user.dc_id}"
            if user.dc_id
            else "-"
        )
        common = await client.get_common_chats(
            user.id
        )
        is_spamwatch_banned = (
            await get_spamwatch_banned(
                user_id
            )
        )
        is_cas_banned = (
            await get_cas_banned(
                user_id
            )
        )
        if not user.is_bot:
            out_str = f"""<b><u>USER INFORMATION</b></u>
├ <b>User ID:</b> <code>{user.id}</code>
├ <b>First Name:</b> {first_name}
├ <b>Last Name:</b> {last_name}
├ <b>Username:</b> {username}
├ <b>DC ID:</b> <code>{dc_id}</code>
├ <b>Is Contact:</b> <code>{humanboolean(user.is_contact)}</code>
├ <b>Is Fake:</b> <code>{humanboolean(user.is_fake)}</code>
├ <b>Is Scam:</b> <code>{humanboolean(user.is_scam)}</code>
├ <b>Is Partner of Telegram:</b> <code>{humanboolean(user.is_support)}</code>
├ <b>Is Spamwatch Banned:</b> <code>{humanboolean(is_spamwatch_banned)}</code>
├ <b>Is CAS Banned:</b> <code>{humanboolean(is_cas_banned)}</code>
├ <b>Is Restricted:</b> <code>{humanboolean(user.is_restricted)}</code>
├ <b>Is Verified:</b> <code>{humanboolean(user.is_verified)}</code>
├ <b>Is Premium:</b> <code>{humanboolean(user.is_premium)}</code>
└ <b>Bio:</b> {bio}

├ <b>Same Groups Seen:</b> <code>{len(common)}</code>
├ <b>Last Seen:</b> <code>{status}</code>
└ <b>Permanent Link:</b> <a href=tg://user?id={user.id}>{fullname}</a>
"""
        else:
            out_str = f"""<b><u>BOT INFORMATION</b></u>
├ <b>Bot ID:</b> <code>{user.id}</code>
├ <b>First Name:</b> {first_name}
├ <b>Last Name:</b> {last_name}
├ <b>Username:</b> {username}
├ <b>DC ID:</b> <code>{dc_id}</code>
├ <b>Is Bot:</b> <code>{humanboolean(user.is_bot)}</code>
├ <b>Is Fake:</b> <code>{humanboolean(user.is_fake)}</code>
├ <b>Is Scam:</b> <code>{humanboolean(user.is_scam)}</code>
├ <b>Is Partner of Telegram:</b> <code>{humanboolean(user.is_support)}</code>
├ <b>Is Spamwatch Banned:</b> <code>{humanboolean(is_spamwatch_banned)}</code>
├ <b>Is CAS Banned:</b> <code>{humanboolean(is_cas_banned)}</code>
├ <b>Is Restricted:</b> <code>{humanboolean(user.is_restricted)}</code>
├ <b>Is Verified:</b> <code>{humanboolean(user.is_verified)}</code>
└ <b>Bio:</b> {bio}

├ <b>Same Groups Seen:</b> <code>{len(common)}</code>
└ <b>Permanent Link:</b> <a href=tg://user?id={user.id}>{fullname}</a>
"""

        photo_id = (
            user.photo.big_file_id
            if user.photo
            else None
        )
        if photo_id:
            photo = await client.download_media(
                photo_id
            )
            await gather(
                _try_purged(x),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await eor(
                x,
                text=out_str,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
    except Exception as e:
        return await eor(
            x, text=f"INFO: {e}"
        )


@pytel.instruction(
    ["cginfo"],
    outgoing=True,
    supergroups=True,
)
async def _chat_info(client, message):
    x = await eor(
        message,
        text="</b>Processing . . .</b>",
    )
    try:
        if (
            len(message.text.split())
            > 1
        ):
            chat_u = (
                message.text.split()[1]
            )
            chat = (
                await client.get_chat(
                    chat_u
                )
            )
        else:
            chatid = message.chat.id
            chat = (
                await client.get_chat(
                    chatid
                )
            )
        username = (
            f"@{chat.username}"
            if chat.username
            else "-"
        )
        description = (
            f"{chat.description}"
            if chat.description
            else "-"
        )
        dc_id = (
            f"{chat.dc_id}"
            if chat.dc_id
            else "-"
        )
        sticker_name = (
            f"{chat.sticker_set_name}"
            if chat.sticker_set_name
            else "-"
        )
        distance = (
            f"{chat.distance}"
            if chat.distance
            else "-"
        )
        h = f"{chat.type}"
        if h.startswith(
            "ChatType.GROUP"
        ) or h.startswith(
            "ChatType.SUPERGROUP"
        ):
            out_str = f"""<b><u>GROUP INFORMATION</u></b>
├ <b>Chat ID:</b> <code>{chat.id}</code>
├ <b>Title:</b> {chat.title}
├ <b>Username:</b> {username}
├ <b>DC ID:</b> <code>{dc_id}</code>
├ <b>Is Scam:</b> <code>{humanboolean(chat.is_scam)}</code>
├ <b>Is Fake:</b> <code>{humanboolean(chat.is_fake)}</code>
├ <b>Is Verified:</b> <code>{humanboolean(chat.is_verified)}</code>
├ <b>Is Restricted:</b> <code>{humanboolean(chat.is_restricted)}</code>
├ <b>Is Protected:</b> <code>{humanboolean(chat.has_protected_content)}</code>
├ <b>Total Members:</b> <code>{chat.members_count}</code>
├ <b>Sticker Name:</b> {sticker_name}
├ <b>Distance:</b> <code>{distance}</code>
└ <b>Description:</b>
{description}
"""
        if h.startswith(
            "ChatType.CHANNEL"
        ):
            out_str = f"""<b><u>CHANNEL INFORMATION</u></b>
├ <b>Channel ID:</b> <code>{chat.id}</code>
├ <b>Title:</b> {chat.title}
├ <b>Username:</b> {username}
├ <b>DC ID:</b> <code>{dc_id}</code>
├ <b>Is Scam:</b> <code>{humanboolean(chat.is_scam)}</code>
├ <b>Is Fake:</b> <code>{humanboolean(chat.is_fake)}</code>
├ <b>Is Verified:</b> <code>{humanboolean(chat.is_verified)}</code>
├ <b>Is Restricted:</b> <code>{humanboolean(chat.is_restricted)}</code>
├ <b>Is Protected:</b> <code>{humanboolean(chat.has_protected_content)}</code>
├ <b>Total Subscriber:</b> <code>{chat.members_count}</code>
└ <b>Description:</b>
{description}
"""
        photo_id = (
            chat.photo.big_file_id
            if chat.photo
            else None
        )
        if photo_id:
            photo = await client.download_media(
                photo_id
            )
            await gather(
                _try_purged(x),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await eor(
                x,
                text=out_str,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
    except Exception as e:
        return await eor(
            x, text=f"INFO: `{e}`"
        )


plugins_helper["info"] = {
    f"{random_prefixies(px)}id [reply/no need]": "To get data id [user/chanel/group/file] information.",
    f"{random_prefixies(px)}ubinfo [id/username/reply user]": "To get data user/bot in Telegram.",
    f"{random_prefixies(px)}cginfo [id/username/reply channel]": "To get data channel/group in Telegram.",
}
