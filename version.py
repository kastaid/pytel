# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

def pytel_version() -> str:
    import json
    with open("manifest.json", mode="r") as pv:
        data = json.load(pv)
    return data.get("version", "unknown")
__version__ = pytel_version()
