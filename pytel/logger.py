# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

try:
    from datetime import (
        date,)
    from logging import (
        CRITICAL, DEBUG,
        ERROR, WARNING,
        Handler,
        LogRecord,
        __file__,
        basicConfig,
        currentframe,
        disable,
        getLogger,)
    from sys import (
        stderr,)
    from typing import (
        Union,)
    from loguru import (
        logger as pylog,)
except KeyboardInterrupt:
    print(
        "Fie Logger Received interrupt while import"
    )
except Exception as excp:
    print(
        f"ERROR: {excp}"
    )

pylog.remove(0)
pylog.add(
    sink="logs/pytel-{}.log".format(
        date.today().strftime(
            "%Y-%m-%d"
        )
    ),
    format="{time:YY/MM/DD HH:mm:ss} | {level: <8}| {name: ^15} | {function: ^15} | {line: >3} : {message}",
    rotation="1 days",
    backtrace=True,
    diagnose=True,
)
pylog.add(
    stderr,
    format="<b><magenta>{time:YY/MM/DD HH:mm:ss}</magenta></b> | <u><b><green>{level}</green></b></u> | <b><cyan>{name}:{function}:{line}</cyan></b> | <b><white>{message}</white></b>",
    level="INFO",
    colorize=True,
)
pylog.opt(
    lazy=True,
    colors=True,
)


class InterceptHandler(
    Handler
):
    """
    param record: record to logs.
    """

    def emit(
        self,
        record: LogRecord,
    ) -> None:
        try:
            level: Union[
                str,
                int,
            ] = pylog.level(
                record.levelname
            ).name
        except (
            ValueError
        ):
            level = (
                record.levelno
            )
        (
            frame,
            depth,
        ) = (
            currentframe(),
            2,
        )
        while (
            frame
            and frame.f_code.co_filename
            == __file__
        ):
            frame = frame.f_back  # type: ignore
            depth += 1
        pylog.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(
            level,
            record.getMessage(),
        )


disable(DEBUG)
getLogger(
    "asyncio"
).setLevel(ERROR)
getLogger(
    "pyrogram"
).setLevel(ERROR)
getLogger(
    "pyrogram.client"
).setLevel(WARNING)
getLogger(
    "instagrapi"
).setLevel(ERROR)
getLogger(
    "pyrogram.session.auth"
).setLevel(CRITICAL)
getLogger(
    "pyrogram.session.session"
).setLevel(CRITICAL)
getLogger(
    "urllib3"
).disabled = True
getLogger(
    "pytgcalls"
).disabled = True
getLogger(
    "urllib3.connectionpool"
).disabled = True
getLogger(
    "io"
).disabled = True
pylog.disable(
    "instagrapi"
)
pylog.disable(
    "pytgcalls"
)
pylog.disable(
    "pyrogram.dispatcher"
)
pylog.disable(
    "pyrogram.connection"
)
pylog.disable(
    "pyrogram.raw.types.BadMsgNotification"
)
pylog.disable(
    "asyncio.base_events"
)

basicConfig(
    handlers=[
        InterceptHandler()
    ],
    level=0,
    force=True,
)
