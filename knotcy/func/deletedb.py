"""Func for delete db."""

import os
import sqlite3


def delete_db(
        connection: sqlite3.Connection,
        db_path: str
        ) -> tuple[bool, str]:
    try:
        connection.close()

        if os.path.exists(db_path):
            os.remove(db_path)
            messages = 'knotcy.db successfully deleted'
            return True, messages
        else:
            messages = 'Error: Knotcy.db not found'
            return False, messages
    except Exception as a:
        messages = f'Error: {a}'
        return False, messages
