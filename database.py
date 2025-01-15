"""
Author: Ido Karadi
Project name: DB API
Description: Part of the DB API program.
This file includes the Database class.
Date: 15/1/25
"""


class Database:
    def __init__(self):
        self._data = {}

    def set_value(self, key, val):
        self._data[key] = val

    def get_value(self, key):
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found in database.")
        return self._data[key]

    def delete_value(self, key):
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found in database.")
        del self._data[key]

    def __repr__(self):
        return f"Database({self._data})"
