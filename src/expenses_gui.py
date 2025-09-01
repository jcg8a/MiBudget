import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from expenses_db import ExpenseDB
from wallets_db import WalletsDB
from currencies_db import CurrenciesDB
from tags_db import TagsDB
from database_manager import DatabaseManager

class ExpenseGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Nuevo Gasto")
        self.geometry("400x500")

        self.db = ExpenseDB(DatabaseManager())
        self.wallets_db = WalletsDB(DatabaseManager())
        self.currencies_db = CurrenciesDB(DatabaseManager())
        self.tags_db = TagsDB(DatabaseManager())

        self.wallets = self.wallets_db.list()
        self.wallets = [w for w in self.wallets if w[2] == "Credit"]
        self.currencies = self.currencies_db.list()
        self.tags = self.tags_db.list()
        self.tags = [t for t in self.tags if t[3] == "Expense"]

        self.wallet_name_to_id = {w[3]: w[0] for w in self.wallets}
        self.currency_name_to_id = {c[2]: c[0] for c in self.currencies}  # Asume que c[2] es nombre
        self.tag_name_to_id = {t[2]: t[0] for t in self.tags}

        self.build_form()

    def build_form(self):
        ttk.Label(self, text="Fecha (YYYY-MM-DD)").pack()
        self.date_entry = ttk.Entry(self)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.pack(pady=5)

        ttk.Label(self, text="Billetera").pack()
        self.wallet_var = tk.StringVar()
        self.wallet_combo = ttk.Combobox(self, textvariable=self.wallet_var, values=list(self.wallet_name_to_id.keys()), state='readonly')
        self.wallet_combo.pack(pady=5)

        ttk.Label(self, text="Moneda").pack()
        self.currency_var = tk.StringVar()
        self.currency_combo = ttk.Combobox(self, textvariable=self.currency_var, values=list(self.currency_name_to_id.keys()), state='readonly')
        self.currency_combo.pack(pady=5)

        ttk.Label(self, text="Monto total").pack()
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack(pady=5)

        ttk.Label(self, text="Número de cuotas").pack()
        self.installments_entry = ttk.Entry(self)
        self.installments_entry.insert(0, "1")
        self.installments_entry.pack(pady=5)

        ttk.Label(self, text="Descripción").pack()
        self.source_entry = ttk.Entry(self)
        self.source_entry.pack(pady=5)

        ttk.Label(self, text="Etiqueta").pack()
        self.tag_var = tk.StringVar()
        self.tag_combo = ttk.Combobox(self, textvariable=self.tag_var, values=list(self.tag_name_to_id.keys()), state='readonly')
        self.tag_combo.pack(pady=5)

        ttk.Label(self, text="Comentario").pack()
        self.comment_entry = ttk.Entry(self)
        self.comment_entry.pack(pady=5)

        ttk.Label(self, text="Interés (%)").pack()
        self.interest_entry = ttk.Entry(self)
        self.interest_entry.insert(0, "0")
        self.interest_entry.pack(pady=5)

        ttk.Button(self, text="Guardar Gasto", command=self.save_expense).pack(pady=10)

    def save_expense(self):
        try:
            date = self.date_entry.get()
            wallet_id = self.wallet_name_to_id[self.wallet_var.get()]
            currency_id = self.currency_name_to_id[self.currency_var.get()]
            amount = float(self.amount_entry.get())
            total_installments = int(self.installments_entry.get())
            source = self.source_entry.get()
            tag_id = self.tag_name_to_id[self.tag_var.get()]
            comment = self.comment_entry.get()
            interest = float(self.interest_entry.get())

            self.db.add(
                date=date,
                wallet_id=wallet_id,
                currency_id=currency_id,
                amount=amount,
                total_installment = total_installments,
                source=source,
                tag_id=tag_id,
                comment=comment,
                interest_rate=interest
            )

            messagebox.showinfo("Éxito", "Gasto guardado correctamente.")
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el gasto: {e}")

    def clear_fields(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.wallet_combo.set("")
        self.currency_combo.set("")
        self.amount_entry.delete(0, tk.END)
        self.installments_entry.delete(0, tk.END)
        self.source_entry.delete(0, tk.END)
        self.tag_combo.set("")
        self.comment_entry.delete(0, tk.END)
        self.interest_entry.delete(0, tk.END)
        self.interest_entry.insert(0, "0")