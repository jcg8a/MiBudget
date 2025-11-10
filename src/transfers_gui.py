import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from wallets_db import WalletsDB
from database_manager import DatabaseManager
from transfers_db import TransfersDB
from currencies_db import CurrenciesDB

class TransfersGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Nueva Transferencia")
        self.geometry("500x600")

        self.db = TransfersDB(DatabaseManager())
        self.currencies_db = CurrenciesDB(DatabaseManager())
        self.wallets_db = WalletsDB(DatabaseManager())

        self.wallets = self.wallets_db.list(include_inactive=False)
        self.wallet_name_to_id = {w[3]: w[0] for w in self.wallets}

        self.currencies = self.currencies_db.list()
        self.currency_name_to_id = {cur[2]: cur[0] for cur in self.currencies}

        #self.fee_container = ttk.Frame(self)
        #self.fee_container.pack()

        self.fees = []
        self.fee_count = 0

        self.build_form()

    def build_form(self):
        ttk.Label(self, text="Fecha (YYYY-MM-DD)").pack()
        self.date_entry = ttk.Entry(self)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.pack(pady=5)

        ttk.Label(self, text="De Wallet").pack()
        self.from_wallet_var = tk.StringVar()
        self.from_wallet_combo = ttk.Combobox(self, textvariable=self.from_wallet_var, values=list(self.wallet_name_to_id.keys()), state='readonly')
        self.from_wallet_combo.pack(pady=5)

        ttk.Label(self, text="A Wallet").pack()
        self.to_wallet_var = tk.StringVar()
        self.to_wallet_combo = ttk.Combobox(self, textvariable=self.to_wallet_var, values=list(self.wallet_name_to_id.keys()), state='readonly')
        self.to_wallet_combo.pack(pady=5)

        ttk.Label(self, text="Moneda origen").pack()
        self.currency_out_var = tk.StringVar()
        self.currency_out_combo = ttk.Combobox(self, textvariable=self.currency_out_var, values=list(self.currency_name_to_id.keys()), state='readonly')
        self.currency_out_combo.pack(pady=5)
        #self.currency_out_entry = ttk.Entry(self)
        #self.currency_out_entry.pack(pady=5)

        ttk.Label(self, text="Monto enviado").pack()
        self.amount_out_entry = ttk.Entry(self)
        self.amount_out_entry.pack(pady=5)

        ttk.Label(self, text="Moneda destino").pack()
        self.currency_in_var = tk.StringVar()
        self.currency_in_combo = ttk.Combobox(self, textvariable=self.currency_in_var, values=list(self.currency_name_to_id.keys()), state='readonly')
        self.currency_in_combo.pack(pady=5)

        ttk.Label(self, text="Monto recibido").pack()
        self.amount_in_entry = ttk.Entry(self)
        self.amount_in_entry.pack(pady=5)

        ttk.Label(self, text="Tasa de Cambio (1 de origen equivale a ... de destino - 1 por defecto)").pack()
        self.rate_entry = ttk.Entry(self)
        self.rate_entry.insert(0, "1.0")
        self.rate_entry.pack(pady=5)

        ttk.Label(self, text="Comentario").pack()
        self.comment_entry = ttk.Entry(self)
        self.comment_entry.pack(pady=5)

        ttk.Label(self, text = 'Comisiones').pack(pady=(10,0))

        header_frame = ttk.Frame(self)
        header_frame.pack()

        ttk.Label(header_frame, text = 'Fecha (yyyy-mm-dd)').grid(row=0, column=0)
        ttk.Label(header_frame, text = 'descripcion').grid(row=0, column=1)
        ttk.Label(header_frame, text = 'Moneda').grid(row=0, column=2)
        ttk.Label(header_frame, text = 'Monto').grid(row=0, column=3)

        self.fee_container =ttk.Frame(self)
        self.fee_container.pack()

        self.add_fee_row()


        #ttk.Label(self, text="Comisiones").pack(pady=5)
        #self.fees_frame = ttk.Frame(self)
        #self.fees_frame.pack(pady=5)

        #self.add_fee_fields()

        ttk.Button(self, text="Agregar otra comisión", command=self.add_fee_row).pack(pady=5)

        # Botón guardar
        ttk.Button(self, text="Guardar Transferencia", command=self.save_transfer).pack(pady=10)

    def add_fee_row(self):
        row = self.fee_count
        date_fee = ttk.Entry(self.fee_container)
        description = ttk.Entry(self.fee_container)
        currency = ttk.Combobox(self.fee_container, values=list(self.currency_name_to_id.keys()), state='readonly')
        amount = ttk.Entry(self.fee_container)
        #wallet = ttk.Combobox(self.fee_container, values=self.wallet_names, state='readonly')

        date_fee.grid(row=row, column=0, padx=5, pady=2)
        description.grid(row=row, column=1, padx=5, pady=2)
        currency.grid(row=row, column=2, padx=5, pady=2)
        amount.grid(row=row, column=3, padx=5, pady=2)
        
        #wallet.grid(row=row, column=3, padx=5, pady=2)

        self.fees.append({"date_entry":date_fee,
                          "desc_entry": description, 
                          "curr_entry": currency, 
                          "amt_entry": amount})
        self.fee_count += 1

    def save_transfer(self):
        try:
            from_wallet_id = self.wallet_name_to_id.get(self.from_wallet_var.get())
            to_wallet_id = self.wallet_name_to_id.get(self.to_wallet_var.get())
            if from_wallet_id == to_wallet_id:
                messagebox.showerror("Error", "Las wallets de origen y destino deben ser diferentes.")
                return

            fees_data = []
            for fee in self.fees:
                date = fee['date_entry'].get().strip()
                desc = fee['desc_entry'].get().strip()
                curr = self.currency_name_to_id.get(fee["curr_entry"].get())
                amt = fee['amt_entry'].get().strip()
                if date and desc and curr and amt:
                    fees_data.append({"date": date, "description":desc, "currency_id":curr, "amount":amt})
            #for desc_entry, curr_entry, amt_entry in self.fees:
            #    desc = desc_entry.get().strip()
            #    curr = self.currency_name_to_id.get(curr_entry.get())
            #    amt = amt_entry.get().strip()
            #    if desc and curr and amt:
            #        fees_data.append({"description": desc, 'currency': curr, "amount": float(amt)})

            print(fees_data)
            self.db.add(
                date=self.date_entry.get(),
                from_wallet_id=from_wallet_id,
                to_wallet_id=to_wallet_id,
                from_currency = self.currency_name_to_id.get(self.currency_out_combo.get()),
                to_currency = self.currency_name_to_id.get(self.currency_in_combo.get()),
                from_amount = float(self.amount_out_entry.get()),
                to_amount = float(self.amount_in_entry.get()),
                #currency=self.currency_entry.get(),
                rate=float(self.rate_entry.get()),
                comment=self.comment_entry.get(),
                fees=fees_data
            )
            #print(fees_data)
            messagebox.showinfo("Éxito", "Transferencia guardada correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la transferencia: {e}")
            print(e)

