"""
Модели данных
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List


class TransactionType(Enum):
    """Типы транзакций"""
    INCOME = "income"
    EXPENSE = "expense"


class CategoryType(Enum):
    """Типы категорий"""
    INCOME = "income"
    EXPENSE = "expense"
    BOTH = "both"  # Для категорий, которые могут быть и доходом и расходом


@dataclass
class Category:
    """Модель категории с указанием типа"""
    name: str
    type: CategoryType = CategoryType.EXPENSE
    color: str = ""  # Цвет для отображения
    icon: str = ""  # Иконка

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type.value,
            'color': self.color,
            'icon': self.icon
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name=data['name'],
            type=CategoryType(data.get('type', 'expense')),
            color=data.get('color', ''),
            icon=data.get('icon', '')
        )


@dataclass
class Transaction:
    """Модель транзакции"""
    id: Optional[str] = None
    date: str = ""
    type: str = TransactionType.EXPENSE.value
    category: str = ""
    amount: float = 0.0
    description: str = ""

    def __post_init__(self):
        if not self.id:
            import uuid
            self.id = str(uuid.uuid4())[:8]
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'type': self.type,
            'category': self.category,
            'amount': self.amount,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


@dataclass
class Budget:
    """Модель бюджета"""
    category: str
    limit: float
    period: str = "monthly"  # monthly, weekly, yearly
    spent: float = 0.0
    type: str = "expense"  # income или expense

    def remaining(self) -> float:
        return self.limit - self.spent

    def percentage_used(self) -> float:
        if self.limit == 0:
            return 0.0
        return (self.spent / self.limit) * 100


class Settings:
    """Настройки приложения"""

    def __init__(self):
        self.theme = "dark"
        self.currency = "₽"
        self.language = "ru"
        self.autosave = True
        self.save_interval = 5

    def to_dict(self):
        return {
            'theme': self.theme,
            'currency': self.currency,
            'language': self.language,
            'autosave': self.autosave,
            'save_interval': self.save_interval
        }

    @classmethod
    def from_dict(cls, data: Dict):
        settings = cls()
        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        return settings