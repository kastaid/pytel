# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import sleep
from contextlib import suppress
from datetime import date
from html import escape
from math import floor
from os import path, remove
from random import choice
from subprocess import (
    SubprocessError,
    run,)
from textwrap import wrap
from time import time
from typing import (
    List,
    Optional,
    Union,
    Any,)
from uuid import uuid4
import cv2
import numpy as np
import qrcode
from PIL import (
    Image,
    ImageDraw,
    ImageFont,)
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageNotModified,)
from pyrogram.errors.exceptions.flood_420 import (
    FloodWait,)
from pytelibs import (
    _i,
    replace_all,
    _CHARACTER_NAMES,
    SIZE_UNITS,)
from pytz import timezone
from pyzbar import pyzbar
from qrcode.image.styledpil import (
    StyledPilImage,)
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask,)
from pytel.config import TimeZone
from pytel.logger import (
    pylog as send_log,)
from .helper import MediaInformation

tz = timezone(TimeZone)


def gg_restricted() -> None:
    with suppress(Exception):
        RunningCommand(_i)


def get_random_hex(
    length: int = 12,
) -> str:
    return uuid4().hex[:length]


def random_prefixies(
    px: Union[str, List[str]]
) -> Optional[str]:
    if px:
        prefixies = choice(px)
    return str(prefixies)


async def mentioned(
    client,
    user_id,
    use_html: bool = None,
) -> str:
    is_user = False
    sep: str = ""
    try:
        user = await client.get_users(
            user_id
        )
        fname = (
            hasattr(user, "last_name")
            and user.last_name
            and f"{sep}{user.first_name} {user.last_name}"
            or f"{sep}{user.first_name}"
        )
        is_user = True
    except BaseException:
        try:
            chats = (
                await client.get_chat(
                    user_id
                )
            )
            fname = chats.title
        except BaseException:
            fname = "Anonymous"
            is_user = True

    fullname = " ".join(
        replace_all(
            escape(fname)
            if use_html
            else fname,
            _CHARACTER_NAMES,
        ).split()
    )
    if is_user:
        if use_html:
            return "<a href=tg://user?id={}>➦{}</a>".format(
                user_id,
                fullname,
            )
        return "[➦{}](tg://user?id={})".format(
            fullname,
            user_id,
        )
    else:
        if str(user_id).startswith("-"):
            user_id = str(
                user_id
            ).replace("-100", "")
        if use_html:
            return "<a href=t.me/c/{}/1?single&thread=>➦{}</a>".format(
                int(user_id),
                fullname,
            )
        return "[➦{}](t.me/c/{}/1?single&thread=)".format(
            fullname,
            int(user_id),
        )


def short_dict(
    dct: Optional[dict],
    reverse: Optional[bool] = False,
) -> Optional[dict]:
    return dict(
        sorted(
            dct.items(), reverse=reverse
        )
    )


def humanboolean(
    x: Optional[bool] = False,
) -> Optional[str]:
    return "Yes" if x else "No"


def time_formatter(
    ms: Union[int, float]
) -> str:
    (
        minutes,
        seconds,
    ) = divmod(
        int(ms / 1000),
        60,
    )
    (
        hours,
        minutes,
    ) = divmod(minutes, 60)
    (
        days,
        hours,
    ) = divmod(hours, 24)
    (
        weeks,
        days,
    ) = divmod(days, 7)
    tmp = (
        (
            (str(weeks) + "wk, ")
            if weeks
            else ""
        )
        + (
            (str(days) + "dy, ")
            if days
            else ""
        )
        + (
            (str(hours) + "hr, ")
            if hours
            else ""
        )
        + (
            (str(minutes) + "min, ")
            if minutes
            else ""
        )
        + (
            (str(seconds) + "sec, ")
            if seconds
            else ""
        )
    )
    return tmp and tmp[:-2] or "0sec"


def RunningCommand(
    cmd: Optional[str],
) -> (str, str):
    try:
        process = run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
        )
        (
            stdout,
            stderr,
        ) = (
            process.stdout,
            process.stderr,
        )
        return str(stdout), str(stderr)
    except SubprocessError as excp:
        send_log.error(excp)


def size_bytes(size_in_bytes):
    if size_in_bytes is None:
        return "0B"
    index = 0
    while (
        size_in_bytes >= 1024
        and index < len(SIZE_UNITS) - 1
    ):
        size_in_bytes /= 1024
        index += 1
    return (
        f"{size_in_bytes:.2f}{SIZE_UNITS[index]}"
        if index > 0
        else f"{size_in_bytes}B"
    )


def subs_like_view_format(
    num_count: Union[int, float],
    precision=2,
) -> Optional[str]:
    suffixes = [
        "",
        "K",
        "M",
        "B",
        "T",
        "Q",
    ]
    m = sum(
        [
            abs(num_count / 1000.0**x)
            >= 1
            for x in range(
                1, len(suffixes)
            )
        ]
    )
    return f"{num_count/1000.0**m:.{precision}f}{suffixes[m]}"


def int2date(
    argdate: Optional[int],
) -> Optional[Any]:
    year = int(argdate / 10000)
    month = int((argdate % 10000) / 100)
    day = int(argdate % 100)
    return date(
        year, month, day
    ).strftime("%d %B %Y")


def resize_images(image):
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = floor(size1new)
        size2new = floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    file_name = (
        f"image_{get_random_hex()}.png"
    )
    im.save(file_name, "PNG")
    if path.exists(image):
        remove(image)
    return file_name


def resize_media(
    media: str,
    video: bool,
    fast_forward: bool,
) -> str:
    if video:
        info_ = MediaInformation.data(
            media
        )
        width = info_["pixel_sizes"][0]
        height = info_["pixel_sizes"][1]
        sec = info_["duration_in_ms"]
        s = round(float(sec)) / 1000

        if height == width:
            height, width = 512, 512
        elif height > width:
            height, width = 512, -1
        elif width > height:
            height, width = -1, 512

        resized_video = f"{media}.webm"
        if fast_forward:
            if s > 3:
                fract_ = 3 / s
                ff_f = round(fract_, 2)
                set_pts_ = (
                    ff_f - 0.01
                    if ff_f > fract_
                    else ff_f
                )
                cmd_f = f"-filter:v 'setpts={set_pts_}*PTS',scale={width}:{height}"
            else:
                cmd_f = f"-filter:v scale={width}:{height}"
        else:
            cmd_f = f"-filter:v scale={width}:{height}"
        fps_ = float(
            info_["frame_rate"]
        )
        fps_cmd = (
            "-r 30 "
            if fps_ > 30
            else ""
        )
        cmd = f"ffmpeg -i {media} {cmd_f} -ss 00:00:00 -to 00:00:03 -an -c:v libvpx-vp9 {fps_cmd}-fs 256K {resized_video}"
        RunningCommand(cmd)
        remove(media)
        return resized_video

    image = Image.open(media)
    maxsize = 512
    scale = maxsize / max(
        image.width, image.height
    )
    new_size = (
        int(image.width * scale),
        int(image.height * scale),
    )

    image = image.resize(
        new_size, Image.LANCZOS
    )
    resized_photo = (
        f"media_{get_random_hex()}.png"
    )
    image.save(resized_photo)
    remove(media)
    return resized_photo


def Memify(image_path, text):
    font_size = 12
    stroke_width = 1

    if ";" in text:
        (
            upper_text,
            lower_text,
        ) = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(
        image_path
    ).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="./resources/fonts/aria.ttf",
        size=int(
            image_height * font_size
        )
        // 100,
    )
    draw = ImageDraw.Draw(img)

    (
        char_width,
        char_height,
    ) = font.getsize("A")
    chars_per_line = (
        image_width // char_width
    )
    top_lines = wrap(
        upper_text, width=chars_per_line
    )
    bottom_lines = wrap(
        lower_text, width=chars_per_line
    )

    if top_lines:
        y = 10
        for line in top_lines:
            (
                line_width,
                line_height,
            ) = font.getsize(line)
            x = (
                image_width - line_width
            ) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = (
            image_height
            - char_height
            * len(bottom_lines)
            - 15
        )
        for line in bottom_lines:
            (
                line_width,
                line_height,
            ) = font.getsize(line)
            x = (
                image_width - line_width
            ) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = path.join(
        "memify.webp"
    )
    img.save(final_image, **img_info)
    return final_image


def making_code(
    client, data, type_file: str
):
    Logo = "resources/kastaid/PYTEL_CODE.jpg"
    logo = Image.open(Logo)
    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = basewidth / float(
        logo.size[0]
    )
    hsize = int(
        (
            float(logo.size[1])
            * float(wpercent)
        )
    )
    logo = logo.resize(
        (basewidth, hsize),
        Image.ANTIALIAS,
    )
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    # adding URL or text to QRcode
    QRcode.add_data(data)
    # generating QR code
    QRcode.make(fit=True)
    QRimg = QRcode.make_image(
        image_factory=StyledPilImage,
        color_mask=RadialGradiantColorMask(),
    )

    # set size of QR code
    pos = (
        (QRimg.size[0] - logo.size[0])
        // 2,
        (QRimg.size[1] - logo.size[1])
        // 2,
    )
    QRimg.paste(logo, pos)

    # save the QR code generated
    output = f"{client.me.id}_code.{type_file}"
    QRimg.save(output)
    return output


async def scanner_code(
    files, type_file: str
):
    image = cv2.imread(files)
    image = cv2.resize(
        image, (640, 850)
    )

    # decode and detect the QR codes and barcodes
    barcodes = pyzbar.decode(image)
    qr_code, code = 0, 0

    if len(barcodes) == 0:
        text = "No barcode found on this image"
        return text

    text = "<b><u>Scanner Code</b></u> ( Barcode / QR Code )\n\n"
    for barcode in barcodes:
        # extract the points of th polygon of the barcode and create a Numpy array
        pts = np.array(
            [barcode.polygon], np.int32
        )
        pts = pts.reshape((-1, 1, 2))

        # check to see if this is a QR code or a barcode
        if barcode.type == "QRCODE":
            qr_code += 1
        elif barcode.type == "CODE128":
            code += 1

        text += "<b>Code:</b> <code>{}</code>\n\n".format(
            barcode.data.decode("utf-8")
        )

    if int(qr_code) != 0:
        text += "{} QR code(s) found on this {}\n".format(
            qr_code,
            type_file,
        )
    if int(code) != 0:
        text += "{} barcode(s) found on this {}\n".format(
            code,
            type_file,
        )

    return text


async def progress(
    current,
    total,
    message,
    start,
    type_of_ps,
    file_name=None,
):
    now = time()
    diff = now - start
    if (
        round(diff % 10.00) == 0
        or current == total
    ):
        percentage = (
            current * 100 / total
        )
        speed = current / diff
        elapsed_time = (
            round(diff) * 1000
        )
        if elapsed_time == 0:
            return
        time_to_completion = (
            round(
                (total - current)
                / speed
            )
            * 1000
        )
        estimated_total_time = (
            elapsed_time
            + time_to_completion
        )
        progress_str = (
            "{0}{1} {2}%\n".format(
                "".join(
                    "🟢"
                    for _ in range(
                        floor(
                            percentage
                            / 10
                        )
                    )
                ),
                "".join(
                    "🔘"
                    for _ in range(
                        10
                        - floor(
                            percentage
                            / 10
                        )
                    )
                ),
                round(percentage, 2),
            )
        )
        tmp = (
            progress_str
            + "{0} of {1}\nETA: {2}".format(
                size_bytes(current),
                size_bytes(total),
                time_formatter(
                    estimated_total_time
                ),
            )
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**File Name:** `{}`\n{}".format(
                        type_of_ps,
                        file_name,
                        tmp,
                    )
                )
            except FloodWait as flood:
                await sleep(flood.value)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit(
                    "{}\n{}".format(
                        type_of_ps, tmp
                    )
                )
            except FloodWait as flood:
                await sleep(flood.value)
            except MessageNotModified:
                pass
