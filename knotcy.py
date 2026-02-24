'''Main entry point for the Knotcy task manager.'''

import sqlite3
import time
from func import start_bunner
from func import clear_all
from datetime import datetime
from func import task_red
from func import folder_red
from func import FOLDER_HELP
# ---------forcomfy------------------------------1
slash = '=' * 20 + '<>' + '=' * 20
connnn = sqlite3.connect('knotcy_base.sqlite')
cur = connnn.cursor()
# подключения class
task = task_red(connnn)
folder = folder_red(connnn)
# -------------------------------------------------------------------------2


def start_main():
    help_h = ""
    while True:
        start_bunner()
        now = datetime.now()
        x = "-" * 16
        print(f"{x}{now.strftime('%d.%m.%Y')}{x}")
        tables = folder.view_folder()
        if help_h:
            print(help_h)
            help_h = ""
        user_action = input(
            f'{'='*42}\n'
            'Welcome, select an action or folder'
            f'(--help):\n{'='*42}\n-> '  # мейби убрать =
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
        if folder.proverka_un_name(user_action):
            start_bunner()
            task.view_and_redact(user_action)

        elif user_action.lower().strip() in [
            '--help', '-help', '--h', '-h'
        ]:
            help_h = (
                f'{'='*42}\n{FOLDER_HELP}\n{'='*42}'
            )
            continue

        elif user_action.lower().strip() in [
            '!r', '!re', '!redact'
        ]:
            folder.redact_view_folder()

        elif user_action.lower().strip() in [
            '!a', '!add', '!create', '!cr'
        ]:
            while True:
                start_bunner()
                names = input(
                    f'Enter name task folder or !q.'
                    f'\n{'='*42}\n-> '
                ).strip()
                if names in [
                    '!q', '!quit', '!ex', '!exit'
                ]:
                    break
                else:
                    folder.add_new_table_folder(names)

        elif user_action.lower().strip() in [
            '!d', '!del', '!delete'
        ]:
            while True:
                start_bunner()
                tables = folder.view_folder()

                name_del = input(
                    'pls enter a folder for del, '
                    '!q to cancel.\n-> '
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
                if folder.proverka_un_name(name_del):
                    folder.del_folder_full(name_del)
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
