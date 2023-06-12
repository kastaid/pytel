# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from typing import Optional
from os import getenv as gets
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('config.env'))


class PYTEL_CONFIG(object):
    API_ID: Optional[int] = gets('API_ID', '')
    API_HASH: Optional[str] = gets('API_HASH', '')
    SESSION: Optional[str] = gets('SESSION', '')
    TGB_TOKEN: Optional[str] = gets('TGB_TOKEN', '')
