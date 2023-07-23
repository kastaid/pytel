# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from os import remove
from random import randrange
from ..client.dbase.dbAntipm import (
    get_antipm_status,
    set_antipm,
    set_pmreport,
    get_pmreport_status,
    set_pmblock,
    get_pmblock_status,
    get_antipm_purged,
    set_pmpurged,
    set_pmlogmedia,
    get_pmlog_media,)
from ..client.dbase.dbLogger import (
    check_logger,)
from . import (
    OWNER_ID,
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
    suppress,
    humanboolean,
    buttons,
    ikmarkup,)


@pytel.instruction(is_antipm=True)
async def _anti_pm_status(
    client, message
):
    if not (pydb.get_key("ANTIPM")) or (
        not message.from_user
    ):
        return
    _ = client.me.id
    (
        is_blocked,
        is_reported,
        is_purged,
        is_scam,
        is_fake,
        is_verified,
        is_premium,
        revoke,
        just_clear,
    ) = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
    )

    if (
        get_antipm_status(user_id=_)
        == "On"
    ):
        user_info = (
            await client.resolve_peer(
                message.from_user.id
            )
        )
        if LOGCHAT_ID:
            chat_id = int(LOGCHAT_ID)
        else:
            log_data = (
                check_logger().get(_)
            )
            chat_id = int(log_data[0])

        if (
            message.from_user.is_self
            or message.from_user.is_contact
            or message.from_user.is_support
            or user_info.user_id
            in list(developer)
        ) or (
            message.from_user.id
            == int(OWNER_ID)
        ):
            return

        if message.from_user.is_scam:
            is_scam = True
        elif message.from_user.is_fake:
            is_fake = True
        elif (
            message.from_user.is_verified
        ):
            is_verified = True
        elif (
            message.from_user.is_premium
        ):
            is_premium = True

        if (
            message.from_user
            and message.text
        ):
            await sleep(
                randrange(
                    3,
                    5,
                )
            )
            x = await message.copy(
                chat_id
            )

        if (
            get_pmlog_media(user_id=_)
            == "On"
        ):
            caption = (
                message.caption
                or message.caption_entities
                if message.from_user
                and message.caption
                or message.caption_entities
                else None
            )
            if (
                message.from_user
                and message.photo
            ):
                file = await client.download_media(
                    message.photo
                )
                await sleep(
                    randrange(
                        3,
                        5,
                    )
                )
                x = await client.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=caption,
                    force_document=True,
                )
                remove(file)
            elif (
                message.from_user
                and message.video
            ):
                file = await client.download_media(
                    message.video
                )
                await sleep(
                    randrange(
                        3,
                        5,
                    )
                )
                x = await client.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=caption,
                    force_document=True,
                )
                remove(file)
            elif (
                message.from_user
                and message.document
            ):
                file = await client.download_media(
                    message.document
                )
                await sleep(
                    randrange(
                        3,
                        5,
                    )
                )
                x = await client.send_document(
                    chat_id,
                    file,
                    caption,
                    force_document=True,
                )
                remove(file)
            elif (
                message.from_user
                and message.audio
            ):
                audio = await client.download_media(
                    message.audio
                )
                await sleep(
                    randrange(
                        3,
                        5,
                    )
                )
                x = await client.send_audio(
                    chat_id,
                    audio,
                    caption,
                )
                remove(audio)
            elif (
                message.from_user
                and message.voice
            ):
                voice = await client.download_media(
                    message.voice
                )
                await sleep(
                    randrange(
                        3,
                        5,
                    )
                )
                x = await client.send_voice(
                    chat_id,
                    voice,
                    caption,
                )
                remove(voice)

        if (
            get_pmreport_status(
                user_id=_
            )
            == "On"
        ):
            await client.send(
                functions.messages.ReportSpam(
                    peer=user_info
                )
            )
        if (
            get_pmblock_status(
                user_id=_
            )
            == "On"
        ):
            await client.send(
                functions.contacts.Block(
                    id=user_info
                )
            )

        if (
            get_antipm_purged(user_id=_)
            == "On"
        ):
            just_clear, revoke = (
                True,
                True,
            )
            await client.send(
                functions.messages.DeleteHistory(
                    peer=user_info,
                    max_id=32,
                    revoke=revoke,
                    just_clear=just_clear,
                )
            )
            is_purged = True

        usrnm = await client.username(
            user_id=user_info.user_id
        )
        if usrnm:
            fmt = f"t.me/{usrnm}"
            rpm = ikmarkup(
                [
                    [
                        buttons(
                            "Check Profile",
                            url=fmt,
                        ),
                    ],
                ]
            )
        else:
            fmt = f"t.me/c/{user_info.user_id}/{message.id}"
            rpm = ikmarkup(
                [
                    [
                        buttons(
                            "Link Message",
                            url=fmt,
                        ),
                    ],
                ]
            )

        full_name = await client.user_fullname(
            user_id=user_info.user_id
        )
        text = """
#ANTIPM_LOGGER
<u><b>STATUS</b></u>
 ├ <b>Name:</b> {}
 ├ <b>User ID:</b> <code>{}</code>
 ├ <b>is_verified:</b> <code>{}</code>
 ├ <b>is_premium:</b> <code>{}</code>
 ├ <b>is_scam:</b> <code>{}</code>
 ├ <b>is_fake:</b> <code>{}</code>
 ├ <b>is_purged:</b> <code>{}</code>
 ├ <b>is_blocked:</b> <code>{}</code>
 └ <b>is_reported:</b> <code>{}</code>

(c) @kastaid #pytel
"""
        with suppress(Exception):
            replied = (
                x.id if x.id else None
            )
            await pytel_tgb.send_message(
                int(chat_id),
                text=text.format(
                    full_name,
                    user_info.user_id,
                    humanboolean(
                        is_verified
                    ),
                    humanboolean(
                        is_premium
                    ),
                    humanboolean(
                        is_scam
                    ),
                    humanboolean(
                        is_fake
                    ),
                    humanboolean(
                        is_purged
                    ),
                    humanboolean(
                        is_blocked
                    ),
                    humanboolean(
                        is_reported
                    ),
                ),
                parse_mode=ParseMode.HTML,
                disable_notification=False,
                disable_web_page_preview=False,
                reply_to_message_id=replied,
                reply_markup=rpm,
            )
            return
    else:
        return False


@pytel.instruction(
    ["antipm"],
    outgoing=True,
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
        set_antipm(
            user_id=_,
            status="On",
        )
        await eor(
            message,
            text="<b>Anti-PM Plugins enabled!</b>",
        )
        return
    elif message.command[1] in [
        "disable",
        "off",
        "0",
        "no",
        "false",
    ]:
        set_antipm(
            user_id=_,
            status="Off",
        )
        await eor(
            message,
            text="<b>Anti-PM Plugins disabled!</b>",
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
    ["pmreport"],
    outgoing=True,
)
async def _antipm_report(
    client, message
):
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_pmreport_status(
                user_id=_
            )
            == "On"
        ):
            text = """
<b>Spam-reporting enabled.
Disable with: </b><code>{}pmreport disable</code>
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
Enable with: </b><code>{}pmreport enable</code>
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
        set_pmreport(
            user_id=_,
            status="On",
        )
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
            user_id=_,
            status="Off",
        )
        await eor(
            message,
            text="<b>Spam-reporting disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}pmreport [enable|disable|on|off]</code>",
        )
        return


@pytel.instruction(
    ["pmblock"],
    outgoing=True,
)
async def _antipm_block(
    client, message
):
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_pmblock_status(
                user_id=_
            )
            == "On"
        ):
            text = """
<b>Blocking users enabled.
Disable with: </b><code>{}pmblock disable</code>
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
Enable with: </b><code>{}pmblock enable</code>
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
        set_pmblock(
            user_id=_,
            status="On",
        )
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
        set_pmblock(
            user_id=_,
            status="Off",
        )
        await eor(
            message,
            text="<b>Blocking users disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}pmblock [enable|disable|on|off]</code>",
        )
        return


@pytel.instruction(
    ["pmpurged"],
    outgoing=True,
)
async def _antipm_purged(
    client, message
):
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_antipm_purged(user_id=_)
            == "On"
        ):
            text = """
<b>Purging messages enabled.
Disable with: </b><code>{}pmpurged disable</code>
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
<b>Purging messages disabled.
Enable with: </b><code>{}pmpurged enable</code>
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
        set_pmpurged(
            user_id=_,
            status="On",
        )
        await eor(
            message,
            text="<b>Purging messages enabled!</b>",
        )
        return
    elif message.command[1] in [
        "disable",
        "off",
        "0",
        "no",
        "false",
    ]:
        set_pmpurged(
            user_id=_,
            status="Off",
        )
        await eor(
            message,
            text="<b>Purging messages disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}pmpurged [enable|disable|on|off]</code>",
        )
        return


@pytel.instruction(
    ["pmlogmedia"],
    outgoing=True,
)
async def _pmlog_media(client, message):
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_pmlog_media(user_id=_)
            == "On"
        ):
            text = """
<b>PMLog media enabled.
Disable with: </b><code>{}pmlogmedia disable</code>
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
<b>PMLog media disabled.
Enable with: </b><code>{}pmlogmedia enable</code>
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
        set_pmlogmedia(
            user_id=_,
            status="On",
        )
        await eor(
            message,
            text="<b>PMLog media enabled!</b>",
        )
        return
    elif message.command[1] in [
        "disable",
        "off",
        "0",
        "no",
        "false",
    ]:
        set_pmlogmedia(
            user_id=_,
            status="Off",
        )
        await eor(
            message,
            text="<b>PMLog media disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}pmlogmedia [enable|disable|on|off]</code>",
        )
        return


plugins_helper["antipm"] = {
    f"{random_prefixies(px)}antipm [on|off|enable|disable]": "To enable anti-pm plugins and anti-pm log.",
    f"{random_prefixies(px)}pmreport [on|off|enable|disable]": "To spam reporting",
    f"{random_prefixies(px)}pmblock [on|off|enable|disable]": "To user blocking",
    f"{random_prefixies(px)}pmpurged [on|off|enable|disable]": "When enabled, deletes all messages from users who are not in the contact book and automatically blocking user.",
    f"{random_prefixies(px)}pmlogmedia [on|off|enable|disable]": "To send any media in pm to logger. If this is not active, then the anti-pm log only runs text messages.",
}
