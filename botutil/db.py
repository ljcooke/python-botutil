import sqlite3


class DB(object):

    def __init__(self, filename, autocommit=False):
        super(DB, self).__init__()

        self.conn = sqlite3.connect(filename)

        if not autocommit:
            self.conn.isolation_level = None

    def cursor(self):
        return self.conn.cursor()

    def __del__(self):
        self.conn.close()
