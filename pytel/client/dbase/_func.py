# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from typing import (
    Any,
    Callable,
    TypeVar,)

T = TypeVar(
    "T",
    bound=Callable[
        ..., Any
    ],
)


def memorize(
    func: T,
) -> T:
    cache: dict = {}

    def wrapper(
        *args: Any,
    ) -> Any:
        if args in cache:
            return cache[
                args
            ]
        else:
            result = (
                func(
                    *args
                )
            )
            cache[
                args
            ] = result
            return result

    wrapper.cache_reset = (
        lambda: cache.clear()
    )
    return wrapper
