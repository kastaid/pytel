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
    ChatSendMediaForbidden,
    ChatSendInlineForbidden,)
from pyrogram.raw import functions
from pyrogram.raw.all import layer
from pyrogram.raw.functions import (
    Ping,
    PingDelayDisconnect,)
from pytelibs import (
    _chpytel,
    _supersu,
    GCAST_BLACKLIST,
    GUCAST_BLACKLIST,
    _GCAST_LOCKED,
    _GUCAST_LOCKED,
    _GBAN_LOCKED,
    _UNGBAN_LOCKED,
    LOCK_TYPES,)
from validators.ip_address import (
    ipv4 as is_ipv4,)
from validators.url import url as is_url
from pytel import pytel, pytel_tgb, pytl
from .. import __license__, start_time
from ..client import (
    Instagram,
    TikTok,
    Pinterest,
    ChatGPT,
    Assistant,
    AstGenerate,
    plugins_helper,
    time_formatter,
    user_and_reason,
    extract_user,
    plugins_button,
    unpack_inline,
    _try_purged,
    eor,
    get_text,
    replied,
    LE,
    fetch_adzan,
    fetch_weather,
    fetch_dns,
    fetch_ipinfo,
    mention_html,
    mention_markdown,
    get_chat_ids,
    get_spamwatch_banned,
    get_cas_banned,
    get_blacklisted,
    random_prefixies,
    screenshots,
    tz,
    int2date,
    buttons,
    ikmarkup,
    attr_file,
    RunningCommand,
    humanboolean,
    legally_required,
    subs_like_view_format,
    channel_groups,
    short_dict,
    size_bytes,
    pydb,)
from ..config import (
    PREFIX as px,
    TimeZone,
    LOGCHAT_ID,
    OWNER_ID,)
from ..logger import pylog as send_log
