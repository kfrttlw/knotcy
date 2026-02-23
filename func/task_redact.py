import sqlite3
from .banner import start_bunner


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

            new_task = input('Enter your task or (!q)\n-> ')
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
                entry = f'{'='*7}Created a new task in <{name_table}>{'='*7}'

        def deleting_task(self, name_table: str) -> None:
            help_help = ""
            while True:
                start_bunner()
                real_num = self.all_nothes_in_table(name_table)
                if real_num:
                    if help_help:
                        print(help_help)
                        help_help = ""
                    num_table = int(input(
                        'Select a number for deleting or (!q).\n-> '
                        ))
                    if num_table in [
                        '!quit', '!q', '!ex', '!exit'
                    ]:
                        break
                    if 1 <= real_num <= len(real_num):
                        id_task = real_num[num_table - 1]
                        try:
                            self.cur.execute(f'''
                                             DELETE FROM "{name_table}"
                                             WHERE id = ?''',
                                             (id_task,))
                            self.connnn.commit()
                        except sqlite3.Error as a:
                            help_help = (
                                f'Error: {a}'
                            )

    #  main
    def view_and_redact(self, name_table: str,) -> None:
        help_help = ""
        while True:
            start_bunner()
            print(f'{'='*15}<You in {name_table}>{'='*15}')
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
                help_help = f'''{'='*42}
    --all command:
    !r, !re, !redact, !redacte -> redact task.
    !a, !add, !cr, !create -> create a task.
    !d, !del, !delete -> delete a task.
    !q, !quit, !ex, !exit -> for back menu.'''
                continue
            elif action.lower().strip() in [
                '!a', '!add', '!cr', '!create'
            ]:
                self.create_task(name_table)

            else:
                help_help = f'{'='*42}\nNot found command - {action}.'
