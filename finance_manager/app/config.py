"""
Конфигурация приложения
"""
import os
from pathlib import Path


class Config:
    """Конфигурация приложения"""

    # Пути
    BASE_DIR = Path(__file__).parent.parent
    APP_DIR = BASE_DIR / "app"
    DATA_DIR = BASE_DIR / "data"

    # Файлы
    ICONS_DIR = APP_DIR / "icons"

    # Настройки приложения
    APP_NAME = "Personal Finance Manager"
    VERSION = "1.0.0"
    COMPANY = "Finance Solutions Inc."

    # Настройки окна
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    # Цвета
    COLORS = {
        'primary': '#1E3A8A',  # Deep Blue
        'secondary': '#10B981',  # Green
        'accent': '#8B5CF6',  # Purple
        'danger': '#EF4444',  # Red
        'warning': '#F59E0B',  # Orange
        'success': '#10B981',  # Green
        'info': '#3B82F6',  # Blue
        'dark': '#1F2937',  # Dark Gray
        'light': '#F9FAFB',  # Light Gray
    }

    # Стили
    FONTS = {
        'title': ('Arial', 18, 'bold'),
        'heading': ('Arial', 16, 'bold'),
        'subheading': ('Arial', 14, 'bold'),
        'normal': ('Arial', 12),
        'small': ('Arial', 10),
    }

    @classmethod
    def setup_directories(cls):
        """Создание необходимых директорий"""
        directories = [
            cls.DATA_DIR,
            cls.ICONS_DIR,
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True)