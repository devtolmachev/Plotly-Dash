import sqlite3
from typing import Any


class Database:

    def __init__(self, database: str = 'testDB.db'):
        self.__base_name = database
        self._base = sqlite3.connect(database=database)

    def apply_query(self, query: str):
        self._base.cursor().execute(query)
        self._base.commit()

    def get_one(self, query: str) -> Any:
        return self._base.cursor().execute(query).fetchone()

    def get_more(self, query: str):
        return self._base.cursor().execute(query).fetchmany()

    def get_all(self, query: str):
        return self._base.cursor().execute(query).fetchall()

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()

    def _connect(self):
        self._base = sqlite3.connect(self.__base_name)

    def _disconnect(self):
        self._base.close()

    @property
    def connection(self):
        return self._base
