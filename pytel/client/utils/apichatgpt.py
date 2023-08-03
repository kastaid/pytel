# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from typing import Optional, Any
import openai
from requests import post
from ...config import AI_KEY


class PytelAI:
    """
    ChatGPT ::
    """

    def __init__(
        self,
        api_key: Optional[str],
        api_base: Optional[str],
    ):
        self.api_key = api_key
        self.api_base = api_base

    def text(
        self,
        query: Optional[str],
    ) -> Optional[str]:
        openai.api_key = self.api_key
        openai.api_base = self.api_base
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"{query}",
                },
            ],
        )
        if response["choices"][0][
            "message"
        ]["content"]:
            return response["choices"][
                0
            ]["message"]["content"]
        elif response["detail"]:
            return response["detail"]
        elif (
            "Invalid response"
            in response
        ):
            return response

    def images(
        self, query: Optional[str]
    ):
        openai.api_key = self.api_key
        openai.api_base = self.api_base
        response = openai.Image.create(
            prompt=str(query),
            n=1,
            size="1024x1024",
        )
        if response["data"][0]["url"]:
            return response["data"][0][
                "url"
            ]
        elif response["detail"]:
            return response["detail"]
        elif (
            "Invalid response"
            in response
        ):
            return response

    def tts(self, query: Optional[str]):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        strings = {"text": query}
        response = post(
            "https://chimeragpt.adventblocks.cc/api/v1/audio/tts/generation",
            headers=headers,
            json=strings,
        ).json()
        if response["url"]:
            return response["url"]
        elif response["detail"]:
            return response["detail"]
        elif (
            "Invalid response"
            in response
        ):
            return response

    def transaudio(
        self, audiofile: Any
    ):
        openai.api_key = self.api_key
        openai.api_base = self.api_base
        with open(
            audiofile, "rb"
        ) as au_f:
            trans = openai.Audio.transcribe(
                file=au_f,
                model="whisper-1",
                response_format="text",
                language="id",
            )
            if trans["text"]:
                return trans["text"]
            elif (
                "Invalid response"
                in trans
            ):
                return trans


ChatGPT = PytelAI(
    api_key=AI_KEY,
    api_base="https://chimeragpt.adventblocks.cc/api/v1",
)
