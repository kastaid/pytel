# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pybase64 import (
    b64encode,
    b64decode,)
from . import (
    eor,
    plugins_helper,
    px,
    pytel,
    get_text,
    random_prefixies,)

_B64 = """
<b>{}</b>

<b><u>INPUT:</b></u>
<code>{}</code>

<b><u>OUTPUT:</b></u>
<code>{}</code>
"""


@pytel.instruction(
    [
        "encode",
        "decode",
    ],
    outgoing=True,
    sensitive=False,
)
async def _base64_en_de(
    client, message
):
    str_data = get_text(
        message, normal=True
    )
    if not str_data:
        await eor(
            message,
            text="Give it something to turn into code.",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    if message.command[0] == "encode":
        lething = str(
            b64encode(
                bytes(str_data, "utf-8")
            )
        )[2:]
        await eor(
            x,
            text=_B64.format(
                "Encode",
                str_data,
                str(lething[:-1]),
            ),
        )
        return

    elif message.command[0] == "decode":
        lething = str(
            b64decode(
                bytes(
                    str_data, "utf-8"
                ),
                validate=True,
            ),
        )[2:]
        await eor(
            x,
            text=_B64.format(
                "Decode",
                str_data,
                str(lething[:-1]),
            ),
        )
        return


plugins_helper["base64"] = {
    f"{random_prefixies(px)}encode [data]": "Transform data that can be used by various systems precisely and safely.",
    f"{random_prefixies(px)}decode [data]": "Translate or read the contents of the code.",
}
