# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pyrogram.types import CallbackQuery
from ..client.dbase.dbStartAsst import (
    checks_users,
    added_users,)
from . import (
    Assistant,
    OWNER_ID,
    pytel_tgb,
    suppress,
    filters,)


@pytel_tgb.on_message(
    filters.command(
        "start",
        prefixes="/",
    )
    & filters.private
    & ~filters.forwarded
)
async def _asst_home(client, message):
    await message.reply(
        Assistant.START.format(
            message.from_user.mention,
        ),
        quote=False,
        disable_web_page_preview=True,
        reply_markup=Assistant.home_buttons,
    )
    fullname = (
        message.from_user.first_name
        + message.from_user.last_name
        if message.from_user.last_name
        else message.from_user.first_name
    )
    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "None"
    )
    if checks_users(
        message.from_user.id
    ):
        return
    else:
        added_users(
            message.from_user.id
        )
        await client.send_message(
            int(OWNER_ID),
            Assistant.start_text_from_user.format(
                fullname,
                message.from_user.id,
                username,
            ),
        )


@pytel_tgb.on_callback_query()
async def _cb_asst(
    client, cq: CallbackQuery
):
    ts = cq.data.lower()
    if ts == "cls":
        with suppress(BaseException):
            await cq.message.delete()
    elif ts == "home":
        with suppress(BaseException):
            await cq.message.edit(
                Assistant.START.format(
                    cq.from_user.mention,
                ),
                disable_web_page_preview=True,
                reply_markup=Assistant.home_buttons,
            )
    elif ts == "privacy":
        with suppress(BaseException):
            await cq.message.edit(
                Assistant.PRIVACY,
                disable_web_page_preview=True,
                reply_markup=Assistant.privacy_buttons,
            )
