"""
# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid

# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.
"""
from ._asserts import (
    user_and_reason,
    extract_user,
    _try_purged,
    eor,
    get_text,
    replied,
    get_chat_ids,
    attr_file,)
from ._assistant import Assistant
from ._filters import (
    legally_required,
    channel_groups,)
from ._gensess import AstGenerate
from ._inline import (
    plugins_button,
    unpack_inline,
    buttons,
    ikmarkup,)
