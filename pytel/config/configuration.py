# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from os import getenv as gets
from typing import Optional
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv("config.env"))


API_ID: Optional[int] = gets("API_ID", "")
API_HASH: Optional[str] = gets("API_HASH", "")
SESSION1: Optional[str] = gets("SESSION1", "")
TGB_TOKEN: Optional[str] = gets("TGB_TOKEN", "")
LOGCHAT_ID: Optional[int] = gets("LOGCHAT_ID", "")
PREFIX: Optional[str] = gets("PREFIX", "")

# Multi Client
SESSION2: Optional[str] = gets("SESSION2", "")
SESSION3: Optional[str] = gets("SESSION3", "")
SESSION4: Optional[str] = gets("SESSION4", "")
SESSION5: Optional[str] = gets("SESSION5", "")
