# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from contextlib import suppress
from mimetypes import guess_type
from re import findall, search
from typing import Optional, Any
from instagrapi import (
    Client as InstagramClient,)
from requests import get
from ...config import IG_USN, IG_PASS


def Pinterest(
    pin_url: Optional[str],
):
    """
    Pinterest :: Downloader
    """
    media = []
    best_pin = []
    req = get(pin_url).url
    if not req:
        return False, False
    mx = search(
        r"pinterest.com/pin/(.*)/", req
    )
    kz = findall(r"\d+", str(mx))
    ids = str(kz[2])
    if not ids:
        return False, False
    url = f"https://api.pinterest.com/v3/pidgets/pins/info/?pin_ids={ids}"
    response = get(url).json()["data"][
        0
    ]
    if response.get("story_pin_data"):
        space = response.get(
            "story_pin_data"
        )
        for page in space["pages"]:
            v = page["blocks"][0].get(
                "video"
            )
            i = page["blocks"][0].get(
                "image"
            )
            if v:
                media.append(
                    v.get("video_list")
                )
            elif i:
                media.append(
                    i.get("images")
                )
            else:
                pass

    elif response.get("videos"):
        v = response.get("videos")
        media.append(
            v.get("video_list")
        )
    elif response.get("images"):
        i = response.get("images")
        media.append(i)
    else:
        pass

    for _, m in enumerate(media):
        # remove .m3u8 urls
        for s in list(m):
            if (
                m[s]["url"]
                .strip()
                .endswith(".m3u8")
            ):
                m.pop(s)
        new_m = sorted(
            m.values(),
            key=lambda s: s["width"]
            * s["height"],
            reverse=True,
        )
        best_pin.append(new_m[0])

    for my_pin in best_pin:
        type_file = guess_type(
            my_pin["url"].strip()
        )[0].split("/")[0]
        if type_file == "video":
            _ = my_pin["url"]
            file_name = (
                "cache/pintdl.mp4"
            )
            r = get(_, stream=True)
            with open(
                file_name, "wb"
            ) as f:
                for (
                    chunk
                ) in r.iter_content(
                    chunk_size=1024
                    * 1024
                ):
                    if chunk:
                        f.write(chunk)
            return "video", file_name
        if type_file == "image":
            _ = my_pin["url"]
            return "image", _


def TikTok(
    tiktok_url: Optional[str],
):
    """
    TikTok :: Downloader
    """
    response = get(
        f"https://api.douyin.wtf/api?url={tiktok_url}"
    ).json()
    if not response:
        return False, False, False
    video = response["video_data"][
        "nwm_video_url"
    ]
    if response["desc"]:
        description = response["desc"]
    else:
        description = "-"
    if response["music"]["play_url"][
        "uri"
    ]:
        audio = response["music"][
            "play_url"
        ]["uri"]
    else:
        audio = None
    return video, audio, description


class MetaAPI:
    def __init__(
        self,
        client: Any,
        ig_usn: Any,
        ig_pass: Any,
    ):
        self.client = client
        self.ig_usn = ig_usn
        self.ig_pass = ig_pass
        self.client.login(
            self.ig_usn, self.ig_pass
        )

    def ig_download(
        self,
        ig_url: Optional[str],
        type_dl: Optional[str] = None,
    ):
        with suppress(Exception):
            photo, video = None, None
            get_id = self.client.media_pk_from_url(
                ig_url
            )
            if type_dl == "photo":
                photo = self.client.photo_download(
                    get_id
                )
                if photo:
                    return photo
                else:
                    return False

            elif type_dl == "video":
                video = self.client.video_download(
                    get_id
                )
                if video:
                    return video
                else:
                    return False

    def get_igusers(
        self, username: Optional[str]
    ):
        info = None
        with suppress(Exception):
            info = self.client.user_info_by_username(
                str(username)
            ).dict()
            if info:
                return info
            else:
                return False


Instagram = MetaAPI(
    client=InstagramClient(),
    ig_usn=IG_USN,
    ig_pass=IG_PASS,
)
