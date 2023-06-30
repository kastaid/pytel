# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import sleep
from contextlib import suppress
from inspect import getfullargspec
from typing import Union
from pyrogram.types import Message


async def _try_purged(message, timer: Union[int, float]):
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
        (message.edit_text if message.from_user.is_self else message.reply) if message.from_user else message.reply
    )
    insc = getfullargspec(functions.__wrapped__).args
    return await functions(**{_: value for _, value in kwargs.items() if _ in insc})
