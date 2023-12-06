# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import (
    sleep,
    gather,)
from io import BytesIO
import cv2
from PIL import Image
from pyrogram import (
    emoji,)
from pyrogram.errors import (
    StickersetInvalid,
    YouBlockedUser,)
from pyrogram.raw.functions.messages import (
    GetStickerSet,)
from pyrogram.raw.types import (
    InputStickerSetShortName,)
from . import (
    ChatSendStickersForbidden,
    ParseMode,
    Rooters,
    Memify,
    eor,
    get_args,
    get_random_hex,
    plugins_helper,
    px,
    pytel,
    replied,
    resize_media,
    random_prefixies,
    _try_purged,
    quotlymaker,)


async def get_response(
    message, client
):
    return [
        x
        async for x in client.get_chat_history(
            "Stickers",
            limit=1,
        )
    ][0].text


@pytel.instruction(
    [
        "sti",
        "stickerinfo",
    ],
    outgoing=True,
)
async def _stickers_info(
    client, message
):
    x = await eor(
        message,
        text="Processing...",
    )
    if (
        not message.reply_to_message
    ):
        await eor(
            x,
            text="Please Reply To Sticker.",
        )
        return
    if (
        not message.reply_to_message.sticker
    ):
        await eor(
            x,
            text="Please Reply To A Sticker.",
        )
        return
    if (
        not message.reply_to_message.sticker.set_name
    ):
        await eor(
            x,
            text="Seems Like A Stray Sticker!",
        )
        return
    stickerset = await client.invoke(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=message.reply_to_message.sticker.set_name
            ),
            hash=0,
        )
    )
    emojis = []
    for (
        stucker
    ) in (
        stickerset.packs
    ):
        if (
            stucker.emoticon
            not in emojis
        ):
            emojis.append(
                stucker.emoticon
            )
    output = f"""**Sticker Pack Title **: `{stickerset.set.title}`
**Sticker Pack Short Name **: `{stickerset.set.short_name}`
**Stickers Count **: `{stickerset.set.count}`
**Archived **: `{stickerset.set.archived}`
**Official **: `{stickerset.set.official}`
**Masks **: `{stickerset.set.masks}`
**Animated **: `{stickerset.set.animated}`
**Emojis In Pack **: `{' '.join(emojis)}`
"""
    await x.edit(output)
    emojis.clear()


@pytel.instruction(
    [
        "ts",
        "takesticker",
    ],
    outgoing=True,
)
async def _take_stickers(
    client, message
):
    user = client.me
    replied = (
        message.reply_to_message
    )
    x = await eor(
        message,
        text="Taking stickers...",
    )
    media_ = None
    emoji_ = None
    is_anim = False
    is_video = False
    resize = False
    ff_vid = False
    if (
        replied
        and replied.media
    ):
        if replied.photo:
            resize = True
        elif (
            replied.document
            and "image"
            in replied.document.mime_type
        ):
            resize = True
            replied.document.file_name
        elif (
            replied.document
            and "tgsticker"
            in replied.document.mime_type
        ):
            is_anim = (
                True
            )
            replied.document.file_name
        elif (
            replied.document
            and "video"
            in replied.document.mime_type
        ):
            resize = True
            is_video = (
                True
            )
            ff_vid = True
        elif (
            replied.animation
        ):
            resize = True
            is_video = (
                True
            )
            ff_vid = True
        elif (
            replied.video
        ):
            resize = True
            is_video = (
                True
            )
            ff_vid = True
        elif (
            replied.sticker
        ):
            if (
                not replied.sticker.file_name
            ):
                await eor(
                    x,
                    text="The sticker has no name/pack.",
                )
                return
            emoji_ = (
                replied.sticker.emoji
            )
            is_anim = (
                replied.sticker.is_animated
            )
            is_video = (
                replied.sticker.is_video
            )
            if not (
                replied.sticker.file_name.endswith(
                    ".tgs"
                )
                or replied.sticker.file_name.endswith(
                    ".webm"
                )
            ):
                resize = (
                    True
                )
                ff_vid = (
                    True
                )
        else:
            await eor(
                x,
                text="Stickers not supported.",
            )
            return
        media_ = await client.download_media(
            replied
        )
    else:
        await eor(
            x,
            text="Please Reply to Media Photo/GIF/Stickers.",
        )
        return
    if media_:
        args = get_args(
            message
        )
        pack = 1
        if (
            len(args)
            == 2
        ):
            (
                emoji_,
                pack,
            ) = args
        elif (
            len(args)
            == 1
        ):
            if args[
                0
            ].isnumeric():
                pack = int(
                    args[
                        0
                    ]
                )
            else:
                emoji_ = args[
                    0
                ]

        if (
            emoji_
            and emoji_
            not in (
                getattr(
                    emoji,
                    _,
                )
                for _ in dir(
                    emoji
                )
                if not _.startswith(
                    "_"
                )
            )
        ):
            emoji_ = None
        if not emoji_:
            emoji_ = "✨"

        u_name = (
            user.username
        )
        u_name = (
            "@" + u_name
            if u_name
            else user.first_name
            or user.id
        )
        packname = f"Sticker_u{user.id}_v{pack}"
        custom_packnick = f"{u_name} Sticker Pack"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = "/newpack"
        if resize:
            media_ = resize_media(
                media_,
                is_video,
                ff_vid,
            )
        if is_anim:
            packname += "_animated"
            packnick += " (Animated)"
            cmd = "/newanimated"
        if is_video:
            packname += (
                "_video"
            )
            packnick += " (Video)"
            cmd = "/newvideo"
        exist = False
        while True:
            try:
                exist = await client.invoke(
                    GetStickerSet(
                        stickerset=InputStickerSetShortName(
                            short_name=packname
                        ),
                        hash=0,
                    )
                )
            except StickersetInvalid:
                exist = (
                    False
                )
                break
            limit = (
                50
                if (
                    is_video
                    or is_anim
                )
                else 120
            )
            if (
                exist.set.count
                >= limit
            ):
                pack += 1
                packname = f"a{user.id}_{pack}"
                packnick = f"{custom_packnick} Vol.{pack}"
                if is_anim:
                    packname += f"_anim{pack}"
                    packnick += f" (Animated){pack}"
                if is_video:
                    packname += f"_video{pack}"
                    packnick += f" (Video){pack}"
                await eor(
                    x,
                    text="Creating New Stickers...",
                )
                continue
            break

        if (
            exist
            is not False
        ):
            try:
                await client.send_message(
                    "stickers",
                    "/addsticker",
                )
            except YouBlockedUser:
                await client.unblock_user(
                    "stickers"
                )
                await sleep(
                    2
                )
                await client.send_message(
                    "stickers",
                    "/addsticker",
                )
            except (
                Exception
            ) as excp:
                await x.edit(
                    f"<b>Exception:</b> <code>{excp}</code>"
                )
                return
            await sleep(
                2
            )
            await client.send_message(
                "stickers",
                packname,
            )
            await sleep(
                2
            )
            limit = (
                "50"
                if is_anim
                else "120"
            )
            while (
                limit
                in await get_response(
                    message,
                    client,
                )
            ):
                pack += 1
                packname = f"a{user.id}_{get_random_hex()}_{pack}"
                packnick = f"{custom_packnick} vol.{pack}"
                if is_anim:
                    packname += "_anim"
                    packnick += " (Animated)"
                if is_video:
                    packname += "_video"
                    packnick += " (Video)"
                await eor(
                    x,
                    text="Creating New Stickers...",
                )
                await client.send_message(
                    "stickers",
                    packname,
                )
                await sleep(
                    2
                )
                if (
                    await get_response(
                        message,
                        client,
                    )
                    == "Invalid pack selected."
                ):
                    await client.send_message(
                        "stickers",
                        cmd,
                    )
                    await sleep(
                        2
                    )
                    await client.send_message(
                        "stickers",
                        packnick,
                    )
                    await sleep(
                        2
                    )
                    await client.send_document(
                        "stickers",
                        media_,
                    )
                    await sleep(
                        2
                    )
                    await client.send_message(
                        "Stickers",
                        emoji_,
                    )
                    await sleep(
                        2
                    )
                    await client.send_message(
                        "Stickers",
                        "/publish",
                    )
                    await sleep(
                        2
                    )
                    if is_anim:
                        await client.send_message(
                            "Stickers",
                            f"<{packnick}>",
                            parse_mode=ParseMode.MARKDOWN,
                        )
                        await sleep(
                            2
                        )
                    await client.send_message(
                        "Stickers",
                        "/skip",
                    )
                    await sleep(
                        2
                    )
                    await client.send_message(
                        "Stickers",
                        packname,
                    )
                    await sleep(
                        2
                    )
                    text = f"""
--**Sticker Added Successfully.**--
└ **Sticker Pack:** --[Click Here](https://t.me/addstickers/{packname})--
"""
                    await x.edit(
                        text=text,
                    )
                    return
            await client.send_document(
                "stickers",
                media_,
            )
            await sleep(
                2
            )
            if (
                await get_response(
                    message,
                    client,
                )
                == "Sorry, the file type is invalid."
            ):
                await x.edit(
                    text="Failed to add sticker. Please add stickers manually to @Stickers"
                )
                return
            await client.send_message(
                "Stickers",
                emoji_,
            )
            await sleep(
                2
            )
            await client.send_message(
                "Stickers",
                "/done",
            )
        else:
            await x.edit(
                "Adding sticker..."
            )
            try:
                await client.send_message(
                    "Stickers",
                    cmd,
                )
            except YouBlockedUser:
                await client.unblock_user(
                    "stickers"
                )
                await client.send_message(
                    "stickers",
                    "/addsticker",
                )
            await sleep(
                2
            )
            await client.send_message(
                "Stickers",
                packnick,
            )
            await sleep(
                2
            )
            await client.send_document(
                "stickers",
                media_,
            )
            await sleep(
                2
            )
            if (
                await get_response(
                    message,
                    client,
                )
                == "Sorry, the file type is invalid."
            ):
                await x.edit(
                    text="Failed to add sticker. Please add stickers manually to @Stickers"
                )
                return
            await client.send_message(
                "Stickers",
                emoji_,
            )
            await sleep(
                2
            )
            await client.send_message(
                "Stickers",
                "/publish",
            )
            await sleep(
                2
            )
            if is_anim:
                await client.send_message(
                    "Stickers",
                    f"<{packnick}>",
                )
                await sleep(
                    2
                )
            await client.send_message(
                "Stickers",
                "/skip",
            )
            await sleep(
                2
            )
            await client.send_message(
                "Stickers",
                packname,
            )
            await sleep(
                2
            )
        text = f"""
--**Sticker Added Successfully.**--
└ **Sticker Pack:** --[Click Here](https://t.me/addstickers/{packname})--
"""
        await x.edit(
            text=text,
        )
        if (
            Rooters
            / media_
        ).exists():
            (
                Rooters
                / media_
            ).unlink(
                missing_ok=True
            )


@pytel.instruction(
    [
        "gst",
        "getsticker",
    ],
    outgoing=True,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _get_stickers(
    client, message
):
    await message.edit(
        "`Downloading . . .`"
    )
    path = (
        await message.reply_to_message.download()
    )
    with open(
        path, "rb"
    ) as f:
        content = (
            f.read()
        )

    file_io = BytesIO(
        content
    )
    names = f"sticker_{get_random_hex()}.png"
    file_io.name = names

    await gather(
        message.delete(),
        client.send_photo(
            message.chat.id,
            file_io,
            reply_to_message_id=replied(
                message
            ),
        ),
    )
    (
        Rooters / names
    ).unlink(
        missing_ok=True
    )


@pytel.instruction(
    ["tiny"],
    outgoing=True,
)
async def _tiny_stickers(
    client, message
):
    reply = (
        message.reply_to_message
    )
    if not (
        reply
        and (reply.media)
    ):
        await eor(
            message,
            text="Please Reply to Media Photo/GIF/Stickers.",
        )
        return
    x = await eor(
        message,
        text="`Processing . . .`",
    )
    fl = await client.download_media(
        reply
    )
    blank = Image.open(
        "resources/images/image_blank.png"
    )
    if fl.endswith(
        (".tgs", ".webm")
    ):
        await eor(
            x,
            text="File not supported.",
        )
        return
    elif fl.endswith(
        (".gif", ".mp4")
    ):
        ifl = cv2.VideoCapture(
            fl
        )
        busy = ifl.read()
        cv2.imwrite(
            "i.png", busy
        )
        fil = "i.png"
        imgs = (
            Image.open(
                fil
            )
        )
        z, d = imgs.size
        if z == d:
            xxx, yyy = (
                200,
                200,
            )
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (
                a * 100
            ) - 50
            bb = (
                b * 100
            ) - 50
            xxx = (
                200
                + 5 * aa
            )
            yyy = (
                200
                + 5 * bb
            )
        h = imgs.resize(
            (
                int(xxx),
                int(yyy),
            )
        )
        h.save(
            "h.png",
            format="PNG",
            optimize=True,
        )
        blanked = (
            Image.open(
                "h.png"
            )
        )
        blank_img = (
            blank.copy()
        )
        blank_img.paste(
            blanked,
            (150, 0),
        )
        blank_img.save(
            "a.webp",
            "WEBP",
            quality=95,
        )
        file = "a.webp"
        (
            Rooters / fil
        ).unlink(
            missing_ok=True
        )
        (
            Rooters
            / "h.png"
        ).unlink(
            missing_ok=True
        )
    else:
        imgs = (
            Image.open(
                fl
            )
        )
        z, d = imgs.size
        if z == d:
            xxx, yyy = (
                200,
                200,
            )
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (
                a * 100
            ) - 50
            bb = (
                b * 100
            ) - 50
            xxx = (
                200
                + 5 * aa
            )
            yyy = (
                200
                + 5 * bb
            )
        h = imgs.resize(
            (
                int(xxx),
                int(yyy),
            )
        )
        h.save(
            "h.png",
            format="PNG",
            optimize=True,
        )
        blanked = (
            Image.open(
                "h.png"
            )
        )
        blank_img = (
            blank.copy()
        )
        blank_img.paste(
            blanked,
            (150, 0),
        )
        blank_img.save(
            "a.webp",
            "WEBP",
            quality=95,
        )
        file = "a.webp"
        (
            Rooters
            / "h.png"
        ).unlink(
            missing_ok=True
        )
    try:
        await gather(
            x.delete(),
            client.send_sticker(
                message.chat.id,
                sticker=file,
                reply_to_message_id=replied(
                    message
                ),
            ),
        )
        (
            Rooters
            / file
        ).unlink(
            missing_ok=True
        )
        (
            Rooters / fl
        ).unlink(
            missing_ok=True
        )
        return
    except ChatSendStickersForbidden:
        await x.edit(
            "You can’t send stickers in this chat."
        )
        (
            Rooters
            / file
        ).unlink(
            missing_ok=True
        )
        (
            Rooters / fl
        ).unlink(
            missing_ok=True
        )
        return


@pytel.instruction(
    ["mmf", "memify"],
    outgoing=True,
)
async def _memify(
    client, message
):
    if (
        not message.reply_to_message_id
    ):
        await eor(
            message,
            text="Please Reply to Media Photo/Stickers.",
        )
        return
    reps = (
        message.reply_to_message
    )
    if not reps.media:
        await eor(
            message,
            text="Please Reply to Media Photo/Stickers.",
        )
        return
    text = get_args(
        message
    )
    if len(text) < 1:
        await eor(
            message,
            text="Please provide text.",
        )
        return
    x = await eor(
        message,
        text="`Memify . . .`",
    )

    if (
        reps.photo
        and reps.photo.file_id
    ):
        file = await client.download_media(
            reps.photo.file_id,
            "cache/",
        )
    elif (
        reps.sticker
        and reps.sticker.file_id
    ):
        file = await client.download_media(
            reps.sticker.file_id,
            "cache/",
        )
    else:
        await eor(
            x,
            text="Please Reply to Media Photo/Stickers.",
        )
        return

    meme = Memify(
        file, text
    )
    try:
        await gather(
            x.delete(),
            client.send_sticker(
                message.chat.id,
                sticker=meme,
                reply_to_message_id=replied(
                    message
                ),
            ),
        )
        (
            Rooters
            / file
        ).unlink(
            missing_ok=True
        )
        (
            Rooters
            / meme
        ).unlink(
            missing_ok=True
        )
        return
    except ChatSendStickersForbidden:
        await x.edit(
            "You can’t send stickers in this chat."
        )
        (
            Rooters
            / file
        ).unlink(
            missing_ok=True
        )
        (
            Rooters
            / meme
        ).unlink(
            missing_ok=True
        )
        return


@pytel.instruction(
    ["q", "quotly"],
    outgoing=True,
    supergroups=True,
)
async def _quotly_stickers(
    client, message
):
    text = None
    y = await eor(
        message,
        text="Checking...",
    )
    reply = (
        message.reply_to_message
    )
    text = (
        reply.text
        or reply.caption
        or reply.caption_entities
    )
    if not text:
        await eor(
            y,
            text="Please reply to message!",
        )
        return

    x = await eor(
        y,
        text="Creating...",
    )

    user = await client.get_messages(
        message.chat.id,
        message_ids=message.id,
        reply_to_message_ids=reply.id,
    )
    (
        res,
        canvas,
    ) = await quotlymaker(
        message.chat.id,
        text,
        reply,
        client,
        user,
    )
    if not res:
        await eor(
            x,
            text="Try again later!",
        )
        return
    files = f"{client.me.id}_quotly.webp"
    canvas.save(files)
    try:
        await client.send_sticker(
            message.chat.id,
            sticker=files,
            reply_to_message_id=replied(
                message
            ),
        )
        await _try_purged(
            x
        )
        (
            Rooters
            / files
        ).unlink(
            missing_ok=True
        )
        return
    except ChatSendStickersForbidden:
        await x.edit(
            "You can’t send stickers in this chat."
        )
        (
            Rooters
            / files
        ).unlink(
            missing_ok=True
        )


plugins_helper[
    "stickers"
] = {
    f"{random_prefixies(px)}sti / stickerinfo [reply to sticker]": "To get stickers information.",
    f"{random_prefixies(px)}ts / takesticker [reply to sticker/gif/photo + (emoji/not))]": "To take sticker.",
    f"{random_prefixies(px)}gst / getsticker [reply to sticker]": "Convert sticker to be Image/Photo.",
    f"{random_prefixies(px)}mmf / memify [text] & [reply to photo/sticker]": "To add text to the image/sticker.",
    f"{random_prefixies(px)}tiny [reply to sticker]": "To reduce the sticker size.",
    f"{random_prefixies(px)}quotly / q [reply to image / reply to message]": "To create quotly.",
}
