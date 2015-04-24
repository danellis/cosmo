import sqlite3

class Database(object):
    def __init__(self, db_filename, flush=False):
        self.db = sqlite3.connect(db_filename)
