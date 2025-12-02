"""
Контроллер для управления данными и обновлением UI
"""
from typing import Callable, List
import threading
from .models import Category


class AppController:
    """Контроллер приложения"""

    def __init__(self, database):
        self._db = database
        self._update_callbacks = []
        self._lock = threading.Lock()

    def add_update_callback(self, callback: Callable):
        """Добавление callback для обновления UI"""
        with self._lock:
            self._update_callbacks.append(callback)

    def remove_update_callback(self, callback: Callable):
        """Удаление callback"""
        with self._lock:
            if callback in self._update_callbacks:
                self._update_callbacks.remove(callback)

    def notify_update(self):
        """Уведомление всех подписчиков об обновлении"""
        with self._lock:
            callbacks = self._update_callbacks.copy()

        for callback in callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Ошибка в callback обновления: {e}")

    @property
    def db(self):
        """Получение базы данных"""
        return self._db

    def get_database(self):
        """Получение базы данных (совместимость)"""
        return self._db

    def get_categories(self) -> List[str]:
        """Получение всех категорий (для совместимости)"""
        return [cat.name for cat in self._db.categories]

    def get_income_categories(self) -> List[str]:
        """Получение категорий доходов"""
        return self._db.get_income_categories()

    def get_expense_categories(self) -> List[str]:
        """Получение категорий расходов"""
        return self._db.get_expense_categories()

    def get_categories_by_type(self, category_type: str) -> List[str]:
        """Получение категорий по типу"""
        return self._db.get_categories_by_type(category_type)

    def get_category_objects(self) -> List[Category]:
        """Получение объектов категорий"""
        return self._db.categories

    def save_category_objects(self, categories: List[Category]):
        """Сохранение объектов категорий"""
        if hasattr(self._db, 'save_categories'):
            self._db.save_categories(categories)
            self.notify_update()

    def add_transaction(self, transaction):
        """Добавление транзакции"""
        try:
            self._db.add_transaction(transaction)
            self.notify_update()
        except Exception as e:
            print(f"Ошибка добавления транзакции: {e}")
            raise

    def delete_transaction(self, transaction_id):
        """Удаление транзакции"""
        try:
            self._db.delete_transaction(transaction_id)
            self.notify_update()
        except Exception as e:
            print(f"Ошибка удаления транзакции: {e}")
            raise

    def update_transaction(self, transaction):
        """Обновление транзакции"""
        try:
            self._db.update_transaction(transaction)
            self.notify_update()
        except Exception as e:
            print(f"Ошибка обновления транзакции: {e}")
            raise
