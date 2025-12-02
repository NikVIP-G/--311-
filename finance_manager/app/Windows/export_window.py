"""
Окно экспорта данных
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from typing import List

from .base_window import BaseWindow
from ..models import Transaction


class ExportWindow(BaseWindow):
    """Окно для экспорта данных"""

    def __init__(self, parent, transactions: List[Transaction],
                 budgets=None, settings=None, categories=None):
        super().__init__(parent, "Экспорт данных", 500, 400)
        self.transactions = transactions
        self.budgets = budgets or []
        self.settings = settings or {}
        self.categories = categories or []
        self.setup_export_ui()

    def setup_export_ui(self):
        """Настройка интерфейса экспорта"""
        # Заголовок
        ctk.CTkLabel(
            self.main_frame,
            text="📤 Экспорт данных",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 20))

        # Информация о данных
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=f"📊 Транзакций: {len(self.transactions)}",
            font=("Arial", 12)
        ).pack(pady=5)

        ctk.CTkLabel(
            info_frame,
            text=f"💰 Бюджетов: {len(self.budgets)}",
            font=("Arial", 12)
        ).pack(pady=5)

        ctk.CTkLabel(
            info_frame,
            text=f"🗂️ Категорий: {len(self.categories)}",
            font=("Arial", 12)
        ).pack(pady=5)

        # Формат экспорта
        format_frame = ctk.CTkFrame(self.main_frame)
        format_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            format_frame,
            text="Формат экспорта:",
            font=("Arial", 12, "bold")
        ).pack(pady=(5, 10))

        self.format_var = ctk.StringVar(value="json")

        formats = [
            ("JSON (все данные)", "json"),
            ("Excel (транзакции)", "excel"),
            ("CSV (транзакции)", "csv"),
            ("PDF отчет", "pdf")
        ]

        for text, value in formats:
            ctk.CTkRadioButton(
                format_frame,
                text=text,
                variable=self.format_var,
                value=value
            ).pack(anchor="w", padx=20, pady=2)

        # Настройки экспорта
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.pack(fill="x", padx=20, pady=10)

        self.include_summary_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            settings_frame,
            text="Включить сводку",
            variable=self.include_summary_var
        ).pack(anchor="w", padx=10, pady=2)

        self.include_charts_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            settings_frame,
            text="Включить графики (только PDF)",
            variable=self.include_charts_var
        ).pack(anchor="w", padx=10, pady=2)

        # Кнопки
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="📁 Выбрать папку и экспортировать",
            command=self.export_data,
            width=250,
            height=40,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="❌ Отмена",
            command=self.destroy,
            width=100,
            height=40
        ).pack(side="left", padx=10)

    def export_data(self):
        """Экспорт данных"""
        try:
            # Выбор папки для сохранения
            folder = filedialog.askdirectory(
                title="Выберите папку для сохранения"
            )

            if not folder:
                return

            export_format = self.format_var.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if export_format == "json":
                filename = self._export_json(folder, timestamp)
            elif export_format == "excel":
                filename = self._export_excel(folder, timestamp)
            elif export_format == "csv":
                filename = self._export_csv(folder, timestamp)
            elif export_format == "pdf":
                filename = self._export_pdf(folder, timestamp)
            else:
                messagebox.showerror("Ошибка", "Неизвестный формат")
                return

            if filename:
                messagebox.showinfo(
                    "Успех",
                    f"✅ Данные экспортированы:\n{filename}"
                )
                self.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта: {str(e)}")

    def _export_json(self, folder: str, timestamp: str) -> str:
        """Экспорт в JSON"""
        try:
            import json

            data = {
                'transactions': [t.to_dict() for t in self.transactions],
                'budgets': [{
                    'category': b.category,
                    'limit': b.limit,
                    'period': b.period,
                    'spent': getattr(b, 'spent', 0),
                    'type': getattr(b, 'type', 'expense')
                } for b in self.budgets],
                'settings': self.settings,
                'categories': [cat.to_dict() if hasattr(cat, 'to_dict') else cat
                               for cat in self.categories],
                'export_date': datetime.now().isoformat(),
                'app_version': '1.0.0'
            }

            filename = os.path.join(folder, f"finance_backup_{timestamp}.json")

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)

            return filename

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта в JSON: {str(e)}")
            return None

    def _export_excel(self, folder: str, timestamp: str) -> str:
        """Экспорт в Excel"""
        try:
            import pandas as pd

            if not self.transactions:
                messagebox.showwarning("Внимание", "Нет транзакций для экспорта")
                return None

            # Подготовка данных транзакций
            transactions_data = []
            for t in self.transactions:
                transactions_data.append({
                    'ID': t.id,
                    'Дата': t.date,
                    'Тип': 'Доход' if t.type == 'income' else 'Расход',
                    'Категория': t.category,
                    'Сумма': t.amount,
                    'Валюта': 'RUB',
                    'Описание': t.description
                })

            filename = os.path.join(folder, f"transactions_{timestamp}.xlsx")

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Лист транзакций
                df = pd.DataFrame(transactions_data)
                df.to_excel(writer, sheet_name='Транзакции', index=False)

                # Лист сводки
                if self.include_summary_var.get():
                    summary = df.groupby(['Тип', 'Категория'])['Сумма'].sum().reset_index()
                    summary.to_excel(writer, sheet_name='Сводка', index=False)

                # Лист бюджетов (если есть)
                if self.budgets:
                    budgets_data = []
                    for b in self.budgets:
                        budgets_data.append({
                            'Категория': b.category,
                            'Лимит': b.limit,
                            'Период': b.period,
                            'Потрачено': getattr(b, 'spent', 0),
                            'Остаток': getattr(b, 'limit', 0) - getattr(b, 'spent', 0),
                            'Тип': getattr(b, 'type', 'expense')
                        })
                    budgets_df = pd.DataFrame(budgets_data)
                    budgets_df.to_excel(writer, sheet_name='Бюджеты', index=False)

            return filename

        except ImportError:
            messagebox.showerror(
                "Ошибка",
                "Для экспорта в Excel установите:\npip install pandas openpyxl"
            )
            return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта в Excel: {str(e)}")
            return None

    def _export_csv(self, folder: str, timestamp: str) -> str:
        """Экспорт в CSV"""
        try:
            import csv

            if not self.transactions:
                messagebox.showwarning("Внимание", "Нет транзакций для экспорта")
                return None

            filename = os.path.join(folder, f"transactions_{timestamp}.csv")

            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['ID', 'Дата', 'Тип', 'Категория', 'Сумма', 'Описание']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for t in self.transactions:
                    writer.writerow({
                        'ID': t.id,
                        'Дата': t.date,
                        'Тип': 'Доход' if t.type == 'income' else 'Расход',
                        'Категория': t.category,
                        'Сумма': t.amount,
                        'Описание': t.description
                    })

            return filename

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта в CSV: {str(e)}")
            return None

    def _export_pdf(self, folder: str, timestamp: str) -> str:
        """Экспорт в PDF"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.units import inch

            if not self.transactions:
                messagebox.showwarning("Внимание", "Нет транзакций для экспорта")
                return None

            filename = os.path.join(folder, f"finance_report_{timestamp}.pdf")

            doc = SimpleDocTemplate(filename, pagesize=A4)
            elements = []

            styles = getSampleStyleSheet()

            # Заголовок
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # center
            )

            elements.append(Paragraph("Финансовый отчет", title_style))
            elements.append(Paragraph(f"Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                                      styles["Normal"]))
            elements.append(Spacer(1, 20))

            # Сводка
            if self.include_summary_var.get():
                income = sum(t.amount for t in self.transactions if t.type == 'income')
                expense = sum(t.amount for t in self.transactions if t.type == 'expense')
                balance = income - expense

                summary_data = [
                    ["Показатель", "Сумма (₽)"],
                    ["Доходы", f"{income:,.2f}"],
                    ["Расходы", f"{expense:,.2f}"],
                    ["Баланс", f"{balance:,.2f}"]
                ]

                summary_table = Table(summary_data, colWidths=[2 * inch, 2 * inch])
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                elements.append(Paragraph("Сводка", styles["Heading2"]))
                elements.append(summary_table)
                elements.append(Spacer(1, 20))

            # Таблица транзакций (первые 50)
            if len(self.transactions) > 0:
                elements.append(Paragraph("Транзакции", styles["Heading2"]))
                elements.append(Paragraph(f"Всего транзакций: {len(self.transactions)}", styles["Normal"]))

                # Подготовка данных
                table_data = [["Дата", "Тип", "Категория", "Сумма", "Описание"]]

                for t in self.transactions[:50]:  # Ограничиваем количество
                    date_str = t.date[:10] if len(t.date) > 10 else t.date
                    type_str = "Доход" if t.type == 'income' else "Расход"
                    amount_str = f"{t.amount:,.2f} ₽"
                    desc = t.description[:30] + "..." if len(t.description) > 30 else t.description

                    table_data.append([date_str, type_str, t.category, amount_str, desc])

                # Создание таблицы
                col_widths = [1 * inch, 0.8 * inch, 1 * inch, 1 * inch, 2 * inch]
                table = Table(table_data, colWidths=col_widths, repeatRows=1)

                # Стиль таблицы
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))

                elements.append(table)

            # Создание PDF
            doc.build(elements)
            return filename

        except ImportError:
            messagebox.showerror(
                "Ошибка",
                "Для экспорта в PDF установите:\npip install reportlab"
            )
            return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта в PDF: {str(e)}")
            return None
