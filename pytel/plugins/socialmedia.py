# pytel < https://t.me/kastaid > Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from json import loads
from os import remove
from re import search, findall
from requests import get as getreq
from search_engine_parser import (
    GoogleSearch,)
from youtube_search import YoutubeSearch
from youtubesearchpython import (
    SearchVideos,)
from yt_dlp import YoutubeDL
from . import (
    Rooters,
    Instagram,
    TikTok,
    Pinterest,
    ParseMode,
    _try_purged,
    eor,
    get_text,
    is_url,
    int2date,
    plugins_helper,
    px,
    pytel,
    suppress,
    humanboolean,
    subs_like_view_format,
    random_prefixies,)

_YOUTUBE_DLDR = """
<b>{}</b>
{} x {} • {}

{} 👍ㅤ│ㅤ<a href=t.me/share/url?url={}>Share ➦</a>ㅤ│ㅤ<a href='{}'>Watch Now 🎥</a>

<b>{}</b>
{} {} <b><a href='youtube.com/c/{}?view_as=subscriber?sub_confirmation=1'>SUBSCRIBE</a></b> 🔔
"""


@pytel.instruction(
    ["ytv", "ytvdl"],
    outgoing=True,
    supergroups=True,
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
    )
    if not str_link:
        await eor(
            message,
            text="Provide a valid link youtube or text result!",
        )
        return

    x = await eor(
        message,
        text="Processing...",
    )
    searching = SearchVideos(
        f"{str_link}",
        offset=1,
        mode="dict",
        max_results=1,
    )
    links = searching.result()
    get_video = links["search_result"]
    loots = get_video[0]["link"]
    thumbn = get_video[0]["title"]
    ch = get_video[0]["channel"]
    url = loots
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
    try:
        with YoutubeDL(
            opsi
        ) as yt_download:
            download_data = yt_download.extract_info(
                url, download=False
            )
            video_duration = round(
                download_data[
                    "duration"
                ]
                / 120
            )
        if video_duration > 120:
            magazine = "120"
            await eor(
                x,
                text=f"Video longer than {video_duration} min aren't allowed.\nMust be <= {magazine} min.",
            )
            return
        xx = await eor(
            x,
            text=f"Downloading <b>{thumbn}</b>",
        )
        videof = yt_download.prepare_filename(
            download_data
        )
        yt_download.process_info(
            download_data
        )
    except BaseException as excp:
        await eor(
            xx,
            text=f"YTDL Error: <pre>{excp}</pre>",
        )
        return
    a_like = subs_like_view_format(
        num_count=download_data[
            "like_count"
        ]
    )
    a_view = subs_like_view_format(
        num_count=download_data[
            "view_count"
        ]
    )
    a_subscriber = (
        subs_like_view_format(
            num_count=download_data[
                "channel_follower_count"
            ]
        )
    )
    a_upload_date = download_data[
        "upload_date"
    ]
    a_date = int2date(
        int(a_upload_date)
    )
    if videof:
        thumbnail = f"cache/{download_data['id']}.webp"
        if not (
            Rooters / thumbnail
        ).exists():
            thumbnail = f"cache/{download_data['id']}.jpg"
        else:
            thumbnail = f"cache/{download_data['id']}.webp"

        video = f"cache/{download_data['id']}.mp4"
        fx = await eor(
            xx,
            text="Uploading video...",
        )
        try:
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
                    loots,
                    loots,
                    ch,
                    a_subscriber,
                    "subscriber",
                    ch.replace(" ", ""),
                ),
            )
            await _try_purged(fx)
            remove(video)
            remove(thumbnail)
            return
        except BaseException as excp:
            await eor(
                fx,
                text=f"Error: {excp}",
            )
            remove(video)
            remove(thumbnail)
            return


@pytel.instruction(
    ["yta", "ytadl"],
    outgoing=True,
    supergroups=True,
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
    )
    if not str_link:
        await eor(
            message,
            text="Provide a valid link youtube or text result!",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    searching = SearchVideos(
        f"{str_link}",
        offset=1,
        mode="dict",
        max_results=1,
    )
    links = searching.result()
    get_audio = links["search_result"]
    loots = get_audio[0]["link"]
    get_audio[0]["duration"]
    thumbn = get_audio[0]["title"]
    ch = get_audio[0]["channel"]
    url = loots
    opsi = {
        "format": "bestaudio/best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
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
    try:
        with YoutubeDL(
            opsi
        ) as yt_download:
            download_data = yt_download.extract_info(
                url, download=False
            )
            audio_duration = round(
                download_data[
                    "duration"
                ]
                / 120
            )
        if audio_duration > 120:
            magazine = "120"
            await eor(
                x,
                text=f"Audio longer than {audio_duration} min aren't allowed.\nMust be <= {magazine} min.",
            )
            return
        xx = await eor(
            x,
            text=f"Downloading <b>{thumbn}</b>",
        )
        audiof = yt_download.prepare_filename(
            download_data
        )
        yt_download.process_info(
            download_data
        )
    except BaseException as excp:
        await eor(
            xx,
            text=f"YTDL Error: <pre>{excp}</pre>",
        )
        return
    a_like = subs_like_view_format(
        num_count=download_data[
            "like_count"
        ]
    )
    a_view = subs_like_view_format(
        num_count=download_data[
            "view_count"
        ]
    )
    a_subscriber = (
        subs_like_view_format(
            num_count=download_data[
                "channel_follower_count"
            ]
        )
    )
    a_upload_date = download_data[
        "upload_date"
    ]
    a_date = int2date(
        int(a_upload_date)
    )
    if audiof:
        thumbnail = f"cache/{download_data['id']}.mp3.webp"
        if not (
            Rooters / thumbnail
        ).exists():
            thumbnail = f"cache/{download_data['id']}.mp3.jpg"
        else:
            thumbnail = f"cache/{download_data['id']}.mp3.webp"

        audio = f"cache/{download_data['id']}.mp3.mp3"
        fx = await eor(
            xx,
            text="Uploading audio...",
        )
        try:
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
                    loots,
                    loots,
                    ch,
                    a_subscriber,
                    "subscriber",
                    ch.replace(" ", ""),
                ),
            )
            await _try_purged(fx)
            remove(audio)
            remove(thumbnail)
            return
        except BaseException as excp:
            await eor(
                fx,
                text=f"Error: {excp}",
            )
            remove(audio)
            remove(thumbnail)
            return


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
    for i in results["videos"]:
        try:
            title = i["title"]
            link = (
                "https://youtube.com"
                + i["url_suffix"]
            )
            channel = i["channel"]
            duration = i["duration"]
            views = i["views"]
            output += f"[{title}]({link})\nChannel: `{channel}`\nDuration: {duration} | {views}\n\n"
        except IndexError:
            break

    await client.send_message(
        message.chat.id,
        text=output,
        disable_notification=False,
        disable_web_page_preview=True,
    )
    await _try_purged(x)


@pytel.instruction(
    ["ggs", "ggsearch"],
    outgoing=True,
)
async def _google_searching(
    client, message
):
    str_result = get_text(
        message,
        save_link=False,
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
    point = str_result.strip()
    page = findall(r"page=\d+", point)
    try:
        page = page[0]
        page = page.replace("page=", "")
        point = point.replace(
            "page=" + page[0], ""
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
        for i in range(5):
            try:
                title = google_results[
                    "titles"
                ][i]
                link = google_results[
                    "links"
                ][i]
                desc = google_results[
                    "descriptions"
                ][i]
                messg += f"[{title}]({link})\n`{desc}`\n\n"
            except IndexError:
                break
    except BaseException as excp:
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
    )
    await _try_purged(x)


@pytel.instruction(
    ["igs", "igsearch"],
    outgoing=True,
    supergroups=True,
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
    )
    if not igusername or (
        "@" not in igusername
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
            infouser["biography"]
            if infouser["biography"]
            else "-"
        )
        id_ig = infouser["pk"]
        username_ig = (
            "@" + infouser["username"]
        )
        fullname_ig = (
            infouser["full_name"]
            if infouser["full_name"]
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
            get_pic = search(
                r"https://instagram.(.*)",
                purl,
            )
            filn = f"cache/{username_ig}.jpg"
            r = getreq(
                get_pic.group(0),
                stream=True,
            )
            with open(filn, "wb") as f:
                for (
                    chunk
                ) in r.iter_content(
                    chunk_size=1024
                    * 1024
                ):
                    if chunk:
                        f.write(chunk)
            await client.send_document(
                message.chat.id,
                document=filn,
                caption=text,
                parse_mode=ParseMode.HTML,
                protect_content=True,
            )
            await _try_purged(x)
            remove(filn)
            return
        else:
            await client.send_message(
                message.chat.id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
            await _try_purged(x)
            return
    else:
        await eor(
            x,
            text="Can't find that users.\nPlease check username again!",
        )
        return


@pytel.instruction(
    ["igpdl", "igvdl"],
    outgoing=True,
    supergroups=True,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _instagram_dl(
    client, message
):
    str_link = get_text(
        message,
        save_link=True,
    )
    if not str_link or not (
        is_url(str_link) is True
        or ("instagram" not in str_link)
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

    if message.command[0] == "igpdl":
        photo = Instagram.ig_download(
            ig_url=str_link,
            type_dl="photo",
        )
        if photo:
            caption = "<b><u>INSTAGRAM DOWNLOADER</b></u>\n\nProjects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>\nMade with <a href='https://developers.facebook.com/docs/instagram/'>Meta</a> ( Facebook )"
            await client.send_photo(
                message.chat.id,
                photo=photo,
                caption=caption,
            )
            remove(photo)
            return await _try_purged(x)
        else:
            await eor(
                x,
                text=f"Maybe you mean igvdl ?\n\nTry: <code>.igvdl {str_link}</code>",
            )

    elif message.command[0] == "igvdl":
        video = Instagram.ig_download(
            ig_url=str_link,
            type_dl="video",
        )
        if video:
            caption = "<b><u>INSTAGRAM DOWNLOADER</b></u>\n\nProjects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>\nMade with <a href='https://developers.facebook.com/docs/instagram/'>Meta</a> ( Facebook )"
            await client.send_video(
                message.chat.id,
                video=video,
                caption=caption,
            )
            remove(video)
            return await _try_purged(x)
        else:
            await eor(
                x,
                text=f"Maybe you mean igpdl ?\n\nTry: <code>.igpdl {str_link}</code>",
            )


@pytel.instruction(
    ["pintdl", "pindl"],
    outgoing=True,
    supergroups=True,
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
    if not str_link or not (
        is_url(str_link) is True
        or ("pin" not in str_link)
    ):
        await eor(
            message,
            text="Provide a valid link Pinterest!",
        )
        return
    x = await eor(
        message, text="Processing..."
    )
    type_file, my_pin = Pinterest(
        pin_url=str_link
    )
    if not my_pin:
        await eor(
            x,
            text="Can't find any files, Please try again later!",
        )
        return
    with suppress(Exception):
        caption = "Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>\nMade with <a href='https://developers.pinterest.com/'>Pinterest</a> ( Developers )"
        if type_file == "video":
            await client.send_video(
                message.chat.id,
                video=my_pin,
                caption=caption,
            )
            await _try_purged(x, 1)
            remove(my_pin)
            return
        if type_file == "image":
            await client.send_photo(
                message.chat.id,
                photo=my_pin,
                caption=caption,
            )
            await _try_purged(x, 1)
            return


@pytel.instruction(
    ["tiktokdl", "ttdl"],
    outgoing=True,
    supergroups=True,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _tiktok_dl(client, message):
    str_link = get_text(
        message,
        save_link=True,
    )
    if not str_link or not (
        is_url(str_link) is True
        or (
            "vt"
            or "tiktok" not in str_link
        )
    ):
        await eor(
            message,
            text="Provide a valid link tiktok!",
        )
        return
    x = await eor(
        message, text="Processing..."
    )
    video, audio, description = TikTok(
        tiktok_url=str_link
    )
    if video:
        with suppress(Exception):
            caption = f"{description}\n\nProjects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>\nMade with <a href='https://tiktok.com'>Tiktok</a>"
            await client.send_video(
                message.chat.id,
                video=video,
                caption=caption,
            )
        if audio:
            with suppress(Exception):
                caption = "Projects by <a href='https://t.me/PYTELPremium/47'>PYTEL-Premium 🇮🇩</a>\nMade with <a href='https://tiktok.com'>Tiktok</a>"
                await client.send_audio(
                    message.chat.id,
                    audio=audio,
                    caption=caption,
                )
    else:
        await eor(
            x,
            text="Can't find Tiktok video!",
        )
        return

    return await _try_purged(x, 1)


plugins_helper["socialmedia"] = {
    f"{random_prefixies(px)}igsearch [username ig]": "To get Information User. ( Instagram )",
    f"{random_prefixies(px)}igpdl [url]/[reply link]": "To get Instagram. ( images )",
    f"{random_prefixies(px)}igvdl [url]/[reply link]": "To get Instagram. ( video/reels )",
    f"{random_prefixies(px)}ytsearch [text/reply]": "Search engine for youtube.",
    f"{random_prefixies(px)}ytadl [url]/[reply/text]": "To get Youtube. ( audio/mp3 )",
    f"{random_prefixies(px)}ytvdl [url]/[reply/text]": "To get Youtube. ( video/mp4 )",
    f"{random_prefixies(px)}ggsearch [text/reply]": "Search engine for google.",
    f"{random_prefixies(px)}ttdl [url]/[reply link]": "To get Tiktok. ( video & original audio ) ( Without Watermark )",
    f"{random_prefixies(px)}pintdl [url]/[reply link]": "To get Pinterest. ( images/video )",
}
