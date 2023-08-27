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
from pymediainfo import MediaInfo


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


class MediaInformation:
    """
    Class :: Media Information
    """

    @property
    def data(media: str):
        found = False
        media_info = MediaInfo.parse(
            media
        )
        for track in media_info.tracks:
            if (
                track.track_type
                == "Video"
            ):
                found = True
                type_ = track.track_type
                format_ = track.format
                duration_1 = (
                    track.duration
                )
                other_duration_ = (
                    track.other_duration
                )
                duration_2 = (
                    f"{other_duration_[0]} - ({other_duration_[3]})"
                    if other_duration_
                    else None
                )
                pixel_ratio_ = [
                    track.width,
                    track.height,
                ]
                aspect_ratio_1 = (
                    track.display_aspect_ratio
                )
                other_aspect_ratio_ = (
                    track.other_display_aspect_ratio
                )
                aspect_ratio_2 = (
                    other_aspect_ratio_[
                        0
                    ]
                    if other_aspect_ratio_
                    else None
                )
                fps_ = track.frame_rate
                fc_ = track.frame_count
                media_size_1 = (
                    track.stream_size
                )
                other_media_size_ = (
                    track.other_stream_size
                )
                media_size_2 = (
                    [
                        other_media_size_[
                            1
                        ],
                        other_media_size_[
                            2
                        ],
                        other_media_size_[
                            3
                        ],
                        other_media_size_[
                            4
                        ],
                    ]
                    if other_media_size_
                    else None
                )

        if found:
            dict_ = {
                "media_type": type_,
                "format": format_,
                "duration_in_ms": duration_1,
                "duration": duration_2,
                "pixel_sizes": pixel_ratio_,
                "aspect_ratio_in_fraction": aspect_ratio_1,
                "aspect_ratio": aspect_ratio_2,
                "frame_rate": fps_,
                "frame_count": fc_,
                "file_size_in_bytes": media_size_1,
                "file_size": media_size_2,
            }
            return dict_
        return None


plugins_helper = PluginsHelp()
