'''To work with task.'''

import sqlite3
from .banner import start_bunner
from .messages import TASK_HELP


class task_red:
    def __init__(self, connection: sqlite3.Connection):
        self.connnn = connection
        self.cur = self.connnn.cursor()

    def all_nothes_in_table(self, name_table: str) -> list:
        try:
            self.cur.execute(f'''
                             SELECT id,
                                    name,
                                    status
                            FROM "{name_table}"''')
            alls = self.cur.fetchall()
            if not alls:
                print('Список пуст.')
                return []

            real_num = []
            if alls:
                for task_id, (id, name, status) in enumerate(alls, start=1):
                    print(f'{task_id}: {name} {status}')  # сделать нумерциаю
                    real_num.append(id)
            return real_num
            # доработать чтоб было сверху
        except sqlite3.Error as w:
            print(f'Error reading table - {name_table}:\n{w}')
            return []

    def create_task(self, name_table: str) -> None:
        entry = ""
        while True:
            start_bunner()
            if entry:
                print(entry)
                entry = ""
            print(f'< You in {name_table}>'.center(42, '='))
            new_task = input(
                f'{'='*42}\nEnter your task or (!q)\n{'='*42}\n-> '
                )
            if new_task.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            else:
                self.cur.execute(
                    f"INSERT INTO {name_table} (name) VALUES (?)",
                    (new_task,)
                )
                self.connnn.commit()
                entry = (
                    '< Created successfuly. >'
                    .center(42, '=')
                )

    def deleting_task(self, name_table: str) -> None:
        help_help = ""
        while True:
            start_bunner()
            real_num = self.all_nothes_in_table(name_table)
            if real_num:
                if help_help:
                    print(help_help)
                    help_help = ""
                num_table = input(
                    f'{'='*42}\n'
                    'Select a number for deleting or (!q).\n-> '
                    )
                if num_table in [
                    '!quit', '!q', '!ex', '!exit'
                ]:
                    break
                else:
                    try:
                        number_table = int(num_table)
                        if 1 <= number_table <= len(real_num):
                            id_task = real_num[number_table - 1]
                            try:
                                self.cur.execute(
                                    f'''
                                    DELETE FROM "{name_table}"
                                    WHERE id = ?''',
                                    (id_task,)
                                    )
                                self.connnn.commit()
                            except sqlite3.Error as a:
                                help_help = (
                                    f'Error sqlite: {a}'
                                )
                        else:
                            help_help = (
                                f'Number - {number_table} '
                                'not found in list.'
                            )
                    except ValueError as e:
                        help_help = (
                                    f'Error number: {e}'
                                )

    def redact_task(self, name_table: str) -> None:
        help_help = ""
        while True:
            start_bunner()
            real_num = self.all_nothes_in_table(name_table)
            if help_help:
                print(help_help)
                help_help = ""
            user_input = input(f'{'='*42}\nSelect a number or (!q).\n->')
            if user_input.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            else:
                try:
                    num_table = int(user_input)
                    if 1 <= num_table <= len(real_num):
                        id_task = real_num[num_table - 1]
                        new_task = input(
                            f'{'='*42}\nInput new task or (!q).\n-> '
                        ).strip()
                        if new_task in [
                            '!q', '!quit', '!ex', '!exit'
                        ]:
                            break
                        else:
                            try:
                                self.cur.execute(
                                    f'''
                                    UPDATE "{name_table}"
                                    SET name = ?
                                    WHERE id =?''',
                                    (new_task, id_task))
                                self.connnn.commit()
                                help_help = (
                                    'Task update successfuly.'
                                )
                            except sqlite3.Error as e:
                                help_help = (
                                    f'Error sqlite3: {e}'
                                )
                    else:
                        help_help = (
                            f'Number - {num_table}, not on the list.'
                        )
                except ValueError as a:
                    help_help = (
                        f'Error value: {a}'
                    )

    def complete_task(self, name_table: str) -> None:
        # мейби сделать ретурн для вывода прогресса
        help_help = ""
        while True:
            start_bunner()
            real_num = self.all_nothes_in_table(name_table)
            if help_help:
                print(help_help)
                help_help = ""
            input_user = input(
                f'{'='*42}\nSelect a number in task for complete or (!q)'
                f'\n{'='*42}.\n-> '
                )
            if input_user in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            else:
                try:
                    num_table: int = int(input_user)
                    if 1 <= num_table <= len(real_num):
                        id_task = real_num[num_table - 1]
                        while True:
                            start_bunner()
                            self.all_nothes_in_table(name_table)
                            center_title = (
                                f'< You redacted task - {id_task}. >'
                                .center(42, '=')
                                )
                            check_status = input(
                                f'{center_title}'
                                '\nPress any button to switch '
                                f'status or (!q).\n{'='*42}\n-> '
                            )
                            if check_status in [
                                '!q', '!quit', '!ex', '!exit'
                            ]:
                                break
                            else:
                                try:
                                    self.cur.execute(f'''
                                                     SELECT status
                                                     FROM "{name_table}"
                                                     WHERE id = ?''',
                                                     (id_task,))
                                    current_status = self.cur.fetchone()[0]
                                    new_status = (
                                        '[X]' if current_status == '[ ]'
                                        else '[ ]'
                                    )
                                    self.cur.execute(f'''
                                                     UPDATE {name_table}
                                                     SET status = ?
                                                     WHERE id = ?''',
                                                     (new_status, id_task))
                                    self.connnn.commit()
                                    help_help = (
                                        f'{'='*42}\nStatus update successfuly.'
                                    )
                                except sqlite3.Error as q:
                                    help_help = (
                                        f'Error sqlite3: {q}'
                                    )
                    else:
                        help_help = (
                            f'{'='*42}\nNumber - {num_table}, not on the list.'
                        )

                except ValueError as q:
                    help_help = (
                        f'\n{'='*42}Error value: {q} .'
                    )

    #  main
    def view_and_redact(self, name_table: str,) -> None:
        help_help = ""
        while True:
            start_bunner()
            print(f'<You in {name_table}>'.center(42, '='))
            self.all_nothes_in_table(name_table)
            if help_help:
                print(help_help)
                help_help = ""
            # здесб сделать чтоб подстравиволось под название крч
            action = input(f'{'='*42}\nSelect action or (--help):\n->')
            if action.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
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
