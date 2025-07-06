import tkinter as tk
from tkinter import ttk, messagebox
from transactions_db import TransactionsDB
from database_manager import DatabaseManager
from currencies_db import CurrenciesDB
from wallets_db import WalletsDB
from tags_db import TagsDB

class IncomeGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestionar ingresos")
        self.geometry("500x400")

        self.db = TransactionsDB(DatabaseManager())
        self.currencies_db = CurrenciesDB(DatabaseManager())
        self.wallets_db = WalletsDB(DatabaseManager())
        self.tags_db = TagsDB(DatabaseManager())

        self.currencies = self.currencies_db.list()
        self.currencies_name_to_id = {cur[2]: cur[0] for cur in self.currencies}

        self.wallets = self.wallets_db.list()
        # self.wallets_name_to_id = {cur[2]: cur[0] for cur in self.currencies}

        self.tags = self.tags_db.list()
        self.tags = [tag for tag in self.tags if tag[3] == 'Income']
        print(self.tags)
        self.tags_name_to_id = {cur[2]: cur[0] for cur in self.tags}

        self.originator_id = None
        self.build_form()
        self.build_listbox()

    def build_form(self):
        ttk.Label(self, text = "Moneda").pack()
        self.currency_var = tk.StringVar()
        self.currency_combo = ttk.Combobox(self, textvariable =self.currency_var, values = list(self.currencies_name_to_id.keys()), state='readonly')
        self.currency_combo.pack(pady=5)

        ttk.Label(self, text = "Billetera (originador)").pack()
        self.originator_var = tk.StringVar()
        self.originator_label = ttk.Label(self, textvariable = self.originator_var)
        self.originator_label.pack(pady=5)

        self.currency_combo.bind("<<ComboboxSelected>>", self.update_originator)
        #print(self.currency_combo)

        ttk.Label(self, text="Fecha (yyyy-mm-dd)").pack()
        self.date_entry = ttk.Entry(self)
        self.date_entry.pack(pady=5)

        ttk.Label(self, text="Monto").pack()
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack(pady=5)

        ttk.Label(self, text="Fuente").pack()
        self.source_entry = ttk.Entry(self)
        self.source_entry.pack(pady=5)

        ttk.Label(self, text="Etiqueta").pack()
        self.tag_var = tk.StringVar()
        self.tag_combo = ttk.Combobox(self, textvariable=self.tag_var, values=list(self.tags_name_to_id.keys()), state='readonly')
        self.tag_combo.pack(pady=5)

        ttk.Label(self, text="Comentarios").pack()
        self.comment_entry = ttk.Entry(self)
        self.comment_entry.pack(pady=5)

        ttk.Button(self, text="Agregar Ingreso", command=self.save_income).pack(pady=10)

    def build_listbox(self):
        ttk.Label(self, text="Ingresos").pack(pady=5)
        self.income_listbox = tk.Listbox(self, width=70)
        self.income_listbox.pack(pady=10)

    def update_income(self):
        self.income_listbox.delete(0, tk.END)
        try:
            rows = self.db.list()
            for row in rows:
                display = f"(Tag:{row[6]}) {row[5]}: {row[4]} - currency: {row[3]} - date {row[1]} [ID: {row[0]}]"
                self.income_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial:\n{e}")

    def save_income(self):
        try:
            date = self.date_entry.get().strip()
            type_val = "income"
            currency_id = self.currencies_name_to_id.get(self.currency_combo.get())
            amount = self.amount_entry.get()
            source = self.source_entry.get().strip()
            tag_id = self.tags_name_to_id.get(self.tag_var.get())
            wallet_id = self.originator_id
            wallet_credit_id = None # para wallet_credit_id
            comment = self.comment_entry.get().strip()   
           
            #print(data)
            required_fields = (date, type_val, currency_id, amount, tag_id, wallet_id)
            if all(required_fields):
                self.db.add(date=date, 
                            type=type_val,
                            currency = currency_id,
                            amount = amount,
                            source=source,
                            tag=tag_id,
                            wallet_id=wallet_id,
                            wallet_credit_id=wallet_credit_id,
                            comment=comment)
                messagebox.showinfo("Éxito", "Ingreso guardado")
                self.update_income()
                self.clear_fields()
            else:
                messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
        except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el ingreso: {e}")

    def update_originator(self, event = None):
        selected_currency = self.currency_var.get()
        self.originator_id = None
        print(selected_currency)
        currency_id = self.currencies_name_to_id.get(selected_currency)
        print(currency_id)

        if currency_id is None:
            self.originator_var.set("No disponible")
            return
        
        for wallet in self.wallets:
            if 'originator' in wallet[1].lower() and wallet[6] == currency_id: 
                self.originator_var.set(f"{wallet[3]} ({wallet[1]} - {wallet[6]})")
                self.originator_id = wallet[0]
                return
            
        self.originator_var.set("No encontrada")

    def clear_fields(self):
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.source_entry.delete(0, tk.END)
        self.comment_entry.delete(0, tk.END)

            

