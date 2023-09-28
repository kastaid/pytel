# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from cachetools import func
from ._BaseClient import pydb


@func.lru_cache
def get_users():
    return (
        pydb.get_key("STARTUSER") or []
    )


@func.lru_cache
def added_users(user: int):
    x = get_users()
    x.append(user)
    return pydb.set_key("STARTUSER", x)


@func.lru_cache
def checks_users(user: int):
    x = get_users()
    if user in x:
        return True
