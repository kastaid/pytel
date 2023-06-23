# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >


class PluginsHelp(dict):
    def append(self, obj: dict) -> None:
        plug = list(obj.keys())[0]
        cmds = {}
        for _ in obj[plug]:
            name = list(_.keys())[0]
            desc = _[name]
            cmds[name] = desc
        self[plug] = cmds

    @property
    def count(self) -> int:
        return len(self)

    @property
    def total(self) -> int:
        return sum(len(_) for _ in self.values())


plugins_helper = PluginsHelp()
