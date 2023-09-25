# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from requests import get, Session
from . import (
    ParseMode,
    _try_purged,
    eor,
    get_text,
    is_ipv4,
    is_url,
    plugins_helper,
    px,
    pytel,
    suppress,
    fetch_ipinfo,
    fetch_dns,
    fetch_phonenumbers,
    time,
    progress,
    replied,
    random_prefixies,
    screenshots,)


@pytel.instruction(
    ["webss"],
    outgoing=True,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _screenshots(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid link!",
        )
        return

    x = await eor(
        message,
        text="Take a screenshot...",
    )
    try:
        file = await screenshots(
            url=url,
            download=False,
        )
    except BaseException as excp:
        await eor(
            x,
            text=f"{excp}",
        )
        return

    if file:
        with suppress(Exception):
            u_time = time()
            z = await eor(
                x,
                text="Uploading...",
            )
            await client.send_photo(
                z.chat.id,
                photo=file,
                caption=(
                    "{} [PYTEL](https://github.com/kastaid/pytel)".format(
                        "Made using",
                    )
                    + "\n{} [KASTA ID 🇮🇩](t.me/kastaid)".format(
                        "a Project by",
                    )
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_to_message_id=replied(
                    message
                ),
                progress=progress,
                progress_args=(
                    z,
                    u_time,
                    "`Uploading File!`",
                    "Screenshot Website",
                ),
                disable_notification=True,
            )
            await _try_purged(z, 2.5)
            return
    else:
        await eor(
            x,
            text="Sorry, couldn't capture the screen.",
        )
        return


@pytel.instruction(
    [
        "short_isgd",
        "short_tiny",
        "short_clck",
    ],
    outgoing=True,
)
async def _shorten_url(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid link!",
        )
        return

    x = await eor(
        message,
        text="Shorten...",
    )
    if (
        message.command[0]
        == "short_isgd"
    ):
        rsp = get(
            "https://is.gd/create.php",
            params={
                "format": "simple",
                "url": url,
            },
        )
    elif (
        message.command[0]
        == "short_tiny"
    ):
        rsp = get(
            "http://tinyurl.com/api-create.php",
            params={"url": url},
        )
    elif (
        message.command[0]
        == "short_clck"
    ):
        rsp = get(
            "https://clck.ru/--",
            params={"url": url},
        )

    with suppress(BaseException):
        if not rsp.ok:
            response = rsp.text.strip()
            await eor(x, text=response)
            return
        else:
            response = rsp.text.strip()
            text = "<b><u>SHORTEN URL</b></u>\n"
            text += f" ├ <b>Before:</b> <code>{url}</code>\n"
            text += f" └ <b>After:</b> <code>{response}</code>"
            await eor(x, text=text)
            return


@pytel.instruction(
    ["unshort"],
    outgoing=True,
)
async def _unshortens(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid link/url!",
        )
        return
    x = await eor(
        message,
        text="Unshorten...",
    )
    sessi = Session()
    resp = sessi.head(
        url,
        allow_redirects=True,
        timeout=3,
        stream=True,
    )
    if (
        resp.status_code == 200
        and resp.url
    ):
        text = "<b><u>UNSHORTEN URL</b></u>\n"
        text += f" ├ <b>Before:</b> <code>{url}</code>\n"
        text += f" └ <b>After:</b> <code>{resp.url}</code>"
        await eor(
            x,
            text=text,
        )
        return
    else:
        await eor(
            x,
            text="Please try again later!",
        )


@pytel.instruction(
    ["ipinfo"],
    outgoing=True,
)
async def _ip_info(client, message):
    ipv = get_text(
        message, save_link=False
    )
    if not ipv or not (
        is_ipv4(ipv) is True
    ):
        await eor(
            message,
            text="Provide a valid IP Address!",
        )
        return
    x = await eor(
        message,
        text="Fetches IP Address...",
    )
    str_ip = await fetch_ipinfo(ipv)
    if str_ip:
        await eor(x, text=str_ip)


@pytel.instruction(
    ["dns", "domain"],
    outgoing=True,
)
async def _domain_ns(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid domain url!",
        )
        return
    x = await eor(
        message,
        text="Fetches DNS...",
    )
    dn_server = await fetch_dns(url)
    if dn_server:
        await eor(x, text=dn_server)


@pytel.instruction(
    ["inb", "infonumber"],
    outgoing=True,
)
async def _numbers_info(
    client, message
):
    numb = get_text(
        message,
        get_phone=True,
        save_link=False,
        normal=False,
    )
    if not numb:
        await eor(
            message,
            text="Provide a valid phone number!",
        )
        return
    x = await eor(
        message,
        text="Processing...",
    )
    rsp = fetch_phonenumbers(numb)
    if rsp:
        await client.send_message(
            message.chat.id,
            text=rsp,
            reply_to_message_id=replied(
                message,
            ),
            disable_web_page_preview=True,
        )
        await _try_purged(x)
    else:
        await eor(
            x, text="Try again later!"
        )


plugins_helper["webtools"] = {
    f"{random_prefixies(px)}webss [url]/[reply link]": "To capture the screen on the link.",
    f"{random_prefixies(px)}short_[isgd/tiny/clck] [url]/[reply link]": "To shorten your link/url.",
    f"{random_prefixies(px)}unshort [url]/[reply link]": "To un-shorten your link/url.",
    f"{random_prefixies(px)}dns / {random_prefixies(px)}domain [url]/[reply link]": "To get DNS ( Domain Name Server )",
    f"{random_prefixies(px)}ipinfo [ip address]": "To get Information IP Address.",
    f"{random_prefixies(px)}inb / infonumber [numbers/reply to numbers]": "To get Information Phone Numbers. ( Tracker by Google-libphonenumber )",
}
