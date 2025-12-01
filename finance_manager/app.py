import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import json
import os
from typing import List, Dict
from dataclasses import asdict

from models import Transaction, Budget, TransactionType
from Frames import balance_frame, charts_frame, quick_actions_frame, transactions_frame
from Windows import add_transaction_window, analytics_window, budgets_window, categories_window, settings_window


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FinanceApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Personal Finance Manager")
        self.root.geometry("1400x800")

        # Настройки по умолчанию
        self.settings = {
            'theme': 'dark',
            'color_theme': 'blue',
            'currency': '₽',
            'autosave': True,
            'save_interval': 5
        }

        # Инициализация данных
        self.data_file = "finance_data.json"
        self.budgets_file = "budgets_data.json"
        self.categories_file = "categories_data.json"

        self.transactions: List[Transaction] = []
        self.budgets: List[Budget] = []
        self.categories: List[str] = []

        self.load_all_data()

        # Создание интерфейса
        self.create_interface()

        # Обработка изменения размера окна
        self.root.bind('<Configure>', self.on_window_resize)

    def create_interface(self):
        """Создание основного интерфейса"""
        # Главное меню
        self.create_menu()

        # Основной контейнер
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Сетка для адаптивности
        self.main_container.grid_rowconfigure(0, weight=0)  # Баланс
        self.main_container.grid_rowconfigure(1, weight=1)  # Основной контент
        self.main_container.grid_rowconfigure(2, weight=0)  # Быстрые действия
        self.main_container.grid_columnconfigure(0, weight=1)

        # Создание фреймов
        self.create_frames()

    def create_menu(self):
        """Создание главного меню"""
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(side="top", fill="x", padx=10, pady=5)

        menu_items = [
            ("➕ Добавить операцию", self.open_add_transaction),
            ("📊 Аналитика", self.open_analytics),
            ("🗂️ Категории", self.open_categories),
            ("💰 Бюджеты", self.open_budgets),
            ("⚙️ Настройки", self.open_settings),
            ("📤 Экспорт", self.export_data),
            ("ℹ️ О программе", self.show_about)
        ]

        for text, command in menu_items:
            btn = ctk.CTkButton(menu_frame, text=text, command=command,
                                width=120, height=30, corner_radius=10)
            btn.pack(side="left", padx=2)

    def create_frames(self):
        """Создание всех фреймов интерфейса"""
        # Фрейм баланса
        self.balance_frame = balance_frame.BalanceFrame(self.main_container)
        self.balance_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Основной контент (таблица + графики)
        content_frame = ctk.CTkFrame(self.main_container)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Настройка сетки для контента
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=2)  # Таблица
        content_frame.grid_columnconfigure(1, weight=1)  # Графики

        # Фрейм транзакций
        self.transactions_frame = transactions_frame.TransactionsFrame(
            content_frame,
            on_delete=self.delete_transaction,
            on_edit=self.edit_transaction
        )
        self.transactions_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        # Фрейм графиков
        self.charts_frame = charts_frame.ChartsFrame(content_frame)
        self.charts_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

        # Фрейм быстрых действий
        self.quick_actions_frame = quick_actions_frame.QuickActionsFrame(
            self.main_container,
            on_quick_income=self.quick_add_income,
            on_quick_expense=self.quick_add_expense,
            on_report=self.generate_report,
            on_search=self.open_search
        )
        self.quick_actions_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Первоначальное обновление UI
        self.update_ui()

    def load_all_data(self):
        """Загрузка всех данных"""
        # Загрузка транзакций
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.transactions = [Transaction(**t) for t in data]

        # Загрузка бюджетов
        if os.path.exists(self.budgets_file):
            with open(self.budgets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.budgets = [Budget(**b) for b in data]

        # Загрузка категорий
        if os.path.exists(self.categories_file):
            with open(self.categories_file, 'r', encoding='utf-8') as f:
                self.categories = json.load(f)

    def save_all_data(self):
        """Сохранение всех данных"""
        # Сохранение транзакций
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(t) for t in self.transactions], f, ensure_ascii=False, indent=2)

        # Сохранение бюджетов
        with open(self.budgets_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(b) for b in self.budgets], f, ensure_ascii=False, indent=2)

        # Сохранение категорий
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(self.categories, f, ensure_ascii=False, indent=2)

    def update_ui(self):
        """Обновление всего интерфейса"""
        # Обновление баланса
        balance = self.calculate_balance()
        monthly_income = self.calculate_monthly_income()
        monthly_expense = self.calculate_monthly_expense()

        self.balance_frame.update_balance(balance, monthly_income, monthly_expense)

        # Обновление таблицы транзакций
        self.transactions_frame.update_transactions(self.transactions)

        # Обновление графиков
        expenses_by_category = self.get_expenses_by_category()
        monthly_income_data = self.get_monthly_income_data()
        balance_history = self.get_balance_history()

        self.charts_frame.update_expense_chart(expenses_by_category)
        self.charts_frame.update_income_chart(monthly_income_data)
        self.charts_frame.update_balance_chart(balance_history)

    # ==================== ОСНОВНЫЕ МЕТОДЫ ====================

    def calculate_balance(self) -> float:
        """Расчет общего баланса"""
        income = sum(t.amount for t in self.transactions if t.type == TransactionType.INCOME.value)
        expense = sum(t.amount for t in self.transactions if t.type == TransactionType.EXPENSE.value)
        return income - expense

    def calculate_monthly_income(self) -> float:
        """Расчет доходов за текущий месяц"""
        current_month = datetime.now().month
        current_year = datetime.now().year

        return sum(
            t.amount for t in self.transactions
            if t.type == TransactionType.INCOME.value and
            datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").month == current_month and
            datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").year == current_year
        )

    def calculate_monthly_expense(self) -> float:
        """Расчет расходов за текущий месяц"""
        current_month = datetime.now().month
        current_year = datetime.now().year

        return sum(
            t.amount for t in self.transactions
            if t.type == TransactionType.EXPENSE.value and
            datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").month == current_month and
            datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").year == current_year
        )

    def get_expenses_by_category(self) -> Dict[str, float]:
        """Получение расходов по категориям"""
        expenses = {}
        for transaction in self.transactions:
            if transaction.type == TransactionType.EXPENSE.value:
                expenses[transaction.category] = expenses.get(transaction.category, 0) + transaction.amount
        return expenses

    def get_monthly_income_data(self) -> Dict[str, float]:
        """Получение доходов по месяцам"""
        monthly_income = {}
        for transaction in self.transactions:
            if transaction.type == TransactionType.INCOME.value:
                date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
                month_key = date.strftime("%Y-%m")
                monthly_income[month_key] = monthly_income.get(month_key, 0) + transaction.amount
        return dict(sorted(monthly_income.items())[-6:])  # Последние 6 месяцев

    def get_balance_history(self) -> List[float]:
        """Получение истории баланса"""
        history = []
        balance = 0

        sorted_transactions = sorted(
            self.transactions,
            key=lambda t: datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S")
        )

        for transaction in sorted_transactions:
            if transaction.type == TransactionType.INCOME.value:
                balance += transaction.amount
            else:
                balance -= transaction.amount
            history.append(balance)

        return history[-30:]  # Последние 30 записей

    # ==================== ОБРАБОТЧИКИ СОБЫТИЙ ====================

    def open_add_transaction(self):
        """Открытие окна добавления транзакции"""
        window = add_transaction_window.AddTransactionWindow(self.root, self.add_transaction)
        window.transient(self.root)
        window.focus_force()

    def add_transaction(self, transaction: Transaction):
        """Добавление новой транзакции"""
        self.transactions.append(transaction)
        self.save_all_data()
        self.update_ui()

    def delete_transaction(self):
        """Удаление выбранной транзакции"""
        selected_idx = self.transactions_frame.get_selected_transaction()
        if selected_idx is not None:
            if messagebox.askyesno("Подтверждение", "Удалить выбранную операцию?"):
                # Преобразуем индекс (таблица показывает в обратном порядке)
                actual_idx = len(self.transactions) - selected_idx - 1
                if 0 <= actual_idx < len(self.transactions):
                    del self.transactions[actual_idx]
                    self.save_all_data()
                    self.update_ui()

    def edit_transaction(self):
        """Редактирование транзакции"""
        selected_idx = self.transactions_frame.get_selected_transaction()
        if selected_idx is not None:
            # В реальном приложении здесь открывалось бы окно редактирования
            messagebox.showinfo("Редактирование",
                                "Функция редактирования будет реализована в следующей версии")

    def open_analytics(self):
        """Открытие окна аналитики"""
        window = analytics_window.AnalyticsWindow(self.root, self.transactions)
        window.transient(self.root)

    def open_categories(self):
        """Открытие окна управления категориями"""
        window = categories_window.CategoriesWindow(
            self.root,
            self.categories,
            self.update_categories
        )
        window.transient(self.root)

    def update_categories(self, categories: List[str]):
        """Обновление списка категорий"""
        self.categories = categories
        self.save_all_data()

    def open_budgets(self):
        """Открытие окна управления бюджетами"""
        window = budgets_window.BudgetsWindow(
            self.root,
            self.budgets,
            self.update_budgets
        )
        window.transient(self.root)

    def update_budgets(self, budgets: List[Budget]):
        """Обновление бюджетов"""
        self.budgets = budgets
        self.save_all_data()

    def open_settings(self):
        """Открытие окна настроек"""
        window = settings_window.SettingsWindow(
            self.root,
            self.settings,
            self.update_settings
        )
        window.transient(self.root)

    def update_settings(self, settings: Dict):
        """Обновление настроек"""
        self.settings = settings

        # Применение темы
        ctk.set_appearance_mode(settings['theme'])
        ctk.set_default_color_theme(settings['color_theme'])

    def quick_add_income(self):
        """Быстрое добавление дохода"""
        self.quick_add(TransactionType.INCOME.value)

    def quick_add_expense(self):
        """Быстрое добавление расхода"""
        self.quick_add(TransactionType.EXPENSE.value)

    def quick_add(self, transaction_type: str):
        """Быстрое добавление транзакции"""
        dialog = ctk.CTkInputDialog(
            text=f"Введите сумму {'дохода' if transaction_type == TransactionType.INCOME.value else 'расхода'}:",
            title="Быстрое добавление"
        )

        amount = dialog.get_input()
        if amount:
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    raise ValueError

                transaction = Transaction(
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    type=transaction_type,
                    category="Быстрая операция",
                    amount=amount_float,
                    description="Быстрое добавление"
                )

                self.add_transaction(transaction)

            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму")

    def generate_report(self):
        """Генерация отчета"""
        try:
            df = pd.DataFrame([asdict(t) for t in self.transactions])
            df['date'] = pd.to_datetime(df['date'])

            filename = f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Все операции', index=False)

                # Сводка по месяцам
                monthly_summary = df.groupby([df['date'].dt.strftime('%Y-%m'), 'type'])['amount'].sum().unstack()
                monthly_summary.to_excel(writer, sheet_name='По месяцам')

                # По категориям
                category_summary = df.groupby(['category', 'type'])['amount'].sum().unstack()
                category_summary.to_excel(writer, sheet_name='По категориям')

            messagebox.showinfo("Успех", f"Отчет сохранен в файл: {filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")

    def open_search(self):
        """Открытие поиска"""
        # В реальном приложении здесь было бы окно поиска
        messagebox.showinfo("Поиск",
                            "Функция поиска будет реализована в следующей версии")

    def export_data(self):
        """Экспорт данных"""
        try:
            df = pd.DataFrame([asdict(t) for t in self.transactions])
            filename = f"finance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Экспорт", f"Данные экспортированы в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
        Personal Finance Manager v1.0

        Приложение для учета личных финансов:
        • Учет доходов и расходов
        • Категоризация операций
        • Управление бюджетами
        • Аналитика и отчеты
        • Визуализация данных

        Разработано с использованием:
        • CustomTkinter - для современного GUI
        • Matplotlib - для графиков
        • Pandas - для анализа данных

        © 2024 Все права защищены
        """

        messagebox.showinfo("О программе", about_text)

    def on_window_resize(self, event):
        """Обработка изменения размера окна"""
        # Адаптивная логика может быть добавлена здесь
        pass

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


# ==================== ТОЧКА ВХОДА ====================

if __name__ == "__main__":
    try:
        import matplotlib.pyplot as plt

        app = FinanceApp()
        app.run()

    except ImportError as e:
        print("Ошибка импорта библиотек. Установите необходимые зависимости:")
        print("pip install customtkinter pandas matplotlib openpyxl")
        print(f"Детали ошибки: {e}")
    except Exception as e:
        print(f"Произошла ошибка при запуске приложения: {e}")