"""
Фрейм для отображения баланса
"""
import customtkinter as ctk
from datetime import datetime
from .base_frame import BaseFrame

class BalanceFrame(BaseFrame):
    """Фрейм баланса"""

    def __init__(self, parent, controller=None, **kwargs):
        # Передаем контроллер в родительский конструктор
        super().__init__(parent, controller=controller, **kwargs)

    def setup_ui(self):
        # Основной контейнер
        self.grid_columnconfigure(0, weight=1)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Финансовый обзор",
            font=("Arial", 18, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Фрейм с показателями
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Настройка колонок
        for i in range(3):
            self.stats_frame.grid_columnconfigure(i, weight=1)

        # Показатели
        self.balance_label = ctk.CTkLabel(
            self.stats_frame,
            text="Баланс: --",
            font=("Arial", 16)
        )
        self.balance_label.grid(row=0, column=0, padx=20, pady=10)

        self.income_label = ctk.CTkLabel(
            self.stats_frame,
            text="Доходы: --",
            font=("Arial", 14),
            text_color="green"
        )
        self.income_label.grid(row=0, column=1, padx=20, pady=10)

        self.expense_label = ctk.CTkLabel(
            self.stats_frame,
            text="Расходы: --",
            font=("Arial", 14),
            text_color="red"
        )
        self.expense_label.grid(row=0, column=2, padx=20, pady=10)

    def update_data(self):
        """Обновление показателей баланса"""
        if not self.db:
            return

        try:
            # Расчет баланса
            balance = self._calculate_balance()
            monthly_income = self._calculate_monthly_income()
            monthly_expense = self._calculate_monthly_expense()

            # Обновление меток
            self.balance_label.configure(text=f"Баланс: {balance:,.2f} ₽".replace(",", " "))
            self.income_label.configure(text=f"Доходы: {monthly_income:,.2f} ₽".replace(",", " "))
            self.expense_label.configure(text=f"Расходы: {monthly_expense:,.2f} ₽".replace(",", " "))
        except Exception as e:
            print(f"Ошибка обновления баланса: {e}")

    def _calculate_balance(self) -> float:
        """Расчет общего баланса"""
        if not self.db:
            return 0.0

        income = 0.0
        expense = 0.0

        for transaction in self.db.transactions:
            if transaction.type == 'income':
                income += transaction.amount
            else:
                expense += transaction.amount

        return income - expense

    def _calculate_monthly_income(self) -> float:
        """Расчет доходов за текущий месяц"""
        if not self.db:
            return 0.0

        current_month = datetime.now().month
        current_year = datetime.now().year
        income = 0.0

        for transaction in self.db.transactions:
            try:
                date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
                if date.month == current_month and date.year == current_year:
                    if transaction.type == 'income':
                        income += transaction.amount
            except ValueError:
                continue

        return income

    def _calculate_monthly_expense(self) -> float:
        """Расчет расходов за текущий месяц"""
        if not self.db:
            return 0.0

        current_month = datetime.now().month
        current_year = datetime.now().year
        expense = 0.0

        for transaction in self.db.transactions:
            try:
                date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
                if date.month == current_month and date.year == current_year:
                    if transaction.type == 'expense':
                        expense += transaction.amount
            except ValueError:
                continue

        return expense
