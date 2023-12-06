# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

import io
import json
import sys
import traceback
from . import (
    DEFAULT_SHELL_BLACKLISTED,
    RunningCommand,
    eor,
    plugins_helper,
    px,
    pytel,
    suppress,
    get_text,
    get_blacklisted,
    random_prefixies,)


@pytel.instruction(
    [
        "sysinfo",
        "sys",
    ],
    outgoing=True,
    sensitive=False,
)
async def _sysinfo_script(
    client, message
):
    neo = "neofetch --stdout"
    x = await eor(
        message,
        text="Checking system...",
    )
    try:
        (
            xy,
            yz,
        ) = RunningCommand(
            neo
        )
        result = xy + yz
        await eor(
            x,
            text=f"```System Information\n{result}\n```",
        )
    except (
        BaseException
    ) as excp:
        await eor(
            x,
            text=f"Exception: {excp}",
        )


@pytel.instruction(
    ["dshell", "dbash"],
    supersu=["PYTEL"],
    sensitive=False,
)
@pytel.instruction(
    [
        "shell",
        "bash",
    ],
    outgoing=True,
    sensitive=False,
)
async def _bash_script(
    client, message
):
    cmd = get_text(
        message,
        normal=True,
    )
    if not cmd:
        await eor(
            message,
            text="Gimme the commands!",
        )
        return
    x = await eor(
        message,
        text="Running...",
    )
    SHELL_BLACKLISTED = await get_blacklisted(
        url="https://raw.githubusercontent.com/kastaid/resources/main/shellblacklist.json",
        is_json=True,
        attempts=6,
        fallbacks=DEFAULT_SHELL_BLACKLISTED,
    )
    if any(
        _.startswith(
            tuple(
                SHELL_BLACKLISTED
            )
        )
        for _ in cmd.lower().split()
    ):
        await eor(
            x,
            text="Command not allowed.",
        )
        return
    (
        stdout,
        stderr,
    ) = RunningCommand(
        cmd
    )
    err, out = "", ""
    result = " **⟩ --Unix Shell--**\n"
    result += f"**Command:** \n```bash\n{cmd}\n```\n\n"
    if stderr:
        err = f"**Error:**\n```bash\n{stderr}\n```\n\n"
    if stdout:
        out = f"**Results:**\n```bash\n{stdout}\n```"
    if (
        not stderr
        and not stdout
    ):
        out = "**Results:**\n```bash\nSuccess\n```"
    result += err + out

    await eor(
        x, text=result
    )


@pytel.instruction(
    ["daexec", "dexec"],
    supersu=["PYTEL"],
    sensitive=False,
)
@pytel.instruction(
    [
        "aexec",
        "exec",
    ],
    outgoing=True,
    sensitive=False,
)
async def _exec_script(
    client, message
):
    code = get_text(
        message,
        normal=True,
    )
    if not code:
        await eor(
            message,
            text="Gimme the code to execution!",
        )
        return
    x = await eor(
        message,
        text="Execution...",
    )

    old_stderr = (
        sys.stderr
    )
    old_stdout = (
        sys.stdout
    )
    redirected_output = (
        sys.stdout
    ) = io.StringIO()
    redirected_error = (
        sys.stderr
    ) = io.StringIO()
    (
        stdout,
        stderr,
        exc,
    ) = (
        None,
        None,
        None,
    )

    try:
        value = await python_execution(
            code,
            client,
            message,
        )
    except Exception:
        value = None
        exc = (
            traceback.format_exc()
        )

    stdout = (
        redirected_output.getvalue()
    )
    stderr = (
        redirected_error.getvalue()
    )
    sys.stdout = (
        old_stdout
    )
    sys.stderr = (
        old_stderr
    )
    execute = (
        exc
        or stderr
        or stdout
        or _parse_eval(
            value
        )
        or "Success"
    )
    output = "**⟩ --Python Execution--**\n"
    output += f"**Command:** ```python\n{code}\n```\n\n"
    output += f"**Results:**\n```python\n{execute}\n```"
    await eor(
        x, text=output
    )


async def python_execution(
    code, client, message
):
    sys.tracebacklimit = (
        0
    )
    exec(
        "async def __aexec(client, message): "
        + "".join(
            f"\n {line}"
            for line in code.split(
                "\n"
            )
        )
    )
    return (
        await locals()[
            "__aexec"
        ](
            client,
            message,
        )
    )


def _parse_eval(
    value=None,
):
    if not value:
        return value
    if isinstance(
        value, dict
    ):
        with suppress(
            Exception
        ):
            return json.dumps(
                value,
                indent=1,
                ensure_ascii=False,
            )
    return str(value)


plugins_helper[
    "script"
] = {
    f"{random_prefixies(px)}shell / bash [reply/text: script]": "To Running the Linux Commands.",
    f"{random_prefixies(px)}aexec / exec [reply/text: code]": "To execute dynamically created programs, in the form of strings or code objects.",
    f"{random_prefixies(px)}sysinfo / sys": "To checking ur systems. ( using neofetch )",
}
