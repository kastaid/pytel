# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in

from asyncio import sleep
from pyrogram.enums import (
    ChatType,
    ChatMembersFilter,
    ChatMemberStatus,)
from . import (
    ParseMode,
    FloodWait,
    _MENTION_LOCKED,
    eor,
    get_text,
    get_chat_ids,
    plugins_helper,
    px,
    pytel,
    suppress,
    _try_purged,
    mentioned,
    random_prefixies,)

mention_chats = []


@pytel.instruction(
    ["mentionall", "tagall"],
    outgoing=True,
    supergroups=True,
)
async def _mention_all(client, message):
    if client:
        user_id = client.me.id
    if user_id in _MENTION_LOCKED:
        await eor(
            message,
            text="Please wait until previous **--mention--** finished...",
        )
        return

    chat_id = message.chat.id
    tx = get_text(message, normal=True)
    if not tx:
        await eor(
            message,
            text="provide a **--text--** or message **--reply--** to the contents of a message when **--tagging--** a member.",
        )

    await _try_purged(message, 0.6)
    mention_chats.append(chat_id)
    _MENTION_LOCKED.add(user_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(
        chat_id
    ):
        if (
            chat_id not in mention_chats
        ) and (
            user_id
            not in _MENTION_LOCKED
        ):
            break
        elif (usr.user.is_bot) or (
            usr.user.is_deleted
        ):
            pass
        usrnum = usrnum + 1
        usrtxt += f"👤 <a href=tg://user?id={usr.user.id}>{await client.user_fullname(usr.user.id)}</a>\n"
        if usrnum == 5:
            try:
                txt = f"```Message\n{tx}\n```\n\n{usrtxt}\n"
                await client.send_message(
                    chat_id,
                    txt,
                    parse_mode=ParseMode.DEFAULT,
                )
                await sleep(20)
                usrnum = 0
                usrtxt = ""
            except FloodWait as flood:
                await sleep(
                    flood.value + 3
                )
                with suppress(
                    Exception
                ):
                    await client.send_message(
                        chat_id,
                        txt,
                        parse_mode=ParseMode.HTML,
                    )
                    await sleep(20)
                    usrnum = 0
                    usrtxt = ""
    with suppress(Exception):
        _MENTION_LOCKED.discard(user_id)
        mention_chats.remove(chat_id)


@pytel.instruction(
    ["cmention", "ctag"],
    outgoing=True,
    supergroups=True,
)
async def _cancel_mention(
    client, message
):
    if client:
        user_id = client.me.id
        chat_id = message.chat.id
    if (
        user_id not in _MENTION_LOCKED
    ) and (
        chat_id not in mention_chats
    ):
        await eor(
            message,
            text="You do not currently mention members of this group.",
        )
        return
    x = await eor(
        message,
        text="Canceling mention members...",
    )
    mention_chats.remove(chat_id)
    _MENTION_LOCKED.discard(user_id)
    await eor(
        x,
        text="Successfully stopped mentioning member.",
    )


@pytel.instruction(
    [
        "tadmins",
        "tadmin",
        "listadmins",
        "listadmin",
        "ladm",
    ],
    outgoing=True,
    supergroups=True,
)
async def _mention_admins(
    client, message
):
    gets = get_text(message)
    if not gets:
        gets = message.chat.id
    with suppress(Exception):
        grp = get_chat_ids(str(gets))
        if not grp:
            await eor(
                message,
                text="Please provide id/username/link messages of groups.",
            )
            return

    msg = await eor(
        message,
        text="<code>Checking ...</code>",
    )
    try:
        chat = await client.get_chat(
            grp
        )
    except Exception as excp:
        await eor(
            msg,
            text=f"Exception: {excp}",
        )
        return

    msg = await eor(
        msg,
        text="<code>Fetching admins...</code>",
    )
    _CH = [ChatType.CHANNEL]
    _GP = [
        ChatType.SUPERGROUP,
        ChatType.GROUP,
    ]
    if chat.type in _CH:
        await eor(
            msg,
            text="Can't fetching admins from channels.",
        )
        return
    elif chat.type in _GP:
        town, tadmins, badmins = (
            [],
            [],
            [],
        )
        async for admin in client.get_chat_members(
            chat.id,
            filter=ChatMembersFilter.ADMINISTRATORS,
        ):
            _admin = [
                ChatMemberStatus.ADMINISTRATOR
            ]
            _owner = [
                ChatMemberStatus.OWNER
            ]
            try:
                if (
                    admin.status
                    in _owner
                ):
                    town.append(
                        await mentioned(
                            client,
                            admin.user.id,
                            use_html=True,
                        )
                    )
                elif (
                    admin.status
                    in _admin
                ):
                    if (
                        admin.user.is_bot
                    ):
                        badmins.append(
                            await mentioned(
                                client,
                                admin.user.id,
                                use_html=True,
                            )
                        )
                    else:
                        tadmins.append(
                            await mentioned(
                                client,
                                admin.user.id,
                                use_html=True,
                            )
                        )

            except (
                BaseException
            ) as excp:
                await eor(
                    msg,
                    text=f"Error: {excp}",
                )
                return

        tadmins.sort()
        badmins.sort()
        total_adm = (
            len(tadmins)
            + len(badmins)
            + len(town)
        )
        text = "<b><u>LIST ADMINS</b></u>\n"
        text += f" ├ {chat.title}\n"
        text += f" └ <b>Group ID:</b> ( <code>{chat.id}</code> )\n\n"
        text += "<b><u>OWNERS</b></u>\n"
        if town:
            for o in town:
                text += (
                    " └ {}\n\n".format(
                        o
                    )
                )
        else:
            text += " └ Anonymous\n\n"
        text += "<b><u>ADMINS</b></u>\n"
        if tadmins:
            for a in tadmins:
                text += (
                    " ├ {}\n".format(a)
                )
            text += "\n"
        else:
            text += " └ Anonymous\n\n"
        text += "<b><u>BOT</b></u>\n"
        if badmins:
            for b in badmins:
                text += (
                    " ├ {}\n".format(b)
                )
            text += "\n"
        else:
            text += " └ Anonymous\n\n"
        text += f"<b><u>TOTAL ADMINISTRATORS</b></u> <code>{total_adm}</code> account."
        await eor(
            msg,
            text=text,
        )
        return (
            town.clear(),
            tadmins.clear(),
            badmins.clear(),
        )


plugins_helper["mention"] = {
    f"{random_prefixies(px)}mentionall / tagall [text/reply message]": "To mention members in the group. ( 20 seconds 1x send messages )",
    f"{random_prefixies(px)}cmention / ctag": "To cancel the current mention.",
    f"{random_prefixies(px)}listadmin / tadmin [id/username/link message or not]": "To mention or get list admins in groups.",
}
