# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from ..client.dbase.dbLogger import (
    check_logger,
)
from . import (
    ParseMode,
    eor,
    developer,
    functions,
    plugins_helper,
    px,
    pytel,
    pytel_tgb,
    random_prefixies,
    pydb,
)

ANTIPM = pydb.get_key("PMSTATUS")
PMBLOCK = pydb.get_key("PMBLOCK")
PMSPAMREPORT = pydb.get_key("PMSPAMREPORT")


@pytel.instruction(is_antipm=True)
async def _anti_pm_status(client, message):
    _ = client.me.id
    is_blocked, is_reported = None, None
    user_info = await client.resolve_peer(
        message.chat.id
    )
    if user_info.user_id in developer:
        return

    if pydb.get_key("PMSPAMREPORT"):
        await client.send(
            functions.messages.ReportSpam(
                peer=user_info
            )
        )
        is_reported = "Yes"
    if pydb.get_key("PMBLOCK"):
        await client.send(
            functions.contacts.Block(
                id=user_info
            )
        )
        is_blocked = "Yes"
    await client.send(
        functions.messages.DeleteHistory(
            peer=user_info,
            max_id=0,
            revoke=True,
        )
    )

    chat_id = check_logger().get(_)
    text = """
#ANTIPM_LOGGER
<u><b>STATUS</b></u>
 ├ <b>User ID:</b> <code>{}</code>
 ├ <b>is_blocked:</b> <code>{}</code>
 └ <b>is_reported:</b> <code>{}</code>
""".format(
        user_info.user_id,
        is_blocked,
        is_reported,
    )
    await pytel_tgb.send_message(
        int(str(chat_id[0])),
        text,
        parse_mode=ParseMode.HTML,
        disable_notification=False,
    )


@pytel.instruction(
    ["antipm", "anti_pm"], outgoing=True
)
async def _anti_pm(client, message):
    if len(message.command) == 1:
        if ANTIPM == "True":
            text = """
<b>Anti-PM status: enabled
Disable with: </b><code>{}antipm disable</code>
""".format(
                random_prefixies(px),
            )
            await eor(
                message,
                text=text,
            )
            return
        else:
            text = """
<b>Anti-PM status: disabled
Enable with: </b><code>{}antipm enable</code>
""".format(
                random_prefixies(px),
            )
            await eor(
                message,
                text=text,
            )
            return
    elif message.command[1] in [
        "enable",
        "on",
        "1",
        "yes",
        "true",
    ]:
        pydb.set_key("PMSTATUS", True)
        await eor(
            message,
            text="<b>Anti-PM enabled!</b>",
        )
        return
    elif message.command[1] in [
        "disable",
        "off",
        "0",
        "no",
        "false",
    ]:
        pydb.set_key("PMSTATUS", False)
        await eor(
            message,
            text="<b>Anti-PM disabled!</b>",
        )
        return
    else:
        text = """
<b>Usage:</b> <code>{}antipm [enable|disable|on|off]</code>
""".format(
            random_prefixies(px),
        )
        await eor(
            message,
            text=text,
        )
        return


@pytel.instruction(
    "antipm_report", outgoing=True
)
async def _antipm_report(client, message):
    if len(message.command) == 1:
        if PMSPAMREPORT == "True":
            text = """
<b>Spam-reporting enabled.
Disable with: </b><code>{}antipm_report disable</code>
""".format(
                random_prefixies(px),
            )
            await eor(
                message,
                text=text,
            )
            return
        else:
            text = """
<b>Spam-reporting disabled.
Disable with: </b><code>{}antipm_report enable</code>
""".format(
                random_prefixies(px),
            )
            await eor(
                message,
                text=text,
            )
            return
    elif message.command[1] in [
        "enable",
        "on",
        "1",
        "yes",
        "true",
    ]:
        pydb.set_key("PMSPAMREPORT", True)
        await eor(
            message,
            text="<b>Spam-reporting enabled!</b>",
        )
        return
    elif message.command[1] in [
        "disable",
        "off",
        "0",
        "no",
        "false",
    ]:
        pydb.set_key("PMSPAMREPORT", False)
        await eor(
            message,
            text="<b>Spam-reporting disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}antipm_report [enable|disable|on|off]</code>",
        )
        return


@pytel.instruction(
    "antipm_block", outgoing=True
)
async def _antipm_block(client, message):
    if len(message.command) == 1:
        if PMBLOCK == "True":
            text = """
<b>Blocking users enabled.
Disable with: </b><code>{}antipm_block disable</code>
""".format(
                random_prefixies(px),
            )
            await eor(
                message,
                text=text,
            )
            return
        else:
            text = """
<b>Blocking users disabled.
Disable with: </b><code>{}antipm_block enable</code>
""".format(
                random_prefixies(px),
            )
            await eor(
                message,
                text=text,
            )
            return
    elif message.command[1] in [
        "enable",
        "on",
        "1",
        "yes",
        "true",
    ]:
        pydb.set_key("PMBLOCK", True)
        await eor(
            message,
            text="<b>Blocking users enabled!</b>",
        )
        return
    elif message.command[1] in [
        "disable",
        "off",
        "0",
        "no",
        "false",
    ]:
        pydb.set_key("PMBLOCK", False)
        await eor(
            message,
            text="<b>Blocking users disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}antipm_block [enable|disable|on|off]</code>",
        )
        return


plugins_helper["antipm"] = {
    f"{random_prefixies(px)}antipm [enable|disable]": "When enabled, deletes all messages from users who are not in the contact book",
    f"{random_prefixies(px)}antipm_report [enable|disable]": "Enable spam reporting",
    f"{random_prefixies(px)}antipm_block [enable|disable]": "Enable user blocking",
}
