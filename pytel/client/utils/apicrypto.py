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

    text = f"#{coin.upper()} ( Market Cap )\n"
    text += f"Rank: {int(resp['data']['coins'][0]['rank'])}\n"
    price: Union[int, float] = resp[
        "data"
    ]["coins"][0]["price"]
    price = crypto_format(price)
    text += f"USD Price: ${price}\n"
    if resp["data"]["coins"][0][
        "btcPrice"
    ]:
        btcprice = resp["data"][
            "coins"
        ][0]["btcPrice"]
        text += f"BTC Price: {crypto_format(btcprice)} ₿\n"
    text += f"Market Cap: ${crypto_format(int(resp['data']['coins'][0]['marketCap']))}\n"
    text += f"Volume 24 Hours: ${crypto_format(int(resp['data']['coins'][0]['24hVolume']))} | {resp['data']['coins'][0]['change']}%"
    return text
