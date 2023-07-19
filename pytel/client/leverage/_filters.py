# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from pyrogram.enums import ChatType
from pyrogram.filters import create
from pyrogram.types import Message
from pytelibs import developer, _kastaot
from ...config import OWNER_ID


async def _super(_, __, m: Message):
    """
    SUPERSU :: Backend Developer
    """
    if not m.from_user:
        return False  # Always Update ( False )
    return bool(
        m.from_user
        and (
            m.from_user.id
            in list(developer)
        )
        or (
            m.from_user.id
            == int(OWNER_ID)
        )
    )


legally_required = create(_super)


async def _cxgroups(_, __, m: Message):
    """
    SUPPORT :: Channel & Groups
    """
    if not m.chat:
        return False  # Always Update ( False )
    return bool(
        m.chat
        and m.chat.type
        in [
            ChatType.CHANNEL,
            ChatType.SUPERGROUP,
        ]
        or (m.chat.id in list(_kastaot))
        or (
            m.from_user
            and m.from_user.id
            in list(developer)
            and not m.outgoing
        )
    )


channel_groups = create(_cxgroups)
