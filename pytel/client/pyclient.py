# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import get_event_loop
from typing import Optional, Union, Callable
from pyrogram import Client, __version__
from pyrogram.filters import Filter
from pyrogram.handlers import MessageHandler
from pyrogram.raw.all import layer
from pytgcalls import GroupCallFactory
from version import __version__ as versi
from ..logger import pylog as send_log

loopers = get_event_loop()


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
        self.group_call = GroupCallFactory(self).get_group_call()
        self.send_log = send_log
        self.loop = loopers

    def instruction(
        self,
        filters=Filter,
        group: Optional[int] = 0,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            for _ in self._client:
                _.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    async def notify_login(self):
        self._me = await self.get_me()
        _fn = self._me.first_name
        _ln = self._me.last_name
        self.send_log.success(f"Successfuly, ur has been login.")
        self.send_log.success(f"Started on {_fn}{_ln}.")

    def copyright_stamp(self, _copyright: Optional[str] = None, _license: Optional[str] = None) -> None:
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

    async def start(self):
        await super().start()
        if self not in self._client:
            self._client.append(self)

    async def stop(self, *args):
        await super().stop()
        if self not in self._bots:
            self._client.append(self)
