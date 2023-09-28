# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from io import BytesIO
from math import ceil
from struct import unpack
from typing import Callable, Optional
from asyncache import cached
from cachetools import MRUCache
from pyrogram.file_id import b64_decode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,)
from ...logger import pylog as send_log
from ..utils import SaveDict


class EqInlineKeyboardButton(
    InlineKeyboardButton
):
    def __eq__(
        self, other: Optional[str]
    ):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def buttons(
    text,
    **kwargs,
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        **kwargs,
    )


def ikmarkup(
    *args,
    **kwargs,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        *args,
        **kwargs,
    )


def plugins_button(
    p_name,
    plugins_dict,
    prefixies,
    group=None,
):
    if not group:
        plugins = sorted(
            [
                EqInlineKeyboardButton(
                    name,
                    callback_data="{}_plug({})".format(
                        prefixies,
                        name,
                    ),
                )
                for name in plugins_dict.value
            ]
        )
    else:
        plugins = sorted(
            [
                EqInlineKeyboardButton(
                    name,
                    callback_data="{}_plug({},{})".format(
                        prefixies,
                        group,
                        name,
                    ),
                )
                for name in plugins_dict.value
            ]
        )
    linear = 2
    get_plugins = list(
        zip(
            plugins[::2],
            plugins[1::2],
        )
    )
    total = 0
    for plgns in get_plugins:
        for _ in plgns:
            total += 1
    if len(plugins) - total == 1:
        get_plugins.append(
            (plugins[-1],)
        )
    elif len(plugins) - total == 2:
        get_plugins.append(
            (
                plugins[-2],
                plugins[-1],
            )
        )

    number_page = ceil(
        len(get_plugins) / linear
    )
    plugins_page = p_name % number_page

    if len(get_plugins) > linear:
        get_plugins = get_plugins[
            plugins_page
            * linear : linear
            * (plugins_page + 1)
        ] + [
            (
                EqInlineKeyboardButton(
                    "◄ ",
                    callback_data="{}_prev({})".format(
                        prefixies,
                        plugins_page,
                    ),
                ),
                EqInlineKeyboardButton(
                    " ►",
                    callback_data="{}_next({})".format(
                        prefixies,
                        plugins_page,
                    ),
                ),
            )
        ]

    return get_plugins


@cached(
    MRUCache(
        maxsize=1024,
    ),
)
def unpack_inline(
    inline_message_id: str,
) -> Callable:
    try:
        b = BytesIO(
            b64_decode(
                inline_message_id
            )
        )
        (
            dc_id,
            message_id,
            pid,
            query_id,
        ) = unpack(
            "=iiiq",
            b.read(),
        )
        peer = int(
            str(pid).replace(
                "-",
                "-100",
            )
        )
        _ = {
            "dc_id": dc_id,
            "message_id": message_id,
            "chat_id": peer,
            "query_id": query_id,
            "inline_message_id": inline_message_id,
        }
        return SaveDict(_)
    except BaseException as excp:
        send_log.exception(excp)
