from datetime import datetime

class WalletsDB:
    def __init__(self, db_manager):
        self.db = db_manager
        self._create_table()

    def _create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS wallets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        type TEXT NOT NULL,
                        alias TEXT NOT NULL,
                        bank TEXT NOT NULL,
                        country TEXT,
                        currency INTEGER NOT NULL,
                        is_active INTEGER DEFAULT 1,
                        date_create DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_update DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_deactivate DATETIME DEFAULT NULL,
                        FOREIGN KEY (currency) REFERENCES currencies(id))''', commit = True)
                
    def add(self, name, type, alias, bank, country, currency):
        self.db.execute('''
                        INSERT INTO wallets (name, type, alias, bank, country, currency)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                        (name, type, alias, bank, country, currency), 
                        commit =  True)
        
    def list(self, include_inactive = False):
        query = 'SELECT * FROM wallets'
        if not include_inactive:
            query += ' WHERE is_active = 1'

        return self.db.execute(query).fetchall()
    
    def deactivate(self, wallet_id):
        self.db.execute('''
                        UPDATE wallets
                        SET is_active = 0, date_deactivate = ?
                        WHERE id = ?''',
                        (datetime.now(), wallet_id),
                        commit = True)
        
    def update(self, wallet_id, name = None, type = None, alias = None, bank = None, country = None, currency = None, is_active=None):
        fields = []
        params = []

        if name:
            fields.append('name = ?')
            params.append(name)

        if type:
            fields.append('type = ?')
            params.append(type)

        if alias:
            fields.append('alias = ?')
            params.append(alias)

        if bank:
            fields.append('bank = ?')
            params.append(bank)

        if country:
            fields.append('country = ?')
            params.append(country)

        if currency:
            fields.append('currency = ?')
            params.append(currency)

        if is_active is not None:
            fields.append("is_active = ?")
            params.append(is_active)
            if is_active == 1:
                fields.append("date_deactivate = ?")
                params.append(None)

        if not fields:
            return

        fields.append('date_update = ?')
        params.append(datetime.now())
        params.append(wallet_id)

        query = f'''
        UPDATE wallets
        SET {', '.join(fields)}
        WHERE id = ?
        '''

        self.db.execute(query, params, commit = True)