# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from ..config import LOGCHAT_ID
from ..logger import pylog as send_log
from .dbase.dbLogger import (
    add_logger,
    already_logger,
)


async def auto_pilots(_) -> None:
    user_id = _.me.id
    if LOGCHAT_ID or already_logger(
        user_id
    ):
        return

    if _.me.username:
        name = _.me.username
    else:
        first_name = (
            _.me.first_name
            if _.me.first_name
            else "ㅤ"
        )
        last_name = (
            _.me.last_name
            if _.me.last_name
            else "ㅤ"
        )
        name = first_name + last_name
    send_log.info(
        f"Creating a group LOGGER for {name}"
    )
    try:
        group_name = "KASTA ID ( LOGGER )"
        group = await _.create_supergroup(
            group_name
        )
        logger_id = group.id
        description = "DON'T DELETE THIS GROUP !!\n\nUser ID : {}\nGroup ID : {}\n\nOur Channel: @kastaid".format(
            user_id, logger_id
        )
        await _.set_chat_description(
            logger_id,
            description=description,
        )
        pics = "resources/kastaid/kasta_logger.jpg"
        await _.set_chat_photo(
            logger_id, photo=pics
        )
        await sleep(0.8)
        add_logger(
            user_id=user_id,
            logger_id=logger_id,
        )
    except BaseException as excp:
        send_log.error(excp)

    send_log.success(
        "Success for creating a group."
    )
