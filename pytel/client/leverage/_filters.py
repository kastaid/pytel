# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

# from pyrogram.enums import ChatType
from pyrogram.filters import create
from pyrogram.types import Message
from pytelibs import _supersu
from ...config import OWNER_ID
from ..dbase.dbAFK import user_afk


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
            in list(_supersu)
        )
        or (
            m.from_user.id
            == int(OWNER_ID)
        )
    )


legally_required = create(_super)


async def check_client_afk(
    _, __, m: Message
):
    user = __.me.id
    return bool(user_afk(user))


client_afk = create(check_client_afk)
