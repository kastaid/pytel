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
from sys import exc_info, exit
from traceback import format_exc as fmex
from typing import (
    Any,
    Callable,
    Coroutine,
    List,
    Optional,
    Union,)
from pyrogram import (
    Client as Raw,
    __version__,
    filters,
    StopPropagation,)
from pyrogram.enums import (
    ChatMemberStatus,
    ChatType,
    ParseMode,)
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    PersistentTimestampInvalid,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,)
from pyrogram.filters import Filter
from pyrogram.handlers import (
    MessageHandler,
    EditedMessageHandler,)
from pyrogram.raw.all import layer
from pyrogram.types import Message
from pytelibs import (
    _c,
    _d,
    _g,
    _l,
    _supersu,
    cpytl,)
from pytgcalls.group_call_factory import (
    GroupCallFactory,)
from pytgcalls.mtproto_client_type import (
    MTProtoClientType,)
from .. import loopers
from ..config import LOGCHAT_ID, PREFIX
from ..logger import pylog
from .dbase.dbLogger import (
    already_logger,
    check_logger,)
from .leverage import legally_required
from .utils import (
    RunningCommand,
    get_blacklisted,
    gg_restricted,
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
            path_to_log_file=None,
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
        is_antipm: Union[
            bool, bool
        ] = None,
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
        group = -1
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
        if is_antipm:
            filt = (
                filters.private
                & ~filters.me
                & ~filters.bot
            )

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

                if (
                    "can_restricted"
                    in privileges
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
                            "I don't have the privilege to access video chats.."
                        )
                        return

                if (
                    "can_send_media_messages"
                    in privileges
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
                    "can_invite_users"
                    in privileges
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
                except (
                    TimeoutError,
                    PersistentTimestampInvalid,
                ):
                    pass
                except StopPropagation:
                    raise StopPropagation
                except (
                    FloodWait
                ) as excp:
                    await sleep(
                        excp.value + 5
                    )
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
                            "%d/%m/%Y %I:%M:%S %p"
                        )
                        format_text = "<code>====</code> ⚠️ <u>Attention</u> ⚠️ <code>====</code>"
                        format_text += "\nPytel is having Problems."
                        format_text += "\n( <u>Please report issue to</u> @kastaot )"
                        format_text += (
                            "\n\n<b>• Datetime:</b> <code>"
                            + date
                            + "</code>"
                        )
                        format_text += "\n\n<b>Evidence ⬇️ </b>"
                        format_text += (
                            "\n\n<b>🚨 Event Trigger:</b> <code>"
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
                            "\n\n<b>🚨 Error text:</b> <code>"
                            + str(
                                exc_info()[
                                    1
                                ]
                            )
                            + "</code>"
                        )
                        format_text += "\n\n<code>======</code> <u>History Commit</u> <code>======</code>"
                        format_text += "\n\n<b>Last 4 Commit:</b> \n"
                        (
                            stdout,
                            stderr,
                        ) = RunningCommand(
                            'git log --pretty=format:"%an: %s" -4'
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

            for _ in self._client:
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
            return wrapper

        return decorator

    async def user_fullname(
        self,
        user_id: Optional[int],
    ) -> Optional[str]:
        user = await self.get_users(
            user_id
        )
        first_n = (
            user.first_name
            if user.first_name
            else "ㅤ"  # blank-font
        )
        last_n = (
            user.last_name
            if user.last_name
            else "ㅤ"  # blank-font
        )
        full_name = first_n + last_n
        return str(full_name)

    async def username(
        self,
        user_id: Optional[int],
    ) -> Optional[str]:
        user = await self.get_users(
            user_id
        )
        if user.username:
            return str(user.username)

    def run_in_loop(
        self,
        catch: Coroutine[
            Any,
            Any,
            None,
        ],
    ) -> Any:
        return self.loop.run_until_complete(
            catch
        )

    async def notify_login(
        self,
    ):
        x = await self.user_fullname(
            user_id=self.me.id
        )
        self.send_log.success(
            f"Started on {x}"
        )

    def _copyright(
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
                "Starting-up Client."
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
                f"Successfuly, ur has been login."
            )
        except FloodWait as excp:
            await sleep(excp.value + 5)
            await super().start()
        except Exception as excp:
            self.send_log.exception(
                excp
            )

    async def stop(self, *args):
        if self not in self._client:
            self._client.append(self)
        try:
            await super().stop()
        except Exception as excp:
            self.send_log.exception(
                excp
            )
