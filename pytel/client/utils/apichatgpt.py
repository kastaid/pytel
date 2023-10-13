# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from typing import Optional
import g4f


class PytelAI:
    """
    ChatGPT :: Open AI
    """

    async def text(
        self,
        query: Optional[str],
    ) -> Optional[str]:
        try:
            response = await g4f.ChatCompletion.create_async(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"{query}",
                    },
                ],
                stream=False,
            )
            if response:
                return response
        except BaseException as excp:
            return str(excp)


ChatGPT = PytelAI()
