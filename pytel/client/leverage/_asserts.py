# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import sleep
from contextlib import (
    suppress,)
from re import (
    findall,
    search,)
from typing import (
    Optional,
    Union,
    Any,)
from pyrogram.enums import (
    MessageEntityType,)
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageTooLong,)
from pyrogram.raw.types import (
    InputPeerChat,
    InputPeerChannel,)
from pyrogram.types import (
    Message,)
from pytelibs import (
    _supersu,)
from ...config import (
    OWNER_ID,)


async def _try_purged(
    message: Message,
    timer: Union[
        int, float
    ] = None,
    revoke: bool = True,
):
    with suppress(
        BaseException
    ):
        if timer:
            await sleep(
                timer
            )
            await message.delete(
                revoke=revoke
            )
            return
        else:
            await message.delete(
                revoke=revoke
            )
            return


async def eor(
    message: Message,
    text: Optional[str],
    *args,
    **kwargs,
) -> Message:
    chunks, chunks1 = (
        [],
        [],
    )
    chunk, chunk1 = (
        "",
        "",
    )
    try:
        if (
            message.sender_chat
        ):
            try:
                return await message.edit_text(
                    text=text,
                    *args,
                    **kwargs,
                )
            except BaseException:
                await message.reply(
                    text=text,
                    *args,
                    **kwargs,
                )
                with suppress(
                    Exception
                ):
                    await _try_purged(
                        message
                    )
                return

        reply = (
            message.reply_to_message
        )
        if reply:
            try:
                if (
                    message.from_user.is_self
                ):
                    return await message.edit_text(
                        text=text,
                        *args,
                        **kwargs,
                    )
            except BaseException:
                return await message.reply(
                    text=text,
                    *args,
                    **kwargs,
                )
                with suppress(
                    Exception
                ):
                    await _try_purged(
                        message
                    )
                return

            try:
                if (
                    message.from_user.id
                    in list(
                        _supersu
                    )
                    or OWNER_ID
                ):
                    return await message.reply(
                        text=text,
                        *args,
                        **kwargs,
                    )
                    with suppress(
                        Exception
                    ):
                        await _try_purged(
                            message
                        )
                    return
                else:
                    return await message.edit_text(
                        text=text,
                        *args,
                        **kwargs,
                    )
            except BaseException:
                return await message.reply(
                    text=text,
                    *args,
                    **kwargs,
                )
                with suppress(
                    Exception
                ):
                    await _try_purged(
                        message
                    )
                return

            if (
                message.from_user
            ):
                return await message.reply(
                    text=text,
                    *args,
                    **kwargs,
                )
            else:
                return await message.edit_text(
                    text=text,
                    *args,
                    **kwargs,
                )
        else:
            if (
                message.from_user.is_self
            ):
                return await message.edit_text(
                    text=text,
                    *args,
                    **kwargs,
                )

            try:
                if (
                    message.from_user.id
                    in list(
                        _supersu
                    )
                    or OWNER_ID
                ):
                    return await message.reply(
                        text=text,
                        *args,
                        **kwargs,
                    )
                    with suppress(
                        Exception
                    ):
                        await _try_purged(
                            message
                        )
                else:
                    return await message.edit_text(
                        text=text,
                        *args,
                        **kwargs,
                    )
            except BaseException:
                await message.reply(
                    text=text,
                    *args,
                    **kwargs,
                )
                with suppress(
                    Exception
                ):
                    await _try_purged(
                        message
                    )
                return

    except (
        MessageTooLong
    ):
        for line in text:
            if (
                len(
                    chunk
                )
                + len(
                    line
                )
                > 4096
            ):
                chunks.append(
                    chunk
                )
                chunk = (
                    ""
                )
            chunk += line
        chunks.append(
            chunk
        )
        try:
            for (
                chunk
            ) in chunks:
                try:
                    a = await message.reply(
                        text=str(
                            chunk
                        ),
                        reply_to_message_id=replied(
                            message
                        ),
                        *args,
                        **kwargs,
                    )
                except MessageTooLong:
                    for line1 in chunk1:
                        if (
                            len(
                                chunk1
                            )
                            + len(
                                line1
                            )
                            > 4096
                        ):
                            chunks1.append(
                                chunk1
                            )
                            chunk1 = ""
                        chunk1 += line1
                    chunks1.append(
                        chunk1
                    )
                    try:
                        for chunk1 in chunks1:
                            b = await message.reply(
                                text=str(
                                    chunk1
                                ),
                                reply_to_message_id=replied(
                                    message
                                ),
                                *args,
                                **kwargs,
                            )
                    except BaseException as excp:
                        return await message.edit_text(
                            text=f"Error: {excp}",
                            *args,
                            **kwargs,
                        )
                    else:
                        with suppress(
                            Exception
                        ):
                            await _try_purged(
                                message
                            )
                        return b
        except (
            BaseException
        ) as excp:
            return await message.edit_text(
                text=f"Error: {excp}",
                *args,
                **kwargs,
            )

        else:
            with suppress(
                Exception
            ):
                await _try_purged(
                    message
                )
            return a


def get_text(
    message: Message,
    save_link: Optional[
        bool
    ] = None,
    get_phone: Optional[
        bool
    ] = None,
    normal: Optional[
        bool
    ] = None,
) -> Optional[str]:
    if (
        message.reply_to_message
    ):
        text_ = (
            message.reply_to_message.text
            or message.reply_to_message.caption
            or message.reply_to_message.caption_entities
        )
    else:
        text_ = (
            message.text.split(
                None, 1
            )[
                1
            ]
            if len(
                message.command,
            )
            != 1
            else None
        )

    if text_ is None:
        return False
    else:
        if get_phone:
            # find phone number
            numb = findall(
                "\\+?[1-9][0-9]{7,14}",
                str(
                    text_
                ),
            )
            for (
                n
            ) in numb:
                if not n:
                    return False
                if not n.startswith(
                    "+"
                ):
                    return f"+{int(n)}"
                else:
                    return str(
                        n
                    )

        elif save_link:
            # find link
            link = findall(
                "http[s]?://(?:[ a-zA-Z]|[0-9]|[$-_@.&+]|(?: %[0-9a-fA-F][0-9a-fA-F]))+",
                text_,
            )
            for (
                x
            ) in link:
                if x:
                    return str(
                        x
                    )
                else:
                    return False
        else:
            if normal:
                return (
                    text_
                )
            return str(
                text_.lower()
            )


def replied(
    message: Message,
):
    reply_id = None

    if (
        message.reply_to_message
    ):
        reply_id = (
            message.reply_to_message.id
        )

    elif (
        message.sender_chat
    ):
        reply_id = (
            message.id
        )

    return reply_id


def attr_file(
    message: Message,
):
    if message.media:
        for (
            message_type
        ) in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "contact",
            "dice",
            "poll",
            "location",
            "venue",
            "sticker",
        ):
            obj = getattr(
                message,
                message_type,
            )
            if obj:
                setattr(
                    obj,
                    "message_type",
                    message_type,
                )
                return (
                    obj
                )


async def extract_userid(
    client,
    message,
    text: str,
):
    def is_int(
        text: str,
    ):
        try:
            int(text)
        except (
            ValueError
        ):
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = (
        message.entities
    )
    if len(entities) < 2:
        try:
            users = (
                await client.get_users(
                    text
                )
            ).id
            return users
        except (
            BaseException
        ):
            text = (
                "-100"
                + text
            )
            try:
                peer = await client.resolve_peer(
                    int(
                        text
                    )
                )
            except BaseException:
                return (
                    False
                )

            if isinstance(
                peer,
                (
                    InputPeerChat,
                ),
            ):
                users = (
                    peer.chat_id
                )
                return (
                    users
                )
            if isinstance(
                peer,
                (
                    InputPeerChannel,
                ),
            ):
                users = (
                    peer.channel_id
                )
                return (
                    users
                )

    entity = entities[1]
    if (
        entity.type
        == MessageEntityType.MENTION
    ):
        return (
            await client.get_users(
                text
            )
        ).id
    if (
        entity.type
        == MessageEntityType.TEXT_MENTION
    ):
        return (
            entity.user.id
        )
    return False


async def user_and_reason(
    client,
    message,
    sender_chat=False,
) -> Any:
    args, text = (
        message.text.strip().split(),
        message.text,
    )
    user, reason = (
        None,
        None,
    )
    if (
        message.reply_to_message
    ):
        reply = (
            message.reply_to_message
        )
        # reply to a message and no reason
        if (
            not reply.from_user
        ):
            if (
                reply.sender_chat
                and reply.sender_chat
                != message.chat.id
                and sender_chat
            ):
                id_ = (
                    reply.sender_chat.id
                )
            else:
                return (
                    False,
                    False,
                )
        else:
            id_ = (
                reply.from_user.id
            )

        if (
            len(args)
            != 2
        ):
            reason = None
        else:
            reason = text.split(
                None, 1
            )[
                1
            ]
        return (
            id_,
            reason,
        )

    # not reply and not reason
    if len(args) == 2:
        user = (
            text.split(
                None, 1
            )[1]
        )
        return (
            await extract_userid(
                client,
                message,
                user,
            ),
            None,
        )

    # not reply and reason
    if len(args) > 2:
        (
            user,
            reason,
        ) = text.split(
            None, 2
        )[
            1:
        ]
        return (
            await extract_userid(
                client,
                message,
                user,
            ),
            reason,
        )

    return user, reason


async def extract_user(
    client, message
) -> Any:
    return (
        await user_and_reason(
            client,
            message,
        )
    )[0]


def get_chat_ids(
    ct: Optional[str],
):
    if ct.startswith(
        "100"
    ) or ct.startswith(
        "-100"
    ):
        return ct
    elif (
        ct.startswith(
            "https://t.me/"
        )
        or ct.startswith(
            "t.me/"
        )
        or ct.startswith(
            "@"
        )
    ):
        if "@" in ct:
            return str(
                ct
            )
        elif "/c/" in ct:
            ct = search(
                r"/c/(.*)/",
                ct,
            ) or search(
                r"/c/(.*)",
                ct,
            )
            return (
                "-100"
                + ct.group(
                    1
                )
            )
        elif (
            "t.me/" in ct
        ):
            ct = search(
                r"t.me/(.*)/",
                ct,
            ) or search(
                r"t.me/(.*)",
                ct,
            )
            return (
                "@"
                + ct.group(
                    1
                )
            )
    else:
        return False


def get_args(
    message: Message,
) -> Optional[str]:
    msg = message.text
    msg = (
        msg.replace(
            " ", "", 1
        )
        if msg[1] == " "
        else msg
    )
    split = (
        msg[1:]
        .replace(
            "\n", " \n"
        )
        .split(" ")
    )
    if (
        " ".join(
            split[1:]
        ).strip()
        == ""
    ):
        return ""
    return " ".join(
        split[1:]
    )
