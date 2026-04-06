'''To work with folder.'''

import sqlite3
from .banner import start_bunner
import math


class folder_red:
    def __init__(self, connection: sqlite3.Connection):
        self.connnn = connection
        self.cur = self.connnn.cursor()

    def proverka_un_name(self, tab_nam: str) -> bool:
        self.cur.execute('''
                         SELECT name
                         FROM sqlite_master
                         WHERE type="table" AND name=?''',
                         (tab_nam,))
        return self.cur.fetchone() is not None

    def view_folder(self,
                    page: int = 1,
                    lim_page: int = 5) -> list[str]:  # показ всех таблиц
        try:
            self.cur.execute('''
                             SELECT name
                             FROM sqlite_master
                             WHERE type="table" AND NAME NOT LIKE "sqlite_%";
                             ''')
            all_tables = self.cur.fetchall()
            if not all_tables:
                print(
                    'Not folder.'
                    f'\n{'='*42}')
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
                  f'{text_center}'
                  f'\n{'='*42}')
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
            return page, "No more pages.".center(42, '='), True
        if user_input in [
            '!p', '!prev', '!l', '!last'
        ]:
            if page > 1:
                return page - 1, "", True
            return page, "You are on the first page".center(42, "="), True
        return page, "", False

    def add_new_table_folder(self, name: str) -> str:
        clean_name = ''.join(e for e in name if e.isalnum() or e == '_')
        if not clean_name:
            messages = f'Error: Name is empty.\n{'='*42}'
            return messages
        if self.proverka_un_name(clean_name):
            messages = (
                f'Error: Table, {clean_name} - already there.'
                f'\n{'='*42}')
            return messages
        else:
            try:
                self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS "{clean_name}"(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status NOT NULL DEFAULT "[ ]"
            );
            ''')
                self.connnn.commit()
                messages = (
                    f'Table - {clean_name} created.'
                    f'\n{'='*42}'
                    )
                return messages

            except sqlite3.Error as e:
                messages = (
                    f'Error: Сreate table '
                    f'- {clean_name}: {e}'
                    f'\n{'='*42}'
                    )
                return messages

    def del_folder_full(self, name_for_del: str) -> str:
        try:
            self.cur.execute(f'DROP TABLE IF EXISTS "{name_for_del}"')
            self.connnn.commit()
            message = f'table - {name_for_del}, deleted.'
            return message

        except sqlite3.Error as w:
            message = f'error deleting table: {w}'
            return message

    def redact_view_folder(self) -> None:
        page = 1
        help_help = ''
        while True:
            start_bunner()
            tables = self.view_folder(page=page)
            if help_help:
                print(help_help)
                help_help = ''

            action_folder = input(
                f'Please select an number'
                '\nor name a folder, '
                f'or (!quit):\n{'='*42}'
                f'\n>Index validation takes priority<\n{'='*42}'
                '\n->'
            )
            page, message, status = self.list_folder(
                action_folder, page, len(tables)
            )
            if action_folder.lower().strip() in [
                '!q', '!quit', '!ex', '!exit'
            ]:
                break
            if status:
                if message:
                    help_help = f'{message}\n{'='*42}'
                continue
            if not action_folder:
                help_help = f'Error: Empty string entered.\n{'='*42}'
                continue

            if action_folder.isdigit():
                indx = int(action_folder) - 1
                if 0 <= indx < len(tables):
                    action_folder = tables[indx][0]
                else:
                    help_help = (
                        f'Error: Unknown number.\n{'='*42}')
                    continue

            if self.proverka_un_name(action_folder):
                start_bunner()
                center_title = f'< Redacting {action_folder} >'.center(42, '=')
                new_name_redacted = input(
                    f'{center_title}'
                    f'\nEnter a new name, a table or (!q)\n{'='*42}\n->'
                )
                if new_name_redacted in [
                    '!q', '!quit', '!ex', '!exit'
                ]:
                    continue
                if len(new_name_redacted) > 34:
                    text = (
                        f'Error: You entered - '
                        f'{len(new_name_redacted)} symbols,'
                        f' max - 34'.center(42, '='))
                    help_help = f'{text}\n{'='*42}'
                    continue
                if not new_name_redacted:
                    help_help = f'Error: Empty string entered.\n{'='*42}'
                    continue
                else:
                    if new_name_redacted:
                        clean_name = ''.join(e for e in new_name_redacted
                                             if e.isalnum() or e == '_')
                        self.cur.execute('''
                                         SELECT name
                                         FROM sqlite_master
                                         WHERE type="table" AND name=?''',
                                         (clean_name,))
                        if self.cur.fetchone():
                            help_help = (
                                f'Error: Folder with name - {clean_name}, '
                                f'\nalready exists\n{'='*42}'
                                )
                        else:
                            if not clean_name:
                                help_help = (
                                    f'Error: name is empty.'
                                    f'\n{'='*42}'
                                    )

                            else:
                                try:
                                    self.cur.execute(f'''
                                                ALTER TABLE "{action_folder}"
                                                RENAME TO "{clean_name}"''')
                                    self.connnn.commit()
                                    help_help = (
                                        f'Name changed successfully.'
                                        f'\nNew name - >{clean_name}<'
                                        f'\n{'='*42}'
                                        )
                                except sqlite3.Error as s:
                                    help_help = (
                                        f'Error: Unknown command: {s}'
                                        f'\n{'='*42}'
                                    )
                    else:
                        help_help = (
                            f'Error: You entered nothing\n{'='*42}'
                            )

            else:
                help_help = (
                    f'Error: Name - {action_folder} '
                    f'not found\n{'='*42}'
                )
