import sqlite3


class DatabaseManager:
    def __init__(self, db_name = 'budget_manager.db'):
        self.db_name = db_name

    def _connect(self):
        return sqlite3.connect(self.db_name)
    
    def execute(self, query, params = (), commit = False):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            return cursor

    # To execute multiple queries at once. I've not use it yet
    #def executemany(self, query, param_list, commit = False):
    #    with self._connect() as conn:
    #        cursor = conn.cursor()
    #        cursor.executemany(query, param_list)
    #        if commit:
    #            conn.commit()
    #        return cursor
    

