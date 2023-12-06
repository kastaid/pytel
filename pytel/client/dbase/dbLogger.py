# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from functools import (
    lru_cache,)
from typing import (
    Optional,)
from ._BaseClient import (
    pydb,)


@lru_cache
def check_logger():
    return (
        pydb.get_key(
            "LOGCHAT_ID"
        )
        or {}
    )


def add_logger(
    user_id: Optional[
        int
    ],
    logger_id,
):
    logchat = (
        check_logger()
    )
    if logchat.get(
        user_id
    ):
        if (
            logger_id
            not in logchat[
                user_id
            ]
        ):
            logchat[
                user_id
            ].append(
                logger_id
            )
    else:
        logchat.update(
            {
                user_id: [
                    logger_id
                ]
            }
        )
    return pydb.set_key(
        "LOGCHAT_ID",
        logchat,
    )


def already_logger(
    user_id: Optional[
        int
    ],
):
    logchat = (
        check_logger()
    )
    if logchat.get(
        int(user_id)
    ):
        return logchat[
            int(user_id)
        ]
