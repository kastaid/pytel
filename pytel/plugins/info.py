# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pyrogram.enums import ChatType
from . import (
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    eor,
    mention_html,
    attr_file,)


@pytel.instruction(
    ["id"],
    outgoing=True,
)
async def _ids(client, message):
    chat_type = message.chat.type

    if chat_type == ChatType.PRIVATE:
        user_id = message.chat.id
        get_u = await client.get_users(
            user_id
        )
        dc_id = (
            get_u.dc_id
            if get_u.dc_id
            else "N/A"
        )
        check_u = (
            "BOT"
            if get_u.is_bot
            else "USER"
        )
        text = """
<b><u>{}</b></u>
 ├ <b>Profile</b>: {}
 ├ <b>ID</b>: <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
            check_u,
            mention_html(
                user_id,
                name=f"{get_u.first_name}",
            ),
            user_id,
            dc_id,
        )
        await eor(
            message,
            text=text,
        )
        return

    elif chat_type == ChatType.CHANNEL:
        dc_id = (
            message.sender_chat.dc_id
            if message.sender_chat.dc_id
            else "N/A"
        )
        channel_id = (
            message.sender_chat.id
        )
        text = """
<b><u>CHANNEL</b></u>
 ├ <b>Profile</b>: {}
 ├ <b>ID</b>: <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
            mention_html(
                channel_id,
                name=f"{message.sender_chat.first_name}",
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
        dc_id = (
            message.chat.dc_id
            if message.chat.dc_id
            else "N/A"
        )
        text = ""
        text += """
<b><u>GROUP</u></b>
 ├ <b>Profile</b>: {}
 ├ <b>ID</b>: <code>{}</code>
 └ <b>DC ID</b>: <code>{}</code>
""".format(
            mention_html(
                message.chat.id,
                name=f"{message.chat.title}",
            ),
            message.chat.id,
            dc_id,
        )
        if message.reply_to_message:
            dc_id = (
                message.reply_to_message.from_user.dc_id
                if message.reply_to_message.from_user.dc_id
                else "N/A"
            )
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
                mention_html(
                    message.reply_to_message.from_user.id,
                    name=f"{message.reply_to_message.from_user.first_name}",
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
            dc_id = (
                message.from_user.dc_id
                if message.from_user.id
                else "N/A"
            )
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
                mention_html(
                    message.from_user.id,
                    name=f"{message.from_user.first_name}",
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
        msg = (
            message.reply_to_message
            or message
        )
        await eor(
            msg,
            text=text,
        )


plugins_helper["info"] = {
    f"{random_prefixies(px)}id [reply/no need]": "To get id information.",
}
