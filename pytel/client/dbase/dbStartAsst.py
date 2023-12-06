# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from functools import (
    lru_cache,)
from ._BaseClient import (
    pydb,)


@lru_cache
def get_users():
    return (
        pydb.get_key(
            "STARTUSER"
        )
        or []
    )


def added_users(
    user: int,
):
    x = get_users()
    x.append(user)
    return pydb.set_key(
        "STARTUSER", x
    )


def checks_users(
    user: int,
):
    x = get_users()
    if user in x:
        return True
