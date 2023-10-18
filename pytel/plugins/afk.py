# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from random import choice
from ..client.dbase.dbAFK import (
    add_afk,
    user_afk,
    rem_afk,)
from . import (
    OUT_AFK,
    client_afk,
    eor,
    filters,
    plugins_helper,
    px,
    pydb,
    pytel,
    random_prefixies,
    _try_purged,)

_AFK_ON_NO_REASON = """
{} is <b><u>AFK</u>!</b>
<b>Since:</b> {}
"""

_AFK_ON_REASON = """
{} is <b><u>AFK</u>!</b>
<b>Reason:</b> {}
<b>Since:</b> {}
"""

_AFK_OUT_NO_REASON = """
{} </b><b><u>{}</u></b>
<b>Since:</b> {}
"""

_AFK_OUT_REASON = """
{} <b><u>{}</u></b>
<b>Reason:</b> {}
<b>Since:</b> {}
"""


@pytel.instruction(
    [
        "afk",
        "brb",
    ],
    outgoing=True,
)
async def _set_client_afk(
    client, message
):
    return await ClientAFK(
        client, message
    )


@pytel.instruction(
    filt=client_afk
    & (
        filters.mentioned
        | filters.private
    )
    & ~filters.me
    & ~filters.bot
    & filters.incoming
)
async def _afk_ongoing(client, message):
    if not (pydb.get_key("AFK")):
        return
    if not message:
        return
    for x in client._client:
        try:
            user: int = x.me.id
        except BaseException:
            return
        if not user_afk(int(user)):
            return
        return await OngoingAFK(
            client, message
        )


@pytel.instruction(
    filt=client_afk
    & filters.outgoing
    & filters.me
    & ~filters.mentioned
)
async def _afk_outgoing(
    client, message
):
    if not (pydb.get_key("AFK")):
        return
    if not message:
        return
    if any(
        _
        in (
            message.text
            or message.caption
            or ""
        ).lower()
        for _ in ["afk", "brb"]
    ):
        return
    for x in client._client:
        try:
            user: int = x.me.id
        except BaseException:
            return
        if not user_afk(int(user)):
            return
        return await OutgoingAFK(
            client, message
        )


async def OngoingAFK(client, message):
    for x in client._client:
        try:
            user = x.me.id
        except BaseException:
            return
        if message.sender_chat:
            return
        if not message.from_user:
            return
        if message.from_user.id == user:
            return

        (
            get_reason,
            afk_since,
        ) = user_afk(int(user))

        name = (
            await client.user_fullname(
                user
            )
        )
        if get_reason == "N/A":
            await message.reply_text(
                _AFK_ON_NO_REASON.format(
                    name,
                    afk_since,
                ),
            )
            return
        else:
            await message.reply_text(
                _AFK_ON_REASON.format(
                    name,
                    get_reason,
                    afk_since,
                ),
            )
            return


async def OutgoingAFK(client, message):
    try:
        user: int = client.me.id
    except BaseException:
        return
    else:
        (
            get_reason,
            afk_since,
        ) = user_afk(int(user))
        name = (
            await client.user_fullname(
                user
            )
        )
        if get_reason == "N/A":
            await message.reply_text(
                _AFK_OUT_NO_REASON.format(
                    name,
                    choice(OUT_AFK),
                    afk_since,
                ),
            )
            rem_afk(int(user))
            return
        else:
            await message.reply_text(
                _AFK_OUT_REASON.format(
                    name,
                    choice(OUT_AFK),
                    get_reason,
                    afk_since,
                ),
            )
            rem_afk(int(user))
            return


async def ClientAFK(client, message):
    user: int = client.me.id
    name = await client.user_fullname(
        user
    )
    get_reason = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not get_reason:
        reason = "N/A"
    else:
        reason = get_reason

    await eor(
        message,
        text=f"{name} stepped <b><u>AFK</u>!</b>",
    )
    await _try_purged(message, 4.5)
    add_afk(int(user), str(reason))


plugins_helper["afk"] = {
    f"{random_prefixies(px)}afk / brb [reason/not]": "AFK means away from keyboard.\nAfter this is activated, if someone tags or messages you, he/she would get an automated reply.",
}
