import tkinter as tk
from tkinter import ttk
from wallets_gui import WalletsGui
from transactions_gui import TransactionsGui
from transfers_gui import TransfersGui
from currencies_gui import CurrenciesGui
from tags_gui import TagsGui
from income_gui import IncomeGui
from expenses_gui import ExpenseGui
from payment_credit_gui import PaymentCreditGui

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MiBudget - Inicio")

        #window size - multiplatform
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")
        #self.root.geometry("300x200")

        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Menú Principal", font=("Helvetica", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Gestionar Wallets", command=self.open_wallets_window).pack(pady=10)
        ttk.Button(self.frame, text="Añadir Pago", command=self.open_transactions_window).pack(pady=10)
        ttk.Button(self.frame, text="Añadir Transferencia", command=self.open_transfers_window).pack(pady=10)
        ttk.Button(self.frame, text="Gestionar monedas", command=self.open_currencies_window).pack(pady=10)
        ttk.Button(self.frame, text="Gestionar Etiquetas", command=self.open_tags_window).pack(pady=10)
        ttk.Button(self.frame, text="Gestionar Ingresos", command=self.open_income_window).pack(pady=10)
        ttk.Button(self.frame, text="Gestionar Gastos", command=self.open_expense_window).pack(pady=10)
        ttk.Button(self.frame, text="Gestionar pago credito", command=self.open_payment_credit_window).pack(pady=10)

    def open_wallets_window(self):
        #new_window = tk.Toplevel(self.root)
        WalletsGui(self.root)

    def open_transactions_window(self):
        TransactionsGui(self.root)

    def open_transfers_window(self):
        TransfersGui(self.root)

    def open_currencies_window(self):
        CurrenciesGui(self.root)

    def open_tags_window(self):
        TagsGui(self.root)

    def open_income_window(self):
        IncomeGui(self.root)

    def open_expense_window(self):
        ExpenseGui(self.root)

    def open_payment_credit_window(self):
        PaymentCreditGui(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
