from .base_frame import BaseFrame
from customtkinter import CTkLabel, CTkFrame


class BalanceFrame(BaseFrame):
    """Фрейм для отображения баланса"""

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self.title_label = CTkLabel(
            self,
            text="Финансовый обзор",
            font=("Arial", 18, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.stats_frame = CTkFrame(self)
        self.stats_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        for i in range(3):
            self.stats_frame.grid_columnconfigure(i, weight=1)

        self.balance_label = CTkLabel(self.stats_frame, text="Баланс: --", font=("Arial", 16))
        self.balance_label.grid(row=0, column=0, padx=20, pady=10)

        self.income_label = CTkLabel(self.stats_frame, text="Доходы: --", font=("Arial", 14), text_color="green")
        self.income_label.grid(row=0, column=1, padx=20, pady=10)

        self.expense_label = CTkLabel(self.stats_frame, text="Расходы: --", font=("Arial", 14), text_color="red")
        self.expense_label.grid(row=0, column=2, padx=20, pady=10)

    def update_balance(self, balance: float, income: float, expense: float):
        self.balance_label.configure(text=f"Баланс: {balance:,.2f} ₽")
        self.income_label.configure(text=f"Доходы: {income:,.2f} ₽")
        self.expense_label.configure(text=f"Расходы: {expense:,.2f} ₽")
