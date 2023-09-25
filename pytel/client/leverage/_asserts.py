# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import sleep
from contextlib import suppress
from inspect import getfullargspec
from re import findall, search
from typing import Optional, Union, Any
from pyrogram.enums import (
    MessageEntityType,)
from pyrogram.types import Message


async def _try_purged(
    message,
    timer: Union[int, float] = None,
):
    with suppress(BaseException):
        if timer:
            await sleep(timer)
            await message.delete()
        else:
            await message.delete()


async def eor(
    message: Message,
    **kwargs,
) -> Message:
    functions = (
        (
            message.edit_text
            if message.from_user.is_self
            else message.reply
        )
        if message.from_user
        else message.reply
    )
    insc = getfullargspec(
        functions.__wrapped__
    ).args
    return await functions(
        **{
            _: value
            for _, value in kwargs.items()
            if _ in insc
        }
    )


def get_text(
    message: Message,
    save_link: Optional[bool] = None,
    get_phone: Optional[bool] = None,
    normal: Optional[bool] = None,
) -> Optional[str]:
    if message.reply_to_message:
        text_ = (
            message.reply_to_message.text
            or message.reply_to_message.caption
            or message.reply_to_message.caption_entities
        )
    else:
        text_ = (
            message.text.split(None, 1)[
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
                str(text_),
            )
            for n in numb:
                if not n:
                    return False
                if not n.startswith(
                    "+"
                ):
                    return f"+{int(n)}"
                else:
                    return str(n)

        elif save_link:
            # find link
            link = findall(
                "http[s]?://(?:[ a-zA-Z]|[0-9]|[$-_@.&+]|(?: %[0-9a-fA-F][0-9a-fA-F]))+",
                text_,
            )
            for x in link:
                if x:
                    return str(x)
                else:
                    return False
        else:
            if normal:
                return text_
            return str(text_.lower())


def replied(
    message: Message,
):
    reply_id = None

    if message.reply_to_message:
        reply_id = (
            message.reply_to_message.id
        )

    elif message.sender_chat:
        reply_id = message.id

    return reply_id


def attr_file(
    message: Message,
):
    if message.media:
        for message_type in (
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
                return obj


async def extract_userid(
    client, message, text: str
):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    if len(entities) < 2:
        return (
            await client.get_users(text)
        ).id
    entity = entities[1]
    if (
        entity.type
        == MessageEntityType.MENTION
    ):
        return (
            await client.get_users(text)
        ).id
    if (
        entity.type
        == MessageEntityType.TEXT_MENTION
    ):
        return entity.user.id
    return None


async def user_and_reason(
    client, message, sender_chat=False
) -> Any:
    args, text = (
        message.text.strip().split(),
        message.text,
    )
    user, reason = None, None
    if message.reply_to_message:
        reply = message.reply_to_message
        # reply to a message and no reason
        if not reply.from_user:
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
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) != 2:
            reason = None
        else:
            reason = text.split(
                None, 1
            )[1]
        return id_, reason

    # not reply and not reason
    if len(args) == 2:
        user = text.split(None, 1)[1]
        return (
            await extract_userid(
                client, message, user
            ),
            None,
        )

    # not reply and reason
    if len(args) > 2:
        user, reason = text.split(
            None, 2
        )[1:]
        return (
            await extract_userid(
                client, message, user
            ),
            reason,
        )

    return user, reason


async def extract_user(
    client, message
) -> Any:
    return (
        await user_and_reason(
            client, message
        )
    )[0]


def get_chat_ids(ct: Optional[str]):
    if ct.startswith(
        "100"
    ) or ct.startswith("-100"):
        return ct
    elif (
        ct.startswith("https://t.me/")
        or ct.startswith("t.me/")
        or ct.startswith("@")
    ):
        if "@" in ct:
            return str(ct)
        elif "/c/" in ct:
            ct = search(
                r"/c/(.*)/", ct
            ) or search(r"/c/(.*)", ct)
            return "-100" + ct.group(1)
        elif "t.me/" in ct:
            ct = search(
                r"t.me/(.*)/", ct
            ) or search(
                r"t.me/(.*)", ct
            )
            return "@" + ct.group(1)
    else:
        return False


def get_args(
    message: Message,
) -> Optional[str]:
    msg = message.text
    msg = (
        msg.replace(" ", "", 1)
        if msg[1] == " "
        else msg
    )
    split = (
        msg[1:]
        .replace("\n", " \n")
        .split(" ")
    )
    if (
        " ".join(split[1:]).strip()
        == ""
    ):
        return ""
    return " ".join(split[1:])
