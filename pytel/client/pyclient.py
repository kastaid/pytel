# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from contextlib import suppress
from datetime import datetime
from sys import exc_info
from traceback import format_exc as fmex
from typing import (
    Any,
    Optional,
    Union,
    Callable,
    Coroutine,
    List,
)
from pyrogram import Client, __version__, filters
from pyrogram.enums import ParseMode, ChatMemberStatus, ChatType
from pyrogram.filters import Filter
from pyrogram.handlers import MessageHandler
from pyrogram.raw.all import layer
from pyrogram.types import Message
from version import __version__ as versi
from .. import loopers
from ..config import PREFIX, LOGCHAT_ID
from ..logger import pylog as send_log
from .dbase.dbLogger import already_logger, check_logger
from .utils import (
    RunningCommand,
    _c,
    _g,
    _l,
    _d,
    tz,
)


class PytelClient(Client):
    _client = []

    def __init__(
        self,
        api_id: Union[int, str] = None,
        api_hash: Optional[str] = None,
        session_string: Optional[str] = None,
        lang_code: Optional[str] = None,
        in_memory: Optional[bool] = None,
        ipv6: Optional[bool] = None,
        *args,
        **kwargs,
    ):
        kwargs["api_id"] = api_id
        kwargs["api_hash"] = api_hash
        kwargs["session_string"] = session_string
        kwargs["lang_code"] = "en"
        kwargs["in_memory"] = True
        kwargs["ipv6"] = False

        super().__init__(**kwargs)
        with suppress(BaseException):
            from pytgcalls import GroupCallFactory
        self.group_call = GroupCallFactory(self).get_group_call()
        self.send_log = send_log
        self.loop = loopers

    def instruction(
        self,
        command: Union[str, List[str]],
        group_only: Union[bool, bool] = False,
        outgoing: Union[bool, bool] = False,
        self_admin: Union[bool, bool] = False,
        disable_errors: Union[bool, bool] = False,
        handler: Union[str, List[str]] = None,
        filt: Union[Filter, Filter] = None,
        group: Optional[int] = 0,
        *args,
        **kwargs,
    ) -> Callable:
        if handler is None:
            handler = PREFIX if PREFIX else "."
        if filt:
            if outgoing:
                filt = filters.command(command, prefixes=handler) & filt & filters.me
            else:
                filt = filters.command(command, prefixes=handler) & filt & filters.me
        else:
            if outgoing:
                filt = filters.command(command, prefixes=handler) & filters.me
            else:
                filt = filters.command(command, prefixes=handler)

        def decorator(func: Callable) -> Callable:
            async def wrapper(client: Client, message: Message):
                user = await client.get_me()
                user_id = user.id
                if already_logger(user_id=user_id) and not LOGCHAT_ID:
                    log_data = check_logger().get(user_id)
                    log_id = log_data[0]
                    send_to = int(log_id)
                elif LOGCHAT_ID:
                    send_to = int(LOGCHAT_ID)
                else:
                    send_to = None
                if self_admin and message.chat.type != ChatType.SUPERGROUP:
                    return await message.edit("This command can be used in supergroups only.")
                if self_admin:
                    me = await client.get_chat_member(message.chat.id, (await client.get_me()).id)
                    if me.status not in (
                        ChatMemberStatus.OWNER,
                        ChatMemberStatus.ADMINISTRATOR,
                    ):
                        return await message.edit("I must be admin to execute this Command")
                if group_only and message.chat.type != ChatType.SUPERGROUP:
                    return await message.edit("This command can be used in supergroups only.")
                try:
                    await func(client, message)
                except Exception as excp:
                    if not disable_errors:
                        send_log.error(excp)
                        date = datetime.now(tz).strftime("%d/%m/%Y %I:%M:%S %p")
                        format_text = "<code>====</code> ⚠️ <u>Attention</u> ⚠️ <code>====</code>"
                        format_text += "\nPytel is having Problems."
                        format_text += "\n( <u>Please report issue to</u> @kastaot )"
                        format_text += "\n\n<b>• Datetime:</b> <code>" + date + "</code>"
                        format_text += "\n\n<b>Evidence ⬇️ </b>"
                        format_text += "\n\n<b>🚨 Event Trigger:</b> <code>" + str(message.text) + "</code>"
                        format_text += "\n\n<b>🚨 Traceback:</b> <code>" + str(fmex()) + "</code>"
                        format_text += "\n\n<b>🚨 Error text:</b> <code>" + str(exc_info()[1]) + "</code>"
                        format_text += "\n\n<code>======</code> <u>History Commit</u> <code>======</code>"
                        format_text += "\n\n<b>Last 5 Commit:</b> \n"
                        stdout, stderr = RunningCommand('git log --pretty=format:"%an: %s" -3')
                        result = str(stdout) + str(stderr)
                        format_text += "<code>" + str(result) + "</code>"
                        with suppress(BaseException):
                            if send_to:
                                respond_text = (
                                    "Sorry, <b>Pytel</b> has been crashed."
                                    "\nThe error logs are send in ur <b><u>Logger Chat</b></u>."
                                )
                                await message.edit(respond_text)
                                await client.send_message(
                                    int(send_to),
                                    format_text,
                                    parse_mode=ParseMode.HTML,
                                    disable_notification=True,
                                )
                            else:
                                respond_text = (
                                    "Sorry, <b>Pytel</b> has been crashed."
                                    "\nThe error logs are send in ur <b><u>Save Messages</b></u>."
                                )
                                await message.edit(respond_text)
                                await client.send_message(
                                    "self",
                                    format_text,
                                    parse_mode=ParseMode.HTML,
                                    disable_notification=True,
                                )

            for _ in self._client:
                _.add_handler(MessageHandler(callback=wrapper, filters=filt), group)
            return wrapper

        return decorator

    def run_in_loop(self, func: Coroutine[Any, Any, None]) -> Any:
        return self.loop.run_until_complete(func)

    async def notify_login(self):
        try:
            self._me = await self.get_me()
            _fn = self._me.first_name if self._me.first_name else "ㅤ"
            _ln = self._me.last_name if self._me.last_name else "ㅤ"
            self.send_log.success(f"Successfuly, ur has been login.")
            self.send_log.success(f"Started on {_fn}{_ln}")
        except BaseException as excp:
            self.send_log.exception(f"Error : {excp}")

    def _copyright(self, _copyright: Optional[str] = None, _license: Optional[str] = None) -> None:
        """
        Copyright, All Rights Reserved.
        """
        _lc = _license
        _cpr = _copyright
        self.send_log.info(f"PYTEL v.{versi}")
        self.send_log.info(f"Pyrogram v.{__version__} (Layer {layer})")
        self.send_log.info(
            f"{_cpr}",
            f"Lincense under : {_lc}",
        )

    async def flash(self):
        try:
            await self.join_chat(_c)
            await sleep(5)
            await self.join_chat(_g)
            await sleep(5)
            await self.join_chat(_l)
            await sleep(5)
            await self.join_chat(_d)
        except Exception as excp:
            self.send_log.exception(f"Exception : {excp}")

    async def start(self):
        await super().start()
        if self not in self._client:
            self._client.append(self)

    async def stop(self, *args):
        await super().stop()
        if self not in self._client:
            self._client.append(self)
