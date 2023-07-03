# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from typing import Optional
from bs4 import BeautifulSoup
from requests import get
from .misc import gsc, gse


class LSE(Exception):
    """Exception"""


class _Lyrics:
    """
    Port from : universe
    """

    BREAKS = "\n\n"
    source_code = None
    title = None

    def __call__(self, source_code, title):
        self.source_code = source_code
        self.title = title

    def __up_title__(self, title):
        self.title = title

    def __GeniusEngine1__(self):
        extract = self.source_code.select(
            ".lyrics"
        )
        if not extract:
            return None

        lyrics = (
            (extract[0].get_text())
            .replace("<br>", "\n")
            .strip()
        )
        return lyrics

    def __GeniusEngine2__(self):
        all_extracts = self.source_code.select(
            'div[class*="Lyrics__Container-sc-"]'
        )
        if not all_extracts:
            return None

        lyrics = ""
        for extract in all_extracts:
            for br in extract.find_all(
                "br"
            ):
                br.replace_with("\n")
            lyrics += extract.get_text()

        return lyrics.strip()

    def genius_engine(self):
        lyrics = (
            self.__GeniusEngine1__()
            or self.__GeniusEngine2__()
        )
        self.__up_title__(self.title[:-16])

        return lyrics

    def glamsham_engine(self):
        extract = self.source_code.find_all(
            "font", class_="general"
        )[5]
        if not extract:
            return None

        for br in extract.find_all("br"):
            br.replace_with("\n")
        lyrics = extract.get_text()
        self._update_title(
            self.title[:-14].strip()
        )

        return lyrics

    def lyricsbell_engine(self):
        extract = self.source_code.select(
            ".lyrics-col p"
        )
        if not extract:
            return None

        lyrics = ""
        for i in range(len(extract)):
            lyrics += (
                extract[i].get_text()
                + self.BREAKS
            )

        lyrics = lyrics.replace(
            "<br>", "\n"
        ).strip()
        self._update_title(self.title[:-13])
        return lyrics

    def lyricsted_engine(self):
        extract = self.source_code.select(
            ".lyric-content p"
        )
        if not extract:
            return None

        lyrics = ""
        for i in range(len(extract)):
            lyrics += (
                extract[i]
                .get_text()
                .strip()
                + self.BREAKS
            )

        lyrics = lyrics.replace(
            "<br>", "\n"
        ).strip()
        return lyrics

    def lyricsoff_engine(self):
        extract = self.source_code.select(
            "#main_lyrics p"
        )
        if not extract:
            return None

        lyrics = ""
        for i in range(len(extract)):
            lyrics += (
                extract[i]
                .get_text(separator="\n")
                .strip()
                + self.BREAKS
            )

        return lyrics.strip()

    def lyricsmint_engine(self):
        extract = self.source_code.find(
            "section", {"id": "lyrics"}
        ).find_all("p")
        if not extract:
            return None

        lyrics = ""
        for i in range(len(extract)):
            lyrics += (
                extract[i]
                .get_text()
                .strip()
                + self.BREAKS
            )

        return lyrics.strip()


class LyricsEngine:
    """
    Port from : universe
    """

    engine_universe = _Lyrics()
    ENGINE = {
        "genius": engine_universe.genius_engine,
        "glamsham": engine_universe.glamsham_engine,
        "lyricsbell": engine_universe.lyricsbell_engine,
        "lyricsted": engine_universe.lyricsted_engine,
        "lyricsoff": engine_universe.lyricsoff_engine,
        "lyricsmint": engine_universe.lyricsmint_engine,
    }

    def __init__(
        self,
        gcs_api_key: Optional[str] = gsc,
        gcs_engine_id: Optional[str] = gse,
    ):
        self.gsc_api = gcs_api_key
        self.gse_id = gcs_engine_id

    def __handle_requests__(
        self, song_name
    ):
        url = "https://www.googleapis.com/customsearch/v1/siterestrict"
        params = {
            "key": self.gsc_api,
            "cx": self.gse_id,
            "q": f"{song_name} lyrics",
        }

        response = get(url, params=params)
        data = response.json()
        if response.status_code != 200:
            raise LSE(data)
        return data

    def __extract_lyrics__(
        self, result_url, title
    ):
        page = get(result_url)
        source_code = BeautifulSoup(
            page.content, "lxml"
        )
        self.engine_universe(
            source_code, title
        )
        for (
            domain,
            engine,
        ) in self.ENGINE.items():
            if domain in result_url:
                lyrics = engine()

        return lyrics

    def getting_my_lyrics(
        self, song_name: str
    ) -> dict:
        data = self.__handle_requests__(
            song_name
        )
        spell = data.get(
            "spelling", {}
        ).get("correctedQuery")
        data = (
            self.__handle_requests__(spell)
            if spell
            else data
        )
        query_results = data.get(
            "items", []
        )

        for i in range(len(query_results)):
            result_url = query_results[i][
                "link"
            ]
            title = query_results[i][
                "title"
            ]
            try:
                lyrics = (
                    self.__extract_lyrics__(
                        result_url, title
                    )
                )
            except Exception as excp:
                raise LSE(excp)

            if lyrics:
                return {
                    "title": self.engine_universe.title,
                    "lyrics": lyrics,
                }

            else:
                return {
                    "error": "No results found"
                }
