"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from contextlib import suppress
from pyrogram import filters
from pyrogram.enums import (
    ParseMode,
    ChatType,)
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageNotModified,
    BotResponseTimeout,
    QueryIdInvalid,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,)
from pyrogram.errors.exceptions.forbidden_403 import (
    ChatSendInlineForbidden,)
from pyrogram.raw import functions
from pyrogram.raw.all import layer
from pyrogram.raw.functions import (
    Ping,
    PingDelayDisconnect,)
from pytelibs import (
    _chpytel,
    developer,
    GCAST_BLACKLIST,)
from validators.url import url as is_url
from pytel import pytel, pytel_tgb, pytl
from .. import __license__, start_time
from ..client import (
    plugins_helper,
    time_formatter,
    plugins_button,
    unpack_inline,
    _try_purged,
    eor,
    get_text,
    replied,
    LE,
    fetch_adzan,
    fetch_weather,
    mention_html,
    mention_markdown,
    get_blacklisted,
    random_prefixies,
    screenshots,
    tz,
    buttons,
    ikmarkup,
    attr_file,
    RunningCommand,
    humanboolean,
    legally_required,
    channel_groups,
    pydb,)
from ..config import (
    PREFIX as px,
    TimeZone,
    LOGCHAT_ID,
    OWNER_ID,)
from ..logger import pylog as send_log
