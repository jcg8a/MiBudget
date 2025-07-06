class TransfersDB:
    def __init__(self, db_manager):
        self.db = db_manager
        self._create_table()

    def _create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS transfers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATETIME NOT NULL,
                        from_wallet_id INTEGER NOT NULL,
                        to_wallet_id INTEGER NOT NULL,
                        from_currency_id INTEGER NOT NULL,
                        to_currency_id INTEGER NOT NULL,
                        from_amount REAL NOT NULL,
                        to_amount REAL NOT NULL,
                        rate REAL DEFAULT 1,
                        comment TEXT,
                        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (from_wallet_id) REFERENCES wallets(id),
                        FOREIGN KEY (to_wallet_id) REFERENCES wallets(id),
                        FOREIGN KEY (from_currency_id) REFERENCES currencies(id),
                        FOREIGN KEY (to_currency_id) REFERENCES currencies(id))''')
        
        self.db.execute('''CREATE TABLE IF NOT EXISTS transfer_fees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        transfer_id INTEGER NOT NULL,
                        date DATETIME NOT NULL,
                        description TEXT NOT NULL,
                        currency_id INTEGER NOT NULL,
                        amount REAL NOT NULL,
                        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (transfer_id) REFERENCES transfers(id),
                        FOREIGN KEY (currency_id) REFERENCES currencies(id))''')
        
    def add(self, date, from_wallet_id, to_wallet_id, from_currency, to_currency, from_amount, to_amount, rate, comment, fees=[]):
        cursor = self.db.execute('''INSERT INTO transfers (
                        date, from_wallet_id, to_wallet_id, from_currency_id, to_currency_id, from_amount, to_amount, rate, comment)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (date, from_wallet_id, to_wallet_id, from_currency, to_currency, from_amount, to_amount, rate, comment), commit = True)
        
        transfer_id = cursor.lastrowid
        
        for fee in fees:
            self.add_fee(transfer_id, fee['date'], fee['description'], fee['currency_id'], fee['amount'])

        return transfer_id
    
    def add_fee(self, transfer_id, date, description, currency_id, amount):
        self.db.execute('''INSERT INTO transfer_fees (
                        transfer_id, date, description, currency_id, amount)
                        VALUES (?, ?, ?, ?, ?)''', (transfer_id, date, description, currency_id, amount), commit = True)
        
    #def get_fee_for_transfer(self, transfer_id):
    #    self.db.execute('''SELECT description, currency_id, amount FROM transfer_fees WHERE transfer_id = ?''', (transfer_id), commit = False)