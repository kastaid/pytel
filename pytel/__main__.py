"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from asyncio import sleep
from contextlib import suppress
from importlib import (
    import_module as import_plugins,)
from pathlib import Path
from sys import exit
from time import time, sleep as sl
from tracemalloc import start
from typing import List, Tuple
from pyrogram.errors.exceptions.bad_request_400 import (
    PersistentTimestampInvalid,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,)
from uvloop import install
from . import (
    __copyright__,
    __license__,
    pytel_tgb,
    pytl,)
from .client import (
    plugins_helper,
    time_formatter,
    Instagram,)
from .client.autopilots import (
    auto_pilots,)
from .client.runmsg import (
    running_message,)
from .logger import pylog as send_log
from .tasks import pytasks

start()

Plugins: Path = Path(__file__).parent


PYTEL = r"""
              _       _
             | |     | |
  _ __  _   _| |_ ___| |
 | '_ \| | | | __/ _ \ |
 | |_) | |_| | ||  __/ |
 | .__/ \__, |\__\___|_|
 | |     __/ |
 |_|    |___/
"""


def sorted_plugins() -> (
    Tuple[List[str], str]
):
    """
    Credits : @illvart
    """
    pytel_path = "plugins/"
    a_plugins = [
        f.stem
        for f in (
            Plugins / pytel_path
        ).rglob("*.py")
        if f.is_file()
        and not str(f).endswith(
            "__init__.py"
        )
    ]
    return sorted(a_plugins)


def load_plugins():
    """
    Credits : @illvart
    """
    send_log.info(
        "Installing plugins..."
    )
    plugins = sorted_plugins()
    loads = time()
    _ = (
        "__init__",
        "__premium",
        "__asstart",
    )
    for plugin in plugins:
        try:
            import_plugins(
                "pytel.plugins."
                + plugin
            )
            if plugin not in _:
                send_log.success(
                    "[✅]" + plugin
                )
                sl(0.5)
        except KeyboardInterrupt:
            send_log.warning(
                "Received interrupt while installing"
            )
        except Exception as excp:
            send_log.exception(
                f"[❌] {plugin} : {excp} "
            )
    loaded_time = time_formatter(
        (time() - loads) * 1000
    )
    loaded_msg = ">> Loaded success!!\nPlugins: {}, Commands: {}\n\n{}\n\n>> Time taken {}".format(
        plugins_helper.count,
        plugins_helper.total,
        "|".join(plugins)
        .replace("|__premium", "")
        .replace("__asstart", ""),
        loaded_time,
    )
    send_log.info(loaded_msg)


async def start_asst():
    send_log.info(
        "Starting-up Assistant."
    )
    try:
        await pytel_tgb.start()
    except FloodWait as flood:
        await sleep(flood.value + 5)
        await pytel_tgb.start()
    except KeyboardInterrupt:
        send_log.warning(
            "Received interrupt while connecting"
        )
    except Exception as excp:
        send_log.exception(excp)
    send_log.success(
        "Successful, Started-On Asisstant."
    )


async def runner():
    await start_asst()
    for _ in pytl:
        try:
            await _.client_started()
            await _.notify_login()
            await auto_pilots(
                _,
                pytel_tgb,
            )
            await sleep(2)
            await running_message(_)
        except KeyboardInterrupt:
            send_log.warning(
                "Received interrupt while connecting"
            )
        except Exception as exc:
            send_log.exception(exc)
    load_plugins()
    await sleep(1.5)
    await _.flash()
    _._copyright(
        _copyright=f"{__copyright__}",
        _license=f"{__license__}",
    )
    await pytasks(
        confirm=True,
        client=pytl,
    )


#    await _.stop()
#    await pytel_tgb.stop()


if __name__ == "__main__":
    print(PYTEL)
    print(__doc__)
    install()
    for x in pytl:
        with suppress(
            PersistentTimestampInvalid,
            TimeoutError,
            ConnectionError,
        ):
            try:
                x.run_in_loop(runner())
            except FloodWait as flood:
                x.send_log.info(flood)
            finally:
                x.send_log.info(
                    "See you next time !",
                )
                Instagram.loged_out(
                    crash=True
                )
                x.loop.stop()
                exit(0)
