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
    Rooters,
    eor,
    plugins_helper,
    px,
    pytel,
    suppress,
    _try_purged,
    get_text,
    random_prefixies,)

_CODE_TEXT = """
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
            text="Give it something to turn into base64 code.",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    criteria, lething = None, None
    if message.command[0] == "encode":
        criteria = "Base64 Encode"
        lething = str(
            b64encode(
                bytes(str_data, "utf-8")
            )
        )[2:]

    elif message.command[0] == "decode":
        criteria = "Base64 Decode"
        lething = str(
            b64decode(
                bytes(
                    str_data, "utf-8"
                ),
                validate=True,
            ),
        )[2:]

    if lething and criteria:
        await eor(
            x,
            text=_CODE_TEXT.format(
                criteria,
                str_data,
                str(lething[:-1]),
            ),
        )
        return


@pytel.instruction(
    [
        "binnary",
        "unbinnary",
    ],
    outgoing=True,
    sensitive=False,
)
async def _binnary_code(
    client, message
):
    str_data = get_text(
        message, normal=True
    )
    if not str_data:
        await eor(
            message,
            text="Give it something to turn into binnary code.",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    criteria, binnary = None, None
    if message.command[0] == "binnary":
        criteria = "Text to Binnary"
        binnary = " ".join(
            format(x, "08b")
            for x in bytearray(
                str_data, "utf-8"
            )
        )

    elif (
        message.command[0]
        == "unbinnary"
    ):
        criteria = "Binnary to Text"
        a = "".join(str_data)
        number = a.split()
        binnary = "".join(
            chr(int(binary, 2))
            for binary in number
        )

    if len(binnary) >= 4096:
        files = "cache/binnary.txt"
        with open(files, "w+") as f:
            f.write(binnary)
        with suppress(BaseException):
            caption = f"""
<u><b>{criteria}</u></b>
"""
            await client.send_document(
                message.chat.id,
                document=files,
                caption=caption,
            )
            await _try_purged(x)
            (Rooters / files).unlink(
                missing_ok=True
            )
            return
    else:
        await eor(
            x,
            text=_CODE_TEXT.format(
                criteria,
                str_data,
                str(binnary),
            ),
        )
        return


plugins_helper["codetools"] = {
    f"{random_prefixies(px)}encode [text/reply to msg]": "Base64 Transform data that can be used by various systems precisely and safely.",
    f"{random_prefixies(px)}decode [data code]": "Base64 Translate or read the contents of the code.",
    f"{random_prefixies(px)}binnary [text/reply to msg]": "Converts text or messages into a binary number.",
    f"{random_prefixies(px)}unbinnary [binnary numbers]": "Converts binary numbers into a message / text.",
}
