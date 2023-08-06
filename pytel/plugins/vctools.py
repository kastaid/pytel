# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import gather
from random import randint
from re import sub, search
from typing import Optional, Any
from pyrogram import enums, Client
from pyrogram.raw.functions.channels import (
    GetFullChannel,)
from pyrogram.raw.functions.messages import (
    GetFullChat,)
from pyrogram.raw.functions.phone import (
    GetGroupCall,
    CreateGroupCall,
    DiscardGroupCall,
    GetGroupParticipants,)
from pyrogram.raw.types import (
    InputGroupCall,
    InputPeerChannel,
    InputPeerChat,)
from . import (
    eor,
    get_text,
    plugins_helper,
    px,
    pytel,
    suppress,
    humanboolean,
    random_prefixies,)


async def get_group_call(
    client: Client,
    message,
    chat_ids: Any = None,
) -> Optional[InputGroupCall]:
    if chat_ids:
        chat_id = chat_ids
    else:
        chat_id = message.chat.id
    chat_peer = (
        await client.resolve_peer(
            chat_id
        )
    )
    if isinstance(
        chat_peer,
        (
            InputPeerChannel,
            InputPeerChat,
        ),
    ):
        if isinstance(
            chat_peer, InputPeerChannel
        ):
            full_chat = (
                await client.send(
                    GetFullChannel(
                        channel=chat_peer
                    )
                )
            ).full_chat
        elif isinstance(
            chat_peer, InputPeerChat
        ):
            full_chat = (
                await client.send(
                    GetFullChat(
                        chat_id=chat_peer.chat_id
                    )
                )
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    return False


async def get_resvc(
    client: Client, group_call: Any
) -> GetGroupCall:
    res = await client.invoke(
        GetGroupCall(
            call=group_call,
            limit=500,
        ),
    )
    return res


async def get_partici(
    client: Client, group_call: Any
) -> GetGroupParticipants:
    par = await client.invoke(
        GetGroupParticipants(
            call=group_call,
            ids=[],
            sources=[],
            offset="",
            limit=500,
        ),
    )
    return par


@pytel.instruction(
    ["devstartvc", "dstvc"],
    supersu=["PYTEL"],
    privileges=[
        "can_manage_video_chats"
    ],
)
@pytel.instruction(
    ["startvc", "stvc"],
    outgoing=True,
    supergroups=True,
    privileges=[
        "can_manage_video_chats"
    ],
)
async def _video_chats_start(
    client, message
):
    flags = " ".join(
        message.command[1:]
    )
    x = await eor(
        message,
        text="Started video chats...",
    )
    title = get_text(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    try:
        if not title:
            text = f"<b><u>{message.chat.title}</u></b>\n└ <b>Video chats started</b>"
            await client.invoke(
                CreateGroupCall(
                    peer=(
                        await client.resolve_peer(
                            chat_id
                        )
                    ),
                    random_id=randint(
                        10000, 999999999
                    ),
                )
            )
            await eor(x, text=text)
            return
        else:
            text = f"<b><u>{message.chat.title}</u></b>\n├ <b>Video chats started</b>\n└ <b>Title:</b> {title}"
            await client.invoke(
                CreateGroupCall(
                    peer=(
                        await client.resolve_peer(
                            chat_id
                        )
                    ),
                    random_id=randint(
                        10000, 999999999
                    ),
                    title=title,
                )
            )
            await eor(x, text=text)
            return
    except Exception as excp:
        client.send_log.exception(excp)
        await eor(
            x, text=f"Exception: {excp}"
        )
        return


@pytel.instruction(
    ["devstopvc", "dspvc"],
    supersu=["PYTEL"],
    privileges=[
        "can_manage_video_chats"
    ],
)
@pytel.instruction(
    ["stopvc", "spvc"],
    outgoing=True,
    supergroups=True,
    privileges=[
        "can_manage_video_chats"
    ],
)
async def _video_chats_stop(
    client, message
):
    x = await eor(
        message,
        text="Stopped video chats...",
    )
    if not (
        group_call := (
            await get_group_call(
                client, message
            )
        )
    ):
        await eor(
            x,
            text="Video chats not available.",
        )
        return
    await client.invoke(
        DiscardGroupCall(
            call=group_call
        )
    )
    text = f"<u><b>{message.chat.title}</b></u>\n└ <b>Video chats has been stopped.</b>"
    await eor(x, text=text)


@pytel.instruction(
    ["devjoinvc", "djvc"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["joinvc", "jvc"],
    outgoing=True,
    supergroups=True,
)
async def _video_chats_joined(
    client, message
):
    x = await eor(
        message,
        text="Joined video chats...",
    )
    gc = (
        message.command[1]
        if len(message.command) > 1
        else message.chat.id
    )
    if isinstance(gc, int):
        gc: int = gc
    else:
        if "@" in gc:
            gc: str = gc
        elif "/c/" or "t.me/" in gc:
            gc = sub(
                "\\s+(.*)$", r"", gc
            )
            gc = (
                search(r"/c/(.*)/", gc)
                or search(
                    r"/c/(.*)", gc
                )
                or search(
                    r"t.me/(.*)/", gc
                )
                or search(
                    r"t.me/(.*)", gc
                )
            )
            gc = (
                f"-100{gc.group(1)}"
                if isinstance(
                    gc.group(1), int
                )
                else f"@{gc.group(1)}"
            )
    try:
        chat = await client.get_chat(gc)
    except Exception as excp:
        client.send_log.exception(excp)
        await eor(
            x, text=f"Exception: {excp}"
        )
        return
    with suppress(ValueError):
        chat_id = int(chat.id)

    group_call = await get_group_call(
        client,
        message,
        chat_ids=chat_id,
    )
    if not group_call:
        await eor(
            x,
            text="Video chats not available.",
        )
        return

    par = await get_partici(
        client, group_call
    )
    check = []
    for i in par.users:
        check.append(i.id)
        if client.me.id in check:
            await eor(
                x,
                text=f"<u><b>{chat.title}</b></u>\n└ <b>You're in Video Chats.</b>",
            )
            check.remove(i.id)
            return
        else:
            with suppress(Exception):
                await client.group_call.start(
                    chat_id
                )

            text = f"<u><b>{chat.title}</b></u>\n└ <b>Joined video chats.</b>"
            await eor(x, text=text)
            return


@pytel.instruction(
    ["devleftvc", "dlvc"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["leftvc", "lvc"],
    outgoing=True,
    supergroups=True,
)
async def _video_chats_leaving(
    client, message
):
    x = await eor(
        message,
        text="Leaving video chats...",
    )
    gc = (
        message.command[1]
        if len(message.command) > 1
        else message.chat.id
    )
    if isinstance(gc, int):
        gc: int = gc
    else:
        if "@" in gc:
            gc: str = gc
        elif "/c/" or "t.me/" in gc:
            gc = sub(
                "\\s+(.*)$", r"", gc
            )
            gc = (
                search(r"/c/(.*)/", gc)
                or search(
                    r"/c/(.*)", gc
                )
                or search(
                    r"t.me/(.*)/", gc
                )
                or search(
                    r"t.me/(.*)", gc
                )
            )
            gc = (
                f"-100{gc.group(1)}"
                if isinstance(
                    gc.group(1), int
                )
                else f"@{gc.group(1)}"
            )
    try:
        chat = await client.get_chat(gc)
    except Exception as excp:
        client.send_log.exception(excp)
        await eor(
            x, text=f"Exception: {excp}"
        )
        return
    with suppress(ValueError):
        chat_id = int(chat.id)

    group_call = await get_group_call(
        client,
        message,
        chat_ids=chat_id,
    )
    if not group_call:
        await eor(
            x,
            text="Video chats not available.",
        )
        return
    par = await get_partici(
        client, group_call
    )
    if int(par.count) > 0:
        check: list = []
        for u in par.users:
            check.append(u.id)
            if client.me.id in check:
                with suppress(
                    Exception
                ):
                    text = f"<u><b>{chat.title}</b></u>\n└ <b>Left video chats.</b>"
                    await gather(
                        client.group_call.leave_current_group_call(),
                        eor(
                            x, text=text
                        ),
                    )
                    #        await client.group_call.stop()
                    check.remove(u.id)
                    return
            else:
                await eor(
                    x,
                    text=f"<u><b>{chat.title}</b></u>\n└ <b>You're not in Video Chats.</b>",
                )
                return
    else:
        await eor(
            x,
            text=f"<u><b>{chat.title}</b></u>\n└ <b>You're not in Video Chats.</b>",
        )
        return


@pytel.instruction(
    ["devinfovc", "divc"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["infovc", "ivc"],
    outgoing=True,
    supergroups=True,
)
async def _video_chats_information(
    client, message
):
    x = await eor(
        message,
        text="Getting information video chats...",
    )
    gc = (
        message.command[1]
        if len(message.command) > 1
        else message.chat.id
    )
    if isinstance(gc, int):
        gc: int = gc
    else:
        if "@" in gc:
            gc: str = gc
        elif "/c/" or "t.me/" in gc:
            gc = sub(
                "\\s+(.*)$", r"", gc
            )
            gc = (
                search(r"/c/(.*)/", gc)
                or search(
                    r"/c/(.*)", gc
                )
                or search(
                    r"t.me/(.*)/", gc
                )
                or search(
                    r"t.me/(.*)", gc
                )
            )
            gc = (
                f"-100{gc.group(1)}"
                if isinstance(
                    gc.group(1), int
                )
                else f"@{gc.group(1)}"
            )
    try:
        chat = await client.get_chat(gc)
    except Exception as excp:
        client.send_log.exception(excp)
        await eor(
            x, text=f"Exception: {excp}"
        )
        return
    with suppress(ValueError):
        chat_id = int(chat.id)

    group_call = await get_group_call(
        client,
        message,
        chat_ids=chat_id,
    )
    if not group_call:
        await eor(
            x,
            text="Video chats not available.",
        )
        return
    try:
        res = await get_resvc(
            client, group_call
        )
        par = await get_partici(
            client, group_call
        )
    except Exception as excp:
        client.send_log.exception(excp)
        await eor(
            x, text=f"Exception: {excp}"
        )
        return

    join_mt = bool(res.call.join_muted)
    if int(par.count) > 0:
        _ = """
<b><u>{}</u></b>

<u>{}</u>
├ <b>{}</b>: <code>{}</code>
├ <b>{}:</b> <code>{}</code>
├ <b>{}:</b> <code>{}</code>
└ <b>{}:</b> <code>{}</code>

<b><u>{}</u></b>
┌─────────────────
""".format(
            "Video Chats Information",
            chat.title,
            "Video Chats Version",
            par.version,
            "Video Chats Title",
            res.call.title or "N/A",
            "Join Muted",
            humanboolean(join_mt),
            "Participants Count",
            par.count,
            "Participants List",
        )
        for i in par.users:
            _ += f"├ <code>{int(i.id)}</code>  -  <a href=tg://user?id={int(i.id)}>{await client.user_fullname(int(i.id))}</a>\n"

    else:
        _ = """
<b><u>{}</u></b>

<u>{}</u>
├ <b>{}</b>: <code>{}</code>
├ <b>{}:</b> <code>{}</code>
├ <b>{}:</b> <code>{}</code>
└ <b>{}:</b> <code>{}</code>
""".format(
            "Video Chats Information",
            chat.title,
            "Video Chats Version",
            par.version,
            "Video Chats Title",
            res.call.title or "N/A",
            "Join Muted",
            humanboolean(join_mt),
            "Participants Count",
            par.count,
        )
    await eor(
        x,
        text=_,
    )
    return


plugins_helper["vctools"] = {
    f"{random_prefixies(px)}startvc / stvc [title or not]": "To started video chats/channel.",
    f"{random_prefixies(px)}stopvc / spvc": "To stopped video chats/channel.",
    f"{random_prefixies(px)}joinvc / jvc [url/link message/username/id or not]": "To joined video chats/channel.",
    f"{random_prefixies(px)}leftvc / lvc [url/link message/username/id or not]": "To left video chats/channel.",
    f"{random_prefixies(px)}infovc / ivc [url/link message/username/id or not]": "To get information video chats/channel.",
}
