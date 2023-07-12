# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from typing import Optional
from ._BaseClient import pydb


def get_antipm():
    return pydb.get_key("ANTIPM") or {}


def get_pmreport():
    return pydb.get_key("PMREPORT") or {}


def get_pmblock():
    return pydb.get_key("PMBLOCK") or {}


def set_antipm(
    user_id: Optional[int],
    status: Optional[str],
):
    apm = get_antipm()
    apm.update({user_id: status})
    return pydb.set_key("ANTIPM", apm)


def get_antipm_status(
    user_id: Optional[int],
):
    apm = get_antipm()
    if user_id in apm.keys():
        return apm[user_id]


def set_pmreport(
    user_id: Optional[int],
    status: Optional[str],
):
    apm = get_pmreport()
    apm.update({user_id: status})
    return pydb.set_key("PMREPORT", apm)


def get_pmreport_status(
    user_id: Optional[int],
):
    apm = get_pmreport()
    if user_id in apm.keys():
        return apm[user_id]


def set_pmblock(
    user_id: Optional[int],
    status: Optional[str],
):
    apm = get_pmblock()
    apm.update({user_id: status})
    return pydb.set_key("PMBLOCK", apm)


def get_pmblock_status(
    user_id: Optional[int],
):
    apm = get_pmblock()
    if user_id in apm.keys():
        return apm[user_id]
