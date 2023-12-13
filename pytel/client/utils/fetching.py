# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

import re
from asyncio import sleep
from base64 import (
    b64decode,)
from datetime import (
    datetime,)
from io import BytesIO
from sys import (
    version_info,)
from time import (
    perf_counter,)
from typing import (
    Any,
    Optional,
    Set,
    Tuple,
    Union,)
from urllib.parse import (
    urlparse as urllibparse,)
import phonenumbers
from aiofiles import open
from aiohttp import (
    ClientSession,
    __version__,)
from asyncache import (
    cached,)
from cachetools import (
    TTLCache,)
from phonenumbers import (
    geocoder,
    carrier,
    timezone as phtimezone,)
from phonenumbers.carrier import (
    _is_mobile,)
from pytelibs import (
    WEATHER_ICONS,)
from pytz import (
    country_timezones,
    timezone,
    country_names,)
from version import (
    __version__ as versi,)
from ...config import (
    IPQUALITY_KEY,)
from .misc import (
    humanboolean,)

_SPAMWATCH_CACHE = TTLCache(
    maxsize=512,
    ttl=120,
    timer=perf_counter,
)  # 2 mins
_CAS_CACHE = TTLCache(
    maxsize=512,
    ttl=120,
    timer=perf_counter,
)  # 2 mins


async def fetching(
    url: Optional[str],
    post: Optional[
        bool
    ] = None,
    headers: Optional[
        dict
    ] = None,
    params: Optional[
        dict
    ] = None,
    json: Optional[
        dict
    ] = None,
    data: Optional[
        dict
    ] = None,
    ssl: Any = None,
    re_json: bool = False,
    re_content: bool = False,
    real: bool = False,
    statuses: Optional[
        Set[int]
    ] = None,
    *args,
    **kwargs,
) -> Any:
    statuses = (
        statuses or {}
    )
    if not headers:
        headers = {
            "User-Agent": "Python/{}.{} aiohttp/{} pytel/{}".format(
                version_info[
                    0
                ],
                version_info[
                    1
                ],
                __version__,
                versi,
            )
        }
    async with ClientSession(
        headers=headers
    ) as session:
        try:
            if post:
                resp = await session.post(
                    url=url,
                    json=json,
                    data=data,
                    ssl=ssl,
                    raise_for_status=False,
                    *args,
                    **kwargs,
                )
            else:
                resp = await session.get(
                    url=url,
                    params=params,
                    ssl=ssl,
                    raise_for_status=False,
                    *args,
                    **kwargs,
                )
        except (
            BaseException
        ):
            return None
        if (
            resp.status
            not in {
                *{
                    200,
                    201,
                },
                *statuses,
            }
        ):
            return None
        if re_json:
            return await resp.json(
                content_type=None
            )
        if re_content:
            return (
                await resp.read()
            )
        if real:
            return resp
        return (
            await resp.text()
        )


@cached(
    TTLCache(
        maxsize=1024,
        ttl=(120 * 30),
        timer=perf_counter,
    )
)  # 1 hours
async def get_blacklisted(
    url: str,
    is_json: bool = False,
    attempts: int = 3,
    fallbacks: Optional[
        Tuple[
            Union[
                int,
                str,
            ]
        ]
    ] = None,
) -> Set[
    Union[int, str]
]:
    count = 0
    is_content = (
        not is_json
    )
    while (
        count < attempts
    ):
        res = await fetching(
            url,
            re_json=is_json,
            re_content=is_content,
        )
        count += 1
        if not res:
            if (
                count
                != attempts
            ):
                await sleep(
                    1
                )
                continue
            ids = (
                fallbacks
                or []
            )
            break
        if is_content:
            reg = r"[^\s#,\[\]\{\}]+"
            data = re.findall(
                reg,
                res.decode(
                    "utf-8"
                ),
            )
            ids = [
                int(x)
                for x in data
                if x.isdecimal()
                or (
                    x.startswith(
                        "-"
                    )
                    and x[
                        1:
                    ].isdecimal()
                )
            ]
        else:
            ids = list(
                res
            )
        break
    return set(ids)


def fetch_phonenumbers(
    number: Optional[
        str
    ] = None,
) -> Optional[str]:
    text = "<b><u>PHONE NUMBER INFORMATION</b></u>\n"
    phoneNumber = phonenumbers.parse(
        number
    )
    # Using the geocoder module of phonenumbers to print the Location in console
    yourLocation = geocoder.description_for_number(
        phoneNumber, "id"
    )
    if not yourLocation:
        return "Phone numbers invalid!"

    text += f"├ <b>Numbers:</b> <code>{number}</code>\n"
    text += f"├ <b>Country:</b> {yourLocation}\n"
    # Using the carrier module of phonenumbers to print the service provider name in console
    yourServiceProvider = carrier.name_for_number(
        phoneNumber, "id"
    )
    text += f"├ <b>Provider:</b> {yourServiceProvider}\n"

    # timezone
    zone = phtimezone.time_zones_for_geographical_number(
        phoneNumber
    )
    text += f"├ <b>Timezone:</b> {zone[0]}\n"

    # is Mobile
    mbl = _is_mobile(
        number
    )
    if mbl:
        text += f"└ <b>Mobile:</b> {mbl}"
    else:
        text += "└ <b>Mobile:</b> <code>Yes</code>\n\n"

    text += "<b>Tracker by</b> ( <b><a href='https://github.com/google'>Google-libphonenumber</a></b> )"
    return str(text)


async def screenshots(
    url: Optional[str],
    file_name: Optional[
        str
    ] = "web-screenshot",
    download: Optional[
        bool
    ] = False,
) -> Any:
    payload = {
        "url": url,
        "width": 1280,
        "height": 1080,
        "scale": 1,
        "format": "jpeg",
    }
    response = await fetching(
        url="https://webscreenshot.vercel.app/api",
        post=True,
        data=payload,
        re_json=True,
    )
    if not response:
        return None
    getpic = response[
        "image"
    ].replace(
        "data:image/jpeg;base64,",
        "",
    )
    file_name = f"{file_name}.jpg"
    if not download:
        file = BytesIO(
            b64decode(
                getpic
            )
        )
        file.name = (
            file_name
        )
    else:
        file = (
            "cache/"
            + file_name
        )
        async with open(
            file,
            mode="wb",
        ) as f:
            await f.write(
                response
            )
            await f.close()

    return file


async def fetch_adzan(
    str_city: Optional[
        str
    ],
) -> Optional[str]:
    url = f"https://muslimsalat.com/{str_city}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    response = (
        await fetching(
            url,
            re_json=True,
        )
    )
    if not response:
        text = "{}!".format(
            "Try again later!",
        )
        return text
    if (
        response[
            "status_code"
        ]
        == 0
    ):
        text = (
            "{}".format(
                "Cannot retrieve adhan data for",
            )
            + f"<u>{str_city}</u>, "
            + "{}".format(
                "please check again.",
            )
        )
    else:
        timefor = f"""
<u>{str(response['query']).capitalize()}, {response['country']}, {response['items'][0]['date_for']}.</u>
"""
        cordinates = f"{response['latitude'] or ''},{response['longitude'] or ''}"
        maps = f"https://www.google.com/maps?q={cordinates}"
        celci = (
            f"{response['today_weather']['temperature']}"
            if response[
                "today_weather"
            ][
                "temperature"
            ]
            else 0
        )
        temperature = (
            "N/A"
            if celci == 0
            else f"{str(celci)}°C | {str(fahrenheit(celci))}°F"
        )
        text = (
            "<b>"
            + "{}".format(
                "Islamic Prayer Times",
            )
            + "</b>\n"
        )
        text += f"{timefor}├ <b>Fajr</b> ❯ <code>{response['items'][0]['fajr']}</code>\n"
        text += f"├ <b>Shurooq</b> ❯ <code>{response['items'][0]['shurooq']}</code>\n"
        text += f"├ <b>Dhuhr</b> ❯ <code>{response['items'][0]['dhuhr']}</code>\n"
        text += f"├ <b>Asr</b> ❯ <code>{response['items'][0]['asr']}</code>\n"
        text += f"├ <b>Maghrib</b> ❯ <code>{response['items'][0]['maghrib']}</code>\n"
        text += f"└ <b>Isha</b> ❯ <code>{response['items'][0]['isha']}</code>\n\n"
        text += (
            "<u>"
            + "{}".format(
                "Additional",
            )
            + "</u>\n"
        )
        text += (
            "├ <b>"
            + "{}".format(
                "Code Country"
            )
            + f"</b> ❯ <code>{response['country_code']}</code>\n"
        )
        text += (
            "├ <b>"
            + "{}".format(
                "Temperature",
            )
            + f"</b> ❯ <code>{temperature}</code>\n"
        )
        text += (
            "├ <b>"
            + "{}".format(
                "Cordinates",
            )
            + f"</b> ❯ <code>{cordinates}</code>\n"
        )
        text += f"└ <b>Maps</b> ❯ <code>{maps}</code>"

    return str(text)


async def fetch_ipinfo(
    str_ip: Optional[
        str
    ],
) -> Optional[str]:
    url = f"http://ip-api.com/json/{str_ip}?fields=status,message,continent,country,countryCode,regionName,city,zip,lat,lon,timezone,currency,isp,mobile,query"
    response = (
        await fetching(
            url,
            re_json=True,
        )
    )
    if not response:
        text = (
            "{}".format(
                "Try again now"
            )
            + "!"
        )
        return text
    if (
        str(
            response.get(
                "status"
            )
        ).lower()
        == "success"
    ):
        coordinates = (
            str(
                response.get(
                    "lat"
                )
                or ""
            )
            + ","
            + str(
                response.get(
                    "lon"
                )
                or ""
            )
        )
        query = (
            response.get(
                "query"
            )
        )
        city = (
            response.get(
                "city"
            )
            or "?"
        )
        regional_name = (
            response.get(
                "regionName"
            )
            or "?"
        )
        country = (
            response.get(
                "country"
            )
            or "?"
        )
        country_code = (
            response.get(
                "countryCode"
            )
            or "?"
        )
        currency = (
            response.get(
                "currency"
            )
            or "?"
        )
        continent = (
            response.get(
                "continent"
            )
            or "?"
        )
        cc_timezone = (
            response.get(
                "timezone"
            )
            or "?"
        )
        isp_ = (
            response.get(
                "isp"
            )
            or "?"
        )
        is_mobile = humanboolean(
            response.get(
                "mobile"
            )
        )
        gmaps = f"https://www.google.com/maps?q={coordinates}"

        text = (
            "<b><u>"
            + "{}".format(
                "IP Address Information"
            )
            + "</u></b>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "IP"
            )
            + f":</b> <code>{query}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "City"
            )
            + f":</b> <code>{city}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Region"
            )
            + f":</b> <code>{regional_name}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Country"
            )
            + f":</b> <code>{country}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Country Code"
            )
            + f":</b> <code>{country_code}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Currency"
            )
            + f":</b> <code>{currency}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Continent"
            )
            + f":</b> <code>{continent}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Coordinates"
            )
            + f":</b> <code>{coordinates}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Time Zone"
            )
            + f":</b> <code>{cc_timezone}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "ISP"
            )
            + f":</b> <code>{isp_}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Mobile"
            )
            + f":</b> <code>{is_mobile}</code>\n"
        )
        text += (
            "└  <b>"
            + "{}".format(
                "Map"
            )
            + f":</b> <code>{gmaps}</code>\n"
        )
    else:
        query = (
            response.get(
                "query"
            )
        )
        status = (
            response.get(
                "status"
            )
        )
        message = (
            response.get(
                "message"
            )
        )
        text = (
            "<b><u>"
            + "{}".format(
                "IP Address Information"
            )
            + "</u></b>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "IP"
            )
            + f":</b> <code>{query}</code>\n"
        )
        text += (
            "├  <b>"
            + "{}".format(
                "Status"
            )
            + f":</b> <code>{status}</code>\n"
        )
        text += (
            "└  <b>"
            + "{}".format(
                "Message"
            )
            + f":</b> <code>{message}</code>\n"
        )
    return text


async def fetch_weather(
    str_city: Optional[
        str
    ],
) -> Optional[str]:
    tz_countries = {
        tz: country
        for country, tzs in country_timezones.items()
        for tz in tzs
    }

    if "," in str_city:
        new_str_city = str_city.split(
            ","
        )
        if (
            len(
                new_str_city[
                    1
                ]
            )
            == 2
        ):
            str_city = (
                new_str_city[
                    0
                ].strip()
                + ","
                + new_str_city[
                    1
                ].strip()
            )
        else:
            country = await get_timezone(
                (
                    new_str_city[
                        1
                    ].strip()
                ).title()
            )
            try:
                countrycode = tz_countries[
                    f"{country}"
                ]
            except (
                KeyError
            ):
                text = "{}".format(
                    "Invalid country."
                )
                return (
                    text
                )
            str_city = (
                new_str_city[
                    0
                ].strip()
                + ","
                + countrycode.strip()
            )

    url = f"https://api.openweathermap.org/data/2.5/weather?q={str_city}&appid=439141654b1019a49e73e5118c6cfd0b"
    response = (
        await fetching(
            url,
            re_json=True,
        )
    )
    if not response:
        text = "{}".format(
            "Cannot retrieve region, please check again."
        )
        return text

    desc = response[
        "weather"
    ][0]["description"]
    wic = response[
        "weather"
    ][0]["icon"]
    ico = dict(
        filter(
            lambda item: wic
            in item[0],
            WEATHER_ICONS.items(),
        )
    )
    icon = ico.get(wic)
    if wic.endswith("n"):
        icons = (
            icon
            + " ( <u>Night</u> ) 🌙"
        )
    else:
        icons = (
            icon
            + " ( <u>Day</u> ) ☀️"
        )
    cityname = response[
        "name"
    ]
    curtemp = response[
        "main"
    ]["temp"]
    humidity = response[
        "main"
    ]["humidity"]
    min_temp = response[
        "main"
    ]["temp_min"]
    max_temp = response[
        "main"
    ]["temp_max"]
    country = response[
        "sys"
    ]["country"]
    sunrise = response[
        "sys"
    ]["sunrise"]
    sunset = response[
        "sys"
    ]["sunset"]
    wind = response[
        "wind"
    ]["speed"]
    winddir = response[
        "wind"
    ]["deg"]

    ctimezone = timezone(
        country_timezones[
            country
        ][
            0
        ]
    )
    time = datetime.now(
        ctimezone
    ).strftime(
        "%A, %H:%M:%S"
    )
    fullcountry_names = (
        country_names[
            f"{country}"
        ]
    )
    dirs = [
        "N",
        "NE",
        "E",
        "SE",
        "S",
        "SW",
        "W",
        "NW",
    ]

    div = 360 / len(dirs)
    funmath = int(
        (
            winddir
            + (div / 2)
        )
        / div
    )
    findir = dirs[
        funmath
        % len(dirs)
    ]
    kmph = str(
        wind * 3.6
    ).split(".")
    mph = str(
        wind * 2.237
    ).split(".")

    def wt_fahrenheit(
        f,
    ):
        temp = str(
            (
                (
                    f
                    - 273.15
                )
                * 9
                / 5
                + 32
            )
        ).split(".")
        return temp[0]

    def wt_celsius(c):
        temp = str(
            (c - 273.15)
        ).split(".")
        return temp[0]

    def wt_sun(unix):
        xx = datetime.fromtimestamp(
            unix,
            tz=ctimezone,
        ).strftime(
            "%H:%M:%S"
        )
        return xx

    text = (
        "<u>"
        + "{}".format(
            "WEATHER INFORMATION"
        )
        + "</u>\n"
    )
    text += (
        "├ <b>"
        + "Temperature"
        + f":</b> {wt_celsius(curtemp)}°C | {wt_fahrenheit(curtemp)}°F\n"
    )
    text += f"├ <b>Min. Temp.:</b> {wt_celsius(min_temp)}°C | {wt_fahrenheit(min_temp)}°F\n"
    text += f"├ <b>Max. Temp.:</b> {wt_celsius(max_temp)}°C | {wt_fahrenheit(max_temp)}°F\n"
    text += (
        "├ <b>"
        + "{}".format(
            "Humidity"
        )
        + f":</b> {humidity}%\n"
    )
    text += "┌─────────────────────\n"
    text += (
        "├ <b>"
        + "{}".format(
            "Wind"
        )
        + f":</b> {kmph[0]} kmh | {mph[0]} mph, {findir}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Sunrise"
        )
        + f":</b> {wt_sun(sunrise)}\n"
    )
    text += (
        "└ <b>"
        + "{}".format(
            "Sunset"
        )
        + f":</b> {wt_sun(sunset)}\n\n"
    )
    text += f"<u><b>{desc.capitalize()}</b></u> {str(icons)}\n"
    text += f"└ {cityname}, {fullcountry_names} {time}"
    text += f"\n\n(c) 2023-present kastaid #pytel"

    return text


async def fetch_dns(
    domain_str: Optional[
        str
    ],
) -> Optional[str]:
    hostname = ".".join(
        urllibparse(
            domain_str
        ).netloc.split(
            "."
        )[
            -2:
        ]
    )
    url = f"https://da.gd/dns/{hostname}"
    response = (
        await fetching(
            url
        )
    )
    if not response:
        text = (
            "{}".format(
                "Can't fetches"
            )
            + f" <b>{hostname}</b> DNS."
        )
    else:
        text = (
            "<b>DNS "
            + "{}".format(
                "records"
            )
            + f" {hostname}</b>\n\n<pre>{response.strip()}</pre>"
        )

    return text


async def links_checker(
    message: Optional[
        str
    ],
) -> Optional[str]:
    if not IPQUALITY_KEY:
        return "Please visit ipqualityscore.com to get API_KEY"

    url = f"https://ipqualityscore.com/api/json/url?key={IPQUALITY_KEY}&url={message}"
    links = (
        await fetching(
            url,
            re_json=True,
        )
    )
    if links:
        text = "<b><u>LINKS CHECKER</u></b>\n"
        if (
            links[
                "dns_valid"
            ]
            is True
        ):
            text += f"<b>IP Address:</b> {links['ip_address']}\n"
        else:
            pass
        text += f"<b>Domain Name:</b> {links['domain']}\n"
        text += f"<b>Domain Age:</b> {links['domain_age']['human']}\n"
        text += f"<b>Risk Score:</b> {links['risk_score']}%\n"
        text += f"<b>Server:</b> {links['server']}\n\n"
        text += f"<b><u>MORE INFORMATION</b></u>\n"
        text += f" ├ <b>Is Adult:</b> {humanboolean(links['adult'])}\n"
        text += f" ├ <b>Is DNS Valid:</b> {humanboolean(links['dns_valid'])}\n"
        text += f" ├ <b>Is Parking:</b> {humanboolean(links['parking'])}\n"
        text += f" ├ <b>Is Phishing:</b> {humanboolean(links['phishing'])}\n"
        text += f" ├ <b>Is Spamming:</b> {humanboolean(links['spamming'])}\n"
        text += f" ├ <b>Is Suspicious:</b> {humanboolean(links['suspicious'])}\n"
        text += f" ├ <b>Is Unsafe:</b> {humanboolean(links['unsafe'])}\n"
        text += f" └ <b>Is Virus Malware:</b> {humanboolean(links['malware'])}\n\n"
        text += f"<code>Copyright (C) 2023-present kastaid</code>"
        return text
    else:
        return "Can't fetches"


async def fetch_github(
    str_username: Optional[
        str
    ],
) -> Optional[str]:
    url = f"https://api.github.com/users/{str_username}"
    response = (
        await fetching(
            url,
            re_json=True,
        )
    )
    if not response:
        text = (
            "{}".format(
                "Cannot retrieve Github data for user "
            )
            + f"<u>{str_username}</u>"
            + "{}".format(
                ", please check again."
            )
        )
        return text, None

    url = response[
        "html_url"
    ]
    profile_url = (
        url.replace(
            "https://",
            "",
        )
    )
    name = response[
        "name"
    ]
    username = response[
        "login"
    ]
    id_acc = response[
        "id"
    ]
    node_id = response[
        "node_id"
    ]
    company = (
        response[
            "company"
        ]
        or "N/A"
    )
    bio = (
        response["bio"]
        or "N/A"
    )
    created_at = (
        response[
            "created_at"
        ]
    )
    avatar_url = (
        response[
            "avatar_url"
        ]
    )
    blog = (
        response["blog"]
        or "N/A"
    )
    location = (
        response[
            "location"
        ]
        or "N/A"
    )
    repositories = response[
        "public_repos"
    ]
    followers = response[
        "followers"
    ]
    following = response[
        "following"
    ]

    text = (
        "<u>"
        + "{}".format(
            "GITHUB INFORMATION"
        )
        + "</u>\n\n"
    )
    text += (
        "<u>"
        + "{}".format(
            "USERS"
        )
        + "</u>\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Name"
        )
        + f":</b> {name}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Username"
        )
        + f":</b> {username}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "ID Account"
        )
        + f":</b> {id_acc}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Node ID"
        )
        + f":</b> {node_id}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Profile Link"
        )
        + f":</b> <url>{profile_url}</url>\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Company"
        )
        + f":</b> {company}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Created on"
        )
        + f":</b> {created_at}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Repositories"
        )
        + f":</b> {repositories}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Blog"
        )
        + f":</b> {blog}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Location"
        )
        + f":</b> {location}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Followers"
        )
        + f":</b> {followers}\n"
    )
    text += (
        "├ <b>"
        + "{}".format(
            "Following"
        )
        + f":</b> {following}\n"
    )
    text += (
        "└ <b>"
        + "{}".format(
            "Bio"
        )
        + f":</b> {bio}"
    )

    return (
        text,
        avatar_url,
    )


async def get_timezone(
    in_country: Optional[
        str
    ],
) -> Optional[str]:
    for (
        country_code
    ) in country_names:
        if (
            in_country
            == country_names[
                country_code
            ]
        ):
            return timezone(
                country_timezones[
                    country_code
                ][
                    0
                ]
            )
    try:
        if country_names[
            in_country
        ]:
            return timezone(
                country_timezones[
                    in_country
                ][
                    0
                ]
            )
    except KeyError:
        return


def fahrenheit(
    celci: Optional[int],
) -> Optional[str]:
    """Convert celcius to farenheit"""
    temperature = (
        int(celci)
        * float(1.8)
    ) + 32
    temperat: str = (
        f"{temperature}"
    )
    temp = (
        temperat.split(
            "."
        )
    )
    return temp[0]


def celcius(
    farenh: Optional[
        int
    ],
) -> Optional[str]:
    """Convert farenheit to celcius"""
    temperature = (
        int(farenh) - 32
    ) / float(1.8)
    temperat: str = (
        f"{temperature}"
    )
    temp = (
        temperat.split(
            "."
        )
    )
    return temp[0]


async def get_spamwatch_banned(
    user_id: Optional[
        int
    ],
) -> Optional[bool]:
    if (
        user_id
        in _SPAMWATCH_CACHE
    ):
        return _SPAMWATCH_CACHE.get(
            user_id
        )
    url = f"https://notapi.vercel.app/api/spamwatch?id={user_id}"
    response = (
        await fetching(
            url,
            re_json=True,
        )
    )
    if not response:
        _SPAMWATCH_CACHE[
            user_id
        ] = False
        return False
    _SPAMWATCH_CACHE[
        user_id
    ] = bool(
        response.get(
            "id"
        )
    )
    return bool(
        response.get(
            "id"
        )
    )


async def get_cas_banned(
    user_id: Optional[
        int
    ],
) -> Optional[bool]:
    if (
        user_id
        in _CAS_CACHE
    ):
        return _CAS_CACHE.get(
            user_id
        )
    url = f"https://api.cas.chat/check?user_id={user_id}"
    response = (
        await fetching(
            url,
            re_json=True,
        )
    )
    if not response:
        _CAS_CACHE[
            user_id
        ] = False
        return False
    _CAS_CACHE[
        user_id
    ] = response.get(
        "ok"
    )
    return response.get(
        "ok"
    )
