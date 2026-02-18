import sqlite3
# from func import start_bunner


class folder_red:
    def __init__(self, connection: sqlite3.Connection):
        self.connnn = connection
        self.cur = self.connnn.cursor()
        pass
