# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >


from ..config import (
    API_ID,
    API_HASH,
    SESSION1,
    SESSION2,
    SESSION3,
    SESSION4,
    SESSION5,
    TGB_TOKEN,
)
from .pyclient import Pytel, PytelClient

pytel_tgb = Pytel(
    name="pytel",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TGB_TOKEN,
    lang_code="en",
    in_memory=True,
    ipv6=False,
)
pytel_1 = (
    PytelClient(
        name="pytel1",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION1,
        lang_code="en",
        in_memory=True,
        ipv6=False,  # pylint: disable-F541
    )
    if SESSION1
    else None
)
pytel_2 = (
    PytelClient(
        name="pytel2",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION2,
        lang_code="en",
        in_memory=True,
        ipv6=False,
    )
    if SESSION2
    else None
)
pytel_3 = (
    PytelClient(
        name="pytel3",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION3,
        lang_code="en",
        in_memory=True,
        ipv6=False,
    )
    if SESSION3
    else None
)
pytel_4 = (
    PytelClient(
        name="pytel4",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION4,
        lang_code="en",
        in_memory=True,
        ipv6=False,  # pylint: disable-F541
    )
    if SESSION4
    else None
)
pytel_5 = (
    PytelClient(
        name="pytel5",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION5,
        lang_code="en",
        in_memory=True,
        ipv6=False,
    )
    if SESSION5
    else None
)

pytel_client = PytelClient(name="all_client")

pytelist = [_ for _ in [pytel_1, pytel_2, pytel_3, pytel_4, pytel_5] if _]

for _ in pytelist:
    pytel_client._client.append(_)
