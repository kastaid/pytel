# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from sys import exit
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from ...config import DB_URI
from ...logger import pylog as send_log

DB: str = DB_URI.replace("postgres:", "postgresql:") if "postgres://" in DB_URI else DB_URI


def start() -> scoped_session:
    machine = create_engine(DB)
    BASE.metadata.bind = machine
    BASE.metadata.create_all(machine)
    return scoped_session(
        sessionmaker(
            bind=machine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        ),
    )


try:
    BASE = declarative_base()
    SESSION = start()
except Exception as excp:
    send_log.exception(excp)
    exit(1)
