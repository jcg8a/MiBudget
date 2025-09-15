import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from wallets_db import WalletsDB
from currencies_db import CurrenciesDB
from transactions_db import TransactionsDB
from database_manager import DatabaseManager
from tags_db import TagsDB
from expenses_db import ExpenseDB

class PaymentCreditGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Registrar Pago de Tarjeta")
        self.geometry("400x500")

        self.db = TransactionsDB(DatabaseManager())
        self.wallets_db = WalletsDB(DatabaseManager())
        self.currencies_db = CurrenciesDB(DatabaseManager())
        self.tags_db = TagsDB(DatabaseManager())
        self.expenses_db = ExpenseDB(DatabaseManager())

        self.wallets = self.wallets_db.list()
        self.wallets_credit = [credit for credit in self.wallets if credit[2] == 'Credit']
        self.currencies = self.currencies_db.list()
        self.tags = self.tags_db.list()
        self.tags = [tag for tag in self.tags if tag[3] == 'Credit']
        print(self.tags)

        self.wallet_name_to_id = {w[1]: w[0] for w in self.wallets}
        self.currency_name_to_id = {c[2]: c[0] for c in self.currencies}
        self.tags_name_to_id = {c[2]: c[0] for c in self.tags}
        self.wallet_credit_name_to_id = {w[1]: w[0] for w in self.wallets_credit}
        
        self.build_form()

    def build_form(self):
        ttk.Label(self, text="Fecha del Pago (YYYY-MM-DD)").pack()
        self.date_entry = ttk.Entry(self)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.pack(pady=5)

        ttk.Label(self, text="Billetera de pago").pack()
        self.wallet_var = tk.StringVar()
        self.wallet_combo = ttk.Combobox(self, textvariable=self.wallet_var, values=list(self.wallet_name_to_id.keys()), state='readonly')
        self.wallet_combo.pack(pady=5)

        ttk.Label(self, text="Tarjeta crédito a pagar").pack()
        self.wallet_credit_var = tk.StringVar()
        self.wallet_credit_combo = ttk.Combobox(self, textvariable=self.wallet_credit_var, values=list(self.wallet_credit_name_to_id.keys()), state='readonly')
        self.wallet_credit_combo.pack(pady=5)

        ttk.Label(self, text="Moneda").pack()
        self.currency_var = tk.StringVar()
        self.currency_combo = ttk.Combobox(self, textvariable=self.currency_var, values=list(self.currency_name_to_id.keys()), state='readonly')
        self.currency_combo.pack(pady=5)

        ttk.Label(self, text="Valor").pack()
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack(pady=5)

        ttk.Label(self, text="Fecha inicio del intervalo cubierto").pack()
        self.start_date_entry = ttk.Entry(self)
        self.start_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.start_date_entry.pack(pady=5)

        ttk.Label(self, text="Fecha fin del intervalo cubierto").pack()
        self.end_date_entry = ttk.Entry(self)
        self.end_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.end_date_entry.pack(pady=5)

        # Button to query expenses
        print("DEBUG: button for expenses")
        ttk.Button(self, text="Buscar gastos cubiertos", command=self.show_expenses).pack(pady=(8,6))

       #Treeview to show query results
        columns = ("id", "fecha", "monto", "descripción", "estado")
        self.expenses_tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        for col in columns:
            self.expenses_tree.heading(col, text=col.capitalize())
            self.expenses_tree.column(col, width=80, anchor="center")
            
        self.expenses_tree.pack(fill="both", expand=True, pady=5)

        ttk.Label(self, text="Descripción").pack()
        self.source_entry = ttk.Entry(self)
        self.source_entry.pack(pady=5)

        ttk.Label(self, text="Etiqueta").pack()
        self.tags_var = tk.StringVar()
        self.tags_combo = ttk.Combobox(self, textvariable=self.tags_var, values=list(self.tags_name_to_id.keys()), state='readonly')
        self.tags_combo.pack(pady=5)

        ttk.Label(self, text="Comentario").pack()
        self.comment_entry = ttk.Entry(self)
        self.comment_entry.pack(pady=5)

        ttk.Button(self, text="Guardar Pago", command=self.save_payment).pack(pady=10)

    def save_payment(self):
        try:
            date = self.date_entry.get()
            type_val = "Payment"
            currency_id = self.currency_name_to_id[self.currency_var.get()]
            amount = self.amount_entry.get()
            source = self.source_entry.get()
            tag_id = self.tags_name_to_id[self.tags_var.get()]
            wallet_id = self.wallet_name_to_id[self.wallet_var.get()]
            wallet_credit_id = self.wallet_name_to_id[self.wallet_credit_var.get()]
            comment = self.comment_entry.get() 
            
            cursor = self.db.add(date=date,
                                 type=type_val,
                                 currency=currency_id,
                                 amount=amount,
                                 source=source,
                                 tag=tag_id,
                                 wallet_id=wallet_id,
                                 wallet_credit_id=wallet_credit_id,
                                 comment=comment)
            
            transaction_id = cursor.lastrowid
            print(f'cursor: {transaction_id}')
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()

            self.expenses_db.add_payment(payment_id=transaction_id, wallet_credit_id=wallet_credit_id, start_date=start_date, end_date=end_date)
            
            

            #messagebox.showinfo("Éxito", f"Pago registrado. ID: {payment_id}")
            #self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el pago: {e}")

    def show_expenses(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        wallet_credit_id = self.wallet_credit_name_to_id.get(self.wallet_credit_var.get())

        # Clean table
        for row in self.expenses_tree.get_children():
            self.expenses_tree.delete(row)

        # Query expenses in the interval
        current_expenses = self.expenses_db.get_current_unpaid_expenses(wallet_credit_id, start_date, end_date)

        # Query older expenses
        older_expenses = self.expenses_db.get_oldest_unpaid_expenses(wallet_credit_id, start_date)

        # Show in the treeview
        for exp in current_expenses:
            self.expenses_tree.insert("", "end", values=(
                exp[0], #id
                exp[1], #expense_id
                exp[2], #date
                exp[3], #installment_number
                exp[4], #amount_installment
                exp[5], #source
                exp[6], #tag_id
                exp[7] #comment
            ))

        for exp in older_expenses:
            self.expenses_tree.insert("", "end", values=(
                                exp[0], #id
                exp[1], #expense_id
                exp[2], #date
                exp[3], #installment_number
                exp[4], #amount_installment
                exp[5], #source
                exp[6], #tag_id
                exp[7] #comment
            ), tags=("oldest",))

        self.expenses_tree.tag_configure("oldest", background="lightyellow")