"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >
"""
from asyncio import (
    set_event_loop,
    sleep,
    Lock,
    AbstractEventLoop,)
from contextlib import suppress
from datetime import datetime
from html import escape
from sys import exc_info, exit
from time import time
from traceback import format_exc as fmex
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Union,)
from pyrogram import (
    Client as Raw,
    __version__,
    filters,
    ContinuePropagation,
    StopPropagation,)
from pyrogram.enums import (
    ChatMemberStatus,
    ChatType,
    ParseMode,)
from pyrogram.errors.exceptions.bad_request_400 import (
    ChannelInvalid,
    MessageIdInvalid,
    MessageNotModified,
    PersistentTimestampInvalid,
    BotMethodInvalid,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,)
from pyrogram.errors.exceptions.forbidden_403 import (
    ChatWriteForbidden,)
from pyrogram.errors.exceptions.internal_server_error_500 import (
    PersistentTimestampOutdated,)
from pyrogram.filters import Filter
from pyrogram.handlers import (
    MessageHandler,
    EditedMessageHandler,)
from pyrogram.raw.all import layer
from pyrogram.raw.functions.channels import (
    GetFullChannel,)
from pyrogram.raw.functions.messages import (
    GetFullChat,)
from pyrogram.raw.functions.phone import (
    GetGroupCall,
    GetGroupParticipants,
    EditGroupCallParticipant,)
from pyrogram.raw.types import (
    InputGroupCall,
    InputPeerChannel,
    InputPeerChat,)
from pyrogram.types import Message
from pytelibs import (
    _c,
    _d,
    _g,
    _l,
    _supersu,
    cpytl,
    replace_all,
    _CHARACTER_NAMES,)
from pytgcalls.group_call_factory import (
    GroupCallFactory,)
from pytgcalls.mtproto_client_type import (
    MTProtoClientType,)
from .. import loopers
from ..config import (
    LOGCHAT_ID,
    PREFIX,
    OWNER_ID,)
from ..logger import pylog
from .dbase import memorize
from .dbase.dbLogger import (
    already_logger,
    check_logger,)
from .leverage import legally_required
from .utils import (
    RunningCommand,
    get_blacklisted,
    gg_restricted,
    mentioned,
    progress,
    tz,)


class PytelClient(Raw):
    """
    Client :: PYTEL
    """

    client: Any
    _client: list
    lock: Any
    loop: Optional[AbstractEventLoop]
    send_log: Any
    group_call: Any

    def __init__(
        self,
        api_id: Union[int, str] = None,
        api_hash: Optional[str] = None,
        session_string: Optional[
            str
        ] = None,
        lang_code: Optional[str] = None,
        in_memory: Optional[
            bool
        ] = None,
        ipv6: Optional[bool] = None,
        app_version: Optional[
            str
        ] = None,
        no_updates: Optional[
            bool
        ] = None,
        sleep_threshold: Optional[
            int
        ] = None,
        workers: Any = None,
        system_version: Any = None,
        device_model: Any = None,
        *args,
        **kwargs: Any,
    ):
        kwargs["api_id"] = api_id
        kwargs["api_hash"] = api_hash
        kwargs[
            "session_string"
        ] = session_string
        kwargs[
            "app_version"
        ] = app_version
        kwargs["workers"] = workers
        kwargs[
            "system_version"
        ] = system_version
        kwargs[
            "device_model"
        ] = device_model
        kwargs[
            "lang_code"
        ] = lang_code.lower()
        kwargs["in_memory"] = in_memory
        kwargs["ipv6"] = ipv6
        kwargs[
            "no_updates"
        ] = no_updates
        kwargs[
            "sleep_threshold"
        ] = sleep_threshold

        self.client = Raw
        self._client = []
        self.send_log = pylog
        self.lock = Lock
        self.loop = set_event_loop(
            loopers
        )
        self.listening = {}
        self.group_call = GroupCallFactory(
            self,
            MTProtoClientType.PYROGRAM,
            enable_logs_to_console=False,
            path_to_log_file="",
        ).get_file_group_call(
            input_filename="",
            play_on_repeat=False,
        )
        super().__init__(
            *args, **kwargs
        )

    def instruction(
        self,
        command: Union[
            str,
            List[str],
        ] = None,
        supergroups: Union[
            bool, bool
        ] = False,
        outgoing: Union[
            bool, bool
        ] = False,
        admin_only: Union[
            bool, bool
        ] = False,
        privileges: Callable[
            ..., Any
        ] = None,
        disable_errors: Union[
            bool, bool
        ] = False,
        handler: Union[
            str,
            List[str],
        ] = None,
        filt: Union[
            Filter,
            Filter,
        ] = None,
        supersu: Callable[
            ..., Any
        ] = None,
        force_edit: Optional[
            bool
        ] = True,
        sensitive: Optional[
            bool
        ] = True,
        group: Optional[int] = None,
        *args,
        **kwargs,
    ) -> Callable:
        group = 0
        if command:
            command = [
                x
                if sensitive
                else x.lower()
                for x in command
            ]
        if handler is None:
            handler = (
                PREFIX
                if PREFIX
                else "."
            )
        if privileges is None:
            privileges = []
        if supersu is None:
            supersu = []
        if "PYTEL" in supersu:
            filt = (
                legally_required
                & filters.command(
                    command,
                    prefixes=handler,
                )
            )
        if outgoing:
            filt = (
                filters.command(
                    command,
                    prefixes=handler,
                )
                & filters.me
            )

        @memorize
        def decorator(
            func: Callable,
        ) -> Callable:
            async def wrapper(
                client: PytelClient,
                message: Message,
            ) -> Callable:
                user_id = client.me.id
                if (
                    already_logger(
                        user_id=user_id
                    )
                    and not LOGCHAT_ID
                ):
                    log_data = check_logger().get(
                        user_id
                    )
                    log_id = log_data[0]
                    send_to = int(
                        log_id
                    )
                elif LOGCHAT_ID:
                    send_to = int(
                        LOGCHAT_ID
                    )
                else:
                    send_to = None

                if admin_only:
                    with suppress(
                        Exception,
                        ValueError,
                    ):
                        me = await client.get_chat_member(
                            message.chat.id,
                            (
                                await client.get_me()
                            ).id,
                        )
                        if (
                            message.chat.type
                            != ChatType.SUPERGROUP
                        ):
                            await message.reply(
                                "This command can be used in supergroups only."
                            )
                            return
                        if (
                            me.status
                            not in (
                                ChatMemberStatus.OWNER,
                                ChatMemberStatus.ADMINISTRATOR,
                            )
                        ):
                            await message.reply(
                                "I must be admin to execute this Command"
                            )
                            return

                # escape suppress
                if (
                    "can_restricted"
                    in privileges
                ):
                    with suppress(
                        Exception,
                        ValueError,
                    ):
                        me = await client.get_chat_member(
                            message.chat.id,
                            (
                                await client.get_me()
                            ).id,
                        )
                        if (
                            me.status
                            not in (
                                ChatMemberStatus.OWNER,
                                ChatMemberStatus.ADMINISTRATOR,
                            )
                        ):
                            await message.reply(
                                "I don't have the privilege to restricting people."
                            )
                            return
                        else:
                            if (
                                me.privileges.can_restrict_members
                            ):  # for admins
                                pass
                            else:
                                await message.reply(
                                    "I don't have the privilege to restricting people."
                                )
                                return
                if (
                    "can_pinned"
                    in privileges
                ):
                    with suppress(
                        Exception,
                        ValueError,
                    ):
                        me = await client.get_chat_member(
                            message.chat.id,
                            (
                                await client.get_me()
                            ).id,
                        )
                        if (
                            not me.privileges.can_pin_messages
                        ):
                            await message.reply(
                                "I don't have the privilege to pinned messages."
                            )
                            return

                if (
                    "can_manage_video_chats"
                    in privileges
                ):
                    with suppress(
                        Exception,
                        ValueError,
                    ):
                        me = await client.get_chat_member(
                            message.chat.id,
                            (
                                await client.get_me()
                            ).id,
                        )
                        if (
                            not me.privileges.can_manage_video_chats
                        ):
                            await message.reply(
                                "I don't have the privilege to access video chats."
                            )
                            return

                if (
                    "can_send_media_messages"
                    in privileges
                ):
                    with suppress(
                        Exception,
                        ValueError,
                    ):
                        me = await client.get_chat_member(
                            message.chat.id,
                            (
                                await client.get_me()
                            ).id,
                        )
                        if (
                            me.privileges
                        ):  # for admins
                            pass
                        else:
                            perm = (
                                await client.get_chat(
                                    message.chat.id,
                                )
                            ).permissions
                            if (
                                not perm.can_send_media_messages
                            ):
                                await message.reply(
                                    "<u>Chat Send Media Forbidden</u> in this Group."
                                )
                                return

                if (
                    "can_promote_members"
                    in privileges
                ):
                    with suppress(
                        Exception,
                        ValueError,
                    ):
                        me = await client.get_chat_member(
                            message.chat.id,
                            (
                                await client.get_me()
                            ).id,
                        )
                        if (
                            me.status
                            not in (
                                ChatMemberStatus.OWNER,
                                ChatMemberStatus.ADMINISTRATOR,
                            )
                        ):
                            await message.reply(
                                "I don't have the privilege to promoting people."
                            )
                            return
                        else:
                            if (
                                me.privileges.can_promote_members
                            ):  # for admins
                                pass
                            else:
                                await message.reply(
                                    "I don't have the privilege to promoting people."
                                )
                                return

                if (
                    "can_invite_users"
                    in privileges
                ):
                    with suppress(
                        Exception,
                        ValueError,
                    ):
                        me = await client.get_chat_member(
                            message.chat.id,
                            (
                                await client.get_me()
                            ).id,
                        )
                        if (
                            me.privileges
                        ):  # for admins
                            pass
                        else:
                            perm = (
                                await client.get_chat(
                                    message.chat.id,
                                )
                            ).permissions
                            if (
                                not perm.can_invite_users
                            ):
                                await message.reply(
                                    "<u>Can't invite users</u> in here."
                                )
                                return

                if (
                    supergroups
                    and message.chat.type
                    not in [
                        ChatType.SUPERGROUP,
                        ChatType.CHANNEL,
                    ]
                ):
                    await message.reply(
                        "This command can be used in supergroups only."
                    )
                    return

                try:
                    await func(
                        client,
                        message,
                    )
                except OSError:
                    try:
                        await client.connect()  # send connection
                        await func(
                            client,
                            message,
                        )
                    except (
                        BaseException
                    ):
                        pass
                except (
                    FloodWait
                ) as excp:
                    await sleep(
                        excp.value + 10
                    )
                    await func(
                        client,
                        message,
                    )
                except MessageIdInvalid:
                    await message.reply(
                        "Message command not found. Please don't delete the command message."
                    )
                    return
                except (
                    ChannelInvalid,
                    MessageNotModified,
                    PersistentTimestampInvalid,
                    PersistentTimestampOutdated,
                    TimeoutError,
                    ChatWriteForbidden,
                ):
                    pass
                except StopPropagation:
                    raise StopPropagation
                except (
                    ContinuePropagation
                ):
                    raise ContinuePropagation
                except (
                    Exception
                ) as excp:
                    if (
                        not disable_errors
                    ):
                        client.send_log.error(
                            excp
                        )
                        date = datetime.now(
                            tz
                        ).strftime(
                            "%d %B, %Y - %H:%M:%S"
                        )
                        format_text = "<code>====</code> ⚠️ <u>Attention</u> ⚠️ <code>====</code>"
                        format_text += "\nPytel is having Problems."
                        format_text += "\n( <u>Please report issue to</u> @kastaot )"
                        format_text += (
                            "\n\n<b>⏰ Datetime:</b> <code>"
                            + date
                            + "</code>"
                        )
                        format_text += "\n\n<b>Evidence ⬇️ </b>"
                        format_text += f"\n\n👤 User: {await mentioned(client, user_id=user_id, use_html=True)}"
                        format_text += f"\n👥 Group Name: {message.chat.title}"
                        format_text += f"\n🔎 Group ID: <code>{message.chat.id}</code>"
                        format_text += (
                            "\n\n<b>🖐🏻 Event Trigger:</b> <code>"
                            + str(
                                message.text
                            )
                            + "</code>"
                        )
                        format_text += (
                            "\n\n<b>🚨 Traceback:</b> <code>"
                            + str(
                                fmex()
                            )
                            + "</code>"
                        )
                        format_text += (
                            "\n\n<b>🚨 Crux of the matter ( Issue ) :</b> <code>"
                            + str(
                                exc_info()[
                                    1
                                ]
                            )
                            + "</code>"
                        )
                        format_text += "\n\n<code>======</code> <u>History Commit</u> <code>======</code>"
                        format_text += "\n\n<b>Last 3 Commit:</b> \n"
                        (
                            stdout,
                            stderr,
                        ) = RunningCommand(
                            'git log --pretty=format:"%an: %s" -3'
                        )
                        result = str(
                            stdout
                        ) + str(stderr)
                        format_text += (
                            "<code>"
                            + str(
                                result
                            )
                            + "</code>"
                        )
                        with suppress(
                            MessageIdInvalid
                        ):
                            if send_to:
                                from pytel import (
                                    pytel_tgb,)

                                await pytel_tgb.send_message(
                                    int(
                                        send_to
                                    ),
                                    text=format_text,
                                    parse_mode=ParseMode.HTML,
                                    disable_notification=False,
                                )
                                await sleep(
                                    1
                                )
                                await pytel_tgb.send_message(
                                    int(
                                        OWNER_ID
                                    ),
                                    text=format_text,
                                    parse_mode=ParseMode.HTML,
                                    disable_notification=False,
                                )

                message.continue_propagation()

            for _ in self._client:
                try:
                    if force_edit:
                        _.add_handler(
                            EditedMessageHandler(
                                callback=wrapper,
                                filters=filt,
                            ),
                            group=group,
                        )

                    _.add_handler(
                        MessageHandler(
                            callback=wrapper,
                            filters=filt,
                        ),
                        group=group,
                    )
                except (
                    BaseException
                ) as excp:
                    pylog.exception(
                        f"Error: {excp}"
                    )

            return wrapper

        return decorator

    async def user_fullname(
        self,
        user_id: Optional[int],
    ) -> Optional[str]:
        separator: str = ""
        user = await self.get_users(
            user_id
        )
        fname = (
            hasattr(user, "last_name")
            and user.last_name
            and f"{separator}{user.first_name} {user.last_name}"
            or f"{separator}{user.first_name}"
        )
        fullname = " ".join(
            replace_all(
                escape(fname),
                _CHARACTER_NAMES,
            ).split()
        )
        return fullname

    async def username(
        self,
        user_id: Optional[int],
    ) -> Optional[str]:
        user = await self.get_users(
            user_id
        )
        if user.username:
            return str(user.username)

    async def notify_login(
        self,
    ):
        with suppress(Exception):
            x = await self.user_fullname(
                user_id=self.me.id
            )
            self.send_log.success(
                f"Started on {x}"
            )
            self.send_log.info(
                f"Preparing plugins for {x}"
            )

    async def _copyright(
        self,
        _copyright: Optional[
            str
        ] = None,
        _license: Optional[str] = None,
    ) -> None:
        """
        Copyright, All Rights Reserved.
        """
        gg_restricted()
        _lc = _license
        _cpr = _copyright
        self.send_log.info(
            f"{self.app_version}"
        )
        self.send_log.info(
            f"Pyrogram v.{__version__} (Layer {layer})"
        )
        self.send_log.info(
            f"{_cpr}",
            f"Lincense under : {_lc}",
        )

    async def flash(
        self,
    ):
        if self not in self._client:
            self._client.append(self)
        try:
            await self.join_chat(_c)
            await sleep(5)
            await self.join_chat(_g)
            await sleep(5)
            await self.join_chat(_l)
            await sleep(5)
            await self.join_chat(_d)
            await sleep(5)
            await self.join_chat(cpytl)
        except BotMethodInvalid:
            pass
        except KeyError:
            pass
        except Exception as excp:
            self.send_log.exception(
                f"Exception : {excp}"
            )

    async def client_started(
        self,
    ):
        if self not in self._client:
            self._client.append(self)
        try:
            self.send_log.info(
                "🚀 Starting-up Client."
            )
            await super().start()
            if self.me.id not in list(
                _supersu
            ):
                KASTA_BLACKLIST = await get_blacklisted(
                    url="https://raw.githubusercontent.com/kastaid/resources/main/kastablacklist.py",
                    attempts=6,
                    fallbacks=None,
                )
                if (
                    self.me.id
                    in KASTA_BLACKLIST
                ):
                    self.send_log.warning(
                        "({} - {}) YOU ARE BLACKLISTED !!".format(
                            self.me.first_name,
                            self.me.id,
                        )
                    )
                    await self.stop()
                    exit(1)
            self.send_log.success(
                f"☑️ Successfuly, ur has been login."
            )
        except FloodWait as excp:
            await sleep(excp.value + 5)
            await super().start()
        except Exception as excp:
            self.send_log.exception(
                excp
            )

    async def downloads_media(
        self,
        message: Message,
        m: Any,
        x: Any,
    ):
        from pytel import Rooters

        caption = (
            m.caption
            or m.caption_entities
            or None
        )
        with suppress(Exception):
            if (m.text) or (m.sticker):
                await m.copy(
                    message.chat.id,
                    reply_to_message_id=message.id,
                )
            s_time = time()
            if m.photo:
                photo = await self.download_media(
                    m.photo,
                    "/cache",
                    progress=progress,
                    progress_args=(
                        x,
                        s_time,
                        "`Downloading File!`",
                        "Telegram Photo",
                    ),
                )
                u_time = time()
                await self.send_photo(
                    message.chat.id,
                    photo=photo,
                    caption=caption,
                    reply_to_message_id=message.id,
                    progress=progress,
                    progress_args=(
                        x,
                        u_time,
                        "`Uploading File!`",
                        "Telegram Photo",
                    ),
                )
                (
                    Rooters / photo
                ).unlink(
                    missing_ok=True
                )
            if m.video:
                video = await self.download_media(
                    m.video,
                    "/cache",
                    progress=progress,
                    progress_args=(
                        x,
                        s_time,
                        "`Downloading File!`",
                        "Telegram Video",
                    ),
                )
                u_time = time()
                await self.send_video(
                    message.chat.id,
                    video=video,
                    caption=caption,
                    supports_streaming=True,
                    reply_to_message_id=message.id,
                    progress=progress,
                    progress_args=(
                        x,
                        u_time,
                        "`Uploading File!`",
                        "Telegram Video",
                    ),
                )
                (
                    Rooters / video
                ).unlink(
                    missing_ok=True
                )
            if m.document:
                file = await self.download_media(
                    m.document,
                    "/cache",
                    progress=progress,
                    progress_args=(
                        x,
                        s_time,
                        "`Downloading File!`",
                        "Telegram Document",
                    ),
                )
                u_time = time()
                await self.send_document(
                    message.chat.id,
                    document=file,
                    caption=caption,
                    force_document=True,
                    reply_to_message_id=message.id,
                    progress=progress,
                    progress_args=(
                        x,
                        u_time,
                        "`Uploading File!`",
                        "Telegram Document",
                    ),
                )
                (Rooters / file).unlink(
                    missing_ok=True
                )
            if m.audio:
                audio = await self.download_media(
                    m.audio,
                    "/cache",
                    progress=progress,
                    progress_args=(
                        x,
                        s_time,
                        "`Downloading File!`",
                        "Telegram Audio",
                    ),
                )
                u_time = time()
                await self.send_audio(
                    message.chat.id,
                    audio,
                    caption,
                    reply_to_message_id=message.id,
                    progress=progress,
                    progress_args=(
                        x,
                        u_time,
                        "`Uploading File!`",
                        "Telegram Audio",
                    ),
                )
                (
                    Rooters / audio
                ).unlink(
                    missing_ok=True
                )
            if m.voice:
                voice = await self.download_media(
                    m.voice,
                    "/cache",
                    progress=progress,
                    progress_args=(
                        x,
                        s_time,
                        "`Downloading File!`",
                        "Telegram Voice",
                    ),
                )
                u_time = time()
                await self.send_voice(
                    message.chat.id,
                    voice,
                    caption,
                    reply_to_message_id=message.id,
                    progress_args=(
                        x,
                        u_time,
                        "`Uploading File!`",
                        "Telegram Voice",
                    ),
                )
                (
                    Rooters / voice
                ).unlink(
                    missing_ok=True
                )
            if m.animation:
                animation = await self.download_media(
                    m.animation,
                    "/cache",
                    progress=progress,
                    progress_args=(
                        x,
                        s_time,
                        "`Downloading File!`",
                        "Telegram Animation",
                    ),
                )
                u_time = time()
                await self.send_animation(
                    message.chat.id,
                    animation,
                    caption,
                    reply_to_message_id=message.id,
                    progress=progress,
                    progress_args=(
                        x,
                        u_time,
                        "`Uploading File!`",
                        "Telegram Animation",
                    ),
                )
                (
                    Rooters / animation
                ).unlink(
                    missing_ok=True
                )

    async def get_group_call(
        self,
        message,
        chat_ids: Any = None,
    ) -> Optional[InputGroupCall]:
        if chat_ids:
            chat_id = chat_ids
        else:
            chat_id = message.chat.id
        chat_peer = (
            await self.resolve_peer(
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
                chat_peer,
                InputPeerChannel,
            ):
                full_chat = (
                    await self.invoke(
                        GetFullChannel(
                            channel=chat_peer
                        )
                    )
                ).full_chat
            elif isinstance(
                chat_peer, InputPeerChat
            ):
                full_chat = (
                    await self.invoke(
                        GetFullChat(
                            chat_id=chat_peer.chat_id
                        )
                    )
                ).full_chat
            if full_chat is not None:
                return full_chat.call
        return False

    async def muting_user_vc(
        self,
        group_call: Any,
        participant: Any,
        muted: bool,
    ) -> EditGroupCallParticipant:
        mtd = await self.invoke(
            EditGroupCallParticipant(
                call=group_call,
                participant=participant,
                muted=muted,
            ),
        )
        return mtd

    async def get_partici(
        self, group_call: Any
    ) -> GetGroupParticipants:
        par = await self.invoke(
            GetGroupParticipants(
                call=group_call,
                ids=[],
                sources=[],
                offset="",
                limit=500,
            ),
        )
        return par

    async def get_resvc(
        self, group_call: Any
    ) -> GetGroupCall:
        res = await self.invoke(
            GetGroupCall(
                call=group_call,
                limit=500,
            ),
        )
        return res

    async def stop(self, *args):
        if self not in self._client:
            self._client.append(self)
        try:
            await super().stop()
        except Exception as excp:
            self.send_log.exception(
                excp
            )
