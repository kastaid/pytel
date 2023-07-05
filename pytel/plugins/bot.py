# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import Lock
from datetime import datetime
from os import getpid
from platform import python_version, uname
from textwrap import indent
from time import time
from typing import Optional
import packaging
import psutil
from git import __version__ as git_ver
from pip import __version__ as pipver
from pyrogram import __version__
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    CallbackQuery,
    InlineKeyboardMarkup,
)
from pytgcalls import __version__ as pytgver
from version import __version__ as b_ver
from . import (
    ParseMode,
    Ping,
    PingDelayDisconnect,
    __license__,
    _try_purged,
    eor,
    layer,
    plugins_helper,
    px,
    pytel,
    pytel_tgb,
    random_prefixies,
    start_time,
    time_formatter,
    tz,
    buttons,
    filters,
)

lock = Lock()


def _ialive() -> Optional[str]:
    LAYER = layer
    my_uptime = time_formatter(
        (time() - start_time) * 1000
    )
    unam = uname()
    time_stamp = datetime.now(tz).strftime(
        "%A, %I:%M:%S %p UTC%z"
    )
    text_active = "<i>“We are connected on the inside.”</i>\n"
    text_active += "----------------------------------------\n"
    text_active += (
        "› <code>Pip:</code> <code>"
        + str(pipver)
        + "</code> \n"
    )
    text_active += (
        "› <code>Git:</code> <code>"
        + str(git_ver)
        + "</code> \n"
    )
    text_active += (
        "› <code>Python:</code> <code>"
        + str(python_version())
        + "</code> \n"
    )
    text_active += (
        "› <code>Packaging:</code> <code>"
        + str(packaging.__version__)
        + "</code> \n"
    )
    text_active += (
        "› <code>Pyrogram:</code> <code>"
        + str(__version__)
        + "</code> \n"
    )
    text_active += (
        "› <code>Telegram Layers:</code> <code>"
        + str(LAYER)
        + "</code> \n"
    )
    text_active += (
        "› <code>Pytgcalls:</code> <code>"
        + str(pytgver)
        + "</code> \n"
    )
    text_active += (
        "› <code>Pytel Version:</code> <code>"
        + str(b_ver)
        + "</code> \n----------------------------------------\n"
    )
    text_active += (
        "› <code>OS:</code> <code>"
        + unam.system
        + "</code> \n"
    )
    text_active += (
        "› <code>Machine:</code> <code>"
        + unam.machine
        + "</code> \n"
    )
    text_active += (
        "› <code>Date:</code> <code>"
        + time_stamp
        + "</code> \n"
    )
    text_active += (
        "› <code>Uptime:</code> <code>"
        + str(my_uptime)
        + "</code> \n----------------------------------------\n"
    )
    text_active += (
        "<b>Powered by</b> "
        + "<b><a href='https://is.gd/ZDEShm'>KASTA ID 🇮🇩</a></b>\n"
    )
    text_active += (
        "<b>Licensed under</b>\n"
        + "<b><a href='https://opensource.org/license/agpl-v3/>'>"
        + str(__license__)
        + "</a></b>\n"
    )
    wrp = indent(
        text_active, " ", lambda line: True
    )
    return str(wrp)


def sys_stats():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(getpid())
    stats = f"""
PYTEL
------------------
UPTIME: {time_formatter((time() - start_time) * 1000)}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%

Copyright (C) 2023-present kastaid
"""
    return stats


@pytel.instruction(
    ["ping", "pong"],
    supersu=True,
)
@pytel.instruction(
    ["ping", "pong"],
    outgoing=True,
)
async def _iping(client, message):
    if (
        message.command[0] == "ping"
        or "pong"
    ):
        plugins_n = "ping"
        try:
            _ = await client.get_inline_bot_results(
                pytel_tgb.me.username,
                plugins_n,
            )
            for name in _.results:
                await message.reply_inline_bot_result(
                    _.query_id, name.id
                )
        except Exception as error:
            return await eor(
                message, text=error
            )
        return await _try_purged(message)


@pytel.instruction(
    ["alive", "on"], supersu=True
)
@pytel.instruction(
    ["alive", "on"], outgoing=True
)
async def _ialv(client, message):
    if (
        message.command[0] == "alive"
        or "on"
    ):
        plugins_n = "alive"
        try:
            _ = await client.get_inline_bot_results(
                pytel_tgb.me.username,
                plugins_n,
            )
            for name in _.results:
                await message.reply_inline_bot_result(
                    _.query_id, name.id
                )
        except Exception as error:
            return await eor(
                message, text=error
            )
        return await _try_purged(message)


@pytel_tgb.on_callback_query(
    filters.regex("sys_stats")
)
async def _sys_callback(
    client, cq: CallbackQuery
):
    text = sys_stats()
    await pytel_tgb.answer_callback_query(
        cq.id, text, show_alert=True
    )


@pytel_tgb.on_inline_query(
    filters.regex("^ping")
)
async def _ping_inline(
    client, cq: CallbackQuery
):
    # pyrogram
    await lock.acquire()
    start_pyro = time()
    await client.invoke(
        Ping(ping_id=client.rnd_id())
    )
    lock.release()
    p1 = time()
    pings_ = f"{str(round((start_pyro - p1) * -50, 2))}"
    # delay ping
    await lock.acquire()
    start_delay = time()
    await client.invoke(
        PingDelayDisconnect(
            ping_id=client.rnd_id(),
            disconnect_delay=15,
        )
    )
    lock.release()
    d1 = time()
    delay_ping = f"{str(round((start_delay - d1) * -50, 2))}"
    txt = f"""
<b><u>PYROGRAM</b></u>
 ├ <b>Speed:</b> <code>{pings_} ms</code>
 └ <b>Delay:</b> <code>{delay_ping} ms</code>
"""
    rpm = [
        [
            buttons(
                "ꜱᴛᴀᴛꜱ",
                callback_data="sys_stats",
            )
        ],
    ]
    await client.answer_inline_query(
        cq.id,
        cache_time=600,
        results=[
            (
                InlineQueryResultArticle(
                    title="PING\n@kastaid #pytel",
                    reply_markup=InlineKeyboardMarkup(
                        rpm
                    ),
                    input_message_content=InputTextMessageContent(
                        message_text=txt,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    ),
                )
            )
        ],
    )


@pytel_tgb.on_inline_query(
    filters.regex("^alive")
)
async def _alive_inline(
    client, cq: CallbackQuery
):
    text = _ialive()
    rpm = [
        [
            buttons(
                "KASTA ID 🇮🇩",
                url="https://t.me/kastaid",
            ),
            buttons(
                "KASTA OT",
                url="https://t.me/kastaot",
            ),
            buttons(
                "REPO",
                url="https://github.com/kastaid/pytel",
            ),
        ],
    ]
    await client.answer_inline_query(
        cq.id,
        cache_time=600,
        results=[
            (
                InlineQueryResultArticle(
                    title="ALIVE\n@kastaid #pytel",
                    reply_markup=InlineKeyboardMarkup(
                        rpm
                    ),
                    input_message_content=InputTextMessageContent(
                        message_text=text,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    ),
                )
            )
        ],
    )


@pytel.instruction(
    ["repository", "repo"], outgoing=True
)
async def _repo(client, message):
    text = "[{}](https://github.com/kastaid/pytel) : source code.".format(
        "Click Here",
    )
    await message.reply(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
    )
    await _try_purged(message, 1.5)


plugins_helper["bot"] = {
    f"{random_prefixies(px)}alive / {random_prefixies(px)}on": "Check alive & version.",
    f"{random_prefixies(px)}ping / {random_prefixies(px)}pong": "Check how long it takes to ping.",
    f"{random_prefixies(px)}repo": "To see source code.",
}
