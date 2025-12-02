from datetime import datetime
from tkinter.ttk import Treeview
from typing import List, Dict
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .base_window import BaseWindow
from ..models import Transaction, TransactionType


class AnalyticsWindow(BaseWindow):
    """Окно аналитики с детальными графиками"""

    def __init__(self, parent, transactions: List[Transaction]):
        super().__init__(parent, "Детальная аналитика", 1000, 700)
        self.transactions = transactions
        self.setup_analytics()

    def setup_analytics(self):
        """Настройка окна аналитики"""
        # Вкладки
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Создание вкладок
        self.summary_tab = self.tabview.add("Сводка")
        self.categories_tab = self.tabview.add("Анализ по категориям")
        self.timeline_tab = self.tabview.add("Временные ряды")

        # Заполнение вкладок
        self.create_summary_tab()
        self.create_categories_tab()
        self.create_timeline_tab()

    def create_summary_tab(self):
        """Создание вкладки со сводкой"""
        # Расчет статистики
        stats = self.calculate_statistics()

        # Отображение статистики
        text_widget = ctk.CTkTextbox(self.summary_tab, font=("Arial", 12))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        summary = f"""
{'=' * 50}
ФИНАНСОВАЯ СВОДКА
{'=' * 50}

Общая статистика:
  • Всего операций: {stats['total_transactions']}
  • Доходных операций: {stats['income_count']}
  • Расходных операций: {stats['expense_count']}

Финансовые показатели:
  • Общий доход: {stats['total_income']:,.2f} ₽
  • Общий расход: {stats['total_expense']:,.2f} ₽
  • Чистый баланс: {stats['net_balance']:,.2f} ₽

Средние значения:
  • Средний доход: {stats['avg_income']:,.2f} ₽
  • Средний расход: {stats['avg_expense']:,.2f} ₽
  • Средняя операция: {stats['avg_transaction']:,.2f} ₽

Период анализа:
  • Начало: {stats['start_date']}
  • Конец: {stats['end_date']}
  • Дней в периоде: {stats['days_count']}
"""
        text_widget.insert("1.0", summary)
        text_widget.configure(state="disabled")

    def create_categories_tab(self):
        """Создание вкладки с анализом по категориям"""
        # Таблица категорий
        columns = ("Категория", "Тип", "Сумма", "Кол-во", "Доля")
        tree = Treeview(self.categories_tab, columns=columns, show="headings", height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Заполнение данными
        categories_stats = self.analyze_categories()
        for cat, data in categories_stats.items():
            tree.insert("", "end", values=(
                cat,
                data['type'],
                f"{data['amount']:,.2f}",
                data['count'],
                f"{data['percentage']:.1f}%"
            ))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def create_timeline_tab(self):
        """Создание вкладки с временными рядами"""
        # График динамики
        fig = Figure(figsize=(9, 6))
        ax = fig.add_subplot(111)

        # Подготовка данных
        timeline_data = self.prepare_timeline_data()

        if timeline_data:
            dates = list(timeline_data.keys())
            income = [timeline_data[d]['income'] for d in dates]
            expense = [timeline_data[d]['expense'] for d in dates]
            balance = [timeline_data[d]['balance'] for d in dates]

            x = range(len(dates))
            width = 0.35

            # Столбцы доходов и расходов
            ax.bar(x, income, width, label='Доходы', color='green', alpha=0.7)
            ax.bar([i + width for i in x], expense, width, label='Расходы', color='red', alpha=0.7)

            # Линия баланса
            ax2 = ax.twinx()
            ax2.plot(x, balance, 'b-', linewidth=2, marker='o', label='Баланс')
            ax2.set_ylabel('Баланс (₽)', color='blue')
            ax2.tick_params(axis='y', labelcolor='blue')

            ax.set_xlabel('Период')
            ax.set_ylabel('Сумма (₽)')
            ax.set_title('Динамика доходов, расходов и баланса')
            ax.set_xticks([i + width / 2 for i in x])
            ax.set_xticklabels(dates, rotation=45, ha='right')
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')

            fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.timeline_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def calculate_statistics(self) -> Dict:
        """Расчет статистики"""
        if not self.transactions:
            return {}

        # Фильтрация по датам
        dates = [datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S") for t in self.transactions]
        start_date = min(dates).strftime("%Y-%m-%d")
        end_date = max(dates).strftime("%Y-%m-%d")

        income_transactions = [t for t in self.transactions if t.type == TransactionType.INCOME.value]
        expense_transactions = [t for t in self.transactions if t.type == TransactionType.EXPENSE.value]

        total_income = sum(t.amount for t in income_transactions)
        total_expense = sum(t.amount for t in expense_transactions)

        return {
            'total_transactions': len(self.transactions),
            'income_count': len(income_transactions),
            'expense_count': len(expense_transactions),
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': total_income - total_expense,
            'avg_income': total_income / len(income_transactions) if income_transactions else 0,
            'avg_expense': total_expense / len(expense_transactions) if expense_transactions else 0,
            'avg_transaction': (total_income + total_expense) / len(self.transactions) if self.transactions else 0,
            'start_date': start_date,
            'end_date': end_date,
            'days_count': (max(dates) - min(dates)).days + 1
        }

    def analyze_categories(self) -> Dict:
        """Анализ данных по категориям"""
        categories = {}

        for transaction in self.transactions:
            cat = transaction.category
            if cat not in categories:
                categories[cat] = {
                    'type': 'Доход' if transaction.type == TransactionType.INCOME.value else 'Расход',
                    'amount': 0,
                    'count': 0
                }

            categories[cat]['amount'] += transaction.amount
            categories[cat]['count'] += 1

        # Расчет долей
        for cat in categories:
            total = sum(categories[c]['amount'] for c in categories
                        if categories[c]['type'] == categories[cat]['type'])
            categories[cat]['percentage'] = (categories[cat]['amount'] / total * 100) if total > 0 else 0

        return categories

    def prepare_timeline_data(self) -> Dict:
        """Подготовка данных для временного ряда"""
        timeline = {}

        for transaction in self.transactions:
            date = datetime.strptime(transaction.date, "%Y-%m-%d %H:%M:%S")
            month_key = date.strftime("%Y-%m")

            if month_key not in timeline:
                timeline[month_key] = {'income': 0, 'expense': 0, 'balance': 0}

            if transaction.type == TransactionType.INCOME.value:
                timeline[month_key]['income'] += transaction.amount
                timeline[month_key]['balance'] += transaction.amount
            else:
                timeline[month_key]['expense'] += transaction.amount
                timeline[month_key]['balance'] -= transaction.amount

        return dict(sorted(timeline.items()))
