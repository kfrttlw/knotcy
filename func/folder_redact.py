import sqlite3
from .banner import start_bunner


class folder_red:
    def __init__(self, connection: sqlite3.Connection):
        self.connnn = connection
        self.cur = self.connnn.cursor()

    def proverka_un_name(self, tab_nam: str) -> bool:
        self.cur.execute("""
                         SELECT name
                         FROM sqlite_master
                         WHERE type='table' AND name=?""",
                         (tab_nam,))
        return self.cur.fetchone() is not None

    def view_folder(self) -> list[str]:  # показ всех таблиц
        try:
            self.cur.execute("""
                             SELECT name
                             FROM sqlite_master
                             WHERE type='table' AND NAME NOT LIKE 'sqlite_%';
                             """)
            # разгрузить глаза потом слишком много места занимают =
            all_tables = [tab[0] for tab in self.cur.fetchall()]
            if all_tables:
                print(f"{'='*42}\nall_tables:")
                for w, table_all_name in enumerate(all_tables, 1):
                    print(f'[{w}] -> {table_all_name}')
                return all_tables
            else:
                print(f'{'='*42}\nYou dont have any folders with task.')
                return []
        except sqlite3.Error as a:
            print(f'Error when viewing folders task: {a}')
            return []

    def add_new_table_folder(self, name: str) -> None:
        clean_name = ''.join(e for e in name if e.isalnum() or e == '_')
        if not clean_name:
            input(
                f'{'='*42}\nError: name is empty.'
                f'\nPress any button to back menu...\n{'='*42}'
                )
            return
        if self.proverka_un_name(clean_name):
            input(
                f'{'='*42}\nTable, {clean_name} - already there.'
                f'\npress any button for back menu...\n{'='*42}'
                )
            # input('press any button for back menu...')
        else:
            try:
                self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS "{clean_name}"(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status NOT NULL DEFAULT '[ ]'
            );
            ''')
                self.connnn.commit()
                input(
                    f'{'='*42}\ntable - {clean_name} created.'
                    f'\npress any button for back menu...\n{'='*42}'
                    )

            except sqlite3.Error as e:
                input(
                    f'{'='*42}\nerror create table'
                    f'- {clean_name}: {e}'
                    f'\npress any button for back menu...\n{'='*42}'
                    )

    def del_folder_full(self, name_for_del: str) -> None:
        try:
            self.cur.execute("""
                             SELECT name
                             FROM sqlite_master
                             WHERE type='table' AND name=?""",
                             (name_for_del,))
            verif_name = [tab[0] for tab in self.cur.fetchall()]
            if name_for_del in verif_name:
                self.cur.execute(f'DROP TABLE IF EXISTS "{name_for_del}"')
                self.connnn.commit()
                print(f'table - {name_for_del}, deleted.')

            else:
                print(f'table with name - {name_for_del}, does not exist ')
        except sqlite3.Error as w:
            print(f'error deleting table: {w}')

        input('press any button for back menu...')  # замена help_h

    def redact_view_folder(self) -> None:
        help_help = ""
        while True:
            start_bunner()
            tables = self.view_folder()
            if help_help:
                print(help_help)
                help_help = ""

            action_folder = input(
                'Please select an number or name a folder,'
                'or (!quit):\n->'
            )

            if action_folder.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            #
            if action_folder.isdigit():
                indx = int(action_folder) - 1
                if 0 <= indx < len(tables):
                    action_folder = tables[indx]
                else:
                    input('unknown number, press any button for back...')
                    continue

            if self.proverka_un_name(action_folder):
                start_bunner()
                new_name_redacted = input(
                    f'Redacting <{action_folder}>'
                    f'enter a new name a table or (!q)\n->'
                )
                if new_name_redacted in [
                    '!q', '!quit', '!ex', '!exit'
                ]:
                    continue
                else:
                    if new_name_redacted:
                        clean_name = ''.join(e for e in new_name_redacted
                                             if e.isalnum() or e == '_')
                        self.cur.execute("""
                                         SELECT name
                                         FROM sqlite_master
                                         WHERE type='table' AND name=?""",
                                         (clean_name,))
                        if self.cur.fetchone():
                            input(
                                f'Folder with name - {clean_name}, '
                                'already exists'
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
                                    self.cur.execute(f'''
                                                ALTER TABLE "{action_folder}"
                                                RENAME TO "{clean_name}"''')
                                    self.connnn.commit()
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
                help_help = (
                    f'{'='*42}Name - {action_folder} '
                    f'not found\n{'='*42}'
                )
