# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from datetime import datetime, timedelta
from typing import Optional
from ._BaseClient import pydb


def user_expired():
    return pydb.get_key("EXP_DT") or {}


def set_expired_days(
    user_id: Optional[int],
    duration,
):
    days_in_month = 1
    if duration <= 12:
        days_in_month = 30 * duration
    expire_date = (
        datetime.now().replace(
            microsecond=0
        )
        + timedelta(days=days_in_month)
    )
    exp = user_expired()
    exp.update(
        {user_id: str(expire_date)}
    )
    return pydb.set_key(
        "EXP_DT",
        exp,
    )


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
        expired = yy - datetime.now()
        formatext = f"{expired.days}d {expired.seconds//3600}h {(expired.seconds//60)%60}m"
        return yy, str(formatext)
    return None


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
