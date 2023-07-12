# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from ..client.dbase.dbAntipm import (
    get_antipm_status,
    set_antipm,
    set_pmreport,
    get_pmreport_status,
    set_pmblock,
    get_pmblock_status,
)
from ..client.dbase.dbLogger import (
    check_logger,
)
from . import (
    LOGCHAT_ID,
    ParseMode,
    eor,
    developer,
    functions,
    plugins_helper,
    px,
    pydb,
    pytel,
    pytel_tgb,
    random_prefixies,
)

PM_STATUS: bool = (
    pydb.get_key("ANTIPM")
    if pydb.get_key("ANTIPM")
    else False
)


@pytel.instruction(is_antipm=PM_STATUS)
async def _anti_pm_status(client, message):
    _ = client.me.id
    if get_antipm_status(user_id=_) != "On":
        return

    is_blocked, is_reported = None, None
    user_info = await client.resolve_peer(
        message.chat.id
    )
    if user_info.user_id in developer:
        return

    if (
        get_pmreport_status(user_id=_)
        == "On"
    ):
        await client.send(
            functions.messages.ReportSpam(
                peer=user_info
            )
        )
        is_reported = "Yes"
    if (
        get_pmblock_status(user_id=_)
        == "On"
    ):
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

    if LOGCHAT_ID:
        chat_id = int(LOGCHAT_ID)
    else:
        log_data = check_logger().get(_)
        chat_id = int(log_data[0])
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
        int(chat_id),
        text,
        parse_mode=ParseMode.HTML,
        disable_notification=False,
    )


@pytel.instruction(
    ["antipm", "anti_pm"], outgoing=True
)
async def _anti_pm(client, message):
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_antipm_status(user_id=_)
            == "On"
        ):
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
        set_antipm(user_id=_, status="On")
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
        set_antipm(user_id=_, status="Off")
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
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_pmreport_status(user_id=_)
            == "On"
        ):
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
        set_pmreport(user_id=_, status="On")
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
        set_pmreport(
            user_id=_, status="Off"
        )
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
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_pmblock_status(user_id=_)
            == "On"
        ):
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
        set_pmblock(user_id=_, status="On")
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
        set_pmblock(user_id=_, status="Off")
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
