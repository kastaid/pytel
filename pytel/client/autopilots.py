# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from ..logger import pylog as send_log
from .dbase import users_db, set_group


async def auto_pilots(_):
    user = await _.get_me()
    user_id = user.id
    logger_data = await users_db.users.find_one({"user_id": user_id})
    logger_id = None

    if logger_data:
        logger_id = logger_data.get("LOGCHAT_ID")

    if not logger_data or not logger_id:
        try:
            group_name = "KASTA ID ( LOGGER )"
            group_description = "DON'T DELETE THIS GROUP !!\n\nOur Channel: @kastaid"
            group = await _.create_supergroup(group_name, group_description)
            logger_id = group.id
            pics = "resources/kastaid/kasta_logger.jpg"
            await _.set_chat_photo(logger_id, photo=pics)
            await sleep(0.5)
            await set_group(user_id, logger_id)
            await sleep(2)
            await users_db.users.update_one(
                {"user_id": user_id},
                {"$set": {"LOGCHAT_ID": logger_id}},
                upsert=True,
            )
        except BaseException as excp:
            send_log.warning(excp)
    if logger_id is None:
        return None

    return int(logger_id)
