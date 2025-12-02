"""
Фрейм для быстрых действий
"""
import customtkinter as ctk
from .base_frame import BaseFrame


class QuickActionsFrame(BaseFrame):
    """Фрейм быстрых действий"""

    def __init__(self, parent, controller=None, on_quick_income=None, on_quick_expense=None,
                 on_report=None, on_search=None, **kwargs):
        self.on_quick_income = on_quick_income
        self.on_quick_expense = on_quick_expense
        self.on_report = on_report
        super().__init__(parent, controller=controller, **kwargs)

    def setup_ui(self):
        """Настройка интерфейса"""
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Быстрые кнопки
        actions = [
            ("💰 Быстрый доход", self.on_quick_income, "green"),
            ("💸 Быстрый расход", self.on_quick_expense, "red"),
            ("📊 Отчет", self.on_report, "blue")
        ]

        for i, (text, command, color) in enumerate(actions):
            btn = ctk.CTkButton(
                self,
                text=text,
                command=command if command else lambda: None,
                height=40,
                fg_color=color,
                hover_color=self._darken_color(color)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

    def _darken_color(self, color_name: str) -> str:
        """Затемнение цвета для эффекта hover"""
        colors = {
            "green": "#2E7D32",
            "red": "#C62828",
            "blue": "#1565C0",
            "orange": "#EF6C00"
        }
        return colors.get(color_name, "#1F538D")

    def update_data(self):
        """Обновление данных"""
        pass
