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
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        ttk.Label(self.frame, text="Menú Principal", font=("Helvetica", 16)).pack(pady=10)

        # Buttons container
        menu_frame = ttk.Frame(self.frame, borderwidth=1)
        menu_frame.pack(side='left', fill='y', padx=(0,10))

        # Botones de ingresos y gastos
        actions_frame = ttk.Frame(menu_frame)
        actions_frame.pack(fill='x', pady=(10,5))
        ttk.Button(actions_frame, text="Pagos", command=self.open_transactions_window).pack(side='left', expand = True, fill='both', padx=5)
        ttk.Button(actions_frame, text="Gastos", command=self.open_expense_window).pack(side='left', expand = True, fill='both', padx=5)
        ttk.Button(actions_frame, text="Ingresos", command=self.open_income_window).pack(side='left', expand = True, fill='both', padx=5)

        movement_frame = ttk.Frame(menu_frame)
        movement_frame.pack(fill='x', pady=(5,10))
        ttk.Button(movement_frame, text="Credito", command=self.open_payment_credit_window).pack(side='left', expand = True, fill='both', padx=5)
        ttk.Button(movement_frame, text="Transferencias", command=self.open_transfers_window).pack(side='left', expand = True, fill='both', padx=5)

        manage_frame = ttk.Frame(menu_frame)
        manage_frame.pack(fill='x', pady=(5,10))
        ttk.Button(manage_frame, text="Monedas", command=self.open_currencies_window).pack(side='left', expand = True, fill='both', padx=5)
        ttk.Button(manage_frame, text="Wallets", command=self.open_wallets_window).pack(side='left', expand = True, fill='both', padx=5)
        ttk.Button(manage_frame, text="Etiquetas", command=self.open_tags_window).pack(side='left', expand = True, fill='both', padx=5)


        stats_frame = ttk.Frame(self.frame, borderwidth=1)
        stats_frame.pack(side='right', fill = 'both', expand=True)
        placeholder = tk.Label(stats_frame, text = 'Stats')
        placeholder.place(relx=0.5, rely=0.5, anchor="center")

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