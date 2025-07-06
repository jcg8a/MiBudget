import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager
from currencies_db import CurrenciesDB

class CurrenciesGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestor de monedas")
        self.geometry('500x600')

        self.db = CurrenciesDB(DatabaseManager())

        self.build_form()
        self.build_listbox()
        self.update_currencies()

    def build_form(self):
        ttk.Label(self, text="Nombre moneda").pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        ttk.Label(self, text="ISO moneda").pack()
        self.currency_entry = ttk.Entry(self)
        self.currency_entry.pack(pady=5)

        ttk.Label(self, text="País").pack()
        self.country_entry = ttk.Entry(self)
        self.country_entry.pack(pady=5)

        ttk.Button(self, text="Agregar moneda", command=self.save_currency).pack(pady=10)
        #ttk.Button(self.frame, text="Desactivar moneda", command=self.deactivate_currency).pack(pady=10)

    def build_listbox(self):
        ttk.Label(self, text="Monedas").pack(pady=5)
        self.currencies_listbox = tk.Listbox(self, width=70)
        self.currencies_listbox.pack(pady=10)

    def update_currencies(self):
        self.currencies_listbox.delete(0, tk.END)
        try:
            rows = self.db.list()
            for row in rows:
                display = f"{row[1]} - {row[2]}: {row[3]} [ID {row[0]}]"
                self.currencies_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial:\n{e}")

    def save_currency(self):
        try:
            data = (self.name_entry.get(),
                    self.currency_entry.get(),
                    self.country_entry.get())
            self.db.add(*data)

            messagebox.showinfo("Éxito", "Moneda guardada")
            self.update_currencies()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la moneda: {e}")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.currency_entry.delete(0, tk.END)
        self.country_entry.delete(0, tk.END)
