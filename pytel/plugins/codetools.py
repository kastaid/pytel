# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from cryptography.fernet import Fernet
from pybase64 import (
    b64encode,
    b64decode,)
from . import (
    Rooters,
    eor,
    converting_binnary,
    plugins_helper,
    px,
    pytel,
    suppress,
    _try_purged,
    replied,
    get_text,
    random_prefixies,
    scanner_code,
    making_code,)

_CODE_TEXT = """
**{}**

**--INPUT:--**
```sh
{}
```

**--OUTPUT:--**
```sh
{}
```
"""


@pytel.instruction(
    ["cryptography", "cryp"],
    outgoing=True,
    sensitive=False,
)
async def _cryptography_fernet(
    client, message
):
    str_data = get_text(
        message, normal=True
    )
    if not str_data:
        await eor(
            message,
            text="Give it something to to convert data into data cryptography.",
        )
    x = await eor(
        message,
        text="Processing...",
    )
    message = str_data
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(
        message.encode()
    )
    decMessage = fernet.decrypt(
        encMessage
    ).decode()
    text = f"""
<b><u>Cryptography</u></b> ( <u>FERNET</u> ) <u>AES-128</u>

<b>Key:</b> <code>{key.decode()}</code>

<b>Encrypt:</b> <code>{encMessage.decode()}</code>

<b>Decrypt:</b> <code>{decMessage}</code>

(c) kastaid #pytel
"""
    await eor(x, text=text)


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
        try:
            lething = str(
                b64encode(
                    bytes(
                        str_data,
                        "utf-8",
                    )
                )
            )[2:]
        except BaseException as excp:
            await eor(
                x,
                text=f"{excp}",
            )
            return

    elif message.command[0] == "decode":
        criteria = "Base64 Decode"
        try:
            lething = str(
                b64decode(
                    bytes(
                        str_data,
                        "utf-8",
                    ),
                    validate=True,
                ),
            )[2:]
        except BaseException as excp:
            await eor(
                x,
                text=f"{excp}",
            )
            return

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
        binnary = converting_binnary(
            data=str_data, convert=True
        )

    elif (
        message.command[0]
        == "unbinnary"
    ):
        criteria = "Binnary to Text"
        binnary = converting_binnary(
            data=str_data, convert=False
        )

    if binnary:
        await eor(
            x,
            text=_CODE_TEXT.format(
                criteria,
                str_data,
                str(binnary),
            ),
        )
        return


@pytel.instruction(
    [
        "mqr",
        "makeqr",
        "smqr",
        "smakeqr",
        "pmqr",
        "pmakeqr",
    ],
    outgoing=True,
    sensitive=False,
)
async def _making_qrcode(
    client, message
):
    str_data = get_text(
        message, normal=True
    )
    if not str_data:
        await eor(
            message,
            text="Give it something to turn into making qrcode.",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )

    if message.command[0][0] == "s":
        output = making_code(
            client, str_data, "webp"
        )
        with suppress(Exception):
            await client.send_sticker(
                message.chat.id,
                sticker=output,
                protect_content=True,
                reply_to_message_id=replied(
                    message
                ),
            )
            await _try_purged(x)
            (Rooters / output).unlink(
                missing_ok=True
            )
            return

    elif message.command[0][0] == "p":
        output = making_code(
            client, str_data, "png"
        )
        with suppress(Exception):
            await client.send_photo(
                message.chat.id,
                photo=output,
                protect_content=True,
                reply_to_message_id=replied(
                    message
                ),
            )
            await _try_purged(x)
            (Rooters / output).unlink(
                missing_ok=True
            )
            return

    else:
        output = making_code(
            client, str_data, "png"
        )
        with suppress(Exception):
            await client.send_photo(
                message.chat.id,
                photo=output,
                protect_content=True,
                reply_to_message_id=replied(
                    message
                ),
            )
            await _try_purged(x)
            (Rooters / output).unlink(
                missing_ok=True
            )
            return


@pytel.instruction(
    [
        "scancode",
        "scode",
    ],
    outgoing=True,
    sensitive=False,
)
async def _scanning_code(
    client, message
):
    rep = message.reply_to_message
    if not rep:
        await eor(
            message,
            text="Please reply to Sticker/Images for Scanning Barcode/QR Code.",
        )
        return

    type_file = ""
    y = await eor(
        message,
        text="Checking...",
    )
    if rep.photo:
        type_file = "images"
        file = (
            await client.download_media(
                rep.photo, "cache/"
            )
        )
    elif (
        rep.sticker
        and rep.sticker.file_id
    ):
        type_file = "sticker"
        file = (
            await client.download_media(
                rep.sticker.file_id,
                "cache/",
            )
        )
    else:
        await eor(
            y,
            text="Please reply to Sticker/Images for Scanning Barcode/QR Code.",
        )
        return

    x = await eor(
        y,
        text="Scanning...",
    )
    data = await scanner_code(
        files=file,
        type_file=type_file,
    )
    if data:
        await client.send_message(
            message.chat.id,
            text=data,
            reply_to_message_id=replied(
                message
            ),
            disable_web_page_preview=True,
        )
        (Rooters / file).unlink(
            missing_ok=True
        )
        await _try_purged(x, 1.5)
        return
    else:
        await eor(
            x,
            text="Can't scanning, try again later!",
        )
        (Rooters / file).unlink(
            missing_ok=True
        )


plugins_helper["codetools"] = {
    f"{random_prefixies(px)}cryp / cryptography [text/reply to msg]": "Cryptography provides symmetric encryption and authentication to data. (Fernet) AES-128",
    f"{random_prefixies(px)}encode [text/reply to msg]": "Base64 Transform data that can be used by various systems precisely and safely.",
    f"{random_prefixies(px)}decode [data code]": "Base64 Translate or read the contents of the code.",
    f"{random_prefixies(px)}binnary [text/reply to msg]": "Converts text or messages into a binary number.",
    f"{random_prefixies(px)}unbinnary [binnary numbers]": "Converts binary numbers into a message / text.",
    f"{random_prefixies(px)}[s/p]makeqr [data/text/reply to msg]": "To create a barcode according to your data. Option: (s: sticker | p: photo | default: be photo)",
    f"{random_prefixies(px)}scancode / scode [reply to barcode/qrcode: sticker/images]": "To Scanning Barcode/QR Code.",
}
