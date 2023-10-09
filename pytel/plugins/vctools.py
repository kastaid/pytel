# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import gather
from threading import RLock
from pyrogram.raw.functions.phone import (
    CreateGroupCall,
    DiscardGroupCall,
    EditGroupCallTitle,)
from pyrogram.raw.types import (
    InputPeerChannel,)
from . import (
    eor,
    extract_user,
    get_text,
    get_chat_ids,
    plugins_helper,
    px,
    pytel,
    _supersu,
    suppress,
    humanboolean,
    random_prefixies,)

_MTVC_TEXT = """
{}
├ <b>Can Talk:</b> <code>{}</code>
└ <b>Users:</b> {}
"""


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
    x = await eor(
        message,
        text="Started video chats...",
    )
    title = get_text(message)
    chat_id = message.chat.id
    peer = await client.resolve_peer(
        chat_id
    )
    try:
        group_call = (
            await client.get_group_call(
                message,
                chat_ids=chat_id,
            )
        )
        if group_call:
            await eor(
                x,
                text="Video chats available.",
            )
            return

        if not title:
            text = f"<b><u>{message.chat.title}</u></b>\n└ <b>Video chats started</b>"
            await client.invoke(
                CreateGroupCall(
                    peer=InputPeerChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash,
                    ),
                    random_id=client.rnd_id()
                    // 9000000000,
                )
            )
            await eor(x, text=text)
            return
        else:
            text = f"<b><u>{message.chat.title}</u></b>\n├ <b>Video chats started</b>\n└ <b>Title:</b> {title}"
            await client.invoke(
                CreateGroupCall(
                    peer=InputPeerChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash,
                    ),
                    random_id=client.rnd_id()
                    // 9000000000,
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
            await client.get_group_call(
                message
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
    ["titlevc", "tvc"],
    outgoing=True,
    supergroups=True,
    privileges=[
        "can_manage_video_chats"
    ],
)
async def _video_chats_settitle(
    client, message
):
    title = get_text(
        message, normal=True
    )
    if not title:
        await eor(
            message,
            text="Gimme a text to setup video chats title.",
        )
        return

    if len(title) > 40:
        await eor(
            message,
            text="The title is too long, it cannot be more than 40 characters.",
        )
        return

    x = await eor(
        message,
        text="Setup title video chats...",
    )
    if not (
        group_call := (
            await client.get_group_call(
                message
            )
        )
    ):
        await eor(
            x,
            text="Video chats not available.",
        )
        return

    await client.invoke(
        EditGroupCallTitle(
            call=group_call,
            title=title,
        )
    )
    text = f"""
<u><b>{message.chat.title}</b></u>
├ <b><u>Video Chat Title</b></u>
└ <b>Title:</b> {title}
"""
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
    _JOIN_LOCK = RLock()
    gets, gc = None, None
    with _JOIN_LOCK:
        gets = get_text(message)
        if not gets:
            gets = message.chat.id

        if gets:
            gc = get_chat_ids(str(gets))
        if not gc:
            await eor(
                message,
                text="Please provide id/username/link messages of group or channel.",
            )
            return

        x = await eor(
            message,
            text="Joined video chats...",
        )
        try:
            chat = (
                await client.get_chat(
                    gc
                )
            )
        except Exception as excp:
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Exception: {excp}",
            )
            return

        chat_id = int(chat.id)
        group_call = (
            await client.get_group_call(
                message,
                chat_ids=chat_id,
            )
        )
        if not group_call:
            await eor(
                x,
                text="Video chats not available.",
            )
            return

        par = await client.get_partici(
            group_call
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
                with suppress(
                    Exception
                ):
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
    _LEFT_LOCK = RLock()
    gets, gc = None, None
    with _LEFT_LOCK:
        gets = get_text(message)
        if not gets:
            gets = message.chat.id

        with suppress(BaseException):
            gc = get_chat_ids(str(gets))
            if not gc:
                await eor(
                    message,
                    text="Please provide id/username/link messages of group or channel.",
                )
                return

        x = await eor(
            message,
            text="Leaving video chats...",
        )
        try:
            chat = (
                await client.get_chat(
                    gc
                )
            )
        except Exception as excp:
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Exception: {excp}",
            )
            return

        chat_id = int(chat.id)
        group_call = (
            await client.get_group_call(
                message,
                chat_ids=chat_id,
            )
        )
        if not group_call:
            await eor(
                x,
                text="Video chats not available.",
            )
            return
        par = await client.get_partici(
            group_call
        )
        if int(par.count) > 0:
            check: list = []
            for u in par.users:
                check.append(u.id)
                if (
                    client.me.id
                    in check
                ):
                    with suppress(
                        Exception
                    ):
                        text = f"<u><b>{chat.title}</b></u>\n└ <b>Left video chats.</b>"
                        await gather(
                            client.group_call.leave_current_group_call(),
                            eor(
                                x,
                                text=text,
                            ),
                        )
                        #        await client.group_call.stop()
                        check.remove(
                            u.id
                        )
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
    _VCINFO_LOCK = RLock()
    gets, gc = None, None
    with _VCINFO_LOCK:
        gets = get_text(message)
        if not gets:
            gets = message.chat.id

        with suppress(BaseException):
            gc = get_chat_ids(str(gets))
            if not gc:
                await eor(
                    message,
                    text="Please provide id/username/link messages of group or channel.",
                )
                return

        x = await eor(
            message,
            text="Getting information video chats...",
        )
        try:
            chat = (
                await client.get_chat(
                    gc
                )
            )
        except Exception as excp:
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Exception: {excp}",
            )
            return

        chat_id = int(chat.id)
        group_call = (
            await client.get_group_call(
                message,
                chat_ids=chat_id,
            )
        )
        if not group_call:
            await eor(
                x,
                text="Video chats not available.",
            )
            return
        try:
            res = (
                await client.get_resvc(
                    group_call
                )
            )
            par = await client.get_partici(
                group_call
            )
        except Exception as excp:
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Exception: {excp}",
            )
            return

        join_mt = bool(
            res.call.join_muted
        )
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


@pytel.instruction(
    [
        "devmutevc",
        "devunmutevc",
        "dmvc",
        "dumvc",
    ],
    supersu=["PYTEL"],
    privileges=[
        "can_manage_video_chats"
    ],
)
@pytel.instruction(
    [
        "mutevc",
        "unmutevc",
        "mvc",
        "umvc",
    ],
    outgoing=True,
    supergroups=True,
    privileges=[
        "can_manage_video_chats"
    ],
)
async def _muting_user_video_chats_(
    client, message
):
    user_id = await extract_user(
        client, message
    )
    x = await eor(
        message,
        text="Checking...",
    )
    if not user_id:
        await eor(
            x,
            text="Unable to find user.",
        )
        return
    if user_id == client.me.id:
        await eor(
            x,
            text="Unable to muting ur self.",
        )
        return
    if user_id in list(_supersu):
        await eor(
            x,
            text="I can't muting, coz he's My Developer..",
        )
        return
    chat_id = message.chat.id
    group_call = (
        await client.get_group_call(
            message,
            chat_ids=chat_id,
        )
    )
    if not group_call:
        await eor(
            x,
            text="Video chats not available.",
        )
        return

    par = await client.get_partici(
        group_call
    )
    text = ""
    if int(par.count) > 0:
        lpar: list = []
        for u in par.users:
            lpar.append(u.id)
            if user_id in lpar:
                participant = await client.resolve_peer(
                    user_id
                )
                mention = (
                    await client.get_users(
                        user_id
                    )
                ).mention
                try:
                    if (
                        message.command[
                            0
                        ][0]
                        == "u"
                    ):
                        muted = False
                        text = "<b><u>Unmuting</u> IN VIDEO CHATS</b>"
                    else:
                        muted = True
                        text = "<b><u>Muting</u> IN VIDEO CHATS</b>"
                    await client.muting_user_vc(
                        group_call=group_call,
                        participant=participant,
                        muted=muted,
                    )
                    await eor(
                        x,
                        text=_MTVC_TEXT.format(
                            text,
                            humanboolean(
                                muted
                            ),
                            mention,
                        ),
                    )
                    lpar.clear()
                    return
                except (
                    Exception
                ) as excp:
                    await eor(
                        x,
                        text=f"Error: {excp}",
                    )
                    return

            else:
                await eor(
                    x,
                    text="The user is not in a video chat.",
                )
                lpar.clear()
                return
    else:
        await eor(
            x,
            text="No one else in the video chat.",
        )
        return


plugins_helper["vctools"] = {
    f"{random_prefixies(px)}startvc / stvc [title or not]": "To started video chats/channel.",
    f"{random_prefixies(px)}stopvc / spvc": "To stopped video chats/channel.",
    f"{random_prefixies(px)}joinvc / jvc [url/link message/username/id or not]": "To joined video chats/channel.",
    f"{random_prefixies(px)}leftvc / lvc [url/link message/username/id or not]": "To left video chats/channel.",
    f"{random_prefixies(px)}infovc / ivc [url/link message/username/id or not]": "To get information video chats/channel.",
    f"{random_prefixies(px)}mutevc / mvc [id/username/reply to user]": "To Muting user in video chats.",
    f"{random_prefixies(px)}unmutevc / umvc [id/username/reply to user]": "To Unmuting user in video chats.",
    f"{random_prefixies(px)}titlevc / tvc [text/reply to message]": "To setup video chats title.",
}
