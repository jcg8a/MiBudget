import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager
from tags_db import TagsDB

class TagsGui(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Etiquetas")
        self.geometry("500x400")

        self.db = TagsDB(DatabaseManager())

        self.build_form()
        self.build_listbox()
        self.update_tags()

    def build_form(self):
        ttk.Label(self, text="Nombre Etiqueta").pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        ttk.Label(self, text="Alias Etiqueta").pack()
        self.alias_entry = ttk.Entry(self)
        self.alias_entry.pack(pady=5)

        ttk.Label(self, text="Tipo").pack()
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self, textvariable=self.type_var, values=["Income", "Expense", "Credit"])
        self.type_combo.pack(pady=5)

        ttk.Button(self, text="Agregar Etiqueta", command=self.save_tag).pack(pady=10)

    def build_listbox(self):
        ttk.Label(self, text="Etiquetas").pack(pady=5)
        self.tags_listbox = tk.Listbox(self, width=70)
        self.tags_listbox.pack(pady=10)

    def update_tags(self):
        self.tags_listbox.delete(0, tk.END)
        try:
            rows = self.db.list()
            for row in rows:
                display = f"({row[3]}) {row[2]} [ID: {row[0]}: {row[1]}]"
                self.tags_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el historial:\n{e}")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.alias_entry.delete(0, tk.END)
        
    def save_tag(self):
        try:
            data = (
                self.name_entry.get().strip(),
                self.alias_entry.get().strip(),
                self.type_combo.get()
            )
            self.db.add(*data)
            self.update_tags()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Etiqueta guardada")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la etiqueta: {e}")
