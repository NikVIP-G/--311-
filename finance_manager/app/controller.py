"""
Контроллер для управления данными и обновлением UI
"""
from typing import Callable, List, Any
import threading


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

    def get_categories(self) -> List[str]:
        """Получение категорий"""
        if hasattr(self._db, 'categories'):
            return self._db.categories
        return []

    def save_categories(self, categories: List[str]):
        """Сохранение категорий"""
        if hasattr(self._db, 'save_categories'):
            self._db.save_categories(categories)
            self.notify_update()

    def get_budgets(self) -> List[Any]:
        """Получение бюджетов"""
        if hasattr(self._db, 'budgets'):
            return self._db.budgets
        return []

    def save_budgets(self, budgets: List[Any]):
        """Сохранение бюджетов"""
        if hasattr(self._db, 'budgets') and hasattr(self._db, 'save_budgets'):
            self._db.budgets = budgets
            self._db.save_budgets()
            self.notify_update()

    def get_settings(self) -> Any:
        """Получение настроек"""
        if hasattr(self._db, 'settings'):
            return self._db.settings
        return None

    def save_settings(self, settings):
        """Сохранение настроек"""
        if hasattr(self._db, 'settings') and hasattr(self._db, 'save_settings'):
            self._db.settings = settings
            self._db.save_settings()
            self.notify_update()