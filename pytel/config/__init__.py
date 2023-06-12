# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from sys import exit
from pathlib import Path

Checker: Path = Path(__file__).parent.parent

directory = ['config.env']
for b in directory:
    for a in (Checker / b).rglob('*.*'):
        if not a.exists():
            print(
                '| [WARNING] | File config.env not found !!'
            )
            exit(1)

try:
    from .configuration import PYTEL_CONFIG as config
except ImportError as excp:
    print(excp)
    exit(1)
