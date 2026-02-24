'''To display a banner.'''

import os

# banner

rise = r""" ____  __.              __
|    |/ _| ____   _____/  |_  ____ ___.__.
|      <  /    \ /  _ \   __\/ ___<   |  |
|    |  \|   |  (  <_> )  | \  \___\___  |
|____|__ \___|  /\____/|__|  \___  > ____|
        \/    \/                 \/\/"""
slash = '=' * 20 + '<>' + '=' * 20


def clear_all() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    # для адапатации под разные ос


def start_bunner() -> None:
    clear_all()
    print(f'{slash}\n{rise}\n{slash}')
