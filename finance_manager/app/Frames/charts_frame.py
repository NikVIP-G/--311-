"""
Фрейм для отображения графиков
"""
import customtkinter as ctk
from .base_frame import BaseFrame


class ChartsFrame(BaseFrame):
    """Фрейм графиков"""

    def __init__(self, parent, controller=None, **kwargs):
        super().__init__(parent, controller=controller, **kwargs)

    def setup_ui(self):
        """Настройка интерфейса"""
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Визуализация данных",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=(10, 10))

        # Сообщение о том, что графики будут реализованы позже
        self.info_label = ctk.CTkLabel(
            self,
            text="Графики и диаграммы будут реализованы\nв следующей версии приложения",
            font=("Arial", 12),
            text_color="gray"
        )
        self.info_label.pack(pady=20)

    def update_data(self):
        """Обновление данных"""
        pass
