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
SESSION1: Optional[str] = gets(
    "SESSION1", ""
)

# Multi Client
SESSION2: Optional[str] = gets(
    "SESSION2", ""
)
SESSION3: Optional[str] = gets(
    "SESSION3", ""
)
SESSION4: Optional[str] = gets(
    "SESSION4", ""
)
SESSION5: Optional[str] = gets(
    "SESSION5", ""
)
SESSION6: Optional[str] = gets(
    "SESSION6", ""
)
SESSION7: Optional[str] = gets(
    "SESSION7", ""
)
SESSION8: Optional[str] = gets(
    "SESSION8", ""
)
SESSION9: Optional[str] = gets(
    "SESSION9", ""
)
SESSION10: Optional[str] = gets(
    "SESSION10", ""
)

# ChatGPT API_KEY
AI_KEY: Optional[str] = gets(
    "AI_KEY", ""
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
