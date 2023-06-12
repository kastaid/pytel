# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from datetime import date
from logging import (
    Handler,
    __file__,
    CRITICAL,
    ERROR,
    DEBUG,
    WARNING,
    disable,
    getLogger,
    Logger,
    basicConfig,
)
from sys import _getframe, stderr
from typing import Optional
from loguru import logger as pylog

pylog.remove(0)
pylog.add(
    "logs/client-{}.log".format(date.today().strftime("%Y-%m-%d")),
    format="{time:YY/MM/DD HH:mm:ss} | {level: <8} | {name: ^15} | {function: ^15} | {line: >3} : {message}",
    rotation="1 days",
)
pylog.add(
    stderr,
    format="{time:YY/MM/DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    level="INFO",
    colorize=False,
)
pylog.opt(lazy=True, colors=False)


class InterceptHandler(Handler):
    def emit(self, record):
        try:
            level = pylog.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = (
            _getframe(6),
            6,
        )  # pylint: disable=W0212
        while frame and frame.f_code.co_filename == __file__:
            frame = frame.f_back
            depth += 1
        pylog.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


disable(DEBUG)
getLogger("asyncio").setLevel(ERROR)
getLogger("pyrogram").setLevel(WARNING)
getLogger("pyrogram.client").setLevel(WARNING)
getLogger("pyrogram.session.auth").setLevel(CRITICAL)
getLogger("pyrogram.session.session").setLevel(CRITICAL)

getLogger("urllib3").disabled = True
getLogger("urllib3.connectionpool").disabled = True
getLogger("io").disabled = True
basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def LOG(name: Optional[str]) -> Logger:
    return getLogger(name)
