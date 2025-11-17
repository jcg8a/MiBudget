
class ExpenseDB:
    def __init__(self, db_manager):
        self.db = db_manager
        self._create_table()

    def _create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        expense_id INTEGER,
                        date DATE NOT NULL,
                        wallet_id INTEGER NOT NULL,
                        currency_id INTEGER NOT NULL,
                        amount REAL NOT NULL,
                        interest_rate REAL DEFAULT 0,
                        total_installment INTEGER NOT NULL,
                        installment_number INTEGER NOT NULL,
                        amount_installment REAL NOT NULL,
                        source TEXT NOT NULL,
                        tag_id INTEGER NOT NULL,
                        comment TEXT,
                        payment_id INTEGER,
                        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (wallet_id) REFERENCES wallets(id),
                        FOREIGN KEY (currency_id) REFERENCES currencies(id),
                        FOREIGN KEY (tag_id) REFERENCES tags(id),
                        FOREIGN KEY (payment_id) REFERENCES transactions(id)
                        )''')
        
    def get_next_expense_id(self):
        #row = self.db.fetchone("SELECT MAX(expense_id) FROM expenses")
        row = self.db.execute("SELECT MAX(expense_id) FROM expenses", commit = False).fetchone()
        return(row[0] or 0) + 1
        #self.db.execute('''CREATE TABLE IF NOT EXISTS expenses (
        #                id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                date DATE NOT NULL,
        #                wallet_id INTEGER NOT NULL,
        #                currency_id INTEGER NOT NULL,
        #                amount REAL NOT NULL,
        #                interest_rate REAL DEFAULT 0,
        #                number_installment INTEGER NOT NULL,
        #                source TEXT NOT NULL,
        #                tag_id INTEGER NOT NULL
        #                comment TEXT,
        #                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        #                date_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        #                FOREIGN KEY (wallet_id) REFERENCES wallets(id),
        #                FOREIGN KEY (currency_id) REFERENCES currencies(id),
        #                FOREIGN KEY (tag_id) REFERENCES tags(id)
        #                )''')
        #
        #self.db.execute('''CREATE TABLE IF NOT EXISTS installments (
        #                id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                expense_id INTEGER NOT NULL,
        #                installment_number INTEGER NOT NULL,
        #                amount REAL NOT NULL,
        #                payment_id INTEGER,
        #                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        #                date_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        #                FOREIGN KEY (expense_id) REFERENCES expenses(id),
        #                FOREIGN KEY (payment_id) REFERENCES transactions(id))''')
        
    def add(self, *, date, wallet_id, currency_id, amount, interest_rate = 0.0, total_installment, source, tag_id, comment):
        expense_id = self.get_next_expense_id()
        amount_installment = round(amount/total_installment, 8)
        for i in range(1, total_installment + 1):
            self.db.execute('''INSERT INTO expenses (
                            expense_id, 
                            date,
                            wallet_id,
                            currency_id,
                            amount, 
                            total_installment,
                            installment_number,
                            amount_installment,
                            interest_rate,
                            source,
                            tag_id, 
                            comment)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (expense_id, date, wallet_id, currency_id, amount, total_installment, i, amount_installment, interest_rate, source, tag_id, comment), 
                            commit = True)
        
    def add_payment(self, payment_id, wallet_credit_id, start_date, end_date):
        #Busca las cuotas sin pagar en fechas anteriores a la fecha de cierre
        rows = self.db.execute('''SELECT * FROM expenses
                               WHERE payment_id IS NULL
                               AND date <= ?
                               AND wallet_id = ?
                               ORDER BY date ASC''', (end_date, wallet_credit_id), commit = False).fetchall()
        print(rows)
        #agrupa las cuotas por expense_id
        grouped = {}
        for row in rows:
            expense_id = row[1]
            grouped.setdefault(expense_id, []).append(row)

        applied_count = 0

        for expense_id, installments in grouped.items():
            date_expense=installments[0][2] #la fecha de la compra. Para todas las coutas la fecha de compra es la misma, asi que tomo la de la primera cuota

            installments.sort(key = lambda r:r[8]) #ordena por número de cuota

            if start_date <= date_expense <= end_date:
                for inst in installments:
                    if inst[13] is None: #payment_id es vacio
                        self.mark_expense_paid(inst[0], payment_id)
                        applied_count += 1
                        break
            elif date_expense < start_date:
                for inst in installments:
                    if inst[13] is None:
                        self.mark_expense_paid(inst[0], payment_id)
                        applied_count += 1
                        break
        return applied_count
    
    def mark_expense_paid(self, expense_row_id, payment_id):
        self.db.execute('''UPDATE expenses SET payment_id = ? WHERE id = ?''',
                        (payment_id, expense_row_id),
                        commit =True)
        
        
    def get_unpaid_expenses(self, wallet_id, start_date, end_date):
        query = """WITH first_unpaid AS (
            SELECT expense_id,
            MIN(id) AS min_id
            FROM expenses
            WHERE wallet_id = :wallet_id
            AND payment_id IS NULL
            GROUP BY expense_id
            )

            SELECT e.id,
            e.expense_id,
            e.date,
            e.installment_number,
            e.amount_installment,
            e."source",
            e.tag_id,
            e.comment,
            fu.min_id,

            CASE 
            	WHEN fu.min_id = e.id AND e.date BETWEEN :start_date AND :end_date THEN 'current'
            	WHEN fu.min_id = e.id AND e.date < :start_date THEN 'older'
            	ELSE 'remaining'
            END AS category
            FROM expenses e
            LEFT JOIN first_unpaid fu ON fu.expense_id = e.expense_id
            WHERE e.wallet_id = :wallet_id
            AND e.payment_id IS NULL
            ORDER BY e.date ASC
        """
        
        params = {"start_date": start_date,
                  "end_date": end_date,
                  "wallet_id": wallet_id}
        
        rows = self.db.execute(query, params, commit = False).fetchall()

        result = {"current": [],
                  "older": [],
                  "remaining": []}

        for r in rows:
            category = r[-1]
            result[category].append(r)

        return result
