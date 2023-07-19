# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from contextlib import suppress
from os import getpid
from random import randrange
from pyrogram import __version__
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,)
from pyrogram.raw.all import layer
from version import __version__ as versi
from ..config import (
    PRODUCTION_MODE,
    PREFIX,
    LOGCHAT_ID,)
from .dbase.dbLogger import (
    already_logger,
    check_logger,)


async def running_message(self, p):
    if PRODUCTION_MODE:
        return
    if self not in self._client:
        self._client.append(self)

    user_id = self.me.id
    if (
        already_logger(user_id=user_id)
        and not LOGCHAT_ID
    ):
        log_data = check_logger().get(
            user_id
        )
        log_id = log_data[0]
        send_to = int(log_id)
    elif LOGCHAT_ID:
        send_to = int(LOGCHAT_ID)
    else:
        send_to = None
    await sleep(randrange(2, 4))
    with suppress(MessageIdInvalid):
        text = """
<b><u>PYTEL</b></u> is up and running!
├ <b>PID :</b>  <i>{}</i>
├ <b>PYTEL :</b>  <i>{}</i>
├ <b>Layer :</b>  <i>{}</i>
├ <b>Pyrogram :</b>  <i>{}</i>
└ <b>Prefix :</b> <code>{}</code>

(c) @kastaid #pytel
""".format(
            getpid(),
            versi,
            layer,
            __version__,
            "".join(PREFIX),
        )
        if send_to:
            await p.send_message(
                int(send_to),
                text=text,
                parse_mode=ParseMode.HTML,
                disable_notification=False,
            )
