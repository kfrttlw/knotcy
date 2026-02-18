# import os
import sqlite3
import time
# import random
# import string
from func import start_bunner
from func import clear_all
from datetime import datetime
from func import task_red
from func import folder_red
# (connnn: sqlite3.Connection, name_table: str,) -> None:
# from func.view_redact import all_nothes_in_table
# (connnn: sqlite3.Connection, name_table: str,) -> None:

# ---------forcomfy------------------------------1
slash = '=' * 20 + '<>' + '=' * 20


def proverka_un_name(tab_nam: str) -> bool:
    cur.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table' AND name=?""",
                (tab_nam,))
    return cur.fetchone() is not None
# ---------forcomfy------------------------------2
# ---------------------------------ХЗдесь все с sql 1 пункт------------------1


connnn = sqlite3.connect('knotcy_base.sqlite')
cur = connnn.cursor()

task = task_red(connnn)  # придумать название
folder = folder_red(connnn)


# для создания папки задач
def add_new_table(name: str) -> None:

    clean_name = ''.join(e for e in name if e.isalnum() or e == '_')

    if not clean_name:
        input('Error: name is empty.\nPress any button to back menu...')
        return

    if proverka_un_name(clean_name):
        print(f'Table, {clean_name} - already there.')
        # input('press any button for back menu...')
    else:
        try:
            cur.execute(f'''
        CREATE TABLE IF NOT EXISTS "{clean_name}"(
            id INTEGER PRIMARY KEY,
            NAME TEXT NOT NULL,
            TYPE TEXT NOT NULL
        );
        ''')
            connnn.commit()
            print(f'table - {clean_name} created.')

        except sqlite3.Error as e:
            print(f"error create table - {clean_name}: {e}")
    input('press any button for back menu...')

# ----------------------------------------------------------------------------2
# ---------------------------------ХЗдесь все для sql 2 пункт---------------1


def view_task_folder() -> list[str]:  # показ всех таблиц
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = [tab[0] for tab in cur.fetchall()]
        if all_tables:
            print("all_tables:")
            for w, table_all_name in enumerate(all_tables, 1):
                print(f'[{w}] -> {table_all_name}')
            return all_tables
        else:
            print('You dont have any folders with task.')
            return []
            # input('press any button for back menu...')
    except sqlite3.Error as a:
        print(f'Error when viewing folders task: {a}')
        return []
# ---------------------------------------------------------------------2
# ---------------------------------ХЗдесь все c sql 2.2 пункт---------1


def redact_view_folder() -> None:
    help_help = ""
    while True:
        start_bunner()
        tables = view_task_folder()
        if help_help:
            print(help_help)
            help_help = ""

        action_folder = input(
            'Please select an number or name a folder,'
            'or (!quit):\n->'
        )

        if action_folder.strip() in ['!q', '!quit', '!ex', '!exit']:
            break
        #
        if action_folder.isdigit():
            indx = int(action_folder) - 1
            if 0 <= indx < len(tables):
                action_folder = tables[indx]
            else:
                input('unknown number, press any button for back...')
                continue

        if proverka_un_name(action_folder):
            start_bunner()
            new_name_redacted = input(
                f'Redacting <{action_folder}>'
                f'enter a new name a table or (!q)\n->'
            )
            if new_name_redacted in ['!q', '!quit', '!ex', '!exit']:
                continue
            else:
                if new_name_redacted:
                    clean_name = ''.join(e for e in new_name_redacted
                                         if e.isalnum() or e == '_')
                    cur.execute("""SELECT name
                                FROM sqlite_master
                                WHERE type='table' AND name=?""",
                                (clean_name,))
                    if cur.fetchone():
                        input(
                            f'Folder with name - {clean_name}, already exists'
                            '\nPress any button to back menu...'
                            )
                    else:
                        if not clean_name:
                            input(
                                'Error: name is empty.'
                                '\nPress any button to back menu...'
                                )

                        else:
                            try:
                                #  one_name = redact_action.replace('"', '""')
                                #  two_name = clean_name.replace('"', '""')
                                cur.execute(f'''
                                            ALTER TABLE "{action_folder}"
                                            RENAME TO "{clean_name}"''')
                                connnn.commit()
                                input(
                                    'Name changed successfully.'
                                    f'\nNew name - <{clean_name}>'
                                    '\nPress any button to back...'
                                    )
                            except sqlite3.Error as s:
                                help_help = f'unknown command: {s}\n'
                else:

                    input(
                        'Error: You entered nothing'
                        '\nPress any button to back...'
                        )

        else:
            help_help = f'{'='*42}Name - {action_folder} not found\n{'='*42}'
# в будущем бы переенсти функцию в редакте самой папке с просмотом
# -----------------ХЗдесь все с sql 3 пункт---------------1


def del_task_folder_full(name_for_del: str) -> None:
    try:
        cur.execute("""SELECT name
                    FROM sqlite_master
                    WHERE type='table' AND name=?""",
                    (name_for_del,))
        verif_name = [tab[0] for tab in cur.fetchall()]
        if name_for_del in verif_name:
            cur.execute(f'DROP TABLE IF EXISTS "{name_for_del}"')
            connnn.commit()
            print(f'table - {name_for_del}, deleted.')

        else:
            print(f'table with name - {name_for_del}, does not exist ')
    except sqlite3.Error as w:
        print(f'error deleting table: {w}')

    input('press any button for back menu...')  # замена help_h


# -------------------------------------------------------------------------2

def start_main():
    help_h = ""
    while True:
        start_bunner()
        tables = view_task_folder()
        now = datetime.now()
        x = "-" * 16
        print(f"{x}{now.strftime('%d.%m.%Y')}{x}")
        if help_h:
            print(help_h)
            help_h = ""
        user_action = input(
            'Welcome, select an action or folder'
            '(--help):\n-> '
            )

        if user_action.lower().strip() in [
            '!quit', '!q', '!ex', '!exit'
        ]:
            print('Exit...')
            time.sleep(0.4)
            clear_all()
            break

        if user_action.isdigit():
            indx = int(user_action) - 1
            if 0 <= indx < len(tables):
                user_action = tables[indx]
            else:
                input(
                    'unknown num, press any button for back...'
                    )
                continue
        if proverka_un_name(user_action):
            start_bunner()
            task.view_and_redact(user_action)

        elif user_action.lower().strip() in [
            '--help', '-help', '--h', '-h'
        ]:
            help_h = f'''{'='*42}
--all command:
!r, !re, !ren, !rename -> redact name a folder.
!a, !add, !create, !cr -> create table.
!d, !del, !delete -> delete a folder.
!q, !quit, !ex, !exit -> for exit.\n{'='*42}'''
            continue

        elif user_action.lower().strip() in [
            '!r', '!re', '!redact'
        ]:
            redact_view_folder()

        elif user_action.lower().strip() in [
            '!a', '!add', '!create', '!cr'
        ]:
            while True:
                start_bunner()
                names = input('pls enter name task folder or !q.\n-> ').strip()
                if names in [
                    '!q', '!quit', '!ex', '!exit'
                ]:
                    break
                else:
                    add_new_table(names)

        elif user_action.lower().strip() in [
            '!d', '!del', '!delete'
        ]:
            while True:
                start_bunner()
                # view_task_folder()
                tables = view_task_folder()

                name_del = input(
                    'pls enter a task folder for del, '
                    '!q to cancel.\n-> '  # испаврить везде
                    )
                if name_del in ['!q', '!quit', '!ex', '!exit']:
                    print('back to menu...')
                    time.sleep(1)
                    break
                if name_del.isdigit():
                    indx = int(name_del) - 1
                    if 0 <= indx < len(tables):
                        name_del = tables[indx]
                    else:
                        input(
                            'unknown num, press any button for back...'
                            )
                        continue
                if proverka_un_name(name_del):
                    del_task_folder_full(name_del)
                else:
                    input('unknown name, press any button for back...')
        # здесб будет просмотр содержимого туда же и редакт перенести

        else:
            help_h = (
                f'{'='*42}\nCommand not found,'
                f'Please return your request.\n{'='*42}'
            )


if __name__ == '__main__':
    start_main()
