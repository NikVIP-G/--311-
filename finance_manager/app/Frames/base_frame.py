"""
Базовый класс для всех фреймов
"""
import customtkinter as ctk


class BaseFrame(ctk.CTkFrame):
    """Базовый фрейм с общими методами"""

    def __init__(self, parent, controller=None, **kwargs):
        # Сохраняем контроллер отдельно
        self._controller = controller

        # Удаляем controller из kwargs, чтобы не передавать в родительский класс
        if 'controller' in kwargs:
            kwargs.pop('controller')

        super().__init__(parent, **kwargs)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Настройка UI (должен быть переопределен)"""
        raise NotImplementedError("Метод setup_ui должен быть реализован")

    @property
    def controller(self):
        """Геттер для контроллера"""
        return self._controller

    @controller.setter
    def controller(self, value):
        """Сеттер для контроллера"""
        self._controller = value

    @property
    def db(self):
        """Получение базы данных через контроллер"""
        if self._controller:
            return self._controller.get_database()
        return None

    def update_data(self):
        """Обновление данных (может быть переопределен)"""
        pass

    def refresh(self):
        """Обновление UI"""
        try:
            self.update_data()
        except Exception as e:
            print(f"Ошибка обновления данных во фрейме {self.__class__.__name__}: {e}")
