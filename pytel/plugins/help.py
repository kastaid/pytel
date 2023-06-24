# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import px, pytel, plugins_helper


@pytel.instruction("help", self_only=True)
async def _help(client, message):
    await message.edit("Tester")


plugins_helper["help"] = {
    f"{px}help [plugin_name]/[reply]": "Get common/plugin/command help by filling the plugin name or reply single word or message that contains plugin name.",
}
