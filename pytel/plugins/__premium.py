# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from time import time
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    CallbackQuery,)
from ..client.dbase.dbExpired import (
    get_expired_date,
    set_expired_days,
    rem_expired,
    user_expired,)
from . import (
    OWNER_ID,
    ChatSendInlineForbidden,
    BotResponseTimeout,
    QueryIdInvalid,
    ParseMode,
    _try_purged,
    px,
    eor,
    pytel,
    pytel_tgb,
    start_time,
    suppress,
    time_formatter,
    buttons,
    filters,
    developer,
    ikmarkup,
    legally_required,
    channel_groups,)


async def _get_status_user(
    from_user: int,
) -> str:
    pyprem, status = (
        "",
        "",
    )
    (
        expired,
        time_left,
    ) = (None, None)
    if from_user:
        status = (
            "VVIP"
            if from_user
            in list(developer)
            or from_user
            == int(OWNER_ID)
            else "Customer"
        )
        (
            expired,
            time_left,
        ) = await get_expired_date(
            int(from_user)
        )
        pyprem = (
            "active-"
            if expired and time_left
            else "inactive-"
        )

        uptime = time_formatter(
            (time() - start_time) * 1000
        )
        text = f"""
<u><b>PYTEL-Premium</b></u> 🇮🇩
<u> └</u> <b>Status</b>: {pyprem}[ <u><b>{status}</u></b> ]
 ├ <b>Uptime</b>: <code>{uptime}</code>
 ├ <b>Expired</b>: {expired}
 └ <b>Time Left</b>: {time_left}

(c) @kastaid #pytel
"""
        return str(text)


@pytel.instruction(
    [
        "expired",
        "status",
    ],
    force_edit=False,
    supergroups=True,
    supersu=["PYTEL"],
    disable_errors=True,
)
@pytel.instruction(
    [
        "expired",
        "status",
    ],
    outgoing=True,
    force_edit=False,
    supergroups=True,
    disable_errors=True,
)
async def _premium_stats(
    client, message
):
    if (
        message.command[0] == "expired"
        or "status"
    ):
        prem_stat = "status_premium"
        try:
            _ = await client.get_inline_bot_results(
                pytel_tgb.me.username,
                prem_stat,
            )
            for result in _.results:
                try:
                    await message.reply_inline_bot_result(
                        query_id=_.query_id,
                        result_id=result.id,
                    )
                except ChatSendInlineForbidden:
                    text = await _get_status_user(
                        client.me.id
                    )
                    await message.reply(
                        text=text,
                    )
                    return
        except BotResponseTimeout:
            await eor(
                message,
                text="Did not answer the request, please try again.",
            )
            return
        return await _try_purged(
            message
        )


@pytel_tgb.on_inline_query(
    filters.regex("status_premium")
)
async def _premstat_inline(
    client,
    cq: CallbackQuery,
):
    from_user = cq.from_user.id
    if from_user:
        rpm = ikmarkup(
            [
                [
                    buttons(
                        "ꜱᴛᴀᴛꜱ",
                        callback_data="sys_stats",
                    ),
                ],
                [
                    buttons(
                        "ᴄʟᴏꜱᴇ",
                        callback_data="help_close",
                    ),
                ],
            ]
        )
        text = await _get_status_user(
            from_user
        )
        with suppress(QueryIdInvalid):
            await client.answer_inline_query(
                cq.id,
                is_personal=True,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="STATUS PREMIUM\n@kastaid #pytel",
                            reply_markup=rpm,
                            input_message_content=InputTextMessageContent(
                                message_text=text,
                                parse_mode=ParseMode.HTML,
                                disable_web_page_preview=True,
                            ),
                        )
                    )
                ],
            )


@pytel_tgb.on_message(
    legally_required
    & channel_groups
    & filters.private
    & filters.command(
        "setpremium",
        prefixes=list(px),
    )
)
async def _set_premium_user(
    client, message
):
    text, duration = (
        None,
        None,
    )
    xy = await message.reply(
        text="Please wait, processing purchase data...",
    )
    if message.reply_to_message:
        user_id = (
            message.reply_to_message.from_user.id
        )
        drt = message.command
        duration = int(drt[1])
    else:
        try:
            m = message.command
            usr = str(m[2])
            duration = int(m[1])
            user = (
                await client.get_users(
                    usr
                )
            )
        except BaseException:
            await xy.edit_text(
                "I can't find that user"
            )
            return

        if (user is None) or (not user):
            await xy.edit_text(
                f"I can't find that user: {usr} ."
            )
            return
        user_id = user.id

    x = await client.get_users(
        user_id
    )  # try
    if (duration is None) or (
        not duration
    ):
        await xy.edit_text(
            "Please fill in the nominal how many months."
        )
        return
    if user_expired().get(int(x.id)):
        (
            expired,
            time_left,
        ) = await get_expired_date(
            int(x.id)
        )
        asxc = f"""
<u>Buyer</u> {x.mention} <u>is already in the database</u>.

❯ <b>Expired</b>: {expired}
❯ <b>Time Left</b>: {time_left}

Want to be extended? wait until it expires.

(c) @kastaid #pytel
"""
        await xy.edit_text(asxc)
        return

    if duration == 1:
        price = "Rp 25.000"
    elif duration == 2:
        price = "Rp 50.000"
    elif duration == 3:
        price = "Rp 75.000"
    elif duration == 4:
        price = "Rp 100.000"
    elif duration == 5:
        price = "Rp 125.000"
    elif duration == 6:
        price = "Rp 150.000"
    elif duration == 7:
        price = "Rp 175.000"
    elif duration == 8:
        price = "Rp 200.000"
    else:
        await xy.edit_text(
            "Purchase a minimum of 1 month and a maximum of 8 months."
        )
        return

    set_expired_days(
        x.id,
        int(duration),
    )
    await sleep(2.5)
    (
        expired,
        time_left,
    ) = await get_expired_date(
        int(x.id)
    )

    text = f"""
✅ <u>Done, purchase has been successful.</u>

<b><u>Buyer Status</b></u>
 ├ <b>Name:</b> {x.mention}
 ├ <b>User ID:</b> <code>{x.id}</code>
 ├ <b>Monthly purchases:</b> {duration} month.
 └ <b>Price:</b> <code>{price}</code>

❯ <b>Expired</b>: {expired}
❯ <b>Time Left</b>: {time_left}

<u>Thank you very much loyal Customer</u>.

<b>Note:</b>
Tekan Tombol Generate Session 🚀
Untuk membuat String Session Pyrogram,
Lalu aktifkan PYTEL-Premium.

(c) @kastaid #pytel
"""
    await _try_purged(xy, 1.5)
    rpm = ikmarkup(
        [
            [
                buttons(
                    "Generate Session 🚀",
                    callback_data="generate_session",
                ),
            ],
        ]
    )
    with suppress(Exception):
        yy = await client.send_animation(
            message.chat.id,
            animation="resources/kastaid/pytel_checkout.gif",
            caption=text,
            unsave=False,
            reply_markup=rpm,
            protect_content=True,
        )
        await yy.copy(x.id)


@pytel_tgb.on_message(
    legally_required
    & channel_groups
    & filters.private
    & filters.command(
        "delpremium",
        prefixes=list(px),
    )
)
async def _del_premium_user(
    client, message
):
    xy = await message.reply(
        text="Please wait...",
    )
    if message.reply_to_message:
        user_id = (
            message.reply_to_message.from_user.id
        )
    else:
        try:
            m = message.command
            username = str(m[1])
            user = (
                await client.get_users(
                    username
                )
            )
        except BaseException:
            await xy.edit_text(
                "I can't find that user"
            )
            return

        if (user is None) or (not user):
            await xy.edit_text(
                f"I can't find that user {username} ."
            )
            return
        user_id = user.id

    x = await client.get_users(user_id)
    if user_expired().get(int(x.id)):
        rem_expired(int(user_id))
        text = f"""
🗑 <u>Done, buyer data has been removed.</u>
 └ <b>User:</b> {x.mention}

(c) @kastaid #pytel
"""
        await xy.edit_text(text)
        return

    else:
        asxc = f"""
<u>Buyer</u> {x.mention} <u>not already in the database</u>
"""
        await xy.edit_text(asxc)
        return
