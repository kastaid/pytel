# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import Lock
from datetime import datetime
from os import getpid, close, execvp
from platform import (
    python_version,
    uname,)
from sys import executable
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
    CallbackQuery,)
from speedtest import Speedtest
from version import __version__ as b_ver
from . import (
    GH_PAT,
    ChatSendMediaForbidden,
    ChatSendInlineForbidden,
    BotResponseTimeout,
    QueryIdInvalid,
    RunningCommand,
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
    ikmarkup,
    filters,
    size_bytes,
    suppress,)

lock = Lock()


async def _er_iping(
    client,
) -> Optional[str]:
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
    text = f"""
<b><u>PYROGRAM</b></u>
 ├ <b>Speed:</b> <code>{pings_} ms</code>
 └ <b>Delay:</b> <code>{delay_ping} ms</code>

(c) @kastaid #pytel
"""
    return str(text)


def _ialive() -> Optional[str]:
    LAYER = layer
    my_uptime = time_formatter(
        (time() - start_time) * 1000
    )
    unam = uname()
    time_stamp = datetime.now(
        tz
    ).strftime("%A, %I:%M:%S %p UTC%z")
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
        "› <code>Pytel:</code> <code>"
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
        text_active,
        " ",
        lambda line: True,
    )
    return str(wrp)


def sys_stats():
    cpu = psutil.cpu_percent()
    mem = (
        psutil.virtual_memory().percent
    )
    disk = psutil.disk_usage(
        "/"
    ).percent
    process = psutil.Process(getpid())
    stats = f"""
PYTEL-Premium ( Client )
-----------------------
UPTIME: {time_formatter((time() - start_time) * 1000)}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
-----------------------

Copyright (C) 2023-present kastaid
"""
    return stats


@pytel.instruction(
    ["speedtest", "speed"],
    outgoing=True,
)
async def _speedtest_net(
    client, message
):
    x = await eor(
        message,
        text="<i>Initializing Speedtest...</i>",
    )
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = result["share"]
    string_speed = f"""
➲ <b><i>SPEEDTEST INFO</i></b>
┠ <b>Upload:</b> <code>{size_bytes(result['upload'] / 8)}/s</code>
┠ <b>Download:</b>  <code>{size_bytes(result['download'] / 8)}/s</code>
┠ <b>Ping:</b> <code>{result['ping']} ms</code>
┠ <b>Time:</b> <code>{result['timestamp']}</code>
┠ <b>Data Sent:</b> <code>{size_bytes(int(result['bytes_sent']))}</code>
┖ <b>Data Received:</b> <code>{size_bytes(int(result['bytes_received']))}</code>

➲ <b><i>SPEEDTEST SERVER</i></b>
┠ <b>Name:</b> <code>{result['server']['name']}</code>
┠ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
┠ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
┠ <b>Latency:</b> <code>{result['server']['latency']}</code>
┠ <b>Latitude:</b> <code>{result['server']['lat']}</code>
┖ <b>Longitude:</b> <code>{result['server']['lon']}</code>

➲ <b><i>CLIENT DETAILS</i></b>
┠ <b>IP Address:</b> <code>{result['client']['ip']}</code>
┠ <b>Latitude:</b> <code>{result['client']['lat']}</code>
┠ <b>Longitude:</b> <code>{result['client']['lon']}</code>
┠ <b>Country:</b> <code>{result['client']['country']}</code>
┠ <b>ISP:</b> <code>{result['client']['isp']}</code>
┖ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
"""
    try:
        await client.send_photo(
            message.chat.id,
            photo=path,
            caption=string_speed,
        )
        return await _try_purged(x, 1.5)
    except ChatSendMediaForbidden:
        await client.send_message(
            message.chat.id,
            text=string_speed,
        )
        return await _try_purged(x, 1.5)


@pytel.instruction(
    ["ping", "pong"],
    supersu=["PYTEL"],
    force_edit=False,
    supergroups=True,
    disable_errors=True,
)
@pytel.instruction(
    ["ping", "pong"],
    outgoing=True,
    force_edit=False,
    supergroups=True,
    disable_errors=True,
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
                try:
                    await message.reply_inline_bot_result(
                        _.query_id,
                        name.id,
                    )
                except ChatSendInlineForbidden:
                    txt = (
                        await _er_iping(
                            client
                        )
                    )
                    await client.send_message(
                        message.chat.id,
                        text=txt,
                        disable_web_page_preview=True,
                    )
        except BotResponseTimeout:
            await message.reply(
                "Did not answer the request, please try again.",
            )
        return await _try_purged(
            message
        )


@pytel.instruction(
    ["alive", "on"],
    supersu=["PYTEL"],
    force_edit=False,
    supergroups=True,
    disable_errors=True,
)
@pytel.instruction(
    ["alive", "on"],
    outgoing=True,
    force_edit=False,
    supergroups=True,
    disable_errors=True,
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
                try:
                    await message.reply_inline_bot_result(
                        _.query_id,
                        name.id,
                    )
                except ChatSendInlineForbidden:
                    text = _ialive()
                    await client.send_message(
                        message.chat.id,
                        text=text,
                        disable_web_page_preview=True,
                    )
        except BotResponseTimeout:
            await message.reply(
                text="Did not answer the request, please try again.",
            )
            return
        return await _try_purged(
            message
        )


@pytel_tgb.on_callback_query(
    filters.regex("sys_stats")
)
async def _sys_callback(
    client,
    cq: CallbackQuery,
):
    text = sys_stats()
    await pytel_tgb.answer_callback_query(
        cq.id,
        text,
        show_alert=True,
    )


@pytel_tgb.on_inline_query(
    filters.regex("^ping")
)
async def _ping_inline(
    client,
    cq: CallbackQuery,
):
    txt = await _er_iping(client)
    rpm = [
        [
            buttons(
                "ꜱᴛᴀᴛꜱ",
                callback_data="sys_stats",
            )
        ],
    ]
    with suppress(QueryIdInvalid):
        await client.answer_inline_query(
            cq.id,
            is_personal=True,
            results=[
                (
                    InlineQueryResultArticle(
                        title="PING\n@kastaid #pytel",
                        reply_markup=ikmarkup(
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
    client,
    cq: CallbackQuery,
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
        ],
        [
            buttons(
                "REPOSITORY",
                url="https://github.com/kastaid/pytel",
            ),
        ],
    ]
    with suppress(QueryIdInvalid):
        await client.answer_inline_query(
            cq.id,
            is_personal=True,
            results=[
                (
                    InlineQueryResultArticle(
                        title="ALIVE\n@kastaid #pytel",
                        reply_markup=ikmarkup(
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


async def restarting(
    message,
) -> None:
    try:
        import psutil

        proc = psutil.Process(getpid())
        for _ in (
            proc.open_files()
            + proc.connections()
        ):
            close(_.fd)
    except BaseException:
        pass
    await _try_purged(message)
    execvp(
        executable,
        [
            executable,
            "-m",
            "pytel",
        ],
    )


@pytel.instruction(
    ["update"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["update"],
    outgoing=True,
)
async def _updates(client, message):
    if lock.locked():
        await message.edit(
            "Please wait until --**updating**-- done."
        )

    async with lock:
        x = await message.reply(
            "Getting information up to date..."
        )
        (
            stdout,
            stderr,
        ) = RunningCommand(
            f"git pull https://{GH_PAT}@github.com/kastaid/pytel"
        )
        if (
            "Already up to date."
            in str(stdout)
        ):
            text = "It's already up-to date!"
            await eor(
                x,
                text=text,
            )
            return

        elif (
            "From https://github.com/kastaid/pytel"
            in str(stderr)
        ):
            await client.lock.acquire()
            yy = await eor(
                x,
                text=f"<u><b>Updating</u>!!</b>\nInstall requirements...",
            )
            with suppress(
                BaseException
            ):
                RunningCommand(
                    "pip3 install -U -r main.txt"
                )
            client.lock.release()
            xy = await eor(
                yy,
                text=f"Update successfuly.\nRestarting, wait for 1 minutes.",
            )
            await restarting(xy)
            return

        else:
            await eor(
                x,
                text="Sorry, I can't update.",
            )
            return


@pytel.instruction(
    ["restart"],
    outgoing=True,
)
async def _restart(client, message):
    x = await message.reply(
        "Restarting client, wait for 1 minutes.."
    )
    await restarting(x)


@pytel.instruction(
    [
        "repository",
        "repo",
    ],
    outgoing=True,
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
    f"{random_prefixies(px)}speed": "To check speed networking.",
    f"{random_prefixies(px)}expired / {random_prefixies(px)}status": "To check status expired.",
    f"{random_prefixies(px)}alive / {random_prefixies(px)}on": "Check alive & version.",
    f"{random_prefixies(px)}ping / {random_prefixies(px)}pong": "Check how long it takes to ping.",
    f"{random_prefixies(px)}update": "To update ur source.",
    f"{random_prefixies(px)}restart": "To restart ur bot.",
    f"{random_prefixies(px)}repo": "To see source code.",
}
