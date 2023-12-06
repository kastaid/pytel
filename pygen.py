# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

import os
from platform import (
    uname,)
from sys import exit
from time import sleep
from version import (
    __version__,)

APP_VERSION = (
    f"PYTEL-v.{__version__}"
)
DEVICE_MODEL = f"{uname().machine}"
SYSTEM_VERSION = f"{uname().system}"
WORKERS = min(
    32,
    (os.cpu_count() or 0) + 4,
)


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

_STRING_TEXT = """
<b>PYTEL</b> <u>PYROGRAM SESSION</u>

<b>API ID:</b> <code>{}</code>

<b>API HASH:</b> <code>{}</code>

<b>STRING:</b>
<code>{}</code>

(c) @kastaid #pytel - @PYTELPremiumBot
"""


def loading():
    print(
        "Checking if Pyrogram is installed...\n"
    )
    for _ in range(3):
        for frame in r"-\|/-\|/":
            print(
                "\b",
                frame,
                sep="",
                end="",
                flush=True,
            )
            sleep(0.1)


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        # Windows
        os.system("cls")


def get_api_id_and_hash():
    print(
        "Get your API ID and API HASH from my.telegram.org\n\n",
    )
    try:
        API_ID = int(
            input(
                "Please enter your API ID: "
            )
        )
    except ValueError:
        print(
            "APP ID must be an integer.\nQuitting..."
        )
        exit(0)
    API_HASH = input(
        "Please enter your API HASH: "
    )
    return (
        API_ID,
        API_HASH,
    )


def session():
    try:
        loading()
        from pyrogram import (
            Client,)

        x = "\bFound an existing installation of Pyrogram...\nSuccessfully Imported.\n\n"
    except BaseException:
        print(
            "\nInstalling Pyrogram..."
        )
        os.system(
            "pip install pyrogram tgcrypto"
        )
        x = "\bDone. Installed and imported Pyrogram."
        from pyrogram import (
            Client,)

    clear_screen()
    print(PYTEL)
    print(x)

    # generate a session
    (
        API_ID,
        API_HASH,
    ) = get_api_id_and_hash()
    print(
        "Enter phone number when asked.\n\n"
    )
    try:
        with Client(
            name="pytel",
            api_id=API_ID,
            api_hash=API_HASH,
            workers=WORKERS,
            app_version=APP_VERSION,
            device_model=DEVICE_MODEL,
            system_version=SYSTEM_VERSION,
            in_memory=True,
        ) as pytel:
            ss = (
                pytel.export_session_string()
            )
            pytel.send_message(
                "me",
                _STRING_TEXT.format(
                    API_ID,
                    API_HASH,
                    ss,
                ),
            )
            print(
                "Session has been sent to your saved messages!"
            )
            exit(0)
    except Exception as excp:
        print(
            "Unexpected error occurred while creating session, make sure to validate your inputs."
        )
        print(excp)


def main():
    clear_screen()
    print(PYTEL)
    try:
        type_of_ss = str(
            input(
                "\npytel using pyrogram session.\n\nDo you want to generate?\n\nEnter choice (Y/n) :  "
            )
        )
    except Exception as excp:
        print(excp)
        exit(0)
    if type_of_ss.lower() in [
        "y",
        "yes",
    ]:
        session()
    elif type_of_ss.lower() in [
        "n",
        "no",
    ]:
        exit(0)
    else:
        print("Invalid choice.")
    x = input("Run again? (Y/n)")
    if x.lower() in [
        "y",
        "yes",
    ]:
        main()
    else:
        exit(0)


main()
