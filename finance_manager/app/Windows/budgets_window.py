from typing import List
from tkinter.ttk import Treeview
from tkinter.messagebox import showerror, showinfo
import customtkinter as ctk

from .base_window import BaseWindow
from finance_manager.app.models import Budget


class BudgetsWindow(BaseWindow):
    """Окно управления бюджетами"""

    def __init__(self, parent, budgets: List[Budget], on_update_budgets=None):
        super().__init__(parent, "Управление бюджетами", 600, 500)
        self.budgets = budgets
        self.on_update_budgets = on_update_budgets
        self.setup_budgets_ui()

    def setup_budgets_ui(self):
        """Настройка интерфейса управления бюджетами"""
        # Таблица бюджетов
        columns = ("Категория", "Лимит (₽)", "Период", "Использовано", "Остаток")
        self.tree = Treeview(self.main_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Заполнение данными
        self.update_budgets_table()

        # Форма добавления бюджета
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)

        # Поля формы
        ctk.CTkLabel(form_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
        self.category_combo = ctk.CTkComboBox(form_frame, width=150)
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Лимит:").grid(row=0, column=2, padx=5, pady=5)
        self.limit_entry = ctk.CTkEntry(form_frame, width=100, placeholder_text="0.00")
        self.limit_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Период:").grid(row=0, column=4, padx=5, pady=5)
        self.period_combo = ctk.CTkComboBox(form_frame, values=["месяц", "неделя", "год"], width=100)
        self.period_combo.grid(row=0, column=5, padx=5, pady=5)

        # Кнопки
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="➕ Добавить бюджет",
                      command=self.add_budget).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="💾 Сохранить все",
                      command=self.save_budgets).pack(side="left", padx=5)

    def update_budgets_table(self):
        """Обновление таблицы бюджетов"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for budget in self.budgets:
            # В реальном приложении здесь был бы расчет использованных средств
            used = 0  # Заглушка
            remaining = budget.limit - used

            self.tree.insert("", "end", values=(
                budget.category,
                f"{budget.limit:,.2f}",
                budget.period,
                f"{used:,.2f}",
                f"{remaining:,.2f}"
            ))

    def add_budget(self):
        """Добавление нового бюджета"""
        try:
            category = self.category_combo.get()
            limit = float(self.limit_entry.get())
            period = self.period_combo.get()

            if not category or limit <= 0:
                raise ValueError("Заполните все поля корректно")

            new_budget = Budget(
                category=category,
                limit=limit,
                period=period
            )

            self.budgets.append(new_budget)
            self.update_budgets_table()

            # Очистка полей
            self.limit_entry.delete(0, "end")

        except ValueError as e:
            showerror("Ошибка", str(e))

    def save_budgets(self):
        """Сохранение бюджетов"""
        if self.on_update_budgets:
            self.on_update_budgets(self.budgets)
        showinfo("Успех", "Бюджеты сохранены!")
        self.destroy()
