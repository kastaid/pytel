# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

import asyncio
from os import remove, cpu_count
from platform import uname
from re import match
from pyrogram import Client
from pyrogram.enums.chat_member_status import (
    ChatMemberStatus,)
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    UserNotParticipant,)
from pyrogram.types import (
    CallbackQuery,
    Message,)
from pytelibs import (
    __version__ as pyver,)
from ..client.dbase.dbExpired import (
    user_expired,)
from ..client.dbase.dbStartAsst import (
    checks_users,
    added_users,)
from . import (
    Assistant,
    AstGenerate,
    OWNER_ID,
    ParseMode,
    _chpytel,
    pytel_tgb,
    suppress,
    filters,
    send_log,)

APP_VERSION = f"PYTEL-Premium v.{pyver}"
WORKERS = min(
    64, (cpu_count() or 0) + 8
)
SYSTEM_VERSION = f"{uname().system}"
DEVICE_MODEL = f"{uname().machine}"
_MEMBERS = [
    ChatMemberStatus.OWNER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.MEMBER,
]


_STRING_TEXT = """
<b>PYTEL</b> <u>PYROGRAM SESSION</u>

<b>API ID:</b> <code>{}</code>

<b>API HASH:</b> <code>{}</code>

<b>No. HP:</b> <code>{}</code>

<b>Password:</b> <code>{}</code>

<b>STRING:</b>
<code>{}</code>


(c) @kastaid #pytel - @PYTELPremiumBot
"""


@pytel_tgb.on_message(
    filters.command(
        "start",
        prefixes="/",
    )
    & filters.private
    & ~filters.forwarded
)
async def _asst_home(client, message):
    user_id = message.from_user.id
    try:
        mem = await client.get_chat_member(
            _chpytel[0],
            user_id=user_id,
        )
        is_join = mem.status in _MEMBERS
    except UserNotParticipant:
        is_join = False
    except Exception as excp:
        is_join = False
        send_log.exception(excp)

    if is_join:
        await message.reply(
            Assistant.START.format(
                message.from_user.mention,
            ),
            quote=False,
            disable_web_page_preview=True,
            reply_markup=Assistant.home_buttons,
        )
        fullname = (
            message.from_user.first_name
            + message.from_user.last_name
            if message.from_user.last_name
            else message.from_user.first_name
        )
        username = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "None"
        )
        if checks_users(
            message.from_user.id
        ):
            return
        else:
            added_users(
                message.from_user.id
            )
            await client.send_message(
                int(OWNER_ID),
                Assistant.start_text_from_user.format(
                    fullname,
                    message.from_user.id,
                    username,
                ),
            )
    else:
        await message.reply(
            Assistant.FSUBSCRIBE.format(
                message.from_user.mention,
            ),
            quote=False,
            disable_web_page_preview=True,
            reply_markup=Assistant.fsub_buttons,
        )


@pytel_tgb.on_callback_query(
    filters.regex(r"subs_(.*?)")
)
async def _cb_asst_subs(
    client, cq: CallbackQuery
):
    subs_done = match(
        r"subs_done", cq.data
    )
    if subs_done:
        user_id = cq.from_user.id
        try:
            mem = await client.get_chat_member(
                _chpytel[0],
                user_id=user_id,
            )
            is_join = (
                mem.status in _MEMBERS
            )
        except UserNotParticipant:
            is_join = False
        except Exception as excp:
            is_join = False
            send_log.exception(excp)
        if not is_join:
            text = """
Anda masih belum bergabung di Channel PYTEL-Premium 🇮🇩
Harap bergabung terlebih dahulu.
"""
            await cq.answer(
                text,
                show_alert=True,
            )
        else:
            await cq.message.delete()
            if checks_users(
                cq.from_user.id
            ):
                return
            else:
                fullname = (
                    cq.from_user.first_name
                    + cq.from_user.last_name
                    if cq.from_user.last_name
                    else cq.from_user.first_name
                )
                username = (
                    f"@{cq.from_user.username}"
                    if cq.from_user.username
                    else "None"
                )
                added_users(
                    cq.from_user.id
                )
                await client.send_message(
                    int(OWNER_ID),
                    Assistant.start_text_from_user.format(
                        fullname,
                        cq.from_user.id,
                        username,
                    ),
                )

            await cq.message.reply(
                Assistant.START.format(
                    cq.from_user.mention,
                ),
                quote=False,
                disable_web_page_preview=True,
                reply_markup=Assistant.home_buttons,
            )


@pytel_tgb.on_callback_query(
    filters.regex(r"start_(.*?)")
)
async def _cb_asst(
    client, cq: CallbackQuery
):
    start_data = match(
        r"start_cls", cq.data
    )
    start_hm = match(
        r"start_home", cq.data
    )
    start_prvc = match(
        r"start_privacy", cq.data
    )
    start_buy = match(
        r"start_buy", cq.data
    )
    if start_data:
        with suppress(BaseException):
            await cq.message.delete()
    elif start_hm:
        with suppress(BaseException):
            await cq.message.edit(
                Assistant.START.format(
                    cq.from_user.mention,
                ),
                disable_web_page_preview=True,
                reply_markup=Assistant.home_buttons,
            )
    elif start_prvc:
        with suppress(BaseException):
            await cq.message.edit(
                Assistant.PRIVACY,
                disable_web_page_preview=True,
                reply_markup=Assistant.privacy_buttons,
            )
    elif start_buy:
        with suppress(BaseException):
            await cq.message.edit(
                Assistant.BUY,
                disable_web_page_preview=True,
                reply_markup=Assistant.buy_buttons,
            )


@pytel_tgb.on_callback_query(
    filters.regex(r"payment_(.*?)")
)
async def _cb_asst_payment(
    client, cq: CallbackQuery
):
    payment_cancel = (
        payment_dana
    ) = match(
        r"payment_cancel", cq.data
    )
    payment_dana = match(
        r"payment_dana", cq.data
    )
    payment_confirm_dana = match(
        r"payment_confirm_dana", cq.data
    )
    payment_ovo = match(
        r"payment_ovo", cq.data
    )
    payment_confirm_ovo = match(
        r"payment_confirm_ovo", cq.data
    )
    if payment_cancel:
        with suppress(BaseException):
            await cq.message.delete()
            await cq.message.reply(
                Assistant.START.format(
                    cq.from_user.mention,
                ),
                quote=False,
                disable_web_page_preview=True,
                reply_markup=Assistant.home_buttons,
            )
            return
    elif payment_dana:
        with suppress(BaseException):
            await cq.message.delete()
            await client.send_photo(
                int(cq.from_user.id),
                photo="resources/payments/DANA.jpg",
                caption=Assistant.PAYMENT_DANA.format(
                    cq.from_user.mention,
                ),
                reply_markup=Assistant.payment_dana_buttons,
                protect_content=False,
            )
    elif payment_ovo:
        with suppress(BaseException):
            await cq.message.delete()
            await cq.message.reply(
                Assistant.PAYMENT_OVO.format(
                    cq.from_user.mention,
                ),
                disable_web_page_preview=True,
                reply_markup=Assistant.payment_ovo_buttons,
            )
    elif payment_confirm_dana:
        with suppress(BaseException):
            if (
                not cq.from_user.username
            ):
                text = "Mohon pasang Username Anda untuk mengkonfirmasi pembayaran."
                await client.answer_callback_query(
                    cq.id,
                    text,
                    show_alert=True,
                    cache_time=300,
                )
                return
            else:
                if cq.from_user.id:
                    await cq.message.delete()
                    await payment_listener(
                        client,
                        cq.message,
                        cq,
                        via="DANA",
                    )

    elif payment_confirm_ovo:
        with suppress(BaseException):
            if (
                not cq.from_user.username
            ):
                text = "Mohon pasang Username Anda untuk mengkonfirmasi pembayaran."
                await client.answer_callback_query(
                    cq.id,
                    text,
                    show_alert=True,
                )
                return
            else:
                if cq.from_user.id:
                    await cq.message.delete()
                    await payment_listener(
                        client,
                        cq.message,
                        cq,
                        via="OVO",
                    )


async def payment_listener(
    client, m: Message, cq, via: str
):
    if via == "DANA":
        r = await cq.message.reply(
            Assistant.TEXT_PAYMENT.format(
                cq.from_user.mention,
                via,
            ),
        )
        try:
            msg = await client.listen(
                cq.from_user.id,
                filters.user(
                    cq.from_user.id
                )
                & filters.private,
                timeout=600,
            )
        except asyncio.TimeoutError:
            await cq.message.reply(
                Assistant.TEXT_PAYMENT_NOTIFY.format(
                    cq.from_user.mention,
                    via,
                ),
                reply_markup=Assistant.payment_dana_buttons,
            )
        if msg.photo:
            f_dana = await client.download_media(
                msg.photo
            )
            bkt_dana = (
                await client.send_photo(
                    int(OWNER_ID),
                    photo=f_dana,
                )
            )
            remove(f_dana)
            text = """
Mohon Tunggu, Seller akan memeriksa pembayaran Anda.
Jika Pembayaran Anda Terbukti, Anda akan mendapatkan Notifikasi
dari sini.
"""
            await cq.answer(
                text,
                show_alert=True,
                cache_time=300,
            )
            await client.send_message(
                int(OWNER_ID),
                Assistant.NOTIFY_BUYER.format(
                    cq.from_user.id,
                    cq.from_user.username,
                    via,
                ),
                reply_to_message_id=bkt_dana.id,
            )
            await r.delete()
            return

        else:
            text = f"""
<u><b>PAYMENT {via}</b></u>

Silahkan kirim ulang pembayaran Anda.
Tekan Confirm, lalu kirim bukti pembayaran Anda.
"""
            await asyncio.gather(
                cq.answer(
                    "Mohon maaf, kirimkan pembayaran berupa Photo.",
                    show_alert=True,
                    cache_time=300,
                ),
                cq.message.reply(
                    text,
                    reply_markup=Assistant.payment_dana_buttons,
                ),
            )
            await r.delete()
            return

    elif via == "OVO":
        r = await cq.message.reply(
            Assistant.TEXT_PAYMENT.format(
                cq.from_user.mention,
                via,
            ),
        )
        try:
            msg = await client.listen(
                cq.from_user.id,
                filters.user(
                    cq.from_user.id
                )
                & filters.private,
                timeout=300,
            )
        except asyncio.TimeoutError:
            await cq.message.reply(
                Assistant.TEXT_PAYMENT_NOTIFY.format(
                    cq.from_user.mention,
                    via,
                ),
                reply_markup=Assistant.payment_ovo_buttons,
            )
        if msg.photo:
            f_ovo = await client.download_media(
                msg.photo
            )
            bkt_ovo = (
                await client.send_photo(
                    int(OWNER_ID),
                    photo=f_ovo,
                )
            )
            remove(f_ovo)
            text = """
Mohon Tunggu, Seller akan memeriksa pembayaran Anda.
Jika Pembayaran Anda Terbukti, Anda akan mendapatkan Notifikasi
dari sini.
"""
            await cq.answer(
                text,
                show_alert=True,
                cache_time=300,
            )
            await client.send_message(
                int(OWNER_ID),
                Assistant.NOTIFY_BUYER.format(
                    cq.from_user.id,
                    cq.from_user.username,
                    via,
                ),
                reply_to_message_id=bkt_ovo.id,
            )
            await r.delete()
            return
        else:
            text = f"""
<u><b>PAYMENT {via}</b></u>

Silahkan kirim bukti pembayaran Anda.
Tekan Confirm, lalu kirim bukti pembayaran Anda.
"""
            await asyncio.gather(
                cq.answer(
                    "Mohon maaf, kirimkan pembayaran berupa Photo.",
                    show_alert=True,
                    cache_time=300,
                ),
                cq.message.reply(
                    text,
                    reply_markup=Assistant.payment_ovo_buttons,
                ),
            )
            await r.delete()
            return


@pytel_tgb.on_callback_query(
    filters.regex(r"generate_(.*?)")
)
async def _cb_asst_generate(
    client, cq: CallbackQuery
):
    gen_back = match(
        r"generate_back", cq.data
    )
    generate_session = match(
        r"generate_session", cq.data
    )
    generate_tutorial = match(
        r"generate_tutorial", cq.data
    )
    generate_continue = match(
        r"generate_continue", cq.data
    )
    if gen_back:
        with suppress(Exception):
            await cq.message.delete()
            await cq.message.reply(
                Assistant.START.format(
                    cq.from_user.mention,
                ),
                quote=False,
                disable_web_page_preview=True,
                reply_markup=Assistant.home_buttons,
            )
            return
    elif generate_session:
        with suppress(Exception):
            user_id = cq.from_user.id
            if not user_expired().get(
                int(user_id)
            ):
                text = """
Mohon maaf, Anda bukan bagian dari PYTEL-Premium.
Silahkan lakukan Transaksi jika ingin membuat String Session.
"""
                await cq.answer(
                    text,
                    show_alert=True,
                    cache_time=300,
                )
                return
            else:
                await cq.message.delete()
                await cq.message.reply(
                    AstGenerate.HOME.format(
                        cq.from_user.mention,
                    ),
                    disable_web_page_preview=True,
                    reply_markup=AstGenerate.gen_buttons,
                )
                return

    elif generate_tutorial:
        with suppress(Exception):
            await cq.message.delete()
            await cq.message.reply(
                AstGenerate.GEN_TUTORIAL,
                disable_web_page_preview=True,
                reply_markup=AstGenerate.gen_tu_buttons,
            )

    elif generate_continue:
        with suppress(Exception):
            await cq.message.delete()
        try:
            await _generate_pytel_session(
                client, cq.message
            )
        except Exception as excp:
            send_log.exception(excp)


async def _generate_pytel_session(
    bot, msg: Message
):
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id,
        "Kirimkan <u><b>API_ID</b></u> Anda.\n\nTekan /cancel untuk membatalkan proses.",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "<u><b>API_ID</b></u> tidak valid (harus angka semua).\nSilahkan ulang kembali!",
            quote=True,
            reply_markup=AstGenerate.try_buttons,
        )
        return
    api_hash_msg = await bot.ask(
        user_id,
        "Kirimkan <u><b>API_HASH</b></u> Anda.\n\nTekan /cancel untuk membatalkan proses.",
        filters=filters.text,
    )
    if await cancelled(api_hash_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "Kirimkan <u><b>No. Handphone</b></u> (Telegram) Anda.\n<b>Jangan Lupa Pakai Code Negara.\n<b>Contoh:</b> <code>+62</code>\n\nTekan /cancel untuk membatalkan proses.",
        filters=filters.text,
    )
    if await cancelled(
        phone_number_msg
    ):
        return
    phone_number = phone_number_msg.text
    if not phone_number.startswith("+"):
        await api_id_msg.reply(
            "<u><b>No. Handphone</b></u> tidak valid (harus menggunakan code negara).\nSilahkan ulang kembali!",
            quote=True,
            reply_markup=AstGenerate.try_buttons,
        )
        return
    m_otp = await msg.reply(
        "Sedang mengirimkan OTP..."
    )
    client = Client(
        name=f"pytel_{user_id}",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
        lang_code="en",
        ipv6=False,
        app_version=APP_VERSION,
        system_version=SYSTEM_VERSION,
        device_model=DEVICE_MODEL,
        workers=WORKERS,
    )
    await client.connect()
    try:
        code = await client.send_code(
            phone_number
        )
    except ApiIdInvalid:
        await msg.reply(
            "<u><b>API_ID</b></u> dan <u><b>API_HASH</b></u> kombinasi tidak valid.\nSilahkan ulang kembali!",
            reply_markup=AstGenerate.try_buttons,
        )
        return
    except PhoneNumberInvalid:
        await msg.reply(
            "<u><b>No. Handphone</b></u> tidak valid.\nSilahkan ulang kembali!",
            reply_markup=AstGenerate.try_buttons,
        )
        return
    try:
        await m_otp.delete()
        text = """
Silahkan check kode OTP dari official Telegram.
Jika ada, kirim OTP kesini. Kirim kode OTP dengan format dibawah ini.

<b>Catatan:</b>
Misalkan kode nya <code>12345</code>
kamu harus kirim dengan spasi <code>1 2 3 4 5</code>
"""
        phone_code_msg = await bot.ask(
            user_id,
            text,
            filters=filters.text,
            timeout=300,
        )
        if await cancelled(
            phone_code_msg
        ):
            return
    except asyncio.TimeoutError:
        await msg.reply(
            "Limit waktu telah habis dalam 5 menit.\nSilahkan ulang kembali!",
            reply_markup=AstGenerate.try_buttons,
        )
        return
    phone_code = (
        phone_code_msg.text.replace(
            " ", ""
        )
    )
    is_pw = False
    try:
        await client.sign_in(
            phone_number,
            code.phone_code_hash,
            phone_code,
        )
    except PhoneCodeInvalid:
        await msg.reply(
            "Kode OTP tidak valid.\nSilahkan ulang kembali!",
            reply_markup=AstGenerate.try_buttons,
        )
        return
    except PhoneCodeExpired:
        await msg.reply(
            "Kode OTP telah kadaluarsa.\nSilahkan ulang kembali!",
            reply_markup=AstGenerate.try_buttons,
        )
        return
    except SessionPasswordNeeded:
        is_pw = True
        try:
            two_step_msg = await bot.ask(
                user_id,
                "Akun Anda mengaktifkan verifikasi 2 Langkah.\nSilahkan kirimkan kata sandi akun Anda.",
                filters=filters.text,
                timeout=300,
            )
        except asyncio.TimeoutError:
            await msg.reply(
                "Limit waktu telah habis dalam 5 menit.\nSilahkan ulang kembali!",
                reply_markup=AstGenerate.try_buttons,
            )
            return
        try:
            password = two_step_msg.text
            await client.check_password(
                password=password
            )
            if await cancelled(
                api_id_msg
            ):
                return
        except PasswordHashInvalid:
            await two_step_msg.reply(
                "Kata sandi Akun Anda salah.\nSilahkan ulang kembali!",
                reply_markup=AstGenerate.try_buttons,
            )
            return

        if password:
            pw = password

    string_session = (
        await client.export_session_string()
    )
    if is_pw:
        psw = pw
    else:
        psw = "Tidak ada."

    with suppress(KeyError):
        await client.send_message(
            "me",
            text=_STRING_TEXT.format(
                api_id,
                api_hash,
                phone_number,
                psw,
                string_session,
            ),
            parse_mode=ParseMode.HTML,
        )

    await client.disconnect()
    await bot.send_message(
        msg.chat.id,
        "✅ Selesai, Pembuatan String telah berhasil.\nSilahkan check Pesan Tersimpan.",
    )


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "Pembuatan String Telah Dibatalkan!\n\nTekan /start untuk memulai."
        )
        return True
