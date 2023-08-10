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

If you want to know more, please contact click the left end button below.

<code>Copyright (C) 2023-present kastaid</code>
"""

    FSUBSCRIBE = """
Kepada user {}

Anda belum bergabung dengan Channel <u></b>PYTEL-Premium</b></u> 🇮🇩
Untuk berkomunikasi dengan <u><b>PYTEL</b></u>
Anda harus bergabung terlebih dahulu.

Jika sudah bergabung, silahkan tekan
tombol dibawah ini.
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
  • Telegram User ID
  • Telegram Username
<b>Note:</b> <i>These are your public telegram details. We do not know your "real" details.</i>

<b>Why we collect and process the personal information:</b>
  • To stats a total users used this bot.
  • To make a broadcasting target correctly.

Our privacy policy may change from time to time.
"""

    BUY = """
Untuk pembayaran <b>PYTEL-Premium</b> tertera pada tombol dibawah ini, selain dari pada tombol dibawah ini adalah <u><b>Fake</b></u> / <u><b>Scam</b></u>.

<b>Disclaimer & Warranty:</b>
Untuk warranty, hanya berlaku untuk deploy ulang gara-gara Akun Anda Terhapus atau ganti ke akun lain.
<i>Tidak berlaku ketika akun Anda Terhapus, lalu meminta Seller menggantikkan Akunnya.</i>

<b>Note ( Warranty ) :</b>
<i>Warranty berjalan selama masa Expired berlangsung!</i>
"""

    PAYMENT_DANA = """
🛒 <u><b>PAYMENT DANA</b></u>

Kepada user {}
Silahkan lakukan transaksi sesuai list dibawah ini.

 • 1 Month ( 1 Bulan ) : Rp 25.000
 • 2 Month ( 2 Bulan ) : Rp 50.000
 • 3 Month ( 3 Bulan ) : Rp 75.000
 • 4 Month ( 4 Bulan ) : Rp 100.000

<b>DANA</b> • <code>+6285717663312</code>
- <code>3901085717663312</code> ( BCA ) Virtual Acc
- <code>88810085717663312</code> ( BRI ) Virtual Acc

A/N = AXEL ALEXIUS LATUKOLAN
Selain diatas <u><b>Fake</b></u> / <u><b>Scam</b></u>.

<b>Catatan:</b>
Tuliskan @username Telegram Anda
pada Deskripsi Pembayaran. ( WAJIB )

Jika sudah melakukan pembayaran,
silahkan Tekan ✅ Confirm Payment.
"""

    PAYMENT_OVO = """
🛒 <u><b>PAYMENT OVO</b></u>

Kepada user {}
Silahkan lakukan transaksi sesuai list dibawah ini.

 • 1 Month ( 1 Bulan ) : Rp 25.000
 • 2 Month ( 2 Bulan ) : Rp 50.000
 • 3 Month ( 3 Bulan ) : Rp 75.000
 • 4 Month ( 4 Bulan ) : Rp 100.000

<b>OVO</b> • <code>+6285717663312</code>
- <code>39358085717663312</code> ( BCA ) Virtual Acc

A/N = AXEL ALEXIUS LATUKOLAN
Selain diatas <u><b>Fake</b></u> / <u><b>Scam</b></u>.

<b>Catatan:</b>
Tuliskan @username Telegram Anda
pada Deskripsi Pembayaran. ( WAJIB )

Jika sudah melakukan pembayaran,
silahkan Tekan ✅ Confirm Payment.
"""

    TEXT_PAYMENT = """
Kepada {}
Silahkan kirimkan bukti pembayaran Anda.
( Screenshoot )

Jika Anda tidak mengirimkan bukti pembayaran dalam
kurun waktu 5 menit, maka status pembelian Anda dibatalkan secara Otomatis.

<b><u>PAYMENT {}</b></u>
"""

    TEXT_PAYMENT_NOTIFY = """
Kepada {}
Limit waktu pembayaran Anda telah habis.
Silahkan tekan tombol dibawah ini untuk pengiriman ulang.
"""

    NOTIFY_BUYER = """
#BUYER #STATUS #CONFIRM

User ID: <code>{}</code>
Username: @{}
via: <b>{}</b>

(c) @kastaid #pytel
"""

    home_buttons = ikmarkup(
        [
            [
                buttons(
                    "🛒 Buy Now",
                    callback_data="start_buy",
                ),
            ],
            [
                buttons(
                    "🔒 Privacy & Policy",
                    callback_data="start_privacy",
                ),
                buttons(
                    "Gen Session 🚀",
                    callback_data="generate_session",
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

    buy_buttons = ikmarkup(
        [
            [
                buttons(
                    "DANA 🇮🇩",
                    callback_data="payment_dana",
                ),
                buttons(
                    "OVO 🇮🇩",
                    callback_data="payment_ovo",
                ),
            ],
            [
                buttons(
                    "Back",
                    callback_data="start_home",
                ),
            ],
        ]
    )

    payment_dana_buttons = ikmarkup(
        [
            [
                buttons(
                    "✅ Confirm Payment",
                    callback_data="payment_confirm_dana",
                ),
            ],
            [
                buttons(
                    "❌ Cancel",
                    callback_data="payment_cancel",
                ),
            ],
        ]
    )

    payment_ovo_buttons = ikmarkup(
        [
            [
                buttons(
                    "✅ Confirm Payment",
                    callback_data="payment_confirm_ovo",
                ),
            ],
            [
                buttons(
                    "❌ Cancel",
                    callback_data="payment_cancel",
                ),
            ],
        ]
    )

    fsub_buttons = ikmarkup(
        [
            [
                buttons(
                    "Bergabung Sekarang",
                    url="t.me/PYTELPremium",
                ),
            ],
            [
                buttons(
                    "Sudah Bergabung",
                    callback_data="subs_done",
                ),
            ],
        ]
    )
