# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from pyrogram.raw import types
from . import (
    OWNER_ID,
    replied,
    functions,
    eor,
    user_and_reason,
    mentioned,
    plugins_helper,
    px,
    pytel,
    _supersu,
    random_prefixies,)


def get_report_reason(text: str):
    if text == "abuse":
        return (
            types.InputReportReasonChildAbuse()
        )
    elif text == "fake" or "faker":
        return (
            types.InputReportReasonFake()
        )
    elif text == "copyright":
        return (
            types.InputReportReasonCopyright()
        )
    elif text == "geogroup" or "geo":
        return (
            types.InputReportReasonGeoIrrelevant()
        )
    elif (
        text == "other"
        or "lainnya"
        or "dll"
    ):
        return (
            types.InputReportReasonOther()
        )
    elif (
        text == "porn"
        or "porno"
        or "pornography"
        or "pornograpi"
    ):
        return (
            types.InputReportReasonPornography()
        )
    elif (
        text == "violence"
        or "scam"
        or "scammer"
        or "phising"
    ):
        return (
            types.InputReportReasonViolence()
        )
    elif (
        text == "spam"
        or "spamming"
        or "spamm"
    ):
        return (
            types.InputReportReasonSpam()
        )


@pytel.instruction(
    ["dreport"],
    supersu=["PYTEL"],
)
@pytel.instruction(
    ["report", "reported"],
    outgoing=True,
)
async def _reported(client, message):
    (
        user,
        reason,
    ) = await user_and_reason(
        client,
        message,
        sender_chat=True,
    )
    if not user:
        await eor(
            message,
            text="I can't find that user.",
        )
        return
    if (user in list(_supersu)) or (
        user == int(OWNER_ID)
    ):
        await eor(
            message,
            text="That's My Developer.",
        )
        return

    x = await eor(
        message,
        text="</b>Reporting . . .</b>",
    )
    user_info = (
        await client.resolve_peer(user)
    )
    rsn = (
        reason.lower()
        if reason
        else "spam"
    )
    try:
        msg_rep = get_report_reason(
            text=rsn
        )
        if (
            msg_rep
            and message.reply_to_message
        ):
            await client.invoke(
                functions.messages.Report(
                    id=replied(message),
                    peer=user_info,
                    reason=msg_rep,
                    message=rsn,
                ),
            )
        elif (
            msg_rep
            and not message.reply_to_message
        ):
            await client.invoke(
                functions.account.ReportPeer(
                    peer=user_info,
                    reason=msg_rep,
                    message=rsn,
                ),
            )

        else:
            await client.invoke(
                functions.messages.ReportSpam(
                    peer=user_info,
                ),
            )

        text = """
<u><b>Reporting</u></b>
├ <b>Target:</b> {}
└ <b>Reason:</b> {}
"""
        await eor(
            x,
            text=text.format(
                await mentioned(
                    client,
                    user,
                    use_html=True,
                ),
                rsn,
            ),
        )
        return

    except Exception as excp:
        await eor(
            x, text=f"Exception {excp}"
        )
        return


plugins_helper["reports"] = {
    f"{random_prefixies(px)}report [id/username/reply to user] [reason: abuse/copyright/fake/spam/porn/geogroup/violence/other]": "To reports user/group/channel & give the reason.",
}
