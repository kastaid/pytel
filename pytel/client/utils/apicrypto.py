# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from typing import Optional, Union
from pytelibs import crypto_format
from requests import get
from ...config import RAPID_KEY


def fetch_crypto(
    coin: Optional[str],
) -> Optional[str]:
    hlp = []
    url = "https://coinranking1.p.rapidapi.com/coins"
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "24h",
        "tiers[0]": "1",
        "orderBy": "marketCap",
        "search": coin,
        "orderDirection": "desc",
        "limit": "50",
        "offset": "0",
    }
    headers = {
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com",
    }
    resp = get(
        url,
        headers=headers,
        params=querystring,
    ).json()
    if resp["status"] != "success":
        return f"Can't Fetching data for {coin.upper()}"

    if not resp["data"]["coins"]:
        return f"Can't Fetching data for {coin.upper()}"

    high, low = None, None
    percent = resp["data"]["coins"][0][
        "change"
    ]
    if not percent.startswith("-"):
        prcn = (
            "<code>+"
            + percent
            + "%</code> 🟢"
        )
    else:
        prcn = (
            "<code>"
            + percent
            + "%</code> 🔴"
        )
    text = f"<b>#{coin.upper()} ( <a href='{resp['data']['coins'][0]['coinrankingUrl']}'>Market Cap</a> )</b>\n"
    text += f"<b>Rank:</b> {int(resp['data']['coins'][0]['rank'])}\n"
    text += f"<b>Percentage Today:</b> {prcn}\n"
    price_now: Union[int, float] = resp[
        "data"
    ]["coins"][0]["price"]
    price = crypto_format(price_now)
    text += f"<b>Price to USD:</b> <code>${price}</code>\n"
    if resp["data"]["coins"][0][
        "btcPrice"
    ]:
        btcprice = resp["data"][
            "coins"
        ][0]["btcPrice"]
        text += f"<b>Price to BTC:</b> {btcprice} ₿\n"
    text += f"<b>Market Cap:</b> <code>${crypto_format(int(resp['data']['coins'][0]['marketCap']))}</code>\n"
    text += f"<b>Volume 24 Hours:</b> <code>${crypto_format(int(resp['data']['coins'][0]['24hVolume']))}</code>\n"
    for x in resp["data"]["coins"][0][
        "sparkline"
    ]:
        if x is None:
            pass
        else:
            hlp.append(x)
    prc = list(hlp)
    high = max(map(str, list(prc)))
    low = min(map(str, list(prc)))
    text += f"<b>Price High:</b> <code>${crypto_format(high)}</code>\n"
    text += f"<b>Price Low:</b> <code>${crypto_format(low)}</code>"
    return text
