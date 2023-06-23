# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient as DB
from ...config import MONGO_URI
from ...logger import pylog as send_log

try:
    mongo = DB(MONGO_URI)
    db = mongo.premium
    users_db = db.users
    log_group = db.loggroup
except BaseException as excp:
    send_log.warning(excp)


async def set_group(user_id: Optional[int], logger_id: Optional[int]):
    await log_group.users.update_one(
        {"user_id": user_id},
        {"$set": {"LOGCHAT_ID": logger_id}},
        upsert=True,
    )
