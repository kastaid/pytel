# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pyrogram.enums import ChatType
from pyrogram.errors import RPCError
from ..client.dbase.dbLogger import (
    check_logger,)
from . import (
    Rooters,
    LOGCHAT_ID,
    _try_purged,
    eor,
    get_text,
    is_url,
    plugins_helper,
    px,
    pytel,
    progress,
    time,
    suppress,
    random_prefixies,)


@pytel.instruction(
    ["swiper"],
    outgoing=True,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _swipper(client, message):
    _ = client.me.id
    if message.reply_to_message:
        rep = message.reply_to_message
        caption = (
            rep.caption
            or rep.caption_entities
            if rep.caption
            or rep.caption_entities
            else None
        )
        await _try_purged(message)
        if LOGCHAT_ID:
            chat_id = int(LOGCHAT_ID)
        else:
            log_data = (
                check_logger().get(_)
            )
            chat_id = int(log_data[0])
        if (
            rep.document
            or rep.video
            or rep.photo
        ):
            file = await client.download_media(
                rep, "cache/"
            )
            await client.send_document(
                chat_id=chat_id,
                document=file,
                caption=caption,
                force_document=True,
            )
            (Rooters / file).unlink(
                missing_ok=True
            )
            return

        else:
            return

    else:
        url = get_text(
            message, save_link=True
        )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid link telegram or reply to media!",
        )

    x = await eor(
        message,
        text="Swiper no swiping...",
    )
    if url.startswith("https"):
        if "?single" in url:
            link_ = url.split(
                "?single"
            )[0]
            msg_id = int(
                link_.split("/")[-1]
            )
        else:
            msg_id = int(
                url.split("/")[-1]
            )
        if "t.me/c/" in url:
            try:
                chat = int(
                    "-100"
                    + str(
                        url.split("/")[
                            -2
                        ]
                    )
                )
                m = await client.get_messages(
                    chat, msg_id
                )
            except RPCError:
                await eor(
                    x,
                    text="You must first join the target channel.",
                )
                return
            try:
                await client.copy_message(
                    message.chat.id,
                    chat,
                    msg_id,
                    reply_to_message_id=message.id,
                )
                await _try_purged(
                    x, 1.5
                )
            except Exception:
                await downloads_media(
                    client,
                    message,
                    m,
                    x,
                )
            await _try_purged(x, 1.5)
            return
        else:
            try:
                chat = str(
                    url.split("/")[-2]
                )
                ms = await client.get_chat(
                    chat
                )
            except RPCError:
                await eor(
                    x,
                    text="You must first join the target channel.",
                )
            if (
                ms.type
                == ChatType.CHANNEL
            ):
                m = await client.get_messages(
                    chat, msg_id
                )
                await downloads_media(
                    client,
                    message,
                    m,
                    x,
                )
                await _try_purged(
                    x, 1.5
                )
                return
            else:
                try:
                    await client.copy_message(
                        message.chat.id,
                        chat,
                        msg_id,
                        reply_to_message_id=message.id,
                    )
                    await _try_purged(
                        x, 1.5
                    )
                except Exception:
                    m = await client.get_messages(
                        chat, msg_id
                    )
                    await downloads_media(
                        client,
                        message,
                        m,
                        x,
                    )
                    await _try_purged(
                        x, 1.5
                    )
                    return


async def downloads_media(
    client,
    message,
    m,
    x,
):
    caption = (
        m.caption
        or m.caption_entities
        or None
    )
    with suppress(Exception):
        if (m.text) or (m.sticker):
            await m.copy(
                message.chat.id,
                reply_to_message_id=message.id,
            )
        s_time = time()
        if m.photo:
            photo = await client.download_media(
                m.photo,
                progress=progress,
                progress_args=(
                    x,
                    s_time,
                    "`Downloading File!`",
                    "Telegram Photo",
                ),
            )
            u_time = time()
            await client.send_photo(
                message.chat.id,
                photo=photo,
                caption=caption,
                reply_to_message_id=message.id,
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Telegram Photo",
                ),
            )
            (Rooters / photo).unlink(
                missing_ok=True
            )
        if m.video:
            video = await client.download_media(
                m.video,
                progress=progress,
                progress_args=(
                    x,
                    s_time,
                    "`Downloading File!`",
                    "Telegram Video",
                ),
            )
            u_time = time()
            await client.send_video(
                message.chat.id,
                video=video,
                caption=caption,
                supports_streaming=True,
                reply_to_message_id=message.id,
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Telegram Video",
                ),
            )
            (Rooters / video).unlink(
                missing_ok=True
            )
        if m.document:
            file = await client.download_media(
                m.document,
                progress=progress,
                progress_args=(
                    x,
                    s_time,
                    "`Downloading File!`",
                    "Telegram Document",
                ),
            )
            u_time = time()
            await client.send_document(
                message.chat.id,
                document=file,
                caption=caption,
                force_document=True,
                reply_to_message_id=message.id,
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Telegram Document",
                ),
            )
            (Rooters / file).unlink(
                missing_ok=True
            )
        if m.audio:
            audio = await client.download_media(
                m.audio,
                progress=progress,
                progress_args=(
                    x,
                    s_time,
                    "`Downloading File!`",
                    "Telegram Audio",
                ),
            )
            u_time = time()
            await client.send_audio(
                message.chat.id,
                audio,
                caption,
                reply_to_message_id=message.id,
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Telegram Audio",
                ),
            )
            (Rooters / audio).unlink(
                missing_ok=True
            )
        if m.voice:
            voice = await client.download_media(
                m.voice,
                progress=progress,
                progress_args=(
                    x,
                    s_time,
                    "`Downloading File!`",
                    "Telegram Voice",
                ),
            )
            u_time = time()
            await client.send_voice(
                message.chat.id,
                voice,
                caption,
                reply_to_message_id=message.id,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Telegram Voice",
                ),
            )
            (Rooters / voice).unlink(
                missing_ok=True
            )
        if m.animation:
            animation = await client.download_media(
                m.animation,
                progress=progress,
                progress_args=(
                    x,
                    s_time,
                    "`Downloading File!`",
                    "Telegram Animation",
                ),
            )
            u_time = time()
            await client.send_animation(
                message.chat.id,
                animation,
                caption,
                reply_to_message_id=message.id,
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Telegram Animation",
                ),
            )
            (
                Rooters / animation
            ).unlink(missing_ok=True)


plugins_helper["swiper"] = {
    f"{random_prefixies(px)}swiper [link messages media/sticker/text (channel/groups)] / [reply to media/document]": "To get files/text/stickers on a channel/groups. ( <i>You must first join the target channel if channel's private</i> )\n\n<b>Note:</b> <i>If you reply to media/document, the file will be sent to the channel logger</i>.",
}
