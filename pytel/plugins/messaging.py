# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    _try_purged,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
)


@pytel.instruction(
    ["del", "delete"], outgoing=True
)
async def _tiktok(client, message):
    replieds = message.reply_to_message
    if replieds:
        await _try_purged(replieds)
        await _try_purged(message, 0.7)
        return
    else:
        await _try_purged(message)


plugins_helper["messaging"] = {
    f"{random_prefixies(px)}del [reply message]": "To delete message.",
}
