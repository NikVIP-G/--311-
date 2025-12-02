"""
Окно управления категориями
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import List

from ..Windows.base_window import BaseWindow
from ..models import Category, CategoryType


class CategoriesWindow(BaseWindow):
    """Окно управления категориями с разделением на доходы и расходы"""

    def __init__(self, parent, categories: List[Category], on_update_categories=None):
        super().__init__(parent, "Управление категориями", 600, 500)
        self.color_var = None
        self.category_type_combo = None
        self.category_type_var = None
        self.new_category_entry = None
        self.expense_listbox = None
        self.income_listbox = None
        self.expense_tab = None
        self.income_tab = None
        self.tabview = None
        self.categories = categories.copy() if categories else []
        self.on_update_categories = on_update_categories
        self.setup_categories_ui()

    def setup_categories_ui(self):
        """Настройка интерфейса управления категориями"""
        # Основной контейнер с вкладками
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Создание вкладок
        self.income_tab = self.tabview.add("💰 Доходы")
        self.expense_tab = self.tabview.add("💸 Расходы")

        # Настройка вкладок
        self.setup_income_tab()
        self.setup_expense_tab()

        # Форма добавления новой категории
        self.setup_add_category_form()

        # Кнопки управления
        self.setup_buttons()

    def setup_income_tab(self):
        """Настройка вкладки категорий доходов"""
        # Заголовок
        ctk.CTkLabel(
            self.income_tab,
            text="Категории доходов:",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))

        # Фрейм для списка категорий с прокруткой
        income_frame = ctk.CTkScrollableFrame(self.income_tab, height=200)
        income_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.income_listbox = ctk.CTkTextbox(income_frame, height=150, state="disabled")
        self.income_listbox.pack(fill="both", expand=True)

        self.update_income_list()

    def setup_expense_tab(self):
        """Настройка вкладки категорий расходов"""
        # Заголовок
        ctk.CTkLabel(
            self.expense_tab,
            text="Категории расходов:",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))

        # Фрейм для списка категорий с прокруткой
        expense_frame = ctk.CTkScrollableFrame(self.expense_tab, height=200)
        expense_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.expense_listbox = ctk.CTkTextbox(expense_frame, height=150, state="disabled")
        self.expense_listbox.pack(fill="both", expand=True)

        self.update_expense_list()

    def setup_add_category_form(self):
        """Настройка формы добавления категории"""
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="Добавить новую категорию:",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(5, 10), sticky="w")

        # Название категории
        ctk.CTkLabel(form_frame, text="Название:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.new_category_entry = ctk.CTkEntry(form_frame, width=200)
        self.new_category_entry.grid(row=1, column=1, padx=5, pady=5)

        # Тип категории
        ctk.CTkLabel(form_frame, text="Тип:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.category_type_var = ctk.StringVar(value="expense")
        self.category_type_combo = ctk.CTkComboBox(
            form_frame,
            variable=self.category_type_var,
            values=["Доход", "Расход"],
            width=100
        )
        self.category_type_combo.grid(row=1, column=3, padx=5, pady=5)

        # Цвет категории (опционально)
        ctk.CTkLabel(form_frame, text="Цвет:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.color_var = ctk.StringVar(value="#2196F3")
        color_combo = ctk.CTkComboBox(
            form_frame,
            variable=self.color_var,
            values=["#4CAF50", "#2196F3", "#FF9800", "#F44336", "#9C27B0", "#00BCD4", "#FFC107"],
            width=100
        )
        color_combo.grid(row=2, column=1, padx=5, pady=5)

    def setup_buttons(self):
        """Настройка кнопок управления"""
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="➕ Добавить",
            command=self.add_category,
            width=120
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🗑️ Удалить выбранную",
            command=self.delete_selected_category,
            width=150,
            fg_color="#dc3545",
            hover_color="#c82333"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="💾 Сохранить",
            command=self.save_categories,
            width=120,
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="❌ Закрыть",
            command=self.destroy,
            width=100
        ).pack(side="left", padx=5)

    def update_income_list(self):
        """Обновление списка категорий доходов"""
        self.income_listbox.configure(state="normal")
        self.income_listbox.delete("1.0", "end")

        income_categories = [cat for cat in self.categories if cat.type == CategoryType.INCOME]
        for category in sorted(income_categories, key=lambda x: x.name):
            color_display = f" ({category.color})" if category.color else ""
            self.income_listbox.insert("end", f"• {category.name}{color_display}\n")

        self.income_listbox.configure(state="disabled")

    def update_expense_list(self):
        """Обновление списка категорий расходов"""
        self.expense_listbox.configure(state="normal")
        self.expense_listbox.delete("1.0", "end")

        expense_categories = [cat for cat in self.categories if cat.type == CategoryType.EXPENSE]
        for category in sorted(expense_categories, key=lambda x: x.name):
            color_display = f" ({category.color})" if category.color else ""
            self.expense_listbox.insert("end", f"• {category.name}{color_display}\n")

        self.expense_listbox.configure(state="disabled")

    def update_categories_list(self):
        """Обновление всех списков категорий"""
        self.update_income_list()
        self.update_expense_list()

    def add_category(self):
        """Добавление новой категории"""
        name = self.new_category_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название категории")
            return

        # Проверяем, нет ли уже такой категории
        for existing in self.categories:
            if existing.name.lower() == name.lower():
                messagebox.showerror("Ошибка", f"Категория '{name}' уже существует")
                return

        # Определяем тип
        category_type = CategoryType.INCOME if self.category_type_var.get() == "Доход" else CategoryType.EXPENSE

        # Создаем новую категорию
        new_category = Category(
            name=name,
            type=category_type,
            color=self.color_var.get()
        )

        self.categories.append(new_category)
        self.update_categories_list()
        self.new_category_entry.delete(0, "end")

        messagebox.showinfo("Успех", f"Категория '{name}' добавлена")

    def delete_selected_category(self):
        """Удаление выбранной категории"""
        # В реальном приложении здесь была бы логика выбора категории
        # Для демонстрации удаляем последнюю добавленную
        if not self.categories:
            messagebox.showwarning("Внимание", "Нет категорий для удаления")
            return

        # Получаем активную вкладку
        current_tab = self.tabview.get()

        if current_tab == "💰 Доходы":
            income_cats = [cat for cat in self.categories if cat.type == CategoryType.INCOME]
            if income_cats:
                category_to_delete = income_cats[-1]
                if messagebox.askyesno("Подтверждение", f"Удалить категорию '{category_to_delete.name}'?"):
                    self.categories.remove(category_to_delete)
                    self.update_categories_list()
        else:
            expense_cats = [cat for cat in self.categories if cat.type == CategoryType.EXPENSE]
            if expense_cats:
                category_to_delete = expense_cats[-1]
                if messagebox.askyesno("Подтверждение", f"Удалить категорию '{category_to_delete.name}'?"):
                    self.categories.remove(category_to_delete)
                    self.update_categories_list()

    def save_categories(self):
        """Сохранение категорий"""
        if self.on_update_categories:
            self.on_update_categories(self.categories)
        messagebox.showinfo("Успех", "Категории сохранены!")
        self.destroy()
