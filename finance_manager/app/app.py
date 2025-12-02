"""
Главное окно приложения
"""
import customtkinter as ctk
from tkinter import messagebox

from .database import Database
from .controller import AppController
from .models import Transaction

from .Windows import (
    AddTransactionWindow,
    AnalyticsWindow,
    BudgetsWindow,
    CategoriesWindow,
    SettingsWindow
)

from .Frames import (
    BalanceFrame,
    TransactionsFrame,
    ChartsFrame,
    QuickActionsFrame
)


class FinanceApp:
    """Главный класс приложения"""

    def __init__(self):
        # Инициализация главного окна
        self.root = ctk.CTk()
        self.root.title("Personal Finance Manager")
        self.root.geometry("1400x800")
        self.root.minsize(800, 600)

        # Настройка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Инициализация базы данных и контроллера
        self.db = Database()
        self.controller = AppController(self.db)

        # Создание интерфейса
        self._create_menu()
        self._create_main_interface()

        # Обновление данных
        self.update_ui()

        # Регистрация в контроллере
        self.controller.add_update_callback(self.update_ui)

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _create_menu(self):
        """Создание главного меню"""
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(side="top", fill="x", padx=10, pady=5)

        menu_items = [
            ("➕ Добавить операцию", self.open_add_transaction),
            ("📊 Аналитика", self.open_analytics),
            ("🗂️ Категории", self.open_categories),
            ("💰 Бюджеты", self.open_budgets),
            ("⚙️ Настройки", self.open_settings),
            ("📤 Экспорт", self.export_data),
            ("ℹ️ О программе", self.show_about)
        ]

        for text, command in menu_items:
            btn = ctk.CTkButton(
                menu_frame,
                text=text,
                command=command,
                width=120,
                height=30,
                corner_radius=10
            )
            btn.pack(side="left", padx=2)

    def _create_main_interface(self):
        """Создание основного интерфейса"""
        # Основной контейнер
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Настройка сетки
        self.main_container.grid_rowconfigure(0, weight=0)  # Баланс
        self.main_container.grid_rowconfigure(1, weight=1)  # Контент
        self.main_container.grid_rowconfigure(2, weight=0)  # Быстрые действия
        self.main_container.grid_columnconfigure(0, weight=1)

        # Фрейм баланса
        self.balance_frame = BalanceFrame(
            self.main_container,
            controller=self.controller,
            fg_color="transparent"
        )
        self.balance_frame.grid(
            row=0, column=0,
            sticky="ew",
            padx=5, pady=5
        )

        # Основной контент
        content_frame = ctk.CTkFrame(self.main_container)
        content_frame.grid(
            row=1, column=0,
            sticky="nsew",
            padx=5, pady=5
        )

        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=2)  # Таблица
        content_frame.grid_columnconfigure(1, weight=1)  # Графики

        # Фрейм транзакций
        self.transactions_frame = TransactionsFrame(
            content_frame,
            controller=self.controller,
            on_delete=self.delete_transaction,
            on_edit=self.edit_transaction
        )
        self.transactions_frame.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(0, 5), pady=5
        )

        # Фрейм графиков
        self.charts_frame = ChartsFrame(
            content_frame,
            controller=self.controller
        )
        self.charts_frame.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(5, 0), pady=5
        )

        # Фрейм быстрых действий
        self.quick_actions_frame = QuickActionsFrame(
            self.main_container,
            controller=self.controller,
            on_quick_income=self.quick_add_income,
            on_quick_expense=self.quick_add_expense,
            on_report=self.generate_report
        )
        self.quick_actions_frame.grid(
            row=2, column=0,
            sticky="ew",
            padx=5, pady=5
        )

    def update_ui(self):
        """Обновление всего интерфейса"""
        try:
            # Обновление фреймов
            if hasattr(self, 'balance_frame'):
                self.balance_frame.refresh()
            if hasattr(self, 'transactions_frame'):
                self.transactions_frame.refresh()
            if hasattr(self, 'charts_frame'):
                self.charts_frame.refresh()
        except Exception as e:
            print(f"Ошибка обновления UI: {e}")
            import traceback
            traceback.print_exc()

    # Обработчики событий

    def open_add_transaction(self):
        """Открытие окна добавления транзакции"""
        try:
            window = AddTransactionWindow(
                self.root,
                controller=self.controller,
                on_save=self._handle_transaction_save
            )
            window.transient(self.root)
            window.grab_set()
            self.root.wait_window(window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно: {str(e)}")
            print(f"Ошибка открытия окна добавления: {e}")
            import traceback
            traceback.print_exc()

    def _handle_transaction_save(self, transaction):
        """Обработка сохранения транзакции"""
        try:
            self.controller.add_transaction(transaction)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить транзакцию: {str(e)}")

    def delete_transaction(self, transaction_id: str):
        """Удаление транзакции"""
        if messagebox.askyesno("Подтверждение", "Удалить выбранную операцию?"):
            try:
                self.controller.delete_transaction(transaction_id)
                messagebox.showinfo("Успех", "Операция удалена")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить транзакцию: {str(e)}")

    def edit_transaction(self):
        """Редактирование транзакции"""
        try:
            transaction_id = self.transactions_frame.get_selected_transaction_id()
            if transaction_id:
                # Находим транзакцию
                transaction = None
                for t in self.db.transactions:
                    if t.id == transaction_id:
                        transaction = t
                        break

                if transaction:
                    window = AddTransactionWindow(
                        self.root,
                        controller=self.controller,
                        transaction_id=transaction_id,
                        on_save=self._handle_transaction_update
                    )
                    window.transient(self.root)
                    window.grab_set()
                    self.root.wait_window(window)
                else:
                    messagebox.showwarning("Внимание", "Транзакция не найдена")
            else:
                messagebox.showwarning("Внимание", "Выберите операцию для редактирования")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно редактирования: {str(e)}")
            import traceback
            traceback.print_exc()

    def _handle_transaction_update(self, transaction):
        """Обработка обновления транзакции"""
        try:
            self.controller.update_transaction(transaction)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить транзакцию: {str(e)}")

    def open_analytics(self):
        """Открытие окна аналитики"""
        try:
            window = AnalyticsWindow(
                self.root,
                transactions=self.db.transactions
            )
            window.transient(self.root)
            window.grab_set()
            self.root.wait_window(window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть аналитику: {str(e)}")
            import traceback
            traceback.print_exc()

    def open_categories(self):
        """Открытие окна категорий"""
        try:
            window = CategoriesWindow(
                self.root,
                categories=self.db.categories,  # Теперь передаем объекты Category
                on_update_categories=self._handle_categories_update
            )
            window.transient(self.root)
            window.grab_set()
            self.root.wait_window(window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть категории: {str(e)}")
            import traceback
            traceback.print_exc()

    def _handle_categories_update(self, categories):
        """Обработка обновления категорий"""
        try:
            self.db.save_categories(categories)
            self.controller.notify_update()  # Уведомляем об обновлении
            messagebox.showinfo("Успех", "Категории обновлены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить категории: {str(e)}")

    def open_budgets(self):
        """Открытие окна бюджетов"""
        try:
            window = BudgetsWindow(
                self.root,
                budgets=self.db.budgets,
                on_update_budgets=self._handle_budgets_update
            )
            window.transient(self.root)
            window.grab_set()
            self.root.wait_window(window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть бюджеты: {str(e)}")
            import traceback
            traceback.print_exc()

    def _handle_budgets_update(self, budgets):
        """Обработка обновления бюджетов"""
        try:
            self.db.budgets = budgets
            self.db.save_budgets()
            self.controller.notify_update()  # Уведомляем об обновлении
            messagebox.showinfo("Успех", "Бюджеты обновлены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить бюджеты: {str(e)}")

    def open_settings(self):
        """Открытие окна настроек"""
        try:
            window = SettingsWindow(
                self.root,
                current_settings=self.db.settings.to_dict() if hasattr(self.db.settings, 'to_dict') else {},
                on_save_settings=self._handle_settings_update
            )
            window.transient(self.root)
            window.grab_set()
            self.root.wait_window(window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть настройки: {str(e)}")
            import traceback
            traceback.print_exc()

    def _handle_settings_update(self, settings):
        """Обработка обновления настроек"""
        try:
            # Обновляем настройки
            for key, value in settings.items():
                if hasattr(self.db.settings, key):
                    setattr(self.db.settings, key, value)

            self.db.save_settings()

            # Применение темы
            if 'theme' in settings:
                ctk.set_appearance_mode(settings['theme'])

            self.controller.notify_update()  # Уведомляем об обновлении
            messagebox.showinfo("Успех", "Настройки сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")

    def quick_add_income(self):
        """Быстрое добавление дохода"""
        self._quick_add("income")

    def quick_add_expense(self):
        """Быстрое добавление расхода"""
        self._quick_add("expense")

    def _quick_add(self, transaction_type):
        """Быстрое добавление транзакции"""
        dialog = ctk.CTkInputDialog(
            text=f"Введите сумму {'дохода' if transaction_type == 'income' else 'расхода'}:",
            title="Быстрое добавление"
        )

        amount = dialog.get_input()
        if amount:
            try:
                amount_float = float(amount.replace(',', '.'))
                if amount_float <= 0:
                    raise ValueError("Сумма должна быть положительной")

                # Получаем категории соответствующего типа
                if transaction_type == 'income':
                    categories = self.db.get_income_categories()
                else:
                    categories = self.db.get_expense_categories()

                if not categories:
                    categories = ["Прочее"]

                transaction = Transaction(
                    type=transaction_type,
                    category=categories[0],
                    amount=amount_float,
                    description="Быстрое добавление"
                )

                self.controller.add_transaction(transaction)
                messagebox.showinfo("Успех", "Операция добавлена")

            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def generate_report(self):
        """Генерация отчета"""
        try:
            import pandas as pd
            from datetime import datetime

            # Проверяем наличие данных
            if not self.db or not hasattr(self.db, 'transactions') or not self.db.transactions:
                messagebox.showwarning("Внимание", "Нет данных для отчета")
                return

            # Подготовка данных
            data = []
            for transaction in self.db.transactions:
                data.append({
                    'Дата': transaction.date,
                    'Тип': 'Доход' if transaction.type == 'income' else 'Расход',
                    'Категория': transaction.category,
                    'Сумма': transaction.amount,
                    'Описание': transaction.description
                })

            if not data:
                messagebox.showwarning("Внимание", "Нет данных для отчета")
                return

            df = pd.DataFrame(data)

            # Создание имени файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_report_{timestamp}.xlsx"

            # Сохранение в Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Все операции', index=False)

                # Сводка по категориям
                summary = df.groupby(['Тип', 'Категория'])['Сумма'].sum().reset_index()
                summary.to_excel(writer, sheet_name='Сводка', index=False)

            messagebox.showinfo("Успех", f"Отчет сохранен в файл:\n{filename}")

        except ImportError:
            messagebox.showerror("Ошибка",
                                 "Для создания отчетов необходимо установить библиотеки:\n"
                                 "pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {str(e)}")
            print(f"Ошибка создания отчета: {e}")
            import traceback
            traceback.print_exc()

    def export_data(self):
        """Экспорт данных"""
        try:
            import json
            from datetime import datetime

            # Проверяем наличие данных
            if not self.db:
                messagebox.showwarning("Внимание", "Нет данных для экспорта")
                return

            data = {
                'transactions': [t.to_dict() for t in self.db.transactions],
                'budgets': [{
                    'category': b.category,
                    'limit': b.limit,
                    'period': b.period,
                    'spent': getattr(b, 'spent', 0)
                } for b in self.db.budgets] if hasattr(self.db, 'budgets') else [],
                'settings': self.db.settings.to_dict() if hasattr(self.db, 'settings') else {},
                'categories': self.db.categories if hasattr(self.db, 'categories') else [],
                'export_date': datetime.now().isoformat()
            }

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"finance_backup_{timestamp}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("Экспорт", f"Данные экспортированы в файл:\n{filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")
            print(f"Ошибка экспорта: {e}")


    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
        Personal Finance Manager v1.0

        Приложение для учета личных финансов:
        • Учет доходов и расходов
        • Категоризация операций
        • Управление бюджетами
        • Аналитика и отчеты
        • Визуализация данных

        Разработано с использованием:
        • CustomTkinter - современный GUI
        • Pandas - анализ данных
        • Matplotlib - визуализация

        © 2025 Все права защищены
        """

        messagebox.showinfo("О программе", about_text)

    def on_closing(self):
        """Обработка закрытия приложения"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            try:
                # Сохраняем все данные
                if hasattr(self, 'db') and self.db:
                    self.db.save_all()
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении данных: {str(e)}")
                self.root.destroy()

    def run(self):
        """Запуск приложения"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Критическая ошибка в mainloop: {e}")
            import traceback
            traceback.print_exc()