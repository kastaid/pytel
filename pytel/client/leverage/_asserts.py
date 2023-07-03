# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import sleep
from contextlib import suppress
from inspect import getfullargspec
from typing import Optional, Union
from pyrogram.types import Message


async def _try_purged(
    message, timer: Union[int, float] = None
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
) -> Optional[str]:
    text_ = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text_ = (
            message.reply_to_message.text
            or message.reply_to_message.caption
        )

    if text_ is None:
        return False
    else:
        if save_link:
            return str(text_)
        else:
            return str(text_.lower())


def replied(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = (
            message.reply_to_message.id
        )

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id
