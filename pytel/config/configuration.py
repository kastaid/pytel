# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from os import getenv as gets
from typing import List, Optional, Union
from dotenv import (
    find_dotenv,
    load_dotenv,)

load_dotenv(find_dotenv("config.env"))

# REQURED
API_ID: Optional[int] = gets(
    "API_ID", ""
)
API_HASH: Optional[str] = gets(
    "API_HASH", ""
)
API_ID1: Optional[int] = gets(
    "API_ID1", ""
)
API_HASH1: Optional[str] = gets(
    "API_HASH1", ""
)
API_ID2: Optional[int] = gets(
    "API_ID2", ""
)
API_HASH2: Optional[str] = gets(
    "API_HASH2", ""
)
API_ID3: Optional[int] = gets(
    "API_ID3", ""
)
API_HASH3: Optional[str] = gets(
    "API_HASH3", ""
)
API_ID4: Optional[int] = gets(
    "API_ID4", ""
)
API_HASH4: Optional[str] = gets(
    "API_HASH4", ""
)
API_ID5: Optional[int] = gets(
    "API_ID5", ""
)
API_HASH5: Optional[str] = gets(
    "API_HASH5", ""
)
API_ID6: Optional[int] = gets(
    "API_ID6", ""
)
API_HASH6: Optional[str] = gets(
    "API_HASH6", ""
)
API_ID7: Optional[int] = gets(
    "API_ID7", ""
)
API_HASH7: Optional[str] = gets(
    "API_HASH7", ""
)
API_ID8: Optional[int] = gets(
    "API_ID8", ""
)
API_HASH8: Optional[str] = gets(
    "API_HASH8", ""
)
API_ID9: Optional[int] = gets(
    "API_ID9", ""
)
API_HASH9: Optional[str] = gets(
    "API_HASH9", ""
)
API_ID10: Optional[int] = gets(
    "API_ID10", ""
)
API_HASH10: Optional[str] = gets(
    "API_HASH10", ""
)
OWNER_ID: int = gets("OWNER_ID", "")
TGB_TOKEN: Optional[str] = gets(
    "TGB_TOKEN", ""
)
LOGCHAT_ID: Optional[int] = gets(
    "LOGCHAT_ID", ""
)
PREFIX: Union[str, List[str]] = gets(
    "PREFIX", ""
).split(",")
TimeZone: Optional[str] = gets(
    "TimeZone", ""
)
BOT_SESSION: Optional[str] = gets(
    "BOT_SESSION", None
)
SESSION1: Optional[str] = gets(
    "SESSION1", None
)

# Multi Client
SESSION2: Optional[str] = gets(
    "SESSION2", None
)
SESSION3: Optional[str] = gets(
    "SESSION3", None
)
SESSION4: Optional[str] = gets(
    "SESSION4", None
)
SESSION5: Optional[str] = gets(
    "SESSION5", None
)
SESSION6: Optional[str] = gets(
    "SESSION6", None
)
SESSION7: Optional[str] = gets(
    "SESSION7", None
)
SESSION8: Optional[str] = gets(
    "SESSION8", None
)
SESSION9: Optional[str] = gets(
    "SESSION9", None
)
SESSION10: Optional[str] = gets(
    "SESSION10", None
)

# Instagram Account
IG_USN: Optional[str] = gets(
    "IG_USN", ""
)
IG_PASS: Optional[str] = gets(
    "IG_PASS", ""
)
IG_SECRET: Optional[str] = gets(
    "IG_SECRET", ""
)

# RAPID API KEY
RAPID_KEY: Optional[str] = gets(
    "RAPID_KEY", ""
)

del load_dotenv, gets
