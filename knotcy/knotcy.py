'''Main entry point for the Knotcy task manager.'''

import sqlite3
import time
import os
from .func import start_bunner
from .func import clear_all
from datetime import datetime
from .func import task_red
from .func import folder_red
from .func import FOLDER_HELP, INFO
from .func import delete_db
# ---------forcomfy------------------------------1
slash = '=' * 20 + '<>' + '=' * 20
db_path = os.path.expanduser("~/.knotcy_db.db")
connnn = sqlite3.connect(db_path)
cur = connnn.cursor()
# подключения class
task = task_red(connnn)
folder = folder_red(connnn)
# -------------------------------------------------------------------------2


def start_main():
    page = 1
    help_h = ''
    while True:
        start_bunner()
        now = datetime.now()
        x = '-' * 16
        print(f'{x}{now.strftime('%d.%m.%Y')}{x}')
        tables = folder.view_folder(page=page)
        if help_h:
            print(help_h)
            help_h = ''
        action_text = 'Select an action or folder:'.center(42, '=')
        help_text = '(--help)'.center(42, '=')
        user_action = input(
            f'{action_text}'
            f'\n{help_text}\n-> ')

        page, messages, status = folder.list_folder(
            user_action, page, len(tables)
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
                user_action = tables[indx][0]
            else:
                text = 'Error: You entered unknown num.'.center(42, '=')
                help_h = (
                    f'{text}'
                    f'\n{'='*42}'
                    )
                continue
        if folder.proverka_un_name(user_action):
            task.view_and_redact(user_action)
            continue

        if status:
            if messages:
                help_h = (
                    f'{messages}'
                    f'\n{'='*42}')
            continue

        elif user_action.lower().strip() in [
            '--help', '-help', '--h', '-h'
        ]:
            help_h = (
                f'{FOLDER_HELP}\n{'='*42}'
            )
            continue
        elif user_action.lower().strip() in [
            '!info', '!inf'
        ]:
            help_h = (
                f'{INFO}\n{'='*42}'
            )

        elif user_action.lower().strip() in [
            '!deldb', '!dbdel'
        ]:
            status, message = delete_db(connnn, db_path)
            if status:
                start_bunner()
                print(
                    f'{message}\n{'='*42}'
                    )
                break
            else:
                help_h = f'{message}\n{'='*42}'
                continue

        elif user_action.lower().strip() in [
            '!r', '!re', '!redact'
        ]:
            folder.redact_view_folder()

        elif user_action.lower().strip() in [
            '!a', '!add', '!create', '!cr'
        ]:
            help_add = ''
            while True:
                start_bunner()
                if help_add:
                    print(help_add)
                    help_add = ''
                names = input(
                    f'Enter name task folder or !q.'
                    f'\n{'='*42}\n-> '
                ).strip()
                if names in [
                    '!q', '!quit', '!ex', '!exit'
                ]:
                    break
                if len(names) > 34:
                    text = (
                        f'You entered - {len(names)} symbols, '
                        f'max - 34'.center(42, '='))
                    help_add = (
                        f'{text}\n{'='*42}'
                    )
                    continue
                else:
                    messages = folder.add_new_table_folder(names)
                    help_add = f'{messages}'
                    continue

        elif user_action.lower().strip() in [
            '!d', '!del', '!delete'
        ]:
            page = 1
            help_h = ''
            while True:
                start_bunner()
                tables = folder.view_folder(page=page)
                if help_h:
                    print(help_h)
                    help_h = ''
                name_del = input(
                    'pls enter a folder for del,'
                    '\nor !q to exit.\n'
                    f'{'='*42}\n>Index validation takes priority<'
                    f'\n{'='*42}\n-> '
                    )
                page, messages, check = folder.list_folder(
                    name_del, page, len(tables)
                )
                if name_del in ['!q', '!quit', '!ex', '!exit']:
                    break
                if check:
                    if messages:
                        help_h = (
                            f'{messages}'
                            f'\n{'='*42}')
                    continue
                if name_del.isdigit():
                    indx = int(name_del) - 1
                    if 0 <= indx < len(tables):
                        name_del = tables[indx][0]
                    else:
                        text = 'Error: Unknown number.'.center(42, '=')
                        help_h = (
                            f'{text}'
                            f'\n{'='*42}'
                            )
                        continue
                if folder.proverka_un_name(name_del):
                    messages = folder.del_folder_full(name_del)
                    help_h = (
                        f'{messages}'
                        f'\n{'='*42}')
                    continue
                else:
                    text = 'Error: Unknown name.'.center(42, '=')
                    help_h = (
                        f'{text}'
                        f'\n{'='*42}')

        else:
            text = 'Error: command not found'.center(42, '=')
            help_h = (
                f'{text}'
                f'\n{'='*42}'
            )


if __name__ == '__main__':
    start_main()
