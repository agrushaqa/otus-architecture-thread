import sqlite3

from features.steps.src.mysql import create_table


class MysqlDbCreate:
    def __init__(self, db_name, request, exception=""):
        self.db_name = db_name
        self.cmd = request

    def execute(self):
        self.conn = sqlite3.connect(self.db_name, isolation_level=None)
        self.db_cursor = self.conn.cursor()
        create_table(self.conn, self.cmd)
        self.conn.close()
