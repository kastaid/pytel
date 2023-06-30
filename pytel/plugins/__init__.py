# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from contextlib import suppress
from pyrogram.enums import ParseMode
from pyrogram.raw.all import layer
from pyrogram.raw.functions import Ping
from pytel import pytel, pytel_tgb
from .. import start_time, __license__
from ..client import plugins_helper, time_formatter
from ..client.leverage import eor, _try_purged
from ..client.utils import developer, tz, LE
from ..config import PREFIX as px, TimeZone
