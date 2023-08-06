# pytel < https://t.me/kastaid >
# Cobpyrig7ht (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from ._inline import buttons, ikmarkup


class AstGenerate:
    """
    GENERATE :: Session Button
    """

    HOME = """
Kepada {}

Jika kamu belum memiliki <b>API_ID</b> ataupun <b>API_HASH</b>,
silahkan Tekan Tombol Tutorial untuk membuat.
Apabila kamu sudah punya, silahkan tekan tombol Lanjut
untuk pembuatan String Session ( Pyrogram ).

<b>Note:</b>
Jangan lupa baca dengan seksama pada saat pembuatan
string session.
"""

    GEN_TUTORIAL = """
<u><b>TUTORIAL</b></u>

1. Anda harus kunjungi my.telegram.org
2. Login akun Telegram Anda, gunakan code Negara +62.
3. Masukkan Kode yg dikirimkan oleh pihak Telegram.
4. Pilih ( tekan ) pada bagian API development tools.
5. Jika belum pernah membuat API, silahkan isi formulir.
6. Jika sudah mengisi formulir,
   kalian akan mendapatkan API_ID dan API_HASH.

<b>Note:</b> Jangan lupa salin API_ID dan API_HASH Anda,
karena itu bahan untuk membuat String Pyrogram.
( Simpan di Pesan Tersimpan / Notes ).

Tekan Tombol Lanjutkan untuk membuat String.

<code>Copyright (C) 2023-present kastaid</code>
"""

    gen_buttons = ikmarkup(
        [
            [
                buttons(
                    "Lanjut",
                    callback_data="generate_continue",
                ),
            ],
            [
                buttons(
                    "Tutorial 💬",
                    callback_data="generate_tutorial",
                ),
            ],
            [
                buttons(
                    "Back",
                    callback_data="generate_back",
                ),
            ],
        ]
    )

    gen_tu_buttons = ikmarkup(
        [
            [
                buttons(
                    "Lanjutkan",
                    callback_data="generate_continue",
                ),
            ],
            [
                buttons(
                    "Back",
                    callback_data="generate_back",
                ),
            ],
        ]
    )
