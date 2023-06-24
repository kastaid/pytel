# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from contextlib import suppress
from ..config import LOGCHAT_ID
from ..logger import pylog as send_log
from .dbase import add_logger, check_logger


async def auto_pilots(_):
    user = await _.get_me()
    user_id = user.id
    with suppress(BaseException):
        logger_data = check_logger(user_id=user_id, use_cache=False)
        logger_id = logger_data
    if not LOGCHAT_ID and not logger_id:
        try:
            group_name = "KASTA ID ( LOGGER )"
            group = await _.create_supergroup(group_name)
            logger_id = group.id
            description = "DON'T DELETE THIS GROUP !!\n\nUser ID : {}\nGroup ID : {}\n\nOur Channel: @kastaid".format(
                user_id, logger_id
            )
            await _.set_chat_description(logger_id, description=description)
            pics = "resources/kastaid/kasta_logger.jpg"
            await _.set_chat_photo(logger_id, photo=pics)
            await sleep(0.8)
            add_logger(user_id=user_id, logger_id=logger_id)
        except BaseException as excp:
            send_log.error(excp)

    else:
        add_logger(user_id=user_id, logger_id=LOGCHAT_ID)
        return None

    return logger_id
