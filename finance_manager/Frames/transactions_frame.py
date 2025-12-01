from .base_frame import BaseFrame
from customtkinter import CTkLabel, CTkFrame, CTkButton
from tkinter import ttk
from typing import List, Optional
from finance_manager.models import Transaction, TransactionType
from datetime import datetime


class TransactionsFrame(BaseFrame):
    """Фрейм для отображения и управления транзакциями"""

    def __init__(self, parent, on_delete=None, on_edit=None, **kwargs):
        self.on_delete_callback = on_delete
        self.on_edit_callback = on_edit
        super().__init__(parent, **kwargs)

    def setup_ui(self):
        # Заголовок
        self.title_label = CTkLabel(
            self,
            text="Последние операции",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=(5, 10))

        # Фрейм для таблицы
        table_container = CTkFrame(self)
        table_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Создание Treeview
        columns = ("Дата", "Тип", "Категория", "Сумма", "Описание")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=12)

        # Настройка колонок
        col_widths = {"Дата": 100, "Тип": 80, "Категория": 120, "Сумма": 100, "Описание": 200}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100))

        # Стилизация
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Привязка событий
        self.tree.bind("<Double-1>", self.on_double_click)

        # Панель кнопок
        self.create_button_panel()

    def create_button_panel(self):
        """Создание панели с кнопками управления"""
        btn_frame = CTkFrame(self, height=40)
        btn_frame.pack(fill="x", pady=(5, 0))

        buttons = [
            ("🔄 Обновить", self.refresh_table),
            ("✏️ Редактировать", self.edit_selected),
            ("🗑️ Удалить", self.delete_selected),
            ("🔍 Фильтр", self.show_filter_dialog)
        ]

        for text, command in buttons:
            btn = CTkButton(btn_frame, text=text, command=command, width=100)
            btn.pack(side="left", padx=5)

    def update_transactions(self, transactions: List[Transaction]):
        """Обновление таблицы транзакций"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавление транзакций
        for transaction in reversed(transactions[-50:]):  # Последние 50
            date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
            formatted_date = date.strftime("%d.%m.%Y %H:%M")

            values = (
                formatted_date,
                "Доход" if transaction.type == TransactionType.INCOME.value else "Расход",
                transaction.category,
                f"{transaction.amount:,.2f} ₽",
                transaction.description[:30] + "..." if len(transaction.description) > 30 else transaction.description
            )

            item = self.tree.insert("", "end", values=values)

            # Раскраска строк
            tags = ('income',) if transaction.type == TransactionType.INCOME.value else ('expense',)
            self.tree.item(item, tags=tags)

        # Настройка тегов для цветов
        self.tree.tag_configure('income', background='#d4edda')
        self.tree.tag_configure('expense', background='#f8d7da')

    def get_selected_transaction(self) -> Optional[int]:
        """Получение индекса выбранной транзакции"""
        selection = self.tree.selection()
        if selection:
            return self.tree.index(selection[0])
        return None

    def on_double_click(self, event):
        """Обработка двойного клика по транзакции"""
        if self.on_edit_callback:
            self.on_edit_callback()

    def edit_selected(self):
        """Редактирование выбранной транзакции"""
        if self.on_edit_callback:
            self.on_edit_callback()

    def delete_selected(self):
        """Удаление выбранной транзакции"""
        if self.on_delete_callback:
            self.on_delete_callback()

    def refresh_table(self):
        """Обновление таблицы"""
        # Может быть переопределен в родительском классе
        pass

    def show_filter_dialog(self):
        """Показ диалога фильтрации"""
        # Может быть переопределен в родительском классе
        pass
