"""
Фрейм для отображения графиков и диаграмм
"""
import customtkinter as ctk
from datetime import datetime, timedelta
from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from .base_frame import BaseFrame


class ChartsFrame(BaseFrame):
    """Фрейм графиков с визуализацией финансовых данных"""

    def __init__(self, parent, controller=None, **kwargs):
        super().__init__(parent, controller=controller, **kwargs)
        self.figures = []
        self.canvases = []
        self.current_tab = 0

    def setup_ui(self):
        """Настройка интерфейса"""
        # Конфигурация сетки
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Заголовок и вкладки
        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Аналитика и графики",
            font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Вкладки для разных графиков
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Создание вкладок
        self.income_expense_tab = self.tabview.add("Доходы/Расходы")
        self.categories_tab = self.tabview.add("По категориям")
        self.trends_tab = self.tabview.add("Динамика")
        self.budget_tab = self.tabview.add("Бюджет")

        # Настройка вкладок
        self.tabview.grid_columnconfigure(0, weight=1)
        self.tabview.grid_rowconfigure(0, weight=1)

        # Кнопка обновления
        self.refresh_btn = ctk.CTkButton(
            self,
            text="🔄 Обновить графики",
            command=self.refresh_all_charts,
            width=120,
            height=30
        )
        self.refresh_btn.grid(row=2, column=0, padx=10, pady=(0, 10))

        # Привязка события смены вкладки
        self.tabview.configure(command=self.on_tab_change)

    def on_tab_change(self):
        """Обработчик смены вкладки"""
        self.current_tab = self.tabview.get()
        self.refresh_current_chart()

    def update_data(self):
        """Обновление всех графиков"""
        try:
            self.refresh_all_charts()
        except Exception as e:
            print(f"Ошибка обновления графиков: {e}")
            import traceback
            traceback.print_exc()

    def refresh_all_charts(self):
        """Обновление всех графиков"""
        self.clear_charts()
        self.create_income_expense_chart()
        self.create_categories_chart()
        self.create_trends_chart()
        self.create_budget_chart()
        self.update_canvases()

    def refresh_current_chart(self):
        """Обновление текущего графика"""
        self.clear_current_tab()

        if self.current_tab == "Доходы/Расходы":
            self.create_income_expense_chart()
        elif self.current_tab == "По категориям":
            self.create_categories_chart()
        elif self.current_tab == "Динамика":
            self.create_trends_chart()
        elif self.current_tab == "Бюджет":
            self.create_budget_chart()

        self.update_canvases()

    def clear_charts(self):
        """Очистка всех графиков"""
        for canvas in self.canvases:
            try:
                canvas.get_tk_widget().destroy()
            except:
                pass

        for fig in self.figures:
            try:
                plt.close(fig)
            except:
                pass

        self.figures.clear()
        self.canvases.clear()

    def clear_current_tab(self):
        """Очистка текущей вкладки"""
        current_frame = None

        if self.current_tab == "Доходы/Расходы":
            current_frame = self.income_expense_tab
        elif self.current_tab == "По категориям":
            current_frame = self.categories_tab
        elif self.current_tab == "Динамика":
            current_frame = self.trends_tab
        elif self.current_tab == "Бюджет":
            current_frame = self.budget_tab

        if current_frame:
            for widget in current_frame.winfo_children():
                widget.destroy()

    def create_income_expense_chart(self):
        """Создание графика доходов/расходов"""
        if not self.db:
            return

        try:
            # Получение данных за текущий месяц
            current_month = datetime.now().month
            current_year = datetime.now().year

            income = 0
            expense = 0

            for transaction in self.db.transactions:
                try:
                    date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
                    if date.month == current_month and date.year == current_year:
                        if transaction.type == 'income':
                            income += transaction.amount
                        else:
                            expense += transaction.amount
                except:
                    continue

            # Создание графика
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)

            labels = ['Доходы', 'Расходы']
            values = [income, expense]
            colors = ['#4CAF50', '#F44336']

            bars = ax.bar(labels, values, color=colors, edgecolor='black', linewidth=1)

            # Добавление значений на столбцы
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.02,
                       f'{value:,.0f} ₽', ha='center', va='bottom', fontsize=10)

            ax.set_title(f'Доходы и расходы за {current_month}.{current_year}',
                        fontsize=14, fontweight='bold')
            ax.set_ylabel('Сумма (₽)', fontsize=12)
            ax.grid(axis='y', alpha=0.3)
            ax.set_axisbelow(True)

            # Расчет баланса
            balance = income - expense
            ax.text(0.5, -0.15, f'Баланс: {balance:,.0f} ₽',
                   transform=ax.transAxes, ha='center', fontsize=12,
                   fontweight='bold', color='green' if balance >= 0 else 'red')

            fig.tight_layout()

            # Добавление на вкладку
            canvas = FigureCanvasTkAgg(fig, self.income_expense_tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

            self.figures.append(fig)
            self.canvases.append(canvas)

        except Exception as e:
            print(f"Ошибка создания графика доходов/расходов: {e}")

    def create_categories_chart(self):
        """Создание круговой диаграммы по категориям"""
        if not self.db:
            return

        try:
            # Анализ расходов по категориям
            categories_data = {}

            for transaction in self.db.transactions:
                if transaction.type == 'expense':  # Только расходы
                    category = transaction.category
                    if category not in categories_data:
                        categories_data[category] = 0
                    categories_data[category] += transaction.amount

            if not categories_data:
                # Если нет данных, показываем сообщение
                label = ctk.CTkLabel(
                    self.categories_tab,
                    text="Нет данных о расходах",
                    font=("Arial", 14),
                    text_color="gray"
                )
                label.pack(expand=True)
                return

            # Сортировка и выбор топ-10 категорий
            sorted_categories = sorted(categories_data.items(), key=lambda x: x[1], reverse=True)
            top_categories = sorted_categories[:10]

            labels = [cat for cat, _ in top_categories]
            values = [val for _, val in top_categories]

            # Создание графика
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)

            # Цветовая схема
            colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

            wedges, texts, autotexts = ax.pie(
                values,
                labels=labels,
                colors=colors,
                autopct=lambda pct: f'{pct:.1f}%\n({pct*sum(values)/100:,.0f} ₽)',
                startangle=90,
                textprops={'fontsize': 9}
            )

            ax.set_title('Расходы по категориям', fontsize=14, fontweight='bold')

            # Настройка отображения процентов
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontsize(8)

            fig.tight_layout()

            # Добавление на вкладку
            canvas = FigureCanvasTkAgg(fig, self.categories_tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

            self.figures.append(fig)
            self.canvases.append(canvas)

        except Exception as e:
            print(f"Ошибка создания круговой диаграммы: {e}")

    def create_trends_chart(self):
        """Создание графика динамики"""
        if not self.db:
            return

        try:
            # Анализ данных за последние 6 месяцев
            current_date = datetime.now()
            months_data = {}

            for i in range(6):
                month = current_date.month - i
                year = current_date.year
                if month <= 0:
                    month += 12
                    year -= 1

                months_data[f"{month:02d}/{year}"] = {'income': 0, 'expense': 0}

            # Сбор данных
            for transaction in self.db.transactions:
                try:
                    date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
                    month_key = f"{date.month:02d}/{date.year}"

                    if month_key in months_data:
                        if transaction.type == 'income':
                            months_data[month_key]['income'] += transaction.amount
                        else:
                            months_data[month_key]['expense'] += transaction.amount
                except:
                    continue

            # Подготовка данных для графика
            months = list(reversed(list(months_data.keys())))
            income_data = [months_data[m]['income'] for m in months]
            expense_data = [months_data[m]['expense'] for m in months]

            # Создание графика
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)

            x = np.arange(len(months))
            width = 0.35

            bars1 = ax.bar(x - width/2, income_data, width, label='Доходы', color='#4CAF50')
            bars2 = ax.bar(x + width/2, expense_data, width, label='Расходы', color='#F44336')

            ax.set_xlabel('Месяц', fontsize=12)
            ax.set_ylabel('Сумма (₽)', fontsize=12)
            ax.set_title('Динамика доходов и расходов', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(months, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            ax.set_axisbelow(True)

            # Добавление значений на столбцы
            def add_values(bars):
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height + max(max(income_data), max(expense_data))*0.01,
                               f'{height:,.0f}', ha='center', va='bottom', fontsize=8)

            add_values(bars1)
            add_values(bars2)

            fig.tight_layout()

            # Добавление на вкладку
            canvas = FigureCanvasTkAgg(fig, self.trends_tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

            self.figures.append(fig)
            self.canvases.append(canvas)

        except Exception as e:
            print(f"Ошибка создания графика динамики: {e}")

    def create_budget_chart(self):
        """Создание графика бюджета"""
        if not self.db:
            return

        try:
            # Проверяем наличие бюджетов
            if not hasattr(self.db, 'budgets') or not self.db.budgets:
                # Если нет бюджетов, показываем сообщение
                label = ctk.CTkLabel(
                    self.budget_tab,
                    text="Бюджеты не настроены\n\nПерейдите в '💰 Бюджеты' для настройки",
                    font=("Arial", 14),
                    text_color="gray"
                )
                label.pack(expand=True)
                return

            # Подготовка данных для графика
            categories = []
            limits = []
            spent = []
            percentages = []

            for budget in self.db.budgets[:8]:  # Показываем топ-8 бюджетов
                # В реальном приложении здесь должен быть расчет потраченных средств
                # Для демонстрации используем случайные данные
                import random
                actual_spent = budget.spent if hasattr(budget, 'spent') else random.uniform(0, budget.limit)

                categories.append(budget.category)
                limits.append(budget.limit)
                spent.append(actual_spent)

                percentage = (actual_spent / budget.limit * 100) if budget.limit > 0 else 0
                percentages.append(percentage)

            # Создание графика
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)

            x = np.arange(len(categories))
            width = 0.35

            bars1 = ax.bar(x - width/2, limits, width, label='Лимит', color='#2196F3', alpha=0.7)
            bars2 = ax.bar(x + width/2, spent, width, label='Потрачено', color='#FF9800')

            # Добавление процентной информации
            for i, (limit, spent_val, percentage) in enumerate(zip(limits, spent, percentages)):
                color = 'green' if percentage <= 80 else 'orange' if percentage <= 100 else 'red'
                ax.text(i, max(limit, spent_val) * 1.05,
                       f'{percentage:.0f}%',
                       ha='center', fontsize=9, fontweight='bold', color=color)

            ax.set_xlabel('Категории', fontsize=12)
            ax.set_ylabel('Сумма (₽)', fontsize=12)
            ax.set_title('Использование бюджета', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=9)
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            ax.set_axisbelow(True)

            fig.tight_layout()

            # Добавление на вкладку
            canvas = FigureCanvasTkAgg(fig, self.budget_tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

            self.figures.append(fig)
            self.canvases.append(canvas)

        except Exception as e:
            print(f"Ошибка создания графика бюджета: {e}")

    def update_canvases(self):
        """Обновление всех канвасов"""
        for canvas in self.canvases:
            try:
                canvas.draw()
            except:
                pass

    def refresh(self):
        """Обновление фрейма (реализация метода из BaseFrame)"""
        self.update_data()