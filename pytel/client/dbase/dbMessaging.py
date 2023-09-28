# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from functools import lru_cache
from ._BaseClient import pydb


@lru_cache
def get_schedule():
    return (
        pydb.get_key("SCHEDULE") or {}
    )


@lru_cache
def get_dspam():
    return (
        pydb.get_key("DELAYSPAM") or {}
    )


def check_schedule(user, chat):
    c = get_schedule()
    if c.get(int(user)):
        a = c[int(user)]["chat"]
        if chat in list(a):
            return True
        return False
    return False


def check_dspam(user, chat):
    c = get_dspam()
    if c.get(int(user)):
        a = c[int(user)]["chat"]
        if chat in list(a):
            return True
        return False
    return False


def add_schedule(user, chat):
    sch = get_schedule()
    if sch.get(int(user)):
        sch[int(user)]["chat"].append(
            chat
        )
    else:
        sch.update(
            {
                int(user): {
                    "chat": [chat]
                }
            }
        )
    pydb.set_key("SCHEDULE", sch)


def cancel_schedule(user, chat):
    sch = get_schedule()
    if (
        sch.get(int(user))
        and sch[int(user)]["chat"]
    ):
        sch[int(user)]["chat"].remove(
            chat
        )
        return pydb.set_key(
            "SCHEDULE", sch
        )


def clear_all_schedule(user):
    sch = get_schedule()
    if sch.get(int(user)):
        sch.pop(int(user))
        return pydb.set_key(
            "SCHEDULE", sch
        )


def add_dspam(user, chat):
    sch = get_dspam()
    if sch.get(int(user)):
        sch[int(user)]["chat"].append(
            chat
        )
    else:
        sch.update(
            {
                int(user): {
                    "chat": [chat]
                }
            }
        )
    pydb.set_key("DELAYSPAM", sch)


def cancel_dspam(user, chat):
    sch = get_dspam()
    if (
        sch.get(int(user))
        and sch[int(user)]["chat"]
    ):
        sch[int(user)]["chat"].remove(
            chat
        )
        return pydb.set_key(
            "DELAYSPAM", sch
        )


def clear_all_dspam(user):
    sch = get_dspam()
    if sch.get(int(user)):
        sch.pop(int(user))
        return pydb.set_key(
            "DELAYSPAM", sch
        )
