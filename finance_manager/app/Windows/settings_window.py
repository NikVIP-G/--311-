from typing import Dict
import customtkinter as ctk
from tkinter.messagebox import showinfo, showerror

from .base_window import BaseWindow


class SettingsWindow(BaseWindow):
    """Окно настроек приложения"""

    def __init__(self, parent, current_settings: Dict, on_save_settings=None):
        super().__init__(parent, "Настройки", 500, 400)
        self.current_settings = current_settings
        self.on_save_settings = on_save_settings
        self.setup_settings_ui()

    def setup_settings_ui(self):
        """Настройка интерфейса настроек"""
        # Прокручиваемый контейнер
        canvas = ctk.CTkCanvas(self.main_frame)
        scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Настройки
        row = 0

        # Внешний вид
        ctk.CTkLabel(scrollable_frame, text="Внешний вид",
                     font=("Arial", 14, "bold")).grid(row=row, column=0, padx=10, pady=(15, 5), sticky="w")
        row += 1

        ctk.CTkLabel(scrollable_frame, text="Тема:").grid(row=row, column=0, padx=20, pady=5, sticky="w")
        self.theme_var = ctk.StringVar(value=self.current_settings.get('theme', 'dark'))
        theme_combo = ctk.CTkComboBox(scrollable_frame,
                                      values=["dark", "light", "system"],
                                      variable=self.theme_var,
                                      width=150)
        theme_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        ctk.CTkLabel(scrollable_frame, text="Цветовая схема:").grid(row=row, column=0, padx=20, pady=5, sticky="w")
        self.color_var = ctk.StringVar(value=self.current_settings.get('color_theme', 'blue'))
        color_combo = ctk.CTkComboBox(scrollable_frame,
                                      values=["blue", "green", "dark-blue"],
                                      variable=self.color_var,
                                      width=150)
        color_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Настройки данных
        ctk.CTkLabel(scrollable_frame, text="Данные",
                     font=("Arial", 14, "bold")).grid(row=row, column=0, padx=10, pady=(15, 5), sticky="w")
        row += 1

        ctk.CTkLabel(scrollable_frame, text="Валюта:").grid(row=row, column=0, padx=20, pady=5, sticky="w")
        self.currency_var = ctk.StringVar(value=self.current_settings.get('currency', '₽'))
        currency_combo = ctk.CTkComboBox(scrollable_frame,
                                         values=["₽", "$", "€", "£"],
                                         variable=self.currency_var,
                                         width=150)
        currency_combo.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        ctk.CTkLabel(scrollable_frame, text="Автосохранение:").grid(row=row, column=0, padx=20, pady=5, sticky="w")
        self.autosave_var = ctk.BooleanVar(value=self.current_settings.get('autosave', True))
        autosave_check = ctk.CTkCheckBox(scrollable_frame, text="Включено",
                                         variable=self.autosave_var)
        autosave_check.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1

        ctk.CTkLabel(scrollable_frame, text="Интервал автосохранения (мин):").grid(row=row, column=0, padx=20, pady=5,
                                                                                   sticky="w")
        self.save_interval_var = ctk.StringVar(value=str(self.current_settings.get('save_interval', 5)))
        interval_entry = ctk.CTkEntry(scrollable_frame,
                                      textvariable=self.save_interval_var,
                                      width=150)
        interval_entry.grid(row=row, column=1, padx=10, pady=5)
        row += 1

        # Кнопки
        button_frame = ctk.CTkFrame(scrollable_frame)
        button_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        ctk.CTkButton(button_frame, text="💾 Сохранить",
                      command=self.save_settings).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="↩️ Сброс",
                      command=self.reset_settings).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="❌ Закрыть",
                      command=self.destroy).pack(side="left", padx=10)

    def save_settings(self):
        """Сохранение настроек"""
        try:
            settings = {
                'theme': self.theme_var.get(),
                'color_theme': self.color_var.get(),
                'currency': self.currency_var.get(),
                'autosave': self.autosave_var.get(),
                'save_interval': int(self.save_interval_var.get())
            }

            if self.on_save_settings:
                self.on_save_settings(settings)

            showinfo("Успех", "Настройки сохранены!")

        except ValueError:
            showerror("Ошибка", "Введите корректный интервал автосохранения")

    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        self.theme_var.set("dark")
        self.color_var.set("blue")
        self.currency_var.set("₽")
        self.autosave_var.set(True)
        self.save_interval_var.set("5")
