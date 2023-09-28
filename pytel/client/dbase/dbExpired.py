# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from datetime import datetime, timedelta
from time import perf_counter
from typing import Optional, Any
from asyncache import cached
from cachetools import TTLCache, func
from ..utils import tz
from ._BaseClient import pydb


@cached(
    TTLCache(
        maxsize=1024,
        ttl=60,
        timer=perf_counter,
    )
)  # 60 seconds
async def countdown_to_datetime(
    expired: Any,
) -> Optional[str]:
    days = expired.days
    seconds = expired.seconds
    hours = int(seconds / 3600)
    minutes = int(
        (seconds - hours * 3600) / 60
    )
    seconds = (
        seconds
        - hours * 3600
        - minutes * 60
    )

    result = str(days) + (
        " Day, "
        if days == 1
        else " Days, "
    )
    result += str(hours) + (
        " Hour, "
        if hours == 1
        else " Hours, "
    )
    result += str(minutes) + (
        " Minute, "
        if minutes == 1
        else " Minutes, "
    )
    result += str(seconds) + (
        " Second."
        if seconds == 1
        else " Seconds."
    )

    return str(result)


@func.lru_cache
def user_expired():
    return pydb.get_key("EXP_DT") or {}


@func.lru_cache
def set_expired_days(
    user_id: Optional[int],
    duration,
):
    days_in_month = 1
    if duration <= 12:
        days_in_month = 30 * duration

    expire_date = datetime.now(
        tz
    ).replace(microsecond=0).replace(
        tzinfo=None
    ) + timedelta(
        days=days_in_month
    )
    exp = user_expired()
    exp.update(
        {user_id: str(expire_date)}
    )
    return pydb.set_key(
        "EXP_DT",
        exp,
    )


@cached(
    TTLCache(
        maxsize=1024,
        ttl=60,
        timer=perf_counter,
    )
)  # 60 seconds
async def get_expired_date(
    user_id,
) -> str:
    exp = pydb.get_key("EXP_DT")
    if exp:
        xx = user_expired().get(
            int(user_id)
        )
        if xx is None:
            return (
                None,
                None,
            )

        yy = datetime.strptime(
            str(xx),
            "%Y-%m-%d %H:%M:%S",
        )
        expired = yy - datetime.now(
            tz
        ).replace(tzinfo=None)
        return (
            yy,
            await countdown_to_datetime(
                expired
            ),
        )
    return None, None


@func.lru_cache
def rem_expired(
    user_id,
):
    exp = user_expired()
    if exp.get(user_id):
        del exp[int(user_id)]
        return pydb.set_key(
            "EXP_DT",
            exp,
        )
