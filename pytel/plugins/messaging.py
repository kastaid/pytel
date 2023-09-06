# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from datetime import datetime, timedelta
from typing import Optional
from ..client.dbase.dbMessaging import (
    add_schedule,
    check_schedule,
    check_dspam,
    cancel_schedule,
    clear_all_schedule,
    add_dspam,
    cancel_dspam,
    clear_all_dspam,)
from . import (
    _try_purged,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    eor,
    tz,
    ParseMode,
    FloodWait,)

schedule_and_delay_example = f"""
Command Guide Schedule and Delay

Examples:
{random_prefixies(px)}schmsg 240 5 360 Hello
{random_prefixies(px)}dsp 240 5 Hello

240    5     360   Hello
 |     |      |      |
time, count, time, message

Time Example:
240 = 4 minute
1 minute equals 60 seconds

Message Example (HTML):
<spoiler>Hello World</spoiler>

HTML Support:
<spoiler> text </spoiler>
<a href='url'> Hello World </a>
<b> bold </b>
<i> italic </i>
<u> underline </u>
<url> URL </url>
<code> code </code>
<pre> Text </pre>
<strong> Text </strong>

MARKDOWN Support:
**bold**
__italic__
--underline--
~~strike~~
||spoiler||
[text URL](https://pyrogram.org/)
[text user mention](tg://user?id=123456789)
`inline fixed-width code`
"""


@pytel.instruction(
    ["del", "delete"],
    outgoing=True,
)
async def _delete(client, message):
    replieds = message.reply_to_message
    if replieds:
        await _try_purged(replieds)
        await _try_purged(
            message,
            0.9,
        )
        return
    else:
        await _try_purged(
            message,
            0.4,
        )


@pytel.instruction(
    ["devpurged"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["purgeme"],
    outgoing=True,
)
async def _purge_me(client, message):
    if len(message.command) != 2:
        return await message.delete()

    user_id = client.me.id
    n = message.text.split(None, 1)[
        1
    ].strip()
    if not n.isnumeric():
        return await eor(
            message,
            text="Invalid Args",
        )

    n = int(n)
    if n <= 1:
        n: int = 2

    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(user_id),
            limit=n,
        )
    ]

    if not message_ids:
        return await eor(
            message,
            text="No messages found.",
        )

    to_delete = [
        message_ids[i : i + 99]
        for i in range(
            0,
            len(message_ids),
            99,
        )
    ]
    for (
        hundred_messages_or_less
    ) in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )


@pytel.instruction(
    ["schedule"],
    outgoing=True,
)
async def _schedule_msg(
    client, message
):
    chat_id: Optional[
        int
    ] = message.chat.id
    user_id = client.me.id
    if check_schedule(user_id, chat_id):
        await eor(
            message,
            text="Please wait until previous --schedule-- msg are finished..",
        )
        return
    else:
        try:
            args = message.text.split(
                " ", 4
            )
            schtimes = float(args[1])
            count = int(args[2])
            tms = float(args[3])
            mesg = str(args[4])
        except BaseException:
            await eor(
                message,
                text=schedule_and_delay_example,
                parse_mode=ParseMode.DISABLED,
            )
            return
        schtimes = (
            60
            if schtimes < 60
            else schtimes
        )
        timesleep = (
            60 if tms < 60 else tms
        )
        await message.delete()
        if count:
            add_schedule(
                int(user_id), chat_id
            )
            for _ in range(count):
                if not check_schedule(
                    user_id, chat_id
                ):
                    break
                try:
                    await client.send_message(
                        int(chat_id),
                        text=mesg,
                        schedule_date=datetime.now(
                            tz
                        )
                        + timedelta(
                            seconds=schtimes
                        ),
                    )
                    await sleep(
                        timesleep
                    )
                except (
                    FloodWait
                ) as excp:
                    await sleep(
                        excp.value + 5
                    )
                    await client.send_message(
                        int(chat_id),
                        text=mesg,
                        schedule_date=datetime.now(
                            tz
                        )
                        + timedelta(
                            seconds=schtimes
                        ),
                    )
                    await sleep(
                        timesleep
                    )
                except BaseException:
                    pass
            cancel_schedule(
                int(user_id), chat_id
            )


@pytel.instruction(
    ["ddsp"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["dsp"],
    outgoing=True,
)
async def _dspam_msg(client, message):
    chat_id: Optional[
        int
    ] = message.chat.id
    user_id = client.me.id
    if check_dspam(user_id, chat_id):
        await eor(
            message,
            text="Please wait until previous **delay-spam** are finished..",
        )
        return
    else:
        try:
            args = message.text.split(
                " ", 3
            )
            count = int(args[2])
            tms = float(args[1])
            mesg = str(args[3])
        except BaseException:
            await eor(
                message,
                text=schedule_and_delay_example,
                parse_mode=ParseMode.DISABLED,
            )
            return
        timesleep = (
            6 if tms < 6 else tms
        )
        await message.delete()
        if count:
            add_dspam(
                int(user_id), chat_id
            )
            for _ in range(count):
                if not check_dspam(
                    user_id, chat_id
                ):
                    break
                try:
                    await client.send_message(
                        int(chat_id),
                        text=mesg,
                    )
                    await sleep(
                        timesleep
                    )
                except (
                    FloodWait
                ) as excp:
                    await sleep(
                        excp.value + 5
                    )
                    await client.send_message(
                        int(chat_id),
                        text=mesg,
                    )
                    await sleep(
                        timesleep
                    )
                except BaseException:
                    pass
            cancel_dspam(
                int(user_id), chat_id
            )


@pytel.instruction(
    ["schcancel", "dspcancel"],
    outgoing=True,
)
async def _cancel_dspsch(
    client, message
):
    if (
        message.command[0]
        == "schcancel"
    ):
        x = await eor(
            message,
            text="Canceling schedule messages...",
        )
        if not check_schedule(
            client.me.id,
            message.chat.id,
        ):
            await eor(
                x,
                text="No current --**Schedule**-- msg are running or cancel in --schedule-- msg.",
            )
            return
        cancel_schedule(
            client.me.id,
            message.chat.id,
        )
        await eor(
            x,
            text="--**Schedule**-- messages has been canceled.",
        )
        return

    if (
        message.command[0]
        == "dspcancel"
    ):
        x = await eor(
            message,
            text="Canceling delay-spam messages...",
        )
        if not check_dspam(
            client.me.id,
            message.chat.id,
        ):
            await eor(
                x,
                text="No current --**Delay**-- messages are running.",
            )
            return
        cancel_dspam(
            client.me.id,
            message.chat.id,
        )
        await eor(
            x,
            text="--**Delay**-- messages has been canceled.",
        )


@pytel.instruction(
    ["clearsch", "cleardsp"],
    outgoing=True,
)
async def _clear_dspsch(
    client, message
):
    if message.command[0] == "cleardsp":
        clear_all_dspam(client.me.id)
        await eor(
            message,
            text="All --**Delay**-- messages has been cleared.",
        )
    if message.command[0] == "clearsch":
        clear_all_schedule(client.me.id)
        await eor(
            message,
            text="All --**Schedule**-- messages has been cleared.",
        )


plugins_helper["messaging"] = {
    f"{random_prefixies(px)}del [reply message]": "To deleted ur messages.",
    f"{random_prefixies(px)}purgeme [count]": "To purged ur messages.",
    f"{random_prefixies(px)}schedule [seconds] [count] [seconds] [text]": "To send schedule message. min: 60 seconds.",
    f"{random_prefixies(px)}dsp [seconds] [count] [text]": "To send delay-spam message. min: 6 seconds.",
    f"{random_prefixies(px)}schcancel": "To canceled ur schedule message in chats.",
    f"{random_prefixies(px)}dspcancel": "To canceled ur delay-spam message in chats.",
    f"{random_prefixies(px)}cleardsp": "To cleared all delay-spam messages.",
    f"{random_prefixies(px)}clearsch": "To cleared all schedule messages.",
}
