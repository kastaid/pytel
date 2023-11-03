# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

import ast
from contextlib import suppress
from sys import exit
from typing import Optional
import attrs
import psycopg2
from localdb import Database
from ...config import DATABASE_URL
from ...logger import pylog


@attrs.define
class BaseDB:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        self._cache: Optional[dict] = {}

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
        try:
            self.db = Database("pytel")
            self.get = self.db.get
            self.set = self.db.set
            self.delete = self.db.delete
        except Exception as excp:
            pylog.exception(excp)
            exit(0)
        super().__init__()

    @property
    def name(self):
        nm: str = "Local"
        return nm

    @property
    def sizes(self):
        return self.db.size

    def keys(self):
        return self._cache.keys()

    def __repr__(
        self,
    ):
        return f"<Pytel.Local\n -total_keys: {len(self.keys())}\n>"


class SqlDB(BaseDB):
    def __init__(self, url):
        self._url = url
        self._connection = None
        self._cursor = None
        try:
            self._connection = (
                psycopg2.connect(
                    dsn=url
                )
            )
            self._connection.autocommit = (
                True
            )
            self._cursor = (
                self._connection.cursor()
            )
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS PYTEL (pytelClient varchar(70))"
            )
        except Exception as error:
            pylog.exception(error)
            pylog.info(
                "Invaid SQL Database"
            )
            if self._connection:
                self._connection.close()
            exit()
        super().__init__()

    @property
    def name(self):
        return "SQL"

    @property
    def sizes(self):
        self._cursor.execute(
            "SELECT pg_size_pretty(pg_relation_size('PYTEL')) AS size"
        )
        data = self._cursor.fetchall()
        return int(
            data[0][0].split()[0]
        )

    def keys(self):
        self._cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name  = 'pytel'"
        )  # case sensitive
        data = self._cursor.fetchall()
        return [_[0] for _ in data]

    def get(self, variable):
        try:
            self._cursor.execute(
                f"SELECT {variable} FROM PYTEL"
            )
        except (
            psycopg2.errors.UndefinedColumn
        ):
            return None
        data = self._cursor.fetchall()
        if not data:
            return None
        if len(data) >= 1:
            for i in data:
                if i[0]:
                    return i[0]

    def set(self, key, value):
        try:
            self._cursor.execute(
                f"ALTER TABLE PYTEL DROP COLUMN IF EXISTS {key}"
            )
        except (
            psycopg2.errors.UndefinedColumn,
            psycopg2.errors.SyntaxError,
        ):
            pass
        except BaseException as er:
            pylog.exception(er)
        self._cache.update({key: value})
        self._cursor.execute(
            f"ALTER TABLE PYTEL ADD {key} TEXT"
        )
        self._cursor.execute(
            f"INSERT INTO PYTEL ({key}) values (%s)",
            (str(value),),
        )
        return True

    def delete(self, key):
        try:
            self._cursor.execute(
                f"ALTER TABLE PYTEL DROP COLUMN {key}"
            )
        except (
            psycopg2.errors.UndefinedColumn
        ):
            return False
        return True

    def flushall(self):
        self._cache.clear()
        self._cursor.execute(
            "DROP TABLE PYTEL"
        )
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS PYTEL (pytelClient varchar(70))"
        )
        return True


pydb = (
    SqlDB(DATABASE_URL)
    if DATABASE_URL
    else Local()
)
