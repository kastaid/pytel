# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pyrogram import enums
from pyrogram.raw import functions
from . import (
    eor,
    plugins_helper,
    px,
    get_text,
    pytel,
    suppress,
    random_prefixies,)


@pytel.instruction(
    ["setmode"],
    outgoing=True,
)
async def _online_offfline(
    client, message
):
    if client.me.id:
        mode = message.text.split(
            None, 1
        )
        if mode[1] in ["online", "on"]:
            # Status Online
            await client.invoke(
                query=functions.account.UpdateStatus(
                    offline=False
                ),
            )
            status = "Online"
            await eor(
                message,
                text=f"✅ Success, ur status is <u>{status}</u>",
            )
            return
        if mode[1] in [
            "offline",
            "off",
        ]:
            # Status Offline
            await client.invoke(
                query=functions.account.UpdateStatus(
                    offline=True
                ),
            )
            status = "Offline"
            await eor(
                message,
                text=f"✅ Success, ur status is <u>{status}</u>",
            )
            return


@pytel.instruction(
    ["setname", "setbio"],
    outgoing=True,
)
async def _set_name_bio(
    client, message
):
    args = get_text(message)
    if message.command[0] == "setbio":
        await client.update_profile(
            bio=args
        )
        text = f"✅ Success\nYour bio set to be: <code>{args}</code>"
        await eor(
            message,
            text=text,
        )
        return
    if message.command[0] == "setname":
        try:
            name = args.split(None, 1)
            first_name = name[0]
            last_name = name[1]
        except Exception:
            example = f"<b><u>Example:</b></u>\n<code>{random_prefixies(px)}setname first_name last_name</code>"
            await eor(
                message, text=example
            )
            return

        await client.update_profile(
            first_name=first_name,
            last_name=last_name,
        )
        text = f"""
✅ Success
<u>Your has been update</u>.
├ <b>First Name:</b> <code>{first_name}</code>
└ <b>Last Name:</b> <code>{last_name}</code>
"""
        await eor(
            message,
            text=text,
        )
        return


@pytel.instruction(
    ["mydialogs"],
    outgoing=True,
)
async def _my_dialogs(client, message):
    x = await eor(
        message, text="Please wait..."
    )
    u, g, sg, c, b, admin_chat = (
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adm = await client.get_me()
    async for dialog in client.get_dialogs():
        if (
            dialog.chat.type
            == enums.ChatType.PRIVATE
        ):
            u = u + 1
        elif (
            dialog.chat.type
            == enums.ChatType.BOT
        ):
            b = b + 1
        elif (
            dialog.chat.type
            == enums.ChatType.GROUP
        ):
            g = g + 1
        elif (
            dialog.chat.type
            == enums.ChatType.SUPERGROUP
        ):
            sg = sg + 1
            user_s = await dialog.chat.get_member(
                int(adm.id)
            )
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                admin_chat = (
                    admin_chat + 1
                )
        elif (
            dialog.chat.type
            == enums.ChatType.CHANNEL
        ):
            c = c + 1

    text = """
<b><u>DIALOGS STATISTICS</u></b>
 ├ <b>Private Messages:</b> {} Users and {} Bots.
 ├ <b>Are in:</b> {} Groups.
 ├ <b>Are in:</b> {} Super Groups.
 ├ <b>Are in:</b> {} Channels.
 └ <b>Admin in:</b> {} Chats.
"""
    with suppress(Exception):
        await eor(
            x,
            text=text.format(
                u,
                b,
                g,
                sg,
                c,
                admin_chat,
            ),
        )


plugins_helper["account"] = {
    f"{random_prefixies(px)}mydialogs": "To get my dialogue statistics.",
    f"{random_prefixies(px)}setmode [offline/online/off/on]": "To setting ur status to be Online or Offline.",
    f"{random_prefixies(px)}setbio [text/reply]": "To updates ur bio. ( Max 70 characters )",
    f"{random_prefixies(px)}setname [first name] [last name]": "To updates ur name.",
}
