from datetime import datetime

class TagsDB:
    def __init__(self, db_manager):
        self.db = db_manager
        self._create_table()

    def _create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS tags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tag TEXT NOT NULL,
                        alias TEXT NOT NULL,
                        type TEXT NOT NULL,
                        is_active INTEGER DEFAULT 1,
                        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_deactivate DATETIME DEFAULT NULL)''',
                        commit = True)
        
        self.add(tag = "credit payment", alias='Pago tarjeta crédito', type ='Credit')
        
    def add(self, tag, alias, type):
        self.db.execute('''INSERT INTO tags (
                        tag, alias, type)
                        VALUES (?, ?, ?)''',
                        (tag, alias, type), 
                        commit = True)
        
    def list(self):
        query = '''SELECT * FROM tags'''
        return self.db.execute(query).fetchall()
    
    def deactivate(self, tag_id):
        self.db.execute('''UPDATE tags
                        SET is_active = 0, date_deactivate = ?
                        WHERE id = ?''',
                        (datetime.now(), tag_id),
                        commit = True)