from tkinter.messagebox import showinfo

from .base_window import BaseWindow
from typing import List
import customtkinter as ctk


class CategoriesWindow(BaseWindow):
    """Окно управления категориями"""

    def __init__(self, parent, categories: List[str], on_update_categories=None):
        super().__init__(parent, "Управление категориями", 500, 400)
        self.categories = categories
        self.on_update_categories = on_update_categories
        self.setup_categories_ui()

    def setup_categories_ui(self):
        """Настройка интерфейса управления категориями"""
        # Список категорий
        ctk.CTkLabel(self.main_frame, text="Текущие категории:",
                     font=("Arial", 14, "bold")).pack(pady=(10, 5))

        self.categories_listbox = ctk.CTkTextbox(self.main_frame, height=150)
        self.categories_listbox.pack(fill="x", padx=10, pady=5)

        # Обновление списка
        self.update_categories_list()

        # Форма добавления новой категории
        ctk.CTkLabel(self.main_frame, text="Добавить новую категорию:",
                     font=("Arial", 12, "bold")).pack(pady=(15, 5))

        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Название:").pack(side="left", padx=5)
        self.new_category_entry = ctk.CTkEntry(form_frame, width=200)
        self.new_category_entry.pack(side="left", padx=5)

        ctk.CTkLabel(form_frame, text="Тип:").pack(side="left", padx=5)
        self.category_type_combo = ctk.CTkComboBox(form_frame,
                                                   values=["Доход", "Расход"],
                                                   width=100)
        self.category_type_combo.pack(side="left", padx=5)

        # Кнопки управления
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="➕ Добавить",
                      command=self.add_category).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Удалить выбранную",
                      command=self.delete_selected).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="💾 Сохранить",
                      command=self.save_categories).pack(side="left", padx=5)

    def update_categories_list(self):
        """Обновление списка категорий"""
        self.categories_listbox.delete("1.0", "end")
        for category in sorted(self.categories):
            self.categories_listbox.insert("end", f"• {category}\n")

    def add_category(self):
        """Добавление новой категории"""
        new_category = self.new_category_entry.get().strip()
        if new_category:
            self.categories.append(new_category)
            self.update_categories_list()
            self.new_category_entry.delete(0, "end")

    def delete_selected(self):
        """Удаление выбранной категории"""
        # В реальном приложении здесь была бы логика выбора
        # Для простоты удаляем последнюю
        if self.categories:
            self.categories.pop()
            self.update_categories_list()

    def save_categories(self):
        """Сохранение категорий"""
        if self.on_update_categories:
            self.on_update_categories(self.categories)
        showinfo("Успех", "Категории сохранены!")
        self.destroy()
