# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from os import remove
from pyrogram.types import (
    InlineKeyboardMarkup,
)
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
    get_pmlog_media,
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
    pytel,
    pytel_tgb,
    random_prefixies,
    suppress,
    humanboolean,
    buttons,
)


@pytel.instruction(is_antipm=True)
async def _anti_pm_status(client, message):
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

    if get_antipm_status(user_id=_) == "On":
        user_info = (
            await client.resolve_peer(
                message.from_user.id
            )
        )
        if LOGCHAT_ID:
            chat_id = int(LOGCHAT_ID)
        else:
            log_data = check_logger().get(_)
            chat_id = int(log_data[0])

        if (
            message.from_user.is_self
            or user_info.user_id
            in developer
        ):
            return

        if message.from_user.is_scam:
            is_scam = True
        elif message.from_user.is_fake:
            is_fake = True
        elif message.from_user.is_verified:
            is_verified = True
        elif message.from_user.is_premium:
            is_premium = True

        if (
            message.from_user
            and message.text
        ):
            x = await message.copy(chat_id)

        if (
            get_pmlog_media(user_id=_)
            == "On"
        ):
            caption = (
                message.caption
                if message.from_user
                and message.caption
                else None
            )
            if (
                message.from_user
                and message.photo
            ):
                photo = await client.download_media(
                    message.photo
                )
                x = await client.send_photo(
                    chat_id, photo, caption
                )
                remove(photo)
            elif (
                message.from_user
                and message.video
            ):
                video = await client.download_media(
                    message.video
                )
                x = await client.send_video(
                    chat_id, video, caption
                )
                remove(video)
            elif (
                message.from_user
                and message.audio
            ):
                audio = await client.download_media(
                    message.audio
                )
                x = await client.send_audio(
                    chat_id, audio, caption
                )
                remove(audio)
            elif (
                message.from_user
                and message.voice
            ):
                voice = await client.download_media(
                    message.voice
                )
                x = await client.send_voice(
                    chat_id, voice, caption
                )
                remove(voice)
            elif (
                message.from_user
                and message.document
            ):
                document = await client.download_media(
                    message.document
                )
                x = await client.send_document(
                    chat_id,
                    document,
                    caption,
                )
                remove(document)

        if (
            get_pmreport_status(user_id=_)
            == "On"
        ):
            await client.send(
                functions.messages.ReportSpam(
                    peer=user_info
                )
            )
            is_reported, revoke = True, True
        if (
            get_pmblock_status(user_id=_)
            == "On"
        ):
            await client.send(
                functions.contacts.Block(
                    id=user_info
                )
            )
            is_blocked, revoke = True, True

        if (
            get_antipm_purged(user_id=_)
            == "On"
        ):
            await client.send(
                functions.contacts.Block(
                    id=user_info
                )
            )
            await client.send(
                functions.messages.DeleteHistory(
                    peer=user_info,
                    max_id=32,
                    revoke=revoke,
                    just_clear=just_clear,
                )
            )
            is_purged, is_blocked = (
                True,
                True,
            )

        usrnm = await client._username(
            user_id=user_info.user_id
        )
        if usrnm:
            fmt = f"t.me/{usrnm}"
            rpm = InlineKeyboardMarkup(
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
            rpm = None

        full_name = await client._fullname(
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
            replied = x.id if x.id else None
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
                    humanboolean(is_scam),
                    humanboolean(is_fake),
                    humanboolean(is_purged),
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
Enable with: </b><code>{}antipm_report enable</code>
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
Enable with: </b><code>{}antipm_block enable</code>
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


@pytel.instruction(
    "antipm_purged", outgoing=True
)
async def _antipm_purged(client, message):
    _ = client.me.id
    if len(message.command) == 1:
        if (
            get_antipm_purged(user_id=_)
            == "On"
        ):
            text = """
<b>Purging messages enabled.
Disable with: </b><code>{}antipm_purged disable</code>
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
Enable with: </b><code>{}antipm_purged enable</code>
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
        set_pmpurged(user_id=_, status="On")
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
            user_id=_, status="Off"
        )
        await eor(
            message,
            text="<b>Purging messages disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}antipm_purged [enable|disable|on|off]</code>",
        )
        return


@pytel.instruction(
    "pmlog_media", outgoing=True
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
Disable with: </b><code>{}pmlog_media disable</code>
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
Enable with: </b><code>{}pmlog_media enable</code>
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
            user_id=_, status="On"
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
            user_id=_, status="Off"
        )
        await eor(
            message,
            text="<b>PMLog media disabled!</b>",
        )
        return
    else:
        await eor(
            message,
            text=f"<b>Usage:</b> <code>{random_prefixies(px)}pmlog_media [enable|disable|on|off]</code>",
        )
        return


plugins_helper["antipm"] = {
    f"{random_prefixies(px)}antipm [enable|disable]": "To enable anti-pm plugins and anti-pm log.",
    f"{random_prefixies(px)}antipm_report [enable|disable]": "To spam reporting",
    f"{random_prefixies(px)}antipm_block [enable|disable]": "To user blocking",
    f"{random_prefixies(px)}antipm_purged [enable|disable]": "When enabled, deletes all messages from users who are not in the contact book and automatically blocking user.",
    f"{random_prefixies(px)}pmlog_media [enable|disable]": "To send any media in pm to logger. If this is not active, then the anti-pm log only runs text messages.",
}
