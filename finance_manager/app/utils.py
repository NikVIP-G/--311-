"""
Вспомогательные функции
"""
import os
import json
from datetime import datetime
from typing import Any, Dict, List
import pandas as pd


def format_currency(amount: float, currency: str = "₽") -> str:
    """Форматирование суммы с валютой"""
    return f"{amount:,.2f} {currency}".replace(",", " ")


def format_date(date_str: str, format_str: str = "%d.%m.%Y %H:%M") -> str:
    """Форматирование даты"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date.strftime(format_str)
    except ValueError:
        return date_str


def safe_json_load(filepath: str, default: Any = None) -> Any:
    """Безопасная загрузка JSON"""
    if default is None:
        default = {}

    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    return default


def export_to_excel(data: List[Dict], filename: str):
    """Экспорт данных в Excel"""
    df = pd.DataFrame(data)

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Данные', index=False)

        # Добавляем форматирование
        worksheet = writer.sheets['Данные']

        # Устанавливаем ширину колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width


def calculate_percentage(value: float, total: float) -> float:
    """Расчет процента"""
    if total == 0:
        return 0.0
    return (value / total) * 100


def get_month_name(month: int) -> str:
    """Получение названия месяца"""
    months = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    return months[month - 1] if 1 <= month <= 12 else ""
