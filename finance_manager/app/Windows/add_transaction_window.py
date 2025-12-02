"""
Окно добавления/редактирования транзакции
"""
import customtkinter as ctk
from tkinter import messagebox

from finance_manager.app.models import Transaction


class AddTransactionWindow(ctk.CTkToplevel):
    """Окно для работы с транзакциями"""

    def __init__(self, parent, controller, transaction_id=None, on_save=None):
        super().__init__(parent)

        self.controller = controller
        self.transaction_id = transaction_id
        self.on_save_callback = on_save

        # Получаем базу данных через контроллер
        self.db = controller.get_database() if controller else None

        # Настройка окна
        if transaction_id:
            self.title("Редактировать операцию")
            self.transaction = None
            if self.db and hasattr(self.db, 'transactions'):
                for t in self.db.transactions:
                    if t.id == transaction_id:
                        self.transaction = t
                        break
        else:
            self.title("Добавить операцию")
            self.transaction = None

        self.geometry("500x600")
        self.resizable(False, False)
        self.grab_set()  # Модальное окно

        # Центрирование
        self._center_window()

        # Создание интерфейса
        self._create_widgets()

        # Если редактирование - заполняем поля
        if self.transaction:
            self._fill_fields()

    def _center_window(self):
        """Центрирование окна"""
        self.update_idletasks()
        width = 500
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        """Создание виджетов"""
        # Основной фрейм
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Тип операции
        ctk.CTkLabel(main_frame, text="Тип операции:",
                    font=("Arial", 12, "bold")).pack(pady=(0, 5))

        self.type_var = ctk.StringVar(value="expense")

        type_frame = ctk.CTkFrame(main_frame)
        type_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkRadioButton(
            type_frame,
            text="Доход",
            variable=self.type_var,
            value="income",
            command=self._on_type_change
        ).pack(side="left", padx=20)

        ctk.CTkRadioButton(
            type_frame,
            text="Расход",
            variable=self.type_var,
            value="expense",
            command=self._on_type_change
        ).pack(side="left", padx=20)

        # Категория
        ctk.CTkLabel(main_frame, text="Категория:",
                    font=("Arial", 12, "bold")).pack(pady=(0, 5))

        self.category_var = ctk.StringVar()
        self.category_combo = ctk.CTkComboBox(
            main_frame,
            variable=self.category_var,
            values=self._get_categories(),
            width=300
        )
        self.category_combo.pack(pady=(0, 15))

        # Сумма
        ctk.CTkLabel(main_frame, text="Сумма (₽):",
                    font=("Arial", 12, "bold")).pack(pady=(0, 5))

        self.amount_var = ctk.StringVar()
        self.amount_entry = ctk.CTkEntry(
            main_frame,
            textvariable=self.amount_var,
            placeholder_text="0.00",
            width=300
        )
        self.amount_entry.pack(pady=(0, 15))

        # Описание
        ctk.CTkLabel(main_frame, text="Описание:",
                    font=("Arial", 12, "bold")).pack(pady=(0, 5))

        self.description_text = ctk.CTkTextbox(main_frame, height=100, width=300)
        self.description_text.pack(pady=(0, 20))

        # Кнопки
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=(10, 0))

        save_text = "Сохранить" if self.transaction else "Добавить"
        ctk.CTkButton(
            button_frame,
            text=save_text,
            command=self._save_transaction,
            fg_color="green",
            hover_color="#2E7D32",
            width=120
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Отмена",
            command=self.destroy,
            fg_color="gray",
            hover_color="#424242",
            width=120
        ).pack(side="left", padx=10)

    def _get_categories(self):
        """Получение категорий"""
        categories = []
        if self.controller and hasattr(self.controller, 'get_categories'):
            categories = self.controller.get_categories()

        if not categories:
            # Категории по умолчанию
            if self.type_var.get() == "income":
                categories = ["Зарплата", "Фриланс", "Инвестиции", "Подарки", "Возврат", "Прочие доходы"]
            else:
                categories = ["Продукты", "Кафе и рестораны", "Транспорт", "Жилье", "Развлечения",
                           "Здоровье", "Образование", "Прочие расходы"]

        return categories

    def _on_type_change(self):
        """Обработка изменения типа операции"""
        categories = self._get_categories()
        self.category_combo.configure(values=categories)
        if categories and not self.category_var.get():
            self.category_combo.set(categories[0])

    def _fill_fields(self):
        """Заполнение полей при редактировании"""
        if self.transaction:
            self.type_var.set(self.transaction.type)
            self.category_var.set(self.transaction.category)
            self.amount_var.set(str(self.transaction.amount))
            self.description_text.insert("1.0", self.transaction.description)
            self._on_type_change()  # Обновляем категории

    def _save_transaction(self):
        """Сохранение транзакции"""
        try:
            # Валидация
            category = self.category_var.get().strip()
            if not category:
                raise ValueError("Выберите категорию")

            try:
                amount = float(self.amount_var.get().replace(",", "."))
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
            except ValueError:
                raise ValueError("Введите корректную положительную сумму")

            description = self.description_text.get("1.0", "end-1c").strip()

            # Создание или обновление транзакции
            if self.transaction:
                # Обновление существующей
                self.transaction.type = self.type_var.get()
                self.transaction.category = category
                self.transaction.amount = amount
                self.transaction.description = description
                transaction = self.transaction
                action = "обновлена"
            else:
                # Создание новой
                transaction = Transaction(
                    type=self.type_var.get(),
                    category=category,
                    amount=amount,
                    description=description
                )
                action = "добавлена"

            # Сохранение через callback
            if self.on_save_callback:
                self.on_save_callback(transaction)

            self.destroy()
            messagebox.showinfo("Успех", f"Операция {action}!")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
