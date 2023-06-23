# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from time import time
from . import (
    Client,
    Message,
    px,
    filters,
    pytel,
    plugins_helper,
)


@pytel.instruction(filters.command("ping", px) & filters.me)
async def ping(client: Client, message: Message):
    start_t = time()
    r = await message.reply("...")
    end_t = time()
    time_taken_s = (end_t - start_t) * 1000
    await r.edit(f"Pong!\n{time_taken_s:.3f} ms")


plugins_helper["bot"] = {
    "{px}": "Check how long it takes to ping.",
}
