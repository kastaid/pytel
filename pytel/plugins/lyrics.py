# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    LE,
    _try_purged,
    get_text,
    plugins_helper,
    px,
    pytel,
    random_prefixies,)


@pytel.instruction(
    ["lyrics"],
    outgoing=True,
)
async def _lyrics(client, message):
    search_text = get_text(message)

    if not search_text:
        return False

    if len(message.command) <= 0:
        return False

    else:
        _ = LE()
        kz = await message.edit(
            "Search lyrics..."
        )
        cx = "{}".format(search_text)
        songs = _.getting_my_lyrics(
            "{}".format(cx)
        )

        if "No results found" in songs:
            x = "No results found."
            return await kz.edit(
                "{}".format(x)
            )

        else:
            rxv = (
                songs.pop("title")
                + "\n\n"
                + songs.pop("lyrics")
            )
            cxz = rxv.replace(
                "\n",
                "\n",
            )
            MyLyrics = "{}".format(cxz)
        await kz.reply(
            MyLyrics,
            disable_notification=True,
        )
        return await _try_purged(kz, 3)


plugins_helper["lyrics"] = {
    f"{random_prefixies(px)}lyrics [artist - song]": "Get song lyrics.",
}
