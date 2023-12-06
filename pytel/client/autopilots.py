# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from sys import exit
from pyrogram.errors.exceptions.bad_request_400 import (
    BotMethodInvalid,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,)
from pyrogram.types import (
    ChatPrivileges,)
from ..config import (
    LOGCHAT_ID,)
from ..logger import (
    pylog as send_log,)
from .dbase.dbLogger import (
    add_logger,
    already_logger,)


async def auto_pilots(
    _, tgb
) -> None:
    if tgb.me.is_bot:
        b_username = (
            tgb.me.username
        )
    user_id = _.me.id
    if (
        LOGCHAT_ID
        or already_logger(
            user_id
        )
    ):
        return

    if _.me.username:
        name = (
            _.me.username
        )
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
        name = (
            first_name
            + last_name
        )
    send_log.info(
        f"Creating a channel LOGGER for {name}"
    )
    try:
        channel_name = "PYTEL 🇮🇩 ( LOGGER )"
        channel = await _.create_channel(
            channel_name
        )
        logger_id: int = (
            channel.id
        )
        await sleep(2)
        await _.promote_chat_member(
            int(
                logger_id
            ),
            b_username,
            privileges=(
                ChatPrivileges(
                    can_post_messages=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_manage_video_chats=True,
                    can_change_info=True,
                    can_promote_members=True,
                    can_edit_messages=True,
                    can_invite_users=True,
                )
            ),
        )
        description = "⚠️ DON'T DELETE THIS CHANNEL !!⚠️\n\nUser ID : {}\nChannel ID : {}\n\nPYTEL Channel: t.me/PYTELPremium\nPowered by: @kastaid".format(
            user_id,
            int(
                logger_id
            ),
        )
        await sleep(1)
        await _.set_chat_description(
            int(
                logger_id
            ),
            description=description,
        )
        pics = "resources/kastaid/pytel_logger.jpg"
        await sleep(1)
        await _.set_chat_photo(
            int(
                logger_id
            ),
            photo=pics,
        )
        await sleep(0.8)
        add_logger(
            user_id=user_id,
            logger_id=logger_id,
        )
    except (
        FloodWait
    ) as flood:
        await sleep(
            flood.value
            + 5
        )
    except (
        ConnectionError
    ):
        await _.connect()
    except (
        BotMethodInvalid
    ):
        pass
    except KeyError:
        pass
    except (
        BaseException
    ) as excp:
        send_log.error(
            f"USER: {name}\nERROR: {excp}"
        )
        exit(1)
    send_log.success(
        "Success for creating a channel."
    )
