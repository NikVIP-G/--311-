from customtkinter import CTkFrame


class BaseFrame(CTkFrame):
    """Базовый класс для всех фреймов"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса (должен быть переопределен)"""
        raise NotImplementedError
