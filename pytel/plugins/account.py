# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep, gather
from io import BytesIO
from PIL import Image
from pyrogram import enums
from pyrogram.raw.functions.messages import (
    DeleteHistory,
    StartBot,)
from . import (
    SETMODE_ONLINE,
    SETMODE_OFFLINE,
    Rooters,
    functions,
    eor,
    extract_user,
    plugins_helper,
    px,
    get_args,
    get_text,
    pytel,
    _supersu,
    suppress,
    random_prefixies,)


@pytel.instruction(
    ["setmode"],
    outgoing=True,
)
async def _online_offline(
    client, message
):
    mode = message.text.split(None, 1)
    if not mode:
        return

    if mode[1] in ["online", "on"]:
        user_lock = client.me.id
        if user_lock in SETMODE_OFFLINE:
            SETMODE_OFFLINE.discard(
                user_lock
            )
        else:
            SETMODE_ONLINE.add(
                user_lock
            )
        status = "Online"
        await eor(
            message,
            text=f"✅ Success, ur status is <u>{status}</u>",
        )
        # Status Online
        while True:
            try:
                if (
                    user_lock
                    not in SETMODE_ONLINE
                ):
                    break
                await client.invoke(
                    query=functions.account.UpdateStatus(
                        offline=False
                    ),
                )
            except Exception:
                SETMODE_ONLINE.discard(
                    user_lock
                )
                break

    elif mode[1] in [
        "offline",
        "off",
    ]:
        user_lock = client.me.id
        if user_lock in SETMODE_ONLINE:
            SETMODE_ONLINE.discard(
                user_lock
            )
        else:
            SETMODE_OFFLINE.add(
                user_lock
            )
        status = "Offline"
        await eor(
            message,
            text=f"✅ Success, ur status is <u>{status}</u>",
        )
        # Status Offline
        while True:
            try:
                if (
                    user_lock
                    not in SETMODE_OFFLINE
                ):
                    break
                await client.invoke(
                    query=functions.account.UpdateStatus(
                        offline=True
                    ),
                )
            except Exception:
                SETMODE_OFFLINE.discard(
                    user_lock
                )
                break


@pytel.instruction(
    ["setname", "setbio"],
    outgoing=True,
)
async def _set_name_bio(
    client, message
):
    args = get_text(
        message, normal=True
    )
    if message.command[0] == "setbio":
        if len(args) >= 70:
            await eor(
                message,
                text="Max 70 Characters.",
            )
            return
        await client.update_profile(
            bio=args
        )
        text = f"✅ Success\nYour bio set to be: <code>{args}</code>"
        await eor(
            message,
            text=text,
        )
        return
    if message.command[0] == "setname":
        try:
            name = args.split(None, 1)
            first_name = name[0]
            last_name = name[1]
        except Exception:
            example = f"<b><u>Example:</b></u>\n<code>{random_prefixies(px)}setname first_name last_name</code>"
            await eor(
                message, text=example
            )
            return

        await client.update_profile(
            first_name=first_name,
            last_name=last_name,
        )
        text = f"""
✅ Success
<u>Your has been update</u>.
├ <b>First Name:</b> <code>{first_name}</code>
└ <b>Last Name:</b> <code>{last_name}</code>
"""
        await eor(
            message,
            text=text,
        )
        return


@pytel.instruction(
    ["mydialogs"],
    outgoing=True,
)
async def _my_dialogs(client, message):
    x = await eor(
        message, text="Please wait..."
    )
    u, g, sg, c, b, admin_chat = (
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adm = await client.get_me()
    async for dialog in client.get_dialogs():
        if (
            dialog.chat.type
            == enums.ChatType.PRIVATE
        ):
            u = u + 1
        elif (
            dialog.chat.type
            == enums.ChatType.BOT
        ):
            b = b + 1
        elif (
            dialog.chat.type
            == enums.ChatType.GROUP
        ):
            g = g + 1
        elif (
            dialog.chat.type
            == enums.ChatType.SUPERGROUP
        ):
            sg = sg + 1
            user_s = await dialog.chat.get_member(
                int(adm.id)
            )
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                admin_chat = (
                    admin_chat + 1
                )
        elif (
            dialog.chat.type
            == enums.ChatType.CHANNEL
        ):
            c = c + 1

    text = """
<b><u>DIALOGS STATISTICS</u></b>
 ├ <b>Private Messages:</b> {} Users and {} Bots.
 ├ <b>Are in:</b> {} Groups.
 ├ <b>Are in:</b> {} Super Groups.
 ├ <b>Are in:</b> {} Channels.
 └ <b>Admin in:</b> {} Chats.
"""
    with suppress(Exception):
        await eor(
            x,
            text=text.format(
                u,
                b,
                g,
                sg,
                c,
                admin_chat,
            ),
        )


@pytel.instruction(
    ["dlimit", "devlimit"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    [
        "limit",
        "limited",
    ],
    outgoing=True,
)
async def _limited(client, message):
    spambot = "@SpamBot"
    await client.unblock_user(spambot)
    x = await eor(
        message,
        text="Getting information...",
    )
    history = await client.resolve_peer(
        spambot
    )
    resp = await client.invoke(
        StartBot(
            bot=history,
            peer=history,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1.6)
    status = await client.get_messages(
        spambot,
        resp.updates[1].message.id + 1,
    )
    await eor(
        x,
        text=f"{status.text}",
    )
    return await client.invoke(
        DeleteHistory(
            peer=history,
            max_id=0,
            revoke=True,
        )
    )


@pytel.instruction(
    ["setpp", "setpfp"],
    outgoing=True,
)
async def _set_pfp(client, message):
    rp = message.reply_to_message
    text = "Successfuly updates ur profile photo."
    if not rp:
        await eor(
            message,
            text="Please reply to photos/video/sticker.",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    if rp.photo:
        file = (
            await client.download_media(
                rp.photo,
                file_name="cache/",
            )
        )
        try:
            await gather(
                client.set_profile_photo(
                    photo=file
                ),
                eor(x, text=text),
            )
            (Rooters / file).unlink(
                missing_ok=True
            )
            return
        except BaseException as excp:
            (Rooters / file).unlink(
                missing_ok=True
            )
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Exception: {excp}",
            )
            return

    elif rp.video:
        file = (
            await client.download_media(
                rp.video,
                file_name="cache/",
            )
        )
        try:
            await gather(
                client.set_profile_photo(
                    photo=file
                ),
                eor(x, text=text),
            )
            (Rooters / file).unlink(
                missing_ok=True
            )
            return
        except BaseException as excp:
            (Rooters / file).unlink(
                missing_ok=True
            )
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Exception: {excp}",
            )
            return

    elif (
        rp.sticker
        and rp.sticker.file_id
    ):
        file = (
            await client.download_media(
                rp.sticker.file_id,
                file_name="cache/",
            )
        )
        if file.endswith(
            ".webp"
        ) or file.endswith(".png"):
            img = Image.open(
                file
            ).convert("RGBA")
            img.save(
                "sticker.png",
                format="PNG",
                optimize=True,
            )
            conv = "sticker.png"
            with open(conv, "rb") as f:
                pp = f.read()
            file_io = BytesIO(pp)
            await gather(
                client.set_profile_photo(
                    photo=file_io
                ),
                eor(x, text=text),
            )
            (Rooters / file).unlink(
                missing_ok=True
            )
            (Rooters / conv).unlink(
                missing_ok=True
            )
            return

        else:
            await eor(
                message,
                text="Please reply to sticker ( type: .wepb )",
            )
            return

    elif (
        rp.document
        and "image"
        in rp.document.mime_type
        or "video"
        in rp.document.mime_type
    ):
        file = (
            await client.download_media(
                rp.document.file_id,
                file_name="cache/",
            )
        )
        with open(file, "rb") as f:
            pp = f.read()
        file_io = BytesIO(pp)
        try:
            await gather(
                client.set_profile_photo(
                    photo=file_io
                ),
                eor(x, text=text),
            )
            (Rooters / file).unlink(
                missing_ok=True
            )
            return
        except BaseException as excp:
            (Rooters / file).unlink(
                missing_ok=True
            )
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Exception: {excp}",
            )
            return

    else:
        await eor(
            message,
            text="Please reply to photos/video/sticker.",
        )
        return


@pytel.instruction(
    [
        "rempfp",
        "rempp",
    ],
    outgoing=True,
)
async def _rempfp(client, message):
    msg = get_args(message, normal=True)
    if msg == "all":
        limit = 0
    elif msg.isdigit():
        limit = int(msg)
    else:
        limit = 1

    count = 0
    x = await eor(
        message,
        text=f"Removing {msg} profile photo...",
    )
    async for photos in client.get_chat_photos(
        "me", limit=limit
    ):
        try:
            await client.delete_profile_photos(
                photos.file_id
            )
            count = count + 1
        except Exception as excp:
            client.send_log.exception(
                excp
            )
            await eor(
                x,
                text=f"Error: ```{excp}```",
            )
            return

    text = "Successfuly removing {} profile photo."
    await eor(
        x,
        text=text.format(
            count,
        ),
    )
    return


@pytel.instruction(
    ["dblock"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    [
        "block",
        "blocked",
        "unblocked",
        "unblock",
    ],
    outgoing=True,
)
async def _blocked(client, message):
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
            text="It's urself.",
        )
        return
    elif user_id in list(_supersu):
        await eor(
            x,
            text="That's My Developer.",
        )
        return

    mention = (
        await client.get_users(user_id)
    ).mention
    user_info = (
        await client.resolve_peer(
            user_id
        )
    )
    x = await eor(
        x,
        text="Blocking user...",
    )
    try:
        if (
            message.command[0]
            == "block"
            or "blocked"
            or "dblock"
        ):
            await client.invoke(
                functions.contacts.Block(
                    id=user_info
                ),
            )
            await eor(
                x,
                text=f"{mention} has been blocked.",
            )
            return
        elif (
            message.command[0][0] == "u"
        ):
            await client.unblock_user(
                user_id
            )
            await eor(
                x,
                text=f"{mention} has been unblocked.",
            )
            return
    except BaseException as excp:
        await eor(
            x, text=f"Exception: {excp}"
        )
        return


plugins_helper["account"] = {
    f"{random_prefixies(px)}block / blocked [id/username/reply to user]": "To blocked users.",
    f"{random_prefixies(px)}unblock / unblocked [id/username/reply to user]": "To unblocked users.",
    f"{random_prefixies(px)}limit / limited": "To check ur account is limited or not.",
    f"{random_prefixies(px)}mydialogs": "To get my dialogue statistics.",
    f"{random_prefixies(px)}setmode [offline/online/off/on]": "To setting ur status to be Online or Offline.",
    f"{random_prefixies(px)}setbio [text/reply]": "To updates ur bio. ( Max 70 characters )",
    f"{random_prefixies(px)}setname [first name] [last name]": "To updates ur name.",
    f"{random_prefixies(px)}setpfp / setpp [reply photo/video/sticker]": "To updates ur profile photo.",
    f"{random_prefixies(px)}rempfp [count: integer/all]": "To removing profile photo.",
}
