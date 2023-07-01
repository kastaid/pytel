# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import sleep
from datetime import datetime
from importlib import import_module as import_plugins
from os import getpid
from pathlib import Path
from sys import exit
from time import time, sleep as sl
from typing import Tuple, List
from pyrogram import __version__, idle
from pyrogram.enums import ParseMode
from pyrogram.raw.all import layer
from uvloop import install
from version import __version__ as versi
from . import (
    __license__,
    __copyright__,
    pytl,
    pytel_tgb,
)
from .client import plugins_helper, time_formatter
from .client.autopilots import auto_pilots
from .client.dbase.dbLogger import already_logger, check_logger
from .client.utils import tz
from .config import PREFIX, LOGCHAT_ID
from .logger import pylog as send_log

Plugins: Path = Path(__file__).parent


async def running_message(self):
    user = await self.get_me()
    user_id = user.id
    if already_logger(user_id=user_id) and not LOGCHAT_ID:
        log_data = check_logger().get(user_id)
        log_id = log_data[0]
        send_to = int(log_id)
    elif LOGCHAT_ID:
        send_to = int(LOGCHAT_ID)
    else:
        send_to = None
    text = """
<b><u>PYTEL</b></u> is up and running!
├ <b>PID :</b>  <i>{}</i>
├ <b>PYTEL :</b>  <i>{}</i>
├ <b>Layer :</b>  <i>{}</i>
├ <b>Pyrogram :</b>  <i>{}</i>
└ <b>Prefix :</b> <code>{}</code>
""".format(
        getpid(),
        versi,
        layer,
        __version__,
        "".join(PREFIX),
    )
    dt = datetime.now(tz)
    await self.send_message(
        int(send_to),
        text=text,
        parse_mode=ParseMode.HTML,
        disable_notification=False,
        schedule_date=dt,
    )


def sorted_plugins() -> Tuple[List[str], str]:
    """
    Credits : @illvart
    """
    pytel_path = "plugins/"
    a_plugins = [
        f.stem for f in (Plugins / pytel_path).rglob("*.py") if f.is_file() and not str(f).endswith("__init__.py")
    ]
    return sorted(a_plugins)


def load_plugins():
    """
    Credits : @illvart
    """
    send_log.info("Installing plugins...")
    plugins = sorted_plugins()
    loads = time()
    _ = ("__init__",)
    for plugin in plugins:
        try:
            import_plugins("pytel.plugins." + plugin)
            if plugin not in _:
                send_log.success("[+]" + plugin)
                sl(0.3)
        except Exception as excp:
            send_log.exception(f"[-] {plugin} : {excp} ")
    loaded_time = time_formatter((time() - loads) * 1000)
    loaded_msg = ">> Loaded plugins: {}, Commands: {}\nTotal {}, Time for {}".format(
        plugins_helper.count,
        plugins_helper.total,
        tuple(plugins),
        loaded_time,
    )
    send_log.info(loaded_msg)


async def runner():
    await pytel_tgb.start()
    send_log.info("Starting-up PYTEL")
    for _ in pytl:
        try:
            await _.start()
            await _.notify_login()
            await auto_pilots(_)
            await sleep(2)
        except Exception as exc:
            send_log.exception(exc)
    load_plugins()
    await sleep(1.5)
    await _.flash()
    _._copyright(_copyright=f"{__copyright__}", _license=f"{__license__}")
    await running_message(_)
    await idle()
    for kz in pytl:
        await kz.stop()


if __name__ == "__main__":
    install()
    for x in pytl:
        try:
            x.run_in_loop(runner())
        except BaseException as excp:
            x.send_log.info(f"{excp}")
        finally:
            x.send_log.info("Goodbye !!!", style="braches")
            x.loop.stop()
            exit(0)
