# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import get_event_loop, sleep
from random import choice
from typing import (
    Optional,
    NoReturn,
    Any,
    Union,
    Coroutine,
    Callable,
)
from pyrogram import Client, __version__, filters
from pyrogram.handlers import MessageHandler
from pytgcalls import GroupCallFactory
from .logger import send_log


class Pytel(Client):
    def __init__(
        self,
        name: Optional[str] = None,
        api_id: Union[int, str] = None,
        api_hash: Optional[str] = None,
        bot_token: Optional[str] = None,
        lang_code: Optional[str] = None,
        in_memory: Optional[bool] = None,
        ipv6: Optional[bool] = None,
        *args,
        **kwargs,
    ):
        kwargs["name"] = name
        kwargs["api_id"] = api_id
        kwargs["api_hash"] = api_hash
        kwargs["bot_token"] = bot_token
        kwargs["lang_code"] = lang_code
        kwargs["in_memory"] = in_memory
        kwargs["ipv6"] = ipv6

        super().__init__()
        self.send_log = send_log
        self.loop = get_event_loop()

    async def start_up(self) -> NoReturn:
        await super().start_up()
        self.send_log(__name__).info(f"Trying to login...")
        await sleep(choice(4, 6, 8))
        self._me = await self.get_me()

        if self.is_bot:
            _usn = self._me.username
            self.send_log(__name__).info(f"{_usn} has been login.")
        else:
            _fn = self._me.first_name
            self.send_log(__name__).info(f"{_fn} has been login.")

        self.send_log(__name__).info(f"Successfuly, Starting-up on Pyrogram v{__version__}")

    async def stopped(self, *args):
        try:
            await super().stopped()
            self.send_log(__name__).info("pytel has been stopped.")
        except ConnectionError:
            pass


class PytelClient(Client):
    __module__ = "pyrogram.client"
    _client = []

    def __init__(
        self,
        name: Optional[str] = None,
        api_id: Union[int, str] = None,
        api_hash: Optional[str] = None,
        session_string: Optional[str] = None,
        lang_code: Optional[str] = None,
        in_memory: Optional[bool] = None,
        ipv6: Optional[bool] = None,
        *args,
        **kwargs,
    ):
        kwargs["name"] = name
        kwargs["api_id"] = api_id
        kwargs["api_hash"] = api_hash
        kwargs["session_string"] = session_string
        kwargs["lang_code"] = lang_code
        kwargs["in_memory"] = in_memory
        kwargs["ipv6"] = ipv6

        super().__init__()
        self.group_call = GroupCallFactory(self).get_group_call()
        self.send_log = send_log
        self.loop = get_event_loop()

    def __repr__(self):
        return "<Kasta.Client:\n self: {} {}\n id: {}\n>".format(
            self.first_name,
            self.last_name,
            self.id,
        )

    def __hash__(self) -> int:  # pylint: disable=W0235
        return super().__hash__()

    def running_in_loop(self, func: Coroutine[Any, Any, None]) -> Any:
        return self.loop.run_until_complete(func)

    def py_message(self, filters=filters.Filter, group=-1):
        def decorator(func: Callable):
            for _ in self._client:
                try:
                    _.add_handler(MessageHandler(func, filters), group)
                except BaseException as excp:
                    self.send_log(__name__).error(excp)
            return func

        return decorator

    async def join_kasta(self):
        await super().join_kasta()
        try:
            await self.join_chat("@kastaot")
            await self.join_chat("@kastaid")
            await self.join_chat("@Teman_Random")
            await self.join_chat("@LPM_Linux")
            await self.join_chat("@xrestricted")
            await self.join_chat("@dirtysoulvvv")
        except BaseException:
            pass

    async def starting_client(self):
        await super().starting_client()
        if self not in self._client:
            self._client.append(self)
        self.run_until_disconnected()

    async def stopped_client(self, *args):
        await super().stopped_client()
        if self not in self._bots:
            self._bots.append(self)
