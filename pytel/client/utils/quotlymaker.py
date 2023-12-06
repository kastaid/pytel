# pytel < https://t.me/kastaid > Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

import json
import os
import random
import textwrap
import urllib
from typing import (
    Optional,
    Any,)
import emoji
from fontTools.ttLib import (
    TTFont,)
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageOps,)
from pyrogram.enums import (
    ChatType,)
from pyrogram.raw import (
    functions,
    types as typ,)
from pyrogram.types import (
    User,
    Chat,)

COLORS = [
    "#F07975",
    "#F49F69",
    "#F9C84A",
    "#8CC56E",
    "#6CC7DC",
    "#80C1FA",
    "#BCB3F9",
    "#E181AC",
]


async def quotlymaker(
    chats: Optional[int],
    msg: Optional[str],
    user: Any,
    client: Any,
    reply: Any,
):
    # Importıng fonts and gettings the size of text
    font = ImageFont.truetype(
        "resources/fonts/RobotoMedium.ttf",
        43,
        encoding="utf-16",
    )
    font2 = ImageFont.truetype(
        "resources/fonts/RobotoRegular.ttf",
        33,
        encoding="utf-16",
    )
    mono = ImageFont.truetype(
        "resources/fonts/SansMono.ttf",
        30,
        encoding="utf-16",
    )
    italic = ImageFont.truetype(
        "resources/fonts/RobotoItalic.ttf",
        33,
        encoding="utf-16",
    )
    fallback = ImageFont.truetype(
        "resources/fonts/Fallback.otf",
        43,
        encoding="utf-16",
    )

    # Splitting text
    maxlength = 0
    width = 0
    text = []
    for (
        line
    ) in msg.split("\n"):
        length = len(
            line
        )
        if length > 43:
            text += textwrap.wrap(
                line, 43
            )
            maxlength = (
                43
            )
            if (
                width
                < fallback.getsize(
                    line[
                        :43
                    ]
                )[
                    0
                ]
            ):
                if (
                    "MessageEntityCode"
                    in str(
                        reply.entities
                    )
                ):
                    width = (
                        mono.getsize(
                            line[
                                :43
                            ]
                        )[
                            0
                        ]
                        + 30
                    )
                else:
                    width = fallback.getsize(
                        line[
                            :43
                        ]
                    )[
                        0
                    ]
        else:
            text.append(
                line
                + "\n"
            )
            if (
                width
                < fallback.getsize(
                    line
                )[
                    0
                ]
            ):
                if (
                    "MessageEntityCode"
                    in str(
                        reply.entities
                    )
                ):
                    width = (
                        mono.getsize(
                            line
                        )[
                            0
                        ]
                        + 30
                    )
                else:
                    width = fallback.getsize(
                        line
                    )[
                        0
                    ]
            if (
                maxlength
                < length
            ):
                maxlength = length

    title = ""
    try:
        if isinstance(
            user.from_user,
            User,
        ):
            details = await client.invoke(
                functions.channels.GetParticipants(
                    chats,
                    user.from_user.id,
                )
            )
            if isinstance(
                details.participant,
                typ.ChannelParticipantCreator,
            ):
                title = (
                    details.participant.rank
                    if details.participant.rank
                    else "Creator"
                )
            elif isinstance(
                details.participant,
                typ.ChannelParticipantAdmin,
            ):
                title = (
                    details.participant.rank
                    if details.participant.rank
                    else "Admin"
                )
            else:
                title = "Anonymous"
        else:
            title = " "
    except (
        TypeError,
        KeyError,
    ):
        pass
    except (
        Exception
    ) as excp:
        client.send_log.exception(
            excp
        )

    titlewidth = (
        font2.getsize(
            title
        )[0]
    )

    nm = ""
    namewidth = 0
    userid = None
    # Get user / bot / group / channel
    try:
        if isinstance(
            user.from_user,
            User,
        ):
            userid = (
                user.from_user.id
            )
            lname = (
                ""
                if not user.from_user.last_name
                else user.from_user.last_name
            )
            nm = (
                user.from_user.first_name
                + " "
                + lname
            )
            namewidth = (
                fallback.getsize(
                    nm
                )[
                    0
                ]
                + 45
            )

        elif isinstance(
            user.sender_chat,
            Chat,
        ):
            _CG = [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]
            if (
                user.sender_chat.type
                in _CG
            ):
                userid = (
                    user.sender_chat.id
                )
                nm = (
                    user.sender_chat.title
                )
                namewidth = (
                    fallback.getsize(
                        nm
                    )[
                        0
                    ]
                    + 45
                )
    except (
        Exception
    ) as excp:
        client.send_log.exception(
            excp
        )

    if namewidth > width:
        width = namewidth
    width += (
        titlewidth + 30
        if titlewidth
        > width
        - namewidth
        else -(
            titlewidth
            - 30
        )
    )
    height = (
        len(text) * 40
    )

    # Profile Photo BG
    pfpbg = Image.new(
        "RGBA",
        (125, 600),
        (0, 0, 0, 0),
    )

    # Draw Template
    (
        top,
        middle,
        bottom,
    ) = await drawer(
        width, height
    )
    # Profile Photo Check and Fetch
    yes = False
    color = (
        random.choice(
            COLORS
        )
    )
    async for photo in client.get_chat_photos(
        userid, limit=1
    ):
        yes = True
    if yes:
        pfp = await client.download_media(
            photo.file_id
        )
        paste = (
            Image.open(
                pfp
            )
        )
        os.remove(pfp)
        paste.thumbnail(
            (105, 105)
        )

        # Mask
        mask_im = Image.new(
            "L",
            paste.size,
            0,
        )
        draw = ImageDraw.Draw(
            mask_im
        )
        draw.ellipse(
            (
                0,
                0,
                105,
                105,
            ),
            fill=255,
        )

        # Apply Mask
        pfpbg.paste(
            paste,
            (0, 0),
            mask_im,
        )
    else:
        (
            paste,
            color,
        ) = await no_photo(
            user, nm
        )
        pfpbg.paste(
            paste, (0, 0)
        )

    # Creating canvas: all the elements
    canvassize = (
        middle.width
        + pfpbg.width,
        top.height
        + middle.height
        + bottom.height,
    )
    canvas = Image.new(
        "RGBA",
        canvassize,
    )
    draw = (
        ImageDraw.Draw(
            canvas
        )
    )

    # Paste canvas
    canvas.paste(
        pfpbg, (0, 0)
    )
    canvas.paste(
        top,
        (pfpbg.width, 0),
    )
    canvas.paste(
        middle,
        (
            pfpbg.width,
            top.height,
        ),
    )
    canvas.paste(
        bottom,
        (
            pfpbg.width,
            top.height
            + middle.height,
        ),
    )
    y = 90

    # Writing Name
    space = (
        pfpbg.width + 30
    )
    namefallback = ImageFont.truetype(
        "resources/fonts/Fallback.otf",
        43,
        encoding="utf-16",
    )
    for letter in nm:
        if (
            letter
            in emoji.EMOJI_DATA
        ):
            (
                newemoji,
                mask,
            ) = await emoji_fetch(
                letter
            )
            canvas.paste(
                newemoji,
                (
                    space,
                    24,
                ),
                mask,
            )
            space += 40
        else:
            if not await fontTest(
                letter
            ):
                draw.text(
                    (
                        space,
                        20,
                    ),
                    letter,
                    font=namefallback,
                    fill=color,
                )
                space += namefallback.getsize(
                    letter
                )[
                    0
                ]
            else:
                draw.text(
                    (
                        space,
                        20,
                    ),
                    letter,
                    font=font,
                    fill=color,
                )
                space += font.getsize(
                    letter
                )[
                    0
                ]

    if title:
        draw.text(
            (
                canvas.width
                - titlewidth
                - 20,
                25,
            ),
            title,
            font=font2,
            fill="#898989",
        )

    # Writing all separating emojis and regular texts
    x = pfpbg.width + 30
    (
        bold,
        mono,
        italic,
        link,
    ) = await get_entity(
        reply
    )
    index = 0
    emojicount = 0
    textfallback = ImageFont.truetype(
        "resources/fonts/Fallback.otf",
        33,
        encoding="utf-16",
    )
    textcolor = "white"
    for line in text:
        for (
            letter
        ) in line:
            index = (
                msg.find(
                    letter
                )
                if emojicount
                == 0
                else msg.find(
                    letter
                )
                + emojicount
            )
            for (
                offset,
                length,
            ) in (
                bold.items()
            ):
                if (
                    index
                    in range(
                        offset,
                        length,
                    )
                ):
                    font2 = ImageFont.truetype(
                        "resources/fonts/RobotoMedium.ttf",
                        33,
                        encoding="utf-16",
                    )
                    textcolor = "white"
            for (
                offset,
                length,
            ) in (
                italic.items()
            ):
                if (
                    index
                    in range(
                        offset,
                        length,
                    )
                ):
                    font2 = ImageFont.truetype(
                        "resources/fonts/RobotoItalic.ttf",
                        33,
                        encoding="utf-16",
                    )
                    textcolor = "white"
            for (
                offset,
                length,
            ) in (
                mono.items()
            ):
                if (
                    index
                    in range(
                        offset,
                        length,
                    )
                ):
                    font2 = ImageFont.truetype(
                        "resources/fonts/SansMono.ttf",
                        30,
                        encoding="utf-16",
                    )
                    textcolor = "white"
            for (
                offset,
                length,
            ) in (
                link.items()
            ):
                if (
                    index
                    in range(
                        offset,
                        length,
                    )
                ):
                    font2 = ImageFont.truetype(
                        "resources/fonts/RobotoRegular.ttf",
                        30,
                        encoding="utf-16",
                    )
                    textcolor = "#898989"
            if (
                letter
                in emoji.EMOJI_DATA
            ):
                (
                    newemoji,
                    mask,
                ) = await emoji_fetch(
                    letter
                )
                canvas.paste(
                    newemoji,
                    (
                        x,
                        y
                        - 2,
                    ),
                    mask,
                )
                x += 45
                emojicount += (
                    1
                )
            else:
                if not await fontTest(
                    letter
                ):
                    draw.text(
                        (
                            x,
                            y,
                        ),
                        letter,
                        font=textfallback,
                        fill=textcolor,
                    )
                    x += textfallback.getsize(
                        letter
                    )[
                        0
                    ]
                else:
                    draw.text(
                        (
                            x,
                            y,
                        ),
                        letter,
                        font=font2,
                        fill=textcolor,
                    )
                    x += font2.getsize(
                        letter
                    )[
                        0
                    ]
            msg = msg.replace(
                letter,
                "¶",
                1,
            )
        y += 45
        x = (
            pfpbg.width
            + 30
        )
    return True, canvas


async def drawer(
    width, height
):
    # Top part
    top = Image.new(
        "RGBA",
        (width, 20),
        (0, 0, 0, 0),
    )
    draw = (
        ImageDraw.Draw(
            top
        )
    )
    draw.line(
        (
            10,
            0,
            top.width
            - 20,
            0,
        ),
        fill=(
            29,
            29,
            29,
            255,
        ),
        width=50,
    )
    draw.pieslice(
        (0, 0, 30, 50),
        180,
        270,
        fill=(
            29,
            29,
            29,
            255,
        ),
    )
    draw.pieslice(
        (
            top.width
            - 75,
            0,
            top.width,
            50,
        ),
        270,
        360,
        fill=(
            29,
            29,
            29,
            255,
        ),
    )

    # Middle part
    middle = Image.new(
        "RGBA",
        (
            top.width,
            height + 75,
        ),
        (
            29,
            29,
            29,
            255,
        ),
    )

    # Bottom part
    bottom = (
        ImageOps.flip(
            top
        )
    )

    return (
        top,
        middle,
        bottom,
    )


async def fontTest(
    letter,
):
    test = TTFont(
        "resources/fonts/RobotoMedium.ttf"
    )
    for table in test[
        "cmap"
    ].tables:
        if (
            ord(letter)
            in table.cmap.keys()
        ):
            return True


async def get_entity(
    msg,
):
    bold = {0: 0}
    italic = {0: 0}
    mono = {0: 0}
    link = {0: 0}
    if not msg.entities:
        return (
            bold,
            mono,
            italic,
            link,
        )
    for (
        entity
    ) in msg.entities:
        if isinstance(
            entity,
            typ.MessageEntityBold,
        ):
            bold[
                entity.offset
            ] = (
                entity.offset
                + entity.length
            )
        elif isinstance(
            entity,
            typ.MessageEntityItalic,
        ):
            italic[
                entity.offset
            ] = (
                entity.offset
                + entity.length
            )
        elif isinstance(
            entity,
            typ.MessageEntityCode,
        ):
            mono[
                entity.offset
            ] = (
                entity.offset
                + entity.length
            )
        elif isinstance(
            entity,
            typ.MessageEntityUrl,
        ):
            link[
                entity.offset
            ] = (
                entity.offset
                + entity.length
            )
        elif isinstance(
            entity,
            typ.MessageEntityTextUrl,
        ):
            link[
                entity.offset
            ] = (
                entity.offset
                + entity.length
            )
        elif isinstance(
            entity,
            typ.MessageEntityMention,
        ):
            link[
                entity.offset
            ] = (
                entity.offset
                + entity.length
            )
    return (
        bold,
        mono,
        italic,
        link,
    )


async def no_photo(
    reply, nm
):
    pfp = Image.new(
        "RGBA",
        (105, 105),
        (0, 0, 0, 0),
    )
    pen = ImageDraw.Draw(
        pfp
    )
    color = (
        random.choice(
            COLORS
        )
    )
    pen.ellipse(
        (0, 0, 105, 105),
        fill=color,
    )
    letter = (
        ""
        if not nm
        else nm[0]
    )
    font = ImageFont.truetype(
        "resources/fonts/RobotoRegular.ttf",
        60,
    )
    pen.text(
        (32, 17),
        letter,
        font=font,
        fill="white",
    )
    return pfp, color


async def emoji_fetch(
    emoji,
):
    emojis = json.loads(
        urllib.request.urlopen(
            "https://github.com/erenmetesar/modules-repo/raw/master/emojis.txt"
        )
        .read()
        .decode()
    )
    if emoji in emojis:
        img = emojis[
            emoji
        ]
        return await transparent(
            urllib.request.urlretrieve(
                img,
                "resources/emoji.png",
            )[
                0
            ]
        )
    img = emojis["⛔"]
    return await transparent(
        urllib.request.urlretrieve(
            img,
            "resources/emoji.png",
        )[
            0
        ]
    )


async def transparent(
    emoji,
):
    emoji = Image.open(
        emoji
    ).convert("RGBA")
    emoji.thumbnail(
        (40, 40)
    )

    # Mask
    mask = Image.new(
        "L", (40, 40), 0
    )
    draw = (
        ImageDraw.Draw(
            mask
        )
    )
    draw.ellipse(
        (0, 0, 40, 40),
        fill=255,
    )
    return emoji, mask
