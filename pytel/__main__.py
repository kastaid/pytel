"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from asyncio import sleep, gather
from concurrent.futures import (
    ThreadPoolExecutor,)
from contextlib import suppress
from importlib import (
    import_module as import_plugins,)
from multiprocessing import cpu_count
from pathlib import Path
from time import time
from tracemalloc import start
from typing import List, Tuple
from pyrogram.errors.exceptions.bad_request_400 import (
    PersistentTimestampInvalid,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,)
from pyrogram.errors.exceptions.internal_server_error_500 import (
    HistoryGetFailed,)
from uvloop import install
from . import (
    loopers,
    __copyright__,
    __license__,
    pytel_tgb,
    pytel,
    pytl,)
from .client import (
    plugins_helper,
    time_formatter,)
from .client.autopilots import (
    auto_pilots,)
from .client.dbase.dbMessaging import (
    clear_all_schedule,
    clear_all_dspam,)
from .client.runmsg import (
    running_message,)
from .logger import pylog as send_log
from .tasks import pytasks

start()

Plugins: Path = Path(__file__).parent
ThreadLock = ThreadPoolExecutor(
    max_workers=cpu_count() * 1,
    thread_name_prefix="PYTEL",
)

PYTEL = r"""
       !
       ^
      / \
     /___\
    |=   =|                  _       _
    |     |                 | |     | |
    |     |      _ __  _   _| |_ ___| |
    |     |     | '_ \| | | | __/ _ \ |
    |     |     | |_) | |_| | ||  __/ |
    |     |     | .__/ \__, |\__\___|_|
   /|##!##|\    | |     __/ |
  / |##!##| \   |_|    |___/
 /  |##!##|  \
|  / ^ | ^ \  |   [ USERBOT-TELEGRAM ] 🤖
| /  ( | )  \ |    • Multi Client Session. ( User )
|/   ( | )   \|    • ChatGPT. ( OpenAI )
    ((   ))        • Managing Group. ( Telegram )
   ((  :  ))       • Social Media. ( Searching & Downloader )
   ((  :  ))
    ((   ))
     (( ))
      ( )
       .        © Copyright 2023-present kastaid
       .               All Rights Reserved.
       .
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


async def load_plugins() -> None:
    """
    Credits : @illvart
    """
    send_log.info(
        f"🔄 Loading plugins for {len(pytl)} Client"
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
                await sleep(0.5)
        except KeyboardInterrupt:
            send_log.warning(
                "Received interrupt while installing"
            )
        except OSError:
            pass
        except Exception as excp:
            send_log.exception(
                f"[❌] {plugin} : {excp} "
            )
    loaded_time = time_formatter(
        (time() - loads) * 1000
    )
    loaded_msg = ">> Loaded success!! 🔥🔥🔥\n💿 Plugins: {}\n🛠 Commands: {}\n\n{}\n\n>> ⏳ Time taken {}".format(
        plugins_helper.count,
        plugins_helper.total,
        "|".join(plugins)
        .replace("|__premium", "")
        .replace("__asstart", ""),
        loaded_time,
    )
    send_log.info(loaded_msg)


async def start_asst() -> None:
    send_log.info(
        "🛸 Starting-up Assistant."
    )
    try:
        await pytel_tgb.start()
    except OSError:
        try:
            await pytel_tgb.connect()
            await pytel_tgb.start()
        except BaseException:
            pass
    except KeyError:
        pass
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
        "☑️ Successful, Started-On Asisstant."
    )


async def execution() -> None:
    await start_asst()
    for _ in pytl:
        try:
            if _ not in pytel._client:
                pytel._client.append(_)
            if _.loop.is_closed():
                _.loop.new_event_loop()
            else:
                _.loop.create_future()
            await _.client_started()
            await _.notify_login()
            await auto_pilots(
                _,
                pytel_tgb,
            )
            # Cleared
            clear_all_dspam(_.me.id)
            clear_all_schedule(_.me.id)
        except FloodWait as flood:
            await sleep(flood.value + 5)
        except KeyboardInterrupt:
            send_log.warning(
                "Received interrupt while connecting"
            )
        except Exception as excp:
            send_log.exception(excp)

    await load_plugins()
    for x in pytl:
        await gather(
            running_message(x),
            x.flash(),
        )
    await x._copyright(
        _copyright=f"{__copyright__}",
        _license=f"{__license__}",
    )
    await pytasks(
        confirm=True,
        client=pytl,
    )
    ThreadLock.shutdown(wait=False)
    for c in pytl:
        await c.loop.shutdown_asyncgens()
        c.loop.stop()
        await c.stop()
        await pytel_tgb.stop()


if __name__ == "__main__":
    print(PYTEL)
    print(__doc__)
    install()
    with suppress(
        ConnectionError,
        HistoryGetFailed,
        PersistentTimestampInvalid,
        TimeoutError,
    ):
        for x in pytl:
            if x.loop.is_closed():
                x.loop.new_event_loop()
            else:
                x.loop.create_future()
            try:
                if x in pytel._client:
                    loopers.create_future()
                    loopers.run_until_complete(
                        execution()
                    )
            except Exception as excp:
                send_log.exception(excp)
#            finally:
#                loopers.close()
