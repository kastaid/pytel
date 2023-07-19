# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

import ast
from contextlib import suppress
from localdb import Database


class BaseDB:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        self._cache = {}

    def get_key(self, key):
        if key in self._cache:
            return self._cache[key]
        value = self._get_data(key)
        self._cache.update({key: value})
        return value

    def re_cache(
        self,
    ):
        self._cache.clear()
        for key in self.keys():
            self._cache.update(
                {key: self.get_key(key)}
            )

    def ping(self):
        return 1

    @property
    def usage(self):
        return 0

    def keys(self):
        return []

    def del_key(self, key):
        if key in self._cache:
            del self._cache[key]
        self.delete(key)
        return

    def _get_data(
        self,
        key=None,
        data=None,
    ):
        if key:
            data = self.get(str(key))
        if data and isinstance(
            data,
            str,
        ):
            with suppress(
                BaseException
            ):
                data = ast.literal_eval(
                    data
                )
        return data

    def set_key(
        self,
        key,
        value,
        cache_only=False,
    ):
        value = self._get_data(
            data=value
        )
        self._cache[key] = value
        if cache_only:
            return
        return self.set(
            str(key),
            str(value),
        )

    def rename(
        self,
        key1,
        key2,
    ):
        _ = self.get_key(key1)
        if _:
            self.del_key(key1)
            self.set_key(
                key2,
                _,
            )
            return 0
        return 1


class Local(BaseDB):
    def __init__(
        self,
    ):
        self.db = Database("pytel")
        self.get = self.db.get
        self.set = self.db.set
        self.delete = self.db.delete
        super().__init__()

    @property
    def name(self):
        return "Local"

    def keys(self):
        return self._cache.keys()

    def __repr__(
        self,
    ):
        return f"<Pytel.Local\n -total_keys: {len(self.keys())}\n>"


pydb = Local()
