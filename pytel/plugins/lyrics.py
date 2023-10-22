# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    LE,
    _try_purged,
    get_text,
    plugins_helper,
    px,
    pytel,
    eor,
    replied,
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
        kz = await eor(
            message,
            text="Search lyrics...",
        )
        try:
            cx = "{}".format(
                search_text
            )
            songs = _.getting_my_lyrics(
                "{}".format(cx)
            )
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
            await client.send_message(
                message.chat.id,
                text=MyLyrics,
                disable_notification=True,
                reply_to_message_id=replied(
                    message
                ),
            )
            await _try_purged(kz, 2.5)
            return
        except BaseException:
            await eor(
                kz,
                text="No results found.",
            )
            return


plugins_helper["lyrics"] = {
    f"{random_prefixies(px)}lyrics [artist - song]": "Get song lyrics.",
}
