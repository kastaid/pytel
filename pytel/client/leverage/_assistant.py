# pytel < https://t.me/kastaid >
# Cobpyrig7ht (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from ._inline import buttons, ikmarkup


class Assistant:
    """
    ASSISTANT :: Buttons
    """

    START = """
✨ <b>Welcome</b> {} !

<b><u>PYTEL-Premium 🇮🇩</b></u> based on @Pyrogram
We provide services with various features
from Telegram Base.

If you want to know more, please contact the contact below.

<code>Copyright (C) 2023-present kastaid</code>
"""

    start_text_from_user = """
#NEW_START #FROM_USER

<b>Name:</b> {}
<b>User ID:</b> <code>{}</code>
<b>Username:</b> {}

(c) @kastaid #pytel
"""

    PRIVACY = """
<b>PYTEL</b> has been made to protect and preserve privacy as best as possible.


<b>We currently collect and process a personal information following:</b>
  • <u>Telegram User ID</u>
  • <u>Telegram Username</u> ( <i>if u've</i> )
  <b>Note:</b> <i>These are your public telegram details. We do not know your "real" details.</i>


<b>Why we collect and process the personal information:</b>
  • <u>To stats a total users used this bot.</u>
  • <u>To make a broadcasting target correctly.</u>


Our privacy policy may change from time to time.
"""

    home_buttons = ikmarkup(
        [
            [
                buttons(
                    "🔒 Privacy & Policy",
                    callback_data="start_privacy",
                ),
                buttons(
                    "Gen Session 🚀",
                    url="t.me/strgen_bot?start=",
                ),
            ],
            [
                buttons(
                    "🌐 Channel 🌐",
                    url="t.me/PYTELPremium/47",
                ),
            ],
        ]
    )

    privacy_buttons = ikmarkup(
        [
            [
                buttons(
                    "Back",
                    callback_data="start_home",
                ),
                buttons(
                    "Close",
                    callback_data="start_cls",
                ),
            ],
        ]
    )
