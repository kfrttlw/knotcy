import os
import sqlite3
import time
import random
import string
from datetime import datetime


#---------forcomfy------------------------------1
rise = r""" ____  __.              __                
|    |/ _| ____   _____/  |_  ____ ___.__.
|      <  /    \ /  _ \   __\/ ___<   |  |
|    |  \|   |  (  <_> )  | \  \___\___  |
|____|__ \___|  /\____/|__|  \___  > ____|
        \/    \/                 \/\/"""
slash = '=' * 20 + '<>' + '=' * 20

def clear_all():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_bunner(info=""):
    clear_all()
    print(f'{slash}\n{rise}\n{slash}')
    if info:
        print(info)


def proverka_un_name(tab_nam): 
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tab_nam,))
    return cur.fetchone() is not None
#---------forcomfy------------------------------2
# ---------------------------------ХЗдесь все с sql 1 пункт------------------------------------1
connnn = sqlite3.connect('base.sqlite')
cur = connnn.cursor()

# для создания папки задач
def add_new_table(name):

    clean_name = ''.join(e for e in name if e.isalnum() or e == '_')

    if not clean_name:
        input('Error: name is empty.\nPress any buuton to back menu...')
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

# ---------------------------------------------------------------------------------------------2 

# ---------------------------------ХЗдесь все для sql 2 пункт------------------------------------1
def view_task_folder(): # показ всех таблиц 
    
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")


        all_tables = [tab[0] for tab in cur.fetchall()]

        if all_tables:
            print("all_tables:")
            for w, table_all_name in enumerate(all_tables, 1):
                print(f'[{w}] -> {table_all_name}')
            return all_tables
            
            
            # for tabl_all in all_tables:
            #     print(f'[0] -> {tabl_all[0]}')
            
        else:
            print('You dont have any folders with task.')
            return []
            # input('press any button for back menu...') 
    except sqlite3.Error as a:
        print(f'Error when viewing folders task: {a}')
        return []    
    # input('press any button for back menu...') 

# ---------------------------------------------------------------------------------------------2
# ---------------------------------ХЗдесь все c sql 2.2 пункт------------------------------------1
def redact_view_folder():
    while True:
        start_bunner()
        view_task_folder()

        action_folder = input('''Please select an numer or name a folder, or:
!r - redact name a folder.
!d - delete a folder.
!q - for back menu.
-> ''')
        
        if action_folder.strip() in ['!q', '!quit', '!ex', '!exit']:
            print('retunr to menu...')
            time.sleep(1)
            break
        elif action_folder.strip() in ['!d', '!del', '!delete']:
            while True:
                start_bunner()
                # view_task_folder()
                tables = view_task_folder()

                name_del = input('pls enter a task folder for del, q to cancel.\n-> ')
                if name_del in ['!q', '!quit', '!ex', '!exit']:
                    print('back to menu...')
                    time.sleep(1)
                    break 
                if name_del.isdigit():
                    indx = int(name_del) - 1
                    if 0 <= indx < len(tables):
                        name_del = tables[indx]
                    else:
                        input('unknown command, press any button for back...')
                        continue
                if name_del:
                    del_task_folder_full(name_del)
                else:
                    input('unknown command, press any button for back...')
        
        elif action_folder.strip() in ['!r', '!re', '!ren', '!rename']:
            try:
                while True:
                    start_bunner()
                    view_task_folder()
                    redact_action = input('Select a folder for redact he name.\n-> ') 
                
                    if redact_action in ['!q', '!quit', '!ex', '!exit']:
                            break
                    if proverka_un_name(redact_action):
                        # while True:
                        start_bunner()
                        print(f'you redacted -> {redact_action}')


                        new_name_redacted = input('''Select a new name a table or, 
!q for exit:
-> ''')
                        if new_name_redacted in ['!q', '!quit', '!ex', '!exit']:
                            break
                        else:
                            if new_name_redacted:

                                # замена на шифр чтоб не было повторений с другими именами при проверке копийw
                                # new_named_for_mask = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range (random.randint(20, 30)))
                                # cur.execute(f"ALTER TABLE {redact_action} RENAME TO {new_named_for_mask}")  
                                # connnn.commit()
                                # -
                                
                                clean_name = ''.join(e for e in new_name_redacted if e.isalnum() or e == '_')
                                cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (clean_name,))
                                if cur.fetchone():        
                                    input(f'A folder with that name - {clean_name}, already exists\nPress any button to back menu...')
                                else:    
                                    if not clean_name:
                                        input('Error: name is empty.\nPress any button to back menu...')
                                        
                                    # крч здесь доделать логику имя принимает маску но если такое имя существует то маска остается навсеглдда 
                                    else:
                                        # one_name = redact_action.replace('"', '""')
                                        # two_name = clean_name.replace('"', '""')
                                        cur.execute(f'ALTER TABLE "{redact_action}" RENAME TO "{clean_name}"')
                                        connnn.commit()
                                        input('Name changed successfully\nPress any button to back...')
                            else: 
                                input('Error: You entered nothing.\nPress any button to back...')
                                    
                
                    else:
                        input(f'Name - {redact_action} not found\nPlease Press any button to back...')

                
            except sqlite3.error as s:
                input(f'unknown command: {s}\nPress any button for back...')
                            
        else:
            input('Command not found, pls return your request.\nPress any button to back...')


# ---------------------------------------------------------------------------------------------2
# ---------------------------------ХЗдесь все с sql 2.3 пункт------------------------------------1

#дописатьв выбор и работу  и мейби переименовать функции не на просмотр а на выбор  конкретно 2 пункт

# ---------------------------------------------------------------------------------------------2

# ---------------------------------ХЗдесь все с sql 3 пункт------------------------------------1
def del_task_folder_full(name_for_del):
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

    input('press any button for back menu...') 
    


# ---------------------------------------------------------------------------------------------2

def start_menu():
    while True:
        # clear_all()
        # print(f'{slash}\n{rise}\n{slash}')
        start_bunner()

        now = datetime.now()
        x = "-" * 16
        
        
        print(f"{x}{now.strftime('%d.%m.%Y')}{x}")

        user_q = input('''Welcome, select action:
1 - add a new task folder.
2 - view task folders.
exit or quit - for exit
-> ''')
        
        if user_q.lower().strip() in ['1', 'add', 'new']:
            start_bunner()
            names = input('pls enter name task folder.\n-> ').strip()
            add_new_table(names)
            
            # input('press any button...')
        elif user_q.lower().strip() in ['2', 'two', 'view']: # доделать!
            help_h = ""
            while True:
                start_bunner()
                view_task_folder()
                if help_h:
                    print(help_h)
                    help_h = ""
                user_action_two = input('please select an action or (--help, !quit, !redact):\n->  ') 


                if user_action_two.lower().strip() in ['!quit', '!q', '!ex', '!exit']:
                    print('retutn to main menu...')
                    time.sleep(1)
                    break
                elif user_action_two.lower().strip() in ['--help', '-help', '--h', '-h']:
                    help_h = f'''{'='*42}
--all command:
!r , !redact - for redacted name your folder.
!q, !quit, !ex, !exit - for exit.\n{'='*42}'''
                    continue                
                                   
                elif user_action_two.lower().strip() in ['!r', '!redact']:
                    redact_view_folder()
                else:
                    help_h = f'{'='*42}\nCommand not found, pls return your request.\n{'='*42}'



        elif user_q.lower().strip() in ['exit', 'ex', 'quit', 'q']:
            start_bunner()
            print('thank you, goodbye!')
            break
        
        else:
            start_bunner()
            print('command not found')
            input('press any button for back menu...')


start_menu()



# при переименовании \ git remote set-url origin git@github.com:ваш_логин/новое_название.git


