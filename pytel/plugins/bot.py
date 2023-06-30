# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from datetime import datetime
from platform import python_version, uname
from textwrap import indent
from time import time, perf_counter
import packaging
from git import __version__ as git_ver
from pip import __version__ as pipver
from pyrogram import __version__
from pytgcalls import __version__ as pytgver
from version import __version__ as b_ver
from . import (
    px,
    pytel,
    plugins_helper,
    time_formatter,
    start_time,
    __license__,
    ParseMode,
    tz,
    Ping,
    layer,
    eor,
    _try_purged,
)


@pytel.instruction("ping", outgoing=True)
async def ping(client, message):
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


@pytel.instruction(["alive", "on"], outgoing=True)
async def alive(client, message):
    LAYER = layer
    my_uptime = time_formatter((time() - start_time) * 1000)
    unam = uname()
    time_stamp = datetime.now(tz).strftime("%A, %I:%M:%S %p UTC%z")
    text_active = "<i>“We are connected on the inside.”</i>\n"
    text_active += "----------------------------------------\n"
    text_active += "› <code>Pip:</code> <code>" + str(pipver) + "</code> \n"
    text_active += "› <code>Git:</code> <code>" + str(git_ver) + "</code> \n"
    text_active += "› <code>Python:</code> <code>" + str(python_version()) + "</code> \n"
    text_active += "› <code>Packaging:</code> <code>" + str(packaging.__version__) + "</code> \n"
    text_active += "› <code>Pyrogram:</code> <code>" + str(__version__) + "</code> \n"
    text_active += "› <code>Telegram Layers:</code> <code>" + str(LAYER) + "</code> \n"
    text_active += "› <code>Pytgcalls:</code> <code>" + str(pytgver) + "</code> \n"
    text_active += (
        "› <code>Pytel Version:</code> <code>" + str(b_ver) + "</code> \n----------------------------------------\n"
    )
    text_active += "› <code>OS:</code> <code>" + unam.system + "</code> \n"
    text_active += "› <code>Machine:</code> <code>" + unam.machine + "</code> \n"
    text_active += "› <code>Date:</code> <code>" + time_stamp + "</code> \n"
    text_active += (
        "› <code>Uptime:</code> <code>" + str(my_uptime) + "</code> \n----------------------------------------\n"
    )
    text_active += "<b>Powered by</b> " + "<b><a href='https://is.gd/ZDEShm'>KASTA ID 🇮🇩</a></b>\n"
    text_active += (
        "<b>Licensed under</b>\n"
        + "<b><a href='https://opensource.org/license/agpl-v3/>'>"
        + str(__license__)
        + "</a></b>\n"
    )
    wrp = indent(text_active, " ", lambda line: True)
    await message.reply(
        text=wrp,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    return await _try_purged(message, 3)


plugins_helper["bot"] = {
    f"{px}ping": "Check how long it takes to ping.",
    f"{px}alive / {px}on": "Check alive & version.",
}
