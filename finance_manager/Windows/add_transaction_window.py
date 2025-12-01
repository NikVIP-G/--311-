from datetime import datetime
from tkinter import messagebox
from typing import List

from .base_window import BaseWindow
import customtkinter as ctk
from finance_manager.models import TransactionType, Transaction


class AddTransactionWindow(BaseWindow):
    """Окно добавления новой транзакции"""

    def __init__(self, parent, on_save_callback):
        super().__init__(parent, "Добавить операцию", 450, 550)
        self.on_save_callback = on_save_callback
        self.transaction_data = None
        self.setup_form()

    def setup_form(self):
        """Настройка формы добавления транзакции"""
        self.canvas = ctk.CTkCanvas(self.main_frame)
        self.scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Поля формы
        self.create_form_fields()

    def create_form_fields(self):
        """Создание полей формы"""
        row = 0

        # Тип операции
        ctk.CTkLabel(self.scrollable_frame, text="Тип операции:",
                     font=("Arial", 12, "bold")).grid(row=row, column=0, padx=10, pady=(15, 5), sticky="w")
        row += 1

        self.type_var = ctk.StringVar(value=TransactionType.EXPENSE.value)
        type_frame = ctk.CTkFrame(self.scrollable_frame)
        type_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ctk.CTkRadioButton(type_frame, text="Доход", variable=self.type_var,
                           value=TransactionType.INCOME.value, command=self.on_type_change).pack(side="left", padx=20)
        ctk.CTkRadioButton(type_frame, text="Расход", variable=self.type_var,
                           value=TransactionType.EXPENSE.value, command=self.on_type_change).pack(side="left", padx=20)
        row += 1

        # Категория
        ctk.CTkLabel(self.scrollable_frame, text="Категория:",
                     font=("Arial", 12, "bold")).grid(row=row, column=0, padx=10, pady=(15, 5), sticky="w")
        row += 1

        self.category_var = ctk.StringVar()
        self.category_combo = ctk.CTkComboBox(
            self.scrollable_frame,
            variable=self.category_var,
            values=self.get_default_categories(),
            width=300
        )
        self.category_combo.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        row += 1

        # Сумма
        ctk.CTkLabel(self.scrollable_frame, text="Сумма (₽):",
                     font=("Arial", 12, "bold")).grid(row=row, column=0, padx=10, pady=(15, 5), sticky="w")
        row += 1

        self.amount_var = ctk.StringVar()
        self.amount_entry = ctk.CTkEntry(
            self.scrollable_frame,
            textvariable=self.amount_var,
            placeholder_text="0.00",
            width=300
        )
        self.amount_entry.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        row += 1

        # Дата
        ctk.CTkLabel(self.scrollable_frame, text="Дата:",
                     font=("Arial", 12, "bold")).grid(row=row, column=0, padx=10, pady=(15, 5), sticky="w")
        row += 1

        self.date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = ctk.CTkEntry(
            self.scrollable_frame,
            textvariable=self.date_var,
            placeholder_text="ГГГГ-ММ-ДД",
            width=300
        )
        self.date_entry.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        row += 1

        # Описание
        ctk.CTkLabel(self.scrollable_frame, text="Описание:",
                     font=("Arial", 12, "bold")).grid(row=row, column=0, padx=10, pady=(15, 5), sticky="w")
        row += 1

        self.description_text = ctk.CTkTextbox(self.scrollable_frame, height=100, width=300)
        self.description_text.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        row += 1

        # Кнопки
        button_frame = ctk.CTkFrame(self.scrollable_frame)
        button_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        ctk.CTkButton(button_frame, text="Сохранить", command=self.save_transaction,
                      fg_color="green", hover_color="#2E7D32").pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Отмена", command=self.destroy,
                      fg_color="gray", hover_color="#424242").pack(side="left", padx=10)

    def get_default_categories(self) -> List[str]:
        """Получение списка категорий по умолчанию"""
        income_categories = ["Зарплата", "Фриланс", "Инвестиции", "Подарки", "Прочие доходы"]
        expense_categories = ["Продукты", "Транспорт", "Жилье", "Развлечения", "Здоровье", "Образование",
                              "Прочие расходы"]

        if self.type_var.get() == TransactionType.INCOME.value:
            return income_categories
        return expense_categories

    def on_type_change(self):
        """Обработка изменения типа операции"""
        categories = self.get_default_categories()
        self.category_combo.configure(values=categories)
        if categories:
            self.category_combo.set(categories[0])

    def save_transaction(self):
        """Сохранение транзакции"""
        try:
            # Валидация данных
            if not self.category_var.get():
                raise ValueError("Выберите категорию")

            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")

            # Проверка даты
            try:
                datetime.strptime(self.date_var.get(), "%Y-%m-%d")
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

            # Создание объекта транзакции
            transaction = Transaction(
                date=f"{self.date_var.get()} {datetime.now().strftime('%H:%M:%S')}",
                type=self.type_var.get(),
                category=self.category_var.get(),
                amount=amount,
                description=self.description_text.get("1.0", "end-1c").strip()
            )

            # Вызов callback
            if self.on_save_callback:
                self.on_save_callback(transaction)

            self.destroy()
            messagebox.showinfo("Успех", "Операция успешно добавлена!")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
