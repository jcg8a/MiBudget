from datetime import datetime

class TransactionsDB:
    def __init__(self, db_manager):
        self.db = db_manager
        self._create_table()

    def _create_table(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATETIME NOT NULL,
                type TEXT NOT NULL,
                currency_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                source TEXT,
                tag_id INTEGER NOT NULL,
                wallet_id INTEGER NOT NULL,
                wallet_credit_id INTEGER,
                comment TEXT,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (wallet_id) REFERENCES wallets(id),
                FOREIGN KEY (currency_id) REFERENCES currencies(id),
                FOREIGN KEY (tag_id) REFERENCES tags(id),
                FOREIGN KEY (wallet_credit_id) REFERENCES wallets(id)
            )
        ''', commit=True)

    def add(self, date, type, currency, amount, source, tag, wallet_id, wallet_credit_id, comment=''):
        """
        Agrega una transacción a la base de datos.

        Parámetros:
        - date (str): Fecha en formato 'YYYY-MM-DD'
        - type (str): Tipo de transacción (ej. 'income', 'expense', etc.)
        - currency (int): ID de la moneda
        - amount (float): Monto de la transacción
        - source (str): Fuente de la transacción (opcional)
        - tag (int): ID del tag
        - wallet_id (int): ID de la billetera
        - wallet_credit_id (int|None): ID de la billetera de crédito (opcional)
        - comment (str|None): Comentario adicional (opcional)
        """

        cursor = self.db.execute('''
            INSERT INTO transactions (
                date, type, currency_id, amount, source, tag_id, wallet_id, wallet_credit_id, comment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, type, currency, amount, source, tag, wallet_id, wallet_credit_id, comment), commit=True)
        return cursor

    def list(self, wallet_id=None):
        if wallet_id:
            return self.db.execute(
                'SELECT * FROM transactions WHERE wallet_id = ? ORDER BY date DESC',
                (wallet_id,)
            ).fetchall()
        return self.db.execute(
            'SELECT * FROM transactions ORDER BY date DESC'
        ).fetchall()

    #def update(self, transaction_id, **kwargs):
    #    fields = []
    #    params = []

    #    for key, value in kwargs.items():
    #        fields.append(f"{key} = ?")
    #        params.append(value)

    #    if not fields:
    #        return

    #    fields.append("date_updated = ?")
    #    params.append(datetime.now())
    #    params.append(transaction_id)

    #    query = f'''
    #        UPDATE transactions
    #        SET {', '.join(fields)}
    #        WHERE id = ?
    #    '''
    #    self.db.execute(query, params, commit=True)

    #def delete(self, transaction_id):
    #    self.db.execute(
    #        'DELETE FROM transactions WHERE id = ?',
    #        (transaction_id,),
    #        commit=True
    #    )

    def list_all_simplified(self):
        return self.db.execute(
            "SELECT id, date, type, amount, tag_id FROM transactions ORDER BY date DESC"
        ).fetchall()