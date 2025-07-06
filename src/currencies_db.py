from datetime import datetime
from wallets_db import WalletsDB

class CurrenciesDB:
    def __init__(self, db_manager):
        self.db = db_manager
        self.wallets_db = WalletsDB(db_manager)
        self._create_table()

    def _create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS currencies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        currency TEXT NOT NULL,
                        country TEXT NOT NULL,
                        date_create DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_deactivate DATETIME DEFAULT NULL)''', commit = True)
        #self.add(name='originator', currency='ori', country='originator')

        
    def add(self, name, currency, country):
        cursor = self.db.execute('''INSERT INTO currencies (name, currency, country)
                        VALUES (?, ?, ?)''',
                        (name, currency, country),
                        commit =True)
        # Me trae el id de la ultima moneda añadida
        #currency_id = self.db.execute('SELECT last_insert_rowid()').fetchone()
        currency_id = cursor.lastrowid
        #currency_id = new_currency[0]
        #currency_country = new_currency[2]
        self.wallets_db.add(name='originator' + "-" + currency,
                            type='originator' + "-" + currency,
                            alias='originator' + "-" + currency,
                            bank ='originator',
                            country=country,
                            currency=currency_id)
        
    def list(self):
        query = '''SELECT * FROM currencies'''
        return self.db.execute(query).fetchall()
    
    def deactivate(self, currency_id):
        self.db.execute('''UPDATE currencies
                        SET is_active = 0, date_deactivate = ?
                        WHERE id = ?''',
                        (datetime.now(), currency_id),
                        commit = True)