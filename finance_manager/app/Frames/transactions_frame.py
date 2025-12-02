"""
Фрейм для отображения и управления транзакциями
"""
import customtkinter as ctk
from tkinter import ttk, messagebox
from typing import Optional
from datetime import datetime

from finance_manager.app.models import TransactionType
from .base_frame import BaseFrame


class TransactionsFrame(BaseFrame):
    """Фрейм транзакций"""

    def __init__(self, parent, controller=None, on_delete=None, on_edit=None, **kwargs):
        self.on_delete_callback = on_delete
        self.on_edit_callback = on_edit
        # Передаем контроллер в родительский конструктор
        super().__init__(parent, controller=controller, **kwargs)

    def setup_ui(self):
        """Настройка интерфейса"""
        # Конфигурация сетки
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Заголовок
        self.grid_rowconfigure(1, weight=1)  # Таблица
        self.grid_rowconfigure(2, weight=0)  # Кнопки

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Последние операции",
            font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Фрейм для таблицы
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Создание Treeview
        columns = ("Дата", "Тип", "Категория", "Сумма", "Описание")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            selectmode="browse"
        )

        # Настройка колонок
        col_widths = {
            "Дата": 120,
            "Тип": 80,
            "Категория": 120,
            "Сумма": 100,
            "Описание": 200
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100), minwidth=50)

        # Стилизация
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещение
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Привязка событий
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Панель кнопок
        self._create_button_panel()

        # Загрузка данных
        self.update_data()

    def _create_button_panel(self):
        """Создание панели кнопок"""
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

        # Кнопки
        buttons = [
            ("🔄 Обновить", self.refresh_table, "blue"),
            ("✏️ Редактировать", self.edit_selected, "orange"),
            ("🗑️ Удалить", self.delete_selected, "red"),
            ("🔍 Фильтр", self.show_filter_dialog, "green"),
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=self._darken_color(color),
                width=120
            )
            btn.grid(row=0, column=i, padx=5, pady=5)

    def _darken_color(self, color_name: str) -> str:
        """Затемнение цвета для эффекта hover"""
        colors = {
            "blue": "#1E40AF",
            "orange": "#EA580C",
            "red": "#DC2626",
            "green": "#059669"
        }
        return colors.get(color_name, "#374151")

    def update_data(self):
        """Обновление данных в таблице"""
        if not self.db:
            print("База данных не доступна в TransactionsFrame")
            return

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Получение транзакций
        try:
            transactions = self.db.get_transactions(limit=50)
        except Exception as e:
            print(f"Ошибка получения транзакций: {e}")
            return

        # Добавление в таблицу
        for transaction in transactions:
            # Форматирование даты
            try:
                date_str = datetime.strptime(
                    transaction.date,
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%d.%m.%Y %H:%M")
            except ValueError:
                date_str = transaction.date

            # Форматирование типа
            type_str = "Доход" if transaction.type == TransactionType.INCOME.value else "Расход"

            # Форматирование суммы
            amount_str = f"{transaction.amount:,.2f} ₽".replace(",", " ")

            # Обрезание описания
            description = transaction.description
            if len(description) > 30:
                description = description[:27] + "..."

            values = (
                date_str,
                type_str,
                transaction.category,
                amount_str,
                description
            )

            item = self.tree.insert("", "end", values=values, tags=(transaction.id,))

            # Раскраска строк
            if transaction.type == TransactionType.INCOME.value:
                self.tree.tag_configure('income', background='#D1FAE5')
                self.tree.item(item, tags=(transaction.id, 'income'))
            else:
                self.tree.tag_configure('expense', background='#FEE2E2')
                self.tree.item(item, tags=(transaction.id, 'expense'))

    def _on_double_click(self, event):
        """Обработка двойного клика"""
        if self.on_edit_callback:
            self.on_edit_callback()

    def _on_select(self, event):
        """Обработка выбора строки"""
        pass

    def get_selected_transaction_id(self) -> Optional[str]:
        """Получение ID выбранной транзакции"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            tags = item['tags']
            if tags:
                return tags[0]  # Первый тег - ID транзакции
        return None

    def edit_selected(self):
        """Редактирование выбранной транзакции"""
        if self.on_edit_callback:
            self.on_edit_callback()

    def delete_selected(self):
        """Удаление выбранной транзакции"""
        transaction_id = self.get_selected_transaction_id()
        if transaction_id and self.on_delete_callback:
            self.on_delete_callback(transaction_id)

    def refresh_table(self):
        """Обновление таблицы"""
        self.update_data()
        messagebox.showinfo("Обновлено", "Таблица транзакций обновлена")

    def show_filter_dialog(self):
        """Показ диалога фильтрации"""
        messagebox.showinfo("Фильтр", "Функция фильтрации будет реализована в следующей версии")
