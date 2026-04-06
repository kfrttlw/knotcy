'''To work with task.'''

import sqlite3
import math
from .banner import start_bunner
from .messages import TASK_HELP


class task_red:
    def __init__(self, connection: sqlite3.Connection):
        self.connnn = connection
        self.cur = self.connnn.cursor()

    def all_nothes_in_table(
            self, name_table: str, page: int = 1, lim_page: int = 5
            ) -> list:
        try:
            self.cur.execute(f'''
                             SELECT id,
                                    name,
                                    status
                            FROM "{name_table}"''')
            alls = self.cur.fetchall()
            if not alls:
                print('The list is empty.')
                return []
            total_task = len(alls)
            total_page = math.ceil(total_task / lim_page)
            start_num = (page - 1) * lim_page
            end_num = start_num + lim_page
            lim_id = alls[start_num:end_num]
            if alls:
                print(f'Page: {page}/{total_page}'.center(42, '='))
                for task_id, (id, name, status) in (
                        enumerate(lim_id, start=start_num + 1)):
                    print(f'{task_id}: {name} {status}')
                text_center = (
                    '!n - next page || !p - prev page'.center(42, '='))
                print(f'{'='*42}\n'
                      f'{text_center}')
            return alls

        except sqlite3.Error as w:
            print(f'Error reading table - {name_table}:\n{w}')
            return []

    def movie_task(
            self,
            input_user: str,
            page: int,
            total_items: int,
            limit: int = 5
            ) -> tuple[int, str, bool]:
        if input_user in [
            '!n', '!next'
        ]:
            if page * limit < total_items:
                return page + 1, "", True
            return page, "No more pages.".center(42, '='), True
        if input_user in [
            '!p', '!prev', '!l', '!last'
        ]:
            if page > 1:
                return page - 1, "", True
            return page, "You are on the first page".center(42, "="), True
        return page, "", False

    def create_task(self, name_table: str) -> None:
        entry = ''
        while True:
            start_bunner()
            print(f'< You in {name_table}>'.center(42, '='))
            if entry:
                print(entry)
                entry = ''
            new_task = input(
                f'{'='*42}\nEnter your task or (!q)\n{'='*42}\n-> '
                )
            if new_task.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            if len(new_task) > 34:
                text = (
                    f'Error: You entered - '
                    f'{len(new_task)} symbols,'
                    ' max - 34')
                entry = f'{'='*42}\n{text}'
                continue
            else:
                self.cur.execute(
                    f'INSERT INTO "{name_table}" (name) VALUES (?)',
                    (new_task,)
                )
                self.connnn.commit()
                text_created = (
                    '< Created successfully. >'
                    .center(42, '=')
                )
                entry = (
                    f'{'='*42}\n{text_created}'
                )

    def deleting_task(self, name_table: str) -> None:
        help_help = ""
        page = 1
        while True:
            start_bunner()
            real_num = self.all_nothes_in_table(name_table, page=page)
            if help_help:
                print(help_help)
                help_help = ""
            num_table = input(
                f'{'='*42}\n'
                f'Select a number for deleting or (!q).\n{'='*42}\n-> '
                )
            page, text, check = self.movie_task(
                num_table, page, len(real_num)
            )
            if num_table in [
                '!quit', '!q', '!ex', '!exit'
            ]:
                break
            if check:
                help_help = f'{text}'
                continue
            else:
                try:
                    number_table = int(num_table)
                    if 1 <= number_table <= len(real_num):
                        id_db, name, status = real_num[number_table - 1]
                        try:
                            self.cur.execute(
                                f'''
                                DELETE FROM "{name_table}"
                                WHERE id = ?''',
                                (id_db,)
                                )
                            self.connnn.commit()
                            help_help = (
                                f'{'='*42}\nSuccessfully deleted Task:'
                                f'\n{number_table}: {name} {status}.'
                            )
                        except sqlite3.Error as a:
                            help_help = (
                                f'Error sqlite: {a}'
                            )
                    else:
                        help_help = (
                            f'{'='*42}\nNumber - {number_table} '
                            'not found in list.'
                        )
                except ValueError:
                    help_help = (
                                f'{'='*42}\nError: Enter a valid number.'
                            )

    def redact_task(self, name_table: str) -> None:
        page = 1
        help_help = ''
        while True:
            start_bunner()
            real_num = self.all_nothes_in_table(name_table, page=page)
            if help_help:
                print(help_help)
                help_help = ''
            slash = f'{'='*42}'
            view = '>You in redact function<'.center(42, '=')
            user_input = input(
                f'{slash}\n{view}\n'
                f'{slash}\nSelect a number or (!q).\n{slash}\n->')
            page, message, check = self.movie_task(
                user_input, page, len(real_num)
                )
            if user_input.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            if check:
                if message:
                    help_help = f'{'='*42}\n{message}'
                continue
            if not user_input:
                help_help = f'{'='*42}\nError: Empty string entered.'
                continue
            else:
                try:
                    num_table = int(user_input)
                    if 1 <= num_table <= len(real_num):
                        db_id, name, status = real_num[num_table - 1]
                        start_bunner()
                        print(
                            f'You redacted - {name} {status}'.center(42, '=')
                            )
                        new_task = input(
                            f'{slash}\nInput new name task or (!q).'
                            f'\n{slash}\n-> '
                        ).strip()
                        if new_task in [
                            '!q', '!quit', '!ex', '!exit'
                        ]:
                            continue
                        if not new_task:
                            help_help = (
                                f'{'='*42}\nError: You entered Empty string.')
                            continue
                        if len(new_task) > 34:
                            text_lenght = (
                                f'Error: You entered - '
                                f'{len(new_task)} symbols,'
                                ' max - 34')
                            help_help = f'{'='*42}\n{text_lenght}'
                        else:
                            try:
                                self.cur.execute(
                                    f'''
                                    UPDATE "{name_table}"
                                    SET name = ?
                                    WHERE id = ?''',
                                    (new_task, db_id))
                                self.connnn.commit()
                                task_done_redact = (
                                    'Task update successfully.'.center(42, '=')
                                    )
                                help_help = (
                                    f'{slash}\n'
                                    f'{task_done_redact}'
                                )
                            except sqlite3.Error as e:
                                help_help = (
                                    f'Error sqlite3: {e}'
                                )
                    else:
                        help_help = (
                            f'{'='*42}\nNumber - {num_table}, not on the list.'
                        )
                except ValueError:
                    help_help = (
                        f'{'='*42}\nError: Enter a valid number.'
                    )

    def complete_task(self, name_table: str) -> None:
        page = 1
        help_help = ''
        while True:
            start_bunner()
            real_num = self.all_nothes_in_table(name_table, page=page)
            if help_help:
                print(help_help)
                help_help = ''
            input_user = input(
                f'{'='*42}\nSelect a number in task\nfor complete, or (!q).'
                f'\n{'='*42}.\n-> '
                )
            page, message, check = self.movie_task(
                input_user, page, len(real_num)
                )
            if input_user in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            if check:
                if message:
                    help_help = f'{'='*42}\n{message}'
                continue
            else:
                try:
                    num_table = int(input_user)
                    if 1 <= num_table <= len(real_num):
                        db_id, name, status = real_num[num_table - 1]
                        self.cur.execute(f'''
                                         SELECT status
                                         FROM "{name_table}"
                                         WHERE id = ?''',
                                         (db_id,))
                        current_status = self.cur.fetchone()[0]
                        new_status = (
                            '[X]' if current_status == '[ ]'
                            else '[ ]'
                        )
                        self.cur.execute(f'''
                                         UPDATE "{name_table}"
                                         SET status = ?
                                         WHERE id = ?''',
                                         (new_status, db_id))
                        self.connnn.commit()
                        help_help = (
                            f'{'='*42}\n'
                            'Status - update successfully.'
                        )
                    else:
                        help_help = (
                            f'{'='*42}\nNumber - {num_table}, not on the list.'
                        )

                except ValueError:
                    help_help = (
                        f'{'='*42}\nError: Enter a valid number.'
                    )

    #  main
    def view_and_redact(self, name_table: str,) -> None:
        page = 1
        help_help = ''
        while True:
            start_bunner()
            print(f'<You in {name_table}>'.center(42, '='))
            real_num = self.all_nothes_in_table(name_table, page=page)
            if help_help:
                print(help_help)
                help_help = ''
            action = input(f'{'='*42}\nSelect number or (--help):'
                           f'\n{'='*42}\n->')
            page, message, check = self.movie_task(action, page, len(real_num))
            if action.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            if check:
                if message:
                    help_help = f'{'='*42}\n{message}'
                continue
            if action.lower().strip() in [
                '--help', '-help', '--h', '-h'
            ]:
                help_help = (
                    f'{'='*42}\n{TASK_HELP}'
                )
                continue
            elif action.lower().strip() in [
                '!a', '!add', '!cr', '!create'
            ]:
                self.create_task(name_table)
            elif action.lower().strip() in [
                '!d', '!delete', '!del'
            ]:
                self.deleting_task(name_table)
            elif action.lower().strip() in [
                '!r', '!re', '!ren', '!rename'
            ]:
                self.redact_task(name_table)
            elif action.lower().strip() in [
                '!c', '!complete', '!done'
            ]:
                self.complete_task(name_table)
            else:
                help_help = f'{'='*42}\nNot found command - {action}.'
