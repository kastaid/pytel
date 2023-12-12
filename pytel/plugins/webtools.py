# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from requests import (
    get,
    Session,)
from . import (
    ParseMode,
    _try_purged,
    eor,
    get_text,
    links_checker,
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

_PHISHING_TEXT = """
<b><u>LINKS CHECKER</u></b>

<b>{}
"""


@pytel.instruction(
    [
        "dclink",
        "devclinks",
    ],
    supersu=["PYTEL"],
)
@pytel.instruction(
    [
        "clink",
        "clinks",
        "checklinks",
    ],
    outgoing=True,
)
async def _check_phishing(
    client, message
):
    url = get_text(
        message,
        save_link=True,
    )
    if not url or not (
        is_url(url)
        is True
    ):
        await eor(
            message,
            text="Provide a valid link!",
        )
        return

    x = await eor(
        message,
        text="Checking...",
    )
    resp = await links_checker(
        url
    )
    if resp:
        await eor(
            x,
            text=resp,
        )
    else:
        await eor(
            x,
            text="Can't fetches",
        )


@pytel.instruction(
    ["webss"],
    outgoing=True,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _screenshots(
    client, message
):
    url = get_text(
        message,
        save_link=True,
    )
    if not url or not (
        is_url(url)
        is True
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
    except (
        BaseException
    ) as excp:
        await eor(
            x,
            text=f"{excp}",
        )
        return

    if file:
        with suppress(
            Exception
        ):
            u_time = (
                time()
            )
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
                    "Uploading File!",
                    "Screenshot Website",
                ),
                disable_notification=True,
            )
            await _try_purged(
                z, 2.5
            )
            return
    else:
        await eor(
            x,
            text="Sorry, couldn't capture the screen.",
        )
        return


@pytel.instruction(
    [
        "dshort_isgd",
        "dshort_tiny",
        "dshort_clck",
    ],
    supersu=["PYTEL"],
)
@pytel.instruction(
    [
        "short_isgd",
        "short_tiny",
        "short_clck",
    ],
    outgoing=True,
)
async def _shorten_url(
    client, message
):
    url = get_text(
        message,
        save_link=True,
    )
    if not url or not (
        is_url(url)
        is True
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
        message.command[
            0
        ]
        == "short_isgd"
        or "dshort_isgd"
    ):
        rsp = get(
            "https://is.gd/create.php",
            params={
                "format": "simple",
                "url": url,
            },
        )
    elif (
        message.command[
            0
        ]
        == "short_tiny"
        or "dshort_tiny"
    ):
        rsp = get(
            "http://tinyurl.com/api-create.php",
            params={
                "url": url
            },
        )
    elif (
        message.command[
            0
        ]
        == "short_clck"
        or "dshort_clck"
    ):
        rsp = get(
            "https://clck.ru/--",
            params={
                "url": url
            },
        )

    with suppress(
        BaseException
    ):
        if not rsp.ok:
            response = (
                rsp.text.strip()
            )
            await eor(
                x,
                text=response,
            )
            return
        else:
            response = (
                rsp.text.strip()
            )
            text = "<b><u>SHORTEN URL</b></u>\n"
            text += f" ├ <b>Before:</b> <code>{url}</code>\n"
            text += f" └ <b>After:</b> <code>{response}</code>"
            await eor(
                x,
                text=text,
            )
            return


@pytel.instruction(
    ["dunshort"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["unshort"],
    outgoing=True,
)
async def _unshortens(
    client, message
):
    url = get_text(
        message,
        save_link=True,
    )
    if not url or not (
        is_url(url)
        is True
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
        resp.status_code
        == 200
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
    ["dipinfo"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["ipinfo"],
    outgoing=True,
)
async def _ip_information(
    client, message
):
    ipv = get_text(
        message,
        save_link=False,
    )
    if not ipv or not (
        is_ipv4(ipv)
        is True
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
    str_ip = await fetch_ipinfo(
        ipv
    )
    if str_ip:
        await eor(
            x,
            text=str_ip,
        )


@pytel.instruction(
    [
        "ddns",
        "devdomain",
    ],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["dns", "domain"],
    outgoing=True,
)
async def _domain_ns(
    client, message
):
    url = get_text(
        message,
        save_link=True,
    )
    if not url or not (
        is_url(url)
        is True
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
    dn_server = (
        await fetch_dns(
            url
        )
    )
    if dn_server:
        await eor(
            x,
            text=dn_server,
        )


@pytel.instruction(
    [
        "dinb",
        "devinfonumber",
    ],
    supersu=["PYTEL"],
)
@pytel.instruction(
    [
        "inb",
        "infonumber",
    ],
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
    rsp = fetch_phonenumbers(
        numb
    )
    if rsp:
        await client.send_message(
            message.chat.id,
            text=rsp,
            reply_to_message_id=replied(
                message,
            ),
            disable_web_page_preview=True,
        )
        await _try_purged(
            x
        )
    else:
        await eor(
            x,
            text="Try again later!",
        )


plugins_helper[
    "webtools"
] = {
    f"{random_prefixies(px)}clinks / checklinks [links/reply to message links]": "To check malicious links. ( Phishing )",
    f"{random_prefixies(px)}webss [url]/[reply link]": "To capture the screen on the link.",
    f"{random_prefixies(px)}short_[isgd/tiny/clck] [url]/[reply link]": "To shorten your link/url.",
    f"{random_prefixies(px)}unshort [url]/[reply link]": "To un-shorten your link/url.",
    f"{random_prefixies(px)}dns / domain [url]/[reply link]": "To get DNS ( Domain Name Server )",
    f"{random_prefixies(px)}ipinfo [ip address]": "To get Information IP Address.",
    f"{random_prefixies(px)}inb / infonumber [numbers/reply to numbers]": "To get Information Phone Numbers. ( Tracker by Google-libphonenumber )",
}
