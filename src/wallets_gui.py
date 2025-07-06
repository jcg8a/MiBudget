import tkinter as tk
from tkinter import ttk, messagebox
from wallets_db import WalletsDB
from database_manager import DatabaseManager
from currencies_db import CurrenciesDB

class WalletsGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Billeteras")
        self.geometry("500x400")

        self.db = WalletsDB(DatabaseManager())
        #self.selected_wallet_id = None
        #cargar la base de currencies:
        self.currencies_db = CurrenciesDB(DatabaseManager())
        self.currencies = self.currencies_db.list()
        self.currencies_name_to_id = {cur[2]: cur[0] for cur in self.currencies}

        #self.frame = ttk.Frame(self, padding=10)
        #self.frame.pack(fill="both", expand=True)

        self.build_form()
        self.build_listbox()
        self.update_wallets()

    def build_form(self):
        ttk.Label(self, text="Nombre billetera").pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        ttk.Label(self, text="Tipo").pack()
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self, textvariable=self.type_var, values=["Debit", "Credit"])
        self.type_combo.pack(pady=5)

        ttk.Label(self, text="Alias").pack()
        self.alias_entry = ttk.Entry(self)
        self.alias_entry.pack(pady=5)

        ttk.Label(self, text="Entidad financiera").pack()
        self.fi_entry = ttk.Entry(self)
        self.fi_entry.pack(pady=5)

        ttk.Label(self, text="Pais").pack()
        self.country_entry = ttk.Entry(self)
        self.country_entry.pack(pady=5)

        ttk.Label(self, text="Moneda").pack()
        self.currency_var = tk.StringVar()
        self.currency_combo = ttk.Combobox(self, textvariable=self.currency_var, values=list(self.currencies_name_to_id.keys()), state='readonly')
        self.currency_combo.pack(pady=5)

        ttk.Button(self, text="Agregar billetera", command=self.save_wallet).pack(pady=10)

    def build_listbox(self):
        ttk.Label(self, text="Billeteras").pack(pady=5)
        self.wallets_listbox = tk.Listbox(self, width=70)
        self.wallets_listbox.pack(pady=10)

    def update_wallets(self):
        self.wallets_listbox.delete(0, tk.END)
        try:
            rows = self.db.list()
            for row in rows:
                display = f"({row[2]}) {row[3]}: {row[4]} - {row[5]} - currency: {row[6]} [ID: {row[0]}: {row[1]}]"
                self.wallets_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial:\n{e}")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.alias_entry.delete(0, tk.END)
        self.fi_entry.delete(0, tk.END)
        self.country_entry.delete(0, tk.END)

    def save_wallet(self):
        try:
            data =(self.name_entry.get().strip(),
                self.type_combo.get(),
                self.alias_entry.get().strip(),
                self.fi_entry.get().strip(),
                self.country_entry.get().strip(),
                self.currencies_name_to_id.get(self.currency_combo.get())   
           )
            #print(data)
            if all(data):
                self.db.add(*data)
                messagebox.showinfo("Éxito", "Billetera guardada")
                self.update_wallets()
                self.clear_fields()
            else:
                messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
        except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la billetera: {e}")
              

        # Formulario de entrada
        #labels = ['Nombre', 'Tipo', 'Alias', 'Banco', 'País', 'Moneda']
        #self.entries = {}
#
        #for i, label in enumerate(labels):
        #    ttk.Label(self.frame, text=label).grid(row=i, column=0, sticky='e')
        #    entry = ttk.Entry(self.frame)
        #    entry.grid(row=i, column=1, padx=5, pady=2)
        #    self.entries[label.lower()] = entry

#        ttk.Button(self.frame, text="Agregar Wallet", command=self.save_wallet).grid(row=len(labels), column=0, columnspan=2, pady=10)
#        ttk.Button(self.frame, text="Actualizar", command=self.update_wallet).grid(row=6, column=1, pady=10)
#        ttk.Button(self.frame, text="Eliminar", command=self.delete_wallet).grid(row=7, column=0, columnspan=2, pady=5)
#
#        self.wallets_listbox = tk.Listbox(self.frame, width=60)
#        self.wallets_listbox.grid(row=8, column=0, columnspan=2)
#        self.wallets_listbox.bind('<<ListboxSelect>>', self.on_wallet_select)
#
#        # Checkbox para incluir inactivas
#        self.include_inactive_var = tk.BooleanVar()
#        self.include_inactive_checkbox = ttk.Checkbutton(
#        self.frame, text="Mostrar inactivas",
#        variable=self.include_inactive_var,
#        command=self.refresh_wallets
#        )
#        self.include_inactive_checkbox.grid(row=9, column=0, columnspan=2, pady=5)
#
#        # Botón para reactivar
#        ttk.Button(self.frame, text="Reactivar", command=self.reactivate_wallet).grid(row=10, column=0, columnspan=2, pady=5)
#
#    def save_wallet(self):
#        values = [self.entries[field].get() for field in ['nombre', 'tipo', 'alias', 'banco', 'país', 'moneda']]
#        if all(values):
#            self.db.add(*values)
#            self.refresh_wallets()
#            self.clear_fields()
#        else:
#            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
#
#    def update_wallet(self):
#        if self.selected_wallet_id is None:
#            messagebox.showwarning("Selección requerida", "Primero selecciona una wallet.")
#            return
#        
#        values = {k: self.entries[k].get() for k in self.entries}
#        self.db.update(
#            self.selected_wallet_id,
#            name=values['nombre'],
#            type=values['tipo'],
#            alias=values['alias'],
#            bank=values['banco'],
#            country=values['país'],
#            currency=values['moneda']
#        )
#        self.refresh_wallets()
#        self.clear_fields()
#
#    def delete_wallet(self):
#        if self.selected_wallet_id is None:
#            messagebox.showwarning("Selección requerida", "Primero selecciona una wallet.")
#            return
#
#        confirm = messagebox.askyesno("Confirmar eliminación", "¿Deseas eliminar (desactivar) esta wallet?")
#        if confirm:
#            self.db.deactivate(self.selected_wallet_id)
#            self.refresh_wallets()
#            self.clear_fields()
#
#    def on_wallet_select(self, event):
#        selection = self.wallets_listbox.curselection()
#        if selection:
#            index = selection[0]
#            wallet = self.wallets_data[index]
#            self.selected_wallet_id = wallet[0]
#    
#            fields = ['name', 'type', 'alias', 'bank', 'country', 'currency']
#            for key, value in zip(fields, wallet[1:7]):
#                self.entries[key].delete(0, tk.END)
#                self.entries[key].insert(0, str(value))
#
#
#    def refresh_wallets(self):
#        self.wallets_listbox.delete(0, tk.END)
#        include_inactive = self.include_inactive_var.get()
#        wallets = self.db.list(include_inactive=include_inactive)
#        self.wallets_data = wallets  # Guardamos para usarlo en selección
#    
#        for w in wallets:
#            estado = "🟢" if w[7] else "🔴"
#            self.wallets_listbox.insert(tk.END, f"{estado} {w[0]} - {w[1]} ({w[2]})")
#
#    def clear_fields(self):
#        self.selected_wallet_id = None
#        for entry in self.entries.values():
#            entry.delete(0, tk.END)
#
#
#    def reactivate_wallet(self):
#        if self.selected_wallet_id is None:
#            messagebox.showwarning("Selección requerida", "Primero selecciona una wallet.")
#            return
#
#        self.db.update(self.selected_wallet_id, is_active=1)
#        self.refresh_wallets()
#        self.clear_fields()