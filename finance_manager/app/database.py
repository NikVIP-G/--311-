"""
Работа с данными приложения
"""
import json
import os
from dataclasses import asdict
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from models import Transaction, Budget, Settings, TransactionType


class Database:
    """Класс для работы с данными"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Используем домашнюю директорию пользователя
            home_dir = os.path.expanduser("~")
            self.data_dir = os.path.join(home_dir, ".personal_finance_manager")
        else:
            self.data_dir = data_dir

        # Создаем директории если не существуют
        os.makedirs(self.data_dir, exist_ok=True)

        # Файлы данных
        self.transactions_file = os.path.join(self.data_dir, "transactions.json")
        self.budgets_file = os.path.join(self.data_dir, "budgets.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        self.categories_file = os.path.join(self.data_dir, "categories.json")

        # Загружаем данные
        self.transactions: List[Transaction] = self._load_transactions()
        self.budgets: List[Budget] = self._load_budgets()
        self.settings: Settings = self._load_settings()
        self.categories: List[str] = self._load_categories()

    def _load_transactions(self) -> List[Transaction]:
        """Загрузка транзакций из файла"""
        if os.path.exists(self.transactions_file):
            try:
                with open(self.transactions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Transaction.from_dict(t) for t in data]
            except (json.JSONDecodeError, IOError):
                print("Ошибка загрузки транзакций, создаем новый файл")

        return []

    def _load_budgets(self) -> List[Budget]:
        """Загрузка бюджетов из файла"""
        if os.path.exists(self.budgets_file):
            try:
                with open(self.budgets_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Budget(**b) for b in data]
            except (json.JSONDecodeError, IOError):
                print("Ошибка загрузки бюджетов, создаем новый файл")

        return []

    def _load_settings(self) -> Settings:
        """Загрузка настроек из файла"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return Settings.from_dict(data)
            except (json.JSONDecodeError, IOError):
                print("Ошибка загрузки настроек, используем по умолчанию")

        return Settings()

    def _load_categories(self) -> List[str]:
        """Загрузка категорий из файла"""
        if os.path.exists(self.categories_file):
            try:
                with open(self.categories_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print("Ошибка загрузки категорий, создаем новый файл")

        # Категории по умолчанию
        default_categories = [
            # Доходы
            "Зарплата", "Фриланс", "Инвестиции", "Подарки", "Возврат",
            # Расходы
            "Продукты", "Кафе и рестораны", "Транспорт", "Жилье", "Коммуналка",
            "Развлечения", "Здоровье", "Образование", "Одежда", "Техника",
            "Подарки", "Путешествия", "Налоги", "Страхование", "Прочее"
        ]
        self.save_categories(default_categories)
        return default_categories

    def save_all(self):
        """Сохранение всех данных"""
        self.save_transactions()
        self.save_budgets()
        self.save_settings()
        self.save_categories()

    def save_transactions(self):
        """Сохранение транзакций"""
        try:
            data = [t.to_dict() for t in self.transactions]
            with open(self.transactions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения транзакций: {e}")

    def save_budgets(self):
        """Сохранение бюджетов"""
        try:
            data = [asdict(b) for b in self.budgets]
            with open(self.budgets_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения бюджетов: {e}")

    def save_settings(self):
        """Сохранение настроек"""
        try:
            data = self.settings.to_dict()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения настроек: {e}")

    def save_categories(self, categories: List[str] = None):
        """Сохранение категорий"""
        if categories is not None:
            self.categories = categories

        try:
            with open(self.categories_file, 'w', encoding='utf-8') as f:
                json.dump(self.categories, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения категорий: {e}")

    # Методы работы с транзакциями
    def add_transaction(self, transaction: Transaction):
        """Добавление новой транзакции"""
        self.transactions.append(transaction)
        self.save_transactions()

    def delete_transaction(self, transaction_id: str):
        """Удаление транзакции по ID"""
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        self.save_transactions()

    def update_transaction(self, transaction: Transaction):
        """Обновление транзакции"""
        for i, t in enumerate(self.transactions):
            if t.id == transaction.id:
                self.transactions[i] = transaction
                break
        self.save_transactions()

    def get_transactions(self, limit: int = None) -> List[Transaction]:
        """Получение транзакций (последние first)"""
        transactions = sorted(
            self.transactions,
            key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )

        if limit:
            transactions = transactions[:limit]

        return transactions

    def get_monthly_summary(self, year: int = None, month: int = None) -> Dict:
        """Сводка за месяц"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        income = 0.0
        expense = 0.0

        for transaction in self.transactions:
            try:
                trans_date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
                if trans_date.year == year and trans_date.month == month:
                    if transaction.type == TransactionType.INCOME.value:
                        income += transaction.amount
                    else:
                        expense += transaction.amount
            except ValueError:
                continue

        return {
            'income': income,
            'expense': expense,
            'balance': income - expense,
            'year': year,
            'month': month
        }

    def get_expenses_by_category(self) -> Dict[str, float]:
        """Расходы по категориям"""
        expenses = {}
        for transaction in self.transactions:
            if transaction.type == TransactionType.EXPENSE.value:
                category = transaction.category
                expenses[category] = expenses.get(category, 0) + transaction.amount
        return expenses

    def get_balance_history(self, days: int = 30) -> List[float]:
        """История баланса за N дней"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Группируем по дням
        daily_balance = {}

        for transaction in self.transactions:
            try:
                trans_date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
                if start_date <= trans_date <= end_date:
                    date_key = trans_date.strftime("%Y-%m-%d")
                    if transaction.type == TransactionType.INCOME.value:
                        daily_balance[date_key] = daily_balance.get(date_key, 0) + transaction.amount
                    else:
                        daily_balance[date_key] = daily_balance.get(date_key, 0) - transaction.amount
            except ValueError:
                continue

        # Создаем последовательность дней
        balance_history = []
        current_balance = 0

        for i in range(days):
            date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            current_balance += daily_balance.get(date, 0)
            balance_history.append(current_balance)

        return list(reversed(balance_history))  # От старых к новым