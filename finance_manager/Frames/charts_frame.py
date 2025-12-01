from typing import Dict, List

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .base_frame import BaseFrame
from customtkinter import CTkLabel,  CTkTabview


class ChartsFrame(BaseFrame):
    """Фрейм для отображения графиков и диаграмм"""

    def setup_ui(self):
        # Заголовок
        self.title_label = CTkLabel(
            self,
            text="Визуализация данных",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=(5, 10))

        # Вкладки для разных типов графиков
        self.tabview = CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        # Создание вкладок
        self.expense_tab = self.tabview.add("Расходы по категориям")
        self.income_tab = self.tabview.add("Доходы по месяцам")
        self.balance_tab = self.tabview.add("Динамика баланса")

        # Инициализация графиков
        self.expense_chart = None
        self.income_chart = None
        self.balance_chart = None

    def update_expense_chart(self, expenses_by_category: Dict[str, float]):
        """Обновление круговой диаграммы расходов"""
        if self.expense_chart:
            self.expense_chart.get_tk_widget().destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if expenses_by_category:
            labels = list(expenses_by_category.keys())
            sizes = list(expenses_by_category.values())
            colors = plt.cm.Set3(range(len(labels)))

            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                   colors=colors, textprops={'fontsize': 8})
            ax.axis('equal')
            ax.set_title('Распределение расходов по категориям', fontsize=12)
        else:
            ax.text(0.5, 0.5, 'Нет данных о расходах',
                    ha='center', va='center', fontsize=14)
            ax.axis('off')

        self.expense_chart = FigureCanvasTkAgg(fig, self.expense_tab)
        self.expense_chart.draw()
        self.expense_chart.get_tk_widget().pack(fill="both", expand=True)

    def update_income_chart(self, monthly_income: Dict[str, float]):
        """Обновление графика доходов по месяцам"""
        if self.income_chart:
            self.income_chart.get_tk_widget().destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if monthly_income:
            months = list(monthly_income.keys())
            incomes = list(monthly_income.values())

            ax.bar(months, incomes, color='green', alpha=0.7)
            ax.set_title('Доходы по месяцам', fontsize=12)
            ax.set_xlabel('Месяц')
            ax.set_ylabel('Сумма (₽)')
            ax.tick_params(axis='x', rotation=45)

            # Добавление значений над столбцами
            for i, v in enumerate(incomes):
                ax.text(i, v + max(incomes) * 0.01, f'{v:,.0f}',
                        ha='center', fontsize=8)
        else:
            ax.text(0.5, 0.5, 'Нет данных о доходах',
                    ha='center', va='center', fontsize=14)
            ax.axis('off')

        self.income_chart = FigureCanvasTkAgg(fig, self.income_tab)
        self.income_chart.draw()
        self.income_chart.get_tk_widget().pack(fill="both", expand=True)

    def update_balance_chart(self, balance_history: List[float]):
        """Обновление графика динамики баланса"""
        if self.balance_chart:
            self.balance_chart.get_tk_widget().destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if balance_history:
            days = list(range(1, len(balance_history) + 1))
            ax.plot(days, balance_history, 'b-', linewidth=2, marker='o', markersize=4)
            ax.fill_between(days, balance_history, alpha=0.3)

            ax.set_title('Динамика баланса', fontsize=12)
            ax.set_xlabel('Дни')
            ax.set_ylabel('Баланс (₽)')
            ax.grid(True, alpha=0.3)

            # Подсветка последнего значения
            last_day = days[-1]
            last_balance = balance_history[-1]
            ax.scatter([last_day], [last_balance], color='red', s=100, zorder=5)
            ax.annotate(f'{last_balance:,.0f} ₽',
                        xy=(last_day, last_balance),
                        xytext=(last_day, last_balance + max(balance_history) * 0.1),
                        ha='center',
                        fontsize=9,
                        arrowprops=dict(arrowstyle='->', color='red'))
        else:
            ax.text(0.5, 0.5, 'Нет данных о балансе',
                    ha='center', va='center', fontsize=14)
            ax.axis('off')

        self.balance_chart = FigureCanvasTkAgg(fig, self.balance_tab)
        self.balance_chart.draw()
        self.balance_chart.get_tk_widget().pack(fill="both", expand=True)
