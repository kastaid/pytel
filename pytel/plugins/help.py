# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from re import match
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageNotModified,
)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from ..client.leverage import plugins_button
from . import (
    _try_purged,
    eor,
    filters,
    get_text,
    plugins_helper,
    px,
    pytel,
    pytel_tgb,
    random_prefixies,
    suppress,
)


@pytel.instruction(
    ["help", "ihelp"], outgoing=True
)
async def _help(client, message):
    if message.command[0] == "ihelp":
        plugins_n = "help_plugins"
        try:
            _ = await client.get_inline_bot_results(
                pytel_tgb.me.username,
                plugins_n,
            )
            for name in _.results:
                await message.reply_inline_bot_result(
                    _.query_id, name.id
                )
        except Exception as error:
            await message.reply(error)
        return await _try_purged(
            message, 3.5
        )

    if message.command[0] == "help":
        plugins_name = get_text(message)
        name = None

        if not plugins_name:
            text = f"<b>Command Guide</b>\n\n<code>{random_prefixies(px)}help lyrics</code> : <u>To get song lyrics</u>\n<code>{random_prefixies(px)}ihelp</code> : <u>Inline help</u>"
            await eor(message, text=text)
            return

        if plugins_name in plugins_helper:
            name = plugins_name
        else:
            for x in plugins_name.split():
                if x in plugins_helper:
                    name = x
                    break
        if name:
            cmds = plugins_helper[name]
            text = f"<b>{len(cmds)} Commands For <u>{name.upper()}</u></b>\n\n"
            for cmd, desc in cmds.items():
                text += "</b>❯</b> <code>{}</code>\n<b>Description:</b> <i>{}</i>\n\n".format(
                    cmd, desc
                )
            text += "(c) @kastaid #pytel"
            await eor(message, text=text)
            return
        await eor(
            message,
            text=f"<b>Plugins Not Found</b> for <code>{plugins_name}</code>\n<b><u>Example</u>:</b> <code>{random_prefixies(px)}ihelp</code> to see inline helper.",
        )
        return


@pytel_tgb.on_inline_query(
    filters.regex("^help_plugins")
)
async def _help_inline(
    client, inline_query
):
    content = "<b>❏ Help Menu\n├ Plugins : {}\n├ Commands : {}\n╰ Prefixies : <code>{}</code></b>\n\n".format(
        plugins_helper.count,
        plugins_helper.total,
        "".join(px),
    )
    content += "(c) @kastaid #pytel"
    await sleep(0.2)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=300,
        results=[
            (
                InlineQueryResultArticle(
                    title="Help Menu",
                    reply_markup=InlineKeyboardMarkup(
                        plugins_button(
                            0,
                            plugins_helper,
                            "help",
                        )
                    ),
                    input_message_content=InputTextMessageContent(
                        content
                    ),
                )
            )
        ],
    )


@pytel_tgb.on_callback_query(
    filters.regex(r"help_(.*?)")
)
async def _(client, callback_query):
    plugins_match = match(
        r"help_plug\((.+?)\)",
        callback_query.data,
    )
    prev_page = match(
        r"help_prev\((.+?)\)",
        callback_query.data,
    )
    next_page = match(
        r"help_next\((.+?)\)",
        callback_query.data,
    )
    back_page = match(
        r"help_back", callback_query.data
    )
    if plugins_match:
        nm = plugins_match[1]
        for _ in nm:
            name = (
                _
                if _ in plugins_helper
                else nm
            )
            cmds = plugins_helper[name]
            text = f"<b>{len(cmds)} Commands For <u>{name.upper()}</b></u>\n\n"
            for cmd, desc in cmds.items():
                text += "<b>❯</b><code>{}</code>\n<b>Description:</b> <i>{}</i>\n\n".format(
                    cmd, desc
                )
            text += "(c) @kastaid #pytel"
            button = [
                [
                    InlineKeyboardButton(
                        "‹ ʙᴀᴄᴋ",
                        callback_data="help_back",
                    )
                ]
            ]
            try:
                await sleep(0.2)
                await callback_query.edit_message_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(
                        button
                    ),
                    disable_web_page_preview=True,
                )
            except (
                MessageNotModified,
                FloodWait,
            ) as excp:
                if (
                    excp.ID
                    == "FLOOD_WAIT_X"
                ):
                    await sleep(excp.value)
                elif (
                    excp.ID
                    == "MESSAGE_NOT_MODIFIED"
                ):
                    await sleep(1.3)
                else:
                    await sleep(1.3)
                with suppress(Exception):
                    await callback_query.edit_message_text(
                        text=text,
                        reply_markup=InlineKeyboardMarkup(
                            button
                        ),
                        disable_web_page_preview=True,
                    )

    prev_text = "<b>❏ Help Menu\n├ Plugins : {}\n├ Commands : {}\n╰ Prefixies : <code>{}</code></b>\n\n".format(
        plugins_helper.count,
        plugins_helper.total,
        "".join(px),
    )
    prev_text += "(c) @kastaid #pytel"
    if prev_page:
        curr_page = int(prev_page[1])
        await sleep(0.2)
        await callback_query.edit_message_text(
            text=prev_text,
            reply_markup=InlineKeyboardMarkup(
                plugins_button(
                    curr_page - 1,
                    plugins_helper,
                    "help",
                )
            ),
            disable_web_page_preview=True,
        )
    next_text = "<b>❏ Help Menu\n├ Plugins : {}\n├ Commands : {}\n╰ Prefixies : <code>{}</code></b>\n\n".format(
        plugins_helper.count,
        plugins_helper.total,
        "".join(px),
    )
    next_text += "(c) @kastaid #pytel"
    if next_page:
        nx_page = int(next_page[1])
        await sleep(0.2)
        await callback_query.edit_message_text(
            text=next_text,
            reply_markup=InlineKeyboardMarkup(
                plugins_button(
                    nx_page + 1,
                    plugins_helper,
                    "help",
                )
            ),
            disable_web_page_preview=True,
        )
    back_text = "<b>❏ Help Menu\n├ Plugins : {}\n├ Commands : {}\n╰ Prefixies : <code>{}</code></b>\n\n".format(
        plugins_helper.count,
        plugins_helper.total,
        "".join(px),
    )
    back_text += "(c) @kastaid #pytel"
    if back_page:
        await sleep(0.2)
        await callback_query.edit_message_text(
            text=back_text,
            reply_markup=InlineKeyboardMarkup(
                plugins_button(
                    0,
                    plugins_helper,
                    "help",
                )
            ),
            disable_web_page_preview=True,
        )


plugins_helper["help"] = {
    f"{random_prefixies(px)}help [plugin_name]/[reply]": "Get common/plugin/command help by filling the plugin name or reply single word or message that contains plugin name.",
    f"{random_prefixies(px)}ihelp": "Get inline helper.",
}
