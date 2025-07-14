import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from transactions_db import TransactionsDB
from database_manager import DatabaseManager
from wallets_db import WalletsDB
from currencies_db import CurrenciesDB
from tags_db import TagsDB

class TransactionsGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Añadir Gasto")
        self.geometry("500x600")

        self.db = TransactionsDB(DatabaseManager())
        self.wallets_db = WalletsDB(DatabaseManager())
        self.currencies_db = CurrenciesDB(DatabaseManager())
        self.tags_db = TagsDB(DatabaseManager())

        self.wallets = self.wallets_db.list(include_inactive=False)
        self.wallet_name_to_id = {w[1]: w[0] for w in self.wallets if 'originator' not in w[2]}
        #self.wallet_info = {w[1]: {"id": w[0], "currency": w[2]} for w in self.wallets}

        self.currencies = self.currencies_db.list()
        self.currency_name_to_id = {cur[2]: cur[0] for cur in self.currencies}

        self.tags = self.tags_db.list()
        self.tags = [tag for tag in self.tags if tag[3] == 'Expense']
        #print(self.tags)
        self.tags_name_to_id = {cur[2]: cur[0] for cur in self.tags}

        self.build_form()
        self.build_listbox()
        self.refresh_transactions()
        

    def build_form(self):
        ttk.Label(self, text="Fecha (YYYY-MM-DD)").pack()
        self.date_entry = ttk.Entry(self)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.pack(pady=5)

        #ttk.Label(self, text="Tipo").pack()
        #self.type_var = tk.StringVar()
        #self.type_combo = ttk.Combobox(self, textvariable=self.type_var, values=["Ingreso", "Pago"])
        #self.type_combo.pack(pady=5)

        ttk.Label(self, text = 'Moneda').pack()
        self.currency_var = tk.StringVar()
        self.currency_combo = ttk.Combobox(self, textvariable= self.currency_var, values = list(self.currency_name_to_id.keys()), state='readonly')
        #self.currency_combo = ttk.Combobox(self, textvariable= self.currency_var, state='readonly')
        #self.currency_combo['values'] = [] # Lo mantengo vacío para que se complete automáticamente
        self.currency_combo.pack(pady=5)

        #ttk.Label(self, text="Moneda").pack()
        #self.currency_entry = ttk.Entry(self)
        #self.currency_entry.pack(pady=5)

        ttk.Label(self, text="Valor").pack()
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack(pady=5)

        ttk.Label(self, text="Fuente").pack()
        self.source_entry = ttk.Entry(self)
        self.source_entry.pack(pady=5)

        ttk.Label(self, text="Etiqueta (Tag)").pack()
        self.tag_var = tk.StringVar()
        self.tag_combo = ttk.Combobox(self, textvariable = self.tag_var, values = list(self.tags_name_to_id.keys()))
        self.tag_combo.pack(pady=5)

        ttk.Label(self, text="Wallet").pack()
        self.wallet_var = tk.StringVar()
        self.wallets_combo = ttk.Combobox(self, textvariable=self.wallet_var)
        self.wallets_combo['values'] = list(self.wallet_name_to_id.keys())
        self.wallets_combo.pack(pady=5)

        ttk.Label(self, text="Comentario").pack()
        self.comment_entry = ttk.Entry(self)
        self.comment_entry.pack(pady=5)

        ttk.Button(self, text="Guardar", command=self.save_transaction).pack(pady=10)

    def build_listbox(self):
        ttk.Label(self, text="Historial de Transacciones").pack(pady=5)
        self.transactions_listbox = tk.Listbox(self, width=70)
        self.transactions_listbox.pack(pady=10)

    def refresh_transactions(self):
        self.transactions_listbox.delete(0, tk.END)
        query = "SELECT id, date, type, amount, tag FROM transactions ORDER BY date DESC"
        try:
            rows = self.db.list_all_simplified()
            for row in rows:
                display = f"{row[1]} - {row[2]}: {row[3]} ({row[4]}) [ID {row[0]}]"
                self.transactions_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial:\n{e}")

    def save_transaction(self):
        try:
            wallet_name = self.wallet_var.get()
            wallet_id = self.wallet_name_to_id.get(wallet_name)

            if wallet_id is None:
                messagebox.showwarning("Wallet no seleccionada", "Por favor selecciona una wallet válida.")
                return

            data = (
                self.date_entry.get(),
                "Payment",
                self.currency_name_to_id.get(self.currency_combo.get()),
                self.amount_entry.get(),
                self.source_entry.get(),
                self.tags_name_to_id.get(self.tag_combo.get()),
                wallet_id,
                None,
                self.comment_entry.get()
            )

            self.db.add(*data)
            messagebox.showinfo("Éxito", "Transacción guardada")
            self.refresh_transactions()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la transacción: {e}")

    def clear_fields(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.currency_combo.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.source_entry.delete(0, tk.END)
        self.tag_combo.delete(0, tk.END)
        self.wallets_combo.set("")
        self.comment_entry.delete(0, tk.END)