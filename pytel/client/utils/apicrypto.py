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
        percent = "+" + percent
    else:
        pass
    text = f"<b>#{coin.upper()} ( <a href='{resp['data']['coins'][0]['coinrankingUrl']}'>Market Cap</a> )</b> | <code>{percent}%</code>\n<pre>"
    text += f"Rank: {int(resp['data']['coins'][0]['rank'])}\n"
    price_now: Union[int, float] = resp[
        "data"
    ]["coins"][0]["price"]
    price = crypto_format(price_now)
    text += f"Price to USD: ${price}\n"
    if resp["data"]["coins"][0][
        "btcPrice"
    ]:
        btcprice = resp["data"][
            "coins"
        ][0]["btcPrice"]
        text += f"Price to BTC: {crypto_format(btcprice)} ₿\n"
    text += f"Market Cap: ${crypto_format(int(resp['data']['coins'][0]['marketCap']))}\n"
    text += f"Volume 24 Hours: ${crypto_format(int(resp['data']['coins'][0]['24hVolume']))}\n"
    high = max(
        resp["data"]["coins"][0][
            "sparkline"
        ]
    )
    low = min(
        resp["data"]["coins"][0][
            "sparkline"
        ]
    )
    text += f"Price High: ${crypto_format(high)}\n"
    text += f"Price Low: ${crypto_format(low)}</pre>"
    return text
