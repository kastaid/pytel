# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from typing import Optional


class PluginsHelp(dict):
    def append(
        self, obj: Optional[dict]
    ) -> None:
        plug = list(obj.keys())[0]
        cmds = {}
        for _ in obj[plug]:
            name = list(_.keys())[0]
            desc = _[name]
            cmds[name] = desc
        self[plug] = cmds

    @property
    def count(self) -> Optional[int]:
        return len(self)

    @property
    def total(self) -> Optional[int]:
        return sum(
            len(_) for _ in self.values()
        )

    @property
    def value(self: Optional[dict]):
        return [*self]


plugins_helper = PluginsHelp()
