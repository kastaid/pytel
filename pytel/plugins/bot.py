# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from datetime import datetime
from platform import python_version, uname
from textwrap import indent
from time import perf_counter, time
import packaging
from git import __version__ as git_ver
from pip import __version__ as pipver
from pyrogram import __version__
from pytgcalls import __version__ as pytgver
from version import __version__ as b_ver
from . import (
    ParseMode,
    Ping,
    __license__,
    _try_purged,
    eor,
    layer,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    start_time,
    time_formatter,
    tz,
)


@pytel.instruction(
    ["ping", "pong"],
    supersu=True,
    disable_errors=True,
)
@pytel.instruction(
    ["ping", "pong"],
    outgoing=True,
    disable_errors=True,
)
async def _ping(client, message):
    start_t = time()
    r = await eor(message, text="...")
    end_t = time()
    time_taken_s = (end_t - start_t) * 1000
    # pyrogram
    times = perf_counter()
    await client.invoke(Ping(ping_id=0))
    pings = round(perf_counter() - times, 3)
    txt = f"""
**Pong!!**
**Server:** `{time_taken_s:.3f} ms`
**Pyrogram:** `{pings} ms`
"""
    await eor(r, text=txt)


@pytel.instruction(
    ["alive", "on"], outgoing=True
)
async def _alive(client, message):
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
    await message.reply(
        text=wrp,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    return await _try_purged(message, 3)


@pytel.instruction(
    ["repository", "repo"], outgoing=True
)
async def _repo(client, message):
    text = "[{}](https://github.com/kastaid/pytel) : source code.".format(
        "Click Here",
    )
    await message.reply(
        message,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_preview=True,
    )
    await _try_purged(message, 1.5)


plugins_helper["bot"] = {
    f"{random_prefixies(px)}alive / {random_prefixies(px)}on": "Check alive & version.",
    f"{random_prefixies(px)}ping": "Check how long it takes to ping.",
    f"{random_prefixies(px)}repo": "To see source code.",
}
