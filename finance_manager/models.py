from dataclasses import dataclass
from enum import Enum


@dataclass
class Transaction:
    """Модель транзакции"""
    date: str
    type: str  # 'income' или 'expense'
    category: str
    amount: float
    description: str


@dataclass
class Budget:
    """Модель бюджета"""
    category: str
    limit: float
    period: str


class TransactionType(Enum):
    """Типы транзакций"""
    INCOME = "income"
    EXPENSE = "expense"
