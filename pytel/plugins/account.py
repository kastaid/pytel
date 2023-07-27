# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pyrogram.raw import functions
from . import (
    eor,
    plugins_helper,
    px,
    get_text,
    pytel,
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


plugins_helper["account"] = {
    f"{random_prefixies(px)}setmode [offline/online/off/on]": "To setting ur status to be Online or Offline.",
    f"{random_prefixies(px)}setbio [text/reply]": "To updates ur bio. ( Max 70 characters )",
    f"{random_prefixies(px)}setname [first name] [last name]": "To updates ur name.",
}
