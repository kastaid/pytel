# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from . import (
    ChatGPT,
    eor,
    get_text,
    plugins_helper,
    px,
    pytel,
    random_prefixies,)


@pytel.instruction(
    [
        "aitext",
        "ask",
    ],
    outgoing=True,
)
async def _openai(client, message):
    if (
        message.command[0] == "aitext"
        or "ask"
    ):
        args = get_text(message)
        if not args:
            await eor(
                message,
                text="ask a question to use ChatGPT.",
            )
            return

        x = await eor(
            message,
            text="currently submitting a request...",
        )
        resp = await ChatGPT.text(args)
        if resp:
            await eor(
                x,
                text=f"```ChatGPT\n{resp}\n```",
            )
            return

        else:
            await eor(
                x,
                text="ChatGPT not reponded!",
            )


plugins_helper["chatgpt"] = {
    f"{random_prefixies(px)}aitext / ask [text/reply]": "To get an answer from ChatGPT in the form of an Text.",
}
