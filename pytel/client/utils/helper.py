# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

import json
from typing import (
    Tuple,
    List,
    Set,
    Union,
    Dict,
    Any,
    Optional,)


class SaveDict(dict):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        if args:
            cdict = args[0]
        else:
            cdict = kwargs
        for key in cdict:
            if isinstance(
                cdict[key],
                dict,
            ):
                cdict[key] = SaveDict(
                    cdict[key]
                )
            elif isinstance(
                cdict[key],
                (
                    list,
                    tuple,
                    set,
                ),
            ):
                cdict[
                    key
                ] = self.convert_list(
                    cdict[key]
                )
        super().__init__(
            *args,
            **cdict,
        )

    def convert_list(
        self,
        n: Union[
            List[Any],
            Tuple[
                Any,
                ...,
            ],
            Set[Any],
        ],
    ) -> List[Any]:
        new_list = []
        for item in n:
            if isinstance(
                item,
                (
                    list,
                    tuple,
                    set,
                ),
            ):
                new_list.append(
                    self.convert_list(
                        item
                    )
                )
            elif isinstance(
                item,
                dict,
            ):
                new_list.append(
                    SaveDict(item)
                )
            else:
                new_list.append(item)
        return new_list

    def to_dict(
        self,
    ) -> Dict[str, Any]:
        _dict = dict(self)
        for key in _dict:
            if isinstance(
                _dict[key],
                SaveDict,
            ):
                _dict[key] = _dict[
                    key
                ].to_dict()
            elif isinstance(
                _dict[key],
                (
                    list,
                    tuple,
                    set,
                ),
            ):
                new_list = []
                for i in _dict[key]:
                    if isinstance(
                        i,
                        SaveDict,
                    ):
                        new_list.append(
                            i.to_dict()
                        )
                    else:
                        new_list.append(
                            i
                        )
                _dict[key] = new_list
        return _dict

    def prettify(
        self,
        indent: int = 4,
    ) -> str:
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
        )

    def __getattr__(self, attr) -> Any:
        if attr in self:
            return self[attr]
        raise AttributeError(
            f"Attrify has no attribute '{attr}'"
        )

    def __dir__(
        self,
    ) -> List[str]:
        mx = dict.__dir__(self)
        mx.extend(
            [
                x
                for x in self.keys()
                if str(x).isalpha()
            ]
        )
        return mx


class PluginsHelp(dict):
    def append(
        self,
        obj: Optional[dict],
    ) -> None:
        plug = list(obj.keys())[0]
        cmds = {}
        for _ in obj[plug]:
            name = list(_.keys())[0]
            desc = _[name]
            cmds[name] = desc
        self[plug] = cmds

    @property
    def count(
        self,
    ) -> Optional[int]:
        return len(self)

    @property
    def total(
        self,
    ) -> Optional[int]:
        return sum(
            len(_)
            for _ in self.values()
        )

    @property
    def value(
        self: Optional[dict],
    ):
        return [*self]


plugins_helper = PluginsHelp()
