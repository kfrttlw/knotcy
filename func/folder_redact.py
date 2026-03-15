'''To work with folder.'''

import sqlite3
from .banner import start_bunner
import math


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

    def view_folder(self,
                    page: int = 1,
                    lim_page: int = 5) -> list[str]:  # показ всех таблиц
        try:
            self.cur.execute("""
                             SELECT name
                             FROM sqlite_master
                             WHERE type='table' AND NAME NOT LIKE 'sqlite_%';
                             """)
            all_tables = self.cur.fetchall()
            if not all_tables:
                print('Not folder.')
                return []
            total_folder = len(all_tables)
            total_page = math.ceil(total_folder / lim_page)
            start_num = (page - 1) * lim_page
            end_num = start_num + lim_page
            lim_id = all_tables[start_num:end_num]

            print('>all_tables<'.center(42, '='))
            print(f'{page}/{total_page}'.center(42, '='))
            for number, table_all_name in enumerate(
                lim_id, start=start_num + 1
            ):
                print(f'[{number}] -> {table_all_name[0]}')
            text_center = (
                '!n - next page || !p - prev page'.center(42, '='))
            print(f'{'='*42}\n'
                  f'{text_center}')
            return all_tables
        except sqlite3.Error as a:
            print(f'Error when viewing folders task: {a}')
            return []

    def list_folder(self,
                    user_input,
                    page,
                    total_items,
                    limit_table: int = 5
                    ) -> tuple[int, str, bool]:
        if user_input in [
            '!n', '!next'
        ]:
            if page * limit_table < total_items:
                return page + 1, "", True
            return page, "No more pages.", True
        if user_input in [
            '!p', '!prev', '!l', '!last'
        ]:
            if page > 1:
                return page - 1, "", True
            return page, "You are on the first page".center(42, "="), True
        return page, "", False

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
                f'{'='*42}\nPlease select an number '
                '\nor name a folder, '
                f'or (!quit):\n{'='*42}\n->'
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
                center_title = f'< Redacting {action_folder} >'.center(42, '=')
                new_name_redacted = input(
                    f'{center_title}'
                    f'\nenter a new name, a table or (!q)\n{'='*42}\n->'
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
                                f'{'='*42}\nFolder with name - {clean_name}, '
                                'already exists'
                                f'\nPress any button to back menu...\n{'='*42}'
                                )
                        else:
                            if not clean_name:
                                input(
                                    f'{'='*42}\nError: name is empty.'
                                    f'\nPress any button '
                                    f'to back menu...\n{'='*42}'
                                    )

                            else:
                                try:
                                    self.cur.execute(f'''
                                                ALTER TABLE "{action_folder}"
                                                RENAME TO "{clean_name}"''')
                                    self.connnn.commit()
                                    help_help = (
                                        f'{'='*42}\nName changed successfully.'
                                        f'\nNew name - <{clean_name}>'
                                        )
                                except sqlite3.Error as s:
                                    help_help = (
                                        f'{'='*42}\nunknown command: {s}'
                                        f'\n{'='*42}'
                                    )
                    else:

                        help_help = (
                            f'{'='*42}\nError: You entered nothing\n{'='*42}'
                            )

            else:
                help_help = (
                    f'{'='*42}\nName - {action_folder} '
                    f'not found\n{'='*42}'
                )
