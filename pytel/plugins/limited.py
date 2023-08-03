# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from pyrogram.raw.functions.messages import (
    DeleteHistory,
    StartBot,)
from . import (
    eor,
    plugins_helper,
    px,
    pytel,
    random_prefixies,)


@pytel.instruction(
    [
        "limit",
        "limited",
    ],
    outgoing=True,
)
async def _limited(client, message):
    spambot = "@SpamBot"
    await client.unblock_user(spambot)
    x = await eor(
        message,
        text="Getting information...",
    )
    history = await client.resolve_peer(
        spambot
    )
    resp = await client.invoke(
        StartBot(
            bot=history,
            peer=history,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1.6)
    status = await client.get_messages(
        spambot,
        resp.updates[1].message.id + 1,
    )
    await eor(
        x,
        text=f"`{status.text}`",
    )
    await client.invoke(
        DeleteHistory(
            peer=history,
            max_id=0,
            revoke=True,
        )
    )
    return


plugins_helper["limited"] = {
    f"{random_prefixies(px)}limited": "To check ur account is limited or not.",
}
