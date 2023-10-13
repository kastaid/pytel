# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

import shlex
import sys
from os import close, getpid, execvp, system
from subprocess import run
from pytelibs import __version__
from requests import get
from .logger import pylog as send_log


def commands(
    cmd: str,
):
    try:
        proc = run(
            shlex.split(cmd),
            shell=False,
            check=True,
        )
        if proc.returncode != 0:
            send_log.error(
                f"Exit code {proc.returncode}"
            )
            sys.exit(1)
        else:
            return proc.stdout
    except BaseException:
        sys.exit(1)


def _restart():
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

    execvp(
        sys.executable,
        [
            sys.executable,
            "-m",
            "pytel",
        ],
    )


def check_pypi_version():
    try:
        response = get(
            f"https://pypi.org/pypi/pytelibs/json"
        ).json()
        latest_version = response[
            "info"
        ]["version"]

        if (
            __version__
            != latest_version
        ):
            send_log.info(
                f"New pytelibs pypi version: {latest_version} (current: {__version__})"
            )
            send_log.info(
                "Pulling..."
            )
            commands(
                cmd="git pull"
            )
            send_log.info(
                "Installing..."
            )
            commands(
                cmd="pip3 install -U pytelibs"
            )
            send_log.success(
                f"pytelibs v{latest_version} has been installed."
            )
            system("clear")
            send_log.info(
                "Restarting..."
            )
            _restart()

    except Exception as e:
        send_log.error(
            f"Failed to check pytelibs pypi version: {e}"
        )
        sys.exit(1)
