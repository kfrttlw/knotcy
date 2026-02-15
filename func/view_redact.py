import sqlite3
# import os


def all_nothes_in_table(connnn: sqlite3.Connection, name_table: str,) -> None:
    cur = connnn.cursor()
    try:
        cur.execute(f'''SELECT *
                        FROM "{name_table}"''')
        alls = cur.fetchall()
        if alls:
            for all in alls:
                print(f'{name_table}:\n{all}.')
        else:
            print(f'{name_table} is empty.')
    except sqlite3.Error as w:
        print(f'Error reading table - {name_table}:\n{w}')


def view_and_redact(connnn: sqlite3.Connection, name_table: str,) -> None:
    # cur = connnn.cursor()
    while True:
        help_help = ""
        if help_help:
            print(help_help)
            help_help = ""
        print(f'{'='*42}You in <{name_table}>{'='*42}')
        all_nothes_in_table(connnn, name_table)

        action = input('Select action or (--help):\n->')
        if action.lower().strip() in [
            '!q', '!quit', '!ex', '!exit'
        ]:
            break
        elif action.lower().strip() in [
            '--help', '-help', '--h', '-h'
        ]:
            help_help = f'''{'='*42}
--all command:
!r, !re, !ren, !rename -> redact name a folder.
!d, !del, !delete -> delete a folder.
!q, !quit, !ex, !exit -> for back menu.\n{'='*42}'''
            continue
        else:
            print(f'Not found command - {action}')
