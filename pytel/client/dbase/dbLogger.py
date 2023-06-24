# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from threading import RLock
from typing import Optional
from cachetools import LRUCache
from sqlalchemy import String, Column, UnicodeText
from .core import (
    SESSION,
    BASE,
    DB,
    create_engine,
)

_SetLOGGER_LOCK = RLock()
_SetLOGGER_CACHE = LRUCache(maxsize=1024)

machine = create_engine(DB)


class SetLOGGER(BASE):
    __tablename__ = "LOGGER_ID"
    user_id = Column(String, primary_key=True, nullable=False)
    logger_id = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, user_id: Optional[str], logger_id):
        self.user_id = str(user_id)
        self.logger_id = logger_id


SetLOGGER.__table__.create(bind=machine, checkfirst=True)


def check_logger(user_id, use_cache: Optional[bool] = False):
    with _SetLOGGER_LOCK:
        user_id, logger_id = str(user_id), None
        if use_cache and user_id in _SetLOGGER_CACHE:
            return _SetLOGGER_CACHE.get(user_id)
        try:
            data = SESSION.query(SetLOGGER).filter(SetLOGGER.user_id == user_id).one_or_none()
            if data:
                SESSION.refresh(data)
                logger_id = data.logger_id
                if use_cache and not _SetLOGGER_CACHE.get(user_id):
                    _SetLOGGER_CACHE[user_id] = logger_id
            return logger_id
        except BaseException:
            return logger_id
        finally:
            SESSION.close()


def add_logger(user_id, logger_id):
    with _SetLOGGER_LOCK:
        if SESSION.query(SetLOGGER).filter(SetLOGGER.user_id == str(user_id)).one_or_none():
            del_logger(user_id)
        adder = SetLOGGER(str(user_id), logger_id)
        SESSION.add(adder)
        SESSION.commit()


def del_logger(user_id):
    with _SetLOGGER_LOCK:
        removes = SESSION.query(SetLOGGER).filter(SetLOGGER.user_id == str(user_id)).delete(synchronize_session="fetch")
        if removes:
            SESSION.commit()
