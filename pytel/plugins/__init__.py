"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from contextlib import suppress
from time import time
from pyrogram import filters
from pyrogram.enums import (
    ParseMode,
    ChatType,)
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageNotModified,
    BotResponseTimeout,
    QueryIdInvalid,
    UsersTooMuch,
    BotsTooMuch,
    UserNotParticipant,
    UserNotMutualContact,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,
    SlowmodeWait,)
from pyrogram.errors.exceptions.forbidden_403 import (
    ChatSendMediaForbidden,
    ChatSendInlineForbidden,
    ChatSendStickersForbidden,
    UserPrivacyRestricted,)
from pyrogram.errors.exceptions.not_acceptable_406 import (
    ChannelPrivate,
    UserRestricted,)
from pyrogram.raw import functions
from pyrogram.raw.all import layer
from pyrogram.raw.functions import (
    Ping,
    PingDelayDisconnect,)
from pytelibs import (
    _chpytel,
    _supersu,
    OUT_AFK,
    DEFAULT_SHELL_BLACKLISTED,
    GCAST_BLACKLIST,
    GUCAST_BLACKLIST,
    _GCAST_LOCKED,
    _GUCAST_LOCKED,
    _GBAN_LOCKED,
    _UNGBAN_LOCKED,
    _INVITED_LOCKED,
    _KICKED_LOCKED,
    _HELP_LOCK,
    _HELP_ACCEPT,
    SETMODE_ONLINE,
    SETMODE_OFFLINE,
    LOCK_TYPES,
    crypto_format,
    converting_binnary,
    normalize_youtube_url,
    is_youtube_url,
    replace_all,)
from validators.ip_address import (
    ipv4 as is_ipv4,)
from validators.url import url as is_url
from pytel import pytel, pytel_tgb, pytl
from .. import (
    __license__,
    start_time,
    Rooters,)
from ..client import (
    Instagram,
    TikTok,
    Pinterest,
    ChatGPT,
    Assistant,
    AstGenerate,
    Memify,
    plugins_helper,
    time_formatter,
    user_and_reason,
    extract_user,
    progress,
    plugins_button,
    unpack_inline,
    _try_purged,
    eor,
    get_text,
    get_args,
    replied,
    resize_images,
    resize_media,
    LE,
    fetch_adzan,
    fetch_crypto,
    fetch_weather,
    fetch_dns,
    fetch_github,
    fetch_ipinfo,
    fetch_phonenumbers,
    mentioned,
    get_chat_ids,
    get_spamwatch_banned,
    get_cas_banned,
    get_blacklisted,
    get_random_hex,
    get_youtube_info,
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
    short_dict,
    size_bytes,
    pydb,
    making_code,
    scanner_code,
    quotlymaker,)
from ..client.leverage import (
    client_afk,
    client_antipm,)
from ..config import (
    PREFIX as px,
    TimeZone,
    LOGCHAT_ID,
    OWNER_ID,
    RAPID_KEY,)
from ..logger import pylog as send_log
