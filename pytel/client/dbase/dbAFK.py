# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from datetime import datetime
from ..utils import time_formatter
from ._BaseClient import pydb


def get_afk():
    return pydb.get_key("AFK") or {}


def add_afk(user, reason):
    afk = get_afk()
    time = datetime.now().timestamp()
    try:
        afk.update(
            {
                int(user): {
                    "status": [
                        reason,
                        time,
                    ]
                }
            }
        )
    except AttributeError:
        a = {
            int(user): {
                "status": [
                    reason,
                    time,
                ]
            }
        }
        pydb.set_key("AFK", a)


def user_afk(user):
    afk = get_afk()
    if afk.get(int(user)):
        afk_since = time_formatter(
            (
                datetime.now().replace(
                    microsecond=0
                )
                - datetime.fromtimestamp(
                    afk[int(user)][
                        "status"
                    ][1]
                )
            ).seconds
            * 1000
        )
        return (
            afk[int(user)]["status"][0],
            afk_since,
        )
    return False


def rem_afk(user):
    afk = get_afk()
    if afk.get(int(user)):
        afk.pop(int(user))
        return pydb.set_key("AFK", afk)
