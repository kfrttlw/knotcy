import sqlite3
from .banner import start_bunner
# from .banner import clear_all

# class all_task:
#     def __init__(self, db_name: str = 'knotcy_base.sqlite'):
#         self.connnn = sqlite3.connect(db_name)
#         self.cur = connnn.cursor


def all_nothes_in_table(connnn: sqlite3.Connection, name_table: str) -> None:
    cur = connnn.cursor()
    try:
        cur.execute(f'''SELECT *
                        FROM "{name_table}"''')
        alls = cur.fetchall()
        if alls:
            for item in alls:
                print(f'{name_table}:\n{item}.')
        else:
            print(f'{name_table} is empty.')
    except sqlite3.Error as w:
        print(f'Error reading table - {name_table}:\n{w}')


def view_and_redact(connnn: sqlite3.Connection, name_table: str,) -> None:
    # cur = connnn.cursor()
    help_help = ""
    while True:
        start_bunner()
        if help_help:
            print(help_help)
            help_help = ""
        print(f'{'='*15}<You in {name_table}>{'='*15}')
        # здесб сделать чтоб подстравиволось под название крч
        all_nothes_in_table(connnn, name_table)
        action = input('Select action or (--help):\n->')
        if action.lower().strip() in [
            '!q', '!quit', '!ex', '!exit'
        ]:
            break
        if action.lower().strip() in [
            '--help', '-help', '--h', '-h'
        ]:
            help_help = f'''{'='*42}
--all command:
!r, !re, !redact, !redacte -> redact task.
!a, !add, !cr, !create -> create a task.
!d, !del, !delete -> delete a task.
!q, !quit, !ex, !exit -> for back menu.\n{'='*42}'''
            continue
        elif action.lower().strip() in [
            '!a', '!add', '!cr', '!create'
        ]:
            pass

        else:
            print(f'Not found command - {action}')
