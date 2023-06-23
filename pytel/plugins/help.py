# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    Client,
    Message,
    px,
    pytel,
    plugins_helper,
    filters,
)


@pytel.instruction(filters.command("help", px) & filters.me)
async def _help(client: Client, message: Message):
    await message.edit("Tester")


plugins_helper["help"] = {
    "{px}help [plugin_name]/[reply]": "Get common/plugin/command help by filling the plugin name or reply single word or message that contains plugin name.",
}
