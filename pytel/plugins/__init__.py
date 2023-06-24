# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from pyrogram.enums import ParseMode
from pyrogram.raw.all import layer
from pyrogram.raw.functions import Ping
from .. import (
    start_time,
    pytel,
    pytel_tgb,
    __license__,
)
from ..client import plugins_helper, time_formatter
from ..config import PREFIX as px
from ..logger import pylog as send_log

DEVS = None
