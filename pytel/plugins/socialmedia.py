# pytel < https://t.me/kastaid > Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from json import loads
from re import (
    search,
    findall,
    sub,)
from requests import (
    get as getreq,)
from search_engine_parser import (
    GoogleSearch,)
from youtube_search import (
    YoutubeSearch,)
from youtubesearchpython import (
    SearchVideos,)
from yt_dlp import (
    YoutubeDL,)
from . import (
    Rooters,
    RAPID_KEY,
    Instagram,
    TikTok,
    Pinterest,
    ParseMode,
    fetch_github,
    _try_purged,
    eor,
    get_text,
    is_url,
    int2date,
    time,
    progress,
    plugins_helper,
    px,
    pytel,
    replied,
    suppress,
    humanboolean,
    normalize_youtube_url,
    is_youtube_url,
    get_youtube_info,
    subs_like_view_format,
    random_prefixies,)

_YOUTUBE_DLDR = """
<b>{}</b>
{} x {} • {}

{} 👍ㅤ│ㅤ<u><b><a href="t.me/share/url?url={}">Share ➦</a></u>ㅤ│ㅤ<u><a href="{}">Watch</a></b></u>

<b>{}</b>
{} {}  <b><a href="youtube.com/c/{}">SUBSCRIBE</a></b> 🔔
"""


@pytel.instruction(
    ["dytv", "devytvdl"],
    supersu=["PYTEL"],
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
@pytel.instruction(
    ["ytv", "ytvdl"],
    outgoing=True,
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _youtube_video_dl(
    client, message
):
    str_link = get_text(
        message,
        save_link=False,
        normal=True,
    )
    if not str_link:
        await eor(
            message,
            text="Provide a valid link youtube or text result!",
        )
        return

    xy = await eor(
        message,
        text="Processing...",
    )

    try:
        if is_youtube_url(
            str_link
        ):
            _links = normalize_youtube_url(
                str_link
            )
            info = get_youtube_info(
                url=_links
            )
            str_link = (
                f"{info.get('channel')} - "
                + f"{info.get('title')}"
            )

        with suppress(
            ValueError
        ):
            searching = SearchVideos(
                f"{str_link}",
                offset=1,
                mode="dict",
                max_results=1,
            )
            links = (
                searching.result()
            )
            get_video = links[
                "search_result"
            ]
            url = get_video[
                0
            ][
                "link"
            ]
            thumbn = get_video[
                0
            ][
                "title"
            ]
            ch = get_video[
                0
            ][
                "channel"
            ]
            opsi = {
                "format": "best",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "writethumbnail": True,
                "writeautomaticsub": True,
                "writesubtitles": True,
                "subtitleslangs": "id",
                "nocheckcertificate": True,
                "noplaylist": True,
                "postprocessors": [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": "mp4",
                    },
                    {
                        "key": "FFmpegSubtitlesConvertor",
                        "format": "ass",
                    },
                ],
                "outtmpl": "cache/%(id)s.mp4",
                "logtostderr": False,
                "quiet": True,
            }

        with YoutubeDL(
            opsi
        ) as yt_download:
            download_data = yt_download.extract_info(
                url,
                download=False,
            )
            video_duration = round(
                download_data[
                    "duration"
                ]
                / 120
            )
        if (
            video_duration
            > 120
        ):
            magazine = (
                "120"
            )
            await eor(
                xy,
                text=f"Video longer than {video_duration} min aren't allowed.\nMust be <= {magazine} min.",
            )
            return
        xx = await eor(
            xy,
            text=f"Downloading <b>{thumbn}</b>",
        )
        videof = yt_download.prepare_filename(
            download_data
        )
        yt_download.process_info(
            download_data
        )
    except (
        BaseException
    ) as excp:
        await eor(
            xy or xx,
            text=f"YTDL Error: <pre>{excp}</pre>",
        )
        return

    try:
        a_like = subs_like_view_format(
            num_count=download_data[
                "like_count"
            ]
        )
    except Exception:
        a_like = "N/A"

    a_view = subs_like_view_format(
        num_count=download_data[
            "view_count"
        ]
    )
    a_subscriber = subs_like_view_format(
        num_count=download_data[
            "channel_follower_count"
        ]
    )
    a_upload_date = (
        download_data[
            "upload_date"
        ]
    )
    a_date = int2date(
        int(
            a_upload_date
        )
    )
    if videof:
        thumbnail = f"cache/{download_data['id']}.webp"
        if not (
            Rooters
            / thumbnail
        ).exists():
            thumbnail = f"cache/{download_data['id']}.jpg"
        else:
            thumbnail = f"cache/{download_data['id']}.webp"

        video = f"cache/{download_data['id']}.mp4"
        fx = await xx.reply(
            text="Uploading video...",
        )
        await _try_purged(
            xx
        )
        try:
            u_time = (
                time()
            )
            await client.send_video(
                message.chat.id,
                video=video,
                thumb=thumbnail,
                duration=download_data[
                    "duration"
                ],
                supports_streaming=True,
                caption=_YOUTUBE_DLDR.format(
                    thumbn,
                    a_view,
                    "watched",
                    a_date,
                    a_like,
                    url,
                    url,
                    ch,
                    a_subscriber,
                    "subscriber",
                    ch.replace(
                        " ",
                        "",
                    ),
                ),
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    fx,
                    u_time,
                    "Uploading Video!",
                    "Youtube Video",
                ),
            )
            (
                Rooters
                / video
            ).unlink(
                missing_ok=True
            )
            (
                Rooters
                / thumbnail
            ).unlink(
                missing_ok=True
            )
            await _try_purged(
                fx
            )
            return
        except (
            BaseException
        ) as excp:
            await eor(
                fx,
                text=f"Error: {excp}",
            )
            (
                Rooters
                / video
            ).unlink(
                missing_ok=True
            )
            (
                Rooters
                / thumbnail
            ).unlink(
                missing_ok=True
            )
            return


@pytel.instruction(
    ["dyta", "devytadl"],
    supersu=["PYTEL"],
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
@pytel.instruction(
    ["yta", "ytadl"],
    outgoing=True,
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _youtube_audio_dl(
    client, message
):
    str_link = get_text(
        message,
        save_link=False,
        normal=True,
    )
    if not str_link:
        await eor(
            message,
            text="Provide a valid link youtube or text result!",
        )
        return

    xy = await eor(
        message,
        text="Processing...",
    )
    try:
        if is_youtube_url(
            str_link
        ):
            _links = normalize_youtube_url(
                str_link
            )
            info = get_youtube_info(
                url=_links
            )
            str_link = (
                f"{info.get('channel')} - "
                + f"{info.get('title')}"
            )

        with suppress(
            BaseException
        ):
            searching = SearchVideos(
                f"{str_link}",
                offset=1,
                mode="dict",
                max_results=1,
            )
            links = (
                searching.result()
            )
            get_audio = links[
                "search_result"
            ]
            url = get_audio[
                0
            ][
                "link"
            ]
            get_audio[0][
                "duration"
            ]
            thumbn = get_audio[
                0
            ][
                "title"
            ]
            ch = get_audio[
                0
            ][
                "channel"
            ]
            opsi = {
                "format": "bestaudio/best",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "writethumbnail": True,
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "noplaylist": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "720",
                    }
                ],
                "outtmpl": "cache/%(id)s.mp3",
                "quiet": True,
                "logtostderr": False,
            }

        with YoutubeDL(
            opsi
        ) as yt_download:
            download_data = yt_download.extract_info(
                url,
                download=False,
            )
            audio_duration = round(
                download_data[
                    "duration"
                ]
                / 120
            )
        if (
            audio_duration
            > 120
        ):
            magazine = (
                "120"
            )
            await eor(
                xy,
                text=f"Audio longer than {audio_duration} min aren't allowed.\nMust be <= {magazine} min.",
            )
            return
        xx = await eor(
            xy,
            text=f"Downloading <b>{thumbn}</b>",
        )
        audiof = yt_download.prepare_filename(
            download_data
        )
        yt_download.process_info(
            download_data
        )
    except (
        BaseException
    ) as excp:
        await eor(
            xy or xx,
            text=f"YTDL Error: <pre>{excp}</pre>",
        )
        return

    print(download_data)
    try:
        a_like = subs_like_view_format(
            num_count=download_data[
                "like_count"
            ]
        )
    except Exception:
        a_like = "N/A"

    a_view = subs_like_view_format(
        num_count=download_data[
            "view_count"
        ]
    )
    a_subscriber = subs_like_view_format(
        num_count=download_data[
            "channel_follower_count"
        ]
    )
    a_upload_date = (
        download_data[
            "upload_date"
        ]
    )
    a_date = int2date(
        int(
            a_upload_date
        )
    )
    if audiof:
        thumbnail = f"cache/{download_data['id']}.mp3.webp"
        if not (
            Rooters
            / thumbnail
        ).exists():
            thumbnail = f"cache/{download_data['id']}.mp3.jpg"
        else:
            thumbnail = f"cache/{download_data['id']}.mp3.webp"

        audio = f"cache/{download_data['id']}.mp3.mp3"
        fx = await xx.reply(
            text="Uploading audio...",
        )
        await _try_purged(
            xx
        )
        try:
            u_time = (
                time()
            )
            await client.send_audio(
                message.chat.id,
                audio=audio,
                thumb=thumbnail,
                title=download_data[
                    "title"
                ],
                performer=download_data[
                    "uploader"
                ],
                caption=_YOUTUBE_DLDR.format(
                    thumbn,
                    a_view,
                    "watched",
                    a_date,
                    a_like,
                    url,
                    url,
                    ch,
                    a_subscriber,
                    "subscriber",
                    ch.replace(
                        " ",
                        "",
                    ),
                ),
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    fx,
                    u_time,
                    "Uploading Audio!",
                    "Youtube Audio",
                ),
            )
            (
                Rooters
                / audio
            ).unlink(
                missing_ok=True
            )
            (
                Rooters
                / thumbnail
            ).unlink(
                missing_ok=True
            )
            await _try_purged(
                fx
            )
            return
        except (
            BaseException
        ) as excp:
            await eor(
                fx,
                text=f"Error: {excp}",
            )
            (
                Rooters
                / audio
            ).unlink(
                missing_ok=True
            )
            (
                Rooters
                / thumbnail
            ).unlink(
                missing_ok=True
            )
            return


@pytel.instruction(
    [
        "dyts",
        "devytsearch",
    ],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["yts", "ytsearch"],
    outgoing=True,
)
async def _youtube_searching(
    client, message
):
    str_result = get_text(
        message,
        save_link=False,
        normal=True,
    )
    if not str_result:
        await eor(
            message,
            text="Provide a text for youtube search!",
        )
        return

    x = await eor(
        message,
        text=f"Searching for {str_result.capitalize()}...",
    )
    try:
        results = loads(
            YoutubeSearch(
                str_result,
                max_results=7,
            ).to_json()
        )
    except ValueError:
        await eor(
            x,
            text="Youtube Search gone retard.\nCan't search that's query!!",
        )
        return
    output = f"**Search Query:**\n--{str_result.capitalize()}--\n\n**Results:**\n"
    for i in results[
        "videos"
    ]:
        try:
            title = i[
                "title"
            ]
            link = (
                "https://youtube.com"
                + i[
                    "url_suffix"
                ]
            )
            channel = i[
                "channel"
            ]
            duration = i[
                "duration"
            ]
            views = i[
                "views"
            ]
            output += f"[{title}]({link})\nChannel: `{channel}`\nDuration: {duration} | {views}\n\n"
        except (
            IndexError
        ):
            break

    await client.send_message(
        message.chat.id,
        text=output,
        disable_notification=False,
        disable_web_page_preview=True,
        reply_to_message_id=replied(
            message
        ),
    )
    await _try_purged(x)


@pytel.instruction(
    [
        "ghs",
        "ghsearch",
        "github",
    ],
    outgoing=True,
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _github_searching(
    client, message
):
    str_username = get_text(
        message,
        save_link=False,
        normal=True,
    )
    if not str_username:
        await eor(
            message,
            text="Provide a valid username / link github!",
        )
        return

    x = await eor(
        message,
        text="Checking...",
    )
    if (
        "github.com/"
        in str_username
    ):
        src = search(
            r"github.(.*)",
            str_username,
        )
        mkz = src.group()
        xyz = mkz.replace(
            "github.com/",
            "",
        )
        str_username = sub(
            r"\/([\s\S]*)$",
            "",
            xyz,
        )

    elif str_username.startswith(
        "@"
    ):
        str_username = str_username.replace(
            "@", ""
        )

    x = await eor(
        message,
        text=f"Searching for @{str_username} ...",
    )

    (
        text,
        avatar_url,
    ) = await fetch_github(
        str_username
    )
    if avatar_url:
        try:
            await client.send_document(
                message.chat.id,
                document=avatar_url,
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=replied(
                    message
                ),
                protect_content=True,
            )
            await _try_purged(
                x
            )
            return
        except Exception:
            await eor(
                x,
                text=text,
            )
            return


@pytel.instruction(
    [
        "ggs",
        "ggsearch",
        "google",
    ],
    outgoing=True,
)
async def _google_searching(
    client, message
):
    str_result = get_text(
        message,
        save_link=False,
        normal=True,
    )
    if not str_result:
        await eor(
            message,
            text="Provide a text for google search!",
        )
        return

    x = await eor(
        message,
        text=f"Searching for {str_result.capitalize()}...",
    )
    point = (
        str_result.strip()
    )
    page = findall(
        r"page=\d+",
        point,
    )
    try:
        page = page[0]
        page = (
            page.replace(
                "page=",
                "",
            )
        )
        point = point.replace(
            "page="
            + page[0],
            "",
        )
    except IndexError:
        page = 1
    try:
        google_args = (
            str(point),
            int(page),
        )
        google_search_engine = (
            GoogleSearch()
        )
        google_results = await google_search_engine.async_search(
            *google_args
        )
        messg = ""
        for i in range(
            5
        ):
            try:
                title = google_results[
                    "titles"
                ][
                    i
                ]
                link = google_results[
                    "links"
                ][
                    i
                ]
                desc = google_results[
                    "descriptions"
                ][
                    i
                ]
                messg += f"[{title}]({link})\n`{desc}`\n\n"
            except IndexError:
                break
    except (
        BaseException
    ) as excp:
        await eor(
            x,
            text=f"Google Error: {excp}",
        )
        return

    await client.send_message(
        message.chat.id,
        text=messg,
        disable_notification=False,
        disable_web_page_preview=True,
        reply_to_message_id=replied(
            message
        ),
    )
    await _try_purged(x)


@pytel.instruction(
    ["digsr", "devigsr"],
    supersu=["PYTEL"],
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
@pytel.instruction(
    ["igsr", "igsearch"],
    outgoing=True,
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _instagram_searching(
    client, message
):
    igusername = get_text(
        message,
        save_link=False,
        normal=True,
    )
    if (
        not igusername
        or (
            "@"
            not in igusername
        )
    ):
        await eor(
            message,
            text="Provide a valid username Instagram!\n\n<b>Example:</b>\nUsername: @ledzeppelin",
        )
        return
    x = await eor(
        message,
        text=f"Searching for {igusername} user...",
    )
    username = igusername.replace(
        "@", ""
    )
    infouser = Instagram.get_igusers(
        username=username
    )
    if infouser:
        bio = (
            infouser[
                "biography"
            ]
            if infouser[
                "biography"
            ]
            else "-"
        )
        id_ig = infouser[
            "pk"
        ]
        username_ig = (
            "@"
            + infouser[
                "username"
            ]
        )
        fullname_ig = (
            infouser[
                "full_name"
            ]
            if infouser[
                "full_name"
            ]
            else "-"
        )
        purl = infouser[
            "profile_pic_url_hd"
        ]
        text = f"""
<u><b>INSTAGRAM PROFILE</u></b>
├ <b>Instagram ID:</b> <code>{id_ig}</code>
├ <b>Username:</b> {username_ig}
├ <b>Fullname:</b> {fullname_ig}
├ <b>Followers:</b> {subs_like_view_format(infouser['follower_count'])}
├ <b>Following:</b> {subs_like_view_format(infouser['following_count'])}
├ <b>Number of Posts:</b> {infouser['media_count']} Media.
├ <b>Is_private</b>: {humanboolean(infouser['is_private'])}
├ <b>Is_verified</b>: {humanboolean(infouser['is_verified'])}
├ <b>Is_business</b>: {humanboolean(infouser['is_business'])}
├ <b>Permanent Link:</b> <a href="instagram.com/{infouser['username']}">{username_ig}</a>
└ <b>Biography</b>: {str(bio)}

Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>
Made with <a href='https://developers.facebook.com/docs/instagram/'>Meta</a> ( Facebook )

Copyright (C) 2023-present @kastaid
"""
        if purl:
            r = getreq(
                purl,
                stream=True,
            )
            filn = f"cache/{username_ig}.jpg"
            with open(
                filn,
                "wb",
            ) as f:
                for (
                    chunk
                ) in r.iter_content(
                    chunk_size=1024
                    * 1024
                ):
                    if chunk:
                        f.write(
                            chunk
                        )
            await client.send_document(
                message.chat.id,
                document=filn,
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=replied(
                    message
                ),
                protect_content=True,
            )
            await _try_purged(
                x
            )
            (
                Rooters
                / filn
            ).unlink(
                missing_ok=True
            )
            return
        else:
            await client.send_message(
                message.chat.id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=replied(
                    message
                ),
            )
            await _try_purged(
                x
            )
            return
    else:
        await eor(
            x,
            text="Can't find that users.\nPlease check username again!",
        )
        return


@pytel.instruction(
    [
        "digpdl",
        "digvdl",
        "digsdl",
    ],
    supersu=["PYTEL"],
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
@pytel.instruction(
    [
        "igpdl",
        "igvdl",
        "igsdl",
    ],
    outgoing=True,
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _instagram_dl(
    client, message
):
    (
        photo,
        video,
        story_,
    ) = (
        None,
        None,
        None,
    )
    str_link = get_text(
        message,
        save_link=True,
    )
    if (
        not str_link
        or not (
            is_url(
                str_link
            )
            is True
            or (
                "instagram"
                not in str_link
            )
        )
    ):
        await eor(
            message,
            text="Provide a valid link Instagram!",
        )
        return

    x = await eor(
        message,
        text="Processing...",
    )

    if (
        message.command[
            0
        ]
        == "igpdl"
        or "digpdl"
    ):
        photo = Instagram.ig_download(
            ig_url=str_link,
            type_dl="photo",
        )
        if photo:
            u_time = (
                time()
            )
            caption = f"""
<b><u>INSTAGRAM PHOTO DOWNLOADER</b></u>
<b>Sources Photo:</b> <a href='{str_link}'>Click Here</a>

Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>
Made with <a href='https://developers.facebook.com/docs/instagram/'>Meta</a> ( Facebook )
"""
            await client.send_photo(
                message.chat.id,
                photo=photo,
                caption=caption,
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Instagram Photo",
                ),
            )
            (
                Rooters
                / photo
            ).unlink(
                missing_ok=True
            )
            return await _try_purged(
                x
            )
        else:
            await eor(
                x,
                text="Can't fetching photo Instagram. Try again!",
            )

    elif (
        message.command[
            0
        ]
        == "igvdl"
        or "digvdl"
    ):
        video = Instagram.ig_download(
            ig_url=str_link,
            type_dl="video",
        )
        if video:
            u_time = (
                time()
            )
            caption = f"""
<b><u>INSTAGRAM VIDEO DOWNLOADER</b></u>
<b>Sources Video:</b> <a href='{str_link}'>Click Here</a>

Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>
Made with <a href='https://developers.facebook.com/docs/instagram/'>Meta</a> ( Facebook )
"""
            await client.send_video(
                message.chat.id,
                video=video,
                caption=caption,
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Instagram Video",
                ),
            )
            (
                Rooters
                / video
            ).unlink(
                missing_ok=True
            )
            return await _try_purged(
                x
            )
        else:
            await eor(
                x,
                text="Can't fetching video Instagram. Try again!",
            )

    elif (
        message.command[
            0
        ]
        == "igsdl"
        or "digsdl"
    ):
        story_ = Instagram.ig_download(
            ig_url=str_link,
            type_dl="story",
        )
        if story_:
            u_time = (
                time()
            )
            caption = f"""
<b><u>INSTAGRAM STORY DOWNLOADER</b></u>
<b>Sources Story:</b> <a href='{str_link}'>Click Here</a>

Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>
Made with <a href='https://developers.facebook.com/docs/instagram/'>Meta</a> ( Facebook )
"""
            await client.send_document(
                message.chat.id,
                document=story_,
                caption=caption,
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Instagram Story",
                ),
            )
            (
                Rooters
                / story_
            ).unlink(
                missing_ok=True
            )
            return await _try_purged(
                x
            )
        else:
            await eor(
                x,
                text="Can't fetching story Instagram. Try again!",
            )


@pytel.instruction(
    [
        "dpintdl",
        "dpindl",
    ],
    supersu=["PYTEL"],
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
@pytel.instruction(
    ["pintdl", "pindl"],
    outgoing=True,
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _pinterest_dl(
    client, message
):
    str_link = get_text(
        message,
        save_link=True,
    )
    if (
        not str_link
        or not (
            is_url(
                str_link
            )
            is True
            or (
                "pin"
                not in str_link
            )
        )
    ):
        await eor(
            message,
            text="Provide a valid link Pinterest!",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    (
        type_file,
        my_pin,
    ) = Pinterest(
        pin_url=str_link
    )
    if not my_pin:
        await eor(
            x,
            text="Can't find any files, Please try again later!",
        )
        return
    u_time = time()
    with suppress(
        Exception
    ):
        caption = f"""
<b><u>PINTEREST DOWNLOADER</b></u>
<b>Sources:</b> <a href='{str_link}'>Click Here</a>

Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>
Made with <a href='https://developers.pinterest.com/'>Pinterest</a> ( Developers )
"""
        if (
            type_file
            == "video"
        ):
            await client.send_video(
                message.chat.id,
                video=my_pin,
                caption=caption,
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Pinterest Video",
                ),
            )
            await _try_purged(
                x, 1
            )
            (
                Rooters
                / my_pin
            ).unlink(
                missing_ok=True
            )
            return
        if (
            type_file
            == "image"
        ):
            await client.send_photo(
                message.chat.id,
                photo=my_pin,
                caption=caption,
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Pinterest Photo",
                ),
            )
            await _try_purged(
                x, 1
            )
            return


@pytel.instruction(
    [
        "dttdl",
        "devtiktokdl",
    ],
    supersu=["PYTEL"],
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
@pytel.instruction(
    ["tiktokdl", "ttdl"],
    outgoing=True,
    supergroups=False,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _tiktok_dl(
    client, message
):
    str_link = get_text(
        message,
        save_link=True,
    )
    if (
        not str_link
        or not (
            is_url(
                str_link
            )
            is True
            or (
                "vt"
                or "tiktok"
                not in str_link
            )
        )
    ):
        await eor(
            message,
            text="Provide a valid link tiktok!",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    (
        video,
        audio,
        description,
    ) = await TikTok(
        tiktok_url=str_link
    )
    if video:
        u_time = time()
        try:
            caption = f"{description}\n\nProjects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>\nMade with <a href='https://tiktok.com'>Tiktok</a>"
            await client.send_video(
                message.chat.id,
                video=video,
                caption=caption,
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    x,
                    u_time,
                    "`Uploading File!`",
                    "Tiktok Video",
                ),
            )
            if audio:
                caption = "Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>\nMade with <a href='https://tiktok.com'>Tiktok</a>"
                await client.send_audio(
                    message.chat.id,
                    audio=audio,
                    caption=caption,
                    reply_to_message_id=replied(
                        message
                    ),
                    progress=progress,
                    progress_args=(
                        x,
                        u_time,
                        "`Uploading File!`",
                        "Tiktok Audio",
                    ),
                )
        except (
            Exception
        ) as excp:
            await eor(
                x,
                text=f"Exception: ```{excp}```",
            )
            return
    else:
        await eor(
            x,
            text="Can't find Tiktok video!",
        )
        return

    return await _try_purged(
        x, 1
    )


@pytel.instruction(
    [
        "dscl",
        "devsocial",
    ],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["scl", "social"],
    outgoing=True,
    supergroups=False,
)
async def _social_links(
    client, message
):
    real_name = get_text(
        message,
        save_link=False,
        normal=True,
    )
    if not real_name:
        await eor(
            message,
            text="Provide a valid real name!",
        )
        return
    x = await eor(
        message,
        text=f"Searching for <b>{real_name}</b>...",
    )
    str_url = "https://social-links-search.p.rapidapi.com/search-social-links"
    querystring = {
        "query": real_name,
        "social_networks": "facebook,tiktok,instagram,snapchat,twitter,youtube,linkedin,github,pinterest",
    }
    headers = {
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "social-links-search.p.rapidapi.com",
    }
    resp = getreq(
        str_url,
        headers=headers,
        params=querystring,
    ).json()
    if (
        resp["status"]
        != "OK"
    ):
        await eor(
            x,
            text="Could'nt fetch data users.",
        )
        return
    text = "<b><u>Links Social Media</b></u>\n"
    text += f"<b>Users:</b> {real_name}\n\n"
    for f in resp[
        "data"
    ]["facebook"]:
        text += f"<b>Facebook:</b> {f}\n"
    for i in resp[
        "data"
    ]["instagram"]:
        text += f"<b>Instagram:</b> {i}\n"
    for t in resp[
        "data"
    ]["twitter"]:
        text += f"<b>Twitter:</b> {t}\n"
    for li in resp[
        "data"
    ]["linkedin"]:
        text += f"<b>LinkedIn:</b> {li}\n"
    for g in resp[
        "data"
    ]["github"]:
        text += f"<b>Github:</b> {g}\n"
    for y in resp[
        "data"
    ]["youtube"]:
        text += f"<b>Youtube:</b> {y}\n"
    for ti in resp[
        "data"
    ]["tiktok"]:
        text += f"<b>TikTok:</b> {ti}\n"
    for s in resp[
        "data"
    ]["snapchat"]:
        text += f"<b>Snapchat:</b> {s}\n"

    await eor(
        message,
        text=text,
    )


plugins_helper[
    "socialmedia"
] = {
    f"{random_prefixies(px)}social [real name]": "To get the user's social media links, start from Facebook/TikTok/Instagram/Snapchat/Twitter/Youtube/LinkedIn/Pinterest/Github.",
    f"{random_prefixies(px)}igsearch [username ig]": "To get Information User. ( Instagram )",
    f"{random_prefixies(px)}igpdl [url]/[reply link]": "To get Instagram. ( image/photo )",
    f"{random_prefixies(px)}igvdl [url]/[reply link]": "To get Instagram. ( video/reels )",
    f"{random_prefixies(px)}igsdl [url]/[reply link]": "To get Instagram. ( story )",
    f"{random_prefixies(px)}ytsearch [text/reply]": "Search engine for youtube.",
    f"{random_prefixies(px)}ytadl [url]/[reply/text]": "To get Youtube. ( audio/mp3 )",
    f"{random_prefixies(px)}ytvdl [url]/[reply/text]": "To get Youtube. ( video/mp4 )",
    f"{random_prefixies(px)}ggsearch / google [text/reply]": "Search engine for google.",
    f"{random_prefixies(px)}ttdl [url]/[reply link]": "To get Tiktok. ( video & original audio ) ( Without Watermark )",
    f"{random_prefixies(px)}pintdl [url]/[reply link]": "To get Pinterest. ( images/video )",
    f"{random_prefixies(px)}github [username/link github]": "To get the User/Organization Github Profile.",
}
